# p29 stopped-run latency audit

Saved traces only; no model/network calls or implementation changes.
Run: runs/test/20261022-1233_jevtree_gpt-oss-20b_browsecomp_raw_browser_p29_return_now_10

## Confirmed client concurrency

Both questions reached at most four actual concurrent HTTP attempts, at most four attempts per wave, with no next-wave start before the preceding wave ended. jev.request records registration/queueing; jev.attempt records HTTP admission. No increase in concurrency is proposed.

## Wall time (overlapping intervals unioned)

| Component | q40, complete | q57, interrupted |
|---|---:|---:|
| Recorded question time | 330.949 s | 1890.381 s |
| D3 active HTTP union | 296.067 s | 1784.341 s |
| D3 joint source/link phase | 236.567 s | 1700.137 s |
| Main model | 8.479 s | 16.291 s |
| Fetch active interval union | 27.206 s | 81.065 s |
| Local chunking sum | 0.630 s | 6.157 s |

Fetch and D3 can overlap; these rows must not be added as exclusive elapsed categories. Queue time is not added again to HTTP wall time.

## Main bottleneck

q57 joint source/link processing occupied about 90% of recorded elapsed time. It sent 44 joint HTTP requests: 31 received responses, nine hit ReadTimeout near 180 s, four were cancelled at interruption. Local queue waits before later starts reached about 332 s. Total actual D3 attempts were 155, not thousands.

A q40 joint request with 56 keys reported 200271 input tokens and took 170.92 s after HTTP start. A q57 request with 31 keys reported 106482 tokens and took 97.09 s. The source state cap of 4096 does not cap aggregate server-reported usage across decision keys. This suggests key-associated work is expensive; reported usage alone cannot establish whether the server physically recomputes or caches shared prefixes. GPU, server queue and network subdivisions need server-side telemetry.

The four-request wave barrier also delays queued work behind a slow/timeout member. This is expected configured behavior, not a violation of four-at-a-time admission. Do not raise concurrency.

## Why early return did not remove the delay

q40 triggered early return in all three searches and never exceeded depth 1, but the first stopping response itself took 170.92 s. Signal-to-drained cleanup took 1.0-1.7 ms. Therefore request cancellation cleanup was not the bottleneck.

q57 triggered no accepted early return. Among 31 successful joint responses carrying return_now, one exceeded .5 (0.50639), but direct/query scores were .00829/.01657, below .15. All six completed searches returned zero source excerpts. The reasoning model consequently continued to search; the seventh search was interrupted. No final result or accuracy exists for q57.

## Why so many full bundles were evaluated

All ten inspected documents had <=16 bundles: 4,1,6,3,5,7,5,1,16,5. The configured short-document cutoff therefore bypassed the document routing tree every time: zero region calls. Planned joint requests totalled 53; nine were still unstarted when interrupted.

The final search alone scheduled 21 whole-bundle evaluations: 16 from a 2023 Frontiers review, five from a 2025 Springer article. At interruption it had already lasted 412.44 s. The full-source calls, attached link keys and exhaustive <=16-bundle policy combine to dominate latency.

## Secondary observations and uncertainty

q57 had 29 fetch failures out of 44 fetches (27 Reader HTTP 422 responses), but fetch wall union was only 81.1 s. Access failures hurt evidence acquisition but do not explain most elapsed time.

q40's first post-cancellation entry wave took 33.09 s per request, whereas similar entry requests elsewhere generally took about 1-3 s. Residual server work after HTTP cancellation or server scheduling contention is a plausible explanation, not proven from client traces.

Next investigation should focus on per-key server workload and the full-bundle/link-key coupling, followed by the exhaustive document cutoff. Four-request admission is already enforced and should remain unchanged.
