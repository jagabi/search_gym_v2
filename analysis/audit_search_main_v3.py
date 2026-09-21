"""Offline audit of saved BrowseComp runs. No model, search or judge calls."""
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean, median

ROOT = Path(__file__).resolve().parents[1]
RUNS = {
    "ragent": "20260920-2130_ragent_gpt-oss-20b_browsecomp_paper_frozen_v1",
    "search-o1": "20260919-1621_search-o1_gpt-oss-20b_browsecomp_paper_frozen_v1",
    "ds_old": "20260921-0016_depthsearch_gpt-oss-20b_browsecomp_paper_frozen_v1",
    "ds_new": "20260921-2144_depthsearch_gpt-oss-20b_browsecomp_ds_search_main_v3",
}


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def output_kind(e, text_key="text"):
    if e.get("finish_reason") == "length":
        return "length"
    if e.get("tool_calls"):
        return "tool_call"
    if not (e.get(text_key) or "").strip():
        return "empty_content"
    return "text"


def main():
    records, summaries, responses = {}, {}, {}
    for name, folder in RUNS.items():
        path = ROOT / "runs/test" / folder
        rows = [json.loads(line) for line in (path / "records.jsonl").read_text(encoding="utf-8").splitlines()]
        assert len(rows) == len({r["index"] for r in rows}) == 300
        records[name] = {r["index"]: r for r in rows}
        summaries[name] = read(path / "summary.json")
        responses[name] = {i: read(path / row["dir"] / "response.json") for i, row in records[name].items()}
    ids = sorted(records["ds_new"])
    assert all(set(rows) == set(ids) for rows in records.values())
    assert all(responses[m][i]["question"] == responses["ds_new"][i]["question"] for m in RUNS for i in ids)
    overview, paired, trace_stats = {}, {}, {}
    examples = defaultdict(list)
    per_question = {}
    for name, rows in records.items():
        summary = summaries[name]
        overview[name] = {k: summary.get(k) for k in (
            "n", "f1", "empty_answers", "judge_errors", "searches_total", "fetch_attempts_total",
            "fetch_success_rate", "selected_entry_fetches_total", "expansion_nodes_total", "llm_calls",
            "input_tokens", "output_tokens", "latency_s_median", "by_category")}
        overview[name].update({
            "correct": sum(r["f1"] == 1 for r in rows.values()),
            "stops": dict(Counter(r["stop_reason"] for r in rows.values())),
            "judge_error_kinds": dict(Counter(str(r.get("judge_error")) for r in rows.values() if r.get("judge_error"))),
            "turns_max": max(r["turns"] for r in rows.values()),
            "turns_40": sum(r["turns"] >= 40 for r in rows.values()),
            "ten_searches": sum(r["searches"] == 10 for r in rows.values()),
        })
        counters = defaultdict(Counter)
        for i, row in rows.items():
            trace_path = ROOT / "runs/test" / RUNS[name] / row["dir"] / "trace.jsonl"
            local = defaultdict(Counter)
            last_main = None
            final_outputs = []
            control_request = {}
            for line in trace_path.open(encoding="utf-8"):
                event = json.loads(line)
                kind = event.get("event")
                counters["events"][kind] += 1
                if kind == "control.request":
                    control_request = json.loads(event["messages"][-1]["content"])
                elif kind == "control.response":
                    mode = event["mode"]
                    decision = event.get("decision", "valid" if event.get("valid") else "invalid")
                    counters["control_decisions"][mode + ":" + decision] += 1
                    local["control_decisions"][mode + ":" + decision] += 1
                    if not event.get("valid"):
                        form = output_kind(event)
                        counters["control_invalid_forms"][mode + ":" + form] += 1
                        if form == "tool_call":
                            calls = event["tool_calls"]
                            detail = "multiple" if len(calls) != 1 else "wrong_tool"
                            if len(calls) == 1 and calls[0]["name"] == "web_fetch":
                                try:
                                    args = json.loads(calls[0]["arguments"])
                                    if not isinstance(args, dict) or set(args) != {"url"} or not isinstance(args["url"], str):
                                        detail = "argument_schema"
                                    else:
                                        sources = control_request.get("sources", [])
                                        selected = {s["url"] for s in sources if s["id"] in control_request.get("selectable", [])}
                                        detail = "unlisted_url" if args["url"] not in selected else "valid_url_rejected"
                                except (ValueError, TypeError):
                                    detail = "malformed_arguments"
                            counters["invalid_selection_calls"][detail] += 1
                        key = mode + ":" + form
                        if len(examples[key]) < 3 and name == "ds_new":
                            examples[key].append({"id": i, "finish": event.get("finish_reason"),
                                "text": event.get("text"), "reasoning_tail": (event.get("reasoning") or "")[-1000:],
                                "tool_calls": event.get("tool_calls")})
                elif kind == "llm.response":
                    last_main = event
                    form = output_kind(event, "raw_text")
                    counters["main_forms"][form] += 1
                    if form == "empty_content":
                        counters["main_empty_finish"][event.get("finish_reason", "unknown")] += 1
                elif kind == "run.final_response":
                    form = output_kind(event, "raw_text")
                    counters["final_forms"][form] += 1
                    if form == "empty_content":
                        counters["final_empty_finish"][event.get("finish_reason", "unknown")] += 1
                    final_outputs.append({k: event.get(k) for k in ("text", "raw_text", "finish_reason", "tool_calls", "attempt")})
                elif kind == "run.truncated":
                    counters["truncation"][event.get("reason")] += 1
                elif kind == "fetch.source":
                    counters["fetch_status"]["failed" if event.get("is_error") else "ok"] += 1
                elif kind == "expand.failed":
                    error = event.get("error", "")
                    counters["expand_failed_messages"][error[:120]] += 1
                elif kind == "tool.unavailable":
                    counters["unavailable_tools"][event.get("tool")] += 1
            if not row.get("answer_chars"):
                counters["empty_question_last_main"][output_kind(last_main or {}, "raw_text")] += 1
                counters["empty_question_final_patterns"][" / ".join(output_kind(x, "raw_text") for x in final_outputs)] += 1
                if name == "ds_new":
                    examples["empty_questions"].append({"id": i, "searches": row["searches"], "turns": row["turns"],
                        "last_main": last_main, "final_outputs": final_outputs,
                        "draft": responses[name][i].get("research_state", {}).get("draft"),
                        "scores": {m: records[m][i]["f1"] for m in RUNS}})
            if name == "ds_new":
                per_question[i] = {"controls": dict(local["control_decisions"]), "f1": row["f1"],
                    "empty": not row["answer_chars"], "category": row["category"],
                    "searches": row["searches"], "entries": row.get("auto_fetches", 0),
                    "nodes": row["expansion_nodes"]}
        trace_stats[name] = {k: dict(v) for k, v in counters.items()}
    for other in ("ragent", "search-o1", "ds_old"):
        wins = [i for i in ids if records["ds_new"][i]["f1"] > records[other][i]["f1"]]
        losses = [i for i in ids if records["ds_new"][i]["f1"] < records[other][i]["f1"]]
        n = len(wins) + len(losses)
        p = min(1, 2 * sum(math.comb(n, k) for k in range(min(len(wins), len(losses)) + 1)) / 2**n) if n else 1
        paired[other] = {"wins": wins, "losses": losses, "exact_mcnemar_p": p,
            "both_correct": sum(records["ds_new"][i]["f1"] == records[other][i]["f1"] == 1 for i in ids)}
    clean = [i for i in ids if all(not records[m][i].get("judge_error") for m in RUNS)]
    result = {"runs": RUNS, "overview": overview, "paired": paired,
        "common_valid_subset": {"n": len(clean), "correct": {m: sum(records[m][i]["f1"] for i in clean) for m in RUNS}},
        "trace_stats": trace_stats, "examples": dict(examples), "per_question": per_question}
    output = ROOT / "analysis/search_main_v3_audit.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"overview": overview, "paired": paired, "common_valid_subset": result["common_valid_subset"],
        "trace_stats": {m: {k: v for k, v in stats.items() if k not in {"events", "expand_failed_messages"}} for m, stats in trace_stats.items()}}, ensure_ascii=False, indent=2))
    print(output)


if __name__ == "__main__":
    main()
