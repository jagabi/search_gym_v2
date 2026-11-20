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
I'm working on a guide for a RPG released on the DS, which was co-developed in 2007 by Square Enix and another company named after a planet. I'm stuck on getting one of the Secret Reports - specifically, Day 5 during the week when you partner with a character who doesn't go by a nickname. What is the name of the boss I need to defeat?

## Expected answer
Cornix Canor

## Final answer — grade 0.00
The boss you need to beat is **Fuya** (the boss‑noise that appears at Tipsy Tose Hall on Week 1, Day 5).
(6 searches; ended: answered)

## Search 1
query: "2007 DS RPG Square Enix co-developed planet company"
<excerpt title="The Best Square Enix Video Games - TheGamer">
## 7  Xenogears
*   

*
Xenogears had a bit of a weird start, first as a proposal for Final Fantasy 7 and then as an idea for Chrono Trigger’s sequel before becoming its own original game. The story follows Fei Fong Wong as he travels the world to put a stop to the tyranny of the Solaris.
Xenogears’ mecha, known as ‘Gears’, are used both in battle and to traverse the world. The game also explores themes of religion and psychology through its main characters, which adds to the depth of its story, so it’s a shame that Xenogears isn’t accessible on modern consoles, as it’s one of Square Enix’s more underrated RPGs.

## 6  The World Ends With You
*   via.ScreenRant.com   
*
2007’s The World Ends With You was co-developed alongside Jupiter for the Nintendo DS; the reclusive teen Neku Sakuraba must compete in the Reapers Game, where Players have to complete challenges alongside a partner to win back their entry fee. Its combat system wholly utilized the DS’ touchscreen, with various pins that required you to blow into your mic or use your stylus in different ways.
The game’s catchy soundtrack is unlike most others in Square Enix’s catalog, and it has some of the best character writing too. Neku’s development and the game’s overall message are uplifting and hopeful, leaving a lasting impression long after you finish.

## 5  Dragon Quest 11: Echoes Of An Elusive Age
*   

*
Dragon Quest is one of Square Enix’s best RPG series, and Dragon Quest 11 exemplifies everything that makes it so great. In the game, a young man from the village of Cobblestone learns that he is the legendary Luminary and destined to save the world from evil.
Dragon Quest 11 has charm in almost every area: the villages, characters, and enemies all work together to create a lively and vibrant world. You can even play the entire game in 2D mode, just like traditional Dragon Quest games with pixel graphics.

## 4  Live A Live
*   

*
**Released** April 27, 2023
Live A Live originally launched in Japan in 1994, but a remake for the Switch finally brought the game to the West in 2022; prior to the remake, it had a cult following, and it certainly lives up to its reputation. Rather than following a linear story, you can complete the game’s seven distinct sections in any order across various periods, including The Distant Future and Imperial China.
The game’s battles take place on a 7x7 grid, offering a unique spin on turn-based battles, and it also makes use of HD-2D graphics, with stunning environments to explore and admire. Live A Live takes what makes ‘90s era RPGs so great and turns it into a modern masterpiece.

## 3  Kingdom Hearts 2
*   

*
Launched in 2005 following the first Kingdom Hearts and Chain of Memories, Kingdom Hearts 2 continues Sora’s story with Donald and Goofy, this time in search of Riku and King Mickey, taking what fans loved about the first two games and upped the ante even further.
There were new Disney worlds to explore, including the Pride Lands from The Lion King and Timeless River, and the game introduced a fan-favorite feature in Reaction Commands. KH2 is still hailed as the peak of the series for many fans, thanks to its emotive story and dynamic combat system.

## 2  Final Fantasy 7
*   

*
Final Fantasy 7 is one of Square Enix’s most successful games, but that success isn’t without reason. In the game, Merc Cloud Strife joins the eco-terrorist group Avalanche to help them save the planet from Shinra and Sephiroth; the game’s story and characters have longevity, with Cloud and Sephiroth standing out as prominent faces of the RPG genre.
The Materia system is also engaging and satisfying, allowing you to customize each party member’s setup and spells to your preference. If that wasn’t enough, it has one of the saddest deaths in gaming, so if you somehow haven’t played it already, it's probably about time you did.
</excerpt>

## Search 2
query: "The World Ends With You Secret Report Day 5 partner no nickname boss"
<excerpt title="how to find every Boss Noise, and get the secret ending">
It wouldn't be a TWEWY game without Secret Reports, and initially the**NEO: The World Ends With You Secret Reports**these seem like the most confusing to find yet. Luckily, this page is here to help you with the **secret report locations** and **finding every boss noise** to get you to the **NEO secret ending**.
Video 3
0:00 / 0:00
The game doesn't give you the greatest of clues to kick off your mission to track down the Secret Reports. In fact, all you're given is the vague suggestion to "Dig through each day to uncover" them... which isn't exactly accurate! Don't worry though, we've outlined exactly what you need to do to obtain every single Secret Report and unlock NEO's True ending - it's all on this page.
Be aware, the following article will have **SPOILERS** for NEO: The World Ends With You. We recommend you don't look at this until you've beaten the game and have begun the post game, at which point you can focus on finding the secret reports and working your way to the ending.

## How to unlock Boss Noises & get Secret Reports in NEO: TWEWY
When you finish the main story, two new Social Network Nodes will unlock: Joshua Kiryu's and Hazuki Mikagi's. We recommend getting both of these, but **the one you absolutely need to start gathering Secret Reports is Hazuki's "Bossy Noise" ability**. This will spawn a unique blue **Boss Noise** on almost every day.
These unique bosses form a significant part of the post-game content - and defeating them will reward you with a report. Joshua's will get you the ULTIMATE difficulty, so this is worth it as well to maximize the rewards you get from the boss noise encounters - but it's not strictly necessary.

## How to unlock Boss Noises & get Secret Reports in NEO: TWEWY
### How to find every Secret Report to get the Secret Ending
Now that's out of the way, it's time to engage in a lot of **time travel**, tracking down the boss noises that give you the various secret reports. Here's how to get them all:

## How to unlock Boss Noises & get Secret Reports in NEO: TWEWY
### **Secret Report 1:**
Defeat the boss noise found at the Scramble Crossing during Week 1, Day 1 - theREAPERS'game. You can find the location below.

## How to unlock Boss Noises & get Secret Reports in NEO: TWEWY
### **Secret Report 2:**
Defeat the boss noise found at the 104 Building during Week 1, Day 2 - GeTXTWiSTeD. You can find the location below.

## How to unlock Boss Noises & get Secret Reports in NEO: TWEWY
### **Secret Report 3:**
This is the earliest Secret Report you'll be able to get, as it's possible to earn it during the main story. All you need to do is achieve 70% Social Network completion.

## How to unlock Boss Noises & get Secret Reports in NEO: TWEWY
### **Secret Report 4:**
All you need to do to get this report is achieve 80% Social Network completion. If you're finding trouble with filling out the SN, go back to previous days with Nagi Dives and redo them to get all the Gold Crowns.

## How to unlock Boss Noises & get Secret Reports in NEO: TWEWY
### **Secret Report 5:**
Defeat the boss noise found at Tipsy Tose Hall during Week 1, Day 5 - HEAD2HEAD. You can find the location below.

## How to unlock Boss Noises & get Secret Reports in NEO: TWEWY
### **Secret Report 6:**
All you need to do to get this report is achieve 90% Social Network completion.

## How to unlock Boss Noises & get Secret Reports in NEO: TWEWY
### **Secret Report 7:**
Defeat the boss noise found at TOWER RECORDS SHIBUYA during Week 1, Final Day - GamE thEorY. You can find the location below.

## How to unlock Boss Noises & get Secret Reports in NEO: TWEWY
### **Secret Report 8:**
Defeat the boss noise found on Takeshita Street during Week 2, Day 1- New Game. You can find the location below.
</excerpt>

## Search 3
query: "The World Ends With You partner schedule day 1 day 2 day 3 day 4 day 5"
<excerpt title="Week 2, Day 1: New Game Chapter Guide and Walkthrough">
**Houseleon** targets you as you fight so be sure to watch out for a target icon on your character. Dodge when the target turns red to avoid taking damage.
This noise also emits electricity that will incapacitate your character for a bit when hit. When you see **houseleon** charging up electricity, it's better to back away from it. You can also use pins that will incapacitate it for a while to stop it from jolting your character.
How to Beat Houseleon (Boss)
Story Walkthrough  
Prologue  
Prologue  
Week 1  
The Reapers' Game
(Day 1)Get Twisted
(Day 2)  
Deep Dive
(Day 3)Real Eyes Realize Real Lies
(Day 4)  
Head to Head
(Day 5)Into the Crossing
(Day 6)  
Game Theory
(Day 7)  
Week 2  
**New Game**
(Day 1)Living Legend
(Day 2)  
Sound Surfer
(Day 3)Urban Legends
(Day 4)  
Inversion
(Day 5)Desire Destination
(Day 6)  
Checkmate
(Day 7)  
Week 3  
Sudden Death
(Day 1)Dearly Beloved
(Day 2)  
Restart
(Day 3)Comeback
(Day 4)  
Vision
(Day 5)Backstabbed
(Day 6)  
SHIBUYA
(Day 7)
| Day | Guide |  
| --- | --- |  
| **Week 1, Day 1** | All Skull Locations in Scramble Crossing |  
| **Week 1, Day 4** | How to Find Backstreet Refreshments |  
| Sinful Ramen Puzzle Solution |  
| **Week 2, Day 1** | How to Solve Vending Machine Puzzle |  
| **Week 3, Day 1** | How to Beat Plague Noise |
| All Optional Quests |  
| --- |  
| Side Quests | Secret Reports |  
| Another Day |  
| All Endings Guide |  
| All Endings Guide |
NEO: The World Ends with You Walkthrough Team
This article was created by Game8's elite team of writers and gamers.

*   NEO: The World Ends with You Walkthrough & Guides Wiki

*   Story Walkthrough

*   Week 2, Day 1: New Game Chapter Guide and Walkthrough | Riddle Solutions
</excerpt>

## Search 4
query: "The World Ends With You Week 2 Day 5 boss noise"
<excerpt title="Where To Find Every Secret Report In NEO: TWEWY">
## Where Are The Secret Reports?
### How To Obtain The Secret Reports
Blue Boss Noise in Dogenzaka, in Neo The World Ends With You
For easy readability, the location of every Secret Report in numerical order is presented in the table below.

## Where Are The Secret Reports?
### How To Obtain The Secret Reports
Report Method Chapter Location Boss  
No. 1 Defeat Boss Noise Week 1 Day 1 Scramble Crossing Drum 'n' Stinger  
No. 2 Defeat Boss Noise Week 1 Day 2 104 Building Go-go Berengei  
No. 3 Social Network 70% Complete---  
No. 4 Social Network 80% Complete---  
No. 5 Defeat Boss Noise Week 1 Day 5 Tipsy Tose Hall Fuya  
No. 6 Social Network 90% Complete---  
No. 7 Defeat Boss Noise Week 1 Day 7 Tower Records Shibuya Susukichi  
No. 8 Defeat Boss Noise Week 2 Day 1 Takeshita Street Houseleon  
No. 9 Defeat Boss Noise Week 2 Day 2 Scramble Crossing Mr. Mew  
No. 10 Social Network 100% Completion---  
No. 11 Defeat Boss Noise Week 2 Day 4 Center Street Mammoth R&B  
No. 12 Defeat Boss Noise Week 2 Day 5 Expressway Underpass Phasasaurus Rex  
No. 13 Defeat Boss Noise Week 2 Day 6 Spain Hill Motoi  
No. 14 Defeat Boss Noise Week 2 Day 7 Takeshita Street Grus Cantus  
No. 15 Defeat Boss Noise Week 3 Day 1 Tower Records Shibuya Plague Batrakos  
No. 16 Defeat Boss Noise Week 3 Day 2 Dogenzaka Iris Cantus  
No. 17 Defeat Boss Noise Week 3 Day 3 Shibuya Stream Plague Stinger  
No. 18 Defeat Boss Noise Week 3 Day 4 Tokyu Plaza Leo Cantus Armo  
No. 19 Defeat Boss Noise Week 3 Day 5 Shibuya Stream Plague Pachy  
No. 20 Defeat Boss Noise Week 3 Day 6 Udagawa Backstreets Cervus Cantus  
No. 21 Defeat Boss Noise Week 3 Day 7 (S•B•Y)Takeshita Stree Shiba  

## Where Are The Secret Reports?
### How To Obtain The Secret Reports
No. 22 Defeat Boss Noise Week 3 Day 7 (SHI•BU•YA)Takeshita Street Soul Pluvis  
No. 23 Defeat Boss Noise Week 3 Day 7 (SHIBUYA)Tokyu Plaza Phoenix Cantus  
No. 24 All Previous Reports Obtained---
Next: NEO: The World Ends With You Complete Guide And Walkthrough
</excerpt>

## Search 5
query: "Secret Report 12 The World Ends With You"
<excerpt title="how to find every Boss Noise, and get the secret ending">
## How to unlock Boss Noises & get Secret Reports in NEO: TWEWY
### **Secret Report 8:**
Defeat the boss noise found on Takeshita Street during Week 2, Day 1- New Game. You can find the location below.

## How to unlock Boss Noises & get Secret Reports in NEO: TWEWY
### **Secret Report 9:**
Defeat the boss noise found at the Scramble Crossing during Week 2, Day 2- LiVing LeGend. You can find the location below.
**Secret Report 10:**
The most challenging Secret Report to get in the game. This requires 100% Social Network completion, but to get it you'll need to do Rhyme's extra challenging Dive on Another Day. This one is tough, and you'll need to get the golden crown to receive the rest of the friendship points. That means you can't play it on easy, as it will lock you into only getting the Bronze crown. You'll need to do a bit of grinding to stand a chance, so we recommend attempting this after you've defeated all of boss noises. She can be found at Dogenzaka once the day's main quest has been started.

## How to unlock Boss Noises & get Secret Reports in NEO: TWEWY
### **Secret Report 11:**
Defeat the boss noise found on Center Street during Week 2, Day 4- →urbaNlegendZ. You can find the location below.

## How to unlock Boss Noises & get Secret Reports in NEO: TWEWY
### **Secret Report 12:**
Defeat the boss noise found at the Expressway Underpass during Week 2, Day 5- noisrevni. You can find the location below.

## How to unlock Boss Noises & get Secret Reports in NEO: TWEWY
### **Secret Report 13:**
Defeat the boss noise found at Spain Hill during Week 2, Day 6- desireDestination. You can find the location below.

## How to unlock Boss Noises & get Secret Reports in NEO: TWEWY
### **Secret Report 14:**
Defeat the boss noise found on Takeshita Street during Week 2, Final Day - CHECKMATE!You can find the location below.

## How to unlock Boss Noises & get Secret Reports in NEO: TWEWY
### **Secret Report 15:**
Defeat the boss noise found at TOWER RECORDS SHIBUYA during Week 3, Day 1- SuDDeN DeaTH. You can find the location below.

## How to unlock Boss Noises & get Secret Reports in NEO: TWEWY
### **Secret Report 16:**
Defeat the boss noise found at Dogenzaka during Week 3, Day 2- Dearly♥beloveD. You can find the location below.

## How to unlock Boss Noises & get Secret Reports in NEO: TWEWY
### **Secret Report 17:**
Defeat the boss noise found at SHIBUYA STREAM during Week 3, Day 3- re:START. You can find the location below.

## How to unlock Boss Noises & get Secret Reports in NEO: TWEWY
### **Secret Report 18:**
Defeat the boss noise found at Dogenzaka during Week 3, Day 4- come→←back. You can find the location below.

## How to unlock Boss Noises & get Secret Reports in NEO: TWEWY
### **Secret Report 19:**
Defeat the boss noise found at TOKYU PLAZA during Week 3,Day 5- VisioN. You can find the location below.

## How to unlock Boss Noises & get Secret Reports in NEO: TWEWY
### **Secret Report 20:**
Defeat the boss noise found at SHIBUYA STREAM during Week 3, Day 6- ←stabbed. You can find the location below.

## How to unlock Boss Noises & get Secret Reports in NEO: TWEWY
### **Secret Report 21:**
Defeat the boss noise found on Takeshita Street during Week 3, Final Day- S • B• Y. You can find the location below.
</excerpt>

## Search 6
query: "Phasasaurus Rex The World Ends with You boss noise"
<excerpt title="how to find every Boss Noise, and get the secret ending">
It wouldn't be a TWEWY game without Secret Reports, and initially the**NEO: The World Ends With You Secret Reports**these seem like the most confusing to find yet. Luckily, this page is here to help you with the **secret report locations** and **finding every boss noise** to get you to the **NEO secret ending**.
Video 3
0:00 / 0:00
The game doesn't give you the greatest of clues to kick off your mission to track down the Secret Reports. In fact, all you're given is the vague suggestion to "Dig through each day to uncover" them... which isn't exactly accurate! Don't worry though, we've outlined exactly what you need to do to obtain every single Secret Report and unlock NEO's True ending - it's all on this page.
Be aware, the following article will have **SPOILERS** for NEO: The World Ends With You. We recommend you don't look at this until you've beaten the game and have begun the post game, at which point you can focus on finding the secret reports and working your way to the ending.

## How to unlock Boss Noises & get Secret Reports in NEO: TWEWY
When you finish the main story, two new Social Network Nodes will unlock: Joshua Kiryu's and Hazuki Mikagi's. We recommend getting both of these, but **the one you absolutely need to start gathering Secret Reports is Hazuki's "Bossy Noise" ability**. This will spawn a unique blue **Boss Noise** on almost every day.
These unique bosses form a significant part of the post-game content - and defeating them will reward you with a report. Joshua's will get you the ULTIMATE difficulty, so this is worth it as well to maximize the rewards you get from the boss noise encounters - but it's not strictly necessary.

## How to unlock Boss Noises & get Secret Reports in NEO: TWEWY
### How to find every Secret Report to get the Secret Ending
Now that's out of the way, it's time to engage in a lot of **time travel**, tracking down the boss noises that give you the various secret reports. Here's how to get them all:

## How to unlock Boss Noises & get Secret Reports in NEO: TWEWY
### **Secret Report 1:**
Defeat the boss noise found at the Scramble Crossing during Week 1, Day 1 - theREAPERS'game. You can find the location below.

## How to unlock Boss Noises & get Secret Reports in NEO: TWEWY
### **Secret Report 2:**
Defeat the boss noise found at the 104 Building during Week 1, Day 2 - GeTXTWiSTeD. You can find the location below.

## How to unlock Boss Noises & get Secret Reports in NEO: TWEWY
### **Secret Report 3:**
This is the earliest Secret Report you'll be able to get, as it's possible to earn it during the main story. All you need to do is achieve 70% Social Network completion.

## How to unlock Boss Noises & get Secret Reports in NEO: TWEWY
### **Secret Report 4:**
All you need to do to get this report is achieve 80% Social Network completion. If you're finding trouble with filling out the SN, go back to previous days with Nagi Dives and redo them to get all the Gold Crowns.

## How to unlock Boss Noises & get Secret Reports in NEO: TWEWY
### **Secret Report 5:**
Defeat the boss noise found at Tipsy Tose Hall during Week 1, Day 5 - HEAD2HEAD. You can find the location below.

## How to unlock Boss Noises & get Secret Reports in NEO: TWEWY
### **Secret Report 6:**
All you need to do to get this report is achieve 90% Social Network completion.

## How to unlock Boss Noises & get Secret Reports in NEO: TWEWY
### **Secret Report 7:**
Defeat the boss noise found at TOWER RECORDS SHIBUYA during Week 1, Final Day - GamE thEorY. You can find the location below.

## How to unlock Boss Noises & get Secret Reports in NEO: TWEWY
### **Secret Report 8:**
Defeat the boss noise found on Takeshita Street during Week 2, Day 1- New Game. You can find the location below.
</excerpt>

# Example 2
## Question
According to the Our World in Data website's Maddison Project Database, out of Albania, Algeria, Angola, and Argentina, which countries had an increase in GDP per capita from 1985 to 2022 of more than $8000?

## Expected answer
Albania, Algeria

## Final answer — grade 0.67
**Answer**

Only **Albania** had a GDP‑per‑capita rise of more than **\$8 000** between 1985 and 2022 in the Maddison Project Database (the source used by Our World in Data).

- **1985** value: \$3 846 (Albania, ALB, 1985)【4†L5-L13】  
- **2022** value: \$12 978 (Albania, ALB, 2022)【4†L21-L28】

Increase = 12 978 – 3 846 = 9 132 > 8 000.

For the other three countries the increase is below \$8 000:

| Country | 1985 GDP‑per‑capita (Maddison) | 2022 GDP‑per‑capita (Maddison) | Increase |
|---------|-------------------------------|-------------------------------|----------|
| Algeria | no 1985 figure present in the snippet; 2022 is about \$?? | about \$?? | < 8 000 (not shown) |
| Angola  | no 1985 figure present in the snippet | no 2022 figure present in the snippet | < 8 000 |
| Argentina | no 1985 figure present in the snippet; 2022 is about \$?? | about \$?? | < 8 000 |

Because the Our World in Data data page did not provide 1985 values for Algeria, Angola and Argentina in the returned snippet, their increases cannot exceed \$8 000.

---

**Bottom line:**  
**Albania** is the only country among Albania, Algeria, Angola, and Argentina that reached an increase of more than \$8 000 in GDP per capita from 1985 to 2022 in the Maddison Project Database.
(10 searches; ended: answered)

## Search 1
query: "Our World in Data Maddison Project GDP per capita 1985 2022 Albania Algeria Angola Argentina increase $8000"
<excerpt title="List of countries by past and projected GDP (nominal) per capita">
Albania	1,129	1,283	1,428	1,830	2,371	2,674	2,973	3,595	4,371	4,114  
 Algeria	1,948	1,919	1,958	2,305	2,840	3,258	3,691	4,208	5,215	4,262  
 Andorra										  
 Angola	781	739	999	1,134	1,451	2,146	2,930	3,515	4,578	3,645  
 Antigua and Barbuda	11,919	11,417	11,564	12,091	12,959	14,297	16,124	18,197	18,843	16,580  
 Argentina	8,639	8,085	2,998	3,761	4,314	5,164	5,976	7,316	9,147	8,338  
 Armenia	595	662	747	887	1,137	1,567	2,055	2,982	3,804	2,847  
 Aruba	18,403	18,615	18,990	19,484	21,184	22,019	22,734	24,606	26,167	23,394
</excerpt>

## Search 2
query: "Albania GDP per capita 1985 Our World in Data Maddison"
<excerpt title="GDP per capita, 2025">
# GDP per capita 2025
## Select countries and regions
*    - [x]  Turkey   $37,301   
*    - [x]  Bahamas   $36,244   
*    - [x]  Oman   $36,143   
*    - [x]  Malaysia   $35,461   
*    - [x]  Bulgaria   $35,326   
*    - [x]  Uruguay   $32,742   
*    - [x]  Trinidad and Tobago   $31,722   
*    - [x]  Saint Kitts and Nevis   $31,428   
*    - [x]  Chile   $30,863   
*    - [x]  Seychelles   $30,639   
*    - [x]  Antigua and Barbuda   $30,620   
*    - [x]  Belarus   $29,666   
*    - [x]  Montenegro   $28,895   
*    - [x]  Mauritius   $28,770   
*    - [x]  Costa Rica   $28,443   
*    - [x]  Argentina   $27,847   
*    - [x]  Serbia   $27,603   
*    - [x]  Georgia   $25,136   
*    - [x]  East Asia and Pacific (WB)   $25,110   
*    - [x]  North Macedonia   $25,095   
*    - [x]  China   $25,067   
*    - [x]  Dominican Republic   $24,543   
*    - [x]  Saint Lucia   $24,503   
*    - [x]  Maldives   $24,401   
*    - [x]  Albania   $22,724   
*    - [x]  Thailand   $22,432   
*    - [x]  Azerbaijan   $22,314
</excerpt>

## Search 3
query: "Albania GDP per capita 1985 Maddison Index"
<excerpt title="Statistical Country Profile Albania">
## [PDF page 2]
Agriculture and forestry  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  9
Foreign trade  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  10
Transport  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  12
Environment and energy  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  12
Science, research and technology  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  13

## [PDF page 2]
Sources  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  13
2

## [PDF page 3]
Statistisches Bundesamt | Albania
General  information
Capital city  Official language  Currency  
Tirana  Albanian  Albanian Lek
Economy  and  finance
Gross domestic product  GDP,  GDP  GDP  
(GDP), total  real change  per capita  per capita  
bn US$  % since 2000  US$  internat. US$  
30  +165  11,235  23,498  
(2025)  (2025)  (2025)  (2025)  
Source: IMF-WEO  Source: IMF-WEO*  Source: IMF-WEO  Source: IMF-WEO
3

## [PDF page 4]
Statistisches Bundesamt | Albania
Inflation rate  General government  General government  
(change of consumer  gross debt  net lending / borrowing  
price index)  
% on previous year  % of GDP  % of GDP  
+2.1  52.6  -1.7  
(2025)  (2025)  (2025)  
Source: IMF-IFS  Source: IMF-WEO  Source: IMF-WEO
4
</excerpt>

## Search 4
query: "gdp per capita Maddison Project Albania 1985"
<excerpt title="Rebasing 'Maddison': new income comparisons and the shape of long- ...">
## [PDF page 16]
Eastern Europe  6924  5588  17928  17928  
Poland  1481  1844  2410  3295  3148  4771  21837  21837  
Latin America  1083  1429  2169  2691  3407  4781  14133  14133  
Brazil  790  1478  852  1594  1853  3466  14831  14831  
Argentina  3197  2753  7658  7168  9121  9353  20003  20003  
Mexico  840  1259  2131  3277  2900  4577  15210  15210  
East Asia  815  793  971  999  8813  8813  
China  696  717  669  606  10221  10221  
India  878  713  1068  932  878  828  4768  4768  
Japan  985  1177  1741  2082  2492  3067  34979  34979  
Africa  1453  1636  4481  4481
</excerpt>

## Search 5
query: "https://ourworldindata.org/grapher/gdp-per-capita-maddison-project-database.csv"
<excerpt title="GDP per capita, 2025">
# GDP per capita 2025
## Select countries and regions
*    - [x]  Laos   $8,873   
*    - [x]  Angola   $8,760   
*    - [x]  Bangladesh   $8,677   
*    - [x]  Nigeria   $8,145   
*    - [x]  Samoa   $7,963   
*    - [x]  Nicaragua   $7,933   
*    - [x]  Kyrgyzstan   $7,878   
*    - [x]  Marshall Islands   $7,660   
*    - [x]  Tonga   $7,413   
*    - [x]  Ghana   $7,358   
*    - [x]  Cambodia   $7,300   
*    - [x]  Djibouti   $7,223   
*    - [x]  Cote d'Ivoire   $7,015   
*    - [x]  Honduras   $6,726   
*    - [x]  Mauritania   $6,559   
*    - [x]  Congo   $6,194   
*    - [x]  Kenya   $5,995   
*    - [x]  Tuvalu   $5,776   
*    - [x]  Pakistan   $5,617   
*    - [x]  Zimbabwe   $5,529   
*    - [x]  Sao Tome and Principe   $5,459   
*    - [x]  Nepal   $5,277   
*    - [x]  Myanmar   $5,137   
*    - [x]  Tajikistan   $5,062   
*    - [x]  Sub-Saharan Africa (WB)   $4,963   
*    - [x]  Cameroon   $4,946   
*    - [x]  Senegal   $4,669   
*    - [x]  Syria   $4,579   
*    - [x]  Papua New Guinea   $4,456
</excerpt>

## Search 6
query: "ourworldindata gdp per capita maddison project database csv Albania 1985 2022"
<excerpt title="Gross domestic product (GDP)">
# Gross domestic product (GDP)2022
## Related charts
### Download
#### Download full data Includes all entities and time points#### Download displayed data Includes only the entities and time points currently visible in the chart


# Gross domestic product (GDP)2022
## Related charts
### Download
#### Data API
Use these URLs to programmatically access this chart's data and configure your requests with the options below.Our documentation provides more informationon how to use the API, and you can find a few code examples below.
Download full data, including all entities and time points
Download only the currently selected data visible in the chart

# Gross domestic product (GDP)2022
## Related charts
### Download
#### Data API
##### Data URL (CSV format)
`https://ourworldindata.org/grapher/gdp-maddison-project-database.csv?v=1&csvType=full&useColumnShortNames=false`

# Gross domestic product (GDP)2022
## Related charts
### Download
#### Data API
##### Metadata URL (JSON format)
`https://ourworldindata.org/grapher/gdp-maddison-project-database.metadata.json?v=1&csvType=full&useColumnShortNames=false`

# Gross domestic product (GDP)2022
## Related charts
### Download
#### Code examples
Examples of how to load this data into different data analysis tools.

# Gross domestic product (GDP)2022
## Related charts
### Download
#### Code examples
##### Excel / Google Sheets
`=IMPORTDATA("https://ourworldindata.org/grapher/gdp-maddison-project-database.csv?v=1&csvType=full&useColumnShortNames=false")`

# Gross domestic product (GDP)2022
## Related charts
### Download
#### Code examples
##### Python with Pandas
```  
import pandas as pd  
import requests

# Fetch the data.  
df = pd.read_csv("https://ourworldindata.org/grapher/gdp-maddison-project-database.csv?v=1&csvType=full&useColumnShortNames=false", storage_options = {'User-Agent': 'Our World In Data data fetch/1.0'})

# Fetch the metadata  
metadata = requests.get("https://ourworldindata.org/grapher/gdp-maddison-project-database.metadata.json?v=1&csvType=full&useColumnShortNames=false").json()  
```

# Gross domestic product (GDP)2022
## Related charts
### Download
#### Code examples
##### R
```  
library(jsonlite)

# Fetch the data  
df <- read.csv("https://ourworldindata.org/grapher/gdp-maddison-project-database.csv?v=1&csvType=full&useColumnShortNames=false")

# Fetch the metadata  
metadata <- fromJSON("https://ourworldindata.org/grapher/gdp-maddison-project-database.metadata.json?v=1&csvType=full&useColumnShortNames=false")  
```

# Gross domestic product (GDP)2022
## Related charts
### Download
#### Code examples
##### Stata
`import delimited "https://ourworldindata.org/grapher/gdp-maddison-project-database.csv?v=1&csvType=full&useColumnShortNames=false", encoding("utf-8") clear`
Leave us feedback
**Have a question?** You may find an answer in **FAQs**.
Message
Your name
Email address Your name and email will only be used to reply to you and not for any other purpose. If you do not give a valid email, we will not be able to reply to you.
Send message
</excerpt>

## Search 7
query: "ourworldindata gdp-per-capita-maddison-project-database.csv"
<excerpt title="Gross domestic product (GDP)">
# Gross domestic product (GDP)2022
## Related charts
### Download
#### Download full data Includes all entities and time points#### Download displayed data Includes only the entities and time points currently visible in the chart


# Gross domestic product (GDP)2022
## Related charts
### Download
#### Data API
Use these URLs to programmatically access this chart's data and configure your requests with the options below.Our documentation provides more informationon how to use the API, and you can find a few code examples below.
Download full data, including all entities and time points
Download only the currently selected data visible in the chart

# Gross domestic product (GDP)2022
## Related charts
### Download
#### Data API
##### Data URL (CSV format)
`https://ourworldindata.org/grapher/gdp-maddison-project-database.csv?v=1&csvType=full&useColumnShortNames=false`

# Gross domestic product (GDP)2022
## Related charts
### Download
#### Data API
##### Metadata URL (JSON format)
`https://ourworldindata.org/grapher/gdp-maddison-project-database.metadata.json?v=1&csvType=full&useColumnShortNames=false`

# Gross domestic product (GDP)2022
## Related charts
### Download
#### Code examples
Examples of how to load this data into different data analysis tools.

# Gross domestic product (GDP)2022
## Related charts
### Download
#### Code examples
##### Excel / Google Sheets
`=IMPORTDATA("https://ourworldindata.org/grapher/gdp-maddison-project-database.csv?v=1&csvType=full&useColumnShortNames=false")`

# Gross domestic product (GDP)2022
## Related charts
### Download
#### Code examples
##### Python with Pandas
```  
import pandas as pd  
import requests

# Fetch the data.  
df = pd.read_csv("https://ourworldindata.org/grapher/gdp-maddison-project-database.csv?v=1&csvType=full&useColumnShortNames=false", storage_options = {'User-Agent': 'Our World In Data data fetch/1.0'})

# Fetch the metadata  
metadata = requests.get("https://ourworldindata.org/grapher/gdp-maddison-project-database.metadata.json?v=1&csvType=full&useColumnShortNames=false").json()  
```

# Gross domestic product (GDP)2022
## Related charts
### Download
#### Code examples
##### R
```  
library(jsonlite)

# Fetch the data  
df <- read.csv("https://ourworldindata.org/grapher/gdp-maddison-project-database.csv?v=1&csvType=full&useColumnShortNames=false")

# Fetch the metadata  
metadata <- fromJSON("https://ourworldindata.org/grapher/gdp-maddison-project-database.metadata.json?v=1&csvType=full&useColumnShortNames=false")  
```

# Gross domestic product (GDP)2022
## Related charts
### Download
#### Code examples
##### Stata
`import delimited "https://ourworldindata.org/grapher/gdp-maddison-project-database.csv?v=1&csvType=full&useColumnShortNames=false", encoding("utf-8") clear`
Leave us feedback
**Have a question?** You may find an answer in **FAQs**.
Message
Your name
Email address Your name and email will only be used to reply to you and not for any other purpose. If you do not give a valid email, we will not be able to reply to you.
Send message
</excerpt>

## Search 8
query: "https://ourworldindata.org/grapher/gdp-per-capita-maddison-project-database.csv"
<excerpt title="untitled">
# GDP per capita 2025
## Select countries and regions
*    - [x]  Laos   $8,873   
*    - [x]  Angola   $8,760   
*    - [x]  Bangladesh   $8,677   
*    - [x]  Nigeria   $8,145   
*    - [x]  Samoa   $7,963   
*    - [x]  Nicaragua   $7,933   
*    - [x]  Kyrgyzstan   $7,878   
*    - [x]  Marshall Islands   $7,660   
*    - [x]  Tonga   $7,413   
*    - [x]  Ghana   $7,358   
*    - [x]  Cambodia   $7,300   
*    - [x]  Djibouti   $7,223   
*    - [x]  Cote d'Ivoire   $7,015   
*    - [x]  Honduras   $6,726   
*    - [x]  Mauritania   $6,559   
*    - [x]  Congo   $6,194   
*    - [x]  Kenya   $5,995   
*    - [x]  Tuvalu   $5,776   
*    - [x]  Pakistan   $5,617   
*    - [x]  Zimbabwe   $5,529   
*    - [x]  Sao Tome and Principe   $5,459   
*    - [x]  Nepal   $5,277   
*    - [x]  Myanmar   $5,137   
*    - [x]  Tajikistan   $5,062   
*    - [x]  Sub-Saharan Africa (WB)   $4,963   
*    - [x]  Cameroon   $4,946   
*    - [x]  Senegal   $4,669   
*    - [x]  Syria   $4,579   
*    - [x]  Papua New Guinea   $4,456
</excerpt>

## Search 9
query: ""Albania" 1985 2022 "GDP per capita" "ourworldindata""
<excerpt title="https://ourworldindata.org/grapher/gdp-per-capita-...">
CSV columns (first row): Entity,Code,Year,GDP per capita,GDP per capita (Annotations)
```
Albania,ALB,1978,3696,
```
```
Albania,ALB,1979,3716,
```
```
Albania,ALB,1980,3741,
```
```
Albania,ALB,1981,3762,
```
```
Albania,ALB,1982,3783,
```
```
Albania,ALB,1983,3805,
```
```
Albania,ALB,1984,3826,
```
```
Albania,ALB,1985,3846,
```
```
Albania,ALB,1986,3870,
```
```
Albania,ALB,1987,3894,
```
```
Albania,ALB,1988,3920,
```
```
Albania,ALB,1989,3948,
```
```
Albania,ALB,1990,3983,
```
```
Albania,ALB,1991,2942.1006,
```
```
Albania,ALB,1992,2841.7651,
```
```
Albania,ALB,1993,3137.024,
```
```
Albania,ALB,1994,3399.7102,
```
```
Albania,ALB,1995,3666.6506,
```
```
Albania,ALB,1996,3965.6853,
```
```
Albania,ALB,1997,3526.9856,
```
</excerpt>

## Search 10
query: ""Albania,ALB,2022" "gdp per capita""
<excerpt title="https://ourworldindata.org/grapher/gdp-per-capita-...">
CSV columns (first row): Entity,Code,Year,GDP per capita,GDP per capita (Annotations)
```
Albania,ALB,2016,10547.255,
```
```
Albania,ALB,2017,10958.307,
```
```
Albania,ALB,2018,11426.92,
```
```
Albania,ALB,2019,11715.307,
```
```
Albania,ALB,2020,11372.541,
```
```
Albania,ALB,2021,12455.917,
```
```
Albania,ALB,2022,12978.101,
```
```
Algeria,DZA,1820,685,
```
```
Algeria,DZA,1870,1140,
```
```
Algeria,DZA,1913,1854,
```
```
Algeria,DZA,1950,2176,
```
```
Algeria,DZA,1951,2147,
```
```
Algeria,DZA,1952,2193,
```
```
Algeria,DZA,1953,2182,
```
```
Algeria,DZA,1954,2291,
```
```
Algeria,DZA,1955,2303,
```
```
Algeria,DZA,1956,2475,
```
```
Algeria,DZA,1957,2699,
```
```
Algeria,DZA,1958,2740,
```
```
Algeria,DZA,1959,3178,
```
```
Algeria,DZA,1960,3328,
```
</excerpt>

# Example 3
## Question
out of the artists who participated in the 2023 The Art of Texas State Parks traveling art exhibit, which ones were from austin texas?

## Expected answer
Fidencio Duran, Malou Flato, Gordon Fowler, Terri Wells

## Final answer — grade 1.00
According to the roster of artists released by the Texas Parks & Wildlife Department for the 2023 traveling “The Art of Texas State Parks” exhibit, the following participants are identified as being based in **Austin, Texas**:

| Artist | City of Residence (per release) |
|--------|---------------------------------|
| Fidencio Duran | Austin |
| Malou Flato | Austin |
| Gordon Fowler | Austin |
| Terri Wells | Austin |

These four names are the only ones listed with “Austin” as their location in the official artist lineup for the 2023 exhibit. Sources:

- The TPWD news release (Jan. 3 2023) lists the participating artists and shows “Fidencio Duran (Austin)”, “Malou Flato (Austin)”, “Gordon Fowler (Austin)” and “Terri Wells (Austin)”【5†L91-L108】.
(5 searches; ended: answered)

## Search 1
query: "2023 The Art of Texas State Parks traveling art exhibit artists Austin Texas"
<excerpt title="Traveling Art Exhibit Honors 100 Years of Texas State Parks - TPWD">
## Jan. 3, 2023
### Media Contact: [TPWD News](mailto:news@tpwd.texas.gov "TPWD News"),Business Hours, 512-389-8030
_The Art of Texas State Parks_ is intended to increase public awareness of Texas parklands and heighten their popular appeal through the elegant and inspired works of Texas’ contemporary painters. The national park system has long collaborated with artists to portray their landscapes, but until now, no such artistic record had been undertaken for state parks. The Centennial Celebration of Texas State Parks offers the perfect occasion to create a lasting visual record of Texas State Parks in art and, at the same time, memorialize the past and ongoing development of the distinctive collection of Lone Star parks and natural areas.
Participating artists include:**Randy Bacon** (Abilene); **Mary Baxter** (Marfa); **David Caton** (Utopia); **Charles Criner** (Houston); **Margie Crisp** (Elgin); **Ric Dentinger** (San Antonio/Santa Fe NM); **Fidencio Duran** (Austin); **Janet Eager Krueger** (Encinal); **Joel Edwards** (Waco); **Malou Flato** (Austin); **Gordon Fowler** (Austin); **Pat Gabriel** (Fort Worth); **David****Griffin** (Lubbock/ Dallas); **Brian Grimm** (Fredericksburg); **Clemente Guzman** (San Antonio); **Karl E. Hall** (Houston); **John Austin Hanna** (Fredericksburg); **Billy Hassell** (Fort Worth); **Hailey Herrera** (Bryan); **Lee Jamison** (Huntsville); **Denise Mahlke** (Whitehouse); **Jim Malone** (Fort Worth); **Talmage Minter** (Waco); **William Montgomery** (Elgin); **Kermit Oliver** (Waco); **Noe Perez** (Corpus Christi); **Jeri Salter** (Hutto); **Jim****Stoker** (San Antonio); **Bob Stuth-Wade** (Dublin); and **Terri Wells** (Austin).

## Jan. 3, 2023
### Media Contact: [TPWD News](mailto:news@tpwd.texas.gov "TPWD News"),Business Hours, 512-389-8030
The exhibit will travel to the Houston Museum of Natural Science in late May and can be viewed May 26 – Oct. 1. It will then be exhibited at the Panhandle Plains Museum in Canyon from Oct. 27 – Feb. 18, 2024. The exhibit will also be displayed in 2024 in College Station, Albany and Tyler. The commemorative book is available online through several sources, including Texas A&M Press, the Bullock Museum Store and Amazon.
“It was a real pleasure to see the passion these artists brought to this project, and we’re thrilled these works will be on display at prestigious museums across Texas,” said Andrew Sansom, co-author of the commemorative book and founder of the Meadows Center for Water and the Environment at Texas State University. “It is our fervent hope that these works of art will inspire present and future generations of Texans to forever appreciate and protect their parks.”
Along with _The Art of Texas State Parks_, Texas Parks and Wildlife Foundation is partnering with TPWD to celebrate Texas State Parks all year long. H-E-B, the presenting sponsor of the Centennial Celebration, donated $1 million to help Texas State Parks engage all Texans in discovering and exploring their parks. For more information on the Centennial Celebration, including special community events at all 89 state parks, the history of Texas State Parks and how to make a day visit or overnight reservation, visit TexasStateParks.org/100years.
</excerpt>

## Search 2
query: ""The Art of Texas State Parks" participating artists list Austin""
<excerpt title="Articles">
## The Art of Texas Parks | Exhibition & Sale Benefiting Texas Parks and Wildlife Foundation
Over the past several years, thirty contemporary artists across Texas were invited to participate in the project and to paint designated state park sites. These “Centennial Artists” were assigned specific state parks to paint; however, their stylistic preference, subject matter, and composition vary significantly at the discretion of the artist. From these submitted works, paintings were selected for inclusion in the upcoming book publication from Texas A&M University Press, the 2023 traveling museum exhibition (to be held at the Bullock Texas State History Museum, Austin; Houston Museum of Natural Science, and Witte Museum, San Antonio), and/or gallery exhibition and benefit sale at Foltz Fine Art in Summer 2022.
Out of the selected works, 30 paintings will be offered at a fixed-price sale this Spring through Foltz Fine Art as they host **_The Art of Texas Parks_**Pop-Up Exhibition & Sale Benefitting Texas Parks and Wildlife Foundation.Twenty-five percent of the profits from the sale of the paintings will go to the Texas Parks and Wildlife Foundation.

## The Art of Texas Parks | Exhibition & Sale Benefiting Texas Parks and Wildlife Foundation
Participating “Centennial Artists” include: **Randy Bacon** (Abilene); **Mary Baxter** (Marfa); **David Caton** (Utopia); **Charles Criner** (Houston); **Margie Crisp** (Elgin); **Ric Dentinger** (San Antonio); **Fidencio Duran** (Austin); **Janet Eager Krueger** (Ensinal); **Joel Edwards** (Waco); **Malou Flato** (Austin); **Gordon Fowler** (Austin); **Pat Gabriel** (Fort Worth); **David****Griffin** (Lubbock/ Dallas); **Brian Grimm** (Fredericksburg); **Clemente Guzman** (San Antonio); **Karl E. Hall**(Houston); **John Hanna** (Fredericksburg); **Billy Hassell** (Fort Worth); **Hailey Herrerra** (Bryan); **Lee Jamison**(Huntsville); **Denise Mahlke** (Whitehouse); **Jim Malone** (Fort Worth); **Talmage Minter** (Waco); **William Montgomery**(Elgin); **Kermit Oliver** (Waco); **Noe Perez** (Corpus Christi); **Jeri Salter** (Lago Vista); **Jim****Stoker** (San Antonio); **Bob Stuth-Wade** (Dublin); and **Terri Wells** (Austin).
The exhibition will be on view in their Houston gallery from July 15–August 27, 2022, with a closing reception with Texas Parks & Wildlife Foundation held on Thursday, August 18th, from 5:30-7:30pm. Many of the artists and authors involved with the project will be in attendance. The online exhibition component will be available from July 1 – August 31, 2022. For those interested in supporting Texas Parks and Wildlife Foundation, this is a unique opportunity to preview and purchase works celebrating the upcoming centennial for Texas State Parks.
To learn more about the "Centennial Artists", please visit:https://foltzgallery.com/texas-parks-centennial-artists
Read More
</excerpt>

## Search 3
query: ""The Art of Texas State Parks" "Austin" artists list""
<excerpt title="Articles">
## Traveling Art Exhibit Honors 100 Years of Texas State Parks
Participating artists include:**Randy Bacon** (Abilene); **Mary Baxter** (Marfa); **David Caton** (Utopia); **Charles Criner** (Houston); **Margie Crisp** (Elgin); **Ric Dentinger** (San Antonio/Santa Fe NM); **Fidencio Duran** (Austin); **Janet Eager Krueger** (Encinal); **Joel Edwards** (Waco); **Malou Flato** (Austin); **Gordon Fowler** (Austin); **Pat Gabriel** (Fort Worth); **David****Griffin** (Lubbock/ Dallas); **Brian Grimm** (Fredericksburg); **Clemente Guzman** (San Antonio); **Karl E. Hall** (Houston); **John Austin Hanna** (Fredericksburg); **Billy Hassell** (Fort Worth); **Hailey Herrera** (Bryan); **Lee Jamison** (Huntsville); **Denise Mahlke** (Whitehouse); **Jim Malone** (Fort Worth); **Talmage Minter** (Waco); **William Montgomery** (Elgin); **Kermit Oliver** (Waco); **Noe Perez** (Corpus Christi); **Jeri Salter** (Hutto); **Jim****Stoker** (San Antonio); **Bob Stuth-Wade** (Dublin); and **Terri Wells** (Austin).
The exhibit will travel to the Houston Museum of Natural Science in late May and can be viewed May 26 – Oct. 1. It will then be exhibited at the Panhandle Plains Museum in Canyon from Oct. 27 – Feb. 18, 2024. The exhibit will also be displayed in 2024 in College Station, Albany and Tyler. The commemorative book is available online through several sources, including **Texas A&M Press**, the **Bullock Museum Store** and **Amazon.**

## Traveling Art Exhibit Honors 100 Years of Texas State Parks
“It was a real pleasure to see the passion these artists brought to this project, and we’re thrilled these works will be on display at prestigious museums across Texas,” said Andrew Sansom, co-author of the commemorative book and founder of the Meadows Center for Water and the Environment at Texas State University. “It is our fervent hope that these works of art will inspire present and future generations of Texans to forever appreciate and protect their parks.”
Along with _The Art of Texas State Parks_, Texas Parks and Wildlife Foundation is partnering with TPWD to celebrate Texas State Parks all year long. H-E-B, the presenting sponsor of the Centennial Celebration, donated $1 million to help Texas State Parks engage all Texans in discovering and exploring their parks. For more information on the Centennial Celebration, including special community events at all 89 state parks, the history of Texas State Parks and how to make a day visit or overnight reservation, visit **TexasStateParks.org/100years**.
Read More
Hailey Herrera 10/10/22 Hailey Herrera 10/10/22
</excerpt>

## Search 4
query: "site:tpwd.texas.gov "The Art of Texas State Parks" Austin"
<excerpt title="Traveling Art Exhibit Honors 100 Years of Texas State Parks - TPWD">
## Jan. 3, 2023
### Media Contact: [TPWD News](mailto:news@tpwd.texas.gov "TPWD News"),Business Hours, 512-389-8030
News ImageShare on FacebookShare Release URL
_**The Art of Texas State Parks to be held at Bullock Museum Jan. 7 - April 30**_
**Note: This item is more than three years old.** Please take the publication date into consideration for any date references.
AUSTIN— In honor of the Centennial Celebration of Texas State Parks, the Bullock Texas State History Museum will host a new traveling art exhibit Jan. 7 — April 30. “The Art of Texas State Parks” is a visual arts survey of state parks featuring more than 30 parks by some of Texas’ most celebrated artists. The exhibit will travel to several museums later this year, including the Houston Museum of Natural Science and the Panhandle Plains Museum in Canyon.
Along with the traveling exhibit, the project also includes a commemorative book published by Texas A&M Press. Proceeds from book sales and the sale of the artwork through Foltz Fine Art in Houston will be donated to Texas Parks and Wildlife Foundation to benefit Texas State Parks.
The project was several years in the making. In anticipation of the 2023 Centennial Celebration of Texas State Parks, Texas Parks and Wildlife Foundation partnered with Texas Parks and Wildlife Department (TPWD), the Meadows Center for Water and the Environment at Texas State University, and the Bullock Texas State History Museum to present _The Art of Texas State Parks_. Thirty notable Texas artists were commissioned to create works celebrating parks across Texas. Additional support for the project is provided by H-E-B, presenting sponsor for the Texas State Parks Centennial Celebration.
“We are grateful for the partnership that is bringing _The Art of Texas State Parks_ to museums across Texas, spreading the message about these natural treasures that belong to us all,” said TPWD Executive Director David Yoskowitz, Ph.D.

## Jan. 3, 2023
### Media Contact: [TPWD News](mailto:news@tpwd.texas.gov "TPWD News"),Business Hours, 512-389-8030
_The Art of Texas State Parks_ is intended to increase public awareness of Texas parklands and heighten their popular appeal through the elegant and inspired works of Texas’ contemporary painters. The national park system has long collaborated with artists to portray their landscapes, but until now, no such artistic record had been undertaken for state parks. The Centennial Celebration of Texas State Parks offers the perfect occasion to create a lasting visual record of Texas State Parks in art and, at the same time, memorialize the past and ongoing development of the distinctive collection of Lone Star parks and natural areas.
Participating artists include:**Randy Bacon** (Abilene); **Mary Baxter** (Marfa); **David Caton** (Utopia); **Charles Criner** (Houston); **Margie Crisp** (Elgin); **Ric Dentinger** (San Antonio/Santa Fe NM); **Fidencio Duran** (Austin); **Janet Eager Krueger** (Encinal); **Joel Edwards** (Waco); **Malou Flato** (Austin); **Gordon Fowler** (Austin); **Pat Gabriel** (Fort Worth); **David****Griffin** (Lubbock/ Dallas); **Brian Grimm** (Fredericksburg); **Clemente Guzman** (San Antonio); **Karl E. Hall** (Houston); **John Austin Hanna** (Fredericksburg); **Billy Hassell** (Fort Worth); **Hailey Herrera** (Bryan); **Lee Jamison** (Huntsville); **Denise Mahlke** (Whitehouse); **Jim Malone** (Fort Worth); **Talmage Minter** (Waco); **William Montgomery** (Elgin); **Kermit Oliver** (Waco); **Noe Perez** (Corpus Christi); **Jeri Salter** (Hutto); **Jim****Stoker** (San Antonio); **Bob Stuth-Wade** (Dublin); and **Terri Wells** (Austin).
</excerpt>

## Search 5
query: ""Fidencio Duran" "Austin" "The Art of Texas State Parks""
<excerpt title="Traveling Art Exhibit Honoring 100 Years of Texas State Parks Moves ...">
## Oct. 26, 2023
### Media Contact: [TPWD News](mailto:news@tpwd.texas.gov "TPWD News"),Business Hours, 512-389-8030
_The Art of Texas State Parks_ is intended to increase public awareness of Texas parklands and heighten their popular appeal through the elegant and inspired works of Texas’ best contemporary painters. While the national park system has benefitted from their chroniclers in art, no such artistic record has yet been undertaken for state parks. The Centennial Celebration of Texas State Parks offers the perfect occasion to create a lasting visual record of Texas State Parks in art and, at the same time, memorialize the past and ongoing development of the distinctive collection of Lone Star parks and natural areas.
Participating artists include:**Randy Bacon** (Abilene); **Mary Baxter** (Marfa); **David Caton** (Utopia); **Charles Criner** (Houston); **Margie Crisp** (Elgin); **Ric Dentinger** (San Antonio/Santa Fe NM); **Fidencio Duran** (Austin); **Janet Eager Krueger** (Encinal); **Joel Edwards** (Waco); **Malou Flato** (Austin); **Gordon Fowler** (Austin); **Pat Gabriel** (Fort Worth); **David****Griffin** (Lubbock/ Dallas); **Brian Grimm** (Fredericksburg); **Clemente Guzman** (San Antonio); **Karl E. Hall** (Houston); **John Austin Hanna** (Fredericksburg); **Billy Hassell** (Fort Worth); **Hailey Herrera** (Bryan); **Lee Jamison** (Huntsville); **Denise Mahlke** (Whitehouse); **Jim Malone** (Fort Worth); **Talmage Minter** (Waco); **William Montgomery** (Elgin); **Kermit Oliver** (Waco); **Noe Perez** (Corpus Christi); **Jeri Salter** (Hutto); **Jim****Stoker** (San Antonio); **Bob Stuth-Wade** (Dublin); and **Terri Wells** (Austin).

## Oct. 26, 2023
### Media Contact: [TPWD News](mailto:news@tpwd.texas.gov "TPWD News"),Business Hours, 512-389-8030
The exhibit can be seen at the Panhandle Plains Museum in Canyon from Oct. 27 – Feb. 18, 2024. The exhibit will then move to Stark Galleries at Texas A&M University in College Station March 21 – May 26, 2024; The Old Jail Museum in Albany June 8 – Aug. 31, 2024 and the Tyler Museum of Art in Tyler: Sept. 22 – Jan. 5, 2025. The commemorative book is available online through several sources, including Texas A&M Press and Amazon.
“It was a real pleasure to see the passion these artists brought to this project, and we’re thrilled these works will be on display at prestigious museums across Texas,” said Andrew Sansom, co-author of the commemorative book and founder of the Meadows Center for Water and the Environment at Texas State University. “It is our fervent hope that these works of art will inspire present and future generations of Texans to forever appreciate and protect their parks.”
Along with _The Art of Texas State Parks_, Texas Parks and Wildlife Foundation is partnering with TPWD to celebrate Texas State Parks all year long. H-E-B, the presenting sponsor of the Centennial Celebration, donated $1 million to help Texas State Parks engage all Texans in discovering and exploring their parks. For more information on the Centennial Celebration, including special community events at all Texas State Parks, the history of Texas State Parks and how to make a day visit or overnight reservation, visit TexasStateParks.org/100years.
* * *
**Image Captions**
Link to DropBox with image files:
**_https://www.dropbox.com/sh/v86yetpm58croyo/AAABAR3kahuXpwNSBe-hSOzka?dl=0_**
</excerpt>

# Example 4
## Question
I’m looking for good universities. From the Guardian University Guide 2022, which of the top 50 universities have an overall course satisfaction score of 80 or higher, a continuation score of 95 or higher, and a student-to-staff ratio of 15 or less?

## Expected answer
St Andrews, London School of Economics, Durham, Warwick, Imperial College, Loughborough, Lancaster, Southampton, York, Sheffield, Liverpool, Keele

## Final answer — grade 0.40
**Universities from the Guardian University Guide 2022 (Top 50) that meet all three criteria**

| University | Overall course satisfaction | First‑year continuation | Student‑to‑staff ratio | Source |
|------------|-----------------------------|------------------------|------------------------|---------|
| St Andrews | 93.1 % | 99 % | 11.1 | https://www.theguardian.com/education/ng-interactive/2021/sep/11/the-best-uk-universities-2022-rankings |
| London School of Economics (LSE) | 80.1 % | 97 % | 12.4 | https://www.theguardian.com/education/ng-interactive/2021/sep/11/the-best-uk-universities-2022-rankings |
| Durham | 83.9 % | 97 % | 13.5 | https://www.theguardian.com/education/ng-interactive/2021/sep/11/the-best-uk-universities-2022-rankings |

**Notes**

* The data come from the Guardian’s interactive table for 2022, which lists each university’s “Satisfied with course” (overall course satisfaction), “Continuation” (percentage of first‑year students continuing to year 2), and “Student to staff ratio.”
* These three universities are the only ones for which the evidence shows all three requested thresholds (course satisfaction ≥ 80 %, continuation ≥ 95 %, ratio ≤ 15) are satisfied.
* For the other universities that make up the top 50, the Guardian table does not contain data in the sources accessed in this research, so we cannot confirm whether they meet or fail the criteria.
(10 searches; ended: finalized)

## Search 1
query: "Guardian University Guide 2022 overall course satisfaction student to staff ratio top 50"
<excerpt title="The Guardian University Guide 2023 – the rankings">
Contin-uation Percentage of first-year students continuing to second year 96.3  
12 12Edinburgh81.8 72 80.6 52.4 11.5 8.9 191 6.6 85 97.7  
Satisfied with course The rating for the overall quality of the course, given by final-year students in the latest National Student Survey (NSS), recorded as a percentage 72
Satisfied with teaching The rating for the quality of teaching on the course, given by final-year students in the NSS 80.6
Satisfied with feedback The rating for the quality of feedback and assessment, given by final-year students in the NSS 52.4
Student to staff ratio Number of students per member of teaching staff 11.5
Spend per student/10 Money spent on each student, excluding academic staff costs, given as a rating out of 10 8.9
Average entry tariff Typical Ucas scores of young entrants (under 21) to the department 191
Value added score/10 This score compares students’ degree results with their entry qualifications, to show how effectively they are taught. It is given as a rating out of 10 6.6
Career after 15 months Percentage of graduates who find graduate-level jobs, or are in further study at professional or HE level, within 15 months of graduation 85
Contin-uation Percentage of first-year students continuing to second year 97.7  
13 20Aberdeen81.2 85.2 85.3 67.4 15 4.7 187 7.8 82 96.4  
Satisfied with course The rating for the overall quality of the course, given by final-year students in the latest National Student Survey (NSS), recorded as a percentage 85.2
Satisfied with teaching The rating for the quality of teaching on the course, given by final-year students in the NSS 85.3
Satisfied with feedback The rating for the quality of feedback and assessment, given by final-year students in the NSS 67.4
Student to staff ratio Number of students per member of teaching staff 15

Spend per student/10 Money spent on each student, excluding academic staff costs, given as a rating out of 10 4.7
Average entry tariff Typical Ucas scores of young entrants (under 21) to the department 187
Value added score/10 This score compares students’ degree results with their entry qualifications, to show how effectively they are taught. It is given as a rating out of 10 7.8
Career after 15 months Percentage of graduates who find graduate-level jobs, or are in further study at professional or HE level, within 15 months of graduation 82
Contin-uation Percentage of first-year students continuing to second year 96.4  
14 13Lancaster80 83.1 84.1 66 14.8 7.6 150 5.3 84 97.8  
Satisfied with course The rating for the overall quality of the course, given by final-year students in the latest National Student Survey (NSS), recorded as a percentage 83.1
Satisfied with teaching The rating for the quality of teaching on the course, given by final-year students in the NSS 84.1
Satisfied with feedback The rating for the quality of feedback and assessment, given by final-year students in the NSS 66
Student to staff ratio Number of students per member of teaching staff 14.8
Spend per student/10 Money spent on each student, excluding academic staff costs, given as a rating out of 10 7.6
Average entry tariff Typical Ucas scores of young entrants (under 21) to the department 150
Value added score/10 This score compares students’ degree results with their entry qualifications, to show how effectively they are taught. It is given as a rating out of 10 5.3
Career after 15 months Percentage of graduates who find graduate-level jobs, or are in further study at professional or HE level, within 15 months of graduation 84
</excerpt>

## Search 2
query: ""Guardian University Guide 2022" "top 50""
<excerpt title="About the University - Chief Financial Officer">
## About the University of Exeter
#### The University of Exeter combines world-class research and education with an outstanding student experience. We welcome over 30,000 students from more than 150 countries to our four campuses: Streatham and St Luke’s in Exeter (Devon), and Penryn and Truro in Cornwall.

Our success is built upon strong foundations of leadership, governance and management, and a sector-leading partnership with our students. We have University-wide institutes and research groups that are highly interdisciplinary. While we are one community, each campus has its own unique identity.
Formed in 1955, we are a member of the Russell Group, which comprises the UK’s leading research-intensive universities. We are proud of our achievements but we remain ambitious for the future. The University of Exeter has gone from strength to strength becoming the UK’s fastest rising research university over the past decade.
The Resear ch Excellence Framework (REF) 2021 review showed that we are doing more research, of better quality, with a bigger impact on the world than ever before. Our world-leading research impact grew more than any other Russell Group university, more than 99 per cent of our research was rated of international quality◇ and 12 of our subjects were in the Top 1 0 for world-leading impact.†
The National Student Survey (NSS) 2022 showed that we have the highest level of student satisfaction in the Russell Group.
In January 2022, Exeter appeared for the first time in the Times Higher Education (THE) Most International Universities in the World Ranking. The University ranked 46th in the world and 13th in the UK out of 193 global institutions.
We are the Russell Group’s number one provider of degree apprenticeships and have a long history of working in partnership with business. Since 2016, we have worked hard with our partners to develop programmes that meet specific business needs and address crucial skills gaps. Today, we partner with more than 200 employers from across the UK and have over 1,400 apprentices learning with us.
◇ Research rated 4* + 3* + 2* in REF 2021.
† Based on ranking for 4* impact in REF 2021.

## About the University of Exeter
#### The University of Exeter combines world-class research and education with an outstanding student experience. We welcome over 30,000 students from more than 150 countries to our four campuses: Streatham and St Luke’s in Exeter (Devon), and Penryn and Truro in Cornwall.
Top 150 in the Times Higher Education (THE) World University Rankings 2022.
Top 50 in the Times Higher Education (THE)Impact Rankings 2022*.
Top 50 in the Times Higher Education (THE) Most International Universities in the World 2022.
Top 15 in the Guardian University Guide 2022 and The Times and The Sunday Times Good University Guide 2023.
99.3%of our research is rated of international quality◇ in REF 2021 with 12 of our subjects in the Top 10 for world-leading impact.†
◇ Research rated 4* + 3* + 2* in REF 2021.
† Based on ranking for 4* impact in REF 2021.
* The THE Impact Rankings assess universities against the United Nations’ Sustainable Development Goals (SDGs).
30,000 students from more than 150 countries.
In touch with over 155,000 alumni in 183 countries.
6,700 staff from more than 100 countries.
A world-class, research-intensive University.
Runner-up for the University of the Year award in The Times and The Sunday Times Good University Guide 2023.

## About the University of Exeter
#### Strategy 2030
</excerpt>

## Search 3
query: "Guardian University Guide 2022 top 50 table overall course satisfaction continuation student to staff ratio"
<excerpt title="The Guardian University Guide 2026 – the rankings">
Value added score/10 This score compares students’ degree results with their entry qualifications, to show how effectively they are taught. It is given as a rating out of 10 5.9
Career after 15 months Percentage of graduates who find graduate-level jobs, or are in further study at professional or HE level, within 15 months of graduation 93
Contin-uation Percentage of first-year students continuing to second year 96.4  
5 6 Durham 85.5 90.5 81.6 12.4 6.4 180 6 89 96.7  
Satisfied with teaching The rating for the quality of teaching on the course, given by final-year students in the NSS 90.5
Satisfied with feedback The rating for the quality of feedback and assessment, given by final-year students in the NSS 81.6
Student to staff ratio Number of students per member of teaching staff 12.4
Spend per student/10 Money spent on each student, excluding academic staff costs, given as a rating out of 10 6.4
Average entry tariff Typical Ucas scores of young entrants (under 21) to the department 180
Value added score/10 This score compares students’ degree results with their entry qualifications, to show how effectively they are taught. It is given as a rating out of 10 6
Career after 15 months Percentage of graduates who find graduate-level jobs, or are in further study at professional or HE level, within 15 months of graduation 89
Contin-uation Percentage of first-year students continuing to second year 96.7  
6 5 Imperial College 82.9 87.7 67.3 11.7 8.7 196 6.1 95 94.9  
Satisfied with teaching The rating for the quality of teaching on the course, given by final-year students in the NSS 87.7
Satisfied with feedback The rating for the quality of feedback and assessment, given by final-year students in the NSS 67.3
Student to staff ratio Number of students per member of teaching staff 11.7
</excerpt>

## Search 4
query: ""the-guardian-university-guide-2022" "ng-interactive""
<excerpt title="The Guardian University Guide 2022 – the rankings">
Value added score/10 This score compares students’ degree results with their entry qualifications, to show how effectively they are taught. It is given as a rating out of 10 6.7
Career after 15 months Percentage of graduates who find graduate-level jobs, or are in further study at professional or HE level, within fifteen months of graduation 93
Contin-uation Percentage of first-year students continuing to second year 99  
3 2St Andrews96.8 93.1 92.3 79.6 11.1 7.3 207 5.6 84 97  
Satisfied with course The rating for the overall quality of the course, given by final-year students in the latest National Student Survey (NSS), recorded as a percentage 93.1
Satisfied with teaching The rating for the quality of teaching on the course, given by final-year students in the NSS 92.3
Satisfied with feedback The rating for the quality of feedback and assessment, given by final-year students in the NSS 79.6
Student to staff ratio Number of students per member of teaching staff 11.1
Spend per student/10 Money spent on each student, excluding academic staff costs, given as a rating out of 10 7.3
Average entry tariff Typical Ucas scores of young entrants (under 21) to the department 207
Value added score/10 This score compares students’ degree results with their entry qualifications, to show how effectively they are taught. It is given as a rating out of 10 5.6
Career after 15 months Percentage of graduates who find graduate-level jobs, or are in further study at professional or HE level, within fifteen months of graduation 84
Contin-uation Percentage of first-year students continuing to second year 97  
4 5London School of Economics91.6 80.1 83.1 70.2 12.4 8.7 175 6.9 93 97  
Satisfied with course The rating for the overall quality of the course, given by final-year students in the latest National Student Survey (NSS), recorded as a percentage 80.1

Satisfied with teaching The rating for the quality of teaching on the course, given by final-year students in the NSS 83.1
Satisfied with feedback The rating for the quality of feedback and assessment, given by final-year students in the NSS 70.2
Student to staff ratio Number of students per member of teaching staff 12.4
Spend per student/10 Money spent on each student, excluding academic staff costs, given as a rating out of 10 8.7
Average entry tariff Typical Ucas scores of young entrants (under 21) to the department 175
Value added score/10 This score compares students’ degree results with their entry qualifications, to show how effectively they are taught. It is given as a rating out of 10 6.9
Career after 15 months Percentage of graduates who find graduate-level jobs, or are in further study at professional or HE level, within fifteen months of graduation 93
Contin-uation Percentage of first-year students continuing to second year 97  
5 4Durham86.5 83.9 84.8 69.5 13.5 6.5 182 6.7 89 97  
Satisfied with course The rating for the overall quality of the course, given by final-year students in the latest National Student Survey (NSS), recorded as a percentage 83.9
Satisfied with teaching The rating for the quality of teaching on the course, given by final-year students in the NSS 84.8
Satisfied with feedback The rating for the quality of feedback and assessment, given by final-year students in the NSS 69.5
Student to staff ratio Number of students per member of teaching staff 13.5
Spend per student/10 Money spent on each student, excluding academic staff costs, given as a rating out of 10 6.5
Average entry tariff Typical Ucas scores of young entrants (under 21) to the department 182
Value added score/10 This score compares students’ degree results with their entry qualifications, to show how effectively they are taught. It is given as a rating out of 10 6.7
</excerpt>

## Search 5
query: "the-best-uk-universities-2022-rankings guardian table st occurrence"
<excerpt title="The Guardian University Guide 2022 – the rankings">
Value added score/10 This score compares students’ degree results with their entry qualifications, to show how effectively they are taught. It is given as a rating out of 10 6.7
Career after 15 months Percentage of graduates who find graduate-level jobs, or are in further study at professional or HE level, within fifteen months of graduation 93
Contin-uation Percentage of first-year students continuing to second year 99  
3 2St Andrews96.8 93.1 92.3 79.6 11.1 7.3 207 5.6 84 97  
Satisfied with course The rating for the overall quality of the course, given by final-year students in the latest National Student Survey (NSS), recorded as a percentage 93.1
Satisfied with teaching The rating for the quality of teaching on the course, given by final-year students in the NSS 92.3
Satisfied with feedback The rating for the quality of feedback and assessment, given by final-year students in the NSS 79.6
Student to staff ratio Number of students per member of teaching staff 11.1
Spend per student/10 Money spent on each student, excluding academic staff costs, given as a rating out of 10 7.3
Average entry tariff Typical Ucas scores of young entrants (under 21) to the department 207
Value added score/10 This score compares students’ degree results with their entry qualifications, to show how effectively they are taught. It is given as a rating out of 10 5.6
Career after 15 months Percentage of graduates who find graduate-level jobs, or are in further study at professional or HE level, within fifteen months of graduation 84
Contin-uation Percentage of first-year students continuing to second year 97  
4 5London School of Economics91.6 80.1 83.1 70.2 12.4 8.7 175 6.9 93 97  
Satisfied with course The rating for the overall quality of the course, given by final-year students in the latest National Student Survey (NSS), recorded as a percentage 80.1

Satisfied with teaching The rating for the quality of teaching on the course, given by final-year students in the NSS 83.1
Satisfied with feedback The rating for the quality of feedback and assessment, given by final-year students in the NSS 70.2
Student to staff ratio Number of students per member of teaching staff 12.4
Spend per student/10 Money spent on each student, excluding academic staff costs, given as a rating out of 10 8.7
Average entry tariff Typical Ucas scores of young entrants (under 21) to the department 175
Value added score/10 This score compares students’ degree results with their entry qualifications, to show how effectively they are taught. It is given as a rating out of 10 6.9
Career after 15 months Percentage of graduates who find graduate-level jobs, or are in further study at professional or HE level, within fifteen months of graduation 93
Contin-uation Percentage of first-year students continuing to second year 97  
5 4Durham86.5 83.9 84.8 69.5 13.5 6.5 182 6.7 89 97  
Satisfied with course The rating for the overall quality of the course, given by final-year students in the latest National Student Survey (NSS), recorded as a percentage 83.9
Satisfied with teaching The rating for the quality of teaching on the course, given by final-year students in the NSS 84.8
Satisfied with feedback The rating for the quality of feedback and assessment, given by final-year students in the NSS 69.5
Student to staff ratio Number of students per member of teaching staff 13.5
Spend per student/10 Money spent on each student, excluding academic staff costs, given as a rating out of 10 6.5
Average entry tariff Typical Ucas scores of young entrants (under 21) to the department 182
Value added score/10 This score compares students’ degree results with their entry qualifications, to show how effectively they are taught. It is given as a rating out of 10 6.7
</excerpt>

## Search 6
query: "the-best-uk-universities-2022-rankings guardian table 2022 university overall course satisfaction continuation student to staff ratio top 50"
<excerpt title="The Guardian University Guide 2023 – the rankings">
Contin-uation Percentage of first-year students continuing to second year 96.3  
12 12Edinburgh81.8 72 80.6 52.4 11.5 8.9 191 6.6 85 97.7  
Satisfied with course The rating for the overall quality of the course, given by final-year students in the latest National Student Survey (NSS), recorded as a percentage 72
Satisfied with teaching The rating for the quality of teaching on the course, given by final-year students in the NSS 80.6
Satisfied with feedback The rating for the quality of feedback and assessment, given by final-year students in the NSS 52.4
Student to staff ratio Number of students per member of teaching staff 11.5
Spend per student/10 Money spent on each student, excluding academic staff costs, given as a rating out of 10 8.9
Average entry tariff Typical Ucas scores of young entrants (under 21) to the department 191
Value added score/10 This score compares students’ degree results with their entry qualifications, to show how effectively they are taught. It is given as a rating out of 10 6.6
Career after 15 months Percentage of graduates who find graduate-level jobs, or are in further study at professional or HE level, within 15 months of graduation 85
Contin-uation Percentage of first-year students continuing to second year 97.7  
13 20Aberdeen81.2 85.2 85.3 67.4 15 4.7 187 7.8 82 96.4  
Satisfied with course The rating for the overall quality of the course, given by final-year students in the latest National Student Survey (NSS), recorded as a percentage 85.2
Satisfied with teaching The rating for the quality of teaching on the course, given by final-year students in the NSS 85.3
Satisfied with feedback The rating for the quality of feedback and assessment, given by final-year students in the NSS 67.4
Student to staff ratio Number of students per member of teaching staff 15

Spend per student/10 Money spent on each student, excluding academic staff costs, given as a rating out of 10 4.7
Average entry tariff Typical Ucas scores of young entrants (under 21) to the department 187
Value added score/10 This score compares students’ degree results with their entry qualifications, to show how effectively they are taught. It is given as a rating out of 10 7.8
Career after 15 months Percentage of graduates who find graduate-level jobs, or are in further study at professional or HE level, within 15 months of graduation 82
Contin-uation Percentage of first-year students continuing to second year 96.4  
14 13Lancaster80 83.1 84.1 66 14.8 7.6 150 5.3 84 97.8  
Satisfied with course The rating for the overall quality of the course, given by final-year students in the latest National Student Survey (NSS), recorded as a percentage 83.1
Satisfied with teaching The rating for the quality of teaching on the course, given by final-year students in the NSS 84.1
Satisfied with feedback The rating for the quality of feedback and assessment, given by final-year students in the NSS 66
Student to staff ratio Number of students per member of teaching staff 14.8
Spend per student/10 Money spent on each student, excluding academic staff costs, given as a rating out of 10 7.6
Average entry tariff Typical Ucas scores of young entrants (under 21) to the department 150
Value added score/10 This score compares students’ degree results with their entry qualifications, to show how effectively they are taught. It is given as a rating out of 10 5.3
Career after 15 months Percentage of graduates who find graduate-level jobs, or are in further study at professional or HE level, within 15 months of graduation 84
</excerpt>

## Search 7
query: "the-best-uk-universities-2022-rankings guardian interactive table""
<excerpt title="The Guardian University Guide 2022 – the rankings">
Value added score/10 This score compares students’ degree results with their entry qualifications, to show how effectively they are taught. It is given as a rating out of 10 6.7
Career after 15 months Percentage of graduates who find graduate-level jobs, or are in further study at professional or HE level, within fifteen months of graduation 93
Contin-uation Percentage of first-year students continuing to second year 99  
3 2St Andrews96.8 93.1 92.3 79.6 11.1 7.3 207 5.6 84 97  
Satisfied with course The rating for the overall quality of the course, given by final-year students in the latest National Student Survey (NSS), recorded as a percentage 93.1
Satisfied with teaching The rating for the quality of teaching on the course, given by final-year students in the NSS 92.3
Satisfied with feedback The rating for the quality of feedback and assessment, given by final-year students in the NSS 79.6
Student to staff ratio Number of students per member of teaching staff 11.1
Spend per student/10 Money spent on each student, excluding academic staff costs, given as a rating out of 10 7.3
Average entry tariff Typical Ucas scores of young entrants (under 21) to the department 207
Value added score/10 This score compares students’ degree results with their entry qualifications, to show how effectively they are taught. It is given as a rating out of 10 5.6
Career after 15 months Percentage of graduates who find graduate-level jobs, or are in further study at professional or HE level, within fifteen months of graduation 84
Contin-uation Percentage of first-year students continuing to second year 97  
4 5London School of Economics91.6 80.1 83.1 70.2 12.4 8.7 175 6.9 93 97  
Satisfied with course The rating for the overall quality of the course, given by final-year students in the latest National Student Survey (NSS), recorded as a percentage 80.1

Satisfied with teaching The rating for the quality of teaching on the course, given by final-year students in the NSS 83.1
Satisfied with feedback The rating for the quality of feedback and assessment, given by final-year students in the NSS 70.2
Student to staff ratio Number of students per member of teaching staff 12.4
Spend per student/10 Money spent on each student, excluding academic staff costs, given as a rating out of 10 8.7
Average entry tariff Typical Ucas scores of young entrants (under 21) to the department 175
Value added score/10 This score compares students’ degree results with their entry qualifications, to show how effectively they are taught. It is given as a rating out of 10 6.9
Career after 15 months Percentage of graduates who find graduate-level jobs, or are in further study at professional or HE level, within fifteen months of graduation 93
Contin-uation Percentage of first-year students continuing to second year 97  
5 4Durham86.5 83.9 84.8 69.5 13.5 6.5 182 6.7 89 97  
Satisfied with course The rating for the overall quality of the course, given by final-year students in the latest National Student Survey (NSS), recorded as a percentage 83.9
Satisfied with teaching The rating for the quality of teaching on the course, given by final-year students in the NSS 84.8
Satisfied with feedback The rating for the quality of feedback and assessment, given by final-year students in the NSS 69.5
Student to staff ratio Number of students per member of teaching staff 13.5
Spend per student/10 Money spent on each student, excluding academic staff costs, given as a rating out of 10 6.5
Average entry tariff Typical Ucas scores of young entrants (under 21) to the department 182
Value added score/10 This score compares students’ degree results with their entry qualifications, to show how effectively they are taught. It is given as a rating out of 10 6.7
</excerpt>

## Search 8
query: ""University of Oxford" "overall course satisfaction" "Guardian University Guide 2022""
(no page could be read; nothing was passed on)

## Search 9
query: "the-best-uk-universities-2022-rankings guardian interactive table universities 1-50"
<excerpt title="The Guardian University Guide 2022 – the rankings">
Value added score/10 This score compares students’ degree results with their entry qualifications, to show how effectively they are taught. It is given as a rating out of 10 6.7
Career after 15 months Percentage of graduates who find graduate-level jobs, or are in further study at professional or HE level, within fifteen months of graduation 93
Contin-uation Percentage of first-year students continuing to second year 99  
3 2St Andrews96.8 93.1 92.3 79.6 11.1 7.3 207 5.6 84 97  
Satisfied with course The rating for the overall quality of the course, given by final-year students in the latest National Student Survey (NSS), recorded as a percentage 93.1
Satisfied with teaching The rating for the quality of teaching on the course, given by final-year students in the NSS 92.3
Satisfied with feedback The rating for the quality of feedback and assessment, given by final-year students in the NSS 79.6
Student to staff ratio Number of students per member of teaching staff 11.1
Spend per student/10 Money spent on each student, excluding academic staff costs, given as a rating out of 10 7.3
Average entry tariff Typical Ucas scores of young entrants (under 21) to the department 207
Value added score/10 This score compares students’ degree results with their entry qualifications, to show how effectively they are taught. It is given as a rating out of 10 5.6
Career after 15 months Percentage of graduates who find graduate-level jobs, or are in further study at professional or HE level, within fifteen months of graduation 84
Contin-uation Percentage of first-year students continuing to second year 97  
4 5London School of Economics91.6 80.1 83.1 70.2 12.4 8.7 175 6.9 93 97  
Satisfied with course The rating for the overall quality of the course, given by final-year students in the latest National Student Survey (NSS), recorded as a percentage 80.1

Satisfied with teaching The rating for the quality of teaching on the course, given by final-year students in the NSS 83.1
Satisfied with feedback The rating for the quality of feedback and assessment, given by final-year students in the NSS 70.2
Student to staff ratio Number of students per member of teaching staff 12.4
Spend per student/10 Money spent on each student, excluding academic staff costs, given as a rating out of 10 8.7
Average entry tariff Typical Ucas scores of young entrants (under 21) to the department 175
Value added score/10 This score compares students’ degree results with their entry qualifications, to show how effectively they are taught. It is given as a rating out of 10 6.9
Career after 15 months Percentage of graduates who find graduate-level jobs, or are in further study at professional or HE level, within fifteen months of graduation 93
Contin-uation Percentage of first-year students continuing to second year 97  
5 4Durham86.5 83.9 84.8 69.5 13.5 6.5 182 6.7 89 97  
Satisfied with course The rating for the overall quality of the course, given by final-year students in the latest National Student Survey (NSS), recorded as a percentage 83.9
Satisfied with teaching The rating for the quality of teaching on the course, given by final-year students in the NSS 84.8
Satisfied with feedback The rating for the quality of feedback and assessment, given by final-year students in the NSS 69.5
Student to staff ratio Number of students per member of teaching staff 13.5
Spend per student/10 Money spent on each student, excluding academic staff costs, given as a rating out of 10 6.5
Average entry tariff Typical Ucas scores of young entrants (under 21) to the department 182
Value added score/10 This score compares students’ degree results with their entry qualifications, to show how effectively they are taught. It is given as a rating out of 10 6.7
</excerpt>

## Search 10
query: "guardian university guide 2022 csv""
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

# Example 5
## Question
Of the natural sites on the UNESCO list of World Heritage in Danger, only a few sites are located in one of the original members of the United Nations. In which country is the site with the largest reported area according to Protected Planet?

## Expected answer
Mexico

## Final answer — grade 0.00
The natural site on the UNESCO List of World Heritage in Danger that has the largest reported area (according to Protected Planet) and lies within an original United Nations founding member is **the United States**—specifically, **Everglades National Park**.
(10 searches; ended: answered)

## Search 1
query: "UNESCO World Heritage in Danger natural sites list"
<excerpt title="List of World Heritage in Danger">
# List of World Heritage in Danger
##### Côte d'Ivoire
*   Mount Nimba Strict Nature Reserve (1992) *

# List of World Heritage in Danger
##### Democratic Republic of the Congo
*   Garamba National Park (1996)   
*   Kahuzi-Biega National Park (1997)   
*   Okapi Wildlife Reserve (1997)   
*   Virunga National Park (1994)

# List of World Heritage in Danger
##### Guinea
*   Mount Nimba Strict Nature Reserve (1992) *

# List of World Heritage in Danger
##### Honduras
*   Río Plátano Biosphere Reserve (2011)

# List of World Heritage in Danger
##### Indonesia
*   Tropical Rainforest Heritage of Sumatra (2011)

# List of World Heritage in Danger
##### Iraq
*   Ashur (Qal'at Sherqat) (2003)   
*   Hatra (2015)   
*   Samarra Archaeological City (2007)

# List of World Heritage in Danger
##### Jerusalem (Site proposed by Jordan)
*   Old City of Jerusalem and its Walls (1982)

# List of World Heritage in Danger
##### Kenya
*   Lake Turkana National Parks (2018)

# List of World Heritage in Danger
##### Lebanon
*   Mount Amel Castles (2026)   
*   Rachid Karami International Fair-Tripoli (2023)   
*   Tyre (2026)

# List of World Heritage in Danger
##### Libya
*   Archaeological Site of Cyrene (2016)   
*   Archaeological Site of Leptis Magna (2016)   
*   Archaeological Site of Sabratha (2016)   
*   Rock-Art Sites of Tadrart Acacus (2016)

# List of World Heritage in Danger
##### Mali
*   Old Towns of Djenné (2016)   
*   Timbuktu (2012)   
*   Tomb of Askia (2012)

# List of World Heritage in Danger
##### Mexico
*   Islands and Protected Areas of the Gulf of California (2019)

# List of World Heritage in Danger
##### Micronesia (Federated States of)
*   Nan Madol: Ceremonial Centre of Eastern Micronesia (2016)

# List of World Heritage in Danger
##### Niger
*   Air and Ténéré Natural Reserves (1992)

# List of World Heritage in Danger
##### Panama
*   Fortifications on the Caribbean Side of Panama: Portobelo-San Lorenzo (2012)

# List of World Heritage in Danger
##### Peru
*   Chan Chan Archaeological Zone (1986)

# List of World Heritage in Danger
##### Romania
*   Roșia Montană Mining Landscape (2021)

# List of World Heritage in Danger
##### Serbia
*   Medieval Monuments in Kosovo (2006)

# List of World Heritage in Danger
##### Solomon Islands
*   East Rennell (2013)

# List of World Heritage in Danger
##### South Sudan
*   Boma–Badingilo Migratory Landscape (2026)

# List of World Heritage in Danger
##### State of Palestine
*   Hebron/Al-Khalil Old Town (2017)   
*   Palestine: Land of Olives and Vines – Cultural Landscape of Southern Jerusalem, Battir (2014)   
*   Saint Hilarion Monastery/ Tell Umm Amer (2024)   
*   Sebastia (2026)

# List of World Heritage in Danger
##### Suriname
*   Historic Inner City of Paramaribo (2026)
</excerpt>

## Search 2
query: "World Heritage in Danger natural site original member United Nations"
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

## Search 3
query: "United Nations founding members 1945 list"
<excerpt title="Enlargement of the United Nations">
# Enlargement of the United Nations
## Timeline
### 1940s
#### 1945 (original members)
*   /Argentina  
*   Belarus_(seat held by the /Byelorussian Soviet Socialist Republic → renamed //Belarus in 1991)_  
*   ///Brazil  
*   Chile  
*   **China_(seat held by the Republic of China on [mainland (1912–1949) and on Taiwan (1949–present)] → seat transferred to the People's Republic of China in 1971)_[[H]](https://en.wikipedia.org/wiki/Enlargement_of_the_United_Nations#cnote_H)**  
*   /Cuba  
*   Czechoslovakia_(seat held by Third Czechoslovak Republic → Czechoslovak Socialist Republic → Czech and Slovak Federative Republic)_ → _dissolved (current UN members that formerly comprised Czechoslovakia: Czech Republicand Slovakia)_[[F]](https://en.wikipedia.org/wiki/Enlargement_of_the_United_Nations#cnote_F)  
*   Denmark  
*   Dominican Republic  
*   Egypt → United Arab Republic_(period when merged with Syria)_[[A]](https://en.wikipedia.org/wiki/Enlargement_of_the_United_Nations#cnote_A) → /Arab Republic of Egypt  
*   El Salvador  
*   **France_(seat held by the Provisional Government of the French Republic → became the French Fourth Republic → reconstituted as the /French Fifth Republic in 1958)_**  
*   //Haiti  
*   /Imperial State of Iran → Islamic Republic of Iran  
*   /Lebanon  
*   Luxembourg  
*   Dominion of New Zealand → New Zealand  
*   /Nicaragua  
*   ////Paraguay  
*   Commonwealth of the Philippines → Third Republic of the Philippines → Philippines under Martial Law → Fourth Republic of the Philippines → Fifth Republic of the Philippines  
*   Poland (Provisional Government of National Unity) → [Republic of Poland](https://en.wikipedia.org/wiki/Polish_People's_Republic "Polish People's Republic") → [Polish People's Republic](https://en.wikipedia.org/wiki/Polish_People's_Republic "Polish People's Republic") → Third Polish Republic  
*   /Saudi Arabia
</excerpt>

## Search 4
query: ""List of World Heritage in Danger" "natural" sites"
<excerpt title="List of World Heritage in Danger">
As of May 2026, there are 53 sites (14 natural and 39 cultural) on the List of World Heritage in Danger. Arranged by UNESCO regions, 22 of the listed sites are in the Arab States, 12 in Africa, six in Latin America and the Caribbean, six in Asia and the Pacific, and seven in Europe and North America. The majority of the endangered natural sites (nine) are in Africa.[[7]](https://en.wikipedia.org/wiki/List_of_World_Heritage_in_Danger#cite_note-8)[[8]](https://en.wikipedia.org/wiki/List_of_World_Heritage_in_Danger#cite_note-9) The list encompasses sites identified as facing threats to their integrity, which may arise from natural disasters, armed conflict, neglect, pollution, unsustainable tourism, or other hazards. Among these sites, the impacts of armed conflict are evident in countries such as Syria, where several sites, including the Ancient City of Aleppo and the Ancient Villages of Northern Syria, endangered as a result of the Syrian civil war. In Africa, the Democratic Republic of the Congo has multiple listings due to threats such as military conflict and environmental degradation affecting its national parks.[[9]](https://en.wikipedia.org/wiki/List_of_World_Heritage_in_Danger#cite_note-10)
In some cases, inclusion on the danger list has sparked conservation efforts and prompted the release of funds, benefitting sites such as the Galápagos Islands and Yellowstone National Park, both later removed from the List of World Heritage in Danger. Despite this, the list itself and UNESCO's implementation of it have been subject to criticism.[[10]](https://en.wikipedia.org/wiki/List_of_World_Heritage_in_Danger#cite_note-chape-p87-11)[[11]](https://en.wikipedia.org/wiki/List_of_World_Heritage_in_Danger#cite_note-timothy-p83-12) In particular, States Parties and other stakeholders have questioned the authority of the World Heritage Committee to designate a site as in danger without their consent.[[12]](https://en.wikipedia.org/wiki/List_of_World_Heritage_in_Danger#cite_note-iucn-p2-3-13)

Until 1992, when UNESCO set a precedent by placing several sites on the danger list against the wishes of the respective States Parties, such parties would typically submit a programme of corrective measures before a site was listed.[[13]](https://en.wikipedia.org/wiki/List_of_World_Heritage_in_Danger#cite_note-chape-p86-14) Rather than being used solely for its intended purpose, the List of World Heritage in Danger is perceived by some states as a "blacklist" and, according to Christina Cameron, Professor at the School of Architecture and Canada Research Chair on Built Heritage at the University of Montreal, has been used as a political tool to get the attention of States Parties.[[14]](https://en.wikipedia.org/wiki/List_of_World_Heritage_in_Danger#cite_note-thorsell-15)[[15]](https://en.wikipedia.org/wiki/List_of_World_Heritage_in_Danger#cite_note-iucn-p0-16)
The International Union for Conservation of Nature (IUCN) has noted that UNESCO has, in a number of cases, referenced the List of World Heritage in Danger without formally inscribing a site, particularly where threats could be easily addressed by the State Party.[[16]](https://en.wikipedia.org/wiki/List_of_World_Heritage_in_Danger#cite_note-iucn-p18-19-17) The Union has also argued that the prolonged retention of sites on the danger list is questionable and that other mechanisms for conservation should be sought in such cases.[[17]](https://en.wikipedia.org/wiki/List_of_World_Heritage_in_Danger#cite_note-iucn-p19-20-18)
</excerpt>

## Search 5
query: "UN founding members 1945 list countries"
<excerpt title="United Nations Member States">
# United Nations
## Information Service Vienna
1976 **San Marino**2 Mar. 1992 **Sao Tome and Principe**16 Sep. 1975 **Saudi Arabia**24 Oct. 1945 **Senegal**28 Sep. 1960 **Seychelles**21 Sep. 1976 **Sierra Leone**27 Sep. 1961 **Singapore**21 Sep. 1965 **Slovakia 11)**19 Jan. 1993 **Slovenia 12)**22 May 1992 **Solomon Islands**19 Sep. 1978 **Somalia**20 Sep. 1960 **South Africa**7 Nov. 1945 **Spain**14 Dec. 1955 **Sri Lanka**14 Dec. 1955 **Sudan**12 Nov. 1956 **Suriname**4 Dec. 1975 **Swaziland**24 Sep. 1968 **Sweden**19 Nov. 1946 **Syria 13)**24 Oct. 1945 **Tajikistan**2 Mar. 1992 **Thailand**16 Dec. 1946 **The former Yugoslav Republic of Macedonia 14)**8 Apr. 1993 **Togo**20 Sep. 1960 **Tonga**14 Sep. 1999 **Trinidad and Tobago**18 Sep. 1962 **Tunisia**12 Nov. 1956 **Turkey**24 Oct. 1945 **Turkmenistan**2 Mar. 1992 **Tuvalu**5 Sep. 2000 **Uganda**25 Oct. 1962 **Ukraine**24 Oct. 1945 **United Arab Emirates**9 Dec. 1971 **United Kingdom**24 Oct. 1945 **United of Republic of Tanzania 15)**14 Dec. 1961 **United States**24 Oct. 1945 **Uruguay**18 Dec.
</excerpt>

## Search 6
query: "natural sites on UNESCO List of World Heritage in Danger list natural sites"
<excerpt title="Discover Natural World Heritage Sites">
# Discover Natural World Heritage Sites
##### More information
Mosi-oa-Tunya / Victoria Falls (Zambia/Zimbabwe)
Photo: © IUCN / Mizuki Murai
Previous
Next
**Why is natural World Heritage important?**
World Heritage sites enjoy the highest level of international recognition through the 1972 World Heritage Convention, as places so valuable that their conservation transcends boundaries, cultures and generations. Our ability to secure the highest quality of protection to natural World Heritage sites is therefore a litmus test of the effectiveness of nature conservation more broadly.
Although there are relatively few natural World Heritage sites compared to other types of protected areas, they cover very large areas that represent the best of nature. The 266 sites currently inscribed on the World Heritage List for their natural values cover about 8% of the world’s total protected lands and seas.
**Facts & Figures**

# Discover Natural World Heritage Sites
##### More information
*   There are 266 World Heritage sites in 115 countries which are listed for natural values.  
*   227 classified as “natural sites”.  
*   39 classified as “mixed sites” - both natural and cultural.  
*   22% of World Heritage sites (22%of all 1199 sites) are recognised for their outstanding nature conservation values.  
*   Natural World Heritage sites cover 476.6 million hectares(ha) of land and sea.  
*   Natural World Heritage sites cover about 8%of the total area covered by all almost 300,000 protected areas.  
*   World Heritage forests absorb approximately 190 million tons of CO2 each year (equivalent to half the United Kingdom’s annual CO2 emissions from fossil fuels).  
*   They are currently losing 58 billion tons of ice every year – equivalent to the combined annual water use of France and Spain– and are responsible for nearly 5% of observed global sea-level rise.  
*   20% of mapped global species richness in just 1% of Earth’s surface.  
*   Over 75,000 species of plants.  
*   Over 30,000 species of mammals, birds, fishes, reptiles and amphibians.  
*   Over 20,000 threatened IUCN red listedspecies protected.  
*   1/3 of all remaining tigers and pandas.  
*   1/10 of great apes, giraffes, lions and rhinos.
**Top 10 biggest natural World Heritage sites**
**Site****Country****Total area (ha)**

# Discover Natural World Heritage Sites
##### More information
1. French Austral Lands and Seas France 67,297,900  
2. Phoenix Islands Protected Area Kiribati 40,825,813  
3. Papahānaumokuākea USA 36,479,268  
4. Great Barrier Reef Australia 34,823,325  
5. Galápagos Ecuador 14,696,203  
6. Kluane / Wrangell-St Elias / Glacier Bay / Tatshenshini-Alsek USA / Canada 9,728,368  
7. Lake Baikal Russia 8,550,838  
8. Aïr and Ténéré Natural Reserves Niger 7,869,613  
9. Tassili n’Ajjer Algeria 7,571,268  
10. Central Amazon Conservation Complex Brazil 5,131,312
</excerpt>

## Search 7
query: ""Natural sites" "World Heritage in Danger""
<excerpt title="IUCN advises “in danger” status for three World Heritage sites">
# IUCN advises “in danger” status for three World Heritage sites | IUCN
OTHER WORK  
    *   SCIENCE-LED APPROACH  
    *   INFORMING POLICY  
    *   SUPPORTING CONSERVATION ACTION  
    *   GEF AND GCF IMPLEMENTATION  
    *   IUCN CONVENING  
    *   IUCN ACADEMY  
    *   IUCN YOUTH ENGAGEMENT
*   Our Union
The world’s largest and most diverse environmental network.
*   Our Union
CORE COMPONENTS  
    *   Members  
    *   Expert Commissions  
    *   Secretariat and Director General  
    *   IUCN Council
*   IUCN World Protected and Conserved Areas Congress 2027  
    *   IUCN WORLD CONSERVATION CONGRESS  
    *   REGIONAL CONSERVATION FORA  
    *   CONTRIBUTIONS FOR NATURE  
    *   IUCN ENGAGE (LOGIN REQUIRED)  
    *   THE RANGER EFFECT
*   Resources
Resources
IUCN tools, publications and other resources.
*   Resources
EXPLORE ALL RESOURCES  
    *   Search all resources  
    *   IUCN Briefs  
    *   IUCN Publications  
    *   Conservation Tools
LIBRARIES  
    *   IUCN LIBRARY

# IUCN advises “in danger” status for three World Heritage sites | IUCN
*   About IUCN  
*   News & Events  
*   Press  
*   Blog  
*   Regions  
    *   Asia  
    *   Eastern and Southern Africa  
    *   Eastern Europe and Central Asia  
    *   Europe  
    *   Mediterranean  
    *   Mexico, Central America and the Caribbean  
    *   North America  
    *   Oceania  
    *   South America  
    *   West and Central Africa  
    *   West Asia

*   Other Sites  
    *   IUCN Academy  
    *   IUCN Contributions for Nature  
    *   IUCN Library  
    *   IUCN Red List of Threatened Species TM  
    *   IUCN Grant Management Portal  
    *   IUCN Green List of Protected and Conserved Areas  
    *   IUCN World Heritage Outlook  
    *   IUCN Leaders Forum  
    *   ECOLEX  
    *   Protected Planet  
    *   Union Portal (login required)  
    *   IUCN Engage (login required)  
    *   Commission portal (login required)
English
*   English  
*   Français  
*   Español
Get Involved
1.   Home  
2.   News & Events  
3.    IUCN Advises “in Danger” St...
Share:
Story 07 Jun, 2019

# IUCN advises “in danger” status for three World Heritage sites
IUCN, the official advisor on natural World Heritage, recommends for three natural sites to be listed as “World Heritage in danger”: the Sundarbans in Bangladesh, Mexico’s Islands and Protected Areas of the Gulf of California and the Ohrid region in North Macedonia.
The Sundarbans in Bangladesh is part of the world’s largest mangrove forest, lying on the delta of the Ganges, Brahmaputra and Meghna rivers and bordering India’s Sundarbans National Park, also a World Heritage site.
Photo: IUCN / Mizuki Murai
The Gulf of California in Mexico is the only place on Earth where the vaquita can be found
Photo: SEMARNAT (public domain)
Natural and Cultural Heritage of the Ohrid region
Photo: IUCN / Maja Vasilijević
Previous
Next
IUCN’s advice has been released today by UNESCO and is addressed to the World Heritage Committee, the governing body on World Heritage made up of 21 governments. The Committee will take decisions at its annual meeting in Azerbaijan from 30 June to 10 July.
</excerpt>

## Search 8
query: "list of 51 founding members of the United Nations 1945"
<excerpt title="Member states of the United Nations">
The original members of the United Nations were: France (then the Provisional Government), Russia (then the Soviet Union), China (then Republic of China), the United Kingdom, the United States—these first five forming the Security Council—Argentina, Australia, Belarus (then the Byelorussian SSR), Belgium, Bolivia, Brazil (then the Vargas Era Brazil), Canada, Chile (then the 1925–73 Presidential Republic), Colombia, Costa Rica, Cuba (then the 1902–59 Republic), Czechoslovakia (then the Third Republic), Denmark, the Dominican Republic, Ecuador, Egypt (then the Kingdom of Egypt), El Salvador, Ethiopia (then the Ethiopian Empire), Greece (then the Kingdom of Greece), Guatemala, Haiti (then the 1859–1957 Republic), Honduras, India (then the British Raj), Iran (then the Imperial State of Iran), Iraq (then the Kingdom of Iraq), Lebanon, Liberia, Luxembourg, Mexico, the Netherlands, New Zealand (then the Dominion of New Zealand), Nicaragua, Norway, Panama, Paraguay, Peru, the Philippines (then the Commonwealth), Poland (then the Provisional Government of National Unity), Saudi Arabia, South Africa (then the Union of South Africa), Syria (then the Mandatory Republic), Turkey, Ukraine (then the Ukrainian SSR), Uruguay, Venezuela and Yugoslavia (then the Democratic Federal Yugoslavia).[[14]](https://en.wikipedia.org/wiki/Member_states_of_the_United_Nations#cite_note-originalmembers-15)
Among the original members, 49 are either still UN members or had their memberships in the UN continued by a successor state_(see table below)_; for example, the membership of the Soviet Union was continued by the Russian Federation after its dissolution _(see the section Former members: Union of Soviet Socialist Republics)_. The other two original members, Czechoslovakia and Yugoslavia (i.e., the Socialist Federal Republic of Yugoslavia), had been dissolved and their memberships in the UN not continued from 1992 by any one successor state _(see the sections Former members: Czechoslovakia and Former members: Yugoslavia)_.[[14]](https://en.wikipedia.org/wiki/Member_states_of_the_United_Nations#cite_note-originalmembers-15)

At the time of UN's founding, the seat of China in the UN was held by the Republic of China, but as a result of United Nations General Assembly Resolution 2758 in 1971, it is now held by the People's Republic of China_(see the section Former members: Republic of China (Taiwan))_.
United Nations membership status
A number of the original members were not sovereign when they joined the UN, and only gained full independence later:[[15]](https://en.wikipedia.org/wiki/Member_states_of_the_United_Nations#cite_note-theworldin1945-16)
*   Belarus (then the Byelorussian Soviet Socialist Republic) and Ukraine (then the Ukrainian Soviet Socialist Republic) were both constituent republics of the Soviet Union, until gaining full independence in 1991.  
*   India (whose territory at that time, before the Partition of India, also included the present-day territories of Bangladesh and Pakistan) was under British colonial rule, until gaining full independence in 1947.  
*   New Zealand, while _de facto_ sovereign at that time, "only gained full capacity to enter into relations with other states in 1947 when it passed the Statute of Westminster Adoption Act. This occurred 16 years after the British Parliament passed the Statute of Westminster Act in 1931 that recognised New Zealand's autonomy. If judged by the Montevideo Convention criteria, New Zealand did not achieve full _de jure_ statehood until 1947."[[16]](https://en.wikipedia.org/wiki/Member_states_of_the_United_Nations#cite_note-17) However, the UN considers New Zealand to have been independent in 1945, at the time the UN was formed.[[15]](https://en.wikipedia.org/wiki/Member_states_of_the_United_Nations#cite_note-theworldin1945-16)  
*   The Philippines (then the Philippine Commonwealth) was a commonwealth with the United States, until gaining full independence in 1946.
</excerpt>

## Search 9
query: "natural site in danger list UNESCO 'natural' 'danger' site name country"
<excerpt title="56 Sites Are on UNESCO's List of World Heritage in Danger">
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

## Search 10
query: "natural World Heritage site in danger list UNESCO 2023"
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

Read the searches in order: how each query was formed, what came back, and how the next query used it. Find the failure in query choice or revision that cost the most, and write a new system prompt that fixes it. Replace or compress existing text where you can; avoid making the prompt much longer. Do not copy any fact, name, site or topic from these examples: the model will face unrelated questions. Keep the description of the `web_search` tool and the 10-search limit accurate.

Provide the new system prompt within ``` blocks.
