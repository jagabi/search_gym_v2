# JEV: cross-parent link score audit (2026-10-07)

## Scope

All 300 current responses and explorer forests were examined. Scoring/source data use only the final run.start segment of each trace. The forest contains 2,559 returned search trees (6 of 2,565 search attempts did not produce trees), 4,735 successful entry roots and 42,613 successful nodes. The 58,587 attempted tree nodes include failed fetches and duplicate-content nodes.

## What is labelled

For the 44 judged-correct questions, identify pages where the gold name/value (including documented spelling/date variants) appears in both the saved reader input and its output. These are observed answer-candidate/value exposure paths, not proof that each page independently satisfies every clue, not causal attribution of the final answer, and not exhaustive human relevance labels for every page. Ignore q240 Instagram/SEO topic-title mentions and use its substantive Wikipedia biography as first evidence instead. Within a search, use lowest depth then successful-root order; all such results are returned together, so this is not wall-clock first arrival.

42 correct questions have a source-backed reader exposure path. q74 obtains Nicholas Constant from a search snippet; q79 reader says John Human but the saved input did not match John/Johan Human, so both are excluded from the source-backed counts. q680 supports 6,187 (comma variant).

## Root and depth

|Successful root order in the first qualifying search|Questions|
|---|---:|
|1|34|
|2|6|
|3|2|

Root order is among successfully fetched entry pages, not raw search-engine rank or the first search in the entire question.

|First qualifying page depth|Questions|
|---|---:|
|1|33|
|2|5|
|3|4|

The 9 expansion-first questions are 351, 374, 391, 516, 598, 756, 761, 946 and 1120. Later searches can also reach some of their answer candidates directly; this audit does not assume those later searches would be unchanged if an early branch were removed.

## Pooled-rank diagnostic

At each existing depth, take each observed parent’s top 5 links by stored JEV link score, pool them, and deduplicate identical URLs by the maximum score. A path survives this ranking test only if every edge falls within the pooled top N at its own depth. Ties are shown as guaranteed/possible bounds. This is a static score-ranking test on the observed forest, not a replayed agent run: a changed expansion policy would discover different parents and links, with unknown fetch failures, and later search queries could change.

|Global N per depth|Expansion-first paths retained, of 9|
|---|---:|
|3|6|
|6|6–7|
|9|9|

Top 3 loses the recorded first paths for q351, q946 and q1120. Top 6 loses q351 and q1120; q946 depends on the 0.22 tie. Top 9 retains the nine paths in the observed forest. This is not an accuracy estimate, and the small positive sample does not establish score calibration.

## Individual expansion-first paths

|Question|Gold|Search|Root|Depth|Edge score → parent-local rank → pooled rank (top5/parent)|
|---|---|---:|---:|---:|---|
|351|Cultural Analytics|5|2|2|0.54 → 4–5/69 → 7–8/10|
|374|Kyle Wohlmut|3|1|2|0.36 → 1/16 → 1/5|
|391|Bedford|9|1|2|0.60 → 1/54 → 1/15|
|516|Peter King|2|3|2|0.64 → 1–2/98 → 1–2/15|
|598|Romanian Statistical Review|2|1|3|0.45 → 1–3/114 → 1–3/15; 0.43 → 1/112 → 2/14|
|756|The Perfect Mother|9|1|2|0.57 → 1/12 → 1/6|
|761|Kirsten Kaschock|1|1|3|0.50 → 2/30 → 2/9; 0.53 → 2/42 → 3/18|
|946|Sharon Olds|3|1|3|0.22 → 2–3/34 → 6–7/15; 0.56 → 2–3/47 → 3–4/33|
|1120|Andre Jarju|3|2|3|0.43 → 2/72 → 2/10; 0.28 → 4–5/93 → 7–8/21|

## Concrete adverse examples

q660 (incorrect final answer, gold Ablade Glover): the third root is October Gallery’s El Anatsui page. Its Artists link scores 0.34, local rank 2/24 but pooled rank 8/12. Following Artists then Glover (0.57, local rank 2, pooled rank 2/34) reaches the correct person. The original source and reader confirm Ghana/UK/USA training and founding Artists Alliance Gallery. Higher-scoring competing links include an exhibition URL alias (0.80), Bottle_cap (0.58), Volta_Region (0.41), and Aluminium_recycling (0.35). Global top6 would remove the bridge before Glover can be discovered.

q946 (correct): Jane Hirshfield → National Book Critics Circle Award for Poetry → Sharon Olds. The first link scores only 0.22, local rank 2–3 but pooled rank 6–7. The second scores 0.56, pooled rank 3–4. This is an observed case where a low-scored bridge reveals a better candidate one hop later. Other parents’ Jane Hirshfield content sits above the bridge; this demonstrates pruning risk, but does not distinguish calibration error from ordinary relevance prediction error or ambiguity in the parent context.

q516 (correct): third root IMDb film page → full cast (0.64; pooled rank 1–2) → Peter King Nzioki, Policeman 1. This is a counterexample to the claim that cross-parent scores have no useful ordering: the useful link from the third root still ranks highly.

q680 (correct): third root Greek Theatre (Los Angeles) Wikipedia page directly supplies 6,187. Reducing to only the highest-ranked root would omit this exposure in that search.

## Broader sensitivity check

Across all observed source-backed reader answer occurrences in correct questions (including repetitions and mere mentions), there are 127 distinct expansion edges: 75 from depth1 parents and 52 from depth2 parents. Pooling top5 per parent, global top9 retains 66–67/75 depth1 edges; global top27 retains 51/52 depth2 edges. Some losses come from top5 candidate truncation itself: the old policy can fetch rank6 after failures/duplicates. These broader counts are lexical exposure sensitivity, not independent verified answer paths or changed accuracy.

## Conclusion and next experiment

Raw scores have useful ordering but should not be treated as calibrated success probabilities. Pure pooled top3/top6 pruning removes known useful paths, especially bridges away from an initially wrong candidate. Retain branch diversity when allocating an unchanged fetch budget. Candidate designs include parent-local rank reservations with tie/failure handling and global score ordering only for discretionary slots; their exact reservation sizes should be checked against these paths before live testing. An alternative is preserving the current first expansion and experimenting only with later allocation. Neither design is established superior by these observational logs.

Do not infer a new-policy accuracy or a depth4/5 benefit from this audit: unvisited destinations are unobserved. Next, compare a defined policy on mixed cases including q660/q946 (fragile bridges), q516/q680 (third-root value), and q374/q391 (successful direct links), holding actual fetch attempts and reader budget fixed. Code for the agent has not been changed.

## All first exposure paths

|Question|Gold|Search|Root|Depth|Page|
|---|---|---:|---:|---:|---|
|8|White Mischief|2|1|1|https://www.imdb.com/name/nm0705535/|
|40|AUG 26 1999|3|1|1|https://worldathletics.org/athletes/kenya/tegla-loroupe-14289238|
|57|Vanderbilt clinical oncology research career development award|1|2|1|https://pmc.ncbi.nlm.nih.gov/articles/PMC7227421/|
|117|2019|1|1|1|https://www.atlasobscura.com/articles/ministers-treehouse|
|128|Bacon, bubblegum, cinnamon and wasabi.|2|1|1|https://carlingwooddental.com/blog/the-evolution-of-floss/|
|131|World Of The Dream Merchants|7|1|1|https://sarockmusic.com/rock-legends/rock-legends-artists/the-dream-merchants/|
|240|Queen Marie of Romania|8|1|1|https://en.wikipedia.org/wiki/Marie_of_Romania|
|351|Cultural Analytics|5|2|2|http://lab.culturalanalytics.info/|
|366|AND1|1|1|1|https://khalhon.com/blogs/community/sample-story?srsltid=AU7gw4WjqB4mb1jlcmM2WMzJzpt3rUTOigvX9maqqu9_1yfjgclBEGZ-|
|374|Kyle Wohlmut|3|1|2|https://thecorrespondent.com/678/concrete-is-one-of-the-most-polluting-materials-in-the-world-heres-how-we-can-make-it-sustainable|
|386|5TB|1|1|1|https://www.pcgamer.com/how-i-game-dean-dodrill/|
|391|Bedford|9|1|2|https://norval.co.za/benoni-is-a-town-in-ekurhuleni-municipality-gauteng-south-africa/history-of-benoni/|
|392|Alexander Yarin|2|2|1|https://mmnl.lab.uic.edu/events/rakesh-prasad-sahu-successfully-defends-his-phd-dissertation-titled-fluid-mechanics-of-nano-textured-coalescing-filters/|
|400|Evangeline Walton|3|1|1|https://en.wikipedia.org/wiki/Clifford_Furnas|
|415|Hsiang Sing Naik|1|1|1|https://pmc.ncbi.nlm.nih.gov/articles/PMC6702735/|
|439|Tiziano Ferro|6|1|1|https://english.elpais.com/people/2023-09-22/singer-tiziano-ferros-difficult-moment-the-singer-announces-his-divorce-from-victor-allen-and-explains-the-nightmare-that-prevents-him-from-taking-his-children-to-italy.html|
|492|Asamoah Gyan|1|1|1|https://www.scribd.com/document/933919320/Asamoah-Gyan|
|516|Peter King|2|3|2|https://www.imdb.com/title/tt0387131/fullcredits/?ref_=tt_ov_ql_1|
|596|Ramesh Badal|9|1|1|https://president.gov.np/attorney-general-of-nepal-mr-ramesh-badal-resigns/|
|598|Romanian Statistical Review|2|1|3|http://www.revistadestatistica.ro/|
|599|Hermann Göring|3|1|1|https://www.whastingsburke.com/hermann-goering/|
|601|Amman|10|1|1|https://en.abouna.org/content/terra-sancta-college-amman-school-%E2%80%9Chas-left-nobody-behind%E2%80%9D|
|666|Prague|2|2|1|https://www.academia.edu/61786897/City_Primeval_New_York_Berlin_Prague|
|680|6187|1|3|1|https://en.wikipedia.org/wiki/Greek_Theatre_(Los_Angeles)|
|685|Lola's Cafe|7|1|1|https://www.tripadvisor.com/Restaurants-g294265-zfd19955-Singapore-Wings.html|
|756|The Perfect Mother|9|1|2|http://aimeemolloy.com/about-the-perfect-mother-book|
|761|Kirsten Kaschock|1|1|3|https://rescuepress.co/news/2015/10/13/2015-black-box-poetry-prize-results|
|771|Secretary|4|1|1|https://balletrising.com/2021/03/03/zama-dance-school/|
|905|Robert Pfaff & Robert Henzi|3|1|1|https://herculeswatches.com/brand-history-hercules-hp/|
|946|Sharon Olds|3|1|3|https://en.wikipedia.org/wiki/Sharon_Olds|
|972|23/01/1989|4|1|1|https://iorr.org/talk/read.php?1,1348623601,newer|
|975|March 1910|3|1|1|https://en.wikipedia.org/wiki/Francis_Lodowic_Bartels|
|1000|Americano|3|1|1|https://www.clevescene.com/news/where-i-hang-paulius-nasvytis-owner-of-the-velvet-tango-room-4172887/|
|1013|Rick|1|2|1|https://www.bookpage.com/interviews/23243-nicole-chung-biography-memoir/|
|1014|Dickson Mounds Museum|3|1|1|https://www.propublica.org/article/repatriation-nagpra-museums-dickson-mounds-museum|
|1047|Francesca Biancani|1|1|1|https://www.unibo.it/sitoweb/francesca.biancani/publications|
|1100|70%|2|1|1|https://www.seashepherdglobal.org/latest-news/siso-reduction-illegal-fishing/|
|1105|Illusion|5|1|1|https://www.imdb.com/title/tt0085051/episodes/|
|1120|Andre Jarju|3|2|3|https://www.cricbuzz.com/profiles/35479/andre-jarju|
|1154|Giusewa|1|1|1|https://www.museumfoundation.org/historic-sites/jemez/|
|1196|Thiruvananthapuram|1|1|1|https://www.facebook.com/groups/ThiruvananthapuramOfficial/posts/2518747081663732/|
|1230|Regal Cinema|10|1|1|https://en.wikipedia.org/wiki/Regal_Cinema|


## Follow-up source correction (page-score audit)

Direct source inspection confirms q79: PDF OCR spells Johan as “J ohan Human”. The lexical screen excluded this legitimate source hit. Including it gives 43 source-backed first paths: roots 1/2/3 = 35/6/2, depths 1/2/3 = 34/5/4. The nine expanded first paths and their pooled-rank results are unchanged. The earlier tables above preserve the explicitly stated lexical-screen result.
