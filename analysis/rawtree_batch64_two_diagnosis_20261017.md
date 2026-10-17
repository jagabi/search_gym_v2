# Batch64 serial: first two completed questions

Run: `20261017-1041_jevtree_gpt-oss-20b_browsecomp_raw_d3_batch64_serial10`.
Saved config confirms question workers=1 and shared d3 HTTP concurrency=4.
This audit does not change runtime code or issue model/fetch requests.

## Results

- q40: empty answer after a d3 ReadTimeout; 246.4522 seconds, one search.
- q57: correct Vanderbilt Clinical Oncology Research Career Development Award;
  986.574 seconds, two searches. It did not fail.
- q117 has a partial trace but no completed response/record and is excluded.
- No HTTP 400 responses in the two completed traces. No trace events after their
  question end times: previous packet-size and orphaned-client-task issues are
  not observed here.

## q40 failure

Node n8 is `http://www.nyrr.org/hall-of-fame/tegla-loroupe`.
Curl succeeded in 6.2651 seconds. There were 73 candidate links, hence 75 total
judgments split into 64 and 11. Its first 64-key packet was queued at 11.2725s,
dispatched at 62.2957s, and failed at 242.3066s: 51.0232s client slot wait plus
180.0109s HTTP response wait. The second packet was never sent.

Seven other packets succeeded. The Wikipedia page's first 64-key packet took
116.0391s and reported 265,898 input tokens; its remaining 8-key packet was
cancelled when n8 timed out. No search result was returned to the main model.
The error is still propagated as a whole-search failure. Increasing the timeout
alone would not address work volume or partial-evidence loss.

The client log cannot distinguish server scheduling delays, slow inference,
or a server-side stall. HTTP durations must not be called GPU execution times.

## q57 timing and workload

| Phase | HTTP successes | Judgment keys | Input tokens | Mean HTTP seconds | Max HTTP seconds |
|---|---:|---:|---:|---:|---:|
| Page + links | 61 | 882 | 2,767,693 | 29.95 | 178.57 |
| Bundles | 33 | 66 | 267,457 | 6.16 | 17.83 |
| Small chunks | 166 | 332 | 408,716 | 1.17 | 3.11 |
| Total | 260 | 1,280 | 3,443,866 | | |

Of the 882 page/link judgments, 768 are link scores and 114 are page scores
(57 successfully fetched previews, two page scores each).

Merged wall-clock intervals, avoiding double-counting concurrent requests:

- Any d3 request in flight: 952.1914s, 96.52% of elapsed.
- Page/link d3 requests in flight: 850.9130s, 86.25%.
- Any Jina fetch in flight: 51.3847s, 5.21% (overlaps with d3).
- Main LLM: 11.5511s.
- Client decision queue only, with no own HTTP/fetch/main activity: 0.0006s.
- Chunking + bundling accumulated work: 2.353s.

The previous four-question run was dominated by inter-question slot waiting.
Here the outstanding work is mostly already sent to d3. The 260 HTTP requests
still represent 1,280 judgments, not 260 model evaluations. The 64-key Wikipedia
packet's 265,898 reported tokens demonstrate that one shared API state does not
mean the server processes only one 5,000-token input in total.

## Useful evidence versus wasted expansion

Search 1 took 514.56s and returned the correct paper's acknowledgments verbatim
from d1 (`https://pmc.ncbi.nlm.nih.gov/articles/PMC7227421/`, chunk 42). Search 2
took another 455.42s; the final reasoning explicitly used the earlier excerpt.

Across both searches, all 16 returned selection groups are from d1. Of the 43
fetched descendant nodes, 29 had incoming link scores below 0.01 and 39 below
0.05. Low scores do not stop expansion; the best available two per parent are
still nominated, even if all links are poor.

Observed paths include:

- YouTube video -> creators (0.00169) -> creator awards (0.00349) -> awards order
  form (0.00198). The order form's 35-key evaluation took 178.57s.
- YouTube video -> YouTube home (0.00422) -> Korean FTC business information
  (0.00144) -> captcha endpoint (0.000374). One 54-key packet on the captcha page
  took 147.19s.

These are concrete low-value link expansions, not evidence that Docling lost the
answer or that all deeper search is useless. The correct paper itself had a low
preview score and was later read successfully, so a root-page score cutoff is
not interchangeable with a child-link expansion rule.

## Suggested next changes (not implemented by this audit)

1. Stop nominating children when all link scores indicate negligible relevance;
   evaluate a provisional child-link floor rather than dropping d1 pages.
2. On an isolated page/packet timeout, preserve completed candidate evidence and
   distinguish failed evaluation from a real low score. Avoid discarding the
   whole search; keep failures and partial usage explicit.
3. Measure large-packet concurrency separately from two-key chunk concurrency.
   Four 64-key HTTP packets can entail 256 judgments. A lower large-packet
   concurrency is an experiment, not a guaranteed throughput improvement.
4. Obtain server scheduling/GPU metrics during a slow packet if identifying the
   server-side stall specifically; client traces alone cannot settle it.

Supporting artifacts: `rawtree_batch64_two_audit.json`,
`rawtree_batch64_requests.json`, and `audit_rawtree_batch64.py`.
