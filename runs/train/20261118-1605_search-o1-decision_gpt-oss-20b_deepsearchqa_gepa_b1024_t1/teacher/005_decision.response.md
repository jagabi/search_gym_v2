The costliest error was in Example 5, Searches 1 and 8 ("1996 women's all-around gold"). The top-ranked excerpt was a block of table rows for ranks 8–21 (0.89 and 0.87). Those rows came from the right table but did not contain the winner. The excerpt with the gold medalist's row ranked lower (0.77 and 0.78), so the main model never received the answer.

A related error appeared in Example 5, Searches 4 and 7. A Wikipedia page of menus, contents and headers (0.25) outranked an excerpt stating that no women competed that year (0.23). That absence statement was the actual answer to the sub-question.

The current instruction rewards excerpts that look like the right source, meaning the same page, table or topic. It does not require the needed fact to actually appear in the excerpt. It also does not count negative facts as evidence. The revision fixes both without growing much longer.

```
Does this excerpt itself state a fact that helps answer the original question, considering the search query? Partial facts, candidate identities, connecting relations, and explicit statements that something did not happen or does not exist all count. Coming from the right page, table, list or topic is not enough: rows or entries that leave out the specific item the question needs, and navigation, menus, headers or download links, do not count. Judge source facts only; the query is not evidence.
```