The costliest error was in Example 1, Searches 3 and 10. Excerpts about the right team but the wrong subject outranked or tied excerpts holding the requested figures:
- **Search 3:** A narrative paragraph tied (0.68) with a 2022–23 stats table, and the narrative was passed on. The table actually held the answer: totals from which the points and rebounds per-game leaders follow (Aaliyah Edwards; Dorka Juhász on a per-game basis).
- **Search 10:** A table of season assist leaders (rank 1, 0.69) beat an excerpt giving a 2022–23 points-per-game figure.
- **Search 7:** A current-season stats page with the wrong year took the top spot (0.75) for a 2022–23 question.

In each case the model rewarded excerpts that matched the team and the word "statistics" or "leaders" over ones with the requested value for the requested period. A milder version appears in Example 3, Searches 4–6. Award facts about an actor from a different scene scored around 0.65, although he did not meet the question's county-fair condition.

The new instruction requires a fact to match the entity, time period and attribute asked about. It also states that tables and lists count, and that background facts do not.

```
Does this excerpt state a source fact that helps answer the original question, considering the search query? Partial facts, candidate identities, connecting relations, and figures in tables or lists count. The fact must match the entity, time period and attribute the question asks about; facts for a different year or season, a different statistic, or a candidate that fails the question's conditions, and general background on the topic, do not count. Judge source facts only; the query is not evidence.
```