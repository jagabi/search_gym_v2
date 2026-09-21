"""모델도 네트워크도 없이 **전 경로**를 한 번 돌린다. 런팟 켜기 전 마지막 점검.

    python tests/offline.py              # 세 방법 전부
    python tests/offline.py --method depthsearch --verbose

가짜 LLM 과 가짜 도구를 물려 `SearchAgent.run()` → `Explorer.explore()` (재귀) →
`Runner` → 채점 → `summary.json` · `tree.svg` 까지 실제 코드 경로를 그대로 태운다.
API 키도 GPU 도 필요 없다.

여기서 잡히는 것: 배선 오류, 시그니처 불일치, 예산 회계 실수, 재귀 종료 조건, 기록
파일 생성. 여기서 못 잡는 것: 모델이 실제로 도구를 부르는지, 사고가 분리되는지 —
그건 `tests/model.py` 가 본다.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import shutil
import sys
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from searchgym.agent import SearchAgent  # noqa: E402
from searchgym.benchmarks import load_benchmark  # noqa: E402
from searchgym.config import load_test  # noqa: E402
from searchgym.explorer import Document  # noqa: E402
from searchgym.llm import Reply, Usage, estimate_tokens  # noqa: E402
from searchgym.paths import resolve  # noqa: E402
from searchgym.report import enable_utf8, summarize, table  # noqa: E402
from searchgym.runner import Runner  # noqa: E402
from searchgym.scoring import Judgement  # noqa: E402
from searchgym.serving import profile_for  # noqa: E402
from searchgym.trace import Trace  # noqa: E402
from searchgym.research_state import SELECT_PROMPT, CONTROL_PROMPT  # noqa: E402

OUT = "runs/_offline"


# --- 가짜 도구 ---------------------------------------------------------------

_RESULTS = [
    {"title": "Treaty of Example — Wikipedia", "link": "https://en.wikipedia.org/wiki/Treaty",
     "snippet": "The treaty was concluded in the 1840s between the parties."},
    {"title": "National Archives: Treaty records", "link": "https://archives.example/treaty",
     "snippet": "Scanned records of the signing, including the register."},
    {"title": "Britannica — Treaty", "link": "https://britannica.example/treaty",
     "snippet": "Overview of the treaty and its consequences."},
    {"title": "A blog about treaties", "link": "https://blog.example/treaties",
     "snippet": "Some general commentary."},
    {"title": "Treaty text (PDF mirror)", "link": "https://mirror.example/treaty.pdf",
     "snippet": "Full text of the treaty."},
    {"title": "Extra result 6", "link": "https://extra.example/6", "snippet": "…"},
]


class FakeTools:
    """WebTools 의 최소 대역. 실제 인터페이스만 흉내낸다."""

    def __init__(self) -> None:
        self.fetched: list[str] = []
        self.searched: list[str] = []
        self.specs = [
            SimpleNamespace(
                name=name,
                as_openai=lambda n=name: {
                    "type": "function",
                    "function": {
                        "name": n,
                        "description": f"fake {n}",
                        "parameters": {"type": "object", "properties": {}},
                    },
                },
            )
            for name in ("web_search", "web_fetch")
        ]

    def specs_for(self, names: list[str]):
        wanted = {n.lower() for n in names}
        return [s for s in self.specs if s.name.lower() in wanted]

    async def search(self, query: str):
        self.searched.append(query)
        payload = {"organic": list(_RESULTS), "answer_box": {"answer": "1840"}}
        return payload, SimpleNamespace(
            is_error=False, duration_ms=12.0, text=json.dumps(payload, ensure_ascii=False)
        )

    async def fetch(self, url: str) -> Document:
        self.fetched.append(url)
        if "broken" in url:
            return Document(url=url, content="HTTP 500", is_error=True)
        # 본문 안에 인라인 링크를 심어 둔다. explorer 가 이걸 따라간다.
        body = (
            f"# Page at {url}\n\n"
            "The treaty was signed in the 1840s. The exact date appears in the "
            f"register, see [footnote]({url}/ref-1) for the scanned entry.\n\n"
            + ("Lorem ipsum dolor sit amet. " * 400)
        )
        return Document(url=url, content=body)

    async def fetch_many(self, entries):
        return [await self.fetch(str(e.get("link") or "")) for e in entries]

    async def call(self, name: str, arguments: dict):
        if name == "web_search":
            _, outcome = await self.search(str(arguments.get("query") or ""))
            return outcome
        document = await self.fetch(str(arguments.get("url") or ""))
        return SimpleNamespace(
            text=document.content, is_error=document.is_error, duration_ms=30.0
        )


# --- 가짜 LLM ---------------------------------------------------------------


class FakeLLM:
    """LLM 의 최소 대역. 메시지를 보고 누가 부르는지 판단해 각본대로 답한다."""

    def __init__(self, profile, explorer_marker: str) -> None:
        self.profile = profile
        self.model_name = profile.repo
        self.base_url = "fake://"
        self.marker = explorer_marker
        self.calls: list[str] = []

    async def chat(self, messages, *, max_tokens, tools=None, usage=None, tool_choice=None) -> Reply:
        system = messages[0]["content"] if messages and messages[0]["role"] == "system" else ""
        turn = sum(1 for m in messages if m["role"] == "assistant") + 1
        names = {t["function"]["name"] for t in (tools or [])}
        who = "explorer" if self.marker in system else "agent"
        if SELECT_PROMPT.strip() in system:
            who = "selector"
        elif CONTROL_PROMPT.strip() in system:
            who = "state"
        self.calls.append(f"{who}:t{turn}:tools={sorted(names) or '-'}")

        if usage is not None:
            usage.add(1000 * turn, 200, 80)

        if who == "selector":
            payload = json.loads(messages[-1]["content"])
            candidates = [s for s in payload["sources"] if s["id"] in payload["selectable"]]
            target = next((s for s in candidates if "archives.example" in s["url"]), None)
            reply = (_tool_reply("web_fetch", {"url": target["url"]}) if target
                     else Reply(text="No useful unread source.", finish_reason="stop"))
        elif who == "state":
            reply = Reply(text='{"candidates":[]}', finish_reason="stop")
        elif who == "explorer":
            reply = self._explorer(messages, turn, names)
        else:
            reply = self._agent(turn, names)
        reply.prompt_tokens, reply.completion_tokens = 1000 * turn, 200
        return reply

    def _agent(self, turn: int, names: set[str]) -> Reply:
        if turn == 1:
            return _tool_reply("web_search", {"query": "treaty signing date register"},
                               reasoning="I need the signing date. Searching.")
        if turn == 2 and "web_fetch" in names:
            return _tool_reply("web_fetch", {"url": _RESULTS[1]["link"]},
                               reasoning="The archives record looks authoritative. Opening it.")
        return Reply(
            reasoning="I have the date now.",
            text="The treaty was signed on 6 February 1840.",
            finish_reason="stop",
        )

    def _explorer(self, messages, turn: int, names: set[str]) -> Reply:
        # 도구가 있고 첫 턴이면 본문의 각주 링크를 하나 연다. 그 다음은 마무리.
        if "web_fetch" in names and turn == 1:
            page = _last_page_url(messages)
            return _tool_reply(
                "web_fetch", {"url": f"{page}/ref-1"},
                reasoning="This page points at the register footnote for the exact date.",
            )
        return Reply(
            reasoning="Extracting the date.",
            text=(
                "**Final Information**\n\n"
                "The register records the signing on 6 February 1840.\n\n"
                "**Status:** partial"
            ),
            finish_reason="stop",
        )

    async def cap(self, text: str, limit_tokens: int):
        if limit_tokens <= 0 or estimate_tokens(text) <= limit_tokens:
            return text, False
        keep = max(0, limit_tokens * 3)
        return text[:keep], True

    async def count_tokens(self, text: str) -> int:
        return estimate_tokens(text)

    async def aclose(self) -> None:
        return None


def _tool_reply(name: str, arguments: dict, reasoning: str = "") -> Reply:
    call = SimpleNamespace(
        id=f"call_{name}_{abs(hash(json.dumps(arguments, sort_keys=True))) % 10000}",
        function=SimpleNamespace(name=name, arguments=json.dumps(arguments)),
    )
    return Reply(reasoning=reasoning, text="", tool_calls=[call], finish_reason="tool_calls")


def _last_page_url(messages) -> str:
    """user 메시지에 박힌 '[1] title — url' 에서 url 을 뽑는다."""
    for message in messages:
        if message["role"] != "user":
            continue
        for line in str(message["content"]).splitlines():
            if line.startswith("[") and " — " in line:
                return line.split(" — ", 1)[1].strip()
    return "https://example.invalid/page"


class FakeJudge:
    model = "fake-judge"

    def grade(self, benchmark, item, answer: str) -> Judgement:
        parts = item.answer_parts or [item.answer]
        return Judgement(
            parts=[(p, i == 0) for i, p in enumerate(parts)],
            excessive=[],
            explanation="fake",
            extracted=answer[:60],
        )


# --- 실행 --------------------------------------------------------------------


async def run_method(method: str, verbose: bool) -> dict:
    config = load_test("conf.yaml", method=method)
    profile = profile_for(config.model)
    marker = config.explorer_prompt.splitlines()[0] if config.explorer_prompt else "\0"

    out = resolve(OUT) / method
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir(parents=True, exist_ok=True)

    benchmark = load_benchmark(config.benchmark.name, config.benchmark.dataset("validation"))
    items = benchmark.load(limit=2)

    runner = Runner(
        profile=profile,
        agent_config=config.agent,
        judge=FakeJudge(),  # type: ignore[arg-type]
        run_dir=out,
        method=method,
        explorer_config=config.explorer if config.uses_explorer else None,
        explorer_prompt=config.explorer_prompt,
        cache_root=out / "_cache",
        use_cache=False,
        workers=1,
    )
    llm = FakeLLM(profile, marker)
    runner.agent.llm = llm  # type: ignore[assignment]

    tools = FakeTools()
    records = []
    for item in items:
        records.append(
            await runner.run_one(benchmark, item, config.system_prompt, tools, stage="")
        )

    summary = summarize(records)
    (out / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    first = records[0]
    checks = {
        "실행 완료": first.result.stop_reason == "answered",
        "답변 있음": bool(first.result.answer.strip()),
        "에러 없음": first.result.error is None,
        "검색 기록": first.result.searches > 0,
        "trace.jsonl": (out / first.dir / "trace.jsonl").exists(),
        "response.json": (out / first.dir / "response.json").exists(),
        "tree.svg": (out / first.dir / "tree.svg").exists(),
        "records.jsonl": (out / "records.jsonl").exists(),
    }
    if config.uses_explorer:
        checks["explorer 호출"] = first.result.explorer_calls > 0
        checks["explorer.json"] = (out / first.dir / "explorer.json").exists()
    if config.explorer.recursive:
        checks["재귀 확장"] = first.result.expansion_nodes > 0
        checks["depth 2 이상 도달"] = first.result.max_depth_reached >= 2
        checks["예산 회계"] = (
            first.result.budget.get("used", 0) == first.result.expansion_nodes
        )

    if verbose:
        print("\nLLM 호출 순서:")
        for line in llm.calls:
            print(f"  {line}")
        print(f"\n페치한 URL: {tools.fetched}")
        print(f"\n게이트가 마지막으로 받은 도구 결과:")
        for step in first.result.steps:
            for call in step.tool_calls:
                print(f"  --- {call.name} {call.arguments}")
                print("  " + str(call.result)[:300].replace("\n", "\n  "))

    return {
        "checks": checks,
        "record": first,
        "summary": summary,
        "dir": out,
        "llm_calls": len(llm.calls),
        "fetched": len(tools.fetched),
    }


def main(argv: list[str] | None = None) -> int:
    enable_utf8()
    parser = argparse.ArgumentParser(description="오프라인 전 경로 점검")
    parser.add_argument("--method", default=None, help="하나만 돌린다")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args(argv)

    methods = [args.method] if args.method else ["ragent", "search-o1", "depthsearch"]
    failed = 0

    for method in methods:
        print(f"\n{'=' * 66}\n{method}\n{'=' * 66}")
        try:
            outcome = asyncio.run(run_method(method, args.verbose))
        except Exception as exc:  # noqa: BLE001
            import traceback

            traceback.print_exc()
            print(f"실패: {exc!r}", file=sys.stderr)
            failed += 1
            continue

        record, summary = outcome["record"], outcome["summary"]
        table(
            "결과",
            {
                "stop_reason": record.result.stop_reason,
                "searches / fetches": f"{record.result.searches} / {record.result.fetches}",
                "expansion / depth": (
                    f"{record.result.expansion_nodes} / {record.result.max_depth_reached}"
                ),
                "explorer 호출": record.result.explorer_calls,
                "예산": record.result.budget or "(없음)",
                "LLM 호출": outcome["llm_calls"],
                "페치": outcome["fetched"],
                "f1": f"{summary.get('f1', 0):.2f}",
                "run_dir": outcome["dir"],
            },
        )
        for name, ok in outcome["checks"].items():
            print(f"  [{'O' if ok else 'X'}] {name}")
            failed += 0 if ok else 1

    print(f"\n{'-' * 66}")
    print("전부 통과" if not failed else f"{failed}건 실패")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
