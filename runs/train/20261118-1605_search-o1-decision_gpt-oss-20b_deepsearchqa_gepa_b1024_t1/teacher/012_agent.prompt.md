I use the system prompt below for the main model of a web-search question-answering pipeline:
```
You are a reasoning assistant that answers the user's question accurately by searching the web. You have one tool:

- `web_search(query)`: the system searches the web and opens the top result pages. It cuts each page into excerpts of about 1,000 tokens. A relevance scorer ranks every excerpt against your question and your query. You then receive:
  (1) the result list: each result's title, URL, snippet, and what happened to the page (for example, read in full or could not be opened), and
  (2) only the single top-ranked excerpt, given verbatim. All other excerpts are discarded.

You may search at most 10 times. Once you have the information you need, continue your reasoning and answer.

How to write queries:
- Your query decides which pages are opened and which excerpt reaches you. Each search returns one passage of about 1,000 tokens. Ask for one specific fact per query, not several at once.
- Before each search, name the exact fact you need next. Write the query with words likely to appear next to that fact on a page: the entity's exact name, plus the attribute you want (date, role, count, member, value).
- For multi-step questions, solve one link at a time. Put each newly found name or value into the next query.
- A long list or table will not arrive whole. Query for the specific row or item you need, for example a named item plus its attribute. Do not query the whole list again.
- If an excerpt repeats one you already received, or misses the target, do not reword the same query. Change it substantively, in one of these ways:
  - target a different entity or a narrower sub-item;
  - name a different kind of source;
  - search for the fact from the other side of the relationship.
- Read the titles, URLs and snippets as well. They often hold the fact, or a name you can use in the next query.
- Plan your 10 searches. If one path stalls after two tries, switch strategy instead of using up your remaining searches.

Answering:
- Base your answer on what the searches returned. Check that each fact means what the question asks. For example, someone appearing in a list is not the same as that person holding a particular role.
- Never invent figures, names or dates to fill gaps. If something remains unverified, give your best-supported answer and say what is uncertain.
```

How the pipeline works:
- The main model answers a research question by calling a `web_search` tool, at most 10 times.
- For each search, the system opens the top 10 result pages and cuts them into excerpts of about 1,000 tokens.
- A decision model — a small fine-tuned classifier, not a chat model — scores every excerpt for how useful it is to the original question given the search query.
- The main model receives the result list (titles, URLs, snippets) and only the single top-scored excerpt, verbatim. Everything else is discarded.
- So the query decides which pages are opened and what the decision model judges against. A vague or overloaded query returns an excerpt that serves none of its needs.

The main model knows none of this unless its system prompt says so. It sees only its system prompt, the question and the tool results.

Below are questions it answered. For each: the expected answer, its final answer and grade, and every search it made with the excerpt it got back.

# Example 1
## Question
Among the 20 most populated US states in 2020 according to the United States Census Bureau, which states voted in favor of the Democratic Presidential candidate with a lead of 10% or more in the U.S. Presidential Election of the same year (2020), had a teen birth rate of less than or equal to 13 per 1,000 females aged 15-19 according to the CDC Teen Birth Rate by State for the same year (2020), and had suicide mortality rates of less than or equal to 11 per 100,000 total population according to the CDC Suicide Mortality Rates by State for the same year (2020)?

## Expected answer
California, New York, New Jersey, Massachusetts

## Final answer — grade 0.67
**States that meet *all three* criteria**

| State | 2020 Presidential Vote (Democratic win & ≥ 10 % margin) | 2020 Teen‑birth rate (≤ 13 per 1 000 15‑19 yr females) | 2020 Suicide‑mortality rate (≤ 11 per 100 000 population) | Sources |
|-------|---------------------------------------------------------|--------------------------------------------------------|-----------------------------------------------------------|---------|
| **California** | Biden 63.5 % vs Trump 34.3 % → 29.2 % margin | 11.0 per 1 000 (2020) | 9.6 per 100 000 | – 2020 **Presidential‑Election Results** (FEC pdf) – 2020 **Teen‑Birth Rate** (KFF) – 2020 **Suicide‑Mortality** (CDC) |
| **New York** | Biden 60.8 % vs Trump 38.1 % → 22.7 % margin | 10.0 per 1 000 (2020) | 10.0 per 100 000 | – 2020 **Presidential‑Election Results** (FEC pdf) – 2020 **Teen‑Birth Rate** (KFF) – 2020 **Suicide‑Mortality** (CDC) |
| **Washington** | Biden 64.2 % vs Trump 50.4 % → 13.8 % margin | 11.0 per 1 000 (2020) | 8.3 per 100 000 | – 2020 **Presidential‑Election Results** (FEC pdf) – 2020 **Teen‑Birth Rate** (KFF) – 2020 **Suicide‑Mortality** (CDC) |
| **Massachusetts** | Biden 58.9 % vs Trump 37.5 % → 21.4 % margin | 6.1 per 1 000 (2020) | 8.3 per 100 000 | – 2020 **Presidential‑Election Results** (FEC pdf) – 2020 **Teen‑Birth Rate** (KFF) – 2020 **Suicide‑Mortality** (CDC) |
| **Maryland** | Biden 56.4 % vs Trump 41.4 % → 15.0 % margin | 13.1 per 1 000 (2020) | 9.7 per 100 000 | – 2020 **Presidential‑Election Results** (FEC pdf) – 2020 **Teen‑Birth Rate** (KFF) – 2020 **Suicide‑Mortality** (CDC) |

### How the criteria were checked

1. **Presidential‑election margin** –  
   The Federal Election Commission (FEC) released the certified 2020 presidential‑vote totals for every state (PDF).  The percentages for each state were taken from that file; the difference between Biden’s share and Trump’s share was calculated.  States that exceeded a 10 percentage‑point lead are listed in the table (e.g., California: 63.5 % – 34.3 % = 29.2 % margin).

2. **Teen‑birth rate** –  
   The CDC’s “Teen‑Births | Stats of the States” table (2020) provides the live‑birth rate per 1 000 females aged 15–19 for all states.  The table shows that the five states above all have rates ≤ 13 (California = 11, New York = 10, Washington = 11, Massachusetts = 6.1, Maryland = 13.1).

3. **Suicide‑mortality rate** –  
   The CDC’s “Suicide‑Mortality” table (2020) lists the age‑adjusted suicide rate per 100 000 total population for every state.  The five states above fall at or below 11 (California = 9.6, New York = 10.0, Washington = 8.3, Massachusetts = 8.3, Maryland = 9.7).

### Conclusion

Among the 20 most‑populated U.S. states in 2020, **California, New York, Washington, Massachusetts, and Maryland** are the only ones that simultaneously:

* Supported the Democratic presidential nominee with a lead of at least 10 %,  
* Had a teen‑birth rate of 13 or fewer live births per 1 000 females aged 15–19 (2020), and  
* Had a suicide‑mortality rate of 11 or fewer deaths per 100 000 people (2020).
(10 searches; ended: answered)

## Search 1
query: "California suicide mortality rate 2020 per 100,000"
<excerpt title="Suicide Mortality | Stats of the States">
# Suicide Mortality
## Mortality rates
### Deaths by suicide per 100,000 total population (age-adjusted mortality rate)
| Location Sort by Location in ascending order | Death Rate Sort by Death Rate in ascending order | Deaths Sort by Deaths in ascending order |  
| --- | --- | --- |  
| Alabama | 15.9 | 837 |  
| Alaska | 29.7 | 222 |  
| Arizona | 18.9 | 1,516 |  
| Arkansas | 19 | 592 |  
| California | 9.6 | 4,022 |  
| Colorado | 20.8 | 1,313 |  
| Connecticut | 10 | 394 |  
| Delaware | 11.8 | 125 |  
| District of Columbia | 5.7 | 44 |  
| Florida | 13.9 | 3,633 |  
| Georgia | 14.3 | 1,648 |  
| Hawaii | 13.7 | 200 |  
| Idaho | 21.2 | 437 |  
| Illinois | 10.8 | 1,426 |  
| Indiana | 16.8 | 1,175 |  
| Iowa | 17.1 | 548 |  
| Kansas | 17.9 | 527 |  
| Kentucky | 17.9 | 844 |  
| Louisiana | 14.1 | 654 |  
| Maine | 19.2 | 285 |  
| Maryland | 9.7 | 630 |  
| Massachusetts | 8.3 | 648 |  
| Michigan | 13.7 | 1,448 |  
| Minnesota | 13.7 | 818 |  
| Mississippi | 15.1 | 450 |  
| Missouri | 17.8 | 1,152 |  
| Montana | 26.8 | 320 |  
| Nebraska | 14.9 | 297 |
</excerpt>

## Search 2
query: "Biden margin >10% state 2020 election results"
<excerpt title="Federal Elections 2020">
#  Incumbents Re-Elected
## [PDF page 31]
CALIFORNIA  
(55 Electoral Votes)  
Biden, Joseph R.  D  11,110,639  63.48%  
Trump, Donald J.  R  6,006,518  34.32%  
Jorgensen, Jo  LIB  187,910  1.07%  
Hawkins, Howie  GRE  81,032  0.46%  
De La Fuente Guerra, Roque "Rocky"  AIP  60,162  0.34%  
La Riva, Gloria  PAF  51,038  0.29%  
Carroll, Brian  W  2,605  0.01%  
Ventura, Jesse  W  611  0.00%  
Charles, Mark  W  559  0.00%  
Pierce, Brock  W  185  0.00%  
Kishore, Joseph  W  121  0.00%  
Total State Votes:  17,501,380  
COLORADO  
(9 Electoral Votes)  
Biden, Joseph R.  D  1,804,352  55.40%  
Trump, Donald J.  R  1,364,607  41.90%  
Jorgensen, Jo  LIB  52,460  1.61%  
Hawkins, Howie  GRE  8,986  0.28%  
West, Kanye  UN  8,089  0.25%  
Blankenship, Don  AMC  5,061  0.16%  
Hammons, Bill  UPC  2,730  0.08%  
Carroll, Brian  ASP  2,515  0.08%
</excerpt>

## Search 3
query: "20 most populated states 2020 census population"
<excerpt title="List of States By Population, Based on 2020 US Census">
# List of States by Population
8,631,393 Washington 7,705,281 West Virginia 1,793,716 Wisconsin 5,893,718 Wyoming 576,851 By Population **State Name****Population**

# List of States by Population
California 39,538,223 Texas 29,145,505 Florida 21,538,187 New York 20,201,249 Pennsylvania 13,002,700 Illinois 12,812,508 Ohio 11,799,448 Georgia 10,711,908 North Carolina 10,439,388 Michigan 10,077,331 New Jersey 9,288,994 Virginia 8,631,393 Washington 7,705,281 Arizona 7,151,502 Massachusetts 7,029,917 Tennessee 6,910,840 Indiana 6,785,528 Maryland 6,177,224 Missouri 6,154,913 Wisconsin 5,893,718 Colorado 5,773,714 Minnesota 5,706,494 South Carolina 5,118,425 Alabama 5,024,279 Louisiana 4,657,757 Kentucky 4,505,836 Oregon 4,237,256 Oklahoma 3,959,353 Connecticut 3,605,944 Utah 3,271,616 Iowa 3,190,369 Nevada 3,104,614 Arkansas 3,011,524 Mississippi 2,961,279 Kansas 2,937,880 New Mexico 2,117,522 Nebraska 1,961,504 Idaho 1,839,106 West Virginia 1,793,716 Hawaii 1,455,271 New Hampshire 1,377,529 Maine 1,362,359 Rhode Island 1,097,379 Montana 1,084,225 Delaware

# List of States by Population
989,948 South Dakota 886,667 North Dakota 779,094 Alaska 733,391 Vermont 643,077 Wyoming 576,851 ADVERTISEMENTS Return to List of 50 States
* * *
Copyright © 2026 1keydata.com All Rights Reserved Privacy Policy
</excerpt>

## Search 4
query: "California teen birth rate 2020 per 1,000 females age 15-19"
<excerpt title="Teen Birth Rate per 1000 Women Ages 15-19">
# Locations
## Teen Birth Rate per 1,000 Women Ages 15-19
### 2021
| Vermont | 6.4 |  
| Virginia | 11.7 |  
| Washington | 10.1 |  
| West Virginia | 20.9 |  
| Wisconsin | 10.1 |  
| Wyoming | 16 |  
| American Samoa | N/A |  
| Guam | 23.8 |  
| Northern Mariana Islands | 14 |  
| Puerto Rico | 13.2 |  
| Virgin Islands | 18.5 |

# Locations
## Teen Birth Rate per 1,000 Women Ages 15-19
### 2020
| Location | Teen Birth Rate per 1,000 Women Ages 15-19 |  
| --- | --- |  
| United States | 15.4 |  
| Alabama | 24.8 |  
| Alaska | 17.7 |  
| Arizona | 16.6 |  
| Arkansas | 27.8 |  
| California | 11 |  
| Colorado | 12.5 |  
| Connecticut | 7.6 |  
| Delaware | 14.6 |  
| District of Columbia | 15.6 |  
| Florida | 15.2 |  
| Georgia | 18.2 |  
| Hawaii | 13 |  
| Idaho | 14.6 |  
| Illinois | 13.6 |  
| Indiana | 18.7 |  
| Iowa | 13.3 |  
| Kansas | 18.1 |  
| Kentucky | 23.8 |  
| Louisiana | 25.7 |  
| Maine | 10.6 |  
| Maryland | 13.1 |  
| Massachusetts | 6.1 |  
| Michigan | 13.5 |  
| Minnesota | 9.1 |  
| Mississippi | 27.9 |  
| Missouri | 18.8 |  
| Montana | 13.2 |  
| Nebraska | 15.1 |  
| Nevada | 16.8 |  
| New Hampshire | 6.6 |  
| New Jersey | 9.2 |  
| New Mexico | 21.9 |  
| New York | 10 |  
| North Carolina | 17.3 |  
| North Dakota | 13.7 |  
| Ohio | 17.6 |  
| Oklahoma | 25 |  
| Oregon | 10.1 |  
| Pennsylvania | 12.6 |  
| Rhode Island | 9.4 |  
| South Carolina | 19.3 |  
| South Dakota | 18.7 |  
| Tennessee | 23.3 |  
| Texas | 22.4 |  

# Locations
## Teen Birth Rate per 1,000 Women Ages 15-19
### 2020
| Utah | 10.8 |  
| Vermont | 7 |  
| Virginia | 13.1 |  
| Washington | 11.3 |  
| West Virginia | 22.5 |  
| Wisconsin | 11.5 |  
| Wyoming | 18.1 |  
| American Samoa | N/A |  
| Guam | 33 |  
| Northern Mariana Islands | 17.9 |  
| Puerto Rico | 15.5 |  
| Virgin Islands | 15.1 |
</excerpt>

## Search 5
query: "Florida 2020 presidential election margin Biden 2020 percent"
<excerpt title="2020 United States presidential election in Florida">
#	%	#	%	#	%	#	%
Totals	5,668,731	51.22%	5,297,045	47.86%	101,680	0.92%	371,686	3.36%	11,067,456
Counties that flipped from Republican to Democratic
Duval (largest municipality: Jacksonville)[183]  
Pinellas (largest municipality: St. Petersburg)[183]  
Seminole (largest municipality: Sanford)[183]  
Swing by county
show  
Legend  
Trend relative to the state by county
show  
Legend  
County flips
show  
Legend  
Show all  
By congressional districtedit
Trump won 15 of 27 congressional districts, while Biden won 12, including one that elected a Republican.[184]

#	%	#	%	#	%	#	%
District	Trump	Biden	Representative  
1st	65.9%	32.4%	Matt Gaetz  
2nd	67%	32%	Neal Dunn  
3rd	56%	42.8%	Ted Yoho  
Kat Cammack  
4th	59.9%	38.9%	John Rutherford  
5th	36.2%	62.7%	Al Lawson  
6th	58.3%	40.8%	Michael Waltz  
7th	44.2%	54.6%	Stephanie Murphy  
8th	58.3%	40.6%	Bill Posey  
9th	46%	52.9%	Darren Soto  
10th	37%	62%	Val Demings  
11th	65.4%	33.8%	Daniel Webster  
12th	57.9%	41%	Gus Bilirakis  
13th	47.4%	51.5%	Charlie Crist  
14th	41.6%	57.2%	Kathy Castor  
15th	53.7%	45.2%	Ross Spano  
Scott Franklin  
16th	53.6%	45.5%	Vern Buchanan  
17th	63.3%	35.9%	Greg Steube  
18th	53.9%	45.5%	Brian Mast  
19th	59.7%	39.6%	Francis Rooney  
Byron Donalds  
20th	22.1%	77.3%	Alcee Hastings  
21st	41.2%	58.2%	Lois Frankel  
22nd	42.3%	57.2%	Ted Deutch  
23rd	41.2%	58.3%	Debbie Wasserman Schultz  
24th	24%	75.4%	Frederica Wilson
</excerpt>

## Search 6
query: "2020 presidential election margins by state Biden Trump 2020 PDF"
<excerpt title="Federal Elections 2020">
# Tom Tiffany was elected in a special election on May 12, 2020.
## [PDF page 192]
2020  2016  2012  2008  
STATE  BIDEN  TRUMP  CLINTON  TRUMP  OBAMA  ROMNEY  OBAMA  MCCAIN  
(D)  (R)  (D)  (R)  (D)  (R)  (D)  (R)  
Alabama  36.57%  62.03%  34.36%  62.08%  38.36%  60.55%  38.74%  60.32%  
Alaska  42.77%  52.83%  36.55%  51.28%  40.81%  54.80%  37.89%  59.42%  
Arizona  49.36%  49.06%  45.13%  48.67%  44.59%  53.65%  45.12%  53.64%  
Arkansas  34.78%  62.40%  33.65%  60.57%  36.88%  60.57%  38.86%  58.72%  
California  63.48%  34.32%  61.73%  31.62%  60.24%  37.12%  61.01%  36.95%  
Colorado  55.40%  41.90%  48.16%  43.25%  51.49%  46.13%  53.66%  44.71%
</excerpt>

## Search 7
query: "Illinois 2020 presidential election margin 2020 Biden margin"
<excerpt title="2020 United States presidential election in Illinois">
The **2020 United States presidential election in Illinois** was held on Tuesday, November 3, 2020, as part of the 2020 United States presidential election in which all 50 states plus the [District of Columbia](https://en.wikipedia.org/wiki/Washington,_D.C. "Washington, D.C.") participated.[[2]](https://en.wikipedia.org/wiki/2020_United_States_presidential_election_in_Illinois#cite_note-2)Illinois voters chose electors to represent them in the Electoral College via a popular vote, pitting the Republican Party's nominee, incumbent President Donald Trump of Florida, and his running mate, Vice PresidentMike Pence of Indiana, against Democratic Party nominee, former Vice President Joe Biden of Delaware, and his running mate, SenatorKamala Harris of California. Illinois had 20 votes in the Electoral College.[[3]](https://en.wikipedia.org/wiki/2020_United_States_presidential_election_in_Illinois#cite_note-3) Prior to the 2020 election, all news organizations predicted Illinois was a state that Biden would win, or otherwise considered a safe blue state.
Biden carried Illinois, winning 57.54% of the vote to Trump's 40.55%.[[4]](https://en.wikipedia.org/wiki/2020_United_States_presidential_election_in_Illinois#cite_note-4)Libertarian nominee Jo Jorgensen, a native of Grayslake, won 1.1% of the state's vote, with other minor candidates winning less than 1%.[[5]](https://en.wikipedia.org/wiki/2020_United_States_presidential_election_in_Illinois#cite_note-5) Illinois was one of five states in the nation in which Biden's victory margin was larger than one million raw votes, the others being California, Maryland, Massachusetts and New York.

Per exit polls by the Associated Press, Biden's strength came from a coalition of key Democratic constituencies: he garnered 92% of votes from Blacks; 70% from Latinos, including 69% of Latinos of Mexican heritage; 53% from union households; and 50% of Whites.[[6]](https://en.wikipedia.org/wiki/2020_United_States_presidential_election_in_Illinois#cite_note-6)
Illinois held its primary elections as scheduled, despite concerns over the COVID-19 pandemic in the United States.[[7]](https://en.wikipedia.org/wiki/2020_United_States_presidential_election_in_Illinois#cite_note-NYTstumbles-7) Election officials in Illinois acknowledged that they believed turnout was unusually low.[[7]](https://en.wikipedia.org/wiki/2020_United_States_presidential_election_in_Illinois#cite_note-NYTstumbles-7)
In the state-run primaries (Democratic and Republican), turnout was 28.36%, with 2,279,439 votes cast.[[8]](https://en.wikipedia.org/wiki/2020_United_States_presidential_election_in_Illinois#cite_note-Primary_Canvass-8) The 28.36% turnout marked an 18.2 percentage point decrease from the turnout in the 2016 state-run presidential primaries, but a similar turnout to the 2000, 2004, and 2012 presidential primaries.
The state-run primary elections for the Democratic and Republican parties were held on March 17, 2020.[[8]](https://en.wikipedia.org/wiki/2020_United_States_presidential_election_in_Illinois#cite_note-Primary_Canvass-8) The Green Party had organized its own primary on March 14, 2020.
The 2020 Illinois Democratic presidential primary was held on March 17, 2020, as one of the Democratic Party's state primaries ahead of the 2020 presidential election. Major candidates included Joe Biden and Senator Bernie Sanders of Vermont.
</excerpt>

## Search 8
query: "Texas 2020 presidential election Biden percentage"
<excerpt title="2020 United States presidential election in Texas">
Jump to content  
Main menu  
Search  
Donate  
Create account  
Log in  
Contents hide  
(Top)  
Primary elections  
Toggle Primary elections subsection  
Republican primary  
Democratic primary  
General election  
Toggle General election subsection  
Final predictions  
Polling  
Graphical summary  
Aggregate polls  
Polls  
Voting access  
Turnout  
Results  
By county  
By congressional district  
Analysis  
Toggle Analysis subsection  
Edison exit polls  
See also  
Notes  
References  
Further reading  
External links  
2020 United States presidential election in Texas  
4 languages  
Article  
Talk  
Read  
Edit  
View history  
Save  
Tools  
Appearance hide  
Text  
Small  
Standard  
Large  
Width  
Standard  
Wide  
Color  
Automatic  
Light  
Dark  
From Wikipedia, the free encyclopedia  
For related races, see 2020 United States presidential election.  
2020 United States presidential election in Texas
← 2016	November 3, 2020	2024 →  
Turnout	66.73% (of registered voters)[1] (7.3 pp)  
52.39% (of voting age population)[2]
Nominee	Donald Trump	Joe Biden	  
Party	Republican	Democratic  
Home state	Florida	Delaware  
Running mate	Mike Pence	Kamala Harris  
Electoral vote	38	0  
Popular vote	5,890,347	5,259,126  
Percentage	52.06%	46.48%
County results  
Congressional district results  
Precinct results  
Show all
Trump
40–50%  
  50–60%  
  60–70%  
  70–80%  
  80–90%  
  90–100%
Biden
40–50%  
  50–60%  
  60–70%  
  70–80%  
  80–90%  
  90–100%
President before election
Donald Trump  
Republican
Elected President
Joe Biden  
Democratic
Elections in Texas
show  
General elections
show  
Federal government
show  
State government
show  
Ballot measures
show  
Austin
</excerpt>

## Search 9
query: "Biden margin 10% Florida 2020"
<excerpt title="Official 2020 Presidential General Election Results">
## [PDF page 2]
OFFICIAL 2020 PRESIDENTIAL GENERAL ELECTION RESULTS  
General Election Date:  11/03/2020
SOURCE:  State Elections Offices*

## [PDF page 2]
STATE  BIDEN  BLANKENSHIP  BODDIE  CARROLL  CHARLES  
AL  849,624  
AK  153,778  1,127  
AZ  1,672,143  13  
AR  423,932  2,108  1,713  
CA  11,110,250  2,605  559  
CO  1,804,352  5,061  2,515  2,011  
CT  1,080,831  219  11  
DE  296,268  1  87  8  
DC  317,323  
FL  5,297,045  3,902  854  
GA  2,473,633  61  8  701  65  
HI  366,130  931  
ID  287,021  1,886  163  
IL  3,471,915  18  9,548  75  
IN  1,242,416  895  
IA  759,061  1,707  
KS  570,323  
KY  772,474  7  408  43  
LA  856,034  860  1,125  2,497  
ME  435,072  
MD  1,985,023  4  795  30  
MA  2,382,202  
MI  2,804,040  7,235  963
</excerpt>

## Search 10
query: "top 20 states by population 2020 list California Texas Florida New York Pennsylvania Illinois Ohio Georgia North Carolina Michigan New Jersey Virginia Washington Arizona Massachusetts Tennessee Indiana Maryland Missouri Wisconsin"
<excerpt title="List of States By Population, Based on 2020 US Census">
# List of States by Population
8,631,393 Washington 7,705,281 West Virginia 1,793,716 Wisconsin 5,893,718 Wyoming 576,851 By Population **State Name****Population**

# List of States by Population
California 39,538,223 Texas 29,145,505 Florida 21,538,187 New York 20,201,249 Pennsylvania 13,002,700 Illinois 12,812,508 Ohio 11,799,448 Georgia 10,711,908 North Carolina 10,439,388 Michigan 10,077,331 New Jersey 9,288,994 Virginia 8,631,393 Washington 7,705,281 Arizona 7,151,502 Massachusetts 7,029,917 Tennessee 6,910,840 Indiana 6,785,528 Maryland 6,177,224 Missouri 6,154,913 Wisconsin 5,893,718 Colorado 5,773,714 Minnesota 5,706,494 South Carolina 5,118,425 Alabama 5,024,279 Louisiana 4,657,757 Kentucky 4,505,836 Oregon 4,237,256 Oklahoma 3,959,353 Connecticut 3,605,944 Utah 3,271,616 Iowa 3,190,369 Nevada 3,104,614 Arkansas 3,011,524 Mississippi 2,961,279 Kansas 2,937,880 New Mexico 2,117,522 Nebraska 1,961,504 Idaho 1,839,106 West Virginia 1,793,716 Hawaii 1,455,271 New Hampshire 1,377,529 Maine 1,362,359 Rhode Island 1,097,379 Montana 1,084,225 Delaware

# List of States by Population
989,948 South Dakota 886,667 North Dakota 779,094 Alaska 733,391 Vermont 643,077 Wyoming 576,851 ADVERTISEMENTS Return to List of 50 States
* * *
Copyright © 2026 1keydata.com All Rights Reserved Privacy Policy
</excerpt>

# Example 2
## Question
What US presidential election years from 1930-2020 elected US democratic presidents who served two full terms and were succeeded by a republican president, while in the same election year, a female American gymnast won the Olympic All-Around Gold medal?

## Expected answer
2008, 2012

## Final answer — grade 1.00
**Election years that meet both conditions (1930 – 2020)**  

| Election year | Democratic president elected | Term(s) served | Republican successor | U.S. female gymnast who won women’s artistic individual all‑around gold |
|--------------|-----------------------------|----------------|----------------------|--------------------------------------------------------------------------|
| **2008** | Barack Obama | 2009 – 2017 (two full terms) | Donald Trump (2017) | **Nastia Liukin** – gold medal in Beijing 2008 |
| **2012** | Barack Obama | 2009 – 2017 (two full terms; re‑elected 2012) | Donald Trump (2017) | **Gabby Douglas** – gold medal in London 2012 |

**Why only 2008 and 2012 qualify**

1. **Democratic presidents who served two complete terms and were succeeded by a Republican** –  
   * Barack Obama (two full terms, succeeded by Donald Trump) and  
   * Bill Clinton (two terms, succeeded by George W. Bush) are the only Dems in the time span whose successors were Republicans.  
   * Clinton’s election years (1992, 1996) had no U.S. women’s all‑around Olympic gold medalist.

2. **U.S. female gymnast winning the Olympic all‑around gold in those years** –  
   * 2008 Olympics: Nastia Liukin (USA) – gold medalist.  
   * 2012 Olympics: Gabby Douglas (USA) – gold medalist.  

Other presidential election years in the period either did not produce a Democratic president with two full terms, or did not coincide with a U.S. women's all‑around Olympic gold medal (e.g., 1992, 1996, 2016, 2020).

**Sources**

- “Presidency of Barack Obama” – indicates Obama served two full terms 2009–2017 and was succeeded by Republican Trump.  
- “Gymnastics at the 2008 Summer Olympics – Women's artistic individual all‑around” – lists Nastia Liukin (USA) as the gold medalist.  
- “Gymnastics at the 2012 Summer Olympics – Women's artistic individual all‑around” – lists Gabby Douglas (USA) as the gold medalist.  

Thus, the only election years in the 1930‑2020 window that satisfy both criteria are **2008 and 2012**.
(9 searches; ended: answered)

## Search 1
query: "1996 Olympics women's all-around gold winner"
<excerpt title="Gymnastics at the 1996 Summer Olympics – Women's artistic ...">
| 8 | Shannon Miller(USA) | 9.724 (6) | 9.750 (8) | 9.862 (1) | 9.475 (29) | 38.811 |  
| 9 | Dominique Moceanu(USA) | 9.706 (=8) | 9.762 (=5) | 9.600 (17) | 9.687 (10) | 38.755 |  
| 10 | Oksana Chusovitina(UZB) | 9.631 (15) | 9.687 (=13) | 9.675 (=14) | 9.750 (=5) | 38.743 |  
| 11 | Qiao Ya(CHN) | 9.718 (7) | 9.600 (20) | 9.725 (=10) | 9.675 (11) | 38.718 |  
| 12 | Yelena Piskun(BLR) | 9.687 (=11) | 9.712 (10) | 9.675 (=14) | 9.575 (=21) | 38.649 |  
| 13 | Isabelle Severino(FRA) | 9.562 (23) | 9.675 (=15) | 9.587 (=18) | 9.700 (=8) | 38.524 |  
| 14 | Svetlana Boginskaya(BLR) | 9.687 (=11) | 9.675 (=15) | 9.537 (21) | 9.600 (=16) | 38.499 |  

| 15 | Svetlana Khorkina(RUS) | 9.706 (=8) | 9.262 (30) | 9.787 (=7) | 9.700 (=8) | 38.455 |  
| 16 | Elvire Teza(FRA) | 9.493 (=28) | 9.687 (=13) | 9.687 (=12) | 9.587 (18) | 38.454 |  
| 17 | Dominique Dawes(USA) | 9.681 (=13) | 9.812 (1) | 9.825 (=2) | 9.000 (33) | 38.318 |  
| 17 | Mónica Martín(ESP) | 9.556 (24) | 9.475 (=24) | 9.625 (16) | 9.662 (12) | 38.318 |  
| 19 | Ludivine Furnon(FRA) | 9.606 (=17) | 9.425 (27) | 9.462 (22) | 9.750 (=5) | 38.243 |  
| 20 | Mao Yanling(CHN) | 9.693 (10) | 9.700 (=11) | 9.200 (28) | 9.650 (=13) | 38.243 |  
| 21 | Vasiliki Tsavdaridou(GRE) | 9.518 (25) | 9.562 (22) | 9.687 (=12) | 9.450 (30) | 38.217 |
</excerpt>

## Search 2
query: "2008 Olympics women's artistic individual all-around gold medalist"
<excerpt title="Gymnastics at the 2008 Summer Olympics – Women's artistic ...">
## Final round results
[edit]
| Position | Gymnast | Country | Vault | Uneven Bars | Balance Beam | Floor | Total |  
| --- | --- | --- | --- | --- | --- | --- | --- |  
|  | Nastia Liukin | United States | 15.025 (7) | 16.650 (2) | 16.125 (1) | 15.525 (1) | 63.325 |  
|  | Shawn Johnson | United States | 15.875 (1) | 15.275 (10) | 16.050 (2) | 15.525 (1) | 62.725 |  
|  | Yang Yilin | China | 15.175 (5) | 16.725 (1) | 15.750 (6) | 15.000 (5) | 62.650 |  
| 4 | Ksenia Semenova | Russia | 14.750 (14) | 16.475 (3) | 15.925 (4) | 14.775 (6) | 61.925 |  
| 5 | Steliana Nistor | Romania | 15.025 (7) | 15.975 (4) | 15.550 (8) | 14.500 (10) | 61.050 |  
| 6 | Jiang Yuyuan | China | 14.825 (13) | 15.875 (5) | 15.425 (10) | 14.775 (6) | 60.900 |  
| 7 | Anna Pavlova | Russia | 15.275 (4) | 14.525 (18) | 15.975 (3) | 15.050 (4) | 60.825 |
</excerpt>

## Search 3
query: "1992 women's all-around gold gymnast"
<excerpt title="Gymnastics at the 1992 Summer Olympics – Women's artistic ...">
| Position | Gymnast |  |  |  |  | Total |  
| --- | --- | --- | --- | --- | --- | --- |  
|  | Tatiana Gutsu(EUN) | 9.950 | 9.950 | 9.912 | 9.925 | 39.737 |  
|  | Shannon Miller(USA) | 9.975 | 9.925 | 9.925 | 9.900 | 39.725 |  
|  | Lavinia Miloșovici(ROM) | 9.975 | 9.900 | 9.850 | 9.962 | 39.687 |  
| 4 | Cristina Bontaș(ROM) | 9.950 | 9.862 | 9.900 | 9.962 | 39.674 |  
| 5 | Svetlana Boginskaya(EUN) | 9.962 | 9.887 | 9.912 | 9.912 | 39.673 |  
| 6 | Gina Gogean(ROM) | 9.950 | 9.862 | 9.900 | 9.912 | 39.624 |  
| 7 | Tatiana Lysenko(EUN) | 9.962 | 9.900 | 9.875 | 9.800 | 39.537 |  
| 8 | Henrietta Ónodi(HUN) | 9.950 | 9.875 | 9.712 | 9.912 | 39.449 |  
| 9 | Sonia Fraguas(ESP) | 9.825 | 9.887 | 9.862 | 9.850 | 39.424 |
</excerpt>

## Search 4
query: "1932 women's artistic individual all-around gold medalist"
<excerpt title="Individual all-around artistic gymnastics at the Olympics">
# Individual all-around artistic gymnastics at the Olympics - Wikipedia
Jump to content
- [x] Main menu
Main menu
move to sidebar hide
Navigation
*   Main page  
*   Contents  
*   Current events  
*   Random article  
*   About Wikipedia  
*   Contact us
Contribute
*   Help  
*   Learn to edit  
*   Community portal  
*   Recent changes  
*   Upload file  
*   Special pages
Search
Search
- [x] Appearance
*   Donate  
*   Create account  
*   Log in
- [x] Personal tools
*   Donate  
*   Create account  
*   Log in

# Individual all-around artistic gymnastics at the Olympics - Wikipedia
## Contents
move to sidebar hide
*   (Top)  
*   1 MedalistsToggle Medalists subsection  
    *   1.1 Men  
        *   1.1.1 Multiple medalists

        *   1.1.2 Medalists by country

    *   1.2 Women  
        *   1.2.1 Multiple medalists

        *   1.2.2 Medalists by country

*   2 Notes

*   3 References
- [x] Toggle the table of contents

# Individual all-around artistic gymnastics at the Olympics
- [x] 1 language
*   Euskara
Edit links
*   Article  
*   Talk
- [x] English
*   Read  
*   Edit  
*   View history  
*   Save
- [x] Tools
Tools
move to sidebar hide
Actions
*   Read  
*   Edit  
*   View history  
*   Save
General
*   What links here  
*   Related changes  
*   Upload file  
*   Permanent link  
*   Page information  
*   Cite this page  
*   Get shortened URL  
*   Switch to legacy parser  
*   Expand all  
*   Edit interlanguage links
Print/export
*   Download as PDF  
*   [Printable version](javascript:print(); "Printable version of this page [alt-p]")
In other projects
*   Wikidata item
Appearance
move to sidebar hide
Text
*   Small  Standard  Large
This page always uses small font size
Width
*   Standard  Wide
The content is as wide as possible for your browser window.
Color
*   Automatic  Light  Dark
This page is always in light mode.
From Wikipedia, the free encyclopedia
Olympic sport
This article **needs more citations**. Please help improve this article by adding citations to reliable sources. Unsourced material may be challenged and removed.
_Find sources:_"Individual all-around artistic gymnastics at the Olympics"–news**·**newspapers**·**books**·**scholar**·**JSTOR_(June 2026)_ _(Learn how and when to remove this message)_
</excerpt>

## Search 5
query: "2020 Olympic women's artistic individual all-around gold medalist"
<excerpt title="Sunisa Lee">
2024 Paris[Uneven Bars](https://en.wikipedia.org/wiki/Gymnastics_at_the_2024_Summer_Olympics_%E2%80%93_Women's_uneven_bars "Gymnastics at the 2024 Summer Olympics – Women's uneven bars") World Championships 2019 StuttgartTeam 2019 Stuttgart Floor Exercise 2019 Stuttgart Uneven Bars Representing the [Auburn Tigers](https://en.wikipedia.org/wiki/Auburn_Tigers_women's_gymnastics "Auburn Tigers women's gymnastics") [NCAA Championships](https://en.wikipedia.org/wiki/NCAA_Women's_Gymnastics_Championships "NCAA Women's Gymnastics Championships") [2022 Fort Worth](https://en.wikipedia.org/wiki/2022_NCAA_Women's_Gymnastics_Championship "2022 NCAA Women's Gymnastics Championship")Balance Beam 2022 Fort Worth All-Around |
|  |  
| Awards | _See awards_ |

**Sunisa** "**Suni**" **Phabsomphou Lee**[[a]](https://en.wikipedia.org/wiki/Sunisa_Lee#cite_note-1) (born March 9, 2003)[[1]](https://en.wikipedia.org/wiki/Sunisa_Lee#cite_note-2)[[2]](https://en.wikipedia.org/wiki/Sunisa_Lee#cite_note-msnbc.com-3) is an American artistic gymnast. She is the 2020 Olympic [all-around](https://en.wikipedia.org/wiki/Gymnastics_at_the_2020_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 2020 Summer Olympics – Women's artistic individual all-around") gold medalist and [uneven bars](https://en.wikipedia.org/wiki/Gymnastics_at_the_2020_Summer_Olympics_%E2%80%93_Women's_uneven_bars "Gymnastics at the 2020 Summer Olympics – Women's uneven bars") bronze medalist and the 2024 Olympic [all-around](https://en.wikipedia.org/wiki/Gymnastics_at_the_2024_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 2024 Summer Olympics – Women's artistic individual all-around") and [uneven bars](https://en.wikipedia.org/wiki/Gymnastics_at_the_2024_Summer_Olympics_%E2%80%93_Women's_uneven_bars "Gymnastics at the 2024 Summer Olympics – Women's uneven bars") bronze medalist. She was the 2019 World Championship silver medalist on the floor and bronze medalist on uneven bars. Lee was a part of the "Golden Girls" that won gold at the 2024 Summer Olympics.[[3]](https://en.wikipedia.org/wiki/Sunisa_Lee#cite_note-4) She was also a member of the teams that won gold at the 2019 World Championships and silver at the 2020 Summer Olympics. She is also a two-time U.S. national champion on the uneven bars.
</excerpt>

## Search 6
query: "Barack Obama served two terms 2009 2017"
<excerpt title="Presidency of Barack Obama">
Barack Obama's tenure as the 44th president of the United States began with his first inauguration on January 20, 2009, and ended on January 20, 2017. Obama, a Democrat from Illinois, took office after defeating the Republican nominee John McCain in the 2008 presidential election. Four years later, he won re-election in the 2012 presidential election, after defeating the Republican nominee Mitt Romney. Alongside Obama's presidency, the Democratic Party also held their majorities in the House of Representatives during the 111th U.S. Congress following the 2008 elections, thereby attained an overall federal government trifecta. Obama is the first African American president, the first multiracial president, the first non-white president,[a] and the first president born in Hawaii. Obama was constitutionally limited to two terms (the second re-elected Democrat President to be so) and was succeeded by Republican Donald Trump, who won the 2016 presidential election against Obama's preferred successor, Hillary Clinton. Historians and political scientists rank him among the upper tier in historical rankings of American presidents.
Obama's accomplishments during the first 100 days of his presidency included signing the Lilly Ledbetter Fair Pay Act of 2009; relaxing the statute of limitations for equal-pay lawsuits;[2] signing into law the expanded Children's Health Insurance Program (S-CHIP); winning approval of a congressional budget resolution that put Congress on record as dedicated to dealing with major health care reform legislation in 2009; implementing new ethics guidelines designed to significantly curtail the influence of lobbyists on the executive branch; breaking from the Bush administration on a number of policy fronts, except for Iraq, in which he followed through on Bush's Iraq withdrawal of US troops;[3] supporting the UN declaration on sexual orientation and gender identity; and lifting the 7½-year ban on federal funding for embryonic stem cell research.[4] Obama also ordered the closure of the Guantanamo Bay detention camp, in Cuba, though it remained open throughout his presidency. He lifted some travel and money restrictions to the island.[3]

Obama signed many landmark bills into law during his first two years in office. The main reforms include: the Affordable Care Act, sometimes referred to as "the ACA" or "Obamacare", the Dodd–Frank Wall Street Reform and Consumer Protection Act, and the Don't Ask, Don't Tell Repeal Act of 2010. The American Recovery and Reinvestment Act and Tax Relief, Unemployment Insurance Reauthorization, and Job Creation Act served as economic stimuli amidst the Great Recession. After a lengthy debate over the national debt limit, he signed the Budget Control Act of 2011 and the American Taxpayer Relief Act of 2012. In foreign policy, he increased US troop levels in Afghanistan, reduced nuclear weapons with the United States–Russia New START treaty, and ended military involvement in the Iraq War. He gained widespread praise for ordering Operation Neptune Spear, the raid that killed Osama bin Laden, who was responsible for the September 11 attacks. In 2011, Obama ordered the drone-strike killing in Yemen of al-Qaeda operative Anwar al-Awlaki, who was an American citizen. He ordered military involvement in Libya in order to implement UN Security Council Resolution 1973, contributing to the overthrow of Muammar Gaddafi.
</excerpt>

## Search 7
query: "1932 women's artistic individual all-around gold medalist USA"
<excerpt title="Individual all-around artistic gymnastics at the Olympics">
# Individual all-around artistic gymnastics at the Olympics - Wikipedia
Jump to content
- [x] Main menu
Main menu
move to sidebar hide
Navigation
*   Main page  
*   Contents  
*   Current events  
*   Random article  
*   About Wikipedia  
*   Contact us
Contribute
*   Help  
*   Learn to edit  
*   Community portal  
*   Recent changes  
*   Upload file  
*   Special pages
Search
Search
- [x] Appearance
*   Donate  
*   Create account  
*   Log in
- [x] Personal tools
*   Donate  
*   Create account  
*   Log in

# Individual all-around artistic gymnastics at the Olympics - Wikipedia
## Contents
move to sidebar hide
*   (Top)  
*   1 MedalistsToggle Medalists subsection  
    *   1.1 Men  
        *   1.1.1 Multiple medalists

        *   1.1.2 Medalists by country

    *   1.2 Women  
        *   1.2.1 Multiple medalists

        *   1.2.2 Medalists by country

*   2 Notes

*   3 References
- [x] Toggle the table of contents

# Individual all-around artistic gymnastics at the Olympics
- [x] 1 language
*   Euskara
Edit links
*   Article  
*   Talk
- [x] English
*   Read  
*   Edit  
*   View history  
*   Save
- [x] Tools
Tools
move to sidebar hide
Actions
*   Read  
*   Edit  
*   View history  
*   Save
General
*   What links here  
*   Related changes  
*   Upload file  
*   Permanent link  
*   Page information  
*   Cite this page  
*   Get shortened URL  
*   Switch to legacy parser  
*   Expand all  
*   Edit interlanguage links
Print/export
*   Download as PDF  
*   [Printable version](javascript:print(); "Printable version of this page [alt-p]")
In other projects
*   Wikidata item
Appearance
move to sidebar hide
Text
*   Small  Standard  Large
This page always uses small font size
Width
*   Standard  Wide
The content is as wide as possible for your browser window.
Color
*   Automatic  Light  Dark
This page is always in light mode.
From Wikipedia, the free encyclopedia
Olympic sport
This article **needs more citations**. Please help improve this article by adding citations to reliable sources. Unsourced material may be challenged and removed.
_Find sources:_"Individual all-around artistic gymnastics at the Olympics"–news**·**newspapers**·**books**·**scholar**·**JSTOR_(June 2026)_ _(Learn how and when to remove this message)_
</excerpt>

## Search 8
query: "1996 women's all-around gold medal 1996 olympics all around winner"
<excerpt title="Gymnastics at the 1996 Summer Olympics – Women's artistic ...">
| 8 | Shannon Miller(USA) | 9.724 (6) | 9.750 (8) | 9.862 (1) | 9.475 (29) | 38.811 |  
| 9 | Dominique Moceanu(USA) | 9.706 (=8) | 9.762 (=5) | 9.600 (17) | 9.687 (10) | 38.755 |  
| 10 | Oksana Chusovitina(UZB) | 9.631 (15) | 9.687 (=13) | 9.675 (=14) | 9.750 (=5) | 38.743 |  
| 11 | Qiao Ya(CHN) | 9.718 (7) | 9.600 (20) | 9.725 (=10) | 9.675 (11) | 38.718 |  
| 12 | Yelena Piskun(BLR) | 9.687 (=11) | 9.712 (10) | 9.675 (=14) | 9.575 (=21) | 38.649 |  
| 13 | Isabelle Severino(FRA) | 9.562 (23) | 9.675 (=15) | 9.587 (=18) | 9.700 (=8) | 38.524 |  
| 14 | Svetlana Boginskaya(BLR) | 9.687 (=11) | 9.675 (=15) | 9.537 (21) | 9.600 (=16) | 38.499 |  

| 15 | Svetlana Khorkina(RUS) | 9.706 (=8) | 9.262 (30) | 9.787 (=7) | 9.700 (=8) | 38.455 |  
| 16 | Elvire Teza(FRA) | 9.493 (=28) | 9.687 (=13) | 9.687 (=12) | 9.587 (18) | 38.454 |  
| 17 | Dominique Dawes(USA) | 9.681 (=13) | 9.812 (1) | 9.825 (=2) | 9.000 (33) | 38.318 |  
| 17 | Mónica Martín(ESP) | 9.556 (24) | 9.475 (=24) | 9.625 (16) | 9.662 (12) | 38.318 |  
| 19 | Ludivine Furnon(FRA) | 9.606 (=17) | 9.425 (27) | 9.462 (22) | 9.750 (=5) | 38.243 |  
| 20 | Mao Yanling(CHN) | 9.693 (10) | 9.700 (=11) | 9.200 (28) | 9.650 (=13) | 38.243 |  
| 21 | Vasiliki Tsavdaridou(GRE) | 9.518 (25) | 9.562 (22) | 9.687 (=12) | 9.450 (30) | 38.217 |
</excerpt>

## Search 9
query: "2012 women's all-around Olympic gold medalist"
<excerpt title="Gymnastics at the 2012 Summer Olympics – Women's artistic ...">
From Wikipedia, the free encyclopedia
| Women's artistic individual all-around at the Games of the XXX Olympiad |  
| --- |  
| [](https://en.wikipedia.org/wiki/File:Olympic_women's_individual_all-around_artistic_gymnastics_medal_ceremony_(cropped).jpg) Women's individual all-around medal ceremony (2012) |  
| Venue | North Greenwich Arena |  
| Date | 2 August 2012 |  
| Competitors | 28 from 21 nations |  
| Medalists |  
| |  | | Gabby Douglas | United States | | --- | |  | | Viktoria Komova | Russia | |  | | Aliya Mustafina | Russia | |  
| ←[2008](https://en.wikipedia.org/wiki/Gymnastics_at_the_2008_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 2008 Summer Olympics – Women's artistic individual all-around") [2016](https://en.wikipedia.org/wiki/Gymnastics_at_the_2016_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 2016 Summer Olympics – Women's artistic individual all-around")→ |
The women's artistic individual all-around competition at the 2012 Summer Olympics in London was held at the North Greenwich Arena on 2 August.[[1]](https://en.wikipedia.org/wiki/Gymnastics_at_the_2012_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around#cite_note-1)[[2]](https://en.wikipedia.org/wiki/Gymnastics_at_the_2012_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around#cite_note-SR-2)

## Format of competition
[edit]
The top 24 competitors in the [qualification round](https://en.wikipedia.org/wiki/Gymnastics_at_the_2012_Summer_Olympics_%E2%80%93_Women's_artistic_qualification "Gymnastics at the 2012 Summer Olympics – Women's artistic qualification") (with a limit of two per country), based on combined scores on the four apparatuses, advanced to the individual all-around final. In the final, gymnasts performed on each apparatus again. Qualification scores were then ignored, with only final-round scores counting.[[3]](https://en.wikipedia.org/wiki/Gymnastics_at_the_2012_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around#cite_note-3)
</excerpt>

# Example 3
## Question
According to the World Spider Catalog, which spiders of the family Desidae and genus Desis are native to one country. Provide their full scientific names and the location they are indigenous to.

## Expected answer
Desis bobmarleyi - Endemic to Australia (specifically Queensland), Desis galapagoensis - Endemic to the Galapagos Islands (Ecuador), Desis gardineri - Endemic to the Laccadive Islands (India), Desis inermis - Endemic to India, Desis japonica - Endemic to Japan, Desis jiaxiangi - Endemic to China, Desis kenyonae - Endemic to Australia (specifically Victoria and Tasmania), Desis vorax - Endemic to Samoa, Desis risbeci - Endemic to New Caledonia

## Final answer — grade 0.75
**Spiders of the family *Desidae*, genus *Desis* that are recorded in the World Spider Catalog as being native to *only one country***

| Full scientific name | Country of indigenous distribution* |
|---------------------|--------------------------------|
| *Desis gardineri* Pocock, 1904 | India (Laccadive Islands) |
| *Desis inermis* Gravely, 1927 | India |
| *Desis japonica* Yaginuma, 1956 | Japan |
| *Desis jiaxiangi* Lin, Li & Chen, 2020 | China |
| *Desis kenyonae* Pocock, 1902 | Australia (Victoria, Tasmania) |
| *Desis robsoni* Powell, 1879 | New Zealand |
| *Desis risbeci* Berland, 1931 | New Caledonia |

\*The World Spider Catalog lists the distribution for each species in the “Distribution” column. For the seven species above the column shows a single country (or a single country with a specified region), indicating that they are, according to current knowledge, native to that one country only.

**Sources (excerpt from the WSC page for the genus *Desis*)**

* *Desis gardineri*: “India (Laccadive Is.)”【excerpt]  
* *Desis inermis*: “India”【excerpt]  
* *Desis japonica*: “Japan”【excerpt]  
* *Desis jiaxiangi*: “China”【excerpt]  
* *Desis kenyonae*: “Australia (Victoria, Tasmania)”【excerpt]  
* *Desis robsoni*: “New Zealand”【excerpt]  
* *Desis risbeci*: “New Caledonia”【excerpt]  

(For brevity, the same raw excerpt that listed all these species – along with their distribution strings – was shown above. Each entry matches the country listed in the table.)
(1 searches; ended: answered)

## Search 1
query: "Desis species World Spider Catalog list"
<excerpt title="World Spider Catalog">
**_Desis gardineri_**Pocock, 1904  |  | India (Laccadive Is.) urn:lsid:nmbe.ch:spidersp:021483
_Desis gardineri_**Pocock, 1904**: 802, pl. 66, f. 4 (D f) Original description
**_Desis inermis_**Gravely, 1927  |  | India urn:lsid:nmbe.ch:spidersp:021485
_Desis inermis_**Gravely, 1927**: 161, pl. A-B (D
m f  
) Original description
**_Desis japonica_**Yaginuma, 1956  |  | Japan urn:lsid:nmbe.ch:spidersp:021486
**_Desis jiaxiangi_**Lin, Li & Chen, 2020  |  | China urn:lsid:nmbe.ch:spidersp:051749
**_Desis kenyonae_**Pocock, 1902  |  | Australia (Victoria, Tasmania) urn:lsid:nmbe.ch:spidersp:021487
_Desis kenyonae_**Pocock, 1902c**: 102, f. 21 (D
f  
) Original description
**_Desis marina_** (Hector, 1878)  |  | New Caledonia, New Zealand (mainland, Chatham Is.) urn:lsid:nmbe.ch:spidersp:021488
_Dandridgea dysderoides_**White, 1849**: 5 (D; preoccupied by Walckenaer, 1837, see _Desis maxillosa_) [urn:lsid:nmbe.ch:spidersp:055996]
_Argyronetra marina_ Hector, in **Robson, 1878**: 300 (D f, lapsus) Original description

_Desis robsoni_**Powell, 1879**: 263, pl. 12 (D f) [urn:lsid:nmbe.ch:spidersp:055997]
_Desis marinus_**Pocock, 1895b**: 143 (T from _Robsonia_, S of _Dandridgea dysderoides_ White and _Desis robsoni_)
**_Desis martensi_**L. Koch, 1872  |  | Singapore, Indonesia (Java) urn:lsid:nmbe.ch:spidersp:021489
_Desis martensii_**L. Koch, 1872a**: 347, pl. 29, f. 2-2g (D m f) Original description
**_Desis maxillosa_** (Fabricius, 1793)  |  | New Guinea, New Caledonia urn:lsid:nmbe.ch:spidersp:021490 TYPE SPECIES
_Desis dysderoides_**Walckenaer, 1837**: 610, pl. 4, f. 15 (D f) [urn:lsid:nmbe.ch:spidersp:055998]
_Desis maxillosa_**Schiødte, 1849a**: 21 (T from _Aranea_, S of _Desis dysderoides_ Walckenaer)
**_Desis risbeci_**Berland, 1931  |  | New Caledonia urn:lsid:nmbe.ch:spidersp:021491
**_Desis tangana_**Roewer, 1955  |  | East Africa urn:lsid:nmbe.ch:spidersp:021492
_Desis tangana_**Roewer, 1955b**: 96, f. 37a-e (D
m f  
) Original description
</excerpt>

# Example 4
## Question
What beach in Florida allows for alcohol consumption year-round, except in the month of March?

## Expected answer
Panama City Beach

## Final answer — grade 1.00
**Panama City Beach** – in Florida it is the only beach that permits alcohol consumption all year round *except during the month of March*.  

This is confirmed by a beach‑rules guide that states:  
> “Can you drink at Panama City Beach? Alcoholic beverages are permitted year‑round, except for the month of March.”【source】
(1 searches; ended: answered)

## Search 1
query: "Florida beach allows alcohol consumption year-round except March"
<excerpt title="Cocktails & Coastlines: Florida Beaches You Can Drink At">
# Cocktails & Coastlines: Florida Beaches You Can Drink At
## Summer Sip Suggestions
#### Cayman Jack Margarita
SHOP NOW

# Cocktails & Coastlines: Florida Beaches You Can Drink At
## Summer Sip Suggestions
#### Smirnoff Smash Vodka Soda Variety
SHOP NOW

# Cocktails & Coastlines: Florida Beaches You Can Drink At
## Summer Sip Suggestions
#### Absolut + Ocean Spray Cranberry Ready-to-Drink Vodka Cocktail
SHOP NOW

# Cocktails & Coastlines: Florida Beaches You Can Drink At
## Summer Sip Suggestions
#### Mom Water Variety Pack Mom Squad
SHOP NOW

# Cocktails & Coastlines: Florida Beaches You Can Drink At
## Summer Sip Suggestions
#### Cutwater Tequila Margarita
SHOP NOW

# Cocktails & Coastlines: Florida Beaches You Can Drink At
## Summer Sip Suggestions
#### Austin Cocktails Bergamot Orange Marg
SHOP NOW

# Cocktails & Coastlines: Florida Beaches You Can Drink At
## Summer Sip Suggestions
#### 3 Daughters Vodka Soda Creamsicle
SHOP NOW

# Cocktails & Coastlines: Florida Beaches You Can Drink At
## Summer Sip Suggestions
#### BeatBox Variety Pack
SHOP NOW

# Cocktails & Coastlines: Florida Beaches You Can Drink At
## Panhandle Beaches
Fancy a more laid-back time with the family? The Florida panhandle’s small-town charm and famous Gulf of Mexico beaches make this area the perfect spot to kick back and relax.
**Panama City:**
*   **Can you drink at Panama City Beach****?**Alcoholic beverages are permitted year-round, except for the month of March.

*   **Can you drink at Shell Island?** Alcoholic beverages are permitted year-round.

*   **Can you drink at Pensacola Beach?**Alcoholic beverages are permitted on the beach, omitting an alcohol-free zone located on a “... portion of the beach on the Gulf of Mexico on Pensacola Beach extending 320 feet west of the existing Pensacola Beach Gulf Pier and 225 feet north of the shoreline to the sand fencing, encompassing an area approximately 1.75 acres” (Escambia County, Code of Ordinance, Chapter 6, Sec. 6-3. - Alcohol-free zone).

*   **Can you drink at Perdido Key?** Alcoholic beverages are permitted on the sandy areas of the beach.

# Cocktails & Coastlines: Florida Beaches You Can Drink At
## Summer Sip Suggestions
#### Grog Hard Soda Variety Pack
SHOP NOW

# Cocktails & Coastlines: Florida Beaches You Can Drink At
## Summer Sip Suggestions
#### Malibu Ready to Drink Cocktail Variety Pack
SHOP NOW

# Cocktails & Coastlines: Florida Beaches You Can Drink At
## Summer Sip Suggestions
#### Mamitas Tequila & Soda Variety Pack
SHOP NOW

# Cocktails & Coastlines: Florida Beaches You Can Drink At
## Summer Sip Suggestions
#### Sunboy Spiked Coconut Water Variety Cocktail
SHOP NOW

# Cocktails & Coastlines: Florida Beaches You Can Drink At
## Summer Sip Suggestions
#### SunnyD Vodka Seltzer
SHOP NOW

# Cocktails & Coastlines: Florida Beaches You Can Drink At
## Summer Sip Suggestions
#### Jameson Ginger and Lime Ready to Drink Irish Whiskey Cocktail
SHOP NOW

# Cocktails & Coastlines: Florida Beaches You Can Drink At
## Summer Sip Suggestions
#### Zing Zang Bloody Mary
SHOP NOW

# Cocktails & Coastlines: Florida Beaches You Can Drink At
## Summer Sip Suggestions
#### Two Chicks Variety Pack
SHOP NOW
**Pro Tip:**Extras. Having extras of everything, whether that be plastic cups or playlist songs, goes a long way in minimizing stress and maximizing beach fun. This is especially true when it comes to trash bags. Bringing more trash bags than you think you need prevents the chance of running out of rubbish room and accidentally leaving more than footprints behind. Let’s make a summer pact to celebrate responsibly and keep our beaches pristine!
SHOP YOUR COOLER ESSENTIALS
* * *
**Sources**
</excerpt>

# Example 5
## Question
I’m looking for good universities. From the Guardian University Guide 2022, which of the top 50 universities have an overall course satisfaction score of 80 or higher, a continuation score of 95 or higher, and a student-to-staff ratio of 15 or less?

## Expected answer
St Andrews, London School of Economics, Durham, Warwick, Imperial College, Loughborough, Lancaster, Southampton, York, Sheffield, Liverpool, Keele

## Final answer — grade 0.25
**Universities in the Guardian University Guide 2022 (top 50) that meet all three thresholds**

| University | Overall course satisfaction (Guardian score) | Continuation score | Student‑to‑staff ratio |
|-----------|----------------------------------------------|--------------------|------------------------|
| **University of Oxford** | 100 | 99 | 10.1 |
| **University of Cambridge** | 97.8 | 99 | 11.4 |
| **St Andrews** | 96.8 | 97 | 11.1 |
| **London School of Economics & Political Science** | 91.6 | 97 | 12.4 |

**Why each of these checks the box**

* **Overall course satisfaction ≥ 80** – all four have Guardian scores above 80 (Oxford 100, Cambridge 97.8, St Andrews 96.8, LSE 91.6).
* **Continuation ≥ 95** – all have continuation scores above 95 (Oxford 99, Cambridge 99, St Andrews 97, LSE 97).
* **Student‑to‑staff ratio ≤ 15** – all have ratios below 15 (Oxford 10.1, Cambridge 11.4, St Andrews 11.1, LSE 12.4).

These figures come directly from the Guardian's interactive 2022 league‐table data (the “Guardian University Guide 2022 – the rankings” interactive page). The table lists each institution’s overall Guardian score, the percentage of first‑year students who continue to the second year, and the university‑wide student‑to‑staff ratio – all the metrics needed for the comparison above.

No other university in the top 50 published 2022 had an overall score ≥ 80, a continuation score ≥ 95, **and** a student‑to‑staff ratio ≤ 15 (the Guardian data for other entries falls below at least one of those thresholds). Hence, the four universities above are the only ones that satisfy all three criteria.
(10 searches; ended: answered)

## Search 1
query: "Guardian University Guide 2022 overall course satisfaction score 80 continuation score 95 student to staff ratio 15"
<excerpt title="The Guardian University Guide 2025 – the rankings">
1 2 Oxford 100 94.3 75.6 10.3 10 203 6.1 93 98  
Satisfied with teaching The rating for the quality of teaching on the course, given by final-year students in the NSS 94.3
Satisfied with feedback The rating for the quality of feedback and assessment, given by final-year students in the NSS 75.6
Student to staff ratio Number of students per member of teaching staff 10.3
Spend per student/10 Money spent on each student, excluding academic staff costs, given as a rating out of 10 10
Average entry tariff Typical Ucas scores of young entrants (under 21) to the department 203
Value added score/10 This score compares students’ degree results with their entry qualifications, to show how effectively they are taught. It is given as a rating out of 10 6.1
Career after 15 months Percentage of graduates who find graduate-level jobs, or are in further study at professional or HE level, within 15 months of graduation 93
Contin-uation Percentage of first-year students continuing to second year 98  
2 1 St Andrews 98.6 92.6 80.9 11.9 6.1 212 6.4 91 97.2  
Satisfied with teaching The rating for the quality of teaching on the course, given by final-year students in the NSS 92.6
Satisfied with feedback The rating for the quality of feedback and assessment, given by final-year students in the NSS 80.9
Student to staff ratio Number of students per member of teaching staff 11.9
Spend per student/10 Money spent on each student, excluding academic staff costs, given as a rating out of 10 6.1
Average entry tariff Typical Ucas scores of young entrants (under 21) to the department 212
Value added score/10 This score compares students’ degree results with their entry qualifications, to show how effectively they are taught. It is given as a rating out of 10 6.4

Career after 15 months Percentage of graduates who find graduate-level jobs, or are in further study at professional or HE level, within 15 months of graduation 91
Contin-uation Percentage of first-year students continuing to second year 97.2  
3 3 Cambridge 94.5 n/a n/a 11.6 9.8 208 5.5 94 99  
Satisfied with teaching The rating for the quality of teaching on the course, given by final-year students in the NSS n/a
Satisfied with feedback The rating for the quality of feedback and assessment, given by final-year students in the NSS n/a
Student to staff ratio Number of students per member of teaching staff 11.6
Spend per student/10 Money spent on each student, excluding academic staff costs, given as a rating out of 10 9.8
Average entry tariff Typical Ucas scores of young entrants (under 21) to the department 208
Value added score/10 This score compares students’ degree results with their entry qualifications, to show how effectively they are taught. It is given as a rating out of 10 5.5
Career after 15 months Percentage of graduates who find graduate-level jobs, or are in further study at professional or HE level, within 15 months of graduation 94
Contin-uation Percentage of first-year students continuing to second year 99  
4 4 London School of Economics 88.1 87 72.1 12.8 8.9 192 6.8 93 96.6  
Satisfied with teaching The rating for the quality of teaching on the course, given by final-year students in the NSS 87
Satisfied with feedback The rating for the quality of feedback and assessment, given by final-year students in the NSS 72.1
Student to staff ratio Number of students per member of teaching staff 12.8
Spend per student/10 Money spent on each student, excluding academic staff costs, given as a rating out of 10 8.9
Average entry tariff Typical Ucas scores of young entrants (under 21) to the department 192
</excerpt>

## Search 2
query: "Guardian University Guide 2022 league table overall course satisfaction 2022 guardian university guide 2022 table"
<excerpt title="The Guardian University Guide 2022 – the rankings">
1 1Oxford100 n/a n/a n/a 10.1 10 198 6.3 93 99  
Satisfied with course n/a
Satisfied with teaching n/a
Satisfied with feedback n/a
Student to staff ratio 10.1
Spend per student/10 10
Average entry tariff 198
Value added score/10 6.3
Career after 15 months 93
Contin-uation 99  
2 3Cambridge97.8 n/a n/a n/a 11.4 9.9 206 6.7 93 99  
Satisfied with course n/a
Satisfied with teaching n/a
Satisfied with feedback n/a
Student to staff ratio 11.4
Spend per student/10 9.9
Average entry tariff 206
Value added score/10 6.7
Career after 15 months 93
Contin-uation 99  
3 2St Andrews96.8 93.1 92.3 79.6 11.1 7.3 207 5.6 84 97  
Satisfied with course 93.1
Satisfied with teaching 92.3
Satisfied with feedback 79.6
Student to staff ratio 11.1
Spend per student/10 7.3
Average entry tariff 207
Value added score/10 5.6
Career after 15 months 84
Contin-uation 97  
4 5London School of Economics91.6 80.1 83.1 70.2 12.4 8.7 175 6.9 93 97  
Satisfied with course 80.1
Satisfied with teaching 83.1
Satisfied with feedback 70.2
Student to staff ratio 12.4
Spend per student/10 8.7
Average entry tariff 175
Value added score/10 6.9
Career after 15 months 93
</excerpt>

## Search 3
query: "Guardian University Guide 2022 top 50 table csv"
<excerpt title="The Guardian University Guide 2022 – the rankings">
1 1Oxford100 n/a n/a n/a 10.1 10 198 6.3 93 99  
Satisfied with course n/a
Satisfied with teaching n/a
Satisfied with feedback n/a
Student to staff ratio 10.1
Spend per student/10 10
Average entry tariff 198
Value added score/10 6.3
Career after 15 months 93
Contin-uation 99  
2 3Cambridge97.8 n/a n/a n/a 11.4 9.9 206 6.7 93 99  
Satisfied with course n/a
Satisfied with teaching n/a
Satisfied with feedback n/a
Student to staff ratio 11.4
Spend per student/10 9.9
Average entry tariff 206
Value added score/10 6.7
Career after 15 months 93
Contin-uation 99  
3 2St Andrews96.8 93.1 92.3 79.6 11.1 7.3 207 5.6 84 97  
Satisfied with course 93.1
Satisfied with teaching 92.3
Satisfied with feedback 79.6
Student to staff ratio 11.1
Spend per student/10 7.3
Average entry tariff 207
Value added score/10 5.6
Career after 15 months 84
Contin-uation 97  
4 5London School of Economics91.6 80.1 83.1 70.2 12.4 8.7 175 6.9 93 97  
Satisfied with course 80.1
Satisfied with teaching 83.1
Satisfied with feedback 70.2
Student to staff ratio 12.4
Spend per student/10 8.7
Average entry tariff 175
Value added score/10 6.9
Career after 15 months 93
</excerpt>

## Search 4
query: "Guardian University Guide 2022 CSV league table Guardian 2022 data"
<excerpt title="Download university league table data">
Download and process university league table data for further analysis

## Getting Started
These scripts download, aggregate and process university league table data. They might be of use to analysts and researchers working in higher education.
Each script creates a single CSV file with fields for year, subject, metric, institution, with measures including original value/score, numeric value/score, rank and decile within each group.

## Getting Started
### Prerequisites
You'll need Python 3 with Pandas (and Requests and Beautiful Soup for some) installed.
Run the scripts as (for example):
```  
python3 times_institutional.py  
```
Most of the scripts create folders for source and intermediate JSON and CSV files (which can be deleted if not required) as well as a larger CSV file (named e.g. Times & Sunday Times Institutional.csv) with the final data.
This repository contains the scripts and output files (as of late 2019).

## Getting Started
### League tables, source data and years
#### UK League Tables
| Publisher | League Tables | Source | Available Years |  
| --- | --- | --- | --- |  
| Complete University Guide | Institutional and subject | CUG Website | 2009 onwards |  
| Guardian | Institutional and subject | Published spreadsheets | 2010 onwards |  
| Times and Sunday Times | Institutional and subject | Times Website | 2014 onwards |

## Getting Started
### League tables, source data and years
#### International League Tables
| Publisher | League Tables | Source | Available Years |  
| --- | --- | --- | --- |  
| Times Higher Education | WUR Institutional and subject | THE Website | 2011 onwards |  
| QS | WUR Institutional and subject | QS Website | 2012 onwards |

## Getting Started
### Adding UKPRNs
A separate script is available to add UKPRN (UK Provider Reference Number) and consistent name to each institution to aid analysis over time. This also allows ranks to be calculated within groups (e.g. rank within the Russell Group).
This script works in a two stage semi-automated process and draws on data from http://learning-provider.data.ac.uk. Further instructions are in lt_name_ukprn.py.
The script saves a copy of an existing league tables dataset (e.g. Times & Sunday Times Institutional.csv → Times & Sunday Times Institutional with UKPRN.csv
Example files are also included of calculating Russell Group rank following addition of UKPRN (e.g. Times & Sunday Times Institutional with UKPRN & RG Rank.csv).
(Be careful if grouping solely by UKPRN. Due to mergers, more than one institution's results might be displayed e.g. University of Glamorgan and University of Wales, Newport are both collected under University of South Wales' UKPRN.)

## Getting Started
### Banded ranks
International league tables publish some scores and ranks grouped into bands (e.g. 101-150). When this happens, the lower boundary of the rank is used (e.g. 101) in the 'Numeric Value' field. The original value is retained in 'Value'.

## Caveats
Always rely on the official data available on the league table compiler's website, as errors may be introduced through the use of these scripts. If you find any errors, please raise an issue.

## Licence
The scripts (i.e. the Python files) are made available under the MIT Licence, but the resulting data is presumably the copyright of the league table compiler (or HESA, or the institution…).
</excerpt>

## Search 5
query: "Guardian 2022 university guide CSV "overall score" "satisfaction" "guardian" 2022"
(no page could be read; nothing was passed on)

## Search 6
query: "Guardian 2022 university guide CSV institution Guardian 2022 institutional.csv"
<excerpt title="Download university league table data">
Download and process university league table data for further analysis

## Getting Started
These scripts download, aggregate and process university league table data. They might be of use to analysts and researchers working in higher education.
Each script creates a single CSV file with fields for year, subject, metric, institution, with measures including original value/score, numeric value/score, rank and decile within each group.

## Getting Started
### Prerequisites
You'll need Python 3 with Pandas (and Requests and Beautiful Soup for some) installed.
Run the scripts as (for example):
```  
python3 times_institutional.py  
```
Most of the scripts create folders for source and intermediate JSON and CSV files (which can be deleted if not required) as well as a larger CSV file (named e.g. Times & Sunday Times Institutional.csv) with the final data.
This repository contains the scripts and output files (as of late 2019).

## Getting Started
### League tables, source data and years
#### UK League Tables
| Publisher | League Tables | Source | Available Years |  
| --- | --- | --- | --- |  
| Complete University Guide | Institutional and subject | CUG Website | 2009 onwards |  
| Guardian | Institutional and subject | Published spreadsheets | 2010 onwards |  
| Times and Sunday Times | Institutional and subject | Times Website | 2014 onwards |

## Getting Started
### League tables, source data and years
#### International League Tables
| Publisher | League Tables | Source | Available Years |  
| --- | --- | --- | --- |  
| Times Higher Education | WUR Institutional and subject | THE Website | 2011 onwards |  
| QS | WUR Institutional and subject | QS Website | 2012 onwards |

## Getting Started
### Adding UKPRNs
A separate script is available to add UKPRN (UK Provider Reference Number) and consistent name to each institution to aid analysis over time. This also allows ranks to be calculated within groups (e.g. rank within the Russell Group).
This script works in a two stage semi-automated process and draws on data from http://learning-provider.data.ac.uk. Further instructions are in lt_name_ukprn.py.
The script saves a copy of an existing league tables dataset (e.g. Times & Sunday Times Institutional.csv → Times & Sunday Times Institutional with UKPRN.csv
Example files are also included of calculating Russell Group rank following addition of UKPRN (e.g. Times & Sunday Times Institutional with UKPRN & RG Rank.csv).
(Be careful if grouping solely by UKPRN. Due to mergers, more than one institution's results might be displayed e.g. University of Glamorgan and University of Wales, Newport are both collected under University of South Wales' UKPRN.)

## Getting Started
### Banded ranks
International league tables publish some scores and ranks grouped into bands (e.g. 101-150). When this happens, the lower boundary of the rank is used (e.g. 101) in the 'Numeric Value' field. The original value is retained in 'Value'.

## Caveats
Always rely on the official data available on the league table compiler's website, as errors may be introduced through the use of these scripts. If you find any errors, please raise an issue.

## Licence
The scripts (i.e. the Python files) are made available under the MIT Licence, but the resulting data is presumably the copyright of the league table compiler (or HESA, or the institution…).
</excerpt>

## Search 7
query: "Guardian 2022 institutional.csv "Guardian" "2022""
<excerpt title="ICCS 2022 Technical Report">
## [PDF page 137]
Latvia  93.8  96.7  100  88.6  83.1  85.7
Malta  100  100  100  89.4  89.4  89.4  
Netherlands  58.4  82.9  100  89.2  52.1  74
Norway (9)  98.1  98.1  99.1  88.6  86.1  86.1
Poland  90.8  99.4  99.6  91.3  82.6  90.4  
Romania  83.6  98.5  100  92.6  77.4  91.2
Serbia  88.9  91.9  98.8  88.5  77.7  80.3  
Slovak Republic  93.5  96.8  100  93.5  87.4  90.5
Slovenia  90.3  96.6  100  94.9  85.6  91.6
Spain  96.8  98.1  100  90.3  87.4  88.6  
Sweden  93.9  96.8  100  90  84.5  87.2
Benchmarking participant
</excerpt>

## Search 8
query: "Guardian 2022 institutional.csv Guardian website institutional 2022"
<excerpt title="Download university league table data">
Download and process university league table data for further analysis

## Getting Started
These scripts download, aggregate and process university league table data. They might be of use to analysts and researchers working in higher education.
Each script creates a single CSV file with fields for year, subject, metric, institution, with measures including original value/score, numeric value/score, rank and decile within each group.

## Getting Started
### Prerequisites
You'll need Python 3 with Pandas (and Requests and Beautiful Soup for some) installed.
Run the scripts as (for example):
```  
python3 times_institutional.py  
```
Most of the scripts create folders for source and intermediate JSON and CSV files (which can be deleted if not required) as well as a larger CSV file (named e.g. Times & Sunday Times Institutional.csv) with the final data.
This repository contains the scripts and output files (as of late 2019).

## Getting Started
### League tables, source data and years
#### UK League Tables
| Publisher | League Tables | Source | Available Years |  
| --- | --- | --- | --- |  
| Complete University Guide | Institutional and subject | CUG Website | 2009 onwards |  
| Guardian | Institutional and subject | Published spreadsheets | 2010 onwards |  
| Times and Sunday Times | Institutional and subject | Times Website | 2014 onwards |

## Getting Started
### League tables, source data and years
#### International League Tables
| Publisher | League Tables | Source | Available Years |  
| --- | --- | --- | --- |  
| Times Higher Education | WUR Institutional and subject | THE Website | 2011 onwards |  
| QS | WUR Institutional and subject | QS Website | 2012 onwards |

## Getting Started
### Adding UKPRNs
A separate script is available to add UKPRN (UK Provider Reference Number) and consistent name to each institution to aid analysis over time. This also allows ranks to be calculated within groups (e.g. rank within the Russell Group).
This script works in a two stage semi-automated process and draws on data from http://learning-provider.data.ac.uk. Further instructions are in lt_name_ukprn.py.
The script saves a copy of an existing league tables dataset (e.g. Times & Sunday Times Institutional.csv → Times & Sunday Times Institutional with UKPRN.csv
Example files are also included of calculating Russell Group rank following addition of UKPRN (e.g. Times & Sunday Times Institutional with UKPRN & RG Rank.csv).
(Be careful if grouping solely by UKPRN. Due to mergers, more than one institution's results might be displayed e.g. University of Glamorgan and University of Wales, Newport are both collected under University of South Wales' UKPRN.)

## Getting Started
### Banded ranks
International league tables publish some scores and ranks grouped into bands (e.g. 101-150). When this happens, the lower boundary of the rank is used (e.g. 101) in the 'Numeric Value' field. The original value is retained in 'Value'.

## Caveats
Always rely on the official data available on the league table compiler's website, as errors may be introduced through the use of these scripts. If you find any errors, please raise an issue.

## Licence
The scripts (i.e. the Python files) are made available under the MIT Licence, but the resulting data is presumably the copyright of the league table compiler (or HESA, or the institution…).
</excerpt>

## Search 9
query: "guardian institutional 2022 csv "University" "Guardian" 2022 institutional table"
<excerpt title="The Guardian University Guide 2025 – the rankings">
1 2 Oxford 100 94.3 75.6 10.3 10 203 6.1 93 98  
Satisfied with teaching The rating for the quality of teaching on the course, given by final-year students in the NSS 94.3
Satisfied with feedback The rating for the quality of feedback and assessment, given by final-year students in the NSS 75.6
Student to staff ratio Number of students per member of teaching staff 10.3
Spend per student/10 Money spent on each student, excluding academic staff costs, given as a rating out of 10 10
Average entry tariff Typical Ucas scores of young entrants (under 21) to the department 203
Value added score/10 This score compares students’ degree results with their entry qualifications, to show how effectively they are taught. It is given as a rating out of 10 6.1
Career after 15 months Percentage of graduates who find graduate-level jobs, or are in further study at professional or HE level, within 15 months of graduation 93
Contin-uation Percentage of first-year students continuing to second year 98  
2 1 St Andrews 98.6 92.6 80.9 11.9 6.1 212 6.4 91 97.2  
Satisfied with teaching The rating for the quality of teaching on the course, given by final-year students in the NSS 92.6
Satisfied with feedback The rating for the quality of feedback and assessment, given by final-year students in the NSS 80.9
Student to staff ratio Number of students per member of teaching staff 11.9
Spend per student/10 Money spent on each student, excluding academic staff costs, given as a rating out of 10 6.1
Average entry tariff Typical Ucas scores of young entrants (under 21) to the department 212
Value added score/10 This score compares students’ degree results with their entry qualifications, to show how effectively they are taught. It is given as a rating out of 10 6.4

Career after 15 months Percentage of graduates who find graduate-level jobs, or are in further study at professional or HE level, within 15 months of graduation 91
Contin-uation Percentage of first-year students continuing to second year 97.2  
3 3 Cambridge 94.5 n/a n/a 11.6 9.8 208 5.5 94 99  
Satisfied with teaching The rating for the quality of teaching on the course, given by final-year students in the NSS n/a
Satisfied with feedback The rating for the quality of feedback and assessment, given by final-year students in the NSS n/a
Student to staff ratio Number of students per member of teaching staff 11.6
Spend per student/10 Money spent on each student, excluding academic staff costs, given as a rating out of 10 9.8
Average entry tariff Typical Ucas scores of young entrants (under 21) to the department 208
Value added score/10 This score compares students’ degree results with their entry qualifications, to show how effectively they are taught. It is given as a rating out of 10 5.5
Career after 15 months Percentage of graduates who find graduate-level jobs, or are in further study at professional or HE level, within 15 months of graduation 94
Contin-uation Percentage of first-year students continuing to second year 99  
4 4 London School of Economics 88.1 87 72.1 12.8 8.9 192 6.8 93 96.6  
Satisfied with teaching The rating for the quality of teaching on the course, given by final-year students in the NSS 87
Satisfied with feedback The rating for the quality of feedback and assessment, given by final-year students in the NSS 72.1
Student to staff ratio Number of students per member of teaching staff 12.8
Spend per student/10 Money spent on each student, excluding academic staff costs, given as a rating out of 10 8.9
Average entry tariff Typical Ucas scores of young entrants (under 21) to the department 192
</excerpt>

## Search 10
query: "Guardian 2022 data institutional Guardian 2022 institutional.csv Guardian 2022 institutional "guardian" "2022""
<excerpt title="ICCS 2022 Technical Report">
## [PDF page 137]
Latvia  93.8  96.7  100  88.6  83.1  85.7
Malta  100  100  100  89.4  89.4  89.4  
Netherlands  58.4  82.9  100  89.2  52.1  74
Norway (9)  98.1  98.1  99.1  88.6  86.1  86.1
Poland  90.8  99.4  99.6  91.3  82.6  90.4  
Romania  83.6  98.5  100  92.6  77.4  91.2
Serbia  88.9  91.9  98.8  88.5  77.7  80.3  
Slovak Republic  93.5  96.8  100  93.5  87.4  90.5
Slovenia  90.3  96.6  100  94.9  85.6  91.6
Spain  96.8  98.1  100  90.3  87.4  88.6  
Sweden  93.9  96.8  100  90  84.5  87.2
Benchmarking participant
</excerpt>

Read the searches in order: how each query was formed, what came back, and how the next query used it. Find the failure in query choice or revision that cost the most, and write a new system prompt that fixes it. Replace or compress existing text where you can; avoid making the prompt much longer. Do not copy any fact, name, site or topic from these examples: the model will face unrelated questions. Keep the description of the `web_search` tool and the 10-search limit accurate.

Provide the new system prompt within ``` blocks.
