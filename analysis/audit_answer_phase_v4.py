"""Saved-run diagnosis; reads observations only, performs no live calls."""
import json
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from statistics import median
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from searchgym.research_state import is_search_endpoint
from audit_search_main_v3 import ROOT, RUNS as PREVIOUS

RUNS = {**PREVIOUS, "v4": "20260922-0859_depthsearch_gpt-oss-20b_browsecomp_ds_answer_phase_v4"}


def read(p):
    return json.loads(p.read_text(encoding="utf-8"))


def norm(s):
    return " ".join(re.findall(r"[a-z0-9]+", str(s).lower()))


def main():
    records, overview = {}, {}
    for method, folder in RUNS.items():
        rows = [json.loads(line) for line in (ROOT / "runs/test" / folder / "records.jsonl").read_text(encoding="utf-8").splitlines()]
        assert len(rows) == len({r["index"] for r in rows}) == 300
        records[method] = {r["index"]: r for r in rows}
        overview[method] = {"correct": sum(r["f1"] == 1 for r in rows), "empty": sum(not r["answer_chars"] for r in rows),
            "calls": sum(r["llm_calls"] for r in rows), "median_seconds": median(r["latency_s"] for r in rows),
            "input_tokens": sum(r["input_tokens"] for r in rows), "output_tokens": sum(r["output_tokens"] for r in rows),
            "stops": dict(Counter(r["stop_reason"] for r in rows))}
    ids = set(records["v4"])
    assert all(set(rows) == ids for rows in records.values())
    pairs = {}
    for other in PREVIOUS:
        win = sorted(i for i in ids if records["v4"][i]["f1"] > records[other][i]["f1"])
        loss = sorted(i for i in ids if records["v4"][i]["f1"] < records[other][i]["f1"])
        n = len(win) + len(loss)
        pairs[other] = {"win": win, "loss": loss,
            "both_correct": sum(records["v4"][i]["f1"] == records[other][i]["f1"] == 1 for i in ids),
            "mcnemar_p": min(1, 2 * sum(math.comb(n, k) for k in range(min(len(win), len(loss)) + 1)) / 2**n) if n else 1}
    old_empty = [i for i in ids if not records["ds_new"][i]["answer_chars"]]
    formerly_empty = {"n": len(old_empty), "correct": [i for i in old_empty if records["v4"][i]["f1"] == 1],
        "nonempty": sum(bool(records["v4"][i]["answer_chars"]) for i in old_empty),
        "still_empty": [i for i in old_empty if not records["v4"][i]["answer_chars"]]}
    stats = defaultdict(Counter)
    examples = defaultdict(list)
    menus = []
    cases = {}
    base = ROOT / "runs/test" / RUNS["v4"]
    for i, row in records["v4"].items():
        response = read(base / row["dir"] / "response.json")
        request, main_tools, query, final_attempt = {}, [], "", None
        state = response.get("research_state", {})
        stats["state"]["has_candidates"] += bool(state.get("candidates"))
        stats["state"]["has_draft"] += bool(state.get("draft", {}).get("text"))
        notes = []
        queries, selected, invalid = [], [], []
        stats["depth"][str(row["max_depth_reached"])] += 1
        gold = norm(response["gold_answer"])
        def mentions(text):
            return bool(gold) and len(gold) >= 4 and (" " + gold + " ") in (" " + norm(text) + " ")
        snippets_gold = False
        for step in response["steps"]:
            for call in step.get("tool_calls", []):
                if call["name"] == "web_search" and not call.get("refused"):
                    result = call.get("result", "")
                    if isinstance(result, str):
                        try:
                            search, _ = json.JSONDecoder().raw_decode(result)
                            snippets_gold |= mentions(json.dumps(search, ensure_ascii=False))
                        except ValueError:
                            pass
        for line in (base / row["dir"] / "trace.jsonl").open(encoding="utf-8"):
            e = json.loads(line)
            kind = e.get("event")
            if kind == "control.request":
                request = json.loads(e["messages"][-1]["content"])
                stats["controller_request_chars"][e["mode"] + ":over_20000"] += len(e["messages"][-1]["content"]) > 20000
                if e["mode"] == "select":
                    menus.append({"chars": len(e["messages"][-1]["content"]), "choices": len(request["selectable"])})
            elif kind == "control.response":
                mode = e["mode"]
                decision = e.get("decision", "valid" if e.get("valid") else "invalid")
                stats["controller"][mode + ":" + decision] += 1
                if mode == "select" and decision == "invalid_tool_call":
                    calls = e.get("tool_calls", [])
                    why, url = "malformed_call", ""
                    try:
                        args = json.loads(calls[0]["arguments"])
                        url = args["url"]
                        sources = list({s["id"]: s for s in request.get("working_state", {}).get("sources", []) + request.get("sources", [])}.values())
                        known = next((s for s in sources if s["url"] == url), None)
                        by_id = next((s for s in sources if s["id"] == url), None)
                        if is_search_endpoint(url):
                            why = "search_engine_url"
                        elif known:
                            why = "known_" + known["status"]
                        elif by_id:
                            why = "id_in_url"
                        elif any(s["url"].lower().rstrip("/") == url.lower().rstrip("/") for s in sources):
                            why = "case_or_slash_variant"
                        else:
                            why = "other_unlisted_url"
                        if len(calls) > 1:
                            why = "multiple_calls"
                        elif calls[0]["name"] != "web_fetch":
                            why = "wrong_tool"
                    except (IndexError, ValueError, KeyError, TypeError):
                        pass
                    stats["invalid_select"][why] += 1
                    invalid.append({"why": why, "url": url, "query": query})
                    if len(examples[why]) < 3:
                        examples[why].append({"id": i, "url": url, "query": query, "reasoning_tail": e.get("reasoning", "")[-800:]})
                if mode == "update-only" and not e.get("valid"):
                    form = "length" if e.get("finish_reason") == "length" else "tool_call" if e.get("tool_calls") else "empty" if not e.get("text") else "text"
                    stats["invalid_state"][form] += 1
            elif kind == "llm.request":
                main_tools = e.get("available_tools", [])
            elif kind == "llm.response":
                stats["main"]["total"] += 1
                if not e.get("raw_text") and not e.get("tool_calls"):
                    stats["main"]["empty_with_tools" if main_tools else "empty_no_tools"] += 1
            elif kind == "run.finalizing":
                stats["finalizing"][e.get("reason")] += 1
            elif kind == "run.final_response":
                final_attempt = e.get("attempt")
                form = "length" if e.get("finish_reason") == "length" else "tool_call" if e.get("tool_calls") else "empty" if not e.get("raw_text") else "text"
                stats["final_outputs"][form] += 1
                stats["final_attempts"][str(final_attempt)] += 1
            elif kind == "tool.call" and e.get("tool") == "web_search":
                query = e["arguments"]["query"]
                queries.append(query)
            elif kind == "search.selected_entry":
                selected.append({"turn": e["turn"], "url": e["url"], "query": query})
            elif kind == "search.selected_result":
                stats["entry_status"]["failed" if e.get("is_error") else "ok"] += 1
            elif kind == "explorer.response" and e.get("phase") in {"extract", "recover"}:
                notes.append({"depth": e.get("depth"), "urls": e.get("urls"), "text": e.get("text", "")})
            elif kind == "expand.tool_withdrawn":
                stats["recursive_stop"]["wasted_calls"] += 1
        note_gold = any(mentions(n["text"]) for n in notes)
        child_gold = any(n["depth"] >= 2 and mentions(n["text"]) for n in notes)
        root_gold = any(n["depth"] == 1 and mentions(n["text"]) for n in notes)
        if row["f1"] == 0:
            stats["wrong_answer_mentions"]["in_search"] += snippets_gold
            stats["wrong_answer_mentions"]["in_reader_notes"] += note_gold
        cases[i] = {"question": response["question"], "gold": response["gold_answer"], "answer": response["answer"],
            "scores": {m: records[m][i]["f1"] for m in RUNS}, "empty": not row["answer_chars"],
            "queries": queries, "selected": selected, "invalid": invalid, "draft": state.get("draft"),
            "candidates": state.get("candidates"), "nodes": row["expansion_nodes"], "depth": row["max_depth_reached"],
            "gold_in_search": snippets_gold, "gold_in_notes": note_gold, "gold_in_children": child_gold, "gold_in_root": root_gold,
            "gold_notes": [n for n in notes if mentions(n["text"])]}
    result = {"runs": RUNS, "overview": overview, "paired": pairs, "formerly_empty": formerly_empty,
        "stats": {k: dict(v) for k, v in stats.items()}, "examples": dict(examples), "cases": cases,
        "selector_input": {key: {"median": median(m[key] for m in menus), "max": max(m[key] for m in menus)}
                           for key in ("chars", "choices")}}
    out = ROOT / "analysis/answer_phase_v4_audit.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k not in {"cases", "examples", "runs"}}, ensure_ascii=False, indent=2))
    print(out)


if __name__ == "__main__":
    main()
