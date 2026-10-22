# Remaining-stage audit with stages 5/6 and link scoring held fixed

Scope: actual P31 run; no production changes, no network requests, no rescoring.
This audit treats previously discussed chunking/evidence and link-input work as fixed and examines downstream admission plus upstream/downstream decisions.

## 7-4 admission and 4-4 inspection

Across 66 searches, 93 child visits were admitted:
- 49 entered full source inspection.
- 18 failed document access.
- 26 had a successful document response but inspect_value below 0.15.

Thus 44/93 admitted child visits supplied no full-body inspection opportunity. This does not establish that any was an answer-bearing page.
Current code chooses up to two child URLs before fetching them. It then processes only that next_level.
When fetch or preview rejects those pages, it does not replace them using the remaining links from the previous frontier.
admit() counts failed attempts in the 10-visit budget. A full initial six roots leave four visits for later depths.
There is no retained beam backlog for retrying the third-ranked link after the first two fail the inspection gate.

The per-parent candidate list is already truncated to two before global sorting. This is a second loss point:
the parent's third candidate cannot fill an unoccupied slot if earlier candidates are duplicates or fail.
Whether that third candidate is useful needs a separate trace-level counterfactual; it is not proven here.

There were five depth transitions where both selected slots came from one parent even though another parent had eligible candidates.
That concentration can be intended and is not sufficient evidence to impose parent diversity automatically.

For root pages, 94 candidates passed the preview floor; 59 were selected for full inspection and 35 were not.
These 35 are never reconsidered by beam traversal after their depth passes. Counts include appearances across searches.
They are not 35 proven useful sources. This is a candidate-retention hypothesis at 4-4, not a chunk-scoring defect.

Examples per question:
- Q57: four child visits, three access failures, one body inspection.
- Q1196: 21 child visits, two access failures, eight preview rejections, eleven inspections.
- Q1230: 14 child visits, three access failures, five preview rejections, six inspections.

## Remaining-stage evidence

| Stage | Observed failure | Confidence / limit |
|---|---|---|
| 1-1 / 1-3 | Q1230 uses all ten searches on traffic-hour phrasing; no theatre history/ownership research target | Confirmed by query list |
| 1-2 | Q746 narrows 1930s birth clue to 1938 and Minneapolis/city-council searches without identifying the person | Confirmed restriction; not proof of correct alternative |
| 2-3 / 2-4 | Entry scoring and six-root quota may discard sources | No confirmed gold-source loss attributable to these gates in this audit |
| 3-1 | Q57 has 47 failures in 64 document fetch attempts | Confirmed; request/HTTP failures distinct from low relevance |
| 4-2 / 4-4 | A new preview gate rejects 26 successfully fetched child pages; root width drops 35 above-floor candidates | Confirmed attrition; useful evidence among dropped candidates not established |
| 4-6 / 7-4 | Current frontier ends without revisiting surviving parent alternatives; failed fetches consume visit budget | Confirmed implementation; accuracy gain from retaining alternatives remains a hypothesis |
| 8-1 / 8-2 | Q1196 turns 3.25% Jain religious share into population growth and keeps Indore | Explicit in returned text and final answer |
| 9-1 / 9-2 | Q516 ends after five searches, calls the 1970s premise mistaken and submits a 1962-born candidate | Explicit final-answer contradiction |
| 9-2 / 9-3 | Q1196 emits long working deliberation together with final answer | Confirmed output; independent of a timeout or early return |

## Suggested next isolated structural check

Keep the model scores, source states, chunking and total visit cap fixed.
Replay saved frontier scores with a retained parent-candidate queue: only replace failed/preview-rejected child visits when capacity remains.
Record which additional URLs would be admitted and which currently selected visits must be displaced at a fixed ten-visit budget.
Retaining alternatives alone cannot recover visits once all ten slots are consumed; no claim of free extra coverage.
Because links may gain or lose relevance after visiting a page, an offline replay can audit admission mechanics but cannot establish final accuracy.

Before changing visit limits, determine whether initial six-root downloading consumes budget needed for replacements and whether
above-floor root candidates should compete again after chosen routes produce no progress. These are 2-4/4-4/7-4 allocation decisions.
Do not add site-specific URL filters, lexical ranking or new fetch tools as a response to these observations.
