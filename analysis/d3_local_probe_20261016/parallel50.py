"""50 simultaneous uncached decision requests against the restarted vLLM API."""
import concurrent.futures
import json
import math
from pathlib import Path
import statistics
import threading
import time
import urllib.error
import urllib.request
import uuid

HERE = Path(__file__).resolve().parent
OUT = HERE / ("parallel50_vllm_" + time.strftime("%Y%m%d-%H%M%S"))
BASE = "http://100.89.209.104:8101"
N = 50


def save(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def request(path, body=None):
    data = json.dumps(body, ensure_ascii=False).encode() if body is not None else None
    req = urllib.request.Request(BASE + path, data=data, headers={"Content-Type": "application/json"})
    started = time.perf_counter()
    try:
        with urllib.request.build_opener(urllib.request.ProxyHandler({})).open(req, timeout=180) as response:
            raw = response.read().decode()
            status, headers = response.status, dict(response.headers)
    except urllib.error.HTTPError as exc:
        raw, status, headers = exc.read().decode(), exc.code, dict(exc.headers)
    except Exception as exc:
        return {"status": None, "error": repr(exc), "wall_s": time.perf_counter() - started}
    elapsed = time.perf_counter() - started
    try:
        parsed = json.loads(raw)
    except ValueError:
        parsed = {"raw": raw}
    return {"status": status, "wall_s": elapsed, "headers": headers, "response": parsed}


def percentile(values, fraction):
    values = sorted(values)
    position = (len(values) - 1) * fraction
    low = math.floor(position)
    high = math.ceil(position)
    return values[low] + (values[high] - values[low]) * (position - low)


def main():
    OUT.mkdir()
    save("models.json", request("/v1/models"))
    save("health_before.json", request("/health"))
    save("metrics_before.json", request("/metrics"))
    bodies = []
    for i in range(5):
        body = json.loads((HERE / "single_question_5k" / f"request_{i:02}.json").read_text(encoding="utf-8"))
        body["model"] = "vllm-sr/d3-mini"
        bodies.append(body)
        save(f"input_{i:02}.json", body)
    barrier = threading.Barrier(N + 1, timeout=60)
    start = [None]

    def work(i):
        salt = uuid.uuid4().hex
        body = {**bodies[i % 5], "cache_salt": salt, "request_id": "parallel50-" + salt}
        barrier.wait()
        sent = time.perf_counter()
        result = request("/v1/systemone", body)
        finished = time.perf_counter()
        result.update(index=i, input_case=i % 5, cache_salt=salt,
                      dispatch_s=sent - start[0], completion_s=finished - start[0])
        save(f"response_{i:02}.json", result)
        return result

    print("Launching 50 requests; output: " + str(OUT), flush=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=N) as pool:
        futures = [pool.submit(work, i) for i in range(N)]
        start[0] = time.perf_counter()
        barrier.wait()
        results = []
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            results.append(result)
            if len(results) % 5 == 0 or result["status"] != 200:
                print(json.dumps({"completed": len(results), "index": result["index"],
                                  "status": result["status"], "wall_s": result["wall_s"],
                                  "elapsed_s": result["completion_s"]}), flush=True)
    results.sort(key=lambda r: r["index"])
    elapsed = max(r["completion_s"] for r in results)
    good = [r for r in results if r["status"] == 200 and
            isinstance(r.get("response", {}).get("answers", {}).get("query_answer", {}).get("noul"), (int, float))]
    times = [r["wall_s"] for r in results]
    tokens = [r["response"].get("usage", {}).get("input_tokens", 0) for r in good]
    summary = {"endpoint": BASE + "/v1/systemone", "requests": N, "concurrency": N,
               "successes": len(good), "failures": N - len(good), "distinct_source_inputs": 5,
               "repetitions_per_source": 10, "cache_policy": "unique cache_salt per request",
               "evaluation_keys_per_request": 1, "retries": 0,
               "batch_wall_s": elapsed, "requests_per_s": len(good) / elapsed,
               "dispatch_span_s": max(r["dispatch_s"] for r in results) - min(r["dispatch_s"] for r in results),
               "latency_s": {"mean": statistics.mean(times), "median": statistics.median(times),
                             "p95": percentile(times, .95), "min": min(times), "max": max(times)},
               "input_tokens": {"total": sum(tokens), "mean": statistics.mean(tokens) if tokens else None,
                                "min": min(tokens, default=None), "max": max(tokens, default=None)},
               "input_tokens_per_s": sum(tokens) / elapsed,
               "score_ranges_by_source": {},
               "note": "One burst, previously smoke-tested server; not a cold-start or sustained-load benchmark. Five real saved texts repeated with isolated prefix caches. No answer-quality evaluation."}
    for i in range(5):
        scores = [r["response"]["answers"]["query_answer"]["noul"] for r in good if r["input_case"] == i]
        summary["score_ranges_by_source"][str(i)] = [min(scores), max(scores)] if scores else []
    save("summary.json", summary)
    save("metrics_after.json", request("/metrics"))
    save("health_after.json", request("/health"))
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
