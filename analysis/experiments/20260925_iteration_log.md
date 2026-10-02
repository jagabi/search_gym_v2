# DepthSearch development experiments, 2026-09-25

## Fixed conditions

- BrowseComp, at most 10 questions per end-to-end run; same gpt-oss model and sampling.
- Search limit 10, returned results 10. Reader turns 6, depth 3, recursive nodes 12,
  children per reader 2, recursive nodes per root 6. Main turns 40.
- Baseline RAgent/search-o1 code and completed runs are unchanged.
- Root reads are depth 1; they do not consume recursive node/child allowances.
- No gold answers, question IDs or domain-specific fixes are inserted into prompts.
- These are small development samples, not an independent final benchmark.
  Single stochastic runs cannot establish a causal accuracy improvement.

## Cohorts

A is the default first 10 test questions: 3, 7, 8, 13, 15, 21, 22, 26, 27, 32.

B was sampled uniformly before score inspection, excluding A, seed 20260925:
173, 240, 265, 510, 716, 865, 954, 1073, 1128, 1264.
The original question records are in `browsecomp_cohort_b_seed20260925.json`.

## Completed comparisons

| Cohort | Method | Correct | LLM calls | Input tokens | Output tokens | Median seconds |
|---|---|---:|---:|---:|---:|---:|
| A | RAgent | 1/10 | 145 | 978,969 | 104,297 | 109.5 |
| A | search-o1 | 1/10 | 762 | 9,617,122 | 770,199 | 1354.9 |
| A | DS v8 | 2/10 | 1057 | 9,605,374 | 929,855 | 1534.6 |
| A | DS v10 | 1/10 | 401 | 3,672,216 | 408,624 | 594.3 |
| A | DS v11 | 0/10 | 428 | 3,091,478 | 398,907 | 475.3 |
| B | RAgent | 3/10 | 140 | 859,420 | 97,147 | 107.4 |
| B | search-o1 | 3/10 | 566 | 7,024,631 | 595,278 | 957.5 |
| B | DS v8 | 3/10 | 944 | 8,991,277 | 881,882 | 1474.4 |
| B | DS v12 | 2/10 | 362 | 2,729,761 | 328,239 | 419.1 |
| B | DS v13 | 2/10 | 331 | 2,572,639 | 334,208 | 361.0 |

Do not compare A versus B to estimate a version effect. Matched records and paths
are in `v11_results.json` and `v12_b_results.json`.

### v11: omit entry interpretation from main — reverted

Kept the normal closure call, but forwarded only source notes to the main model.
This did not improve this run's accuracy or calls; retaining it was not justified.
It does not prove that all entry interpretations help. The original v10 behavior
was restored before v12. Snapshot: `v11_notes_only/`.

### v12: preserve balanced parentheses in recursive URLs — retained

An actual parser defect cut `.../Runners_(film)` at the closing parenthesis.
DS-only link parsing now preserves balanced/nested parentheses and strips only
surrounding Markdown delimiters. Legacy method paths retain their prior parser.
Snapshot: `v12_link_integrity/`. URL fix tests include execution of the exact URL.

In cohort B there were 89 search batches, 98 root fetches, 29 failed root fetches,
22 batches where every selected root failed, and 16 multi-root selection rounds.
There were 7 recursive returns (5 partial, 1 answered, 1 not_found) plus 4 failed
recursive accesses. See `v12_b_batches.json` for per-question accounting.
This confirms recursive behavior, not that it caused correct final answers.

### v13: one alternate selection after all roots fail — tested, reverted

Parent: v12. One extra selection round is offered only when every selected root
fails access and unused supplied alternatives remain. Both rounds share the
existing root, call, recovery and fetch allowances. Successfully opened but
irrelevant pages do not trigger this access-only fallback. Same cohort B.
164 offline tests passed before launch. It finished 2/10, same as v12, with one
new correct answer (q00865) and one lost answer (q00510). Thirteen recovery rounds
opened six alternatives successfully; four alternative fetches failed and three
rounds chose no alternate. The score gain was not demonstrated. The lower total
calls also coincide with fewer searches (76 versus 89), so they do not establish
that recovery is cheaper. The simpler parent was restored for the next experiment.
Snapshot and six extra regression tests: `v13_access_recovery/`.

The newly correct q00865 used a search title/snippet saying "red suitcase" without
identifying the founders or obtaining a supporting original biography. Keep the
official judge score, but do not present this as a validated recursive success.
No contamination-filter or baseline setting was changed.

## Next diagnosis prepared: factual handoff versus answering again

Saved logs show the entry closure sometimes restates unknown identifying
conditions as satisfied. In q01073 it asserted that a candidate matched distances
and a beach relationship absent from the page notes. In q00265 it promoted an
unverified drama/blog match. The main model then continued with those candidates.

`prepare_handoff_probe.py` builds paired requests from four actual saved contexts,
two repetitions each (16 model-only calls). The proposed variant gives the closure
source observations and notes, asks for observed relations/unresolved conditions,
and leaves the original research question and final decision with the parent.
It does not remove page notes or change extraction/navigation. No production
change was adopted from merely preparing these cases. No search/fetch/judge runs in replay.

### Handoff replays completed; v14 testing

The first 16 calls compared original versus question-free observation handoffs.
A second 8 calls tested the observation format while retaining the original
question for relevance and requesting a short report. All 24 returned nonempty
normal responses. See `handoff_probe_audit.json` for exact accounting and qualitative
limits. Each variant used the same four saved contexts, two repetitions each.

| Variant | Calls | Input tokens | Output tokens | Mean response characters |
|---|---:|---:|---:|---:|
| Original | 8 | 42,788 | 13,280 | 1097.6 |
| Question-free observations | 8 | 42,098 | 9,101 | 2047.5 |
| Question-aware scoped report | 8 | 42,876 | 5,460 | 1102.4 |

Original replays still promoted incomplete blog/town matches. The question-free
variant preserved alternative candidates but added irrelevant unknowns and, in
one successful-film context, rejected the candidates globally. It was not adopted.
The scoped variant returned local reports in all eight cases and retained the
successful film candidate in both repeats. It still confused some entities and
suggested speculative leads; this is not a factual-accuracy guarantee. Original
token cost also includes a single long 7,540-token completion; don't extrapolate
the aggregate savings from these curated cases.

v14 changes only `ENTRY_RETURN_PROMPT` relative to v12, plus its DS cache version.
Original question, source observations, page notes, main loop, root selection and
recursion stay intact. 158 offline tests passed. Cohort B end-to-end run is active:
tag `ds_handoff_v14_b`; snapshot `v14_observation_handoff/`.

The initial v14 execution stopped at 23:17 KST with zero completed records. On
September 26 the server was checked, source/config files matched the snapshot,
and the same run was resumed. Four incomplete traces were preserved under the
run's `interrupted_20260925/` directory before restarting those questions.

## Additional evidence-preservation feasibility checks (offline only so far)

Literal quoted text was matched back to paragraphs already supplied to the v12
readers. Out of 69 extraction responses, 51 contained sufficiently long quoted
spans. Whitespace-only matching found unique paragraph anchors in 28 responses.
Ignoring presentation markup and retaining all matching paragraphs raised
coverage to 40 responses, but still matched only 95/344 quoted spans. A mismatch
does not prove hallucination: paraphrasing, ellipses and markup also break matches.
This heuristic was not added to production.

`prepare_paragraph_probe.py` instead prepares eight model-only extraction calls
(four saved pages, two repetitions), adding local paragraph labels to the exact
already-seen text. It requests citations to those labels within the normal reader
note; no new tool arguments, retrievals or gold data are involved. The prospective
mechanism would return cited source paragraphs alongside the generated notes,
using the existing verbatim-supplement limit. This is a prepared diagnostic, not
an adopted change or measured accuracy improvement.

## Trace parsing note

JSONL records must be split on literal LF (`split('\n')`), not Python `splitlines()`.
Model text can contain Unicode line separators inside a valid JSON string.
Previously reported malformed trace fragments can be artifacts of that parser;
the new audit utility reads literal LF and does not silently skip those records.


## September 26: v14 completed and reverted; structural v15

v14 finished 2/10, same correct IDs as v12 (240, 510), 382 calls versus 362,
3,015,026 input / 349,990 output tokens, median 454.9 s. No gain demonstrated.
ENTRY_RETURN_PROMPT restored from v12. Earlier active-run text is historical.

Paragraph diagnostics: 16 mixed-instruction calls completed, then 8 calls with
a coherent extraction contract (4 saved pages x 2). The clean version returned
6 valid selections, 2 explicit none selections, no invalid IDs, 110,646 input /
9,962 output tokens. Some model prose still misstates relations; prose in Evidence
and Connections is therefore not forwarded as source facts. Coverage/Missing/Next
links remain explicitly marked navigation hypotheses. None selections can lose
useful evidence; syntactic validity is not semantic correctness.

v15 replaces reader fact rewriting with source paragraph selection and code-side
verbatim handoff, preserving recursive link navigation and child returns. Existing
8,192-token supplement cap applies; truncation is explicit. PDF/CSV parsing stays;
the reader selects their source blocks just as for HTML. No extra model stage or
retrieval tool. Baseline paths and cache identities preserved. 165 offline tests
passed, including recursive handoff, invalid IDs, source isolation, and token cap.
Snapshot: v15_extractive_passages. Cohort B end-to-end test is next.


## September 27: research README and v15 resume

README now documents IEEE Access target, gpt-oss-20b / Qwen3.5-9B, DeepSearchQA /
BrowseComp / EvoBrowseComp, actual 10-search/10-result controls and search-o1 top-10,
full and small-run scores, rejected changes, source-loss cases, and reproducibility.
All 64 saved run folders were inventoried; 59 contain completed records. Old README
was preserved. EvoBrowseComp currently has 400 test records, not the historical
50/50/300 split example. No Qwen or EvoBrowseComp completed main runs were found.

v15 had only 5 completed records (173,240,265,510,865), 2 correct, 236 calls.
No Python process remained and source/config hashes matched the saved snapshot.
Four incomplete question directories were preserved in interrupted_20260926/;
the remaining five questions resumed with unchanged code/config. Completed records
and baseline results were retained. Interrupted attempts are separate costs.

A new exact-phrase transport audit is diagnostic only: aliases may be missed and
short words/spam may match without evidence. q01073 is manually confirmed: source
P65 mentions Puerto Viejo, but v15 chose Evidence none because it could not establish
all question conditions. Thus selecting exact source paragraphs still loses useful
partial leads. Also verified that _assistant_message does not replay reasoning_content;
plain CoT clearing is not a grounded remedy for main-model candidate persistence.


v15 completed 10/10: 2 correct (240,510), 454 calls, 3,575,929 input and 363,631
output tokens, median 489.5 s. v12 was 2 correct on the same IDs, 362 calls,
2,729,761 input and 328,239 output. No observed accuracy benefit; default rejected.
There were 38 recursive returns, 113 selection records (60 empty, including 8
access-screen bypasses), 0 invalid-ID selections and 2 clipped source returns.

Default config restores v12 main/reader prompts and disables extractive_evidence.
Experimental implementation remains tested and archived. The balanced URL registry
fix remains, so DS-only cache advances to agent/54-ds-link-registry; baseline 35
unchanged. 165 offline tests pass after restoring defaults. No additional full run
was started. Next architectural hypothesis is to separate navigation decisions
from evidence filtering, rather than add more extraction instructions; untested.
