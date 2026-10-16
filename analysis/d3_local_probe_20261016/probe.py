"""Read-only d3-mini API probe: five sequential + five concurrent requests.

Uses saved benchmark pages; no new fetches or changes to the agent pipeline.
Token lengths are estimates on preparation and measured from server usage.
"""
import concurrent.futures
import json
import math
from pathlib import Path
import re
import statistics
import sys
import time
import urllib.error
import urllib.request

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE = "http://100.89.209.104:8101"
RUN = ROOT / "runs/test/20261013-1807_jevtree_gpt-oss-20b_browsecomp_v66_query_split_content10"


def save(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def request(path, body=None):
    data = None if body is None else json.dumps(body, ensure_ascii=False).encode()
    req = urllib.request.Request(BASE + path, data=data, headers={"Content-Type": "application/json"})
    start = time.perf_counter()
    try:
        with urllib.request.build_opener(urllib.request.ProxyHandler({})).open(req, timeout=180) as response:
            raw = response.read().decode()
            status, headers = response.status, dict(response.headers)
    except urllib.error.HTTPError as exc:
        raw, status, headers = exc.read().decode(), exc.code, dict(exc.headers)
    elapsed = time.perf_counter() - start
    try:
        parsed = json.loads(raw)
    except ValueError:
        parsed = {"raw": raw}
    timing = next((v for k, v in headers.items() if k.lower() == "server-timing"), "")
    timings = {m.group(1): float(m.group(2)) for m in re.finditer(r"([\w-]+);dur=([\d.]+)", timing)}
    return {"status": status, "wall_s": elapsed, "server_ms": timings, "headers": headers, "response": parsed}


def estimated_prefix(text, budget):
    # No local model tokenizer is installed. This heuristic is NOT reported as
    # a measured token count: each result stores the server's actual usage.
    total, end = 0, 0
    for match in re.finditer(r"\w+|[^\w\s]", text):
        cost = max(1, math.ceil(len(match.group()) / 5))
        if total + cost > budget:
            break
        total += cost
        end = match.end()
    return text[:end], total


def source(q):
    with (RUN / f"q{q:05}/trace.jsonl").open(encoding="utf-8") as stream:
        for line in stream:
            event = json.loads(line)
            if event["event"] != "jevtree.reader_request":
                continue
            state = json.loads(event["messages"][1]["content"])
            if len(state["page_text"]) >= 25000:
                return state
    raise RuntimeError(f"No sufficiently long saved page for {q}")


def run_case(phase, index, body):
    result = request("/v1/decisions", body)
    result.update(phase=phase, case=index, page_chars=len(body["state"]["page_text"]))
    save(f"{phase}_{index:02}_response.json", result)
    print(json.dumps({k: result[k] for k in ("phase", "case", "status", "wall_s", "server_ms")}
                     | {"usage": result["response"].get("usage"), "answers": result["response"].get("answers")}), flush=True)
    return result


def describe(results):
    times = [r["wall_s"] for r in results]
    tokens = [r["response"].get("usage", {}).get("input_tokens") for r in results]
    return {"n": len(results), "successes": sum(r["status"] == 200 for r in results),
            "wall_mean_s": statistics.mean(times), "wall_median_s": statistics.median(times),
            "wall_min_s": min(times), "wall_max_s": max(times), "input_tokens": tokens}


def main():
    global HERE
    single = "--single" in sys.argv
    if single:
        HERE = HERE / "single_question_5k"
        HERE.mkdir(exist_ok=True)
    save("health.json", request("/health"))
    save("models.json", request("/v1/models"))
    bodies, sequential = [], []
    # Correct the size estimate using preceding measurements, without adding
    # calibration inference calls. Concurrent requests repeat the SAME bodies.
    scale = 1.0
    for i, q in enumerate([40, 117, 326, 366, 516]):
        state = source(q)
        page, estimated = estimated_prefix(state["page_text"], int(4700 * scale))
        state["page_text"] = page
        body = {"model": "d3-mini", "state": state, "questions": {
            "query_answer": {"type": "noul",
                "instructions": "Does page_text contain source facts that answer search_query, even if question remains unresolved?",
                "criteria": {"true": "The current query is answered by explicit source facts.",
                             "false": "No query answer; mere mention or speculation."}},
            "direct_answer": {"type": "noul", "instructions": "Does page_text explicitly answer question?",
                "criteria": {"true": "The original question's answer is explicitly supported.",
                             "false": "The original question's answer is not supported."}}
        }}
        if single:
            del body["questions"]["direct_answer"]
        save(f"request_{i:02}.json", body)
        bodies.append(body)
        result = run_case("sequential", i, body)
        sequential.append(result)
        if result["status"] != 200:
            raise RuntimeError("Stop after failed decision request; inspect saved response")
        actual = result["response"].get("usage", {}).get("input_tokens", 0)
        if actual > 300:
            scale = estimated / max(1, actual - 300)
    start = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        parallel = list(pool.map(lambda item: run_case("parallel5", *item), enumerate(bodies)))
    parallel_wall = time.perf_counter() - start
    summary = {"endpoint": BASE + "/v1/decisions", "model": "d3-mini",
               "questions_per_request": 1 if single else 2, "distinct_inputs": 5, "measured_requests": 10,
               "note": "Approximate 5k target; actual server input_tokens reported. Identical bodies reused across phases. No model tokenizer locally. Short smoke request ran before measurements. No chunk localization/quality evaluation.",
               "sequential": describe(sequential), "parallel5": describe(parallel),
               "sequential_wall_sum_s": sum(r["wall_s"] for r in sequential),
               "parallel5_batch_wall_s": parallel_wall,
               "answers_repeat_exactly": [a["response"].get("answers") == b["response"].get("answers")
                                          for a, b in zip(sequential, parallel)]}
    save("summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
