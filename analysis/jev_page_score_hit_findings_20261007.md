# JEV page-score hit audit — 2026-10-07

## What the two scores mean

- direct_answer: Does the supplied page_text explicitly answer the original question? JEV sees at most the 5,000-token prefix.
- answer_likelihood: Does this possibly truncated page_text suggest the full page may contain the answer?

## Population and definition

The current 300-question run has 42,613 scored nodes and 9,193 selected reader-page events. This audit measures available saved source content, not whether the final main-model answer was correct. Reader inputs may themselves be capped at 32,768 tokens; this does not inspect uncaptured portions of the live page.

All selected reader pages were screened for normalized gold-name/value occurrences. This is only a lexical proxy: incidental numbers and names create false positives; OCR, markdown-separated dates, aliases, and paraphrases create false negatives. The 55 events with direct_answer >= 0.80 OR answer_likelihood >= 0.90 were then reviewed against stored source text. They span 25 questions, with repeated/related pages retained because the metric counts actual reader-page events. These are not 55 independent questions.

Manual source hit means that the benchmark gold name/value is present as a relevant answer fact (for example the requested date, role, composer, capacity, or candidate identity) rather than an incidental string. It does not require each page to verify every identification clue, and is not an independent fact-check of the benchmark gold. No external browsing or paid model calls were used. In high-direct positive cases the answer clue is also present in the JEV prefix.

## Manually reviewed high-score results

|Selection|Reader-page events|Source hits|Hit rate|Questions|
|---|---:|---:|---:|---:|
|direct_answer >= 0.80|41|18|43.9%|21|
|answer_likelihood >= 0.90|38|20|52.6%|18|
|Both thresholds|24|16|66.7%|14|
|direct_answer >= 0.90|3|3|100.0%|2|

The mean direct score in its >=0.80 group is 0.8495, while observed source hit rate is 0.4390. The mean likelihood in its >=0.90 group is 0.9208, while observed source hit rate is 0.5263. These selected-sample results do not support interpreting the numeric scores as calibrated probabilities of actual answer evidence. Different thresholds select different populations; they are not a fair standalone comparison of the two ranking functions. The >=0.90 direct group has only 3 events across 2 questions, including a translated version of the same biography.

## Raw occurrence proxy across all selected pages

490/9193 = 5.33% contain the matched gold string/variant in saved reader input, before the high-score manual corrections. This is NOT the true answer hit rate. 7,034/9,193 (76.5%) selected pages have direct_answer < 0.15, often selected through the likelihood queue.

|Score interval|direct_answer: lexical hits/events|answer_likelihood: lexical hits/events|
|---|---:|---:|
|0.00–0.15|276/7034 (3.9%)|0/3 (0.0%)|
|0.15–0.30|107/1287 (8.3%)|75/2494 (3.0%)|
|0.30–0.50|61/556 (11.0%)|97/3212 (3.0%)|
|0.50–0.70|20/219 (9.1%)|171/2586 (6.6%)|
|0.70–0.90|24/94 (25.5%)|129/860 (15.0%)|
|0.90–1.00|2/3 (66.7%)|18/38 (47.4%)|

## Why high scores miss

- q151: original question requires a person born in Italy in the 1920s. Dalida pages get 0.83/0.88 and 0.87/0.91, despite explicitly stating 1933 and Cairo; gold is Sergio Reggiani. An answer-shaped birth name is mistaken for the requested person’s answer.
- q680: a Greek Theatre guide gets direct_answer 0.88 but gives current capacity 5,870, while the requested historical post-expansion capacity is 6,187. The correct venue is not sufficient to support the requested time-specific value.
- q765: translation/dictionary pages echo a search phrase about hospital attendance and get direct_answer 0.89. They provide no supported gold count 31,547. Query-shaped text is being mistaken for evidence.
- q852: six high-likelihood MIT records name Dimitris Bertsimas (or another advisor) rather than gold Richard C. Larson. Shared institution/year is insufficient to identify the intended thesis.
- q960: Dias/Da Gama monument pages get likelihood 0.90–0.92 while the gold is Magellan’s Cross. Superficial explorer/cross overlap is insufficient.
- q458: a numeric match in a Montenegro tourism PDF is incidental; the actual requested-month growth reported by that source is 21.1%, not gold 5.4%. This page is corrected to a miss in the manual table.

## OCR/date corrections

- q79: the source really says “I am particularly indebted to J ohan Human”. OCR splits Johan, so the previous exact/normalized lexical audit missed it. This is a genuine source hit; the earlier source-backed path count of 42 rises to 43 when this case is manually corrected. The additional path is root 1, depth 1; expanded-path ranking results are unchanged.
- q975: the translated biography has March 13, 1910 split across markdown links. It supports gold March 1910, despite failing the naive contiguous phrase check.

## Implication

Use the values as ranking signals, not proof that a page answers the question and not literal 80%/90% correctness probabilities. Jointly high scores are cleaner in this sample (16/24), but still insufficient for automatic acceptance. Do not globally raise cutoffs based on this positive-tail audit: useful bridge pages often score lower. A concrete next evaluation is to make the short scoring criterion explicitly require the requested fact for an entity consistent with the question’s identifying clues, reject query echoes, and treat explicit contradictions as negative evidence. Re-evaluate both high-score false positives and known low-score useful bridges at the same input/call budget before any 300-question rerun. No production code was modified.

## Reviewed events

|Question|direct|likelihood|Source hit|URL|
|---|---:|---:|---|---|
|40|0.94|0.93|yes|http://www.sporting-heroes.net/athletics/kenya/tegla-loroupe-1560/10-000m-bronze-medals-at-1995-1999-world-championships_a08946/|
|79|0.83|0.93|yes|https://pure.manchester.ac.uk/ws/portalfiles/portal/54573399/FULL_TEXT.PDF|
|131|0.88|0.93|no|https://billyforrest.wordpress.com/tag/the-dream-merchants/|
|151|0.83|0.88|no|https://www.imdb.com/name/nm0197931/bio/?ref_=nmtrv_ov_ql_1|
|151|0.87|0.91|no|https://www.imdb.com/title/tt0416362/|
|240|0.34|0.90|yes|https://www.instagram.com/popular/queen-mary-of-romania/?utm_source=topic_pill|
|366|0.88|0.96|yes|https://www.bizjournals.com/philadelphia/news/2022/08/23/and1-philadelphia-netflix-hot-sauce-professor.html|
|400|0.85|0.94|yes|https://en.wikipedia.org/wiki/Evangeline_Walton|
|445|0.82|0.87|no|https://res.cloudinary.com/itimages/image/upload/f_auto,q_auto/prd/splash_background_images/619c7ba3-69af-4bde-92a1-b3d7e3b6e518|
|458|0.84|0.83|no|https://www.monstat.org/userfiles/file/turizam/dolasci%20i%20nocenja%202014/11/Release%20November%202014.pdf|
|516|0.69|0.90|yes|https://en.wikipedia.org/wiki/Peter_Nzioki|
|582|0.87|0.80|no|https://contemporaryperformance.com/2019/01/28/in-performance-berlin-zvizdal-chernobyl-so-far-so-close-out-there-festival/|
|582|0.80|0.76|no|https://www.onassis.org/whats-on/fast-forward-festival-6/one-emerging-point-view|
|582|0.80|0.74|no|https://www.onassis.org/whats-on/fast-forward-festival-6/one-emerging-point-view/fff6-sudden-rise|
|680|0.81|0.89|yes|https://en.wikipedia.org/wiki/Greek_Theatre_(Los_Angeles)|
|680|0.81|0.72|no|https://washedup.app/guides/a-saturday-at-the-greek-theatre-how-5870-people-end-up-there-and-how-to-be-one-o|
|680|0.88|0.75|no|https://washedup.app/guides/greek-theatre|
|680|0.85|0.78|no|https://www.page-turnbull.com/portfolio-items/greek-theatre/|
|680|0.81|0.82|no|https://www.visitcalifornia.com/experience/greek-theatre/|
|756|0.81|0.91|yes|https://fictionwritersreview.com/interview/an-interview-with-aimee-molloy/|
|757|0.81|0.79|no|https://www.ldshop.gg/blog/nte/mint-best-builds.html|
|765|0.89|0.89|no|https://www.anglais.com/traduire/hospital%20opened%201983%20outpatient%20attendances%202014%2035000%20emergency%20department%202011%2024000|
|765|0.89|0.88|no|https://www.frenchdictionary.com/translate/hospital%20opened%201983%20outpatient%20attendances%202014%2035000%20emergency%20department%202011%2024000|
|852|0.62|0.91|no|http://hdl.handle.net/1721.1/98562|
|852|0.86|0.93|no|http://hdl.handle.net/1721.1/98570|
|852|0.84|0.91|no|http://hdl.handle.net/1721.1/98719|
|852|0.60|0.91|no|https://dspace.mit.edu/entities/publication/70ae3cac-de84-4fb2-8e66-5605250e1d19|
|852|0.84|0.92|no|https://dspace.mit.edu/entities/publication/ed2addc6-9c1f-4c1f-951c-67b67640666e|
|852|0.88|0.94|no|https://dspace.mit.edu/handle/1721.1/98570|
|905|0.81|0.90|yes|https://www.swiss-pavilion.com/members/hercules/|
|960|0.48|0.90|no|https://shs.cairn.info/article/GEN_086_0126/pdf?lang=fr|
|960|0.68|0.91|no|https://www.alamy.com/bartolomeu-dias-monument-at-cape-point-in-the-cape-of-good-hope-nature-image66424069.html?imageid=759619BA-00F7-44DB-87D9-F87683562A5E&pn=2&searchId=ad3f39a76d6edb6906d9e37955e55697&searchtype=0|
|960|0.67|0.90|no|https://www.alamy.com/dias-cross-cape-point-cape-of-good-hope-cape-town-south-africa-original-cross-was-erected-in-1488-by-bartholomew-diaz-the-portuguese-navigator-image545633250.html|
|960|0.74|0.91|no|https://www.alamy.com/dias-cross-cape-point-cape-of-good-hope-cape-town-south-africa-with-a-view-to-cape-point-in-the-distance-original-cross-was-erected-in-1488-by-image545633224.html|
|960|0.71|0.92|no|https://www.alamy.com/stock-photo-dias-cross-at-cape-point-cape-of-good-hope-in-western-cape-south-africa-54464637.html|
|960|0.69|0.92|no|https://www.alamy.com/the-da-gama-padrao-a-monument-to-vasco-da-gama-in-the-cape-point-nature-image7262822.html?imageid=69AC7510-BF21-4F80-A7A9-2C04BE8E941B&pn=1&searchId=8ad7161a6872d888b69818856c7f6061&searchtype=9|
|960|0.70|0.91|no|https://www.alamy.com/the-diaz-padrao-in-the-cape-point-nature-reserve-in-south-africa-image7262830.html?imageid=5EDF9219-D61F-45BE-AE10-8B974352158A&pn=2&searchId=ad3f39a76d6edb6906d9e37955e55697&searchtype=0|
|972|0.89|0.93|yes|https://iorr.org/talk/read.php?1,1348623601,newer|
|975|0.92|0.95|yes|https://en.wikipedia.org/wiki/Francis_Lodowic_Bartels|
|975|0.96|0.96|yes|https://translate.google.com/translate?&u=https%3A%2F%2Fde.wikipedia.org%2Fwiki%2FFrancis_Lodowic_Bartels&sl=de&tl=en&prev=_t&hl=en|
|1013|0.81|0.80|yes|https://www.bookpage.com/interviews/23243-nicole-chung-biography-memoir/|
|1100|0.89|0.93|yes|https://seashe.ph/IllegalFishingReduction|
|1100|0.89|0.93|yes|https://www.facebook.com/seashepherdglobal/posts/goodnews-operation-siso-achieves70reduction-in-illegal-fishingin-calabrian-water/715628160599651/|
|1100|0.88|0.93|yes|https://www.seashepherdglobal.org/latest-news/siso-reduction-illegal-fishing/|
|1105|0.80|0.85|no|https://www.facebook.com/groups/153852248004111/posts/8874001915989057/|
|1105|0.80|0.84|no|https://www.facebook.com/groups/476621670342445/posts/1426554578682478/|
|1105|0.73|0.90|yes|https://www.imdb.com/title/tt0085051/|
|1105|0.80|0.91|yes|https://www.imdb.com/title/tt0085051/episodes/|
|1105|0.82|0.93|yes|https://www.imdb.com/title/tt0085898/?ref_=tt_epspo_ep_1|
|1105|0.81|0.92|yes|https://www.imdb.com/title/tt0641485/?ref_=ttep_ep_2|
|1154|0.62|0.91|yes|https://www.museumfoundation.org/historic-sites/jemez/|
|1176|0.86|0.93|no|https://en.wikipedia.org/wiki/Doom_(1993_video_game)|
|1176|0.84|0.93|yes|https://en.wikipedia.org/wiki/Hexen:_Beyond_Heretic|
|1176|0.71|0.91|no|https://en.wikipedia.org/wiki/The_Getaway_(video_game)|
|1176|0.86|0.92|no|https://en.wikipedia.org/wiki/Tribes:_Vengeance|
