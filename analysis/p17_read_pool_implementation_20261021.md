# p17: closed branches retain source candidates

This revision includes the preceding unmeasured p16 changes. It does not represent
an independent benchmark result. Raw version: raw-browser-d3-navigation-docling/17.

## Source selection and branch closure

- Every successfully fetched document with valid direct/query preview scores stays
  in the reading pool across all visited depths, including local RETURN nodes.
- Local READ proposals request a reading step. The source is selected from the
  entire pool, not just the nodes making those proposals. A previously closed
  source may win without reopening its outgoing links.
- Choose by the maximum direct/query marginal reading score, then the available
  objective reservation as tie-breaker. The original direct/query reservations and
  total document-read limit still apply. No numeric reading floor is added.
- After new original chunks are read, refresh reading scores of still-unread pool
  candidates when needed. This includes closed branches. Already refreshed open
  nodes reuse their current scores; an evidence revision avoids redundant scoring.
- A failed marginal comparison retains an earlier valid source score and records
  the failure. It is not changed to zero. Partial score pairs are updated atomically.
- Closed branches never re-enter the expansion frontier. The existing per-depth
  barrier, parent beam, child beam, visit/depth limits and chunk cache are retained.

## Zero-read completion

When beam traversal finishes with no document selected for reading, choose exactly
one best eligible source from the same pool and run the existing region/bundle/chunk
reader before returning. This uses an existing read slot, not an additional budget.
There is no second forced read if any document was already read, including a read
that produced no selected chunks because the document lacked qualifying evidence.

No forced selection occurs with zero read quota, failed fetches only, or no complete
source reading scores. Missing navigation action scores do not invalidate otherwise
valid source reading scores: useful original evidence can still be read while the
branch-control failure remains explicitly unknown.

This guarantees one document-reading attempt under the eligibility conditions; it
does not guarantee relevant selected chunks or a correct final answer. Access errors
and main-model reasoning/finalization failures remain outside this structural fix.

## Trace

- `rawtree.read_selection` records reason (`node_read_request` or `zero_read_search`),
  candidate ids, source scores, evidence revisions, selected id and objective.
- `rawtree.node_action` records the executed read and requesting node ids. A source
  can have RETURN followed by READ without any new child expansion; these events
  describe different decisions. Final minimum reads use `reason=zero_read_search`.
- `zero_read_selections` is aggregated into `reader_stats`.
- `rawtree.read_context` and the final source chunk cache remain the actual evidence
  record. The minimum reading occurs before `rawtree.traversal_end` is emitted;
  that interval continues to include staged reading, as in p15/p16.

## Costs and validation

Only existing structural selection and diagnostics were changed. No new research
tools, lexical/embedding retrievers, main-reasoning forwarding, access fallbacks,
model changes, budget increases or local experiments. Configuration values and the
main system prompt are unchanged. Conditional comparisons and minimum reads may
increase latency relative to returning no evidence; server measurements are required.

Server regression source covers all-RETURN minimum reading, reading a closed source
on a sibling's request, refreshing a closed source after new evidence, explicit zero
read quota, failed fetches, partial navigation judgments with valid source scores,
and no forced second read. Existing sibling completion/depth/read-budget tests remain.

Local verification is restricted to static AST parsing and scoped whitespace checks;
no unit tests, project imports, model calls or benchmark/replay runs were executed.

```cmd
python test.py --method jevtree --model gpt-oss --benchmark browsecomp --path data/browsecomp/test_diagnostic10.json --limit 10 --raw-traversal beam --expect-raw-traversal beam --tag raw_browser_p17_readpool10
```

Inspect q326 source selection/excerpts, q746 entry alternatives, zero-read selections,
empty final answers, correctness, successful d3 work and per-question latency. p17
retains p16 entry admission and evidence-first formatting, so a new run measures the
combined revision rather than isolating the minimum-read policy alone.
