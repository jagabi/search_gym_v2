"""vLLM OpenAI 호환 서버 하나를 감싼 얇은 래퍼.

메인 에이전트와 explorer 가 **같은 엔드포인트, 같은 모델**을 쓰므로 호출 경로를
여기 하나로 모은다. 토크나이저를 아는 것도 이 계층이다 — 컨텍스트 절단은 서버의
`/tokenize` 로 재야 하고, tiktoken 같은 남의 인코딩은 어휘가 달라 수백 토큰씩
어긋난다.

확장 사고는 **항상 켠다**. 모델마다 기본값이 반대라(gemma-4 OFF / qwen3.5 ON)
명시하지 않으면 비교가 성립하지 않고, Search-o1 의 결과가 추론 모델을 전제로
하기 때문이다(논문 §4.4: "ordinary LLMs cannot effectively utilize search as a
tool"). gpt-oss 만 시스템 프롬프트 한 줄로 강도를 받으므로 프로파일이 그 값을 준다.
"""

from __future__ import annotations

import asyncio
import json
import re
from dataclasses import dataclass, field
from types import SimpleNamespace
from typing import Any
from uuid import uuid4

from openai import AsyncOpenAI

from .serving import ServeProfile

# 서버측 5xx 재시도. harmony 파서가 한 샘플에서 죽는 일이 있어 다시 뽑으면 지나간다.
_MAX_SERVER_RETRIES = 2
_RETRY_BACKOFF_S = 1.0

__all__ = ["LLM", "Reply", "Usage"]


def normalize_tool_names(reply: Reply, tools: list[dict[str, Any]] | None) -> list[dict]:
    """Repair only observed, unambiguous channel/header residue on offered names."""
    changes = []
    for call in reply.tool_calls:
        raw = call.function.name
        for spec in tools or []:
            name = spec["function"]["name"]
            if raw != name and re.fullmatch(re.escape(name) + r"(?:\]|json|<\|channel\|>json)", raw):
                call.function.name = name
                changes.append({"raw": raw, "name": name})
                break
    return changes


def history_tool_call(call: Any) -> dict:
    """Keep malformed output in traces, never replay broken JSON/channel syntax."""
    name = call.function.name
    try:
        args = json.loads(call.function.arguments)
        if not isinstance(args, dict):
            args = {}
    except (ValueError, TypeError):
        args = {}
    return {"id": call.id, "type": "function", "function": {
        "name": name if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_-]{0,63}", name) else "invalid_tool_call",
        "arguments": json.dumps(args, ensure_ascii=False)}}


def recover_tool_calls(reply: Reply, tools: list[dict[str, Any]] | None) -> bool:
    """Recover one leaked Harmony call, only with an offered name and intact JSON.

    Some server responses put a tool envelope in content and return tool_calls=[].
    Do not infer a call from reasoning, quoted examples, or incomplete arguments.
    The normal tool dispatcher still applies argument and budget validation.
    """
    if reply.tool_calls or reply.truncated or not tools:
        return False
    raw = (reply.text or "").strip()
    if not raw.startswith(("<|start|>", "<|im_start|>")):
        return False
    brace = raw.find("{")
    if brace < 0:
        return False
    token = r"<\|[^|>]{0,64}\|>"
    header = re.sub(token, "", raw[:brace])
    match = re.fullmatch(
        r"assistant\s*(?:(?:commentary|analysis)\s*)?to=functions\.([a-zA-Z_][\w]*)[\s\]}>:]*",
        header,
    )
    if not match or match.group(1) not in {t["function"]["name"] for t in tools}:
        return False
    try:
        arguments, end = json.JSONDecoder().raw_decode(raw[brace:])
    except (ValueError, RecursionError):
        return False
    if not isinstance(arguments, dict) or re.sub(token, "", raw[brace + end:]).strip():
        return False
    reply.tool_calls = [SimpleNamespace(
        id="recovered_" + uuid4().hex, type="function",
        function=SimpleNamespace(name=match.group(1), arguments=json.dumps(arguments, ensure_ascii=False)),
    )]
    return True


@dataclass(slots=True)
class Usage:
    input_tokens: int = 0
    output_tokens: int = 0
    reasoning_tokens: int = 0
    calls: int = 0

    def add(self, prompt: int | None, completion: int | None, reasoning: int | None = 0) -> None:
        self.input_tokens += prompt or 0
        self.output_tokens += completion or 0
        self.reasoning_tokens += reasoning or 0
        self.calls += 1

    def merge(self, other: Usage) -> None:
        self.input_tokens += other.input_tokens
        self.output_tokens += other.output_tokens
        self.reasoning_tokens += other.reasoning_tokens
        self.calls += other.calls

    def as_dict(self) -> dict[str, int]:
        return {
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "reasoning_tokens": self.reasoning_tokens,
            "calls": self.calls,
        }


@dataclass(slots=True)
class Reply:
    """한 번의 chat.completions 결과에서 우리가 쓰는 것만."""

    reasoning: str = ""
    text: str = ""
    tool_calls: list[Any] = field(default_factory=list)
    finish_reason: str = ""
    prompt_tokens: int = 0
    completion_tokens: int = 0

    @property
    def truncated(self) -> bool:
        """max_tokens 에 걸려 끊긴 응답. 이건 답변이 아니다."""
        return self.finish_reason == "length"

    @property
    def context_tokens(self) -> int:
        return self.prompt_tokens + self.completion_tokens


class LLM:
    def __init__(
        self,
        profile: ServeProfile,
        base_url: str,
        api_key: str = "EMPTY",
        timeout_s: float = 600.0,
        model_name: str = "",
    ) -> None:
        self.profile = profile
        self.base_url = base_url
        self.api_key = api_key
        # 팟이 서빙하는 이름. 기성 이미지는 --served-model-name 을 우리가 못 정할 수
        # 있으므로 덮어쓸 수 있게 둔다. tests/model.py 가 서버의 이름 목록을 찍어 준다.
        self.model_name = model_name or profile.repo
        self._client = AsyncOpenAI(base_url=base_url, api_key=api_key, timeout=timeout_s)
        self._http: Any = None  # /tokenize 용. 처음 쓸 때 만든다

    # --- 생성 ---------------------------------------------------------------

    async def chat(
        self,
        messages: list[dict[str, Any]],
        *,
        max_tokens: int,
        tools: list[dict[str, Any]] | None = None,
        usage: Usage | None = None,
        tool_choice: str | None = None,
    ) -> Reply:
        request: dict[str, Any] = {
            "model": self.model_name,
            "messages": messages,
            "max_tokens": max_tokens,
            **self.profile.sampling,
        }
        if tools and tool_choice != "none":
            request["tools"] = tools
            request["tool_choice"] = tool_choice or "auto"
        elif tool_choice == "none":
            request["tool_choice"] = "none"

        # extra_body 는 한 번에 합쳐 넣는다(두 곳에서 따로 주면 서로 덮어쓴다).
        extra = dict(self.profile.sampling_extra)
        if self.profile.thinking_kwarg:
            extra["chat_template_kwargs"] = {"enable_thinking": True}
        if extra:
            request["extra_body"] = extra

        response = await self._create(request)
        choice = response.choices[0]
        message = choice.message

        # vLLM chat completions has used both names across releases.  GPT-OSS
        # on v0.28 emits ``reasoning`` while several earlier servers emit
        # ``reasoning_content``.
        reply = Reply(
            reasoning=str(
                getattr(message, "reasoning_content", None)
                or getattr(message, "reasoning", "")
                or ""
            ),
            text=str(message.content or ""),
            tool_calls=list(getattr(message, "tool_calls", None) or []),
            finish_reason=str(getattr(choice, "finish_reason", "") or ""),
        )
        if raw := response.usage:
            details = getattr(raw, "completion_tokens_details", None)
            reply.prompt_tokens = raw.prompt_tokens or 0
            reply.completion_tokens = raw.completion_tokens or 0
            if usage is not None:
                usage.add(
                    raw.prompt_tokens,
                    raw.completion_tokens,
                    self._reasoning_tokens(details, reply.reasoning),
                )
        elif usage is not None:
            usage.calls += 1
        return reply

    async def _create(self, request: dict[str, Any]) -> Any:
        """생성 호출. **서버측 5xx 는 다시 뽑는다.**

        vLLM 의 harmony 파서가 gpt-oss 의 출력을 파싱하다 500 으로 죽는 일이 있다
        (실측: 30문항에 1건).

            500 unexpected tokens remaining in message header: Some("...")

        모델이 채널 토큰을 흘리거나 메시지가 어중간하게 끝나면 나는데, 요청이 아니라
        **그 한 번의 샘플**이 문제라 같은 요청을 다시 보내면 대개 지나간다
        (temperature 1.0 이므로 다시 뽑으면 다른 출력이다). 재시도가 없으면 500 한
        번에 문항 전체가 죽어 답이 0자로 남는다.

        4xx 는 우리 요청이 틀린 것이므로 재시도하지 않는다 — 그대로 올린다.
        """
        last: Exception | None = None
        for attempt in range(_MAX_SERVER_RETRIES + 1):
            try:
                return await self._client.chat.completions.create(**request)
            except Exception as exc:  # noqa: BLE001 — 상태 코드로 갈라낸다
                status = getattr(exc, "status_code", None)
                if status is None or status < 500 or attempt == _MAX_SERVER_RETRIES:
                    raise
                last = exc
                await asyncio.sleep(_RETRY_BACKOFF_S * (attempt + 1))
        raise last  # pragma: no cover — 위 루프에서 반드시 반환하거나 raise 한다

    @staticmethod
    def _reasoning_tokens(details: Any, reasoning: str) -> int:
        """사고 토큰 수. 서버가 세 주면 그것을, 아니면 근사한다.

        vLLM 은 gpt-oss 의 `completion_tokens_details.reasoning_tokens` 를 채우지
        않는다(실측: `reasoning_content` 는 멀쩡히 오는데 이 값만 0). 그대로 두면
        세 방법의 사고량 비교가 통째로 0 이 되므로, 값이 없을 때만 텍스트에서
        근사한다. 근사치라는 사실은 여기에만 있으면 된다 — 방법 간 비교에 쓰는
        값이라 셋 모두 같은 방식으로 세면 편향이 없다.
        """
        reported = getattr(details, "reasoning_tokens", None) if details else None
        if reported:
            return int(reported)
        return estimate_tokens(reasoning) if reasoning else 0

    # --- 토큰 ---------------------------------------------------------------

    async def count_tokens(self, text: str) -> int:
        """**돌리는 모델의 토크나이저로** 센다. 실패하면 근사치로 물러선다."""
        try:
            import httpx

            if self._http is None:
                headers = {}
                if self.api_key and self.api_key != "EMPTY":
                    headers["Authorization"] = f"Bearer {self.api_key}"
                self._http = httpx.AsyncClient(timeout=30.0, headers=headers or None)
            root = self.base_url.rstrip("/").removesuffix("/v1")
            response = await self._http.post(
                f"{root}/tokenize", json={"model": self.model_name, "prompt": text}
            )
            return int(response.json()["count"])
        except Exception:
            return estimate_tokens(text)

    async def cap(self, text: str, limit_tokens: int) -> tuple[str, bool]:
        """토큰 상한에 맞춰 자른다. 경계 근처에서만 서버에 정확한 수를 묻는다."""
        if limit_tokens <= 0 or estimate_tokens(text) < limit_tokens * 0.9:
            return text, False
        exact = await self.count_tokens(text)
        if exact <= limit_tokens:
            return text, False
        # 이 텍스트의 실제 토큰당 문자 수로 자를 지점을 잡는다.
        keep = max(0, int(limit_tokens * len(text) / max(exact, 1)))
        return text[:keep], True

    async def aclose(self) -> None:
        if self._http is not None:
            await self._http.aclose()
            self._http = None


def estimate_tokens(text: str) -> int:
    """빠른 근사치. 정확한 값은 LLM.count_tokens 가 준다."""
    return max(1, len(text) // 3)
