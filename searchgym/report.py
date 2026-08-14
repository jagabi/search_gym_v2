"""콘솔 표와 요약 파일.

실행 디렉터리를 열었을 때 무엇을 돌렸고 어떻게 됐는지 파일 두 개로 알 수 있어야
한다. `summary.json`이 그 답이고, `records.jsonl`이 문항별 원본이다.
"""

from __future__ import annotations

import json
import statistics as st
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Any, Iterable

if TYPE_CHECKING:  # 서빙 환경에는 runner의 의존성(openai 등)이 없다. 타입에만 쓴다.
    from .runner import Record

__all__ = ["behaviour", "enable_utf8", "table", "write_json"]


def enable_utf8() -> None:
    """Windows 콘솔 기본 코덱에서 검색 결과의 비-ASCII가 깨지는 것을 막는다."""
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8", errors="replace")
            except (AttributeError, OSError):
                pass


def table(title: str, rows: dict[str, Any]) -> None:
    width = max((len(str(k)) for k in rows), default=0)
    print(f"\n{title}")
    print("-" * (width + 40))
    for key, value in rows.items():
        print(f"  {str(key):<{width}}  {value}")


def write_json(path: Path, payload: Any) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False, default=str), encoding="utf-8"
    )
    return path


def behaviour(records: Iterable["Record"]) -> dict[str, Any]:
    """검색 행동 요약. 정확도만큼 중요한 축이라 항상 같이 낸다."""
    items = list(records)
    if not items:
        return {}
    searches = [r.result.searches for r in items]
    fetches = [r.result.fetches for r in items]
    return {
        "searches_mean": round(st.mean(searches), 2),
        "searches_median": round(st.median(searches), 1),
        "searches_max": max(searches),
        "searches_total": sum(searches),
        "fetches_mean": round(st.mean(fetches), 2),
        "fetches_total": sum(fetches),
        "turns_mean": round(st.mean([r.result.turns for r in items]), 2),
        "latency_s_median": round(st.median([r.result.latency_ms for r in items]) / 1000, 1),
        "input_tokens": sum(r.result.usage.input_tokens for r in items),
        "output_tokens": sum(r.result.usage.output_tokens for r in items),
        "reasoning_tokens": sum(r.result.usage.reasoning_tokens for r in items),
        "empty_answers": sum(1 for r in items if not r.result.answer.strip()),
        "run_errors": sum(1 for r in items if r.result.error),
    }


def summarize(records: Iterable["Record"]) -> dict[str, Any]:
    """집계 + 행동 + 검색 예산 구간별 정확도."""
    from .scoring import aggregate  # 지연 import (서빙 환경에서 report만 쓸 수 있게)

    items = list(records)
    summary = {**aggregate(r.judgement for r in items), **behaviour(items)}
    summary["by_search_count"] = _by_search_count(items)
    return summary


def _by_search_count(records: list["Record"]) -> dict[str, Any]:
    """검색을 많이 할수록 정확한가. 실측상 반대인 경우가 많아 항상 본다."""
    buckets = [(0, 0), (1, 4), (5, 9), (10, 14), (15, 19), (20, 10_000)]
    out: dict[str, Any] = {}
    for low, high in buckets:
        group = [r for r in records if low <= r.result.searches <= high]
        if not group:
            continue
        label = f"{low}" if low == high else (f"{low}+" if high > 9999 else f"{low}-{high}")
        out[label] = {
            "n": len(group),
            "score": round(st.mean([r.score for r in group]), 4),
        }
    return out
