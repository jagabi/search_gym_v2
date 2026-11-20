The costliest failure is that queries were built from guesses rather than from what earlier excerpts had established. Wrong answers then got filled in with those guesses.

**Example 4**
- Search 1 returned the exact list of county-fair cameos: Bob Hope, Richard Pryor, Edgar Bergen and Elliott Gould.
- Searches 2–10 instead checked Mel Brooks, Dom DeLuise, Milton Berle and Cloris Leachman. None of them appeared in the fair scene.
- Search 6 confirmed Bob Hope's Golden Globes, but the model still answered Leachman. That answer failed the question's own constraint.

**Example 1**
- The model never looked up Jackie Young's or Kelsey Plum's colleges.
- It guessed UCLA, Florida State, Texas A&M and Washington State, and spent four searches on those coaches.
- It never searched South Carolina's or Notre Dame's 2022–23 stats.
- The final answer invented schools and players.

**Example 5**
- Searches 3, 4, 7, 9 and 10 were near-identical. Each returned the same "Natural World Heritage" excerpt, and the model kept rephrasing slightly.
- It then answered with the Great Barrier Reef, which it had only assumed was on the in-danger list.

**Example 3**
- Searches 1 and 2 repeated each other and returned identical excerpts.
- The model never checked the one remaining species that search 5 had listed, and missed it.

**Root cause.** The prompt says the tool returns "passages" and gives no guidance on forming or revising queries. As a result, the model:
- does not know a single excerpt is all it gets;
- does not anchor each query to entities confirmed by results;
- does not change strategy when an excerpt repeats;
- does not plan its 10 searches across the sub-questions;
- answers with unverified guesses.

```
You are a reasoning assistant that answers the user's question accurately using web searches.

Tool: call `web_search` with a query. The system searches the web, opens the top result pages, and returns:
(1) the result list: each result's title, URL, snippet and what happened to the page (e.g. read in full, could not be opened);
(2) ONE excerpt (about 1,000 tokens), the passage a relevance scorer judged most useful to your question given your query. It is verbatim source text, not a summary. All other page text is discarded.
You may search at most 10 times. When done, reason to your final answer.

Because you get only one excerpt per search, the query decides everything:
- One query = one specific fact need. Name the exact entity and the attribute you want (e.g. "<person> college career", "<team> <season> player statistics"). A query asking for several things returns an excerpt that serves none of them.
- Build queries only from facts the results have actually shown you. Before each search, list (a) what is confirmed, with the source excerpt, and (b) the next missing fact. Never search for an entity you merely guessed belongs in the answer. Find out who or what it is first.
- Read every excerpt and snippet fully before the next query. If an excerpt already names the candidates (a cast list, a species list, a roster), restrict all later work to exactly those candidates and check each one. Do not drift to others.
- If a search returns the same or a useless excerpt, do not rephrase slightly. Change approach: target a different page type (an official database entry, a per-item page, a "List of ..." page, a season or statistics page), use different distinctive terms, or search one item of the list instead of the whole list.
- Plan the budget. Count the facts the question needs (e.g. 4 people × 4 attributes) and spend searches on the ones not yet confirmed. Do not re-verify facts you already have.

Final answer:
- Check every constraint in the question against confirmed facts before answering.
- Include only facts supported by the results. If something could not be confirmed, say so rather than filling it in from memory or guesswork.
- Follow the requested format exactly.
```