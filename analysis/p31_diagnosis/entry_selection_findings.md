# Entry selection audit: titles/snippets and final six

Saved P31 ten-question run only; no production changes or model requests.

## Truncation

RawTree applies title<=80 and snippet<=160 local tokenizer tokens. No explanatory comment establishes why those exact limits are necessary.
All 575 candidate leads could be matched to the original search results preserved in tool returns.
No title or snippet differed after RawTree lead construction in this run: zero observed truncations.
Search-engine-provided ellipses are already present upstream and are not evidence of RawTree clipping.
This does not justify retaining the caps; it only means they do not explain this run's failures.

## Final six selection

Each result is independently scored on original-question relevance and current-query relevance, with the full candidate list as comparison state.
For the beam six-entry configuration:
1. Lock two highest original-question entries.
2. Lock two highest current-query entries not already chosen.
3. Score each remaining candidate's entry_gain against those four locked leads.
4. Fill the final two slots with the highest entry_gain values.

No absolute entry relevance/gain floor is applied. The two extra slots are filled whenever enough candidates exist,
even when all gain values are small. Extra-slot selection uses gain alone; it does not combine relevance and gain.
Only the four locked leads are comparison context. The second extra is not rescored against the first extra,
so the two additions are not guaranteed to be complementary to each other.

65 of 66 searches had entry candidates: 575 candidates, 361 selected root visits.
56 searches used the complement stage; 46 changed the selection relative to the pre-complement original/query 3+3 quota list.
This is frequent use of the policy, not a measured error rate.

## Observed problematic opportunities

### Q1196: a plausible alternative artist loses to a literal-query category page

Query: famous artist born in Indore aristocratic family.

An India Culture government-account Facebook lead said `Born in an aristocratic family from Kerala`,
with a snippet naming Raja Ravi Varma. Scores: original .12965, query .15347, gain .09228; excluded.
This is a plausible original-clue alternative to the assumed city, not proof that the page establishes every original condition.

The two added slots went to:
- Instagram popular page `Famous Artist Born In Indore Aristocratic Family`, a reel category repeating the query:
  original .11933, query .13818, gain .22957.
- Instagram reel about Lata Mangeshkar's musical family: original .11167, query .17195, gain .56468.

The alternate-location artist lead is lower in entry_gain than the query-repetition page.
The observed selection does not achieve the prompt's stated aim of preserving candidates that test an unverified location assumption.
Whether the omitted page can actually establish the gold city needs source-content validation; no such request was made here.

### Q516: a complete cast source is omitted by a weak gain comparison

Query: Sandy Woodrow The Constant Gardener actor.

| Lead | Original | Query | Gain | Selected |
|---|---:|---:|---:|---|
| TVGuide Full Cast & Crew | .37143 | .48435 | .00963 | no |
| Spirituality and Practice Film Review | .29871 | .38146 | .01951 | yes |
| IMDb Danny Huston as Sandy Woodrow | .43994 | .50967 | .02624 | yes |

The initial four already include Wikipedia, IMDb's film page, Encyclopedia.com, and Rotten Tomatoes cast/crew.
It is plausible to consider another cast page redundant; however, the system has not fetched those selected sources yet
and cannot know whether they are accessible or include minor roles. The chosen IMDb character source later failed access.
The missing TVGuide cast page's gold-actor contents have not been confirmed. This is a source-access/redundancy tradeoff,
not a proven missed gold answer. The gain values are all small yet the policy makes a mandatory top-two choice.

### Q57: the principal target paper is usually retained

PMC7227421 is selected whenever observed in the candidate list; publisher/DOI article sources are also selected in several searches.
Some publisher duplicates are excluded by gain, but this run's target-paper failure is dominated by actual access failures,
not by a consistent inability to admit the identified article.

## Focused hypotheses for a later pilot

Use compact entry-gain instructions that test whether the actual lead offers an additional identifying route,
including challenges to query assumptions. A query-repetition category title is not an observed new identifying relation.
Check false positives and false negatives on saved candidate sets before changing the selection algorithm.
If addressing the final-two policy, compare gain-only selection to relevance-aware complement selection with the same six-entry budget.
Do not assume that a different domain is complementary or that unvisited duplicate sources are already redundant in accessible evidence.
