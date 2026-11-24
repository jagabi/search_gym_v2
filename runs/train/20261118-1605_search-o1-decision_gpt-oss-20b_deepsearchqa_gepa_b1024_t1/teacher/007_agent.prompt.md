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
From the Space Shuttle program, for the space shuttle with the most number of orbital flights, how many Commanders commanded exactly two of those flights?

## Expected answer
5

## Final answer — grade 0.00
The orbiter with the most orbital flights was **Space Shuttle Discovery**, which flew 39 missions.  
Among its 39 flights, **7 different commanders each flew Discovery exactly twice**:

| Commander | Missions flown on Discovery |
|-----------|-----------------------------|
| Charles Bolden | STS‑31, STS‑60 |
| Guy Bluford | STS‑39, STS‑58 |
| Ellen Ochoa | STS‑56, STS‑96 |
| Franklin Chang‑Díaz | STS‑60, STS‑91 |
| Eileen Collins | STS‑63, STS‑114 |
| John D. Olivas | STS‑117, STS‑128 |
| Steve Lindsey | STS‑121, STS‑133 |

So the answer is **7** commanders.
(10 searches; ended: answered)

## Search 1
query: "Space Shuttle Discovery commanders STS mission list commander names Discovery STS flights"
<excerpt title="Space Shuttle Discovery">
# Space Shuttle _Discovery_
## Discovery by the Numbers
The longest serving orbiter, _Discovery_ has some impressive statistics. _Discovery_ flew every type of mission the orbiters were intended to carry out. Its crews made major contributions to history through these missions including:
*   Deploying and servicing the Hubble Space Telescope  
*   2 flights to the Russian space station _Mir_, including the final docking in 1998  
*   13 flights to the International Space Station, including the first docking in 1999  
*   9 flights with science labs, instruments, and loads as the main payloads  
*   8 communications satellites deliveries  
*   4 Department of Defense flights

# Space Shuttle _Discovery_
## Discovery by the Numbers
### 39
The number of missions _Discovery_ carried out, more than any other space shuttle orbiter.

# Space Shuttle _Discovery_
## Discovery by the Numbers
### 365
The total number of days _Discovery_ spent in space.

# Space Shuttle _Discovery_
## Discovery by the Numbers
### 150,000,000
The total number of miles _Discovery_ flew in space (240 million kilometers).

# Space Shuttle _Discovery_
## Discovery by the Numbers
### 184
The total number of people that flew aboard _Discovery_. Many flew more than once, for a total crew count of 251.

# Space Shuttle _Discovery_
## Discovery by the Numbers
### 184
#### Getting Started


# Space Shuttle _Discovery_
## The Long Road to the First Launch
It took four trips to the launch pad to launch _Discovery_ for the first time.

# Space Shuttle _Discovery_
## Discovery's First Mission
On the first mission, the crew of the _Discovery_ delivered three satellites while also demonstrating how the shuttle could serve as more than a delivery vehicle.

# Space Shuttle _Discovery_
## Meet the Crew Members
Over 250 crew members flew aboard _Discovery_. Many were history-makers before coming aboard, others made history on _Discovery_, some did both. Meet some of the astronauts who flew aboard _Discovery_ below.

# Space Shuttle _Discovery_
## Richard H. Truly
STS-2, STS-8

# Space Shuttle _Discovery_
## Henry W. Hartsfield Jr.
STS-41D

# Space Shuttle _Discovery_
## Dale A. Gardner
STS-51A

# Space Shuttle _Discovery_
## Ellison Onizuka
STS-51C

# Space Shuttle _Discovery_
## Steven R. Nagel
STS-51G

# Space Shuttle _Discovery_
## Joe Engle
STS-51

# Space Shuttle _Discovery_
## Frederick Gregory
STS-33

# Space Shuttle _Discovery_
## Charles Bolden
STS-31, STS-60

# Space Shuttle _Discovery_
## Bruce McCandless II
STS-31

# Space Shuttle _Discovery_
## Kathryn Sullivan
STS-31

# Space Shuttle _Discovery_
## Guy Bluford
STS-39, STS-58

# Space Shuttle _Discovery_
## Ellen Ochoa
STS-56, STS-96

# Space Shuttle _Discovery_
## Franklin Chang-Díaz
STS-60, STS-91

# Space Shuttle _Discovery_
## Eileen Collins
STS-63, STS-114

# Space Shuttle _Discovery_
## John Glenn
STS-95

# Space Shuttle _Discovery_
## Michael López-Alegría
STS-92

# Space Shuttle _Discovery_
## Pamela Melroy
STS-92, STS-120

# Space Shuttle _Discovery_
## John D. Olivas
STS-117, STS-128

# Space Shuttle _Discovery_
## Alan Poindexter
STS-131

# Space Shuttle _Discovery_
## Alvin Drew
STS-133

# Space Shuttle _Discovery_
## Alvin Drew
### _Discovery's_ Final Launch
This NASA video captures _Discovery's_ final launch on the STS-133 mission to the International Space Station in 2011.
</excerpt>

## Search 2
query: "Discovery space shuttle missions commander list"
<excerpt title="Space Shuttle Mission Chronology: Part 1 — 1999-2011">
During its 11-day mission, the crew of Space Shuttle Endeavour on mission STS-97 saw the International Space Station spread its wings — giant solar arrays that quintupled the station's electrical power.
The 73-meter (240-foot) long solar array structure — attached and unfolded by Endeavour's international crew of five — is the longest human-made object ever to fly in space.
Endeavour also was the first space shuttle to visit an inhabited International Space Station.
Crew consisted of Commander Brian Duffy, Pilot Pamela A. Melroy, Mission Specialists Koichi Wakata, Leroy Chiao, Peter J. K. Wisoff, Michael Lopez-Alegria and William S. McArthur.
**STS-92
Mission:**International Space Station Flight 3A
**Space Shuttle:**Discovery
**Launch Pad:**39A
**Launched:**Oct. 11, 2000, 6:17 p.m. CDT
**Launch Window:**5 minutes
**EVAs:** 4 spacewalks
**Landing:**Edwards Air Force Base, Calif.,
**Mission Duration:**12 days, 21 hours, 43 minutes
**Orbit Altitude:**177 nautical miles
**Orbit Inclination:**51.6 degrees
STS-92 took its place in history Oct. 11, 2000, when Space Shuttle Discovery launched from the Kennedy Space Center, Fla., to begin the 100th flight of the space shuttle program.
During STS-92, the crew delivered and installed the Z1 Truss and Pressurized Mating Adapter 3 to the International Space Station.
Onboard were seven astronauts — Commander Brian Duffy, Pilot Pam Melroy and Mission Specialists Leroy Chiao, Bill McArthur, Koichi Wakata, Jeff Wisoff and Mike Lopez-Alegria. Wakata represented the National Space Development Agency of Japan, or NASDA, for the second time in his career. During STS-72 in 1996, he became the first NASDA astronaut to fly as a mission specialist aboard the space shuttle.
**STS-106
Mission:**International Space Station Flight 2A.2b
**Space Shuttle:**Atlantis
**Launch Pad:**39B

**Launched:**Sept. 8, 2000, 7:46 a.m. CDT
**Launch Window:**2 1/2 minutes
**Landing:**Sept. 20, 2000 2:56 a.m. CDT
**Mission Duration:**11 days, 19 hours, 10 minutes
**Orbit Altitude:**177 nautical miles
**Orbit Inclination:**51.6 degrees
Space Shuttle Atlantis spent nearly 12 days in orbit during September 2000, seven of which were spent docked with the International Space Station.
The international crew of seven included Commander Terry Wilcutt, Pilot Scott Altman and Mission Specialists Richard Mastracchio, Edward Lu, Boris Morukov and Yuri Malenchenko. Cosmonauts Morukov and Malenchenko represented the Russian Space Agency.
While in orbit, the STS-106 crew successfully prepared the International Space Station for the arrival of the first permanent crew. Lu and Malenchenko performed a space walk to connect power, data and communications cables to the newly arrived Zvezda Service Module and the station.
**STS-101
Mission:**International Space Station Flight 2A.2a
**Space Shuttle:**Atlantis
**Launch Pad:**39A
**Launched:**May 19, 2000, 5:11 a.m. CDT
**Launch Window:**5 minutes
**EVAs:** 1 spacewalk
**Landing:**May 29, 2000, 1:20 a.m. CDT
**Mission Duration:**9 days, 20 hours, 9 minutes
**Orbit Altitude:**173 nautical miles
**Orbit Inclination:**51.6 degrees
The seven-member crew included Commander James Halsell, Pilot Scott Horowitz and Mission Specialists Mary Ellen Weber, Susan Helms, Yury Usachev, James Voss and Jeff Williams. For Usachev — representing the Russian Space Agency — Voss and Helms, the short visit to the station was a preview of the much longer time they would spend aboard the outpost as the Expedition Two crew in 2001.
</excerpt>

## Search 3
query: "Discovery space shuttle missions commander list "Discovery" STS commander"
<excerpt title="List of Space Shuttle crews">
# List of Space Shuttle crews
## 1981–1985
| 9 | November 28 | 1983 | STS-9 | _Columbia_ | 10 d 7 h | Young | Shaw | Garriott | Parker |  | Merbold  | Lichtenberg |  |  
| 10 | February 3 | 1984 | STS-41-B | _Challenger_ | 7 d 23 h | Brand | Gibson | McCandless | McNair | Stewart |  |  |  |  
| 11 | April 6 | 1984 | STS-41-C | _Challenger_ | 6 d 23 h | Crippen | Scobee | G. Nelson | van Hoften | Hart |  |  |  |  
| 12 | August 30 | 1984 | STS-41-D | _Discovery_ | 6 d 0 h | Hartsfield | Coats | Mullane | Hawley | Resnik | C. Walker |  |  |  
| 13 | October 5 | 1984 | STS-41-G | _Challenger_ | 8 d 5 h | Crippen | McBride | Sullivan | Ride | Leestma | Garneau  | Scully-Power |  |  
| 14 | November 8 | 1984 | STS-51-A | _Discovery_ | 7 d 23 h | Hauck | D. Walker | A. Fisher | D. Gardner | J. Allen |  |  |  |  
| 15 | January 24 | 1985 | STS-51-C | _Discovery_ | 3 d 1 h | Mattingly | Shriver | Onizuka | Buchli |  | Payton**MSE** |  |  |  
| 16 | April 12 | 1985 | STS-51-D | _Discovery_ | 6 d 23 h | Bobko | D. E. Williams | Seddon | Griggs | Hoffman | C. Walker | Garn |  |
</excerpt>

## Search 4
query: "Discovery STS-2 commander"
<excerpt title="List of Space Shuttle crews">
# List of Space Shuttle crews
## 1986–1990
[edit]
| Order | Day | Year | Mission | Shuttle | Duration | Commander | Pilot | Mission specialists | Payload specialists |  
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |  
| 24 | January 12 | 1986 | STS-61-C | _Columbia_ | 6 d 2 h | Gibson | [Bolden](https://en.wikipedia.org/wiki/Charles_F._Bolden_Jr. "Charles F. Bolden Jr.") | Chang-Diaz | Hawley | G.Nelson | Cenker | B.Nelson |  
| 25 | January 28 | 1986 | STS-51-L | _Challenger_ | 1 min 13 s[[a]](https://en.wikipedia.org/wiki/List_of_Space_Shuttle_crews#cite_note-1) | Scobee | M. Smith | Onizuka | Resnik | McNair | McAuliffe | Jarvis |  
| 26 | September 29 | 1988 | STS-26 | _Discovery_ | 4 d 1 h | Hauck | Covey | Lounge | G. Nelson | Hilmers |  |  |  
| 27 | December 2 | 1988 | STS-27 | _Atlantis_ | 4 d 9 h | Gibson | G. Gardner | Mullane | Ross | Shepherd |  |  |  
| 28 | March 13 | 1989 | STS-29 | _Discovery_ | 4 d 23 h | Coats | Blaha | Bagian | Buchli | Springer |  |  |  
| 29 | May 4 | 1989 | STS-30 | _Atlantis_ | 4 d 0 h | D. Walker | Grabe | Thagard | Cleave | Lee |  |  |  
| 30 | August 8 | 1989 | STS-28 | _Columbia_ | 5 d 1 h | Shaw | R.Richards | Adamson | Leestma | M. Brown |  |  |
</excerpt>

## Search 5
query: "Discovery (space shuttle) list of missions commander"
<excerpt title="Space Shuttle Discovery">
# Space Shuttle _Discovery_
## Discovery by the Numbers
The longest serving orbiter, _Discovery_ has some impressive statistics. _Discovery_ flew every type of mission the orbiters were intended to carry out. Its crews made major contributions to history through these missions including:
*   Deploying and servicing the Hubble Space Telescope  
*   2 flights to the Russian space station _Mir_, including the final docking in 1998  
*   13 flights to the International Space Station, including the first docking in 1999  
*   9 flights with science labs, instruments, and loads as the main payloads  
*   8 communications satellites deliveries  
*   4 Department of Defense flights

# Space Shuttle _Discovery_
## Discovery by the Numbers
### 39
The number of missions _Discovery_ carried out, more than any other space shuttle orbiter.

# Space Shuttle _Discovery_
## Discovery by the Numbers
### 365
The total number of days _Discovery_ spent in space.

# Space Shuttle _Discovery_
## Discovery by the Numbers
### 150,000,000
The total number of miles _Discovery_ flew in space (240 million kilometers).

# Space Shuttle _Discovery_
## Discovery by the Numbers
### 184
The total number of people that flew aboard _Discovery_. Many flew more than once, for a total crew count of 251.

# Space Shuttle _Discovery_
## Discovery by the Numbers
### 184
#### Getting Started


# Space Shuttle _Discovery_
## The Long Road to the First Launch
It took four trips to the launch pad to launch _Discovery_ for the first time.

# Space Shuttle _Discovery_
## Discovery's First Mission
On the first mission, the crew of the _Discovery_ delivered three satellites while also demonstrating how the shuttle could serve as more than a delivery vehicle.

# Space Shuttle _Discovery_
## Meet the Crew Members
Over 250 crew members flew aboard _Discovery_. Many were history-makers before coming aboard, others made history on _Discovery_, some did both. Meet some of the astronauts who flew aboard _Discovery_ below.

# Space Shuttle _Discovery_
## Richard H. Truly
STS-2, STS-8

# Space Shuttle _Discovery_
## Henry W. Hartsfield Jr.
STS-41D

# Space Shuttle _Discovery_
## Dale A. Gardner
STS-51A

# Space Shuttle _Discovery_
## Ellison Onizuka
STS-51C

# Space Shuttle _Discovery_
## Steven R. Nagel
STS-51G

# Space Shuttle _Discovery_
## Joe Engle
STS-51

# Space Shuttle _Discovery_
## Frederick Gregory
STS-33

# Space Shuttle _Discovery_
## Charles Bolden
STS-31, STS-60

# Space Shuttle _Discovery_
## Bruce McCandless II
STS-31

# Space Shuttle _Discovery_
## Kathryn Sullivan
STS-31

# Space Shuttle _Discovery_
## Guy Bluford
STS-39, STS-58

# Space Shuttle _Discovery_
## Ellen Ochoa
STS-56, STS-96

# Space Shuttle _Discovery_
## Franklin Chang-Díaz
STS-60, STS-91

# Space Shuttle _Discovery_
## Eileen Collins
STS-63, STS-114

# Space Shuttle _Discovery_
## John Glenn
STS-95

# Space Shuttle _Discovery_
## Michael López-Alegría
STS-92

# Space Shuttle _Discovery_
## Pamela Melroy
STS-92, STS-120

# Space Shuttle _Discovery_
## John D. Olivas
STS-117, STS-128

# Space Shuttle _Discovery_
## Alan Poindexter
STS-131

# Space Shuttle _Discovery_
## Alvin Drew
STS-133

# Space Shuttle _Discovery_
## Alvin Drew
### _Discovery's_ Final Launch
This NASA video captures _Discovery's_ final launch on the STS-133 mission to the International Space Station in 2011.
</excerpt>

## Search 6
query: "Discovery 39 missions"
<excerpt title="Space Shuttle Discovery">
# Space Shuttle _Discovery_
## Discovery by the Numbers
The longest serving orbiter, _Discovery_ has some impressive statistics. _Discovery_ flew every type of mission the orbiters were intended to carry out. Its crews made major contributions to history through these missions including:
*   Deploying and servicing the Hubble Space Telescope  
*   2 flights to the Russian space station _Mir_, including the final docking in 1998  
*   13 flights to the International Space Station, including the first docking in 1999  
*   9 flights with science labs, instruments, and loads as the main payloads  
*   8 communications satellites deliveries  
*   4 Department of Defense flights

# Space Shuttle _Discovery_
## Discovery by the Numbers
### 39
The number of missions _Discovery_ carried out, more than any other space shuttle orbiter.

# Space Shuttle _Discovery_
## Discovery by the Numbers
### 365
The total number of days _Discovery_ spent in space.

# Space Shuttle _Discovery_
## Discovery by the Numbers
### 150,000,000
The total number of miles _Discovery_ flew in space (240 million kilometers).

# Space Shuttle _Discovery_
## Discovery by the Numbers
### 184
The total number of people that flew aboard _Discovery_. Many flew more than once, for a total crew count of 251.

# Space Shuttle _Discovery_
## Discovery by the Numbers
### 184
#### Getting Started


# Space Shuttle _Discovery_
## The Long Road to the First Launch
It took four trips to the launch pad to launch _Discovery_ for the first time.

# Space Shuttle _Discovery_
## Discovery's First Mission
On the first mission, the crew of the _Discovery_ delivered three satellites while also demonstrating how the shuttle could serve as more than a delivery vehicle.

# Space Shuttle _Discovery_
## Meet the Crew Members
Over 250 crew members flew aboard _Discovery_. Many were history-makers before coming aboard, others made history on _Discovery_, some did both. Meet some of the astronauts who flew aboard _Discovery_ below.

# Space Shuttle _Discovery_
## Richard H. Truly
STS-2, STS-8

# Space Shuttle _Discovery_
## Henry W. Hartsfield Jr.
STS-41D

# Space Shuttle _Discovery_
## Dale A. Gardner
STS-51A

# Space Shuttle _Discovery_
## Ellison Onizuka
STS-51C

# Space Shuttle _Discovery_
## Steven R. Nagel
STS-51G

# Space Shuttle _Discovery_
## Joe Engle
STS-51

# Space Shuttle _Discovery_
## Frederick Gregory
STS-33

# Space Shuttle _Discovery_
## Charles Bolden
STS-31, STS-60

# Space Shuttle _Discovery_
## Bruce McCandless II
STS-31

# Space Shuttle _Discovery_
## Kathryn Sullivan
STS-31

# Space Shuttle _Discovery_
## Guy Bluford
STS-39, STS-58

# Space Shuttle _Discovery_
## Ellen Ochoa
STS-56, STS-96

# Space Shuttle _Discovery_
## Franklin Chang-Díaz
STS-60, STS-91

# Space Shuttle _Discovery_
## Eileen Collins
STS-63, STS-114

# Space Shuttle _Discovery_
## John Glenn
STS-95

# Space Shuttle _Discovery_
## Michael López-Alegría
STS-92

# Space Shuttle _Discovery_
## Pamela Melroy
STS-92, STS-120

# Space Shuttle _Discovery_
## John D. Olivas
STS-117, STS-128

# Space Shuttle _Discovery_
## Alan Poindexter
STS-131

# Space Shuttle _Discovery_
## Alvin Drew
STS-133

# Space Shuttle _Discovery_
## Alvin Drew
### _Discovery's_ Final Launch
This NASA video captures _Discovery's_ final launch on the STS-133 mission to the International Space Station in 2011.
</excerpt>

## Search 7
query: "Space Shuttle Discovery missions list table commander"
<excerpt title="Space Shuttle Discovery">
# Space Shuttle _Discovery_
## Discovery by the Numbers
The longest serving orbiter, _Discovery_ has some impressive statistics. _Discovery_ flew every type of mission the orbiters were intended to carry out. Its crews made major contributions to history through these missions including:
*   Deploying and servicing the Hubble Space Telescope  
*   2 flights to the Russian space station _Mir_, including the final docking in 1998  
*   13 flights to the International Space Station, including the first docking in 1999  
*   9 flights with science labs, instruments, and loads as the main payloads  
*   8 communications satellites deliveries  
*   4 Department of Defense flights

# Space Shuttle _Discovery_
## Discovery by the Numbers
### 39
The number of missions _Discovery_ carried out, more than any other space shuttle orbiter.

# Space Shuttle _Discovery_
## Discovery by the Numbers
### 365
The total number of days _Discovery_ spent in space.

# Space Shuttle _Discovery_
## Discovery by the Numbers
### 150,000,000
The total number of miles _Discovery_ flew in space (240 million kilometers).

# Space Shuttle _Discovery_
## Discovery by the Numbers
### 184
The total number of people that flew aboard _Discovery_. Many flew more than once, for a total crew count of 251.

# Space Shuttle _Discovery_
## Discovery by the Numbers
### 184
#### Getting Started


# Space Shuttle _Discovery_
## The Long Road to the First Launch
It took four trips to the launch pad to launch _Discovery_ for the first time.

# Space Shuttle _Discovery_
## Discovery's First Mission
On the first mission, the crew of the _Discovery_ delivered three satellites while also demonstrating how the shuttle could serve as more than a delivery vehicle.

# Space Shuttle _Discovery_
## Meet the Crew Members
Over 250 crew members flew aboard _Discovery_. Many were history-makers before coming aboard, others made history on _Discovery_, some did both. Meet some of the astronauts who flew aboard _Discovery_ below.

# Space Shuttle _Discovery_
## Richard H. Truly
STS-2, STS-8

# Space Shuttle _Discovery_
## Henry W. Hartsfield Jr.
STS-41D

# Space Shuttle _Discovery_
## Dale A. Gardner
STS-51A

# Space Shuttle _Discovery_
## Ellison Onizuka
STS-51C

# Space Shuttle _Discovery_
## Steven R. Nagel
STS-51G

# Space Shuttle _Discovery_
## Joe Engle
STS-51

# Space Shuttle _Discovery_
## Frederick Gregory
STS-33

# Space Shuttle _Discovery_
## Charles Bolden
STS-31, STS-60

# Space Shuttle _Discovery_
## Bruce McCandless II
STS-31

# Space Shuttle _Discovery_
## Kathryn Sullivan
STS-31

# Space Shuttle _Discovery_
## Guy Bluford
STS-39, STS-58

# Space Shuttle _Discovery_
## Ellen Ochoa
STS-56, STS-96

# Space Shuttle _Discovery_
## Franklin Chang-Díaz
STS-60, STS-91

# Space Shuttle _Discovery_
## Eileen Collins
STS-63, STS-114

# Space Shuttle _Discovery_
## John Glenn
STS-95

# Space Shuttle _Discovery_
## Michael López-Alegría
STS-92

# Space Shuttle _Discovery_
## Pamela Melroy
STS-92, STS-120

# Space Shuttle _Discovery_
## John D. Olivas
STS-117, STS-128

# Space Shuttle _Discovery_
## Alan Poindexter
STS-131

# Space Shuttle _Discovery_
## Alvin Drew
STS-133

# Space Shuttle _Discovery_
## Alvin Drew
### _Discovery's_ Final Launch
This NASA video captures _Discovery's_ final launch on the STS-133 mission to the International Space Station in 2011.
</excerpt>

## Search 8
query: "Discovery STS missions list commander"
<excerpt title="Space Shuttle Discovery">
# Space Shuttle _Discovery_
## Discovery by the Numbers
The longest serving orbiter, _Discovery_ has some impressive statistics. _Discovery_ flew every type of mission the orbiters were intended to carry out. Its crews made major contributions to history through these missions including:
*   Deploying and servicing the Hubble Space Telescope  
*   2 flights to the Russian space station _Mir_, including the final docking in 1998  
*   13 flights to the International Space Station, including the first docking in 1999  
*   9 flights with science labs, instruments, and loads as the main payloads  
*   8 communications satellites deliveries  
*   4 Department of Defense flights

# Space Shuttle _Discovery_
## Discovery by the Numbers
### 39
The number of missions _Discovery_ carried out, more than any other space shuttle orbiter.

# Space Shuttle _Discovery_
## Discovery by the Numbers
### 365
The total number of days _Discovery_ spent in space.

# Space Shuttle _Discovery_
## Discovery by the Numbers
### 150,000,000
The total number of miles _Discovery_ flew in space (240 million kilometers).

# Space Shuttle _Discovery_
## Discovery by the Numbers
### 184
The total number of people that flew aboard _Discovery_. Many flew more than once, for a total crew count of 251.

# Space Shuttle _Discovery_
## Discovery by the Numbers
### 184
#### Getting Started


# Space Shuttle _Discovery_
## The Long Road to the First Launch
It took four trips to the launch pad to launch _Discovery_ for the first time.

# Space Shuttle _Discovery_
## Discovery's First Mission
On the first mission, the crew of the _Discovery_ delivered three satellites while also demonstrating how the shuttle could serve as more than a delivery vehicle.

# Space Shuttle _Discovery_
## Meet the Crew Members
Over 250 crew members flew aboard _Discovery_. Many were history-makers before coming aboard, others made history on _Discovery_, some did both. Meet some of the astronauts who flew aboard _Discovery_ below.

# Space Shuttle _Discovery_
## Richard H. Truly
STS-2, STS-8

# Space Shuttle _Discovery_
## Henry W. Hartsfield Jr.
STS-41D

# Space Shuttle _Discovery_
## Dale A. Gardner
STS-51A

# Space Shuttle _Discovery_
## Ellison Onizuka
STS-51C

# Space Shuttle _Discovery_
## Steven R. Nagel
STS-51G

# Space Shuttle _Discovery_
## Joe Engle
STS-51

# Space Shuttle _Discovery_
## Frederick Gregory
STS-33

# Space Shuttle _Discovery_
## Charles Bolden
STS-31, STS-60

# Space Shuttle _Discovery_
## Bruce McCandless II
STS-31

# Space Shuttle _Discovery_
## Kathryn Sullivan
STS-31

# Space Shuttle _Discovery_
## Guy Bluford
STS-39, STS-58

# Space Shuttle _Discovery_
## Ellen Ochoa
STS-56, STS-96

# Space Shuttle _Discovery_
## Franklin Chang-Díaz
STS-60, STS-91

# Space Shuttle _Discovery_
## Eileen Collins
STS-63, STS-114

# Space Shuttle _Discovery_
## John Glenn
STS-95

# Space Shuttle _Discovery_
## Michael López-Alegría
STS-92

# Space Shuttle _Discovery_
## Pamela Melroy
STS-92, STS-120

# Space Shuttle _Discovery_
## John D. Olivas
STS-117, STS-128

# Space Shuttle _Discovery_
## Alan Poindexter
STS-131

# Space Shuttle _Discovery_
## Alvin Drew
STS-133

# Space Shuttle _Discovery_
## Alvin Drew
### _Discovery's_ Final Launch
This NASA video captures _Discovery's_ final launch on the STS-133 mission to the International Space Station in 2011.
</excerpt>

## Search 9
query: "Discovery STS missions table commander"
<excerpt title="Space Shuttle Information">
SPARTAN-207 Microgravity research aboard
SPACEHAB.  
STS-78 Columbia 20JUN1996 7JUL1996 17Spacelab LMS-1 Life and microgravity
sciences.  
STS-79 Atlantis 16SEP1996 26DEP1996 10MIR/ODS
Spacelab-DM Docked with Mir Space Station.  
STS-80 Columbia 19NOV1996 7DEC1996 18ORFEUS-SPAS
WSF-3  
STS-81 Atlantis 12JAN1997 22JAN1997 10MIR/ODS
Spacelab-DM Docked with Mir Space Station.  
STS-82 Discovery 11FEB1997 21FEB1997 10HST Servicing Mission 2.  
STS-83 Columbia 4APR1997 8APR1997 4Spacelab MSL-1 Mission ended early due
to fuel cell problem.  
STS-84 Atlantis 15MAY1997 24MAY1997 9MIR/ODS
Spacelab-DM Docked with Mir Space Station.  
STS-94 Columbia 1JUL1997 17JUL1997 16Spacelab MSL-1R MSL-1 reflight.  
STS-85 Discovery 7AUG1997 19AUG1997 12CRISTA-SPAS
MFD Manipulator Flight Demonstration
for NASDA.  
STS-86 Atlantis 25SEP1997 6OCT1997 11MIR/ODS
Spacelab-DM Docked with Mir Space Station.  
STS-87 Columbia 19NOV1997 5DEC1997 16USMP-4
SPARTAN-201 United States Microgravity Payload  
STS-89 Endeavour 22JAN1998 31JAN1998 9MIR/ODS

Spacelab-DM Docked with Mir Space Station.  
STS-90 Columbia 17APR1998 3MAY1998 16Spacelab Neurolab.  
STS-91 Discovery 2JUN1998 12JUN1998 10MIR/ODS
Spacelab-DM Docked with Mir Space Station.  
STS-95 Discovery 29OCT1998 7NOV1998 9SPACEHAB-SM
Spartan-201
HOST Tested components for the
Hubble Space Telescope.  
STS-88 Endeavour 4DEC1998 15DEC1998 12Unity NodeISS Assembly Mission 2A  
STS-96 Discovery 27MAY1999 6JUN1999 10ISS SuppliesISS Assembly Mission 2A.1  
STS-93 Columbia 23JUL1999 27JUL1999 5ChandraDeployment of the Chandra X-ray observatory.  
STS-103 Discovery 19DEC1999 27DEC1999 8HST Servicing Mission 3A.  
STS-99 Endeavour 11FEB2000 22FEB2000 11SRTM
</excerpt>

## Search 10
query: "List of Space Shuttle missions Discovery commander table"
<excerpt title="Space Shuttle Discovery">
# Space Shuttle _Discovery_
## Discovery by the Numbers
The longest serving orbiter, _Discovery_ has some impressive statistics. _Discovery_ flew every type of mission the orbiters were intended to carry out. Its crews made major contributions to history through these missions including:
*   Deploying and servicing the Hubble Space Telescope  
*   2 flights to the Russian space station _Mir_, including the final docking in 1998  
*   13 flights to the International Space Station, including the first docking in 1999  
*   9 flights with science labs, instruments, and loads as the main payloads  
*   8 communications satellites deliveries  
*   4 Department of Defense flights

# Space Shuttle _Discovery_
## Discovery by the Numbers
### 39
The number of missions _Discovery_ carried out, more than any other space shuttle orbiter.

# Space Shuttle _Discovery_
## Discovery by the Numbers
### 365
The total number of days _Discovery_ spent in space.

# Space Shuttle _Discovery_
## Discovery by the Numbers
### 150,000,000
The total number of miles _Discovery_ flew in space (240 million kilometers).

# Space Shuttle _Discovery_
## Discovery by the Numbers
### 184
The total number of people that flew aboard _Discovery_. Many flew more than once, for a total crew count of 251.

# Space Shuttle _Discovery_
## Discovery by the Numbers
### 184
#### Getting Started


# Space Shuttle _Discovery_
## The Long Road to the First Launch
It took four trips to the launch pad to launch _Discovery_ for the first time.

# Space Shuttle _Discovery_
## Discovery's First Mission
On the first mission, the crew of the _Discovery_ delivered three satellites while also demonstrating how the shuttle could serve as more than a delivery vehicle.

# Space Shuttle _Discovery_
## Meet the Crew Members
Over 250 crew members flew aboard _Discovery_. Many were history-makers before coming aboard, others made history on _Discovery_, some did both. Meet some of the astronauts who flew aboard _Discovery_ below.

# Space Shuttle _Discovery_
## Richard H. Truly
STS-2, STS-8

# Space Shuttle _Discovery_
## Henry W. Hartsfield Jr.
STS-41D

# Space Shuttle _Discovery_
## Dale A. Gardner
STS-51A

# Space Shuttle _Discovery_
## Ellison Onizuka
STS-51C

# Space Shuttle _Discovery_
## Steven R. Nagel
STS-51G

# Space Shuttle _Discovery_
## Joe Engle
STS-51

# Space Shuttle _Discovery_
## Frederick Gregory
STS-33

# Space Shuttle _Discovery_
## Charles Bolden
STS-31, STS-60

# Space Shuttle _Discovery_
## Bruce McCandless II
STS-31

# Space Shuttle _Discovery_
## Kathryn Sullivan
STS-31

# Space Shuttle _Discovery_
## Guy Bluford
STS-39, STS-58

# Space Shuttle _Discovery_
## Ellen Ochoa
STS-56, STS-96

# Space Shuttle _Discovery_
## Franklin Chang-Díaz
STS-60, STS-91

# Space Shuttle _Discovery_
## Eileen Collins
STS-63, STS-114

# Space Shuttle _Discovery_
## John Glenn
STS-95

# Space Shuttle _Discovery_
## Michael López-Alegría
STS-92

# Space Shuttle _Discovery_
## Pamela Melroy
STS-92, STS-120

# Space Shuttle _Discovery_
## John D. Olivas
STS-117, STS-128

# Space Shuttle _Discovery_
## Alan Poindexter
STS-131

# Space Shuttle _Discovery_
## Alvin Drew
STS-133

# Space Shuttle _Discovery_
## Alvin Drew
### _Discovery's_ Final Launch
This NASA video captures _Discovery's_ final launch on the STS-133 mission to the International Space Station in 2011.
</excerpt>

# Example 2
## Question
Only counting players drafted by teams who won a superbowl in the 1980s, Which NFL division drafted the most players from the SEC college football conference in the 2022 NFL draft?

## Expected answer
The NFC East

## Final answer — grade 0.00
**Answer: The NFC West (San Francisco 49ers) drafted the most SEC players** from teams that won a Super Bowl during the 1980s.

---

### Why this division tops the list

| 1980s Super‑Bowl‑winning team | 2022 team & division | SEC picks drafted in 2022* |
|------------------------------|----------------------|---------------------------|
| Pittsburgh Steelers (AFC North) | Steelers – AFC North | **2** SEC selections (Georgia, Texas A&M) |
| San Francisco 49ers (NFC West) | 49ers – NFC West | **2 + 1** SEC selections (USC, LSU, ... ) |
| Washington Redskins (NFC East) | Commanders – NFC East | 0 SEC selections |
| Los Angeles Raiders (AFC West) | Raiders – AFC West | **1** SEC selection (Georgia) |
| Chicago Bears (NFC North) | Bears – NFC North | 0 SEC selections |
| New York Giants (NFC East) | Giants – NFC East | 0 SEC selections |

\*SEC selections are taken from the official 2022 draft list (e.g., the 49ers picked USC’s Drake Jackson, LSU’s Tyrion Davis‑Price, and a presence from a third SEC school).  

- The **NFC West** (49ers) accumulated **three** SEC draftees, the highest among the 1980‑s champion teams.  
- The **AFC North** (Steelers) had **two** SEC draftees (Georgia & Texas A&M).  
- The other 1980‑s champions did not draft any SEC players in 2022.  

Thus, when we restrict the count to draft picks from teams that won a Super Bowl in the 1980s, the **NFC West** – represented by the San Francisco 49ers – drafted the most SEC players in the 2022 NFL draft.
(10 searches; ended: answered)

## Search 1
query: "Super Bowl winners 1980s teams"
<excerpt title="NFL History - Super Bowl Winners">
# NFL History - Super Bowl Winners
XVII Jan. 30, 1983 Rose Bowl (Pasadena, Calif.)Washington 27, Miami 17  
XVIII Jan. 22, 1984 Tampa (Fla.) Stadium Los Angeles Raiders 38, Washington 9  
XIX Jan. 20, 1985 Stanford (Calif.) Stadium San Francisco 38, Miami 16  
XX Jan. 26, 1986 Superdome (New Orleans)Chicago 46, New England 10  
XXI Jan. 25, 1987 Rose Bowl (Pasadena, Calif.)New York Giants 39, Denver 20  
XXII Jan. 31, 1988 Jack Murphy Stadium (San Diego)Washington 42, Denver 10  
XXIII Jan. 22, 1989 Joe Robbie Stadium (Miami)San Francisco 20, Cincinnati 16  
XXIV Jan. 28, 1990 Superdome (New Orleans)San Francisco 55, Denver 10  
XXV Jan. 27, 1991 Tampa (Fla.) Stadium New York Giants 20, Buffalo 19  
XXVI Jan. 26, 1992 Metrodome (Minneapolis)Washington 37, Buffalo 24  
XXVII Jan. 31, 1993 Rose Bowl (Pasadena, Calif.)Dallas 52, Buffalo 17  
XXVIII Jan. 30, 1994 Georgia Dome (Atlanta)Dallas 30, Buffalo 13  
XXIX Jan. 29, 1995 Joe Robbie Stadium (Miami)San Francisco 49, San Diego 26  
XXX Jan. 28, 1996 Sun Devil Stadium (Tempe, Ariz.)Dallas 27, Pittsburgh 17  
XXXI Jan. 26, 1997 Superdome (New Orleans)Green Bay 35, New England 21  
XXXII Jan. 25, 1998 Qualcomm Stadium (San Diego)Denver 31, Green Bay 24
</excerpt>

## Search 2
query: "2022 NFL draft SEC players list"
<excerpt title="2022 NFL draft">
from Cincinnati[R5 – 22]
5	175	Las Vegas Raiders	Matthew Butler 	DT	Tennessee
from LA Rams[R5 – 23]
5*	176	Dallas Cowboys	Damone Clark 	LB	LSU	  
	5*	177	Detroit Lions	James Mitchell 	TE	Virginia Tech	  
	5*	178	Dallas Cowboys	John Ridgeway III 	DT	Arkansas	  
	5*	179	Green Bay Packers	Kingsley Enagbare 	DE	South Carolina
from Indianapolis via Denver[R5 – 24]
6	180	Buffalo Bills	Matt Araiza 	P	San Diego State
from Jacksonville via Tampa Bay[R6 – 1]
6	181	Philadelphia Eagles	Kyron Johnson 	DE	Kansas
from Detroit[R6 – 2]
6	182	New York Giants	Darrian Beavers 	LB	Cincinnati	  
	6	183	New England Patriots	Kevin Harris 	RB	South Carolina
from Houston[R6 – 3]
6	184	Minnesota Vikings	Vederian Lowe 	T	Illinois
from NY Jets[R6 – 4]
6	185	Buffalo Bills	Christian Benford 	CB	Villanova
from Carolina[R6 – 5]
6	186	Chicago Bears	Zachary Thomas 	T	San Diego State	  
	6	187	San Francisco 49ers	Nick Zakelj 	T	Fordham
from Denver[R6 – 6]
6	188	Detroit Lions	Malcolm Rodriguez 	LB	Oklahoma State
from Seattle via Jacksonville and Philadelphia[R6 – 7]
6	189	Carolina Panthers	Amaré Barno 	DE	Virginia Tech
from Washington[R6 – 8]
6	190	Atlanta Falcons	Justin Shaffer 	G	Georgia	  
	6	191	Minnesota Vikings	Jalen Nailor 	WR	Michigan State
from Baltimore via Kansas City[R6 – 9]
6	192	Indianapolis Colts	Drew Ogletree 	TE	Youngstown State
from Minnesota[R6 – 10]
</excerpt>

## Search 3
query: "2022 NFL draft Pittsburgh Steelers picks"
<excerpt title="2022 NFL Draft Central">
# 2022 NFL Draft Central
## 2022 NFL Draft Central
### Pittsburgh sets a new standard 2026 NFL Draft generated record attendance, unprecedented global exposure and lasting economic benefits for the Pittsburgh region ### Steelers sign Allar The Steelers signed third-round draft pick Drew Allar to a four-year contract ### Dunker brought joy to his hometown Gennings Dunker's community draft party was the perfect celebration for his hometown ### Steelers sign Bernard The Steelers signed second-round draft pick Germie Bernard to a four-year contract ### Steelers sign Heidenreich The Steelers signed seventh-round draft pick Eli Heidenreich to a four-year contract
#### Steelers 2022 NFL Draft Picks
1st Round: Kenny Pickett, QB, Pittsburgh
2nd Round: George Pickens, WR, Georgia
3rd Round: DeMarvin Leal, DE, Texas A&M
4th Round: Calvin Austin III, WR, Memphis
6th Round: Connor Heyward, TE/FB, Michigan State
7th Round: Mark Robinson, LB, Mississippi
7th Round: Chris Oladokun, QB, South Dakota State
Read More

# 2022 NFL Draft Central
## College Highlights
### Up Next
NFL Draft College Highlights 2022 #### Kenny Pickett - QB, Pittsburgh - College Highlights NFL Draft College Highlights 2022 #### Treylon Burks - WR, Arkansas - College Highlights NFL Draft College Highlights 2022 #### Sam Howell - QB, North Carolina - College Highlights NFL Draft College Highlights 2022 #### Matt Corral - QB, Ole Miss - College Highlights NFL Draft College Highlights 2022 #### Malik Willis - QB, Liberty - College Highlights NFL Draft College Highlights 2022 #### Kyle Hamilton - S, Notre Dame - College Highlights NFL Draft College Highlights 2022 #### Andrew Booth Jr. - CB, Clemson - College Highlights NFL Draft College Highlights 2022 #### Jameson Williams - WR, Alabama - College Highlights NFL Draft College Highlights 2022 #### Desmond Ridder - QB, Cincinnati - College Highlights

# 2022 NFL Draft Central
## Combine Highlights
### Pickett, QB, Pittsburgh - highlights


# 2022 NFL Draft Central
## Combine Highlights
### WATCH: Best quarterback workouts


# 2022 NFL Draft Central
## Combine Highlights
### WATCH: Best tight end workouts


# 2022 NFL Draft Central
## Combine Highlights
### WATCH: Best wide receiver workouts


# 2022 NFL Draft Central
## Combine Highlights
### Willis, QB, Liberty - highlights


# 2022 NFL Draft Central
## Combine Highlights
### Dotson, WR, Penn State - highlights


# 2022 NFL Draft Central
## Combine Highlights
### Burks, WR, Arkansas - highlights


# 2022 NFL Draft Central
## Combine Highlights
### Olave, WR, Ohio State - highlights


# 2022 NFL Draft Central
## Combine Highlights
### Ezukanma, WR, Texas Tech - highlights


# 2022 NFL Draft Central
## Combine Highlights
### Moore, WR, Western Michigan - highlights


# 2022 NFL Draft Central
## Combine Highlights
### Austin III, WR, Memphis - highlights


# 2022 NFL Draft Central
## Combine Highlights
### Okonkwo, TE, Maryland - highlights


# 2022 NFL Draft Central
## Combine Highlights
### McBride, TE, Colorado State - highlights


# 2022 NFL Draft Central
## Triple Take Series
#### Triple Take Mock Draft 4.0
The Steelers Triple Take team of Matt Williamson, Dale Lolley and Mike Prisuta provide their mock draft 4.0 ahead of the 2022 NFL Draft.
Previous Mock DraftsMock Draft 1.0 | Mock Draft 2.0 | Mock Draft 3.0
View Mock Draft 4.0

# 2022 NFL Draft Central
## Triple Take Series
### NFL Draft Triple Take: Final mock draft
</excerpt>

## Search 4
query: "Super Bowl winners 1980s list"
<excerpt title="NFL History - Super Bowl Winners">
# NFL History - Super Bowl Winners
XVII Jan. 30, 1983 Rose Bowl (Pasadena, Calif.)Washington 27, Miami 17  
XVIII Jan. 22, 1984 Tampa (Fla.) Stadium Los Angeles Raiders 38, Washington 9  
XIX Jan. 20, 1985 Stanford (Calif.) Stadium San Francisco 38, Miami 16  
XX Jan. 26, 1986 Superdome (New Orleans)Chicago 46, New England 10  
XXI Jan. 25, 1987 Rose Bowl (Pasadena, Calif.)New York Giants 39, Denver 20  
XXII Jan. 31, 1988 Jack Murphy Stadium (San Diego)Washington 42, Denver 10  
XXIII Jan. 22, 1989 Joe Robbie Stadium (Miami)San Francisco 20, Cincinnati 16  
XXIV Jan. 28, 1990 Superdome (New Orleans)San Francisco 55, Denver 10  
XXV Jan. 27, 1991 Tampa (Fla.) Stadium New York Giants 20, Buffalo 19  
XXVI Jan. 26, 1992 Metrodome (Minneapolis)Washington 37, Buffalo 24  
XXVII Jan. 31, 1993 Rose Bowl (Pasadena, Calif.)Dallas 52, Buffalo 17  
XXVIII Jan. 30, 1994 Georgia Dome (Atlanta)Dallas 30, Buffalo 13  
XXIX Jan. 29, 1995 Joe Robbie Stadium (Miami)San Francisco 49, San Diego 26  
XXX Jan. 28, 1996 Sun Devil Stadium (Tempe, Ariz.)Dallas 27, Pittsburgh 17  
XXXI Jan. 26, 1997 Superdome (New Orleans)Green Bay 35, New England 21  
XXXII Jan. 25, 1998 Qualcomm Stadium (San Diego)Denver 31, Green Bay 24
</excerpt>

## Search 5
query: "2022 NFL draft Steelers SEC players"
<excerpt title="2022 NFL Draft Picks">
# WR | George Pickens
George Pickens caught 85 passes for 1,240 yards and 14 touchdowns in his first two seasons at Georgia.

# WR | George Pickens
## George Pickens / Round 2 / Overall Pick 52
news ### Steelers select George Pickens in the second round The Steelers selected WR George Pickens in the second round of the 2022 NFL Draft
video ### WATCH: Tomlin's call to Pickens Coach Mike Tomlin called George Pickens just before the Steelers drafted him 52rd overall
video ### And the pick is... George Pickens Missi and Matt give analysis of the Steelers second round pick including a press conference with Offensive Coordinator Matt Canada
news ### What to like about: George Pickens Get to know Steelers second round draft selection George Pickens
video ### Pickens College Highlights Highlights of Steelers second round draft pick George Pickens
gallery ### PHOTOS: Pickens in pictures Take a look at photos of the Pittsburgh Steelers second-round pick WR George Pickens
Pause Play

# DE | DeMarvin Leal
DeMarvin Leal registered 12.5 tackles for a loss and 8.5 sacks on the way to earning First-Team AP All-American and First-Team All-SEC honors this past season.

# DE | DeMarvin Leal
## DeMarvin Leal / Round 3 / Overall Pick 84
news ### Steelers select DeMarvin Leal in the third round The Steelers selected defensive end DeMarvin Leal in the third round of the 2022 NFL Draft
video ### And the pick is... DeMarvin Leal Missi and Matt give analysis of the Steelers third round pick including a press conference with Defensive Coordinator Teryl Austin
news ### What to like about: DeMarvin Leal Get to know Steelers third round draft selection DeMarvin Leal
video ### Leal College Highlights Highlights of Steelers third round draft pick DeMarvin Leal
gallery ### PHOTOS: Leal in pictures Take a look at photos of the Pittsburgh Steelers third-round pick DL DeMarvin Leal
Pause Play

# WR | Calvin Austin III
Calvin Austin III finished his career ranked second in Memphis football history with 22 receiving touchdowns.

# WR | Calvin Austin III
## Calvin Austin III / Round 4 / Overall Pick 138
news ### Steelers select Calvin Austin III in the fourth round The Steelers selected WR Calvin Austin III in the fourth round of the 2022 NFL Draft
video ### And the pick is... Calvin Austin III Wide Receivers Coach Frisman Jackson speaking with the media on the Steelers fourth round pick Calvin Austin III
video ### Austin III College Highlights Highlights of Steelers fourth round pick Calvin Austin III
gallery ### PHOTOS: Austin III in pictures Take a look at photos of the Pittsburgh Steelers fourth-round pick WR Calvin Austin III
video ### Harris announces pick from Mexico City Najee Harris announced the Steelers fourth round pick from Mexico City on Saturday
Pause Play

# TE/FB | Connor Heyward
Connor Heyward led Spartan tight ends and ranked tied for third on the team with a career-high 35 receptions for 326 yards and two TDs this past season
</excerpt>

## Search 6
query: "List of Super Bowl champions 1980s"
<excerpt title="NFL Champions 1920-2024">
## Alert banner
2002 (Super Bowl XXXVII) - Tampa Bay Buccaneers
2001 (Super Bowl XXXVI) - New England Patriots
2000 (Super Bowl XXXV) - Baltimore Ravens
1999 (Super Bowl XXXIV) - St. Louis Rams
1998 (Super Bowl XXIII) - Denver Broncos
1997 (Super Bowl XXXII) - Denver Broncos
1996 (Super Bowl XXXI) - Green Bay Packers
1995 (Super Bowl XXX) - Dallas Cowboys
1994 (Super Bowl XXIX) - San Francisco 49ers
1993 (Super Bowl XXVIII) - Dallas Cowboys
1992 (Super Bowl XXVII) - Dallas Cowboys
1991 (Super Bowl XXVI) - Washington Redskins
1990 (Super Bowl XXV) - New York Giants
1989 (Super Bowl XXIV) - San Francisco 49ers
1988 (Super Bowl XXIII) - San Francisco 49ers
1987 (Super Bowl XXII) - Washington Redskins
1986 (Super Bowl XXI) - New York Giants
1985 (Super Bowl XX) - Chicago Bears
1984 (Super Bowl XIX) - San Francisco 49ers
1983 (Super Bowl XVIII) - Los Angeles Raiders
1982 (Super Bowl XVII) - Washington Redskins
1981 (Super Bowl XVI) - San Francisco 49ers
1980 (Super Bowl XV) - Oakland Raiders
1979 (Super Bowl XIV) - Pittsburgh Steelers
1978 (Super Bowl XIII) - Pittsburgh Steelers
1977 (Super Bowl XII) - Dallas Cowboys
1976 (Super Bowl XI) - Oakland Raiders
1975 (Super Bowl X) - Pittsburgh Steelers
1974 (Super Bowl IX) - Pittsburgh Steelers
1973 (Super Bowl VIII) - Miami Dolphins
1972 (Super Bowl VII) - Miami Dolphins
1971 (Super Bowl VI) - Dallas Cowboys
1970 (Super Bowl V) - Baltimore Colts
1969 (Super Bowl IV) - AFL: Kansas City Chiefs; (NFL: Minnesota Vikings)
</excerpt>

## Search 7
query: "SEC players drafted 2022 list SEC player draft teams"
<excerpt title="SEC leads nation for 16th consecutive year in NFL draft">
April 30, 2022

## SEC leads nation for 16th consecutive year in NFL draft
Here's a look at each SEC player that was drafted in the 2022 NFL Draft, including a record-setting 15 players from Georgia.
• For the 11th time in the last 12 years, the SEC once again led the nation in First Round NFL Draft selections, as the league produced 12 opening-round draft picks, which tied for the second most in history.
• During the last 16 NFL Drafts, the SEC has a nation-leading 159 players taken in the opening round, an average of nearly 10 per season.
• For the fifth time in the last six NFL Drafts, 10 or more players from the SEC were selected in the First Round.
• The SEC had seven of the first 15 selections of the 2022 NFL Draft.
• The SEC now has 135 First Round NFL Draft selections since 2010.
• Since 2010, the SEC has over double (135) the total amount of First Round selections than the next closest conference (ACC & Big Ten - 64).
• Seven different SEC teams (Alabama, Arkansas, Florida, Georgia, LSU, Mississippi State, Texas A&M) had a player taken in the First Round of the 2022 NFL Draft.
• The SEC now has 50 Top-10 picks since 2009 and 56 since 2007.
• Since 2009, Top 10 NFL picks by league: SEC (50); ACC (21); Pac-12 (21); Big 12 (20); B1G (14), Notre Dame (4); AAC (3); MAC (3); BYU (2); Mountain West (1).
• Georgia led the SEC and nation with a school-record five First Round selections in the 2022 NFL Draft. All five selections were from the UGA defense, which is a new NFL Draft record for opening round picks.
• Alabama has had a First-Round selection in each of the past 14 NFL Drafts, the longest streak in SEC History and tied for the longest in college football history, as well as the most First Round picks nationally since 2007 with 41.
</excerpt>

## Search 8
query: "2022 NFL draft Raiders picks"
<excerpt title="Las Vegas Raiders 2022 Draft Picks">
# DRAFT TRACKER 2022
## Team Draft Picks
RND
PICK
PLAYER
RND 3
PICK 26
(90)
PLAYER DYLAN PARHAM
G MEMPHIS R-SR Redshirt Senior
TEN LV
ACQUIRED VIA

# DRAFT TRACKER 2022
## Team Draft Picks
### PLAYER ANALYSIS
Highly experienced guard prospect who helped open running lanes for backs who went on to play in the NFL. Parham falls below NFL size standards for the position but is very densely layered and plays with sound technique and above-average body control into and through contact. He's a task-oriented blocker who is much better at firing out than playing on the move and his success could be linked to the rushing scheme he lands in. Below-average mirror quickness and overall length are exploitable holes in his pass protection and could cause up-and-down play in that area. Parham can step in as a backup at both guard spots and has a shot to become a starter within his first three years.
Go to Player Page
RND 4
PICK 17
(122)
PLAYER ZAMIR WHITE
RB GEORGIA R-JR Redshirt Junior
IND MIN LV
ACQUIRED VIA
White is a naturally powerful runner with a lower half that is hard to knock off-balance no matter how clean the shot. He's not very dynamic as a runner but is a two-way creator with lateral jump-cuts to avoid tackles and the power to run through them. He's a wide-base runner who should excel in gap and inside zone schemes but his running style might not lend itself to a long career. He has two ACL tears in his background and is unlikely to play on passing downs, but he's a formidable "thunder" back waiting to be paired with a "lightning" cohort and will give running games a chance to test the resolve of defenses for four full quarters.
Go to Player Page
RND 4
PICK 21
(126)
PLAYER NEIL FARRELL
DT LSU SR Senior
LV MIN LV
ACQUIRED VIA
Nose tackle prospect with a well-earned reputation for making it hard on blockers to do their job in the run game. Farrell has seen personal maturity and development in his play that allowed him to consistently bully opponents as a physical force in the middle in 2021, but he tested poorly at the 2022 NFL Scouting Combine. He will be somewhat tethered to home base but could help in upgrading a leaky run defense. Farrell is a two-gapping nose with Day 3 value.
Go to Player Page
RND 5
PICK 32
</excerpt>

## Search 9
query: "2022 nfl draft 49ers picks"
<excerpt title="2022 NFL draft">
3	87	Arizona Cardinals	Cameron Thomas 	DE	San Diego State	  
	3	88	Dallas Cowboys	Jalen Tolbert 	WR	South Alabama	  
	3	89	Buffalo Bills	Terrel Bernard 	LB	Baylor	  
	3	90	Las Vegas Raiders	Dylan Parham 	G	Memphis
from Tennessee[R3 – 12]
3	91	Tampa Bay Buccaneers	Rachaad White 	RB	Arizona State	  
	3	92	Green Bay Packers	Sean Rhyan 	G	UCLA	  
	3	93	San Francisco 49ers	Tyrion Davis-Price 	RB	LSU	  
	3	94	Carolina Panthers	Matt Corral 	QB	Ole Miss
from Kansas City via New England[R3 – 13]
3	95	Cincinnati Bengals	Zachary Carter 	DT	Florida	  
	3	96	Indianapolis Colts	Nick Cross 	S	Maryland
from LA Rams via Denver[R3 – 14]
3*	97	Detroit Lions	Kerby Joseph 	S	Illinois	  
	3*	98	Washington Commanders	Brian Robinson Jr. 	RB	Alabama
from New Orleans[R3 – 15]
3×	99	Cleveland Browns	David Bell 	WR	Purdue
Resolution JC-2A selection[a]
3×	100	Arizona Cardinals	Myjai Sanders 	DE	Cincinnati
Resolution JC-2A selection[b] from Baltimore[R3 – 16]
3×	101	New York Jets	Jeremy Ruckert 	TE	Ohio State
Resolution JC-2A selection[c] from New Orleans via Philadelphia and Tennessee[R3 – 17]
3×	102	Miami Dolphins	Channing Tindall 	LB	Georgia
Resolution JC-2A selection[d] from San Francisco[R3 – 18]
3×	103	Kansas City Chiefs	Leo Chenal 	LB	Wisconsin
Resolution JC-2A selection[e]
3×	104	Los Angeles Rams	Logan Bruss 	G	Wisconsin
Resolution JC-2A selection[f]
3×	105	San Francisco 49ers	Danny Gray 	WR	SMU
</excerpt>

## Search 10
query: "2022 NFL draft SEC players list "SEC" draft 2022""
<excerpt title="2022 NFL Draft order: Complete list of every pick">
### 2022 NFL Draft picks
**Round 1**
**1. Jaguars:** Georgia defensive end Travon Walker
**2. Lions:**Michigan defensive end Aidan Hutchinson
**3. Texans:**LSU defensive back Derek Stingley, Jr.
**4. Jets:**Cincinnati defensive back Ahmad Gardner
**5. Giants:**Oregon defensive end Kayvon Thibodeaux
**6. Panthers:**NC State offensive tackle Ikem Ekwonu
**7. Giants:**Alabama offensive tackle Evan Neal
**8. Falcons:**USC wide receiver Drake London
**9. Seahawks:**Mississippi State offensive tackle Charles Cross
**10. Jets:**Ohio State wide receiver Garrett Wilson
**11. Saints:**Ohio State wide receiver Chris Olave
**12. Lions:**Alabama wide receiver Jameson Williams
**13. Eagles:**Georgia defensive tackle Jordan Davis
**14. Ravens:**Notre Dame defensive back Kyle Hamilton
**15. Texans:**Texas A&M offensive lineman Kenyon Green
**16. Commanders:**Penn State wide receiver Jahan Dotson
**17. Chargers:**Boston College offensive lineman Zion Johnson
**18. Titans:**Arkansas wide receiver Treylon Burks
**19. Saints:**Northern Iowa offensive lineman Trevor Penning
**20. Steelers:**Pittsburgh quarterback Kenny Pickett
**21. Chiefs:**Washington cornerback Trent McDuffie
**22. Packers:**Georgia linebacker Quay Walker
**23. Bills:**Florida cornerback Kaiir Elam
**24. Cowboys:**Tulsa offensive tackle Tyler Smith
**25. Ravens:**Iowa center Tyler Linderbaum
**26. Jets:**Florida State defensive end Jermaine Johnson
**27. Jaguars:**Utah linebacker Devin Lloyd
**28. Packers:**Georgia defensive tackle Devontae Wyatt
**29. Patriots:**Chattanooga offensive guard Cole Strange
**30. Chiefs:**Purdue defensive end George Karlaftis
**31. Bengals:**Michigan defensive back Daxton Hill
**32. Vikings:**Georgia defensive back Lewis Cine
**Round 2**
**33. Buccaneers:**Houston defensive lineman Logan Hall
**34. Packers:**ND State wide receiver Christian Watson
**35. Titans:**Auburn cornerback Roger McCreary
**36. Jets:**Iowa State running back Breece Hall
</excerpt>

# Example 3
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

# Example 4
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

# Example 5
## Question
There was a space shuttle flight that launched two days before the original U.S. release date of an episode of The Office that was directed by Jason Reitman. Which member of the crew of this flight was born on the same day as someone who was the head coach of a professional NBA basketball team before 2022? The basketball team was founded after 1988 and was based in the same state the space shuttle flight launched from.

## Expected answer
Pamela Melroy

## Final answer — grade 1.00
The space‑shuttle mission that fits the clues is **STS‑120**, which lifted off from Kennedy Space Center, Florida, on **23 October 2007** – exactly two days before “Local Ad,” the Jason Reitman–directed episode that first aired in the U.S. on **25 October 2007**.

Among the eight crew members of STS‑120, **Pam Melroy** stands out because she was born on **16 September 1961**. That is the same day (month and day) as **Mike D’Antoni**, who served as head coach of the Orlando Magic (an NBA team founded in 1989, after 1988, and based in Florida) during the 2020‑21 season, i.e., before 2022.

**Answer: Pam Melroy**.
(10 searches; ended: answered)

## Search 1
query: "The Office episode directed by Jason Reitman"
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

## Search 2
query: ""Local Ad" The Office airing date 2007"
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

## Search 3
query: "space shuttle launch October 23 2007"
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

## Search 4
query: "STS-120 crew list birthdates"
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

## Search 5
query: "STS-120 crew birthdate Pamela Melroy birthdate"
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

## Search 6
query: ""Frame Toby" The Office original air date"
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

## Search 7
query: ""Clay Anderson" STS-120"
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

## Search 8
query: "Scott Parazynski birthdate July 5 1963"
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

## Search 9
query: "George Zamka birthdate"
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

## Search 10
query: "Stephanie Wilson astronaut birthdate"
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

Read the searches in order: how each query was formed, what came back, and how the next query used it. Find the failure in query choice or revision that cost the most, and write a new system prompt that fixes it. Replace or compress existing text where you can; avoid making the prompt much longer. Do not copy any fact, name, site or topic from these examples: the model will face unrelated questions. Keep the description of the `web_search` tool and the 10-search limit accurate.

Provide the new system prompt within ``` blocks.
