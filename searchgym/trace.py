"""문항 하나의 실행 기록.

한 문항 = JSONL 파일 하나. 각 줄이 이벤트 하나이고 pandas로 바로 읽힌다.
어떤 모델을 쓰든 이벤트 이름과 필드가 같아야 비교가 되므로 여기서 고정한다.

    run.start / run.end / run.error
    llm.request / llm.response
    tool.call / tool.result
    budget.exhausted            검색 예산이 소진되어 도구를 끊은 시점
"""

from __future__ import annotations

import json
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

__all__ = ["Trace", "ToolCall", "Usage"]


@dataclass(slots=True)
class Usage:
    input_tokens: int = 0
    output_tokens: int = 0
    reasoning_tokens: int = 0

    def add(self, prompt: int | None, completion: int | None, reasoning: int | None = 0) -> None:
        self.input_tokens += prompt or 0
        self.output_tokens += completion or 0
        self.reasoning_tokens += reasoning or 0

    def as_dict(self) -> dict[str, int]:
        return {
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "reasoning_tokens": self.reasoning_tokens,
        }


@dataclass(slots=True)
class ToolCall:
    """모델이 실행한 도구 호출 한 건. 벤더와 무관하게 같은 형태다."""

    name: str
    arguments: dict[str, Any] = field(default_factory=dict)
    result_chars: int = 0
    is_error: bool = False
    duration_ms: float = 0.0

    @property
    def query(self) -> str:
        return str(self.arguments.get("query") or "")

    @property
    def url(self) -> str:
        return str(self.arguments.get("url") or "")

    def as_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "arguments": self.arguments,
            "result_chars": self.result_chars,
            "is_error": self.is_error,
            "duration_ms": round(self.duration_ms, 1),
        }


class Trace:
    """append-only JSONL. 스레드 안전하다."""

    def __init__(self, path: Path, run_id: str) -> None:
        self.path = path
        self.run_id = run_id
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self._origin = time.perf_counter()

    def event(self, kind: str, **fields: Any) -> None:
        record = {
            "elapsed_ms": round((time.perf_counter() - self._origin) * 1000, 1),
            "run_id": self.run_id,
            "event": kind,
            **fields,
        }
        line = json.dumps(record, ensure_ascii=False, default=str)
        with self._lock, self.path.open("a", encoding="utf-8") as handle:
            handle.write(line + "\n")


class NullTrace(Trace):
    """트레이스를 남기지 않는 자리 표시자(테스트·드라이런용)."""

    def __init__(self) -> None:  # noqa: D107
        self.run_id = ""
        self._origin = time.perf_counter()

    def event(self, kind: str, **fields: Any) -> None:
        return
