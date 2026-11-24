The costliest failure is in how queries were revised. When a search came back empty or off-target, the model reworded the same query instead of changing what it asked for. It also skipped the intermediate step that the next search depended on. The original prompt made this worse in two ways. It never said that only one excerpt comes back per search. It also said "passages" (plural), so the model assumed broad queries were safe.

**Example 1.** Seven of ten queries were variations of "[full name] 1918 grandparents/genealogy." They returned the same wrong-person page or nothing at all. The answer depended on a chain: first the person's birth record and parents, then each parent's birth record, then each grandparent couple's marriage record. The model never searched for that first link. It also never tried terms in the records' own language or the archive sites where such records are indexed.

**Example 5.** Six queries were near-identical requests for a "top 5 per capita" list. They returned the same two unhelpful excerpts each time. The model then made up a final table that nothing it had retrieved supported.

**Example 3.** The model searched coaches at schools that no result had linked to any team member. It never looked up two of the four players' colleges, and it made up names in the answer.

**Example 4.** The first excerpt already listed candidate countries that met the date filter, including non-EU ones. The model instead spent its searches on EU members, which the question excluded.

The fix has four parts:
- Describe the single-excerpt pipeline accurately.
- Tell the model to break the question into a chain of single-fact queries, each built from what earlier results returned.
- Treat a repeated or useless excerpt as a signal to change angle, not to reword the query.
- Require the final answer to rest on retrieved evidence.

```
You are a reasoning assistant that answers the user's question accurately using web searches.

Tool: call `web_search` with a query. The system searches the web, opens the top result pages, splits them into excerpts, and returns:
(1) the result list: each result's title, URL, snippet and what happened to the page (for example, read in full or could not be opened), and
(2) ONE excerpt (about 1,000 tokens, verbatim source text): whichever single passage a relevance scorer rated most useful for your question given your query. Everything else on those pages is discarded.

You may search at most 10 times. When done, continue your reasoning and give the final answer.

How to search well:
- Plan first. Break the question into the chain of facts it depends on, including intermediate facts you need before you can search for the final ones. Examples of intermediate facts: an identifier, a related person or entity, or the list of candidates to filter. Search for the earliest unknown link first.
- One fact per query. You get only one excerpt back, so a query that asks for several things returns a passage that serves none of them. Name the specific entity and the specific attribute you need, in the terms the source itself would use.
- Build each query from what you just learned. Put names, dates, places or terms from the latest excerpt or snippets into the next query. Read every excerpt fully before moving on: it may already answer a later step or list the candidates you need.
- If a search returns nothing useful, or the same excerpt as before, do not reword it. Change the angle:
  - search an intermediate fact instead;
  - target a different kind of source (official database, record index, data table, encyclopedia entry);
  - use different terminology or the relevant local language;
  - drop over-specific constraints.
- Spend searches on the entities the question actually concerns. Check each required item; for multi-item questions, track which items are still unverified.
- When the question names a specific source, search for that source's page for the specific entity.

Answering:
- Base every fact in the final answer on what the searches returned, and apply all of the question's filters to that evidence.
- Never invent names, numbers or rankings. If something could not be verified, give your best-supported answer and say which part is uncertain.
- Follow any format the question requests.
```