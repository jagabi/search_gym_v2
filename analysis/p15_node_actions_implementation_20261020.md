# p15: node-local read / expand / return

Scope: existing RawTree beam traversal only. Main model retains only web_search;
main reasoning is not sent to d3. No new research tools or retrieval methods.
d3 endpoint, packet size, concurrency and numeric search/read/depth budgets are unchanged.
Raw version is raw-browser-d3-navigation-docling/15, invalidating the old raw cache fingerprint.

## Execution

1. Retain initial search-result ranking and admission of at most six documents.
2. Fetch and evaluate all admitted nodes at the current depth concurrently. A node's
   preview evaluation includes its existing direct/query relevance keys plus available
   return_now, read_now, expand_now keys. These share one observation; current packet
   size 1 still means separate HTTP requests, with the existing four-question wave cap.
3. Select each node's maximum-scoring available action. Ties prefer return, then read,
   then expand. RETURN closes only this branch, never cancels sibling work, and does
   not promote an unread prefix into source excerpts. No new numeric stop threshold.
4. If any surviving node proposes READ, read one document before advancing depth.
   Compare read_now scores, with the existing direct/query objective as a tie-breaker;
   assign the first available direct reservation, then query. Existing document-region,
   bundle and atomic-chunk selection still apply. This is partial reading, not exhaustive.
5. Store bounded original selected chunks (existing read-context budget, not summaries).
   Re-evaluate still-open nodes against those chunks. Closed branches stay closed.
   Previously read or duplicate documents are not available READ actions.
6. Repeat until there are no READ proposals. Among EXPAND proposals retain at most
   the existing parent beam width, ranked by expand_now, then query relevance. Only
   these parents incur individual link evaluations. Link keys see selected original
   chunks too. Existing per-parent nominations, link floor and global child beam apply.
7. Open the selected children only after the current depth's work has finished.
   No speculative next-depth fetch or asynchronous global stop.
8. Finish when branches close, paths/budgets are exhausted, or decisions are unavailable.
   Exhausting the document-read budget disables new expansion; no forced quota fill.
   A zero configured read quota still allows traversal-only comparison configurations.
9. Render the selected documents from the scored-chunk cache under the existing global
   excerpt quotas/output budget. No second reading pass.

## Diagnostics and limitations

- rawtree.node_action records executed read/expand/return or unavailable, scores and depth.
- rawtree.read_context retains selected original chunk ids; rawtree.expansion_selection
  and rawtree.frontier show which parents and children were actually admitted.
- rawtree.traversal_end distinguishes branches_closed, read_budget, page_budget,
  frontier_exhausted and evaluation_failed. branch_returns is aggregated in reader_stats.
- An incomplete action judgment is recorded as failure/unknown, never a successful RETURN.
- Existing chunk/link floors remain. Threshold-free here refers only to branch action selection.
- More action keys and post-read judgments add d3 work. Early branch closure may avoid link
  judgments and child visits, but latency/accuracy improvements are not yet measured.
- Each depth still waits for its slowest fetch/evaluation; initial root admission is unchanged.
- Reading is prioritized within a completed depth. Two READ choices may consume both slots
  there and end traversal. The model must value deeper routes over redundant local reading.
- Scores can still close useful branches under partial observation; tie-to-return is an
  explicit policy choice. Source coverage and score comparability require server evaluation.
- The p14 81.6-minute q40 trace contains zero successful d3 judgments and 103 180-second
  ReadTimeout errors. This structural change does not fix that external service failure.

## Verification

Only static AST parsing and scoped git diff whitespace checks locally. No tests,
benchmark runs, model requests, or network probes executed locally.
Server regression source covers sibling RETURN independence, depth barriers,
read-before-expansion, reserving a second read through depth three, read limits,
ties, and incomplete action scores. Retained traversal-then-read source-selection
regressions explicitly use best_first; beam scheduling regressions use action scores.

CMD, first diagnostic item:

```cmd
python test.py --method jevtree --model gpt-oss --benchmark browsecomp --path data/browsecomp/test_diagnostic10.json --limit 1 --raw-traversal beam --expect-raw-traversal beam --tag raw_browser_p15_nodeactions1
```

CMD, diagnostic ten:

```cmd
python test.py --method jevtree --model gpt-oss --benchmark browsecomp --path data/browsecomp/test_diagnostic10.json --limit 10 --raw-traversal beam --expect-raw-traversal beam --tag raw_browser_p15_nodeactions10
```
