# P31 PPLX, no early return: diagnostic ten

Run: 20261022-1504_jevtree_gpt-oss-20b_browsecomp_raw_browser_p31_pplx_no_early_return_10.
All observations below come from saved records and traces. No production edits or model experiments were made.

5/10 correct. Sum of question runtime = 2202.5s (36m42.5s); mean 220.25s; median 188.65s.
66 searches, 1717 decision HTTP attempts, 1717 HTTP 200, zero decision evaluation failures.
429 document fetch attempts, 141 failures (32.9%). Forty of 66 searches returned no selected evidence.
108 pages entered full inspection; 45 pages contributed returned evidence; 443 bundles scored; 64 returned.
PPLX input usage = 9,310,222 tokens, corresponding to $0.18620444 at $0.02/M (calculated, not billing-dashboard confirmation).

PPLX HTTP mean 0.760s, median 0.522s, p95 2.413s, max 5.916s.
Queue mean 0.521s, max 2.836s. No return_now key/early-return path remains in this version.

| Index | Correct | Seconds | Searches | Inspections depth1/depth2/depth3 | Empty-evidence searches |
|---|---|---:|---:|---|---:|
| 40 | yes | 86.8 | 3 | 5/2/0 | 0 |
| 57 | no | 187.9 | 10 | 1/1/0 | 9 |
| 117 | yes | 58.2 | 2 | 2/1/0 | 1 |
| 326 | yes | 78.1 | 3 | 1/1/2 | 2 |
| 366 | yes | 124.8 | 3 | 4/2/1 | 1 |
| 516 | no | 189.4 | 5 | 10/5/3 | 0 |
| 598 | yes | 235.1 | 10 | 7/2/0 | 6 |
| 746 | no | 460.4 | 10 | 9/6/6 | 7 |
| 1196 | no | 527.7 | 10 | 9/6/5 | 5 |
| 1230 | no | 254.1 | 10 | 11/4/2 | 9 |

The first seven questions overlap the previous d3 run: 3/7 -> 5/7, runtime 2665.1s -> 960.3s (-64.0%).
326 and 598 improved. Both provider and early-return policy changed; this comparison does not isolate either causal effect.

## 516: wrong navigation and source selection, then explicit premise override

Gold Peter King; submitted Danny Huston. No Peter King/Metacritic answer-bearing source was fetched in this trajectory,
so this is different from the previous run's cancellation of a fetched gold cast page.

Search `The Constant Gardener policeman character actor police officer 2005`, ID d16f8e0ad8c4499c8e65241e9ee027ad:
- IMDb_(identifier), a Wikipedia explanatory page, received link value 0.8264506892 and occupied a depth-2 visit.
- Danny Huston received 0.1719442223 and also entered depth 2.
- From Huston, The Proposition (2005 film) received 0.1551070894 and entered depth 3.
- The Proposition bundle 0 received direct_answer 0.6537065836, query_answer 0.0645521751;
  it took the original-question source quota despite not supplying the requested Constant Gardener policeman relationship.
- Subsequent searches repeated the same film/actor neighborhood. The main model never verified the Kinsey director clue.
- Final answer calls the 1970s premise mistaken, despite stating 1962, misidentifies Sandy Woodrow as a policeman,
  and invents a 2013 film connection. Merely finishing all packets does not fix these semantic errors.

Related stages: 7-3/7-4 navigation; 6-2/6-3 evidence judgment and quotas; 1/8/9 query, constraint interpretation and answer.

## 57: access dominates, repeated queries do not change the research route

47/64 fetch attempts failed. Only two pages were fully inspected and one of ten searches returned evidence.
Nine subsequent query variants mostly repeat 2019, four authors and DOTATATE; the final answer remains attached to
a different article title. Correct article identifiers PMC7227421 and DOI 10.1080/17474124.2019.1685381 occur as
discovery/access leads, but the target award paragraph was not retrieved.
This does not support blaming a lost chunk or an API timeout.

Related stages: 3-1 access; 1-3 candidate/route change; 8-1 article identity.

## 746: partial clues accumulate without reaching a person

Gold Japan. Seven of ten searches return no evidence. The returned evidence identifies Minnesota corn production,
an Ottawa tribal discussion, and Hannibal Hamlin. It does not identify the required person.
Later queries constrain Minneapolis, City Council and 1938 although the original question only supplies a 1930s birth range.
No relevant person-biography passage establishing teenage residence was fetched. Japan substring hits were unrelated
navigation/news/export content and must not be counted as recovered answer evidence.
Depth 3 was genuinely inspected six times, but depth alone did not bridge these clues to a person.

Related stages: 1-1/1-2/1-3 query goal/assumptions; 7-3 navigation toward the missing relation.

## 1196: a numerically matching but semantically different value is accepted

Gold Thiruvananthapuram; submitted Indore. Returned source text says 3.25% follows Jainism.
The final answer explicitly reinterprets this religious-population share as the requested population growth statistic.
It also treats a claim of ten parliamentary terms as satisfying three consecutive terms and asserts unsupported artist identity.
The final text contains approximately 10,055 characters of working deliberation and answer, so output quality remains an issue.

Indore district bundles received direct_answer values around 0.53-0.58 despite failing to establish the requested conjunction.
Partial candidate evidence is intentionally permitted, so these numbers alone do not prove an incorrect probability;
the failure is that mismatched partial evidence dominates the selected route and the main model promotes it into full support.
An unverified Scribd title mentions the gold city and growth rate but scored 0.136 at preview. A title matching the puzzle
does not establish genuine source evidence and is insufficient grounds to lower the global floor.

Related stages: 6-2 relation/metric scope; 8-1/8-2 evidence binding and hypothesis revision; 9-2 answer.

## 1230: ten queries stay on the traffic clue and never test theatre ownership/history

Gold Regal Cinema. Nine of ten searches return no evidence. Queries repeatedly substitute annual/peak/200/205/TomTom,
including an unsupported Chicago hypothesis, but never investigate a locally owned Great Depression cinema near stations,
a museum and a gallery. The one evidence-bearing search returns modern traffic articles about Australia and Washington DC,
which do not establish the requested 2019 record. No relevant Regal Cinema source was fetched.
The 17 inspected pages do not demonstrate successful recall because the upstream research target stayed narrow and unproductive.

Related stages: 1-1/1-3 query target and route changes; 6-2 year/metric scope of accepted evidence.

## Improvements and next checks

326 reached the Fran Manushkin encyclopedia biography, answering Baby; it did not repeat the previous Chicago/title drift.
598 now submitted Romanian Statistical Review. These are observed improvements, not proof of which simultaneous change caused them.

Priority: audit link keys against their actual source paragraphs and destinations, starting with the high-scoring IMDb identifier link
and actor-to-other-film transitions. Then audit evidence keys on exact relation mismatches (actor/role/work and year/metric),
including valid partial/refuting evidence. Avoid a blanket threshold change or a long prompt append based on these ten questions.
Use static log replays to define labeled cases before a narrowly scoped pilot; no such new pilot was run here.

Fetch is now the largest measured component of slow questions: q746 fetch-active union 254.55s versus PPLX-active 114.69s;
q1196 fetch-active union 302.93s versus PPLX-active 133.10s. Intervals can overlap and should not be added as an exact partition.
