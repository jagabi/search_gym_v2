# Manual scheduler simulation before another server experiment

No source edits, execution, replay, unit tests or model calls. The values below
are fictional action preferences used to trace control flow. They are not d3
predictions and do not establish accuracy or score calibration.

## Existing p17: deterministic counterexamples

### A. A good expansion is starved by unrelated reads

Initial depth 1, two remaining document reads:

| Node | Best proposal | Preference |
|---|---|---:|
| A | EXPAND | .85 |
| B | READ | .65 |
| C | READ | .60 |

Current scheduler enters reading whenever any READ exists. Suppose B's read does
not change C's proposal. It reads B, then C. The second read removes EXPAND from A.
No child visit occurs, despite A initially having the strongest proposal.
This failure follows from code order and budget gating, without a server run.

### B. Depth 2 is cut off by the final read

Remaining reads: one. Node A proposes EXPAND .58 over RETURN .52; another node
requests reading. The current loop reads that node, consumes the last slot, then
requests only RETURN for A. A's .43 RETURN wins because it is the only available
action, not because a new model comparison rejected expansion. Actual p17 examples
include q1196 and q1230 at depth 2.

### C. Minimum reading can reveal a route that cannot be followed

All nodes initially RETURN. The exit-time minimum read finds a useful source
record link beyond the prefix. Current p17 immediately renders evidence and
returns. No routing evaluation receives that new route within the search.
Minimum reading therefore does not restore recursive traversal.

## Candidate state-machine correction, not an implemented revision

Separate document-read accounting from local branch closure. Branch candidates
are judged with actual destination information; links in selected original chunks
are incorporated before the next route judgment. The reading pool retains closed
sources. A newly observed route is new information and may require reconsidering
the affected node; this differs deliberately from irrevocable closure under an old
prefix observation. Old sibling branches need not all be rerun.

Represent consumption of the final document-read slot as an explicit terminal
operation rather than an ordinary read that silently disables future expansion:

- READ_CONTINUE: available with at least two remaining slots. Read once, then
  evaluate the newly observed evidence/routes. Consumes one actual read.
- EXPAND: available within depth/visit bounds while at least one slot remains.
  Reading proposals at other nodes have no unconditional precedence over it.
- READ_FINISH: with one remaining slot, choose the best source from the observed
  pool, read it and end this search deliberately. It cannot mean read-then-expand.
- FINISH: return already selected evidence without filling the remaining slot.
- RETURN(node): closes that node under its current observation; does not stop
  siblings or remove the source from the reading pool.

READ and EXPAND require an explicit scheduler choice. Sorting probabilities of
source relevance, route usefulness and exhaustion is not a demonstrated substitute
for comparable next-operation judgments. Joint action semantics/observation size
remain a design and server-validation question; these traces do not settle them.

## Candidate flow traces and required invariants

1. **Easy source:** R=2, READ_CONTINUE(A) -> R=1. Source excerpts establish the
   query relation; routing judges further routes unhelpful. FINISH -> one read,
   no child visits, no forced second read. High relevance alone does not end search.
2. **Useful route first:** R=2, select EXPAND(A) instead of B's pending read.
   Children at depth 2 are evaluated before a source is committed. A promising
   further route can reach depth 3; source selection may remain deferred. At no
   point does the existence of another READ proposal force consumption of R.
3. **First read, then depth 3:** READ_CONTINUE(A) -> R=1. Select EXPAND(B) ->
   depth 2. Select EXPAND(B1) -> depth 3. READ_FINISH(best observed source) -> R=0
   and terminal return. Two actual reads, maximum depth 3, no increase in budgets.
4. **Last read is chosen early:** R=1, READ_FINISH(B) wins over EXPAND(A). Read B
   and finish. No depth 3 here, but this is an explicit terminal tradeoff. Calling
   it an ordinary read and later claiming d3 chose RETURN would be misleading.
5. **All branches initially close:** R=2, no previous read, eligible scored source
   exists. Minimum read is READ_CONTINUE(best source), not an immediate exit read.
   If new original content reveals a useful route, evaluate that affected route
   with R=1; EXPAND may continue. If not, FINISH after one read. If no chunks qualify,
   an attempt is still counted; a second read is not automatically forced.
6. **Sibling returns:** A and B RETURN while C's work is pending. Complete C's
   current-depth job. If C proposes an accepted expansion, only C's children open.
   No local RETURN cancels sibling work or bypasses the depth barrier.
7. **Budget boundary:** READ_CONTINUE is unavailable at R=1. READ_FINISH is
   terminal. Therefore R=0 with newly scheduled child jobs is an invalid state,
   detectable before model inference. Visit/depth limits always remain hard bounds.

## Counterexample that cannot be promised away

Suppose a first bridge requires a full read to expose link 1, a second bridge
requires another full read to expose link 2, and the final source requires a third
read to expose its answer. A two-read budget cannot guarantee solving that path.
Renaming a third read as preview/preprocessing would hide a budget increase.
This is a limitation of the stated observation budget, not a scheduler bug.

Likewise, no trace proves that d3 will choose a gold route, an unread source will
contain an answer, or the main model will use returned facts correctly.

## Before another hour-long benchmark

The above traces are acceptance requirements for implementation and later server
regressions, not tests already run. Review that code preserves each transition,
does not hide last-slot consumption, observes real destination information, and
re-evaluates newly found routes before returning. Only then use the diagnostic run
to measure uncertain model choices, answer quality, cost and depth behavior.
