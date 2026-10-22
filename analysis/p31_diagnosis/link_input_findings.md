# Link-score audit: actual inputs, destinations and outcomes

Scope: saved P31 trace requests/results; no model calls, no production edits.
29 targeted scored-link occurrences were recovered. This is a targeted case audit, not a random sample or a global error-rate estimate.

## Confirmed high scores for explanatory pages

### Q516: IMDb identifier explanation versus the actual film record

Source: `https://en.wikipedia.org/wiki/The_Constant_Gardener_(film)`.
Query: `The Constant Gardener policeman character actor police officer 2005`.
Request ID: `b62872519d39486a86eaf7ce6865ee3c`; key `link_32`.

Actual visible source fragment:

```markdown
* [_The Constant Gardener_](https://www.imdb.com/title/tt0387131/) at [IMDb](link_32)
```

Local URL mapping: `link_32 -> https://en.wikipedia.org/wiki/IMDb_(identifier)`.
The actual IMDb film URL is the preceding link on the film title, not the numbered link on IMDb.
It had already been admitted as root n0 and failed Reader access, so it was excluded from candidate questions by visited filtering.
The model did not receive the selected destination URL as part of the question or state; it received the anchor and nearby source text.

Score: 0.8264506892. Actual visit admitted. Destination inspection value: 0.0097915199.
Repeated with later queries: identifier link scores 0.5889703993 and 0.6233853826;
destination preview scores 0.0137235974 and 0.0084687828. These all fail the 0.15 inspection floor.

Confirmed: a Wikipedia identifier definition is repeatedly scored as a strong route to an actor/role lookup.
Inference: neighboring film-record context is attributed to the explanatory link; URL masking and the generic IMDb label
make the distinction unavailable or difficult in the actual model input. This is not proof of the model's internal reasoning.
The source-to-link-key mapping itself matches the recorded destination; no accidental score/URL swapping was identified.

### Q40: World Athletics encyclopedia page versus athlete profile

Source: Tegla Loroupe Wikipedia biography.

```markdown
* [Tegla Loroupe](link_47) at [World Athletics](link_48)
```

Local mapping: link_48 -> `https://en.wikipedia.org/wiki/World_Athletics` (organization description).
The athlete profile is the neighboring link on Tegla Loroupe.
Organization-link scores: 0.6495154461 and 0.9123585246 for two searches.
After actual visits, inspect_value was 0.0715467780 and 0.0564041674.

This repeats the same external-reference sentence ambiguity. The question was ultimately answered correctly,
so it demonstrates wasted navigation, not a sufficient cause of an incorrect final answer.

## Separate cases that should not be labelled the same way

### The Proposition: weak route admitted, not an extremely high link score

From Danny Huston's biography, The Proposition link received 0.1551070894, then 0.1240817272 and 0.1194450477
in later searches. These exceeded the 0.10 floor and survived relative candidate selection.
Other occurrences of the same URL in overlapping source bundles were much lower, e.g. 0.0144598277 and 0.0122706687
in the first search. Current aggregation retains the maximum score for each URL.

The 0.6537065836 previously discussed is the destination bundle's direct_answer score, not its link score.
The confirmed link-selection observation is a low-but-eligible detour promoted by maximum aggregation and a thin surviving frontier.
It is not evidence that the link classifier gave this movie an IMDb-like 0.8 score.

### Danny Huston: high value can be correct for the intermediate query

When the main query is `Sandy Woodrow The Constant Gardener actor`, the source explicitly says
`Danny Huston as Sandy Woodrow`. A 0.6750849135 link score for Danny Huston's biography is reasonable for that query.
The research error is accepting Sandy Woodrow as the requested policeman and retaining a candidate with a conflicting birth year.
Do not classify every route toward the eventual wrong answer as a bad link judgment.

## Conclusions within stage 7

1. Yes, confirmed high-scoring irrelevant/explanatory links exist and consumed actual visits.
2. Strong repeated examples involve the external-reference pattern `[record](record_URL) at [service](definition_URL)`.
   The model receives generic service labels and neighboring record context while the actual destination is masked.
3. Separately, one high occurrence among several low scores survives URL-level max aggregation, and marginally eligible
   links can occupy the beam even with modest absolute scores. These concern how stage 7-3 outputs feed 7-4.
4. None of these observations establishes that replacing those visits would retrieve the gold actor or fix Q516.

The next narrowly scoped comparison should preserve source state and question targets and test whether a link question
that identifies its actual destination can distinguish a record from a definition. No such comparison was run here.
No site-specific URL blacklist, lexical ranking or new tool has been added.
