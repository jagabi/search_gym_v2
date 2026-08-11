"""검색 에이전트 — vLLM OpenAI 호환 서버 위의 도구 루프.

세 모델 모두 같은 코드로 돈다. 다른 것은 서빙 플래그(serving.py)뿐이다.
도구 실행이 우리 프로세스 안에 있으므로 두 가지가 가능하다.

    1. **검색 예산 하드캡.** 벤더 서버측 루프에서는 못 하던 것이다. 예산이 떨어지면
       도구 목록을 회수하고 "이제 답하라"고 알린다.
    2. **정제(Search-o1의 Reason-in-Documents).** 페치한 원문을 메인 대화에 그대로
       넣지 않고, 같은 모델에게 한 번 더 물어 필요한 것만 요약해 넣는다. 원문이
       컨텍스트를 오염시키는 것을 막는다.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from typing import Any

from openai import AsyncOpenAI

from .serving import ServeProfile
from .tools import ToolSpec, WebTools
from .trace import ToolCall, Trace, Usage

__all__ = ["AgentConfig", "RunResult", "SearchAgent"]

FINISH_NOTICE = (
    "Search budget exhausted — no more tool calls are available. "
    "Answer now from what you have gathered."
)


@dataclass(slots=True)
class AgentConfig:
    base_url: str = "http://127.0.0.1:8000/v1"
    api_key: str = "EMPTY"  # vLLM은 키를 검사하지 않는다
    max_tokens: int = 4096
    # 검색 예산. 실측상 이 상한이 비용과 정확도를 동시에 좌우한다.
    max_searches: int = 20
    max_fetches: int = 10
    max_turns: int = 40
    # 페치 원문을 같은 모델로 한 번 압축해 넣는다(Search-o1 방식).
    refine_fetched: bool = True
    refine_max_tokens: int = 1024
    # 비우면 모델 프로파일의 기본값을 쓴다(gpt-oss는 medium). 덮어쓸 때만 채운다.
    reasoning_effort: str = ""
    timeout_s: float = 600.0


@dataclass(slots=True)
class RunResult:
    """한 문항 실행 결과. 어떤 모델이든 같은 형태다."""

    answer: str = ""
    reasoning: str = ""
    tool_calls: list[ToolCall] = field(default_factory=list)
    usage: Usage = field(default_factory=Usage)
    turns: int = 0
    stop_reason: str = ""
    latency_ms: float = 0.0
    error: str | None = None

    @property
    def searches(self) -> int:
        return sum(1 for c in self.tool_calls if c.name == "web_search")

    @property
    def fetches(self) -> int:
        return sum(1 for c in self.tool_calls if c.name == "web_fetch")

    @property
    def queries(self) -> list[str]:
        return [c.query for c in self.tool_calls if c.name == "web_search" and c.query]

    @property
    def urls(self) -> list[str]:
        return [c.url for c in self.tool_calls if c.name == "web_fetch" and c.url]

    def as_dict(self) -> dict[str, Any]:
        return {
            "answer": self.answer,
            "reasoning": self.reasoning,
            "stop_reason": self.stop_reason,
            "turns": self.turns,
            "searches": self.searches,
            "fetches": self.fetches,
            "tool_calls": [c.as_dict() for c in self.tool_calls],
            "usage": self.usage.as_dict(),
            "latency_ms": round(self.latency_ms, 1),
            "error": self.error,
        }

    def render_trajectory(self) -> str:
        """교사 피드백에 들어갈 사람이 읽는 궤적."""
        if not self.tool_calls:
            return "(the agent answered without using any tool)"
        lines = []
        for i, call in enumerate(self.tool_calls, 1):
            label = "search" if call.name == "web_search" else "open  "
            detail = f'"{call.query}"' if call.name == "web_search" else call.url
            note = "  [failed]" if call.is_error else ""
            lines.append(f"{i:>3}. {label}  {detail}{note}")
        return "\n".join(lines)


class SearchAgent:
    def __init__(self, profile: ServeProfile, config: AgentConfig | None = None) -> None:
        self.profile = profile
        self.config = config or AgentConfig()
        self._client = AsyncOpenAI(
            base_url=self.config.base_url,
            api_key=self.config.api_key,
            timeout=self.config.timeout_s,
        )

    async def run(
        self,
        question: str,
        system_prompt: str | None,
        tools: WebTools,
        trace: Trace,
    ) -> RunResult:
        cfg = self.config
        result = RunResult()
        started = time.perf_counter()

        system = _system_prompt(
            system_prompt, cfg.reasoning_effort or self.profile.reasoning_effort
        )
        messages: list[dict[str, Any]] = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": question})

        specs = {spec.name: spec for spec in tools.specs}
        trace.event(
            "run.start",
            model=self.profile.repo,
            question=question,
            system_prompt=system,
            budget={"searches": cfg.max_searches, "fetches": cfg.max_fetches},
        )

        try:
            for turn in range(1, cfg.max_turns + 1):
                result.turns = turn
                exhausted = result.searches >= cfg.max_searches and result.fetches >= cfg.max_fetches
                available = [] if exhausted else _available(specs, result, cfg)

                trace.event("llm.request", turn=turn, tools=[t.name for t in available])
                message = await self._complete(messages, available, result)

                calls = list(getattr(message, "tool_calls", None) or [])
                trace.event(
                    "llm.response",
                    turn=turn,
                    text=(message.content or "")[:2000],
                    tool_calls=[c.function.name for c in calls],
                )

                if reasoning := getattr(message, "reasoning_content", None):
                    result.reasoning = reasoning

                if not calls:
                    result.answer = (message.content or "").strip()
                    result.stop_reason = "answered"
                    break

                messages.append(_assistant_message(message, calls))
                for call in calls:
                    output = await self._run_tool(call, tools, result, trace)
                    messages.append(
                        {"role": "tool", "tool_call_id": call.id, "content": output}
                    )

                if not exhausted and _just_exhausted(result, cfg):
                    trace.event("budget.exhausted", searches=result.searches, fetches=result.fetches)
                    messages.append({"role": "user", "content": FINISH_NOTICE})
            else:
                result.stop_reason = "max_turns"
                trace.event("run.truncated", reason="max_turns", turns=cfg.max_turns)
        except Exception as exc:
            result.error = repr(exc)
            result.stop_reason = "error"
            trace.event("run.error", error=result.error)

        result.latency_ms = (time.perf_counter() - started) * 1000
        trace.event("run.end", **result.as_dict())
        return result

    # --- 내부 ---------------------------------------------------------------

    async def _complete(
        self, messages: list[dict[str, Any]], tools: list[ToolSpec], result: RunResult
    ) -> Any:
        request: dict[str, Any] = {
            "model": self.profile.repo,
            "messages": messages,
            "max_tokens": self.config.max_tokens,
            **self.profile.sampling,
        }
        if tools:
            request["tools"] = [t.as_openai() for t in tools]
            request["tool_choice"] = "auto"

        response = await self._client.chat.completions.create(**request)
        if usage := response.usage:
            details = getattr(usage, "completion_tokens_details", None)
            result.usage.add(
                usage.prompt_tokens,
                usage.completion_tokens,
                getattr(details, "reasoning_tokens", 0) if details else 0,
            )
        return response.choices[0].message

    async def _run_tool(
        self, call: Any, tools: WebTools, result: RunResult, trace: Trace
    ) -> str:
        name = call.function.name
        arguments = _parse_arguments(call.function.arguments)
        trace.event("tool.call", tool=name, arguments=arguments)

        outcome = await tools.call(name, arguments)
        text = outcome.text
        if name == "web_fetch" and not outcome.is_error and self.config.refine_fetched:
            text = await self._refine(arguments.get("url", ""), text, result)

        result.tool_calls.append(
            ToolCall(
                name=name,
                arguments=arguments,
                result_chars=len(text),
                is_error=outcome.is_error,
                duration_ms=outcome.duration_ms,
            )
        )
        trace.event(
            "tool.result",
            tool=name,
            arguments=arguments,
            is_error=outcome.is_error,
            duration_ms=round(outcome.duration_ms, 1),
            raw_chars=len(outcome.text),
            result_chars=len(text),
        )
        return text

    async def _refine(self, url: str, page: str, result: RunResult) -> str:
        """페치 원문을 같은 모델로 압축한다(Search-o1의 Reason-in-Documents).

        원문은 메인 대화에 절대 들어가지 않는다. 이 호출이 실패하면 압축 없이
        원문을 쓴다 — 정제는 최적화이지 정확성 요건이 아니다.
        """
        try:
            response = await self._client.chat.completions.create(
                model=self.profile.repo,
                messages=[{"role": "user", "content": _REFINE_PROMPT.format(url=url, page=page)}],
                max_tokens=self.config.refine_max_tokens,
                temperature=0.0,
            )
        except Exception:
            return page
        if usage := response.usage:
            result.usage.add(usage.prompt_tokens, usage.completion_tokens)
        return (response.choices[0].message.content or "").strip() or page


def _system_prompt(system_prompt: str | None, reasoning_effort: str) -> str:
    """gpt-oss는 추론 강도를 시스템 프롬프트 한 줄로 받는다."""
    parts = [p for p in (system_prompt or "").strip().splitlines()]
    if reasoning_effort:
        parts = [f"Reasoning: {reasoning_effort}", *parts]
    return "\n".join(parts).strip()


def _available(specs: dict[str, ToolSpec], result: RunResult, cfg: AgentConfig) -> list[ToolSpec]:
    """예산이 남은 도구만 노출한다. 상한에 닿은 도구는 목록에서 사라진다."""
    names = []
    if result.searches < cfg.max_searches:
        names.append("web_search")
    if result.fetches < cfg.max_fetches:
        names.append("web_fetch")
    return [specs[name] for name in names if name in specs]


def _just_exhausted(result: RunResult, cfg: AgentConfig) -> bool:
    return result.searches >= cfg.max_searches and result.fetches >= cfg.max_fetches


def _assistant_message(message: Any, calls: list[Any]) -> dict[str, Any]:
    return {
        "role": "assistant",
        "content": message.content or "",
        "tool_calls": [
            {
                "id": c.id,
                "type": "function",
                "function": {"name": c.function.name, "arguments": c.function.arguments},
            }
            for c in calls
        ],
    }


def _parse_arguments(raw: str | None) -> dict[str, Any]:
    if not raw:
        return {}
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        return {"_raw": raw}
    return parsed if isinstance(parsed, dict) else {"_value": parsed}


_REFINE_PROMPT = """\
Below is a web page fetched while researching a question. Extract only what a
researcher could use, and drop everything else.

Keep: concrete facts, figures, dates, names, and any statement that answers or
narrows a question. Keep the exact numbers and their units. Note the page's own
title and what kind of source it is.
Drop: navigation, boilerplate, ads, and prose that carries no fact.

If the page contains nothing useful, reply with exactly: NO USEFUL CONTENT

URL: {url}

---
{page}
---

Extracted facts:"""
