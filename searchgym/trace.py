"""문항 하나의 실행 기록.

한 문항 = JSONL 파일 하나. 각 줄이 이벤트 하나이고 pandas로 바로 읽힌다.
어떤 모델을 쓰든 이벤트 이름과 필드가 같아야 비교가 되므로 여기서 고정한다.

    run.start / run.end / run.error / run.truncated
    llm.request / llm.response
    tool.call / tool.result
    search.fetched              검색당 자동 페치 결과 (search-o1 / depthsearch)
    explorer.start / explorer.end / explorer.error
    expand.node / expand.return / expand.failed     확장 노드 하나의 생애
    budget.search_exhausted     검색 예산 소진
    budget.nodes_exhausted      확장 노드 예산 소진
    budget.context_exhausted    대화 컨텍스트 상한 도달
    contamination.filtered      벤치마크 유출 검색 결과 제거
    contamination.blocked_page  벤치마크 유출 페이지 차단
"""

from __future__ import annotations

import json
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

__all__ = ["Trace", "ToolCall"]


@dataclass(slots=True)
class ToolCall:
    """모델이 실행한 도구 호출 한 건. 벤더와 무관하게 같은 형태다.

    `result`에는 모델이 **실제로 본 것**이 들어간다.
        web_search  파싱된 검색 결과(title/link/snippet)
        web_fetch   explorer 요약 (jina 원문이 아니다 — 그건 explorer.json)
    """

    name: str
    arguments: dict[str, Any] = field(default_factory=dict)
    result: Any = None
    result_chars: int = 0
    is_error: bool = False
    # 예산 초과로 실행하지 않고 안내만 돌려준 호출.
    refused: bool = False
    # 문항 원문이 실려 있어 걷어낸 검색 결과 수(벤치마크 유출).
    leaked: int = 0
    duration_ms: float = 0.0
    # 이 호출이 태운 explorer 들의 호출 트리. 시각화(tree.svg)의 입력이다.
    # **목록인 이유**: search-o1 은 검색 한 번에 상위 k개 페이지를 각각 따로
    # 읽히므로 호출 하나가 explorer 를 k개 태운다. DepthSearch도 선택한 진입
    # 페이지마다 트리 하나를 검색 호출에 연결한다.
    explorations: list[dict[str, Any]] = field(default_factory=list)

    @property
    def query(self) -> str:
        return str(self.arguments.get("query") or "")

    @property
    def url(self) -> str:
        return str(self.arguments.get("url") or "")

    def as_dict(self, full: bool = True) -> dict[str, Any]:
        slim = {
            "name": self.name,
            "arguments": self.arguments,
            "result_chars": self.result_chars,
            "is_error": self.is_error,
            "refused": self.refused,
            "leaked": self.leaked,
            "duration_ms": round(self.duration_ms, 1),
            "explorations": self.explorations,
        }
        return {**slim, "result": self.result} if full else slim


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

