# p17 diagnostic ten: policy works, accuracy improvement is limited

Run: `20261021-1012_jevtree_gpt-oss-20b_browsecomp_raw_browser_p17_readpool10`.
Comparison: p15 `20261020-2338_jevtree_gpt-oss-20b_browsecomp_raw_browser_p15_nodeactions10`.
Only saved logs were analyzed. No code edits, tests, benchmark/replay runs, project
imports or model/network requests. p17 includes p16 changes, so effects cannot be
assigned to the minimum-read policy alone. The same ten are diagnostic, not held-out.

## Aggregate

| Metric | p15 | p17 |
|---|---:|---:|
| Accuracy | 4/10 | 5/10 |
| Empty final answers | 4 | 1 |
| Searches | 83 | 78 |
| Sum of recorded question times | 3,083.6 s (51.39 min) | 3,132.9 s (52.22 min) |
| Median question time | 310.75 s | 352.8 s |
| Documents read | 36 | 84 |
| Returned chunks | 236 | 564 |
| Successful d3 requests | 6,397 | 7,663 |
| d3 input tokens | 19,223,136 | 18,683,485 |
| Main input tokens | 1,793,249 | 2,203,267 |
| Main calls | 109 | 102 |
| Fetch attempts / failures | 449 / 142 | 413 / 105 |
| Descendant visits | 27 | 12 |

Summed latency rises 1.60%; median rises 13.5%. Reads rise 133.3%, main input
tokens rise 22.9%, while d3 input tokens fall 2.8%. More requests alone do not mean
the same increase in compute cost. Successful d3 HTTP service time in uncached
traces also improves: p15 median 663.3 ms / mean 917.0 ms versus p17 median
609.4 ms / mean 765.0 ms. Runtime is descriptive, not a controlled causal comparison.
p15 q40 is cached from its preceding single-item run; p17 has no agent cache hits.
The latency sum is not the run's concurrent wall time.

## Per question

| ID | p15 -> p17 score | p17 searches | p15 -> p17 seconds | p17 reads | Minimum-read selections |
|---|---|---:|---|---:|---:|
| 40 | 1 -> 1 | 3 | 125.8 -> 180.5 | 5 | 0 |
| 57 | 0 -> 0 | 10 | 328.0 -> 344.2 | 9 | 5 |
| 117 | 1 -> 1 | 6 | 203.4 -> 195.6 | 7 | 3 |
| 326 | 0 -> 0 | 10 | 218.1 -> 364.3 | 10 | 4 |
| 366 | 1 -> 1 | 3 | 189.8 -> 124.3 | 4 | 0 |
| 516 | 0 -> 0 | 10 | 667.0 -> 421.6 | 11 | 7 |
| 598 | 0 -> 1 | 10 | 312.3 -> 331.5 | 8 | 5 |
| 746 | 0 -> 0 | 10 | 309.2 -> 403.4 | 11 | 7 |
| 1196 | 1 -> 1 | 6 | 404.4 -> 361.4 | 8 | 3 |
| 1230 | 0 -> 0 | 10 | 325.6 -> 406.1 | 11 | 6 |

All four previously correct items stay correct. The only additional scored success
is 598, produced on the second finalization attempt after ten searches. Four items
still answer normally during research, as in p15. This is not evidence of a large
increase in grounded problem-solving ability.

## Did the implemented policy execute?

Yes. Across 78 searches:

- Minimum-reading selection occurs 40 times. Eleven of those return no selected
  source excerpts. Of the other 29, presence of excerpts does not establish relevance.
- There are only five searches with zero document reads: four have no admitted
  results; one has two results and both fetches fail. This respects the eligibility
  rule rather than indicating the minimum-read selection was skipped incorrectly.
- Sixteen searches return no excerpts, including failed/empty searches and selected
  documents without qualifying chunk output.
- Thirty-nine minimum reads use nodes already marked RETURN. Two further reads
  requested by siblings select previously closed source candidates. Thus branch
  closure no longer excludes source reading. No evidence here establishes that
  these two independent-pool selections caused an answer improvement.
- The minimum-read winner's preview score has median .4743, minimum .1768 and
  maximum .7991. These describe scores only; there is no new policy threshold.

Forced reading therefore solves the zero-reading control-flow problem. It also
reads weak candidates. It does not create missing source discovery or guarantee
that the chunks are useful. Expanding the minimum to two reads is not supported.

## Failure localization

### 326: this run never discovers the correct author

p15 fetched the Fran Manushkin source containing Baby / Baby, Come Out! but closed
it unread. p17 reads ten documents, yet neither Manushkin nor that title change
appears in inspected search leads, source previews, complete chunked documents or
returned evidence. Thus this run cannot test whether preserving that particular
source would solve the item: the source is absent upstream.

The first minimum read selects Cormac McCarthy. Other selections include generic
tour guides and birdwatching, as well as unrelated author biographies. Query-only
relevance wins even when original-question relevance is weak. Examples:
Walk Chicago Tours guides direct .1548 / query .7991; Virginia birdwatching direct
.0740 / query .3729. The main ultimately cannot identify an author and returns an
abstention. This is source discovery / subject-relation precision, not remaining
zero-reading loss. Do not claim that more reading solved 326.

### 516: a valid candidate is delivered too late, then rejected

The correct The Constant Gardener / The Fifth Estate / director connections are
reached. The last, tenth query finally discovers Peter King Nzioki as Policeman 1.
This actor-role relation is selected from NNDB and delivered verbatim; the final
answer even names him. There is no remaining search budget for parental/birth
verification. The main rejects candidates without establishing its negative claims.
It spends earlier queries on repeated director identification and zodiac questions.

Unlike p15, the candidate is present. The current bottleneck is delayed candidate
arrival, search allocation and final inference, not d3 discarding that final cast
relation. Reading all chunked Metacritic source data inspected did not reveal an
earlier Peter King / Nzioki passage, so this audit does not assert an earlier hidden
cast-chunk loss there.

### 746: the alternate VP is absent from search leads in this run

No Rockefeller result appears in the inspected result candidates. The only source
mention found is a generic vice-president navigation menu, not a Maine-birth fact.
The new conditional entry admission cannot preserve an alternate lead that was
not returned. The selected/read sources supply Hamlin; no evidence identifies the
target person or Japan. The final answer is Unknown but incorrectly presents many
unverified question premises as confirmed facts.

Several queries repeat Iowa waterways or restrict an unsupported person to a
particular birth year. Do not claim that p16 entry diversity succeeded or failed
on the p15 rank-7 Rockefeller case: that comparison opportunity is absent here.

### 57: access failure is more specifically identified

The correct PMC7227421 URL fails five times. Reader returns HTTP 422 with
`AssertionFailureError`, status 42206, message `Expected status code 200 but got 203`.
This is failure of the asserted source-status check, not a PDF-type diagnosis and
not the earlier d3 timeout. The trace does not contain the 203 response body, so
it does not establish whether that body was a real article or an access screen.
Do not treat accepting 203 as a proven fix without inspecting that body on server.
Final answer remains empty despite nine document reads elsewhere.

### 598: scored success, incomplete evidentiary chain

The judge accepts the Romanian publication answer. However the cited
RRS4_2014_site.pdf fails three times and the specific RRS_10_2013_a1en.pdf fails
twice. Each reports `Expected status code 200 but got 503` through Reader HTTP 422.
The answer's cited acknowledgements were therefore not verified from that PDF.
Search leads and other source material may support the venue inference, but this
is not demonstrated full-paper verification. Report the correct score honestly
without treating the single gain as proof of a robust retrieval improvement.

### 1230: final reasoning contradicts its own quoted conditions

The first forced read is Tampa Theatre. The final answer describes a 1926 opening
as being in the early 1929-1933 depression and claims 174 hours is strictly between
200 and 210. These are visible contradictions in the final answer, not a lack of
source reading: eleven documents were read. The route never establishes the gold
Regal Cinema. More raw reading alone does not remedy these inference errors.

## Implications for the next revision

Keep the closed-source pool invariant: its intended operation is verified. Do not
increase minimum read count, depth or visits on this evidence. The next retrieval
target is precision of candidate/subject relations and useful bridge selection,
especially where a high query score promotes a source weakly connected to the
original identification. This requires semantic d3 criteria, not lexical rules.

326/746 also expose upstream query-route failures; 516 exposes candidate arrival
at the final query; 1230 exposes main inference. Under the user's fixed main-model
constraint these are limits on what tree/source ranking alone can guarantee. Keep
those separate from controllable source selection rather than claiming all failures
are tree-expansion defects. Access issues require server-side source-body diagnosis.

No code changes were made for this diagnosis. The existing modified q746/q1196
trace files were only read, not edited or reverted. Machine-readable metrics are
saved in `p17_readpool10_audit_20261021.json`.
