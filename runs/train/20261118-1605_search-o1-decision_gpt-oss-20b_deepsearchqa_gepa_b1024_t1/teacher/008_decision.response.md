The costliest error was in Example 1, Search 4. The excerpt that held the answer was the original DS game's Secret Reports list, giving the Day 5 boss as Cornix Canor. It ranked only 5th, at 0.80. Above it sat guides for the 2021 sequel. Those guides matched the query words "Secret Report" and "Day 5" but described a different game. The same error appeared in Search 3, and only a sequel guide was passed on, so the grade was 0.

The same failure shows up elsewhere:
- **Example 4:** the 2025 edition of the league table outranked the 2022 edition the question asked for.
- **Example 2:** data from other sources (other databases, nominal-GDP tables) outranked the specific dataset the question named.

The current instruction never asks the model to check that the excerpt is about the same item, edition, year and source the question specifies. The new instruction adds that check and says that facts about a look-alike item do not count.

```
Does this excerpt state a fact that helps answer the original question about the exact item, version, year and source the question specifies? Partial facts, candidate identities and connecting relations count. Facts about a similar but different item, such as a sequel, remake, another edition or year, or another dataset, do not count even if the wording matches. Judge source facts only; the query is not evidence.
```