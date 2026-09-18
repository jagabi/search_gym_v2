"""Read saved runs/judge caches only; never call a model or search service."""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[1]
METHODS = ("ragent", "search-o1", "depthsearch")
CASES = (73, 123, 193, 195, 255, 344, 364, 374, 423, 583, 687, 715, 745, 790, 838, 853)


def bucket(score):
    return "zero" if score == 0 else "full" if score == 1 else "partial"


def saved_judge(question, answer, model):
    h = hashlib.sha256()
    for part in ("judge/1", model, "deepsearchqa", question, answer):
        h.update(part.encode("utf-8"))
        h.update(b"\x00")
    key = h.hexdigest()
    path = ROOT / "runs/_cache/judge" / key[:2] / f"{key}.json"
    if not path.exists():
        return None
    j = json.loads(path.read_text(encoding="utf-8"))
    return {"path": str(path.relative_to(ROOT)), **{
        k: j.get(k) for k in ("tp", "fp", "fn", "f1", "explanation", "correctness_details", "excessive_answers", "error")
    }}


def main():
    original = json.loads((ROOT / "analysis/comparison_300_audit.json").read_text(encoding="utf-8"))
    questions = original["questions"]
    matrices = {}
    for m in METHODS[:2]:
        matrices[m] = {
            source: dict(Counter(bucket(q["scores"]["depthsearch"]) for q in questions if bucket(q["scores"][m]) == source))
            for source in ("zero", "partial", "full")
        }
    by_type = {}
    for typ in ("single", "set"):
        qs = [q for q in questions if q["answer_type"] == typ]
        by_type[typ] = {"n": len(qs), "methods": {
            m: {"counts": dict(Counter(bucket(q["scores"][m]) for q in qs)),
                "f1": mean(q["scores"][m] for q in qs)} for m in METHODS
        }}

    selected = [q for q in questions if q["scores"]["depthsearch"] == 0 and max(q["scores"][m] for m in METHODS[:2]) > 0]
    strata = {
        "both_baselines_positive": [q["id"] for q in selected if min(q["scores"][m] for m in METHODS[:2]) > 0],
        "only_ragent_positive": [q["id"] for q in selected if q["scores"]["ragent"] > 0 and q["scores"]["search-o1"] == 0],
        "only_o1_positive": [q["id"] for q in selected if q["scores"]["search-o1"] > 0 and q["scores"]["ragent"] == 0],
    }
    configs = {m: json.loads((ROOT / "runs/test" / original["runs"][m] / "config.json").read_text(encoding="utf-8")) for m in METHODS}
    output_rows = []
    for q in questions:
        if q not in selected and q["id"] not in CASES:
            continue
        row = {k: q[k] for k in ("id", "question", "gold", "scores", "answer_type", "answers")}
        row["judge"] = {m: saved_judge(q["question"], q["answers"][m], configs[m]["judge"]["model"]) for m in METHODS}
        row["details"] = {}
        methods = METHODS if q["id"] in CASES else ("depthsearch",)
        for m in methods:
            p = ROOT / "runs/test" / original["runs"][m] / f"q{q['id']:05d}" / "response.json"
            r = json.loads(p.read_text(encoding="utf-8"))
            drafts = [s for s in r["steps"] if s.get("text", "").strip() and not s.get("tool_calls")]
            row["details"][m] = {
                "response_path": str(p.relative_to(ROOT)),
                **{k: r.get(k) for k in ("searches", "fetch_attempts", "expansion_nodes", "stop_reason", "error", "context_exhausted")},
                "last_no_tool_text": drafts[-1]["text"] if drafts else "",
                "last_no_tool_text_warning": "May be an unfinished plan, not a valid or independently scored draft.",
                "calls": [{"turn": s["turn"], "name": c["name"], "arguments": c["arguments"],
                           "is_error": c.get("is_error"), "refused": c.get("refused")}
                          for s in r["steps"] for c in s.get("tool_calls", [])],
            }
        output_rows.append(row)
    cached_zero = [r["judge"]["depthsearch"] for r in output_rows if r["id"] in {q["id"] for q in selected} and r["judge"]["depthsearch"]]
    result = {
        "scope": "Offline matched-run analysis. No model/search/judge calls. No runtime code changes.",
        "runs": original["runs"], "matrices": matrices, "by_type": by_type,
        "baseline_positive_ds_zero": {"n": len(selected), "types": dict(Counter(q["answer_type"] for q in selected)), "strata": strata},
        "all_three_zero": sum(all(q["scores"][m] == 0 for m in METHODS) for q in questions),
        "partial_f1_means": {m: mean(q["scores"][m] for q in questions if 0 < q["scores"][m] < 1) for m in METHODS},
        "zero_judge_diagnostic": {"cached": len(cached_zero), "fp_zero": sum(j["fp"] == 0 for j in cached_zero),
                                  "warning": "FP=0 is NOT an abstention label: incomplete composite answers and some wrong answers also get FP=0."},
        "case_selection": "Purposeful examples across acquisition, extraction, handoff, completion, finalization, and scoring; not prevalence estimates.",
        "questions": output_rows,
    }
    assert len(questions) == 300
    assert sum(by_type[t]["methods"]["depthsearch"]["counts"].get("zero", 0) for t in by_type) == 151
    assert len(selected) == sum(len(v) for v in strata.values()) == 75
    (ROOT / "analysis/zero_partial_300_audit.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: result[k] for k in ("matrices", "by_type", "baseline_positive_ds_zero", "all_three_zero", "partial_f1_means", "zero_judge_diagnostic")}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
