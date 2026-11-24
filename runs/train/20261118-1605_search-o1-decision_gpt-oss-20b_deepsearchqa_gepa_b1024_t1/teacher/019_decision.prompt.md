I use the instruction below for a decision model inside a web-search question-answering pipeline:
```
Does this excerpt contain source facts that help answer the original question, given the search query? Count specific values, records, table rows, names, dates or relations for the entities the question asks about, even if they cover only part of what is needed (one year, one item, one candidate). Commentary, opinion or general discussion that echoes the question's wording but gives no checkable values for those entities does not count. The query itself is not evidence.
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

## Grade 1.00

## Search 1 — query: "2007 DS RPG co-developed by Square Enix other company named after a planet"
### Rank 1 of 201 — 0.69 (passed on)
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
### Rank 2 of 201 — 0.37
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
### Rank 3 of 201 — 0.21
<excerpt title="Square Enix - Mario Wiki - Fandom">
**Square Enix** is a Japanese video game company known for developing the _Final Fantasy_, _Dragon Quest_, and (in collaboration with Disney) _Kingdom Hearts_ franchises. It was created by the merger of **Square** and **Enix** on April 1, 2003.
Before its merger with Enix, Square was noted for making _Super Mario RPG: Legend of the Seven Stars_ in collaboration with Nintendo.
Square Enix also made _Mario Hoops 3-on-3_ and _Itadaki Street DS_ for the Nintendo DS, with the latter exclusive to Japan. Both of those DS games are crossovers between the _Mario_ franchise and one of Square Enix's franchises (_Final Fantasy_ in the former's case, and _Dragon Quest_ in the latter's case). Another of the company's creations is _Mario Sports Mix_, the first _Mario_ spin-off from the company to be made for the Wii. The game includes the same _Final Fantasy_ characters who appear in _Mario Hoops 3-on-3_, as well as Slime, one of the _Dragon Quest_ characters who appears in _Itadaki Street DS_. The company logo appears in _Mario Hoops 3-on-3_, where it can be seen on two courts: Mario Stadium and Peach Field. Square Enix also developed another _Dragon Quest_-_Mario_ crossover game called _Fortune Street_, a sequel to _Itadaki Street DS_.

Square Enix is also one of the third-party companies represented by playable characters in _Super Smash Bros. for Nintendo 3DS_ / _Wii U_, with Cloud Strife, the hero of _Final Fantasy VII_, available as a downloadable fighter. Also, a stage based on a location from _Final Fantasy VII_; Midgar, is available. In addition, accessories for Mii Fighters based on Geno and Chocobo were available for purchase. The second _Final Fantasy_ fighter, Sephiroth, makes his debut as a DLC character in _Super Smash Bros. Ultimate_, Cloud returns as a fighter, and Midgar also appears as a returning stage. _Super Smash Bros. Ultimate_'s Challenger Pack 2 downloadable content features elements from the _Dragon Quest_ series, including the fighter Hero and the stage Yggdrasil's Altar, while Challenger Pack 11 (the final DLC pack for _Super Smash Bros. Ultimate_) introduces downloadable content originating from the Square Enix-developed _Kingdom Hearts_ series, including the character Sora and the stage Hollow Bastion. Mii Fighter items based on characters from the _Dragon Quest_ series are also available as DLC in _Super Smash Bros. Ultimate_.
In 2023, a remake of _Super Mario RPG_ was released, developed by ArtePiazza, a frequent collaborator with Square Enix, best known for remaking several entries in the _Dragon Quest_ series.

## _Mario_ games developed and/or published[]
| Title | Year released | Console |  
| --- | --- | --- |  
| _Super Mario RPG: Legend of the Seven Stars_ | 1996 | SNES |  
| _Mario Hoops 3-on-3_ | 2006 | Nintendo DS |  
| _Itadaki Street DS_ | 2007 | Nintendo DS |  
| _Mario Sports Mix_ | 2010 | Wii |  
| _Fortune Street_ | 2011 | Wii |

## []
| Title | Year released | Console |  
| --- | --- | --- |  
| _Super Smash Bros. for Nintendo 3DS_ | 2014 | Nintendo 3DS |  
| _Super Smash Bros. for Wii U_ | 2014 | Wii U |  
| _Super Smash Bros. Ultimate_ | 2018 | Nintendo Switch |  
| _Super Mario RPG_ | 2023 | Nintendo Switch |

## Gallery[]
Square's original logo
Enix's original logo
</excerpt>
### Rank 4 of 201 — 0.19
<excerpt title="Square Enix">
Romano, Sal (September 18, 2014). "Square Enix announces Shinra cloud gaming service". Gematsu. Archived from the original on April 16, 2016. Retrieved May 14, 2016.  
Jump up to:  
 Purchese, Robert (January 6, 2016). "Square Enix closes cloud gaming company Shinra Technologies". Eurogamer. Gamer Network. Archived from the original on January 8, 2016. Retrieved January 6, 2016.  
 Eisenbeis, Richard (September 19, 2014). "Hands On with Square Enix's New Streaming Service". Kotaku. Archived from the original on June 2, 2016. Retrieved May 11, 2016.  
Jump up to:  
 Alvarez, Edgar (August 14, 2015). "Square Enix is killing its game-streaming service in Japan". Engadget. Archived from the original on June 2, 2016. Retrieved May 11, 2016.  
 "Final Fantasy VII Streaming On Cloud Gaming Services In Japan". Siliconera. December 24, 2013. Archived from the original on September 24, 2020. Retrieved September 20, 2020.  
 "SQUARE ENIX in G-cluster App". gcluster.jp. Archived from the original on September 26, 2020. Retrieved September 20, 2020.  
 Jenkins, David (December 12, 2005). "Square Enix To Complete Taito Takeover". Gamasutra. Archived from the original on September 21, 2016. Retrieved May 20, 2016.  
Jump up to:  
 "Taito Announces Digital Download System For Arcades". Gamasutra. September 13, 2010. Archived from the original on August 11, 2014. Retrieved July 28, 2014.
</excerpt>
### Rank 5 of 201 — 0.18
<excerpt title="Companies: Square Enix">
## The merger
So 2003 approached and both big RPG developers had to face the future of RPG development. Enix had to finance a big RPG project developed by tri-Ace (not to forget the plans of doing Dragon Quest VIII), and Square set up an expensive online community while developing some new games for the Nintendo GBA, the Sony PlayStation 2 and even the Game Cube. On top of that, Game development got more and more expensive. It seemed for both companies the best solution to merge. And so they did. In 2003, Squaresoft Co, Ltd. and Enix Corporation became one...
Officially, Enix took over Square back then. All the shareholders of Square got paid to exchange their Square shares for Enix shares. The management, however, was moved from Square to Square Enix. So the company that took over another was now controlled by those they took over. Quite awkward businessman-stuff, if you ask me.
Anyway, now both of the big RPG makers were able to create their games under the same flag. This was a shocking moment for many fans since there always was quite some rivalry going on between Square fans and Enix fans. Now they were fans of the same company. Some gamers now screamed that the games don't have the same quality as before the merger, and some even quit their hobby because they thought everything is lost. But was everything really lost? The portfolio of the new founded company was quite impressive: Star Ocean: Till The End of Time, Final Fantasy XI online, Dragon Quest VIII, Kingdom Hearts: Chain of Memories, Front Mission 4, Radiata Stories, Romacing SaGa... all of them were great RPGs created between 2003 and 2005. Now the company was even powerful enough to delay the release date of Final Fantasy XII so that they can do more finishing work without fearing bankruptcy if the game isn't released as soon as possible. They even were powerful enough now to support their former rival Game Arts while they were developing Grandia III, which was also released as a "Square Enix" game in 2006.

## The merger
This article was written on May 28th, 2006. On this day, Square-Enix's plans for the future looked promising. Children of Mana (DS), Final Fantasy III (DS) and Final Fantasy VII: Crisis core (PSP) seemed to be pretty good handheld-RPGs, where one was more focused on gameplay and the other two on story. The support of home consoles looked also very promising - Final Fantasy XII (PS2), Final Fantasy XIII (PS3), Final Fantasy: Crystal Chronicles 2 (Wii), Dragon Quest Yangus (PS2), Dragon Quest (Wii), Dawn of Mana (PS2), Valkyrie Profile 2: Silmeria (PS2)... there were lots of possibly great games announced. However, not everything went as perfect as Square Enix could have wished for: Game Arts was bought by a big online game publisher, stalling the new relationship between Square-Enix and Game Arts. Microsoft was able to make a contract with tri-Ace so that they'll create a RPG exclusively for the XBox 360 console without working together with Square-Enix. Did that mean that the long partnership between Square-Enix and tri-Ace ended? That was quite uncertain in late May 2006. How does a very famous Square action RPG say? "Time flows like a river, but history repeats." Will this work for Square Enix too?
Although I did this already at the copyright comments section, I just wanted to repeat this: All images (and especially the logos!) on this page are property of their respective owners. Consulting Moby Games helped me a lot to back up everything I wrote down.
</excerpt>

## Search 2 — query: ""The World Ends with You" developed by Square Enix Jupiter"
### Rank 1 of 98 — 0.71 (passed on)
<excerpt title="The World Ends With You | Fandom">
Overview
_**The World Ends with You**_, known in Japan as _**It's a Wonderful World**_ (すばらしきこのせかい _Subarashiki Kono Sekai_), is an action-RPG for the Nintendo DS and the first installment in _The World Ends with You_ series. The game was released in Japan in July 2007, and in PAL regions and North America on April 22, 2008.
The game was developed by the _Kingdom Hearts_ team, Square Enix, and Jupiter. The character designs were made by Tetsuya Nomura and Gen Kobayashi. The distinctive art style is inspired by the aesthetics of Shibuya’s youth culture. The development of the game was inspired by elements of Jupiter's previously released game, _Kingdom Hearts: Chain of Memories_.
The story is focused on a asocial teenager named Neku Sakuraba and his new allies who are forced to participate in a mysterious deadly game called the Reapers' Game in which they will die by being erased from existence if they do not complete daily missions. The battle system uses many of the unique features of the Nintendo DS, including combat taking place on both screens, and attacks performed by certain motions on the touchscreen or by shouting into the microphone. Elements of Japanese youth culture, such as fashion, food, and cell phones, are key aspects of the missions.
A port titled _The World Ends with You -Solo Remix-_ was released on iOS and Android mobile phones on August 27, 2012.
The Nintendo Switch remaster titled _The World Ends with You: Final Remix_ released September 27th, 2018 in Japan, and elsewhere on October 12th, 2018.
The anime adaptation, titled _The World Ends with You The Animation_, was released in 2021.
A sequel, titled _NEO: The World Ends with You_, was released on July 27th, 2021 for the Nintendo Switch and PlayStation 4, and September 28, 2021 for PC.

## Gameplay[]
_The World Ends with You_ is an action-RPG for the Nintendo DS, and uses many intricate gameplay elements.

## Gameplay[]
### Combat[]
_See Also_: Combat
Shiki (top) and Neku (bottom) fighting Noise.
The combat system in _The World Ends with You_, called the Stride Battle Cross System, utilizes both DS screens to function. The top screen is occupied by Neku's current partner, and the bottom screen is used by Neku himself. The two places are called "Zones", and in each Zone, there are the same Noise, the enemies in the game. The enemies inside the Zones share an HP bar between them, meaning that attacking an enemy in one Zone will damage it in the other Zone as well. Neku and his partner are synchronized as well, and therefore also share a HP bar. Being synchronized also allows their access to powerful Fusion attacks which attack all enemies for large damage. During battle, a Light Puck will pass from Neku to his partner as attacks are used. The more the Puck is passed around, the higher the combo built up and therefore the higher the damage.
The bottom screen is used to control Neku. Various touches of the bottom screen make Neku perform specific actions and move, depending on what pins he has equipped. These can range from short slides on the enemy to tapping at the air to shoot projectiles, but only 6 pins at maximum can be equipped at once. The top screen, containing Neku's current partner, is controlled by pressing the directional buttons, or the control pad, in specific directions to select a pathway of arrows. What lies at the end of each arrow varies by partner, however. If the right set of commands are met, the player gets a star, which contributes towards a Fusion attack.
For example, Shiki has arrows leading to cards, based on Zener Cards, and matching them with the cards on top gives a star. The partner cannot directly move, but can dodge, block, or in Joshua's case, float. Once a Fusion command has been acquired, it can be tapped on the touch screen to use it, and special cards can be used to upgrade these to a higher level.
</excerpt>
### Rank 2 of 98 — 0.71
<excerpt title="The World Ends with You">
_The World Ends with You_ was developed by the same team that created the _Kingdom Hearts_ series, with input from Jupiter,[[26]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-29) the company that developed _Kingdom Hearts: Chain of Memories_ for the Game Boy Advance. Development of the game started two and a half years before its Japanese release, during the development of _Kingdom Hearts II_ and as development of _Chain of Memories_ was concluding.[[27]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-roundtable1-30) At that time, Nintendo revealed their next handheld system, the Nintendo DS, but was not yet available to the market; Square Enix requested the team to develop a game specifically for the handheld system.[[27]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-roundtable1-30)

The creative team — consisting of director Tatsuya Kando, co-director Tomohiro Hasegawa, planning director Takeshi Arakawa, and creative producer and character designer Tetsuya Nomura — were able to experience the DS during the "Touch DS" event in November 2004.[[28]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-roundtable2-31) From this demonstration, they had envisioned a version of _Chain of Memories_ in which the card game aspects would be present on the bottom screen and an action role-playing game on the top. As they continued to work on the game, the developers realized that they wanted to use the touchscreen more, to make "a game that can only be played on the DS".[[28]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-roundtable2-31) However, they also encountered the problem that by focusing heavily on the touchscreen, the top screen would be ignored. From this, the idea of the dual-screen battle system arose.[[28]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-roundtable2-31) Several other options were explored for the top screen gameplay, including command-based battles or a rhythm game, but once they reviewed the game from the eyes of the player, they ultimately settled on the card-game approach with the player having the option to control the game if they wanted to.[[29]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-postmortem-32)

Even with the completion of the Japanese version of the game, the team felt the dual-screen system was too much for overseas audiences, and attempted to change the card-game mechanic into a special meter that would fill up with normal attacks from Neku, but this was not completed in time for release.[[29]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-postmortem-32) The team was able to alter the "information overload" of the numerous tutorials at the start of the game in the North American release, reducing the amount of text presented as well as allowing the tutorials to be skipped. The "Active Encounter" system, the ability for the player to select when and how to go into battle, was developed specifically to avoid the issues of "grinding" that are common with most standard RPG systems.[[29]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-postmortem-32) While they included the mechanics of being able to scan non-playable characters to see their thoughts, the team was not able to integrate this mechanic more into the game.[[29]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-postmortem-32)
</excerpt>
### Rank 3 of 98 — 0.62
<excerpt title="Postmortem: Square Enix's THE WORLD ENDS WITH YOU">
## What Went Right
This middleware had only been used for voice compression in the past, and this was the first time anyone had used it for music. We were blown away when we heard the first vocal track coming out of the DS, and realized we'd be able to include a full digital soundtrack.
We removed the pre-rendered movies and replaced them with Flash-style sequences, which freed up cartridge space to include over 30 songs. In the end, about 1/4th of the game ROM consists of compressed music data. This was an example of how trying something new really paid off.

## What Went Wrong
**1. Time management and development culture clash.**
The game was developed by Square Enix in Tokyo and Jupiter in Kyoto. While we originally commissioned Jupiter as the developer, we wound up with more creative crossover than we thought.
The Square-side directors got involved in the gameplay design elements, while Jupiter went beyond the call of duty and assisted with the game planning. The cooperative endeavor resulted in a fantastic product, but it came at a price.
Square and Jupiter have very different development cultures, but it took us a while to realize it. We assumed all companies' development processes were the same -- that our way was the standard. Once we met up and reached a consensus on how to do things, work proceeded much more smoothly.
Geographically, we were very distant as well -- it takes about two hours to get between Tokyo and Kyoto via bullet train. It was critical that we met in person, but this ended up costing us time, and it hurt the schedule at every step.
We had weekly telephone conferences, but it was hard for us to "read" each other over the line. Sadly, we were unable to do video conferencing, which I believe would have resulted in a more open, jam-session sort of feel.
**2. Story creation scheduling.**
Even though we were happy with how the story turned out, the process started going smoothly only halfway through the project. When we started, we were plagued by confused direction and constant rewrites by the scenario staff.
Changing plot elements mid-project is risky business, and we were making tweaks to the scenario all the way up until just before master submission!
We were able to pull it off because the game didn't contain a lot of voice -- if it had been voice-heavy, we would have had to lock down the scenario far earlier.
Although it's obvious that the scenario should be put together early on in the development process, it also takes time to create something that's truly interesting. Maintaining this balance is extremely important.
We made three big mistakes with some of the gameplay concepts we implemented. The first issue was how the player could "scan" the thoughts of NPCs. We should have integrated this into the story more, because it never really related to solving puzzles.
I can't say the whole system was unnecessary, but it could have been integrated much better. If there is a sequel, this is something we'll need to work on.
</excerpt>
### Rank 4 of 98 — 0.61
<excerpt title="The World Ends With You : Video Games">
# Feedback
## Product Description
### Product description
The World Ends with You DS

# Feedback
## Product Description
### Amazon.com
From the creators of the award-winning Final Fantasy and Kingdom Hearts franchises comes a revolutionary, modern action-RPG title for a new generation of gamers. Square Enix and Jupiter team up once again to showcase The World Ends With You, a trendy and vibrant gaming experience developed exclusively for the Nintendo DS. Featuring an intuitive combat system and exciting multiplayer mode, The World Ends With You is set to immerse gamers into the modern-day culture of Japan.
Story
The story begins as Neku Sakuraba, an unsociable 15-year-old boy, unexpectedly wakes up in the Shibuya shopping district of Tokyo, Japan. While trying to piece together his rude awakening, he receives a strange text message warning him that he will cease to exist unless he accomplishes a certain mission. Although he barely has time to grasp what is happening to him, he commences his assigned task in the mysterious streets of Shibuya.Features:
*   Distinctive modern art style created by a team of artists led by Tetsuya Nomura, world-renowned character designer of the upcoming Fabula Nova Crystallis project which includes Final Fantasy XIII and Final Fantasy Versus XIII  
*   Innovative Stride-Cross Battle System allows players to control two characters simultaneously, unleashing special attacks with the stylus  
*   Collect a vast array of custom-designed pins, each with a powerful psychic ability that can be activated with the right touch or sound command  
*   Customize characters with Shibuya?s coolest fashions and exchange items with other players via Mingle Mode  
*   Experience an amazing soundtrack combining a fusion of musical influences from hip-hop to rock to electronica  
*   Battle with up to three friends in Tin Pin Slammer, an exciting and fast-paced mini-game, via local wireless connection
* * *

# Feedback
## Related products with free delivery on eligible orders
Sponsored | Try Prime for unlimited fast, free shipping
Page 1 of 1Start over
_Previous page of related Sponsored Products_
1.   [Feedback](javascript:void(0))   iPLYGAM Switch Game Case Holder for Nintendo Switch 2/OLED/Lite with 96 Cartridge S...212 Black Friday Deal-20%KRW 29,364 KRW 29,364 Typical price: KRW 36,708 Typical price:null KRW36,708 FREE delivery Tue, Dec 1 to Republic of Korea on $49 (KRW 66,643) of eligible items Climate Pledge Friendly    
2.   [Feedback](javascript:void(0))   GHOST Energy Drink, Zero Sugars, 12-Pack, Electric Limeade, 16oz | Energy & Focus P...15,376 Black Friday Deal-15%KRW 34,655 KRW 34,655(KRW 177 KRW177 / fluid ounce) Typical: KRW 40,788 Typical:null KRW40,788 FREE delivery Tue, Dec 1 to Republic of Korea on $49 (KRW 66,643) of eligible items    
3.   [Feedback](javascript:void(0))   FINTIE Soft Silicone Protective Case Compatible with Nintendo Switch 2017 | Ergonom...4,340 Black Friday Deal-20%KRW 14,131 KRW 14,131 Typical price: KRW 17,667 Typical price:null KRW17,667 FREE delivery Tue, Dec 1 to Republic of Korea on $49 (KRW 66,643) of eligible items    
4.   [Feedback](javascript:void(0))   I Love You More The End I Win Heart Matching Keychains Valentines Keychain | I love...1 KRW 10,867 KRW 10,867 FREE delivery Tue, Dec 1 to Republic of Korea on $49 (KRW 66,643) of eligible items
</excerpt>
### Rank 5 of 98 — 0.60
<excerpt title="The World Ends with You">
The game's credits show scenes seven days later in the RG. As Neku walks from Udagawa to the statue of Hachikō to meet Beat, Rhyme, and Shiki, he discusses how the past three weeks have changed him for the better. In a statement addressed to an absent Joshua, Neku states that he trusts him despite not forgiving him for his actions. Neku then asks if Joshua will be present at Hachikō as well.[[24]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-27) Secret reports that can be obtained by completing additional missions after beating the game reveal that Joshua, after seeing Neku's personality change while playing the game, decides to spare Shibuya, now believing it to be ideal.[[25]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-28)
The _Final Remix_ version of the game adds new storyline content taking place after the main game. Neku and Beat awaken in a geographically distorted alternate version of Shibuya and are assigned a mission to escape it within 24 hours. Accompanied by a Reaper named Coco Atarashi, the two traverse through the alternate Shibuya while encountering Shiki and Rhyme. As they progress, Neku has visions of a city being destroyed and a strange girl with Shiki's stuffed animal, as well as what are seemingly distorted flashbacks of his death and Rhyme's sacrifice. When Rhyme sacrifices herself to save Beat as in Neku's vision, Neku realizes that he is having visions of the future. Neku and Beat arrive at Mr. Hanekoma's café, and he reveals that the Shibuya they have been traversing is a giant Noise Coco created. Neku and Beat defeat the Noise and return to reality. An enraged Coco shoots Neku dead, but Joshua fends her off. Joshua meets with Hanekoma to discuss recent events; they reveal that Shinjuku has been erased and that Noise are starting to appear in the RG, and that the strange girl from Neku's visions was a survivor of the incident who they theorize caused Neku's visions and was helping him. Elsewhere, Coco plots to continue using Neku for her plans and resurrects Minamimoto to serve as his partner.

_The World Ends with You_ was developed by the same team that created the _Kingdom Hearts_ series, with input from Jupiter,[[26]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-29) the company that developed _Kingdom Hearts: Chain of Memories_ for the Game Boy Advance. Development of the game started two and a half years before its Japanese release, during the development of _Kingdom Hearts II_ and as development of _Chain of Memories_ was concluding.[[27]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-roundtable1-30) At that time, Nintendo revealed their next handheld system, the Nintendo DS, but was not yet available to the market; Square Enix requested the team to develop a game specifically for the handheld system.[[27]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-roundtable1-30)
</excerpt>

## Search 3 — query: "TWEWY Secret Report Day 5 partner"
### Rank 1 of 124 — 0.69 (passed on)
<excerpt title="Secret Reports - The World Ends with You Wiki - Fandom">
Mr. Hanekoma, author of the Secret Reports.
The **Secret Reports** are records written by Sanae Hanekoma. They contain information that fill in many of the plot holes in _The World Ends With You_ and _NEO: The World Ends with You_.
To those who have not finished the games, they spoil major parts of the stories of both games. Players may wish to collect them in-game for the reward of reading them, as reading this article may disincentivize players from collecting them.
**Spoiler warning**: Plot and/or character details follow.

## The World Ends with You[]


## Obtaining the Reports[]
The Secret Reports can only be obtained after defeating Draco Cantus and unlocking the Chapters Menu. Each chapter's mark contains between one and four stars, which label the tasks to be completed before each report is unlocked. This list contains instructions on completing each of these tasks, as some of them are obscure.
Additionally, for Final Remix, Secret Report 21 cannot be accessed unless the player has unlocked A New Day. It is not necessary to begin or complete A New Day to read Secret Report 21, however.

## Obtaining the Reports[]
| Week and Day | Star 1 | Star 2 | Star 3 | Star 4 |  
| --- | --- | --- | --- | --- |  
| Shiki, Day 1 | After meeting Shiki and defeating the Noise, check Hachiko. |  |  |  |  
| Shiki, Day 2 | Obtain the Secret Report for Week 1, Day 1. Obvious, right? | Kill all of the pig noise. The pig indicator by your phone helps. | Talk to the statue loving guy next to the Moyai after clearing the wall. |  |  
| Shiki, Day 3 | Obtain the Secret Report for Week 1, Day 2. Obvious, right? | Kill all of the pig noise. The pig indicator by your phone helps. | After you learn how to imprint, head to Ramen Don in Dogenzaka to get the "ramen" meme. Imprint it on Futoshi and follow him. | Take down the Vespertillo Canor Blue Noise in the Concert Stage on either Hard or Ultimate Difficulty. |  
| Shiki, Day 4 | Kill all of the pig noise. The pig indicator by your phone helps. | Once Shiki says she wants to go into 104, try to leave instead. | Take down Shades' Blue Noise in the Scramble Crossing on Hard or Ultimate Difficulty. | Take down Beat's Blue Noise at 104 on Hard or Ultimate Difficulty. |  
| Shiki, Day 5 | Obtain the Secret Report for Week 1, Day 4. Obvious, right? | Kill all of the pig noise. The pig indicator by your phone helps. | When Mina and Ai play Reaper Creeper, move the coin to white for all three questions. | Take down the Cornix Canor Blue Noise at Molco on Hard or Ultimate Difficulty. |  
| Shiki, Day 6 | Obtain the Secret Report for Week 1, Day 5. Obvious, right? | Obtain the Secret Report for Week 1, Day 3. Obvious, right? | Kill all of the pig noise. The pig indicator by your phone helps. | When Makoto talks to Shooter in Center St. Entrance, imprint "Totally gnarly!" instead of "Unreal, bro!" |
</excerpt>
### Rank 2 of 124 — 0.60
<excerpt title="Secret Reports - The World Ends with You Wiki - Fandom">
## Obtaining the Reports[]
| Week and Day | Star 1 | Star 2 | Star 3 | Star 4 |  
| --- | --- | --- | --- | --- |  
| Shiki, Day 1 | After meeting Shiki and defeating the Noise, check Hachiko. |  |  |  |  
| Shiki, Day 2 | Obtain the Secret Report for Week 1, Day 1. Obvious, right? | Kill all of the pig noise. The pig indicator by your phone helps. | Talk to the statue loving guy next to the Moyai after clearing the wall. |  |  
| Shiki, Day 3 | Obtain the Secret Report for Week 1, Day 2. Obvious, right? | Kill all of the pig noise. The pig indicator by your phone helps. | After you learn how to imprint, head to Ramen Don in Dogenzaka to get the "ramen" meme. Imprint it on Futoshi and follow him. | Take down the Vespertillo Canor Blue Noise in the Concert Stage on either Hard or Ultimate Difficulty. |  
| Shiki, Day 4 | Kill all of the pig noise. The pig indicator by your phone helps. | Once Shiki says she wants to go into 104, try to leave instead. | Take down Shades' Blue Noise in the Scramble Crossing on Hard or Ultimate Difficulty. | Take down Beat's Blue Noise at 104 on Hard or Ultimate Difficulty. |  
| Shiki, Day 5 | Obtain the Secret Report for Week 1, Day 4. Obvious, right? | Kill all of the pig noise. The pig indicator by your phone helps. | When Mina and Ai play Reaper Creeper, move the coin to white for all three questions. | Take down the Cornix Canor Blue Noise at Molco on Hard or Ultimate Difficulty. |  
| Shiki, Day 6 | Obtain the Secret Report for Week 1, Day 5. Obvious, right? | Obtain the Secret Report for Week 1, Day 3. Obvious, right? | Kill all of the pig noise. The pig indicator by your phone helps. | When Makoto talks to Shooter in Center St. Entrance, imprint "Totally gnarly!" instead of "Unreal, bro!" |
</excerpt>
### Rank 3 of 124 — 0.58
<excerpt title="The World Ends with You - Secret Report FAQ - DS - By CursedAnubis">
In other words, humans, Reapers, and Noise are all  
entities of formed of Soul. The only difference is their  
code.
And what are Noise? Entities without conscious will,  
only the drive to multiply. Thus, they constantly  
thirst for Soul, attacking Players and possessing  
humans in the Realground.
5/5
Soul consumed by Noise is destroyed, even if the  
Noise is erased.
Thus, possessed by humans often exhibit a rush of  
euphoria immediately after the Noise is removed.
Though untested, the same would likely hold were a  
Player or Reaper possessed.
--------------------------------------------
Secret Report 5 - Empty Urban Legends - SRS5|   
--------------------------------------------------------------------------  
Rhyme is caught in the Reapers' Trap and  
erased, leaving Neku and Shiki alone again...
Complete the Following to view this day's report:
Star 1: Collect the report for Shiki, Day 4.
Star 2: Track down and eliminate all of this chapter's Pig Noise symbols.
Star 3: Get Mr. Ducky.(White! White! White!)  
	As the hint may tell you, when playing Reaper Creeper with the  
	two girls, pick white three times, and it will be given to you.
Star 4: Eliminate the Boss symbol No. 90 within this chapter at hard or  
	above.  
	Molco; at the bottom-left corner of the area  
	-DO NOT DO CHAIN REDUCTION BATTLES-
Report Contents---------
1/6
The Realground and Underground are planes of   
existence. Other planes exist as well: the one  
inhabited solely by Noise, for example, or Our  
customary plane.
The planes are stacked in parallel, through each   
exists at a different frequency vibe, in tune with  
its inhabitants.
Observing a lower plane from a higher plane is simple.  
Actual trans-planar contact, while possible, is highly  
complex. The vibes of adjacent planes are closer,  
making passage between them comparatively easier.  
                                                                       2/6  
More distant planes show greater differences in vibe  
frequencies, and thus communion becomes more  
difficult.
</excerpt>
### Rank 4 of 124 — 0.52
<excerpt title="Secret Reports - The World Ends with You Wiki - Fandom">
## NEO: The World Ends with You[]


## Obtaining the NEO Reports[]
The Secret Reports can be obtained by either fighting blue boss noise using Hazuki Mikagi's social network reward, or reaching certain percentage values on the social network.
**Secret Report No. 1**- Defeat the boss noise at Scramble Crossing during Week 1, Day 1
**Secret Report No. 2**- Defeat the boss noise at the 104 Building during Week 1, Day 2
**Secret Report No. 3**- 70% of the Social Network Completed
**Secret Report No. 4**- 80% of the Social Network Completed
**Secret Report No. 5**- Defeat the boss noise found at Tipsy Tose Hall during Week 1, Day 5
**Secret Report No. 6**- 90% of the Social Network Completed
**Secret Report No. 7**- Defeat the boss noise found at TOWER RECORDS SHIBUYA during Week 1, Day 7
**Secret Report No. 8**- Defeat the boss noise found on Takeshita Street during Week 2, Day 1
**Secret Report No. 9**- Defeat the boss noise found at the Scramble Crossing during Week 2, Day 2
**Secret Report No. 10**- 100% of the Social Network Completed
**Secret Report No. 11**- Defeat the boss noise found on Center Street during Week 2, Day 4
**Secret Report No. 12**- Defeat the boss noise found at the Expressway Underpass during Week 2, Day 5
**Secret Report No. 13**- Defeat the boss noise found at Spain Hill during Week 2, Day 6
**Secret Report No. 14**- Defeat the boss noise found on Takeshita Street during Week 2, Day 7
**Secret Report No. 15**- Defeat the boss noise found at TOWER RECORDS SHIBUYA during Week 3, Day 1
**Secret Report No. 16**- Defeat the boss noise found at Dogenzaka during Week 3, Day 2
**Secret Report No. 17**- Defeat the boss noise found at SHIBUYA STREAM during Week 3, Day 3

## Obtaining the NEO Reports[]
**Secret Report No. 18**- Defeat the boss noise found at TOKYU PLAZA during Week 3, Day 4
**Secret Report No. 19**- Defeat the boss noise found at SHIBUYA STREAM during Week 3, Day 5
**Secret Report No. 20**- Defeat the boss noise found at Udagawa Backstreets during Week 3, Day 6
**Secret Report No. 21**- Defeat the boss noise found on Takeshita Street during Week 3, Day 7
**Secret Report No. 22**- Defeat the boss noise found on Takeshita Street during Week 3, Day 7'
**Secret Report No. 23**- Defeat the boss noise found at TOKYU PLAZA during Week 3, Day 7' '
**Secret Report No. 24**- Received once every other secret report is unlocked.
</excerpt>
### Rank 5 of 124 — 0.49
<excerpt title="Secret Reports - The World Ends with You Wiki - Fandom">
## Obtaining the Reports[]
| Joshua, Day 5 | Obtain the Secret Report for Week 2, Day 4. Obvious, right? | Kill all of the pig noise. The pig indicator by your phone helps. | One of the Reapers between you and Cat Street challenges you to a match of Tin Pin. Be a sport and lose to him. | Uzuki and Kariya are pretty angry today. Find their Blue Noise in Udagawa and smack them down on Hard or Ultimate. |  
| Joshua, Day 6 | Obtain the Secret Report for Week 2, Day 5. Obvious, right? | Kill all of the pig noise. The pig indicator by your phone helps. | During your sprint to Udagawa, let your inner jerkface out and ignore everyone's pleas for help. If you really feel bad, you can go back and save them afterwards. | Take down the Grindcore Minks Blue Noise at AMX on Hard or Ultimate Difficulty. |  
| Joshua, Day 7 | Obtain the Secret Report for Week 2, Day 5. Obvious, right? | Kill all of the pig noise. The pig indicator by your phone helps. | Swing by A-East and head into the Stage before climbing Pork City to find the men of Def M**ä**rch inside. Neku immediately thinks to run outside, which you should do. | Head out to Shibukyu Main Store for a rematch with Pi-Face and his minions. Beat them down on Hard or Ultimate Difficulty. |  
| Beat, Day 1 | Kill all of the pig noise. The pig indicator by your phone helps. | On your way back from the Underpass, check Hachiko. Yes, again. | Uzuki's Blue Noise is hanging out next to Kariya's by the Moyai at the Bus Terminal. You know the drill. | Kariya's Blue Noise is chilling next to Uzuki's by the Moyai at the Bus Terminal. You know the drill. |  

## Obtaining the Reports[]
| Beat, Day 2 | Obtain the Secret Report for Week 3, Day 1. Obvious, right? | Kill all of the pig noise. The pig indicator by your phone helps. | While you're chasing down Ironface, stop by the Cosmic Corner shop in Dogenzaka. | Have fun with this one. Take down the Woolly AOR Blue Noise at the Scramble on Hard or Ultimate. Good luck. |  
| Beat, Day 3 | Obtain the Secret Report for Week 3, Day 2. Obvious, right? | Kill all of the pig noise. The pig indicator by your phone helps. | When Makoto's old boss is asking Reaper Creeper for some advice, send the coin to the black circle. Also, handy tip, if you come back again and choose not to creep, Shadow Ramen will open on Day 6. | Take out the Pteroptus Canor Blue Noise in the Concert Stage on Hard or Ultimate Difficulty. |  
| Beat, Day 4 | Obtain the Secret Report for Week 3, Day 3. Obvious, right? | Obtain the Secret Report for Week 2, Day 7. Obvious, right? | Remember all the papers in the Miyashita Park Underpass? After opening the wall to Towa Records, backtrack to where the sun and moon papers were. |  |  
| Beat, Day 5 | Obtain the Secret Report for Week 3, Day 4. Obvious, right? | Kill all of the pig noise. The pig indicator by your phone helps. | On your way through Shibu-Q Heads, you'll be jumped by a TON of Reapers. Once you take them down, have a chat with the remaining one for a few laughs. | Another tough noise. The Goth Metal Drake Blue Noise awaits you in Dogenzaka. Take it down, Hard or Ultimate. |
</excerpt>

## Search 4 — query: "Secret Report Joshua Day 5 boss"
### Rank 1 of 55 — 0.80 (passed on)
<excerpt title="how to find every Boss Noise, and get the secret ending">
It wouldn't be a TWEWY game without Secret Reports, and initially the**NEO: The World Ends With You Secret Reports**these seem like the most confusing to find yet. Luckily, this page is here to help you with the **secret report locations** and **finding every boss noise** to get you to the **NEO secret ending**.
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
### Rank 2 of 55 — 0.72
<excerpt title="Turf (Week 2, Day 5) - The World Ends with You Wiki - Fandom">
## Noise[]
| 53 |  | Carcinofolk | Shibukyu Main Store, Miyashita Park, Cat Street, Spain Hill, Tipsy Tose Hall, AMX |  
| 54 |  | Carcinoska | Scramble Crossing, Statue of Hachiko, Station Underpass, 104 Building, Dogenzaka, A-East, Shibukyu Main Store, Shibu Dept. Store, Cadoi City, Towa Records, Miyashita Park Underpass, Miyashita Park, Cat Street, Molco, Spain Hill, Tipsy Tose Hall, Shibu-Q Heads, AMX |  
| 56 |  | Carcinosamps | Scramble Crossing, Statue of Hachiko, Station Underpass, 104 Building, A-East, Shibukyu Main Store, Shibu Dept. Store, Towa Records, Miyashita Park Underpass, Miyashita Park, Cat Street, Molco, Spain Hill, Shibu-Q Heads, AMX |  
| 58 |  | Decadraven | West Exit Bus Terminal |  
| 59 |  | Easterraven | West Exit Bus Terminal, Center St. Entrance |  
| 80 |  | Reaper Beat | Miyashita Park Underpass (Boss) |  
| 82 |  | Uzuki Yashiro (Berserk) | Udagawa Back Streets (Blue Noise) |  
| 84 |  | Koki Kariya (Berserk) | Udagawa Back Streets (Blue Noise) |

## Rewards[]
Note: Technically clearing the wall to Miyashita Park should be listed as a Main Story event, however the reward received (if any) is dependent on who wins the game of Tin Pin Slammer. As such, while these are technically rewards for clearing the wall, they are listed as extra rewards due to being dependent on actions that are optional.
Main Story Rewards | Event | First Playthrough | Replay |  
| --- | --- | --- |  
| Clear wall to Shibu Dept. Store | (S) ATK Boost Joshua | None |  
| Clear wall to Cadoi City | Psych Support | Psych Support |  
| Clear wall to Towa Records | (S) DEF Boost Joshua | None |  
| Clear wall to Miyashita Park Underpass | Strong Body | Strong Body |  
| Clear wall to Cat Street | Clears all other walls | Clears all other walls |  
| Fight Reaper Beat | (S) Safe Landing Joshua_(DS)_ (S) Quick Boot Joshua_(Remix)_ 10,000 Yen | 10,000 Yen |  
| Fight the Trance Rhino | 10,000 Yen Scarletite | 10,000 Yen |
Extra Rewards | Event | Reward |  
| --- | --- |  
| Clear the wall to Miyashita Park by winning the Tin Pin Slammer game against Tenho | Tin Pin Thrift |  
| Clear the wall to Miyashita Park by losing the Tin Pin Slammer game against Tenho | Secret Box_(Replay only)_ |  
| Beat Shooter at Tin Pin Slammer at the Stride | 500 Yen |  
| Beat Yammer at Tin Pin Slammer at the Stride | Tin Pin Hellfire |
Pig Drops | Species/Variety | Location | Reward |  
| --- | --- | --- |  
| Pig Carol/Ichimonji | West Exit Bus Terminal | Nikkari |  
| Pig Salsa/Countdown | Cat Street | Burning Melon |
Secret Box | Initial | Subsequent |  
| --- | --- |  
| Biker Gloves | 500 Yen |
</excerpt>
### Rank 3 of 55 — 0.67
<excerpt title="Secret Report Guide : r/TWEWY">
# The World Ends With You Final Remix - Secret Reports
        *   Black Book Bag (Move the Coin to Black in Reaper Creeper)

        *   Boss Symbol No. 89 (Concert Stage)

    *   Day 4 (Video Guide)

        *   Gakuran (Examine !!! in Miyashita Park Underpass)

    *   Day 5 (Video Guide)

        *   Pig Noise Symbols (AMX, Shibu Department Store, Towa Records, West Exit Bus Terminal)

        *   Head Honcho (Talk to the Reaper after the Reaper Battle in Shibu-Q Heads)

        *   Boss Symbol No 47 (Dogenzaka)

    *   Day 6 (Video Guide)

        *   Pig Noise Symbols (Station Underpass, Udagawa Back Streets)

        *   Lucky Mallet (Finish Day 3 without Reaper Creeper, enter Shadow Ramen in Day 6)

        *   Boss Symbol No 93 (Statue of Hachiko)

    *   Day 7 (Video Guide)

        *   Pig Noise Symbols (Miyashita Park)

        *   Samurai Helm (Enter Ramen Don in Dogenzaka)

        *   Boss Symbol No. 94 (Rubicon)
Read more
Share
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
Marie587
•8y ago
Can you **please** help me with Joshua, day 5??? I have tried to beat the bosses on hard mode plenty of times, and I can't do it no matter what I do. The girl's attack are impossible to miss, and I never was able to unlock the last two slots for my pins, and it's just been really hard for me. And no matter what I do, she always spam attacks me--am I supposed to be maxing out my stats or something?? Is there something crucial that I'm missing?? Please!!
Reply  Share
Underbuffed
•8y ago
The fight against Boss Symbol No. 82 & 84 is one of the hardest. You should have all 6 pin slots unlocked and enough bravery to wear good clothes. If you don't have that I suggest eat bravery increasing food and changing the date of the switch to the next day, so you can eat again. Also buy the missing 2 pin slots.
Reply  Share
Densten
•8y ago
Or you could just buy Hollow Leg from Shibu-Q Heads.
Reply  Share
Marie587
•8y ago
Ah shit, thank you so much. I was kinda dumb and during the main game play-through because I didn't realize that I could unlock more than 4 (since this was my first time playing). So now I'm having the worst time of my life in the post game unlocking the last two because the materials necessary for it are really hard to get.
Reply  Share
More replies
eoloskiks
•4mo ago
Her name is Uzuki
Reply  Share
More replies
TriforceofDoom
•8y ago
So I'm having trouble with the underpass pig in Beat 6. I am dealing single digits of damage & sometimes even zero. I'm guessing it's invulnerable to melee attacks after experimentation but I still can't deal enough damage.
Looni_bezdelnica
•2y ago
От всей души благодарю за тот гайд! и... можете пожалуйста помочь с секретным днем?
crustybones71
•2y ago
Thank you for this =)
Puzzleheaded-Idea931
•5y ago
Love you, thx guys
ceruleanhail
•4y ago
Thank you for the guide!

# Comments Section
Just wanna add for future players that Beat's Day 6 Pig Noise is missing 1 in Shibuya Dept Store from the list. Maybe the vid shows it, but I was following the list only and became baffled when the quest wasn't marked complete after visiting the 2 places.
</excerpt>
### Rank 4 of 55 — 0.59
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
### Rank 5 of 55 — 0.59
<excerpt title="Secret Report Guide : r/TWEWY">
# The World Ends With You Final Remix - Secret Reports
    *   Day 3 (Video Guide)

        *   Pig Noise Symbols (Tipsy Tose Hall, Miyashita Park Underpass)

        *   Pirate Hat (When searching for Ramen Imprints, talk to Tech in Concert Stage and check !!!)

        *   Boss Symbol No. 44 (Miyashita Park)

    *   Day 4 (Video Guide)

        *   Pig Noise Symbols (Molco)

        *   Samurai Wig (Wildcat in Cat Street, after taking photos in the phone booth)

    *   Day 5 (Video Guide)

        *   Pig Noise Symbols (Cat Street, West Exit Bus Terminal)

        *   Biker Gloves (Lose to the Reaper in Tin Pin Slammer)

        *   Boss Symbol No. 82 & 84 (Udagawa Backstreets)

    *   Day 6 (Video Guide)

        *   Pig Noise Symbols (Center St. Entrance, Shibu-Q Heads)

        *   Ninja Garb (Pick "Keep Moving" 3 times)

        *   Boss Symbol No. 22 (AMX)

    *   Day 7 (Video Guide)

        *   Pig Noise Symbols (A-East, Shibukyu Main Store)

        *   Boy's Uniform with Blazer (Enter Concert Stage and then try to exit)

        *   Boss Symbol No. 92 (Shibukyu Main Store)

*   Beat (Video Guide)

    *   Day 1 (Video Guide)

        *   Pig Noise Symbols (West Exit Bus Terminal, Station Underpass)

        *   Girls' Uniform with Blazer (Examine Statue of Hachiko)

        *   Boss Symbol No. 81 (West Exit Bus Terminal)

        *   Boss Symbol No. 83 (West Exit Bus Terminal)

    *   Day 2 (Video Guide)

        *   Pig Noise Symbols (Dogenzaka, Statue of Hachiko)

        *   False Teeth (Enter Cosmic Corner in Dogenzaka)

        *   Boss Symbol No. 66 (Scramble Crossing)

    *   Day 3 (Video Guide)

        *   Pig Noise Symbols (104 Building, 104 Building)

# The World Ends With You Final Remix - Secret Reports
        *   Black Book Bag (Move the Coin to Black in Reaper Creeper)

        *   Boss Symbol No. 89 (Concert Stage)

    *   Day 4 (Video Guide)

        *   Gakuran (Examine !!! in Miyashita Park Underpass)

    *   Day 5 (Video Guide)

        *   Pig Noise Symbols (AMX, Shibu Department Store, Towa Records, West Exit Bus Terminal)

        *   Head Honcho (Talk to the Reaper after the Reaper Battle in Shibu-Q Heads)

        *   Boss Symbol No 47 (Dogenzaka)

    *   Day 6 (Video Guide)

        *   Pig Noise Symbols (Station Underpass, Udagawa Back Streets)

        *   Lucky Mallet (Finish Day 3 without Reaper Creeper, enter Shadow Ramen in Day 6)

        *   Boss Symbol No 93 (Statue of Hachiko)

    *   Day 7 (Video Guide)

        *   Pig Noise Symbols (Miyashita Park)

        *   Samurai Helm (Enter Ramen Don in Dogenzaka)

        *   Boss Symbol No. 94 (Rubicon)
Read more
Share
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

## Search 5 — query: "Shiki Day 5 Secret Report Cornix Canor"
### Rank 1 of 127 — 0.94 (passed on)
<excerpt title="Secret Reports - The World Ends with You Wiki - Fandom">
## Obtaining the Reports[]
| Week and Day | Star 1 | Star 2 | Star 3 | Star 4 |  
| --- | --- | --- | --- | --- |  
| Shiki, Day 1 | After meeting Shiki and defeating the Noise, check Hachiko. |  |  |  |  
| Shiki, Day 2 | Obtain the Secret Report for Week 1, Day 1. Obvious, right? | Kill all of the pig noise. The pig indicator by your phone helps. | Talk to the statue loving guy next to the Moyai after clearing the wall. |  |  
| Shiki, Day 3 | Obtain the Secret Report for Week 1, Day 2. Obvious, right? | Kill all of the pig noise. The pig indicator by your phone helps. | After you learn how to imprint, head to Ramen Don in Dogenzaka to get the "ramen" meme. Imprint it on Futoshi and follow him. | Take down the Vespertillo Canor Blue Noise in the Concert Stage on either Hard or Ultimate Difficulty. |  
| Shiki, Day 4 | Kill all of the pig noise. The pig indicator by your phone helps. | Once Shiki says she wants to go into 104, try to leave instead. | Take down Shades' Blue Noise in the Scramble Crossing on Hard or Ultimate Difficulty. | Take down Beat's Blue Noise at 104 on Hard or Ultimate Difficulty. |  
| Shiki, Day 5 | Obtain the Secret Report for Week 1, Day 4. Obvious, right? | Kill all of the pig noise. The pig indicator by your phone helps. | When Mina and Ai play Reaper Creeper, move the coin to white for all three questions. | Take down the Cornix Canor Blue Noise at Molco on Hard or Ultimate Difficulty. |  
| Shiki, Day 6 | Obtain the Secret Report for Week 1, Day 5. Obvious, right? | Obtain the Secret Report for Week 1, Day 3. Obvious, right? | Kill all of the pig noise. The pig indicator by your phone helps. | When Makoto talks to Shooter in Center St. Entrance, imprint "Totally gnarly!" instead of "Unreal, bro!" |
</excerpt>
### Rank 2 of 127 — 0.93
<excerpt title="Secret Reports - The World Ends with You Wiki - Fandom">
Mr. Hanekoma, author of the Secret Reports.
The **Secret Reports** are records written by Sanae Hanekoma. They contain information that fill in many of the plot holes in _The World Ends With You_ and _NEO: The World Ends with You_.
To those who have not finished the games, they spoil major parts of the stories of both games. Players may wish to collect them in-game for the reward of reading them, as reading this article may disincentivize players from collecting them.
**Spoiler warning**: Plot and/or character details follow.

## The World Ends with You[]


## Obtaining the Reports[]
The Secret Reports can only be obtained after defeating Draco Cantus and unlocking the Chapters Menu. Each chapter's mark contains between one and four stars, which label the tasks to be completed before each report is unlocked. This list contains instructions on completing each of these tasks, as some of them are obscure.
Additionally, for Final Remix, Secret Report 21 cannot be accessed unless the player has unlocked A New Day. It is not necessary to begin or complete A New Day to read Secret Report 21, however.

## Obtaining the Reports[]
| Week and Day | Star 1 | Star 2 | Star 3 | Star 4 |  
| --- | --- | --- | --- | --- |  
| Shiki, Day 1 | After meeting Shiki and defeating the Noise, check Hachiko. |  |  |  |  
| Shiki, Day 2 | Obtain the Secret Report for Week 1, Day 1. Obvious, right? | Kill all of the pig noise. The pig indicator by your phone helps. | Talk to the statue loving guy next to the Moyai after clearing the wall. |  |  
| Shiki, Day 3 | Obtain the Secret Report for Week 1, Day 2. Obvious, right? | Kill all of the pig noise. The pig indicator by your phone helps. | After you learn how to imprint, head to Ramen Don in Dogenzaka to get the "ramen" meme. Imprint it on Futoshi and follow him. | Take down the Vespertillo Canor Blue Noise in the Concert Stage on either Hard or Ultimate Difficulty. |  
| Shiki, Day 4 | Kill all of the pig noise. The pig indicator by your phone helps. | Once Shiki says she wants to go into 104, try to leave instead. | Take down Shades' Blue Noise in the Scramble Crossing on Hard or Ultimate Difficulty. | Take down Beat's Blue Noise at 104 on Hard or Ultimate Difficulty. |  
| Shiki, Day 5 | Obtain the Secret Report for Week 1, Day 4. Obvious, right? | Kill all of the pig noise. The pig indicator by your phone helps. | When Mina and Ai play Reaper Creeper, move the coin to white for all three questions. | Take down the Cornix Canor Blue Noise at Molco on Hard or Ultimate Difficulty. |  
| Shiki, Day 6 | Obtain the Secret Report for Week 1, Day 5. Obvious, right? | Obtain the Secret Report for Week 1, Day 3. Obvious, right? | Kill all of the pig noise. The pig indicator by your phone helps. | When Makoto talks to Shooter in Center St. Entrance, imprint "Totally gnarly!" instead of "Unreal, bro!" |
</excerpt>
### Rank 3 of 127 — 0.87
<excerpt title="The World Ends With You - Secret Reports">
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
path. Come to Center St. Entrance, talk to Makoto or the kid, imprint Makoto
and choose "Totally gnarly" to obtain Solid Slammer.
#= Day 7
~Collect the report for Shiki, Day 6.
~Track down and eliminate all of this chapter's Pig Noise Symbols.
</excerpt>
### Rank 4 of 127 — 0.69
<excerpt title="The World Ends with You - Secret Report FAQ - DS - By CursedAnubis">
In other words, humans, Reapers, and Noise are all  
entities of formed of Soul. The only difference is their  
code.
And what are Noise? Entities without conscious will,  
only the drive to multiply. Thus, they constantly  
thirst for Soul, attacking Players and possessing  
humans in the Realground.
5/5
Soul consumed by Noise is destroyed, even if the  
Noise is erased.
Thus, possessed by humans often exhibit a rush of  
euphoria immediately after the Noise is removed.
Though untested, the same would likely hold were a  
Player or Reaper possessed.
--------------------------------------------
Secret Report 5 - Empty Urban Legends - SRS5|   
--------------------------------------------------------------------------  
Rhyme is caught in the Reapers' Trap and  
erased, leaving Neku and Shiki alone again...
Complete the Following to view this day's report:
Star 1: Collect the report for Shiki, Day 4.
Star 2: Track down and eliminate all of this chapter's Pig Noise symbols.
Star 3: Get Mr. Ducky.(White! White! White!)  
	As the hint may tell you, when playing Reaper Creeper with the  
	two girls, pick white three times, and it will be given to you.
Star 4: Eliminate the Boss symbol No. 90 within this chapter at hard or  
	above.  
	Molco; at the bottom-left corner of the area  
	-DO NOT DO CHAIN REDUCTION BATTLES-
Report Contents---------
1/6
The Realground and Underground are planes of   
existence. Other planes exist as well: the one  
inhabited solely by Noise, for example, or Our  
customary plane.
The planes are stacked in parallel, through each   
exists at a different frequency vibe, in tune with  
its inhabitants.
Observing a lower plane from a higher plane is simple.  
Actual trans-planar contact, while possible, is highly  
complex. The vibes of adjacent planes are closer,  
making passage between them comparatively easier.  
                                                                       2/6  
More distant planes show greater differences in vibe  
frequencies, and thus communion becomes more  
difficult.
</excerpt>
### Rank 5 of 127 — 0.65
<excerpt title="Cornix Canor - The World Ends with You Wiki - Fandom">
# Cornix Canor
Sign In to Save SaveEdit
*   History  
*   Purge  
*   Talk (0)

# Cornix Canor
## Cornix Canor
| ← Previous Noise | Next Noise → |  
| --- | --- |  
| Pteropus Canor | Ovis Cantus |

# Cornix Canor
## Cornix Canor
### nbr
90

# Cornix Canor
## Cornix Canor
### **Hit Points**
800

# Cornix Canor
## Cornix Canor
### **Attack**
100

# Cornix Canor
## Cornix Canor
### **PP**
20

# Cornix Canor
## Cornix Canor
### **EXP Gained**
0

# Cornix Canor
## Cornix Canor
### **Found**
W1D5: Molco (Blue Noise)  
W1D7: West Exit Bus Terminal (Boss)

# Cornix Canor
## Cornix Canor
### **Date(s) Encountered**
Week 1: Day 5 (Blue Noise)  
Week 1: Day 7 (Boss)

# Cornix Canor
## Cornix Canor
### **Resistance**
100% Positive
100% Negative

# Cornix Canor
## Cornix Canor
### **Pin Drops**
**U** - Brainy Cat (1.30%)
**H** - Cornix (1.00%)
**N** - Lovely Beam (5.00%)
**E** - Natural Magnum (5.00%)
_"Watch the shadow cast by this ruler of Noise ravens for a clue on when it'll attack!"_— Noise Report  
**Cornix Canor** is a BossNoise found in Week One of _The World Ends with You_.

# Cornix Canor
## Abilities[]
*   **Flight State**: Cornix Canor spends most of its time in flight above the fray. While in flight, it will not be visible on either screen, but its shadow will be visible crossing the bottom screen as it flys across. Each time it completes lap across the screen, it will descend closer and closer to the battle, eventually dropping in for a **Sweep**.  
*   **Sweep**: When it has descended low enough, it will appear on the bottom screen, sweeping from one side to the other and damaging Neku if it collides with him. Once gone on the bottom, it will do the same for the top screen. Once done sweeping, it will return back to **Flight State**.  
*   **Drag and Drop**: While doing a **Sweep**, Cornix may pick up and drag an obstacle off the screen. While Cornix is towing an obstacle, he will be slowed, giving Neku an opening to attack. After returning to **Flight State**, it will drop the object onto the bottom screen. The shadow of the obstacle will be visible to indicate where it will fall, inflicting damage to Neku if he is caught under it. Cornix will not drop obstacles onto the top screen.  
*   **Decadraven Minions**: Up to six Decadraven will be present on at all times during the fight. When one is erased, it will be momentarily be replaced by another.
</excerpt>

## Search 6 — query: "The World Ends with You partner nicknames list"
### Rank 1 of 219 — 0.72 (passed on)
<excerpt title="The World Ends with You">
The player controls Neku Sakuraba (桜庭 音操, _Sakuraba Neku_; ネク _Neku_), an initially asocial teenage boy who claims that he does not "get" people, and rarely interacts with others at first. Computer-controlled characters make up the rest of the cast, which includes players paired with Neku.[[11]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-Noise_zones-14) In the first Game, Neku is paired with Shiki Misaki (美咲 四季, _Misaki Shiki_; シキ _Shiki_), a teenage girl who takes on the form of her best friend, as her physical appearance was her price of entry for the Game.[[12]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-15) In the second Game, Neku's partner is an intelligent and sly teenage boy, Yoshiya Kiryu (桐生 義弥, _Kiryū Yoshiya_), who prefers to be called Joshua (ヨシュア, _Yoshua_). Neku's final partner is Daisukenojo Bito (尾藤 大輔之丞, _Bitō Daisukenojō_), originally a player and ex-Reaper who calls himself "Beat" (ビイト, _Biito_).[[13]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-16) Beat became a Reaper to find a way to bring his younger sister, Raimu Bito (尾藤 来夢, _Bitō Raimu_) (nicknamed "Rhyme" (ライム, _Raimu_)), back to life, as she had sacrificed herself to save him from a Noise attack.[[14]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-17)Sanae Hanekoma (羽狛 早苗, _Hanekoma Sanae_; ハネコマ _Hanekoma_), the Producer, bound her soul to a pin from which her Noise could be summoned, and gave it to Beat. The final Game Master, Mitsuki Konishi (虚西 充妃, _Konishi Mitsuki_; コニシ _Konishi_), crushes her Noise form and transforms it back into a pin.

Besides the Composer and the Conductor, there are other high-ranking Reapers.[[15]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-18) For each week of the Game, Game Masters are assigned by the Conductor to lead the opposition to the players. Of the Game Masters opposing Neku, Sho Minamimoto (南師 猩, _Minamimoto Shō_; ミナミモト _Minamimoto_) is the most dangerous, as he willingly circumvents the rules in an attempt to supplant the Composer.[[16]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-19) While participating in the Games to earn promotions for their performance, the Reapers' goal is to ascend to the highest form of spiritual existence, the Angels.[[17]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-20) Angels supervise the Games and, if the stakes of a Game are particularly high, they send down one of their own to serve as the Producer.[[18]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-21) For the three weeks of the game's story, Sanae Hanekoma is the Producer. Disguised as a Shibuya café owner, he guides new players and narrates the "Secret Reports", which are obtained by completing additional missions after completing the game.
</excerpt>
### Rank 2 of 219 — 0.70
<excerpt title="The World Ends with You (Video Game)">
# - E
*   Once More, with Clarity: The game does this _three times_ with the same sequence  of Neku's death. First, Neku ends up scanning Joshua's mind, which normally shouldn't be possible, and ends up seeing his dead body in his mind. When he scans Joshua again, we see a sequence where Joshua appears to shoot Neku. Then on the final day, the presence of Joshua and Minamimoto in the same area makes him remember the same sequence of events, only this time, it's revealed that Joshua was aiming for Minamimoto, who was right behind Neku, and it appears that Minamimoto was the one who shot Neku, and _then_ during the ending, Joshua restores the full memory, where it's revealed that Minamimoto was aiming for Joshua, but failed due to Joshua still having some of his powers, causing Minamimoto to flee. Then, Joshua _definitely_ kills Neku and leaves him with his extra Player pin.  
*   One Size Fits All: Once you can get your character's Bravery stat high enough, you can get them to wear all sorts of clothes that are smaller than the characters.  
*   One-Winged Angel: Every Game Master and Hanekoma start their boss battles by morphing into their Cantus forms. The Final Boss does it twice.  You beat Kitaniji in his human form, then he assumes his Noise form, only for Joshua to arrive after he's beaten, giving Kitaniji the idea to use Joshua to give his One Winged Angel form its own One Winged Angel: Draco Cantus.  
*   Only Known by Their Nickname: The entire cast, though, admittedly, some more than others. Justified in some cases, as Neku and his partner are usually never formally introduced to the GM or other reapers, and thus actually don't know their names.  
    *    Neku Sakuraba - Phones  
    *    Yoshiya Kiryu - Joshua, Josh, J  
    *    Daisukenojo Bito - Beat, Skulls, Freshmeat  
    *   Raimu Bito - Rhyme, Skulls Jr.  
    *    Uzuki Yashiro - Pinky  
    *    Koki Kariya - Lollipop  
    *    Yodai Higashizawa - Big Guy, Ram-Crotch  

# - E
    *    Sho Minamimoto - Pi-Face, The Grim Heaper  
    *    Mitsuki Konishi - Iron Maiden and several variations thereof.  
    *    Megumi Kitaniji - Shades  
    *    Sanae Hanekoma - Mr. H  
    *    CAT (Mr. Hanekoma), Piggy (Mr. Mew), Nao-Nao, Makoto "Mick" Miki, Shuuto "Shooter" Dan, Itaru "Yammer" Yokoyamada, and Eiji "The Prince" Oji.  
    *    And then there's Another Day, in which the main cast all get themselves color codenames. Neku doesn't ever get to actually introduce himself.
</excerpt>
### Rank 3 of 219 — 0.66
<excerpt title="The World Ends with You">
A player in the UG is invisible to the living in the RG, though one can sometimes read and influence their thoughts. The UG is frequented by creatures called "Noise", which are attracted by the negative feelings of the living. To progress in the Reapers' Game, players are often required to defeat Noise by killing or "erasing" them.[[4]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-ign_review-7) However, each Noise exists in two parallel universes, or "zones", simultaneously, and can only be defeated by two players simultaneously fighting and defeating the Noise from these separate zones. To do so, players are required to form a pact with another player to survive the Noise.[[11]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-Noise_zones-14) Players receive assignments via text messages sent to their cell phones, and their right hands are imprinted with a countdown indicating the time left in the mission.[[4]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-ign_review-7) After a day's mission is complete, the remaining players find themselves at the start of the next day's mission, having no sense of the time that has passed in between.

The player controls Neku Sakuraba (桜庭 音操, _Sakuraba Neku_; ネク _Neku_), an initially asocial teenage boy who claims that he does not "get" people, and rarely interacts with others at first. Computer-controlled characters make up the rest of the cast, which includes players paired with Neku.[[11]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-Noise_zones-14) In the first Game, Neku is paired with Shiki Misaki (美咲 四季, _Misaki Shiki_; シキ _Shiki_), a teenage girl who takes on the form of her best friend, as her physical appearance was her price of entry for the Game.[[12]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-15) In the second Game, Neku's partner is an intelligent and sly teenage boy, Yoshiya Kiryu (桐生 義弥, _Kiryū Yoshiya_), who prefers to be called Joshua (ヨシュア, _Yoshua_). Neku's final partner is Daisukenojo Bito (尾藤 大輔之丞, _Bitō Daisukenojō_), originally a player and ex-Reaper who calls himself "Beat" (ビイト, _Biito_).[[13]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-16) Beat became a Reaper to find a way to bring his younger sister, Raimu Bito (尾藤 来夢, _Bitō Raimu_) (nicknamed "Rhyme" (ライム, _Raimu_)), back to life, as she had sacrificed herself to save him from a Noise attack.[[14]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-17)Sanae Hanekoma (羽狛 早苗, _Hanekoma Sanae_; ハネコマ _Hanekoma_), the Producer, bound her soul to a pin from which her Noise could be summoned, and gave it to Beat. The final Game Master, Mitsuki Konishi (虚西 充妃, _Konishi Mitsuki_; コニシ _Konishi_), crushes her Noise form and transforms it back into a pin.
</excerpt>
### Rank 4 of 219 — 0.64
<excerpt title="The World Ends with You (Video Game)">
# - E
    *    Sho Minamimoto - Pi-Face, The Grim Heaper  
    *    Mitsuki Konishi - Iron Maiden and several variations thereof.  
    *    Megumi Kitaniji - Shades  
    *    Sanae Hanekoma - Mr. H  
    *    CAT (Mr. Hanekoma), Piggy (Mr. Mew), Nao-Nao, Makoto "Mick" Miki, Shuuto "Shooter" Dan, Itaru "Yammer" Yokoyamada, and Eiji "The Prince" Oji.  
    *    And then there's Another Day, in which the main cast all get themselves color codenames. Neku doesn't ever get to actually introduce himself.

# - E
*   Only One Save File: The game only has a single save file, and attempting to start a New Game from the title screen will instead ask the player to erase the existing save data if there's one already present. It will warn the player at least three times before starting a new game if a save file is already present.  
*   Ontological Mystery: One of your objectives in the first week is to figure out just how you ended up waking up in the middle of the Scramble.  
*   Our Angels Are Different: They run the Game too, and are even higher in status than the Composer, but they're generally more like rule keepers that watch from the sidelines than anything else. (Hanekoma's one of them.)  
*   Our Dark Matter Is Mysterious: There is a metal crafting pin called Dark Matter, inlaid with gemstones made of the eponymous substance. It can be crafted at certain shops or dropped by certain bosses on Ultimate difficulty.  
*   Our Dragons Are Different: The game's final boss, Draco Cantus, is a snake-like dragon Noise form of Kitaniji, evolving from his Anguis Cantus form after he absorbed Joshua's powers.  
*   Our Souls Are Different: People can be erased, but as it turns out, souls are immortal, so they're not gone for good. If taken and reshaped by a strong enough outside source, they can even come back to life, in their own form or as something else.  
*   Our Wyverns Are Different: The Drake Noise are huge wyverns that are mostly made graffiti/tattoo-like heads, horns, spines, appendages, and tails with cross patterns on their wings. They are some of the toughest enemies in the game as they capable of breathing a barrage of bullets, charge at the player at high-speeds, slash them with their wings, and whip their tails at the Players.  
*   Out-of-Character Alert: Seeing the characters act grossly out of character is a major red flag that something is seriously wrong in "A New Day"; Uzuki is a Lazy Bum, Kariya is the ruthlessly ambitious one, and Joshua is a stammering Shrinking Violet who always goes by his full name.  
*   Outside-the-Box Tactic:  
    *    The Elephant Noise and both forms of the final boss can be defeated easily in a matter of seconds with the Time Bomb psych.
</excerpt>
### Rank 5 of 219 — 0.60
<excerpt title="The World Ends with You (Video Game)">
# - E
*   Gameplay Automation: If controlling Neku and the partner at the same time appears too difficult, you have the option of allowing the AI to take over the partner's controls after a set period of time at the expense of the AI being slower than the player and suffering from some Artificial Stupidity. You also get a free PP multiplier for not using it.  
*   Gameplay Grading: After each battle, your performance is ranked based on number of reductions, time, damage taken, and how many "special" bonuses you achieved (such as combos, puck passes/cross combos, having autoplay disabled, failing to get any pin drops, only using one character...), and these are combined into an overall rank. The overall rank itself doesn't mean anything, but the components give a multiplier to the PP earned, so if you're grinding your pins, you're gonna want to aim for ★ ranks anyway.  
*   Gender-Blender Name: Shiki, Makoto, Sanae, and Kitanji, the last of whom was apparently teased as a child for being named Megumi. Might explain a lot of things.  
*   Generic Graffiti:  
    *    Inverted, as the game's graffiti is mostly CAT's doing with only a few generic tags appearing, and none of it is specifically relevant to the story. Except for the bit where Neku was killed (thus becoming the Composers's proxy) because he was standing admiring CAT's mural.  
    *   It's revealed in the secret reports that CAT's murals attract those with a lot of imagination, and this was the reason why Joshua selected Neku (amongst other reasons) to be his proxy.

# - E
*   Genre-Busting: Although it's commonly classified as an Action RPG, the combat system, particularly on the bottom screen, is quite reminiscent of belt-scrolling Beat 'em Ups with Stylish Action elements that incentivizes skillful play and creative use of your pins. The pins themselves, although are attacks that the player can use in Neku's repertoire instead of creatures, are similar to a mon series with hundreds of pins to collect, evolve, and master.  
*   Geometric Magic: Calling forth Taboo Noise is done creating a circular refinery sigil with graffiti. Minamimoto creates one as a fallback plan if he gets erased by the Players, which allowed him to be resurrected as a Taboo Noise during Week 3.  
*   "Get Back Here!" Boss: Several of the bosses like to teleport, such as Uzuki and Reaper Beat, as well as Taboo Minamimoto. Cornix Canor also has a tendency to stay offscreen for 90% of the battle, only flying by every once in a while.  
*   Giant Enemy Crab: Inverted. Although the Carcin Noise are not gigantic in scale, but they are still larger than average crustaceans and, depending on the Carcin type, they are also capable of using their pincers to pinch or jab Players, throw them, block incoming attacks, or weaponize their boomerang-like pincer.  
*   Glass Cannon: Beat. Even if his attack and defense stats are equal with Shiki's or Joshua's, he'll still give and receive more damage than them, respectively. His Fusion, which can potentially charge up the fastest, also has the potential to damage him if you screw up.  
*   The Glasses Come Off: Konishi starts her transformation into Tigris Cantus by removing her glasses and staring cruelly at the screen.  
*   Glowing Eyes of Doom: When everyone in Shibuya is possessed by the O-pins, their eyes glow red.  
*   God Was My Co-Pilot: Joshua, Neku's partner for the second week, is the Composer. Also Mr. Hanekoma, who's actually even _higher_ rank than Josh.
</excerpt>

## Search 7 — query: "Shiki day 5 boss Cornix"
### Rank 1 of 106 — 0.85 (passed on)
<excerpt title="Noise List by Day and Location - The World Ends with You Wiki - Fandom">
The following is a list of where **Noise** can be found by day and location. For a list of information about individual Noise, please see the Noise Report.

## Week 1[]
### Shiki, Day 1[]
| No. | Noise | Noise symbols | Location |  
| --- | --- | --- | --- |  
| 01 | Dixiefrog | N/A | Scramble Crossing (Event), Statue of Hachiko (Event), 104 Building (Event) |  
| 15 | Mosh Grizzly | N/A | 104 Building (Event) |

## Week 1[]
### Shiki, Day 2[]
| No. | Noise | Noise symbols | Location |  
| --- | --- | --- | --- |  
| 01 | Dixiefrog |  | Station Underpass, West Exit Bus Terminal |  
| 12 | Garage Wolf |  | West Exit Bus Terminal, Statue of Hachiko (Event) |  
| 18 | Gabba Bat |  | Station Underpass |  
| 37 | Metal Corehog | N/A | Statue of Hachiko (Boss) |

## Week 1[]
### Shiki, Day 3[]
| No. | Noise | Noise symbols | Location |  
| --- | --- | --- | --- |  
| 01 | Dixiefrog |  | A-East, Shibukyu Main Store |  
| 12 | Garage Wolf |  | A-East, Dogenzaka |  
| 15 | Mosh Grizzly |  | A-East, Dogenzaka, Shibukyu Main Store |  
| 18 | Gabba Bat |  | A-East |  
| 88 | Vespertilio Canor |  | Concert Stage (Boss), Concert Stage (Postgame) |

## Week 1[]
### Shiki, Day 4[]
| No. | Noise | Noise symbols | Location |  
| --- | --- | --- | --- |  
| 01 | Dixiefrog |  | 104 Building, Scramble Crossing, Shibu Dept. Store, Cadoi City, Towa Records (Event) |  
| 02 | Bigbanfrog |  | 104 Building, Scramble Crossing, Shibu Dept. Store, Cadoi City, Towa Records (Event) |  
| 10 | Bigbansprog |  | Spawns with Bigbanfrog |  
| 12 | Garage Wolf |  | 104 Building, Scramble Crossing |  
| 15 | Mosh Grizzly |  | 104 Building, Scramble Crossing, Shibu Dept. Store, Cadoi City |  
| 61 | Swing Shark | N/A | Towa Records (Boss) |  
| 80 | Reaper Beat |  | 104 Building (Postgame) |  
| 87 | Megumi Kitaniji |  | Scramble Crossing (Postgame) |

## Week 1[]
### Shiki, Day 5[]
| No. | Noise | Noise symbols | Location |  
| --- | --- | --- | --- |  
| 01 | Dixiefrog |  | AMX |  
| 02 | Bigbanfrog |  | Tipsy Tose Hall, AMX, Spain Hill, Molco |  
| 10 | Bigbansprog |  | Spawns with Bigbanfrog |  
| 12 | Garage Wolf |  | Tipsy Tose Hall, AMX, Spain Hill, Molco |  
| 15 | Mosh Grizzly |  | Tipsy Tose Hall, AMX, Spain Hill, Molco |  
| 16 | Circle Pit Grizzly | N/A | Spain Hill (Boss) |  
| 33 | Hard Corehog |  | Tipsy Tose Hall, Spain Hill, Molco |  
| 90 | Cornix Canor |  | Molco (Postgame) |
</excerpt>
### Rank 2 of 106 — 0.83
<excerpt title="TWEWY Boss Noise Symbols Guide - The Candid Gamer">
## Week 1
### Week 1, Day 4
**No. 80: Reaper Beat**
**Location:** 104 Building
At the start of this day, Neku and the gang awaken at the 104 Building. **Towards the left of the area,** a scan will reveal Boss Noise Symbol No. 80 (a good source of **_Dark Matter_** on _Ultimate_ difficulty,) along the top left portion of the 104 Building’s ad screen.
**Items and Drop Rate**:
**Ultimate**: Dark Matter – 0.50%
**Hard**: I Live for Food – 10.00%
**Normal**: I Live for Food – 5.00%
**Easy**: Wild Boar – 5.00%
**No. 87: Megumi Kitaniji**
**Location:** Scramble Crossing
To get to the scramble crossing, you’ll have to talk to Beat and Rhyme, and talk with Shiki about shopping, trends, and Mr. Mew. Afterwards, you are free to leave without Shiki yelling to go shopping.
**Boss Noise Symbol No. 87 can found at the bottom of the center of the Scramble Crossing.**
**Items and Drop Rate**:
**Ultimate**: Black Uranus – 0.13%
**Hard**: Me Time is Free Time – 5.00%
**Normal**: Mitama – 10.00%
**Easy**: Mitama – 5.00%
* * *

## Week 1
### Week 1, Day 5
**No. 90: Cornix Canor**
**Location:** Molco
Starting at Tipsy Tose Hall, the reaper blocking the way to Spain Hill wants you to defeat two of the largest Noise Symbols in the area. Leaving the area and returning is not penalized.
Once the way to Spain Hill has been opened, a black-hooded reaper at the top of the area wants you to bring them **_(CD) Track 1 — “Underground”_**.
After this wall has been opened, near the bottom of the newly accessible Molco, the Boss Noise symbol can be found **on a billboard to the left.**
**Items and Drop Rate**:
**Ultimate**: Brainy Cat – 1.30%
**Hard**: Cornix – 1.00%
**Normal**: Lovely Beam – 5.00%
**Easy**: Natural Magnum – 5.00%
* * *

## Week 1
### Week 1, Day 7
**No. 91: Ovis Cantus**
**Location:** Station Underpass
Finding the Boss Noise here requires following chapter progression as normal.
From the Scramble Crossing, head for the Statue of Hachicko, fight in a 3-chain reduction in any area to appease the reaper, pass through the West Exit Bus Terminal, and into the Station Underpass.
The large boss noise symbol can be scanned for **near the end of the Station Underpass.**
**Items and Drop Rate**:
**Ultimate**: Stalwart as the Mount – 0.13%
**Hard**: Ovis – 0.44%
**Normal**: 10,000 Yen – 20.00%
**Easy**: 5,000 Yen – 20.00%
* * *

## Week 2
Week 2 is notable for providing backstory on the Game, and learning some of it in a behind-the-scenes way.
There are 5 boss symbols in the second week: **No. 86**, **No. 44**, **No. 82 and 84** (treated as one symbol), **No. 22**, and **No. 92**.
</excerpt>
### Rank 3 of 106 — 0.79
<excerpt title="Empty Urban Legends (Week 1, Day 5) | The World Ends With You | Fandom">
## Walkthrough[]
After the opening scene, move to the right where a businessman in a black suit stands. He’ll play Reaper Creeper; move the coin to any of the three spots, as the choice won’t mean much in particular. Remember to do it slowly as if the coin moves too fast, the man will believe he bumped the paper and retry. After playing, Neku and Shiki will receive the meme “Reaper Creeper”. The route to Spain Hill is blocked by a Reaper who will only put the wall down when two of the biggest Noise symbols are defeated. After fighting them, the Reaper will clear the route.At Spain Hill, fight some noise until Neku and Shiki talk about how the Noise won’t stop coming and the source is revealed to be two girls, Mina and Ai. Scan them and erase some of the orange Noise surrounding them. After the fight, talk to them and imprint “Reaper Creeper” on Ai. She’ll play Reaper Creeper with Mina; there’s no benefit to any of the choices over each other, but choosing White for all questions will get Mr. Ducky, needed for the post-game’s Secret Report. After the conversation ends and Ai and Mina make up, finish off the last Noise in the area.When the final Noise is erased, a Circle Pit Grizzly will attack. Defeat it to finish the chapter.

## Noise[]
| No. | Noise | Pic. | Location |  
| --- | --- | --- | --- |  
| 01 | Dixiefrog |  | AMX |  
| 02 | Bigbanfrog |  | Tipsy Tose Hall, AMX, Spain Hill, Molco |  
| 10 | Bigbansprog |  | Tipsy Tose Hall, AMX, Spain Hill, Molco |  
| 12 | Garage Wolf |  | Tipsy Tose Hall, AMX, Spain Hill, Molco |  
| 15 | Mosh Grizzly |  | Tipsy Tose Hall, AMX, Spain Hill, Molco |  
| 16 | Circle Pit Grizzly |  | Spain Hill (Boss) |  
| 33 | Hard Corehog |  | Tipsy Tose Hall, Spain Hill, Molco |  
| 90 | Cornix Canor |  | Molco (Blue Noise) (Postgame) |

## Rewards[]
Main Story Rewards | Event | First Playthrough | Subsequent |  
| --- | --- | --- |  
| Play Reaper Creeper with "Shrimp" | "Reaper Creeper" meme | "Reaper Creeper" meme |  
| Clear wall to Spain Hill | Murasame Durable Leather 10,000 Yen | Murasame Durable Leather 10,000 Yen |  
| Erase 3 or more Chump Noise symbols at Spain Hill | (S) Block Shiki_(DS)_ (S) Gauge Extender Shiki_(Remix)_ 1,000 Yen | 1,000 Yen |  
| Erase final Negative Noise possessing Ai and Mina | (S) DEF Boost Shiki | 500 Yen |  
| Defeat the Circle Pit Grizzly | (S) ATK Boost Shiki (S) Retry Battles Bngh D Scarletite | Bngh D |
Extra Rewards | Event | Reward |  
| --- | --- |  
| Erase Negative Noise possessing Makoto | 5,000 Yen "Tin Pin ticket" meme |  
| Clear wall to Molco | 1,000 Yen Crimson Chili |  
| Choose "white" all 3 times during Reaper Creeper | Secret Box_(Replay only)_ |
Pig Drops | Species | Location | Reward |  
| --- | --- | --- |  
| Pig Samba | AMX | Rare Metal |  
| Pig Cha-cha | Molco | 5,000 Yen |
Secret Box | Initial | Subsequent |  
| --- | --- |  
| Mr. Ducky | 500 Yen |
</excerpt>
### Rank 4 of 106 — 0.77
<excerpt title="Noise List by Day and Location - The World Ends with You Wiki - Fandom">
## Week 1[]
### Shiki, Day 5[]
| No. | Noise | Noise symbols | Location |  
| --- | --- | --- | --- |  
| 01 | Dixiefrog |  | AMX |  
| 02 | Bigbanfrog |  | Tipsy Tose Hall, AMX, Spain Hill, Molco |  
| 10 | Bigbansprog |  | Spawns with Bigbanfrog |  
| 12 | Garage Wolf |  | Tipsy Tose Hall, AMX, Spain Hill, Molco |  
| 15 | Mosh Grizzly |  | Tipsy Tose Hall, AMX, Spain Hill, Molco |  
| 16 | Circle Pit Grizzly | N/A | Spain Hill (Boss) |  
| 33 | Hard Corehog |  | Tipsy Tose Hall, Spain Hill, Molco |  
| 90 | Cornix Canor |  | Molco (Postgame) |

## Week 1[]
### Shiki, Day 6[]
| No. | Noise | Noise symbols | Location |  
| --- | --- | --- | --- |  
| 02 | Bigbanfrog |  | Every Map |  
| 10 | Bigbansprog |  | Spawns with Bigbanfrog |  
| 12 | Garage Wolf |  | Scramble Crossing, 104 Building, Towa Records, Spain Hill, AMX |  
| 15 | Mosh Grizzly |  | 104 Building, Cadoi City, Towa Records, Molco, Spain Hill, Tipsy Tose Hall, AMX |  
| 33 | Hard Corehog |  | Scramble Crossing, Towa Records, Molco, Spain Hill, Tipsy Tose Hall, Center St. Entrance |  
| 58 | Decadraven |  | Scramble Crossing, Shibu Dept. Store, Cadoi City, Towa Records, Tipsy Tose Hall, Center St. Entrance |

## Week 1[]
### Shiki, Day 7[]
| No. | Noise | Noise symbols | Location |  
| --- | --- | --- | --- |  
| 02 | Bigbanfrog |  | Scramble Crossing, 104 Building, Shibu Dept. Store, Cadoi City, Towa Records, Molco, Spain Hill, AMX, Center St. Entrance, Statue of Hachiko, West Exit Bus Terminal |  
| 10 | Bigbansprog |  | Spawns with Bigbanfrog |  
| 12 | Garage Wolf |  | 104 Building, Spain Hill, Statue of Hachiko |  
| 15 | Mosh Grizzly |  | Scramble Crossing, 104 Building, Shibu Dept. Store, Cadoi City, Molco, Spain Hill, Tipsy Tose Hall, AMX, Statue of Hachiko |  
| 16 | Circle Pit Grizzly |  | Statue of Hachiko (_Final Remix_ Optional Boss) |  
| 18 | Gabba Bat |  | Station Underpass |  
| 26 | J Popguin |  | Scramble Crossing, 104 Building, Cadoi City, Towa Records, Molco, Spain Hill, AMX, Statue of Hachiko |  
| 33 | Hard Corehog |  | Scramble Crossing, Towa Records, Molco, Spain Hill, Tipsy Tose Hall, Center St. Entrance, West Exit Bus Terminal |  
| 35 | Melodi Corehog |  | Statue of Hachiko (_Final Remix_ only) |  
| 58 | Decadraven |  | Scramble Crossing, Shibu Dept. Store, Cadoi City, Towa Records, Tipsy Tose Hall, Center St. Entrance, West Exit Bus Terminal |  
| 90 | Cornix Canor | N/A | West Exit Bus Terminal (Boss) |  
| 91 | Ovis Cantus |  | Station Underpass (Boss), Station Underpass (Postgame) |
</excerpt>
### Rank 5 of 106 — 0.77
<excerpt title="The World Ends with You - Boss Guide - DS - By cyborg99sreturn">
==============================================================================
Week 1 (WEEK1)
==============================================================================
Week 1, Day 5, Boss 1 (W1D5B1):   
Circle Pit Grizzly - Difficulty 6/10; Annoyance Factor 2/10  
HP: 3500  
Attack: 150  
No weaknesses or resistances.  
PP: 15  
No EXP earned.
Attacks:  
Backhand - backhands Neku or his partner. No knockdown, but causes Neku to   
flinch if hit.  
Swipe - swipes with huge claw to attack Neku or his partner. Knocks down if   
deals damage. Can toss obstacles with it.  
Grizzly Slam - raises a claw and jumps into the air, damaging Neku, then lands   
on the ground, causing a shockwave. First hit causes less damage than Swipe(a   
little more than half) while the shockwave deals extremely heavy damage(twice   
as strong as Swipe).
Strategy:   
Play defensively and attack from range. Use a Psychokinesis pin to attack with  
the obstacles first so they'll break and he can't hit you with Swipe from   
range.  
Circle Pit Grizzly is oddly aggressive for a Noise and attacks extremely fast   
with a lot of power. If you think you can manage it, juggle it with your Ice   
Blow/Risers, Murasame(or it's evolutions) that you just got, and Force Rounds.  
Ice Blow/Risers > Murasame > Force Rounds > Ice Blow/Risers should keep him in  
the air and you unharmed. Otherwise, just stay at range and blast it from a   
far. Don't forget to block with Shiki when you see it start to attack.
Week 1, Day 7, Boss 1 (W1D7B1):  
Cornix Canor - Difficulty 2/10; Annoyance Factor 8/10   
HP: 800  
Attack: 100  
No weaknesses or resistances.  
PP: 20  
No EXP earned.

==============================================================================
Week 1 (WEEK1)
==============================================================================
Attacks:  
Summon Decadravens - All throughout the fight if there are not 4 Decadravens   
in the battle, they will be constantly summoned. Thankfully they don't try to   
steal your pins. Just like the other Canor, these minions do not drop Pins and  
assumingly no EXP/PP.  
Dive - If it's not carrying something, it will fly back and forth on the   
bottom Zone(you can see it's shadow). When it gets to the ground, it will make  
a screech and it will either dive from one side of the screen to the other,   
picking an obstacle(even one of the bigass Buses from time to time O_O) up on   
the way. It will then move to the top Zone and dive the opposite way. To make   
it drop what it is carrying, simply hit it once with Shiki.  
Drop - If you don't hit it when it's on the top Zone, it flies back down to   
the bottom Zone. You'll once again see its shadow, along with the shadow of   
the thing it's carrying. Obviously bigger obstacles mean bigger shadows. It   
will fly in the sky back and forth a few times until it decides to drop it on   
Neku. Dodge this by simply moving out of the way. Beware of dropped Cars,   
Vans, and Buses!
</excerpt>

# Example 2
## Question
What beach in Florida allows for alcohol consumption year-round, except in the month of March?

## Expected answer
Panama City Beach

## Grade 1.00

## Search 1 — query: "Florida beach alcohol allowed year round except March"
### Rank 1 of 22 — 0.98 (passed on)
<excerpt title="Spring break 2025 and Florida beaches you can, can't bring alcohol">
## Which Florida beaches allow alcohol during spring break months?
*   **Panama City Beach:**Alcoholic beverages are permitted year-round, except for March.  
*   **Pensacola Beach:**Alcoholic beverages are permitted on the beach, omitting an alcohol-free zone located on a “... portion of the beach on the Gulf of Mexico on Pensacola Beach extending 320 feet west of the existing Pensacola Beach Gulf Pier and 225 feet north of the shoreline to the sand fencing, encompassing an area approximately 1.75 acres” (Escambia County, Code of Ordinance, Chapter 6, Sec. 6-3. - Alcohol-free zone).

## Can I consume alcohol in Florida State Parks?
![Image 2: Joe Wallace cruises the Silver River in Silver Springs, FL on Friday, February 14, 2025. The five-mile river, which is part of the 4000 acre Silver Springs State Park, offers visitors a look at natural Florida by canoe, boat or glass bottom boat from the headwater. The park has no development and doesn’t allow swimming or access to the banks. Boating is at idle speed only. The State Park system has had control of the former attraction since 2013 and has worked to return it to a natural state. The park is open is open from 8 a.m to sunset every day of the year. Canoes and kayaks can be launched from the head water but boat access is from Ray Wayside Park near the Ocklawaha river Bridge only. [Alan Youngblood/Ocala Star-Banner]](https://www.newsherald.com/gcdn/authoring/authoring-images/2025/02/20/NOSB/79345747007-a-34-i-9922-1.jpg?width=660&height=435&fit=crop&format=pjpg&auto=webp)  
For those wanting to ditch the crowds and head to a state park beach, keep in mind you'll have to ditch the alcoholic drinks.
Alcoholic consumption is alsonot permitted in public locationswithin any of the Florida state parks, including beaches, tubing/paddling areas, or first-come first-served picnicking areas. It is allowed in reserved overnight accommodations and covered picnic pavilions.

## Where else is alcohol banned on Florida beaches during Spring Break?
Heads up for those heading to Panama City Beach for spring break — residents have already experienced a ban on booze in March for nine years.
According to the city's ordinances, alcoholic beverages are not permitted on the beach during the popular spring break month. Enforced back in 2016, the ban was put in place after seeing[years of unruly crowds and upticks in violence](https://www.newsherald.com/story/news/local/2023/03/09/panama-city-beach-residents-not-exempt-from-marchs-beach-alcohol-ban/69982785007/#:~:text=He%20noted%20that%20officials%20approved,in%20crime%20throughout%20the%20city.).
In addition to no alcohol on the sandy beaches,the rules also include:
*   No alcohol sales between 2 a.m. and 7 a.m.  
*   No consumption of alcohol on the right of way or in parking lots  
*   No loitering in parking lots or on the shoulder of the road  
*   No parking on the right of way in scenic corridors after sunset  
*   No metal shovels and no holes may be dug deeper than two feet on the sandy beach  
*   No glass on the beach  
*   City noise ordinances will be strictly enforced  
*   People must also heed to double red flags warning and must not leave any trash behind.
_Contributing reporting: C. A. Bridges, USA TODAY NETWORK - Florida_
</excerpt>
### Rank 2 of 22 — 0.98
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
### Rank 3 of 22 — 0.98
<excerpt title="Spring break 2025 and Florida beaches you can, can't bring alcohol">
Feb. 24, 2025, 3:01 p.m. ET
*   Several Florida beaches, primarily on the East and West Coasts, allow alcohol consumption with some restrictions.  
*   Alcohol is not permitted in public areas of Florida state parks, including beaches.
Once again, Miami Beach is cracking down on spring break chaos, but what about Panama City beaches?
After its viral "break up with Spring Break" campaign last year, city officials are letting visitors know they won't tolerate "disorderly crowds, lawless behavior and violence" this season.
Ahead of this year's crowd, they released another video titled "Spring Break Reality Check Miami Beach," which features spring breakers in a mock reality show. The video details the city's DUI sobriety checkpoints, the $100 parking and the curfew.
Do all Florida beaches have legislation similar to Miami Beach regarding spring break and consuming alcohol on the beach? Here's what to know before you pack your cooler and head out on your vacation.

## What are Florida's laws regarding alcoholic beverages in public?
According to Florida's Open Container laws,the public consumption of alcohol is generally prohibited, which includes spaces such as parks, streets, or even beaches. Depending on where you are, you can be cited for possessing an open alcoholic beverage while in public.
However,[Florida law firm HP Defenders](https://www.hpdefenders.com/blog/can-you-drink-alcohol-on-florida-beaches/#:~:text=So%2C%20can%20you%20drink%20alcohol,designated%20areas%20on%20certain%20beaches.)writes that exceptions do exist, with certain beaches having designated areas where alcohol consumption is allowed.

## Which Florida beaches allow alcohol during spring break months?
ABC Winesshared a list of where you can bring booze on your beach day (responsibly!) and their restrictions:
**East Coast Beaches**
*   **Flagler Beach:**Alcoholic beverages are permitted on the beach.  
*   **Cocoa Beach:**Alcoholic beverages are permitted on the beach.  
*   **Playalinda Beach:**Alcoholic beverages are permitted on the beach.
**West Coast Beaches**
*   **Madeira Beach:**Alcoholic beverages are permitted on the beach; just not in glass containers.  
*   **St. Pete Beach:**Alcoholic beverages are allowed on the sand at beachfront hotels, but this is limited to hotel guests.  
*   **Treasure Island:**Alcoholic beverages are allowed but only in non-glass containers. It is also not allowed on the beach between the 8500 block and the 9900 block of Treasure Island Beach between 8 a.m. and 4 p.m. on Saturdays and Sundays.  
*   **Redington Beach:**Alcoholic beverages are permitted on the beach. Please note that alcohol is**not**permitted on the neighboring (and similarly named) beaches of Redington Shores and North Redington Beach.  
*   **Siesta Beach:**Alcoholic beverages are permitted on the beach; just no glass containers.  
*   **Turtle Beach:**Alcoholic beverages are permitted on the beach; just no glass containers  
*   **Lido Beach:**Alcoholic beverages are permitted on the beach; just no glass containers  
*   **Naples Municipal Beach:**Alcoholic beverages are permitted on the beach; however, they are not permitted on the pier (except beer and wine between noon and one hour past sunset). Please note that alcohol is not permitted one block north and one block south of the pier on 12th Avenue, 13th Avenue and Broad Avenue South.
**Panhandle Beaches**

## Which Florida beaches allow alcohol during spring break months?
*   **Panama City Beach:**Alcoholic beverages are permitted year-round, except for March.  
*   **Pensacola Beach:**Alcoholic beverages are permitted on the beach, omitting an alcohol-free zone located on a “... portion of the beach on the Gulf of Mexico on Pensacola Beach extending 320 feet west of the existing Pensacola Beach Gulf Pier and 225 feet north of the shoreline to the sand fencing, encompassing an area approximately 1.75 acres” (Escambia County, Code of Ordinance, Chapter 6, Sec. 6-3. - Alcohol-free zone).
</excerpt>
### Rank 4 of 22 — 0.95
<excerpt title="No booze on the beach for the month of March in PCB">
# No booze on the beach for the month of March in PCB
*   Time Travel Tuesday   
*   Breast Cancer Resources   
*   We the People   
*   America 250   
*   Recreation & Outdoors   
*   Aging Untold   
*   Contests   
*   Submit Photos & Video   
*   Newsletter   
*   Shop Local   
*   Contact Us 

    *   Meet the Team   
    *   Meet the Sales Team   
    *   Advertise With Us   
    *   Find a Job 

*   Programming Schedule   
*   NextGen TV   
*   Circle Country   
*   Local News Live   
*   InvestigateTV   
*   Watching Your Wallet   
*   PowerNation   
*   My NetworkTV   
*   Digital Marketing   
*   Gray AI Policy
ByKatie Bente
Published: Feb. 9, 2022 at 6:51 PM CST
Share
Add Us On Google Add as a preferred source on Google
PANAMA CITY BEACH, Fla. (WJHG/WECP) - Spring break is fast approaching and that means so are the spring break ordinances. One of the biggest rules some visitors might not know about is there is absolutely no alcohol allowed on the sandy beaches.
March in Panama City Beach is typically filled with sunshine and spring breakers.
“You know I’ve seen a lot of accidents when there was the booze you know on the beach,” Bay County resident Shawn Brown said.
Having booze on the beach is allowed 11 months of the year with the exception of March.
“Now since we have that law in place, you know it’s cut down quite a bit,” Brown said.
A list of ordinances was put into place by the city back in 2016. One of them quote, “prohibits the possession or consumption of alcohol on the sandy gulf beach.”
“I did know about it,” one resident said.
“Yeah, I did. you know the spring breakers come down here, they can get out of hand,” Brown said.
While this spring break rule is common knowledge for those who have been here these last few years, many of those who haven’t said they had no idea the law existed.
If you break the rule, you could land yourself in jail with an up to $500 fine.

# No booze on the beach for the month of March in PCB
In March of 2021, Panama City Beach police said they made more than 360 arrests, including 16 juveniles.
_Copyright 2022 WJHG. All rights reserved._

# No booze on the beach for the month of March in PCB
#### Most Read
###### Bicyclist killed in crash with flatbed truck on U.S. 98 in Bay County


# No booze on the beach for the month of March in PCB
#### Most Read
###### Walton County commissioner resigns, officials confirm


# No booze on the beach for the month of March in PCB
#### Most Read
###### Highway patrol to pay $70,000 to former Wild Orchid member in DUI arrest settlement


# No booze on the beach for the month of March in PCB
#### Most Read
###### Roadblock due to crash on N. Lakeshore Dr. and Panama City Beach Pkwy.


# No booze on the beach for the month of March in PCB
#### Most Read
###### BCSO holds press conference, announces arrests in two separate investigations


# No booze on the beach for the month of March in PCB
#### Most Read
###### Boil water notice issued for portions of three Panama City Beach streets


# No booze on the beach for the month of March in PCB
#### Most Read
###### Here’s how much Medicare Part B premiums are increasing in 2027


# No booze on the beach for the month of March in PCB
#### Most Read
###### Driver’s license, motor vehicle issuance system back to normal after ‘degradation of services,’ FLHSMV says
</excerpt>
### Rank 5 of 22 — 0.92
<excerpt title="Spring Break rules now in effect">
Back  KR
Search with your voice
Sign in
KR
Spring Break rules now in effect
0:02 / 1:55
•Watch full video
6:485:239:421:4712:5316:431:3816:128:0129:144:0415:00
WJHG-TV NewsChannel 7 | Northwest Florida
5.25K subscribers
Download
589 views 8mo ago
589 views • Mar 4, 2026
For the month of March, alcohol is prohibited on the beach in Panama City Beach, and bars close by 2 a.m. For more Local News from WJHG: https://www.wjhg.com/…
more
more

## Comments


## Comments 2


## In this video


## Spring Break rules now in effect
WJHG-TV NewsChannel 7 | Northwest Florida
1 Likes
589 Views
Mar 4 2026
For the month of March, alcohol is prohibited on the beach in Panama City Beach, and bars close by 2 a.m. For more Local News from WJHG: https://www.wjhg.com/ For more YouTube Content: /@wjhgtv
Transcript
Follow along using the transcript.

## Spring Break rules now in effect
### WJHG-TV NewsChannel 7 | Northwest Florida 5.25K subscribers
VideosAboutFacebookTwitterInstagram

## Video details
Date
Mar 4, 2026
Views
589
Likes
1

## Transcript
### Post-Midterm Cold Open - SNL
Saturday Night Live
13M 11d ago

## Transcript
### Florida rains for 24 hours straight causing major floods, Brevard, Broward, South FL, Volusia
LiveNOW from FOX
69K 3h ago

## Transcript
### The orphaned, injured baby wild otter has regained its vitality.
이웃집수달 Zoo Family
1.1M 8d ago

## Transcript
### California bans Waymo vehicles from freeways
NBC News
706K 1d ago

## Transcript
### NE-YO의 킬링보이스를 라이브로!🎙️ – So Sick, Because Of You, Up Out & Gone, Ms. Tundraㅣ딩고뮤직ㅣdingo Music
딩고 뮤직 / dingo music
8.2M 9d ago

## Transcript
### World’s Largest Economies | GDP History & Projection (1 AD–2100)
Global Stats
1.2M 4mo ago

## Transcript
### Chaos erupts during spring break in Florida
NBC News
762K 8mo ago

## Transcript
### I Asked 1000 People About Their Biggest Regrets in Life and Learned...
Sprouht
3.3M 7mo ago

## Transcript
### 20 Worst Plane Landing Fails
lucaas
444K 2w ago

## Transcript
### 강남역에서 37년 째 성형외과 운영하는 70세 의사의 하루
휴먼스토리
821K 2w ago

## Transcript
### Warrior Beach Retreat honors wounded veterans in Panama City Beach - Captain Sam Brasfield
WJHG-TV NewsChannel 7 | Northwest Florida
29 2d ago

## Transcript
### How Did Immigrants and Refugees Become a Headache for Europe? | Europe, Immigration, Refugees
김지윤의 지식Play
267K 8h ago

## Transcript
### ["Is Indonesia Ruined?"… Foreigners Fleeing as Currency Becomes Worthless [Economic Concert] / KBS...](https://www.youtube.com/watch?v=Kzx8xuGPKCE&pp=ugUHEgVlbi1VUw%3D%3D)
KBS News
1.5M 7h ago

## Transcript
### [[News Tracker] The Tragic End of the 'Test King' / Despite All the Warnings... / The Struggles of...](https://www.youtube.com/watch?v=9M6oRQdsMok&pp=ugUHEgVlbi1VUw%3D%3D)
MBN News
171K 6h ago
Auto-dubbed
</excerpt>

## Search 2 — query: "abcfws.com "Alcoholic beverages are permitted year-round, except for March""
(no page could be scored)

## Search 3 — query: "Panama City Beach alcohol March on the beach ban"
### Rank 1 of 36 — 0.92 (passed on)
<excerpt title="Spring Break rules now in effect">
Back  KR
Search with your voice
Sign in
KR
Spring Break rules now in effect
0:02 / 1:55
•Watch full video
6:485:239:421:4712:5316:431:3816:128:0129:144:0415:00
WJHG-TV NewsChannel 7 | Northwest Florida
5.25K subscribers
Download
589 views 8mo ago
589 views • Mar 4, 2026
For the month of March, alcohol is prohibited on the beach in Panama City Beach, and bars close by 2 a.m. For more Local News from WJHG: https://www.wjhg.com/…
more
more

## Comments


## Comments 2


## In this video


## Spring Break rules now in effect
WJHG-TV NewsChannel 7 | Northwest Florida
1 Likes
589 Views
Mar 4 2026
For the month of March, alcohol is prohibited on the beach in Panama City Beach, and bars close by 2 a.m. For more Local News from WJHG: https://www.wjhg.com/ For more YouTube Content: /@wjhgtv
Transcript
Follow along using the transcript.

## Spring Break rules now in effect
### WJHG-TV NewsChannel 7 | Northwest Florida 5.25K subscribers
VideosAboutFacebookTwitterInstagram

## Video details
Date
Mar 4, 2026
Views
589
Likes
1

## Transcript
### Post-Midterm Cold Open - SNL
Saturday Night Live
13M 11d ago

## Transcript
### Florida rains for 24 hours straight causing major floods, Brevard, Broward, South FL, Volusia
LiveNOW from FOX
69K 3h ago

## Transcript
### The orphaned, injured baby wild otter has regained its vitality.
이웃집수달 Zoo Family
1.1M 8d ago

## Transcript
### California bans Waymo vehicles from freeways
NBC News
706K 1d ago

## Transcript
### NE-YO의 킬링보이스를 라이브로!🎙️ – So Sick, Because Of You, Up Out & Gone, Ms. Tundraㅣ딩고뮤직ㅣdingo Music
딩고 뮤직 / dingo music
8.2M 9d ago

## Transcript
### World’s Largest Economies | GDP History & Projection (1 AD–2100)
Global Stats
1.2M 4mo ago

## Transcript
### Chaos erupts during spring break in Florida
NBC News
762K 8mo ago

## Transcript
### I Asked 1000 People About Their Biggest Regrets in Life and Learned...
Sprouht
3.3M 7mo ago

## Transcript
### 20 Worst Plane Landing Fails
lucaas
444K 2w ago

## Transcript
### 강남역에서 37년 째 성형외과 운영하는 70세 의사의 하루
휴먼스토리
821K 2w ago

## Transcript
### Warrior Beach Retreat honors wounded veterans in Panama City Beach - Captain Sam Brasfield
WJHG-TV NewsChannel 7 | Northwest Florida
29 2d ago

## Transcript
### How Did Immigrants and Refugees Become a Headache for Europe? | Europe, Immigration, Refugees
김지윤의 지식Play
267K 8h ago

## Transcript
### ["Is Indonesia Ruined?"… Foreigners Fleeing as Currency Becomes Worthless [Economic Concert] / KBS...](https://www.youtube.com/watch?v=Kzx8xuGPKCE&pp=ugUHEgVlbi1VUw%3D%3D)
KBS News
1.5M 7h ago

## Transcript
### [[News Tracker] The Tragic End of the 'Test King' / Despite All the Warnings... / The Struggles of...](https://www.youtube.com/watch?v=9M6oRQdsMok&pp=ugUHEgVlbi1VUw%3D%3D)
MBN News
171K 6h ago
Auto-dubbed
</excerpt>
### Rank 2 of 36 — 0.91
<excerpt title="Panama City Beach Rules & Regulations | Visitor FAQs">
Skip navigationSkip to main content

## FAQ's
##### Where is there public beach access?
All of the beaches in Bay County are public. Bay County maintains 96 public access points stretching from the East end of Thomas Dr. to the west end of Front Beach Road. Visitors should not park in areas marked by no parking signs or on private property without permission of the owner. There are 4 easy to use public parking areas with beach access; Pier Park/Russell-Fields City Pier (16101 Front Beach Road), MB Miller County Pier (12213 Front Beach Road), Rick Seltzer Park (7419 Thomas Drive), and St. Andrews State Park on the East End of Thomas Drive (4607 State Park Lane).
View Access Points

## FAQ's
##### Are tents allowed on the beach?
Tents are welcome on our beach. However, tents and any other personal items that are left unattended between the hours 7:00 p.m. and 7:00 a.m. are subject to removal by the authorized beach services contractor under the Leave No Trace Ordinance. Read through our Leave No Trace Ordinance for more information on how we can protect our beaches.
Read Ordinance

## FAQ's
##### Where is the best place to find shells on the beach?
Shells can be found all along Bay County beaches both on the shore and in the water. Early mornings are the most productive shelling times because the beaches are less crowded. Particularly popular shelling sites include the jetties at St. Andrews State Park, Shell Island, and Crooked Beach located between the Eastern end of Tyndall Air Force Base.
View Beaches

## FAQ's
##### Do I need a fishing license?
Yes! A fishing license is required to fish in all the waters in the Panama City Beach area unless fishing from a licensed fishing pier or charter boat operated by a licensed captain. A 3-day out of state license can be purchased for $17 at all area Walmart stores, most bait and tackle shops, and the Bay County Tax Collectors Office located at 17109 Panama City Beach Parkway. For more information on Fishing Regulations please visithttp://myfwc.com.
View Fishing Charters

## FAQ's
##### Which time zone is Panama City Beach in?
Central Time Zone

## FAQ's
##### Are there age restrictions for accommodations in Panama City Beach?
Age requirements are set by each individual property. Many hotels follow an 18 or older policy while most condominiums have older age requirements such as 21, 25, or 27. These policies can change so it is important to stay in contact with the property where reservations have been made to ensure compliance with their policies.
View Hotels

## FAQ's
##### Is alcohol allowed on the beach?
Persons 21 or older are allowed to consume alcoholic beverages on the beach 11 months out of the year. Alcoholic beverages are not permitted on the sandy beach during the month of March. Glass bottles are strictly prohibited year round on the beach.

## FAQ's
##### Why are the beach flags red?
Bay County and Panama City Beach maintain a flag warning system which alerts swimmers when water conditions have become dangerous. Red flags are used to indicate a high hazard which means rip currents are strong and can present significant danger to swimmers. When red flags are flying swimmers are urged to use extreme caution when entering the water. When double red flags are raised, the Gulf of Mexico is closed to the public. Local officials constantly monitor water conditions. Once it has been determined that water conditions have become safe for swimmers, the flags will be changed accordingly.
Read More

## FAQ's
##### When will the seaweed go away?
Seaweed is naturally occurring vegetation that develops when environmental conditions are conducive to its development. Seaweed can come and go with the tides so there might be seaweed present one day and then be gone the next. Although large amounts of seaweed can be unpleasant, it is not harmful to humans and is necessary for the maintenance of a healthy ecosystem along the Gulf of Mexico.

## FAQ's
##### Does Panama City Beach clean the seaweed off the beach?
Yes, the beach services contractor does sweep the beach on a regular cycle. Because of its importance to the maintenance of a healthy beach ecosystem, the Department of Environmental Protection discourages the daily removal of seaweed from the beaches.
</excerpt>
### Rank 3 of 36 — 0.88
<excerpt title="For March, alcohol is prohibited on the beach in Panama City ...">
# WCTV.tv - For March, alcohol is prohibited on the beach in... | Facebook
Log In
Log In
Forgot Account?

# WCTV.tv - For March, alcohol is prohibited on the beach in... | Facebook
## WCTV.tv's Post
* * *
[](https://www.facebook.com/WCTV.tv?__cft__[0]=AZgVYg0Y-xrMUSVFvZNPyC60e3lJ9ko6bgCyd905iosj1cQ-VjG2zGwhqfbPI14Xw9obO4hvxwef3sBIRfDpGX8WYoRk1BAZdUJtIYszY41ivuUB_TjvGtHxgmgBjrvHIGT3CUqL4A9xyblfj8nQaUKFI-ezbqIO&__tn__=%3C%3C%2CP-R)
### [**WCTV.tv**](https://www.facebook.com/WCTV.tv?__cft__[0]=AZgVYg0Y-xrMUSVFvZNPyC60e3lJ9ko6bgCyd905iosj1cQ-VjG2zGwhqfbPI14Xw9obO4hvxwef3sBIRfDpGX8WYoRk1BAZdUJtIYszY41ivuUB_TjvGtHxgmgBjrvHIGT3CUqL4A9xyblfj8nQaUKFI-ezbqIO&__tn__=-UC%2CP-R)
Tuesday, March 3, 2026 at 5:15 PM

# WCTV.tv - For March, alcohol is prohibited on the beach in... | Facebook
## WCTV.tv's Post
[March 3](https://www.facebook.com/WCTV.tv/posts/pfbid02gcLqw6SmVp2LUn7T4RBje8fsPVVRgHMY7MycA7MJMLvPFP5mzjJCYAyM23NrLnrAl?__cft__[0]=AZgVYg0Y-xrMUSVFvZNPyC60e3lJ9ko6bgCyd905iosj1cQ-VjG2zGwhqfbPI14Xw9obO4hvxwef3sBIRfDpGX8WYoRk1BAZdUJtIYszY41ivuUB_TjvGtHxgmgBjrvHIGT3CUqL4A9xyblfj8nQaUKFI-ezbqIO&__tn__=%2CO%2CP-R) ·
For March, alcohol is prohibited on the beach in Panama City Beach, and bars close by 2 a.m. Thoughts?
[](https://www.facebook.com/photo/?fbid=1391627136338334&set=a.638044215029967&__cft__[0]=AZgVYg0Y-xrMUSVFvZNPyC60e3lJ9ko6bgCyd905iosj1cQ-VjG2zGwhqfbPI14Xw9obO4hvxwef3sBIRfDpGX8WYoRk1BAZdUJtIYszY41ivuUB_TjvGtHxgmgBjrvHIGT3CUqL4A9xyblfj8nQaUKFI-ezbqIO&__tn__=EH-R)
![Image 3](blob:http://localhost/85d8b181a20aeb64a3afc2f1c39d2480)
</excerpt>
### Rank 4 of 36 — 0.86
<excerpt title="For March, alcohol is prohibited on the beach in Panama City ...">
# WCTV.tv - For March, alcohol is prohibited on the beach in... | Facebook
## WCTV.tv's Post
[March 3](https://www.facebook.com/WCTV.tv/posts/pfbid02gcLqw6SmVp2LUn7T4RBje8fsPVVRgHMY7MycA7MJMLvPFP5mzjJCYAyM23NrLnrAl?__cft__[0]=AZgVYg0Y-xrMUSVFvZNPyC60e3lJ9ko6bgCyd905iosj1cQ-VjG2zGwhqfbPI14Xw9obO4hvxwef3sBIRfDpGX8WYoRk1BAZdUJtIYszY41ivuUB_TjvGtHxgmgBjrvHIGT3CUqL4A9xyblfj8nQaUKFI-ezbqIO&__tn__=%2CO%2CP-R) ·
For March, alcohol is prohibited on the beach in Panama City Beach, and bars close by 2 a.m. Thoughts?
[](https://www.facebook.com/photo/?fbid=1391627136338334&set=a.638044215029967&__cft__[0]=AZgVYg0Y-xrMUSVFvZNPyC60e3lJ9ko6bgCyd905iosj1cQ-VjG2zGwhqfbPI14Xw9obO4hvxwef3sBIRfDpGX8WYoRk1BAZdUJtIYszY41ivuUB_TjvGtHxgmgBjrvHIGT3CUqL4A9xyblfj8nQaUKFI-ezbqIO&__tn__=EH-R)
![Image 3](blob:http://localhost/85d8b181a20aeb64a3afc2f1c39d2480)

# WCTV.tv - For March, alcohol is prohibited on the beach in... | Facebook
## WCTV.tv's Post
![Image 4](blob:http://localhost/2b45e6f1a2ae097354c0b291152873d5)
![Image 5](blob:http://localhost/520c193f0276d495fb772a9afb8b220d)
All reactions:
93
21 comments
17 shares
Like
Comment
Most relevant
[](https://www.facebook.com/WCTV.tv?comment_id=Y29tbWVudDoxMzkxNjI3MTgzMDA0OTk2XzE2MDkyNDE2MTY3ODMyOTY%3D&__cft__[0]=AZgVYg0Y-xrMUSVFvZNPyC60e3lJ9ko6bgCyd905iosj1cQ-VjG2zGwhqfbPI14Xw9obO4hvxwef3sBIRfDpGX8WYoRk1BAZdUJtIYszY41ivuUB_TjvGtHxgmgBjrvHIGT3CUqL4A9xyblfj8nQaUKFI-ezbqIO&__tn__=R]-R)
Author
</excerpt>
### Rank 5 of 36 — 0.86
<excerpt title="March rules expire in Panama City Beach, allowing alcohol on the beach">
April 1, 2026, 3:31 p.m. ET
*   Panama City Beach's March-only spring break ordinances, including a ban on alcohol on the beach, expired on April 1.  
*   Some restrictions will continue into April, such as overnight beach closures in certain areas and a curfew for unaccompanied minors.  
*   The city's mayor stated there are no current plans to extend the stricter March alcohol rules into April.
PANAMA CITY BEACH − Beachgoers can once again crack open a cold one along the sandy coast, and that's not an April Fool's joke.
Starting April 1, a list of spring break-related ordinances spanning the month of March expires in the Panama City Beach area. They include no alcohol on the sandy beach, no consuming alcohol in commercial parking lots and no nightly alcohol sales after 2 a.m.
While the March ordinances have expired, there still are some spring break-related rules on the beach that are slated to last into April.
"There are no plans right now to reevaluate the March rules," Mayor Stuart Tettemer said when asked whether officials might consider extending them into April. "We want to take a step back. We now have (multiple) layers of rules for spring break."

## Overnight beach closures, high impact zones continue
There are temporary overnight beach closures for two portions of the coast in Panama City Beach that will run until April 30. Closures are in effect from 10 p.m. to 4 a.m. The affected beaches span from Beach Access 25 to Beach access 36, as well as from Beach Access 58 to the east end property line of the Calypso Condominiums.
Panama City Beach and Bay County officials also designated March 28 to April 22 a high impact period for the area. Additionally, they established high impact zones, or areas with increased police presence and penalties.
They are located near Pier Park, south of Middle Beach Road from about Alf Coleman Road to Clara Avenue; south of Middle Beach Road from about Richard Jackson Boulevard to the east end of the city's limits; and east of PCB's city limits along Thomas Drive to Raven Street, encompassing Grand Lagoon to the sandy beach area.

## Curfew for unaccompanied minors is still in effect
On top of all that, a temporary nightly curfew for unaccompanied minors from 8 p.m. to 5 a.m. is in effect until the high impact period is over.
March has gone well," Tettemer said. "Obviously, there's always issues during spring break, but we prepared for this, and so far, so good. Spring break does continue into April, but so far the preparations have worked. We're ready for anything that happens."

## Past problems with spring break
Officials have taken such a strict approach when it comes to spring break because the Beach once was known as a spring break capital of the U.S. In about 2015, leaders attempted to change that by enacting the March like no alcohol on the beach for the month.
The spring break craziness did die down for a handful of years after, but in recent years it has ramped back up.
From March 1 to April 14, 2025, Panama City Beach Police Department officers responded to more than 8,100 calls for service, arrested 770 people and wrote about 1,500 citations.
During the same time period from within Beach zones overseen by the Bay County's Sheriff's Office, deputies responded to more than 4,700 calls for service, arrested 213 people and wrote 647 citations.
Also in that 45-day stretch, two people were killed in a shooting at Sunnyside Apartments, three people were shot in a gang-related shooting, a teen accidentally shot himself at Origins at Seahaven Condominium; and gunshots were reported near a Lighthouse Road residence, Hammerhead Fred's, Checkers on the Beach and inside Laketown Wharf's parking garage.
"We don't want to be overly burdensome, but we want to address the problem," Tettemer said. "The high impact period rules ... really came about due to a change in spring break behavior. (For example), what we saw last year. ... The high impact rules really are to protect public health, safety and welfare."
</excerpt>

# Example 3
## Question
What US presidential election years from 1930-2020 elected US democratic presidents who served two full terms and were succeeded by a republican president, while in the same election year, a female American gymnast won the Olympic All-Around Gold medal?

## Expected answer
2008, 2012

## Grade 1.00

## Search 1 — query: "1932 Olympics women's all-around gymnastics gold USA"
### Rank 1 of 26 — 0.75 (passed on)
<excerpt title="Mildred Didrikson Wins Gold In Los Angeles 1932 | The Olympics On The ...">
# Mildred Didrikson Wins Gold In Los Angeles 1932 | The Olympics On The Record
## Transcript
### Behind every great athlete there is someone who never stops believing. 💫⛸️
Olympic Games
133 11 min ago
Shorts New

# Mildred Didrikson Wins Gold In Los Angeles 1932 | The Olympics On The Record
## Transcript
### Marvellous. ✨
Olympic Games
27K 1d ago
Show more
Show more
</excerpt>
### Rank 2 of 26 — 0.74
<excerpt title="Mildred Didrikson Wins Gold In Los Angeles 1932 | The Olympics On The ...">
# Mildred Didrikson Wins Gold In Los Angeles 1932 | The Olympics On The Record
## In this video
Transcript

# Mildred Didrikson Wins Gold In Los Angeles 1932 | The Olympics On The Record
## Key moments
### How did Babe Didrikson get her nickname? ### How did Babe Didrikson get her nickname? 0:22


# Mildred Didrikson Wins Gold In Los Angeles 1932 | The Olympics On The Record
## Key moments
### How did Babe Didrikson get her nickname?
0:22

# Mildred Didrikson Wins Gold In Los Angeles 1932 | The Olympics On The Record
## Key moments
### Who played Babe Didrikson? ### Who played Babe Didrikson? 2:46


# Mildred Didrikson Wins Gold In Los Angeles 1932 | The Olympics On The Record
## Key moments
### Who played Babe Didrikson?
2:46
Sync to video time

# Mildred Didrikson Wins Gold In Los Angeles 1932 | The Olympics On The Record
## Mildred Didrikson Wins Gold In Los Angeles 1932 | The Olympics On The Record
Olympic Games
Olympic Games
369 Likes
38K Views
2018 Sep 2
📲 Subscribe to @olympics: http://oly.ch/Subscribe All-American and all-around star athlete Mildred "Babe" Didrikson picks up two gold medals at the Olympic Games Los Angeles 1932. The most famous Olympic Records are presented in entertaining packages using recreations, animations and a mix of other visual methods: http://bit.do/EN-OTR _____________________________________________________ 🇨🇳 #Beijing2022 replays: https://oly.ch/B22Replays 🇯🇵 #Tokyo2020 replays: https://oly.ch/T20Replays 🗞️ News from the Olympic world: https://oly.ch/News…...more
...more Show less
Transcript
Follow along using the transcript.
Show transcript

# Mildred Didrikson Wins Gold In Los Angeles 1932 | The Olympics On The Record
## Mildred Didrikson Wins Gold In Los Angeles 1932 | The Olympics On The Record
### Olympic Games 16.7M subscribers
VideosAbout
4:24 4:24How One Man Changed the High Jump Forever | The Olympics on the Record by Olympic Games
On The Record | Olympic Channel Only on the Olympic Channel!

# Mildred Didrikson Wins Gold In Los Angeles 1932 | The Olympics On The Record
## Video details
Date
Sep 2, 2018
Views
38,524
Likes
369

# Mildred Didrikson Wins Gold In Los Angeles 1932 | The Olympics On The Record
## Transcript
NaN / NaN
4:15

# Mildred Didrikson Wins Gold In Los Angeles 1932 | The Olympics On The Record
## Transcript
### How Japan Changed Swimming Forever | The Olympics On The Record
Olympic Games
553K 8y ago
1:45:12

# Mildred Didrikson Wins Gold In Los Angeles 1932 | The Olympics On The Record
## Transcript
### Full Olympic Film - Mexico City 1968 Olympic Games
Olympic Games
945K 12y ago
2:26

# Mildred Didrikson Wins Gold In Los Angeles 1932 | The Olympics On The Record
## Transcript
### THIS is why you should NEVER give up! 💪🏻 The Lasse Virén Story
Olympic Games
1.8M 3y ago
4:24

# Mildred Didrikson Wins Gold In Los Angeles 1932 | The Olympics On The Record
## Transcript
### How One Man Changed the High Jump Forever | The Olympics on the Record
Olympic Games
10M 8y ago
2:13

# Mildred Didrikson Wins Gold In Los Angeles 1932 | The Olympics On The Record
## Transcript
### The Highest Scoring Dive EVER!
Olympic Games
5.8M 5y ago
5:22
</excerpt>
### Rank 3 of 26 — 0.69
<excerpt title="Mildred Didrikson Wins Gold In Los Angeles 1932 | The Olympics On The ...">
# Mildred Didrikson Wins Gold In Los Angeles 1932 | The Olympics On The Record - YouTube
## Mildred Didrikson Wins Gold In Los Angeles 1932 | The Olympics On The Record
4:15 How Japan Changed Swimming Forever | The Olympics On The Record Olympic Games 553K • 8y ago Live Playlist ()Mix (50+)1:45:12 Full Olympic Film - Mexico City 1968 Olympic Games Olympic Games 945K • 12y ago Live Playlist ()Mix (50+)2:26 THIS is why you should NEVER give up! 💪🏻 The Lasse Virén Story Olympic Games 1.8M • 3y ago Live Playlist ()Mix (50+)4:24 How One Man Changed the High Jump Forever | The Olympics on the Record Olympic Games 10M • 8y ago Live Playlist ()Mix (50+)2:13 The Highest Scoring Dive EVER!Olympic Games 5.8M • 5y ago Live Playlist ()Mix (50+)5:22 Bizarre London marathon earns legendary status | Strangest Moments Olympic Games 194K • 8y ago Live Playlist ()Mix (50+)6:16 James Bond and The Queen London 2012 Performance Olympic Games 86M • 14y ago Live Playlist ()Mix (50+)5:15 South Korea's Olympic Records in Womens Archery | The Olympics On The Record Olympic Games 129K • 8y ago Live Playlist ()Mix (50+)11:43 Moments that Left Us SPEECHLESS at Paris 2024!

# Mildred Didrikson Wins Gold In Los Angeles 1932 | The Olympics On The Record - YouTube
## Mildred Didrikson Wins Gold In Los Angeles 1932 | The Olympics On The Record
❤️🫂Olympic Games 2.3M • 1y ago Live Playlist ()Mix (50+)4:25 The Photo-Finish of One of the Biggest Olympic Rivalries | Olympics On The Record Olympic Games 2.3M • 9y ago Live Playlist ()Mix (50+)3:56 Incredible Moment As Underdog Billy Mills Wins 10,000m Gold - Tokyo 1964 Olympics Olympic Games 2.2M • 13y ago Live Playlist ()Mix (50+)4:06 Kerri Strug's Unforgettable Determination to Win Gymnastics Olympic Gold | Strangest Moments Olympic Games 9M • 8y ago Live Playlist ()Mix (50+)

# Mildred Didrikson Wins Gold In Los Angeles 1932 | The Olympics On The Record
Olympic Games
Olympic Games
16.7M subscribers
Subscribe
Subscribed
369
Download
38K views 8y ago#Beijing2022#Tokyo2020
38,524 views • Sep 2, 2018 • #Beijing2022 #Tokyo2020
📲 Subscribe to @olympics: http://oly.ch/Subscribe All-American and all-around star athlete Mildred "Babe" Didrikson picks up two gold medals at the Olympic Games Los Angeles 19…more
more
Transcript
Follow along using the transcript.
Show transcript

# Mildred Didrikson Wins Gold In Los Angeles 1932 | The Olympics On The Record
### Olympic Games 16.7M subscribers
VideosAbout
4:24 4:24How One Man Changed the High Jump Forever | The Olympics on the Record by Olympic Games
On The Record | Olympic Channel Only on the Olympic Channel!

# Mildred Didrikson Wins Gold In Los Angeles 1932 | The Olympics On The Record
## Video details
Date
Sep 2, 2018
Views
38,524
Likes
369
Show less
#Beijing2022#Tokyo2020

# Mildred Didrikson Wins Gold In Los Angeles 1932 | The Olympics On The Record
38,524 views 38K views
Sep 2, 2018
369
Download
</excerpt>
### Rank 4 of 26 — 0.60
<excerpt title="Mildred Didrikson Wins Gold In Los Angeles 1932 | The Olympics On The ...">
# Mildred Didrikson Wins Gold In Los Angeles 1932 | The Olympics On The Record - YouTube
Back  KR
Skip navigation
Search
Search with your voice
Sign in
KR
[Video 2](blob:https://www.youtube.com/88196948-0963-4a99-8e2e-c0cede952905)
Mildred Didrikson Wins Gold In Los Angeles 1932 | The Olympics On The Record
Tap to unmute
2x

# Mildred Didrikson Wins Gold In Los Angeles 1932 | The Olympics On The Record - YouTube
## Mildred Didrikson Wins Gold In Los Angeles 1932 | The Olympics On The Record
Olympic Games 38,524 views 8y ago
Includes paid promotion
Copy link
Info
Shopping
If playback doesn't begin shortly, try restarting your device.
•
You're signed out
Videos you watch may be added to the TV's watch history and influence TV recommendations. To avoid this, cancel and sign in to YouTube on your computer.
Cancel Confirm
Olympic Games
Subscribe
Subscribed
Welcome to the Olympic Games™ channel, where the Games never end! 🥇 From the best musical moments at the Olympics in our Music Monday series to weekly compilation videos with highlights from the Olympics on Fridays, plus exclusive documentaries about the stories behind the glory, this is where you can find everything about the biggest sporting event in the world.
Watch more Olympianys on the Record!
olympicchannel.com
Visit
Michael Johnson takes his Golden Shoes to Victory at Atlanta 1996 | The Olympics On The Record 4:49
Hide
Up next
Live Upcoming
CancelPlay Now
Share
- [x] Include playlist
An error occurred while retrieving sharing information. Please try again later.
0:00
0:02 / 3:15
Live
•Watch full video
•
•

# Mildred Didrikson Wins Gold In Los Angeles 1932 | The Olympics On The Record - YouTube
## Mildred Didrikson Wins Gold In Los Angeles 1932 | The Olympics On The Record
4:15 How Japan Changed Swimming Forever | The Olympics On The Record Olympic Games 553K • 8y ago Live Playlist ()Mix (50+)1:45:12 Full Olympic Film - Mexico City 1968 Olympic Games Olympic Games 945K • 12y ago Live Playlist ()Mix (50+)2:26 THIS is why you should NEVER give up! 💪🏻 The Lasse Virén Story Olympic Games 1.8M • 3y ago Live Playlist ()Mix (50+)4:24 How One Man Changed the High Jump Forever | The Olympics on the Record Olympic Games 10M • 8y ago Live Playlist ()Mix (50+)2:13 The Highest Scoring Dive EVER!Olympic Games 5.8M • 5y ago Live Playlist ()Mix (50+)5:22 Bizarre London marathon earns legendary status | Strangest Moments Olympic Games 194K • 8y ago Live Playlist ()Mix (50+)6:16 James Bond and The Queen London 2012 Performance Olympic Games 86M • 14y ago Live Playlist ()Mix (50+)5:15 South Korea's Olympic Records in Womens Archery | The Olympics On The Record Olympic Games 129K • 8y ago Live Playlist ()Mix (50+)11:43 Moments that Left Us SPEECHLESS at Paris 2024!
</excerpt>
### Rank 5 of 26 — 0.54
<excerpt title="Mildred Didrikson Wins Gold In Los Angeles 1932 | The Olympics On The ...">
# Mildred Didrikson Wins Gold In Los Angeles 1932 | The Olympics On The Record
## Transcript
### The Highest Scoring Dive EVER!
Olympic Games
5.8M 5y ago
5:22

# Mildred Didrikson Wins Gold In Los Angeles 1932 | The Olympics On The Record
## Transcript
### Bizarre London marathon earns legendary status | Strangest Moments
Olympic Games
194K 8y ago
6:16

# Mildred Didrikson Wins Gold In Los Angeles 1932 | The Olympics On The Record
## Transcript
### James Bond and The Queen London 2012 Performance
Olympic Games
86M 14y ago
5:15

# Mildred Didrikson Wins Gold In Los Angeles 1932 | The Olympics On The Record
## Transcript
### South Korea's Olympic Records in Womens Archery | The Olympics On The Record
Olympic Games
129K 8y ago
11:43

# Mildred Didrikson Wins Gold In Los Angeles 1932 | The Olympics On The Record
## Transcript
### Moments that Left Us SPEECHLESS at Paris 2024! ❤️🫂
Olympic Games
2.3M 1y ago
4:25

# Mildred Didrikson Wins Gold In Los Angeles 1932 | The Olympics On The Record
## Transcript
### The Photo-Finish of One of the Biggest Olympic Rivalries | Olympics On The Record
Olympic Games
2.3M 9y ago
3:56

# Mildred Didrikson Wins Gold In Los Angeles 1932 | The Olympics On The Record
## Transcript
### Incredible Moment As Underdog Billy Mills Wins 10,000m Gold - Tokyo 1964 Olympics
Olympic Games
2.2M 13y ago
4:06

# Mildred Didrikson Wins Gold In Los Angeles 1932 | The Olympics On The Record
## Transcript
### Kerri Strug's Unforgettable Determination to Win Gymnastics Olympic Gold | Strangest Moments
Olympic Games
9M 8y ago
5:37

# Mildred Didrikson Wins Gold In Los Angeles 1932 | The Olympics On The Record
## Transcript
### Mr. Bean Live Performance at the London 2012 Olympic Games
Olympic Games
151M 14y ago
21:03

# Mildred Didrikson Wins Gold In Los Angeles 1932 | The Olympics On The Record
## Transcript
### Nadia Comăneci 🤸🏼‍♀️ - All seven perfect 🔟's at Montreal 1976
Olympic Games and Olympics Gymnastics
4.4M 2y ago
7:10

# Mildred Didrikson Wins Gold In Los Angeles 1932 | The Olympics On The Record
## Transcript
### Almaktoum's Historic Olympic Gold In Athens 2004 | The Olympics On The Record
Olympic Games
519K 8y ago
3:45

# Mildred Didrikson Wins Gold In Los Angeles 1932 | The Olympics On The Record
## Transcript
### Ann Packer Wins 800m Gold For Great Britain - Tokyo 1964 Olympics
Olympic Games
339K 13y ago
5:44

# Mildred Didrikson Wins Gold In Los Angeles 1932 | The Olympics On The Record
## Transcript
### The Stories of the Craziest Mistakes at the Olympic Games | Strangest Moments
Olympic Games
970K 8y ago
Shorts New

# Mildred Didrikson Wins Gold In Los Angeles 1932 | The Olympics On The Record
## Transcript
### ICONIC ✨ There's no such thing as too much sparkles!
Olympic Games
2K 8h ago
Shorts New

# Mildred Didrikson Wins Gold In Los Angeles 1932 | The Olympics On The Record
## Transcript
### Behind every great athlete there is someone who never stops believing. 💫⛸️
Olympic Games
133 11 min ago
Shorts New
</excerpt>

## Search 2 — query: "1996 women's all-around gold gymnast USA"
### Rank 1 of 70 — 0.83 (passed on)
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
### Rank 2 of 70 — 0.81
<excerpt title="Gymnastics at the 1996 Summer Olympics – Women's artistic ...">
| 15 | Svetlana Khorkina(RUS) | 9.706 (=8) | 9.262 (30) | 9.787 (=7) | 9.700 (=8) | 38.455 |  
| 16 | Elvire Teza(FRA) | 9.493 (=28) | 9.687 (=13) | 9.687 (=12) | 9.587 (18) | 38.454 |  
| 17 | Dominique Dawes(USA) | 9.681 (=13) | 9.812 (1) | 9.825 (=2) | 9.000 (33) | 38.318 |  
| 17 | Mónica Martín(ESP) | 9.556 (24) | 9.475 (=24) | 9.625 (16) | 9.662 (12) | 38.318 |  
| 19 | Ludivine Furnon(FRA) | 9.606 (=17) | 9.425 (27) | 9.462 (22) | 9.750 (=5) | 38.243 |  
| 20 | Mao Yanling(CHN) | 9.693 (10) | 9.700 (=11) | 9.200 (28) | 9.650 (=13) | 38.243 |  
| 21 | Vasiliki Tsavdaridou(GRE) | 9.518 (25) | 9.562 (22) | 9.687 (=12) | 9.450 (30) | 38.217 |  

| 22 | Lioubov Sheremeta(UKR) | 9.468 (30) | 9.637 (18) | 9.587 (=18) | 9.512 (=26) | 38.204 |  
| 23 | Svitlana Zelepukina(UKR) | 9.512 (=26) | 9.650 (17) | 9.325 (25) | 9.537 (25) | 38.024 |  
| 24 | Joana Juárez(ESP) | 9.568 (22) | 9.575 (21) | 9.300 (27) | 9.512 (=26) | 37.955 |  
| 25 | Alena Polozkova(BLR) | 9.587 (19) | 9.162 (32) | 9.450 (23) | 9.600 (=16) | 37.799 |  
| 26 | Yvonne Tousek(CAN) | 9.493 (=28) | 9.100 (33) | 9.575 (20) | 9.625 (16) | 37.793 |  
| 27 | Mercedes Pacheco(ESP) | 9.462 (31) | 9.625 (19) | 9.137 (30) | 9.562 (=23) | 37.786 |  
| 28 | Adrienn Varga(HUN) | 9.606 (=17) | 9.187 (31) | 9.312 (26) | 9.487 (28) | 37.592 |
</excerpt>
### Rank 3 of 70 — 0.77
<excerpt title="Magnificent Seven (gymnastics)">
The **Magnificent Seven** was the 1996 [United States Olympic women's gymnastics team](https://en.wikipedia.org/wiki/United_States_women's_national_artistic_gymnastics_team "United States women's national artistic gymnastics team") that won the first-ever gold medal for the United States in the [women's team competition](https://en.wikipedia.org/wiki/Gymnastics_at_the_1996_Summer_Olympics_%E2%80%93_Women's_artistic_team_all-around "Gymnastics at the 1996 Summer Olympics – Women's artistic team all-around") at the 1996 Summer Olympics in Atlanta. The seven members of the team were Shannon Miller, Dominique Moceanu, Dominique Dawes, Kerri Strug, Amy Chow, Jaycie Phelps, and team captain Amanda Borden. Miller, Chow, and Dawes also won an individual gold, silver, and bronze medals respectively in Atlanta. The team is perhaps best known for Strug sticking the landing of a vault to clinch the gold medal while injured.
The leader of the Magnificent Seven is often said to be Shannon Miller, the second most decorated American gymnast in history and that year's reigning national champion.[[1]](https://en.wikipedia.org/wiki/Magnificent_Seven_(gymnastics)#cite_note-1) The other two individual stars on the team were Dominique Dawes and Dominique Moceanu, the previous two national champions (in 1994 and 1995 respectively). However, Kerri Strug eventually qualified for the individual all-around over Moceanu.
The other three members on the team were less heralded. Nevertheless, they were an integral part of the team's success. Amy Chow had the highest difficulty of anyone on the team, most notably on the uneven bars. Jaycie Phelps provided clean lines and solid gymnastics on all four events. The final member to qualify for the team, Amanda Borden, was named team captain.[[2]](https://en.wikipedia.org/wiki/Magnificent_Seven_(gymnastics)#cite_note-2)[[3]](https://en.wikipedia.org/wiki/Magnificent_Seven_(gymnastics)#cite_note-3)

The highest two scoring athletes on the team during the compulsories did not even perform at the Olympic Trials. Both Miller and Moceanu had been sidelined with injuries but were named to the team anyway, proving that the petition system was in the team's best interest.
The team compulsories took place on July 21, 1996. Unlike in the 1992 Games, when two athletes from each country participated in each session, in these Games, teams competed together. The United States team competed in the third session, with Russia and China left to compete in the fourth session. Romania had already competed in the first session, so the United States team could only chase their already posted scores. The top four teams would compete in the last session during the optionals. Ultimately, Ukraine, not China, earned this fourth spot along with the United States, Russia, and Romania.
With seven athletes on each team for the first and only time, each team (other than Romania who had only six members because of an injury) put their six best team members up on each event. Of these six scores, only the top five would count. On the United States team in both compulsories and optionals, Miller, Moceanu, Dawes, Strug, and Phelps competed on all four events while Chow only competed on bars and vault and Borden only competed on beam and floor. The United States started their meet on uneven bars with no major misses. Miller earned the highest score of 9.775, and Strug's score of 9.675 was dropped.
Following uneven bars, the team moved to the balance beam where Strug led off with a shaky performance. Borden and Dawes followed, each with noticeable errors. Phelps, who won the compulsory round at the Olympic Trials (although neither Miller or Moceanu competed at this event), was next. Although known for her beautiful technique, she looked shaky from the start of the routine and fell off the beam during the fouette jump element. Although she finished strongly, her low score of 9.012 was dropped. Miller followed with a routine that appeared to be flawless and earned the overall high beam score of the competition, 9.737. Moceanu anchored the United States and with only minor errors and impeccable form on certain elements earned a 9.687.
</excerpt>
### Rank 4 of 70 — 0.74
<excerpt title="Magnificent Seven (gymnastics)">
| Magnificent Seven |  
| --- |  
| Full name | Amanda Borden, Amy Chow, Dominique Dawes, Shannon Miller, Dominique Moceanu, Jaycie Phelps, and Kerri Strug |  
| Gymnastics career |  
| Discipline | [Women's artistic gymnastics](https://en.wikipedia.org/wiki/Women's_artistic_gymnastics "Women's artistic gymnastics") |  
| Country represented | * United States |  
| Medal record Representing United States Olympic Games 1996 Atlanta[Team](https://en.wikipedia.org/wiki/Gymnastics_at_the_1996_Summer_Olympics_%E2%80%93_Women's_artistic_team_all-around "Gymnastics at the 1996 Summer Olympics – Women's artistic team all-around") 1996 Atlanta[Balance beam](https://en.wikipedia.org/wiki/Gymnastics_at_the_1996_Summer_Olympics_%E2%80%93_Women's_balance_beam "Gymnastics at the 1996 Summer Olympics – Women's balance beam") 1996 Atlanta[Uneven bars](https://en.wikipedia.org/wiki/Gymnastics_at_the_1996_Summer_Olympics_%E2%80%93_Women's_uneven_bars "Gymnastics at the 1996 Summer Olympics – Women's uneven bars") 1996 Atlanta[Floor exercise](https://en.wikipedia.org/wiki/Gymnastics_at_the_1996_Summer_Olympics_%E2%80%93_Women's_floor "Gymnastics at the 1996 Summer Olympics – Women's floor") |

The **Magnificent Seven** was the 1996 [United States Olympic women's gymnastics team](https://en.wikipedia.org/wiki/United_States_women's_national_artistic_gymnastics_team "United States women's national artistic gymnastics team") that won the first-ever gold medal for the United States in the [women's team competition](https://en.wikipedia.org/wiki/Gymnastics_at_the_1996_Summer_Olympics_%E2%80%93_Women's_artistic_team_all-around "Gymnastics at the 1996 Summer Olympics – Women's artistic team all-around") at the 1996 Summer Olympics in Atlanta. The seven members of the team were Shannon Miller, Dominique Moceanu, Dominique Dawes, Kerri Strug, Amy Chow, Jaycie Phelps, and team captain Amanda Borden. Miller, Chow, and Dawes also won an individual gold, silver, and bronze medals respectively in Atlanta. The team is perhaps best known for Strug sticking the landing of a vault to clinch the gold medal while injured.
The leader of the Magnificent Seven is often said to be Shannon Miller, the second most decorated American gymnast in history and that year's reigning national champion.[[1]](https://en.wikipedia.org/wiki/Magnificent_Seven_(gymnastics)#cite_note-1) The other two individual stars on the team were Dominique Dawes and Dominique Moceanu, the previous two national champions (in 1994 and 1995 respectively). However, Kerri Strug eventually qualified for the individual all-around over Moceanu.
The other three members on the team were less heralded. Nevertheless, they were an integral part of the team's success. Amy Chow had the highest difficulty of anyone on the team, most notably on the uneven bars. Jaycie Phelps provided clean lines and solid gymnastics on all four events. The final member to qualify for the team, Amanda Borden, was named team captain.[[2]](https://en.wikipedia.org/wiki/Magnificent_Seven_(gymnastics)#cite_note-2)[[3]](https://en.wikipedia.org/wiki/Magnificent_Seven_(gymnastics)#cite_note-3)
</excerpt>
### Rank 5 of 70 — 0.72
<excerpt title="Gymnastics at the 1996 Summer Olympics – Women's artistic ...">
| Rank | Gymnast | Vault | Uneven Bars | Balance Beam | Floor Exercise | Total |  
| --- | --- | --- | --- | --- | --- | --- |  
|  | Lilia Podkopayeva(UKR) | 9.781 (3) | 9.800 (=2) | 9.787 (=7) | 9.887 (1) | 39.255 |  
|  | Gina Gogean(ROU) | 9.775 (4) | 9.700 (=11) | 9.800 (=5) | 9.800 (3) | 39.075 |  
|  | Simona Amânar(ROU) | 9.843 (1) | 9.762 (=5) | 9.725 (=10) | 9.737 (7) | 39.067 |  
| Lavinia Miloșovici(ROU) | 9.743 (5) | 9.737 (9) | 9.775 (9) | 9.812 (2) |  
| 5 | Mo Huilan(CHN) | 9.799 (2) | 9.800 (=2) | 9.800 (=5) | 9.650 (=13) | 39.049 |  
| 6 | Dina Kochetkova(RUS) | 9.581 (20) | 9.787 (4) | 9.825 (=2) | 9.787 (4) | 38.980 |  
| 7 | Rozalia Galiyeva(RUS) | 9.681 (=13) | 9.762 (=5) | 9.825 (=2) | 9.637 (15) | 38.905 |  

| 8 | Shannon Miller(USA) | 9.724 (6) | 9.750 (8) | 9.862 (1) | 9.475 (29) | 38.811 |  
| 9 | Dominique Moceanu(USA) | 9.706 (=8) | 9.762 (=5) | 9.600 (17) | 9.687 (10) | 38.755 |  
| 10 | Oksana Chusovitina(UZB) | 9.631 (15) | 9.687 (=13) | 9.675 (=14) | 9.750 (=5) | 38.743 |  
| 11 | Qiao Ya(CHN) | 9.718 (7) | 9.600 (20) | 9.725 (=10) | 9.675 (11) | 38.718 |  
| 12 | Yelena Piskun(BLR) | 9.687 (=11) | 9.712 (10) | 9.675 (=14) | 9.575 (=21) | 38.649 |  
| 13 | Isabelle Severino(FRA) | 9.562 (23) | 9.675 (=15) | 9.587 (=18) | 9.700 (=8) | 38.524 |  
| 14 | Svetlana Boginskaya(BLR) | 9.687 (=11) | 9.675 (=15) | 9.537 (21) | 9.600 (=16) | 38.499 |
</excerpt>

## Search 3 — query: "1992 women's all-around gymnastics gold medal olympics winner"
### Rank 1 of 91 — 0.89 (passed on)
<excerpt title="Gymnastics at the 1992 Summer Olympics – Women's artistic ...">
From Wikipedia, the free encyclopedia
| Women's artistic individual all-around at the Games of the XXV Olympiad |  
| --- |  
|  Pictogram for Gymnastics |  
| Venue | Palau Sant Jordi |  
| Date | 28 – 30 July 1992 |  
| Competitors | 92 from 24 nations |  
| Medalists |  
| |  | | Tatiana Gutsu | Unified Team | | --- | |  | | Shannon Miller | United States | |  | | Lavinia Miloșovici | Romania | |  
| ←[1988](https://en.wikipedia.org/wiki/Gymnastics_at_the_1988_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 1988 Summer Olympics – Women's artistic individual all-around") [1996](https://en.wikipedia.org/wiki/Gymnastics_at_the_1996_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 1996 Summer Olympics – Women's artistic individual all-around")→ |
These are the results of the women's individual all-around competition, one of six events for female competitors in artistic gymnastics at the 1992 Summer Olympics in Barcelona. The qualification and final rounds took place on July 28 and 30th 1992 at the Palau Sant Jordi.[[1]](https://en.wikipedia.org/wiki/Gymnastics_at_the_1992_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around#cite_note-SR-1)

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
### Rank 2 of 91 — 0.89
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
### Rank 3 of 91 — 0.83
<excerpt title="Her dismount is unreal. Tatiana Gutsu was the 1992 Olympic all- ...">
# Her dismount is unreal. 🤯 Tatiana Gutsu was the 1992 Olympic all-around champion for a reason! • • #olympics #balancebeam #beam #dismount #gymnast #acrobatics #gymnastics #acro #tumbling | Gymnastics Direct | Facebook
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

# Video
## Related Reels
Gymnastics Direct 3.5K
Gymnastics Direct 116K
Gymnastics Direct 1.9K
Gymnastics Direct 2.7K
Gymnastics Direct 2K
Gymnastics Direct 4.4K
Gymnastics Direct 4.6K
Gymnastics Direct 4K

# Video
## Related videos
[ 0:29](https://www.facebook.com/100066338027371/videos/1437038358539936/?__so__=permalink&__cft__[0]=AZiZMT5GsK8iAeqtlmQNrZbLBrBWx3LOZFda6qvXmwYOFRFxHBmsEbd7yvg9G5ETFbf-WxJA7QXVtGURS5r2u7sCpy_zxkJPRwiQw1sd7e_1808b42O2ERYROFp09pBbb0hObUQ0NClM-IoapxHT4Q)
[](https://www.facebook.com/watch/100066338027371/?__cft__[0]=AZiZMT5GsK8iAeqtlmQNrZbLBrBWx3LOZFda6qvXmwYOFRFxHBmsEbd7yvg9G5ETFbf-WxJA7QXVtGURS5r2u7sCpy_zxkJPRwiQw1sd7e_1808b42O2ERYROFp09pBbb0hObUQ0NClM-IoapxHT4Q)
</excerpt>
### Rank 4 of 91 — 0.77
<excerpt title="Tatiana Gutsu">
[1992 Nantes](https://en.wikipedia.org/wiki/1992_European_Women's_Artistic_Gymnastics_Championships "1992 European Women's Artistic Gymnastics Championships")All-Around [1992 Nantes](https://en.wikipedia.org/wiki/1992_European_Women's_Artistic_Gymnastics_Championships "1992 European Women's Artistic Gymnastics Championships")Vault [1992 Nantes](https://en.wikipedia.org/wiki/1992_European_Women's_Artistic_Gymnastics_Championships "1992 European Women's Artistic Gymnastics Championships")Uneven Bars [1992 Nantes](https://en.wikipedia.org/wiki/1992_European_Women's_Artistic_Gymnastics_Championships "1992 European Women's Artistic Gymnastics Championships")Balance Beam [1992 Nantes](https://en.wikipedia.org/wiki/1992_European_Women's_Artistic_Gymnastics_Championships "1992 European Women's Artistic Gymnastics Championships")Floor Exercise |
**Tatiana Gutsu**, rarely **Tetiana Hutsu**,[[2]](https://en.wikipedia.org/wiki/Tatiana_Gutsu#cite_note-2) (Ukrainian: Тетяна Костянтинівна Ґуцу, Romanian: _Tatiana Guțu_; born 5 September 1976, in Odesa, Ukrainian SSR) is a Ukrainian former artistic gymnast from the Soviet Union and the winner of the all-around title in the 1992 Summer Olympics. She was renowned for performing some of the most difficult routines in the sport.[[3]](https://en.wikipedia.org/wiki/Tatiana_Gutsu#cite_note-:0-3) She was inducted into the International Gymnastics Hall of Fame in 2022.[[4]](https://en.wikipedia.org/wiki/Tatiana_Gutsu#cite_note-4)

Born into a Ukrainian family with Moldovan roots, Gutsu started in gymnastics at age 6. She became a member of the national team of the Soviet Union in 1988.[[5]](https://en.wikipedia.org/wiki/Tatiana_Gutsu#cite_note-5) Her first major international competition was the 1991 World Artistic Gymnastics Championships in Indianapolis, where she won the team title with the Soviet Union[[6]](https://en.wikipedia.org/wiki/Tatiana_Gutsu#cite_note-6) and finished fifth in the individual all-around,[[7]](https://en.wikipedia.org/wiki/Tatiana_Gutsu#cite_note-7) while winning silver medals in two individual apparatus finals: the uneven bars and balance beam. Her silver on beam was highly controversial because the winner, Soviet teammate Svetlana Boginskaya, performed a simpler routine.
Gutsu was quickly noticed for the difficulty of her routines. She was one of the few gymnasts during the late 80s/early 90s to perform a double-twisting Yurchenko vault. She also debuted a double layout somersault on floor with split legs in the first salto, a skill that few others have been able to perform. Perhaps most impressively, she ended her floor routine in the team competition with a double layout somersault.
The following year, she had a disastrous showing at the 1992 World Championships. She had been expected to contend for gold on three events—uneven bars, balance beam, and floor exercise—but failed to reach the finals on any of them, suffering falls on both the bars and floor. However, at the European Gymnastics Championships that year, she won the all-around, vault, and uneven bars titles, as well as a silver on the balance beam. She was the most successful gymnast of the championship and established herself as one of the favorites for the Olympic all-around title.
In the preliminary round of competition at the Olympics, Gutsu, then 15, fell from the balance beam and was ranked 9th in the all-around. She had been on course to win the optional portion of the team competition and was one of the favourites for the beam gold medal, but the fall meant she did not qualify for the beam final.
</excerpt>
### Rank 5 of 91 — 0.76
<excerpt title="Tatiana Gutsu wins closest Olympic all-around title">
# Out of Bounds - In 1992, Tatiana Gutsu won the all-around... | Facebook
Log In
Log In
Forgot Account?

# Out of Bounds - In 1992, Tatiana Gutsu won the all-around... | Facebook
## Out of Bounds's Post
* * *
[](https://www.facebook.com/people/Out-of-Bounds/61580552867004/?__cft__[0]=AZgXrFIxC7QKmdzO2t2rMhA5DSHuqRRKCHeBxV2DRsSf1n8OMSOSypSREDGL-nSCKWpTeSwbYMyNCPhtQbbmPaHX1hQ84qcrv9btudrCWSyfchYWz_aa44IhYfbm7ReGnQYlqMemADw8YXqlmlN78hJW7IALvtq22s2T&__tn__=%3C%3C%2CP-R)
### [**Out of Bounds**](https://www.facebook.com/people/Out-of-Bounds/61580552867004/?__cft__[0]=AZgXrFIxC7QKmdzO2t2rMhA5DSHuqRRKCHeBxV2DRsSf1n8OMSOSypSREDGL-nSCKWpTeSwbYMyNCPhtQbbmPaHX1hQ84qcrv9btudrCWSyfchYWz_aa44IhYfbm7ReGnQYlqMemADw8YXqlmlN78hJW7IALvtq22s2T&__tn__=-UC%2CP-R)
Tuesday, December 30, 2025 at 7:43 PM

# Out of Bounds - In 1992, Tatiana Gutsu won the all-around... | Facebook
## Out of Bounds's Post
[December 30, 2025](https://www.facebook.com/permalink.php?story_fbid=pfbid07DB5nADVfuLtCsTb5rAifcgZBWen1CPrzTEjKcLnkFHdk8McmnKteE7N3iLCSGK1l&id=61580552867004&__cft__[0]=AZgXrFIxC7QKmdzO2t2rMhA5DSHuqRRKCHeBxV2DRsSf1n8OMSOSypSREDGL-nSCKWpTeSwbYMyNCPhtQbbmPaHX1hQ84qcrv9btudrCWSyfchYWz_aa44IhYfbm7ReGnQYlqMemADw8YXqlmlN78hJW7IALvtq22s2T&__tn__=%2CO%2CP-R) ·
In 1992, Tatiana Gutsu won the all-around title by .012, which remains the closest margin of victory ever in an Olympic all-around final. [#gymnastics](https://www.facebook.com/hashtag/gymnastics?__eep__=6&__cft__[0]=AZgXrFIxC7QKmdzO2t2rMhA5DSHuqRRKCHeBxV2DRsSf1n8OMSOSypSREDGL-nSCKWpTeSwbYMyNCPhtQbbmPaHX1hQ84qcrv9btudrCWSyfchYWz_aa44IhYfbm7ReGnQYlqMemADw8YXqlmlN78hJW7IALvtq22s2T&__tn__=*NK-R)
</excerpt>

## Search 4 — query: "1996 women's all-around gymnastics gold medal winner"
### Rank 1 of 63 — 0.88 (passed on)
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
### Rank 2 of 63 — 0.87
<excerpt title="Gymnastics at the 1996 Summer Olympics – Women's artistic ...">
| 15 | Svetlana Khorkina(RUS) | 9.706 (=8) | 9.262 (30) | 9.787 (=7) | 9.700 (=8) | 38.455 |  
| 16 | Elvire Teza(FRA) | 9.493 (=28) | 9.687 (=13) | 9.687 (=12) | 9.587 (18) | 38.454 |  
| 17 | Dominique Dawes(USA) | 9.681 (=13) | 9.812 (1) | 9.825 (=2) | 9.000 (33) | 38.318 |  
| 17 | Mónica Martín(ESP) | 9.556 (24) | 9.475 (=24) | 9.625 (16) | 9.662 (12) | 38.318 |  
| 19 | Ludivine Furnon(FRA) | 9.606 (=17) | 9.425 (27) | 9.462 (22) | 9.750 (=5) | 38.243 |  
| 20 | Mao Yanling(CHN) | 9.693 (10) | 9.700 (=11) | 9.200 (28) | 9.650 (=13) | 38.243 |  
| 21 | Vasiliki Tsavdaridou(GRE) | 9.518 (25) | 9.562 (22) | 9.687 (=12) | 9.450 (30) | 38.217 |  

| 22 | Lioubov Sheremeta(UKR) | 9.468 (30) | 9.637 (18) | 9.587 (=18) | 9.512 (=26) | 38.204 |  
| 23 | Svitlana Zelepukina(UKR) | 9.512 (=26) | 9.650 (17) | 9.325 (25) | 9.537 (25) | 38.024 |  
| 24 | Joana Juárez(ESP) | 9.568 (22) | 9.575 (21) | 9.300 (27) | 9.512 (=26) | 37.955 |  
| 25 | Alena Polozkova(BLR) | 9.587 (19) | 9.162 (32) | 9.450 (23) | 9.600 (=16) | 37.799 |  
| 26 | Yvonne Tousek(CAN) | 9.493 (=28) | 9.100 (33) | 9.575 (20) | 9.625 (16) | 37.793 |  
| 27 | Mercedes Pacheco(ESP) | 9.462 (31) | 9.625 (19) | 9.137 (30) | 9.562 (=23) | 37.786 |  
| 28 | Adrienn Varga(HUN) | 9.606 (=17) | 9.187 (31) | 9.312 (26) | 9.487 (28) | 37.592 |
</excerpt>
### Rank 3 of 63 — 0.78
<excerpt title="Magnificent Seven (gymnastics)">
The **Magnificent Seven** was the 1996 [United States Olympic women's gymnastics team](https://en.wikipedia.org/wiki/United_States_women's_national_artistic_gymnastics_team "United States women's national artistic gymnastics team") that won the first-ever gold medal for the United States in the [women's team competition](https://en.wikipedia.org/wiki/Gymnastics_at_the_1996_Summer_Olympics_%E2%80%93_Women's_artistic_team_all-around "Gymnastics at the 1996 Summer Olympics – Women's artistic team all-around") at the 1996 Summer Olympics in Atlanta. The seven members of the team were Shannon Miller, Dominique Moceanu, Dominique Dawes, Kerri Strug, Amy Chow, Jaycie Phelps, and team captain Amanda Borden. Miller, Chow, and Dawes also won an individual gold, silver, and bronze medals respectively in Atlanta. The team is perhaps best known for Strug sticking the landing of a vault to clinch the gold medal while injured.
The leader of the Magnificent Seven is often said to be Shannon Miller, the second most decorated American gymnast in history and that year's reigning national champion.[[1]](https://en.wikipedia.org/wiki/Magnificent_Seven_(gymnastics)#cite_note-1) The other two individual stars on the team were Dominique Dawes and Dominique Moceanu, the previous two national champions (in 1994 and 1995 respectively). However, Kerri Strug eventually qualified for the individual all-around over Moceanu.
The other three members on the team were less heralded. Nevertheless, they were an integral part of the team's success. Amy Chow had the highest difficulty of anyone on the team, most notably on the uneven bars. Jaycie Phelps provided clean lines and solid gymnastics on all four events. The final member to qualify for the team, Amanda Borden, was named team captain.[[2]](https://en.wikipedia.org/wiki/Magnificent_Seven_(gymnastics)#cite_note-2)[[3]](https://en.wikipedia.org/wiki/Magnificent_Seven_(gymnastics)#cite_note-3)

The highest two scoring athletes on the team during the compulsories did not even perform at the Olympic Trials. Both Miller and Moceanu had been sidelined with injuries but were named to the team anyway, proving that the petition system was in the team's best interest.
The team compulsories took place on July 21, 1996. Unlike in the 1992 Games, when two athletes from each country participated in each session, in these Games, teams competed together. The United States team competed in the third session, with Russia and China left to compete in the fourth session. Romania had already competed in the first session, so the United States team could only chase their already posted scores. The top four teams would compete in the last session during the optionals. Ultimately, Ukraine, not China, earned this fourth spot along with the United States, Russia, and Romania.
With seven athletes on each team for the first and only time, each team (other than Romania who had only six members because of an injury) put their six best team members up on each event. Of these six scores, only the top five would count. On the United States team in both compulsories and optionals, Miller, Moceanu, Dawes, Strug, and Phelps competed on all four events while Chow only competed on bars and vault and Borden only competed on beam and floor. The United States started their meet on uneven bars with no major misses. Miller earned the highest score of 9.775, and Strug's score of 9.675 was dropped.
Following uneven bars, the team moved to the balance beam where Strug led off with a shaky performance. Borden and Dawes followed, each with noticeable errors. Phelps, who won the compulsory round at the Olympic Trials (although neither Miller or Moceanu competed at this event), was next. Although known for her beautiful technique, she looked shaky from the start of the routine and fell off the beam during the fouette jump element. Although she finished strongly, her low score of 9.012 was dropped. Miller followed with a routine that appeared to be flawless and earned the overall high beam score of the competition, 9.737. Moceanu anchored the United States and with only minor errors and impeccable form on certain elements earned a 9.687.
</excerpt>
### Rank 4 of 63 — 0.75
<excerpt title="Magnificent Seven (gymnastics)">
The secondary story, often overlooked by the public, is that both Strug and Moceanu were in a tight contest with each other and with Dawes to qualify to the individual All-Around competition. Only three gymnasts per country could advance to the All-Around final, and had Strug not vaulted again, she would have finished fourth behind Miller, Dawes, and Moceanu. Exactly how this may have played a factor is unknown, but unlike the other U.S. gymnasts who opted to perform an easier vault first, Moceanu and Strug both performed their harder Yurchenko 1.5 for both attempts, despite warming up the easier Yurchenko half. Karolyi's strategy may have been to maximize the scores of his own gymnasts for All-Around qualification, rather than secure safe vault scores for the team first. Moceanu and Strug needed vault scores of 9.450 and 9.775 respectively to qualify ahead of Dawes.
Strug walked around, trying to shake off the injury to her ankle, as she headed back to the start of the vaulting runway with Karolyi's and her teammates' encouragement. With the scores of the three best Russian floor workers yet to be posted, Strug needed to vault a second time to secure the gold medal for her team and prevent the Russians from catching up. She performed the second vault well and nearly stuck the landing, however, she immediately lifted her injured leg and collapsed in pain, needing to be carried off the podium. Strug scored a 9.712, securing the gold medal, and the crowd erupted with cheers. This image of Strug's vault instantly became the most enduring moment of the 1996 Olympics and one of the most celebrated moments in American Olympic history. Strug not only qualified for vault finals but also for the All-Around competition. In a twist of irony, the vault that secured her place in the All-Around also prohibited her from participating as she was too injured to compete, and Moceanu took her place. Miller took her place in the vault finals, and Dawes took her place in the floor finals. Additionally, Dawes qualified for vault finals during this competition, earning the team's high vault score of 9.762.

Strug was immediately carried away to a hospital tent, however, Karolyi, adamant that she not miss the medal ceremony, eventually carried her to the podium behind the team. Miller moved out of her assigned place in line (based on height) to Strug's left side to help lift Strug onto the podium along with Moceanu who was on Strug's right. Because of being whisked away from the team and the thick bandage on her leg, Strug didn't have time to put the pants of her warm-up suit on and thus was the only one not wearing them. Because of these factors, the resulting team photographs show a less uniform look amongst the teammates than in other years.
Despite Strug's heroic vault, Miller was the team's highest-scoring member of the team competition, earning the second-highest two-day total in the entire competition (78.028, behind Lilia Podkopayeva's 78.061). However, Dawes (39.187) was the team's highest-scoring member during the optionals portion of the competition (only Simona Amânar's optionals score of 39.387 was higher than that of Dawes), and Strug's optionals total (39.073) also narrowly outscored Miller's (38.967).
The team's gold medal victory was considered phenomenal for the United States because Russia (in its incarnations as the Soviet Union and Unified Team) had won the event in every Olympics it had entered since 1952. Furthermore, the United States had never won the event in either the Olympics or the World Championships, yet in Atlanta, they fielded the deepest American team in history up to that point and upstaged both the Russians and the reigning World Champions Romanians.
Winning the gold medal instantly endeared the team to the American public, and tours, endorsement deals, interviews, and televised specials followed, earning them all a secure place in American Olympic and gymnastics history.
</excerpt>
### Rank 5 of 63 — 0.74
<excerpt title="Gymnastics at the 1996 Summer Olympics – Women's artistic ...">
| Rank | Gymnast | Vault | Uneven Bars | Balance Beam | Floor Exercise | Total |  
| --- | --- | --- | --- | --- | --- | --- |  
|  | Lilia Podkopayeva(UKR) | 9.781 (3) | 9.800 (=2) | 9.787 (=7) | 9.887 (1) | 39.255 |  
|  | Gina Gogean(ROU) | 9.775 (4) | 9.700 (=11) | 9.800 (=5) | 9.800 (3) | 39.075 |  
|  | Simona Amânar(ROU) | 9.843 (1) | 9.762 (=5) | 9.725 (=10) | 9.737 (7) | 39.067 |  
| Lavinia Miloșovici(ROU) | 9.743 (5) | 9.737 (9) | 9.775 (9) | 9.812 (2) |  
| 5 | Mo Huilan(CHN) | 9.799 (2) | 9.800 (=2) | 9.800 (=5) | 9.650 (=13) | 39.049 |  
| 6 | Dina Kochetkova(RUS) | 9.581 (20) | 9.787 (4) | 9.825 (=2) | 9.787 (4) | 38.980 |  
| 7 | Rozalia Galiyeva(RUS) | 9.681 (=13) | 9.762 (=5) | 9.825 (=2) | 9.637 (15) | 38.905 |  

| 8 | Shannon Miller(USA) | 9.724 (6) | 9.750 (8) | 9.862 (1) | 9.475 (29) | 38.811 |  
| 9 | Dominique Moceanu(USA) | 9.706 (=8) | 9.762 (=5) | 9.600 (17) | 9.687 (10) | 38.755 |  
| 10 | Oksana Chusovitina(UZB) | 9.631 (15) | 9.687 (=13) | 9.675 (=14) | 9.750 (=5) | 38.743 |  
| 11 | Qiao Ya(CHN) | 9.718 (7) | 9.600 (20) | 9.725 (=10) | 9.675 (11) | 38.718 |  
| 12 | Yelena Piskun(BLR) | 9.687 (=11) | 9.712 (10) | 9.675 (=14) | 9.575 (=21) | 38.649 |  
| 13 | Isabelle Severino(FRA) | 9.562 (23) | 9.675 (=15) | 9.587 (=18) | 9.700 (=8) | 38.524 |  
| 14 | Svetlana Boginskaya(BLR) | 9.687 (=11) | 9.675 (=15) | 9.537 (21) | 9.600 (=16) | 38.499 |
</excerpt>

## Search 5 — query: "1948 women's all-around gymnastics gold olympics winner USA"
### Rank 1 of 75 — 0.47 (passed on)
<excerpt title="Team USA's First Medal: Women's Gymnastics at London 1948">
The 1948 Olympics, known as the “Austerity Games” due to the persistence of post-war rationing, were held in London. The Olympics were suspended in 1940 and 1944, and London, the city scheduled to host in 1944, was granted the first Games to be held since 1936. While the Games were largely meant as a means to restore the British nation and to reinvigorate the Olympic Movement’s ideals of peace and unity, grim reminders of the recent war and political tensions pervaded the Games, not excluding the women’s gymnastics event.
Germany, the reigning Olympic gold medalist in women’s gymnastics, and Japan were not invited to compete as they were under Allied military occupation, and while the USSR was invited to the Games, they chose not to participate. The Olympic Salute, which was strictly forbidden due to its similarity to the Nazi salute, was also absent from these Games. Athletes were instead instructed to only turn their heads toward the Royal Box, where King George VI sat, during the opening ceremonies. The greatest indication of war, however, was the state of the host city. Laddie Bakanic, a member of the gymnastics team from the United States, remembered arriving at a city that was simply “destroyed,” in her 2012 interview with the New York Times.
The war, and the cancellation of the 1940 and 1944 Olympics, meant, for many gymnasts, that their Olympic dreams would never come to fruition. One such gymnast was Pearl Perkins, a Jewish athlete who won the national all-around title in 1937, 1941, and 1943. Perkins was named to the 1936 United States Olympic team, but her parents did not allow her to attend due to Berlin’s anti-semitic environment. Perkins would continue to train through 1940 and 1944, but her opportunity to participate in the Olympics never arrived.
_Pearl Perkins on the parallel bars_

Helm McKee, the 1938 and 1944 U.S. national champion, had a similar story. She was forbidden from attending the Olympics due to political tensions between her coach and the Amateur Athletics Union. She set her sights on the 1940 and 1944 Olympics, but was never able to compete. Margaret Weissman, the 1939 national champion, would also miss the opportunity to go to the Olympics, along with Roberta Ranck, the first-ever national champion, whose knee injury prevented her from attending in 1936.
Despite the absence of some of its early champions, the United States’ Olympic team would be boosted by the efforts of more recent national champions and gymnasts who had waited patiently for their shot at the Games. The 1945 and 1946 national champion and Olympic team captain Clara Schroth and 1947 and 1948 national champion Helen Shifano, whom the New York Times described as “diminutive stenographers,” were joined by the 1936 Olympian Consetta Lenz, who had two children between her Olympics and had only trained for six months before tryouts. Bakanic, Meta Elste (a former circus performer), Marian Barone, Dorothy Dalton, and Anita Simonis rounded out the team. The United States Olympic Team tryouts took place at Temple University on April 9, four months before the Olympic competition, and the top eight all-around gymnasts were chosen for the team.
This would be the first time the United States had competed internationally in women’s gymnastics since the 1936 Olympic Games, as no team was sent to the 1938 World Championships. At the 1938 Worlds, the women were allowed to compete for individual apparatus titles for the first time, but only Czechoslovakia, Yugoslavia, and Poland competed. The Czech team swept the medals, and Vlasta Děkanová defended her 1934 all-around title and won the vault, balance beam, and parallel bars gold medals. The world championships was also placed on hold, however, and Děkanová would have to wait until 1948 to compete again at the international level.
</excerpt>
### Rank 2 of 75 — 0.35
<excerpt title="Olympic Games History - Women">
**Results at a Glance**
Full Results
_November 23 – December 7, 1956_ _Melbourne, Australia **·**West Melbourne Stadium_
**U.S. Roster**
*   Muriel Davis Grossfeld  
*   Doris Fuchs Brause  
*   Judith Hult Howe  
*   Jacquelyn Klein Fie  
*   Joyce May Racek  
*   Sandra M. Ruddick  
*   Ingeborg Elizabeth Fuchs, alternate  
*   Erna Wachtel, Coach
**Results at a Glance**
Full Results
_July 20 – August 2, 1952_ _Helsinki, Finland **·**Messuhalli_
**U.S. Roster**
*   Marion Twyning Barone  
*   Dorothy Dalton  
*   Meta Neumann Elste  
*   Ruth Grulkowski  
*   Marie Hoesly  
*   Doris Ann Kirkman  
*   Clara Schroth Lomady  
*   Ruth Topalian  
*   Roberta Bonniwell, Coach
**Results at a Glance**
Full Results
_July 30 – August 13, 1948_ _London, England **·**Empress Hall_
**U.S. Roster**
*   Ladislava A. Bakanic  
*   Marion Twyning Barone  
*   Dorothy Dalton  
*   Meta Neumann Elste  
*   Consetta Lenz  
*   Clara Schroth Lomady  
*   Helen Schifano  
*   Anita Simonis Zetts  
*   George Miele, Coach  
*   Joseph Salzman, Coach
**Results at a Glance**
Full Results
_August 1-15, 1936_ _Berlin, Germany **·**Dietrich Eckart Open-Air Theatre_
**U.S. Roster**
*   Jennie Caputo  
*   Consetta Caruccio  
*   Margaret Duff  
*   Irma Haubold  
*   Marie Kibler Phillips  
*   Ada Lunardoni Cumiskey  
*   Adelaide Meyer  
*   Mary Wright  
*   George Miele, Coach  
*   Dr. Margaret Brown, Manager
**Results at a Glance**
Full Results

_July 31 – August 13, 1932_ _Los Angeles, California **·**Olympic Stadium_
**Results at a Glance**
Full Results
_July 29 – August 11, 1928_ _Amsterdam, The Netherlands **·**Olympic Stadium_
**Results at a Glance**
Full Results
</excerpt>
### Rank 3 of 75 — 0.31
<excerpt title="Team USA's First Medal: Women's Gymnastics at London 1948">
Helm McKee, the 1938 and 1944 U.S. national champion, had a similar story. She was forbidden from attending the Olympics due to political tensions between her coach and the Amateur Athletics Union. She set her sights on the 1940 and 1944 Olympics, but was never able to compete. Margaret Weissman, the 1939 national champion, would also miss the opportunity to go to the Olympics, along with Roberta Ranck, the first-ever national champion, whose knee injury prevented her from attending in 1936.
Despite the absence of some of its early champions, the United States’ Olympic team would be boosted by the efforts of more recent national champions and gymnasts who had waited patiently for their shot at the Games. The 1945 and 1946 national champion and Olympic team captain Clara Schroth and 1947 and 1948 national champion Helen Shifano, whom the New York Times described as “diminutive stenographers,” were joined by the 1936 Olympian Consetta Lenz, who had two children between her Olympics and had only trained for six months before tryouts. Bakanic, Meta Elste (a former circus performer), Marian Barone, Dorothy Dalton, and Anita Simonis rounded out the team. The United States Olympic Team tryouts took place at Temple University on April 9, four months before the Olympic competition, and the top eight all-around gymnasts were chosen for the team.
This would be the first time the United States had competed internationally in women’s gymnastics since the 1936 Olympic Games, as no team was sent to the 1938 World Championships. At the 1938 Worlds, the women were allowed to compete for individual apparatus titles for the first time, but only Czechoslovakia, Yugoslavia, and Poland competed. The Czech team swept the medals, and Vlasta Děkanová defended her 1934 all-around title and won the vault, balance beam, and parallel bars gold medals. The world championships was also placed on hold, however, and Děkanová would have to wait until 1948 to compete again at the international level.

When Děkanová was able to compete at the London Olympics in 1948, she was met with the largest international competition that had ever been held for women’s gymnastics. Eleven teams participated, up from eight in 1936 and five in 1928, and eight women competed on each team. Similar to previous Olympics, women would only be allowed to compete in a team final, and they would be given a team score based on group exercises (one with and one without portable apparatuses) and individual apparatuses. However, in this Olympics, women did not compete on bars, but instead competed on the rings. Each team member did a compulsory exercise on rings, along with compulsory and voluntary exercises on beam and vault. Like the 1936 Olympics, the bottom two individuals’ total scores for each team would be dropped, meaning all teams were essentially made up of all-arounders.
The countries competing in the event included Czechoslovakia, Hungary, the United States, Sweden, Holland, Austria, Yugoslavia, Italy, Great Britain, France, and Belgium, and they finished in that order. Czechoslovakia and Hungary, the second and third place winners in 1936, respectively, were neck-and-neck for most of the competition, with the Hungarian team beating the Czech team on beam and the team group exercise, and the Czech team getting higher scores on vault, rings, and the portable apparatus event, beating Hungary by about five points. The United States trailed both teams and earned a solid third place eighteen points behind Hungary.
_The Czech team that won gold at the 1948 Olympic Games_
Considering their reputation as winners of the 1934 and 1938 Worlds and the silver medalists in 1936, it should not be surprising that the Czech team was able to clinch gold; however, the circumstances of these Games were far from ideal for this team. Eliska Misáková, Czech team member and sister of teammate Miloslava Misáková, contracted polio and fell ill upon arriving in England. She was treated and placed in an iron lung, but died on the day the women’s events began. The Czech flag was raised with a black border in her honor during the medal ceremony.
</excerpt>
### Rank 4 of 75 — 0.26
<excerpt title="Team USA's First Medal: Women's Gymnastics at London 1948">
The Czech team also lost their coach, though this did not occur until after the team final. Coach Marie Provaznikova was the FIG’s president of the Women’s Gymnastic Committee as well as the coach of the Czechoslovakian team. Czechoslovakia’s newly communist government was initially reluctant to allow her to go to London due to her status as an enemy of the state. However, they relented, allowing Provaznikova to attend the Olympic Games. While there, she defected, and later moved to the United States, making her the first person to use the Olympics as a means of defecting from a country.
Outside of the tragedy on the Czech side, the event itself was not without mishap. Gymnastics events at this time were usually held outdoors. The women’s team final, which took place at the same time as men’s events, had to be moved indoors due to a rainstorm. There were also concerns over whether the music in women’s routines would distract the men. Ironically, during the competition it was the loud cheering during the the men’s events that would affect the women. One British woman became startled by audience members cheering for a male athlete while she was performing on the rings, and this caused her dismount to become an accidental somersault. She fortunately landed safely, to the audience’s relief.
The question of safety, along with why women competed on rings just this once and never again, was addressed in a Jezebel article in 2012. In it, Bakanic explains that there was “nothing there but a cotton mat on the ground” under the rings, explaining the audience’s reaction when the British gymnast had her mishap on that event. Bakanic also says that the difficulty of their exercises were limited by the available materials and the somewhat dangerous construction of the equipment. The beam, for example, was made of wood without a protective coating. Bakanic does not know why women competed on rings that year but not on bars, and it is unclear why this was not made a permanent practice, or why the apparatuses at worlds were different from the ones at the Olympics.
_Marian Barone of the United States on beam_

The women’s gymnastics event at the 1948 Olympics in London, then, was largely representative of the lack of establishment for the women’s side of the sport at that time, with no individual contests, a transition in apparatuses, and a less-than-clear vision of what role women would take in this sport in general. There were, however, harbingers of the future: the first defection hinted at later Soviet control and dominance in the sport, and the United States’ women took advantage of the Soviet absence to take a medal, similar to the circumstances that would allow them to win their next medal, Mary Lou Retton’s gold in 1984.
It is important to note as well that, while women have come a long way in the sport since 1948, learning more about the history of the sport can give us fodder to question women’s current status in the sport: Why can’t Simone Biles take a stab at rings? Why can’t women have eight events instead of six? Why can’t Viktoria Komova try parallel bars?
**Article by Jessica Taylor Price**
</excerpt>
### Rank 5 of 75 — 0.25
<excerpt title="30 years ago, we became the first women's gymnastics team in history ...">
# Shannon Miller - 30 years ago, we became the first women’s... | Facebook
## Shannon Miller's Post
[](https://www.facebook.com/photo/?fbid=1578773186937892&set=pcb.1578773246937886&__cft__[0]=AZgupN99Eeg18gotP6Tzqj3JgPZhfV2PbtEzTa7yXfeXljm1z4WVi7RzVMBQO2mPYF6_9QsaKbxtTXtxWLyCiF32BK9QkKWUEDgcrcPD-ThSTzPaYUieQlhraIfxLllCXjtQXQkF4Kk9HNVkSHB1uVgBhlZnJFRs&__tn__=*b2H-R)
[](https://www.facebook.com/photo/?fbid=1578773170271227&set=pcb.1578773246937886&__cft__[0]=AZgupN99Eeg18gotP6Tzqj3JgPZhfV2PbtEzTa7yXfeXljm1z4WVi7RzVMBQO2mPYF6_9QsaKbxtTXtxWLyCiF32BK9QkKWUEDgcrcPD-ThSTzPaYUieQlhraIfxLllCXjtQXQkF4Kk9HNVkSHB1uVgBhlZnJFRs&__tn__=*b3H-R)

# Shannon Miller - 30 years ago, we became the first women’s... | Facebook
## Shannon Miller's Post
[ +4](https://www.facebook.com/photo/?fbid=1578773163604561&set=pcb.1578773246937886&__cft__[0]=AZgupN99Eeg18gotP6Tzqj3JgPZhfV2PbtEzTa7yXfeXljm1z4WVi7RzVMBQO2mPYF6_9QsaKbxtTXtxWLyCiF32BK9QkKWUEDgcrcPD-ThSTzPaYUieQlhraIfxLllCXjtQXQkF4Kk9HNVkSHB1uVgBhlZnJFRs&__tn__=*b4H-R)
[Video 2](blob:https://www.facebook.com/ddc47e8b-48f2-40d5-9339-bf2e165f3d25)
![Image 7](blob:http://localhost/85d8b181a20aeb64a3afc2f1c39d2480)
![Image 8](blob:http://localhost/2b45e6f1a2ae097354c0b291152873d5)
All reactions:
28K
1K comments
1.6K shares
Like
Comment
Most relevant
Pam Thompson
When you see something like this at 12 years old, you don't forget it.
</excerpt>

## Search 6 — query: "2008 women's all-around gymnastics gold medal USA Nastia Liukin"
### Rank 1 of 76 — 0.84 (passed on)
<excerpt title="Nastia Liukin">
**Anastasia** "**Nastia**" **Liukin** (; Russian: Анастасия Валерьевна Люкина, IPA:[[ˈlʲʉkʲɪnə]](https://en.wikipedia.org/wiki/Help:IPA/Russian "Help:IPA/Russian"); born October 30, 1989) is a Russian-American former artistic gymnast. She is the 2008 Olympic[all-around](https://en.wikipedia.org/wiki/Gymnastics_at_the_2008_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 2008 Summer Olympics – Women's artistic individual all-around") champion, a five-time Olympic medalist, the 2005 and 2007 World champion on the balance beam, and the 2005 World champion on the uneven bars. She is also a four-time all-around U.S. national champion, winning twice as a junior and twice as a senior. With nine World Championships medals, seven of them individual, Liukin is tied with Shannon Miller for the third-highest tally of World Championship medals among U.S. gymnasts. Liukin also tied Miller's record (later equaled by Simone Biles) as the American gymnast having won the most medals in a single non-boycotted Olympic Games. In October 2011, Liukin announced that she was returning to gymnastics with the hopes of making a second Olympic team. Liukin did not make the 2012 Olympic team and retired from the sport on July 2, 2012.
Since 2010, Liukin has hosted the Nastia Liukin Cup, an annual gymnastics competition for the top Level 10 gymnasts in the United States. She has worked as a gymnastics commentator for NBC Sports and appeared on season 20 of _Dancing with the Stars_. She was inducted into the International Gymnastics Hall of Fame in 2018 and into the U.S. Olympic and Paralympic Hall of Fame in 2019.

## Early life and education
[edit]
Liukin was born on October 30, 1989, in Moscow, Russian SFSR, Soviet Union. She is the only child of two former Soviet champion gymnasts: 1988 Summer Olympics double-gold medalist Valeri Liukin and 1987 World clubs champion in rhythmic gymnastics Anna Kotchneva.[[3]](https://en.wikipedia.org/wiki/Nastia_Liukin#cite_note-usajune08-3)[[4]](https://en.wikipedia.org/wiki/Nastia_Liukin#cite_note-washpost-4) Her nickname _Nastia_ is a Russian diminutive for Anastasia, and she is fluent in English and Russian.[[3]](https://en.wikipedia.org/wiki/Nastia_Liukin#cite_note-usajune08-3)[[5]](https://en.wikipedia.org/wiki/Nastia_Liukin#cite_note-nastialeap-5). The family emigrated to the United States when Nastia was two and a half years old, following the breakup of the Soviet Union and easing of travel restrictions,[[6]](https://en.wikipedia.org/wiki/Nastia_Liukin#cite_note-bio1-6) and settled first in New Orleans before moving to Texas. In 1994, Valeri Liukin teamed up with another former Soviet champion athlete, Yevgeny Marchenko, to open the World Olympic Gymnastics Academy (WOGA) in Plano, Texas.[[3]](https://en.wikipedia.org/wiki/Nastia_Liukin#cite_note-usajune08-3)
</excerpt>
### Rank 2 of 76 — 0.83
<excerpt title="Nastia Liukin">
World Championships 2005 MelbourneUneven bars 2005 Melbourne Balance beam 2007 StuttgartTeam 2007 Stuttgart Balance beam 2005 Melbourne All-around 2005 Melbourne Floor exercise 2006 AarhusTeam 2006 Aarhus Uneven bars 2007 Stuttgart Uneven bars Pan American Games 2003 Santo DomingoTeam 2003 Santo Domingo Balance beam 2007 Rio de JaneiroTeam 2003 Santo Domingo All-around 2007 Rio de Janeiro Uneven bars 2007 Rio de Janeiro Balance beam 2003 Santo Domingo Uneven bars 2003 Santo Domingo Floor exercise Pacific Rim Championships 2006 Honolulu Team 2006 Honolulu Uneven bars 2008 San JoseTeam 2008 San Jose All-around 2008 San Jose Balance beam 2008 San Jose Uneven bars 2006 Honolulu All-around 2006 Honolulu Balance beam FIG World Cup | Event | 1 st | 2 nd | 3 rd | | --- | --- | --- | --- | | All-Around World Cup | 2 | 0 | 0 | |
|  |  
| Education | New York University |  
| Parents | * Valeri Liukin (father) * Anna Kotchneva (mother) |  
| Website | nastialiukin.com |

**Anastasia** "**Nastia**" **Liukin** (; Russian: Анастасия Валерьевна Люкина, IPA:[[ˈlʲʉkʲɪnə]](https://en.wikipedia.org/wiki/Help:IPA/Russian "Help:IPA/Russian"); born October 30, 1989) is a Russian-American former artistic gymnast. She is the 2008 Olympic[all-around](https://en.wikipedia.org/wiki/Gymnastics_at_the_2008_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 2008 Summer Olympics – Women's artistic individual all-around") champion, a five-time Olympic medalist, the 2005 and 2007 World champion on the balance beam, and the 2005 World champion on the uneven bars. She is also a four-time all-around U.S. national champion, winning twice as a junior and twice as a senior. With nine World Championships medals, seven of them individual, Liukin is tied with Shannon Miller for the third-highest tally of World Championship medals among U.S. gymnasts. Liukin also tied Miller's record (later equaled by Simone Biles) as the American gymnast having won the most medals in a single non-boycotted Olympic Games. In October 2011, Liukin announced that she was returning to gymnastics with the hopes of making a second Olympic team. Liukin did not make the 2012 Olympic team and retired from the sport on July 2, 2012.
Since 2010, Liukin has hosted the Nastia Liukin Cup, an annual gymnastics competition for the top Level 10 gymnasts in the United States. She has worked as a gymnastics commentator for NBC Sports and appeared on season 20 of _Dancing with the Stars_. She was inducted into the International Gymnastics Hall of Fame in 2018 and into the U.S. Olympic and Paralympic Hall of Fame in 2019.
</excerpt>
### Rank 3 of 76 — 0.82
<excerpt title="Nastia Liukin">
| Nastia Liukin |  
| --- |  
|  Liukin in 2020 |  
| Personal information |  
| Full name | Anastasia Liukin |  
| Nickname | Nastia |  
| Born | October 30, 1989 (age 37) Moscow, Russian SFSR, Soviet Union |  
| Height | 5 ft 3 in (160 cm)[[1]](https://en.wikipedia.org/wiki/Nastia_Liukin#cite_note-1) |  
| Gymnastics career |  
| Discipline | [Women's artistic gymnastics](https://en.wikipedia.org/wiki/Women's_artistic_gymnastics "Women's artistic gymnastics") |  
| Country represented | * [United States](https://en.wikipedia.org/wiki/United_States_women's_national_artistic_gymnastics_team "United States women's national artistic gymnastics team") * (2002–2009, 2011–2012) |  
| Gym | World Olympic Gymnastics Academy |  
| Head coach | Valeri Liukin |  
| Former coach | Anna Kotchneva |  
| Eponymous skills | Liukin (Balance beam) |  
| Retired | July 2, 2012[[2]](https://en.wikipedia.org/wiki/Nastia_Liukin#cite_note-Boren-2) |  

| Medal record Women's artistic gymnastics Representing the United States | Event | 1 st | 2 nd | 3 rd | | --- | --- | --- | --- | | Olympic Games | 1 | 3 | 1 | | World Championships | 4 | 5 | 0 | | Pan American Games | 3 | 3 | 2 | | Pacific Rim Championships | 5 | 3 | 0 | | American Cup | 2 | 0 | 0 | | Total | 15 | 14 | 3 | Olympic Games 2008 Beijing[All-around](https://en.wikipedia.org/wiki/Gymnastics_at_the_2008_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 2008 Summer Olympics – Women's artistic individual all-around") 2008 Beijing[Team](https://en.wikipedia.org/wiki/Gymnastics_at_the_2008_Summer_Olympics_%E2%80%93_Women's_artistic_team_all-around "Gymnastics at the 2008 Summer Olympics – Women's artistic team all-around") 2008 Beijing[Uneven bars](https://en.wikipedia.org/wiki/Gymnastics_at_the_2008_Summer_Olympics_%E2%80%93_Women's_uneven_bars "Gymnastics at the 2008 Summer Olympics – Women's uneven bars") 2008 Beijing[Balance beam](https://en.wikipedia.org/wiki/Gymnastics_at_the_2008_Summer_Olympics_%E2%80%93_Women's_balance_beam "Gymnastics at the 2008 Summer Olympics – Women's balance beam") 2008 Beijing[Floor exercise](https://en.wikipedia.org/wiki/Gymnastics_at_the_2008_Summer_Olympics_%E2%80%93_Women's_floor "Gymnastics at the 2008 Summer Olympics – Women's floor")
</excerpt>
### Rank 4 of 76 — 0.79
<excerpt title="Nastia Liukin">
| Medal record Women's artistic gymnastics Representing the United States | Event | 1 st | 2 nd | 3 rd | | --- | --- | --- | --- | | Olympic Games | 1 | 3 | 1 | | World Championships | 4 | 5 | 0 | | Pan American Games | 3 | 3 | 2 | | Pacific Rim Championships | 5 | 3 | 0 | | American Cup | 2 | 0 | 0 | | Total | 15 | 14 | 3 | Olympic Games 2008 Beijing[All-around](https://en.wikipedia.org/wiki/Gymnastics_at_the_2008_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 2008 Summer Olympics – Women's artistic individual all-around") 2008 Beijing[Team](https://en.wikipedia.org/wiki/Gymnastics_at_the_2008_Summer_Olympics_%E2%80%93_Women's_artistic_team_all-around "Gymnastics at the 2008 Summer Olympics – Women's artistic team all-around") 2008 Beijing[Uneven bars](https://en.wikipedia.org/wiki/Gymnastics_at_the_2008_Summer_Olympics_%E2%80%93_Women's_uneven_bars "Gymnastics at the 2008 Summer Olympics – Women's uneven bars") 2008 Beijing[Balance beam](https://en.wikipedia.org/wiki/Gymnastics_at_the_2008_Summer_Olympics_%E2%80%93_Women's_balance_beam "Gymnastics at the 2008 Summer Olympics – Women's balance beam") 2008 Beijing[Floor exercise](https://en.wikipedia.org/wiki/Gymnastics_at_the_2008_Summer_Olympics_%E2%80%93_Women's_floor "Gymnastics at the 2008 Summer Olympics – Women's floor")

World Championships 2005 MelbourneUneven bars 2005 Melbourne Balance beam 2007 StuttgartTeam 2007 Stuttgart Balance beam 2005 Melbourne All-around 2005 Melbourne Floor exercise 2006 AarhusTeam 2006 Aarhus Uneven bars 2007 Stuttgart Uneven bars Pan American Games 2003 Santo DomingoTeam 2003 Santo Domingo Balance beam 2007 Rio de JaneiroTeam 2003 Santo Domingo All-around 2007 Rio de Janeiro Uneven bars 2007 Rio de Janeiro Balance beam 2003 Santo Domingo Uneven bars 2003 Santo Domingo Floor exercise Pacific Rim Championships 2006 Honolulu Team 2006 Honolulu Uneven bars 2008 San JoseTeam 2008 San Jose All-around 2008 San Jose Balance beam 2008 San Jose Uneven bars 2006 Honolulu All-around 2006 Honolulu Balance beam FIG World Cup | Event | 1 st | 2 nd | 3 rd | | --- | --- | --- | --- | | All-Around World Cup | 2 | 0 | 0 | |
|  |  
| Education | New York University |  
| Parents | * Valeri Liukin (father) * Anna Kotchneva (mother) |  
| Website | nastialiukin.com |
</excerpt>
### Rank 5 of 76 — 0.79
<excerpt title="Nastia Liukin Wins Gold In Women's All-Around">
# Nastia Liukin Wins Gold In Women's All-Around
Team USA
Team USA
364K subscribers
Subscribe
Subscribed
268
Download
55K views 8y ago
55,375 views • Aug 14, 2018
Relive when USA gymnast Nastia Liukin won gold in the women's all-around in the Olympic Games Beijing 2008.…more
more
How this was made
Auto-dubbed
Audio tracks for some languages were automatically generated. Learn more
Transcript
Follow along using the transcript.
Show transcript

# Nastia Liukin Wins Gold In Women's All-Around
### Team USA 364K subscribers
VideosAbout Facebook Instagram Subscribe to Team USA

# Nastia Liukin Wins Gold In Women's All-Around
## Video details
Date
Aug 14, 2018
Views
55,375
Likes
268
Show less

# Nastia Liukin Wins Gold In Women's All-Around
55,375 views 55K views
Aug 14, 2018
268
Download

# Nastia Liukin Wins Gold In Women's All-Around
## 13 Comments
Sort comments
Sort by
Top Show featured commentsNewest Show recent comments, including potential spam
Add a comment...

# Nastia Liukin Wins Gold In Women's All-Around
## 13 Comments
### @HotMessMemories1
6 years ago
She stuck ALL her landings that day!
Show less Read more
Like
16
Dislike
Reply
1 reply
Hide replies
1 reply

# Nastia Liukin Wins Gold In Women's All-Around
## 13 Comments
### @mowdel88
8 years ago
USA Gymnastics, please post her whole floor routine in the 08 OG AA!
Show less Read more
Like
18
Dislike
Reply

# Nastia Liukin Wins Gold In Women's All-Around
## 13 Comments
### @megan_megan_0001
8 years ago
Perfect vault
Show less Read more
Like
22
Dislike
Reply

# Nastia Liukin Wins Gold In Women's All-Around
## 13 Comments
### @breyonnaleone6357
5 years ago
Such a beautiful gymnast, best vault I’ve ever seen
Show less Read more
Like
6
Dislike
Reply

# Nastia Liukin Wins Gold In Women's All-Around
## 13 Comments
### @uselessjoe
5 years ago
best American gymnast during that time
Show less Read more
Like
4
Dislike
Reply

# Nastia Liukin Wins Gold In Women's All-Around
## 13 Comments
### @thegreenskittle
5 years ago
Impressive confidence and mental strength - she delivered her absolute best when it counted the most. Didn't fail to nerves or silly mistake.
Show less Read more
Like
1
Dislike
Reply

# Nastia Liukin Wins Gold In Women's All-Around
## 13 Comments
### @abbephillips8466
5 years ago
Amazed how Nastia won gold all around for the country but do not see her compensated for all her yrs of dedication.
Show less Read more
Like
1
Dislike
Reply

# Nastia Liukin Wins Gold In Women's All-Around
## 13 Comments
### @maryalthene
7 years ago
Saw her on dwts
Show less Read more
Like
1
Dislike
Reply

# Nastia Liukin Wins Gold In Women's All-Around
## 13 Comments
### @jadecummings8093
8 years ago
Show less Read more
Like
2
Dislike
Reply

# Nastia Liukin Wins Gold In Women's All-Around
## 13 Comments
### @dinachen4602
7 years ago
She looks skinny, but she's strong enough or else she wouldn't have winned the gold medal.
Show less Read more
Like
3
Dislike
Reply
1 reply
Hide replies
1 reply
</excerpt>

## Search 7 — query: "2012 women's all-around olympic gold medal gymnast"
### Rank 1 of 47 — 0.88 (passed on)
<excerpt title="Artistic Gymnastics at the 2012 Summer Olympics">
# Artistic Gymnastics at the 2012 Summer Olympics
## Medals
| Event | Gold | Silver | Bronze |  
| --- | --- | --- | --- |  
| All-Around, Individual, Men | Kohei Uchimura | JPN | Marcel Nguyen | GER | Danell Leyva | USA |  
| Team, Men | People's Republic of China | CHN | Japan | JPN | Great Britain | GBR |  
| Floor Exercise, Men | Zou Kai | CHN | Kohei Uchimura | JPN | Denis Ablyazin | RUS |  
| Vault, Men | Yang Hak-Seon | KOR | Denis Ablyazin | RUS | Ihor Radivilov | UKR |  
| Parallel Bars, Men | Feng Zhe | CHN | Marcel Nguyen | GER | Hamilton Sabot | FRA |  
| Horizontal Bar, Men | Epke Zonderland | NED | Fabian Hambüchen | GER | Zou Kai | CHN |  
| Rings, Men | Arthur Zanetti | BRA | Chen Yibing | CHN | Matteo Morandi | ITA |  
| Pommel Horse, Men | Krisztián Berki | HUN | Louis Smith | GBR | Max Whitlock | GBR |  
| All-Around, Individual, Women | Gabby Douglas | USA | Viktoriya Komova | RUS | Aliya Mustafina | RUS |  
| Team, Women | United States | USA | Russian Federation | RUS | Romania | ROU |  
| Floor Exercise, Women | Aly Raisman | USA | Cătălina Ponor | ROU | Aliya Mustafina | RUS |  
| Vault, Women | Sandra Izbașa | ROU | McKayla Maroney | USA | Mariya Paseka | RUS |  
| Uneven Bars, Women | Aliya Mustafina | RUS | He Kexin | CHN | Beth Tweddle | GBR |  
| Balance Beam, Women | Deng Linlin | CHN | Sui Lu | CHN | Aly Raisman | USA |

# Artistic Gymnastics at the 2012 Summer Olympics
## Medal table
| NOC | Gold | Silver | Bronze | Total |  
| --- | --- | --- | --- | --- |  
| People's Republic of China |  CHN | 4 | 3 | 1 | 8 |  
| United States |  USA | 3 | 1 | 2 | 6 |  
| Russian Federation |  RUS | 1 | 3 | 4 | 8 |  
| Japan |  JPN | 1 | 2 | 0 | 3 |  
| Romania |  ROU | 1 | 1 | 1 | 3 |  
| Brazil |  BRA | 1 | 0 | 0 | 1 |  
| Hungary |  HUN | 1 | 0 | 0 | 1 |  
| Netherlands |  NED | 1 | 0 | 0 | 1 |  
| Republic of Korea |  KOR | 1 | 0 | 0 | 1 |  
| Germany |  GER | 0 | 3 | 0 | 3 |  
| Great Britain |  GBR | 0 | 1 | 3 | 4 |  
| France |  FRA | 0 | 0 | 1 | 1 |  
| Italy |  ITA | 0 | 0 | 1 | 1 |  
| Ukraine |  UKR | 0 | 0 | 1 | 1 |

# Artistic Gymnastics at the 2012 Summer Olympics
## Medal table
### Did you know?
The first and only (thru 2026) ski jumper to win all three events at a single Olympics is Finnish athlete Matti Nykänen, who did so at the 1988 Olympics.
Login | Statistics | About | Image Credits | FAQ | Feedback
© OlyMADMen 2006 — 2026
</excerpt>
### Rank 2 of 47 — 0.83
<excerpt title="Artistic Gymnastics at the 2012 Summer Olympics">
# Olympedia – Artistic Gymnastics at the 2012 Summer Olympics
Toggle navigation
Olympedia
*   Athletes  
    *   Advanced search  
    *   Horse search  
    *   Related Olympians  
    *   Counts  
    *   Doubles  
    *   Lists  
    *   Country representation

    *   Athletes

*   Countries  
    *   Head-to-head  
    *   Best results  
    *   Results comparison

    *   Countries

*   Games  
    *   Games  
    *   Medals  
    *   Results  
    *   Opening ceremony  
    *   Venues

*   Sports  
    *   Disciplines & Sports  
    *   Events

*   IOC  
    *   Organizations  
    *   Definitions  
    *   Awards  
    *   Meetings  
    *   Host city selection

*   Statistics

    *   Medals by country  
    *   Medals by athlete  
    *   Medal tables  
    *   Participations  
    *   Olympic Records  
    *   Age records  
    *   Age at death  
    *   Lists  
    *   Today

    *   Statistics

*   Feedback
1.   Home  
2.   Games  
3.   2012 Summer Olympics  
4.   Artistic Gymnastics

# Artistic Gymnastics at the 2012 Summer Olympics
| Dates | 28 July – 7 August 2012 |  
| --- |  
| Medal Events | 14 |  
| Venues | North Greenwich Arena, Greenwich, London |
The artistic gymnastics events at the 2012 Summer Olympics were held at The O2 Arena in London, referred to as the North Greenwich Arena for the Games, which was also the location for the finals of the basketball tournament. The program remained the same as it had since 1960, with the men’s portion having remained unchanged since 1936, and consisted for 14 events: 8 for men and 6 for women.
China topped the medal table with eight, four of which were gold, repeating their placement from the 2008 Summer Games. The Chinese were far less dominant in London, however, for they had won nine of the 14 gold medals in Beijing and 14 overall. The only other country to capture more than one gold medal was the United States, who won half of the women’s events: the team all-around, the individual all-around, and the floor exercise. The host nation had a relatively good haul as well, with Louis Smith winning the nation’s first silver medal in the sport since 1908 and Great Britain taking home four medals overall, equal to their total from all other Olympics combined. The Netherlands had a historic moment when Epke Zonderland was crowned Olympic champion in the horizontal bar, the nation’s second gold medal, and podium finish, in Olympic gymnastics, with the first having come in 1928. Yang Hak-Seon became South Korea’s first Olympic gymnastics gold medalist after emerging victorious in the men’s horse vault, while Arthur Zanetti of Brazil, winner of the men’s rings event, earned his nation’s first Olympic gymnastics medal ever.

# Artistic Gymnastics at the 2012 Summer Olympics
Zou Kai of China was the most decorated gymnast for the men, winning gold medals in the floor exercise and the team all-around and a bronze medal in the horizontal bar. American Aly Raisman was the star of the women’s events, winning gold in the floor exercise and the team all-around as well as bronze on the balance beam. Two competitors, Yordan Yovchev of Bulgaria and Oksana Chusovitina of Germany, participated in their sixth Olympics in London, a record number of appearances for a gymnast.
</excerpt>
### Rank 3 of 47 — 0.83
<excerpt title="Gabby Douglas [USA] - Women's Individual All-Around">
# Gabby Douglas [USA] - Women's Individual All-Around | Champions of London 2012
## Comments 963
Top Show featured commentsNewest Show recent comments, including potential spam

# Gabby Douglas [USA] - Women's Individual All-Around | Champions of London 2012
## Key moments
### GABRIELLE DOUGLAS (USA) ### GABRIELLE DOUGLAS (USA) 0:17


# Gabby Douglas [USA] - Women's Individual All-Around | Champions of London 2012
## Key moments
### GABRIELLE DOUGLAS (USA)
0:17

# Gabby Douglas [USA] - Women's Individual All-Around | Champions of London 2012
## Key moments
### BEAM ### BEAM 0:24


# Gabby Douglas [USA] - Women's Individual All-Around | Champions of London 2012
## Key moments
### BEAM
0:24

# Gabby Douglas [USA] - Women's Individual All-Around | Champions of London 2012
## Key moments
### VAULT ### VAULT 1:57


# Gabby Douglas [USA] - Women's Individual All-Around | Champions of London 2012
## Key moments
### VAULT
1:57

# Gabby Douglas [USA] - Women's Individual All-Around | Champions of London 2012
## Key moments
### SCORE - 15.966 ### SCORE - 15.966 2:06


# Gabby Douglas [USA] - Women's Individual All-Around | Champions of London 2012
## Key moments
### SCORE - 15.966
2:06

# Gabby Douglas [USA] - Women's Individual All-Around | Champions of London 2012
## Key moments
### UNEVEN BARS ### UNEVEN BARS 2:12


# Gabby Douglas [USA] - Women's Individual All-Around | Champions of London 2012
## Key moments
### UNEVEN BARS
2:12

# Gabby Douglas [USA] - Women's Individual All-Around | Champions of London 2012
## Key moments
### SCORE - 15.733 ### SCORE - 15.733 2:47


# Gabby Douglas [USA] - Women's Individual All-Around | Champions of London 2012
## Key moments
### SCORE - 15.733
2:47

# Gabby Douglas [USA] - Women's Individual All-Around | Champions of London 2012
## Key moments
### FLOOR ### FLOOR 2:52


# Gabby Douglas [USA] - Women's Individual All-Around | Champions of London 2012
## Key moments
### FLOOR
2:52

# Gabby Douglas [USA] - Women's Individual All-Around | Champions of London 2012
## Key moments
### SCORE - 15.033 ### SCORE - 15.033 4:16


# Gabby Douglas [USA] - Women's Individual All-Around | Champions of London 2012
## Key moments
### SCORE - 15.033
4:16

# Gabby Douglas [USA] - Women's Individual All-Around | Champions of London 2012
## Key moments
### TOTAL SCORE - 62.232 ### TOTAL SCORE - 62.232 4:26


# Gabby Douglas [USA] - Women's Individual All-Around | Champions of London 2012
## Key moments
### TOTAL SCORE - 62.232
4:26
Sync to video time
</excerpt>
### Rank 4 of 47 — 0.82
<excerpt title="Gabby Douglas [USA] - Women's Individual All-Around">
# Gabby Douglas [USA] - Women's Individual All-Around | Champions of London 2012
## Video details
### Last 10 Women's Uneven Bars Winners at the Olympics | Top Moments
Olympic Games
903K 6y ago
5:39

# Gabby Douglas [USA] - Women's Individual All-Around | Champions of London 2012
## Video details
### Russia - Synchronized Swimming | Champions of London 2012
Olympic Games
3.9M 10y ago
Show more
Show more
</excerpt>
### Rank 5 of 47 — 0.81
<excerpt title="Fierce Five">
| Fierce Five |  
| --- |  
|  Fierce Five members at the White House. Left to right: Aly Raisman, Gabby Douglas, McKayla Maroney, Kyla Ross, Jordyn Wieber |  
| Personal information |  
| Full name | Gabby Douglas, McKayla Maroney, Aly Raisman, Kyla Ross, and Jordyn Wieber |  
| Gymnastics career |  
| Discipline | [Women's artistic gymnastics](https://en.wikipedia.org/wiki/Women's_artistic_gymnastics "Women's artistic gymnastics") |  
| Country represented | * United States |  
| Medal record Representing United States Olympic Games 2012 London[Team](https://en.wikipedia.org/wiki/Gymnastics_at_the_2012_Summer_Olympics_%E2%80%93_Women's_artistic_team_all-around "Gymnastics at the 2012 Summer Olympics – Women's artistic team all-around") 2012 London[All-around](https://en.wikipedia.org/wiki/Gymnastics_at_the_2012_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 2012 Summer Olympics – Women's artistic individual all-around") 2012 London[Floor exercise](https://en.wikipedia.org/wiki/Gymnastics_at_the_2012_Summer_Olympics_%E2%80%93_Women's_floor "Gymnastics at the 2012 Summer Olympics – Women's floor") 2012 London[Vault](https://en.wikipedia.org/wiki/Gymnastics_at_the_2012_Summer_Olympics_%E2%80%93_Women's_vault "Gymnastics at the 2012 Summer Olympics – Women's vault") 2012 London[Balance beam](https://en.wikipedia.org/wiki/Gymnastics_at_the_2012_Summer_Olympics_%E2%80%93_Women's_balance_beam "Gymnastics at the 2012 Summer Olympics – Women's balance beam") |

The **Fierce Five** was the artistic gymnastics team that won the second team gold medal for the United States in the women's team competition at the 2012 Summer Olympics. Originally referred to as the **Fab Five**, the five members of the team were Gabby Douglas, McKayla Maroney, Aly Raisman, Kyla Ross, and Jordyn Wieber. Later in the Olympic Games, Douglas won a gold medal in the individual all-around event, becoming the first African-American ever to do so; Maroney won silver on the vault; Raisman, the team captain, won bronze on the balance beam and gold on the floor exercise.
Aly Raisman, the oldest team member, became age eligible for senior international competitions in 2010.[[1]](https://en.wikipedia.org/wiki/Fierce_Five#cite_note-1) That year, she helped the American team win the silver medal behind Russia at the World Championships.[[2]](https://en.wikipedia.org/wiki/Fierce_Five#cite_note-2)Gabby Douglas, McKayla Maroney, and Jordyn Wieber began competing in senior competitions in 2011 and competed at the 2011 World Championships alongside Raisman, Sabrina Vega, and Alicia Sacramone.[[3]](https://en.wikipedia.org/wiki/Fierce_Five#cite_note-3) The team won the gold medal by over 4 points ahead of Russia.[[4]](https://en.wikipedia.org/wiki/Fierce_Five#cite_note-4) Wieber then won the individual all-around title while Raisman finished fourth.[[5]](https://en.wikipedia.org/wiki/Fierce_Five#cite_note-5) Maroney won the vault title,[[6]](https://en.wikipedia.org/wiki/Fierce_Five#cite_note-6) and Wieber and Raisman won bronze medals on the balance beam and floor exercise, respectively.[[7]](https://en.wikipedia.org/wiki/Fierce_Five#cite_note-7)
Ross competing at the 2012 U.S. Classic
</excerpt>

## Search 8 — query: "2012 women's all-around gold gymnast USA Gabby Douglas"
### Rank 1 of 63 — 0.85 (passed on)
<excerpt title="Gabby Douglas">
| Gabby Douglas |  
| --- |  
|  Douglas at the 2016 Olympic Games |  
| Personal information |  
| Full name | Gabrielle Christina Victoria Douglas[[1]](https://en.wikipedia.org/wiki/Gabby_Douglas#cite_note-sports-reference-1) |  
| Born | December 31, 1995 (age 30) Newport News, Virginia, U.S. |  
| Height | 5 ft 2.5 in (159 cm)[[2]](https://en.wikipedia.org/wiki/Gabby_Douglas#cite_note-2) |  
| Gymnastics career |  
| Discipline | [Women's artistic gymnastics](https://en.wikipedia.org/wiki/Women's_artistic_gymnastics "Women's artistic gymnastics") |  
| Country represented | * [United States](https://en.wikipedia.org/wiki/United_States_women's_national_artistic_gymnastics_team "United States women's national artistic gymnastics team") * (2008–2012, 2014–2016) |  
| Gym | _WOGA_ _Buckeye Gymnastics_ _[Chow's Gymnastics](https://en.wikipedia.org/wiki/Chow's\_Gymnastics\_and\_Dance\_Institute "Chow's Gymnastics and Dance Institute")_ |  
| Former coaches | Liang Chow Kittia Carpenter Christian Gallardo Valeri Liukin |  

| Medal record Women's artistic gymnastics Representing United States Olympic Games 2012 London[Team](https://en.wikipedia.org/wiki/Gymnastics_at_the_2012_Summer_Olympics_%E2%80%93_Women's_artistic_team_all-around "Gymnastics at the 2012 Summer Olympics – Women's artistic team all-around") 2012 London[All-around](https://en.wikipedia.org/wiki/Gymnastics_at_the_2012_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 2012 Summer Olympics – Women's artistic individual all-around") 2016 Rio de Janeiro[Team](https://en.wikipedia.org/wiki/Gymnastics_at_the_2016_Summer_Olympics_%E2%80%93_Women's_artistic_team_all-around "Gymnastics at the 2016 Summer Olympics – Women's artistic team all-around") World Championships 2011 TokyoTeam 2015 GlasgowTeam 2015 Glasgow All-around Pacific Rim Championships 2012 SeattleTeam 2012 Seattle Uneven bars Pan American Championships 2010 GuadalajaraTeam 2010 Guadalajara Uneven bars FIG World Cup | Event | 1 st | 2 nd | 3 rd | | --- | --- | --- | --- | | All-Around World Cup | 1 | 0 | 0 | |
</excerpt>
### Rank 2 of 63 — 0.85
<excerpt title="Gabby Douglas">
**Gabrielle Christina Victoria Douglas** (born December 31, 1995)[[3]](https://en.wikipedia.org/wiki/Gabby_Douglas#cite_note-usagymprofile-3) is an American artistic gymnast. She is the [2012 Olympic all-around](https://en.wikipedia.org/wiki/Gymnastics_at_the_2012_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 2012 Summer Olympics – Women's artistic individual all-around") gold medalist and the 2015 World all-around silver medalist. She was a member of the gold-winning teams at both the [2012](https://en.wikipedia.org/wiki/Gymnastics_at_the_2012_Summer_Olympics_%E2%80%93_Women's_artistic_team_all-around "Gymnastics at the 2012 Summer Olympics – Women's artistic team all-around") and the [2016 Summer Olympics](https://en.wikipedia.org/wiki/Gymnastics_at_the_2016_Summer_Olympics_%E2%80%93_Women's_artistic_team_all-around "Gymnastics at the 2016 Summer Olympics – Women's artistic team all-around"), dubbed the "Fierce Five" and the "Final Five" by the media, respectively. She was also a member of the gold-winning American teams at the 2011 and the 2015 World Championships. Additionally, she is the 2012 U.S. champion on the uneven bars and the 2016 American Cup all-around champion.
Douglas is the first African American to win an Olympic individual all-around title, and the first U.S. gymnast to win gold in both the individual all-around and team competitions at the same Olympic Games. With a total of six Olympic and World Championship medals, she is the [11th most decorated U.S. female gymnast](https://en.wikipedia.org/wiki/United_States_women's_national_artistic_gymnastics_team#Most_decorated_gymnasts "United States women's national artistic gymnastics team") of all time.

Douglas's gymnastics successes have led to her life story adaptation in the 2014 Lifetimebiopic film, _The Gabby Douglas Story_, as well as her own reality television series, _Douglas Family Gold_. She is the author of two books: _Grace, Gold, and Glory: My Leap of Faith_ and _Raising the Bar_. In 2021, she won the first season of _The Masked Dancer_.
Douglas was born on December 31, 1995, to parents Timothy Douglas and Natalie Hawkins-Douglas,[[4]](https://en.wikipedia.org/wiki/Gabby_Douglas#cite_note-4) in Newport News, Virginia,[[1]](https://en.wikipedia.org/wiki/Gabby_Douglas#cite_note-sports-reference-1) and grew up in nearby Virginia Beach.[[5]](https://en.wikipedia.org/wiki/Gabby_Douglas#cite_note-5) She has two older sisters, Arielle and Joyelle, and one older brother, Johnathan.[[6]](https://en.wikipedia.org/wiki/Gabby_Douglas#cite_note-6) She began training in gymnastics at age six when Arielle convinced their mother to enroll Gabby in classes.[[7]](https://en.wikipedia.org/wiki/Gabby_Douglas#cite_note-7) Her first gym was Excalibur Gymnastics in Virginia Beach.[[8]](https://en.wikipedia.org/wiki/Gabby_Douglas#cite_note-8) At the age of eight, Douglas won the Level 4 all-around gymnastics title at the 2004 Virginia State Championships.[[9]](https://en.wikipedia.org/wiki/Gabby_Douglas#cite_note-9)[[10]](https://en.wikipedia.org/wiki/Gabby_Douglas#cite_note-nbclocalprofile-10)
</excerpt>
### Rank 3 of 63 — 0.85
<excerpt title="Gabby Douglas">
| Medal record Women's artistic gymnastics Representing United States Olympic Games 2012 London[Team](https://en.wikipedia.org/wiki/Gymnastics_at_the_2012_Summer_Olympics_%E2%80%93_Women's_artistic_team_all-around "Gymnastics at the 2012 Summer Olympics – Women's artistic team all-around") 2012 London[All-around](https://en.wikipedia.org/wiki/Gymnastics_at_the_2012_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 2012 Summer Olympics – Women's artistic individual all-around") 2016 Rio de Janeiro[Team](https://en.wikipedia.org/wiki/Gymnastics_at_the_2016_Summer_Olympics_%E2%80%93_Women's_artistic_team_all-around "Gymnastics at the 2016 Summer Olympics – Women's artistic team all-around") World Championships 2011 TokyoTeam 2015 GlasgowTeam 2015 Glasgow All-around Pacific Rim Championships 2012 SeattleTeam 2012 Seattle Uneven bars Pan American Championships 2010 GuadalajaraTeam 2010 Guadalajara Uneven bars FIG World Cup | Event | 1 st | 2 nd | 3 rd | | --- | --- | --- | --- | | All-Around World Cup | 1 | 0 | 0 | |

**Gabrielle Christina Victoria Douglas** (born December 31, 1995)[[3]](https://en.wikipedia.org/wiki/Gabby_Douglas#cite_note-usagymprofile-3) is an American artistic gymnast. She is the [2012 Olympic all-around](https://en.wikipedia.org/wiki/Gymnastics_at_the_2012_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 2012 Summer Olympics – Women's artistic individual all-around") gold medalist and the 2015 World all-around silver medalist. She was a member of the gold-winning teams at both the [2012](https://en.wikipedia.org/wiki/Gymnastics_at_the_2012_Summer_Olympics_%E2%80%93_Women's_artistic_team_all-around "Gymnastics at the 2012 Summer Olympics – Women's artistic team all-around") and the [2016 Summer Olympics](https://en.wikipedia.org/wiki/Gymnastics_at_the_2016_Summer_Olympics_%E2%80%93_Women's_artistic_team_all-around "Gymnastics at the 2016 Summer Olympics – Women's artistic team all-around"), dubbed the "Fierce Five" and the "Final Five" by the media, respectively. She was also a member of the gold-winning American teams at the 2011 and the 2015 World Championships. Additionally, she is the 2012 U.S. champion on the uneven bars and the 2016 American Cup all-around champion.
Douglas is the first African American to win an Olympic individual all-around title, and the first U.S. gymnast to win gold in both the individual all-around and team competitions at the same Olympic Games. With a total of six Olympic and World Championship medals, she is the [11th most decorated U.S. female gymnast](https://en.wikipedia.org/wiki/United_States_women's_national_artistic_gymnastics_team#Most_decorated_gymnasts "United States women's national artistic gymnastics team") of all time.
</excerpt>
### Rank 4 of 63 — 0.78
<excerpt title="Gabby Douglas [USA] - Women's Individual All-Around">
# Gabby Douglas [USA] - Women's Individual All-Around | Champions of London 2012
## Comments 963
Top Show featured commentsNewest Show recent comments, including potential spam

# Gabby Douglas [USA] - Women's Individual All-Around | Champions of London 2012
## Key moments
### GABRIELLE DOUGLAS (USA) ### GABRIELLE DOUGLAS (USA) 0:17


# Gabby Douglas [USA] - Women's Individual All-Around | Champions of London 2012
## Key moments
### GABRIELLE DOUGLAS (USA)
0:17

# Gabby Douglas [USA] - Women's Individual All-Around | Champions of London 2012
## Key moments
### BEAM ### BEAM 0:24


# Gabby Douglas [USA] - Women's Individual All-Around | Champions of London 2012
## Key moments
### BEAM
0:24

# Gabby Douglas [USA] - Women's Individual All-Around | Champions of London 2012
## Key moments
### VAULT ### VAULT 1:57


# Gabby Douglas [USA] - Women's Individual All-Around | Champions of London 2012
## Key moments
### VAULT
1:57

# Gabby Douglas [USA] - Women's Individual All-Around | Champions of London 2012
## Key moments
### SCORE - 15.966 ### SCORE - 15.966 2:06


# Gabby Douglas [USA] - Women's Individual All-Around | Champions of London 2012
## Key moments
### SCORE - 15.966
2:06

# Gabby Douglas [USA] - Women's Individual All-Around | Champions of London 2012
## Key moments
### UNEVEN BARS ### UNEVEN BARS 2:12


# Gabby Douglas [USA] - Women's Individual All-Around | Champions of London 2012
## Key moments
### UNEVEN BARS
2:12

# Gabby Douglas [USA] - Women's Individual All-Around | Champions of London 2012
## Key moments
### SCORE - 15.733 ### SCORE - 15.733 2:47


# Gabby Douglas [USA] - Women's Individual All-Around | Champions of London 2012
## Key moments
### SCORE - 15.733
2:47

# Gabby Douglas [USA] - Women's Individual All-Around | Champions of London 2012
## Key moments
### FLOOR ### FLOOR 2:52


# Gabby Douglas [USA] - Women's Individual All-Around | Champions of London 2012
## Key moments
### FLOOR
2:52

# Gabby Douglas [USA] - Women's Individual All-Around | Champions of London 2012
## Key moments
### SCORE - 15.033 ### SCORE - 15.033 4:16


# Gabby Douglas [USA] - Women's Individual All-Around | Champions of London 2012
## Key moments
### SCORE - 15.033
4:16

# Gabby Douglas [USA] - Women's Individual All-Around | Champions of London 2012
## Key moments
### TOTAL SCORE - 62.232 ### TOTAL SCORE - 62.232 4:26


# Gabby Douglas [USA] - Women's Individual All-Around | Champions of London 2012
## Key moments
### TOTAL SCORE - 62.232
4:26
Sync to video time
</excerpt>
### Rank 5 of 63 — 0.76
<excerpt title="Gabby Douglas">
#### 2012 Summer Olympics
[edit]
Douglas (right) during the [all-around final](https://en.wikipedia.org/wiki/Gymnastics_at_the_2012_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 2012 Summer Olympics – Women's artistic individual all-around") at the 2012 Summer Olympics
At the 2012 Summer Olympics at the O2 Arena (North Greenwich Arena) in London, Douglas and her teammates (nicknamed the "Fierce Five") advanced to the team final in first place. Additionally, Douglas advanced to the all-around, uneven bars, and balance beam finals.[[55]](https://en.wikipedia.org/wiki/Gabby_Douglas#cite_note-55)[[56]](https://en.wikipedia.org/wiki/Gabby_Douglas#cite_note-56) They won the [team event](https://en.wikipedia.org/wiki/Gymnastics_at_the_2012_Summer_Olympics_%E2%80%93_Women's_artistic_team_all-around "Gymnastics at the 2012 Summer Olympics – Women's artistic team all-around") gold medal with Douglas contributing on all four apparatuses.[[57]](https://en.wikipedia.org/wiki/Gabby_Douglas#cite_note-57) They were the first American team to do so since the "Magnificent Seven" won at the 1996 Summer Olympics in Atlanta, Georgia.[[58]](https://en.wikipedia.org/wiki/Gabby_Douglas#cite_note-olympicteamgold-58)[[59]](https://en.wikipedia.org/wiki/Gabby_Douglas#cite_note-59)

#### 2012 Summer Olympics
Douglas won the gold medal in the [all-around final](https://en.wikipedia.org/wiki/Gymnastics_at_the_2012_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 2012 Summer Olympics – Women's artistic individual all-around") with a total score of 62.232.[[60]](https://en.wikipedia.org/wiki/Gabby_Douglas#cite_note-60) She became the first African American woman,[[61]](https://en.wikipedia.org/wiki/Gabby_Douglas#cite_note-61) as well as the first woman of color of any nationality, to win the event.[[62]](https://en.wikipedia.org/wiki/Gabby_Douglas#cite_note-62) She also became the fourth American woman to win Olympic all-around gold as well as the third straight to do so after Mary Lou Retton in Los Angeles in 1984, Carly Patterson in Athens in 2004 and Nastia Liukin in Beijing in 2008, all of whom were at the venue and watched Douglas equal their feat.[[63]](https://en.wikipedia.org/wiki/Gabby_Douglas#cite_note-corneau-63)[[64]](https://en.wikipedia.org/wiki/Gabby_Douglas#cite_note-64) She also became the first American gymnast ever to win both the team and individual all-around gold at the same Olympics.[[65]](https://en.wikipedia.org/wiki/Gabby_Douglas#cite_note-65)
</excerpt>

## Search 9 — query: "1948 women's all-around gymnastics gold winner United States"
### Rank 1 of 99 — 0.53 (passed on)
<excerpt title="Team USA's First Medal: Women's Gymnastics at London 1948">
The 1948 Olympics, known as the “Austerity Games” due to the persistence of post-war rationing, were held in London. The Olympics were suspended in 1940 and 1944, and London, the city scheduled to host in 1944, was granted the first Games to be held since 1936. While the Games were largely meant as a means to restore the British nation and to reinvigorate the Olympic Movement’s ideals of peace and unity, grim reminders of the recent war and political tensions pervaded the Games, not excluding the women’s gymnastics event.
Germany, the reigning Olympic gold medalist in women’s gymnastics, and Japan were not invited to compete as they were under Allied military occupation, and while the USSR was invited to the Games, they chose not to participate. The Olympic Salute, which was strictly forbidden due to its similarity to the Nazi salute, was also absent from these Games. Athletes were instead instructed to only turn their heads toward the Royal Box, where King George VI sat, during the opening ceremonies. The greatest indication of war, however, was the state of the host city. Laddie Bakanic, a member of the gymnastics team from the United States, remembered arriving at a city that was simply “destroyed,” in her 2012 interview with the New York Times.
The war, and the cancellation of the 1940 and 1944 Olympics, meant, for many gymnasts, that their Olympic dreams would never come to fruition. One such gymnast was Pearl Perkins, a Jewish athlete who won the national all-around title in 1937, 1941, and 1943. Perkins was named to the 1936 United States Olympic team, but her parents did not allow her to attend due to Berlin’s anti-semitic environment. Perkins would continue to train through 1940 and 1944, but her opportunity to participate in the Olympics never arrived.
_Pearl Perkins on the parallel bars_

Helm McKee, the 1938 and 1944 U.S. national champion, had a similar story. She was forbidden from attending the Olympics due to political tensions between her coach and the Amateur Athletics Union. She set her sights on the 1940 and 1944 Olympics, but was never able to compete. Margaret Weissman, the 1939 national champion, would also miss the opportunity to go to the Olympics, along with Roberta Ranck, the first-ever national champion, whose knee injury prevented her from attending in 1936.
Despite the absence of some of its early champions, the United States’ Olympic team would be boosted by the efforts of more recent national champions and gymnasts who had waited patiently for their shot at the Games. The 1945 and 1946 national champion and Olympic team captain Clara Schroth and 1947 and 1948 national champion Helen Shifano, whom the New York Times described as “diminutive stenographers,” were joined by the 1936 Olympian Consetta Lenz, who had two children between her Olympics and had only trained for six months before tryouts. Bakanic, Meta Elste (a former circus performer), Marian Barone, Dorothy Dalton, and Anita Simonis rounded out the team. The United States Olympic Team tryouts took place at Temple University on April 9, four months before the Olympic competition, and the top eight all-around gymnasts were chosen for the team.
This would be the first time the United States had competed internationally in women’s gymnastics since the 1936 Olympic Games, as no team was sent to the 1938 World Championships. At the 1938 Worlds, the women were allowed to compete for individual apparatus titles for the first time, but only Czechoslovakia, Yugoslavia, and Poland competed. The Czech team swept the medals, and Vlasta Děkanová defended her 1934 all-around title and won the vault, balance beam, and parallel bars gold medals. The world championships was also placed on hold, however, and Děkanová would have to wait until 1948 to compete again at the international level.
</excerpt>
### Rank 2 of 99 — 0.37
<excerpt title="United States women's national artistic gymnastics team">
[1992](https://en.wikipedia.org/wiki/Gymnastics_at_the_1992_Summer_Olympics_%E2%80%93_Women's_artistic_team_all-around "Gymnastics at the 1992 Summer Olympics – Women's artistic team all-around") and [2000](https://en.wikipedia.org/wiki/Gymnastics_at_the_2000_Summer_Olympics_%E2%80%93_Women's_artistic_team_all-around "Gymnastics at the 2000 Summer Olympics – Women's artistic team all-around").[[2]](https://en.wikipedia.org/wiki/United_States_women's_national_artistic_gymnastics_team#cite_note-2) The 2016 team name alluded to Márta Károlyi's final team to coach and that the team structure will be changed to four members beginning with the 2020 Olympic Games.
The [1988 Olympic Games](https://en.wikipedia.org/wiki/Gymnastics_at_the_1988_Summer_Olympics_%E2%80%93_Women's_artistic_team_all-around "Gymnastics at the 1988 Summer Olympics – Women's artistic team all-around") was the only year in which the team did not medal since its formation in 1982; they missed the bronze medal by one controversial deduction. Six American women have won the Olympic individual all-around title, including six consecutive titles from 2004–24: Mary Lou Retton (1984), Carly Patterson (2004), Nastia Liukin (2008), Gabby Douglas (2012), Simone Biles (2016 and 2024), and Sunisa Lee (2020). The most decorated American gymnast at the Olympics, with eleven medals, is Simone Biles (7 gold, 2 silvers, 2 bronze).

### World Championships
[edit]
The United States women team is currently third in the all-time medal count for the World Artistic Gymnastics Championships. The first American gymnast to win a medal at the World Championships was Cathy Rigby who won silver on beam in 1970.[[3]](https://en.wikipedia.org/wiki/United_States_women's_national_artistic_gymnastics_team#cite_note-3) The first female American gymnast to win a world title was Marcia Frederick in 1978 on the uneven bars.[[4]](https://en.wikipedia.org/wiki/United_States_women's_national_artistic_gymnastics_team#cite_note-4) The most decorated American gymnast at the World Championships is Simone Biles, who won 25 medals (19 gold, 3 silver and 3 bronze) from 2013 to 2019.[[5]](https://en.wikipedia.org/wiki/United_States_women's_national_artistic_gymnastics_team#cite_note-espn.com-5) The United States won team gold in 2003, 2007, 2011, 2014, 2015, 2018, 2019, 2022, and 2023 .[[6]](https://en.wikipedia.org/wiki/United_States_women's_national_artistic_gymnastics_team#cite_note-usagym.org-6) Additionally, nine American women have won the individual World all-around title: Kim Zmeskal (1991), Shannon Miller (1993–1994), Chellsie Memmel (2005), Shawn Johnson (2007), Bridget Sloan (2009), Jordyn Wieber (2011), Simone Biles (2013–2015, 2018–2019, 2023), Morgan Hurd (2017), and Skye Blakely (2026). Biles is the only American gymnast to win both the Olympic and World all-around titles.

### World Championships
As of August 9, 2026:[[7]](https://en.wikipedia.org/wiki/United_States_women's_national_artistic_gymnastics_team#cite_note-7)
</excerpt>
### Rank 3 of 99 — 0.35
<excerpt title="Olympic Games History - Women">
**Results at a Glance**
Full Results
_November 23 – December 7, 1956_ _Melbourne, Australia **·**West Melbourne Stadium_
**U.S. Roster**
*   Muriel Davis Grossfeld  
*   Doris Fuchs Brause  
*   Judith Hult Howe  
*   Jacquelyn Klein Fie  
*   Joyce May Racek  
*   Sandra M. Ruddick  
*   Ingeborg Elizabeth Fuchs, alternate  
*   Erna Wachtel, Coach
**Results at a Glance**
Full Results
_July 20 – August 2, 1952_ _Helsinki, Finland **·**Messuhalli_
**U.S. Roster**
*   Marion Twyning Barone  
*   Dorothy Dalton  
*   Meta Neumann Elste  
*   Ruth Grulkowski  
*   Marie Hoesly  
*   Doris Ann Kirkman  
*   Clara Schroth Lomady  
*   Ruth Topalian  
*   Roberta Bonniwell, Coach
**Results at a Glance**
Full Results
_July 30 – August 13, 1948_ _London, England **·**Empress Hall_
**U.S. Roster**
*   Ladislava A. Bakanic  
*   Marion Twyning Barone  
*   Dorothy Dalton  
*   Meta Neumann Elste  
*   Consetta Lenz  
*   Clara Schroth Lomady  
*   Helen Schifano  
*   Anita Simonis Zetts  
*   George Miele, Coach  
*   Joseph Salzman, Coach
**Results at a Glance**
Full Results
_August 1-15, 1936_ _Berlin, Germany **·**Dietrich Eckart Open-Air Theatre_
**U.S. Roster**
*   Jennie Caputo  
*   Consetta Caruccio  
*   Margaret Duff  
*   Irma Haubold  
*   Marie Kibler Phillips  
*   Ada Lunardoni Cumiskey  
*   Adelaide Meyer  
*   Mary Wright  
*   George Miele, Coach  
*   Dr. Margaret Brown, Manager
**Results at a Glance**
Full Results

_July 31 – August 13, 1932_ _Los Angeles, California **·**Olympic Stadium_
**Results at a Glance**
Full Results
_July 29 – August 11, 1928_ _Amsterdam, The Netherlands **·**Olympic Stadium_
**Results at a Glance**
Full Results
</excerpt>
### Rank 4 of 99 — 0.34
<excerpt title="United States women's national artistic gymnastics team">
As of 2026, the U.S. team is the reigning Olympic team gold medalist, with the five gymnasts nicknamed the "Golden Girls."
The U.S. women won the team competition bronze medal at the 1948 Summer Olympics. Afterwards, they did not win another Summer Olympics or World Championships medal until 1984 when the Olympic team won silver. During that competition, Mary Lou Retton also became the first American to win the individual all-around gold medal. The Americans started consistently winning Olympic and World team medals in the early 1990s with future Hall of Famers Shannon Miller and Dominique Dawes. The 1996 Olympic team, known as the Magnificent Seven, was the first American team to win Olympic gold. An iconic moment in the sport's history came late in the competition, when an injured Kerri Strug stuck a vault to secure the title. After 1996, the team regressed for several years as their stars took breaks from competing.
Márta Károlyi headed the program after the 2000 Olympics, ushering in an era of success for the U.S. team as they became one of the most dominant countries in women's gymnastics. The U.S. team has medalled in every Olympics and Worlds since 2000. They won their first team World gold medal in 2003. At the 2004 Olympics, they won the team silver, and Carly Patterson became the second American gymnast to win the individual all-around and the first to do so at a non-Boycotted Olympic Games. The U.S. team continued their success into the next quad. They won another Olympic silver medal in 2008. Nastia Liukin and Shawn Johnson were two of the best gymnasts of their era and finished first and second in the 2008 individual all-around.

They won gold at the 2011 World Championships and then won gold at the 2012 Olympics by over five points. The 2012 team was nicknamed the Fierce Five and included Gabby Douglas, the first African American woman to win the Olympic individual all-around. In 2013, Simone Biles started her senior career and helped the U.S. team dominate the sport through 2016. In addition to the team gold medals, Biles won the individual all-around at the World Championships and Olympic Games for four straight years. The 2016 Olympic team, featuring Biles and veterans Douglas and Aly Raisman, was named the Final Five. They won the team competition by more than eight points.
The USA Gymnastics women have won the Olympic Gold four times, in [1996](https://en.wikipedia.org/wiki/Gymnastics_at_the_1996_Summer_Olympics_%E2%80%93_Women's_artistic_team_all-around "Gymnastics at the 1996 Summer Olympics – Women's artistic team all-around"), [2012](https://en.wikipedia.org/wiki/Gymnastics_at_the_2012_Summer_Olympics_%E2%80%93_Women's_artistic_team_all-around "Gymnastics at the 2012 Summer Olympics – Women's artistic team all-around"), [2016](https://en.wikipedia.org/wiki/Gymnastics_at_the_2016_Summer_Olympics_%E2%80%93_Women's_artistic_team_all-around "Gymnastics at the 2016 Summer Olympics – Women's artistic team all-around"), and [2024](https://en.wikipedia.org/wiki/Gymnastics_at_the_2024_Summer_Olympics_%E2%80%93_Women's_artistic_team_all-around "Gymnastics at the 2024 Summer Olympics – Women's artistic team all-around"). These successes led to the nicknames Magnificent Seven, Fierce Five, Final Five, and Golden Girls, respectively.
</excerpt>
### Rank 5 of 99 — 0.30
<excerpt title="30 years ago, we became the first women's gymnastics team in history ...">
# Shannon Miller - 30 years ago, we became the first women’s... | Facebook
## Shannon Miller's Post
[](https://www.facebook.com/photo/?fbid=1578773186937892&set=pcb.1578773246937886&__cft__[0]=AZgupN99Eeg18gotP6Tzqj3JgPZhfV2PbtEzTa7yXfeXljm1z4WVi7RzVMBQO2mPYF6_9QsaKbxtTXtxWLyCiF32BK9QkKWUEDgcrcPD-ThSTzPaYUieQlhraIfxLllCXjtQXQkF4Kk9HNVkSHB1uVgBhlZnJFRs&__tn__=*b2H-R)
[](https://www.facebook.com/photo/?fbid=1578773170271227&set=pcb.1578773246937886&__cft__[0]=AZgupN99Eeg18gotP6Tzqj3JgPZhfV2PbtEzTa7yXfeXljm1z4WVi7RzVMBQO2mPYF6_9QsaKbxtTXtxWLyCiF32BK9QkKWUEDgcrcPD-ThSTzPaYUieQlhraIfxLllCXjtQXQkF4Kk9HNVkSHB1uVgBhlZnJFRs&__tn__=*b3H-R)

# Shannon Miller - 30 years ago, we became the first women’s... | Facebook
## Shannon Miller's Post
[ +4](https://www.facebook.com/photo/?fbid=1578773163604561&set=pcb.1578773246937886&__cft__[0]=AZgupN99Eeg18gotP6Tzqj3JgPZhfV2PbtEzTa7yXfeXljm1z4WVi7RzVMBQO2mPYF6_9QsaKbxtTXtxWLyCiF32BK9QkKWUEDgcrcPD-ThSTzPaYUieQlhraIfxLllCXjtQXQkF4Kk9HNVkSHB1uVgBhlZnJFRs&__tn__=*b4H-R)
[Video 2](blob:https://www.facebook.com/ddc47e8b-48f2-40d5-9339-bf2e165f3d25)
![Image 7](blob:http://localhost/85d8b181a20aeb64a3afc2f1c39d2480)
![Image 8](blob:http://localhost/2b45e6f1a2ae097354c0b291152873d5)
All reactions:
28K
1K comments
1.6K shares
Like
Comment
Most relevant
Pam Thompson
When you see something like this at 12 years old, you don't forget it.
</excerpt>

## Search 10 — query: "Barack Obama served two full terms succeeded by Donald Trump"
### Rank 1 of 151 — 0.77 (passed on)
<excerpt title="Presidency of Barack Obama">
Barack Obama's tenure as the 44th president of the United States began with his first inauguration on January 20, 2009, and ended on January 20, 2017. Obama, a Democrat from Illinois, took office after defeating the Republican nominee John McCain in the 2008 presidential election. Four years later, he won re-election in the 2012 presidential election, after defeating the Republican nominee Mitt Romney. Alongside Obama's presidency, the Democratic Party also held their majorities in the House of Representatives during the 111th U.S. Congress following the 2008 elections, thereby attained an overall federal government trifecta. Obama is the first African American president, the first multiracial president, the first non-white president,[a] and the first president born in Hawaii. Obama was constitutionally limited to two terms (the second re-elected Democrat President to be so) and was succeeded by Republican Donald Trump, who won the 2016 presidential election against Obama's preferred successor, Hillary Clinton. Historians and political scientists rank him among the upper tier in historical rankings of American presidents.
Obama's accomplishments during the first 100 days of his presidency included signing the Lilly Ledbetter Fair Pay Act of 2009; relaxing the statute of limitations for equal-pay lawsuits;[2] signing into law the expanded Children's Health Insurance Program (S-CHIP); winning approval of a congressional budget resolution that put Congress on record as dedicated to dealing with major health care reform legislation in 2009; implementing new ethics guidelines designed to significantly curtail the influence of lobbyists on the executive branch; breaking from the Bush administration on a number of policy fronts, except for Iraq, in which he followed through on Bush's Iraq withdrawal of US troops;[3] supporting the UN declaration on sexual orientation and gender identity; and lifting the 7½-year ban on federal funding for embryonic stem cell research.[4] Obama also ordered the closure of the Guantanamo Bay detention camp, in Cuba, though it remained open throughout his presidency. He lifted some travel and money restrictions to the island.[3]

Obama signed many landmark bills into law during his first two years in office. The main reforms include: the Affordable Care Act, sometimes referred to as "the ACA" or "Obamacare", the Dodd–Frank Wall Street Reform and Consumer Protection Act, and the Don't Ask, Don't Tell Repeal Act of 2010. The American Recovery and Reinvestment Act and Tax Relief, Unemployment Insurance Reauthorization, and Job Creation Act served as economic stimuli amidst the Great Recession. After a lengthy debate over the national debt limit, he signed the Budget Control Act of 2011 and the American Taxpayer Relief Act of 2012. In foreign policy, he increased US troop levels in Afghanistan, reduced nuclear weapons with the United States–Russia New START treaty, and ended military involvement in the Iraq War. He gained widespread praise for ordering Operation Neptune Spear, the raid that killed Osama bin Laden, who was responsible for the September 11 attacks. In 2011, Obama ordered the drone-strike killing in Yemen of al-Qaeda operative Anwar al-Awlaki, who was an American citizen. He ordered military involvement in Libya in order to implement UN Security Council Resolution 1973, contributing to the overthrow of Muammar Gaddafi.
</excerpt>
### Rank 2 of 151 — 0.77
<excerpt title="Presidency of Barack Obama">
Jump to content  
Main menu  
Search  
Donate  
Create account  
Log in  
Contents hide  
(Top)  
Major acts and legislation  
Milestones  
Toggle Milestones subsection  
Administration  
Toggle Administration subsection  
Judicial appointments  
Toggle Judicial appointments subsection  
Domestic affairs  
Toggle Domestic affairs subsection  
Foreign affairs  
Toggle Foreign affairs subsection  
Ethics  
Toggle Ethics subsection  
Elections during the Obama presidency  
Toggle Elections during the Obama presidency subsection  
Approval ratings and other opinions  
See also  
Notes  
References  
Further reading  
Toggle Further reading subsection  
External links  
Presidency of Barack Obama  
17 languages  
Article  
Talk  
Read  
View source  
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
For a chronological guide, see Timeline of the Barack Obama presidency.  
Official portrait, 2009
Presidency of Barack Obama  
January 20, 2009 – January 20, 2017
Vice President
Joe Biden
Cabinet	Full list  
Party	Democratic  
Election	  
20082012
Seat	White House
← George W. Bush  
Donald Trump (I) →
Seal of the President
Archived website  
Library website
This article is part of  
a series about  
Barack Obama
show  
Personal  
show  
Illinois State Senator and U.S. Senator from Illinois  
show  
44th President of the United States  
show  
Tenure  
show  
Policies  
show  
Appointments  
show  
Presidential campaigns
vte

Barack Obama's tenure as the 44th president of the United States began with his first inauguration on January 20, 2009, and ended on January 20, 2017. Obama, a Democrat from Illinois, took office after defeating the Republican nominee John McCain in the 2008 presidential election. Four years later, he won re-election in the 2012 presidential election, after defeating the Republican nominee Mitt Romney. Alongside Obama's presidency, the Democratic Party also held their majorities in the House of Representatives during the 111th U.S. Congress following the 2008 elections, thereby attained an overall federal government trifecta. Obama is the first African American president, the first multiracial president, the first non-white president,[a] and the first president born in Hawaii. Obama was constitutionally limited to two terms (the second re-elected Democrat President to be so) and was succeeded by Republican Donald Trump, who won the 2016 presidential election against Obama's preferred successor, Hillary Clinton. Historians and political scientists rank him among the upper tier in historical rankings of American presidents.
Obama's accomplishments during the first 100 days of his presidency included signing the Lilly Ledbetter Fair Pay Act of 2009; relaxing the statute of limitations for equal-pay lawsuits;[2] signing into law the expanded Children's Health Insurance Program (S-CHIP); winning approval of a congressional budget resolution that put Congress on record as dedicated to dealing with major health care reform legislation in 2009; implementing new ethics guidelines designed to significantly curtail the influence of lobbyists on the executive branch; breaking from the Bush administration on a number of policy fronts, except for Iraq, in which he followed through on Bush's Iraq withdrawal of US troops;[3] supporting the UN declaration on sexual orientation and gender identity; and lifting the 7½-year ban on federal funding for embryonic stem cell research.[4] Obama also ordered the closure of the Guantanamo Bay detention camp, in Cuba, though it remained open throughout his presidency. He lifted some travel and money restrictions to the island.[3]
</excerpt>
### Rank 3 of 151 — 0.61
<excerpt title="The Uncertain Legacy of Barack Obama '83 | Columbia College Today">
O n January 20, 2009, Barack Obama ’83 (his graduation coincided with my first year teaching at Columbia) became the 44th President of the United States and the nation’s first black President. He will leave office in January 2017 having served two full terms. While Obama’s election was an historic event, filled with high hopes, his accomplishments and legacy are controversial and will be debated for years.
When Democratic Party candidate Obama defeated Sen. John McCain (R-Ariz.) in 2008, George W. Bush’s presidency was ending at a low point, directly related to both the military quagmire that occurred after the United States’ invasion of Iraq in 2003 and to the financial crisis at that time. The nation was entering into a Great Recession. Dealing with this posed a great challenge, but expectations were high — indeed too high. Working in Obama’s favor was his strong electoral showing: 53 percent to 46 percent in the popular vote and a 365–173 rout in the Electoral College. The Democrats won a large majority in the House of Representatives and for a brief period in 2009 had a 60–40 libuster-proof Senate majority. Working against Obama was an enormous (and still growing) partisan divide among Democratic Party and Republican Party leaders and voters. Widely written about by political scientists (myself included), this ideologically-driven partisan divide emerged in the 1970s and took off by the 1990s; Bush — who aspired to be a “uniter” not a “divider” — had hoped to end it but failed.

It’s important to consider the history here. The two major parties had been ideologically mixed after being realigned in the 1930s. Southern Democrats who were conservative on racial and labor issues countered the northern liberal wing of the party; moderate Republicans who were liberal on civil rights and other issues countered their party’s economic conservatism. The balance slowly unraveled with the ascendancy of northern Democrats in tandem with the Civil Rights movement, which led the Democrats, spurred by President Lyndon Johnson, to become the more liberal party on racial issues with the passage of landmark civil rights and voting rights legislation in 1964 and 1965. Over time, southern conservative Democrats left the party and the Republicans began to pick them up as part of Republican President Richard Nixon’s “southern strategy” in 1968. As new issues arose, intra-party competition led the parties to divide ideologically, with Democrats as liberals and Republicans as conservatives on economic and regulatory issues as well as on individual rights and liberties, with moderates slowly disappearing from both parties, especially the GOP.
By 2008, virtually every major issue divided the parties. Political emotions were running high, and there was a widening rift in national security and foreign policy as the Democrats and Republicans came to differ on the use of diplomacy versus the unilateral use of military force. Adding to the conflict was the fact that with the 1980 Senate and 1994 House elections, the parties became evenly matched for control of all branches of government. This increased the stakes in national elections, and it explains why Senate Minority Leader Mitch McConnell (R-Ky.) said in October 2010, “The single most important thing we want to achieve is for President Obama to be a one-term president.”
</excerpt>
### Rank 4 of 151 — 0.59
<excerpt title="Presidency of Barack Obama">
After winning re-election by defeating Republican opponent Mitt Romney, Obama was sworn in for a second term on January 20, 2013. During this term, he condemned the 2013 Snowden leaks as unpatriotic, but called for more restrictions on the National Security Agency (NSA) to address privacy issues. Obama also promoted inclusion for LGBT Americans. His administration filed briefs that urged the Supreme Court to strike down same-sex marriage bans as unconstitutional (United States v. Windsor and Obergefell v. Hodges); same-sex marriage was legalized nationwide in 2015 after the Court ruled so in Obergefell. He advocated for gun control in response to the Sandy Hook Elementary School shooting, indicating support for a ban on assault weapons, and issued wide-ranging executive actions concerning global warming and immigration. In foreign policy, he ordered military interventions in Iraq and Syria in response to gains made by ISIL after the 2011 withdrawal from Iraq, promoted discussions that led to the 2015 Paris Agreement on global climate change, drew down US troops in Afghanistan in 2016, initiated sanctions against Russia following its annexation of Crimea and again after interference in the 2016 US elections, brokered the Joint Comprehensive Plan of Action nuclear deal with Iran, and normalized US relations with Cuba. Obama nominated three justices to the Supreme Court: Sonia Sotomayor and Elena Kagan were confirmed as justices, while Merrick Garland was denied hearings or a vote from the Republican-majority Senate.
Major acts and legislation
Economic policy actions
Responding to the Great Recession  
American Recovery and Reinvestment Act of 2009  
Automotive industry bailout  
Wall Street reform  
Credit CARD Act of 2009  
Dodd–Frank Wall Street Reform and Consumer Protection Act  
Taxation and spending  
Tax Relief, Unemployment Insurance Reauthorization, and Job Creation Act of 2010  
Budget Control Act of 2011  
American Taxpayer Relief Act of 2012  
Bipartisan Budget Act of 2015  
2013 debt ceiling crisis and government shutdown  
Continuing Appropriations Act, 2014  
Bipartisan Budget Act of 2013
Other domestic policy actions
</excerpt>
### Rank 5 of 151 — 0.59
<excerpt title="Michelle Obama Addresses if Barack Would Consider Third Term Run vs ...">
Michelle Obama has given her thoughts on a third term for Barack Obama should the rules be changed to allow two-term presidents to run again.
The former first lady is married to former President Barack Obama, who held office for two consecutive terms from 2008 to 2016, where he was succeeded by President Donald Trump. Joe Biden held office for one term after beating Trump in the 2020 election, but Trump made a return to office for a second term following the 2024 election.
Now, Michelle Obama has responded to the idea that Barack Obama could run for a third term if Trump bypasses the Constitution and runs for a third term. _Newsweek_ has contacted the Obamas and the White House for comment on this story.

## **Why It Matters**
Trump has floated the idea of running for a third term, despite the 22nd Amendment of the United States Constitution barring a president from serving more than two terms. It states: "No person...shall be elected more than twice."
In early 2025, official merchandise from the Donald Trump online store bore the words: "Trump 2028(Rewrite the Rules)."
In a March 2025 interview with NBC's Kristen Welker, Trump said he was "not joking" about running for a third time, and said there were "methods" to be able to do it.
However, he has backtracked previously, including an interview with the same journalist in May 2025, where he said: "I'll be an eight-year president, I'll be a two-term president. I always thought that was very important."
According to a March 2025 report from _Politico_, Trump said he has "never looked into" running for a third term, but said "people are asking me to run."
He was then asked about, should that happen, whether Democrats could potentially run Obama again, to which he said: "I'd love that. That would be a good one. I'd like that."

## **What To Know**
Speaking with Alex Cooper on the _Call Her Daddy_ podcast uploaded on January 21, former first lady Obama was asked "for fun" whether, if Trump "changed the law and runs for a third term, hypothetically, do you think your husband would consider running?"
And she answered: "I hope not."
"I would actively work against that," she said. "I would be at home working against it."
She added: "I do believe in the need for new vision. The two terms is not just about 'we like him,' we're changing and growing so fast. This is a hard job, it requires new energy, new vision all the time, new ways of looking at the world.
"I do believe that eight years is enough. And there are so many talented people out there—why would we keep going with the same people? How are we going to build young leaders if the same people keep doing it again and again and again?
"I think there's room for that wisdom, but there's room for new ideas to come in. I think two terms is enough, for everybody."
She said she was "really curious" about the younger generation's perspective on how to run the country, pointing out that people are traveling more and have different experiences to the older generation.

## **What Happens Next**
In January 2026, Democrat Tom Umberg, a California state senator, introduced a new bill which would ensure Trump would be excluded from the ballot in the 2028 presidential election.
The proposed bill would allow the California secretary of state to request proof of a candidate's eligibility, and exclude candidates from the ballot if they are constitutionally ineligible.
Read more here: Newsweek
</excerpt>

# Example 4
## Question
Using the census data from census.gov, find the Florida counties with less than 50000 residents in the year 2022, that had a GDP less than half a billion (in 2017 chained dollars) in that same year according to the Bureau of Economic Analysis. Exclude counties named after a founding father of the United States from the list by The White House.

## Expected answer
Calhoun County, Dixie County, Gilchrist County, Glades County, Gulf County, Holmes County, Lafayette County, Liberty County, Union County.

## Grade 0.13

## Search 1 — query: "Florida counties 2022 population 50000 census.gov"
### Rank 1 of 220 — 0.73 (passed on)
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
### Rank 2 of 220 — 0.72
<excerpt title="Florida Population: Census Summary - 2020">
## [PDF page 35]
41  Columbia  69,698  67,531  56,513  42,613  0.32  0.36  0.35  0.33  
42  Jackson  47,319  49,746  46,755  41,375  0.22  0.26  0.29  0.32  
43  Gadsden  43,826  46,389  45,087  41,116  0.20  0.25  0.28  0.32  
44  Suwannee  43,474  41,551  34,844  26,780  0.20  0.22  0.22  0.21  
45  Levy  42,915  40,801  34,450  25,912  0.20  0.22  0.22  0.20

## [PDF page 35]
46  Okeecho bee  39,644  39,996  35,910  29,627  0.18  0.21  0.22  0.23  
47  Hendry  39,619  39,140  36,210  25,773  0.18  0.21  0.23  0.20  
48  DeSoto  33,976  34,862  32,209  23,865  0.16  0.19  0.20  0.18  
49  Wakulla  33,764  30,776  22,863  14,202  0.16  0.16  0.14  0.11  
50  Bradford  28,303  28,520  26,088  22,515  0.13  0.15  0.16  0.17
</excerpt>
### Rank 3 of 220 — 0.71
<excerpt title="Florida Population: Census Summary - 2020">
## [PDF page 28]
Flagler  115,378  95,696  49,832  28,701  20.6  92.0  73.6  
Franklin  12,451  11,549  9,829  8,967  7.8  17.5  9.6  
Gadsden  43,826  46,389  45,087  41,116  -5.5  2.9  9.7  
Gilchrist  17,864  16,939  14,437  9,667  5.5  17.3  49.3  
Glades  12,126  12,884  10,576  7,591  -5.9  21.8  39.3  
Gulf  14,192  15,863  14,560  11,504  -10.5  8.9  26.6  
Hamilton  14,004  14,799  13,327  10,930  -5.4  11.0  21.9  
Hardee  25,327  27,731  26,938  19,499  -8.7  2.9  38.2  
Hendry  39,619  39,140  36,210  25,773  1.2  8.1  40.5
</excerpt>
### Rank 4 of 220 — 0.71
<excerpt title="Florida Population: Census Summary - 2020">
## [PDF page 42]
3  Tampa  49,250  384,959  335,709  53  Ocala  7,276  63,591  56,315  
4  Miami  42,733  442,241  399,508  54  Leesburg  6,883  27,000  20,117  
5  Port St. Lucie  40,248  204,851  164,603  55  Plantation  6,795  91,750  84,955  
6  Cape Coral  39,711  194,016  154,305  56  Oviedo  6,717  40,059  33,342  
7  Doral  30,165  75,874  45,709  57  Port Orange  6,548  62,596  56,048  
8  Fort Myers  24,097  86,395  62,298  58  Gre enacres  6,417  43,990  37,573  
9  St. Cloud  23,781  58,964  35,183  59  Delray Beach  6,324  66,846  60,522  
10  Homestead  20,228  80,737  60,509  60  Crestview  6,156  27,134  20,978
</excerpt>
### Rank 5 of 220 — 0.70
<excerpt title="Population Table for Florida Counties | HDPulse Data Portal - NIH">
# Social & Economic Environment
## Data Visualization
| Wakulla County | 54.1 | 19,151 | 1,045 |  
| Calhoun County | 54.2 | 7,308 | 1,019 |  
| Pasco County | 54.3 | 332,142 | 993 |  
| Jackson County | 54.6 | 26,356 | 926 |  
| Putnam County | 54.7 | 41,145 | 909 |  
| Walton County | 55.5 | 46,025 | 766 |  
| Taylor County | 55.8 | 11,990 | 718 |  
| Palm Beach County | 56.2 | 862,352 | 652 |  
| St. Johns County | 56.2 | 172,527 | 652 |  
| St. Lucie County | 56.3 | 203,011 | 638 |  
| Madison County | 56.8 | 10,277 | 587 |  
| Nassau County | 57.1 | 55,848 | 553 |  
| Volusia County | 57.3 | 332,322 | 527 |  
| Jefferson County | 57.5 | 8,678 | 497 |  
| Brevard County | 58.1 | 367,734 | 434 |  
| Lake County | 58.2 | 240,241 | 420 |  
| Marion County | 58.2 | 232,764 | 420 |  
| Dixie County | 58.4 | 9,969 | 400 |  
| Levy County | 58.4 | 26,512 | 400 |
</excerpt>

## Search 2 — query: "White House list counties named after founding father"
### Rank 1 of 36 — 0.71 (passed on)
<excerpt title="List of U.S. counties named after presidents of the United States">
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
### Rank 2 of 36 — 0.64
<excerpt title="List of U.S. counties named after presidents of the United States">
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
### Rank 3 of 36 — 0.64
<excerpt title="List of U.S. counties named after presidents of the United States">
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
</excerpt>
### Rank 4 of 36 — 0.63
<excerpt title="List of U.S. counties named after presidents of the United States">
A total of 24 presidents have U.S. counties or county equivalents named after them.
Location of counties named for presidents George Washington, Thomas Jefferson, Andrew Jackson, and Abraham Lincoln, as well as for Benjamin Franklin.
In the United States, a county is an administrative or political subdivision of a U.S. state that consists of a geographic region with specific boundaries and usually some level of governmental authority. Most counties have subdivisions which may include townships, municipalities, and unincorporated areas. Some counties are consolidated city-counties which are simultaneously municipalities and counties.
48 of the 50 U.S. states are subdivided into counties, while the remaining two states and four of the five inhabited territories are subdivided into county equivalents by the state, territory, or the United States Census Bureau.[[a]](https://www.wikiwand.com/en/List_of_U.S._counties_named_after_presidents_of_the_United_States#cite_note-1) Louisiana is subdivided into parishes, Alaska is subdivided into boroughs,[[b]](https://www.wikiwand.com/en/List_of_U.S._counties_named_after_presidents_of_the_United_States#cite_note-2) and the territories use various other types of subdivisions. Some states also have independent cities, which the United States Census Bureau treats as county equivalents.
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
### Rank 5 of 36 — 0.61
<excerpt title="List of the most common U.S. county name etymologies">
## Franklin County (25 counties)
[edit]
_Twenty three of the twenty five Franklin Counties in the United States are named for Benjamin Franklin, the famous Founding Father, printer, scientist, philosopher, and diplomat._
*   Franklin County, Alabama  
*   Franklin County, Arkansas  
*   Franklin County, Florida  
*   Franklin County, Georgia  
*   Franklin County, Idaho: named for Franklin, Idaho, the first town in the state, in turn named for Franklin Richards, an apostle of the Church of Jesus Christ of Latter-day Saints  
*   Franklin County, Illinois  
*   Franklin County, Indiana  
*   Franklin County, Iowa  
*   Franklin County, Kansas  
*   Franklin County, Kentucky  
*   Franklin County, Maine  
*   Franklin County, Massachusetts  
*   Franklin County, Mississippi  
*   Franklin County, Missouri  
*   Franklin County, Nebraska  
*   Franklin County, New York  
*   Franklin County, North Carolina  
*   Franklin County, Ohio  
*   Franklin County, Pennsylvania  
*   Franklin County, Tennessee  
*   Franklin County, Texas: probably named for Benjamin Cromwell Franklin, an early judge and legislator in Texas[[1]](https://en.wikipedia.org/wiki/List_of_the_most_common_U.S._county_name_etymologies#cite_note-1)  
*   Franklin County, Vermont  
*   Franklin County, Virginia  
*   Franklin County, Washington  
*   Franklin Parish, Louisiana

## Jackson County (24 counties)
[edit]
_Twenty one of the twenty four Jackson Counties in the United States are named for Andrew Jackson, the seventh President._
*   Jackson County, Alabama  
*   Jackson County, Arkansas  
*   Jackson County, Colorado  
*   Jackson County, Florida  
*   Jackson County, Georgia: named for James Jackson, the 23rd governor of Georgia  
*   Jackson County, Illinois  
*   Jackson County, Indiana  
*   Jackson County, Iowa  
*   Jackson County, Kansas  
*   Jackson County, Kentucky  
*   Jackson County, Michigan  
*   Jackson County, Minnesota: named for Henry Jackson, a member of the first Minnesota Territory legislature  
*   Jackson County, Mississippi  
*   Jackson County, Missouri  
*   Jackson County, North Carolina  
*   Jackson County, Ohio  
*   Jackson County, Oklahoma: named for Thomas Jonathan "Stonewall" Jackson, the famous Confederate general  
*   Jackson County, Oregon  
*   Jackson County, South Dakota  
*   Jackson County, Tennessee  
*   Jackson County, Texas  
*   Jackson County, West Virginia  
*   Jackson County, Wisconsin  
*   Jackson Parish, Louisiana
</excerpt>

## Search 3 — query: "Florida county GDP 2017 BEA Florida county GDP 2017"
### Rank 1 of 54 — 0.63 (passed on)
<excerpt title="FL, BEA - Economic Data Series | FRED | St. Louis Fed">
### Gross Domestic Product: All Industry Total in Florida
Millions of Dollars

### Real Gross Domestic Product: All Industry Total in Florida
Millions of Chained 2017 Dollars

### Per Capita Personal Income in Florida
Dollars, Annual, Not Seasonally Adjusted 1929 to 2025 (Sep 30)

### Real Gross Domestic Product: All Industries in Calhoun County, FL
Thousands of Chained 2017 U.S. Dollars, Annual, Not Seasonally Adjusted 2001 to 2024 (Feb 5)

### Real Gross Domestic Product: All Industries in Gulf County, FL
Thousands of Chained 2017 U.S. Dollars, Annual, Not Seasonally Adjusted 2001 to 2024 (Feb 5)

### Real Gross Domestic Product: All Industries in Liberty County, FL
Thousands of Chained 2017 U.S. Dollars, Annual, Not Seasonally Adjusted 2001 to 2024 (Feb 5)

### Real Gross Domestic Product: All Industries in Baker County, FL
Thousands of Chained 2017 U.S. Dollars, Annual, Not Seasonally Adjusted 2001 to 2024 (Feb 5)

### Real Gross Domestic Product: All Industries in Lafayette County, FL
Thousands of Chained 2017 U.S. Dollars, Annual, Not Seasonally Adjusted 2001 to 2024 (Feb 5)

### Real Gross Domestic Product: All Industries in Gilchrist County, FL
Thousands of Chained 2017 U.S. Dollars, Annual, Not Seasonally Adjusted 2001 to 2024 (Feb 5)

### Gross Domestic Product: All Industries in Miami-Dade County, FL
Thousands of U.S. Dollars, Annual, Not Seasonally Adjusted 2001 to 2024 (Feb 5)

### Real Gross Domestic Product: All Industries in Dixie County, FL
Thousands of Chained 2017 U.S. Dollars, Annual, Not Seasonally Adjusted 2001 to 2024 (Feb 5)

### Total Gross Domestic Product for Miami-Fort Lauderdale-West Palm Beach, FL (MSA) (DISCONTINUED)
Millions of Dollars, Annual, Not Seasonally Adjusted 2001 to 2023 (2024-12-04)

### Real Gross Domestic Product: All Industries in Union County, FL
Thousands of Chained 2017 U.S. Dollars, Annual, Not Seasonally Adjusted 2001 to 2024 (Feb 5)

### Real Gross Domestic Product: All Industries in Holmes County, FL
Thousands of Chained 2017 U.S. Dollars, Annual, Not Seasonally Adjusted 2001 to 2024 (Feb 5)

### Real Gross Domestic Product: All Industries in Glades County, FL
Thousands of Chained 2017 U.S. Dollars, Annual, Not Seasonally Adjusted 2001 to 2024 (Feb 5)

### Real Gross Domestic Product: All Industries in Hardee County, FL
Thousands of Chained 2017 U.S. Dollars, Annual, Not Seasonally Adjusted 2001 to 2024 (Feb 5)

### Real Gross Domestic Product: All Industries in Taylor County, FL
Thousands of Chained 2017 U.S. Dollars, Annual, Not Seasonally Adjusted 2001 to 2024 (Feb 5)

### Real Gross Domestic Product: All Industries in Jackson County, FL
Thousands of Chained 2017 U.S. Dollars, Annual, Not Seasonally Adjusted 2001 to 2024 (Feb 5)

### Real Gross Domestic Product: All Industries in Gadsden County, FL
Thousands of Chained 2017 U.S. Dollars, Annual, Not Seasonally Adjusted 2001 to 2024 (Feb 5)

### Real Gross Domestic Product: All Industries in Franklin County, FL
Thousands of Chained 2017 U.S. Dollars, Annual, Not Seasonally Adjusted 2001 to 2024 (Feb 5)
</excerpt>
### Rank 2 of 54 — 0.55
<excerpt title="FL, BEA - Economic Data Series | FRED | St. Louis Fed">
### Regional Price Parities: All Items for Miami-Fort Lauderdale-West Palm Beach, FL (MSA)
Index, Annual, Not Seasonally Adjusted 2008 to 2024 (Feb 20)

### Real Gross Domestic Product: All Industries in Miami-Dade County, FL
Thousands of Chained 2017 U.S. Dollars, Annual, Not Seasonally Adjusted 2001 to 2024 (Feb 5)

### Total Personal Income in Florida
Millions of Dollars, Quarterly, Seasonally Adjusted Annual Rate Q1 1948 to Q2 2026 (Sep 30)

### Per Capita Personal Income in Palm Beach County, FL
Dollars, Annual, Not Seasonally Adjusted 1969 to 2024 (Feb 5)

### Total Gross Domestic Product for Jacksonville, FL (MSA) (DISCONTINUED)
Millions of Dollars, Annual, Not Seasonally Adjusted 2001 to 2023 (2024-12-04)

### Gross Domestic Product: State and Local in Florida
Millions of Dollars, Annual, Not Seasonally Adjusted 1997 to 2025 (Sep 30)

### Per Capita Personal Income in Miami-Dade County, FL
Dollars, Annual, Not Seasonally Adjusted 1969 to 2024 (Feb 5)

### Gross Domestic Product: Construction (23) in Florida
Millions of Dollars

### Gross Domestic Product: All Industries in Palm Beach County, FL
Thousands of U.S. Dollars, Annual, Not Seasonally Adjusted 2001 to 2024 (Feb 5)

### Regional Price Parities: All Items for Florida
Index, Annual, Not Seasonally Adjusted 2008 to 2024 (Feb 20)

### Total Real Gross Domestic Product for Orlando-Kissimmee-Sanford, FL (MSA) (DISCONTINUED)
Millions of Chained 2017 Dollars, Annual, Not Seasonally Adjusted 2001 to 2023 (2024-12-04)

### Real Gross Domestic Product: All Industries in Flagler County, FL
Thousands of Chained 2017 U.S. Dollars, Annual, Not Seasonally Adjusted 2001 to 2024 (Feb 5)
</excerpt>
### Rank 3 of 54 — 0.53
<excerpt title="FL, BEA - Economic Data Series | FRED | St. Louis Fed">
### Real Gross Domestic Product: All Industries in Franklin County, FL
Thousands of Chained 2017 U.S. Dollars, Annual, Not Seasonally Adjusted 2001 to 2024 (Feb 5)

### Real Gross Domestic Product: All Industries in Bradford County, FL
Thousands of Chained 2017 U.S. Dollars, Annual, Not Seasonally Adjusted 2001 to 2024 (Feb 5)

### Real Gross Domestic Product: All Industries in DeSoto County, FL
Thousands of Chained 2017 U.S. Dollars, Annual, Not Seasonally Adjusted 2001 to 2024 (Feb 5)

### Real Gross Domestic Product: All Industries in Hendry County, FL
Thousands of Chained 2017 U.S. Dollars, Annual, Not Seasonally Adjusted 2001 to 2024 (Feb 5)

### Real Gross Domestic Product: All Industries in Madison County, FL
Thousands of Chained 2017 U.S. Dollars, Annual, Not Seasonally Adjusted 2001 to 2024 (Feb 5)

### Real Gross Domestic Product: All Industries in Wakulla County, FL
Thousands of Chained 2017 U.S. Dollars, Annual, Not Seasonally Adjusted 2001 to 2024 (Feb 5)

### Real Gross Domestic Product: All Industries in Levy County, FL
Thousands of Chained 2017 U.S. Dollars, Annual, Not Seasonally Adjusted 2001 to 2024 (Feb 5)

### Real Gross Domestic Product: All Industries in Hamilton County, FL
Thousands of Chained 2017 U.S. Dollars, Annual, Not Seasonally Adjusted 2001 to 2024 (Feb 5)

### Real Gross Domestic Product: All Industries in Okeechobee County, FL
Thousands of Chained 2017 U.S. Dollars, Annual, Not Seasonally Adjusted 2001 to 2024 (Feb 5)

### Real Gross Domestic Product: All Industries in Suwannee County, FL
Thousands of Chained 2017 U.S. Dollars, Annual, Not Seasonally Adjusted 2001 to 2024 (Feb 5)

### Real Gross Domestic Product: All Industries in Jefferson County, FL
Thousands of Chained 2017 U.S. Dollars, Annual, Not Seasonally Adjusted 2001 to 2024 (Feb 5)

### Real Gross Domestic Product: All Industries in Washington County, FL
Thousands of Chained 2017 U.S. Dollars, Annual, Not Seasonally Adjusted 2001 to 2024 (Feb 5)

### Total Gross Domestic Product for Tampa-St. Petersburg-Clearwater, FL (MSA) (DISCONTINUED)
Millions of Dollars, Annual, Not Seasonally Adjusted 2001 to 2023 (2024-12-04)

### Gross Domestic Product: All Industries in Calhoun County, FL
Thousands of U.S. Dollars, Annual, Not Seasonally Adjusted 2001 to 2024 (Feb 5)

### Total Real Gross Domestic Product for Miami-Fort Lauderdale-West Palm Beach, FL (MSA) (DISCONTINUED)
Millions of Chained 2017 Dollars, Annual, Not Seasonally Adjusted 2001 to 2023 (2024-12-04)

### Total Gross Domestic Product for Orlando-Kissimmee-Sanford, FL (MSA) (DISCONTINUED)
Millions of Dollars, Annual, Not Seasonally Adjusted 2001 to 2023 (2024-12-04)

### Regional Price Parities: All Items for Miami-Fort Lauderdale-West Palm Beach, FL (MSA)
Index, Annual, Not Seasonally Adjusted 2008 to 2024 (Feb 20)
</excerpt>
### Rank 4 of 54 — 0.49
<excerpt title="Hillsborough's GDP grew 28% Since 2018">
## Tampa Bay Region Counties
Over one-fifth of Florida’s GDP originates from the Tampa Bay Region. The region’s economy grew faster between 2018-2023 (25.36%) than during 2013-2018 (17.36%).
At the county level, GDP growth from 2018 to 2023 ranged from 20.23% (Pinellas) to 35.44% (Pasco), averaging 26.58%. Hillsborough County leads the region with a GDP of $115.8 billion, nearly double that of Pinellas ($60.1 billion). While Citrus County’s economy contracted by 2.1% between 2013-2018, it rebounded strongly, growing 27.64% from 2013-2023.
Except for Sarasota County, all counties in the region experienced faster growth between 2018-2023 compared to 2013-2018. Sarasota County’s growth declined from 28.85% (2013-2018) to 23.17% (2018-2023), yet it still saw a total increase of 58.71% over the last decade.
Overall, the Tampa Bay region outpaced Florida’s economic growth between 2018-2023 (25.36% vs. 23.07%) but slightly trailed over the ten-year period (46.88% vs. 47.13%).

## Table 1. Tampa Bay Region Counties – 2013, 2018, and 2023 Gross Domestic Product in Billions of Constant 2017 Dollars
**Area****2013****2018****2023****2013-2018 Percent Change****2018-2023 Percent Change****2013-2023 Percent Change**  
Citrus 4.0 3.9 5.1-2.11%30.39%27.64%  
Hernando 3.7 4.2 5.3 15.38%25.57%44.88%  
Hillsborough 77.1 90.8 115.8 17.75%27.57%50.22%  
Manatee 12.1 14.9 19.2 23.57%28.71%59.05%  
Pasco 11.0 13.0 17.7 18.36%35.44%60.31%  
Pinellas 44.5 50.0 60.1 12.44%20.23%35.18%  
Polk 22.6 26.5 32.2 17.28%21.59%42.60%  
Sarasota 16.5 21.3 26.2 28.85%23.17%58.71%  
**Tampa Bay Region****191.4****224.6****281.5****17.36%****25.36%****47.13%**  
**Florida****880.2****1,050.4****1,292.8****19.34%****23.07%****46.88%**
</excerpt>
### Rank 5 of 54 — 0.44
<excerpt title="Hillsborough's GDP grew 28% Since 2018">
## Figure 1a. Citrus, Hernando, Hillsborough, and Manatee Counties – 2013, 2018, and 2023 Gross Domestic Product in Billions of Constant 2017 Dollars
This bar chart shows gross domestic product (GDP) in billions of constant 2017 dollars by county for 4 counties in the Tampa Bay Region: Citrus, Hernando, Hillsborough, and Manatee. In Citrus, GDP was $4.0 billion in 2013. It declined slightly to $3.9 billion in 2018 and increased to $5.1 billion in 2023. In Hernando, GDP was $3.7 billion in 2013. It increased to $4.2 billion in 2018 and increased again to $5.3 billion in 2023. In Hillsborough, GDP was $77.1 billion in 2013. It increased to $90.8 billion in 2018 and increased again to $115.8 billion in 2023. In Manatee, GDP was $12.1 billion in 2013. It increased to $14.9 billion in 2018 and increased again to $19.2 billion in 2023.

## Figure 1b. Pasco, Pinellas, Polk, and Sarasota Counties – 2013, 2018, and 2023 Gross Domestic Product in Billions of Constant 2017 Dollars
This bar chart shows gross domestic product (GDP) in billions of constant 2017 dollars by county for 4 counties in the Tampa Bay Region: Pasco, Pinellas, Polk, and Sarasota. In Pasco, GDP was $11.0 billion in 2013. It increased to $13.0 billion in 2018 and increased again to $17.7 billion in 2023. In Pinellas, GDP was $44.5 billion in 2013. It increased to $50.0 billion in 2018 and increased again to $60.1 billion in 2023. In Polk, GDP was $22.6 billion in 2013. It increased to $26.5 billion in 2018 and increased again to $32.2 billion in 2023. In Sarasota, GDP was $16.5 billion in 2013. It increased to $21.3 billion in 2018 and increased again to $26.2 billion in 2023.

## Figure 1c. Hillsborough County, Tampa Bay Region, and Florida – 2013, 2018, and 2023 Gross Domestic Product in Billions of Constant 2017 Dollars
This bar chart shows gross domestic product (GDP) in billions of constant 2017 dollars for Hillsborough County, Tampa Bay Region, and Florida. In Hillsborough County, GDP was $77.1 billion in 2013. It inceased to $90.8 billion in 2018 and increased again to $115.8 billion in 2023. In Tampa Bay Region, GDP was $191.4 billion in 2013. It increased to $224.6 billion in 2018 and increased again to $281.5 billion in 2023. In Florida, GDP was $880.2 billion in 2013. It increased to $1.05 trillion in 2018 and increased again to $1.3 trillion in 2023.
</excerpt>

## Search 4 — query: "White House counties named after founding fathers list"
### Rank 1 of 26 — 0.70 (passed on)
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
### Rank 2 of 26 — 0.61
<excerpt title="List of U.S. counties named after U.S. Presidents - EverybodyWiki">
This is a **list of U.S. counties which are named for Presidents of the United States**.
Buy Maps

## Washington County (31 counties)
_This is a list of all of the Counties in the United States named for George Washington, the first president of the United States._
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

## Jefferson County (24 counties with 3 more indirectly named for Jefferson)
_This is a list of all of the Counties in the United States named for Thomas Jefferson, the third president of the United States._
Track Exec Orders
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
*   Jefferson County, Oregon  
*   Jefferson County, Ohio  
*   Jefferson County, Oklahoma  
*   Jefferson County, Pennsylvania  
*   Jefferson County, Tennessee  
*   Jefferson County, Texas  
*   Jefferson County, Washington  
*   Jefferson County, West Virginia  
*   Jefferson County, Wisconsin  
*   Jefferson Parish, Louisiana
PLUS
*   Jefferson County, Colorado: Jefferson is named for the Territory of Jefferson, which in turn is named for Thomas Jefferson. The Territory of Jefferson extralegally governed the area before the United States Congress established the Colorado Territory, which in turn is named for Thomas Jefferson.  
*   Jefferson County, Montana: Jefferson is named for the Jefferson River, which in turn is named for Thomas Jefferson.  
*   Jefferson County, Oregon: Jefferson is named for Mount Jefferson on the county's western boundary, which in turn is named for Thomas Jefferson.
</excerpt>
### Rank 3 of 26 — 0.60
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
### Rank 4 of 26 — 0.60
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
### Rank 5 of 26 — 0.54
<excerpt title="List of U.S. counties named after U.S. Presidents - EverybodyWiki">
## Madison County (probably 19 with 2 more indirectly named for Madison)
_This is a list of all of the Counties in the United States named for James Madison, the fourth president of the United States._
Track Exec Orders
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
PLUS
*   Madison County, Montana is named for the Madison River, which in turn is named for James Madison.  
*   Madison County, Nebraska is probably named for Madison, Wisconsin, which in turn is named for James Madison, where most of the new county's settlers were from.

## Lincoln County (17 counties)
_This is a list of all of the Counties in the United States named for Abraham Lincoln, the sixteenth president of the United States._
Track Exec Orders
*   Lincoln County, Arkansas  
*   Lincoln County, Colorado  
*   Lincoln County, Idaho  
*   Lincoln County, Kansas  
*   Lincoln County, Minnesota  
*   Lincoln County, Mississippi  
*   Lincoln County, Montana is probably named for Abraham Lincoln.  
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
NOTE (8 Counties were named for other people named Lincoln) Five Counties are named for Benjamin Lincoln, a leading general in the American Revolutionary War.
*   Lincoln County, Georgia  
*   Lincoln County, Kentucky  
*   Lincoln County, Missouri  
*   Lincoln County, North Carolina  
*   Lincoln County, Tennessee
ALSO:
*   Lincoln County, Maine is named for the city of Lincoln, England.  
*   Lincoln County, South Dakota: is named for Lincoln County, Maine.

## Monroe County (17 counties)
_This is a list of all of the Counties in the United States named for James Monroe, the fifth president of the United States._
Track Exec Orders
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
*   Monroe County, Ohio was named for Monroe when he was United States Secretary of State.  
*   Monroe County, Pennsylvania  
*   Monroe County, Tennessee  
*   Monroe County, West Virginia  
*   Monroe County, Wisconsin
</excerpt>

## Search 5 — query: "White House founding fathers list counties"
### Rank 1 of 162 — 0.70 (passed on)
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
### Rank 2 of 162 — 0.59
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
### Rank 3 of 162 — 0.57
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
### Rank 4 of 162 — 0.51
<excerpt title="Hundreds of U.S. Places and Counties Have Patriotic Names or Pay Tribute ...">
The Thirteen British colonies that would become the first of the United States – Connecticut, Delaware, Georgia, Maryland, Massachusetts, New Hampshire, New Jersey, New York, North Carolina, Pennsylvania, Rhode Island, South Carolina, and Virginia – declared independence from the Kingdom of Great Britain on July 4, 1776.
As of July 2024, there were 55 incorporated places with patriotic names. Topping the list: “Liberty” with “Independence” a distant second.
To commemorate the occasion, here’s some patriotic trivia courtesy of the U.S. Census Bureau to share with family and friends at your Independence Day festivities.

### Nation’s Population
The first federal census was not conducted until 1790 but the Census Bureau estimates Pennsylvania’s population in 1775 was 302,000 based on counts conducted during the Colonial and Continental periods. The following year, the Founding Fathers signed the Declaration of Independence in Philadelphia, formally asserting separation from British rule and making July 4, 1776, a pivotal point in the nation’s history.
By 2024, Pennsylvania’s population had grown to about 13.1 million, more than 43 times larger, according to Census Bureau estimates.
Delegates from all Thirteen Colonies signed the declaration. In 1780, the nearest available Census Bureau population estimate to the signing, nearly2.8 million peoplelived in what would become the first of the United States of America.
According toCensus Bureau estimates for July 2025, there are about 342.0 million people living in the United States, almost 123 times more than in 1780.

### Patriotic Place Names
The nation is filled with patriotically named places. Some share names with prominent historical figures (Madison, Wisconsin, or Jeffersontown, Kentucky) while others are named for patriotic concepts or ideals (Yankee Springs, Michigan, or Independence, Kansas).
As of July 2024, 164 U.S. places and 126 counties or county equivalents shared at least part of their name with one of the following Founding Fathers: Benjamin Franklin, George Washington, Thomas Jefferson, James Madison, Alexander Hamilton, John Adams, or John Jay (Figure 1).
About 0.8% of incorporated places and 4.0% of counties share at least part of their name with a founding father.
“Place” refers to most cities, towns, villages and boroughs.
George Washington is the only founding father after whom a state is named. And that state even has a small city named George. The 2020 Census population of George, Washington: 809.
Washington, D.C., the nation’s capital, is also named in his honor.
As of July 2024, there were 55 incorporated places with patriotic names. Topping the list: “Liberty” with “Independence” a distant second (Figure 2).
The list also includes places with names containing a patriotic reference like Libertyville, Illinois, and Federal Heights, Colorado.
As of July 2024, 0.28% of the nation’s 19,479 incorporated places had names invoking patriotic concepts (Figure 2).

### Available Data
The Census Bureau releases estimates of the total population for cities and towns. It also releases population estimates by age, sex, race and Hispanic origin for the nation, states, counties, and metropolitan and micropolitan statistical areas.
The latest data and tables with the names of all U.S. counties and incorporated places were released in May 2025.
Information on a wide variety of population characteristics — from ancestry to internet use — is available on the Population webpage.
**_Travis Shoemaker is a writer/editor for America Counts in the Census Bureau’s Communications Directorate._**

## Related Statistics
*
* * *
Facts for Features The Fourth of July: 2025 On this day in 1776, the Continental Congress approved the Declaration of Independence, setting the 13 colonies on the road to freedom as a sovereign nation.
* * *
*
* * *
Population Our population statistics cover age, sex, race, Hispanic origin, migration, ancestry, language use, veterans, as well as population estimates and projections.
* * *

## Subscribe
Our email newsletter is sent out on the day we publish a story. Get an alert directly in your inbox to read, share and blog about our newest stories.
Contact ourPublic Information Officefor media inquiries or interviews.
</excerpt>
### Rank 5 of 162 — 0.47
<excerpt title="Founding Fathers of the United States">
George Washington (1789–1797)  
John Adams (1797–1801)  
Thomas Jefferson (1801–1809)  
James Madison (1809–1817)  
James Monroe (1817–1825)  
Demographics and other characteristics
The Founding Fathers represented the upper echelon of political leadership in the British colonies during the latter half of the 18th century.[261][262] All were leaders in their communities and respective colonies who were willing to assume responsibility for public affairs.[263]
Of the signers of the Declaration of Independence, Articles of Confederation, and U.S. Constitution, nearly all were native born and of British heritage, including Scots, Irish, and Welsh.[264][265] Nearly half were lawyers, while the remainder were primarily businessmen and planter-farmers.[266][267][268] The average age of the founders was 43.[269] Benjamin Franklin, born in 1706, was the oldest, while only a few were born after 1750 and thus were in their 20s.[270][271][272]
The following sections discuss these and other demographic topics in greater detail. For the most part, the information is confined to signers/delegates associated with the Declaration of Independence, Articles of Confederation, and Constitution.
Political experience
All of the Founding Fathers had extensive political experience at the national and state levels.[273][274] As just one example, the signers of the Declaration of Independence and Articles of Confederation were members of Second Continental Congress, while four-fifths of the delegates at the Constitutional Convention had served in the Congress either during or prior to the convention. The remaining fifth attending the convention were recognized as leaders in the state assemblies that appointed them.
Following are brief profiles of the political backgrounds of some of the more notable founders:
</excerpt>

## Search 6 — query: ""Jackson County" FL GDP 2022 2017 chained dollars"
### Rank 1 of 147 — 0.85 (passed on)
<excerpt title="Real Gross Domestic Product: Government and Government ... - FRED">
#
Real Gross Domestic Product: Government and Government Enterprises in Jackson County, FL (REALGDPGOVT12063)
Observations
2024: 411,290 | Thousands of Chained 2017 U.S. Dollars, Not Seasonally Adjusted |  Annual
Updated: Feb 5, 2026 8:55 AM CST
Next Release Date: Dec 2, 2026
Observations
2024:411,290
Updated: Feb 5, 2026 8:55 AM CST
Next Release Date: Dec 2, 2026
2024:411,290  
2023:403,437  
2022:389,015  
2021:370,196  
2020:370,896  
View All
Units:
Thousands of Chained 2017 U.S. Dollars,
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
(a)Real Gross Domestic Product: Government and Government Enterprises in Jackson County, FL,Thousands of Chained 2017 U.S. Dollars,Not Seasonally Adjusted(REALGDPGOVT12063)
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

#
For example, invert an exchange rate by using formula 1/a, where “a” refers to the first FRED data series added to this line. Or calculate the spread between 2 interest rates, a and b, by using the formula a - b.
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
###### Real Gross Domestic Product: Government and Government Enterprises in Jackson County, FL
</excerpt>
### Rank 2 of 147 — 0.85
<excerpt title="Real Gross Domestic Product: Government and Government ... - FRED">
# Real Gross Domestic Product: Government and Government Enterprises in Jackson County, FL (REALGDPGOVT12063) | FRED | St. Louis Fed
Skip to main content
* * *
*

# Real Gross Domestic Product: Government and Government Enterprises in Jackson County, FL (REALGDPGOVT12063) | FRED | St. Louis Fed
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
Home>Categories>U.S. Regional Data>States>Florida>Counties>Jackson County, FL

#
Real Gross Domestic Product: Government and Government Enterprises in Jackson County, FL (REALGDPGOVT12063)
Observations
2024: 411,290 | Thousands of Chained 2017 U.S. Dollars, Not Seasonally Adjusted |  Annual
Updated: Feb 5, 2026 8:55 AM CST
Next Release Date: Dec 2, 2026
Observations
2024:411,290
Updated: Feb 5, 2026 8:55 AM CST
Next Release Date: Dec 2, 2026
2024:411,290  
2023:403,437  
2022:389,015  
2021:370,196  
2020:370,896  
View All
Units:
Thousands of Chained 2017 U.S. Dollars,
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
(a)Real Gross Domestic Product: Government and Government Enterprises in Jackson County, FL,Thousands of Chained 2017 U.S. Dollars,Not Seasonally Adjusted(REALGDPGOVT12063)
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
</excerpt>
### Rank 3 of 147 — 0.63
<excerpt title="Jackson County, Florida Economic Profile">
## AI Insights
### Take it further
**AI Insights:** Built into ExecutivePulse. Continuous analysis tied to your own pipeline: industry-shift signals, prospect matches, retention prompts.
**Managed Services:** Prefer to hand it off? Our team delivers the analysis and consulting for you.
Schedule a Demo
Available as premium offerings.

## AI Insights
### Data Sources
Updated from official federal government data.
Census ACS 5-Year 2024
BLS QCEW 2024 annual
BLS LAUS 2025 annual
BEA Regional GDP 2024
BEA Regional Price Parity 2024
Census CBP 2023
HUD Fair Market Rents FY2026
FCC Broadband Map 2024
USAspending.gov FY2026
College Scorecard AY 2022-23
American Community Survey figures on this page are 2020-2024 five-year averages rather than single-year counts. A five-year estimate pools 60 months of survey responses, so each value describes the period as a whole.

## Frequently Asked Questions
Key economic and demographic figures for Jackson County, Florida, from federal data sources.
What is the population of Jackson County, Florida?  
48,250 (U.S. Census Bureau, ACS 5-Year Estimates).
What is the median household income in Jackson County, Florida?  
$49,149 in nominal dollars (U.S. Census Bureau, ACS 5-Year Estimates). Adjusted for local prices using the BEA all-items regional price parity for Florida (103.4 against a national average of 100), that is $47,533 at national average prices. BEA publishes regional price parity at state level; there is no county-level figure.
What is the unemployment rate in Jackson County, Florida?  
4.5% (2025 annual average, U.S. Bureau of Labor Statistics, LAUS).
What is the GDP of Jackson County, Florida?  
$2B (U.S. Bureau of Economic Analysis, CAGDP2).
**Jackson County, FL**: Public data. Imagine the full platform.
Get a Demo →
</excerpt>
### Rank 4 of 147 — 0.60
<excerpt title="Gross Domestic Product by County | FRED | St. Louis Fed">
### Gross Domestic Product: All Industries in Miami-Dade County, FL
Thousands of U.S. Dollars, Annual, Not Seasonally Adjusted 2001 to 2024 (Feb 5)

### Total Gross Domestic Product for Austin-Round Rock, TX (MSA) (DISCONTINUED)
Millions of Dollars, Annual, Not Seasonally Adjusted 2001 to 2023 (2024-12-04)

### Real Gross Domestic Product: All Industries in Dixie County, FL
Thousands of Chained 2017 U.S. Dollars, Annual, Not Seasonally Adjusted 2001 to 2024 (Feb 5)

### Total Gross Domestic Product for Miami-Fort Lauderdale-West Palm Beach, FL (MSA) (DISCONTINUED)
Millions of Dollars, Annual, Not Seasonally Adjusted 2001 to 2023 (2024-12-04)

### Real Gross Domestic Product: All Industries in Union County, FL
Thousands of Chained 2017 U.S. Dollars, Annual, Not Seasonally Adjusted 2001 to 2024 (Feb 5)

### Real Gross Domestic Product: All Industries in Holmes County, FL
Thousands of Chained 2017 U.S. Dollars, Annual, Not Seasonally Adjusted 2001 to 2024 (Feb 5)

### Real Gross Domestic Product: All Industries in Glades County, FL
Thousands of Chained 2017 U.S. Dollars, Annual, Not Seasonally Adjusted 2001 to 2024 (Feb 5)

### Real Gross Domestic Product: All Industries in Hardee County, FL
Thousands of Chained 2017 U.S. Dollars, Annual, Not Seasonally Adjusted 2001 to 2024 (Feb 5)

### Total Gross Domestic Product for Nashville-Davidson--Murfreesboro--Franklin, TN (MSA) (DISCONTINUED)
Millions of Dollars, Annual, Not Seasonally Adjusted 2001 to 2023 (2024-12-04)

### Total Gross Domestic Product for Houston-The Woodlands-Sugar Land, TX (MSA) (DISCONTINUED)
Millions of Dollars, Annual, Not Seasonally Adjusted 2001 to 2023 (2024-12-04)

### Total Gross Domestic Product for Seattle-Tacoma-Bellevue, WA (MSA) (DISCONTINUED)
Millions of Dollars, Annual, Not Seasonally Adjusted 2001 to 2023 (2024-12-04)

### Real Gross Domestic Product: All Industries in Taylor County, FL
Thousands of Chained 2017 U.S. Dollars, Annual, Not Seasonally Adjusted 2001 to 2024 (Feb 5)

### Gross Domestic Product: All Industries in San Francisco County, CA
Thousands of U.S. Dollars, Annual, Not Seasonally Adjusted 2001 to 2024 (Feb 5)

### Real Gross Domestic Product: All Industries in Jackson County, FL
Thousands of Chained 2017 U.S. Dollars, Annual, Not Seasonally Adjusted 2001 to 2024 (Feb 5)

### Real Gross Domestic Product: All Industries in Gadsden County, FL
Thousands of Chained 2017 U.S. Dollars, Annual, Not Seasonally Adjusted 2001 to 2024 (Feb 5)

### Real Gross Domestic Product: All Industries in Franklin County, FL
Thousands of Chained 2017 U.S. Dollars, Annual, Not Seasonally Adjusted 2001 to 2024 (Feb 5)

### Real Gross Domestic Product: All Industries in Bradford County, FL
Thousands of Chained 2017 U.S. Dollars, Annual, Not Seasonally Adjusted 2001 to 2024 (Feb 5)
</excerpt>
### Rank 5 of 147 — 0.45
<excerpt title="What is the gross domestic product (GDP) in Pasco County, FL?">
## What is Pasco County's GDP per person?
| 12063 | Jackson County | 30628.0 |  
| 12037 | Franklin County | 30087.0 |  
| 12123 | Taylor County | 29961.0 |  
| 12019 | Clay County | 29865.0 |  
| 12027 | DeSoto County | 29824.0 |  
| 12113 | Santa Rosa County | 29502.0 |  
| 12035 | Flagler County | 29281.0 |  
| 12013 | Calhoun County | 29062.0 |  
| 12039 | Gadsden County | 28817.0 |  
| 12101 | Pasco County | 28596.0 |  
| 12067 | Lafayette County | 27720.0 |  
| 12133 | Washington County | 27340.0 |  
| 12003 | Baker County | 27161.0 |  
| 12055 | Highlands County | 27122.0 |  
| 12043 | Glades County | 26768.0 |  
| 12075 | Levy County | 26702.0 |  
| 12125 | Union County | 26013.0 |  
| 12053 | Hernando County | 26013.0 |  
| 12007 | Bradford County | 25909.0 |  
| 12129 | Wakulla County | 24508.0 |  
| 12041 | Gilchrist County | 22026.0 |  
| 12059 | Holmes County | 21718.0 |  
| 12065 | Jefferson County | 21357.0 |  

## What is Pasco County's GDP per person?
| 12029 | Dixie County | 17705.0 |

## Keep exploring
*    ### How do national parks affect the economy? Jan 23, 2026  
*    ### Just the Facts on the US national debt  
*   ### 2026 State of the Union: Economy  
*    ### Just the Facts about the US economy
</excerpt>

## Search 7 — query: "Hamilton County Florida name origin Alexander Hamilton"
### Rank 1 of 53 — 0.69 (passed on)
<excerpt title="Governor Ron DeSantis Unveils Statue of “Father of the Treasury” ...">
March
11
2026
**HAMILTON COUNTY, Fla.**—Today, Governor Ron DeSantis unveiled a new statue honoring Founding Father Alexander Hamilton in Hamilton County, continuing Florida’s commemoration of the nation’s upcoming 250th anniversary and recognizing Hamilton’s lasting contributions to the American Republic and to Florida’s early history. The statue, located in White Springs along the banks of the historic Suwannee River, is part of a broader initiative to install monuments to America’s Founding Fathers in Florida counties that bear their names.
“I was proud to unveil a new statue of Hamilton County’s namesake, Alexander Hamilton,”**said Governor Ron DeSantis.**“His participation in the fight for independence, his contributions to writing the Federalist Papers, his public service as a diplomat and ‘Father of the Treasury,’ and his role as a confidante to George Washington made Hamilton an indispensable figure in our nation’s history.”
“Installing a statue of Alexander Hamilton in the county named after him is a fitting tribute to the Founding Father who was the most vocal about Florida’s vital importance to America’s destiny,”**said America250FL Chair and Secretary of State Cord Byrd.** “Florida is number one in the nation when it comes to celebrating our 250th anniversary with events planned throughout 2026.”
"Florida honors our nation and its history, and we welcome this new monument of Alexander Hamilton in our Founding Father statue series,"**said Bryan Griffin, President & CEO of VISIT FLORIDA.**"This is yet another reason that Florida is the best destination to celebrate America, all year long. We invite travelers to come experience our numerous historical sites around the state and join us in enthusiastically commemorating our nation's 250th birthday."
Hamilton distinguished himself early in the American Revolution, joining the New York militia in 1775 and serving as an artillery officer in several key battles. In 1777, General George Washington appointed Hamilton as his aide-de-camp, making him one of Washington’s most trusted advisors. Hamilton later commanded American forces during the decisive Battle of Yorktown, which helped secure American victory and independence.
Following the war, Hamilton became a leading advocate for a stronger national government. As the principal author of The Federalist Papers, he wrote 51 of the 85 essays defending the ratification of the United States Constitution.

President George Washington later appointed Hamilton as the nation’s first Secretary of the Treasury, where he established the foundations of the American financial system by stabilizing public credit, promoting domestic industry, and creating a national banking system. Hamilton also founded the Revenue Cutter Service, which later evolved into the modern United States Coast Guard.
Hamilton also recognized the strategic importance of Florida to the future of the United States. As a congressional delegate from New York, he advocated for American access to the Mississippi River and supported the acquisition of Florida from Spain. His diplomatic efforts helped shape Pinckney’s Treaty of 1795, which established the boundary between Spanish Florida and the United States—a border that still separates Florida and Georgia today.
Hamilton’s legacy in Florida continued after the United States acquired the territory through the Adams-Onís Treaty of 1819. President James Monroe later appointed Hamilton’s son, Alexander Hamilton Jr., as U.S. district attorney for East Florida, where he helped establish the territory’s early legal framework. In recognition of the family’s influence and Hamilton’s contributions to the nation, Hamilton County was established in 1827 and named in his honor.
**About America 250 Florida**
Today’s unveiling is part of Florida’s broader initiative to honor the individuals who shaped our nation over the past 250 years and to preserve America’s civic pride and heritage for future generations.
America 250 Florida marks the state’s official observance of America’s semiquincentennial and will host and help sponsor special events throughout the year for Floridians from all corners of the state to enjoy. Floridians can find information on events, exhibits, heritage sites, and participation opportunities atAmerica250FL.com, the state’s official hub for the Semiquincentennial celebration.
</excerpt>
### Rank 2 of 53 — 0.68
<excerpt title="Founding Fathers Today we recognize Hamilton County, Florida ...">
# Founding Fathers Today we recognize Hamilton County, Florida, which was named after America’s financial architect, Alexander Hamilton who was born on #OTD. Fun Fact: Hamilton County is the only county in Florida that does not share a land border with its neighboring Florida counties. Watch this video to learn more about Hamilton County: | America250FL | Facebook
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
Sorry, we're having trouble playing this video.
[Learn more](https://www.facebook.com/help/396404120401278/list?__cft__[0]=AZgdJ9GRr-s1a3Njy-WbCf0pg8wz6uT6x9Y2higHpy4GCn9c9F65D24ONnHJbf7GibB5tEjmRJH6vB43h2a2YwuPa1r87tqxOQijXobf61wPcY0LI8Cw0SQp8k9Z6YLgs4oA945AG8tigsLMuWWWaA)
Founding Fathers Today we recognize Hamilton County, Florida, which was named after America’s financial architect, Alexander Hamilton who was born on #OTD. Fun Fact: Hamilton County is the only county in Florida that does not share a land border with its neighboring Florida counties. Watch this video to learn more about Hamilton County:
Like
Comment
Share
![Image 1](blob:http://localhost/85d8b181a20aeb64a3afc2f1c39d2480)
4
·
680 views

# Video
## **America250FL**
Sunday, January 11, 2026 at 3:00 PM
January 11 ·
Follow
Founding Fathers…
See more

# Video
## Comments


# Video
## Related videos
[ 0:59](https://www.facebook.com/61573890020822/videos/3154298218100608/?__so__=permalink&__cft__[0]=AZjAL2jnaxCgFQ18BIk3jc7OZu8-tW6bemAiAwIaOwfN-X_P8GPcjunkZO_q4AHvg137Mo8k94pXh7s4kZdmHJ-gxXDVRItyy6PRYTtoRnOhqICWs9V_0nugxTrc0sb3ZEd3wpZX-2piYC9GY-cXAA)
[](https://www.facebook.com/watch/61573890020822/?__cft__[0]=AZjAL2jnaxCgFQ18BIk3jc7OZu8-tW6bemAiAwIaOwfN-X_P8GPcjunkZO_q4AHvg137Mo8k94pXh7s4kZdmHJ-gxXDVRItyy6PRYTtoRnOhqICWs9V_0nugxTrc0sb3ZEd3wpZX-2piYC9GY-cXAA)
</excerpt>
### Rank 3 of 53 — 0.67
<excerpt title="Hamilton County, Florida">
| Hamilton County, Florida |  
| --- |  
| County |  
|  Hamilton County Courthouse in Jasper |  
|  Seal |  
|  Location within the U.S. state of Florida |  
| Coordinates: 30°29′N 82°57′W / 30.49°N 82.95°W |  
| Country | United States |  
| State | Florida |  
| Founded | December 26, 1827 |  
| Named for | Alexander Hamilton |  
| Seat | Jasper |  
| Largest city | Jasper |  
| Area |  
| •Total | 519 sq mi (1,340 km 2) |  
| •Land | 514 sq mi (1,330 km 2) |  
| •Water | 5.3 sq mi (14 km 2) 1.0% |  
| Population (2020) |  
| •Total | 14,004 |  
| •Estimate (2025) | 14,180  |  
| •Density | 27.2/sq mi (10.5/km 2) |  
| Time zone | UTC−5 (Eastern) |  
| •Summer (DST) | UTC−4 (EDT) |  
| Congressional district | [3rd](https://en.wikipedia.org/wiki/Florida's_3rd_congressional_district "Florida's 3rd congressional district") |  
| Website | www.hamiltoncountyfl.com |
**Hamilton County** is a county located in the north central portion of the U.S. state of Florida. As of the 2020 census, the population was 14,004, down from 14,799 at the 2010 census.[[1]](https://en.wikipedia.org/wiki/Hamilton_County,_Florida#cite_note-QF-1) Its county seat is Jasper.[[2]](https://en.wikipedia.org/wiki/Hamilton_County,_Florida#cite_note-GR6-2)

Hamilton County was created in 1827[[3]](https://en.wikipedia.org/wiki/Hamilton_County,_Florida#cite_note-3) from portions of Jefferson County. It was named for Alexander Hamilton, first United States Secretary of the Treasury.[[4]](https://en.wikipedia.org/wiki/Hamilton_County,_Florida#cite_note-4)
According to the U.S. Census Bureau, the county has a total area of 519 square miles (1,340 km 2), of which 514 square miles (1,330 km 2) is land and 5.3 square miles (14 km 2) (1.0%) is water.[[5]](https://en.wikipedia.org/wiki/Hamilton_County,_Florida#cite_note-GR1-5) It is the only county in Florida entirely north of Interstate 10.[[6]](https://en.wikipedia.org/wiki/Hamilton_County,_Florida#cite_note-6)
Hamilton County is the only county in Florida that is not connected to Florida by land. This is due to it being separated from neighboring Florida counties by river (the Suwannee and the Withlacoochee rivers). It does, however, touch Georgia via land.
*   Echols County, Georgia - north  
*   Columbia County - east  
*   Suwannee County - south  
*   Madison County - west  
*   Lowndes County, Georgia - northwest
The main railroad line through Hamilton County is the Norfolk Southern Railway's Navair District (originally the Georgia Southern and Florida Railway), which runs mostly in close proximity to US 41 from Lake City across a bridge over the Suwannee River and the Columbia-Hamilton County Line southeast of White Plains to the Florida-Georgia State Line northwest of Jennings. A former section of the Atlantic Coast Line Railroad's DuPont—Lakeland Line survives as a rail trail in Jasper.
</excerpt>
### Rank 4 of 53 — 0.66
<excerpt title="Hamilton County Maps - Florida Center for Instructional Technology">
> _Click on a thumbnail image to view a full size version of that map._  
>   
>   
> Hamilton County is Florida's 15 th county, established on December 26, 1827, from a segment of Escambia County. It gains its name from Alexander Hamilton, the first U.S. Secretary of the Treasury. Jasper is the county seat.  
>   
>   
> For earlier maps of this area, visit the Escambia County map gallery.
Record 26 to 50 of 80  
Hamilton County, 1888
_A map of Hamilton County showing county lines, the county seat (Jasper), railroads, and cities current to 1888...._
Hamilton County, 1888
_This detail shows county lines and county seats current to the period, major towns and cities, and railroad routes and stations for Hamilton County. The Townships are subdivided into sections, and those sections offered for sale by the land departmen..._
Hamilton County, 1888
_This detail of a map of Florida indicates Hamilton County current to 1888. The map was issued by the Florida Southern Railway Company. It shows lands, owned, and offered for sale by said department. Six square miles makes up a township, which is numb..._
Hamilton County, 1889
_This is a detail of a map of Florida showing counties, railroads, cities, inland waters, etc for Hamilton County. Each color represents a different route. The origin and destination for each route is found on the main map in an Explanation key. Featu..._
Hamilton County, 1890
_A map of Hamilton County showing towns, bodies of water, county lines, the county seat (Jasper), and railroads connecting the major cities current to 1890. ..._
Hamilton County, 1890
_A map of Hamilton County showing the county seat (Jasper), cities, roads, towns, rivers, lakes, and railroads present in 1890...._
Hamilton County, 1890
_A map of Hamilton County showing county lines, the county seat (Jasper), railroads, and cities current to 1890...._
Hamilton County, 1892

_This detail of a map of Florida indicates Hamilton County current to 1892. Major waterways are shown with thin, concentric lines. The thick black lines represent railroads. The central features of the detail include Quincy, Midway, and Mount Pleasant..._
Hamilton County, 1893
_A map of Hamilton County showing county lines, the county seat (Jasper), and railroads connecting the major cities current to 1893...._
Hamilton County, 1894
_A map of Hamilton County showing county lines, the county seat (Jasper), railroads, and cities current to 1894...._
Hamilton County, 1895
_This Florida map of Hamilton County outlines the county boundary and railroads connecting to major cities, current to 1895. ..._
Hamilton County, 1897
_A map of Hamilton County showing forts, towns, bodies of water, county lines, the county seat (Jasper), and railroads connecting the major cities current to 1897. Township and Range grids extending from the Tallahassee Meridian and Tallahassee Base L..._
Hamilton County, 1898
_A map of Hamilton County as of 1898 showing rivers, railroads, towns, and the county seat, Jasper...._
Hamilton County, 1898
_A map of Hamilton County showing county lines, the county seat (Jasper), and railroads connecting the major cities current to 1898...._
Hamilton County, 1898
_Digitization provided by the USF Libraries Digitization Center. Rare Maps. This is a detail map of Hamilton county circa 1898. This map shows section township range (STR). Main cities and towns are shown such as the county seat Jasper. Inland waters ..._
Hamilton County, 1899
_A map of Hamilton County showing county lines, the county seat (Jasper), and railroads connecting the major cities current to 1899...._
Hamilton County, 1900
_A map of Hamilton County showing county lines, the county seat (Jasper), railroads, and cities current to 1900...._
Hamilton County, 1900
</excerpt>
### Rank 5 of 53 — 0.62
<excerpt title="Hamilton County, Florida">
Hamilton County was created in 1827[[3]](https://en.wikipedia.org/wiki/Hamilton_County,_Florida#cite_note-3) from portions of Jefferson County. It was named for Alexander Hamilton, first United States Secretary of the Treasury.[[4]](https://en.wikipedia.org/wiki/Hamilton_County,_Florida#cite_note-4)
According to the U.S. Census Bureau, the county has a total area of 519 square miles (1,340 km 2), of which 514 square miles (1,330 km 2) is land and 5.3 square miles (14 km 2) (1.0%) is water.[[5]](https://en.wikipedia.org/wiki/Hamilton_County,_Florida#cite_note-GR1-5) It is the only county in Florida entirely north of Interstate 10.[[6]](https://en.wikipedia.org/wiki/Hamilton_County,_Florida#cite_note-6)
Hamilton County is the only county in Florida that is not connected to Florida by land. This is due to it being separated from neighboring Florida counties by river (the Suwannee and the Withlacoochee rivers). It does, however, touch Georgia via land.
*   Echols County, Georgia - north  
*   Columbia County - east  
*   Suwannee County - south  
*   Madison County - west  
*   Lowndes County, Georgia - northwest
The main railroad line through Hamilton County is the Norfolk Southern Railway's Navair District (originally the Georgia Southern and Florida Railway), which runs mostly in close proximity to US 41 from Lake City across a bridge over the Suwannee River and the Columbia-Hamilton County Line southeast of White Plains to the Florida-Georgia State Line northwest of Jennings. A former section of the Atlantic Coast Line Railroad's DuPont—Lakeland Line survives as a rail trail in Jasper.

Historical population| Census | Pop. | Note | %± |  
| --- | --- | --- | --- |  
| 1830 | 553 |  | — |  
| 1840 | 1,464 |  | 164.7% |  
| 1850 | 2,511 |  | 71.5% |  
| 1860 | 4,154 |  | 65.4% |  
| 1870 | 5,749 |  | 38.4% |  
| 1880 | 6,790 |  | 18.1% |  
| 1890 | 8,507 |  | 25.3% |  
| 1900 | 11,881 |  | 39.7% |  
| 1910 | 11,825 |  | −0.5% |  
| 1920 | 9,873 |  | −16.5% |  
| 1930 | 9,454 |  | −4.2% |  
| 1940 | 9,778 |  | 3.4% |  
| 1950 | 8,981 |  | −8.2% |  
| 1960 | 7,705 |  | −14.2% |  
| 1970 | 7,787 |  | 1.1% |  
| 1980 | 8,761 |  | 12.5% |  
| 1990 | 10,930 |  | 24.8% |  
| 2000 | 13,327 |  | 21.9% |  
| 2010 | 14,799 |  | 11.0% |  
| 2020 | 14,004 |  | −5.4% |
</excerpt>

## Search 8 — query: "County Population Totals and Components of Change 2020-2025 Florida 2022 population"
### Rank 1 of 273 — 0.82 (passed on)
<excerpt title="Florida Estimates of Population 2025">
## [PDF page 32]
40  Putnam  76,600  73,321  74,364  70,423  0.33  0.34  0.40  0.44  
41  Columbia  72,388  69,698  67,531  56,513  0.31  0.32  0.36  0.35  
42  Jackson  49,728  47,319  49,746  46,755  0.21  0.22  0.26  0.29  
43  Suwannee  47,274  43,474  41,551  34,844  0.20  0.20  0.22  0.22  
44  Hendry  47,085  39,619  39,140  36,210  0.20  0.18  0.21  0.23

## [PDF page 32]
45  Levy  46,270  42,915  40,801  34,450  0.20  0.20  0.22  0.22  
46  Gadsden  44,790  43,826  46,389  45,087  0.19  0.20  0.25  0.28  
47  Okeecho bee  40,314  39,644  39,996  35,910  0.17  0.18  0.21  0.22  
48  Wakulla  38,189  33,764  30,776  22,863  0.16  0.16  0.16  0.14  
49  DeSoto  35,947  33,976  34,862  32,209  0.15  0.16  0.19  0.20
</excerpt>
### Rank 2 of 273 — 0.80
<excerpt title="Florida Estimates of Population 2025">
## [PDF page 32]
45  Levy  46,270  42,915  40,801  34,450  0.20  0.20  0.22  0.22  
46  Gadsden  44,790  43,826  46,389  45,087  0.19  0.20  0.25  0.28  
47  Okeecho bee  40,314  39,644  39,996  35,910  0.17  0.18  0.21  0.22  
48  Wakulla  38,189  33,764  30,776  22,863  0.16  0.16  0.16  0.14  
49  DeSoto  35,947  33,976  34,862  32,209  0.15  0.16  0.19  0.20

## [PDF page 32]
50  Baker  29,139  28,259  27,115  22,259  0.12  0.13  0.14  0.14  
51  Bradford  27,668  28,303  28,520  26,088  0.12  0.13  0.15  0.16  
52  Washington  26,876  25,318  24,896  20,973  0.11  0.12  0.13  0.13  
53  Hardee  26,042  25,327  27,731  26,938  0.11  0.12  0.15  0.17  
54  T a y lo r  22,011  21,796  22,570  19,256  0.09  0.10  0.12  0.12
</excerpt>
### Rank 3 of 273 — 0.80
<excerpt title="Florida Estimates of Population 2025">
## [PDF page 32]
50  Baker  29,139  28,259  27,115  22,259  0.12  0.13  0.14  0.14  
51  Bradford  27,668  28,303  28,520  26,088  0.12  0.13  0.15  0.16  
52  Washington  26,876  25,318  24,896  20,973  0.11  0.12  0.13  0.13  
53  Hardee  26,042  25,327  27,731  26,938  0.11  0.12  0.15  0.17  
54  T a y lo r  22,011  21,796  22,570  19,256  0.09  0.10  0.12  0.12

## [PDF page 32]
55  Ho lmes  20,042  19,653  19,927  18,564  0.09  0.09  0.11  0.12  
56  Gilchrist  19,716  17,864  16,939  14,437  0.08  0.08  0.09  0.09  
57  Madison  18,859  17,968  19,224  18,733  0.08  0.08  0.10  0.12  
58  Dixie  17,217  16,759  16,422  13,827  0.07  0.08  0.09  0.09  
59  Union  16,821  16,147  15,535  13,442  0.07  0.07  0.08  0.08
</excerpt>
### Rank 4 of 273 — 0.78
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
### Rank 5 of 273 — 0.77
<excerpt title="Florida Estimates of Population 2025">
## [PDF page 23]
Collier  37,562  16,811  21,523  -4,712  42,274  0.0  100.0  
Columbia  2,690  3,678  5,149  -1,471  4,161  0.0  100.0  
DeSoto  1,971  1,956  2,207  -2 51  2,222  0.0  100.0  
Dixie  4 58  7 95  1,401  -6 06  1,064  0.0  100.0  
Duval  83,477  63,254  50,605  12,649  70,828  15.2  84.8

## [PDF page 23]
Escambia  15,823  18,502  20,758  -2,256  18,079  0.0  100.0  
Flagler  25,336  4,253  8,824  -4,571  29,907  0.0  100.0  
Franklin  9 32  4 36  8 50  -4 14  1,346  0.0  100.0  
Gadsden  9 64  2,397  2,929  -5 32  1,496  0.0  100.0  
Gilchrist  1,852  1,014  1,269  -2 55  2,107  0.0  100.0
Glades  9 29  3 40  7 66  -4 26  1,355  0.0  100.0  
Gulf  2,429  5 78  1,117  -5 39  2,968  0.0  100.0  
Hamilton  1 51  7 89  9 96  -2 07  3 58  0.0  100.0  
Hardee  7 15  1,758  1,464  2 94  4 21  41.1  58.9  
Hendry  7,466  2,862  1,935  9 27  6,539  12.4  87.6
</excerpt>

## Search 9 — query: "County Population Totals and Components of Change 2020-2025 Florida 2022 population"
### Rank 1 of 243 — 0.82 (passed on)
<excerpt title="untitled">
## [PDF page 32]
40  Putnam  76,600  73,321  74,364  70,423  0.33  0.34  0.40  0.44  
41  Columbia  72,388  69,698  67,531  56,513  0.31  0.32  0.36  0.35  
42  Jackson  49,728  47,319  49,746  46,755  0.21  0.22  0.26  0.29  
43  Suwannee  47,274  43,474  41,551  34,844  0.20  0.20  0.22  0.22  
44  Hendry  47,085  39,619  39,140  36,210  0.20  0.18  0.21  0.23

## [PDF page 32]
45  Levy  46,270  42,915  40,801  34,450  0.20  0.20  0.22  0.22  
46  Gadsden  44,790  43,826  46,389  45,087  0.19  0.20  0.25  0.28  
47  Okeecho bee  40,314  39,644  39,996  35,910  0.17  0.18  0.21  0.22  
48  Wakulla  38,189  33,764  30,776  22,863  0.16  0.16  0.16  0.14  
49  DeSoto  35,947  33,976  34,862  32,209  0.15  0.16  0.19  0.20
</excerpt>
### Rank 2 of 243 — 0.80
<excerpt title="untitled">

</excerpt>
### Rank 3 of 243 — 0.80
<excerpt title="untitled">

</excerpt>
### Rank 4 of 243 — 0.78
<excerpt title="untitled">

</excerpt>
### Rank 5 of 243 — 0.77
<excerpt title="untitled">

</excerpt>

## Search 10 — query: "Real Gross Domestic Product: All Industries in Jackson County, FL 2022 FRED"
### Rank 1 of 39 — 0.66 (passed on)
<excerpt title="Gross Domestic Product: Government and Government Enterprises in ...">
#
Gross Domestic Product: Government and Government Enterprises in Jackson County, FL (GDPGOVT12063)
Observations
2024: 521,351 | Thousands of U.S. Dollars, Not Seasonally Adjusted |  Annual
Updated: Feb 5, 2026 9:13 AM CST
Next Release Date: Dec 2, 2026
Observations
2024:521,351
Updated: Feb 5, 2026 9:13 AM CST
Next Release Date: Dec 2, 2026
2024:521,351  
2023:491,365  
2022:450,461  
2021:419,512  
2020:410,217  
View All
Units:
Thousands of U.S. Dollars,
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
(a)Gross Domestic Product: Government and Government Enterprises in Jackson County, FL,Thousands of U.S. Dollars,Not Seasonally Adjusted(GDPGOVT12063)
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

#
For example, invert an exchange rate by using formula 1/a, where “a” refers to the first FRED data series added to this line. Or calculate the spread between 2 interest rates, a and b, by using the formula a - b.
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
###### Gross Domestic Product: Government and Government Enterprises in Jackson County, FL
</excerpt>
### Rank 2 of 39 — 0.65
<excerpt title="Gross Domestic Product: Government and Government Enterprises in ...">
# Gross Domestic Product: Government and Government Enterprises in Jackson County, FL (GDPGOVT12063) | FRED | St. Louis Fed
Skip to main content
* * *
*

# Gross Domestic Product: Government and Government Enterprises in Jackson County, FL (GDPGOVT12063) | FRED | St. Louis Fed
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
Home>Categories>U.S. Regional Data>States>Florida>Counties>Jackson County, FL

#
Gross Domestic Product: Government and Government Enterprises in Jackson County, FL (GDPGOVT12063)
Observations
2024: 521,351 | Thousands of U.S. Dollars, Not Seasonally Adjusted |  Annual
Updated: Feb 5, 2026 9:13 AM CST
Next Release Date: Dec 2, 2026
Observations
2024:521,351
Updated: Feb 5, 2026 9:13 AM CST
Next Release Date: Dec 2, 2026
2024:521,351  
2023:491,365  
2022:450,461  
2021:419,512  
2020:410,217  
View All
Units:
Thousands of U.S. Dollars,
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
(a)Gross Domestic Product: Government and Government Enterprises in Jackson County, FL,Thousands of U.S. Dollars,Not Seasonally Adjusted(GDPGOVT12063)
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
</excerpt>
### Rank 3 of 39 — 0.63
<excerpt title="Table Data - Gross Domestic Product: All Industries in Jackson County, FL">
| Title | Gross Domestic Product: All Industries in Jackson County, FL |  
| --- |  
| Series ID | GDPALL12063 |  
| Source | U.S. Bureau of Economic Analysis |  
| Release | Gross Domestic Product by County |  
| Seasonal Adjustment | Not Seasonally Adjusted |  
| Frequency | Annual |  
| Units | Thousands of U.S. Dollars |  
| Date Range | 2001-01-01 to 2024-01-01 |  
| Last Updated | 2026-02-05 9:22 AM CST |  
| Notes | GDP by county is a measure of the market value of final goods and services produced within a county area in a particular period. While other measures of county economies rely mainly on labor market data, these statistics incorporate multiple data sources that capture trends in labor, revenue, and value of production. As a result, the capital-intensive industries are captured more fully than when measured solely by labor data. |

| DATE | VALUE |  
| --- | --- |  
| 2001-01-01 | 803256 |  
| 2002-01-01 | 878332 |  
| 2003-01-01 | 968248 |  
| 2004-01-01 | 1031492 |  
| 2005-01-01 | 1103122 |  
| 2006-01-01 | 1158049 |  
| 2007-01-01 | 1219950 |  
| 2008-01-01 | 1220964 |  
| 2009-01-01 | 1119996 |  
| 2010-01-01 | 1190431 |  
| 2011-01-01 | 1245447 |  
| 2012-01-01 | 1107077 |  
| 2013-01-01 | 1158035 |  
| 2014-01-01 | 1160582 |  
| 2015-01-01 | 1194866 |  
| 2016-01-01 | 1263924 |  
| 2017-01-01 | 1312518 |  
| 2018-01-01 | 1351818 |  
| 2019-01-01 | 1405859 |  
| 2020-01-01 | 1435394 |  
| 2021-01-01 | 1548669 |  

| 2022-01-01 | 1706508 |  
| 2023-01-01 | 1862485 |  
| 2024-01-01 | 1986155 |
</excerpt>
### Rank 4 of 39 — 0.59
<excerpt title="Gross Domestic Product for Jackson County, FL - ERSys®">
# Gross Domestic Product for Jackson County, FL - ERSys®
## Gross Domestic Product Comparisons
2020-04-01 1,626,162.35 1,150,211,170.95 21,575,324.58  
2020-07-01 1,506,766.62 1,065,452,010.17 19,783,470.57  
2020-10-01 1,642,997.37 1,166,407,299.12 21,520,168.79  
2021-01-01 1,660,693.44 1,178,469,288.77 21,894,606.98  
2021-04-01 1,676,955.40 1,222,448,043.34 22,471,578.67  
2021-07-01 1,751,521.66 1,275,510,205.55 23,161,724.45  
2021-10-01 1,804,084.82 1,312,827,863.16 23,695,292.64  
2022-01-01 1,977,578.32 1,358,783,946.97 24,517,753.62  

# Gross Domestic Product for Jackson County, FL - ERSys®
## Gross Domestic Product Comparisons
2022-04-01 1,929,942.04 1,387,051,887.16 24,885,131.04  
2022-07-01 2,012,891.01 1,442,832,952.01 25,658,918.15  
2022-10-01 2,050,173.67 1,489,952,693.36 26,122,333.05  
2023-01-01 2,080,502.42 1,528,321,522.83 26,583,528.62  
2023-04-01 2,033,610.05 1,565,889,286.05 27,013,065.25  
2023-07-01 2,054,875.81 1,582,374,160.57 27,301,166.43  
2023-10-01 2,092,845.84 1,612,733,732.23 27,813,217.88  
2024-01-01 2,130,324.88 1,642,253,691.16 28,141,652.90
</excerpt>
### Rank 5 of 39 — 0.59
<excerpt title="Government and Government Enterprises in Jackson County, FL ...">
# Real Gross Domestic Product: Government and Government Enterprises in Jackson County, FL (REALGDPGOVT12063) | FRED | St. Louis Fed
Skip to main content
* * *
*

# Real Gross Domestic Product: Government and Government Enterprises in Jackson County, FL (REALGDPGOVT12063) | FRED | St. Louis Fed
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
Home>Categories>U.S. Regional Data>States>Florida>Counties>Jackson County, FL

#
Real Gross Domestic Product: Government and Government Enterprises in Jackson County, FL (REALGDPGOVT12063)
Observations
2024: 411,290 | Thousands of Chained 2017 U.S. Dollars, Not Seasonally Adjusted |  Annual
Updated: Feb 5, 2026 8:55 AM CST
Next Release Date: Dec 2, 2026
Observations
2024:411,290
Updated: Feb 5, 2026 8:55 AM CST
Next Release Date: Dec 2, 2026
2024:411,290  
2023:403,437  
2022:389,015  
2021:370,196  
2020:370,896  
View All
Units:
Thousands of Chained 2017 U.S. Dollars,
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
(a)Real Gross Domestic Product: Government and Government Enterprises in Jackson County, FL,Thousands of Chained 2017 U.S. Dollars,Not Seasonally Adjusted(REALGDPGOVT12063)
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
</excerpt>

# Example 5
## Question
According to the Our World in Data website's Maddison Project Database, out of Albania, Algeria, Angola, and Argentina, which countries had an increase in GDP per capita from 1985 to 2022 of more than $8000?

## Expected answer
Albania, Algeria

## Grade 0.00

## Search 1 — query: "Our World in Data Maddison GDP per capita 1985 Albania 2022 Argentina"
### Rank 1 of 352 — 0.74 (passed on)
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
### Rank 2 of 352 — 0.64
<excerpt title="List of countries by past and projected GDP (nominal) per capita">
Albania	4,098	4,440	4,274	4,496	4,585	4,182	4,473	4,988	5,861	6,022  
 Algeria	4,941	5,946	6,058	5,998	6,109	4,692	4,427	4,554	4,568	4,453  
 Andorra	49,030	51,957	45,714	45,630	46,299	38,877	39,595	40,018	42,230	40,688  
 Angola	4,102	5,184	5,702	5,876	6,055	4,676	3,991	4,694	3,689	2,941  
 Antigua and Barbuda	15,343	15,045	15,724	15,051	15,423	15,839	16,164	16,401	17,471	17,899  
 Argentina	10,413	12,788	13,890	14,489	13,209	14,895	12,773	14,618	11,786	9,942  
 Armenia	3,066	3,354	3,622	3,690	3,864	3,527	3,540	3,883	4,205	4,599
</excerpt>
### Rank 3 of 352 — 0.64
<excerpt title="List of countries by past and projected GDP (nominal) per capita">
Andorra	36,974	41,807	41,379	44,484	46,410	50,425	53,988	55,175	55,986	56,685  
 Angola	1,977	2,404	3,905	3,079	3,156	3,588	3,876	4,047	3,777	3,571  
 Antigua and Barbuda	14,420	16,128	18,429	20,100	20,888	21,676	22,504	23,308	24,047	24,809  
 Argentina	8,489	10,610	13,702	14,020	13,550	14,399	16,021	15,741	15,559	15,875  
 Armenia	4,267	4,674	6,539	7,973	8,456	9,496	10,662	11,045	11,739	12,584  
 Aruba	22,558	26,463	30,467	34,314	37,169	40,534	42,934	44,957	46,772	48,394  
 Australia	53,319	64,411	65,778	64,849	65,685	66,379	75,172	78,039	80,039	82,164
</excerpt>
### Rank 4 of 352 — 0.64
<excerpt title="List of countries by past and projected GDP (nominal) per capita">
Argentina	8,315	7,775	2,919	3,666	4,285	5,145	5,951	7,282	9,094	8,282  
 Armenia	663	738	832	986	1,260	1,733	2,268	3,286	4,180	3,109  
 Aruba	20,620	20,672	20,434	20,835	22,567	23,303	24,046	25,836	27,089	24,640  
 Australia	21,398	20,181	22,293	28,305	33,925	37,574	39,706	46,990	49,395	46,457  
 Austria	24,398	24,379	26,246	31,968	36,585	38,208	40,425	46,552	51,327	47,549  
 Azerbaijan	650	696	753	869	1,025	1,547	2,422	3,771	5,508	4,932  
 Bahamas	21,241	21,497	22,505	22,008	21,996	23,406	23,721	24,306	23,657	22,043
</excerpt>
### Rank 5 of 352 — 0.56
<excerpt title="List of countries by past and projected GDP (nominal) per capita">
Argentina	4,680	6,194	7,367	7,522	8,081	7,993	8,330	8,861	8,944	8,388  
 Armenia	650	599	363	347	383	426	537	557	648	636  
 Aruba	12,308	13,496	14,047	14,938	17,342	16,441	16,586	17,927	19,082	19,356  
 Australia	18,940	19,015	18,591	17,888	20,205	21,634	23,777	23,600	20,826	22,547  
 Austria	21,549	22,356	24,906	24,117	25,606	30,162	29,590	26,489	27,131	26,979  
 Azerbaijan	905	914	712	552	446	396	405	500	557	569  
 Bahamas	14,436	13,927	13,656	13,328	13,806	14,309	16,034	17,127	18,998	20,506
</excerpt>

## Search 2 — query: "ourworldindata gdp per capita maddison project database csv"
### Rank 1 of 83 — 0.28 (passed on)
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
### Rank 2 of 83 — 0.21
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
### Rank 3 of 83 — 0.19
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
### Rank 4 of 83 — 0.18
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
### Rank 5 of 83 — 0.16
<excerpt title="Gross domestic product (GDP)">
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

# Gross domestic product (GDP)2022
## Related charts
### Download
#### Our World in Data is free and accessible for everyone.
Help us do this work by making a donation.
Donate now
Our World in Data is a project ofGlobal Change Data Lab, a nonprofit based in the UK (Reg. Charity No. 1186433). Our charts, articles, and data are licensed underCC BY, unless stated otherwise. The source code for our tools and software is made publicly available for transparency and educational reference under acustom license. Re-use requires permission. Third-party materials, including some charts and data, are subject to third-party licenses. See ourFAQs for more details.

# Gross domestic product (GDP)2022
## Related charts
### Download
#### Our World in Data is free and accessible for everyone.
##### Explore
*   Topics  
*   Data  
*   Data Insights

# Gross domestic product (GDP)2022
## Related charts
### Download
#### Our World in Data is free and accessible for everyone.
##### Resources
*   Latest  
*   SDG Tracker  
*   Teaching with OWID

# Gross domestic product (GDP)2022
## Related charts
### Download
#### Our World in Data is free and accessible for everyone.
##### About
*   About us  
*   Organization  
*   Funding  
*   Team  
*   Jobs  
*   FAQs

# Gross domestic product (GDP)2022
## Related charts
### Download
#### Our World in Data is free and accessible for everyone.
##### RSS Feeds
*   Research & Writing  
*   Data Insights

# Gross domestic product (GDP)2022
## Related charts
### Download
#### Our World in Data is free and accessible for everyone.
##### Follow us
*   Privacy policy  
*   Cookie notice  
*   Legal disclaimer  
*   Grapher license  
*   Send feedback

# Gross domestic product (GDP)2022
## Cookies help us build a better website
We are a **non-profit** that relies on reader donations. We never use ads on our website or sell user data.
Reject optional cookies Accept optional cookies
We use a small number of **cookies** and similar technologies to **make our website work**. Some of these are essential and can't be switched off. Other **optional cookies** help us better understand **how our website is used** — by accepting these, you can help us improve our publication for everyone. Read more in our Privacy Policy or manage your cookie settings.
</excerpt>

## Search 3 — query: "Albania GDP per capita 1985 2022 ourworldindata"
### Rank 1 of 199 — 0.46 (passed on)
<excerpt title="List of countries by past and projected GDP (PPP) per capita">
Jump to content  
Main menu  
Search  
Donate  
Create account  
Log in  
Contents hide  
(Top)  
IMF estimates  
Toggle IMF estimates subsection  
1980s  
1990s  
2000s  
2010s  
2020s  
2030s  
See also  
References  
Sources  
External links  
List of countries by past and projected GDP (PPP) per capita  
6 languages  
Article  
Talk  
Read  
Edit source  
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
This is an alphabetical list of countries by past and projected Gross Domestic Product per capita, based on the Purchasing Power Parity (PPP) methodology, not on official exchange rates. Values are given in International Dollars. These figures have been taken from the International Monetary Fund's World Economic Outlook (WEO) Database, October 2026 edition.[1]

IMF estimatesedit source  
1980sedit source  
IMF estimates (1980s)[1]  
Country / territory	1980	1981	1982	1983	1984	1985	1986	1987	1988	1989  
 Afghanistan										  
 Albania	2,174	2,466	2,638	2,713	2,808	2,795	2,953	2,943	2,948	3,274  
 Algeria	4,169	4,559	4,990	5,292	5,609	5,829	5,778	5,729	5,649	6,003  
 Andorra										  
 Angola	1,560	1,589	1,644	1,734	1,856	1,758	1,795	1,866	1,997	2,020  
 Antigua and Barbuda	3,426	3,924	4,211	4,678	5,427	6,129	7,094	7,889	8,723	9,629  
 Argentina	7,178	7,276	7,358	7,821	8,127	7,670	8,277	8,598	8,622	8,230  
 Armenia										  
 Aruba							8,114	9,229	10,969	12,568
</excerpt>
### Rank 2 of 199 — 0.42
<excerpt title="List of countries by past and projected GDP (PPP) per capita">
Antigua and Barbuda	10,300	10,792	10,986	11,578	12,296	11,691	12,348	12,884	13,282	13,633  
 Argentina	8,251	9,300	10,350	11,092	11,838	11,598	12,316	13,389	13,904	13,476  
 Armenia			1,792	1,614	1,799	1,992	2,151	2,264	2,460	2,586  
 Aruba	13,414	14,825	15,914	17,392	18,886	19,274	19,351	20,869	21,405	21,792  
 Australia	18,503	18,712	19,437	20,488	21,732	22,559	23,610	24,907	26,092	27,318  
 Austria	22,155	23,489	24,251	24,692	25,674	26,846	27,955	29,014	30,332	31,856  
 Azerbaijan			3,692	2,895	2,341	2,066	2,134	2,342	2,486	2,781
</excerpt>
### Rank 3 of 199 — 0.40
<excerpt title="List of countries by past and projected GDP (PPP) per capita">
IMF estimatesedit source  
1980sedit source  
IMF estimates (1980s)[1]  
Country / territory	1980	1981	1982	1983	1984	1985	1986	1987	1988	1989  
 Afghanistan										  
 Albania	2,174	2,466	2,638	2,713	2,808	2,795	2,953	2,943	2,948	3,274  
 Algeria	4,169	4,559	4,990	5,292	5,609	5,829	5,778	5,729	5,649	6,003  
 Andorra										  
 Angola	1,560	1,589	1,644	1,734	1,856	1,758	1,795	1,866	1,997	2,020  
 Antigua and Barbuda	3,426	3,924	4,211	4,678	5,427	6,129	7,094	7,889	8,723	9,629  
 Argentina	7,178	7,276	7,358	7,821	8,127	7,670	8,277	8,598	8,622	8,230  
 Armenia										  
 Aruba							8,114	9,229	10,969	12,568
</excerpt>
### Rank 4 of 199 — 0.39
<excerpt title="List of countries by past and projected GDP (PPP) per capita">
Palestine	2,990	2,697	2,333	2,639	3,214	3,583	3,552	3,677	3,919	4,171  
 Yemen										  
 Zambia	1,516	1,584	1,630	1,723	1,835	1,964	2,110	2,267	2,403	2,549  
 Zimbabwe	3,772	3,850	3,618	3,089	2,950	2,793	2,735	2,707	2,294	2,456  
2010sedit source  
IMF estimates (2010s)[1]  
Country / territory	2010	2011	2012	2013	2014	2015	2016	2017	2018	2019  
 Afghanistan	1,900	1,990	2,218	2,303	2,320	2,292	2,303	2,339	2,436	2,589  
 Albania	9,812	10,297	10,719	11,165	11,378	12,343	13,260	14,022	14,962	16,318  
 Algeria	11,431	11,775	12,027	12,287	12,742	12,990	13,333	13,483	13,704	13,851
</excerpt>
### Rank 5 of 199 — 0.38
<excerpt title="List of countries by past and projected GDP (PPP) per capita">
Zimbabwe									3,820	3,842  
2000sedit source  
IMF estimates (2000s)[1]  
Country / territory	2000	2001	2002	2003	2004	2005	2006	2007	2008	2009  
 Afghanistan			1,083	1,113	1,106	1,231	1,283	1,467	1,522	1,782  
 Albania	4,364	4,878	5,194	5,610	6,104	6,678	7,336	8,047	8,885	9,302  
 Algeria	7,448	7,730	8,153	8,724	9,222	9,876	10,320	10,764	11,008	10,993  
 Andorra										  
 Angola	3,856	3,974	4,433	4,518	4,987	5,660	6,290	7,032	7,646	7,555  
 Antigua and Barbuda	14,500	13,915	14,133	15,142	16,283	17,700	20,349	22,601	22,775	19,942  
 Argentina	13,529	13,091	11,733	12,914	14,309	15,911	17,550	19,456	20,433	19,155
</excerpt>

## Search 4 — query: "gdp-per-capita-maddison-project-database csv ourworldindata"
### Rank 1 of 87 — 0.28 (passed on)
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
### Rank 2 of 87 — 0.19
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
### Rank 3 of 87 — 0.18
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
### Rank 4 of 87 — 0.15
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
### Rank 5 of 87 — 0.14
<excerpt title="Our World in Data">
# World regions in the Maddison Project Database
## Select countries
*   - [x]  South Korea      
*   - [x]  Afghanistan      
*   - [x]  Albania      
*   - [x]  Algeria      
*   - [x]  Andorra      
*   - [x]  Angola      
*   - [x]  Antigua and Barbuda      
*   - [x]  Argentina      
*   - [x]  Armenia      
*   - [x]  Australia      
*   - [x]  Austria      
*   - [x]  Azerbaijan      
*   - [x]  Bahamas      
*   - [x]  Bahrain      
*   - [x]  Bangladesh      
*   - [x]  Barbados      
*   - [x]  Belarus      
*   - [x]  Belgium      
*   - [x]  Belize      
*   - [x]  Benin      
*   - [x]  Bhutan      
*   - [x]  Bolivia      
*   - [x]  Bosnia and Herzegovina      
*   - [x]  Botswana      
*   - [x]  Brazil      
*   - [x]  Brunei      
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
*   - [x]  Cuba      
*   - [x]  Cyprus      
*   - [x]  Czechia      
*   - [x]  Democratic Republic of Congo      
*   - [x]  Denmark      
*   - [x]  Djibouti      
*   - [x]  Dominica      
*   - [x]  Dominican Republic
</excerpt>

## Search 5 — query: "gdp-per-capita-maddison-project-database.csv"
### Rank 1 of 97 — 0.40 (passed on)
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
### Rank 2 of 97 — 0.15
<excerpt title="Rebasing 'Maddison': new income comparisons and the shape of long- ...">
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
### Rank 3 of 97 — 0.15
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
### Rank 4 of 97 — 0.09
<excerpt title="Global average GDP per capita over the long run">
# Global average GDP per capita over the long run
## Sources and processing
### How we process data at Our World in Data
##### Notes on our processing step for this indicator
The data presented here from 1990 onwards is from the World Bank. We constructed the data before 1990 using the 1990 World Bank observation and applying the growth rates implied by the Maddison Project Database. Similarly, we built the data before 1820 using the adjusted 1820 estimate calculated by the previous method and applying the growth rates implied by the Maddison Database. These steps are necessary because World Bank data adjusted for inflation and the cost of living between countries is only available from 1990 onwards and also because the three datasets estimate GDP with different prices.
We rounded the adjusted results before 1990 to address uncertainty in the underlying data. We rounded GDP data to the nearest million, and GDP to the nearest hundred.

# Global average GDP per capita over the long run
## Reuse this work
*   All data produced by third-party providers and made available by Our World in Data are subject to the license terms from the original providers. Our work would not be possible without the data providers we rely on, so we ask you to always cite them appropriately (see below). This is crucial to allow data providers to continue doing their work, enhancing, maintaining and updating valuable data.  
*   All data, visualizations, and code produced by Our World in Data are completely open access under theCreative Commons BY license. You have the permission to use, distribute, and reproduce these in any medium, provided the source and authors are credited.

# Global average GDP per capita over the long run
## Reuse this work
### Citations
#### How to cite this page
To cite this page overall, including any descriptions, FAQs or explanations of the data authored by Our World in Data, please use the following citation:
`“Data Page: Global average GDP per capita over the long run”, part of the following publication: Max Roser, Bertha Rohenkohl, Pablo Arriagada, Joe Hasell, Hannah Ritchie, and Esteban Ortiz-Ospina (2023) - “Economic Growth”. Data adapted from Eurostat, OECD, IMF, and World Bank, Bolt and van Zanden, Angus Maddison. Retrieved from https://archive.ourworldindata.org/20261102-112946/grapher/global-average-gdp-per-capita-over-the-long-run.html [online resource] (archived on November 2, 2026).`

# Global average GDP per capita over the long run
## Reuse this work
### Citations
#### How to cite this data
In-line citation If you have limited space (e.g. in data visualizations), you can use this abbreviated in-line citation:
`Eurostat, OECD, IMF, and World Bank (2026); Bolt and van Zanden – Maddison Project Database 2023; Maddison Database 2010 – with major processing by Our World in Data`
Full citation
`Eurostat, OECD, IMF, and World Bank (2026); Bolt and van Zanden – Maddison Project Database 2023; Maddison Database 2010 – with major processing by Our World in Data. “Global average GDP per capita over the long run – Maddison Database, Maddison Project Database, World Bank – In constant international-$. Historical data” [dataset]. Eurostat, OECD, IMF, and World Bank, “World Development Indicators 129”; Bolt and van Zanden, “Maddison Project Database 2023”; Angus Maddison, “Maddison Database 2010” [original data]. Retrieved November 19, 2026 from https://archive.ourworldindata.org/20261102-112946/grapher/global-average-gdp-per-capita-over-the-long-run.html (archived on November 2, 2026).`

# Global average GDP per capita over the long run
## Reuse this work
### Download
#### Quick download
Download the data shown in this chart as a ZIP file containing a CSV file, metadata in JSON format, and a README. The CSV file can be opened in Excel, Google Sheets, and other data analysis tools.
</excerpt>
### Rank 5 of 97 — 0.09
<excerpt title="Global average GDP per capita over the long run">
# Global average GDP per capita over the long run
## Reuse this work
### Download
#### Quick download
Download the data shown in this chart as a ZIP file containing a CSV file, metadata in JSON format, and a README. The CSV file can be opened in Excel, Google Sheets, and other data analysis tools.

# Global average GDP per capita over the long run
## Reuse this work
### Download
#### Download full data Includes all entities and time points#### Download displayed data Includes only the entities and time points currently visible in the chart


# Global average GDP per capita over the long run
## Reuse this work
### Download
#### Data API
Use these URLs to programmatically access this chart's data and configure your requests with the options below.Our documentation provides more informationon how to use the API, and you can find a few code examples below.
Download full data, including all entities and time points
Download only the currently selected data visible in the chart

# Global average GDP per capita over the long run
## Reuse this work
### Download
#### Data API
##### Data URL (CSV format)
`https://ourworldindata.org/grapher/global-average-gdp-per-capita-over-the-long-run.csv?v=1&csvType=full&useColumnShortNames=false`

# Global average GDP per capita over the long run
## Reuse this work
### Download
#### Data API
##### Metadata URL (JSON format)
`https://ourworldindata.org/grapher/global-average-gdp-per-capita-over-the-long-run.metadata.json?v=1&csvType=full&useColumnShortNames=false`

# Global average GDP per capita over the long run
## Reuse this work
### Download
#### Code examples
Examples of how to load this data into different data analysis tools.

# Global average GDP per capita over the long run
## Reuse this work
### Download
#### Code examples
##### Excel / Google Sheets
`=IMPORTDATA("https://ourworldindata.org/grapher/global-average-gdp-per-capita-over-the-long-run.csv?v=1&csvType=full&useColumnShortNames=false")`

# Global average GDP per capita over the long run
## Reuse this work
### Download
#### Code examples
##### Python with Pandas
```  
import pandas as pd  
import requests

# Fetch the data.  
df = pd.read_csv("https://ourworldindata.org/grapher/global-average-gdp-per-capita-over-the-long-run.csv?v=1&csvType=full&useColumnShortNames=false", storage_options = {'User-Agent': 'Our World In Data data fetch/1.0'})

# Fetch the metadata  
metadata = requests.get("https://ourworldindata.org/grapher/global-average-gdp-per-capita-over-the-long-run.metadata.json?v=1&csvType=full&useColumnShortNames=false").json()  
```

# Global average GDP per capita over the long run
## Reuse this work
### Download
#### Code examples
##### R
```  
library(jsonlite)

# Fetch the data  
df <- read.csv("https://ourworldindata.org/grapher/global-average-gdp-per-capita-over-the-long-run.csv?v=1&csvType=full&useColumnShortNames=false")

# Fetch the metadata  
metadata <- fromJSON("https://ourworldindata.org/grapher/global-average-gdp-per-capita-over-the-long-run.metadata.json?v=1&csvType=full&useColumnShortNames=false")  
```

# Global average GDP per capita over the long run
## Reuse this work
### Download
#### Code examples
##### Stata
`import delimited "https://ourworldindata.org/grapher/global-average-gdp-per-capita-over-the-long-run.csv?v=1&csvType=full&useColumnShortNames=false", encoding("utf-8") clear`
Leave us feedback
**Have a question?** You may find an answer in **FAQs**.
Message
Your name
Email address Your name and email will only be used to reply to you and not for any other purpose. If you do not give a valid email, we will not be able to reply to you.
Send message
</excerpt>

## Search 6 — query: "Albania 1985 GDP per capita Maddison 1985 $""
### Rank 1 of 2856 — 0.75 (passed on)
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
### Rank 2 of 2856 — 0.72
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
### Rank 3 of 2856 — 0.69
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
### Rank 4 of 2856 — 0.66
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
### Rank 5 of 2856 — 0.65
<excerpt title="List of countries by past and projected GDP (nominal) per capita">
Jump to content  
Main menu  
Search  
Donate  
Create account  
Log in  
Contents hide  
(Top)  
IMF estimates  
Toggle IMF estimates subsection  
1980s  
1990s  
2000s  
2010s  
2020s  
2030s  
CIA estimates in 1990  
UN estimates  
Toggle UN estimates subsection  
1970s  
1980s  
1990s  
2000s  
2010s  
2020s  
Centre for Economics and Business Research estimate for 2040  
Other sources 1965  
See also  
Sources  
References  
External links  
List of countries by past and projected GDP (nominal) per capita  
8 languages  
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
This is an alphabetical list of countries by past and projected gross domestic product per capita, based on official exchange rates, not on the purchasing power parity (PPP) methodology. Values are given in USDs and have not been adjusted for inflation. These figures have been taken from the International Monetary Fund's World Economic Outlook (WEO) Database October 2026 edition),[1] World Bank, or various sources.

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

## Search 7 — query: "https://ourworldindata.org/grapher/gdp-per-capita-maddison-project-database.csv"
### Rank 1 of 113 — 0.25 (passed on)
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
### Rank 2 of 113 — 0.19
<excerpt title="Search">
## There are no results for this query.
*   ### Primary energy use per person Measured in kilowatt-hours of total energy supply per person.   
*   ### Global primary energy use by source Measured in terawatt-hours of total energy supply.   
*   ### Electricity generation by source Measured in terawatt-hours. 

*   ### Maize production
Download options
*   ### Share of people who are undernourished   
*   ### Malnutrition: Share of children who are stunted Share of children younger than five years old who are defined as stunted. Stunting is when a child is significantly shorter than the average for their age. It is a consequence of poor nutrition or repeated infection.   
*   ### Daily supply of calories per person Measured in kilocalories per person per day. This indicates the calories that are available for consumption, but does not necessarily measure the number of calories actually consumed, since it doesn't factor in consumer waste. 

*   ### Share of population living in extreme poverty Extreme poverty is defined as living below the International Poverty Line of $3 per day. This data is adjusted for inflation and differences in living costs between countries.
Download options
*   ### GDP per capita Long-run data in constant international-$ – GDP per capita is a country's gross domestic product divided by its population. This data is adjusted for inflation and differences in living costs between countries.   
*   ### Distribution of population between different poverty lines This data is adjusted for inflation and differences in living costs between countries.   
*   ### Human Development Index The Human Development Index (HDI) is a summary measure of key dimensions of human development: a long and healthy life, a good education, and a decent standard of living. Higher values indicate higher human development. 

*   ### Literate and illiterate world population Share of adults who can read and write a simple statement about their everyday life.
Download options
*   ### Literacy rate Share of adults who can read and write a simple statement about their everyday life.   
*   ### Average years of schooling Average years of formal education for individuals aged 15-64.   
*   ### Share of children in primary school age who are in school Share of children of who are enrolled in primary education amongst the total population of children of official primary school age. 

*   ### Share of the population using the Internet International Telecommunication Union – Share of the population who used the Internet in the last three months.
Download options

## There are no results for this query.
*   ### Research & development spending as a share of GDP Includes basic research, applied research, and experimental development.   
*   ### Annual number of objects launched into space This includes satellites, probes, landers, crewed spacecrafts, and space station flight elements launched into Earth orbit or beyond.   
*   ### Cost of sequencing a full human genome Cost of sequencing the full genetic information of a human, measured in US$. This data is not adjusted for inflation. 

*   ### Share of population using at least a basic drinking water source A basic drinking water service is water from an improved water source that can be collected within a 30-minute round trip, including queuing.
Download options
*   ### Share of the population with access to electricity   
*   ### Share of the population using at least basic sanitation services Basic sanitation services are defined as improved sanitation facilities, such as toilets or latrines, which are not shared with other households.   
*   ### Who Americans spend their time with, by age Measured in hours per day, based on averages from surveys in the United States between 2010 and 2024. 

*   ### Democracy Classification by Lührmann et al. (2018) based on expert estimates by V-Dem.
Download options
*   ### People living in democracies and autocracies Classification by Lührmann et al. (2018) based on expert estimates by V-Dem.   
*   ### Number of countries with key economic and social rights for women   
*   ### Number of countries protecting core LGBT+ rights Countries that fully implement these core policies. Countries that only partially implement them, such as when laws differ across the country, are not included. 

*   ### Deaths in armed conflicts by region Reported deaths of combatants and civilians due to fighting in armed conflicts. Deaths due to disease and starvation resulting from the conflict are not included. Data for 2026 is incomplete and includes deaths within the first three quarters.
Download options
</excerpt>
### Rank 3 of 113 — 0.18
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
### Rank 4 of 113 — 0.18
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
### Rank 5 of 113 — 0.14
<excerpt title="Global GDP over the long run">
## Data sources
#### Eurostat, OECD, IMF, and World Bank – World Development Indicators
```  
International Comparison Program (ICP), World Bank (WB), uri: https://www.worldbank.org/en/programs/icp/data, note: This information is for ICP’s PPPs utilized in WDI, publisher: International Comparison Program (ICP), date accessed: May 30, 2024, date published: May 30, 2024;  
The Eurostat PPP Programme, Eurostat (ESTAT), uri: https://ec.europa.eu/eurostat/databrowser/explore/all/all_themes, publisher: Eurostat;  
The OECD PPP Programme, Organisation for Economic Co-operation and Development (OECD), uri: https://data-explorer.oecd.org/, publisher: OECD;  
Staff estimates, World Bank (WB);  
National Accounts data files, Organisation for Economic Co-operation and Development (OECD);  
World Economic Outlook database, International Monetary Fund (IMF). Indicator NY.GDP.MKTP.PP.KD (https://data.worldbank.org/indicator/NY.GDP.MKTP.PP.KD). World Development Indicators – World Bank (2026). Accessed on 2026-07-27.  
```

## Data sources
#### Bolt and van Zanden – Maddison Project Database
The Maddison Project Database provides information on comparative economic growth and income levels over the very long run. The 2023 version of this database covers 169 countries and the period up to 2022. The new estimates are presented and discussed in Bolt and Van Zanden (2024), "Maddison style estimates of the evolution of the world economy: A new 2023 update", Journal of Economic Surveys, 1–41.
Retrieved on
April 26, 2024
Retrieved from
Citation
This is the citation of the original data obtained from the source, prior to any processing or adaptation by Our World in Data.
```  
Bolt, Jutta and Jan Luiten van Zanden (2024), "Maddison style estimates of the evolution of the world economy: A new 2023 update", Journal of Economic Surveys, 1–41. DOI: 10.1111/joes.12618.  
The Maddison Project Database builds on the efforts of many researchers who have carefully reconstructed historical data on economic growth and population for individual countries. You can find the full list of sources in the original dataset.  
```

## Data sources
#### Angus Maddison – Maddison Database
The final database version provided by Angus Maddison, covering world population, GDP and per capita GDP from 1-2008 AD.
Retrieved on
December 23, 2022
Retrieved from
Citation
This is the citation of the original data obtained from the source, prior to any processing or adaptation by Our World in Data.

## How to cite
#### How to cite this page
To cite this page overall, including any descriptions, FAQs or explanations of the data authored by Our World in Data, please use the following citation:
`“Data Page: Global GDP over the long run”, part of the following publication: Max Roser, Bertha Rohenkohl, Pablo Arriagada, Joe Hasell, Hannah Ritchie, and Esteban Ortiz-Ospina (2023) - “Economic Growth”. Data adapted from Eurostat, OECD, IMF, and World Bank, Bolt and van Zanden, Angus Maddison. Retrieved from https://archive.ourworldindata.org/20261102-112946/grapher/global-gdp-over-the-long-run.html [online resource] (archived on November 2, 2026).`
</excerpt>

## Search 8 — query: "https://ourworldindata.org/grapher/gdp-per-capita-maddison-project-database.csv"
### Rank 1 of 113 — 0.25 (passed on)
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
### Rank 2 of 113 — 0.19
<excerpt title="untitled">

</excerpt>
### Rank 3 of 113 — 0.18
<excerpt title="untitled">

</excerpt>
### Rank 4 of 113 — 0.18
<excerpt title="untitled">

</excerpt>
### Rank 5 of 113 — 0.14
<excerpt title="untitled">

</excerpt>

## Search 9 — query: "https://ourworldindata.org/grapher/gdp-per-capita-maddison-project-database.csv"
### Rank 1 of 113 — 0.25 (passed on)
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
### Rank 2 of 113 — 0.19
<excerpt title="untitled">

</excerpt>
### Rank 3 of 113 — 0.18
<excerpt title="untitled">

</excerpt>
### Rank 4 of 113 — 0.18
<excerpt title="untitled">

</excerpt>
### Rank 5 of 113 — 0.14
<excerpt title="untitled">

</excerpt>

## Search 10 — query: "https://ourworldindata.org/grapher/gdp-per-capita-maddison-project-database.csv"
### Rank 1 of 89 — 0.25 (passed on)
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
### Rank 2 of 89 — 0.18
<excerpt title="untitled">

</excerpt>
### Rank 3 of 89 — 0.18
<excerpt title="untitled">

</excerpt>
### Rank 4 of 89 — 0.15
<excerpt title="Our World in Data">
# Human Development Index vs. GDP per capita 2023
## Select countries and regions
*   - [x]  South Korea      
*   - [x]  Afghanistan      
*   - [x]  Albania      
*   - [x]  Algeria      
*   - [x]  Andorra      
*   - [x]  Angola      
*   - [x]  Antigua and Barbuda      
*   - [x]  Argentina      
*   - [x]  Armenia      
*   - [x]  Australia      
*   - [x]  Austria      
*   - [x]  Azerbaijan      
*   - [x]  Bahamas      
*   - [x]  Bahrain      
*   - [x]  Bangladesh      
*   - [x]  Barbados      
*   - [x]  Belarus      
*   - [x]  Belgium      
*   - [x]  Belize      
*   - [x]  Benin      
*   - [x]  Bhutan      
*   - [x]  Bolivia      
*   - [x]  Bosnia and Herzegovina      
*   - [x]  Botswana      
*   - [x]  Brazil      
*   - [x]  Brunei      
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
</excerpt>
### Rank 5 of 89 — 0.14
<excerpt title="untitled">

</excerpt>

For each search, read the top excerpt and the ones ranked below it, and judge whether the order is right for answering the question. An excerpt holding the answer, or a fact that leads to it, should outrank one that only repeats the query's words or covers the topic without a checkable fact. If none of the excerpts holds anything useful, that is the search's fault, not this instruction's. Find the ranking error that cost the most and write a new instruction that fixes it. Replace or compress existing text where you can; avoid making it much longer. Do not write the "Original question" or "Search query" lines; they are appended for you. Do not copy any fact, name, site or topic from these examples.

Provide the new instruction within ``` blocks.
