"""web_fetch 를 모델이 부르는 것과 **같은 경로**(MCP)로 호출한다.

출력은 가공하지 않는다. 화면에 나오는 것이 곧 explorer(또는 ragent 의 메인 모델)에게
들어가는 문자열이다.

Jina Reader 옵션을 바꿔 가며 비교하는 것이 이 스크립트의 주 용도다.

    python tests/fetch.py https://en.wikipedia.org/wiki/Kyoto
    python tests/fetch.py <url> --links                # 본문 끝에 링크 목록을 붙인다
    python tests/fetch.py <url> --links --format text  # 마크다운 대신 평문
    python tests/fetch.py <url> --engine browser       # JS 렌더링
    python tests/fetch.py <url> --max-chars 40000      # 서버측 비상 밸브
    python tests/fetch.py <url> --head 3000            # 화면에는 앞부분만
    python tests/fetch.py <url> --save page.md

**--links 가 depthsearch 의 전제조건이다.** 링크 목록이 없으면 explorer 는 따라
들어갈 URL 자체를 볼 수 없다. 대신 링크가 많은 페이지에서는 본문보다 링크가 길어져
정제기의 문서 토큰 예산을 먹으므로, 여기서 실제 크기를 재 보고 정하면 된다.

    python tests/fetch.py <url>            # 링크 없이 몇 자인가
    python tests/fetch.py <url> --links    # 링크 켜면 몇 자가 되는가
"""

from __future__ import annotations

import argparse
import asyncio
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from searchgym.paths import load_env, resolve  # noqa: E402
from searchgym.report import enable_utf8  # noqa: E402


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="web_fetch 직접 호출")
    parser.add_argument("url", help="열 페이지의 절대 URL")
    parser.add_argument(
        "--links", action="store_true", help="X-With-Links-Summary — 링크 목록을 붙인다"
    )
    parser.add_argument("--images", action="store_true", help="X-With-Images-Summary")
    parser.add_argument(
        "--format", default=None, choices=["markdown", "text", "html"],
        help="X-Return-Format (기본 markdown)",
    )
    parser.add_argument(
        "--engine", default=None, choices=["browser", "direct"],
        help="X-Engine. browser 는 JS 를 렌더링한다(느리다)",
    )
    parser.add_argument(
        "--max-chars", type=int, default=None,
        help="서버측 비상 밸브(FETCH_MAX_CHARS). 0 = 무제한",
    )
    parser.add_argument("--head", type=int, default=0, help="화면에는 앞 N자만 (0 = 전부)")
    parser.add_argument("--save", default=None, help="전문을 파일로 저장")
    parser.add_argument(
        "--tokens", action="store_true",
        help="vLLM /tokenize 로 실제 토큰 수를 잰다(서버가 떠 있어야 한다)",
    )
    return parser.parse_args(argv)


async def main_async(argv: list[str] | None = None) -> int:
    enable_utf8()
    load_env()
    args = parse_args(argv)

    # MCP 서브프로세스로 그대로 전달된다(WebTools 가 이 키들을 넘긴다).
    if args.links:
        os.environ["JINA_WITH_LINKS"] = "1"
    if args.images:
        os.environ["JINA_WITH_IMAGES"] = "1"
    if args.format:
        os.environ["JINA_RETURN_FORMAT"] = args.format
    if args.engine:
        os.environ["JINA_ENGINE"] = args.engine
    if args.max_chars is not None:
        os.environ["FETCH_MAX_CHARS"] = str(args.max_chars)

    from searchgym.tools import WebTools

    async with WebTools() as tools:
        document = await tools.fetch(args.url)

    if document.is_error:
        print(document.content, file=sys.stderr)
        return 1

    text = document.content
    print(text[: args.head] if args.head else text)
    if args.head and len(text) > args.head:
        print(f"\n... (앞 {args.head:,}자만 표시. 전체 {len(text):,}자)", file=sys.stderr)

    options = [
        f"format={os.getenv('JINA_RETURN_FORMAT', 'markdown')}",
        f"links={'on' if args.links else 'off'}",
        f"images={'on' if args.images else 'off'}",
        f"engine={os.getenv('JINA_ENGINE') or 'default'}",
        f"max_chars={os.getenv('FETCH_MAX_CHARS', '0')}",
    ]
    print(f"\n---\n{len(text):,}자  ·  " + "  ".join(options), file=sys.stderr)

    if args.tokens:
        print(f"토큰: {await _count(text):,}", file=sys.stderr)
    if args.save:
        resolve(args.save).write_text(text, encoding="utf-8")
        print(f"저장: {resolve(args.save)}", file=sys.stderr)
    return 0


async def _count(text: str) -> int:
    from searchgym.config import load_test
    from searchgym.llm import LLM
    from searchgym.serving import profile_for

    config = load_test()
    llm = LLM(profile_for(config.model), base_url=config.agent.base_url)
    try:
        return await llm.count_tokens(text)
    finally:
        await llm.aclose()


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main_async()))
