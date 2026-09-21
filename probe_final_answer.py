"""Replay final writing on saved empty answers; no search, fetch or judge calls."""
import argparse
import asyncio
import json
from datetime import datetime
from pathlib import Path

from searchgym.agent import SearchAgent, FINAL_SYSTEM
from searchgym.config import load_test
from searchgym.llm import Usage
from searchgym.report import enable_utf8
from searchgym.research_state import ResearchState
from searchgym.serving import profile_for
from searchgym.trace import Trace

ROOT = Path(__file__).resolve().parent
DEFAULT_RUN = ROOT / "runs/test/20260921-2144_depthsearch_gpt-oss-20b_browsecomp_ds_search_main_v3"


def saved_input(response):
    """Pass only the original question and observed results, never evaluation labels."""
    history = [{"role": "user", "content": response["question"]}]
    for step in response["steps"]:
        for call in step.get("tool_calls", []):
            content = call.get("result", "")
            history.append({"role": "tool", "content": content if isinstance(content, str)
                            else json.dumps(content, ensure_ascii=False)})
    state = ResearchState.from_snapshot(response.get("research_state"))
    return history, state.render() if state else ""


async def run(args):
    source = Path(args.run)
    rows = [json.loads(line) for line in (source / "records.jsonl").read_text(encoding="utf-8").splitlines()]
    targets = sorted((row for row in rows if not row.get("answer_chars")), key=lambda r: r["index"])[:args.limit]
    print(f"{len(targets)} saved empty answers; at most {2 * len(targets)} final-writing calls. No search/fetch/judge calls.")
    print("Cases: " + ", ".join(row["dir"] for row in targets))
    if args.dry_run or not targets:
        return
    config = load_test(args.conf, method="depthsearch")
    out = ROOT / "runs/final_probe" / datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    out.mkdir(parents=True)
    (out / "final_prompt.txt").write_text(FINAL_SYSTEM, encoding="utf-8")
    agent = SearchAgent(profile_for(config.model), config.agent, method="depthsearch")
    results = []
    try:
        for row in targets:
            response = json.loads((source / row["dir"] / "response.json").read_text(encoding="utf-8"))
            messages, checkpoint = saved_input(response)
            usage = Usage()
            trace = Trace(out / (row["dir"] + ".jsonl"), row["dir"])
            answer = await agent._salvage(messages, trace, usage, checkpoint=checkpoint, answer_only=True)
            value = {"id": row["index"], "answer": answer, "nonempty": bool(answer), "usage": usage.as_dict()}
            results.append(value)
            (out / (row["dir"] + ".json")).write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"{row['dir']}: nonempty={bool(answer)} calls={usage.calls} chars={len(answer)}")
    finally:
        await agent.aclose()
    summary = {"source_run": str(source), "attempts": len(results), "nonempty": sum(r["nonempty"] for r in results),
        "usage": {k: sum(r["usage"][k] for r in results) for k in ("calls", "input_tokens", "output_tokens")},
        "interpretation": "Output reliability only, not accuracy. Old run results are unchanged."}
    (out / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    print(f"Results: {out}")


def main():
    enable_utf8()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path, default=DEFAULT_RUN)
    parser.add_argument("--conf", default="conf.yaml")
    parser.add_argument("--limit", type=int, default=8)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.limit < 1:
        parser.error("--limit must be positive")
    asyncio.run(run(args))


if __name__ == "__main__":
    main()
