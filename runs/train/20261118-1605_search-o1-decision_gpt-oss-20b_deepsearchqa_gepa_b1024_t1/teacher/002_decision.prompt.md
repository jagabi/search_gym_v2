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
Find the names of the four members of the US women's 3X3 basketball team at the 2020 Olympics. Find out what their final college team was and who the head coach of their final college team was during the 2022/2023 season, as well as the name of the team player with the highest average points per game for that season and the team player with the highest average rebounds per game for that season. Provide a bulleted list with the name of the 3X3 team member, the name of their final college, the name of the coach in the 2022/2023 season, the name of the team player with the highest average points in the 2022/2023 season, and the name of the team player with the highest average rebounds in the 2022/2023 season in a comma separated list for each bullet point. Order the bullet list in alphabetical order by the player's first name. Do not list any other information.

## Expected answer
* Allisha Gray, University of South Carolina, Dawn Staley, Zia Cooke, Aliyah Boston
* Jacquelyn (Jackie) Young, University of Notre Dame, Niele Ivey, Sonia Citron, Olivia Miles
* Kelsey Plum, University of Washington, Tina Langley, Dalayah Daniels, Dalayah Daniels
* Stefanie Dolson, University of Connecticut, Geno Auriemma, Aaliyah Edwards, Dorka Juhasz

## Grade 0.00

## Search 1 — query: "US women's 3x3 basketball team 2020 Olympics roster"
### Rank 1 of 91 — 0.91 (passed on)
<excerpt title="3x3 Women's Olympics">
# USA Basketball 3x3 at the Olympics
3x3 basketball was featured as an Olympic sport for the first time at the 2020 Tokyo Games (held in 2021). The United States are the only team to medal in multiple Games and made history as the first Olympic 3x3 women’s gold medal winner with a team featuring WNBA players Stefanie Dolson, Allisha Gray, Kelsey Plum and Jackie Young.
[Opens in a new window ![Image 10: USA Basketball](blob:http://localhost/b9a31d3949b1882a09ed2f8508d538f3)](https://www.nike.com/)
[Opens in a new window ![Image 11: USA Basketball](blob:http://localhost/b9a31d3949b1882a09ed2f8508d538f3)](https://www.sofi.com/)
[Opens in a new window ![Image 12: USA Basketball](blob:http://localhost/b9a31d3949b1882a09ed2f8508d538f3)](https://tide.com/en-us)
[Opens in a new window ![Image 13: USA Basketball](blob:http://localhost/b9a31d3949b1882a09ed2f8508d538f3)](https://www.uclahealth.org/)
[Opens in a new window ![Image 14: USA Basketball](blob:http://localhost/b9a31d3949b1882a09ed2f8508d538f3)](https://shop.wayvia.com/?campaignid=l7LRp4bEoq_4e722e41-775b-4028-aadf-951565ab7b5d&productid=5vqu0xvwkb9uh0&displaylanguage=en_US)
</excerpt>
### Rank 2 of 91 — 0.91
<excerpt title="Basketball at the 2020 Summer Olympics – Women's 3x3 tournament">
## Competition schedule
| [Italy](https://en.wikipedia.org/wiki/Italy_women's_national_3x3_team "Italy women's national 3x3 team")[[12]](https://en.wikipedia.org/wiki/Basketball_at_the_2020_Summer_Olympics_%E2%80%93_Women's_3x3_tournament#cite_note-12) | Chiara Consolini | [Rae Lin D'Alie](https://en.wikipedia.org/wiki/Rae_Lin_D'Alie "Rae Lin D'Alie") | Marcella Filippi | Giulia Rulli |  
| [Japan](https://en.wikipedia.org/wiki/Japan_women's_national_3x3_team "Japan women's national 3x3 team")[[13]](https://en.wikipedia.org/wiki/Basketball_at_the_2020_Summer_Olympics_%E2%80%93_Women's_3x3_tournament#cite_note-13) | Stephanie Mawuli | Risa Nishioka | Mio Shinozaki | Mai Yamamoto |  
| [Mongolia](https://en.wikipedia.org/wiki/Mongolia_women's_national_3x3_team "Mongolia women's national 3x3 team")[[14]](https://en.wikipedia.org/wiki/Basketball_at_the_2020_Summer_Olympics_%E2%80%93_Women's_3x3_tournament#cite_note-14) | Enkhtaivany Chimeddolgor | Onolbaataryn Khulan | Bayasgalangiin Solongo | Mönkhsaikhany Tserenlkham |  

## Competition schedule
| [United States](https://en.wikipedia.org/wiki/United_States_women's_national_3x3_team "United States women's national 3x3 team")[[15]](https://en.wikipedia.org/wiki/Basketball_at_the_2020_Summer_Olympics_%E2%80%93_Women's_3x3_tournament#cite_note-15) | Stefanie Dolson | Allisha Gray | Kelsey Plum | Jackie Young[[16]](https://en.wikipedia.org/wiki/Basketball_at_the_2020_Summer_Olympics_%E2%80%93_Women's_3x3_tournament#cite_note-16) |
Katie Lou Samuelson originally qualified as the fourth team member of the United States, but she tested positive for COVID-19 and was replaced by Jackie Young.[[17]](https://en.wikipedia.org/wiki/Basketball_at_the_2020_Summer_Olympics_%E2%80%93_Women's_3x3_tournament#cite_note-17)
The following 12 referees were selected for the tournament.[[18]](https://en.wikipedia.org/wiki/Basketball_at_the_2020_Summer_Olympics_%E2%80%93_Women's_3x3_tournament#cite_note-18)
</excerpt>
### Rank 3 of 91 — 0.90
<excerpt title="Basketball at the 2020 Summer Olympics – Women's 3x3 tournament">
## Competition schedule
| [United States](https://en.wikipedia.org/wiki/United_States_women's_national_3x3_team "United States women's national 3x3 team")[[15]](https://en.wikipedia.org/wiki/Basketball_at_the_2020_Summer_Olympics_%E2%80%93_Women's_3x3_tournament#cite_note-15) | Stefanie Dolson | Allisha Gray | Kelsey Plum | Jackie Young[[16]](https://en.wikipedia.org/wiki/Basketball_at_the_2020_Summer_Olympics_%E2%80%93_Women's_3x3_tournament#cite_note-16) |
Katie Lou Samuelson originally qualified as the fourth team member of the United States, but she tested positive for COVID-19 and was replaced by Jackie Young.[[17]](https://en.wikipedia.org/wiki/Basketball_at_the_2020_Summer_Olympics_%E2%80%93_Women's_3x3_tournament#cite_note-17)
The following 12 referees were selected for the tournament.[[18]](https://en.wikipedia.org/wiki/Basketball_at_the_2020_Summer_Olympics_%E2%80%93_Women's_3x3_tournament#cite_note-18)

## Competition schedule
| Pos | Team | Pld | W | L | PF | PA | PD | Qualification |  
| --- | --- | --- | --- | --- | --- | --- | --- | --- |  
| 1 | [United States](https://en.wikipedia.org/wiki/United_States_women's_national_3x3_team "United States women's national 3x3 team") | 7 | 6 | 1 | 136 | 98 | +38 | [Semifinals](https://en.wikipedia.org/wiki/Basketball_at_the_2020_Summer_Olympics_%E2%80%93_Women's_3x3_tournament#Semifinals) |  
| 2 | [ROC](https://en.wikipedia.org/wiki/Russia_women's_national_3x3_team "Russia women's national 3x3 team") | 7 | 5[[a]](https://en.wikipedia.org/wiki/Basketball_at_the_2020_Summer_Olympics_%E2%80%93_Women's_3x3_tournament#cite_note-table_hth_ROC0.26952016971517-19) | 2 | 129 | 90 | +39 |  
| 3 | [China](https://en.wikipedia.org/wiki/China_women's_national_3x3_team "China women's national 3x3 team") | 7 | 5[[a]](https://en.wikipedia.org/wiki/Basketball_at_the_2020_Summer_Olympics_%E2%80%93_Women's_3x3_tournament#cite_note-table_hth_ROC0.26952016971517-19) | 2 | 127 | 97 | +30 | [Quarterfinals](https://en.wikipedia.org/wiki/Basketball_at_the_2020_Summer_Olympics_%E2%80%93_Women's_3x3_tournament#Quarterfinals) |
</excerpt>
### Rank 4 of 91 — 0.89
<excerpt title="Roster Named for USA Basketball Women's 3x3 Olympic Qualifying ...">
# Roster Named for USA Basketball Women’s 3&#215;3 Olympic Qualifying Team
## Roster Named for USA Basketball Women’s 3x3 Olympic Qualifying Team
Mon, Feb 17, 2020, 9:34 PM
/
USA Basketball
The four-member rosters today were announced for the USA Basketball Men’s and Women’s 3×3 Olympic Qualifying Tournament Teams that will compete in the 2020 FIBA 3×3 Olympic Qualifying Tournament March 18-22 in Bengaluru, India, where the top three finishing men’s and women’s teams will earn berths into the 2020 Tokyo Olympic Games.
Named to the USA women’s team were current WNBA players: Napheesa Collier (Minnesota Lynx/O’Fallon, Mo.), Stefanie Dolson (Chicago Sky/Port Jervis, N.Y.), Allisha Gray (Dallas Wings/Sandersville, Ga.) and Kelsey Plum (Las Vegas Aces/Poway, Calif.).
The rosters were selected by the USA Basketball 3×3 Selection Committees following Feb. 12-15 training camps in Chicago that featured 11 female and 16 male hopefuls.
“USA Basketball is grateful to all of the athletes who attended training camp and competed for a roster spot,” said Jay Demings, USA Basketball Youth & Sport Development director and member of the USA Basketball 3×3 Men’s and Women’s Selection Committees. “It was a very talented field for both the men and women, and the committees had a very difficult task in selecting these teams. In the end, we are confident in the abilities of the eight players and the strength of the teams overall. Now, it is on to the very important task of qualifying the USA for the 3×3 Olympic basketball competition in Tokyo.”
The USA women earned their spot in the FIBA 3×3 Olympic Qualifying Tournament by virtue of their status on the FIBA 3×3 world rankings as of this past November.
As per FIBA regulations, all teams taking part in the 2020 FIBA 3×3 Olympic Qualifying Tournament must include on their rosters at least two athletes who are ranked among the federation’s top 10 FIBA 3×3 athletes.
</excerpt>
### Rank 5 of 91 — 0.83
<excerpt title="2024 USA 3x3 Women's National Team - 3x3 Women's Olympics">
# 3x3 Women's Olympics
## Athletes
### Cierra Burdick
*   **Height**6‐2  
    *   **Weight**165  
    *   **Current Age**33  
    *   **Hometown**Charlotte, NC  
    *   **High School**David W. Butler HS  
    *   **College**University of Tennessee
*
Full bio[![Image 68: USA Basketball](blob:http://localhost/b9a31d3949b1882a09ed2f8508d538f3) #5](https://www.usab.com/players/dearica-hamby)

# 3x3 Women's Olympics
## Athletes
### Dearica Hamby
*   **Position(s)**Forward  
    *   **Height**6‐3  
    *   **Current Age**33  
    *   **Hometown**Marietta, GA  
    *   **High School**Norcross HS  
    *   **College**Wake Forest University
*
Full bio[![Image 69: USA Basketball](blob:http://localhost/b9a31d3949b1882a09ed2f8508d538f3) #10](https://www.usab.com/players/rhyne-howard)

# 3x3 Women's Olympics
## Athletes
### Rhyne Howard
*   **Height**6‐2  
    *   **Weight**180  
    *   **Current Age**26  
    *   **Current Team**Atlanta Dream  
    *   **Hometown**Cleveland, TN  
    *   **High School**Bradley Central HS  
    *   **College**University of Kentucky
*
Full bio[![Image 70: USA Basketball](blob:http://localhost/b9a31d3949b1882a09ed2f8508d538f3) #9](https://www.usab.com/players/hailey-van-lith)

# 3x3 Women's Olympics
## Athletes
### Hailey Van Lith
*   **Height**5‐9  
    *   **Weight**155  
    *   **Current Age**25  
    *   **Hometown**Wenatchee, WA  
    *   **High School**Cashmere HS  
    *   **College**TCU
*
Cierra Burdick #7   
    *   Height:**6‐2**  
    *   Weight:**165**  
    *   Current Age:**33**  
    *   Hometown:**Charlotte, NC**  
    *   High School:**David W. Butler HS**  
    *   College:**University of Tennessee**
Full Bio  
*     
Dearica Hamby #5   
    *   Position(s):**Forward**  
    *   Height:**6‐3**  
    *   Current Age:**33**  
    *   Hometown:**Marietta, GA**  
    *   High School:**Norcross HS**  
    *   College:**Wake Forest University**
Full Bio  
*     
Rhyne Howard #10   
    *   Height:**6‐2**  
    *   Weight:**180**  
    *   Current Age:**26**  
    *   Current Team:**Atlanta Dream**  
    *   Hometown:**Cleveland, TN**  
    *   High School:**Bradley Central HS**  
    *   College:**University of Kentucky**
Full Bio  
*     
Hailey Van Lith #9   
    *   Height:**5‐9**  
    *   Weight:**155**  
    *   Current Age:**25**  
    *   Hometown:**Wenatchee, WA**  
    *   High School:**Cashmere HS**  
    *   College:**TCU**
Full Bio
</excerpt>

## Search 2 — query: "Allisha Gray college basketball Tennessee State"
### Rank 1 of 119 — 0.47 (passed on)
<excerpt title="Allisha Gray">
**Medals** Women's 3x3 basketball Representing [United States](https://en.wikipedia.org/wiki/United_States_women's_national_3x3_team "United States women's national 3x3 team") Olympic Games 2020 Tokyo[Team](https://en.wikipedia.org/wiki/Basketball_at_the_2020_Summer_Olympics_%E2%80%93_Women's_3x3_tournament "Basketball at the 2020 Summer Olympics – Women's 3x3 tournament") FIBA 3x3 AmeriCup [2025 León](https://en.wikipedia.org/wiki/2025_FIBA_3x3_AmeriCup_%E2%80%93_Women's_tournament "2025 FIBA 3x3 AmeriCup – Women's tournament")
**Allisha Gray** ( _AL-lee-shə_;[[1]](https://en.wikipedia.org/wiki/Allisha_Gray#cite_note-1) born January 12, 1995) is an American professional basketball player for the Atlanta Dream of the [Women's National Basketball Association](https://en.wikipedia.org/wiki/Women's_National_Basketball_Association "Women's National Basketball Association") (WNBA) and for Vinyl of Unrivaled. She won a gold medal in [women's 3x3 basketball](https://en.wikipedia.org/wiki/Basketball_at_the_2020_Summer_Olympics_%E2%80%93_Women's_3x3_tournament "Basketball at the 2020 Summer Olympics – Women's 3x3 tournament") at the 2020 Summer Olympics.[[2]](https://en.wikipedia.org/wiki/Allisha_Gray#cite_note-2)[[3]](https://en.wikipedia.org/wiki/Allisha_Gray#cite_note-3)

She played college basketball for the [North Carolina Tar Heels](https://en.wikipedia.org/wiki/North_Carolina_Tar_Heels_women's_basketball "North Carolina Tar Heels women's basketball") and [South Carolina Gamecocks](https://en.wikipedia.org/wiki/South_Carolina_Gamecocks_women's_basketball "South Carolina Gamecocks women's basketball"). After she was selected 4th overall by the Dallas Wings in the 2017 WNBA draft, Gray won the WNBA Rookie of the Year award.
She was a member of the U18 USA Basketball National Team as well as the 3-on-3 National Team. Named 3A state player of the year three times. She led Washington County to a three-year record of 88–4 that included a perfect 32–0 record and a 3A state championship in 2010–11. As a junior, Gray averaged 32.0 points and 8.5 rebounds en route to a state runner-up finish. She then missed most of her senior season with a knee injury
Heavily recruited by power programs, she was ranked the 7th overall player as part of a high-profile 2013 recruiting class. After receiving offers from Maryland, Kentucky, South Carolina, etc., she eventually chose to attend North Carolina to play for Coach Sylvia Hatchell. After two years in Chapel Hill, Gray shockingly announced that she would be transferring. It was then reported that her reason for transferring was due to UNC's athletic-academic scandal. In May 2015, it was announced that Gray had transferred to South Carolina to play for Dawn Staley. Gray won a [National Championship](https://en.wikipedia.org/wiki/NCAA_Women's_Division_I_Basketball_Championship "NCAA Women's Division I Basketball Championship") with the 2017 Gamecocks in her final college season.
</excerpt>
### Rank 2 of 119 — 0.47
<excerpt title="Allisha Gray">
# Allisha Gray - USA Basketball
### Coach Academy
*   Frequently Asked Questions

# Allisha Gray - USA Basketball
### 3X Play
*   Rules & Standards

# Allisha Gray - USA Basketball
### On-Demand Courses
*   Frequently Asked Questions

# Allisha Gray - USA Basketball
### E-Learning
*   Frequently Asked Questions

# Allisha Gray - USA Basketball
### Coaching Resources
*   Skills and Drills  
        *   Youth Guidelines  
        *   Official USA Basketball Guidebook & E-Book

# Allisha Gray - USA Basketball
### Sign Up for Notifications
*   Safe Sport    ### Safe Sport

        ### Report an Incident

    
        ### MAAPP & Athlete and Participant Safety & Protection

    
        ### Resources

    
        ### Disciplinary Records

         
*   News  
*   Opens in a new window Foundation  
*   Opens in a new window Shop
Opens in a new window Open facebookOpens in a new window Open twitterOpens in a new window Open instagramOpens in a new window Open youtube
Open Search
Search Search Close Search
Calendar Events
Open Menu

# Allisha Gray
Position(s)**Guard**
Height**6‐0**
Age**31**
Hometown**Sandersville, GA**
High School**Washington County HS**
College**University of South Carolina**
*   Bio   
*   5-ON-5 STATS   
*   3X3 STATS
_**As of March 27, 2026**_

# Allisha Gray
## USA Basketball Notes
*   **Gold Medals:**2025 FIBA 3x3 AmeriCup, 2020 Olympic Games (3x3).  
*   **Bronze Medals:**2026 FIBA 3x3 Champions Cup  
*   **Teams:**2026 USA 3x3 Champions Cup Team, 2025 USA 3x3 AmeriCup Team,2020 USA Women’s Olympic Team (3x3), 2021 USA Women’s Olympic Qualifying Team (3x3), 2019 Women’s National Team (exhibitions)  
*   **Tournament Titles:** 2021 FIBA 3x3 Olympic Qualifying Tournament.  
*   **Honors:** 2026 FIBA 3x3 Champions Cup All-Tournament Team, 2025 FIBA 3x3 AmeriCup MVP, 2021 USA Basketball 3x3 Athlete of the Year, 2021 Big Twelve International MVP (3x3).  
*   **2026:**  
    *   Named to the 2026 USA 3x3 Champions Cup Team (3/9/26) and won bronze at the 2026 FIBA 3x3 Champions Cup in Bangkok. In five games (4-1), averaged team-best 6.8 points and 3.6 rebounds while being named to All-Tournament Team.

*   **2025:**  
    *   Named to the 2025 USA 3x3 Women's AmeriCup Team (11/19/25) and won gold at the 2025 FIBA 3x3 AmeriCup in Leon, Mexico. In five games (5-0), she averaged 5.0 points, 2.8 key assists and 2.2 rebounds en route to MVP honors.

*   **2024:**  
    *   Attending the 2024 USA 3x3 Women's National Team training camp in April in Springfield, MA.  
    *   Participated in the 2024 USA Women’s National Team February training camp in New York.
</excerpt>
### Rank 3 of 119 — 0.44
<excerpt title="Allisha Gray">
She played college basketball for the [North Carolina Tar Heels](https://en.wikipedia.org/wiki/North_Carolina_Tar_Heels_women's_basketball "North Carolina Tar Heels women's basketball") and [South Carolina Gamecocks](https://en.wikipedia.org/wiki/South_Carolina_Gamecocks_women's_basketball "South Carolina Gamecocks women's basketball"). After she was selected 4th overall by the Dallas Wings in the 2017 WNBA draft, Gray won the WNBA Rookie of the Year award.
She was a member of the U18 USA Basketball National Team as well as the 3-on-3 National Team. Named 3A state player of the year three times. She led Washington County to a three-year record of 88–4 that included a perfect 32–0 record and a 3A state championship in 2010–11. As a junior, Gray averaged 32.0 points and 8.5 rebounds en route to a state runner-up finish. She then missed most of her senior season with a knee injury
Heavily recruited by power programs, she was ranked the 7th overall player as part of a high-profile 2013 recruiting class. After receiving offers from Maryland, Kentucky, South Carolina, etc., she eventually chose to attend North Carolina to play for Coach Sylvia Hatchell. After two years in Chapel Hill, Gray shockingly announced that she would be transferring. It was then reported that her reason for transferring was due to UNC's athletic-academic scandal. In May 2015, it was announced that Gray had transferred to South Carolina to play for Dawn Staley. Gray won a [National Championship](https://en.wikipedia.org/wiki/NCAA_Women's_Division_I_Basketball_Championship "NCAA Women's Division I Basketball Championship") with the 2017 Gamecocks in her final college season.

## Professional career
[edit]
After helping lead [South Carolina](https://en.wikipedia.org/wiki/South_Carolina_Gamecocks_women's_basketball "South Carolina Gamecocks women's basketball") to the NCAA Championship, Gray opted to enter the 2017 WNBA draft. By entering, she would forgo her final season of college eligibility.[[4]](https://en.wikipedia.org/wiki/Allisha_Gray#cite_note-4) She was drafted 4th overall by the Dallas Wings placing her in the city where she won a national title two weeks prior, and eventually pairing her with South Carolina teammate, Kaela Davis, who was selected 10th. In her rookie season, Gray immediately entered the Wings' starting lineup at the shooting guard. She started in all 34 games and averaged 13.1 ppg. On August 12, 2017, Gray scored a career-high 21 points in a 96–88 loss to the Connecticut Sun.[[5]](https://en.wikipedia.org/wiki/Allisha_Gray#cite_note-5) The Wings finished as the number 7 seed in the league with a 16–18 record. The Wings were defeated in the first round elimination game 86–76 by the Washington Mystics. On September 19, 2017, it was announced by the WNBA that Gray won the 2017 Rookie of the Year Award.[[6]](https://en.wikipedia.org/wiki/Allisha_Gray#cite_note-6)
Gray with the Dallas Wings in 2021
In her second season, Gray continued her starting role with the Wings. With the arrival of all-star center Liz Cambage, Gray would have a reduced offensive load on the team. Gray averaged 9.2 ppg in her second season, helping the Wings to the number 8 seed with a 15–19 record. In the first round elimination game, the Wings lost 101–83 to the Phoenix Mercury.
</excerpt>
### Rank 4 of 119 — 0.41
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
### Rank 5 of 119 — 0.38
<excerpt title="Allisha Gray">
# Allisha Gray
## Professional Notes
*   Drafted No. 4 by Dallas in the 2017 WNBA Draft.  
*   Was the 2017 WNBA Rookie of the Year.  
*   To visit Gray’s WNBA bio, click here.

# Allisha Gray
## College Notes
*   Played two years (2013-14 through 2014-15) for the University of North Carolina before transferring to the University of South Carolina.  
*   After sitting out the 2015-16 season, averaged 13.2 points, 5.0 rebounds and 2.5 assists in helping lead USC to the 2017 NCAA Championship, the SEC regular season and tournament titles, and a 33-4 record.  
*   NCAA Final Four All-Tournament Team and All-Region Team (2017), WBCA All-America honorable mention (2015); All-Atlantic Coast Conference first team (2015), ACC All-Freshman Team (2014).

# Allisha Gray
## Personal Notes
*   Hails from Sandersville, Georgia, where she was the 2012 Gatorade State Player of the Year at Washington County H.S.  
*   Three-time Georgia Athletic Coaches Association Class 3A Player of the Year.  
*   Daughter of Annie and Dr. Allen Gray; has an older brother Marlo East, a younger brother A.J. Gray and a younger sister Ashley Gray.
**TEAMS****G/S****AVG MIN****FGM-FGA****PCT****3PM-3PA****PCT****FTM-FTA****PCT****REB/AVG****PTS/AVG****AST****TO****BLK****STL**  
2019 WNT 4/0 8.3 7-13.538 4-5.800 4-5.800 4/ 1.0 22/ 5.5 1 1 0 3  
2018 WNT 2/1 7.0 0-5.000 0-1.000 0-0.—-2/ 1.0 0/ 0.0 0 3 1 2  
**Totals****6/1****7-18****.389****4-6****.667****4-5****.800****6/ 1.0****22/3.7****1****4****1****5**

# Allisha Gray
## Personal Notes
**3x3 TEAMS****G****1PM-A****PCT****2PM-3A****PCT****FTM-A****PCT****REB/AVG****PTS/AVG****KAS****DRV****DNK****BLK****BZR****TO**  
2020 OLY 3x3 9 26-45.578 5-16.313 12-16.750 43/ 4.8 50/ 5.6 11 10 0 9 0 3  
2021 3x3 OQT 6 18-27.667 8-21.381 5-8.625 30/ 5.0 39/ 6.5 4 6 0 5 0 7  
Big 12 Exh 7 _*Statistics unavailable_  
**Totals****22**
</excerpt>

## Search 3 — query: "UConn women's basketball 2022-23 leading scorer points per game"
### Rank 1 of 352 — 0.68 (passed on)
<excerpt title="2022–23 UConn Huskies women's basketball team">
The Huskies finished an injury-plagued previous season with a record of 30–6, losing the [championship game](https://en.wikipedia.org/wiki/2022_NCAA_Division_I_women's_basketball_championship_game "2022 NCAA Division I women's basketball championship game") of the [2022 NCAA women's basketball tournament](https://en.wikipedia.org/wiki/2022_NCAA_Division_I_women's_basketball_tournament "2022 NCAA Division I women's basketball tournament") to South Carolina. Three graduates from that squad were selected in the 2022 WNBA draft, but with six returning starters including the backcourt of Paige Bueckers, Azzi Fudd, and Nika Mühl, with forwards Dorka Juhász, Aaliyah Edwards, and Caroline Ducharme, UConn was expected to win the much improved Big East again. Bueckers tore an ACL in a pickup game before fall workouts,[[1]](https://en.wikipedia.org/wiki/2022%E2%80%9323_UConn_Huskies_women's_basketball_team#cite_note-2) and five-star recruit Ice Brady suffered a tendon dislocation during an early practice; both players underwent season ending surgeries and sat on the bench all season.[[2]](https://en.wikipedia.org/wiki/2022%E2%80%9323_UConn_Huskies_women's_basketball_team#cite_note-3)

Starting the season already down two players, UConn played surprisingly well against early opponents, with strong wins against #3 Texas, #10 NC State, and #9 Iowa in the first weeks. In the Texas game, Juhász injured a thumb and was sidelined for several weeks. Aubrey Griffin, who had redshirted the previous season because of injury, and Lou Lopez Sénéchal, a graduate transfer shooting guard from Fairfield University, got some starts and immediately impacted the team with their durability and shooting proficiency. Fudd began the season as a leading scorer, with Mühl leading the country in assists per game, and Edwards seemingly unstoppable in the paint. Fudd was injured in the loss to #7 Notre Dame, and by the end of December the Huskies only had seven players healthy, even after Juhász's return. On January 8, UConn's contest against DePaul was postponed because the Huskies only had six players able to play.[[3]](https://en.wikipedia.org/wiki/2022%E2%80%9323_UConn_Huskies_women's_basketball_team#cite_note-4)
</excerpt>
### Rank 2 of 352 — 0.68
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
### Rank 3 of 352 — 0.64
<excerpt title="2022–23 UConn Huskies women's basketball team">
#### Recruiting class of 2024
John's College High School") | Arlington, VA | | F | 42 | Amari DeBerry | 6 ft 5 in (1.96 m) | So | Williamsville South | Williamsville, NY | | F | 44 | Aubrey Griffin | 6 ft 1 in (1.85 m) | RS Jr | Ossining | Ossining, NY | | Head coach * Geno Auriemma (West Chester) Assistant coach(es) * Chris Dailey (Rutgers) * Jamelle Elliott (Connecticut) * Morgan Valley (Connecticut) * * * Legend * **(C)** Team captain * **(S)** Suspended * **(I)** Ineligible * **(W)**Walk-on *
Injured *  Current redshirt * * * Roster Last update: March 11, 2023 |
| 2022–23 Pre-season video: The Standard |  
| --- |  
| UCONN Women's Basketball "The Standard" |

#### Recruiting class of 2024
The Huskies began the season by hosting the Kutztown Golden Bears in an exhibition contest, the first meeting between the two schools. It was not the first time the Golden Bears had visited Storrs, however. On their return from a 2017 exhibition game against UMass, the Kutztown women were invited to tour the UConn campus and attend practice. Katie Lou Samuelson later said the Huskies wanted to show Kutztown "...what it means to be at this university and what we've been working for."[[13]](https://en.wikipedia.org/wiki/2022%E2%80%9323_UConn_Huskies_women's_basketball_team#cite_note-14) In the November 6, 2022 exhibition at the XL Center, the Golden Bears briefly led 7–6 at the start, but the Huskies quickly took over, taking a 30 point lead into halftime. The final tally was 115–42.[[14]](https://en.wikipedia.org/wiki/2022%E2%80%9323_UConn_Huskies_women's_basketball_team#cite_note-15)[[15]](https://en.wikipedia.org/wiki/2022%E2%80%9323_UConn_Huskies_women's_basketball_team#cite_note-16)

#### Recruiting class of 2024
UConn opened the regular season with a 98–39 win against the Huskies of Northeastern. Azzi Fudd led all scorers with 26 points, and Lou Lopez Sénéchal scored 17. Forwards Aaliyah Edwards and Dorka Juhász each recorded double doubles, Edwards with 12 rebounds and 14 points, and Juhász with 11 rebounds and 14 points. Aubrey Griffin, who had redshirted the previous season due to injury, came off the bench to hit six of seven field goal attempts including her only three-point attempt, scoring 13 points.[[16]](https://en.wikipedia.org/wiki/2022%E2%80%9323_UConn_Huskies_women's_basketball_team#cite_note-17)[[17]](https://en.wikipedia.org/wiki/2022%E2%80%9323_UConn_Huskies_women's_basketball_team#cite_note-18)
An early season home contest against a top ten opponent is always highly anticipated, but the second game against number three Texas was a rematch for Husky graduate transfer Lou Lopez Sénéchal. After a loss in NCAA tournament play against Texas ended her four-year career at Fairfield University, Lopez Sénéchal found herself with an extra year of eligibility (due to COVID) and through the transfer portal arrived in Storrs. She prepared herself to play Texas, saying "... losing the last game of your season and then playing them the second game of the season is something I'm looking forward to."[[18]](https://en.wikipedia.org/wiki/2022%E2%80%9323_UConn_Huskies_women's_basketball_team#cite_note-19)
</excerpt>
### Rank 4 of 352 — 0.64
<excerpt title="UConn Huskies women's basketball statistical leaders">
| 3 | Sue Bird | 231 | [2001–02](https://en.wikipedia.org/wiki/2001%E2%80%9302_Connecticut_Huskies_women's_basketball_team "2001–02 Connecticut Huskies women's basketball team") |  
| 4 | Crystal Dangerfield | 225 | [2018–19](https://en.wikipedia.org/wiki/2018%E2%80%9319_UConn_Huskies_women's_basketball_team "2018–19 UConn Huskies women's basketball team") |  
| 5 | Jennifer Rizzotti | 222 | [1995–96](https://en.wikipedia.org/wiki/1995%E2%80%9396_Connecticut_Huskies_women's_basketball_team "1995–96 Connecticut Huskies women's basketball team") |  
| 6 | Diana Taurasi | 208 | [2001–02](https://en.wikipedia.org/wiki/2001%E2%80%9302_Connecticut_Huskies_women's_basketball_team "2001–02 Connecticut Huskies women's basketball team") |  
| 7 | Moriah Jefferson | 204 | [2015–16](https://en.wikipedia.org/wiki/2015%E2%80%9316_UConn_Huskies_women's_basketball_team "2015–16 UConn Huskies women's basketball team") |  
| 8 | Maya Moore | 199 | [2008–09](https://en.wikipedia.org/wiki/2008%E2%80%9309_Connecticut_Huskies_women's_basketball_team "2008–09 Connecticut Huskies women's basketball team") |  

| 9 | Moriah Jefferson | 195 | [2013–14](https://en.wikipedia.org/wiki/2013%E2%80%9314_UConn_Huskies_women's_basketball_team "2013–14 UConn Huskies women's basketball team") |  
| 10 | Moriah Jefferson | 191 | [2014–15](https://en.wikipedia.org/wiki/2014%E2%80%9315_UConn_Huskies_women's_basketball_team "2014–15 UConn Huskies women's basketball team") |  
|  | Gabby Williams | 191 | [2017–18](https://en.wikipedia.org/wiki/2017%E2%80%9318_UConn_Huskies_women's_basketball_team "2017–18 UConn Huskies women's basketball team") |Single game| Rk | Player | Assists | Season | Opponent |  
| --- | --- | --- | --- | --- |  
| 1 | Nika Mühl | 15 | [2022–23](https://en.wikipedia.org/wiki/2022%E2%80%9323_UConn_Huskies_women's_basketball_team "2022–23 UConn Huskies women's basketball team") | NC State |  
| 2 | Paige Bueckers | 14 | [2020–21](https://en.wikipedia.org/wiki/2020%E2%80%9321_UConn_Huskies_women's_basketball_team "2020–21 UConn Huskies women's basketball team") | Butler |  
|  | Nika Mühl | 14 | [2022–23](https://en.wikipedia.org/wiki/2022%E2%80%9323_UConn_Huskies_women's_basketball_team "2022–23 UConn Huskies women's basketball team") | Tennessee |
</excerpt>
### Rank 5 of 352 — 0.63
<excerpt title="UConn Huskies women's basketball statistical leaders">
| 10 | Pam Webber | 546 | [1991–92](https://en.wikipedia.org/wiki/1991%E2%80%9392_Connecticut_Huskies_women's_basketball_team?action=edit&redlink=1 "1991–92 Connecticut Huskies women's basketball team (page does not exist)")[1992–93](https://en.wikipedia.org/wiki/1992%E2%80%9393_Connecticut_Huskies_women's_basketball_team?action=edit&redlink=1 "1992–93 Connecticut Huskies women's basketball team (page does not exist)")[1993–94](https://en.wikipedia.org/wiki/1993%E2%80%9394_Connecticut_Huskies_women's_basketball_team?action=edit&redlink=1 "1993–94 Connecticut Huskies women's basketball team (page does not exist)")[1994–95](https://en.wikipedia.org/wiki/1994%E2%80%9395_Connecticut_Huskies_women's_basketball_team "1994–95 Connecticut Huskies women's basketball team") |Season| Rk | Player | Assists | Season |  
| --- | --- | --- | --- |  
| 1 | Nika Mühl | 284 | [2022–23](https://en.wikipedia.org/wiki/2022%E2%80%9323_UConn_Huskies_women's_basketball_team "2022–23 UConn Huskies women's basketball team") |  
| 2 | Nika Mühl | 253 | [2023–24](https://en.wikipedia.org/wiki/2023%E2%80%9324_UConn_Huskies_women's_basketball_team "2023–24 UConn Huskies women's basketball team") |  

| 3 | Sue Bird | 231 | [2001–02](https://en.wikipedia.org/wiki/2001%E2%80%9302_Connecticut_Huskies_women's_basketball_team "2001–02 Connecticut Huskies women's basketball team") |  
| 4 | Crystal Dangerfield | 225 | [2018–19](https://en.wikipedia.org/wiki/2018%E2%80%9319_UConn_Huskies_women's_basketball_team "2018–19 UConn Huskies women's basketball team") |  
| 5 | Jennifer Rizzotti | 222 | [1995–96](https://en.wikipedia.org/wiki/1995%E2%80%9396_Connecticut_Huskies_women's_basketball_team "1995–96 Connecticut Huskies women's basketball team") |  
| 6 | Diana Taurasi | 208 | [2001–02](https://en.wikipedia.org/wiki/2001%E2%80%9302_Connecticut_Huskies_women's_basketball_team "2001–02 Connecticut Huskies women's basketball team") |  
| 7 | Moriah Jefferson | 204 | [2015–16](https://en.wikipedia.org/wiki/2015%E2%80%9316_UConn_Huskies_women's_basketball_team "2015–16 UConn Huskies women's basketball team") |  
| 8 | Maya Moore | 199 | [2008–09](https://en.wikipedia.org/wiki/2008%E2%80%9309_Connecticut_Huskies_women's_basketball_team "2008–09 Connecticut Huskies women's basketball team") |
</excerpt>

## Search 4 — query: "North Carolina Tar Heels women's basketball 2022-23 head coach"
### Rank 1 of 89 — 0.82 (passed on)
<excerpt title="2022–23 North Carolina Tar Heels women's basketball team">
| [Virginia](https://en.wikipedia.org/wiki/2022%E2%80%9323_Virginia_Cavaliers_women's_basketball_team "2022–23 Virginia Cavaliers women's basketball team") | 4 | – | 14 |  | .222 |  |  | 15 | – | 15 |  | .500 |  
| [Georgia Tech](https://en.wikipedia.org/wiki/2022%E2%80%9323_Georgia_Tech_Yellow_Jackets_women's_basketball_team "2022–23 Georgia Tech Yellow Jackets women's basketball team") | 4 | – | 14 |  | .222 |  |  | 13 | – | 17 |  | .433 |  
| [Pittsburgh](https://en.wikipedia.org/wiki/2022%E2%80%9323_Pittsburgh_Panthers_women's_basketball_team "2022–23 Pittsburgh Panthers women's basketball team") | 3 | – | 15 |  | .167 |  |  | 10 | – | 20 |  | .333 |  
|  |  
| † [2023 ACC tournament](https://en.wikipedia.org/wiki/2023_ACC_women's_basketball_tournament "2023 ACC women's basketball tournament") winner As of March 27, 2023 Rankings from [AP poll](https://en.wikipedia.org/wiki/2022%E2%80%9323_NCAA_Division_I_women's_basketball_rankings "2022–23 NCAA Division I women's basketball rankings") |

The **2022–23 North Carolina Tar Heels women's basketball team** represented the University of North Carolina at Chapel Hill in the [2022–23 NCAA Division I women's basketball season](https://en.wikipedia.org/wiki/2022%E2%80%9323_NCAA_Division_I_women's_basketball_season "2022–23 NCAA Division I women's basketball season"). The Tar Heels were led by head coach Courtney Banghart, who was in her fourth season. She was assisted by Joanne Aluka-White, Adrian Walters, and Itoro Coleman. The Tar Heels played their home games at Carmichael Arena as members of the Atlantic Coast Conference.
</excerpt>
### Rank 2 of 89 — 0.80
<excerpt title="2022-23 Women's Basketball Coaching Staff">
# University of North Carolina Athletics


# 2022-23 Women's Basketball Coaching Staff
Skip Ad
2022-23
*   2026-27  
*   2025-26  
*   2024-25  
*   2023-24  
*   2022-23  
*   2021-22  
*   2020-21  
*   2019-20  
*   2018-19  
*   2017-18  
*   2016-17  
*   2015-16  
*   2014-15  
*   2013-14  
*   2012-13  
*   2011-12
vs
**Gardner-Webb**  
Nov 24 (Tue)
7 PM
Buy From$10+

# 2022-23 Women's Basketball Coaching Staff
## Coaching Staff
| Name | Title | Phone | Email Address |  
| --- | --- | --- | --- |  
| Courtney Banghart | Head Coach |  |  |  
| Joanne Aluka-White | Assistant Coach |  | [aluka@email.unc.edu](mailto:aluka@email.unc.edu) |  
| Itoro Coleman | Assistant Coach/Recruiting Coordinator |  |  |  
| Adrian Walters | Assistant Coach | 919-962-5411 | [adub2@email.unc.edu](mailto:adub2@email.unc.edu) |  
| Sam Miller | Director of Scouting and Video Operations/Assistant Coach | 919-260-1690 | [smiller1@unc.edu](mailto:smiller1@unc.edu) |  
| Sean Sullivan | Director of Player Personnel, Development and Recruiting Operations/Assistant Coach |  | [ssullivan@unc.edu](mailto:ssullivan@unc.edu) |  
| Jessika Carrington | Assistant to the AD/Director of Basketball Operations | 919-260-2581 | [Jcarunc@unc.edu](mailto:Jcarunc@unc.edu) |  
| Liz Roberts | Director of Recruiting Management and Student-Athlete Engagement |  | [lizrob@live.unc.edu](mailto:lizrob@live.unc.edu) |  
| Caleb Krueger | Head Strength and Conditioning Coach |  | [calebmhk@email.unc.edu](mailto:calebmhk@email.unc.edu) |  
| Andrew Graber | Assistant Strength & Conditioning Coach |  |  |  
| Dr. Josh Berkowitz | Team Physician | 919-966-3655 | [josh_berkowitz@med.unc.edu](mailto:josh_berkowitz@med.unc.edu) |  
| Jodi Schneider | Head Athletic Trainer | 919-962-2067 | [jodis@email.unc.edu](mailto:jodis@email.unc.edu) |  
| Emily Adney | Academic Counselor | 919-962-9536 | [emily6@email.unc.edu](mailto:emily6@email.unc.edu) |
</excerpt>
### Rank 3 of 89 — 0.80
<excerpt title="2022–23 North Carolina Tar Heels women's basketball team">
From Wikipedia, the free encyclopedia
| 2022–23[North Carolina Tar Heels women's basketball](https://en.wikipedia.org/wiki/North_Carolina_Tar_Heels_women's_basketball "North Carolina Tar Heels women's basketball") |  
| --- |  
|  |  
| Phil Knight Invitational champions |  
| [NCAA tournament](https://en.wikipedia.org/wiki/2023_NCAA_Division_I_women's_basketball_tournament "2023 NCAA Division I women's basketball tournament"), Second Round |  
| Conference | Atlantic Coast Conference |  
| Ranking |  
| Coaches | No.21 |  
| AP | No.20 |  
| Record | 22–11 (11–7 ACC) |  
| Head coach | * Courtney Banghart (4th season) |  
| Assistant coaches | * Joanne Aluka-White * Itoro Coleman * Adrian Walters |  
| Home arena | Carmichael Arena |  
| Seasons ←[2021–22](https://en.wikipedia.org/wiki/2021%E2%80%9322_North_Carolina_Tar_Heels_women's_basketball_team "2021–22 North Carolina Tar Heels women's basketball team") [2023–24](https://en.wikipedia.org/wiki/2023%E2%80%9324_North_Carolina_Tar_Heels_women's_basketball_team "2023–24 North Carolina Tar Heels women's basketball team")→ |

[2022–23 ACC women's basketball standings](https://en.wikipedia.org/wiki/2022%E2%80%9323_Atlantic_Coast_Conference_women's_basketball_season "2022–23 Atlantic Coast Conference women's basketball season")| * [v](https://en.wikipedia.org/wiki/Template:2022%E2%80%9323_ACC_women's_basketball_standings "Template:2022–23 ACC women's basketball standings") * [t](https://en.wikipedia.org/wiki/Template_talk:2022%E2%80%9323_ACC_women's_basketball_standings "Template talk:2022–23 ACC women's basketball standings") * [e](https://en.wikipedia.org/wiki/Special:EditPage/Template:2022%E2%80%9323_ACC_women's_basketball_standings "Special:EditPage/Template:2022–23 ACC women's basketball standings") | Conf. |  |  | Overall |  
| --- | --- | --- | --- | --- |  
| Team | W |  | L |  | PCT |  |  | W |  | L |  | PCT |  
| No. 10т [Notre Dame](https://en.wikipedia.org/wiki/2022%E2%80%9323_Notre_Dame_Fighting_Irish_women's_basketball_team "2022–23 Notre Dame Fighting Irish women's basketball team") | 15 | – | 3 |  | .833 |  |  | 27 | – | 6 |  | .818 |  
| No. 13 [Duke](https://en.wikipedia.org/wiki/2022%E2%80%9323_Duke_Blue_Devils_women's_basketball_team "2022–23 Duke Blue Devils women's basketball team") | 14 | – | 4 |  | .778 |  |  | 26 | – | 7 |  | .788 |
</excerpt>
### Rank 4 of 89 — 0.79
<excerpt title="2022–23 North Carolina Tar Heels women's basketball team">
The **2022–23 North Carolina Tar Heels women's basketball team** represented the University of North Carolina at Chapel Hill in the [2022–23 NCAA Division I women's basketball season](https://en.wikipedia.org/wiki/2022%E2%80%9323_NCAA_Division_I_women's_basketball_season "2022–23 NCAA Division I women's basketball season"). The Tar Heels were led by head coach Courtney Banghart, who was in her fourth season. She was assisted by Joanne Aluka-White, Adrian Walters, and Itoro Coleman. The Tar Heels played their home games at Carmichael Arena as members of the Atlantic Coast Conference.

The Tar Heels finished the season 22–11 overall record and 11–7 in [ACC play](https://en.wikipedia.org/wiki/2022%E2%80%9323_Atlantic_Coast_Conference_women's_basketball_season "2022–23 Atlantic Coast Conference women's basketball season") to finish in a tie for sixth place. As the seventh seed in the [ACC tournament](https://en.wikipedia.org/wiki/2023_ACC_women's_basketball_tournament "2023 ACC women's basketball tournament"), they defeated [Clemson](https://en.wikipedia.org/wiki/2022%E2%80%9323_Clemson_Tigers_women's_basketball_team "2022–23 Clemson Tigers women's basketball team") in the second round before losing to rivals [Duke](https://en.wikipedia.org/wiki/2022%E2%80%9323_Duke_Blue_Devils_women's_basketball_team "2022–23 Duke Blue Devils women's basketball team") in the quarterfinals. They received an at-large bid to the [NCAA Tournament](https://en.wikipedia.org/wiki/2023_NCAA_Division_I_women's_basketball_tournament "2023 NCAA Division I women's basketball tournament") and were the six seed in the [Seattle 3 Regional](https://en.wikipedia.org/wiki/2023_NCAA_Division_I_women's_basketball_tournament#Seattle_Regional_3_%E2%80%93_Climate_Pledge_Arena_%E2%80%93_Seattle,_WA "2023 NCAA Division I women's basketball tournament"). They defeated eleven seed [St. John's](https://en.wikipedia.org/wiki/2022%E2%80%9323_St._John's_Red_Storm_women's_basketball_team "2022–23 St.
</excerpt>
### Rank 5 of 89 — 0.78
<excerpt title="2022-23 Women's Basketball Coaching Staff">
# 2022-23 Women's Basketball Coaching Staff
## Coaching Staff
| Name | Title | Phone | Email Address |  
| --- | --- | --- | --- |  
| Courtney Banghart | Head Coach |  |  |  
| Joanne Aluka-White | Assistant Coach |  | [aluka@email.unc.edu](mailto:aluka@email.unc.edu) |  
| Itoro Coleman | Assistant Coach/Recruiting Coordinator |  |  |  
| Adrian Walters | Assistant Coach | 919-962-5411 | [adub2@email.unc.edu](mailto:adub2@email.unc.edu) |  
| Sam Miller | Director of Scouting and Video Operations/Assistant Coach | 919-260-1690 | [smiller1@unc.edu](mailto:smiller1@unc.edu) |  
| Sean Sullivan | Director of Player Personnel, Development and Recruiting Operations/Assistant Coach |  | [ssullivan@unc.edu](mailto:ssullivan@unc.edu) |  
| Jessika Carrington | Assistant to the AD/Director of Basketball Operations | 919-260-2581 | [Jcarunc@unc.edu](mailto:Jcarunc@unc.edu) |  
| Liz Roberts | Director of Recruiting Management and Student-Athlete Engagement |  | [lizrob@live.unc.edu](mailto:lizrob@live.unc.edu) |  
| Caleb Krueger | Head Strength and Conditioning Coach |  | [calebmhk@email.unc.edu](mailto:calebmhk@email.unc.edu) |  
| Andrew Graber | Assistant Strength & Conditioning Coach |  |  |  
| Dr. Josh Berkowitz | Team Physician | 919-966-3655 | [josh_berkowitz@med.unc.edu](mailto:josh_berkowitz@med.unc.edu) |  
| Jodi Schneider | Head Athletic Trainer | 919-962-2067 | [jodis@email.unc.edu](mailto:jodis@email.unc.edu) |  
| Emily Adney | Academic Counselor | 919-962-9536 | [emily6@email.unc.edu](mailto:emily6@email.unc.edu) |  

# 2022-23 Women's Basketball Coaching Staff
## Coaching Staff
| Dr. Jeni Shannon | Director, Mental Health and Performance Psychology | 919-966-3655 | [jenishannon@unc.edu](mailto:jenishannon@unc.edu) |  
| Dana Gelin | Director of Athletic Communications | 919-455-8289 (cell) | [dgelin@unc.edu](mailto:dgelin@unc.edu) |

# 2022-23 Women's Basketball Coaching Staff
## Footer
*     
*     
*     
*     
*
We educate and inspire through athletics
© 2026 University of North Carolina Athletics
*   Terms of Service  
*   Privacy Policy  
*   Accessibility  
*    Do Not Sell or Share My Personal Information
</excerpt>

## Search 5 — query: "Arizona Wildcats women's basketball 2022-23 head coach"
### Rank 1 of 102 — 0.81 (passed on)
<excerpt title="2022–23 Arizona Wildcats women's basketball team">
| No. 23 [Washington State](https://en.wikipedia.org/wiki/2022%E2%80%9323_Washington_State_Cougars_women's_basketball_team "2022–23 Washington State Cougars women's basketball team") † | 9 | – | 9 |  | .500 |  |  | 23 | – | 11 |  | .676 |  
| [Oregon](https://en.wikipedia.org/wiki/2022%E2%80%9323_Oregon_Ducks_women's_basketball_team "2022–23 Oregon Ducks women's basketball team") | 7 | – | 11 |  | .389 |  |  | 20 | – | 15 |  | .571 |  
| [Washington](https://en.wikipedia.org/wiki/2022%E2%80%9323_Washington_Huskies_women's_basketball_team "2022–23 Washington Huskies women's basketball team") | 7 | – | 11 |  | .389 |  |  | 19 | – | 15 |  | .559 |  
| [California](https://en.wikipedia.org/wiki/2022%E2%80%9323_California_Golden_Bears_women's_basketball_team "2022–23 California Golden Bears women's basketball team") | 4 | – | 14 |  | .222 |  |  | 13 | – | 17 |  | .433 |  
| [Oregon State](https://en.wikipedia.org/wiki/2022%E2%80%9323_Oregon_State_Beavers_women's_basketball_team "2022–23 Oregon State Beavers women's basketball team") | 4 | – | 14 |  | .222 |  |  | 13 | – | 18 |  | .419 |  

| [Arizona State](https://en.wikipedia.org/wiki/2022%E2%80%9323_Arizona_State_Sun_Devils_women's_basketball_team "2022–23 Arizona State Sun Devils women's basketball team") | 1 | – | 17 |  | .056 |  |  | 8 | – | 20 |  | .286 |  
|  |  
| † [2023 Pac-12 Tournament](https://en.wikipedia.org/wiki/2023_Pac-12_Conference_women's_basketball_tournament "2023 Pac-12 Conference women's basketball tournament") winner Rankings from [AP poll](https://en.wikipedia.org/wiki/2022%E2%80%9323_NCAA_Division_I_women's_basketball_rankings#AP_Poll "2022–23 NCAA Division I women's basketball rankings") |
The **2022–23 Arizona Wildcats women's basketball team** represented the University of Arizona during the [2022–23 NCAA Division I women's basketball season](https://en.wikipedia.org/wiki/2022%E2%80%9323_NCAA_Division_I_women's_basketball_season "2022–23 NCAA Division I women's basketball season"). The Wildcats were led by seventh-year head coach Adia Barnes. This was the Wildcats' 49th season at the on-campus McKale Center in Tucson, Arizona and 44th season as a member of the Pac-12 Conference.
</excerpt>
### Rank 2 of 102 — 0.77
<excerpt title="2022–23 Arizona Wildcats women's basketball team">
From Wikipedia, the free encyclopedia
| 2022–23[Arizona Wildcats women's basketball](https://en.wikipedia.org/wiki/Arizona_Wildcats_women's_basketball "Arizona Wildcats women's basketball") |  
| --- |  
|  |  
| [NCAA tournament](https://en.wikipedia.org/wiki/2023_NCAA_Division_I_women's_basketball_tournament "2023 NCAA Division I women's basketball tournament"), Second Round |  
| Conference | Pac-12 Conference |  
| Ranking |  
| AP | No.25 |  
| Record | 22–10 (11–7 Pac-12) |  
| Head coach | * Adia Barnes (7th season) |  
| Assistant coaches | * Ashley Davis (2nd season) * Salvo Coppa (7th season) * Erin Grant (2nd season) |  
| Home arena | McKale Center |  
| Seasons ←[2021–22](https://en.wikipedia.org/wiki/2021%E2%80%9322_Arizona_Wildcats_women's_basketball_team "2021–22 Arizona Wildcats women's basketball team") [2023–24](https://en.wikipedia.org/wiki/2023%E2%80%9324_Arizona_Wildcats_women's_basketball_team "2023–24 Arizona Wildcats women's basketball team")→ |

[2022–23 Pac-12 Conference women's basketball standings](https://en.wikipedia.org/wiki/2022%E2%80%9323_Pac-12_Conference_women's_basketball_season "2022–23 Pac-12 Conference women's basketball season")| * [v](https://en.wikipedia.org/wiki/Template:2022%E2%80%9323_Pac-12_Conference_women's_basketball_standings "Template:2022–23 Pac-12 Conference women's basketball standings") * [t](https://en.wikipedia.org/wiki/Template_talk:2022%E2%80%9323_Pac-12_Conference_women's_basketball_standings "Template talk:2022–23 Pac-12 Conference women's basketball standings") * [e](https://en.wikipedia.org/wiki/Special:EditPage/Template:2022%E2%80%9323_Pac-12_Conference_women's_basketball_standings "Special:EditPage/Template:2022–23 Pac-12 Conference women's basketball standings") | Conf. |  |  | Overall |  
| --- | --- | --- | --- | --- |  
| Team | W |  | L |  | PCT |  |  | W |  | L |  | PCT |  
| No. 8 [Utah](https://en.wikipedia.org/wiki/2022%E2%80%9323_Utah_Utes_women's_basketball_team "2022–23 Utah Utes women's basketball team") | 15 | – | 3 |  | .833 |  |  | 27 | – | 5 |  | .844 |
</excerpt>
### Rank 3 of 102 — 0.76
<excerpt title="Arizona women's basketball GM Michelle Marciniak announces ...">
# Arizona women’s basketball GM Michelle Marciniak announces departure from program
> After much reflection, I’ve made the difficult decision to step down from my role as General Manager of the [The University of Arizona](https://www.facebook.com/uarizona?__cft__[0]=AZbnlBatPMC0an6TDpV8qJ7j93t3fWad1CpgtFFuNJwCq8ML5zWjw_BRikr0pGFshVmcAdHAFVTDyrK371_zoU4HZ2ZmkOB6x0DvOL1tP5nipNd1pJAz6EHfQkCIDMLuKY1aYAIOT4cllxntsiepVw7t4AnL6orhV9jRL3_8uE-2uw&__tn__=-]K-R) Women’s Basketball program and return home to Knoxville, Tennessee - to be with my Mom as she continues to battle the relentless progressing disease of Alzheimer’s.  
>   
>   
> My Mom has always been there for me and it’s time to go home.  
>   
>   
> I’m incredibly grateful for my time at the University of Arizona. I want to sincerely thank Athletics Director Desiree Reed-Francois and her entire leadership team for their trust, support, and exemplary leadership. It was an honor to work alongside such dedicated colleagues who care deeply about student-athletes and the future of [Arizona Athletics](https://www.facebook.com/ArizonaWildcats?__cft__[0]=AZbnlBatPMC0an6TDpV8qJ7j93t3fWad1CpgtFFuNJwCq8ML5zWjw_BRikr0pGFshVmcAdHAFVTDyrK371_zoU4HZ2ZmkOB6x0DvOL1tP5nipNd1pJAz6EHfQkCIDMLuKY1aYAIOT4cllxntsiepVw7t4AnL6orhV9jRL3_8uE-2uw&__tn__=-]K-R).  
>   
>   

# Arizona women’s basketball GM Michelle Marciniak announces departure from program
> I’m also thankful to Coach [Becky Burke](https://www.facebook.com/becky.burke.73?__cft__[0]=AZbnlBatPMC0an6TDpV8qJ7j93t3fWad1CpgtFFuNJwCq8ML5zWjw_BRikr0pGFshVmcAdHAFVTDyrK371_zoU4HZ2ZmkOB6x0DvOL1tP5nipNd1pJAz6EHfQkCIDMLuKY1aYAIOT4cllxntsiepVw7t4AnL6orhV9jRL3_8uE-2uw&__tn__=-]K-R) for trusting me with a role that is still evolving in collegiate athletics. Building together with her, the staff, and our players has been a truly special experience and I’m proud to be a part of laying the foundation for the new era of Arizona WBB.  
>   
>   
> Thank you [Arizona Women’s Basketball](https://www.facebook.com/ArizonaWBB?__cft__[0]=AZbnlBatPMC0an6TDpV8qJ7j93t3fWad1CpgtFFuNJwCq8ML5zWjw_BRikr0pGFshVmcAdHAFVTDyrK371_zoU4HZ2ZmkOB6x0DvOL1tP5nipNd1pJAz6EHfQkCIDMLuKY1aYAIOT4cllxntsiepVw7t4AnL6orhV9jRL3_8uE-2uw&__tn__=-]K-R) fans. Your passion for WBB is truly special and some of the best support I’ve experienced in my career!  
>   
>
</excerpt>
### Rank 4 of 102 — 0.76
<excerpt title="2022–23 Arizona Wildcats women's basketball team">
| [Arizona State](https://en.wikipedia.org/wiki/2022%E2%80%9323_Arizona_State_Sun_Devils_women's_basketball_team "2022–23 Arizona State Sun Devils women's basketball team") | 1 | – | 17 |  | .056 |  |  | 8 | – | 20 |  | .286 |  
|  |  
| † [2023 Pac-12 Tournament](https://en.wikipedia.org/wiki/2023_Pac-12_Conference_women's_basketball_tournament "2023 Pac-12 Conference women's basketball tournament") winner Rankings from [AP poll](https://en.wikipedia.org/wiki/2022%E2%80%9323_NCAA_Division_I_women's_basketball_rankings#AP_Poll "2022–23 NCAA Division I women's basketball rankings") |
The **2022–23 Arizona Wildcats women's basketball team** represented the University of Arizona during the [2022–23 NCAA Division I women's basketball season](https://en.wikipedia.org/wiki/2022%E2%80%9323_NCAA_Division_I_women's_basketball_season "2022–23 NCAA Division I women's basketball season"). The Wildcats were led by seventh-year head coach Adia Barnes. This was the Wildcats' 49th season at the on-campus McKale Center in Tucson, Arizona and 44th season as a member of the Pac-12 Conference.

The Wildcats finished the 2021–22 season with a record of 21–8, 10–6 in Pac-12 play. The Wildcats were invited to the [2022 NCAA tournament](https://en.wikipedia.org/wiki/2022_NCAA_Division_I_women's_basketball_tournament "2022 NCAA Division I women's basketball tournament") where they defeated UNLV in the first round before losing to [North Carolina](https://en.wikipedia.org/wiki/2021%E2%80%9322_North_Carolina_Tar_Heels_women's_basketball_team "2021–22 North Carolina Tar Heels women's basketball team") in the second round.
Arizona Wildcats Departures| Name | Number | Pos. | Height | Year | Hometown | Notes |  
| --- | --- | --- | --- | --- | --- | --- |  
| Sam Thomas | 14 | F | 6'0 | Graduate Student | Bloomfield Hills, MI | Completed college eligibility |  
| Ariyah Copeland | 22 | F | 6'3 | Graduate Student | Columbus, GA | Completed college eligibility |  
| **Reference:** |
</excerpt>
### Rank 5 of 102 — 0.73
<excerpt title="2022-23 Women's Basketball Roster">
# 2022-23 Women's Basketball Roster
## Players
|  | 34 | Maya Nnaji | F | 6' 4'' | null | Fr. | Hopkins, Minn. | Hopkins HS |  |
| Coaching Staff |  
| --- |  
| Image | Name | Title | Email | Phone Number |  
|  | Adia Barnes | Head Coach | azwbball@arizona.edu | 520-621-4014 |  
|  | Salvo Coppa | Assistant Coach | coppa@arizona.edu | 520-621-4014 |  
|  | Ashley Davis | Assistant Coach |  | 520-621-4014 |  
|  | Erin Grant | Assistant Coach | grante@email.arizona.edu | 520-621-4014 |  
|  | Bett Shelby | Special Assistant to the Head Coach | bettyshelby@arizona.edu |  |  
|  | Kayla Scott | Director of Basketball Operations | scottke@email.arizona.edu |  |  
|  | Aari McDonald | Director of Recruiting Operations |  |  |  
|  | Bart Jameson | Associate Athletic Trainer | tbartjameson@arizona.edu | 520-621-0821 |  
|  | Matt Herrera | Manager of Creative Media | matthewherrera@arizona.edu |  |  
|  | Julian Mills | Video Coordinator |  |  |  
|  | Jaime Fernandez | Assistant Coach, Performance Enhancement | jaimef1@arizona.edu | 520-621-6915 |  
|  | Hailey Loftin | Associate Director of Communication Services (WBB) | hloftin@arizona.edu | 520-626-9395 |

# 2022-23 Women's Basketball Roster
## Related News
Skip Ad
All News
Skip Ad
Arizona Takes Down Oregon State in Overtime Thriller 84-80 Arizona Takes Down Oregon State in Overtime Thriller 84-80
Sunday, November 15
Arizona Returns Home to Host Oregon State Sunday Arizona Returns Home to Host Oregon State Sunday
Saturday, November 14
Arizona Falls at No. 10 UCLA, 76-44 Arizona Falls at No. 10 UCLA, 76-44
Thursday, November 12
Arizona Women’s Basketball Signs Four to 2027 Class Arizona Women’s Basketball Signs Four to 2027 Class
Wednesday, November 11
All News

# 2022-23 Women's Basketball Roster
## Related Videos
Skip Ad
All Videos
Skip Ad
Arizona Women's Basketball Press Conference Arizona Women's Basketball Press Conference
Sunday, November 15
McKale Center at Alkeme Arena Game Day Enhancements McKale Center at Alkeme Arena Game Day Enhancements
Tuesday, November 03
Arizona Women's Basketball Press Conference - Sumayah Sugapong & Molly Ladwig Arizona Women's Basketball Press Conference - Sumayah Sugapong & Molly Ladwig
Tuesday, August 18
Arizona Women's Basketball Press Conference - Becky Burke Arizona Women's Basketball Press Conference - Becky Burke
Tuesday, August 18
All Videos
Skip Ad
Skip Ad
</excerpt>

## Search 6 — query: "Paige Bueckers points per game 2022-23 UConn women's basketball"
### Rank 1 of 179 — 0.61 (passed on)
<excerpt title="Paige Bueckers">
Year	Team	GP	GS	MPG	FG%	3P%	FT%	RPG	APG	SPG	BPG	TO	PPG  
2020–21	UConn	29	29	36.1	.524	.464	.869	4.9	5.8	2.3	.4	2.5	20.0  
2021–22	UConn	17	13	29.2	.544	.353	.714	4.0	3.9	1.5	.6	1.7	14.6  
2022–23	UConn	Did not play due to injury  
2023–24	UConn	39	39	31.9	.530	.416	.834	5.2	3.8	2.2	1.4	1.5	21.9  
2024–25*	UConn	38	38	30.3	.534	.419	.889	4.4	4.6	2.1	.8	1.3	19.9  
Career	123	119	32.0	.531	.423	.850	4.7	4.6	2.1	.8	1.7	19.8  
Statistics gathered from Sports-Reference.[234]  
Personal lifeedit  
Bueckers attending a Minnesota Lynx game in 2023
</excerpt>
### Rank 2 of 179 — 0.54
<excerpt title="2023-24 Women's Basketball Cumulative Statistics">
| Player uniform | Player name | GP | GS | MINUTES | SCORING | FG | 3PT | FT | REBOUNDS | PF | AST | TO | STL | BLK |  
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |  
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  
| 05 | Bueckers, Paige | 39 | 39 | 1244 | 31.9 | 854 | 21.9 | 317 | 598 | .530 | 84 | 202 | .416 | 136 | 163 | .834 | 34 | 168 | 202 | 5.2 | 64 | 150 | 60 | 86 | 53 |  
| 03 | Edwards, Aaliyah | 37 | 37 | 1126 | 30.4 | 652 | 17.6 | 261 | 440 | .593 | 0 | 3 | .000 | 130 | 174 | .747 | 89 | 252 | 341 | 9.2 | 95 | 76 | 93 | 62 | 36 |  
| 12 | Shade, Ashlynn | 38 | 33 | 1188 | 31.3 | 419 | 11.0 | 167 | 347 | .481 | 64 | 180 | .356 | 21 | 23 | .913 | 28 | 105 | 133 | 3.5 | 52 | 55 | 39 | 37 | 4 |
</excerpt>
### Rank 3 of 179 — 0.53
<excerpt title="Paige Bueckers injury: How UConn star's career has unfolded, what this ...">
# Paige Bueckers injury: How UConn star's career has unfolded, what this all means for Huskies in 2022-23
## But now...
Although UConn lost Nelson-Odada and Williams, a healthy Bueckers alongside Fudd seemed capable of lifting the team to similar heights in 2022-23. The Huskies were expected to be very competitive once again, but now the question is who will step up for Bueckers in wake of her devastating injury.
Bueckers ended her sophomore campaign with averages of 14.6 points, 4.0 rebounds, 3.9 assists and 1.5 steals while shooting 54.4% from the field in 17 games. Those stats weren't as strong as they were in her freshman season, but they would've likely been the same or better had it not been for her midseason injury. Bueckers is impactful on both sides of the ball, and the Huskies will certainly miss that next season as they figure out their depth.
Without Nelson-Odada, a 6-foot-5 forward, the team loses its leader in shooting percentage (59.5%) and rebounding (7.5 per game) from a season ago. She also had the most steals (55) and assists (116) on the team last season. Meanwhile, Williams left as the second-leading scorer behind Bueckers, as she averaged 14.2 points per game in 2021-22.
So, Fudd is now UConn's only double-digit scorer returning. Last season, she averaged 12.1 points per game while shooting 45.7% from the field and a team-best 43.0% from 3-point range. The 5-foot-11 guard will be entering her sophomore season with a bigger role than she probably expected.
Staying healthy will be more important than ever for the Huskies. Other players working on recovery this offseason are Dorka Juhász (wrist), Caroline Ducharme (hip) and Aubrey Griffin (back). Griffin, a 6-foot-1 forward, dealt with a handful of injuries and missed all of last season, undergoing back surgery in January.
</excerpt>
### Rank 4 of 179 — 0.46
<excerpt title="2023-24 Women's Basketball Cumulative Statistics">
Skip to main contentAll Rotators Playing
*   2026-27  
*   2025-26  
*   2024-25  
*   2023-24  
*   2022-23  
*   2021-22  
*   2020-21  
*   2019-20  
*   2018-19  
*   2017-18  
*   2016-17  
*   2015-16
View PDF
*   Overall  
*   Conference

*   Totals  
*   Scoring  
*   Averages
GP -  Games Played
GS -  Games Started
MIN -  Total Minutes
AVG -  Average Minutes Per Game
PTS -  Points
AVG -  Average Points Per Game
FGM -  Field Goals Made
FGA -  Field Goals Attempted
FG% -  Field Goal Percentage
3PT -  3-Point Field Goals Made
3PTA -  3-Point Field Goals Attempted
3PT% -  3-Point Field Goal Percentage
FTM -  Free Throws Made
FTA -  Free Throws Attempted
FT% -  Free Throw Percentage
OFF -  Offensive Rebounds
DEF -  Defensive Rebounds
TOT -  Total Rebounds
AVG -  Average Rebounds Per Game
PF -  Personal Fouls
AST -  Assists
TO -  Turnovers
STL -  Steals
BLK -  Blocks

| Player uniform | Player name | GP | GS | MINUTES | SCORING | FG | 3PT | FT | REBOUNDS | PF | AST | TO | STL | BLK |  
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |  
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  
| 05 | Bueckers, Paige | 39 | 39 | 1244 | 31.9 | 854 | 21.9 | 317 | 598 | .530 | 84 | 202 | .416 | 136 | 163 | .834 | 34 | 168 | 202 | 5.2 | 64 | 150 | 60 | 86 | 53 |  
| 03 | Edwards, Aaliyah | 37 | 37 | 1126 | 30.4 | 652 | 17.6 | 261 | 440 | .593 | 0 | 3 | .000 | 130 | 174 | .747 | 89 | 252 | 341 | 9.2 | 95 | 76 | 93 | 62 | 36 |  
| 12 | Shade, Ashlynn | 38 | 33 | 1188 | 31.3 | 419 | 11.0 | 167 | 347 | .481 | 64 | 180 | .356 | 21 | 23 | .913 | 28 | 105 | 133 | 3.5 | 52 | 55 | 39 | 37 | 4 |
</excerpt>
### Rank 5 of 179 — 0.45
<excerpt title="Paige Bueckers">
Bueckers made her season debut on November 14, 2021, recording a season-high 34 points, six rebounds, and four assists in a 95–80 win against Arkansas.[105] She matched the program record for points in a season opener set by Kerry Bascom in 1989.[106][107] On December 5, Bueckers injured her left knee while dribbling the ball up the court with 40 seconds remaining in a 73–54 victory over Notre Dame, and had to be carried off the floor by teammates. An MRI and CT scans revealed that she suffered a tibial plateau fracture with an estimated recovery period of six to eight weeks.[108] On December 13, Bueckers underwent surgery to repair the fracture and a previously undisclosed lateral meniscus tear. She was expected to be sidelined for eight more weeks.[109] During Bueckers' absence, UConn had a 15–4 record and briefly fell out of the top 10 in the AP Poll for the first time since 2005.[110] The team's winning streaks of 240 games against unranked teams and 169 games against conference opponents ended in losses to Georgia Tech and Villanova, respectively.[111][112]

Bueckers was cleared to return against St. John's on February 25, 2022. She came off the bench for the first time in her career and scored 8 points, playing only 13 minutes due to a minutes restriction, in a 93–38 victory.[113] Bueckers continued to receive limited playing time until the NCAA tournament,[114] and UConn won the Big East tournament despite her scoring only two points in the championship game against Villanova.[115] Her offensive production also declined from before her injury.[116] On March 28, at the Elite Eight of the NCAA Tournament, Bueckers led her team to a 91–87 double-overtime win over top-seeded NC State, as UConn reached its 14th consecutive Final Four. She scored a game-high 27 points on 10-15 from the field, including 15 points in the two overtime periods (4-5 from the field and 6-6 from the free-throw line), and was named MOP of the Bridgeport Regional.[117] In the Final Four, Bueckers recorded 14 points, five assists and four rebounds in a 63–58 victory against top-seeded Stanford, the defending champions.[118][119] In a 64–49 loss to top-seeded South Carolina at the national championship game,[120] Bueckers was the only UConn player to score in double digits as she posted 14 points and six rebounds, and was named to the Final Four All-Tournament Team.[121] Bueckers was an AP All-American Honorable Mention selection.[122] As a sophomore, she averaged 14.6 points, four rebounds and 3.9 assists per game.[123]
In addition to her athletic honors, Bueckers was again named to the university's dean's list for her first semester as a sophomore.[1]
Redshirt yearedit
</excerpt>

## Search 7 — query: "2022-23 South Carolina Gamecocks women's basketball leading scorer points per game"
### Rank 1 of 217 — 0.75 (passed on)
<excerpt title="south carolina gamecocks - Women's College Basketball">
my favs Access and manage your favorites here DISMISS
*   Scores  
*   Watch  
*   Betting  
*   Stories

*   SPORTS & TEAMS  
*   PLAYERS  
*   SHOWS  
*   PERSONALITIES  
*   TOPICS
POPULAR SEARCHES
- No Data Available -
BROWSE BY
Built on
1 SOUTH CAROLINA GAMECOCKS 5-0 · 8TH IN SEC
5-0 · 8TH IN SEC
WOMENS COLLEGE BASKETBALL>

## NEWS## SCHEDULE## STANDINGS## ROSTER## STATS## ODDS## GAME LOG


## PLAYER STATS
### Points Per Game Tessa Johnson 17.0 PPG### Three Point Field Goals Made Per Game Tessa Johnson 2.3 3FGM/G### Free Throws Made Per Game Chloe Kitts 4.0 FTM/G### High Game Points Tessa Johnson 28 HIGH### Rebounds Per Game Chloe Kitts 10.3 RPG### True Shooting Percentage Alicia Tournebize 80.0 TS%### Assists Per Game Chloe Kitts 3.0 APG### Turnovers Per Game Joyce Edwards 2.8 TPG### Steals Per Game Joyce Edwards 2.0 SPG### Blocks Per Game Alicia Tournebize 1.3 BPG### Fouls Per Game Jerzy Robinson 3.0 FPG### Usage Rate Oliviyah Edwards 28.6 USG%### Effective Field Goal Percentage Alicia Tournebize 80.0 EFG%### Minutes Per Game Tessa Johnson 29.3 MPG

## TEAM STATS
### Points Per Game 84.8 PPG T-31ST OVERALL### Three Point Field Goals Made Per Game 5.5 3FGM/G### Free Throws Made Per Game 19.8 FTM/G### Points Per Game Differential 19.5 PPG DIFF### Rebounds Per Game 38.8 RPG T-63RD OVERALL### Rebounds Per Game Differential 9.5 RPG DIFF### Field Goal Percentage 48.4 FG% 27TH OVERALL### True Shooting Percentage - TS%### Assists Per Game 16.5 APG T-71ST OVERALL### Turnovers Per Game 16.5 TPG### Steals Per Game 9.8 SPG### Blocks Per Game 5.0 BPG### Personal Fouls Per Game 18.5 PFPG### Offensive Rating 112.2 OFF RTG### Defensive Rating 86.4 DEF RTG
Top Leagues
NFLCollege FootballINDYCARMLBCollege BasketballNASCAR
Top Shows
The Herd with Colin CowherdFirst Things FirstThe Joel Klatt ShowKevin Harvick's Happy HourBear Bets
Affiliated Apps
FOX SportsFOX One
Quick Links
Best Betting Apps & SitesBest Sportsbook PromosWatch Ravens vs PanthersWatch Saints vs BearsWatch Titans vs CowboysWatch Buccaneers vs LionsWatch Jets vs Chargers
FOX SPORTS™, SPEED™, SPEED.COM™ & © 2026 Fox Media LLC and Fox Sports Interactive Media, LLC. All rights reserved. Use of this website (including any and all parts and components) constitutes your acceptance of these Terms of Use andPrivacy Policy |Advertising Choices | Your Privacy Choices |Closed Captioning
HelpPressAdvertise with UsJobsRSSSitemap
FS1FOXFOX NewsFox CorporationFOX Sports SupportsFOX Deportes
</excerpt>
### Rank 2 of 217 — 0.74
<excerpt title="Early roster analysis for USC women's basketball in 2022-23">
Dawn Staleyhad plenty of talent to manage throughout the 2021-22 national championship season for South Carolina women’s basketball.
The Gamecocks are on track to return many key pieces and reload with more talent behind next year’s hopes of becoming the fourth NCAA women’s basketball program to win back-to-back titles.
Here’s an early look at how the Gamecocks’ roster is shaping up for the 2022-23 campaign.

### 1. Four of USC’s five national championship starters return
Part of this season’s recipe for national championship success for South Carolina was that it returned the entire roster from the 2020-21 Final Four team. This time, the Gamecocks return all but one starter.
Aliyah Boston will enter her senior year as the nation’s best player, unanimously selected as national player of the year behind a record-breaking season of 27 straight double-doubles. The 6-foot-5 forward led the Gamecocks on both ends of the floor — as USC’s best scorer (16.8 points per game) and rebounder (12.5 boards per game) — and is set to continue to be a matchup nightmare for opposing teams.
Brea Beal has fully come into her role as the Gamecocks’ defensive specialist, bringing 100 career starts into her final campaign in Columbia. The 6-foot-1 guard scored less often as a junior than she did as a sophomore — averaging 5.1 last season compared with 7.1 the year prior — but her veteran presence is set to lead one of the nation’s most prolific defenses next year.
Zia Cooke’s junior campaign was more inconsistent than either of her first two seasons with USC, averaging a career-low 10.7 points per game on 34.2% shooting. The 5-foot-9 guard has room to grow but still made her impact known with big games against North Carolina and Louisville in this year’s NCAA tournament.
Veteran starter Victaria Saxton’s decision to return for a fifth year solidified the return of the Gamecocks’ formidable frontcourt. The 6-foot-2 forward showed her impact throughout the season as the team’s second-best rebounder and shot blocker, but she was undeniably important to South Carolina’s Sweet 16 win over North Carolina (6 points, 14 rebounds) and Elite Eight victory over Creighton (11 points, 11 rebounds).

### 2. Managing USC’s departures
A notable piece missing from last year’s starting five is point guard Destanni Henderson, who left South Carolina on a high note behind a career-best 26 points in the national championship victory over UConn. She’s projected to go in the first round of the WNBA draft after two seasons as South Carolina’s starting point guard, during which she led the Gamecocks to back-to-back Final Fours and the title win.
Veteran reserve LeLe Grissett exhausted her eligibility after taking a final year to play with USC after missing the 2021 NCAA tournament due to injury. Grissett provided sparks both on and off the floor, and that will be tough to replicate.
The Gamecocks will also deal with two transfer portal departures from reserves Elysa Wesolek and Eniya Russell. Both Wesolek and Russell saw limited minutes in the 2021-22 season. Wesolek, a senior, has one year of eligibility remaining, while Russell has two.
Destiny Littleton has been on a college basketball roster for five years, sitting out the 2019-20 season after transferring to USC from Texas. The Gamecocks’ 3-point specialist off the bench could, in theory, return for another season, though she earned her undergraduate degree in 2021 and was recognized in this year’s senior day ceremonies.
</excerpt>
### Rank 3 of 217 — 0.71
<excerpt title="South Carolina Gamecocks women's basketball statistical leaders">
| 2 | [A'ja Wilson](https://en.wikipedia.org/wiki/A'ja_Wilson "A'ja Wilson") | 103 | [2015–16](https://en.wikipedia.org/wiki/2015%E2%80%9316_South_Carolina_Gamecocks_women's_basketball_team "2015–16 South Carolina Gamecocks women's basketball team") |  
| 3 | Ashlyn Watkins | 91[[12]](https://en.wikipedia.org/wiki/South_Carolina_Gamecocks_women's_basketball_statistical_leaders#cite_note-AWESPN-12) | [2023–24](https://en.wikipedia.org/wiki/2023%E2%80%9324_South_Carolina_Gamecocks_women's_basketball_team "2023–24 South Carolina Gamecocks women's basketball team") |  
| 4 | Aliyah Boston | 90 | [2021–22](https://en.wikipedia.org/wiki/2021%E2%80%9322_South_Carolina_Gamecocks_women's_basketball_team "2021–22 South Carolina Gamecocks women's basketball team") |  
|  | [A'ja Wilson](https://en.wikipedia.org/wiki/A'ja_Wilson "A'ja Wilson") | 90 | [2016–17](https://en.wikipedia.org/wiki/2016%E2%80%9317_South_Carolina_Gamecocks_women's_basketball_team "2016–17 South Carolina Gamecocks women's basketball team") |  
| 6 | Aliyah Boston | 86 | [2019–20](https://en.wikipedia.org/wiki/2019%E2%80%9320_South_Carolina_Gamecocks_women's_basketball_team "2019–20 South Carolina Gamecocks women's basketball team") |  

| 7 | Elem Ibiam | 83 | [2013–14](https://en.wikipedia.org/wiki/2013%E2%80%9314_South_Carolina_Gamecocks_women's_basketball_team "2013–14 South Carolina Gamecocks women's basketball team") |  
| 8 | Kamilla Cardoso | 82[[10]](https://en.wikipedia.org/wiki/South_Carolina_Gamecocks_women's_basketball_statistical_leaders#cite_note-KCESPN-10) | [2023–24](https://en.wikipedia.org/wiki/2023%E2%80%9324_South_Carolina_Gamecocks_women's_basketball_team "2023–24 South Carolina Gamecocks women's basketball team") |  
| 9 | Aliyah Boston | 81 | [2020–21](https://en.wikipedia.org/wiki/2020%E2%80%9321_South_Carolina_Gamecocks_women's_basketball_team "2020–21 South Carolina Gamecocks women's basketball team") |  
| 10 | Aliyah Boston | 73 | [2022–23](https://en.wikipedia.org/wiki/2022%E2%80%9323_South_Carolina_Gamecocks_women's_basketball_team "2022–23 South Carolina Gamecocks women's basketball team") |  
|  | Alaina Coates | 73 | [2013–14](https://en.wikipedia.org/wiki/2013%E2%80%9314_South_Carolina_Gamecocks_women's_basketball_team "2013–14 South Carolina Gamecocks women's basketball team") |Single game  
| Rank | Player | Blocks | Season | Opponent |  
| --- | --- | --- | --- | --- |
</excerpt>
### Rank 4 of 217 — 0.65
<excerpt title="South Carolina Gamecocks women's basketball statistical leaders">
| 7 | Elem Ibiam | 83 | [2013–14](https://en.wikipedia.org/wiki/2013%E2%80%9314_South_Carolina_Gamecocks_women's_basketball_team "2013–14 South Carolina Gamecocks women's basketball team") |  
| 8 | Kamilla Cardoso | 82[[10]](https://en.wikipedia.org/wiki/South_Carolina_Gamecocks_women's_basketball_statistical_leaders#cite_note-KCESPN-10) | [2023–24](https://en.wikipedia.org/wiki/2023%E2%80%9324_South_Carolina_Gamecocks_women's_basketball_team "2023–24 South Carolina Gamecocks women's basketball team") |  
| 9 | Aliyah Boston | 81 | [2020–21](https://en.wikipedia.org/wiki/2020%E2%80%9321_South_Carolina_Gamecocks_women's_basketball_team "2020–21 South Carolina Gamecocks women's basketball team") |  
| 10 | Aliyah Boston | 73 | [2022–23](https://en.wikipedia.org/wiki/2022%E2%80%9323_South_Carolina_Gamecocks_women's_basketball_team "2022–23 South Carolina Gamecocks women's basketball team") |  
|  | Alaina Coates | 73 | [2013–14](https://en.wikipedia.org/wiki/2013%E2%80%9314_South_Carolina_Gamecocks_women's_basketball_team "2013–14 South Carolina Gamecocks women's basketball team") |Single game  
| Rank | Player | Blocks | Season | Opponent |  
| --- | --- | --- | --- | --- |  

| 1 | Aliyah Boston | 10 | [2020–21](https://en.wikipedia.org/wiki/2020%E2%80%9321_South_Carolina_Gamecocks_women's_basketball_team "2020–21 South Carolina Gamecocks women's basketball team") | Georgia |  
|  | Aliyah Boston | 10 | [2019–20](https://en.wikipedia.org/wiki/2019%E2%80%9320_South_Carolina_Gamecocks_women's_basketball_team "2019–20 South Carolina Gamecocks women's basketball team") | Alabama State |  
|  | Alaina Coates | 10 | [2015–16](https://en.wikipedia.org/wiki/2015%E2%80%9316_South_Carolina_Gamecocks_women's_basketball_team "2015–16 South Carolina Gamecocks women's basketball team") | Winthrop |  
| 4 | Laeticia Amihere | 9 | [2020–21](https://en.wikipedia.org/wiki/2020%E2%80%9321_South_Carolina_Gamecocks_women's_basketball_team "2020–21 South Carolina Gamecocks women's basketball team") | Texas |  
|  | [A'ja Wilson](https://en.wikipedia.org/wiki/A'ja_Wilson "A'ja Wilson") | 8 | [2017–18](https://en.wikipedia.org/wiki/2017%E2%80%9318_South_Carolina_Gamecocks_women's_basketball_team "2017–18 South Carolina Gamecocks women's basketball team") | Temple |
</excerpt>
### Rank 5 of 217 — 0.61
<excerpt title="South Carolina Gamecocks women's basketball statistical leaders">
| 7 | Katrina Anderson | 371 | [1978–79](https://en.wikipedia.org/wiki/1978%E2%80%9379_South_Carolina_Gamecocks_women's_basketball_team?action=edit&redlink=1 "1978–79 South Carolina Gamecocks women's basketball team (page does not exist)") |  
| 8 | Aliyah Boston | 364 | [2022–23](https://en.wikipedia.org/wiki/2022%E2%80%9323_South_Carolina_Gamecocks_women's_basketball_team "2022–23 South Carolina Gamecocks women's basketball team") |  
| 9 | Denise Nanney | 361 | [1974–75](https://en.wikipedia.org/wiki/1974%E2%80%9375_South_Carolina_Gamecocks_women's_basketball_team?action=edit&redlink=1 "1974–75 South Carolina Gamecocks women's basketball team (page does not exist)") |  
| 10 | Alaina Coates | 360 | [2015–16](https://en.wikipedia.org/wiki/2015%E2%80%9316_South_Carolina_Gamecocks_women's_basketball_team "2015–16 South Carolina Gamecocks women's basketball team") |Single game  
| Rank | Player | Rebounds | Season | Opponent |  
| --- | --- | --- | --- | --- |  
| 1 | Demetress Adams | 26 | [2007–08](https://en.wikipedia.org/wiki/2007%E2%80%9308_South_Carolina_Gamecocks_women's_basketball_team?action=edit&redlink=1 "2007–08 South Carolina Gamecocks women's basketball team (page does not exist)") | Arkansas |  

| 2 | Aliyah Boston | 25 | [2019–20](https://en.wikipedia.org/wiki/2019%E2%80%9320_South_Carolina_Gamecocks_women's_basketball_team "2019–20 South Carolina Gamecocks women's basketball team") | Arkansas |  
| 3 | [A'ja Wilson](https://en.wikipedia.org/wiki/A'ja_Wilson "A'ja Wilson") | 24 | [2017–18](https://en.wikipedia.org/wiki/2017%E2%80%9318_South_Carolina_Gamecocks_women's_basketball_team "2017–18 South Carolina Gamecocks women's basketball team") | LSU |  
|  | Denise Nanney | 24 | [1974–75](https://en.wikipedia.org/wiki/1974%E2%80%9375_South_Carolina_Gamecocks_women's_basketball_team?action=edit&redlink=1 "1974–75 South Carolina Gamecocks women's basketball team (page does not exist)") | Anderson |  
| 5 | Denise Nanney | 23 | [1974–75](https://en.wikipedia.org/wiki/1974%E2%80%9375_South_Carolina_Gamecocks_women's_basketball_team?action=edit&redlink=1 "1974–75 South Carolina Gamecocks women's basketball team (page does not exist)") | Davidson |  
| 6 | Aliyah Boston | 22 | [2021–22](https://en.wikipedia.org/wiki/2021%E2%80%9322_South_Carolina_Gamecocks_women's_basketball_team "2021–22 South Carolina Gamecocks women's basketball team") | North Carolina |
</excerpt>

## Search 8 — query: "Washington Huskies women's basketball 2022-23 head coach"
### Rank 1 of 68 — 0.72 (passed on)
<excerpt title="Tina Langley">
**Tina Michelle Langley** (born September 3, 1973) is the current head coach of the [Washington Huskies women's basketball](https://en.wikipedia.org/wiki/Washington_Huskies_women's_basketball "Washington Huskies women's basketball") team.[[1]](https://en.wikipedia.org/wiki/Tina_Langley#cite_note-1) From 2015 to 2021, she was head coach for the [Rice Owls women's basketball](https://en.wikipedia.org/wiki/Rice_Owls_women's_basketball "Rice Owls women's basketball") team.[[2]](https://en.wikipedia.org/wiki/Tina_Langley#cite_note-2) Before joining Rice, she served as an associate head coach for the [Maryland Terrapins women's basketball team](https://en.wikipedia.org/wiki/Maryland_Terrapins_women's_basketball "Maryland Terrapins women's basketball"), helping the program advance to the Final Four in 2014 and 2015.[[3]](https://en.wikipedia.org/wiki/Tina_Langley#cite_note-3)

## Head coaching record
[edit]
Record table| Season | Team | Overall | Conference | Standing | Postseason |  
| --- | --- | --- | --- | --- | --- |  
| **[Rice Owls](https://en.wikipedia.org/wiki/Rice_Owls_women's_basketball "Rice Owls women's basketball")**_(Conference USA)_(2015–2021) |  
| [2015–16](https://en.wikipedia.org/wiki/2015%E2%80%9316_NCAA_Division_I_women's_basketball_season "2015–16 NCAA Division I women's basketball season") | [Rice](https://en.wikipedia.org/wiki/2015%E2%80%9316_Rice_Owls_women's_basketball_team "2015–16 Rice Owls women's basketball team") | 9–22 | 6–11 | T–8th |  |  
| [2016–17](https://en.wikipedia.org/wiki/2016%E2%80%9317_NCAA_Division_I_women's_basketball_season "2016–17 NCAA Division I women's basketball season") | [Rice](https://en.wikipedia.org/wiki/2016%E2%80%9317_Rice_Owls_women's_basketball_team "2016–17 Rice Owls women's basketball team") | 22–13 | 8–10 | T–8th | [WBI champions](https://en.wikipedia.org/wiki/2017_Women's_Basketball_Invitational "2017 Women's Basketball Invitational") |
</excerpt>
### Rank 2 of 68 — 0.67
<excerpt title="Tina Langley - Women's Basketball Coach - University of Washington ...">
# Tina Langley - Women's Basketball
Skip Ad
Langley, Tina
*   Bowlin, Patrick  
*   Brown, Tasha  
*   Donnelly, Buddy  
*   Goodman, Aleah  
*   Jackson, Mark  
*   King, Latara   
*   Langley, Tina  
*   Wilson, Drew  
*   Wilson, Lauren
vs
**Stanford**  
Nov 20 (Fri)
7:00 PM
Buy From$15+
Tina Langley
*   Title: Head Coach
Skip Ad
Bio
Tina Langley has established herself as one of women’s college basketball’s premier program builders, earning a national reputation for transforming multiple programs into thriving championship contenders. A proven coach with multiple Final Four appearances and a track record of on- and off-the-court success, Langley has twice inherited teams near the bottom of their conferences and elevated them into nationally ranked programs. At Washington, she has restored the Huskies to recent national prominence, guiding the program to consecutive NCAA Tournament appearances and reestablishing its place among the nation’s Top 25.
Named the 12th head coach in Washington history on April 5, 2021, Langley enters the 2026–27 season after engineering one of the nation’s most impressive turnarounds. Since arriving on Montlake, she has led steady year-over-year progress, taking the Huskies from last place in the Pac-12 to a No. 24 final Associated Press ranking and the highest NET finish in program history at No. 22 in 2026. In just five seasons, she has transformed Washington into a consistent postseason contender with national momentum. Langley’s teams are known for their discipline, offensive efficiency and defensive toughness.
The foundation of that resurgence was laid quickly and has correlated with Langley’s relentless commitment to a values-based, people-first culture. Nothing speaks to this more prominently than the Huskies’ unprecedented continuity across their entire basketball operation.

# Tina Langley - Women's Basketball
In 2022–23, Washington improved from seven wins to 19, marking the second-largest single-season turnaround in program history. In Washington’s inaugural Big Ten season (2024–25), the Huskies also made history by leading the conference in field goal percentage (49.5%), three-point percentage (40.1%) and free throw percentage (83.6%) during league play while finishing the regular season on a five-game winning streak. The Huskies have since reached the NCAA Tournament in back-to-back seasons for the first time in more than a decade, highlighted by a No. 6 seed in 2026.
During the 2025–26 campaign, Washington recorded 22 victories, 10 conference wins, seven road wins and 13 home wins, all the program’s highest totals since 2016–17. The 2025–26 Huskies also earned a school-record six victories over Top 30 NET opponents and built one of the nation’s elite defenses, holding eight NCAA Tournament teams to their lowest or second-lowest scoring outputs of the season.
Player acquisition and development have also been a hallmark of Langley’s career and is demonstrated in the multiple individual awards her players have received. In 2025–26, Sayvia Sellers earned First Team All-Big Ten honors, Avery Howell received All-Big Ten Honorable Mention recognition, and Brynn McGaughy was selected to the unanimous All-Big Ten Freshman Team. Across her coaching career, Langley has developed 56 all-conference performers in total and coached 14 WNBA Draft selections. At Washington, Dalayah Daniels became the program’s first WNBA Draft pick since 2017, while Elle Ladine and Nancy Mulkey also advanced to the professional ranks under her leadership.
</excerpt>
### Rank 3 of 68 — 0.66
<excerpt title="Tina Langley">
From Wikipedia, the free encyclopedia
Tina Langley
Langley with [Washington](https://en.wikipedia.org/wiki/Washington_Huskies_women's_basketball "Washington Huskies women's basketball") in 2025  
Current position  
TitleHead coach  
Team[Washington](https://en.wikipedia.org/wiki/Washington_Huskies_women's_basketball "Washington Huskies women's basketball")  
ConferenceBig Ten  
Record 86–71 (.548)  
Biographical details  
Born September 3, 1973 (age 53)
Jasper, Alabama, U.S.  
Playing career  
1991–1993Bevill State CC  
1993–1995West Alabama  
PositionPoint guard  
Coaching career (HC unless noted)  
1998–2003[Toledo](https://en.wikipedia.org/wiki/Toledo_Rockets_women's_basketball "Toledo Rockets women's basketball") (assistant)  
2003–2005[Clemson](https://en.wikipedia.org/wiki/Clemson_Tigers_women's_basketball "Clemson Tigers women's basketball") (assistant)  
2005Georgia (assistant)  
2008–2015[Maryland](https://en.wikipedia.org/wiki/Maryland_Terrapins_women's_basketball "Maryland Terrapins women's basketball") (assistant)  
2015–2021[Rice](https://en.wikipedia.org/wiki/Rice_Owls_women's_basketball "Rice Owls women's basketball")  
2021–present[Washington](https://en.wikipedia.org/wiki/Washington_Huskies_women's_basketball "Washington Huskies women's basketball")  
Head coaching record  
Overall 212–132 (.616)

**Tina Michelle Langley** (born September 3, 1973) is the current head coach of the [Washington Huskies women's basketball](https://en.wikipedia.org/wiki/Washington_Huskies_women's_basketball "Washington Huskies women's basketball") team.[[1]](https://en.wikipedia.org/wiki/Tina_Langley#cite_note-1) From 2015 to 2021, she was head coach for the [Rice Owls women's basketball](https://en.wikipedia.org/wiki/Rice_Owls_women's_basketball "Rice Owls women's basketball") team.[[2]](https://en.wikipedia.org/wiki/Tina_Langley#cite_note-2) Before joining Rice, she served as an associate head coach for the [Maryland Terrapins women's basketball team](https://en.wikipedia.org/wiki/Maryland_Terrapins_women's_basketball "Maryland Terrapins women's basketball"), helping the program advance to the Final Four in 2014 and 2015.[[3]](https://en.wikipedia.org/wiki/Tina_Langley#cite_note-3)
</excerpt>
### Rank 4 of 68 — 0.64
<excerpt title="Tina Langley - Women's Basketball Coach - University of Washington ...">
# Tina Langley - Women's Basketball Coach - University of Washington Athletics
Skip Ad
*   DAWGS UNLEASHED

    *   Dawgs Unleashed  
    *   Washington Huskies Exchange  
    *   Custom Pick-A-Player Apparel
Skip Ad
*   CONTENT

    *   Go Huskies App Presented by WaFd Bank  
    *   GoHuskies News Presented by Banner Bank  
    *   GoHuskies Magazine  
    *   GoHuskies Podcast with Tony Castricone Presented by Air Van Moving  
    *   Husky E-News  
    *   Husky All-Access: Photos  
    *   Husky All-Access: Videos  
    *   Huskies New Era Archives

    *   Social Media Directory  
    *   Football Broadcast Info  
    *   Live Audio  
    *   Big Ten Network  
    *   B1G+  
    *   RSS Feeds
Skip Ad
*   SHOP

    *   Official Online Store  
    *   Team Gear  
    *   Men  
    *   Women  
    *   Kids

    *   Hats  
    *   Gameday & Tailgate  
    *   Drinkware  
    *   Auto Accessories  
    *   Flags & Banners
Skip Ad
*   UW.EDU
Returning to Main Navigation
Skip Ad
*   Women's BasketballSkip Ad         
*   Schedule  
*   Roster  
*   Coaches  
*   Tickets  
*   Partner with Huskies  
*   Donate  
*   Statistics  
    *   Season Stats  
    *   Season Stats (PDF)

*   Media Info  
    *   Record Book (PDF)  
    *   Quick Facts (PDF)

*   Pledge Per Three  
*    More +   
    *   News  
    *   Promotions  
    *   History  
    *   Facilities  
    *   Photos  
    *   Final Four Run  
    *   Recruit Questionnaire  
    *   Alumni Form  
    *   U-Dub

# Tina Langley - Women's Basketball
Skip Ad
Langley, Tina
*   Bowlin, Patrick  
*   Brown, Tasha  
*   Donnelly, Buddy  
*   Goodman, Aleah  
*   Jackson, Mark  
*   King, Latara   
*   Langley, Tina  
*   Wilson, Drew  
*   Wilson, Lauren
vs
**Stanford**  
Nov 20 (Fri)
7:00 PM
Buy From$15+
Tina Langley
*   Title: Head Coach
Skip Ad
Bio
Tina Langley has established herself as one of women’s college basketball’s premier program builders, earning a national reputation for transforming multiple programs into thriving championship contenders. A proven coach with multiple Final Four appearances and a track record of on- and off-the-court success, Langley has twice inherited teams near the bottom of their conferences and elevated them into nationally ranked programs. At Washington, she has restored the Huskies to recent national prominence, guiding the program to consecutive NCAA Tournament appearances and reestablishing its place among the nation’s Top 25.
Named the 12th head coach in Washington history on April 5, 2021, Langley enters the 2026–27 season after engineering one of the nation’s most impressive turnarounds. Since arriving on Montlake, she has led steady year-over-year progress, taking the Huskies from last place in the Pac-12 to a No. 24 final Associated Press ranking and the highest NET finish in program history at No. 22 in 2026. In just five seasons, she has transformed Washington into a consistent postseason contender with national momentum. Langley’s teams are known for their discipline, offensive efficiency and defensive toughness.
The foundation of that resurgence was laid quickly and has correlated with Langley’s relentless commitment to a values-based, people-first culture. Nothing speaks to this more prominently than the Huskies’ unprecedented continuity across their entire basketball operation.
</excerpt>
### Rank 5 of 68 — 0.60
<excerpt title="Tina Langley - Women's Basketball Coach - University of Washington ...">
# Tina Langley - Women's Basketball Coach - University of Washington Athletics
*   INSIDE

    *   Academic Services  
    *   Band/Spirit/Mascot  
    *   Boundless Futures  
    *   Camps  
    *   Charitable Donations  
    *   Compliance  
    *   Diversity, Equity & Inclusion  
    *   EADA/NCAA Reports  
    *   Emergency Resources  
    *   Employment  
    *   Facilities  
    *   Facility Rentals

    *   Media  
    *   Mental Health Resources  
    *   Monthly Calendar Presented by Toyota  
    *   Sponsorship Opportunities  
    *   Staff Central  
    *   Staff Directory  
    *   Sports Medicine  
    *   Student-Athlete Handbook  
    *   Sustainability  
    *   Title IX  
    *   UW Olympians & Paralympians  
    *   Husky National Championships
Skip Ad
*   TICKETS

    *   Ticket Information  
    *   Buy Tickets  
    *   Browse By Sport  
    *   UW Account Manager  
    *   UW Student Account Manager  
    *   Mobile Ticketing  
    *   Dawg Pack Student Tickets  
    *   Group Tickets  
    *   Dubs Club  
    *   Football Season Ticket Benefits  
    *   Meet Your Team  
    *   Husky Stadium 3D Virtual Seat Map  
    *   SeatGeek: Buy or Sell Football Tickets  
    *   Vet Tix  
    *   Subscribe to Husky E-News

    *   Gameday  
    *   Fan Code of Conduct  
    *   Security Screening & Bag Policy  
    *   Frequently Asked Questions  
    *   Sailgating  
    *   Transportation  
    *   UW Football Gameday Info  
    *   Lost & Found  
    *   Gameday at Alaska Airlines Arena  
    *   Promotions  
    *   The Zone at Husky Football  
    *   Montlake Memories Experiences  
    *   RevelXP Full-Service Tailgating  
    *   Gameday Map
Skip Ad
*   TYEE CLUB

    *   Tyee Club  
    *   About Tyee Club  
    *   Big W Club  
    *   Hall of Fame  
    *   Pledge For Purple

    *   Go BIG! for Washington  
    *   Premium Seating  
    *   The Tyee Difference  
    *   Contact Tyee Club
</excerpt>

## Search 9 — query: "Stefanie Dolson college South Dakota State women's basketball coach 2022-23"
### Rank 1 of 106 — 0.31 (passed on)
<excerpt title="Stefanie Dolson">
# Stefanie Dolson - USA Basketball
### Coach Academy
*   Frequently Asked Questions

# Stefanie Dolson - USA Basketball
### 3X Play
*   Rules & Standards

# Stefanie Dolson - USA Basketball
### On-Demand Courses
*   Frequently Asked Questions

# Stefanie Dolson - USA Basketball
### E-Learning
*   Frequently Asked Questions

# Stefanie Dolson - USA Basketball
### Coaching Resources
*   Skills and Drills  
        *   Youth Guidelines  
        *   Official USA Basketball Guidebook & E-Book

# Stefanie Dolson - USA Basketball
### Sign Up for Notifications
*   Safe Sport    ### Safe Sport

        ### Report an Incident

    
        ### MAAPP & Athlete and Participant Safety & Protection

    
        ### Resources

    
        ### Disciplinary Records

         
*   News  
*   Opens in a new window Foundation  
*   Opens in a new window Shop
Opens in a new window Open facebookOpens in a new window Open twitterOpens in a new window Open instagramOpens in a new window Open youtube
Open Search
Search Search Close Search
Calendar Events
Open Menu

# Stefanie Dolson
Position(s)**Center**
Height**6‐5**
Weight**210**
Age**34**
Hometown**Port Jervis, NY**
College**University of Connecticut**
*   Bio   
*   5-ON-5 STATS   
*   3X3 STATS
**_As of March 31, 2026_**

# Stefanie Dolson
## USA Basketball Notes
*   **Gold Medals:** 2020 Olympic 3x3, 2019 FIBA AmeriCup, 2011 FIBA U19 World Cup, 2010 FIBA Americas U18 Championship.  
*   **2026**  
    *   Participated in the April 2026 Women's National Team Training Camp in Phoenix.

*   **2022**  
    *   Named a finalist for the 2022 USA Women's National Team roster (9/11/22).  
    *   Invited to attend 2022 USA Basketball Women’s National Team training camp from Sept. 6-12 in Las Vegas.  
    *   Named to the 2022 USA World Cup Qualifying Team on Feb. 7, 2022.

*   **2021**  
    *   As a member of the USA's first U.S. Olympic 3x3 Basketball Team, averaged 5.4 points and 5.6 rebounds to help the USA to an 8-1 record and gold medal at the inaugural Olympic 3x3 competition. Among all tournament participants, was No. 2 in 1-point shooting percentage (.689).  
    *   As a member of the 2021 USA 3x3 National Team, averaged 5.7 points and 4.0 rebounds to help compile 6-0 record at the FIBA 3x3 Olympic Qualifying Tournament Graz, Austria. Most importantly, the USA’s semifinal win qualified the USA for the inaugural 3x3 Olympic event in Tokyo, and the USA finished No. 1 at the tournament based on FIBA’s rankings.  
    *   Inaugural 3x3 event was the 2021 Big Twelve International in Voiron, France, where the USA women finished 6-1 and in first place and Dolson was named to the all-tournament team.  
    *   Participated in the 2021 USA 3x3 Olympic Qualifying Team's March training camp in San Antonio.  
    *   Took part in the 2021 USA National Team's February training camp in South Carolina and March camp in San Antonio.
</excerpt>
### Rank 2 of 106 — 0.28
<excerpt title="Stefanie Dolson">
*   [McDonald's All-American](https://en.wikipedia.org/wiki/McDonald's_All-American_Game "McDonald's All-American Game") ([2010](https://en.wikipedia.org/wiki/2010_McDonald's_All-American_Girls_Game "2010 McDonald's All-American Girls Game"))  
**Stats at WNBA.com**  
**Stats at Basketball Reference**  
**Medals** Women's 3x3 basketball Representing [United States](https://en.wikipedia.org/wiki/United_States_women's_national_3x3_team "United States women's national 3x3 team") Olympic Games 2020 Tokyo[Team](https://en.wikipedia.org/wiki/Basketball_at_the_2020_Summer_Olympics_%E2%80%93_Women's_3x3_tournament "Basketball at the 2020 Summer Olympics – Women's 3x3 tournament") Representing United States Women's basketball [FIBA AmeriCup](https://en.wikipedia.org/wiki/FIBA_Women's_AmeriCup "FIBA Women's AmeriCup") [2019 Puerto Rico](https://en.wikipedia.org/wiki/2019_FIBA_Women's_AmeriCup "2019 FIBA Women's AmeriCup")[Team](https://en.wikipedia.org/wiki/United_States_women's_national_basketball_team "United States women's national basketball team") [FIBA Under-19 World Cup](https://en.wikipedia.org/wiki/FIBA_Under-19_Women's_Basketball_World_Cup "FIBA Under-19 Women's Basketball World Cup") 2011 Chile[Team](https://en.wikipedia.org/wiki/United_States_women's_national_under-19_basketball_team "United States women's national under-19 basketball team") [FIBA Under-18 Americas Championship](https://en.wikipedia.org/wiki/FIBA_Under-18_Women's_Americas_Championship "FIBA Under-18 Women's Americas Championship") 2010 United States[Team](https://en.wikipedia.org/wiki/United_States_women's_national_under-19_basketball_team "United States women's national under-19 basketball team")

**Stefanie Marie Dolson**[[2]](https://en.wikipedia.org/wiki/Stefanie_Dolson#cite_note-2) (born January 8, 1992) is an American professional basketball player for the Seattle Storm of the [Women's National Basketball Association](https://en.wikipedia.org/wiki/Women's_National_Basketball_Association "Women's National Basketball Association") (WNBA).[[3]](https://en.wikipedia.org/wiki/Stefanie_Dolson#cite_note-3) She was drafted sixth overall in the 2014 WNBA draft.[[4]](https://en.wikipedia.org/wiki/Stefanie_Dolson#cite_note-4) Dolson played center for the [UConn women's basketball team](https://en.wikipedia.org/wiki/UConn_Huskies_women's_basketball "UConn Huskies women's basketball") and won back-to-back national championships in [2013](https://en.wikipedia.org/wiki/2013_NCAA_Women's_Division_I_Basketball_Tournament "2013 NCAA Women's Division I Basketball Tournament") and [2014.](https://en.wikipedia.org/wiki/2014_NCAA_Women's_Division_I_Basketball_Tournament "2014 NCAA Women's Division I Basketball Tournament") She won a gold medal in [3x3 basketball](https://en.wikipedia.org/wiki/Basketball_at_the_2020_Summer_Olympics_%E2%80%93_Women's_3x3_tournament "Basketball at the 2020 Summer Olympics – Women's 3x3 tournament") at the 2020 Summer Olympics.[[5]](https://en.wikipedia.org/wiki/Stefanie_Dolson#cite_note-5)[[6]](https://en.wikipedia.org/wiki/Stefanie_Dolson#cite_note-:0-6)
</excerpt>
### Rank 3 of 106 — 0.28
<excerpt title="Stefanie Dolson">
**Stefanie Marie Dolson**[[2]](https://en.wikipedia.org/wiki/Stefanie_Dolson#cite_note-2) (born January 8, 1992) is an American professional basketball player for the Seattle Storm of the [Women's National Basketball Association](https://en.wikipedia.org/wiki/Women's_National_Basketball_Association "Women's National Basketball Association") (WNBA).[[3]](https://en.wikipedia.org/wiki/Stefanie_Dolson#cite_note-3) She was drafted sixth overall in the 2014 WNBA draft.[[4]](https://en.wikipedia.org/wiki/Stefanie_Dolson#cite_note-4) Dolson played center for the [UConn women's basketball team](https://en.wikipedia.org/wiki/UConn_Huskies_women's_basketball "UConn Huskies women's basketball") and won back-to-back national championships in [2013](https://en.wikipedia.org/wiki/2013_NCAA_Women's_Division_I_Basketball_Tournament "2013 NCAA Women's Division I Basketball Tournament") and [2014.](https://en.wikipedia.org/wiki/2014_NCAA_Women's_Division_I_Basketball_Tournament "2014 NCAA Women's Division I Basketball Tournament") She won a gold medal in [3x3 basketball](https://en.wikipedia.org/wiki/Basketball_at_the_2020_Summer_Olympics_%E2%80%93_Women's_3x3_tournament "Basketball at the 2020 Summer Olympics – Women's 3x3 tournament") at the 2020 Summer Olympics.[[5]](https://en.wikipedia.org/wiki/Stefanie_Dolson#cite_note-5)[[6]](https://en.wikipedia.org/wiki/Stefanie_Dolson#cite_note-:0-6)

Dolson played volleyball and basketball at Minisink Valley High School in Slate Hill, New York[[7]](https://en.wikipedia.org/wiki/Stefanie_Dolson#cite_note-:1-7) and was a member of the National Honor Society. During her junior year she averaged 18.9 points, 16.7 rebounds, 5.0 assists and 6.2 blocks. As a senior, she averaged 22.8 points, 17.6 rebounds, 5.6 assists and 5.2 blocks.
Dolson led Minisink Valley High School to four straight New York State Public High School Athletic Association Section 9 championship game appearances and finished her career at Minisink Valley with 1,951 points and 1,607 rebounds.[[7]](https://en.wikipedia.org/wiki/Stefanie_Dolson#cite_note-:1-7) She was a McDonald's High School All-American and participated in the All-Star game where she had 12 points and eight rebounds in the McDonald's All-American Game.[[8]](https://en.wikipedia.org/wiki/Stefanie_Dolson#cite_note-Dolson_bio-8)
As a freshman for UConn in 2010–11, Dolson averaged 10.2 points and 6.1 rebounds per game on the season. On March 8, Dolson recorded 24 points and 9 rebounds in a 73–64 win over Notre Dame at the Big East tournament title game. She was named to the BIG EAST All-Tournament Team. Dolson was subsequently named to the Big East Rookie Team alongside teammate Bria Hartley.[[9]](https://en.wikipedia.org/wiki/Stefanie_Dolson#cite_note-uconnprofile-9)
Dolson completed her sophomore season averaging 23.9 minutes, 10.4 points, 6.0 rebounds and 1.5 blocks per game. Dolson started her second year in strong form, however, her output slowed, and her scoring average dropped below ten points for her last eighteen regular season games. At the Final Four, Dolson came back strong, she scored 20 points in the overtime loss to Notre Dame.
</excerpt>
### Rank 4 of 106 — 0.28
<excerpt title="Stefanie Dolson - WNBA Wiki">
*   WNBA champion (2021)  
*   2× WNBA All-Star (2015, 2017)  
*   EuroLeague champion (2022)  
*   WNBA Commissioner's Cup Champion(2023)  
*   2× NCAA champion (2013, 2014)  
*   Senior CLASS Award (2014)  
*   AAC Defensive Player of the Year (2014)  
*   WBCA Defensive Player of the Year (2014)  
*   Second-team All-American – AP (2014)  
*   2x WBCA Coaches' All-American (2013, 2014)  
*   3x All-American – USBWA (2013–2015)  
*   First-team All-AAC (2014)  
*   Third-team All-American – AP (2013)  
*   First-team All-Big East (2013)  
*   Big East All-Freshman Team (2011)  
*   McDonald's All-American (2010)  
**Stats at NBA.com**  
**Stats at WNBA.com**  
**Stats at Basketball Reference**  
**Stats at Basketball Reference**
Women's Basketball Hall of Fame  
**Medals** Women's 3x3 basketball Representing [[File:{{{flag wikipedia:alias}}}|23x15px|border |alt=|link=]][[{{{wikipedia:alias}}} {{{wikipedia:altlink}}}|{{{wikipedia:alias}}}]] Olympic Games 2020 TokyoTeam Representing United States Women's Basketball FIBA AmeriCup 2019 Puerto RicoTeam FIBA Under-19 World Cup 2011 ChileTeam FIBA Under-18 Americas Championship 2010 United StatesTeam

**Stefanie Marie Dolson**[[2]](https://wnba.miraheze.org/wiki/Stefanie_Dolson#cite_note-2) (born January 8, 1992) is an American professional basketball player for the Washington Mystics of the Women's National Basketball Association (WNBA).[[3]](https://wnba.miraheze.org/wiki/Stefanie_Dolson#cite_note-3) She was drafted sixth overall in the 2014 WNBA draft.[[4]](https://wnba.miraheze.org/wiki/Stefanie_Dolson#cite_note-4) Dolson played center for the UConn women's basketball team and won back-to-back national championships in 2013 and 2014. She won a gold medal in 3x3 basketball at the 2020 Summer Olympics.[[5]](https://wnba.miraheze.org/wiki/Stefanie_Dolson#cite_note-5)[[6]](https://wnba.miraheze.org/wiki/Stefanie_Dolson#cite_note-:0-6)
Dolson played volleyball and basketball at Minisink Valley High School in Slate Hill, New York[[7]](https://wnba.miraheze.org/wiki/Stefanie_Dolson#cite_note-:1-7) and was a member of the National Honor Society. During her junior year she averaged 18.9 points, 16.7 rebounds, 5.0 assists and 6.2 blocks. As a senior, she averaged 22.8 points, 17.6 rebounds, 5.6 assists and 5.2 blocks.
Dolson led Minisink Valley High School to four straight New York State Public High School Athletic Association Section 9 championship game appearances and finished her career at Minisink Valley with 1,951 points and 1,607 rebounds.[[7]](https://wnba.miraheze.org/wiki/Stefanie_Dolson#cite_note-:1-7) She was a McDonald's High School All-American and participated in the All-Star game where she had 12 points and eight rebounds in the McDonald's All-American Game.[[8]](https://wnba.miraheze.org/wiki/Stefanie_Dolson#cite_note-Dolson_bio-8)
</excerpt>
### Rank 5 of 106 — 0.26
<excerpt title="Stefanie Dolson - WNBA Wiki">
Stefanie Dolson
Dolson with the Washington Mystics in 2024  
No. 31 – Washington Mystics  
PositionCenter  
LeagueWNBA  
Personal information  
Born January 8, 1992 (age 34)
Port Jervis, New York, U.S.  
Listed height 6 ft 4 in (1.93 m)  
Listed weight 235 lb (107 kg)  
Career information  
High schoolMinisink Valley
(Slate Hill, New York)  
CollegeUConn (2010–2014)  
WNBA draft2014: 1st round, 6th overall pick  
Drafted byWashington Mystics  
Playing career 2014–present  
Career history  
2014–2016Washington Mystics  
2014–2015WBC Spartak Moscow Region  
2015–2016Edirne Belediyesi Edirnespor BK[tr][[1]](https://wnba.miraheze.org/wiki/Stefanie_Dolson#cite_note-USA_Basketball-1)  
2016 Sichuan Whale  
2017–2021Chicago Sky  
2017–2018Dike Basket Napoli[it]  
2018–2019Henan Phoenix  
2019–2020Hebei Win Power  
2022–2023Sopron Basket  
2022–2023New York Liberty  
2023–2024ASVEL Féminin  
2024–present Washington Mystics  
2025–presentLaces BC  
Career highlights

*   WNBA champion (2021)  
*   2× WNBA All-Star (2015, 2017)  
*   EuroLeague champion (2022)  
*   WNBA Commissioner's Cup Champion(2023)  
*   2× NCAA champion (2013, 2014)  
*   Senior CLASS Award (2014)  
*   AAC Defensive Player of the Year (2014)  
*   WBCA Defensive Player of the Year (2014)  
*   Second-team All-American – AP (2014)  
*   2x WBCA Coaches' All-American (2013, 2014)  
*   3x All-American – USBWA (2013–2015)  
*   First-team All-AAC (2014)  
*   Third-team All-American – AP (2013)  
*   First-team All-Big East (2013)  
*   Big East All-Freshman Team (2011)  
*   McDonald's All-American (2010)  
**Stats at NBA.com**  
**Stats at WNBA.com**  
**Stats at Basketball Reference**  
**Stats at Basketball Reference**
Women's Basketball Hall of Fame  
**Medals** Women's 3x3 basketball Representing [[File:{{{flag wikipedia:alias}}}|23x15px|border |alt=|link=]][[{{{wikipedia:alias}}} {{{wikipedia:altlink}}}|{{{wikipedia:alias}}}]] Olympic Games 2020 TokyoTeam Representing United States Women's Basketball FIBA AmeriCup 2019 Puerto RicoTeam FIBA Under-19 World Cup 2011 ChileTeam FIBA Under-18 Americas Championship 2010 United StatesTeam
</excerpt>

## Search 10 — query: "2022-23 UConn women's basketball leading scorer points per game"
### Rank 1 of 357 — 0.69 (passed on)
<excerpt title="UConn Huskies women's basketball statistical leaders">
| 3 | Sue Bird | 231 | [2001–02](https://en.wikipedia.org/wiki/2001%E2%80%9302_Connecticut_Huskies_women's_basketball_team "2001–02 Connecticut Huskies women's basketball team") |  
| 4 | Crystal Dangerfield | 225 | [2018–19](https://en.wikipedia.org/wiki/2018%E2%80%9319_UConn_Huskies_women's_basketball_team "2018–19 UConn Huskies women's basketball team") |  
| 5 | Jennifer Rizzotti | 222 | [1995–96](https://en.wikipedia.org/wiki/1995%E2%80%9396_Connecticut_Huskies_women's_basketball_team "1995–96 Connecticut Huskies women's basketball team") |  
| 6 | Diana Taurasi | 208 | [2001–02](https://en.wikipedia.org/wiki/2001%E2%80%9302_Connecticut_Huskies_women's_basketball_team "2001–02 Connecticut Huskies women's basketball team") |  
| 7 | Moriah Jefferson | 204 | [2015–16](https://en.wikipedia.org/wiki/2015%E2%80%9316_UConn_Huskies_women's_basketball_team "2015–16 UConn Huskies women's basketball team") |  
| 8 | Maya Moore | 199 | [2008–09](https://en.wikipedia.org/wiki/2008%E2%80%9309_Connecticut_Huskies_women's_basketball_team "2008–09 Connecticut Huskies women's basketball team") |  

| 9 | Moriah Jefferson | 195 | [2013–14](https://en.wikipedia.org/wiki/2013%E2%80%9314_UConn_Huskies_women's_basketball_team "2013–14 UConn Huskies women's basketball team") |  
| 10 | Moriah Jefferson | 191 | [2014–15](https://en.wikipedia.org/wiki/2014%E2%80%9315_UConn_Huskies_women's_basketball_team "2014–15 UConn Huskies women's basketball team") |  
|  | Gabby Williams | 191 | [2017–18](https://en.wikipedia.org/wiki/2017%E2%80%9318_UConn_Huskies_women's_basketball_team "2017–18 UConn Huskies women's basketball team") |Single game| Rk | Player | Assists | Season | Opponent |  
| --- | --- | --- | --- | --- |  
| 1 | Nika Mühl | 15 | [2022–23](https://en.wikipedia.org/wiki/2022%E2%80%9323_UConn_Huskies_women's_basketball_team "2022–23 UConn Huskies women's basketball team") | NC State |  
| 2 | Paige Bueckers | 14 | [2020–21](https://en.wikipedia.org/wiki/2020%E2%80%9321_UConn_Huskies_women's_basketball_team "2020–21 UConn Huskies women's basketball team") | Butler |  
|  | Nika Mühl | 14 | [2022–23](https://en.wikipedia.org/wiki/2022%E2%80%9323_UConn_Huskies_women's_basketball_team "2022–23 UConn Huskies women's basketball team") | Tennessee |
</excerpt>
### Rank 2 of 357 — 0.69
<excerpt title="UConn women's basketball: Players, stats, records, historic moments from ...">
## UConn women's basketball all-time roster
*   Daphne Roper (!981-83): 7.1 points per game, 6.5 rebounds per game  
*   Missy Rose (1993-97): 1.5 points per game, 0.8 rebounds per game  
*   Pamela Rothfuss (1988-92): 0.6 points per game, 0.6 rebounds per game  
*   Gina Ryba (1975-77): 0.6 points per game, 1.8 rebounds per game  
*   Rashidat Sadiq (2004-05): 2.3 points per game, 1.2 rebounds per game  
*   Nykesga Sales (1994-98): 15.9 points per game, 5.0 rebounds per game  
*   Qadence Samuels (2023-25): 3.3 points per game, 1.8 rebounds per game  
*   Katie Lou Samuelson (2015-19): 16.7 points per game, 4.5 rebounds per game  
*   Paige Sauer (1996-00): 7.1 points per game, 4.2 rebounds per game  
*   Shannon Saunders (1988-92): 2.4 points per game, 1.6 rebounds per game  
*   Kelly Schumacher (1997-01): 5.4 points per game, 3.8 rebounds per game  
*   Lou Lopez Sénéchal (2022-23): 15.5 points per game, 3.1 rebounds per game  
*   Ashlynn Shade (2023-25): 9.4 points per game, 3.1 rebounds per game  
*   Linda Shannon (1974-75)  
*   Liz Sherwood (2003-04): 4.3 points per game, 1.8 rebounds per game  
*   Valerie Sirois (1976-79): 12.2 points per game, 3.2 rebounds per game
</excerpt>
### Rank 3 of 357 — 0.68
<excerpt title="2022–23 UConn Huskies women's basketball team">
The Huskies finished an injury-plagued previous season with a record of 30–6, losing the [championship game](https://en.wikipedia.org/wiki/2022_NCAA_Division_I_women's_basketball_championship_game "2022 NCAA Division I women's basketball championship game") of the [2022 NCAA women's basketball tournament](https://en.wikipedia.org/wiki/2022_NCAA_Division_I_women's_basketball_tournament "2022 NCAA Division I women's basketball tournament") to South Carolina. Three graduates from that squad were selected in the 2022 WNBA draft, but with six returning starters including the backcourt of Paige Bueckers, Azzi Fudd, and Nika Mühl, with forwards Dorka Juhász, Aaliyah Edwards, and Caroline Ducharme, UConn was expected to win the much improved Big East again. Bueckers tore an ACL in a pickup game before fall workouts,[[1]](https://en.wikipedia.org/wiki/2022%E2%80%9323_UConn_Huskies_women's_basketball_team#cite_note-2) and five-star recruit Ice Brady suffered a tendon dislocation during an early practice; both players underwent season ending surgeries and sat on the bench all season.[[2]](https://en.wikipedia.org/wiki/2022%E2%80%9323_UConn_Huskies_women's_basketball_team#cite_note-3)

Starting the season already down two players, UConn played surprisingly well against early opponents, with strong wins against #3 Texas, #10 NC State, and #9 Iowa in the first weeks. In the Texas game, Juhász injured a thumb and was sidelined for several weeks. Aubrey Griffin, who had redshirted the previous season because of injury, and Lou Lopez Sénéchal, a graduate transfer shooting guard from Fairfield University, got some starts and immediately impacted the team with their durability and shooting proficiency. Fudd began the season as a leading scorer, with Mühl leading the country in assists per game, and Edwards seemingly unstoppable in the paint. Fudd was injured in the loss to #7 Notre Dame, and by the end of December the Huskies only had seven players healthy, even after Juhász's return. On January 8, UConn's contest against DePaul was postponed because the Huskies only had six players able to play.[[3]](https://en.wikipedia.org/wiki/2022%E2%80%9323_UConn_Huskies_women's_basketball_team#cite_note-4)
</excerpt>
### Rank 4 of 357 — 0.67
<excerpt title="UConn women's basketball: Players, stats, records, historic moments from ...">
## UConn women's basketball all-time roster
*   Catherine Bochain (1979-83): 14.2 points per game, 4.4 rebounds per game  
*   Tonya Boone (1989-94): 4.5 points per game, 2.2 rebounds per game  
*   Catherine Borman (1982-83): 0.3 points per game, 0.3 rebounds per game  
*   Rosemary Borsuk (1975-78): 6.8 points per game, 9.0 rebounds per game  
*   Ice Brady (2022-25): 4.1 points per game, 3.1 rebounds per game  
*   Patricia Bresser (1976-78): 6.8 points per game, 2.5 rebounds per game  
*   Jill Brumbaugh (1984-88): 6.6 points per game, 1.9 rebounds per game  
*   Heather Buck (2009-13): 1.7 points per game, 1.9 rebounds per game  
*   Paige Bueckers (2020-25): 19.9 points per game, 4.7 rebounds per game  
*   Natalie Butler (2015-17): 5.5 points per game, 4.6 rebounds per game  
*   Batouly Camara (2017-19) 1.4 points per game, 1.2 rebounds per game  
*   Barbara Carter (1986-88): 1.4 points per game, 0.3 rebounds per game  
*   Swin Cash (1998-02): 11.9 points per game, 6.8 rebounds per game  
*   Kathleen Cermola (1980-84): 6.6 points per game, 2.0 rebounds per game  
*   Tina Charles (2006-10): 15.4 points per game, 9.0 rebounds per game  
*   Autumn Chassion (2020-21): 1.0 points per game, 0.3 rebounds per game
</excerpt>
### Rank 5 of 357 — 0.67
<excerpt title="UConn Huskies women's basketball statistical leaders">
| 10 | Pam Webber | 546 | [1991–92](https://en.wikipedia.org/wiki/1991%E2%80%9392_Connecticut_Huskies_women's_basketball_team?action=edit&redlink=1 "1991–92 Connecticut Huskies women's basketball team (page does not exist)")[1992–93](https://en.wikipedia.org/wiki/1992%E2%80%9393_Connecticut_Huskies_women's_basketball_team?action=edit&redlink=1 "1992–93 Connecticut Huskies women's basketball team (page does not exist)")[1993–94](https://en.wikipedia.org/wiki/1993%E2%80%9394_Connecticut_Huskies_women's_basketball_team?action=edit&redlink=1 "1993–94 Connecticut Huskies women's basketball team (page does not exist)")[1994–95](https://en.wikipedia.org/wiki/1994%E2%80%9395_Connecticut_Huskies_women's_basketball_team "1994–95 Connecticut Huskies women's basketball team") |Season| Rk | Player | Assists | Season |  
| --- | --- | --- | --- |  
| 1 | Nika Mühl | 284 | [2022–23](https://en.wikipedia.org/wiki/2022%E2%80%9323_UConn_Huskies_women's_basketball_team "2022–23 UConn Huskies women's basketball team") |  
| 2 | Nika Mühl | 253 | [2023–24](https://en.wikipedia.org/wiki/2023%E2%80%9324_UConn_Huskies_women's_basketball_team "2023–24 UConn Huskies women's basketball team") |  

| 3 | Sue Bird | 231 | [2001–02](https://en.wikipedia.org/wiki/2001%E2%80%9302_Connecticut_Huskies_women's_basketball_team "2001–02 Connecticut Huskies women's basketball team") |  
| 4 | Crystal Dangerfield | 225 | [2018–19](https://en.wikipedia.org/wiki/2018%E2%80%9319_UConn_Huskies_women's_basketball_team "2018–19 UConn Huskies women's basketball team") |  
| 5 | Jennifer Rizzotti | 222 | [1995–96](https://en.wikipedia.org/wiki/1995%E2%80%9396_Connecticut_Huskies_women's_basketball_team "1995–96 Connecticut Huskies women's basketball team") |  
| 6 | Diana Taurasi | 208 | [2001–02](https://en.wikipedia.org/wiki/2001%E2%80%9302_Connecticut_Huskies_women's_basketball_team "2001–02 Connecticut Huskies women's basketball team") |  
| 7 | Moriah Jefferson | 204 | [2015–16](https://en.wikipedia.org/wiki/2015%E2%80%9316_UConn_Huskies_women's_basketball_team "2015–16 UConn Huskies women's basketball team") |  
| 8 | Maya Moore | 199 | [2008–09](https://en.wikipedia.org/wiki/2008%E2%80%9309_Connecticut_Huskies_women's_basketball_team "2008–09 Connecticut Huskies women's basketball team") |
</excerpt>

# Example 2
## Question
Referencing Statistics Canada (table 23-10-0253-01), which Canadian airports reported over 500,000 passengers in 2020 were also eligible for airport relief funding or the Airport Critical Infrastructure Program in 2021, as verified by Transport Canada?

## Expected answer
Halifax Stanfield Airport, Edmonton Airport, Winnipeg James Armstrong Richardson Airport, Ottawa Macdonald-Cartier Airport, Toronto (Lester B) Pearson Airport, Montréal (Pierre Elliott Trudeau) Airport, Calgary Airport, Vancouver Airport

## Grade 0.78

## Search 1 — query: "Statistics Canada table 23-10-0253-01 2020 passenger traffic Canada airports"
### Rank 1 of 65 — 0.64 (passed on)
<excerpt title="List of the busiest airports in Canada">
20	Kelowna International Airport	Kelowna	75,581	3 	  
21	Billy Bishop Toronto City Airport	Toronto	73,469	1 	  
22	Edmonton International Airport	Edmonton Metropolitan Region	71,316	3 	  
23	Langley Regional Airport	Langley Township	71,225	1 	  
24	Greater Moncton Roméo LeBlanc International Airport	Moncton	69,855	9 	  
25	Sault Ste. Marie Airport	Sault Ste. Marie	67,725	5 	  
26	Montréal–Mirabel International Airport	Greater Montreal	66,572	1 	  
27	Edmonton/Villeneuve Airport	Edmonton	65,450	2 	  
28	Ottawa Macdonald–Cartier International Airport	Ottawa	64,797		  
29	Fredericton International Airport	Fredericton	57,697	15 	  
30	Regina International Airport	Regina	44,433	1 	  
31	Halifax Stanfield International Airport	Halifax	32,315		  
32	Vancouver Harbour Flight Centre	Metro Vancouver	32,204		  
2020edit
Air traffic decreased greatly in this year due to the COVID-19 pandemic.

Canada's busiest airports by passenger trafficedit  
Rank	Rank  
change	Airport	Serves	Total  
passengers	Annual  
change  
1		Toronto Pearson International Airport	Greater Toronto Area	13,307,077[118]	73.6%   
2		Vancouver International Airport	Metro Vancouver	7,300,287[119]	72.3%   
3	1	Calgary International Airport	Calgary Region	5,675,483[120]	68.4%   
4	1	Montréal–Trudeau International Airport	Greater Montreal	5,436,998[121]	73.2%   
5		Edmonton International Airport	Edmonton Metropolitan Region	2,628,891[122]	67.7%   
6		Ottawa Macdonald–Cartier International Airport	National Capital Region	1,363,512[123]	73.3%   
7		Winnipeg Richardson International Airport	Winnipeg Capital Region	1,299,225[124]	71.0%   
8		Halifax Stanfield International Airport	Halifax	995,426[125]	76.2%   
9	1	Kelowna International Airport	Kelowna/Okanagan Valley	737,447[126]	63.7%   
10	1	Victoria International Airport	Greater Victoria	574,874[127]	70.1%   
11	1	Québec City Jean Lesage International Airport	Quebec City	535,111[128]	70.1%   
12	1	Saskatoon John G. Diefenbaker International Airport	Saskatoon	461,900[129]	69.0%   
13	4	Billy Bishop Toronto City Airport	Toronto	389,000[130]	86.0%
</excerpt>
### Rank 2 of 65 — 0.60
<excerpt title="List of the busiest airports in Canada">
10	Kelowna International Airport	Kelowna	1,818,926	92.4%	99,846	5.1%	50,241	2.6%  
11	Victoria International Airport	Victoria	1,594,847	86.4%	n/aD	 	n/aD	   
12	Québec City Jean Lesage International Airport	Quebec City	1,164,377	67.6%	217,983	12.7%	339,163	29.1%  
13	Saskatoon John G. Diefenbaker International Airport	Saskatoon	1,299,529	88.1%	n/aD	 	n/aD	   
14	St. John's International Airport	St. John's	1,385,675	96.6%	n/aD	 	n/aD	   
15	Regina International Airport	Regina	1,061,654	91.2%	n/aD	 	n/aD	   
16	Thunder Bay International Airport	Thunder Bay	707,042	95.5%	n/aD	 	n/aD	   
17	Abbotsford International Airport	Abbotsford/Fraser Valley	n/aD	 	n/aD	 	n/aD	   
18	John C. Munro Hamilton International Airport	Hamilton	n/aD	 	n/aD	 	n/aD	   
19	London International Airport	London	627,960	93.6%	n/aD	 	n/aD	   
20	Greater Moncton International Airport	Moncton	608,982	92.6%	n/aD	 	n/aD	   
Notesedit  
A.^Statistics Canada figures.  
B.^Airport operating authority figures.  
C.^Estimated from graph.  
D.^Numbers are "suppressed to meet the confidentiality requirements of the Statistics Act".[151]  
E.^Estimated figure.  
Referencesedit
</excerpt>
### Rank 3 of 65 — 0.57
<excerpt title="List of the busiest airports in Canada">
Canada's busiest airports by passenger trafficedit  
Rank	Rank  
change	Airport	Serves	Total  
passengers	Annual  
change  
1		Toronto Pearson International Airport	Greater Toronto Area	13,307,077[118]	73.6%   
2		Vancouver International Airport	Metro Vancouver	7,300,287[119]	72.3%   
3	1	Calgary International Airport	Calgary Region	5,675,483[120]	68.4%   
4	1	Montréal–Trudeau International Airport	Greater Montreal	5,436,998[121]	73.2%   
5		Edmonton International Airport	Edmonton Metropolitan Region	2,628,891[122]	67.7%   
6		Ottawa Macdonald–Cartier International Airport	National Capital Region	1,363,512[123]	73.3%   
7		Winnipeg Richardson International Airport	Winnipeg Capital Region	1,299,225[124]	71.0%   
8		Halifax Stanfield International Airport	Halifax	995,426[125]	76.2%   
9	1	Kelowna International Airport	Kelowna/Okanagan Valley	737,447[126]	63.7%   
10	1	Victoria International Airport	Greater Victoria	574,874[127]	70.1%   
11	1	Québec City Jean Lesage International Airport	Quebec City	535,111[128]	70.1%   
12	1	Saskatoon John G. Diefenbaker International Airport	Saskatoon	461,900[129]	69.0%   
13	4	Billy Bishop Toronto City Airport	Toronto	389,000[130]	86.0%
</excerpt>
### Rank 4 of 65 — 0.55
<excerpt title="List of the busiest airports in Canada">
11		Victoria International Airport	Greater Victoria	1,740,107[58]	16.8%   
12		Québec City Jean Lesage International Airport	Quebec City Metropolitan Region	1,688,736[59]	43.8%   
13	2	Saskatoon John G. Diefenbaker International Airport	Saskatoon Metropolitan Area	1,277,863[13]	34.2%   
14		Abbotsford International Airport	Abbotsford/Fraser Valley	1,275,484[60]	28.5%   
15	2	St. John's International Airport	St. John's Metropolitan Area	1,260,000[61]	17.4%   
16		Regina International Airport	Regina	981,845[62]	28.5%   
17		John C. Munro Hamilton International Airport	Greater Toronto and Hamilton Area	820,011[63]	27.0%   
18		Thunder Bay International Airport	Thunder Bay	714,070[64]	18.7%   
19		Greater Moncton Roméo LeBlanc International Airport	Greater Moncton	600,121[65]	28.0%   
20		Yellowknife Airport	Yellowknife	511,864[66]	14.6%   
21		Region of Waterloo International Airport	Waterloo Region	445,312[67]	18.4%   
22		Prince George Airport	Prince George	417,848[68]	14.6%   
23		Charlottetown Airport	Charlottetown	402,686[69]	17.9%   
24		Nanaimo Airport	Nanaimo	377,454[70]	11.7%  
25		Comox Valley Airport	Comox	371,989[71]	15.0%
</excerpt>
### Rank 5 of 65 — 0.54
<excerpt title="List of the busiest airports in Canada">
9		Kelowna International Airport	Kelowna/Okanagan Valley	829,804[9]	12.5%   
10		Victoria International Airport	Greater Victoria	673,478[84]	17.2%   
11	7	Abbotsford International Airport	Abbotsford/Fraser Valley	503,955[106]	59.7%   
12	3	St. John's International Airport	St. John's	478,124[107]	31%   
13	1	Saskatoon John G. Diefenbaker International Airport	Saskatoon	439,927[108]	4.8%   
14		Regina International Airport	Regina	355,490[109]	4.0%   
15	4	Québec City Jean Lesage International Airport	Quebec City	353,203[110]	34%   
16	2	Thunder Bay International Airport	Thunder Bay	316,025[90]	7.9%   
17	4	Billy Bishop Toronto City Airport	Toronto	282,000[111]	27.5%   
18	2	John C. Munro Hamilton International Airport	Hamilton	250,019[112]	24.0%   
19		Fort McMurray International Airport	Fort McMurray	228,627[25]	0.3%   
20	1	Prince George Airport	Prince George	201,506[113]	13.8%   
21	1	Nanaimo Airport	Nanaimo	193,425[95]	11.0%   
22		Greater Moncton Roméo LeBlanc International Airport	Greater Moncton	177,040[114]	2.1%   
23	7	Region of Waterloo International Airport	Waterloo Region	171,828[115]	245%
</excerpt>

## Search 2 — query: "Transport Canada airport relief funding 2021 eligibility list"
### Rank 1 of 68 — 0.85 (passed on)
<excerpt title="Airport Relief Fund">
# Airport Relief Fund
From: Transport Canada

# Airport Relief Fund
## Backgrounder
The Airport Relief Fund is a new contribution funding program to provide $64.8 million in financial relief to Canada’s airports that are struggling with the financial impact of reduced air travel due to the COVID‑19 pandemic. The Airport Relief Fund will provide immediate financial assistance to targeted eligible airports to help maintain operations and mitigate the risk of airport insolvency.
May 2021
The Airport Relief Fund is a new contribution funding program to provide $64.8 million in financial relief to Canada’s airports that are struggling with the financial impact of reduced air travel due to the COVID‑19 pandemic. The Airport Relief Fund will provide immediate financial assistance to targeted eligible airports to help maintain operations and mitigate the risk of airport insolvency.
The following airports have been identified as eligible for funding from the Airport Relief Fund:
*   Abbotsford International Airport   
*   Kelowna International Airport  
*   Prince George Airport  
*   Victoria International Airport  
*   Edmonton International Airport  
*   Fort McMurray International Airport  
*   Saskatoon John G. Diefenbaker International Airport  
*   Regina International Airport  
*   Winnipeg James Armstrong Richardson International Airport  
*   Billy Bishop Toronto City Airport  
*   John C. Munro Hamilton International Airport  
*   London International Airport  
*   Ottawa Macdonald-Cartier International Airport  
*   Thunder Bay International Airport  
*   Québec City Jean-Lesage International Airport  
*   Fredericton International Airport  
*   Greater Moncton Roméo LeBlanc International Airport  
*   Saint John Airport  
*   Halifax Stanfield International Airport  
*   Charlottetown Airport  
*   Gander International Airport  
*   St. John's International Airport
The allocation of funding will consider each airport’s regional importance and strategic significance within Canada’s system of airports. The amount of funding will be calculated using a tiered approach, based on 2019 revenues, as follows:

# Airport Relief Fund
## Backgrounder
*   Airports with 2019 revenues between $100 million and $250 million will receive a base amount of $5 million and an additional allocation of funding equivalent to 0.5 per cent of the airport’s 2019 revenue.  
*   Airports with 2019 revenues between $25 million and $100 million will receive a base amount of $1.5 million and an additional allocation of funding equivalent to 4 per cent of the airport’s 2019 revenue.  
*   Airports with 2019 revenues between $10 million and $25 million will receive a base amount of $1 million and an additional allocation of funding equivalent to 4.5 per cent of the airport’s 2019 revenue.  
*   Airports with 2019 revenues less than $10 million will receive a base amount of $0.5 million and an additional allocation of funding equivalent to 8.5 per cent of the airport’s 2019 revenue.
More information on the Airport Relief Fund, including program eligibility requirements and funding application process, can be found here. Airport Relief Fund
Search for related information by keyword:Air transport | Transport Canada | Canada | Transport and infrastructure | Coronavirus (COVID-19) | general public | backgrounders

# Airport Relief Fund
## Page details
2021-05-13

# Airport Relief Fund
## About this site
### Government of Canada
*   All contacts  
*   Departments and agencies  
*   About government
</excerpt>
### Rank 2 of 68 — 0.43
<excerpt title="Funding programs - Transports Canada">
# Funding programs
## List of funding programs
Displaying 1 - 25 of 33
Filter
Apply

# Funding programs
## List of funding programs
| Mode | Title | Description |  
| --- | --- | --- |  
| Aviation | Airport Critical Infrastructure Program | Funding to help Canada’s large airports make critical investments in safety, security or transit infrastructure. |  
| Aviation | Airport Relief Fund | Fund provides contribution funding to assist targeted airport authorities manage the financial impact of reduced air travel as a result of the impact of the COVID-19 pandemic. |  
| Aviation | Airports Capital Assistance Program | Funds regional airports' projects to improve safety, protect airport assets and reduce operating costs. |  
| Aviation | Airports Operations and Maintenance Subsidy Program | Helps fund remote airports, ensuring year-round, safe transportation links to isolated communities. |  
| Aviation | Commemoration Fund for the Victims of the Ethiopian Airlines Flight 302 Tragedy | Funding for student scholarships and commemorative projects in memory of the Canadian Victims of the Ethiopian Airlines Flight 302 Tragedy. |  
| Rail | Program to Enhance Rail Safety Engagement | Funding to increase capacity for Indigenous and local communities, organizations, and entities to engage with Transport Canada regarding the rail transportation system. |  
| Rail | Rail Climate Change Adaptation Program | Funding to help Canada's rail sector research, develop, and implement innovative technologies, tools, and approaches to reduce complex risks climate change and extreme weather. |  
| Rail | Rail Safety Improvement Program | Transport Canada’s Rail Safety Improvement Program provides funding to projects that increase safety at high-risk grade crossings and along rail lines. |  
| Marine | Abandoned Boats Program | Funds projects that remove abandoned and wrecked small boats or that promote boat recycling and environmental awareness. |  
| Marine | Ballast Water Innovation Program | The Ballast Water Innovation Program (BWIP) helps industry address technical and operational challenges with a Ballast Water Management System (BWMS) in the Great Lakes and St. Lawrence River (GLSLR) region, whose waters are cold, fresh, and mixed with sediment. |  
| Marine | Boating Safety Contribution Program | Funds projects that promote safer boating or that study ways to change boating behaviours. |  
| Marine | Community Participation Funding Program | Funds Indigenous groups and members of local communities who wish to participate in planning changes to marine transportation in Canada. |  
| Marine | Ferry Services Contribution Program | Helps fund inter-provincial ferry services in Atlantic Canada and Eastern Quebec. |
</excerpt>
### Rank 3 of 68 — 0.42
<excerpt title="Funding programs - Transports Canada">
# Funding programs
## List of funding programs
| Mode | Title | Description |  
| --- | --- | --- |  
| Aviation | Airport Critical Infrastructure Program | Funding to help Canada’s large airports make critical investments in safety, security or transit infrastructure. |  
| Aviation | Airport Relief Fund | Fund provides contribution funding to assist targeted airport authorities manage the financial impact of reduced air travel as a result of the impact of the COVID-19 pandemic. |  
| Aviation | Airports Capital Assistance Program | Funds regional airports' projects to improve safety, protect airport assets and reduce operating costs. |  
| Aviation | Airports Operations and Maintenance Subsidy Program | Helps fund remote airports, ensuring year-round, safe transportation links to isolated communities. |  
| Aviation | Commemoration Fund for the Victims of the Ethiopian Airlines Flight 302 Tragedy | Funding for student scholarships and commemorative projects in memory of the Canadian Victims of the Ethiopian Airlines Flight 302 Tragedy. |  
| Rail | Program to Enhance Rail Safety Engagement | Funding to increase capacity for Indigenous and local communities, organizations, and entities to engage with Transport Canada regarding the rail transportation system. |  
| Rail | Rail Climate Change Adaptation Program | Funding to help Canada's rail sector research, develop, and implement innovative technologies, tools, and approaches to reduce complex risks climate change and extreme weather. |  
| Rail | Rail Safety Improvement Program | Transport Canada’s Rail Safety Improvement Program provides funding to projects that increase safety at high-risk grade crossings and along rail lines. |  
| Marine | Abandoned Boats Program | Funds projects that remove abandoned and wrecked small boats or that promote boat recycling and environmental awareness. |  
| Marine | Ballast Water Innovation Program | The Ballast Water Innovation Program (BWIP) helps industry address technical and operational challenges with a Ballast Water Management System (BWMS) in the Great Lakes and St. Lawrence River (GLSLR) region, whose waters are cold, fresh, and mixed with sediment. |  
| Marine | Boating Safety Contribution Program | Funds projects that promote safer boating or that study ways to change boating behaviours. |  
| Marine | Community Participation Funding Program | Funds Indigenous groups and members of local communities who wish to participate in planning changes to marine transportation in Canada. |  
| Marine | Ferry Services Contribution Program | Helps fund inter-provincial ferry services in Atlantic Canada and Eastern Quebec. |
</excerpt>
### Rank 4 of 68 — 0.41
<excerpt title="National air sector support programs - Transports Canada">
**Location**: National
**Summary of Issue/Background**
*   The air sector has remained one of the hardest-hit industries since the beginning of the COVID-19 pandemic. To support Canada’s airports and airlines through the disruption, Transport Canada has put in place measures to help mitigate the financial impact caused by the pandemic, enabling a strong travel restart and recovery. 

*   The **Airports Capital Assistance Program** (ACAP) is a contribution funding program that launched in 1995 and provides federal funds to help eligible airports finance capital projects that will maintain and improve safety. 

*   As a result of COVID-19, ACAP received a received a one-time top-up funding of $186 million over two years. This financial support will help ensure that Canada’s smaller airports can immediately carry out required safety improvements despite revenue losses due to the pandemic.

*   **Airport Critical Infrastructure Program** (ACIP)is a contribution funding program that is providing financial support to large airports that are making critical capital investments related to safety, security or connectivity to mass transit. 

*   The fund, launched in May 2021, is intended to provide funding to ensure that essential infrastructure projects are not cancelled or delayed due to the pandemic. 

*   To support the operations of Canada’s airports during the COVID-19 pandemic**, rent relief**was provided to the 21 National Airports System airport authorities and the operator of Toronto Billy Bishop Airport, Ports Toronto, that pay rent to the federal government. Rent was deferred or waived for a set period depending on the size of the airport. 

*   The **Airport Relief Fund** is a contribution funding program to provide immediate financial relief to certain Canadian airports that are struggling with the financial impact of reduced air travel due to the COVID-19 pandemic. As of July 2021, twenty-two agreements have been signed, awarding all the funding. 

*   The **Remote Air Services Program**(RASP) was created in September 2020 to provide contribution funding through bilateral agreements with Provinces, Territories and regional indigenous governments to support continued access to essential air services to remote communities. 

*   In addition, Finance Canada, with support from Transport Canada and Innovation, Science and Economic Development Canada, has negotiated agreements with several large air carriers to provide them with liquidity to enable their restart and recovery in return for a number of binding commitments, including on passenger refunds and restoration of service to Canadian communities.
**Messages**

*   The Government of Canada is committed to helping airports mitigate the financial impact of the COVID-19 pandemic through several targeted support measures that are designed to provide much-needed support to airports. 

*   Canadian airports require support for infrastructure projects to maintain safety, security, and connectivity for travelers, airport workers, and surrounding communities. 

*   The Government of Canada looks forward to continue working with our provincial, territorial and Indigenous counterparts to support air carriers providing service to remote communities.
</excerpt>
### Rank 5 of 68 — 0.32
<excerpt title="Minister of Transport introduces new funding programs to support ...">
# Minister of Transport introduces new funding programs to support Canada’s airports
From: Transport Canada

# Minister of Transport introduces new funding programs to support Canada’s airports
## News release
The global COVID-19 pandemic has had an unprecedented impact on the air sector in Canada.
May 11, 2021  Ottawa Transport Canada
The global COVID-19 pandemic has had an unprecedented impact on the air sector in Canada. Airports have been significantly affected, experiencing major decreases in traffic over the past 15 months. Despite these consequences, airports have played a crucial role since the start of the pandemic by continuing to provide essential air services, including traveling to medical appointments, air ambulance services, community resupply, getting goods to market, search and rescue operations, and forest fire response.
Today, the Minister of Transport, the Honourable Omar Alghabra, launched two new contribution funding programs to help Canada’s airports recover from the effects of the COVID-19 pandemic:
*   **The Airport Critical Infrastructure Program (ACIP)** is a new program providing close to $490 million to financially assist Canada’s larger airports with investments in critical infrastructure-related to safety, security or connectivity;  
*   **The Airport Relief Fund (ARF)** is a new program providing almost $65 million in financial relief to targeted Canadian airports to help maintain operations.
In addition to launching these two new funding programs, the Minister announced that Transport Canada’s Airports Capital Assistance Program (ACAP) is receiving a funding top-up of $186 million over two years. The ACAP is an existing contribution funding program which provides financial assistance to Canada’s local and regional airports for safety-related infrastructure projects and equipment purchases.

# Minister of Transport introduces new funding programs to support Canada’s airports
## Quotes
> “Canada’s airports are major contributors to our country’s economy, and play a key role in sustaining the social and economic well-being of our communities, and our local airport workers. These programs will help ensure that, as Canada works towards recovery and travel restart post pandemic, our airports remain viable and continue to provide Canadians with safe, reliable and efficient travel options, while creating and maintaining good paying jobs in the airport sector.”  
>   
>   
>   
> _The Honourable Omar Alghabra  
>   
>  Minister of Transport_
</excerpt>

## Search 3 — query: "Airport Critical Infrastructure Program eligibility Transport Canada 2021 airports"
### Rank 1 of 53 — 0.76 (passed on)
<excerpt title="Lessons Learned Review of the Airport Critical Infrastructure Program">
## Introduction
### COVID-19 and its impact on air travel
Initial disruptions to air travel began in January 2020, driven by emerging health concerns and precautionary measures. Canada’s early response included issuing travel advisories and preparing quarantine protocols.
By March 2020, the aviation sector faced a global crisis as countries imposed border closures and travel bans. Airlines worldwide cancelled large volumes of flights and passenger demand collapsed.Footnote 1 Canada closed its borders to most foreign nationals on March 16, 2020, followed by a Canada-U.S. border closure for non-essential travel on March 21, 2020. All international flights coming into Canada were redirected to four airports (i.e., Toronto Pearson International Airport, Vancouver International Airport, Calgary International Airport, and Montréal–Trudeau International Airport).
The most severe and widespread impacts on air travel occurred between March and May 2020. By May, global flight activity had declined by approximately 80% compared to the same period in 2019.Footnote 2 Canada’s international arrivals dropped by over 90%, with strict entry requirements including testing and quarantine.Footnote 3 These measures resulted in an unprecedented contraction in air traffic, severely affecting airport operations and revenues. Passenger traffic across all Canadian airports is displayed in Figure 1.
**Figure 1. Total passengers enplaned and deplaned 2019 to 2024 at all Canadian airports**

## Introduction
### Program background
ACIP is a contribution funding program that was introduced during the COVID-19 pandemic when Canada’s airports were suffering from dramatic decreases in passengers and revenues. It was designed in 2020 and launched in May 2021 to help Canada’s larger airports (525,000+ passengers per year) continue to make critical investments in safety, security, connectivity to mass transit, and biosecurity. Because of declining revenues during the pandemic, infrastructure projects at Canadian airports were at risk of being delayed or cancelled, which would have postponed their potential benefits or permanently reduced an airport’s ability to deliver efficient services to Canadians. For example, opting to temporarily patch a runway or taxiway instead of completing a comprehensive repaving project would be more costly in the long run, with the airport authority having to pay twice – once for the temporary repair and again for the comprehensive rehabilitation. Further, given the drastic decrease in flight activity and the pre-existing construction for some mass transit projects (like Ottawa’s Light Rail Transit expansion) the COVID-19 pandemic provided an ideal window of opportunity to complete significant infrastructure projects.
The duration of the program was initially from fiscal year (FY) 2021-22 to 2025-26 but was extended to 2027-28, in October 2025, to allow time for the completion of major projects that were delayed due to supply chain issues and construction logistics.
ACIP’s calls for proposals opened on May 11, 2021, for the safety, security, and mass transit streams, and on August 13, 2021, for biosecurity. Money for biosecurity was announced in Budget 2021 (in April 2021), after ACIP had been designed and approved. Project proposals and expressions of interest were accepted starting on May 24, 2021. Specifically, applicants were invited to voluntarily submit an EOI to ensure eligibility and for feedback on their project proposal. Following that, applicants submitted a CPP for a funding decision. In practice, some applicants bypassed the EOI and proceeded directly to submitting a CPP.
TC offered information sessions to eligible airports for each application callout. They also organized regular meetings with eligible recipients and encouraged them to contact the ACIP team with questions at any time.
</excerpt>
### Rank 2 of 53 — 0.75
<excerpt title="Lessons Learned Review of the Airport Critical Infrastructure Program">
## Introduction
### Program design and delivery
Overall, ACIP funding was intended to enable investments in critical infrastructure projects that would continue through the pandemic and would support the recovery of the air sector through:
*   Uninterrupted implementation of projects to ensure continued safety and security, including compliance with standards and regulatory requirements  
*   Helping airports mitigate the financial impact of the pandemic  
*   Helping airports to avoid increasing passenger fees to pay for infrastructure projects  
*   Stimulating economic activity through the jobs that ACIP projects would provide  
*   Enabling airports to protect air travelers from the transmission of COVID-19 and help regain Canadians’ confidence in the safety of air travel.
The main Offices of Primary Interest (OPIs) at TC responsible for the design of ACIP were Transportation Infrastructure Programs and Air Policy. Program delivery was the responsibility of Transportation Infrastructure Programs. The number of full-time equivalents (FTE) within Transportation Infrastructure Programs that worked on ACIP decreased over time, with a high of 16 in 2021 to a low of 5 in 2024.
ACIP funds up to 50% of the total project cost for ACIP-approved infrastructure projects across four key streams. These include:
1.   safety, which encompasses initiatives such as runway rehabilitation, lighting improvements, and the acquisition of firefighting equipment  
2.   security, which involves projects like relocating screening or border checkpoints and enhancing cybersecurity infrastructure  
3.   mass transit, which supports the development of transit stations and other transportation infrastructure connected to airports  
4.   biosecurity, which focuses on infrastructure for COVID-19 testing and screening
Given the immediate need for funding due to the cash flow of some recipient airports, ACIP was designed to be flexible in how it allocated funds. TC could front-load contributions so that recipients could access a larger proportion of funding early in the project cycle. However, TC funding would not exceed 50% of the project’s total cost.

## Introduction
### Program design and delivery
#### ACIP projects and funding
ACIP received 77 project proposals, of which 53 projects were funded (68% approval rate). As shown in Figure 2, overall, the safety stream had the greatest number of projects and received the highest amount of funding. On a per project basis, the mass transit stream received the highest amount of funding.
**Figure 2. ACIP projects and committed funding by stream**
As of May 2026, 45 projects have been completed. Figure 3 demonstrates the proportion of projects completed by stream. By the time the final project proposal was approved (in February 2022), $568M had been committed out of the available $570M budget (99%).Footnote 4
**Figure 3. Project completion rate as of Spring 2026 (%)**
ACIP’s contribution budget of $570M (including the additional $82M added for biosecurity projects in August 2021) was intended for eligible recipients according to the following criteria:
*   National Airport System (NAS) airports that have annual passenger volumes over 525,000 (as of December 2019), are certified (i.e., meet TC safety standards and regulations), and are not eligible for the Airports Capital Assistance Program (ACAP), a program that funds airport capital projects, on a cost-sharing basis, for airports with less than 525,000 annual passengers.  
*   Specific non-NAS airports (Abbotsford, Fort McMurray, TradePort International Corporation - Hamilton International Airport, and Ports Toronto - Billy Bishop Toronto City Airport) whose passenger volumes make them ineligible for ACAP.
Figure 4 presents the number of projects completed and funding disbursed by year. Many projects span several years from launch to final claim. Projects are counted in the year that they were completed, and the financial data represents the project’s total cost at the time of their final claim payment. ACIP funding, however, would have been paid incrementally over the duration of the project.
</excerpt>
### Rank 3 of 53 — 0.71
<excerpt title="Airport Critical Infrastructure Program">
# Airport Critical Infrastructure Program
From: Transport Canada

# Airport Critical Infrastructure Program
## Backgrounder
The Airport Critical Infrastructure Program (ACIP) is a contribution funding program to help Canada’s larger airports make critical investments in safety, security or connectivity to mass transit.
The Airport Critical Infrastructure Program (ACIP) is a contribution funding program to help Canada’s larger airports make critical investments in safety, security or connectivity to mass transit.
With $489.6 million available over five years, the Program will help eligible airports mitigate the financial impact of the COVID-19 pandemic, as part of the Government of Canada’s strategy to ensure that Canada’s air transportation system provides Canadians with choice, connectivity and affordable air travel.
Canada’s world-leading network of airports has been put under substantial financial strain as a result of the dramatic decline in passenger travel resulting from the COVID-19 pandemic. Infrastructure projects, including those at airports, are generally long horizon investments with years of planning beforehand and many years of benefits thereafter.
Funding may be provided to owners and/or operators of the following types of airports:
*   National Airport System (NAS) airports with annual passenger volumes of over 525,000 passengers (as of December 2019)

*   Non-NAS Airports with annual passenger volumes of over 525,000 passengers (as of December 2019)
Eligible projects include:
*   Safety-related projects (e.g., runway and lighting rehabilitation)

*   Infrastructure projects for the purposes of operational efficiency and/or to enhance security at airports

*   Improvements to mass transit connections at airports
More information on ACIP, including program eligibility requirements and funding application process, can be found here: https://tc.canada.ca/en/programs/airport-critical-infrastructure-program
Search for related information by keyword:Aviation | Transport Canada | Canada | Transport and infrastructure | Coronavirus (COVID-19) | general public | backgrounders

# Airport Critical Infrastructure Program
## Page details
2022-08-15

# Airport Critical Infrastructure Program
## About this site
### Government of Canada
*   All contacts  
*   Departments and agencies  
*   About government

# Airport Critical Infrastructure Program
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

# Airport Critical Infrastructure Program
## About this site
### Government of Canada Corporate
*   Social media  
*   Mobile applications  
*   About Canada.ca  
*   Terms and conditions  
*   Privacy
</excerpt>
### Rank 4 of 53 — 0.71
<excerpt title="Lessons Learned Review of the Airport Critical Infrastructure Program">
## Introduction
### Program background
ACIP is a contribution funding program that was introduced during the COVID-19 pandemic when Canada’s airports were suffering from dramatic decreases in passengers and revenues. It was designed in 2020 and launched in May 2021 to help Canada’s larger airports (525,000+ passengers per year) continue to make critical investments in safety, security, connectivity to mass transit, and biosecurity. Because of declining revenues during the pandemic, infrastructure projects at Canadian airports were at risk of being delayed or cancelled, which would have postponed their potential benefits or permanently reduced an airport’s ability to deliver efficient services to Canadians. For example, opting to temporarily patch a runway or taxiway instead of completing a comprehensive repaving project would be more costly in the long run, with the airport authority having to pay twice – once for the temporary repair and again for the comprehensive rehabilitation. Further, given the drastic decrease in flight activity and the pre-existing construction for some mass transit projects (like Ottawa’s Light Rail Transit expansion) the COVID-19 pandemic provided an ideal window of opportunity to complete significant infrastructure projects.
The duration of the program was initially from fiscal year (FY) 2021-22 to 2025-26 but was extended to 2027-28, in October 2025, to allow time for the completion of major projects that were delayed due to supply chain issues and construction logistics.
ACIP’s calls for proposals opened on May 11, 2021, for the safety, security, and mass transit streams, and on August 13, 2021, for biosecurity. Money for biosecurity was announced in Budget 2021 (in April 2021), after ACIP had been designed and approved. Project proposals and expressions of interest were accepted starting on May 24, 2021. Specifically, applicants were invited to voluntarily submit an EOI to ensure eligibility and for feedback on their project proposal. Following that, applicants submitted a CPP for a funding decision. In practice, some applicants bypassed the EOI and proceeded directly to submitting a CPP.
TC offered information sessions to eligible airports for each application callout. They also organized regular meetings with eligible recipients and encouraged them to contact the ACIP team with questions at any time.

## Introduction
### Program design and delivery
Overall, ACIP funding was intended to enable investments in critical infrastructure projects that would continue through the pandemic and would support the recovery of the air sector through:
*   Uninterrupted implementation of projects to ensure continued safety and security, including compliance with standards and regulatory requirements  
*   Helping airports mitigate the financial impact of the pandemic  
*   Helping airports to avoid increasing passenger fees to pay for infrastructure projects  
*   Stimulating economic activity through the jobs that ACIP projects would provide  
*   Enabling airports to protect air travelers from the transmission of COVID-19 and help regain Canadians’ confidence in the safety of air travel.
The main Offices of Primary Interest (OPIs) at TC responsible for the design of ACIP were Transportation Infrastructure Programs and Air Policy. Program delivery was the responsibility of Transportation Infrastructure Programs. The number of full-time equivalents (FTE) within Transportation Infrastructure Programs that worked on ACIP decreased over time, with a high of 16 in 2021 to a low of 5 in 2024.
ACIP funds up to 50% of the total project cost for ACIP-approved infrastructure projects across four key streams. These include:
1.   safety, which encompasses initiatives such as runway rehabilitation, lighting improvements, and the acquisition of firefighting equipment  
2.   security, which involves projects like relocating screening or border checkpoints and enhancing cybersecurity infrastructure  
3.   mass transit, which supports the development of transit stations and other transportation infrastructure connected to airports  
4.   biosecurity, which focuses on infrastructure for COVID-19 testing and screening
Given the immediate need for funding due to the cash flow of some recipient airports, ACIP was designed to be flexible in how it allocated funds. TC could front-load contributions so that recipients could access a larger proportion of funding early in the project cycle. However, TC funding would not exceed 50% of the project’s total cost.
</excerpt>
### Rank 5 of 53 — 0.68
<excerpt title="Lessons Learned Review of the Airport Critical Infrastructure Program">
## Introduction
### Program design and delivery
#### ACIP projects and funding
ACIP received 77 project proposals, of which 53 projects were funded (68% approval rate). As shown in Figure 2, overall, the safety stream had the greatest number of projects and received the highest amount of funding. On a per project basis, the mass transit stream received the highest amount of funding.
**Figure 2. ACIP projects and committed funding by stream**
As of May 2026, 45 projects have been completed. Figure 3 demonstrates the proportion of projects completed by stream. By the time the final project proposal was approved (in February 2022), $568M had been committed out of the available $570M budget (99%).Footnote 4
**Figure 3. Project completion rate as of Spring 2026 (%)**
ACIP’s contribution budget of $570M (including the additional $82M added for biosecurity projects in August 2021) was intended for eligible recipients according to the following criteria:
*   National Airport System (NAS) airports that have annual passenger volumes over 525,000 (as of December 2019), are certified (i.e., meet TC safety standards and regulations), and are not eligible for the Airports Capital Assistance Program (ACAP), a program that funds airport capital projects, on a cost-sharing basis, for airports with less than 525,000 annual passengers.  
*   Specific non-NAS airports (Abbotsford, Fort McMurray, TradePort International Corporation - Hamilton International Airport, and Ports Toronto - Billy Bishop Toronto City Airport) whose passenger volumes make them ineligible for ACAP.
Figure 4 presents the number of projects completed and funding disbursed by year. Many projects span several years from launch to final claim. Projects are counted in the year that they were completed, and the financial data represents the project’s total cost at the time of their final claim payment. ACIP funding, however, would have been paid incrementally over the duration of the project.

## Introduction
### Program design and delivery
#### ACIP projects and funding
The vertical bars in Figure 4 reveal that the largest number of projects, including all biosecurity projects, were completed by 2023-24. The largest amount of ACIP funding was paid to recipients in the following fiscal year, 2024-25, as demonstrated by the trend line.
**Figure 4. Completed projects and ACIP funding per year**
Note that Figure 4 only includes the 45 projects that were completed as of May 2026. At the time of writing, 8 projects were underway but not yet complete.

## Introduction
### Lessons learned review: objective and scope
This review was conducted to address the information needs of TC’s senior management. The general purpose of the review was to collect evidence related to the relevance, effectiveness, design/delivery, and efficiency of ACIP, and to identify any lessons learned that could be used to inform future TC programming. For the full list of review questions, please see Appendix A.
This review covers the period from FY 2021-22 to FY 2024-25, given that the sunset date for the program was originally March 2026.Footnote 5

## Introduction
### Approach and methods
The following research methods and data sources were used to conduct the lessons learned review:

## Introduction
### Approach and methods
#### Document/Literature review
*   Program documents (presentation decks, briefing notes, recipient contribution agreements, final project reports, and cabinet documents), along with a review of the literature related to comparable international airport infrastructure programs.

## Introduction
### Approach and methods
#### Media review
*   News articles, project announcements and updates from the Canadian news media

## Introduction
### Approach and methods
#### Data review and analysis
*   A comprehensive review of ACIP-related data contained in project trackers  
*   Airport passenger volumes and revenues  
*   Building Construction Price Index  
*   ACIP budget and expenditures
</excerpt>

## Search 4 — query: "Airport Critical Infrastructure Program eligibility 525,000 passengers Transport Canada 2021"
### Rank 1 of 139 — 0.84 (passed on)
<excerpt title="Keeping Canada Connected: The Challenge of Regional Air Service ...">
## [PDF page 39]
airports, which operate with smaller passenger volumes compared to their larger counterparts. However,  
the program’s temporary two-year term limited its ability to act as a catalyst for air service beyond 2023.  
Airports Capital Assistance Program

## [PDF page 39]
The Airports Capital Assistance Program (ACAP), managed by Transport Canada, began in 1995 and  
has since invested over $1 billion in more than 1,200 projects across over 200 Canadian airports.48F48F49  
ACAP funds rehabilitation projects at local and regional airports that meet specific eligibility criteria,  
including passenger volume thresholds, year-round scheduled services, and federal certification  
standards.49F49F50 The program supports projects such as runway rehabilitation, equipment purchases for  
firefighting and snow removal, and terminal safety improvements.50 F50 F51 Depending on passenger volumes,  
the federal government covers a percentage of project costs, with airports north of the 60th parallel  
receiving a minimum of 85% funding.51 F51 F52 ACAP eligibility is restricted to airports that serve between 1,000  
and 525,000 passengers per year (unless it is a designated “remote” airport) and have regularly  
scheduled commercial passenger services year-round.52F52F53 A temporary expansion to this threshold to 1  
million passengers per year occurred from 2021 to 2023 as part of the government’s COVID-19 response  
for the sector.53F53F54 While ACAP supports regional air service by addressing regional airports’ infrastructure  
needs, its narrow focus on infrastructure and safety-related projects limits its ability to include broader  
service development.  
Airport Critical Infrastructure Program  
Created in 2021, the Airport Critical Infrastructure Program  
(ACIP) is a temporary 5-year federal initiative aimed at  
mitigating the COVID-19 pandemic's impact on larger  
Canadian airports. ACIP complements ACAP by primarily  
supporting airports with annual passenger volumes exceeding  
525,000, where it funds infrastructure projects related to  
safety, efficiency, and transit connections.54F54F55 ACIP can help  
larger regional airports alleviate the cost of critical  
infrastructure that is necessary for the airport to service  
additional passengers and aircraft. Although ACIP has  
supported 19 airports, including 10 regional ones, its
Yellowknife Airport

## [PDF page 39]
49 Airports Capital Assistance Program. Government of Canada. https://tc.canada.ca/en/programs/airports-capital-assistance-  
program  
50 Apply for ACAP funding. Government of Canada. https://tc.canada.ca/en/aviation/operating-airports-aerodromes/apply-acap-  
funding  
51 Ibid.  
52 Information for ACAP applicants. Government of Canada. https://tc.canada.ca/en/aviation/operating-airports-aerodromes/apply-  
acap-funding/information-acap-applicants  
53 Ibid.  
54 Enhancement of the Airports Capital Assistance Program. Transport Canada. https://www.canada.ca/en/transport-  
canada/news/2021/05/enhancement-of-the-airports-capital-assistance-program.html  
55 Airport Critical Infrastructure Program. Transport Canada. https://www.canada.ca/en/transport-canada/news/2021/05/airport-  
critical-infrastructure-program.html
34 | P  a  g  e
PDF link  
PDF link  
PDF link  
PDF link  
PDF link
</excerpt>
### Rank 2 of 139 — 0.80
<excerpt title="Lessons Learned Review of the Airport Critical Infrastructure Program">
## Introduction
### Program background
ACIP is a contribution funding program that was introduced during the COVID-19 pandemic when Canada’s airports were suffering from dramatic decreases in passengers and revenues. It was designed in 2020 and launched in May 2021 to help Canada’s larger airports (525,000+ passengers per year) continue to make critical investments in safety, security, connectivity to mass transit, and biosecurity. Because of declining revenues during the pandemic, infrastructure projects at Canadian airports were at risk of being delayed or cancelled, which would have postponed their potential benefits or permanently reduced an airport’s ability to deliver efficient services to Canadians. For example, opting to temporarily patch a runway or taxiway instead of completing a comprehensive repaving project would be more costly in the long run, with the airport authority having to pay twice – once for the temporary repair and again for the comprehensive rehabilitation. Further, given the drastic decrease in flight activity and the pre-existing construction for some mass transit projects (like Ottawa’s Light Rail Transit expansion) the COVID-19 pandemic provided an ideal window of opportunity to complete significant infrastructure projects.
The duration of the program was initially from fiscal year (FY) 2021-22 to 2025-26 but was extended to 2027-28, in October 2025, to allow time for the completion of major projects that were delayed due to supply chain issues and construction logistics.
ACIP’s calls for proposals opened on May 11, 2021, for the safety, security, and mass transit streams, and on August 13, 2021, for biosecurity. Money for biosecurity was announced in Budget 2021 (in April 2021), after ACIP had been designed and approved. Project proposals and expressions of interest were accepted starting on May 24, 2021. Specifically, applicants were invited to voluntarily submit an EOI to ensure eligibility and for feedback on their project proposal. Following that, applicants submitted a CPP for a funding decision. In practice, some applicants bypassed the EOI and proceeded directly to submitting a CPP.
TC offered information sessions to eligible airports for each application callout. They also organized regular meetings with eligible recipients and encouraged them to contact the ACIP team with questions at any time.

## Introduction
### Program design and delivery
Overall, ACIP funding was intended to enable investments in critical infrastructure projects that would continue through the pandemic and would support the recovery of the air sector through:
*   Uninterrupted implementation of projects to ensure continued safety and security, including compliance with standards and regulatory requirements  
*   Helping airports mitigate the financial impact of the pandemic  
*   Helping airports to avoid increasing passenger fees to pay for infrastructure projects  
*   Stimulating economic activity through the jobs that ACIP projects would provide  
*   Enabling airports to protect air travelers from the transmission of COVID-19 and help regain Canadians’ confidence in the safety of air travel.
The main Offices of Primary Interest (OPIs) at TC responsible for the design of ACIP were Transportation Infrastructure Programs and Air Policy. Program delivery was the responsibility of Transportation Infrastructure Programs. The number of full-time equivalents (FTE) within Transportation Infrastructure Programs that worked on ACIP decreased over time, with a high of 16 in 2021 to a low of 5 in 2024.
ACIP funds up to 50% of the total project cost for ACIP-approved infrastructure projects across four key streams. These include:
1.   safety, which encompasses initiatives such as runway rehabilitation, lighting improvements, and the acquisition of firefighting equipment  
2.   security, which involves projects like relocating screening or border checkpoints and enhancing cybersecurity infrastructure  
3.   mass transit, which supports the development of transit stations and other transportation infrastructure connected to airports  
4.   biosecurity, which focuses on infrastructure for COVID-19 testing and screening
Given the immediate need for funding due to the cash flow of some recipient airports, ACIP was designed to be flexible in how it allocated funds. TC could front-load contributions so that recipients could access a larger proportion of funding early in the project cycle. However, TC funding would not exceed 50% of the project’s total cost.
</excerpt>
### Rank 3 of 139 — 0.80
<excerpt title="Lessons Learned Review of the Airport Critical Infrastructure Program">
## Introduction
### Program design and delivery
Overall, ACIP funding was intended to enable investments in critical infrastructure projects that would continue through the pandemic and would support the recovery of the air sector through:
*   Uninterrupted implementation of projects to ensure continued safety and security, including compliance with standards and regulatory requirements  
*   Helping airports mitigate the financial impact of the pandemic  
*   Helping airports to avoid increasing passenger fees to pay for infrastructure projects  
*   Stimulating economic activity through the jobs that ACIP projects would provide  
*   Enabling airports to protect air travelers from the transmission of COVID-19 and help regain Canadians’ confidence in the safety of air travel.
The main Offices of Primary Interest (OPIs) at TC responsible for the design of ACIP were Transportation Infrastructure Programs and Air Policy. Program delivery was the responsibility of Transportation Infrastructure Programs. The number of full-time equivalents (FTE) within Transportation Infrastructure Programs that worked on ACIP decreased over time, with a high of 16 in 2021 to a low of 5 in 2024.
ACIP funds up to 50% of the total project cost for ACIP-approved infrastructure projects across four key streams. These include:
1.   safety, which encompasses initiatives such as runway rehabilitation, lighting improvements, and the acquisition of firefighting equipment  
2.   security, which involves projects like relocating screening or border checkpoints and enhancing cybersecurity infrastructure  
3.   mass transit, which supports the development of transit stations and other transportation infrastructure connected to airports  
4.   biosecurity, which focuses on infrastructure for COVID-19 testing and screening
Given the immediate need for funding due to the cash flow of some recipient airports, ACIP was designed to be flexible in how it allocated funds. TC could front-load contributions so that recipients could access a larger proportion of funding early in the project cycle. However, TC funding would not exceed 50% of the project’s total cost.

## Introduction
### Program design and delivery
#### ACIP projects and funding
ACIP received 77 project proposals, of which 53 projects were funded (68% approval rate). As shown in Figure 2, overall, the safety stream had the greatest number of projects and received the highest amount of funding. On a per project basis, the mass transit stream received the highest amount of funding.
**Figure 2. ACIP projects and committed funding by stream**
As of May 2026, 45 projects have been completed. Figure 3 demonstrates the proportion of projects completed by stream. By the time the final project proposal was approved (in February 2022), $568M had been committed out of the available $570M budget (99%).Footnote 4
**Figure 3. Project completion rate as of Spring 2026 (%)**
ACIP’s contribution budget of $570M (including the additional $82M added for biosecurity projects in August 2021) was intended for eligible recipients according to the following criteria:
*   National Airport System (NAS) airports that have annual passenger volumes over 525,000 (as of December 2019), are certified (i.e., meet TC safety standards and regulations), and are not eligible for the Airports Capital Assistance Program (ACAP), a program that funds airport capital projects, on a cost-sharing basis, for airports with less than 525,000 annual passengers.  
*   Specific non-NAS airports (Abbotsford, Fort McMurray, TradePort International Corporation - Hamilton International Airport, and Ports Toronto - Billy Bishop Toronto City Airport) whose passenger volumes make them ineligible for ACAP.
Figure 4 presents the number of projects completed and funding disbursed by year. Many projects span several years from launch to final claim. Projects are counted in the year that they were completed, and the financial data represents the project’s total cost at the time of their final claim payment. ACIP funding, however, would have been paid incrementally over the duration of the project.
</excerpt>
### Rank 4 of 139 — 0.79
<excerpt title="Keeping Canada Connected: The Challenge of Regional Air Service ...">
## [PDF page 73]
service level. In 2021, the Government of Canada temporarily expanded the eligibility criteria for  
ACAP from airports with less than 525,000 passengers to airports with less than 1 million passengers  
for a one-year period.18 8 F189 The Government should reinstate this new expanded eligibility criteria on a  
permanent basis and allow funding for both new infrastructure and maintenance of existing facilities  
to attract and retain air service. ACAP should be permanently re-capitalized with at a minimum of  
$150 million annually, adjusted for inflation as well as the significant escalation of construction costs.
•  Incorporate Regional Development in a renewed National Aviation Strategy: The current  
strategy is outdated and needs to be realigned with travel, trade and economic development  
interests.  The government should collaborate with stakeholders to create a comprehensive strategy  
ensuring the long-term sustainability of regional air service. This strategy should define Canada’s  
vision for aviation, addressing key areas such as infrastructure, connectivity, regulations, competition,  
and passenger experience. The strategy should situate the government’s policy approach to  
supporting the aviation sector within its broader internal and international trade, tourism, immigration,  
global affairs and national defence agendas. This will enable air carriers and regional airports to plan  
on areas such including but not limited to resilient supply chains, national defence in the Arctic and  
destination development.

## [PDF page 73]
•  Support the Labour Needs of the Aviation Industry at Regional Airports: The aviation industry is  
facing a shortage of critical professionals, including pilots, aircraft maintenance engineers, avionics  
technicians, flight instructors, and other operational staff. Regional airlines and airports often struggle  
to retain these workers, as larger competitors can offer more competitive salaries and benefits. To  
address this challenge, the government should develop a comprehensive recruitment strategy  
focused on regional communities. This strategy should include expanding aviation training programs  
at post-secondary institutions across Canada to attract both domestic and international students.  
Additionally, the government should establish dedicated immigration pathways to expedite the entry  
of aviation professionals and ensure swift credential recognition for highly skilled foreign workers.  
Enhancing labour mobility is also crucial, requiring collaboration with provinces to enable mutual  
recognition of aviation training and certifications across provincial borders.  
Furthermore, early career initiatives, such as scholarships and high school-entry programs, should be  
introduced to attract young talent, especially in regional areas. Financial support for academic and  
professional certifications would also help new and existing industry professionals advance their  
careers in Canada. Measures like reduced-interest loans, nationally backed lending programs, and  
other financial aid options could be implemented.  By implementing these measures, the government  
can strengthen the aviation workforce, support regional airports, and ensure the long-term  
sustainability of the industry.
•  Streamline Regulations to Improve Regional Connectivity: The government should eliminate  
inefficiencies that burden regional airports and limit connectivity. This includes exploring innovative  
solutions like video interviews for border and security clearances at smaller airports. Additionally,  
security screening could be optimized to reduce operational costs and connection times, particularly  
for U.S.-bound passengers transiting through Canadian hubs.
By implementing these measures, the Government of Canada can protect and enhance regional air  
service, ensuring its vital role in economic development and national connectivity.
189 Enhancement of the Airports Capital Assistance Program. Transport Canada. https://www.canada.ca/en/transport-  
canada/news/2021/05/enhancement-of-the-airports-capital-assistance-program.html
68 | P  a  g  e
PDF link

## [PDF page 74]
69 | P  a  g  e
</excerpt>
### Rank 5 of 139 — 0.77
<excerpt title="Airport Critical Infrastructure Program">
# Airport Critical Infrastructure Program
From: Transport Canada

# Airport Critical Infrastructure Program
## Backgrounder
The Airport Critical Infrastructure Program (ACIP) is a contribution funding program to help Canada’s larger airports make critical investments in safety, security or connectivity to mass transit.
The Airport Critical Infrastructure Program (ACIP) is a contribution funding program to help Canada’s larger airports make critical investments in safety, security or connectivity to mass transit.
With $489.6 million available over five years, the Program will help eligible airports mitigate the financial impact of the COVID-19 pandemic, as part of the Government of Canada’s strategy to ensure that Canada’s air transportation system provides Canadians with choice, connectivity and affordable air travel.
Canada’s world-leading network of airports has been put under substantial financial strain as a result of the dramatic decline in passenger travel resulting from the COVID-19 pandemic. Infrastructure projects, including those at airports, are generally long horizon investments with years of planning beforehand and many years of benefits thereafter.
Funding may be provided to owners and/or operators of the following types of airports:
*   National Airport System (NAS) airports with annual passenger volumes of over 525,000 passengers (as of December 2019)

*   Non-NAS Airports with annual passenger volumes of over 525,000 passengers (as of December 2019)
Eligible projects include:
*   Safety-related projects (e.g., runway and lighting rehabilitation)

*   Infrastructure projects for the purposes of operational efficiency and/or to enhance security at airports

*   Improvements to mass transit connections at airports
More information on ACIP, including program eligibility requirements and funding application process, can be found here: https://tc.canada.ca/en/programs/airport-critical-infrastructure-program
Search for related information by keyword:Aviation | Transport Canada | Canada | Transport and infrastructure | Coronavirus (COVID-19) | general public | backgrounders

# Airport Critical Infrastructure Program
## Page details
2022-08-15

# Airport Critical Infrastructure Program
## About this site
### Government of Canada
*   All contacts  
*   Departments and agencies  
*   About government

# Airport Critical Infrastructure Program
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

# Airport Critical Infrastructure Program
## About this site
### Government of Canada Corporate
*   Social media  
*   Mobile applications  
*   About Canada.ca  
*   Terms and conditions  
*   Privacy
</excerpt>

## Search 5 — query: ""Airport Critical Infrastructure Program" eligible airports list 2021 Canada"
### Rank 1 of 330 — 0.91 (passed on)
<excerpt title="AMCO Study of Airports and Aerodromes">
## [PDF page 89]
The proportion of project costs that are  funded through ACAP decreases  with  hi gher  passenger  
volumes.  For example,  projects airports with between 1,000 and 49,999 annual  enplaned / deplaned  
passengers are eligible for 100% funding, while facilities that serve between 500,000 and 524,999  
passengers are eligible for 5% funding.  Projects eligible under ACAP follow a three-  part prioritization:

## [PDF page 89]
1.  Projects to rehabilitate airside  facilities or buy equipment for aircraft rescue and firefighting.  
Examples include runway and taxiway rehabilitation projects, visual aid and lighting  
replacements, and the acquisition of firefighting equipment;  
2.  Mobile equipment acquisition projects, such  as snow blowers, plows, and tractors; and  
3.  Terminal building safety improvement projects, such as sprinkler upgrades and asbestos  
removal.  
With few exceptions, ACAP is limited to the rehabilitation or replacement of existing assets as opposed  
to the development of new facilities and is confined to infrastructure that is directly associated with air  
carrier operations. A taxiway serving a general aviation hangar row, for example, would be ineligible  
for funding through ACAP.  
C OV ID -19 Program Changes  
In May 2021 during the COVID  -19 pandemic, the federal government announced a series of temporary  
enhancements to ACAP that would apply over a two-  year period, including:  
•  A one-  time increase in annual funding, including  an additional  $93M in 2021-  2022 and $93M  
in 2022  -2023; and  
•  The extension of program eligibility to eight NAS airports serving  few er  than 1M annual  
passengers, including London International Airport and Thunder Bay International Airport in  
Ontario.  
These changes were made recognizing  that  the si gni fi cant financial impacts experienced by regional  
airports had the potential to delay or cancel critical infrastructure rehabilitation and replacement  
projects.  While the future of the C OV ID  -19 pandemic remains uncertain and  the trajectory of the  
financial recovery of Ontario’s airports is  unclear as of 2022, the pandemic-related ACAP changes  
described above have not been announced for continuation past 2022-  2023  and the program is  
expected to return to its pre-  pandemic $38M annual budget.

## [PDF page 89]
9.1.2  Airport Critical Infrastructure Program  
The Airport Critical Infrastructure Program was announced in May 2021 as a temporary program in  
response to the COVID-19 pandemic, with $490M in funding to be made available over a five-  y e ar  
period. ACIP eligible airports include NAS and  non-NAS airports that served more than 525,000  
passengers in 2019 –  in Ontario, this includes six airports: Toronto Pearson International Airport,  
Ottawa International Airport, London International Airport, Thunder Bay International Airport, Hamilton  
International Airport, and Billy Bishop Toronto City Airport. Under ACIP, eligible projects include safety-  
related initiatives, projects to improve operational efficiency or security, and rapid transit connectivity  
projects.  
ACIP is a temporary program and its renewal has not been announced beyond the terms of the $490M  
five-year period  set to expire in 2026.
Study of Ontario’s Airports and Aerodromes Airport Management Council of Ontario  74
</excerpt>
### Rank 2 of 330 — 0.87
<excerpt title="AMCO Study of Airports and Aerodromes">
## [PDF page 89]
9.1.2  Airport Critical Infrastructure Program  
The Airport Critical Infrastructure Program was announced in May 2021 as a temporary program in  
response to the COVID-19 pandemic, with $490M in funding to be made available over a five-  y e ar  
period. ACIP eligible airports include NAS and  non-NAS airports that served more than 525,000  
passengers in 2019 –  in Ontario, this includes six airports: Toronto Pearson International Airport,  
Ottawa International Airport, London International Airport, Thunder Bay International Airport, Hamilton  
International Airport, and Billy Bishop Toronto City Airport. Under ACIP, eligible projects include safety-  
related initiatives, projects to improve operational efficiency or security, and rapid transit connectivity  
projects.  
ACIP is a temporary program and its renewal has not been announced beyond the terms of the $490M  
five-year period  set to expire in 2026.
Study of Ontario’s Airports and Aerodromes Airport Management Council of Ontario  74

## [PDF page 90]
9.1.3  Regional Air T ransportation Initiative  
In 2021, the federal government made a one-  time announcement of $206M in funding on a national  
scale for the  Regional Air Transportation Initiative. In Ontario, RATI is administered through the two  
R egi onal  Development Agencies: FedDev Ontario and FedNor Ontario. RATI was opened to regional  
and local airports that support air service connectivity, with an emphasis on facilities that support  
scheduled passenger air services that were negatively impacted by the COVID-19 pandemic.  
The RATI program targets projects that will result in increased regional air transportation connectivity,  
address the cash flow needs of airports negatively impacted by the COVID-19 pandemic, and / or  
adapt or modernize airport operations. Although applications were prioritized according to the degree  
to which they achieve the program aims, mandatory criteria  regarding certification or minimum activity  
levels were not used. As a result, a wide range of airports in Ontario have benefited from RATI funding,  
including Community airports such as Tillsonburg and St. Thomas, Regional Passenger facilities such  
as Sarnia, and Northern & Remote facilities such as Wawa. Projects advanced through RATI funding  
have included terminal building modernizations, master planning and air service data collection  
studies, capital construction projects, and mobile equipment replacement projects.  
The RATI program is fully subscribed as of May 2022 and its reopening for additional applications  has  
not been announced.
</excerpt>
### Rank 3 of 330 — 0.71
<excerpt title="Air Sector Recovery - Transports Canada">
*   Canada’s air transportation is a major contributor to the national economy and an important source of jobs. Before the COVID-19 pandemic, the sector contributed over $14 billion in real gross domestic product and employed approximately 107,000 Canadians.

*   The impact of the pandemic on the air transportation sector was unprecedented. Following its onset, travel volumes fell by 90% for a year, generating some of the largest revenue and job losses of any major sector.

*   In the wake of these challenges, the Government of Canada took considerable actions to support the air sector:  
    *   In March 2020, the Government of Canada announced Airport Rent Relief from March to December 2020 by waiving rents for the 21 airport authorities that have ground leases with the federal government, as well as Ports Toronto which operates Billy Bishop Toronto City Airport. Additional support was provided from January to December 2023 through a combination of waivers and deferrals.   
    *   In April 2020, the Government of Canada announced up to $17.3 million for Northern Carriers to ensure that essential goods like food and medical supplies could reach communities in the Territories that depend on air transport. The Government announced more funding of up to $174 million in August 2020 to ensure continuity of essential air access to remote communities through bilateral agreements with provinces and territories under the Remote Air Services Program (RASP).  
    *   The Airports Capital Assistance Program (ACAP), which provides up to $38 million per year in funding to small and regional airports to make critical investments in safety-related capital infrastructure, received a one-time top up funding of $186 million for two years from 2021- 2023. During this period, the minimum federal cost share was increased to 50% and the program was expanded to include 8 small federally owned airports. This financial support helped make sure that Canada’s smaller airports could immediately make required safety improvements despite revenue losses due to COVID-19.  
    *   In May 2021, the Airport Relief Fund (ARF) provided $64.8 million in financial relief to 22 airports struggling with reduced air travel during the COVID-19 pandemic. This helped eligible airports maintain operations and mitigate the risk of insolvency.  
    *   In 2021, the Airport Critical Infrastructure Program (ACIP) was launched to provide over $570 million in funding over 5 years to airports for eligible infrastructure projects related to safety, security, connectivity to mass transit systems, or testing and screening related to COVID-19 and its variants. This funding was allocated to 53 critical infrastructure projects at 19 airports across Canada.  

    *   The Regional Air Transportation Initiative (RATI), delivered by Canada’s Regional Development Agencies (RDAs) in 2021 also provided $206 million over two years to eligible regional businesses and airports that directly contribute to regional air transportation to help maintain regional air connections and services during the pandemic.
</excerpt>
### Rank 4 of 330 — 0.69
<excerpt title="Lessons Learned Review of the Airport Critical Infrastructure Program">
## Introduction
### COVID-19 and its impact on air travel
Initial disruptions to air travel began in January 2020, driven by emerging health concerns and precautionary measures. Canada’s early response included issuing travel advisories and preparing quarantine protocols.
By March 2020, the aviation sector faced a global crisis as countries imposed border closures and travel bans. Airlines worldwide cancelled large volumes of flights and passenger demand collapsed.Footnote 1 Canada closed its borders to most foreign nationals on March 16, 2020, followed by a Canada-U.S. border closure for non-essential travel on March 21, 2020. All international flights coming into Canada were redirected to four airports (i.e., Toronto Pearson International Airport, Vancouver International Airport, Calgary International Airport, and Montréal–Trudeau International Airport).
The most severe and widespread impacts on air travel occurred between March and May 2020. By May, global flight activity had declined by approximately 80% compared to the same period in 2019.Footnote 2 Canada’s international arrivals dropped by over 90%, with strict entry requirements including testing and quarantine.Footnote 3 These measures resulted in an unprecedented contraction in air traffic, severely affecting airport operations and revenues. Passenger traffic across all Canadian airports is displayed in Figure 1.
**Figure 1. Total passengers enplaned and deplaned 2019 to 2024 at all Canadian airports**

## Introduction
### Program background
ACIP is a contribution funding program that was introduced during the COVID-19 pandemic when Canada’s airports were suffering from dramatic decreases in passengers and revenues. It was designed in 2020 and launched in May 2021 to help Canada’s larger airports (525,000+ passengers per year) continue to make critical investments in safety, security, connectivity to mass transit, and biosecurity. Because of declining revenues during the pandemic, infrastructure projects at Canadian airports were at risk of being delayed or cancelled, which would have postponed their potential benefits or permanently reduced an airport’s ability to deliver efficient services to Canadians. For example, opting to temporarily patch a runway or taxiway instead of completing a comprehensive repaving project would be more costly in the long run, with the airport authority having to pay twice – once for the temporary repair and again for the comprehensive rehabilitation. Further, given the drastic decrease in flight activity and the pre-existing construction for some mass transit projects (like Ottawa’s Light Rail Transit expansion) the COVID-19 pandemic provided an ideal window of opportunity to complete significant infrastructure projects.
The duration of the program was initially from fiscal year (FY) 2021-22 to 2025-26 but was extended to 2027-28, in October 2025, to allow time for the completion of major projects that were delayed due to supply chain issues and construction logistics.
ACIP’s calls for proposals opened on May 11, 2021, for the safety, security, and mass transit streams, and on August 13, 2021, for biosecurity. Money for biosecurity was announced in Budget 2021 (in April 2021), after ACIP had been designed and approved. Project proposals and expressions of interest were accepted starting on May 24, 2021. Specifically, applicants were invited to voluntarily submit an EOI to ensure eligibility and for feedback on their project proposal. Following that, applicants submitted a CPP for a funding decision. In practice, some applicants bypassed the EOI and proceeded directly to submitting a CPP.
TC offered information sessions to eligible airports for each application callout. They also organized regular meetings with eligible recipients and encouraged them to contact the ACIP team with questions at any time.
</excerpt>
### Rank 5 of 330 — 0.68
<excerpt title="Lessons Learned Review of the Airport Critical Infrastructure Program">
## Introduction
### Program design and delivery
Overall, ACIP funding was intended to enable investments in critical infrastructure projects that would continue through the pandemic and would support the recovery of the air sector through:
*   Uninterrupted implementation of projects to ensure continued safety and security, including compliance with standards and regulatory requirements  
*   Helping airports mitigate the financial impact of the pandemic  
*   Helping airports to avoid increasing passenger fees to pay for infrastructure projects  
*   Stimulating economic activity through the jobs that ACIP projects would provide  
*   Enabling airports to protect air travelers from the transmission of COVID-19 and help regain Canadians’ confidence in the safety of air travel.
The main Offices of Primary Interest (OPIs) at TC responsible for the design of ACIP were Transportation Infrastructure Programs and Air Policy. Program delivery was the responsibility of Transportation Infrastructure Programs. The number of full-time equivalents (FTE) within Transportation Infrastructure Programs that worked on ACIP decreased over time, with a high of 16 in 2021 to a low of 5 in 2024.
ACIP funds up to 50% of the total project cost for ACIP-approved infrastructure projects across four key streams. These include:
1.   safety, which encompasses initiatives such as runway rehabilitation, lighting improvements, and the acquisition of firefighting equipment  
2.   security, which involves projects like relocating screening or border checkpoints and enhancing cybersecurity infrastructure  
3.   mass transit, which supports the development of transit stations and other transportation infrastructure connected to airports  
4.   biosecurity, which focuses on infrastructure for COVID-19 testing and screening
Given the immediate need for funding due to the cash flow of some recipient airports, ACIP was designed to be flexible in how it allocated funds. TC could front-load contributions so that recipients could access a larger proportion of funding early in the project cycle. However, TC funding would not exceed 50% of the project’s total cost.

## Introduction
### Program design and delivery
#### ACIP projects and funding
ACIP received 77 project proposals, of which 53 projects were funded (68% approval rate). As shown in Figure 2, overall, the safety stream had the greatest number of projects and received the highest amount of funding. On a per project basis, the mass transit stream received the highest amount of funding.
**Figure 2. ACIP projects and committed funding by stream**
As of May 2026, 45 projects have been completed. Figure 3 demonstrates the proportion of projects completed by stream. By the time the final project proposal was approved (in February 2022), $568M had been committed out of the available $570M budget (99%).Footnote 4
**Figure 3. Project completion rate as of Spring 2026 (%)**
ACIP’s contribution budget of $570M (including the additional $82M added for biosecurity projects in August 2021) was intended for eligible recipients according to the following criteria:
*   National Airport System (NAS) airports that have annual passenger volumes over 525,000 (as of December 2019), are certified (i.e., meet TC safety standards and regulations), and are not eligible for the Airports Capital Assistance Program (ACAP), a program that funds airport capital projects, on a cost-sharing basis, for airports with less than 525,000 annual passengers.  
*   Specific non-NAS airports (Abbotsford, Fort McMurray, TradePort International Corporation - Hamilton International Airport, and Ports Toronto - Billy Bishop Toronto City Airport) whose passenger volumes make them ineligible for ACAP.
Figure 4 presents the number of projects completed and funding disbursed by year. Many projects span several years from launch to final claim. Projects are counted in the year that they were completed, and the financial data represents the project’s total cost at the time of their final claim payment. ACIP funding, however, would have been paid incrementally over the duration of the project.
</excerpt>

## Search 6 — query: "2020 air passenger traffic table 23-10-0253-01 Canadian airports 500k"
### Rank 1 of 197 — 0.72 (passed on)
<excerpt title="List of the busiest airports in Canada">
20	Kelowna International Airport	Kelowna	75,581	3 	  
21	Billy Bishop Toronto City Airport	Toronto	73,469	1 	  
22	Edmonton International Airport	Edmonton Metropolitan Region	71,316	3 	  
23	Langley Regional Airport	Langley Township	71,225	1 	  
24	Greater Moncton Roméo LeBlanc International Airport	Moncton	69,855	9 	  
25	Sault Ste. Marie Airport	Sault Ste. Marie	67,725	5 	  
26	Montréal–Mirabel International Airport	Greater Montreal	66,572	1 	  
27	Edmonton/Villeneuve Airport	Edmonton	65,450	2 	  
28	Ottawa Macdonald–Cartier International Airport	Ottawa	64,797		  
29	Fredericton International Airport	Fredericton	57,697	15 	  
30	Regina International Airport	Regina	44,433	1 	  
31	Halifax Stanfield International Airport	Halifax	32,315		  
32	Vancouver Harbour Flight Centre	Metro Vancouver	32,204		  
2020edit
Air traffic decreased greatly in this year due to the COVID-19 pandemic.

Canada's busiest airports by passenger trafficedit  
Rank	Rank  
change	Airport	Serves	Total  
passengers	Annual  
change  
1		Toronto Pearson International Airport	Greater Toronto Area	13,307,077[118]	73.6%   
2		Vancouver International Airport	Metro Vancouver	7,300,287[119]	72.3%   
3	1	Calgary International Airport	Calgary Region	5,675,483[120]	68.4%   
4	1	Montréal–Trudeau International Airport	Greater Montreal	5,436,998[121]	73.2%   
5		Edmonton International Airport	Edmonton Metropolitan Region	2,628,891[122]	67.7%   
6		Ottawa Macdonald–Cartier International Airport	National Capital Region	1,363,512[123]	73.3%   
7		Winnipeg Richardson International Airport	Winnipeg Capital Region	1,299,225[124]	71.0%   
8		Halifax Stanfield International Airport	Halifax	995,426[125]	76.2%   
9	1	Kelowna International Airport	Kelowna/Okanagan Valley	737,447[126]	63.7%   
10	1	Victoria International Airport	Greater Victoria	574,874[127]	70.1%   
11	1	Québec City Jean Lesage International Airport	Quebec City	535,111[128]	70.1%   
12	1	Saskatoon John G. Diefenbaker International Airport	Saskatoon	461,900[129]	69.0%   
13	4	Billy Bishop Toronto City Airport	Toronto	389,000[130]	86.0%
</excerpt>
### Rank 2 of 197 — 0.71
<excerpt title="Air Carrier Traffic at Canadian Airports">
## [PDF page 12]
St  John’s  Intl,  N.L.  1,365,652  1,304,321  -4.5  60,649  38,346  -36.8  93,299  101,812  9.1  1,444,479  
Sudbury,  Ont.  x  x  x  x  x  x  0  0  ...  229,010  
Sydney,  N.S.  x  x  x  x  x  x  x  x  x  181,762  
Terrace,  B.C.  x  276,879  x  x  0  x  0  0  ...  276,879  
Thunder  Bay,  Ont.  x  x  x  x  x  x  x  x  x  732,136  
Timmins,  Ont.  210,448  210,831  0.2  0  0  ...  0  0  ...  210,831  
Toronto/Billy  Bishop  Toronto  City,  Ont.  x  x  x  x  x  x  0  0  ...  x  
Toronto/Lester  B  Pearson  Intl,  Ont.  15,021,121  15,661,502  4.3  10,165,869  10,752,741  5.8  12,270,822  13,224,598  7.8  39,638,841  
Vancouver  Harbour,  B.C.  x  x  x  0  0  ...  x  x  x  252,143
</excerpt>
### Rank 3 of 197 — 0.71
<excerpt title="Air Carrier Traffic at Canadian Airports">
## [PDF page 11]
Abbotsford,B.C.  xxxxx  
Calgary  Intl,  Alta.  7,267,827  7,311,102  14,446,981  14,578,929  0.9  
Charlottetown,  P.E.I.  155,451  155,372  308,351  310,823  0.8  
Comox,  B.C.  173,622  170,296  317,974  343,918  8.2  
Cranbrook,  B.C.  64,953  64,825  125,156  129,778  3.7  
Deer  Lake,  N.L.  161,178  163,478  319,791  324,656  1.5  
Edmonton  Intl,  Alta.  3,730,217  3,735,924  7,634,926  7,466,141  -2.2  
FortMacKay/Albian,Alta.  xxxxx  
FortMacKay/Horizon,Alta.  xxxxx  
Fort  McMurray,  Alta.  508,807  499,338  1,164,761  1,008,145  -13.4  
Fort  St  John,  B.C.  128,597  127,924  245,800  256,521  4.4
</excerpt>
### Rank 4 of 197 — 0.70
<excerpt title="Air Carrier Traffic at Canadian Airports">
## [PDF page 11]
Fredericton  International,  N.B.  168,765  168,524  x  337,289  x  
Gander  Intl,  N.L.  85,152  86,746  141,134  171,898  21.8  
Goose  Bay,  N.L.  94,189  95,772  176,170  189,961  7.8  
Grande  Prairie,  Alta.  xxxxx  
Halifax/Robert  L  Stanfield  Intl,  N.S.  1,802,370  1,799,480  3,579,850  3,601,850  0.6  
Hamilton,Ont.  xxxxx  
Iqaluit,  Nvt.  69,453  87,180  x  156,633  x  
Kamloops,B.C.  xxxxx  
Kelowna,  B.C.  776,277  774,372  1,562,546  1,550,649  -0.8  
Kitchener/Waterloo,  Ont.  71,414  74,270  133,829  145,684  8.9  
London,  Ont.  241,272  236,312  478,713  477,584  -0.2  
Moncton/Greater  Moncton  Intl,  N.B.  315,498  312,556  648,547  628,054  -3.2
</excerpt>
### Rank 5 of 197 — 0.69
<excerpt title="Air Carrier Traffic at Canadian Airports">
## [PDF page 12]
Kelowna,  B.C.  1,376,309  1,388,411  0.9  152,059  127,474  -16.2  34,178  34,764  1.7  1,550,649  
Kitchener/Waterloo,  Ont.  x  x  x  x  x  x  x  x  x  145,684  
London,  Ont.  x  x  x  x  x  x  28,397  25,776  -9.2  477,584  
Moncton/Greater  Moncton  Intl,  N.B.  585,870  576,498  -1.6  24,909  11,192  -55.1  37,768  40,364  6.9  628,054  
Montréal/Pierre  Elliott  Trudeau  Intl,  Que.  5,388,605  5,521,181  2.5  3,385,698  3,436,743  1.5  5,437,639  5,795,323  6.6  14,753,247  
Nanaimo,  B.C.  x  x  x  x  x  x  0  0  ...  x  

## [PDF page 12]
Ottawa/Macdonald-Cartier  Intl,  Ont.  3,313,170  3,374,404  1.8  715,222  623,357  -12.8  439,075  430,781  -1.9  4,428,542  
Prince  George,  B.C.  x  x  x  x  x  x  x  x  x  431,851  
Québec/Jean  Lesage  Intl,  Que.  862,574  897,769  4.1  233,579  220,393  -5.6  352,891  371,222  5.2  1,489,384  
Regina  Intl,  Sask.  990,946  1,039,179  4.9  x  x  x  x  x  x  1,241,818  
SaintJohn,N.B.  xxxxxxxxxx  
Saskatoon/John  G  Diefenbaker  Intl,  Sask.  1,183,704  1,201,835  1.5  x  x  x  x  x  x  1,422,350  
SaultSteMarie,Ont.  xxxxxxxxxx  
Sept-Îles,  Que.  x  x  x  x  x  x  x  x  x  146,237
</excerpt>

## Search 7 — query: ""ACIP eligible airports" 2021 Canada list"
### Rank 1 of 201 — 0.89 (passed on)
<excerpt title="AMCO Study of Airports and Aerodromes">
## [PDF page 89]
The proportion of project costs that are  funded through ACAP decreases  with  hi gher  passenger  
volumes.  For example,  projects airports with between 1,000 and 49,999 annual  enplaned / deplaned  
passengers are eligible for 100% funding, while facilities that serve between 500,000 and 524,999  
passengers are eligible for 5% funding.  Projects eligible under ACAP follow a three-  part prioritization:

## [PDF page 89]
1.  Projects to rehabilitate airside  facilities or buy equipment for aircraft rescue and firefighting.  
Examples include runway and taxiway rehabilitation projects, visual aid and lighting  
replacements, and the acquisition of firefighting equipment;  
2.  Mobile equipment acquisition projects, such  as snow blowers, plows, and tractors; and  
3.  Terminal building safety improvement projects, such as sprinkler upgrades and asbestos  
removal.  
With few exceptions, ACAP is limited to the rehabilitation or replacement of existing assets as opposed  
to the development of new facilities and is confined to infrastructure that is directly associated with air  
carrier operations. A taxiway serving a general aviation hangar row, for example, would be ineligible  
for funding through ACAP.  
C OV ID -19 Program Changes  
In May 2021 during the COVID  -19 pandemic, the federal government announced a series of temporary  
enhancements to ACAP that would apply over a two-  year period, including:  
•  A one-  time increase in annual funding, including  an additional  $93M in 2021-  2022 and $93M  
in 2022  -2023; and  
•  The extension of program eligibility to eight NAS airports serving  few er  than 1M annual  
passengers, including London International Airport and Thunder Bay International Airport in  
Ontario.  
These changes were made recognizing  that  the si gni fi cant financial impacts experienced by regional  
airports had the potential to delay or cancel critical infrastructure rehabilitation and replacement  
projects.  While the future of the C OV ID  -19 pandemic remains uncertain and  the trajectory of the  
financial recovery of Ontario’s airports is  unclear as of 2022, the pandemic-related ACAP changes  
described above have not been announced for continuation past 2022-  2023  and the program is  
expected to return to its pre-  pandemic $38M annual budget.

## [PDF page 89]
9.1.2  Airport Critical Infrastructure Program  
The Airport Critical Infrastructure Program was announced in May 2021 as a temporary program in  
response to the COVID-19 pandemic, with $490M in funding to be made available over a five-  y e ar  
period. ACIP eligible airports include NAS and  non-NAS airports that served more than 525,000  
passengers in 2019 –  in Ontario, this includes six airports: Toronto Pearson International Airport,  
Ottawa International Airport, London International Airport, Thunder Bay International Airport, Hamilton  
International Airport, and Billy Bishop Toronto City Airport. Under ACIP, eligible projects include safety-  
related initiatives, projects to improve operational efficiency or security, and rapid transit connectivity  
projects.  
ACIP is a temporary program and its renewal has not been announced beyond the terms of the $490M  
five-year period  set to expire in 2026.
Study of Ontario’s Airports and Aerodromes Airport Management Council of Ontario  74
</excerpt>
### Rank 2 of 201 — 0.85
<excerpt title="AMCO Study of Airports and Aerodromes">
## [PDF page 89]
9.1.2  Airport Critical Infrastructure Program  
The Airport Critical Infrastructure Program was announced in May 2021 as a temporary program in  
response to the COVID-19 pandemic, with $490M in funding to be made available over a five-  y e ar  
period. ACIP eligible airports include NAS and  non-NAS airports that served more than 525,000  
passengers in 2019 –  in Ontario, this includes six airports: Toronto Pearson International Airport,  
Ottawa International Airport, London International Airport, Thunder Bay International Airport, Hamilton  
International Airport, and Billy Bishop Toronto City Airport. Under ACIP, eligible projects include safety-  
related initiatives, projects to improve operational efficiency or security, and rapid transit connectivity  
projects.  
ACIP is a temporary program and its renewal has not been announced beyond the terms of the $490M  
five-year period  set to expire in 2026.
Study of Ontario’s Airports and Aerodromes Airport Management Council of Ontario  74

## [PDF page 90]
9.1.3  Regional Air T ransportation Initiative  
In 2021, the federal government made a one-  time announcement of $206M in funding on a national  
scale for the  Regional Air Transportation Initiative. In Ontario, RATI is administered through the two  
R egi onal  Development Agencies: FedDev Ontario and FedNor Ontario. RATI was opened to regional  
and local airports that support air service connectivity, with an emphasis on facilities that support  
scheduled passenger air services that were negatively impacted by the COVID-19 pandemic.  
The RATI program targets projects that will result in increased regional air transportation connectivity,  
address the cash flow needs of airports negatively impacted by the COVID-19 pandemic, and / or  
adapt or modernize airport operations. Although applications were prioritized according to the degree  
to which they achieve the program aims, mandatory criteria  regarding certification or minimum activity  
levels were not used. As a result, a wide range of airports in Ontario have benefited from RATI funding,  
including Community airports such as Tillsonburg and St. Thomas, Regional Passenger facilities such  
as Sarnia, and Northern & Remote facilities such as Wawa. Projects advanced through RATI funding  
have included terminal building modernizations, master planning and air service data collection  
studies, capital construction projects, and mobile equipment replacement projects.  
The RATI program is fully subscribed as of May 2022 and its reopening for additional applications  has  
not been announced.
</excerpt>
### Rank 3 of 201 — 0.66
<excerpt title="Lessons Learned Review of the Airport Critical Infrastructure Program">
## Introduction
### COVID-19 and its impact on air travel
Initial disruptions to air travel began in January 2020, driven by emerging health concerns and precautionary measures. Canada’s early response included issuing travel advisories and preparing quarantine protocols.
By March 2020, the aviation sector faced a global crisis as countries imposed border closures and travel bans. Airlines worldwide cancelled large volumes of flights and passenger demand collapsed.Footnote 1 Canada closed its borders to most foreign nationals on March 16, 2020, followed by a Canada-U.S. border closure for non-essential travel on March 21, 2020. All international flights coming into Canada were redirected to four airports (i.e., Toronto Pearson International Airport, Vancouver International Airport, Calgary International Airport, and Montréal–Trudeau International Airport).
The most severe and widespread impacts on air travel occurred between March and May 2020. By May, global flight activity had declined by approximately 80% compared to the same period in 2019.Footnote 2 Canada’s international arrivals dropped by over 90%, with strict entry requirements including testing and quarantine.Footnote 3 These measures resulted in an unprecedented contraction in air traffic, severely affecting airport operations and revenues. Passenger traffic across all Canadian airports is displayed in Figure 1.
**Figure 1. Total passengers enplaned and deplaned 2019 to 2024 at all Canadian airports**

## Introduction
### Program background
ACIP is a contribution funding program that was introduced during the COVID-19 pandemic when Canada’s airports were suffering from dramatic decreases in passengers and revenues. It was designed in 2020 and launched in May 2021 to help Canada’s larger airports (525,000+ passengers per year) continue to make critical investments in safety, security, connectivity to mass transit, and biosecurity. Because of declining revenues during the pandemic, infrastructure projects at Canadian airports were at risk of being delayed or cancelled, which would have postponed their potential benefits or permanently reduced an airport’s ability to deliver efficient services to Canadians. For example, opting to temporarily patch a runway or taxiway instead of completing a comprehensive repaving project would be more costly in the long run, with the airport authority having to pay twice – once for the temporary repair and again for the comprehensive rehabilitation. Further, given the drastic decrease in flight activity and the pre-existing construction for some mass transit projects (like Ottawa’s Light Rail Transit expansion) the COVID-19 pandemic provided an ideal window of opportunity to complete significant infrastructure projects.
The duration of the program was initially from fiscal year (FY) 2021-22 to 2025-26 but was extended to 2027-28, in October 2025, to allow time for the completion of major projects that were delayed due to supply chain issues and construction logistics.
ACIP’s calls for proposals opened on May 11, 2021, for the safety, security, and mass transit streams, and on August 13, 2021, for biosecurity. Money for biosecurity was announced in Budget 2021 (in April 2021), after ACIP had been designed and approved. Project proposals and expressions of interest were accepted starting on May 24, 2021. Specifically, applicants were invited to voluntarily submit an EOI to ensure eligibility and for feedback on their project proposal. Following that, applicants submitted a CPP for a funding decision. In practice, some applicants bypassed the EOI and proceeded directly to submitting a CPP.
TC offered information sessions to eligible airports for each application callout. They also organized regular meetings with eligible recipients and encouraged them to contact the ACIP team with questions at any time.
</excerpt>
### Rank 4 of 201 — 0.66
<excerpt title="Lessons Learned Review of the Airport Critical Infrastructure Program">
## Introduction
### Program design and delivery
Overall, ACIP funding was intended to enable investments in critical infrastructure projects that would continue through the pandemic and would support the recovery of the air sector through:
*   Uninterrupted implementation of projects to ensure continued safety and security, including compliance with standards and regulatory requirements  
*   Helping airports mitigate the financial impact of the pandemic  
*   Helping airports to avoid increasing passenger fees to pay for infrastructure projects  
*   Stimulating economic activity through the jobs that ACIP projects would provide  
*   Enabling airports to protect air travelers from the transmission of COVID-19 and help regain Canadians’ confidence in the safety of air travel.
The main Offices of Primary Interest (OPIs) at TC responsible for the design of ACIP were Transportation Infrastructure Programs and Air Policy. Program delivery was the responsibility of Transportation Infrastructure Programs. The number of full-time equivalents (FTE) within Transportation Infrastructure Programs that worked on ACIP decreased over time, with a high of 16 in 2021 to a low of 5 in 2024.
ACIP funds up to 50% of the total project cost for ACIP-approved infrastructure projects across four key streams. These include:
1.   safety, which encompasses initiatives such as runway rehabilitation, lighting improvements, and the acquisition of firefighting equipment  
2.   security, which involves projects like relocating screening or border checkpoints and enhancing cybersecurity infrastructure  
3.   mass transit, which supports the development of transit stations and other transportation infrastructure connected to airports  
4.   biosecurity, which focuses on infrastructure for COVID-19 testing and screening
Given the immediate need for funding due to the cash flow of some recipient airports, ACIP was designed to be flexible in how it allocated funds. TC could front-load contributions so that recipients could access a larger proportion of funding early in the project cycle. However, TC funding would not exceed 50% of the project’s total cost.

## Introduction
### Program design and delivery
#### ACIP projects and funding
ACIP received 77 project proposals, of which 53 projects were funded (68% approval rate). As shown in Figure 2, overall, the safety stream had the greatest number of projects and received the highest amount of funding. On a per project basis, the mass transit stream received the highest amount of funding.
**Figure 2. ACIP projects and committed funding by stream**
As of May 2026, 45 projects have been completed. Figure 3 demonstrates the proportion of projects completed by stream. By the time the final project proposal was approved (in February 2022), $568M had been committed out of the available $570M budget (99%).Footnote 4
**Figure 3. Project completion rate as of Spring 2026 (%)**
ACIP’s contribution budget of $570M (including the additional $82M added for biosecurity projects in August 2021) was intended for eligible recipients according to the following criteria:
*   National Airport System (NAS) airports that have annual passenger volumes over 525,000 (as of December 2019), are certified (i.e., meet TC safety standards and regulations), and are not eligible for the Airports Capital Assistance Program (ACAP), a program that funds airport capital projects, on a cost-sharing basis, for airports with less than 525,000 annual passengers.  
*   Specific non-NAS airports (Abbotsford, Fort McMurray, TradePort International Corporation - Hamilton International Airport, and Ports Toronto - Billy Bishop Toronto City Airport) whose passenger volumes make them ineligible for ACAP.
Figure 4 presents the number of projects completed and funding disbursed by year. Many projects span several years from launch to final claim. Projects are counted in the year that they were completed, and the financial data represents the project’s total cost at the time of their final claim payment. ACIP funding, however, would have been paid incrementally over the duration of the project.
</excerpt>
### Rank 5 of 201 — 0.63
<excerpt title="Lessons Learned Review of the Airport Critical Infrastructure Program">
## Findings
### Relevance
#### Finding 2: ACIP was complementary to, and not duplicative of, other TC programs that provide funding to airports.
Several airports received funding from other TC airport funding programs. These programs are listed in Table 1. Strategically, ACIP addressed gaps in existing TC airport infrastructure funding programs by enabling previously ineligible high-traffic airports - like Pearson International Airport, Vancouver International Airport, and Montreal-Trudeau International Airport - to access infrastructure funding that was unavailable through ACAP due to passenger volume thresholds. In addition, many ACIP-eligible airports were not eligible for highly targeted airport funding programs like the Remote Air Services Program (RASP).
**Table 1. Other TC airport funding programs**

## Findings
### Relevance
#### Finding 2: ACIP was complementary to, and not duplicative of, other TC programs that provide funding to airports.
| **TC Program** | **Description** |  
| --- | --- |  
| Airports Capital Assistance Program (ACAP) | Launched in 1995 to fund rehabilitation projects in airports of lessthan 525,000 passengers per year. Larger airports (over 525,000 passengers) that qualify for ACIP do not qualify for ACAP. |  
| Airport Relief Fund | Committed $64.8M in 2021-22 to airports with revenues of less than $250M in 2019 to maintain operations and mitigate the risk of insolvency. |  
| Short Term Rent Relief | Offered tiered relief for different sizes of airports: * Waived rent and equivalent charges for small airports (less than 1M passengers per year) for the 2021 to 2023 lease years * Waived rent and equivalent charges for medium airports (between 1M and 10M passengers per year) for the 2021 lease year * Deferred rent for large airports (more than 10M passengers per year) from 2021 to 2024, at which point repayments would take place over a 10-year period. |  
| Remote Air Services Program (RASP) | * RASP was launched in spring 2020 after COVID-19 caused severe revenue losses for air carriers serving remote communities, threatening service continuity. * Transport Canada identified about 140 remote communities that rely on air service as their only practical year-round mode of transportation. * 21 core small carriers provided scheduled flights to transport essential workers, people requiring medical services, food, supplies, medicines, and medical testing materials. |  
| National Trade Corridors Fund (NTCF) | Launched in 2017, this program offers $4.3B to improve the efficiency, fluidity, and resiliency of trade corridors and supply chains. |
</excerpt>

## Search 8 — query: "Transport Canada ACIP eligible airports list 2021 pdf"
### Rank 1 of 147 — 0.54 (passed on)
<excerpt title="Lessons Learned Review of the Airport Critical Infrastructure Program">
## Introduction
### Program design and delivery
Overall, ACIP funding was intended to enable investments in critical infrastructure projects that would continue through the pandemic and would support the recovery of the air sector through:
*   Uninterrupted implementation of projects to ensure continued safety and security, including compliance with standards and regulatory requirements  
*   Helping airports mitigate the financial impact of the pandemic  
*   Helping airports to avoid increasing passenger fees to pay for infrastructure projects  
*   Stimulating economic activity through the jobs that ACIP projects would provide  
*   Enabling airports to protect air travelers from the transmission of COVID-19 and help regain Canadians’ confidence in the safety of air travel.
The main Offices of Primary Interest (OPIs) at TC responsible for the design of ACIP were Transportation Infrastructure Programs and Air Policy. Program delivery was the responsibility of Transportation Infrastructure Programs. The number of full-time equivalents (FTE) within Transportation Infrastructure Programs that worked on ACIP decreased over time, with a high of 16 in 2021 to a low of 5 in 2024.
ACIP funds up to 50% of the total project cost for ACIP-approved infrastructure projects across four key streams. These include:
1.   safety, which encompasses initiatives such as runway rehabilitation, lighting improvements, and the acquisition of firefighting equipment  
2.   security, which involves projects like relocating screening or border checkpoints and enhancing cybersecurity infrastructure  
3.   mass transit, which supports the development of transit stations and other transportation infrastructure connected to airports  
4.   biosecurity, which focuses on infrastructure for COVID-19 testing and screening
Given the immediate need for funding due to the cash flow of some recipient airports, ACIP was designed to be flexible in how it allocated funds. TC could front-load contributions so that recipients could access a larger proportion of funding early in the project cycle. However, TC funding would not exceed 50% of the project’s total cost.

## Introduction
### Program design and delivery
#### ACIP projects and funding
ACIP received 77 project proposals, of which 53 projects were funded (68% approval rate). As shown in Figure 2, overall, the safety stream had the greatest number of projects and received the highest amount of funding. On a per project basis, the mass transit stream received the highest amount of funding.
**Figure 2. ACIP projects and committed funding by stream**
As of May 2026, 45 projects have been completed. Figure 3 demonstrates the proportion of projects completed by stream. By the time the final project proposal was approved (in February 2022), $568M had been committed out of the available $570M budget (99%).Footnote 4
**Figure 3. Project completion rate as of Spring 2026 (%)**
ACIP’s contribution budget of $570M (including the additional $82M added for biosecurity projects in August 2021) was intended for eligible recipients according to the following criteria:
*   National Airport System (NAS) airports that have annual passenger volumes over 525,000 (as of December 2019), are certified (i.e., meet TC safety standards and regulations), and are not eligible for the Airports Capital Assistance Program (ACAP), a program that funds airport capital projects, on a cost-sharing basis, for airports with less than 525,000 annual passengers.  
*   Specific non-NAS airports (Abbotsford, Fort McMurray, TradePort International Corporation - Hamilton International Airport, and Ports Toronto - Billy Bishop Toronto City Airport) whose passenger volumes make them ineligible for ACAP.
Figure 4 presents the number of projects completed and funding disbursed by year. Many projects span several years from launch to final claim. Projects are counted in the year that they were completed, and the financial data represents the project’s total cost at the time of their final claim payment. ACIP funding, however, would have been paid incrementally over the duration of the project.
</excerpt>
### Rank 2 of 147 — 0.50
<excerpt title="Lessons Learned Review of the Airport Critical Infrastructure Program">
## Introduction
### COVID-19 and its impact on air travel
Initial disruptions to air travel began in January 2020, driven by emerging health concerns and precautionary measures. Canada’s early response included issuing travel advisories and preparing quarantine protocols.
By March 2020, the aviation sector faced a global crisis as countries imposed border closures and travel bans. Airlines worldwide cancelled large volumes of flights and passenger demand collapsed.Footnote 1 Canada closed its borders to most foreign nationals on March 16, 2020, followed by a Canada-U.S. border closure for non-essential travel on March 21, 2020. All international flights coming into Canada were redirected to four airports (i.e., Toronto Pearson International Airport, Vancouver International Airport, Calgary International Airport, and Montréal–Trudeau International Airport).
The most severe and widespread impacts on air travel occurred between March and May 2020. By May, global flight activity had declined by approximately 80% compared to the same period in 2019.Footnote 2 Canada’s international arrivals dropped by over 90%, with strict entry requirements including testing and quarantine.Footnote 3 These measures resulted in an unprecedented contraction in air traffic, severely affecting airport operations and revenues. Passenger traffic across all Canadian airports is displayed in Figure 1.
**Figure 1. Total passengers enplaned and deplaned 2019 to 2024 at all Canadian airports**

## Introduction
### Program background
ACIP is a contribution funding program that was introduced during the COVID-19 pandemic when Canada’s airports were suffering from dramatic decreases in passengers and revenues. It was designed in 2020 and launched in May 2021 to help Canada’s larger airports (525,000+ passengers per year) continue to make critical investments in safety, security, connectivity to mass transit, and biosecurity. Because of declining revenues during the pandemic, infrastructure projects at Canadian airports were at risk of being delayed or cancelled, which would have postponed their potential benefits or permanently reduced an airport’s ability to deliver efficient services to Canadians. For example, opting to temporarily patch a runway or taxiway instead of completing a comprehensive repaving project would be more costly in the long run, with the airport authority having to pay twice – once for the temporary repair and again for the comprehensive rehabilitation. Further, given the drastic decrease in flight activity and the pre-existing construction for some mass transit projects (like Ottawa’s Light Rail Transit expansion) the COVID-19 pandemic provided an ideal window of opportunity to complete significant infrastructure projects.
The duration of the program was initially from fiscal year (FY) 2021-22 to 2025-26 but was extended to 2027-28, in October 2025, to allow time for the completion of major projects that were delayed due to supply chain issues and construction logistics.
ACIP’s calls for proposals opened on May 11, 2021, for the safety, security, and mass transit streams, and on August 13, 2021, for biosecurity. Money for biosecurity was announced in Budget 2021 (in April 2021), after ACIP had been designed and approved. Project proposals and expressions of interest were accepted starting on May 24, 2021. Specifically, applicants were invited to voluntarily submit an EOI to ensure eligibility and for feedback on their project proposal. Following that, applicants submitted a CPP for a funding decision. In practice, some applicants bypassed the EOI and proceeded directly to submitting a CPP.
TC offered information sessions to eligible airports for each application callout. They also organized regular meetings with eligible recipients and encouraged them to contact the ACIP team with questions at any time.
</excerpt>
### Rank 3 of 147 — 0.45
<excerpt title="Lessons Learned Review of the Airport Critical Infrastructure Program">
## Introduction
### Program design and delivery
#### ACIP projects and funding
ACIP received 77 project proposals, of which 53 projects were funded (68% approval rate). As shown in Figure 2, overall, the safety stream had the greatest number of projects and received the highest amount of funding. On a per project basis, the mass transit stream received the highest amount of funding.
**Figure 2. ACIP projects and committed funding by stream**
As of May 2026, 45 projects have been completed. Figure 3 demonstrates the proportion of projects completed by stream. By the time the final project proposal was approved (in February 2022), $568M had been committed out of the available $570M budget (99%).Footnote 4
**Figure 3. Project completion rate as of Spring 2026 (%)**
ACIP’s contribution budget of $570M (including the additional $82M added for biosecurity projects in August 2021) was intended for eligible recipients according to the following criteria:
*   National Airport System (NAS) airports that have annual passenger volumes over 525,000 (as of December 2019), are certified (i.e., meet TC safety standards and regulations), and are not eligible for the Airports Capital Assistance Program (ACAP), a program that funds airport capital projects, on a cost-sharing basis, for airports with less than 525,000 annual passengers.  
*   Specific non-NAS airports (Abbotsford, Fort McMurray, TradePort International Corporation - Hamilton International Airport, and Ports Toronto - Billy Bishop Toronto City Airport) whose passenger volumes make them ineligible for ACAP.
Figure 4 presents the number of projects completed and funding disbursed by year. Many projects span several years from launch to final claim. Projects are counted in the year that they were completed, and the financial data represents the project’s total cost at the time of their final claim payment. ACIP funding, however, would have been paid incrementally over the duration of the project.

## Introduction
### Program design and delivery
#### ACIP projects and funding
The vertical bars in Figure 4 reveal that the largest number of projects, including all biosecurity projects, were completed by 2023-24. The largest amount of ACIP funding was paid to recipients in the following fiscal year, 2024-25, as demonstrated by the trend line.
**Figure 4. Completed projects and ACIP funding per year**
Note that Figure 4 only includes the 45 projects that were completed as of May 2026. At the time of writing, 8 projects were underway but not yet complete.

## Introduction
### Lessons learned review: objective and scope
This review was conducted to address the information needs of TC’s senior management. The general purpose of the review was to collect evidence related to the relevance, effectiveness, design/delivery, and efficiency of ACIP, and to identify any lessons learned that could be used to inform future TC programming. For the full list of review questions, please see Appendix A.
This review covers the period from FY 2021-22 to FY 2024-25, given that the sunset date for the program was originally March 2026.Footnote 5

## Introduction
### Approach and methods
The following research methods and data sources were used to conduct the lessons learned review:

## Introduction
### Approach and methods
#### Document/Literature review
*   Program documents (presentation decks, briefing notes, recipient contribution agreements, final project reports, and cabinet documents), along with a review of the literature related to comparable international airport infrastructure programs.

## Introduction
### Approach and methods
#### Media review
*   News articles, project announcements and updates from the Canadian news media

## Introduction
### Approach and methods
#### Data review and analysis
*   A comprehensive review of ACIP-related data contained in project trackers  
*   Airport passenger volumes and revenues  
*   Building Construction Price Index  
*   ACIP budget and expenditures
</excerpt>
### Rank 4 of 147 — 0.38
<excerpt title="Lessons Learned Review of the Airport Critical Infrastructure Program">
## Findings
### Relevance
#### Finding 2: ACIP was complementary to, and not duplicative of, other TC programs that provide funding to airports.
Several airports received funding from other TC airport funding programs. These programs are listed in Table 1. Strategically, ACIP addressed gaps in existing TC airport infrastructure funding programs by enabling previously ineligible high-traffic airports - like Pearson International Airport, Vancouver International Airport, and Montreal-Trudeau International Airport - to access infrastructure funding that was unavailable through ACAP due to passenger volume thresholds. In addition, many ACIP-eligible airports were not eligible for highly targeted airport funding programs like the Remote Air Services Program (RASP).
**Table 1. Other TC airport funding programs**

## Findings
### Relevance
#### Finding 2: ACIP was complementary to, and not duplicative of, other TC programs that provide funding to airports.
| **TC Program** | **Description** |  
| --- | --- |  
| Airports Capital Assistance Program (ACAP) | Launched in 1995 to fund rehabilitation projects in airports of lessthan 525,000 passengers per year. Larger airports (over 525,000 passengers) that qualify for ACIP do not qualify for ACAP. |  
| Airport Relief Fund | Committed $64.8M in 2021-22 to airports with revenues of less than $250M in 2019 to maintain operations and mitigate the risk of insolvency. |  
| Short Term Rent Relief | Offered tiered relief for different sizes of airports: * Waived rent and equivalent charges for small airports (less than 1M passengers per year) for the 2021 to 2023 lease years * Waived rent and equivalent charges for medium airports (between 1M and 10M passengers per year) for the 2021 lease year * Deferred rent for large airports (more than 10M passengers per year) from 2021 to 2024, at which point repayments would take place over a 10-year period. |  
| Remote Air Services Program (RASP) | * RASP was launched in spring 2020 after COVID-19 caused severe revenue losses for air carriers serving remote communities, threatening service continuity. * Transport Canada identified about 140 remote communities that rely on air service as their only practical year-round mode of transportation. * 21 core small carriers provided scheduled flights to transport essential workers, people requiring medical services, food, supplies, medicines, and medical testing materials. |  
| National Trade Corridors Fund (NTCF) | Launched in 2017, this program offers $4.3B to improve the efficiency, fluidity, and resiliency of trade corridors and supply chains. |
</excerpt>
### Rank 5 of 147 — 0.36
<excerpt title="Lessons Learned Review of the Airport Critical Infrastructure Program">
## Introduction
### Program background
ACIP is a contribution funding program that was introduced during the COVID-19 pandemic when Canada’s airports were suffering from dramatic decreases in passengers and revenues. It was designed in 2020 and launched in May 2021 to help Canada’s larger airports (525,000+ passengers per year) continue to make critical investments in safety, security, connectivity to mass transit, and biosecurity. Because of declining revenues during the pandemic, infrastructure projects at Canadian airports were at risk of being delayed or cancelled, which would have postponed their potential benefits or permanently reduced an airport’s ability to deliver efficient services to Canadians. For example, opting to temporarily patch a runway or taxiway instead of completing a comprehensive repaving project would be more costly in the long run, with the airport authority having to pay twice – once for the temporary repair and again for the comprehensive rehabilitation. Further, given the drastic decrease in flight activity and the pre-existing construction for some mass transit projects (like Ottawa’s Light Rail Transit expansion) the COVID-19 pandemic provided an ideal window of opportunity to complete significant infrastructure projects.
The duration of the program was initially from fiscal year (FY) 2021-22 to 2025-26 but was extended to 2027-28, in October 2025, to allow time for the completion of major projects that were delayed due to supply chain issues and construction logistics.
ACIP’s calls for proposals opened on May 11, 2021, for the safety, security, and mass transit streams, and on August 13, 2021, for biosecurity. Money for biosecurity was announced in Budget 2021 (in April 2021), after ACIP had been designed and approved. Project proposals and expressions of interest were accepted starting on May 24, 2021. Specifically, applicants were invited to voluntarily submit an EOI to ensure eligibility and for feedback on their project proposal. Following that, applicants submitted a CPP for a funding decision. In practice, some applicants bypassed the EOI and proceeded directly to submitting a CPP.
TC offered information sessions to eligible airports for each application callout. They also organized regular meetings with eligible recipients and encouraged them to contact the ACIP team with questions at any time.

## Introduction
### Program design and delivery
Overall, ACIP funding was intended to enable investments in critical infrastructure projects that would continue through the pandemic and would support the recovery of the air sector through:
*   Uninterrupted implementation of projects to ensure continued safety and security, including compliance with standards and regulatory requirements  
*   Helping airports mitigate the financial impact of the pandemic  
*   Helping airports to avoid increasing passenger fees to pay for infrastructure projects  
*   Stimulating economic activity through the jobs that ACIP projects would provide  
*   Enabling airports to protect air travelers from the transmission of COVID-19 and help regain Canadians’ confidence in the safety of air travel.
The main Offices of Primary Interest (OPIs) at TC responsible for the design of ACIP were Transportation Infrastructure Programs and Air Policy. Program delivery was the responsibility of Transportation Infrastructure Programs. The number of full-time equivalents (FTE) within Transportation Infrastructure Programs that worked on ACIP decreased over time, with a high of 16 in 2021 to a low of 5 in 2024.
ACIP funds up to 50% of the total project cost for ACIP-approved infrastructure projects across four key streams. These include:
1.   safety, which encompasses initiatives such as runway rehabilitation, lighting improvements, and the acquisition of firefighting equipment  
2.   security, which involves projects like relocating screening or border checkpoints and enhancing cybersecurity infrastructure  
3.   mass transit, which supports the development of transit stations and other transportation infrastructure connected to airports  
4.   biosecurity, which focuses on infrastructure for COVID-19 testing and screening
Given the immediate need for funding due to the cash flow of some recipient airports, ACIP was designed to be flexible in how it allocated funds. TC could front-load contributions so that recipients could access a larger proportion of funding early in the project cycle. However, TC funding would not exceed 50% of the project’s total cost.
</excerpt>

## Search 9 — query: ""Airport Critical Infrastructure Program" "eligible airports" Canada 2021 list"
### Rank 1 of 348 — 0.90 (passed on)
<excerpt title="AMCO Study of Airports and Aerodromes">
## [PDF page 89]
The proportion of project costs that are  funded through ACAP decreases  with  hi gher  passenger  
volumes.  For example,  projects airports with between 1,000 and 49,999 annual  enplaned / deplaned  
passengers are eligible for 100% funding, while facilities that serve between 500,000 and 524,999  
passengers are eligible for 5% funding.  Projects eligible under ACAP follow a three-  part prioritization:

## [PDF page 89]
1.  Projects to rehabilitate airside  facilities or buy equipment for aircraft rescue and firefighting.  
Examples include runway and taxiway rehabilitation projects, visual aid and lighting  
replacements, and the acquisition of firefighting equipment;  
2.  Mobile equipment acquisition projects, such  as snow blowers, plows, and tractors; and  
3.  Terminal building safety improvement projects, such as sprinkler upgrades and asbestos  
removal.  
With few exceptions, ACAP is limited to the rehabilitation or replacement of existing assets as opposed  
to the development of new facilities and is confined to infrastructure that is directly associated with air  
carrier operations. A taxiway serving a general aviation hangar row, for example, would be ineligible  
for funding through ACAP.  
C OV ID -19 Program Changes  
In May 2021 during the COVID  -19 pandemic, the federal government announced a series of temporary  
enhancements to ACAP that would apply over a two-  year period, including:  
•  A one-  time increase in annual funding, including  an additional  $93M in 2021-  2022 and $93M  
in 2022  -2023; and  
•  The extension of program eligibility to eight NAS airports serving  few er  than 1M annual  
passengers, including London International Airport and Thunder Bay International Airport in  
Ontario.  
These changes were made recognizing  that  the si gni fi cant financial impacts experienced by regional  
airports had the potential to delay or cancel critical infrastructure rehabilitation and replacement  
projects.  While the future of the C OV ID  -19 pandemic remains uncertain and  the trajectory of the  
financial recovery of Ontario’s airports is  unclear as of 2022, the pandemic-related ACAP changes  
described above have not been announced for continuation past 2022-  2023  and the program is  
expected to return to its pre-  pandemic $38M annual budget.

## [PDF page 89]
9.1.2  Airport Critical Infrastructure Program  
The Airport Critical Infrastructure Program was announced in May 2021 as a temporary program in  
response to the COVID-19 pandemic, with $490M in funding to be made available over a five-  y e ar  
period. ACIP eligible airports include NAS and  non-NAS airports that served more than 525,000  
passengers in 2019 –  in Ontario, this includes six airports: Toronto Pearson International Airport,  
Ottawa International Airport, London International Airport, Thunder Bay International Airport, Hamilton  
International Airport, and Billy Bishop Toronto City Airport. Under ACIP, eligible projects include safety-  
related initiatives, projects to improve operational efficiency or security, and rapid transit connectivity  
projects.  
ACIP is a temporary program and its renewal has not been announced beyond the terms of the $490M  
five-year period  set to expire in 2026.
Study of Ontario’s Airports and Aerodromes Airport Management Council of Ontario  74
</excerpt>
### Rank 2 of 348 — 0.86
<excerpt title="AMCO Study of Airports and Aerodromes">
## [PDF page 89]
9.1.2  Airport Critical Infrastructure Program  
The Airport Critical Infrastructure Program was announced in May 2021 as a temporary program in  
response to the COVID-19 pandemic, with $490M in funding to be made available over a five-  y e ar  
period. ACIP eligible airports include NAS and  non-NAS airports that served more than 525,000  
passengers in 2019 –  in Ontario, this includes six airports: Toronto Pearson International Airport,  
Ottawa International Airport, London International Airport, Thunder Bay International Airport, Hamilton  
International Airport, and Billy Bishop Toronto City Airport. Under ACIP, eligible projects include safety-  
related initiatives, projects to improve operational efficiency or security, and rapid transit connectivity  
projects.  
ACIP is a temporary program and its renewal has not been announced beyond the terms of the $490M  
five-year period  set to expire in 2026.
Study of Ontario’s Airports and Aerodromes Airport Management Council of Ontario  74

## [PDF page 90]
9.1.3  Regional Air T ransportation Initiative  
In 2021, the federal government made a one-  time announcement of $206M in funding on a national  
scale for the  Regional Air Transportation Initiative. In Ontario, RATI is administered through the two  
R egi onal  Development Agencies: FedDev Ontario and FedNor Ontario. RATI was opened to regional  
and local airports that support air service connectivity, with an emphasis on facilities that support  
scheduled passenger air services that were negatively impacted by the COVID-19 pandemic.  
The RATI program targets projects that will result in increased regional air transportation connectivity,  
address the cash flow needs of airports negatively impacted by the COVID-19 pandemic, and / or  
adapt or modernize airport operations. Although applications were prioritized according to the degree  
to which they achieve the program aims, mandatory criteria  regarding certification or minimum activity  
levels were not used. As a result, a wide range of airports in Ontario have benefited from RATI funding,  
including Community airports such as Tillsonburg and St. Thomas, Regional Passenger facilities such  
as Sarnia, and Northern & Remote facilities such as Wawa. Projects advanced through RATI funding  
have included terminal building modernizations, master planning and air service data collection  
studies, capital construction projects, and mobile equipment replacement projects.  
The RATI program is fully subscribed as of May 2022 and its reopening for additional applications  has  
not been announced.
</excerpt>
### Rank 3 of 348 — 0.69
<excerpt title="Lessons Learned Review of the Airport Critical Infrastructure Program">
## Introduction
### COVID-19 and its impact on air travel
Initial disruptions to air travel began in January 2020, driven by emerging health concerns and precautionary measures. Canada’s early response included issuing travel advisories and preparing quarantine protocols.
By March 2020, the aviation sector faced a global crisis as countries imposed border closures and travel bans. Airlines worldwide cancelled large volumes of flights and passenger demand collapsed.Footnote 1 Canada closed its borders to most foreign nationals on March 16, 2020, followed by a Canada-U.S. border closure for non-essential travel on March 21, 2020. All international flights coming into Canada were redirected to four airports (i.e., Toronto Pearson International Airport, Vancouver International Airport, Calgary International Airport, and Montréal–Trudeau International Airport).
The most severe and widespread impacts on air travel occurred between March and May 2020. By May, global flight activity had declined by approximately 80% compared to the same period in 2019.Footnote 2 Canada’s international arrivals dropped by over 90%, with strict entry requirements including testing and quarantine.Footnote 3 These measures resulted in an unprecedented contraction in air traffic, severely affecting airport operations and revenues. Passenger traffic across all Canadian airports is displayed in Figure 1.
**Figure 1. Total passengers enplaned and deplaned 2019 to 2024 at all Canadian airports**

## Introduction
### Program background
ACIP is a contribution funding program that was introduced during the COVID-19 pandemic when Canada’s airports were suffering from dramatic decreases in passengers and revenues. It was designed in 2020 and launched in May 2021 to help Canada’s larger airports (525,000+ passengers per year) continue to make critical investments in safety, security, connectivity to mass transit, and biosecurity. Because of declining revenues during the pandemic, infrastructure projects at Canadian airports were at risk of being delayed or cancelled, which would have postponed their potential benefits or permanently reduced an airport’s ability to deliver efficient services to Canadians. For example, opting to temporarily patch a runway or taxiway instead of completing a comprehensive repaving project would be more costly in the long run, with the airport authority having to pay twice – once for the temporary repair and again for the comprehensive rehabilitation. Further, given the drastic decrease in flight activity and the pre-existing construction for some mass transit projects (like Ottawa’s Light Rail Transit expansion) the COVID-19 pandemic provided an ideal window of opportunity to complete significant infrastructure projects.
The duration of the program was initially from fiscal year (FY) 2021-22 to 2025-26 but was extended to 2027-28, in October 2025, to allow time for the completion of major projects that were delayed due to supply chain issues and construction logistics.
ACIP’s calls for proposals opened on May 11, 2021, for the safety, security, and mass transit streams, and on August 13, 2021, for biosecurity. Money for biosecurity was announced in Budget 2021 (in April 2021), after ACIP had been designed and approved. Project proposals and expressions of interest were accepted starting on May 24, 2021. Specifically, applicants were invited to voluntarily submit an EOI to ensure eligibility and for feedback on their project proposal. Following that, applicants submitted a CPP for a funding decision. In practice, some applicants bypassed the EOI and proceeded directly to submitting a CPP.
TC offered information sessions to eligible airports for each application callout. They also organized regular meetings with eligible recipients and encouraged them to contact the ACIP team with questions at any time.
</excerpt>
### Rank 4 of 348 — 0.69
<excerpt title="Lessons Learned Review of the Airport Critical Infrastructure Program">
## Introduction
### Program design and delivery
Overall, ACIP funding was intended to enable investments in critical infrastructure projects that would continue through the pandemic and would support the recovery of the air sector through:
*   Uninterrupted implementation of projects to ensure continued safety and security, including compliance with standards and regulatory requirements  
*   Helping airports mitigate the financial impact of the pandemic  
*   Helping airports to avoid increasing passenger fees to pay for infrastructure projects  
*   Stimulating economic activity through the jobs that ACIP projects would provide  
*   Enabling airports to protect air travelers from the transmission of COVID-19 and help regain Canadians’ confidence in the safety of air travel.
The main Offices of Primary Interest (OPIs) at TC responsible for the design of ACIP were Transportation Infrastructure Programs and Air Policy. Program delivery was the responsibility of Transportation Infrastructure Programs. The number of full-time equivalents (FTE) within Transportation Infrastructure Programs that worked on ACIP decreased over time, with a high of 16 in 2021 to a low of 5 in 2024.
ACIP funds up to 50% of the total project cost for ACIP-approved infrastructure projects across four key streams. These include:
1.   safety, which encompasses initiatives such as runway rehabilitation, lighting improvements, and the acquisition of firefighting equipment  
2.   security, which involves projects like relocating screening or border checkpoints and enhancing cybersecurity infrastructure  
3.   mass transit, which supports the development of transit stations and other transportation infrastructure connected to airports  
4.   biosecurity, which focuses on infrastructure for COVID-19 testing and screening
Given the immediate need for funding due to the cash flow of some recipient airports, ACIP was designed to be flexible in how it allocated funds. TC could front-load contributions so that recipients could access a larger proportion of funding early in the project cycle. However, TC funding would not exceed 50% of the project’s total cost.

## Introduction
### Program design and delivery
#### ACIP projects and funding
ACIP received 77 project proposals, of which 53 projects were funded (68% approval rate). As shown in Figure 2, overall, the safety stream had the greatest number of projects and received the highest amount of funding. On a per project basis, the mass transit stream received the highest amount of funding.
**Figure 2. ACIP projects and committed funding by stream**
As of May 2026, 45 projects have been completed. Figure 3 demonstrates the proportion of projects completed by stream. By the time the final project proposal was approved (in February 2022), $568M had been committed out of the available $570M budget (99%).Footnote 4
**Figure 3. Project completion rate as of Spring 2026 (%)**
ACIP’s contribution budget of $570M (including the additional $82M added for biosecurity projects in August 2021) was intended for eligible recipients according to the following criteria:
*   National Airport System (NAS) airports that have annual passenger volumes over 525,000 (as of December 2019), are certified (i.e., meet TC safety standards and regulations), and are not eligible for the Airports Capital Assistance Program (ACAP), a program that funds airport capital projects, on a cost-sharing basis, for airports with less than 525,000 annual passengers.  
*   Specific non-NAS airports (Abbotsford, Fort McMurray, TradePort International Corporation - Hamilton International Airport, and Ports Toronto - Billy Bishop Toronto City Airport) whose passenger volumes make them ineligible for ACAP.
Figure 4 presents the number of projects completed and funding disbursed by year. Many projects span several years from launch to final claim. Projects are counted in the year that they were completed, and the financial data represents the project’s total cost at the time of their final claim payment. ACIP funding, however, would have been paid incrementally over the duration of the project.
</excerpt>
### Rank 5 of 348 — 0.69
<excerpt title="Air Sector Recovery - Transports Canada">
*   Canada’s air transportation is a major contributor to the national economy and an important source of jobs. Before the COVID-19 pandemic, the sector contributed over $14 billion in real gross domestic product and employed approximately 107,000 Canadians.

*   The impact of the pandemic on the air transportation sector was unprecedented. Following its onset, travel volumes fell by 90% for a year, generating some of the largest revenue and job losses of any major sector.

*   In the wake of these challenges, the Government of Canada took considerable actions to support the air sector:  
    *   In March 2020, the Government of Canada announced Airport Rent Relief from March to December 2020 by waiving rents for the 21 airport authorities that have ground leases with the federal government, as well as Ports Toronto which operates Billy Bishop Toronto City Airport. Additional support was provided from January to December 2023 through a combination of waivers and deferrals.   
    *   In April 2020, the Government of Canada announced up to $17.3 million for Northern Carriers to ensure that essential goods like food and medical supplies could reach communities in the Territories that depend on air transport. The Government announced more funding of up to $174 million in August 2020 to ensure continuity of essential air access to remote communities through bilateral agreements with provinces and territories under the Remote Air Services Program (RASP).  
    *   The Airports Capital Assistance Program (ACAP), which provides up to $38 million per year in funding to small and regional airports to make critical investments in safety-related capital infrastructure, received a one-time top up funding of $186 million for two years from 2021- 2023. During this period, the minimum federal cost share was increased to 50% and the program was expanded to include 8 small federally owned airports. This financial support helped make sure that Canada’s smaller airports could immediately make required safety improvements despite revenue losses due to COVID-19.  
    *   In May 2021, the Airport Relief Fund (ARF) provided $64.8 million in financial relief to 22 airports struggling with reduced air travel during the COVID-19 pandemic. This helped eligible airports maintain operations and mitigate the risk of insolvency.  
    *   In 2021, the Airport Critical Infrastructure Program (ACIP) was launched to provide over $570 million in funding over 5 years to airports for eligible infrastructure projects related to safety, security, connectivity to mass transit systems, or testing and screening related to COVID-19 and its variants. This funding was allocated to 53 critical infrastructure projects at 19 airports across Canada.  

    *   The Regional Air Transportation Initiative (RATI), delivered by Canada’s Regional Development Agencies (RDAs) in 2021 also provided $206 million over two years to eligible regional businesses and airports that directly contribute to regional air transportation to help maintain regional air connections and services during the pandemic.
</excerpt>

## Search 10 — query: ""Airport Critical Infrastructure Program" eligible airports list 2021 Transport Canada released"
### Rank 1 of 246 — 0.65 (passed on)
<excerpt title="Air Sector Recovery - Transports Canada">
*   Canada’s air transportation is a major contributor to the national economy and an important source of jobs. Before the COVID-19 pandemic, the sector contributed over $14 billion in real gross domestic product and employed approximately 107,000 Canadians.

*   The impact of the pandemic on the air transportation sector was unprecedented. Following its onset, travel volumes fell by 90% for a year, generating some of the largest revenue and job losses of any major sector.

*   In the wake of these challenges, the Government of Canada took considerable actions to support the air sector:  
    *   In March 2020, the Government of Canada announced Airport Rent Relief from March to December 2020 by waiving rents for the 21 airport authorities that have ground leases with the federal government, as well as Ports Toronto which operates Billy Bishop Toronto City Airport. Additional support was provided from January to December 2023 through a combination of waivers and deferrals.   
    *   In April 2020, the Government of Canada announced up to $17.3 million for Northern Carriers to ensure that essential goods like food and medical supplies could reach communities in the Territories that depend on air transport. The Government announced more funding of up to $174 million in August 2020 to ensure continuity of essential air access to remote communities through bilateral agreements with provinces and territories under the Remote Air Services Program (RASP).  
    *   The Airports Capital Assistance Program (ACAP), which provides up to $38 million per year in funding to small and regional airports to make critical investments in safety-related capital infrastructure, received a one-time top up funding of $186 million for two years from 2021- 2023. During this period, the minimum federal cost share was increased to 50% and the program was expanded to include 8 small federally owned airports. This financial support helped make sure that Canada’s smaller airports could immediately make required safety improvements despite revenue losses due to COVID-19.  
    *   In May 2021, the Airport Relief Fund (ARF) provided $64.8 million in financial relief to 22 airports struggling with reduced air travel during the COVID-19 pandemic. This helped eligible airports maintain operations and mitigate the risk of insolvency.  
    *   In 2021, the Airport Critical Infrastructure Program (ACIP) was launched to provide over $570 million in funding over 5 years to airports for eligible infrastructure projects related to safety, security, connectivity to mass transit systems, or testing and screening related to COVID-19 and its variants. This funding was allocated to 53 critical infrastructure projects at 19 airports across Canada.  

    *   The Regional Air Transportation Initiative (RATI), delivered by Canada’s Regional Development Agencies (RDAs) in 2021 also provided $206 million over two years to eligible regional businesses and airports that directly contribute to regional air transportation to help maintain regional air connections and services during the pandemic.
</excerpt>
### Rank 2 of 246 — 0.61
<excerpt title="Keeping Canada Connected: The Challenge of Regional Air Service ...">
## [PDF page 39]
airports, which operate with smaller passenger volumes compared to their larger counterparts. However,  
the program’s temporary two-year term limited its ability to act as a catalyst for air service beyond 2023.  
Airports Capital Assistance Program

## [PDF page 39]
The Airports Capital Assistance Program (ACAP), managed by Transport Canada, began in 1995 and  
has since invested over $1 billion in more than 1,200 projects across over 200 Canadian airports.48F48F49  
ACAP funds rehabilitation projects at local and regional airports that meet specific eligibility criteria,  
including passenger volume thresholds, year-round scheduled services, and federal certification  
standards.49F49F50 The program supports projects such as runway rehabilitation, equipment purchases for  
firefighting and snow removal, and terminal safety improvements.50 F50 F51 Depending on passenger volumes,  
the federal government covers a percentage of project costs, with airports north of the 60th parallel  
receiving a minimum of 85% funding.51 F51 F52 ACAP eligibility is restricted to airports that serve between 1,000  
and 525,000 passengers per year (unless it is a designated “remote” airport) and have regularly  
scheduled commercial passenger services year-round.52F52F53 A temporary expansion to this threshold to 1  
million passengers per year occurred from 2021 to 2023 as part of the government’s COVID-19 response  
for the sector.53F53F54 While ACAP supports regional air service by addressing regional airports’ infrastructure  
needs, its narrow focus on infrastructure and safety-related projects limits its ability to include broader  
service development.  
Airport Critical Infrastructure Program  
Created in 2021, the Airport Critical Infrastructure Program  
(ACIP) is a temporary 5-year federal initiative aimed at  
mitigating the COVID-19 pandemic's impact on larger  
Canadian airports. ACIP complements ACAP by primarily  
supporting airports with annual passenger volumes exceeding  
525,000, where it funds infrastructure projects related to  
safety, efficiency, and transit connections.54F54F55 ACIP can help  
larger regional airports alleviate the cost of critical  
infrastructure that is necessary for the airport to service  
additional passengers and aircraft. Although ACIP has  
supported 19 airports, including 10 regional ones, its
Yellowknife Airport

## [PDF page 39]
49 Airports Capital Assistance Program. Government of Canada. https://tc.canada.ca/en/programs/airports-capital-assistance-  
program  
50 Apply for ACAP funding. Government of Canada. https://tc.canada.ca/en/aviation/operating-airports-aerodromes/apply-acap-  
funding  
51 Ibid.  
52 Information for ACAP applicants. Government of Canada. https://tc.canada.ca/en/aviation/operating-airports-aerodromes/apply-  
acap-funding/information-acap-applicants  
53 Ibid.  
54 Enhancement of the Airports Capital Assistance Program. Transport Canada. https://www.canada.ca/en/transport-  
canada/news/2021/05/enhancement-of-the-airports-capital-assistance-program.html  
55 Airport Critical Infrastructure Program. Transport Canada. https://www.canada.ca/en/transport-canada/news/2021/05/airport-  
critical-infrastructure-program.html
34 | P  a  g  e
PDF link  
PDF link  
PDF link  
PDF link  
PDF link
</excerpt>
### Rank 3 of 246 — 0.61
<excerpt title="Lessons Learned Review of the Airport Critical Infrastructure Program">
## Introduction
### Program design and delivery
Overall, ACIP funding was intended to enable investments in critical infrastructure projects that would continue through the pandemic and would support the recovery of the air sector through:
*   Uninterrupted implementation of projects to ensure continued safety and security, including compliance with standards and regulatory requirements  
*   Helping airports mitigate the financial impact of the pandemic  
*   Helping airports to avoid increasing passenger fees to pay for infrastructure projects  
*   Stimulating economic activity through the jobs that ACIP projects would provide  
*   Enabling airports to protect air travelers from the transmission of COVID-19 and help regain Canadians’ confidence in the safety of air travel.
The main Offices of Primary Interest (OPIs) at TC responsible for the design of ACIP were Transportation Infrastructure Programs and Air Policy. Program delivery was the responsibility of Transportation Infrastructure Programs. The number of full-time equivalents (FTE) within Transportation Infrastructure Programs that worked on ACIP decreased over time, with a high of 16 in 2021 to a low of 5 in 2024.
ACIP funds up to 50% of the total project cost for ACIP-approved infrastructure projects across four key streams. These include:
1.   safety, which encompasses initiatives such as runway rehabilitation, lighting improvements, and the acquisition of firefighting equipment  
2.   security, which involves projects like relocating screening or border checkpoints and enhancing cybersecurity infrastructure  
3.   mass transit, which supports the development of transit stations and other transportation infrastructure connected to airports  
4.   biosecurity, which focuses on infrastructure for COVID-19 testing and screening
Given the immediate need for funding due to the cash flow of some recipient airports, ACIP was designed to be flexible in how it allocated funds. TC could front-load contributions so that recipients could access a larger proportion of funding early in the project cycle. However, TC funding would not exceed 50% of the project’s total cost.

## Introduction
### Program design and delivery
#### ACIP projects and funding
ACIP received 77 project proposals, of which 53 projects were funded (68% approval rate). As shown in Figure 2, overall, the safety stream had the greatest number of projects and received the highest amount of funding. On a per project basis, the mass transit stream received the highest amount of funding.
**Figure 2. ACIP projects and committed funding by stream**
As of May 2026, 45 projects have been completed. Figure 3 demonstrates the proportion of projects completed by stream. By the time the final project proposal was approved (in February 2022), $568M had been committed out of the available $570M budget (99%).Footnote 4
**Figure 3. Project completion rate as of Spring 2026 (%)**
ACIP’s contribution budget of $570M (including the additional $82M added for biosecurity projects in August 2021) was intended for eligible recipients according to the following criteria:
*   National Airport System (NAS) airports that have annual passenger volumes over 525,000 (as of December 2019), are certified (i.e., meet TC safety standards and regulations), and are not eligible for the Airports Capital Assistance Program (ACAP), a program that funds airport capital projects, on a cost-sharing basis, for airports with less than 525,000 annual passengers.  
*   Specific non-NAS airports (Abbotsford, Fort McMurray, TradePort International Corporation - Hamilton International Airport, and Ports Toronto - Billy Bishop Toronto City Airport) whose passenger volumes make them ineligible for ACAP.
Figure 4 presents the number of projects completed and funding disbursed by year. Many projects span several years from launch to final claim. Projects are counted in the year that they were completed, and the financial data represents the project’s total cost at the time of their final claim payment. ACIP funding, however, would have been paid incrementally over the duration of the project.
</excerpt>
### Rank 4 of 246 — 0.58
<excerpt title="Lessons Learned Review of the Airport Critical Infrastructure Program">
## Introduction
### COVID-19 and its impact on air travel
Initial disruptions to air travel began in January 2020, driven by emerging health concerns and precautionary measures. Canada’s early response included issuing travel advisories and preparing quarantine protocols.
By March 2020, the aviation sector faced a global crisis as countries imposed border closures and travel bans. Airlines worldwide cancelled large volumes of flights and passenger demand collapsed.Footnote 1 Canada closed its borders to most foreign nationals on March 16, 2020, followed by a Canada-U.S. border closure for non-essential travel on March 21, 2020. All international flights coming into Canada were redirected to four airports (i.e., Toronto Pearson International Airport, Vancouver International Airport, Calgary International Airport, and Montréal–Trudeau International Airport).
The most severe and widespread impacts on air travel occurred between March and May 2020. By May, global flight activity had declined by approximately 80% compared to the same period in 2019.Footnote 2 Canada’s international arrivals dropped by over 90%, with strict entry requirements including testing and quarantine.Footnote 3 These measures resulted in an unprecedented contraction in air traffic, severely affecting airport operations and revenues. Passenger traffic across all Canadian airports is displayed in Figure 1.
**Figure 1. Total passengers enplaned and deplaned 2019 to 2024 at all Canadian airports**

## Introduction
### Program background
ACIP is a contribution funding program that was introduced during the COVID-19 pandemic when Canada’s airports were suffering from dramatic decreases in passengers and revenues. It was designed in 2020 and launched in May 2021 to help Canada’s larger airports (525,000+ passengers per year) continue to make critical investments in safety, security, connectivity to mass transit, and biosecurity. Because of declining revenues during the pandemic, infrastructure projects at Canadian airports were at risk of being delayed or cancelled, which would have postponed their potential benefits or permanently reduced an airport’s ability to deliver efficient services to Canadians. For example, opting to temporarily patch a runway or taxiway instead of completing a comprehensive repaving project would be more costly in the long run, with the airport authority having to pay twice – once for the temporary repair and again for the comprehensive rehabilitation. Further, given the drastic decrease in flight activity and the pre-existing construction for some mass transit projects (like Ottawa’s Light Rail Transit expansion) the COVID-19 pandemic provided an ideal window of opportunity to complete significant infrastructure projects.
The duration of the program was initially from fiscal year (FY) 2021-22 to 2025-26 but was extended to 2027-28, in October 2025, to allow time for the completion of major projects that were delayed due to supply chain issues and construction logistics.
ACIP’s calls for proposals opened on May 11, 2021, for the safety, security, and mass transit streams, and on August 13, 2021, for biosecurity. Money for biosecurity was announced in Budget 2021 (in April 2021), after ACIP had been designed and approved. Project proposals and expressions of interest were accepted starting on May 24, 2021. Specifically, applicants were invited to voluntarily submit an EOI to ensure eligibility and for feedback on their project proposal. Following that, applicants submitted a CPP for a funding decision. In practice, some applicants bypassed the EOI and proceeded directly to submitting a CPP.
TC offered information sessions to eligible airports for each application callout. They also organized regular meetings with eligible recipients and encouraged them to contact the ACIP team with questions at any time.
</excerpt>
### Rank 5 of 246 — 0.55
<excerpt title="Lessons Learned Review of the Airport Critical Infrastructure Program">
## Introduction
### Program design and delivery
#### ACIP projects and funding
ACIP received 77 project proposals, of which 53 projects were funded (68% approval rate). As shown in Figure 2, overall, the safety stream had the greatest number of projects and received the highest amount of funding. On a per project basis, the mass transit stream received the highest amount of funding.
**Figure 2. ACIP projects and committed funding by stream**
As of May 2026, 45 projects have been completed. Figure 3 demonstrates the proportion of projects completed by stream. By the time the final project proposal was approved (in February 2022), $568M had been committed out of the available $570M budget (99%).Footnote 4
**Figure 3. Project completion rate as of Spring 2026 (%)**
ACIP’s contribution budget of $570M (including the additional $82M added for biosecurity projects in August 2021) was intended for eligible recipients according to the following criteria:
*   National Airport System (NAS) airports that have annual passenger volumes over 525,000 (as of December 2019), are certified (i.e., meet TC safety standards and regulations), and are not eligible for the Airports Capital Assistance Program (ACAP), a program that funds airport capital projects, on a cost-sharing basis, for airports with less than 525,000 annual passengers.  
*   Specific non-NAS airports (Abbotsford, Fort McMurray, TradePort International Corporation - Hamilton International Airport, and Ports Toronto - Billy Bishop Toronto City Airport) whose passenger volumes make them ineligible for ACAP.
Figure 4 presents the number of projects completed and funding disbursed by year. Many projects span several years from launch to final claim. Projects are counted in the year that they were completed, and the financial data represents the project’s total cost at the time of their final claim payment. ACIP funding, however, would have been paid incrementally over the duration of the project.

## Introduction
### Program design and delivery
#### ACIP projects and funding
The vertical bars in Figure 4 reveal that the largest number of projects, including all biosecurity projects, were completed by 2023-24. The largest amount of ACIP funding was paid to recipients in the following fiscal year, 2024-25, as demonstrated by the trend line.
**Figure 4. Completed projects and ACIP funding per year**
Note that Figure 4 only includes the 45 projects that were completed as of May 2026. At the time of writing, 8 projects were underway but not yet complete.

## Introduction
### Lessons learned review: objective and scope
This review was conducted to address the information needs of TC’s senior management. The general purpose of the review was to collect evidence related to the relevance, effectiveness, design/delivery, and efficiency of ACIP, and to identify any lessons learned that could be used to inform future TC programming. For the full list of review questions, please see Appendix A.
This review covers the period from FY 2021-22 to FY 2024-25, given that the sunset date for the program was originally March 2026.Footnote 5

## Introduction
### Approach and methods
The following research methods and data sources were used to conduct the lessons learned review:

## Introduction
### Approach and methods
#### Document/Literature review
*   Program documents (presentation decks, briefing notes, recipient contribution agreements, final project reports, and cabinet documents), along with a review of the literature related to comparable international airport infrastructure programs.

## Introduction
### Approach and methods
#### Media review
*   News articles, project announcements and updates from the Canadian news media

## Introduction
### Approach and methods
#### Data review and analysis
*   A comprehensive review of ACIP-related data contained in project trackers  
*   Airport passenger volumes and revenues  
*   Building Construction Price Index  
*   ACIP budget and expenditures
</excerpt>

# Example 3
## Question
In The Muppet Movie, which actor who cameoed in the county fair scene has at least one star on the Walk of Fame, an Emmy, and a Golden Globe?

## Expected answer
Bob Hope

## Grade 0.00

## Search 1 — query: "The Muppet Movie county fair cameo"
### Rank 1 of 49 — 0.77 (passed on)
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
### Rank 2 of 49 — 0.60
<excerpt title="The Muppet Movie">
Joined by Rowlf the Dog, the Muppets pick up Miss Piggy – who is hitchhiking on the side of the road – and continue their journey; but their car breaks down in the desert. Sitting at a campfire, the group realizes that they will likely miss the auditions the next day. Kermit wanders off, ashamed for bringing his friends on a fruitless journey, but personal reflection restores his commitment. He returns to camp, where he discovers that the Electric Mayhem have come to their rescue, having learned of their plight by reading ahead in the film's script. The Mayhem offer to drive the group the rest of the way in their bus.
The group is warned by a reformed Max that Hopper has hired an assassin, Snake Walker, to kill Kermit. Kermit decides to face his aggressor and proposes a Western-style showdown in a nearby ghost town. There, they find inventor Dr. Bunsen Honeydew and his assistant Beaker. Kermit and his friends are saved when one of Dr. Honeydew's inventions, "insta-grow" pills, enlarges Mayhem drummer Animal, who frightens away Hopper and his henchmen.
Once the Muppets reach the Hollywood studio, they meet executive Lew Lord, who signs them to a "standard 'rich and famous' contract". The first take in their attempt to perform the script goes awry when Gonzo crashes into the prop rainbow, which knocks the scenery down and an explosion blows a hole in the roof of the studio, but a real rainbow shines through the hole and illuminates all the Muppets. Joined by characters from other Henson productions – including _Sesame Street_, _[Emmet Otter's Jug-Band Christmas](https://en.wikipedia.org/wiki/Emmet\_Otter's\_Jug-Band\_Christmas "Emmet Otter's Jug-Band Christmas")_, and _The Land of Gorch_ – the Muppets sing the final verse in a reprise of "Rainbow Connection". As the film ends, Sweetums tears through the screen, elated that he caught up with them.

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
</excerpt>
### Rank 3 of 49 — 0.46
<excerpt title="The Muppet Movie">
| Box office | $76.7 million[[7]](https://en.wikipedia.org/wiki/The_Muppet_Movie#cite_note-8)[[8]](https://en.wikipedia.org/wiki/The_Muppet_Movie#cite_note-9) |
_**The Muppet Movie**_ is a 1979 musicalroadcomedy film, directed by James Frawley and produced by Jim Henson, and the first theatrical film to feature the Muppets. A co-production between the United Kingdom and the United States, the film was written by _The Muppet Show_ writers Jerry Juhl and Jack Burns. Produced during the third season of _The Muppet Show_, the film tells the origin story of the Muppets, as Kermit the Frog embarks on a cross-country trip to Los Angeles, encountering several of the Muppets—who all share the same ambition of finding success in professional show business—along the way while being pursued by Doc Hopper, a greedy restaurateur with intentions of recruiting Kermit to promote his frog legs business.
The film stars Muppet performers Henson, Frank Oz, Jerry Nelson, Richard Hunt, and Dave Goelz, as well as Charles Durning and Austin Pendleton, and it features cameo appearances by Bob Hope, Dom DeLuise, James Coburn, Cloris Leachman, Richard Pryor, Telly Savalas, Edgar Bergen (in his final film appearance before his death), Orson Welles, Madeline Kahn, Milton Berle, Carol Kane, Steve Martin, Mel Brooks, Elliott Gould, and Paul Williams. Notable for its surreal humour, meta-references and prolific use of cameos, _The Muppet Movie_ was released by Associated Film Distribution in the United Kingdom on May 31, 1979, and in the United States on June 22, 1979.
The film received critical praise, including two Academy Award nominations for Paul Williams and Kenneth Ascher's musical score and their song "Rainbow Connection". The film grossed $76.7 million worldwide against an $8 million budget. _The Muppet Movie_ was followed by seven feature films starring the Muppets as well as several more television series and media. In 2009, the film was deemed "culturally, historically, or aesthetically significant" by the Library of Congress and selected for preservation in the National Film Registry.
</excerpt>
### Rank 4 of 49 — 0.31
<excerpt title="The Muppet Movie">
### Special guest stars (in order of appearance)
The closing reprise of "Rainbow Connection" featured a crowd of more than 250 Muppet characters—virtually every Muppet that had been created up to that point in time.[[9]](https://en.wikipedia.org/wiki/The_Muppet_Movie#cite_note-:22-10)[[14]](https://en.wikipedia.org/wiki/The_Muppet_Movie#cite_note-:5-15)[[29]](https://en.wikipedia.org/wiki/The_Muppet_Movie#cite_note-:3-30) According to Henson Archivist Karen Falk, 137 puppeteers were enlisted from the Puppeteers of America (along with the regular Muppets performers) to perform every Muppet extant.[[9]](https://en.wikipedia.org/wiki/The_Muppet_Movie#cite_note-:22-10)[[29]](https://en.wikipedia.org/wiki/The_Muppet_Movie#cite_note-:3-30) Prior to the day-long filming of the shot, Henson gave the enthusiastic participants a lesson in the art of cinematic puppetry. The scene involved 150 puppeteers performing in a pit that was 6 feet (1.8 m) deep and 17 feet (5.2 m) wide.[[9]](https://en.wikipedia.org/wiki/The_Muppet_Movie#cite_note-:22-10)[[29]](https://en.wikipedia.org/wiki/The_Muppet_Movie#cite_note-:3-30) In September 1978, Edgar Bergen, Henson's idol who appeared in a cameo role, died shortly after completing his scenes. Henson was asked by his family to say a few words with Kermit for his memorial service. Henson agreed, and he attended Bergen's memorial service for its speech.[[30]](https://en.wikipedia.org/wiki/The_Muppet_Movie#cite_note-FOOTNOTEDurrett199475-31) Henson dedicated the film to his memory.

### Special guest stars (in order of appearance)
The film's music and lyrics were written by Paul Williams and Kenneth Ascher. Regarding the music's composition, Williams said; "Jim Henson gave you more [creative] freedom than anybody I've ever worked with in my life. I said, 'You want to hear the songs as we're writing them?' He said, 'No. I'll hear them in the studio. I know I'm gonna love them.' You just don't get that kind of freedom on a project these days."[[31]](https://en.wikipedia.org/wiki/The_Muppet_Movie#cite_note-songfacts-32) "Never Before, Never Again" was originally sung by Johnny Mathis, but was changed to Miss Piggy when Jim Henson thought it would be funnier if she sang it to herself.[[29]](https://en.wikipedia.org/wiki/The_Muppet_Movie#cite_note-:3-30) Mathis would later sing the song in the television special _The Muppets Go Hollywood_.[[29]](https://en.wikipedia.org/wiki/The_Muppet_Movie#cite_note-:3-30)
"Movin' Right Along", "Never Before, Never Again", and "I Hope That Somethin' Better Comes Along" were shortened in the film, compared to their soundtrack versions, for continuity purposes._[citation needed_] The latter, a duet between Rowlf and Kermit, contained references that the studio considered too mature for children, although the song appeared complete in the British theatrical and home video debut versions._[citation needed_]
</excerpt>
### Rank 5 of 49 — 0.28
<excerpt title="The Muppet Movie">
| The Muppet Movie |  
| --- |  
| [](https://en.wikipedia.org/wiki/File:The_Muppet_Movie.jpg "A car with various muppets riding it drives forward. Near the bottom of the car is the text \"The Muppet Movie\" in an oval. Above the car is an enlarged illustration of Miss Piggy holding Kermit the Frog.") Theatrical release poster by Drew Struzan |  
| Directed by | James Frawley |  
| Written by | * Jerry Juhl * Jack Burns |  
| Based on | _The Muppet Show_ byJim Henson |  
| Produced by | Jim Henson |  
| Starring | * Jim Henson * Frank Oz * Jerry Nelson * Richard Hunt * Dave Goelz * Charles Durning * Austin Pendleton * Edgar Bergen * Milton Berle * Mel Brooks * James Coburn * Dom DeLuise * Elliott Gould * Bob Hope * Madeline Kahn * Carol Kane * Cloris Leachman * Steve Martin * Richard Pryor * Telly Savalas * Orson Welles * Paul Williams |  
| Cinematography | Isidore Mankofsky |  
| Edited by | Christopher Greenbury |  
| Music by | * Paul Williams * Kenneth Ascher |  
| Production companies | * ITC Entertainment * Henson Associates |  
| Distributed by | ITC Film Distributors Limited[[a]](https://en.wikipedia.org/wiki/The_Muppet_Movie#cite_note-Distribution-4) (United Kingdom and Ireland) Associated Film Distribution[[a]](https://en.wikipedia.org/wiki/The_Muppet_Movie#cite_note-Distribution-4) (North America) |  
| Release dates | * May 31,1979(United Kingdom) * June 22,1979(United States) |  
| Running time | * 97 minutes (UK version)[[4]](https://en.wikipedia.org/wiki/The_Muppet_Movie#cite_note-5) * 95 minutes (US version)[[5]](https://en.wikipedia.org/wiki/The_Muppet_Movie#cite_note-numbers-6) |  
| Countries | * United Kingdom * United States |  
| Language | English |  
| Budget | $8 million[[6]](https://en.wikipedia.org/wiki/The_Muppet_Movie#cite_note-FOOTNOTEJay_Jones2013296-7) |
</excerpt>

## Search 2 — query: "James Coburn Emmy Award"
### Rank 1 of 89 — 0.57 (passed on)
<excerpt title="James Coburn">
### Supporting actor in films
| 1972 | _The Carey Treatment_ | Dr. Peter Carey |  |  
| _The Honkers_ | Lew Lathrop |  |  
| _A Reason to Live, a Reason to Die_ | Colonel Pembroke | Renamed _Massacre at Fort Holman_ for U.S. release |  
| 1973 | _Pat Garrett and Billy the Kid_ | Pat Garrett |  |  
| _The Last of Sheila_ | Clinton Green |  |  
| _Harry in Your Pocket_ | Harry |  |  
| 1974 | _The Internecine Project_ | Robert Elliot |  |  
| 1975 | _Bite the Bullet_ | Luke Matthews |  |  
| _Hard Times_ | Speed |  |  
| _Jackpot_ |  | Unfinished film |  
| 1976 | _Sky Riders_ | Jim McCabe |  |  
| _The Last Hard Men_ | Zach Provo |  |  
| _Midway_ | Captain Vinton Maddox |  |  
| 1977 | _White Rock_ | Narrator |  |  
| _Cross of Iron_ | Sergeant Rolf Steiner |  |  
| 1978 | _California Suite_ | Pilot in Diana Barrie's Film on Airplane | Uncredited |  
| 1979 | _Firepower_ | Fanon |  |  
| _The Muppet Movie_ | El Sleezo Cafe Owner | Cameo |  
| _Goldengirl_ | Jack Dryden |  |  
| 1980 | _The Baltimore Bullet_ | Nick Casey |  |  
| _Loving Couples_ | Dr. Walter Kirby |  |  
| _Mr. Patman_ | Patman |  |  
| 1981 | _High Risk_ | Serrano |  |  
| _Looker_ | John Reston |  |  
| 1985 | _[Martin's Day](https://en.wikipedia.org/wiki/Martin's\_Day "Martin's Day")_ | Lieutenant Lardner |  |  
| 1986 | _Death of a Soldier_ | Major Patrick Dannenberg |  |  
| 1989 | _Train to Heaven_ | Gregorius |  |
</excerpt>
### Rank 2 of 89 — 0.56
<excerpt title="James Coburn — Google Arts & Culture">
James Harrison Coburn III was an American actor who was featured in more than 70 films, largely action roles, and made 100 television appearances during a 45-year career.
Coburn was a capable, rough-hewn leading man, whose toothy grin and lanky physique made him a perfect tough guy in numerous leading and supporting roles in westerns and action films, such as The Magnificent Seven, Hell Is for Heroes; The Great Escape; Charade, Our Man Flint, In Like Flint, The President's Analyst, Hard Times, Duck, You Sucker!, Pat Garrett and Billy the Kid, and Cross of Iron. In 1997, Coburn won an Academy Award for his supporting role as Glen Whitehouse in Affliction. In 2002, he received a Primetime Emmy Award for Outstanding Miniseries nomination for producing The Mists of Avalon.
During the New Hollywood era, Coburn cultivated an image synonymous with "cool" and, along with such contemporaries as Lee Marvin, Steve McQueen, Charles Bronson, and Clint Eastwood, he became one of the most prominent "tough-guy" actors of his day.

### Discover this historical figure


## “Taking in and blowing out smoke? And now you see girls smoking cigars. It got to be such a fad. Girls on the covers of magazines, smoking cigars. Give me a break. I didn't want to be a part of that. I don't like 'popular'.”
James Coburn
Aug 31, 1928 - Nov 18, 2002
</excerpt>
### Rank 3 of 89 — 0.53
<excerpt title="Remembering today, James Coburn 🕯️ On what would have been his ...">
# Disney Dave - Remembering today, James Coburn 🕯️ On what... | Facebook
## Disney Dave's Post
He was a great actor. Happy heavenly birthday James Coburn.
*   [11w](https://www.facebook.com/disneydaveukwdwinfo/posts/pfbid02rAFneZBUWQFRVRZCjsLJVqPPaEEZ6SRs78Zw158gmvStHszFd2z543jpYpReuX4kl?comment_id=918357147548517&__cft__[0]=AZhhhHca5bxt0AJGk8Ju_qi9yc2s1KDeVNzCTJME8RDTXerYbQ5UdlcO58NJ3OKiVG0RZN1OEMea2BPmpk4lwEbh62g3eDo_da9Z04LUTlGf7cdZrLDnrDjJ_GD3O4jSF5RzKo6bNhiQtdk1Iy5LoJlp4Er4TOaD&__tn__=R]-R)
[](https://www.facebook.com/gerard.gianoli.ii?comment_id=Y29tbWVudDoxNjc4NDYyNjc3NjE1MDY5XzEzNDgwNjk2MDc0MDcyMDQ%3D&__cft__[0]=AZhhhHca5bxt0AJGk8Ju_qi9yc2s1KDeVNzCTJME8RDTXerYbQ5UdlcO58NJ3OKiVG0RZN1OEMea2BPmpk4lwEbh62g3eDo_da9Z04LUTlGf7cdZrLDnrDjJ_GD3O4jSF5RzKo6bNhiQtdk1Iy5LoJlp4Er4TOaD&__tn__=R]-R)

# Disney Dave - Remembering today, James Coburn 🕯️ On what... | Facebook
## Disney Dave's Post
[Gerard Gianoli II](https://www.facebook.com/gerard.gianoli.ii?comment_id=Y29tbWVudDoxNjc4NDYyNjc3NjE1MDY5XzEzNDgwNjk2MDc0MDcyMDQ%3D&__cft__[0]=AZhhhHca5bxt0AJGk8Ju_qi9yc2s1KDeVNzCTJME8RDTXerYbQ5UdlcO58NJ3OKiVG0RZN1OEMea2BPmpk4lwEbh62g3eDo_da9Z04LUTlGf7cdZrLDnrDjJ_GD3O4jSF5RzKo6bNhiQtdk1Iy5LoJlp4Er4TOaD&__tn__=R]-R)
He was involved in The Muppet Show and The Muppet Movie.
*   [11w](https://www.facebook.com/disneydaveukwdwinfo/posts/pfbid02rAFneZBUWQFRVRZCjsLJVqPPaEEZ6SRs78Zw158gmvStHszFd2z543jpYpReuX4kl?comment_id=1348069607407204&__cft__[0]=AZhhhHca5bxt0AJGk8Ju_qi9yc2s1KDeVNzCTJME8RDTXerYbQ5UdlcO58NJ3OKiVG0RZN1OEMea2BPmpk4lwEbh62g3eDo_da9Z04LUTlGf7cdZrLDnrDjJ_GD3O4jSF5RzKo6bNhiQtdk1Iy5LoJlp4Er4TOaD&__tn__=R]-R)
1
</excerpt>
### Rank 4 of 89 — 0.50
<excerpt title="James Coburn">
| James Coburn |  
| --- |  
|  Coburn as Anthony Wayne in _The Californians_ (1959) |  
| Born | James Harrison Coburn III August 31, 1928 Laurel, Nebraska, U.S. |  
| Died | November 18, 2002 (aged 74) Beverly Hills, California, U.S. |  
| Resting place | Pierce Brothers Westwood Village Memorial Park and Mortuary |  
| Education | Los Angeles City College |  
| Occupation | Actor |  
| Years active | 1953–2002 |  
| Spouses | Beverly Kelly ​ ​ (m.1959;div.1979)​ Paula Murad ​ (m.1993)​ |  
| Children | 2 |  
| Awards | Academy Award for Best Supporting Actor – _Affliction_ (1997) |
**James Harrison Coburn III**[[1]](https://en.wikipedia.org/wiki/James_Coburn#cite_note-info-1) (August 31, 1928– November 18, 2002) was an American actor who featured in more than 70 films, largely action roles, and made 100 television appearances during a 45-year career.[[2]](https://en.wikipedia.org/wiki/James_Coburn#cite_note-amgbio-2)

Coburn was in numerous leading roles in Westerns and action films.[[3]](https://en.wikipedia.org/wiki/James_Coburn#cite_note-3) He had starring roles in _The Magnificent Seven_, _Hell Is for Heroes_, _The Great Escape_, _Charade_ and _Hard Times_ as well as the lead role in _Our Man Flint_ and its sequel _In Like Flint_, _[The President's Analyst](https://en.wikipedia.org/wiki/The\_President's\_Analyst "The President's Analyst")_, _Duck, You Sucker!_, _Pat Garrett and Billy the Kid_, and _Cross of Iron_. In 1998, Coburn won an Academy Award for his supporting role as Glen Whitehouse in _Affliction_. In 2002, he received a Primetime Emmy Award for Outstanding Miniseries nomination for producing _The Mists of Avalon_.[[4]](https://en.wikipedia.org/wiki/James_Coburn#cite_note-4)
During the New Hollywood era, he cultivated an image synonymous with "cool".[[5]](https://en.wikipedia.org/wiki/James_Coburn#cite_note-5)
James Harrison Coburn III was born in Laurel, Nebraska, on August 31, 1928, the son of James Harrison Coburn II (1902–1975) and Mylet S. Coburn (_née_ Johnson; 1900–1984). His father and namesake was of Scots-Irish ancestry and his mother was of Swedish ancestry. Her parents emigrated from Sweden. James' father had a garage business in Laurel that was destroyed by the Great Depression.[[6]](https://en.wikipedia.org/wiki/James_Coburn#cite_note-6) Coburn was raised in Compton, California, where he attended Compton Junior College.
In 1950, Coburn was drafted into the U.S. Army, where he served as a truck driver and occasionally a disc jockey on an Army radio station in Texas. He also narrated Army training films in Mainz, West Germany.[[7]](https://en.wikipedia.org/wiki/James_Coburn#cite_note-7)

He attended Los Angeles City College,[[8]](https://en.wikipedia.org/wiki/James_Coburn#cite_note-obituary-8) where he studied acting with fellow actor Jeff Corey under Stella Adler's tutelage, and later made his stage debut at the La Jolla Playhouse in Herman Melville's _Billy Budd_.[[9]](https://en.wikipedia.org/wiki/James_Coburn#cite_note-9)
</excerpt>
### Rank 5 of 89 — 0.42
<excerpt title="James Coburn | Emmy Awards and Nominations">
# James Coburn
#### Features
##### Online Originals
Governor Spotlight
Online Originals
Governor Spotlight

# James Coburn
#### Features
##### News
Academy News
Awards News
Member News
Televerse News
Foundation News
Press Releases
In Memoriam
News
Academy News
Awards News
Member News
Televerse News
Foundation News
Press Releases
In Memoriam

# James Coburn
#### Features
##### Media
Photo Library
Video Library
Viewing Platform
Search All Videos
Media
Photo Library
Video Library
Viewing Platform
Search All Videos

# James Coburn
#### Awards
##### Awards
Nominees/Winners
Awards Search
Awards News
Awards FAQs
Awards Calendar
Downloads
Awards
Nominees/Winners
Awards Search
Awards News
Awards FAQs
Awards Calendar
Downloads

# James Coburn
#### Awards
##### Emmy Awards
Emmy Awards Show
Backstage LIVE!
Creative Arts Emmys Show
Emmy Awards Search
Emmy Rules & Procedures
Nominations
Governors Award
Emmy Awards
Emmy Awards Show
Backstage LIVE!
Creative Arts Emmys Show
Emmy Awards Search
Emmy Rules & Procedures
Nominations
Governors Award

# James Coburn
#### Awards
##### Los Angeles Area Emmy Awards
Nominees
Rules & Procedures
Awards Calendar
Los Angeles Area Emmy Awards
Nominees
Rules & Procedures
Awards Calendar

# James Coburn
#### Awards
##### Engineering, Science & Technology Emmy Awards
Engineering, Science & Technology Emmy Awards

# James Coburn
#### Awards
##### Television Academy Honors
Television Academy Honors

# James Coburn
#### Awards
##### Hall of Fame
Hall of Fame

# James Coburn
#### Awards
##### College Television Awards
College Television Awards

# James Coburn
#### Awards
##### Bob Hope Humanitarian Award
Bob Hope Humanitarian Award

# James Coburn
#### Awards
##### Legacy Award
Legacy Award

# James Coburn
#### Academy
##### About the Academy
From the Chair
Frequently Asked Questions
The Emmy Statuette
History
Careers
About the Academy
From the Chair
Frequently Asked Questions
The Emmy Statuette
History
Careers

# James Coburn
#### Academy
##### Organization
Board of Governors
Executive Committee
Committees
Executive Staff
Corporate Partners
Peer Groups
Organization
Board of Governors
Executive Committee
Committees
Executive Staff
Corporate Partners
Peer Groups

# James Coburn
#### Academy
##### Advocacy
Advocacy

# James Coburn
#### Academy
##### Diversity, Equity, Inclusion & Accessibility
Diversity, Equity, Inclusion & Accessibility

# James Coburn
#### Academy
##### Corporate Partners
Corporate Partners

# James Coburn
#### Academy
##### Membership
Member Log In
Become a Member
Membership
Member Log In
Become a Member

# James Coburn
#### Academy
##### Contact Us
Document Downloads
Press Downloads
Contact Us
Document Downloads
Press Downloads

# James Coburn
#### Foundation
##### Foundation
Foundation Board
Foundation Staff
Foundation Alumni
Foundation
Foundation Board
Foundation Staff
Foundation Alumni

# James Coburn
#### Foundation
##### Foundation Features
Foundation News
The Take Newsletter
Strategic Impact
Foundation Features
Foundation News
The Take Newsletter
Strategic Impact

# James Coburn
#### Foundation
##### Programs
Internships
Media Educators Conference
The Power of TV
Access: Behind the Screens
Programs
Internships
Media Educators Conference
The Power of TV
Access: Behind the Screens

# James Coburn
#### Foundation
##### Foundation Events
Emmys Golf Classic
Emmys Pickleball Slam
Foundation Events
Emmys Golf Classic
Emmys Pickleball Slam

# James Coburn
#### Foundation
##### Support
Give Today
Ways to Give
Auction
Support
Give Today
Ways to Give
Auction

# James Coburn
#### Foundation
##### The Interviews: An Oral History of Television
The Interviews: An Oral History of Television

# James Coburn
#### Foundation
##### College Television Awards
College Television Awards

# James Coburn
#### Membership
##### Membership
Member Log In
No Invitation Necessary
Become a Member
Peer Group Requirements
Membership Benefits
Membership
Member Log In
No Invitation Necessary
Become a Member
Peer Group Requirements
Membership Benefits
</excerpt>

## Search 3 — query: "Bob Hope Emmy Award"
### Rank 1 of 79 — 0.42 (passed on)
<excerpt title="Bob Hope: The First 90 Years | Emmy Awards and Nominations">
# Bob Hope: The First 90 Years | Emmy Awards and Nominations | Television Academy
## Log In
Hello, nice to see you back!
Log in to your Television Academy account:
Username
Password
Log In...
Forgot Password?
Forgot Username?

# Bob Hope: The First 90 Years | Emmy Awards and Nominations | Television Academy
## Not a member yet?
If you're seeking ways to connect with working television industry professionals, both in front of and behind the camera, joining our organization offers you unparalleled access, benefits and opportunities.
Learn more about Television Academy Membership
If you're ready to join, click below to start the application process.
Join Now
Home>Awards

# Bob Hope: The First 90 Years
Close
Video 3
/
Photo Credit:
Photo Credit:
/
Awards & NominationsNews & Features

# Bob Hope: The First 90 Years
##### 4 Nominations


# Bob Hope: The First 90 Years
##### 1 Emmy
Show Wins Only
Winner

# Bob Hope: The First 90 Years
##### 1 Emmy
###### Outstanding Variety, Music Or Comedy Special - 1993
Bob Hope: The First 90 Years
NBC
Nancy Malone, _Supervising Producer_
LINDA HOPEDon Mischer
Nominee

# Bob Hope: The First 90 Years
##### 1 Emmy
###### Outstanding Individual Achievement In Choreography - 1993
Bob Hope: The First 90 Years
NBC
Don Crichton
Nominee

# Bob Hope: The First 90 Years
##### 1 Emmy
###### Outstanding Individual Achievement In Editing For A Miniseries Or A Special - Multi-Camera Producti - 1993
Bob Hope: The First 90 Years
NBC
HARRY ARENDSDavid BlewittSUSAN EISNEREVE GAGEJAMES R. HARDYFloyd IngramRICK PICCINIROBERT P. SCHNEIDERDouglass M. Stewart Jr.
Nominee

# Bob Hope: The First 90 Years
##### 1 Emmy
###### Outstanding Individual Achievement In Music And Lyrics - 1993
Bob Hope: The First 90 Years
NBC
Ray CharlesBuz Kohan
Television Academy
AcademyFoundationMembershipCareers
Contact
Contact UsFrequently Asked Questions
Press
Press Portal
Policies
Privacy PolicyTrademark PolicyUser AgreementSite Submission RulesCode of Conduct
Website content © Television Academy.
EMMY, EMMYS, and the Emmy Statuette are registered trademarks and/or copyrights Of ATAS and NATAS.
TELEVISION ACADEMY and ACADEMY OF TELEVISION ARTS & SCIENCES are registered trademarks of ATAS.
Close
Back

# Bob Hope: The First 90 Years
#### Features


# Bob Hope: The First 90 Years
#### Awards


# Bob Hope: The First 90 Years
#### Academy


# Bob Hope: The First 90 Years
#### Foundation


# Bob Hope: The First 90 Years
#### Membership


# Bob Hope: The First 90 Years
#### More
##### Explore More


# Bob Hope: The First 90 Years
#### Features
##### Emmy Magazine
Articles
From the Chair
Me and My Emmy
Interviews Archive
Under the Cover
Back Issues
Emmy Magazine
Articles
From the Chair
Me and My Emmy
Interviews Archive
Under the Cover
Back Issues

# Bob Hope: The First 90 Years
#### Features
##### Online Originals
Governor Spotlight
Online Originals
Governor Spotlight

# Bob Hope: The First 90 Years
#### Features
##### News
Academy News
Awards News
Member News
Televerse News
Foundation News
Press Releases
In Memoriam
News
Academy News
Awards News
Member News
Televerse News
Foundation News
Press Releases
In Memoriam

# Bob Hope: The First 90 Years
#### Features
##### Media
Photo Library
Video Library
Viewing Platform
Search All Videos
Media
Photo Library
Video Library
Viewing Platform
Search All Videos
</excerpt>
### Rank 2 of 79 — 0.34
<excerpt title="Bob Hope: The First 90 Years | Emmy Awards and Nominations">
# Bob Hope: The First 90 Years
#### Features
##### Media
Photo Library
Video Library
Viewing Platform
Search All Videos
Media
Photo Library
Video Library
Viewing Platform
Search All Videos

# Bob Hope: The First 90 Years
#### Awards
##### Awards
Nominees/Winners
Awards Search
Awards News
Awards FAQs
Awards Calendar
Downloads
Awards
Nominees/Winners
Awards Search
Awards News
Awards FAQs
Awards Calendar
Downloads

# Bob Hope: The First 90 Years
#### Awards
##### Emmy Awards
Emmy Awards Show
Backstage LIVE!
Creative Arts Emmys Show
Emmy Awards Search
Emmy Rules & Procedures
Nominations
Governors Award
Emmy Awards
Emmy Awards Show
Backstage LIVE!
Creative Arts Emmys Show
Emmy Awards Search
Emmy Rules & Procedures
Nominations
Governors Award

# Bob Hope: The First 90 Years
#### Awards
##### Los Angeles Area Emmy Awards
Nominees
Rules & Procedures
Awards Calendar
Los Angeles Area Emmy Awards
Nominees
Rules & Procedures
Awards Calendar

# Bob Hope: The First 90 Years
#### Awards
##### Engineering, Science & Technology Emmy Awards
Engineering, Science & Technology Emmy Awards

# Bob Hope: The First 90 Years
#### Awards
##### Television Academy Honors
Television Academy Honors

# Bob Hope: The First 90 Years
#### Awards
##### Hall of Fame
Hall of Fame

# Bob Hope: The First 90 Years
#### Awards
##### College Television Awards
College Television Awards

# Bob Hope: The First 90 Years
#### Awards
##### Bob Hope Humanitarian Award
Bob Hope Humanitarian Award

# Bob Hope: The First 90 Years
#### Awards
##### Legacy Award
Legacy Award

# Bob Hope: The First 90 Years
#### Academy
##### About the Academy
From the Chair
Frequently Asked Questions
The Emmy Statuette
History
Careers
About the Academy
From the Chair
Frequently Asked Questions
The Emmy Statuette
History
Careers

# Bob Hope: The First 90 Years
#### Academy
##### Organization
Board of Governors
Executive Committee
Committees
Executive Staff
Corporate Partners
Peer Groups
Organization
Board of Governors
Executive Committee
Committees
Executive Staff
Corporate Partners
Peer Groups

# Bob Hope: The First 90 Years
#### Academy
##### Advocacy
Advocacy

# Bob Hope: The First 90 Years
#### Academy
##### Diversity, Equity, Inclusion & Accessibility
Diversity, Equity, Inclusion & Accessibility

# Bob Hope: The First 90 Years
#### Academy
##### Corporate Partners
Corporate Partners

# Bob Hope: The First 90 Years
#### Academy
##### Membership
Member Log In
Become a Member
Membership
Member Log In
Become a Member

# Bob Hope: The First 90 Years
#### Academy
##### Contact Us
Document Downloads
Press Downloads
Contact Us
Document Downloads
Press Downloads

# Bob Hope: The First 90 Years
#### Foundation
##### Foundation
Foundation Board
Foundation Staff
Foundation Alumni
Foundation
Foundation Board
Foundation Staff
Foundation Alumni

# Bob Hope: The First 90 Years
#### Foundation
##### Foundation Features
Foundation News
The Take Newsletter
Strategic Impact
Foundation Features
Foundation News
The Take Newsletter
Strategic Impact

# Bob Hope: The First 90 Years
#### Foundation
##### Programs
Internships
Media Educators Conference
The Power of TV
Access: Behind the Screens
Programs
Internships
Media Educators Conference
The Power of TV
Access: Behind the Screens

# Bob Hope: The First 90 Years
#### Foundation
##### Foundation Events
Emmys Golf Classic
Emmys Pickleball Slam
Foundation Events
Emmys Golf Classic
Emmys Pickleball Slam

# Bob Hope: The First 90 Years
#### Foundation
##### Support
Give Today
Ways to Give
Auction
Support
Give Today
Ways to Give
Auction

# Bob Hope: The First 90 Years
#### Foundation
##### The Interviews: An Oral History of Television
The Interviews: An Oral History of Television

# Bob Hope: The First 90 Years
#### Foundation
##### College Television Awards
College Television Awards
</excerpt>
### Rank 3 of 79 — 0.33
<excerpt title="Bob Hope: The First 90 Years | Emmy Awards and Nominations">
# Bob Hope: The First 90 Years | Emmy Awards and Nominations | Television Academy
#### Awards
##### Legacy Award
Legacy Award

# Bob Hope: The First 90 Years | Emmy Awards and Nominations | Television Academy
#### Academy
##### About the Academy
From the Chair
Frequently Asked Questions
The Emmy Statuette
History
Careers
About the Academy
From the Chair
Frequently Asked Questions
The Emmy Statuette
History
Careers

# Bob Hope: The First 90 Years | Emmy Awards and Nominations | Television Academy
#### Academy
##### Organization
Board of Governors
Executive Committee
Committees
Executive Staff
Corporate Partners
Peer Groups
Organization
Board of Governors
Executive Committee
Committees
Executive Staff
Corporate Partners
Peer Groups

# Bob Hope: The First 90 Years | Emmy Awards and Nominations | Television Academy
#### Academy
##### Advocacy
Advocacy

# Bob Hope: The First 90 Years | Emmy Awards and Nominations | Television Academy
#### Academy
##### Diversity, Equity, Inclusion & Accessibility
Diversity, Equity, Inclusion & Accessibility

# Bob Hope: The First 90 Years | Emmy Awards and Nominations | Television Academy
#### Academy
##### Corporate Partners
Corporate Partners

# Bob Hope: The First 90 Years | Emmy Awards and Nominations | Television Academy
#### Academy
##### Membership
Member Log In
Become a Member
Membership
Member Log In
Become a Member

# Bob Hope: The First 90 Years | Emmy Awards and Nominations | Television Academy
#### Academy
##### Contact Us
Document Downloads
Press Downloads
Contact Us
Document Downloads
Press Downloads

# Bob Hope: The First 90 Years | Emmy Awards and Nominations | Television Academy
#### Foundation
##### Foundation
Foundation Board
Foundation Staff
Foundation Alumni
Foundation
Foundation Board
Foundation Staff
Foundation Alumni

# Bob Hope: The First 90 Years | Emmy Awards and Nominations | Television Academy
#### Foundation
##### Foundation Features
Foundation News
The Take Newsletter
Strategic Impact
Foundation Features
Foundation News
The Take Newsletter
Strategic Impact

# Bob Hope: The First 90 Years | Emmy Awards and Nominations | Television Academy
#### Foundation
##### Programs
Internships
Media Educators Conference
The Power of TV
Access: Behind the Screens
Programs
Internships
Media Educators Conference
The Power of TV
Access: Behind the Screens

# Bob Hope: The First 90 Years | Emmy Awards and Nominations | Television Academy
#### Foundation
##### Foundation Events
Emmys Golf Classic
Emmys Pickleball Slam
Foundation Events
Emmys Golf Classic
Emmys Pickleball Slam

# Bob Hope: The First 90 Years | Emmy Awards and Nominations | Television Academy
#### Foundation
##### Support
Give Today
Ways to Give
Auction
Support
Give Today
Ways to Give
Auction

# Bob Hope: The First 90 Years | Emmy Awards and Nominations | Television Academy
#### Foundation
##### The Interviews: An Oral History of Television
The Interviews: An Oral History of Television

# Bob Hope: The First 90 Years | Emmy Awards and Nominations | Television Academy
#### Foundation
##### College Television Awards
College Television Awards

# Bob Hope: The First 90 Years | Emmy Awards and Nominations | Television Academy
#### Membership
##### Membership
Member Log In
No Invitation Necessary
Become a Member
Peer Group Requirements
Membership Benefits
Membership
Member Log In
No Invitation Necessary
Become a Member
Peer Group Requirements
Membership Benefits

# Bob Hope: The First 90 Years | Emmy Awards and Nominations | Television Academy
#### Membership
##### Events
Past Events
Screening Room
Events
Past Events
Screening Room

# Bob Hope: The First 90 Years | Emmy Awards and Nominations | Television Academy
#### Membership
##### Governor Spotlight
Governor Spotlight

# Bob Hope: The First 90 Years | Emmy Awards and Nominations | Television Academy
#### Membership
##### Viewing Platform
Viewing Platform
SectionsFeaturesAwardsAcademyFoundationMembership
</excerpt>
### Rank 4 of 79 — 0.32
<excerpt title="Bob Hope: The First 90 Years | Emmy Awards and Nominations">
# Bob Hope: The First 90 Years | Emmy Awards and Nominations | Television Academy
Skip to main content
The people who bring you the Emmys®
SearchMember Log InMore
FeaturesAwardsAcademyFoundationMembership
Close
Back

# Bob Hope: The First 90 Years | Emmy Awards and Nominations | Television Academy
#### Features


# Bob Hope: The First 90 Years | Emmy Awards and Nominations | Television Academy
#### Awards


# Bob Hope: The First 90 Years | Emmy Awards and Nominations | Television Academy
#### Academy


# Bob Hope: The First 90 Years | Emmy Awards and Nominations | Television Academy
#### Foundation


# Bob Hope: The First 90 Years | Emmy Awards and Nominations | Television Academy
#### Membership


# Bob Hope: The First 90 Years | Emmy Awards and Nominations | Television Academy
#### More
##### Explore More


# Bob Hope: The First 90 Years | Emmy Awards and Nominations | Television Academy
#### Features
##### Emmy Magazine
Articles
From the Chair
Me and My Emmy
Interviews Archive
Under the Cover
Back Issues
Emmy Magazine
Articles
From the Chair
Me and My Emmy
Interviews Archive
Under the Cover
Back Issues

# Bob Hope: The First 90 Years | Emmy Awards and Nominations | Television Academy
#### Features
##### Online Originals
Governor Spotlight
Online Originals
Governor Spotlight

# Bob Hope: The First 90 Years | Emmy Awards and Nominations | Television Academy
#### Features
##### News
Academy News
Awards News
Member News
Televerse News
Foundation News
Press Releases
In Memoriam
News
Academy News
Awards News
Member News
Televerse News
Foundation News
Press Releases
In Memoriam

# Bob Hope: The First 90 Years | Emmy Awards and Nominations | Television Academy
#### Features
##### Media
Photo Library
Video Library
Viewing Platform
Search All Videos
Media
Photo Library
Video Library
Viewing Platform
Search All Videos

# Bob Hope: The First 90 Years | Emmy Awards and Nominations | Television Academy
#### Awards
##### Awards
Nominees/Winners
Awards Search
Awards News
Awards FAQs
Awards Calendar
Downloads
Awards
Nominees/Winners
Awards Search
Awards News
Awards FAQs
Awards Calendar
Downloads

# Bob Hope: The First 90 Years | Emmy Awards and Nominations | Television Academy
#### Awards
##### Emmy Awards
Emmy Awards Show
Backstage LIVE!
Creative Arts Emmys Show
Emmy Awards Search
Emmy Rules & Procedures
Nominations
Governors Award
Emmy Awards
Emmy Awards Show
Backstage LIVE!
Creative Arts Emmys Show
Emmy Awards Search
Emmy Rules & Procedures
Nominations
Governors Award

# Bob Hope: The First 90 Years | Emmy Awards and Nominations | Television Academy
#### Awards
##### Los Angeles Area Emmy Awards
Nominees
Rules & Procedures
Awards Calendar
Los Angeles Area Emmy Awards
Nominees
Rules & Procedures
Awards Calendar

# Bob Hope: The First 90 Years | Emmy Awards and Nominations | Television Academy
#### Awards
##### Engineering, Science & Technology Emmy Awards
Engineering, Science & Technology Emmy Awards

# Bob Hope: The First 90 Years | Emmy Awards and Nominations | Television Academy
#### Awards
##### Television Academy Honors
Television Academy Honors

# Bob Hope: The First 90 Years | Emmy Awards and Nominations | Television Academy
#### Awards
##### Hall of Fame
Hall of Fame

# Bob Hope: The First 90 Years | Emmy Awards and Nominations | Television Academy
#### Awards
##### College Television Awards
College Television Awards

# Bob Hope: The First 90 Years | Emmy Awards and Nominations | Television Academy
#### Awards
##### Bob Hope Humanitarian Award
Bob Hope Humanitarian Award

# Bob Hope: The First 90 Years | Emmy Awards and Nominations | Television Academy
#### Awards
##### Legacy Award
Legacy Award
</excerpt>
### Rank 5 of 79 — 0.30
<excerpt title="Bob Hope: The First 90 Years | Emmy Awards and Nominations">
# Bob Hope: The First 90 Years | Emmy Awards and Nominations | Television Academy
#### Membership
##### Viewing Platform
Viewing Platform
SectionsFeaturesAwardsAcademyFoundationMembership

# Bob Hope: The First 90 Years | Emmy Awards and Nominations | Television Academy
#### Membership
##### Emmy Magazine
Articles
From the Chair
Me and My Emmy
Interviews Archive
Under the Cover
Back Issues
Emmy Magazine
Articles
From the Chair
Me and My Emmy
Interviews Archive
Under the Cover
Back Issues

# Bob Hope: The First 90 Years | Emmy Awards and Nominations | Television Academy
#### Membership
##### Online Originals
Governor Spotlight
Online Originals
Governor Spotlight

# Bob Hope: The First 90 Years | Emmy Awards and Nominations | Television Academy
#### Membership
##### News
Academy News
Awards News
Member News
Televerse News
Foundation News
Press Releases
In Memoriam
News
Academy News
Awards News
Member News
Televerse News
Foundation News
Press Releases
In Memoriam

# Bob Hope: The First 90 Years | Emmy Awards and Nominations | Television Academy
#### Membership
##### Media
Photo Library
Video Library
Viewing Platform
Search All Videos
Media
Photo Library
Video Library
Viewing Platform
Search All Videos

# Bob Hope: The First 90 Years | Emmy Awards and Nominations | Television Academy
#### Membership
##### Awards
Nominees/Winners
Awards Search
Awards News
Awards FAQs
Awards Calendar
Downloads
Awards
Nominees/Winners
Awards Search
Awards News
Awards FAQs
Awards Calendar
Downloads

# Bob Hope: The First 90 Years | Emmy Awards and Nominations | Television Academy
#### Membership
##### Emmy Awards
Emmy Awards Show
Backstage LIVE!
Creative Arts Emmys Show
Emmy Awards Search
Emmy Rules & Procedures
Nominations
Governors Award
Emmy Awards
Emmy Awards Show
Backstage LIVE!
Creative Arts Emmys Show
Emmy Awards Search
Emmy Rules & Procedures
Nominations
Governors Award

# Bob Hope: The First 90 Years | Emmy Awards and Nominations | Television Academy
#### Membership
##### Los Angeles Area Emmy Awards
Nominees
Rules & Procedures
Awards Calendar
Los Angeles Area Emmy Awards
Nominees
Rules & Procedures
Awards Calendar

# Bob Hope: The First 90 Years | Emmy Awards and Nominations | Television Academy
#### Membership
##### Engineering, Science & Technology Emmy Awards
Engineering, Science & Technology Emmy Awards

# Bob Hope: The First 90 Years | Emmy Awards and Nominations | Television Academy
#### Membership
##### Television Academy Honors
Television Academy Honors

# Bob Hope: The First 90 Years | Emmy Awards and Nominations | Television Academy
#### Membership
##### Hall of Fame
Hall of Fame

# Bob Hope: The First 90 Years | Emmy Awards and Nominations | Television Academy
#### Membership
##### College Television Awards
College Television Awards

# Bob Hope: The First 90 Years | Emmy Awards and Nominations | Television Academy
#### Membership
##### Bob Hope Humanitarian Award
Bob Hope Humanitarian Award

# Bob Hope: The First 90 Years | Emmy Awards and Nominations | Television Academy
#### Membership
##### Legacy Award
Legacy Award

# Bob Hope: The First 90 Years | Emmy Awards and Nominations | Television Academy
#### Membership
##### About the Academy
From the Chair
Frequently Asked Questions
The Emmy Statuette
History
Careers
About the Academy
From the Chair
Frequently Asked Questions
The Emmy Statuette
History
Careers

# Bob Hope: The First 90 Years | Emmy Awards and Nominations | Television Academy
#### Membership
##### Organization
Board of Governors
Executive Committee
Committees
Executive Staff
Corporate Partners
Peer Groups
Organization
Board of Governors
Executive Committee
Committees
Executive Staff
Corporate Partners
Peer Groups

# Bob Hope: The First 90 Years | Emmy Awards and Nominations | Television Academy
#### Membership
##### Advocacy
Advocacy
</excerpt>

## Search 4 — query: "Telly Savalas Emmy award"
### Rank 1 of 50 — 0.66 (passed on)
<excerpt title="Biography of Telly Savalas, Actor Who Played Detective Kojak">
## Movie Career
Telly Savalas appeared in his first movie _Mad Dog Coll_ in 1961. His work impressed Burt Lancaster who secured Savalas a role in _The Young Savages_. Young Telly was in demand as a character actor. In 1962, he earned an Academy Award nomination for Best Supporting Actor for his role in _Birdman of Alcatraz_ also starring Burt Lancaster. Savalas appeared in the successful medical drama _The Interns_ and its sequel _The New Interns_.
In 1965, Telly Savalas shaved his head to appear as Pontius Pilate in _The Greatest Story Ever Told_. He stayed bald for the rest of his life, and it became a signature part of his appearance as an actor. One of Savalas's most memorable film roles came in 1967 when he appeared in _The Dirty Dozen_ in a role turned down by Jack Palance. After portraying the villain Blofeld in the 1969 James Bond thriller _On Her Majesty's Secret Service_, Savalas received second billing to Clint Eastwood in _Kelly's Heroes_ and Charles Bronson in _Violent City_ in 1970.
Telly Savalas in "On Her Majesty's Secret Service".Silver Screen Collection / Getty Images

## Detective Kojak
Telly Savalas first appeared as Police Detective Lt. Theo Kojak in the spring 1973 TV movie _The Marcus-Nelson Murders_. CBS turned the film into a regular series in the fall of 1973. Detective Kojak was known for enjoying lollipops and his tagline, "Who loves ya, baby?" The show was a Nielsen rating success ranking in the top 10 for its first season and remaining in the top 20 for two more seasons. CBS canceled the series after five seasons but revived it for seven TV movies from 1985 through 1990.
Telly Savalas in "Kojak".Moviepix / Getty Images
Telly Savalas earned Emmy Award nominations for Outstanding Lead Actor in a Drama Series for his role on _Kojak_. He won in 1974. While the series ran, Savalas continued to occasionally appear in movies. After the show's cancellation, he played mostly cameo and supporting roles in films and TV series.

## Personal Life
Telly Savalas married three times. He wed his first wife, his college sweetheart Katherine Nicolaides, in 1948. Their daughter Christina was born in 1950. After a 1957 divorce, he married Marilyn Garden, a theater instructor, in 1960. Together, they had two daughters, Penelope and Candace. Following a long separation, they divorced in 1974.
Savalas began a relationship with actress Sally Adams in 1969. Though they never married, she adopted the name Sally Savalas and gave birth to their son Nicholas in 1973. They ended their relationship in 1978, and Sally sued Telly Savalas for financial support in 1980.
In 1984, Telly Savalas married travel agent Julie Hovland. They had two children, son Christian and daughter Ariana. They remained married for the rest of Savalas's life.

## Later Life and Death
In addition to his acting career, Savalas found success with a spoken-word record of the song "If" originally recorded by the pop group Bread. It reached #1 on the pop charts in the U.K. in 1975. He was also a world-class poker player and owned the successful racehorse Telly's Pop.
In 1988, Telly Savalas received a diagnosis of bladder cancer. He died on January 22, 1994, due to complications of bladder and prostate cancer. He is buried in Los Angeles, California.
</excerpt>
### Rank 2 of 50 — 0.65
<excerpt title="Telly Savalas">
## Awards and nominations
[edit]
| Year | Award | Category | Nominated work | Results | Ref. |  
| --- | --- | --- | --- | --- | --- |  
| 1962 | Academy Awards | Best Supporting Actor | _Birdman of Alcatraz_ | Nominated | [[75]](https://en.wikipedia.org/wiki/Telly_Savalas#cite_note-75) |  
| Golden Globe Awards | Best Supporting Actor – Motion Picture | Nominated | [[76]](https://en.wikipedia.org/wiki/Telly_Savalas#cite_note-76) |  
| 1965 | _Battle of the Bulge_ | Nominated |  
| 1974 | Best Actor in a Television Series – Drama | _Kojak_ | Won |  
| 1975 | Won[[a]](https://en.wikipedia.org/wiki/Telly_Savalas#cite_note-77) |  
| 1976 | Nominated |  
| 1977 | Nominated |  
| 1973 | Primetime Emmy Awards | Outstanding Single Performance by an Actor in a Leading Role | _The Marcus-Nelson Murders_ | Nominated | [[77]](https://en.wikipedia.org/wiki/Telly_Savalas#cite_note-78) |  
| 1974 | Best Lead Actor in a Drama Series | _Kojak_(Episode: "Requiem for a Cop") | Won |  
| 1975 | Outstanding Lead Actor in a Drama Series | _Kojak_ | Nominated |  
| Outstanding Directing in a Drama Series | _Kojak_(Episode: "I Want to Report a Dream...") | Nominated |

## Awards and nominations
*   _This is Telly Savalas..._ (1972)  
*   _Telly_ (1974)  
*   _Telly Savalas_ (1975)  
*   _Who Loves Ya Baby_ (1976)  
*   _Sweet Surprise_ [released on cassette and CD under the title _Some Broken Hearts_] (1980)

*   "Try to Remember" (1972)  
*   "Look Around You" (1972)  
*   "I Don't Want To Know / I Walk The Line" (1972)  
*   "We All End Up The Same" (1972)  
*   "If" (1974)  
*   "[You've Lost That Lovin' Feelin'](https://en.wikipedia.org/wiki/You've_Lost_That_Lovin'_Feelin' "You've Lost That Lovin' Feelin'") / Help Me Make It Through the Night" (1974)  
*   "Who Loves Ya Baby" (1975)  
*   "A Good Time Man Like Me Ain't Got No Business Singing The Blues" (1976)  
*   "Sweet Surprise" (1980)  
*   "Some Broken Hearts Never Mend" (1980)  
*   "Lovin' Understandin' Man" (1981)  
*   "Goodbye Madame" (1982)
1.   ↑Tied with Robert Blake for _Baretta_.
</excerpt>
### Rank 3 of 50 — 0.61
<excerpt title="Biography of Telly Savalas, Actor Who Played Detective Kojak">
Aristotelis "Telly" Savalas (January 21, 1922–January 22, 1994) was an actor best known for his title role in the 1970s _Kojak_ TV series. He earned an Emmy Award for his part in the show. He also had a successful movie career earning an Academy Award nomination for _Birdman of Alcatraz_ in 1962.

### Fast Facts: Telly Savalas
*   **Occupation:**Actor  
*   **Known For**: The role of Detective Lt. Theo Kojak in the 1970s TV drama series _Kojak_  
*   **Born:**January 21, 1922 in Garden City, New York  
*   **Died:**January 22, 1994 in Universal City, California  
*   **Education:**Columbia University  
*   **Key Accomplishment**: Emmy Award for Outstanding Lead Actor in a Drama Series in _Kojak_  
*   **Famous Quote:**"We're all born bald, baby."

## Early Life and Career
As the second of five children born to Greek immigrants Nick and Christina Savalas, Telly Savalas sold newspapers and shined shoes along with his brother Gus to help support the family. When first entering elementary school, Telly only spoke Greek, but he soon learned English. He graduated from high school in Floral Park, New York in 1940.
Telly Savalas served three years in the United States Army during World War II and earned a Purple Heart. After returning home, he studied at Columbia University. During the war, Savalas studied radio and television production. He put that education to use in the 1950s working for Voice of America where he eventually hosted his own talk show _Telly's Coffee Shop_.
In the early 1950s, a Hollywood agent looking for an actor with a French accent called Voice of America, and Telly Savalas answered the phone and faked a French accent. He received the job. The show was called "And Bring Home a Baby," an episode of _Armstrong Circle Theatre_ on CBS in 1958. Savalas appeared as a guest star in multiple TV series until he landed a regular part on the 1961 TV series _Acapulco_.

## Movie Career
Telly Savalas appeared in his first movie _Mad Dog Coll_ in 1961. His work impressed Burt Lancaster who secured Savalas a role in _The Young Savages_. Young Telly was in demand as a character actor. In 1962, he earned an Academy Award nomination for Best Supporting Actor for his role in _Birdman of Alcatraz_ also starring Burt Lancaster. Savalas appeared in the successful medical drama _The Interns_ and its sequel _The New Interns_.
In 1965, Telly Savalas shaved his head to appear as Pontius Pilate in _The Greatest Story Ever Told_. He stayed bald for the rest of his life, and it became a signature part of his appearance as an actor. One of Savalas's most memorable film roles came in 1967 when he appeared in _The Dirty Dozen_ in a role turned down by Jack Palance. After portraying the villain Blofeld in the 1969 James Bond thriller _On Her Majesty's Secret Service_, Savalas received second billing to Clint Eastwood in _Kelly's Heroes_ and Charles Bronson in _Violent City_ in 1970.
Telly Savalas in "On Her Majesty's Secret Service".Silver Screen Collection / Getty Images
</excerpt>
### Rank 4 of 50 — 0.61
<excerpt title="Telly Savalas">
_Kojak_ aired on CBS for five seasons from October 24, 1973, until March 18, 1978, with 118 episodes produced.[[23]](https://en.wikipedia.org/wiki/Telly_Savalas#cite_note-TVGuide-23) The role won Savalas an Emmy and two Golden Globes for Best Actor in a Drama Series. Co-stars on the show included Savalas's younger brother George as Detective Stavros, a sensitive, wild-haired, quiet, comedic foil to Kojak's street-wise humor in an otherwise dark dramatic series,[[34]](https://en.wikipedia.org/wiki/Telly_Savalas#cite_note-34)Kevin Dobson as Kojak's trusted young partner, Det. Bobby Crocker, whose on-screen chemistry with Savalas was a success story of 1970s television,[[35]](https://en.wikipedia.org/wiki/Telly_Savalas#cite_note-35) and Dan Frazer as Captain Frank McNeil.[[36]](https://en.wikipedia.org/wiki/Telly_Savalas#cite_note-36)
Due to a decline in ratings, the series was cancelled by CBS in 1978. Savalas and Frazer were the only actors to appear in all 118 episodes. Savalas was unhappy about the show's demise[[37]](https://en.wikipedia.org/wiki/Telly_Savalas#cite_note-37) but got the chance to reprise the Kojak persona in several television movies, starting in 1985.[[38]](https://en.wikipedia.org/wiki/Telly_Savalas#cite_note-38)[[39]](https://en.wikipedia.org/wiki/Telly_Savalas#cite_note-39) The first film, subtitled _The Belarus File_ and broadcast in February 1985, reunited Savalas with several of his co-stars from the series: younger brother George, Dan Frazer, Mark Russell (Det. Saperstein) and Vince Conti (Det. Rizzo). This marked those actors' final appearances in the _Kojak_ franchise.[[40]](https://en.wikipedia.org/wiki/Telly_Savalas#cite_note-40)[[41]](https://en.wikipedia.org/wiki/Telly_Savalas#cite_note-41)
</excerpt>
### Rank 5 of 50 — 0.59
<excerpt title="Telly Savalas Biography, Celebrity Facts and Awards">
# Telly Savalas
## Fast Facts
*   A long-term resident of the Sheraton-Universal Hotel in Hollywood, the hotel would eventually name their bar after the actor following his death  
*   Died from complications due to cancer of the bladder and prostate  
*   Born to Greek parents, he only spoke Greek until the age of 18 when he learned English after enrolling at Columbia University  
*   Worked for the State Department as a host of "Your Voice of America․"  
*   Det․ Kojak's onscreen affinity for lollipops was originally written into the series to accomodate Savalas' apparent sweet tooth  
*   His most famed role was that of the titular detective on CBS series "Kojak․"  
*   Initially got into the entertainment via network news as the executive producer of the "Gillette Cavalcade of Sports" before venturing to Hollywood to pursue a career in front of the camera  
*   Made more than 50 guest appearances on numerous TV series throughout the '50s and '60s  
*   Godfather of Jennifer Aniston  
*   Was a lifeguard as a teenager, and once failed to save a man from drowning, an event that he claimed haunted him throughout his adult life
* * *

# Telly Savalas
## Awards
*   1963 Oscar - Best Actor in a Supporting Role:Nominated  
*   1963 Golden Globe - Best Supporting Actor:Nominated  
*   1966 Golden Globe - Best Supporting Actor:Nominated  
*   1968 Golden Laurel - Male Supporting Performance:Nominated  
*   1973 Primetime Emmy - Outstanding Single Performance by an Actor in a Leading Role:Nominated  
*   1974 Primetime Emmy - Best Lead Actor in a Drama Series:Winner  
*   1975 Bambi - TV Series International:Winner  
*   1975 Golden Globe - Best TV Actor - Drama:Winner  
*   1975 Primetime Emmy - Outstanding Lead Actor in a Drama Series:Nominated  
*   1975 Primetime Emmy - Outstanding Directing in a Drama Series:Nominated  
*   1976 Golden Globe - Best Actor in a Television Series - Drama:Winner  
*   1976 TP de Oro - Best Foreign Actor (Mejor Actor Extranjero):Winner  
*   1977 Golden Globe - Best Actor in a Television Series - Drama:Nominated  
*   1978 Golden Globe - Best Actor in a Television Series - Drama:Nominated  
*   2005 TV Land Award - Favorite Private Eye:Nominated
* * *
Advertisement
Advertisement
*   Today's Netflix Top 10 Rankings  
*   If You Like This Show...  
*   The 100 Best Shows on TV  
*   Renewed or Canceled?  
*   Editors Pick Your Next Favorite Show
About
*   About TV Guide  
*   Newsletters  
*   Careers  
*   Help Center
Policies
*   Privacy Policy  
*   Terms of Use  
*   Cookie Settings
Get the TV Guide app
App StoreGoogle Play
Follow us
© 2026 TV GUIDE, A FANDOM COMPANY. ALL RIGHTS RESERVED.
</excerpt>

## Search 5 — query: "Telly Savalas walk of fame star"
### Rank 1 of 44 — 0.69 (passed on)
<excerpt title="Telly Savalas">
In the late 1970s, Savalas narrated three UK travelogues titled _Telly Savalas Looks at Portsmouth_, _Telly Savalas Looks at Aberdeen_, and _Telly Savalas Looks at Birmingham_. They were produced by Harold Baim and were examples of quota quickies, which were then part of a requirement that cinemas in the United Kingdom show a set percentage of British-produced films.[[53]](https://en.wikipedia.org/wiki/Telly_Savalas#cite_note-53) In the 1980s and early 1990s, Savalas appeared in commercials for the Players' Club Gold Card. In 1982, along with Bob Hope and Linda Evans, he participated in the "world premiere" television ad introducing Diet Coke to Americans.[[54]](https://en.wikipedia.org/wiki/Telly_Savalas#cite_note-54) On October 28, 1987, Savalas hosted _Return to the Titanic Live_, a two-hour television special broadcast from [Cité des Sciences et de l'Industrie](https://en.wikipedia.org/wiki/Cit%C3%A9_des_Sciences_et_de_l'Industrie "Cité des Sciences et de l'Industrie") in Paris, which was widely criticized as being insensitive and for making light of the tragic sinking soon after its wreck was discovered.[[55]](https://en.wikipedia.org/wiki/Telly_Savalas#cite_note-NYTIMES-55)[[56]](https://en.wikipedia.org/wiki/Telly_Savalas#cite_note-TWP-56) He also hosted the 1989 video _UFOs and Channeling._
He received a star on the Hollywood Walk of Fame in 1983. In 1999, _TV Guide_ ranked him number 18 on its 50 Greatest TV Stars of All Time list.[[57]](https://en.wikipedia.org/wiki/Telly_Savalas#cite_note-57)
The Savalas brothers (l-r): Teddy, Telly, Gus, and George

Savalas was married three times. In 1948, after his father's death from bladder cancer, Savalas married his college sweetheart, Katherine Nicolaides. Their daughter Christina, named after his mother, was born in 1950. In 1957, Katherine filed for divorce. She urged him to move back to his mother's house during that same year.[[14]](https://en.wikipedia.org/wiki/Telly_Savalas#cite_note-NYT94-14)
While Savalas was going broke, he founded the Garden City Theater Center in his native Garden City. While working there, he met Marilyn Gardner, a theater teacher. They married in 1960. Marilyn gave birth to their daughter, Penelope, in 1961. A second daughter, Candace, was born in 1963. They divorced in 1974, after a long separation.[[14]](https://en.wikipedia.org/wiki/Telly_Savalas#cite_note-NYT94-14)
In January 1969, while working on the movie _On Her Majesty's Secret Service_, Savalas met Sally Adams (billed as Dani Sheridan, one of Blofeld's "Angels of Death"), an actress 24 years his junior, whose daughter from a previous relationship is Nicollette Sheridan. Savalas later moved in with Sally, who gave birth to their son Nicholas Savalas on February 24, 1973. Although Savalas and Sally Adams never legally married, she went by the name Sally Savalas.[[58]](https://en.wikipedia.org/wiki/Telly_Savalas#cite_note-bulletin-58) They stopped living together in December 1978. She filed a palimony lawsuit against him in 1980, demanding support for herself, their son, and for Nicollette.[[58]](https://en.wikipedia.org/wiki/Telly_Savalas#cite_note-bulletin-58)
</excerpt>
### Rank 2 of 44 — 0.68
<excerpt title="A proud moment featuring American actor Telly Savalas, kneeling beside ...">
# Instagram
Log In
Sign Up
Never miss a post from hollywoodboxuk
Sign up for Instagram to stay in the loop.
By continuing, you agree to Instagram's Terms of Use and Privacy Policy.
Sign up
Log in
hollywoodboxuk
•
Follow
AI-generated profile
* * *
hollywoodboxuk47w
A proud moment featuring American actor Telly Savalas, kneeling beside his newly dedicated star on the Hollywood Walk of Fame, which he received on October 26, 1983, for his work in motion pictures. The shot shows the actor, best known for his title role in the television series Kojak, wearing a light-colored blazer and smiling at the plaque in his hands, which also bears his name. Savalas also appeared in numerous other notable films, such as The Dirty Dozen and Kelly's Heroes, and was nominated for an Academy Award for his performance in Birdman of Alcatraz.
#tellysavalas#hollywoodwalkoffame#1983#hollywood#actor#icon#kojak#film#movie#tv#redcarpet#celebrity#whoovesyababy

# Instagram
## No comments yet.
Start the conversation.
5
December 20, 2025
Log in to like or comment.
* * *
More posts from hollywoodboxuk
See more posts
* * *
Meta
About
Blog
Jobs
Help
API
Privacy
Terms
Locations
Popular
Instagram Lite
Meta AI
Muse
Threads
Contact Uploading & Non-Users
Meta Verified
English
© 2026 Instagram from Meta
</excerpt>
### Rank 3 of 44 — 0.60
<excerpt title="Telly Savalas getting his star on the Walk of Fame, October 26, 1983.">
# FABULOUS FILMS & STARS | Telly Savalas getting his star on the Walk of Fame, October 26, 1983. | Facebook
Log In
Log In
Forgot Account?
[](https://www.facebook.com/groups/1684044015213864/?__cft__[0]=AZg0g1RNtc4ejqvJVg2brbp2AFzwvOFX55cvN0thB0qtxEgjgMGQrmRhLVef5EXgW165jm2Pep_Lq6-AEnlZJZN-LzvuQYfT9mwuhPnFjJWXLyO8zephFkM40G56P_1TaqJIkn9aNw6eZe3vZWlDd8gie79wVuZLiT7yooONLDaBKE1QRx7YL_TlgoODsPkP&__tn__=%3C%3C%2CP-R)
## [FABULOUS FILMS & STARS](https://www.facebook.com/groups/1684044015213864/?__cft__[0]=AZg0g1RNtc4ejqvJVg2brbp2AFzwvOFX55cvN0thB0qtxEgjgMGQrmRhLVef5EXgW165jm2Pep_Lq6-AEnlZJZN-LzvuQYfT9mwuhPnFjJWXLyO8zephFkM40G56P_1TaqJIkn9aNw6eZe3vZWlDd8gie79wVuZLiT7yooONLDaBKE1QRx7YL_TlgoODsPkP&__tn__=-UC%2CP-R) ·
Join
Denise Cutrone Binder
·
Admin
·
Monday, October 26, 2026 at 8:20 PM

# FABULOUS FILMS & STARS | Telly Savalas getting his star on the Walk of Fame, October 26, 1983. | Facebook
[October 26 at 8:20 PM](https://www.facebook.com/groups/1684044015213864/?multi_permalinks=4849171748701059&hoisted_section_header_type=recently_seen&__cft__[0]=AZg0g1RNtc4ejqvJVg2brbp2AFzwvOFX55cvN0thB0qtxEgjgMGQrmRhLVef5EXgW165jm2Pep_Lq6-AEnlZJZN-LzvuQYfT9mwuhPnFjJWXLyO8zephFkM40G56P_1TaqJIkn9aNw6eZe3vZWlDd8gie79wVuZLiT7yooONLDaBKE1QRx7YL_TlgoODsPkP&__tn__=%2CO%2CP-R) ·
Telly Savalas getting his star on the Walk of Fame, October 26, 1983.
[](https://www.facebook.com/photo/?fbid=30183563211233753&set=gm.4849171748701059&idorvanity=1684044015213864&__cft__[0]=AZg0g1RNtc4ejqvJVg2brbp2AFzwvOFX55cvN0thB0qtxEgjgMGQrmRhLVef5EXgW165jm2Pep_Lq6-AEnlZJZN-LzvuQYfT9mwuhPnFjJWXLyO8zephFkM40G56P_1TaqJIkn9aNw6eZe3vZWlDd8gie79wVuZLiT7yooONLDaBKE1QRx7YL_TlgoODsPkP&__tn__=EH-R)
</excerpt>
### Rank 4 of 44 — 0.59
<excerpt title="Star for Telly Savalas, Hollywood Walk of Fame">
# Star for Telly Savalas, Hollywood Walk of Fame | This star h… | Flickr
Opens in a new window Opens an external website Opens an external website in a new window
This website utilizes technologies such as cookies to enable essential site functionality, as well as for analytics, personalization, and targeted advertising. You may change your settings at any time or accept the default settings. You may close this banner to continue with only essential cookies.   
Your preferences are saved across the devices where you're signed in, and may differ from the choices you make here.
Privacy PolicyCookie Policy  
Storage Preferences
*   - [x] Targeted Advertising   
*   - [x] Personalization   
*   - [x] Analytics
Save Accept All Reject Non-Essential
Storage Preferences
Explore
✨ Get Pro
Log InSign Up
Open main menu
Search
Log InSign Up
Back to photostream
✨Get Pro
PRO
Scarlet SapphoScarlet Sappho
Follow
* * *

# Star for Telly Savalas, Hollywood Walk of Fame
## This star honors storied Greek-American actor **Telly Savalas**, who, among other roles, played **Kojak** as well as one of the renditions of villain **Blofeld** in the **James Bond 007** canon.
I love Savalas for another reason; he was the **godfather** for my Greek Goddess and ultimate idol, **Jennifer Aniston**.
Located close to the Hollywood & Highland Complex.
1,095 views
•3 faves•0 comments
Uploaded on November 7, 2017 Taken on November 1, 2017
Nikon D550018.0-140.0 mm f/3.5-5.6 Show settings
Hollywood Hills West, Los Angeles, California
Protomaps© OpenStreetMap
PRO
Scarlet SapphoFollow
I love Savalas for another reason; he was the **godfather** for my Greek Goddess and ultimate idol, **Jennifer Aniston**.
Located close to the Hollywood & Highland Complex.

# Comments(0)
Show your appreciation with the gift of Flickr Pro
Claudio Castelli, nywheels, and moreska faved this
Add comment
1,095 views
3 faves 0 comments
Uploaded on November 7, 2017 Taken on November 1, 2017
All rights reserved
* * *
Nikon D550018.0-140.0 mm f/3.5-5.6
Aperture ƒ/8.0
Focal length 38 mm
Exposure time 0.003 sec (1/400)
ISO 100
Flash (off, did not fire)
Show EXIF
Hollywood Hills West, Los Angeles, California
Protomaps© OpenStreetMap

# Comments(0)
##### This photo is in 3 albums
*   Ελλάδα Greece: Υπερπόντιος Overseas 32 items  
*   Jennifer Aniston, Greek Goddess 31 items  
*   USA: California, Southern 1277 items
* * *

# Comments(0)
### Tags
Aristotelis SavalasCaliforniaGrauman's Chinese TheatreHollywoodKojakLos AngelesNorth AmericaTCL Chinese TheatreTelly SavalasTinseltownUSAUnited StatesUnited States of AmericaΑριστοτέλης ΣαβάλαςΤέλλυ ΣαβάλαςUSGoddess Godfather
* * *

# Comments(0)
### Additional info
License (History)
All rights reserved
License History
Viewing privacy Public
Safety level Safe
Content type Photo
S Search
←→Photo navigation
<>Thumbnail navigation
Z Zoom
B Back to context
Sign Up

# Comments(0)
## Language
English

# Comments(0)
## SmugMug Films
YouTube Channel

# Comments(0)
## Quick links
AboutJobsBlogAdvertiseDevelopersCookiesGuidelinesHelpReport

# Comments(0)
## Policies
LegalPrivacyTerms
© 2026Connecting people through photography.
</excerpt>
### Rank 5 of 44 — 0.56
<excerpt title="Telly Savalas getting his star on the Walk of Fame, October 26, 1983.">
# FABULOUS FILMS & STARS | Telly Savalas getting his star on the Walk of Fame, October 26, 1983. | Facebook
[October 26 at 8:20 PM](https://www.facebook.com/groups/1684044015213864/?multi_permalinks=4849171748701059&hoisted_section_header_type=recently_seen&__cft__[0]=AZg0g1RNtc4ejqvJVg2brbp2AFzwvOFX55cvN0thB0qtxEgjgMGQrmRhLVef5EXgW165jm2Pep_Lq6-AEnlZJZN-LzvuQYfT9mwuhPnFjJWXLyO8zephFkM40G56P_1TaqJIkn9aNw6eZe3vZWlDd8gie79wVuZLiT7yooONLDaBKE1QRx7YL_TlgoODsPkP&__tn__=%2CO%2CP-R) ·
Telly Savalas getting his star on the Walk of Fame, October 26, 1983.
[](https://www.facebook.com/photo/?fbid=30183563211233753&set=gm.4849171748701059&idorvanity=1684044015213864&__cft__[0]=AZg0g1RNtc4ejqvJVg2brbp2AFzwvOFX55cvN0thB0qtxEgjgMGQrmRhLVef5EXgW165jm2Pep_Lq6-AEnlZJZN-LzvuQYfT9mwuhPnFjJWXLyO8zephFkM40G56P_1TaqJIkn9aNw6eZe3vZWlDd8gie79wVuZLiT7yooONLDaBKE1QRx7YL_TlgoODsPkP&__tn__=EH-R)

# FABULOUS FILMS & STARS | Telly Savalas getting his star on the Walk of Fame, October 26, 1983. | Facebook
![Image 2](blob:http://localhost/85d8b181a20aeb64a3afc2f1c39d2480)
![Image 3](blob:http://localhost/2b45e6f1a2ae097354c0b291152873d5)
All reactions:
128
10 comments
8 shares
Like
Comment
Share
Most relevant
Michael Ruth
Who love ya baby. Now I want a lollipop
*   [3w](https://www.facebook.com/groups/1684044015213864/posts/4849171748701059/?comment_id=4849234545361446&__cft__[0]=AZg0g1RNtc4ejqvJVg2brbp2AFzwvOFX55cvN0thB0qtxEgjgMGQrmRhLVef5EXgW165jm2Pep_Lq6-AEnlZJZN-LzvuQYfT9mwuhPnFjJWXLyO8zephFkM40G56P_1TaqJIkn9aNw6eZe3vZWlDd8gie79wVuZLiT7yooONLDaBKE1QRx7YL_TlgoODsPkP&__tn__=R]-R)
Glenn Bentley
The pioneer of shaved heads.
</excerpt>

## Search 6 — query: "Telly Savalas Golden Globe award"
### Rank 1 of 56 — 0.64 (passed on)
<excerpt title="Telly Savalas">
## Awards and nominations
68.   Jump up to: 12"Telly Savalas". [_Autopsy: The Last Hours of..._](https://en.wikipedia.org/wiki/Autopsy:_The_Last_Hours_of... "Autopsy: The Last Hours of...") (television). Season 13. Episode 4. May 14, 2022.  
69.   ↑Henkel, John (December 1994). "Prostate Cancer: New Tests Create Treatment Dilemmas". _FDA Consumer_. Vol.28, no.10. Archived from the original on January 19, 2012. Retrieved June 16, 2009.  
70.   ↑"Sheraton Universal Hotel". _seeing-stars.com_. Archived from the original on December 8, 2010. Retrieved September 5, 2022.  
71.   ↑Wharton, David (January 25, 1994). "Telly's Favorite Hotel Knew Him as a Regular Guy". _Los Angeles Times_.  
72.   ↑Pappas, Gregory (January 21, 2018). "Nine Facts You May Not Know About the Late Telly Savalas". _The Pappas Post_. Retrieved March 1, 2018.  
73.   ↑"Performances:: 1975, London Palladium | Royal Variety Charity". _www.royalvarietycharity.org_. Retrieved August 29, 2021.  
74.   ↑"The Royal Variety Performance 1975". _YouTube_. Retrieved August 29, 2021.  
75.   ↑"The 35th Academy Awards (1963) Nominees and Winners". Academy of Motion Picture Arts and Sciences. October 5, 2014. Retrieved May 12, 2016.  
76.   ↑"Telly Savalas". Golden Globe Awards. Retrieved October 12, 2023.  
77.   ↑"Telly Savalas". Academy of Television Arts & Sciences. Retrieved October 12, 2023.

## Awards and nominations
*   Official website  
*   Telly Savalas at IMDb  
*   Telly Savalas at the TCM Movie Database (archived)   
*   Telly Savalas discography at Discogs  
*   Telly Savalas on Find a Grave
</excerpt>
### Rank 2 of 56 — 0.62
<excerpt title="Telly Savalas">
| 1967 | _The F.B.I._ | Ed Clementi | Episode-2 part: "The Executioners" |  
| _The Man from U.N.C.L.E_ | Count Valerino De Fanzini | 2 episodes |  
| _Bob Hope Presents the Chrysler Theatre_ | Mueller | Episode: "Don't Wait for Tomorrow" |  
| _[Garrison's Gorillas](https://en.wikipedia.org/wiki/Garrison's\_Gorillas "Garrison's Gorillas")_ | Wheeler | Episode: "The Big Con" |  
| _Cimarron Strip_ | 'Bear' | Episode: "The Battleground" |  
| 1970 | _The Red Skelton Show_ | 'Tex' | Episode: "Stagecoach Hijack" |  
| 1971 | _ITV Sunday Night Theatre_ | Gregor Antonescu | Episode: "Man and Boy" |  
| _[Mongo's Back in Town](https://en.wikipedia.org/wiki/Mongo's\_Back\_in\_Town "Mongo's Back in Town")_ | Lieutenant Pete Tolstad | Television film (also known as _Steel Wreath_) |  
| 1972 | _Visions..._ | Lieutenant Phil Keegan | Television film |  
| 1973 | _The Marcus-Nelson Murders_ | Lieutenant Theo Kojak | Television film Nominated—Primetime Emmy Award for Outstanding Single Performance by an Actor in a Leading Role |  
| _She Cried Murder_ | Inspector Joe Brody | Television film |  
| 1973–1978 | _Kojak_ | Lieutenant Theo Kojak | 118 episodes Golden Globe Award for Best Actor in a Television Series – Drama(1975–1976) Primetime Emmy Award for Best Lead Actor in a Drama Series(1974) Nominated—Golden Globe Award for Best Actor in a Television Series – Drama(1977–1978) Nominated—Primetime Emmy Award for Outstanding Lead Actor in a Drama Series(1975) Nominated—Primetime Emmy Award for Outstanding Directing in a Drama Series(1975) |  
| 1974 | _The Carol Burnett Show_ | Himself | Season 8 Episode 5 |
</excerpt>
### Rank 3 of 56 — 0.58
<excerpt title="Telly Savalas">
## Awards and nominations
[edit]
| Year | Award | Category | Nominated work | Results | Ref. |  
| --- | --- | --- | --- | --- | --- |  
| 1962 | Academy Awards | Best Supporting Actor | _Birdman of Alcatraz_ | Nominated | [[75]](https://en.wikipedia.org/wiki/Telly_Savalas#cite_note-75) |  
| Golden Globe Awards | Best Supporting Actor – Motion Picture | Nominated | [[76]](https://en.wikipedia.org/wiki/Telly_Savalas#cite_note-76) |  
| 1965 | _Battle of the Bulge_ | Nominated |  
| 1974 | Best Actor in a Television Series – Drama | _Kojak_ | Won |  
| 1975 | Won[[a]](https://en.wikipedia.org/wiki/Telly_Savalas#cite_note-77) |  
| 1976 | Nominated |  
| 1977 | Nominated |  
| 1973 | Primetime Emmy Awards | Outstanding Single Performance by an Actor in a Leading Role | _The Marcus-Nelson Murders_ | Nominated | [[77]](https://en.wikipedia.org/wiki/Telly_Savalas#cite_note-78) |  
| 1974 | Best Lead Actor in a Drama Series | _Kojak_(Episode: "Requiem for a Cop") | Won |  
| 1975 | Outstanding Lead Actor in a Drama Series | _Kojak_ | Nominated |  
| Outstanding Directing in a Drama Series | _Kojak_(Episode: "I Want to Report a Dream...") | Nominated |

## Awards and nominations
*   _This is Telly Savalas..._ (1972)  
*   _Telly_ (1974)  
*   _Telly Savalas_ (1975)  
*   _Who Loves Ya Baby_ (1976)  
*   _Sweet Surprise_ [released on cassette and CD under the title _Some Broken Hearts_] (1980)

*   "Try to Remember" (1972)  
*   "Look Around You" (1972)  
*   "I Don't Want To Know / I Walk The Line" (1972)  
*   "We All End Up The Same" (1972)  
*   "If" (1974)  
*   "[You've Lost That Lovin' Feelin'](https://en.wikipedia.org/wiki/You've_Lost_That_Lovin'_Feelin' "You've Lost That Lovin' Feelin'") / Help Me Make It Through the Night" (1974)  
*   "Who Loves Ya Baby" (1975)  
*   "A Good Time Man Like Me Ain't Got No Business Singing The Blues" (1976)  
*   "Sweet Surprise" (1980)  
*   "Some Broken Hearts Never Mend" (1980)  
*   "Lovin' Understandin' Man" (1981)  
*   "Goodbye Madame" (1982)
1.   ↑Tied with Robert Blake for _Baretta_.
</excerpt>
### Rank 4 of 56 — 0.57
<excerpt title="Telly Savalas">
_Kojak_ aired on CBS for five seasons from October 24, 1973, until March 18, 1978, with 118 episodes produced.[[23]](https://en.wikipedia.org/wiki/Telly_Savalas#cite_note-TVGuide-23) The role won Savalas an Emmy and two Golden Globes for Best Actor in a Drama Series. Co-stars on the show included Savalas's younger brother George as Detective Stavros, a sensitive, wild-haired, quiet, comedic foil to Kojak's street-wise humor in an otherwise dark dramatic series,[[34]](https://en.wikipedia.org/wiki/Telly_Savalas#cite_note-34)Kevin Dobson as Kojak's trusted young partner, Det. Bobby Crocker, whose on-screen chemistry with Savalas was a success story of 1970s television,[[35]](https://en.wikipedia.org/wiki/Telly_Savalas#cite_note-35) and Dan Frazer as Captain Frank McNeil.[[36]](https://en.wikipedia.org/wiki/Telly_Savalas#cite_note-36)
Due to a decline in ratings, the series was cancelled by CBS in 1978. Savalas and Frazer were the only actors to appear in all 118 episodes. Savalas was unhappy about the show's demise[[37]](https://en.wikipedia.org/wiki/Telly_Savalas#cite_note-37) but got the chance to reprise the Kojak persona in several television movies, starting in 1985.[[38]](https://en.wikipedia.org/wiki/Telly_Savalas#cite_note-38)[[39]](https://en.wikipedia.org/wiki/Telly_Savalas#cite_note-39) The first film, subtitled _The Belarus File_ and broadcast in February 1985, reunited Savalas with several of his co-stars from the series: younger brother George, Dan Frazer, Mark Russell (Det. Saperstein) and Vince Conti (Det. Rizzo). This marked those actors' final appearances in the _Kojak_ franchise.[[40]](https://en.wikipedia.org/wiki/Telly_Savalas#cite_note-40)[[41]](https://en.wikipedia.org/wiki/Telly_Savalas#cite_note-41)
</excerpt>
### Rank 5 of 56 — 0.56
<excerpt title="Telly Savalas">
| _[Mackenna's Gold](https://en.wikipedia.org/wiki/Mackenna's\_Gold "Mackenna's Gold")_ | Sergeant Tibbs |  |  
| _Sophie's Place_ | Herbie Haseler | Known as _Crooks and Coronets_ in the United Kingdom |  
| _[On Her Majesty's Secret Service](https://en.wikipedia.org/wiki/On\_Her\_Majesty's\_Secret\_Service\_(film) "On Her Majesty's Secret Service (film)")_ | Ernst Stavro Blofeld |  |  
| 1970 | _Land Raiders_ | Vicente Cardenas |  |  
| _[Kelly's Heroes](https://en.wikipedia.org/wiki/Kelly's\_Heroes "Kelly's Heroes")_ | Joe 'Big Joe' |  |  
| _Violent City_ | Al Weber |  |  
| 1971 | _Pretty Maids All in a Row_ | Surcher |  |  
| _A Town Called Bastard_ | Don Carlos |  |  
| _Clay Pigeon_ | Redford |  |  
| 1972 | _Crime Boss_ | Don Vincenzo |  |  
| _Sonny and Jed_ | Sheriff Franciscus |  |  
| _Horror Express_ | Captain Kazan |  |  
| _The Killer Is on the Phone_ | Ranko Drasovic |  |  
| _Pancho Villa_ | Pancho Villa |  |  
| _A Reason to Live, a Reason to Die_ | Maggiore Ward |  |  
| 1973 | _Senza Ragione_ | 'Memphis' |  |  
| 1974 | _Lisa and the Devil_ | Leandro |  |  
| 1975 | _Inside Out_ | Harry Morgan |  |  
| 1976 | _Killer Force_ | Harry Webb |  |  
| 1978 | _Capricorn One_ | Albain |  |  
| 1979 | _Escape to Athena_ | Zeno |  |  
| _Beyond the Poseidon Adventure_ | Captain Stefan Svevo |  |  
| _The Muppet Movie_ | El Sleezo Tough |  |  
| 1980 | _Border Cop_ | Frank Cooper |  |  

| 1981 | _Maria Tomba Homem_ | Unknown | Mazzaropi, had as objective, to make the next film, with the actor, perhaps with the title _KOJECA_ (parody of the name of the series _Kojak_), but he died before even starting the pre-production of the film, on June 13, 1981. |  
| 1982 | _Fake-Out_ | Lieutenant Thurston |  |  
| 1983 | _Afghanistan pourquoi?_ | Rebel Leader |  |  
| 1984 | _Cannonball Run II_ | Hymie Kaplan |  |  
| 1985 | _Beyond Reason_ | Dr. Nicholas Mati | Originally filmed in 1977 and not released theatrically; made available on home video eight years later Also director and writer |  
| 1986 | _GoBots: Battle of the Rock Lords_ | Magmar | Voice |  
| 1988 | _Faceless_ | Terry Hallen |  |  
| 1993 | _Mind Twister_ | Richard Howland |  |  
| 1995 | _Backfire!_ | Most Evil Man | Posthumous release (final film role) |
</excerpt>

## Search 7 — query: ""county fair" "The Muppet Movie" cameo"
### Rank 1 of 39 — 0.80 (passed on)
<excerpt title="Blu-ray Review: The Muppet Movie: the Original Classic- Nearly 35th ...">
_The Muppet Movie_ arrives on Blu-ray, right in time to perk interest for the new Muppet film that hits theaters next year. It doesn’t matter how many new Muppet movies get made, though; none can equal the charm and witty humor of the 1979 original, written by Jack Burns and Jerry Juhl and directed by James Frawley. Fresh from the success of the hilarious _Muppet Show_ TV series, Jim Henson and his associates made _The Muppet Movie_ a bonafide success, both critically and with theatergoers. It generated a hit soundtrack album and garnered an Academy Award nomination for the wonderful song, ”The Rainbow Connection” (written by Paul Williams and Kenny Ascher) and won a Grammy for Best Album for Children.
Everything works in this movie. The story is a classic tale of following your dream. The script is funny, melancholy, weird and optimistic. The characters regularly break the fourth wall, creating a sense of community with the audience, as in ”we’re all in this together.” And the songs are near perfect. Oh, and there are the cameos, a blend of old Hollywood and 70s hipness human cameos.
During the county fair sequence, Elliot Gould (at the peak of his popularity), Edgar Bergen & Charlie McCarthy, Bob Hope and Richard Pryor all appear within minutes of each other. Elsewhere, Steve Martin (then a rising comedian) and Mel Brooks also have screen time. This was the spirit of _The Muppet Show_, in which you’d see Rita Moreno one week and Elton John the next and this approach worked seamlessly in _The Muppet Movie._
Sadly, I feel that Disney sometimes tries to cram _their_ stars in the new Muppet movies, how else do you explain Selena Gomez, Whoopi Gholberg and Rico Rodriquez appearing in the movie. The cast list for the new film includes Brigit Mendler, Debby Ryan and Joss Lynch. Don’t know who they are? Just ask a kid who watches the Disney Channel and they’ll tell you. Is it too far fetched to expect Iron Man and Luke Skywalker in future films?

Thankfully, Disney finally gives us _The Muppet Movie_ on Blu-ray for children of all ages to watch for years to come. As far as I’m concerned, it’s a film should rank at the top of the best family movies, a list that would include _E.T., Wizard of Oz_ and _Willy Wonka and the Chocolate Factory._ It continues to entertain. Henson, Frank Oz and their motley crew of puppeteers pulled off a remarkable feat in 1979: they made a movie for the ages.
While it’s a great thing to see this Blu-ray release, what I’d really love to see is Disney invest in a complete remastering of the film. While this release definitely improves over the most recent DVD issues, the film print is still very grainy and the sound still could use some punching up. I hate to be critical of one of my favorite films. But we all know the technology is around and that this film, which was added to the Library of Congress National Film Registry in 2009, deserves to have the full kit and caboodle.
_The Muppet Movie: the Original Classic- Nearly 35 th Anniversary Edition_ comes with a digital copy of the film, as well as assorted bonus features, including Disney Intermission Frog-E-Oke Sing-Along (which mean, when you pause the film, there are some cool extra features that were shot for the Blu-ray release); Jim Frawley’s Extended Camera Test; Doc Hopper’s Extended Camera Test Commercial; Original Theatrical Trailers and Outtake Easter Eggs.

### About the Author
Scott Malchus is a writer, filmmaker and die hard Cleveland Indians fan. His memoir, â€œBasement Songs,â€ is available in paperback and Kindle. He wrote and directed the film â€œKing's Highway." His family is heavily involved in fund raising to find a cure for cystic fibrosis. Scott Malchus is an employee of Cartoon Network and Turner Broadcasting. The opinions expressed on Popdose are his own and do not reflect those of his employer. Email: Malchus@popdose.com. Follow him @MrMalchus
View All Articles
</excerpt>
### Rank 2 of 39 — 0.78
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
### Rank 3 of 39 — 0.74
<excerpt title="Celebrate 40 Years of The Muppet Movie with These “ ...">
**Speaking of James Frawley…**The director of _The Muppet Movie_ is himself suitably colorful—perfect for wrangling a host of hilarious, human-esque characters! Frawley got his start on stage in the acclaimed 1960s off-Broadway improvisational troupe The Premise, later appearing on TV’s _Gunsmoke_, _Outer Limits_, and _The Danny Kaye Show_. In the meantime, Frawley was cultivating his skills as a photographer; helming an acclaimed short film called _J-24_ led Frawley to directing, and he eventually won an Emmy Award as director on the fan-favorite ‘60s sitcom _The Monkees_.
**Just a Frog and His Banjo…**_The Muppet Movie_ memorably opens with Kermit the Frog, perched on a log in the lush green swamp he calls “home,” playing his banjo and singing one of his now signature tunes: “Rainbow Connection.” Ever wonder how they managed to film that scene? The man behind the frog, Jim Henson, spent three full days under water inside a specially constructed “bathysphere,” operating Kermit through rubber-sleeved arms! According to the film’s press notes, the submersible was made from two aluminum jet-engine containers and was wired for both sight (a video monitor which enabled Henson to see Kermit’s performance) and sound (Henson’s microphone hookup).
**Even Muppets Need Transportation…**Did you know that Fozzie Bear drives two different cars in _The Muppet Movie_? One is a 1947 Ford “Woody” station wagon, and the other is a 1951 Studebaker Champion. Meanwhile, Gonzo and his chicken companion Camilla drive a 1969 Citreon plumbing repair truck, while later in the film, Dr. Teeth and the Electric Mayhem are seen tooling around in a brightly painted 1961 International school bus.

**Special Guest Cameos A-Plenty…**Most Muppet fans are familiar with _The Muppet Movie_’s cavalcade of guest appearances—from radio/ventriloquist legend Edgar Bergen (in his final film appearance) and Madeline Kahn to Steve Martin, Richard Pryor, and Mel Brooks, the film boasts a veritable “who’s who” of comedy talent. One such cameo is Oscar nominee Elliott Gould; according to the film’s press material, Gould was once asked to emcee the Miss Universe Pageant, which he declined due to a busy filming schedule. But the pageant world came ‘round again—albeit fictitiously—when Gould was asked to appear in _The Muppet Movie_ as the host of the quaint Bogen County Fair’s beauty contest… won by Miss Piggy, of course!
**Some Hollywood History…**The film follows the Muppets on their journey to Hollywood, as they dream of big-screen stardom—all the while pursued by the flamboyantly evil Doc Hopper (Charles Durning), a fast-food tycoon who wants Kermit to star in his commercials. The climactic scene where Kermit and friends finally face off against Doc and his henchmen is portrayed in classic western-film style… and was even shot at the very same location as the showdown in Gary Cooper’s iconic 1952 western _High Noon_.
**A Truly Lasting Legacy…**In 2009, _The Muppet Movie_ was named to the prestigious National Film Registry by the Library of Congress. So what exactly does that mean? Every year since 1988, the registry’s Preservation Board selects 25 films—deemed “culturally, historically, or aesthetically significant”—that showcase the enduring range and diversity of American film heritage, all in an effort to increase awareness for its preservation. We’re sure any Muppet fan would agree: Preserving _The Muppet Movie_ for future generations is a _fantastic_ idea!
Want to keep celebrating this Muppetational milestone? Check out our 10 Fan-tastic Milestones Pin Set, which features an exclusive pin celebrating 40 years of _The Muppet Movie._
</excerpt>
### Rank 4 of 39 — 0.63
<excerpt title="The Muppet Movie">
Joined by Rowlf the Dog, the Muppets pick up Miss Piggy – who is hitchhiking on the side of the road – and continue their journey; but their car breaks down in the desert. Sitting at a campfire, the group realizes that they will likely miss the auditions the next day. Kermit wanders off, ashamed for bringing his friends on a fruitless journey, but personal reflection restores his commitment. He returns to camp, where he discovers that the Electric Mayhem have come to their rescue, having learned of their plight by reading ahead in the film's script. The Mayhem offer to drive the group the rest of the way in their bus.
The group is warned by a reformed Max that Hopper has hired an assassin, Snake Walker, to kill Kermit. Kermit decides to face his aggressor and proposes a Western-style showdown in a nearby ghost town. There, they find inventor Dr. Bunsen Honeydew and his assistant Beaker. Kermit and his friends are saved when one of Dr. Honeydew's inventions, "insta-grow" pills, enlarges Mayhem drummer Animal, who frightens away Hopper and his henchmen.
Once the Muppets reach the Hollywood studio, they meet executive Lew Lord, who signs them to a "standard 'rich and famous' contract". The first take in their attempt to perform the script goes awry when Gonzo crashes into the prop rainbow, which knocks the scenery down and an explosion blows a hole in the roof of the studio, but a real rainbow shines through the hole and illuminates all the Muppets. Joined by characters from other Henson productions – including _Sesame Street_, _[Emmet Otter's Jug-Band Christmas](https://en.wikipedia.org/wiki/Emmet\_Otter's\_Jug-Band\_Christmas "Emmet Otter's Jug-Band Christmas")_, and _The Land of Gorch_ – the Muppets sing the final verse in a reprise of "Rainbow Connection". As the film ends, Sweetums tears through the screen, elated that he caught up with them.

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
</excerpt>
### Rank 5 of 39 — 0.42
<excerpt title="The Muppet Movie">
| Box office | $76.7 million[[7]](https://en.wikipedia.org/wiki/The_Muppet_Movie#cite_note-8)[[8]](https://en.wikipedia.org/wiki/The_Muppet_Movie#cite_note-9) |
_**The Muppet Movie**_ is a 1979 musicalroadcomedy film, directed by James Frawley and produced by Jim Henson, and the first theatrical film to feature the Muppets. A co-production between the United Kingdom and the United States, the film was written by _The Muppet Show_ writers Jerry Juhl and Jack Burns. Produced during the third season of _The Muppet Show_, the film tells the origin story of the Muppets, as Kermit the Frog embarks on a cross-country trip to Los Angeles, encountering several of the Muppets—who all share the same ambition of finding success in professional show business—along the way while being pursued by Doc Hopper, a greedy restaurateur with intentions of recruiting Kermit to promote his frog legs business.
The film stars Muppet performers Henson, Frank Oz, Jerry Nelson, Richard Hunt, and Dave Goelz, as well as Charles Durning and Austin Pendleton, and it features cameo appearances by Bob Hope, Dom DeLuise, James Coburn, Cloris Leachman, Richard Pryor, Telly Savalas, Edgar Bergen (in his final film appearance before his death), Orson Welles, Madeline Kahn, Milton Berle, Carol Kane, Steve Martin, Mel Brooks, Elliott Gould, and Paul Williams. Notable for its surreal humour, meta-references and prolific use of cameos, _The Muppet Movie_ was released by Associated Film Distribution in the United Kingdom on May 31, 1979, and in the United States on June 22, 1979.
The film received critical praise, including two Academy Award nominations for Paul Williams and Kenneth Ascher's musical score and their song "Rainbow Connection". The film grossed $76.7 million worldwide against an $8 million budget. _The Muppet Movie_ was followed by seven feature films starring the Muppets as well as several more television series and media. In 2009, the film was deemed "culturally, historically, or aesthetically significant" by the Library of Congress and selected for preservation in the National Film Registry.
</excerpt>

## Search 8 — query: "Elliot Gould Walk of Fame"
### Rank 1 of 78 — 0.30 (passed on)
<excerpt title="Elliott Gould Hollywood Walk Of Fame Star Location">
# Elliott Gould Hollywood Walk Of Fame Star Location
Log In
Sign Up
Watch reels about elliott gould hollywood walk of fame star location from people around the world.

# Elliott Gould Hollywood Walk Of Fame Star Location
## hollywood walk of fame stars


# Elliott Gould Hollywood Walk Of Fame Star Location
## walk of fame


# Elliott Gould Hollywood Walk Of Fame Star Location
## hollywood walk of stars


# Elliott Gould Hollywood Walk Of Fame Star Location
## location of


# Elliott Gould Hollywood Walk Of Fame Star Location
## hollywood walk


# Elliott Gould Hollywood Walk Of Fame Star Location
## hollywood walk of fame


# Elliott Gould Hollywood Walk Of Fame Star Location
## faming


# Elliott Gould Hollywood Walk Of Fame Star Location
## goulds


# Elliott Gould Hollywood Walk Of Fame Star Location
## star walk


# Elliott Gould Hollywood Walk Of Fame Star Location
## hollywoods
[[](https://www.instagram.com/themagicofpfeiffer) themagicofpfe... 2,468 February 10: Happy Birthda Alan Hale Sr. (1892–1950) #AlanHaleSr #actor #OldHollywood #happybirthday](https://www.instagram.com/reel/DUkJz48DohU/?utm_source=popular_topic_grid)
[[](https://www.instagram.com/themagicofpfeiffer) themagicofpfe... 1,953 February 7: Happy Birthday Eddie Bracken (1915–2002) #EddieBracken #actor #homealone #OldHollywood #happybirthday](https://www.instagram.com/reel/DUcbvbyAFTv/?utm_source=popular_topic_grid)
[[](https://www.instagram.com/themagicofpfeiffer) themagicofpfe... 1,644 January 30: Happy Birthday John Ireland (1914–1992) #JohnIreland #actor #OldHollywood #happybirthday](https://www.instagram.com/reel/DUH1nFzjk5U/?utm_source=popular_topic_grid)
[[](https://www.instagram.com/themagicofpfeiffer) themagicofpfe... 2,701 February 12: Happy Birthday Lorne Greene (1915–1987) #LorneGreene #actor #OldHollywood #happybirthday](https://www.instagram.com/reel/DUpUvLPgDHe/?utm_source=popular_topic_grid)
[[](https://www.instagram.com/themagicofpfeiffer) themagicofpfe... 1,456 January 31: Happy Birthday To John Agar (1921–2002) #JohnAgar #actor #OldHollywood #happybirthday](https://www.instagram.com/reel/DUKcLA9AInk/?utm_source=popular_topic_grid)
</excerpt>
### Rank 2 of 78 — 0.29
<excerpt title="Friends Star Elliott Gould, 88, Makes Rare Public Appearance in LA!">
# Friends Star Elliott Gould, 88, Makes Rare Public Appearance in LA! 😱
## 0 Comments
Sort comments
Sort by
Top Show featured commentsNewest Show recent comments, including potential spam
Add a comment...

# Friends Star Elliott Gould, 88, Makes Rare Public Appearance in LA! 😱
## Comments
Top Show featured commentsNewest Show recent comments, including potential spam

# Friends Star Elliott Gould, 88, Makes Rare Public Appearance in LA! 😱
## In this video
Transcript

# Friends Star Elliott Gould, 88, Makes Rare Public Appearance in LA! 😱
## Friends Star Elliott Gould, 88, Makes Rare Public Appearance in LA! 😱
CinStar
CinStar
4 Likes
7 Views
19h Ago
Legendary Friends actor Elliott Gould has made a rare public appearance in Los Angeles at 88! ❤️ Best known for playing Jack Geller, the father of Ross and Monica on the iconic sitcom Friends, Elliott continues to bring back nostalgic memories for fans. Did you recognize this Hollywood legend? Subscribe to Cinstar for the latest celebrity news and Hollywood updates! 🌟 #ElliottGould#Friends#JackGeller#HollywoodNews#CelebrityNews#Cinstar#Shorts…...more
...more Show less
How this was made
Auto-dubbed
Audio tracks for some languages were automatically generated. Learn more

# Friends Star Elliott Gould, 88, Makes Rare Public Appearance in LA! 😱
## Friends Star Elliott Gould, 88, Makes Rare Public Appearance in LA! 😱
### People mentioned
1 person

# Elliott Gould #### American actor (born 1938)
Transcript
Follow along using the transcript.
Show transcript

# Elliott Gould #### American actor (born 1938)
### CinStar 1.03K subscribers
VideosAbout Instagram

# Elliott Gould #### American actor (born 1938)
## Video details
Date
Nov 17, 2026
Views
7
Likes
4

# Elliott Gould #### American actor (born 1938)
## Transcript
NaN / NaN
11:58

# Elliott Gould #### American actor (born 1938)
## Transcript
### Nobody Can Handle Matthew Perry's SARCASTIC Personality
RingRivalry
38K 11d ago
16:37

# Elliott Gould #### American actor (born 1938)
## Transcript
### When Hollywood Legends Were Asked About Matthew Perry
Sovrenza and Nointra
510K 3w ago
25:06 New

# Elliott Gould #### American actor (born 1938)
## Transcript
### 10 Biopic Actors Who Nailed Their Impression & 10 Who Didn't Come Close
MsMojo
603K 5d ago
21:40 New

# Elliott Gould #### American actor (born 1938)
## Transcript
### [[손석희의 12시] ‘수능 D-1’ AI 부정행위 논란, 정승제에게 묻다 _정승제 수학 강사 | 질문들 | MBC 261118](https://m.youtube.com/watch?v=xVVXr7IMCJI)
손석희의 12시
7K 2h ago
15:55 New

# Elliott Gould #### American actor (born 1938)
## Transcript
### When Cat Decides to Keep a Close Eye on Dad's Work! 🤣
The Chuckling Cats
22K 1d ago
18:19 New

# Elliott Gould #### American actor (born 1938)
## Transcript
### The Time Machine (1960): Where Are They Now? | What Really Happened to Them?
CineTime Capsule
42K 12h ago
33:49 New

# Elliott Gould #### American actor (born 1938)
## Transcript
### [[Breaking] Top Tax Accountant Caught Hiding Spy Camera in Correction Tape [News Playlist] / Chann...](https://m.youtube.com/watch?v=7eO0DXbwBps)
채널A News
92K 4h ago
23:15 New
</excerpt>
### Rank 3 of 78 — 0.25
<excerpt title="Friends Star Elliott Gould, 88, Makes Rare Public Appearance in LA!">
# Elliott Gould #### American actor (born 1938)
## Transcript
### [[Breaking] Top Tax Accountant Caught Hiding Spy Camera in Correction Tape [News Playlist] / Chann...](https://m.youtube.com/watch?v=7eO0DXbwBps)
채널A News
92K 4h ago
23:15 New

# Elliott Gould #### American actor (born 1938)
## Transcript
### WEEKEND NAUGHTY/NICE: Angelina Jolie Blames Brad Pitt For Daughter’s Hospitalization
Rob Shuter
96K Streamed 3d ago
20:20

# Elliott Gould #### American actor (born 1938)
## Transcript
### When six auditions changed TV forever
ScreenPuff
1.6M 6mo ago
24:40 New

# Elliott Gould #### American actor (born 1938)
## Transcript
### [[충격단독]김세의 쳐넣으려고 현재10억쓴 장사의신.아직 50억남았습니다."은현장의 렉카박멸"](https://m.youtube.com/watch?v=XAwS7tU8Cqc&pp=0gcJCcgHAYcqIYzv)
장사의 신
168K 4h ago
36:10 New

# Elliott Gould #### American actor (born 1938)
## Transcript
### "유행도 숙제가 됐다." 억지 유행에 지친 한국인들 근황ㅣ지식인 클래스 EP.38 (김난도 교수)
지식인사이드
1.5M 1d ago
6:50

# Elliott Gould #### American actor (born 1938)
## Transcript
### Matthew Perry's Newfound Success | Late Night with Conan O’Brien
Conan O'Brien
451K 3y ago
14:40

# Elliott Gould #### American actor (born 1938)
## Transcript
### Friends Bloopers That Were Better Than The Actual Scene!
Weird Hollywood Movie Facts
355K 3mo ago
15:39 New

# Elliott Gould #### American actor (born 1938)
## Transcript
### Bush and Obama Can’t Stop Roasting Each Other, and It’s HILARIOUS!
Celeb Cuts
3.3M 3d ago
16:45 New

# Elliott Gould #### American actor (born 1938)
## Transcript
### Who Really Wanted Jensen Huang Out of Nvidia
The Money Timeline
932K 4d ago
1:02:36

# Elliott Gould #### American actor (born 1938)
## Transcript
### Chandler Off Script | Matthew Perry All Appearances | David Letterman
Letterman
28K 8d ago
36:37 New

# Elliott Gould #### American actor (born 1938)
## Transcript
### 수능날 아침 전국민에 재난문자...'OS 탈옥'하면 무용지물?｜손수호, 김단테
김현정의 고수다
158K 20h ago
Auto-dubbed
16:12 New

# Elliott Gould #### American actor (born 1938)
## Transcript
### Why Saved by the Bell’s Dennis Haskins Never Talked About the Revival
Flashback Fame
7.2K 16h ago
13:53 New

# Elliott Gould #### American actor (born 1938)
## Transcript
### This Scene Is NOT Edited! Take a Closer Look At This “Back To The Future” Blooper
The Fade Out Files
960 18h ago
25:13

# Elliott Gould #### American actor (born 1938)
## Transcript
### Friends | The Making of Friends with Marta Kauffman and David Crane | Warner Bros. Entertainment
Warner Bros. Entertainment
285K 2y ago
Show more
Show more
</excerpt>
### Rank 4 of 78 — 0.25
<excerpt title="Elliott Gould">
| Elliott Gould |  
| --- |  
|  Gould in 1986 |  
| Born | Elliott Goldstein August 29, 1938 (age 88)[[1]](https://en.wikipedia.org/wiki/Elliott_Gould#cite_note-APCB-1) New York City, U.S. |  
| Occupation | Actor |  
| Years active | 1964–present |  
| Spouses | * Barbra Streisand ​ ​ (m.1963;div.1971)​ * Jennifer Bogart ​ ​ (m.1973;div.1975)​ ​ ​ (m.1978;div.1989)​ |  
| Children | 3, including Jason |  
| Relatives | Paul Bogart (former father-in-law) |
**Elliott Gould** (; né**Goldstein**; born August 29, 1938) is an American actor.

Gould's breakthrough role was in the film _Bob & Carol & Ted & Alice_ (1969), for which he received a nomination for the Academy Award for Best Supporting Actor. The following year, he starred as Capt. Trapper John McIntyre in the Robert Altman film _M*A*S*H_ (1970), for which he received nominations for a BAFTA Award and Golden Globe Award. Gould continued working with Altman in _The Long Goodbye_ (1973) and _California Split_ (1974). Other notable film roles include _Getting Straight_ (1970), Alan Arkin's _Little Murders_ (1971), Ingmar Bergman's _The Touch_ (1971), Richard Attenborough's _A Bridge Too Far_ (1977), _Capricorn One_ (1978), _The Silent Partner_ (1978), Barry Levinson's _Bugsy_ (1991), _American History X_ (1998), Steven Soderbergh's _Contagion_ (2011), and _Ruby Sparks_ (2012). He also starred as Reuben Tishkoff in the [_Ocean's_ film series](https://en.wikipedia.org/wiki/Ocean's_(film_series) "Ocean's (film series)") (2001, 2004, 2007, and 2018).
Gould is a member of [_Saturday Night Live_'s Five Timers' Club](https://en.wikipedia.org/wiki/SNL's_Five_Timer's_Club "SNL's Five Timer's Club"), having hosted six times from 1976 to 1980. He is also known on television for his recurring roles as Jack Geller on the NBCsitcom_Friends_ (1994–2004) and Ezra Goldman in the Showtime series _Ray Donovan_ (2013–2016).
</excerpt>
### Rank 5 of 78 — 0.23
<excerpt title="Friends Star Elliott Gould, 88, Makes Rare Public Appearance in LA!">
# Friends Star Elliott Gould, 88, Makes Rare Public Appearance in LA! 😱 - YouTube
## Friends Star Elliott Gould, 88, Makes Rare Public Appearance in LA! 😱
| What Really Happened to Them?CineTime Capsule 42K • 12h ago Live Playlist ()Mix (50+)[33:49 [Breaking] Top Tax Accountant Caught Hiding Spy Camera in Correction Tape [News Playlist] / Chann...채널A News 92K • 4h ago Live Playlist ()Mix (50+)](https://www.youtube.com/watch?v=7eO0DXbwBps)23:15 WEEKEND NAUGHTY/NICE: Angelina Jolie Blames Brad Pitt For Daughter’s Hospitalization Rob Shuter 96K • Streamed 3d ago Live Playlist ()Mix (50+)20:20 When six auditions changed TV forever ScreenPuff 1.6M • 6mo ago Live Playlist ()Mix (50+)[24:40 [충격단독]김세의 쳐넣으려고 현재10억쓴 장사의신.아직 50억남았습니다."은현장의 렉카박멸"장사의 신 168K • 4h ago Live Playlist ()Mix (50+)](https://www.youtube.com/watch?v=XAwS7tU8Cqc)36:10 "유행도 숙제가 됐다." 억지 유행에 지친 한국인들 근황ㅣ지식인 클래스 EP.38 (김난도 교수)지식인사이드 1.5M • 1d ago Live Playlist ()Mix (50+)6:50 Matthew Perry's Newfound Success | Late Night with Conan O’Brien Conan O'Brien 451K • 3y ago Live Playlist ()Mix (50+)

# Friends Star Elliott Gould, 88, Makes Rare Public Appearance in LA! 😱
CinStar
CinStar
1.03K subscribers
Subscribe
Subscribed
4
Download
1
2
3
4
5
6
7
8
9
0
1
2
3
4
5
6
7
8
9
0
1
2
3
4
5
6
7
8
9
views
1
2
3
4
5
6
7
8
9
0
1
2
3
4
5
6
7
8
9
0
1
2
3
4
5
6
7
8
9
1
2
3
4
5
6
7
8
9
0
1
2
3
4
5
6
7
8
9
0
1
2
3
4
5
6
7
8
9
h ago
#ElliottGould#Friends#JackGeller
7 views • Nov 17, 2026 • #ElliottGould #Friends #JackGeller
Legendary Friends actor Elliott Gould has made a rare public appearance in Los Angeles at 88! ❤️ Best known for playing Jack Geller, the father of Ross and Monica on the iconic sitcom Friends, Elliott continues to bring back nost…more
more
How this was made
Auto-dubbed
Audio tracks for some languages were automatically generated. Learn more

# Friends Star Elliott Gould, 88, Makes Rare Public Appearance in LA! 😱
### People mentioned
1 person

# Elliott Gould #### American actor (born 1938)
Transcript
Follow along using the transcript.
Show transcript

# Elliott Gould #### American actor (born 1938)
### CinStar 1.03K subscribers
VideosAbout Instagram

# Elliott Gould #### American actor (born 1938)
## Video details
Date
Nov 17, 2026
Views
7
Likes
4
Show less
#ElliottGould#Friends#JackGeller

# Friends Star Elliott Gould, 88, Makes Rare Public Appearance in LA! 😱
7 views
Nov 17, 2026
4
Download

# Friends Star Elliott Gould, 88, Makes Rare Public Appearance in LA! 😱
## 0 Comments
Sort comments
Sort by
Top Show featured commentsNewest Show recent comments, including potential spam
Add a comment...
</excerpt>

## Search 9 — query: ""Elliot Gould" Emmy"
### Rank 1 of 57 — 0.29 (passed on)
<excerpt title="EcoLuxe Lounge Celebrates Emmys while raising Awareness for ...">
The highlight of my time at the**EcoLuxe Lounge**at the Beverly Hilton Hotel in Beverly Hills was seeing legendary actor **Elliott Gould**, known for his roles in M.A.S.H, Ray Donovan, Ocean’s Eleven, Twelve, and Thirteen, Friends, and more. Also, we loved spending time with the host’s new pup, who acted as a personal smile maker and perfect accessory for picture taking in the snazzy white couch lounge. The luxury retreat was created to celebrate the 66th Annual Primetime Emmy Nominees and Presenters while raising awareness and funds for **Big Brothers Big Sisters Los Angeles**. The penthouse suite offered a massive outdoor veranda with stunning views of Los Angeles.
Actor Elliott Gould (Photo credit: Melissa Curtin)
Many of us know how valuable the Big Brothers Big Sisters program is, which helps children develop positive relationships that have a direct and lasting effect on their lives. Providing children who face adversity with strong and enduring professionally supported one-to-one relationships that change their lives for the better is the organization’s mission. Adult volunteers (‘Bigs’) are matched with children (‘Littles’), ages 6 through 18, in communities across Los Angeles County.
Thanks to LA’s leading sustainable TV/film product placement producer, **Debbie Durkin** brought this charity together with eco conscious brands, luxury vacations, and the best in lifestyle so guests could enjoy a Sunday filled with treats. Festivities included wine tastings from **Club W**, farm to-table-fare from **Circa 55**, a **MAN GLAM lounge**, Luxury travel vacations from **Caribbean Living Magazine**, the best in fall fashion and beauty, a celebrity pet lounge and music from **DJ Dime**, all in a spectacular space designed by **White Lotus Productions.**
Some of the fun guests that stopped by included:

*   **Beau Bridges**_(Masters of Sex)_ picking up a silk tie from Mark Roscoe.  
*   **Damien Puckler**_(GRIMM_) stocking up on Canine Caviar & Feline Caviar’s Holistic Alkaline-based pet foods.  
*   _Dancing with the Stars_ pro**Gleb Savchenko**trying on sunglasses from Serengeti Eyewear.  
*   **Sam Richardson**_(VEEP)_ tasting rosé from Club W.  
*   _Orange Is The New Black_ stars**Alysia Reiner**and**Madeline Brewer**hitting the green carpet at _ECOLUXE Lounge._  
*   **Elliot Gould**_(Ray Donovan)_ cuddling Debbie Durkin’s white lab Custos in the celebrity pet lounge.  
*   **Patrick Gallagher**_(Night at the Museum) stocking up on Freshbody’s Fresh Balls._  
*   **Teyonah Parris**_(Mad Men) picking up_ JAndre all natural cosmetic sponges.  
*   **Wes Ramsey**(CSI: Miami) talking about the importance of posture alignment with AlignMed.  
*   **Alex Meneses**_(The Goldbergs)_ getting her GLAM on from OC Hair & Makeup!  
*   **Drew Seeley**_(A Cinderella Story)_ picking up a trip from Caribbean Living Magazine & Hard Rock Hotels _._  
*   **Tenille Houston**_(The Canyons_) taking home Tamala Lingerie in her ECOLUXE giftbag.  
*   **Taylour Paige**_(VH1’s Hit the Floor)_ loving the Nourishing Beauty Serumfrom Youth Eternal by KellyAnn.  
*   **Scott Bailey**_(The Bay)_ snacking on white chocolate covered Oreos and red velvet VyPassetti Cake Pops.
Our favorite featured brands included **John Paul Pet Products**, the perfect wipes to clean your cat or dog, **Fresh Balls**(yes, we are serious) from FreshBody.com– the new science of dry, **The Rein Coat**,the premiere calming coat for the discerning dog, which makes the dog feel calm by stimulating a mother dog picking up her young, **AlignMed’s Posture Shirt**, and every possible natural make-up sponge from **J.Andre**.
Photo credit: Melissa Curtin
</excerpt>
### Rank 2 of 57 — 0.23
<excerpt title="10 reasons to get to know Elliott Gould, the '70s ultimate movie star, at this ...">
# 10 reasons to get to know Elliott Gould, the ’70s ultimate movie star, at this Philly retrospective
### MOVIES
#### He couldn’t get his City Council member to fix a dangerous intersection. Now he wants Jeffery Young Jr.’s job.
XGtjZAJgDF1Ya3NzXmAxeABrc3RAdjFwTGhadAN3C2QHa2BoA2AxcAdrWntfdDF4QmhaYAVjInAHf3BgBncie1l8WnxOdDJ/XHxwfEBgMnBCfAVkBnQcbAF/Y3AGYDJ4BXxzfEBgMn9YfAV8TWMMdAR8c2dedwxkAX9zdE53DHwAfHNaT2ALYAZrXX9bYAtsBX9dXV90IXNffAV4QHcxb1lrY2dbYAxzX3xwY1t3IX9faGB3X2Myc1h8c3xPdAtsB2tgd1x3C2ABa2NWB2MiWVx+Y3RPYyFsAGtaY113MnNffE13WnQxb11/XVIDdzF/XmtzVVx0VHgGa11rXWALbE9rYHtadAt8BH5zWgN3MWwEaAVkQHdUZAVrXVlbdiF4B2hdVVp0DF1ZaF1jXHcxfE1rYGdadjF8BWhNc110InQEa11gAnYyUgVoXWNddyF8BWhaa15gVHNca3B3X2AyWV1+cGNbYDFwBmtzfANgC2QHfmBoAnciXVhoY39cdFRzX35geAN3MWQBfHN0TXQyUVx8YHwEYyJwAH9zYAVjMmAGfHBoT3QyY1h/TVJNYyJ3X3xafE90DFYBf01kBGMMfAV/
</excerpt>
### Rank 3 of 57 — 0.22
<excerpt title="With my old friend, the incomparable Master actor Elliott Gould, making me ...">
*      
*
•
Follow
* * *
With my old friend, the incomparable Master actor Elliott Gould, making me laugh as always, at the party/presentation of the well-deserved Ralph Morgan awards given to him and great actress Diane Ladd. Lots of family and friends present. It was a memorable, sweet occasion.
Legend!!!
Reply
The great David Proval in there as well. Great photo!
2 likes
Reply
AND Diane Ladd. Not only are they great actors, they have given many years in service to our Union to guide us to help and health for ALL our Union members. You have, too, Lee. Thank you❣️
3 likes
Reply
Love this award was given to Elliot Gould❣️
1 like
Reply
Love you love you all 💘
1 like
Reply
❤️❤️❤️❤️
2 likes
Reply
Look amazing
2 likes
Reply
Great picture of both !
1 like
Reply
Bob, Carol Ted & Alice was one of my favorite films. Elliot was perfect.
❤️
2 likes
Reply
Still looking great Lee
1 like
Reply
Wonderful ♥️♥️♥️
1 like
Reply
got a little story for you about Elliot - hope to see you some to tell you
2 likes
Reply
286 17
</excerpt>
### Rank 4 of 57 — 0.22
<excerpt title="10 reasons to get to know Elliott Gould, the '70s ultimate movie star, at this ...">
# 10 reasons to get to know Elliott Gould, the ’70s ultimate movie star, at this Philly retrospective
### MOVIES
#### He couldn’t get his City Council member to fix a dangerous intersection. Now he wants Jeffery Young Jr.’s job.
"AMP_AUTH_BASE_URL":"UHN8BnYudwBVXVZOWAxaQnwFeE13IWQEa11zW3QiYEJ/TWdadCJsQn9aZAJ3IlIGf01zWmMMZEJ8XXAHdCFnXHxddAR0DHRCa3B7Wncie1h+Y3BOYzJvXH9NaARjMnBMa2B0BWAMc1xoWmQGYwtjWWhjUgZ3MndYfAVoTXYxfAB/cHRA","AUTH0_DOMAIN":"Um97BVwiXQVSWmNGdwt8A3xgaE93HHAFf2NoT3QycE98c1ZAYAxwBWhdZE93MnQHa11SQHQidAR/cGBAdiJ3XQ==","AUTH0_CLIENTID":"fGN7XHdUBExSc11CYwhvXn5dZAJ3IlIEfGNoTXQhcEx/c3dbdCJvWWtzfAR0MlZCf3N0BXQhZARoXWtcYzJkTXxddAR3DGwEf01wB3Qcc1l8BXhNdyJgT39weEB3MnhCfE10BXcheAg=","PIANO_ID":"UH93QnchDFlTBHdYYxxaTGhjdAV0C2QEf3N7WnQhfEJoY3RNdDJWTGhQDAo=",

# 10 reasons to get to know Elliott Gould, the ’70s ultimate movie star, at this Philly retrospective
### MOVIES
#### He couldn’t get his City Council member to fix a dangerous intersection. Now he wants Jeffery Young Jr.’s job.
"MIXED_CONTENT":"fn9dWFoIY0JrcHtOYwtgA39jaE9gHHddf2B8B3Qyc1l8Y3RPdAx3XXxwYE9gHGddf2NVW2AcdE1rXVJAdAxgTHxgYEB2MmNef2B7XmMhbE18Y3gHYwx4T3xadE53IWwHa2N7WnQLY1k=","VIAFOURA_SITE_UUID":"VHBoTXQLWUBVWUEDWCJaTWtjZE50ImBCaF1zXXQiYAVoY2BNdDJgTHxzYAV0DG9cf2NSBXQLZExrY39cdyFkT2tzeEB0InhMa2NSTndUcEx8XX9fdFR8T35ga150VHhMaE18BXcMdAdrY39ddBxsCA==","GOOGLE_CLIENT_ID":"UnBdTnQ+Y1t/BGsEdBxaTWtjc110MnRNa11kTnQiXgRrY3NfdCJ8BGtjd19jMXwFaAV4QGMMZE1/c2ADdCF8Qn5jY1t0HGQEfwVoAmAMWVhrYGQHdxx3WHxzf19gDF5MfGBkQHQMdAdoXXhAYwtsBH9gaE1jC3tca3BoA3Qhe1loWnQEdDJzX3wFeANjIlFZfnNdXXQyUV9+c3gHdzJdXn8FfAR3MXxCf2B8BHcyd15oXXQGdCJsBX5jcE50MmQFfHNwAmMidAV/c3NcdDJkCA==",
</excerpt>
### Rank 5 of 57 — 0.22
<excerpt title="10 reasons to get to know Elliott Gould, the '70s ultimate movie star, at this ...">
# 10 reasons to get to know Elliott Gould, the ’70s ultimate movie star, at this Philly retrospective
### MOVIES
#### He couldn’t get his City Council member to fix a dangerous intersection. Now he wants Jeffery Young Jr.’s job.
"GRAPHQL_KEY":"Ull3WF0LcwFUb2dGdAh8A3xNcEB2In9ZfF1aBHcLb198XXRAdBx8BX8FeAd2Mn9Yf2NzW3Yyf1lrY3ROdBx0QmtddE9gMlFffGNaT3YicABrYHRPdzFsQnxzVgdjC2wFfHN0BmM3CAg=","GATEWAY_URL":"Un9kBlghf09VYAgEdiEBA39gfE90DGNcfHN0T2MMdAB8YHxPdzJ0BGhaaE90DHQHfAVoQHQccAZ8Y1JAdjFsAHxgeAdgMXwFfAV/WmALb15oWndadCFgBg==","GATEWAY_SLS_URL":"fFoER3cLUgZ8YH9ZWzFSA3xgZEB2MnQGf2BoT3cyZ15/Y1ZPdjJwBGtgdE93ImQFfF1gBmMMZAB8YGAHYyF/XnxjUgZgMWBNfAV3XnYxYAdrY2tfYzFjXg==","FEEDS_URL":"fnBBQXcic09rYGsDXQtkA3xjY1tgMnQGf2B0B2Acd1x8cHhPdBx0TXxzcE93MmRPfFpkT3ccZAZ8cGhAdFRjXWtjf1pjMnwHfE1SB3dUYAd8Y3gFdDF8BGtdeE5gMnxPfAVoTmBUbAVoY2NadFRvXH9jUgo=",

# 10 reasons to get to know Elliott Gould, the ’70s ultimate movie star, at this Philly retrospective
### MOVIES
#### He couldn’t get his City Council member to fix a dangerous intersection. Now he wants Jeffery Young Jr.’s job.
"RESIZER_KEY":"U11zT2AxXUF/Y3NdWwt8A39gdARgDHQAfHN8BXQiYAZ/WmQFdCJ/X3xzVkB2MngHf3N0TnQcY1lrY1pAdwt8AX9NVk90MlYEa2NkTnciZExrXVZNdFRsAWtaaAR2MXwAa2B0QHYnCAg=","GOOGLEANALYTICS_ID":"aFl4AlsifAdoY3tcdiJgA39jUgZ3MnRNfFp8BnYydE1/YGBAYBxjWXxjUgR2MngA",
</excerpt>

## Search 10 — query: "Elliot Gould walk of fame star"
### Rank 1 of 72 — 0.29 (passed on)
<excerpt title="Hollywood never quite knew what to do with Elliott Gould. He did not look like a ...">
# Cozy Nest - Hollywood never quite knew what to do with... | Facebook
## Cozy Nest's Post
[February 24](https://www.facebook.com/cozynestus/posts/pfbid0zTewX8xCCJixMuJdj2VixmZ1mTduRgUmJ6nLGFzdeU92fsRSWhuE3qC9txWid8MPl?__cft__[0]=AZgHhmXWgXHGrXRQwOploFcW3rS4_E0sZSHJjdV1qZs0TZwfLZylTPEGo5t-XmcU__92rBpIxQevpt8Ij782Mo9fBXdf0Ms5ae5xq_8ji4XdBH2yoxq6ayEyiAKytv_vUnukAapfEanh_c3pDHsi4aevWpXZu1Q&__tn__=%2CO%2CP-R) ·
Hollywood never quite knew what to do with Elliott Gould. He did not look like a movie star, and he did not try to become one. He was tall and loose limbed, with unruly curls, a Brooklyn mumble, and a face that always seemed mildly amused by the entire idea of celebrity. And yet, in 1969, he earned an Academy Award nomination for Bob & Carol & Ted & Alice, and almost overnight, he became one of the most recognizable actors in America.
Then came MASH. Robert Altman’s chaotic war satire landed like a shockwave. The film captured a generation that was tired of authority, tired of slogans, and tired of pretending everything made sense. Gould’s Trapper John was irreverent, weary, and quietly defiant. He did not play rebellion. He lived inside it. Time magazine put him on its cover in 1970 and called him a star for an uptight age. That same year, four of his films were released. Hollywood did not simply want Elliott Gould. It depended on him.
And then it stopped.

# Cozy Nest - Hollywood never quite knew what to do with... | Facebook
## Cozy Nest's Post
In 1971, Gould was cast in a film called A Glimpse of Tiger. The production unraveled. Accounts varied, but tensions escalated, schedules broke down, and the film collapsed before it could be completed. Warner Brothers labeled Gould unreliable. Two psychotherapists, who never personally examined him, reportedly signed off on an insurance claim that described him as unstable. That paperwork was enough. Within months, the man who had been on the cover of Time could not get a phone call returned.
When director Ingmar Bergman publicly described Gould as difficult after working with him on The Touch, the label hardened. Hollywood did not require nuance. It required agreement. Once the industry decided who you were, there was little room to argue otherwise.
But Elliott Gould did not disappear.
He worked whenever he was allowed to. Robert Altman, who understood outsiders better than most, offered him a lifeline by casting him as Philip Marlowe in The Long Goodbye in 1973. Gould played the legendary detective not as a smooth hero, but as a distracted observer drifting through a world that no longer followed the old rules. The film failed at the box office, but time transformed it. Today, it is regarded as one of the most honest and unconventional detective films ever made.
Through the late 1970s and into the 1980s, Gould adjusted. He stopped chasing leading man status and became something rarer. A character actor with presence. He appeared on Saturday Night Live six times. He showed up in Muppet films. He took small roles in major productions and carried large roles in smaller ones. He never stopped working.
Then, quietly, the culture caught up.
In the 1990s, a new generation met him as Jack Geller on Friends, a warm and awkward television father whose sincerity felt earned. Soon after, director Steven Soderbergh cast him in Ocean’s Eleven as Reuben Tishkoff. Gould’s presence carried decades of survival, humor, and resilience. Soderbergh later said that having him on set simply brought good energy.
</excerpt>
### Rank 2 of 72 — 0.28
<excerpt title="Hollywood never quite knew what to do with Elliott Gould. He did not look like a ...">
# Cozy Nest - Hollywood never quite knew what to do with... | Facebook
Log In
Log In
Forgot Account?

# Cozy Nest - Hollywood never quite knew what to do with... | Facebook
## Cozy Nest's Post
* * *
[](https://www.facebook.com/cozynestus?__cft__[0]=AZgHhmXWgXHGrXRQwOploFcW3rS4_E0sZSHJjdV1qZs0TZwfLZylTPEGo5t-XmcU__92rBpIxQevpt8Ij782Mo9fBXdf0Ms5ae5xq_8ji4XdBH2yoxq6ayEyiAKytv_vUnukAapfEanh_c3pDHsi4aevWpXZu1Q&__tn__=%3C%3C%2CP-R)
### [**Cozy Nest**](https://www.facebook.com/cozynestus?__cft__[0]=AZgHhmXWgXHGrXRQwOploFcW3rS4_E0sZSHJjdV1qZs0TZwfLZylTPEGo5t-XmcU__92rBpIxQevpt8Ij782Mo9fBXdf0Ms5ae5xq_8ji4XdBH2yoxq6ayEyiAKytv_vUnukAapfEanh_c3pDHsi4aevWpXZu1Q&__tn__=-UC%2CP-R)
Tuesday, February 24, 2026 at 5:20 PM

# Cozy Nest - Hollywood never quite knew what to do with... | Facebook
## Cozy Nest's Post
[February 24](https://www.facebook.com/cozynestus/posts/pfbid0zTewX8xCCJixMuJdj2VixmZ1mTduRgUmJ6nLGFzdeU92fsRSWhuE3qC9txWid8MPl?__cft__[0]=AZgHhmXWgXHGrXRQwOploFcW3rS4_E0sZSHJjdV1qZs0TZwfLZylTPEGo5t-XmcU__92rBpIxQevpt8Ij782Mo9fBXdf0Ms5ae5xq_8ji4XdBH2yoxq6ayEyiAKytv_vUnukAapfEanh_c3pDHsi4aevWpXZu1Q&__tn__=%2CO%2CP-R) ·
Hollywood never quite knew what to do with Elliott Gould. He did not look like a movie star, and he did not try to become one. He was tall and loose limbed, with unruly curls, a Brooklyn mumble, and a face that always seemed mildly amused by the entire idea of celebrity. And yet, in 1969, he earned an Academy Award nomination for Bob & Carol & Ted & Alice, and almost overnight, he became one of the most recognizable actors in America.
Then came MASH. Robert Altman’s chaotic war satire landed like a shockwave. The film captured a generation that was tired of authority, tired of slogans, and tired of pretending everything made sense. Gould’s Trapper John was irreverent, weary, and quietly defiant. He did not play rebellion. He lived inside it. Time magazine put him on its cover in 1970 and called him a star for an uptight age. That same year, four of his films were released. Hollywood did not simply want Elliott Gould. It depended on him.
And then it stopped.
</excerpt>
### Rank 3 of 72 — 0.24
<excerpt title="Elliott Gould">
| Elliott Gould |  
| --- |  
|  Gould in 1986 |  
| Born | Elliott Goldstein August 29, 1938 (age 88)[[1]](https://en.wikipedia.org/wiki/Elliott_Gould#cite_note-APCB-1) New York City, U.S. |  
| Occupation | Actor |  
| Years active | 1964–present |  
| Spouses | * Barbra Streisand ​ ​ (m.1963;div.1971)​ * Jennifer Bogart ​ ​ (m.1973;div.1975)​ ​ ​ (m.1978;div.1989)​ |  
| Children | 3, including Jason |  
| Relatives | Paul Bogart (former father-in-law) |
**Elliott Gould** (; né**Goldstein**; born August 29, 1938) is an American actor.

Gould's breakthrough role was in the film _Bob & Carol & Ted & Alice_ (1969), for which he received a nomination for the Academy Award for Best Supporting Actor. The following year, he starred as Capt. Trapper John McIntyre in the Robert Altman film _M*A*S*H_ (1970), for which he received nominations for a BAFTA Award and Golden Globe Award. Gould continued working with Altman in _The Long Goodbye_ (1973) and _California Split_ (1974). Other notable film roles include _Getting Straight_ (1970), Alan Arkin's _Little Murders_ (1971), Ingmar Bergman's _The Touch_ (1971), Richard Attenborough's _A Bridge Too Far_ (1977), _Capricorn One_ (1978), _The Silent Partner_ (1978), Barry Levinson's _Bugsy_ (1991), _American History X_ (1998), Steven Soderbergh's _Contagion_ (2011), and _Ruby Sparks_ (2012). He also starred as Reuben Tishkoff in the [_Ocean's_ film series](https://en.wikipedia.org/wiki/Ocean's_(film_series) "Ocean's (film series)") (2001, 2004, 2007, and 2018).
Gould is a member of [_Saturday Night Live_'s Five Timers' Club](https://en.wikipedia.org/wiki/SNL's_Five_Timer's_Club "SNL's Five Timer's Club"), having hosted six times from 1976 to 1980. He is also known on television for his recurring roles as Jack Geller on the NBCsitcom_Friends_ (1994–2004) and Ezra Goldman in the Showtime series _Ray Donovan_ (2013–2016).
</excerpt>
### Rank 4 of 72 — 0.24
<excerpt title="Hollywood never quite knew what to do with Elliott Gould. He did not look like a ...">
# Cozy Nest - Hollywood never quite knew what to do with... | Facebook
## Cozy Nest's Post
Today, Elliott Gould has nearly two hundred screen credits, an Academy Award nomination, and a career that collapsed and rebuilt itself more than once. He never became the kind of leading man Hollywood preferred to control. He became something more enduring. An actor whose work grows richer with time.
He once said that success did not change him. Perhaps that was the problem. Or perhaps that is why, after all these years, he remains unforgettable.
[](https://www.facebook.com/photo/?fbid=904291165900652&set=a.132957463034030&__cft__[0]=AZgHhmXWgXHGrXRQwOploFcW3rS4_E0sZSHJjdV1qZs0TZwfLZylTPEGo5t-XmcU__92rBpIxQevpt8Ij782Mo9fBXdf0Ms5ae5xq_8ji4XdBH2yoxq6ayEyiAKytv_vUnukAapfEanh_c3pDHsi4aevWpXZu1Q&__tn__=EH-R)
![Image 3](blob:http://localhost/85d8b181a20aeb64a3afc2f1c39d2480)
![Image 4](blob:http://localhost/c228214878b3eaebe7a83f7398b606a3)
![Image 5](blob:http://localhost/2b45e6f1a2ae097354c0b291152873d5)
All reactions:
130
9 comments
11 shares
Like
Comment
Most relevant
Craig Woodward
Warner Brothers made him their scapegoat ... nice work, guys

# Cozy Nest - Hollywood never quite knew what to do with... | Facebook
## Cozy Nest's Post
*   [38w](https://www.facebook.com/cozynestus/posts/pfbid0zTewX8xCCJixMuJdj2VixmZ1mTduRgUmJ6nLGFzdeU92fsRSWhuE3qC9txWid8MPl?comment_id=1583405143791372&__cft__[0]=AZgHhmXWgXHGrXRQwOploFcW3rS4_E0sZSHJjdV1qZs0TZwfLZylTPEGo5t-XmcU__92rBpIxQevpt8Ij782Mo9fBXdf0Ms5ae5xq_8ji4XdBH2yoxq6ayEyiAKytv_vUnukAapfEanh_c3pDHsi4aevWpXZu1Q&__tn__=R]-R)
[](https://www.facebook.com/people/Mark-Johnson/pfbid02UJSDfnTq4oCHggoZNsUjiGxmh6YPmEg6LCS84Pw753WXz23qBn6wo9mRJuP8DofEl/?comment_id=Y29tbWVudDo5MDQyOTExOTI1NjczMTZfMjU5NzIxNzI5ODkxMDQzMzY%3D&__cft__[0]=AZgHhmXWgXHGrXRQwOploFcW3rS4_E0sZSHJjdV1qZs0TZwfLZylTPEGo5t-XmcU__92rBpIxQevpt8Ij782Mo9fBXdf0Ms5ae5xq_8ji4XdBH2yoxq6ayEyiAKytv_vUnukAapfEanh_c3pDHsi4aevWpXZu1Q&__tn__=R]-R)
</excerpt>
### Rank 5 of 72 — 0.23
<excerpt title="Never a typical Hollywood star, Oscar-nominated actor Elliot Gould, known ...">
# Never a typical Hollywood star, Oscar-nominated actor Elliot Gould, known for such classics as "MASH" and "The Long Goodbye" is as colorful and distinctive as the unorthodox characters he'd played. https://cbsn.ws/3j58H8F | CBS Sunday Morning | Facebook
Log In
Log In
Forgot Account?

# Video
Home
Live
Reels
Explore
More
Home
Live
Reels
Explore
Video 2
0:00 / 0:00
Elliott Gould on his unconventional stardom
Like
Comment
Share
![Image 2](blob:http://localhost/85d8b181a20aeb64a3afc2f1c39d2480)
![Image 3](blob:http://localhost/2b45e6f1a2ae097354c0b291152873d5)
676
·
20 comments
·
22K views

# Video
## **CBS Sunday Morning**
Monday, October 19, 2020 at 4:59 PM
October 19, 2020 ·
Follow
Never a typical Hollywood star, Oscar-nominated actor Elliot Gould, known for such classics as "MASH…
See more

# Video
## Comments
Most relevant
Top fan
Sam Akira Chang
He did great work...
*   11w
Noelene Griffiths
*   4y
View more comments
2 of 19

# Video
## Related Reels
CBS Sunday Morning 79K
CBS Sunday Morning 16K
CBS Sunday Morning 1.9M
CBS Sunday Morning 178K
CBS Sunday Morning 125K
CBS Sunday Morning 3.3M
CBS Sunday Morning 21K
CBS Sunday Morning 26K
CBS Sunday Morning 78K
CBS Sunday Morning 858K
CBS Sunday Morning 1.3M
CBS Sunday Morning 624K

# Video
## Related videos
[ 2:13](https://www.facebook.com/100059590535685/videos/1840364527166481/?__so__=permalink&__cft__[0]=AZg1nAIL4wtl70D4ru6FPTwFhsOw4ewAiBqSuHx0ZUjLVCijNPtL0U-v4RacB-IjBctVBup3fAq-LH3a3l9lGeYBBH8QNc5Hgd5HMUFmuOw6rjMBH7chtzgNssTKhw96xoMjWcim_AGQVqlnUdzSrA)
[](https://www.facebook.com/watch/100059590535685/?__cft__[0]=AZg1nAIL4wtl70D4ru6FPTwFhsOw4ewAiBqSuHx0ZUjLVCijNPtL0U-v4RacB-IjBctVBup3fAq-LH3a3l9lGeYBBH8QNc5Hgd5HMUFmuOw6rjMBH7chtzgNssTKhw96xoMjWcim_AGQVqlnUdzSrA)
</excerpt>

# Example 4
## Question
There was a space shuttle flight that launched two days before the original U.S. release date of an episode of The Office that was directed by Jason Reitman. Which member of the crew of this flight was born on the same day as someone who was the head coach of a professional NBA basketball team before 2022? The basketball team was founded after 1988 and was based in the same state the space shuttle flight launched from.

## Expected answer
Pamela Melroy

## Grade 1.00

## Search 1 — query: "The Office episode directed by Jason Reitman"
### Rank 1 of 38 — 0.87 (passed on)
<excerpt title="8 Famous Directors You Didn't Know Worked on The Office">
# 8 Famous Directors You Didn't Know Worked on The Office
## Jason Reitman
Photo: Getty Images
The fall of 2007 was a very good time to be Jason Reitman. The _Thank You for Smoking_ director (and son of legendary comedy filmmaker Ivan Reitman) was launching his feature breakthrough _Juno_ at festivals, and he was also making his debut as a director on _The Office_. Reitman directed two episodes of the series, both very memorable: "Local Ad" in Season 4 and "Frame Toby" in Season 5.

# 8 Famous Directors You Didn't Know Worked on The Office
## Marc Webb
Photo: Getty Images
Though he's best known now for his work on _The Amazing Spider-Man_ films, Marc Webb got his start with smaller stories like the hit romantic dramedy _(500) Days of Summer._ A year after that film hit big, he brought his skills to _The Office_, directing the Season 6 episode "The Manager and the Salesman," which also featured the debut of Oscar-winner Kathy Bates as Sabre CEO, Jo Bennett.
**RELATED:The Office Actors Who Also Wrote Episodes of the Hit NBC Comedy**

# 8 Famous Directors You Didn't Know Worked on The Office
## Jon Favreau
Photo: Getty Images
After making the leap to mega-blockbusters with the first two _Iron Man_ films, Jon Favreau returned to his small-scale comedy roots in 2013 and directed one of the most pivotal episodes of _The Office_'s final season. In "Moving On," Andy Bernard (Ed Helms) and Pam Beesly (Jenna Fischer) both consider major personal crossroads, and the episode helps set up the eventual series finale. It's Favreau's only contribution, but it feels like a fun return to the years of _Swingers_ and _Made_.

# 8 Famous Directors You Didn't Know Worked on The Office
## Cast Members Turned Directors
Jim Halpert (John Krasinski) appears in a scene from The Office, Season 9 Episode 3. Photo: Byron Cohen/NBC/NBCU Photo Bank
Through nine seasons and 200 episodes,_The Office_ also managed to get members of its core cast in on the directorial fun. Throughout the run, directors stepping from in front of the camera to helm episodes included B.J. Novak (five episodes), Steve Carell (three episodes), John Krasinski (three episodes), Rainn Wilson (three episodes), Ed Helms (two episodes), Mindy Kaling (two episodes), and Brian Baumgartner (one episode).
_**Relive all nine seasons of The Office — now streamingon Peacock. Die-hard audience members who have made it through the entire series more than once can discover never-before-seen bonus footage inthe extended "Superfan Episodes"currently spanning Seasons 1-6.**_
Read more about:
*   The Office
</excerpt>
### Rank 2 of 38 — 0.86
<excerpt title="TIL that J.J. Abrams, Joss Whedon, Harold Ramis, Jon Favreau, Bryan ...">
# TIL that J.J. Abrams, Joss Whedon, Harold Ramis, Jon Favreau, Bryan Cranston, and Jason Reitman all directed at least one episode of The Offce : r/todayilearned
Skip to main contentTIL that J.J. Abrams, Joss Whedon, Harold Ramis, Jon Favreau, Bryan Cranston, and Jason Reitman all directed at least one episode of The Offce : r/todayilearned
Open menu Open navigationGo to Reddit Home
r/todayilearned
Sign UpSign up for RedditLog InLog in to Reddit
Expand user menu Open settings menu
Go to todayilearned
r/todayilearned•11y ago
u/a_esbech

# TIL that J.J. Abrams, Joss Whedon, Harold Ramis, Jon Favreau, Bryan Cranston, and Jason Reitman all directed at least one episode of The Offce
imdb.com Open
Share
airbnb•Ad
호스팅, 참 좋죠. 근데 혼자 다 하려니 막막하신가요? 다행히 공동 호스트가 도와드릴 수 있어요.
Sign Up
airbnb.co.kr
u/airbnb•Ad
Travel hack: Book the home you want, then plan the trip around that.
Book Now
airbnb.com
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
mild_gingervitis
•11y ago
**J.J. Abrams** - "_Cocktails_" (Season 3 Ep. 17)
**Joss Whedon** - "_Business School_" (Season 3 Ep. 16)
"_Branch Wars_" (Season 4 Ep. 6)
**Harold Ramis** - "_A Benihana Christmas_" (Season 3 Ep. 10)
"_Safety Training_" (Season 3 Ep. 19)
"_Beach Games_" (Season 3 Ep. 22)
"_The Delivery: Part 2_" (Season 6 Ep. 18)
**Jon Favreau** - "_Moving On_" (Season 9 Ep. 16)
**Bryan Cranston** - "_Work Bus_" (Season 9 Ep. 4)
**Jason Reitman** - "_Local Ad_" (Season 4 Ep. 5)
"_Frame Toby_" (Season 5 Ep. 8)
Atwenfor
•11y ago
Of course Cranston directed the one where they operate their business from the back of a vehicle.
Roller_ball
•11y ago
And Whedon directed the one with a bat and had some vampire jokes. This was back when he was mainly known for Buffy and Angel.
more reply
more reply
more reply
More replies
Bensas42
•11y ago
I always love getting surprised by their names in the episodes.
a_probiotic_disaster
•11y ago
Jon Favreau's episode was meh, but the rest of these are amazing episodes. Maybe even some of the best episodes.
[deleted]
•11y ago
That's actually what I think of Jon Favreau all the time, just meh.
[deleted]
•11y ago
Comment removed by moderator
more replies
more replies
more replies
More replies
more replies
more replies
more replies
[deleted]
•11y ago
I found a still from JJ Abrams episode. http://i.imgur.com/WjBrVRk.png
Reply  Share
[deleted]
•11y ago
Comment deleted by user
Reply  Share
more replies
more replies
More replies
Blitz_Kreegs
•11y ago
</excerpt>
### Rank 3 of 38 — 0.86
<excerpt title="Local Ad">
From Wikipedia, the free encyclopedia
| "**Local Ad**" |  
| --- |  
| _The Office_ episode |  
|  The Dunder Mifflin graphic created by Pam for the "Local Ad" |  
| Episode no. | Season 4 Episode 9 |  
| Directed by | Jason Reitman |  
| Written by | B. J. Novak |  
| Cinematography by | Randall Einhorn |  
| Editing by | David Rogers |  
| Production code | 409 |  
| Original air date | October 25,2007[[1]](https://en.wikipedia.org/wiki/Local_Ad#cite_note-Spider-1) |  
| Guest appearances |  
| * Kyle Bornheimer as Adman * Andy Buckley as David Wallace * Tim Kang as Koh |  
| Episode chronology |  
| ←**Previous** "Money"**Next**→ "Branch Wars" |  
| _The Office_(American season 4) |  
| List of episodes |
"**Local Ad**" is the ninth episode of the fourth season of the American comedytelevision series_The Office_ and the show's sixty-second episode overall. The episode was written by B. J. Novak, who also acts in the show as Ryan Howard, and directed by Jason Reitman. It originally aired in the United States on October 25, 2007, on NBC.[[1]](https://en.wikipedia.org/wiki/Local_Ad#cite_note-Spider-1)
After a video team is brought to the office to create a commercial for the company, Michael decides that the employees of the Scranton branch of Dunder Mifflin can create a better commercial. While the majority of the staff work on the commercial, Dwight, still depressed from his break-up with Angela, instead chooses to play a computer game.

## Plot
When Michael Scott learns that the Scranton branch's participation in a Dunder Mifflin television commercial is limited to five seconds of the staff waving at the camera, he dismisses the advertising consultants sent to the branch, and convinces the company's corporate headquarters to consider an alternative version that he will produce himself.
Michael asks Pam Beesly to design an animated logo, and she works all night on it.[[2]](https://en.wikipedia.org/wiki/Local_Ad#cite_note-CB-2)[[3]](https://en.wikipedia.org/wiki/Local_Ad#cite_note-PPL-3)Phyllis Vance's mission to enlist visiting author Sue Grafton to appear in the ad is unsuccessful. Headed by Darryl Philbin, a group of employees write and perform a jingle for the commercial, which Michael ultimately rejects. Andy Bernard, meanwhile, struggles throughout the day to recall the product name from an advertising jingle that contains the lyrics "Gimme a break. Gimme a break. Break me off a piece of that..."
Dwight Schrute, playing in the online virtual world of _Second Life_, has created an avatar named Dwight Shelford, also a paper salesman, patterned after his once-perfect real life. He now uses _Second Life_ as an escape from his real-life troubles, even creating a virtual _Second Life_, called _Second Second Life_. Jim Halpert creates his own avatar named Jim Samtanko, a guitar-playing Philadelphia sportswriter, and enters _Second Life_ in order to spy on Dwight.
Dwight reluctantly becomes Andy's confidante regarding his relationship with Angela Martin, Dwight's former girlfriend. Dwight's spirits are lifted when he learns that, during a makeout session with Andy, Angela cried, "Oh, D!". Andy assumes "D" is a diminutive for Andy.
</excerpt>
### Rank 4 of 38 — 0.84
<excerpt title="TIL that J.J. Abrams, Joss Whedon, Harold Ramis, Jon Favreau, Bryan ...">
# Comments Section
mild_gingervitis
•11y ago
**J.J. Abrams** - "_Cocktails_" (Season 3 Ep. 17)
**Joss Whedon** - "_Business School_" (Season 3 Ep. 16)
"_Branch Wars_" (Season 4 Ep. 6)
**Harold Ramis** - "_A Benihana Christmas_" (Season 3 Ep. 10)
"_Safety Training_" (Season 3 Ep. 19)
"_Beach Games_" (Season 3 Ep. 22)
"_The Delivery: Part 2_" (Season 6 Ep. 18)
**Jon Favreau** - "_Moving On_" (Season 9 Ep. 16)
**Bryan Cranston** - "_Work Bus_" (Season 9 Ep. 4)
**Jason Reitman** - "_Local Ad_" (Season 4 Ep. 5)
"_Frame Toby_" (Season 5 Ep. 8)
Atwenfor
•11y ago
Of course Cranston directed the one where they operate their business from the back of a vehicle.
Roller_ball
•11y ago
And Whedon directed the one with a bat and had some vampire jokes. This was back when he was mainly known for Buffy and Angel.
more reply
more reply
more reply
More replies
Bensas42
•11y ago
I always love getting surprised by their names in the episodes.
a_probiotic_disaster
•11y ago
Jon Favreau's episode was meh, but the rest of these are amazing episodes. Maybe even some of the best episodes.
[deleted]
•11y ago
That's actually what I think of Jon Favreau all the time, just meh.
[deleted]
•11y ago
Comment removed by moderator
more replies
more replies
more replies
More replies
more replies
more replies
more replies
[deleted]
•11y ago
I found a still from JJ Abrams episode. http://i.imgur.com/WjBrVRk.png
Reply  Share
[deleted]
•11y ago
Comment deleted by user
Reply  Share
more replies
more replies
More replies
Blitz_Kreegs
•11y ago
</excerpt>
### Rank 5 of 38 — 0.84
<excerpt title="8 Famous Directors You Didn't Know Worked on The Office">
# 8 Famous Directors You Didn't Know Worked on The Office
## Famous Directors Who Helmed Episodes of _The Office_
* * *

# 8 Famous Directors You Didn't Know Worked on The Office
## Amy Heckerling
Photo: Getty Images
Amy Heckerling is a legendary filmmaker known for making a seminal teen comedy in the 1980s,_Fast Times at Ridgemont High_,and a seminal teen comedy in the 1990s,_Clueless_. In the 2000s, when _The Office_ was still in its early days, she brought those gifts to the NBC series, directing the finale of the abbreviated first season, "Hot Girl," guest starring future multi-Oscar nominee Amy Adams.

# 8 Famous Directors You Didn't Know Worked on The Office
## Paul Feig
Photo: Getty Images
When _The Office_ launched, Paul Feig was still best known for his work in comedy television, having created the cult classics_Freaks & Geeks_and worked on shows like _Undeclared_ and _Arrested Development_. Along the way, before he broke through with _Bridesmaids_ a few years later, he became one of _The Office_'s most valuable directors. Between Season 2 and Season 7, Feig directed 14 episodes of _The Office_, including classics like "Office Olympics," the two-part Season 5 premiere "Weight Loss," and of course, arguably the best episode of _The Office_ ever made, "Dinner Party."

# 8 Famous Directors You Didn't Know Worked on The Office
## Harold Ramis
Photo: Getty Images
As a writer, actor, and director, Harold Ramis is a comedy legend, a multi-hyphenate who still found time to hang out with the Dunder Mifflin gang for a few episodes. Ramis ended up helming four episodes of the series over the course of its run, working primarily in Season 3, where he worked on stories like "Safety Training" and the two-part classic holiday episode "A Benihana Christmas."

# 8 Famous Directors You Didn't Know Worked on The Office
## Joss Whedon
Photo: Getty Images
Though Joss Whedon's work is often funny, he's not really known as a comedy storyteller. Still, that didn't stop the creator of _Buffy the Vampire Slayer_ from pitching in for a couple of episodes of _The Office_ as the series hit its stride. Over the course of its run, Whedon helmed two _Office_ episodes, including Season 3's"Business School" and the Season 4 classic "Branch Wars."
**RELATED:_The Office_ Ending Explained**

# 8 Famous Directors You Didn't Know Worked on The Office
## J.J. Abrams
Photo: Getty Images
By Season 3,_The Office_ was well on its way to becoming a TV icon, and that meant bigger and bigger names were getting in on the act. One of those big names for the show's third year was J.J. Abrams, creator of _Alias_ and _Lost_, fresh off the success of directing his first feature film,_Mission: Impossible III_. Abrams only helmed one episode of the series, but it's a memorable one: "Cocktail Party," a landmark moment in the relationship between Michael Scott (Steve Carell) and Jan Levinson (Melora Hardin).

# 8 Famous Directors You Didn't Know Worked on The Office
## Jason Reitman
Photo: Getty Images
The fall of 2007 was a very good time to be Jason Reitman. The _Thank You for Smoking_ director (and son of legendary comedy filmmaker Ivan Reitman) was launching his feature breakthrough _Juno_ at festivals, and he was also making his debut as a director on _The Office_. Reitman directed two episodes of the series, both very memorable: "Local Ad" in Season 4 and "Frame Toby" in Season 5.
</excerpt>

## Search 2 — query: ""Local Ad" The Office airing date 2007"
### Rank 1 of 188 — 0.92 (passed on)
<excerpt title="Local Ad">
From Wikipedia, the free encyclopedia
| "**Local Ad**" |  
| --- |  
| _The Office_ episode |  
|  The Dunder Mifflin graphic created by Pam for the "Local Ad" |  
| Episode no. | Season 4 Episode 9 |  
| Directed by | Jason Reitman |  
| Written by | B. J. Novak |  
| Cinematography by | Randall Einhorn |  
| Editing by | David Rogers |  
| Production code | 409 |  
| Original air date | October 25,2007[[1]](https://en.wikipedia.org/wiki/Local_Ad#cite_note-Spider-1) |  
| Guest appearances |  
| * Kyle Bornheimer as Adman * Andy Buckley as David Wallace * Tim Kang as Koh |  
| Episode chronology |  
| ←**Previous** "Money"**Next**→ "Branch Wars" |  
| _The Office_(American season 4) |  
| List of episodes |
"**Local Ad**" is the ninth episode of the fourth season of the American comedytelevision series_The Office_ and the show's sixty-second episode overall. The episode was written by B. J. Novak, who also acts in the show as Ryan Howard, and directed by Jason Reitman. It originally aired in the United States on October 25, 2007, on NBC.[[1]](https://en.wikipedia.org/wiki/Local_Ad#cite_note-Spider-1)
After a video team is brought to the office to create a commercial for the company, Michael decides that the employees of the Scranton branch of Dunder Mifflin can create a better commercial. While the majority of the staff work on the commercial, Dwight, still depressed from his break-up with Angela, instead chooses to play a computer game.

## Plot
When Michael Scott learns that the Scranton branch's participation in a Dunder Mifflin television commercial is limited to five seconds of the staff waving at the camera, he dismisses the advertising consultants sent to the branch, and convinces the company's corporate headquarters to consider an alternative version that he will produce himself.
Michael asks Pam Beesly to design an animated logo, and she works all night on it.[[2]](https://en.wikipedia.org/wiki/Local_Ad#cite_note-CB-2)[[3]](https://en.wikipedia.org/wiki/Local_Ad#cite_note-PPL-3)Phyllis Vance's mission to enlist visiting author Sue Grafton to appear in the ad is unsuccessful. Headed by Darryl Philbin, a group of employees write and perform a jingle for the commercial, which Michael ultimately rejects. Andy Bernard, meanwhile, struggles throughout the day to recall the product name from an advertising jingle that contains the lyrics "Gimme a break. Gimme a break. Break me off a piece of that..."
Dwight Schrute, playing in the online virtual world of _Second Life_, has created an avatar named Dwight Shelford, also a paper salesman, patterned after his once-perfect real life. He now uses _Second Life_ as an escape from his real-life troubles, even creating a virtual _Second Life_, called _Second Second Life_. Jim Halpert creates his own avatar named Jim Samtanko, a guitar-playing Philadelphia sportswriter, and enters _Second Life_ in order to spy on Dwight.
Dwight reluctantly becomes Andy's confidante regarding his relationship with Angela Martin, Dwight's former girlfriend. Dwight's spirits are lifted when he learns that, during a makeout session with Andy, Angela cried, "Oh, D!". Andy assumes "D" is a diminutive for Andy.
</excerpt>
### Rank 2 of 188 — 0.90
<excerpt title="The Office (U.S. TV series) - Wikipedia, the free encyclopedia">
## [edit]References
61.   **^**NBC Universal (2007-01-17). _NBC renews hit series The Office \_,\_ My Name is Earl \_,\_ Heroes \_, and\_ Law & Order: Special Victims Unit \_for full season of episodes in 2007-'08\__. Press release. http://www.nbcumv.com/release_detail.nbc/entertainment-20070117000000-nbcrenewshitserie.html. Retrieved on 2008-04-12.  
62.   **^** Serpe, Gina. Strike Support: _Office_, Stars Call In Sick. E! News, 2007-11-07. Retrieved on 2008-04-12.  
63.   **^** Carter, Bill. "No Pause Button: TV Studios and Writers Play Catch-Up After Strike." _The New York Times_, 2008-02-13 Retrieved on 2008-04-12.  
64.   **^**"Branch Wars". written by Mindy Kaling, directed by Joss Whedon. _The Office_ (NBC) (58). 2007-11-01.  
65.   **^**"Dunder Mifflin Infinity". written by Michael Schur and directed by Craig Zisk. _The Office_ (NBC) (53). 2007-10-04.  
66.   **^**"Money". written and directed by Paul Lieberstein. _The Office_ (NBC) (56). 2007-10-18.  
67.   ^ _**a**__**b**_"Fun Run". written and directed by Greg Daniels. _The Office_ (NBC) (53). 2007-09-27.  
68.   **^**"Local Ad". written by B.J. Novak and directed by Jason Reitman. _The Office_ (NBC) (56). 2007-10-25.  
69.   **^**Goodbye Toby Episode Recap NBC.com
</excerpt>
### Rank 3 of 188 — 0.89
<excerpt title="The Office (U.S. TV series) - Wikipedia, the free encyclopedia">
## [edit]References
53.   **^**"The Client". written by Paul Lieberstein, directed by Greg Daniels. _The Office_ (NBC) (13). 2005-11-08.  
54.   **^**"Valentine's Day". written by Michael Schur, directed by Greg Daniels. _The Office_ (NBC) (22). 2006-02-09.  
55.   **^**"Office Olympics". written by Michael Schur, directed by Paul Feig. _The Office_ (NBC) (9). 2005-10-04.  
56.   **^**"Drug Testing". written by Jennifer Celotta, directed by Greg Daniels. _The Office_ (NBC) (26). 2006-04-27. A deleted scene in that episode suggests he never actually was a deputy.  
57.   **^**Rizzo, Francis (2006-09-12). "_The Office_ - Season Two". DVD Talk. http://www.dvdtalk.com/reviews/23501/office-season-two-the/. Retrieved on 2008-08-15.  
58.   **^**"Branch Closing". written by Michael Schur, directed by Tucker Gates. _The Office_ (NBC) (35). 2006-11-09.  
59.   **^**"Phyllis' Wedding". written by Caroline Williams, directed by Ken Whittingham. _The Office_ (NBC) (43). 2007-02-08.  
60.   **^**"The Return". written by Michael Schur, Lee Eisenberg and Gene Stupnitsky, directed by Greg Daniels. _The Office_ (NBC) (41). 2007-01-18.  

## [edit]References
61.   **^**NBC Universal (2007-01-17). _NBC renews hit series The Office \_,\_ My Name is Earl \_,\_ Heroes \_, and\_ Law & Order: Special Victims Unit \_for full season of episodes in 2007-'08\__. Press release. http://www.nbcumv.com/release_detail.nbc/entertainment-20070117000000-nbcrenewshitserie.html. Retrieved on 2008-04-12.  
62.   **^** Serpe, Gina. Strike Support: _Office_, Stars Call In Sick. E! News, 2007-11-07. Retrieved on 2008-04-12.  
63.   **^** Carter, Bill. "No Pause Button: TV Studios and Writers Play Catch-Up After Strike." _The New York Times_, 2008-02-13 Retrieved on 2008-04-12.  
64.   **^**"Branch Wars". written by Mindy Kaling, directed by Joss Whedon. _The Office_ (NBC) (58). 2007-11-01.  
65.   **^**"Dunder Mifflin Infinity". written by Michael Schur and directed by Craig Zisk. _The Office_ (NBC) (53). 2007-10-04.  
66.   **^**"Money". written and directed by Paul Lieberstein. _The Office_ (NBC) (56). 2007-10-18.  
67.   ^ _**a**__**b**_"Fun Run". written and directed by Greg Daniels. _The Office_ (NBC) (53). 2007-09-27.  
68.   **^**"Local Ad". written by B.J. Novak and directed by Jason Reitman. _The Office_ (NBC) (56). 2007-10-25.  
69.   **^**Goodbye Toby Episode Recap NBC.com
</excerpt>
### Rank 4 of 188 — 0.80
<excerpt title="The Office (U.S.) on The Incomparable">
## The Office
### Discussed in these episodes
##### 65 One Sheet of Paper (S4E13)
After Mikah spilled coffee on their single sheet of white paper, he and Tiff head back to the office to grab another sheet and talk about “Job Fair.” This episode of “The Office” aired on May 8, 2008.
*   Somehow I Manage August 22, 2019 Earlier today Stanley sassed me.

## The Office
### Discussed in these episodes
##### 64 Clash of the Titans (S4E12)
After Mikah gets a little sassy with Tiff, the two resolve their differences and sit down to discuss, “Did I Stutter?” This episode of “The Office” aired on May 1, 2008.
*   Somehow I Manage August 8, 2019 Letâ€™s hear it for the boys.

## The Office
### Discussed in these episodes
##### 63 One-Stop Customer Experience (S4E11)
After Mikah forgot to let security know they’d be staying late, Tiff and he decided to hop the fence so the two could meet up to discuss “Night Out.” This episode of “The Office” aired on April 24, 2008.
*   Somehow I Manage June 20, 2019 Could have done this over email

## The Office
### Discussed in these episodes
##### 62 The Five Families (S4E10)
After Tiff and Mikah negotiate their way into some new, comfortable chairs, the two discuss “Chair Model.” This episode of “The Office” aired on April 17, 2008.
*   Somehow I Manage June 13, 2019 Snip snap, snip snap, snip snap

## The Office
### Discussed in these episodes
##### 61 That One Night (S4E9)
After Tiff and Mikah perfect their “That One Night” duet, the two sit down to discuss “Dinner Party.” This episode of “The Office” aired on April 10, 2008.
*   Somehow I Manage May 30, 2019 Tan almost everywhere. Jan almost everywhere.

## The Office
### Discussed in these episodes
##### 60 XOXO Michael (S4E8)
After preparing their answers for the lawyers, Tiff and Mikah carefully discuss “The Deposition.” This episode of “The Office” aired on November 15, 2007.
*   Somehow I Manage May 23, 2019 I HAVE HEMORRHOIDS!

## The Office
### Discussed in these episodes
##### 59 The Overkill Killer (S4E7)
After crafting a sturdy pants tent, Tiff and Mikah discuss “Survivor Man.” This episode of “The Office” aired on November 8, 2007.
*   Somehow I Manage May 16, 2019 We will burn Utica to the ground.

## The Office
### Discussed in these episodes
##### 58 Big Butt, Bigger Heart (S4E6)
After Tiff and Mikah infiltrate Utica, the two discuss “Branch Wars.” This episode of “The Office” aired on November 1, 2007.
*   Somehow I Manage May 9, 2019 Limitless paper in a paperless world.

## The Office
### Discussed in these episodes
##### 57 Second Second Life (S4E5)
After narrowly escaping Second Life, Tiff and Mikah have a nice chat about “Local Ad.” This episode of “The Office” aired on October 25, 2007.
*   Somehow I Manage May 2, 2019 I declare BANKRUPTCY!

## The Office
### Discussed in these episodes
##### 56 The Beets Motel (S4E4)
Tiff and Mikah check out the new agrotourism industry before settling in to talk about “Money.” This episode of “The Office” aired on October 18, 2007.
*   Somehow I Manage April 25, 2019 It’s going to get all stupid up in here!
</excerpt>
### Rank 5 of 188 — 0.78
<excerpt title="The Office Season 4 Episode Guide">
****
**Episode 1 – Fun Run – Original Air Date – 09/27/2007**
TV Ratings : 9.67 Million Viewers | Adults 18-49: 5.1/12&nbsp;
THE RUN FOR THE CURE-SPECIAL ONE-HOUR PREMIERE – A freak accident causes Michael (Golden Globe winner Steve Carell) to feel the office is cursed. He explores the religious beliefs of his employees before deciding to hold a charity 5K fun run. Meanwhile, further developments in the romances of Pam (Jenna Fischer) and Jim (John Krasinski), and Dwight (Rainn Wilson) and Angela (Angela Kinsey) are explored. B.J. Novak, Melora Hardin, Ed Helms, Leslie David Baker, Brian Baumgartner, Kate Flannery, Oscar Nunez, Phyllis Smith, Paul Lieberstein, Mindy Kaling, Craig Robinson and Creed Bratton also star.
**Episode 2 – Dunder Mifflin Infinity – Original Air Date – 10/04/2007**
TV Ratings : 8.49 Million Viewers | Adults 18-49: 4.5/11
THERE&#39;S A NEW BOSS IN TOWN – Much to the dismay of Michael (Golden Globe winner Steve Carell) and many of the employees, Ryan (B.J. Novak) returns to the Scranton branch of Dunder Mifflin to bring the company into the digital age. Angela (Angela Kinsey) is still upset about her cat. Rainn Wilson, John Krasinski, Jenna Fischer, Melora Hardin, Ed Helms, Leslie David Baker, Brian Baumgartner, Kate Flannery, Oscar Nunez, Phyllis Smith, Paul Lieberstein, Mindy Kaling, Craig Robinson and Creed Bratton also star.
**Episode 3 – Launch Party – Original Air Date – 10/11/2007**

THE WORLDWIDE WEB–The Dunder Mifflin Infinity website is launching and Michael (Golden Globe winner Steve Carell) is excited about going to the big launch party in New York while Angela (Angela Kinsey) plans a satellite party for the Scranton branch. Meanwhile, Dwight (Rainn Wilson) competes against the website to see who can sell the most paper in one day. John Krasinski, Jenna Fischer, B.J. Novak, Melora Hardin, Ed Helms, Leslie David Baker, Brian Baumgartner, Kate Flannery, Mindy Kaling, Paul Lieberstein, Oscar Nunez, Phyllis Smith, Creed Bratton, and Craig Robinson also star.
**Episode 4 – Money – Original Air Date – 10/18/2007**
EASY COME, EASY GO–As Jan (Melora Hardin) renovates the condo, Michael (Golden Globe winner Steve Carell) confronts his growing debt every way he can, which includes pressuring his employees for a loan. Pam (Jenna Fischer) and Jim (John Krasinski) spend a night out on Dwight&#39;s (Rainn Wilson) family farm, now a bed and breakfast. B.J. Novak, Ed Helms, Leslie David Baker, Brian Baumgartner, Kate Flannery, Oscar Nunez, Phyllis Smith, Paul Lieberstein, Mindy Kaling, Creed Bratton and Craig Robinson also star.
**Episode 5 – Local Ad – Original Air Date – 10/25/2007**
THE WONDERFUL WORLD OF ADVERTISING– When the Scranton branch is asked to participate in a Dunder Mifflin ad, Michael (Golden Globe winner Steve Carell) seizes his chance to exhibit his creativity. Meanwhile, Dwight (Rainn Wilson) explores the online world of Second Life. John Krasinski, Jenna Fischer, B.J Novak, Ed Helms, Leslie David Baker, Brian Baumgartner, Kate Flannery, Mindy Kaling, Angela Kinsey, Paul Lieberstein, Oscar Nunez, Phyllis Smith, Creed Bratton and Craig Robinson also star.
**Episode 6 – Branch Wars – Original Air Date – 11/01/2007**
</excerpt>

## Search 3 — query: "space shuttle launch October 23 2007"
### Rank 1 of 120 — 0.74 (passed on)
<excerpt title="Florida Rocket & Space Shuttle Launches 2007: Archive Guide">
**This page is now a 2007 launch archive, not a live schedule.** The original version mixed historical listings with future-tense planning language that no longer helps anyone. In 2026, the better use is to keep a smaller, verified archive of notable 2007 Space Coast launches and point real trip planners toward current official sources.
If you are planning an actual launch day, use our future launch schedules guide and rocket launch viewing guide instead. Kennedy only publishes officially announced launch information, and dates can shift very quickly.
Florida’s 2007 launch year sits in the later Shuttle era, but it already shows the mix of station assembly work and broader science missions that kept the Space Coast busy.

## The current 2026 planning answer first
As of **July 12, 2026**, the official Kennedy ticket system still shows **1-day admission at $77 for adults and $67 for children**, and **2-day admission at $91 and $81**. Kennedy’s launch pages also show that some launch opportunities are **included with admission**, while premium days may add **$75**, **$99** or more in transportation or special-event charges.
That is the only reliable price framework for a real trip. Everything below is here for historical context, not for booking decisions.

## Notable officially documented Florida launches from 2007
*   **June 8, 2007 - STS-117:** NASA says **Atlantis** launched from **Pad 39A** at **7:38:04 p.m. EDT** on the STS-117 International Space Station assembly mission.  
*   **August 4, 2007 - Mars Phoenix:** NASA Science says the **Phoenix** Mars lander launched from **Cape Canaveral Air Force Station** on a **Delta II**.  
*   **August 8, 2007 - STS-118:** NASA says **Endeavour** launched on **August 8, 2007** for the 22nd shuttle flight to the International Space Station.  
*   **October 23, 2007 - STS-120:** NASA says **Discovery** launched on **October 23, 2007** and carried the **Harmony** multi-port module for the station.

## Why 2007 stands out
2007 is a useful archive year because it captures the later Shuttle program doing exactly what it was built to do best: heavy station assembly and major international hardware delivery. At the same time, Cape Canaveral was still sending science missions like **Phoenix** beyond Earth orbit. That combination makes the year stronger as a history page than as a raw date list.
For current launch-day decisions, keep this archive alongside NASA Kennedy Space Center, Kennedy Space Center tickets and Space Shuttle Atlantis. Those are much more useful for a real 2026 holiday than a year-by-year archive page.
</excerpt>
### Rank 2 of 120 — 0.70
<excerpt title="STS-120">
STS-120  
Scott E. Parazynski performs a repair of a torn solar panel on the P6 truss, reinstalled on the ISS four days earlier.  
NamesSpace Transportation System-120
Mission type ISS assembly  
OperatorNASA  
COSPAR ID2007-050A  
SATCAT no.32272  
Mission duration 15 days, 2 hours, 24 minutes  
Distance travelled 10,060,000 kilometres (6,250,000 mi)[[NASA 1]](https://en.wikipedia.org/wiki/STS-120#cite_note-finalsr-1)  
Orbits completed 238
Spacecraft properties  
SpacecraftSpace Shuttle_Discovery_  
Launch mass 121,643 kilograms (268,177 lb)[[1]](https://en.wikipedia.org/wiki/STS-120#cite_note-2)  
Landing mass 91,578 kilograms (201,895 lb)[[NASA 2]](https://en.wikipedia.org/wiki/STS-120#cite_note-presskit-3)
Crew  
Crew size 7  
Members*   Pamela A. Melroy
*   George D. Zamka  
*   Douglas H. Wheelock  
*   Stephanie Wilson  
*   Scott E. Parazynski  
*   Paolo A. Nespoli  
Launching*   Daniel M. Tani  
Landing*   Clayton Anderson
Start of mission  
Launch date October 23, 2007, 15:38:19 UTC  
Launch siteKennedy, LC-39A
End of mission  
Landing date November 7, 2007, 18:01:18 UTC  
Landing site Kennedy, SLF Runway 33

Orbital parameters  
Reference systemGeocentric  
RegimeLow Earth  
Perigee altitude340 kilometres (210 mi)[[NASA 3]](https://en.wikipedia.org/wiki/STS-120#cite_note-spacewarn-4)  
Apogee altitude344 kilometres (214 mi)[[NASA 3]](https://en.wikipedia.org/wiki/STS-120#cite_note-spacewarn-4)  
Inclination51.6 degrees[[2]](https://en.wikipedia.org/wiki/STS-120#cite_note-ql-5)  
Period91.6 minutes[[2]](https://en.wikipedia.org/wiki/STS-120#cite_note-ql-5)
Docking with ISS  
Docking portPMA-2
(Destiny forward)  
Docking date 25 October 2007 12:40 UTC  
Undocking date 5 November 2007 10:32 UTC  
Time docked 10 days, 21 hours, 52 minutes
(left to right) Parazynski, Wheelock, Wilson, Zamka, Melroy, Tani and Nespoli
Space Shuttle program
←STS-118
STS-122→
**STS-120** was a Space Shuttle mission to the International Space Station (ISS) that launched on October 23, 2007, from the Kennedy Space Center, Florida.[[NASA 4]](https://en.wikipedia.org/wiki/STS-120#cite_note-main-6) The mission is also referred to as **ISS-10A** by the ISS program. STS-120 delivered the _Harmony_ module and reconfigured a portion of the station in preparation for future assembly missions.[[NASA 2]](https://en.wikipedia.org/wiki/STS-120#cite_note-presskit-3) STS-120 was flown by Space Shuttle_Discovery_, and was the twenty-third Space Shuttle mission to the ISS. It was Discovery's 34th flight.
Two commanders: Melroy and Whitson place the STS-120 mission insignia on the wall of the newly installed _Harmony_ module.
</excerpt>
### Rank 3 of 120 — 0.70
<excerpt title="STS-120">
Orbital parameters  
Reference systemGeocentric  
RegimeLow Earth  
Perigee altitude340 kilometres (210 mi)[[NASA 3]](https://en.wikipedia.org/wiki/STS-120#cite_note-spacewarn-4)  
Apogee altitude344 kilometres (214 mi)[[NASA 3]](https://en.wikipedia.org/wiki/STS-120#cite_note-spacewarn-4)  
Inclination51.6 degrees[[2]](https://en.wikipedia.org/wiki/STS-120#cite_note-ql-5)  
Period91.6 minutes[[2]](https://en.wikipedia.org/wiki/STS-120#cite_note-ql-5)
Docking with ISS  
Docking portPMA-2
(Destiny forward)  
Docking date 25 October 2007 12:40 UTC  
Undocking date 5 November 2007 10:32 UTC  
Time docked 10 days, 21 hours, 52 minutes
(left to right) Parazynski, Wheelock, Wilson, Zamka, Melroy, Tani and Nespoli
Space Shuttle program
←STS-118
STS-122→
**STS-120** was a Space Shuttle mission to the International Space Station (ISS) that launched on October 23, 2007, from the Kennedy Space Center, Florida.[[NASA 4]](https://en.wikipedia.org/wiki/STS-120#cite_note-main-6) The mission is also referred to as **ISS-10A** by the ISS program. STS-120 delivered the _Harmony_ module and reconfigured a portion of the station in preparation for future assembly missions.[[NASA 2]](https://en.wikipedia.org/wiki/STS-120#cite_note-presskit-3) STS-120 was flown by Space Shuttle_Discovery_, and was the twenty-third Space Shuttle mission to the ISS. It was Discovery's 34th flight.
Two commanders: Melroy and Whitson place the STS-120 mission insignia on the wall of the newly installed _Harmony_ module.

As commander of STS-120, Pamela Melroy became the second woman (after Eileen Collins) to command a Space Shuttle mission.[[3]](https://en.wikipedia.org/wiki/STS-120#cite_note-second-7) Additionally, the Expedition 16 crew that received STS-120 was commanded by Peggy Whitson, the first female ISS commander.[[4]](https://en.wikipedia.org/wiki/STS-120#cite_note-space2-8)[[5]](https://en.wikipedia.org/wiki/STS-120#cite_note-fox2-9) The flight of STS-120 thus became the first time two female mission commanders were in space at the same time.[[6]](https://en.wikipedia.org/wiki/STS-120#cite_note-chicks-10)[[7]](https://en.wikipedia.org/wiki/STS-120#cite_note-msnbc1-11)[[8]](https://en.wikipedia.org/wiki/STS-120#cite_note-history1-12)

### Crew prior to the Space Shuttle _Columbia_ disaster
[edit]
Prior to the Space Shuttle _Columbia_ disaster, the original crew manifest for STS-120 was:
The STS-120 mission patch was designed by Michael Foreman before he was reassigned to STS-123.
</excerpt>
### Rank 4 of 120 — 0.70
<excerpt title="STS-120">
# STS-120
## Mission Facts
### Crew:
Pam Melroy, Commander
George Zamka, Pilot
Scott Parazynski, Mission Specialist
Doug Wheelock, Mission Specialist
Stephanie Wilson, Mission Specialist
Paolo Nespoli, Mission Specialist
Daniel Tani, Flight Engineer, Embarking to International Space Station
Clay Anderson, Flight Engineer, Returning from International Space Station

# STS-120
## **STS-120: Perfect Beginning and End to a Spectacular Mission**
Carrying a crew of seven astronauts, space shuttle Discovery began mission STS-120 with a brilliant, on-time launch from NASA’s Kennedy Space Center in Florida on Oct. 23, 2007.
The prime payload was an Italian-built U.S. module called Harmony. The construction mission’s two primary goals were to attach Harmony to the International Space Station in a temporary position and relocate the P6 truss segment and its solar arrays to the end of the port side of the station.
The mission, commanded by Pam Melroy, also delivered Mission Specialist Dan Tani to the space station, where he replaced astronaut Clay Anderson who returned to Earth on Discovery after spending five months onboard the station.
The crew conducted four spacewalks during the mission, including one which pitted shuttle, station and ground crews against a snagged and torn solar array.
Outstanding work by the teams resulted in a repaired, fully deployed and functional array, paving the way for upcoming missions.
After 15 days and 238 orbits of the Earth, Discovery and crew were welcomed back to Florida on Nov. 7 where they touched down on Runway 33 at Kennedy’s Shuttle Landing Facility.

# STS-120
## STS-120
10 Images
Go To Gallery
Go To Gallery

# STS-120
## Resources


# STS-120
## STS-120 Press Kit
Get an overview of the STS mission, its crew and activities during this mission.

# STS-120
## Discovery Fact Sheet
An overview of this shuttle's flights.

# STS-120
## STS-120 Mission Poster
View the official poster for this mission.

# STS-120
## STS-120 Crew Poster
View the official crew poster for this mission.

# STS-120
## Shuttle News
See All Shuttle News
Article 3 Min Read Through NASA’s Lens: Capturing Space Shuttle Endeavour’s Move to LA
Article 3 Min Read I Am Artemis: Allison Mjoen
Image Article 2 Min Read Shannon Lucid’s Record-Setting Mission Aboard Mir Image Article 2 Min Read NASA Unveils Enterprise, the First Space Shuttle
Featured Story

# Retired Space Shuttle Locations
Shuttle Atlantis – Kennedy Space Center Visitor Complex Shuttle Discovery – Steven F. Udvar-Hazy Center Shuttle Endeavour – California Science…
Read the Story
Keep Exploring

# Retired Space Shuttle Locations
## Discover More Topics From NASA
Overview of NASA’s Missions Humans In Space ### Humans to Mars Like the Moon, Mars is a rich destination for scientific discovery and a driver of technologies that will enable humans… Astronauts
</excerpt>
### Rank 5 of 120 — 0.66
<excerpt title="STS-120">
# STS-120 - NASA
## Suggested Searches
### Highlights
11 min read ### La NASA anuncia la cobertura de la misión lunar Artemis II article 8 months ago 15 min read ### Agenda diaria de la misión a la Luna de Artemis II de la NASA article 8 months ago 6 min read ### La NASA refuerza Artemis: añade una misión y perfecciona su arquitectura general article 9 months ago

# STS-120
Occurred 22 years ago
STS-120 was the 23rd shuttle mission to the International Space Station, and launched an Italian-built U.S. multi-port module for the station.
Orbiter
Discovery
mission duration
15 days, 2 hours, 23 minutes
Launch
Oct. 23, 2007
Landing
Nov. 7, 2007
These seven astronauts took a break from training to pose for the STS-120 crew portrait. Pictured from the left are astronauts Scott E. Parazynski, Douglas H. Wheelock, Stephanie D. Wilson, all mission specialists; George D. Zamka, pilot; Pamela A. Melroy, commander; Daniel M. Tani, Expedition 16 flight engineer; and Paolo A. Nespoli, mission specialist representing the European Space Agency (ESA). The crew members were attired in training versions of their shuttle launch and entry suits. Tani joined Expedition 16 as flight engineer after launching to the International Space Station (ISS) and is scheduled to return home on mission STS-122. STS-120 launched October 23, 2007 with the main objectives of installing the U.S. Node 2, Harmony, and the relocation and deployment of the P6 truss to its permanent location.
NASA

# STS-120
## Mission Facts
**Orbiter:** Discovery
**Mission:**Space Station Assembly Mission 10A
**Primary Payload:** Harmony Node 2
**Launch Date:** Oct. 23, 2007
**Launch Time:** 11:38 a.m. EDT
**Launch Pad:** 39A
**Landing Date:** Nov. 7, 2007
**Landing Time:** 1:01 p.m. EST
**Landing Site:** Kennedy Space Center
**Inclination/Altitude:** 51.6 degrees/122 nautical miles

# STS-120
## Mission Facts
### Crew:
Pam Melroy, Commander
George Zamka, Pilot
Scott Parazynski, Mission Specialist
Doug Wheelock, Mission Specialist
Stephanie Wilson, Mission Specialist
Paolo Nespoli, Mission Specialist
Daniel Tani, Flight Engineer, Embarking to International Space Station
Clay Anderson, Flight Engineer, Returning from International Space Station
</excerpt>

## Search 4 — query: "STS-120 crew list birthdates"
### Rank 1 of 84 — 0.56 (passed on)
<excerpt title="STS-120">
# STS-120 - NASA
## Suggested Searches
### Highlights
11 min read ### La NASA anuncia la cobertura de la misión lunar Artemis II article 8 months ago 15 min read ### Agenda diaria de la misión a la Luna de Artemis II de la NASA article 8 months ago 6 min read ### La NASA refuerza Artemis: añade una misión y perfecciona su arquitectura general article 9 months ago

# STS-120
Occurred 22 years ago
STS-120 was the 23rd shuttle mission to the International Space Station, and launched an Italian-built U.S. multi-port module for the station.
Orbiter
Discovery
mission duration
15 days, 2 hours, 23 minutes
Launch
Oct. 23, 2007
Landing
Nov. 7, 2007
These seven astronauts took a break from training to pose for the STS-120 crew portrait. Pictured from the left are astronauts Scott E. Parazynski, Douglas H. Wheelock, Stephanie D. Wilson, all mission specialists; George D. Zamka, pilot; Pamela A. Melroy, commander; Daniel M. Tani, Expedition 16 flight engineer; and Paolo A. Nespoli, mission specialist representing the European Space Agency (ESA). The crew members were attired in training versions of their shuttle launch and entry suits. Tani joined Expedition 16 as flight engineer after launching to the International Space Station (ISS) and is scheduled to return home on mission STS-122. STS-120 launched October 23, 2007 with the main objectives of installing the U.S. Node 2, Harmony, and the relocation and deployment of the P6 truss to its permanent location.
NASA

# STS-120
## Mission Facts
**Orbiter:** Discovery
**Mission:**Space Station Assembly Mission 10A
**Primary Payload:** Harmony Node 2
**Launch Date:** Oct. 23, 2007
**Launch Time:** 11:38 a.m. EDT
**Launch Pad:** 39A
**Landing Date:** Nov. 7, 2007
**Landing Time:** 1:01 p.m. EST
**Landing Site:** Kennedy Space Center
**Inclination/Altitude:** 51.6 degrees/122 nautical miles

# STS-120
## Mission Facts
### Crew:
Pam Melroy, Commander
George Zamka, Pilot
Scott Parazynski, Mission Specialist
Doug Wheelock, Mission Specialist
Stephanie Wilson, Mission Specialist
Paolo Nespoli, Mission Specialist
Daniel Tani, Flight Engineer, Embarking to International Space Station
Clay Anderson, Flight Engineer, Returning from International Space Station
</excerpt>
### Rank 2 of 84 — 0.55
<excerpt title="STS-120">
STS-120  
Scott E. Parazynski performs a repair of a torn solar panel on the P6 truss, reinstalled on the ISS four days earlier.  
NamesSpace Transportation System-120
Mission type ISS assembly  
OperatorNASA  
COSPAR ID2007-050A  
SATCAT no.32272  
Mission duration 15 days, 2 hours, 24 minutes  
Distance travelled 10,060,000 kilometres (6,250,000 mi)[[NASA 1]](https://en.wikipedia.org/wiki/STS-120#cite_note-finalsr-1)  
Orbits completed 238
Spacecraft properties  
SpacecraftSpace Shuttle_Discovery_  
Launch mass 121,643 kilograms (268,177 lb)[[1]](https://en.wikipedia.org/wiki/STS-120#cite_note-2)  
Landing mass 91,578 kilograms (201,895 lb)[[NASA 2]](https://en.wikipedia.org/wiki/STS-120#cite_note-presskit-3)
Crew  
Crew size 7  
Members*   Pamela A. Melroy
*   George D. Zamka  
*   Douglas H. Wheelock  
*   Stephanie Wilson  
*   Scott E. Parazynski  
*   Paolo A. Nespoli  
Launching*   Daniel M. Tani  
Landing*   Clayton Anderson
Start of mission  
Launch date October 23, 2007, 15:38:19 UTC  
Launch siteKennedy, LC-39A
End of mission  
Landing date November 7, 2007, 18:01:18 UTC  
Landing site Kennedy, SLF Runway 33

Orbital parameters  
Reference systemGeocentric  
RegimeLow Earth  
Perigee altitude340 kilometres (210 mi)[[NASA 3]](https://en.wikipedia.org/wiki/STS-120#cite_note-spacewarn-4)  
Apogee altitude344 kilometres (214 mi)[[NASA 3]](https://en.wikipedia.org/wiki/STS-120#cite_note-spacewarn-4)  
Inclination51.6 degrees[[2]](https://en.wikipedia.org/wiki/STS-120#cite_note-ql-5)  
Period91.6 minutes[[2]](https://en.wikipedia.org/wiki/STS-120#cite_note-ql-5)
Docking with ISS  
Docking portPMA-2
(Destiny forward)  
Docking date 25 October 2007 12:40 UTC  
Undocking date 5 November 2007 10:32 UTC  
Time docked 10 days, 21 hours, 52 minutes
(left to right) Parazynski, Wheelock, Wilson, Zamka, Melroy, Tani and Nespoli
Space Shuttle program
←STS-118
STS-122→
**STS-120** was a Space Shuttle mission to the International Space Station (ISS) that launched on October 23, 2007, from the Kennedy Space Center, Florida.[[NASA 4]](https://en.wikipedia.org/wiki/STS-120#cite_note-main-6) The mission is also referred to as **ISS-10A** by the ISS program. STS-120 delivered the _Harmony_ module and reconfigured a portion of the station in preparation for future assembly missions.[[NASA 2]](https://en.wikipedia.org/wiki/STS-120#cite_note-presskit-3) STS-120 was flown by Space Shuttle_Discovery_, and was the twenty-third Space Shuttle mission to the ISS. It was Discovery's 34th flight.
Two commanders: Melroy and Whitson place the STS-120 mission insignia on the wall of the newly installed _Harmony_ module.
</excerpt>
### Rank 3 of 84 — 0.50
<excerpt title="STS-120 Facts for Kids">
Quick facts for kids
STS-120  
Astronaut Scott Parazynski fixes a torn solar panel on the International Space Station.
Mission type ISS assembly  
OperatorNASA  
Mission duration 15 days, 2 hours, 24 minutes.  
Distance travelled 10,060,000 kilometres (6,250,000 mi)  
Orbits completed 238
Spacecraft properties  
SpacecraftSpace Shuttle_Discovery_  
Launch mass 129,823 kilograms (286,211 lb)  
Landing mass 91,578 kilograms (201,895 lb)
Crew  
Crew size 7  
Members*   Pamela A. Melroy
*   George D. Zamka  
*   Douglas H. Wheelock  
*   Stephanie Wilson  
*   Scott E. Parazynski  
*   Paolo A. Nespoli  
Launching*   Daniel M. Tani  
Landing*   Clayton Anderson
Start of mission  
Launch date 23 October 2007, 15:38:19 UTC  
Launch siteKennedyLC-39A
End of mission  
Landing date 7 November 2007, 18:01:18 UTC  
Landing siteKennedy SLF Runway 33
Orbital parameters  
Reference systemGeocentric  
RegimeLow Earth  
Perigee340 kilometres (210 mi)  
Apogee344 kilometres (214 mi)  
Inclination51.6 degrees  
Period91.6 minutes
Docking with ISS  
Docking port PMA-2
(Destiny forward)  
Docking date 25 October 2007 12:40 UTC  
Undocking date 5 November 2007 10:32 UTC  
Time docked 10 days, 21 hours, 52 minutes
(left to right) Parazynski, Wheelock, Wilson, Zamka, Melroy, Tani and Nespoli
Space Shuttle program
←STS-118
STS-122→

**STS-120** was a Space Shuttle mission to the International Space Station (ISS). It launched on October 23, 2007, from the Kennedy Space Center in Florida. This mission was also known as **ISS-10A** by the ISS program. The main goal of STS-120 was to deliver the _Harmony_ module. It also helped prepare the space station for future parts to be added. The mission used the Space Shuttle _Discovery_ (also known as Space Shuttle_Discovery_). It was the 23rd Space Shuttle mission to visit the ISS.
</excerpt>
### Rank 4 of 84 — 0.49
<excerpt title="STS-120">
# STS-120
## Mission Facts
### Crew:
Pam Melroy, Commander
George Zamka, Pilot
Scott Parazynski, Mission Specialist
Doug Wheelock, Mission Specialist
Stephanie Wilson, Mission Specialist
Paolo Nespoli, Mission Specialist
Daniel Tani, Flight Engineer, Embarking to International Space Station
Clay Anderson, Flight Engineer, Returning from International Space Station

# STS-120
## **STS-120: Perfect Beginning and End to a Spectacular Mission**
Carrying a crew of seven astronauts, space shuttle Discovery began mission STS-120 with a brilliant, on-time launch from NASA’s Kennedy Space Center in Florida on Oct. 23, 2007.
The prime payload was an Italian-built U.S. module called Harmony. The construction mission’s two primary goals were to attach Harmony to the International Space Station in a temporary position and relocate the P6 truss segment and its solar arrays to the end of the port side of the station.
The mission, commanded by Pam Melroy, also delivered Mission Specialist Dan Tani to the space station, where he replaced astronaut Clay Anderson who returned to Earth on Discovery after spending five months onboard the station.
The crew conducted four spacewalks during the mission, including one which pitted shuttle, station and ground crews against a snagged and torn solar array.
Outstanding work by the teams resulted in a repaired, fully deployed and functional array, paving the way for upcoming missions.
After 15 days and 238 orbits of the Earth, Discovery and crew were welcomed back to Florida on Nov. 7 where they touched down on Runway 33 at Kennedy’s Shuttle Landing Facility.

# STS-120
## STS-120
10 Images
Go To Gallery
Go To Gallery

# STS-120
## Resources


# STS-120
## STS-120 Press Kit
Get an overview of the STS mission, its crew and activities during this mission.

# STS-120
## Discovery Fact Sheet
An overview of this shuttle's flights.

# STS-120
## STS-120 Mission Poster
View the official poster for this mission.

# STS-120
## STS-120 Crew Poster
View the official crew poster for this mission.

# STS-120
## Shuttle News
See All Shuttle News
Article 3 Min Read Through NASA’s Lens: Capturing Space Shuttle Endeavour’s Move to LA
Article 3 Min Read I Am Artemis: Allison Mjoen
Image Article 2 Min Read Shannon Lucid’s Record-Setting Mission Aboard Mir Image Article 2 Min Read NASA Unveils Enterprise, the First Space Shuttle
Featured Story

# Retired Space Shuttle Locations
Shuttle Atlantis – Kennedy Space Center Visitor Complex Shuttle Discovery – Steven F. Udvar-Hazy Center Shuttle Endeavour – California Science…
Read the Story
Keep Exploring

# Retired Space Shuttle Locations
## Discover More Topics From NASA
Overview of NASA’s Missions Humans In Space ### Humans to Mars Like the Moon, Mars is a rich destination for scientific discovery and a driver of technologies that will enable humans… Astronauts
</excerpt>
### Rank 5 of 84 — 0.41
<excerpt title="Sts-120 launch with pam melroy at kennedy space center">
# STS-120... - American Space Museum & Space Walk of Fame | Facebook
## American Space Museum & Space Walk of Fame's Post
[October 25 at 12:00 AM](https://www.facebook.com/SpaceWalkOfFame/posts/pfbid0ewumWtdjVuYV56fA92tyxTiAQPzbPBfYeAtaZ3LkKBFq2Bvu7xsfK37UvqzMpyugl?__cft__[0]=AZirmb5CsN3EUabRRaU1xfJsyiNVh6nrSu9S9QsgKUJeZ1jY4klXXLHjs0pFCB-wRfjdVtlVfqsu3j0L5oHy_7LS_n5n-VMOTnNRRDh0AJ5O2ImgbdxMz5KKylWcPaR5Y1-nB4w4uwPcUkE5gNeoATZtGqMvCFRX&__tn__=%2CO%2CP-R) ·
STS-120 LAUNCHED 19 YEARS AGO WITH PAM MELROY IN COMMAND
NASA astronaut Pam Melroy, became the second female commander of a spaceship when STS-120 and Discovery blasted off Kennedy Space Center on Oct. 23, 2007.
This 23rd Shuttle flight to the International Space Station was a hard-hat mission with spacewalks of two astronauts to install the Harmony module and repair torn solar panels. It was one of the longest Shuttle missions at more than 15 days.
Shuttle commander Melroy joined ISS commander Peggy Whiteson to become the first two female commanders of spacecraft in Earth orbit.
Pictured from the left are astronauts Scott E. Parazynski (fifth and last spaceflight); Douglas H. Wheelock (first of two spaceflights), Stephanie D. Wilson (second of three) , all mission specialists; George D. Zamka (first of two), pilot; Pamela A. Melroy, commander (third and last spaceflight) ; Daniel M. Tani (2nd and last), Expedition 15 flight engineer; and Paolo A. Nespoli (1st of 3), mission specialist representing the European Space Agency (ESA).

# STS-120... - American Space Museum & Space Walk of Fame | Facebook
## American Space Museum & Space Walk of Fame's Post
STS-120 carried the signatures of over 500,000 students that participated in the 2007 Student Signatures in Space program, jointly sponsored by NASA and Lockheed Martin. In celebration of Space Day in May 2007, students from over 500 schools around the world signed giant posters. Their signatures were scanned onto a disk, and the disk was manifested on the STS-120 mission.
Melroy was a deputy NASA administrator under the President Joe Biden administration, working with administrator Bill Nelson, space flier, and his deputy administrator, astronaut Bob Cabana.
[](https://www.facebook.com/photo/?fbid=1905885307049296&set=pcb.1905885447049282&__cft__[0]=AZirmb5CsN3EUabRRaU1xfJsyiNVh6nrSu9S9QsgKUJeZ1jY4klXXLHjs0pFCB-wRfjdVtlVfqsu3j0L5oHy_7LS_n5n-VMOTnNRRDh0AJ5O2ImgbdxMz5KKylWcPaR5Y1-nB4w4uwPcUkE5gNeoATZtGqMvCFRX&__tn__=*b0H-R)
</excerpt>

## Search 5 — query: "STS-120 crew birthdate Pamela Melroy birthdate"
### Rank 1 of 23 — 0.78 (passed on)
<excerpt title="Pamela Melroy">
From Wikipedia, the free encyclopedia
| Pamela Melroy |  
| --- |  
|  Official portrait, 2023 |  
|  |  
| 15th Deputy Administrator of the National Aeronautics and Space Administration |  
| **In office** June 21, 2021–January 20, 2025 |  
| President | Joe Biden |  
| Preceded by | James Morhard |  
| Succeeded by | Matthew P. Anderson |  
| Personal details |  
| Born | Pamela Ann Melroy September 17, 1961 (age 65) Palo Alto, California, U.S. |  
| Education | Wellesley College (BA) Massachusetts Institute of Technology (MS) |  
|  |  
| **Space career** |  
| NASA astronaut |  
| Rank | Colonel, USAF |  
| Time in space | 38d 20h 6m |  
| Selection | NASA Group 15 (1994) |  
| Mission | STS-92 STS-112 STS-120 |  
| Mission insignia |  |  
|  |
**Pamela Ann Melroy** (born September 17, 1961) is an American retired United States Air Force officer and NASAastronaut who also served as the deputy administrator of NASA. She served as pilot on Space Shuttle missions STS-92 and STS-112 and commanded mission STS-120 before leaving the agency in August 2009. After serving as deputy program manager of Space Exploration Initiatives with Lockheed Martin,[[1]](https://en.wikipedia.org/wiki/Pamela_Melroy#cite_note-1) Melroy joined the Federal Aviation Administration in 2011, where she was a senior technical advisor and director of field operations for the FAA's Office of Commercial Space Transportation.[[2]](https://en.wikipedia.org/wiki/Pamela_Melroy#cite_note-2)
In 2013, she left the FAA and joined DARPA as deputy director of the Tactical Technology Office. She left the agency in February 2017.

In November 2021, Melroy was inducted into the United States Astronaut Hall of Fame at the Kennedy Space Center Visitor Complex. The ceremony, originally planned for May 2020, was delayed due to the COVID-19 pandemic.[[3]](https://en.wikipedia.org/wiki/Pamela_Melroy#cite_note-3)[[4]](https://en.wikipedia.org/wiki/Pamela_Melroy#cite_note-4)
Melroy served as Deputy Administrator of NASA from 2021 to 2025[[5]](https://en.wikipedia.org/wiki/Pamela_Melroy#cite_note-5)[[6]](https://en.wikipedia.org/wiki/Pamela_Melroy#cite_note-6), helping design strategies like Moon to Mars (Artemis), NASA 2040, Low Earth Orbit (LEO) Commercialization and Space Sustainability[[7]](https://en.wikipedia.org/wiki/Pamela_Melroy#cite_note-7).
Today, she works as a strategic advisor and keynote speaker[[8]](https://en.wikipedia.org/wiki/Pamela_Melroy#cite_note-8).
</excerpt>
### Rank 2 of 23 — 0.77
<excerpt title="Biographical Data">
Title: PDF document  
URL Source: https://www.nasa.gov/wp-content/uploads/2025/05/melroy-pamela.pdf  
Markdown Content:

## [PDF page 1]
Biographical Data
Lyndon B. Johnson Space Center  
Houston, Texas  77058  National Aeronautics and  
Space Administration
PAMELA ANN MELROY (COLONEL, USAF, RET.)  
NASA ASTRONAUT (FORMER)
PERSONAL  DATA:  Born  September  17,  1961,  in  Palo  Alto,  California.  Married  to  
Douglas W. Hollett.  Considers Rochester, New York, to be her hometown.  Pam enjoys  
theatre, tap and jazz dancing, reading, cooking and flying.  Her parents, David and Helen  
Melroy, reside in upstate New York.
EDUCATION:  Graduated from Bishop Kearney High School, Rochester, New York, in  
1979.  Bachelor of Arts degree in Physics and Astronomy from Wellesley College, 1983.  
Master of Science degree in Earth and Planetary Sciences from Massachusetts Institute of  
Technology, 1984.
ORGANIZATIONS:  Member of the Wellesley College Board of Trustees; the Society of  
Experimental Test Pilots; the Association of Space Explorers and The Ninety-Nines, Inc.
SPECIAL HONORS:  Recipient of the Air Force Meritorious Service Medal, First Oak  
Leaf Cluster; Air Medal, First Oak Leaf Cluster; Aerial Achievement Medal, First Oak Leaf Cluster and Expeditionary Medal, First  
Oak Leaf Cluster.  Recipient of the NASA Distinguished Service Medal and the NASA Outstanding Leadership Medal.

## [PDF page 1]
EXPERIENCE:  Colonel Melroy was commissioned through the Air Force Reserve Officers’ Training Corps (ROTC) program in  
1983.  After completing a Master’s degree, she attended undergraduate pilot training at Reese Air Force Base in Lubbock, Texas,  
and graduated in 1985.  Melroy flew the KC-10 for six years at Barksdale Air Force Base in Bossier City, Louisiana, as a co-pilot,  
aircraft commander and instructor pilot.  Colonel Melroy is a veteran of Operation Just Cause and Operation Desert Shield/Desert  
Storm, with more than 200 combat and combat support hours.  In June 1991, she attended the Air Force Test Pilot School at Edwards  
Air Force Base, California.  Upon her graduation, she was assigned to the C-17 Combined Test Force, where she served as a test  
pilot until her selection for the Astronaut Program.  She has logged more than 6,000 hours flight time in more than 50 different  
aircraft.  Colonel Melroy retired from the Air Force in February 2007.
</excerpt>
### Rank 3 of 23 — 0.70
<excerpt title="Former Air Force Pilot Second Woman to Command Shuttle">
# Former Air Force Pilot Second Woman to Command Shuttle
### Story by Gerald Gilmore


# Former Air Force Pilot Second Woman to Command Shuttle
### War.gov
✔✗Subscribe
176
Retired Air Force Col. Pamela A. Melroy will become the second woman to command a NASA space shuttle flight when Discovery lifts off from Cape Canaveral, Fla., tomorrow.
The STS-120 flight is the 23rd shuttle mission to the International Space Station, according NASA’s Web site. The mission will launch an Italian-built U.S. multi-port module for the station. The “Harmony” device will provide attachment points for European and Japanese laboratory modules.
Melroy, 46, piloted KC-10 tanker planes and tested prototype C-17 transport aircraft in the Air Force. She retired from the military in February.
In a recent interview, Melroy said she’d always wanted to experience space travel. “That was my dream; even going into the Air Force, I knew I wanted to be an astronaut,” said Melroy, who was born in Palo Alto, Calif.
Melroy is leading a crew of six other astronauts, including two military officers, aboard Discovery. She is the second woman to command a shuttle flight. Air Force Col. Eileen M. Collins became the first woman to command a shuttle flight aboard the Columbia during mission STS-93 in July 1999. Collins commanded the Columbia again during shuttle mission STS-114 in July-August 2005. Collins retired from NASA in May 2006.
Other STS-120 crew members are:
-- Marine Col. George D. Zamka, 45, born in Jersey City, N.J.;
-- Scott E. Parazynski, 46, born in Little Rock, Ark.;
-- Army Col. Douglas H. Wheelock, 47, born in Binghamton, N.Y.;
-- Stephanie D. Wilson, 41, born in Boston;
-- Paolo A. Nespoli, 50, a European Space Agency astronaut who was born in Milan, Italy; and
-- Daniel M. Tani, 46, born in Ridley Park, Pa.

# Former Air Force Pilot Second Woman to Command Shuttle
### War.gov
Another astronaut, Clayton C. Anderson, 48, will return to earth from the space station aboard shuttle mission STS-120. Tani will replace Anderson aboard the space station. Tani will return to earth on shuttle mission STS-122.
Discovery’s STS-120 mission is slated to return to the John F. Kennedy Space Center’s shuttle landing site in Florida on Nov. 6.
Story by Gerry J. Gilmore, American Forces Press Service

# Former Air Force Pilot Second Woman to Command Shuttle
## NEWS INFO
Date Taken:10.21.2007  
Date Posted:07.03.2025 21:52  
Story ID:524242  
Location:WASHINGTON, US
* * *
Web Views:86  
Downloads:0
* * *

# Former Air Force Pilot Second Woman to Command Shuttle
## NEWS INFO
#### PUBLIC DOMAIN
This work, Former Air Force Pilot Second Woman to Command Shuttle, by Gerald Gilmore, identified by DVIDS, must comply with the restrictions shown on https://www.dvidshub.net/about/copyright.

# Former Air Force Pilot Second Woman to Command Shuttle
## CONNECTED MEDIA


# Former Air Force Pilot Second Woman to Command Shuttle
## MORE LIKE THIS


# Former Air Force Pilot Second Woman to Command Shuttle
## CONTROLLED VOCABULARY KEYWORDS
_No keywords found._
Add Keyword

# Former Air Force Pilot Second Woman to Command Shuttle
## TAGS
American Forces Press Service
Defense.gov DefenseLink Archive

# Former Air Force Pilot Second Woman to Command Shuttle
## OPTIONS
*   Register/Login to Download  
*   Validate Your Account to Download  
*   Connect My Placements  
*   Download Story  
*   Add to My Albums  
*   [Create TinyURL](javascript:document.submitTiny.submit())  
*   Connect to Placements  
*   Add to Playlist  
*   Distribute Story  
*   Edit Story  
*   Add News & Images to Playlist  
*   Printable Version  
*   Request Audio Version
</excerpt>
### Rank 4 of 23 — 0.65
<excerpt title="Col. Pamela A. Melroy">
Foil: 17 Panel: 2 Column: 2 Line: 42
**Wall of Honor Level:**
Air and Space Friend
**Honored by:**
PERSONAL DATA: Born September 17, 1961, in Palo Alto, California. Considers Rochester, New York, to be her hometown. Married to Christopher Wallace. She enjoys theatre, tap and jazz dancing, reading, cooking, and flying. Her parents, David and Helen Melroy, reside in upstate New York.
EDUCATION: Graduated from Bishop Kearney High School, Rochester, New York, in 1979. Bachelor of science degree in physics and astronomy from Wellesley College, 1983. Master of science degree in earth & planetary sciences from Massachusetts Institute of Technology, 1984.
ORGANIZATIONS: Member of the Society of Experimental Test Pilots, the Order of Daedalians, and the 99s.
SPECIAL HONORS: Recipient of the Air Force Meritorious Service Medal, First Oak Leaf Cluster; Air Medal, First Oak Leaf Cluster; Aerial Achievement Medal, First Oak Leaf Cluster; and Expeditionary Medal, First Oak Leaf Cluster
EXPERIENCE: Melroy was commissioned through the Air Force ROTC program in 1983. After completing a masters degree, she attended Undergraduate Pilot Training at Reese Air Force Base in Lubbock, Texas and was graduated in 1985. She flew the KC-10 for six'years at Barksdale Air Force Base in Bossier City, Louisiana, as a copilot, aircraft commander and instructor pilot. Melroy is a veteran of JUST CAUSE and DESERT SHIELD/DESERT STORM, with over 200 combat and combat support hours. In June 1991, she attended the Air Force Test Pilot School at Edwards Air Force Base, California. Upon her graduation, she was assigned to the C-17 Combined Test Force, where she served as a test pilot until her selection for the astronaut program. She has logged over 5,000 hours flight time in over 45 different aircraft.

NASA EXPERIENCE: Selected as an astronaut candidate by NASA in December 1994, Melroy reported to the Johnson Space Center in March 1995. She completed a year of training and evaluation and is qualified for flight assignment as a shuttle pilot. Initially assigned to astronaut support duties for Iaunch and Ianding, she has also worked Advanced Projects for the Astronaut Office. Melroy served as pilot on two flights (STS-92 in 2000 and STS-112 in 2002), and has logged over 562 hours in space.
SPACE FLIGHT EXPERIENCE: STS-92 Discovery (October 11-24, 2000) was launched from the Kennedy Space Center, Florida and returned to land at Edwards Air Force Base, California. During the 13-day flight, the seven member crew attached the Z1 Truss and Pressurized Mating Adapter 3 to the International Space Station using Discovery's robotic arm and performed four space walks to configure these elements. This expansion of the ISS opened the door for future assembly missions and prepared the station for its first resident crew. The STS-92 mission was accomplished in 202 orbits, traveling 5.3 million miles in 12 days, 21 hours, 40 minutes and 25 seconds.
STS-112 Atlantis (October 7-18, 2002) launched from and returned to land at the Kennedy Space Center, Florida. STS-112 was an International Space Station assembly mission during which the crew conducted joint operations with the Expedition-5 by delivering and installing the S-One Truss (the third piece of the station's 11-piece Integrated Truss Structure). It took three spacewalks to outfit and activate the new component. The crew also transferred cargo between the two vehicles and used the shuttle's thruster jets during two maneuvers to raise the station's orbit. STS-112 was the first shuttle mission to use a camera on the External Tank, providing a live view of the launch to flight controllers and NASA TV viewers. The mission was accomplished in 170 orbits, traveling 4.5 million miles in 10 days, 19 hours, and 58 minutes.

_Wall of Honor profiles are provided by the honoree or the donor who added their name to the Wall of Honor. The Museum cannot validate all facts contained in the profiles._
</excerpt>
### Rank 5 of 23 — 0.64
<excerpt title="Pamela Melroy">
## Early life and education
[edit]
Melroy was born in Palo Alto, California, and graduated from Bishop Kearney High School in Rochester, New York in 1979.[[9]](https://en.wikipedia.org/wiki/Pamela_Melroy#cite_note-9) She received a Bachelor of Arts in physics and astronomy from Wellesley College in 1983.[[10]](https://en.wikipedia.org/wiki/Pamela_Melroy#cite_note-Wellesley-10) She then earned her Master of Science in Earth and planetary science from the Massachusetts Institute of Technology in 1984. On May 18, 2008, Melroy received an honorary degree from Iona College in New Rochelle, New York.
Melroy was commissioned through Air Force ROTC, Detachment 365, in 1984. After completing a master's degree, she attended Undergraduate Pilot Training at Reese Air Force Base in Lubbock, Texas and was graduated in 1985. She flew the KC-10 for six years at Barksdale Air Force Base in Bossier City, Louisiana, as a copilot, aircraft commander and instructor pilot. Melroy is a veteran of the United States invasion of Panama and Operation Desert Shield/Desert Storm, with over 200 combat and combat support hours. In June 1991, she attended the Air Force Test Pilot School at Edwards Air Force Base, California. Upon her graduation, she was assigned to the C-17 Combined Test Force, where she served as a test pilot until her selection for the astronaut program. She has logged over 5,000 hours of flight time in over 50 different aircraft. Melroy retired from the Air Force in February 2007.
Melroy aboard the ISS during STS-112

## Early life and education
Selected as an astronaut candidate by NASA in December 1994, Melroy reported to the Johnson Space Center in March 1995. She completed a year of training and evaluation and was qualified for flight assignment as a shuttle pilot. Initially assigned to astronaut support duties for launch and landing, she also worked Advanced Projects for the Astronaut Office. She also performed CAPCOM duties in mission control. Melroy served on the _Columbia_ Reconstruction Team as the lead for the crew module and served as deputy project manager for the _Columbia_ crew survival investigation team. In her final position, she served as branch chief for the Orion branch of the Astronaut Office.
Melroy served as pilot on two flights (STS-92 in 2000 and STS-112 in 2002), and was the mission commander on STS-120 in 2007, making her the second woman to command a Space Shuttle mission (after Eileen Collins).[[11]](https://en.wikipedia.org/wiki/Pamela_Melroy#cite_note-11) The STS-120 crew visited the station during Expedition 16, commanded by Peggy Whitson. Whitson was the first female ISS commander, making the STS-120 mission the first time that two female mission commanders were in orbit at the same time.[[12]](https://en.wikipedia.org/wiki/Pamela_Melroy#cite_note-bionasa-12)[[13]](https://en.wikipedia.org/wiki/Pamela_Melroy#cite_note-13)
She has logged more than 924 hours (over 38 days) in space.[[12]](https://en.wikipedia.org/wiki/Pamela_Melroy#cite_note-bionasa-12)
</excerpt>

## Search 6 — query: ""Frame Toby" The Office original air date"
### Rank 1 of 96 — 0.89 (passed on)
<excerpt title="The Office season 5 Frame Toby Reviews">
# The Office season 5 Frame Toby Reviews - Metacritic
Explore TV   
    *   November TV Preview  
    *   Renew/Cancel Scorecard  
    *   Apple TV: New & Upcoming  
    *   Disney+: New & Upcoming  
    *   HBO Max: New & Upcoming  
    *   Hulu: New & Upcoming  
    *   Netflix: New & Upcoming  
    *   Paramount+: New & Upcoming  
    *   Peacock: New & Upcoming  
    *   Prime Video: New & Upcoming  
    *   See All
New TV Shows
*   → TV Premiere Calendar  
    *   Cunk on Cinema  
    *   12 12 12  
    *   The Good Daughter  
    *   The Body  
    *   LOTR: The Rings of Power S3  
    *   It Gets Worse  
    *   Black Doves S2  
    *   North of North S2  
    *   All's Fair S2  
    *   See All New Shows
*   Music
New Albums   
    *   U2: Carnaval De Luz  
    *   Kings of Leon: O My Beloved  
    *   DIIV: ZIRP!  
    *   Queens of the Stone Age: Perfecth  
    *   The Avalanches: No Bad Memories  
    *   Eels: Cookie Happened  
    *   Fontaines DC: Dopamine Chamber  
    *   Richard Thompson: Hippies, Thugs & Heroes  
    *   Troye Sivan: She's the Best  
    *   Teenage Fanclub: Do Not Dare to Dream  
    *   All recent album releases ...
*   News
Register
*   TV-PG  
*   NBC  
*   Nov 20, 2008  
*   22 m
Summary Based on the popular British series of the same name, this faster-paced American version follows the daily interactions of a group of idiosyncratic office employees at paper company Dunder Mifflin's Scranton branch via a documentary film crew's cameras. Regional manager Michael (Steve Carell) thinks he's the coolest, funniest, best boss ever -... Read More
*   Comedy
Directed By:Jason Reitman
Written By:Greg Daniels, Mindy Kaling, Ricky Gervais, Stephen Merchant, Anthony Q. Farrell
❮ The Office

# The Office season 5 Frame Toby Reviews - Metacritic
S5 • Episode 8
Frame Toby
Air Date:
Nov 20, 2008
User score
Available after 4 ratings
tbd
My Score
Drag or tap to give a rating
Hover and click to give a rating
tbd
Add My Review

# The Office season 5 Frame Toby Reviews - Metacritic
## Where to Watch
Peacock Premium(Subscription required)All Watch Options
JustWatch
Not available in your country?
ExpressVPN Get 3 Extra months free $6.67/mth
</excerpt>
### Rank 2 of 96 — 0.87
<excerpt title="Frame Toby - The Office (Season 5, Episode 9)">
# ‎Frame Toby - The Office (Season 5, Episode 9) - Apple TV
Search
Sign In
Frame Toby
The Office

# Frame Toby
Comedy
**S5, E9:** An office mess -- A mysterious person in the office has made a huge mess in the microwave and will not clean it up. Meanwhile, Michael (Golden Globe winner Steve Carell) has to come to terms with the fact that there have been certain personnel changes in his staff without his knowing. Rainn Wilson, John Krasinski, Jenna Fischer, B.J. Novak, Ed Helms, Leslie David Baker, Brian Baumgartner, Kate Flannery, Mindy Kaling, Angela Kinsey, Phyllis Smith, Oscar Nunez, Paul Lieberstein and Creed Bratton also star.
Nov 20, 2008 · 19m
StarringAndy Buckley, Lee Eisenberg, Patrick Faucette
DirectorJason Reitman
*    All of Apple TV and Peacock. One subscription. Bundle and Save Plans start at $17.99/month   Explore

# Frame Toby
## Cast & Crew
*    Jason Reitman Director    
*    Andy Buckley David Wallace    
*    Lee Eisenberg Gino    
*    Patrick Faucette Policeman 1    
*    Michael "Mick" Harrity Policeman 2    
*    Gene Stupnitsky Leo

# Frame Toby
## Cast & Crew
### Information
Released 2008 Run Time 19 min Rated TV-14 Content Advisories Suggestive Dialogue, Language Region of Origin United States© 2005-2009 NBC Studios, Inc. and Universal Network Television LLC. All Rights Reserved.

# Frame Toby
## Cast & Crew
### Languages
Original Audio English, English (United Kingdom)Audio
English (United States) (AAC)
Subtitles
English (United States) (CC)

# Frame Toby
## Cast & Crew
### Accessibility
Closed captions (CC) refer to subtitles in the available language with the addition of relevant non-dialogue information.
United States
*   Español (México)
Select a country or region
</excerpt>
### Rank 3 of 96 — 0.83
<excerpt title="The Office – “Frame Toby”">
### “Frame Toby”
_**November 20th, 2008**_
Michael Scott is not a heartless man – he may hate Toby with every fibre of his being, and he may act as if his return is in fact a 911 emergency, but this does not mean that Michael is a terrible person. Under the circumstances, it makes perfect sense that Toby (Paul Lieberstein) returning would make Michael upset: he didn’t know he was there for a week because he refuses to go into the annex because “that’s where Holly worked,” and his most hated person replacing the person he loved would be highly problematic for anyone, yet alone someone as devoid of stability as Michael.
What works about “Frame Toby” (Michael’s initial reaction to his return, Dwight’s contribution to the eponymous effort, the conclusion of that particular story arc) works fine, but it felt like there was a bigger story here. The last time Michael was this adversarial with a co-worked was in “Goodbye, Stanley,” an episode where Michael finally came to his senses at episode’s end and he and Stanley actually talked out their differences. One of those scenes here could have gone a long way to formalizing Michael’s Holly issues, but the episode never goes there; instead, it spends a bit too much time on Pam’s non-triumphant return to the office, and never quite feels like a cohesive episode or something that adds to the existing mythology of this epic feud.
I don’t quite know what was going on with Pam in this episode in regards to the dirty microwave. It didn’t really serve as a metaphor for anything, considering that we never got a scene where Pam got to question whether perhaps her ungrateful and slobbish office mates are inferior to her artistic friends in New York, and it didn’t really do anything but put her in a bad mood to heighten the shift in emotions in terms of the final scene at Jim and Pam’s new house. Jenna Fischer’s return to the office felt like a chance to either give us some of that classic Jim/Pam office banter (mostly absent in the episode), and yet they instead turned Pam into a fairly bitter and unpleasant individual (even if I agree with her point, it didn’t do her character any favours entertainment wise). Perhaps I was missing something, but there just wasn’t anything here that made me think it was a smart use of time in the episode.

### “Frame Toby”
Yes, Jim and Pam’s conclusion was charming, but I don’t know if it’s quite as positive as they make it out to be. As Zap2it.com’s Daniel Fienbergpointed out on Twitter, this is now three storylines in a week (“Friday Night Lights” and “Brothers & Sisters” did it as well) about one partner buying or thinking about buying a house as a “surprise” for the other, and it’s just a hideously bad idea. While part of Pam is touched by the gesture, I would tend to think that one night sleeping in the second bedroom (what with his parents’ room boarded up) and waking up to the house Jim went heavily into debt for in order to help out his Mother won’t go over too well. That garage would make an awful studio in terms of its lighting situation, and I think that beyond Jim’s charming presentation the charm will, in fact, wear off. While I’m fine with these two playing out a slow born storyline, it’s weird to pair this side of it with, of all things, the microwave. Even if the end result is a real dramatic moment in their relationship, this part could have been balanced better.
The other side of the episode was stronger because it flowed more like we expect The Office to flow. Michael’s desperation to be rid of Toby was played for some good laughs, whether it was buying the fake weed or his sweat-covered attempt to talk to Toby while pretending to be his friend, but as noted above it felt like Michael’s reaction could have been more dramatically powerful. Considering how much Holly is tied up in this storyline, I don’t think that Michael’s guilt over Toby’s police search was enough. I liked that Michael was incredulous about Toby not being more mad (more angry that taxpayer dollars and safety were threatened than be the fact that Michael would attempt to frame him for felony possession with intent to traffic), but it felt like the next logical step was for Michael to discuss his recent loss before humorously reverting back to hatred just to establish some sense of normalcy. It wasn’t a poorly executed storyline, it was just one that didn’t click as I wanted it to.
</excerpt>
### Rank 4 of 96 — 0.76
<excerpt title="The Office season 5 Frame Toby Reviews">
# The Office season 5 Frame Toby Reviews - Metacritic
## Where to Watch
Peacock Premium(Subscription required)All Watch Options
JustWatch
Not available in your country?
ExpressVPN Get 3 Extra months free $6.67/mth

# The Office season 5 Frame Toby Reviews - Metacritic
## Season Episodes
View All Seasons
Episode 1 • Sep 25, 2008 • 43 m Weight Loss Michael tries to motivate the Scranton branch to lose weight as part of an interoffice competition. Jim is lost after Pam leaves for art school in New York, and Angela continues to see Dwight even though she is now engaged to Andy.
Episode 2 • Oct 9, 2008 • 22 m Business Ethics A confession at an H.R. business ethics seminar leads to a dispute between Michael and Holly over whether Meredith should be fired. Dwight tries to prove to Jim how long he can go without taking a personal break.
Episode 3 • Oct 16, 2008 • 22 m Baby Shower After planning an office baby shower for Jan, Michael is upset when he finds out that she had the baby without him--even though he's already been told that he's not the baby's father.
Episode 4 • Oct 23, 2008 • 22 m Crime Aid Michael and Holly have sex for the first time, and Michael holds a fundraiser for the office after it is burglarized. Dwight confides in Phyllis after Andy and Angela set a wedding date, and Jim runs into Pam's ex-fiancé, Roy.
Episode 5 • Oct 30, 2008 • 22 m Employee Transfer Holly is transferred back to New Hampshire after corporate discovers that she and Michael are dating. Dwight tries to apply to Cornell to get under Andy's skin. Jim's brothers and Pam decide to play a trick on Jim when they meet for lunch.
Episode 6 • Nov 6, 2008 • 22 m Customer Survey Dwight and Jim believe that something is suspicious about their low customer performance ratings. After consulting with Angela, Andy finds the perfect site for their wedding--Dwight's beet farm.
Episode 7 • Nov 13, 2008 • 22 m Business Trip David Wallace sends Michael on a business trip to Winnipeg to help him forget about Holly's transfer to Nashua, and Pam tells Jim that she failed a class and has to stay in New York City.
Episode 8 • Nov 20, 2008 • 22 m Frame Toby
</excerpt>
### Rank 5 of 96 — 0.76
<excerpt title="The Office season 5 Frame Toby Reviews">
# The Office season 5 Frame Toby Reviews - Metacritic
## Season Episodes
View All Seasons
Episode 1 • Sep 25, 2008 • 43 m Weight Loss Michael tries to motivate the Scranton branch to lose weight as part of an interoffice competition. Jim is lost after Pam leaves for art school in New York, and Angela continues to see Dwight even though she is now engaged to Andy.
Episode 2 • Oct 9, 2008 • 22 m Business Ethics A confession at an H.R. business ethics seminar leads to a dispute between Michael and Holly over whether Meredith should be fired. Dwight tries to prove to Jim how long he can go without taking a personal break.
Episode 3 • Oct 16, 2008 • 22 m Baby Shower After planning an office baby shower for Jan, Michael is upset when he finds out that she had the baby without him--even though he's already been told that he's not the baby's father.
Episode 4 • Oct 23, 2008 • 22 m Crime Aid Michael and Holly have sex for the first time, and Michael holds a fundraiser for the office after it is burglarized. Dwight confides in Phyllis after Andy and Angela set a wedding date, and Jim runs into Pam's ex-fiancé, Roy.
Episode 5 • Oct 30, 2008 • 22 m Employee Transfer Holly is transferred back to New Hampshire after corporate discovers that she and Michael are dating. Dwight tries to apply to Cornell to get under Andy's skin. Jim's brothers and Pam decide to play a trick on Jim when they meet for lunch.
Episode 6 • Nov 6, 2008 • 22 m Customer Survey Dwight and Jim believe that something is suspicious about their low customer performance ratings. After consulting with Angela, Andy finds the perfect site for their wedding--Dwight's beet farm.
Episode 7 • Nov 13, 2008 • 22 m Business Trip David Wallace sends Michael on a business trip to Winnipeg to help him forget about Holly's transfer to Nashua, and Pam tells Jim that she failed a class and has to stay in New York City.
Episode 8 • Nov 20, 2008 • 22 m Frame Toby
</excerpt>

## Search 7 — query: ""Clay Anderson" STS-120"
### Rank 1 of 84 — 0.73 (passed on)
<excerpt title="STS-120">
# STS-120 - NASA
## Suggested Searches
### Highlights
11 min read ### La NASA anuncia la cobertura de la misión lunar Artemis II article 8 months ago 15 min read ### Agenda diaria de la misión a la Luna de Artemis II de la NASA article 8 months ago 6 min read ### La NASA refuerza Artemis: añade una misión y perfecciona su arquitectura general article 9 months ago

# STS-120
Occurred 22 years ago
STS-120 was the 23rd shuttle mission to the International Space Station, and launched an Italian-built U.S. multi-port module for the station.
Orbiter
Discovery
mission duration
15 days, 2 hours, 23 minutes
Launch
Oct. 23, 2007
Landing
Nov. 7, 2007
These seven astronauts took a break from training to pose for the STS-120 crew portrait. Pictured from the left are astronauts Scott E. Parazynski, Douglas H. Wheelock, Stephanie D. Wilson, all mission specialists; George D. Zamka, pilot; Pamela A. Melroy, commander; Daniel M. Tani, Expedition 16 flight engineer; and Paolo A. Nespoli, mission specialist representing the European Space Agency (ESA). The crew members were attired in training versions of their shuttle launch and entry suits. Tani joined Expedition 16 as flight engineer after launching to the International Space Station (ISS) and is scheduled to return home on mission STS-122. STS-120 launched October 23, 2007 with the main objectives of installing the U.S. Node 2, Harmony, and the relocation and deployment of the P6 truss to its permanent location.
NASA

# STS-120
## Mission Facts
**Orbiter:** Discovery
**Mission:**Space Station Assembly Mission 10A
**Primary Payload:** Harmony Node 2
**Launch Date:** Oct. 23, 2007
**Launch Time:** 11:38 a.m. EDT
**Launch Pad:** 39A
**Landing Date:** Nov. 7, 2007
**Landing Time:** 1:01 p.m. EST
**Landing Site:** Kennedy Space Center
**Inclination/Altitude:** 51.6 degrees/122 nautical miles

# STS-120
## Mission Facts
### Crew:
Pam Melroy, Commander
George Zamka, Pilot
Scott Parazynski, Mission Specialist
Doug Wheelock, Mission Specialist
Stephanie Wilson, Mission Specialist
Paolo Nespoli, Mission Specialist
Daniel Tani, Flight Engineer, Embarking to International Space Station
Clay Anderson, Flight Engineer, Returning from International Space Station
</excerpt>
### Rank 2 of 84 — 0.63
<excerpt title="Clayton Anderson">
# Clayton Anderson
- [x] 29 languages
*   العربية  
*   مصرى  
*   Български  
*   বাংলা  
*   Català  
*   Čeština  
*   Dansk  
*   Deutsch  
*   Español  
*   Eesti  
*   فارسی  
*   Suomi  
*   Français  
*   Galego  
*   Magyar  
*   Bahasa Indonesia  
*   Italiano  
*   日本語  
*   Latviešu  
*   Malagasy  
*   Bahasa Melayu  
*   Nederlands  
*   Polski  
*   Português  
*   Русский  
*   Slovenčina  
*   Svenska  
*   Türkçe  
*   Українська
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
Print/export
*   Download as PDF  
*   [Printable version](javascript:print(); "Printable version of this page [p]")
In other projects
*   Wikimedia Commons  
*   Wikidata item
Appearance
move to sidebar hide
From Wikipedia, the free encyclopedia
American astronaut (born 1959)

# Clayton Anderson
| Clayton Anderson |  
| --- |  
|  Anderson in 2009 |  
| Born | Clayton Conrad Anderson (1959-02-23) February 23, 1959 (age 67) Omaha, Nebraska, U.S. |  
| Education | Hastings College (BS) Iowa State University (MS) |  
| **Space career** |  
| NASA astronaut |  
| Time in space | 166d 21h 10m |  
| Selection | NASA Group 17 (1998) |  
| TotalEVAs | 6 |  
| Total EVA time | 38h 28m |  
| Missions | Expedition 15/16 (STS-117/STS-120) STS-131 |  
| Mission insignia |  |  
|  |
**Clayton Conrad Anderson** (born February 23, 1959) is a retired NASAastronaut. Launched on STS-117, he replaced Sunita Williams on June 10, 2007 as a member of the ISS Expedition 15 crew.[[1]](https://en.wikipedia.org/wiki/Clayton_Anderson#cite_note-nasa-07-142-1) He is currently an author, a motivational speaker, and a Professor of Practice at Iowa State University in Ames, Iowa. In 2022, he became the president and CEO of the Strategic Air Command & Aerospace Museum.

# Clayton Anderson
## Early life and education
[edit]
Anderson graduated from Ashland-Greenwood High School, Ashland, Nebraska, 1977, received a Bachelor of Science degree (cum laude) in physics at Hastings College, Nebraska, in 1981 and a Master of Science degree in aerospace engineering at Iowa State University in 1983.[[2]](https://en.wikipedia.org/wiki/Clayton_Anderson#cite_note-clay_bio-2)

# Clayton Anderson
## NASA career
[edit]
</excerpt>
### Rank 3 of 84 — 0.57
<excerpt title="Clayton “Astro Clay” Anderson">
### Astronaut, Speaker, and Author
– United States Astronaut, Retired
– STS-117/120, STS-131; ISS Expedition 15/16;NEEMO 5
– 167 days in space and 38 hours and 28 minutes over 6 spacewalks
– STEM Ambassador, Social Media Advocate, NASA Supporter
– Motivational Speaking Topics Include:
*   The Dream of a Lifetime  
*   Never a Commander, Always a Leader  
*   If at First You Don’t Succeed…  
*   Turn Pages into Dreams  
*   You’re Just Like Me!  
*   For the Beauty of the Earth
For more information on booking “Astro Clay” for speaking engagements or events pleasecontact us here
Official Website
Twitter: @Astro_Clay
Official Facebook
Youtube

### Biography
Astronaut Clayton “Astro Clay” Anderson, Nebraska’s only Astronaut, spent 167 days in space and 38 hours and 28 minutes in executing 6 spacewalks. He applied 15 times before NASA selected him as an Astronaut in 1998; and he spent 30 years working for NASA, 15 as an engineer and then 15 as an Astronaut.
Succeeding in one of the most difficult and coveted jobs in the world through perseverance and a never-give-up mantra, Anderson employs NASA’s “Plan, Train and Fly (Execute)” philosophy to all his speaking engagements and projects. Coupled with lessons learned in the areas of leadership, persistence, and passion, he provides unique and “out of this world” insights for those seeking to achieve practical execution.
Clay’s AWARD WINNING book, The Ordinary Spaceman: From Boyhood Dreams to Astronaut, children’s books A is for Astronaut: Blasting Through the Alphabet and It’s a Question of Space: An Ordinary Astronaut’s Answers to Sometimes Extraordinary Questions and a special “Astronaut Edition” Fisher Space Pen are available at www.AstroClay.com.

### STEAM / Education
The moniker of STEM… Science, Technology, Engineering, and Math appears throughout the world intending to raise awareness with respect to the need for young people to pursue these fields of study. Adding the A for arts, brings everything full circle, yielding a big picture view that captures the essence of what Astronaut Anderson believes are key educational and professional pursuits. After all, painting is — in its simplest form — chemistry. Playing a musical instrument — whether it be a guitar or trombone — conforms to basic laws of physics. And what better way to help induce a more socially empathetic and aware society, than by invoking STEAM to produce a cadre of well-rounded scholars?
STEAM also serves as a solid foundational lexicon. In all educational disciplines –when one tries to “talk” or “learn” in a specific language– having a basic grasp of relevant vocabulary is critical for all youth. More so, with those who have a passion to follow a career or educational path in a STEAM-related field (or maybe even one day become an Astronaut!), one simple word –introduced at an early age– can open a whole new universe in a young mind. In writing A is for Astronaut: Blasting Through the Alphabet, Anderson seeks to emphasize the importance of this exposure, i.e., a simple awareness of, or introduction to, certain words that will one day lead to more in-depth knowledge and understanding of its meaning and the discipline(s) that surround it. Promoting STEAM education is a key component to enable students and adults alike, to compete worldwide in all education and employment venues. Astronaut Anderson’s presentations are intended to do just that… using his life’s lessons of perseverance and his passion to succeed, to inspire and suggest how the benefits of a STEAM-focused approach can be a critical asset in pursuing one’s dreams while creating a more well-rounded citizenry.
</excerpt>
### Rank 4 of 84 — 0.57
<excerpt title="Meeting Nebraska astronaut Clay Anderson">
# Space Hipsters | My mom and I had the pleasure of meeting Nebraska's only astronaut today | Facebook
Log In
Log In
Forgot Account?
[](https://www.facebook.com/groups/176051159106442/?__cft__[0]=AZicjvQZzTvJH299SqmpN1yYsfIfeuGgV8ng9aPpiKcQNfR4QS56iOwOPgi2ia8dAHMMNiXfFNNeKHpwGqhfrTNEs4388KbR5Esg8DOTe1bi6P44UjsfVLhvltWCOFRp2FByljefe0nJhGSaWDM1jwX1iVLO-bT8u_YFq9a9LEVy97mSlWzB9F5RO9J4&__tn__=%3C%3C%2CP-R)
## [Space Hipsters](https://www.facebook.com/groups/176051159106442/?__cft__[0]=AZicjvQZzTvJH299SqmpN1yYsfIfeuGgV8ng9aPpiKcQNfR4QS56iOwOPgi2ia8dAHMMNiXfFNNeKHpwGqhfrTNEs4388KbR5Esg8DOTe1bi6P44UjsfVLhvltWCOFRp2FByljefe0nJhGSaWDM1jwX1iVLO-bT8u_YFq9a9LEVy97mSlWzB9F5RO9J4&__tn__=-UC%2CP-R) ·
Join
Jessica Hilt
·
Saturday, October 14, 2023 at 6:28 PM

# Space Hipsters | My mom and I had the pleasure of meeting Nebraska's only astronaut today | Facebook
[October 14, 2023](https://www.facebook.com/groups/176051159106442/?multi_permalinks=6982233558488134&hoisted_section_header_type=recently_seen&__cft__[0]=AZicjvQZzTvJH299SqmpN1yYsfIfeuGgV8ng9aPpiKcQNfR4QS56iOwOPgi2ia8dAHMMNiXfFNNeKHpwGqhfrTNEs4388KbR5Esg8DOTe1bi6P44UjsfVLhvltWCOFRp2FByljefe0nJhGSaWDM1jwX1iVLO-bT8u_YFq9a9LEVy97mSlWzB9F5RO9J4&__tn__=%2CO%2CP-R) ·
My mom and I had the pleasure of meeting Nebraska's only astronaut today! Clay Anderson was a member of STS-117, Expedition 15/16, STS-120, and STS-131. I believe all were carrying items to outfit/replace other items on the ISS. He's written several childrens books and at least one autobiography. He read one of his books to the kids and then signed books and took pictures. He recently moved back to Nebraska to head the Strategic Air and Space Museum near Ashland, NE.
</excerpt>
### Rank 5 of 84 — 0.56
<excerpt title="Astronaut Clay Anderson to Speak at Museum of Flight June 19">
# Astronaut Clay Anderson to Speak at Museum of Flight June 19
_NASA astronaut speaks about his five-month experience on the International Space Station_
SEATTLE, June 17, 2009
--NASA Astronaut Clayton C. Anderson, who lived for 152 days aboard the International Space Station in 2007 as a member of the Expedition 15 and 16 Crews, will speak at the Museum of Flight on Friday, June 19 at 2 p.m. His presentation is entitled "Life on the Space Station." While on orbit at the Space Station, he performed numerous scientific and engineering experiments, conducted three spacewalks and used the Robotic Manipulator System--commonly called Canadarm2--developed by the Canadian Space Agency to prepare the Station for the arrival of the U.S. built "Harmony" node. Anderson is currently assigned to the Space Shuttle crew of STS-131, scheduled to launch in March, 2010. He will present in the William M. Allen Theater and will be available for autographs and questions following the program.

# Astronaut Clay Anderson to Speak at Museum of Flight June 19
Anderson was born and raised in Nebraska, which he considers his home state. He graduated from Ashland-Greenwood High School, Ashland, Nebraska, in 1977; received a bachelor of science degree cum laude in Physics from Hastings College, Nebraska in 1981 and a master of science degree in Aerospace Engineering from Iowa State University in 1983. He launched to the ISS on June 8, 2007 aboard Space Shuttle Atlantis--STS-117--as the Expedition 15 Flight Engineer and the Science Officer and returned to Earth aboard Space Shuttle Discovery as a member of the STS-120 crew, landing at Kennedy Space Center on November 7, 2007. Expedition 15 and 16 included a number of science and engineering experiments from Russia, Europe, Canada and the United States. These included medical and physical sciences research, as well as observations of the Earth. Orbiting the earth at more than 220 miles, the ISS offers an ideal vantage point for crew members to continue observational efforts that began in the early 1960's. During Expeditions 15 through 18, activities included collaboration with the International Polar Year activities. Phenomena studied included auroras and mesospheric clouds. Astronaut photography of the earth can be found at: http://eol.jsc.nasa.gov/ipy
Anderson joined the NASA Johnson Space Center in 1983 in the Mission Operations Directorate Mission Planning and Analysis Division where he performed rendezvous and proximity operations trajectory designs for early space shuttle and ISS missions. In 1988 he became the Flight Design Manager leading the trajectory design team for the Galileo planetary mission--STS-34--while serving as the backup for the Magellan planetary mission--STS-31. In 1993 he was named the Chief of the Flight Design Branch. From 1996 until his selection as an astronaut in 1998, Anderson held the post of Manager, Emergency Operations Center, NASA Johnson Space Center.
Date:
Friday, June 19, 2009

# Astronaut Clay Anderson to Speak at Museum of Flight June 19
*   About the Museum  
*   Mission  
*   History  
*   Press (Current page)  
*   Careers  
*   Volunteers  
*   Vision 2050  
*   Trustees & Leadership  
*   Annual Reports  
*   Aloft Magazine  
*   Diversity & Inclusion  
*   Friendship Museums  
*   Privacy & Terms  
*   Admission Pass Donations  
*   Blog  
*   Podcast  
*   Contact Us  
*   eNews Signup
</excerpt>

## Search 8 — query: "Scott Parazynski birthdate July 5 1963"
### Rank 1 of 86 — 0.35 (passed on)
<excerpt title="Scott Parazynski">
_NASA Astronaut_
**Personal data**
Born 28 July 1961, in Little Rock, Arkansas USA. Married to the former Gail Marie Vozzella. They have two children. He enjoys rock climbing, mountaineering, flying, scuba, skiing, travel, woodwork and nature photography. A commercial, multi-engine, seaplane and instrument-rated pilot.
**Education**
He received a Bachelor of Science degree in biology from _Stanford University_ in 1983, continuing on to graduate with honours from _Stanford Medical School_ in 1989.
**Special honours**
Various US medical awards and achievements and various NASA awards including four Space Flight Medals, two Exceptional Service Medals and a Distinguished Service Medal.
**Experience**
Parazynski studied antigenic variation in African sleeping sickness. He conducted research at the NASA Ames Research Center on fluid shifts during human space flight and has been involved in the design of exercise devices being developed for long-duration space flight. He has also conducted research on high-altitude acclimatisation and has numerous publications to his name.
**NASA experience**
Selected as an astronaut in March 1992. After completing one year of training and evaluation, Parazynski served as one of the EVA crew representatives in the Astronaut Office Mission Development Branch. He served as the Astronaut Office Operations Planning Branch crew representative for Space Shuttle, Space Station and Soyuz training, and also served as Deputy (Operations and Training) of the Astronaut Office ISS Branch. Most recently, he served as Chief of the Astronaut Office EVA Branch. He was the Astronaut Office Lead for Space Shuttle Thermal Protection System Inspection and Repair following the Columbia tragedy.
**Space flight experience**
The STS-66 ATLAS-3 mission (3-14 November 1994): ATLAS-3 was part of an on-going programme to determine the Earth's energy balance and atmospheric change over an 11-year solar cycle, particularly with respect to human impact on the ozone. Parazynski had responsibility for a number of activities including operation of the ATLAS experiments. An exercise device he developed was also evaluated during the mission.

STS-86 (25 September to 6 October 1997): This Shuttle mission to the Mir Space Station included the first Shuttle-based joint American-Russian spacewalk. Parazynski was the navigator during the Mir rendezvous and performed a 5-hour spacewalk with Russian cosmonaut Vladimir Titov during which they retrieved four experiment packages. Other EVA objectives included the evaluation of EVA tools and a systems flight test of the Simplified Aid for EVA Rescue (SAFER).
STS-95 (29 October to 7 November 1998), which included ESA astronaut Pedro Duque was a 9-day mission during which the crew supported a variety of research payloads, including deployment of the Spartan solar-observing spacecraft and the testing of the Hubble Space Telescope Orbital Systems Test Platform. Parazynski’s tasks included being the navigator for the Spartan spacecraft rendezvous and operating the Shuttle’s robotic arm.
STS-100 (19 April to 1 May 2001) during which the crew successfully delivered and installed the "Canadarm2" robotic arm, on the International Space Station used for assembly and maintenance. Parazynski conducted two spacewalks with Canadian astronaut Chris Hadfield to assemble and power the robotic arm. Parazynski also operated the Shuttle’s robotic arm to install and remove a European-built Multi-Purpose Logistics Module.
All of these four missions have included a European astronaut: Jean-Francois Clervoy (STS-66), Jean-Loup Chrétien (STS-86), Pedro Duque (STS-95) and Umberto Guidoni (STS-100). Parazynski will serve as the Lead Spacewalker during the STS-120 mission.

## stay updated
Subscribe to our newsletter to receive the latest news, mission updates, and exclusive insights directly in your inbox. Be the first to know about our upcoming projects and breakthroughs.
</excerpt>
### Rank 2 of 86 — 0.34
<excerpt title="parazynski bio current">
## [PDF page 1]
Biographical Data
Lyndon B. Johnson Space Center  National Aeronautics and  
Houston, Texas  77058  Space Administration
SCOTT E. PARAZYNSKI (M .D.)  
NASA ASTRONAUT (FORM ER)
PERSONAL DATA:  Born July 28, 1961, in Little Rock, Arkansas.  He has  t wo  
beautiful  children.  He  enjoys mountaineering, rock climbing, flying, scuba  diving,  
skiing, travel, woodworking and nature photography.  A commercial, multi-  engine  
seaplane and instrument-rated pilot, Dr. Parazynski has  logged  more than  2,500 flight  
hours in a variety of aircraft.  As a mountaineer, he has scaled major mountains in the  
Alaska Range, the Cascades, the Rockies,  the Andes  and the Himalayas.  His summits  
include Cerro Aconcagua (22,841 feet above sea level) and  all  59  of Colorado’s peaks  
that are more than  14,000 feet in altitude.  After failing to reach the summit of Mount  
Everest (29,035  feet) in 2008,  due to a severe back injury, on May 20, 2009,  he became  
the first astronaut to stand on top of the world.
EDUCATION:  Attended junior high school in Dakar, Senegal, and Beirut, Lebanon.  
Attended high school at the Tehran American School, Iran, and the American  
Community School, Athens, Greece, graduating in 1979.  He received a B  achelor of  
Science degree in B  iology from Stanford University in 1983, continuing on to graduate with honors from Stanford Medical  
School in 1989.  He served his medical internship at the Brigham and Women’s Hospital of Harvard Medical School (1990).  He  
had completed 22 months of a residency program in emergency medicine in Denver, Colorado,  when  he was selected  fo r  the  
astronaut corps.

## [PDF page 1]
ORGANIZATIONS:  Fellow of the Aerospace Medical Association and the Explorers Club.  Member of the American Society  
for Gravitational and Space Biology,  the Wilderness Medical Society, the American Alpine Club, the Association of Space  
Explorers and the Aircraft Owners and Pilots Association.  Chairman  of the Board  of the  Challenger Center for Space Science  
Education and T rustee of the Houston Museum of N  atural Science.
SPECIAL HONORS:  National Institutes of Health Predoctoral T raining Award in Cancer Biology (1983); Rhodes Scholarship  
finalist (1984); NASA Graduate Student Researcher’s Award (1988); Stanford Medical Scholars Program (1988); Research  
Honors Award from Stanford Medical School (1989); NASA-Ames Certificate of Recognition (1990); Wilderness Medical  
Society Research Award (1991); Space Station Team Excellence Award (1996); Vladimir Komarov Diploma from the  
Fédération Aéronautique Internationale  (1995, 1999); NASA Exceptional Service Medals (1998, 1999); NASA Space Flight  
Medals (1994, 1997, 1998, 2001, 2007); NASA Distinguished Service Medals  (2002,  2009); Ellis Island Family Heritage Award  
(2005); Flight Achievement Award from the American Astronomical Association (1998, 2008); Aviation Week Laureate Award  
(2008);  Lowell Thomas Award from the Explorers Club (2008); Randolph C. Lovelace Award from the Society of NASA Flight  
Surgeons (2008); Arkansas Aviation Hall of Fame (2008); National Eagle Scout Association Outstanding Eagle Award (2012)
</excerpt>
### Rank 3 of 86 — 0.33
<excerpt title="parazynski bio current">
Title: PDF document  
URL Source: https://www.nasa.gov/wp-content/uploads/2016/01/parazynski_scott.pdf  
Markdown Content:

## [PDF page 1]
Biographical Data
Lyndon B. Johnson Space Center  National Aeronautics and  
Houston, Texas  77058  Space Administration
SCOTT E. PARAZYNSKI (M .D.)  
NASA ASTRONAUT (FORM ER)
PERSONAL DATA:  Born July 28, 1961, in Little Rock, Arkansas.  He has  t wo  
beautiful  children.  He  enjoys mountaineering, rock climbing, flying, scuba  diving,  
skiing, travel, woodworking and nature photography.  A commercial, multi-  engine  
seaplane and instrument-rated pilot, Dr. Parazynski has  logged  more than  2,500 flight  
hours in a variety of aircraft.  As a mountaineer, he has scaled major mountains in the  
Alaska Range, the Cascades, the Rockies,  the Andes  and the Himalayas.  His summits  
include Cerro Aconcagua (22,841 feet above sea level) and  all  59  of Colorado’s peaks  
that are more than  14,000 feet in altitude.  After failing to reach the summit of Mount  
Everest (29,035  feet) in 2008,  due to a severe back injury, on May 20, 2009,  he became  
the first astronaut to stand on top of the world.
EDUCATION:  Attended junior high school in Dakar, Senegal, and Beirut, Lebanon.  
Attended high school at the Tehran American School, Iran, and the American  
Community School, Athens, Greece, graduating in 1979.  He received a B  achelor of  
Science degree in B  iology from Stanford University in 1983, continuing on to graduate with honors from Stanford Medical  
School in 1989.  He served his medical internship at the Brigham and Women’s Hospital of Harvard Medical School (1990).  He  
had completed 22 months of a residency program in emergency medicine in Denver, Colorado,  when  he was selected  fo r  the  
astronaut corps.
</excerpt>
### Rank 4 of 86 — 0.32
<excerpt title="Born on this day, 28 July 1961, 🇺🇸 Scott Parazynski @astrodocscott ...">
Log In
Sign Up
everest_today
•
Follow
* * *
everest_today  
16w
Born on this day, 28 July 1961, 🇺🇸 Scott Parazynski @astrodocscott, American physician, former NASA astronaut and mountaineer.  
A veteran of five Space Shuttle missions and seven spacewalks, Parazynski reached the summit of Mt Everest in 2009. He became the first person in history to have both flown in space and stood on the world’s highest summit.
Photo © Scott Parazynski/NASA.
dr.fernandoesberard15w
🫡🫡🫡
Reply
418 2
July 28
Log in to like or comment.
More posts from everest_today
See more posts
* * *
</excerpt>
### Rank 5 of 86 — 0.29
<excerpt title="Scott E. Parazynski">
| Scott Parazynski |  
| --- |  
|  Official portrait, 2008 |  
| Born | Scott Edward Parazynski July 28, 1961 (age 65) Little Rock, Arkansas, U.S. |  
| Education | Stanford University (BS, MD) |  
| **Space career** |  
| NASA astronaut |  
| Time in space | 57d 15h 34m |  
| Selection | NASA Group 14 (1992) |  
| TotalEVAs | 7 |  
| Total EVA time | 47h 5m |  
| Mission | STS-66 STS-86 STS-95 STS-100 STS-120 |  
| Mission insignia |  |  
| Retired | March 24, 2009 |
**Scott Edward Parazynski** (born July 28, 1961) is an American physician and former NASAastronaut. A veteran of five Space Shuttle flights and seven spacewalks, Parazynski's latest mission was STS-120 in October 2007 – highlighted by a dramatic, unplanned extra-vehicular activity (EVA) to repair a live solar array. In May 2016, he was inducted into the United States Astronaut Hall of Fame. He retired from NASA in March 2009 to pursue entrepreneurial opportunities in the private sector, and he is currently the CEO of a technology start-up. He is the first person to have both flown in space and summited Mount Everest, the highest point on Earth.[[1]](https://en.wikipedia.org/wiki/Scott_E._Parazynski#cite_note-1) He describes his life's experiences in his 2017 memoir _The Sky Below_.[[2]](https://en.wikipedia.org/wiki/Scott_E._Parazynski#cite_note-2)

Parazynski is of Polish descent, as his great-great-grandparents migrated from Kraków to the US.[[3]](https://en.wikipedia.org/wiki/Scott_E._Parazynski#cite_note-se-3) He considers Palo Alto, California, and Evergreen, Colorado, to be his hometowns. He is married to Meenakshi Wadhwa, a planetary scientist at Arizona State University. He has two children with his first wife, Gail. Scott enjoys mountaineering, rock climbing, flying and scuba diving. A commercial, multi-engine, seaplane and instrument-rated pilot, Parazynski has logged over 2500 flight hours in a variety of aircraft. As a mountaineer, his summits include Cerro Aconcagua (at 22,841 feet (6,962 m) above sea level, the tallest mountain in the world outside Asia) and all 59 of Colorado's peaks over 14,000 feet (4,300 m) in altitude. He first attempted to summit Mount Everest in May 2008, but was forced to turn back before the summit due to a severe back injury. Serving as team physician for the Discovery Channel[[4]](https://en.wikipedia.org/wiki/Scott_E._Parazynski#cite_note-4) a year later, at 4:00 am on May 20, 2009, he successfully summited the 29,029 feet (8,848 m) mountain.

Other notable expeditions include a scientific dive into the summit caldera lake atop Licancabur Volcano (19,409 feet (5,916 m) on the Bolivian-Chilean border), one of the world's highest lakes, and setting the first bootprints adjacent Masaya Volcano's lava lake in Nicaragua with Sam Cossman in 2016.[[5]](https://en.wikipedia.org/wiki/Scott_E._Parazynski#cite_note-5) He also travelled aboard OceanGate's submersible _Titan_ and visited the wreck of the _Titanic_ in the North Atlantic.[[6]](https://en.wikipedia.org/wiki/Scott_E._Parazynski#cite_note-6)[[7]](https://en.wikipedia.org/wiki/Scott_E._Parazynski#cite_note-7)
</excerpt>

## Search 9 — query: "George Zamka birthdate"
### Rank 1 of 51 — 0.77 (passed on)
<excerpt title="On this day in 1962 Col. George Zamka (USMC, Ret.), raised in Rochester ...">
# On this day in 1962 Col. George... - Michigan Heroes Museum
## Michigan Heroes Museum's Post
[June 29, 2022](https://www.facebook.com/MIHeroes/posts/pfbid02cDLUDPrp5QqxRx3uWPWZgRuhAvV8f4DS7QaqtAush2LRiYwzJzSzK4TruMUkJfsol?__cft__[0]=AZgNr6ZdkbPtR3dRtarJF30A7e5cD06LyZ2417n2pMDYOaP1eMKdOg1ixUQYDsB8ZL2qul5-FuWUEn4wgoVnMVF39x-lXfmjDi73bfCmdVZLkqghVd83BK2Fiie6vQXIZUobVGJSel1JHj5XQ8E7XjgefE6uwbvK&__tn__=%2CO%2CP-R) ·
On this day in 1962 Col. George Zamka (USMC, Ret.), raised in Rochester Hills, MI, was born.

# On this day in 1962 Col. George... - Michigan Heroes Museum
## Michigan Heroes Museum's Post
Colonel Zamka received a Bachelor of Science degree in mathematics from the United States Naval Academy in 1984 and a Master of Science degree in engineering management from the Florida Institute of Technology in 1997. After basic flight training, he was trained as an A-6E pilot at Whidbey Island, Washington, in 1987-88. He then flew with Marine All Weather Attack Squadron VMA(AW)-242 in El Toro, California, and later served in administration and flight safety roles and also as Squadron Weapons and Tactics Instructor. In 1990, he trained to be an F/A-18 pilot and was assigned to Marine All Weather Fighter Attack Squadron VMFA(AW)-121, also in El Toro. He flew the F/A-18D Night Attack Hornet during overseas deployments to Japan, Korea, Singapore, and Southwest Asia. Zamka flew 66 combat missions over occupied Kuwait and Iraq during Desert Storm. In 1993 he served with First Battalion, Fifth Marines, in Camp Pendleton, California, and the 31st Marine Expeditionary Unit in the Western Pacific. He was selected to attend the United States Air Force Test Pilot School class 94A and graduated in December 1994. Zamka was then assigned as an F/A-18 test pilot/project officer and the F/A-18 Operations Officer for the Naval Strike Aircraft Test Squadron (NSATS). Zamka was selected in the seventeenth group of astronauts in 1998. Col. Zamka’s first shuttle mission was as pilot of STS-120 Discovery October 27-November 7, 2007, which delivered the Harmony Node module to the International Space Station. On his second spaceflight he commanded STS-130 Endeavour February 8–22, 2010, where he participated in the installation of the Tranquility Node and the Cupola, a large robotics workstation with seven windows providing views of the station as well as Earth.

# On this day in 1962 Col. George... - Michigan Heroes Museum
## Michigan Heroes Museum's Post
He has been awarded six Navy Strike Air Medals, Navy Commendation Medal with Combat V, three NASA Superior Accomplishment Awards, has been honored as a Distinguished Graduate, United States Naval Academy, and has also received the Officer’s Cross of the Order of Merit of the Republic of Poland. Over his two spaceflights he spent 28 days, 20 hours, and 29 minutes in space and orbited Earth 455 times. He currently serves as the Senior Assistant Vice President of Tactical Air Support, Inc.
Col. Zamka’s Marine uniform, astronaut flightsuit and other items he has donated can be seen at the Michigan Heroes Museum 10am-5pm daily. Honor. Respect. Remember.
</excerpt>
### Rank 2 of 51 — 0.76
<excerpt title="George D. Zamka">
From Wikipedia, the free encyclopedia
| George Zamka |  
| --- |  
|  |  
| Born | George David Zamka June 29, 1962 (age 64) Jersey City, New Jersey, U.S. |  
| Other name | Zambo |  
| Education | United States Naval Academy (BS) |  
| **Space career** |  
| NASA astronaut |  
| Rank | Colonel, USMC |  
| Time in space | 28d 20h 32m |  
| Selection | NASA Group 17 (1998) |  
| Mission | STS-120 STS-130 |  
| Mission insignia |  |
**George David "Zambo" Zamka** (born June 29, 1962) is a former NASAastronaut and United States Marine Corpspilot with over 3500 flight hours in more than 30 different aircraft. Zamka piloted the Space Shuttle _Discovery_ in its October 2007 mission to the International Space Station and served as the commander of mission STS-130 in February 2010.
George David Zamka was born on June 29, 1962, at Margaret Hague Hospital in Jersey City, New Jersey.[[1]](https://en.wikipedia.org/wiki/George_D._Zamka#cite_note-:0-1)[[2]](https://en.wikipedia.org/wiki/George_D._Zamka#cite_note-2) He was raised in New York City; Irvington, New York; Medellín, Colombia;[[3]](https://en.wikipedia.org/wiki/George_D._Zamka#cite_note-Mom-3) and Rochester Hills, Michigan. He graduated from Rochester Adams High School in Michigan in 1980. His personal hobbies include weightlifting, running, bicycling, scuba diving, and boating.[[4]](https://en.wikipedia.org/wiki/George_D._Zamka#cite_note-4)

Zamka is married and has two children. His extended family resides in Colorado, Mississippi, Georgia, Indiana, Florida and Tennessee. Zamka is of Colombian[[5]](https://en.wikipedia.org/wiki/George_D._Zamka#cite_note-5)[[6]](https://en.wikipedia.org/wiki/George_D._Zamka#cite_note-6) and Polish ancestry.[[7]](https://en.wikipedia.org/wiki/George_D._Zamka#cite_note-rhg-7)[[8]](https://en.wikipedia.org/wiki/George_D._Zamka#cite_note-8)[[9]](https://en.wikipedia.org/wiki/George_D._Zamka#cite_note-9)
Zamka graduated with a Bachelor of Science degree in mathematics from the United States Naval Academy in 1984. He was then commissioned as a second lieutenant in the United States Marine Corps. He received A-6E Intruder training at Naval Air Station Whidbey Island, Washington in 1985–1987. He was assigned to VMA(AW)-242 at Marine Corps Air Station El Toro, California. In addition to flight safety and administration, he was a squadron weapons and tactics instructor. In 1990, he trained as an F/A-18D Hornet pilot and was then assigned to VMFA(AW)-121. Zamka flew 66 combat missions during Operation Desert Storm. In 1993, he was assigned to the 1st Battalion, 5th Marines at Marine Corps Base Camp Pendleton, California as a forward air controller. In December 1994, he graduated from the U.S. Air Force Test Pilot School, following which, he served as an F/A-18 Hornet test pilot and operations officer.
In 1997, he earned a Masters of Science degree in engineering management from the Florida Institute of Technology. In 1998, he returned to VMFA(AW)-121 and deployed to MCAS Iwakuni, Japan.
</excerpt>
### Rank 3 of 51 — 0.73
<excerpt title="George D. Zamka">
Title: PDF document  
URL Source: https://www.nasa.gov/wp-content/uploads/2016/01/zamka_george.pdf  
Markdown Content:

## [PDF page 1]
Biographical Data
Lyndon B. Johnson Space Center  National Aeronautics and  
Houston, Texas  77058  Space Administration
GEORGE D. ZAM KA (COLONEL, USM C, RET.)  
NASA ASTRONAUT (FORM ER)
PERSONAL DATA:  Born in 19  62 in Jersey City, New Jersey.  Raised in New York  
City; Irvington, New York; Medellin, Colombia;  and Rochester Hills, Michigan.  
Married to the former Elisa P. Walker of Mississippi; they have two children.  He  
enjoys weightlifting, running, bicycling, scuba  diving  and boating.  His mother,  
So fia Za mk a ,  and brother,  Conrad P. Zamka,  both live in Florida.  His father,  
Conrad Za mk a , resides in Indiana.
EDUCATION:  Graduated from Rochester Adams High School, Rochester Hills  ,  
Michigan, in 1980. Received a Bachelor  o f  Science degree in M  athematics from the  
United States Naval Academy in 1984; received a Master of S  cience degree in  
Engineering Management from the Florida Institute of T echnology in 1997.
ORGANIZATIONS:  Association of Space Explorers, United States Naval Academy  
Alumni Association, Marine Corps Association and Marine Corps Aviation  
Association
SPECIAL HONORS:  NASA Space Flight Medal (t wo ),  NASA Outstanding Leadership Medal, Legion of Merit,  
Distinguished Flying Cross, Defense Meritorious Service Medal, Meritorious Service Medal, Navy Strike Air Medal (six),  
Navy Commendation Medal with Combat V and various other military service and campaign awards.  Distinguished Graduate,  
United States Naval Academy.  Commodore’s list and Academic Achievement Award, T raining Air Wing Five.  Awarded the  
Officer’s Cross of the Order of Merit of the Republic of Poland.
</excerpt>
### Rank 4 of 51 — 0.71
<excerpt title="George Zamka">
# George Zamka
## Related links
### George Zamka - Italian version
Astronauta della NASADati biograficiNato nel 1962 a Jersey City, New Jersey, USA. Sposato con Elisa Walker, ha due figli. Le sue passioni sono il sollevamento pesi, la corsa, il ciclismo, le immersioni, le barche.
Read article
* * *
Share this page
*   copy url  
*   (Opens in a new window)(Opens in a new window)

# George Zamka
## Related links
### Content
Social platforms
Messaging direct share
[](mailto:?body=https%3A%2F%2Fwww.esa.int%2Farticles%2Fgeorge-zamka)

# George Zamka
## stay updated
Subscribe to our newsletter to receive the latest news, mission updates, and exclusive insights directly in your inbox. Be the first to know about our upcoming projects and breakthroughs.
Join our newsletter(Opens in a new window)

# George Zamka
## ELEVATING THE FUTURE OF EUROPE
*   Mission  
*   Directorates  
*   Careers  
*   Business  
*   News

*   ESA Space shop(Opens in a new window)  
*   ESA Web TV(Opens in a new window)

*   Education(Opens in a new window)  
*   ESA kids(Opens in a new window)
English
*   Terms and conditions  
*   Privacy notice  
*   Cookie settings  
*   Newsletter
(Opens in a new window)(Opens in a new window)(Opens in a new window)(Opens in a new window)(Opens in a new window)(Opens in a new window)(Opens in a new window)
Loading languages
is your current language. Based on your location, would you like to switch to ?
We use cookies which are essential for you to access our website and/or to provide you with our services, enable you to share our website content via your social media accounts and allow us to measure and improve the performance of our website.
Accept all cookies Accept only essential cookiesSee our cookie notice

# George Zamka
## Cookie preferences
We use cookies which are essential for you to access our website and/or to provide you with our services, enable you to share our website content via your social media accounts and allow us to measure and improve the performance of our website.
Accept all cookies Accept only essential cookiesSee our cookie notice
</excerpt>
### Rank 5 of 51 — 0.70
<excerpt title="On this day in 1962 Col. George Zamka (USMC, Ret.), raised in Rochester ...">
# On this day in 1962 Col. George... - Michigan Heroes Museum
Log In

# On this day in 1962 Col. George... - Michigan Heroes Museum
## Michigan Heroes Museum's Post
* * *
[](https://www.facebook.com/MIHeroes?__cft__[0]=AZgNr6ZdkbPtR3dRtarJF30A7e5cD06LyZ2417n2pMDYOaP1eMKdOg1ixUQYDsB8ZL2qul5-FuWUEn4wgoVnMVF39x-lXfmjDi73bfCmdVZLkqghVd83BK2Fiie6vQXIZUobVGJSel1JHj5XQ8E7XjgefE6uwbvK&__tn__=%3C%3C%2CP-R)
### [**Michigan Heroes Museum**](https://www.facebook.com/MIHeroes?__cft__[0]=AZgNr6ZdkbPtR3dRtarJF30A7e5cD06LyZ2417n2pMDYOaP1eMKdOg1ixUQYDsB8ZL2qul5-FuWUEn4wgoVnMVF39x-lXfmjDi73bfCmdVZLkqghVd83BK2Fiie6vQXIZUobVGJSel1JHj5XQ8E7XjgefE6uwbvK&__tn__=-UC%2CP-R)
Wednesday, June 29, 2022 at 3:00 AM

# On this day in 1962 Col. George... - Michigan Heroes Museum
## Michigan Heroes Museum's Post
[June 29, 2022](https://www.facebook.com/MIHeroes/posts/pfbid02cDLUDPrp5QqxRx3uWPWZgRuhAvV8f4DS7QaqtAush2LRiYwzJzSzK4TruMUkJfsol?__cft__[0]=AZgNr6ZdkbPtR3dRtarJF30A7e5cD06LyZ2417n2pMDYOaP1eMKdOg1ixUQYDsB8ZL2qul5-FuWUEn4wgoVnMVF39x-lXfmjDi73bfCmdVZLkqghVd83BK2Fiie6vQXIZUobVGJSel1JHj5XQ8E7XjgefE6uwbvK&__tn__=%2CO%2CP-R) ·
On this day in 1962 Col. George Zamka (USMC, Ret.), raised in Rochester Hills, MI, was born.
</excerpt>

## Search 10 — query: "Stephanie Wilson astronaut birthdate"
### Rank 1 of 79 — 0.81 (passed on)
<excerpt title="STS -121 in 2006, STS-120, 2007 & STS-131 in 2010. Stephanie is the ...">
# HAPPY... - American Space Museum & Space Walk of Fame | Facebook
Log In
Log In
Forgot Account?

# HAPPY... - American Space Museum & Space Walk of Fame | Facebook
## American Space Museum & Space Walk of Fame's Post
* * *
[](https://www.facebook.com/stories/369654544005721/UzpfSVNDOjExNTE2Mjg5Mjc2MDU0NjE=/?view_single=false&__cft__[0]=AZg9N1aDPedgRCakF8QE49tUdn1W-50mtnmaz7WyxIwc583ac3KQDDFmPTuWx-9yc8hZGmoo-zx2Q0kSPXYN_XUwF2X6cdIb-etHI5IZYtvmNwiz7K9GsgqGDAfHlFCwhjsI2l1GvAGON--Y3bplrWcJ0TZCVuJj&__tn__=%3C%3C%2CP-R)
### [**American Space Museum & Space Walk of Fame**](https://www.facebook.com/SpaceWalkOfFame?__cft__[0]=AZg9N1aDPedgRCakF8QE49tUdn1W-50mtnmaz7WyxIwc583ac3KQDDFmPTuWx-9yc8hZGmoo-zx2Q0kSPXYN_XUwF2X6cdIb-etHI5IZYtvmNwiz7K9GsgqGDAfHlFCwhjsI2l1GvAGON--Y3bplrWcJ0TZCVuJj&__tn__=-UC%2CP-R)
Saturday, September 27, 2025 at 3:07 PM

# HAPPY... - American Space Museum & Space Walk of Fame | Facebook
## American Space Museum & Space Walk of Fame's Post
[September 27, 2025](https://www.facebook.com/SpaceWalkOfFame/posts/pfbid02JejWo7SsB4NtBoyXprsqAq8MX4YLF5Z7YbHHdHADXKGmrYZro76SdFPgZ4fyV2sml?__cft__[0]=AZg9N1aDPedgRCakF8QE49tUdn1W-50mtnmaz7WyxIwc583ac3KQDDFmPTuWx-9yc8hZGmoo-zx2Q0kSPXYN_XUwF2X6cdIb-etHI5IZYtvmNwiz7K9GsgqGDAfHlFCwhjsI2l1GvAGON--Y3bplrWcJ0TZCVuJj&__tn__=%2CO%2CP-R) ·
HAPPY BIRTHDAY ASTRONAUT STEPHANIE WILSON, 59 TODAY
Three-time Shuttle astronaut Stephanie Diana Wilson was born September 27, 1966 in Boston, Massachusetts and grew up in Pittsfield.
One of nine Artemis women selected for possible Moon missions, Stephanie has completed 58 orbits around the Sun, and 42 days orbiting Earth.
Stephanie Wilson’s three Shuttle missions orbiting around the Earth were all aboard Orbiter Discovery: STS-121 in 2006, STS-120, 2007 & STS-131 in 2010.
Stephanie is the second African American woman to go into space, after Mae Jemison. Her 42 days in space are the most of any female African-American astronaut.
Wilson graduated from Taconic High School, Pittsfield, Massachusetts, in 1984. She graduated Harvard University in 1988, receiving a bachelor of science degree in engineering science. Wilson earned a Master of Science degree in aerospace engineering from the University of Texas, in 1992. Wilson has returned to Harvard as a member of the Harvard Board of Overseers.
</excerpt>
### Rank 2 of 79 — 0.77
<excerpt title="Stephanie Wilson">
| Stephanie Wilson |  
| --- |  
|  Wilson in 2019 |  
| Born | Stephanie Diana Wilson September 27, 1966 (age 60) Boston, Massachusetts, U.S. |  
| Education | Harvard University (BS) University of Texas, Austin (MS) |  
| **Space career** |  
| NASA astronaut |  
| Time in space | 42d 23h 46m |  
| Selection | NASA Group 16 (1996) |  
| Missions | STS-121 STS-120 STS-131 |  
| Mission insignia |  |
**Stephanie Diana Wilson** (born September 27, 1966)[[1]](https://en.wikipedia.org/wiki/Stephanie_Wilson#cite_note-womenastronauts-1) is an American engineer and a NASAastronaut. She flew to space onboard three Space Shuttle missions and is the second African American woman to go into space after Mae Jemison. As of 2026, her almost 43 days in space are the second most of any female African American astronaut, having been surpassed by Jessica Watkins in 2022.

## Early life and education
[edit]
Wilson was born in Boston, Massachusetts on September 27, 1966. About a year later, her parents, Eugene and Barbara Wilson,[[2]](https://en.wikipedia.org/wiki/Stephanie_Wilson#cite_note-:0-2) decided to move to Pittsfield, Massachusetts.[[3]](https://en.wikipedia.org/wiki/Stephanie_Wilson#cite_note-3) Eugene, a native of Nesmith, South Carolina, used his electronics training from his time in the Navy to get himself a degree from Northeastern University and a long career in electrical engineering for Raytheon, Sprague Electric, and Lockheed Martin,[[2]](https://en.wikipedia.org/wiki/Stephanie_Wilson#cite_note-:0-2)[[4]](https://en.wikipedia.org/wiki/Stephanie_Wilson#cite_note-4) while Barbara, from Talbot County, Georgia,[[5]](https://en.wikipedia.org/wiki/Stephanie_Wilson#cite_note-5) worked as a production assistant for Lockheed Martin.[[2]](https://en.wikipedia.org/wiki/Stephanie_Wilson#cite_note-:0-2)
After attending Stearns Elementary School, she attended Crosby Junior High School.[[6]](https://en.wikipedia.org/wiki/Stephanie_Wilson#cite_note-iberkshires.com-6) For a career awareness class in middle school, Wilson was assigned to interview someone in a field that interested her. Since she liked to look up at the sky,[[7]](https://en.wikipedia.org/wiki/Stephanie_Wilson#cite_note-7) she interviewed Williams College astronomer Jay Pasachoff,[[6]](https://en.wikipedia.org/wiki/Stephanie_Wilson#cite_note-iberkshires.com-6) clarifying her potential career interest in space. In high school, Eugene encouraged Stephanie to go into engineering,[[2]](https://en.wikipedia.org/wiki/Stephanie_Wilson#cite_note-:0-2) so she decided to become an aerospace engineer.
</excerpt>
### Rank 3 of 79 — 0.77
<excerpt title="Stephanie Wilson">
## Early life and education
[edit]
Wilson was born in Boston, Massachusetts on September 27, 1966. About a year later, her parents, Eugene and Barbara Wilson,[[2]](https://en.wikipedia.org/wiki/Stephanie_Wilson#cite_note-:0-2) decided to move to Pittsfield, Massachusetts.[[3]](https://en.wikipedia.org/wiki/Stephanie_Wilson#cite_note-3) Eugene, a native of Nesmith, South Carolina, used his electronics training from his time in the Navy to get himself a degree from Northeastern University and a long career in electrical engineering for Raytheon, Sprague Electric, and Lockheed Martin,[[2]](https://en.wikipedia.org/wiki/Stephanie_Wilson#cite_note-:0-2)[[4]](https://en.wikipedia.org/wiki/Stephanie_Wilson#cite_note-4) while Barbara, from Talbot County, Georgia,[[5]](https://en.wikipedia.org/wiki/Stephanie_Wilson#cite_note-5) worked as a production assistant for Lockheed Martin.[[2]](https://en.wikipedia.org/wiki/Stephanie_Wilson#cite_note-:0-2)
After attending Stearns Elementary School, she attended Crosby Junior High School.[[6]](https://en.wikipedia.org/wiki/Stephanie_Wilson#cite_note-iberkshires.com-6) For a career awareness class in middle school, Wilson was assigned to interview someone in a field that interested her. Since she liked to look up at the sky,[[7]](https://en.wikipedia.org/wiki/Stephanie_Wilson#cite_note-7) she interviewed Williams College astronomer Jay Pasachoff,[[6]](https://en.wikipedia.org/wiki/Stephanie_Wilson#cite_note-iberkshires.com-6) clarifying her potential career interest in space. In high school, Eugene encouraged Stephanie to go into engineering,[[2]](https://en.wikipedia.org/wiki/Stephanie_Wilson#cite_note-:0-2) so she decided to become an aerospace engineer.

## Early life and education
Wilson graduated from Taconic High School, Pittsfield, Massachusetts, in 1984. She attended Harvard University, receiving a Bachelor of Science degree in engineering science in 1988. Wilson earned a Master of Science degree in aerospace engineering from the University of Texas in 1992.[[1]](https://en.wikipedia.org/wiki/Stephanie_Wilson#cite_note-womenastronauts-1) Wilson has returned to Harvard as a member of the Harvard Board of Overseers.[[8]](https://en.wikipedia.org/wiki/Stephanie_Wilson#cite_note-8) She was the Chief Marshal for the 362nd Harvard Commencement on May 30, 2013.[[9]](https://en.wikipedia.org/wiki/Stephanie_Wilson#cite_note-9)
Wilson during STS-120, with a model of Node 2 floating in front of her
Wilson worked for two years for the former Martin Marietta Astronautics Group in Denver, Colorado. As a Loads and Dynamics engineer for the Titan IV rocket, Wilson was responsible for performing coupled loads analyses for the launch vehicle and payloads during flight events. Wilson left Martin Marietta in 1990 to attend graduate school at the University of Texas. Her research focused on the control and modeling of large, flexible space structures.
Following the completion of her graduate work, Wilson began working for the Jet Propulsion Laboratory in Pasadena, California, in 1992. As a member of the Attitude and Articulation Control Subsystem for the Galileo spacecraft, Wilson was responsible for assessing attitude controller performance, science platform pointing accuracy, antenna pointing accuracy, and spin rate accuracy. She worked in the areas of sequence development and testing as well. While at the Jet Propulsion Laboratory, Wilson also supported the Interferometery Technology Program as a member of the Integrated Modeling Team, which was responsible for finite element modeling, controller design, and software development.
</excerpt>
### Rank 4 of 79 — 0.76
<excerpt title="Happy birthday astronaut Stephanie Wilson, 59 today">
# HAPPY... - American Space Museum & Space Walk of Fame | Facebook
Log In
Log In
Forgot Account?

# HAPPY... - American Space Museum & Space Walk of Fame | Facebook
## American Space Museum & Space Walk of Fame's Post
* * *
[](https://www.facebook.com/stories/369654544005721/UzpfSVNDOjExNTE2Mjg5Mjc2MDU0NjE=/?view_single=false&__cft__[0]=AZhtb_IWNbEQNeIKdZW2q21BV7-uVdk_XUtoPHpYWuS0lNqT5YY7ZxJs6Hoz7RDc0XJB7pZMXQChhBsHRLAdzL0YzQ7eauFcnSM0ghnSQLUhAzroKfG_ruN0ffB4grPAD8VddOnuJPoEJLenyDyDp2dgt9_vxRLU&__tn__=%3C%3C%2CP-R)
### [**American Space Museum & Space Walk of Fame**](https://www.facebook.com/SpaceWalkOfFame?__cft__[0]=AZhtb_IWNbEQNeIKdZW2q21BV7-uVdk_XUtoPHpYWuS0lNqT5YY7ZxJs6Hoz7RDc0XJB7pZMXQChhBsHRLAdzL0YzQ7eauFcnSM0ghnSQLUhAzroKfG_ruN0ffB4grPAD8VddOnuJPoEJLenyDyDp2dgt9_vxRLU&__tn__=-UC%2CP-R)
Sunday, September 27, 2026 at 9:01 PM

# HAPPY... - American Space Museum & Space Walk of Fame | Facebook
## American Space Museum & Space Walk of Fame's Post
[September 27](https://www.facebook.com/SpaceWalkOfFame/posts/pfbid02o4H3nZNtZFfLNPhJTU4VNKCgDPbjGXscbgCLAVnhxqBkLvLcBMaFps6NFvG9qKaJl?__cft__[0]=AZhtb_IWNbEQNeIKdZW2q21BV7-uVdk_XUtoPHpYWuS0lNqT5YY7ZxJs6Hoz7RDc0XJB7pZMXQChhBsHRLAdzL0YzQ7eauFcnSM0ghnSQLUhAzroKfG_ruN0ffB4grPAD8VddOnuJPoEJLenyDyDp2dgt9_vxRLU&__tn__=%2CO%2CP-R) ·
HAPPY BIRTHDAY ASTRONAUT STEPHANIE WILSON, 60 TODAY
Three-time Shuttle astronaut Stephanie Diana Wilson was born September 27, 1966 in Boston, Massachusetts and grew up in Pittsfield.
One of nine Artemis women selected for possible Moon missions, Stephanie has completed 58 orbits around the Sun, and 42 days orbiting Earth.
Stehanie Wilson’s three Shuttle missions orbiting around the Earth were all aboard Orbiter Discovery: STS-121 in 2006, STS-120, 2007 & STS-131 in 2010.
Stephanie is the second African American woman to go into space, after Mae Jemison. Her 42 days in space are the most of any female African-American astronaut.
</excerpt>
### Rank 5 of 79 — 0.76
<excerpt title="STS -121 in 2006, STS-120, 2007 & STS-131 in 2010. Stephanie is the ...">
# HAPPY... - American Space Museum & Space Walk of Fame | Facebook
## American Space Museum & Space Walk of Fame's Post
[September 27, 2025](https://www.facebook.com/SpaceWalkOfFame/posts/pfbid02JejWo7SsB4NtBoyXprsqAq8MX4YLF5Z7YbHHdHADXKGmrYZro76SdFPgZ4fyV2sml?__cft__[0]=AZg9N1aDPedgRCakF8QE49tUdn1W-50mtnmaz7WyxIwc583ac3KQDDFmPTuWx-9yc8hZGmoo-zx2Q0kSPXYN_XUwF2X6cdIb-etHI5IZYtvmNwiz7K9GsgqGDAfHlFCwhjsI2l1GvAGON--Y3bplrWcJ0TZCVuJj&__tn__=%2CO%2CP-R) ·
HAPPY BIRTHDAY ASTRONAUT STEPHANIE WILSON, 59 TODAY
Three-time Shuttle astronaut Stephanie Diana Wilson was born September 27, 1966 in Boston, Massachusetts and grew up in Pittsfield.
One of nine Artemis women selected for possible Moon missions, Stephanie has completed 58 orbits around the Sun, and 42 days orbiting Earth.
Stephanie Wilson’s three Shuttle missions orbiting around the Earth were all aboard Orbiter Discovery: STS-121 in 2006, STS-120, 2007 & STS-131 in 2010.
Stephanie is the second African American woman to go into space, after Mae Jemison. Her 42 days in space are the most of any female African-American astronaut.
Wilson graduated from Taconic High School, Pittsfield, Massachusetts, in 1984. She graduated Harvard University in 1988, receiving a bachelor of science degree in engineering science. Wilson earned a Master of Science degree in aerospace engineering from the University of Texas, in 1992. Wilson has returned to Harvard as a member of the Harvard Board of Overseers.

# HAPPY... - American Space Museum & Space Walk of Fame | Facebook
## American Space Museum & Space Walk of Fame's Post
She is married to Julius McCurdy, and enjoys skiing and stamp collecting.
Happy birthday and we hope you enjoyed YOUR day, Stephanie!
Wilson’s NASA bio:
[https://www.nasa.gov/.../bio.../stephanie-d-wilson/biography](https://l.facebook.com/l.php?u=https%3A%2F%2Fwww.nasa.gov%2Fastronauts%2Fbiographies%2Fstephanie-d-wilson%2Fbiography&h=AUCP7xjjKF0fSP9Xqw3163idvnchyW3vI92yXKElua3fDdkgBzSp8O9I4b_j3ECrCw4ixYM7-k1bwwR35rO9g_s8Bmpt5RTmzu3yFJfGPtX-ix_P5bOHQkrZZGc2yrrgWH73owOVDy8LE5-gckDzdveQzdIGfWOrbkmzEw&__tn__=-UK-R&c[0]=AUAuKIJQze-po7hYAiRWdhPdus1oA2045FbCxgxLZQ_IZCMcEzcbb8mAOGUI3kNAFrN_gaUtU3WkuTD8x0KZ3Flq5NEFdOvliQMVQUoWd9XKObLSHdESXV-65aPO3CPVTpmE8x6aCBCex5EklyZkuBgYCnmAwU4FJf_wt8LQrir7MeNC25VJ-xeNotax7Hg)
</excerpt>

# Example 5
## Question
According to the World Spider Catalog, which spiders of the family Desidae and genus Desis are native to one country. Provide their full scientific names and the location they are indigenous to.

## Expected answer
Desis bobmarleyi - Endemic to Australia (specifically Queensland), Desis galapagoensis - Endemic to the Galapagos Islands (Ecuador), Desis gardineri - Endemic to the Laccadive Islands (India), Desis inermis - Endemic to India, Desis japonica - Endemic to Japan, Desis jiaxiangi - Endemic to China, Desis kenyonae - Endemic to Australia (specifically Victoria and Tasmania), Desis vorax - Endemic to Samoa, Desis risbeci - Endemic to New Caledonia

## Grade 0.95

## Search 1 — query: "World Spider Catalog Desis species native only to one country"
### Rank 1 of 160 — 0.85 (passed on)
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
### Rank 2 of 160 — 0.84
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
### Rank 3 of 160 — 0.76
<excerpt title="World Spider Catalog">
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

**_Desis vorax_**L. Koch, 1872  |  | Samoa urn:lsid:nmbe.ch:spidersp:021493
_Desis vorax_**L. Koch, 1872a**: 345, pl. 29, f. 1 (D
m  
) Original description
</excerpt>
### Rank 4 of 160 — 0.75
<excerpt title="World Spider Catalog">
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
</excerpt>
### Rank 5 of 160 — 0.73
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

## Search 2 — query: "Desis species list World Spider Catalog""
### Rank 1 of 65 — 0.89 (passed on)
<excerpt title="[Arachnida • 2020] <i>Desis jiaxiangi </i>• First Report of the Spider Genus ...">
Species New to Science
new & recent described Flora & Fauna species from all over the World esp. Asia, Oriental, Indomalayan & Malesiana region
Friday, May 1, 2020  
[Arachnida • 2020] Desis jiaxiangi • First Report of the Spider Genus Desis (Araneae, Desidae) from China, with Description of A New Species
Desis jiaxiangi Lin, Li & Chen, 2020
DOI: 10.11646/zootaxa.4755.3.11  
Photograph by Zixuan Lin.
The spider genus Desis Walckenaer, 1837 is the type genus of the spider family Desidae Pocock, 1895. Desis spiders hide in silk sacs between rocks or shells during high tide and forage during low tide (Baehr et al. 2017). Four Desis species have been recorded from Asia: Desis gardineri Pocock, 1904 (India), Desis inermis Gravely, 1927 (India), Desis japonica Yaginuma, 1956 (Japan) and Desis martensi L. Koch, 1872 (Malaysia) (World Spider Catalog 2020). Until now, only one species of the family Desidae, Badumna tangae Zhu, Zhang & Yang, 2006, has been reported from China (Zhu et al. 2006). Here, we describe a new species of Desis and report the genus from China for the first time.
Figure 4. Desis jiaxiangi, live holotype male.
Photograph by Zixuan Lin.
Desis jiaxiangi sp. nov.
Etymology. The species is named after Mr Jiaxiang Wu, the collector of the holotype; noun (name) in genitive case.

Yejie Lin, Shuqiang Li and Haifeng Chen. 2020. First Report of the Spider Genus Desis (Araneae, Desidae) from China, with Description of A New Species. Zootaxa. 4755(3); 593–597. DOI: 10.11646/zootaxa.4755.3.11
</excerpt>
### Rank 2 of 65 — 0.88
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
### Rank 3 of 65 — 0.84
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
### Rank 4 of 65 — 0.83
<excerpt title="World Spider Catalog">
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

**_Desis vorax_**L. Koch, 1872  |  | Samoa urn:lsid:nmbe.ch:spidersp:021493
_Desis vorax_**L. Koch, 1872a**: 345, pl. 29, f. 1 (D
m  
) Original description
</excerpt>
### Rank 5 of 65 — 0.80
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

## Search 3 — query: "site:wsc.nmbe.ch "Desis" "Desidae" 2017"
### Rank 1 of 783 — 0.85 (passed on)
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
### Rank 2 of 783 — 0.83
<excerpt title="World Spider Catalog">
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

**_Desis vorax_**L. Koch, 1872  |  | Samoa urn:lsid:nmbe.ch:spidersp:021493
_Desis vorax_**L. Koch, 1872a**: 345, pl. 29, f. 1 (D
m  
) Original description
</excerpt>
### Rank 3 of 783 — 0.83
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
### Rank 4 of 783 — 0.83
<excerpt title="Desidae Pocock, 1895">
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
</excerpt>
### Rank 5 of 783 — 0.83
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

## Search 4 — query: "Desis bobmarleyi WSC"
### Rank 1 of 86 — 0.72 (passed on)
<excerpt title="Lyrical Spider - University of Texas Marine Science Institute">
Skip to content
This marine spider was recently cataloged and named after Bob Marley in reference to the song “High Tide or Low Tide” which aptly describes the spider’s habitat. Credit: Robert Raven, CC BY 4.0
DATE July 9, 2023
VOLUME 69
EPISODE 2
Audio 3
A few years ago, some scientists in Australia got a tip from a city council member in a town in the state of Queensland, on the country’s northeastern coast: Some unusual spiders were appearing on the beaches of a nearby town during especially low tides.
The scientists checked it out. And their analysis revealed that the spider belonged to a species that hadn’t been cataloged before. So they recorded its details—an adult male is about a quarter of an inch long, a female about 50 percent larger, for example. And they gave it a name: _Desis bobmarleyi_—Bob Marley’s Intertidal Spider. The name was inspired by a song by the Reggae singer and writer, “High Tide or Low Tide.” The name seemed fitting for the spider, which lives full-time in the zone between the limits of high and low tides.
When the tide is high, the spider finds a small air pocket in the rocks, coral, a barnacle shell, or a clump of seaweed. It then spins a web to seal the entrance to the pocket, so it can survive for hours while submerged. One of the spiders found by the research team, for example, had created a nest in a coral that was as much as 10 feet deep at high tide.
Bobmarleyi comes out to eat at low tide. It catches tiny organisms on the rocks, plants, coral, or debris that’s washed up on the beach. And when the tide rolls back in, it walls itself up again—waiting for the next chance to come out of its water-tight home on the Australian beach.
</excerpt>
### Rank 2 of 86 — 0.62
<excerpt title="[Arachnida • 2017] Desis bobmarleyi • A New Spider (Araneae, Desidae) ...">
Species New to Science
new & recent described Flora & Fauna species from all over the World esp. Asia, Oriental, Indomalayan & Malesiana region
Friday, December 29, 2017  
[Arachnida • 2017] Desis bobmarleyi • A New Spider (Araneae, Desidae) from Coral Reefs in Australia’s Sunshine State and its Relative from Sāmoa
Desis bobmarleyi
Baehr, Raven & Harms, 2017
DOI: 10.3897/evolsyst.1.15735
Abstract  
Spiders of the genus Desis Walckenaer, 1837 (Araneae: Desidae) are water-adapted spiders and live in the intertidal zone on reefs, marine debris and under rocks. Here, we describe a new intertidal species from tropical Queensland and name it after Bob Marley, whose song “High Tide or Low Tide” inspired us as it lives in a “high tide low tide” habitat. We also re-describe a close morphological relative, Desis vorax L. Koch, 1872 from Sāmoa. This species was described some 150 years ago from the Godeffroy Collection which holds the oldest major collection of Australasian and Pacific spiders, now mainly hosted in the Centre of Natural History in Hamburg (CeNak). A third species, Desis hartmeyeri Simon, 1909, was described from juvenile specimens only and is considered a nomen dubium.
“None but ourselves can free our minds.” Bob Marley, Redemption Song (1980).
Key Words: Taxonomy, systematics, new species, Bob Marley, intertidal, spiders, Australia, Pacific
Figure 1. Life image of Desis bobmarleyi sp. n. female allotype
(Photo: R. Raven).
Desis bobmarleyi male holotype
(photo: R. Raven)
Systematics  
Family DESIDAE Pocock, 1895  
Subfamily Desinae Pocock, 1895
Desis Walckenaer, 1837
Desis bobmarleyi sp. n.
</excerpt>
### Rank 3 of 86 — 0.62
<excerpt title="Desis bobmarleyi, a marine spider species in Australia">
# Wildlife Animals | Desis bobmarleyi | Facebook
Desis* bobmarleyi is an underwater spider species found in the shores of north eastern Queensland, Australia. It is known to build air chambers from silk. D. bobmarleyi is named in honour of the Jamaican singer-songwriter Bob Marley (1945 – 1981). As an intertidal species the name was inspired by Marley's song "High Tide or Low Tide". In April 2018 the World Register of Marine Species named it one of the top 10 most remarkable species discovered in 2017. The spider is an araneomorph. D. bobmarleyi is a recent discovery, which is important to note when examining its data. Additionally, because it is part of the genus Desis, it is considered a fully aquatic animal which is interesting because of its evolutionary history. The trnL2 and trnN genes, which are seen in marine spiders that are a part of the genus, must have experienced some kind of rearrangement that allowed for the development of its current traits. The long hairs on its legs and abdomen trap an air bubble which allows it to breathe while submerged.
* Desis is a genus of intertidal spiders that was first described by Charles Athanase Walckenaer in 1837. It is found in Australasia, the Pacific, Japan, eastern and southern Africa, and India. They are truly marine spiders, living in the intertidal zone and only emerging at night on the ebb tide to hunt for invertebrates and small fish. In the day and during high tides, they hide in an air chamber sealed with silk.
As of May 2019 it contains fourteen species.

# Wildlife Animals | Desis bobmarleyi | Facebook
[](https://www.facebook.com/photo/?fbid=347087711146253&set=gm.3392335157646066&idorvanity=2489985901214334&__cft__[0]=AZgX-vS2cj0331Y8xiT2A293uj8h5wzElN_Dej1h-l4tWpd8XG4ofn7YGWzWTHc_Har2YBOkVm-xc7D28T4w0B-TlvGkL0ssUAi57zwigcKj2oSyqhPCsJaCDYeiNR1WEnFDMBop34xaluishKGoqpgFql0yFTpkBJZUzObnW1gomx71BA0IWZu6l58RhWsv&__tn__=EH-R)
![Image 4](blob:http://localhost/b2a9e322d16c8b9e64f4456e8bf93e51)
All reactions:
1
1 comment
1 share
Like
Comment
Share
Most relevant
Irena Nagyova
Moderator

# Wildlife Animals | Desis bobmarleyi | Facebook
*   [3y](https://www.facebook.com/groups/2489985901214334/posts/3392335157646066/?comment_id=3392344210978494&__cft__[0]=AZgX-vS2cj0331Y8xiT2A293uj8h5wzElN_Dej1h-l4tWpd8XG4ofn7YGWzWTHc_Har2YBOkVm-xc7D28T4w0B-TlvGkL0ssUAi57zwigcKj2oSyqhPCsJaCDYeiNR1WEnFDMBop34xaluishKGoqpgFql0yFTpkBJZUzObnW1gomx71BA0IWZu6l58RhWsv&__tn__=R]-R)
1
![Image 6](blob:http://localhost/520c193f0276d495fb772a9afb8b220d)
See more on Facebook
See more on Facebook
Email or phone number
Password
Log In
Forgot password?
or
Create new account
</excerpt>
### Rank 4 of 86 — 0.61
<excerpt title="Desis bobmarleyi, a marine spider species in Australia">
# Wildlife Animals | Desis bobmarleyi | Facebook
Log In
Log In
Forgot Account?
[](https://www.facebook.com/groups/2489985901214334/?__cft__[0]=AZgX-vS2cj0331Y8xiT2A293uj8h5wzElN_Dej1h-l4tWpd8XG4ofn7YGWzWTHc_Har2YBOkVm-xc7D28T4w0B-TlvGkL0ssUAi57zwigcKj2oSyqhPCsJaCDYeiNR1WEnFDMBop34xaluishKGoqpgFql0yFTpkBJZUzObnW1gomx71BA0IWZu6l58RhWsv&__tn__=%3C%3C%2CP-R)
## [Wildlife Animals](https://www.facebook.com/groups/2489985901214334/?__cft__[0]=AZgX-vS2cj0331Y8xiT2A293uj8h5wzElN_Dej1h-l4tWpd8XG4ofn7YGWzWTHc_Har2YBOkVm-xc7D28T4w0B-TlvGkL0ssUAi57zwigcKj2oSyqhPCsJaCDYeiNR1WEnFDMBop34xaluishKGoqpgFql0yFTpkBJZUzObnW1gomx71BA0IWZu6l58RhWsv&__tn__=-UC%2CP-R) ·
Join
Caleb Jones
·
Admin
·
Thursday, October 19, 2023 at 10:51 AM

# Wildlife Animals | Desis bobmarleyi | Facebook
[October 19, 2023](https://www.facebook.com/groups/2489985901214334/?multi_permalinks=3392335157646066&hoisted_section_header_type=recently_seen&__cft__[0]=AZgX-vS2cj0331Y8xiT2A293uj8h5wzElN_Dej1h-l4tWpd8XG4ofn7YGWzWTHc_Har2YBOkVm-xc7D28T4w0B-TlvGkL0ssUAi57zwigcKj2oSyqhPCsJaCDYeiNR1WEnFDMBop34xaluishKGoqpgFql0yFTpkBJZUzObnW1gomx71BA0IWZu6l58RhWsv&__tn__=%2CO%2CP-R) ·
Desis bobmarleyi, a marine spider species in Australia
Titles are generated by AI from Meta
Desis bobmarleyi.
''Desis species are marine spiders that live in the intertidal zone, often in coral reefs. During high tides, they hide underwater in an air chamber sealed with silk. They emerge at night during low tides to to hunt for invertebrates and small fish.
Healthy oceans are the life support system for our planet, and we need to work to protect them and their inhabitants.''
Quote by Joseph Schubert (biologist primarily interested in the taxonomy/systematics, evolution, and behaviour of Australian spiders) and photos from ''Baehr, Raven & Harms'' (2017).
</excerpt>
### Rank 5 of 86 — 0.60
<excerpt title="[Arachnida • 2017] Desis bobmarleyi • A New Spider (Araneae, Desidae) ...">
Etymology: The specific name is a patronym in honour of Bob Marley, an internationally renowned Jamaican Reggae singer and songwriter.
Common name: We propose Bob Marley’s Intertidal Spider as a common name.
Diagnosis: Males of Desis bobmarleyi sp. n. resemble D. kenyonae, D. marina and D. vorax in having a broad, semicircular conductor with a retrolateral conductor plate, a hood-shaped DTA and a spine-like MTA but can be separated from these by having a broadly triangular conductor plate (CP), a stout conductor tip and an indented hood–shaped tip of the retrodistal apophysis (DTA) (Figs 3E, 7A, B). Females of Desis bobmarleyi sp. n. share the long convoluted copulatory ducts but have them arranged spherical not longitudinal (Fig. 7D).
Distribution: Known from intertidal zones of the Great Barrier Reef at the north-eastern coast of Queensland: Australia’s “Sunshine State”. The exact distribution range along the coastline of Australia is still unknown.
Figure 2. Locality and life images of Desis bobmarleyi sp. n.:  
A, beach near Port Douglas high tide; B, same low tide; C, Desis bobmarleyi sp. n. on coral at low tide (photo: Paul Hoye); D, Desis bobmarleyi male holotype (photo: R. Raven).
Barbara C. Baehr, Robert Raven and Danilo Harms. 2017. “High Tide or Low Tide”: Desis bobmarleyi sp. n., A New Spider from Coral Reefs in Australia’s Sunshine State and its Relative from Sāmoa (Araneae, Desidae, Desis). Evolutionary Systematics. 1; 111-120.  DOI: 10.3897/evolsyst.1.15735  
New species of marine spider emerges at low tide to remind scientists of Bob Marley  phy.so/433168954 via @physorg_com
</excerpt>

## Search 5 — query: "site:wsc.nmbe.ch "species-list" "Desis""
### Rank 1 of 1 — 0.56 (passed on)
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

## Search 6 — query: "Desis formidabilis distribution"
### Rank 1 of 14 — 0.83 (passed on)
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
### Rank 2 of 14 — 0.81
<excerpt title="Desis formidabilis (Formidable Shore Spider)">
Desis formidabilis is a desid spider adapted to rocky intertidal shores in southern Africa. A study on the Cape Peninsula found its nests concentrated in the middle shore zone rather than higher or lower parts of the shore. The spider’s  sacs can be parasitized by the  Echthrodesis lamorali, linking its nests to a documented shore-food-web interaction.

## Images


## Habitat
On Cape Peninsula rocky shores, nests were more abundant in the mid-shore zone than at higher or lower shore levels.

## Distribution
Recorded from coastal Namibia and South Africa, including the Cape Peninsula.

## Host Associations
*   **Echthrodesis lamorali** - An  whose offspring develop in D. formidabilis egg sacs.The study found  activity in 13.85% of sampled  sacs.

## Life Cycle
The  Echthrodesis lamorali lays eggs in D. formidabilis egg sacs; where the  entered a sac, all eggs in it were parasitized.

## Behavior
Builds nests on the shore; on studied Cape Peninsula sites, nests were most abundant in the mid-shore zone.

## Ecological Role
Its  sacs provide a  resource for the  Echthrodesis lamorali. In one Cape Peninsula study,  activity occurred in 43.31% of sampled nests.

## Tags


## Sources and further reading
</excerpt>
### Rank 3 of 14 — 0.75
<excerpt title="Desis formidabilis">
Several synonyms have been established through taxonomic revision, including _Paradesis tubicola_ Pocock, 1898, _Desis pentheri_ Simon, 1910, and _Desis beckeri_ Hewitt, 1913.[[1]](https://en.wikipedia.org/wiki/Desis_formidabilis#cite_note-wsc-1)
_Desis formidabilis_ is found along the coastlines of Namibia and South Africa.[[1]](https://en.wikipedia.org/wiki/Desis_formidabilis#cite_note-wsc-1) In South Africa, the species has been recorded from the Eastern Cape and Western Cape provinces.[[2]](https://en.wikipedia.org/wiki/Desis_formidabilis#cite_note-dippenaar-2) Notable localities include Port Alfred, East London, Port Elizabeth, [Betty's Bay](https://en.wikipedia.org/wiki/Betty's_Bay "Betty's Bay"), Hermanus, Cape Point, and Saldanha Bay.[[2]](https://en.wikipedia.org/wiki/Desis_formidabilis#cite_note-dippenaar-2)
This species is specialized for life in the intertidal zone, inhabiting rocky shores between the low water neap and high water neap tide levels. As a result, it is submerged twice daily for several hours during high tide cycles. The spider constructs retreats in rock crevices and is adapted to the semi-aquatic lifestyle typical of the genus _Desis_.[[3]](https://en.wikipedia.org/wiki/Desis_formidabilis#cite_note-cambridge1891-3)
_Desis formidabilis_ exhibits sexual size dimorphism, with females being notably larger than males.[[3]](https://en.wikipedia.org/wiki/Desis_formidabilis#cite_note-cambridge1891-3) Adult males measure 9.5 to nearly 15 mm in length (excluding chelicerae), while females including the chelicerae reach 20 mm.[[3]](https://en.wikipedia.org/wiki/Desis_formidabilis#cite_note-cambridge1891-3)

The cephalothorax, chelicerae, labium, maxillae, and sternum are rich liver-colored. The legs and pedipalps are yellow-brown with reddish tinges. The opisthosoma is dull brown.[[3]](https://en.wikipedia.org/wiki/Desis_formidabilis#cite_note-cambridge1891-3) The cephalothorax is slightly longer than the chelicerae, with a broad-oval form that is truncated at the front. The surface is clothed with short, light brownish hairs, but not densely.[[3]](https://en.wikipedia.org/wiki/Desis_formidabilis#cite_note-cambridge1891-3)
The chelicerae are notably long and powerful, projecting forward and curved, with strong teeth on their inner sides. They are furnished with numerous hairs, and the fangs are long, strong, and slightly curved. The eye arrangement follows the typical pattern for the genus, with the posterior median eyes positioned much closer to each other than to the lateral eyes in the same row.[[3]](https://en.wikipedia.org/wiki/Desis_formidabilis#cite_note-cambridge1891-3)
The legs are moderate in length and strength, following the formula I, IV, II, III. They lack spines but are densely clothed with hairs, particularly on the metatarsi and tarsi, which almost form scopulae. The terminal claws are strong, with the superior pair furnished with 6-7 small teeth toward their base.[[3]](https://en.wikipedia.org/wiki/Desis_formidabilis#cite_note-cambridge1891-3)
The species is listed as Least Concern on the South African Red List due to its relatively wide distribution range. However, potential threats include oil spills and coastal pollution, which could affect population numbers.[[2]](https://en.wikipedia.org/wiki/Desis_formidabilis#cite_note-dippenaar-2)
</excerpt>
### Rank 4 of 14 — 0.62
<excerpt title="Nest site choice by the intertidal spider Desis formidabilis (Araneae">
# Nest site choice by the intertidal spider Desis formidabilis (Araneae: Desidae) and nest utilisation by its hymenopteran egg parasitoid - White Rose Research Online
Toggle navigationWhite Rose Research Online
*   Home  
*   Search  
*   Browse  
*   Contact

# Nest site choice by the intertidal spider Desis formidabilis (Araneae: Desidae) and nest utilisation by its hymenopteran egg parasitoid
Owen, CA, van Noort, S, Compton, SGorcid.org/0000-0002-1247-8058 et al. (1 more author) (2019) _Nest site choice by the intertidal spider Desis formidabilis (Araneae: Desidae) and nest utilisation by its hymenopteran egg parasitoid._ Ecological Entomology, 44 (1). pp. 62-70. ISSN: 0307-6946

# Nest site choice by the intertidal spider Desis formidabilis (Araneae: Desidae) and nest utilisation by its hymenopteran egg parasitoid
## Abstract
1. Echthrodesis lamorali Masner, 1968 is the only known parasitoid of the eggs of the intertidal rocky shore spider Desis formidabilis O.P. Cambridge 1890 and is endemic to a small area of South Africa.

2. The abundance of spider nests and parasitoid presence were assessed in relation to their in- and between-shore location at multiple sites within the distribution of E. lamorali along the Cape Peninsula (Western Cape, South Africa).

3. Desis formidabilis nests were more abundant in the mid-shore zone than higher up or lower down the shore. Spider population sizes also differed between collection sites, with higher numbers recorded on the cooler western coast of the peninsula.

4. Evidence of parasitoid activity was recorded in 43.31% of the 127 nests and 13.85% of the 592 egg sacs they contained. 5. Where parasitoids gained entry to a spider egg sac, oviposition took place into all of the eggs present.

6. Incidence of wasp activity was positively correlated with spider nest concentration, not with height up the shore, suggesting that both the host and parasitoid are tolerant of salt-water inundation.

7. These results should assist managers of the Table Mountain National Park, in which the full distribution of E. lamorali falls, to better understand this component of rocky shore community dynamics.
</excerpt>
### Rank 5 of 14 — 0.58
<excerpt title="Nest site choice by the intertidal spider Desis formidabilis (Araneae">
# Nest site choice by the intertidal spider Desis formidabilis (Araneae: Desidae) and nest utilisation by its hymenopteran egg parasitoid
## Abstract
1. Echthrodesis lamorali Masner, 1968 is the only known parasitoid of the eggs of the intertidal rocky shore spider Desis formidabilis O.P. Cambridge 1890 and is endemic to a small area of South Africa.

2. The abundance of spider nests and parasitoid presence were assessed in relation to their in- and between-shore location at multiple sites within the distribution of E. lamorali along the Cape Peninsula (Western Cape, South Africa).

3. Desis formidabilis nests were more abundant in the mid-shore zone than higher up or lower down the shore. Spider population sizes also differed between collection sites, with higher numbers recorded on the cooler western coast of the peninsula.

4. Evidence of parasitoid activity was recorded in 43.31% of the 127 nests and 13.85% of the 592 egg sacs they contained. 5. Where parasitoids gained entry to a spider egg sac, oviposition took place into all of the eggs present.

6. Incidence of wasp activity was positively correlated with spider nest concentration, not with height up the shore, suggesting that both the host and parasitoid are tolerant of salt-water inundation.

7. These results should assist managers of the Table Mountain National Park, in which the full distribution of E. lamorali falls, to better understand this component of rocky shore community dynamics.

# Nest site choice by the intertidal spider Desis formidabilis (Araneae: Desidae) and nest utilisation by its hymenopteran egg parasitoid
## Metadata
| Item Type: | Article |  
| ---: |  
| Authors/Creators: | * Owen, CA * van Noort, S * Compton, SGhttps://orcid.org/0000-0002-1247-8058 * Coetzee, JA |  
| Copyright, Publisher and Additional Information: | (c) 2018, The Royal Entomological Society. This is the peer reviewed version of the following article: 'Owen, CA, van Noort, S, Compton, SG, and Coetzee, JA (2018). Nest site choice by the intertidal spider Desis formidabilis (Araneae: Desidae) and nest utilisation by its hymenopteran egg parasitoid. Ecological Entomology,' which has been published in final form at [https://doi.org/10.1111/een.12675]. This article may be used for non-commercial purposes in accordance with Wiley Terms and Conditions for Self-Archiving. |  
| Keywords: | Density dependence, Echthrodesis lamorali, Platygastridae, Scelioninae, Rocky shore, Zonation |  
| Dates: | * Accepted: 8 August 2018 * Published (online): 12 September 2018 * Published: 3 January 2019 |  
| Institution: | The University of Leeds |  
| Academic Units: | The University of Leeds>Faculty of Biological Sciences (Leeds)>School of Biology (Leeds) |  
| Date Deposited: | 04 Dec 2018 12:57 |  
| Last Modified: | 12 Sep 2019 00:39 |  
| Status: | Published |  
| Publisher: | Wiley |  
| Identification Number: | 10.1111/een.12675 |  
| Open Archives Initiative ID (OAI ID): | oai:eprints.whiterose.ac.uk:139051 |
</excerpt>

## Search 7 — query: "Desis crosslandi distribution"
### Rank 1 of 48 — 0.00 (passed on)
<excerpt title="Contact Us">
Skip to main content
Home
Join Our Email List
Donate Now
Contact Us

## Send Us Questions About Our Empowerment Programs
Please use the form below to contact our team.

## Send Us a Message
Full Name  (required)
Email Address  (required)
Phone Number
Message  (required)

## Our Locations
### East Los Angeles — Client Resource Center
646 S. Atlantic Blvd., Los Angeles, CA 90022
[(323) 780-1920](tel:3237801920)
[info@desisocal.org](mailto:info@desisocal.org)

## Our Locations
### South East LA Office
2677 Zoe Avenue, Suite 109C, Huntington Park, CA 90255
[(323) 780-1920](tel:3237801920)

## Our Locations
### The DESI Shop — A Community Discount Store
6525 Whittier Blvd., Los Angeles, CA 90022
[(213) 671-8414](tel:2136718414)
</excerpt>
### Rank 2 of 48 — 0.00
<excerpt title="Desi Brothers Farmers Market Plans Maple Grove Store">
# Desi Brothers Farmers Market Plans Maple Grove Store - YouTube
## Desi Brothers Farmers Market Plans Maple Grove Store
Playlist | 미리 듣기만 해도 설레는 크리스마스 재즈🎅 | Christmas Jazz Playlist JazzNe 1.6K watching • 2w ago Live Playlist ()Mix (50+)11:46 Trump Gets Weird in Asia, Everything is Broken in America & Measles are Making a Comeback!Jimmy Kimmel Live 1.5M • 5h ago Live Playlist ()Mix (50+)5:26 리트 만점자에 변호사들 작심 비판 "말과 글에서 영특함 못 봤다"뉴스1TV 3.6K • 47 min ago Live Playlist ()Mix (50+)39:26 1억 4천만 원에 퀄리티가 말도 안 된다. 번역기 돌려가며 주문했더니 배타고 와서 설치까지 뚝딱｜해외직구로 구매한 2층 패시브 하우스｜건축탐구 집｜#골라듄다큐 EBSDocumentary (EBS 다큐)1.7M • 8d ago Live Playlist ()Mix (50+)6:27 Come to think of it, Elon Musk’s current situation is about more than just a $475 million loss | ...크랩 KLAB 63K • 2h ago Live Playlist ()Mix (50+)45:38 The fairies have arrived. Laurel. | EP. 164 Jang Na-ra, Kim Hye-yoon | Salon Drip TEO 테오 1.1M • 1d ago Live Playlist ()Mix (50+)[14:20 초조한 리트 만점자 이진우 근황? "목요일에 다 말하겠다" [사건영수증] YTN 30K • 1h ago Live Playlist ()Mix (50+)](https://www.youtube.com/watch?v=lfVJzUzx2wE)9:50 "연락해도 답이 없어" 라이브 켠다더니…수능 전날 행방묘연 #뉴스다 / JTBC News JTBC News 1.5M • 8h ago Live Playlist ()Mix (50+)[33:41 Singing live undercover pretending to be a track (ft.

# Desi Brothers Farmers Market Plans Maple Grove Store - YouTube
## Desi Brothers Farmers Market Plans Maple Grove Store
GUMMY) | [Background Live]제이키아웃 JAYKEEOUT 15K • 2h ago Live Playlist ()Mix (50+)](https://www.youtube.com/watch?v=vqWMftZ4zJ4)[33:18 [Playlist] 위안의 음악을 듣는 시간, 류이치 사카모토 책바 Chaegbar 3.4M • 3y ago Live Playlist ()Mix (50+)](https://www.youtube.com/watch?v=F7Ni1nMMm5I)3:33 5-year-old with autism finds support community at neighborhood grocery store Land of 10,000 Stories: The Complete Collection 7.9K • 10mo ago Live Playlist ()Mix (50+)36:10 "유행도 숙제가 됐다." 억지 유행에 지친 한국인들 근황ㅣ지식인 클래스 EP.38 (김난도 교수)지식인사이드 1.5M • 1d ago Live Playlist ()Mix (50+)

# Desi Brothers Farmers Market Plans Maple Grove Store
CCX Media Community News
CCX Media Community News
9.32K subscribers
Subscribe
Subscribed
4
Download
1.3K views 5y ago
1,381 views • Jun 17, 2021
A new grocery store is planned for Maple Grove, a type the city currently does not have. Texas-based Desi Brothers Farmers Market is planning a store for a vacant lot northeast of County Road 30 and Garland Lane. It would be located between the AutoZone and Walgreens stores. Desi Brothers specializes in Indian and Middle Eastern foods and ingredients.…more
more
Transcript
Follow along using the transcript.
Show transcript

# Desi Brothers Farmers Market Plans Maple Grove Store
### CCX Media Community News 9.32K subscribers
VideosAbout Facebook Twitter News Twitter Sports Instagram
</excerpt>
### Rank 3 of 48 — 0.00
<excerpt title="Desi Brothers Farmers Market Plans Maple Grove Store">
# Desi Brothers Farmers Market Plans Maple Grove Store
### CCX Media Community News 9.32K subscribers
VideosAbout Facebook Twitter News Twitter Sports Instagram

# Desi Brothers Farmers Market Plans Maple Grove Store
## Video details
Date
Jun 17, 2021
Views
1,381
Likes
4
Show less

# Desi Brothers Farmers Market Plans Maple Grove Store
1,381 views 1.3K views
Jun 17, 2021
4
Download

# Desi Brothers Farmers Market Plans Maple Grove Store
## 0 Comments
Sort comments
Sort by
Top Show featured commentsNewest Show recent comments, including potential spam
Add a comment...

# Desi Brothers Farmers Market Plans Maple Grove Store
## Comments
Top Show featured commentsNewest Show recent comments, including potential spam

# Desi Brothers Farmers Market Plans Maple Grove Store
## In this video
Transcript

# Desi Brothers Farmers Market Plans Maple Grove Store
## Desi Brothers Farmers Market Plans Maple Grove Store
CCX Media Community News
CCX Media Community News
4 Likes
1.3K Views
2021 Jun 17
A new grocery store is planned for Maple Grove, a type the city currently does not have. Texas-based Desi Brothers Farmers Market is planning a store for a vacant lot northeast of County Road 30 and Garland Lane. It would be located between the AutoZone and Walgreens stores. Desi Brothers specializes in Indian and Middle Eastern foods and ingredients. http://www.ccxmedia.org/ccxsports/ccxnews/ccxmedia.org CCX Media is on Comcast Xfinity in the Northwest Suburbs of Minneapolis and includes the cities Brooklyn Center, Brooklyn Park, Crystal, Golden Valley, Maple Grove, New Hope, Osseo, Plymouth and Robbinsdale.…...more
...more Show less
Transcript
Follow along using the transcript.
Show transcript

# Desi Brothers Farmers Market Plans Maple Grove Store
## Desi Brothers Farmers Market Plans Maple Grove Store
### CCX Media Community News 9.32K subscribers
VideosAbout Facebook Twitter News Twitter Sports Instagram

# Desi Brothers Farmers Market Plans Maple Grove Store
## Video details
Date
Jun 17, 2021
Views
1,381
Likes
4

# Desi Brothers Farmers Market Plans Maple Grove Store
## Transcript
NaN / NaN
LIVE

# Desi Brothers Farmers Market Plans Maple Grove Store
## Transcript
### Playlist | 미리 듣기만 해도 설레는 크리스마스 재즈🎅 | Christmas Jazz Playlist
JazzNe
1.6K watching
11:46 New

# Desi Brothers Farmers Market Plans Maple Grove Store
## Transcript
### Trump Gets Weird in Asia, Everything is Broken in America & Measles are Making a Comeback!
Jimmy Kimmel Live
1.5M 5h ago
5:26 New

# Desi Brothers Farmers Market Plans Maple Grove Store
## Transcript
### 리트 만점자에 변호사들 작심 비판 "말과 글에서 영특함 못 봤다"
뉴스1TV
3.6K 47 min ago
39:26

# Desi Brothers Farmers Market Plans Maple Grove Store
## Transcript
### 1억 4천만 원에 퀄리티가 말도 안 된다. 번역기 돌려가며 주문했더니 배타고 와서 설치까지 뚝딱｜해외직구로 구매한 2층 패시브 하우스｜건축탐구 집｜#골라듄다큐
EBSDocumentary (EBS 다큐)
1.7M 8d ago
6:27 New

# Desi Brothers Farmers Market Plans Maple Grove Store
## Transcript
### Come to think of it, Elon Musk’s current situation is about more than just a $475 million loss | ...
크랩 KLAB
63K 2h ago
45:38 New

# Desi Brothers Farmers Market Plans Maple Grove Store
## Transcript
### The fairies have arrived. Laurel. | EP. 164 Jang Na-ra, Kim Hye-yoon | Salon Drip
TEO 테오
1.1M 1d ago
Auto-dubbed
14:20 New
</excerpt>
### Rank 4 of 48 — 0.00
<excerpt title="DESI Databases - DESI Data">
DESI has developed a PostgreSQL database of catalog-level quantities available with Data Release 1 (DR1) as well as the Early Data Release (EDR). Access information for NERSC and NOIRLab’s Astro Data Lab is provided below.
Note
Currently, these databases do not grant access to the actual DESI spectra nor to the majority of the Value Added Catalogs (VACs) described in the DR1 paper.

## NOIRLab’s Astro Data Lab¶
The Astro Data Lab hosts a copy of the DESI DR1 database tables, which is accessible either anonymously via a Web Query Interface or using authenticated services such as a JupyterLab platform. In addition, the DESI EDR database tables are available.
For more information please see the Astro Data Lab page describing DESI data access.

## NERSC¶
A copy of the database is hosted at NERSC and is accessible to anyone with a NERSC account. To get started, add the access credentials to your `~/.pgpass` file in your NERSC `$HOME` directory:
```  
cat /global/common/software/desi/desi_public.pgpass >> ~/.pgpass  
chmod 600 ~/.pgpass  
```
You only need to do this once.   
Once that is set up, connect with `psql` from the command line:
```  
psql -U desi_public -h specprod-db.desi.lbl.gov -d desi  
```
or from Python using the psycopg2 library:
```  
import psycopg2  
conn = psycopg2.connect(host="specprod-db.desi.lbl.gov",  
                        database="desi", user="desi_public")  
```
This database uses the default PostgreSQL port, 5432, so it is not necessary to specify the port.
The DR1 database tables, described below, are all contained in the `iron` schema. In the examples below, note that table names are schema-qualified, _i.e._, `iron.target` rather than `target`.
The EDR data are contained in the `fuji` schema, which has minor differences from `iron` which are noted in the “Changes” sections below.
Finally note that the `guadalupe` spectroscopic production is also available.
For more information, a Jupyter notebook tutorial about using the database is available at the DESI GitHub tutorial repository.
Warning
The NERSC copy of the database is _only_ accessible inside the NERSC network. You must access this database via a NERSC node, _e.g._ a perlmutter login node.
If you do not have a NERSC account, we recommend using NOIRLab’s Astro Data Lab service described below.

## Schema Names¶
As described above, several different schema are available. This table gives the schema name equivalents at NERSC and NOIRLab’s Astro Data Lab.
| NERSC Schema | NOIRLab Schema | Description |  
| --- | --- | --- |  
| `fuji` | `desi_edr` | Database schema for DESI EDR catalog data |  
| `guadalupe` | Not available | Database schema for the first 20% of Year 1 catalog data (DR1 supplement) |  
| `iron` | `desi_dr1` | Database schema for DESI DR1 catalog data |

## Matching Redshift Tables to Targeting Data¶
Matching redshift results back to targeting is an important task for many DESI science projects. Below we briefly describe the fundamentals of this matching using the database.
</excerpt>
### Rank 5 of 48 — 0.00
<excerpt title="DESI Databases - DESI Data">
## Matching Redshift Tables to Targeting Data¶
Matching redshift results back to targeting is an important task for many DESI science projects. Below we briefly describe the fundamentals of this matching using the database.

## Matching Redshift Tables to Targeting Data¶
### Tile-based¶
The `ztile` table contains a foreign key pointing to the primary key of the `target` table. This means that for any row of `ztile`, there is a pre-matched entry in the `target` table, and it can be accessed with a simple join, such as:
```  
SELECT z.targetid, z.spgrp, z.spgrpval, z.tileid, z.z, z.zwarn, z.spectype,  
    t.desi_target, t.bgs_target, t.mws_target, t.scnd_target,  
    p.ra, p.dec  
FROM iron.ztile AS z  
JOIN iron.target AS t ON z.targetphotid = t.id  
JOIN iron.photometry AS p ON z.targetid = p.targetid  
LIMIT 50;  
```
Note the `z.targetphotid = t.id`. This query also demonstrates a `JOIN` with the `photometry` table, where `targetid` is unique.

## Matching Redshift Tables to Targeting Data¶
### HEALPixel-based¶
The redshift results from HEALPixel-based coadds in the `zpix` table may be made up of several tiles, so it is not as simple to match these with targeting data. In the majority of cases, the targeting information is the same for a `targetid` across multiple tiles, as long as the tiles are part of the same `survey` (_e.g._`main`). However it is not _always_ the case, so we have instead collected the best values of the targeting information and placed those values directly in the `zpix` table. Here is the analogous query to the query above:
```  
SELECT z.targetid, z.survey, z.program, z.healpix, z.z, z.zwarn, z.spectype,  
    z.desi_target, z.bgs_target, z.mws_target, z.scnd_target,  
    p.ra, p.dec  
FROM iron.zpix AS z  
JOIN iron.photometry AS p ON z.targetid = p.targetid  
LIMIT 50;  
```

## Full Description of Database Tables¶
The following catalog tables are available:
| Name | Description |  
| --- | --- |  
| exposure | Summary quantities for every DESI exposure. |  
| fiberassign | Quantities obtained when a DESI target is assigned to a fiber. |  
| frame | Summary quantities for each petal of the DESI instrument in a given exposure; in normal operation there are ten frames for every exposure. |  
| photometry | Photometric quantities from Legacy Surveys DR9 for every TARGETID. |  
| potential | For a given tile, this table lists all targets that could have received a fiber assignment. |  
| target | The quantities obtained when photometric objects are analyzed in the target selection process. |  
| tile | Summary quantities for every DESI tile (pointing on the sky). |  
| zpix | Redshift and other quantities for spectra that have been grouped and coadded by HEALPixel. |  
| ztile | Redshift and other quantities for spectra that have been grouped and coadded by tile. |
</excerpt>

## Search 8 — query: "Desis galapagoensis distribution"
### Rank 1 of 141 — 0.78 (passed on)
<excerpt title="Desis galapagoensis">
# Desis galapagoensis - Wikipedia
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

# Desis galapagoensis - Wikipedia
## Contents
move to sidebar hide
*   (Top)  
*   1 References
- [x] Toggle the table of contents

# _Desis galapagoensis_
- [x] 6 languages
*   Cebuano  
*   Français  
*   Nederlands  
*   Svenska  
*   Tiếng Việt  
*   Winaray
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
Species of spider
| _Desis galapagoensis_ |  
| --- |  
| Scientific classification |  
| Kingdom: | Animalia |  
| Phylum: | Arthropoda |  
| Subphylum: | Chelicerata |  
| Class: | Arachnida |  
| Order: | Araneae |  
| Infraorder: | Araneomorphae |  
| Family: | Desidae |  
| Genus: | _Desis_ |  
| Species: | _**D.galapagoensis**_ |  
| Binomial name |  
| **_Desis galapagoensis_** Hirst, 1925 |

# _Desis galapagoensis_
_**Desis galapagoensis**_ is a species of spider in the genus _Desis_, and the family Desidae.[[1]](https://en.wikipedia.org/wiki/Desis_galapagoensis#cite_note-1)[[2]](https://en.wikipedia.org/wiki/Desis_galapagoensis#cite_note-2) The species is found on Floreana Island.[[3]](https://en.wikipedia.org/wiki/Desis_galapagoensis#cite_note-3)
</excerpt>
### Rank 2 of 141 — 0.77
<excerpt title="Desis galapagoensis">
# _Desis galapagoensis_
_**Desis galapagoensis**_ is a species of spider in the genus _Desis_, and the family Desidae.[[1]](https://en.wikipedia.org/wiki/Desis_galapagoensis#cite_note-1)[[2]](https://en.wikipedia.org/wiki/Desis_galapagoensis#cite_note-2) The species is found on Floreana Island.[[3]](https://en.wikipedia.org/wiki/Desis_galapagoensis#cite_note-3)

# _Desis galapagoensis_
## References
[edit]
1.   ↑"NMBE - World Spider Catalog". _wsc.nmbe.ch_. Natural History Museum Bern. Retrieved 2024-10-10.  
2.   ↑DeGrave, Sammy (2023). "_Desis galapagoenis_ Hirst, 1925". _WoRMS_. World Register of Marine Species.  
3.   ↑"Galapagos Species Database". _CDF dataZone_. Retrieved 2024-10-10.
| Taxon identifiers |  
| --- |  
| _Desis galapagoensis_ | * Wikidata: Q1810919 * ADW: Desis_galapagoensis * BioLib: 1025577 * CoL: 34ZNW * EoL: 1200353 * GBIF (old): 2143013 * iNaturalist: 818274 * IRMNG: 10436680 * ITIS: 878102 * Open Tree of Life: 3560091 * WoRMS: 509856 * WSC: urn:lsid:nmbe.ch:spidersp:021482 |
This article related to Desidae spiders is a stub. You can help Wikipedia by adding missing information.
*   v  
*   t  
*   e
Retrieved from "https://en.wikipedia.org/w/index.php?title=Desis_galapagoensis&oldid=1275916210"
Categories:
*   Spiders described in 1925  
*   Desidae  
*   Spiders of South America  
*   Galápagos Islands coastal fauna  
*   Desidae stubs
Hidden categories:

# _Desis galapagoensis_
## References
*   Articles with short description  
*   Short description is different from Wikidata  
*   Articles with 'species' microformats  
*   All stub articles

*    This page was last edited on 15 February 2025, at 21:07(UTC).  
*   Page was rendered with Parsoid.  
*   Text is available under the Creative Commons Attribution-ShareAlike 4.0 License; additional terms may apply. By using this site, you agree to the Terms of Use and Privacy Policy. Wikipedia® is a registered trademark of the Wikimedia Foundation, Inc., a non-profit organization.

*   Privacy policy  
*   About Wikipedia  
*   Disclaimers  
*   Contact Wikipedia  
*   Legal & safety contacts  
*   Code of Conduct  
*   Developers  
*   Statistics  
*   Cookie statement  
*   Mobile view  
*   Edit preview settings

*     
*
Search
Search
- [x] Toggle the table of contents
_Desis galapagoensis_
6 languagesAdd topic
</excerpt>
### Rank 3 of 141 — 0.75
<excerpt title="Desis galapagoensis - dataZone - Charles Darwin Foundation">
The Galapagos Species Database shares the information about the species from our Natural History Collections.

## _Desis galapagoensis_
arácnidos, Arachnids
*   Taxonomy  
*   Distribution  
*   References
In the tide zone.
Domain
Eukaryota
Kingdom
Animalia
Phylum
Arthropoda
Class
Arachnida
Order
Araneae
Family
Desidae
Genus
Desis
Species
galapagoensis
Taxon category: Accepted
Origin: Endemic
Map of specimen collection localities or observation records for this species in our collections database.
Distribution: Distribution: Only known from Galápagos. Galápagos distribution: Floreana.
*    Baert, L. Jean-Pierre Maelfait, Konjev Desender, Frederik Hendrickx (2023) Updated checklist, origin, distribution, literature and genital drawings of the spiders of the Galápagos Islands _Belgian Journal of Entomology 142: 1–188._  
*    Baert, L.L. Maelfait, J.-P. (2000) Check List of the Described Spider Species of the Galápagos Archipelago (Araneae). _Bull. Inst. R. Sci. Nat. Belg. Entomol. 70: 243-245._  
*    Baert, L.L. Malfait, J.-P., Hendrickx, F. & Desender, K. (2008) Distribution and Habitat Preference of the Spiders (Araneae) of Galápagos. _Bull. Inst. R. Sci. Nat. Belg. Entomol. 78: 39-111._  
*    Buchholz, S. Baert, L., Rodríguez, J., E Causton, C., & Jäger, H. (2020) Spiders in Galapagos–diversity, biogeography and origin. _Biological Journal of the Linnean Society, 130(1), 41-48._  
*    Hirst, S. (1925) On a new marine spider (Desis galapagoensis, sp. n.) from the Galapagos Islands. _Annals and Magazine of Natural History, 9th ser. 16: 271._  

## _Desis galapagoensis_
*    Horton, T. Horton, T., Kroh, A., Ahyong, S., Bailly, N., Boyko, C. B., Brandão, S. N., Gofas, S., Hooper, J. N. A., Hernandez, F., Holovachov, O., Mees, J., Molodtsova, T. N., Paulay, G., Decock, W., Dekeyzer, S., Poffyn, G., Vandepitte, L., Vanhoorne, B., Adlard, R., ... Zhao, Z. (2021) World Register of Marine Species. _Available from https://www.marinespecies.org at VLIZ._  
*    Roth, V.D. Craig, P.R. (1970) Arachnida of the Galápagos Islands (Excluding Acarina). _Mission zoologique belge aux îles Galapagos et en Ecuador (N. et J. Leleup, 1964-1965), 2: 107-124._

## _Desis galapagoensis_
### You are welcome to download and use the information found in this page, acknowledging its source.
This page should be cited as follows:
> "Galapagos Species Database, _Desis galapagoensis_", dataZone. Charles Darwin Foundation, https://datazone.darwinfoundation.org/en/checklist/?species=11907. Accessed 18 November 2026.
</excerpt>
### Rank 4 of 141 — 0.68
<excerpt title="Distribution and habitat preference of the spiders (Araneae) of Galapagos">
## [PDF page 11]
Distribution:  Cosmopolite distribution.  A!titudinal range:  IBC  (2- 225  m);  IVA  (at 600 m  alt.)  ;  
DAP,  FLO,  GAE, ISN,  IVW,  PIN,  RAB,  SCB ,  SCZ,  
Creugas bellator (L. KOCH,  1866)  SFE (on all these islands: 2-20 m).
Distribution  in  the  Archipelago  (Map  23):  FLO(l), Ecological  range  : Typical  for  sal t  marshes  or habitats  
ICA(J)  ,  IVW(l), SAN(l), SCZ(7).  near the sea.
Attitudinal  range:  FLO  (at 400  m),  ICA  (at 400 m),  Distribution: Only known from Galapagos.  
IVW  (at 750  m) ,  SAN  (at 580 m) ,  SCZ (at  2  m  and  
between  570-  875  m).  Tivyna spatula (GERTSCH  &  D  Av1s,  193  7)

## [PDF page 11]
Eco  logical  range  :  It  is  found  in  humid  forests  and Distribution  in  the  Archipe lago  (Map  27):  BAL,  
highland  Pampa  vegetation  on  F  loreana,  Cerro  Azul  ESP(l),  FER(8),  IBC(l  ),  ICA(  l  ), ISN(3) , IVA(lO),  
and Vol  ca  n Wolf.  On Santa Cruz  it was most abundant  IVD(l),  IVW(2),  MAR(3),  PIZ(l),  RAB(l),  SAN(5),  
in  the  Scalesia forest and the Fem-s  edge zone, but was  SCB(l ),  SCZ(l2), SEY(l).  
a lso encountered in  the Littoral zone.  
Altitudinal  range:  FER (5-200  &  1300-13  60 m);  ISN  
D  istribution :  Known  from  Venezuela,  Colombia  and  (2-5  &  at 600 m); IVA (from coast to sununi  t); SCZ (up  
Ecuador.  to 250 m); BAL, ESP, IBC, ICA, IVD, IVW, MAR, PIZ,  
RAB , SAN, SCB,  SEY (2-30 m).
DESIDAE  Ecological range:  It is  most  abundant  in  the  Littoral  
and  lower  Arid  zone  along  the  coast.  On  Santa  Cruz  
Desis galapagoensis HrRST ,  1925  it  climbs  up  to 250 m  along  the  no11hem  side.  It  is  
a  lso  found  in the  summit Arid zone  of Femandin a  and  
Distribution  in  the Archipelago  (Map 24): FLO .  Vo lean A  lcedo.
</excerpt>
### Rank 5 of 141 — 0.61
<excerpt title="Distribution and habitat preference of the spiders (Araneae) of Galapagos">
## [PDF page 11]
Eco  logical  range  :  It  is  found  in  humid  forests  and Distribution  in  the  Archipe lago  (Map  27):  BAL,  
highland  Pampa  vegetation  on  F  loreana,  Cerro  Azul  ESP(l),  FER(8),  IBC(l  ),  ICA(  l  ), ISN(3) , IVA(lO),  
and Vol  ca  n Wolf.  On Santa Cruz  it was most abundant  IVD(l),  IVW(2),  MAR(3),  PIZ(l),  RAB(l),  SAN(5),  
in  the  Scalesia forest and the Fem-s  edge zone, but was  SCB(l ),  SCZ(l2), SEY(l).  
a lso encountered in  the Littoral zone.  
Altitudinal  range:  FER (5-200  &  1300-13  60 m);  ISN  
D  istribution :  Known  from  Venezuela,  Colombia  and  (2-5  &  at 600 m); IVA (from coast to sununi  t); SCZ (up  
Ecuador.  to 250 m); BAL, ESP, IBC, ICA, IVD, IVW, MAR, PIZ,  
RAB , SAN, SCB,  SEY (2-30 m).
DESIDAE  Ecological range:  It is  most  abundant  in  the  Littoral  
and  lower  Arid  zone  along  the  coast.  On  Santa  Cruz  
Desis galapagoensis HrRST ,  1925  it  climbs  up  to 250 m  along  the  no11hem  side.  It  is  
a  lso  found  in the  summit Arid zone  of Femandin a  and  
Distribution  in  the Archipelago  (Map 24): FLO .  Vo lean A  lcedo.

## [PDF page 12]
50  Leon BAERT, Jean-Pierre MAELFAIT, Frederik HENDRICKX &  Konjev D  ESENDER
Distribution:  Known from the USA, Mexico, Cuba and  sedge z one.  
the B  a  h arna Islands  .  
Distribution  : Only  known from Gal a pag o  s  .  
Dictyna sp .1  
Camillina galapagoensis (B ANKS,  1902)  
Distribution in the Archipelago (Map 28)  : IVD(l).  
Distribution  in  the  A  rc  hipe lago  (Map  31):  BAL(  l  ),  
A  ltitudinal range: At an altitude of 100 m  .  FER(lO),  F  L0(2),  IBC(l),  ICA(2),  ISN( 5),  IVA(7),  
IVD(7),  IVW(8),  MAR(4) , PIN(13),  PIZ(2),  SAN (3) ,  
Ecological range:  Coastal Arid zone.  SCB (5), SCZ(24),  SFE(2), SPL(l )  .
</excerpt>

## Search 9 — query: "Desis vorax distribution"
### Rank 1 of 69 — 0.84 (passed on)
<excerpt title="[Arachnida • 2017] Desis bobmarleyi • A New Spider (Araneae, Desidae) ...">
Species New to Science
new & recent described Flora & Fauna species from all over the World esp. Asia, Oriental, Indomalayan & Malesiana region
Friday, December 29, 2017  
[Arachnida • 2017] Desis bobmarleyi • A New Spider (Araneae, Desidae) from Coral Reefs in Australia’s Sunshine State and its Relative from Sāmoa
Desis bobmarleyi
Baehr, Raven & Harms, 2017
DOI: 10.3897/evolsyst.1.15735
Abstract  
Spiders of the genus Desis Walckenaer, 1837 (Araneae: Desidae) are water-adapted spiders and live in the intertidal zone on reefs, marine debris and under rocks. Here, we describe a new intertidal species from tropical Queensland and name it after Bob Marley, whose song “High Tide or Low Tide” inspired us as it lives in a “high tide low tide” habitat. We also re-describe a close morphological relative, Desis vorax L. Koch, 1872 from Sāmoa. This species was described some 150 years ago from the Godeffroy Collection which holds the oldest major collection of Australasian and Pacific spiders, now mainly hosted in the Centre of Natural History in Hamburg (CeNak). A third species, Desis hartmeyeri Simon, 1909, was described from juvenile specimens only and is considered a nomen dubium.
“None but ourselves can free our minds.” Bob Marley, Redemption Song (1980).
Key Words: Taxonomy, systematics, new species, Bob Marley, intertidal, spiders, Australia, Pacific
Figure 1. Life image of Desis bobmarleyi sp. n. female allotype
(Photo: R. Raven).
Desis bobmarleyi male holotype
(photo: R. Raven)
Systematics  
Family DESIDAE Pocock, 1895  
Subfamily Desinae Pocock, 1895
Desis Walckenaer, 1837
Desis bobmarleyi sp. n.
</excerpt>
### Rank 2 of 69 — 0.81
<excerpt title="Desis (spider)">
From Wikipedia, the free encyclopedia
| _Desis_ |  
| --- |  
|  |  
| female _Desis japonica_ |  
|  |  
| _D. formidabilis_ |  
| Scientific classification |  
| Kingdom: | Animalia |  
| Phylum: | Arthropoda |  
| Subphylum: | Chelicerata |  
| Class: | Arachnida |  
| Order: | Araneae |  
| Infraorder: | Araneomorphae |  
| Family: | Desidae |  
| Genus: | _Desis_ Walckenaer, 1837[[1]](https://en.wikipedia.org/wiki/Desis_(spider)#cite_note-wsc-1) |  
| Type species |  
| _D. maxillosa_ (Fabricius, 1793) |  
| Species |  
| 15, see text |
_**Desis**_ is a genus of intertidal spiders that was first described by Charles Athanase Walckenaer in 1837.[[2]](https://en.wikipedia.org/wiki/Desis_(spider)#cite_note-Walc1837-2) Species of the genus are found in Australasia, the Pacific, Japan, eastern and southern Africa, and India. They are marine spiders, living in the intertidal zone and only emerging at the ebb tide to hunt for invertebrates including shrimp. When submerged during high tides, they stay in an air chamber sealed with silk,[[3]](https://en.wikipedia.org/wiki/Desis_(spider)#cite_note-arach-3)[[4]](https://en.wikipedia.org/wiki/Desis_(spider)#cite_note-BaehRaveHarm17-4)[[5]](https://en.wikipedia.org/wiki/Desis_(spider)#cite_note-nyffeler-5) and breathe its air.[[6]](https://en.wikipedia.org/wiki/Desis_(spider)#cite_note-myst-6)
As of October 2025, this genus includes fifteen species:[[1]](https://en.wikipedia.org/wiki/Desis_(spider)#cite_note-wsc-1)

*   _Desis bobmarleyi_ Baehr, Raven& Harms, 2017 – Australia (Queensland)  
*   _Desis crosslandi_Pocock, 1903 – Tanzania (Zanzibar), Madagascar, Comoros, Mayotte  
*   _Desis formidabilis_(O. Pickard-Cambridge, 1891) – Namibia, South Africa  
*   _Desis galapagoensis_ Hirst, 1925 – Galapagos  
*   _Desis gardineri_ Pocock, 1904 – India (Laccadive Is.)  
*   _Desis inermis_ Gravely, 1927 – India  
*   _Desis japonica_ Yaginuma, 1956 – Japan  
*   _Desis jiaxiangi_ Lin, Li & Chen, 2020 – China  
*   _Desis kenyonae_ Pocock, 1902 – Australia (Victoria, Tasmania)  
*   _Desis marina_(Hector, 1878) – New Caledonia, New Zealand (mainland, Chatham Is.)  
*   _Desis martensi_L. Koch, 1872 – Singapore, Indonesia (Java)  
*   _Desis maxillosa_(Fabricius, 1793) – New Guinea, New Caledonia (type species)  
*   _Desis risbeci_Berland, 1931 – New Caledonia  
*   _Desis tangana_Roewer, 1955 – East Africa  
*   _Desis vorax_ L. Koch, 1872 – Samoa
</excerpt>
### Rank 3 of 69 — 0.79
<excerpt title="Desis (spider)">
*   _Desis bobmarleyi_ Baehr, Raven& Harms, 2017 – Australia (Queensland)  
*   _Desis crosslandi_Pocock, 1903 – Tanzania (Zanzibar), Madagascar, Comoros, Mayotte  
*   _Desis formidabilis_(O. Pickard-Cambridge, 1891) – Namibia, South Africa  
*   _Desis galapagoensis_ Hirst, 1925 – Galapagos  
*   _Desis gardineri_ Pocock, 1904 – India (Laccadive Is.)  
*   _Desis inermis_ Gravely, 1927 – India  
*   _Desis japonica_ Yaginuma, 1956 – Japan  
*   _Desis jiaxiangi_ Lin, Li & Chen, 2020 – China  
*   _Desis kenyonae_ Pocock, 1902 – Australia (Victoria, Tasmania)  
*   _Desis marina_(Hector, 1878) – New Caledonia, New Zealand (mainland, Chatham Is.)  
*   _Desis martensi_L. Koch, 1872 – Singapore, Indonesia (Java)  
*   _Desis maxillosa_(Fabricius, 1793) – New Guinea, New Caledonia (type species)  
*   _Desis risbeci_Berland, 1931 – New Caledonia  
*   _Desis tangana_Roewer, 1955 – East Africa  
*   _Desis vorax_ L. Koch, 1872 – Samoa

1.   Jump up to: 12"Genus Desis". World Spider Catalog. doi:10.24436/2. Retrieved 2025-10-02.  
2.   ↑Walckenaer, C. A. (1837). _Histoire naturelle des insectes. Aptères_.  
3.   ↑"Desis sp. Marine Spiders". _www.arachne.org.au_. Retrieved 2016-01-18.  
4.   ↑Baehr, B.C.; Raven, R. & Harms, D. (2017). "'High Tide or Low Tide': _Desis bobmarleyi_ sp. n., a new spider from coral reefs in Australia's Sunshine State and its relative from Sāmoa (Araneae, Desidae, Desis)". _Evolutionary Systematics_. **1**: 111–120. doi:10.3897/evolsyst.1.15735.  
5.   ↑Nyffeler, M.; Pusey, B.J. (2014). "Fish Predation by Semi-Aquatic Spiders: A Global Pattern". _PLOS ONE_. **9** (6) e99459. Bibcode:2014PLoSO...999459N. doi:10.1371/journal.pone.0099459. PMC4062410. PMID24940885.  
6.   ↑"Mysterious Marine Spiders in Sydney Harbour". _The Australian Museum_. Retrieved 2023-11-25.
*   Citizen science observations for Desis at iNaturalist
</excerpt>
### Rank 4 of 69 — 0.78
<excerpt title="Desis bobmarleyi sp. n., a new spider from coral reefs in Australia's ...">
## Systematics
### Family DESIDAE Pocock, 1895
#### Subfamily Desinae Pocock, 1895
##### _Desis_ Walckenaer, 1837
###### Material examined.
JUVENILE FEMALE SYNTYPE (ZMH-A0000100), from Western Australia, Albany, 35°1’S, 117°53’E. 2 JUVENILE FEMALE SYNTYPES (ZMB), ONE JUVENILE SYNTYPE (WAM)

## Systematics
### Family DESIDAE Pocock, 1895
#### Subfamily Desinae Pocock, 1895
##### _Desis_ Walckenaer, 1837
###### Remarks.
The description of this species was based on juvenile specimens (Rack 1961; York Main and Harvey 1992) and the four juveniles are deposited at three museums: one in Hamburg, two in Berlin and one in Perth. Simon (1909) did not designate a holotype and all four specimens are treated here as syntypes. The identification of species in morphologically conserved groups of spiders, such as Desidae, inevitably requires adult specimens and _D. hartmeyeri_ cannot be reliably identified based on these specimens and may be synonymous with some of the other Australian species for which adult specimens are available. No additional information on this species – biological, distributional or taxonomic – is available that could elucidate its status. The collection locality is geographically distinct (all other records are from eastern Australia) but many _Desis_ species have wide ranges and the specific habitat is not strongly distinct from any such habitats in south-eastern Australia. The purpose of a species description is to facilitate species identification but this is not possible from the data available and the specific name adds to taxonomic redundancy in this group of spiders. This species is a _nomen dubium_.

## Systematics
### Family DESIDAE Pocock, 1895
#### Subfamily Desinae Pocock, 1895
##### _Desis_ Walckenaer, 1837
###### Taxon classification
Animalia
Araneae
Desidae
3C4FC80D-2634-52AF-93AF-63F4ACF6192B Desis vorax
L. Koch, 1872
1.   Download: Download high-res image (1MB)  
2.   Download: Download full-size image
Figure 6. _Desis vorax_ L. Koch, 1872, male holotype (ZSMH- A0000099): **A**, habitus, dorsal view; **B**, same, ventral view; **C**, prosoma, ventral view; **D**, male palp, retrolateral view; D, same, ventral view; **E**, same, prolateral view;. Scale bars: 1.0 mm.
169 Desis vorax L. Koch, 1872, 345–346, Taf. 29 fig. 1-1, Sāmoa-Inseln, Upolu, male Holotype (Mus. GODEFFROY Nr. 6538) (32) (Rack 1961).

## Systematics
### Family DESIDAE Pocock, 1895
#### Subfamily Desinae Pocock, 1895
##### _Desis_ Walckenaer, 1837
###### Material examined.
MALE HOLOTYPE (ZMH-A0000099), from The Independent State of Sāmoa, Upolu, 20°15’N, 155°51’W, Godeffroy Collection.

## Systematics
### Family DESIDAE Pocock, 1895
#### Subfamily Desinae Pocock, 1895
##### _Desis_ Walckenaer, 1837
###### Diagnoses.
Males of _D. vorax_ can be separated from other _Desis_ species, including _D. bobmarleyi_, _D. marina_ and _D. kenyonae_, by having a slim, triangular conductor plate (CP) and a slender conductor tip (Fig. 7F).
</excerpt>
### Rank 5 of 69 — 0.72
<excerpt title="Desis bobmarleyi sp. n., a new spider from coral reefs in Australia's ...">
## Systematics
### Family DESIDAE Pocock, 1895
#### Subfamily Desinae Pocock, 1895
##### _Desis_ Walckenaer, 1837
###### Diagnoses.
Males of _D. vorax_ can be separated from other _Desis_ species, including _D. bobmarleyi_, _D. marina_ and _D. kenyonae_, by having a slim, triangular conductor plate (CP) and a slender conductor tip (Fig. 7F).

## Systematics
### Family DESIDAE Pocock, 1895
#### Subfamily Desinae Pocock, 1895
##### _Desis_ Walckenaer, 1837
###### Description.
_Male_ (Holotype, ZMH-A0000099). Total length 5.85. Prosoma 3.47 long, 2.23 wide, pl/pw 1.55; sternum 1.55 long, 1.38 wide, sl/sw 1.12; opisthosoma 3.30 long, 2.14 wide. Eight eyes in two rows; AME 0.12; ALE 0.14; PLE 0.16; PME 0.17; AME–AME 0.11; ALE–AME 0.12; ALE–PLE 0.05; PLE–PME 0.17; PME–PME 0.20. Clypeus 0.04 high. Prosoma pale bleached, long rectangular, anteriorly straight; fovea short, 0.05 of prosoma length. Chelicerae paturon pale, bleached, strong, elongated, longer than sternum with 5 strong prolateral teeth, fangs 0.9 the length of paturon. Endites, labium and sternum pale bleached, labium trapezoid medially indented, with lateral sinuous margin; endites long with sharp triangular tip, double as long as labium; opisthosoma pale bleached with dark brown markings laterally and a median band scattered in triangles; venter pale. Legs pale, bleached, all tarsi with 3 claws, 3 rd claw about 1/3 length of dorsal claws, both dorsal claws with about eight strong teeth. Body covered with long pale setae.

## Systematics
### Family DESIDAE Pocock, 1895
#### Subfamily Desinae Pocock, 1895
##### _Desis_ Walckenaer, 1837
###### Description.
Palp (Figs 6D–F, 7E, F): cymbium pear-shaped, longer than wide, with slight sclerotisation on retrolateral margin covered with long setae and 5 thick spines in distal third; conductor large, elliptical with slim, triangular sclerotized CP and slender tip, embolus thin, semicircular, covered by conductor, median apophysis thin needle-shaped, retrodistal apophysis with hood–shaped tip. RTA medially indented and ventrally straight.

## Systematics
### Family DESIDAE Pocock, 1895
#### Subfamily Desinae Pocock, 1895
##### _Desis_ Walckenaer, 1837
###### Distribution.
Currently known only from Upolu, one of the islands of the Independent State of Sāmoa. The wider distribution of this species is still unknown but it may be more widespread across the islands of Sāmoa.

## Systematics
### Family DESIDAE Pocock, 1895
#### Subfamily Desinae Pocock, 1895
##### _Desis_ Walckenaer, 1837
###### Remarks.
Apparently, this species has not been re-collected since its original discovery but may have been overlooked because it is found in habitats that are not usually associated with spiders.
</excerpt>

## Search 10 — query: "Desis crosslandi distribution Tanzania Zanzibar"
### Rank 1 of 27 — 0.04 (passed on)
<excerpt title="Indians in Tanzania">
From Wikipedia, the free encyclopedia
Indians in Tanzania| _Watanzania wenye asili ya Kihindi_(Swahili) |  
| --- |  
| Total population |  
| c. 60,000 (2015)[[1]](https://en.wikipedia.org/wiki/Indians_in_Tanzania#cite_note-1)[[2]](https://en.wikipedia.org/wiki/Indians_in_Tanzania#cite_note-2)[[a]](https://en.wikipedia.org/wiki/Indians_in_Tanzania#endnote_Notea) |  
| Regions with significant populations |  
| Dar es Salaam, Zanzibar |  
| Languages |  
| Kutchi-Swahili, Odia,[[3]](https://en.wikipedia.org/wiki/Indians_in_Tanzania#cite_note-3)English (lingua franca), Kiswahili, Gujarati, Kutchi, Hindi |  
| Religion |  
| Islam, Hinduism, Zoroastrianism, Sikhism; significant minorities Christianity |  
| Related ethnic groups |  
| PIO, NRI and Desi |  
| * * * a.**^** includes about 10,000 expatriates |
Indian Prime Minister Narendra Modi meets members of Indian community in Dar es Salaam, 10 July 2016
**Indian Tanzanians** constitute a significant demographic minority within Tanzania; more than 60,000 Tanzanian citizens of Indian descent reside in the country.[[4]](https://en.wikipedia.org/wiki/Indians_in_Tanzania#cite_note-4) Many among them are wealthy traders and entrepreneurs. Despite making up only 0.2% of the population, they are considered by the Hindu Council of Tanzania to have disproportionate ownership of Tanzanian companies.[[5]](https://en.wikipedia.org/wiki/Indians_in_Tanzania#cite_note-5) Indians have a long history in Tanzania, starting with the seasonal arrival of Gujarati traders who used the trade winds. They gradually settled there and came to control the trade in Zanzibar. Several buildings from that period still stand in Stone Town, the primary trading center on the island.
</excerpt>
### Rank 2 of 27 — 0.04
<excerpt title="Tanzania - Distribution and Sales Channels">
# Tanzania - Distribution and Sales Channels
        *   Investor Guide  
        *   Industry Overview Hub  
        *   Workforce Development  
        *   Fact Sheets  
        *   Reports and Publications  
        *   Online Data Tools

    *   Let Our Experts Help

        *   About Select USA  
        *   Services  
        *   Contact Us

    *   Additional Resources

        *   State Business Incentives Database  
        *   Careers and Internships

*   News  
*   About Us  
*   Contact Us
1.   Home  
2.   Country Commercial Guides  
3.   Tanzania - Distribution and Sales Channels
Tanzania Country Commercial Guide
Learn about the market conditions, opportunities, regulations, and business conditions in Tanzania, prepared by at U.S. Embassies worldwide by Commerce Department, State Department and other U.S. agencies’ professionals.
FacebookXLinkedInEmailCopy Link
*   Tanzania Country Commercial Guide  
    *   Doing Business in  
        *   Market Overview  
        *   Market Challenges  
        *   Market Opportunities  
        *   Market Entry Strategy

    *   Leading Sectors for US Exports & Investments  
        *   Healthcare  
        *   Agriculture and Agricultural Processing  
        *   Energy  
        *   Mining  
        *   Information and Communications Technology

    *   Customs, Regulations & Standards  
        *   Trade Barriers  
        *   Import Tariffs  
        *   Import Requirements and Documentation  
        *   Labeling/Marking Requirements  
        *   U.S. Export Controls  
        *   Temporary Entry  
        *   Prohibited & Restricted Imports  
        *   Customs Regulations  
        *   Trade Standards  
        *   Trade Agreements  
        *   Licensing Requirements for Professional Services

    *   Selling US Products & Services  
        *   Distribution and Sales Channels  
        *   eCommerce  
        *   Selling Factors and Techniques  
        *   Trade Financing  
        *   Protecting Intellectual Property  
        *   Selling to the Public Sector

    *   Business Travel  
        *   Business Travel

    *   Investment Climate Statement  
        *   Investment Climate Statement
Select Country Guide
Distribution and Sales Channels
**Last published date:**2026-05-19

# Tanzania - Distribution and Sales Channels
The main point of entry for imports is the port of Dar es Salaam. The city of Dar es Salaam is the commercial hub of the country and is the key entry and distribution point for imported goods. From the port, goods are transported upcountry. Transportation is mainly through roads but there is a government effort to revive the railway sector through the standard gauge railway project. Secondary ports of entry are Tanga, Mtwara and Zanzibar. Distributors play a key role for the market entry and sales of U.S. goods. The Commercial Service highly recommends using a well-researched and knowledgeable distributor to be successful in the market.

# Tanzania - Distribution and Sales Channels
## Using an Agent to Sell U.S. Products and Services
Agents will fast-track the entry of U.S. firms into the Tanzanian market. The U.S. Commercial Service (USCS) at the U.S. Embassy in Dar es Salaam can assist U.S companies interested in finding local agents through a Gold Key Service (GKS). The USCS office can also arrange a physical meeting for U.S. companies to meet with local agents.
</excerpt>
### Rank 3 of 27 — 0.04
<excerpt title="Tanzania - Geography for Kids">
**Capital:** Dodoma
**Population:** 58,005,463

## Brief History of Tanzania:
People have lived in the area of Tanzania for thousands of years. Some of the oldest known remnants of humans have been found in Tanzania. The tribal peoples of the Bantu moved into the area around 2,000 years ago and organized city-states formed around 500 AD. In the 1700s the Arabs arrived and began to use Tanzania for the slave trade. The Sultan Seyyid Said claimed the coastal areas and made Zanzibar his capital city. Zanzibar soon became the main location for the Arab slave trade.
The first European to arrive was Portuguese explorer Vasco da Gama in 1498. Portugal claimed control of the coastland, but did not settle in the area. Portugal tried to maintain control of the ocean trade and to demand tribute from the local tribes. However, the Arab Omani soon forced Portugal from the area.
It was in Tanzania that Scottish missionary David Livingstone, who crusaded against the slave trade, was found by American journalist Henry Stanley and Stanley made his famous statement "Dr. Livingstone, I presume?" Stanley had been commissioned by the New York Herald to find David Livingstone.
Over the years the British became more involved in the area. In 1890 Zanzibar became a British Protectorate. At the same time Germany took control of other areas of Tanzania called Tanganyika. After World War II, the British took full control of both Zanzibar and Tanganyika until 1961 when Tanganyika became an independent country. In 1964 Tanganyika and Zanzibar merged to become Tanzania.

## The Geography of Tanzania
**Total Size:** 945,087 square km
**Size Comparison:** slightly larger than twice the size of California
**Geographical Coordinates:** 6 00 S, 35 00 E
**World Region or Continent:**Africa
**General Terrain:** plains along coast; central plateau; highlands in north, south
**Geographical Low Point:** Indian Ocean 0 m
**Geographical High Point:** Kilimanjaro 5,895 m
**Climate:** varies from tropical along coast to temperate in highlands
**Major cities:** DODOMA (Capital), Dar Es Salaam 3.207 million (2009), Mwanza, Zanzibar City

## The People of Tanzania
**Type of Government:** republic
**Languages Spoken:** Kiswahili or Swahili (official), Kiunguja (name for Swahili in Zanzibar), English (official, primary language of commerce, administration, and higher education), Arabic (widely spoken in Zanzibar), many local languages
**Independence:** 26 April 1964; Tanganyika became independent 9 December 1961 (from UK-administered UN trusteeship); Zanzibar became independent 19 December 1963 (from UK); Tanganyika united with Zanzibar 26 April 1964 to form the United Republic of Tanganyika and Zanzibar; renamed United Republic of Tanzania 29 October 1964
**National Holiday:** Union Day (Tanganyika and Zanzibar), 26 April (1964)
**Nationality:** Tanzanian(s)
**Religions:** mainland - Christian 30%, Muslim 35%, indigenous beliefs 35%; Zanzibar - more than 99% Muslim
**National Symbol:** Uhuru (Freedom) torch
**National Anthem or Song:** Mungu ibariki Afrika (God Bless Africa)
</excerpt>
### Rank 4 of 27 — 0.03
<excerpt title="8101 - AEF Drop of Zanzibar Limited">
# 8101 - AEF Drop of Zanzibar Limited
## AEF Drop of Zanzibar Limited
*   Back to Search
DISCLOSURES MENU
*   Home  
*   IFC Projects  
*   IFC Corporate Disclosures  
*   Transparency at IFC

*   INQUIRIES  
*   SUBSCRIPTION

# 8101 - AEF Drop of Zanzibar Limited
## Summary of Proposed Investment
**Project Number**  
8101
**Company Name**  
Drop of Zanzibar Ltd.
**Date SPI Disclosed**  
Apr 9, 1997
**Country**  
Tanzania
**Industry**  
Agribusiness and Forestry
**Status**  
Completed
**Sector**  
Soft Drink
**Department**  
Gbl Ind, Manufact, Agribus & Services
**Environmental Category**  
B - Limited
**Previous Events**  
Approved : Jul 16, 1997
Signed : Aug 14, 1997
Invested : Oct 9, 1997

# 8101 - AEF Drop of Zanzibar Limited
## Project Description
SUMMARY OF PROJECT INFORMATION (SPI)
Project name Tanzania-Drop of Zanzibar Ltd  
Region Sub-Saharan Africa
Sector Manufacturing
Project No 008101
Projected Board Date May 15, 1997
Company Name: Drop of Zanzibar Ltd
Technical Partners and/or Major Shareholders: Mr. Bruno Conti, Italian (25%), proposed Managing Director, Mr. Walter Rigo, Italian (15%), proposed Production Manager, Mrs. Nadia M. Mohammed Rigo, Zanzibari (10%), experienced businesswoman and Panafric Construction Corporation, Liberian (50%), Investment company.
Project Cost including proposed IFC Investment:
Project cost: US$1.25 million
IFC Investment: US$400,000
Location of Project and Description of Site: The project is located in Mgenihaji area in Central District of Zanzibar. The project area covers 5 hectares having 5 different water veins. The factory site is on the main road linking the city of Zanzibar to Uroa Bay, at about 15 kms from the city centre.
Description of Company and Purpose of Project: Drop of Zanzibar Ltd. is a new company that is in the process of establishing a mineral water processing and bottling plant. The project will be located in Zanzibar and will have a capacity of 2,300 bottles per hour. Water will be sourced from several wells on a 33 year concession basis by the Government. The total cost of the project is estimated at US$1.25 million of which IFC has been approached to provide a loan of US$400,000.
Developmental Impact: The project will create direct employment for 45 people; add value to a natural resource - water; and save substantial amounts of foreign exchange through import substitution.
IFC Role: (a) IFC is to provide medium term loan finance which is not readily available in Zanzibar or Tanzania; (b) Provide catalytic effect by encouraging the foreign investors to go ahead with the project whose success will attract more foreign investors in Zanzibar; and (c) provide technical assistance (through its consultant) with regard to environmental protection and water quality management issues.
</excerpt>
### Rank 5 of 27 — 0.03
<excerpt title="Tanzania - Geography for Kids">
## The People of Tanzania
**Type of Government:** republic
**Languages Spoken:** Kiswahili or Swahili (official), Kiunguja (name for Swahili in Zanzibar), English (official, primary language of commerce, administration, and higher education), Arabic (widely spoken in Zanzibar), many local languages
**Independence:** 26 April 1964; Tanganyika became independent 9 December 1961 (from UK-administered UN trusteeship); Zanzibar became independent 19 December 1963 (from UK); Tanganyika united with Zanzibar 26 April 1964 to form the United Republic of Tanganyika and Zanzibar; renamed United Republic of Tanzania 29 October 1964
**National Holiday:** Union Day (Tanganyika and Zanzibar), 26 April (1964)
**Nationality:** Tanzanian(s)
**Religions:** mainland - Christian 30%, Muslim 35%, indigenous beliefs 35%; Zanzibar - more than 99% Muslim
**National Symbol:** Uhuru (Freedom) torch
**National Anthem or Song:** Mungu ibariki Afrika (God Bless Africa)

## Economy of Tanzania
**Major Industries:** agricultural processing (sugar, beer, cigarettes, sisal twine); diamond, gold, and iron mining, salt, soda ash; cement, oil refining, shoes, apparel, wood products, fertilizer
**Agricultural Products:** coffee, sisal, tea, cotton, pyrethrum (insecticide made from chrysanthemums), cashew nuts, tobacco, cloves, corn, wheat, cassava (tapioca), bananas, fruits, vegetables; cattle, sheep, goats
**Natural Resources:** hydropower, tin, phosphates, iron ore, coal, diamonds, gemstones, gold, natural gas, nickel
**Major Exports:** gold, coffee, cashew nuts, manufactures, cotton
**Major Imports:** consumer goods, machinery and transportation equipment, industrial raw materials, crude oil
**Currency:** Tanzanian shilling (TZS)
**National GDP:** $67,900,000,000
** Source for population (2012 est.) and GDP (2011 est.) is CIA World Factbook.
Back to **Geography** Home Page
</excerpt>

For each search, read the top excerpt and the ones ranked below it, and judge whether the order is right for answering the question. An excerpt holding the answer, or a fact that leads to it, should outrank one that only repeats the query's words or covers the topic without a checkable fact. If none of the excerpts holds anything useful, that is the search's fault, not this instruction's. Find the ranking error that cost the most and write a new instruction that fixes it. Replace or compress existing text where you can; avoid making it much longer. Do not write the "Original question" or "Search query" lines; they are appended for you. Do not copy any fact, name, site or topic from these examples.

Provide the new instruction within ``` blocks.
