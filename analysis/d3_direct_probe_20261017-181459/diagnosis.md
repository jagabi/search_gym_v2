# Direct d3 replay — 2026-10-17

Source: stopped v7 run `20261017-1754_jevtree_gpt-oss-20b_browsecomp_raw_browser_p8_10/q00040`.
The source trace ends at 18.89 minutes during its first search. It shows 103 successful
HTTP requests averaging 41.85 seconds, one server disconnect, and four cancellations.
Client queue time was at most 0.66 milliseconds; maximum packet size was 8 and
maximum client in-flight judgments was 32. This is not a client admission wait.

## Direct requests, outside RawTree and LocalDecision

All tests use direct urllib HTTP POST to the configured `/v1/systemone` endpoint,
without a proxy. Each case starts with zero server running/waiting requests.
Request IDs and cache salts are fresh. State and questions match the saved packets.
No server configuration, production configuration, or benchmark process was changed.

| Case | Original run HTTP time | Direct HTTP time |
|---|---:|---:|
| 2 keys: athletics world records | 73.981 s | 2.004 s |
| 8 keys: Kenenisa Bekele | 67.790 s | 4.191 s |

Both isolated calls had negligible internal queue time and all expected results.

## Same four 8-key inputs: concurrent versus sequential

Inputs: Kenenisa Bekele, World Athletics Championships records, Half marathon,
and Olympic athletics records. Both modes complete exactly 32 judgments and
report exactly 133,742 input tokens. Neither mode reports a failure.

| Mode | Individual HTTP times | Total wall time |
|---|---|---:|
| Four HTTP requests concurrently | 19.127, 22.039, 41.685, 39.154 s | 41.826 s |
| One HTTP request at a time | 4.406, 4.080, 3.929, 3.489 s | 16.018 s |

The concurrent trial took 2.61 times as long for this identical workload.
During concurrency, server samples showed up to 21 internal requests waiting.

Server metrics deltas:

| Metric | Concurrent | Sequential |
|---|---:|---:|
| Completed internal requests | 32 | 32 |
| Sum of internal queue times | 486.669 s | 0.001785 s |
| Sum of internal inference times | 296.121 s | 71.966 s |
| Preemptions | 0 | 0 |
| Prefix-cache hits / queries | 0 / 0 | 0 / 0 |

Sums overlap and are not wall-clock durations. Internal inference duration also
increased under concurrency, so this is not just queue delay with unchanged
processing time. The precise GPU/server scheduling cause requires server-side
inspection; these metrics do not establish GPU utilization or a particular bug.

## Interpretation

The 32-outstanding-judgment default remains too aggressive for these inputs on
the current server. The next conservative setting is 8 outstanding judgments:
an 8-key packet runs alone, while up to four 2-key packets can still use the
four-HTTP ceiling. This preserves every judgment and reduces offered concurrency.

These are one trial per mode, concurrent then sequential, on four inputs. They
are evidence for the concurrency bottleneck, not a validated universal optimum
or a guarantee of whole-question runtime. The search still evaluates up to 50
pages before returning evidence, which contributes substantial remaining work.

Artifacts: `summary.json`, `concurrent4/summary.json`, `sequential4/summary.json`;
each folder also retains request/response payloads and before/after metrics.
