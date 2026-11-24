I use the instruction below for a decision model inside a web-search question-answering pipeline:
```
Does this excerpt provide evidence useful for answering the original question, considering the search query? Partial facts, candidate identities, and connecting relations count. Judge source facts only; the query is not evidence.
```

What the decision model is: a small fine-tuned classifier, not a chat model. It reads an instruction phrased as a yes/no criterion together with one text excerpt, and outputs only the probability that the answer is yes. It follows short, concrete criteria. It cannot follow procedures, examples or output formats.

How it is used: a main model answers a research question with up to 10 web searches. For each search, the top 10 result pages are cut into excerpts of about 1,000 tokens. Every excerpt is scored with this instruction, followed by two lines the system appends:
  Original question: <the research question>
  Search query: <the query just issued>
Only the top-scored excerpt is passed to the main model; the rest are discarded.

The decision model knows none of this. It sees only the instruction, the two appended lines and one excerpt, so the instruction must make sense on its own.

Below are questions the pipeline answered. For each: the expected answer, the grade, and for every search the five top-scored excerpts with their scores.

# Example 1
## Question
Using jw.org as your only source, compare the figures published in the following publications, and tell me which country (excluding those countries that have been removed from up-to-date reporting) saw the greatest overall reduction, by number (not percent) in reported peak publishers, between 2017 and 2023: 2017 Service Year Report of Jehovah’s Witnesses Worldwide, 2018 Service Year Report of Jehovah’s Witnesses Worldwide, 2019 Service Year Report of Jehovah’s Witnesses Worldwide, 2020 Service Year Report of Jehovah’s Witnesses Worldwide, 2021 Service Year Report of Jehovah’s Witnesses Worldwide, 2022 Service Year Report of Jehovah’s Witnesses Worldwide, and 2023 Service Year Report of Jehovah’s Witnesses Worldwide.

## Expected answer
Ukraine

## Grade 0.00

## Search 1 — query: "2017 Service Year Report Jehovah’s Witnesses Worldwide peak publishers country"
### Rank 1 of 70 — 0.72 (passed on)
<excerpt title="2017 Service Year Report - Jehovah's Witnesses">
### 2017 Service Year Report
| --- |  
| Year | Country or Territory | Population | Peak Publishers | Ratio, 1 Publisher to | Average Publishers | % Increase | Baptisms | Average Pioneer Publishers | Congregations | Memorial Attendance |  
| 2017 | Albania | 3,204,000 | 5,637 | 568 | 0 | 2 | 230 | 1,351 | 89 | 11,927 |  
| 2017 | American Samoa | 55,519 | 189 | 294 | 0 | -11 |  | 38 | 3 | 625 |  
| 2017 | Andorra | 72,280 | 178 | 406 | 0 | 9 | 1 | 18 | 3 | 352 |  
| 2017 | Angola | 26,849,678 | 143,322 | 187 | 0 | 12 | 11,758 | 19,631 | 1,913 | 617,099 |  
| 2017 | Anguilla | 17,087 | 81 | 211 | 0 | 3 | 1 | 10 | 2 | 297 |  
| 2017 | Antigua | 91,889 | 485 | 189 | 0 | 1 | 15 | 49 | 7 | 1,398 |  
| 2017 | Argentina | 44,044,811 | 150,823 | 292 | 0 | 1 | 3,962 | 24,676 | 1,999 | 312,070 |
</excerpt>
### Rank 2 of 70 — 0.69
<excerpt title="2017 Service Year Report - Jehovah's Witnesses">
### 2017 Service Year Report
| 2017 | Germany | 82,315,658 | 165,470 | 497 | 0 |  | 2,839 | 13,699 | 2,118 | 267,296 |  
| 2017 | Ghana | 28,833,629 | 135,498 | 213 | 0 | 3 | 6,743 | 15,267 | 2,019 | 340,731 |  
| 2017 | Gibraltar | 32,348 | 124 | 261 | 0 | -4 |  | 17 | 2 | 171 |  
| 2017 | Greece | 10,815,197 | 28,773 | 376 | 0 |  | 510 | 4,201 | 370 | 44,748 |  
| 2017 | Greenland | 55,860 | 173 | 323 | 0 | 3 | 1 | 39 | 5 | 348 |  
| 2017 | Grenada | 117,724 | 569 | 207 | 0 | 1 | 4 | 71 | 10 | 1,446 |  
| 2017 | Guadeloupe | 403,544 | 8,207 | 49 | 0 |  | 198 | 726 | 120 | 19,092 |  
| 2017 | Guam | 159,358 | 726 | 220 | 0 |  | 21 | 142 | 9 | 1,852 |
</excerpt>
### Rank 3 of 70 — 0.69
<excerpt title="2017 Service Year Report - Jehovah's Witnesses">
### 2017 Service Year Report
| 2017 | Sri Lanka | 20,894,716 | 6,165 | 3,389 | 0 | 2 | 194 | 817 | 114 | 14,570 |  
| 2017 | Sudan | 40,533,330 | 703 | 57,658 | 0 | 2 | 16 | 83 | 15 | 2,517 |  
| 2017 | Suriname | 558,368 | 3,106 | 180 | 0 | 3 | 120 | 338 | 55 | 10,237 |  
| 2017 | Swaziland | 1,323,468 | 3,212 | 412 | 0 | 2 | 144 | 302 | 81 | 9,020 |  
| 2017 | Sweden | 9,967,637 | 22,418 | 445 | 0 |  | 293 | 2,391 | 309 | 34,966 |  
| 2017 | Switzerland | 8,420,000 | 19,251 | 437 | 0 |  | 340 | 1,243 | 273 | 31,952 |  
| 2017 | Tahiti | 268,207 | 3,219 | 83 | 0 | 1 | 108 | 515 | 48 | 9,136 |  
| 2017 | Taiwan | 23,556,169 | 10,498 | 2,244 | 0 | 4 | 611 | 3,536 | 169 | 19,545 |
</excerpt>
### Rank 4 of 70 — 0.67
<excerpt title="2017 Service Year Report - Jehovah's Witnesses">
### 2017 Service Year Report
| 2017 | New Zealand | 4,817,903 | 14,150 | 340 | 0 |  | 363 | 1,334 | 187 | 26,735 |  
| 2017 | Nicaragua | 6,223,400 | 29,082 | 214 | 0 | 2 | 1,054 | 4,487 | 491 | 88,198 |  
| 2017 | Niger | 21,563,607 | 316 | 68,239 | 0 | 5 | 6 | 38 | 7 | 866 |  
| 2017 | Nigeria | 190,886,000 | 381,398 | 500 | 0 | 3 | 13,531 | 39,389 | 6,533 | 800,874 |  
| 2017 | Niue | 1,614 | 24 | 67 | 0 |  |  | 3 | 1 | 67 |  
| 2017 | Norfolk Island | 1,748 | 7 | 250 | 0 |  |  |  | 1 | 18 |  
| 2017 | Norway | 5,258,317 | 11,652 | 451 | 0 |  | 214 | 1,064 | 167 | 18,100 |  
| 2017 | Pakistan | 197,015,955 | 1,109 | 177,652 | 0 | 4 | 27 | 99 | 19 | 3,956 |
</excerpt>
### Rank 5 of 70 — 0.67
<excerpt title="2017 Service Year Report - Jehovah's Witnesses">
### 2017 Service Year Report
| 2017 | Guatemala | 17,033,200 | 40,222 | 423 | 0 | 2 | 1,783 | 6,572 | 902 | 96,767 |  
| 2017 | Guinea | 13,371,995 | 929 | 14,394 | 0 | 7 | 55 | 119 | 20 | 3,728 |  
| 2017 | Guinea-Bissau | 1,865,000 | 170 | 11 | 0 | 8 | 5 | 45 | 3 | 745 |  
| 2017 | Guyana | 773,651 | 3,545 | 218 | 0 | 2 | 119 | 500 | 48 | 12,315 |  
| 2017 | Haiti | 9,993,000 | 20,472 | 488 | 0 |  | 1,057 | 2,853 | 290 | 79,415 |  
| 2017 | Honduras | 8,314,200 | 23,106 | 360 | 0 |  | 987 | 4,435 | 445 | 65,718 |  
| 2017 | Hong Kong | 7,389,500 | 5,452 | 1,355 | 0 |  | 454 | 1,041 | 63 | 9,101 |  
| 2017 | Hungary | 9,784,000 | 21,853 | 448 | 0 | -2 | 392 | 1,942 | 295 | 37,831 |
</excerpt>

## Search 2 — query: "peak publishers 2017 2023 Jehovah's Witnesses service year report"
### Rank 1 of 91 — 0.32 (passed on)
<excerpt title="2023 Service Report Grand Totals - A few thoughts... : r/exjw">
# Comments Section
aphantDude
•3y ago• Edited 3y ago
The drop in congregations was mainly due to closing foreign language congregations, covid made it more convinient (worst case just zoom) to merge them and e.g. EU laws made the D2D in foreign languages nearly impossible (no notes allowed at all). And some merged obviously to sell the KH ;) somehow they have to pay the bills.
the unbaptized thing i see it as well, so much kids in some countries (40%+ are 14 or younger in many places in africa) reducing the age increases the publisher count a lot, 2024 could be surprisingly "good" for that reason, but after that they cant do much anymore and the decline will show up (if they dare to even report it continuesly)
Reply  Share
Aposta-fish
•3y ago
In my state I know of several congregations deleted that were major congregations not just foreign language. Also 4 Kingdom Halls sold, I’m sure more but haven’t checked in a couple years. They’re trying hard not to show how many KH’s are up for sale but there’s dozens upon dozens!
Reply  Share
aphantDude
•3y ago
yeah, i know of one in my area as well
not saying there is no trend at all, just saying there have been many foreign language closures esp. in europe, also one problem might be lack of brothers to keep them running
Reply  Share
More replies
More replies
Similar-Historian-70
•3y ago
I've done some calculations and yes, WT is shrinking in the western world. The only growth comes mostly from Africa and some countries in Asia. Europe, Oceania, North and South America is shrinking. In some countries there is increase, like in Germany, but it is only because of migration and refugees from Ukraine. Here are some numbers:
\ Total increase in average publishers over 2022: + 110,059
\ + 119,540 in Africa
\ + 14,722 in Asia
\ - 16,957 in North America+Caribbean
\ - 3,359 in South America
\ - 3,025 in Europe
\ - 355 in Oceania

# Comments Section
\ - 507 in 33 other lands
Yes, the growth in Africa is bigger than total growth worldwide. The growth comes mostly from third world countries, what explains the panic mode of the GB and recent changes and new light. The new publishers in these countries probably wouldn't donate enough money to pay for the CSA court cases.
Reply  Share
[deleted]
•3y ago
Good work similar. Western Europe and the US were stagnant 25 years ago when I left. South America joining the party is a little surprising.
And yes, the third world growth was concerning back then too.
Reply  Share
Wild-Second-7082
•3y ago
Every religious group that does missionary work in Africa touts success as well
Reply  Share
More replies
a-watcher
•3y ago
I am happy to welcome significantly more partakers.
Reply  Share
naenare
•3y ago
I frankly think this is a smoke screen and they are just making numbers up to make it seem not as bad as it actually is. Why would we think they are being in any way truthful? They have always feed us half truths and downright lies.
Reply  Share
Odd-Seesaw
•3y ago
PIMO elder here. I personally believe the cult leaders are reporting what they get from congregations... BUT also they aren't representing the true situation. The source of false info is coming from publishers. Many many many publishers just lie on the report and most elders are fine with that.
In my congregation, the service reports we have basically been flatlined for 5 years (no increase, no decrease). But attendance at meetings at the Kingdom Hall is dismal. It's rare to have more than 1 car group for service.
Reply  Share
naenare
•3y ago
They are covering their asses and lying about CSA and court cases about disfellowshipping, why would the numbers be any different?
Reply  Share
more replies
more replies
more replies
More replies
More replies
Aposta-fish
•3y ago
</excerpt>
### Rank 2 of 91 — 0.21
<excerpt title="2023 Service Report Grand Totals - A few thoughts... : r/exjw">
# 2023 Service Report Grand Totals - A few thoughts...
*   Even with a slight increase in 2023, the number of congregations has decreased by 2,210 from the peak in 2020 (120,387).

*   Average Publishers per congregation is now 73. This continues to increase which means some congregations are getting very large. The congregation where I attended has ~130 publishers.

*   The peak number of congregations occurring in 2020 makes no sense. Congregation mergers were completed in many places during the 2017-2019 time frame. Even in the mid-sized city where I live in the central US, the congregations mergers were completed before the pandemic started. The oddball up and down totals for congregations is further evidence that the data provided by Watchtower in the annual reports is questionable at best and likely just wrong. You can't trust it.
Read more
Share
Allora_Network•Ad
Compete on live volatility, commodities and Hyperliquid predictions. Climb the leaderboard and earn.
Learn More
forge.allora.network
u/ExitLag•Ad
Competitive, Premier or Unrated: play Valorant with a steadier connection.
Sign Up
exitlag.com
Sort by:
Best
Open comment sort options
*   Best   
*   Top   
*   New   
*   Controversial   
*   Old   
*   Q&A

# Comments Section
aphantDude
•3y ago• Edited 3y ago
The drop in congregations was mainly due to closing foreign language congregations, covid made it more convinient (worst case just zoom) to merge them and e.g. EU laws made the D2D in foreign languages nearly impossible (no notes allowed at all). And some merged obviously to sell the KH ;) somehow they have to pay the bills.
the unbaptized thing i see it as well, so much kids in some countries (40%+ are 14 or younger in many places in africa) reducing the age increases the publisher count a lot, 2024 could be surprisingly "good" for that reason, but after that they cant do much anymore and the decline will show up (if they dare to even report it continuesly)
Reply  Share
Aposta-fish
•3y ago
In my state I know of several congregations deleted that were major congregations not just foreign language. Also 4 Kingdom Halls sold, I’m sure more but haven’t checked in a couple years. They’re trying hard not to show how many KH’s are up for sale but there’s dozens upon dozens!
Reply  Share
aphantDude
•3y ago
yeah, i know of one in my area as well
not saying there is no trend at all, just saying there have been many foreign language closures esp. in europe, also one problem might be lack of brothers to keep them running
Reply  Share
More replies
More replies
Similar-Historian-70
•3y ago
I've done some calculations and yes, WT is shrinking in the western world. The only growth comes mostly from Africa and some countries in Asia. Europe, Oceania, North and South America is shrinking. In some countries there is increase, like in Germany, but it is only because of migration and refugees from Ukraine. Here are some numbers:
\ Total increase in average publishers over 2022: + 110,059
\ + 119,540 in Africa
\ + 14,722 in Asia
\ - 16,957 in North America+Caribbean
\ - 3,359 in South America
\ - 3,025 in Europe
\ - 355 in Oceania
</excerpt>
### Rank 3 of 91 — 0.18
<excerpt title="Service Year Reports - Jehovah's Witnesses">
## Did You Know … ?
### 2022 Service Year Report
| 2022 | Turks and Caicos | 40,000 | 352 | 125 | 319 | -5 | 0 | 58 | 7 | 976 |  
| 2022 | Tuvalu | 12,000 | 97 | 245 | 49 | -22 | 0 | 3 | 1 | 210 |  
| 2022 | Uganda | 44,900,000 | 9,262 | 4,942 | 9,085 | 1 | 419 | 1,208 | 167 | 28,907 |  
| 2022 | Ukraine | 41,130,000 | 127,378 | 335 | 122,694 | -4 | 1,941 | 18,592 | 1,429 | 211,528 |  
| 2022 | United States of America | 334,805,000 | 1,238,431 | 272 | 1,230,463 | -1 | 16,200 | 229,730 | 12,040 | 2,344,212 |  
| 2022 | Uruguay | 3,496,000 | 11,960 | 294 | 11,878 | -2 | 193 | 1,885 | 149 | 25,010 |  
| 2022 | Vanuatu | 322,000 | 635 | 530 | 607 | -15 | 19 | 99 | 13 | 3,584 |  

## Did You Know … ?
### 2022 Service Year Report
| 2022 | Venezuela | 28,705,000 | 131,634 | 221 | 130,055 | -2 | 2,758 | 31,316 | 1,714 | 355,695 |  
| 2022 | Virgin Islands, British | 31,000 | 218 | 146 | 213 | -5 | 0 | 30 | 4 | 765 |  
| 2022 | Virgin Islands, U.S. | 104,000 | 592 | 200 | 521 | -2 | 1 | 108 | 8 | 1,289 |  
| 2022 | Wallis & Futuna Islands | 11,000 | 66 | 175 | 63 | 0 | 2 | 6 | 1 | 212 |  
| 2022 | Yap | 12,000 | 34 | 387 | 31 | 0 | 2 | 7 | 1 | 132 |  
| 2022 | Zambia | 18,921,000 | 215,382 | 99 | 191,372 | 5 | 4,770 | 18,034 | 3,529 | 864,131 |  
| 2022 | Zimbabwe | 15,179,000 | 45,582 | 355 | 42,810 | 2 | 730 | 7,190 | 1,036 | 105,824 |
</excerpt>
### Rank 4 of 91 — 0.18
<excerpt title="Service Year Reports - Jehovah's Witnesses">
## Did You Know … ?
### 2022 Service Year Report
| --- |  
| Year | Country or Territory | Population | Peak Publishers | Ratio, 1 Publisher to | Average Publishers | % Increase | Baptisms | Average Pioneer Publishers | Congregations | Memorial Attendance |  
| 2022 | Albania | 2,866,000 | 5,577 | 518 | 5,531 | -1 | 112 | 1,363 | 83 | 12,106 |  
| 2022 | American Samoa | 55,000 | 154 | 420 | 131 | -9 | 0 | 32 | 3 | 647 |  
| 2022 | Andorra | 77,000 | 169 | 461 | 167 | -1 | 0 | 23 | 3 | 331 |  
| 2022 | Angola | 35,027,000 | 159,384 | 226 | 154,953 | 3 | 3,273 | 25,609 | 2,539 | 485,484 |  
| 2022 | Anguilla | 15,000 | 67 | 259 | 58 | 5 | 0 | 11 | 1 | 208 |  
| 2022 | Antigua | 100,000 | 478 | 215 | 466 | 1 | 0 | 41 | 7 | 1,244 |  
| 2022 | Argentina | 47,327,000 | 155,443 | 308 | 153,787 | -2 | 2,869 | 35,977 | 1,945 | 345,669 |
</excerpt>
### Rank 5 of 91 — 0.17
<excerpt title="Service Year Reports - Jehovah's Witnesses">
## Did You Know … ?
### 2022 Service Year Report
| 2022 | Central African Republic | 5,017,000 | 2,661 | 2,053 | 2,444 | 4 | 61 | 265 | 65 | 16,500 |  
| 2022 | Chad | 17,414,000 | 806 | 22,734 | 766 | -1 | 30 | 93 | 22 | 3,501 |  
| 2022 | Chile | 19,829,000 | 86,746 | 230 | 86,316 | 0 | 1,301 | 20,069 | 955 | 218,637 |  
| 2022 | Chuuk | 54,000 | 32 | 2,000 | 27 | -13 | 0 | 8 | 2 | 180 |  
| 2022 | Colombia | 51,513,000 | 188,219 | 278 | 185,586 | -2 | 3,187 | 31,715 | 2,267 | 568,136 |  
| 2022 | Congo, Dem. Republic of | 95,241,000 | 223,678 | 437 | 217,977 | 8 | 5,173 | 20,239 | 4,037 | 1,107,590 |  
| 2022 | Congo, Republic of | 5,798,000 | 8,556 | 707 | 8,200 | 2 | 194 | 1,250 | 116 | 25,093 |
</excerpt>

## Search 3 — query: "countries removed from up-to-date reporting jw.org service year report"
### Rank 1 of 63 — 0.13 (passed on)
<excerpt title="2025 Country and Territory Reports">
| **Myanmar** | 51,317,000 | 5,382 | 9,677 | 5,303 | 2 | 253 | 1,195 | 115 | 5,947 | 10,543 |  
| **Namibia** | 3,093,000 | 3,083 | 1,045 | 2,961 | 6 | 181 | 438 | 54 | 4,490 | 9,736 |  
| **Nauru** | 12,000 | 21 | 800 | 15 | 7 |  | 4 | 1 | 35 | 150 |  
| **Nepal** | 29,876,000 | 3,001 | 10,103 | 2,957 | 3 | 167 | 956 | 62 | 4,189 | 7,756 |  
| **Netherlands** | 18,069,000 | 29,552 | 616 | 29,341 |  | 412 | 3,233 | 333 | 8,218 | 48,179 |  
| **Nevis** | 13,000 | 94 | 167 | 78 | 7 |  | 9 | 1 | 63 | 252 |  
| **New Caledonia** | 265,000 | 2,726 | 99 | 2,688 | 1 | 115 | 359 | 32 | 2,468 | 7,606 |  

| **New Zealand** | 5,331,000 | 14,809 | 364 | 14,652 | 1 | 239 | 1,930 | 169 | 5,375 | 27,066 |  
| **Nicaragua** | 7,008,000 | 29,071 | 243 | 28,880 | 1 | 831 | 5,596 | 440 | 23,237 | 78,226 |  
| **Niger** | 27,918,000 | 385 | 82,112 | 340 | 6 | 10 | 59 | 9 | 442 | 976 |  
| **Nigeria** | 237,528,000 | 421,375 | 589 | 403,535 | 3 | 27,263 | 52,575 | 6,221 | 766,292 | 818,848 |  
| **Niue** | 2,000 | 21 | 105 | 19 |  |  | 3 | 1 | 6 | 47 |  
| **North Macedonia** | 1,826,000 | 1,275 | 1,452 | 1,258 | 1 | 40 | 204 | 22 | 473 | 2,310 |  
| **Norway** | 5,601,000 | 12,096 | 466 | 12,020 |  | 156 | 1,553 | 161 | 3,058 | 17,583 |
</excerpt>
### Rank 2 of 63 — 0.13
<excerpt title="2025 Country and Territory Reports">
| **Central African Republic** | 5,513,000 | 3,705 | 1,563 | 3,527 | 11 | 334 | 511 | 72 | 9,875 | 25,256 |  
| **Chad** | 19,341,000 | 1,082 | 18,705 | 1,034 | 11 | 74 | 138 | 26 | 1,201 | 4,229 |  
| **Chile** | 20,207,000 | 88,664 | 229 | 88,202 | 1 | 1,905 | 21,602 | 1,024 | 37,753 | 185,618 |  
| **Chuuk** | 50,000 | 32 | 1,786 | 28 |  | 3 | 8 | 2 | 59 | 144 |  
| **Colombia** | 52,696,000 | 193,778 | 274 | 192,392 | 2 | 5,895 | 42,653 | 2,341 | 142,088 | 526,568 |  
| **Congo, Dem. Republic of** | 115,685,000 | 306,303 | 389 | 297,215 | 11 | 23,170 | 38,139 | 4,810 | 788,698 | 1,411,774 |  

| **Congo, Republic of** | 6,565,000 | 10,811 | 635 | 10,344 | 8 | 613 | 1,947 | 135 | 26,097 | 33,669 |  
| **Cook Islands** | 17,000 | 209 | 89 | 190 | -2 | 9 | 31 | 3 | 91 | 522 |  
| **Costa Rica** | 5,153,000 | 32,604 | 159 | 32,381 | 1 | 755 | 5,201 | 417 | 17,791 | 67,637 |  
| **Côte d’Ivoire** | 32,712,000 | 14,068 | 2,415 | 13,545 | 6 | 759 | 1,865 | 232 | 22,612 | 52,597 |  
| **Croatia** | 3,874,000 | 4,595 | 850 | 4,560 | -1 | 114 | 467 | 56 | 785 | 7,014 |  
| **Cuba** | 9,748,000 | 83,406 | 118 | 82,835 | -1 | 2,258 | 10,928 | 1,283 | 82,483 | 196,596 |  
| **Curaçao** | 156,000 | 1,930 | 81 | 1,917 | 1 | 35 | 290 | 24 | 1,149 | 4,942 |
</excerpt>
### Rank 3 of 63 — 0.12
<excerpt title="2025 Country and Territory Reports">
| **Senegal** | 19,391,000 | 1,642 | 12,226 | 1,586 | 1 | 49 | 238 | 27 | 1,707 | 3,104 |  
| **Serbia** | 6,586,000 | 3,850 | 1,745 | 3,774 | 2 | 73 | 802 | 59 | 1,232 | 6,817 |  
| **Seychelles** | 122,000 | 417 | 332 | 368 | 7 | 15 | 39 | 5 | 318 | 1,019 |  
| **Sierra Leone** | 8,820,000 | 2,803 | 3,313 | 2,662 | 9 | 170 | 427 | 44 | 5,357 | 9,205 |  
| **Slovakia** | 5,422,000 | 11,267 | 484 | 11,194 |  | 178 | 1,094 | 139 | 2,278 | 20,620 |  
| **Slovenia** | 2,131,000 | 1,735 | 1,244 | 1,713 | -1 | 13 | 293 | 22 | 487 | 2,624 |  
| **Solomon Islands** | 798,000 | 1,814 | 468 | 1,704 | 1 | 76 | 252 | 38 | 1,581 | 11,406 |  

| **South Africa** | 63,101,000 | 107,746 | 600 | 105,117 | 4 | 4,646 | 17,081 | 1,925 | 105,918 | 260,378 |  
| **South Sudan** | 15,787,000 | 2,469 | 6,556 | 2,408 | 14 | 221 | 405 | 37 | 5,252 | 7,992 |  
| **Spain** | 49,316,000 | 127,840 | 388 | 126,954 | 2 | 2,146 | 27,257 | 1,377 | 37,939 | 211,887 |  
| **Sri Lanka** | 21,763,000 | 7,169 | 3,083 | 7,059 | 2 | 135 | 1,359 | 86 | 6,886 | 14,806 |  
| **Sudan** | 51,662,000 | 71 | 771,075 | 67 | -52 | 19 | 7 | 3 | 96 | 160 |  
| **Suriname** | 640,000 | 3,265 | 201 | 3,180 | 1 | 124 | 427 | 54 | 3,049 | 8,796 |
</excerpt>
### Rank 4 of 63 — 0.11
<excerpt title="2025 Country and Territory Reports">
| **Malaysia** | 34,200,000 | 5,740 | 6,024 | 5,677 |  | 278 | 1,660 | 117 | 5,181 | 11,991 |  
| **Mali** | 25,199,000 | 366 | 73,897 | 341 | -6 | 7 | 41 | 6 | 391 | 861 |  
| **Malta** | 545,000 | 883 | 629 | 867 | 3 | 10 | 186 | 10 | 287 | 1,508 |  
| **Marshall Islands** | 37,000 | 154 | 264 | 140 | 7 | 8 | 29 | 4 | 258 | 659 |  
| **Martinique** | 355,000 | 4,825 | 75 | 4,763 |  | 86 | 802 | 54 | 3,053 | 9,981 |  
| **Mauritius** | 1,200,000 | 2,163 | 563 | 2,131 |  | 61 | 354 | 28 | 1,522 | 4,841 |  
| **Mayotte** | 329,000 | 131 | 2,697 | 122 | -15 | 8 | 35 | 2 | 164 | 303 |  

| **Mexico** | 131,947,000 | 887,844 | 150 | 879,024 | 1 | 24,896 | 172,697 | 12,215 | 579,848 | 2,129,826 |  
| **Moldova** | 2,381,000 | 15,513 | 154 | 15,422 | -10 | 407 | 2,200 | 158 | 5,105 | 27,432 |  
| **Monaco** | 38,000 | 46 | 864 | 44 |  |  | 8 | 1 | 16 | 111 |  
| **Mongolia** | 3,545,000 | 469 | 8,002 | 443 |  | 42 | 202 | 8 | 492 | 1,120 |  
| **Montenegro** | 624,000 | 448 | 1,438 | 434 | 5 | 2 | 140 | 8 | 114 | 759 |  
| **Montserrat** | 4,000 | 29 | 148 | 27 | -10 |  | 9 | 1 | 39 | 88 |  
| **Mozambique** | 35,632,000 | 109,531 | 345 | 103,244 | 12 | 10,368 | 14,043 | 2,072 | 177,808 | 405,172 |
</excerpt>
### Rank 5 of 63 — 0.11
<excerpt title="2025 Country and Territory Reports">
| **Equatorial Guinea** | 1,669,000 | 3,132 | 568 | 2,936 | 11 | 277 | 458 | 36 | 7,542 | 8,501 |  
| **Estonia** | 1,370,000 | 4,118 | 334 | 4,097 |  | 45 | 691 | 54 | 1,187 | 6,468 |  
| **Eswatini** | 1,256,000 | 3,519 | 366 | 3,431 | 4 | 166 | 497 | 74 | 4,969 | 8,902 |  
| **Ethiopia** | 133,271,000 | 12,853 | 10,668 | 12,493 | 6 | 723 | 3,590 | 209 | 8,872 | 27,152 |  
| **Falkland Islands** | 4,000 | 9 | 571 | 7 | -30 |  | 5 | 1 | 8 | 18 |  
| **Faroe Islands** | 55,000 | 126 | 451 | 122 | -8 | 2 | 16 | 4 | 54 | 181 |  
| **Fiji** | 901,000 | 3,107 | 306 | 2,946 | 1 | 138 | 600 | 58 | 3,653 | 11,744 |  

| **Finland** | 5,636,000 | 18,366 | 309 | 18,264 |  | 184 | 2,577 | 261 | 6,123 | 25,716 |  
| **France** | 68,668,000 | 140,797 | 492 | 139,548 | 1 | 2,431 | 22,137 | 1,445 | 40,539 | 228,785 |  
| **French Guiana** | 292,000 | 3,045 | 98 | 2,984 | 1 | 96 | 690 | 43 | 4,327 | 10,463 |  
| **Gabon** | 2,420,000 | 5,033 | 498 | 4,862 | 5 | 198 | 829 | 64 | 7,751 | 10,917 |  
| **Gambia** | 2,822,000 | 358 | 8,156 | 346 | 10 | 9 | 67 | 6 | 474 | 761 |  
| **Georgia** | 3,705,000 | 19,523 | 191 | 19,439 | 2 | 533 | 4,021 | 213 | 4,441 | 32,044 |  
| **Germany** | 83,600,000 | 176,478 | 476 | 175,685 |  | 2,860 | 22,874 | 1,954 | 45,600 | 270,177 |
</excerpt>

## Search 4 — query: "2018 Service Year Report peak publishers country jw.org"
### Rank 1 of 208 — 0.42 (passed on)
<excerpt title="Jehovah's Witnesses—2018 Country and Territory Reports">
PLAY
2018 Country and Territory Reports

| Country or Territory | Population | 2018 Peak Pubs. | Ratio, 1 Publisher to | % Inc. Over 2017 | 2018 No. Bptzd. | Av. Pio. Pubs. | No. of Congs. | Memorial Attendance |  
| --- | --- | --- | --- | --- | --- | --- | --- | --- |  
| **Albania** | 2,870,324 | 5,647 | 508 |  | 143 | 1,332 | 93 | 11,866 |  
| **American Samoa** | 55,679 | 194 | 287 | -6 | 8 | 36 | 3 | 682 |  
| **Andorra** | 76,953 | 178 | 432 | -4 | 3 | 16 | 3 | 354 |  
| **Angola** | 27,794,030 | 155,991 | 178 | 9 | 12,215 | 22,994 | 2,111 | 635,980 |  
| **Anguilla** | 17,087 | 67 | 255 |  |  | 11 | 2 | 225 |  
| **Antigua** | 91,889 | 479 | 192 | -1 | 9 | 48 | 7 | 1,337 |  
| **Argentina** | 44,494,502 | 153,342 | 290 | 1 | 4,229 | 24,075 | 1,980 | 312,994 |  
| **Armenia** | 2,986,500 | 10,977 | 272 |  | 262 | 2,213 | 134 | 21,843 |
</excerpt>
### Rank 2 of 208 — 0.39
<excerpt title="Jehovah's Witnesses—2018 Country and Territory Reports">
| **Cayman Islands** | 62,000 | 265 | 234 |  | 3 | 34 | 3 | 620 |  
| **Central African Republic** | 5,000,000 | 2,889 | 1,731 | 3 | 138 | 306 | 56 | 17,622 |  
| **Chad** | 15,000,000 | 847 | 17,710 | 3 | 69 | 76 | 19 | 4,558 |  
| **Chile** | 18,552,218 | 80,451 | 231 | 2 | 2,140 | 13,280 | 1,012 | 177,431 |  
| **Chuuk** | 48,651 | 47 | 1,035 | 10 | 2 | 17 | 2 | 181 |  
| **Colombia** | 49,850,000 | 181,691 | 274 | 3 | 6,482 | 27,657 | 2,243 | 512,386 |  
| **Congo, Dem. Republic of** | 84,004,989 | 229,740 | 366 | 4 | 15,825 | 20,940 | 3,772 | 1,220,046 |  
| **Congo, Republic of** | 5,399,895 | 7,899 | 684 | 8 | 550 | 737 | 88 | 34,550 |  
| **Cook Islands** | 17,411 | 196 | 89 | -3 | 3 | 26 | 3 | 482 |
</excerpt>
### Rank 3 of 208 — 0.38
<excerpt title="Jehovah's Witnesses—2018 Country and Territory Reports">
| **Kiribati** | 118,414 | 150 | 789 | 5 | 9 | 33 | 3 | 557 |  
| **Korea, Republic of** | 51,635,256 | 101,246 | 510 |  | 1,770 | 43,692 | 1,278 | 135,489 |  
| **Kosovo** | 1,798,506 | 262 | 6,865 | -1 | 7 | 110 | 8 | 579 |  
| **Kosrae** | 6,616 | 18 | 368 | -6 |  | 6 | 1 | 82 |  
| **Kyrgyzstan** | 6,256,700 | 5,420 | 1,154 | 1 | 183 | 1,223 | 83 | 10,321 |  
| **Latvia** | 1,925,253 | 2,216 | 869 | -1 | 42 | 328 | 37 | 3,288 |  
| **Lesotho** | 2,269,178 | 4,248 | 534 | 2 | 169 | 517 | 91 | 10,919 |  
| **Liberia** | 4,892,190 | 7,286 | 671 | 3 | 333 | 707 | 141 | 46,011 |  
| **Liechtenstein** | 38,110 | 90 | 423 | -1 |  | 2 | 1 | 132 |
</excerpt>
### Rank 4 of 208 — 0.38
<excerpt title="Jehovah's Witnesses—2018 Country and Territory Reports">
| **Indonesia** | 268,459,957 | 28,283 | 9,492 | 2 | 1,442 | 4,283 | 492 | 58,658 |  
| **Ireland** | 6,632,457 | 7,061 | 939 | 2 | 131 | 1,048 | 120 | 11,842 |  
| **Israel** | 9,055,123 | 1,808 | 5,008 | 7 | 42 | 309 | 31 | 4,179 |  
| **Italy** | 60,457,909 | 251,502 | 240 |  | 4,307 | 37,435 | 2,921 | 417,090 |  
| **Jamaica** | 2,899,000 | 11,425 | 254 | -1 | 315 | 1,522 | 178 | 31,962 |  
| **Japan** | 127,185,332 | 212,802 | 598 |  | 2,050 | 65,890 | 3,025 | 294,296 |  
| **Kazakhstan** | 18,533,849 | 17,507 | 1,059 | -1 | 517 | 3,869 | 261 | 30,809 |  
| **Kenya** | 51,226,537 | 29,860 | 1,716 | 2 | 1,160 | 3,643 | 641 | 73,103 |  

| **Kiribati** | 118,414 | 150 | 789 | 5 | 9 | 33 | 3 | 557 |  
| **Korea, Republic of** | 51,635,256 | 101,246 | 510 |  | 1,770 | 43,692 | 1,278 | 135,489 |  
| **Kosovo** | 1,798,506 | 262 | 6,865 | -1 | 7 | 110 | 8 | 579 |  
| **Kosrae** | 6,616 | 18 | 368 | -6 |  | 6 | 1 | 82 |  
| **Kyrgyzstan** | 6,256,700 | 5,420 | 1,154 | 1 | 183 | 1,223 | 83 | 10,321 |  
| **Latvia** | 1,925,253 | 2,216 | 869 | -1 | 42 | 328 | 37 | 3,288 |  
| **Lesotho** | 2,269,178 | 4,248 | 534 | 2 | 169 | 517 | 91 | 10,919 |  
| **Liberia** | 4,892,190 | 7,286 | 671 | 3 | 333 | 707 | 141 | 46,011 |  
| **Liechtenstein** | 38,110 | 90 | 423 | -1 |  | 2 | 1 | 132 |
</excerpt>
### Rank 5 of 208 — 0.36
<excerpt title="Jehovah's Witnesses—2018 Country and Territory Reports">
| **Taiwan** | 23,570,000 | 10,839 | 2,175 | 3 | 344 | 3,603 | 181 | 20,626 |  
| **Tanzania** | 59,477,688 | 18,705 | 3,180 | 4 | 1,066 | 1,950 | 455 | 58,620 |  
| **Thailand** | 68,414,135 | 5,170 | 13,233 | 6 | 154 | 1,923 | 125 | 10,347 |  
| **Timor-Leste** | 1,324,094 | 366 | 3,618 | 4 | 28 | 82 | 5 | 845 |  
| **Tinian** | 2,500 | 14 | 179 | 8 |  | 1 | 1 | 41 |  
| **Togo** | 7,991,000 | 21,755 | 367 | 3 | 794 | 2,290 | 307 | 64,898 |  
| **Tonga** | 109,008 | 209 | 522 | -5 | 6 | 30 | 2 | 511 |  
| **Trinidad & Tobago** | 1,371,824 | 10,030 | 137 | 1 | 274 | 1,322 | 127 | 24,401 |  
| **Turkey** | 80,810,525 | 3,506 | 23,049 | 13 | 121 | 841 | 47 | 6,275 |
</excerpt>

## Search 5 — query: "removed from up-to-date reporting jw.org countries removed from up-to-date reporting"
### Rank 1 of 94 — 0.11 (passed on)
<excerpt title="2025 Country and Territory Reports">
| **Myanmar** | 51,317,000 | 5,382 | 9,677 | 5,303 | 2 | 253 | 1,195 | 115 | 5,947 | 10,543 |  
| **Namibia** | 3,093,000 | 3,083 | 1,045 | 2,961 | 6 | 181 | 438 | 54 | 4,490 | 9,736 |  
| **Nauru** | 12,000 | 21 | 800 | 15 | 7 |  | 4 | 1 | 35 | 150 |  
| **Nepal** | 29,876,000 | 3,001 | 10,103 | 2,957 | 3 | 167 | 956 | 62 | 4,189 | 7,756 |  
| **Netherlands** | 18,069,000 | 29,552 | 616 | 29,341 |  | 412 | 3,233 | 333 | 8,218 | 48,179 |  
| **Nevis** | 13,000 | 94 | 167 | 78 | 7 |  | 9 | 1 | 63 | 252 |  
| **New Caledonia** | 265,000 | 2,726 | 99 | 2,688 | 1 | 115 | 359 | 32 | 2,468 | 7,606 |  

| **New Zealand** | 5,331,000 | 14,809 | 364 | 14,652 | 1 | 239 | 1,930 | 169 | 5,375 | 27,066 |  
| **Nicaragua** | 7,008,000 | 29,071 | 243 | 28,880 | 1 | 831 | 5,596 | 440 | 23,237 | 78,226 |  
| **Niger** | 27,918,000 | 385 | 82,112 | 340 | 6 | 10 | 59 | 9 | 442 | 976 |  
| **Nigeria** | 237,528,000 | 421,375 | 589 | 403,535 | 3 | 27,263 | 52,575 | 6,221 | 766,292 | 818,848 |  
| **Niue** | 2,000 | 21 | 105 | 19 |  |  | 3 | 1 | 6 | 47 |  
| **North Macedonia** | 1,826,000 | 1,275 | 1,452 | 1,258 | 1 | 40 | 204 | 22 | 473 | 2,310 |  
| **Norway** | 5,601,000 | 12,096 | 466 | 12,020 |  | 156 | 1,553 | 161 | 3,058 | 17,583 |
</excerpt>
### Rank 2 of 94 — 0.09
<excerpt title="2025 Country and Territory Reports">
| **Korea, Republic of** | 51,169,000 | 105,726 | 485 | 105,552 |  | 1,505 | 55,002 | 1,239 | 33,841 | 134,522 |  
| **Kosovo** | 1,586,000 | 277 | 6,030 | 263 | 10 | 5 | 131 | 7 | 275 | 489 |  
| **Kosrae** | 7,000 | 12 | 636 | 11 | 22 | 1 | 5 | 1 | 23 | 36 |  
| **Kyrgyzstan** | 7,282,000 | 5,242 | 1,403 | 5,190 | 1 | 131 | 1,562 | 71 | 2,417 | 9,569 |  
| **Latvia** | 1,857,000 | 2,104 | 894 | 2,077 |  | 28 | 379 | 29 | 714 | 3,188 |  
| **Lesotho** | 2,363,000 | 4,594 | 537 | 4,404 | 7 | 281 | 808 | 83 | 6,086 | 11,900 |  
| **Liberia** | 5,731,000 | 9,225 | 659 | 8,693 | 9 | 661 | 1,241 | 159 | 24,984 | 41,561 |  

| **Liechtenstein** | 40,000 | 108 | 381 | 105 | 3 |  | 11 | 1 | 23 | 166 |  
| **Lithuania** | 2,891,000 | 2,918 | 1,001 | 2,887 |  | 27 | 491 | 39 | 796 | 4,541 |  
| **Luxembourg** | 682,000 | 2,264 | 306 | 2,227 | 1 | 9 | 290 | 32 | 803 | 4,029 |  
| **Macao** | 688,000 | 435 | 1,619 | 425 | 9 | 1 | 139 | 6 | 477 | 859 |  
| **Madagascar** | 32,741,000 | 45,673 | 734 | 44,597 | 7 | 3,014 | 9,091 | 865 | 85,204 | 176,453 |  
| **Madeira** | 259,000 | 1,208 | 216 | 1,199 | 1 | 13 | 188 | 19 | 429 | 1,904 |  
| **Malawi** | 22,216,000 | 127,154 | 192 | 115,535 | 9 | 8,439 | 10,726 | 2,058 | 159,387 | 370,884 |
</excerpt>
### Rank 3 of 94 — 0.09
<excerpt title="2025 Country and Territory Reports">
| **Senegal** | 19,391,000 | 1,642 | 12,226 | 1,586 | 1 | 49 | 238 | 27 | 1,707 | 3,104 |  
| **Serbia** | 6,586,000 | 3,850 | 1,745 | 3,774 | 2 | 73 | 802 | 59 | 1,232 | 6,817 |  
| **Seychelles** | 122,000 | 417 | 332 | 368 | 7 | 15 | 39 | 5 | 318 | 1,019 |  
| **Sierra Leone** | 8,820,000 | 2,803 | 3,313 | 2,662 | 9 | 170 | 427 | 44 | 5,357 | 9,205 |  
| **Slovakia** | 5,422,000 | 11,267 | 484 | 11,194 |  | 178 | 1,094 | 139 | 2,278 | 20,620 |  
| **Slovenia** | 2,131,000 | 1,735 | 1,244 | 1,713 | -1 | 13 | 293 | 22 | 487 | 2,624 |  
| **Solomon Islands** | 798,000 | 1,814 | 468 | 1,704 | 1 | 76 | 252 | 38 | 1,581 | 11,406 |  

| **South Africa** | 63,101,000 | 107,746 | 600 | 105,117 | 4 | 4,646 | 17,081 | 1,925 | 105,918 | 260,378 |  
| **South Sudan** | 15,787,000 | 2,469 | 6,556 | 2,408 | 14 | 221 | 405 | 37 | 5,252 | 7,992 |  
| **Spain** | 49,316,000 | 127,840 | 388 | 126,954 | 2 | 2,146 | 27,257 | 1,377 | 37,939 | 211,887 |  
| **Sri Lanka** | 21,763,000 | 7,169 | 3,083 | 7,059 | 2 | 135 | 1,359 | 86 | 6,886 | 14,806 |  
| **Sudan** | 51,662,000 | 71 | 771,075 | 67 | -52 | 19 | 7 | 3 | 96 | 160 |  
| **Suriname** | 640,000 | 3,265 | 201 | 3,180 | 1 | 124 | 427 | 54 | 3,049 | 8,796 |
</excerpt>
### Rank 4 of 94 — 0.08
<excerpt title="2025 Country and Territory Reports">
| **Central African Republic** | 5,513,000 | 3,705 | 1,563 | 3,527 | 11 | 334 | 511 | 72 | 9,875 | 25,256 |  
| **Chad** | 19,341,000 | 1,082 | 18,705 | 1,034 | 11 | 74 | 138 | 26 | 1,201 | 4,229 |  
| **Chile** | 20,207,000 | 88,664 | 229 | 88,202 | 1 | 1,905 | 21,602 | 1,024 | 37,753 | 185,618 |  
| **Chuuk** | 50,000 | 32 | 1,786 | 28 |  | 3 | 8 | 2 | 59 | 144 |  
| **Colombia** | 52,696,000 | 193,778 | 274 | 192,392 | 2 | 5,895 | 42,653 | 2,341 | 142,088 | 526,568 |  
| **Congo, Dem. Republic of** | 115,685,000 | 306,303 | 389 | 297,215 | 11 | 23,170 | 38,139 | 4,810 | 788,698 | 1,411,774 |  

| **Congo, Republic of** | 6,565,000 | 10,811 | 635 | 10,344 | 8 | 613 | 1,947 | 135 | 26,097 | 33,669 |  
| **Cook Islands** | 17,000 | 209 | 89 | 190 | -2 | 9 | 31 | 3 | 91 | 522 |  
| **Costa Rica** | 5,153,000 | 32,604 | 159 | 32,381 | 1 | 755 | 5,201 | 417 | 17,791 | 67,637 |  
| **Côte d’Ivoire** | 32,712,000 | 14,068 | 2,415 | 13,545 | 6 | 759 | 1,865 | 232 | 22,612 | 52,597 |  
| **Croatia** | 3,874,000 | 4,595 | 850 | 4,560 | -1 | 114 | 467 | 56 | 785 | 7,014 |  
| **Cuba** | 9,748,000 | 83,406 | 118 | 82,835 | -1 | 2,258 | 10,928 | 1,283 | 82,483 | 196,596 |  
| **Curaçao** | 156,000 | 1,930 | 81 | 1,917 | 1 | 35 | 290 | 24 | 1,149 | 4,942 |
</excerpt>
### Rank 5 of 94 — 0.08
<excerpt title="2025 Country and Territory Reports">
| **Malaysia** | 34,200,000 | 5,740 | 6,024 | 5,677 |  | 278 | 1,660 | 117 | 5,181 | 11,991 |  
| **Mali** | 25,199,000 | 366 | 73,897 | 341 | -6 | 7 | 41 | 6 | 391 | 861 |  
| **Malta** | 545,000 | 883 | 629 | 867 | 3 | 10 | 186 | 10 | 287 | 1,508 |  
| **Marshall Islands** | 37,000 | 154 | 264 | 140 | 7 | 8 | 29 | 4 | 258 | 659 |  
| **Martinique** | 355,000 | 4,825 | 75 | 4,763 |  | 86 | 802 | 54 | 3,053 | 9,981 |  
| **Mauritius** | 1,200,000 | 2,163 | 563 | 2,131 |  | 61 | 354 | 28 | 1,522 | 4,841 |  
| **Mayotte** | 329,000 | 131 | 2,697 | 122 | -15 | 8 | 35 | 2 | 164 | 303 |  

| **Mexico** | 131,947,000 | 887,844 | 150 | 879,024 | 1 | 24,896 | 172,697 | 12,215 | 579,848 | 2,129,826 |  
| **Moldova** | 2,381,000 | 15,513 | 154 | 15,422 | -10 | 407 | 2,200 | 158 | 5,105 | 27,432 |  
| **Monaco** | 38,000 | 46 | 864 | 44 |  |  | 8 | 1 | 16 | 111 |  
| **Mongolia** | 3,545,000 | 469 | 8,002 | 443 |  | 42 | 202 | 8 | 492 | 1,120 |  
| **Montenegro** | 624,000 | 448 | 1,438 | 434 | 5 | 2 | 140 | 8 | 114 | 759 |  
| **Montserrat** | 4,000 | 29 | 148 | 27 | -10 |  | 9 | 1 | 39 | 88 |  
| **Mozambique** | 35,632,000 | 109,531 | 345 | 103,244 | 12 | 10,368 | 14,043 | 2,072 | 177,808 | 405,172 |
</excerpt>

## Search 6 — query: "up-to-date reporting removed countries jw.org Service Year Report removed from up-to-date reporting"
### Rank 1 of 79 — 0.13 (passed on)
<excerpt title="2025 Country and Territory Reports">
| **Myanmar** | 51,317,000 | 5,382 | 9,677 | 5,303 | 2 | 253 | 1,195 | 115 | 5,947 | 10,543 |  
| **Namibia** | 3,093,000 | 3,083 | 1,045 | 2,961 | 6 | 181 | 438 | 54 | 4,490 | 9,736 |  
| **Nauru** | 12,000 | 21 | 800 | 15 | 7 |  | 4 | 1 | 35 | 150 |  
| **Nepal** | 29,876,000 | 3,001 | 10,103 | 2,957 | 3 | 167 | 956 | 62 | 4,189 | 7,756 |  
| **Netherlands** | 18,069,000 | 29,552 | 616 | 29,341 |  | 412 | 3,233 | 333 | 8,218 | 48,179 |  
| **Nevis** | 13,000 | 94 | 167 | 78 | 7 |  | 9 | 1 | 63 | 252 |  
| **New Caledonia** | 265,000 | 2,726 | 99 | 2,688 | 1 | 115 | 359 | 32 | 2,468 | 7,606 |  

| **New Zealand** | 5,331,000 | 14,809 | 364 | 14,652 | 1 | 239 | 1,930 | 169 | 5,375 | 27,066 |  
| **Nicaragua** | 7,008,000 | 29,071 | 243 | 28,880 | 1 | 831 | 5,596 | 440 | 23,237 | 78,226 |  
| **Niger** | 27,918,000 | 385 | 82,112 | 340 | 6 | 10 | 59 | 9 | 442 | 976 |  
| **Nigeria** | 237,528,000 | 421,375 | 589 | 403,535 | 3 | 27,263 | 52,575 | 6,221 | 766,292 | 818,848 |  
| **Niue** | 2,000 | 21 | 105 | 19 |  |  | 3 | 1 | 6 | 47 |  
| **North Macedonia** | 1,826,000 | 1,275 | 1,452 | 1,258 | 1 | 40 | 204 | 22 | 473 | 2,310 |  
| **Norway** | 5,601,000 | 12,096 | 466 | 12,020 |  | 156 | 1,553 | 161 | 3,058 | 17,583 |
</excerpt>
### Rank 2 of 79 — 0.10
<excerpt title="2025 Country and Territory Reports">
| **Central African Republic** | 5,513,000 | 3,705 | 1,563 | 3,527 | 11 | 334 | 511 | 72 | 9,875 | 25,256 |  
| **Chad** | 19,341,000 | 1,082 | 18,705 | 1,034 | 11 | 74 | 138 | 26 | 1,201 | 4,229 |  
| **Chile** | 20,207,000 | 88,664 | 229 | 88,202 | 1 | 1,905 | 21,602 | 1,024 | 37,753 | 185,618 |  
| **Chuuk** | 50,000 | 32 | 1,786 | 28 |  | 3 | 8 | 2 | 59 | 144 |  
| **Colombia** | 52,696,000 | 193,778 | 274 | 192,392 | 2 | 5,895 | 42,653 | 2,341 | 142,088 | 526,568 |  
| **Congo, Dem. Republic of** | 115,685,000 | 306,303 | 389 | 297,215 | 11 | 23,170 | 38,139 | 4,810 | 788,698 | 1,411,774 |  

| **Congo, Republic of** | 6,565,000 | 10,811 | 635 | 10,344 | 8 | 613 | 1,947 | 135 | 26,097 | 33,669 |  
| **Cook Islands** | 17,000 | 209 | 89 | 190 | -2 | 9 | 31 | 3 | 91 | 522 |  
| **Costa Rica** | 5,153,000 | 32,604 | 159 | 32,381 | 1 | 755 | 5,201 | 417 | 17,791 | 67,637 |  
| **Côte d’Ivoire** | 32,712,000 | 14,068 | 2,415 | 13,545 | 6 | 759 | 1,865 | 232 | 22,612 | 52,597 |  
| **Croatia** | 3,874,000 | 4,595 | 850 | 4,560 | -1 | 114 | 467 | 56 | 785 | 7,014 |  
| **Cuba** | 9,748,000 | 83,406 | 118 | 82,835 | -1 | 2,258 | 10,928 | 1,283 | 82,483 | 196,596 |  
| **Curaçao** | 156,000 | 1,930 | 81 | 1,917 | 1 | 35 | 290 | 24 | 1,149 | 4,942 |
</excerpt>
### Rank 3 of 79 — 0.09
<excerpt title="Why the annual report is misleading : r/exjw">
# Comments Section
The cult has been lying for years about their numbers and it’s getting obvious they can’t continue. If any thing they may have started using this Covid as a chance to make some adjustments but on the other hand they can’t stop their bullshit so they start up again and make it look as though Europe, Japan and even Pakistan has growth. Common now Pakistan?!? With a country like growth in Pakistan as reported it just shows their full of shit!
This is just a shell game their playing and I think the Pakistan report was a Easter egg that a pimo bethelite put in the report to tell us it’s all bullshit!
chinapomo
•4y ago
Excellent analysis.
About point 8, historically they have been able to offset the loss of hours due to the reduced requirements thanks to a new influx of pioneers. But usually, that takes 5/6 years.
[deleted]
•4y ago
Thank you 🙂
Don_Python
•4y ago
Those moving temporarily (for less than three months, IIRIC) continue to report to their home congregation. Given there was just four-percent decrease in Ukraine (based on the average pubs number, btw), your theory seems poorly based. Also, zero new Russian- or Ukrainian-language congregations have been created in Germany since the beginning of the war.
It also comes to my mind that we apparently have different definitions of "misleading" because I don't see from your post "why the annual report is misleading".
TheHistoryCritic
•4y ago
Continuing to report to their home congregation wouldn't be possible if half the congregation was gone, dispersed throughout Europe. Since about 30% of the overall population left Ukraine, I used 30% as my estimate. Since congregations in Western Europe would have taken them in, and the entire thing would have been seen as temporary, I'm not surprised that no new Ukrainian (or Russian) language congs were established. For the most part, the refugees have returned to Ukraine. By the time of the annual report, any temporary congregations would have been disbanded anyway.
One thing I had not thought of when I put this together was the fact that being a Jehovah's Witness in Ukraine serves as grounds for getting a conscientious objector status. I wonder how many PIMO's delayed leaving so that they didn't have to fight?

# Comments Section
Personally, if I was young enough and I thought I'd be of use, I'd be over there with my fatigues on.
1 more reply
1 more reply
1 more reply
More replies
phandesal
•4y ago
TLDR version pls but I do appreciate your long post
ModaMeNow
•4y ago
Great points...and as always: if they didn't baptize and count children as publishers the numbers would look ridiculously bad.
And wait till the Great Boomer Death Cliff realllly begins
[deleted]
•4y ago
The borg is definitely in decline. I mentioned this on another post but I believe the biggest sign of decline is seeing how badly their three biggest markets of The United States, Brazil, and Mexico are doing. There are more than 3 million jdubs in these 3 countries and there was a decrease of 2% between them last year. It can't be a good sign if the 3 countries where almost half of all jdubs are decrease instead of grow.
RMCM1914
•4y ago
Great analysis. Thanks for your efforts here.
I think that the aging of the organization and the flight of younger ones raised in it will be the most significant factor in its continuing decline.
u/Grok_by_SpaceXSI•Ad
Grok Bot never stops. Close your laptop and wake up to finished work.
Sign Up
x.ai
EyeAmmGroot
•4y ago
The annual report contains distorted or false numbers mixed with accurate ones-
Selling of KH, reporting “ I had some witnessing activity” as field service, pioneer title even though not getting the hours due to Covid, zoom meetings w/cameras off, no regional conventions just TV convention over multiple weekends-
I mean come on - there are not 8 million+ PIMI on the planet- But there are tens of millions of people affected by the JW religion worldwide-
[deleted]
•4y ago
Comment deleted by user
cultwashedmybrain
•4y ago
Same
1 more reply
1 more reply
1 more reply
8 more replies
8 more replies
</excerpt>
### Rank 4 of 79 — 0.09
<excerpt title="Why the annual report is misleading : r/exjw">
# Comments Section
Personally, if I was young enough and I thought I'd be of use, I'd be over there with my fatigues on.
1 more reply
1 more reply
1 more reply
More replies
phandesal
•4y ago
TLDR version pls but I do appreciate your long post
ModaMeNow
•4y ago
Great points...and as always: if they didn't baptize and count children as publishers the numbers would look ridiculously bad.
And wait till the Great Boomer Death Cliff realllly begins
[deleted]
•4y ago
The borg is definitely in decline. I mentioned this on another post but I believe the biggest sign of decline is seeing how badly their three biggest markets of The United States, Brazil, and Mexico are doing. There are more than 3 million jdubs in these 3 countries and there was a decrease of 2% between them last year. It can't be a good sign if the 3 countries where almost half of all jdubs are decrease instead of grow.
RMCM1914
•4y ago
Great analysis. Thanks for your efforts here.
I think that the aging of the organization and the flight of younger ones raised in it will be the most significant factor in its continuing decline.
u/Grok_by_SpaceXSI•Ad
Grok Bot never stops. Close your laptop and wake up to finished work.
Sign Up
x.ai
EyeAmmGroot
•4y ago
The annual report contains distorted or false numbers mixed with accurate ones-
Selling of KH, reporting “ I had some witnessing activity” as field service, pioneer title even though not getting the hours due to Covid, zoom meetings w/cameras off, no regional conventions just TV convention over multiple weekends-
I mean come on - there are not 8 million+ PIMI on the planet- But there are tens of millions of people affected by the JW religion worldwide-
[deleted]
•4y ago
Comment deleted by user
cultwashedmybrain
•4y ago
Same
1 more reply
1 more reply
1 more reply
8 more replies
8 more replies

# More posts you may like
Related posts
*   2026 Service Year Report Highlights and Implications r/exjw•2d ago    ### 2026 Service Year Report Highlights and Implications    49 upvotes ·22 comments
* * *
*    Preply  •Ad    You don’t need more grammar drills. You need someone who can tell you why you’re stuck. A Preply tutor can. Find yours.       preply.com Book Now
* * *
*   A thank you to this community, from someone who made it out r/exjw•3d ago    ### A thank you to this community, from someone who made it out    81 upvotes ·14 comments
* * *
*   The Rumor Mill: News and Gossip - November 16, 2026 r/exjw•2d ago    ### The Rumor Mill: News and Gossip - November 16, 2026    13 upvotes ·13 comments
* * *
*   They’re suspicious and i need help r/exjw•3d ago    ### They’re suspicious and i need help    143 upvotes ·79 comments
* * *
*   We lost someone to them 🫡😢 +shocking announcement r/exjw•4d ago    ### We lost someone to them 🫡😢 +shocking announcement    157 upvotes ·44 comments
* * *
*   It’s the morning after my announcement. r/exjw•7d ago    ### It’s the morning after my announcement.    487 upvotes ·125 comments
* * *
*   Advice sought for what comes next r/exjw•6d ago    ### Advice sought for what comes next    62 upvotes ·37 comments
* * *
*   Complete List of Updates for the Past Three Years r/exjw•6d ago    ### Complete List of Updates for the Past Three Years    69 upvotes ·18 comments
* * *
</excerpt>
### Rank 5 of 79 — 0.08
<excerpt title="2025 Country and Territory Reports">
| **Senegal** | 19,391,000 | 1,642 | 12,226 | 1,586 | 1 | 49 | 238 | 27 | 1,707 | 3,104 |  
| **Serbia** | 6,586,000 | 3,850 | 1,745 | 3,774 | 2 | 73 | 802 | 59 | 1,232 | 6,817 |  
| **Seychelles** | 122,000 | 417 | 332 | 368 | 7 | 15 | 39 | 5 | 318 | 1,019 |  
| **Sierra Leone** | 8,820,000 | 2,803 | 3,313 | 2,662 | 9 | 170 | 427 | 44 | 5,357 | 9,205 |  
| **Slovakia** | 5,422,000 | 11,267 | 484 | 11,194 |  | 178 | 1,094 | 139 | 2,278 | 20,620 |  
| **Slovenia** | 2,131,000 | 1,735 | 1,244 | 1,713 | -1 | 13 | 293 | 22 | 487 | 2,624 |  
| **Solomon Islands** | 798,000 | 1,814 | 468 | 1,704 | 1 | 76 | 252 | 38 | 1,581 | 11,406 |  

| **South Africa** | 63,101,000 | 107,746 | 600 | 105,117 | 4 | 4,646 | 17,081 | 1,925 | 105,918 | 260,378 |  
| **South Sudan** | 15,787,000 | 2,469 | 6,556 | 2,408 | 14 | 221 | 405 | 37 | 5,252 | 7,992 |  
| **Spain** | 49,316,000 | 127,840 | 388 | 126,954 | 2 | 2,146 | 27,257 | 1,377 | 37,939 | 211,887 |  
| **Sri Lanka** | 21,763,000 | 7,169 | 3,083 | 7,059 | 2 | 135 | 1,359 | 86 | 6,886 | 14,806 |  
| **Sudan** | 51,662,000 | 71 | 771,075 | 67 | -52 | 19 | 7 | 3 | 96 | 160 |  
| **Suriname** | 640,000 | 3,265 | 201 | 3,180 | 1 | 124 | 427 | 54 | 3,049 | 8,796 |
</excerpt>

## Search 7 — query: ""removed from up-to-date reporting" "jw.org""
(no page could be scored)

## Search 8 — query: "2023 Service Year Report country and territory reports jw.org 2023 country and territory"
### Rank 1 of 34 — 0.23 (passed on)
<excerpt title="Service Year Reports - Jehovah's Witnesses">
## Did You Know … ?
Jehovah’s Witnesses publish the number of publishers, pioneers, memorial attendees, and baptisms annually. However, they do not disclose the number of members who leave or are expelled from the religious group, despite keeping records of such ones.

## Did You Know … ?
### 2022 Service Year Report
You can export all of the content as a comma-separated value (csv) file, or you can use the print function to export to PDF. If you want to export a portion of the data only, use the drop-down menu to select country or territory(s) before using the export function.

## Did You Know … ?
### 2022 Service Year Report
| Country or Territory All * 33 Other Lands * Albania * American Samoa * Andorra * Angola * Anguilla * Antigua * Argentina * Armenia * Aruba * Australia * Austria * Azerbaijan * Azores * Bahamas * Bangladesh * Barbados * Belarus * Belgium * Belize * Benin * Bermuda * Bolivia * Bonaire * Bosnia and Herzegovina * Botswana * Brazil * Britain * Bulgaria * Burkina Faso * Burundi * Cambodia * Cameroon * Canada * Cape Verde * Cayman Islands * Central African Republic * Chad * Chile * Chuuk * Colombia * Congo, Dem. Republic of * Congo, Republic of * Cook Islands * Costa Rica * Croatia * Cuba * Curaçao * Cyprus * Czech Republic * Côte d’Ivoire * Denmark * Dominica * Dominican Republic * Ecuador * El Salvador * Equatorial Guinea * Estonia * Eswatini * Ethiopia * Falkland Islands * Faroe Islands * Fiji * Finland * France * French Guiana * Gabon * Gambia * Georgia * Germany * Ghana * Gibraltar * Grand Total (239 Lands) * Greece * Greenland * Grenada * Guadeloupe * Guam * Guatemala * Guinea * Guinea-Bissau * Guyana * Haiti * Honduras * Hong Kong * Hungary * Iceland * India * Indonesia * Ireland * Israel * Italy * Jamaica * Japan * Kazakhstan * Kenya * Kiribati * Korea, Republic of * Kosovo * Kosrae * Kyrgyzstan * Latvia * Lesotho * Liberia * Liechtenstein * Lithuania * Luxembourg * Macao * Madagascar * Madeira * Malawi * Malaysia * Mali * Malta * Marshall Islands * Martinique * Mauritius * Mayotte * Mexico * Moldova * Mongolia * Montenegro * Montserrat * Mozambique * Myanmar * Namibia * Nauru * Nepal * Netherlands * Nevis * New Caledonia * New Zealand * Nicaragua * Niger * Nigeria * Niue * North Macedonia * Norway * Pakistan * Palau * Palestinian Territories * Panama * Papua New Guinea * Paraguay * Peru * Philippines * Pohnpei * Poland * Portugal * Puerto Rico * Rodrigues * Romania * Rota * Rwanda * Réunion * Saba * Saipan * Samoa * San Marino * Senegal * Serbia * Seychelles * Sierra Leone * Slovakia * Slovenia * Solomon Islands * South Africa * South Sudan * Spain * Sri Lanka * St. Barthélemy * St. Eustatius * St. Helena * St.

## Did You Know … ?
### 2022 Service Year Report
Kitts * St. Lucia * St. Maarten * St. Martin * St. Pierre and Miquelon * St. Vincent & the Grenadines * Sudan * Suriname * Sweden * Switzerland * São Tomé and Príncipe * Tahiti * Taiwan * Tanzania * Thailand * Timor-Leste * Tinian * Togo * Tonga * Trinidad & Tobago * Turkey * Turks and Caicos * Tuvalu * Uganda * Ukraine * United States of America * Uruguay * Vanuatu * Venezuela * Virgin Islands, British * Virgin Islands, U.S. * Wallis & Futuna Islands * Yap * Zambia * Zimbabwe OK Cancel Search * Search in * Year * Country or Territory * Population * Peak Publishers * Ratio, 1 Publisher to * Average Publishers * % Increase * Baptisms * Average Pioneer Publishers * Congregations * Memorial Attendance |
</excerpt>
### Rank 2 of 34 — 0.21
<excerpt title="Service Year Reports - Jehovah's Witnesses">
## Did You Know … ?
### 2022 Service Year Report
Kitts * St. Lucia * St. Maarten * St. Martin * St. Pierre and Miquelon * St. Vincent & the Grenadines * Sudan * Suriname * Sweden * Switzerland * São Tomé and Príncipe * Tahiti * Taiwan * Tanzania * Thailand * Timor-Leste * Tinian * Togo * Tonga * Trinidad & Tobago * Turkey * Turks and Caicos * Tuvalu * Uganda * Ukraine * United States of America * Uruguay * Vanuatu * Venezuela * Virgin Islands, British * Virgin Islands, U.S. * Wallis & Futuna Islands * Yap * Zambia * Zimbabwe OK Cancel Search * Search in * Year * Country or Territory * Population * Peak Publishers * Ratio, 1 Publisher to * Average Publishers * % Increase * Baptisms * Average Pioneer Publishers * Congregations * Memorial Attendance |

## Did You Know … ?
### 2022 Service Year Report
| --- |  
| Year | Country or Territory | Population | Peak Publishers | Ratio, 1 Publisher to | Average Publishers | % Increase | Baptisms | Average Pioneer Publishers | Congregations | Memorial Attendance |  
| 2022 | Albania | 2,866,000 | 5,577 | 518 | 5,531 | -1 | 112 | 1,363 | 83 | 12,106 |  
| 2022 | American Samoa | 55,000 | 154 | 420 | 131 | -9 | 0 | 32 | 3 | 647 |  
| 2022 | Andorra | 77,000 | 169 | 461 | 167 | -1 | 0 | 23 | 3 | 331 |  
| 2022 | Angola | 35,027,000 | 159,384 | 226 | 154,953 | 3 | 3,273 | 25,609 | 2,539 | 485,484 |  
| 2022 | Anguilla | 15,000 | 67 | 259 | 58 | 5 | 0 | 11 | 1 | 208 |  
| 2022 | Antigua | 100,000 | 478 | 215 | 466 | 1 | 0 | 41 | 7 | 1,244 |  
| 2022 | Argentina | 47,327,000 | 155,443 | 308 | 153,787 | -2 | 2,869 | 35,977 | 1,945 | 345,669 |
</excerpt>
### Rank 3 of 34 — 0.20
<excerpt title="Service Year Reports - Jehovah's Witnesses">
## Did You Know … ?
### 2022 Service Year Report
| 2022 | Bangladesh | 170,298,000 | 338 | 509,874 | 334 | 2 | 7 | 140 | 6 | 1,048 |  
| 2022 | Barbados | 288,000 | 2,389 | 122 | 2,360 | -1 | 38 | 191 | 30 | 6,732 |  
| 2022 | Belarus | 9,433,000 | 6,167 | 1,546 | 6,100 | -1 | 125 | 1,475 | 83 | 11,784 |  
| 2022 | Belgium | 11,584,000 | 25,970 | 448 | 25,835 | 0 | 334 | 2,441 | 336 | 44,337 |  
| 2022 | Belize | 441,000 | 2,614 | 174 | 2,539 | -1 | 49 | 487 | 54 | 8,317 |  
| 2022 | Benin | 12,782,000 | 14,202 | 953 | 13,410 | 2 | 380 | 1,841 | 246 | 38,932 |  
| 2022 | Bermuda | 62,000 | 443 | 159 | 389 | -3 | 0 | 73 | 5 | 963 |
</excerpt>
### Rank 4 of 34 — 0.20
<excerpt title="Service Year Reports - Jehovah's Witnesses">
## Did You Know … ?
### 2022 Service Year Report
| --- |  
| Year | Country or Territory | Population | Peak Publishers | Ratio, 1 Publisher to | Average Publishers | % Increase | Baptisms | Average Pioneer Publishers | Congregations | Memorial Attendance |  
| 2022 | Albania | 2,866,000 | 5,577 | 518 | 5,531 | -1 | 112 | 1,363 | 83 | 12,106 |  
| 2022 | American Samoa | 55,000 | 154 | 420 | 131 | -9 | 0 | 32 | 3 | 647 |  
| 2022 | Andorra | 77,000 | 169 | 461 | 167 | -1 | 0 | 23 | 3 | 331 |  
| 2022 | Angola | 35,027,000 | 159,384 | 226 | 154,953 | 3 | 3,273 | 25,609 | 2,539 | 485,484 |  
| 2022 | Anguilla | 15,000 | 67 | 259 | 58 | 5 | 0 | 11 | 1 | 208 |  
| 2022 | Antigua | 100,000 | 478 | 215 | 466 | 1 | 0 | 41 | 7 | 1,244 |  
| 2022 | Argentina | 47,327,000 | 155,443 | 308 | 153,787 | -2 | 2,869 | 35,977 | 1,945 | 345,669 |
</excerpt>
### Rank 5 of 34 — 0.20
<excerpt title="Service Year Reports - Jehovah's Witnesses">
## Did You Know … ?
### 2022 Service Year Report
| 2022 | Cook Islands | 18,000 | 211 | 90 | 199 | 1 | 2 | 27 | 3 | 500 |  
| 2022 | Costa Rica | 5,213,000 | 32,504 | 161 | 32,290 | 0 | 546 | 4,275 | 435 | 72,360 |  
| 2022 | Côte d’Ivoire | 29,389,000 | 11,877 | 2,521 | 11,657 | 0 | 255 | 1,577 | 231 | 37,361 |  
| 2022 | Croatia | 4,069,000 | 4,736 | 867 | 4,693 | -2 | 40 | 462 | 57 | 7,218 |  
| 2022 | Cuba | 11,113,000 | 91,710 | 123 | 90,315 | -3 | 1,216 | 8,932 | 1,399 | 166,891 |  
| 2022 | Curaçao | 166,000 | 2,040 | 83 | 1,991 | -1 | 40 | 254 | 25 | 5,629 |  
| 2022 | Cyprus | 1,224,000 | 2,960 | 421 | 2,908 | 3 | 28 | 571 | 40 | 5,178 |
</excerpt>

## Search 9 — query: "2017 Service Year Report csv"
### Rank 1 of 46 — 0.13 (passed on)
<excerpt title="Public Libraries Survey (PLS)">
## About the Data Files
### FY 2021
*   Data Files – CSV (ZIP 3 MB), SAS (ZIP 4 MB), and SPSS (ZIP 5 MB)  
*   Data File Documentation and User's Guide (PDF 2 MB)  
*   Research Brief: Changes in Public Library Services as the COVID-19 Pandemic Continued Through FY 2021

## About the Data Files
### FY 2020
*   Data Files – CSV (ZIP 3 MB), SAS (ZIP 4 MB), and SPSS (ZIP 3 MB)  
*   Documentation (PDF 2.33 MB)  
*   Infographic: How Public Libraries Adapted at the Start of the COVID-19 Pandemic, June 2022 (PDF 1.2MB)  
*   Research Brief: Access to Public Library Services During the First Nine Months of the COVID-19 Pandemic, May 2023

## About the Data Files
### FY 2019
Data Files – CSV (ZIP 3 MB), SAS (ZIP 4 MB), and SPSS(ZIP 5 MB)
Documentation (PDF 2.55 MB)
Public Libraries in the United States: Findings from the FY 2019 Public Libraries Survey
Supplementary Tables List (XLS 22 KB)
*   Tables 1-6A: Number and Percentage of Public Libraries by Select Characteristics(XLS 116 KB)  
*   Tables 7-13A: Public Library Revenue and Expenses(XLS 124 KB)  
*   Tables 14-25A: Public Library Services, Resources, and Programs(XLS 465 KB)  
*   Tables 26-27A: Public Library Staffing(XLS 50 KB)  
*   Tables 28-28A: Size of Public Libraries(XLS 32 KB)  
*   Tables 29-43: State Rankings on Key Variables(XLS 106 KB)

## About the Data Files
### FY 2018
*   Data Files - CSV (ZIP 3.1 MB), SAS (ZIP 3.9 MB), and SPSS (ZIP 4.6 MB)  
*   Supplementary Tables (PDF 3MB), Supplementary Tables Excel (ZIP 593 KB)  
*   Documentation (PDF 2.7 MB)  
*   Research Brief (PDF 342 KB)

## About the Data Files
### FY 2017
*   Data Files - CSV(ZIP 3.1MB),SAS(ZIP 3.8MB), andSPSS(ZIP 4.8MB)  
*   Documentation (PDF 1.9MB)  
*   Annual Report Volume 1, Volume 2  
*   Rural Libraries in America: An Infographic Overview
State Detail Tables: Rural Libraries in America (Download Excel:XLSX 84KB) (DownloadPDF 163KB)
*   Supplementary Tables (PDF 2.9MB)  
*   State Profiles  
*   News Release - July 16, 2020  
*   News Release- November 30, 2020
</excerpt>
### Rank 2 of 46 — 0.08
<excerpt title="Public Libraries Survey (PLS)">
## About the Data Files
### FY 2017
*   Data Files - CSV(ZIP 3.1MB),SAS(ZIP 3.8MB), andSPSS(ZIP 4.8MB)  
*   Documentation (PDF 1.9MB)  
*   Annual Report Volume 1, Volume 2  
*   Rural Libraries in America: An Infographic Overview
State Detail Tables: Rural Libraries in America (Download Excel:XLSX 84KB) (DownloadPDF 163KB)
*   Supplementary Tables (PDF 2.9MB)  
*   State Profiles  
*   News Release - July 16, 2020  
*   News Release- November 30, 2020

## About the Data Files
### FY 2016
The FY 2016 PLS shows that public libraries continue to evolve to meet changing community needs. More than 171 million registered users, representing over half of the nearly 311 million Americans who lived within a public library service area, visited public libraries over 1.35 billion times in 2016. Public libraries offered half a million more programs in 2016 than in 2015; 113 million people attended 5.2 million programs in 2016. In addition, the number of electronic materials continued to grow, with public libraries offering over 391 million e-books to their patrons in the United States.
*   Data Files -CSV(ZIP 3.12MB),SAS(ZIP 3.87MB),and SPSS (ZIP 4.85MB)  
*   Documentation(PDF 4.35MB)  
*   Annual Report  
*   Supplementary Tables(PDF 4.6MB),User Note 1(PDF 41KB), and User Note 2 (PDF 42KB)  
*   State Profiles  
*   Data Element Definitions(PDF 1.4MB)

## About the Data Files
### FY 2015
The FY 2015 PLS shows that the trends noted in previous years are continuing. Nearly 311 million Americans lived within a public library service area in 2015, an increase from 306 million in 2014. Public libraries offered 4.7 million programs in 2015, attended by 106 million people, 4 million more attendees than the previous year. In addition, the number of electronic materials, including audio, video and e-books, continued to grow, increasing by over 50 percent between 2014 and 2015.
*   Data Files -CSV(ZIP),SAS(ZIP), and SPSS (ZIP)  
*   Documentation(PDF 1.9MB)  
*   Annual Report  
*   State Profiles(PDF 6.3MB)  
*   Supplementary Tables(PDF 4.4MB) and User Note(PDF 53KB)  
*   Data Element Definitions(PDF 1.4MB)  
*   News Release- August 2, 2018

## About the Data Files
### FY 2014
The 2014 PLS shows libraries continuing to adapt to 21st century needs and a growing population. More than 306 million Americans lived within a public library service area in 2014, compared to 305 million in2013. Libraries offered more children and young adult programs, with an estimated 5 million more Americans attending library programs compared to the previous year. In addition, the number of downloadable audio, video, and electronic books available to the public grew significantly.
*   Data Files -CSV (ZIP) and SAS (ZIP)  
*   Documentation (PDF)  
*   Annual Report  
*   Supplementary Tables (PDF)  
*   Data Element Definitions (PDF)
</excerpt>
### Rank 3 of 46 — 0.05
<excerpt title="Public Libraries Survey (PLS)">
The Public Libraries Survey (PLS) examines when, where, and how library services are changing to meet the needs of the public. These data, supplied annually by public libraries across the country, provide information that policymakers and practitioners can use to make informed decisions about the support and strategic management of libraries. Browse research briefs and over 25 years ofresearch publications about the Public Libraries Survey (PLS).
**Purpose:** The survey provides statistics on the status of public libraries in the United States.
**Coverage:** The data are collected from approximately 9,000 public libraries with approximately 17,000 individual public library outlets (main libraries, branches, and bookmobiles) in the 50 states, the District of Columbia, and outlying territories.
**Content:** Data includes information about library visits, circulation, size of collections, public service hours, staffing, electronic resources, operating revenues and expenditures and number of service outlets. Learn more about PLS data element definitions.
**Frequency:** Collected annually since 1988. (Data files are available since 1992.)
**Methods:** At the state level, PLS is administered by Data Coordinators, appointed by the chief officer of the state library agency from each state or outlying area. State Data Coordinators collect the requested data from local public libraries and report these data to us via a web-based reporting system.
**Use:** PLS data are useful to researchers, journalists, the public, local practitioners, and policymakers at the federal, state, and local levels, and are used for planning, evaluation, and policy making. Download the datasets in multiple formats below, or use our online Library Search & Compare tool to find a library and browse the latest available data.

## About the Data Files
The data files available on our web site are public-use data files. These files have had some data removed to protect the confidentiality of individually identifiable survey respondents. Public-use data files are publicly available without restriction, and do not require a license. Survey data are coded or aggregated without individually identifiable information. Data that could be directly identified with one individual (salaries and wages for librarians for a library with one librarian, for example) are removed.
A small proportion of the data that has been collected are in restricted-use data files, which contain individually identifiable information, which is confidential and protected by law. For more information on restricted-use data files, please contact us.

## About the Data Files
### FY 2024
*   Data Files – CSV (ZIP 3 MB), SAS (ZIP 4 MB), and SPSS (ZIP 5 MB) **NEW!**  
*   Data File Documentation and User's Guide (PDF 2 MB)**NEW!**

## About the Data Files
### FY 2023
*   Research Brief: Public Library Trends Between FY 2018 and FY 2023  
*   Data Files – CSV (ZIP 4 MB), SAS (ZIP 4 MB), and SPSS (ZIP 5 MB)  
*   Data File Documentation and User's Guide (PDF 2 MB)  
*   PLS Benchmarking Tables (ZIP 1 MB)

## About the Data Files
### FY 2022
*   Data Files – CSV (ZIP 3 MB), SAS (ZIP 4 MB), and SPSS (ZIP 5 MB)  
*   Data File Documentation and User's Guide (PDF 2 MB)  
*   Research Brief: Methodological Improvements to the Public Libraries Survey

## About the Data Files
### FY 2021
*   Data Files – CSV (ZIP 3 MB), SAS (ZIP 4 MB), and SPSS (ZIP 5 MB)  
*   Data File Documentation and User's Guide (PDF 2 MB)  
*   Research Brief: Changes in Public Library Services as the COVID-19 Pandemic Continued Through FY 2021
</excerpt>
### Rank 4 of 46 — 0.03
<excerpt title="Service Annual Survey Tables - Census Bureau">
Stats displayed in columns and rows with title, ID, notes, sources, and release date. Many tables on census.gov are in downloadable XLS, CSV and PDF file formats.
*
* * *
Table Service Annual Survey Latest Data (NAICS-basis): 2022 August 31, 2026 Latest Annual Services Report - includes estimates with accompanying measures of sampling variability
* * *
*
* * *
Table Service Annual Survey Latest Data (NAICS-basis): 2021 November 22, 2022 Latest Annual Services Report - includes estimates with accompanying measures of sampling variability
* * *
*
* * *
Table Service Annual Survey Latest Data (NAICS-basis): 2020 November 23, 2021 These are the archived reports (NAICS-basis) for 2020
* * *
*
* * *
Table Service Annual Survey Historical Data (NAICS-basis): 2019 April 29, 2021 These are the archived reports (NAICS-basis) for 2019.
* * *
*
* * *
Table Service Annual Survey Historical Data (NAICS-basis): 2018 December 10, 2020 These are the archived reports (NAICS-basis) for 2018.
* * *
*
* * *
Table Service Annual Survey Historical Data (NAICS-basis): 2016 November 27, 2017 These are the archived reports (NAICS-basis) for 2016.
* * *
*
* * *
Table Service Annual Survey Historical Data (SIC-basis): 1998 These are the archived reports (SIC-basis) for 1998.
* * *
*
* * *
Table Service Annual Survey Historical Data (NAICS-basis): 2002 February 01, 2004 These are the archived reports (NAICS-basis) for 2002.
* * *
*
* * *

Table Service Annual Survey Historical Data (NAICS-basis): 2000 December 01, 2001 These are the archived reports (NAICS-basis) for 2000.
* * *
*
* * *
Table Service Annual Survey Historical Data (SIC-basis): 1997 These are the archived reports (SIC-basis) for 1997.
* * *
*
* * *
Table Service Annual Survey Historical Data (SIC-basis): 1985-1994 These are the archived reports (SIC-basis) for 1985-1994.
* * *
*
* * *
Table Service Annual Survey Historical Data (NAICS-basis): 2010 February 01, 2012 These are the archived reports (NAICS-basis) for 2010.
* * *
*
* * *
Table Service Annual Survey Historical Data (NAICS-basis): 2009 February 01, 2011 These are the archived reports (NAICS-basis) for 2009.
* * *
*
* * *
Table Service Annual Survey Historical Data (NAICS-basis): 2006 January 01, 2008 These are the archived reports (NAICS-basis) for 2006.
* * *
*
* * *
Table Service Annual Survey Historical Data (NAICS-basis): 2005 February 01, 2007 These are the archived reports (NAICS-basis) for 2005.
* * *
*
* * *
Table Service Annual Survey Historical Data (NAICS-basis): 2015 January 28, 2016 These are the archived reports (NAICS-basis) for 2015.
* * *
*
* * *
Table Service Annual Survey Historical Data (NAICS-basis): 2012 January 01, 2012 These are the archived reports (NAICS-basis) for 2012.
* * *
*
* * *
</excerpt>
### Rank 5 of 46 — 0.02
<excerpt title="Public Libraries Survey (PLS)">
## About the Data Files
### FY 2005 PLS and Earlier
Please note that the National Center for Education Statistics (NCES) conducted the FY 2005 and earlier surveys and produced the data files and reports.

## About the Data Files
### FY 2005 PLS and Earlier
| Fiscal Year | Data Files | Documentation | Reports | Data Element Definitions |  
| --- | --- | --- | --- | --- |  
| 2005 | CSV (ZIP) and SAS (ZIP) | Documentation (PDF) | Annual Report (PDF) | Definitions (PDF) |  
| 2004 | CSV (ZIP) and SAS (ZIP) | Documentation (PDF) | Annual Report (PDF) | Definitions (PDF) |  
| 2003 | CSV (ZIP) and SAS (ZIP) | Documentation (PDF) | Annual Report (PDF) | Definitions (PDF) |  
| 2002 | CSV (ZIP) and SAS (ZIP) | Documentation | Annual Report |  |  
| 2001 | CSV (ZIP) and SAS (ZIP) | Documentation (PDF) | Annual Report (PDF) |  |  
| 2000 note | CSV (ZIP) and SAS (ZIP) | Documentation (PDF) | Annual Report (PDF) |  |  
| 1999 | CSV (ZIP) and SAS (ZIP) | Documentation (PDF) | Annual Report (PDF) |  |  
| 1998 | CSV (ZIP) and SAS (ZIP) | Documentation (PDF) | Annual Report (PDF) |  |  
| 1997 | CSV (ZIP) and SAS (ZIP) | Documentation | Annual Report |  |  
| 1996 | CSV (ZIP) and SAS (ZIP) | Documentation (PDF) | Annual Report (PDF) |  |  
| 1995 | CSV (ZIP) and SAS (ZIP) | Documentation (PDF) | Annual Report (PDF) and ResearchBrief (PDF) |  |  
| 1994 | CSV (ZIP) and SAS (ZIP) | Documentation (PDF) | Annual Report (PDF) |  |  
| 1993 | CSV (ZIP) and SAS (ZIP) | Documentation (PDF) | Annual Report (PDF) and Special Report (PDF) |  |  
| 1992 | CSV (ZIP) and SAS (ZIP) | Documentation (PDF) | Annual Report (PDF) |  |
Note: The electronic codebook and database (ZIP) are available for FY 2000.

## About the Data Files
### FY 2005 PLS and Earlier
Annual reports, but not data files, are available for PLS FY 1991(PDF), FY 1990(PDF), and FY 1989(PDF).
</excerpt>

## Search 10 — query: ""up-to-date reporting" "Jehovah""
### Rank 1 of 25 — 0.13 (passed on)
<excerpt title="Missing Information in Articles">
# Missing Information in Articles
*   Search  
*   Free Quizzes  
*   Videos  
*   Expert Profiles  
*   Blog  
*   About BrainMass  
*   Advertise  
*   Join
Sign in
Search
*   Join BrainMass  
*   Solution Library  
*   Get Custom Help  
*   eBook Library

*   Free Quizzes  
*   Videos  
*   Expert Profiles  
*   Blog  
*   About BrainMass  
*   Advertise
Sign in
1.   Psychology  
2.   Social Psychology  
3.   523336
Purchase Solution
Add  $2.49
Not what you're looking for?
Search Our LibraryAsk Custom Question
Give the APA reference for the article, followed by a brief overview of the issue and the author's position on the issue. Then offer your analysis of the article regarding missing information and suggest information to support the argument. Include some information resources that would assist this author in his/her decision-making matrix.
Reference:
The New JW/org: Watchtower/s attempt to tame the Internet (2012, September 3). Retrieved January 29, 2913, from http://jwsurvey.org.

# Missing Information in Articles
##### Purchase this Solution
* * *
Add to Cart - $2.49

# Missing Information in Articles
##### Solution Summary
* * *
This solution provides an overview of an author's position on specific issues, and offers an analysis of the missing information in the article.

# Missing Information in Articles
##### Solution Preview
* * *
(1) Give the APA reference for the article, followed by a brief overview of the issue and the author's position on the issue.
Overview
The article discusses the decision by Jehovah Witnesses to downsize from its previous three websites on the Internet to one contact outlet. The Watch Tower Society website cite its reason for discontinuing its previous websites to just one was to more effectively serve as the single point of contact for people seeking to assess Jehovah's witnesses online. Based on the Op Ed, it was decided to consolidate three sites into one referred to as Jw.org. The new site was viewed as appealing and easy to navigate, and suggested a minor improvement. However, the issue raised in the article, according to the author, no new content was provided regarding religious instruction. For example, the Watch Tower Society had suggested that its primary focus of the new website would be offer "an appealing picture of [their] preaching work". The writer of the Op Ed asserts that the religious organization took on a distinctive new look with deceptive intentions. For example, the religion claimed that a newsroom section would provide up-to-date reporting on events affecting God's people worldwide. However, it is argued that rather than highlighting its religious beliefs and practices in a more positive light, a closer inspection of ...

# Missing Information in Articles
##### Purchase this Solution
* * *
Add to Cart - $2.49
* * *

# Missing Information in Articles
##### Free BrainMass Quizzes


# Missing Information in Articles
##### Anxiety Disorders
This quiz is designed to help students gain a better understanding of various types of anxiety disorders.

# Missing Information in Articles
##### How can you tell if your loved one is suicidal?
This is a small quiz to help determine if a loved one is suicidal and what steps should be taken to help stop suicide.

# Missing Information in Articles
##### A Review of Qualitative and Quantitative methodologies
This quiz is designed to test your knowledge of qualitative and quantitative methodologies. Knowing the difference between the two can help in making the important decision of which to use when conducting research.

# Missing Information in Articles
##### Can you name these types of cognitive distortions?
In each mini-scenario, can you identify the type of cognitive distortion being displayed? All of us are subject to cognitive errors, biases, and distortions throughout our daily lives.

# Missing Information in Articles
##### Concepts in Personality Psychology
This quiz will test student's understanding of concepts relating to personality psychology.
View More Free Quizzes
</excerpt>
### Rank 2 of 25 — 0.06
<excerpt title="SECRET LETTER of Watchtower Media Changes!">
Christian Congregation
of Jehovah’s Witnesses
2821 Route 22, Patterson, NY 12563-2237 Phone: (845) 306-1100
4/2/12-E
April 2, 2012
TO ALL CONGREGATIONS
Re: Announcement to be read following Watchtower Study during week of April 2, 2012
Dear Brothers:
The Internet is a technology that Jehovah’s organization is using to good advantage to spread the good news to all corners of the earth. Consider the impact our Web sites are having. On a typical day, 400,000 people, both Witnesses and non-Witnesses, visit watchtower.org, jw.org, or jw-media.org.
They read our publications online in over 430 languages. Each day they download close to half a million audio, text, or sign-language-video files. Every day a hundred requests for Bible studies are sent in. To enhance the effectiveness of our use of the Internet, the Governing Body has decided to consolidate the three sites into one site called jw.org. The Web site will be completely redesigned. It will be appealing and easy to navigate using either a computer or a mobile device.
The redesigned jw.org Web site is planned for release around the beginning of June 2012. It will paint an appealing picture of our preaching work, branch offices, Kingdom Halls, and conventions.
A newsroom section will provide up-to-date reporting on events affecting God’s people
worldwide. Selected features from our magazines that can be presented more effectively on the Web site will now be published only on jw.org. These include the following: “For Young People,” “My Bible Lessons,” and the Gilead graduation report from the public edition of The Watchtower and “For Family Review” and “Young People Ask” from Awake! In addition, a series of online articles available only on the Web site will provide concise, clear answers to questions about the Bible and about Jehovah’s Witnesses.
The Governing Body has noted the growing tendency for people to obtain reading material

from the Internet and has carefully weighed the effect this trend is having on the printing industry and on our ability to obtain paper and equipment for printing. Based on these changing conditions, effective with the issues of January 2013, Awake! and the public edition of The Watchtower will be reduced from 32 pages to 16 pages. These magazines that we distribute to the public will continue to provide a rich supply of enlightening material to attract people to the truth of God’s Word. Since each issue will contain less material, it may be possible for more translation teams to be able to translate every issue of Awake! and the public edition of The Watchtower, thus increasing the number of languages in which they are available. The study edition of The Watchtower will continue to be a 32-page magazine.
The Governing Body is confident that these adjustments will enable us to reach even more
people with the Bible’s life-saving message while continuing to provide a rich supply of nourishing spiritual food for the worldwide brotherhood.
Your brothers,
cc: Traveling overseers
April 2, 2012
Page 2
PS to coordinator of the body of elders:
This matter should be kept strictly confidential among the elders until the letter is read in your congregation. Please arrange for this letter to be read to the congregation following the Watchtower Study during the week of April 2, 2012. This will be the same day as the special talk. In most congregations this will be Sunday, April 8, 2012. The brother who delivered the special talk should be invited to read this letter to the audience, if he is available to do so. Thereafter, this letter should be posted on the information board for four weeks.
The reading of this letter is in addition to the shorter announcement to be read by the chairman immediately following the special talk as outlined in the letter dated February 1, 2012, to all bodies of elders. Therefore, the chairman will read the shorter announcement following the special talk and before the Watchtower Study. Following the Watchtower Study, the brother who delivered the special talk will read this letter and thereafter introduce the concluding song
</excerpt>
### Rank 3 of 25 — 0.06
<excerpt title="Watchtower Decline Seen in Magazine Downsizing!">
# Watchtower Decline Seen in Magazine Downsizing! - [Mirror of TheSnarkyApologist]
## In this video
Transcript

# Watchtower Decline Seen in Magazine Downsizing! - [Mirror of TheSnarkyApologist]
## Watchtower Decline Seen in Magazine Downsizing! - [Mirror of TheSnarkyApologist]
Matt Clayberg Ministries
Matt Clayberg Ministries
58 Likes
5K Views
2012 Apr 3
Christian Congregation of Jehovah's Witnesses 2821 Route 22, Patterson, NY 12563-2237 Phone: (845) 306-1100 4/2/12-E April 2, 2012 TO ALL CONGREGATIONS Re: Announcement to be read following Watchtower Study during week of April 2, 2012 Dear Brothers: The Internet is a technology that Jehovah's organization is using to good advantage to spread the good news to all corners of the earth. Consider the impact our Web sites are having. On a typical day, 400,000 people, both Witnesses and non-Witnesses, visit watchtower.org, jw.org, or jw-media.org. They read our publications online in over 430 languages. Each day they download close to half a million audio, text, or sign-language-video files. Every day a hundred requests for Bible studies are sent in. To enhance the effectiveness of our use of the Internet, the Governing Body has decided to consolidate the three sites into one site called jw.org. The Web site will be completely redesigned. It will be appealing and easy to navigate using either a computer or a mobile device. The redesigned jw.org Web site is planned for release around the beginning of June 2012. It will paint an appealing picture of our preaching work, branch offices, Kingdom Halls, and conventions. A newsroom section will provide up-to-date reporting on events affecting God's people worldwide. Selected features from our magazines that can be presented more effectively on the Web site will now be published only on jw.org. These include the following: "For Young People," "My Bible Lessons," and the Gilead graduation report from the public edition of The Watchtower and "For Family Review" and "Young People Ask" from Awake! In addition, a series of online articles available only on the Web site will provide concise, clear answers to questions about the Bible and about Jehovah's Witnesses.
</excerpt>
### Rank 4 of 25 — 0.06
<excerpt title="Biting off more than they can chew - why I think the Society's ...">
Hi everyone
I've been giving some thought to the Society's latest decision to reduce the size of the Awake, and relaunch jw.org as a revamped site - intended for bringing in yet more converts. For those who missed it, here is the relevant part of the leaked letter to elders discussing these changes...
_The Internet is a technology that Jehovah’s organization is using to good advantage to spread the good news to all corners of the earth. Consider the impact our Web sites are having. On a typical day, 400,000 people, both Witnesses and non-Witnesses, visit watchtower.org, jw.org, or jw-media.org.  
They read our publications online in over 430 languages. Each day they download close to half a million audio, text, or sign-language-video files. Every day a hundred requests for Bible studies are sent in. To enhance the effectiveness of our use of the Internet, the Governing Body has decided to consolidate the three sites into one site called jw.org. The Web site will be completely redesigned. It will be appealing and easy to navigate using either a computer or a mobile device.
The redesigned jw.org Web site is planned for release around the beginning of June 2012. It will paint an appealing picture of our preaching work, branch offices, Kingdom Halls, and conventions.
A newsroom section will provide up-to-date reporting on events affecting God’s people
worldwide. Selected features from our magazines that can be presented more effectively on the Web site will now be published only on jw.org. These include the following: “For Young People,” “My Bible Lessons,” and the Gilead graduation report from the public edition of The Watchtower and “For Family Review” and “Young People Ask” from Awake! In addition, a series of online articles available only on the Web site will provide concise, clear answers to questions about the Bible and about Jehovah’s Witnesses._
Whilst I note the cautious tone of jwfacts in his thread on this subject (and I understand his reasoning) I believe the above development is exciting news - and grounds for optimism for those of us who dearly wish to live to see the Society's downfall. I don't believe it will result in growth for the Society, but (if anything) ever-decreasing growth if the Society rely overly on the Internet to spread its message. Why?

The Watch Tower Society have been fighting a losing battle with the Internet over recent years despite repeated calls for publishers to go nowhere near it if they can help it. The recent Watchtower article discussing "Internet Eve" is a good example of their attempts to breed paranoia - even comparing search engines like Google to an unscrupulous gang of mushroom pickers!
Whilst you can breed fear and intimidation about the "negative" aspects of the internet among hardened Witnesses, it is less easy to establish ground rules among those who are interested in researching the religion for the first time, and who aren't already indoctrinated into embracing your threats and fear-mongering concerning other Witness-related material to be found online.
I have a limited amount of experience of using the internet to run a business. In the relatively brief period in which I have taken an active interest in global web behavior, I have noticed this - you CANNOT predict people's behavior online. For example, anyone who runs a pay-per-click campaign on their website will tell you that, in the area of keywords alone, people will type in a sweeping variety of word combinations to arrive at the same web page. The same will surely be true when it comes to people trying to find the Society's official website, no matter how simple and easy to remember their domain name is. Everyone is different, and you will always get those who stumble on apostate material if they are encouraged to research JWs online, and yet the Society thinks they can direct all JW-interested internet surfers to jw.org and NO other JW-related site, just by doing a bit of spring cleaning?? Do me a favour!
The Society may have enjoyed a degree of success in warning the rank and file away from cyberspace, but their target audience for the soon-to-be-launched upgraded jw.org is much more savvy than the Governing Body seemingly believes. For the most part, they haven't yet been taught to fear the Faithful Slave. They are curious and inquisitive, and they want to know the real truth and not just what is handed to them on a plate.
</excerpt>
### Rank 5 of 25 — 0.05
<excerpt title="Watchtower Decline Seen in Magazine Downsizing!">
# Watchtower Decline Seen in Magazine Downsizing! - [Mirror of TheSnarkyApologist]
## Watchtower Decline Seen in Magazine Downsizing! - [Mirror of TheSnarkyApologist]
Matt Clayberg Ministries
Matt Clayberg Ministries
58 Likes
5K Views
2012 Apr 3
Christian Congregation of Jehovah's Witnesses 2821 Route 22, Patterson, NY 12563-2237 Phone: (845) 306-1100 4/2/12-E April 2, 2012 TO ALL CONGREGATIONS Re: Announcement to be read following Watchtower Study during week of April 2, 2012 Dear Brothers: The Internet is a technology that Jehovah's organization is using to good advantage to spread the good news to all corners of the earth. Consider the impact our Web sites are having. On a typical day, 400,000 people, both Witnesses and non-Witnesses, visit watchtower.org, jw.org, or jw-media.org. They read our publications online in over 430 languages. Each day they download close to half a million audio, text, or sign-language-video files. Every day a hundred requests for Bible studies are sent in. To enhance the effectiveness of our use of the Internet, the Governing Body has decided to consolidate the three sites into one site called jw.org. The Web site will be completely redesigned. It will be appealing and easy to navigate using either a computer or a mobile device. The redesigned jw.org Web site is planned for release around the beginning of June 2012. It will paint an appealing picture of our preaching work, branch offices, Kingdom Halls, and conventions. A newsroom section will provide up-to-date reporting on events affecting God's people worldwide. Selected features from our magazines that can be presented more effectively on the Web site will now be published only on jw.org. These include the following: "For Young People," "My Bible Lessons," and the Gilead graduation report from the public edition of The Watchtower and "For Family Review" and "Young People Ask" from Awake! In addition, a series of online articles available only on the Web site will provide concise, clear answers to questions about the Bible and about Jehovah's Witnesses.
</excerpt>

# Example 2
## Question
Using the census data from census.gov, find the Florida counties with less than 50000 residents in the year 2022, that had a GDP less than half a billion (in 2017 chained dollars) in that same year according to the Bureau of Economic Analysis. Exclude counties named after a founding father of the United States from the list by The White House.

## Expected answer
Calhoun County, Dixie County, Gilchrist County, Glades County, Gulf County, Holmes County, Lafayette County, Liberty County, Union County.

## Grade 0.59

## Search 1 — query: "Florida county population 2022 < 50000 census.gov"
### Rank 1 of 71 — 0.85 (passed on)
<excerpt title="Demographics of Florida">
### Population by county by year
| DeSoto | 33,976 | 34,862 | 32,209 |  
| Dixie | 16,759 | 16,422 | 13,827 |  
| Duval | 995,567 | 864,263 | 778,879 |  
| Escambia | 321,905 | 297,619 | 294,410 |  
| Flagler | 115,378 | 95,696 | 49,832 |  
| Franklin | 12,451 | 11,549 | 9,829 |  
| Gadsden | 43,826 | 46,389 | 45,087 |  
| Gilchrist | 17,864 | 16,939 | 14,437 |  
| Glades | 12,126 | 12,884 | 10,576 |  
| Gulf | 14,192 | 15,863 | 14,560 |  
| Hamilton | 14,004 | 14,799 | 13,327 |  
| Hardee | 25,327 | 27,731 | 26,938 |  
| Hendry | 39,619 | 39,140 | 36,210 |  
| Hernando | 194,515 | 172,778 | 130,802 |  
| Highlands | 101,235 | 98,786 | 87,366 |  
| Hillsborough | 1,459,762 | 1,229,226 | 998,948 |
</excerpt>
### Rank 2 of 71 — 0.84
<excerpt title="How many people live in Florida?">
## What are Florida's most populous counties?
| 12073 | Leon County | 300488 |  
| 12001 | Alachua County | 291782 |  
| 12019 | Clay County | 236760 |  
| 12091 | Okaloosa County | 220483 |  
| 12053 | Hernando County | 218150 |  
| 12015 | Charlotte County | 212122 |  
| 12113 | Santa Rosa County | 207653 |  
| 12005 | Bay County | 199718 |  
| 12061 | Indian River County | 172139 |  
| 12017 | Citrus County | 170174 |  
| 12085 | Martin County | 165666 |  
| 12119 | Sumter County | 154693 |  
| 12035 | Flagler County | 136744 |  
| 12055 | Highlands County | 109778 |  
| 12089 | Nassau County | 104376 |  
| 12131 | Walton County | 89666 |  
| 12087 | Monroe County | 80908 |  
| 12107 | Putnam County | 77301 |  
| 12023 | Columbia County | 73977 |  
| 12063 | Jackson County | 49980 |  
| 12075 | Levy County | 47765 |  
| 12121 | Suwannee County | 47536 |  
| 12051 | Hendry County | 46130 |  
| 12039 | Gadsden County | 44151 |  

## What are Florida's most populous counties?
| 12093 | Okeechobee County | 42369 |  
| 12129 | Wakulla County | 37115 |  
| 12027 | DeSoto County | 36744 |  
| 12003 | Baker County | 29325 |  
| 12007 | Bradford County | 28075 |  
| 12133 | Washington County | 26503 |  
| 12049 | Hardee County | 26068 |  
| 12123 | Taylor County | 21843 |  
| 12041 | Gilchrist County | 20233 |  
| 12059 | Holmes County | 19876 |  
| 12079 | Madison County | 18364 |  
| 12029 | Dixie County | 17614 |  
| 12065 | Jefferson County | 15921 |  
| 12045 | Gulf County | 15876 |  
| 12125 | Union County | 15738 |  
| 12047 | Hamilton County | 14334 |  
| 12013 | Calhoun County | 13278 |  
| 12043 | Glades County | 13132 |  
| 12037 | Franklin County | 12979 |  
| 12067 | Lafayette County | 8640 |  
| 12077 | Liberty County | 7955 |
</excerpt>
### Rank 3 of 71 — 0.82
<excerpt title="Demographics of Florida">
### Population by county by year
| Holmes | 19,653 | 19,927 | 18,564 |  
| Indian River | 159,788 | 138,028 | 112,947 |  
| Jackson | 47,319 | 49,746 | 46,755 |  
| Jefferson | 14,510 | 14,761 | 12,902 |  
| Lafayette | 8,226 | 8,870 | 7,022 |  
| Lake | 383,956 | 297,047 | 210,527 |  
| Lee | 760,822 | 618,754 | 440,888 |  
| Leon | 292,198 | 275,487 | 239,452 |  
| Levy | 42,915 | 40,801 | 34,450 |  
| Liberty | 7,974 | 8,365 | 7,021 |  
| Madison | 17,968 | 19,224 | 18,733 |  
| Manatee | 399,710 | 322,833 | 264,002 |  
| Marion | 375,908 | 331,303 | 258,916 |  
| Martin | 158,431 | 146,318 | 126,731 |  
| Miami-Dade (Dade) | 2,701,767 | 2,496,457 | 2,253,779 |  
| Monroe | 82,874 | 73,090 | 79,589 |
</excerpt>
### Rank 4 of 71 — 0.79
<excerpt title="How many people live in Florida?">
## What are Florida's most populous counties?
| 12093 | Okeechobee County | 42369 |  
| 12129 | Wakulla County | 37115 |  
| 12027 | DeSoto County | 36744 |  
| 12003 | Baker County | 29325 |  
| 12007 | Bradford County | 28075 |  
| 12133 | Washington County | 26503 |  
| 12049 | Hardee County | 26068 |  
| 12123 | Taylor County | 21843 |  
| 12041 | Gilchrist County | 20233 |  
| 12059 | Holmes County | 19876 |  
| 12079 | Madison County | 18364 |  
| 12029 | Dixie County | 17614 |  
| 12065 | Jefferson County | 15921 |  
| 12045 | Gulf County | 15876 |  
| 12125 | Union County | 15738 |  
| 12047 | Hamilton County | 14334 |  
| 12013 | Calhoun County | 13278 |  
| 12043 | Glades County | 13132 |  
| 12037 | Franklin County | 12979 |  
| 12067 | Lafayette County | 8640 |  
| 12077 | Liberty County | 7955 |

## What are Florida's most populous cities?
The largest city in Florida is Jacksonville with about 1.01 million residents in 2024.

## Cities and counties in Florida ranked by population
Cities and counties in Florida ranked by population 1.Jacksonville 1,009,833  
2.Miami 487,014  
3.Tampa 414,547  
4.Orlando 334,854  
5.St.Petersburg 267,102  
6.Port St.Lucie 258,575  
7.Hialeah 235,388  
8.Cape Coral 233,025  
9.Tallahassee 205,089  
10.Fort Lauderdale 190,641

## Keep exploring
*    ### Semiquincentennial snapshot: the US at 250 years Jul 1, 2026  
*    ### Which states have the largest elderly populations? Dec 11, 2025  
*    ### What is the poverty rate in Florida? Updates monthly  
*   ### How many people in Florida speak a language other than English at home? Updates annually

## Methodology
USAFacts standardizes data, in areas such as time and demographics, to make it easier to understand and compare.
</excerpt>
### Rank 5 of 71 — 0.77
<excerpt title="Demographics of Florida">
### Population by county by year
| Nassau | 90,352 | 73,314 | 57,663 |  
| Okaloosa | 211,668 | 180,822 | 170,498 |  
| Okeechobee | 39,644 | 39,996 | 35,910 |  
| Orange | 1,429,908 | 1,145,956 | 896,344 |  
| Osceola | 388,656 | 268,685 | 172,493 |  
| Palm Beach | 1,492,191 | 1,320,134 | 1,131,191 |  
| Pasco | 561,891 | 464,697 | 344,768 |  
| Pinellas | 959,107 | 916,542 | 921,495 |  
| Polk | 725,046 | 602,095 | 483,924 |  
| Putnam | 73,321 | 74,364 | 70,423 |  
| St. Johns | 273,425 | 190,039 | 123,135 |  
| St. Lucie | 329,226 | 277,789 | 192,695 |  
| Santa Rosa | 188,000 | 151,372 | 117,743 |  
| Sarasota | 434,006 | 379,448 | 325,961 |  
| Seminole | 470,856 | 422,718 | 365,199 |  

### Population by county by year
| Sumter | 129,752 | 93,420 | 53,345 |  
| Suwannee | 43,474 | 41,551 | 34,844 |  
| Taylor | 21,796 | 22,570 | 19,256 |  
| Union | 16,147 | 15,535 | 13,442 |  
| Volusia | 553,543 | 494,593 | 443,343 |  
| Wakulla | 33,764 | 30,776 | 22,863 |  
| Walton | 75,305 | 55,043 | 40,601 |  
| Washington | 25,318 | 24,896 | 20,973 |  
| Total | 21,538,187 | 18,801,332 | 15,982,824 |
Florida population pyramid
In the 2020 US Census Florida had a median age of 43 years old. The median age was higher for females than males; with the median age being 41.5 for males and 44.5 for females.[[16]](https://en.wikipedia.org/wiki/Demographics_of_Florida#cite_note-16)
</excerpt>

## Search 2 — query: "Florida county 2022 population estimate 2022 census"
### Rank 1 of 231 — 0.85 (passed on)
<excerpt title="Florida Estimates of Population 2022">
## [PDF page 32]
45  Gadsden  43,967  43,826  46,389  45,087  0.20  0.20  0.25  0.28  
46  Hendry  40,633  39,619  39,140  36,210  0.18  0.18  0.21  0.23  
47  Okeechobee  39,385  39,644  39,996  35,910  0.18  0.18  0.21  0.22  
48  Wakulla  35,169  33,764  30,776  22,863  0.16  0.16  0.16  0.14  
49  DeSoto  34,748  33,976  34,862  32,209  0.16  0.16  0.19  0.20

## [PDF page 32]
50  Baker  27,881  28,259  27,115  22,259  0.13  0.13  0.14  0.14  
51  Bradford  27,013  28,303  28,520  26,088  0.12  0.13  0.15  0.16  
52  Hardee  25,544  25,327  27,731  26,938  0.11  0.12  0.15  0.17  
53  Washington  25,461  25,318  24,896  20,973  0.11  0.12  0.13  0.13  
54  Taylor  21,375  21,796  22,570  19,256  0.10  0.10  0.12  0.12
</excerpt>
### Rank 2 of 231 — 0.84
<excerpt title="Florida Estimates of Population 2022">
## [PDF page 45]
11  Okeechobee  22.4  8,775  45  Brevard  18.5  113,822  
12  Santa Rosa  22.3  42,859  46  Franklin  18.5  2,289  
13  Gadsden  22.1  9,699  47  Union  18.5  2,928  
14  Bay  21.8  38,854  48  Hernando  18.4  36,087  
15  Seminole  21.8  104,138  49  Lee  18.4  143,841
16  Putnam  21.7  15,968  50  Marion  18.4  70,162  
17  Wakulla  21.7  7,460  51  Flagler  18.2  21,745  
18  Escambia  21.6  70,080  52  Volusia  18.2  102,280  
19  Madison  21.6  3,906  53  Dixie  18.1  3,034  
20  Columbia  21.5  14,982  54  Alachua  17.9  50,863

## [PDF page 45]
21  St. Johns  21.4  61,200  55  Jefferson  17.9  2,615  
22  Suwannee  21.4  9,332  56  Collier  17.6  67,424  
23  Lafayette  21.3  1,687  57  Gulf  17.3  2,562  
24  St. Lucie  21.0  71,474  58  Highlands  17.3  17,652  
25  Liberty  20.9  1,559  59  Indian River  17.1  27,716
26  Broward  20.8  407,335  60  Glades  16.9  2,050  
27  Holmes  20.8  4,091  61  Pinellas  16.9  162,716  
28  DeSoto  20.7  7,049  62  Martin  15.6  24,767  
29  Washington  20.7  5,169  63  Citrus  14.8  23,102  
30  Walton  20.6  16,050  64  Monroe  14.8  12,313
</excerpt>
### Rank 3 of 231 — 0.84
<excerpt title="Florida Estimates of Population 2022">
## [PDF page 49]
11  St. Lucie  22.9  78,021  45  Glades  11.5  1,390  
12  Alachua  22.3  63,579  46  Dixie  10.8  1,811  
13  Union  20.8  3,282  47  Levy  10.7  4,659  
14  Bradford  20.3  5,676  48  Manatee  10.5  43,005  
15  Palm Beach  20.3  305,282  49  Indian River  10.4  16,742
16  Hillsborough  20.2  301,206  50  Lee  10.1  78,802  
17  Taylor  20.0  4,185  51  Okeechobee  9.3  3,659  
18  Columbia  18.8  13,156  52  Hardee  8.9  2,260  
19  Putnam  17.6  12,959  53  Collier  7.9  30,042  
20  Miami-Dade  17.5  476,852  54  Pasco  7.8  45,011

## [PDF page 49]
21  Polk  17.3  129,131  55  St. Johns  7.7  21,909  
22  Liberty  16.1  1,204  56  Santa Rosa  7.6  14,640  
23  Baker  15.5  4,436  57  Sumter  7.6  10,292  
24  Seminole  15.0  71,689  58  Monroe  7.5  6,268  
25  Osceola  14.9  60,589  59  Nassau  7.5  6,985
26  Washington  14.6  3,637  60  Hernando  7.4  14,619  
27  Marion  14.4  54,848  61  Charlotte  7.0  13,327  
28  Clay  14.2  31,483  62  Martin  6.6  10,509  
29  DeSoto  14.2  4,841  63  Walton  6.5  5,095  
30  Gulf  14.2  2,110  64  Holmes  6.4  1,266
31  Wakulla  14.2  4,870  65  Gilchrist  6.1  1,114  
32  Calhoun  13.9  1,903  66  Sarasota  6.0  26,437  
33  Bay  13.0  23,150  67  Citrus  4.2  6,463
</excerpt>
### Rank 4 of 231 — 0.83
<excerpt title="Florida Estimates of Population 2022">
## [PDF page 32]
40  Putnam  74,249  73,321  74,364  70,423  0.33  0.34  0.40  0.44  
41  Columbia  71,525  69,698  67,531  56,513  0.32  0.32  0.36  0.35  
42  Jackson  48,395  47,319  49,746  46,755  0.22  0.22  0.26  0.29  
43  Suwannee  44,688  43,474  41,551  34,844  0.20  0.20  0.22  0.22  
44  Levy  44,288  42,915  40,801  34,450  0.20  0.20  0.22  0.22

## [PDF page 32]
45  Gadsden  43,967  43,826  46,389  45,087  0.20  0.20  0.25  0.28  
46  Hendry  40,633  39,619  39,140  36,210  0.18  0.18  0.21  0.23  
47  Okeechobee  39,385  39,644  39,996  35,910  0.18  0.18  0.21  0.22  
48  Wakulla  35,169  33,764  30,776  22,863  0.16  0.16  0.16  0.14  
49  DeSoto  34,748  33,976  34,862  32,209  0.16  0.16  0.19  0.20
</excerpt>
### Rank 5 of 231 — 0.83
<excerpt title="Florida Estimates of Population 2022">
## [PDF page 15]
Table 1. Estimates of Population by County and City in Florida, 2022  
(Continued)  
Revenue Sharing Use Only  
April 1  Total  April 1  Estimates  
County, City,  2022  Change  2020  less Inmates  
and State  Estimate  2020–2022  Census  Inmates  April 1, 2022  
Lee County  802,178  41,356  760,822  114  802,064
Bonita Springs  55,502  1,858  53,644  6  55,496  
Cape Coral  208,053  14,037  194,016  27  208,026  
Estero  37,842  903  36,939  0  37,842  
Fort Myers  96,755  10,360  86,395  26  96,729  
Fort Myers Beach  5,589  7  5,582  0  5,589  
Sanibel  6,485  103  6,382  0  6,485  
UNINCORPORATED  391,952  14,088  377,864  55  391,897  
Leon County  299,130  6,932  292,198  1,159  297,971

## [PDF page 15]
Tallahassee  200,289  4,120  196,169  1,141  199,148  
UNINCORPORATED  98,841  2,812  96,029  18  98,823  
Levy County  44,288  1,373  42,915  0  44,288
Bronson  1,147  7  1,140  0  1,147  
Cedar Key  689  2  687  0  689  
Chiefland  2,321  5  2,316  0  2,321  
Fanning Springs (part)  692  -12  704  0  692  
Inglis  1,492  16  1,476  0  1,492  
Otter Creek  108  0  108  0  108  
Williston  3,085  109  2,976  0  3,085  
Yankeetown  585  -3  588  0  585  
UNINCORPORATED  34,169  1,249  32,920  0  34,169  
Liberty County  7,831  -143  7,974  1,410  6,421
</excerpt>

## Search 3 — query: "The White House list of counties named after a founding father"
### Rank 1 of 92 — 0.61 (passed on)
<excerpt title="List of U.S. counties named after presidents of the United States">
## Counties named for Thomas Jefferson
[edit]
22 counties and one parish in the United States are named after Thomas Jefferson (1743–1826), the third president of the United States.
*   Jefferson County, Alabama  
*   Jefferson County, Arkansas  
*   Jefferson County, Florida  
*   Jefferson County, Georgia  
*   Jefferson County, Idaho  
*   Jefferson County, Illinois  
*   Jefferson County, Indiana  
*   Jefferson County, Iowa  
*   Jefferson County, Kansas  
*   Jefferson County, Kentucky  
*   Jefferson County, Mississippi  
*   Jefferson County, Missouri  
*   Jefferson County, Nebraska  
*   Jefferson County, New York  
*   Jefferson County, Ohio  
*   Jefferson County, Oklahoma  
*   Jefferson County, Pennsylvania  
*   Jefferson County, Tennessee  
*   Jefferson County, Texas  
*   Jefferson County, Washington  
*   Jefferson County, West Virginia  
*   Jefferson County, Wisconsin  
*   Jefferson Parish, Louisiana
Three counties were indirectly named for Jefferson:
*   Jefferson County, Colorado: Jefferson is named after the Territory of Jefferson, which in turn is named after Thomas Jefferson.  
*   Jefferson County, Montana: Jefferson is named after the Jefferson River, which in turn is named after Thomas Jefferson.  
*   Jefferson County, Oregon: Jefferson is named after Mount Jefferson on the county's western boundary which in turn is named after Thomas Jefferson.

## Counties named for Andrew Jackson
[edit]
21 counties and one parish in the United States are named after Andrew Jackson (1767–1845), the seventh president of the United States.
*   Jackson County, Alabama  
*   Jackson County, Arkansas  
*   Jackson County, Colorado  
*   Jackson County, Florida  
*   Jackson County, Illinois  
*   Jackson County, Indiana  
*   Jackson County, Iowa  
*   Jackson County, Kansas  
*   Jackson County, Kentucky  
*   Jackson County, Michigan  
*   Jackson County, Mississippi  
*   Jackson County, Missouri  
*   Jackson County, North Carolina  
*   Jackson County, Ohio  
*   Jackson County, Oregon  
*   Jackson County, South Dakota  
*   Jackson County, Tennessee  
*   Jackson County, Texas  
*   Jackson County, West Virginia  
*   Jackson County, Wisconsin  
*   Jackson Parish, Louisiana  
*   Hickory County, Missouri (after Jackson's nickname "Old Hickory")
Three counties named Jackson County are named for individuals other than Andrew Jackson: Jackson County, Georgia is named after James Jackson, the 23rd governor of Georgia. Jackson County, Minnesota is named after Henry Jackson, a member of the first Minnesota Territory legislature. Jackson County, Oklahoma is named after Confederate general Stonewall Jackson.

## Counties named for James Madison
[edit]
18 counties and one parish in the United States are named after James Madison (1751–1836), the fourth president of the United States.
*   Madison County, Alabama  
*   Madison County, Arkansas  
*   Madison County, Florida  
*   Madison County, Georgia  
*   Madison County, Idaho  
*   Madison County, Illinois  
*   Madison County, Indiana  
*   Madison County, Iowa  
*   Madison County, Kentucky  
*   Madison County, Mississippi  
*   Madison County, Missouri  
*   Madison County, New York  
*   Madison County, North Carolina  
*   Madison County, Ohio  
*   Madison County, Tennessee  
*   Madison County, Texas  
*   Madison County, Virginia  
*   Madison Parish, Louisiana
Two counties were indirectly named for Madison:
*   Madison County, Montana is named after the Madison River, which in turn is named for James Madison.  
*   Madison County, Nebraska is probably named for Madison, Wisconsin, which in turn is named after James Madison, where most of the new county's settlers were from._[citation needed_]
</excerpt>
### Rank 2 of 92 — 0.52
<excerpt title="List of U.S. counties named after presidents of the United States">
## Counties named for James Madison
[edit]
18 counties and one parish in the United States are named after James Madison (1751–1836), the fourth president of the United States.
*   Madison County, Alabama  
*   Madison County, Arkansas  
*   Madison County, Florida  
*   Madison County, Georgia  
*   Madison County, Idaho  
*   Madison County, Illinois  
*   Madison County, Indiana  
*   Madison County, Iowa  
*   Madison County, Kentucky  
*   Madison County, Mississippi  
*   Madison County, Missouri  
*   Madison County, New York  
*   Madison County, North Carolina  
*   Madison County, Ohio  
*   Madison County, Tennessee  
*   Madison County, Texas  
*   Madison County, Virginia  
*   Madison Parish, Louisiana
Two counties were indirectly named for Madison:
*   Madison County, Montana is named after the Madison River, which in turn is named for James Madison.  
*   Madison County, Nebraska is probably named for Madison, Wisconsin, which in turn is named after James Madison, where most of the new county's settlers were from._[citation needed_]

## Counties named for Abraham Lincoln
[edit]
16 counties and one parish in the United States are named after Abraham Lincoln (1809–1865), the sixteenth president of the United States.
*   Lincoln County, Arkansas  
*   Lincoln County, Colorado  
*   Lincoln County, Idaho  
*   Lincoln County, Kansas  
*   Lincoln County, Minnesota  
*   Lincoln County, Mississippi  
*   Lincoln County, Montana  
*   Lincoln County, Nebraska  
*   Lincoln County, Nevada  
*   Lincoln County, New Mexico  
*   Lincoln County, Oklahoma  
*   Lincoln County, Oregon  
*   Lincoln County, Washington  
*   Lincoln County, West Virginia  
*   Lincoln County, Wisconsin  
*   Lincoln County, Wyoming  
*   Lincoln Parish, Louisiana
Seven other Lincoln counties exist in the United States; five of these counties are named for Benjamin Lincoln, a general in the American Revolutionary War. Lincoln County, Maine is named after the city of Lincoln, England, and Lincoln County, South Dakota is named after Lincoln County, Maine.

## Counties named for James Monroe
[edit]
17 counties in the United States are named after James Monroe (1758–1831), the fifth president of the United States.
*   Monroe County, Alabama  
*   Monroe County, Arkansas  
*   Monroe County, Florida  
*   Monroe County, Georgia  
*   Monroe County, Illinois  
*   Monroe County, Indiana  
*   Monroe County, Iowa  
*   Monroe County, Kentucky  
*   Monroe County, Michigan  
*   Monroe County, Mississippi  
*   Monroe County, Missouri  
*   Monroe County, New York  
*   Monroe County, Ohio  
*   Monroe County, Pennsylvania  
*   Monroe County, Tennessee  
*   Monroe County, West Virginia  
*   Monroe County, Wisconsin

## Counties named for Ulysses S. Grant
[edit]
11 counties and one parish in the United States are named after Ulysses S. Grant (1822–1885), the eighteenth president of the United States.
*   Grant County, Arkansas  
*   Grant County, Kansas  
*   Grant County, Minnesota  
*   Grant County, Nebraska  
*   Grant County, New Mexico  
*   Grant County, North Dakota  
*   Grant County, Oklahoma  
*   Grant County, Oregon  
*   Grant County, South Dakota  
*   Grant County, Washington  
*   Grant County, West Virginia  
*   Grant Parish, Louisiana
Three other Grant counties exist in the United States. Grant County, Indiana was named after Captains Samuel and Moses Grant of Kentucky. Grant County, Kentucky was named after Samuel Grant, John Grant, and/or Squire Grant, early settlers of Kentucky. Grant County, Wisconsin was named after an early pioneer who opened a trade with local Native Americans.
</excerpt>
### Rank 3 of 92 — 0.50
<excerpt title="List of U.S. counties named after presidents of the United States">
A total of 24 presidents have U.S. counties or county equivalents named after them.
Location of counties named for presidents George Washington, Thomas Jefferson, Andrew Jackson, and Abraham Lincoln, as well as for Benjamin Franklin.
In the United States, a county is an administrative or political subdivision of a U.S. state that consists of a geographic region with specific boundaries and usually some level of governmental authority. Most counties have subdivisions which may include townships, municipalities, and unincorporated areas. Some counties are consolidated city-counties which are simultaneously municipalities and counties.
48 of the 50 U.S. states are subdivided into counties, while the remaining two states and four of the five inhabited territories are subdivided into county equivalents by the state, territory, or the United States Census Bureau.[[a]](https://en.wikipedia.org/wiki/List_of_U.S._counties_named_after_presidents_of_the_United_States#cite_note-1) Louisiana is subdivided into parishes, Alaska is subdivided into boroughs,[[b]](https://en.wikipedia.org/wiki/List_of_U.S._counties_named_after_presidents_of_the_United_States#cite_note-2) and the territories use various other types of subdivisions. Some states also have independent cities, which the United States Census Bureau treats as county equivalents.

## Counties named for George Washington
[edit]
30 counties and one parish in the United States are named after George Washington (1732–1799), the first president of the United States.
*   Washington County, Alabama  
*   Washington County, Arkansas  
*   Washington County, Colorado  
*   Washington County, Florida  
*   Washington County, Georgia  
*   Washington County, Idaho  
*   Washington County, Illinois  
*   Washington County, Indiana  
*   Washington County, Iowa  
*   Washington County, Kansas  
*   Washington County, Kentucky  
*   Washington County, Maine  
*   Washington County, Maryland  
*   Washington County, Minnesota  
*   Washington County, Mississippi  
*   Washington County, Missouri  
*   Washington County, Nebraska  
*   Washington County, New York  
*   Washington County, North Carolina  
*   Washington County, Ohio  
*   Washington County, Oklahoma  
*   Washington County, Oregon  
*   Washington County, Pennsylvania  
*   Washington County, Rhode Island  
*   Washington County, Tennessee  
*   Washington County, Texas  
*   Washington County, Utah  
*   Washington County, Vermont  
*   Washington County, Virginia  
*   Washington County, Wisconsin  
*   Washington Parish, Louisiana

## Counties named for Thomas Jefferson
[edit]
22 counties and one parish in the United States are named after Thomas Jefferson (1743–1826), the third president of the United States.
*   Jefferson County, Alabama  
*   Jefferson County, Arkansas  
*   Jefferson County, Florida  
*   Jefferson County, Georgia  
*   Jefferson County, Idaho  
*   Jefferson County, Illinois  
*   Jefferson County, Indiana  
*   Jefferson County, Iowa  
*   Jefferson County, Kansas  
*   Jefferson County, Kentucky  
*   Jefferson County, Mississippi  
*   Jefferson County, Missouri  
*   Jefferson County, Nebraska  
*   Jefferson County, New York  
*   Jefferson County, Ohio  
*   Jefferson County, Oklahoma  
*   Jefferson County, Pennsylvania  
*   Jefferson County, Tennessee  
*   Jefferson County, Texas  
*   Jefferson County, Washington  
*   Jefferson County, West Virginia  
*   Jefferson County, Wisconsin  
*   Jefferson Parish, Louisiana
Three counties were indirectly named for Jefferson:
*   Jefferson County, Colorado: Jefferson is named after the Territory of Jefferson, which in turn is named after Thomas Jefferson.  
*   Jefferson County, Montana: Jefferson is named after the Jefferson River, which in turn is named after Thomas Jefferson.  
*   Jefferson County, Oregon: Jefferson is named after Mount Jefferson on the county's western boundary which in turn is named after Thomas Jefferson.
</excerpt>
### Rank 4 of 92 — 0.46
<excerpt title="July 4 - Hundreds of U.S. places and counties have patriotic names or pay ...">
# July 4 - Hundreds of U.S. places and counties have patriotic names or pay tribute to Founding Fathers
### More from this section
#### James Bond’s casino chips up for auction for first time
As of July 2024, 164 U.S. places and 126 counties or county equivalents shared at least part of their name with one of the following Founding Fathers: Benjamin Franklin, George Washington, Thomas Jefferson, James Madison, Alexander Hamilton, John Adams, or John Jay.
About 0.8% of incorporated places and 4.0% of counties share at least part of their name with a Founding Father.
“Place” refers to most cities, towns, villages and boroughs.
George Washington is the only Founding Father after whom a state is named. And that state even has a small city named George. The 2020 Census population of George, Washington: 809.
Washington, D.C., the nation’s capital, is also named in his honor.
As of July 2024, there were 55 incorporated places with patriotic names. Topping the list: “Liberty,” with “Independence” a distant second.
The list also includes places with names containing a patriotic reference like Libertyville, Illinois, and Federal Heights, Colorado.
As of July 2024, 0.28% of the nation’s 19,479 incorporated places had names invoking patriotic concepts.

# July 4 - Hundreds of U.S. places and counties have patriotic names or pay tribute to Founding Fathers
### More from this section
#### James Bond’s casino chips up for auction for first time
*   Facebook  
*   Twitter  
*   WhatsApp  
*   [SMS](sms:?body=Check%20out%20this%20link:%20www.fwbusiness.com/tncms/asset/editorial/ebd38456-de34-4748-8a2a-d0611692e86a "SMS")  
*   [Email](mailto:?subject=%5Bfwbusiness.com%5D%20July%204%20-%20Hundreds%20of%20U.S.%20places%20and%20counties%20have%20patriotic%20names%20or%20pay%20tribute%20to%20Founding%20Fathers&body=https%3A%2F%2Fwww.fwbusiness.com%2Fnews%2Farticle_ebd38456-de34-4748-8a2a-d0611692e86a.html%3Futm_medium%3Dsocial%26utm_source%3Demail%26utm_campaign%3Duser-share "Email")  
*   [Print](javascript:window.print() "Print")  
*   Copy article link  
*   Save
</excerpt>
### Rank 5 of 92 — 0.45
<excerpt title="All 46 U.S. Presidents Were Born in Just 21 States but Hundreds of Places ...">
# All 46 U.S. Presidents Were Born in Just 21 States but Hundreds of Places Have Presidential Names
## All 46 U.S. Presidents Were Born in Just 21 States but Hundreds of Places Have Presidential Names
### Fun Facts
*   Of the 45 men who have been or are president of the United States, a third (15) came from just two states: eight from Virginia and seven from Ohio.  
*   Many presidents (29) were born in states that were colonies or former colonies. While there were 13 colonies, 15 states were former colonies because Maine was then part of Massachusetts and Vermont was part of New York.  
*   The top five presidents with matching county names are: Washington (31), Jefferson (26), Jackson (24), Lincoln (24) and Madison (20). Of the 3,143 counties in the United States, 298 match presidential names.  
*   Only eight presidents were born west of the Mississippi. The president born farthest west? Barack Obama in Hawaii. Even though we may think of Ronald Reagan as a Californian because he served as governor of that state, he was born in Illinois. Richard Nixon, however, was born in California and is the only president from the West Coast.
**_Derick Moore is a senior communications specialist at the Census Bureau._**
This article was filed under:
Government
History
Population

# All 46 U.S. Presidents Were Born in Just 21 States but Hundreds of Places Have Presidential Names
## Subscribe
Our email newsletter is sent out on the day we publish a story. Get an alert directly in your inbox to read, share and blog about our newest stories.
Sign Up Today
Contact ourPublic Information Officefor media inquiries or interviews.
*   America Counts Story Who Conducted the First Census in 1790? March 09, 2020 Sixteen U.S. marshals, one territorial governor and their deputies counted 3.929,214 people in the nascent United States.  
*   America Counts Story Who Knew? Famous People Worked for Census June 05, 2018 Telephone inventor Alexander Graham Bell wrote a special Census report on the nation's deaf, mute and blind. Congresswoman Shirley Chisholm was an enumerator.  
*   America Counts Story Constitution Day and the Census September 16, 2019 Sept. 17 is a reminder that the Founding Fathers suggested most of the original census questions and devised how the count determines political representation.

# All 46 U.S. Presidents Were Born in Just 21 States but Hundreds of Places Have Presidential Names
## More Stories
America Counts: Stories
*   Families and Living Arrangements Average U.S. Family Size Just Over Three People November 17, 2026 The size of families living together varies based on householder characteristics.  
*   Population New Estimates Show Population Decline in U.S. Territories Through 2100 November 05, 2026 The new Census Bureau International Database updates population estimates and projections for four U.S. territories and 21 countries.  
*   Population Share of Older Adults With Disabilities Fell at All Education Levels November 03, 2026 New data show that disability rates among older adults declined in 2025, particularly among women and adults with less than a high school education.  
*   Housing Sewers or Septic Systems? How U.S. States Treat Wastewater October 29, 2026 The 2025 American Community Survey out today provides data on what state and type of community rely on public sewer vs. septic systems.
Page Last Revised - April 11, 2024
✕
Is this page helpful?
YesNo
✕
NO THANKS
255 characters maximum255 characters maximum reached
✕
Thank you for your feedback.
Comments or suggestions?
Top
Back to Header
Receive Updates
To sign up for updates please enter your email address.
Enter your email address  Subscribe
* * *
Stay Current
America CountsDirector’s BlogDeputy Director’s BlogRandom SamplingsResearch Matters
Stay Connected
ContactSupportJobs
Follow
Information Quality|Data Linkage Infrastructure|Data Protection and Privacy Policy|Accessibility|FOIA|Inspector General|No FEAR Act|U.S. Department of Commerce|USA.gov
* * *
Measuring America's People and Economy
loading
</excerpt>

## Search 4 — query: "Florida county named after founding father Washington Jefferson Monroe"
### Rank 1 of 68 — 0.82 (passed on)
<excerpt title="The evolution of the state of Florida's counties historic maps and ...">
#### Created Counties
*   Escambia  
*   St. Johns
Duval County — named for then-Governor William Pope Duval — is created in the northern area of St. Johns County, above the mouth of the Suwannee River.
Jackson County — named after former Governor Andrew Jackson — is created in the area of Escambia County between the Chocwatachee and Suwannee rivers.
*   Duval  
*   Jackson
Gadsden County is created in the area of Jackson County between the Apalachicola River and the Suwannee River, taking its name from James Gadsden, Jackson’s former aide.
The southern area of St. Johns County — south of the Caloosahatchee River and Lake Okeechobee — becomes Monroe County, named for then-President James Monroe.
*   Gadsden  
*   Monroe
The panhandle is further subdivided with the addition of Walton and Leon counties, the latter named for Ponce de León who led the first European expedition of Florida.
East of the Suwannee River St. Johns County is greatly downsized, having a majority of its former sprawl become Mosquito County. Alachua County is also formed at this time, comprising the western halves of Duval and St Johns counties.
Finally, the northern area of Duval County becomes Nassau County, named after the German Duchy of Nassau.
*   Walton  
*   Leon  
*   Alachua  
*   Mosquito  
*   Nassau
Washington County, named after former President George Washington, is formed from the western half of Jackson County.
*   Washington
Leon County is divided in to four counties. From West to East: Leon County — now a fraction of its former size, Jefferson County, Madison County, and Hamilton County. The new counties are named after former Presidents Thomas Jefferson and James Madison, as well as founding father and former Secretary of the Treasury Alexander Hamilton.
*   Jefferson  
*   Madison  
*   Hamilton
The southern section of Gadsden County becomes Franklin County, after Benjamin Franklin, while the northern reached of Alachua County become Columbia County, after an old poetic name for America.
Fayette County was also created in name, but never assigned any territory. Thus it is listed below, but cannot be found on the map.
*   Columbia  
*   Franklin  
*   Fayette
</excerpt>
### Rank 2 of 68 — 0.80
<excerpt title="The evolution of the state of Florida's counties historic maps and ...">
#### Spanish Colonies
“Under Spanish rule, Florida was divided by the natural separation of the Suwanee River into West Florida and East Florida.
Upon the purchase of Florida, (1819) by the United States of America, West Florida and East Florida became two counties: Escambia County and St Johns County, so named and so ordained as counties with respective county governments by Andrew Jackson, Military Governor of the Territory of Florida.”

#### Spanish Colonies
##### Text from Territory of Florida Map 1. Historic Florida maps provided courtesy of the University of Florida.
Escambia and St. Johns counties, each named for Florida rivers, are created in the areas that were formerly East and West Florida, respectively, by military ordinance under Governor Andrew Jackson.

#### Created Counties
*   Escambia  
*   St. Johns
Duval County — named for then-Governor William Pope Duval — is created in the northern area of St. Johns County, above the mouth of the Suwannee River.
Jackson County — named after former Governor Andrew Jackson — is created in the area of Escambia County between the Chocwatachee and Suwannee rivers.
*   Duval  
*   Jackson
Gadsden County is created in the area of Jackson County between the Apalachicola River and the Suwannee River, taking its name from James Gadsden, Jackson’s former aide.
The southern area of St. Johns County — south of the Caloosahatchee River and Lake Okeechobee — becomes Monroe County, named for then-President James Monroe.
*   Gadsden  
*   Monroe
The panhandle is further subdivided with the addition of Walton and Leon counties, the latter named for Ponce de León who led the first European expedition of Florida.
East of the Suwannee River St. Johns County is greatly downsized, having a majority of its former sprawl become Mosquito County. Alachua County is also formed at this time, comprising the western halves of Duval and St Johns counties.
Finally, the northern area of Duval County becomes Nassau County, named after the German Duchy of Nassau.
*   Walton  
*   Leon  
*   Alachua  
*   Mosquito  
*   Nassau
Washington County, named after former President George Washington, is formed from the western half of Jackson County.
*   Washington
Leon County is divided in to four counties. From West to East: Leon County — now a fraction of its former size, Jefferson County, Madison County, and Hamilton County. The new counties are named after former Presidents Thomas Jefferson and James Madison, as well as founding father and former Secretary of the Treasury Alexander Hamilton.
*   Jefferson  
*   Madison  
*   Hamilton
The southern section of Gadsden County becomes Franklin County, after Benjamin Franklin, while the northern reached of Alachua County become Columbia County, after an old poetic name for America.
Fayette County was also created in name, but never assigned any territory. Thus it is listed below, but cannot be found on the map.
*   Columbia  
*   Franklin  
*   Fayette
</excerpt>
### Rank 3 of 68 — 0.72
<excerpt title="Monroe County, Florida">
**Monroe County** is the southernmost county of the state of Florida.[[1]](https://en.wikipedia.org/wiki/Monroe_County,_Florida#cite_note-1) As of the 2020 census, the population was 82,874.[[2]](https://en.wikipedia.org/wiki/Monroe_County,_Florida#cite_note-census-2) Its county seat is Key West.[[3]](https://en.wikipedia.org/wiki/Monroe_County,_Florida#cite_note-GR6-3) Monroe County includes the islands of the Florida Keys and comprises the Key West-Key Largo Micropolitan Statistical Area. Over 99.9% of the county's population lives on the Florida Keys. The mainland, which is part of the Everglades, comprises 87% of the county's land area and is virtually uninhabited with only 17 people recorded in the 2020 census.[[4]](https://en.wikipedia.org/wiki/Monroe_County,_Florida#cite_note-4)
Monroe County was created in 1823. It was named for James Monroe, the fifth president of the United States from 1817 to 1825.[[5]](https://en.wikipedia.org/wiki/Monroe_County,_Florida#cite_note-5)
According to the U.S. Census Bureau, the county has a total area of 3,738 square miles (9,680 km 2), of which 983 square miles (2,550 km 2) (26.3%) is land and 2,754 square miles (7,130 km 2) (73.7%) is water.[[6]](https://en.wikipedia.org/wiki/Monroe_County,_Florida#cite_note-GR1-6) It is the largest county in Florida by total area.
More than 99.9 percent of the Monroe County population lives in the island chain known as the Florida Keys.

Two thirds of the large area in what local residents call "mainland Monroe" is uninhabited by virtue of being part of the Everglades National Park, and the remainder by the Big Cypress National Preserve in the northeastern interior. The area, officially named Cape SableCensus County Division, is virtually uninhabited. This area has 87.4 percent of the county's land area (859.6 out of 983 sq mi (2,546 km 2)), but it had only 0.022 percent of the county's population (18 out of 82,170) as of the 2021 American Community Survey. The Census Bureau defines this area as Census Tract 9800 of Monroe County, Florida.[[7]](https://en.wikipedia.org/wiki/Monroe_County,_Florida#cite_note-7)
In mainland Monroe, the only three populated places appearing on detailed maps and in the USGS geographic name database are Flamingo, Pinecrest, (not to be confused with much larger Pinecrest of neighboring Miami-Dade County), and Trail City. Flamingo, on the south coast and at the end of State Road 9336 (Flamingo Lodge Highway), is the location of the Flamingo Lodge and the Flamingo Ranger Station (with Visitor Center & Marina). 7 mi (11 km) northeast on the highway is the West Lake Trail (station). Pinecrest, located in the northern interior of the county (in the Big Cypress National Preserve) on Loop Road (given that name since it forms a loop with U.S. Highway 41 further north), hosts the Loop Road Education Center. Trail City is 4 mi (6 km) west of Pinecrest on Loop Road. Loop Road can be found on most maps as CR 94, although the roadway no longer has a numbered designation and is now managed by the National Park Service.
Between the south coast of Florida's mainland and the Florida Keys is Florida Bay, which is encompassed by the Everglades National Park and contains numerous islets or keys.
</excerpt>
### Rank 4 of 68 — 0.70
<excerpt title="Monroe County, Florida">
Parts of this article (those related to rebuilding following hurricanes, specifically the 2017 Hurricane Irma, and developing discussions of urban resilience, climate resilience, and planning) need to be **updated**. Please help update this article to reflect recent events or newly available information._(September 2017)_
| Monroe County, Florida |  
| --- |  
| County |  
|  The Monroe County Courthouse in Key West |  
|  Flag  Seal |  
|  Location within the U.S. state of Florida |  
| Coordinates: 25°07′N 81°09′W / 25.12°N 81.15°W |  
| Country | United States |  
| State | Florida |  
| Founded | July 3, 1823 |  
| Named for | James Monroe |  
| Seat | Key West |  
| Largest city | Key West |  
| Area |  
| •Total | 3,738 sq mi (9,680 km 2) |  
| •Land | 983 sq mi (2,550 km 2) |  
| •Water | 2,754 sq mi (7,130 km 2) 73.7% |  
| Population (2020) |  
| •Total | 82,874 |  
| •Estimate (2025) | 80,406  |  
| •Density | 84.3/sq mi (32.6/km 2) |  
| Time zone | UTC−5 (Eastern) |  
| •Summer (DST) | UTC−4 (EDT) |  
| Congressional district | [28th](https://en.wikipedia.org/wiki/Florida's_28th_congressional_district "Florida's 28th congressional district") |  
| Website | www.monroecounty-fl.gov |

**Monroe County** is the southernmost county of the state of Florida.[[1]](https://en.wikipedia.org/wiki/Monroe_County,_Florida#cite_note-1) As of the 2020 census, the population was 82,874.[[2]](https://en.wikipedia.org/wiki/Monroe_County,_Florida#cite_note-census-2) Its county seat is Key West.[[3]](https://en.wikipedia.org/wiki/Monroe_County,_Florida#cite_note-GR6-3) Monroe County includes the islands of the Florida Keys and comprises the Key West-Key Largo Micropolitan Statistical Area. Over 99.9% of the county's population lives on the Florida Keys. The mainland, which is part of the Everglades, comprises 87% of the county's land area and is virtually uninhabited with only 17 people recorded in the 2020 census.[[4]](https://en.wikipedia.org/wiki/Monroe_County,_Florida#cite_note-4)
Monroe County was created in 1823. It was named for James Monroe, the fifth president of the United States from 1817 to 1825.[[5]](https://en.wikipedia.org/wiki/Monroe_County,_Florida#cite_note-5)
According to the U.S. Census Bureau, the county has a total area of 3,738 square miles (9,680 km 2), of which 983 square miles (2,550 km 2) (26.3%) is land and 2,754 square miles (7,130 km 2) (73.7%) is water.[[6]](https://en.wikipedia.org/wiki/Monroe_County,_Florida#cite_note-GR1-6) It is the largest county in Florida by total area.
More than 99.9 percent of the Monroe County population lives in the island chain known as the Florida Keys.
</excerpt>
### Rank 5 of 68 — 0.67
<excerpt title="Monroe County Maps - Florida Center for Instructional Technology">
> _Click on a thumbnail image to view a full size version of that map._  
>   
>   
> Monroe County is Florida's 6 th county, established on July 3, 1823, from a segment of St. Johns County. It gains its name from James Monroe (1758-1832), the 5 th President of the United States (1817-1825). One of his achievements was obtaining the Floridas from Spain. Key West is the county seat.  
>   
>   
> For earlier maps of this area, visit the St. Johns County map gallery.
Record 1 to 25 of 90  
Detail - Geographical, statistical, and historical map of Florida, 1827
_This detail of a 1827 map shows major rivers, lakes, coastal features, settlements, and roads in Monroe County. The county is crossed by many waterways including the Caloosahatchee River, the Youngs River, and Gallivans Creek. The coast line features..._
Monroe County, 1830
_Digitization provided by the USF Libraries Digitization Center. Rare Maps. This is a map of Monroe County, circa 1830. It is a portion of Rand McNally and Co.'s new business map of Florida. It shows county boundaries, Florida Keys, Florida Reefs, inl..._
Monroe County, 1832
_Digitization provided by the USF Libraries Digitization Center. Rare Maps. This is a map of Monroe County, circa 1832. It shows county boundaries, cities and towns and inland waters. Key West is shown as Thompsons Island on this map. Scale ca. 1:4,1..._
[Monroe County, 1834
_Digitization provided by the USF Libraries Digitization Center. Rare Maps. This is a detail map of Monroe county circa 1834 when it encompassed the entire southern portion of Florida and the Florida Keys. It shows main towns and cities including Key ..._
Detail - Florida, 1839

_This detail of a map from the Tanner's Universal Atlas shows towns, forts, roads, canals, major rivers and lakes in Monroe County. This detail shows many forts including Fort Denaud, Fort Dulaney, and Fort Keais. Along the coastline, there are severa..._
Detail - Map of the State of Florida, 1842
_This detail of a 1842 map of Florida shows roads, railroads, counties, forts, naval depots and other military installations, major towns, rivers, and lakes for the Monroe County. Several waterways traverse Monroe County including Delaware River, Nort..._
Monroe County, 1845
_A map of Monroe County as of 1845 showing rivers and the Everglades...._
Monroe County, 1845
_Meyer's 1845 map of Florida is derived from the Tanner/Mitchell Universal atlas map of 1839. This detail of that map covers Monroe County. Routes of travel are covered along with major waterways. The Everglades expand over the majority of the detail...._
Monroe County, 1850
_Meyer's 1850 map of Florida is derived from the Tanner/Mitchell Universal atlas map of 1839, and similar to the 1845 maps. In this updated detail of Monroe County, waterways and townships are noted. Coastal creeks and rivers are shown such as Rio Rat..._
Monroe County, 1856
_This detail of a map from the annual report of the Surveyor General in 1856 shows Monroe County. Drainage, cities and towns, roads, trails, and location of railroad lines are shown in great detail. The major feature of detail is the Everglades. Other..._
Monroe County, 1857
_A map of Monroe County as of 1857 showing towns, forts, bodies of water, and the Everglades...._
Indian Territory in South Florida, 1859
_Map of an area designated as Indian Territory taken from a 1859 railroad map of Florida. The area includes a portion of Monroe County northwest of the Everglades. Township grids based on the Tallahassee basis parallel and the Tallahassee prime meridi..._
The Florida Keys, 1859
</excerpt>

## Search 5 — query: "White House founding fathers list"
### Rank 1 of 126 — 0.68 (passed on)
<excerpt title="The United States Constitution: The Founding Fathers - Research Guides">
# The United States Constitution: The Founding Fathers
## Biographies
From biography.com:
*   John Adams  
*   Samuel Adams  
*   Benjamin Franklin  
*   Alexander Hamilton  
*   Patrick Henry  
*   Thomas Jefferson  
*   James Madison  
*   James Monroe  
*   Thomas Paine  
*   George Washington
Read biographies of the founding fathers from the National Constitution Center here. This list includes short biographies of not just the major figures, but all of the delegates to the Constitutional Convention.
If you want to see the writings of some of the major Founders, visit the National Archives' Founders Online database. It contains over 183,000 papers and other documents by George Washington, Benjamin Franklin, John & Abigail Adams, Thomas Jefferson, Alexander Hamilton, James Monroe, and James Madison.

# The United States Constitution: The Founding Fathers
## Other Resources
Given their importance in American history, it's not surprising that hundreds of books have been written about the founders and their lives. Below is a list of just a few of these books.
**Individual Biographies:**
Ammon, Harry. _James Monroe: The Quest for National Identity_. 1990
Cheney, Lynne. _James Madison: A Life Reconsidered_. 2015
Chernow, Ron. _Alexander Hamilton_. 2005
Chernow, Ron. _Washington: A Life_. 2011
Ellis, Joseph. _Passionate Sage: The Character and Legacy of John Adams_. 2001
Flexner, James T. _George Washington: The Indispensable Man_. 1994
Franklin, Benjamin. _The Autobiography of Benjamin Franklin_. 1996
Isaacson, Walter. _Benjamin Franklin: An American Life_. 2004
McCullough, David. _John Adams_. 2002
Meacham, Jon. _Thomas Jefferson: The Art of Power_. 2012
Nelson, Craig. _Thomas Paine: Enlightenment, Revolution, and the Birth of Modern Nations_. 2007
Stoll, Ira. _Samuel Adams: A Life_. 2009
Unger,Harlow Giles._Lion of Liberty: Patrick Henry and the Call to a New Nation_. 2011
**Group Biographies:**
Ellis, Joseph. _Founding__Brothers: The Revolutionary Generation_. 2002
Ellis, Joseph. _The Quartet: Orchestrating the Second American Revolution, 1783-1789_. 2016
Kiernan, Denise. _Signing Their Rights Away: The Fame and Misfortune of the Men Who Signed the United States Constitution_. 2011
McCullough, David. _1776_. 2006
Roberts, Cokie. _Founding Mothers: The Women Who Raised Our Nation_. 2005
Roberts, Cokie. _Ladies of Liberty: The Women Who Shaped Our Nation_. 2009

# The United States Constitution: The Founding Fathers
## Other Resources
Vile, John R. _The Men Who Made the Constitution: Lives of the Delegates to the Constitutional Convention_. 2013
Wood, Gordon S. _Revolutionary Characters: What Made the Founders Different_. 2007
*   <<**Previous:** History of the Constitution  
*   **Next:** Constitutional Amendments: The Bill of Rights >>

*   Last Updated:Feb 2, 2026 3:21 PM  
*   URL:https://law.tamu.libguides.com/usconstitution  
*   [Print Page](javascript: window.print();)
Login to LibApps
Subjects:
*   Subject Guides
[](javascript:void(0); "Back to Top")
</excerpt>
### Rank 2 of 126 — 0.68
<excerpt title="Wikipedia">
The criticisms are what led to the amendments proposed under the Bill of Rights. Madison, the bill's principal author, was originally opposed to the amendments, but was influenced by the 1776 Virginia Declaration of Rights, primarily written by Mason, and the Declaration of Independence, by Thomas Jefferson.[253] Jefferson, while in France, shared Henry's and Mason's fears about a strong central government, especially the president's power, but because of his friendship with Madison and the pending Bill of Rights, he quieted his concerns.[254] Alexander Hamilton, however, was opposed to a Bill of Rights believing the amendments not only unnecessary but dangerous:
Why declare things shall not be done, which there is no power to do ... that the liberty of the press shall not be restrained, when no power is given by which restrictions may be imposed?[255]
Madison had no way of knowing the debate between Virginia's two legislative houses would delay the adoption of the amendments for more than two years.[256] The final draft, referred to the states by the federal Congress on September 25, 1789,[257] was not ratified by Virginia's Senate until December 15, 1791.[256]  
The Bill of Rights drew its authority from the consent of the people and held that,
The enumeration in the Constitution, of certain rights, shall not be construed to deny or disparage others retained by the people.  
— Article 11.
The powers not delegated to the United States by the Constitution, nor prohibited by it to the States, are reserved to the States respectively, or to the people.  
— Article 12.[258]
Madison came to be recognized as the founding era's foremost proponent of religious liberty, free speech, and freedom of the press.[259]
Ascending to the presidency
The first five U.S. presidents are regarded as Founding Fathers for their active participation in the American Revolution: Washington, John Adams, Jefferson, Madison, and Monroe. Each of them served as a delegate to the Continental Congress.[260]
</excerpt>
### Rank 3 of 126 — 0.65
<excerpt title="The United States Constitution: The Founding Fathers - Research Guides">
# The Founding Fathers - The United States Constitution - Research Guides at Texas A&M University School of Law
Skip to Main Content
1.   Dee J. Kelly Law Library  
2.   Research Guides  
3.   The United States Constitution  
4.   The Founding Fathers
Search this Guide  Search

# The United States Constitution: The Founding Fathers
Resources for researching the history, drafting, interpretation, and other elements of the U.S. Constitution.
*   Introduction  
*   History of the Constitution  
*   The Founding Fathers  
    *   Introduction  
    *   Biographies  
    *   Other Resources

*   Constitutional Amendments: The Bill of Rights  
*   Constitutional Amendments: Amendments 11-27  
*   Constitutional Law & Interpretation  
*   The Constitution in American Life  
*   Find Out More!

# The United States Constitution: The Founding Fathers
## Introduction
"The Founding Fathers" is the name collectively given to several historical figures who played pivotal roles in America's independence from Great Britain and the establishment of the United States government. While the names included on the list vary, they often include John Adams, Samuel Adams, Benjamin Franklin, Alexander Hamilton, Patrick Henry, Thomas Jefferson, James Madison, James Monroe, Thomas Paine and George Washington. The name can also refer to the members of the Constitutional Convention, the signers of the Declaration of Independence, and/or the drafters of the Constitution.
There is a similar group known as the "Founding Mothers", women who, through their writings and actions, influenced the creation of the new government. This group includes Abigail Adams, Deborah Franklin, Dolley Madison, Eliza Pinckney, Martha Washington and Mercy Otis Warren, among others.

# The United States Constitution: The Founding Fathers
## Biographies
From biography.com:
*   John Adams  
*   Samuel Adams  
*   Benjamin Franklin  
*   Alexander Hamilton  
*   Patrick Henry  
*   Thomas Jefferson  
*   James Madison  
*   James Monroe  
*   Thomas Paine  
*   George Washington
Read biographies of the founding fathers from the National Constitution Center here. This list includes short biographies of not just the major figures, but all of the delegates to the Constitutional Convention.
If you want to see the writings of some of the major Founders, visit the National Archives' Founders Online database. It contains over 183,000 papers and other documents by George Washington, Benjamin Franklin, John & Abigail Adams, Thomas Jefferson, Alexander Hamilton, James Monroe, and James Madison.
</excerpt>
### Rank 4 of 126 — 0.64
<excerpt title="Wikipedia">
Jump to content  
Main menu  
Search  
Donate  
Create account  
Log in  
Contents hide  
(Top)  
Historical founders  
Origin of phrase  
List of Founding Fathers  
Toggle List of Founding Fathers subsection  
The colonies unite (1765–1774)  
Continental Congress (1774–1775)  
Toggle Continental Congress (1774–1775) subsection  
Declaration of Independence (1776)  
Fighting for independence  
Toggle Fighting for independence subsection  
Constitutional Convention  
Toggle Constitutional Convention subsection  
Ascending to the presidency  
Demographics and other characteristics  
Toggle Demographics and other characteristics subsection  
Religion  
Founders on currency and postage  
Political and cultural impact  
Toggle Political and cultural impact subsection  
Religious freedom  
Slavery  
Toggle Slavery subsection  
Scholarly analysis  
Toggle Scholarly analysis subsection  
See also  
Notes  
Citations  
Bibliography  
Toggle Bibliography subsection  
Further reading  
Toggle Further reading subsection  
External links  
Founding Fathers of the United States  
67 languages  
Article  
Talk  
Read  
View source  
View history  
Save  
Tools  
Appearance hide  
From Wikipedia, the free encyclopedia  
"Founding Fathers" redirects here. For the founding fathers of other countries, see List of national founders.  
Founding Fathers of the United States  
1760s–1820s
The Committee of Five (Adams, Sherman, Livingston, Jefferson, and Franklin) present their draft of the Declaration of Independence to the Second Continental Congress in Philadelphia on June 28, 1776, as depicted in John Trumbull's 1818 portrait.
Location	Thirteen Colonies  
Including	Signers of the Declaration of Independence (1776), Articles of Confederation (1781), and United States Constitution (1789)  
Leaders	  
John Adams  
Samuel Adams  
Benjamin Franklin  
Alexander Hamilton  
John Hancock  
Patrick Henry  
John Jay  
Thomas Jefferson  
Richard Henry Lee  
Robert R. Livingston  
James Madison  
George Mason  
Robert Morris  
Peyton Randolph  
Roger Sherman  
Joseph Warren  
George Washington  
James Wilson
</excerpt>
### Rank 5 of 126 — 0.64
<excerpt title="Category:Founding Fathers of the ...">
# Category:Founding Fathers of the United States
## Pages in category "Founding Fathers of the United States"
### L
*   Marquis de Lafayette  
*   John Langdon (politician)  
*   Edward Langworthy (Founding Father)  
*   [John Lansing Jr.](https://en.wikipedia.org/wiki/John_Lansing_Jr. "John Lansing Jr.")  
*   Henry Laurens  
*   Francis Lightfoot Lee  
*   Richard Henry Lee  
*   Francis Lewis  
*   Philip Livingston  
*   Robert R. Livingston  
*   William Livingston  
*   James Lovell (politician)  
*   [Thomas Lynch Jr.](https://en.wikipedia.org/wiki/Thomas_Lynch_Jr. "Thomas Lynch Jr.")

# Category:Founding Fathers of the United States
## Pages in category "Founding Fathers of the United States"
### M
*   Henry Marchant  
*   John Marshall  
*   Alexander Martin  
*   Luther Martin  
*   George Mason  
*   John Mathews (lawyer)  
*   James McClurg  
*   James McHenry  
*   Thomas McKean  
*   John Francis Mercer  
*   Arthur Middleton  
*   Thomas Mifflin  
*   James Monroe  
*   Gouverneur Morris  
*   Lewis Morris  
*   Robert Morris (financier)  
*   John Morton (American politician)

# Category:Founding Fathers of the United States
## Pages in category "Founding Fathers of the United States"
### N
*   [Thomas Nelson Jr.](https://en.wikipedia.org/wiki/Thomas_Nelson_Jr. "Thomas Nelson Jr.")

# Category:Founding Fathers of the United States
## Pages in category "Founding Fathers of the United States"
### P
*   William Paca  
*   Robert Treat Paine  
*   Thomas Paine  
*   William Paterson (judge)  
*   John Penn (North Carolina politician)  
*   William Pierce (Georgia politician)  
*   Charles Pinckney (governor)  
*   Charles Cotesworth Pinckney

# Category:Founding Fathers of the United States
## Pages in category "Founding Fathers of the United States"
### R
*   Edmund Randolph  
*   Peyton Randolph  
*   George Read (American politician, born 1733)  
*   Joseph Reed (politician)  
*   Daniel Roberdeau  
*   Caesar Rodney  
*   George Ross (American politician)  
*   Benjamin Rush  
*   Edward Rutledge  
*   John Rutledge

# Category:Founding Fathers of the United States
## Pages in category "Founding Fathers of the United States"
### S
*   Nathaniel Scudder  
*   James Smith (Pennsylvania politician)  
*   Jonathan Bayard Smith  
*   Richard Dobbs Spaight  
*   Richard Stockton (Continental Congressman)  
*   Thomas Stone  
*   Caleb Strong

# Category:Founding Fathers of the United States
## Pages in category "Founding Fathers of the United States"
### T
*   George Taylor (Pennsylvania politician)  
*   Edward Telfair  
*   Charles Thomson  
*   Matthew Thornton

# Category:Founding Fathers of the United States
## Pages in category "Founding Fathers of the United States"
### V
*   Nicholas Van Dyke (politician, born 1738)
</excerpt>

## Search 6 — query: "White House founding fathers list John Adams Benjamin Franklin Alexander Hamilton"
### Rank 1 of 124 — 0.81 (passed on)
<excerpt title="Founding Fathers of the United States">
Name	Province/state	DI (1776)	AC (1777)	USC (1787)  
Andrew Adams	Connecticut		Yes	  
John Adams	Massachusetts	Yes		  
Samuel Adams	Yes	Yes	  
Thomas Adams	Virginia		Yes	  
Abraham Baldwin	Georgia			Yes  
John Banister	Virginia		Yes	  
Josiah Bartlett	New Hampshire	Yes	Yes	  
Richard Bassett	Delaware			Yes  
Gunning Bedford Jr.			Yes  
John Blair Jr.	Virginia			Yes  
William Blount	North Carolina			Yes  
Carter Braxton	Virginia	Yes		  
David Brearley	New Jersey			Yes  
Jacob Broom	Delaware			Yes  
Pierce Butler	South Carolina			Yes  
Charles Carroll	Maryland	Yes		  
Daniel Carroll		Yes	Yes  
Samuel Chase	Yes		  
Abraham Clark	New Jersey	Yes		  
William Clingan	Pennsylvania		Yes	  
George Clymer	Yes		Yes  
John Collins	Rhode Island		Yes	  
Francis Dana	Massachusetts		Yes	  
Jonathan Dayton	New Jersey			Yes  
John Dickinson	Delaware		Yes	Yes  
William Henry Drayton	South Carolina		Yes	  
James Duane	New York		Yes	  
William Duer		Yes	  
William Ellery	Rhode Island	Yes	Yes	  
William Few	Georgia			Yes  
Thomas Fitzsimons	Pennsylvania			Yes  
William Floyd	New York	Yes		  
Benjamin Franklin	Pennsylvania	Yes		Yes  
Elbridge Gerry	Massachusetts	Yes	Yes	  
Nicholas Gilman	New Hampshire			Yes  
Nathaniel Gorham	Massachusetts			Yes  
Button Gwinnett	Georgia	Yes		  
Lyman Hall	Yes		  
Alexander Hamilton	New York			Yes  
John Hancock	Massachusetts	Yes	Yes	  
John Hanson	Maryland		Yes	  
Cornelius Harnett	North Carolina		Yes	  
Benjamin Harrison V	Virginia	Yes		  
John Hart	New Jersey	Yes		  
John Harvie	Virginia		Yes	  
Joseph Hewes	North Carolina	Yes		  
Thomas Heyward Jr.	South Carolina	Yes	Yes	  
Samuel Holten	Massachusetts		Yes	  
William Hooper	North Carolina	Yes
</excerpt>
### Rank 2 of 124 — 0.79
<excerpt title="Founding Fathers of the United States">
After Washington's final victory at the surrender at Yorktown on October 19, 1781, more than a year passed before official negotiations for peace commenced. The Treaty of Paris was drafted in November 1782, and negotiations began in April 1783. The completed treaty was signed on September 3. Benjamin Franklin, John Adams, John Jay and Henry Laurens represented the United States,[183] while David Hartley, a member of Parliament, and Richard Oswald, a prominent and influential Scottish businessman, represented Great Britain.[184][185]
Franklin, who had a long-established rapport with the French and was almost entirely responsible for securing an alliance with them a few months after the start of the war, was greeted with high honors from the French council, while the others received due accommodations but were generally considered to be amateur negotiators.[186] Communications between Britain and France were largely effected through Franklin and Lord Shelburne who was on good terms with Franklin.[187] Franklin, Adams and Jay understood the concerns of the French at this uncertain juncture and, using that to their advantage, in the final sessions of negotiations convinced both the French and the British that American independence was in their best interests.[188]
Constitutional Convention  
Main article: Constitutional Convention (United States)  
Scene at the Signing of the Constitution of the United States, a 1940 portrait by Howard Chandler Christy depicting the 1787 Constitutional Convention in Philadelphia
Under the Articles of Confederation, the Congress of the Confederation had no power to collect taxes, regulate commerce, pay the national debt, conduct diplomatic relations, or effectively manage the western territories.[189][190][191] Key leaders – George Washington, Thomas Jefferson, Alexander Hamilton, James Madison, and others – began fearing for the young nation's fate.[192] As the Articles' weaknesses became more and more apparent, the idea of creating a strong central government gained support, leading to the call for a convention to amend the Articles.[193][194]
</excerpt>
### Rank 3 of 124 — 0.77
<excerpt title="Founding Fathers of the United States">
Key events	  
Stamp Act  
Boston Tea Party  
Intolerable Acts  
American Revolutionary War  
Lee Resolution  
Declaration of Independence  
Articles of Confederation  
Treaty of Paris  
United States Constitution  
Bill of Rights  
This article is part of a series on the  
History of the  
United States
The ratification of the U.S. Constitution in Philadelphia in 1787 (by Howard Chandler Christy, 1940)
Timeline and periods
Topics
Groups
Places
OutlineList of yearsHistoriography  
 Category Portal
vte  
George Washington, a key Founding Father, was commanding general of the Continental Army during the Revolutionary War and a Revolutionary hero, presided over the Constitutional Convention and became the nation's first president in April 1789.[1]
The Founding Fathers of the United States, referred to as the Founding Fathers or the Founders by Americans, were a group of late-eighteenth-century American revolutionary leaders who united the Thirteen Colonies, oversaw the War of Independence from Great Britain, established the United States of America, and crafted a framework of government for the new nation.
The Founding Fathers include those who wrote and signed the United States Declaration of Independence, the Articles of Confederation, and the Constitution of the United States, certain military personnel who fought in the American Revolutionary War, and others who greatly assisted in the nation's formation. The single person most identified as Father of the United States is George Washington, commanding general in the American Revolution and the nation's first president. In 1973, the historian Richard B. Morris identified seven figures as key founders, based on what he called the "triple tests" of leadership, longevity, and statesmanship: John Adams, Benjamin Franklin, Alexander Hamilton, John Jay, Thomas Jefferson, James Madison, and Washington.[2]
Most of the Founding Fathers had ancestry traceable back to England, though many had family roots extending across the other regions of the British Isles: Scotland, Wales, and Ireland. Additionally, some traced their lineage back to the early Dutch settlers of New York (New Netherland) during the colonial era, while others were descendants of French Huguenots who settled in the British Thirteen Colonies, escaping religious persecution in France.[3][4][5] Many of them were wealthy merchants, lawyers, and landowners.
</excerpt>
### Rank 4 of 124 — 0.77
<excerpt title="Founding Fathers of the United States">
Jump to content  
Main menu  
Search  
Donate  
Create account  
Log in  
Contents hide  
(Top)  
Historical founders  
Origin of phrase  
List of Founding Fathers  
Toggle List of Founding Fathers subsection  
The colonies unite (1765–1774)  
Continental Congress (1774–1775)  
Toggle Continental Congress (1774–1775) subsection  
Declaration of Independence (1776)  
Fighting for independence  
Toggle Fighting for independence subsection  
Constitutional Convention  
Toggle Constitutional Convention subsection  
Ascending to the presidency  
Demographics and other characteristics  
Toggle Demographics and other characteristics subsection  
Religion  
Founders on currency and postage  
Political and cultural impact  
Toggle Political and cultural impact subsection  
Religious freedom  
Slavery  
Toggle Slavery subsection  
Scholarly analysis  
Toggle Scholarly analysis subsection  
See also  
Notes  
Citations  
Bibliography  
Toggle Bibliography subsection  
Further reading  
Toggle Further reading subsection  
External links  
Founding Fathers of the United States  
67 languages  
Article  
Talk  
Read  
View source  
View history  
Save  
Tools  
Appearance hide  
From Wikipedia, the free encyclopedia  
"Founding Fathers" redirects here. For the founding fathers of other countries, see List of national founders.  
Founding Fathers of the United States  
1760s–1820s
The Committee of Five (Adams, Sherman, Livingston, Jefferson, and Franklin) present their draft of the Declaration of Independence to the Second Continental Congress in Philadelphia on June 28, 1776, as depicted in John Trumbull's 1818 portrait.
Location	Thirteen Colonies  
Including	Signers of the Declaration of Independence (1776), Articles of Confederation (1781), and United States Constitution (1789)  
Leaders	  
John Adams  
Samuel Adams  
Benjamin Franklin  
Alexander Hamilton  
John Hancock  
Patrick Henry  
John Jay  
Thomas Jefferson  
Richard Henry Lee  
Robert R. Livingston  
James Madison  
George Mason  
Robert Morris  
Peyton Randolph  
Roger Sherman  
Joseph Warren  
George Washington  
James Wilson
</excerpt>
### Rank 5 of 124 — 0.76
<excerpt title="Founding Fathers of the United States">
Historical founders  
Thomas Jefferson, a key Founding Father, was the primary author of the Declaration of Independence, which Pulitzer Prize-winning historian Joseph Ellis says contains "the most potent and consequential words in U.S. history".[6]
The historian Richard B. Morris's selection of seven key founders was widely accepted through the 20th century.[7][8] John Adams, Thomas Jefferson, and Benjamin Franklin were members of the Committee of Five that were charged by the Second Continental Congress with drafting the Declaration of Independence. Franklin, Adams, and John Jay negotiated the 1783 Treaty of Paris, which established American independence and brought an end to the American Revolutionary War.[9] The constitutions drafted by Jay and Adams for their respective states of New York (1777) and Massachusetts (1780) proved influential in the language used in developing the U.S. Constitution.[10][11][12] The Federalist Papers, which advocated the ratification of the Constitution, were written by Alexander Hamilton, James Madison, and Jay. George Washington was commander-in-chief of the Continental Army and later president of the Constitutional Convention.[13][14]
Each of these men held additional important roles in the early government of the United States. Washington, Adams, Jefferson, and Madison served as the first four presidents; Adams and Jefferson were the nation's first two vice presidents;[15] Jay was the nation's first chief justice;[16] Hamilton was the first secretary of the treasury;[17] Jefferson was the first secretary of state;[18][19] and Franklin was America's most senior diplomat from the start of the Revolutionary War through its conclusion with the signing of the Treaty of Paris in 1783.[20]
The list of Founding Fathers is often expanded to include the signers of the Declaration of Independence and individuals who later approved the U.S. Constitution.[2] Some scholars regard all delegates to the Constitutional Convention as Founding Fathers whether they approved the Constitution or not.[21][22] In addition, some historians include signers of the Articles of Confederation, which was adopted in 1781 as the nation's first constitution.[23]
</excerpt>

## Search 7 — query: "2020-2025 County Population Totals and Components of Change Florida 2022"
### Rank 1 of 261 — 0.72 (passed on)
<excerpt title="Florida Estimates of Population 2025">
## [PDF page 25]
Broward  1,993,535  1,944,375  1,748,066  1,623,018  2.5  11.2  7.7  
Calhoun  13,655  13,648  14,625  13,017  0.1  -6.7  12.4  
Charlotte  223,430  186,847  159,978  141,627  19.6  16.8  13.0  
Citrus  166,500  153,843  141,236  118,085  8.2  8.9  19.6  
Clay  238,605  218,245  190,865  140,814  9.3  14.3  35.5

## [PDF page 25]
Collier  413,314  375,752  321,520  251,377  10.0  16.9  27.9  
Columbia  72,388  69,698  67,531  56,513  3.9  3.2  19.5  
DeSoto  35,947  33,976  34,862  32,209  5.8  -2.5  8.2  
Dixie  17,217  16,759  16,422  13,827  2.7  2.1  18.8  
Duval  1,079,044  995,567  864,263  778,879  8.4  15.2  11.0

## [PDF page 25]
Escambia  337,728  321,905  297,619  294,410  4.9  8.2  1.1  
Flagler  140,714  115,378  95,696  49,832  22.0  20.6  92.0  
Franklin  13,383  12,451  11,549  9,829  7.5  7.8  17.5  
Gadsden  44,790  43,826  46,389  45,087  2.2  -5.5  2.9  
Gilchrist  19,716  17,864  16,939  14,437  10.4  5.5  17.3
</excerpt>
### Rank 2 of 261 — 0.71
<excerpt title="Florida Estimates of Population 2025">
## [PDF page 49]
11  St. Lucie  23.5  86,577  45  Lafayette  10.9  8 84  
12  Alachua  22.6  66,264  46  Dixie  10.8  1,857  
13  Union  20.7  3,336  47  Levy  10.8  4,888  
14  Hillsborough  20.6  317,427  48  Manatee  10.6  46,471  
15  Palm Beach  20.6  315,173  49  Indian River  10.5  17,601
16  T a y lo r  20.2  4,391  50  Lee  10.2  81,963  
17  Columbia  19.4  13,999  51  Okeecho bee  9.3  3,671  
18  Bradford  18.8  5,159  52  Hardee  9.1  2,326  
19  Polk  17.6  140,485  53  P as co  8.4  51,144  
20  Putnam  17.5  13,314  54  Collier  8.0  31,927

## [PDF page 49]
21  Liberty  17.4  1,388  55  St. Johns  7.9  24,922  
22  Miami-Dade  17.1  473,426  56  Hernando  7.8  15,952  
23  Se m i no le  15.5  75,565  57  Santa Rosa  7.8  15,882  
24  Osceola  15.2  66,979  58  Monroe  7.7  6,480  
25  Gulf  15.0  2,451  59  Nassau  7.6  7,683
26  Clay  14.9  34,389  60  Sumter  7.6  11,873  
27  Washington  14.7  3,751  61  Ho lmes  7.2  1,426  
28  Marion  14.6  59,077  62  Charlotte  7.1  14,464  
29  DeSoto  14.4  5,023  63  Martin  6.7  10,959  
30  Wakulla  14.1  5,116  64  Walton  6.6  5,535
</excerpt>
### Rank 3 of 261 — 0.71
<excerpt title="Florida Estimates of Population 2025">
## [PDF page 45]
6  Hillsborough  22.7  349,560  40  Jackson  18.8  9,231  
7  Orange  22.3  332,306  41  Palm Beach  18.8  288,355  
8  Duval  22.1  232,588  42  Hamilton  18.7  2,562  
9  Okaloosa  21.9  48,027  43  L eo n  18.6  56,151  
10  Polk  21.9  174,462  44  Manatee  18.3  80,471
11  Santa Rosa  21.7  44,050  45  Brevard  17.9  114,953  
12  Okeecho bee  21.7  8,575  46  Union  17.9  2,888  
13  Bay  21.3  40,010  47  Marion  17.9  72,213  
14  Se m i no le  21.3  103,668  48  Franklin  17.9  2,318  
15  Gadsden  21.1  9,394  49  Hernando  17.8  36,344

## [PDF page 45]
16  Wakulla  21.1  7,627  50  Lee  17.8  142,462  
17  Putnam  21.1  15,991  51  Alachua  17.7  51,885  
18  Escambia  21.1  70,223  52  Volusia  17.6  102,838  
19  Madison  20.9  3,900  53  Dixie  17.6  3,038  
20  St. Johns  20.8  65,450  54  Flagler  17.6  22,999
21  Lafayette  20.6  1,667  55  Collier  16.9  67,486  
22  Columbia  20.5  14,833  56  Jefferson  16.8  2,587  
23  Suwannee  20.5  9,337  57  Highlands  16.7  17,451  
24  St. Lucie  20.4  75,169  58  Indian River  16.5  27,758  
25  Bradford  20.3  5,570  59  Pinellas  16.4  159,999
</excerpt>
### Rank 4 of 261 — 0.70
<excerpt title="Florida Estimates of Population 2025">
## [PDF page 30]
Hamilton  14,155  14,004  14,799  13,327  1.1  -5.4  11.0  
Lafayette  8,601  8,226  8,870  7,022  4.6  -7.3  26.3  
Levy  46,270  42,915  40,801  34,450  7.8  5.2  18.4  
Madison  18,859  17,968  19,224  18,733  5.0  -6.5  2.6  
Suwannee  47,274  43,474  41,551  34,844  8.7  4.6  19.2  
T a y lo r  22,011  21,796  22,570  19,256  1.0  -3.4  17.2  
Union  16,821  16,147  15,535  13,442  4.2  3.9  15.6  
Northeast Florida  2,019,491  1,794,547  1,515,656  1,243,005  12.5  18.4  21.9

## [PDF page 30]
Baker  29,139  28,259  27,115  22,259  3.1  4.2  21.8  
Clay  238,605  218,245  190,865  140,814  9.3  14.3  35.5  
Duval  1,079,044  995,567  864,263  778,879  8.4  15.2  11.0  
Flagler  140,714  115,378  95,696  49,832  22.0  20.6  92.0  
Nassau  107,053  90,352  73,314  57,663  18.5  23.2  27.1  
Putnam  76,600  73,321  74,364  70,423  4.5  -1.4  5.6  
St. Johns  348,336  273,425  190,039  123,135  27.4  43.9  54.3
</excerpt>
### Rank 5 of 261 — 0.69
<excerpt title="Florida Estimates of Population 2025">
## [PDF page 17]
Islamorada, Village of Islands  7,379  2 72  7,107  0  7,379  
Key Colony Beach  7 96  6  7 90  0  7 96  
Key West  26,526  82  26,444  2  26,524  
Layton  2 21  11  2 10  0  2 21  
Marathon  10,163  4 74  9,689  0  10,163  
UNINCORPORATED  39,622  9 88  38,634  0  39,622  
Nassau County  107,053  16,701  90,352  67  106,986
Callahan  1,752  2 26  1,526  0  1,752  
Fernandina Beach  13,958  9 06  13,052  0  13,958  
Hilliard  3,127  1 60  2,967  0  3,127  
UNINCORPORATED  88,216  15,409  72,807  67  88,149  
Okaloosa County  226,193  14,525  211,668  1,415  224,778

## [PDF page 17]
Cinco Bayou  4 47  -10  4 57  0  4 47  
Crestview  31,702  4,568  27,134  0  31,702  
Destin  14,640  7 09  13,931  0  14,640  
Fort Walton  Beach  21,553  6 31  20,922  0  21,553  
Laurel Hill  7 46  1 62  5 84  0  7 46  
Mary Esther  4,457  4 75  3,982  0  4,457  
Niceville  17,119  1,347  15,772  0  17,119  
Shalimar  7 33  -4  7 37  0  7 33  
Valparaiso  5,105  3 53  4,752  0  5,105  
UNINCORPORATED  129,691  6,294  123,397  1,415  128,276  
Okeechobee County  40,314  6 70  39,644  1,850  38,464
</excerpt>

## Search 8 — query: "Holmes County Florida population 2022"
### Rank 1 of 72 — 0.91 (passed on)
<excerpt title="Holmes County">
## [PDF page 1]
Population Estimates  Housing  
Holmes County  Florida  Housing Counts  Holmes County  Florida  
2021 Estimate  19,665  21,898,945  Housing units, 2020 Census  8,622  9,865,350  
% change 2020-2021  0.1%  1.7%  Occupied  7,282  8,529,067  
2022 Estimate  19,784  22,276,132  Vacant  1,340  1,336,283  
% change 2020-2022  0.7%  3.4%  
2023 Estimate  19,910  22,634,867  Building Permits  
% change 2020-2023  1.3%  5.1%  Units Permitted  Holmes County  Florida  
2024 Estimate  20,059  23,014,551  2000  41  155,269  
% change 2020-2024  2.1%  6.9%  2010  16  38,679  
2025 Estimate  20,042  23,379,261  2020  11  164,074  
% change 2020-2025  2.0%  8.5%  2021  13  213,494  
Based on 2025 Estimate  2022  11  211,962  
2030  20,268  24,909,028  2023  12  193,788
</excerpt>
### Rank 2 of 72 — 0.90
<excerpt title="Holmes County">
## [PDF page 1]
% Male  53.4%  48.6%  Percent of the State  0.0%  
% Female  46.6%  51.4%  2023 GDP  426,288  1,309,392,241  
Race (alone) & Ethnicity  Percent of the State  0.0%  
% Not Hispanic-White  85.3%  51.5%  2024 GDP  437,047  1,352,275,106  
% Not Hispanic-Black or African American  6.2%  14.5%  Percent of the State  0.0%  
% Not Hispanic-American Indian and Alaska Native  0.6%  0.2%  
% Not Hispanic-Asian  0.4%  2.9%  
% Not Hispanic-Native Hawaiian and Other Pacific  Population by Housing Type  
Islander  0.1%  0.1%  
% Not Hispanic-Some Other Race  0.1%  0.6%  Holmes County  Florida  
% Not Hispanic-Two or More Races  3.8%  3.7%  Household Population  17,741  21,073,604  
% Hispanic or Latino (of any race)  3.5%  26.5%  Household Population per Occupied Housing Unit  2.44  2.47  
Group Quarters Population  1,912  464,583

## [PDF page 1]
Population Estimates  Housing  
Holmes County  Florida  Housing Counts  Holmes County  Florida  
2021 Estimate  19,665  21,898,945  Housing units, 2020 Census  8,622  9,865,350  
% change 2020-2021  0.1%  1.7%  Occupied  7,282  8,529,067  
2022 Estimate  19,784  22,276,132  Vacant  1,340  1,336,283  
% change 2020-2022  0.7%  3.4%  
2023 Estimate  19,910  22,634,867  Building Permits  
% change 2020-2023  1.3%  5.1%  Units Permitted  Holmes County  Florida  
2024 Estimate  20,059  23,014,551  2000  41  155,269  
% change 2020-2024  2.1%  6.9%  2010  16  38,679  
2025 Estimate  20,042  23,379,261  2020  11  164,074  
% change 2020-2025  2.0%  8.5%  2021  13  213,494  
Based on 2025 Estimate  2022  11  211,962  
2030  20,268  24,909,028  2023  12  193,788
</excerpt>
### Rank 3 of 72 — 0.90
<excerpt title="Holmes County, Florida Population 2026">
# Holmes County
## Holmes County Population
1850–2026
20,114
2026 projection
▲2.7% since 2020 (increase)
Source:U.S. Census Bureau decennial counts and annual estimates. 2026 is a projection. Values between recorded years are interpolated.
Use the left and right arrow keys to inspect population observations.
1850–2026
20,114
2026 projection
▲2.7% since 2020 (increase)
Source:U.S. Census Bureau decennial counts and annual estimates. 2026 is a projection. Values between recorded years are interpolated.
Use the left and right arrow keys to inspect population observations.

# Holmes County
## Holmes County Population
### Population by year
Population estimates for Holmes County. Annual change is shown as a percentage. Growth is the total change since the preceding observation.| Year | Population | Growth | Annual change |  
| --- | --- | --- | --- |  
| 2026 | 20,114 | -5 | 0.02% |  
| 2025 | 20,119 | -5 | 0.02% |  
| 2024 | 20,124 | +183 | 0.92% |  
| 2023 | 19,941 | +309 | 1.57% |  
| 2022 | 19,632 | +333 | 1.73% |  
| 2021 | 19,299 | -292 | 1.49% |  
| 2020 | 19,591 | -70 | 0.36% |  
| 2019 | 19,661 | +149 | 0.76% |  
| 2018 | 19,512 | +54 | 0.28% |  
| 2017 | 19,458 | +32 | 0.16% |
Show earlier years
Showing 10 of 32 years.

# Holmes County
## Holmes County Demographics
**43.7**median age
* * *

# Holmes County
## Holmes County Demographics
#### Median age
Female**45.7** yrs
Male**41.8** yrs
* * *

# Holmes County
## Holmes County Demographics
#### Adults
**15,522**
**4,139** seniors (65+) · 27% of adults 11,383 other adults

# Holmes County
## Holmes County Demographics
#### Sex
**Female 47.3%** · 9,235**Male 52.7%** · 10,278
U.S. Census Bureau, 2024 ACS 5-year estimates · TableS0101

# Holmes County
## Holmes County Demographics
### Race and ethnicity
Tap a square or a group below to highlight it.
Each square is about 1% of residents (roughly 195 people).
*   White 16,427 84.2%  
*   Black 1,124 5.8%  
*   Two or more races 947 4.9%  
*   Hispanic 716 3.7%  
*   Other, incl. Native American 178 0.9%  
*   Asian 121 0.6%
Hispanic or Latino residents can be of any race. All other groups exclude Hispanic residents.
U.S. Census Bureau, 2024 ACS 5-year estimates · TableB03002

# Holmes County
## Holmes County Income
**$49,343**median household income

# Holmes County
## Holmes County Income
#### Median household income
**$49,343**
Half of households earn more, half earn less
</excerpt>
### Rank 4 of 72 — 0.89
<excerpt title="Resident Population in Holmes County, FL (FLHOLM9POP) - FRED">
# Resident Population in Holmes County, FL (FLHOLM9POP) | FRED | St. Louis Fed
Skip to main content
* * *
*

# Resident Population in Holmes County, FL (FLHOLM9POP) | FRED | St. Louis Fed
## Explore Our Apps
* * *
*    ### FRED Tools and resources to find and use economic data worldwide  
    *    ### FRASER U.S. financial, economic, and banking history  
    *    ### ALFRED Vintages of economic data from specific dates in history  
    *    ### CASSIDI View banking market concentrations and perform HHI analysis
*
*   Release Calendar  
*   Tools   
    *   FRED MCP Connector  
    *   FRED Add-in for Excel  
    *   FRED API  
    *   FRED Mobile Apps

*   News  
*   Blog  
*   About   
    *   What is FRED  
    *   Tutorial  
    *   Digital Badges  
    *   Contact Us

*   My Account  
*    Explore Our Apps
* * *
*    ### FRED Tools and resources to find and use economic data worldwide  
    *    ### FRASER U.S. financial, economic, and banking history  
    *    ### ALFRED Vintages of economic data from specific dates in history  
    *    ### CASSIDI View banking market concentrations and perform HHI analysis
*   STL Fed Home Page
* * *
*   Release Calendar  
*   Tools 

    *   FRED MCP Connector  
    *   FRED Add-in for Excel  
    *   FRED API  
    *   FRED Mobile Apps

*   News  
*   Blog  
*   About 

    *   What is FRED  
    *   Tutorial  
    *   Digital Badges  
    *   Contact Us
Home>Categories>U.S. Regional Data>States>Florida>Counties>Holmes County, FL

#
Resident Population in Holmes County, FL (FLHOLM9POP)
Observations
2025: 20.119 | Thousands of Persons, Not Seasonally Adjusted |  Annual
Updated: Mar 27, 2026 2:58 PM CDT
Next Release Date: Not Available
Observations
2025:20.119
Updated: Mar 27, 2026 2:58 PM CDT
Next Release Date: Not Available
2025:20.119  
2024:20.124  
2023:19.941  
2022:19.632  
2021:19.299  
View All
Units:
Thousands of Persons,
Not Seasonally Adjusted
Frequency:
Annual
1Y 5Y 10Y Max
From to
Date:
Edit GraphEdit Map
Download
View Map
EDIT LineADD LineFORMAT
Line 1
(a)Resident Population in Holmes County, FL,Thousands of Persons,Not Seasonally Adjusted(FLHOLM9POP)
Units
Select a date that will equal 100 for your custom index:
U.S. recession: or **Enter date as YYYY-MM-DD**
- [x] Display integer periods instead of dates (e.g. ...,-1,0,1,...) with the value scaled to 100 at period 0.
Integer start/end to Copy to all
Modify frequency
Aggregation method:
Customize data
Write a custom formula to transform one or more series or combine two or more series.
You can begin by adding a series to combine with your existing series.
Type keywords to search for data
Add
Now create a custom formula to combine or transform the series.
Need help?
For example, invert an exchange rate by using formula 1/a, where “a” refers to the first FRED data series added to this line. Or calculate the spread between 2 interest rates, a and b, by using the formula a - b.
</excerpt>
### Rank 5 of 72 — 0.89
<excerpt title="Resident Population in Holmes County, FL (FLHOLM9POP) - FRED">
#
Resident Population in Holmes County, FL (FLHOLM9POP)
Observations
2025: 20.119 | Thousands of Persons, Not Seasonally Adjusted |  Annual
Updated: Mar 27, 2026 2:58 PM CDT
Next Release Date: Not Available
Observations
2025:20.119
Updated: Mar 27, 2026 2:58 PM CDT
Next Release Date: Not Available
2025:20.119  
2024:20.124  
2023:19.941  
2022:19.632  
2021:19.299  
View All
Units:
Thousands of Persons,
Not Seasonally Adjusted
Frequency:
Annual
1Y 5Y 10Y Max
From to
Date:
Edit GraphEdit Map
Download
View Map
EDIT LineADD LineFORMAT
Line 1
(a)Resident Population in Holmes County, FL,Thousands of Persons,Not Seasonally Adjusted(FLHOLM9POP)
Units
Select a date that will equal 100 for your custom index:
U.S. recession: or **Enter date as YYYY-MM-DD**
- [x] Display integer periods instead of dates (e.g. ...,-1,0,1,...) with the value scaled to 100 at period 0.
Integer start/end to Copy to all
Modify frequency
Aggregation method:
Customize data
Write a custom formula to transform one or more series or combine two or more series.
You can begin by adding a series to combine with your existing series.
Type keywords to search for data
Add
Now create a custom formula to combine or transform the series.
Need help?
For example, invert an exchange rate by using formula 1/a, where “a” refers to the first FRED data series added to this line. Or calculate the spread between 2 interest rates, a and b, by using the formula a - b.

#
Use the assigned data series variables (a, b, c, etc.) together with operators (+, -, *, /, ^, etc.), parentheses and constants (1, 1.5, 2, etc.) to create your own formula (e.g., 1/a, a-b, (a+b)/2, (a/(a+b+c))*100). As noted above, you may add other data series to this line before entering a formula.
Formula
Apply Formula
Finally, you can change the units of your new series.
Units
Select a date that will equal 100 for your custom index:
U.S. recession: or **Enter date as YYYY-MM-DD**

#
#### Add the minimum, maximum, and average calculations of selected lines to the graph
Do not include this line in calculations (default)
Include this line in calculations
Include this line in calculations, but do not display it
ADD LINE
Add data series to graph
Type keywords to search for data
Add data series
Create user-defined line
You can customize a graph by adding a straight line between two data points.
Create line
FORMAT GRAPH
Graph type
Stacking:

#
#### Add the minimum, maximum, and average calculations of selected lines to the graph
##### Details
###### Display
- [x] Title 

- [x] Axis titles 

- [x] Tooltip 

- [x] Recession shading 

- [x] Log scale left 

- [x] Log scale right

#
#### Add the minimum, maximum, and average calculations of selected lines to the graph
##### Details
###### Customize
Frame
Plot area
Text
Height
Width
Apply

#
#### Add the minimum, maximum, and average calculations of selected lines to the graph
##### Line 1
###### Resident Population in Holmes County, FL
</excerpt>

## Search 9 — query: "Florida County 2022 Estimate PDF 2025 "2022 Estimate" "County" "2025" pdf"
### Rank 1 of 79 — 0.65 (passed on)
<excerpt title="Jefferson County">
## [PDF page 1]
% Male  51.6%  48.6%  Percent of the State  0.0%  
% Female  48.4%  51.4%  2023 GDP  308,359  1,309,392,241  
Race (alone) & Ethnicity  Percent of the State  0.0%  
% Not Hispanic-White  60.1%  51.5%  2024 GDP  340,534  1,352,275,106  
% Not Hispanic-Black or African American  31.7%  14.5%  Percent of the State  0.0%  
% Not Hispanic-American Indian and Alaska Native  0.2%  0.2%  
% Not Hispanic-Asian  0.2%  2.9%  
% Not Hispanic-Native Hawaiian and Other Pacific  Population by Housing Type  
Islander  0.0%  0.1%  
% Not Hispanic-Some Other Race  0.4%  0.6%  Jefferson County  Florida  
% Not Hispanic-Two or More Races  2.8%  3.7%  Household Population  13,497  21,073,604  
% Hispanic or Latino (of any race)  4.5%  26.5%  Household Population per Occupied Housing Unit  2.32  2.47  
Group Quarters Population  1,013  464,583

## [PDF page 1]
Population Estimates  Housing  
Jefferson County  Florida  Housing Counts  Jefferson County  Florida  
2021 Estimate  14,590  21,898,945  Housing units, 2020 Census  6,690  9,865,350  
% change 2020-2021  0.6%  1.7%  Occupied  5,816  8,529,067  
2022 Estimate  14,923  22,276,132  Vacant  874  1,336,283  
% change 2020-2022  2.8%  3.4%  
2023 Estimate  15,402  22,634,867  Building Permits  
% change 2020-2023  6.1%  5.1%  Units Permitted  Jefferson County  Florida  
2024 Estimate  15,667  23,014,551  2000  70  155,269  
% change 2020-2024  8.0%  6.9%  2010  21  38,679  
2025 Estimate  15,761  23,379,261  2020  70  164,074  
% change 2020-2025  8.6%  8.5%  2021  112  213,494  
Based on 2025 Estimate  2022  88  211,962  
2030  16,238  24,909,028  2023  69  193,788
</excerpt>
### Rank 2 of 79 — 0.63
<excerpt title="Madison County Florida Profile">
## [PDF page 1]
% Not Hispanic-Black or African American  35.0%  14.5%  Percent of the State  0.0%  
% Not Hispanic-American Indian and Alaska Native  0.3%  0.2%  2021 GDP  396,448  1,029,575,591  
% Not Hispanic-Asian  0.3%  2.9%  Percent of the State  0.0%  
% Not Hispanic-Native Hawaiian and Other Pacific  
Islander  0.0%  0.1%  
% Not Hispanic-Some Other Race  0.4%  0.6%  Population by Housing Type  
% Not Hispanic-Two or More Races  2.9%  3.7%  Madison County  Florida  
% Hispanic or Latino (of any race)  4.9%  26.5%  Household Population  16,253  21,073,604  
Household Population per Occupied Housing Unit  2.36  2.47  
Group Quarters Population  1,715  464,583

## [PDF page 1]
Population Estimates  Housing  
Madison County  Florida  Housing Counts  Madison County  Florida  
2021 Estimate  18,122  21,898,945  Housing units, 2020 Census  8,315  9,865,350  
% change 2020-2021  0.9%  1.7%  Occupied  6,877  8,529,067  
2022 Estimate  18,438  22,276,132  Vacant  1,438  1,336,283  
% change 2020-2022  2.6%  3.4%  
Based on 2021 Estimate  Building Permits  
2025  18,262  23,164,008  Units Permitted  Madison County  Florida  
2030  18,420  24,471,129  2000  45  155,269  
2035  18,496  25,520,837  2010  27  38,679  
2040  18,551  26,405,472  2020  43  164,074  
2045  18,593  27,176,715  2021  52  213,494  
2050  18,628  27,877,707

## [PDF page 1]
Population Characteristics  Density  
Madison County  Florida  Persons per square mile  Madison County  Florida  
Language spoken at home other than English  2000  27.1  296.4  
Persons aged 5 and over  7.4%  29.8%  2010  27.6  350.6  
Place of birth  2020  25.8  401.4  
Foreign born  4.6%  21.0%  2022  26.0  408.2  
Veteran status  
Civilian population 18 and over  7.5%  8.2%
</excerpt>
### Rank 3 of 79 — 0.56
<excerpt title="Jefferson County">
## [PDF page 1]
Population Estimates  Housing  
Jefferson County  Florida  Housing Counts  Jefferson County  Florida  
2021 Estimate  14,590  21,898,945  Housing units, 2020 Census  6,690  9,865,350  
% change 2020-2021  0.6%  1.7%  Occupied  5,816  8,529,067  
2022 Estimate  14,923  22,276,132  Vacant  874  1,336,283  
% change 2020-2022  2.8%  3.4%  
2023 Estimate  15,402  22,634,867  Building Permits  
% change 2020-2023  6.1%  5.1%  Units Permitted  Jefferson County  Florida  
2024 Estimate  15,667  23,014,551  2000  70  155,269  
% change 2020-2024  8.0%  6.9%  2010  21  38,679  
2025 Estimate  15,761  23,379,261  2020  70  164,074  
% change 2020-2025  8.6%  8.5%  2021  112  213,494  
Based on 2025 Estimate  2022  88  211,962  
2030  16,238  24,909,028  2023  69  193,788
</excerpt>
### Rank 4 of 79 — 0.54
<excerpt title="Jefferson County">
Title: PDF document  
URL Source: https://edr.state.fl.us/content/area-profiles/county/jefferson.pdf  
Markdown Content:

## [PDF page 1]
Jefferson County
Florida's 61st most populous county  
with 0.1% of Florida's population

## [PDF page 1]
Population  Real Gross Domestic Product  
Real GDP  
Census Population  Jefferson County  Florida  (Thousands of Chained 2017 Dollars)  Jefferson County  Florida  
1980 Census  10,703  9,746,961  2017 GDP  250,290  1,014,866,863  
1990 Census  11,296  12,938,071  Percent of the State  0.0%  
2000 Census  12,902  15,982,824  2018 GDP  241,506  1,050,433,812  
2010 Census  14,761  18,801,332  Percent of the State  0.0%  
2020 Census  14,510  21,538,187  2019 GDP  251,869  1,084,913,903  
% change 2010-2020  -1.7%  14.6%  Percent of the State  0.0%  
Age  2020 GDP  250,405  1,072,481,562  
% Under 18 years of age  16.9%  19.5%  Percent of the State  0.0%  
% Aged 65 and over  24.7%  21.2%  2021 GDP  268,747  1,172,655,328  
% Median age  49.8  43.0  Percent of the State  0.0%  
Gender  2022 GDP  274,490  1,245,927,559
</excerpt>
### Rank 5 of 79 — 0.44
<excerpt title="Miami-Dade County">
## [PDF page 1]
Based on 2025 Estimate  2022  11,605  211,962  
2030  2,916,375  24,909,028  2023  12,781  193,788  
2035  2,994,448  26,074,611  2024  10,608  173,326  
2040  3,054,197  26,967,897  2025  16,535  178,297  
2045  3,100,926  27,664,885  
2050  3,140,714  28,250,130  
Population DensityMiami-Dade  
Persons per square mile  County  Florida  
Population CharacteristicsMiami-Dade  2000  1,158.1  296.4  
Language Spoken at home  County  Florida  2010  1,315.5  350.6  
(% of total persons aged 5 and over)  2020  1,422.1  401.4  
Speak only English  24.7%  69.4%  2025  1,481.6  435.8  
Speak a language other than English  75.3%  30.6%  
Speak English "very well"  40.2%  18.1%  
Place of birth  Households and Family Households  
Miami-Dade  
Foreign born  54.5%  21.9%  Households  County  Florida  
Veteran status  Total households, 2000 Census  776,906  6,338,075  

## [PDF page 1]
Civilian population 18 and over  2.0%  7.4%  Family households, 2000 Census  548,493  4,210,760  
% with own children under 18  47.9%  42.3%  
Migration  Total households, 2010 Census  867,352  7,420,802  
Residence 1 Year Ago  Miami-Dade  
Persons aged 1 and over  County  Florida  Family households, 2010 Census  602,911  4,835,475  
Same house  88.0%  86.3%  % with own children under 18  44.0%  40.0%  
Different house in the U.S.  9.9%  12.6%  Average Household Size, 2010 Census  2.83  2.48  
Same county in Florida  7.7%  6.6%  Average Family Size, 2010 Census  3.33  3.01  
Different county in Florida  1.0%  3.1%  Total households, 2020 Census  967,414  8,529,067  
Different county in another state  1.3%  2.9%  Family households, 2020 Census  669,137  5,571,482  
Abroad  2.1%  1.1%  % with own children under 18  39.1%  36.0%
</excerpt>

## Search 10 — query: "Florida counties population 2022 50000"
### Rank 1 of 69 — 0.81 (passed on)
<excerpt title="How many people live in Florida?">
## What are Florida's most populous counties?
| 12073 | Leon County | 300488 |  
| 12001 | Alachua County | 291782 |  
| 12019 | Clay County | 236760 |  
| 12091 | Okaloosa County | 220483 |  
| 12053 | Hernando County | 218150 |  
| 12015 | Charlotte County | 212122 |  
| 12113 | Santa Rosa County | 207653 |  
| 12005 | Bay County | 199718 |  
| 12061 | Indian River County | 172139 |  
| 12017 | Citrus County | 170174 |  
| 12085 | Martin County | 165666 |  
| 12119 | Sumter County | 154693 |  
| 12035 | Flagler County | 136744 |  
| 12055 | Highlands County | 109778 |  
| 12089 | Nassau County | 104376 |  
| 12131 | Walton County | 89666 |  
| 12087 | Monroe County | 80908 |  
| 12107 | Putnam County | 77301 |  
| 12023 | Columbia County | 73977 |  
| 12063 | Jackson County | 49980 |  
| 12075 | Levy County | 47765 |  
| 12121 | Suwannee County | 47536 |  
| 12051 | Hendry County | 46130 |  
| 12039 | Gadsden County | 44151 |  

## What are Florida's most populous counties?
| 12093 | Okeechobee County | 42369 |  
| 12129 | Wakulla County | 37115 |  
| 12027 | DeSoto County | 36744 |  
| 12003 | Baker County | 29325 |  
| 12007 | Bradford County | 28075 |  
| 12133 | Washington County | 26503 |  
| 12049 | Hardee County | 26068 |  
| 12123 | Taylor County | 21843 |  
| 12041 | Gilchrist County | 20233 |  
| 12059 | Holmes County | 19876 |  
| 12079 | Madison County | 18364 |  
| 12029 | Dixie County | 17614 |  
| 12065 | Jefferson County | 15921 |  
| 12045 | Gulf County | 15876 |  
| 12125 | Union County | 15738 |  
| 12047 | Hamilton County | 14334 |  
| 12013 | Calhoun County | 13278 |  
| 12043 | Glades County | 13132 |  
| 12037 | Franklin County | 12979 |  
| 12067 | Lafayette County | 8640 |  
| 12077 | Liberty County | 7955 |
</excerpt>
### Rank 2 of 69 — 0.79
<excerpt title="Population Table for Florida Counties | HDPulse Data Portal - NIH">
# Social & Economic Environment
## Data Visualization
| Charlotte County | 9.8 | 19,620 | 407 |  
| Indian River County | 10.0 | 16,738 | 385 |  
| Lake County | 10.7 | 44,239 | 344 |  
| Highlands County | 10.8 | 11,458 | 338 |  
| Glades County | 11.0 | 1,378 | 323 |  
| Martin County | 11.1 | 18,029 | 320 |  
| Alachua County | 11.6 | 32,992 | 301 |  
| Hardee County | 11.7 | 3,011 | 296 |  
| Duval County | 12.2 | 124,891 | 275 |  
| Pasco County | 12.3 | 75,194 | 270 |  
| Pinellas County | 12.4 | 119,232 | 266 |  
| Polk County | 12.6 | 99,373 | 263 |  
| Flagler County | 12.8 | 16,192 | 256 |  
| Sarasota County | 13.0 | 59,568 | 244 |  
| Okeechobee County | 13.4 | 5,455 | 235 |  
| DeSoto County | 13.6 | 4,819 | 228 |  
| Manatee County | 14.5 | 62,221 | 195 |  
| Seminole County | 15.1 | 72,673 | 187 |  
| St. Lucie County | 18.2 | 65,657 | 139 |  
| Lee County | 18.9 | 154,309 | 128 |
</excerpt>
### Rank 3 of 69 — 0.79
<excerpt title="How many people live in Florida?">
## What are Florida's most populous counties?
| 12093 | Okeechobee County | 42369 |  
| 12129 | Wakulla County | 37115 |  
| 12027 | DeSoto County | 36744 |  
| 12003 | Baker County | 29325 |  
| 12007 | Bradford County | 28075 |  
| 12133 | Washington County | 26503 |  
| 12049 | Hardee County | 26068 |  
| 12123 | Taylor County | 21843 |  
| 12041 | Gilchrist County | 20233 |  
| 12059 | Holmes County | 19876 |  
| 12079 | Madison County | 18364 |  
| 12029 | Dixie County | 17614 |  
| 12065 | Jefferson County | 15921 |  
| 12045 | Gulf County | 15876 |  
| 12125 | Union County | 15738 |  
| 12047 | Hamilton County | 14334 |  
| 12013 | Calhoun County | 13278 |  
| 12043 | Glades County | 13132 |  
| 12037 | Franklin County | 12979 |  
| 12067 | Lafayette County | 8640 |  
| 12077 | Liberty County | 7955 |

## What are Florida's most populous cities?
The largest city in Florida is Jacksonville with about 1.01 million residents in 2024.

## Cities and counties in Florida ranked by population
Cities and counties in Florida ranked by population 1.Jacksonville 1,009,833  
2.Miami 487,014  
3.Tampa 414,547  
4.Orlando 334,854  
5.St.Petersburg 267,102  
6.Port St.Lucie 258,575  
7.Hialeah 235,388  
8.Cape Coral 233,025  
9.Tallahassee 205,089  
10.Fort Lauderdale 190,641

## Keep exploring
*    ### Semiquincentennial snapshot: the US at 250 years Jul 1, 2026  
*    ### Which states have the largest elderly populations? Dec 11, 2025  
*    ### What is the poverty rate in Florida? Updates monthly  
*   ### How many people in Florida speak a language other than English at home? Updates annually

## Methodology
USAFacts standardizes data, in areas such as time and demographics, to make it easier to understand and compare.
</excerpt>
### Rank 4 of 69 — 0.77
<excerpt title="Florida Counties by Population (2026)">
# Florida Counties by Population (2026)
| Santa Rosa County | 214,759 | 1K | 212 | 13.61% |  
| Bay County | 208,816 | 759 | 275 | 19.63% |  
| Indian River County | 174,038 | 503 | 346 | 8.47% |  
| Citrus County | 173,511 | 582 | 298 | 12.26% |  
| Martin County | 167,342 | 544 | 308 | 5.47% |  
| Sumter County | 161,283 | 557 | 290 | 23.78% |  
| Flagler County | 144,436 | 486 | 297 | 24.48% |  
| Highlands County | 112,352 | 1K | 110 | 10.87% |  
| Nassau County | 109,266 | 649 | 168 | 20.02% |  
| Walton County | 96,480 | 1K | 93 | 27.12% |  
| Monroe County | 78,797 | 983 | 80 | -4.89% |  
| Putnam County | 78,295 | 728 | 108 | 6.69% |  
| Columbia County | 74,467 | 797 | 93 | 6.75% |  
| Hendry County | 49,911 | 1.2K | 43 | 25.64% |  
| Levy County | 49,396 | 1.1K | 44 | 14.7% |  
| Jackson County | 49,321 | 918 | 54 | 4.71% |
</excerpt>
### Rank 5 of 69 — 0.74
<excerpt title="Population Table for Florida Counties | HDPulse Data Portal - NIH">
# Social & Economic Environment
## Data Visualization
| Hamilton County | 4.5 | 606 | 1,073 |  
| Columbia County | 4.7 | 3,398 | 1,030 |  
| Putnam County | 4.7 | 3,562 | 1,030 |  
| Santa Rosa County | 4.9 | 9,666 | 985 |  
| Taylor County | 5.3 | 1,139 | 917 |  
| Citrus County | 5.6 | 9,049 | 868 |  
| Escambia County | 5.7 | 18,565 | 846 |  
| Gadsden County | 5.7 | 2,509 | 846 |  
| Suwannee County | 6.0 | 2,733 | 798 |  
| Sumter County | 6.1 | 8,779 | 779 |  
| Lafayette County | 6.8 | 558 | 682 |  
| Clay County | 7.0 | 15,912 | 657 |  
| Leon County | 7.4 | 22,129 | 620 |  
| Walton County | 7.4 | 6,149 | 620 |  
| Hernando County | 8.4 | 17,411 | 523 |  
| Bay County | 8.6 | 16,046 | 496 |  
| Volusia County | 8.8 | 51,097 | 477 |  
| Okaloosa County | 9.2 | 19,914 | 453 |  
| Marion County | 9.4 | 37,761 | 436 |  
| St. Johns County | 9.4 | 28,971 | 436 |  
| Brevard County | 9.7 | 61,540 | 417 |
</excerpt>

# Example 3
## Question
Of all the botanists who have papers in the “papers of individual botanists” section of the Sherardian Library (MSS. Sherard 26-448), which ones never held the position of Sherardian Professor of Botany?  Please list their full names in the order that their work appears in the Sherardian Library.

## Expected answer
Robert Morison, Jacob Bobart the Younger, William Sherard, George Claridge Druce

## Grade 0.00

## Search 1 — query: "Sherardian Professor of Botany list of holders"
### Rank 1 of 7 — 0.75 (passed on)
<excerpt title="Sherardian Professor of Botany">
From Wikipedia, the free encyclopedia
The **Sherardian Chair of Botany** is a professorship at the University of Oxford that was established in 1734.[[1]](https://en.wikipedia.org/wiki/Sherardian_Professor_of_Botany#cite_note-Oxford_University_Gazette-1) It was created following an endowment by William Sherard on his death in 1728. In his will, Sherard stipulated that the first holder of the chair was to be Johann Jacob Dillenius.[[2]](https://en.wikipedia.org/wiki/Sherardian_Professor_of_Botany#cite_note-2) The Sherardian Professor is also a fellow of Magdalen College, Oxford

## List of Sherardian Professors of Botany
[edit]
*   Johann Jacob Dillenius (1734 to 1747)  
*   Humphry Sibthorp (1747 to 1783)  
*   John Sibthorp (1784 to 1796)  
*   George Williams (1796 to 1834)[[3]](https://en.wikipedia.org/wiki/Sherardian_Professor_of_Botany#cite_note-3)  
*   Charles Giles Bridle Daubeny (1834 to 1867)[[4]](https://en.wikipedia.org/wiki/Sherardian_Professor_of_Botany#cite_note-4)  
*   Marmaduke Alexander Lawson (1868 to 1882)[[5]](https://en.wikipedia.org/wiki/Sherardian_Professor_of_Botany#cite_note-5)  
*   Isaac Bayley Balfour (1884 to 1888)  
*   Sydney Howard Vines (1888 to 1919)  
*   Frederick Keeble (1920 to 1927)  
*   Arthur Tansley (1927 to 1937)  
*   Theodore Osborn (1937 to 1953)  
*   C. D. Darlington (1953 to 1971)  
*   F. R. Whatley (1971 to 1991)  
*   Hugh G. Dickinson (1991 to 2009)[[1]](https://en.wikipedia.org/wiki/Sherardian_Professor_of_Botany#cite_note-Oxford_University_Gazette-1)  
*   Liam Dolan (2009 to 2021)[[6]](https://en.wikipedia.org/wiki/Sherardian_Professor_of_Botany#cite_note-6)  
*   Lars Østergaard (2022 to present)[[7]](https://en.wikipedia.org/wiki/Sherardian_Professor_of_Botany#cite_note-7)
</excerpt>
### Rank 2 of 7 — 0.73
<excerpt title="Sherardian Professor of Botany">
## List of Sherardian Professors of Botany
[edit]
*   Johann Jacob Dillenius (1734 to 1747)  
*   Humphry Sibthorp (1747 to 1783)  
*   John Sibthorp (1784 to 1796)  
*   George Williams (1796 to 1834)[[3]](https://en.wikipedia.org/wiki/Sherardian_Professor_of_Botany#cite_note-3)  
*   Charles Giles Bridle Daubeny (1834 to 1867)[[4]](https://en.wikipedia.org/wiki/Sherardian_Professor_of_Botany#cite_note-4)  
*   Marmaduke Alexander Lawson (1868 to 1882)[[5]](https://en.wikipedia.org/wiki/Sherardian_Professor_of_Botany#cite_note-5)  
*   Isaac Bayley Balfour (1884 to 1888)  
*   Sydney Howard Vines (1888 to 1919)  
*   Frederick Keeble (1920 to 1927)  
*   Arthur Tansley (1927 to 1937)  
*   Theodore Osborn (1937 to 1953)  
*   C. D. Darlington (1953 to 1971)  
*   F. R. Whatley (1971 to 1991)  
*   Hugh G. Dickinson (1991 to 2009)[[1]](https://en.wikipedia.org/wiki/Sherardian_Professor_of_Botany#cite_note-Oxford_University_Gazette-1)  
*   Liam Dolan (2009 to 2021)[[6]](https://en.wikipedia.org/wiki/Sherardian_Professor_of_Botany#cite_note-6)  
*   Lars Østergaard (2022 to present)[[7]](https://en.wikipedia.org/wiki/Sherardian_Professor_of_Botany#cite_note-7)
</excerpt>
### Rank 3 of 7 — 0.71
<excerpt title="Category:Sherardian Professors of Botany">
Add links
*   Category  
*   Talk

*   Read  
*   Edit  
*   View history
Tools
Actions
*   Read  
*   Edit  
*   View history
General
*   What links here  
*   Related changes  
*   Upload file  
*   Permanent link  
*   Page information  
*   Get shortened URL  
*   Switch to legacy parser  
*   Add interlanguage links
Print/export
*   Download as PDF  
*   Printable version
In other projects
*   Wikimedia Commons  
*   Wikidata item
Appearance
Text
*   Small
Standard
Large
This page always uses small font size
This page always uses small font size
Width
*   Standard
Wide
The content is as wide as possible for your browser window.
Color
*   Automatic
Light
Dark
This page is always in light mode.
Help
From Wikipedia, the free encyclopedia
*   University of Oxford portal
The main article for this category is **Sherardian Professor of Botany**.

## Pages in category "Sherardian Professors of Botany"
The following 13 pages are in this category, out of 13 total. This list may not reflect recent changes.

## Pages in category "Sherardian Professors of Botany"
### B
*   Isaac Bayley Balfour

## Pages in category "Sherardian Professors of Botany"
### D
*   C. D. Darlington  
*   Charles Daubeny  
*   Johann Jacob Dillenius  
*   Liam Dolan

## Pages in category "Sherardian Professors of Botany"
### K
*   Frederick Keeble

## Pages in category "Sherardian Professors of Botany"
### L
*   Marmaduke Alexander Lawson

## Pages in category "Sherardian Professors of Botany"
### O
*   Theodore Osborn

## Pages in category "Sherardian Professors of Botany"
### S
*   Humphry Sibthorp (botanist)  
*   John Sibthorp

## Pages in category "Sherardian Professors of Botany"
### T
*   Arthur Tansley

## Pages in category "Sherardian Professors of Botany"
### V
*   Sydney Howard Vines

## Pages in category "Sherardian Professors of Botany"
### W
*   George Williams (physician)
Retrieved from "https://en.wikipedia.org/w/index.php?title=Category:Sherardian_Professors_of_Botany&oldid=644489450"
Category:
*   Statutory Professors of the University of Oxford
Hidden category:
*   Category main article does not match category title
</excerpt>
### Rank 4 of 7 — 0.67
<excerpt title="Biology welcome new Sherardian Professorship in Botany">
The Department of Biology welcome Professor Lars Østergaard from November 2022 as the new Sherardian Professor of Botany. Lars joins the department from the John Innes Centre, Norwich where he studied comparative reproductive tissue development using both crops and non-cultivated plant species as model systems. A principal driver for research in Lars’ laboratory is based on connecting disciplines in the area of developmental biology to understand how morphological diversity evolves.
Legumes are a staple part of many diets worldwide. The five leading types of legumes purchased in the US were pinto bean, black bean, kidney bean, lima bean, and chickpea.
In addition to his fundamental programme, Lars is committed to identifying translational opportunities to improve the yield and production of our most common crops, such as legumes. Legumes are a very important group of plants which include many staple foods such as beans, lentils, peas, and chickpeas. Most plants in this group are grown agriculturally for human consumption of livestock forage, so improving their yields will make a huge impact to global food security.
With his recently initiated programme on legume research, he will exploit his experience with model-to-crop approaches to improve specific traits related to legume pod growth and seed yield. Lars will continue this research now with the Department of Biology in Oxford.
Professor Lars Østergaard said:
> “It is a great honour to have been given this opportunity and I am hugely excited to establish my research programme at the new Department of Biology in Oxford. I look forward to building new collaborations across the department.”
The Sherardian Professorship, established in 1734, constitutes a long line of influential biologists working in the field of Botany. Lars takes over the post from Liam Dolan, whose work whilst in post has led to spin outs such as MOA in 2018. Liam’s research into the genetic mechanisms of plant growth, development and herbicide resistance was applied through MOA, and is now helping to tackle herbicide resistance in the food production industry.
Other former post holders include Arthur Tansley, who introduced the concept of ecosystems into biology, Bob Whatley, who contributed greatly to early work on photosynthesis, energy metabolism, and the origin of mitochondria in the serial endosymbiotic theory, and Hugh Dickinson who still contributes to work on epigenetics and cell fate in plant reproductive lineages, even in retirement.

Mark Fricker, Joint Head of the Department of Biology, said:
> “We are excited to welcome Lars to Oxford and the Department. His elegant experimental work on fruit development in model plants such as Arabidopsis and Capsella has significantly advanced the molecular understanding of this critical part of the plant life cycle. He has also begun to translate these fundamental discoveries into crop improvement for agronomically relevant members of the Brassicaceae and Fabaceae (legumes) using precision breeding. He is set to play a major role in developing these approaches in Oxford as part of the new Biology Department.”
</excerpt>
### Rank 5 of 7 — 0.46
<excerpt title="Sherardian Professor of Botany">
## List of Sherardian Professors of Botany
1.   Jump up to: 12"SHERARDIAN PROFESSORSHIP OF BOTANY". _Oxford University Gazette_. University of Oxford. 12 January 2006. Retrieved 13 January 2015.  
2.   ↑Allen, D. E. (September 2013). "Sherard, William (1659–1728)". _Oxford Dictionary of National Biography_ (online ed.). Oxford University Press. doi:10.1093/ref:odnb/25355. Retrieved 13 January 2015.(Subscription, Wikipedia Library access or UK public library membership required.)  
3.   ↑Boulger, G. S.; Hutchins, Roger (2004). "Williams, George (bap. 1762, d. 1834)". _Oxford Dictionary of National Biography_ (online ed.). Oxford University Press. doi:10.1093/ref:odnb/29504. Retrieved 14 January 2015.(Subscription, Wikipedia Library access or UK public library membership required.)  
4.   ↑Goddard, Nicholas (2004). "Daubeny, Charles Giles Bridle (1795–1867)". _Oxford Dictionary of National Biography_ (online ed.). Oxford University Press. doi:10.1093/ref:odnb/7187. Retrieved 14 January 2015.(Subscription, Wikipedia Library access or UK public library membership required.)  
5.   ↑"News". _Botanical Gazette_. **22** (5): 430–432. November 1896. doi:10.1086/327440. JSTOR2464014.  
6.   ↑"Professor Liam Dolan". _People at Magdalen_. Magdalen College, Oxford. Retrieved 13 January 2015.  
7.   ↑"Professor Lars Østergaard".
Categories:
*   Professorships at the University of Oxford  
*   Professorships in botany  
*   Magdalen College, Oxford  
*   1734 establishments in England
</excerpt>

## Search 2 — query: ""Sherardian Library" "MSS. Sherard 26-448" papers of individual botanists"
(no page could be scored)

## Search 3 — query: ""MSS. Sherard 26-448" catalogue"
(no page could be scored)

## Search 4 — query: ""MSS. Sherard 26-448" "papers of individual botanists" list"
(no page could be scored)

## Search 5 — query: ""papers of individual botanists" Sherardian Library list"
(no page could be scored)

## Search 6 — query: ""MSS. Sherard 26-448" "catalogue""
(no page could be scored)

## Search 7 — query: ""MSS. Sherard" 26-448 pdf catalogue"
(no page could be scored)

## Search 8 — query: ""Sherardian Library" "papers of individual botanists" catalogue pdf"
(no page could be scored)

## Search 9 — query: "MSS. Sherard 26-448 catalogue pdf"
### Rank 1 of 104 — 0.03 (passed on)
<excerpt title="MSS Catalog - Quality Standards">
# MSS Catalog
## Quick Links
### Use Multi-User PDFs To:
*   Save money when you buy a document for your team  
*   Save time by purchasing once for multiple users  
*   Effortlessly distribute a PDF to your team with our self-service interface

# MSS Catalog
## Quick Links
### How to Buy
*   To upgrade your PDF to a Multi-User Redline version, simply add the PDF to your cart and you will be presented with a pop-up window that will display user and pricing information.  
*   From the pop-up window, select your upgrade and press the “Add Selected Upgrades” button.
There are corrections to this edition, which are available as separate documents.
There are amendments to this edition, which are available as separate documents.
Techstreet's Printed Edition + PDF option allows you to purchase a print edition of your document along with a PDF for immediate download at a package price.
This is a historical version of this document. A more current edition is available.
This is the most up-to-date edition of this document.
A secure PDF contains features that enforce existing copyright laws by preventing reproduction or distribution to other users. In order to successfully use your secure PDF, Adobe Acrobat Reader 8.0 or higher, and the free FileOpen plug-in installed.
Includes the base document plus all amendments and changes
**Device/OS:**Macos  
**Browser:**Chrome 148.0.0.0  
**User Agent:**Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36  
**Store Name:**mss  
**Page:**/mss/subgroups/53418?srsltid=AYCX9vJoQXZ0uK36n5evn2AJF_30xaGpKqFyB7DyYgd0oH8qDoaUstik  
**Referrer:**Direct Navigation  
**IP:**210.119.114.22, 104.23.160.186  
**Language:**en  
**Customer #:**Not Logged In  
**Member?:**NO  
**Cart #:**1618632590  
**Order #:**None  
**Cookies:**YES  
×
Accuris Support Portal
Welcome to the
Accuris Support Portal
From this AI-based portal, you can...

# MSS Catalog
## Quick Links
### How to Buy
*   Submit a ticket to report an issue  
*   Track your cases’ progress  
*   Explore our knowledge base  
*   Start a live chat session
Go To Chat Now
</excerpt>
### Rank 2 of 104 — 0.03
<excerpt title="MSS SP-44: Steel Pipe Line Flanges">
## [PDF page 21]
26  40.00  4.25  4.94  8.75  29.44  28  2.00  36.00  29.50  31.88  0.500  29.500  0.781  R93  0.50  0.06  
28  42.25  4.38  5.19  9.25 31,62  28  2.12  38.00  31.50  33.88  0.500  31.500  0.781  R94  0.50  0.06  
30  44.50  4.50  5.50  9.75  33.94  28  2.12 40.25  33.75  36.12  0.500  33.750  0.781  R95  0.50  0.06  
32  47.00  4.62  5.81  10.25  36.12  28  2.38 42.50  36.00  38.75  0.562  36.000  0.906  R96  0.50  0.06  

## [PDF page 21]
34  49.00  4.75  6.06  10.62  38.31  28  2.38 44.50  38.00  40.75  0.562  38.000  0.906  R97  0.56  0.06  
36  51.75  4.88  6.38  11.12  40.62  28  2.62  47.00  40.25  43.00  0.562  40.250  0.906  R98  0.56  0.06  
38  50.00  6.00  6.12  10.00  40.25  28  2.38  45.75 41.50  -  ----  --  -  0.56 -  
40  52.00  6.25  6.38  10.38  42.25  32  2.38  47.75  43.75  ---  -  --  --  --0.'56 -  
42  55.25  6.62  6.75 11.00  44.38  28  2.62 50.50  46.00  --  ---  ---  --  --  0.56  -
</excerpt>
### Rank 3 of 104 — 0.03
<excerpt title="MSS SP-44: Steel Pipe Line Flanges">
## [PDF page 19]
26  38.25  3.12  3.31  7.25  28.38 28 1.75  34.50  29.50 31.88  O.SOO  29.500  0.781  R93  0.38  0.06  
28  40.75  3.38  3.56  7.75 30.50  28  1.75 37.00  31.50  33.88  0.500  31.500  0.781  R94  0.44  0.06  
30  43.00  3.62  3.75  8.25  32.56 28  1.88  39.25  33.75  36.12 0.500  33.750  0.781 R95 0.44  0.06  
32  45.25  3.88  3.94  8.75  34.69 28 2.00  41.50  36.00 38.75  0.562  36.000  0.906  R96  0.44  0.06  

## [PDF page 19]
34  47.50  4.00  4.12  9.12  36.88  i 28  2.00  43.50  38.00  40.75  0.562  38.000  0.906 R97  0.50  0.06  
36  50.00  4.12  4.38  9.50  39.00  32  2.12  46.00  40.25  43.00  0.562  40.250  0.906  R98  0.50  0.06  
38  46.00  4.25  4.25  7.12  39.12 32  1.62 43.00  40.50  --  --  --  --  --  0.50  -  
4J  48.75  4.50  4.50  7.62  41.25  32  1.75 45.50  42.75  --  --  --  --  -  0.50 -  
42  50.75  4.69  4.69  7.88  43.25 32  1.75  47.50  44.75  --  --  --  --  -  0.50  --
</excerpt>
### Rank 4 of 104 — 0.03
<excerpt title="MSS SP-44: Steel Pipe Line Flanges">
## [PDF page 22]
I  42  61.50  8.12  9.12  14.62  46.31  24  3.62  54.75  47.75  --  -  ----0.81 -  
44  64.88  8.44  9.56  15.38  48.62  24  3.88  57.62 50.00 --  -  ---  -  0.88  -
1  46  68.25  8.88  10.06  16.18  50.88  24  4.12  60.50  52.50  --  -  --  -  -  0.88  -  
l48  70.25  9.19  10.38  16.50  52.88  24  4.12  62.50  54.50  --  -  ---  -  0.94  -

## [PDF page 22]
~  ,~-  
General Notes:  Notes:  (a)  Rating for  raised  face flanges is  predicated  on the use  of sheet gaskets  shown  in Table  2.  
For matching  tolerances  see Section 10.  (b)  Dimensions  to be  specified  by customer.  
For welding  end detail  see  Figures  1,2 and 3.  (c)  See  Section 5.  00  
(d)  Where calculated  blind  thickness  is  less  than the  mating  welding  neck,  the  thicknesses.  "'=  
were  made equal.  See  paragraph 5.5  for material  requirements.  t  
(e)  Hub dimension for Size  24 'and smaller flanges  may vary as  explained  in  paragraph 5.3.2.

## [PDF page 23]
MSS  STANDARD PRACTICE  SP-44
I TABLE  11  -  PERMISSABLE IMPERFECTIONS IN  FLANGE FACING FINISH(a)  I
MAXIMUM RADIAL(b)  MAXIMUM DEPTH AND  RADIAL  
PROJECTION OF IMPERFECTIONS  PROJECfION OF IMPERFECfIONS  
NPS  WHICH ARE NO  DEEPER THAN  WHICH ARE  DEEPER THAN  
THE BOTTOM  OF THE  THE BOTTOM  OF THE  
SERRATIONS~ IN.  SERRATIONS, IN.
12  -14  0.31  0.18  
16  0.38  0.18  
18  -  24  0.50  0.25
26  -  36  0.50  0.25  
38  -  48  0.56  0.28  
50-60  0.62  0.31
NOTES:  (a)  Imperfections  less  than half the  depth  of the  serrations  shall  not  be cause  for  rejection.  
See paragraph 7.4.  
(b)  A  radial  projection shall be  measured  by  the  difference  between  an  inner  radius  and  an  
outer  radius  encompassing  the  imperfection  where  the  radius  is  struck  from  the  center  
line  of the  bore.
17
</excerpt>
### Rank 5 of 104 — 0.03
<excerpt title="MSS SP-44: Steel Pipe Line Flanges">
## [PDF page 21]
FLANGE  DIMENSIONS  HUB  DIM.  DRILLING  r ACING DIMENSIONS  
Pipe  00 of  THICK. OF HAN.  (e)  No.  of  Dia.  of  Dia  . of  Raised  RING -TYPE JOINT FiUet  Groove  
Size  F(ange  Weld-  Bld'(d)  Length  ODLarge'  Bolt  Bolt  Bolt  Face  Facing  tJepth Pitch WIdth  Ring  Radius  Fillet  
Neck  Thru  Hub Fig. End  Hub  Holes  Holes  Cirde  Dia.  Dia.  of Groo~e Dia.  Gr~~ve  No.  (min)  Radius  
0  C E  Y  X  R  K i-  F D  A  r  
12  22.00  2.62  2.62  6.12 15.75  20  1.38  19.25  15.00  16.25  0.312  15.000  0.469  R57  0.44  0.03  
14  23.75  2.75  2.75 6.50  17.00  20  1.50  20.75 16.25  \8.00  D.312  16.500  0.469  R61  0.44  0.03  
16  27.00  3.00  3.00  7.00  19.50  20  1.62  23.75  \8.50  20.00  0.312  18.500  0.469  R65  0.44  0.03  

## [PDF page 21]
18  29.25  3.25  3.25  7.25 21.50  20 1,75  25.75  21.00  22.62  0.312  21.000  0.469  R69  0.44  0.03  
20  32.00  3.50  3.50  7.50 24.00  24  1.75 28.50  23.00  25:00  0.375  23.000  0.531  R73  0.44  0.06  
22  34.25  3.75  3.75  7.75 26.25  24  1.88 30.62 25.25  27.00  0.438  25.000  0.594  R81  0.44  0.06  
24  37.00  4.00  4.00  8.00  28.25  24  2.00  33.00  27.25  29.50  0.438  27.250  0.656  R77  0.44  0.06
</excerpt>

## Search 10 — query: ""MSS. Sherard 26-448" pdf"
(no page could be scored)

# Example 4
## Question
According to Stats Canada, which three categories regarding timber assets in Quebec (by area in hectares) saw the largest raw growth from 1961 to 1962?

## Expected answer
Fire, Regeneration, Non-reserved Accessible Closing Stock

## Grade 0.00

## Search 1 — query: "Statistique Canada bois assets Quebec 1961 1962 hectares growth raw growth"
### Rank 1 of 37 — 0.02 (passed on)
<excerpt title="From mixed dairy farming to intensive feedlot agriculture: The evolution of ...">
#### Editor’s Note: This is part of a series showing the work of the Sustainable Farm Systems project.
In summary, this specialization in swine production, the result of a socioecological transition towards an industrial regime, is not efficient or sustainable, as it is the cause of serious landscape and environmental costs (i.e. landscape degradation, loss of biodiversity, or contamination of groundwater). Although agricultural productivity has increased greatly, the changes have resulted in the consumption of large amounts of energy, most of which is imported, contributing to global warming. Studies of traditional agroecosystems, however, can help our society in a transition towards a new more sustainable socioecological regime.

#### Editor’s Note: This is part of a series showing the work of the Sustainable Farm Systems project.
###### Feature Image: “Farmer girl milking a cow”. Provided by Julie Ruiz, UQTR.
* * *
[[1]](https://niche-canada.org/2016/10/21/from-mixed-dairy-farming-to-intensive-feedlot-agriculture-the-evolution-of-agrarian-landscapes-in-quebec/#_ftnref1)Haberl, H., V. Winiwarter, K. Andersson, R.U. Ayres, C. Boone, A. Castillo, G. Cunfer, M. Fischer-Kowalski, W.R. Freudenburg, E. Furman, R. Kaufmann, F. Krausmann, E. Langthaler, H. Lotze-Campen, M. Mirtl, C.L. Redman, A. Reenberg, A. Wardell, B. Warr, and H. Zechmeister. 2006, “From LTER to LTSER: Conceptualizing the socioeconomic dimension of long-term socioecological research.” _Ecology and Society_ 11: 2-13.

#### Editor’s Note: This is part of a series showing the work of the Sustainable Farm Systems project.
###### Feature Image: “Farmer girl milking a cow”. Provided by Julie Ruiz, UQTR.
[[2]](https://niche-canada.org/2016/10/21/from-mixed-dairy-farming-to-intensive-feedlot-agriculture-the-evolution-of-agrarian-landscapes-in-quebec/#_ftnref2)González de Molina, M., Toledo, V.M., 2014. _The Social Metabolism. A Socio-Ecological Theory of Historical Change, Environmental History_. Springer, New York; Marull, J., Pino, J., Tello, E., Cordobilla, M.J., 2010. Social metabolism, landscapechangeandland-useplanning in the Barcelona MetropolitanRegion. _Land Use Policy_ 27, 497–510; Tello, E., Galán, E., Sacristán, V., Cunfer, G., Guzmán, G.I., González de Molina, M., Krausmann, F., Gingrich, S., Padró, R., Marco, I., Moreno-Delgado, D., 2016. Openingtheblack box of energythroughputs in farmsystems: A decompositionanalysisbetweentheenergyreturns to external inputs, internalbiomassreusesand total inputs consumed (the Vallès County, Catalonia, c.1860 and 1999). _Ecological Economics_ 121, 160–174.
[[3]](https://niche-canada.org/2016/10/21/from-mixed-dairy-farming-to-intensive-feedlot-agriculture-the-evolution-of-agrarian-landscapes-in-quebec/#_ftnref3) Ecological connectivity is a measure of the capacity of one species to move across a heterogeneous landscape without being interrupted by artificial barriers.
[[4]](https://niche-canada.org/2016/10/21/from-mixed-dairy-farming-to-intensive-feedlot-agriculture-the-evolution-of-agrarian-landscapes-in-quebec/#_ftnref4) Statistics Canada, 1968: _1966 Census of Agriculture,_ Statistics Canada, Ottawa.
</excerpt>
### Rank 2 of 37 — 0.02
<excerpt title="When Did Quebec Catch Up Economically?">
## [PDF page 4]
1.  See Vincent  Geloso, Grand ratt rapage et déclin t ranquille: Une histoire économique et soc iale  
du Quebec depuis 1900, Accent grave, 2013, for an extensive discussion of  these issues.  910 Peel Street, Suite 600  
2 .  Morris Altman, “Economic Development with High Wages: An Historical Perspective,”  Montreal (Quebec) H3C 2H8, Canada  
Explorations in Economic Histor y, Vol. 25 (1988), p. 203.  Telephone: 514-273-0969  
3 .  Herbert Emer y and Clint Levitt, “Cost of  living, real wages and real incomes in thirteen  Fax: 514-273-2581  
Canadian cities, 1900–1950,” Canadian Journal of Economics / Revue canadienne  Website: www.iedm.org  
d’économique, Vol. 35 (2002), No. 1, p. 135.  The Montreal Economic Institute is an independent, non-partisan, not-for-  
4 .  Chris Minns and Mar y McKinnon, The Impact of School Prov ision on Pupil Attendance:  profit research and educational organization. Through its publications, media  
Ev idence from the Early 20th centur y, Working Paper No. 116/09 (2009), Department of  appearances and conferences, the MEI stimulates debate on public policies in  
Economic Histor y, London School of  Economics and Political Science, p. 29.  Quebec and across Canada by proposing wealth-creating reforms based on  
5.  Gérard Bernier and Robert Boily, Le Quebec en chiffres, de 1850 à nos jours, Association  market mechanisms. It does not accept any government funding.  
canadienne-française pour l’avancement des sciences, 1986, pp. 208-211.  The opinions expressed in this study do not necessarily represent those of  the  

## [PDF page 4]
6 .  Dominion Bureau of  Statistics, Canada Year  Book, 1961, p. 752.  Montreal Economic Institute or of  the members of  its board of  directors.  
7 .  Dominion Bureau of  Statistics, Canada Year  Book, 1948-1949 and 1961; Statistics Canada,  
Histor ical Statistics of Canada: Section K – Consumer Pr ice Indexes for Reg ional Cities, 1940  The publication of  this study in no way implies that the Montreal Economic  
to 1975.  Institute or the members of  its board of  directors are in favour of  or oppose  
8 .  (For Quebec investment) Dominion Bureau of  Statistics, Canada Year  Book, 1947 and  the passage of  any bill.  
1962; (for inflation) Statistics Canada, Histor ical Statistics of Canada: Section K – Consum  -  
er Pr ice Indexes for Reg ional Cities, 1940 to 1975; (for workers) Ministère du Commerce et  Reproduction is authorized for non-commercial educational purposes  
de l’Industrie, L’Annuaire statistique du Quebec, 1960 and 1977-1978.  provided  the source is mentioned.  
9 .  Dominion Bureau of  Statistics, Canada Year  Book,  1948-49, p. 1051; Dominion Bureau of  Montreal Economic Institute © 2013  
Statistics, Canada Year  Book, 1962, p. 1108.  
10.  Ministère du Commerce et de l’Industrie, L’Annuaire statistique du Quebec, 1961, p. 648.  Illustration: Ygreck  Graphic design: Mireille Dufour  
11.  Ibid., p. 604.  
12.  See the addenda on the Montreal Economic Institute website at iedm.org.  
4
</excerpt>
### Rank 3 of 37 — 0.01
<excerpt title="Forestry in Quebec: 15 Facts & Statistics">
# Forestry in Quebec: 15 Facts & Statistics
### VIDEO: Asia Pays Premium for Canadian Oil, While U.S. Discount Widens
Video Script: Remember when anti-everything groups said new oil pipelines would create no value for Canadians an...
[![Image 11: Canada's Largest Ports: Top 5 Busiest Canadian Seaports](https://assets.nationbuilder.com/canadaaction/pages/7512/meta_images/original/Canada's_largest_seaports_-_Top_5_busiest_ports_in_Canada.jpg?1760983406)](https://www.canadaaction.ca/largest-seaports-canada)

# Forestry in Quebec: 15 Facts & Statistics
### Canada's Largest Ports: Top 5 Busiest Canadian Seaports
With coastlines on both the Pacific and Atlantic Oceans, Canadians are incredibly blessed to have access to coastal ...
*     
*     
*     
*     
*   

*       *   Take Action  
    *   Join Us  
    *   Volunteer  
    *   Social Media  
    *   Young Canadians for Resources  
    *   Infographics  
    *   Campaigns

*       *   Issues  
    *   Natural Resources  
    *   Indigenous Communities  
    *   Canadian Economy  
    *   Nuclear Electricity  
    *   Energy Security  
    *   LNG Development  
    *   Trade Diversification

*   Blog  
*       *   About  
    *   Who We Are  
    *   Contact  
    *   Funding  
    *   Donate  
    *   Resources For Kids
Principles, Privacy Policy & Terms of Use
Copyright © 2026 Canada Action Coalition
</excerpt>
### Rank 4 of 37 — 0.01
<excerpt title="How much forest does Canada have?">
## On this page
*   Theme introduction  
*   Changes in forest area  
*   Indicator: Forest area  
*   Indicator: Deforestation and afforestation  
*   Indicator: Wood volume  
*   Sources and information

## Theme introductionFootnote 1
Canada is home to 369 million hectares (ha) of forest, or 3.69 million km 2, which is close to 9% of the world’s total forest. To get a sense of the area of Canada’s forests, the land area of India is about 297 million ha. Canadians depend on and value these forests for many different uses including recreation, conservation, traditional Indigenous practices and sustainable timber harvest. Strict rules require harvest areas to be regenerated either through planting or natural regrowth. Canada’s National Deforestation Monitoring System reports that over the last 34 years, less than half of 1% of Canada’s forest has been deforested.

## Theme introductionFootnote 1
### What is a forest?
Canada’s National Forest Inventory (NFI) uses the United Nations Food and Agriculture Organization definition of forest area:
*   land not predominantly under agricultural or urban land use  
*   spanning an area greater than 0.5 ha  
*   with trees taller than 5 m and tree canopy cover of more than 10%
OR
*   land that has the capability to support trees taller than 5 m with more than 10% canopy cover
Forest area is still considered to be forest after a temporary loss of tree cover, such as after wildfire or clearcut harvesting. Changes in forest area result from:
*   Afforestation—the deliberate establishment of forests on lands previously not forested  
*   Deforestation—the permanent clearing of forests to make way for new, non-forest land uses, such as agriculture or urban expansion  
*   Natural forest expansion or dieback

## Theme introductionFootnote 1
### How do we monitor the change in our forests?
The Canadian Forest Service (CFS) works with provincial and territorial partners to maintain Canada’s national forest monitoring and reporting capabilities via the NFI, the National Forest Information System, the National Forestry Database and the National Forest Carbon Monitoring Accounting and Reporting System. Remote sensing also plays a crucial role enabling increasingly more detailed forest monitoring over large areas.
The technology and programs that Canada uses to monitor forests and how they change have evolved since the creation of the CFS 125 years ago. While each province and territory have long-standing programs to monitor forests in their jurisdictions, the NFI is only 24 years old. In comparison, Sweden, the United Kingdom (UK), and several other countries have decades of data collected through their NFIs. Canada’s relatively young NFI was created to ensure our forest monitoring uses a statistically robust sampling approach by using a national plot network with consistent methodology. The NFI replaced older monitoring methods such as the Canadian Forest Inventory (CanFI), which relied on data submissions from various sources and did not include large areas of northern forests.

## Theme introductionFootnote 1
### How do we monitor the change in our forests?
#### Select National Forest Inventories around the world
Image summary  
Flags representing each country and the year their NFIs were established.
**Select National Forest Inventories around the world**
*   Finland (1921)  
*   UK (1924)  
*   France (1958)  
*   Mexico (2002)  
*   Russia (2008)  
*   Sweden (1923)  
*   USA (1930)  
*   Canada (2000)  
*   Brazil (2005)
Canada’s NFI was created to provide recurrent estimates and show changes over time for many forest attributes across the country. Forest change is determined by comparing the values between two points in time, which helps us understand trends. Shortly after Canada’s NFI was created, the CFS could publish point estimates of many forest attributes. However, only recently has enough data been collected to publish information on forest change. This is a major milestone for our NFI! Using data collected between 2000 and 2017, we can estimate changes in Canadian forests over that period. This is the time between the “establishment” and “first remeasurement” periods as seen below.
</excerpt>
### Rank 5 of 37 — 0.01
<excerpt title="From mixed dairy farming to intensive feedlot agriculture: The evolution of ...">
#### Editor’s Note: This is part of a series showing the work of the Sustainable Farm Systems project.
###### Feature Image: “Farmer girl milking a cow”. Provided by Julie Ruiz, UQTR.
[[2]](https://niche-canada.org/2016/10/21/from-mixed-dairy-farming-to-intensive-feedlot-agriculture-the-evolution-of-agrarian-landscapes-in-quebec/#_ftnref2)González de Molina, M., Toledo, V.M., 2014. _The Social Metabolism. A Socio-Ecological Theory of Historical Change, Environmental History_. Springer, New York; Marull, J., Pino, J., Tello, E., Cordobilla, M.J., 2010. Social metabolism, landscapechangeandland-useplanning in the Barcelona MetropolitanRegion. _Land Use Policy_ 27, 497–510; Tello, E., Galán, E., Sacristán, V., Cunfer, G., Guzmán, G.I., González de Molina, M., Krausmann, F., Gingrich, S., Padró, R., Marco, I., Moreno-Delgado, D., 2016. Openingtheblack box of energythroughputs in farmsystems: A decompositionanalysisbetweentheenergyreturns to external inputs, internalbiomassreusesand total inputs consumed (the Vallès County, Catalonia, c.1860 and 1999). _Ecological Economics_ 121, 160–174.
[[3]](https://niche-canada.org/2016/10/21/from-mixed-dairy-farming-to-intensive-feedlot-agriculture-the-evolution-of-agrarian-landscapes-in-quebec/#_ftnref3) Ecological connectivity is a measure of the capacity of one species to move across a heterogeneous landscape without being interrupted by artificial barriers.
[[4]](https://niche-canada.org/2016/10/21/from-mixed-dairy-farming-to-intensive-feedlot-agriculture-the-evolution-of-agrarian-landscapes-in-quebec/#_ftnref4) Statistics Canada, 1968: _1966 Census of Agriculture,_ Statistics Canada, Ottawa.

#### Editor’s Note: This is part of a series showing the work of the Sustainable Farm Systems project.
###### Feature Image: “Farmer girl milking a cow”. Provided by Julie Ruiz, UQTR.
[[5]](https://niche-canada.org/2016/10/21/from-mixed-dairy-farming-to-intensive-feedlot-agriculture-the-evolution-of-agrarian-landscapes-in-quebec/#_ftnref5) Statistics Canada, 1953: _Ninth Census of Agriculture. 1951,_ Statistics Canada, Ottawa ; Statistics Canada, 2012: 2011 Census of Agriculture. Available online at: http://www.statcan.gc.ca/eng/ca2011/index.
The following two tabs change content below.
*   Bio  
*   Latest Posts
</excerpt>

## Search 2 — query: ""timber assets" Quebec 1961 1962 hectares"
### Rank 1 of 1493 — 0.07 (passed on)
<excerpt title="and Resource Accounts Concepts, Sources and Methods of the ...">
## [PDF page 48]
serves.  •  The linkage of the SAA with the MEFA (Chapter 4) will  
Production, capital costs and operating costs - Data on  be strengthened so that the effect of recycling on the  
quantity and value of production and operating costs for  rate of depletion of metal reser ves can be better stud-  
metal mines are available from Statistics Canada1 and from  ied.  
the Minerals and Metals Policy Sector of Natural Resources  •  Finally, attention will be given to overcoming two shor t-  
Canada. The value of the produced capital stock used in  comings of the valuation methods currently employed  
coal mines and the value of the annual depreciation of that  in the MSAA. The first of these is the fact that mone-  
stock, by province and coal type, are also available from  tar y values are calculated for only a small par t of Can-  
Statistics Canada.2  ada’s known subsoil asset reser ves. The second is the  
Classification of metal assets  - The classification of metal  tendency of the present value method to underesti-  
assets used in the physical account is distinct from that in  mate the value of subsoil assets.  
the monetary account. While the physical account records  
reserves on a metal-by-metal basis, the monetary account  
records reserves by mine type. The classification of mine  3.4  Timber Asset Accounts  
used in the monetary account is identical to the classifica-  
tion of mining industries in the  Standard Industrial Classifi-  The  Timber Asset Accounts comprise two accounts–one  
cation (Statistics Canada, 1980):  physical and one monetary–describing Canada’s timber as-  
•  gold mines;  sets. These accounts currently focus on the use of the for-  
est for timber supply only. Other uses of the forest–for  
•  copper and copper-zinc mines;  recreation or wildlife habitat for example–have not yet been  
•  nickel-copper mines;  considered. Timber supply has been chosen as the initial  
orientation of the account since this is the principal econom-  
•  silver-lead-zinc mines;  ic use of the forest in Canada.  
•  molybdenum mines;  As mentioned, the Timber Asset Accounts (TAA) comprise  
two accounts: the  Physical Timber Asset Account  

## [PDF page 48]
•  uranium mines; and  (PTAA) and the  Monetary Timber Asset Account  
•  iron mines.  (MTAA). Both accounts present annual time series data be-  
ginning in 1961 at the national and provincial/territorial lev-  
Classification by mine type rather than metal in the mone-  els. The PTAA provides year-end quantitative measures of  
tary account precludes arbitrary decisions regarding the  Canada’s timber asset stocks and the impacts of harvesting  
share of mine development and exploitation costs attributa-  and natural events on these stocks. The MTAA, being the  
ble to each metal in polymetallic mines.3  value counterpart of the physical account, presents year-  
end value estimates for these same stocks. Although the  
stocks that are valued in the MTAA are the same as those  
described in physical terms in the PTAA, the stock changes  
shown in the physical account (growth, harvesting and nat-  
ural losses) do not currently have monetary equivalents in  
the MTAA.  
In Canada, forest quality (in the sense of timber productivi-
1.  Statistics Canada,  Metal Mines, Catalogue no. 26-223.  ty) and accessibility limit the portion of the forest that pro-  
2.  Statistics Canada, Investment and Capital Stock Division.  vides economic benefit. For this reason, only the  
3.  A polymetallic mine is one at which more than one metal is mined.
40Statistics Canada - Catalogue no. 16-505-GIE Concepts, Sources and Methods
</excerpt>
### Rank 2 of 1493 — 0.07
<excerpt title="Timber assets (area)">
# Timber assets (area)
*   Skip to main content  
*   Skip to "About this site"

# Timber assets (area)
## Language selection
*   Français
/ Gouvernement du Canada

# Timber assets (area)
## Search and menus
*   Search and menus

# Timber assets (area)
## Search
Search Statistics Canada
Search

# Timber assets (area)
## Topics menu
*   Subjects  
*   Data  
*   Analysis  
*   Reference  
*   Geography  
*   Census  
*   Surveys and statistical programs  
*   About StatCan  
*   Canada.ca
1.   Home  
2.   Data

# Timber assets (area)
## Archived Content
Information identified as archived is provided for reference, research or recordkeeping purposes. It is not subject to the Government of Canada Web Standards and has not been altered or updated since it was archived. Pleasecontact us to request a format other than those available.
[Content is archived.](javascript:;)

# Archived - Timber assets (area) (x 1,000)1, 2
Frequency:Annual
Table: 38-10-0106-01 (formerly CANSIM 153-0029)
Release date: 2010-09-28
_Geography:_
Help
Save my customizations
Customize table
Geography :
Reference period
From:  To:
Apply
Add/Remove data

# Archived - Timber assets (area) (x 1,000)1, 2
## Add/Remove data help
Select your items to create your customized table.
Download options

# Archived - Timber assets (area) (x 1,000)1, 2
## Download options
### CSV Download as displayed{{ csvSize }}kB.


# Archived - Timber assets (area) (x 1,000)1, 2
## Download options
### CSV Download as displayed(excluding accompanying symbols).


# Archived - Timber assets (area) (x 1,000)1, 2
## Download options
### CSV Download as displayed(symbols separate).


# Archived - Timber assets (area) (x 1,000)1, 2
## Download options
### CSV Download selected data(for database loading).


# Archived - Timber assets (area) (x 1,000)1, 2
## Download options
### CSV Download cube metadata information, ~50kB.


# Archived - Timber assets (area) (x 1,000)1, 2
## Download options
### CSV Download entire table "Timber assets (area)".


# Archived - Timber assets (area) (x 1,000)1, 2
## Download options
### SDMX Download entire table.
Other data access options:Developers
Showing  records
Filter
Reset
No results found.
**Notes :**
**How to cite:** Statistics Canada. Table 38-10-0106-01 Timber assets (area) (x 1,000)
**DOI:**https://doi.org/10.25318/3810010601-eng

# Archived - Timber assets (area) (x 1,000)1, 2
## Related information
Source (Surveys and statistical programs)
*   Canadian System of Environmental-Economic Accounts - Natural Resource Asset Accounts
Subjects and keywords

# Archived - Timber assets (area) (x 1,000)1, 2
## Related information
### Subjects
*   Economic accounts  
    Environment accounts

    

*   Environment  
    Land, oceans, ecosystems and biodiversity
Date modified: 2026-11-18

# Archived - Timber assets (area) (x 1,000)1, 2
## About this site
### Statistics Canada
*   Contact StatCan  
*   Trust Centre

# Archived - Timber assets (area) (x 1,000)1, 2
## About this site
### Government of Canada
*   All contacts  
*   Departments and agencies  
*   About government
</excerpt>
### Rank 3 of 1493 — 0.05
<excerpt title="and Resource Accounts Concepts, Sources and Methods of the ...">
## [PDF page 33]
Natural resource assets, in general, are those natu-  Non-financial assets (national wealth)  
ral resources over which ownership rights can be en-  1 Produced assets  
forced and from which economic benefits can be  1.1 Capital (structures, machinery and equipment)  
derived by the owners. They meet the criteria for qual-  
ification as economic assets as set out in the SNA93,  1.2 Consumer durables (autos, furniture and appli-  
where they are termed  tangible non-produced as-  ances)  
sets.  1.3 Inventories  
Land assets include land associated with residential  1.4 Other produced assets (monuments, valuables  
and non-residential buildings, agricultural land and  and collectibles)  
land used for recreation or environmental protection  2 Non-produced assets  
(parkland for example).  2.1 Land  
Timber assets  are those timber stocks that are capa-  Residential land  
ble of producing a merchantable stand within a rea-  Non-residential built-up land  
sonable period of time, that are physically accessible  Agricultural land  
and that are not reserved for purposes other than har-  Land inventory2  
vesting.  Recreational and protected land  
Subsoil assets  are restricted to  developed reserves  2.2 Timber  
of subsoil resources; that is, those reserves that can  2.3 Wildlife  
be expected to be recovered through existing installa-  Fish  
tions (wells or mines) under existing operating meth-  
ods and economic conditions.  Undeveloped  Other wildlife  
reserves of subsoil resources are those that require  2.4 Subsoil assets  
further capital investment before extraction can occur;  Oil, crude bitumen and natural gas  
they are not considered economic assets because  Coal  
economic benefits cannot be derived from them in the  Metals  
immediate future.  Undiscovered recoverable re-  Non-metals  
sources are those believed to exist on the basis of  
available geological and geophysical evidence, but  3 Intangible assets  
which have not yet been shown to exist by drilling,  3.1 Goodwill3  
testing or production.  3.2 Other intangible assets
</excerpt>
### Rank 4 of 1493 — 0.05
<excerpt title="and Resource Accounts Concepts, Sources and Methods of the ...">
## [PDF page 5]
2.5  Denmark................................................................ 17  4  Material and Energy Flow Accounts  .......................67  
2.6  The Netherlands.................................................... 17  4.1  Rationale, uses and linkages  ................................68  
2.7  Sweden  ................................................................. 18  4.1.1  Why account for materials and energy?  ........68  
2.8  France  ................................................................... 18  4.1.2  Uses of the MEFA  ..........................................69  
2.9  Summary  ............................................................... 19  4.1.3  Linkages to other accounts  ............................70  
3  Natural Resource Stock Accounts  .......................... 21  4.2  Key concepts .........................................................71  
3.1  Rationale, uses and linkages  ................................ 23  4.3  The MEFA accounting framework  .........................73  
3.1.1  Uses  ............................................................... 25  4.3.1  Benefits of the input-output framework  ..........75  
3.1.2  Linkages to other accounts  ............................ 26  4.3.2  Elements of the framework  ............................76  
3.2  Physical versus monetary accounts  ...................... 27  4.3.3  Treatment of durable-good wastes  ................80  
4.3.4  Classifications  ................................................82  
3.2.1  Valuation in the NRSA  ................................... 27  4.4  Data sources and methods  ...................................85  
3.2.2  Other market and non-market values  ............ 31  4.4.1  Water  .............................................................86  
3.3  Subsoil Asset Accounts......................................... 32  4.4.2  Energy ............................................................88  
3.3.1  Physical Accounts  .......................................... 32  4.4.3  Greenhouse gases .........................................91  
3.3.2  Monetary accounts......................................... 35  4.4.4  Data Gaps  ......................................................95  

## [PDF page 5]
3.3.3  Reconciliation accounts  ................................. 38  4.5  Future directions for the MEFA  .............................96  
3.3.4  Data sources and methods  ............................ 38  
3.3.5  Future directions for the  Annex 4.1  Statistics Canada’s  
Subsoil Asset Accounts  ................................. 40  Input-Output Accounts ................................97  
3.4  Timber Asset Accounts  ......................................... 40  
3.4.1  Physical Timber Asset Account  ..................... 41  Annex 4.2  Technical details of MEFA indicators  .......100
Canadian System of Environmental and Resource AccountsStatistics Canada - Catalogue no. 16-505-GIEiii
</excerpt>
### Rank 5 of 1493 — 0.04
<excerpt title="and Resource Accounts Concepts, Sources and Methods of the ...">
## [PDF page 33]
Linking the Environment and the Economy  Natural Resource Stock Accounts
Text Box 3.1  Text Box 3.2  
Natural Resource Assets in the NRSA  Non-ﬁnancial Assets of the CNBSA  1

## [PDF page 33]
Natural resource assets, in general, are those natu-  Non-financial assets (national wealth)  
ral resources over which ownership rights can be en-  1 Produced assets  
forced and from which economic benefits can be  1.1 Capital (structures, machinery and equipment)  
derived by the owners. They meet the criteria for qual-  
ification as economic assets as set out in the SNA93,  1.2 Consumer durables (autos, furniture and appli-  
where they are termed  tangible non-produced as-  ances)  
sets.  1.3 Inventories  
Land assets include land associated with residential  1.4 Other produced assets (monuments, valuables  
and non-residential buildings, agricultural land and  and collectibles)  
land used for recreation or environmental protection  2 Non-produced assets  
(parkland for example).  2.1 Land  
Timber assets  are those timber stocks that are capa-  Residential land  
ble of producing a merchantable stand within a rea-  Non-residential built-up land  
sonable period of time, that are physically accessible  Agricultural land  
and that are not reserved for purposes other than har-  Land inventory2  
vesting.  Recreational and protected land  
Subsoil assets  are restricted to  developed reserves  2.2 Timber  
of subsoil resources; that is, those reserves that can  2.3 Wildlife  
be expected to be recovered through existing installa-  Fish  
tions (wells or mines) under existing operating meth-  
ods and economic conditions.  Undeveloped  Other wildlife  
reserves of subsoil resources are those that require  2.4 Subsoil assets  
further capital investment before extraction can occur;  Oil, crude bitumen and natural gas  
they are not considered economic assets because  Coal  
economic benefits cannot be derived from them in the  Metals  
immediate future.  Undiscovered recoverable re-  Non-metals  
sources are those believed to exist on the basis of  
available geological and geophysical evidence, but  3 Intangible assets  
which have not yet been shown to exist by drilling,  3.1 Goodwill3  
testing or production.  3.2 Other intangible assets
</excerpt>

## Search 3 — query: "StatCan "Timber assets (area)" 1961 1962 Quebec""
### Rank 1 of 251 — 0.09 (passed on)
<excerpt title="Timber assets (area)">
# Timber assets (area)
*   Skip to main content  
*   Skip to "About this site"

# Timber assets (area)
## Language selection
*   Français
/ Gouvernement du Canada

# Timber assets (area)
## Search and menus
*   Search and menus

# Timber assets (area)
## Search
Search Statistics Canada
Search

# Timber assets (area)
## Topics menu
*   Subjects  
*   Data  
*   Analysis  
*   Reference  
*   Geography  
*   Census  
*   Surveys and statistical programs  
*   About StatCan  
*   Canada.ca
1.   Home  
2.   Data

# Timber assets (area)
## Archived Content
Information identified as archived is provided for reference, research or recordkeeping purposes. It is not subject to the Government of Canada Web Standards and has not been altered or updated since it was archived. Pleasecontact us to request a format other than those available.
[Content is archived.](javascript:;)

# Archived - Timber assets (area) (x 1,000)1, 2
Frequency:Annual
Table: 38-10-0106-01 (formerly CANSIM 153-0029)
Release date: 2010-09-28
_Geography:_
Help
Save my customizations
Customize table
Geography :
Reference period
From:  To:
Apply
Add/Remove data

# Archived - Timber assets (area) (x 1,000)1, 2
## Add/Remove data help
Select your items to create your customized table.
Download options

# Archived - Timber assets (area) (x 1,000)1, 2
## Download options
### CSV Download as displayed{{ csvSize }}kB.


# Archived - Timber assets (area) (x 1,000)1, 2
## Download options
### CSV Download as displayed(excluding accompanying symbols).


# Archived - Timber assets (area) (x 1,000)1, 2
## Download options
### CSV Download as displayed(symbols separate).


# Archived - Timber assets (area) (x 1,000)1, 2
## Download options
### CSV Download selected data(for database loading).


# Archived - Timber assets (area) (x 1,000)1, 2
## Download options
### CSV Download cube metadata information, ~50kB.


# Archived - Timber assets (area) (x 1,000)1, 2
## Download options
### CSV Download entire table "Timber assets (area)".


# Archived - Timber assets (area) (x 1,000)1, 2
## Download options
### SDMX Download entire table.
Other data access options:Developers
Showing  records
Filter
Reset
No results found.
**Notes :**
**How to cite:** Statistics Canada. Table 38-10-0106-01 Timber assets (area) (x 1,000)
**DOI:**https://doi.org/10.25318/3810010601-eng

# Archived - Timber assets (area) (x 1,000)1, 2
## Related information
Source (Surveys and statistical programs)
*   Canadian System of Environmental-Economic Accounts - Natural Resource Asset Accounts
Subjects and keywords

# Archived - Timber assets (area) (x 1,000)1, 2
## Related information
### Subjects
*   Economic accounts  
    Environment accounts

    

*   Environment  
    Land, oceans, ecosystems and biodiversity
Date modified: 2026-11-18

# Archived - Timber assets (area) (x 1,000)1, 2
## About this site
### Statistics Canada
*   Contact StatCan  
*   Trust Centre

# Archived - Timber assets (area) (x 1,000)1, 2
## About this site
### Government of Canada
*   All contacts  
*   Departments and agencies  
*   About government
</excerpt>
### Rank 2 of 251 — 0.07
<excerpt title="A Historical Feminist Political Ecology of Eastern Ontario's Forests, 1849">
# Ontario’s F orests, 1849 - 2013
## Gendered Socionature (Identities, Roles & Relations)
Sorlin, Sverker and Warde, Paul. (2007). The problem of the problem of environmental
history: A re-reading of the field. Environmental History, 12 (1), 107-130.
Spivak, Gayatri Chakravorty. (1987) In other worlds: Essays in Cultural Politics . New York: Metheun.
Statistics Canada, Timber Assets (Volume) for Ontario, 1961 to 1997. Table Number:
1530030. Timber Harvests, Table Number I530030.
Statistics Canada, Timber Assets (Area) for Ontario, 1961 to 1997. Table Number 1530029.
Timber Assets, Table Number I530029.
Statistics Canada, Value of Timber Stocks by Province, 1961-997. Table Number 1530011.
Timber Stocks by Province, Table Number 1530011.
Statistics Canada. (2014). Natural Resources: Ontario forest resources data. Retrieved from
http://cfs.nrcan.gc.ca/statsprofile/overview/on
Statistics Canada. (2014). Natural Resources: Forest area harvested by province and territory,
1975 to 2011. Retrieved from  http://www.statcan.gc.ca/tables-tableaux/sum
som/l01/cst01/envi36a-eng.htm
Statistics Canada. (2014). Lumber production by species, external trade and estimated 216
consumption, 1908 to 1975. Retrieved from
http://www5.statcan.gc.ca/access_acces/archive.action?l=eng&loc=L134_148-eng.csv
Statistics Canada. (2018). Forest inventory overview. Retrieved from
https://cfs.nrcan.gc.ca/statsprofile/overview/ca
Stratford, Angela. (2007). Racialization of poverty: Indigenous women, the Indian Act and
</excerpt>
### Rank 3 of 251 — 0.04
<excerpt title="Timber assets (area)">
# Archived - Timber assets (area) (x 1,000)1, 2
## About this site
### Government of Canada
*   All contacts  
*   Departments and agencies  
*   About government

# Archived - Timber assets (area) (x 1,000)1, 2
## About this site
### Government of Canada
#### Themes and topics
*   Jobs  
*   Immigration and citizenship  
*   Travel and tourism  
*   Business  
*   Benefits  
*   Health  
*   Taxes  
*   Environment and natural resources  
*   National security and defence  
*   Culture, history and sport  
*   Policing, justice and emergencies  
*   Transport and infrastructure  
*   Canada and the world  
*   Money and finance  
*   Science and innovation  
*   Indigenous peoples  
*   Veterans and military  
*   Youth  
*   Manage life events

# Archived - Timber assets (area) (x 1,000)1, 2
## About this site
### Government of Canada Corporate
*   Social media  
*   Mobile applications  
*   About Canada.ca  
*   Terms and conditions  
*   Privacy
</excerpt>
### Rank 4 of 251 — 0.03
<excerpt title="A Historical Feminist Political Ecology of Eastern Ontario's Forests, 1849">
# Ontario’s F orests, 1849 - 2013
## Ontario’s Forest Policy
By the 1960s, however, concerns were raised around the Province’s capacity to achieve
forest regeneration, with reforestation efforts in the north particularly necessary. There were various reasons for this predicament, such as seed-stock issues, the relative newness of professional/technical forest management and forest inventories still in progress. The outcome, however, was singular: poor forest conditions, impacting all users. As a result, the Crown Timber Act was again amended in 1962, this time transferring the full responsibility of replanting the forests to the Province, leaving harvesting as the sole responsibility of forest companies (Isherwood & Verheggen, 1997, p. 34).
With the activity of regeneration no longer a priority, the forest industry was able to invest heavily in harvesting and manufacturing technology, which allowed more trees to be cut and processed faster (Isherwood & Verheggen, 1997, p. 34). By the 1970s, local forest companies were relying on expensive, large-scale skidders, cutters and giant Caterpillars to harvest an ever-increasing number of trees (Statistics Canada, Timber Assets by Volume for Ontario, 1961-1997). These improvements in mechanisation were also found in modernised manufacturing plants, such as the Sawyer-Stoll Lumber Company in Tweed, where value-added products (e.g. finished pallets), were processed (see Figure 14). Here, over 2.5 million board feet of lumber could be processed in one year, resulting in the production of over 275,000 pallets (one log, around 16 metres in length, produced 50 feet of board timber) (Tweed News, May,
1978, ‘Modern equipment at Sawyer -Stoll Plant’).

# Ontario’s F orests, 1849 - 2013
## Ontario’s Forest Policy
These technological advancements, coupled with a forest policy that sustained production (Lawson et al., 2001, p. 292), resulted in forest companies almost doubling the area harvested in the province - from 138,000 hectares in 1960 up to 257,000 hectares in 1997 (Statistics Canada, Timber Assets by Volume for Ontario, 1961-1997). These efforts would increase Provincial 113
earnings from just over 3 million in 1961 to almost 40 million in 1997 (Statistics Canada, Value of Timber Stocks by Province, 1961-997). While growth in earnings and the area harvested were largely the result of i ntensive logging occurring in Ontario’s boreal forests, companies in the
eastern part of the province were also benefiting greatly from this technocentric age of forestry (Lawson, et al., 2001, p. 292).
> Figure 14. ‘Sawyer -Stoll’s Modern Pallet Manufacturing Plant’, Tweed News,  
> 1978. Photo: Cloyne and District Historical Society Archives.
In terms of forest renewal, however, it seems the public might not have been getting its
money’s worth as the area reforested in this period decreased from 450,000 hec tares in 1961 to 284,000 hectares in 1997 (Statistics Canada, Timber Assets by Area for Ontario, 1961-1997). While this suggests that the area planted was higher than the overall area harvested, it is important to note that actual reforestation levels have dropped almost 50% in the last 40 years. This was not because the forests were replanted. Indeed, forested areas today only account for 10-17% of what they were prior to the start of intensive harvesting in the mid-19 th century
(OMNR, 2014, ‘ Ontario’s p rotected areas summary statistics’ ). 114
</excerpt>
### Rank 5 of 251 — 0.03
<excerpt title="A Historical Feminist Political Ecology of Eastern Ontario's Forests, 1849">
# Ontario’s F orests, 1849 - 2013
## Ontario’s Forest Policy
These technological advancements, coupled with a forest policy that sustained production (Lawson et al., 2001, p. 292), resulted in forest companies almost doubling the area harvested in the province - from 138,000 hectares in 1960 up to 257,000 hectares in 1997 (Statistics Canada, Timber Assets by Volume for Ontario, 1961-1997). These efforts would increase Provincial 113
earnings from just over 3 million in 1961 to almost 40 million in 1997 (Statistics Canada, Value of Timber Stocks by Province, 1961-997). While growth in earnings and the area harvested were largely the result of i ntensive logging occurring in Ontario’s boreal forests, companies in the
eastern part of the province were also benefiting greatly from this technocentric age of forestry (Lawson, et al., 2001, p. 292).
> Figure 14. ‘Sawyer -Stoll’s Modern Pallet Manufacturing Plant’, Tweed News,  
> 1978. Photo: Cloyne and District Historical Society Archives.
In terms of forest renewal, however, it seems the public might not have been getting its
money’s worth as the area reforested in this period decreased from 450,000 hec tares in 1961 to 284,000 hectares in 1997 (Statistics Canada, Timber Assets by Area for Ontario, 1961-1997). While this suggests that the area planted was higher than the overall area harvested, it is important to note that actual reforestation levels have dropped almost 50% in the last 40 years. This was not because the forests were replanted. Indeed, forested areas today only account for 10-17% of what they were prior to the start of intensive harvesting in the mid-19 th century
(OMNR, 2014, ‘ Ontario’s p rotected areas summary statistics’ ). 114
</excerpt>

## Search 4 — query: "download csv timber assets area Quebec 1961 1962"
### Rank 1 of 118 — 0.26 (passed on)
<excerpt title="Timber assets (area) - Open Government Portal - Canada.ca">
# Timber assets (area) - Open Government Portal
## You are here:
1.   Canada.ca  
2.   Open Government  
3.   Search
Open Data

# Timber assets (area)
Timber assets (area)This table contains 80 series, with data for years 1961 - 2003 (not all combinations necessarily have data for all years), and was last released on 2010-09-28. This table contains data described by the following dimensions (Not all combinations are available): Geography (10 items: Canada; New Brunswick; Newfoundland and Labrador; Nova Scotia ...), Timber assets (area) (8 items: Timber assets (area); non reserved accessible opening stock; Timber assets (area); fire; Timber assets (area); mortality; Timber assets (area); harvest ...).2023-01-17 Statistics Canada infostats@statcan.gc.ca Economics and Industry Nature and Environment economic accounts environment environment accounts land oceans ecosystems and biodiversity table Dataset CSV https://www150.statcan.gc.ca/n1/tbl/csv/38100106-fra.zip Dataset CSV https://www150.statcan.gc.ca/n1/tbl/csv/38100106-eng.zip Dataset XML https://www150.statcan.gc.ca/n1/tbl/sdmx/38100106-SDMX.zip Supporting Document HTML https://www150.statcan.gc.ca/t1/tbl1/fr/tv.action?pid=3810010601 Supporting Document HTML https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=3810010601
This table contains 80 series, with data for years 1961 - 2003 (not all combinations necessarily have data for all years), and was last released on 2010-09-28. This table contains data described by the following dimensions (Not all combinations are available): Geography (10 items: Canada; New Brunswick; Newfoundland and Labrador; Nova Scotia ...), Timber assets (area) (8 items: Timber assets (area); non reserved accessible opening stock; Timber assets (area); fire; Timber assets (area); mortality; Timber assets (area); harvest ...).
*   **Publisher - Current Organization Name:** Statistics Canada   
*   **Licence:**Open Government Licence - Canada

# Timber assets (area)
## Data and Resources
Search
*   Dataset CSV French  Dataset  CSV
[Explore](javascript:void(0);)  
    *   More information  
    *   Go to resource
*   Dataset CSV English  Dataset  CSV
[Explore](javascript:void(0);)  
    *   More information  
    *   Go to resource
*   Dataset XML English  French  Dataset  XML
[Explore](javascript:void(0);)  
    *   More information  
    *   Go to resource
*   Supporting Document HTML French  Guide  HTML
[Explore](javascript:void(0);)  
    *   More information  
    *   Go to resource
*   Supporting Document HTML English  Guide  HTML
[Explore](javascript:void(0);)  
    *   More information  
    *   Go to resource
Similar records
*   Timber assets (volume)  
*   Value of timber stocks (methods I and II)  
*   Natural resource assets and produced assets  
*   Indicator Summary Data: Trends in Timber Harvesting in BC  
*   Value of selected natural resource reserves
Did you find this dataset useful?
</excerpt>
### Rank 2 of 118 — 0.22
<excerpt title="Timber assets (area)">
# Timber assets (area)
*   Skip to main content  
*   Skip to "About this site"

# Timber assets (area)
## Language selection
*   Français
/ Gouvernement du Canada

# Timber assets (area)
## Search and menus
*   Search and menus

# Timber assets (area)
## Search
Search Statistics Canada
Search

# Timber assets (area)
## Topics menu
*   Subjects  
*   Data  
*   Analysis  
*   Reference  
*   Geography  
*   Census  
*   Surveys and statistical programs  
*   About StatCan  
*   Canada.ca
1.   Home  
2.   Data

# Timber assets (area)
## Archived Content
Information identified as archived is provided for reference, research or recordkeeping purposes. It is not subject to the Government of Canada Web Standards and has not been altered or updated since it was archived. Pleasecontact us to request a format other than those available.
[Content is archived.](javascript:;)

# Archived - Timber assets (area) (x 1,000)1, 2
Frequency:Annual
Table: 38-10-0106-01 (formerly CANSIM 153-0029)
Release date: 2010-09-28
_Geography:_
Help
Save my customizations
Customize table
Geography :
Reference period
From:  To:
Apply
Add/Remove data

# Archived - Timber assets (area) (x 1,000)1, 2
## Add/Remove data help
Select your items to create your customized table.
Download options

# Archived - Timber assets (area) (x 1,000)1, 2
## Download options
### CSV Download as displayed{{ csvSize }}kB.


# Archived - Timber assets (area) (x 1,000)1, 2
## Download options
### CSV Download as displayed(excluding accompanying symbols).


# Archived - Timber assets (area) (x 1,000)1, 2
## Download options
### CSV Download as displayed(symbols separate).


# Archived - Timber assets (area) (x 1,000)1, 2
## Download options
### CSV Download selected data(for database loading).


# Archived - Timber assets (area) (x 1,000)1, 2
## Download options
### CSV Download cube metadata information, ~50kB.


# Archived - Timber assets (area) (x 1,000)1, 2
## Download options
### CSV Download entire table "Timber assets (area)".


# Archived - Timber assets (area) (x 1,000)1, 2
## Download options
### SDMX Download entire table.
Other data access options:Developers
Showing  records
Filter
Reset
No results found.
**Notes :**
**How to cite:** Statistics Canada. Table 38-10-0106-01 Timber assets (area) (x 1,000)
**DOI:**https://doi.org/10.25318/3810010601-eng

# Archived - Timber assets (area) (x 1,000)1, 2
## Related information
Source (Surveys and statistical programs)
*   Canadian System of Environmental-Economic Accounts - Natural Resource Asset Accounts
Subjects and keywords

# Archived - Timber assets (area) (x 1,000)1, 2
## Related information
### Subjects
*   Economic accounts  
    Environment accounts

    

*   Environment  
    Land, oceans, ecosystems and biodiversity
Date modified: 2026-11-18

# Archived - Timber assets (area) (x 1,000)1, 2
## About this site
### Statistics Canada
*   Contact StatCan  
*   Trust Centre

# Archived - Timber assets (area) (x 1,000)1, 2
## About this site
### Government of Canada
*   All contacts  
*   Departments and agencies  
*   About government
</excerpt>
### Rank 3 of 118 — 0.11
<excerpt title="Timber assets (area) - Open Government Portal - Canada.ca">
# Timber assets (area)
## Data and Resources
Search
*   Dataset CSV French  Dataset  CSV
[Explore](javascript:void(0);)  
    *   More information  
    *   Go to resource
*   Dataset CSV English  Dataset  CSV
[Explore](javascript:void(0);)  
    *   More information  
    *   Go to resource
*   Dataset XML English  French  Dataset  XML
[Explore](javascript:void(0);)  
    *   More information  
    *   Go to resource
*   Supporting Document HTML French  Guide  HTML
[Explore](javascript:void(0);)  
    *   More information  
    *   Go to resource
*   Supporting Document HTML English  Guide  HTML
[Explore](javascript:void(0);)  
    *   More information  
    *   Go to resource
Similar records
*   Timber assets (volume)  
*   Value of timber stocks (methods I and II)  
*   Natural resource assets and produced assets  
*   Indicator Summary Data: Trends in Timber Harvesting in BC  
*   Value of selected natural resource reserves
Did you find this dataset useful?

# Timber assets (area)
## Provide feedback on this dataset
Privacy Statement  
The collection and use of your personal information is authorized by the _Financial Administration Act_. Collection and use of your personal information for this site is in accordance with the federal _Privacy Act_. Your personal information is used to validate your use of GC datasets and for information on the development of the GC open data initiative, and may also be used to evaluate the effectiveness of the program in responding to client needs. In exceptional circumstances (e.g. network intrusion, or of individuals who make inappropriate remarks or threats, etc.), personal information may be disclosed without your consent pursuant to subsection 8(2) of the _Privacy Act_.
Any personal information that may be collected is described in the Standard Personal Information Banks entitled Public Communications, PSU 914, and Outreach Activities, PSU 938, which can be found in the Treasury Board of Canada Secretariat (TBS) publication: _InfoSource_.
Under the _Privacy Act_, you have the right of access to, and correction of, your personal information, if you have provided any. Note however, that to exercise either of these rights; you must make a request for access to your personal information. For more information about your right of access, please read about the Access to Information Program.
Any questions, comments, concerns or complaints you may have regarding this Statement, your privacy rights and the _Privacy Act_ may be directed to the TBS Access to Information and Privacy Coordinator by email at [atip.aiprp@tbs-sct.gc.ca](mailto:atip.aiprp@tbs-sct.gc.ca) or by calling 613-946-6260 or 1-866-312-1511. If you are not satisfied with TBS' response to your privacy concern, you may wish to contact the Office of the Privacy Commissioner by email at [info@priv.gc.ca](mailto:info@priv.gc.ca) or by telephone at 1-800-282-1376. You have the right to complain to the Office of the Privacy Commissioner about TBS' handling of your personal information.
Name
Email address
I am a
Reason for feedback
Feedback
(required)
Have your say
*   Rate this dataset  
*   Provide feedback
Additional Information
</excerpt>
### Rank 4 of 118 — 0.10
<excerpt title="Timber assets (area) - Open Government Portal - Canada.ca">
# Timber assets (area)
## About this site
### Government of Canada
*   All contacts  
*   Departments and agencies  
*   About government

# Timber assets (area)
## About this site
### Government of Canada
#### Themes and topics
*   Jobs  
*   Immigration and citizenship  
*   Travel and tourism  
*   Business  
*   Benefits  
*   Health  
*   Taxes  
*   Environment and natural resources  
*   National security and defence  
*   Culture, history and sport  
*   Policing, justice and emergencies  
*   Transport and infrastructure  
*   Canada and the world  
*   Money and finances  
*   Science and innovation  
*   Indigenous Peoples  
*   Veterans and military  
*   Youth  
*   Manage life events

# Timber assets (area)
## About this site
### Government of Canada Corporate
*   Social media  
*   Mobile applications  
*   About Canada.ca  
*   Terms and conditions  
*   Privacy
**Downloads**
Requesting Download...
</excerpt>
### Rank 5 of 118 — 0.06
<excerpt title="Downloads">
## Harvest
**5.1. Net merchantable volume of roundwood harvested by ownership, category and species group**
| Resource Type | Formats |  
| --- | --- |  
| Data | XLSXCSV |  
| Data Dictionary | XLSX |  
| Data Comments | XLS |
**5.2. Area harvested by ownership, management and harvesting method**
| Resource Type | Formats |  
| --- | --- |  
| Data | XLSXCSV |  
| Data Dictionary | XLSX |  
| Data Comments | XLS |

## Regeneration
**6.1. Area of site preparation by ownership and treatment**
| Resource Type | Formats |  
| --- | --- |  
| Data | XLSXCSV |  
| Data Dictionary | XLSX |  
| Data Comments | XLS |
**6.2. Area of scarification by ownership**
| Resource Type | Formats |  
| --- | --- |  
| Data | XLSXCSV |  
| Data Dictionary | XLSX |  
| Data Comments | XLS |
**6.3. Area of direct seeding by ownership and application method**
| Resource Type | Formats |  
| --- | --- |  
| Data | XLSXCSV |  
| Data Dictionary | XLSX |  
| Data Comments | XLS |
**6.4. Number of seedlings planted by ownership and species group**
| Resource Type | Formats |  
| --- | --- |  
| Data | XLSXCSV |  
| Data Dictionary | XLSX |  
| Data Comments | XLS |
**6.5. Area planted by ownership and species group**
| Resource Type | Formats |  
| --- | --- |  
| Data | XLSXCSV |  
| Data Dictionary | XLSX |  
| Data Comments | XLS |
**6.6. Area of stand tending by ownership, treatment and method**
| Resource Type | Formats |  
| --- | --- |  
| Data | XLSXCSV |  
| Data Dictionary | XLSX |  
| Data Comments | XLS |

## Revenues
**7.Statement of revenues from the sale of timber from provincial Crown land**
| Resource Type | Formats |  
| --- | --- |  
| Data | XLSXCSV |  
| Data Dictionary | XLSX |  
| Data Comments | XLS |
</excerpt>

## Search 5 — query: "https://www150.statcan.gc.ca/n1/tbl/csv/38100106-eng.zip"
### Rank 1 of 24 — 0.25 (passed on)
<excerpt title="Timber assets (area) - Open Government Portal - Canada.ca">
# Timber assets (area) - Open Government Portal
## You are here:
1.   Canada.ca  
2.   Open Government  
3.   Search
Open Data

# Timber assets (area)
Timber assets (area)This table contains 80 series, with data for years 1961 - 2003 (not all combinations necessarily have data for all years), and was last released on 2010-09-28. This table contains data described by the following dimensions (Not all combinations are available): Geography (10 items: Canada; New Brunswick; Newfoundland and Labrador; Nova Scotia ...), Timber assets (area) (8 items: Timber assets (area); non reserved accessible opening stock; Timber assets (area); fire; Timber assets (area); mortality; Timber assets (area); harvest ...).2023-01-17 Statistics Canada infostats@statcan.gc.ca Economics and Industry Nature and Environment economic accounts environment environment accounts land oceans ecosystems and biodiversity table Dataset CSV https://www150.statcan.gc.ca/n1/tbl/csv/38100106-fra.zip Dataset CSV https://www150.statcan.gc.ca/n1/tbl/csv/38100106-eng.zip Dataset XML https://www150.statcan.gc.ca/n1/tbl/sdmx/38100106-SDMX.zip Supporting Document HTML https://www150.statcan.gc.ca/t1/tbl1/fr/tv.action?pid=3810010601 Supporting Document HTML https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=3810010601
This table contains 80 series, with data for years 1961 - 2003 (not all combinations necessarily have data for all years), and was last released on 2010-09-28. This table contains data described by the following dimensions (Not all combinations are available): Geography (10 items: Canada; New Brunswick; Newfoundland and Labrador; Nova Scotia ...), Timber assets (area) (8 items: Timber assets (area); non reserved accessible opening stock; Timber assets (area); fire; Timber assets (area); mortality; Timber assets (area); harvest ...).
*   **Publisher - Current Organization Name:** Statistics Canada   
*   **Licence:**Open Government Licence - Canada

# Timber assets (area)
## Data and Resources
Search
*   Dataset CSV French  Dataset  CSV
[Explore](javascript:void(0);)  
    *   More information  
    *   Go to resource
*   Dataset CSV English  Dataset  CSV
[Explore](javascript:void(0);)  
    *   More information  
    *   Go to resource
*   Dataset XML English  French  Dataset  XML
[Explore](javascript:void(0);)  
    *   More information  
    *   Go to resource
*   Supporting Document HTML French  Guide  HTML
[Explore](javascript:void(0);)  
    *   More information  
    *   Go to resource
*   Supporting Document HTML English  Guide  HTML
[Explore](javascript:void(0);)  
    *   More information  
    *   Go to resource
Similar records
*   Timber assets (volume)  
*   Value of timber stocks (methods I and II)  
*   Natural resource assets and produced assets  
*   Indicator Summary Data: Trends in Timber Harvesting in BC  
*   Value of selected natural resource reserves
Did you find this dataset useful?
</excerpt>
### Rank 2 of 24 — 0.18
<excerpt title="Actifs en bois (superficie) - Portail du gouvernement ouvert">
# Actifs en bois (superficie) - Portail du gouvernement ouvert
## Vous êtes ici :
1.   Canada.ca  
2.   Gouvernement ouvert  
3.   Rechercher
Données ouvertes

# Actifs en bois (superficie)
Actifs en bois (superficie)Ce tableau contient 80 séries, avec des données pour les années 1961 - 2003 (il n'y a pas nécessairement de données pour toutes les années pour l'ensemble des combinaisons), et sa dernière date de diffusion remonte au 2010-09-28. Ce tableau contient des données telles que décrites par les dimensions suivantes (les combinaisons ne sont pas toutes disponibles): Géographie (10 éléments: Canada; Nouveau-Brunswick; Terre-Neuve-et-Labrador; Nouvelle-Écosse ...), Actifs en bois (superficie) (8 éléments: Actifs en bois (superficie); stock d'ouverture non réservé et accessible; Actifs en bois (superficie); incendies; Actifs en bois (superficie); mortalité; Actifs en bois (superficie); récolte ...).2023-01-17 Statistique Canada infostats@statcan.gc.ca Économie et industrie Nature et environnement comptes de l'environnement comptes économiques environnement tableau terres océans écosystèmes et biodiversité Ensembles de données CSV https://www150.statcan.gc.ca/n1/tbl/csv/38100106-fra.zip Ensembles de données CSV https://www150.statcan.gc.ca/n1/tbl/csv/38100106-eng.zip Ensembles de données XML https://www150.statcan.gc.ca/n1/tbl/sdmx/38100106-SDMX.zip Document connexe HTML https://www150.statcan.gc.ca/t1/tbl1/fr/tv.action?pid=3810010601 Document connexe HTML https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=3810010601

# Actifs en bois (superficie)
Ce tableau contient 80 séries, avec des données pour les années 1961 - 2003 (il n'y a pas nécessairement de données pour toutes les années pour l'ensemble des combinaisons), et sa dernière date de diffusion remonte au 2010-09-28. Ce tableau contient des données telles que décrites par les dimensions suivantes (les combinaisons ne sont pas toutes disponibles): Géographie (10 éléments: Canada; Nouveau-Brunswick; Terre-Neuve-et-Labrador; Nouvelle-Écosse ...), Actifs en bois (superficie) (8 éléments: Actifs en bois (superficie); stock d'ouverture non réservé et accessible; Actifs en bois (superficie); incendies; Actifs en bois (superficie); mortalité; Actifs en bois (superficie); récolte ...).
*   **Éditeur - Nom actuel de l’organisation :** Statistique Canada   
*   **Licence :**Licence du gouvernement ouvert - Canada
</excerpt>
### Rank 3 of 24 — 0.12
<excerpt title="Timber assets (area) - Open Government Portal - Canada.ca">
# Timber assets (area)
## Provide feedback on this dataset
Privacy Statement  
The collection and use of your personal information is authorized by the _Financial Administration Act_. Collection and use of your personal information for this site is in accordance with the federal _Privacy Act_. Your personal information is used to validate your use of GC datasets and for information on the development of the GC open data initiative, and may also be used to evaluate the effectiveness of the program in responding to client needs. In exceptional circumstances (e.g. network intrusion, or of individuals who make inappropriate remarks or threats, etc.), personal information may be disclosed without your consent pursuant to subsection 8(2) of the _Privacy Act_.
Any personal information that may be collected is described in the Standard Personal Information Banks entitled Public Communications, PSU 914, and Outreach Activities, PSU 938, which can be found in the Treasury Board of Canada Secretariat (TBS) publication: _InfoSource_.
Under the _Privacy Act_, you have the right of access to, and correction of, your personal information, if you have provided any. Note however, that to exercise either of these rights; you must make a request for access to your personal information. For more information about your right of access, please read about the Access to Information Program.
Any questions, comments, concerns or complaints you may have regarding this Statement, your privacy rights and the _Privacy Act_ may be directed to the TBS Access to Information and Privacy Coordinator by email at [atip.aiprp@tbs-sct.gc.ca](mailto:atip.aiprp@tbs-sct.gc.ca) or by calling 613-946-6260 or 1-866-312-1511. If you are not satisfied with TBS' response to your privacy concern, you may wish to contact the Office of the Privacy Commissioner by email at [info@priv.gc.ca](mailto:info@priv.gc.ca) or by telephone at 1-800-282-1376. You have the right to complain to the Office of the Privacy Commissioner about TBS' handling of your personal information.
Name
Email address
I am a
Reason for feedback
Feedback
(required)
Have your say
*   Rate this dataset  
*   Provide feedback
Additional Information

# Timber assets (area)
## Provide feedback on this dataset
*   **Keywords:**  
    *   economic accounts  
    *   environment  
    *   environment accounts  
    *   land oceans ecosystems and biodiversity  
    *   table

*   **Subject:**  
    *    Economics and Industry  
    *    Nature and Environment

*   **Series Title:** Table   
*   **Series Issue ID:** Table 38100106; Formerly CANSIM Table 153-0029   
*   **Maintenance and Update Frequency:** Annually   
*   **Date Published:** 2010-09-28   
*   **Openness Rating**:
About this Record
*   **Record Released:** 2018-06-27   
*   **Record Modified:** 2023-01-17   
*   **Record ID:** 3dea01f1-0161-412a-93b6-76b4bfab17d6   
*   **Metadata:**  
    *   Link to JSON format  
    *   DCAT (JSON-LD)  
    *   DCAT (XML)

*   Atom Feed

# Timber assets (area)
## About this site
### Government of Canada
*   All contacts  
*   Departments and agencies  
*   About government
</excerpt>
### Rank 4 of 24 — 0.11
<excerpt title="Actifs en bois (superficie) - Portail du gouvernement ouvert">
# Actifs en bois (superficie)
## Indiquez vos commentaires sur ce jeu de données
Les questions, commentaires, préoccupations et plaintes concernant la présente déclaration, vos droits en matière de protection des renseignements personnels et la _Loi sur la protection des renseignements personnels_ peuvent être adressés au coordonnateur de l'accès à l'information et de la protection des renseignements personnels du SCT par courriel, à [atip.aiprp@tbs-sct.gc.ca](mailto:atip.aiprp@tbs-sct.gc.ca) ou par téléphone, au 613-946-6260 ou au 1-866-312-1511. Si vous n'êtes pas satisfait de la réponse du SCT, vous pouvez vous adresser au Commissariat à la protection de la vie privée du Canada par courriel, à [info@priv.gc.ca](mailto:info@priv.gc.ca) ou par téléphone, au 1-800-282-1376. Vous avez le droit de déposer une plainte au Commissariat à la protection de la vie privée relativement au traitement de vos renseignements personnels par le SCT.
Nom
Adresse de courriel
Je suis
Motifs de la rétroaction
Commentaires
(requis)
À vous la parole
*   Évaluez ce jeu de données  
*   Fournir un retour d’information
Informations complémentaires
*   **Mots clés :**  
    *   comptes de l'environnement  
    *   comptes économiques  
    *   environnement  
    *   tableau  
    *   terres océans écosystèmes et biodiversité

*   **Sujet :**  
    *    Économie et industrie  
    *    Nature et environnement

*   **Nom de la série :** Tableau   
*   **Numéro de publication de la série :** Tableau 38100106; Anciennement Table CANSIM 153-0029   
*   **Fréquence d'entretien et de mise à jour :** Annuel   
*   **Date de publication :** 2010-09-28   
*   **Cote de degrée d’ouverture des données** :
Au sujet de ce dossier

# Actifs en bois (superficie)
## Indiquez vos commentaires sur ce jeu de données
*   **Dossier publié :** 2018-06-27   
*   **Dossier modifié :** 2023-01-17   
*   **Identificateur du dossier :** 3dea01f1-0161-412a-93b6-76b4bfab17d6   
*   **Métadonnées :**  
    *   Lien au format JSON  
    *   DCAT (JSON-LD)  
    *   DCAT (XML)

*   Fil de nouvelles Atom

# Actifs en bois (superficie)
## À propos de ce site
### Gouvernement du Canada
*   Toutes les coordonnées  
*   Ministères et organismes  
*   À propos du gouvernement

# Actifs en bois (superficie)
## À propos de ce site
### Gouvernement du Canada
#### Thèmes et sujets
*   Emplois  
*   Immigration et citoyenneté  
*   Voyage et tourisme  
*   Entreprises  
*   Prestations  
*   Santé  
*   Impôts  
*   Environnement et ressources naturelles  
*   Sécurité nationale et défense  
*   Culture, histoire et sport  
*   Services de police, justice et urgences  
*   Transport et infrastructure  
*   Le Canada et le monde  
*   Argent et finances  
*   Science et innovation  
*   Autochtones  
*   Vétérans et militaires  
*   Jeunesse  
*   Gérer les événements de la vie
</excerpt>
### Rank 5 of 24 — 0.09
<excerpt title="Actifs en bois (superficie) - Portail du gouvernement ouvert">
# Actifs en bois (superficie)
Ce tableau contient 80 séries, avec des données pour les années 1961 - 2003 (il n'y a pas nécessairement de données pour toutes les années pour l'ensemble des combinaisons), et sa dernière date de diffusion remonte au 2010-09-28. Ce tableau contient des données telles que décrites par les dimensions suivantes (les combinaisons ne sont pas toutes disponibles): Géographie (10 éléments: Canada; Nouveau-Brunswick; Terre-Neuve-et-Labrador; Nouvelle-Écosse ...), Actifs en bois (superficie) (8 éléments: Actifs en bois (superficie); stock d'ouverture non réservé et accessible; Actifs en bois (superficie); incendies; Actifs en bois (superficie); mortalité; Actifs en bois (superficie); récolte ...).
*   **Éditeur - Nom actuel de l’organisation :** Statistique Canada   
*   **Licence :**Licence du gouvernement ouvert - Canada

# Actifs en bois (superficie)
## Données et ressources
Rechercher
*   Ensembles de données CSV français  Jeu de données  CSV
[Explorer](javascript:void(0);)  
    *   Plus d'information  
    *   Aller à la ressource
*   Ensembles de données CSV anglais  Jeu de données  CSV
[Explorer](javascript:void(0);)  
    *   Plus d'information  
    *   Aller à la ressource
*   Ensembles de données XML anglais  français  Jeu de données  XML
[Explorer](javascript:void(0);)  
    *   Plus d'information  
    *   Aller à la ressource
*   Document connexe HTML français  Guide  HTML
[Explorer](javascript:void(0);)  
    *   Plus d'information  
    *   Aller à la ressource
*   Document connexe HTML anglais  Guide  HTML
[Explorer](javascript:void(0);)  
    *   Plus d'information  
    *   Aller à la ressource
Dossiers similaires
*   Actifs en bois (volume)  
*   Valeur des stocks en bois (méthodes I et II)  
*   Compte de l’étendue de la couverture terrestre protégée et conservée, par sous-aire …  
*   Compte de l’étendue de la couverture terrestre protégée et conservée, par écoprovince …  
*   Couverture terrestre par classe, Canada, sous-aire de drainage, aire de drainage principale …
Avez-vous trouvé ce jeu de données utile?
</excerpt>

## Search 6 — query: "https://www150.statcan.gc.ca/n1/tbl/csv/38100106-eng.zip"
### Rank 1 of 24 — 0.25 (passed on)
<excerpt title="untitled">
# Timber assets (area) - Open Government Portal
## You are here:
1.   Canada.ca  
2.   Open Government  
3.   Search
Open Data

# Timber assets (area)
Timber assets (area)This table contains 80 series, with data for years 1961 - 2003 (not all combinations necessarily have data for all years), and was last released on 2010-09-28. This table contains data described by the following dimensions (Not all combinations are available): Geography (10 items: Canada; New Brunswick; Newfoundland and Labrador; Nova Scotia ...), Timber assets (area) (8 items: Timber assets (area); non reserved accessible opening stock; Timber assets (area); fire; Timber assets (area); mortality; Timber assets (area); harvest ...).2023-01-17 Statistics Canada infostats@statcan.gc.ca Economics and Industry Nature and Environment economic accounts environment environment accounts land oceans ecosystems and biodiversity table Dataset CSV https://www150.statcan.gc.ca/n1/tbl/csv/38100106-fra.zip Dataset CSV https://www150.statcan.gc.ca/n1/tbl/csv/38100106-eng.zip Dataset XML https://www150.statcan.gc.ca/n1/tbl/sdmx/38100106-SDMX.zip Supporting Document HTML https://www150.statcan.gc.ca/t1/tbl1/fr/tv.action?pid=3810010601 Supporting Document HTML https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=3810010601
This table contains 80 series, with data for years 1961 - 2003 (not all combinations necessarily have data for all years), and was last released on 2010-09-28. This table contains data described by the following dimensions (Not all combinations are available): Geography (10 items: Canada; New Brunswick; Newfoundland and Labrador; Nova Scotia ...), Timber assets (area) (8 items: Timber assets (area); non reserved accessible opening stock; Timber assets (area); fire; Timber assets (area); mortality; Timber assets (area); harvest ...).
*   **Publisher - Current Organization Name:** Statistics Canada   
*   **Licence:**Open Government Licence - Canada

# Timber assets (area)
## Data and Resources
Search
*   Dataset CSV French  Dataset  CSV
[Explore](javascript:void(0);)  
    *   More information  
    *   Go to resource
*   Dataset CSV English  Dataset  CSV
[Explore](javascript:void(0);)  
    *   More information  
    *   Go to resource
*   Dataset XML English  French  Dataset  XML
[Explore](javascript:void(0);)  
    *   More information  
    *   Go to resource
*   Supporting Document HTML French  Guide  HTML
[Explore](javascript:void(0);)  
    *   More information  
    *   Go to resource
*   Supporting Document HTML English  Guide  HTML
[Explore](javascript:void(0);)  
    *   More information  
    *   Go to resource
Similar records
*   Timber assets (volume)  
*   Value of timber stocks (methods I and II)  
*   Natural resource assets and produced assets  
*   Indicator Summary Data: Trends in Timber Harvesting in BC  
*   Value of selected natural resource reserves
Did you find this dataset useful?
</excerpt>
### Rank 2 of 24 — 0.18
<excerpt title="untitled">

</excerpt>
### Rank 3 of 24 — 0.12
<excerpt title="untitled">

</excerpt>
### Rank 4 of 24 — 0.11
<excerpt title="untitled">

</excerpt>
### Rank 5 of 24 — 0.09
<excerpt title="untitled">

</excerpt>

## Search 7 — query: "38100106-eng.csv Quebec"
### Rank 1 of 38 — 0.03 (passed on)
<excerpt title="Pre-packaged CSV files - CGN Canada/Province/Territory/Undersea">
# Canadian Geographical Names - CGN - Pre-packaged CSV files - CGN Canada/Province/Territory/Undersea - Open Government Portal
## Menu
    *   National security  
    *   Canadian Armed Forces  
    *   Jobs in national security and defence  
    *   Services and benefits  
    *   Cyber security  
    *   Defence equipment purchases and upgrades  
    *   Protecting the Canadian border  
    *   Transportation security

    *   Most requested  
        *   Jobs in the Forces  
        *   Canadian military support to Ukraine  
        *   Military ranks  
        *   Defence equipment  
        *   Canada's Defence policy  
        *   Join the Cadet Program

*   Culture, history and sport  
    *   Culture, history and sport: home

    *   Funding - Culture, history and sport  
    *   Events, celebrations and commemorations  
    *   Cultural landmarks and attractions  
    *   Canadian identity and society  
    *   Sport  
    *   History and heritage  
    *   Arts and media  
    *   Youth leadership and cultural program  
    *   Cultural trade and investment

    *   Most requested  
        *   Visit the Canadian Virtual War Memorial  
        *   Anthems and symbols of Canada  
        *   Find a CRTC decision  
        *   Research your family history  
        *   Search census records  
        *   Major events in Canada's Capital Region

*   Policing, justice and emergencies  
    *   Policing, justice and emergencies: home

    *   Policing  
    *   Justice  
    *   Emergencies  
    *   Corrections  
    *   Parole, record suspension, expungement and clemency  
    *   Victims of crime  
    *   Crime and justice statistics

    *   Most requested  
        *   Wildfire Response  
        *   Apply/Renew a firearms licence  
        *   Get a criminal records check  
        *   Apply for a criminal record suspension  
        *   What to do during an emergency  
        *   Know the law on impaired driving  
        *   Help solve a crime

*   Transport and infrastructure  
    *   Transport and infrastructure: home

    *   Zero-emission vehicles  
    *   Aviation  
    *   Marine transportation  
    *   Road transportation  
    *   Rail transportation  
    *   Dangerous goods  
    *   Infrastructure
</excerpt>
### Rank 2 of 38 — 0.03
<excerpt title="Pre-packaged CSV files - CGN Canada/Province/Territory/Undersea">
# Canadian Geographical Names - CGN - Pre-packaged CSV files - CGN Canada/Province/Territory/Undersea - Open Government Portal
*   Skip to main content  
*   Skip to "About government"  
*   Switch to basic HTML version

# Canadian Geographical Names - CGN - Pre-packaged CSV files - CGN Canada/Province/Territory/Undersea - Open Government Portal
## Language selection
*   Français fr
/ Gouvernement du Canada

# Canadian Geographical Names - CGN - Pre-packaged CSV files - CGN Canada/Province/Territory/Undersea - Open Government Portal
## Search
Search Canada.ca
Search

# Canadian Geographical Names - CGN - Pre-packaged CSV files - CGN Canada/Province/Territory/Undersea - Open Government Portal
## Menu
Main Menu
*   Jobs and the workplace  
    *   Jobs: home

    *   Job Bank  
    *   Government of Canada jobs  
    *   Youth and student employment  
    *   Jobs in national security and defence  
    *   Moving within Canada to work  
    *   Funding for jobs and training  
    *   Training  
    *   Hiring and managing employees  
    *   Starting a business  
    *   Employment Insurance benefits and leave  
    *   Workplace standards  
    *   Pensions and retirement

    *   Most requested  
        *   Work in Canada - work permits  
        *   Immigrate as a skilled worker  
        *   Hire a temporary foreign worker  
        *   Federal Skilled Worker Program  
        *   View your records of employment  
        *   Submit a record of employment - employers  
        *   Federal Student Work Experience Program (FSWEP)  
        *   Apply for a Social Insurance Number (SIN)

*   Immigration and citizenship  
    *   Immigration and citizenship: home

    *   IRCC applications  
    *   Visit Canada  
    *   Live in Canada permanently  
    *   Work in Canada temporarily  
    *   Study in Canada  
    *   Refugees and asylum  
    *   International Experience Canada (IEC)  
    *   Passports and other travel documents  
    *   Citizenship  
    *   Permanent resident (PR) cards and status  
    *   Settling in Canada as a newcomer  
    *   International adoption  
    *   Explore immigration programs  
    *   Immigration fraud and scams  
    *   Inadmissibility, enforcement and appeals

    *   Most requested  
        *   Sign in to your IRCC account  
        *   Check your application status  
        *   Current processing times  
        *   Find an application form  
        *   Portals for representatives and partners

*   Travel and tourism  
    *   Travel and tourism: home

    *   Travel advice and advisories  
    *   Travel outside Canada  
    *   Air travel  
    *   Canadian passports and travel documents  
    *   Stay connected  
    *   Assistance outside Canada  
    *   Visit Canada  
    *   Return or travel to Canada  
    *   Canadian attractions, events and experiences
</excerpt>
### Rank 3 of 38 — 0.03
<excerpt title="Pre-packaged CSV files - CGN Canada/Province/Territory/Undersea">
# Canadian Geographical Names - CGN - Pre-packaged CSV files - CGN Canada/Province/Territory/Undersea - Open Government Portal
## Menu
Main Menu
*   Jobs and the workplace  
    *   Jobs: home

    *   Job Bank  
    *   Government of Canada jobs  
    *   Youth and student employment  
    *   Jobs in national security and defence  
    *   Moving within Canada to work  
    *   Funding for jobs and training  
    *   Training  
    *   Hiring and managing employees  
    *   Starting a business  
    *   Employment Insurance benefits and leave  
    *   Workplace standards  
    *   Pensions and retirement

    *   Most requested  
        *   Work in Canada - work permits  
        *   Immigrate as a skilled worker  
        *   Hire a temporary foreign worker  
        *   Federal Skilled Worker Program  
        *   View your records of employment  
        *   Submit a record of employment - employers  
        *   Federal Student Work Experience Program (FSWEP)  
        *   Apply for a Social Insurance Number (SIN)

*   Immigration and citizenship  
    *   Immigration and citizenship: home

    *   IRCC applications  
    *   Visit Canada  
    *   Live in Canada permanently  
    *   Work in Canada temporarily  
    *   Study in Canada  
    *   Refugees and asylum  
    *   International Experience Canada (IEC)  
    *   Passports and other travel documents  
    *   Citizenship  
    *   Permanent resident (PR) cards and status  
    *   Settling in Canada as a newcomer  
    *   International adoption  
    *   Explore immigration programs  
    *   Immigration fraud and scams  
    *   Inadmissibility, enforcement and appeals

    *   Most requested  
        *   Sign in to your IRCC account  
        *   Check your application status  
        *   Current processing times  
        *   Find an application form  
        *   Portals for representatives and partners

*   Travel and tourism  
    *   Travel and tourism: home

    *   Travel advice and advisories  
    *   Travel outside Canada  
    *   Air travel  
    *   Canadian passports and travel documents  
    *   Stay connected  
    *   Assistance outside Canada  
    *   Visit Canada  
    *   Return or travel to Canada  
    *   Canadian attractions, events and experiences
</excerpt>
### Rank 4 of 38 — 0.03
<excerpt title="Full Table Download (CSV) User Guide">
## General Information
*   Download files are unilingual; there is a separate English and French version for each table.  
*   Previously used CANSIM table numbers have been replaced by numeric Product Identification codes, called PIDs. Each table has a unique PID.  
*   English downloads are in CSV format and use commas as the separator. French downloads are also in CSV format but use semi-colons as the separator. This is by design to accommodate the decimal display standard in French, which uses a comma (,) instead of the period (.) used in English.  
*   Data is 'bundled' in a .zip format containing 2 .csv files; a data file containing both data and textual 'stub' information, and a corresponding metadata file. Users receive both on download.  
*   The .zip filename has the format 'PID-eng.zip' in English and 'PID-fra.zip' in French. The filenames for the data and metadata files have the structures "PID.csv and PID_Metadata.csv', in both English and French.  
*   Some information (i.e. dimension names, member names) appears in both the data and metadata file. This redundancy is by design. It accommodates the advanced user who requires the ability to sort and filter on the data, and it also allows the novice user to understand the information being presented through the presence of basic descriptions.  
*   For 2021 Census cubes (98-XXXX-XX) there have been changes introduced in both the metadata and data files, which makes the record layouts for both files different than non-Census cubes.These differences have been described in this document.

## Data File(non-Census cubes)
*   A Statistics Canada data table contains a minimum of 1 dimension (variable) and a maximum of 10. A standard record layout for the .csv data output file includes a minimum of 14 fields, and always includes a geography dimension. These fields are listed below and described in the record layout section of this document  
    *   REF_DATE  
    *   GEO  
    *   DGUID  
    *   UOM  
    *   UOM_ID  
    *   SCALAR_FACTOR  
    *   SCALAR_ID  
    *   VECTOR  
    *   COORDINATE  
    *   VALUE  
    *   STATUS  
    *   SYMBOL  
    *   TERMINATED  
    *   DECIMALS

*   The number of fields in the data output file varies based on the complexity of the table. For example, a table with 6 dimensions contains at least 4 more fields in the output file as compared to a table with only 2 dimensions.  
*   The sort order within the data files has been modified from previous .csv outputs. Data will now be sorted by ref_date in ascending order.  
*   For data points requiring decimal representation, the value in the data file has the decimal applied. However, by design, an additional separate, specific decimal precision field is also included in the file in order to explicitly identify the decimal precision for each data point.  
*   The scalar factor description and scalar identification (ID) fields are paired together and are systematically included in the data output file.  
*   The unit of measure description and unit of measure identification (ID) fields are paired together and are systematically included in the data output file.  
*   Where symbols are used to replace data on the web (i.e. F and X), these same symbols appear in designated status fields in the downloadable file. When such symbols appear in the status field, the corresponding value field will remain blank.
</excerpt>
### Rank 5 of 38 — 0.02
<excerpt title="Pre-packaged CSV files - CGN Canada/Province/Territory/Undersea">
# Canadian Geographical Names - CGN - Pre-packaged CSV files - CGN Canada/Province/Territory/Undersea - Open Government Portal
## Menu
    *   Most requested  
        *   Drone safety  
        *   What not to bring on a plane  
        *   Register your vessel  
        *   Child car seat safety  
        *   Transporting dangerous goods - Regulations  
        *   _Canadian Aviation Regulations_

*   Canada and the world  
    *   Canada and the world: home

    *   International offices and emergency contacts  
    *   Study, work and travel worldwide  
    *   Information by country and territory  
    *   Stories  
    *   Canada's foreign policy and international relations  
    *   Global issues and international assistance  
    *   Canadian funding for international initiatives  
    *   International trade and investment

    *   Most requested  
        *   International education and scholarships  
        *   Contact an embassy or consulate  
        *   Sanctions  
        *   Authenticate a document  
        *   International treaties signed by Canada  
        *   Project Browser  
        *   Contact a foreign representative in Canada  
        *   Canada-United States trade: federal supports

*   Money and finances  
    *   Money and finances Finance: home

    *   Managing your money  
    *   Consumer affairs  
    *   Debt and borrowing  
    *   Education funding  
    *   Pensions and retirement  
    *   Financial tools and calculators  
    *   Savings and investments  
    *   Taxes  
    *   Financial literacy programs  
    *   Business financing and support  
    *   Protection from frauds and scams  
    *   Financial and money services regulation  
    *   Insolvency

    *   Most requested  
        *   Canada's response to U.S. tariffs  
        *   Housing  
        *   Student loans  
        *   Credit report and scores  
        *   Mortgages  
        *   Make a budget  
        *   Set up or change direct deposit  
        *   Find a bankruptcy or insolvency record

*   Science and innovation  
    *   Science and innovation: home

# Canadian Geographical Names - CGN - Pre-packaged CSV files - CGN Canada/Province/Territory/Undersea - Open Government Portal
## Menu
    *   Research funding and awards  
    *   R&D and innovation  
    *   Science subjects  
    *   Health emergency readiness  
    *   Research institutes and facilities  
    *   Open data, statistics and archives  
    *   Science education resources  
    *   Intellectual property and copyright  
    *   Directory of scientists and research professionals  
    *   Our environment  
    *   Federal Open Science Repository of Canada

    *   Most requested  
        *   Grants for technological innovation (IRAP)  
        *   National building codes  
        *   Federal Science Libraries Network  
        *   Check sunrise and sunset times  
        *   Official times across Canada  
        *   Live view of northern lights cam

*   Manage life events  
    *   Manage life events: home

    *   Welcoming a child  
    *   Learn and plan for your retirement  
    *   What to do when someone dies

    *   Most requested  
        *   Sign in to a Government of Canada account  
        *   CPP payment amounts  
        *   Benefits payments dates  
        *   Canada child benefit  
        *   Canadian Retirement Income Calculator  
        *   Prepare tax returns for someone who died  
        *   Get a birth certificate  
        *   Apply for a SIN

# Canadian Geographical Names - CGN - Pre-packaged CSV files - CGN Canada/Province/Territory/Undersea - Open Government Portal
## You are here:
1.   Canada.ca  
2.   Open Government  
3.   Search  
4.   Canadian Geographical Names - CGN
Open Data
</excerpt>

## Search 8 — query: "https://www150.statcan.gc.ca/n1/tbl/csv/38100106-eng.zip"
### Rank 1 of 24 — 0.25 (passed on)
<excerpt title="untitled">
# Timber assets (area) - Open Government Portal
## You are here:
1.   Canada.ca  
2.   Open Government  
3.   Search
Open Data

# Timber assets (area)
Timber assets (area)This table contains 80 series, with data for years 1961 - 2003 (not all combinations necessarily have data for all years), and was last released on 2010-09-28. This table contains data described by the following dimensions (Not all combinations are available): Geography (10 items: Canada; New Brunswick; Newfoundland and Labrador; Nova Scotia ...), Timber assets (area) (8 items: Timber assets (area); non reserved accessible opening stock; Timber assets (area); fire; Timber assets (area); mortality; Timber assets (area); harvest ...).2023-01-17 Statistics Canada infostats@statcan.gc.ca Economics and Industry Nature and Environment economic accounts environment environment accounts land oceans ecosystems and biodiversity table Dataset CSV https://www150.statcan.gc.ca/n1/tbl/csv/38100106-fra.zip Dataset CSV https://www150.statcan.gc.ca/n1/tbl/csv/38100106-eng.zip Dataset XML https://www150.statcan.gc.ca/n1/tbl/sdmx/38100106-SDMX.zip Supporting Document HTML https://www150.statcan.gc.ca/t1/tbl1/fr/tv.action?pid=3810010601 Supporting Document HTML https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=3810010601
This table contains 80 series, with data for years 1961 - 2003 (not all combinations necessarily have data for all years), and was last released on 2010-09-28. This table contains data described by the following dimensions (Not all combinations are available): Geography (10 items: Canada; New Brunswick; Newfoundland and Labrador; Nova Scotia ...), Timber assets (area) (8 items: Timber assets (area); non reserved accessible opening stock; Timber assets (area); fire; Timber assets (area); mortality; Timber assets (area); harvest ...).
*   **Publisher - Current Organization Name:** Statistics Canada   
*   **Licence:**Open Government Licence - Canada

# Timber assets (area)
## Data and Resources
Search
*   Dataset CSV French  Dataset  CSV
[Explore](javascript:void(0);)  
    *   More information  
    *   Go to resource
*   Dataset CSV English  Dataset  CSV
[Explore](javascript:void(0);)  
    *   More information  
    *   Go to resource
*   Dataset XML English  French  Dataset  XML
[Explore](javascript:void(0);)  
    *   More information  
    *   Go to resource
*   Supporting Document HTML French  Guide  HTML
[Explore](javascript:void(0);)  
    *   More information  
    *   Go to resource
*   Supporting Document HTML English  Guide  HTML
[Explore](javascript:void(0);)  
    *   More information  
    *   Go to resource
Similar records
*   Timber assets (volume)  
*   Value of timber stocks (methods I and II)  
*   Natural resource assets and produced assets  
*   Indicator Summary Data: Trends in Timber Harvesting in BC  
*   Value of selected natural resource reserves
Did you find this dataset useful?
</excerpt>
### Rank 2 of 24 — 0.18
<excerpt title="untitled">

</excerpt>
### Rank 3 of 24 — 0.12
<excerpt title="untitled">

</excerpt>
### Rank 4 of 24 — 0.11
<excerpt title="untitled">

</excerpt>
### Rank 5 of 24 — 0.09
<excerpt title="untitled">

</excerpt>

## Search 9 — query: "38100106-eng.zip download"
### Rank 1 of 161 — 0.03 (passed on)
<excerpt title="Directory Listing /ftp/Specs/archive/38_series/38.106">
# Directory Listing /ftp/Specs/archive/38_series/38.106
## www.3gpp.org / ftp / Specs / archive / 38_series / 38.106
Drag and drop documents here or click to upload
Invalid folder name
Download

# Directory Listing /ftp/Specs/archive/38_series/38.106
## www.3gpp.org / ftp / Specs / archive / 38_series / 38.106
| - [x] |  | sort by name/desc | sort by date/desc | sort by size/desc |  
| --- | --- | --- | --- | --- |  
| - [x] |  | 38106-k00.zip | 2026/09/27 12:23 | 1894,9 KB |  
| - [x] |  | 38106-j60.zip | 2026/09/27 12:19 | 1892,9 KB |  
| - [x] |  | 38106-ic0.zip | 2026/09/27 10:25 | 1664,7 KB |  
| - [x] |  | 38106-j50.zip | 2026/07/06 12:15 | 1820 KB |  
| - [x] |  | 38106-ib0.zip | 2026/07/06 12:12 | 1591,1 KB |  
| - [x] |  | 38106-j40.zip | 2026/03/27 11:03 | 1814 KB |  
| - [x] |  | 38106-ia0.zip | 2026/03/27 11:03 | 1587,4 KB |  
| - [x] |  | 38106-hc0.zip | 2026/03/27 11:02 | 620,5 KB |  
| - [x] |  | 38106-j30.zip | 2026/01/17 11:21 | 1811,6 KB |
</excerpt>
### Rank 2 of 161 — 0.03
<excerpt title="Directory Listing /ftp/Specs/archive/38_series/38.106">
# Directory Listing /ftp/Specs/archive/38_series/38.106
## www.3gpp.org / ftp / Specs / archive / 38_series / 38.106
| - [x] |  | sort by name/desc | sort by date/desc | sort by size/desc |  
| --- | --- | --- | --- | --- |  
| - [x] |  | 38106-k00.zip | 2026/09/27 12:23 | 1894,9 KB |  
| - [x] |  | 38106-j60.zip | 2026/09/27 12:19 | 1892,9 KB |  
| - [x] |  | 38106-ic0.zip | 2026/09/27 10:25 | 1664,7 KB |  
| - [x] |  | 38106-j50.zip | 2026/07/06 12:15 | 1820 KB |  
| - [x] |  | 38106-ib0.zip | 2026/07/06 12:12 | 1591,1 KB |  
| - [x] |  | 38106-j40.zip | 2026/03/27 11:03 | 1814 KB |  
| - [x] |  | 38106-ia0.zip | 2026/03/27 11:03 | 1587,4 KB |  
| - [x] |  | 38106-hc0.zip | 2026/03/27 11:02 | 620,5 KB |  
| - [x] |  | 38106-j30.zip | 2026/01/17 11:21 | 1811,6 KB |
</excerpt>
### Rank 3 of 161 — 0.03
<excerpt title="Directory Listing /ftp/Specs/archive/38_series/38.106">
# Directory Listing /ftp/Specs/archive/38_series/38.106
## www.3gpp.org / ftp / Specs / archive / 38_series / 38.106
| - [x] |  | 38106-h90.zip | 2024/07/11 0:02 | 628,9 KB |  
| - [x] |  | 38106-i40.zip | 2024/04/05 9:14 | 1000,7 KB |  
| - [x] |  | 38106-h80.zip | 2024/04/05 9:13 | 627,1 KB |  
| - [x] |  | 38106-i30.zip | 2024/01/10 11:21 | 829,9 KB |  
| - [x] |  | 38106-h70.zip | 2024/01/10 11:20 | 624,3 KB |  
| - [x] |  | 38106-i20.zip | 2023/09/29 7:42 | 547,6 KB |  
| - [x] |  | 38106-h60.zip | 2023/09/29 7:42 | 585,6 KB |  
| - [x] |  | 38106-i10.zip | 2023/06/29 10:48 | 545,8 KB |  
| - [x] |  | 38106-h50.zip | 2023/06/29 10:47 | 583,6 KB |  
| - [x] |  | 38106-i00.zip | 2023/04/06 20:10 | 547,8 KB |  

# Directory Listing /ftp/Specs/archive/38_series/38.106
## www.3gpp.org / ftp / Specs / archive / 38_series / 38.106
| - [x] |  | 38106-h40.zip | 2023/04/06 13:49 | 509,2 KB |  
| - [x] |  | 38106-h30.zip | 2023/01/10 15:17 | 507,3 KB |  
| - [x] |  | 38106-h20.zip | 2022/09/27 17:10 | 499,3 KB |  
| - [x] |  | 38106-h10.zip | 2022/06/24 13:21 | 468,8 KB |  
| - [x] |  | 38106-100.zip | 2022/04/01 9:41 | 451,5 KB |  
| - [x] |  | 38106-h00.zip | 2022/04/01 9:16 | 350,9 KB |  
| - [x] |  | 38106-010.zip | 2022/03/15 12:01 | 344,5 KB |  
| - [x] |  | 38106-001.zip | 2021/04/02 6:04 | 55,3 KB |
* * *
37 items.
</excerpt>
### Rank 4 of 161 — 0.02
<excerpt title="HappyFile Archive">
| .zip ADK300ER14_happyfile.net_5868e1ed | .zip ADK300ER14_happyfile.net_5868e1ed | 2022-12-08 08:40 | 29M |  |  
| .tar AIR-AP1560-K9-ME-8-10-105-0_98.185.224.163_happyfile.net_b1a9b244 | .tar AIR-AP1560-K9-ME-8-10-105-0_98.185.224.163_happyfile.net_b1a9b244 | 2026-10-30 00:53 | 67M |  |  
| .tar AIR-AP1560-K9-ME-8-10-130-0_98.185.224.163_happyfile.net_0f61b26b | .tar AIR-AP1560-K9-ME-8-10-130-0_98.185.224.163_happyfile.net_0f61b26b | 2020-12-30 01:03 | 65M |  |  
| .zip AIR-AP1850-K9-ME-8-10-171-0_149.106.155.132_happyfile.net_da9dd8d0 | .zip AIR-AP1850-K9-ME-8-10-171-0_149.106.155.132_happyfile.net_da9dd8d0 | 2025-10-22 03:15 | 501M |  |  

| .zip AIR-AP1850-K9-ME-8-10-196-0_149.106.155.132_happyfile.net_1fb0a3ed | .zip AIR-AP1850-K9-ME-8-10-196-0_149.106.155.132_happyfile.net_1fb0a3ed | 2025-10-21 05:41 | 502M |  |  
| .tar AIR-AP2800-K9-ME-8-10-130-0_2600:4040:a5ef:7e00:3c3a:2dd5:f4df:eaeb_happyfile.net_554fc426 | .tar AIR-AP2800-K9-ME-8-10-130-0_2600:4040:a5ef:7e00:3c3a:2dd5:f4df:eaeb_happyfile.net_554fc426 | 2020-12-30 01:03 | 65M |  |  
| .zip AIR-AP2800-K9-ME-8-10-196-0_2804:214:800a:460:855d:46ec:ef14:783_happyfile.net_8b5c523a | .zip AIR-AP2800-K9-ME-8-10-196-0_2804:214:800a:460:855d:46ec:ef14:783_happyfile.net_8b5c523a | 2026-06-16 10:48 | 502M |  |
</excerpt>
### Rank 5 of 161 — 0.02
<excerpt title="Directory Listing /ftp/Specs/archive/38_series/38.106">
# Directory Listing /ftp/Specs/archive/38_series/38.106
## www.3gpp.org / ftp / Specs / archive / 38_series / 38.106
| - [x] |  | 38106-j20.zip | 2025/09/30 14:58 | 1793,1 KB |  
| - [x] |  | 38106-j10.zip | 2025/06/24 12:57 | 1792,7 KB |  
| - [x] |  | 38106-i90.zip | 2025/06/24 12:57 | 1589,2 KB |  
| - [x] |  | 38106-j00.zip | 2025/03/29 0:06 | 1590 KB |  
| - [x] |  | 38106-i80.zip | 2025/03/28 23:50 | 1591,9 KB |  
| - [x] |  | 38106-i70.zip | 2025/01/08 21:09 | 1589,1 KB |  
| - [x] |  | 38106-hb0.zip | 2025/01/08 21:08 | 634 KB |  
| - [x] |  | 38106-i60.zip | 2024/09/25 10:33 | 1571,9 KB |  
| - [x] |  | 38106-ha0.zip | 2024/09/25 10:33 | 629,9 KB |  
| - [x] |  | 38106-i50.zip | 2024/07/11 0:03 | 1562,4 KB |
</excerpt>

## Search 10 — query: "Timber assets (area) Quebec 1961 1962 Stats Canada"
### Rank 1 of 126 — 0.15 (passed on)
<excerpt title="Timber assets (area) - Open Government Portal - Canada.ca">
# Timber assets (area) - Open Government Portal
## You are here:
1.   Canada.ca  
2.   Open Government  
3.   Search
Open Data

# Timber assets (area)
Timber assets (area)This table contains 80 series, with data for years 1961 - 2003 (not all combinations necessarily have data for all years), and was last released on 2010-09-28. This table contains data described by the following dimensions (Not all combinations are available): Geography (10 items: Canada; New Brunswick; Newfoundland and Labrador; Nova Scotia ...), Timber assets (area) (8 items: Timber assets (area); non reserved accessible opening stock; Timber assets (area); fire; Timber assets (area); mortality; Timber assets (area); harvest ...).2023-01-17 Statistics Canada infostats@statcan.gc.ca Economics and Industry Nature and Environment economic accounts environment environment accounts land oceans ecosystems and biodiversity table Dataset CSV https://www150.statcan.gc.ca/n1/tbl/csv/38100106-fra.zip Dataset CSV https://www150.statcan.gc.ca/n1/tbl/csv/38100106-eng.zip Dataset XML https://www150.statcan.gc.ca/n1/tbl/sdmx/38100106-SDMX.zip Supporting Document HTML https://www150.statcan.gc.ca/t1/tbl1/fr/tv.action?pid=3810010601 Supporting Document HTML https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=3810010601
This table contains 80 series, with data for years 1961 - 2003 (not all combinations necessarily have data for all years), and was last released on 2010-09-28. This table contains data described by the following dimensions (Not all combinations are available): Geography (10 items: Canada; New Brunswick; Newfoundland and Labrador; Nova Scotia ...), Timber assets (area) (8 items: Timber assets (area); non reserved accessible opening stock; Timber assets (area); fire; Timber assets (area); mortality; Timber assets (area); harvest ...).
*   **Publisher - Current Organization Name:** Statistics Canada   
*   **Licence:**Open Government Licence - Canada

# Timber assets (area)
## Data and Resources
Search
*   Dataset CSV French  Dataset  CSV
[Explore](javascript:void(0);)  
    *   More information  
    *   Go to resource
*   Dataset CSV English  Dataset  CSV
[Explore](javascript:void(0);)  
    *   More information  
    *   Go to resource
*   Dataset XML English  French  Dataset  XML
[Explore](javascript:void(0);)  
    *   More information  
    *   Go to resource
*   Supporting Document HTML French  Guide  HTML
[Explore](javascript:void(0);)  
    *   More information  
    *   Go to resource
*   Supporting Document HTML English  Guide  HTML
[Explore](javascript:void(0);)  
    *   More information  
    *   Go to resource
Similar records
*   Timber assets (volume)  
*   Value of timber stocks (methods I and II)  
*   Natural resource assets and produced assets  
*   Indicator Summary Data: Trends in Timber Harvesting in BC  
*   Value of selected natural resource reserves
Did you find this dataset useful?
</excerpt>
### Rank 2 of 126 — 0.09
<excerpt title="Timber assets (area)">
# Timber assets (area)
*   Skip to main content  
*   Skip to "About this site"

# Timber assets (area)
## Language selection
*   Français
/ Gouvernement du Canada

# Timber assets (area)
## Search and menus
*   Search and menus

# Timber assets (area)
## Search
Search Statistics Canada
Search

# Timber assets (area)
## Topics menu
*   Subjects  
*   Data  
*   Analysis  
*   Reference  
*   Geography  
*   Census  
*   Surveys and statistical programs  
*   About StatCan  
*   Canada.ca
1.   Home  
2.   Data

# Timber assets (area)
## Archived Content
Information identified as archived is provided for reference, research or recordkeeping purposes. It is not subject to the Government of Canada Web Standards and has not been altered or updated since it was archived. Pleasecontact us to request a format other than those available.
[Content is archived.](javascript:;)

# Archived - Timber assets (area) (x 1,000)1, 2
Frequency:Annual
Table: 38-10-0106-01 (formerly CANSIM 153-0029)
Release date: 2010-09-28
_Geography:_
Help
Save my customizations
Customize table
Geography :
Reference period
From:  To:
Apply
Add/Remove data

# Archived - Timber assets (area) (x 1,000)1, 2
## Add/Remove data help
Select your items to create your customized table.
Download options

# Archived - Timber assets (area) (x 1,000)1, 2
## Download options
### CSV Download as displayed{{ csvSize }}kB.


# Archived - Timber assets (area) (x 1,000)1, 2
## Download options
### CSV Download as displayed(excluding accompanying symbols).


# Archived - Timber assets (area) (x 1,000)1, 2
## Download options
### CSV Download as displayed(symbols separate).


# Archived - Timber assets (area) (x 1,000)1, 2
## Download options
### CSV Download selected data(for database loading).


# Archived - Timber assets (area) (x 1,000)1, 2
## Download options
### CSV Download cube metadata information, ~50kB.


# Archived - Timber assets (area) (x 1,000)1, 2
## Download options
### CSV Download entire table "Timber assets (area)".


# Archived - Timber assets (area) (x 1,000)1, 2
## Download options
### SDMX Download entire table.
Other data access options:Developers
Showing  records
Filter
Reset
No results found.
**Notes :**
**How to cite:** Statistics Canada. Table 38-10-0106-01 Timber assets (area) (x 1,000)
**DOI:**https://doi.org/10.25318/3810010601-eng

# Archived - Timber assets (area) (x 1,000)1, 2
## Related information
Source (Surveys and statistical programs)
*   Canadian System of Environmental-Economic Accounts - Natural Resource Asset Accounts
Subjects and keywords

# Archived - Timber assets (area) (x 1,000)1, 2
## Related information
### Subjects
*   Economic accounts  
    Environment accounts

    

*   Environment  
    Land, oceans, ecosystems and biodiversity
Date modified: 2026-11-18

# Archived - Timber assets (area) (x 1,000)1, 2
## About this site
### Statistics Canada
*   Contact StatCan  
*   Trust Centre

# Archived - Timber assets (area) (x 1,000)1, 2
## About this site
### Government of Canada
*   All contacts  
*   Departments and agencies  
*   About government
</excerpt>
### Rank 3 of 126 — 0.05
<excerpt title="FOREST RESOURCES 2.—Estimate of Standing Timber, by Type and Size ...">
Title: PDF document  
URL Source: https://www66.statcan.gc.ca/eng/1962/196204690449_p.%20449.pdf  
Markdown Content:

## [PDF page 1]
FOREST RESOURCES  449
2.—Estimate  of Standing Timber, by Type and Size and by Province and Region, 1961
Coniferous  Broadleaved  Totals
Province or Territory Province or Territory  
and Region and Region  Large  Small  Large  Small  
Large  1  Small Material2 Total  1  2  Total  Material1  Material2  Total  
Material  Material  Material
Million cu. ft. Million cu. ft. Million cu. ft. Million cu. ft. Million cu. ft. Million cu. ft. '000 '000 '000 '000 '000 '000 Million Million Million Million Million Million Million Million Million Million Million Million '000 '000 '000 '000 '000 '000 Million Million Million Million Million Million Million Million Million Million Million Million '000 '000 '000 '000 '000 '000 Million  
cords cords cords cords cords cords cu. ft. cu. ft. cu. ft. cu. ft. cu. ft. cu. ft. cu. ft. cu. ft. cu. ft. cu. ft. cu. ft. cu. ft. cords cords cords cords cords cords cu. ft. cu. ft. cu. ft. cu. ft. cu. ft. cu. ft. cu. ft. cu. ft. cu. ft. cu. ft. cu. ft. cu. ft. cords cords cords cords cords cords cu. ft.  
Accessible

## [PDF page 1]
2,296 1,101 2,296 1,101 2,296 1,101 2,296 1,101 2,296 1,101 2,296 1,101 129,225 6S.S48 129,225 6S.S48 129,225 6S.S48 129,225 6S.S48 129,225 6S.S48 129,225 6S.S48 13,280 6,485 13,280 6,485 13,280 6,485 13,280 6,485 13,280 6,485 13,280 6,485 293 293 293 293 293 293 3,755 2,185 3,755 2,185 3,755 2,185 3,755 2,185 3,755 2,185 3,755 2,185 613 613 613 613 613 613 2,589 1,184 2,589 1,184 2,589 1,184 2,589 1,184 2,589 1,184 2,589 1,184 132,980 86,5S8 132,980 86,5S8 132,980 86,5S8 132,980 86,5S8 132,980 86,5S8
</excerpt>
### Rank 4 of 126 — 0.04
<excerpt title="Timber assets (area) - Open Government Portal - Canada.ca">
# Timber assets (area) - Open Government Portal
## Menu
    *   Most requested  
        *   Jobs in the Forces  
        *   Canadian military support to Ukraine  
        *   Military ranks  
        *   Defence equipment  
        *   Canada's Defence policy  
        *   Join the Cadet Program

*   Culture, history and sport  
    *   Culture, history and sport: home

    *   Funding - Culture, history and sport  
    *   Events, celebrations and commemorations  
    *   Cultural landmarks and attractions  
    *   Canadian identity and society  
    *   Sport  
    *   History and heritage  
    *   Arts and media  
    *   Youth leadership and cultural program  
    *   Cultural trade and investment

    *   Most requested  
        *   Visit the Canadian Virtual War Memorial  
        *   Anthems and symbols of Canada  
        *   Find a CRTC decision  
        *   Research your family history  
        *   Search census records  
        *   Major events in Canada's Capital Region

*   Policing, justice and emergencies  
    *   Policing, justice and emergencies: home

    *   Policing  
    *   Justice  
    *   Emergencies  
    *   Corrections  
    *   Parole, record suspension, expungement and clemency  
    *   Victims of crime  
    *   Crime and justice statistics

    *   Most requested  
        *   Wildfire Response  
        *   Apply/Renew a firearms licence  
        *   Get a criminal records check  
        *   Apply for a criminal record suspension  
        *   What to do during an emergency  
        *   Know the law on impaired driving  
        *   Help solve a crime

*   Transport and infrastructure  
    *   Transport and infrastructure: home

    *   Zero-emission vehicles  
    *   Aviation  
    *   Marine transportation  
    *   Road transportation  
    *   Rail transportation  
    *   Dangerous goods  
    *   Infrastructure

    *   Most requested  
        *   Drone safety  
        *   What not to bring on a plane  
        *   Register your vessel  
        *   Child car seat safety  
        *   Transporting dangerous goods - Regulations  
        *   _Canadian Aviation Regulations_

*   Canada and the world  
    *   Canada and the world: home
</excerpt>
### Rank 5 of 126 — 0.04
<excerpt title="Timber assets (area) - Open Government Portal - Canada.ca">
# Timber assets (area)
## Data and Resources
Search
*   Dataset CSV French  Dataset  CSV
[Explore](javascript:void(0);)  
    *   More information  
    *   Go to resource
*   Dataset CSV English  Dataset  CSV
[Explore](javascript:void(0);)  
    *   More information  
    *   Go to resource
*   Dataset XML English  French  Dataset  XML
[Explore](javascript:void(0);)  
    *   More information  
    *   Go to resource
*   Supporting Document HTML French  Guide  HTML
[Explore](javascript:void(0);)  
    *   More information  
    *   Go to resource
*   Supporting Document HTML English  Guide  HTML
[Explore](javascript:void(0);)  
    *   More information  
    *   Go to resource
Similar records
*   Timber assets (volume)  
*   Value of timber stocks (methods I and II)  
*   Natural resource assets and produced assets  
*   Indicator Summary Data: Trends in Timber Harvesting in BC  
*   Value of selected natural resource reserves
Did you find this dataset useful?

# Timber assets (area)
## Provide feedback on this dataset
Privacy Statement  
The collection and use of your personal information is authorized by the _Financial Administration Act_. Collection and use of your personal information for this site is in accordance with the federal _Privacy Act_. Your personal information is used to validate your use of GC datasets and for information on the development of the GC open data initiative, and may also be used to evaluate the effectiveness of the program in responding to client needs. In exceptional circumstances (e.g. network intrusion, or of individuals who make inappropriate remarks or threats, etc.), personal information may be disclosed without your consent pursuant to subsection 8(2) of the _Privacy Act_.
Any personal information that may be collected is described in the Standard Personal Information Banks entitled Public Communications, PSU 914, and Outreach Activities, PSU 938, which can be found in the Treasury Board of Canada Secretariat (TBS) publication: _InfoSource_.
Under the _Privacy Act_, you have the right of access to, and correction of, your personal information, if you have provided any. Note however, that to exercise either of these rights; you must make a request for access to your personal information. For more information about your right of access, please read about the Access to Information Program.
Any questions, comments, concerns or complaints you may have regarding this Statement, your privacy rights and the _Privacy Act_ may be directed to the TBS Access to Information and Privacy Coordinator by email at [atip.aiprp@tbs-sct.gc.ca](mailto:atip.aiprp@tbs-sct.gc.ca) or by calling 613-946-6260 or 1-866-312-1511. If you are not satisfied with TBS' response to your privacy concern, you may wish to contact the Office of the Privacy Commissioner by email at [info@priv.gc.ca](mailto:info@priv.gc.ca) or by telephone at 1-800-282-1376. You have the right to complain to the Office of the Privacy Commissioner about TBS' handling of your personal information.
Name
Email address
I am a
Reason for feedback
Feedback
(required)
Have your say
*   Rate this dataset  
*   Provide feedback
Additional Information
</excerpt>

# Example 5
## Question
I'm studying the effects of product safety legislation on safety recalls during periods of economic turmoil, with a main focus on the Covid-19 pandemic in Australia and gas products. 

Give me a list of the PRA Numbers of all product safety recalls posted on www.productsafety.gov.au between 1 January 2020 and 1 July 2020 (inclusive) that have been labelled as containing the topic "Gas products and appliances". Exclude products that were not sold 'Nationally'.

The list should look like this: 2020/11111, 2020/11112, 2020/11115, 2020/11116, 2020/11117, 2020/11119, 2020/11125

## Expected answer
2020/18315, 2020/18164, 2020/18098

## Grade 0.00

## Search 1 — query: "site:productsafety.gov.au 2020 "PRA" "Gas products and appliances" "National""
(no page could be scored)

## Search 2 — query: "PRA 2020 gas products and appliances site:productsafety.gov.au"
### Rank 1 of 77 — 0.09 (passed on)
<excerpt title="Suburban Recreational Vehicle Water Heaters Model SW6PA, ...">
## Product description
Suburban Recreational Vehicle Water Heaters fitted to caravans, motorhomes and horse float campers.
Models:
*   SW6PA  
*   SW6DEA  
*   SW6DA  
*   SW4DEA  
*   SW4DA  
*   SW4DECA  
*   SW6DECA
Serial numbers between:
*   181315552 and 193002648 (some serial numbers may end with a 'D'), and  
*   8183311827 and 8190201139.
**How to identify affected water heaters:**Open the exterior access door to the water heater and check the model and serial number located on the right-hand side.
Manufactured between 4 April 2018 and 1 August 2019.
Sold between 1 May 2018 and 25 September 2019.
See the list of affected serial numbers in the 'Identifying features' section below.
There are 18,139 affected units.
See a list of details to help identify the product

## Reason the product is recalled
A component of the water heater may be improperly manufactured and allow carbon monoxide into your caravan, motorhome or horse float camper.

## The hazards to consumers
Carbon monoxide is a poisonous gas and can cause serious illness, injury or death. Carbon monoxide has no smell or taste, is highly flammable and can only be detected with a carbon monoxide alarm. Loss of consciousness can occur within minutes and death can occur within hours. Further information on the hazards of carbon monoxide can be viewed here.

## What consumers should do
Consumers who have not already had their unit inspected must not use the affected water heater in gas mode under any circumstances, even if they have a carbon monoxide detector.
**The remedy for this recall was updated on 29 January 2024. An inspection is no longer required, all affected water heaters that have not already been inspected will be replaced for free.**
Contact Coast to Coast Caravan and Leisure for a free replacement.
Call 02 9645 7685 or email recalls@coastrv.com.au.
Coast to Coast Caravan and Leisure will offer compensation for any additional consequential loss suffered by the consumer where there is damage or devaluation to the caravan or motorhome attributed to the installation of a replacement water heater. Consequential loss will be determined on a case by case basis.
For more information visit www.coastrv.com.au/suburban-recall.

## What consumers should do
### Who sold the product
Coast to Coast Caravan and Leisure agents and dealerships

## What consumers should do
### Dates available for sale
1 May 2018 - 25 September 2019

## What consumers should do
### Where the product was sold
Nationally
International

## Responsible regulators
Regulators are established or appointed by government. They enforce regulations and rules.
**Quote PRA number 2019/17885** when contacting a regulator about this recall.

## Responsible regulators
### Recall and remedy questions
Contact the Australian Competition and Consumer Commission if you have:
*   a question about the remedy being offered to you by the business that is responsible for managing this recall, or  
*   concerns about the way the business is managing this recall.
</excerpt>
### Rank 2 of 77 — 0.06
<excerpt title="Conducting a consumer product safety recall">
## [PDF page 17]
Your recall adver  tisement is at tached to your recall notice on the Product S afet y Australia website.
You may need to change the amount of information available on your recall adver  tisement to suit  
the communications channel you use. Always give consumers a link to the full details and recalls  
adver  tisement that is on your website or the recall notice on the Product S afet y Australia website.
E xamples of adver  tisements and communications are in our re c all communications package.
12
PDF link

## [PDF page 18]
Example:
Do you own this product?
"[Click to add: Product name]"  
"[Click to add: product identifiers]"
Dates sold: "[Click to add: dates sold]"
Why the product is recalled: "[Click to add: Text]"
Hazard:  "[Click to add: Text]"
1.  "[Click to add call to action statement]"  
2.  Send us an email or phone us if you are unable to return the product  
or have sold or gifted it to another person
Ask our staff to find out more about the recall.
[email@email.com]
"[Phone number]" Xam to Xpm Monday to Friday
Purchased from: "[Click to add: Text]"
Scan for information about this recall
[Add your own QR Code or remove if not required]
Set yourself a reminder to check at home
•  Take a photo of this notice  
•  Set a reminder on your phone
PRA [xx/  xxxx]
See productsafety.gov.au for  
Australian product recall information
13

## [PDF page 19]
Te l  l people who a re oversea s a nd g ive us a copy
Tell people you have supplied the product to, who are located outside Australia, in writing as  
soon as practical.
Tell them that the product is being recalled in Australia and describe:  
	the defect or why it is dangerous, or the use or misuse that is dangerous  
	if the product does not meet or is likely not to meet a mandator y safet y standard or is banned.
Within 10 days of informing overseas people, you must give a copy of your notice to the  
Commonwealth Minister. You can do this by emailing the notice to recallsmonitoring@accc.gov.au.
This is a requirement under the Australian Consumer L aw.
If you are coordinating the recall for other suppliers who have supplied the product to a person  
outside Australia, you need to make sure that all the suppliers meet this notification requirement.
Repor  t a ny produc t-re lated deat  h s, ser ious i nju r ies,  
or i  l  l  nesses
Submit a mandator y repor  t within 2 days of becoming aware of any death, serious injur y or  
illness associated with a consumer product you supplied.
You are required to submit a mandator y repor  t if your product has caused a death, serious injur y or  
illness, regardless of whether you have recalled the product. This is a legal requirement under the  
Australian Consumer L aw and penalties may apply if you do not repor  t or take longer than 2 days  
to repor t.
A serious illness or injur y is an acute physical injur y or illness which needs medical or surgical  
treatment by, or under the super vision of, a medical practitioner or a nurse.
A mandator y repor  t is when a supplier tells the Commonwealth Minister of a death, serious injur y  
or illness that was caused, or may have been caused, by the use or foreseeable misuse of a  
consumer product.
The ACCC accepts your mandator  y repor  t on behalf of the Commonwealth Minister.
If you need to submit a mandator y repor  t for a product you have recalled, reassess the risk and  
update your communication strategy. This includes adding a message to your recall communications  
that serious injuries have occurred.
14

## [PDF page 19]
PDF link
</excerpt>
### Rank 3 of 77 — 0.05
<excerpt title="Conducting a consumer product safety recall">
## [PDF page 73]
I n store adver  t  isi ng poster
Do you own this product?
"[Click to add: Product name]"  
"[Click to add: product identifiers]"
Dates sold: "[Click to add: dates sold]"
Why the product is recalled: "[Click to add: Text]"
Hazard:  "[Click to add: Text]"
1.  "[Click to add call to action statement]"  
2.  Send us an email or phone us if you are unable to return the product  
or have sold or gifted it to another person
Ask our staff to find out more about the recall.
[email@email.com]
"[Phone number]" Xam to Xpm Monday to Friday
Purchased from: "[Click to add: Text]"
Scan for information about this recall
[Add your own QR Code or remove if not required]
Set yourself a reminder to check at home
•  Take a photo of this notice  
•  Set a reminder on your phone
PRA [xx/  xxxx]
See productsafety.gov.au for  
Australian product recall information
68

## [PDF page 74]
SM S
Message for unk nown consumers
From: [supplier name]
PRODU CT S A FE T  Y R ECA LL :
[ produc t].
Do you own this produc t ?
[inser  t call to ac tion]
More de tails: [web address].
PRA No.[XX/XXXX]
U nsub: reply S TOP
Message for k nown consumers
From: [supplier name]
PRODU CT S A FE T  Y R ECA LL :
You bought [ produc t] from us in [MM Y  Y].
[inser  t call to ac tion]
More de tails: [web address].
PRA No.[XX/XXXX]
U nsub: reply S TOP
Understand your obligations under the S pam Act 20 03 and the Privacy Act 198 8 before sending an S MS  
to consumers.
69
PDF link  
PDF link

## [PDF page 75]
Soc ia  l med ia message
E  xa m p l e:
Does your child sleep in these pyjamas? S top using the product immediately and return it to the place  
of purchase for a full refund. [Link to recall information]
	Include a call to action and ask a question to viewers – see examples.  
	Keep your message simple with plain language, easy and shor  t words:
–  include a clear image of the recalled product  
–  add the product name  
–  describe the defect – use the approved words from your recall message  
–  refer to the maximum harm that can occur, which may mean specif ying “  death or serious  
injur y ” as the potential harm that could occur.  
	Set a sc hedule to repeat your message – your social media manager or coordinator may have  
this available for you to use.  
	Add a Learn More or C ontac t Us bu t ton if the option is available – direct consumers to the  
recall information on your website, the recall notice on the Product S afet y Australia website, or an  
online form where consumers can contact you.  
	Create a s tor y to use in addition to your social media post:
–  include your social media image  
–  ask a question to consumers (see examples)  
–  include the words: S wipe up to learn more about the recall OR S wipe up to get your refund  
–  direct consumers to the recall information on your website, or your recall notice on  
productsafet y.gov.au  
–  the swipe up option may only be available to business social media profiles with a large number  
of followers.
70
</excerpt>
### Rank 4 of 77 — 0.05
<excerpt title="Conducting a consumer product safety recall">
## [PDF page 57]
Somet  i mes a not  her gover n ment agenc  y leads t  he  
reca  l  l
Dif ferent government agencies are responsible for regulating the safet y of dif ferent t ypes of  
products including:  
	agricultural products  
	a s b e s to s  
	building and building materials  
	c he mic als  
	therapeutic goods such as medicines, complementar y medicines, medical devices and medical  
te s t s  
	electrical goods  
	food and beverages  
	gas appliances  
	road vehicles and road traffic safet y  
	smoking and tobacco  
	veterinar y chemical products.
Products that are covered by a specialist regime may also be a consumer good covered by the  
Australian C onsumer L aw.
Which agency is the lead agency
The ACCC and specialist agencies have arrangements in place to identif y which agency is the lead  
agency when a product safet y issue occurs.
52

## [PDF page 58]
Agricultural and veterinar  y produc ts, food, therapeutic goods, and road  
vehicles  
For the following products, the specialist agency, and not the ACCC, is the lead agency for the recall  
and other safet y issues.
For these products, the specialist agency :  
	assesses the recall and publishes the recall on its website  
	decides whether to inter vene in the recall and what actions to take.
The specialist agency ’s guidelines, and not these guidelines, apply to the recall. Suppliers need to  
check the specialist agency ’s recall guidelines, as updated from time to time, to understand what they  
have to do when conducting the recall.
Product  Specialist (lead) agency  Recall resources
Agricultural and  Australian Pesticides and  Re call website  
veterinar y chemical  Veterinar y Medicines Authorit y  Guidelines For re calling Agricultural and Veterinar y  
pro ducts  Chemical Products
Food  Food S tandards Australia  Re call website  
New Zealand (FS A NZ ) is the  Food Industr y Re call proto col  
coordinating authorit y working  
with the relevant state or  Noti fi cation of the re call to the AC C C is done by  
territor y food agency  FS A NZ on behalf of the food business under  taking  
the re call
Therapeutic goods  Therapeutic Goods  Re call website  
Administration  Uniform re call pro cedure for therapeutic goods
Road vehicles and  Depar tment of Infrastructure,  Re calls website  
approved road  Transpor t, Regional  Re calls policy  
vehicle par ts  Development and  
Communications  Re call notices for road vehicles and approved road  
vehicles par  ts are re ceived by the Depar  tment , and  
not the AC C C, under the Australian C onsumer L aw
53
PDF link  
PDF link  
PDF link  
PDF link  
PDF link  
PDF link  
PDF link  
PDF link  
PDF link  
PDF link  
PDF link  
PDF link
</excerpt>
### Rank 5 of 77 — 0.05
<excerpt title="Conducting a consumer product safety recall">
## [PDF page 71]
	The chance of injur y or death is low or rare  
	It is unlikely that an incident will occur  
	In the unlikely event  
	Low  r isk  
	In rare circumstances/occasions  
	Isolated incidents  
	E  x  tre m el y rare c ases  
	No injuries in Australia have been repor  ted  
	No injuries have occurred  
	Thermal event  
	Hot smoke  
	S econdar y impact.
66

## [PDF page 72]
E m  a  i  l  /  le t  te  r
S ubjec t: Produc t safet y recall – [inser t produc t name] [PR  A No. X X  / X X X X]
Dear [consumer ’s name]
Do you own this product? (or) Our records show  
that you purchased this product in [Month Year].  
Product name  
Product identifiers (barcode, model number)  
Purchased from: [Stores where product was sold]  
Dates sold
Why we are recalling the product  
[insert defect information here here]  
Hazard: [insert hazard information here]  
[Insert image of  You are at risk of [death or injury] if you continue to use this product  
the defect if  OR  
available in  Your child is at risk of [death or injury] if they continue [play with / use] this  
addition to hazard  product.  
symbol]
1.  [insert call to action statement]  
2.  Contact us if you are unable to return the product or have sold it to another  
person.
[www.website.com/recall]  
[email@email.com]  
(0X) XXXX XXXX Xam to Xpm Monday to Friday
Contact the Translating and Interpreting Service (TIS).  
131 450 or visit tisnational.gov.au to book a phone interpreter and provide our  
phone number 0X XXXX XXXX
If you have a hearing or speech impairment- contact us through the National  
Relay Service  
1800 555 660  and ask for 0X XXXX XXXX  or visit RelayService.gov.au
See productsafety.gov.au for  
Australian product recall information
Yours sincerely,  
[name]  
[position]
67

## [PDF page 73]
I n store adver  t  isi ng poster
Do you own this product?
"[Click to add: Product name]"  
"[Click to add: product identifiers]"
Dates sold: "[Click to add: dates sold]"
Why the product is recalled: "[Click to add: Text]"
Hazard:  "[Click to add: Text]"
1.  "[Click to add call to action statement]"  
2.  Send us an email or phone us if you are unable to return the product  
or have sold or gifted it to another person
Ask our staff to find out more about the recall.
[email@email.com]
"[Phone number]" Xam to Xpm Monday to Friday
Purchased from: "[Click to add: Text]"
Scan for information about this recall
[Add your own QR Code or remove if not required]
Set yourself a reminder to check at home
•  Take a photo of this notice  
•  Set a reminder on your phone
PRA [xx/  xxxx]
See productsafety.gov.au for  
Australian product recall information
68
</excerpt>

## Search 3 — query: "2020 "PRA" "Gas products and appliances" productsafety.gov.au 2020"
### Rank 1 of 1 — 0.17 (passed on)
<excerpt title="Suburban Recreational Vehicle Water Heaters Model SW6PA, ...">
## Product description
Suburban Recreational Vehicle Water Heaters fitted to caravans, motorhomes and horse float campers.
Models:
*   SW6PA  
*   SW6DEA  
*   SW6DA  
*   SW4DEA  
*   SW4DA  
*   SW4DECA  
*   SW6DECA
Serial numbers between:
*   181315552 and 193002648 (some serial numbers may end with a 'D'), and  
*   8183311827 and 8190201139.
**How to identify affected water heaters:**Open the exterior access door to the water heater and check the model and serial number located on the right-hand side.
Manufactured between 4 April 2018 and 1 August 2019.
Sold between 1 May 2018 and 25 September 2019.
See the list of affected serial numbers in the 'Identifying features' section below.
There are 18,139 affected units.
See a list of details to help identify the product

## Reason the product is recalled
A component of the water heater may be improperly manufactured and allow carbon monoxide into your caravan, motorhome or horse float camper.

## The hazards to consumers
Carbon monoxide is a poisonous gas and can cause serious illness, injury or death. Carbon monoxide has no smell or taste, is highly flammable and can only be detected with a carbon monoxide alarm. Loss of consciousness can occur within minutes and death can occur within hours. Further information on the hazards of carbon monoxide can be viewed here.

## What consumers should do
Consumers who have not already had their unit inspected must not use the affected water heater in gas mode under any circumstances, even if they have a carbon monoxide detector.
**The remedy for this recall was updated on 29 January 2024. An inspection is no longer required, all affected water heaters that have not already been inspected will be replaced for free.**
Contact Coast to Coast Caravan and Leisure for a free replacement.
Call 02 9645 7685 or email recalls@coastrv.com.au.
Coast to Coast Caravan and Leisure will offer compensation for any additional consequential loss suffered by the consumer where there is damage or devaluation to the caravan or motorhome attributed to the installation of a replacement water heater. Consequential loss will be determined on a case by case basis.
For more information visit www.coastrv.com.au/suburban-recall.

## What consumers should do
### Who sold the product
Coast to Coast Caravan and Leisure agents and dealerships

## What consumers should do
### Dates available for sale
1 May 2018 - 25 September 2019

## What consumers should do
### Where the product was sold
Nationally
International

## Responsible regulators
Regulators are established or appointed by government. They enforce regulations and rules.
**Quote PRA number 2019/17885** when contacting a regulator about this recall.

## Responsible regulators
### Recall and remedy questions
Contact the Australian Competition and Consumer Commission if you have:
*   a question about the remedy being offered to you by the business that is responsible for managing this recall, or  
*   concerns about the way the business is managing this recall.
</excerpt>

## Search 4 — query: "site:productsafety.gov.au "2020/" "Gas products and appliances" "National""
(no page could be scored)

## Search 5 — query: "site:productsafety.gov.au "PRA" "Gas products" "2020/""
### Rank 1 of 1 — 0.14 (passed on)
<excerpt title="Suburban Recreational Vehicle Water Heaters Model SW6PA, ...">
## Product description
Suburban Recreational Vehicle Water Heaters fitted to caravans, motorhomes and horse float campers.
Models:
*   SW6PA  
*   SW6DEA  
*   SW6DA  
*   SW4DEA  
*   SW4DA  
*   SW4DECA  
*   SW6DECA
Serial numbers between:
*   181315552 and 193002648 (some serial numbers may end with a 'D'), and  
*   8183311827 and 8190201139.
**How to identify affected water heaters:**Open the exterior access door to the water heater and check the model and serial number located on the right-hand side.
Manufactured between 4 April 2018 and 1 August 2019.
Sold between 1 May 2018 and 25 September 2019.
See the list of affected serial numbers in the 'Identifying features' section below.
There are 18,139 affected units.
See a list of details to help identify the product

## Reason the product is recalled
A component of the water heater may be improperly manufactured and allow carbon monoxide into your caravan, motorhome or horse float camper.

## The hazards to consumers
Carbon monoxide is a poisonous gas and can cause serious illness, injury or death. Carbon monoxide has no smell or taste, is highly flammable and can only be detected with a carbon monoxide alarm. Loss of consciousness can occur within minutes and death can occur within hours. Further information on the hazards of carbon monoxide can be viewed here.

## What consumers should do
Consumers who have not already had their unit inspected must not use the affected water heater in gas mode under any circumstances, even if they have a carbon monoxide detector.
**The remedy for this recall was updated on 29 January 2024. An inspection is no longer required, all affected water heaters that have not already been inspected will be replaced for free.**
Contact Coast to Coast Caravan and Leisure for a free replacement.
Call 02 9645 7685 or email recalls@coastrv.com.au.
Coast to Coast Caravan and Leisure will offer compensation for any additional consequential loss suffered by the consumer where there is damage or devaluation to the caravan or motorhome attributed to the installation of a replacement water heater. Consequential loss will be determined on a case by case basis.
For more information visit www.coastrv.com.au/suburban-recall.

## What consumers should do
### Who sold the product
Coast to Coast Caravan and Leisure agents and dealerships

## What consumers should do
### Dates available for sale
1 May 2018 - 25 September 2019

## What consumers should do
### Where the product was sold
Nationally
International

## Responsible regulators
Regulators are established or appointed by government. They enforce regulations and rules.
**Quote PRA number 2019/17885** when contacting a regulator about this recall.

## Responsible regulators
### Recall and remedy questions
Contact the Australian Competition and Consumer Commission if you have:
*   a question about the remedy being offered to you by the business that is responsible for managing this recall, or  
*   concerns about the way the business is managing this recall.
</excerpt>

## Search 6 — query: "2020 gas products and appliances recall site:productsafety.gov.au "PRA""
### Rank 1 of 74 — 0.23 (passed on)
<excerpt title="Suburban Recreational Vehicle Water Heaters Model SW6PA, ...">
## Product description
Suburban Recreational Vehicle Water Heaters fitted to caravans, motorhomes and horse float campers.
Models:
*   SW6PA  
*   SW6DEA  
*   SW6DA  
*   SW4DEA  
*   SW4DA  
*   SW4DECA  
*   SW6DECA
Serial numbers between:
*   181315552 and 193002648 (some serial numbers may end with a 'D'), and  
*   8183311827 and 8190201139.
**How to identify affected water heaters:**Open the exterior access door to the water heater and check the model and serial number located on the right-hand side.
Manufactured between 4 April 2018 and 1 August 2019.
Sold between 1 May 2018 and 25 September 2019.
See the list of affected serial numbers in the 'Identifying features' section below.
There are 18,139 affected units.
See a list of details to help identify the product

## Reason the product is recalled
A component of the water heater may be improperly manufactured and allow carbon monoxide into your caravan, motorhome or horse float camper.

## The hazards to consumers
Carbon monoxide is a poisonous gas and can cause serious illness, injury or death. Carbon monoxide has no smell or taste, is highly flammable and can only be detected with a carbon monoxide alarm. Loss of consciousness can occur within minutes and death can occur within hours. Further information on the hazards of carbon monoxide can be viewed here.

## What consumers should do
Consumers who have not already had their unit inspected must not use the affected water heater in gas mode under any circumstances, even if they have a carbon monoxide detector.
**The remedy for this recall was updated on 29 January 2024. An inspection is no longer required, all affected water heaters that have not already been inspected will be replaced for free.**
Contact Coast to Coast Caravan and Leisure for a free replacement.
Call 02 9645 7685 or email recalls@coastrv.com.au.
Coast to Coast Caravan and Leisure will offer compensation for any additional consequential loss suffered by the consumer where there is damage or devaluation to the caravan or motorhome attributed to the installation of a replacement water heater. Consequential loss will be determined on a case by case basis.
For more information visit www.coastrv.com.au/suburban-recall.

## What consumers should do
### Who sold the product
Coast to Coast Caravan and Leisure agents and dealerships

## What consumers should do
### Dates available for sale
1 May 2018 - 25 September 2019

## What consumers should do
### Where the product was sold
Nationally
International

## Responsible regulators
Regulators are established or appointed by government. They enforce regulations and rules.
**Quote PRA number 2019/17885** when contacting a regulator about this recall.

## Responsible regulators
### Recall and remedy questions
Contact the Australian Competition and Consumer Commission if you have:
*   a question about the remedy being offered to you by the business that is responsible for managing this recall, or  
*   concerns about the way the business is managing this recall.
</excerpt>
### Rank 2 of 74 — 0.09
<excerpt title="Conducting a consumer product safety recall">
## [PDF page 71]
	The chance of injur y or death is low or rare  
	It is unlikely that an incident will occur  
	In the unlikely event  
	Low  r isk  
	In rare circumstances/occasions  
	Isolated incidents  
	E  x  tre m el y rare c ases  
	No injuries in Australia have been repor  ted  
	No injuries have occurred  
	Thermal event  
	Hot smoke  
	S econdar y impact.
66

## [PDF page 72]
E m  a  i  l  /  le t  te  r
S ubjec t: Produc t safet y recall – [inser t produc t name] [PR  A No. X X  / X X X X]
Dear [consumer ’s name]
Do you own this product? (or) Our records show  
that you purchased this product in [Month Year].  
Product name  
Product identifiers (barcode, model number)  
Purchased from: [Stores where product was sold]  
Dates sold
Why we are recalling the product  
[insert defect information here here]  
Hazard: [insert hazard information here]  
[Insert image of  You are at risk of [death or injury] if you continue to use this product  
the defect if  OR  
available in  Your child is at risk of [death or injury] if they continue [play with / use] this  
addition to hazard  product.  
symbol]
1.  [insert call to action statement]  
2.  Contact us if you are unable to return the product or have sold it to another  
person.
[www.website.com/recall]  
[email@email.com]  
(0X) XXXX XXXX Xam to Xpm Monday to Friday
Contact the Translating and Interpreting Service (TIS).  
131 450 or visit tisnational.gov.au to book a phone interpreter and provide our  
phone number 0X XXXX XXXX
If you have a hearing or speech impairment- contact us through the National  
Relay Service  
1800 555 660  and ask for 0X XXXX XXXX  or visit RelayService.gov.au
See productsafety.gov.au for  
Australian product recall information
Yours sincerely,  
[name]  
[position]
67

## [PDF page 73]
I n store adver  t  isi ng poster
Do you own this product?
"[Click to add: Product name]"  
"[Click to add: product identifiers]"
Dates sold: "[Click to add: dates sold]"
Why the product is recalled: "[Click to add: Text]"
Hazard:  "[Click to add: Text]"
1.  "[Click to add call to action statement]"  
2.  Send us an email or phone us if you are unable to return the product  
or have sold or gifted it to another person
Ask our staff to find out more about the recall.
[email@email.com]
"[Phone number]" Xam to Xpm Monday to Friday
Purchased from: "[Click to add: Text]"
Scan for information about this recall
[Add your own QR Code or remove if not required]
Set yourself a reminder to check at home
•  Take a photo of this notice  
•  Set a reminder on your phone
PRA [xx/  xxxx]
See productsafety.gov.au for  
Australian product recall information
68
</excerpt>
### Rank 3 of 74 — 0.09
<excerpt title="Conducting a consumer product safety recall">
## [PDF page 17]
Your recall adver  tisement is at tached to your recall notice on the Product S afet y Australia website.
You may need to change the amount of information available on your recall adver  tisement to suit  
the communications channel you use. Always give consumers a link to the full details and recalls  
adver  tisement that is on your website or the recall notice on the Product S afet y Australia website.
E xamples of adver  tisements and communications are in our re c all communications package.
12
PDF link

## [PDF page 18]
Example:
Do you own this product?
"[Click to add: Product name]"  
"[Click to add: product identifiers]"
Dates sold: "[Click to add: dates sold]"
Why the product is recalled: "[Click to add: Text]"
Hazard:  "[Click to add: Text]"
1.  "[Click to add call to action statement]"  
2.  Send us an email or phone us if you are unable to return the product  
or have sold or gifted it to another person
Ask our staff to find out more about the recall.
[email@email.com]
"[Phone number]" Xam to Xpm Monday to Friday
Purchased from: "[Click to add: Text]"
Scan for information about this recall
[Add your own QR Code or remove if not required]
Set yourself a reminder to check at home
•  Take a photo of this notice  
•  Set a reminder on your phone
PRA [xx/  xxxx]
See productsafety.gov.au for  
Australian product recall information
13

## [PDF page 19]
Te l  l people who a re oversea s a nd g ive us a copy
Tell people you have supplied the product to, who are located outside Australia, in writing as  
soon as practical.
Tell them that the product is being recalled in Australia and describe:  
	the defect or why it is dangerous, or the use or misuse that is dangerous  
	if the product does not meet or is likely not to meet a mandator y safet y standard or is banned.
Within 10 days of informing overseas people, you must give a copy of your notice to the  
Commonwealth Minister. You can do this by emailing the notice to recallsmonitoring@accc.gov.au.
This is a requirement under the Australian Consumer L aw.
If you are coordinating the recall for other suppliers who have supplied the product to a person  
outside Australia, you need to make sure that all the suppliers meet this notification requirement.
Repor  t a ny produc t-re lated deat  h s, ser ious i nju r ies,  
or i  l  l  nesses
Submit a mandator y repor  t within 2 days of becoming aware of any death, serious injur y or  
illness associated with a consumer product you supplied.
You are required to submit a mandator y repor  t if your product has caused a death, serious injur y or  
illness, regardless of whether you have recalled the product. This is a legal requirement under the  
Australian Consumer L aw and penalties may apply if you do not repor  t or take longer than 2 days  
to repor t.
A serious illness or injur y is an acute physical injur y or illness which needs medical or surgical  
treatment by, or under the super vision of, a medical practitioner or a nurse.
A mandator y repor  t is when a supplier tells the Commonwealth Minister of a death, serious injur y  
or illness that was caused, or may have been caused, by the use or foreseeable misuse of a  
consumer product.
The ACCC accepts your mandator  y repor  t on behalf of the Commonwealth Minister.
If you need to submit a mandator y repor  t for a product you have recalled, reassess the risk and  
update your communication strategy. This includes adding a message to your recall communications  
that serious injuries have occurred.
14

## [PDF page 19]
PDF link
</excerpt>
### Rank 4 of 74 — 0.07
<excerpt title="Conducting a consumer product safety recall">
## [PDF page 73]
I n store adver  t  isi ng poster
Do you own this product?
"[Click to add: Product name]"  
"[Click to add: product identifiers]"
Dates sold: "[Click to add: dates sold]"
Why the product is recalled: "[Click to add: Text]"
Hazard:  "[Click to add: Text]"
1.  "[Click to add call to action statement]"  
2.  Send us an email or phone us if you are unable to return the product  
or have sold or gifted it to another person
Ask our staff to find out more about the recall.
[email@email.com]
"[Phone number]" Xam to Xpm Monday to Friday
Purchased from: "[Click to add: Text]"
Scan for information about this recall
[Add your own QR Code or remove if not required]
Set yourself a reminder to check at home
•  Take a photo of this notice  
•  Set a reminder on your phone
PRA [xx/  xxxx]
See productsafety.gov.au for  
Australian product recall information
68

## [PDF page 74]
SM S
Message for unk nown consumers
From: [supplier name]
PRODU CT S A FE T  Y R ECA LL :
[ produc t].
Do you own this produc t ?
[inser  t call to ac tion]
More de tails: [web address].
PRA No.[XX/XXXX]
U nsub: reply S TOP
Message for k nown consumers
From: [supplier name]
PRODU CT S A FE T  Y R ECA LL :
You bought [ produc t] from us in [MM Y  Y].
[inser  t call to ac tion]
More de tails: [web address].
PRA No.[XX/XXXX]
U nsub: reply S TOP
Understand your obligations under the S pam Act 20 03 and the Privacy Act 198 8 before sending an S MS  
to consumers.
69
PDF link  
PDF link

## [PDF page 75]
Soc ia  l med ia message
E  xa m p l e:
Does your child sleep in these pyjamas? S top using the product immediately and return it to the place  
of purchase for a full refund. [Link to recall information]
	Include a call to action and ask a question to viewers – see examples.  
	Keep your message simple with plain language, easy and shor  t words:
–  include a clear image of the recalled product  
–  add the product name  
–  describe the defect – use the approved words from your recall message  
–  refer to the maximum harm that can occur, which may mean specif ying “  death or serious  
injur y ” as the potential harm that could occur.  
	Set a sc hedule to repeat your message – your social media manager or coordinator may have  
this available for you to use.  
	Add a Learn More or C ontac t Us bu t ton if the option is available – direct consumers to the  
recall information on your website, the recall notice on the Product S afet y Australia website, or an  
online form where consumers can contact you.  
	Create a s tor y to use in addition to your social media post:
–  include your social media image  
–  ask a question to consumers (see examples)  
–  include the words: S wipe up to learn more about the recall OR S wipe up to get your refund  
–  direct consumers to the recall information on your website, or your recall notice on  
productsafet y.gov.au  
–  the swipe up option may only be available to business social media profiles with a large number  
of followers.
70
</excerpt>
### Rank 5 of 74 — 0.07
<excerpt title="Conducting a consumer product safety recall">
## [PDF page 57]
Somet  i mes a not  her gover n ment agenc  y leads t  he  
reca  l  l
Dif ferent government agencies are responsible for regulating the safet y of dif ferent t ypes of  
products including:  
	agricultural products  
	a s b e s to s  
	building and building materials  
	c he mic als  
	therapeutic goods such as medicines, complementar y medicines, medical devices and medical  
te s t s  
	electrical goods  
	food and beverages  
	gas appliances  
	road vehicles and road traffic safet y  
	smoking and tobacco  
	veterinar y chemical products.
Products that are covered by a specialist regime may also be a consumer good covered by the  
Australian C onsumer L aw.
Which agency is the lead agency
The ACCC and specialist agencies have arrangements in place to identif y which agency is the lead  
agency when a product safet y issue occurs.
52

## [PDF page 58]
Agricultural and veterinar  y produc ts, food, therapeutic goods, and road  
vehicles  
For the following products, the specialist agency, and not the ACCC, is the lead agency for the recall  
and other safet y issues.
For these products, the specialist agency :  
	assesses the recall and publishes the recall on its website  
	decides whether to inter vene in the recall and what actions to take.
The specialist agency ’s guidelines, and not these guidelines, apply to the recall. Suppliers need to  
check the specialist agency ’s recall guidelines, as updated from time to time, to understand what they  
have to do when conducting the recall.
Product  Specialist (lead) agency  Recall resources
Agricultural and  Australian Pesticides and  Re call website  
veterinar y chemical  Veterinar y Medicines Authorit y  Guidelines For re calling Agricultural and Veterinar y  
pro ducts  Chemical Products
Food  Food S tandards Australia  Re call website  
New Zealand (FS A NZ ) is the  Food Industr y Re call proto col  
coordinating authorit y working  
with the relevant state or  Noti fi cation of the re call to the AC C C is done by  
territor y food agency  FS A NZ on behalf of the food business under  taking  
the re call
Therapeutic goods  Therapeutic Goods  Re call website  
Administration  Uniform re call pro cedure for therapeutic goods
Road vehicles and  Depar tment of Infrastructure,  Re calls website  
approved road  Transpor t, Regional  Re calls policy  
vehicle par ts  Development and  
Communications  Re call notices for road vehicles and approved road  
vehicles par  ts are re ceived by the Depar  tment , and  
not the AC C C, under the Australian C onsumer L aw
53
PDF link  
PDF link  
PDF link  
PDF link  
PDF link  
PDF link  
PDF link  
PDF link  
PDF link  
PDF link  
PDF link  
PDF link
</excerpt>

## Search 7 — query: "2020 "Gas products and appliances" site:productsafety.gov.au/recalls"
### Rank 1 of 1 — 0.09 (passed on)
<excerpt title="Suburban Recreational Vehicle Water Heaters Model SW6PA, ...">
## Product description
Suburban Recreational Vehicle Water Heaters fitted to caravans, motorhomes and horse float campers.
Models:
*   SW6PA  
*   SW6DEA  
*   SW6DA  
*   SW4DEA  
*   SW4DA  
*   SW4DECA  
*   SW6DECA
Serial numbers between:
*   181315552 and 193002648 (some serial numbers may end with a 'D'), and  
*   8183311827 and 8190201139.
**How to identify affected water heaters:**Open the exterior access door to the water heater and check the model and serial number located on the right-hand side.
Manufactured between 4 April 2018 and 1 August 2019.
Sold between 1 May 2018 and 25 September 2019.
See the list of affected serial numbers in the 'Identifying features' section below.
There are 18,139 affected units.
See a list of details to help identify the product

## Reason the product is recalled
A component of the water heater may be improperly manufactured and allow carbon monoxide into your caravan, motorhome or horse float camper.

## The hazards to consumers
Carbon monoxide is a poisonous gas and can cause serious illness, injury or death. Carbon monoxide has no smell or taste, is highly flammable and can only be detected with a carbon monoxide alarm. Loss of consciousness can occur within minutes and death can occur within hours. Further information on the hazards of carbon monoxide can be viewed here.

## What consumers should do
Consumers who have not already had their unit inspected must not use the affected water heater in gas mode under any circumstances, even if they have a carbon monoxide detector.
**The remedy for this recall was updated on 29 January 2024. An inspection is no longer required, all affected water heaters that have not already been inspected will be replaced for free.**
Contact Coast to Coast Caravan and Leisure for a free replacement.
Call 02 9645 7685 or email recalls@coastrv.com.au.
Coast to Coast Caravan and Leisure will offer compensation for any additional consequential loss suffered by the consumer where there is damage or devaluation to the caravan or motorhome attributed to the installation of a replacement water heater. Consequential loss will be determined on a case by case basis.
For more information visit www.coastrv.com.au/suburban-recall.

## What consumers should do
### Who sold the product
Coast to Coast Caravan and Leisure agents and dealerships

## What consumers should do
### Dates available for sale
1 May 2018 - 25 September 2019

## What consumers should do
### Where the product was sold
Nationally
International

## Responsible regulators
Regulators are established or appointed by government. They enforce regulations and rules.
**Quote PRA number 2019/17885** when contacting a regulator about this recall.

## Responsible regulators
### Recall and remedy questions
Contact the Australian Competition and Consumer Commission if you have:
*   a question about the remedy being offered to you by the business that is responsible for managing this recall, or  
*   concerns about the way the business is managing this recall.
</excerpt>

## Search 8 — query: ""2020/" "Gas products" site:productsafety.gov.au/recalls"
### Rank 1 of 1 — 0.07 (passed on)
<excerpt title="Suburban Recreational Vehicle Water Heaters Model SW6PA, ...">
## Product description
Suburban Recreational Vehicle Water Heaters fitted to caravans, motorhomes and horse float campers.
Models:
*   SW6PA  
*   SW6DEA  
*   SW6DA  
*   SW4DEA  
*   SW4DA  
*   SW4DECA  
*   SW6DECA
Serial numbers between:
*   181315552 and 193002648 (some serial numbers may end with a 'D'), and  
*   8183311827 and 8190201139.
**How to identify affected water heaters:**Open the exterior access door to the water heater and check the model and serial number located on the right-hand side.
Manufactured between 4 April 2018 and 1 August 2019.
Sold between 1 May 2018 and 25 September 2019.
See the list of affected serial numbers in the 'Identifying features' section below.
There are 18,139 affected units.
See a list of details to help identify the product

## Reason the product is recalled
A component of the water heater may be improperly manufactured and allow carbon monoxide into your caravan, motorhome or horse float camper.

## The hazards to consumers
Carbon monoxide is a poisonous gas and can cause serious illness, injury or death. Carbon monoxide has no smell or taste, is highly flammable and can only be detected with a carbon monoxide alarm. Loss of consciousness can occur within minutes and death can occur within hours. Further information on the hazards of carbon monoxide can be viewed here.

## What consumers should do
Consumers who have not already had their unit inspected must not use the affected water heater in gas mode under any circumstances, even if they have a carbon monoxide detector.
**The remedy for this recall was updated on 29 January 2024. An inspection is no longer required, all affected water heaters that have not already been inspected will be replaced for free.**
Contact Coast to Coast Caravan and Leisure for a free replacement.
Call 02 9645 7685 or email recalls@coastrv.com.au.
Coast to Coast Caravan and Leisure will offer compensation for any additional consequential loss suffered by the consumer where there is damage or devaluation to the caravan or motorhome attributed to the installation of a replacement water heater. Consequential loss will be determined on a case by case basis.
For more information visit www.coastrv.com.au/suburban-recall.

## What consumers should do
### Who sold the product
Coast to Coast Caravan and Leisure agents and dealerships

## What consumers should do
### Dates available for sale
1 May 2018 - 25 September 2019

## What consumers should do
### Where the product was sold
Nationally
International

## Responsible regulators
Regulators are established or appointed by government. They enforce regulations and rules.
**Quote PRA number 2019/17885** when contacting a regulator about this recall.

## Responsible regulators
### Recall and remedy questions
Contact the Australian Competition and Consumer Commission if you have:
*   a question about the remedy being offered to you by the business that is responsible for managing this recall, or  
*   concerns about the way the business is managing this recall.
</excerpt>

## Search 9 — query: "site:productsafety.gov.au/recalls "recalls" "2020""
### Rank 1 of 11 — 0.16 (passed on)
<excerpt title="Toyota Corolla ZZE122 and ZZE123 MY2003-2005">
## Product description
Corolla ZZE122
Model Years 2003-2005
Front passenger side airbag
5 475 vehicles affected
Corolla ZZE123
Model Years 2003-2005
Front passenger side airbag
785 vehicles affected
All Vehicle Identification Numbers(VINs) in this recall commence with AHT
Vehicles in this recall were previously recalled for the replacement of the driver's airbag in recall PRA2017/15950 (campaign GGG30).
Total of 6 260 affected vehicles
See a list of details to help identify the product

## Reason the product is recalled
Takata airbag inflator: As it gets older, a combination of heat and humidity can cause the airbag inflator propellant to degrade. If an affected vehicle is involved in a collision triggering the airbag, the metal inflator housing may explode/rupture under too much internal pressure.

## The hazards to consumers
In the event of an airbag inflator rupture, metal fragments could propel out through the airbag cushion towards the vehicle occupants causing serious injury or fatality.

## What consumers should do
_Please Note_: Vehicles in this recall were previously recalled for the replacement of the driver's airbag in recallPRA2017/15950(campaign GGG30). Owners must now have the passenger airbag replaced.
Owners of affected vehicles are advised that the vehicle is under 'critical recall’. It is recommended that you stop driving the vehicle and immediately arrange for airbag replacement as the vehicle has a heightened risk of causing injury or death. The critical recall category applies toalpha airbagsand also includes other airbags specified by Toyota.
Toyota will offer to arrange for your vehicle to either be towed to the place of replacement or for a mobile technician to be sent to the vehicle (or some similar arrangement), so that you do not have to drive the vehicle in order to receive a replacement airbag.
Owners of affected vehicles should contact their local Toyota dealership or Toyota’s head office directly by phoning 1800 987 366 or emailing[guestexperience@toyota.com.au](mailto:guestexperience@toyota.com.au)to arrange for a replacement airbag inflator free of charge.
Consumers can use Toyota’s VIN look-up tool to see if their vehicle is affected by this recall:http://recalls.toyota.com.au/#/
Alternatively, consumers can use their registration plate number to check if their vehicle is affected by going tohttp://www.ismyairbagsafe.com.au

## What consumers should do
### Who sold the product
Toyota Motor Corporation Australia

## What consumers should do
### Dates available for sale
30 April 2003 - 30 September 2004

## What consumers should do
### Where the product was sold
Nationally

## Responsible regulators
Regulators are established or appointed by government. They enforce regulations and rules.
**Quote PRA number 2020/18579** when contacting a regulator about this recall.

## Responsible regulators
### Recall and remedy questions
Contact the Australian Competition and Consumer Commission if you have:
*   a question about the remedy being offered to you by the business that is responsible for managing this recall, or  
*   concerns about the way the business is managing this recall.
</excerpt>
### Rank 2 of 11 — 0.16
<excerpt title="669 Animal Bath Toys">
# 669 Animal Bath Toys
## Product description
Kids animal bath toys 3pcs (duck, horse and lamb)
See a list of details to help identify the product

# 669 Animal Bath Toys
## Reason the product is recalled
The product does not comply with the permanent ban on children's products containing more than 1% diethylhexyl phthalate (DEHP). These products are banned under the 'Consumer Protection Notice No. 11 of 2011, Permanent Ban on Children's Products containing more than 1% diethylhexyl phthalate (DEHP)'.
DEHP is a commonly used plasticiser that is used to make plastics such as polyvinyl chloride (PVC) soft and flexible.

# 669 Animal Bath Toys
## The hazards to consumers
A risk of reproductive toxicity exists for young children if they extensively chew or suck on objects with unsafe levels of DEHP.

# 669 Animal Bath Toys
## What consumers should do
Consumers should cease using the product and return it to the place of purchase for a full refund.
For more information, consumers can contact T&C Wholesale Pty Ltd on 03 9555 8943 or via email service@tangs.com.au

# 669 Animal Bath Toys
## Details to help identify the product
### Who is running the recall
T&C Wholesale Pty Ltd

# 669 Animal Bath Toys
## Details to help identify the product
### Who sold the product
Discount variety stores

# 669 Animal Bath Toys
## Details to help identify the product
### Identifying numbers


# 669 Animal Bath Toys
## Details to help identify the product
### Other identifying numbers
669-004A

# 669 Animal Bath Toys
## Details to help identify the product
### Dates available for sale
8 July 2019 - 4 March 2020

# 669 Animal Bath Toys
## Details to help identify the product
### Where the product was sold
Victoria

# 669 Animal Bath Toys
## Print supporting information
Recall advertisement.pdf 1.62 MB

# 669 Animal Bath Toys
## Responsible regulators
Regulators are established or appointed by government. They enforce regulations and rules.
**Quote PRA number 2020/18292** when contacting a regulator about this recall.

# 669 Animal Bath Toys
## Responsible regulators
### Recall and remedy questions
Contact the Australian Competition and Consumer Commission if you have:
*   a question about the remedy being offered to you by the business that is responsible for managing this recall, or  
*   concerns about the way the business is managing this recall.

# 669 Animal Bath Toys
## Is this page useful?
Yes  No
Thanks for your feedback.
ACCC Product Safety on TwitterACCC Product Safety on FacebookACCC Product Safety on YouTubeACCC Instagram
The ACCC acknowledges the Traditional Custodians of the lands across Australia on which we live and work. We acknowledge their connection to this Country and pay our respect to Elders past, present and emerging.

# 669 Animal Bath Toys
## Footer menu
*   Accessibility  
*   Cookies  
*   Disclaimer and copyright  
*   Glossary  
*   Vulnerability disclosure  
*   Privacy
×
Close
원본 텍스트
번역 평가
보내주신 의견은 Google 번역을 개선하는 데 사용됩니다.
</excerpt>
### Rank 3 of 11 — 0.15
<excerpt title="669 Animal Bath Toys">
# 669 Animal Bath Toys | ACCC Product Safety
Skip to contentSkip to navigationSkip to search
Top utilities
*   News  
*   Contact
Related sites
*   ACCC  
*   Scamwatch
번역에서 제공
Search Menu
Search (required)
Search

# 669 Animal Bath Toys | ACCC Product Safety
*   Consumers Expand submenu for "Consumers"  
    *   Know your product safety rights  
        *   Search all consumer guides  
        *   Shop online for products that are safe  
        *   Buy safe second-hand products online

    *   Respond to recalls and unsafe products  
        *   Report an unsafe product  
        *   What to do when a product is recalled  
        *   Search product recalls

    *   Keep baby safe  
        *   Bathe and change baby  
        *   Feed and soothe baby  
        *   Move baby  
        *   Play with baby  
        *   Settle baby to sleep

    *   Drive and ride safely  
    *   Use cosmetic and fashion products safely  
    *   Play and exercise safely  
        *   Kids' toys  
        *   Sport, exercise and play equipment

    *   Be safe around the home  
        *   Batteries and technology  
        *   Garden and outdoor products  
        *   Products inside the home

    *   Handle chemicals and poisons safely

*   Business Expand submenu for "Business"  
    *   Understand product safety rules  
        *   Product safety laws and liability  
        *   Product safety as a consumer guarantee  
        *   Standards and how to comply  
        *   Bans and how to comply  
        *   Recalls and the role of government

    *   Search mandatory standards  
    *   Find banned products  
    *   Supplier guides  
    *   Know how to sell safe products  
        *   Sell safe products online  
        *   Sell safe second-hand products online  
        *   Second-hand products sold through online marketplaces  
        *   Source and test products  
        *   Develop a compliance program

    *   Recall an unsafe product  
    *   Make a mandatory report  
    *   Submit a voluntary report  
    *   Fines and penalties  
    *   E-bikes, e-scooters and e-micromobility devices

*   Search product recalls  
*   About us Expand submenu for "About us"  
    *   About the ACCC  
    *   Product safety priorities  
    *   The product safety system  
    *   Improving mandatory standards  
    *   Product safety news  
        *   News  
        *   Receive email alerts  
        *   Subscribe for product safety news  
        *   Subscribe to RSS feeds

# 669 Animal Bath Toys | ACCC Product Safety
    *   Product safety consultations  
    *   Publications  
    *   Online product safety pledge  
    *   Our campaigns  
    *   Contact us
Breadcrumb
1.   Home  
2.   Search product recalls
Listen

# 669 Animal Bath Toys
T&C Wholesale Pty Ltd

# 669 Animal Bath Toys
### Recall published
24 April 2020

# 669 Animal Bath Toys
### PRA number
2020/18292

# 669 Animal Bath Toys
### Topics
Chemicals and poisons
Diethylhexylphthalate DEHP (toxic substance)
Kids' toys
Bath toys
Toys for babies and toddlers

# 669 Animal Bath Toys
## Product description
Kids animal bath toys 3pcs (duck, horse and lamb)
See a list of details to help identify the product
</excerpt>
### Rank 4 of 11 — 0.10
<excerpt title="Suburban Recreational Vehicle Water Heaters Model SW6PA, ...">
## Product description
Suburban Recreational Vehicle Water Heaters fitted to caravans, motorhomes and horse float campers.
Models:
*   SW6PA  
*   SW6DEA  
*   SW6DA  
*   SW4DEA  
*   SW4DA  
*   SW4DECA  
*   SW6DECA
Serial numbers between:
*   181315552 and 193002648 (some serial numbers may end with a 'D'), and  
*   8183311827 and 8190201139.
**How to identify affected water heaters:**Open the exterior access door to the water heater and check the model and serial number located on the right-hand side.
Manufactured between 4 April 2018 and 1 August 2019.
Sold between 1 May 2018 and 25 September 2019.
See the list of affected serial numbers in the 'Identifying features' section below.
There are 18,139 affected units.
See a list of details to help identify the product

## Reason the product is recalled
A component of the water heater may be improperly manufactured and allow carbon monoxide into your caravan, motorhome or horse float camper.

## The hazards to consumers
Carbon monoxide is a poisonous gas and can cause serious illness, injury or death. Carbon monoxide has no smell or taste, is highly flammable and can only be detected with a carbon monoxide alarm. Loss of consciousness can occur within minutes and death can occur within hours. Further information on the hazards of carbon monoxide can be viewed here.

## What consumers should do
Consumers who have not already had their unit inspected must not use the affected water heater in gas mode under any circumstances, even if they have a carbon monoxide detector.
**The remedy for this recall was updated on 29 January 2024. An inspection is no longer required, all affected water heaters that have not already been inspected will be replaced for free.**
Contact Coast to Coast Caravan and Leisure for a free replacement.
Call 02 9645 7685 or email recalls@coastrv.com.au.
Coast to Coast Caravan and Leisure will offer compensation for any additional consequential loss suffered by the consumer where there is damage or devaluation to the caravan or motorhome attributed to the installation of a replacement water heater. Consequential loss will be determined on a case by case basis.
For more information visit www.coastrv.com.au/suburban-recall.

## What consumers should do
### Who sold the product
Coast to Coast Caravan and Leisure agents and dealerships

## What consumers should do
### Dates available for sale
1 May 2018 - 25 September 2019

## What consumers should do
### Where the product was sold
Nationally
International

## Responsible regulators
Regulators are established or appointed by government. They enforce regulations and rules.
**Quote PRA number 2019/17885** when contacting a regulator about this recall.

## Responsible regulators
### Recall and remedy questions
Contact the Australian Competition and Consumer Commission if you have:
*   a question about the remedy being offered to you by the business that is responsible for managing this recall, or  
*   concerns about the way the business is managing this recall.
</excerpt>
### Rank 5 of 11 — 0.08
<excerpt title="Boppy Hug and Nest Newborn Lounger">
# Boppy Hug and Nest Newborn Lounger
## The hazards to consumers
The baby or child may suffocate, which can lead to severe injury or death.

# Boppy Hug and Nest Newborn Lounger
## What consumers should do
Consumers should stop using the product and return it to the place of purchase or BPM Australia for a full refund.
For more information, consumers can contact their place of purchase, or BPM Australia Pty Ltd on
02 9457 0000 (Mon-Fri, 9am-5pm AEST), via email at customerservice@mybpm.com.au or go to www.chicco.com.au

# Boppy Hug and Nest Newborn Lounger
## Details to help identify the product
### Who is running the recall
BPM Australia Pty Ltd

# Boppy Hug and Nest Newborn Lounger
## Details to help identify the product
### Who sold the product
Sold instore and online at children's stores and expos, including:
Amazon AU
Baby Junction
Babyland
Better Than Sox
Button & Wheel
Big W
eBay
Chicco
Matty's Toys and Baby
The Nile
Tiny Fox
Unanderra Pharmacy
Whole Bubs

# Boppy Hug and Nest Newborn Lounger
## Details to help identify the product
### Identifying product features
Ref: 07 079939 470 000
Code: 79939
Barcode:8058664076710

# Boppy Hug and Nest Newborn Lounger
## Details to help identify the product
### Dates available for sale
9 December 2020 - 16 September 2021

# Boppy Hug and Nest Newborn Lounger
## Details to help identify the product
### Where the product was sold
Nationally
Online

# Boppy Hug and Nest Newborn Lounger
## Details to help identify the product
### Manufacturer country ID
Romania

# Boppy Hug and Nest Newborn Lounger
## Print supporting information
Recall advertisement.pdf 124.54 KB

# Boppy Hug and Nest Newborn Lounger
## Responsible regulators
Regulators are established or appointed by government. They enforce regulations and rules.
**Quote PRA number 2021/19205** when contacting a regulator about this recall.

# Boppy Hug and Nest Newborn Lounger
## Responsible regulators
### Recall and remedy questions
Contact the Australian Competition and Consumer Commission if you have:
*   a question about the remedy being offered to you by the business that is responsible for managing this recall, or  
*   concerns about the way the business is managing this recall.

# Boppy Hug and Nest Newborn Lounger
## Is this page useful?
Yes  No
Thanks for your feedback.
ACCC Product Safety on TwitterACCC Product Safety on FacebookACCC Product Safety on YouTubeACCC Instagram
The ACCC acknowledges the Traditional Custodians of the lands across Australia on which we live and work. We acknowledge their connection to this Country and pay our respect to Elders past, present and emerging.

# Boppy Hug and Nest Newborn Lounger
## Footer menu
*   Accessibility  
*   Cookies  
*   Disclaimer and copyright  
*   Glossary  
*   Vulnerability disclosure  
*   Privacy
×
Close
원본 텍스트
번역 평가
보내주신 의견은 Google 번역을 개선하는 데 사용됩니다.
</excerpt>

## Search 10 — query: ""Gas products and appliances" "recall" 2020 site:productsafety.gov.au/recalls"
### Rank 1 of 1 — 0.12 (passed on)
<excerpt title="Suburban Recreational Vehicle Water Heaters Model SW6PA, ...">
## Product description
Suburban Recreational Vehicle Water Heaters fitted to caravans, motorhomes and horse float campers.
Models:
*   SW6PA  
*   SW6DEA  
*   SW6DA  
*   SW4DEA  
*   SW4DA  
*   SW4DECA  
*   SW6DECA
Serial numbers between:
*   181315552 and 193002648 (some serial numbers may end with a 'D'), and  
*   8183311827 and 8190201139.
**How to identify affected water heaters:**Open the exterior access door to the water heater and check the model and serial number located on the right-hand side.
Manufactured between 4 April 2018 and 1 August 2019.
Sold between 1 May 2018 and 25 September 2019.
See the list of affected serial numbers in the 'Identifying features' section below.
There are 18,139 affected units.
See a list of details to help identify the product

## Reason the product is recalled
A component of the water heater may be improperly manufactured and allow carbon monoxide into your caravan, motorhome or horse float camper.

## The hazards to consumers
Carbon monoxide is a poisonous gas and can cause serious illness, injury or death. Carbon monoxide has no smell or taste, is highly flammable and can only be detected with a carbon monoxide alarm. Loss of consciousness can occur within minutes and death can occur within hours. Further information on the hazards of carbon monoxide can be viewed here.

## What consumers should do
Consumers who have not already had their unit inspected must not use the affected water heater in gas mode under any circumstances, even if they have a carbon monoxide detector.
**The remedy for this recall was updated on 29 January 2024. An inspection is no longer required, all affected water heaters that have not already been inspected will be replaced for free.**
Contact Coast to Coast Caravan and Leisure for a free replacement.
Call 02 9645 7685 or email recalls@coastrv.com.au.
Coast to Coast Caravan and Leisure will offer compensation for any additional consequential loss suffered by the consumer where there is damage or devaluation to the caravan or motorhome attributed to the installation of a replacement water heater. Consequential loss will be determined on a case by case basis.
For more information visit www.coastrv.com.au/suburban-recall.

## What consumers should do
### Who sold the product
Coast to Coast Caravan and Leisure agents and dealerships

## What consumers should do
### Dates available for sale
1 May 2018 - 25 September 2019

## What consumers should do
### Where the product was sold
Nationally
International

## Responsible regulators
Regulators are established or appointed by government. They enforce regulations and rules.
**Quote PRA number 2019/17885** when contacting a regulator about this recall.

## Responsible regulators
### Recall and remedy questions
Contact the Australian Competition and Consumer Commission if you have:
*   a question about the remedy being offered to you by the business that is responsible for managing this recall, or  
*   concerns about the way the business is managing this recall.
</excerpt>

For each search, read the top excerpt and the ones ranked below it, and judge whether the order is right for answering the question. An excerpt holding the answer, or a fact that leads to it, should outrank one that only repeats the query's words or covers the topic without a checkable fact. If none of the excerpts holds anything useful, that is the search's fault, not this instruction's. Find the ranking error that cost the most and write a new instruction that fixes it. Replace or compress existing text where you can; avoid making it much longer. Do not write the "Original question" or "Search query" lines; they are appended for you. Do not copy any fact, name, site or topic from these examples.

Provide the new instruction within ``` blocks.
