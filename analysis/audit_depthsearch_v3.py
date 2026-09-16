"""Read saved runs only: no model/search/judge calls, no modification of runs."""
import argparse
import collections
import json
import random
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def records(run):
    return {r["index"]: r for line in (run / "records.jsonl").read_text(encoding="utf-8").splitlines()
            if line.strip() for r in [json.loads(line)]}


def score(row):
    return float(row.get("f1") or 0)


def compare(current, previous):
    pairs = [(i, score(current[i]) - score(previous[i])) for i in sorted(current.keys() & previous.keys())]
    deltas = [v for _, v in pairs]
    rng = random.Random(47)
    boots = sorted(statistics.mean(rng.choices(deltas, k=len(deltas))) for _ in range(10000))
    return {"n": len(pairs), "mean_delta": statistics.mean(deltas),
            "paired_bootstrap_95pct": [boots[250], boots[9749]],
            "wins": [[i, round(d, 4)] for i, d in pairs if d > 1e-6],
            "losses": [[i, round(d, 4)] for i, d in pairs if d < -1e-6],
            "ties": sum(abs(d) <= 1e-6 for _, d in pairs)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("run", type=Path)
    parser.add_argument("--out", type=Path, default=ROOT / "analysis/depthsearch_v3_audit.json")
    args = parser.parse_args()
    current = records(args.run)
    report = {"run": str(args.run), "summary": read(args.run / "summary.json"), "comparisons": {}, "questions": []}
    for label, name in {
        "v2": "20260915-1602_depthsearch_gpt-oss-20b_deepsearchqa_evidence-v2-fix",
        "v1": "20260915-1431_depthsearch_gpt-oss-20b_deepsearchqa_evidence-v1",
        "ragent": "20260912-2055_ragent_gpt-oss-20b_deepsearchqa_f1",
    }.items():
        report["comparisons"][label] = compare(current, records(ROOT / "runs/test" / name))
    counts = collections.defaultdict(collections.Counter)
    tokens = collections.defaultdict(list)
    for idx, row in sorted(current.items()):
        folder = args.run / row["dir"]
        response = read(folder / "response.json")
        q = {"index": idx, "f1": score(row), "question": response["question"], "gold": response.get("gold_answer"),
             "answer": response.get("answer"), "stop": row.get("stop_reason"), "searches": row["searches"],
             "nodes": row["expansion_nodes"], "turns": row["turns"], "calls": row["llm_calls"],
             "input_tokens": row["input_tokens"], "queries": [], "invalid": [], "document_ops": [],
             "state_ops": [], "fetch_failures": [], "errors": [], "reader_starts": [], "drafts": []}
        for line in (folder / "trace.jsonl").read_text(encoding="utf-8").splitlines():
            ev = json.loads(line)
            kind = ev["event"]
            counts["events"][kind] += 1
            if kind == "tool.call":
                counts["main_tools"][ev["tool"]] += 1
                if ev["tool"] == "web_search":
                    q["queries"].append(ev["arguments"].get("query"))
            elif kind == "tool.invalid_arguments":
                q["invalid"].append(ev)
                counts["invalid"][ev["tool"] + ": " + ev["error"]] += 1
            elif kind == "llm.response":
                if not ev.get("tool_calls"):
                    q["drafts"].append({k: ev.get(k) for k in ("turn", "text", "raw_text", "finish_reason")})
            elif kind == "document.read":
                raw = ev.get("arguments", {})
                if isinstance(raw, str):
                    try:
                        raw = json.loads(raw)
                    except ValueError:
                        raw = {"raw": raw}
                try:
                    output = json.loads(ev["output"])
                except ValueError:
                    output = {"message": ev["output"]}
                if not isinstance(output, dict):
                    output = {"unexpected": output}
                item = {"phase": ev.get("phase"), "args": raw, "error": output.get("error"),
                        "total": output.get("total"), "output_preview": ev["output"][:450]}
                q["document_ops"].append(item)
                counts["document_actions"][str(raw.get("action"))] += 1
                counts["document_phases"][ev.get("phase")] += 1
                if output.get("error"):
                    counts["document_errors"][str(output["error"])] += 1
                if output.get("total") == 0:
                    counts["zero_match_actions"][str(raw.get("action"))] += 1
            elif kind == "research.state":
                q["state_ops"].append(ev)
                counts["state_actions"][ev["arguments"].get("action")] += 1
            elif kind == "fetch.source":
                counts["retrievals"][ev.get("retrieval")] += 1
                if ev.get("is_error") or ev.get("retrieval_note"):
                    q["fetch_failures"].append(ev)
            elif kind in {"run.error", "run.salvage_failed"}:
                q["errors"].append(ev)
            elif kind == "explorer.start":
                item = {k: ev.get(k) for k in ("depth", "can_expand", "openable_links", "budget", "documents")}
                q["reader_starts"].append(item)
                counts["reader_expandability"][f'd{ev["depth"]} expand={ev["can_expand"]}'] += 1
            elif kind == "explorer.response":
                phase = ev.get("phase", "unknown")
                tokens[phase].append((ev.get("prompt_tokens", 0), ev.get("completion_tokens", 0)))
            elif kind == "research.final_state":
                q["final_state"] = {k: ev.get(k) for k in ("candidates", "unknown_cells", "pending_total", "local_reads")}
        report["questions"].append(q)
    report["counts"] = {k: dict(v) for k, v in counts.items()}
    report["reader_tokens"] = {k: {"calls": len(v), "input": sum(a for a, _ in v),
                                    "output": sum(b for _, b in v)} for k, v in tokens.items()}
    args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("comparisons", "counts", "reader_tokens")}, ensure_ascii=False, indent=2))
    print("PER QUESTION: id f1 search nodes calls docops stateops stop")
    for q in report["questions"]:
        print(q["index"], round(q["f1"], 3), q["searches"], q["nodes"], q["calls"],
              len(q["document_ops"]), len(q["state_ops"]), q["stop"])


if __name__ == "__main__":
    main()
