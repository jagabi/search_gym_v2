"""Fixed 50-job workload at each concurrency; no retries or server mutations."""
import concurrent.futures
import argparse
import json
from pathlib import Path
import statistics
import time
import uuid

from parallel50 import request, percentile

HERE = Path(__file__).resolve().parent
OUT = HERE / ("concurrency_sweep_" + time.strftime("%Y%m%d-%H%M%S"))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def metrics(response):
    values = {}
    for line in response.get("response", {}).get("raw", "").splitlines():
        if line and not line.startswith("#"):
            key, value = line.rsplit(" ", 1)
            try:
                values[key] = float(value)
            except ValueError:
                pass
    return values


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--concurrency', nargs='+', type=int, default=[4, 8, 16, 32])
    args = parser.parse_args()
    if any(c < 1 for c in args.concurrency):
        parser.error('concurrency must be positive')
    OUT.mkdir()
    bodies = []
    for i in range(5):
        body = json.loads((HERE / "single_question_5k" / f"request_{i:02}.json").read_text(encoding="utf-8"))
        body["model"] = "vllm-sr/d3-mini"
        bodies.append(body)
        save(OUT / f"input_{i:02}.json", body)
    save(OUT / "models.json", request("/v1/models"))
    summaries = []
    print(str(OUT), flush=True)
    for concurrency in args.concurrency:
        folder = OUT / f"c{concurrency:02}"
        folder.mkdir()
        before = request("/metrics")
        save(folder / "metrics_before.json", before)
        started = time.perf_counter()

        def work(i):
            salt = uuid.uuid4().hex
            body = {**bodies[i % 5], "cache_salt": salt, "request_id": "sweep-" + salt}
            sent = time.perf_counter()
            result = request("/v1/systemone", body)
            result.update(index=i, input_case=i % 5, cache_salt=salt,
                          dispatch_s=sent-started, completion_s=time.perf_counter()-started)
            save(folder / f"response_{i:02}.json", result)
            return result

        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as pool:
            futures = [pool.submit(work, i) for i in range(50)]
            for future in concurrent.futures.as_completed(futures):
                results.append(future.result())
                if len(results) % 10 == 0:
                    print(json.dumps({"concurrency": concurrency, "completed": len(results),
                                      "elapsed_s": time.perf_counter()-started}), flush=True)
        elapsed = max(r["completion_s"] for r in results)
        after = request("/metrics")
        save(folder / "metrics_after.json", after)
        b, a = metrics(before), metrics(after)
        names = ["request_success_total", "request_queue_time_seconds_sum", "request_queue_time_seconds_count",
                 "request_inference_time_seconds_sum", "request_inference_time_seconds_count",
                 "iteration_tokens_total_count", "iteration_tokens_total_sum", "prompt_tokens_total",
                 "num_preemptions_total", "prefix_cache_hits_total"]
        delta = {n: sum(v-b.get(k, 0) for k, v in a.items() if k.startswith("vllm:"+n+"{")) for n in names}
        good = [r for r in results if r["status"] == 200 and
                isinstance(r.get("response", {}).get("answers", {}).get("query_answer", {}).get("noul"), (float, int))]
        times = [r["wall_s"] for r in good]
        tokens = sum(r["response"].get("usage", {}).get("input_tokens", 0) for r in good)
        summary = {"concurrency": concurrency, "requests": 50, "successes": len(good),
                   "failures": 50-len(good), "batch_wall_s": elapsed, "input_tokens": tokens,
                   "input_tokens_per_s": tokens/elapsed,
                   "successful_request_latency_s": {"mean": statistics.mean(times), "median": statistics.median(times),
                                                    "p95": percentile(times, .95)} if times else {},
                   "server_metrics_delta": delta,
                   "note": "Closed loop; request latency excludes local executor queue. Total wall includes all 50 jobs. Five inputs repeated ten times; unique cache_salt; one evaluation key; no retries. Concurrency levels run in specified order, one trial each; no server configuration changes."}
        summaries.append(summary)
        save(folder / "summary.json", summary)
        save(OUT / "summary.json", summaries)
        print(json.dumps(summary), flush=True)
        if len(good) != 50:
            print("Stopping sweep after failed requests to avoid overlapping unfinished server work.", flush=True)
            break


if __name__ == "__main__":
    main()
