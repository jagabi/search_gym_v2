"""Replay saved fetch/skip/invalid entry decisions with the legacy DS selector.

This does not exercise the independent_clues policy now enabled in DS config.

Only selection model calls run. No search, fetch, reader, or judge calls. Stops
at the first valid selection/normal reply; this does NOT test end-to-end accuracy
or simulate reading pages. --dry-run reads files only.
"""
from __future__ import annotations

import argparse
import asyncio
import copy
import json
from collections import Counter
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

from searchgym.agent import RunResult, SearchAgent, _FetchSession
from searchgym.config import load_test
from searchgym.report import enable_utf8
from searchgym.research_state import ResearchState, SELECT_PROMPT, source_key
from searchgym.serving import profile_for
from searchgym.trace import Trace


ROOT = Path(__file__).resolve().parent
DEFAULT_RUN = ROOT / "runs/test/20260922-0859_depthsearch_gpt-oss-20b_browsecomp_ds_answer_phase_v4"
GROUPS = ("fetch", "skip", "invalid_tool_call")


def load_saved_cases(run: Path, per_group: int = 3) -> list[dict]:
    """Stratify on old decision and menu size, never correctness or gold answers."""
    groups = {g: [] for g in GROUPS}
    for directory in sorted(run.glob("q*")):
        response_path, trace_path = directory / "response.json", directory / "trace.jsonl"
        if not response_path.exists() or not trace_path.exists():
            continue
        response = json.loads(response_path.read_text(encoding="utf-8"))
        searches = {}
        for step in response["steps"]:
            for call in step.get("tool_calls", []):
                if call["name"] != "web_search" or call.get("refused") or call.get("is_error"):
                    continue
                raw = call.get("result", {})
                try:
                    payload = json.JSONDecoder().raw_decode(raw)[0] if isinstance(raw, str) else raw
                except ValueError:
                    continue
                if isinstance(payload, dict):
                    searches.setdefault(step["turn"], []).extend(payload.get("organic", []))
        turn, query, pending = 0, "", None
        question_groups = {}
        with trace_path.open(encoding="utf-8") as stream:
            for line in stream:
                event = json.loads(line)
                if event["event"] == "tool.call" and event.get("tool") == "web_search":
                    turn, query = event["turn"], event["arguments"].get("query", "")
                if event["event"] == "control.request" and event.get("mode") == "select":
                    pending = json.loads(event["messages"][1]["content"])
                if event["event"] != "control.response" or event.get("mode") != "select" or pending is None:
                    continue
                group = event.get("decision")
                if group not in groups:
                    continue
                # Preserve the largest menu per question/group, then sample across
                # those sizes. Avoid nine early, empty-history toy decisions.
                size = len(pending.get("selectable", []))
                if group in question_groups and question_groups[group]["old_menu_size"] >= size:
                    continue
                observed = [e for t, entries in searches.items() if t <= turn for e in entries]
                question_groups[group] = {
                    "case": f"{directory.name}_t{turn}_{group}", "group": group, "turn": turn,
                    "query": query, "question": pending["question"], "payload": pending,
                    "search_entries": observed, "fresh_entries": searches.get(turn, []),
                    "old_menu_size": size, "old_selected": event.get("selected"),
                }
        for group, case in question_groups.items():
            groups[group].append(case)
    selected = []
    for group, cases in groups.items():
        cases.sort(key=lambda c: (c["old_menu_size"], c["case"]))
        count = min(per_group, len(cases))
        if not count:
            raise ValueError(f"No saved {group} cases in {run}")
        indexes = [round((len(cases) - 1) * (i + 0.5) / count) for i in range(count)]
        selected.extend(cases[i] for i in indexes)
    return selected


def restore_state(case: dict) -> tuple[ResearchState, list[str]]:
    payload = copy.deepcopy(case["payload"])
    state = ResearchState.from_snapshot(payload["working_state"]) or ResearchState()
    # These are observations available AT this decision, not final-run evidence.
    for source in payload["sources"]:
        sid = source["id"]
        state.sources[sid] = {**source, "snippets": [source.get("evidence", "")], "notes": [],
                              "search_entry": False}
        state.by_url[source_key(source["url"])] = sid
    for entry in case["search_entries"]:
        try:
            known = state.source(entry.get("link", ""))
        except ValueError:
            continue
        if known:
            known["search_entry"] = True
    focus = []
    for entry in case["fresh_entries"]:
        try:
            known = state.source(entry.get("link", ""))
        except ValueError:
            continue
        if known:
            focus.append(known["id"])
    return state, list(dict.fromkeys(focus))


async def replay_case(agent: SearchAgent, case: dict, trace: Trace) -> dict:
    state, focus = restore_state(case)
    result, session = RunResult(research_state=state), _FetchSession()
    # Count only this probe's calls, not the historical working state's counters.
    state.metrics = {}
    decisions, selected = [], None
    for _ in range(agent.config.max_tool_recoveries + 1):
        selected = await agent._control(case["question"], result, trace, focus, select=True,
                                        session=session, query=case["query"])
        decisions.append(session.decision)
        if session.decision not in {"invalid_tool_call", "empty_response", "truncated"}:
            break
    return {"case": case["case"], "old_decision": case["group"], "old_menu_size": case["old_menu_size"],
            "new_menu_size": len(state.selectable()), "decisions": decisions,
            "selected_url": state.sources[selected]["url"] if selected else None,
            "metrics": state.metrics, "usage": result.usage.as_dict()}


async def run(args) -> None:
    cases = load_saved_cases(args.run, args.per_group)
    config = load_test(args.conf, method="depthsearch")
    for c in cases:
        state, _ = restore_state(c)
        print(f"{c['case']}: menu {c['old_menu_size']} -> {len(state.selectable())}")
    max_calls = len(cases) * args.repeats * (config.agent.max_tool_recoveries + 1)
    print(f"{len(cases)} cases x {args.repeats} repetitions; at most {max_calls} selection calls, no search/fetch/judge.")
    if args.dry_run:
        return
    output = ROOT / "runs/entry_decision_probe" / datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    output.mkdir(parents=True)
    (output / "config.json").write_text(json.dumps({"source_run": str(args.run.resolve()),
        "agent": asdict(config.agent), "model": config.model, "repeats": args.repeats,
        "selection": "Per old outcome, one largest-menu decision per question; sample menu-size strata.",
        "scope": "Selection and invalid-call recovery only; no page reading or accuracy scoring."}, indent=2), encoding="utf-8")
    (output / "selector_prompt.txt").write_text(SELECT_PROMPT, encoding="utf-8")
    agent = SearchAgent(profile_for(config.model), config.agent, method="depthsearch")
    semaphore = asyncio.Semaphore(config.run.workers)

    async def one(case, repetition):
        async with semaphore:
            name = f"{case['case']}_r{repetition}"
            value = await replay_case(agent, case, Trace(output / f"{name}.jsonl", name))
            value["repetition"] = repetition
            (output / f"{name}.json").write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"{name}: {' -> '.join(value['decisions'])}")
            return value
    try:
        rows = await asyncio.gather(*(one(c, r) for c in cases for r in range(1, args.repeats + 1)))
    finally:
        await agent.aclose()
    summary = {"attempts": len(rows),
        "first_decisions": dict(Counter(r["decisions"][0] for r in rows)),
        "final_decisions": dict(Counter(r["decisions"][-1] for r in rows)),
        "by_old_decision": {g: dict(Counter(r["decisions"][-1] for r in rows if r["old_decision"] == g)) for g in GROUPS},
        "usage": {k: sum(r["usage"][k] for r in rows) for k in ("calls", "input_tokens", "output_tokens")},
        "interpretation": "Protocol diagnosis on saved observations, not source usefulness or benchmark accuracy."}
    (output / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    print(f"Results: {output}")


if __name__ == "__main__":
    enable_utf8()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path, default=DEFAULT_RUN)
    parser.add_argument("--conf", default="conf.yaml")
    parser.add_argument("--per-group", type=int, default=3)
    parser.add_argument("--repeats", type=int, default=1)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.per_group < 1 or args.repeats < 1:
        parser.error("--per-group and --repeats must be positive")
    asyncio.run(run(args))
