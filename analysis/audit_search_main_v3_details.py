"""Detailed saved-trace diagnosis; no API calls."""
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from searchgym.research_state import is_search_endpoint
from audit_search_main_v3 import ROOT, RUNS, read

base = ROOT / "runs/test" / RUNS["ds_new"]
audit = read(ROOT / "analysis/search_main_v3_audit.json")
counts, examples, cases = Counter(), defaultdict(list), {}
focus = {8, 52, 326, 334, 510, 898, 972, 975, 1237, 492, 1066}
root_distribution, empty_stats = Counter(), Counter()
root_max = []
for record_line in (base / "records.jsonl").read_text(encoding="utf-8").splitlines():
    row = json.loads(record_line)
    i, empty = row["index"], not row["answer_chars"]
    response = read(base / row["dir"] / "response.json")
    root_distribution[row.get("auto_fetches", 0)] += 1
    if row.get("auto_fetches", 0) >= 8:
        root_max.append({"id": i, "entries": row["auto_fetches"], "nodes": row["expansion_nodes"], "budget": response.get("budget")})
    if empty:
        empty_stats["n"] += 1
        empty_stats["searches=" + str(row["searches"])] += 1
        empty_stats["draft_nonempty"] += bool(response.get("research_state", {}).get("draft", {}).get("text"))
        empty_stats["any_baseline_correct"] += any(audit["examples"]["empty_questions"][j]["scores"][m] == 1
            for j in range(len(audit["examples"]["empty_questions"])) if audit["examples"]["empty_questions"][j]["id"] == i
            for m in ("ragent", "search-o1"))
    if i in focus:
        cases[i] = {"question": response["question"], "gold": response.get("gold_answer"), "answer": response["answer"],
            "draft": response.get("research_state", {}).get("draft"), "f1": row["f1"], "searches": [], "entries": [], "invalids": []}
    request, tools = {}, []
    for line in (base / row["dir"] / "trace.jsonl").open(encoding="utf-8"):
        e = json.loads(line)
        kind = e.get("event")
        if kind == "llm.request":
            tools = e.get("available_tools", [])
        elif kind == "llm.response":
            if not e.get("raw_text") and not e.get("tool_calls") and e.get("finish_reason") == "stop":
                counts["main_empty:" + ("with_tools" if tools else "no_tools")] += 1
            counts["main_requests:" + ("with_tools" if tools else "no_tools")] += 1
        elif kind == "control.request":
            request = json.loads(e["messages"][-1]["content"])
        elif kind == "control.response":
            if e.get("mode") == "select" and e.get("decision") == "invalid_tool_call":
                calls = e.get("tool_calls", [])
                if len(calls) != 1:
                    continue
                try:
                    url = json.loads(calls[0]["arguments"])["url"]
                except (ValueError, TypeError, KeyError):
                    continue
                sources = list({s["id"]: s for s in (
                    request.get("working_state", {}).get("sources", []) + request.get("sources", []))}.values())
                known = next((s for s in sources if s["url"] == url), None)
                by_id = next((s for s in sources if s["id"] == url), None)
                try:
                    engine = is_search_endpoint(url)
                except (ValueError, TypeError):
                    engine = False
                if engine:
                    reason = "search_engine_url"
                elif known:
                    reason = "known_" + known["status"]
                elif by_id:
                    reason = "source_id_in_url"
                elif any(s["url"].lower().rstrip("/") == url.lower().rstrip("/") for s in sources):
                    reason = "case_or_trailing_slash_variant"
                else:
                    reason = "other_unlisted_url"
                counts[reason] += 1
                if len(examples[reason]) < 5:
                    examples[reason].append({"id": i, "url": url, "reasoning_tail": (e.get("reasoning") or "")[-450:]})
                if i in focus:
                    cases[i]["invalids"].append({"reason": reason, "url": url})
            elif e.get("mode") == "update-only" and not e.get("valid") and e.get("text"):
                if len(examples["update_invalid_text"]) < 3:
                    examples["update_invalid_text"].append({"id": i, "text": e["text"][:1800], "finish_reason": e.get("finish_reason")})
        elif kind == "tool.call" and e.get("tool") == "web_search" and i in focus:
            cases[i]["searches"].append(e.get("arguments"))
        elif kind == "search.selected_entry" and i in focus:
            cases[i]["entries"].append({"turn": e.get("turn"), "url": e.get("url")})
    if empty and len(examples["empty_last_reasoning"]) < 3:
        examples["empty_last_reasoning"].append({"id": i, "text": response["steps"][-1].get("reasoning", "")[-1800:]})
result = {"counts": dict(counts), "examples": dict(examples), "empty_stats": dict(empty_stats),
    "root_distribution": dict(root_distribution), "root_examples": root_max[:6], "cases": cases}
out = ROOT / "analysis/search_main_v3_details.json"
out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps({k: v for k, v in result.items() if k not in {"cases", "examples"}}, ensure_ascii=False, indent=2))
print(out)
