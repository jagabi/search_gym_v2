"""검색 하나에 대해 explorer 경로를 통째로 돌려 본다 — 모델 없이 게이트만 빼고.

    depthsearch  search → (메인 모델이 고른) 페이지 1개 → explorer(재귀)
    search-o1    search → 상위 k개 자동 페치 → explorer

마지막에 찍히는 것이 **게이트(메인 추론 모델)가 도구 결과로 받는 바로 그 문자열**이다.
가공하지 않는다.

    python tests/explorer.py "who signed the treaty of waitangi"
    python tests/explorer.py "<검색어>" --rank 3                  # 3위 페이지를 연다
    python tests/explorer.py "<검색어>" --url https://...         # 검색 건너뛰고 그 URL 만
    python tests/explorer.py "<검색어>" --question "<원 문항>"     # 목표를 정확히 준다
    python tests/explorer.py "<검색어>" --method search-o1        # 자동 top-k, 재귀 없이
    python tests/explorer.py "<검색어>" --depth 3 --nodes 12 --children 2
    python tests/explorer.py "<검색어>" --links                   # 링크 목록 켜고
    python tests/explorer.py "<검색어>" --trace out.jsonl

vLLM 이 떠 있어야 한다(explorer 가 모델 호출이다).
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from searchgym.agent import _strip_leaks, strip_page_leaks  # noqa: E402
from searchgym.config import load_test  # noqa: E402
from searchgym.explorer import Budget, Explorer  # noqa: E402
from searchgym.llm import LLM, Usage  # noqa: E402
from searchgym.paths import load_env, resolve  # noqa: E402
from searchgym.report import enable_utf8  # noqa: E402
from searchgym.serving import profile_for  # noqa: E402
from searchgym.trace import NullTrace, Trace  # noqa: E402


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="explorer 경로 직접 실행")
    parser.add_argument("query", help="게이트가 던졌다고 가정할 검색어")
    parser.add_argument("--conf", default="conf.yaml")
    parser.add_argument("--method", default=None, help="search-o1 | depthsearch")
    parser.add_argument("--model", default=None)
    parser.add_argument("--question", default=None, help="원 문항. 없으면 검색어를 쓴다")
    parser.add_argument("--reasoning", default="", help="누적 추론 블록(선택)")
    parser.add_argument("--top-k", type=int, default=None, help="자동 페치 수 (search-o1)")
    parser.add_argument(
        "--rank", type=int, default=1,
        help="depthsearch: 검색 결과 몇 위를 열 것인가 (메인 모델의 선택을 대신한다)",
    )
    parser.add_argument("--url", default=None, help="검색을 건너뛰고 이 URL 만 연다")
    parser.add_argument("--depth", type=int, default=None, help="explorer.max_depth")
    parser.add_argument("--nodes", type=int, default=None, help="확장 노드 예산")
    parser.add_argument("--children", type=int, default=None, help="노드당 자식 수")
    parser.add_argument("--links", action="store_true", help="Jina 링크 목록을 켠다")
    parser.add_argument("--prompt", default=None, help="explorer 프롬프트를 파일에서 읽는다")
    parser.add_argument("--trace", default=None, help="이벤트를 JSONL 로 저장")
    parser.add_argument("--tree", action="store_true", help="explorer 호출 트리를 JSON 으로")
    return parser.parse_args(argv)


async def main_async(argv: list[str] | None = None) -> int:
    enable_utf8()
    load_env()
    args = parse_args(argv)

    if args.links:
        os.environ["JINA_WITH_LINKS"] = "1"

    config = load_test(args.conf, method=args.method, model=args.model)
    if not config.uses_explorer:
        print(f"'{config.method}' 는 explorer 를 쓰지 않습니다. --method 로 바꾸세요.", file=sys.stderr)
        return 1

    if args.top_k is not None:
        config.agent.search_top_k = args.top_k
    if args.depth is not None:
        config.explorer.max_depth = args.depth
    if args.nodes is not None:
        config.explorer.max_expansion_nodes = args.nodes
    if args.children is not None:
        config.explorer.max_subtree_children = args.children
    if args.prompt:
        config.explorer_prompt = resolve(args.prompt).read_text(encoding="utf-8").strip()

    question = args.question or args.query
    profile = profile_for(config.model)
    llm = LLM(
        profile,
        base_url=config.agent.base_url,
        api_key=config.agent.api_key,
        timeout_s=config.agent.timeout_s,
        model_name=config.agent.model_name,
    )
    trace = Trace(resolve(args.trace), run_id="explorer-test") if args.trace else NullTrace()
    budget = Budget(config.explorer.max_expansion_nodes)
    usage = Usage()

    print(f"method    {config.method}")
    print(f"model     {llm.model_name}  @ {config.agent.base_url}")
    print(f"페치      {'자동 top-' + str(config.agent.search_top_k) if config.agent.search_top_k else '메인 모델 선택 (여기서는 --rank %d)' % args.rank}")
    print(f"explorer  depth<={config.explorer.max_depth}  nodes={budget.total}  "
          f"children<={config.explorer.max_subtree_children}  turns<={config.explorer.max_turns}")
    print(f"links     {'on' if args.links else 'off'}")

    from searchgym.tools import WebTools

    try:
        async with WebTools(search_results=config.agent.search_results) as tools:
            if args.url:
                entries = [{"link": args.url, "title": ""}]
                print(f"\n=== (검색 건너뜀) {args.url}")
            else:
                print(f"\n=== search: {args.query!r} " + "=" * 30)
                parsed, outcome = await tools.search(args.query)
                if outcome.is_error:
                    print(outcome.text, file=sys.stderr)
                    return 1
                parsed, leaked = _strip_leaks(parsed, question)
                organic = parsed.get("organic") or []
                for i, entry in enumerate(organic[:10], 1):
                    mark = ">" if (not config.agent.search_top_k and i == args.rank) else " "
                    print(f"{mark}{i:>2}. {entry.get('title', '')}\n     {entry.get('link', '')}")
                if leaked:
                    print(f"(8-gram 유출 필터: {leaked}건 제거)")

                if config.agent.search_top_k:
                    # search-o1 — 상위 k개를 자동으로 연다
                    entries = organic[: config.agent.search_top_k]
                else:
                    # depthsearch — 메인 모델이 하나를 고른다. 여기서는 --rank 로 대신한다
                    entries = organic[args.rank - 1 : args.rank]

            print(f"\n=== fetch {len(entries)} page(s) " + "=" * 28)
            documents = await tools.fetch_many(entries)
            for document in documents:
                if not document.is_error:
                    document.content, blocked = strip_page_leaks(document.content, question)
                    if blocked:
                        document.is_error = True
                mark = "ERR " if document.is_error else "    "
                print(f"{mark}{len(document.content):>8,}자  {document.url}")

            async def guarded(url: str):
                document = await tools.fetch(url)
                if not document.is_error:
                    document.content, blocked = strip_page_leaks(document.content, question)
                    document.is_error = document.is_error or blocked
                return document

            explorer = Explorer(llm, config.explorer, config.explorer_prompt, guarded)
            ok = [d for d in documents if not d.is_error]

            print("\n=== explorer " + "=" * 40)
            result = await explorer.explore(
                question=question,
                reasoning=args.reasoning,
                query=args.query,
                documents=ok or documents,
                budget=budget,
                trace=trace,
                usage=usage,
                depth=1,
            )
    finally:
        await llm.aclose()

    print(f"status={result.status}  nodes={result.nodes}  depth_reached={result.depth_reached}  "
          f"calls={result.calls}  dead_dives={result.dead_dives}  turns={result.turns}")
    print(f"budget {json.dumps(budget.as_dict())}   usage {json.dumps(usage.as_dict())}")
    if result.error:
        print(f"error: {result.error}", file=sys.stderr)

    if args.tree:
        print("\n=== explorer tree " + "=" * 35)
        print(json.dumps(result.log, ensure_ascii=False, indent=2))

    print("\n=== 게이트가 받는 문자열 " + "=" * 32)
    print(result.render_for_gate())
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main_async()))
