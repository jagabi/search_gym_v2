"""Why does the main model (not) fetch after a search?

For runs where the main model holds web_fetch, classify each executed search by
what the main model did on the next turn (fetch / search again / answer), and relate
that to (a) whether the gold answer string already appears in the returned
titles/snippets (post-hoc only; gold never reaches the model) and (b) how the next
turn's reasoning talks about the results.

    python analysis/experiments/audit_fetch_decisions.py RUN_DIR [RUN_DIR ...] --out OUT.json
"""

import argparse
import collections
import glob
import json
import os
import re

DISMISS = re.compile(
    r"not (?:very |that |really )?(?:relevant|helpful|useful|related)|irrelevant|unrelated|"
    r"nothing (?:relevant|useful|helpful)|no (?:relevant|useful|helpful|obvious|clear)\b|"
    r"(?:doesn't|does not|don't|do not) (?:help|seem|appear|show|mention|match)|"
    r"none of (?:these|them|the results)|no luck|no results|not (?:found|find)|"
    r"(?:results|they) (?:are|seem) (?:generic|random|spam)", re.I)
LEAD = re.compile(
    r"https?://|\b(?:open|fetch|visit|read|look at|check) (?:the |this |that )?(?:page|article|link|site|result|wiki)|"
    r"promising|could be (?:the|our) (?:answer|candidate)|candidate", re.I)


def norm(text):
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", " ", str(text).lower())).strip()


def gold_strings(item):
    parts = item.get("answer_parts") or []
    out = [item.get("answer") or ""] + [p if isinstance(p, str) else json.dumps(p) for p in parts]
    return [g for g in (norm(x) for x in out) if len(g) >= 4]


def result_text(result):
    if isinstance(result, dict):
        rows = result.get("organic") or []
        return " ".join(f"{r.get('title', '')} {r.get('snippet', '')}" for r in rows)
    return str(result or "")


def next_action(step):
    names = [c["name"] for c in step.get("tool_calls") or [] if not c.get("refused")]
    if "web_fetch" in names:
        return "fetch"
    if "web_search" in names:
        return "search"
    return "answer" if (step.get("text") or "").strip() else "other"


def audit(run, items):
    searches = []
    first_fetch_turns, fetches_after_exhaustion, total_fetch = [], 0, 0
    for path in sorted(glob.glob(run + "/q*/response.json")):
        qid = int(os.path.basename(os.path.dirname(path))[1:])
        response = json.load(open(path, encoding="utf-8"))
        steps = response.get("steps") or []
        gold = gold_strings(items.get(qid, {}))
        done_searches = 0
        first = None
        for k, step in enumerate(steps):
            for call in step.get("tool_calls") or []:
                if call.get("refused"):
                    continue
                if call["name"] == "web_fetch":
                    total_fetch += 1
                    fetches_after_exhaustion += done_searches >= 10
                    first = first or step["turn"]
                if call["name"] != "web_search" or call.get("is_error"):
                    continue
                done_searches += 1
                if k + 1 >= len(steps):
                    continue
                nxt = steps[k + 1]
                text = norm(result_text(call.get("result")))
                reasoning = nxt.get("reasoning") or ""
                searches.append({
                    "qid": qid, "turn": step["turn"],
                    "action": next_action(nxt),
                    "gold_in_results": any(g in text for g in gold) if gold else None,
                    "dismiss": bool(DISMISS.search(reasoning)),
                    "lead": bool(LEAD.search(reasoning)),
                })
        first_fetch_turns.append(first)
    by_action = collections.Counter(s["action"] for s in searches)

    def rate(rows, key="action", value="fetch"):
        return round(sum(r[key] == value for r in rows) / len(rows), 3) if rows else None

    gold_rows = [s for s in searches if s["gold_in_results"] is not None]
    no_fetch = [s for s in searches if s["action"] == "search"]
    fetched = [s for s in searches if s["action"] == "fetch"]
    return {
        "run": os.path.basename(run),
        "searches": len(searches),
        "next_action": dict(by_action),
        "p_fetch_next": rate(searches),
        "p_fetch_next_if_gold_in_results": rate([s for s in gold_rows if s["gold_in_results"]]),
        "p_fetch_next_if_gold_absent": rate([s for s in gold_rows if not s["gold_in_results"]]),
        "gold_in_results_rate": rate(gold_rows, "gold_in_results", True),
        "search_again": {
            "n": len(no_fetch),
            "reasoning_dismisses_results": rate(no_fetch, "dismiss", True),
            "reasoning_mentions_lead": rate(no_fetch, "lead", True),
            "gold_in_results": rate([s for s in no_fetch if s["gold_in_results"] is not None], "gold_in_results", True),
        },
        "fetched_next": {
            "n": len(fetched),
            "reasoning_dismisses_results": rate(fetched, "dismiss", True),
            "reasoning_mentions_lead": rate(fetched, "lead", True),
        },
        "questions_without_fetch": sum(t is None for t in first_fetch_turns),
        "median_first_fetch_turn": sorted(t for t in first_fetch_turns if t)[len([t for t in first_fetch_turns if t]) // 2]
        if any(first_fetch_turns) else None,
        "fetches_after_10_searches": f"{fetches_after_exhaustion}/{total_fetch}",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("runs", nargs="+")
    parser.add_argument("--out")
    args = parser.parse_args()
    report = []
    for run in args.runs:
        config = json.load(open(run + "/config.json", encoding="utf-8"))
        # Saved paths may come from another machine; keep data/<benchmark>/<file>.
        parts = str(config.get("dataset") or "").replace("\\", "/").split("/")
        dataset = os.path.join(*parts[-3:]) if len(parts) >= 3 and parts[-3] == "data" else ""
        if not os.path.exists(dataset):
            dataset = ""
        items = {it["index"]: it for it in json.load(open(dataset, encoding="utf-8"))} if dataset else {}
        row = audit(run, items)
        report.append(row)
        print(json.dumps(row, ensure_ascii=False, indent=1))
    if args.out:
        json.dump(report, open(args.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
