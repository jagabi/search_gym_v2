"""탐색 궤적 그림(`tree.svg`)을 눈으로 확인한다.

    python tests/tree.py --demo                        # 세 방법의 예시 그림
    python tests/tree.py runs/test/<런>/q00003/response.json
    python tests/tree.py runs/test/<런> --all           # 그 실행의 모든 문항 다시 그리기

실행할 때 문항 디렉터리마다 자동으로 저장되지만, 모양을 손보거나 지난 실행을 다시
그릴 때 쓴다. 모델도 도구도 필요 없다.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from searchgym.agent import RunResult, Step  # noqa: E402
from searchgym.llm import Usage  # noqa: E402
from searchgym.paths import resolve  # noqa: E402
from searchgym.report import enable_utf8  # noqa: E402
from searchgym.trace import ToolCall  # noqa: E402
from searchgym.tree import render, build  # noqa: E402


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="탐색 궤적 그림 확인")
    parser.add_argument("target", nargs="?", help="response.json 또는 실행 디렉터리")
    parser.add_argument("--demo", action="store_true", help="세 방법의 예시 그림을 만든다")
    parser.add_argument("--all", action="store_true", help="디렉터리 아래 전부 다시 그린다")
    parser.add_argument("--out", default=None, help="저장 경로(파일 하나일 때)")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    enable_utf8()
    args = parse_args(argv)

    if args.demo:
        out = resolve(args.out or "runs/_demo")
        out.mkdir(parents=True, exist_ok=True)
        for name, result in _demos().items():
            path = out / f"tree_{name}.svg"
            path.write_text(
                render(
                    build(result, _QUESTION),
                    title=f"q · {_QUESTION}",
                    subtitle=(
                        f"{name} · searches {result.searches} · fetches {result.fetches}"
                        f" · expansion {result.expansion_nodes}"
                        f" · depth {result.max_depth_reached}"
                    ),
                ),
                encoding="utf-8",
            )
            print(f"{name:12} -> {path}")
        print("\n브라우저로 열어 보세요.")
        return 0

    if not args.target:
        print("response.json 이나 실행 디렉터리를 주거나 --demo 를 쓰세요.", file=sys.stderr)
        return 1

    target = resolve(args.target)
    files = (
        sorted(target.rglob("response.json")) if target.is_dir() else [target]
    )
    if not files:
        print(f"response.json 을 찾지 못했습니다: {target}", file=sys.stderr)
        return 1
    if not args.all:
        files = files[:1]

    for path in files:
        payload = json.loads(path.read_text(encoding="utf-8"))
        result = _from_payload(payload)
        svg = render(
            build(result, payload.get("question", "")),
            title=f"q · {payload.get('question', '')}",
            subtitle=(
                f"{payload.get('method', '?')} · searches {result.searches}"
                f" · fetches {result.fetches} · expansion {result.expansion_nodes}"
                f" · depth {result.max_depth_reached} · {result.stop_reason}"
            ),
        )
        out = resolve(args.out) if (args.out and not args.all) else path.parent / "tree.svg"
        out.write_text(svg, encoding="utf-8")
        print(f"{path.parent.name} -> {out}")
    return 0


def _from_payload(payload: dict) -> RunResult:
    from searchgym.runner import _result_from

    return _result_from(payload)


# --- 예시 --------------------------------------------------------------------

_QUESTION = "Which two treaties did the same delegate sign, and in what years?"


def _demos() -> dict[str, RunResult]:
    def search(q: str, **kw) -> ToolCall:
        return ToolCall(name="web_search", arguments={"query": q}, **kw)

    def fetch(u: str, **kw) -> ToolCall:
        return ToolCall(name="web_fetch", arguments={"url": u}, **kw)

    def node(url, depth, status, opened=()):
        return {
            "depth": depth, "urls": [url], "turns": 1, "status": status,
            "information": "…", "nodes": len(opened), "error": None,
            "opened": list(opened),
        }

    # ① ragent — 검색과 페치가 나란히. 원문이 그대로 들어간다.
    ragent = RunResult(
        answer="…",
        steps=[
            Step(turn=1, tool_calls=[search("treaty delegate signed two")]),
            Step(turn=2, tool_calls=[fetch("https://en.wikipedia.org/wiki/Delegate_A")]),
            Step(turn=3, tool_calls=[fetch("https://archives.gov/records/treaty-1840")]),
            Step(turn=4, tool_calls=[search("delegate A 1842 treaty signature")]),
            Step(turn=5, tool_calls=[fetch("https://example.org/broken", is_error=True)]),
        ],
        turns=5, stop_reason="answered", usage=Usage(calls=5),
    )

    # ② search-o1 — 검색 하나가 상위 k개를 자동으로 읽는다. 깊이는 없다.
    s1a = search("treaty delegate signed two")
    s1a.exploration = {
        **node("", 1, "partial"),
        "urls": [
            "https://en.wikipedia.org/wiki/Delegate_A",
            "https://archives.gov/records/treaty-1840",
            "https://britannica.com/treaty",
        ],
        "entry": "search",
    }
    s1b = search("delegate A 1842 treaty signature")
    s1b.exploration = {
        **node("", 1, "answered"),
        "urls": ["https://archives.gov/records/treaty-1842", "https://example.org/x"],
        "entry": "search",
    }
    searcho1 = RunResult(
        answer="…",
        steps=[Step(turn=1, tool_calls=[s1a]), Step(turn=2, tool_calls=[s1b])],
        turns=3, stop_reason="answered", explorer_calls=2, usage=Usage(calls=5),
    )

    # ③ depthsearch — 메인 모델이 고른 페치가 재귀 서브트리를 낳는다.
    f1 = fetch("https://en.wikipedia.org/wiki/Delegate_A")
    f1.exploration = {
        **node("https://en.wikipedia.org/wiki/Delegate_A", 1, "partial",
               opened=[
                   node("https://en.wikipedia.org/wiki/Delegate_A#cite_note-3", 2, "answered",
                        opened=[node("https://archives.gov/records/treaty-1840", 3, "answered")]),
                   node("https://en.wikipedia.org/wiki/Treaty_list", 2, "not_found"),
               ]),
        "entry": "fetch",
    }
    f2 = fetch("https://archives.gov/records/treaty-1842")
    f2.exploration = {
        **node("https://archives.gov/records/treaty-1842", 1, "answered"),
        "entry": "fetch",
    }
    depthsearch = RunResult(
        answer="…",
        steps=[
            Step(turn=1, tool_calls=[search("treaty delegate signed two")]),
            Step(turn=2, tool_calls=[f1]),
            Step(turn=3, tool_calls=[search("delegate A 1842 treaty")]),
            Step(turn=4, tool_calls=[f2]),
        ],
        turns=5, stop_reason="answered",
        expansion_nodes=3, max_depth_reached=3, explorer_calls=5, dead_dives=1,
        usage=Usage(calls=9),
    )

    return {"ragent": ragent, "search-o1": searcho1, "depthsearch": depthsearch}


if __name__ == "__main__":
    raise SystemExit(main())
