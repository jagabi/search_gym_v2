# p22: document opportunity before branch closure

## Saved failure

The p21 diagnostic question 57 finished with an empty answer after 579.4 seconds,
10 searches and 991 d3 judgments. No link expansion occurred (maximum depth 1).
PMC access failed with reader assertion `Expected status code 200 but got 203`.
However, search 8 successfully fetched a PDF mirror of the exact requested paper.
The saved native extraction contains the requested award on PDF page 11:
`Vanderbilt clinical oncology research career development award: 5K12CA090625-19.`
It was never selected for chunk reading or delivered to the main model.

Its preview scores were direct=.0773, query=.2815, return=.5201, expand=.2504.
The old independent action argmax closed it. Europe PMC's metadata was read instead.
This establishes a lost document opportunity, not just an access failure.

## Changes

- Reading questions ask for expected gain from the full document. Source-supported
  document identity can justify inspecting unseen sections; the requested fact need
  not already appear in the prefix. No funding/PDF/site-specific reading rule.
- Query reading, bundle and atomic-chunk judgments retain the original question as
  the goal. Matching words, identifiers or dates in unrelated records is insufficient.
- Beam traversal no longer requests an independent `return_now` score. Eligible
  read and expansion opportunities are considered first; closure is derived when
  neither qualifies. Read/expand ties prefer reading the observed source.
- Admission uses existing config values: document reading uses `jev_floor=.15`,
  expansion opportunities use `jev_link_floor=.10`. These values are unchanged,
  but their application to all beam operations is explicit and recorded in policy.
- Spent direct/query quotas are excluded from action and sibling ordering. Reading
  selection is restricted to the current depth, so a previously traversed bridge
  cannot consume the final slot intended for reached documents.
- No forced best-document read below the admission floor. Incomplete preview/action
  judgments are logged as unknown failures, never silently successful closure.
- Read/visit/depth quotas, shared concurrency, main-model tools and p21 section
  routing remain as configured. No new service or main-model action.

## Verification and limits

96 offline RawTree tests passed using synthetic tokenizer, fake d3 and fake documents.
Tests cover the saved PDF opportunity scores, two-document complementary reading,
spent objective quotas, low-gain no-read, depth barriers, unknown failures and p21
section routing. The score replay establishes selection behavior only; it does not
predict new d3 scores. No Jina/d3/main-model/judge request or benchmark was run.

Removing return judgments saves one judgment per formerly scored branch decision.
More reads/expansions can survive, so total time may increase. Existing thresholds
are not calibrated probability guarantees. New prompts may still underrate a correct
document, region or award chunk. Empty main-model final responses are not repaired by
this change.

Server command:

```cmd
python test.py --method jevtree --model gpt-oss --benchmark browsecomp --path data/browsecomp/test_diagnostic10.json --split test --limit 10 --tag raw_browser_p22_read_gain --expect-raw-traversal beam --no-cache
```
