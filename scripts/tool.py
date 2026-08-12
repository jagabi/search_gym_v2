"""도구를 모델 없이 직접 호출한다. LLM이 부르는 것과 **같은 경로**(MCP)로 나간다.

    python scripts/tool.py                                   # 도구 목록과 스키마
    python scripts/tool.py fetch https://example.com
    python scripts/tool.py search "gemma 4 12b context length"
    python scripts/tool.py fetch <url> --full                 # 전문 출력
    python scripts/tool.py fetch <url> --save page.md         # 파일로 저장
    python scripts/tool.py fetch <url> --refine "내 검색어"    # Search-o1 정제까지

`--refine`은 vLLM이 떠 있어야 한다(configs/eval.yaml의 agent.base_url을 쓴다).
정제 없이 쓰면 Jina가 돌려준 원문 그대로를 본다.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from searchgym.paths import load_env, resolve  # noqa: E402
from searchgym.report import enable_utf8, table  # noqa: E402
from searchgym.tools import WebTools  # noqa: E402

PREVIEW = 4000  # 콘솔 미리보기만. 모델이 받는 양과 무관하다(--full로 전부)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="MCP 도구 직접 호출")
    parser.add_argument("tool", nargs="?", choices=["search", "fetch"], help="생략하면 도구 목록")
    parser.add_argument("value", nargs="?", help="search면 질의, fetch면 URL")
    parser.add_argument("--full", action="store_true", help="자르지 않고 전부 출력")
    parser.add_argument("--save", default=None, help="결과를 파일로 저장")
    parser.add_argument(
        "--refine",
        nargs="?",
        const="",
        default=None,
        metavar="QUERY",
        help="Search-o1 정제를 함께 돌린다. 값을 주면 그것을 current search query로 쓴다",
    )
    parser.add_argument("--config", default="configs/eval.yaml", help="--refine이 쓸 설정")
    return parser.parse_args(argv)


async def run(args: argparse.Namespace) -> int:
    async with WebTools() as tools:
        if not args.tool:
            for spec in tools.specs:
                print(f"\n{spec.name}")
                print(f"  {spec.description.splitlines()[0] if spec.description else ''}")
                print(f"  schema: {json.dumps(spec.input_schema, ensure_ascii=False)}")
            return 0

        if not args.value:
            print("search면 질의를, fetch면 URL을 주세요.", file=sys.stderr)
            return 1

        name = "web_search" if args.tool == "search" else "web_fetch"
        arguments = {"query": args.value} if args.tool == "search" else {"url": args.value}

        outcome = await tools.call(name, arguments)
        table(
            f"{name}  {args.value[:60]}",
            {
                "error": outcome.is_error,
                "소요": f"{outcome.duration_ms:.0f}ms",
                "길이": f"{len(outcome.text):,}자",
            },
        )

        body = outcome.text
        if args.tool == "search" and not outcome.is_error:
            body = _render_search(body)

        print()
        print(body if args.full else body[:PREVIEW])
        if not args.full and len(body) > PREVIEW:
            print(f"\n... ({len(body):,}자 중 {PREVIEW}자만. 전부 보려면 --full)")

        if args.save:
            path = resolve(args.save)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(outcome.text, encoding="utf-8")
            print(f"\n저장됨: {path}")

        if args.refine is not None and args.tool == "fetch" and not outcome.is_error:
            await _refine(args, outcome.text)
    return 0


def _render_search(raw: str) -> str:
    """검색 결과를 사람이 읽게 편다. 모델은 이 JSON을 그대로 받는다."""
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return raw
    lines = []
    if box := data.get("answer_box"):
        lines.append(f"[answer box] {json.dumps(box, ensure_ascii=False)}\n")
    for i, item in enumerate(data.get("organic", []), 1):
        lines.append(f"{i:>2}. {item.get('title', '')}")
        lines.append(f"    {item.get('link', '')}")
        if snippet := item.get("snippet"):
            lines.append(f"    {snippet}")
    if note := data.get("filtered_results"):
        lines.append(f"\n[filtered] {note}")
    return "\n".join(lines)


async def _refine(args: argparse.Namespace, page: str) -> None:
    """에이전트가 쓰는 것과 같은 정제 경로를 태운다."""
    from openai import AsyncOpenAI

    from searchgym.agent import REFINE_PROMPT
    from searchgym.config import load_eval
    from searchgym.serving import profile_for

    config = load_eval(args.config)
    profile = profile_for(config.model)
    client = AsyncOpenAI(
        base_url=config.agent.base_url, api_key=config.agent.api_key, timeout=config.agent.timeout_s
    )
    prompt = REFINE_PROMPT.format(
        prev_reasoning="(none — direct tool test)",
        search_query=args.refine or args.value,
        document=page,
    )
    response = await client.chat.completions.create(
        model=profile.repo,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=config.agent.refine_max_tokens,
    )
    refined = (response.choices[0].message.content or "").strip()
    table(
        "Search-o1 정제",
        {
            "model": profile.repo,
            "search_query": args.refine or args.value,
            "원문": f"{len(page):,}자",
            "정제 후": f"{len(refined):,}자",
            "압축률": f"{len(refined) / max(len(page), 1):.1%}",
        },
    )
    print(f"\n{refined}")


def main(argv: list[str] | None = None) -> int:
    enable_utf8()
    load_env()
    return asyncio.run(run(parse_args(argv)))


if __name__ == "__main__":
    raise SystemExit(main())
