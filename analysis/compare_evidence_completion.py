"""Compare four saved runs, offline; no model/search/judge calls or runtime edits."""
import json
import random
from collections import Counter
from pathlib import Path
from statistics import mean, median, quantiles

ROOT = Path(__file__).resolve().parents[1]
METHODS = ("ragent", "search-o1", "ds_old", "ds_new")


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def bucket(f1):
    return "zero" if f1 == 0 else "full" if f1 == 1 else "partial"


def describe(rows, method):
    records = [q["records"][method] for q in rows]
    scores = [r["f1"] for r in records]
    return {
        "n": len(rows), "f1": mean(scores),
        **{b: sum(bucket(s) == b for s in scores) for b in ("zero", "partial", "full")},
        "precision": mean(r["precision"] for r in records),
        "recall": mean(r["recall"] for r in records),
        "empty": sum(r["answer_chars"] == 0 for r in records),
        "judge_errors": sum(bool(r["judge_error"]) for r in records),
        "run_errors": sum(bool(r["error"]) for r in records),
        "searches_mean": mean(r["searches"] for r in records),
        "fetch_attempts_mean": mean(r["fetch_attempts"] for r in records),
        "expansion_nodes_mean": mean(r["expansion_nodes"] for r in records),
        "llm_calls_mean": mean(r["llm_calls"] for r in records),
        "input_tokens_total": sum(r["input_tokens"] for r in records),
        "output_tokens_total": sum(r["output_tokens"] for r in records),
        "latency_s_median": median(r["latency_s"] for r in records),
        "turns_mean": mean(r["turns"] for r in records),
        "turns_40": sum(r["turns"] == 40 for r in records),
        "stop_reasons": dict(Counter(r["stop_reason"] for r in records)),
    }


def paired(rows, other):
    d = [q["scores"]["ds_new"] - q["scores"][other] for q in rows]
    rng = random.Random(20260919)
    samples = [sum(rng.choices(d, k=len(d))) / len(d) for _ in range(20000)]
    percentiles = quantiles(samples, n=1000, method="inclusive")
    return {"n": len(d), "mean_delta": mean(d),
            "wins": sum(v > 1e-9 for v in d), "ties": sum(abs(v) <= 1e-9 for v in d),
            "losses": sum(v < -1e-9 for v in d),
            "paired_question_bootstrap_95ci": [percentiles[24], percentiles[974]]}


def main():
    old = read(ROOT / "analysis/comparison_300_audit.json")
    runs = {"ragent": old["runs"]["ragent"], "search-o1": old["runs"]["search-o1"],
            "ds_old": old["runs"]["depthsearch"],
            "ds_new": "20260919-0052_depthsearch_gpt-oss-20b_deepsearchqa_ds_evidence_completion"}
    records, responses, configs = {}, {}, {}
    for m, name in runs.items():
        path = ROOT / "runs/test" / name
        lines = [json.loads(s) for s in (path / "records.jsonl").read_text(encoding="utf-8").splitlines()]
        assert len(lines) == 300 and len({r["index"] for r in lines}) == 300
        records[m] = {r["index"]: r for r in lines}
        responses[m] = {i: read(path / r["dir"] / "response.json") for i, r in records[m].items()}
        configs[m] = read(path / "config.json")
    expected = {q["id"] for q in old["questions"]}
    assert all(set(records[m]) == expected for m in METHODS)
    rows = []
    for q in old["questions"]:
        i = q["id"]
        for m in METHODS:
            assert responses[m][i]["question"] == q["question"]
            assert responses[m][i]["gold_answer"] == q["gold"]
            assert records[m][i]["category"] == q["category"]
        rows.append({k: q[k] for k in ("id", "category", "answer_type", "answer_count")}
                    | {"scores": {m: records[m][i]["f1"] for m in METHODS},
                       "records": {m: records[m][i] for m in METHODS}})
    overall = {m: describe(rows, m) for m in METHODS}
    by_type = {t: {m: describe([q for q in rows if q["answer_type"] == t], m) for m in METHODS}
               for t in ("single", "set")}
    by_category = {c: {"n": sum(q["category"] == c for q in rows),
                       **{m: mean(q["scores"][m] for q in rows if q["category"] == c) for m in METHODS}}
                   for c in sorted({q["category"] for q in rows})}
    transitions = {m: {a: {b: sum(bucket(q["scores"][m]) == a and bucket(q["scores"]["ds_new"]) == b for q in rows)
                            for b in ("zero", "partial", "full")}
                        for a in ("zero", "partial", "full")}
                   for m in METHODS[:-1]}
    target = [q for q in rows if q["scores"]["ds_old"] == 0 and max(q["scores"][m] for m in METHODS[:2]) > 0]
    empty = [q for q in rows if q["records"]["ds_new"]["answer_chars"] == 0]
    empty_traces = []
    for q in empty:
        path = ROOT / "runs/test" / runs["ds_new"] / q["records"]["ds_new"]["dir"] / "trace.jsonl"
        events = [json.loads(s) for s in path.read_text(encoding="utf-8").splitlines()]
        finals = [e for e in events if e["event"] == "run.final_response"]
        empty_traces.append({"id": q["id"], "finalization_attempts": len(finals),
                             "raw_outputs_all_empty": all(not e.get("raw_text") for e in finals),
                             "finish_reasons": [e.get("finish_reason") for e in finals],
                             "salvage_errors": [e.get("error") for e in events if e["event"] == "run.salvage_failed"]})
    examples = [q for q in rows if q["id"] in (17, 73, 123, 158, 193, 255, 344, 364, 374, 443, 583, 687, 715, 745, 838)]
    result = {
        "runs": runs, "matched_ids_questions_gold_categories": True,
        "scope": "All 300 matched questions; empty responses count as zero. Saved scores, no regrading.",
        "uncertainty": "20,000 paired question bootstrap samples, seed 20260919. CIs cover question sampling only, not run/search/judge variability; same investigated dataset, not held-out confirmation.",
        "configs": {m: {"model": configs[m]["model"], "judge": configs[m]["judge"],
                         "searches": configs[m]["agent"]["max_searches"],
                         "results": configs[m]["agent"]["search_results"],
                         "endpoint": configs[m]["agent"]["base_url"]} for m in METHODS},
        "overall": overall, "by_type": by_type, "by_category": by_category,
        "paired": {m: paired(rows, m) for m in METHODS[:-1]},
        "paired_by_type": {t: paired([q for q in rows if q["answer_type"] == t], "ds_old") for t in by_type},
        "transitions_to_new": transitions,
        "old_baseline_positive_ds_zero": {"n": len(target), "new": describe(target, "ds_new")},
        "new_baseline_positive_ds_zero": sum(q["scores"]["ds_new"] == 0 and max(q["scores"][m] for m in METHODS[:2]) > 0 for q in rows),
        "empty_new": [{k: v for k, v in q.items() if k != "records"} |
                      {"stop": q["records"]["ds_new"]["stop_reason"],
                       "turns": q["records"]["ds_new"]["turns"],
                       "judge_error": q["records"]["ds_new"]["judge_error"]} for q in empty],
        "empty_new_scores_old_total": sum(q["scores"]["ds_old"] for q in empty),
        "empty_trace_diagnostics": empty_traces,
        "prior_cases": [{k: v for k, v in q.items() if k != "records"} for q in examples],
        "questions": rows,
    }
    dest = ROOT / "analysis/evidence_completion_comparison.json"
    dest.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k not in ("questions", "configs", "runs")}, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
