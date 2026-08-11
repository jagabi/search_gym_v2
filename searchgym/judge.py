"""판정 모델 — Gemini + structured output.

자유 텍스트를 정규식으로 파싱하면 포맷이 조금만 흔들려도 무효 판정이 되므로,
벤치마크가 만들어 준 JSON 스키마를 `response_json_schema`로 강제한다.

판정 실패는 그 문항을 0점으로 만든다(집계에서 judge_error로 따로 센다). 일시적인
오류 하나가 학습 신호를 오염시키므로 재시도를 넉넉히 준다.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass
from typing import Any

from google import genai
from google.genai import types

from .benchmarks import Benchmark, Item
from .paths import require_env
from .scoring import Judgement

__all__ = ["Judge", "JudgeConfig"]


@dataclass(slots=True)
class JudgeConfig:
    model: str = "gemini-3.6-flash"
    thinking_level: str = "low"
    temperature: float = 0.0
    max_retries: int = 8


class Judge:
    """문항 하나를 채점해 `Judgement`로 돌려준다. 스레드에서 같이 써도 된다."""

    def __init__(self, config: JudgeConfig | None = None) -> None:
        self.config = config or JudgeConfig()
        self.model = self.config.model
        self._client = genai.Client(
            api_key=require_env("GOOGLE_API_KEY", "GEMINI_API_KEY"),
            http_options=types.HttpOptions(
                retry_options=types.HttpRetryOptions(attempts=self.config.max_retries)
            ),
        )

    def grade(self, benchmark: Benchmark, item: Item, response: str) -> Judgement:
        if not response.strip():
            # 빈 응답은 채점하지 않는다. 호출 측이 0점 + 실패 피드백으로 처리한다.
            return Judgement(error="empty_response")

        started = time.perf_counter()
        try:
            raw = self._client.models.generate_content(
                model=self.model,
                contents=benchmark.judge_prompt(item, response),
                config=types.GenerateContentConfig(
                    temperature=self.config.temperature,
                    response_mime_type="application/json",
                    response_json_schema=benchmark.judge_schema(item),
                    thinking_config=types.ThinkingConfig(
                        thinking_level=self.config.thinking_level
                    ),
                ),
            )
        except Exception as exc:
            return Judgement(error=repr(exc), latency_ms=_ms(started))

        text = raw.text or ""
        try:
            payload = json.loads(text)
        except (json.JSONDecodeError, TypeError) as exc:
            return Judgement(error=f"판정 JSON 파싱 실패: {exc}", raw={"text": text}, latency_ms=_ms(started))
        if not isinstance(payload, dict):
            return Judgement(error="판정이 JSON 객체가 아닙니다.", raw={"text": text}, latency_ms=_ms(started))

        try:
            judgement = benchmark.parse_judgement(item, payload)
        except Exception as exc:
            return Judgement(error=f"판정 파싱 실패: {exc!r}", raw=payload, latency_ms=_ms(started))

        judgement.raw = payload
        judgement.latency_ms = _ms(started)
        if usage := raw.usage_metadata:
            judgement.usage = {
                "input_tokens": usage.prompt_token_count or 0,
                "output_tokens": usage.candidates_token_count or 0,
                "thinking_tokens": usage.thoughts_token_count or 0,
            }
        return judgement


def _ms(started: float) -> float:
    return (time.perf_counter() - started) * 1000
