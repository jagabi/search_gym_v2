"""Search-Time Contamination 점검 — 에이전트가 벤치마크 자체를 찾아갔는가.

    python scripts/contamination.py                    # runs/ 전체
    python scripts/contamination.py runs/eval/2026...  # 한 실행만

라이브 웹을 검색하는 에이전트는 벤치마크의 메타데이터·문항·정답을 그대로 긁어올 수
있다(arXiv 2606.05241). 그러면 점수가 실력이 아니라 유출을 측정한다. 도구 서버가
BLOCKED_TERMS로 막고 있지만, **막혔다는 사실 자체가 보고할 수치**다 — 시도가 몇 번
있었는지, 어떤 질의였는지가 논문 부록에 들어간다.

우리 트레이스에는 모든 질의와 연 URL이 남으므로 사후에 전부 셀 수 있다.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from searchgym.paths import resolve  # noqa: E402
from searchgym.report import enable_utf8, table  # noqa: E402

# 벤치마크 유출 신호. "dataset" 같은 흔한 단어는 넣지 않는다 — 데이터를 찾는 문항이
# 많아 오탐이 압도적이 된다(실측: 오탐 88건 대 진짜 1건).
BENCHMARK = re.compile(
    r"deepsearchqa|deep\s*search\s*qa|browsecomp|dsqa|"
    r"humanity'?s\s*last\s*exam|\bhle\b|\bgaia\b|hotpotqa",
    re.I,
)
HOSTS = re.compile(r"huggingface\.co/datasets|paperswithcode|openreview|kaggle\.com/datasets", re.I)


def scan(root: Path) -> dict:
    """트레이스에서 **모든** URL 출처를 훑는다.

    게이트가 부른 도구만 보면 안 된다. search-o1/depthsearch 는 상위 k개를 자동으로
    열고(`search.fetched`), depthsearch 는 explorer 가 링크를 따라 더 연다
    (`expand.node`). 깊이가 깊어질수록 미러에 닿을 확률이 오르므로 여기가 핵심이다.
    """
    queries = urls = 0
    hits: list[tuple[str, str, str]] = []
    filtered_results = blocked_pages = 0
    by_depth: Counter[int] = Counter()

    for trace in root.rglob("*.jsonl"):
        if trace.name == "records.jsonl":
            continue
        run = trace.parent.name
        for line in trace.read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            kind = event.get("event")

            # 8-gram 필터가 실제로 걷어낸 횟수. 막혔다는 사실 자체가 보고할 수치다.
            if kind == "contamination.filtered":
                filtered_results += int(event.get("removed") or 0)
                continue
            if kind == "contamination.blocked_page":
                blocked_pages += int(event.get("count") or 1)
                continue

            # 게이트가 직접 부른 도구
            if kind == "tool.result":
                args = event.get("arguments") or {}
                if query := args.get("query"):
                    queries += 1
                    if BENCHMARK.search(query):
                        hits.append((run, "query", query[:120]))
                if url := args.get("url"):
                    urls += 1
                    by_depth[0] += 1
                    if BENCHMARK.search(url) or HOSTS.search(url):
                        hits.append((run, "fetch", url[:120]))

            # 검색당 자동 페치 (depth 1)
            elif kind == "search.fetched":
                for url in event.get("urls") or []:
                    urls += 1
                    by_depth[1] += 1
                    if BENCHMARK.search(url) or HOSTS.search(url):
                        hits.append((run, "auto", url[:120]))

            # explorer 의 확장 (depth >= 2)
            elif kind == "expand.node":
                url = str(event.get("url") or "")
                depth = int(event.get("depth") or 2)
                urls += 1
                by_depth[depth] += 1
                if url and (BENCHMARK.search(url) or HOSTS.search(url)):
                    hits.append((run, f"d{depth}", url[:120]))

    return {
        "queries": queries,
        "urls": urls,
        "hits": hits,
        "filtered_results": filtered_results,
        "blocked_pages": blocked_pages,
        "by_depth": dict(sorted(by_depth.items())),
    }


def main(argv: list[str] | None = None) -> int:
    enable_utf8()
    parser = argparse.ArgumentParser(description="벤치마크 유출 점검")
    parser.add_argument("root", nargs="?", default="runs", help="검사할 디렉터리")
    args = parser.parse_args(argv)

    root = resolve(args.root)
    if not root.exists():
        print(f"없는 경로: {root}", file=sys.stderr)
        return 1

    report = scan(root)
    hits = report["hits"]
    total = report["queries"] + report["urls"]
    table(
        "Search-Time Contamination",
        {
            "검사 대상": root,
            "검색 질의": f"{report['queries']:,}건",
            "연 URL": f"{report['urls']:,}건  (깊이별 {report['by_depth']})",
            "8-gram 필터로 지운 검색 결과": f"{report['filtered_results']:,}건",
            "8-gram 필터로 막은 페이지": f"{report['blocked_pages']:,}건",
            "의심 접근": f"{len(hits)}건 ({len(hits) / total:.2%})" if total else "0건",
            "판정": "깨끗함" if not hits else "유출 시도 있음 — 아래 확인",
        },
    )

    if hits:
        print("\n의심 접근:")
        for run, kind, text in hits[:40]:
            print(f"  [{kind:<5}] {run[:40]:<40} {text}")
        if len(hits) > 40:
            print(f"  ... 외 {len(hits) - 40}건")
        print(
            "\n도구 서버의 BLOCKED_TERMS가 막고 있다면 시도는 실패했을 것이다."
            "\n트레이스의 is_error와 결과 길이로 실제 유출 여부를 확인할 것."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
