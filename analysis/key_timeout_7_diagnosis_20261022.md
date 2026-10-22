# D3 key-timeout run: first seven completed questions

Run: `20261022-1354_jevtree_gpt-oss-20b_browsecomp_raw_browser_key_timeout_10`.
The eighth question is excluded. No production edits or network experiments were performed for this diagnosis.

3/7 correct (42.9%); total 2665.1 seconds; 48 searches; 980 attempted decision HTTP requests.
24 decision failures: 19 overall timeouts and 5 remote disconnects. Eight timeouts were link-only packets;
four were entry judgments, and seven were bundle packets containing evidence questions.
81/256 fetch attempts failed, including 69 HTTP 422 and four HTTP 503 failures.

| Question | Correct | Seconds | Searches | Deepest visit | Inspections at depth 1/2/3 | Searches returning no evidence |
|---|---|---:|---:|---:|---|---:|
| 40 | yes | 149.8 | 4 | 1 | 7/0/0 | 0 |
| 57 | no | 680.1 | 10 | 3 | 8/3/1 | 5 |
| 117 | yes | 115.3 | 4 | 2 | 2/0/0 | 3 |
| 326 | no | 403.2 | 10 | 2 | 10/0/0 | 4 |
| 366 | yes | 156.8 | 3 | 3 | 5/1/0 | 0 |
| 516 | no | 815.9 | 7 | 3 | 11/8/2 | 0 |
| 598 | no | 344.0 | 10 | 2 | 6/0/0 | 8 |

## 516: positive answer clue fetched and selected, then cancelled by another page

Gold answer: Peter King. Answer submitted: Donald Sumpter, explicitly born 1943 despite the question requiring the 1970s.
The current search also drifted to Robert Schwentke instead of verifying the Kinsey director clue.

Search ID `96dbaedf8d924ad9ba3669eae8600726`, query `Tim Donohue policeman The Constant Gardener`:
- Metacritic credits contains `Peter King Nzioki — Policeman 1` in fetched content and in actual d3 state.
- Metacritic preview inspect_value = 0.3632788598; it was selected for full bundle inspection alongside Wikipedia's film page.
- Its bundle 0 had 123 questions, split into 64 and 59 keys. Bundle 1 had 140 questions, split into 64/64/12.
- At question elapsed 592.6882s, Wikipedia film bundle 0 emitted return_now = 0.5277997559.
- At 592.6894s, Metacritic's first 64-key packet was cancelled after 25.831s in HTTP; the other packets did not finish.
- The search returned the film page, not the Metacritic cast evidence.

This is a concrete race between sufficient-looking evidence and a slower source. It is not a fetch failure,
not an initial preview rejection and not a timeout of the gold packet. Mixed link/evidence packets make
link-rich cast pages slower. Repeated Donald Sumpter filmography returns then reinforced an incorrect candidate.
The concurrency cleanup worked mechanically; the semantic stopping decision and the material discarded by it did not.

## 57: plausible target article found but inaccessible; irrelevant papers survive selection

Gold funding award: Vanderbilt clinical oncology research career development award.
Searches identified Satya Das and the four-author 2019 article, DOI `10.1080/17474124.2019.1685381`, PMC7227421.
PMC, publisher and DOI fetches failed with Reader HTTP 422. The gold funding sentence was not present in fetched bodies.
Five other source bundles were returned, including 2024/2025 studies and an unrelated funding passage from a 2024 arXiv paper.
The last three searches used reader URL strings as search queries, yielding no source evidence.
There was one bundle timeout (4 keys/13s); it does not establish that the award was lost to timeout.

## 326: unsupported city restriction and eventual constraint abandonment

Gold title: Baby. Answer submitted: There it is: Baja!.
An initial broad tallest-buildings search returned a list. Subsequent searches repeatedly constrained the author's city
to Chicago and guessed 1972/1973 before establishing the person. The two hobbies were not used to recover the candidate.
After ten searches the answer admitted that birthplace, hobbies and occupations had not been verified.
There were no D3 timeout errors for this question (two remote preview disconnects).
Depth 2 was visited but zero depth-2 pages were selected for full inspection.
This is principally query/constraint handling, not evidence lost to the new timeout.

## 598: exact-looking PDF lead inaccessible, then finalization accepts a research plan

Gold publication: Romanian Statistical Review. Submitted answer: `Let's quickly search:`.
Searches 2 and 3 surfaced `https://www.revistadestatistica.ro/wp-content/uploads/2014/01/RRS_10_2013_a1en.pdf`.
The snippet explicitly matched `HDS test (Table 3 in Appendix)`. Native fetching failed with HTTP 503 and later ConnectError.
Eight of ten searches returned no source evidence. Subsequent queries guessed Warsaw/Sofia before moving to Iasi.
After search exhaustion the first finalization response was a plan, but was accepted as a final answer without the second attempt.
In SearchAgent._salvage, `_looks_like_unfinished_research` is applied only to depthsearch or answer_only mode;
this jevtree finalization did not receive that check. The final output failure was consequently mislabelled `finalized`.

## Priorities supported by these observations

1. Revisit return_now semantics and handling of already admitted, competing source evidence; avoid turning generic
   query-level confirmation into immediate cancellation of a source containing the exact requested role/entity relation.
   Waiting for every document would reintroduce the latency problem, so compare bounded completion of admitted evidence work
   with changing which evidence justifies termination. Neither has been implemented here.
2. Treat evidence and link latency together: a cast page with 123+ keys becomes disadvantaged in a race against a short page.
   Combining all keys reduces HTTP count but can delay answer-bearing evidence.
3. Apply finalization validity checks consistently across methods; don't accept an unfinished plan as a nonempty answer.
4. Identify and preserve discriminating original constraints in decision prompts and query planning. PPLX transport
   can improve latency, but cannot by itself restore a missed birth-year, actor-role, city, article or funding relationship.
5. Keep access failures distinct from model relevance failures. No additional fetch workaround was added.

Key-only D3 timeouts are not a complete latency model: tiny packets can share a four-request wave/server with large packets.
The timeout tightening caused real lost judgments, but cannot explain all four wrong answers. Exact accuracy impact
requires a controlled comparison and was not inferred from this one run.
