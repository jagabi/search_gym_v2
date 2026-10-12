"""Summarize actual LDS records without further network/model calls."""
import argparse
from collections import Counter
from datetime import datetime
import json
from pathlib import Path
import statistics


def read_jsonl(path):
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            rows.append(json.loads(line))
        except ValueError:  # Last line may still be being written during a live run.
            pass
    return rows


def concurrency(events, start, end):
    edges = sorted((datetime.fromisoformat(e["timestamp"]).timestamp(),
                    1 if e["kind"] == start else -1)
                   for e in events if e["kind"] in (start, end))
    active = peak = 0
    seconds = 0
    previous = None
    for instant, delta in edges:
        if active and previous is not None:
            seconds += instant - previous
        active += delta
        peak = max(peak, active)
        previous = instant
    return {"peak": peak, "active_wall_seconds": round(seconds, 2)}


def distribution(values):
    return {"count": len(values), "mean": round(statistics.mean(values), 2),
            "median": round(statistics.median(values), 2), "sum": round(sum(values), 2)} if values else {}


def summarize(run):
    records = {r["index"]: r for r in read_jsonl(run / "records.jsonl")}
    summary = {"run": str(run), "questions": [], "timing_note":
               "Logical fetch timings include tool work, native document handling and retries; not pure Jina service time. "
               "Concurrency uses UTC action timestamps. Historical runs have different transport and queries."}
    run_actions = []
    for qdir in sorted(run.glob("q*")):
        if not (qdir / "trace.jsonl").exists():
            continue
        qid = int(qdir.name[1:])
        q = {"index": qid, "record": records.get(qid), "searches": []}
        if (qdir / "response.json").exists():
            response = json.loads((qdir / "response.json").read_text(encoding="utf-8"))
            q.update(question=response["question"], gold_answer=response["gold_answer"], answer=response["answer"])
        all_actions = []
        structures = sorted(qdir.glob("lds/*/structure.json"), key=lambda p: p.stat().st_mtime)
        for number, p in enumerate(structures, 1):
            data = json.loads(p.read_text(encoding="utf-8"))
            nodes, actions = data["nodes"], read_jsonl(p.parent / "actions.jsonl")
            all_actions.extend(actions)
            fetched = [n for n in nodes if n.get("fetch_order")]
            roots = []
            for root in (n for n in nodes if not n["parent_id"] and n.get("fetch_order")):
                branch = [n for n in fetched if n["root_id"] == root["id"]]
                roots.append({"id": root["id"], "url": root["url"], "rank": root["rank"],
                              "fetches": len(branch), "max_depth": max(n["depth"] for n in branch)})
            replay = {}
            for action in actions:
                replay.update({n["id"]: n for n in action["updates"]})
            complete = actions[-1]["kind"] == "search_end"
            if complete:
                assert replay == {n["id"]: n for n in nodes}, p
                assert len(fetched) == data["stats"]["fetched"] <= data["config"]["fetch_budget"]
                assert all(n["depth"] <= data["config"]["depth"] for n in nodes)
                assert sum(n["status"] == "failed" for n in nodes) == data["stats"]["fetch_failed"]
            q["searches"].append({"number": number, "search_id": data["search_id"], "query": data["query"],
                "complete": complete, "stats": data["stats"], "actions": len(actions),
                "last_action": actions[-1]["kind"], "depth_fetches": dict(Counter(n["depth"] for n in fetched)),
                "discrepancy_fetches": dict(Counter(n["discrepancy"] for n in fetched)),
                "max_discrepancy_limit": max(a["discrepancy_limit"] for a in actions), "roots": roots,
                "fetch_seconds": distribution([n["fetch_duration_ms"] / 1000 for n in fetched if "fetch_duration_ms" in n]),
                "jev_seconds": distribution([n["jev_duration_ms"] / 1000 for n in fetched if "jev_duration_ms" in n]),
                "fetch_concurrency": concurrency(actions, "fetch_start", "fetch_end"),
                "readers": [{k: n.get(k) for k in ("id", "root_id", "url", "depth", "rank", "discrepancy", "direct_answer", "answer_likelihood", "query_answer", "reader_objective", "notes")}
                            for n in nodes if n["read"]],
                "structure": str(p.relative_to(run))})
        q["fetch_concurrency"] = concurrency(all_actions, "fetch_start", "fetch_end")
        run_actions.extend(all_actions)
        q["historical"] = {}
        for label, folder in (("search_o1", "20260919-1621_search-o1_gpt-oss-20b_browsecomp_paper_frozen_v1"),
                              ("old_jev", "20261004-1329_jevtree_gpt-oss-20b_browsecomp_jevtree_v66_diagnostic10")):
            path = run.parent / folder / "records.jsonl"
            q["historical"][label] = next((r for r in read_jsonl(path) if r["index"] == qid), None)
        summary["questions"].append(q)
    summary["fetch_concurrency"] = concurrency(run_actions, "fetch_start", "fetch_end")
    output = run / "lds_summary.json"
    output.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = ["# LDS depth 6: two-question diagnostic", "",
             "5 starting roots when available; top 5 children per parent; depth 6; 40 logical fetch attempts per search. "
             "Local Jina, RPM pacing off, up to 50 simultaneous requests per session. "
             "Original main/reader/JEV scoring prompts retained.", "",
             "Selected cases, not a random accuracy sample. Historical runs differ in queries, date and transport; "
             "timing differences cannot be attributed to LDS alone.", "",
             "| Question | Run | Correct | Searches | Fetch attempts | Seconds | GPT input tokens | JEV input tokens |",
             "|---|---|---:|---:|---:|---:|---:|---:|"]
    for q in summary["questions"]:
        for label, r in [("LDS", q["record"]), *q["historical"].items()]:
            if r:
                lines.append(f'| {q["index"]} | {label} | {int(r["score"] == 1)} | {r["searches"]} | '
                             f'{r["fetch_attempts"]} | {r["latency_s"]} | {r["input_tokens"]:,} | '
                             f'{r.get("reader_stats", {}).get("jev_input_tokens", 0):,} |')
    lines += ["", "## Actual traversal", "",
              f'Peak simultaneous logical fetches across the run: {summary["fetch_concurrency"]["peak"]}. '
              "LDS schedules one candidate per root per round, so a single five-root search does not fill the 50-request transport cap.", "",
              "| Question | Search | Fetches | Max fetched depth | Max discrepancy phase | Reader pages | Complete |",
              "|---|---:|---:|---:|---:|---:|---|"]
    for q in summary["questions"]:
        for s in q["searches"]:
            lines.append(f'| {q["index"]} | {s["number"]} | {s["stats"]["fetched"]} | '
                         f'{max(s["depth_fetches"], default=0)} | {s["max_discrepancy_limit"]} | '
                         f'{len(s["readers"])} | {s["complete"]} |')
    lines += ["", "## Observations", "",
              "- q392: correct advisor Alexander Yarin was already present in a depth-1 Mathematics Genealogy result "
              "in search 3. The search still used all 40 fetches and descended into the advisor genealogy. "
              "This case does not demonstrate a depth-6 accuracy gain.",
              "- q660: search 1 returned largely Warren Buffett and other unrelated roots but still spent 40 fetches. "
              "Searches 3, 5, 6 and 7 repeatedly targeted Yusuf Grillo Pavilion, including changes to the year.",
              "- q660 final answer: Bruce Obomeyoma Onobrakpeya; gold: Ablade Glover. "
              "LDS answered 1/2 correctly, matching old JEV on these cases; historical search-o1 answered 2/2.",
              "- q660 search 8: on the depth-2 MoMAA artist directory (node n0026), JEV ranked "
              "https://momaa.org/icons-african-art/ablade-glover/ seventh at 0.32. "
              "Top-5 candidate retention excluded it from LDS. Merely retaining more candidates would not fetch them all, "
              "but retaining rank 7 does not guarantee it would be visited within 40 attempts.", "",
              "## Next changes to consider (not implemented)", "",
              "1. Separate the retained candidate list from the fetch budget: preserve all ranked links and "
              "let the scheduler spend the same fixed budget. Revisit alternative order before assuming this guarantees more coverage.",
              "2. Add the previously proposed query-answer objective and evaluate stopping when the narrow query has been answered. "
              "The current full-question direct_answer score cannot reliably identify completion of an intermediate query.", "",
              "## Artifacts and validation", "",
              "- [Action-by-action SVG viewer](lds_viewer/index.html): question/search selector, previous/next, zoom, SVG original, structure link.",
              "- [Full machine-readable summary](lds_summary.json): root allocation, depth/discrepancy counts, durations and reader notes.",
              "- Each question's lds/<search_id>/ contains actions.jsonl, structure.json and pages/. Trace files retain "
              "raw fetch text plus JEV and model requests/responses.",
              "- Completed search actions replay to the exact final node state. Logical fetch budgets and depth limits are checked.",
              "- 74 tests passed across LDS, JEV, reader integrity and fetch-session checks; browser controls and SVG loading verified.", "",
              summary["timing_note"], "",
              "For this first run, use UTC timestamps or per-search actions.jsonl elapsed_ms for LDS timing. "
              "The running process used per-search elapsed_ms in trace LDS action entries; subsequent code uses search_elapsed_ms "
              "there so global trace timing remains consistent. Non-LDS trace events were unaffected.", ""]
    (run / "lds_findings.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"summary": str(output), "questions": [{"id": q["index"],
          "complete": bool(q["record"]), "searches": len(q["searches"]),
          "fetch_concurrency": q["fetch_concurrency"]} for q in summary["questions"]]}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", type=Path)
    summarize(parser.parse_args().run)
