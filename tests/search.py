"""web_search 를 모델이 부르는 것과 **같은 경로**(MCP)로 호출한다.

출력은 가공하지 않는다. 화면에 나오는 것이 곧 모델의 도구 결과로 들어가는 문자열이다.

    python tests/search.py "gemma 4 12b context length"
    python tests/search.py "..." --results 5           # serper 결과 수
    python tests/search.py "..." --region kr --lang ko # 한국어 벤치마크 설정
    python tests/search.py "..." --question "<문항>"    # 8-gram 유출 필터까지 적용
    python tests/search.py "..." --save out.json
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from searchgym.agent import _strip_leaks  # noqa: E402
from searchgym.paths import load_env, resolve  # noqa: E402
from searchgym.report import enable_utf8  # noqa: E402


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="web_search 직접 호출")
    parser.add_argument("query", help="검색어")
    parser.add_argument("--results", type=int, default=None, help="serper 결과 수 (기본 10)")
    parser.add_argument("--region", default=None, help="gl. 기본 .env 의 SEARCH_REGION")
    parser.add_argument("--lang", default=None, help="hl. 기본 .env 의 SEARCH_LANGUAGE")
    parser.add_argument(
        "--question",
        default=None,
        help="이 문항 기준으로 8-gram 유출 필터를 적용한다(에이전트가 하는 것과 동일)",
    )
    parser.add_argument("--save", default=None, help="결과를 파일로 저장")
    return parser.parse_args(argv)


async def main_async(argv: list[str] | None = None) -> int:
    enable_utf8()
    load_env()
    args = parse_args(argv)

    if args.results is not None:
        os.environ["SEARCH_RESULTS"] = str(args.results)
    if args.region:
        os.environ["SEARCH_REGION"] = args.region
    if args.lang:
        os.environ["SEARCH_LANGUAGE"] = args.lang

    from searchgym.tools import WebTools

    async with WebTools() as tools:
        parsed, outcome = await tools.search(args.query)

    if outcome.is_error:
        print(outcome.text, file=sys.stderr)
        return 1

    text = outcome.text
    if args.question:
        parsed, leaked = _strip_leaks(parsed, args.question)
        if leaked:
            print(f"[8-gram 유출 필터: {leaked}건 제거]", file=sys.stderr)
        text = json.dumps(parsed, ensure_ascii=False)

    print(text)

    print(
        f"\n---\n{len(text):,}자 · organic {len(parsed.get('organic') or [])}건 · "
        f"{outcome.duration_ms:.0f}ms",
        file=sys.stderr,
    )
    if args.save:
        resolve(args.save).write_text(text, encoding="utf-8")
        print(f"저장: {resolve(args.save)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main_async()))
