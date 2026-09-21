"""Offline matched BrowseComp audit; no model, judge, or search requests."""
import json
import math
import re
from collections import Counter
from pathlib import Path
from statistics import mean, median
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parents[1]
RUNS = {
    "ragent": "20260920-2130_ragent_gpt-oss-20b_browsecomp_paper_frozen_v1",
    "search-o1": "20260919-1621_search-o1_gpt-oss-20b_browsecomp_paper_frozen_v1",
    "depthsearch": "20260921-0016_depthsearch_gpt-oss-20b_browsecomp_paper_frozen_v1",
}


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def norm(s):
    return " ".join(re.findall(r"[a-z0-9]+", s.lower()))


def main():
    records, responses = {}, {}
    for m, run in RUNS.items():
        p = ROOT / "runs/test" / run
        rs = [json.loads(s) for s in (p / "records.jsonl").read_text(encoding="utf-8").splitlines()]
        assert len(rs) == len({r["index"] for r in rs}) == 300
        records[m] = {r["index"]: r for r in rs}
        responses[m] = {i: read(p / r["dir"] / "response.json") for i, r in records[m].items()}
    ids = sorted(records["depthsearch"])
    assert all(set(rs) == set(ids) for rs in records.values())
    rows = []
    for i in ids:
        rs = {m: records[m][i] for m in RUNS}
        ds = responses["depthsearch"][i]
        assert all(responses[m][i]["question"] == ds["question"] and
                   responses[m][i]["gold_answer"] == ds["gold_answer"] for m in RUNS)
        calls = [{"turn": s["turn"], **c} for s in ds["steps"] for c in s.get("tool_calls", [])]
        searches = [c for c in calls if c["name"] == "web_search" and not c.get("refused")]
        fetches = [c for c in calls if c["name"] == "web_fetch" and not c.get("refused")]
        drafts = [s for s in ds["steps"] if s.get("text", "").strip() and not s.get("tool_calls")]
        gold = norm(ds["gold_answer"])
        def mentions(text):
            return len(gold) >= 4 and bool(gold) and (" " + gold + " ") in (" " + norm(text) + " ")
        q = {
            "id": i, "category": rs["depthsearch"]["category"],
            "gold": ds["gold_answer"], "question": ds["question"],
            "scores": {m: r["f1"] for m, r in rs.items()},
            "records": rs, "answers": {m: responses[m][i]["answer"] for m in RUNS},
            "ds_queries": [c["arguments"].get("query", "") for c in searches],
            "ds_fetches": [{"turn": c["turn"], "url": c["arguments"].get("url", ""),
                            "error": c.get("is_error"), "reused": "Previously saved notes" in c.get("result", "")}
                           for c in fetches],
            "draft": drafts[-1]["text"] if drafts else "",
            "gold_in_draft": bool(drafts) and mentions(drafts[-1]["text"]),
            "gold_in_final": mentions(ds["answer"]),
            "gold_in_tool_results": any(mentions(c.get("result", "")) for c in calls),
            "gold_in_search_results": any(mentions(c.get("result", "")) for c in searches),
            "gold_in_fetch_results": any(mentions(c.get("result", "")) for c in fetches),
            "first_fetch_searches_before": (sum(c["turn"] < fetches[0]["turn"] for c in searches) if fetches else None),
            "search_error_texts": [c.get("result", "")[:800] for c in searches if c.get("is_error")],
        }
        rows.append(q)
    policy = {}
    for method in RUNS:
        counts = Counter()
        engine_ids = set()
        for i, response in responses[method].items():
            searches = 0
            for step in response["steps"]:
                for call in step.get("tool_calls", []):
                    if call.get("refused"):
                        continue
                    if call["name"] == "web_search":
                        searches += 1
                    elif call["name"] == "web_fetch":
                        counts["main_fetch_calls"] += 1
                        counts["main_fetch_after_10_searches"] += searches >= 10
                        counts["main_fetch_errors"] += bool(call.get("is_error"))
                        counts["main_fetch_reused"] += "Previously saved notes" in str(call.get("result", ""))
                        p = urlparse(call["arguments"].get("url", ""))
                        engine = p.hostname and any(
                            p.hostname == h or p.hostname.endswith("." + h)
                            for h in ("google.com", "bing.com", "duckduckgo.com", "search.yahoo.com")
                        )
                        if engine and any(k in parse_qs(p.query) for k in ("q", "p")):
                            counts["main_search_engine_query_fetches"] += 1
                            counts["main_search_engine_query_fetches_after_10"] += searches >= 10
                            counts["main_search_engine_query_fetch_errors"] += bool(call.get("is_error"))
                            engine_ids.add(i)
        policy[method] = {**counts, "main_search_engine_query_question_ids": sorted(engine_ids)}
    paired = {}
    for other in ("ragent", "search-o1"):
        win = sum(q["scores"]["depthsearch"] > q["scores"][other] for q in rows)
        loss = sum(q["scores"]["depthsearch"] < q["scores"][other] for q in rows)
        n = win + loss
        p = min(1, 2 * sum(math.comb(n, k) for k in range(min(win, loss) + 1)) / 2 ** n) if n else 1
        paired[other] = {"ds_only_correct": win, "baseline_only_correct": loss,
                         "both_correct": sum(q["scores"]["depthsearch"] == q["scores"][other] == 1 for q in rows),
                         "exact_mcnemar_two_sided_p": p}
    loss_rows = [q for q in rows if not q["scores"]["depthsearch"] and max(q["scores"][m] for m in ("ragent", "search-o1"))]
    def group(qs):
        if not qs:
            return {"n": 0}
        return {"n": len(qs), "scores": {m: mean(q["scores"][m] for q in qs) for m in RUNS},
                "ids": [q["id"] for q in qs]}
    result = {"scope": "Saved matched 300 questions; no regrading. Gold substring checks are diagnostic heuristics, not proof of valid source evidence.",
              "runs": RUNS, "paired": paired, "policy_metrics": policy,
              "overall": {m: {"correct": sum(r["f1"] for r in records[m].values()),
                               "empty": sum(not r["answer_chars"] for r in records[m].values()),
                               "judge_errors": [{"id": i, "error": r["judge_error"]} for i, r in records[m].items() if r["judge_error"]],
                               "turn40": sum(r["turns"] == 40 for r in records[m].values()),
                               "mean_calls": mean(r["llm_calls"] for r in records[m].values()),
                               "mean_fetch_attempts": mean(r["fetch_attempts"] for r in records[m].values()),
                               "no_main_fetch": sum(r["fetches"] == 0 for r in records[m].values())} for m in RUNS},
              "ds_loss_union": group(loss_rows),
              "ds_exclusive": group([q for q in rows if q["scores"]["depthsearch"] and not max(q["scores"][m] for m in ("ragent", "search-o1"))]),
              "groups": {"turn40": group([q for q in rows if q["records"]["depthsearch"]["turns"] == 40]),
                         "recursive": group([q for q in rows if q["records"]["depthsearch"]["expansion_nodes"] > 0]),
                         "no_recursive": group([q for q in rows if q["records"]["depthsearch"]["expansion_nodes"] == 0]),
                         "search_failure": group([q for q in rows if q["records"]["depthsearch"]["search_failures"]]),
                         "judge_error": group([q for q in rows if q["records"]["depthsearch"]["judge_error"]]),
                         "no_errors_common": group([q for q in rows if all(not r["judge_error"] and not r["error"] and not r["search_failures"] for r in q["records"].values())]),
                         "first_fetch_after_0_to_3_searches": group([q for q in rows if q["first_fetch_searches_before"] is not None and q["first_fetch_searches_before"] <= 3]),
                         "first_fetch_after_4_to_9_searches": group([q for q in rows if q["first_fetch_searches_before"] is not None and 4 <= q["first_fetch_searches_before"] <= 9]),
                         "first_fetch_after_10_searches": group([q for q in rows if q["first_fetch_searches_before"] == 10]),
                         "never_main_fetch": group([q for q in rows if q["first_fetch_searches_before"] is None])},
              "by_category": {c: group([q for q in rows if q["category"] == c]) for c in sorted({q["category"] for q in rows})},
              "loss_gold_mentions": {k: [q["id"] for q in loss_rows if q[k]] for k in ("gold_in_search_results", "gold_in_fetch_results", "gold_in_draft", "gold_in_final")},
              "questions": rows}
    (ROOT / "analysis/browsecomp_300_audit.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k not in ("questions", "by_category")}, ensure_ascii=True, indent=2))
    print("LOSS CASES")
    for q in loss_rows:
        print(json.dumps({"id": q["id"], "gold": q["gold"], "scores": q["scores"],
                          "searches": q["records"]["depthsearch"]["searches"],
                          "turns": q["records"]["depthsearch"]["turns"],
                          "nodes": q["records"]["depthsearch"]["expansion_nodes"],
                          "mentions": {k: q[k] for k in ("gold_in_search_results", "gold_in_fetch_results", "gold_in_draft", "gold_in_final")},
                          "final": q["answers"]["depthsearch"][:750]}, ensure_ascii=True))


if __name__ == "__main__":
    main()
