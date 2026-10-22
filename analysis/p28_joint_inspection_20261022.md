# p28: single inspection gate and joint evidence/link evaluation

Scope: raw beam traversal. No live model, Jina, search, judge or benchmark calls were made.

## Runtime flow

1. Existing search-result entry ranking admits up to six initial pages.
2. Fetch this depth's pages. Each gate receives only page_title and page_text; the entire JSON state is counted with the configured d3 tokenizer and capped at 4096 tokens. Depth 1 uses the search title (Reader title fallback); deeper pages use the Reader title.
3. One inspect_value key estimates the chance of finding relevant source facts OR concrete onward routes. No per-link keys or separate expansion decision at this gate.
4. Rank passing pages by inspect_value, floor .15. Inspect at most frontier_width=2 distinct bodies per depth; exact-body dedup can backfill a slot.
5. Preserve the existing Docling chunks, overlaps and document routing tree. Routing criteria now include potential source facts OR concrete links. Routing state also has only page_title and page_text.
6. Evaluate selected full bundles with direct_answer, query_answer and link_N keys together. Complete state <=4096, including title, JSON escaping and marker conversion. Rebundle existing chunks as needed for state overhead; no atomic rescoring. Original unmodified bundle text remains the evidence returned to the main model.
7. Destinations are stored locally; state has no outgoing_links, URL, navigation_path, section_path, search_lead or selected_sources. Self/visited/duplicate links are filtered before questions. Link IDs bind scores to destinations inside the local bundle callback. Valid partial scores survive missing response keys.
8. At most 300 link judgments per page, shared across its observed bundles. Keys beyond the cap are not issued and get page_link_budget diagnostics. Requests contain <=64 keys and run with the existing shared concurrency of four. For a single state with 120 eligible links, two evidence keys plus 120 link keys produce packets of 64 and 58.
9. Links survive even if the bundle fails the evidence floor. Each inspected parent nominates branch=2 links; frontier_width=2 children enter the next depth. Depth=3 and fetch_budget=10 remain in force.
10. After traversal, select final evidence source documents with direct_reads=1/query_reads=1 and reads=2 total, using observed bundle evidence scores. Quota exhaustion no longer stops navigation. Final rendering reuses scored bundles with existing output limits.

## Budget semantics

- reads now records actual inspected documents. inspected_pages makes that meaning explicit.
- evidence_pages records final evidence source selections; direct_reads/query_reads count their respective final quotas.
- The same frontier_width currently limits inspections per depth and next-depth visits. This is visible in raw policy metadata.
- Default visits can be 6+2+2, with at most 2+2+2 body inspections. This can inspect more bodies than the old two-read terminal policy. No runtime or accuracy improvement is claimed.
- Legacy best_first/progressive paths retain their own behavior; this update targets configured raw beam.

## Offline verification

119 raw/native regressions checked: 118 passed in the broad run; the remaining regression's obsolete read-count expectation was updated to distinguish 50 inspections from six evidence sources, and its focused rerun passed. Tests cover one-key gate, title selection, minimal state, complete-state token limits, shared source multi-key packets, 120-link packet splitting, cross-bundle 300-key cap, exact-body dedup, visited filtering, bridge-only routes, depth barriers, partial failures, source URL preservation, document routing, native PDF/CSV and final output.
