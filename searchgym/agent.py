"""검색 에이전트 — vLLM OpenAI 호환 서버 위의 도구 루프.

세 모델 모두 같은 코드로 돈다. 다른 것은 서빙 플래그(serving.py)뿐이다.
도구 실행이 우리 프로세스 안에 있으므로 세 가지가 가능하다.

    1. **검색 예산.** 상한을 넘으면 도구를 뺏는 대신 "한도 초과, 이제 답하라"를
       도구 결과로 돌려준다. 모델이 스스로 마무리하게 두는 쪽이 안전하다.
    2. **컨텍스트 상한.** 대화 토큰을 계속 세다가 상한에 닿으면 도구 결과를 남은
       만큼만 잘라 넣고 답을 강제한다. 컨텍스트 초과로 실행이 통째로 죽는 것을 막는다.
    3. **정제(Search-o1의 Reason-in-Documents).** 페치 원문을 메인 대화에 넣지 않고,
       같은 모델에게 직전 추론·현재 질의와 함께 넘겨 필요한 것만 뽑아 넣는다.
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

SEARCH_EXHAUSTED = (
    "web_search limit reached — you have used all {used} of your {limit} searches and "
    "no further search will run. Answer the question now from what you have gathered."
)
CONTEXT_EXHAUSTED = (
    "\n\n[Context limit reached. The result above was truncated and no further tool "
    "output can be added. Answer the question now from what you have gathered.]"
)


@dataclass(slots=True)
class AgentConfig:
    base_url: str = "http://127.0.0.1:8000/v1"
    api_key: str = "EMPTY"  # vLLM은 키를 검사하지 않는다
    max_tokens: int = 8192
    # 검색 예산. 넘어도 차단하지 않고 "이제 답하라"를 돌려준다.
    max_searches: int = 20
    # 0이면 무제한. 페치는 정제를 거쳐 짧게 들어가므로 굳이 막지 않는다.
    max_fetches: int = 0
    max_turns: int = 40
    # 대화 컨텍스트 상한. 서버의 --max-model-len에서 답변 여유를 뺀 값으로 둔다
    # (128000 - 8000 = 120000). 도구 결과가 이 선을 넘기면 잘라 넣는다.
    context_limit: int = 120_000
    # 페치 원문을 같은 모델로 압축해 넣는다(Search-o1 방식).
    refine_fetched: bool = True
    # 정제기의 출력 상한. 정제 호출은 페이지 하나만 단독으로 받으므로 넉넉히 준다 —
    # 이건 상한이지 목표가 아니고, 대부분의 정제는 한참 못 미친다.
    refine_max_tokens: int = 32768
    # 정제기에 넣을 **원문**의 토큰 상한. 도구 서버는 어떤 모델이 떠 있는지 모르므로
    # 자 단위로만 자른다(FETCH_MAX_CHARS). 토큰 단위 절단은 모델을 아는 여기서 한다.
    refine_max_document_tokens: int = 50_000
    # 비우면 모델 프로파일의 기본값을 쓴다(gpt-oss는 medium). 덮어쓸 때만 채운다.
    reasoning_effort: str = ""
    timeout_s: float = 600.0


@dataclass(slots=True)
class Step:
    """한 턴에 모델이 한 일. response.json의 단위."""

    turn: int
    reasoning: str = ""
    text: str = ""
    tool_calls: list[ToolCall] = field(default_factory=list)

    def as_dict(self, full: bool = True) -> dict[str, Any]:
        return {
            "turn": self.turn,
            "reasoning": self.reasoning,
            "text": self.text,
            "tool_calls": [c.as_dict(full) for c in self.tool_calls],
        }


@dataclass(slots=True)
class RunResult:
    """한 문항 실행 결과. 어떤 모델이든 같은 형태다."""

    answer: str = ""
    steps: list[Step] = field(default_factory=list)
    # Search-o1 정제 기록. 원문까지 들고 있어 무거우므로 캐시에는 넣지 않는다.
    refinements: list[dict[str, Any]] = field(default_factory=list)
    usage: Usage = field(default_factory=Usage)
    turns: int = 0
    stop_reason: str = ""
    latency_ms: float = 0.0
    context_tokens: int = 0
    error: str | None = None

    @property
    def tool_calls(self) -> list[ToolCall]:
        return [c for s in self.steps for c in s.tool_calls]

    @property
    def reasoning(self) -> str:
        """턴별 추론을 이어 붙인 것. 사람이 훑어볼 때 쓴다."""
        return "\n\n".join(f"[turn {s.turn}] {s.reasoning}" for s in self.steps if s.reasoning)

    @property
    def searches(self) -> int:
        return sum(1 for c in self.tool_calls if c.name == "web_search" and not c.refused)

    @property
    def fetches(self) -> int:
        return sum(1 for c in self.tool_calls if c.name == "web_fetch" and not c.refused)

    @property
    def queries(self) -> list[str]:
        return [c.query for c in self.tool_calls if c.name == "web_search" and c.query]

    @property
    def urls(self) -> list[str]:
        return [c.url for c in self.tool_calls if c.name == "web_fetch" and c.url]

    def as_dict(self) -> dict[str, Any]:
        """캐시와 트레이스에 들어가는 슬림 버전(도구 결과 본문 제외)."""
        return {
            "answer": self.answer,
            "stop_reason": self.stop_reason,
            "turns": self.turns,
            "searches": self.searches,
            "fetches": self.fetches,
            "context_tokens": self.context_tokens,
            "steps": [s.as_dict(full=False) for s in self.steps],
            "usage": self.usage.as_dict(),
            "latency_ms": round(self.latency_ms, 1),
            "error": self.error,
        }

    def as_response(self) -> dict[str, Any]:
        """response.json — 추론·응답·도구 호출·도구 결과를 전부 담는다."""
        return {**self.as_dict(), "steps": [s.as_dict(full=True) for s in self.steps]}

    def render_trajectory(self) -> str:
        """교사 피드백에 들어갈 사람이 읽는 궤적."""
        calls = self.tool_calls
        if not calls:
            return "(the agent answered without using any tool)"
        lines = []
        for i, call in enumerate(calls, 1):
            label = "search" if call.name == "web_search" else "open  "
            detail = f'"{call.query}"' if call.name == "web_search" else call.url
            note = "  [refused: budget]" if call.refused else ("  [failed]" if call.is_error else "")
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
        self._http: Any = None  # /tokenize용. 처음 쓸 때 만든다

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

        specs = [spec for spec in tools.specs]
        trace.event(
            "run.start",
            model=self.profile.repo,
            question=question,
            system_prompt=system,
            budget={
                "searches": cfg.max_searches,
                "fetches": cfg.max_fetches or "unlimited",
                "context_tokens": cfg.context_limit,
            },
        )

        try:
            for turn in range(1, cfg.max_turns + 1):
                result.turns = turn
                step = Step(turn=turn)
                result.steps.append(step)

                trace.event("llm.request", turn=turn, context_tokens=result.context_tokens)
                message = await self._complete(messages, specs, result)

                step.reasoning = str(getattr(message, "reasoning_content", "") or "")
                step.text = str(message.content or "")
                calls = list(getattr(message, "tool_calls", None) or [])
                trace.event(
                    "llm.response",
                    turn=turn,
                    reasoning_chars=len(step.reasoning),
                    text=step.text[:2000],
                    tool_calls=[c.function.name for c in calls],
                )

                if not calls:
                    result.answer = step.text.strip()
                    result.stop_reason = "answered"
                    break

                messages.append(_assistant_message(message, calls))
                for call in calls:
                    output = await self._run_tool(call, tools, result, step, trace)
                    messages.append(
                        {"role": "tool", "tool_call_id": call.id, "content": output}
                    )
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
            "tools": [t.as_openai() for t in tools],
            "tool_choice": "auto",
            **self.profile.sampling,
        }
        response = await self._client.chat.completions.create(**request)
        if usage := response.usage:
            details = getattr(usage, "completion_tokens_details", None)
            result.usage.add(
                usage.prompt_tokens,
                usage.completion_tokens,
                getattr(details, "reasoning_tokens", 0) if details else 0,
            )
            # 서버가 센 값이 가장 정확하다. 다음 턴의 컨텍스트 크기는 이번 프롬프트
            # 더하기 이번 출력이다.
            result.context_tokens = (usage.prompt_tokens or 0) + (usage.completion_tokens or 0)
        return response.choices[0].message

    async def _run_tool(
        self, call: Any, tools: WebTools, result: RunResult, step: Step, trace: Trace
    ) -> str:
        cfg = self.config
        name = call.function.name
        arguments = _parse_arguments(call.function.arguments)
        # 예산은 **이 호출을 빼고** 지금까지 실행된 횟수로 센다. 기록을 먼저 붙이면
        # 자기 자신을 세어 한 번씩 덜 쓰게 된다.
        used = result.searches if name == "web_search" else result.fetches
        record = ToolCall(name=name, arguments=arguments)
        step.tool_calls.append(record)

        # 1) 예산 — 차단이 아니라 안내를 돌려준다.
        if name == "web_search" and used >= cfg.max_searches:
            notice = SEARCH_EXHAUSTED.format(used=used, limit=cfg.max_searches)
            record.refused, record.result = True, notice
            trace.event("budget.search_exhausted", turn=step.turn, used=used)
            return notice
        if name == "web_fetch" and cfg.max_fetches and used >= cfg.max_fetches:
            notice = (
                f"web_fetch limit reached — you have used all {used} of your "
                f"{cfg.max_fetches} fetches. Answer the question now from what you have."
            )
            record.refused, record.result = True, notice
            trace.event("budget.fetch_exhausted", turn=step.turn, used=used)
            return notice

        trace.event("tool.call", turn=step.turn, tool=name, arguments=arguments)
        outcome = await tools.call(name, arguments)
        record.is_error = outcome.is_error
        record.duration_ms = outcome.duration_ms
        text = outcome.text

        # 2) 페치 원문은 메인 대화에 넣지 않는다. 정제한 것만 넣는다.
        if name == "web_fetch" and not outcome.is_error and cfg.refine_fetched:
            text = await self._refine(arguments.get("url", ""), text, result, step)

        # 3) 컨텍스트 상한 — 남은 만큼만 넣고 답을 강제한다.
        text, truncated = await self._fit(text, result)
        if truncated:
            trace.event(
                "budget.context_exhausted",
                turn=step.turn,
                context_tokens=result.context_tokens,
                limit=cfg.context_limit,
            )

        record.result = _parse_result(name, text)
        record.result_chars = len(text)
        trace.event(
            "tool.result",
            turn=step.turn,
            tool=name,
            arguments=arguments,
            is_error=outcome.is_error,
            duration_ms=round(outcome.duration_ms, 1),
            raw_chars=len(outcome.text),
            result_chars=len(text),
            truncated=truncated,
        )
        return text

    async def _fit(self, text: str, result: RunResult) -> tuple[str, bool]:
        """도구 결과가 컨텍스트 상한을 넘기면 남은 토큰만큼만 남긴다."""
        remaining = self.config.context_limit - result.context_tokens
        if remaining <= 0:
            return CONTEXT_EXHAUSTED.strip(), True

        # 대개는 근사치로 충분하다. 경계 근처에서만 서버에 정확한 수를 묻는다.
        if _estimate_tokens(text) < remaining * 0.9:
            return text, False

        exact = await self._count_tokens(text)
        if exact <= remaining:
            return text, False
        # 이 텍스트의 실제 토큰당 문자 수로 자를 지점을 잡는다.
        keep = max(0, int(remaining * len(text) / max(exact, 1)))
        return text[:keep] + CONTEXT_EXHAUSTED, True

    async def _cap(self, text: str, limit_tokens: int) -> tuple[str, bool]:
        """텍스트를 토큰 상한에 맞춰 자른다. 모델 토크나이저 기준이다."""
        if limit_tokens <= 0 or _estimate_tokens(text) < limit_tokens * 0.9:
            return text, False
        exact = await self._count_tokens(text)
        if exact <= limit_tokens:
            return text, False
        keep = max(0, int(limit_tokens * len(text) / max(exact, 1)))
        return text[:keep], True

    async def _count_tokens(self, text: str) -> int:
        """**돌리는 모델의 토크나이저로** 센다 — vLLM의 /tokenize.

        tiktoken 같은 남의 인코딩은 어휘가 달라 수백 토큰씩 어긋난다. 컨텍스트
        경계를 다루는 자리라 서버에 직접 묻는다. 실패하면 근사치로 물러선다.
        """
        try:
            import httpx

            if self._http is None:
                self._http = httpx.AsyncClient(timeout=30.0)
            root = self.config.base_url.rstrip("/").removesuffix("/v1")
            response = await self._http.post(
                f"{root}/tokenize", json={"model": self.profile.repo, "prompt": text}
            )
            return int(response.json()["count"])
        except Exception:
            return _estimate_tokens(text)

    async def _refine(self, url: str, page: str, result: RunResult, step: Step) -> str:
        """페치 원문을 같은 모델로 압축한다(Search-o1의 Reason-in-Documents).

        직전 추론과 가장 최근 검색어를 함께 넘겨, 지금 알아내려는 것에 맞춰 뽑게 한다.
        이 호출이 실패하면 원문을 그대로 쓴다 — 정제는 최적화이지 정확성 요건이 아니다.
        """
        document, doc_truncated = await self._cap(page, self.config.refine_max_document_tokens)
        prompt = REFINE_PROMPT.format(
            prev_reasoning=_previous_reasoning(result) or "(none yet)",
            search_query=_latest_query(result) or "(no search issued yet)",
            document=document,
        )
        started = time.perf_counter()
        refined, error = page, None
        try:
            response = await self._client.chat.completions.create(
                model=self.profile.repo,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=self.config.refine_max_tokens,
            )
        except Exception as exc:
            error = repr(exc)
        else:
            if usage := response.usage:
                result.usage.add(usage.prompt_tokens, usage.completion_tokens)
            refined = (response.choices[0].message.content or "").strip() or page

        result.refinements.append(
            {
                "turn": step.turn,
                "url": url,
                "search_query": _latest_query(result),
                "prev_reasoning": _previous_reasoning(result),
                "document_chars": len(page),
                "document_truncated": doc_truncated,
                "document": page,  # jina 원문 전체. search_o1.json에만 남는다
                "refined": refined,
                "refined_chars": len(refined),
                "latency_ms": round((time.perf_counter() - started) * 1000, 1),
                "error": error,
            }
        )
        return refined


# --- 도우미 -----------------------------------------------------------------


def _system_prompt(system_prompt: str | None, reasoning_effort: str) -> str:
    """gpt-oss는 추론 강도를 시스템 프롬프트 한 줄로 받는다."""
    parts = [p for p in (system_prompt or "").strip().splitlines()]
    if reasoning_effort:
        parts = [f"Reasoning: {reasoning_effort}", *parts]
    return "\n".join(parts).strip()


def _previous_reasoning(result: RunResult) -> str:
    """정제기에 넘길 직전 추론 블록."""
    for step in reversed(result.steps):
        if step.reasoning:
            return step.reasoning
    return ""


def _latest_query(result: RunResult) -> str:
    for call in reversed(result.tool_calls):
        if call.name == "web_search" and call.query:
            return call.query
    return ""


def _parse_result(name: str, text: str) -> Any:
    """검색 결과는 구조를 살려 저장한다(title/link/snippet). 나머지는 문자열."""
    if name != "web_search":
        return text
    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError):
        return text


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


def _estimate_tokens(text: str) -> int:
    """빠른 근사치. 정확한 값은 SearchAgent._count_tokens(서버 /tokenize)가 준다."""
    return max(1, len(text) // 3)


REFINE_PROMPT = """\
**Task Instruction:**

You are tasked with reading and analyzing a fetched web page based on the following inputs: **Previous Reasoning Steps**, **Current Search Query**, and the **Fetched Web Page**. Your objective is to extract relevant and helpful information for **Current Search Query** from the **Fetched Web Page** and seamlessly integrate this information into the **Previous Reasoning Steps** to continue reasoning for the original question.

**Guidelines:**

1. **Analyze the Fetched Web Page:**
- Carefully review the content of the fetched web page.
- Identify factual information that is relevant to the **Current Search Query** and can aid in the reasoning process for the original question.

2. **Extract Relevant Information:**
- Select the information from the Fetched Web Page that directly contributes to advancing the **Previous Reasoning Steps**.
- Ensure that the extracted information is accurate and relevant.

3. **Output Format:**
- **If the web page provides helpful information for current search query:** Present the information beginning with `**Final Information**` as shown below.
**Final Information**

[Helpful information]

- **If the web page does not provide any helpful information for current search query:** Output the following text.
**Final Information**

No helpful information found.

**Inputs:**
- **Previous Reasoning Steps:**
{prev_reasoning}

- **Current Search Query:**
{search_query}

- **Fetched Web Page:**
{document}

Now you should analyze the web page and find helpful information based on the current search query "{search_query}" and previous reasoning steps.
"""
