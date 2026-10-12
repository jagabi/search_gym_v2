# LDS depth 6: two-question diagnostic

5 starting roots when available; top 5 children per parent; depth 6; 40 logical fetch attempts per search. Local Jina, RPM pacing off, up to 50 simultaneous requests per session. Original main/reader/JEV scoring prompts retained.

Selected cases, not a random accuracy sample. Historical runs differ in queries, date and transport; timing differences cannot be attributed to LDS alone.

| Question | Run | Correct | Searches | Fetch attempts | Seconds | GPT input tokens | JEV input tokens |
|---|---|---:|---:|---:|---:|---:|---:|
| 392 | LDS | 1 | 3 | 81 | 646.1 | 156,335 | 310,386 |
| 392 | search_o1 | 1 | 4 | 19 | 321.2 | 172,920 | 0 |
| 392 | old_jev | 1 | 3 | 84 | 1069.4 | 187,074 | 419,037 |
| 660 | LDS | 0 | 10 | 360 | 2069.4 | 790,211 | 1,620,026 |
| 660 | search_o1 | 1 | 9 | 74 | 1722.9 | 1,232,376 | 0 |
| 660 | old_jev | 0 | 8 | 323 | 4610.1 | 677,191 | 1,294,820 |

## Actual traversal

Peak simultaneous logical fetches across the run: 10. LDS schedules one candidate per root per round, so a single five-root search does not fill the 50-request transport cap.

| Question | Search | Fetches | Max fetched depth | Max discrepancy phase | Reader pages | Complete |
|---|---:|---:|---:|---:|---:|---|
| 392 | 1 | 40 | 6 | 1 | 5 | True |
| 392 | 2 | 1 | 1 | 0 | 1 | True |
| 392 | 3 | 40 | 6 | 1 | 6 | True |
| 660 | 1 | 40 | 6 | 1 | 6 | True |
| 660 | 2 | 40 | 6 | 1 | 6 | True |
| 660 | 3 | 40 | 6 | 1 | 6 | True |
| 660 | 4 | 0 | 0 | 0 | 0 | True |
| 660 | 5 | 40 | 6 | 1 | 6 | True |
| 660 | 6 | 40 | 6 | 1 | 6 | True |
| 660 | 7 | 40 | 5 | 1 | 6 | True |
| 660 | 8 | 40 | 6 | 1 | 6 | True |
| 660 | 9 | 40 | 6 | 1 | 6 | True |
| 660 | 10 | 40 | 6 | 1 | 6 | True |

## Observations

- q392: correct advisor Alexander Yarin was already present in a depth-1 Mathematics Genealogy result in search 3. The search still used all 40 fetches and descended into the advisor genealogy. This case does not demonstrate a depth-6 accuracy gain.
- q660: search 1 returned largely Warren Buffett and other unrelated roots but still spent 40 fetches. Searches 3, 5, 6 and 7 repeatedly targeted Yusuf Grillo Pavilion, including changes to the year.
- q660 final answer: Bruce Obomeyoma Onobrakpeya; gold: Ablade Glover. LDS answered 1/2 correctly, matching old JEV on these cases; historical search-o1 answered 2/2.
- q660 search 8: on the depth-2 MoMAA artist directory (node n0026), JEV ranked https://momaa.org/icons-african-art/ablade-glover/ seventh at 0.32. Top-5 candidate retention excluded it from LDS. Merely retaining more candidates would not fetch them all, but retaining rank 7 does not guarantee it would be visited within 40 attempts.

## Next changes to consider (not implemented)

1. Separate the retained candidate list from the fetch budget: preserve all ranked links and let the scheduler spend the same fixed budget. Revisit alternative order before assuming this guarantees more coverage.
2. Add the previously proposed query-answer objective and evaluate stopping when the narrow query has been answered. The current full-question direct_answer score cannot reliably identify completion of an intermediate query.

## Artifacts and validation

- [Action-by-action SVG viewer](lds_viewer/index.html): question/search selector, previous/next, zoom, SVG original, structure link.
- [Full machine-readable summary](lds_summary.json): root allocation, depth/discrepancy counts, durations and reader notes.
- Each question's lds/<search_id>/ contains actions.jsonl, structure.json and pages/. Trace files retain raw fetch text plus JEV and model requests/responses.
- Completed search actions replay to the exact final node state. Logical fetch budgets and depth limits are checked.
- 74 tests passed across LDS, JEV, reader integrity and fetch-session checks; browser controls and SVG loading verified.

Logical fetch timings include tool work, native document handling and retries; not pure Jina service time. Concurrency uses UTC action timestamps. Historical runs have different transport and queries.

For this first run, use UTC timestamps or per-search actions.jsonl elapsed_ms for LDS timing. The running process used per-search elapsed_ms in trace LDS action entries; subsequent code uses search_elapsed_ms there so global trace timing remains consistent. Non-LDS trace events were unaffected.
