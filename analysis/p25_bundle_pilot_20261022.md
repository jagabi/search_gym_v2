# p25: final evidence units are 4096 d3 tokens

## Scope and source provenance

Live calls were restricted to the configured `vllm-sr/d3-mini` System One endpoint.
Original source bodies, original benchmark questions and the actual queries that
retrieved them were extracted from saved traces. No new web search, Jina fetch,
main-model answer generation or judge call was made. Exact evidence checks are
stored in the pilot case files and used only AFTER scoring, never as model input.

Sources:

- 40: Sporting Heroes, Tegla Loroupe personal-best table: 10,000 metres,
  30:32.03, Sevilla, 26 AUG 1999.
- 57: original manuscript PDF mirror, award in Acknowledgments/Funding:
  Vanderbilt clinical oncology research career development award.
- 366: AND1's own history page, Mixtape promotion and US retail history statement.
- 1196: Urban Sprawl PDF, paragraph linking Thiruvananthapuram to 3.25% growth.

Every pilot folder contains cases.json with full question, actual search query,
source URL, original body and saved-trace provenance, plus per-case input/output
traces, returned text and result JSON. Gold checks establish source-passage
delivery, not correctness of every clue or an end-to-end benchmark answer.

## Default route: same four original documents

Both variants used 4096-token bundles, the same configured d3 tokenizer and
concurrency 4. Baseline retained the p24 atomic rescoring stage; revised reading
stopped at the bundle. Tokenizer/model preparation and initial local chunking are
outside the reported scoring/selection timer. Bodies were prechunked in both.

| Case | Evidence baseline/revised | HTTP baseline/revised | Keys baseline/revised | Selection seconds baseline/revised |
|---|---|---:|---:|---:|
| 40 | yes / yes | 2 / 1 | 8 / 2 | 4.05 / 1.53 |
| 57 | yes / yes | 14 / 6 | 46 / 12 | 141.32 / 35.90 |
| 366 | yes / yes | 6 / 2 | 40 / 4 | 114.56 / 1.84 |
| 1196 | yes / yes | 14 / 4 | 68 / 8 | 324.54 / 3.93 |
| Total | 4/4 / 4/4 | 36 / 13 | 162 / 26 | 584.47 / 43.20 |

Recorded endpoint input tokens: 622488 -> 98926. Returned source tokens:
12060 -> 22752. Larger original passages are now delivered; the downstream
main-model context cost may therefore increase. These sequential single-sample
timings are sensitive to service conditions and are not a full-run speed claim.

Actual largest bundle sizes were 1312, 4055, 4068 and 3948 tokens respectively;
all are below 4096 according to the configured d3 tokenizer. Questions and
decision instructions are additional request tokens, not part of this body cap.

Artifacts: bundle_pilots/p25_atomic_baseline and bundle_pilots/p25_bundle4096.

## Controlled region-routing check and observed repair

All four documents have <=16 bundles and therefore do not activate the default
coarse region tree. To exercise stage 5, only the pilot set min_bundles=1 and
leaf_bundles=2 for cases 57 and 1196. Production defaults remain 16 and 4.

Before the terminal repair, 57 preserved its gold bundle, but 1196 selected
bundles 0 and 2 and discarded gold bundle 1. Its sparse 600-token sample omitted
the population paragraph. Sample direct/query scores were .00876/.02542.

Repair: multi-bundle internal regions retain sampled routing; a singleton leaf
is scored from its FULL <=4096-token body. The original score is carried into
final selection, without a second evaluation and even if cross-request score
cache is disabled. A leaf error remains unknown and is not fabricated as zero.

With identical controlled settings after repair:

| Case | Selected terminal bundles | Evidence returned | HTTP | Keys | Seconds |
|---|---|---|---:|---:|---:|
| 57 | 2, 3 | yes | 5 | 12 | 6.75 |
| 1196 | 0, 1 | yes | 4 | 8 | 3.86 |

1196 gold-bundle direct/query scores became .27849/.85045 when the full unit
was actually shown. This diagnoses an avoidable terminal sampling loss. It does
not establish that higher-level sparse routing never loses useful regions.

Artifacts: bundle_pilots/p25_regions4096 (observed failure) and
bundle_pilots/p25_regions_fixed4096 (same cases/settings after repair).

## Production changes and limits

- `jev_bundle_tokens=4096`, measured by the configured d3 tokenizer.
- Docling's 512-token pieces and existing overlap remain internal representation;
  there are no per-piece d3 calls and no previous/next-piece scoring windows.
- Final selected units are whole scored bundles. Overlaps are merged before
  output budgeting; a unit that does not fit is omitted whole, not cut.
- No unscored neighbor content is appended. Existing output budget and selection
  quotas remain; their units are now bundles. This can affect later main-model
  behavior and is not evaluated by this isolated pilot.
- The comparison cards used for subsequent read decisions preserve whole selected
  units rather than silently dropping units larger than the old 1200-token card.
- Search, page entry, action decisions, link expansion, main-model query drift
  and answer synthesis were outside the live test.

Offline: 128 raw regressions and 4 native-document regressions passed. Added
tests require no atomic scoring, exact whole-unit delivery, no unscored neighbor
expansion, whole-unit output admission and one full terminal evaluation even
with score cache disabled.

Focused d3-only rerun (choose a fresh tag):

```cmd
python analysis/pilot_bundle_reading.py --tag p25_bundle4096_repeat
```

Full diagnostic command, not run as part of this pilot:

```cmd
python test.py --method jevtree --model gpt-oss --benchmark browsecomp --path data/browsecomp/test_diagnostic10.json --split test --limit 10 --tag raw_browser_p25_bundle4096_10 --expect-raw-traversal beam --no-cache
```
