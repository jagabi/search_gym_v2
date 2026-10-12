# LDS + local Reader diagnostic

Configuration: 5 successful starting roots when available, top 5 link candidates per
parent, depth 6 (search results are depth 1), 40 logical fetch attempts per search.
Main search budget and JEV/reader prompts remain unchanged. Page evaluation at
depth 6 is retained for reader selection; outgoing links are not evaluated there.

LDS uses sibling rank only. Every non-first child costs one discrepancy; all
starting roots have discrepancy zero. Discrepancy limits increase from zero.
At equal limit, alternatives near the root come first. Ties retain original
candidate order. Starting roots are reserved before descending, with remaining
search results replacing failed/duplicate roots. Each round schedules at most
one new candidate per active root. Fetch and JEV operations run concurrently
within their stages, with a round barrier before the next deterministic selection.

The 40-attempt limit includes fetch failures and duplicate bodies, but excludes
URLs skipped because they were already reserved/visited. It counts tool fetch
attempts, not transport-level retries. Content/URL deduplication is shared across
searches within each question. No absolute expansion-score threshold is applied.

Local transport: `JINA_BASE_URL=http://100.111.87.95:3001`, `JINA_RPM=0`,
`JINA_MAX_CONCURRENT=50`, `JINA_TIMEOUT_S=60`. HTTP/HTTPS are selected from the
base URL. The 50-request cap is shared by all questions in one Runner/MCP session;
independent processes have independent caps. Native-document handling remains.
Hosted API authentication is not sent to the local server. Default pacing remains
available when using the hosted endpoint without an explicit zero RPM setting.

## Run exactly the two diagnostic questions

```powershell
python test.py --method jevtree --benchmark browsecomp --path data/browsecomp/test_lds2.json --limit 2 --tag lds_d6_local50_2q --no-cache
```

The dataset contains only q392 and q660, selected from the previously inspected
cases. These are behavioral diagnostics, not an accuracy estimate.

## Saved structure

- Existing `trace.jsonl`: full JEV request/response bodies, raw fetch text before
  token truncation, model/reader output, and LDS events.
- `lds/<search_id>/actions.jsonl`: append-only actions, UTC timestamps, per-search
  elapsed time, counters and node deltas. Recoverable even if interrupted.
- `lds/<search_id>/structure.json`: atomic snapshots of settings, query, final
  node states, candidate ranks/scores, parent/root IDs, discrepancy counts, timing,
  selected readers, notes, errors and actions.
- `lds/<search_id>/pages/<node_id>.md`: fetched document after the standard agent
  filtering/token cap, including failed and duplicate responses.
- `explorer.json`: existing tree schema plus a complete `lds` field per search.

To render or refresh **all actual actions**, including from an active run:

```powershell
python -m searchgym.lds_visualize runs/test/<run-folder>
```

Open `<run-folder>/lds_viewer/index.html`. Select a question/search; use previous,
next, arrow keys or the action number. Each frame is a standalone SVG. Pending
siblings are collapsed as `+N`, with the active sibling list shown separately.
No future nodes are used when rendering earlier frames. Open the SVG original
for full-resolution viewing of dense forests.

This does not implement the earlier proposed query-answer objective split.
It isolates the LDS traversal and local fetch changes while retaining the reader.
