"""Bounded, structured run inspection. Streams traces; never prints full payloads.

python analysis/inspect_run.py RUN summary
python analysis/inspect_run.py RUN metrics
python analysis/inspect_run.py RUN steps --question 598
python analysis/inspect_run.py RUN evidence --question 598 --terms "HDS|Romanian"
"""
import argparse
import collections
import json
import statistics
import sys
from pathlib import Path


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def events(path):
    with path.open(encoding="utf-8") as stream:
        for line in stream:
            yield json.loads(line)


def union(spans):
    total = 0
    end = 0
    for start, stop in sorted(spans):
        total += max(0, stop - max(start, end))
        end = max(end, stop)
    return total


def describe(values):
    if not values:
        return {}
    vals = sorted(values)
    return {"n": len(vals), "sum_s": round(sum(vals), 2),
            "mean_s": round(statistics.mean(vals), 3),
            "p95_s": round(vals[min(len(vals)-1, int(len(vals)*.95))], 3),
            "max_s": round(vals[-1], 3)}


def metrics(folder):
    requests, llms, batches, searches = {}, {}, {}, {}
    service, spans = collections.defaultdict(list), collections.defaultdict(list)
    counts = collections.Counter()
    active, wave_errors, peak, versions = set(), 0, 0, set()
    last_batch = None
    slow = []
    for e in events(folder / "trace.jsonl"):
        t, event = e["elapsed_ms"] / 1000, e["event"]
        counts[event] += 1
        if event == "jev.request":
            ctx = e["context"]
            key = next(iter(e["body"]["questions"]), "")
            phase = ctx["phase"]
            if phase == "preview":
                phase = "link" if key.startswith("link_") else "page"
            requests[e["request_id"]] = {"phase": phase, "ctx": ctx, "queued": t}
        elif event == "jev.attempt":
            rid = e["request_id"]
            r = requests[rid]
            r.update(start=t, batch=e.get("batch_id"))
            batch = r["batch"]
            if batch != last_batch and active:
                wave_errors += 1
            last_batch = batch
            active.add(rid)
            peak = max(peak, len(active))
            b = batches.setdefault(batch, {"start": t, "end": t, "service": 0, "size": 0})
            b["size"] += 1
        elif event == "jev.response":
            r = requests[e["request_id"]]
            duration = t - r["start"]
            service[r["phase"]].append(duration)
            spans["d3"].append((r["start"], t))
            b = batches[r["batch"]]
            b["end"] = max(b["end"], t)
            b["service"] += duration
            if duration > 30:
                slow.append({"t": round(t, 1), "seconds": round(duration, 1), "phase": r["phase"], "context": r["ctx"]})
        elif event in ("jev.result", "jev.error", "jev.cancelled"):
            active.discard(e["request_id"])
            # Retries reuse the request; only a result/cancellation is terminal.
            if event != "jev.error":
                requests.pop(e["request_id"], None)
        elif event == "fetch.raw":
            seconds = e["duration_ms"] / 1000
            service["fetch"].append(seconds)
            spans["fetch"].append((t-seconds, t))
        elif event == "llm.request":
            llms[e["turn"]] = t
        elif event == "llm.response" and e["turn"] in llms:
            start = llms.pop(e["turn"])
            service["main"].append(t-start)
            spans["main"].append((start, t))
        elif event == "rawtree.start":
            versions.add(e["version"])
            searches[e["search_id"]] = {"query": e["query"], "start_s": round(t, 2), "mode": e.get("config", {}).get("jev_traversal")}
        elif event == "rawtree.traversal_end":
            searches[e["search_id"]].update(traversal_s=round(t-searches[e["search_id"]]["start_s"], 2), end_reason=e.get("reason"), visits=e.get("page_visits"))
        elif event == "rawtree.return":
            searches[e["search_id"]].update(end_s=round(t, 2), duration_s=round(e["duration_s"], 2), stats=e["stats"], sources=[v.get("source") for v in e["returned"]])
    combined = [p for v in spans.values() for p in v]
    wall = read(folder / "response.json")["latency_ms"] / 1000
    return {"wall_s": wall, "versions": sorted(versions), "counts": dict(counts),
            "service": {k: describe(v) for k, v in service.items()},
            "active_s": {k: round(union(v), 2) for k, v in spans.items()},
            "other_s": round(wall-union(combined), 2), "max_http": peak,
            "wave_overlap": wave_errors, "batch_sizes": dict(collections.Counter(b["size"] for b in batches.values())),
            "wave_utilization": round(sum(b["service"] for b in batches.values()) / max(1, sum(4*(b["end"]-b["start"]) for b in batches.values())), 4),
            "slow_requests": slow, "searches": list(searches.values())}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", type=Path)
    parser.add_argument("mode", choices=["summary", "metrics", "steps", "evidence"])
    parser.add_argument("--question", type=int)
    parser.add_argument("--terms", default="")
    parser.add_argument("--limit", type=int, default=12)
    parser.add_argument("--chars", type=int, default=450)
    args = parser.parse_args()
    records = list(events(args.run / "records.jsonl"))
    out = Path("analysis") / ("audit_" + args.run.name.split("_")[0])
    out.mkdir(exist_ok=True)
    for row in records:
        if args.question is not None and row["index"] != args.question:
            continue
        folder = args.run / row["dir"]
        response = read(folder / "response.json")
        if args.mode == "summary":
            print(json.dumps({"id": row["index"], "correct": row["score"], "min": round(row["latency_s"]/60, 1), "searches": row["searches"], "d3": row["reader_stats"]["jev_requests"], "gold": response["gold_answer"]}, ensure_ascii=False))
        elif args.mode == "metrics":
            result = metrics(folder)
            (out / (row["dir"]+".json")).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
            print(json.dumps({"id": row["index"], **{k: result[k] for k in ["wall_s", "active_s", "other_s", "max_http", "wave_overlap", "wave_utilization"]}}, ensure_ascii=False), flush=True)
        elif args.mode == "steps":
            for step in response["steps"][:args.limit]:
                tools = [{"name": t.get("name", t.get("tool")), "arguments": t.get("arguments")} for t in step.get("tool_calls", [])]
                print(json.dumps({"id": row["index"], "turn": step["turn"], "reasoning": step.get("reasoning", "")[:args.chars], "text": step.get("text", "")[:args.chars], "tools": tools}, ensure_ascii=False))
        elif args.mode == "evidence":
            terms = [x.casefold() for x in args.terms.split("|") if x]
            found, counts, samples, seen = [], collections.Counter(), collections.Counter(), set()
            for e in events(folder / "trace.jsonl"):
                if e["event"] not in ("fetch.raw", "rawtree.return", "llm.response"):
                    continue
                content = e.get("content", e.get("text", ""))
                lower = content.casefold()
                for term in terms:
                    pos = lower.find(term)
                    if pos < 0:
                        continue
                    key = (e["event"], term)
                    counts["/".join(key)] += 1
                    identity = (*key, e.get("url"), e.get("search_id"))
                    if identity in seen or samples[key] >= args.limit:
                        continue
                    seen.add(identity)
                    samples[key] += 1
                    found.append({"event": e["event"], "minute": round(e["elapsed_ms"]/60000, 2), "term": term, "url": e.get("url"), "search_id": e.get("search_id"), "offset": pos, "excerpt": content[max(0, pos-100):pos+args.chars]})
            result = {"counts": dict(counts), "matches": found}
            (out / (row["dir"]+"_evidence.json")).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
            print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
