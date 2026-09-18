# DepthSearch evidence-completion revision

## Scope

Addresses the saved 300-question run's source-loss, unfinished-candidate,
repeated-route and final-answer rewrite failures. These are mechanism changes,
not a measured performance improvement. No live model, search or judge calls
were made during implementation.

Search limits remain 10 calls and 10 results for all three methods. Fetch,
recursion, turn and context limits are unchanged. RAgent/search-o1 prompts,
runtime policy and response cache version remain unchanged. Only DepthSearch's
response cache version advances to `agent/37-ds-evidence-completion`.

## Changes

- Main prompt tracks supported/contradicted/unknown conditions per candidate.
  It encourages completing promising candidates without waiting for an exhaustive
  candidate universe, then widening coverage. No fixed search/fetch schedule.
- Search/fetch descriptions emphasize useful entry pages and missing conditions.
  Unverified answer values should not become search filters.
- Reader prompt preserves relevant rows, explicit source scope, missing fields
  and useful links. It forbids placeholder instructions in place of evidence.
- DS attaches the supplied source verbatim for compact native PDF/CSV sources
  and Markdown-table pages that fit the reader's existing output-token limit.
  This uses the already filtered, capped reading input. It does not fetch extra
  pages or invoke another model. Larger sources receive an explicit summary-only
  coverage notice; they are not silently reduced to a misleading prefix. This
  does not solve arbitrary long-table extraction.
- The supplement remains separate from model prose and survives child returns
  and the existing page-note cache. Identical content at another URL produces
  a no-progress notice instead of another verbatim supplement. No fuzzy URL ban.
- Normal DS finalization receives the draft, its working synthesis and original
  conversation/tool history. It reviews source support instead of solving again
  from tool results alone. It may still correct unsupported conclusions. Empty,
  malformed or truncated completions retain the recovery path; failed review
  retains a valid draft. Tools remain disabled during finalization.
- Supported cross-source deductions and supported subsets are allowed. Unknown
  attributes are not invented; incomplete coverage is qualified.

## Validation and limits

- 76 offline unit/integration tests passed, including 11 new regressions for
  source rows, recursive/cache handoff, size/truncation, repeated content, draft
  review, recovery, and baseline behavior.
- Replayed q00344's saved 10,776-character reader input with a fake summarizer
  that omitted later rows. Alabama, Florida and Georgia survived in the source
  supplement with no extra fetch or generation call. Token counting in this
  offline replay uses the test double, not a live tokenizer/model evaluation.
- Main and reader system prompts are 246 and 259 whitespace-delimited words.
- Raw supplements increase input tokens on qualifying pages. Existing context
  limits still apply. Finalizer review is not a guarantee against answer drift.
- Candidate completion and route changes remain model policies, not a claim
  that every relevant page will be read or every set item verified.

## Run

```sh
python test.py --limit 300 --method depthsearch --tag ds_evidence_completion
```

For a short check, replace 300 with 30. The DS response-cache version change
prevents reuse of responses from the previous implementation; baselines need
not be rerun for this diagnostic comparison. Evaluate zero/partial/full rates
for set questions alongside mean F1, and inspect whether returned rows actually
lead to completing missing conditions.
