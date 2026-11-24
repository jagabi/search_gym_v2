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
I'm working on a guide for a RPG released on the DS, which was co-developed in 2007 by Square Enix and another company named after a planet. I'm stuck on getting one of the Secret Reports - specifically, Day 5 during the week when you partner with a character who doesn't go by a nickname. What is the name of the boss I need to defeat?

## Expected answer
Cornix Canor

## Grade 0.00

## Search 1 — query: "Square Enix co-developed 2007 DS RPG planet named company"
### Rank 1 of 177 — 0.74 (passed on)
<excerpt title="List of Square Enix video games">
Final Fantasy Tactics: The War of the Lions	PlayStation Portable	May 10, 2007	Square Enix	Yes	Yes	Yes	[79]  
Call of Duty 4: Modern Warfare (Japan release)	PlayStation 3, Xbox 360	May 26, 2007	Infinity Ward	Yes		  
Dragon Quest: Monster Battle Road	Arcade	June 2007	Rocket Studio	Yes			[80][81]  
Final Fantasy II	PlayStation Portable	June 7, 2007	Tose	Yes	Yes	Yes	[82]  
Itadaki Street DS	Nintendo DS	June 21, 2007	Think Garage	Yes			[57][83]  
Dragon Quest Swords: The Masked Queen and the Tower of Mirrors	Wii	July 12, 2007	Genius Sonority / Eighting	Yes	Yes	Yes	[84]  
The World Ends with You	Nintendo DS	July 27, 2007	Square Enix / Jupiter	Yes	Yes	Yes	[85]  
Final Fantasy XII International Zodiac Job System	PlayStation 2	August 9, 2007	Square Enix	Yes			[86]  
Final Fantasy Crystal Chronicles: Ring of Fates	Nintendo DS	August 23, 2007	Square Enix	Yes	Yes	Yes	[87]  
Crisis Core: Final Fantasy VII	PlayStation Portable	September 13, 2007	Square Enix	Yes	Yes	Yes	[88]  
Final Fantasy Tactics A2: Grimoire of the Rift	Nintendo DS	October 25, 2007	Square Enix	Yes	Yes	Yes	[89]  
Yosumin DS	Nintendo DS	November 8, 2007	Square Enix	Yes			[90]  
Dragon Quest IV[C]	Nintendo DS	November 22, 2007	ArtePiazza / Cattle Call	Yes	Yes	Yes	[91][92]
</excerpt>
### Rank 2 of 177 — 0.41
<excerpt title="List of Square Enix video games">
Final Fantasy Fables: Chocobo's Dungeon	Wii	December 13, 2007	h.a.n.d.	Yes	Yes	Yes	[93]  
Final Fantasy IV	Nintendo DS	December 20, 2007	Matrix Software	Yes	Yes	Yes	[94]  
Star Ocean: First Departure	PlayStation Portable	December 27, 2007	Tose	Yes	Yes	Yes	[95]  
Nintendo Switch	December 5, 2019	[96]  
PlayStation 4	[96]  
Final Fantasy Crystal Chronicles: My Life as a King	Wii	March 25, 2008	Square Enix	Yes	Yes	Yes	[97]  
Star Ocean: Second Evolution	PlayStation Portable	April 2, 2008	Tose	Yes	Yes	Yes	[98]  
PlayStation 4	October 28, 2015			[99]  
PlayStation Vita	[99]  
PlayStation 3	December 24, 2015			[99]  
Front Mission 2089: Border of Madness	Nintendo DS	May 29, 2008	h.a.n.d.	Yes			[100]  
Lord of Vermilion	Arcade	June 17, 2008	Think Garage	Yes			[57][101]  
Nanashi no Game	Nintendo DS	July 3, 2008	Epics	Yes			[102][103]  
Dragon Quest V[D]	Nintendo DS	July 17, 2008	ArtePiazza	Yes	Yes	Yes	[104]  
Sigma Harmonics	Nintendo DS	August 21, 2008	Think Garage	Yes			[57][105]  
Infinite Undiscovery	Xbox 360	September 2, 2008	tri-Ace	Yes	Yes	Yes	[106]  
Soul Eater: Monotone Princess	Wii	September 25, 2008	Square Enix	Yes			[107]
</excerpt>
### Rank 3 of 177 — 0.22
<excerpt title="Companies: Square Enix">
## The merger
So 2003 approached and both big RPG developers had to face the future of RPG development. Enix had to finance a big RPG project developed by tri-Ace (not to forget the plans of doing Dragon Quest VIII), and Square set up an expensive online community while developing some new games for the Nintendo GBA, the Sony PlayStation 2 and even the Game Cube. On top of that, Game development got more and more expensive. It seemed for both companies the best solution to merge. And so they did. In 2003, Squaresoft Co, Ltd. and Enix Corporation became one...
Officially, Enix took over Square back then. All the shareholders of Square got paid to exchange their Square shares for Enix shares. The management, however, was moved from Square to Square Enix. So the company that took over another was now controlled by those they took over. Quite awkward businessman-stuff, if you ask me.
Anyway, now both of the big RPG makers were able to create their games under the same flag. This was a shocking moment for many fans since there always was quite some rivalry going on between Square fans and Enix fans. Now they were fans of the same company. Some gamers now screamed that the games don't have the same quality as before the merger, and some even quit their hobby because they thought everything is lost. But was everything really lost? The portfolio of the new founded company was quite impressive: Star Ocean: Till The End of Time, Final Fantasy XI online, Dragon Quest VIII, Kingdom Hearts: Chain of Memories, Front Mission 4, Radiata Stories, Romacing SaGa... all of them were great RPGs created between 2003 and 2005. Now the company was even powerful enough to delay the release date of Final Fantasy XII so that they can do more finishing work without fearing bankruptcy if the game isn't released as soon as possible. They even were powerful enough now to support their former rival Game Arts while they were developing Grandia III, which was also released as a "Square Enix" game in 2006.

## The merger
This article was written on May 28th, 2006. On this day, Square-Enix's plans for the future looked promising. Children of Mana (DS), Final Fantasy III (DS) and Final Fantasy VII: Crisis core (PSP) seemed to be pretty good handheld-RPGs, where one was more focused on gameplay and the other two on story. The support of home consoles looked also very promising - Final Fantasy XII (PS2), Final Fantasy XIII (PS3), Final Fantasy: Crystal Chronicles 2 (Wii), Dragon Quest Yangus (PS2), Dragon Quest (Wii), Dawn of Mana (PS2), Valkyrie Profile 2: Silmeria (PS2)... there were lots of possibly great games announced. However, not everything went as perfect as Square Enix could have wished for: Game Arts was bought by a big online game publisher, stalling the new relationship between Square-Enix and Game Arts. Microsoft was able to make a contract with tri-Ace so that they'll create a RPG exclusively for the XBox 360 console without working together with Square-Enix. Did that mean that the long partnership between Square-Enix and tri-Ace ended? That was quite uncertain in late May 2006. How does a very famous Square action RPG say? "Time flows like a river, but history repeats." Will this work for Square Enix too?
Although I did this already at the copyright comments section, I just wanted to repeat this: All images (and especially the logos!) on this page are property of their respective owners. Consulting Moby Games helped me a lot to back up everything I wrote down.
</excerpt>
### Rank 4 of 177 — 0.21
<excerpt title="Square Enix">
Square Electronic Arts LLC	April 27, 1998	April 1, 2003	Costa Mesa, California, United States	A 70/30 joint venture with Electronic Arts for North American publication of Square's titles. It was folded into Square Enix's US operations after Square purchased EA's stake in the venture.	[262]  
Electronic Arts Square Co., Ltd.	May 1, 1998	April 1, 2003	Japan	A similar 30/70 joint-venture with Electronic Arts for Japanese publication of EA's titles. After the Square Enix merger, EA purchased Square's stake in the business and renamed it Electronic Arts Co., Ltd.	[263]  
Taito Soft Corporation (previously The Game Designers Studio)	June 22, 1999	March 11, 2010	Hirakawa-cho, 2-chome, Chiyoda-ku, Tokyo, Japan	Square Enix Co., Ltd. game development brand.	[264][265]  
Enix America Inc.	1999	April 1, 2003	Seattle, King County, Washington, United States	A joint venture between Enix and Eidos Interactive to publish Enix games for Western markets.	[266][267]  
Square Enix Webstar Network Technology (Beijing) Co., Ltd. (previously Enix Webstar Network Technology (Beijing) Co., Ltd.)	2001	February 28, 2005	Beijing, China	Enix Chinese publishing division.	[256][non-primary source needed]  
UIEvolution	March 2004	December 17, 2007	Bellevue, Washington, United States	Square Enix mobile software development division.	[34]  
Taito Art Corporation	September 28, 2005	July 28, 2008	Tokyo, Japan	Taito travel and insurance agency subsidiary.	[268][non-primary source needed]
</excerpt>
### Rank 5 of 177 — 0.19
<excerpt title="List of Square Enix video games">
For games released before the merger, see List of Square video games and List of Enix games.  
For mobile games released by the company, see List of Square Enix mobile games.  
For game franchises, see List of Square Enix video game franchises.  
For games released by Taito, both before and after the acquisition, see List of Taito games  
For games primarily published by the group's European branch see List of Square Enix Europe games.  
Console and PC gamesedit  
List of games  
Title	System	Original release date	Developer(s)	JP	NA	PAL	Ref(s)  
Bakusou Yankee Damashii	Windows	May 23, 2003	Atelier Double	Yes			[6]  
Hanjuku Hero Tai 3D	PlayStation 2	June 26, 2003	Square Enix	Yes			[7]  
All Star Pro-Wrestling III	PlayStation 2	August 7, 2003	Square Enix	Yes			[8]  
Final Fantasy Crystal Chronicles	GameCube	August 8, 2003	Square Enix	Yes	Yes	Yes	[9]  
Nintendo Switch	August 27, 2020	[10]  
PlayStation 4	[10]  
Sword of Mana	Game Boy Advance	August 29, 2003	Brownie Brown	Yes	Yes	Yes	[11]  
Drakengard	PlayStation 2	September 11, 2003	Cavia	Yes	Yes	Yes	[12]  
Kenshin Dragon Quest: Yomigaerishi Densetsu no Ken	Handheld TV	September 19, 2003	Square Enix	Yes			[13]  
The King of Automobile Companies	Web browser	October 1, 2003	thinkArts	Yes			[14]  
Front Mission	PlayStation	October 23, 2003	Square Enix	Yes			[15]  
Nintendo DS	March 22, 2007	Yes		[16]
</excerpt>

## Search 2 — query: ""Jupiter" "2007" DS "RPG""
### Rank 1 of 81 — 0.79 (passed on)
<excerpt title="NEO: The World Ends With You Is a Modern Hidden Gem">
# NEO: The World Ends With You Is a Modern Hidden Gem - YouTube
## NEO: The World Ends With You Is a Modern Hidden Gem
Man KBash 175K • 4y ago Live Playlist ()Mix (50+)20:52 The Biggest Moment of Existential Dread in Korean History 마이너 리뷰 갤러리 79K • 16h ago Live Playlist ()Mix (50+)Tranquil Autumn Cafe Jazz - Smooth Jazz with Cozy Street Ambience & Birdsong for Work & Relaxation Quiet Autumn Jazz 189 watching • 1mo ago Live Playlist ()Mix (50+)

# NEO: The World Ends With You Is a Modern Hidden Gem
Gaius Isidoro
Gaius Isidoro
4.01K subscribers
Subscribe
Subscribed
164
Download
3K views 2y ago
3,020 views • May 26, 2024
Tetsuya Nomura and the Kingdom Hearts team worked with developer Jupiter to create one of the most innovative and well-received action RPGs on the Nintendo DS platform in 2007 in Japan and 2008 worldwide. That game was known as Subarashiku Kono Sekai or It's a Wonderful World in Japan. But in the west this game was called The World Ends With You.…more
more
How this was made
Auto-dubbed
Audio tracks for some languages were automatically generated. Learn more

# NEO: The World Ends With You Is a Modern Hidden Gem
### Games


# The World Ends with You #### 2007
Gaming
Transcript
Follow along using the transcript.
Show transcript

# The World Ends with You #### 2007
### Gaius Isidoro 4.01K subscribers
VideosAbout Subscribe

# The World Ends with You #### 2007
## Video details
Date
May 26, 2024
Views
3,020
Likes
164
Show less

# NEO: The World Ends With You Is a Modern Hidden Gem
3,020 views 3K views
May 26, 2024
164
Download

# NEO: The World Ends With You Is a Modern Hidden Gem
## 13 Comments
Sort comments
Sort by
Top Show featured commentsNewest Show recent comments, including potential spam
Add a comment...
Pinned by @GaiusIsidoro

# NEO: The World Ends With You Is a Modern Hidden Gem
## 13 Comments
### @GaiusIsidoro
@GaiusIsidoro @GaiusIsidoro2 years ago
Thank you for watching!
Show less Read more
Like
4
Dislike
Reply

# NEO: The World Ends With You Is a Modern Hidden Gem
## 13 Comments
### @iSearchYoutube
2 years ago
Spread the word folks, give the franchise some exposure!
Show less Read more
Like
9
Dislike
Reply

# NEO: The World Ends With You Is a Modern Hidden Gem
## 13 Comments
### @rascalnotwascal7737
2 years ago
Sqaure Enix has always neglected TWEWY. They didn't market Neo at all either. Really breaks my heart because the chracters are some of my favorite in a JRPG
Show less Read more
Like
3
Dislike
Reply

# NEO: The World Ends With You Is a Modern Hidden Gem
## 13 Comments
### @Zeroxshinobi
2 years ago
TWEWY seems destined to be an underrated gem. I didn't expect Neo to be as good but I find it to be equally as good. Such a great game and wonderful story that made me feel good by end game.
Show less Read more
Like
2
Dislike
Reply

# NEO: The World Ends With You Is a Modern Hidden Gem
## 13 Comments
### @DrAzmo
2 years ago
I'm hoping you get a lot of views on this. Anything to let people know. There's only a few games from my teen years that are still near and dear to my heart: TWEWY and Phantom Dust. I religiously check up to see on sequels and while I didn't pre-order, I bought Neo on launch day and I wish I hadn't lost the switch in the divorce.
Show less Read more
Like
4
Dislike
Reply
</excerpt>
### Rank 2 of 81 — 0.76
<excerpt title="NEO: The World Ends With You Is a Modern Hidden Gem">
# NEO: The World Ends With You Is a Modern Hidden Gem
## 13 Comments
### @DrAzmo
2 years ago
I'm hoping you get a lot of views on this. Anything to let people know. There's only a few games from my teen years that are still near and dear to my heart: TWEWY and Phantom Dust. I religiously check up to see on sequels and while I didn't pre-order, I bought Neo on launch day and I wish I hadn't lost the switch in the divorce.
Show less Read more
Like
4
Dislike
Reply

# NEO: The World Ends With You Is a Modern Hidden Gem
## 13 Comments
### @kermitwithamustache3885
2 years ago
Glad more people are enjoying this modern classic, one of the better jrpgs of the generation and so little people played it
Show less Read more
Like
8
Dislike
Reply
1 reply
Hide replies
1 reply

# NEO: The World Ends With You Is a Modern Hidden Gem
## 13 Comments
### @ChenKen991
2 years ago
It's up there for me in the best games this generation. Gameplay was really fun and only got better as the game progressed, soundtrack is easily 10/10 with no bad tracks for me, returning characters were hyped and the rest of the game succeed the mechanics in the original game like threads, foods and difficulty management really really well.
Show less Read more
Like
Dislike
Reply

# NEO: The World Ends With You Is a Modern Hidden Gem
## 13 Comments
### @KillaPaint
2 years ago
Just a little comment for the algorithm
Show less Read more
Like
2
Dislike
Reply

# NEO: The World Ends With You Is a Modern Hidden Gem
## 13 Comments
### @rathalos4783
2 years ago
ngl it's not a gem, this game is shit compared to the original.
Show less Read more
Like
Dislike
Reply
1 reply
Hide replies
1 reply

# NEO: The World Ends With You Is a Modern Hidden Gem
## 13 Comments
### @stupidredname
2 years ago
I like twewt but I can admit it sucks lol
Show less Read more
Like
1
Dislike
Reply
1 reply
Hide replies
1 reply
Top is selected, so you'll see featured comments

# NEO: The World Ends With You Is a Modern Hidden Gem
## Comments 13
Top Show featured commentsNewest Show recent comments, including potential spam

# NEO: The World Ends With You Is a Modern Hidden Gem
## In this video
Transcript

# NEO: The World Ends With You Is a Modern Hidden Gem
## NEO: The World Ends With You Is a Modern Hidden Gem
Gaius Isidoro
Gaius Isidoro
164 Likes
3K Views
2024 May 26
Tetsuya Nomura and the Kingdom Hearts team worked with developer Jupiter to create one of the most innovative and well-received action RPGs on the Nintendo DS platform in 2007 in Japan and 2008 worldwide. That game was known as Subarashiku Kono Sekai or It's a Wonderful World in Japan. But in the west this game was called The World Ends With You. Fourteen years later, the game's successor NEO: The World Ends With You was released to much less fanfare. In this video I talk about NEO: The World Ends With You and why I think the game is a modern hidden gem that deserves more attention than it got. ► Subscribe: /@gaiusisidoro NEO: The World Ends With You Is a Modern Hidden Gem Amazon Affiliate Purchase Links (I make money from purchases from these links): NEO: The World Ends With You (Switch/US/Physical): https://amzn.to/3WTkUVJ The World Ends With You: Final Remix (Switch/US/Physical): https://amzn.to/4ayqv6R…...more
...more Show less
How this was made
Auto-dubbed
Audio tracks for some languages were automatically generated. Learn more

# NEO: The World Ends With You Is a Modern Hidden Gem
## NEO: The World Ends With You Is a Modern Hidden Gem
### Games


# The World Ends with You #### 2007
Gaming
Transcript
Follow along using the transcript.
Show transcript
</excerpt>
### Rank 3 of 81 — 0.74
<excerpt title="The World Ends with You">
_**The World Ends with You**_[[c]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-4) is an action role-playing game co-developed by Square Enix and Jupiter for the Nintendo DS. Set in the modern-day Shibuya shopping district of Tokyo, _The World Ends with You_ features a distinctive art style and urban fantasy elements inspired by Shibuya and its youth culture. Development was inspired by elements of Jupiter's previous handheld game, _Kingdom Hearts: Chain of Memories_. It was released in Japan in July 2007, and in PAL regions and North America in April 2008. Later, an enhanced port by [h.a.n.d.](https://en.wikipedia.org/wiki/H.a.n.d. "H.a.n.d.") for mobile devices was released in 2012 under the title _**The World Ends with You: Solo Remix**_, while another enhanced port for the Nintendo Switch was released worldwide in 2018 under the title _**The World Ends with You: Final Remix**_.
In the story, protagonist Neku Sakuraba and his allies are forced to participate in a game that will determine their fate. The battle system uses many of the unique features of the Nintendo DS, including combat that takes place on both screens, and attacks performed by certain motions on the touchscreen or by shouting into the microphone. Elements of Japanese youth culture, such as fashion, food, and cell phones, are key aspects of the missions and character progression.
_The World Ends with You_ received critical acclaim upon release, with critics praising the graphics, soundtrack, and integration of gameplay into the Shibuya setting, with minor criticism directed at its learning curve and occasionally imprecise touch-screen controls. It is regarded as one of the best Nintendo DS games, and one of the greatest video games ever made. In the first week of its release, the game was the second best-selling DS title in Japan, and the top-selling DS title in North America. Shiro Amano, writer and artist of the _Kingdom Hearts_manga, later created a manga based on the video game. An anime adaptation by Square Enix, DOMERICA, and Shin-Ei Animation aired from April 10 to June 26, 2021.

The iPhone, iPad and Android versions were removed in July 2023.[[2]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-5)
A sequel, _Neo: The World Ends with You_, was released worldwide on Nintendo Switch and PlayStation 4 on July 27, 2021, and on Windows on September 28.
_The World Ends with You_ is an action role-playing game arranged into three chapters based on the three weeks that Neku is involved in the Reapers' Game, with each chapter further divided by each day of the week. The player controls Neku and his partner as they explore Shibuya to complete each day's mission. Although most missions require completion within a certain time for Neku and his partner, this timer is not correlated to the passage of time for the player.[[3]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-eurogamer_review-6)
Shibuya is divided into several districts, some of which may be inaccessible on certain days or blocked by a wall that can only be removed by satisfying the request of a nearby Reaper, such as erasing Noise symbols, wearing a certain brand of clothing, or bringing an item. Neku can scan the area by activating a special pin, which reveals the thoughts of the non-player characters in the Realground and memes, hints which may help to progress the plot.[[4]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-ign_review-7) The scan also reveals random Noise symbols that drift about the area, or in some cases, float around a specific character. The player initiates a battle by touching Noise symbols; each symbol constitutes one round of battle. Selecting more than one Noise symbol at a time results in a multi-round battle, referred to in-game as multiple noise "reductions", that gradually increases in difficulty with each round and has greater rewards upon success. Altering the difficulty of the Noise and the amount of health for Neku and his partner also alter the benefits gained.[[5]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-1UP_review-8)
</excerpt>
### Rank 4 of 81 — 0.72
<excerpt title="Spectrobes Gets Excavation Date">
# Spectrobes Gets Excavation Date - IGN
Skip to content
ShortsDaily GamesEntertainmentReviewsGuides
Join for free
HomeSearch
Reviews
All ReviewsEditor's ChoiceGame ReviewsMovie ReviewsTV Show ReviewsTech Reviews
News
All NewsColumnsPlayStationXboxNintendoPCMobileEntertainmentMoviesShowsComicsTech
Guides
Cyberpunk 2077Final Fantasy ResonanceGTA 5Red Dead Redemption 2The Legend of Zelda: Breath of the WildThe Legend of Zelda: Ocarina of Time RemakeThe Legend of Zelda: Tears of the KingdomAll Guides
Interactive MapsIGN ShortsIGN Daily GamesPlaylist
Discover
Release DatesPercy Jackson World GuideStar Wars Zero CompanyAudible 2026METRO 2039Planet PokemonPreordersVideo Game TrailersMovie TrailersTV TrailersBest Tech for GamingUniversal Studios Hollywood HubDiscover Universal Orlando Resort
StoreRewards
Videos
Original ShowsPopularTrailersGameplayAll Videos
Privacy PolicyTerms of Use
More
IGN on socialAbout UsAccessibilityAdChoicesEditorial StandardsDo Not Sell My Personal InformationSite MapBoardsContact SupportAdvertise With IGN
Site Themes
Classic
Dark Mode
Automatic
Based on system preferences
Change Region
Africa (opens in a new window)AdriaAustralia (opens in a new window)Benelux (opens in a new window)Brazil (opens in a new window)Canada (opens in a new window)China (opens in a new window)Czech / Slovakia (opens in a new window)France (opens in a new window)Germany (opens in a new window)Greece (opens in a new window)Hungary (opens in a new window)India (opens in a new window)Ireland (opens in a new window)Israel (opens in a new window)Italy (opens in a new window)Japan (opens in a new window)Latin AmericaMiddle East - EnglishMiddle East - ArabicNordicPakistan (opens in a new window)Poland (opens in a new window)Portugal (opens in a new window)Romania (opens in a new window)Southeast AsiaSpain (opens in a new window)Turkey (opens in a new window)United Kingdom (opens in a new window)United States (opens in a new window)

# Spectrobes Gets Excavation Date - IGN
©2026 IGN a brand of IGN Entertainment, Inc. All Rights Reserved. No part of this website or its content may be reproduced without the copyright owner’s permission. IGN® and IGN Entertainment are trademarks or registered trademarks of IGN Entertainment, Inc.
Back To Top
Join for free or log in
Home›News›Spectrobes

# Spectrobes Gets Excavation Date
## Buena Vista launches the new RPG early next year.
ByDavid Adams
Updated: May 17, 2012 9:58am UTC
Add IGN on Google
00
Publisher Buena Vista Games today revealed that Spectrobes, a Japanese action-RPG from developer Jupiter Corporation, will ship worldwide on March 15, 2007.
Following its work on Kingdom Hearts: Chain of Memories, Jupiter offers an original sci-fi adventure for the Nintendo DS. Heroes Rallen and Jeena must excavate, awaken and train Spectrobes, prehistoric creatures which are crucial in defeating the evil Krawl forces. Throughout the game, players train Spectrobes, boosting their power and adjusting them to match a particular play style.
00

# Spectrobes Gets Excavation Date
## Buena Vista launches the new RPG early next year.
### Recommends
Rockstar Games Explains Why GTA 6 Is Missing Features From Past Games Like Prostitutes 18
I've Played the First 30 Minutes of GTA 6 on Every Console, Here's How Performance Compares 38
GTA 6 Review - NO Story Spoilers 1.8k

# Spectrobes Gets Excavation Date
## Buena Vista launches the new RPG early next year.
### Get the tools to beat your game
IGN Plus members get full access to all of IGN's maps and wikis, get to browse IGN ad free, and more. Try it today for as low at $2.49 a month.
Learn more
</excerpt>
### Rank 5 of 81 — 0.72
<excerpt title="The World Ends with You">
| The World Ends with You |  
| --- |  
|  North American Nintendo DS cover art. From left to right: Joshua, Neku, Beat (above), Shiki, and Rhyme. |  
| Developers | * Square Enix * Jupiter[[a]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-1) |  
| Publisher | Square Enix[[b]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-2) |  
| Directors | * Tatsuya Kando * Tomohiro Hasegawa * Tetsuro Hosokawa |  
| Producers | * Shinji Hashimoto * Tetsuya Nomura * Hatao Ogata |  
| Designers | * Takeshi Arakawa * Hiroyuki Itou |  
| Artists | * Tetsuya Nomura * Gen Kobayashi |  
| Writer | Sachie Hirano |  
| Composer | Takeharu Ishimoto |  
| Series | _The World Ends with You_ |  
| Platforms | * Nintendo DS * iOS * Android * Nintendo Switch |  
| Release | July 27, 2007 * **Nintendo DS** * JP: July 27, 2007 * EU: April 18, 2008 * NA: April 22, 2008 * AU: April 24, 2008[[1]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-3) **iOS** * WW: August 27, 2012 **Android** * WW: June 26, 2014 **Nintendo Switch** * JP: September 27, 2018 * WW: October 12, 2018 |  
| Genre | Action role-playing |  
| Modes | Single-player, multiplayer (_Final Remix_) |

_**The World Ends with You**_[[c]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-4) is an action role-playing game co-developed by Square Enix and Jupiter for the Nintendo DS. Set in the modern-day Shibuya shopping district of Tokyo, _The World Ends with You_ features a distinctive art style and urban fantasy elements inspired by Shibuya and its youth culture. Development was inspired by elements of Jupiter's previous handheld game, _Kingdom Hearts: Chain of Memories_. It was released in Japan in July 2007, and in PAL regions and North America in April 2008. Later, an enhanced port by [h.a.n.d.](https://en.wikipedia.org/wiki/H.a.n.d. "H.a.n.d.") for mobile devices was released in 2012 under the title _**The World Ends with You: Solo Remix**_, while another enhanced port for the Nintendo Switch was released worldwide in 2018 under the title _**The World Ends with You: Final Remix**_.
In the story, protagonist Neku Sakuraba and his allies are forced to participate in a game that will determine their fate. The battle system uses many of the unique features of the Nintendo DS, including combat that takes place on both screens, and attacks performed by certain motions on the touchscreen or by shouting into the microphone. Elements of Japanese youth culture, such as fashion, food, and cell phones, are key aspects of the missions and character progression.
_The World Ends with You_ received critical acclaim upon release, with critics praising the graphics, soundtrack, and integration of gameplay into the Shibuya setting, with minor criticism directed at its learning curve and occasionally imprecise touch-screen controls. It is regarded as one of the best Nintendo DS games, and one of the greatest video games ever made. In the first week of its release, the game was the second best-selling DS title in Japan, and the top-selling DS title in North America. Shiro Amano, writer and artist of the _Kingdom Hearts_manga, later created a manga based on the video game. An anime adaptation by Square Enix, DOMERICA, and Shin-Ei Animation aired from April 10 to June 26, 2021.
</excerpt>

## Search 3 — query: ""Secret Report" "The World Ends with You""
### Rank 1 of 50 — 0.80 (passed on)
<excerpt title="Secret Reports - Neo: The World Ends with You Guide">
# Secret Reports
ByRicky Frech, Casey DeFreitas, Angie Harvey, +3 more
Updated: Aug 24, 2021 11:55pm UTC
Add IGN on Google
This page is part of IGN's Neo: The World Ends with You Wiki guide and details where to find all 24 of the **Secret Reports**. Collecting all of these will give you access to the NEO TWEWY secret ending, making them important to find. Fortunately, it's not too tough once you get a handle on things.
Importantly, you need to make sure you unlock Hazuki Mikagi's Social Link node. This lets you go back to chapters and take on bosses in the form of blue noise. These are the main way you'll get **Secret Reports**, though a few are also tied to completing your Social Network.

# Secret Reports
## How to get all **Secret Reports** in NEO TWEWY
As mentioned above, the key is going back and fighting blue noise in past chapters. You'll also need to complete your Social Network, which requires playing the dive during Another Day in Dogenzaka. That gives you 15 Friendship Points and is required for unlocking every node.

# Secret Reports
## How to get all **Secret Reports** in NEO TWEWY
| Secret Report | Location |  
| --- | --- |  
| **Secret Report #1** | Week 1 Day 1 - Drum 'n' Stinger (Scramble Crossing) |  
| **Secret Report #2** | Week 1 Day 2 - Go-go Beringei (104 Building) |  
| **Secret Report #3** | Social Network 70% Complete |  
| **Secret Report #4** | Social Network 80% Complete |  
| **Secret Report #5** | Week 1 Day 5 - Fuya (Tipsy Tose Hall) |  
| **Secret Report #6** | Social Network 90% Complete |  
| **Secret Report #7** | Week 1 Day 7 - Susukichi (Tower Records Shibuya) |  
| **Secret Report #8** | Week 2 Day 1 - Houseleon (Takeshita St.) |  
| **Secret Report #9** | Week 2 Day 2 - Mr. Mew (Scramble Crossing) |  
| **Secret Report #10** | Social Network 100% Complete |  
| **Secret Report #11** | Week 2 Day 4 - Mammoth R&B (Center Street) |  
| **Secret Report #12** | Week 2 Day 5 - Phasasaurus Rex (Expressway Underpass) |  
| **Secret Report #13** | Week 2 Day 6 - Motoi (Spain Hill) |  
| **Secret Report #14** | Week 2 Day 7 - Grus Cantus (Takeshita Street) |  
| **Secret Report #15** | Week 3 Day 1 - Plague Batrakos (Tower Records Shibuya) |  
| **Secret Report #16** | Week 3 Day 2 - Iris Cantus (Dogenzaka) |  
| **Secret Report #17** | Week 3 Day 3 - Plague Stinger Boss (Shibuya Stream) |  
| **Secret Report #18** | Week 3 Day 4 - Leo Cantus Armo (Tokyu Plaza) |
</excerpt>
### Rank 2 of 50 — 0.78
<excerpt title="Secret Report Guide : r/TWEWY">
# The World Ends With You Final Remix - Secret Reports
*   Shiki (Video Guide)

    *   Day 1(Video Guide)

        *   Nose Glasses (Check the !!! at the Statue of Hachiko)

    *   Day 2 (Video Guide)

        *   Pig Noise Symbols (West Bus Terminal, Statue of Hachiko)

        *   Sailor Suit (Talk to the guy next to the Moai Statue)

    *   Day 3 (Video Guide)

        *   Pig Noise Symbols (Dogenzaka, Shibukyu Main Store)

        *   Yukata (Imprint Ramen on the Tech at Shibukyu Main Store)

        *   Boss Symbol No. 88 (Concert Stage)

    *   Day 4 (Video Guide)

        *   Pig Noise Symbols (104 Building, Scramble Crossing)

        *   Mrs. Claus (Go south after talking to Beat and Rhyme)

        *   Boss Symbol No. 87 (Scramble Crossing)

        *   Boss Symbol No. 80 (104 Building)

    *   Day 5 (Video Guide)

        *   Pig Noise Symbols (Molco, AMX)

        *   Mr. Ducky (Drag the coin to white 3 times during Reaper Creeper)

        *   Boss Symbol No. 90 (Molco)

    *   Day 6 (Video Guide)

        *   Pig Noise Symbols (Cadoi City)

        *   Solid Slammer (Imprint "Totally gnarly" during Shooter talk)

    *   Day 7 (Video Guide)

        *   Pig Noise Symbols (Towa Records)

        *   Mr. Mew Suit (Check Phone Booth of Love in Molco)

        *   Boss Symbol No. 91 (Station Underpass)

*   Joshua (Video Guide)

    *   Day 1 (Video Guide)

        *   Potted Plant (Examine Statue of Hachiko)

    *   Day 2 (Video Guide)

        *   Pig Noise Symbols (Spain Hill, Molco, Tipsy Tose Hall)

        *   Supermask's mask (Enter Mexican Dog in Spain Hill)

        *   Boss Symbol No. 86 (Tipsy Tose Hall)
</excerpt>
### Rank 3 of 50 — 0.78
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
### Rank 4 of 50 — 0.77
<excerpt title="Secret Report Guide : r/TWEWY">
# Secret Report Guide : r/TWEWY
Skip to main content
Open menu Open navigationGo to Reddit Home
r/TWEWY
Sign UpSign up for RedditLog InLog in to Reddit
Expand user menu Open settings menu
Go to TWEWY
r/TWEWY•8y ago
u/Underbuffed
Spoiler

# Secret Report Guide
Guide

# The World Ends With You Final Remix - Secret Reports
*   Shiki (Video Guide)

    *   Day 1(Video Guide)

        *   Nose Glasses (Check the !!! at the Statue of Hachiko)

    *   Day 2 (Video Guide)

        *   Pig Noise Symbols (West Bus Terminal, Statue of Hachiko)

        *   Sailor Suit (Talk to the guy next to the Moai Statue)

    *   Day 3 (Video Guide)

        *   Pig Noise Symbols (Dogenzaka, Shibukyu Main Store)

        *   Yukata (Imprint Ramen on the Tech at Shibukyu Main Store)

        *   Boss Symbol No. 88 (Concert Stage)

    *   Day 4 (Video Guide)

        *   Pig Noise Symbols (104 Building, Scramble Crossing)

        *   Mrs. Claus (Go south after talking to Beat and Rhyme)

        *   Boss Symbol No. 87 (Scramble Crossing)

        *   Boss Symbol No. 80 (104 Building)

    *   Day 5 (Video Guide)

        *   Pig Noise Symbols (Molco, AMX)

        *   Mr. Ducky (Drag the coin to white 3 times during Reaper Creeper)

        *   Boss Symbol No. 90 (Molco)

    *   Day 6 (Video Guide)

        *   Pig Noise Symbols (Cadoi City)

        *   Solid Slammer (Imprint "Totally gnarly" during Shooter talk)

    *   Day 7 (Video Guide)

        *   Pig Noise Symbols (Towa Records)

        *   Mr. Mew Suit (Check Phone Booth of Love in Molco)

        *   Boss Symbol No. 91 (Station Underpass)

*   Joshua (Video Guide)

    *   Day 1 (Video Guide)

        *   Potted Plant (Examine Statue of Hachiko)

    *   Day 2 (Video Guide)

        *   Pig Noise Symbols (Spain Hill, Molco, Tipsy Tose Hall)

        *   Supermask's mask (Enter Mexican Dog in Spain Hill)

        *   Boss Symbol No. 86 (Tipsy Tose Hall)
</excerpt>
### Rank 5 of 50 — 0.74
<excerpt title="Secret Reports - Neo: The World Ends with You Guide">
# Secret Reports
## How to get all **Secret Reports** in NEO TWEWY
| Secret Report | Location |  
| --- | --- |  
| **Secret Report #1** | Week 1 Day 1 - Drum 'n' Stinger (Scramble Crossing) |  
| **Secret Report #2** | Week 1 Day 2 - Go-go Beringei (104 Building) |  
| **Secret Report #3** | Social Network 70% Complete |  
| **Secret Report #4** | Social Network 80% Complete |  
| **Secret Report #5** | Week 1 Day 5 - Fuya (Tipsy Tose Hall) |  
| **Secret Report #6** | Social Network 90% Complete |  
| **Secret Report #7** | Week 1 Day 7 - Susukichi (Tower Records Shibuya) |  
| **Secret Report #8** | Week 2 Day 1 - Houseleon (Takeshita St.) |  
| **Secret Report #9** | Week 2 Day 2 - Mr. Mew (Scramble Crossing) |  
| **Secret Report #10** | Social Network 100% Complete |  
| **Secret Report #11** | Week 2 Day 4 - Mammoth R&B (Center Street) |  
| **Secret Report #12** | Week 2 Day 5 - Phasasaurus Rex (Expressway Underpass) |  
| **Secret Report #13** | Week 2 Day 6 - Motoi (Spain Hill) |  
| **Secret Report #14** | Week 2 Day 7 - Grus Cantus (Takeshita Street) |  
| **Secret Report #15** | Week 3 Day 1 - Plague Batrakos (Tower Records Shibuya) |  
| **Secret Report #16** | Week 3 Day 2 - Iris Cantus (Dogenzaka) |  
| **Secret Report #17** | Week 3 Day 3 - Plague Stinger Boss (Shibuya Stream) |  
| **Secret Report #18** | Week 3 Day 4 - Leo Cantus Armo (Tokyu Plaza) |  

# Secret Reports
## How to get all **Secret Reports** in NEO TWEWY
| **Secret Report #19** | Week 3 Day 5 - Plague Pachy Boss (Shibuya Stream) |  
| **Secret Report #20** | Week 3 Day 6 - Cervus Cantus (Udagawa Backstreets) |  
| **Secret Report #21** | Week 3 Day 7-1 - Shiba (Takeshita Street) |  
| **Secret Report #22** | Week 3 Day 7-2 - Soul Pulvis (Takeshita Street) |  
| **Secret Report #23** | Week 3 Day 7-3 - Phoenis Cantus (Tokyu Plaza) |  
| **Secret Report #24** | Either get Secret Report 21-23 or get Social Network 100% complete. |
Looking for more? Make sure to see the full list of Collectibles, the Noisepedia, and the NEO: The World Ends with You Walkthrough.

# Secret Reports
## How to get all **Secret Reports** in NEO TWEWY
### Up Next: Noisepedia
Previous GraffitiNext Noisepedia

# Secret Reports
## How to get all **Secret Reports** in NEO TWEWY
### Top Guide Sections
*   Beginner's Guide - Basics and Features  
*   Scramble Slam Tips - How to Earn Scramble Points  
*   Walkthrough  
*   Side Quests

# Secret Reports
## How to get all **Secret Reports** in NEO TWEWY
### Was this guide helpful?
Leave feedback
</excerpt>

## Search 4 — query: ""Secret Report" "Day 5" "The World Ends with You""
### Rank 1 of 74 — 0.86 (passed on)
<excerpt title="Secret Reports - Neo: The World Ends with You Guide">
# Secret Reports
ByRicky Frech, Casey DeFreitas, Angie Harvey, +3 more
Updated: Aug 24, 2021 11:55pm UTC
Add IGN on Google
This page is part of IGN's Neo: The World Ends with You Wiki guide and details where to find all 24 of the **Secret Reports**. Collecting all of these will give you access to the NEO TWEWY secret ending, making them important to find. Fortunately, it's not too tough once you get a handle on things.
Importantly, you need to make sure you unlock Hazuki Mikagi's Social Link node. This lets you go back to chapters and take on bosses in the form of blue noise. These are the main way you'll get **Secret Reports**, though a few are also tied to completing your Social Network.

# Secret Reports
## How to get all **Secret Reports** in NEO TWEWY
As mentioned above, the key is going back and fighting blue noise in past chapters. You'll also need to complete your Social Network, which requires playing the dive during Another Day in Dogenzaka. That gives you 15 Friendship Points and is required for unlocking every node.

# Secret Reports
## How to get all **Secret Reports** in NEO TWEWY
| Secret Report | Location |  
| --- | --- |  
| **Secret Report #1** | Week 1 Day 1 - Drum 'n' Stinger (Scramble Crossing) |  
| **Secret Report #2** | Week 1 Day 2 - Go-go Beringei (104 Building) |  
| **Secret Report #3** | Social Network 70% Complete |  
| **Secret Report #4** | Social Network 80% Complete |  
| **Secret Report #5** | Week 1 Day 5 - Fuya (Tipsy Tose Hall) |  
| **Secret Report #6** | Social Network 90% Complete |  
| **Secret Report #7** | Week 1 Day 7 - Susukichi (Tower Records Shibuya) |  
| **Secret Report #8** | Week 2 Day 1 - Houseleon (Takeshita St.) |  
| **Secret Report #9** | Week 2 Day 2 - Mr. Mew (Scramble Crossing) |  
| **Secret Report #10** | Social Network 100% Complete |  
| **Secret Report #11** | Week 2 Day 4 - Mammoth R&B (Center Street) |  
| **Secret Report #12** | Week 2 Day 5 - Phasasaurus Rex (Expressway Underpass) |  
| **Secret Report #13** | Week 2 Day 6 - Motoi (Spain Hill) |  
| **Secret Report #14** | Week 2 Day 7 - Grus Cantus (Takeshita Street) |  
| **Secret Report #15** | Week 3 Day 1 - Plague Batrakos (Tower Records Shibuya) |  
| **Secret Report #16** | Week 3 Day 2 - Iris Cantus (Dogenzaka) |  
| **Secret Report #17** | Week 3 Day 3 - Plague Stinger Boss (Shibuya Stream) |  
| **Secret Report #18** | Week 3 Day 4 - Leo Cantus Armo (Tokyu Plaza) |
</excerpt>
### Rank 2 of 74 — 0.85
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
### Rank 3 of 74 — 0.84
<excerpt title="Secret Report Guide : r/TWEWY">
# The World Ends With You Final Remix - Secret Reports
*   Shiki (Video Guide)

    *   Day 1(Video Guide)

        *   Nose Glasses (Check the !!! at the Statue of Hachiko)

    *   Day 2 (Video Guide)

        *   Pig Noise Symbols (West Bus Terminal, Statue of Hachiko)

        *   Sailor Suit (Talk to the guy next to the Moai Statue)

    *   Day 3 (Video Guide)

        *   Pig Noise Symbols (Dogenzaka, Shibukyu Main Store)

        *   Yukata (Imprint Ramen on the Tech at Shibukyu Main Store)

        *   Boss Symbol No. 88 (Concert Stage)

    *   Day 4 (Video Guide)

        *   Pig Noise Symbols (104 Building, Scramble Crossing)

        *   Mrs. Claus (Go south after talking to Beat and Rhyme)

        *   Boss Symbol No. 87 (Scramble Crossing)

        *   Boss Symbol No. 80 (104 Building)

    *   Day 5 (Video Guide)

        *   Pig Noise Symbols (Molco, AMX)

        *   Mr. Ducky (Drag the coin to white 3 times during Reaper Creeper)

        *   Boss Symbol No. 90 (Molco)

    *   Day 6 (Video Guide)

        *   Pig Noise Symbols (Cadoi City)

        *   Solid Slammer (Imprint "Totally gnarly" during Shooter talk)

    *   Day 7 (Video Guide)

        *   Pig Noise Symbols (Towa Records)

        *   Mr. Mew Suit (Check Phone Booth of Love in Molco)

        *   Boss Symbol No. 91 (Station Underpass)

*   Joshua (Video Guide)

    *   Day 1 (Video Guide)

        *   Potted Plant (Examine Statue of Hachiko)

    *   Day 2 (Video Guide)

        *   Pig Noise Symbols (Spain Hill, Molco, Tipsy Tose Hall)

        *   Supermask's mask (Enter Mexican Dog in Spain Hill)

        *   Boss Symbol No. 86 (Tipsy Tose Hall)
</excerpt>
### Rank 4 of 74 — 0.83
<excerpt title="Secret Report Guide : r/TWEWY">
# Secret Report Guide : r/TWEWY
Skip to main content
Open menu Open navigationGo to Reddit Home
r/TWEWY
Sign UpSign up for RedditLog InLog in to Reddit
Expand user menu Open settings menu
Go to TWEWY
r/TWEWY•8y ago
u/Underbuffed
Spoiler

# Secret Report Guide
Guide

# The World Ends With You Final Remix - Secret Reports
*   Shiki (Video Guide)

    *   Day 1(Video Guide)

        *   Nose Glasses (Check the !!! at the Statue of Hachiko)

    *   Day 2 (Video Guide)

        *   Pig Noise Symbols (West Bus Terminal, Statue of Hachiko)

        *   Sailor Suit (Talk to the guy next to the Moai Statue)

    *   Day 3 (Video Guide)

        *   Pig Noise Symbols (Dogenzaka, Shibukyu Main Store)

        *   Yukata (Imprint Ramen on the Tech at Shibukyu Main Store)

        *   Boss Symbol No. 88 (Concert Stage)

    *   Day 4 (Video Guide)

        *   Pig Noise Symbols (104 Building, Scramble Crossing)

        *   Mrs. Claus (Go south after talking to Beat and Rhyme)

        *   Boss Symbol No. 87 (Scramble Crossing)

        *   Boss Symbol No. 80 (104 Building)

    *   Day 5 (Video Guide)

        *   Pig Noise Symbols (Molco, AMX)

        *   Mr. Ducky (Drag the coin to white 3 times during Reaper Creeper)

        *   Boss Symbol No. 90 (Molco)

    *   Day 6 (Video Guide)

        *   Pig Noise Symbols (Cadoi City)

        *   Solid Slammer (Imprint "Totally gnarly" during Shooter talk)

    *   Day 7 (Video Guide)

        *   Pig Noise Symbols (Towa Records)

        *   Mr. Mew Suit (Check Phone Booth of Love in Molco)

        *   Boss Symbol No. 91 (Station Underpass)

*   Joshua (Video Guide)

    *   Day 1 (Video Guide)

        *   Potted Plant (Examine Statue of Hachiko)

    *   Day 2 (Video Guide)

        *   Pig Noise Symbols (Spain Hill, Molco, Tipsy Tose Hall)

        *   Supermask's mask (Enter Mexican Dog in Spain Hill)

        *   Boss Symbol No. 86 (Tipsy Tose Hall)
</excerpt>
### Rank 5 of 74 — 0.80
<excerpt title="The World Ends With You - Secret Reports">
down to Scramble Crossing and you will get this item.
~Eliminate the boss symbol No. 87 within this chapter at Hard or above.
The Blue Noise Symbol found in Scramble Crossing, Megumi Kitanji.
~Eliminate the boss symbol No. 80 within this chapter at Hard or above.
The Blue Noise Symbol found in 104 Building, Reaper Beat.
#= Day 5
~Collect the report for Shiki, Day 4.
~Track down and eliminate all of this chapter's Pig Noise symbols.
~Get Mr. Ducky. (White! White! White!).
Talk to the man in black clothes at Tipsy Tose Hall, move the coin to white
to obtain Reaper Creeper meme. Go to Spain Hill, defeat 3 Noise Symbols, then
Ai and Mina would appear in front of Mexican Dog. Now scan Ai and Mina and
defeat the Yellow Noise Symbols surrounding them. After that, talk to them,
imprint and select the Reaper Creeper meme. Move the coin to white for three
times to obtain the Mr. Ducky.
~Eliminate the boss symbol No. 90 within this chapter at Hard or above.
The Blue Noise Symbol found in Molco, Cornix Canor.
#= Day 6
~Collect the report for Shiki, Day 5.
~Collect the report for Shiki, Day 3.
~Track down and eliminate all of this chapter's Pig Noise Symbols.
~Get the Solid Slammer. ("Totally gnarly!")
At the beginning, talk to Makoto in the Scramble Crossing, then scan him
(Three hours). Scan him again and defeat the Yellow Noise Symbol to obtain
"Unreal, bro". "Come get some hot stuff", "Totally gnarly" memes. Talk to
Makoto or the girl, imprint Makoto and choose "Totally gnarly". Afterwards,
talk to the Reaper at top right and select the following options to answer
his questions: 1. Edoga the Shop, 2. High heels, 3. Bubbles to clear the
Discover more
Try Action Games
Play Tabletop RPGs
Dolls
path. Come to Center St. Entrance, talk to Makoto or the kid, imprint Makoto
and choose "Totally gnarly" to obtain Solid Slammer.
#= Day 7
</excerpt>

## Search 5 — query: "The World Ends with You week 1 partner"
### Rank 1 of 98 — 0.83 (passed on)
<excerpt title="The World Ends with You">
The player controls Neku Sakuraba (桜庭 音操, _Sakuraba Neku_; ネク _Neku_), an initially asocial teenage boy who claims that he does not "get" people, and rarely interacts with others at first. Computer-controlled characters make up the rest of the cast, which includes players paired with Neku.[[11]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-Noise_zones-14) In the first Game, Neku is paired with Shiki Misaki (美咲 四季, _Misaki Shiki_; シキ _Shiki_), a teenage girl who takes on the form of her best friend, as her physical appearance was her price of entry for the Game.[[12]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-15) In the second Game, Neku's partner is an intelligent and sly teenage boy, Yoshiya Kiryu (桐生 義弥, _Kiryū Yoshiya_), who prefers to be called Joshua (ヨシュア, _Yoshua_). Neku's final partner is Daisukenojo Bito (尾藤 大輔之丞, _Bitō Daisukenojō_), originally a player and ex-Reaper who calls himself "Beat" (ビイト, _Biito_).[[13]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-16) Beat became a Reaper to find a way to bring his younger sister, Raimu Bito (尾藤 来夢, _Bitō Raimu_) (nicknamed "Rhyme" (ライム, _Raimu_)), back to life, as she had sacrificed herself to save him from a Noise attack.[[14]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-17)Sanae Hanekoma (羽狛 早苗, _Hanekoma Sanae_; ハネコマ _Hanekoma_), the Producer, bound her soul to a pin from which her Noise could be summoned, and gave it to Beat. The final Game Master, Mitsuki Konishi (虚西 充妃, _Konishi Mitsuki_; コニシ _Konishi_), crushes her Noise form and transforms it back into a pin.

Besides the Composer and the Conductor, there are other high-ranking Reapers.[[15]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-18) For each week of the Game, Game Masters are assigned by the Conductor to lead the opposition to the players. Of the Game Masters opposing Neku, Sho Minamimoto (南師 猩, _Minamimoto Shō_; ミナミモト _Minamimoto_) is the most dangerous, as he willingly circumvents the rules in an attempt to supplant the Composer.[[16]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-19) While participating in the Games to earn promotions for their performance, the Reapers' goal is to ascend to the highest form of spiritual existence, the Angels.[[17]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-20) Angels supervise the Games and, if the stakes of a Game are particularly high, they send down one of their own to serve as the Producer.[[18]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-21) For the three weeks of the game's story, Sanae Hanekoma is the Producer. Disguised as a Shibuya café owner, he guides new players and narrates the "Secret Reports", which are obtained by completing additional missions after completing the game.
</excerpt>
### Rank 2 of 98 — 0.82
<excerpt title="The World Ends with You">
A player in the UG is invisible to the living in the RG, though one can sometimes read and influence their thoughts. The UG is frequented by creatures called "Noise", which are attracted by the negative feelings of the living. To progress in the Reapers' Game, players are often required to defeat Noise by killing or "erasing" them.[[4]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-ign_review-7) However, each Noise exists in two parallel universes, or "zones", simultaneously, and can only be defeated by two players simultaneously fighting and defeating the Noise from these separate zones. To do so, players are required to form a pact with another player to survive the Noise.[[11]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-Noise_zones-14) Players receive assignments via text messages sent to their cell phones, and their right hands are imprinted with a countdown indicating the time left in the mission.[[4]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-ign_review-7) After a day's mission is complete, the remaining players find themselves at the start of the next day's mission, having no sense of the time that has passed in between.

The player controls Neku Sakuraba (桜庭 音操, _Sakuraba Neku_; ネク _Neku_), an initially asocial teenage boy who claims that he does not "get" people, and rarely interacts with others at first. Computer-controlled characters make up the rest of the cast, which includes players paired with Neku.[[11]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-Noise_zones-14) In the first Game, Neku is paired with Shiki Misaki (美咲 四季, _Misaki Shiki_; シキ _Shiki_), a teenage girl who takes on the form of her best friend, as her physical appearance was her price of entry for the Game.[[12]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-15) In the second Game, Neku's partner is an intelligent and sly teenage boy, Yoshiya Kiryu (桐生 義弥, _Kiryū Yoshiya_), who prefers to be called Joshua (ヨシュア, _Yoshua_). Neku's final partner is Daisukenojo Bito (尾藤 大輔之丞, _Bitō Daisukenojō_), originally a player and ex-Reaper who calls himself "Beat" (ビイト, _Biito_).[[13]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-16) Beat became a Reaper to find a way to bring his younger sister, Raimu Bito (尾藤 来夢, _Bitō Raimu_) (nicknamed "Rhyme" (ライム, _Raimu_)), back to life, as she had sacrificed herself to save him from a Noise attack.[[14]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-17)Sanae Hanekoma (羽狛 早苗, _Hanekoma Sanae_; ハネコマ _Hanekoma_), the Producer, bound her soul to a pin from which her Noise could be summoned, and gave it to Beat. The final Game Master, Mitsuki Konishi (虚西 充妃, _Konishi Mitsuki_; コニシ _Konishi_), crushes her Noise form and transforms it back into a pin.
</excerpt>
### Rank 3 of 98 — 0.80
<excerpt title="The World Ends with You">
Besides the Composer and the Conductor, there are other high-ranking Reapers.[[15]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-18) For each week of the Game, Game Masters are assigned by the Conductor to lead the opposition to the players. Of the Game Masters opposing Neku, Sho Minamimoto (南師 猩, _Minamimoto Shō_; ミナミモト _Minamimoto_) is the most dangerous, as he willingly circumvents the rules in an attempt to supplant the Composer.[[16]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-19) While participating in the Games to earn promotions for their performance, the Reapers' goal is to ascend to the highest form of spiritual existence, the Angels.[[17]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-20) Angels supervise the Games and, if the stakes of a Game are particularly high, they send down one of their own to serve as the Producer.[[18]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-21) For the three weeks of the game's story, Sanae Hanekoma is the Producer. Disguised as a Shibuya café owner, he guides new players and narrates the "Secret Reports", which are obtained by completing additional missions after completing the game.

The game's story follows Neku over the three weeks that he plays the Game, paired with partners Shiki, Joshua, and Beat for each week, respectively. Neku is initially confused, as he does not know how he died or how he arrived at the UG. As he develops friendships with his partners, he starts to understand the rules of the Game. After the first week, only Shiki is allowed to return to the living, and she promises to meet Neku at the statue of Hachikō.[[19]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-22)[[20]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-23) He also recovers his entry fee, which was his memories, except for the events leading up to his death. However, Shiki has become what Neku values most, and she is used as his new entry fee for the second week; in addition, Beat defects to the Reapers in hopes of finding a way to resurrect Rhyme after she sacrifices herself to save him. During the second week, Neku recalls small details of his death; he eventually realizes that Sho Minamimoto, one of the Reapers he faced during the Game, shot him. At the end of the second week, Joshua seemingly sacrifices himself to save Neku from an explosion Minamimoto causes.
</excerpt>
### Rank 4 of 98 — 0.79
<excerpt title="The World Ends with You">
The game's story follows Neku over the three weeks that he plays the Game, paired with partners Shiki, Joshua, and Beat for each week, respectively. Neku is initially confused, as he does not know how he died or how he arrived at the UG. As he develops friendships with his partners, he starts to understand the rules of the Game. After the first week, only Shiki is allowed to return to the living, and she promises to meet Neku at the statue of Hachikō.[[19]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-22)[[20]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-23) He also recovers his entry fee, which was his memories, except for the events leading up to his death. However, Shiki has become what Neku values most, and she is used as his new entry fee for the second week; in addition, Beat defects to the Reapers in hopes of finding a way to resurrect Rhyme after she sacrifices herself to save him. During the second week, Neku recalls small details of his death; he eventually realizes that Sho Minamimoto, one of the Reapers he faced during the Game, shot him. At the end of the second week, Joshua seemingly sacrifices himself to save Neku from an explosion Minamimoto causes.

Because Joshua was never actually dead, the Game is nullified and Neku is forced to play the game a third time. His entry fee this time is all of the other players, meaning he cannot form any pacts and stands no chance against the Noise; however, Beat defects from the Reapers and rejoins Neku. Neku and Beat find that the Reapers and the population of Shibuya are wearing special red pins that brainwash them into thinking the same thoughts. Without any missions to complete, the two venture to the fabled "Shibuya River", which Joshua was looking for during the second week. At the river, they find Megumi Kitaniji (北虹 寵, _Kitaniji Megumi_; キタニジ _Kitaniji_), the Game's Conductor, who explains that he created the red pins in an attempt to remake Shibuya, which the Composer challenged him to do. If he fails, both he, and as a price for losing the Game, Shibuya, will be erased.[[21]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-24)[[22]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-25)
Joshua reappears and reveals himself to be the Composer, returning to Neku the missing part of his memory of his death: Joshua was the one who shot Neku and chose him to be his proxy in his challenge with Kitaniji. Minamimoto, who had been trying to usurp the position of Composer, attempted to kill Joshua in his weakened state as a human. After Kitaniji fails to defeat Neku by using his friends against him, Joshua gives Neku one last challenge: to shoot Joshua to determine the fate of Shibuya. Neku is too conflicted to make a choice, and Joshua shoots him down.[[23]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-26) Neku finds himself back at the scramble crossing, confused but alive.
</excerpt>
### Rank 5 of 98 — 0.57
<excerpt title="General Speedrunning Guide - The World Ends With You">
## **Solo Remix for iOS/Android (SR)**
To be perfectly honest, this is a dead category. For the dual screen purists, there is DS, and for the high-definition glory, there is FR, which is faster because of co-op mode. That leaves SR in an unattractive position, because SR is basically FR without co-op. Any strategies that apply to FR may apply to SR. However, the partner attacks at a much slower rate compared to co-op.

## **Japanese version?**
The Japanese DS version has less text bubbles, so text is faster. However, certain equips are worse, which makes it slower overall. Stick to the English version. As for FR, it is unknown whether or not it's faster.
*   Vanilla Soft Serve gives +1 BRV instead of +2. This delays Neku's Biker Jacket equip until W2D5.  
*   BRAVE+ gives +10 BRV instead of +20. This affects Beat the most, as he'll be crippled until D4.  
*   The Burst Rounds psych has an efficiency rating of 50% instead of 150%. As Burst Rounds is used from W2D3 onward, this drastically hinders Neku's damage output.  
*   The Daruma pin has a different name, _Gemaga_, and has a starting pin ATK of 32 instead of 50.  
*   Lv1 and Lv2 fusions cost 5 and 10 stars, instead of 4 and 8.

## **Equips**
Too much information to be listed here. Please see the equip guide.

## **Daily Guide: Week 1 (Shiki)**
Directions show the most direct path to advance the story.

## D1: Scramble > Hachiko > 104
Everything is forced. In FR, it's possible to lightly activate Pyrokinesis to erase the frogs without rebooting the pin.

## D2: Termpass > Hachiko > Bus Terminal > Hachiko
For Thunderbolt in DS, it has a programming error that results in half the shots missing. For Shockwave, it's possible to get 11 uses before reboot by pausing after the 8th use, then initiating another 3-hit combo. When examining the statue for the first time, immediately select "scout for more info" to skip dialogue.

## D3: Concert > Dogenzaka > Shibukyu Main > Dogenzaka (cough drops) > Concert > Shibukyu Main > Dogenzaka > Concert
In FR, Ribbon Bonnet is cheaper and requires less BRV, so Shiki can wear it right away. The pig at Dogenzaka should be fought for food money at Ramen Don and Shibukyu Sunshine. The cough drops side quest is about a 30-second detour, but should be done to get the Lucky Star pin, which sells for ¥20000.

## D4: 104 > Towa Records
Sell Lucky Star to shop at 104. Don't sell the ¥500 pins because there's a wall that needs them. If LVG is 1/3, the ¥1000 pin drop from the blue frog is 90%. You may fight the pig at 104 to level up and guarantee the drop.

## D5: Tipsy Tose > AMX (CD) > Molco (via Tipsy Tose/Spain Hill) > Spain Hill
Equip Murasame when you get it, because there's a wall that needs it at Lv3. In FR, it will evolve at Lv4, so unequip it before that happens. Shopping at Molco before fighting the noise at Spain Hill is very important, as the Tigre Punks and D+B shops have some nice equips.

## D6: Scramble > Center St. > Molco (via Scramble) > Scramble (via Spain Hill) > 104
Pay attention to the route, as you must backtrack. A 4-chain at Center St. should be done to get some Rare Metal (RM) for the Biker Jacket. 6 RM is required for 2 jackets. Make sure you speak to the wall reaper before leaving Center St. to allow the backtrack. When fighting at Scramble Crossing for the Red Skull mission, make sure to only select bird noise symbols for more RM.
</excerpt>

# Example 2
## Question
According to the Our World in Data website's Maddison Project Database, out of Albania, Algeria, Angola, and Argentina, which countries had an increase in GDP per capita from 1985 to 2022 of more than $8000?

## Expected answer
Albania, Algeria

## Grade 0.80

## Search 1 — query: "Albania GDP per capita Maddison Project 2022"
### Rank 1 of 87 — 0.22 (passed on)
<excerpt title="Albania GDP per Capita | 2025 | 2026 | Data">
# Albania's GDP PPP per Capita
Chile36,614 36,710  
Costa Rica35,366 36,413  
North Macedonia33,789 35,187  
Mauritius33,905 34,941  
Dominican Republic31,374 32,596  
Gabon32,075 32,389  
Armenia30,290 32,218  
Thailand31,123 31,830  
Azerbaijan31,276 31,661  
China30,186 31,639  
Guyana30,701 30,701  
Mexico30,159 30,399  
Bhutan27,902 29,680  
Bosnia and Herzegovina27,713 28,604  
Suriname27,428 28,313  
Turkmenistan28,045 28,305  
Botswana27,036 27,807  
Egypt26,119 27,079  
Paraguay25,936 26,815  
Brazil26,035 26,538  
Albania25,043 26,137  
Peru25,209 25,733  
Mongolia24,029 25,255  
Libya24,202 24,753  
Vietnam22,732 24,522  
Colombia24,093 24,413  
Indonesia22,471 23,460  
Sri Lanka20,338 21,062  
Ukraine21,117 21,043  
Algeria20,334 20,863
</excerpt>
### Rank 2 of 87 — 0.17
<excerpt title="Albania GDP per Capita | 2025 | 2026 | Data">
# Albania's GDP PPP per Capita
[Rest of World](javascript:__doPostBack('ctl00$cphPageContents$lbFilterMoreRestOfWorld',''))
* * *
[High Income Countries](javascript:__doPostBack('ctl00$cphPageContents$lbFilterMoreHighIncomeCountries',''))
[Middle Income Countries](javascript:__doPostBack('ctl00$cphPageContents$lbFilterMoreMiddleIncomeCountries',''))
[Low Income Countries](javascript:__doPostBack('ctl00$cphPageContents$lbFilterMoreLowIncomeCountries',''))
* * *
[Bottom Billion](javascript:__doPostBack('ctl00$cphPageContents$lbFilterMoreBottomBillion','')) **Trade & Political Blocs**
[European Union](javascript:__doPostBack('ctl00$cphPageContents$lbFilterMoreEU',''))
[ASEAN](javascript:__doPostBack('ctl00$cphPageContents$lbFilterMoreASEAN',''))
[RCEP](javascript:__doPostBack('ctl00$cphPageContents$lbFilterMoreRCEP',''))
[CPTPP](javascript:__doPostBack('ctl00$cphPageContents$lbFilterMoreCPTPP',''))
[BRICS](javascript:__doPostBack('ctl00$cphPageContents$lbFilterMoreBRICS',''))
**Forums**
[OECD](javascript:__doPostBack('ctl00$cphPageContents$lbFilterMoreOECD',''))
[G7](javascript:__doPostBack('ctl00$cphPageContents$lbFilterMoreG7',''))
[G20](javascript:__doPostBack('ctl00$cphPageContents$lbFilterMoreG20',''))
[IPEF](javascript:__doPostBack('ctl00$cphPageContents$lbFilterMoreIPEF',''))
[Commonwealth](javascript:__doPostBack('ctl00$cphPageContents$lbFilterMoreCommonwealth',''))
* * *
Omit countries with poor quality GDP data: - [x]
Omit countries with poor quality governance: - [x]
* * *
How to use filters [Reset all filters](javascript:__doPostBack('ctl00$cphPageContents$lbResetFilters',''))
GDP Per Capita (PPP, Int$, 2021 Constant Prices)Estimate
(2025)Estimate
</excerpt>
### Rank 3 of 87 — 0.17
<excerpt title="Albania GDP per Capita | 2025 | 2026 | Data">
# Albania's GDP PPP per Capita
Zimbabwe9,263 9,554  
Myanmar8,494 8,619  
Pakistan8,432 8,606  
Nepal8,202 8,504  
Cameroon8,137 8,196  
Senegal7,701 7,936  
Guinea7,525 7,895  
Ethiopia7,006 7,469  
Tajikistan7,014 7,401  
Papua New Guinea6,793 6,892  
Zambia6,612 6,800  
Benin6,144 6,425  
Tanzania5,999 6,187  
Gambia5,528 5,690  
Rwanda5,386 5,665  
Sierra Leone5,273 5,381  
Mali5,134 5,267  
Togo5,007 5,151  
Comoros5,073 5,131  
Uganda4,892 5,065  
Guinea-Bissau4,833 4,958  
Burkina Faso4,497 4,598  
Sudan4,352 4,519  
Lesotho4,513 4,518  
Chad4,344 4,426  
Haiti4,196 4,083  
Congo, Dem. Rep3,257 3,323  
Niger3,192 3,312  
Afghanistan3,505 3,287  
Madagascar3,136 3,182  
Liberia2,806 2,900  
Malawi2,530 2,534  
Mozambique2,398 2,358  
Central African Republic2,252 2,239
</excerpt>
### Rank 4 of 87 — 0.17
<excerpt title="Albania GDP per Capita | 2025 | 2026 | Data">
# Albania's GDP PPP per Capita
GROSS DOMESTIC PRODUCT PER CAPITA 2025 & 2026 ESTIMATES
* * *
**Albania's GDP per capita (PPP) is estimated to be $26,137 for 2026.** This figure is derived from a GDP (PPP) of $72 billion, which accounts for the informal economy and any base year effects, and a population of 2.7 million.
GDP per capita (PPP based) is a crucial economic metric that measures a country's economic output per person. It's calculated by converting a nation's Gross Domestic Product (GDP) into international dollars using Purchasing Power Parity (PPP) exchange rates, which reflect the actual cost of living within a country. This adjusted GDP figure is then divided by the total population to determine the average economic output per individual.
Albania's data is highlighted in the table below, use the filter and sort order options to allow easy comparison with other countries.
Data source: World Economics Research, London
**Filter:**
[All](javascript:__doPostBack('ctl00$cphPageContents$lbFilterAll',''))
[Africa](javascript:__doPostBack('ctl00$cphPageContents$lbFilterAfrica',''))
[Asia Pacific](javascript:__doPostBack('ctl00$cphPageContents$lbFilterAsiaPacific',''))
[Americas](javascript:__doPostBack('ctl00$cphPageContents$lbFilterAmericas',''))
[Europe](javascript:__doPostBack('ctl00$cphPageContents$lbFilterEurope',''))
More...
*   **Thematic Groupings**
[Global South](javascript:__doPostBack('ctl00$cphPageContents$lbFilterMoreGlobalSouth',''))
[Global North](javascript:__doPostBack('ctl00$cphPageContents$lbFilterMoreGlobalNorth',''))
* * *
[Emerging Markets](javascript:__doPostBack('ctl00$cphPageContents$lbFilterMoreEmergingMarkets',''))
[Frontier Markets](javascript:__doPostBack('ctl00$cphPageContents$lbFilterMoreFrontierMarkets',''))
[Developed Markets](javascript:__doPostBack('ctl00$cphPageContents$lbFilterMoreDevelopedMarkets',''))
</excerpt>
### Rank 5 of 87 — 0.15
<excerpt title="File:Gdp per capita maddison project database, 1 to 2022, NIC.svg">
# File:Gdp per capita maddison project database, 1 to 2022, NIC.svg
## Summary
[edit]
Description Gdp per capita maddison project database, 1 to 2022, NIC.svg**English:** GDP per capita, NIC  
Date 2022  
Sourcehttps://ourworldindata.org/grapher/gdp-per-capita-maddison-project-database?tab=map  
Author Our World In Data  
Permission
(Reusing this file)"License: All of Our World in Data is completely open access and all work is licensed under the Creative Commons BY license. You have the permission to use, distribute, and reproduce in any medium, provided the source and authors are credited."

# File:Gdp per capita maddison project database, 1 to 2022, NIC.svg
## Licensing
[edit]
This file is licensed under the Creative CommonsAttribution 4.0 International license.
You are free:
*   **to share** – to copy, distribute and transmit the work  
*   **to remix** – to adapt the work
Under the following conditions:
*   **attribution** – You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.
https://creativecommons.org/licenses/by/4.0 CC BY 4.0 Creative Commons Attribution 4.0 true true

# File:Gdp per capita maddison project database, 1 to 2022, NIC.svg
## File history
Click on a date/time to view the file as it appeared at that time.
|  | Date/Time | Thumbnail | Dimensions | User | Comment |  
| --- | --- | --- | --- | --- | --- |  
| current | 18:46, 4 February 2026 |  | 850 × 833 (28 KB) | Doc James(talk | contribs) | Importing from https://ourworldindata.org/grapher/gdp-per-capita-maddison-project-database?tab=map |
You cannot overwrite this file.

# File:Gdp per capita maddison project database, 1 to 2022, NIC.svg
## File usage on Commons
The following page uses this file:
*   Template:OWID/Gdp per capita maddison project database

# File:Gdp per capita maddison project database, 1 to 2022, NIC.svg
## Metadata
This file contains additional information such as Exif metadata which may have been added by the digital camera, scanner, or software program used to create or digitize it. If the file has been modified from its original state, some details such as the timestamp may not fully reflect those of the original file. The timestamp is only as accurate as the clock in the camera, and it may be completely wrong.
| Width | 850 |  
| --- |  
| Height | 833.05 |  
| Show extended details |

# File:Gdp per capita maddison project database, 1 to 2022, NIC.svg
## Structured data
Structured data labels link to their respective Wikidata pages and will open in a new window.Dismiss

# File:Gdp per capita maddison project database, 1 to 2022, NIC.svg
## Structured data
### Items portrayed in this file
#### depicts
Edit
from Wikidata
Custom value
Custom value
Some value
No value

# File:Gdp per capita maddison project database, 1 to 2022, NIC.svg
## Structured data
### Items portrayed in this file
#### copyright status
Edit

# File:Gdp per capita maddison project database, 1 to 2022, NIC.svg
## Structured data
### Items portrayed in this file
#### copyrighted
Mark as prominent
</excerpt>

## Search 2 — query: "Albania GDP per capita 1985 Maddison Project"
### Rank 1 of 161 — 0.34 (passed on)
<excerpt title="Albania Economy: GDP, Inflation and Historical Data">
Economic AtlasEurope & Central Asia Albania
Country data profile

## Albania: economic indicators
Historical output, prices, jobs, trade, population and market data.
Region**Europe & Central Asia**
Income group**Upper middle income**
Currency**Albanian lek**
Data updated**Nov 6, 2026**
Key figuresData explorerMore seriesSources

## Key figures
Latest published observations · coverage through 2025
Interactive data explorer

## GDP and economic indicators
Add countries or measures to the same chart. Hover for exact values and drag the lower timeline to change the date range.
Up to 12 series
Country Indicator
🇦🇱 Albania
GDP
Published values share one scale. Use this mode when the selected indicators have comparable units.
*   Albania · GDP
**About this chart** Gross domestic product is the total income earned through the production of goods and services in an economic territory during an accounting period. It can be measured in three different ways: using either the expenditure approach, the income approach, or the production approach. This indicator is expressed in current prices, meaning no adjustment has been made to account for price changes over time. This indicator is expressed in United States dollars.
Default measure GDP, current US$
Latest observation 2025
Source World Bank WDI
Forecasts Not included
Latest data

## More indicators
Browse all indicators →
Detailed statistics

## Economic history
Observed data and published historical estimates. Missing years are not treated as zero.

## Economic history
### Long-run GDP per person
Maddison Project Database · real 2011 US$
*   Real GDP per person

## Economic history
### GDP per person
Current US dollars
*   GDP per person

## Economic history
### Growth and prices
Annual percentage change
*   GDP growth  
*   Inflation

## Economic history
### Trade openness
Exports and imports as a share of GDP
*   Exports  
*   Imports

## Economic history
### Jobs and labor force
Modeled ILO estimates where available
*   Unemployment  
*   Labor-force participation

## Economic history
### Share prices
Representative national index where available
No observations are available for this chart.

## Economic history
### Debt and investment
Share of GDP
*   Government debt / GDP  
*   FDI inflows / GDP
Data & methodology

## Sources for this profile
Each line keeps its source definition, unit and observation year.
</excerpt>
### Rank 2 of 161 — 0.33
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
### Rank 3 of 161 — 0.16
<excerpt title="Albania GDP per Capita | 2025 | 2026 | Data">
# Albania's GDP PPP per Capita
GROSS DOMESTIC PRODUCT PER CAPITA 2025 & 2026 ESTIMATES
* * *
**Albania's GDP per capita (PPP) is estimated to be $26,137 for 2026.** This figure is derived from a GDP (PPP) of $72 billion, which accounts for the informal economy and any base year effects, and a population of 2.7 million.
GDP per capita (PPP based) is a crucial economic metric that measures a country's economic output per person. It's calculated by converting a nation's Gross Domestic Product (GDP) into international dollars using Purchasing Power Parity (PPP) exchange rates, which reflect the actual cost of living within a country. This adjusted GDP figure is then divided by the total population to determine the average economic output per individual.
Albania's data is highlighted in the table below, use the filter and sort order options to allow easy comparison with other countries.
Data source: World Economics Research, London
**Filter:**
[All](javascript:__doPostBack('ctl00$cphPageContents$lbFilterAll',''))
[Africa](javascript:__doPostBack('ctl00$cphPageContents$lbFilterAfrica',''))
[Asia Pacific](javascript:__doPostBack('ctl00$cphPageContents$lbFilterAsiaPacific',''))
[Americas](javascript:__doPostBack('ctl00$cphPageContents$lbFilterAmericas',''))
[Europe](javascript:__doPostBack('ctl00$cphPageContents$lbFilterEurope',''))
More...
*   **Thematic Groupings**
[Global South](javascript:__doPostBack('ctl00$cphPageContents$lbFilterMoreGlobalSouth',''))
[Global North](javascript:__doPostBack('ctl00$cphPageContents$lbFilterMoreGlobalNorth',''))
* * *
[Emerging Markets](javascript:__doPostBack('ctl00$cphPageContents$lbFilterMoreEmergingMarkets',''))
[Frontier Markets](javascript:__doPostBack('ctl00$cphPageContents$lbFilterMoreFrontierMarkets',''))
[Developed Markets](javascript:__doPostBack('ctl00$cphPageContents$lbFilterMoreDevelopedMarkets',''))
</excerpt>
### Rank 4 of 161 — 0.14
<excerpt title="Albania GDP per Capita | 2025 | 2026 | Data">
# Albania's GDP PPP per Capita
[Rest of World](javascript:__doPostBack('ctl00$cphPageContents$lbFilterMoreRestOfWorld',''))
* * *
[High Income Countries](javascript:__doPostBack('ctl00$cphPageContents$lbFilterMoreHighIncomeCountries',''))
[Middle Income Countries](javascript:__doPostBack('ctl00$cphPageContents$lbFilterMoreMiddleIncomeCountries',''))
[Low Income Countries](javascript:__doPostBack('ctl00$cphPageContents$lbFilterMoreLowIncomeCountries',''))
* * *
[Bottom Billion](javascript:__doPostBack('ctl00$cphPageContents$lbFilterMoreBottomBillion','')) **Trade & Political Blocs**
[European Union](javascript:__doPostBack('ctl00$cphPageContents$lbFilterMoreEU',''))
[ASEAN](javascript:__doPostBack('ctl00$cphPageContents$lbFilterMoreASEAN',''))
[RCEP](javascript:__doPostBack('ctl00$cphPageContents$lbFilterMoreRCEP',''))
[CPTPP](javascript:__doPostBack('ctl00$cphPageContents$lbFilterMoreCPTPP',''))
[BRICS](javascript:__doPostBack('ctl00$cphPageContents$lbFilterMoreBRICS',''))
**Forums**
[OECD](javascript:__doPostBack('ctl00$cphPageContents$lbFilterMoreOECD',''))
[G7](javascript:__doPostBack('ctl00$cphPageContents$lbFilterMoreG7',''))
[G20](javascript:__doPostBack('ctl00$cphPageContents$lbFilterMoreG20',''))
[IPEF](javascript:__doPostBack('ctl00$cphPageContents$lbFilterMoreIPEF',''))
[Commonwealth](javascript:__doPostBack('ctl00$cphPageContents$lbFilterMoreCommonwealth',''))
* * *
Omit countries with poor quality GDP data: - [x]
Omit countries with poor quality governance: - [x]
* * *
How to use filters [Reset all filters](javascript:__doPostBack('ctl00$cphPageContents$lbResetFilters',''))
GDP Per Capita (PPP, Int$, 2021 Constant Prices)Estimate
(2025)Estimate
</excerpt>
### Rank 5 of 161 — 0.14
<excerpt title="Rebasing 'Maddison': new income comparisons and the shape of long- ...">
## [PDF page 27]
Chile  3622  2836  0.32  0.23  
Colombia  2784  2874  0.24  0.23  
Costa Rica  3137  3240  0.27  0.26
Dominican Republic  2006  1601  0.18  0.13
Ecuador  2583  2509  0.23  0.20  
El Salvador  1418  1204  0.12  0.10  
Guatemala  2324  1529  0.20  0.12
Honduras  1204  1334  0.11  0.11
Panama  3220  2345  0.28  0.19  
Paraguay  2108  1481  0.18  0.12  
Peru  2663  1634  0.23  0.13
Uruguay  4180  3771  0.37  0.30
Venezuela  6317  4625  0.55  0.37
United States  11448  12468  1.00  1.00
Sources: see Tables 1 and 2
27

## [PDF page 28]
Notes: GDP  per  capita  in  USD  (PPP)  is  computed  as  GDP  per  capita  in  USD  (XR)  from  Table  1  divided  by  the  
GDP price level from Table 2. For example, the ‘Original’ estimate for Argentina is computed as 7384/1.42=5210,  
while the ‘Rebased’ estimate is computed as 11100/1.71=6488.
Table C1 showed  the  impact  of  GDP per  capita  revisions  and  Table  C2 showed  the  impact  of  
changes  in PPP  computation  methods.  Table C3  combines  these  two  factors  in  estimates  of  
PPP-converted  GDP  per  capita.  As  the  final  two  columns  show,  the  combination  of  factors  
result in lower levels of GDP per capita relative to the United States, with the changes from GK  
to GEKS PPPs as the most systematic factor. Heterogeneity across countries is substantial, with  
Colombia’s  relative  income  level  remaining  almost  unchanged,  while  Peru’s  relative  income  
level  declines  from  23  percent  to  13  percent  of  the  US  level.  This  heterogeneity  is  primarily  
due to differences in GDP per capita revisions (Table 1): in Columbia GDP per capita has been  
revised upwards, while in Peru it has been revised downwards.
Table  C4.  GDP  per  capita  in  PPP-converted  2011  US  dollars  for  16  Latin  American  
countries – 1800-2011
1800  1850  1900  1950  1980  2011
Argentina  2312  2835  5887  9121  15409  20003
</excerpt>

## Search 3 — query: "Albania 2022 GDP per capita Maddison Project Our World in Data"
### Rank 1 of 78 — 0.54 (passed on)
<excerpt title="GDP per capita, 2025">
# GDP per capita 2025
## Select countries and regions
*    - [x]  Kazakhstan   $37,851   
*    - [x]  Panama   $37,516   
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
*    - [x]  North Macedonia   $25,095   
*    - [x]  China   $25,067   
*    - [x]  Dominican Republic   $24,543   
*    - [x]  Saint Lucia   $24,503   
*    - [x]  Maldives   $24,401   
*    - [x]  Albania   $22,724   
*    - [x]  Thailand   $22,432
</excerpt>
### Rank 2 of 78 — 0.42
<excerpt title="Gross domestic product (GDP), 2022">
# Gross domestic product (GDP)2022
## Select countries and regions
*    - [x]  Estonia   $40B   
*    - [x]  Armenia   $39.7B   
*    - [x]  Botswana   $39.3B   
*    - [x]  Madagascar   $38.6B   
*    - [x]  Trinidad and Tobago   $37.5B   
*    - [x]  Burkina Faso   $37.3B   
*    - [x]  Albania   $36.2B   
*    - [x]  Luxembourg   $36.1B   
*    - [x]  Gabon   $36B   
*    - [x]  Cyprus   $34.3B   
*    - [x]  Benin   $33.3B   
*    - [x]  Nicaragua   $32.8B   
*    - [x]  Kyrgyzstan   $31.7B   
*    - [x]  Mozambique   $31.4B   
*    - [x]  Mali   $30.6B   
*    - [x]  North Macedonia   $28.8B   
*    - [x]  Rwanda   $28.5B   
*    - [x]  Mauritius   $27B   
*    - [x]  Malawi   $26.5B   
*    - [x]  Zimbabwe   $25.9B   
*    - [x]  Niger   $24.8B   
*    - [x]  Chad   $24.1B   
*    - [x]  Palestine   $24.1B   
*    - [x]  Moldova   $23.8B   
*    - [x]  Congo   $23.7B   
*    - [x]  Guinea   $23.7B   
*    - [x]  Namibia   $21.9B   
*    - [x]  Equatorial Guinea   $20.2B   
*    - [x]  Jamaica   $20B   
*    - [x]  Malta   $18.3B
</excerpt>
### Rank 3 of 78 — 0.29
<excerpt title="GDP per capita: Comparing data from World Bank and Maddison Project ...">
# GDP per capita: Comparing data from World Bank and Maddison Project Database, 2022
Our World in Data
*   Browse by topic   
*   Data  
*   Latest  
*   Resources   
*   About
Subscribe
Donate

# GDP per capita: Comparing data from World Bank and Maddison Project Database 2022
This data is adjusted for inflation and differences in living costs between countries.
Table
Scatter
Settings
1990 2022
**Data source:** Eurostat, OECD, IMF, and World Bank (2026); Bolt and van Zanden – Maddison Project Database 2023 – Learn more about this data
**Note:** This data is expressed in international-$ at 2021 prices.
OurWorldinData.org/economic-growth | CC BY
*      
*      
*

# GDP per capita: Comparing data from World Bank and Maddison Project Database 2022
## Select countries and regions
Search for a country or region
Sort by: Name
All countries and regions

# GDP per capita: Comparing data from World Bank and Maddison Project Database 2022
## Select countries and regions
*   - [x]  South Korea      
*   - [x]  Afghanistan      
*   - [x]  Albania      
*   - [x]  Algeria      
*   - [x]  Angola      
*   - [x]  Argentina      
*   - [x]  Armenia      
*   - [x]  Australia      
*   - [x]  Austria      
*   - [x]  Azerbaijan      
*   - [x]  Bahrain      
*   - [x]  Bangladesh      
*   - [x]  Barbados      
*   - [x]  Belarus      
*   - [x]  Belgium      
*   - [x]  Benin      
*   - [x]  Bolivia      
*   - [x]  Bosnia and Herzegovina      
*   - [x]  Botswana      
*   - [x]  Brazil      
*   - [x]  Bulgaria      
*   - [x]  Burkina Faso      
*   - [x]  Burundi      
*   - [x]  Cambodia      
*   - [x]  Cameroon      
*   - [x]  Canada      
*   - [x]  Cape Verde      
*   - [x]  Central African Republic      
*   - [x]  Chad      
*   - [x]  Chile      
*   - [x]  China      
*   - [x]  Colombia      
*   - [x]  Comoros      
*   - [x]  Congo      
*   - [x]  Costa Rica      
*   - [x]  Cote d'Ivoire      
*   - [x]  Croatia      
*   - [x]  Cyprus      
*   - [x]  Czechia      
*   - [x]  Democratic Republic of Congo      
*   - [x]  Denmark      
*   - [x]  Djibouti      
*   - [x]  Dominica      
*   - [x]  Dominican Republic      
*   - [x]  Ecuador      
*   - [x]  Egypt      
*   - [x]  El Salvador      
*   - [x]  Equatorial Guinea      
*   - [x]  Estonia
</excerpt>
### Rank 4 of 78 — 0.27
<excerpt title="GDP per capita: Comparing data from World Bank and Maddison Project ...">
# GDP per capita: Comparing data from World Bank and Maddison Project Database 2022
## Select countries and regions
*   - [x]  South Korea      
*   - [x]  Afghanistan      
*   - [x]  Albania      
*   - [x]  Algeria      
*   - [x]  Angola      
*   - [x]  Argentina      
*   - [x]  Armenia      
*   - [x]  Australia      
*   - [x]  Austria      
*   - [x]  Azerbaijan      
*   - [x]  Bahrain      
*   - [x]  Bangladesh      
*   - [x]  Barbados      
*   - [x]  Belarus      
*   - [x]  Belgium      
*   - [x]  Benin      
*   - [x]  Bolivia      
*   - [x]  Bosnia and Herzegovina      
*   - [x]  Botswana      
*   - [x]  Brazil      
*   - [x]  Bulgaria      
*   - [x]  Burkina Faso      
*   - [x]  Burundi      
*   - [x]  Cambodia      
*   - [x]  Cameroon      
*   - [x]  Canada      
*   - [x]  Cape Verde      
*   - [x]  Central African Republic      
*   - [x]  Chad      
*   - [x]  Chile      
*   - [x]  China      
*   - [x]  Colombia      
*   - [x]  Comoros      
*   - [x]  Congo      
*   - [x]  Costa Rica      
*   - [x]  Cote d'Ivoire      
*   - [x]  Croatia      
*   - [x]  Cyprus      
*   - [x]  Czechia      
*   - [x]  Democratic Republic of Congo      
*   - [x]  Denmark      
*   - [x]  Djibouti      
*   - [x]  Dominica      
*   - [x]  Dominican Republic      
*   - [x]  Ecuador      
*   - [x]  Egypt      
*   - [x]  El Salvador      
*   - [x]  Equatorial Guinea      
*   - [x]  Estonia
</excerpt>
### Rank 5 of 78 — 0.23
<excerpt title="GDP per capita vs. Electoral Democracy Index, 2022">
All countries and regions

*   South Korea   
*   Afghanistan   
*   Albania   
*   Algeria   
*   Angola   
*   Argentina   
*   Armenia   
*   Australia   
*   Austria   
*   Azerbaijan   
*   Bahrain   
*   Bangladesh   
*   Barbados   
*   Belarus   
*   Belgium   
*   Benin   
*   Bolivia   
*   Bosnia and Herzegovina   
*   Botswana   
*   Brazil   
*   Bulgaria   
*   Burkina Faso   
*   Burundi   
*   Cambodia   
*   Cameroon   
*   Canada   
*   Cape Verde   
*   Central African Republic   
*   Chad   
*   Chile   
*   China   
*   Colombia   
*   Comoros   
*   Congo   
*   Costa Rica   
*   Cote d'Ivoire   
*   Croatia   
*   Cuba   
*   Cyprus   
*   Czechia   
*   Democratic Republic of Congo   
*   Denmark   
*   Djibouti   
*   Dominican Republic   
*   Ecuador   
*   Egypt   
*   El Salvador   
*   Equatorial Guinea   
*   Estonia   
*   Eswatini   
*   Ethiopia   
*   Finland   
*   France   
*   Gabon   
*   Gambia   
*   Georgia   
*   Germany   
*   Ghana   
*   Greece   
*   Guatemala   
*   Guinea   
*   Guinea-Bissau   
*   Haiti   
*   Honduras   
*   Hong Kong   
*   Hungary   
*   Iceland   
*   India   
*   Indonesia   
*   Iran   
*   Iraq   
*   Ireland   
*   Israel   
*   Italy   
*   Jamaica   
*   Japan   
*   Jordan   
*   Kazakhstan   
*   Kenya   
*   Kuwait   
*   Kyrgyzstan   
*   Laos   
*   Latvia   
*   Lebanon   
*   Lesotho   
*   Liberia   
*   Libya   
*   Lithuania   
*   Luxembourg   
*   Madagascar   
*   Malawi   
*   Malaysia   
*   Mali   
*   Malta   
*   Mauritania   
*   Mauritius   
*   Mexico   
*   Moldova   
*   Mongolia   
*   Montenegro   
*   Morocco   
*   Mozambique   
*   Myanmar   
*   Namibia   
*   Nepal   
*   Netherlands   
*   New Zealand   
*   Nicaragua   
*   Niger   
*   Nigeria   
*   North Korea   
*   North Macedonia   
*   Norway   
*   Oman
</excerpt>

## Search 4 — query: "Albania real GDP per capita 1985 Maddison Project 2011 US$"
### Rank 1 of 224 — 0.31 (passed on)
<excerpt title="Albania Economy: GDP, Inflation and Historical Data">
Economic AtlasEurope & Central Asia Albania
Country data profile

## Albania: economic indicators
Historical output, prices, jobs, trade, population and market data.
Region**Europe & Central Asia**
Income group**Upper middle income**
Currency**Albanian lek**
Data updated**Nov 6, 2026**
Key figuresData explorerMore seriesSources

## Key figures
Latest published observations · coverage through 2025
Interactive data explorer

## GDP and economic indicators
Add countries or measures to the same chart. Hover for exact values and drag the lower timeline to change the date range.
Up to 12 series
Country Indicator
🇦🇱 Albania
GDP
Published values share one scale. Use this mode when the selected indicators have comparable units.
*   Albania · GDP
**About this chart** Gross domestic product is the total income earned through the production of goods and services in an economic territory during an accounting period. It can be measured in three different ways: using either the expenditure approach, the income approach, or the production approach. This indicator is expressed in current prices, meaning no adjustment has been made to account for price changes over time. This indicator is expressed in United States dollars.
Default measure GDP, current US$
Latest observation 2025
Source World Bank WDI
Forecasts Not included
Latest data

## More indicators
Browse all indicators →
Detailed statistics

## Economic history
Observed data and published historical estimates. Missing years are not treated as zero.

## Economic history
### Long-run GDP per person
Maddison Project Database · real 2011 US$
*   Real GDP per person

## Economic history
### GDP per person
Current US dollars
*   GDP per person

## Economic history
### Growth and prices
Annual percentage change
*   GDP growth  
*   Inflation

## Economic history
### Trade openness
Exports and imports as a share of GDP
*   Exports  
*   Imports

## Economic history
### Jobs and labor force
Modeled ILO estimates where available
*   Unemployment  
*   Labor-force participation

## Economic history
### Share prices
Representative national index where available
No observations are available for this chart.

## Economic history
### Debt and investment
Share of GDP
*   Government debt / GDP  
*   FDI inflows / GDP
Data & methodology

## Sources for this profile
Each line keeps its source definition, unit and observation year.
</excerpt>
### Rank 2 of 224 — 0.23
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
### Rank 3 of 224 — 0.17
<excerpt title="Albania Real GDP 2025">
# Albania GDP: $16bn
## Get World Economics Data Alerts & Insights by Email
Register your email address to receive the latest data and analysis for Albania and other countries.

# Albania GDP: $16bn
## Key Indicators for Albania
Comprehensive economic data including GDP, growth rates, debt levels, and population figures
Indicator Value Year See more  
GDP Data Quality Rating B 2025View  
Population Data Quality Rating B 2025View  
Governance Rating C 2025View
GDP (PPP)
Base Year Adjusted + Informal Economy$69bn 2025View  
GDP (Current / Nominal Prices)$25bn 2025View  
GDP (Constant Prices / Real)$16bn 2025View  
GDP Growth Rate 3.4%2025View  
GDP Debt to GDP Ratio 40.6%2025View
GDP per Capita (PPP)
Base Year Adjusted + Informal Economy$25,043 2025View  
GDP per Capita (Current / Nominal)$9,276 2025View  
GDP per Capita (Constant / Real)$5,863 2025View  
GDP per Capita Growth Rate 4.1%2025View
Population Size 2.79 million 2025View  
Fertility Rate 1.2%2025View  
Workforce Size 1.22 million 2025View
Carbon Emissions (per Capita)1.83 tCO2e 2023View  
Methane Emissions (per Capita)0.87 tCO2e 2023View  
See all indicators
ACCESS DATA FOR MORE COUNTRIES
Please read our Terms of Service and Disclaimer relating to data on this page.
**Explore More Countries**
</excerpt>
### Rank 4 of 224 — 0.16
<excerpt title="[OC] Real GDP per capita in 2011 USD since 1800 for selected countries, log ...">
# [OC] Real GDP per capita in 2011 USD since 1800 for selected countries, log scale. Source: Maddison Project Database, 2020. Created using Google Sheets. : r/dataisbeautiful
Skip to main content[OC] Real GDP per capita in 2011 USD since 1800 for selected countries, log scale. Source: Maddison Project Database, 2020. Created using Google Sheets. : r/dataisbeautiful
Open menu Open navigationGo to Reddit Home
r/dataisbeautiful
Sign UpSign up for RedditLog InLog in to Reddit
Expand user menu Open settings menu
Go to dataisbeautiful
r/dataisbeautiful•5y ago
u/LeroyoJenkins

# [OC] Real GDP per capita in 2011 USD since 1800 for selected countries, log scale. Source: Maddison Project Database, 2020. Created using Google Sheets.
OC
![Image 2: r/dataisbeautiful - [OC] Real GDP per capita in 2011 USD since 1800 for selected countries, log scale. Source: Maddison Project Database, 2020. Created using Google Sheets.](https://preview.redd.it/real-gdp-per-capita-in-2011-usd-since-1800-for-selected-v0-xiyrze3va7871.png?width=640&crop=smart&auto=webp&s=b7c4fb3106e4ecb52a196385c1dd0b81bee12188)![Image 3: r/dataisbeautiful - [OC] Real GDP per capita in 2011 USD since 1800 for selected countries, log scale. Source: Maddison Project Database, 2020. Created using Google Sheets.](https://preview.redd.it/real-gdp-per-capita-in-2011-usd-since-1800-for-selected-v0-xiyrze3va7871.png?width=640&crop=smart&auto=webp&s=b7c4fb3106e4ecb52a196385c1dd0b81bee12188)
![Image 4: r/dataisbeautiful - [OC] Real GDP per capita in 2011 USD since 1800 for selected countries, log scale. Source: Maddison Project Database, 2020. Created using Google Sheets.](https://i.redd.it/xiyrze3va7871.png)
Archived post. New comments cannot be posted and votes cannot be cast.
Share
Leverage_Shares•Ad
Introducing the Anthropic Daily ETFs: ANUU for 2x long exposure and ANDD for 2x short exposure.
Learn More
leverageshares.com
u/airbnb•Ad

# [OC] Real GDP per capita in 2011 USD since 1800 for selected countries, log scale. Source: Maddison Project Database, 2020. Created using Google Sheets.
Over 8 million listings. Over 220 countries. One easy place to book.
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
</excerpt>
### Rank 5 of 224 — 0.16
<excerpt title="Rebasing 'Maddison': new income comparisons and the shape of long- ...">
## [PDF page 27]
Chile  3622  2836  0.32  0.23  
Colombia  2784  2874  0.24  0.23  
Costa Rica  3137  3240  0.27  0.26
Dominican Republic  2006  1601  0.18  0.13
Ecuador  2583  2509  0.23  0.20  
El Salvador  1418  1204  0.12  0.10  
Guatemala  2324  1529  0.20  0.12
Honduras  1204  1334  0.11  0.11
Panama  3220  2345  0.28  0.19  
Paraguay  2108  1481  0.18  0.12  
Peru  2663  1634  0.23  0.13
Uruguay  4180  3771  0.37  0.30
Venezuela  6317  4625  0.55  0.37
United States  11448  12468  1.00  1.00
Sources: see Tables 1 and 2
27

## [PDF page 28]
Notes: GDP  per  capita  in  USD  (PPP)  is  computed  as  GDP  per  capita  in  USD  (XR)  from  Table  1  divided  by  the  
GDP price level from Table 2. For example, the ‘Original’ estimate for Argentina is computed as 7384/1.42=5210,  
while the ‘Rebased’ estimate is computed as 11100/1.71=6488.
Table C1 showed  the  impact  of  GDP per  capita  revisions  and  Table  C2 showed  the  impact  of  
changes  in PPP  computation  methods.  Table C3  combines  these  two  factors  in  estimates  of  
PPP-converted  GDP  per  capita.  As  the  final  two  columns  show,  the  combination  of  factors  
result in lower levels of GDP per capita relative to the United States, with the changes from GK  
to GEKS PPPs as the most systematic factor. Heterogeneity across countries is substantial, with  
Colombia’s  relative  income  level  remaining  almost  unchanged,  while  Peru’s  relative  income  
level  declines  from  23  percent  to  13  percent  of  the  US  level.  This  heterogeneity  is  primarily  
due to differences in GDP per capita revisions (Table 1): in Columbia GDP per capita has been  
revised upwards, while in Peru it has been revised downwards.
Table  C4.  GDP  per  capita  in  PPP-converted  2011  US  dollars  for  16  Latin  American  
countries – 1800-2011
1800  1850  1900  1950  1980  2011
Argentina  2312  2835  5887  9121  15409  20003
</excerpt>

## Search 5 — query: "Albania 1985 gdp per capita 2011 US$ Maddison"
### Rank 1 of 2667 — 0.72 (passed on)
<excerpt title="https://www.ers.usda.gov/media/6159/historical-and...">
CSV columns (first row): Observation,Category,Year,Unit,Value
```
Albania,Country,1973,Real GDP Per Capita in 2017 USD,1651.2461
```
```
Albania,Country,1974,Real GDP Per Capita in 2017 USD,1678.6183
```
```
Albania,Country,1975,Real GDP Per Capita in 2017 USD,1707.9681
```
```
Albania,Country,1976,Real GDP Per Capita in 2017 USD,1737.9182
```
```
Albania,Country,1977,Real GDP Per Capita in 2017 USD,1765.4679
```
```
Albania,Country,1978,Real GDP Per Capita in 2017 USD,1802.386
```
```
Albania,Country,1979,Real GDP Per Capita in 2017 USD,1834.8916
```
```
Albania,Country,1980,Real GDP Per Capita in 2017 USD,1856.0826
```
```
Albania,Country,1981,Real GDP Per Capita in 2017 USD,1924.6429
```
```
Albania,Country,1982,Real GDP Per Capita in 2017 USD,1941.6061
```
```
Albania,Country,1983,Real GDP Per Capita in 2017 USD,1923.472
```
```
Albania,Country,1984,Real GDP Per Capita in 2017 USD,1860.9095
```
```
Albania,Country,1985,Real GDP Per Capita in 2017 USD,1855.1622
```
</excerpt>
### Rank 2 of 2667 — 0.32
<excerpt title="https://www.ers.usda.gov/media/6159/historical-and...">
CSV columns (first row): Observation,Category,Year,Unit,Value
```
Albania,Country,1982,"Real GDP Per Capita in 2017 USD, Annual Growth Rate",0.8813653
```
```
Albania,Country,1983,"Real GDP Per Capita in 2017 USD, Annual Growth Rate",-0.93397075
```
```
Albania,Country,1984,"Real GDP Per Capita in 2017 USD, Annual Growth Rate",-3.2525816
```
```
Albania,Country,1985,"Real GDP Per Capita in 2017 USD, Annual Growth Rate",-0.30884439
```
```
Albania,Country,1986,"Real GDP Per Capita in 2017 USD, Annual Growth Rate",3.5794203
```
```
Albania,Country,1987,"Real GDP Per Capita in 2017 USD, Annual Growth Rate",-2.7197142
```
```
Albania,Country,1988,"Real GDP Per Capita in 2017 USD, Annual Growth Rate",-3.3534601
```
```
Albania,Country,1989,"Real GDP Per Capita in 2017 USD, Annual Growth Rate",7.8102565
```
```
Albania,Country,1990,"Real GDP Per Capita in 2017 USD, Annual Growth Rate",-10.944579
```
```
Albania,Country,1991,"Real GDP Per Capita in 2017 USD, Annual Growth Rate",-26.556385
```
```
Albania,Country,1992,"Real GDP Per Capita in 2017 USD, Annual Growth Rate",-3.8928413
```
</excerpt>
### Rank 3 of 2667 — 0.29
<excerpt title="Albania Economy: GDP, Inflation and Historical Data">
Economic AtlasEurope & Central Asia Albania
Country data profile

## Albania: economic indicators
Historical output, prices, jobs, trade, population and market data.
Region**Europe & Central Asia**
Income group**Upper middle income**
Currency**Albanian lek**
Data updated**Nov 6, 2026**
Key figuresData explorerMore seriesSources

## Key figures
Latest published observations · coverage through 2025
Interactive data explorer

## GDP and economic indicators
Add countries or measures to the same chart. Hover for exact values and drag the lower timeline to change the date range.
Up to 12 series
Country Indicator
🇦🇱 Albania
GDP
Published values share one scale. Use this mode when the selected indicators have comparable units.
*   Albania · GDP
**About this chart** Gross domestic product is the total income earned through the production of goods and services in an economic territory during an accounting period. It can be measured in three different ways: using either the expenditure approach, the income approach, or the production approach. This indicator is expressed in current prices, meaning no adjustment has been made to account for price changes over time. This indicator is expressed in United States dollars.
Default measure GDP, current US$
Latest observation 2025
Source World Bank WDI
Forecasts Not included
Latest data

## More indicators
Browse all indicators →
Detailed statistics

## Economic history
Observed data and published historical estimates. Missing years are not treated as zero.

## Economic history
### Long-run GDP per person
Maddison Project Database · real 2011 US$
*   Real GDP per person

## Economic history
### GDP per person
Current US dollars
*   GDP per person

## Economic history
### Growth and prices
Annual percentage change
*   GDP growth  
*   Inflation

## Economic history
### Trade openness
Exports and imports as a share of GDP
*   Exports  
*   Imports

## Economic history
### Jobs and labor force
Modeled ILO estimates where available
*   Unemployment  
*   Labor-force participation

## Economic history
### Share prices
Representative national index where available
No observations are available for this chart.

## Economic history
### Debt and investment
Share of GDP
*   Government debt / GDP  
*   FDI inflows / GDP
Data & methodology

## Sources for this profile
Each line keeps its source definition, unit and observation year.
</excerpt>
### Rank 4 of 2667 — 0.25
<excerpt title="https://www.ers.usda.gov/media/6159/historical-and...">
CSV columns (first row): Observation,Category,Year,Unit,Value
```
Albania,Country,1999,Real GDP Per Capita in 2017 USD,1894.5582
```
```
Albania,Country,2000,Real GDP Per Capita in 2017 USD,2044.7478
```
```
Albania,Country,2001,Real GDP Per Capita in 2017 USD,2235.8101
```
```
Albania,Country,2002,Real GDP Per Capita in 2017 USD,2361.0996
```
```
Albania,Country,2003,Real GDP Per Capita in 2017 USD,2518.7065
```
```
Albania,Country,2004,Real GDP Per Capita in 2017 USD,2685.855
```
```
Albania,Country,2005,Real GDP Per Capita in 2017 USD,2865.0835
```
```
Albania,Country,2006,Real GDP Per Capita in 2017 USD,3068.4866
```
```
Albania,Country,2007,Real GDP Per Capita in 2017 USD,3287.8247
```
```
Albania,Country,2008,Real GDP Per Capita in 2017 USD,3569.9287
```
```
Albania,Country,2009,Real GDP Per Capita in 2017 USD,3726.3708
```
```
Albania,Country,2010,Real GDP Per Capita in 2017 USD,3901.3621
```
```
Albania,Country,2011,Real GDP Per Capita in 2017 USD,4034.396
```
</excerpt>
### Rank 5 of 2667 — 0.25
<excerpt title="https://www.ers.usda.gov/media/6159/historical-and...">
CSV columns (first row): Observation,Category,Year,Unit,Value
```
Albania,Country,1986,Real GDP Per Capita in 2017 USD,1921.5663
```
```
Albania,Country,1987,Real GDP Per Capita in 2017 USD,1869.3052
```
```
Albania,Country,1988,Real GDP Per Capita in 2017 USD,1806.6188
```
```
Albania,Country,1989,Real GDP Per Capita in 2017 USD,1947.7203
```
```
Albania,Country,1990,Real GDP Per Capita in 2017 USD,1734.5505
```
```
Albania,Country,1991,Real GDP Per Capita in 2017 USD,1273.9166
```
```
Albania,Country,1992,Real GDP Per Capita in 2017 USD,1224.3251
```
```
Albania,Country,1993,Real GDP Per Capita in 2017 USD,1343.8687
```
```
Albania,Country,1994,Real GDP Per Capita in 2017 USD,1434.4541
```
```
Albania,Country,1995,Real GDP Per Capita in 2017 USD,1601.3693
```
```
Albania,Country,1996,Real GDP Per Capita in 2017 USD,1722.3103
```
```
Albania,Country,1997,Real GDP Per Capita in 2017 USD,1523.8575
```
```
Albania,Country,1998,Real GDP Per Capita in 2017 USD,1664.932
```
</excerpt>

## Search 6 — query: "Albania gdp per capita 1985 ourworldindata"
### Rank 1 of 354 — 0.74 (passed on)
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
### Rank 2 of 354 — 0.63
<excerpt title="List of countries by past and projected GDP (nominal) per capita">
Albania	4,098	4,440	4,274	4,496	4,585	4,182	4,473	4,988	5,861	6,022  
 Algeria	4,941	5,946	6,058	5,998	6,109	4,692	4,427	4,554	4,568	4,453  
 Andorra	49,030	51,957	45,714	45,630	46,299	38,877	39,595	40,018	42,230	40,688  
 Angola	4,102	5,184	5,702	5,876	6,055	4,676	3,991	4,694	3,689	2,941  
 Antigua and Barbuda	15,343	15,045	15,724	15,051	15,423	15,839	16,164	16,401	17,471	17,899  
 Argentina	10,413	12,788	13,890	14,489	13,209	14,895	12,773	14,618	11,786	9,942  
 Armenia	3,066	3,354	3,622	3,690	3,864	3,527	3,540	3,883	4,205	4,599
</excerpt>
### Rank 3 of 354 — 0.62
<excerpt title="List of countries by past and projected GDP (nominal) per capita">
Palestine	2,406	2,712	2,889	3,123	3,159	3,084	3,326	3,407	3,353	3,443  
 Yemen					1,046	732	688	701	749	813  
 Zambia	1,451	1,625	1,710	1,821	1,708	1,296	1,239	1,483	1,464	1,259  
 Zimbabwe	1,399	1,616	1,851	1,992	2,050	1,998	2,036	2,115	3,602	2,605  
2020sedit  
IMF estimates (2020s)[1][2]  
Country / territory	2020	2021	2022	2023	2024	2025	2026	2027	2028	2029  
 Afghanistan	517	356	357	416	418	450  
 Albania	6,024	7,191	7,816	9,803	11,391	12,814	13,968	14,957	15,977	17,054  
 Algeria	3,724	4,136	4,946	5,353	5,749	5,997	6,910	6,975	6,875	6,780
</excerpt>
### Rank 4 of 354 — 0.60
<excerpt title="List of countries by past and projected GDP (nominal) per capita">
South Yemen	106	95	105	84	88	87	111	133	157	164  
 Yugoslavia	721	776	803	1,037	1,422	1,579	1,768	2,131	2,513	3,128  
 Zambia	369	363	413	506	602	533	545	518	560	668  
 Zimbabwe	388	434	518	616	716	760	728	712	689	791  
1980sedit  
Country / territory	1980	1981	1982	1983	1984	1985	1986	1987	1988	1989  
 Afghanistan	276	268	271	277	282	286	290	255	234	288  
 Albania	799	810	818	811	784	783	788	762	770	904  
 Algeria	2,185	2,219	2,192	2,294	2,413	2,564	2,707	2,690	2,385	2,191  
 Andorra	15,662	13,124	12,161	10,152	9,780	9,838	13,112	15,962	18,101	19,191
</excerpt>
### Rank 5 of 354 — 0.57
<excerpt title="List of countries by past and projected GDP (nominal) per capita">
IMF estimatesedit  
1980sedit  
IMF estimates (1980s)[1]  
Country / territory	1980	1981	1982	1983	1984	1985	1986	1987	1988	1989  
 Afghanistan										  
 Albania	728	818	825	816	788	789	856	832	805	861  
 Algeria	2,462	2,502	2,447	2,514	2,640	2,989	2,929	2,936	2,327	2,309  
 Andorra										  
 Angola	1,074	978	953	968	1,000	1,093	995	1,109	1,171	1,326  
 Antigua and Barbuda	1,935	2,200	2,479	2,794	3,260	3,849	4,731	5,612	6,757	7,545  
 Argentina	8,361	6,671	3,258	3,963	4,375	3,249	3,857	3,910	4,524	2,867  
 Armenia										  
 Aruba										  
 Australia	11,021	12,544	12,250	11,606	12,591	10,981	11,259	13,015	16,266	18,232
</excerpt>

## Search 7 — query: ""gdp-per-capita-maddison-project-database" Albania 1985"
### Rank 1 of 1166 — 0.66 (passed on)
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
### Rank 2 of 1166 — 0.48
<excerpt title="https://ourworldindata.org/grapher/gdp-per-capita-...">
CSV columns (first row): Entity,Code,Year,GDP per capita,GDP per capita (Annotations)
```
Algeria,DZA,1984,5361,
```
```
Algeria,DZA,1985,5469,
```
```
Algeria,DZA,1986,5262,
```
```
Algeria,DZA,1987,5088,
```
```
Algeria,DZA,1988,4850,
```
```
Algeria,DZA,1989,4889,
```
```
Algeria,DZA,1990,4697,
```
```
Algeria,DZA,1991,4708.232,
```
```
Algeria,DZA,1992,4850.223,
```
```
Algeria,DZA,1993,4816.924,
```
```
Algeria,DZA,1994,4856.9854,
```
```
Algeria,DZA,1995,5142.384,
```
```
Algeria,DZA,1996,5451.6343,
```
```
Algeria,DZA,1997,5638.48,
```
```
Algeria,DZA,1998,6069.7773,
```
```
Algeria,DZA,1999,6421.5083,
```
```
Algeria,DZA,2000,6834.5537,
```
```
Algeria,DZA,2001,7218.2456,
```
```
Algeria,DZA,2002,7814.8384,
```
```
Algeria,DZA,2003,8590.178,
```
</excerpt>
### Rank 3 of 1166 — 0.41
<excerpt title="https://ourworldindata.org/grapher/gdp-per-capita-...">
CSV columns (first row): Entity,Code,Year,GDP per capita,GDP per capita (Annotations)
```
Albania,ALB,1998,3873.373,
```
```
Albania,ALB,1999,4432.0425,
```
```
Albania,ALB,2000,4808.4795,
```
```
Albania,ALB,2001,5285.809,
```
```
Albania,ALB,2002,5608.9624,
```
```
Albania,ALB,2003,6004.645,
```
```
Albania,ALB,2004,6419.8706,
```
```
Albania,ALB,2005,6858.4673,
```
```
Albania,ALB,2006,7347.33,
```
```
Albania,ALB,2007,7866.1577,
```
```
Albania,ALB,2008,8522.13,
```
```
Albania,ALB,2009,8859.472,
```
```
Albania,ALB,2010,9222.973,
```
```
Albania,ALB,2011,9484,
```
```
Albania,ALB,2012,9634.334,
```
```
Albania,ALB,2013,9748.728,
```
```
Albania,ALB,2014,9942.276,
```
```
Albania,ALB,2015,10192.529,
```
</excerpt>
### Rank 4 of 1166 — 0.39
<excerpt title="https://ourworldindata.org/grapher/gdp-per-capita-...">
CSV columns (first row): Entity,Code,Year,GDP per capita,GDP per capita (Annotations)
```
Argentina,ARG,1963,8695,
```
```
Argentina,ARG,1964,9446,
```
```
Argentina,ARG,1965,10155,
```
```
Argentina,ARG,1966,10076,
```
```
Argentina,ARG,1967,10200,
```
```
Argentina,ARG,1968,10485,
```
```
Argentina,ARG,1969,11217,
```
```
Argentina,ARG,1970,11639,
```
```
Argentina,ARG,1971,12003,
```
```
Argentina,ARG,1972,12170,
```
```
Argentina,ARG,1973,12691,
```
```
Argentina,ARG,1974,13284,
```
```
Argentina,ARG,1975,12946,
```
```
Argentina,ARG,1976,12696,
```
```
Argentina,ARG,1977,13236,
```
```
Argentina,ARG,1978,12444,
```
```
Argentina,ARG,1979,13114,
```
```
Argentina,ARG,1980,13080,
```
```
Argentina,ARG,1981,12125,
```
```
Argentina,ARG,1982,11550,
```
```
Argentina,ARG,1983,11775,
```
```
Argentina,ARG,1984,11837,
```
```
Argentina,ARG,1985,10895,
```
```
Argentina,ARG,1986,11515,
```
</excerpt>
### Rank 5 of 1166 — 0.30
<excerpt title="https://ourworldindata.org/grapher/gdp-per-capita-...">
CSV columns (first row): Entity,Code,Year,GDP per capita,GDP per capita (Annotations)
```
Angola,AGO,1974,2727,
```
```
Angola,AGO,1975,1710,
```
```
Angola,AGO,1976,1521,
```
```
Angola,AGO,1977,1500,
```
```
Angola,AGO,1978,1530,
```
```
Angola,AGO,1979,1527,
```
```
Angola,AGO,1980,1532,
```
```
Angola,AGO,1981,1471,
```
```
Angola,AGO,1982,1374,
```
```
Angola,AGO,1983,1288,
```
```
Angola,AGO,1984,1259,
```
```
Angola,AGO,1985,1242,
```
```
Angola,AGO,1986,1106,
```
```
Angola,AGO,1987,1211,
```
```
Angola,AGO,1988,1360,
```
```
Angola,AGO,1989,1360,
```
```
Angola,AGO,1990,1384,
```
```
Angola,AGO,1991,1437.1472,
```
```
Angola,AGO,1992,1389.3295,
```
```
Angola,AGO,1993,1080.4806,
```
```
Angola,AGO,1994,1120.8481,
```
```
Angola,AGO,1995,1319.1589,
```
```
Angola,AGO,1996,1533.9839,
```
</excerpt>

## Search 8 — query: "2022 Albania GDP per capita Maddison Project Our World in Data"
### Rank 1 of 99 — 0.65 (passed on)
<excerpt title="List of countries by GDP (nominal) per capita">
## Table
| Nauru | 16,076 | 14,640 | 15,645 |  
| Argentina | 16,021 | 14,898 | 13,970 |  
| Malaysia | 15,981 | 13,125 | 11,867 |  
| China[[n 3]](https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)_per_capita#cite_note-China-THM-12) | 15,371 | 13,862 | 13,206 |  
| Saint Lucia | 15,091 | 14,746 | 14,323 |  
| World | 14,217 | 14,406 | 13,097 |  
| Albania | 13,968 | 12,998 | 9,685 |  
| Mauritius | 13,671 | 12,991 | 11,763 |  
| Grenada | 13,298 | 12,107 | 11,705 |  
| Dominican Republic | 13,245 | 11,059 | 10,876 |  
| Brazil | 12,397 | 10,713 | 10,311 |  
| Turkmenistan | 12,291 | 6,540 | 9,161 |  
| Belarus | 11,962 | 10,279 | 8,387 |  
| North Macedonia | 11,762 | 10,490 | 9,299 |  
| Peru | 11,498 | 9,684 | 8,456 |  
| Saint Vincent and the Grenadines | 11,405 | 12,562 | 11,294 |
</excerpt>
### Rank 2 of 99 — 0.53
<excerpt title="GDP per capita, 2023">
# GDP per capita 2023
## Select countries
*    - [x]  Suriname   $16,649   
*    - [x]  Ukraine   $16,432   
*    - [x]  Saint Vincent and the Grenadines   $16,246   
*    - [x]  Dominica   $16,019   
*    - [x]  Albania   $15,969   
*    - [x]  Grenada   $15,265   
*    - [x]  Mongolia   $15,172   
*    - [x]  Paraguay   $15,007   
*    - [x]  Iran   $14,809   
*    - [x]  Algeria   $14,580   
*    - [x]  Bhutan   $14,416   
*    - [x]  Peru   $14,338   
*    - [x]  Ecuador   $14,189   
*    - [x]  Indonesia   $13,957   
*    - [x]  Fiji   $13,915   
*    - [x]  Iraq   $13,712   
*    - [x]  Vietnam   $13,055   
*    - [x]  Lebanon   $12,819   
*    - [x]  Sri Lanka   $12,740   
*    - [x]  South Africa   $12,620   
*    - [x]  Guatemala   $12,209   
*    - [x]  Tunisia   $12,112   
*    - [x]  Belize   $11,849   
*    - [x]  Moldova   $11,372   
*    - [x]  El Salvador   $11,245   
*    - [x]  Barbados   $10,831   
*    - [x]  Philippines   $10,110   
*    - [x]  Kyrgyzstan   $9,891
</excerpt>
### Rank 3 of 99 — 0.50
<excerpt title="GDP per capita, 2025">
# GDP per capita 2025
## Select countries and regions
*    - [x]  Kazakhstan   $37,851   
*    - [x]  Panama   $37,516   
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
*    - [x]  North Macedonia   $25,095   
*    - [x]  China   $25,067   
*    - [x]  Dominican Republic   $24,543   
*    - [x]  Saint Lucia   $24,503   
*    - [x]  Maldives   $24,401   
*    - [x]  Albania   $22,724   
*    - [x]  Thailand   $22,432
</excerpt>
### Rank 4 of 99 — 0.40
<excerpt title="Gross domestic product (GDP), 2022">
# Gross domestic product (GDP)2022
## Select countries and regions
*    - [x]  Estonia   $40B   
*    - [x]  Armenia   $39.7B   
*    - [x]  Botswana   $39.3B   
*    - [x]  Madagascar   $38.6B   
*    - [x]  Trinidad and Tobago   $37.5B   
*    - [x]  Burkina Faso   $37.3B   
*    - [x]  Albania   $36.2B   
*    - [x]  Luxembourg   $36.1B   
*    - [x]  Gabon   $36B   
*    - [x]  Cyprus   $34.3B   
*    - [x]  Benin   $33.3B   
*    - [x]  Nicaragua   $32.8B   
*    - [x]  Kyrgyzstan   $31.7B   
*    - [x]  Mozambique   $31.4B   
*    - [x]  Mali   $30.6B   
*    - [x]  North Macedonia   $28.8B   
*    - [x]  Rwanda   $28.5B   
*    - [x]  Mauritius   $27B   
*    - [x]  Malawi   $26.5B   
*    - [x]  Zimbabwe   $25.9B   
*    - [x]  Niger   $24.8B   
*    - [x]  Chad   $24.1B   
*    - [x]  Palestine   $24.1B   
*    - [x]  Moldova   $23.8B   
*    - [x]  Congo   $23.7B   
*    - [x]  Guinea   $23.7B   
*    - [x]  Namibia   $21.9B   
*    - [x]  Equatorial Guinea   $20.2B   
*    - [x]  Jamaica   $20B   
*    - [x]  Malta   $18.3B
</excerpt>
### Rank 5 of 99 — 0.32
<excerpt title="GDP per capita: Comparing data from World Bank and Maddison Project ...">
# GDP per capita: Comparing data from World Bank and Maddison Project Database, 2022
Our World in Data
*   Browse by topic   
*   Data  
*   Latest  
*   Resources   
*   About
Subscribe
Donate

# GDP per capita: Comparing data from World Bank and Maddison Project Database 2022
This data is adjusted for inflation and differences in living costs between countries.
Table
Scatter
Settings
1990 2022
**Data source:** Eurostat, OECD, IMF, and World Bank (2026); Bolt and van Zanden – Maddison Project Database 2023 – Learn more about this data
**Note:** This data is expressed in international-$ at 2021 prices.
OurWorldinData.org/economic-growth | CC BY
*      
*      
*

# GDP per capita: Comparing data from World Bank and Maddison Project Database 2022
## Select countries and regions
Search for a country or region
Sort by: Name
All countries and regions

# GDP per capita: Comparing data from World Bank and Maddison Project Database 2022
## Select countries and regions
*   - [x]  South Korea      
*   - [x]  Afghanistan      
*   - [x]  Albania      
*   - [x]  Algeria      
*   - [x]  Angola      
*   - [x]  Argentina      
*   - [x]  Armenia      
*   - [x]  Australia      
*   - [x]  Austria      
*   - [x]  Azerbaijan      
*   - [x]  Bahrain      
*   - [x]  Bangladesh      
*   - [x]  Barbados      
*   - [x]  Belarus      
*   - [x]  Belgium      
*   - [x]  Benin      
*   - [x]  Bolivia      
*   - [x]  Bosnia and Herzegovina      
*   - [x]  Botswana      
*   - [x]  Brazil      
*   - [x]  Bulgaria      
*   - [x]  Burkina Faso      
*   - [x]  Burundi      
*   - [x]  Cambodia      
*   - [x]  Cameroon      
*   - [x]  Canada      
*   - [x]  Cape Verde      
*   - [x]  Central African Republic      
*   - [x]  Chad      
*   - [x]  Chile      
*   - [x]  China      
*   - [x]  Colombia      
*   - [x]  Comoros      
*   - [x]  Congo      
*   - [x]  Costa Rica      
*   - [x]  Cote d'Ivoire      
*   - [x]  Croatia      
*   - [x]  Cyprus      
*   - [x]  Czechia      
*   - [x]  Democratic Republic of Congo      
*   - [x]  Denmark      
*   - [x]  Djibouti      
*   - [x]  Dominica      
*   - [x]  Dominican Republic      
*   - [x]  Ecuador      
*   - [x]  Egypt      
*   - [x]  El Salvador      
*   - [x]  Equatorial Guinea      
*   - [x]  Estonia
</excerpt>

## Search 9 — query: "Albania,ALB,2022, GDP per capita 2022, Our World in Data Maddison Project"
### Rank 1 of 44 — 0.46 (passed on)
<excerpt title="Albania GDP per Capita | Economic Indicators | CEIC">
Albania Gross Domestic Product (GDP) per Capita reached 6,867.696 USD in Dec 2022, compared with 6,412.690 USD in Dec 2021. See the table below for more data.

| Government and Public Finance | Last | Frequency | Range |  
| --- | --- | --- | --- |  
| Consolidated Fiscal Balance: % of GDP (%) | -1.8 2025 | yearly | 1997 - 2025 |  
| Consolidated Fiscal Balance (USD mn) | 769.641 Aug 2026 | monthly | Dec 1997 - Aug 2026 |  
| Tax Revenue (USD mn) | 5,009.233 Aug 2026 | monthly | Dec 1997 - Aug 2026 |  
| Tax Revenue: % of GDP (%) | 20.3 2025 | yearly | 1997 - 2025 |  
| National Government Debt (USD mn) | 15,870.8 Mar 2026 | quarterly | Sep 2010 - Mar 2026 |  
| Government Debt: % of GDP (%) | 49.4 Jun 2026 | quarterly | Sep 2010 - Jun 2026 |  
| Forecast: Government Expenditure (ALL bn) | 1,214.244 2031 | yearly | 1997 - 2031 |  
| Forecast: Government Net Debt (ALL bn) | 1,755.902 2031 | yearly | 1997 - 2031 |  
| Forecast: Government Revenue (ALL bn) | 1,127.893 2031 | yearly | 1997 - 2031 |  
| General Govt Balance: Cons: ytd: Revenue (ALL mn) | 557,578.960 Aug 2026 | monthly | Dec 1997 - Aug 2026 |  
| General Govt Balance: Cons: ytd: Revenue: Tax: TC: Value Added Tax (ALL mn) | 165,382.210 Aug 2026 | monthly | Jan 2002 - Aug 2026 |
</excerpt>
### Rank 2 of 44 — 0.40
<excerpt title="Albania GDP 2022 — $19.0B, Rank #123 (Excel & CSV)">
Country Profile · GDP · 2022
Albania's GDP is **$19.0B** in 2022 — ranked **#123** in the world, accounting for **0.02%** of global GDP.
$19.0B
GDP (2022)
$7,757
GDP per capita
0.02%
of world GDP

## ↓ Download this data
Albania GDP history (2015–2024), per capita, growth and world share. Excel and CSV.

## Key figures
| Indicator | Value | Year |  
| --- | --- | --- |  
| GDP (current US$) | $19.0B | 2022 |  
| GDP per capita | $7,757 | 2022 |  
| GDP growth | +4.8% | 2022 |  
| Population | 2.5M | 2022 |  
| World GDP rank | #123 | 2022 |  
| Share of world GDP | 0.02% | 2022 |

## GDP history
Year-by-year GDP data for Albania.
| Year | GDP | Per capita | Growth | Rank | % World |  
| --- | --- | --- | --- | --- | --- |  
| 2025 | $30.5B | $12,998 | +3.8% | #112 | 0.03% |  
| 2024 | $27.0B | $11,378 | +4.0% | #112 | 0.02% |  
| 2023 | $23.5B | $9,731 | +4.0% | #116 | 0.02% |  
| 2022 | $19.0B | $7,757 | +4.8% | #123 | 0.02% |  
| 2021 | $18.0B | $7,242 | +9.0% | #123 | 0.02% |  
| 2020 | $15.2B | $6,028 | -3.3% | #124 | 0.02% |  
| 2019 | $15.6B | $6,069 | +2.1% | #126 | 0.02% |  
| 2018 | $15.4B | $5,898 | +3.7% | #128 | 0.02% |  
| 2017 | $13.3B | $5,006 | +3.3% | #132 | 0.02% |  
| 2016 | $12.0B | $4,458 | +3.9% | #132 | 0.02% |  
| 2015 | $11.5B | $4,200 | +2.2% | #137 | 0.02% |

## FAQ
What is the GDP of Albania?  
Albania's GDP is $19.0B in 2022, ranking #123.
What is Albania's GDP per capita?  
GDP per capita is $7,757.
What share of world GDP is Albania?  
Albania accounts for 0.02% of world GDP in 2022.
**About.** Figures from the World Bank's World Development Indicators. Full historical series (2015–2024) available in the download above.
</excerpt>
### Rank 3 of 44 — 0.40
<excerpt title="Gross domestic product (GDP), 2022 - Our World in Data">
# Gross domestic product (GDP)2022
## Select countries and regions
*    - [x]  Estonia   $40B   
*    - [x]  Armenia   $39.7B   
*    - [x]  Botswana   $39.3B   
*    - [x]  Madagascar   $38.6B   
*    - [x]  Trinidad and Tobago   $37.5B   
*    - [x]  Burkina Faso   $37.3B   
*    - [x]  Albania   $36.2B   
*    - [x]  Luxembourg   $36.1B   
*    - [x]  Gabon   $36B   
*    - [x]  Cyprus   $34.3B   
*    - [x]  Benin   $33.3B   
*    - [x]  Nicaragua   $32.8B   
*    - [x]  Kyrgyzstan   $31.7B   
*    - [x]  Mozambique   $31.4B   
*    - [x]  Mali   $30.6B   
*    - [x]  North Macedonia   $28.8B   
*    - [x]  Rwanda   $28.5B   
*    - [x]  Mauritius   $27B   
*    - [x]  Malawi   $26.5B   
*    - [x]  Zimbabwe   $25.9B   
*    - [x]  Niger   $24.8B   
*    - [x]  Chad   $24.1B   
*    - [x]  Palestine   $24.1B   
*    - [x]  Moldova   $23.8B   
*    - [x]  Congo   $23.7B   
*    - [x]  Guinea   $23.7B   
*    - [x]  Namibia   $21.9B   
*    - [x]  Equatorial Guinea   $20.2B   
*    - [x]  Jamaica   $20B   
*    - [x]  Malta   $18.3B
</excerpt>
### Rank 4 of 44 — 0.30
<excerpt title="Albania GDP per capita in current US$ 1988 - 2022 | WITS Data">
# Albania GDP per capita
, in current US$
1988-2023
Country / Region
Albania
Year / Range
1988-2023
Indicator
GDP per capita (current US$)
Please note the exports, imports and tariff data are based on reported data and not gap filled. Please check the Data Availabilityfor coverage.

# Albania GDP per capita
#### Chart View
*   [](javascript:void(0))

    *   PNG

    *   JPEG

*   [](javascript:void(0))  
*   [](javascript:void(0))_Copy and paste the following code to your website:_
line
[More Countries](javascript:void)
Country
Albania

# Albania GDP per capita
#### Table View
*   [](javascript:void(0))

    *   Excel

*   [](javascript:void(0))

    *   Print All  
    *   Print Selected  
    *   [Print](javascript:void(0))

*   [](javascript:void(0))- [x] Include Metadata.
* * *
- [x] Show top records.
* * *
_Copy and paste the following code to your website:_
By Country and Region
Loading...
Country Name
1988
1989
1990
1991
1992
1993
1994
Albania
652.77
698.00
617.23
336.59
200.85
367.28
586.42
*   About  
*   .  
*   Contact  
*   .  
*   Usage Conditions  
*   .  
*   Legal  
*   .  
*   Data Providers  
*   .  
*   Page refreshed : Nov-18-2026 20:58 ET
Partners*   ITC
*   .  
*   UNCTAD  
*   .  
*   UNSTATS  
*   .  
*   World Trade Organization  
*   .  
*   World Bank

# WITS - Country Selection
×
</excerpt>
### Rank 5 of 44 — 0.28
<excerpt title="Albania GDP per capita in current US$ 1988 - 2022 | WITS Data">
# Albania GDP per capita in current US$ 1988 - 2022 | WITS Data
WITS
*   [En](javascript:void(0))  
*   Es
Toggle navigation Toggle navigation

# Albania GDP per capita in current US$ 1988 - 2022 | WITS Data
*   [English](javascript:void(0))  
*   Español  
*   |  
*   [Login](javascript:void(0))  
*   Register

*   [](javascript:void(0); "Facebook")  
*   [](javascript:void(0); "Twitter")  
*   [](javascript:void(0); "Linkedin")  
*   [](javascript:void(0); "Google Plus")  
*   [](javascript:void(0); "Reddit")  
*   [](javascript:void(0); "StumbleUpon")  
*   [](javascript:void(0); "Delicious")  
*   [](javascript:void(0); "Email")

*   Trade Stats  
    *   By Country  
    *   By Indicator  
    *   By Product (HS 6-digit)  
    *   Visualization  
    *   Data Download  
    *   Metadata  
    *   Data Availability  
    *   Help

*   Tariffs  
    *   GPTAD  
    *   UNCTAD TRAINS

*   Non-Tariff Measures  
    *   Summary  
    *   By Country  
    *   Visualization  
    *   Data Download  
    *   Metadata  
    *   Data Availability  
    *   About NTM

*   GVC  
    *   About GVC  
    *   Visualization  
    *   GVC Indicator Metadata  
    *   GVC Data Download

*   API  
    *   API overview  
    *   API documentation

*   Analytical database  
*   Tools  
    *   Compare Countries  
    *   Simulation Tool  
    *   TRIST

*   Bulk Download

*   Home  
*   About WITS  
*   Reference  
    *   Methodology  
    *   Glossary  
    *   Reference Data  
    *   Concordances  
    *   Links

*   Training  
    *   Training overview  
    *   Video Tutorials  
    *   eLearning

*   Support Links  
    *   Did you know  
    *   FAQ  
    *   WITS manual  
    *   Help  
    *   eLearning  
    *   Wits AI

*   At a Glance  
*   Summary  
*   Partner  
*   Product Group  
*   [Country](javascript:void)
Go To

# Albania GDP per capita in current US$ 1988 - 2022 | WITS Data
*   Exports  
*   Imports  
*   Trade % of GDP MRV  
*   Trade  
*   Trade Indicators  
*   Tariff  
*   Developement Indicators  
*   Top Exports  
*   Top Imports  
*   Products
Share
*   Facebook  
*   [Twitter](javascript:void(0); "Twitter")  
*   Linkedin  
*   Google Plus  
*   Reddit  
*   Stumble Upon  
*   Delicious  
*   Email  
*   whatsapp
Custom Query Help
Loading...

# Albania GDP per capita
, in current US$
1988-2023
Country / Region
Albania
Year / Range
1988-2023
Indicator
GDP per capita (current US$)
Please note the exports, imports and tariff data are based on reported data and not gap filled. Please check the Data Availabilityfor coverage.
</excerpt>

## Search 10 — query: ""Albania,ALB,2022" "GDP per capita" "Our World in Data""
### Rank 1 of 1056 — 0.58 (passed on)
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
### Rank 2 of 1056 — 0.39
<excerpt title="https://ourworldindata.org/grapher/gdp-per-capita-...">
CSV columns (first row): Entity,Code,Year,GDP per capita,GDP per capita (Annotations)
```
Albania,ALB,1998,3873.373,
```
```
Albania,ALB,1999,4432.0425,
```
```
Albania,ALB,2000,4808.4795,
```
```
Albania,ALB,2001,5285.809,
```
```
Albania,ALB,2002,5608.9624,
```
```
Albania,ALB,2003,6004.645,
```
```
Albania,ALB,2004,6419.8706,
```
```
Albania,ALB,2005,6858.4673,
```
```
Albania,ALB,2006,7347.33,
```
```
Albania,ALB,2007,7866.1577,
```
```
Albania,ALB,2008,8522.13,
```
```
Albania,ALB,2009,8859.472,
```
```
Albania,ALB,2010,9222.973,
```
```
Albania,ALB,2011,9484,
```
```
Albania,ALB,2012,9634.334,
```
```
Albania,ALB,2013,9748.728,
```
```
Albania,ALB,2014,9942.276,
```
```
Albania,ALB,2015,10192.529,
```
</excerpt>
### Rank 3 of 1056 — 0.30
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
### Rank 4 of 1056 — 0.28
<excerpt title="https://ourworldindata.org/grapher/gdp-per-capita-...">
CSV columns (first row): Entity,Code,Year,GDP per capita,GDP per capita (Annotations)
```
Algeria,DZA,2004,9182.294,
```
```
Algeria,DZA,2005,9969.623,
```
```
Algeria,DZA,2006,10385.779,
```
```
Algeria,DZA,2007,10974.742,
```
```
Algeria,DZA,2008,11475.002,
```
```
Algeria,DZA,2009,11907.021,
```
```
Algeria,DZA,2010,12587.744,
```
```
Algeria,DZA,2011,13204,
```
```
Algeria,DZA,2012,13392.944,
```
```
Algeria,DZA,2013,13508.265,
```
```
Algeria,DZA,2014,13760.384,
```
```
Algeria,DZA,2015,14007.894,
```
```
Algeria,DZA,2016,14198.272,
```
```
Algeria,DZA,2017,14149.915,
```
```
Algeria,DZA,2018,14083.772,
```
```
Algeria,DZA,2019,14000.279,
```
```
Algeria,DZA,2020,13086.293,
```
```
Algeria,DZA,2021,13337.262,
```
```
Algeria,DZA,2022,13506.444,
```
</excerpt>
### Rank 5 of 1056 — 0.25
<excerpt title="https://ourworldindata.org/grapher/gdp-per-capita-...">
CSV columns (first row): Entity,Code,Year,GDP per capita,GDP per capita (Annotations)
```
Algeria,DZA,1984,5361,
```
```
Algeria,DZA,1985,5469,
```
```
Algeria,DZA,1986,5262,
```
```
Algeria,DZA,1987,5088,
```
```
Algeria,DZA,1988,4850,
```
```
Algeria,DZA,1989,4889,
```
```
Algeria,DZA,1990,4697,
```
```
Algeria,DZA,1991,4708.232,
```
```
Algeria,DZA,1992,4850.223,
```
```
Algeria,DZA,1993,4816.924,
```
```
Algeria,DZA,1994,4856.9854,
```
```
Algeria,DZA,1995,5142.384,
```
```
Algeria,DZA,1996,5451.6343,
```
```
Algeria,DZA,1997,5638.48,
```
```
Algeria,DZA,1998,6069.7773,
```
```
Algeria,DZA,1999,6421.5083,
```
```
Algeria,DZA,2000,6834.5537,
```
```
Algeria,DZA,2001,7218.2456,
```
```
Algeria,DZA,2002,7814.8384,
```
```
Algeria,DZA,2003,8590.178,
```
</excerpt>

# Example 3
## Question
out of the artists who participated in the 2023 The Art of Texas State Parks traveling art exhibit, which ones were from austin texas?

## Expected answer
Fidencio Duran, Malou Flato, Gordon Fowler, Terri Wells

## Grade 1.00

## Search 1 — query: "2023 The Art of Texas State Parks traveling art exhibit artists list"
### Rank 1 of 45 — 0.97 (passed on)
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
### Rank 2 of 45 — 0.97
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
### Rank 3 of 45 — 0.97
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
### Rank 4 of 45 — 0.96
<excerpt title="Traveling Art Exhibit Honoring 100 Years of Texas State Parks Moves ...">
## Oct. 26, 2023
### Media Contact: [TPWD News](mailto:news@tpwd.texas.gov "TPWD News"),Business Hours, 512-389-8030
News ImageShare on FacebookShare Release URL
_**Art of Texas State Parks at Panhandle-Plains Historical Museum Oct. 27– Feb. 18, 2024**_
**Note: This item is more than three years old.** Please take the publication date into consideration for any date references.
AUSTIN— In honor of the Centennial Celebration of Texas State Parks, the Panhandle-Plains Historical Museum in Canyon will display a new traveling art exhibit Oct. 27– Feb. 18, 2024.
_The Art of Texas State Parks_ is a visual arts survey of state parks featuring more than 30 parks by some of Texas’ finest artists. Along with the traveling exhibit, the project also includes a commemorative book published by Texas A&M Press. Proceeds from book sales and the sale of the artwork through Foltz Fine Art in Houston will be donated to Texas Parks and Wildlife Foundation to benefit Texas State Parks.
The project was several years in the making. In anticipation of the 2023 Centennial Celebration of Texas State Parks, Texas Parks and Wildlife Foundation partnered with Texas Parks and Wildlife Department (TPWD), the Meadows Center for Water and the Environment at Texas State University, and the Bullock Texas State History Museum to present _The Art of Texas State Parks_. Thirty notable Texas artists were commissioned to create works celebrating parks across Texas. Additional support for the project is provided by H-E-B, presenting sponsor for the Texas State Parks Centennial Celebration.
“We have been thrilled at the response to this year-long Centennial celebration of our parks, and hope that in displaying these extraordinary pieces, visitors will be inspired to get out, and enjoy and explore the stunning natural landscapes we’re fortunate to have right in our backyards,” said Texas Parks and Wildlife Department (TPWD) Executive Director David Yoskowitz, Ph.D. “We are grateful for the collaboration that is bringing _The Art of Texas State Parks_ to museums across Texas, spreading the message about these natural treasures that belong to us all.”

## Oct. 26, 2023
### Media Contact: [TPWD News](mailto:news@tpwd.texas.gov "TPWD News"),Business Hours, 512-389-8030
_The Art of Texas State Parks_ is intended to increase public awareness of Texas parklands and heighten their popular appeal through the elegant and inspired works of Texas’ best contemporary painters. While the national park system has benefitted from their chroniclers in art, no such artistic record has yet been undertaken for state parks. The Centennial Celebration of Texas State Parks offers the perfect occasion to create a lasting visual record of Texas State Parks in art and, at the same time, memorialize the past and ongoing development of the distinctive collection of Lone Star parks and natural areas.
Participating artists include:**Randy Bacon** (Abilene); **Mary Baxter** (Marfa); **David Caton** (Utopia); **Charles Criner** (Houston); **Margie Crisp** (Elgin); **Ric Dentinger** (San Antonio/Santa Fe NM); **Fidencio Duran** (Austin); **Janet Eager Krueger** (Encinal); **Joel Edwards** (Waco); **Malou Flato** (Austin); **Gordon Fowler** (Austin); **Pat Gabriel** (Fort Worth); **David****Griffin** (Lubbock/ Dallas); **Brian Grimm** (Fredericksburg); **Clemente Guzman** (San Antonio); **Karl E. Hall** (Houston); **John Austin Hanna** (Fredericksburg); **Billy Hassell** (Fort Worth); **Hailey Herrera** (Bryan); **Lee Jamison** (Huntsville); **Denise Mahlke** (Whitehouse); **Jim Malone** (Fort Worth); **Talmage Minter** (Waco); **William Montgomery** (Elgin); **Kermit Oliver** (Waco); **Noe Perez** (Corpus Christi); **Jeri Salter** (Hutto); **Jim****Stoker** (San Antonio); **Bob Stuth-Wade** (Dublin); and **Terri Wells** (Austin).
</excerpt>
### Rank 5 of 45 — 0.80
<excerpt title="The Art of Texas State Parks">
In 2023, the Texas Parks and Wildlife Department marks the 100th anniversary of the state park system. From its inception in 1923, the Texas park system has grown to 95 sites, covering more than 627,000 acres and comprising 74 state parks, 13 historic sites, and 8 natural areas. This vast collection of natural lands and public places now accommodates almost 9 million visitors each year.
_The Art of Texas State Parks_ celebrates this rich tradition, offering an engaging visual arts survey of Texas state parks as seen through the eyes of leading artists from across the state. Editors Andrew Sansom and Linda J. Reaves have collected original works from thirty of the state’s most influential artists. These stunning visual works are accompanied by a thoughtful essay by William E. Reaves on the time-honored legacy of landscape painting in Texas and by Sansom’s reflections on the vital place of landscape art in Texas conservation. Rounding out the collection, assistant state park director Kevin Good offers an informative profile of Texas state parks, and the work concludes with profiles of the artists whose pieces appear in this special centennial collection.
The centennial of the state parks system offers the perfect occasion to create a lasting visual record of Texas parks in art while memorializing the past and ongoing development of the distinctive collection of Lone Star parks and natural areas. _The Art of Texas State Parks_ offers readers increased awareness of Texas parklands and heightens their popular appeal through the elegant and inspired works of some of Texas’ finest contemporary artists.
Includes the work of these artists:

Randy Bacon, Abilene Mary Baxter, Marfa David Caton, Utopia Charles Criner, Houston Margie Crisp, Elgin Ric Dentinger, San Antonio Fidencio Duran, Austin Janet Eager Krueger, Encinal Joel R. Edwards, Waco Malou Flato, Austin Gordon Fowler, Austin Pat Gabriel, Fort Worth David R. Griffin, Dallas Brian Grimm, Fredericksburg Clemente F. Guzman III, San Antonio Karl E. Hall, Houston John Austin Hanna, Fredericksburg Billy Hassell, Fort Worth Hailey E. Herrera, Bryan Lee Jamison, Huntsville Denise LaRue Mahlke, Whitehouse Talmage Minter, Waco William B. Montgomery, Elgin Kermit Oliver, Waco Noe Perez, Corpus Christi Jeri Salter, Hutto Jim Stoker, San Antonio Bob Stuth-Wade, Dublin Terri M. Wells, Austin
_All author proceeds from the sale of this book will benefit the Texas Parks and Wildlife Foundation._
</excerpt>

# Example 4
## Question
I’m looking for good universities. From the Guardian University Guide 2022, which of the top 50 universities have an overall course satisfaction score of 80 or higher, a continuation score of 95 or higher, and a student-to-staff ratio of 15 or less?

## Expected answer
St Andrews, London School of Economics, Durham, Warwick, Imperial College, Loughborough, Lancaster, Southampton, York, Sheffield, Liverpool, Keele

## Grade 0.25

## Search 1 — query: "Guardian University Guide 2022 overall course satisfaction score 80 continuation score 95 student to staff ratio 15"
### Rank 1 of 131 — 0.70 (passed on)
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
### Rank 2 of 131 — 0.68
<excerpt title="The Guardian University Guide 2025 – the rankings">
Value added score/10 This score compares students’ degree results with their entry qualifications, to show how effectively they are taught. It is given as a rating out of 10 6.8
Career after 15 months Percentage of graduates who find graduate-level jobs, or are in further study at professional or HE level, within 15 months of graduation 93
Contin-uation Percentage of first-year students continuing to second year 96.6  
5 5 Imperial College 82.6 85.5 64.4 11.9 8.6 204 6.6 96 95.6  
Satisfied with teaching The rating for the quality of teaching on the course, given by final-year students in the NSS 85.5
Satisfied with feedback The rating for the quality of feedback and assessment, given by final-year students in the NSS 64.4
Student to staff ratio Number of students per member of teaching staff 11.9
Spend per student/10 Money spent on each student, excluding academic staff costs, given as a rating out of 10 8.6
Average entry tariff Typical Ucas scores of young entrants (under 21) to the department 204
Value added score/10 This score compares students’ degree results with their entry qualifications, to show how effectively they are taught. It is given as a rating out of 10 6.6
Career after 15 months Percentage of graduates who find graduate-level jobs, or are in further study at professional or HE level, within 15 months of graduation 96
Contin-uation Percentage of first-year students continuing to second year 95.6  
6 7 Durham 80.8 87.9 74.2 13.5 6.2 185 6.2 91 97.5  
Satisfied with teaching The rating for the quality of teaching on the course, given by final-year students in the NSS 87.9
Satisfied with feedback The rating for the quality of feedback and assessment, given by final-year students in the NSS 74.2
Student to staff ratio Number of students per member of teaching staff 13.5
</excerpt>
### Rank 3 of 131 — 0.63
<excerpt title="The Guardian University Guide 2025 – the rankings">
Spend per student/10 Money spent on each student, excluding academic staff costs, given as a rating out of 10 7.4
Average entry tariff Typical Ucas scores of young entrants (under 21) to the department 127
Value added score/10 This score compares students’ degree results with their entry qualifications, to show how effectively they are taught. It is given as a rating out of 10 6.7
Career after 15 months Percentage of graduates who find graduate-level jobs, or are in further study at professional or HE level, within 15 months of graduation 72
Contin-uation Percentage of first-year students continuing to second year 85.2  
34 48 Leicester 61.5 83 76 14.4 5.4 131 5.8 84 95.1  
Satisfied with teaching The rating for the quality of teaching on the course, given by final-year students in the NSS 83
Satisfied with feedback The rating for the quality of feedback and assessment, given by final-year students in the NSS 76
Student to staff ratio Number of students per member of teaching staff 14.4
Spend per student/10 Money spent on each student, excluding academic staff costs, given as a rating out of 10 5.4
Average entry tariff Typical Ucas scores of young entrants (under 21) to the department 131
Value added score/10 This score compares students’ degree results with their entry qualifications, to show how effectively they are taught. It is given as a rating out of 10 5.8
Career after 15 months Percentage of graduates who find graduate-level jobs, or are in further study at professional or HE level, within 15 months of graduation 84
Contin-uation Percentage of first-year students continuing to second year 95.1  
35 44 Reading 61.4 85.2 78.8 15.8 5.4 130 5.7 84 94.6  
Satisfied with teaching The rating for the quality of teaching on the course, given by final-year students in the NSS 85.2

Satisfied with feedback The rating for the quality of feedback and assessment, given by final-year students in the NSS 78.8
Student to staff ratio Number of students per member of teaching staff 15.8
Spend per student/10 Money spent on each student, excluding academic staff costs, given as a rating out of 10 5.4
Average entry tariff Typical Ucas scores of young entrants (under 21) to the department 130
Value added score/10 This score compares students’ degree results with their entry qualifications, to show how effectively they are taught. It is given as a rating out of 10 5.7
Career after 15 months Percentage of graduates who find graduate-level jobs, or are in further study at professional or HE level, within 15 months of graduation 84
Contin-uation Percentage of first-year students continuing to second year 94.6  
36 37 Birmingham 61.2 83.9 70.7 14.6 5.8 157 4.7 88 96  
Satisfied with teaching The rating for the quality of teaching on the course, given by final-year students in the NSS 83.9
Satisfied with feedback The rating for the quality of feedback and assessment, given by final-year students in the NSS 70.7
Student to staff ratio Number of students per member of teaching staff 14.6
Spend per student/10 Money spent on each student, excluding academic staff costs, given as a rating out of 10 5.8
Average entry tariff Typical Ucas scores of young entrants (under 21) to the department 157
Value added score/10 This score compares students’ degree results with their entry qualifications, to show how effectively they are taught. It is given as a rating out of 10 4.7
Career after 15 months Percentage of graduates who find graduate-level jobs, or are in further study at professional or HE level, within 15 months of graduation 88
</excerpt>
### Rank 4 of 131 — 0.63
<excerpt title="The Guardian University Guide 2025 – the rankings">
Satisfied with feedback The rating for the quality of feedback and assessment, given by final-year students in the NSS 78.8
Student to staff ratio Number of students per member of teaching staff 15.8
Spend per student/10 Money spent on each student, excluding academic staff costs, given as a rating out of 10 5.4
Average entry tariff Typical Ucas scores of young entrants (under 21) to the department 130
Value added score/10 This score compares students’ degree results with their entry qualifications, to show how effectively they are taught. It is given as a rating out of 10 5.7
Career after 15 months Percentage of graduates who find graduate-level jobs, or are in further study at professional or HE level, within 15 months of graduation 84
Contin-uation Percentage of first-year students continuing to second year 94.6  
36 37 Birmingham 61.2 83.9 70.7 14.6 5.8 157 4.7 88 96  
Satisfied with teaching The rating for the quality of teaching on the course, given by final-year students in the NSS 83.9
Satisfied with feedback The rating for the quality of feedback and assessment, given by final-year students in the NSS 70.7
Student to staff ratio Number of students per member of teaching staff 14.6
Spend per student/10 Money spent on each student, excluding academic staff costs, given as a rating out of 10 5.8
Average entry tariff Typical Ucas scores of young entrants (under 21) to the department 157
Value added score/10 This score compares students’ degree results with their entry qualifications, to show how effectively they are taught. It is given as a rating out of 10 4.7
Career after 15 months Percentage of graduates who find graduate-level jobs, or are in further study at professional or HE level, within 15 months of graduation 88

Contin-uation Percentage of first-year students continuing to second year 96  
37 27 Leeds 61.1 81.2 67 14.4 7.3 163 5.3 86 96  
Satisfied with teaching The rating for the quality of teaching on the course, given by final-year students in the NSS 81.2
Satisfied with feedback The rating for the quality of feedback and assessment, given by final-year students in the NSS 67
Student to staff ratio Number of students per member of teaching staff 14.4
Spend per student/10 Money spent on each student, excluding academic staff costs, given as a rating out of 10 7.3
Average entry tariff Typical Ucas scores of young entrants (under 21) to the department 163
Value added score/10 This score compares students’ degree results with their entry qualifications, to show how effectively they are taught. It is given as a rating out of 10 5.3
Career after 15 months Percentage of graduates who find graduate-level jobs, or are in further study at professional or HE level, within 15 months of graduation 86
Contin-uation Percentage of first-year students continuing to second year 96  
38 38 Northumbria 60.7 83.4 80.1 15.5 4.8 143 6.6 82 89.2  
Satisfied with teaching The rating for the quality of teaching on the course, given by final-year students in the NSS 83.4
Satisfied with feedback The rating for the quality of feedback and assessment, given by final-year students in the NSS 80.1
Student to staff ratio Number of students per member of teaching staff 15.5
Spend per student/10 Money spent on each student, excluding academic staff costs, given as a rating out of 10 4.8
Average entry tariff Typical Ucas scores of young entrants (under 21) to the department 143
Value added score/10 This score compares students’ degree results with their entry qualifications, to show how effectively they are taught. It is given as a rating out of 10 6.6
</excerpt>
### Rank 5 of 131 — 0.62
<excerpt title="The Guardian University Guide 2025 – the rankings">
Satisfied with feedback The rating for the quality of feedback and assessment, given by final-year students in the NSS 75
Student to staff ratio Number of students per member of teaching staff 18.8
Spend per student/10 Money spent on each student, excluding academic staff costs, given as a rating out of 10 7.2
Average entry tariff Typical Ucas scores of young entrants (under 21) to the department 210
Value added score/10 This score compares students’ degree results with their entry qualifications, to show how effectively they are taught. It is given as a rating out of 10 4.2
Career after 15 months Percentage of graduates who find graduate-level jobs, or are in further study at professional or HE level, within 15 months of graduation 86
Contin-uation Percentage of first-year students continuing to second year 93.6  
18 18 Exeter 66.2 87 72.2 16.3 4.7 163 6.2 86 96.2  
Satisfied with teaching The rating for the quality of teaching on the course, given by final-year students in the NSS 87
Satisfied with feedback The rating for the quality of feedback and assessment, given by final-year students in the NSS 72.2
Student to staff ratio Number of students per member of teaching staff 16.3
Spend per student/10 Money spent on each student, excluding academic staff costs, given as a rating out of 10 4.7
Average entry tariff Typical Ucas scores of young entrants (under 21) to the department 163
Value added score/10 This score compares students’ degree results with their entry qualifications, to show how effectively they are taught. It is given as a rating out of 10 6.2
Career after 15 months Percentage of graduates who find graduate-level jobs, or are in further study at professional or HE level, within 15 months of graduation 86

Contin-uation Percentage of first-year students continuing to second year 96.2  
19 21 Surrey 65.4 87.7 80.5 14.4 5.4 142 4 88 93.7  
Satisfied with teaching The rating for the quality of teaching on the course, given by final-year students in the NSS 87.7
Satisfied with feedback The rating for the quality of feedback and assessment, given by final-year students in the NSS 80.5
Student to staff ratio Number of students per member of teaching staff 14.4
Spend per student/10 Money spent on each student, excluding academic staff costs, given as a rating out of 10 5.4
Average entry tariff Typical Ucas scores of young entrants (under 21) to the department 142
Value added score/10 This score compares students’ degree results with their entry qualifications, to show how effectively they are taught. It is given as a rating out of 10 4
Career after 15 months Percentage of graduates who find graduate-level jobs, or are in further study at professional or HE level, within 15 months of graduation 88
Contin-uation Percentage of first-year students continuing to second year 93.7  
20 21 Sheffield 65.3 86.4 78 14.4 5.7 157 5.2 86 95.7  
Satisfied with teaching The rating for the quality of teaching on the course, given by final-year students in the NSS 86.4
Satisfied with feedback The rating for the quality of feedback and assessment, given by final-year students in the NSS 78
Student to staff ratio Number of students per member of teaching staff 14.4
Spend per student/10 Money spent on each student, excluding academic staff costs, given as a rating out of 10 5.7
Average entry tariff Typical Ucas scores of young entrants (under 21) to the department 157
Value added score/10 This score compares students’ degree results with their entry qualifications, to show how effectively they are taught. It is given as a rating out of 10 5.2
</excerpt>

## Search 2 — query: "Guardian University Guide 2022 league table overall course satisfaction 2022 guardian university guide 2022 table"
### Rank 1 of 143 — 0.71 (passed on)
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
### Rank 2 of 143 — 0.70
<excerpt title="The Guardian University Guide 2022 – the rankings">
Contin-uation 97  
5 4Durham86.5 83.9 84.8 69.5 13.5 6.5 182 6.7 89 97  
Satisfied with course 83.9
Satisfied with teaching 84.8
Satisfied with feedback 69.5
Student to staff ratio 13.5
Spend per student/10 6.5
Average entry tariff 182
Value added score/10 6.7
Career after 15 months 89
Contin-uation 97  
6 8Warwick85.3 84.6 85.1 70.7 12.8 7 170 5.3 88 97  
Satisfied with course 84.6
Satisfied with teaching 85.1
Satisfied with feedback 70.7
Student to staff ratio 12.8
Spend per student/10 7
Average entry tariff 170
Value added score/10 5.3
Career after 15 months 88
Contin-uation 97  
7 9Imperial College84.9 83 85 62.2 11.1 9.2 197 5.1 96 96  
Satisfied with course 83
Satisfied with teaching 85
Satisfied with feedback 62.2
Student to staff ratio 11.1
Spend per student/10 9.2
Average entry tariff 197
Value added score/10 5.1
Career after 15 months 96
Contin-uation 96  
8 6Bath84.7 87.1 86 63.2 15.1 6.1 167 6.4 91 97  
Satisfied with course 87.1
Satisfied with teaching 86
Satisfied with feedback 63.2
Student to staff ratio 15.1
Spend per student/10 6.1
Average entry tariff 167
</excerpt>
### Rank 3 of 143 — 0.65
<excerpt title="The Guardian University Guide 2022 – the rankings">
Contin-uation 91  
38 26Coventry70.2 79.3 83.6 72.3 14.2 6.4 112 6.3 82 90  
Satisfied with course 79.3
Satisfied with teaching 83.6
Satisfied with feedback 72.3
Student to staff ratio 14.2
Spend per student/10 6.4
Average entry tariff 112
Value added score/10 6.3
Career after 15 months 82
Contin-uation 90  
38 37Cardiff70.2 77 80.6 63.5 13.7 6.7 145 4.9 85 95  
Satisfied with course 77
Satisfied with teaching 80.6
Satisfied with feedback 63.5
Student to staff ratio 13.7
Spend per student/10 6.7
Average entry tariff 145
Value added score/10 4.9
Career after 15 months 85
Contin-uation 95  
40 59Liverpool70.0 81.5 83.4 69.6 13.9 7.6 140 5.4 83 96  
Satisfied with course 81.5
Satisfied with teaching 83.4
Satisfied with feedback 69.6
Student to staff ratio 13.9
Spend per student/10 7.6
Average entry tariff 140
Value added score/10 5.4
Career after 15 months 83
Contin-uation 96  
41 27Northumbria69.6 75.4 78.6 70.7 15.5 4 139 6.9 78 91  
Satisfied with course 75.4
Satisfied with teaching 78.6
Satisfied with feedback 70.7
Student to staff ratio 15.5

Spend per student/10 4
Average entry tariff 139
Value added score/10 6.9
Career after 15 months 78
Contin-uation 91  
41 38UEA69.6 80.8 83.3 68.2 13.2 4.2 133 5.8 82 93  
Satisfied with course 80.8
Satisfied with teaching 83.3
Satisfied with feedback 68.2
Student to staff ratio 13.2
Spend per student/10 4.2
Average entry tariff 133
Value added score/10 5.8
Career after 15 months 82
Contin-uation 93  
41 53Plymouth69.6 80.2 83.7 73.3 17.1 5 124 7.9 80 93  
Satisfied with course 80.2
Satisfied with teaching 83.7
Satisfied with feedback 73.3
Student to staff ratio 17.1
Spend per student/10 5
Average entry tariff 124
Value added score/10 7.9
Career after 15 months 80
Contin-uation 93  
44 59Sussex68.9 77.6 80.7 63.6 17.4 6.3 136 4.1 80 96  
Satisfied with course 77.6
Satisfied with teaching 80.7
Satisfied with feedback 63.6
Student to staff ratio 17.4
Spend per student/10 6.3
Average entry tariff 136
Value added score/10 4.1
Career after 15 months 80
</excerpt>
### Rank 4 of 143 — 0.65
<excerpt title="The Guardian University Guide 2022 – the rankings">
Spend per student/10 4
Average entry tariff 139
Value added score/10 6.9
Career after 15 months 78
Contin-uation 91  
41 38UEA69.6 80.8 83.3 68.2 13.2 4.2 133 5.8 82 93  
Satisfied with course 80.8
Satisfied with teaching 83.3
Satisfied with feedback 68.2
Student to staff ratio 13.2
Spend per student/10 4.2
Average entry tariff 133
Value added score/10 5.8
Career after 15 months 82
Contin-uation 93  
41 53Plymouth69.6 80.2 83.7 73.3 17.1 5 124 7.9 80 93  
Satisfied with course 80.2
Satisfied with teaching 83.7
Satisfied with feedback 73.3
Student to staff ratio 17.1
Spend per student/10 5
Average entry tariff 124
Value added score/10 7.9
Career after 15 months 80
Contin-uation 93  
44 59Sussex68.9 77.6 80.7 63.6 17.4 6.3 136 4.1 80 96  
Satisfied with course 77.6
Satisfied with teaching 80.7
Satisfied with feedback 63.6
Student to staff ratio 17.4
Spend per student/10 6.3
Average entry tariff 136
Value added score/10 4.1
Career after 15 months 80

Contin-uation 96  
45 40Kingston68.8 76.9 80.4 72.6 17.6 5.8 116 5.3 75 92  
Satisfied with course 76.9
Satisfied with teaching 80.4
Satisfied with feedback 72.6
Student to staff ratio 17.6
Spend per student/10 5.8
Average entry tariff 116
Value added score/10 5.3
Career after 15 months 75
Contin-uation 92  
46 43Oxford Brookes68.7 77 78.7 65.6 14.2 4.7 114 5.8 81 94  
Satisfied with course 77
Satisfied with teaching 78.7
Satisfied with feedback 65.6
Student to staff ratio 14.2
Spend per student/10 4.7
Average entry tariff 114
Value added score/10 5.8
Career after 15 months 81
Contin-uation 94  
46 50Bolton68.7 80.1 85.1 76.6 14.5 8.4 114 2 69 88  
Satisfied with course 80.1
Satisfied with teaching 85.1
Satisfied with feedback 76.6
Student to staff ratio 14.5
Spend per student/10 8.4
Average entry tariff 114
Value added score/10 2
Career after 15 months 69
Contin-uation 88  
48 35Keele68.5 82.9 83.6 69.8 14.8 4.2 121 4.8 81 95  
Satisfied with course 82.9
Satisfied with teaching 83.6
Satisfied with feedback 69.8
Student to staff ratio 14.8
</excerpt>
### Rank 5 of 143 — 0.64
<excerpt title="The Guardian University Guide 2022 – the rankings">
Average entry tariff 164
Value added score/10 5.7
Career after 15 months 90
Contin-uation 94  
24 24Swansea73.5 86.2 84.4 71.4 14.8 5.7 130 4.7 84 94  
Satisfied with course 86.2
Satisfied with teaching 84.4
Satisfied with feedback 71.4
Student to staff ratio 14.8
Spend per student/10 5.7
Average entry tariff 130
Value added score/10 4.7
Career after 15 months 84
Contin-uation 94  
25 30Aston73.3 79.4 80.8 65.8 15.8 6 126 6 83 96  
Satisfied with course 79.4
Satisfied with teaching 80.8
Satisfied with feedback 65.8
Student to staff ratio 15.8
Spend per student/10 6
Average entry tariff 126
Value added score/10 6
Career after 15 months 83
Contin-uation 96
26 45University of the Arts London73.2 64.5 73.1 73.8 12.8 9.8 140 7 65 91  
Satisfied with course 64.5
Satisfied with teaching 73.1
Satisfied with feedback 73.8
Student to staff ratio 12.8
Spend per student/10 9.8
Average entry tariff 140
Value added score/10 7
Career after 15 months 65
Contin-uation 91  
27 31Sheffield72.8 82.3 84.1 67.9 14 4.9 150 5.5 84 96  
Satisfied with course 82.3
Satisfied with teaching 84.1
</excerpt>

## Search 3 — query: "Guardian University Guide 2022 top 50 table csv"
### Rank 1 of 58 — 0.61 (passed on)
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
### Rank 2 of 58 — 0.58
<excerpt title="The Guardian University Guide 2022 – the rankings">
Contin-uation 97  
5 4Durham86.5 83.9 84.8 69.5 13.5 6.5 182 6.7 89 97  
Satisfied with course 83.9
Satisfied with teaching 84.8
Satisfied with feedback 69.5
Student to staff ratio 13.5
Spend per student/10 6.5
Average entry tariff 182
Value added score/10 6.7
Career after 15 months 89
Contin-uation 97  
6 8Warwick85.3 84.6 85.1 70.7 12.8 7 170 5.3 88 97  
Satisfied with course 84.6
Satisfied with teaching 85.1
Satisfied with feedback 70.7
Student to staff ratio 12.8
Spend per student/10 7
Average entry tariff 170
Value added score/10 5.3
Career after 15 months 88
Contin-uation 97  
7 9Imperial College84.9 83 85 62.2 11.1 9.2 197 5.1 96 96  
Satisfied with course 83
Satisfied with teaching 85
Satisfied with feedback 62.2
Student to staff ratio 11.1
Spend per student/10 9.2
Average entry tariff 197
Value added score/10 5.1
Career after 15 months 96
Contin-uation 96  
8 6Bath84.7 87.1 86 63.2 15.1 6.1 167 6.4 91 97  
Satisfied with course 87.1
Satisfied with teaching 86
Satisfied with feedback 63.2
Student to staff ratio 15.1
Spend per student/10 6.1
Average entry tariff 167
</excerpt>
### Rank 3 of 58 — 0.55
<excerpt title="The Guardian University Guide 2022 – the rankings">
Satisfied with teaching 83
Satisfied with feedback 64.7
Student to staff ratio 13.7
Spend per student/10 6.9
Average entry tariff 159
Value added score/10 6
Career after 15 months 85
Contin-uation 96  
17 23Southampton74.8 82.3 84.2 68.8 13.2 6 151 6.6 84 95  
Satisfied with course 82.3
Satisfied with teaching 84.2
Satisfied with feedback 68.8
Student to staff ratio 13.2
Spend per student/10 6
Average entry tariff 151
Value added score/10 6.6
Career after 15 months 84
Contin-uation 95  
18 16York74.6 81.6 84.6 69.2 13.6 5.1 149 4 84 97  
Satisfied with course 81.6
Satisfied with teaching 84.6
Satisfied with feedback 69.2
Student to staff ratio 13.6
Spend per student/10 5.1
Average entry tariff 149
Value added score/10 4
Career after 15 months 84
Contin-uation 97  
18 15Strathclyde74.6 85.5 86.3 65.4 18.9 6.6 199 5.2 86 93  
Satisfied with course 85.5
Satisfied with teaching 86.3
Satisfied with feedback 65.4
Student to staff ratio 18.9
Spend per student/10 6.6
Average entry tariff 199
Value added score/10 5.2
Career after 15 months 86
</excerpt>
### Rank 4 of 58 — 0.54
<excerpt title="The Guardian University Guide 2022 – the rankings">
Spend per student/10 4
Average entry tariff 139
Value added score/10 6.9
Career after 15 months 78
Contin-uation 91  
41 38UEA69.6 80.8 83.3 68.2 13.2 4.2 133 5.8 82 93  
Satisfied with course 80.8
Satisfied with teaching 83.3
Satisfied with feedback 68.2
Student to staff ratio 13.2
Spend per student/10 4.2
Average entry tariff 133
Value added score/10 5.8
Career after 15 months 82
Contin-uation 93  
41 53Plymouth69.6 80.2 83.7 73.3 17.1 5 124 7.9 80 93  
Satisfied with course 80.2
Satisfied with teaching 83.7
Satisfied with feedback 73.3
Student to staff ratio 17.1
Spend per student/10 5
Average entry tariff 124
Value added score/10 7.9
Career after 15 months 80
Contin-uation 93  
44 59Sussex68.9 77.6 80.7 63.6 17.4 6.3 136 4.1 80 96  
Satisfied with course 77.6
Satisfied with teaching 80.7
Satisfied with feedback 63.6
Student to staff ratio 17.4
Spend per student/10 6.3
Average entry tariff 136
Value added score/10 4.1
Career after 15 months 80

Contin-uation 96  
45 40Kingston68.8 76.9 80.4 72.6 17.6 5.8 116 5.3 75 92  
Satisfied with course 76.9
Satisfied with teaching 80.4
Satisfied with feedback 72.6
Student to staff ratio 17.6
Spend per student/10 5.8
Average entry tariff 116
Value added score/10 5.3
Career after 15 months 75
Contin-uation 92  
46 43Oxford Brookes68.7 77 78.7 65.6 14.2 4.7 114 5.8 81 94  
Satisfied with course 77
Satisfied with teaching 78.7
Satisfied with feedback 65.6
Student to staff ratio 14.2
Spend per student/10 4.7
Average entry tariff 114
Value added score/10 5.8
Career after 15 months 81
Contin-uation 94  
46 50Bolton68.7 80.1 85.1 76.6 14.5 8.4 114 2 69 88  
Satisfied with course 80.1
Satisfied with teaching 85.1
Satisfied with feedback 76.6
Student to staff ratio 14.5
Spend per student/10 8.4
Average entry tariff 114
Value added score/10 2
Career after 15 months 69
Contin-uation 88  
48 35Keele68.5 82.9 83.6 69.8 14.8 4.2 121 4.8 81 95  
Satisfied with course 82.9
Satisfied with teaching 83.6
Satisfied with feedback 69.8
Student to staff ratio 14.8
</excerpt>
### Rank 5 of 58 — 0.51
<excerpt title="The Guardian University Guide 2022 – the rankings">
Contin-uation 91  
38 26Coventry70.2 79.3 83.6 72.3 14.2 6.4 112 6.3 82 90  
Satisfied with course 79.3
Satisfied with teaching 83.6
Satisfied with feedback 72.3
Student to staff ratio 14.2
Spend per student/10 6.4
Average entry tariff 112
Value added score/10 6.3
Career after 15 months 82
Contin-uation 90  
38 37Cardiff70.2 77 80.6 63.5 13.7 6.7 145 4.9 85 95  
Satisfied with course 77
Satisfied with teaching 80.6
Satisfied with feedback 63.5
Student to staff ratio 13.7
Spend per student/10 6.7
Average entry tariff 145
Value added score/10 4.9
Career after 15 months 85
Contin-uation 95  
40 59Liverpool70.0 81.5 83.4 69.6 13.9 7.6 140 5.4 83 96  
Satisfied with course 81.5
Satisfied with teaching 83.4
Satisfied with feedback 69.6
Student to staff ratio 13.9
Spend per student/10 7.6
Average entry tariff 140
Value added score/10 5.4
Career after 15 months 83
Contin-uation 96  
41 27Northumbria69.6 75.4 78.6 70.7 15.5 4 139 6.9 78 91  
Satisfied with course 75.4
Satisfied with teaching 78.6
Satisfied with feedback 70.7
Student to staff ratio 15.5

Spend per student/10 4
Average entry tariff 139
Value added score/10 6.9
Career after 15 months 78
Contin-uation 91  
41 38UEA69.6 80.8 83.3 68.2 13.2 4.2 133 5.8 82 93  
Satisfied with course 80.8
Satisfied with teaching 83.3
Satisfied with feedback 68.2
Student to staff ratio 13.2
Spend per student/10 4.2
Average entry tariff 133
Value added score/10 5.8
Career after 15 months 82
Contin-uation 93  
41 53Plymouth69.6 80.2 83.7 73.3 17.1 5 124 7.9 80 93  
Satisfied with course 80.2
Satisfied with teaching 83.7
Satisfied with feedback 73.3
Student to staff ratio 17.1
Spend per student/10 5
Average entry tariff 124
Value added score/10 7.9
Career after 15 months 80
Contin-uation 93  
44 59Sussex68.9 77.6 80.7 63.6 17.4 6.3 136 4.1 80 96  
Satisfied with course 77.6
Satisfied with teaching 80.7
Satisfied with feedback 63.6
Student to staff ratio 17.4
Spend per student/10 6.3
Average entry tariff 136
Value added score/10 4.1
Career after 15 months 80
</excerpt>

## Search 4 — query: "Guardian University Guide 2022 CSV league table Guardian 2022 data"
### Rank 1 of 24 — 0.37 (passed on)
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
### Rank 2 of 24 — 0.14
<excerpt title="Guardian University Guide 2027: Rankings Explained for ...">
By: **Opeyemi Daniel Abatan**
The Guardian University Guide 2027 was published on 12 September 2026 and ranks 123 UK universities. It is the main UK table that leaves out research altogether and judges universities on teaching, student satisfaction and outcomes.
Guardian 2027 at a glance
Published
12 September 2026
Universities ranked
123
Number 1
University of Oxford
Top in London
LSE, 3rd overall
Best for
Teaching quality, satisfaction and graduate careers
Part of our University Rankings 2027 hub: every major UK league table explained for international students.
01

## Which UK universities are top in the Guardian University Guide 2027?
Oxford stays first, Cambridge rises to 2nd and LSE is 3rd, top in London again. Loughborough climbed to 9th and the University of the Arts London is 10th, the only specialist arts institution in the top 10.
1
Oxford
Satisfied with teaching: 96.3% · Career after 15 months: 89
2
Cambridge
Satisfied with teaching: 94.6% · Career after 15 months: 91
3
London School of Economics
Satisfied with teaching: 91.6% · Career after 15 months: 92
4
St Andrews
Satisfied with teaching: 94.4% · Career after 15 months: 85
5
Imperial College London
Satisfied with teaching: 90.9% · Career after 15 months: 95
6
7
Warwick
Satisfied with teaching: 91.3% · Career after 15 months: 88
8
9
10
University of the Arts London
Satisfied with teaching: 85.4% · Career after 15 months: 70
11
Edinburgh
Satisfied with teaching: 87.5% · Career after 15 months: 85
12
13
UCL
Satisfied with teaching: 87.6% · Career after 15 months: 87
14
Birmingham
Satisfied with teaching: 90.4% · Career after 15 months: 84
15
16
Exeter
Satisfied with teaching: 88% · Career after 15 months: 85
17
Strathclyde
Satisfied with teaching: 89.7% · Career after 15 months: 84
18
19
20
Free 2027 shortlist
Not sure which ranked universities you can get into? We match your grades, budget and intake to universities that will accept you.
Get my free shortlist →
Free, with no agency fees and no obligation.
02

## What does the Guardian table measure?
The Guardian score is built from student satisfaction with teaching and with feedback; the student-staff ratio; spending per student; average entry tariff; value added (how far students progress from their entry grades); continuation; and career after 15 months, the share of graduates in graduate-level work or further study 15 months after finishing.
Because research is not counted, universities that put teaching first can rank far higher here than in QS or THE.
03

## Which Study Now partners climbed the most in 2027?
Several of our partners made large gains compared with the 2026 guide:
20
32
37
51
54
67
67
71
73
73
Talk to a counsellor
Turn the rankings into a shortlist: courses, fees, scholarships and intakes that fit you, for 2027 entry.
Check my eligibility →
Free, with no agency fees and no obligation.
Free download
The 2027 Rankings Shortlist Guide: every major league table, fees and intakes in one PDF.
Get the guide →
05

## Frequently asked questions
### Which university is top of the Guardian University Guide 2027?
The University of Oxford, followed by Cambridge, LSE, St Andrews and Imperial College London.
</excerpt>
### Rank 3 of 24 — 0.12
<excerpt title="Accessing university league table data">
# Accessing university league table data


# Cookies on bath.ac.uk
Cookies are little files that we save on your device to remember your preferences. We use some essential cookies to make this site work. We'd also like to set analytics cookies to understand how you use this site so that we can give you the best experience possible. We use services from Vimeo, YouTube and other third-party services that may also use cookies.
The cookies used on this website are listed in our Privacy and cookie policy(Opens in a new window)
Accept all cookies Reject optional cookies
* * *

# Cookies on bath.ac.uk
## Necessary Cookies
Necessary cookies enable core functionality such as page navigation and access to secure areas and are always turned on. They do not include any personally identifiable data. The website cannot function properly without these cookies, and they can only be disabled by changing your browser preferences.
* * *

# Cookies on bath.ac.uk
## Necessary Cookies
### Performance, analytics and marketing cookies
These cookies help us improve our site and understand how you use it. Some are also used for advertising, remarketing and retargeting, meaning we may share non‑personal data with trusted partners (like Google) to measure campaign performance and show more relevant ads. Accepting these cookies enables consent signals such as ad_storage and ad_personalization.
- [x] Analytics On Off
* * *
Save and close
About this tool(Opens in a new window)
Skip to main content
- [x] Open menu
University of Bath
- [x] Open search
*   Staff  
*   Students  
*   Alumni

*   Courses  
*   Research  
*   Innovation  
*   Sport  
*   Departments  
*   About  
*   Students  
*   Staff  
*   Alumni
- [x] Close search

# Accessing university league table data
## Overview of university league table indicators and how to access data.


# On this page
*   National league tables  
*   International league tables  
*   Peformance and access to data  
*   Enquiries
*   National league tables  
*   International league tables  
*   Peformance and access to data  
*   Enquiries

# National league tables
League table performance is driven by the selection and weighting of a range of indicators.
There are three main national league tables that provide overall and subject rankings:
*   the Complete University Guide

*   the Guardian University Guide

*   The Times and The Sunday Times Good University Guide
Much of the data for national league tables comes from HESA data returns. Typical indicators include:
*   student satisfaction  
*   research quality  
*   entry standards  
*   graduate prospects  
*   good honours or 1st and 2:1 degrees awarded  
*   value added  
*   spend per student  
*   retention and completion rates  
*   student-staff ratio

# International league tables
There are also a number of international league tables such as the Times Higher Education World University Rankings and the QS World University Rankings. International rankings usually include academic reputation and citation indicators.

# Peformance and access to data
Information on our league table performance is available on the rankings and reputation webpage. For further information on league table methodologies and access to data, please contact Graham Brooks [mb2571@bath.ac.uk](mailto:mb2571@bath.ac.uk).

# Enquiries
If you have any questions, please contact us.
* * *

# Graham Brooks
*   [mb2571@bath.ac.uk](mailto:mb2571@bath.ac.uk)  
*   [01225384568](tel:+441225384568)
Contents

# On this page
*   National league tables  
*   International league tables  
*   Peformance and access to data  
*   Enquiries
Showing slide 1 of 11
Showing slide 1 of 11
Find out more about our rankings
University of Bath
© University of Bath 2026
* * *
Go to FacebookGo to BlueSkyGo to InstagramGo to LinkedInGo to SnapChatGo to TikTokGo to WeChatGo to Sina WeiboGo to YouTubeGo to Xiaohongshu
</excerpt>
### Rank 4 of 24 — 0.11
<excerpt title="Methodology behind the Guardian University Guide 2022">
## _What are the metrics?_
**Expenditure per student**In order to approximate the level of resources that a student could expect to have dedicated to their provision, we look at the total expenditure in each subject area and divide it by the volume of students taking the subject. We exclude academic staff costs as the benefits of high staff volumes are already captured by the student-staff ratios but recognise that many costs of delivery are centralised: we add the amount of money each provider has spent per students on academic services such as libraries and computing facilities per student, over the past 2 years.
This metric is expressed as points/10 and contributes 5% to the total score of a department.
**Continuation**Taking a degree-level course is a positive experience for most students but is not suited to everybody and some students struggle and discontinue their studies. Providers can do a lot to support their students – they might promote engagement with studies and with the broader higher education experience - and this measure captures how successful each department is in achieving this. We look at the proportion of students who continue their studies beyond the first year and measure the extent to which this exceeds expectations based on entry qualifications.
To achieve this, we take all first-year students on full-time first-degree courses that are scheduled to take longer than a year to complete and look ahead to 1 December in the following academic year to observe the proportion who are still active in higher education. This proportion is viewed positively, regardless of whether the student has switched course, transferred to a different provider, or been required to repeat their first year – only those who become inactive in the UK’s HE system are counted negatively.
To take the effect of entry qualifications into account we create an index score for each student who has a positive outcome, using their expectation of continuation up to a maximum of 97%. To calculate the score there must have been 35 entrants in the most recent cohort and 65 across the last 2 or 3 years.
This index score, aggregated across the last 2 or 3 years, contributes 15% to the total score of non-medical departments. However, it is the percentage score – also averaged over 2 or 3 years – that is displayed.

## _What are the metrics?_
**Student satisfaction**The National Student Survey asks final year students for the extent to which they agree with 27 positive statements about their academic experience of the course and support that they received. Responses are on a 5-point Likert scale (1. definitely disagree to 5. definitely agree) and we take the responses from full-time first-degree students registered at the provider course to produce two statistics: a satisfaction rate and an average response. The satisfaction rate looks across the questions concerned and reports the proportion of responses that were ‘definitely agree’ or ‘mostly agree’ while the average response gives the average Likert score between 1 and 5 that was observed in the responses to those questions.
To assess the **teaching quality** that a student can expect to experience we took responses from the 2020 and 2021 NSS surveys and aggregated them for the following questions:
*   Staff are good at explaining things

*   Staff have made the subject interesting

*   The course is intellectually stimulating

*   My course has challenged me to achieve my best work
The overall satisfaction rate for each provider is displayed, and the average response is used with a 8% weighting.
To assess the likelihood that a student will be satisfied with **assessment** procedures and the **feedback** they receive we took responses from the 2020 and 2021 NSS surveys and aggregated them for the following questions:
*   The criteria used in marking have been clear in advance

*   Marking and assessment has been fair

*   Feedback on my work has been timely

*   I have received helpful comments on my work
The overall satisfaction rate for each provider is displayed, and the average response is used with a 8% weighting.
To assess the **overall satisfaction**of students with their courses we aggregated responses from the 2020 and 2021 NSS surveys for the question “overall, I am satisfied with the quality of the course”.
The overall satisfaction rate for each provider is displayed, and the average response is used with a 4% weighting.
Data was released at the CAH (common aggregation hierarchy) levels of aggregation and we used details of how these map to HECOS (Higher Education classification of subjects) to weight and aggregate results for each of our 54 subjects, prioritising results from the most granular level.
</excerpt>
### Rank 5 of 24 — 0.11
<excerpt title="Methodology behind the Guardian University Guide 2022">
## _What are the metrics?_
**Student satisfaction**The National Student Survey asks final year students for the extent to which they agree with 27 positive statements about their academic experience of the course and support that they received. Responses are on a 5-point Likert scale (1. definitely disagree to 5. definitely agree) and we take the responses from full-time first-degree students registered at the provider course to produce two statistics: a satisfaction rate and an average response. The satisfaction rate looks across the questions concerned and reports the proportion of responses that were ‘definitely agree’ or ‘mostly agree’ while the average response gives the average Likert score between 1 and 5 that was observed in the responses to those questions.
To assess the **teaching quality** that a student can expect to experience we took responses from the 2020 and 2021 NSS surveys and aggregated them for the following questions:
*   Staff are good at explaining things

*   Staff have made the subject interesting

*   The course is intellectually stimulating

*   My course has challenged me to achieve my best work
The overall satisfaction rate for each provider is displayed, and the average response is used with a 8% weighting.
To assess the likelihood that a student will be satisfied with **assessment** procedures and the **feedback** they receive we took responses from the 2020 and 2021 NSS surveys and aggregated them for the following questions:
*   The criteria used in marking have been clear in advance

*   Marking and assessment has been fair

*   Feedback on my work has been timely

*   I have received helpful comments on my work
The overall satisfaction rate for each provider is displayed, and the average response is used with a 8% weighting.
To assess the **overall satisfaction**of students with their courses we aggregated responses from the 2020 and 2021 NSS surveys for the question “overall, I am satisfied with the quality of the course”.
The overall satisfaction rate for each provider is displayed, and the average response is used with a 4% weighting.
Data was released at the CAH (common aggregation hierarchy) levels of aggregation and we used details of how these map to HECOS (Higher Education classification of subjects) to weight and aggregate results for each of our 54 subjects, prioritising results from the most granular level.

## _What are the metrics?_
**Value Added**In order to assess the extent to which each department will support its students towards achieving good grades, we use value added scores to track students from enrolment to graduation. A student’s chances of getting a good classification of degree (a 1st or a 2:1) are already affected by the qualifications that they start with so our scores take this into account and report the extent to which a student exceeded expectations.
Each full-time student is given a probability of achieving a 1st or 2:1, based on the qualifications that they enter with or, if they have vague entry qualifications, the total percentage of good degrees expected for the student in their department. If they manage to earn a good degree, then they score points that reflect how difficult it was to do so (in fact, they score the reciprocal of the probability of getting a 1st or 2:1). Otherwise they score zero. Students taking integrated masters are always regarded as having a positive outcome.
At least 30 students must be in a subject for a meaningful value added score to be calculated using the most recent year of data alone. If there are more than 15 students in the most recent year and the total number across two years reaches 30, then a two-year average is calculated.
This metric is expressed as points/10 and contributes 15% to the total score of a department.
**Career prospects**Using results from the Graduate Outcomes survey for the graduating cohort of 2017/18, we seek to assess the extent to which students have taken a positive first step in the 15 months after graduation, in the hope that similar patterns will repeat for future cohorts. We value students that enter graduate level occupations (approximated by SOC groups 1-3: professional, managerial & technical occupations) and students that go on to further study at a professional or HE level and treat these students as positive.
</excerpt>

## Search 5 — query: "Guardian 2022 university guide CSV "overall score" "satisfaction" "guardian" 2022"
(no page could be scored)

## Search 6 — query: "Guardian 2022 university guide CSV institution Guardian 2022 institutional.csv"
### Rank 1 of 182 — 0.30 (passed on)
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
### Rank 2 of 182 — 0.17
<excerpt title="Colleges">
inst_name
string
Institution (entity) name  
Special values  
-1—Missing/not reported  
-2—Not applicable  
-3—Suppressed data
inst_alias
string
Institution name alias  
Special values  
-1—Missing/not reported  
-2—Not applicable  
-3—Suppressed data
address
string
Street address or post office box  
Special values  
-1—Missing/not reported  
-2—Not applicable  
-3—Suppressed data
state_abbr
string
State abbreviation  
Special values  
-1—Missing/not reported  
-2—Not applicable  
-3—Suppressed data
fips  
FILTER  
integer
Federal Information Processing Standards state code  
Special values  
1—Alabama  
2—Alaska  
3—American Samoa  
4—Arizona
+ MORE  
zip
string
Zip code  
Special values  
-1—Missing/not reported  
-2—Not applicable  
-3—Suppressed data
phone_number
string
General information telephone number  
Special values  
-1—Missing/not reported  
-2—Not applicable  
-3—Suppressed data
city
string
City location of institution  
Special values  
-1—Missing/not reported  
-2—Not applicable  
-3—Suppressed data
county_name
string
County name  
Special values  
-1—Missing/not reported  
-2—Not applicable  
-3—Suppressed data
county_fips  
FILTER  
integer
Federal Information Processing Standards county code  
Special values  
-1—Missing/not reported  
-2—Not applicable  
-3—Suppressed data
region  
FILTER  
integer
Bureau of Economic Analysis (BEA) regions  
Special values  
0—US service schools  
1—New England: CT, ME, MA, NH, RI, and VT  
2—Mid East: DE, DC, MD, NJ, NY, and PA  
3—Great Lakes: IL, IN, MI, OH, and WI
+ MORE  
urban_centric_locale  
FILTER  
integer
Degree of urbanization (urban-centric locale)  
Special values  
1—Large city  
2—Midsize city  
3—Urban fringe of large city  
4—Urban fringe of midsize city
+ MORE  
cbsa  
FILTER  
integer
Core-based statistical area  
Special values  
-1—Missing/not reported  
-2—Not applicable  
-3—Suppressed data
</excerpt>
### Rank 3 of 182 — 0.12
<excerpt title="Colleges">
Institution open to the general public  
Special values  
0—No  
1—Yes  
-1—Missing/not reported  
-2—Not applicable
+ MORE  
title_iv_indicator  
FILTER  
integer
OPE Title IV eligibility indicator code  
Special values  
1—Participates in Title IV federal financial aid programs  
2—Branch campus of a main campus that participates in Title IV  
3—Deferment only, limited participation  
4—New participants (became eligible during the winter collection period)
+ MORE  
postsec_public_active  
FILTER  
integer
Postsecondary institution indicator  
Special values  
1—Active postsecondary institution  
2—Not primarily postsecondary or open to public  
3—Not active  
-1—Missing/not reported
+ MORE  
postsec_public_active_title_iv  
FILTER  
integer
Postsecondary and Title IV institution indicator  
Special values  
1—Title IV postsecondary institution  
2—Non-Title IV postsecondary institution  
3—Title IV NOT primarily postsecondary institution  
4—Non-Title IV NOT primarily postsecondary institution
+ MORE  
date_closed
string
Date institution closed  
Special values  
-1—Missing/not reported  
-2—Not applicable  
-3—Suppressed data
newid  
FILTER  
integer
Unit ID for merged schools  
Special values  
-1—Missing/not reported  
-2—Not applicable  
-3—Suppressed data
year_deleted  
FILTER  
integer
Year institution was deleted from Integrated Postsecondary Education Data System  
Special values  
-1—Missing/not reported  
-2—Not applicable  
-3—Suppressed data
inst_control  
FILTER  
integer
Control of institution  
Special values  
1—Public  
2—Private not-for-profit  
3—Private for-profit  
-1—Missing/not reported
+ MORE  
institution_level  
FILTER  
integer
Level of institution  
Special values  
1—Less than two years (below associate's)  
2—At least two but less than four years  
3—Less than four years  
4—Four or more years
+ MORE  
inst_category  
FILTER  
integer
Institutional category  
Special values  
1—Degree-granting, graduate with no undergraduate degrees  
2—Degree-granting, primarily baccalaureate or above  
3—Degree-granting, not primarily baccalaureate or above  
4—Degree-granting, associate's and certificates
+ MORE  
inst_size  
FILTER  
integer
</excerpt>
### Rank 4 of 182 — 0.12
<excerpt title="Colleges">
Institution (entity) name  
Special values  
-1—Missing/not reported  
-2—Not applicable  
-3—Suppressed data
address
string
Street address or post office box  
Special values  
-1—Missing/not reported  
-2—Not applicable  
-3—Suppressed data
state_abbr
string
State abbreviation  
Special values  
-1—Missing/not reported  
-2—Not applicable  
-3—Suppressed data
zip
string
Zip code  
Special values  
-1—Missing/not reported  
-2—Not applicable  
-3—Suppressed data
county_fips  
FILTER  
integer
Federal Information Processing Standards county code  
Special values  
-1—Missing/not reported  
-2—Not applicable  
-3—Suppressed data
county_name
string
County name  
Special values  
-1—Missing/not reported  
-2—Not applicable  
-3—Suppressed data
geo_longitude
float
Geocoded longitude of institution  
Special values  
-1—Missing/not reported  
-2—Not applicable  
-3—Suppressed data
geo_latitude
float
Geocoded latitude of institution  
Special values  
-1—Missing/not reported  
-2—Not applicable  
-3—Suppressed data
geocode_accuracy
integer
Accuracy of geocode match  
Special values  
1—High confidence  
2—Medium confidence  
3—Low confidence  
4—Did not geocode
+ MORE  
geocode_accuracy_detailed
integer
Type of geocode match  
Special values  
1—Point address  
2—Street address  
3—Subaddress  
4—Street intersection
+ MORE  
state_fips_geo  
FILTER  
integer
Federal Information Processing Standards state code  
Special values  
1—Alabama  
2—Alaska  
3—American Samoa  
4—Arizona
+ MORE  
county_fips_geo  
FILTER  
integer
Federal Information Processing Standards county code  
Special values  
-1—Missing/not reported  
-2—Not applicable  
-3—Suppressed data
tract  
FILTER  
integer
Census tract  
Special values  
-1—Missing/not reported  
-2—Not applicable  
-3—Suppressed data
block_group  
FILTER  
integer
Block group number  
Special values  
-1—Missing/not reported  
-2—Not applicable  
-3—Suppressed data
geoid_block  
FILTER  
string
</excerpt>
### Rank 5 of 182 — 0.10
<excerpt title="Methodology behind the Guardian University Guide 2022">
## _What are the metrics?_
**Expenditure per student**In order to approximate the level of resources that a student could expect to have dedicated to their provision, we look at the total expenditure in each subject area and divide it by the volume of students taking the subject. We exclude academic staff costs as the benefits of high staff volumes are already captured by the student-staff ratios but recognise that many costs of delivery are centralised: we add the amount of money each provider has spent per students on academic services such as libraries and computing facilities per student, over the past 2 years.
This metric is expressed as points/10 and contributes 5% to the total score of a department.
**Continuation**Taking a degree-level course is a positive experience for most students but is not suited to everybody and some students struggle and discontinue their studies. Providers can do a lot to support their students – they might promote engagement with studies and with the broader higher education experience - and this measure captures how successful each department is in achieving this. We look at the proportion of students who continue their studies beyond the first year and measure the extent to which this exceeds expectations based on entry qualifications.
To achieve this, we take all first-year students on full-time first-degree courses that are scheduled to take longer than a year to complete and look ahead to 1 December in the following academic year to observe the proportion who are still active in higher education. This proportion is viewed positively, regardless of whether the student has switched course, transferred to a different provider, or been required to repeat their first year – only those who become inactive in the UK’s HE system are counted negatively.
To take the effect of entry qualifications into account we create an index score for each student who has a positive outcome, using their expectation of continuation up to a maximum of 97%. To calculate the score there must have been 35 entrants in the most recent cohort and 65 across the last 2 or 3 years.
This index score, aggregated across the last 2 or 3 years, contributes 15% to the total score of non-medical departments. However, it is the percentage score – also averaged over 2 or 3 years – that is displayed.

## _What are the metrics?_
**Student satisfaction**The National Student Survey asks final year students for the extent to which they agree with 27 positive statements about their academic experience of the course and support that they received. Responses are on a 5-point Likert scale (1. definitely disagree to 5. definitely agree) and we take the responses from full-time first-degree students registered at the provider course to produce two statistics: a satisfaction rate and an average response. The satisfaction rate looks across the questions concerned and reports the proportion of responses that were ‘definitely agree’ or ‘mostly agree’ while the average response gives the average Likert score between 1 and 5 that was observed in the responses to those questions.
To assess the **teaching quality** that a student can expect to experience we took responses from the 2020 and 2021 NSS surveys and aggregated them for the following questions:
*   Staff are good at explaining things

*   Staff have made the subject interesting

*   The course is intellectually stimulating

*   My course has challenged me to achieve my best work
The overall satisfaction rate for each provider is displayed, and the average response is used with a 8% weighting.
To assess the likelihood that a student will be satisfied with **assessment** procedures and the **feedback** they receive we took responses from the 2020 and 2021 NSS surveys and aggregated them for the following questions:
*   The criteria used in marking have been clear in advance

*   Marking and assessment has been fair

*   Feedback on my work has been timely

*   I have received helpful comments on my work
The overall satisfaction rate for each provider is displayed, and the average response is used with a 8% weighting.
To assess the **overall satisfaction**of students with their courses we aggregated responses from the 2020 and 2021 NSS surveys for the question “overall, I am satisfied with the quality of the course”.
The overall satisfaction rate for each provider is displayed, and the average response is used with a 4% weighting.
Data was released at the CAH (common aggregation hierarchy) levels of aggregation and we used details of how these map to HECOS (Higher Education classification of subjects) to weight and aggregate results for each of our 54 subjects, prioritising results from the most granular level.
</excerpt>

## Search 7 — query: "Guardian 2022 institutional.csv "Guardian" "2022""
### Rank 1 of 769 — 0.10 (passed on)
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
### Rank 2 of 769 — 0.07
<excerpt title="ICCS 2022 Technical Report">
## [PDF page 135]
Latvia  93.4  96.7  100  88.6  82.8  85.7
Malta  100  100  100  89.3  89.3  89.3  
Netherlands  57.7  83.2  100  89.5  51.6  74.5
Norway (9)  96.6  96.6  99.3  88.6  84.9  84.9
Poland  91.2  99.4  99.6  91  82.6  90.1  
Romania  82.9  97.5  100  93.5  77.5  91.1
Serbia  88.7  92  98.6  88.1  77  79.9  
Slovak Republic  91.9  96.2  100  93.2  85.6  89.7
Slovenia  90.2  96.6  100  94.9  85.6  91.6
Spain  96.9  98.1  100  90.2  87.4  88.6  
Sweden  94.2  96.8  100  89.8  84.6  86.9
Benchmarking participant
North Rhine-Westphalia  89.5  95.4  99.4  88.2  78.4  83.6  
Schleswig-Holstein  57  73.7  98.8  80  45.1  58.3
</excerpt>
### Rank 3 of 769 — 0.06
<excerpt title="Guardian Pharmacy Services, Inc. (GRDN) institutional holders">
## Coverage & totals by quarter
Reporting institutions
Disclosed shares
Disclosed value
Counts also change with data coverage and reporting entities; they do not measure net buying.Distinct managers with a live stock row in this CUSIP; totals may include overlapping filings and are not a share of the company.

## Explore all 197 reporting institutions.
This page includes 20 of 197 reporting institutions. Log in to look up the full history beyond 3 years, use advanced screening & filtering, download CSV, and get the complete set through the Akkru API.
*   Download CSV  
*   Earlier quarters  
*   Advanced screening & filtering  
*   API & AI access
Already have an account?
＋ New accounts get free API credits to explore data beyond ownership filings.
For AI agents & developers  
The initial HTML of this page carries its exact data as script#research-data (JSON): values, units, scope, preview limits and SEC sources. Read it directly, no script or API key needed; script#research-access says what needs an account. This page lists 20 of 197 reporting institutions; totals use the complete disclosed data.
Without an account: the last 3 years, with the row caps stated on the page. A free account opens all history on file on these pages and the CSV of what a page shows. Rows beyond the caps and bulk retrieval go through the authenticated API / MCP / CLI.
MCP  https://api.akkrudata.ai/mcp
akkru_institutional_holdings  
{"action":"holders","cusip":"40145W101","quarter":"2026Q3","type":"positions","page_size":100}
Connect to MCP with OAuth and follow the returned pagination. Credits and usage limits depend on the account.
MCP endpoint https://api.akkrudata.ai/mcp API / MCP / CLI documentation/documentsllms.txt/llms.txt
Sources, coverage & how to read this data  
Figures are as reported to the SEC and merged with later amendments where Akkru could match them. Preview limits apply to what is listed, not to the totals, which come from the complete reported data. Nothing is zero-filled: a missing quarter or month is shown as missing.
Akkru Data
We use cookies to measure how our advertising performs. Essential cookies are always on; advertising cookies are set only if you accept.We use cookies to measure our ads.
40
</excerpt>
### Rank 4 of 769 — 0.06
<excerpt title="ICCS 2022 Technical Report">
## [PDF page 152]
CI2BPM2  67.2  0.39  0.98  CI3SCM1  78.9  0.42  0.95  CI4ZHC1_R  55.7  0.52  1.00  
CI4OCM1  50.5  0.34  1.04  CI4EAM1  71.3  0.46  0.94  CI4ZHL2_R  34.7  0.31  1.24  
CI4OCM2  59.3  0.39  0.99  CI4INM1  90.5  0.34  0.98  CI4ZHC3  46.5  0.44  0.94  
C I 4NTM1  69.1  0.47  0.91  CI2ASM1  59.1  0.41  0.99  CI4ZHC4  33.7  0.37  0.99  
CI3PLM1  85.8  0.38  0.92  CI2ASM2  75.0  0.45  0.93  C I 4ZHM5  75.2  0.38  0.99  
CI4ECM1  49.0  0.39  1.00  C I 3UHM1  67.5  0.42  0.98  C I 4ZE M1  83.9  0.34  0.99
</excerpt>
### Rank 5 of 769 — 0.05
<excerpt title="ICCS 2022 Technical Report">
## [PDF page 153]
Country  CX2W F O2  CX4FKC1  CX4FWC2  CX2W F O1  CX4NHC2  CX2BIO1  CX4DVC1  CX3CPO1  CX3CPO2  CX4SLC3  CX4SLC4  
Br az i l  66  68  75  61  63  58  63  71  60  79  78  
Bulgaria  74  62  68  71  80  76  69  76  81  85  88  
C h i n es e  Ta i p ei  87  80  85  74  68  74  73  88  90  92  92  
Colom bia  70  73  75  72  75  80  77  70  83  84  89  
Croat ia  83  83  96  92  91  85  93  95  96  95  95  
Cyprus  93  85  77  87  100  80  87  66  66  94  92  
Den m a r k  95  91  96  92  92  95  92  95  95  94  97  
Es t o n i a  84  96  96  91  91  87  91  79  80  90  83
</excerpt>

## Search 8 — query: "Guardian 2022 institutional.csv Guardian website institutional 2022"
### Rank 1 of 209 — 0.29 (passed on)
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
### Rank 2 of 209 — 0.10
<excerpt title="Methodology behind the Guardian University Guide 2022">
## _What are the metrics?_
**Student satisfaction**The National Student Survey asks final year students for the extent to which they agree with 27 positive statements about their academic experience of the course and support that they received. Responses are on a 5-point Likert scale (1. definitely disagree to 5. definitely agree) and we take the responses from full-time first-degree students registered at the provider course to produce two statistics: a satisfaction rate and an average response. The satisfaction rate looks across the questions concerned and reports the proportion of responses that were ‘definitely agree’ or ‘mostly agree’ while the average response gives the average Likert score between 1 and 5 that was observed in the responses to those questions.
To assess the **teaching quality** that a student can expect to experience we took responses from the 2020 and 2021 NSS surveys and aggregated them for the following questions:
*   Staff are good at explaining things

*   Staff have made the subject interesting

*   The course is intellectually stimulating

*   My course has challenged me to achieve my best work
The overall satisfaction rate for each provider is displayed, and the average response is used with a 8% weighting.
To assess the likelihood that a student will be satisfied with **assessment** procedures and the **feedback** they receive we took responses from the 2020 and 2021 NSS surveys and aggregated them for the following questions:
*   The criteria used in marking have been clear in advance

*   Marking and assessment has been fair

*   Feedback on my work has been timely

*   I have received helpful comments on my work
The overall satisfaction rate for each provider is displayed, and the average response is used with a 8% weighting.
To assess the **overall satisfaction**of students with their courses we aggregated responses from the 2020 and 2021 NSS surveys for the question “overall, I am satisfied with the quality of the course”.
The overall satisfaction rate for each provider is displayed, and the average response is used with a 4% weighting.
Data was released at the CAH (common aggregation hierarchy) levels of aggregation and we used details of how these map to HECOS (Higher Education classification of subjects) to weight and aggregate results for each of our 54 subjects, prioritising results from the most granular level.

## _What are the metrics?_
**Value Added**In order to assess the extent to which each department will support its students towards achieving good grades, we use value added scores to track students from enrolment to graduation. A student’s chances of getting a good classification of degree (a 1st or a 2:1) are already affected by the qualifications that they start with so our scores take this into account and report the extent to which a student exceeded expectations.
Each full-time student is given a probability of achieving a 1st or 2:1, based on the qualifications that they enter with or, if they have vague entry qualifications, the total percentage of good degrees expected for the student in their department. If they manage to earn a good degree, then they score points that reflect how difficult it was to do so (in fact, they score the reciprocal of the probability of getting a 1st or 2:1). Otherwise they score zero. Students taking integrated masters are always regarded as having a positive outcome.
At least 30 students must be in a subject for a meaningful value added score to be calculated using the most recent year of data alone. If there are more than 15 students in the most recent year and the total number across two years reaches 30, then a two-year average is calculated.
This metric is expressed as points/10 and contributes 15% to the total score of a department.
**Career prospects**Using results from the Graduate Outcomes survey for the graduating cohort of 2017/18, we seek to assess the extent to which students have taken a positive first step in the 15 months after graduation, in the hope that similar patterns will repeat for future cohorts. We value students that enter graduate level occupations (approximated by SOC groups 1-3: professional, managerial & technical occupations) and students that go on to further study at a professional or HE level and treat these students as positive.
</excerpt>
### Rank 3 of 209 — 0.10
<excerpt title="Methodology behind the Guardian University Guide 2022">
## _What are the metrics?_
**Expenditure per student**In order to approximate the level of resources that a student could expect to have dedicated to their provision, we look at the total expenditure in each subject area and divide it by the volume of students taking the subject. We exclude academic staff costs as the benefits of high staff volumes are already captured by the student-staff ratios but recognise that many costs of delivery are centralised: we add the amount of money each provider has spent per students on academic services such as libraries and computing facilities per student, over the past 2 years.
This metric is expressed as points/10 and contributes 5% to the total score of a department.
**Continuation**Taking a degree-level course is a positive experience for most students but is not suited to everybody and some students struggle and discontinue their studies. Providers can do a lot to support their students – they might promote engagement with studies and with the broader higher education experience - and this measure captures how successful each department is in achieving this. We look at the proportion of students who continue their studies beyond the first year and measure the extent to which this exceeds expectations based on entry qualifications.
To achieve this, we take all first-year students on full-time first-degree courses that are scheduled to take longer than a year to complete and look ahead to 1 December in the following academic year to observe the proportion who are still active in higher education. This proportion is viewed positively, regardless of whether the student has switched course, transferred to a different provider, or been required to repeat their first year – only those who become inactive in the UK’s HE system are counted negatively.
To take the effect of entry qualifications into account we create an index score for each student who has a positive outcome, using their expectation of continuation up to a maximum of 97%. To calculate the score there must have been 35 entrants in the most recent cohort and 65 across the last 2 or 3 years.
This index score, aggregated across the last 2 or 3 years, contributes 15% to the total score of non-medical departments. However, it is the percentage score – also averaged over 2 or 3 years – that is displayed.

## _What are the metrics?_
**Student satisfaction**The National Student Survey asks final year students for the extent to which they agree with 27 positive statements about their academic experience of the course and support that they received. Responses are on a 5-point Likert scale (1. definitely disagree to 5. definitely agree) and we take the responses from full-time first-degree students registered at the provider course to produce two statistics: a satisfaction rate and an average response. The satisfaction rate looks across the questions concerned and reports the proportion of responses that were ‘definitely agree’ or ‘mostly agree’ while the average response gives the average Likert score between 1 and 5 that was observed in the responses to those questions.
To assess the **teaching quality** that a student can expect to experience we took responses from the 2020 and 2021 NSS surveys and aggregated them for the following questions:
*   Staff are good at explaining things

*   Staff have made the subject interesting

*   The course is intellectually stimulating

*   My course has challenged me to achieve my best work
The overall satisfaction rate for each provider is displayed, and the average response is used with a 8% weighting.
To assess the likelihood that a student will be satisfied with **assessment** procedures and the **feedback** they receive we took responses from the 2020 and 2021 NSS surveys and aggregated them for the following questions:
*   The criteria used in marking have been clear in advance

*   Marking and assessment has been fair

*   Feedback on my work has been timely

*   I have received helpful comments on my work
The overall satisfaction rate for each provider is displayed, and the average response is used with a 8% weighting.
To assess the **overall satisfaction**of students with their courses we aggregated responses from the 2020 and 2021 NSS surveys for the question “overall, I am satisfied with the quality of the course”.
The overall satisfaction rate for each provider is displayed, and the average response is used with a 4% weighting.
Data was released at the CAH (common aggregation hierarchy) levels of aggregation and we used details of how these map to HECOS (Higher Education classification of subjects) to weight and aggregate results for each of our 54 subjects, prioritising results from the most granular level.
</excerpt>
### Rank 4 of 209 — 0.09
<excerpt title="Methodology behind the Guardian University Guide 2022">
## _What are the metrics?_
**Entry standards**This measure seeks to approximate the aptitude of fellow students who a prospective student can anticipate and reports the observed average grades of students joining the department – not the conditions of admission to the course that may be advertised. Average tariffs are determined by taking the total tariff points of first-year, first-degree, full-time entrants who were aged under 21 at the start of their course, if the qualifications that they entered with could all be expressed using the tariff system devised by UCAS. There must be more than seven students in any meaningful average and only students entering year 1 of a course (not a foundation year) with certain types of qualification are included. Departments that are dominated by mature entrants are not considered appropriate for this statistic because the age filter would capture and represent the entry tariff of only the minority of students.
This metric contributes 15% to the total score of a department, and refers to those who entered the department in 2019/20.
**Student-staff ratios**Student-staff ratios seek to approximate the levels of staff contact that a student can expect to receive by dividing the volume of students who are taking modules in a subject by the volume of staff who are available to teach it. Thus a low ratio is treated positively – it indicates that more staff contact could be anticipated.
Staff and students are reported on a ‘full time equivalent’ basis and research-only staff are excluded from the staff volume. Students on placement or on a course that is franchised to another provider have their volume discounted accordingly.
At least 28 students and three staff (both FTE) must be present in an SSR calculation using 2019/20 data alone. Smaller departments that had at least seven student and two staff FTE in 2019/20, and at least 30 student FTE in total across 2018/19 and 2019/20, have a two-year average calculated.
This metric contributes 15% to the total score of a department. It is released at HESA cost centre level, and we map each cost centre to one or more of our subjects.

## _What are the metrics?_
**Expenditure per student**In order to approximate the level of resources that a student could expect to have dedicated to their provision, we look at the total expenditure in each subject area and divide it by the volume of students taking the subject. We exclude academic staff costs as the benefits of high staff volumes are already captured by the student-staff ratios but recognise that many costs of delivery are centralised: we add the amount of money each provider has spent per students on academic services such as libraries and computing facilities per student, over the past 2 years.
This metric is expressed as points/10 and contributes 5% to the total score of a department.
**Continuation**Taking a degree-level course is a positive experience for most students but is not suited to everybody and some students struggle and discontinue their studies. Providers can do a lot to support their students – they might promote engagement with studies and with the broader higher education experience - and this measure captures how successful each department is in achieving this. We look at the proportion of students who continue their studies beyond the first year and measure the extent to which this exceeds expectations based on entry qualifications.
To achieve this, we take all first-year students on full-time first-degree courses that are scheduled to take longer than a year to complete and look ahead to 1 December in the following academic year to observe the proportion who are still active in higher education. This proportion is viewed positively, regardless of whether the student has switched course, transferred to a different provider, or been required to repeat their first year – only those who become inactive in the UK’s HE system are counted negatively.
To take the effect of entry qualifications into account we create an index score for each student who has a positive outcome, using their expectation of continuation up to a maximum of 97%. To calculate the score there must have been 35 entrants in the most recent cohort and 65 across the last 2 or 3 years.
This index score, aggregated across the last 2 or 3 years, contributes 15% to the total score of non-medical departments. However, it is the percentage score – also averaged over 2 or 3 years – that is displayed.
</excerpt>
### Rank 5 of 209 — 0.09
<excerpt title="Methodology behind the Guardian University Guide 2022">
## How do we use the metric results?
First of all, we determine if a department has enough data to support a ranking. Often individual metrics are missing and we seek to keep the department in the rankings where we can. An institution can only be included in the table if the weighting value of any indicators that are missing add up to 40% or less, and if the institution’s relevant department teaches at least 35 full time first degree students. There must also be at least 25 students (FTE) in the relevant cost centre.
For those institutions that qualify for inclusion in the subject table, each score is compared to the average score achieved by the other institutions that qualify, using standard deviations to gain a normal distribution of standardised scores (S-scores). The standardised score for student: staff ratios is negative, to reflect that low ratios are regarded as better. We cap certain S-scores – extremely high NSS, expenditure and SSR figures – at three standard deviations. This is to prevent a valid but extreme value from exerting an influence that far exceeds that of all other measures.
For metrics in subjects where there are very few datapoints we refer to the distribution of scores observed for a higher aggregation of subjects (CAH1). As mentioned earlier, we also set a minimum standard deviation for each metric and make adjustments to the mean tariff that is referenced by departments with students who entered with Scottish Highers or Advanced Highers.
Although we don’t display anything, we need to plug the gap left in the total score that is left by any missing indicators. We use a substitution that firstly looks for the corresponding standardised score in the previous year and then, if nothing is available, resorts to looking at whether the missing metric is correlated to general performance in that subject. If it is, the department’s performance in the other metrics is used – effectively assuming that it would have performed as well in the missing metric as it did in everything else. If not, the average score achieved by other providers of the subject is used.
Using the weighting attached to each metric, the standardised scores are weighted and totalled to give an overall institutional score (rescaled to 100) against which the departments are ranked.
**The institutional ranking**The institutional table ranks institutions according to their performance in the subject tables, but considers two other factors when calculating overall performance.

## How do we use the metric results?
First, the number of students in a department influences the extent to which that department’s total standardised score contributes to the institution’s overall score. And second, the number of institutions included in the subject table determines the extent to which a department can affect the institutional table.
The number of full-time undergraduates in each subject is expressed as a percentage of the total number of full-time undergraduates counted in subjects for which the institution is included within the subject table. For each subject, the number of institutions included within the table is counted and the natural logarithm of this value is calculated. The total S-Score for each subject – which can be negative or positive – is multiplied by these two values, and the results are summed for all subjects, to give an overall S-score for each institution. Institutions are ranked according to this overall S-score, though the value displayed in the published table is a scaled version of this, that gives the top university 100 points and all the others a smaller (but positive) points tally.
Each institution has overall versions of each of the indicators displayed next to its overall score out of 100, but these are crude institutional averages that are otherwise disconnected from the tables and give no consideration to subject mix. Therefore these institutional averages cannot be used to calculate the overall score or ranking position.
The indicators of performance for value added and for expenditure per student are treated slightly differently, because they need to be converted into points out of 10 before being displayed. Therefore these indicators do read from the subject level tables, again using student numbers to create a weighted average.
Institutions that appear in fewer than eight subject tables are not included in the main ranking of universities.
**Course directory**The KIS database of courses, to which institutions provide regular updates to describe courses that students will be able to apply for in future years, is the data source of the courses that we list under each department in each subject group.
We have associated each full-time course with one or more subject groups, based on the subject data associated with the courses. We gave institutions the freedom to adjust these associations with subjects and also to change details of the courses. We include courses that are not at degree level, even though such provision is excluded from the data used to generate scores and rankings. Due to timing of publication, an update to this data will take place in September.
</excerpt>

## Search 9 — query: "guardian institutional 2022 csv "University" "Guardian" 2022 institutional table"
### Rank 1 of 912 — 0.46 (passed on)
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
### Rank 2 of 912 — 0.39
<excerpt title="The Guardian University Guide 2025 – the rankings">
Value added score/10 This score compares students’ degree results with their entry qualifications, to show how effectively they are taught. It is given as a rating out of 10 6.8
Career after 15 months Percentage of graduates who find graduate-level jobs, or are in further study at professional or HE level, within 15 months of graduation 93
Contin-uation Percentage of first-year students continuing to second year 96.6  
5 5 Imperial College 82.6 85.5 64.4 11.9 8.6 204 6.6 96 95.6  
Satisfied with teaching The rating for the quality of teaching on the course, given by final-year students in the NSS 85.5
Satisfied with feedback The rating for the quality of feedback and assessment, given by final-year students in the NSS 64.4
Student to staff ratio Number of students per member of teaching staff 11.9
Spend per student/10 Money spent on each student, excluding academic staff costs, given as a rating out of 10 8.6
Average entry tariff Typical Ucas scores of young entrants (under 21) to the department 204
Value added score/10 This score compares students’ degree results with their entry qualifications, to show how effectively they are taught. It is given as a rating out of 10 6.6
Career after 15 months Percentage of graduates who find graduate-level jobs, or are in further study at professional or HE level, within 15 months of graduation 96
Contin-uation Percentage of first-year students continuing to second year 95.6  
6 7 Durham 80.8 87.9 74.2 13.5 6.2 185 6.2 91 97.5  
Satisfied with teaching The rating for the quality of teaching on the course, given by final-year students in the NSS 87.9
Satisfied with feedback The rating for the quality of feedback and assessment, given by final-year students in the NSS 74.2
Student to staff ratio Number of students per member of teaching staff 13.5
</excerpt>
### Rank 3 of 912 — 0.36
<excerpt title="The Guardian University Guide 2025 – the rankings">
Satisfied with feedback The rating for the quality of feedback and assessment, given by final-year students in the NSS 76.1
Student to staff ratio Number of students per member of teaching staff 13.9
Spend per student/10 Money spent on each student, excluding academic staff costs, given as a rating out of 10 7.4
Average entry tariff Typical Ucas scores of young entrants (under 21) to the department 179
Value added score/10 This score compares students’ degree results with their entry qualifications, to show how effectively they are taught. It is given as a rating out of 10 4.1
Career after 15 months Percentage of graduates who find graduate-level jobs, or are in further study at professional or HE level, within 15 months of graduation 89
Contin-uation Percentage of first-year students continuing to second year 96.3  
9 8 UCL 74.8 84.2 69.7 10.9 7.2 183 5.9 90 96.4  
Satisfied with teaching The rating for the quality of teaching on the course, given by final-year students in the NSS 84.2
Satisfied with feedback The rating for the quality of feedback and assessment, given by final-year students in the NSS 69.7
Student to staff ratio Number of students per member of teaching staff 10.9
Spend per student/10 Money spent on each student, excluding academic staff costs, given as a rating out of 10 7.2
Average entry tariff Typical Ucas scores of young entrants (under 21) to the department 183
Value added score/10 This score compares students’ degree results with their entry qualifications, to show how effectively they are taught. It is given as a rating out of 10 5.9
Career after 15 months Percentage of graduates who find graduate-level jobs, or are in further study at professional or HE level, within 15 months of graduation 90

Contin-uation Percentage of first-year students continuing to second year 96.4  
10 10 Loughborough 74.6 87.6 75.6 14.1 4.5 162 5.5 89 96.6  
Satisfied with teaching The rating for the quality of teaching on the course, given by final-year students in the NSS 87.6
Satisfied with feedback The rating for the quality of feedback and assessment, given by final-year students in the NSS 75.6
Student to staff ratio Number of students per member of teaching staff 14.1
Spend per student/10 Money spent on each student, excluding academic staff costs, given as a rating out of 10 4.5
Average entry tariff Typical Ucas scores of young entrants (under 21) to the department 162
Value added score/10 This score compares students’ degree results with their entry qualifications, to show how effectively they are taught. It is given as a rating out of 10 5.5
Career after 15 months Percentage of graduates who find graduate-level jobs, or are in further study at professional or HE level, within 15 months of graduation 89
Contin-uation Percentage of first-year students continuing to second year 96.6  
11 11 Lancaster 73.5 87.4 76.5 14 6.7 154 5.7 86 96.8  
Satisfied with teaching The rating for the quality of teaching on the course, given by final-year students in the NSS 87.4
Satisfied with feedback The rating for the quality of feedback and assessment, given by final-year students in the NSS 76.5
Student to staff ratio Number of students per member of teaching staff 14
Spend per student/10 Money spent on each student, excluding academic staff costs, given as a rating out of 10 6.7
Average entry tariff Typical Ucas scores of young entrants (under 21) to the department 154
Value added score/10 This score compares students’ degree results with their entry qualifications, to show how effectively they are taught. It is given as a rating out of 10 5.7
</excerpt>
### Rank 4 of 912 — 0.35
<excerpt title="The Guardian University Guide 2025 – the rankings">
Satisfied with feedback The rating for the quality of feedback and assessment, given by final-year students in the NSS 75
Student to staff ratio Number of students per member of teaching staff 18.8
Spend per student/10 Money spent on each student, excluding academic staff costs, given as a rating out of 10 7.2
Average entry tariff Typical Ucas scores of young entrants (under 21) to the department 210
Value added score/10 This score compares students’ degree results with their entry qualifications, to show how effectively they are taught. It is given as a rating out of 10 4.2
Career after 15 months Percentage of graduates who find graduate-level jobs, or are in further study at professional or HE level, within 15 months of graduation 86
Contin-uation Percentage of first-year students continuing to second year 93.6  
18 18 Exeter 66.2 87 72.2 16.3 4.7 163 6.2 86 96.2  
Satisfied with teaching The rating for the quality of teaching on the course, given by final-year students in the NSS 87
Satisfied with feedback The rating for the quality of feedback and assessment, given by final-year students in the NSS 72.2
Student to staff ratio Number of students per member of teaching staff 16.3
Spend per student/10 Money spent on each student, excluding academic staff costs, given as a rating out of 10 4.7
Average entry tariff Typical Ucas scores of young entrants (under 21) to the department 163
Value added score/10 This score compares students’ degree results with their entry qualifications, to show how effectively they are taught. It is given as a rating out of 10 6.2
Career after 15 months Percentage of graduates who find graduate-level jobs, or are in further study at professional or HE level, within 15 months of graduation 86

Contin-uation Percentage of first-year students continuing to second year 96.2  
19 21 Surrey 65.4 87.7 80.5 14.4 5.4 142 4 88 93.7  
Satisfied with teaching The rating for the quality of teaching on the course, given by final-year students in the NSS 87.7
Satisfied with feedback The rating for the quality of feedback and assessment, given by final-year students in the NSS 80.5
Student to staff ratio Number of students per member of teaching staff 14.4
Spend per student/10 Money spent on each student, excluding academic staff costs, given as a rating out of 10 5.4
Average entry tariff Typical Ucas scores of young entrants (under 21) to the department 142
Value added score/10 This score compares students’ degree results with their entry qualifications, to show how effectively they are taught. It is given as a rating out of 10 4
Career after 15 months Percentage of graduates who find graduate-level jobs, or are in further study at professional or HE level, within 15 months of graduation 88
Contin-uation Percentage of first-year students continuing to second year 93.7  
20 21 Sheffield 65.3 86.4 78 14.4 5.7 157 5.2 86 95.7  
Satisfied with teaching The rating for the quality of teaching on the course, given by final-year students in the NSS 86.4
Satisfied with feedback The rating for the quality of feedback and assessment, given by final-year students in the NSS 78
Student to staff ratio Number of students per member of teaching staff 14.4
Spend per student/10 Money spent on each student, excluding academic staff costs, given as a rating out of 10 5.7
Average entry tariff Typical Ucas scores of young entrants (under 21) to the department 157
Value added score/10 This score compares students’ degree results with their entry qualifications, to show how effectively they are taught. It is given as a rating out of 10 5.2
</excerpt>
### Rank 5 of 912 — 0.35
<excerpt title="The Guardian University Guide 2025 – the rankings">
Satisfied with feedback The rating for the quality of feedback and assessment, given by final-year students in the NSS 78.8
Student to staff ratio Number of students per member of teaching staff 15.8
Spend per student/10 Money spent on each student, excluding academic staff costs, given as a rating out of 10 5.4
Average entry tariff Typical Ucas scores of young entrants (under 21) to the department 130
Value added score/10 This score compares students’ degree results with their entry qualifications, to show how effectively they are taught. It is given as a rating out of 10 5.7
Career after 15 months Percentage of graduates who find graduate-level jobs, or are in further study at professional or HE level, within 15 months of graduation 84
Contin-uation Percentage of first-year students continuing to second year 94.6  
36 37 Birmingham 61.2 83.9 70.7 14.6 5.8 157 4.7 88 96  
Satisfied with teaching The rating for the quality of teaching on the course, given by final-year students in the NSS 83.9
Satisfied with feedback The rating for the quality of feedback and assessment, given by final-year students in the NSS 70.7
Student to staff ratio Number of students per member of teaching staff 14.6
Spend per student/10 Money spent on each student, excluding academic staff costs, given as a rating out of 10 5.8
Average entry tariff Typical Ucas scores of young entrants (under 21) to the department 157
Value added score/10 This score compares students’ degree results with their entry qualifications, to show how effectively they are taught. It is given as a rating out of 10 4.7
Career after 15 months Percentage of graduates who find graduate-level jobs, or are in further study at professional or HE level, within 15 months of graduation 88

Contin-uation Percentage of first-year students continuing to second year 96  
37 27 Leeds 61.1 81.2 67 14.4 7.3 163 5.3 86 96  
Satisfied with teaching The rating for the quality of teaching on the course, given by final-year students in the NSS 81.2
Satisfied with feedback The rating for the quality of feedback and assessment, given by final-year students in the NSS 67
Student to staff ratio Number of students per member of teaching staff 14.4
Spend per student/10 Money spent on each student, excluding academic staff costs, given as a rating out of 10 7.3
Average entry tariff Typical Ucas scores of young entrants (under 21) to the department 163
Value added score/10 This score compares students’ degree results with their entry qualifications, to show how effectively they are taught. It is given as a rating out of 10 5.3
Career after 15 months Percentage of graduates who find graduate-level jobs, or are in further study at professional or HE level, within 15 months of graduation 86
Contin-uation Percentage of first-year students continuing to second year 96  
38 38 Northumbria 60.7 83.4 80.1 15.5 4.8 143 6.6 82 89.2  
Satisfied with teaching The rating for the quality of teaching on the course, given by final-year students in the NSS 83.4
Satisfied with feedback The rating for the quality of feedback and assessment, given by final-year students in the NSS 80.1
Student to staff ratio Number of students per member of teaching staff 15.5
Spend per student/10 Money spent on each student, excluding academic staff costs, given as a rating out of 10 4.8
Average entry tariff Typical Ucas scores of young entrants (under 21) to the department 143
Value added score/10 This score compares students’ degree results with their entry qualifications, to show how effectively they are taught. It is given as a rating out of 10 6.6
</excerpt>

## Search 10 — query: "Guardian 2022 data institutional Guardian 2022 institutional.csv Guardian 2022 institutional "guardian" "2022""
### Rank 1 of 797 — 0.08 (passed on)
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
### Rank 2 of 797 — 0.08
<excerpt title="ICCS 2022 Technical Report">
## [PDF page 135]
Latvia  93.4  96.7  100  88.6  82.8  85.7
Malta  100  100  100  89.3  89.3  89.3  
Netherlands  57.7  83.2  100  89.5  51.6  74.5
Norway (9)  96.6  96.6  99.3  88.6  84.9  84.9
Poland  91.2  99.4  99.6  91  82.6  90.1  
Romania  82.9  97.5  100  93.5  77.5  91.1
Serbia  88.7  92  98.6  88.1  77  79.9  
Slovak Republic  91.9  96.2  100  93.2  85.6  89.7
Slovenia  90.2  96.6  100  94.9  85.6  91.6
Spain  96.9  98.1  100  90.2  87.4  88.6  
Sweden  94.2  96.8  100  89.8  84.6  86.9
Benchmarking participant
North Rhine-Westphalia  89.5  95.4  99.4  88.2  78.4  83.6  
Schleswig-Holstein  57  73.7  98.8  80  45.1  58.3
</excerpt>
### Rank 3 of 797 — 0.07
<excerpt title="Guardian Pharmacy Services, Inc. (GRDN) institutional holders">
## Coverage & totals by quarter
Reporting institutions
Disclosed shares
Disclosed value
Counts also change with data coverage and reporting entities; they do not measure net buying.Distinct managers with a live stock row in this CUSIP; totals may include overlapping filings and are not a share of the company.

## Explore all 197 reporting institutions.
This page includes 20 of 197 reporting institutions. Log in to look up the full history beyond 3 years, use advanced screening & filtering, download CSV, and get the complete set through the Akkru API.
*   Download CSV  
*   Earlier quarters  
*   Advanced screening & filtering  
*   API & AI access
Already have an account?
＋ New accounts get free API credits to explore data beyond ownership filings.
For AI agents & developers  
The initial HTML of this page carries its exact data as script#research-data (JSON): values, units, scope, preview limits and SEC sources. Read it directly, no script or API key needed; script#research-access says what needs an account. This page lists 20 of 197 reporting institutions; totals use the complete disclosed data.
Without an account: the last 3 years, with the row caps stated on the page. A free account opens all history on file on these pages and the CSV of what a page shows. Rows beyond the caps and bulk retrieval go through the authenticated API / MCP / CLI.
MCP  https://api.akkrudata.ai/mcp
akkru_institutional_holdings  
{"action":"holders","cusip":"40145W101","quarter":"2026Q3","type":"positions","page_size":100}
Connect to MCP with OAuth and follow the returned pagination. Credits and usage limits depend on the account.
MCP endpoint https://api.akkrudata.ai/mcp API / MCP / CLI documentation/documentsllms.txt/llms.txt
Sources, coverage & how to read this data  
Figures are as reported to the SEC and merged with later amendments where Akkru could match them. Preview limits apply to what is listed, not to the totals, which come from the complete reported data. Nothing is zero-filled: a missing quarter or month is shown as missing.
Akkru Data
We use cookies to measure how our advertising performs. Essential cookies are always on; advertising cookies are set only if you accept.We use cookies to measure our ads.
40
</excerpt>
### Rank 4 of 797 — 0.06
<excerpt title="ICCS 2022 Technical Report">
## [PDF page 153]
Country  CX2W F O2  CX4FKC1  CX4FWC2  CX2W F O1  CX4NHC2  CX2BIO1  CX4DVC1  CX3CPO1  CX3CPO2  CX4SLC3  CX4SLC4  
Br az i l  66  68  75  61  63  58  63  71  60  79  78  
Bulgaria  74  62  68  71  80  76  69  76  81  85  88  
C h i n es e  Ta i p ei  87  80  85  74  68  74  73  88  90  92  92  
Colom bia  70  73  75  72  75  80  77  70  83  84  89  
Croat ia  83  83  96  92  91  85  93  95  96  95  95  
Cyprus  93  85  77  87  100  80  87  66  66  94  92  
Den m a r k  95  91  96  92  92  95  92  95  95  94  97  
Es t o n i a  84  96  96  91  91  87  91  79  80  90  83
</excerpt>
### Rank 5 of 797 — 0.05
<excerpt title="ICCS 2022 Technical Report">
## [PDF page 153]
F rance  71  80  87  81  84  88  83  83  82  -  91  
It al y  82  88  90  84  87  89  84  89  87  86  88  
Latvia  67  80  88  68  63  75  71  64  59  79  84  
Lithuania  95  96  95  97  94  98  98  91  90  94  96  
M alt a  82  79  77  78  80  84  84  66  70  88  85  
Netherlands  80  79  81  79  80  85  87  84  91  87  90  
North Rhine-Westphalia*  62  77  76  77  81  83  78  72  72  84  86  
Norway  79  68  79  76  74  85  79  73  83  86  87  
P oland  95  95  97  95  98  97  94  97  98  93  96  
Rom ani a  100  100  100  100  100  100  100  100  100  100  100
</excerpt>

# Example 5
## Question
Of the natural sites on the UNESCO list of World Heritage in Danger, only a few sites are located in one of the original members of the United Nations. In which country is the site with the largest reported area according to Protected Planet?

## Expected answer
Mexico

## Grade 0.00

## Search 1 — query: "list of founding members of the United Nations 1945 original members"
### Rank 1 of 153 — 0.71 (passed on)
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
### Rank 2 of 153 — 0.63
<excerpt title="Member states of the United Nations">
In principle, only sovereign states can become UN members,[[8]](https://en.wikipedia.org/wiki/Member_states_of_the_United_Nations#cite_note-United_Nations-9) and currently, all UN members are sovereign states. Although five members were not sovereign when they joined the UN, they all subsequently became fully independent between 1946 and 1991.[[9]](https://en.wikipedia.org/wiki/Member_states_of_the_United_Nations#cite_note-10) Because a state can only be admitted to membership in the UN by the approval of the Security Council and the General Assembly,[[10]](https://en.wikipedia.org/wiki/Member_states_of_the_United_Nations#cite_note-11)[[8]](https://en.wikipedia.org/wiki/Member_states_of_the_United_Nations#cite_note-United_Nations-9)a number of states that are considered sovereign according to the Montevideo Convention are not members of the UN. This is because the UN does not consider them to possess sovereignty, mainly due to the lack of international recognition or due to opposition from one of the permanent members.
In addition to the member states, the UN also invites non-member states to become observer states at the UN General Assembly,[[11]](https://en.wikipedia.org/wiki/Member_states_of_the_United_Nations#cite_note-12) allowing them to participate and speak in General Assembly meetings, but not vote. Observers are generally intergovernmental organizations and international organizations and entities whose statehood or sovereignty is not precisely defined.
The world in 1945, after World War II. In light blue, the founding members of the United Nations. In dark blue, protectorates and territories of the founding members.

The UN officially came into existence on 24 October 1945, after ratification of the United Nations Charter by the five permanent members of the United Nations Security Council (the Republic of China, France, the Soviet Union, the United Kingdom, and the United States) and a majority of the other signatories.[[12]](https://en.wikipedia.org/wiki/Member_states_of_the_United_Nations#cite_note-13) A total of 51 original members (or founding members) joined that year; 50 of them signed the Charter at the United Nations Conference on International Organization in San Francisco on 26 June 1945, while Poland, which was not represented at the conference, signed it on 15 October 1945.[[13]](https://en.wikipedia.org/wiki/Member_states_of_the_United_Nations#cite_note-14)[[14]](https://en.wikipedia.org/wiki/Member_states_of_the_United_Nations#cite_note-originalmembers-15)
</excerpt>
### Rank 3 of 153 — 0.63
<excerpt title="United Nations">
The October 1943 Moscow Conference resulted in the Moscow Declarations, including the Four Power Declaration on General Security. This declaration was signed by the Allied Big Four—the United States, the Soviet Union, the United Kingdom, and China—and aimed for the creation "at the earliest possible date of a general international organization". This was the first public announcement that a new international organization was being contemplated to replace the League of Nations. The Tehran Conference followed shortly afterwards at which Roosevelt, Churchill and Joseph Stalin, the leader of the Soviet Union, met and discussed the idea of a post-war international organization.[22]
The new international organization was formulated and negotiated amongst the delegations from the Allied Big Four at the Dumbarton Oaks Conference from 21 September to 7 October 1944. They agreed on proposals for the aims, structure and functioning of the new organization.[23][24][25] It took the conference at Yalta in February 1945, and further negotiations with the Soviet Union, before all the issues were resolved.[23]
Founding (1945)  
The UN in 1945: founding members in light blue, protectorates and territories of the founding members in dark blue (Some nations' land would be different from now.)

By 1 March 1945, 21 additional states had signed the Declaration by the United Nations.[26] After months of planning, the UN Conference on International Organization opened in San Francisco on 25 April 1945. It was attended by 50 nations' governments and a number of non-governmental organizations.[27][28][29] The delegations of the Big Four chaired the plenary meetings.[30] Previously, Churchill had urged Roosevelt to restore France to its status of a major power after the liberation of Paris in August 1944. The drafting of the Charter of the United Nations was completed over the following two months, and it was signed on 26 June 1945 by the representatives of the 50 countries.[31][32] The UN officially came into existence at 20:07 (UTC) on 24 October 1945,[33][34] upon ratification of the Charter by the five permanent members of the Security Council: the United States, the United Kingdom, France, the Soviet Union and China — and by a majority of the other 46 nations.[35][36]
The first meetings of the General Assembly, with 51 nations represented,[b] and the Security Council took place in London beginning in January 1946.[35] Debates began at once, covering topical issues such as the presence of Soviet troops in Iranian Azerbaijan and British forces in Greece.[39] British diplomat Gladwyn Jebb served as interim secretary-general.
The General Assembly selected New York City as the site for the headquarters of the UN. Construction began on 14 September 1948 and the facility was completed on 9 October 1952. The Norwegian Foreign Minister, Trygve Lie, was the first elected UN secretary-general.[35]
Cold War (1947–1991)  
Dag Hammarskjöld was a particularly active secretary-general from 1953 until his death in 1961.
</excerpt>
### Rank 4 of 153 — 0.63
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
### Rank 5 of 153 — 0.62
<excerpt title="Member states of the United Nations">
The UN officially came into existence on 24 October 1945, after ratification of the United Nations Charter by the five permanent members of the United Nations Security Council (the Republic of China, France, the Soviet Union, the United Kingdom, and the United States) and a majority of the other signatories.[[12]](https://en.wikipedia.org/wiki/Member_states_of_the_United_Nations#cite_note-13) A total of 51 original members (or founding members) joined that year; 50 of them signed the Charter at the United Nations Conference on International Organization in San Francisco on 26 June 1945, while Poland, which was not represented at the conference, signed it on 15 October 1945.[[13]](https://en.wikipedia.org/wiki/Member_states_of_the_United_Nations#cite_note-14)[[14]](https://en.wikipedia.org/wiki/Member_states_of_the_United_Nations#cite_note-originalmembers-15)

The original members of the United Nations were: France (then the Provisional Government), Russia (then the Soviet Union), China (then Republic of China), the United Kingdom, the United States—these first five forming the Security Council—Argentina, Australia, Belarus (then the Byelorussian SSR), Belgium, Bolivia, Brazil (then the Vargas Era Brazil), Canada, Chile (then the 1925–73 Presidential Republic), Colombia, Costa Rica, Cuba (then the 1902–59 Republic), Czechoslovakia (then the Third Republic), Denmark, the Dominican Republic, Ecuador, Egypt (then the Kingdom of Egypt), El Salvador, Ethiopia (then the Ethiopian Empire), Greece (then the Kingdom of Greece), Guatemala, Haiti (then the 1859–1957 Republic), Honduras, India (then the British Raj), Iran (then the Imperial State of Iran), Iraq (then the Kingdom of Iraq), Lebanon, Liberia, Luxembourg, Mexico, the Netherlands, New Zealand (then the Dominion of New Zealand), Nicaragua, Norway, Panama, Paraguay, Peru, the Philippines (then the Commonwealth), Poland (then the Provisional Government of National Unity), Saudi Arabia, South Africa (then the Union of South Africa), Syria (then the Mandatory Republic), Turkey, Ukraine (then the Ukrainian SSR), Uruguay, Venezuela and Yugoslavia (then the Democratic Federal Yugoslavia).[[14]](https://en.wikipedia.org/wiki/Member_states_of_the_United_Nations#cite_note-originalmembers-15)
Among the original members, 49 are either still UN members or had their memberships in the UN continued by a successor state_(see table below)_; for example, the membership of the Soviet Union was continued by the Russian Federation after its dissolution _(see the section Former members: Union of Soviet Socialist Republics)_. The other two original members, Czechoslovakia and Yugoslavia (i.e., the Socialist Federal Republic of Yugoslavia), had been dissolved and their memberships in the UN not continued from 1992 by any one successor state _(see the sections Former members: Czechoslovakia and Former members: Yugoslavia)_.[[14]](https://en.wikipedia.org/wiki/Member_states_of_the_United_Nations#cite_note-originalmembers-15)
</excerpt>

## Search 2 — query: "Protected Planet site UNESCO World Heritage in Danger natural area largest"
### Rank 1 of 89 — 0.66 (passed on)
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
### Rank 2 of 89 — 0.42
<excerpt title="IUCN advises “in danger” status for three World Heritage sites">
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

# IUCN advises “in danger” status for three World Heritage sites
### Power plants put the Sundarbans in danger
IUCN recommends placing the Sundarbans in Bangladesh on the List of World Heritage in Danger, due to severe threats from coal-fired power plants and numerous industrial activities in close proximity. The site is part of the world’s largest mangrove forest, home to the royal Bengal tiger.
Following a joint IUCN-UNESCO mission in 2016, the World Heritage Committee called for the large Rampal power plant project, planned 65km from the site, to be cancelled and relocated. Despite this, its construction has continued without any assessment of its impact on the Sundarbans’ World Heritage values.
Two additional coal-fired power plants are being constructed on the Payra River, which flows into the same bay as the Sundarbans. Over 150 industrial projects are also active upstream of the site, and their associated shipping and dredging activities further threaten its hydrological and ecological dynamics. The hydrological systems, which drive this dynamics, are very large in scale and vulnerable to upstream impacts.

# IUCN advises “in danger” status for three World Heritage sites
### Illegal wildlife trade pushes the vaquita to extinction
In Mexico’s Islands and Protected Areas of the Gulf of California, the vaquita – the smallest and most endangered species of porpoise –faces imminent extinction. The porpoise gets entangled in gillnets used to illegally fish the Critically Endangered totoaba, whose swim bladder fetches high prices in Asian markets.
Alarmingly it is estimated only 10 individual vaquitas are left, compared to 30 in 2017. The site is the only place on Earth where the species exists, which is one of the reasons for its World Heritage status.
Despite Mexico’s extensive efforts to ban gillnets and combat illegal international trafficking of totoaba products, illegal fishing within the site has further escalated in the past two years. IUCN recommends placing the site on the List of World Heritage in Danger to mobilise urgent action to protect the site’s unique marine life and ensure the area with the last remaining vaquitas stays gillnet-free.
</excerpt>
### Rank 3 of 89 — 0.38
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
### Rank 4 of 89 — 0.25
<excerpt title="Central Amazon Conservation Complex">
**Brief description**
This site of more than 6 million hectares is the largest protected area in the Amazon Basin and one of the richest areas of the planet in terms of biodiversity. First, Jaú National Park was inscribed in 2000. The property was subsequently expanded in 2003 with the addition of three other protected areas (Anavilhanas National Park, Amanã Sustainable Development Reserve, and Mamairauá Sustainable Development Reserve). The classification of these four sites developed into the current property entitled Central Amazon Conservation Complex.
Located primarily at the confluence of the Negro and Solimões Rivers, the property contains the majority of the ecosystems recorded in the Amazon, including dryland forests and periodically flooded lowland forests (várzea and igapó, as well as black-water or white-water watercourses, waterfalls, swamps, lakes and beaches. The Anavilhanas Archipelago, one of the largest river archipelagos in the world, is constantly evolving and is home to the largest array of electric fish on the planet. The site protects a wide variety of flora and fauna, including rare and endangered species such as the giant Arapaima (the largest freshwater fish in South America), the giant otter, Amazonian manatee, the black caiman and two species of freshwater dolphins.
**_Criterion (ix)_:** The várzea and igapó flooded forests, lakes, rivers and islands of the site demonstrate ongoing ecological processes in the development of terrestrial and freshwater ecosystems. They include a constantly changing and evolving mosaic of river channels, lakes, and landforms. In constant movement, the floating mats of vegetation typical of the várzea watercourses include a significant number of endemic species and the largest array of electric fishes in the world. Anavilhanas contains the second largest river archipelago in the world, much better preserved than the larger Mariuá Archipelago, located in the same river upstream of Anavilhanas. It illustrates the process of colonization and evolution of the vegetation on changing landforms.

**_Criterion (x)_:** The property protects a large and representative sample of the flora and fauna of the forests of the Amazon Central Plain, with a significant number of terrestrial and aquatic ecosystems associated with the forest which are periodically inundated by seasonal flooding, as well as swamps. Known as one of the largest Endemic Bird Areas and also as a Centre of Plant Diversity, the property protects an impressive variety of flora and fauna species of which around 60% of the fish species living in the Negro River watershed, and 60% of the birds recorded in the Central Amazon region. Characterized by a high degree of endemism, much of the wildlife is nocturnal. The property represents one of the most diverse regions for primates, with endangered species such as the bald uakari (Cacajao calvus) and black squirrel monkey saimiri (Saimiri vanzolinii) and some endangered water species as the giant otter (Pteronura brasiliensis), the Amazonian manatee (Trichechus inunguis) and the black caiman (Melanosuchus Niger). Other notable species are the golden-backed black uakari (Cacajao melanocephalus), yellow caiman (Caiman crocodilus), jaguar (Panthera onca) and harpy eagle (Harpy harpyja), the last two being "near threatened" according to the IUCN Red List. The “pirarucu” (Arapaima gigas), the largest freshwater fish in South America, and two species of river dolphins (Inia geoffrensis and Sotalia fluviatilis), all three with a "data deficient" status, are also found in the property. In addition, 64 species of electric fish, which is the strongest known diversity for this group unique in the world, with a circulation range and an adaptation rate comparable to those of cichlids in the African Rift Valley, have been identified in the property
**Integrity**
The dimensions of the property are sufficient to maintain important ecological and biological processes, such as chablis, fluctuations in the dynamics of flooding and wildfires, which offers unique opportunities to study their effects on biodiversity in natural ecosystems. The dryland forests which constitute a large part of Jau and Amanã are virtually pristine wilderness areas covering millions of hectares.
</excerpt>
### Rank 5 of 89 — 0.21
<excerpt title="The Sundarbans World Heritage site is the largest area of mangrove forest in ...">
# The Sundarbans World Heritage site is the largest area of mangrove forest in the world and it is the only one that is inhabited by the iconic but endangered Bengal tiger. Watch our video to see how the biosphere reserve is working with the local community to create a peaceful co-existence between humans & tigers. 🐯 https://whc.unesco.org/en/list/798 #MangroveDay #Mangroves #WorldHeritage | UNESCO | Facebook
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
World Mangrove Day - World Heritage site the Sundarbans
Like
Comment
Share
![Image 2](blob:http://localhost/85d8b181a20aeb64a3afc2f1c39d2480)
![Image 3](blob:http://localhost/2b45e6f1a2ae097354c0b291152873d5)
314
·
4 comments
·
9.2K views

# Video
## **UNESCO**
Friday, July 26, 2019 at 6:05 PM
July 26, 2019 ·
Follow
The Sundarbans World Heritage site is the largest area of mangrove forest in the world and it is the …
See more

# Video
## Comments
Most relevant
Manoj Kumar
Sundarban
*   7y
Deborah Lee
*   7y
View more comments
2 of 4

# Video
## Related Reels
UNESCO 32K
UNESCO 21K
UNESCO 27K
UNESCO 18K
UNESCO 22K
UNESCO 7.4K
UNESCO 6.6K
UNESCO 40K
UNESCO 10K
UNESCO 32K
UNESCO 17K
UNESCO 11K

# Video
## Related videos
[ 1:12](https://www.facebook.com/100064966710803/videos/1680622763682396/?__so__=permalink&__cft__[0]=AZh2NOkVd2VCnFkbOCkHbMwo8exiNRB3nzIA9OqoeTx5ICTpUV9RCGDpxkk6u3un4YXJgRX57h61Lf_AFPHi-vX2xdLh76nJ-HTdrQ16j0SS-ghDQeP1Oj_mTvnwr8cwmxG7d_Q1LbzXZnZwsgB8zg)
[](https://www.facebook.com/watch/100064966710803/?__cft__[0]=AZh2NOkVd2VCnFkbOCkHbMwo8exiNRB3nzIA9OqoeTx5ICTpUV9RCGDpxkk6u3un4YXJgRX57h61Lf_AFPHi-vX2xdLh76nJ-HTdrQ16j0SS-ghDQeP1Oj_mTvnwr8cwmxG7d_Q1LbzXZnZwsgB8zg)
[Madanjeet_Prize_laureate_V1.mp4](https://www.facebook.com/100064966710803/videos/1680622763682396/?__so__=permalink&__cft__[0]=AZh2NOkVd2VCnFkbOCkHbMwo8exiNRB3nzIA9OqoeTx5ICTpUV9RCGDpxkk6u3un4YXJgRX57h61Lf_AFPHi-vX2xdLh76nJ-HTdrQ16j0SS-ghDQeP1Oj_mTvnwr8cwmxG7d_Q1LbzXZnZwsgB8zg)
</excerpt>

## Search 3 — query: "UNESCO World Heritage in Danger natural sites list"
### Rank 1 of 83 — 0.49 (passed on)
<excerpt title="List of World Heritage in Danger">
# List of World Heritage in Danger
##### Central African Republic
*   Manovo-Gounda St Floris National Park (1997)

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
### Rank 2 of 83 — 0.39
<excerpt title="Facing major threats, six new sites join UNESCO's List of World">
The World Heritage Committee has also decided to inscribe on its List of World Heritage in Danger three sites that had been previously recognized; signaling they are now facing serious threats to the values that justified their inscription in the first place. These are: Ancient City of Taurica Chersonese and its Chora (Ukraine), the Historic Inner City of Paramaribo (Suriname) and Tyre (Lebanon).
The three sites that were nominated for inscription on an emergency basis are:
**Boma-Badingilo Migratory Landscape (South Sudan):** A vast expanse of East African savanna, this site hosts the largest known terrestrial mammal migration in the world, and its unique biodiversity makes it an ecosystem of exceptional global significance. The site also reflects the important cultural, and linguistic diversity of the region with several ethnic groups who have been custodians of this landscape through herding, farming and fishing for centuries and even millennia. The Committee has flagged several serious threats, notably infrastructure development, commercial poaching, and wildlife trafficking and trade, which directly affect the large populations of migratory mammals. A context of persistent insecurity, along with limited institutional and financial capacity, also hinders effective conservation of the site.
**Mount Amel Castles (Lebanon):** The five castles that make up this site bear witness to the evolution of defensive systems in the region from the era of the Crusades and Islamic dynasties through to the end of the 19th century. This site, which had already been granted enhanced protection in November 2024 by UNESCO's Committee for the Protection of Cultural Property in the Event of Armed Conflict, is currently suffering heavy damage. According to the Committee, the ongoing conflict directly jeopardizes the site's conservation and requires urgent intervention.

**Sebastia (State of Palestine):**This site preserves the archaeological record of the successive occupation of the site by different civilizations from at least the 9th century BCE, when Samaria-Sebaste served as the capital of the northern Kingdom of Israel, through the Hellenistic, Roman, Byzantine and Islamic periods, with later architectural remains dating to the Crusader era, as well as the Ayyubid/Mamluk and Ottoman periods, when it was one of the designated “Throne Villages”. The main threat facing the site concerns the planned expropriation and creation of the "Samaria" (Shomron) national park, which could divide the property. In addition to the impact of the conflict in the Middle-East, the site also faces pressures related to development, land-use planning, governance and the erosion of the remains.
**Three sites that were already inscribed on the World Heritage List that have now been inscribed on the List of World Heritage in Danger upon the recommendation of the Committee:**
**Ancient City of Tauric Chersonese and its Chora(Ukraine):**The Committee noted with the deepest concern that, due to the Autonomous Republic of Crimea (Ukraine) being temporarily occupied by the Russian Federation, the State Party is unable to ensure the site’s protection or guarantee its conservation or management. In this context, it welcomed the partnership between UNESCO and UNITAR/UNOSAT, which has enabled since 2014, regular monitoring of the state of conservation of the site using satellite images. These observations revealed a significant deterioration in the authenticity and integrity of the property, resulting from new construction and large-scale archaeological excavations. Given the State Party’s inability to fulfill its conservation responsibilities, as well as the observed damage to the property’s Outstanding Universal Value, the Committee decided to inscribe it on the List of World Heritage in Danger. It also called for strengthened international cooperation to prevent the illicit trafficking of cultural property originating from the Autonomous Republic of Crimea (Ukraine).
</excerpt>
### Rank 3 of 83 — 0.34
<excerpt title="Chart: Where UNESCO World Heritage Is In Danger">
# Where UNESCO World Heritage Is In Danger
by[Katharina Buchholz](mailto:katharina.buchholz@statista.com),
Jul 31, 2024
Travel and tourism worldwide
A look at the current list of cultural UNESCO World Heritage sites in danger shows that most are located in war zones and unstable states, like Syria, Lebanon, Afghanistan, Iraq, Yemen, Venezuela, Libya, Mali, Ukraine and Palestine. The latter in 2024 saw one site added - the Saint Hilarion Monastery or Tell Umm Amer. One of the earliest monastic sites in the Middle East which dates back to the 4th century is located in a coastal region in the Gaza strip and is therefore currently located in an active conflict zone.
In 2023, the historic city centers of Ukrainian cities Lviv, Kiev and Odessa were added to the list due to the ongoing war there. Other World Heritage monuments are threatened by construction projects, like historic sites in Egypt and Uzbekistan as well as the Vienna historic center, where UNESCO is taking issue with the construction of a large new hotel. Increased development in the city was also the reason why Liverpool in the UK lost its World Heritage status in 2021.
Venice and its lagoon was not added to the World Heritage in danger list after having been nominated last year. It would have been the only cultural heritage entry where climate change was having a significant impact. Nepalese pilgrimage site Lumbibi, known as the birthplace of the Buddha, was recommended for inclusion due to disrepair, but was also ultimately not included. The same is true for UK site Stonehenge, which is in the eyes of the UNESCO threatened by the construction of a new motorway tunnel. After having received a warning in 2023, the site was recommended for in-danger status this year but the decision was postponed until 2026. Among the sites receiving grave warnings in 2024 was the historic city of Budapest, Hungary, three natural sites in Russia including Lake Baikal, one Europe's last primeval forests, Bialowieza of Eastern Poland and Belarus as well as another UK property, Derwent Valley Mills in Derbyshire in Central England - due to construction planned within the 18th-century cotton spinning site.
Katharina Buchholz
Data Journalist
</excerpt>
### Rank 4 of 83 — 0.27
<excerpt title="List of World Heritage in Danger">
# UNESCO World Heritage Centre - List of World Heritage in Danger
World Heritage Convention
*   Help preserve sites now!  
*   Explore UNESCO  
*
English
*   English   
    *   Français
*   Login

*   Our expertisechevron_left Our expertise  About World Heritage News Events The Convention Convention Text Basic Texts Operational Guidelines Policy Compendium Declaration of principles to promote international solidarity and cooperation to preserve World Heritage  Governing Bodies The General Assembly The Committee Resolutions / Decisions Sessions since 1976 The States Parties The Advisory Bodies  Funding World Heritage Fund Financial regulations International Assistance The Emblem Questions and answers  The Centre Employment & Internships Who's Who / Contacts Director of the World Heritage Centre Africa Arab States Asia & Pacific Europe & North America Latin America and the Caribbean      
*   The Listchevron_left The List  Global Strategy Criteria Upstream Process Tentative Lists World Heritage List Nominations  World Heritage List New Inscribed Properties UNESCO Sites Navigator Interactive Map World Heritage in Danger The List in Danger  Reporting & Monitoring State of Conservation Periodic Reporting Questionnaires 2026-2030 Questionnaires 2018-2024 Questionnaires 2008-2015 Reactive Monitoring List of factors affecting the properties  Success Stories Examples of the Convention at work      
*   Activitieschevron_left Activities  Activites  
The World Heritage Centre is at the forefront of the international community’s efforts to protect and preserve.
Browse all activitiesWorld Heritage CanopyHeritage Solutions for Sustainable Futures Browse case studies Featured Activities Indicators Culture|2030 World Heritage Cities Programme Recommendation on the Historic Urban Landscape Cultural Landscapes Capacity Building Category 2 Centres  Natural World Heritage Climate Change and World Heritage World Heritage Marine Programme World Heritage and Biodiversity Corporate sector and the World Heritage ‘no-go’ commitment Reducing Disasters Risks at World Heritage Properties World Heritage and Indigenous Peoples  World Heritage Education Programme World Heritage Volunteers Initiative World Heritage and Sustainable Development Sustainable Tourism Programme World Heritage Programme for Small Island Developing States (SIDS) Initiative on Heritage of Religious Interest
*   Partnerships
chevron_left Partnerships
World Heritage partnerships for conservation
Ensuring that World Heritage sites sustain their outstanding universal value is an increasingly challenging mission in today’s complex world, where sites are vulnerable to the effects of uncontrolled urban development, unsustainable tourism practices, neglect, natural calamities, pollution, political instability, and conflict.
Our PartnersDonate

# UNESCO World Heritage Centre - List of World Heritage in Danger
*   Partnerships  
    *   Marketplace  
    *   Our Partners  
    *   Civil Society  
    *   Donate
*   Publicationschevron_left Publications  Publications Paper Series Urban Notebooks Brochures & Info kits Resource Manuals Other materials Newsletter  Review Wall Map Documents Collections  Resources Search Glossary  About this Website Terms / Policies Syndication Site Map Useful Websites      
*   Search search
World Heritage Convention
close
Search search
Take advantage of the search to browse through the World Heritage Centre information.
World Heritage ListWorld Heritage in DangerList of World Heritage in Danger
Print

# UNESCO World Heritage Centre - List of World Heritage in Danger
###### Share on social media
FacebookTwitter

# UNESCO World Heritage Centre - List of World Heritage in Danger
###### UNESCO social media
FacebookYoutubeTwitterRSS World HeritageTerms / PoliciesSyndication

# List of World Heritage in Danger
The 58 properties which the World Heritage Committee has decided to include on the List of World Heritage in danger in accordance with Article 11(4) of the _Convention_.
Web Browser not supported for ESRI ArcGIS API version 4.10. WebGL must be enable, see documentation
*   Satellite    
*   Gray    
*   Topographic    
*   Dark Background  

*   XY basemap dd ddm dms mgrs usng utm No position
2,000 km
1,000 mi
Earthstar Geographics
Powered by Esri

# List of World Heritage in Danger
##### Afghanistan
*   Cultural Landscape and Archaeological Remains of the Bamiyan Valley (2003)   
*   Minaret and Archaeological Remains of Jam (2002)

# List of World Heritage in Danger
##### Bolivia (Plurinational State of)
*   City of Potosí (2014)

# List of World Heritage in Danger
##### Central African Republic
*   Manovo-Gounda St Floris National Park (1997)
</excerpt>
### Rank 5 of 83 — 0.26
<excerpt title="List of World Heritage in Danger">
As of May 2026, there are 53 sites (14 natural and 39 cultural) on the List of World Heritage in Danger. Arranged by UNESCO regions, 22 of the listed sites are in the Arab States, 12 in Africa, six in Latin America and the Caribbean, six in Asia and the Pacific, and seven in Europe and North America. The majority of the endangered natural sites (nine) are in Africa.[[7]](https://en.wikipedia.org/wiki/List_of_World_Heritage_in_Danger#cite_note-8)[[8]](https://en.wikipedia.org/wiki/List_of_World_Heritage_in_Danger#cite_note-9) The list encompasses sites identified as facing threats to their integrity, which may arise from natural disasters, armed conflict, neglect, pollution, unsustainable tourism, or other hazards. Among these sites, the impacts of armed conflict are evident in countries such as Syria, where several sites, including the Ancient City of Aleppo and the Ancient Villages of Northern Syria, endangered as a result of the Syrian civil war. In Africa, the Democratic Republic of the Congo has multiple listings due to threats such as military conflict and environmental degradation affecting its national parks.[[9]](https://en.wikipedia.org/wiki/List_of_World_Heritage_in_Danger#cite_note-10)
In some cases, inclusion on the danger list has sparked conservation efforts and prompted the release of funds, benefitting sites such as the Galápagos Islands and Yellowstone National Park, both later removed from the List of World Heritage in Danger. Despite this, the list itself and UNESCO's implementation of it have been subject to criticism.[[10]](https://en.wikipedia.org/wiki/List_of_World_Heritage_in_Danger#cite_note-chape-p87-11)[[11]](https://en.wikipedia.org/wiki/List_of_World_Heritage_in_Danger#cite_note-timothy-p83-12) In particular, States Parties and other stakeholders have questioned the authority of the World Heritage Committee to designate a site as in danger without their consent.[[12]](https://en.wikipedia.org/wiki/List_of_World_Heritage_in_Danger#cite_note-iucn-p2-3-13)

Until 1992, when UNESCO set a precedent by placing several sites on the danger list against the wishes of the respective States Parties, such parties would typically submit a programme of corrective measures before a site was listed.[[13]](https://en.wikipedia.org/wiki/List_of_World_Heritage_in_Danger#cite_note-chape-p86-14) Rather than being used solely for its intended purpose, the List of World Heritage in Danger is perceived by some states as a "blacklist" and, according to Christina Cameron, Professor at the School of Architecture and Canada Research Chair on Built Heritage at the University of Montreal, has been used as a political tool to get the attention of States Parties.[[14]](https://en.wikipedia.org/wiki/List_of_World_Heritage_in_Danger#cite_note-thorsell-15)[[15]](https://en.wikipedia.org/wiki/List_of_World_Heritage_in_Danger#cite_note-iucn-p0-16)
The International Union for Conservation of Nature (IUCN) has noted that UNESCO has, in a number of cases, referenced the List of World Heritage in Danger without formally inscribing a site, particularly where threats could be easily addressed by the State Party.[[16]](https://en.wikipedia.org/wiki/List_of_World_Heritage_in_Danger#cite_note-iucn-p18-19-17) The Union has also argued that the prolonged retention of sites on the danger list is questionable and that other mechanisms for conservation should be sought in such cases.[[17]](https://en.wikipedia.org/wiki/List_of_World_Heritage_in_Danger#cite_note-iucn-p19-20-18)
</excerpt>

## Search 4 — query: "natural sites in danger list UNESCO 'Natural' 'Danger'"
### Rank 1 of 57 — 0.45 (passed on)
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
### Rank 2 of 57 — 0.40
<excerpt title="Facing major threats, six new sites join UNESCO's List of World">
The World Heritage Committee has also decided to inscribe on its List of World Heritage in Danger three sites that had been previously recognized; signaling they are now facing serious threats to the values that justified their inscription in the first place. These are: Ancient City of Taurica Chersonese and its Chora (Ukraine), the Historic Inner City of Paramaribo (Suriname) and Tyre (Lebanon).
The three sites that were nominated for inscription on an emergency basis are:
**Boma-Badingilo Migratory Landscape (South Sudan):** A vast expanse of East African savanna, this site hosts the largest known terrestrial mammal migration in the world, and its unique biodiversity makes it an ecosystem of exceptional global significance. The site also reflects the important cultural, and linguistic diversity of the region with several ethnic groups who have been custodians of this landscape through herding, farming and fishing for centuries and even millennia. The Committee has flagged several serious threats, notably infrastructure development, commercial poaching, and wildlife trafficking and trade, which directly affect the large populations of migratory mammals. A context of persistent insecurity, along with limited institutional and financial capacity, also hinders effective conservation of the site.
**Mount Amel Castles (Lebanon):** The five castles that make up this site bear witness to the evolution of defensive systems in the region from the era of the Crusades and Islamic dynasties through to the end of the 19th century. This site, which had already been granted enhanced protection in November 2024 by UNESCO's Committee for the Protection of Cultural Property in the Event of Armed Conflict, is currently suffering heavy damage. According to the Committee, the ongoing conflict directly jeopardizes the site's conservation and requires urgent intervention.

**Sebastia (State of Palestine):**This site preserves the archaeological record of the successive occupation of the site by different civilizations from at least the 9th century BCE, when Samaria-Sebaste served as the capital of the northern Kingdom of Israel, through the Hellenistic, Roman, Byzantine and Islamic periods, with later architectural remains dating to the Crusader era, as well as the Ayyubid/Mamluk and Ottoman periods, when it was one of the designated “Throne Villages”. The main threat facing the site concerns the planned expropriation and creation of the "Samaria" (Shomron) national park, which could divide the property. In addition to the impact of the conflict in the Middle-East, the site also faces pressures related to development, land-use planning, governance and the erosion of the remains.
**Three sites that were already inscribed on the World Heritage List that have now been inscribed on the List of World Heritage in Danger upon the recommendation of the Committee:**
**Ancient City of Tauric Chersonese and its Chora(Ukraine):**The Committee noted with the deepest concern that, due to the Autonomous Republic of Crimea (Ukraine) being temporarily occupied by the Russian Federation, the State Party is unable to ensure the site’s protection or guarantee its conservation or management. In this context, it welcomed the partnership between UNESCO and UNITAR/UNOSAT, which has enabled since 2014, regular monitoring of the state of conservation of the site using satellite images. These observations revealed a significant deterioration in the authenticity and integrity of the property, resulting from new construction and large-scale archaeological excavations. Given the State Party’s inability to fulfill its conservation responsibilities, as well as the observed damage to the property’s Outstanding Universal Value, the Committee decided to inscribe it on the List of World Heritage in Danger. It also called for strengthened international cooperation to prevent the illicit trafficking of cultural property originating from the Autonomous Republic of Crimea (Ukraine).
</excerpt>
### Rank 3 of 57 — 0.37
<excerpt title="Natural World Heritage">
# Natural World Heritage
## A threatened paradise
Natural World Heritage sites account for around 8% of the total surface area covered by all 280,000+ terrestrial and marine protected areas worldwide. Yet they are under increasing pressure. According to IUCN, the official advisory body on nature under the World Heritage Convention, climate change, invasive species and the negative impacts of tourism are currently the three most significant threats. Other major threats include poaching, planned infrastructure such as roads, dams, mining, oil and gas projects, and conflicts.
To date 16 natural World Heritage sites are on the List of World Heritage in Danger. Climate change is however the fastest growing threat to natural World Heritage, with the number of sites highly threatened by climate change almost doubling in the last decade. Every 1°C increase in temperature could double the number of species exposed to dangerous climate conditions. Forests, coral reefs and glaciers are among some of the most affected ecosystems. Wetlands, low-lying deltas, permafrost and fire sensitive ecosystems are also affected.
Almost 2/3 of forests found in World Heritage sites are threatened by land use pressures and climate-related hazards such as wildfires. A first global scientific assessment of greenhouse gas emissions and sequestration in World Heritage forests revealed that at least 10 sites were net carbon sources since 2000 and that one single climate-related hazard could make a forest site from a carbon sink to source.
World Heritage-listed coral reefs, such as theGreat Barrier Reef (Australia)(the world's largest coral reef system), theAldabra Atoll (Seychelles)in the Indian Ocean (the world's second-largest coral atoll) and the Belize Barrier Reef (Belize)in the Atlantic (the largest barrier reef in the northern hemisphere) have been affected by devastating mass coral bleaching events over the past decades. A first global scientific assessment of the impacts of climate change on World Heritage coral reefs revealed that by 2040, all World Heritage-listed coral reefs could face annual severe bleaching events at least twice a decade.

# Natural World Heritage
## A threatened paradise
World Heritage glaciers have been retreating at an accelerated rate since 2000 due to warming temperatures. They are currently losing 58 billion tons of ice every year – equivalent to the combined annual water use of France and Spain– and are responsible for nearly 5% of observed global sea-level rise. Glaciers in a third of the 50 World Heritage glacierized sites are condemned to disappear by 2050, regardless of efforts to limit temperature increases. This includes the last remaining glaciers in Africa such as Mount Kilimanjaro as well as other iconic sites in Europe and North America such as the Dolomites (Italy), Pyrénées – Mont Perdu (France, Spain) and Yosemite National Park (United States of America).
Due to their environmental and social risks, planned infrastructure development projects pose a major threat to World Heritage, with almost a hundred sites being affected by proposed or realised roads (Iguaçu National Park in Brazil), mining, oil and gas projects (Virunga National Park in the Democratic Republic of the Congo). Another important threat is the construction of dams, with more than 50 World Heritage sites reporting potential impacts from water infrastructure projects underway or planned, such as Tanzania's Selous Game Reserve, home to the critically endangered black rhinoceros.
Pressure on natural sites from massive tourism is also increasing. Every year, natural World Heritage sites receive more than 100 million visitors and tourism infrastructure projects have been reported in more than 30 sites, such as Mosi-oa-Tunya / Victoria Falls (Zambia/Zimbabwe), the world’s greatest sheet of falling water, and Volcanoes of Kamchatka (Russian Federation), home to the world's largest known variety of salmonoid fish.
The impacts of invasive species is also among the major threats to natural World Heritage sites and the biodiversity they help protect. With the unfolding impacts of climate change, the problem is likely to get worse. According to the IUCN World Heritage Outlook, more than 100 sites are affected by invasive species, particularly island sites. For instance, in Cuba's Alejandro de Humboldt National Park invasive alien trees are transforming the habitat by growing much faster than native trees. Fish (mostly trout), cats and rodents notably rats are other invasive species threatening natural World Heritage sites such as East Rennell (Solomon Islands).
Previous
Central Africa World Heritage Forest Initiative (CAWHFI)
play_arrow Watch
</excerpt>
### Rank 4 of 57 — 0.36
<excerpt title="List of World Heritage in Danger">
# List of World Heritage in Danger
##### Central African Republic
*   Manovo-Gounda St Floris National Park (1997)

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
### Rank 5 of 57 — 0.35
<excerpt title="Sites In Danger">
Simien National Park (**Ethiopia)**was added to the Danger list in 1996 as rebel armies took control of this region of northern Ethiopia and the park suffered a further influx of people, threatening the habitat of the Simien fox, Walia ibex and other critically endangered endemic wildlife. Although wildlife populations are now recovering well, there is still some way to go in achieving long-term sustainable management for the park and re-establishing viable populations of key species.
Mount Nimba Strict Nature Reserve (**Guinea)**was added to the Danger list in 1992 as a result of the mining threat, as detailed under the entry for this site under Cote D’Ivoire (above)
Rainforests of the Atsinanana (**Madagascar)**were added to the Danger list in 2010 on account of political and civil unrest throughout the country, the withdrawal of much international aid (including funds that were critical to the management of the various separate forests that make up the property), and an escalating problem of illegal timber cutting.
Air and Tenere Natural Reserves (**Niger)**was added to the Danger list in 1992 as the area fell under the control of rebel Tuareg groups and government lost control. Most of the large mammals and other endangered wildlife has subsequently been destroyed.
Niokolo-Koba National Park (**Senegal)**was added to the Danger list in 2007 in response to a pervasive deterioration in management capacity and the decline of large mammal populations as a result of poaching.
Ruins of Kilwa Kisiwani and Ruins of Songo Mnara (**Tanzania)**was added to the Danger list in 2004 as a result of a general deterioration of the structures and lack of capacity to take remedial action.
Tombs of Buganda Kings at Kasubi (**Uganda)**was added to the Danger list in 2010 following its destruction by fire.
Timbuktu and the Tomb of Askia**(Mali)** were added to the Danger list in 2012 following the willfull destruction of some of the ancient mausoleums in Timbuktu by religious extremists seeking to establish their own fundamentalist Islamist state in northern Mali
**African sites previously included on the Danger List**

The Rwenzori Mountains National Park (Uganda) was added to the Danger List in 1999 when a rebel insurgency resulted in loss of management control and closure of the park to visitors. Peace was subsequently restored and the park removed from the Danger List in 2004
Djoudj National Bird Sanctuary (Senegal) was included on the Danger List between 2000 and 2006 on the basis of threats from invasive species of aquatic plant, and problems of salinity and siltation associated with the construction of dams and sluices to control the flow of the Senegal River.
Ichkeul National Park (Tunisia) was included on the Danger List between 1996 and 2006 due to salinity problems resulting from the damming of inflowing rivers. This affected the ecology of the lake severely, reducing the quantity of freshwater plant life and the populations of over-wintering waterfowl. These have never fully recovered.
Ngorongoro Conservation Area (Tanzania) was one of the first sites to be inscribed on the List of World Heritage In Danger, from 1984-89, due to a deterioration in its general ecological condition resulting from poor management.
</excerpt>

## Search 5 — query: "Central Amazon Conservation Complex UNESCO World Heritage in Danger"
### Rank 1 of 83 — 0.73 (passed on)
<excerpt title="Central Amazon Conservation Complex - World Heritage Outlook">
Country
Brazil
Inscribed in
2000
The conservation outlook for this site has been assessed as "good with some concerns" in the latest assessment cycle. Explore the Conservation Outlook Assessment for the site below. You have the option to access the summary, or the detailed assessment.
The Central Amazon Conservation Complex makes up the largest protected area in the Amazon Basin (over 6 million hectares) and is one of the planet’s richest regions in terms of biodiversity. It also includes an important sample of varzea ecosystems, igapó forests, lakes and channels which take the form of a constantly evolving aquatic mosaic that is home to the largest array of electric fish in the world. The site protects key threatened species, including giant arapaima fish, the Amazonian manatee, the black caiman and two species of river dolphin. © UNESCO
*   **Summary**Overview of the site's Conservation Outlook Read more  
*   **Full assessment**The complete Conservation Outlook Assessment for this site, with more details on values, threats, protection and management Read more  
*   **References**The source of information for the Conservation Outlook Assessment See references

## Summary
### 2025 Conservation Outlook
Finalised on
11 Oct 2025
Good with some concerns
Overall, the values of this site remain in good condition, even if showing some localized impacts. Increasing visitation pressure and road expansion, especially caused by the Rio Negro Bridge construction, are increasing pressure over the conservation units comprising this World Heritage site, mainly the Anavilhanas National Park, requiring improvement of infrastructure and better management of tourism in order to contribute to the conservation of these areas. Management effectiveness evaluations of individual conservation units comprising the site show a relatively good level, nonetheless especially human capacity needs strengthening. Main concerns are related to potential impacts caused by climate change, especially wildfires in the broader Amazon Basin, which could result in negative impacts on the site's hydrological and ecological processes and which require a regional approach to data collection, information analysis and management.

## Summary
### Current state and trend of VALUES
Low Concern
Conditions of the values of the site present a low concern and a stable trend without significant changes compared to previous reports. The integration of community in monitoring programs and tourism management is showing positive results in terms of raising awareness and implementing sustainable practices for the recognition and protection of the site's biodiversity values. The resilience of key areas, such as the Jaú River, reflects the continued stability of terrestrial and freshwater ecosystems. While the site continues to support a high diversity of habitats, pressures from climate change, plastic pollution, and resource extraction could pose risks to long-term integrity. However, comprehensive data is lacking to determine trends for some specific values.

## Summary
### Overall THREATS
Low Threat
The Central Amazon Conservation Complex faces persistent and emerging threats that challenge its ecological integrity and resource sustainability, the greatest threat being the increasing occurrence of wildfire, especially in Jaú National Park and around the site. Most other threats are localized including increased human activity driven by road development and the Río Negro Bridge, leading to greater pressure from subsistence agriculture, hunting, fishing, and resource extraction. Tourism growth, particularly unregulated visitation in Anavilhanas National Park and Jaú National Park, continues to outpace management capacity, raising concerns about habitat disturbance, waste disposal, and risks associated with wildlife interactions, including the introduction of non-native species and potential zoonotic diseases. Despite improvements in sustainable fisheries management in Mamirauá and Amanã Sustainable Development Reserves, illegal fishing remains an issue, alongside the overexploitation of wildlife and deforestation linked to small riverside settlements. Potential threats, such as increased visitation and plastic pollution, require further regulation and mitigation, while cargo ship activity in the Anavilhanas archipelago remains a persistent risk due to potential pollution and oil spills. While the impact of past dam constructions on sedimentation and hydrology is likely, the absence of new dam projects reduces immediate concerns.
</excerpt>
### Rank 2 of 83 — 0.72
<excerpt title="Central Amazon -- World Heritage Site">
**Site**: Central Amazon Conservation Complex
**Location**: Brazil
**Year Designated**: 2003
**Category**: Natural
**Criteria**: (ix)(x)
**Reason**: These tropical forests in the heart of the Amazon basin are some of the most biodiverse areas on Earth and home to many species found nowhere else.
* * *
The verdant green forests of the Amazon Basin cover an area larger than Texas. And the largest protected area within this vast and vital ecosystem is the Central Amazon Conservation Complex—a sprawling 23,000-square-mile (6-million-hectare) site that is itself bigger than Switzerland.
The Amazon is one of the most biodiverse places on the entire planet. It's particularly rich in freshwater species—including more than 3,000 different fish species and the world’s largest variety of electric fish. The region is also home to unique and threatened South American species, including the giant arapaima fish, the Amazonian manatee, the black caiman, and two species of river dolphin.
Within the enormous Central Amazon Conservation Complex several distinct, smaller entities house their own unique environments. _Mamirauá_ Reserve’s _várzea_ ecosystem is a landscape of seasonally flooded forests, floodplains, and swamps where the “white water” is actually yellowish in color due to suspended sediments.
Each year the Amazon—which is so large its system contains 20 percent of Earth’s freshwater—and its tributaries rise as much as 30 feet (9 meters) to replenish floodplain soils and nutrients and recharge lakes and ponds. Fish, reptiles, and other aquatic species take advantage of this cyclical occurrence to move into newly flooded areas and exploit their resources until the waters subside. (Some fish, for example, are known to eat fruit from forest trees.)
Jaú National Park’s _igapó_ (blackwater) drainage is a flooded ecosystem of low, thin trees named for the dark color its water acquires from decomposing organic matter.
While the Amazon is famed for these flooded forests, lakes, and channels, the region is also home to dry tropical forests.

But some of those trees are targeted by logging operations, which, along with mining and the conversion of clear lands to ranching or agriculture, constitute serious threats to the long-term future of the Amazon Basin. Although rules are in place to protect the Central Amazon Conservation Complex and other areas from inappropriate uses, they can be extremely difficult to enforce.

## How to Get There
Rivers, not roads, are the transportation hubs in this region, and most of the few visitors to the Central Amazon Conservation Complex arrive by boat, employing everything from canoes to speedboats. Manaus and Tefé are two popular gateway communities for such adventures.

## When to Visit
The Amazon is hot and humid all year, so the main seasonal consideration is rainfall. Rain (and river levels) reach their low ebb in November, then begin to build toward annual maximums in June and July.

## How to Visit
A visit to this area offers a chance to explore a vast wilderness largely untrammeled by tourist infrastructure. Most tourist access is regulated by the government, however, and independent travel can be a challenge. Visitors typically book boat tours and many stay in local ecolodge camps.
</excerpt>
### Rank 3 of 83 — 0.67
<excerpt title="Central Amazon Conservation Complex">
# Central Amazon Conservation Complex | Protected Planet
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

# Central Amazon Conservation Complex
220296  SITE ID
52320.18 km²  Reported Area
Type  Terrestrial and Inland Waters Protected Areas
Location Brazil
Read an assessment of this site by visiting the IUCN World Heritage Outlook Link
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

# Central Amazon Conservation Complex
## Attributes
*   Name Complexe de conservation de l’Amazonie centrale  
*   English Name Central Amazon Conservation Complex  
*   English Designation World Heritage Site (natural or mixed)  
*   IUCN Management Category Not Applicable  
*   Status Inscribed  
*   Type of Designation International  
*   Status Year 2000  
*   Governance Type Not Reported  
*   Governance Subtype Not Applicable  
*   Management Authority Not Reported  
*   Management Plan Not Reported  
*   Ownership Type Not Reported  
*   Ownership Subtype Not Applicable  
*   International Criteria(ix);(x)  
*   Inland Waters Not Reported  
*   Supplementary Information Not Applicable

# Central Amazon Conservation Complex
## Management Effectiveness Evaluations
*   IUCN World Heritage Outlook 2017, 2020, 2025
</excerpt>
### Rank 4 of 83 — 0.53
<excerpt title="Natural World Heritage sites under growing threat, but bright spots remain">
## The outlook
Every few years, the International Union for Conservation of Nature— a global contingent of more than 1,400 government agencies and private organizations focused on environmental conservation—evaluates the environmental and biological conditions at all UNESCO World Heritage sites selected for their natural significance.
That includes the Okavango Delta in Botswana, home to the world’s largest population of African elephants; the Central Amazon Conservation Complex in Brazil; the Socotra Archipelago in Yemen with hundreds of species of birds and fish; the Tropical Rainforest Heritage of Sumatra, Indonesia; the Central Amazon Conservation Complex in Brazil, and Everglades National Park, Florida.
The IUCN reports to UNESCO on each site’s current state and natural value, the threats it faces, the effectiveness of its protection and management, and actions needed to secure its future. The IUCN rates each site’s status from “good” to “critical” as a way of tracking its conservation progress over time.
> One-third of the 50 World Heritage sites that contain glaciers will see those glaciers disappear by 2050, the report projects.
The most recent report—the fourth in a series that began in 2014—was presented at the IUCN World Conservation Congress on Oct. 11, 2025.
Overall, the report documents a decline in the conditions of these remarkable places. The proportion of World Heritage sites with a positive conservation outlook—“good” or “good with some concerns”—has dropped to 57 percent after remaining at 63 percent in 2014, 2017 and 2020. In addition, the proportion of sites considered of “significant concern” or “critical” has increased in the last five years from 37 percent to 43 percent. Many of those are in Mesoamerica, Africa and South America, as well as the Middle East, North Africa and the Mediterranean.
Botswana’s Okavango Delta is one of the world’s last remaining high-biodiversity ecosystems; it’s so vast that it can be seen from space. Photo: Wynand Uys

## Threats from the natural world
The report identifies several key challenges affecting heritage sites. The most widespread conservation challenge the report identifies is climate change.
Climate-related changes in biological conditions such as ocean acidity, salt concentrations, sediment buildup, droughts, flooding and groundwater flow, and variable temperatures are considered “high” or “very high” threats to 117 of the 271 heritage sites evaluated—43 percent of them.
One-third of the 50 World Heritage sites that contain glaciers will see those glaciers disappear by 2050, the report projects.
Around the world, coral reefs have been, and are still, bleaching—turning white as the colorful organisms that build and inhabit them die off—affecting 30 percent of the 29 World Heritage-listed coral reef ecosystems.
In addition, invasive species are encroaching on World Heritage sites. For example, in Ecuador’s Galápagos Islands, invasive species like rats and feral cats are considered one of the main causes of extinctions, including to the islands’ famous birds. In Australia’s Gondwana Rainforest, the last vestiges of an ancient plant and animal ‘living museum’are retreating due to invading non-native species.
News reports in the last week say that a recent surge in ocean temperatures has caused widespread bleaching and death of the world’s warm-water corals. According to scientists, this officially triggers the first climate tipping point for one of our ecosystems. Photo: Ekaterina Zlotnikova
</excerpt>
### Rank 5 of 83 — 0.51
<excerpt title="CENTRAL AMAZON CONSERVATION COMPLEX">
## Brazil
_This immense 4.9 million square hectare complex of tropical rainforest protects one of the most biodiverse regions in the world. In Jaú National Park it includes one of the best examples of a blackwater (igapó) flooded ecosystem. In Mamiraua Reserve it includes one of the best examples of a whitewater (várzea) seasonally flooded forest with undisturbed dry tropical (terra-firme) forest between them. The site protects the largest array of electric fish in the world and key threatened species such as the giant arapaima fish, Amazonian manatee, black caiman and two species of river dolphin. The biodiversity includes examples of speciation accelerated by the extreme conditions which has resulted in a high degree of endemism. The area is a constantly changing mosaic of habitats extensive enough to contain processes such as wind-blows, floods and burns, providing opportunities to study their effect on the biodiversity of natural ecosystems on a large scale._

## Country
* * *
Brazil

## Name
* * *
Central Amazon Conservation Complex

## Natural World Heritage Serial Site
* * *
2000: Jaú National Park inscribed on the World Heritage List under Natural Criteria ix and x:
2003: Mamirauá Sustainable Development Reserve Focal Zone, Amanã Sustainable Development
Reserve and Anavilhanas Ecological Station inscribed on the World Heritage List as extensions
to Jau National Park under Natural Criteria ix and x.
Designation of the remainder of Mamirauá Reserve was deferred and may be included later.

## Statement of Outstanding Universal Value [pending]
* * *
The UNESCO World Heritage Committee issued the following statement at the time of inscription:
**Justification for Inscription**
**Criterion (ix):** The varzea and igapó forests, lakes, rivers, and islands of the proposed site together constitute physical and biological formations and demonstrate ongoing ecological processes in the development of terrestrial and freshwater ecosystems. They include a constantly changing and evolving mosaic of river channels, lakes, and landforms. The floating (and constantly moving and changing) mats of vegetation typical of the varzea watercourses include a significant number of endemic species, including the largest array of electric fishes in the world. Anavilhanas contains the second largest archipelago of river islands in the Brazilian Amazon.
**Criterion (x):** The expanded property substantially increases the already impressive protection offered by Jaú National Park to the biological diversity, habitats, and endangered species found in the Central Amazon region. The area is one of the Endemic Bird Areas of the World, is considered as one of the World Wildlife Fund’s 200 Priority Ecoregion for Conservation, and it is also a Centre of Plant Diversity. The expansion of Jaú National Park to include an important sample of Varzea ecosystems, igapó forests, lakes and channels significantly increases the representation of the aquatic biodiversity of the Central Amazon region. Expansion of the site also enhance the protection of key threatened species including giant arapaima fish, the Amazonian manatee, the black caiman, and two species of river dolphins.

## International Designation
* * *
1993: Mamirauá designated a Wetland of International Importance under the Ramsar Convention (1,124,000 ha).
2001: The Complex designated the core area of the Central Amazon Biosphere Reserve (20,859,987 ha) under the UNESCO Man & Biosphere Programme.

## IUCN Management Categories
* * *
| Jaú National Park: | II National Park |  
| --- | --- |  
| Mamirauá Sustainable Development Reserve: | VI Managed Resource Protected Area |  
| Amanã Sustainable Development Reserve: | V Protected Landscape |  
| Anavilhanas Ecological Station: | Ia Strict Nature Reserve |

## Biogeographical Province
* * *
Amazonian (8.5.1)
</excerpt>

## Search 6 — query: ""Central Amazon Conservation Complex" "in danger""
### Rank 1 of 186 — 0.74 (passed on)
<excerpt title="We Need A Planetary Ethic For The Amazon">
Credits
_Homero Aridjis is a writer, environmentalist and former ambassador to UNESCO._
MEXICO CITY — Governments often invoke national sovereignty as a justification for exploiting and devastating natural resources, asserting that the people will benefit if coal or oil or timber or copper or gold or whatever else is extracted from the Earth. The opposite is usually true: the people affected by the disappearance of their natural environment are often left in a worse state than before.
Who is entitled to sovereignty in the Amazon region? The descendants of peoples who have lived in and off the forest since time immemorial? Or the descendants of the conquerors and despoilers who brutally subjected the local inhabitants to their power? The descendants of these earlier indigenous societies have vested rights — indeed, vested ownership —in the Amazon.
Forty percent of the world’s tropical forests are found in the Amazon region, and perhaps 15 percent of Earth’s biodiversity. Every year the rainforest absorbs 2 billion tons of carbon dioxide from the atmosphere, braking climate change. But in the last 50 years, more than 300,000 of the Amazon’s 1.5 million square miles have been sacrificed to logging, agriculture and cattle ranching, mining, dams and road construction. The area lost is almost the size of Pakistan. And if current trends of deforestation and carbon dioxide emissions continue, by 2050 almost half of the Amazon’s tree species will be threatened with extinction.
_**“Jair Bolsonaro is without a doubt the head of state who poses the greatest danger to the environment.”**_
Partly because of the fires this year in the Amazon, the world is unlikely to reach its goal of limiting global warming to 2 degrees Celsius. This month, Brazil’s National Institute for Space Research reported that there have been 74,000 fires to date in 2019, 80 percent more than the same period last year. In the past month, there were more than 3,500 fires burning on indigenous lands in the Amazon. This is a planetary issue, not just one of sovereign concern to Brazil.

Brazil’s president, Jair Bolsonaro, a former army officer, is without a doubt the head of state who poses the greatest danger to the environment. On July 27, during a ceremony with the military, he declared his intention to exploit the Amazon’s biodiversity and disparaged environmental NGOs. He also criticized what he labels the “indigenous land demarcation industry” practiced by previous administrations. In his zeal to sacrifice the environment to agriculture, Bolsonaro approved the use of hundreds of new pesticides, many of which are banned in the European Union. Five hundred million honeybees died over a three-month period in Brazil this year, a collapse that has been blamed on pesticides.
During a speech I gave at Yale Law School in 1992, I argued that we need an International Court of the Environment — “a tribunal for the prosecution of ecocides, whether they are [perpetrated by] countries, economic entities or individuals.” As the Amazon dwindles before our eyes, if such a court existed today, Bolsonaro would be brought before it as a criminal.
_**“We need an International Court of the Environment, a tribunal for the prosecution of ecocides.”**_
However, in the absence of an international environmental court, he should be brought before the International Criminal Court in the Netherlands on charges of genocide. France, for example, could refer Bolsonaro’s war on Brazil’s indigenous citizens, whose lives and livelihoods are in jeopardy, to the ICC prosecutor, who would take it from there. The process is thorough, detailed and would take years, but the initial referral could be made expeditiously and would shine a spotlight on ongoing threats of genocide, applying pressure now and ultimately setting a cautionary precedent for other heads of government who see themselves as sovereigns of the Amazon region.
On the other hand, little protection is afforded by inclusion of a natural property in UNESCO’s World Heritage List. UNESCO can vote to include properties on a list called World Heritage in Danger to sound an alert that a place is under threat and as an incitement to action. Comprising 6 million acres, the Central Amazon Conservation Complex, a World Heritage Site, is the largest protected area in the Amazon. Will the situation of this vast natural property be debated at the next session of the World Heritage Committee in China next year?

As humans continue to trash the Earth, we need a planetary ethic that will address the question of whether relatively recently delineated political boundaries give governments the moral and ethical right to dispose of the complex masterpieces of nature on which the world depends, and whose disappearance will bring dire consequences extending far beyond artificial national boundaries.
</excerpt>
### Rank 2 of 186 — 0.60
<excerpt title="Central Amazon Conservation Complex - Maps">
# Central Amazon Conservation Complex - Maps - UNESCO World Heritage Centre
*   Partnerships  
    *   Marketplace  
    *   Our Partners  
    *   Civil Society  
    *   Donate
*   Publicationschevron_left Publications  Publications Paper Series Urban Notebooks Brochures & Info kits Resource Manuals Other materials Newsletter  Review Wall Map Documents Collections  Resources Search Glossary  About this Website Terms / Policies Syndication Site Map Useful Websites      
*   Search search
World Heritage Convention
close
Search search
Take advantage of the search to browse through the World Heritage Centre information.
search
tune Filter
By Properties
No value selected.
Use Up and Down arrows to view available values, Enter to select. Use Left and Right arrows to view selected values, Delete key to deselect.
By States Parties
No value selected.
Use Up and Down arrows to view available values, Enter to select. Use Left and Right arrows to view selected values, Delete key to deselect.
By Regions
No value selected.
Use Up and Down arrows to view available values, Enter to select. Use Left and Right arrows to view selected values, Delete key to deselect.
- [x] Danger Site 

- [x] Delisted 

- [x] Transboundary / Transnational
Year Inscribed
Themes
All
Cities
Cultural Landscape
Forest
Marine & coastal
Earthen Architecture
Criteria
with  only with
Cultural Criteria:
- [x]
i- [x]
ii- [x]
iii- [x]
iv- [x]
v- [x]
vi  
 Natural Criteria:
- [x]
vii- [x]
viii- [x]
ix- [x]
x
Keywords
No value selected.
Use Up and Down arrows to view available values, Enter to select. Use Left and Right arrows to view selected values, Delete key to deselect.
Category
- [x] Cultural 

- [x] Natural 

- [x] Mixed
Media
All
With videos
With photo gallery
Display with the brief description
Without
With
Display component parts
Less component parts
All Component parts
Order by
Country
Region
Year
Name of the property
Search
The ListCentral Amazon Conservation Complex
Print

# Central Amazon Conservation Complex - Maps - UNESCO World Heritage Centre
###### Share on social media
FacebookTwitter

# Central Amazon Conservation Complex - Maps - UNESCO World Heritage Centre
###### UNESCO social media
FacebookYoutubeTwitterRSS World HeritageTerms / PoliciesSyndication

# Central Amazon Conservation Complex
*   Description  
*   Maps  
*   Documents  
*   Gallery  
*   Video  
*   Indicators  
*   Assistance

# Central Amazon Conservation Complex
##### Geographical data (2)
Web Browser not supported for ESRI ArcGIS API version 4.10 or higher WebGL must be enable, see documentation
*   Satellite    
*   Base WHC    
*   Topographic    
*   Dark
Powered by Esri
| ID | Name | State Party | Coordinates | Property | Buffer Zone |  
| --- | --- | --- | --- | --- | --- |  
| 998-001 | Jau National Park, Amana Sustainable Development Reserve and Demonstration Area of Mamiraua Sustainable Development Reserve | Brazil | S2 11 41.61 W63 20 59.92 | 4,882,000 ha | — |  
| 998-002 | Anavilhanas Ecological Station | Brazil | S2 22 53.21 W60 47 12.31 | 350,018 ha | — |
Expand Table southDownload (RSS/XML/KML)
</excerpt>
### Rank 3 of 186 — 0.53
<excerpt title="Central Amazon Conservation Complex - Maps">
# Central Amazon Conservation Complex
##### Geographical data (2)
Web Browser not supported for ESRI ArcGIS API version 4.10 or higher WebGL must be enable, see documentation
*   Satellite    
*   Base WHC    
*   Topographic    
*   Dark
Powered by Esri
| ID | Name | State Party | Coordinates | Property | Buffer Zone |  
| --- | --- | --- | --- | --- | --- |  
| 998-001 | Jau National Park, Amana Sustainable Development Reserve and Demonstration Area of Mamiraua Sustainable Development Reserve | Brazil | S2 11 41.61 W63 20 59.92 | 4,882,000 ha | — |  
| 998-002 | Anavilhanas Ecological Station | Brazil | S2 22 53.21 W60 47 12.31 | 350,018 ha | — |
Expand Table southDownload (RSS/XML/KML)

# Central Amazon Conservation Complex
##### Maps
|  | Date | Title |  
| --- | --- | --- |  
|  | 2002 | WORLD NATURAL HERITAGE AND CULTURAL LANDSCAPE HERITAGE SITE-THE CENTRAL AMAZONAN PROTECTED AREAS; Scale: 1: 6 000 000 |
Disclaimer
The Nomination files produced by the States Parties are published by the World Heritage Centre at its website and/or in working documents in order to ensure transparency, access to information and to facilitate the preparations of comparative analysis by other nominating States Parties.
The sole responsibility for the content of each Nomination file lies with the State Party concerned. The publication of the Nomination file, including the maps and names, does not imply the expression of any opinion whatsoever of the World Heritage Committee or of the Secretariat of UNESCO concerning the history or legal status of any country, territory, city or area or of its boundaries.
Committee sessionsStatutory DocumentsCommittee decisions48 th session (2026)47 th session (2025)
General Assembly26 th GA (2027)25 th GA (2025)
About World HeritageThe ConventionConvention TextPolicy CompendiumDeclaration of principlesOperational GuidelinesThe EmblemThe States PartiesThe Advisory BodiesThe CentreEmployment & InternshipsWho's Who
The ListWorld Heritage ListWorld Heritage in DangerNew InscriptionsCriteria for SelectionTentative ListsWorld Heritage List Nominations
Reporting & MonitoringState of Conservation (SOC)Periodic ReportingQuestionnaires 2018-2024Questionnaires 2008-2015Reactive MonitoringAfricaArab StatesAsia & PacificLatin America and the CaribbeanEurope and North America
PartnershipsBecome a PartnerWhat Partners DoOur Partners
ActivitiesAll our activitiesVolunteer
PublicationsWorld Heritage ReviewSeriesResource ManualsWorld Heritage wall mapMore publications ...
FundingWorld Heritage FundInternational Assistance
MoreContactsSite MapBecome a memberDonate Now!
UNESCOUNESCO Latest NewsTake ActionIdeas & DataOur ImpactOur expertiseCore Data PortalSubscribe to our newsletters
Terms of useTerms of UseUNESCO Name & LogoUNESCO FAQReport fraud, abuse, misconductScam alert
PoliciesProtection of human rights (Procedure 104)Access to InformationWebsite Privacy NoticeEvents Privacy NoticeData Protection and PrivacyEnvironmental and Social Policies
Follow us

# Central Amazon Conservation Complex
##### Maps
FacebookInstagramTwitterYoutubeLinkedinSyndication RSS
1.   UNESCO  
2.   Culture  
3.   World Heritage Centre  
4.   The List  
5.   World Heritage List
© UNESCO World Heritage Centre 1992-2026
top
×

# Central Amazon Conservation Complex
##### You don't have your Password or Username
Please enter your **email**. You will receive a message with the process to get your password.
Search
×

# Central Amazon Conservation Complex
##### Login
Please enter your username Your password
- [x] remember my profile
Forgot your username or password?Become a member
Previous Next Login
</excerpt>
### Rank 4 of 186 — 0.49
<excerpt title="For 54 years, the WorldHeritage Convention has brought together ...">
*      
*
•
Follow
* * *
For 54 years, the #WorldHeritage Convention has brought together 196 nations, heritage professionals, local communities, Indigenous peoples and partners around a shared vision: safeguarding the cultural and natural heritage that reflects our collective history, diversity and creativity.  
Through international cooperation, it has provided a unique framework for identifying, protecting and promoting heritage of Outstanding Universal Value across the globe. Today, the World Heritage List includes 1,273 properties in 173 countries: 991 cultural, 240 natural and 42 mixed sites, illustrating both the remarkable richness of our planet and the enduring relevance of the Convention.
As we mark this anniversary, let us take this opportunity to renew our commitment to ensuring that this heritage continues to be protected, valued and transmitted to future generations.
1. Morocco - Ksar of Ait-Ben-Haddou © Olena Tur

2. Sierra Leone - Gola-Tiwai Complex © RSPB

3. Palau - Rock Islands Southern Lagoon © Ko Hon Chiu Vincent

4. Czechia - Historic Centre of Prague © Limes.Media/Tim Schnarr

5. Brazil - Central Amazon Conservation Complex© Our Place the World Heritage Collection

6. Lebanon - Baalbek © Limes.Media/Tim Schnarr

7. China - Hubei Shennongjia © Institute of Botany, The Chinese Academy of Science

8. Kenya - The Historic Town and Archaeological Site of Gedi © National Museums of Kenya

9. Montenegro - Durmitor National Park© Tim Schnarr/Limes.Media

10. Nicaragua - León Cathedral © Ko Hon Chiu Vincent
#UNESCO

## No comments yet.
Start the conversation.
30
</excerpt>
### Rank 5 of 186 — 0.32
<excerpt title="Central Amazon Conservation Complex">
**EXPLORE BRAZIL’S CENTRAL AMAZON CONSERVATION COMPLEX with this slideshow, check the location map and get all the facts and information below.**
Central Amazon Conservation Complex
Central Amazon Conservation Complex
For slideshow description see right or scroll down (mobile). Click to view slideshow
**Location and Values:** Brazil’s Central Amazon Conservation Complex is one of the world’s largest conservation areas, protecting a massive 53,000 km 2 of the central Amazon rainforest and its exceptional biodiversity. It includes vast areas of seasonally-flooded ‘varzea’ and ‘igapo’ forests and a constantly evolving mosaic of river channels, lakes and landforms.
**Conservation Status and Prospects.** According to IUCN’s recent Conservation Outlook Assessment the conservation status of this site is ‘good with some concerns’. The IUCN report notes that ‘overall, the conservation values of this very large property are in good condition, with only minor human impacts around settled areas. While local riverside communities engage in subsistence agriculture, hunting, fishing, and extraction of timber and non-timber forest products human population density remains low and impacts are limited to narrow bands of higher land on natural levees along stream courses. Overall, protection and management of the conservation complex is quite effective. Despite the currently very good state of conservation, the expected consequences of anticipated climate change and potentially increasing pressures due to urban expansion and better access (provided for example by a recently constructed bridge) give rise to some concerns.’
**Links:**
Google Earth
Official UNESCO Site Details
IUCN Conservation Outlook
UNEP-WCMC Site Description
Birdlife IBA

The photos in this slideshow are intended to ‘tell the story’ of Brazil’s Central Amazon Conservation Complex, showing the area’s flooded forest landscapes, plants and animals, people, threats and conservation needs. It includes recent photographs from a river trip up the Rio Negro from Manaus, through the Anavilhas archipelago and into Jau National Park, with photos of many of the area’s unusual birds and mammals. These include pink river dolphins, Linnaeus’s two-toed sloth, Amazonian manatee, woolly monkey, white-bellied and black-faced spider monkeys, various species of river turtles, birds such as the red-billed and Toco toucan and festive Amazon parrot and a selection of the region’s incredible diversity of fishes. This page of the website is still under development and a more detailed description of the various aspects of the site which are illustrated in the slideshow will be included in due course – so please come back again soon!

### Factfile
**Website Category:**Tropical & Sub-tropical Forests
**Area:** 53,230 km 2
**Inscribed:** 2000 (Extension 2003)
**Criteria:**
*   Ecological processes (ix);  
*   Natural habitat for biodiversity (x);  
*   Significant number of rare, endemic and/or endangered species (x)

### Share this page
</excerpt>

## Search 7 — query: "Brazil natural world heritage in danger site"
### Rank 1 of 78 — 0.55 (passed on)
<excerpt title="List of World Heritage Sites in Brazil">
# List of World Heritage Sites in Brazil
## World Heritage Sites
| Sanctuary of Bom Jesus de Matosinhos |  | Minas Gerais | 1985 | 334; i, iv (cultural) | The sanctuary complex represents the apex of Christian art in Latin America. The church, which is from the second half of the 18th century, is in the Baroque style with the interior in the Italian-inspired Rococo style. The church is approached by the path passing seven chapels with polychrome sculptures depicting the Stations of the Cross by the sculptor Aleijadinho. The outdoor stairway is decorated by soapstonesculptures of twelve prophets, also by Aleijadinho.[[12]](https://en.wikipedia.org/wiki/List_of_World_Heritage_Sites_in_Brazil#cite_note-12) |  
| Iguaçu National Park |  | Paraná | 1986 | 355; vii, x (natural) | Iguazu Falls on the eponymous river span over 2,700 m (8,900 ft) and have a vertical drop of 80 m (260 ft). They are located on the border of Brazil and Argentina, where the area is protected as a separate World Heritage Site, the Iguazú National Park. The surrounding area comprises the Paranese subtropical rainforest, a part of the Atlantic Forest. The forest is rich in biodiversity and is home to large animals such as the tapir, giant anteater, giant otter, ocelot, jaguar, and jaguarundi. From 1999 to 2001, the site was listed as endangered due to an illegally opened road through the park, dams on the river, and helicopter flights.[[13]](https://en.wikipedia.org/wiki/List_of_World_Heritage_Sites_in_Brazil#cite_note-13)[[14]](https://en.wikipedia.org/wiki/List_of_World_Heritage_Sites_in_Brazil#cite_note-14)[[5]](https://en.wikipedia.org/wiki/List_of_World_Heritage_Sites_in_Brazil#cite_note-Igua%C3%A7u-5) |  

# List of World Heritage Sites in Brazil
## World Heritage Sites
| Brasília |  | Federal District | 1987 | 445; i, iv (cultural) | As a part of his modernization project, President Juscelino Kubitschek decided to move the national capital to the newly established city of Brasília. The city was designed by the architects Lúcio Costa and Oscar Niemeyer and constructed between 1956 and 1960. The city plan follows the concepts of modernist architecture, as promoted by Le Corbusier, on a large scale, and adjusted to a setting in a tropical climate. Some of the important buildings include the Cathedral of Brasília (pictured), the National Congress Palace, and the Cláudio Santoro National Theater.[[15]](https://en.wikipedia.org/wiki/List_of_World_Heritage_Sites_in_Brazil#cite_note-15) |  
| Serra da Capivara National Park |  | Piauí | 1991 | 606; iii (cultural) | The area of the national park has been inhabited for millennia and is one of the oldest archaeological sites in the Americas. There are over 300 sites with rock paintings (example pictured), some of which have been dated to be more than 25,000 years old. The age of these paintings revolutionized the classical theories of initial peopling of the Americas through Beringia. Excavations uncovered initial presence of hunter-gatherer societies and later ceramic-farmer societies.[[16]](https://en.wikipedia.org/wiki/List_of_World_Heritage_Sites_in_Brazil#cite_note-16) |
</excerpt>
### Rank 2 of 78 — 0.52
<excerpt title="Natural World Heritage sites under growing threat, but bright spots remain">
## The outlook
Every few years, the International Union for Conservation of Nature— a global contingent of more than 1,400 government agencies and private organizations focused on environmental conservation—evaluates the environmental and biological conditions at all UNESCO World Heritage sites selected for their natural significance.
That includes the Okavango Delta in Botswana, home to the world’s largest population of African elephants; the Central Amazon Conservation Complex in Brazil; the Socotra Archipelago in Yemen with hundreds of species of birds and fish; the Tropical Rainforest Heritage of Sumatra, Indonesia; the Central Amazon Conservation Complex in Brazil, and Everglades National Park, Florida.
The IUCN reports to UNESCO on each site’s current state and natural value, the threats it faces, the effectiveness of its protection and management, and actions needed to secure its future. The IUCN rates each site’s status from “good” to “critical” as a way of tracking its conservation progress over time.
> One-third of the 50 World Heritage sites that contain glaciers will see those glaciers disappear by 2050, the report projects.
The most recent report—the fourth in a series that began in 2014—was presented at the IUCN World Conservation Congress on Oct. 11, 2025.
Overall, the report documents a decline in the conditions of these remarkable places. The proportion of World Heritage sites with a positive conservation outlook—“good” or “good with some concerns”—has dropped to 57 percent after remaining at 63 percent in 2014, 2017 and 2020. In addition, the proportion of sites considered of “significant concern” or “critical” has increased in the last five years from 37 percent to 43 percent. Many of those are in Mesoamerica, Africa and South America, as well as the Middle East, North Africa and the Mediterranean.
Botswana’s Okavango Delta is one of the world’s last remaining high-biodiversity ecosystems; it’s so vast that it can be seen from space. Photo: Wynand Uys

## Threats from the natural world
The report identifies several key challenges affecting heritage sites. The most widespread conservation challenge the report identifies is climate change.
Climate-related changes in biological conditions such as ocean acidity, salt concentrations, sediment buildup, droughts, flooding and groundwater flow, and variable temperatures are considered “high” or “very high” threats to 117 of the 271 heritage sites evaluated—43 percent of them.
One-third of the 50 World Heritage sites that contain glaciers will see those glaciers disappear by 2050, the report projects.
Around the world, coral reefs have been, and are still, bleaching—turning white as the colorful organisms that build and inhabit them die off—affecting 30 percent of the 29 World Heritage-listed coral reef ecosystems.
In addition, invasive species are encroaching on World Heritage sites. For example, in Ecuador’s Galápagos Islands, invasive species like rats and feral cats are considered one of the main causes of extinctions, including to the islands’ famous birds. In Australia’s Gondwana Rainforest, the last vestiges of an ancient plant and animal ‘living museum’are retreating due to invading non-native species.
News reports in the last week say that a recent surge in ocean temperatures has caused widespread bleaching and death of the world’s warm-water corals. According to scientists, this officially triggers the first climate tipping point for one of our ecosystems. Photo: Ekaterina Zlotnikova
</excerpt>
### Rank 3 of 78 — 0.47
<excerpt title="Natural World Heritage sites under growing threat, but bright spots remain">
Jessica Beaudette
October 22, 2025
**Of the world’s 271 UNESCO World Heritage sites that are recognized at least in part for their natural features, many are under pressure from climate change, invasive species and underfunding. But it’s not all bad, and there’s reason to feel hopeful too.**
Botswana’s fertile Okavango Delta is one of the last remaining high-biodiversity ecosystems in the world, home to cheetahs, African wild dogs, baobab trees, crocodiles, termites and owls that catch fish. Roughly the size of the state of Connecticut, the freshwater Okavango Delta opens into an enormous alluvial fan that stretches up to 5,800 square miles (15,000 square kilometers) into the Kalahari Desert. The area is so vast it can be seen from space, but most people have never heard of it.
In recognition of its natural and cultural significance, the Okavango Delta was designated a UNESCO World Heritage Site in 2014. When I conducted research in the Okavango in 2024, I witnessed both its natural beauty and the ebullient warmth of the people who live there.
The health of the delta—and of 270 other natural sites across the globe—is the subject of the latest IUCN World Heritage Outlook, a recurring wellness report on the planet’s most treasured natural places. The report’s findings are not dire, but they aren’t great, either. Many of these extraordinary places are increasingly at risk due to escalating climate change, invasive species, and a lack of consistent funding to protect them.

## The outlook
Every few years, the International Union for Conservation of Nature— a global contingent of more than 1,400 government agencies and private organizations focused on environmental conservation—evaluates the environmental and biological conditions at all UNESCO World Heritage sites selected for their natural significance.
That includes the Okavango Delta in Botswana, home to the world’s largest population of African elephants; the Central Amazon Conservation Complex in Brazil; the Socotra Archipelago in Yemen with hundreds of species of birds and fish; the Tropical Rainforest Heritage of Sumatra, Indonesia; the Central Amazon Conservation Complex in Brazil, and Everglades National Park, Florida.
The IUCN reports to UNESCO on each site’s current state and natural value, the threats it faces, the effectiveness of its protection and management, and actions needed to secure its future. The IUCN rates each site’s status from “good” to “critical” as a way of tracking its conservation progress over time.
> One-third of the 50 World Heritage sites that contain glaciers will see those glaciers disappear by 2050, the report projects.
The most recent report—the fourth in a series that began in 2014—was presented at the IUCN World Conservation Congress on Oct. 11, 2025.
Overall, the report documents a decline in the conditions of these remarkable places. The proportion of World Heritage sites with a positive conservation outlook—“good” or “good with some concerns”—has dropped to 57 percent after remaining at 63 percent in 2014, 2017 and 2020. In addition, the proportion of sites considered of “significant concern” or “critical” has increased in the last five years from 37 percent to 43 percent. Many of those are in Mesoamerica, Africa and South America, as well as the Middle East, North Africa and the Mediterranean.
Botswana’s Okavango Delta is one of the world’s last remaining high-biodiversity ecosystems; it’s so vast that it can be seen from space. Photo: Wynand Uys
</excerpt>
### Rank 4 of 78 — 0.45
<excerpt title="List of World Heritage Sites in Brazil">
# List of World Heritage Sites in Brazil - Wikipedia
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

# List of World Heritage Sites in Brazil - Wikipedia
## Contents
move to sidebar hide
*   (Top)  
*   1 World Heritage Sites

*   2 Tentative list

*   3 See also

*   4 References
- [x] Toggle the table of contents

# List of World Heritage Sites in Brazil
- [x] 30 languages
*   Беларуская  
*   Deutsch  
*   Español  
*   فارسی  
*   Français  
*   Galego  
*   हिन्दी  
*   Hrvatski  
*   Magyar  
*   Italiano  
*   日本語  
*   ქართული  
*   Қазақша  
*   한국어  
*   Latviešu  
*   मैथिली  
*   മലയാളം  
*   Malti  
*   नेपाली  
*   Polski  
*   Português  
*   Русский  
*   Slovenščina  
*   Српски / srpski  
*   ไทย  
*   Татарча / tatarça  
*   Українська  
*   Tiếng Việt  
*   მარგალური  
*   中文
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
Atlantic Forest
Brasília
Brazilian Atlantic Islands
Jaú
Amanã
Anavilhanas
Mamirauá
Chapada dos Veadeiros
Emas
Discovery Coast
Salvador
São Luís
Diamantina
Goiás
Olinda
Ouro Preto
Iguaçu
São Miguel das Missões
Pampulha
Pantanal
Paraty
Rio de Janeiro
Congonhas
São Francisco Square
Serra da Capivara
Lençóis Maranhenses
Cavernas do Peruaçu
Teatro Amazonas
Teatro da Paz
</excerpt>
### Rank 5 of 78 — 0.44
<excerpt title="Urgent alert on human rights threats due to Pantanal degradation">
The Pantanal is the world’s largest freshwater wetland. It’s nearly 18 million hectares stretch across Brazil, Bolivia, and Paraguay, making a home for thousands of species, some of which are in danger of extinction. It hosts six different Ramsar sites, wetlands of international importance, and has been designated as a Biosphere Reserve and UNESCO World Heritage Site.
Forest fires, drought, and deforestation, due largely to the expansion of industrial agriculture and the construction of hydroelectric dams, have destroyed millions of hectares of this wetland. The devastation is not only environmental, but it has also affected the lives of those who inhabit the region, threatening their right to live in a healthy environment.
In addition, the Pantanal provides resources and sustains the livelihoods of about 1.5 million people. More than 270 communities—including indigenous peoples, cattle ranchers and riparian communities—depend directly or indirectly on the wetland, although its relevance transcends the region and is fundamental to the well-being of more than 10 million people.
However, the Pantanal is at risk of collapse. Only 5 percent of its area is protected. In recent years, forest fires, drought and deforestation—associated with the expansion of agribusiness and the construction of dams—have destroyed millions of hectares of this wetland. This damage violates the rights of local people and communities.

## **Environmental Damage and Human Rights**
The intensification of extractive activities during recent years, principally ranching and industrial agriculture, have led to unprecedented droughts and fires in the Pantanal.
In 2020, wildfires destroyed more than 4.5 million hectares, almost one-third of the wetland’s area. And so far in 2022, more than 123 thousand hectares have been consumed by fires, 26 percent more than had burned during the same time period in 2021. In addition to the fires, drought has been intensifying.
One of the most serious cases is that of the Guató people of Baía dos Guató, Brazil, who have lost almost 90 percent of their territory to fire.
"The fires destroyed crops, burned houses. The fire destroyed a large part of our territory, destroying many trees, animals, birds, damaging our animals and plants and our food security, because it destroyed our crops," said one of its members. "Everything is coming to an end."
Fires in the Pantanal have caused the loss of forests and biodiversity, aggravating the climate crisis. They also impact the health and livelihoods of nearby communities by destroying their homes and territories, making them more susceptible to health problems, especially respiratory problems. Fires have resulted in the loss of seeds and the death of animals.
The drought especially impacts communities that depend on fishing for food and income (about 70 percent of Pantanal villagers depend on fishing as their main livelihood). Women engaged in artisanal bait collection for sport fishing have been particularly affected.
The traditional communities in the region have also been severely impacted, as the fire has reached all of their territories, destroying almost half of them.
This has repercussions on the development of their cultural practices, as for many Pantanal communities the connection with the land plays an essential role. They obtain from nature the plants for their traditional medicines and raw materials to build their houses, utensils and handicrafts.
For the Yshir, for example, the destruction of the Pantanal threatens their belief system and cosmology (where the forest, rivers and wildlife are central), preventing them from maintaining their traditional ceremonies based on these beliefs.

## **An Emergency Call**
The Interamerican Association for Environmental Defense (AIDA) and Ecologia e Ação (ECOA) prepared an urgent alert for United Nations Human Rights Rapporteurs to report on the critical situation of the Pantanal and request that they issue recommendations to the three countries where the wetland is located in order to prevent the recurrence of fires, ensure the restoration of ecosystems and guarantee the rights of local populations.
We also ask them to visit the site to learn about its situation first hand and to give their recommendations a greater force and sense of urgency.
The biological wealth of the Pantanal is incalculable. The site provides several ecosystem services: flood flow regulation, climate regulation, soil fertility control, biological control, biodiversity maintenance and is a source of water, food and raw materials for the population.
The environmental and social importance of the Pantanal requires urgent, coordinated, transboundary and effective actions to ensure its restoration and protection.
It is time to join forces and take care of the enormous natural and cultural wealth of this biome that is so important for life.
</excerpt>

## Search 8 — query: ""List of World Heritage in Danger" Brazil natural"
### Rank 1 of 314 — 0.68 (passed on)
<excerpt title="List of World Heritage Sites in South America">
# List of World Heritage Sites in South America
## World Heritage Sites
| Humberstone and Santa Laura Saltpeter Works |  | ChileTarapacá, Chile 20°12′30″S 69°47′40″W / 20.20833°S 69.79444°W / -20.20833; -69.79444 (Humberstone and Santa Laura Saltpeter Works) | Cultural: (ii), (iii), (iv) | — | 2005 | Situated in the Atacama Desert, the two saltpeter works are representative of the saltpeter industry that flourished in northern Chile in the 19th and early 20th century and brought together people from different parts of South America and Europe creating a unique culture with its own language and customs. The site was listed as endangered from 2005 to 2019 due to damage, vandalism, looting and the general fragile nature of the structures as a result of a 40 years' lack of maintenance. | [[59]](https://en.wikipedia.org/wiki/List_of_World_Heritage_Sites_in_South_America#cite_note-63)[[60]](https://en.wikipedia.org/wiki/List_of_World_Heritage_Sites_in_South_America#cite_note-29-sess-p142-143-64)[[61]](https://en.wikipedia.org/wiki/List_of_World_Heritage_Sites_in_South_America#cite_note-65) |  

# List of World Heritage Sites in South America
## World Heritage Sites
| Iguaçu National Park |  | BrazilParaná, Brazil 25°41′S 54°26′W / 25.683°S 54.433°W / -25.683; -54.433 (Iguaçu National Park) | Natural: (vii), (x) | 170,086 (420,290) | 1986 | Together with Iguazú National Park on the Argentinian side, the park protects Iguazu Falls, one of the world's largest waterfalls, and is home to many rare and endangered species such as giant anteater or the giant otter. The site had been listed as endangered 1999–2001 due to an illegally opened road through the park, dams on the Iguazu River and helicopter flights. | [[62]](https://en.wikipedia.org/wiki/List_of_World_Heritage_Sites_in_South_America#cite_note-66) |  
| Iguazú National Park |  | ArgentinaMisiones Province, Mesopotamia Argentina 25°31′5″S 54°8′0″W / 25.51806°S 54.13333°W / -25.51806; -54.13333 (Iguazú National Park) | Natural: (vii), (x) | 55,000 (140,000) | 1984 | Together with Iguaçu National Park on the Brazilian side, the park protects Iguazu Falls, one of the world's largest waterfalls. Its subtropical rainforest is home to more than 2000 species of vascular plants and large mammals such as tapirs, giant anteaters, howler monkeys, ocelots and jaguars. | [[63]](https://en.wikipedia.org/wiki/List_of_World_Heritage_Sites_in_South_America#cite_note-67) |
</excerpt>
### Rank 2 of 314 — 0.64
<excerpt title="World Heritage Committee Adds Four Sites to the List of World Heritage in ...">
**Marrakesh - UNESCO's World Heritage Committee, meeting in Marrakech (Morocco) since November 29, has today included four new sites on its List of World Heritage in Danger.**
They are the Iguacu National Park (Brazil), the Rwenzori Mountains (Uganda), the Salonga National Park (Democratic Republic of the Congo) and the Groups of Monuments at Hampi (India).
The inclusion of the **Iguacu National Park** on the List of World Heritage in Danger follows a mission carried out at the site in March 1999. The illegal opening, by local people, of a road cutting the park in two, and affecting the values for whch the site was inscribed in the World Heritage List was the main cause of concern. The Committee recognized the efforts made by the State Party to implement the recommendations of the mission. However, in the absence of satisfactory progress with regard to the permanent closing of the road and the implementation of the recovery plan, the Committee decided to include Iguacu National Park in the List of World Heritage in Danger.
Regarding the **Rwenzori Mountains**, the Committee stressed that the security situation - rebels having occupied the site since 1997 - has prevented any conservation activity worthy of the name. It called on the World Heritage Centre and the World Conservation Union (IUCN), which work in close co-operation with the Ugandan body responsible for wildlife preservation, to consult non- governmental conservation organisations and other international organisations present in the region to discuss ways of making all the parties involved in the conflict aware of the need to respect the site's world heritage status and to develop projects to support site management.
**Salonga National Park** was the only site, out of five in the Democratic Republic of the Congo, not yet included on the List of World Heritage in Danger. Given its location in the centre of the country, it was less affected by on-going armed conflict. Poaching and housing construction, however, have threatened the site's integrity and inclusion on the List will enable Salonga - along with the four other sites in the DRC - to gain from a UNESCO project, financed largely by the United Nations Foundation, aimed at providing assistance - a sum of 4.1 million dollars - for personnel training and equipment as well as bio-diversity conservation.

The inclusion of **the Groups of Monuments at Hampi** has been prompted by the construction of two suspension bridges which dominate the natural environment and threaten the World Heritage site's integrity. The construction of a road towards one of the bridges will result in a major increase in heavy goods traffic and has already resulted in the dismantling and reconstruction of an important historic monument - a mandapa (a pillared stone rest-house) within the borders of the site. This dislocation signifies serious problems in the implementation of cultural heritage policies and regulations.
The List of World Heritage in Danger now numbers 27 sites around the world. They include natural reserves and historic monuments such as Angkor (Cambodia), the Everglades and Yellowstone national parks (United States), and Timbuktu (Mali). The List also includes the four other sites in the Democratic Republic of Congo: the Garamba, Virunga, Kahuzi-Biega National Parks and the Okapi Wildlife Reserve.
The List of endangered sites is designed to attract the attention of world leaders and focus public opinion on the need to preserve cultural or natural sites of universal value that are particularly threatened by natural causes or by human intervention. The List is revised annually at the meeting of UNESCO's World Heritage Committee, which this year is taking place in Morocco - from November 29 to December 4. The Committee will announce new sites to be included in the World Heritage List tomorrow, December 1
</excerpt>
### Rank 3 of 314 — 0.59
<excerpt title="List of World Heritage Sites in South America">
# List of World Heritage Sites in South America
## World Heritage Sites
| Cueva de las Manos, Río Pinturas |  | ArgentinaSanta Cruz Province, Argentina 47°9′0″S 70°40′0″W / 47.15000°S 70.66667°W / -47.15000; -70.66667 (Cueva de las Manos, Río Pinturas) | Cultural: (iii) | — | 1999 | Named for the paintings of hands, the cave contains rock art from between 13,000 and 9,500 years ago that bear witness to the earliest human inhabitants in South America. | [[32]](https://en.wikipedia.org/wiki/List_of_World_Heritage_Sites_in_South_America#cite_note-34) |  
| Discovery Coast Atlantic Forest Reserves |  | Brazil Atlantic Coast, Bahia and Espírito Santo states, Brazil 16°30′S 39°15′W / 16.500°S 39.250°W / -16.500; -39.250 (Discovery Coast Atlantic Forest Reserves) | Natural: (ix), (x) | 111,930 (276,600) | 1999 | The site comprises some of the last remaining Atlantic Forests and shows a very high diversity with many rare and endemic species. As such it is of high interest both for scientists and for conservation. | [[33]](https://en.wikipedia.org/wiki/List_of_World_Heritage_Sites_in_South_America#cite_note-35) |  

# List of World Heritage Sites in South America
## World Heritage Sites
| ESMA Museum and Site of Memory – Former Clandestine Centre of Detention, Torture and Extermination |  | Buenos Aires, Argentina34°32′18.24″S 58°27′48.96″W / 34.5384000°S 58.4636000°W / -34.5384000; -58.4636000 (ESMA Museum and Site of Memory – Former Clandestine Centre of Detention, Torture and Extermination) | Cultural: (vi) | 0.907 (2.24); buffer zone 16.77 (41.4) | 2023 |  | [[34]](https://en.wikipedia.org/wiki/List_of_World_Heritage_Sites_in_South_America#cite_note-36) |  
| Fray Bentos Cultural-Industrial Landscape |  | UruguayRío Negro Department, Uruguay 33°07′04″S 58°19′54″W / 33.117778°S 58.331667°W / -33.117778; -58.331667 (Fray Bentos Cultural-Industrial Landscape) | Cultural: (ii), (iv) | 274 (680); buffer zone 2,128 (5,260) | 2015 |  | [[35]](https://en.wikipedia.org/wiki/List_of_World_Heritage_Sites_in_South_America#cite_note-37) |
</excerpt>
### Rank 4 of 314 — 0.57
<excerpt title="World Heritage Sites by Country 2026">
Natural	No	Ancient and Primeval Beech Forests of the Carpathians and Other Regions of Europe *  
Cultural	No	Mehmed Paša Sokolović Bridge in Višegrad  
Cultural	No	Old Bridge Area of the Old City of Mostar  
Cultural	No	Stećci Medieval Tombstone Graveyards *  
Natural	No	Vjetrenica Cave, Ravno  
Botswana  
TYPE
ENDANGERED
NAME
Natural	No	Okavango Delta  
Cultural	No	Tsodilo  
Brazil  
TYPE
ENDANGERED
NAME
Natural	No	Atlantic Forest South-East Reserves  
Cultural	No	Brasilia  
Natural	No	Brazilian Atlantic Islands: Fernando de Noronha and Atol das Rocas Reserves  
Natural	No	Central Amazon Conservation Complex (Extension of "Jaú National Park")  
Natural	No	Cerrado Protected Areas: Chapada dos Veadeiros and Emas National Parks  
Natural	No	Discovery Coast Atlantic Forest Reserves  
Cultural	No	Historic Centre of Salvador de Bahia  
Cultural	No	Historic Centre of São Luís  
Cultural	No	Historic Centre of the Town of Diamantina  
Cultural	No	Historic Centre of the Town of Goiás  
Cultural	No	Historic Centre of the Town of Olinda  
Cultural	No	Historic Town of Ouro Preto  
Natural	No	Iguaçu National Park  
Cultural	No	Jesuit Missions of the Guaranis: San Ignacio Mini, Santa Ana, Nuestra Señora de Loreto and Santa Maria Mayor (Argentina), Ruins of Sao Miguel das Missoes (Brazil) *  
Natural	No	Lençóis Maranhenses National Park  
Cultural	No	Pampulha Modern Ensemble  
Natural	No	Pantanal Conservation Area  
Mixed	No	Paraty and Ilha Grande – Culture and Biodiversity  
Cultural	No	Rio de Janeiro: Carioca Landscapes between the Mountain and the Sea  
Cultural	No	Sanctuary of Bom Jesus do Congonhas  
Cultural	No	São Francisco Square in the Town of São Cristóvão  
Cultural	No	Serra da Capivara National Park  
Cultural	No	Sítio Roberto Burle Marx  
Cultural	No	Valongo Wharf Archaeological Site  
Bulgaria  
TYPE
ENDANGERED
NAME
</excerpt>
### Rank 5 of 314 — 0.56
<excerpt title="List of World Heritage Sites in South America">
# List of World Heritage Sites in South America
## World Heritage Sites
| Iguaçu National Park |  | BrazilParaná, Brazil 25°41′S 54°26′W / 25.683°S 54.433°W / -25.683; -54.433 (Iguaçu National Park) | Natural: (vii), (x) | 170,086 (420,290) | 1986 | Together with Iguazú National Park on the Argentinian side, the park protects Iguazu Falls, one of the world's largest waterfalls, and is home to many rare and endangered species such as giant anteater or the giant otter. The site had been listed as endangered 1999–2001 due to an illegally opened road through the park, dams on the Iguazu River and helicopter flights. | [[62]](https://en.wikipedia.org/wiki/List_of_World_Heritage_Sites_in_South_America#cite_note-66) |  
| Iguazú National Park |  | ArgentinaMisiones Province, Mesopotamia Argentina 25°31′5″S 54°8′0″W / 25.51806°S 54.13333°W / -25.51806; -54.13333 (Iguazú National Park) | Natural: (vii), (x) | 55,000 (140,000) | 1984 | Together with Iguaçu National Park on the Brazilian side, the park protects Iguazu Falls, one of the world's largest waterfalls. Its subtropical rainforest is home to more than 2000 species of vascular plants and large mammals such as tapirs, giant anteaters, howler monkeys, ocelots and jaguars. | [[63]](https://en.wikipedia.org/wiki/List_of_World_Heritage_Sites_in_South_America#cite_note-67) |  

# List of World Heritage Sites in South America
## World Heritage Sites
| Ischigualasto / Talampaya Natural Parks |  | ArgentinaSan Juan and La Rioja Province Argentina 30°0′S 68°0′W / 30.000°S 68.000°W / -30.000; -68.000 (Ischigualasto / Talampaya Natural Parks) | Natural: (viii) | 275,369 (680,450) | 2000 | As the most complete continental fossil site of the Triassic period (245–208 million years ago), the propertie's remains of mammals, dinosaurs and plants reveal the evolution of vertebrates. | [[64]](https://en.wikipedia.org/wiki/List_of_World_Heritage_Sites_in_South_America#cite_note-68) |  
| Jesuit Block and Estancias of Córdoba |  | ArgentinaCórdoba Argentina 31°25′14″S 64°11′28″W / 31.42056°S 64.19111°W / -31.42056; -64.19111 (Jesuit Block and Estancias of Córdoba) | Cultural: (ii), (iv) | — | 2000 | Founded in the early 17th century, this Jesuit reduction has preserved the university, church, residences and five farming estates (estancias), illustrating the missionary and economic activities carried out by the Jesuits over a period of 150 years in the New World. | [[65]](https://en.wikipedia.org/wiki/List_of_World_Heritage_Sites_in_South_America#cite_note-69) |
</excerpt>

## Search 9 — query: "original members of the United Nations list 51 countries"
### Rank 1 of 93 — 0.59 (passed on)
<excerpt title="About Us | United Nations">
One place where the world's nations can
gather together, discuss common problems
and find shared solutions.
The United Nations is an international organization founded in 1945. Currently made up of 193 Member States, the UN and its work are guided by the purposes and principles contained in its founding Charter.
The UN has evolved over the years to keep pace with a rapidly changing world.
But one thing has stayed the same: it remains the one place on Earth where all the world’s nations can gather together, discuss common problems, and find shared solutions that benefit all of humanity.
Video 3
The most impossible job on Earth. So far only 9 people have held the top leadership position in the world’s largest multilateral organization. What does it mean to be UN Secretary-General?
>   
> ## Secretary-General  
>   
>   
> In the end, it comes down to values [...] We want the world our children inherit to be defined by the values enshrined in the UN Charter: peace, justice, respect, human rights, tolerance and solidarity.  
>   
> António Guterres United Nations Secretary-General
The Secretary-General is Chief Administrative Officer of the UN – and is also a symbol of the Organization's ideals and an advocate for all the world's peoples, especially the poor and vulnerable.
The Secretary-General is appointed by the General Assembly on the recommendation of the Security Council for a 5-year, renewable term.
The current Secretary-General, and the 9 th occupant of the post, is António Guterres of Portugal, who took office on 1 January 2017.
On the 18 th of June, 2021, Guterres was re-appointed to a second term, pledging as his priority to continue helping the world chart a course out of the COVID-19 pandemic.

## UN System
©WFP/Ali Habib
The United Nations is part of the UN system, which, in addition to the UN itself, comprises many programmes, funds and specialized agencies, each of which have their own area of work, leadership and budget.
The UN coordinates its work with these separate UN system entities, all of which cooperate with the Organization to help it achieve its goals.
**UN System**

## UN Emblem and Flag
The UN’s symbol — who designed it? what does it mean?

## UN History
*   Overview  
*   Milestones in UN History  
Timeline from 1941 to the present

*   The San Francisco Conference  
51 countries sign the UN Charter creating a new organization

*   Preparatory Years: UN Charter History  
Events which led to the UN’s creation

*   Predecessor: The League of Nations  
The League of Nations and the first international organizations

## Nobel Peace Prize
The UN, UN system entities, and staff have been awarded the Nobel Peace Prize more than a dozen times.
</excerpt>
### Rank 2 of 93 — 0.52
<excerpt title="Member states of the United Nations">
In principle, only sovereign states can become UN members,[[8]](https://en.wikipedia.org/wiki/Member_states_of_the_United_Nations#cite_note-United_Nations-9) and currently, all UN members are sovereign states. Although five members were not sovereign when they joined the UN, they all subsequently became fully independent between 1946 and 1991.[[9]](https://en.wikipedia.org/wiki/Member_states_of_the_United_Nations#cite_note-10) Because a state can only be admitted to membership in the UN by the approval of the Security Council and the General Assembly,[[10]](https://en.wikipedia.org/wiki/Member_states_of_the_United_Nations#cite_note-11)[[8]](https://en.wikipedia.org/wiki/Member_states_of_the_United_Nations#cite_note-United_Nations-9)a number of states that are considered sovereign according to the Montevideo Convention are not members of the UN. This is because the UN does not consider them to possess sovereignty, mainly due to the lack of international recognition or due to opposition from one of the permanent members.
In addition to the member states, the UN also invites non-member states to become observer states at the UN General Assembly,[[11]](https://en.wikipedia.org/wiki/Member_states_of_the_United_Nations#cite_note-12) allowing them to participate and speak in General Assembly meetings, but not vote. Observers are generally intergovernmental organizations and international organizations and entities whose statehood or sovereignty is not precisely defined.
The world in 1945, after World War II. In light blue, the founding members of the United Nations. In dark blue, protectorates and territories of the founding members.

The UN officially came into existence on 24 October 1945, after ratification of the United Nations Charter by the five permanent members of the United Nations Security Council (the Republic of China, France, the Soviet Union, the United Kingdom, and the United States) and a majority of the other signatories.[[12]](https://en.wikipedia.org/wiki/Member_states_of_the_United_Nations#cite_note-13) A total of 51 original members (or founding members) joined that year; 50 of them signed the Charter at the United Nations Conference on International Organization in San Francisco on 26 June 1945, while Poland, which was not represented at the conference, signed it on 15 October 1945.[[13]](https://en.wikipedia.org/wiki/Member_states_of_the_United_Nations#cite_note-14)[[14]](https://en.wikipedia.org/wiki/Member_states_of_the_United_Nations#cite_note-originalmembers-15)
</excerpt>
### Rank 3 of 93 — 0.52
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
### Rank 4 of 93 — 0.51
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
### Rank 5 of 93 — 0.48
<excerpt title="Where can I find information about the founding members of the UN?">
The following information comes from the UN MembershipResearch Guide.

## Founding Member States
The United Nations was established by the Charter of the United Nations and Statute of the International Court of Justice.
The Charter was signed on 26 June 1945 by the representatives of 50 countries; Poland signed on 15 October 1945. There were 51 Founding Members in 1945. The founding members of the United Nations are the countries that were invited to participate in the 1945 San Francisco Conference at which the UN Charter and Statute of the ICJ was adopted. Participation was determined by virtue of having signed or adhered to the Declaration by United Nations (1942) or as approved at the Conference.
In accordance with Article 110, the Charter entered into force on 24 October 1945, after ratification by the five permanent members of the Security Council and a majority of the other countries. Twenty-two countries subsequently deposited their instruments of ratification. The table below reflects the pattern of ratification: first the five permanent members, then the other countries that ratified by 24 October, and then the remaining countries.
Since 1945, some of the Founding Members have changed their names, others have been dissolved and new states have succeeded them.

## Founding Member States
| Original Member State | Date of Signing | Deposit of Ratification | Current Name/Successor States |  
| --- | --- | --- | --- |  
| Republic of China | 26 June 1945 | 28 Sept. 1945 | People's Republic of China |  
| France | 26 June 1945 | 31 Aug. 1945 |  |  
| Union of Soviet Socialist Republics | 26 June 1945 | 24 Oct. 1945 | Russian Federation |  
| United Kingdom of Great Britain and Northern Ireland | 26 June 1945 | 20 Oct. 1945 |  |  
| United States of America | 26 June 1945 | 8 Aug. 1945 |  |  
| Argentina | 26 June 1945 | 24 Sept. 1945 |  |  
| Brazil | 26 June 1945 | 21 Sept. 1945 |  |  
| Byelorussian Soviet Socialist Republic | 26 June 1945 | 24 Oct. 1945 | Belarus |  
| Chile | 26 June 1945 | 11 Oct. 1945 |  |  
| Cuba | 26 June 1945 | 15 Oct. 1945 |  |  
| Czechoslovakia | 26 June 1945 | 19 Oct. 1945 | Czechia and Slovakia |  
| Denmark | 26 June 1945 | 9 Oct. 1945 |  |  
| Dominican Republic | 26 June 1945 | 4 Sept. 1945 |  |  
| Egypt | 26 June 1945 | 22 Oct. 1945 |  |  
| El Salvador | 26 June 1945 | 26 Sept. 1945 |  |  
| Haiti | 26 June 1945 | 27 Sept. 1945 |  |
</excerpt>

## Search 10 — query: "World Heritage in Danger natural sites list Wikipedia"
### Rank 1 of 165 — 0.37 (passed on)
<excerpt title="List of World Heritage in Danger">
# List of World Heritage in Danger
##### Central African Republic
*   Manovo-Gounda St Floris National Park (1997)

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
### Rank 2 of 165 — 0.36
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
### Rank 3 of 165 — 0.28
<excerpt title="1978 (1st list - 2nd session)">
Germany	Garden Kingdom of Dessau-Wörlitz	Cultural	534  
Monastic Island of Reichenau	Cultural	974  
 Hungary	Early Christian Necropolis of Pécs (Sopianae)	Cultural	853  
 Italy	Assisi, the Basilica of San Francesco and Other Franciscan Sites	Cultural	990  
City of Verona	Cultural	797  
Isole Eolie (Aeolian Islands)	Natural	908  
 Japan	Gusuku Sites and Related Properties of the Kingdom of Ryukyu	Cultural	972  
 Lesotho (F)  
 South Africa	Maloti-Drakensberg Park	Mixed	985  
 Lithuania  
 Russia	Curonian Spit	Cultural	994  
 Malaysia	Gunung Mulu National Park	Natural	1013  
Kinabalu Park (F)	Natural	1012  
 Netherlands	Rietveld Schröderhuis (Rietveld Schröder House)	Cultural	965  
 Nicaragua	Ruins of León Viejo (F)	Cultural	613  
 Oman	Land of Frankincense	Cultural	1010  
 Peru	Historical Centre of the City of Arequipa	Cultural	1016  
 Russia	Ensemble of the Ferapontov Monastery	Cultural	982  
Historic and Architectural Complex of the Kazan Kremlin	Cultural	980  
 Senegal	Island of Saint-Louis	Cultural	956  
 Slovakia	Bardejov Town Conservation Reserve	Cultural	973  
 South Korea	Gochang, Hwasun and Ganghwa Dolmen Sites	Cultural	977  
Gyeongju Historic Areas	Cultural	976  
 Spain	Archaeological Ensemble of Tarraco	Cultural	875  
Archaeological Site of Atapuerca	Cultural	989  
Catalan Romanesque Churches of the Vall de Boí	Cultural	988  
Palmeral of Elche	Cultural	930  
Roman Walls of Lugo	Cultural	987  
 Suriname	Central Suriname Nature Reserve (F)	Natural	1017  
 Sweden	Agricultural Landscape of Southern Öland	Cultural	968  

  Switzerland	Three Castles, Defensive Wall and Ramparts of the Market-Town of Bellinzona	Cultural	884  
 Tanzania	Stone Town of Zanzibar	Cultural	173  
 United Kingdom	Blaenavon Industrial Landscape	Cultural	984  
 United Kingdom  
( Bermuda) (F)	Historic Town of St George and Related Fortifications, Bermuda	Cultural	983  
 Uzbekistan	Historic Centre of Shakhrisyabz	Cultural	885  
 Venezuela	Ciudad Universitaria de Caracas	Cultural	986  
2001 (25th session)edit
31 sites (25 cultural, 6 natural)  
Host:  Finland
</excerpt>
### Rank 4 of 165 — 0.27
<excerpt title="1978 (1st list - 2nd session)">
22 sites (16 cultural, 6 natural)  
Host:  Tunisia
Country	Site	Category	UNESCO Reference no.  
 Australia	Shark Bay, Western Australia	Natural	578  
 Bolivia	Historic City of Sucre	Cultural	566  
 Brazil	Serra da Capivara National Park	Cultural	606  
 Finland	Fortress of Suomenlinna	Cultural	583  
Old Rauma (F)	Cultural	582  
 France	Cathedral of Notre-Dame, Former Abbey of Saint-Remi and Palace of Tau, Reims	Cultural	601  
Paris, Banks of the Seine	Cultural	600  
 Germany	Abbey and Altenmünster of Lorsch	Cultural	515  
 Indonesia	Borobudur Temple Compounds	Cultural	592  
Komodo National Park	Natural	609  
Prambanan Temple Compounds	Cultural	642  
Ujung Kulon National Park (F)	Natural	608  
 Mexico	Historic Centre of Morelia	Cultural	585  
 Mozambique	Island of Mozambique (F)	Cultural	599  
 Niger	Air and Ténéré Natural Reserves (F)	Natural	573  
 Romania	Danube Delta (F)	Natural	588  
 Spain	Poblet Monastery	Cultural	518  
 Sri Lanka	Rangiri Dambulla Cave Temple	Cultural	561  
 Sweden	Royal Domain of Drottningholm (F)	Cultural	559  
 Thailand	Historic City of Ayutthaya	Cultural	576  
Historic Town of Sukhothai and Associated Historic Towns (F)	Cultural	574  
Thungyai-Huai Kha Khaeng Wildlife Sanctuaries	Natural	591  
1992 (16th session)edit
20 sites (16 cultural, 4 natural)  
Host:  United States

Country	Site	Category	UNESCO Reference no.  
 Albania	Butrint (F)	Cultural	570  
 Algeria	Kasbah of Algiers	Cultural	565  
 Australia	K'gari (Fraser Island)	Natural	630  
 Cambodia	Angkor (F)	Cultural	668  
 China	Huanglong Scenic and Historic Interest Area	Natural	638  
Jiuzhaigou Valley Scenic and Historic Interest Area	Natural	637  
Wulingyuan Scenic and Historic Interest Area	Natural	640  
( Czechoslovakia)  
 Czech Republic	Historic Centre of Český Krumlov	Cultural	617  
Historic Centre of Prague	Cultural	616  
Historic Centre of Telč (F)	Cultural	621  
 France	Bourges Cathedral	Cultural	635  
 Germany	Mines of Rammelsberg, Historic Town of Goslar and Upper Harz Water Management System	Cultural	623  
 Greece	Pythagoreion and Heraion of Samos	Cultural	595  
 Mexico	El Tajin, Pre-Hispanic City	Cultural	631  
 Poland	Old City of Zamość	Cultural	564  
 Russia	Cultural and Historic Ensemble of the Solovetsky Islands	Cultural	632  
Historic Monuments of Novgorod and Surroundings	Cultural	604  
White Monuments of Vladimir and Suzdal	Cultural	633  
 Thailand	Ban Chiang Archaeological Site	Cultural	575  
 United States	Taos Pueblo	Cultural	492  
1993 (17th session)edit
33 sites (29 cultural, 4 natural)  
Host:  Colombia
</excerpt>
### Rank 5 of 165 — 0.26
<excerpt title="1978 (1st list - 2nd session)">
South Africa	iSimangaliso Wetland Park – Maputo National Park	Natural	914  
 Netherlands	Droogmakerij de Beemster (Beemster Polder)	Cultural	899  
 Nigeria	Sukur Cultural Landscape (F)	Cultural	938  
 Philippines	Historic City of Vigan	Cultural	502  
Puerto-Princesa Subterranean River National Park	Natural	652  
 Poland	Kalwaria Zebrzydowska: the Mannerist Architectural and Park Landscape Complex and Pilgrimage Park	Cultural	905  
 Portugal	Laurisilva of Madeira	Natural	934  
 Romania	Dacian Fortresses of the Orastie Mountains	Cultural	906  
Historic Centre of Sighişoara	Cultural	902  
Wooden Churches of Maramureş	Cultural	904  
 Russia	Western Caucasus	Natural	900  
 Saint Kitts and Nevis	Brimstone Hill Fortress National Park (F)	Cultural	910  
 South Africa	Fossil Hominid Sites of South Africa	Cultural	915  
Robben Island (F)	Cultural	916  
 Spain	Ibiza, Biodiversity and Culture	Mixed	417  
San Cristóbal de La Laguna	Cultural	929  
 Turkmenistan	State Historical and Cultural Park 'Ancient Merv' (F)	Cultural	886  
 United Kingdom	Heart of Neolithic Orkney	Cultural	514  
 Vietnam	Hoi An Ancient Town	Cultural	948  
My Son Sanctuary	Cultural	949  
2000 (24th session)edit
61 sites (50 cultural, 10 natural, 1 mixed)  
Host:  Australia
</excerpt>

For each search, read the top excerpt and the ones ranked below it, and judge whether the order is right for answering the question. An excerpt holding the answer, or a fact that leads to it, should outrank one that only repeats the query's words or covers the topic without a checkable fact. If none of the excerpts holds anything useful, that is the search's fault, not this instruction's. Find the ranking error that cost the most and write a new instruction that fixes it. Replace or compress existing text where you can; avoid making it much longer. Do not write the "Original question" or "Search query" lines; they are appended for you. Do not copy any fact, name, site or topic from these examples.

Provide the new instruction within ``` blocks.
