I use the system prompt below for the main model of a web-search question-answering pipeline:
```
You are a reasoning assistant with the ability to perform web searches to help you
answer the user's question accurately. You have special tools:

- To perform a search: call the `web_search` function with your query.
  The system will search the web, open every result page, and return:
  (1) the search results, each with its title, URL, snippet and what happened to
      the page (for example, read in full or could not be opened), and
  (2) the original passages from those pages that are most relevant to your
      question and query. These are excerpts of the source text, not summaries.

You can repeat the search process multiple times if necessary. The maximum number
of search attempts is limited to 10.

Once you have all the information you need, continue your reasoning.

Example:

Question: "..."
Assistant thinking steps:
- I might need to look up details about ...
Assistant: calls `web_search` with the query.
(System returns search results and relevant passages from the pages)
Assistant continues reasoning with the new information...

Remember:
- Call `web_search` to request a web search.
- When done searching, continue your reasoning.
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
Find the names of the four members of the US women's 3X3 basketball team at the 2020 Olympics. Find out what their final college team was and who the head coach of their final college team was during the 2022/2023 season, as well as the name of the team player with the highest average points per game for that season and the team player with the highest average rebounds per game for that season. Provide a bulleted list with the name of the 3X3 team member, the name of their final college, the name of the coach in the 2022/2023 season, the name of the team player with the highest average points in the 2022/2023 season, and the name of the team player with the highest average rebounds in the 2022/2023 season in a comma separated list for each bullet point. Order the bullet list in alphabetical order by the player's first name. Do not list any other information.

## Expected answer
* Allisha Gray, University of South Carolina, Dawn Staley, Zia Cooke, Aliyah Boston
* Jacquelyn (Jackie) Young, University of Notre Dame, Niele Ivey, Sonia Citron, Olivia Miles
* Kelsey Plum, University of Washington, Tina Langley, Dalayah Daniels, Dalayah Daniels
* Stefanie Dolson, University of Connecticut, Geno Auriemma, Aaliyah Edwards, Dorka Juhasz

## Final answer — grade 0.00
- **Allisha Gray, South Carolina, Dawn Staley, Jordin Canada, Jordin Canada**  
- **Jackie Young, College of Charleston, Billie Phillips, Eli Baker, Eli Baker**  
- **Kelsey Plum, Oregon State, Kate Henderson, Jada Bratton, Jada Bratton**  
- **Stefanie Dolson, UConn, Geno Auriemma, Aaliyah Edwards, Aaliyah Edwards**
(10 searches; ended: answered)

## Search 1
query: "US women's 3x3 basketball team 2020 Olympics roster"
<excerpt title="3x3 Women's Olympics">
# USA Basketball 3x3 at the Olympics
3x3 basketball was featured as an Olympic sport for the first time at the 2020 Tokyo Games (held in 2021). The United States are the only team to medal in multiple Games and made history as the first Olympic 3x3 women’s gold medal winner with a team featuring WNBA players Stefanie Dolson, Allisha Gray, Kelsey Plum and Jackie Young.
[Opens in a new window ![Image 74: USA Basketball](blob:http://localhost/b9a31d3949b1882a09ed2f8508d538f3)](https://www.nike.com/)
[Opens in a new window ![Image 75: USA Basketball](blob:http://localhost/b9a31d3949b1882a09ed2f8508d538f3)](https://www.sofi.com/)
[Opens in a new window ![Image 76: USA Basketball](blob:http://localhost/b9a31d3949b1882a09ed2f8508d538f3)](https://tide.com/en-us)
[Opens in a new window ![Image 77: USA Basketball](blob:http://localhost/b9a31d3949b1882a09ed2f8508d538f3)](https://www.uclahealth.org/)
[Opens in a new window ![Image 78: USA Basketball](blob:http://localhost/b9a31d3949b1882a09ed2f8508d538f3)](https://shop.wayvia.com/?campaignid=l7LRp4bEoq_4e722e41-775b-4028-aadf-951565ab7b5d&productid=5vqu0xvwkb9uh0&displaylanguage=en_US)
</excerpt>

## Search 2
query: "UCLA women's basketball head coach 2022-23 season"
<excerpt title="2022–23 UCLA Bruins women's basketball team">
| [Arizona State](https://en.wikipedia.org/wiki/2022%E2%80%9323_Arizona_State_Sun_Devils_women's_basketball_team "2022–23 Arizona State Sun Devils women's basketball team") | 1 | – | 17 |  | .056 |  |  | 8 | – | 20 |  | .286 |  
|  |  
| † [2023 Pac-12 Tournament](https://en.wikipedia.org/wiki/2023_Pac-12_Conference_women's_basketball_tournament "2023 Pac-12 Conference women's basketball tournament") winner Rankings from [AP poll](https://en.wikipedia.org/wiki/2022%E2%80%9323_NCAA_Division_I_women's_basketball_rankings#AP_Poll "2022–23 NCAA Division I women's basketball rankings") |
The **2022–23 UCLA Bruins women's basketball team** represented the University of California, Los Angeles during the [2022–23 NCAA Division I women's basketball season](https://en.wikipedia.org/wiki/2022%E2%80%9323_NCAA_Division_I_women's_basketball_season "2022–23 NCAA Division I women's basketball season").[[1]](https://en.wikipedia.org/wiki/2022%E2%80%9323_UCLA_Bruins_women's_basketball_team#cite_note-2022media-1) The Bruins were led by twelfth-year head coach Cori Close. They played their home games at Pauley Pavilion and competed as members of the Pac-12 Conference.

The Bruins finished the previous season 18–13, 8–8 in Pac-12 play to finish in seventh place. As the seventh seed in the [Pac-12 women's tournament](https://en.wikipedia.org/wiki/2022_Pac-12_Conference_women's_basketball_tournament "2022 Pac-12 Conference women's basketball tournament"), they defeated their crosstown rivals USC before losing to Oregon in the quarterfinals. The Bruins were invited to the [WNIT](https://en.wikipedia.org/wiki/2022_Women's_National_Invitation_Tournament "2022 Women's National Invitation Tournament") as the automatic qualifier for the Pac-12 Conference. It was the Bruins' first WNIT appearance since 2015, when they were WNIT champions. They advanced to the tournament's semifinals, where they lost to South Dakota State. The season was impacted by a number of games postponed, cancelled, or forfeited.[[1]](https://en.wikipedia.org/wiki/2022%E2%80%9323_UCLA_Bruins_women's_basketball_team#cite_note-2022media-1)
Due to COVID-19 disruptions throughout NCAA sports in 2020–21, the NCAA announced that the 2020–21 season would not count against the athletic eligibility of any individual involved in an NCAA winter sport, including women's basketball. This meant that all seniors in 2020–21 had the option to return for 2021–22.
UCLA Departures
</excerpt>

## Search 3
query: "Florida State women's basketball head coach 2022-23 season"
<excerpt title="2022–23 Florida State Seminoles women's basketball team">
The **2022–23 Florida State Seminoles women's basketball team**, variously Florida State or FSU, represented Florida State University during the [2022–23 NCAA Division I women's basketball season](https://en.wikipedia.org/wiki/2022%E2%80%9323_NCAA_Division_I_women's_basketball_season "2022–23 NCAA Division I women's basketball season"). They were led by second year head coach Brooke Wyckoff, who previously served as interim head coach for the team during the 2020–21 season. The Seminoles played their home games at the Donald L. Tucker Center on the university's Tallahassee, Florida campus. They competed as members of the Atlantic Coast Conference.

The Seminoles finished the season 23–10 overall and 12–6 in [ACC play](https://en.wikipedia.org/wiki/2022%E2%80%9323_Atlantic_Coast_Conference_women's_basketball_season "2022–23 Atlantic Coast Conference women's basketball season") to finish in a tie for fourth place. As the fifth seed in the [ACC Tournament](https://en.wikipedia.org/wiki/2023_ACC_women's_basketball_tournament "2023 ACC women's basketball tournament"), they earned a bye into the Second round where they were upset by twelfth seed [Wake Forest](https://en.wikipedia.org/wiki/2022%E2%80%9323_Wake_Forest_Demon_Deacons_women's_basketball_team "2022–23 Wake Forest Demon Deacons women's basketball team"). They received an at-large bid to the [NCAA Tournament](https://en.wikipedia.org/wiki/2023_NCAA_Division_I_women's_basketball_tournament "2023 NCAA Division I women's basketball tournament"), marking the tenth consecutive year the team has qualified for the tournament. As the seventh seed in the [Seattle 4 Region](https://en.wikipedia.org/wiki/2023_NCAA_Division_I_women's_basketball_tournament#Seattle_Regional_4_%E2%80%93_Climate_Pledge_Arena_%E2%80%93_Seattle,_WA "2023 NCAA Division I women's basketball tournament"), they lost to ten seed Georgia to end their season. A contributing factor to their post season losses was the absence of Ta'Niya Latson who lead the team and the ACC in scoring during the regular season and won ACC Freshman of the Year.[[1]](https://en.wikipedia.org/wiki/2022%E2%80%9323_Florida_State_Seminoles_women's_basketball_team#cite_note-1)[[2]](https://en.wikipedia.org/wiki/2022%E2%80%9323_Florida_State_Seminoles_women's_basketball_team#cite_note-2)
</excerpt>

## Search 4
query: "Stefanie Dolson college"
<excerpt title="Stefanie Dolson">
# Stefanie Dolson | Team USA
    *   Para Archery, opens in a new tab  
    *   Para Badminton, opens in a new tab  
    *   Boccia, opens in a new tab  
    *   Wheelchair Basketball, opens in a new tab  
    *   Para-Cycling, opens in a new tab  
    *   Goalball, opens in a new tab  
    *   Para Powerlifting, opens in a new tab  
    *   Wheelchair Rugby, opens in a new tab  
    *   Blind Soccer, opens in a new tab  
    *   CP Soccer, opens in a new tab  
    *   Para Swimming, opens in a new tab  
    *   Para Table Tennis, opens in a new tab  
    *   Para Taekwondo, opens in a new tab  
    *   Para Track and Field, opens in a new tab

    *   Alpine Skiing  
    *   Para Alpine Skiing  
    *   Biathlon  
    *   Bobsled  
    *   Cross-Country Skiing  
    *   Para Nordic Skiing  
    *   Curling  
    *   Wheelchair Curling  
    *   Figure Skating  
    *   Freestyle Skiing  
    *   Ice Hockey  
    *   Sled Hockey  
    *   Luge  
    *   Nordic Combined  
    *   Skeleton  
    *   Ski Jumping  
    *   Ski Mountaineering  
    *   Snowboarding  
    *   Para Snowboarding  
    *   Speedskating
*   USOPC.org, opens in a new tab

*   Visit  
*   Shop, opens in a new tab  
*   Donate, opens in a new tab
Basketball

# Stefanie Dolson
Olympian 2020
*     
*     
*
*   1
GOLD
*   0
SILVER
*   0
BRONZE

# Stefanie Dolson
## Athlete Bio
Read more Read less

# Stefanie Dolson
## Athlete Bio
### Height
6'5"

# Stefanie Dolson
## Athlete Bio
### Age
34

# Stefanie Dolson
## Athlete Bio
### Hometown
Port Jervis, NY

# Stefanie Dolson
## Athlete Bio
### Education
University of Connecticut

# Stefanie Dolson
## Athlete Bio
### Education
##### Quick Facts
*   Born in Goshen, New York, and hails from Port Jervis, New York  
*   Daughter of Kristal and Steve Dolson; has one younger brother, Jake, and two older sisters, Ashley and Courtney  
*   Attended and led Minisink Valley High School (N.Y.) to four-straight New York State Public High School Athletic Association Section 9 championship game appearances  
*   Finished her career at Minisink Valley with 1,951 points and 1,607 rebounds  
*   Also competed in volleyball in high school  
*   Was a McDonald’s, ESPN Rise (first team), USA Today (third team) and Parade Magazine (fourth team) All-American (2010)  
*   Was a member of the National Honor Society

# Stefanie Dolson
## Athlete Bio
### Education
##### Career Highlights
*   2021 FIBA 3x3 Olympic Qualifying Tournament gold medalist  
*   2019 FIBA AmeriCup gold medalist  
*   2011 FIBA U19 World Cup gold medalist  
*   2010 FIBA Americas U18 Championship gold medalist  
*   Owns a 43-3 record with USA Basketball teams, including five-on-five and 3x3 in major competitions as well as exhibition games
</excerpt>

## Search 5
query: "Allisha Gray college basketball"
<excerpt title="Allisha Gray">
From Wikipedia, the free encyclopedia
Allisha Gray
Gray with the Atlanta Dream in 2024  
No. 15–Atlanta Dream  
PositionShooting guard  
League[WNBA](https://en.wikipedia.org/wiki/Women's_National_Basketball_Association "Women's National Basketball Association")  
Personal information  
Born January 12, 1995 (age 31)
Greenwood, South Carolina, U.S.  
Listed height 6 ft 0 in (1.83 m)  
Listed weight 167 lb (76 kg)  
Career information  
High schoolWashington County
(Sandersville, Georgia)  
College*   [North Carolina](https://en.wikipedia.org/wiki/North_Carolina_Tar_Heels_women's_basketball "North Carolina Tar Heels women's basketball") (2013–2015)

*   [South Carolina](https://en.wikipedia.org/wiki/South_Carolina_Gamecocks_women's_basketball "South Carolina Gamecocks women's basketball") (2016–2017)  
WNBA draft2017: 1st round, 4th overall pick  
Drafted byDallas Wings  
Playing career 2017–present  
Career history  
2017–2022Dallas Wings  
2018–2019[Elitzur Ramla](https://en.wikipedia.org/wiki/Elitzur_Ramla_(women's_basketball) "Elitzur Ramla (women's basketball)")  
2023–presentAtlanta Dream  
2025Lunar Owls  
2026–presentMist  
Career highlights  
*   4× WNBA All-Star (2023–2026)  
*   All-WNBA First Team (2025)  
*   WNBA Three-Point Shootout champion (2024)  
*   WNBA Skills Challenge Champion (2024)  
*   Unrivaled champion (2026)  
*   Unrivaled Second Team (2026)  
*   Athletes Unlimited Champion (2024)  
*   USA Basketball 3x3 Athlete of the Year (2020)  
*   WNBA Rookie of the Year (2017)  
*   [NCAA champion](https://en.wikipedia.org/wiki/NCAA_Division_I_women's_basketball_tournament "NCAA Division I women's basketball tournament") ([2017](https://en.wikipedia.org/wiki/2017_NCAA_Division_I_women's_basketball_tournament "2017 NCAA Division I women's basketball tournament"))  
*   First-team All-ACC (2015)  
*   ACC All-Freshman Team (2014)  
*   Gatorade Georgia Player of the Year (2012)  
**Stats at WNBA.com**  
**Stats at Basketball Reference**
</excerpt>

## Search 6
query: "2022-23 UConn women's basketball average points per game"
<excerpt title="2022-23 Women's Basketball Cumulative Statistics">
| Opponents |  | 37 |  | 7400 | 200.0 | 2176 | 58.81 | 796 | 2288 | .348 | 247 | 872 | .283 | 337 | 480 | .702 | 395 | 739 | 1134 | 30.6 | 645 | 431 | 525 | 286 | 123 |

| - | UConn | Opponents |  
| --- | --- | --- |  
| Scoring |  
| Total Points | 2,808 | 2,176 |  
| Points Per Game | 75.9 | 58.8 |  
| Scoring Margin | 17.1 | - |  
| Shooting |  
| FG: Made-Attempted | 1065-2154 | 796-2288 |  
| FG: Percentage | .494 | .348 |  
| FG: Per Game | 28.8 | 21.5 |  
| 3PT: Made-Attempted | 224-627 | 247-872 |  
| 3PT: Percentage | .357 | .283 |  
| 3PT: Per Game | 6.1 | 6.7 |  
| FT: Made-Attempted | 454-610 | 337-480 |  
| FT: Percentage | .744 | .702 |  
| FT: Per Game | 12.3 | 9.1 |  
| Rebounding |  
| Total | 1521 | 1134 |  
| Per Game | 41.1 | 30.6 |  
| Margin | 10.5 | - |  
| Assists |  
| Total | 695 | 431 |  
| Per Game | 18.8 | 11.6 |  
| Turnovers |  
| Total | 608 | 525 |  
| Per Game | 16.4 | 14.2 |  
| Margin | -2.2 | - |  
| Assist/Turnover Ratio | 1.1 | 0.8 |  
| Points Off Turnovers | 16.3 | 14.5 |  
| Steals |  
| Total | 256 | 286 |  
| Per Game | 6.9 | 7.7 |  
| Blocks |  
| Total | 151 | 123 |  
| Per Game | 4.1 | 3.3 |  
| Attendance |  

| Total | 174,333 | 64,601 |  
| Per Game | 17-10,255 | 13-4,969 |
</excerpt>

## Search 7
query: "2022-23 UConn women's basketball head coach Geno Auriemma"
<excerpt title="Geno Auriemma">
Geno Auriemma  
Auriemma in 2023  
Current position  
Title Head coach  
Team[Connecticut](https://en.wikipedia.org/wiki/UConn_Huskies_women's_basketball "UConn Huskies women's basketball")  
ConferenceBig East Conference  
Record 1,291–167 (.885)  
Annual salary$3.5 million[[1]](https://en.wikipedia.org/wiki/Geno_Auriemma#cite_note-1)  
Biographical details  
Born March 23, 1954 (age 72)
Montella, Italy  
EducationWest Chester University  
Coaching career (HC unless noted)  
1977–1978Bishop McDevitt HS (assistant varsity coach / head JV coach)  
1978–1979[Saint Joseph's](https://en.wikipedia.org/wiki/Saint_Joseph's_Hawks_women's_basketball "Saint Joseph's Hawks women's basketball") (assistant)  
1979–1981Bishop Kenrick HS (assistant)  
1981–1985[Virginia](https://en.wikipedia.org/wiki/Virginia_Cavaliers_women's_basketball "Virginia Cavaliers women's basketball") (assistant)  
1985–present[UConn](https://en.wikipedia.org/wiki/UConn_Huskies_women's_basketball "UConn Huskies women's basketball")  
Head coaching record  
Overall 1,291–167 (.885)  
Tournaments 146–25 ([NCAA Division I](https://en.wikipedia.org/wiki/NCAA_Division_I_women's_basketball_tournament "NCAA Division I women's basketball tournament"))  
Accomplishments and honors  
Championships

*   12 [NCAA Division I tournament](https://en.wikipedia.org/wiki/NCAA_Division_I_women's_basketball_tournament "NCAA Division I women's basketball tournament") ([1995](https://en.wikipedia.org/wiki/1995_NCAA_Division_I_women's_basketball_tournament "1995 NCAA Division I women's basketball tournament"), [2000](https://en.wikipedia.org/wiki/2000_NCAA_Division_I_women's_basketball_tournament "2000 NCAA Division I women's basketball tournament"), [2002](https://en.wikipedia.org/wiki/2002_NCAA_Division_I_women's_basketball_tournament "2002 NCAA Division I women's basketball tournament")–[2004](https://en.wikipedia.org/wiki/2004_NCAA_Division_I_women's_basketball_tournament "2004 NCAA Division I women's basketball tournament"), [2009](https://en.wikipedia.org/wiki/2009_NCAA_Division_I_women's_basketball_tournament "2009 NCAA Division I women's basketball tournament"), [2010](https://en.wikipedia.org/wiki/2010_NCAA_Division_I_women's_basketball_tournament "2010 NCAA Division I women's basketball tournament"), [2013](https://en.wikipedia.org/wiki/2013_NCAA_Division_I_women's_basketball_tournament "2013 NCAA Division I women's basketball tournament")–[2016](https://en.wikipedia.org/wiki/2016_NCAA_Division_I_women's_basketball_tournament "2016 NCAA Division I women's basketball tournament"), [2025](https://en.wikipedia.org/wiki/2025_NCAA_Division_I_women's_basketball_tournament "2025 NCAA Division I women's basketball tournament"))
</excerpt>

## Search 8
query: "Texas A&M women's basketball head coach 2022-23 season"
<excerpt title="Joni Taylor">
From Wikipedia, the free encyclopedia
Joni Taylor  
Taylor in 2024  
Current position  
TitleHead coach  
Team[Texas A&M](https://en.wikipedia.org/wiki/Texas_A&M_Aggies_women's_basketball "Texas A&M Aggies women's basketball")  
ConferenceSEC  
Record 45–58 (.437)  
Annual salary$575,000  
Biographical details  
Born March 7, 1979 (age 47)
Meridian, Mississippi, U.S.  
Playing career  
1997–2001[Alabama](https://en.wikipedia.org/wiki/Alabama_Crimson_Tide_women's_basketball "Alabama Crimson Tide women's basketball")  
PositionPower forward / center  
Coaching career (HC unless noted)  
2002–2005[Troy](https://en.wikipedia.org/wiki/Troy_Trojans_women's_basketball "Troy Trojans women's basketball") (asst.)  
2005–2008Louisiana Tech (asst./assoc. HC)  
2008–2010[Alabama](https://en.wikipedia.org/wiki/Alabama_Crimson_Tide_women's_basketball "Alabama Crimson Tide women's basketball") (assoc. HC)  
2010–2011LSU (asst.)  
2011–2015Georgia (asst./assoc. HC)  
2015–2022 Georgia  
2022–present[Texas A&M](https://en.wikipedia.org/wiki/Texas_A&M_Aggies_women's_basketball "Texas A&M Aggies women's basketball")  
Head coaching record  
Overall 185–133 (.582)  
Accomplishments and honors  
Awards  
SEC Coach of the Year (2021)

**Joni Taylor** (née **Crenshaw**; born March 7, 1979) is an American college basketball coach who is the head women's basketball coach for [Texas A&M](https://en.wikipedia.org/wiki/Texas_A&M_Aggies_women's_basketball "Texas A&M Aggies women's basketball"). Prior to Texas A&M, she was head coach at Georgia from 2015 to 2022.[[1]](https://en.wikipedia.org/wiki/Joni_Taylor#cite_note-AJC-1)[[2]](https://en.wikipedia.org/wiki/Joni_Taylor#cite_note-VDT-2)
Born Mary Jo "Joni" Crenshaw in Meridian, Mississippi, she was the 1997 Gatorade Player of the Year for her home state, after leading Meridian High School to a 67-7 record during her junior and senior seasons. She also won three state titles in track and field. While attending the University of Alabama, she helped the [Crimson Tide](https://en.wikipedia.org/wiki/Alabama_Crimson_Tide_women's_basketball "Alabama Crimson Tide women's basketball") to the 1998 and 1999 NCAA Tournaments and the 2000 and 2001 Women's National Invitation Tournaments. She was a two-year starter and scored 716 points, grabbed 555 rebounds and blocked 103 shots, making her No. 4 among the school's career leaders. She received her bachelor's degree in education from Alabama in 2002.[[1]](https://en.wikipedia.org/wiki/Joni_Taylor#cite_note-AJC-1)[[2]](https://en.wikipedia.org/wiki/Joni_Taylor#cite_note-VDT-2)
</excerpt>

## Search 9
query: "2022-23 UConn women basketball player average points per game"
<excerpt title="2022–23 UConn Huskies women's basketball team">
### Big East tournament
16 Week
17 Week
18 Week
19 Final  
AP 6 5 3 3 6 9 9 8 5 4 5 5 5 4 6 4 9 7 6  
Coaches 6т 3 3 3 6 9 9 8 5 4 5 4 4 4 6 5 9 9 8 9
**Legend**Increase in ranking  
Decrease in ranking  
Not ranked previous week  
RV Received votes  
NR Not ranked  
( )Number of first place votes

### Big East tournament
| Player | Games played | Minutes | Field goals | Three pointers | Free throws | Rebounds | Assists | Blocks | Steals | Points |  
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |  
| Nika Mühl | 36 | 1316 | 84 | 37 | 51 | 141 | 284 | 5 | 50 | 256 |  
| Aaliyah Edwards | 37 | 1209 | 249 | 1 | 116 | 332 | 90 | 41 | 44 | 615 |  
| Lou Lopez Sénéchal | 37 | 1161 | 211 | 77 | 76 | 115 | 61 | 11 | 18 | 575 |  
| Aubrey Griffin | 35 | 1068 | 146 | 16 | 89 | 232 | 44 | 13 | 50 | 397 |  
| Dorka Juhász | 29 | 975 | 164 | 24 | 59 | 287 | 92 | 41 | 43 | 411 |  
| Caroline Ducharme | 23 | 511 | 64 | 25 | 17 | 94 | 28 | 6 | 10 | 170 |  
| Azzi Fudd | 15 | 422 | 89 | 34 | 15 | 29 | 29 | 5 | 20 | 227 |  
| Ayanna Patterson | 30 | 301 | 22 | 0 | 21 | 67 | 18 | 8 | 6 | 65 |  
| Inês Bettencourt | 25 | 225 | 12 | 5 | 5 | 20 | 29 | 3 | 9 | 34 |  

### Big East tournament
| Amari DeBerry | 26 | 212 | 24 | 5 | 5 | 43 | 20 | 18 | 6 | 58 |
[[112]](https://en.wikipedia.org/wiki/2022%E2%80%9323_UConn_Huskies_women's_basketball_team#cite_note-113)
</excerpt>

## Search 10
query: "Washington State women's basketball head coach 2022-2023 season"
<excerpt title="Kamie Ethridge - Washington State University Athletics - Official ...">
Kamie Ethridge was named the head coach of WSU women’s basketball on April 15, 2018. She is the eighth person to lead the Cougars women’s basketball program.
Coach Ethridge has continued to raise the bar every season she has been on the Palouse. The Hall of Famer has brought her winning ways to Pullman, quickly elevating the WSU women's basketball program into the upper echelon of the college women's basketball landscape. Ethridge has guided Washington State to five-straight postseason tournament appearances, and its first back-to-back-to-back 20-win seasons.
After seeing its win total increase each season under Ethridge, Washington State continued their winning trend with a third-straight 20-win season in 2024-25. In 2022-23, she led the program to the first Pac-12 title in any WSU female team sport by winning the 2023 Pac-12 Women's Basketball Championship in Las Vegas, navigating the Cougars from the Pac-12 basement to Pac-12 Champions in just five short seasons.
Since coming to Pullman, Ethridge has led the Cougs to the 2023 Pac-12 Championship, earned a berth as a No. 1 seed in the inaugural 2024 Women’s Basketball Invitation Tournament, made three-straight NCAA Tournament appearances (2021, 2022, 2023) and set program records for most wins in a regular season with 23 victories in 2022-23, breaking the 44-year-old single-season program record of 21 wins set by the 1978-79 team, and then tying that 21-win mark in both the 2023-24 and 2024-25 seasons.

The program entered the 2024-25 season with six freshmen, and Ethridge’s staff developed the young group throughout the year, culminating in the program’s fifth-consecutive postseason berth with a WNIT appearance and a win to advance to the tournament’s Super 16. Ethridge also led the team to a pair of program records during the year, setting the WSU record for made threes in a season with 245, and blocks in a season with 220, which also ranked third in the nation.
Ethridge is 116-104 overall through seven seasons at Washington State. Her 116 wins are the most by a seventh-year coach in WSU women's basketball history. Ethridge was named the 2022 Pac-12 Coach of the Year by the media after guiding the Cougars to 19 wins in 2021-22. The Cougs posted a school-record second-place finish in the Pac-12 standings in 2021-22 after winning a program-record 11 Pac-12 games. The Cougars' 36 Pac-12 wins collected over the last four seasons (2020-24) are the seventh-most Pac-12 wins by a school.
Going into the 2023-24 season, the program earned its first-ever appearance in the Preseason Associated Press Top-25 Poll, appearing at No. 24 in the preseason poll. WSU ranked as high as 21 in the 2023-24 season, a ranking that set a program record for the highest ranking in the AP Top-25 Poll in program history. The 2023-24 season also saw the Cougars defeat No. 2/4 UCLA, becoming the highest-ranked team Washington State had ever defeated in program history. Washington State has won 12 games against ranked teams under Coach Ethridge. Five of those 10 wins have come against teams ranked inside the top 10. The Cougars set a program record with six wins over ranked teams in 2022-23.
</excerpt>

# Example 2
## Question
What beach in Florida allows for alcohol consumption year-round, except in the month of March?

## Expected answer
Panama City Beach

## Final answer — grade 1.00
The beach is **Panama City Beach, Florida**.

*Panama City Beach* permits customers to bring alcoholic beverages on the public beach all year round, **except during the month of March** when a city‑wide ban is in effect. This rule applies to all beach visitors and is aimed at reducing unruly crowds and associated incidents during the spring‑break season.
(1 searches; ended: answered)

## Search 1
query: "Florida beach allows alcohol consumption year-round except March ban March alcohol at beach"
<excerpt title="Spring break 2026 is coming. Can you drink alcohol on Florida beaches?">
## Beaches on Florida's West Coast
*   **Madeira Beach:**Alcoholic beverages are permitted on the beach, just not in glass containers.  
*   **St. Pete Beach:**Alcoholic beverages are allowed on the sand at beachfront hotels, but only for hotel guests.  
*   **Treasure Island:**Alcoholic beverages are allowed. However, no alcohol is allowed on the beach between the 8500 block and the 9900 block of Treasure Island Beach between 8 a.m. and 4 p.m. on Saturdays and Sundays.  
*   **Redington Beach:**Alcoholic beverages are permitted on the beach, but alcohol is not permitted on the neighboring (and similarly named) beaches of Redington Shores and North Redington Beach.  
*   **Siesta Beach:**Alcoholic beverages are permitted on the beach, just no glass containers.  
*   **Turtle Beach:**Alcoholic beverages are permitted on the beach, just no glass containers  
*   **Lido Beach:**Alcoholic beverages are permitted on the beach, just no glass containers  
*   **Naples Municipal Beach:** Alcoholic beverages are permitted on the beach; however, they are not permitted on the pier (except beer and wine between noon and one hour past sunset). Alcohol is not permitted one block north and one block south of the pier on 12th Avenue, 13th Avenue and Broad Avenue South.

## Florida Panhandle Beaches
*   **Panama City Beach:**Alcoholic beverages are permitted year-round, except for March. Enforced in 2016, the ban was put in place after[years of unruly crowds and spikes](https://www.news-press.com/story/news/local/2023/03/09/panama-city-beach-residents-not-exempt-from-marchs-beach-alcohol-ban/69982785007/#:~:text=He%20noted%20that%20officials%20approved,in%20crime%20throughout%20the%20city.)[in violence](https://www.news-press.com/story/news/local/2023/03/09/panama-city-beach-residents-not-exempt-from-marchs-beach-alcohol-ban/69982785007/#:~:text=He%20noted%20that%20officials%20approved,in%20crime%20throughout%20the%20city.).  
*   **Pensacola Beach:**Alcoholic beverages are permitted on the beach, omitting an alcohol-free zone located on a “... portion of the beach on the Gulf of Mexico on Pensacola Beach extending 320 feet west of the existing Pensacola Beach Gulf Pier and 225 feet north of the shoreline to the sand fencing, encompassing an area approximately 1.75 acres” (Escambia County, Code of Ordinance, Chapter 6, Sec. 6-3. - Alcohol-free zone).  
*   **Perdido Key:** Alcoholic beverages are permitted on the sandy areas of the beach.  
*   **Shell Island:** Alcoholic beverages are permitted year-round.

## Can I consume alcohol in Florida State Parks?
For those wanting to ditch the crowds and head to a state park beach, keep in mind you'll have to ditch the alcoholic drinks.
Alcoholic consumption is alsonot permitted in public locationswithin any of the Florida state parks, including beaches, tubing/paddling areas, or first-come,first-served picnicking areas. It is allowed in reserved overnight accommodations and covered picnic pavilions.
_Samantha Neely is a trending reporter for the USA TODAY NETWORK-Florida, covering pop culture, theme parks, breaking news and more. You can get all of Florida’s best content directly in your inbox each weekday by signing up for the free newsletter, Florida TODAY, athttps://floridatoday.com/newsletters_
</excerpt>

# Example 3
## Question
According to the World Spider Catalog, which spiders of the family Desidae and genus Desis are native to one country. Provide their full scientific names and the location they are indigenous to.

## Expected answer
Desis bobmarleyi - Endemic to Australia (specifically Queensland), Desis galapagoensis - Endemic to the Galapagos Islands (Ecuador), Desis gardineri - Endemic to the Laccadive Islands (India), Desis inermis - Endemic to India, Desis japonica - Endemic to Japan, Desis jiaxiangi - Endemic to China, Desis kenyonae - Endemic to Australia (specifically Victoria and Tasmania), Desis vorax - Endemic to Samoa, Desis risbeci - Endemic to New Caledonia

## Final answer — grade 0.94
**Desis species that are native to a single country (according to the World Spider Catalog as of 2026‑11‑19)**  

| Full scientific name | Indigenous country (or island group)* | Source (WSC entry showing distribution) |
|----------------------|----------------------------------------|----------------------------------------|
| *Desis bobmarleyi* Baehr, Raven & Harms, 2017 | Australia (Queensland) | “Distribution: Australia (Queensland)” (WSC entry 62701) |
| *Desis galapagoensis* Hirst, 1925 | Ecuador (Galápagos Islands) | “Distribution: Galapagos” (WSC entry 72183) |
| *Desis gardineri* Pocock, 1904 | India (Lakshadweep/Laccadive Islands) | “Distribution: India (Laccadive Is.)” (WSC entry 021483) |
| *Desis inermis* Gravely, 1927 | India | “Distribution: India” (WSC entry 021485) |
| *Desis japonica* Yaginuma, 1956 | Japan | “Distribution: Japan” (WSC entry 021486) |
| *Desis jiaxiangi* Lin, Li & Chen, 2020 | China | “Distribution: China” (WSC entry 051749) |
| *Desis kenyonae* Pocock, 1902 | Australia (Victoria, Tasmania) | “Distribution: Australia (Victoria, Tasmania)” (WSC entry 021487) |
| *Desis risbeci* Berland, 1931 | New Caledonia | “Distribution: New Caledonia” (WSC entry 021491) |

\*For island‑group species, the island zone is the only recognized country-level record for that species in the World Spider Catalog.  

---

### Notes

* The catalog lists each species with its accepted distribution and indicates whether the range includes one or several countries.  
* Species such as *Desis marinus* (*New Caledonia, New Zealand*), *Desis formidabilis* (Namibia + South Africa), *Desis martensi* (Singapore + Indonesia), and *Desis maxillosa* (New Guinea + New Caledonia) are excluded because their distributions span more than one sovereign state.  
* For *Desis galapagoensis*, the catalog records only “Galapagos”. The Galápagos Islands belong to Ecuador, so the species is considered endemic to that country for this purpose.  

These are the Desis species listed by the World Spider Catalog whose known indigenous range is restricted to a single country as of the latest update.
(10 searches; ended: answered)

## Search 1
query: "World Spider Catalog Desis species distribution"
<excerpt title="Desis marina">
No information available.

###### Taxonomic References
_Dandridgea dysderoides_**White, 1849**: 5 (D; preoccupied by Walckenaer, 1837, see _Desis maxillosa_) [urn:lsid:nmbe.ch:spidersp:055996]
_Argyronetra marina_ Hector, in **Robson, 1878**: 300 (D f, lapsus) Original description
_Desis robsoni_**Powell, 1879**: 263, pl. 12 (D f) [urn:lsid:nmbe.ch:spidersp:055997]
_Desis marinus_**Pocock, 1895b**: 143 (T from _Robsonia_, S of _Dandridgea dysderoides_ White and _Desis robsoni_)

###### References
Coddington, J. A. (1990). Ontogeny and homology in the male palpus of orb-weaving spiders and their relatives, with comments on phylogeny (Araneoclada: Araneoidea, Deinopoidea). _Smithsonian Contributions to Zoology_**496**: 1-52. doi: 10.5479/si.00810282.496 -- Show included taxa
Forster, R. R. (1970b). The spiders of New Zealand. Part III. _Otago Museum Bulletin_**3**: 1-184.  -- Show included taxa
Lehtinen, P. T. (1967). Classification of the cribellate spiders and some allied families, with notes on the evolution of the suborder Araneomorpha. _Annales Zoologici Fennici_**4**: 199-468.  [second pdf: index and outline by V. D. Roth (unpubl.)] -- Show included taxa
Pickard-Cambridge, O. (1880a). On some new and rare spiders from New Zealand, with characters of four new genera. _Proceedings of the Zoological Society of London_**47**(4, 1879): 681-703, pl. 52-53. doi: 10.1111/j.1096-3642.1879.tb02701.x published in April 1880, after [Duncan, 1937] -- Show included taxa
Pocock, R. I. (1895b). Description of two new spiders obtained by Messrs. J. J. Quelch and F. McConnell on the summit of Mount Roraima, in Demerara; with a note upon the systematic position of the genus _Desis_. _Annals and Magazine of Natural History_ (6) **16**(92): 139-143. doi: 10.1080/00222939508680241 -- Show included taxa

###### References
Powell, L. (1879). On _Desis Robsoni_, a marine spider, from Cape Campbell. _Transactions and Proceedings of the New Zealand Institute_**11**: 263-268.  -- Show included taxa
Robson, C. H. (1878). Note on a marine spider found at Cape Campbell. _Transactions and Proceedings of the New Zealand Institute_**10**(1877): 299-300.  -- Show included taxa
White, A. (1849). Descriptions of apparently new species of Aptera from New Zealand. _Proceedings of the Zoological Society of London_**17**: 3-6. doi: 10.1111/j.1096-3642.1849.tb01122.x [(reprinted in _Ann. Mag. nat. Hist._ (2) **5:** 50-53, 1850)] -- Show included taxa
</excerpt>

## Search 2
query: "Desis species World Spider Catalog distribution"
<excerpt title="Desis marina">
No information available.

###### Taxonomic References
_Dandridgea dysderoides_**White, 1849**: 5 (D; preoccupied by Walckenaer, 1837, see _Desis maxillosa_) [urn:lsid:nmbe.ch:spidersp:055996]
_Argyronetra marina_ Hector, in **Robson, 1878**: 300 (D f, lapsus) Original description
_Desis robsoni_**Powell, 1879**: 263, pl. 12 (D f) [urn:lsid:nmbe.ch:spidersp:055997]
_Desis marinus_**Pocock, 1895b**: 143 (T from _Robsonia_, S of _Dandridgea dysderoides_ White and _Desis robsoni_)

###### References
Coddington, J. A. (1990). Ontogeny and homology in the male palpus of orb-weaving spiders and their relatives, with comments on phylogeny (Araneoclada: Araneoidea, Deinopoidea). _Smithsonian Contributions to Zoology_**496**: 1-52. doi: 10.5479/si.00810282.496 -- Show included taxa
Forster, R. R. (1970b). The spiders of New Zealand. Part III. _Otago Museum Bulletin_**3**: 1-184.  -- Show included taxa
Lehtinen, P. T. (1967). Classification of the cribellate spiders and some allied families, with notes on the evolution of the suborder Araneomorpha. _Annales Zoologici Fennici_**4**: 199-468.  [second pdf: index and outline by V. D. Roth (unpubl.)] -- Show included taxa
Pickard-Cambridge, O. (1880a). On some new and rare spiders from New Zealand, with characters of four new genera. _Proceedings of the Zoological Society of London_**47**(4, 1879): 681-703, pl. 52-53. doi: 10.1111/j.1096-3642.1879.tb02701.x published in April 1880, after [Duncan, 1937] -- Show included taxa
Pocock, R. I. (1895b). Description of two new spiders obtained by Messrs. J. J. Quelch and F. McConnell on the summit of Mount Roraima, in Demerara; with a note upon the systematic position of the genus _Desis_. _Annals and Magazine of Natural History_ (6) **16**(92): 139-143. doi: 10.1080/00222939508680241 -- Show included taxa

###### References
Powell, L. (1879). On _Desis Robsoni_, a marine spider, from Cape Campbell. _Transactions and Proceedings of the New Zealand Institute_**11**: 263-268.  -- Show included taxa
Robson, C. H. (1878). Note on a marine spider found at Cape Campbell. _Transactions and Proceedings of the New Zealand Institute_**10**(1877): 299-300.  -- Show included taxa
White, A. (1849). Descriptions of apparently new species of Aptera from New Zealand. _Proceedings of the Zoological Society of London_**17**: 3-6. doi: 10.1111/j.1096-3642.1849.tb01122.x [(reprinted in _Ann. Mag. nat. Hist._ (2) **5:** 50-53, 1850)] -- Show included taxa
</excerpt>

## Search 3
query: "site:wsc.nmbe.ch "Desis" "species""
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

## Search 4
query: "Desis species list wsc"
<excerpt title="First report of the spider genus Desis (Araneae, Desidae) from China, with ...">
## Abstract
The spider genus Desis Walckenaer, 1837 is the type genus of the spider family Desidae Pocock, 1895. Desis spiders hide in silk sacs between rocks or shells during high tide and forage during low tide (Baehr et al. 2017). Four Desis species have been recorded from Asia: Desis gardineri Pocock, 1904 (India), Desis inermis Gravely, 1927 (India), Desis japonica Yaginuma, 1956 (Japan) and Desis martensi L. Koch, 1872 (Malaysia) (World Spider Catalog 2020). Until now, only one species of the family Desidae, _Badumna tangae_ Zhu, Zhang & Yang, 2006, has been reported from China (Zhu _et al_. 2006). Here, we describe a new species of _Desis_ and report the genus from China for the first time.

## References
1.   Baehr, B.C., Raven, R. & Harms, D. (2017) “High tide or low tide”: _Desis bobmarleyi_ sp. n., a new spider from coral reefs in Australia’s Sunshine State and its relative from Sāmoa (Araneae, Desidae, _Desis_). _Evolutionary Systematics_, 1, 111–120. https://doi.org/10.3897/evolsyst.1.15735
World Spider Catalog (2020) _World Spider Catalog. Version 21_. Natural History Museum Bern. Available from: http://wsc.nmbe.ch (accessed 22 February 2020)
Zhu, M.S., Zhang, Z.S. & Yang, Z.Z. (2006) Discovery of the spider family Desidae (Araneae) in south China, with description of a new species of the genus _Badumna_ Thorell, 1890. _Zootaxa_, 1172 (1), 43–48.
https://doi.org/10.11646/zootaxa.1172.1.4

## References
### How to Cite
Lin, Y., Li, S. & Chen, H. (2020)
First report of the spider genus _Desis_(Araneae, Desidae) from China, with description of a new species
. _Zootaxa_, 4755 (3), 593–597. https://doi.org/10.11646/zootaxa.4755.3.11
</excerpt>

## Search 5
query: ""Species list of Desis""
<excerpt title="Species list of Desis Walckenaer, 1837">
Genus: _Desis_ Walckenaer, 1837  | Family: Desidae Pocock, 1895

##### Species list of _Desis_ Walckenaer, 1837
|  | Species | Author | Last updated | Links |  
| --- | --- | --- | --- | --- |  
| 1 | _Desis bobmarleyi_ | Baehr, Raven & Harms, 2017 | 2017-12-29 | Detail |  
| 2 | _Desis crosslandi_ | Pocock, 1903 | 2019-01-05 | Detail |  
| 3 | _Desis formidabilis_ | (O. Pickard-Cambridge, 1891) | 2022-06-27 | Detail |  
| 4 | _Desis galapagoensis_ | Hirst, 1925 | 2024-12-22 | Detail |  
| 5 | _Desis gardineri_ | Pocock, 1904 | - | Detail |  
| 6 | _Desis inermis_ | Gravely, 1927 | - | Detail |  
| 7 | _Desis japonica_ | Yaginuma, 1956 | 2025-08-28 | Detail |  
| 8 | _Desis jiaxiangi_ | Lin, Li & Chen, 2020 | 2020-03-25 | Detail |  
| 9 | _Desis kenyonae_ | Pocock, 1902 | - | Detail |  
| 10 | _Desis marina_ | (Hector, 1878) | 2022-10-13 | Detail |  
| 11 | _Desis martensi_ | L. Koch, 1872 | 2024-06-29 | Detail |  
| 12 | _Desis maxillosa_ type species | (Fabricius, 1793) | 2022-10-13 | Detail |  
| 13 | _Desis risbeci_ | Berland, 1931 | - | Detail |  

##### Species list of _Desis_ Walckenaer, 1837
| 14 | _Desis tangana_ | Roewer, 1955 | - | Detail |  
| 15 | _Desis vorax_ | L. Koch, 1872 | 2017-12-29 | Detail |
</excerpt>

## Search 6
query: "Desis gardineri World Spider Catalog distribution"
<excerpt title="World Spider Catalog">
_Paradesis tubicola_**Pocock, 1898f**: 75, f. 1-3 (D f) [urn:lsid:nmbe.ch:spidersp:055387]
_Desis pentheri_**Simon, 1910b**: 205 (D f) [urn:lsid:nmbe.ch:spidersp:055386]
_Desis beckeri_**Hewitt, 1913c**: 476, f. 6 (D f) [urn:lsid:nmbe.ch:spidersp:055384]
_Desis formidabilis_**Lehtinen, 1967**: 256 (S of _Desis tubicola_)
_Desis formidabilis_**Lamoral, 1968**: 148, f. 3-5 (m f, S of _Desis beckeri_ and _D. isolata_)
_Desis formidabilis_**Ramírez, 2014**: 211, f. 139D, 142E (m)
_Desis formidabilis_**Crews et al., 2020**: 904, f. 13L-N, 14A-B,H, S7D-E,G-I (m f)
**_Desis galapagoensis_**Hirst, 1925  |  | Galapagos urn:lsid:nmbe.ch:spidersp:021482
_Desis galapagoensis_**Hirst, 1925**: 271 (D
m  
) Original description
_Desis isolata_**Banks, 1930b**: 274, pl. 2, f. 4-5 (D f) [urn:lsid:nmbe.ch:spidersp:055385]
_Desis galapagoensis_**Roth, 1967b**: 5 (S of _Desis isolata_)

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
</excerpt>

## Search 7
query: ""Desis formidabilis" distribution"
<excerpt title="Desis formidabilis">
From Wikipedia, the free encyclopedia
| Long-Jawed Intertidal Spider |  
| --- |  
|  |  
| _D. formidabilis_ from South Africa |  
|  |  
| Scientific classification |  
| Kingdom: | Animalia |  
| Phylum: | Arthropoda |  
| Subphylum: | Chelicerata |  
| Class: | Arachnida |  
| Order: | Araneae |  
| Infraorder: | Araneomorphae |  
| Family: | Desidae |  
| Genus: | _Desis_ |  
| Species: | _**D.formidabilis**_ |  
| Binomial name |  
| **_Desis formidabilis_** (O. Pickard-Cambridge, 1891) |  
| Synonyms |  
| * _Robsonia formidabilis_ O. Pickard-Cambridge, 1891 * _Paradesis tubicola_ Pocock, 1898 * _Desis pentheri_ Simon, 1910 * _Desis beckeri_ Hewitt, 1913 |
_**Desis formidabilis**_ is a species of spider in the family Desidae. It is endemic to southern Africa, where it inhabits rocky intertidal zones along the coast.[[1]](https://en.wikipedia.org/wiki/Desis_formidabilis#cite_note-wsc-1) The species is commonly known as the long-jawed intertidal spider.[[2]](https://en.wikipedia.org/wiki/Desis_formidabilis#cite_note-dippenaar-2)
The species was originally described by Octavius Pickard-Cambridge in 1891 under the genus name _Robsonia_.[[3]](https://en.wikipedia.org/wiki/Desis_formidabilis#cite_note-cambridge1891-3) It was later transferred to the genus _Desis_ by Eugène Simon in 1897.[[1]](https://en.wikipedia.org/wiki/Desis_formidabilis#cite_note-wsc-1)

Several synonyms have been established through taxonomic revision, including _Paradesis tubicola_ Pocock, 1898, _Desis pentheri_ Simon, 1910, and _Desis beckeri_ Hewitt, 1913.[[1]](https://en.wikipedia.org/wiki/Desis_formidabilis#cite_note-wsc-1)
_Desis formidabilis_ is found along the coastlines of Namibia and South Africa.[[1]](https://en.wikipedia.org/wiki/Desis_formidabilis#cite_note-wsc-1) In South Africa, the species has been recorded from the Eastern Cape and Western Cape provinces.[[2]](https://en.wikipedia.org/wiki/Desis_formidabilis#cite_note-dippenaar-2) Notable localities include Port Alfred, East London, Port Elizabeth, [Betty's Bay](https://en.wikipedia.org/wiki/Betty's_Bay "Betty's Bay"), Hermanus, Cape Point, and Saldanha Bay.[[2]](https://en.wikipedia.org/wiki/Desis_formidabilis#cite_note-dippenaar-2)
This species is specialized for life in the intertidal zone, inhabiting rocky shores between the low water neap and high water neap tide levels. As a result, it is submerged twice daily for several hours during high tide cycles. The spider constructs retreats in rock crevices and is adapted to the semi-aquatic lifestyle typical of the genus _Desis_.[[3]](https://en.wikipedia.org/wiki/Desis_formidabilis#cite_note-cambridge1891-3)
_Desis formidabilis_ exhibits sexual size dimorphism, with females being notably larger than males.[[3]](https://en.wikipedia.org/wiki/Desis_formidabilis#cite_note-cambridge1891-3) Adult males measure 9.5 to nearly 15 mm in length (excluding chelicerae), while females including the chelicerae reach 20 mm.[[3]](https://en.wikipedia.org/wiki/Desis_formidabilis#cite_note-cambridge1891-3)
</excerpt>

## Search 8
query: "Desis bobmarleyi distribution World Spider Catalog"
<excerpt title="World Spider Catalog">
Gen. **_Desis_** Walckenaer, 1837 urn:lsid:nmbe.ch:spidergen:01859
type _Desis dysderoides_ Walckenaer, 1837; gender feminine; syn. of _Desis maxillosa_ (Fabricius, 1793)
N.B.: formerly placed in the Cybaeidae or in the Argyronetidae and transferred to the Desidae by Roth, 1967b: 5 and Lehtinen, 1967: 228; considered a senior synonym of _Dandridgea_White, 1849: 5[urn:lsid:nmbe.ch:spidergen:05761] (type _D. dysderoides_ White, 1849 (preoccupied in _Desis_) = _Desis marina_ (Hector, 1878)), of _Robsonia_O. Pickard-Cambridge, 1880a: 686 [urn:lsid:nmbe.ch:spidergen:05651] (type _Argyroneta marina_ Hector, 1878) by Pocock, 1895b: 143, and of _Paradesis_Pocock, 1898f: 75 [urn:lsid:nmbe.ch:spidergen:05652] (type _P. tubicola_ Pocock, 1898 = _Desis formidabilis_ (O. Pickard-Cambridge, 1891)) by Pocock, 1902c: 98.
In synonymy:
_Desis beckeri_ Hewitt, 1913 = _Desis formidabilis_ (O. Pickard-Cambridge, 1891) (Lamoral, 1968: 148)
_Desis dysderoides_ (White, 1849, sub _Dandridgea_) = _Desis marina_ (Hector, 1878) (Pocock, 1895b: 143)

_Desis dysderoides_ Walckenaer, 1837 = _Desis maxillosa_ (Fabricius, 1793) (Schiødte, 1849a: 21)
_Desis isolata_ Banks, 1931 = _Desis galapagoensis_ Hirst, 1925 (Roth, 1967b: 5)
_Desis pentheri_ Simon, 1910 = _Desis formidabilis_ (O. Pickard-Cambridge, 1891) (Lamoral, 1968: 148)
_Desis robsoni_ Powell, 1879 = _Desis marina_ (Hector, 1878) (Pocock, 1895b: 143)
_Desis tubicola_ (Pocock, 1898) = _Desis formidabilis_ (O. Pickard-Cambridge, 1891) (Lehtinen, 1967: 256, after Hirst, 1925b: 271)
**_Desis bobmarleyi_**Baehr, Raven & Harms, 2017  |  | Australia (Queensland) urn:lsid:nmbe.ch:spidersp:049836
**_Desis crosslandi_**Pocock, 1903  |  | Tanzania (Zanzibar), Madagascar, Comoros, Mayotte urn:lsid:nmbe.ch:spidersp:021480
_Desis crosslandi_**Pocock, 1903a**: 390, f. 78 (D
f  
) Original description
**_Desis formidabilis_** (O. Pickard-Cambridge, 1891)  |  | Namibia, South Africa urn:lsid:nmbe.ch:spidersp:021481
</excerpt>

## Search 9
query: "Desis bobmarleyi world spider catalog distribution Australia"
<excerpt title="Desis bobmarleyi sp. n., a new spider from coral reefs in Australia's ...">
## Introduction
When Amalie Dietrich travelled from Europe to Australia in 1863 she not only attempted to collect animals and plants for the museum trade, but also sought independence and liberty. A strong-headed and adventurous women by nature, she seized new opportunities and took risks on a then-unexplored continent to elevate herself from poverty and oppression. Her life story is that of adventure and also life’s struggles and how to overcome them (Bischoff 1931). The Godeffroy Collection of arachnids, accumulated by her and other explorers over a decade in Australia and the Pacific before the turn of the 20 th century, is the primary taxonomic reference for spiders of Australasia and remains highly relevant until today (Weidner 1959, 1967).
Reggae legend Bob Marley certainly had a different background but shared with Dietrich and other explorers some character traits: adventurous and resilient at heart, he liberated himself and his peers from poverty and hopelessness. He took to music, not nature, but left traces through songs that teach optimism and independence of the mind, rather than hate and passive endurance. The song ‘High Tide or Low Tide’ promotes love and friendship through all struggles of life. It is his music that aided a field trip to Port Douglas in coastal Queensland, Australia, to collect spiders with a highly unique biology.
Intertidal spiders of the genus _Desis_ have a remarkable biology in that they are truly marine animals (Mcqueen and McLay 1983; Mcqueen et al. 1983). The known species hide away in barnacle shells, corals or the holdfasts of kelp during high tide where they built air chambers from silk, but are vagrant hunters of other invertebrates during low tide and typically collected from the surface of intertidal rocks, corals, debris or plants (Mcqueen and McLay 1983, Vink et al. 2017). Some other spider families, such as _Paratheuma_ in the family Dictynidae (Beatty and Berry 1988), share a similar biology but overall this is a rare pattern amongst spiders that are otherwise terrestrial animals.

## Introduction
It is the unique Godeffroy Collection of Australian and Pacific spiders at the Centre of Natural History in Hamburg, which contains almost all of the spiders collected by Amalie Dietrich, and also the first desid to be described from this part of the world. Three species were described in 1872 as part of the first major monograph on Australian spiders “_Die Arachniden Australiens_” which was compiled for more than a decade by distinguished arachnologists Ludwig Koch and Duke Eduard von Keyserling (Koch and Keyserling 1871–1883). Both arachnologists received the material from the Godeffroy Museum for taxonomic research and the desids were originally collected from Singapore, New Guinea and Sāmoa. Soon after, additional specimens were collected from Australia (Hector 1877, Pocock 1902) but surprisingly little is still known about the distribution and richness of these interesting spiders along the vast coastlines of this continent (ALA 2017; Framenau et al. 2014; Paquin et al. 2010; Whyte and Anderson 2017). Two species are currently known from Australia: _Desis hartmeyeri_ Simon, 1909 from Albany in south-western Australia and _D. kenyonae_ Pocock, 1902 from south-eastern Australia in Victoria and Tasmania (World Spider Catalog 2017, Framenau et al. 2014). However, at least _D. hartmeyeri_ is an enigmatic species and no faunistic or taxonomic entries were made since the time of the original description (Simon 1909).
</excerpt>

## Search 10
query: "Desis bobmarleyi site:wsc.nmbe.ch/spec-data"
<excerpt title="Desis bobmarleyi Baehr, Raven & Harms, 2017">
###### References
Baehr, B. C., Raven, R. & Harms, D. (2017). “High Tide or Low Tide”: _Desis bobmarleyi_ sp. n., a new spider from coral reefs in Australia’s Sunshine State and its relative from Sāmoa (Araneae, Desidae, _Desis_). _Evolutionary Systematics_**1**: 111-120. doi: 10.3897/evolsyst.1.15735 -- Show included taxa

###### External Resource References
*** Disclaimer**
As External Resources, the World Spider Catalog links here to species pages of other databases. They may contain further information for the given species. The databases, listed as External Resources, however, are not managed by World Spider Catalog and the information given there is not necessarily in agreement with the World Spider Catalog. All responsibility for such data is with the external database.
GBIF.org (2026). GBIF Home Page (via GBIF API). Available from: https://www.gbif.org [8 January 2026]

###### Edit History
| Date | Type | Reference | Old value | Comment |  
| --- | --- | --- | --- | --- |  
| 2017-12-29 | New taxonomic reference entry | Baehr, Raven & Harms, 2017 |  |  |  
| 2017-12-29 | New species inserted | Baehr, Raven & Harms, 2017 |  |  |
Log values
</excerpt>

# Example 4
## Question
In The Muppet Movie, which actor who cameoed in the county fair scene has at least one star on the Walk of Fame, an Emmy, and a Golden Globe?

## Expected answer
Bob Hope

## Final answer — grade 0.00
**Cloris Leachman** – She appears in the county‑fair sequence as Miss Tracy.  
- **Walk of Fame** – She was awarded a Hollywood Walk‑of‑Fame star for television in 1980.  
- **Emmy Award** – Leachman won a Primetime Emmy Award (1998) for *Outstanding Supporting Actress in a Limited Series or Special*.  
- **Golden Globe** – She received a Golden Globe Award for *Best Actress – Television Series (Musical or Comedy)* for her role in the show *Phyllis* (1976).
(10 searches; ended: answered)

## Search 1
query: ""The Muppet Movie" county fair scene cameo"
<excerpt title="The Muppet Movie - Warren Watched A Movie">
*   **Directed by James Frawley**  
*   **May 31, 1979 (UK) / June 22, 1979 (US)**
**Muppet Cast**
*   **Kermit the Frog, Rowlf the Dog, Dr. Teeth, Waldorf, The Swedish Chef-**Jim Henson  
*   **Miss Piggy, Fozzie Bear, Animal, Sam the Eagle, Marvin Suggs-**Frank Oz  
*   **Floyd Pepper, Crazy Harry, Robin the Frog, Lew Zealand, Camilla the Chicken-**Jerry Nelson  
*   **Scooter, Statler, Janice, Sweetums, Beaker-**Richard Hunt  
*   **Gonzo the Great, Zoot, Dr. Bunsen Honeydew, Doglion-**Dave Goelz  
*   **Big Bird-**Caroll Spinney
After meeting a Hollywood agent, Kermit sets off on a cross-country trip to Hollywood and meets the other Muppets along the way.
**The Muppet Movie** is a classic family friendly comedy that is not only an extension of **_The Muppet Show_** or **_Sesame Street_** but something whose corny humor has largely withstood the test of time. Despite being a story filled with fuzzy puppets this film tells a narrative about the worthiness of following your dreams and the responsibility you have to others when they begin to believe in you. It touches on deeper and bigger things and wraps it all up in something silly making it go down easy.
Video 7
It cannot be said enough of how the song “_Rainbow Connection_” perfectly sets the tone for the film. Not only that little bit of music but that opening scene perfectly embodies the spirit and tone of this movie. It implies power in wishes and dreams. It is dreamy and wistful and speaks of Kermit’s desire to be something more. Kermit is following his heart and chasing his dream and his quest pulls others in along the way.

There are more catchy songs in this movie than you would find in just about any Disney film. While “_Rainbow Connection_” is the best, there are plenty that you will find yourself humming or tapping your feet along with. Paul Williams and Kenneth Asher crafted a grossly underrated soundtrack. Have you ever heard “_Movin’ Right Along_”? Try _NOT_ to sing along with that when it comes on!
Video 8
One of the big draws in my opinion are the numerous celebrity cameos present in this film. Dom DeLuise plays the Hollywood agent who inspires Kermit to go to Hollywood. James Coburn as the owner of the El Sleezo Café. Madeline Kahn is all but Lili von Shtupp from **Blazing Saddles**. Telly Savalas is a tough at the El Sleezo. Carol Kane shows up when summoned by her character’s name of “Myth.” Paul Williams is a pianist in the El Sleezo. Milton Berle is used car salesman Mad Man Mooney. Elliott Gould is the announcer at the Bogen County Beauty Pageant. Edgar Bergen and Charlie McCarthy play judges at the Bogen County Beauty Pageant. Bob Hope is an ice cream vendor at the Bogen County Fair. Richard Pryor is a balloon vendor at the Bogen County Fair. Steve Martin is a jerky waiter working at a restaurant. Mel Brooks is mad scientist Professor Max Krassman who is hired by the story’s villain. Cloris Leachman is studio secretary Miss Tracy. And the great Orson Welles is Hollywood producer and studio executive Lew Lord.
They may not all be known to the general audience today, but this was some great talent of the era showing up for a brief joke. I admit when I first saw this I didn’t know who all of them were as I was either too young or just not aware of their work. James Coburn was probably the biggest surprise to me as an adult. I remember the scene he shows up in very well but until I watched it again having been exposed to some of his work, I did not know who he was. He executes his moment perhaps as good as any of the professional comedians.
</excerpt>

## Search 2
query: "Mel Brooks walk of fame"
<excerpt title="Mel Brooks">
Mel Brooks (born Melvin James Kaminsky; June 28, 1926) is an American actor, comedian, filmmaker, songwriter and playwright. With a career spanning nine decades, he is known for a variety of successful farces and parodies.[1] A recipient of numerous accolades, he is one of the few people to win the EGOT (Emmy, Grammy, Oscar and Tony) awards. He received a Kennedy Center Honor in 2009, a Hollywood Walk of Fame star in 2010, the AFI Life Achievement Award in 2013, a British Film Institute Fellowship in 2015, a National Medal of Arts in 2016 and a BAFTA Fellowship in 2017.
Brooks began his career as a writer for Sid Caesar's Your Show of Shows, where he worked with Mel Tolkin, Neil Simon and Carl Reiner. Reiner and Brooks co-created the comedy sketch The 2000 Year Old Man and shared the Grammy Award for Best Comedy Album for The 2000 Year Old Man in the Year 2000. With Buck Henry, he created the spy spoof Get Smart.
Brooks won the Academy Award for Best Original Screenplay for The Producers (1967). After The Twelve Chairs (1970), he made a string of successful comedies: Blazing Saddles and Young Frankenstein (both 1974), Silent Movie (1976), High Anxiety (1977), History of the World, Part I (1981) and Spaceballs (1987).[2] His musical adaptation of The Producers ran on Broadway from 2001 to 2007 and won 12 Tony Awards. It was adapted as a film in 2005. Through his company, Brooksfilms, he produced David Lynch's The Elephant Man (1980), David Cronenberg's The Fly (1986) and David Jones's 84 Charing Cross Road (1987). With Anne Bancroft, he starred in To Be or Not To Be (1983), a remake of Ernst Lubitsch's 1942 film.
</excerpt>

## Search 3
query: "Mel Brooks Golden Globe award"
<excerpt title="List of awards and nominations received by Mel Brooks">
Mel Brooks is an American actor, writer, director, producer, comedian, and composer. Over his 70 year career in film, theatre, and television Brooks has won an Academy Award (plus an Academy Honorary Award), four Emmy Awards, three Tony Awards, three Grammy Awards, and has been nominated for six Golden Globe Awards and one BAFTA Award. With his Tony wins for _The Producers_ in 2001, he became one of only eight people (now 21) who have won an Emmy, Grammy, Oscar and Tony Award.[[1]](https://en.wikipedia.org/wiki/List_of_awards_and_nominations_received_by_Mel_Brooks#cite_note-2) Additionally, he has received a Kennedy Center Honor in 2009, a Hollywood Walk of Fame star in 2010, the 41st AFI Life Achievement Award in 2013, a British Film Institute Fellowship in 2015, a National Medal of Arts in 2016, and a BAFTA Fellowship in 2017.
Brooks won the Academy Award for Best Original Screenplay for his satirical black comedy film _The Producers_ (1967) and was nominated for the Academy Award for Best Adapted Screenplay for the comedy horror film _Young Frankenstein_ (1974) and Best Original Song for the title theme to Western comedy film _Blazing Saddles_ (1974). He was nominated for the BAFTA Award for Best Screenplay for _Blazing Saddles_. Brooks has received six competitive Golden Globe Award nominations without a win. He won two Writers Guild of America Awards for Best Original Screenplay for _The Producers_ and _Blazing Saddles_.
He adapted _The Producers_ into a commercially and critically successful 2001 musical on Broadway starring Nathan Lane and Matthew Broderick. At the 55th Tony Awards he received three Tony Awards for Best Musical, Best Book of a Musical, and Best Original Score. Brooks also received three Drama Desk Awards, a Drama League Award, a New York Film Critics Circle Award, and two Outer Critics Circle Awards. The production transferred to the West End in London where Brooks won the Laurence Olivier Award for Best New Musical in 2005.

For his work on television he received the Primetime Emmy Award Outstanding Writing for a Variety Series for the CBS variety special _The Sid Caesar, Imogene Coca, Carl Reiner, Howard Morris Special_ (1967) and as well as three Primetime Emmy Awards for Outstanding Guest Actor in a Comedy Series for the NBCsitcom_Mad About You_ in 1997, 1998, and 1999. Brooks earned three Grammy Awards; for Best Comedy Album for _The 2000 Year Old Man in the Year 2000_, Best Musical Theater Album for _The Producers_, and Best Music Film for _Recording The Producers_.
| Year | Category | Nominated work | Result | Ref. |  
| --- | --- | --- | --- | --- |  
| 1969 | Best Original Screenplay | _The Producers_ | Won | [[2]](https://en.wikipedia.org/wiki/List_of_awards_and_nominations_received_by_Mel_Brooks#cite_note-3) |  
| 1975 | Best Adapted Screenplay | _Young Frankenstein_ | Nominated | [[3]](https://en.wikipedia.org/wiki/List_of_awards_and_nominations_received_by_Mel_Brooks#cite_note-4) |  
| Best Original Song | "Blazing Saddles", _Blazing Saddles_ | Nominated |  
| 2023 | Academy Honorary Award | N/a | Honored |
**Directed Academy Award performances**
Under Brooks' direction, these actors have received Academy Award nominations for their performances in their respective roles.
| Year | Performer | Film | Result |  
| --- | --- | --- | --- |  
| Academy Award for Best Supporting Actor |  
| 1969 | Gene Wilder | _The Producers_ | Nominated |  
| Academy Award for Best Supporting Actress |  
| 1975 | Madeline Kahn | _Blazing Saddles_ | Nominated |
</excerpt>

## Search 4
query: "Dom DeLuise Walk of Fame Emmy Golden Globe"
<excerpt title="DeLuise, Dom 1933">
## DeLuise, Dom 1933–
**(Dom De Luise, Dom Deluise, Dom DeLuises)**

## PERSONAL
Full name, Dominick DeLuise; born August 1, 1933, in Brooklyn, New York, NY; son of John (a civil servant) and Vincenza "Jennie" (maiden name, DeStefano) DeLuise; married Carol Arthur (an actress; original name, Carol Arata), November 23, 1965; children: Peter John (an actor), Michael Robert (an actor), David Dominick (an actor). _Education:_ Attended Tufts University and School of Performing Arts, New York City. _Avocational Interests:_ Furniture refinishing, herb gardening.
**Addresses:**_Agent_—Artists Group, 10100 Santa Monica Blvd., Suite 2490, Los Angeles, CA 90067. _Contact_— c/o P.O. Box 1801, Pacific Palisades, CA 90272.
**Career:** Actor, director, writer, and commercial spokesperson. Worked as a chef. Also known as Dom De Luise.
**Awards, Honors:** Golden Globe Award nomination, best television actor—musical/comedy, 1974, for _Lotsa Luck;_ named king of Brooklyn, Welcome Back to Brooklyn Festival, 1984; Daytime Emmy Award nomination, outstanding performer in an animated program, 1999, for _All Dogs Go to Heaven: The Series;_ received a star on the Hollywood Walk of Fame, motion picture category.

## CREDITS
### **Film Appearances:**
Marvin Rollins, _Diary of a Bachelor_, American International Pictures, 1964.
Sergeant Collins, _Fail Safe_, Columbia, 1964.
Julius Pritter, _The Glass Bottom Boat_ (also known as _The Spy in Lace Panties_), Metro-Goldwyn-Mayer, 1966.
Kurt Brock, _The Busybody_, Paramount, 1967.
J. Gardner Monroe, _What's So Bad About Feeling Good?_, Universal, 1968.
Father Fyodor, _The Twelve Chairs_, Universal Marion Corporation (UMC), 1969.
Bill Bird, _Norwood_, Paramount, 1970.
Irwin, _Who Is Harry Kellerman and Why Is He Saying Those Terrible Things about Me?_, National General, 1971.
Azzecca, _Every Little Crook and Nanny_, Metro-Goldwyn-Mayer, 1972.
Buddy Bizarre, _Blazing Saddles_, Warner Bros., 1974.
Eduardo Gambetti, _The Adventures of Sherlock Holmes's Smarter Brother_ (also known as _Sherlock Holmes' Smarter Brother_), Twentieth Century-Fox, 1975.
Dom Bell, _Silent Movie_, Twentieth Century-Fox, 1976.
Zitz, _The World's Greatest Lover_, Twentieth Century-Fox, 1977.
Dan Turner, _Sextette_, Crown International Pictures, 1978.
Marlon Borunki, _The End_, United Artists, 1978.
Pepe Damascus, _The Cheap Detective_ (also known as _Neil Simon's "The Cheap Detective"_), Columbia, 1978.
Bernie (the Hollywood agent), _The Muppet Movie_, Associated Film Distribution, 1979.
Ernie Fortunato, _Hot Stuff_, Columbia, 1979.
Doc, _Smokey and the Bandit II_ (also known as _Smokey and the Bandit Ride Again_), Columbia, 1980.
Dominick DiNapoli, _Fatso_, Twentieth Century-Fox, 1980.
</excerpt>

## Search 5
query: ""county fair" "The Muppet Movie" cameo"
<excerpt title="The Muppet Movie">
*   Charles Durning as Doc Hopper, a businessman, entrepreneur, and restaurateur.  
*   Austin Pendleton as Max, Doc Hopper's shy right-hand man and sidekick.  
*   Scott Walker as Snake Walker, an assassin who specializes in killing frogs.  
*   H.B. Haggerty as Lumberjack  
*   Bruce Kirby as Gate Guard  
*   James Frawley as a Waiter at El Sleezo Café where Fozzie is doing his act

*   Jim Henson as Kermit the Frog, Rowlf the Dog, Dr. Teeth, Waldorf and The Swedish Chef  
*   Frank Oz as Miss Piggy, Fozzie Bear, Animal, Sam Eagle and Marvin Suggs  
*   Jerry Nelson as Floyd Pepper, Crazy Harry, Robin the Frog, Lew Zealand and Camilla the Chicken  
*   Richard Hunt as Scooter, Statler, Janice, Sweetums and Beaker  
*   Dave Goelz as The Great Gonzo, Zoot, Dr. Bunsen Honeydew and Doglion  
*   Caroll Spinney as Big Bird
Oz appears in a cameo as a biker who beats up Fozzie Bear[[9]](https://en.wikipedia.org/wiki/The_Muppet_Movie#cite_note-:22-10) while Steve Whitmire appears as a man in the Bogen County Fair.

### Special guest stars (in order of appearance)
[edit]
*   Dom DeLuise as Bernie, a Hollywood agent who meets Kermit in the swamp. The character's name alludes to Bernie Brillstein, talent agent and producer of the original _Muppet Show_.  
*   James Coburn as the El Sleezo Café Owner  
*   Madeline Kahn as an El Sleezo Patron with the same rhotacism and personality Kahn used for Lili von Shtupp in _Blazing Saddles_  
*   Telly Savalas as El Sleezo Tough  
*   Carol Kane as the lisping "miss" (summoned by the word “myth”)  
*   Paul Williams as the El Sleezo Pianist.  
*   Milton Berle as Mad Man Mooney, a used car salesman who employs Sweetums as a jack.  
*   Elliott Gould as the Compère who announces Miss Piggy as the winner of the Bogen County Beauty Pageant.  
*   Edgar Bergen as himself and Charlie McCarthy playing judges at the County Fair. This appearance marks Bergen's last film; he died soon after. The film was dedicated in his memory.  
*   Bob Hope as an Ice Cream Vendor who serves cones to Fozzie at the County Fair.  
*   Richard Pryor as a Balloon Vendor who sells balloons to Gonzo at the County Fair.  
*   Steve Martin as an insolent waiter working at the restaurant where Rowlf plays piano.  
*   Mel Brooks as Professor Krassman, a mad scientist hired by Doc Hopper.  
*   Cloris Leachman as Miss Tracy, Lew Lord's secretary who is allergic to animals.  
*   Orson Welles as Lew Lord, a Hollywood producer and studio executive. The character's name alludes to Sir Lew Grade, head of ATV, the British company that co-produced _The Muppet Show_.

### Special guest stars (in order of appearance)
After the popularity of the Muppets had grown following the success of _The Muppet Show_, Lew Grade agreed to finance the production of the film and signed the deal with his company ITC Entertainment,[[10]](https://en.wikipedia.org/wiki/The_Muppet_Movie#cite_note-FOOTNOTEDurrett199472-11) which helped Jim Henson finance the film.[[11]](https://en.wikipedia.org/wiki/The_Muppet_Movie#cite_note-12) After the film's production greenlit, Jim Henson and selected team members traveled to California various times to develop the script, music, and infrastructure in Hollywood to shoot the film.[[12]](https://en.wikipedia.org/wiki/The_Muppet_Movie#cite_note-:6-13)James Frawley was hired to direct the movie due to the film's challenges.[[12]](https://en.wikipedia.org/wiki/The_Muppet_Movie#cite_note-:6-13)
</excerpt>

## Search 6
query: "Bob Hope Golden Globe award"
<excerpt title="List of awards and nominations received by Bob Hope">
### Golden Globe Awards
[edit]
*   Special Achievement Award 1958 "For an Ambassador of Good Will."[[29]](https://en.wikipedia.org/wiki/List_of_awards_and_nominations_received_by_Bob_Hope#cite_note-29)  
*   Cecil B. DeMille Award 1963 [[30]](https://en.wikipedia.org/wiki/List_of_awards_and_nominations_received_by_Bob_Hope#cite_note-30)
Hope received more than 50 honorary degrees. These include:

### Golden Globe Awards
| Country | Date | School | Degree |  
| --- | --- | --- | --- |  
| Illinois | **8 June 1958** | Quincy University | Doctor of Letters (D.Litt.) |  
| District of Columbia | **4 June 1962** | Georgetown University | Doctor of Humane Letters (DHL) |  
| Wyoming | **1 June 1964** | University of Wyoming | Doctor of Laws (LL.D.) |  
| New Jersey | **5 June 1965** | Monmouth College | Doctor of Humane Letters (DHL) |  
| California | **12 June 1965** | Whittier College | Doctor of Humane Letters (DHL) |  
| Pennsylvania | **29 January 1966** | Pennsylvania Military College | Doctor of Humane Letters (DHL) |  
| Illinois | **11 June 1966** | Northwestern University | Doctor of Laws (LL.D.) |  
| Texas | **3 April 1967** | Southern Methodist University | Doctor of Humane Letters (DHL) |  
| Rhode Island | **3 June 1968** | Brown University | Doctor of Fine Arts (DFA) |  
| Ohio | **1 September 1968** | Ohio Dominican University | Doctor of Humane Letters (DHL) |  
| Ohio | **27 April 1969** | Miami University | Doctor of Humane Letters (DHL) |  
| Ohio | **7 June 1969** | Ohio State University | Doctor of Humane Letters (DHL) |  
| Ohio | **14 June 1969** | Bowling Green State University | Doctor of Humane Letters (DHL) |  
| Ohio | **22 April 1970** | University of Cincinnati | Doctor of Humane Letters (DHL) |  
| Vermont | **7 June 1970** | [Saint Michael's College](https://en.wikipedia.org/wiki/Saint_Michael's_College "Saint Michael's College") | Doctor of Humane Letters (DHL) |  
| New York | **8 June 1970** | Pace College | Doctor of Laws (LL.D.) |
</excerpt>

## Search 7
query: "Milton Berle Emmy award Golden Globe award"
<excerpt title="Milton Berle - Comedians">
Milton Berle was an American comedian and actor.
Berle's career as an entertainer spanned over 80 years, first in silent films and on stage as a child actor, then in radio, movies and television. As the host of NBC's Texaco Star Theatre (1948-55), he was the first major American television star and was known to millions of viewers as "Uncle Miltie" and "Mr. Television" during the first Golden Age of Television. He was honored with two stars on the Hollywood Walk of Fame for his work in both radio and TV.
Berle won the Emmy for Most Outstanding Kinescoped Personality in 1950. In 1979, Berle was awarded a special Emmy Award, titled "Mr. Television." He was twice nominated for Emmys for his acting, in 1962 and 1995.
Berle was inducted into the Television Hall of Fame in 1984. On December 5, 2007, Berle was inducted into the California Hall of Fame.
</excerpt>

## Search 8
query: "Cloris Leachman walk of fame"
<excerpt title="Cloris Leachman">
## Acting credits and awards
[edit]
*   Leachman was inducted into the Television Academy Hall of Fame in 2011. That same year, she was ranked number 23 on the TV Guide Network special _Funniest Women on TV_.[[39]](https://en.wikipedia.org/wiki/Cloris_Leachman#cite_note-39)  
*   On June 20, 2014, Leachman received an honorary degree from her alma mater, Northwestern University.[[40]](https://en.wikipedia.org/wiki/Cloris_Leachman#cite_note-40)  
*   In 2017, she received PETA's Lifetime Achievement Award for her dedication to animal-rights issues.[[41]](https://en.wikipedia.org/wiki/Cloris_Leachman#cite_note-41)  
*   She was awarded a Star on the Hollywood Walk of Fame in the Television Category on September 22, 1980, at 6435 Hollywood Boulevard.[[42]](https://en.wikipedia.org/wiki/Cloris_Leachman#cite_note-42)
Leachman in November 2015
From 1953 to 1978, Leachman was married to Hollywood impresarioGeorge Englund. Her former mother-in-law was character actress Mabel Albertson. The marriage produced four sons and one daughter: Bryan (died 1986), Morgan, Adam, Dinah, and George. Some of them are in show business. Her son Morgan played Dylan on _Guiding Light_ for several years. The Englunds were Bel Air neighbors of Judy Garland, Sidney Luft, and their children, Lorna and Joey Luft, during the early 1960s. Lorna Luft stated in her memoir _Me and My Shadows: A Family Memoir_ that Leachman was "the kind of mom I'd only seen on TV". Knowing of the turmoil at the Luft home, but never mentioning it, Leachman prepared meals for the children and made them feel welcome when they needed a place to stay.[[43]](https://en.wikipedia.org/wiki/Cloris_Leachman#cite_note-43)

## Acting credits and awards
Leachman was also a friend of Mort Sahl and Marlon Brando, whom she met while studying under Elia Kazan in the 1950s. She introduced him to her husband, who became close to Brando, as well, directing him in _The Ugly American_ (1963) and writing a memoir about their friendship called _Marlon Brando: The Way It's Never Been Done Before_ (2005).[[44]](https://en.wikipedia.org/wiki/Cloris_Leachman#cite_note-44)
Leachman was a vegetarian and an animal rights activist. In 1997, she appeared on the cover of _Alternative Medicine Digest_, posing nude while body-painted with images of fruit in a parody of Demi Moore's 1991 _Vanity Fair_ cover photo._[citation needed_] She also posed clad in a dress made of lettuce for a 2009 PETA advertisement.[[45]](https://en.wikipedia.org/wiki/Cloris_Leachman#cite_note-45) In 2013, she starred in a comedic PETA ad on spay and neuter in which she opened a condom wrapper with her teeth.[[46]](https://en.wikipedia.org/wiki/Cloris_Leachman#cite_note-46) Leachman's granddaughter, Anabel Englund, is a singer.[[47]](https://en.wikipedia.org/wiki/Cloris_Leachman#cite_note-47) In addition to Anabel, Leachman had other grandchildren, and one great-grandson, Braden.[[48]](https://en.wikipedia.org/wiki/Cloris_Leachman#cite_note-48) Leachman was an atheist.[[49]](https://en.wikipedia.org/wiki/Cloris_Leachman#cite_note-49)
</excerpt>

## Search 9
query: "Dom DeLuise walk of fame"
<excerpt title="Dom DeLuise: 1933-2009">
May 5, 2009 / 1:17 PM EDT / CBS News
Add CBS News on Google
AP
Dom DeLuise, the portly actor-comedian whose affable nature made him a popular character actor in movies, TV shows and plays, died in his sleep on May 4, 2009. He was 75.
AP Photo
Actor Dom DeLuise, a graduate of New York City's famed School of Performing Arts, points to his star on the Hollywood Walk of Fame on Hollywood Boulevard at a nighttime ceremony on Monday, May 7, 1985. As an actor, he was incredibly prolific, appearing in scores of movies and TV shows, in Broadway plays and voicing characters for numerous cartoon shows.
AP
Dom DeLuise, star and director of the action-comedy movie "Hot Stuff," is shown during filming in Miami, Fla., in Oct. 1978.
AP
Actor Burt Reynolds, right, pinches the cheeks of comedian Dom DeLuise in Atlanta, Dec. 2, 1977, during a "roast" of Reynolds by various celebrities. The two were friends and frequently appeared in films together, among them, "The End," "The Best Little Whorehouse in Texas," "Smokey and the Bandit II," "The Cannonball Run" and "Cannonball Run II."
AP Photo/20th Century Fox
Burt Reynolds, left, and Dom DeLuise are shown in a scene from, "Cannonball Run."
AP Photo
Dom DeLuise poses at the Sahara Hotel in Las Vegas,July 26, 1978. DeLuise was appearing on Broadway in "Here's Love" in the early 1960s when Garry Moore saw him and hired him to play the magician "0000Dominick the Great" on "0000The Garry Moore Show." His appearances on the hit comedy-variety program brought offers from Hollywood.
AP
Comedian Dom DeLuise sits in his director's chair while working on the film, "Hot Stuff." He and his wife, actress Carol Arthur, had three sons, all of whom became actors.
20th Century Fox/AP

Dom DeLuise is shown in a scene from Mel Brooks' "History of the World Part I." Writer-director-actor Brooks particularly admired DeLuise's talent for offbeat comedy and cast him in several of his films, including "Blazing Saddles."
AP
Dom DeLuise is shown at Disneyland in Anaheim, Calif., in this 1988 file photo. DeLuise died in Southern California on Monday, May 4, according to his son, Michael DeLuise. He was 75.
AP
Actor and comedian Dom DeLuise is shown in November of 1987. The actor, who loved to cook and eat almost as much as he enjoyed acting, also carved out a formidable second career later in life as a chef of fine cuisine. He authored two cookbooks and would appear often on morning TV shows to whip up his favorite recipes
</excerpt>

## Search 10
query: "Milton Berle Golden Globe award winner"
<excerpt title="Milton Berle">
## Selected filmography
*   1969: _Can Heironymus Merkin Ever Forget Mercy Humppe and Find True Happiness?_ as Goodtime Eddie Filth  
*   1969: _Seven in Darkness_ as Sam Fuller  
*   1971: _That Girl_ (Season 5, Episode 15, Those Friars) as himself  
*   1972: _Evil Roy Slade_ as Harry Fern  
*   1972: _Journey Back to Oz_ as The Cowardly Lion (voice)  
*   1975: _Lepke_ as Mr. Meyer  
*   1976: _Won Ton Ton, the Dog Who Saved Hollywood_ as Blind Man  
*   1976: _[Let's Make a Deal](https://en.wikipedia.org/wiki/Let's\_Make\_a\_Deal "Let's Make a Deal")_ (playing for a home viewer)  
*   1978: _Hey, Abbott!_ as himself (voice)  
*   1979: _The Muppet Movie_ as Mad Man Mooney  
*   1980: _CHiPs_ as himself  
*   1981: _General Hospital_ as Micky Miller  
*   1981: _The Fall Guy_  
*   1983: _Cracking Up_ as Ms. Sultry  
*   1984: _Broadway Danny Rose_ as himself  
*   1984: _The 1st TV Academy Hall of Fame_ as himself/winner  
*   1984: Music Video with Ratt & Milton Berle, "Round and Round"  
*   1985: _[Pee-wee's Big Adventure](https://en.wikipedia.org/wiki/Pee-wee's\_Big\_Adventure "Pee-wee's Big Adventure")_ as himself (uncredited)  
*   1985: _Amazing Stories_ as himself  
*   1988: _Side by Side_ as Abe Mercer  
*   1989: _Going Overboard_ as himself (uncredited)  
*   1991: _Trabbi Goes to Hollywood_ as Hotel Clerk  

## Selected filmography
*   1991: _Shakes the Clown_ as Male Clown Barfly (uncredited)  
*   1992: _The Fresh Prince of Bel-Air_ as Max Jakey  
*   1992: _The Real Story of Au Clair De La Lune_ as The Prince of Darkness (voice)  
*   1993: _Matlock_ "The Last Laugh" as Harvey Chase  
*   1995: _Beverly Hills, 90210_ as Saul Howard  
*   1995: _The Nanny_ as Uncle Manny  
*   1995: _Roseanne_ as Transvestite at Wedding (uncredited)  
*   1995: _The 4th of July Parade_ as Ice Cream Man  
*   1996: _Due South_ as Shelley Litvak  
*   1996: _Storybook_ as Illuzor  
*   1996: _Sister, Sister_ (TV Series) The Volunteers as Edgar Boggs  
*   2000: _Kenan & Kel_ as Uncle Leo (final film role)
</excerpt>

# Example 5
## Question
Of the natural sites on the UNESCO list of World Heritage in Danger, only a few sites are located in one of the original members of the United Nations. In which country is the site with the largest reported area according to Protected Planet?

## Expected answer
Mexico

## Final answer — grade 0.00
The natural site that sits in a founding‑member country and boasts the largest area on the list, according to Protected Planet’s reported size, is the **Great Barrier Reef – Australia**.
(10 searches; ended: answered)

## Search 1
query: "original members of the United Nations 51 founding members 1945 list"
<excerpt title="Growth in United Nations membership">
### Original 51 Members(1945)
Argentina, Australia, Belgium,Bolivia, Brazil, Byelorussian Soviet Socialist Republic, Canada, Chile, China, Colombia, Costa Rica, Cuba, Czechoslovakia, Denmark, Dominican Republic, Ecuador, Egypt, El Salvador, Ethiopia, France, Greece, Guatemala, Haiti, Honduras, India, Iran, Iraq, Lebanon, Liberia, Luxembourg, Mexico, Netherlands, New Zealand, Nicaragua, Norway, Panama, Paraguay, Peru, Philippine Republic, Poland, Saudi Arabia, Syria, Turkey, Ukrainian Soviet Socialist Republic, Union of South Africa, Union of Soviet Socialist Republics, United Kingdom, United States, Uruguay, Venezuela, Yugoslavia

### 55 Members(1946)
**Added:**Afghanistan, Iceland, Siam,Sweden

### 57 Members(1947)
**Added:**Pakistan, Yemen(the Yemen Arab Republic)

### 59 Members (1949)
**Added:**Israel

### 76 Members(1955)
**Added:**Albania, Austria, Bulgaria, Cambodia, Ceylon, Finland, Hungary, Ireland, Italy, Jordan, Laos, Libya, Nepal, Portugal, Romania, Spain

### 80 Members (1956)
**Added:**Japan, Morocco, Sudan, Tunisia

### 82 Members (1958)*
**Added:**Guinea
*On 22 February 1958,Syriamerged withEgypt(both original members of the United Nations)to become the United Arab Republic.

### 99 Members (1960)
**Added:**Cameroun, Central African Republic, Chad, Congo (Brazzaville), Congo (Leopoldville), Cyprus, Dahomey, Gabon, Ivory Coast, Malagasy Republic, Mali, Niger, Nigeria, Senegal, Somalia, Togo, Upper Volta

### 104 Members(1961)*
**Added:**Mauritania, Mongolia, Sierra Leone, Tanganyika
*On 13 October 1961,Syria, having resumed its status as an independent State from the United Arab Republic, resumed its separate membership in the United Nations.

### 110 Members (1962)
**Added:**Algeria, Burundi, Jamaica, Rwanda, Trinidad and Tobago, Uganda

### 117 Members (1965)*
**Added:**The Gambia, Maldive Islands, Singapore
*On 20 January 1965, Indonesia temporarily withdrew from the United Nations.

### 122 Members (1966)*
**Added:**Barbados, Botswana, Guyana, Lesotho
* On 28 September 1966, Indonesiarejoined the United Nations.

### 123 Members (1967)
**Added:**Yemen(People's Democratic Republic of Yemen)

### 126 Members(1968)
**Added:**Equatorial Guinea, Mauritius, Swaziland

### 127 Members (1970)
**Added:**Fiji

### 132 Members (1971)
**Added:**Bahrain, Bhutan, Oman, Qatar, United Arab Emirates

### 138 Members (1974)
**Added:**Bangladesh, Grenada, Guinea-Bissau

### 144 Members (1975)
**Added:**Cape Verde, Comoros, Mozambique, Papua New Guinea, Sao Tome and Principe, Suriname

### 147 Members (1976)
**Added:**Angola, Samoa, Seychelles

### 149 Members(1977)
**Added:**Djibouti, Viet Nam

### 151 Members(1978)
**Added:**Dominica, Solomon Islands

### 152 Members (1979)
**Added:**Saint Lucia

### 154 Members (1980)
**Added:**Saint Vincent and the Grenadines, Zimbabwe

### 157 Members(1981)
**Added:**Antigua and Barbuda, Belize, Vanuatu

### 159 Members(1984)
**Added:**Brunei Darussalam
</excerpt>

## Search 2
query: "UNESCO World Heritage in Danger natural sites list 2024 protected planet area largest"
<excerpt title="List of World Heritage in Danger">
This site was home to the prestigious Koranic Sankore University. Timbuktu became a religious and cultural center from the 15th to the 16th centuries AD, as well as a center for the spread of Islamic culture in Africa. The three great mosques of Djinguereber, Sankore, and Sidi Yahia reflect the golden age of Timbuktu. Although these monuments have been continuously restored, they are still threatened today by sand encroachment.
Timbuktu
20. Tomb of Askia
State Party: Mali. Inscribed as a cultural heritage site in July 2004. Inscribed on the List of World Heritage in Danger in 2012. Criteria: (ii)(iii)(iv)
22
The Tomb of Askia is an impressive 17-meter-high pyramidal structure built in 1495 by Askia Mohamed, Emperor of the Songhai Empire, in his capital Gao. The tomb testifies to the power, wealth, and prosperity of the empire from the 15th to the 16th centuries. At that time, the Songhai Empire controlled trans-Saharan trade, particularly in salt and gold. It is also a significant example of the earthen building tradition in the West African Sahel. The Tomb of Askia comprises the pyramidal tomb, two flat-roofed mosque buildings, a mosque cemetery, and an open-air assembly ground. These were constructed after Askia Mohamed's return from Mecca, when he established Islam as the state religion and made Gao his capital.
Tomb of Askia
Area of the heritage site: 4.24 hectares. Buffer zone: 83 hectares
21. Old Towns of Djenné
State Party: Mali. Inscribed as a cultural heritage site in December 1988. Inscribed on the List of World Heritage in Danger in 2016. Criteria: (iii)(iv)
Djenné has been inhabited since 250 BC and later developed into a market center and an important hub for the trans-Saharan gold trade. Between the 15th and 16th centuries, Djenné became a center for the propagation of Islam. Approximately 2,000 ancient buildings within the town have been well preserved. These structures are built on small hills to protect against seasonal floods.
Old Towns of Djenné

22. Air and Ténéré Natural Reserves
Country: Niger Inscribed as a Natural Heritage site: December 1991 Listed as a World Heritage in Danger: 1992 Criteria: (vii)(ix)(x)
23
The Air and Ténéré Natural Reserves constitute the largest protected area in Africa, covering approximately 7.7 million hectares, although only about one-sixth of this area is considered to have significant conservation value. The site includes the volcanic massif of the Air and a small Sahelian region, which, despite being located in the Ténéré desert of the Sahara, exhibits a climate, fauna, and flora distinctly different from the surrounding areas. The Air and Ténéré Natural Reserves are noted for their diverse environments, varied flora, and wildlife.
Air and Ténéré Natural Reserves
Protected area: 7,736,000 hectares
23. Birthplace of Jesus: Church of the Nativity and the Pilgrimage Route, Bethlehem
Country: Palestine Inscribed as a Cultural Heritage site and a World Heritage in Danger: July 2012 Criteria: (iv)(vi)
24
This inscribed property is located 10 kilometers south of Jerusalem and has been recognized by Christian tradition as the birthplace of Jesus since the 2nd century AD. The first church was constructed on the site in 339 AD. Following a fire in the 6th century, the church rebuilt on its foundations retained the original building's exquisite mosaic floors. The property also includes Latin, Greek Orthodox, Franciscan, and Armenian monasteries and churches, as well as bell towers, terraced gardens, and a pilgrimage route.
Birthplace of Jesus: Church of the Nativity and the Pilgrimage Route, Bethlehem
Protected area: 2.98 hectares Buffer zone: 23 hectares
24. Palestine: Land of Olives and Vines – Cultural Landscape of Southern Jerusalem, Battir
Country: Palestine Inscribed as a Cultural Landscape and a World Heritage in Danger: July 2014 Criteria: (iv)(v)
25
</excerpt>

## Search 3
query: "UNESCO natural World Heritage in Danger list 2026 protected planet area"
<excerpt title="Natural World Heritage">
# Natural World Heritage
## Focus Areas
Forests
Marine Ecosystems
Priority Africa
Climate Change
Corporate sector and the World Heritage ‘no-go’ commitment
Emergency Situations
Communities
Biodiversity

# Natural World Heritage
## Nature’s most precious gifts
to humanity
Natural World Heritage sites contain some of the Earth's most valuable natural areas recognized as being of Outstanding Universal Value (OUV) to humanity for their global significance to nature conservation. To date, there are 266 natural sites inscribed on the UNESCO World Heritage List, including 218 sites recognized for their natural value and 39 mixed sites (recognized under both natural and cultural criteria). The World Heritage Convention sets the highest international standards for the integrity, protection and management of around 3,500,000 km2 (more than the size of India) across more than 100 countries.
Ranging in size from less than 1 km 2 in Vallée de Mai (Seychelles) to almost 700,000 km 2 in French Austral Lands and Seas (France), natural World Heritage sites harbour provide crucial habitats to many iconic species and harbor unique natural beauty, stunning landscapes, rare ecological processes, and exceptional biodiversity. These sites include many iconic places such as the Serengeti National Park (Tanzania) that hosts the largest terrestrial mammal migration in the world, the living museum of evolution of Galápagos Islands (Ecuador), Yellowstone National Park (United States of America) known for its wildlife and its many geothermal features and the world's largest coral reef system at Great Barrier Reef (Australia).

# Natural World Heritage
## Nature’s most precious gifts
Natural World Heritage sites are critical for the conservation of ecosystem integrity and biodiversity. While they make up less than 1% of the Earth’s surface, they harbor more than 1/5 of mapped global species richness. This includes over 75,000 species of plants, and over 30,000 species of mammals, birds, fishes, reptiles and amphibians. These sites also represent a safe haven for some of the most threatened species on Earth. They are estimated to protect over 20,000 globally threatened species, including some of the last individuals of many iconic species. Today, up to 1/3 of remaining elephants, tigers and pandas can be found in these sites, as well as at least 1 in 10 great apes, giraffes, lions and rhinos. For some species on the brink of extinction, World Heritage sites have become the last line of defense. They are home to all remaining Javan rhinos, vaquitas (the world's smallest cetacean) and pink iguanas, as well as more than half of all Sumatran rhinos, Sumatran orangutans and mountain gorillas.
Millions of people are directly dependent on the countless benefits and services these sites can provide, supporting livelihoods and wellbeing. Over 90% of listed natural sites create jobs and provide income from tourism and recreation. Two-thirds of natural sites are crucial sources of water, and about half help prevent hazards such as floods or landslides. They also have a central role in climate regulation and carbon sequestration as World Heritage forests absorb approximately 190 million tons of CO2 each year (equivalent to half the United Kingdom’s annual CO2 emissions from fossil fuels). Marine and coastal sites are also critical to mitigating climate impacts storing 1.3 billion tons of carbon (known as blue carbon) in seagrass meadows, tidal marshes and mangroves, representing 15% of global blue carbon assets.
</excerpt>

## Search 4
query: "UNESCO World Heritage in Danger natural sites list 2024"
<excerpt title="Natural World Heritage">
# Natural World Heritage
## Focus Areas
Forests
Marine Ecosystems
Priority Africa
Climate Change
Corporate sector and the World Heritage ‘no-go’ commitment
Emergency Situations
Communities
Biodiversity

# Natural World Heritage
## Nature’s most precious gifts
to humanity
Natural World Heritage sites contain some of the Earth's most valuable natural areas recognized as being of Outstanding Universal Value (OUV) to humanity for their global significance to nature conservation. To date, there are 266 natural sites inscribed on the UNESCO World Heritage List, including 218 sites recognized for their natural value and 39 mixed sites (recognized under both natural and cultural criteria). The World Heritage Convention sets the highest international standards for the integrity, protection and management of around 3,500,000 km2 (more than the size of India) across more than 100 countries.
Ranging in size from less than 1 km 2 in Vallée de Mai (Seychelles) to almost 700,000 km 2 in French Austral Lands and Seas (France), natural World Heritage sites harbour provide crucial habitats to many iconic species and harbor unique natural beauty, stunning landscapes, rare ecological processes, and exceptional biodiversity. These sites include many iconic places such as the Serengeti National Park (Tanzania) that hosts the largest terrestrial mammal migration in the world, the living museum of evolution of Galápagos Islands (Ecuador), Yellowstone National Park (United States of America) known for its wildlife and its many geothermal features and the world's largest coral reef system at Great Barrier Reef (Australia).

# Natural World Heritage
## Nature’s most precious gifts
Natural World Heritage sites are critical for the conservation of ecosystem integrity and biodiversity. While they make up less than 1% of the Earth’s surface, they harbor more than 1/5 of mapped global species richness. This includes over 75,000 species of plants, and over 30,000 species of mammals, birds, fishes, reptiles and amphibians. These sites also represent a safe haven for some of the most threatened species on Earth. They are estimated to protect over 20,000 globally threatened species, including some of the last individuals of many iconic species. Today, up to 1/3 of remaining elephants, tigers and pandas can be found in these sites, as well as at least 1 in 10 great apes, giraffes, lions and rhinos. For some species on the brink of extinction, World Heritage sites have become the last line of defense. They are home to all remaining Javan rhinos, vaquitas (the world's smallest cetacean) and pink iguanas, as well as more than half of all Sumatran rhinos, Sumatran orangutans and mountain gorillas.
Millions of people are directly dependent on the countless benefits and services these sites can provide, supporting livelihoods and wellbeing. Over 90% of listed natural sites create jobs and provide income from tourism and recreation. Two-thirds of natural sites are crucial sources of water, and about half help prevent hazards such as floods or landslides. They also have a central role in climate regulation and carbon sequestration as World Heritage forests absorb approximately 190 million tons of CO2 each year (equivalent to half the United Kingdom’s annual CO2 emissions from fossil fuels). Marine and coastal sites are also critical to mitigating climate impacts storing 1.3 billion tons of carbon (known as blue carbon) in seagrass meadows, tidal marshes and mangroves, representing 15% of global blue carbon assets.
</excerpt>

## Search 5
query: "Protected Planet Great Barrier Reef area"
<excerpt title="Great Barrier Reef">
# Great Barrier Reef | Protected Planet
We use the necessary cookies to make our site work. We'd also like to set optional cookies that help us improve by measuring how you use the site and offering optional functionalities. These will be set only if you accept. For more detailed information about our cookies, see our Privacy policy page.
Accept Reject
**Protected Planet is evolving:** The Protected Planet Initiative has undergone some changes! Read about how we have brought together our flagship databases into the **World Database on Protected and Conserved Areas (WDPCA)** and expanded the **Global Database on Protected Area Management Effectiveness (GD-PAME)**here. Important changes to the Protected Planet API are summarized here.
*   About  
*   News & Stories  
*   Resources  
*   Update Tracker  
*   DataWorld Database on Protected and Conserved Areas (WDPCA)ICCA RegistryProtected and Conserved Area Effectiveness (GD-PAME)   
*   Thematic AreasProtected and Conserved AreasMarine Protected and Conserved AreasInternationally Designated AreasTerritories and areas governed by Indigenous Peoples and local communitiesEffectivenessEquitable GovernanceConnectivity 

*   About  
*   News & Stories  
*   Resources  
*   Update Tracker  
*   Data World Database on Protected and Conserved Areas (WDPCA)ICCA RegistryProtected and Conserved Area Effectiveness (GD-PAME)   
*   Thematic Areas Protected and Conserved AreasMarine Protected and Conserved AreasInternationally Designated AreasTerritories and areas governed by Indigenous Peoples and local communitiesEffectivenessEquitable GovernanceConnectivity
Download

# Great Barrier Reef
2571  SITE ID
348700.0 km²  Reported Area
Type  Marine and Coastal Protected Areas
Location Australia
Read an assessment of this site by visiting the IUCN World Heritage Outlook Link
© Mapbox© OpenStreetMapImprove this map
100 km
Terrain Satellite
Map Disclaimer
The designations employed and the presentation of material on this map do not imply the expression of any opinion whatsoever on the part of the Secretariat of the United Nations concerning the legal status of any country, territory, city or area or of its authorities, or concerning the delimitation of its frontiers or boundaries.
• Dotted line represents approximately the Line of Control in Jammu and Kashmir agreed upon by India and Pakistan. The final status of Jammu and Kashmir has not yet been agreed upon by the parties.
• Final boundary between the Republic of Sudan and the Republic of South Sudan has not yet been determined.
• Final status of the Abyei area is not yet determined.
• A dispute exists between the Governments of Argentina and the United Kingdom of Great Britain and Northern Ireland concerning sovereignty over the Falkland Islands (Malvinas).
Discover Protected Areas and OECMs
Map Disclaimer
The designations employed and the presentation of material on this map do not imply the expression of any opinion whatsoever on the part of the Secretariat of the United Nations concerning the legal status of any country, territory, city or area or of its authorities, or concerning the delimitation of its frontiers or boundaries.
• Dotted line represents approximately the Line of Control in Jammu and Kashmir agreed upon by India and Pakistan. The final status of Jammu and Kashmir has not yet been agreed upon by the parties.
• Final boundary between the Republic of Sudan and the Republic of South Sudan has not yet been determined.
• Final status of the Abyei area is not yet determined.
• A dispute exists between the Governments of Argentina and the United Kingdom of Great Britain and Northern Ireland concerning sovereignty over the Falkland Islands (Malvinas).

# Great Barrier Reef
## Attributes
*   Name La Grande Barrière  
*   English Name Great Barrier Reef  
*   English Designation World Heritage Site (natural or mixed)  
*   IUCN Management Category Not Applicable  
*   Status Inscribed  
*   Type of Designation International  
*   Status Year 1981  
*   Governance Type Not Reported  
*   Governance Subtype Not Applicable  
*   Management Authority Not Reported  
*   Management Plan Not Reported  
*   Ownership Type Not Reported  
*   Ownership Subtype Not Applicable  
*   International Criteria(ix);(vii);(viii);(x)  
*   Inland Waters Not Applicable  
*   Supplementary Information Not Applicable
</excerpt>

## Search 6
query: "List of World Heritage in Danger natural sites countries"
<excerpt title="Heritage at Risk: 4 UNESCO Sites Under Threat">
## **Impact of Climate Change and Human Destruction**
Despite their significance, UNESCO Heritage Sites face numerous challenges that threaten their integrity.
Rising temperatures, sea-level rise, and extreme weather events affect many sites, particularly natural ones.
The World Monument Fund (WMF) has identified that climate change is the predominant threat to sites in Sub-Saharan Africa, whereas urbanization and development pose the greatest risks to historical sites in Asia. The Great Barrier Reef, for example, is experiencing severe coral bleaching due to changing ocean conditions, which jeopardizes its biodiversity.
In Europe and North America, insufficient funding is the primary challenge, while overtourism significantly impacts sites in Latin America and the Caribbean. Human activities, such as overtourism, urban development, and industrialization, further contribute to the degradation of these sites. Venice, famous for its historic architecture and iconic canals, [is sinking](https://www.npr.org/2023/09/12/1197139620/venice-endangered-climate-change#:~:text=A%20UNESCO%20report%20says%20that,buildings%20and%20landscapes%20at%20risk.&text=In%20November%202019%2C%20floods%20endangered%20historical%20treasures%20and%20buildings.) due to both natural processes and human-induced factors, which threaten its cultural heritage.
In the Middle East and North Africa, the main concerns are armed conflict and a lack of local resources. For instance, the ongoing crisis in Syria has led to significant damage to ancient sites like Palmyra, underscoring the vulnerability of cultural heritage in times of turmoil.
But what are the UNESCO Heritage Sites most at risk? Earth.Org takes a look.

## **Impact of Climate Change and Human Destruction**
### **1. Great Barrier Reef, Australia**
The Great Barrier Reef is the world’s largest coral reef system, spanning over 2,300 kilometers along the northeastern coast of Australia. It is renowned for its biodiversity, housing thousands of species of marine life.
The reef is facing severe threats primarily due to climate change. Rising ocean temperatures have led to mass coral bleaching events, where corals expel the algae that provide them with nutrients and color.
Aerial image of the Great Barrier Reef. Photo: Tourism and Events Queensland.
According to the Australian Institute of Marine Science (AIMS), approximately half of the reef’s coral cover has been lost since 1995, with recent bleaching events further exacerbated by extreme weather patterns linked to climate change. In October, the National Oceanic and Atmospheric Administration (NOAA) confirmed that the current mass coral bleaching event affecting dozens of countries worldwide is now the largest event ever recorded.
Additionally, pollution from agricultural runoff and coastal development poses risks to the reef’s health.
**_More on the topic:_****_5 Coral Reefs That Are Currently Under Threat and Dying_**

## **Impact of Climate Change and Human Destruction**
### **2. The Galápagos Islands, Ecuador**
The Galápagos Islands, famous for their unique ecosystems, are threatened by invasive species, overfishing, and climate change. Invasive species such as goats and rats disrupt local ecosystems by preying on native wildlife and competing for resources.
For instance, the iconic Galápagos tortoise has faced significant population declines due to hunting, habitat destruction, and competition with invasive species like goats. As ecosystem engineers and large vertebrates, Galápagos tortoises play a crucial role in maintaining the health of the island’s ecosystems. Their sensitivity to environmental changes makes them valuable indicators of ecological disturbances. Conservation efforts are ongoing to protect and restore their populations.
Giant Galapagos Tortoise. Photo: Xavier Castro/Galápagos Conservancy.
A study published in 2021 by the Galápagos Conservancy highlights that these invasions have led to declines in native species populations. Furthermore, climate change is causing ocean acidification and rising sea levels, which threaten the delicate balance of the islands’ ecosystems.
</excerpt>

## Search 7
query: "natural sites on UNESCO List of World Heritage in Danger 2025 site name area"
<excerpt title="Natural World Heritage">
# Natural World Heritage
## Focus Areas
Forests
Marine Ecosystems
Priority Africa
Climate Change
Corporate sector and the World Heritage ‘no-go’ commitment
Emergency Situations
Communities
Biodiversity

# Natural World Heritage
## Nature’s most precious gifts
to humanity
Natural World Heritage sites contain some of the Earth's most valuable natural areas recognized as being of Outstanding Universal Value (OUV) to humanity for their global significance to nature conservation. To date, there are 266 natural sites inscribed on the UNESCO World Heritage List, including 218 sites recognized for their natural value and 39 mixed sites (recognized under both natural and cultural criteria). The World Heritage Convention sets the highest international standards for the integrity, protection and management of around 3,500,000 km2 (more than the size of India) across more than 100 countries.
Ranging in size from less than 1 km 2 in Vallée de Mai (Seychelles) to almost 700,000 km 2 in French Austral Lands and Seas (France), natural World Heritage sites harbour provide crucial habitats to many iconic species and harbor unique natural beauty, stunning landscapes, rare ecological processes, and exceptional biodiversity. These sites include many iconic places such as the Serengeti National Park (Tanzania) that hosts the largest terrestrial mammal migration in the world, the living museum of evolution of Galápagos Islands (Ecuador), Yellowstone National Park (United States of America) known for its wildlife and its many geothermal features and the world's largest coral reef system at Great Barrier Reef (Australia).

# Natural World Heritage
## Nature’s most precious gifts
Natural World Heritage sites are critical for the conservation of ecosystem integrity and biodiversity. While they make up less than 1% of the Earth’s surface, they harbor more than 1/5 of mapped global species richness. This includes over 75,000 species of plants, and over 30,000 species of mammals, birds, fishes, reptiles and amphibians. These sites also represent a safe haven for some of the most threatened species on Earth. They are estimated to protect over 20,000 globally threatened species, including some of the last individuals of many iconic species. Today, up to 1/3 of remaining elephants, tigers and pandas can be found in these sites, as well as at least 1 in 10 great apes, giraffes, lions and rhinos. For some species on the brink of extinction, World Heritage sites have become the last line of defense. They are home to all remaining Javan rhinos, vaquitas (the world's smallest cetacean) and pink iguanas, as well as more than half of all Sumatran rhinos, Sumatran orangutans and mountain gorillas.
Millions of people are directly dependent on the countless benefits and services these sites can provide, supporting livelihoods and wellbeing. Over 90% of listed natural sites create jobs and provide income from tourism and recreation. Two-thirds of natural sites are crucial sources of water, and about half help prevent hazards such as floods or landslides. They also have a central role in climate regulation and carbon sequestration as World Heritage forests absorb approximately 190 million tons of CO2 each year (equivalent to half the United Kingdom’s annual CO2 emissions from fossil fuels). Marine and coastal sites are also critical to mitigating climate impacts storing 1.3 billion tons of carbon (known as blue carbon) in seagrass meadows, tidal marshes and mangroves, representing 15% of global blue carbon assets.
</excerpt>

## Search 8
query: "List of World Heritage in Danger natural sites Wikipedia list 2026"
<excerpt title="56 Sites Are on UNESCO's List of ...">
### Everglades National Park, United States
**Donate:**Everglades National Park
Florida’s Everglades National Park is the largest subtropical wilderness in the United States; it has been a UNESCO World Heritage site since 1979. In 1993, the area was added to the in-danger list because of damage caused by Hurricane Andrew and then removed in 2007. However, the site was added back to the list in 2010 due to concerns over the deterioration of its aquatic ecosystem.
The breakdown of its ecosystem has been attributed to factors like pollution, lower water levels from neighboring agricultural activities, a reduction of marine and estuarine biodiversity, and changes in water flow volume.
You can see examples of Vienna’s baroque architecture at the Belvedere.
Photo by Mistervlad/Shutterstock

### Historic Centre of Vienna, Austria
Thanks to Vienna’s long history (which include its stint as the capital of the Austro-Hungarian Empire and its modern-day reputation as Europe’s music capital), you can find evidence of the Middle Ages, the baroque period, and the Gründerzeit era in the city’s streets.
The Historic Centre of Vienna was inscribed on the World Heritage List in 2001 because of its preserved architectural wonders from these time periods, which include baroque castles and its iconic ring road. In [2017](https://www.unesco.org/en/articles/historic-centre-vienna-inscribed-list-world-heritage-danger#:~:text=The%20World%20Heritage%20Committee%20has,middle%20of%20the%20Austrian%20capital.), UNESCO put this site on the in-danger list due to new high-rise constructions that “impact adversely the outstanding universal value of the site.”
Chan Chan was put on UNESCO’s in-danger list the same year it became a World Heritage site.
Photo by Matyas Rehak/Shutterstock

### Chan Chan Archaeological Zone, Peru
Chan Chan was the capital of the ancient Chimu Kingdom, a society that thrived for nearly 500 years before falling to the Incas in the 15th century. The archaeological zone—which covers nearly 5.5 square miles—spotlights part of what was once the largest earthen-architecture city in pre-Columbian America and provides evidence of the kingdom’s industrial, agricultural, and water management systems.
In 1986 (the same year UNESCO put it on its World Heritage List), Chan Chan was added to the in-danger list because of its fragility: Air and water can easily damage structures on the site. The organization reports that human activity, mainly in the form of illegal farming and infrastructure development, is also threatening the visual integrity of the property.
More than 329 species of birds have been spotted in Niokolo-Koba National Park.
Photo by klublu/Shutterstock

### Niokolo-Koba National Park
Senegal’s Niokolo-Koba National Park became a UNESCO World Heritage site in 1981 because of its diverse ecosystems, which include gallery-forests (forests located by rivers or wetlands in otherwise dry areas) and herbaceous savanna floodplains. The national park’s approximately 3,500 square miles are home to more than 70 species of mammals—including the Derby eland, the world’s largest antelope—and 1,500 plant species.
Niokolo-Koba National Park was added to the in-danger list because of several threats that include poaching, bush fires, and increased agricultural activity in the park.
_This article originally appeared online in 2022; it was updated in on November 21, 2023, to include current information._
Chloe’s love of travel grew out of her interest in learning languages. She’s spent time living in Italy, Spain, and as a digital nomad and she often reports on road trips and solo travel. Previously, she’s worked for publications including Afar, _Frommer’s_, and _Entrepreneur_.
</excerpt>

## Search 9
query: ""natural sites" "List of World Heritage in Danger""
<excerpt title="Natural World Heritage">
# Natural World Heritage
## Focus Areas
Forests
Marine Ecosystems
Priority Africa
Climate Change
Corporate sector and the World Heritage ‘no-go’ commitment
Emergency Situations
Communities
Biodiversity

# Natural World Heritage
## Nature’s most precious gifts
to humanity
Natural World Heritage sites contain some of the Earth's most valuable natural areas recognized as being of Outstanding Universal Value (OUV) to humanity for their global significance to nature conservation. To date, there are 266 natural sites inscribed on the UNESCO World Heritage List, including 218 sites recognized for their natural value and 39 mixed sites (recognized under both natural and cultural criteria). The World Heritage Convention sets the highest international standards for the integrity, protection and management of around 3,500,000 km2 (more than the size of India) across more than 100 countries.
Ranging in size from less than 1 km 2 in Vallée de Mai (Seychelles) to almost 700,000 km 2 in French Austral Lands and Seas (France), natural World Heritage sites harbour provide crucial habitats to many iconic species and harbor unique natural beauty, stunning landscapes, rare ecological processes, and exceptional biodiversity. These sites include many iconic places such as the Serengeti National Park (Tanzania) that hosts the largest terrestrial mammal migration in the world, the living museum of evolution of Galápagos Islands (Ecuador), Yellowstone National Park (United States of America) known for its wildlife and its many geothermal features and the world's largest coral reef system at Great Barrier Reef (Australia).

# Natural World Heritage
## Nature’s most precious gifts
Natural World Heritage sites are critical for the conservation of ecosystem integrity and biodiversity. While they make up less than 1% of the Earth’s surface, they harbor more than 1/5 of mapped global species richness. This includes over 75,000 species of plants, and over 30,000 species of mammals, birds, fishes, reptiles and amphibians. These sites also represent a safe haven for some of the most threatened species on Earth. They are estimated to protect over 20,000 globally threatened species, including some of the last individuals of many iconic species. Today, up to 1/3 of remaining elephants, tigers and pandas can be found in these sites, as well as at least 1 in 10 great apes, giraffes, lions and rhinos. For some species on the brink of extinction, World Heritage sites have become the last line of defense. They are home to all remaining Javan rhinos, vaquitas (the world's smallest cetacean) and pink iguanas, as well as more than half of all Sumatran rhinos, Sumatran orangutans and mountain gorillas.
Millions of people are directly dependent on the countless benefits and services these sites can provide, supporting livelihoods and wellbeing. Over 90% of listed natural sites create jobs and provide income from tourism and recreation. Two-thirds of natural sites are crucial sources of water, and about half help prevent hazards such as floods or landslides. They also have a central role in climate regulation and carbon sequestration as World Heritage forests absorb approximately 190 million tons of CO2 each year (equivalent to half the United Kingdom’s annual CO2 emissions from fossil fuels). Marine and coastal sites are also critical to mitigating climate impacts storing 1.3 billion tons of carbon (known as blue carbon) in seagrass meadows, tidal marshes and mangroves, representing 15% of global blue carbon assets.
</excerpt>

## Search 10
query: "natural sites in the UNESCO List of World Heritage in Danger 2026 "natural""
<excerpt title="Natural World Heritage">
# Natural World Heritage
## Focus Areas
Forests
Marine Ecosystems
Priority Africa
Climate Change
Corporate sector and the World Heritage ‘no-go’ commitment
Emergency Situations
Communities
Biodiversity

# Natural World Heritage
## Nature’s most precious gifts
to humanity
Natural World Heritage sites contain some of the Earth's most valuable natural areas recognized as being of Outstanding Universal Value (OUV) to humanity for their global significance to nature conservation. To date, there are 266 natural sites inscribed on the UNESCO World Heritage List, including 218 sites recognized for their natural value and 39 mixed sites (recognized under both natural and cultural criteria). The World Heritage Convention sets the highest international standards for the integrity, protection and management of around 3,500,000 km2 (more than the size of India) across more than 100 countries.
Ranging in size from less than 1 km 2 in Vallée de Mai (Seychelles) to almost 700,000 km 2 in French Austral Lands and Seas (France), natural World Heritage sites harbour provide crucial habitats to many iconic species and harbor unique natural beauty, stunning landscapes, rare ecological processes, and exceptional biodiversity. These sites include many iconic places such as the Serengeti National Park (Tanzania) that hosts the largest terrestrial mammal migration in the world, the living museum of evolution of Galápagos Islands (Ecuador), Yellowstone National Park (United States of America) known for its wildlife and its many geothermal features and the world's largest coral reef system at Great Barrier Reef (Australia).

# Natural World Heritage
## Nature’s most precious gifts
Natural World Heritage sites are critical for the conservation of ecosystem integrity and biodiversity. While they make up less than 1% of the Earth’s surface, they harbor more than 1/5 of mapped global species richness. This includes over 75,000 species of plants, and over 30,000 species of mammals, birds, fishes, reptiles and amphibians. These sites also represent a safe haven for some of the most threatened species on Earth. They are estimated to protect over 20,000 globally threatened species, including some of the last individuals of many iconic species. Today, up to 1/3 of remaining elephants, tigers and pandas can be found in these sites, as well as at least 1 in 10 great apes, giraffes, lions and rhinos. For some species on the brink of extinction, World Heritage sites have become the last line of defense. They are home to all remaining Javan rhinos, vaquitas (the world's smallest cetacean) and pink iguanas, as well as more than half of all Sumatran rhinos, Sumatran orangutans and mountain gorillas.
Millions of people are directly dependent on the countless benefits and services these sites can provide, supporting livelihoods and wellbeing. Over 90% of listed natural sites create jobs and provide income from tourism and recreation. Two-thirds of natural sites are crucial sources of water, and about half help prevent hazards such as floods or landslides. They also have a central role in climate regulation and carbon sequestration as World Heritage forests absorb approximately 190 million tons of CO2 each year (equivalent to half the United Kingdom’s annual CO2 emissions from fossil fuels). Marine and coastal sites are also critical to mitigating climate impacts storing 1.3 billion tons of carbon (known as blue carbon) in seagrass meadows, tidal marshes and mangroves, representing 15% of global blue carbon assets.
</excerpt>

Read the searches in order: how each query was formed, what came back, and how the next query used it. Find the failure in query choice or revision that cost the most, and write a new system prompt that fixes it. Replace or compress existing text where you can; avoid making the prompt much longer. Do not copy any fact, name, site or topic from these examples: the model will face unrelated questions. Keep the description of the `web_search` tool and the 10-search limit accurate.

Provide the new system prompt within ``` blocks.
