# p15 diagnosis and p16 structural revision

Source run: `20261020-2338_jevtree_gpt-oss-20b_browsecomp_raw_browser_p15_nodeactions10`.
Analysis reads saved files only. No local benchmark, replay, unit tests, imports of
project code, server requests or model calls were run.

## Observations

- Overall accuracy 4/10. Four empty answers (326, 516, 598, 746) count as zero.
  The summary labels these `judge_errors: empty_response`; these are missing model
  answers, not evidence of four judge API failures. Valid-answer-only accuracy 4/6
  is not the benchmark accuracy. Question 57 emitted an action plan as its answer.
- Searches 83, versus p13's 69. Summed recorded latency 3,083.6 s / 51.39 min,
  median 310.75 s; p13 was 8,808.8 s / 146.81 min. These are sums of question
  latencies, not a claim about concurrent run wall time. q40 is cached from the
  preceding single-question run; nine uncached latencies sum to 2,957.8 s.
- Successful d3 judgments 6,397, input tokens 19,223,136, compared with p13's
  18,766 judgments and 63,352,957 input tokens. There are two failed d3 attempts.
  Service time also differs: uncached p15 successful HTTP median 663.3 ms and
  mean 917.0 ms. Thus the runtime gain cannot all be attributed to traversal.
- Reads 36 across 83 searches, with 324 branch returns. Uncached traces contain
  81 searches: 57 perform no reading, 54 perform neither reading nor expansion.
  Uncached actions: RETURN 311, READ 33, EXPAND 16. Twenty-two unread RETURN
  actions had positive direct/query preview relevance higher than RETURN itself,
  but were closed because the separate abstract read-action score was lower.
- Fetch attempts 449, failures 142 (31.6%). No new access workaround is proposed.

| ID | Correct | Searches | Recorded seconds | Page reads | Outcome |
|---|---:|---:|---:|---:|---|
| 40 | yes | 2 | 125.8 | 3 | cached from single-question run |
| 57 | no | 10 | 328.0 | 8 | action-plan answer; target access failed |
| 117 | yes | 7 | 203.4 | 2 | solved |
| 326 | no | 10 | 218.1 | 0 | empty answer; correct source discarded |
| 366 | yes | 5 | 189.8 | 4 | solved |
| 516 | no | 10 | 667.0 | 6 | empty answer; wrong director searches |
| 598 | no | 10 | 312.3 | 2 | empty answer; target PDF access failed |
| 746 | no | 10 | 309.2 | 3 | empty answer; alternative VP excluded |
| 1196 | yes | 9 | 404.4 | 6 | solved |
| 1230 | no | 10 | 325.6 | 2 | wrong city; exclusive boundary violated |

## Concrete failures

### 326: useful observed source was never delivered

The Fran Manushkin Encyclopedia source prefix explicitly contains:
`Baby ... 1972, published as Baby, Come Out!, 1984`.
One preview scored original-question usefulness .79346, query usefulness .52900,
RETURN .74217, READ .26222. The page was closed, and the entire ten-search
question performed zero chunk reading. A later finalization reasoning mentions
Baby but still produces no final answer. This is an actionable retrieval-policy
regression, not a lack of discoverable evidence.

### 746: independent admission scores crowd out a different candidate

The `Vice President born in Maine` result set includes Nelson Rockefeller as rank 7,
with a snippet explicitly connecting him to Bar Harbor and the vice presidency.
Its query score is .59543, but all six admitted entries are Hamlin-related.
The fetched Hamlin pages are then closed without reading. The main model later
combines a 1930s-born person with Hamlin's nineteenth-century chronology.
Preserving another source-supported candidate is a tree admission problem;
making the main model reason correctly afterward is not guaranteed.

### 1230: useful query facts lose to an abstract closing preference

The Business Today prefix explicitly pairs Mumbai with 209 rush-hour hours;
the preview gives query relevance .76632 but READ .37977 and RETURN .44262.
It is closed. Some Mumbai content from another article is returned, but the final
answer selects an invented Moscow cinema and treats 210 as strictly below 210.
Better routing can improve evidence delivery; it does not prove the main model
will stop misusing numeric constraints.

### Remaining failures

- 57: the correct PMC7227421 URL fails eight times with Reader HTTP 422.
- 598: the correct RRS_10_2013_a1en.pdf fails twice with Reader HTTP 422.
  The PDF hint is present in reader diagnostics. A hint alone does not establish
  the underlying browser failure mechanism.
- 516: the first search assumes Bruce Beresford, followed by other guessed
  directors. No Bill Condon / Peter King / Nzioki match appears in this run's
  source preview evidence inspected. Re-ranking unavailable answers cannot solve
  this automatically. No benchmark-specific names or answers enter p16 prompts.
- All four empty-answer cases have two finalization attempts; the reasoning
  continues proposing searches despite no tools being available. No extra retries,
  model replacement or reasoning forwarding is added here.

## p16 implementation

1. **Positive marginal reading value:** reuse the two direct/query d3 judgments,
   now conditioned on already selected original evidence. Derive READ as their max.
   A query-answering fact can be read even if it does not solve the full question.
   Eliminate the separate `read_now` HTTP judgment. Available actions still compete
   by argmax with RETURN on ties; no numeric branch-stop threshold is added.
2. **Exhaustion instead of generic cost preference:** RETURN asks whether useful
   relations are already extracted or neither the document nor its concrete routes
   plausibly contain new relevant facts. Explicit useful prefix facts support reading,
   not returning. EXPAND asks about concrete additional destination evidence.
3. **Conditional entry admission:** keep standalone ranking, seed the first four
   slots balanced between direct/query objectives under the default six-entry budget,
   compare all remaining leads with that
   seed using one `entry_gain` key each, and fill the existing last two slots by added
   route value. The slot count reuses the existing frontier width, capped below the
   admitted width. This is d3 semantic judgment, not entity parsing or domain rules.
   Missing comparisons retain the original admission order; failures remain unknown.
4. **Evidence first:** put retrieved original excerpts before the navigation notice
   and original unverified search JSON in the beam search response. Preserve all
   existing content and output bounds. No new summarization or interpretation model.
5. Preserve exact numeric values and event years, including facts refuting guesses,
   in d3 relation instructions. Strict bounds exclude endpoints.

The main model, its system prompt, only-web_search tool contract, reader endpoint,
packet size 1, four-question HTTP wave limit, 10 searches, 6 initial pages,
2-parent/child beam, depth 3, 10 visits, 2 reads, chunk quotas and output budget
are unchanged. No BM25, lexical matcher, embedding retriever, query rewrite tool,
forced minimum read count, or access fallback is introduced.

Initial default six-page judgments lose one key per readable page. The new entry
comparison normally adds six short judgments per ten-result search. Post-read
re-evaluation now judges two positive reading objectives instead of one abstract
reading key. More useful reading can add work within existing budgets. Runtime
parity and accuracy improvements are hypotheses, not measured results.

## Verification and server command

Static AST parsing and scoped diff whitespace checks only. Server regression source
adds a high-query/low-original case beating RETURN without a separate read request,
evidence-before-navigation ordering, marginal entry admission, and failure fallback.
Existing local-return independence, depth barriers and read-limit regressions remain.

```cmd
python test.py --method jevtree --model gpt-oss --benchmark browsecomp --path data/browsecomp/test_diagnostic10.json --limit 10 --raw-traversal beam --expect-raw-traversal beam --tag raw_browser_p16_evidence10
```

Check the same ten for correct answers, zero-read searches, empty final answers,
query count, successful d3 work and per-question time. In particular inspect 326's
first Manushkin read and 746's candidate admission. Do not interpret accuracy on
this diagnostic ten as a held-out generalization result.
