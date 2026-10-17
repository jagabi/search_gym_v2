# RawTree diagnostic10 audit — 2026-10-17

Run: `runs/test/20261016-2355_jevtree_gpt-oss-20b_browsecomp_raw_d3_c4_d5_10`

## Result and configuration

- 6/10 correct: 40, 117, 326, 366, 598, 1196.
- Incorrect: 57, 516, 746, 1230. Question 516 has a runtime error followed by a salvaged answer; 746 contains no actual country answer.
- Saved run configuration: question workers=4, shared d3 concurrency=4. Local Jina status confirms RPM=0 and max concurrent=50.
- Changed only `conf.yaml` run.workers from 4 to 1 for subsequent executions. Loaded configuration verifies workers=1 and d3 concurrency=4. No benchmark launched; retrieval, scoring, and prompts unchanged.

## Latency

Times below are individual question elapsed times in a concurrent run, not isolated single-question timings. Queue-only means that question has a pending d3 request but no active d3 HTTP, fetch, or main LLM interval. Other questions may be using the shared server during these intervals.

| Question | Correct | Elapsed minutes | Queue-only minutes | d3 HTTP active union minutes | Fetch active union minutes |
|---|---:|---:|---:|---:|---:|
| 40 | yes | 34.93 | 21.00 | 11.05 | 2.44 |
| 57 | no | 61.57 | 43.46 | 13.32 | 3.65 |
| 117 | yes | 30.11 | 20.74 | 6.89 | 2.12 |
| 326 | yes | 52.03 | 31.14 | 15.35 | 5.12 |
| 366 | yes | 24.08 | 14.53 | 8.16 | 1.17 |
| 516 | no | 103.20 | 72.90 | 24.08 | 5.22 |
| 598 | yes | 74.80 | 49.61 | 18.45 | 6.08 |
| 746 | no | 90.15 | 55.74 | 28.43 | 5.03 |
| 1196 | yes | 61.04 | 34.46 | 22.76 | 3.38 |
| 1230 | no | 43.44 | 12.81 | 26.04 | 8.39 |

Mean elapsed 57.54 minutes; median 56.54 minutes. Sum of question elapsed times 34,521.14 seconds is NOT run wall time. Queue-only totals 21,383.67 seconds (61.94% of summed question times). Fetch-active unions total 2,555.88 seconds (7.40%). Fetch and d3-active columns may overlap; do not sum them into a decomposition. HTTP duration includes transport and server queueing, not GPU compute alone.

Trace counts: 66,338 d3 requests/attempts, 66,337 responses, one connection error; 79,841,748 reported input tokens from successful responses.

| Phase | Successful requests | Mean slot wait seconds | Mean HTTP response seconds |
|---|---:|---:|---:|
| Preview | 3,858 | 45.82 | 1.37 |
| Link | 50,291 | 61.84 | 0.46 |
| Bundle | 2,202 | 58.78 | 1.90 |
| Small chunk | 9,986 | 64.79 | 0.64 |

Link scoring accounts for 75.81% of successful calls. Selecting two children does not limit scoring to two calls: every candidate is evaluated separately before selecting children. All question workers share the four decision slots.

Fetch: 2,211 curl attempts (282 errors), mean 2.92s; 324 browser attempts (18 errors), mean 6.97s. These error counts do not include challenge pages incorrectly accepted as successful content. Completed-search chunking plus bundling totals only 134.5s across all questions.

Records undercount work from the aborted search in 516: reader_stats reports 8,291 d3 calls and zero failures, while the trace has 9,239 successful calls and one error. Run-wide record total 65,389 successful calls versus trace total 66,337. Use trace counts for workload diagnosis.

Completed search trees contain 2,182 fast-fetch nodes: d1=446, d2=399, d3=422, d4=454, d5=461. Returned selection groups by depth: d1=332, d2=73, d3=33, d4=21, d5=11. These are selection groups, not unique chunks or verified answer evidence. They exclude the unfinished search in 516. Deep traversal consumes 61.3% of these nodes (d3–5) but supplies 13.8% of selection groups; this alone does not measure causal answer value.

## Incorrect questions

### 57 — correct paper found, curl failure mistaken for poor relevance

Gold: Vanderbilt clinical oncology research career development award. Answer: invented American Cancer Society / Bonavita award.

The first organic result is https://pmc.ncbi.nlm.nih.gov/articles/PMC7227421/ . An independent read of the paper confirms its acknowledgments explicitly state the gold award (https://pmc.ncbi.nlm.nih.gov/articles/PMC7227421/#acknowledgments1).

The run's curl fetch returned only 220 characters of "Cookies must be enabled" and an HHS disclosure link, with is_error=false. Preview scored this as direct=0.06196, query=0.09119. The correct paper never received a browser fetch. No Vanderbilt award text appears in fetched or returned source content. The model repeated similar drug/year queries and eventually guessed an award.

This is a failure of the two-stage admission decision: blocked content became a relevance judgment. A retrieval-unknown state must be distinguished from irrelevant content; a relevant search result with blocked curl content needs a bounded browser retry path. That is an architecture correction, not evidence that better universal scraping establishes a research advantage.

### 516 — partial evidence lost when deeper traversal failed

Gold: Peter King. Answer: Kalyan Banerjee with unsupported and internally inconsistent biographical/film claims.

Queries initially assumed Indonesia without support, then found Fernando Meirelles and The Constant Gardener, diverted into Paul Greengrass, and only later searched Kinsey/Bill Condon. The ninth search was `Bill Condon 2013 film`.

At 5699.7s a d1 curl fetch of https://letterboxd.com/film/the-fifth-estate/ contained "Peter King Nzioki" in the cast list, at character 3918. It was inside the retained 15,275-character / 4,998-token prefix. Preview scores: direct=0.14066, query=0.63636. This is a candidate lead, not proof of all biographical constraints.

At 6180.0s, a link evaluation on n21/link_24 raised RemoteProtocolError: server disconnected without sending a response. The ninth search has no rawtree.return. Its newly fetched cast evidence never reached the main model. A salvage call answered using earlier material. Thus low direct score alone cannot be blamed: the current browser selection has no score floor, and selection/reading never completed for this search.

Preserving completed branches and returning partial evidence on optional-link failure directly addresses this tree-specific loss. Guaranteeing a correct final answer from that change is not possible from these logs.

### 746 — unsupported geographic narrowing plus unparsed tool-like output

Gold: Japan. Final answer contains ongoing reasoning and a search-looking instruction, not a country answer.

Queries guessed Iowa/Minneapolis, even though the clue concerns birthplace rather than necessarily later residence. The search repeatedly targeted Minnesota municipal committees without identifying Person A. Japan in returned excerpts refers to Walter Mondale's ambassadorship, not Person A's teenage stay.

At turn 8, llm.response has finish_reason=stop, reasoning_chars=0, tool_calls=[], recovered_tool_call=false. raw_text contains an assistant/commentary/functions.web_search call-like token sequence. The application accepted the text as an answer, with stop_reason=answered. Only seven of ten allowed searches were used.

This is a model/output-protocol issue in addition to the research failure. Shared output-protocol repairs should be applied consistently to baselines if comparing research methods; do not count this as a depth-search contribution.

### 1230 — city not established, final answer fabricates condition matches

Gold: Regal Cinema. Answer: Coolidge Corner Theatre, with alleged Boston 205-hour traffic and nearby-station facts.

The model fixed on 205 despite the actual question allowing 201–209, then alternated Boston and Saint Petersburg/Russia/Florida. Returned source text does include a Melbourne article saying 205 hours on the road, of which 92 in traffic; this does not establish Boston's 2019 peak congestion. It also returned a Coolidge history excerpt, but the final Boston traffic and station claims are not supported by the retrieved excerpts.

Matches for "Regal" are unrelated Regal Park Place/King of Prussia cinema listings, a bibliography surname, or "regality". They do not show the intended theater was recovered. The failure is candidate discovery and unsupported synthesis, not demonstrated loss of a fetched answer chunk. Query-number matching and generic film/traffic pages do not supply the required city/year/metric relation.

## Next experiments, in priority order

1. Run serial questions with the current internal d3 concurrency=4 to isolate latency; no assumption that elapsed time simply divides by four or that total throughput improves.
2. Isolate optional link failures and return completed partial evidence. Flush partial usage counters even on errors.
3. Replace per-link binary enumeration with a bounded selection workload. Candidate grouping/selection must be separately validated; merging HTTP payloads alone does not prove reduced model work.
4. Preserve blocked/unknown retrieval state at the curl-to-browser admission boundary.
5. Revisit expansion depth only after measuring isolated timings and checking the evidence contribution of deep nodes. Keep the chunker for now.

Artifacts: `analysis/audit_rawtree_ten.py`, `analysis/rawtree_ten_audit.json`, `analysis/rawtree_ten_evidence.json`. The latter is a substring-hit aid; incidental matches are explicitly distinguished from answer evidence above.
