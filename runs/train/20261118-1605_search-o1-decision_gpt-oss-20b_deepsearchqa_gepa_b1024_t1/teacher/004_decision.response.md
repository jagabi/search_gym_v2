The costliest error is the excerpt that matches the query's words but concerns the wrong entity, year or kind of item, ranked above the excerpt that names real candidates. Two cases show it:

- **Example 1, Search 9:** a reference list of Mercury and lunar papers (0.47) outranked the excerpt naming the Swift and Voltaire craters on Deimos (0.24). Those two craters are part of the expected answer.
- **Example 1, Searches 3 and 6:** lunar crater tables listing only scientists approved in 1973 scored 0.6–0.7. They match the query's terms but contain no literary namesakes.
- **Example 4, Search 10:** a Gary airport station page (0.71) outranked the correct O'Hare station page (0.49).

The new instruction asks for facts about the question's specific targets. It counts candidates that may meet the question's conditions. It excludes keyword overlap, citation lists, and records about a different entity or period.

```
Does this excerpt state a fact about the specific things the original question asks for: a name, value, date, or connection for the right entity, place and period? Partial facts and candidate items that could meet the question's conditions count. Text that only shares words with the query, lists references, or describes a different entity, place, year or kind of item does not. Judge source facts only; the query is not evidence.
```