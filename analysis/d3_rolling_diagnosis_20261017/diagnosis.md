# Rolling RawTree latency diagnosis — 2026-10-17

Run: `runs/test/20261017-1720_jevtree_gpt-oss-20b_browsecomp_raw_browser_rolling10`.
Observed q40 trace ends in cancellation at 1,236.01 seconds, in the first search.
No completed search or final answer is recorded.

## Observed execution

- Version 6 rolling scheduler is active. Maximum concurrent decision HTTP requests: 4.
- Summed HTTP in-flight durations divided by four available slots and search elapsed time: 97.4% occupancy.
- At least one decision HTTP request in flight for 1,225.4 seconds. This is not GPU execution time.
- 42 browser fetches; median 2.6 seconds, maximum 9.7 seconds.
- 44 decision requests submitted, carrying 1,309 evaluation keys. 30 succeeded, 10 reached the 180-second read timeout, 4 were cancelled.
- Successful request latency: mean 97.4 seconds, median 99.0 seconds, maximum 178.9 seconds. All requests were still in the page/link preview phase.
- Tegla Loroupe's Wikipedia preview was available at 149.26 seconds. Full-document evidence selection still waits for the bounded traversal to finish; the main model had received no excerpts before cancellation.

## Controlled replay

The server was idle before each replay: running=0 and waiting=0. Replayed the same state/questions with fresh request_id and cache_salt, sequentially. No server configuration changed. Measurements are one trial each, not a throughput benchmark.

| Request | Run latency | Idle replay latency | Reported input tokens |
|---|---:|---:|---:|
| n35, 2 keys, Ferenc Szekeres | 164.6 s | 1.886 s | 10,732 |
| n1, first 64 keys, Tegla Loroupe | 41.1 s | 27.942 s | 263,441 |

For the 64-key replay, vLLM successful requests increased by exactly 64 and prompt tokens by 263,441. Sum of internal queue times increased by 623.846 seconds (9.748 seconds per internal request); sum of inference durations increased by 173.517 seconds (2.711 seconds per internal request). These sums overlap and must not be added as wall time. One intermediate metrics sample showed 24 waiting internal requests.

The 2-key replay increased successful requests by 2, internal queue-time sum by approximately 0.000064 seconds, and inference-duration sum by 1.425 seconds.

Raw before/after metrics and replay results: `single_replay.json`.

## Conclusion and limits

The rolling scheduler removed the client batch barrier, but the four HTTP slots are now almost continuously occupied. HTTP concurrency 4 is not internal evaluation concurrency 4: four full packets can submit 256 judgments. A small request's 165-second observed delay is not intrinsic to its content, as shown by its 1.9-second idle replay. Large packets alone also have substantial compute and queueing costs.

Exact attribution of every original request's delay remains unavailable because metrics were not sampled during that run. Current metrics do not prove whether a timed-out request continued server work. No server restart, timeout change, evaluation-key removal, or benchmark rerun was performed in this diagnosis.

Potential next experiments should retain all judgments and four HTTP slots, but compare smaller per-request packets (e.g. 8 or 16 keys) on the same workload, measuring total wall time, timeout rate, and server queue/inference metrics. Smaller packets may improve fairness and failure granularity; they do not remove inference work or guarantee a large throughput gain. Returning useful evidence earlier is a separate traversal/agent behavior change: currently up to 50 visits must finish before evidence selection, for each search.
