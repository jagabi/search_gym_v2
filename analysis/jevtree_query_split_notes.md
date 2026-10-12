# JEV query/original split — 2026-10-12

Implemented; the ten-question benchmark has NOT been run.

- `direct_answer`: does the visible page explicitly answer the original `question`?
- `query_answer`: does the visible page provide source facts answering `search_query`,
  even if the full question remains unresolved? Replaces `answer_likelihood`.
- Entry and outgoing-link evaluation prioritize the current query, while retaining
  credit for direct evidence answering the original question. One score per link;
  the LDS expansion policy and fetch budget are unchanged.
- Both JEV page evaluation and the free-form reader now receive `question`,
  `search_query`, `page_url`, and `page_text`. No main reasoning or extracted conditions.
- Reader quotas: `jev_reads: 6`, `jev_direct_reads: 2`, `jev_query_reads: 4`.
  Reserve the best two original-answer documents first, then up to four remaining
  query-answer documents. Keep the existing 0.15 eligibility floor for each score.
  Overlap is read once and consumes the direct slot only. Missing eligible documents
  leave slots unused; quotas do not transfer. Both explicit quotas must sum to reads.
- Scores and the objective that selected each reader page are stored in trace/tree/LDS
  logs. Per-question reader_stats includes tree_direct_reads and tree_query_reads.
- JEV cache identity includes the changed prompts, input version and quotas.
  Baseline cache fingerprints continue to exclude JEV-only settings.

Unchanged: five starting roots, five candidates per parent, depth six, forty logical
fetch attempts per search, no new early stopping, local Jina with no RPM pacing and
fifty maximum concurrent requests per session. No new link filtering in this change.

## User-run diagnostic ten

```powershell
python test.py --method jevtree --benchmark browsecomp --path data/browsecomp/test_diagnostic10.json --limit 10 --tag lds_query_split10 --no-cache
```

The diagnostic set mixes five cases all prior methods answered correctly and five
cases only some methods answered correctly. It is not a random accuracy sample.
Run configuration, question timings, GPT/JEV tokens and raw traces are saved as usual.

Generate the per-action SVGs after running (replace the folder with the new run):

```powershell
python -m searchgym.lds_visualize runs/test/<new-run-folder>
```

Validation: 21 offline JEV tests and 6 offline LDS tests passed. No benchmark/model
requests were made as part of this change.
