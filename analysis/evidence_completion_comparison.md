# ds_evidence_completion: matched 300-question comparison

All four runs have identical question IDs, question text, gold answers and categories.
Scores below include empty answers as zero; no answers were regenerated or regraded.
All use gpt-oss-20b, the same configured Gemini judge, and 10 searches / 10 results.
Source: `evidence_completion_comparison.json`; reproduce with
`python analysis/compare_evidence_completion.py`.

## Overall

| Metric | RAgent | search-o1 | Previous DS | New DS |
|---|---:|---:|---:|---:|
| Mean F1 | .3919 | .4424 | .4148 | .4406 |
| F1 = 0 | 135 | 124 | 151 | 134 |
| 0 < F1 < 1 | 102 | 102 | 63 | 80 |
| F1 = 1 | 63 | 74 | 86 | 86 |
| Mean precision | .4292 | .4622 | .4538 | .4719 |
| Mean recall | .4030 | .4713 | .4144 | .4438 |
| Empty answers | 1 | 0 | 2 | 13 |

New DS gains .025821 over previous DS and .048718 over RAgent; it remains
.001754 below search-o1. Set-question partial-credit recovery is visible, but
neither preservation of every old success nor superiority to search-o1 follows.

## Answer type

| Metric | RAgent | search-o1 | Previous DS | New DS |
|---|---:|---:|---:|---:|
| Single (119): F1 | .3319 | .3725 | .3838 | .4118 |
| Single: zero / partial / full | 79 / 1 / 39 | 74 / 2 / 43 | 73 / 1 / 45 | 70 / 0 / 49 |
| Set (181): F1 | .4314 | .4883 | .4352 | .4596 |
| Set: zero / partial / full | 56 / 101 / 24 | 50 / 100 / 31 | 78 / 62 / 41 | 64 / 80 / 37 |

The remaining mean-F1 deficit against search-o1 is in set questions. DS still
has more set-question perfect answers, but more zeroes and fewer partial answers.

## Paired transitions, previous DS to new DS

| Previous result | New zero | New partial | New full |
|---|---:|---:|---:|
| Zero (151) | 110 | 21 | 20 |
| Partial (63) | 10 | 43 | 10 |
| Full (86) | 14 | 16 | 56 |

41 previous zeroes become positive; 24 previous positives become zero. Of the
86 previous perfect answers, 56 remain perfect and 30 regress; 30 other questions
become perfect. The same total of perfect answers does not imply stable successes.

Of the previously targeted 75 questions where a baseline scored positive and
DS scored zero, 34 now score positive (19 partial, 15 full). Across all questions,
baseline-positive/new-DS-zero cases fall from 75 to 59, including new regressions.

| New DS compared with | Higher F1 | Same F1 | Lower F1 | Mean delta | Paired bootstrap 95% interval |
|---|---:|---:|---:|---:|---:|
| RAgent | 87 | 149 | 64 | +.0487 | [-.0019, +.0989] |
| search-o1 | 77 | 149 | 74 | -.0018 | [-.0533, +.0488] |
| Previous DS | 68 | 177 | 55 | +.0258 | [-.0210, +.0727] |

20,000 paired question-bootstrap samples with fixed seed. All intervals include
zero. These intervals describe question sampling only, not generation/search/judge
variability. This is the same dataset used for diagnosis, not held-out confirmation.

## Categories (mean F1)

| Category | N | RAgent | search-o1 | Previous DS | New DS |
|---|---:|---:|---:|---:|---:|
| Arts | 22 | .4564 | .4783 | .5772 | .5461 |
| Education | 25 | .3800 | .3204 | .3640 | .3689 |
| Finance & Economics | 25 | .3465 | .4538 | .2492 | .4733 |
| Geography | 25 | .3670 | .5002 | .3920 | .3845 |
| Health | 25 | .2927 | .2302 | .1992 | .2638 |
| History | 24 | .5331 | .5384 | .6451 | .5556 |
| Media & Entertainment | 23 | .2081 | .3819 | .3485 | .3130 |
| Other | 24 | .2883 | .3717 | .2722 | .2620 |
| Politics & Government | 25 | .5757 | .5638 | .5779 | .4638 |
| Science | 25 | .4599 | .3748 | .4222 | .4967 |
| Sports | 15 | .5114 | .6386 | .4018 | .5004 |
| Technology | 18 | .4528 | .5960 | .5952 | .6878 |
| Travel | 24 | .2778 | .4243 | .4109 | .5082 |

Category samples are small; these are descriptive changes, not established
domain-specific causal effects. Finance contributes the largest net F1 gain.

## Cost and completion

| Metric | RAgent | search-o1 | Previous DS | New DS |
|---|---:|---:|---:|---:|
| Searches / question | 8.47 | 6.70 | 7.81 | 7.91 |
| Recorded fetch attempts / question | 4.66 | 55.07 | 10.98 | 16.87 |
| LLM calls / question | 15.94 | 53.20 | 34.45 | 42.06 |
| Total input tokens (million) | 90.64 | 211.83 | 132.99 | 189.18 |
| Total output tokens (million) | 1.53 | 19.16 | 7.40 | 8.03 |
| Median latency (seconds) | 120.75 | 1064.40 | 352.40 | 478.15 |
| Reached turn 40 | 2 | 0 | 6 | 64 |

Latency is descriptive: runs occurred at different times, with deployment/cache
differences. Fetch-attempt counters are recorded attempts, not unique successful
network downloads; cached note reuse and refusals must not be confused with new
evidence. The input-token increase cannot be attributed solely to raw supplements:
main turns and calls also increased.

All 13 new empty answers stopped with `max_turns` at turn 40. Each trace shows
two final-answer attempts with empty raw text, `finish_reason=stop`, and no salvage
exception. Thus the saved `judge_errors=13` are `empty_response`, not evidence of
13 judge-service failures. This does not identify why the model returned empty text.
The 287 nonempty answers have mean F1 .4606, but excluding failures is not a fair
headline comparison; the benchmark result remains .4406 / 300.

## Previously inspected cases: scores only, not causal validation

- q00123: 0 -> 1; q00158: 0 -> .75; q00255: 0 -> 1; q00583: 0 -> 1.
- q00374: 0 -> .4.
- q00344, q00687, q00838 remain zero; implementing the proposed mechanism did not
  automatically solve these end-to-end cases.
- Previous positive controls q00073: 1 -> 0; q00364: 1 -> .6667.

Next diagnosis should separate the 40-turn/empty-finalization path from the 30
previous full-answer regressions and the remaining set-question zeroes. No runtime
code or prompts were changed during this statistical comparison.
