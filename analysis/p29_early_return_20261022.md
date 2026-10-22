# p29: search-local early return with committed partial results

No live d3, Jina, main model, judge or benchmark calls were made. All verification used fake decisions / HTTP MockTransport.

## Decision

- Page inspection remains one inspect_value key. State remains page_title + page_text, <=4096 d3 tokens.
- Only full source-bundle evaluation adds return_now alongside direct_answer, query_answer and eligible link_N keys. All authored instructions and criteria are English.
- return_now asks whether explicit source facts establish or refute the CURRENT search target within the original question's scope. It does not decide the overall final answer. Topic mentions, unresolved candidates, partial lists and promising links alone do not suffice.
- Uses the existing noul response format: >0.5 means yes; a tie continues. No new tunable confidence threshold or choice-response parser was introduced.
- A yes is accepted only with both evidence keys present, an eligible final-source objective above the existing evidence floor, a nonzero final source quota, and enough output space for the complete bundle (including a conservative header allowance).

## Concurrency and ownership

1. Every search creates its own SearchReturn event and candidate list.
2. LocalDecision can deliver valid scores per completed HTTP packet. The first packet includes the two evidence keys and return_now; a later link packet cannot hold up a valid return signal.
3. Packet callbacks synchronously commit raw source units and valid link scores before setting the stop event. Partial or cancelled pages therefore do not lose completed evidence.
4. Stop-aware gathers preserve completed results, cancel unfinished owned tasks and await their cleanup. Source/region code stops scheduling new work. The HTTP admission guard checks the event again after acquiring request capacity, preventing queued packets from starting after the signal.
5. drain_search waits for this search's cancelled dispatch/HTTP tasks only. Another search is neither cancelled nor awaited. Client-side cancellation does not prove the remote model server stopped its already-running computation.
6. After draining, no child frontier is opened. Final rendering reuses committed cache entries and prioritizes returning source documents/bundles so unrelated higher relevance cannot displace the stopping evidence.
7. Multiple completed signals are permitted; each bundle registers at most once. The next search gets a fresh signal.

## Diagnostics

- rawtree.early_return_requested: node, bundle and return score.
- rawtree.early_return_drained: preserved candidates/pages, next_depth_started=false.
- rawtree.traversal_end.reason=return_now.
- early_returns and return_now_signals aggregate into reader statistics.

## Verification

129 raw/native offline tests passed. Coverage includes fast-return/slow-sibling cancellation; first 64-key packet stopping a stalled remaining link packet; preserved winning source despite a higher relevance sibling; multiple simultaneous signals; resetting between searches; isolating another concurrent search during cleanup; tie/no-evidence/output-budget guards; English authored prompts; existing traversal, transport, output and PDF/CSV regressions.

Existing limits remain unchanged: HTTP concurrency four, <=64 keys per request, per-depth inspection/frontier width two, branch two, depth three, ten visits and two final evidence-source slots. The initial depth's page-preview barrier remains; early return applies once full source evidence has actually been observed. Runtime and answer accuracy require server-side evaluation.
