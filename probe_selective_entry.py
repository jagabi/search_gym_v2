"""Replay isolated saved search batches through the real DS selector.

No web search, page fetch, recursion or judge calls. Only the configured model is
called, once per case/repetition. This diagnostic is NOT benchmark accuracy.
Use --dry-run to inspect the cases without any model/network calls.
"""
from __future__ import annotations

import argparse
import asyncio
import json
from collections import Counter
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

from searchgym.agent import RunResult, SearchAgent
from searchgym.config import load_test
from searchgym.report import enable_utf8
from searchgym.research_state import ResearchState, SELECT_PROMPT, SELECT_FETCH_TOOL, parse_control, source_key
from searchgym.serving import profile_for
from searchgym.trace import Trace


ROOT = Path(__file__).resolve().parent
DEFAULT_RUN = ROOT / "runs/test/20260921-0016_depthsearch_gpt-oss-20b_browsecomp_paper_frozen_v1"
# Manually audited useful entry pages, never provided to the selector as labels.
# Matching a reference is useful-source selection, NOT proof of answering correctly.
REFERENCES = (
    (8, "https://en.wikipedia.org/wiki/Michael_Radford", "previously_missed"),
    (326, "https://www.kidlit411.com/2014/04/kidlit411-author-spotlight-Fran-Manushkin.html", "previously_missed"),
    (334, "https://www.31percentwool.com/post/future-of-fonts", "previously_missed"),
    (510, "https://www.americanpancake.com/2020/04/rosenfeld-and-blues-rock-noir-tingle-of.html", "previously_missed"),
    (972, "https://iorr.org/talk/read.php?1,1348623601,newer", "previously_missed"),
    (898, "https://en.wikipedia.org/wiki/Raphael_Armattoe", "previously_correct"),
    (1237, "https://www.boxofficeindia.com/years.php?year=2012&pageId=4", "previously_correct"),
)


def load_cases(run: Path) -> list[dict]:
    cases = []
    for index, reference, group in REFERENCES:
        response = json.loads((run / f"q{index:05d}" / "response.json").read_text(encoding="utf-8"))
        found = None
        for step in response["steps"]:
            for call in step.get("tool_calls", []):
                if call["name"] != "web_search" or call.get("refused") or call.get("is_error"):
                    continue
                try:
                    payload = json.loads(call["result"]) if isinstance(call["result"], str) else call["result"]
                except (TypeError, ValueError):
                    continue
                entries = payload.get("organic", []) if isinstance(payload, dict) else []
                if any(e.get("link") == reference for e in entries):
                    found = {"id": index, "question": response["question"], "turn": step["turn"],
                             "entries": entries, "reference": reference, "group": group,
                             "query": call.get("arguments", {}).get("query", "")}
                    break
            if found:
                break
        if found is None:
            raise ValueError(f"q{index:05d}: audited URL absent from saved search results; do not silently replace the case")
        cases.append(found)
    return cases


def case_state(case: dict) -> tuple[ResearchState, list[str]]:
    """Build only from observable search entries; no answers or reference labels."""
    state = ResearchState()
    ids = []
    for entry in case["entries"]:
        try:
            ids.append(state.register(str(entry.get("link") or ""),
                                      title=str(entry.get("title") or ""),
                                      snippet=str(entry.get("snippet") or ""), search_entry=True))
        except ValueError:
            continue
    return state, ids


async def replay_case(agent: SearchAgent, case: dict, trace: Trace) -> dict:
    state, ids = case_state(case)
    result = RunResult(research_state=state)
    selected = await agent._control(case["question"], result, trace, ids, select=True, query=case.get("query", ""))
    url = state.sources[selected]["url"] if selected else None
    return {"id": case["id"], "saved_turn": case["turn"], "group": case["group"],
            "selected": selected, "selected_url": url, "reference_url": case["reference"],
            "reference_hit": bool(url and source_key(url) == source_key(case["reference"])),
            "checkpoint": state.snapshot(), "usage": result.usage.as_dict(),
            "note": "A different selected source may also be useful; this is not an accuracy label."}


def inspect_probe(directory: Path) -> dict:
    """Read existing traces only; never instantiate a model or change old results."""
    paths = sorted(directory.glob("q*.jsonl"))
    if not paths:
        raise ValueError(f"No probe traces found in {directory}")
    rows = []
    for path in paths:
        selectable = []
        for line in path.read_text(encoding="utf-8-sig").splitlines():
            event = json.loads(line)
            if event.get("event") == "control.request":
                for message in event.get("messages", []):
                    if message.get("role") == "user":
                        payload = json.loads(message["content"])
                        selectable = payload.get("selectable", [])
            if event.get("event") != "control.response":
                continue
            body = event.get("text") or ""
            reasoning = event.get("reasoning") or ""
            parsed = parse_control(body)
            detail = ""
            if event.get("decision"):
                category = event["decision"]
            elif event.get("finish_reason") == "length":
                category = "truncated"
            elif event.get("tool_calls"):
                category = "unexpected_tool_calls"
            elif not body.strip():
                category = "reasoning_only" if reasoning.strip() else "empty_response"
            elif not parsed:
                category = "invalid_json_or_empty_object"
                try:
                    value = json.loads(body)
                    detail = f"JSON type: {type(value).__name__}"
                except ValueError as exc:
                    detail = str(exc)
            elif event.get("valid") is False:
                category = "rejected_despite_parseable_json"
                detail = "Older traces do not record tool calls; inspect transport output."
            elif "read" not in parsed:
                category = "missing_read_field"
            elif parsed["read"] is None:
                category = "explicit_skip"
            elif not isinstance(parsed["read"], str) or parsed["read"] not in selectable:
                category = "invalid_source_id"
            else:
                category = "selected_source"
            rows.append({"file": path.name, "category": category, "detail": detail,
                         "finish_reason": event.get("finish_reason"),
                         "text_chars": len(body), "reasoning_chars": len(reasoning),
                         "read": event.get("selected", parsed.get("read")), "text": body, "reasoning": reasoning,
                         "tool_calls": event.get("tool_calls", [])})
    if not rows:
        raise ValueError("No control.response events found; inspect control.error events in the traces.")
    summary = dict(Counter(row["category"] for row in rows))
    report = {"directory": str(directory.resolve()), "responses": len(rows),
              "categories": summary, "rows": rows,
              "note": "Offline inspection only. Original responses retained; no model calls or result changes."}
    output = directory / "inspection.json"
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    for row in rows:
        print(f"{row['file']}: {row['category']} finish={row['finish_reason']} "
              f"text={row['text_chars']} reasoning={row['reasoning_chars']} read={row['read']}")
    for category in summary:
        example = next(row for row in rows if row["category"] == category)
        print(f"\n--- {category}: {example['file']} ---")
        print(example["detail"])
        print("TEXT:\n" + example["text"][:4000])
        if example["tool_calls"]:
            print("TOOL CALLS:\n" + json.dumps(example["tool_calls"], ensure_ascii=False))
        print("REASONING (first 2000 chars):\n" + example["reasoning"][:2000])
    print(f"\nFull diagnostic: {output}")
    return report


async def run(args) -> None:
    cases = load_cases(Path(args.run))
    for case in cases:
        rank = next(i for i, e in enumerate(case["entries"], 1) if e.get("link") == case["reference"])
        print(f"q{case['id']:05d}  saved turn={case['turn']}  reference rank={rank}  {case['group']}")
    print(f"\n{len(cases)} cases x {args.repeats} repetitions = {len(cases) * args.repeats} selector calls; no web/fetch/judge calls.")
    if args.dry_run:
        return

    config = load_test(args.conf, method="depthsearch")
    config.agent.depthsearch_control = True
    out = ROOT / "runs/selector_probe" / datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    out.mkdir(parents=True)
    (out / "config.json").write_text(json.dumps({"agent": asdict(config.agent), "model": config.model,
        "source_run": str(Path(args.run).resolve()), "repeats": args.repeats,
        "scope": "Isolated search-batch diagnosis; fresh state each time, no end-to-end scoring."}, indent=2), encoding="utf-8")
    (out / "selector_prompt.txt").write_text(SELECT_PROMPT, encoding="utf-8")
    (out / "selector_tool.json").write_text(json.dumps(SELECT_FETCH_TOOL, indent=2), encoding="utf-8")
    agent = SearchAgent(profile_for(config.model), config.agent, method="depthsearch")
    semaphore = asyncio.Semaphore(config.run.workers)
    async def one(case, repetition):
        async with semaphore:
            trace = Trace(out / f"q{case['id']:05d}_{repetition}.jsonl", f"q{case['id']}-{repetition}")
            value = await replay_case(agent, case, trace)
            value["repetition"] = repetition
            print(f"q{case['id']:05d}/{repetition}: reference_hit={value['reference_hit']} selected={value['selected_url']}")
            (out / f"q{case['id']:05d}_{repetition}.json").write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")
            return value
    try:
        rows = await asyncio.gather(*(one(c, n) for c in cases for n in range(1, args.repeats + 1)))
    finally:
        await agent.aclose()
    summary = {"attempts": len(rows), "reference_hits": sum(r["reference_hit"] for r in rows),
        "selected_any": sum(bool(r["selected"]) for r in rows),
        "controller_invalid": sum(r["checkpoint"]["metrics"].get("controller_invalid", 0) for r in rows),
        "controller_skips": sum(r["checkpoint"]["metrics"].get("controller_skips", 0) for r in rows),
        "controller_errors": sum(r["checkpoint"]["metrics"].get("controller_errors", 0) for r in rows),
        "usage": {k: sum(r["usage"][k] for r in rows) for k in ("calls", "input_tokens", "output_tokens")},
        "interpretation": "Curated diagnostic, not benchmark accuracy. Missed reference can be another useful source. No live source availability or final-answer performance tested."}
    (out / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    print(f"\nResults: {out}")


def main() -> None:
    enable_utf8()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--conf", default="conf.yaml")
    parser.add_argument("--run", default=str(DEFAULT_RUN))
    parser.add_argument("--repeats", type=int, default=2)
    parser.add_argument("--dry-run", action="store_true", help="Read saved inputs only; no model/network calls")
    parser.add_argument("--inspect", type=Path, metavar="PROBE_DIR",
                        help="Inspect existing probe responses offline; no model/network calls")
    args = parser.parse_args()
    if args.inspect is not None:
        inspect_probe(args.inspect)
        return
    if args.repeats < 1:
        parser.error("--repeats must be positive")
    asyncio.run(run(args))


if __name__ == "__main__":
    main()
