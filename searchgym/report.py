"""콘솔 표와 요약 파일.

실행 디렉터리를 열었을 때 무엇을 돌렸고 어떻게 됐는지 파일 두 개로 알 수 있어야
한다. `summary.json` 이 그 답이고, `records.jsonl` 이 문항별 원본이다.

정확도만 보면 안 된다. 이 실험이 재는 것은 **탐색량과 컨텍스트 소비의 분리**라서,
검색 횟수·확장 노드·도달 깊이·컨텍스트 소진율을 정확도와 나란히 낸다.
"""

from __future__ import annotations

import json
import logging
import statistics as st
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Any, Iterable

if TYPE_CHECKING:  # 서빙 환경에는 runner의 의존성(openai 등)이 없다. 타입에만 쓴다.
    from .runner import Record

__all__ = ["behaviour", "enable_utf8", "quiet_libraries", "summarize", "table", "write_json"]


def enable_utf8() -> None:
    """Windows 콘솔 기본 코덱에서 검색 결과의 비-ASCII가 깨지는 것을 막는다."""
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8", errors="replace")
            except (AttributeError, OSError):
                pass


# 실행 중 터미널에 쏟아지지만 우리가 할 일이 없는 서드파티 경고들.
# 진행 상황을 읽을 수 없게 만들고, 진짜 문제를 묻어 버린다.
_NOISY_LOGGERS = (
    # pypdf: layout 모드로 PDF 를 읽을 때 회전된 텍스트를 만나면 페이지마다 한 줄씩
    # 찍는다("Rotated text discovered"). 우리가 고를 수 있는 선택지가 없고, 실제로
    # 무엇을 놓쳤는지는 트레이스로 남기는 편이 낫다.
    "pypdf",
    # google-genai: 판정 호출마다 "Direct use of automatic function calling (AFC) ..."
    # 를 찍는다. 우리는 판정에 함수 호출을 쓰지 않으므로 해당 사항이 없다.
    "google_genai",
    "google.genai",
)


def quiet_libraries() -> None:
    """서드파티 경고를 끈다. **우리 코드의 경고는 건드리지 않는다.**"""
    for name in _NOISY_LOGGERS:
        logging.getLogger(name).setLevel(logging.ERROR)


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
    """탐색 행동 요약. 정확도만큼 중요한 축이라 항상 같이 낸다."""
    items = list(records)
    if not items:
        return {}
    n = len(items)
    searches = [r.result.searches for r in items]
    nodes = [r.result.expansion_nodes for r in items]
    depths = [r.result.max_depth_reached for r in items]

    return {
        "searches_mean": round(st.mean(searches), 2),
        "searches_median": round(st.median(searches), 1),
        "searches_max": max(searches),
        "searches_total": sum(searches),
        # 검색 상한에 실제로 부딪힌 비율. ②가 ③보다 자주 부딪히는지가 예측이다.
        "search_exhausted_rate": round(
            sum(1 for r in items if _hit_search_cap(r)) / n, 4
        ),
        "fetches_mean": round(st.mean([r.result.fetches for r in items]), 2),
        "fetches_total": sum(r.result.fetches for r in items),
        # 도구 계층의 건강 상태. **낮으면 다른 숫자를 읽을 필요가 없다** — 웹이
        # 들어오지 않은 실행이라 방법 비교가 성립하지 않는다.
        # **도구 계층이 살아 있는가.** 둘 중 하나라도 낮으면 다른 숫자는 읽을 필요가
        # 없다 — 웹이 안 들어온 실행이라 방법 비교가 성립하지 않는다. 검색 쪽을
        # 빼두었다가 Serper 크레딧 소진으로 검색의 47% 가 실패하는 것을 통째로
        # 놓쳤다(페치 성공률만 보고 정상이라 판단했다).
        "search_attempts_total": sum(r.result.search_attempts for r in items),
        "search_success_rate": round(
            1 - sum(r.result.search_failures for r in items)
            / max(1, sum(r.result.search_attempts for r in items)), 4),
        "fetch_attempts_total": sum(r.result.fetch_attempts for r in items),
        "fetch_success_rate": round(
            1 - sum(r.result.fetch_failures for r in items)
            / max(1, sum(r.result.fetch_attempts for r in items)),
            4,
        ),

        # 확장 (depth >= 2)
        "expansion_nodes_mean": round(st.mean(nodes), 2),
        "expansion_nodes_total": sum(nodes),
        "expansion_used_rate": round(sum(1 for v in nodes if v) / n, 4),
        "node_budget_exhausted_rate": round(
            sum(1 for r in items if r.result.budget_exhausted) / n, 4
        ),
        # 중복 억제가 실제로 도는가. 소스에서 걷어낸 링크 수(1번 겹)와 그래도
        # 새어 나와 사후에 막힌 수(2번 겹)를 나란히 본다. 후자가 크면 구조적
        # 차단이 새고 있다는 뜻이다.
        "expansion_links_stripped_total": sum(
            int(r.result.budget.get("links_stripped") or 0) for r in items
        ),
        "expansion_duplicates_total": sum(
            int(r.result.budget.get("duplicates") or 0) for r in items
        ),
        # 페이지에 없는 URL(지어낸 주소)을 열려다 막힌 수. explorer 가 링크를
        # 따라가는 대신 주소를 추측하고 있는지가 여기서 보인다.
        "expansion_off_page_total": sum(
            int(r.result.budget.get("off_page") or 0) for r in items
        ),
        # 페이지의 링크는 아니지만 읽던 사이트 안이라 허용된 이동. URL 구조를
        # 추론해 자매 페이지로 간 횟수 — 깊이가 실제로 쓰이는 방식 하나다.
        # 앞 세션이 이미 거절당한 주소를 다시 집은 횟수. 0 에 가까워야 정상이다.
        "expansion_repeat_refusals_total": sum(
            int(r.result.budget.get("repeats") or 0) for r in items
        ),
        "expansion_same_site_total": sum(
            int(r.result.budget.get("same_site") or 0) for r in items
        ),
        # 고유 방문 URL. 확장 노드 수와 함께 보면 탐색이 넓은지 겹치는지가 나온다.
        "visited_urls_total": sum(
            int(r.result.budget.get("visited") or 0) for r in items
        ),
        # 깊이 분포 — 깊이 축의 그림이 여기서 나온다. depth 2 이상만 센다.
        "nodes_by_depth": _depth_histogram(items),
        "max_depth_mean": round(st.mean(depths), 2),
        "max_depth_max": max(depths),
        "explorer_calls_mean": round(st.mean([r.result.explorer_calls for r in items]), 2),
        # explorer 가 연 페이지 중 status == not_found 로 끝난 것.
        "dead_dives_total": sum(r.result.dead_dives for r in items),
        "dead_dive_rate": round(sum(r.result.dead_dives for r in items) / max(1, sum(nodes)), 4),

        # 컨텍스트 — 이 실험의 직접 증거다.
        "context_exhausted_rate": round(
            sum(1 for r in items if r.result.context_exhausted) / n, 4
        ),
        "context_tokens_median": int(st.median([r.result.context_tokens for r in items])),

        "turns_mean": round(st.mean([r.result.turns for r in items]), 2),
        "latency_s_median": round(st.median([r.result.latency_ms for r in items]) / 1000, 1),
        "input_tokens": sum(r.result.usage.input_tokens for r in items),
        "output_tokens": sum(r.result.usage.output_tokens for r in items),
        "reasoning_tokens": sum(r.result.usage.reasoning_tokens for r in items),
        "llm_calls": sum(r.result.usage.calls for r in items),
        "empty_answers": sum(1 for r in items if not r.result.answer.strip()),
        "run_errors": sum(1 for r in items if r.result.error),
        "invalid_tool_calls": sum(r.result.invalid_tool_calls for r in items),
        "reused_page_notes": sum(int(r.result.budget.get("reused", 0)) for r in items),
        "reader_stats": {
            key: sum(r.result.reader_stats.get(key, 0) for r in items)
            for key in sorted({k for r in items for k in r.result.reader_stats})
        },
    }


def summarize(records: Iterable["Record"]) -> dict[str, Any]:
    """집계 + 행동 + 구간별 정확도."""
    from .scoring import aggregate  # 지연 import (서빙 환경에서 report만 쓸 수 있게)

    items = list(records)
    summary = {**aggregate(r.judgement for r in items), **behaviour(items)}
    summary["by_search_count"] = _buckets(
        items, lambda r: r.result.searches, [(0, 0), (1, 2), (3, 5), (6, 9), (10, 10_000)]
    )
    summary["by_expansion_count"] = _buckets(
        items, lambda r: r.result.expansion_nodes, [(0, 0), (1, 3), (4, 7), (8, 11), (12, 10_000)]
    )
    summary["by_depth"] = _buckets(
        items, lambda r: r.result.max_depth_reached, [(1, 1), (2, 2), (3, 10)]
    )
    summary["by_category"] = _by_category(items)
    return summary


def _hit_search_cap(record: "Record") -> bool:
    return any(c.refused for c in record.result.tool_calls if c.name == "web_search")


def _depth_histogram(records: list["Record"]) -> dict[str, int]:
    """깊이별로 실제로 연 노드 수를 합친다.

    `max_depth_mean` 은 문항이 **얼마나 깊이 갔나**만 말하고 그 깊이에서 몇 개를
    열었는지는 말하지 않는다. 평면과 재귀를 가르는 그림에는 이쪽이 필요하다.
    depth 1 은 메인 모델이 고른 페치라 여기 오지 않는다(확장이 아니다).
    """
    out: dict[str, int] = {}
    for r in records:
        for depth, count in (r.result.budget.get("nodes_by_depth") or {}).items():
            out[str(depth)] = out.get(str(depth), 0) + int(count)
    return dict(sorted(out.items()))


def _buckets(
    records: list["Record"], key: Any, edges: list[tuple[int, int]]
) -> dict[str, Any]:
    """구간별 정답률. 많이 탐색할수록 정확한가 — 실측상 반대인 경우가 많아 항상 본다."""
    out: dict[str, Any] = {}
    for low, high in edges:
        group = [r for r in records if low <= key(r) <= high]
        if not group:
            continue
        label = f"{low}" if low == high else (f"{low}+" if high > 9999 else f"{low}-{high}")
        out[label] = {
            "n": len(group),
            "score": round(st.mean([r.score for r in group]), 4),
        }
    return out


def _by_category(records: list["Record"]) -> dict[str, Any]:
    """카테고리별 정답률. 깊이의 이득은 전역이 아니라 도메인에 따라 갈릴 것으로 본다."""
    groups: dict[str, list["Record"]] = {}
    for record in records:
        groups.setdefault(record.category or "(none)", []).append(record)
    return {
        name: {"n": len(group), "score": round(st.mean([r.score for r in group]), 4)}
        for name, group in sorted(groups.items())
    }
