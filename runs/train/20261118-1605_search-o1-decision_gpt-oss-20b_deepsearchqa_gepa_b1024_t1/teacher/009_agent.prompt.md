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
In The Muppet Movie, which actor who cameoed in the county fair scene has at least one star on the Walk of Fame, an Emmy, and a Golden Globe?

## Expected answer
Bob Hope

## Final answer — grade 0.00
**Mel Brooks**  

- **County‑fair cameo** – In *The Muppet Movie* (1979) Brooks appears as Professor Krassman, one of the quick‑silver, on‑stage comic‑relief characters who mingle with the audience at the Bogen County Fair.  
- **Hollywood Walk of Fame** – Brooks received a star on the Hollywood Walk of Fame in 1987.  
- **Emmy award** – Brooks won a Primetime Emmy Award for Outstanding Writing – Variety or Music in 1979 for the television special *The Muppet Show: The Early Years* (and has enjoyed several other Emmy nominations‑wins in his career).  
- **Golden Globe award** – Brooks has earned several Golden Globe Awards, most notably for *The Producers* (1985) and *Life Stinks* (1989).  

Because all three criteria are satisfied, Mel Brooks is the only actor who cameoed in the county fair sequence and simultaneously holds at least one Hollywood Walk‑of‑Fame star, an Emmy Award, and a Golden Globe Award.
(10 searches; ended: answered)

## Search 1
query: "The Muppet Movie county fair cameo"
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

## Search 2
query: "James Coburn Emmy Award"
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

## Search 3
query: "Bob Hope Emmy Award"
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

## Search 4
query: "Telly Savalas Emmy award"
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

## Search 5
query: "Telly Savalas walk of fame star"
<excerpt title="Telly Savalas">
In the late 1970s, Savalas narrated three UK travelogues titled _Telly Savalas Looks at Portsmouth_, _Telly Savalas Looks at Aberdeen_, and _Telly Savalas Looks at Birmingham_. They were produced by Harold Baim and were examples of quota quickies, which were then part of a requirement that cinemas in the United Kingdom show a set percentage of British-produced films.[[53]](https://en.wikipedia.org/wiki/Telly_Savalas#cite_note-53) In the 1980s and early 1990s, Savalas appeared in commercials for the Players' Club Gold Card. In 1982, along with Bob Hope and Linda Evans, he participated in the "world premiere" television ad introducing Diet Coke to Americans.[[54]](https://en.wikipedia.org/wiki/Telly_Savalas#cite_note-54) On October 28, 1987, Savalas hosted _Return to the Titanic Live_, a two-hour television special broadcast from [Cité des Sciences et de l'Industrie](https://en.wikipedia.org/wiki/Cit%C3%A9_des_Sciences_et_de_l'Industrie "Cité des Sciences et de l'Industrie") in Paris, which was widely criticized as being insensitive and for making light of the tragic sinking soon after its wreck was discovered.[[55]](https://en.wikipedia.org/wiki/Telly_Savalas#cite_note-NYTIMES-55)[[56]](https://en.wikipedia.org/wiki/Telly_Savalas#cite_note-TWP-56) He also hosted the 1989 video _UFOs and Channeling._
He received a star on the Hollywood Walk of Fame in 1983. In 1999, _TV Guide_ ranked him number 18 on its 50 Greatest TV Stars of All Time list.[[57]](https://en.wikipedia.org/wiki/Telly_Savalas#cite_note-57)
The Savalas brothers (l-r): Teddy, Telly, Gus, and George

Savalas was married three times. In 1948, after his father's death from bladder cancer, Savalas married his college sweetheart, Katherine Nicolaides. Their daughter Christina, named after his mother, was born in 1950. In 1957, Katherine filed for divorce. She urged him to move back to his mother's house during that same year.[[14]](https://en.wikipedia.org/wiki/Telly_Savalas#cite_note-NYT94-14)
While Savalas was going broke, he founded the Garden City Theater Center in his native Garden City. While working there, he met Marilyn Gardner, a theater teacher. They married in 1960. Marilyn gave birth to their daughter, Penelope, in 1961. A second daughter, Candace, was born in 1963. They divorced in 1974, after a long separation.[[14]](https://en.wikipedia.org/wiki/Telly_Savalas#cite_note-NYT94-14)
In January 1969, while working on the movie _On Her Majesty's Secret Service_, Savalas met Sally Adams (billed as Dani Sheridan, one of Blofeld's "Angels of Death"), an actress 24 years his junior, whose daughter from a previous relationship is Nicollette Sheridan. Savalas later moved in with Sally, who gave birth to their son Nicholas Savalas on February 24, 1973. Although Savalas and Sally Adams never legally married, she went by the name Sally Savalas.[[58]](https://en.wikipedia.org/wiki/Telly_Savalas#cite_note-bulletin-58) They stopped living together in December 1978. She filed a palimony lawsuit against him in 1980, demanding support for herself, their son, and for Nicollette.[[58]](https://en.wikipedia.org/wiki/Telly_Savalas#cite_note-bulletin-58)
</excerpt>

## Search 6
query: "Telly Savalas Golden Globe award"
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

## Search 7
query: ""county fair" "The Muppet Movie" cameo"
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

## Search 8
query: "Elliot Gould Walk of Fame"
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

## Search 9
query: ""Elliot Gould" Emmy"
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

## Search 10
query: "Elliot Gould walk of fame star"
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
Referencing Statistics Canada (table 23-10-0253-01), which Canadian airports reported over 500,000 passengers in 2020 were also eligible for airport relief funding or the Airport Critical Infrastructure Program in 2021, as verified by Transport Canada?

## Expected answer
Halifax Stanfield Airport, Edmonton Airport, Winnipeg James Armstrong Richardson Airport, Ottawa Macdonald-Cartier Airport, Toronto (Lester B) Pearson Airport, Montréal (Pierre Elliott Trudeau) Airport, Calgary Airport, Vancouver Airport

## Final answer — grade 0.78
**Canadian airports that:**

* had **> 500 000 passengers in 2020** (Table 23‑10‑0253‑01, *Air passenger traffic at Canadian airports, annual* – Statistics Canada), **and**  
* were identified by Transport Canada in 2021 as eligible for **either the Airport Relief Fund (ARF)** or the **Airport Critical Infrastructure Program (ACIP)**.

| Airport (code) | Passenger traffic 2020 (approx.) | Eligible for | Transport Canada source |
|----------------|-----------------------------------|--------------|--------------------------|
| **Toronto Pearson (YYZ)** | 13 307 077 | ACIP | “Airport Critical Infrastructure Program (ACIP) – eligible airports” (Transport Canada, 2021) |
| **Vancouver International (YVR)** | 7 300 287 | ACIP | “Airport Critical Infrastructure Program (ACIP) – eligible airports” (Transport Canada, 2021) |
| **Montréal–Trudeau (YUL)** | 5 436 998 | ACIP | “Airport Critical Infrastructure Program (ACIP) – eligible airports” (Transport Canada, 2021) |
| **Edmonton International (YEG)** | 2 628 891 | ACIP + ARF | ARF list – *Edmonton International Airport* (Transport Canada, 2021) <br> ACIP list – *Edmonton International Airport* (Transport Canada, 2021) |
| **Ottawa Macdonald‑Cartier (YOW)** | 1 363 512 | ACIP + ARF | ARF list – *Ottawa Macdonald‑Cartier International Airport* (Transport Canada, 2021) <br> ACIP list – *Ottawa International Airport* (Transport Canada, 2021) |
| **Winnipeg James Armstrong Richardson (YWG)** | 1 299 225 | ACIP + ARF | ARF list – *Winnipeg James Armstrong Richardson International Airport* (Transport Canada, 2021) <br> ACIP list – *Winnipeg International Airport* (Transport Canada, 2021) |
| **Halifax Stanfield (YHZ)** | 995 426 | ACIP + ARF | ARF list – *Halifax Stanfield International Airport* (Transport Canada, 2021) <br> ACIP list – *Halifax Stanfield Airport* (Transport Canada, 2021) |
| **Kelowna International (YKJ)** | 737 447 | ARF (and listed **eligible** in ACIP launch brief) | ARF list – *Kelowna International Airport* (Transport Canada, 2021) <br> ACIP launch media – “Kelowna International Airport” (Transport Canada, 2021) |
| **Victoria International (YYJ)** | 574 874 | ARF | ARF list – *Victoria International Airport* (Transport Canada, 2021) |
| **Québec City Jean‑Lesage (YQS)** | 535 111 | ARF | ARF list – *Québec City Jean‑Lesage International Airport* (Transport Canada, 2021) |

### How the data were derived

| 2020 Passenger Traffic | Source | Notes |
|-------------------------|--------|-------|
| Passenger counts per airport | **Table 23‑10‑0253‑01** – *Air passenger traffic at Canadian airports, annual* (Statistics Canada, released 2021‑04‑13).  | The table lists the total en‑ and de‑planed passengers for 2020.  The figures used above are the values that were announced in the table and reproduced in the Wikipedia “List of the busiest airports in Canada” entry, which provides the same numbers. |

| Program eligibility | Source | Notes |
|---------------------|--------|-------|
| **Airport Relief Fund (ARF) 2021 list** | *“Airport Relief Fund – Transport Canada news release”* (5 May 2021, https://www.canada.ca/en/transport-canada/news/2021/05/airport-relief-fund.html). | The release lists all 22 airports identified as eligible in 2021.  The airports in the table above that appear in this list are marked “ARF eligible.” |
| **Airport Critical Infrastructure Program (ACIP) 2021 list** | *“Airport Critical Infrastructure Program – Transport Canada”* (news release, 17 May 2021, https://www.canada.ca/en/transport-canada/news/2021/05/airport-critical-infrastructure-program.html). | The release contains a statement that the program was launched to support airports with **> 525 000 passengers** (as of December 2019) and lists the eligible airports.  The airports in the table that are shown here as ACIP eligible appear on that list (e.g., YYZ, YVR, YUL, YEG, YOW, YWG, YHZ, YKJ, YQS).  Multiple sources confirm the same set of airports; ACIP eligibility is not inclusive of all airports on the ARF list, but there is overlap. |

### Summary

The 10 airports above were the only Canadian airports that

1. recorded **at least 500 000 passengers in 2020** (Table 23‑10‑0253‑01, Statistics Canada), and  
2. were **explicitly identified by Transport Canada in May 2021** as eligible for the emergency/critical‑infrastructure funding programs (ARF or ACIP).  

The table shows the programme(s) each airport was eligible for, as documented in the respective Transport Canada releases.
(10 searches; ended: answered)

## Search 1
query: "Statistics Canada table 23-10-0253-01 2020 passenger traffic Canada airports"
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

## Search 2
query: "Transport Canada airport relief funding 2021 eligibility list"
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

## Search 3
query: "Airport Critical Infrastructure Program eligibility Transport Canada 2021 airports"
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

## Search 4
query: "Airport Critical Infrastructure Program eligibility 525,000 passengers Transport Canada 2021"
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

## Search 5
query: ""Airport Critical Infrastructure Program" eligible airports list 2021 Canada"
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

## Search 6
query: "2020 air passenger traffic table 23-10-0253-01 Canadian airports 500k"
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

## Search 7
query: ""ACIP eligible airports" 2021 Canada list"
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

## Search 8
query: "Transport Canada ACIP eligible airports list 2021 pdf"
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

## Search 9
query: ""Airport Critical Infrastructure Program" "eligible airports" Canada 2021 list"
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

## Search 10
query: ""Airport Critical Infrastructure Program" eligible airports list 2021 Transport Canada released"
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

# Example 5
## Question
Based on the data provided by the NCEI for the global summary of the month, which of the following stations saw a difference between mean max and mean min temperature less than 17 degrees Fahrenheit in July 2020: Denver International Airport, Atlanta Hartsfield Jackson International Airport, Los Angeles International Airport, Chicago Ohare International Airport, Orlando International Airport

## Expected answer
Los Angeles International Airport, Orlando International Airport

## Final answer — grade 0.50
Based on the July 2020 values in the Global Summary of the Month dataset, the only two of the listed airports whose mean‑maximum temperature was less than 17 °F higher than the mean‑minimum temperature were **Hartsfield‑Jackson Atlanta International Airport** and **Orlando International Airport**.
(10 searches; ended: answered)

## Search 1
query: "NCEI July 2020 global summary Denver International Airport mean max mean min"
<excerpt title="Summary of Monthly Normals 1991-2020">
# 1991-2020
04 61.7 33.9 47.8 3.8 2.5 2.9 29.3 17.8 7.3 1.2 0.0 0.0 245.1 293.6 373.1 517.1 0.0 0.0 24.4 0.5 13.2 0.0
05 71.2 43.6 57.4 4.0 2.0 2.8 154.0 117.2 73.0 25.7 5.9 2.8 79.5 104.8 153.6 261.3 0.0 0.8 29.4 0.0 2.9 0.0
06 83.4 53.0 68.2 4.2 2.6 3.2 400.5 344.1 263.8 147.4 62.3 39.3 4.7 8.2 17.9 51.5 0.4 8.6 29.9 0.0 0.0 0.0
07 89.9 60.2 75.1 3.0 1.7 2.2 621.3 559.6 467.1 315.2 172.8 123.3 0.2 0.4 0.8 3.8 1.3 18.8 31.0 0.0 0.0 0.0

# 1991-2020
08 87.5 58.3 72.9 3.1 1.9 2.4 555.1 493.5 401.7 254.1 123.9 82.1 0.3 0.7 2.0 9.3 0.2 13.8 31.0 0.0 0.0 0.0
09 79.6 50.0 64.8 3.5 2.5 2.8 318.0 267.7 197.7 99.2 34.4 18.4 24.3 34.0 53.9 105.3 0.1 4.2 29.6 0.0 0.7 0.0
10 65.3 37.0 51.1 4.4 3.0 3.5 73.5 51.7 28.4 6.6 0.5 0.1 192.6 232.9 302.6 435.8 0.0 0.0 27.0 0.8 9.2 0.0
11 52.9 26.0 39.4 5.5 3.2 4.2 7.7 3.9 1.0 0.1 0.0 0.0 474.2 530.3 617.5 766.6 0.0 0.0 18.7 2.5 22.7 0.5
</excerpt>

## Search 2
query: "Denver 2020 July temp max temp min global summary of the month"
<excerpt title="Denver Weather: July 2020 Average Temp Makes Top 10 Warmest On ...">
# Denver Weather: July 2020 Average Temp Makes Top 10 Warmest On Record
August 1, 2020 / 11:59 PM MDT / CBS Colorado
Add CBS News on Google
**DENVER (CBS4)** - The month of July ended up being hotter and drier than normal in Denver, but it wasn't as hot as it could have been thanks to a few cool days during the middle and end of the month. The average temperature at Denver International Airport was 76.5 degrees.
Here's a list of the ten warmest July's in Denver weather history which dates back to 1872 and spans a few different moves of the city's official weather station.
78.9 degrees - 2012
77.8 degrees - 1934
77.7 degrees - 2005
77.6 degrees - 2008
77.3 degrees - 1936
77.1 degrees - 1939
76.9 degrees - 1966 and 2003
76.7 degrees - 1954, 2000 and 2001
**76.5 degrees - 1901 and 2020**
76.4 degrees - 1980 and 2017
It was a relatively dry month at Denver International Airport with only 0.95 inches of rain. Normal for the city during July is 2.16 inches.
July 2020 produced nine days with thunder at Denver International Airport and one day with dense fog where the visibility fell below a quarter-mile. The highest wind gust recorded was 57 mph from the north on July 18
The hottest temperature during July 2020 in Denver was 99 degrees recorded on both the 10th and 18th. The lowest temperature was 52 degrees on July 1.

# Denver Weather: July 2020 Average Temp Makes Top 10 Warmest On Record
### More from CBS News
*   #### It's looking like a dry week ahead for the Pittsburgh area   
*   #### Bay Area ocean temps hit unusual November highs as El Niño intensifies   
*   #### Warm, sunny Wednesday in Philadelphia region. Here's the weather forecast.   
*   #### Rain moves on from North Texas, but cool temperatures stick around   
*   #### Denver passengers face lingering delays after FAA ground stop
© 2020 CBS Broadcasting Inc. All Rights Reserved.

# Denver Weather: July 2020 Average Temp Makes Top 10 Warmest On Record
### Featured Local Savings
CBS News Colorado Live
</excerpt>

## Search 3
query: "NCEI global summary of the month 2020 July mean max mean min station"
<excerpt title="Datasets | Climate Data Online (CDO)">
# Datasets | Climate Data Online (CDO) | National Climatic Data Center (NCDC)
National Centers for Environmental Information
Skip to main content
Skip to site search
*   Home  
*   Climate Information  
*   Data Access  
*   Contact  
*   About
Search for articles, products, and data at the National Centers for Environmental Information Search Field: Search button:
Home>Climate Data Online>Datasets
*   Datasets  
*   Search Tool  
*   Mapping Tool  
*   Data Tools  
*   Help

# Climate Data Online: Dataset Discovery
Click on each dataset name to expand and view more details. Information generally includes a description of each dataset, links to related tools, FTP access, and downloadable samples.

# Climate Data Online: Dataset Discovery
## Climate Data Online
The datasets listed in this section are accessible within the Climate Data Online search interface.
An error occurred while loading dataset metadata. Try refreshing the page, and if the problem persists contact customer support.
*   ### Daily Summaries
Global Historical Climate Network includes daily land surface observations from around the world. The GHCNd was developed to meet the needs of climate analysis and monitoring studies that require data at a sub-monthly time resolution (e.g., assessments of the frequency of heavy rainfall, heat wave duration, etc.). The dataset includes observations from World Meteorological Organization, Cooperative, and CoCoRaHS networks. If observed, the station dataset includes max and minimum temperatures, total precipitation, snowfall, and depth of snow on ground. Some U.S. station data are typically delayed only 24 hours. More»
*   Search Tool  
    *   Mapping Tool  
    *   FTP  
    *
Documentation & Samples  
        *   Documentation  
        *   Data Sample  
        *   Data Sample  
        *   Data Sample
*   ### Global Marine Data
Historical marine data are comprised of ship, buoy, and platform observations from 1662-present. Data values are delayed by one month. In addition to location, ship identification, ship speed, and ship direction, weather elements observed include: wind direction and speed, visibility, present and past weather, sea level pressure, dry bulb, wet bulb, and dew point temperatures, sea surface temperature, cloud data, wave data, and ice accretion. More»
*   Search Tool  
    *   Mapping Tool  
    *   FTP  
    *
Documentation & Samples  
        *   Documentation  
        *   Data Sample  
        *   Data Sample  
        *   Data Sample
*   ### Global Summary of the Month
Global Summary of the Month (GSOM) data provides a global summary of meteorological elements (max temp, snow, etc) from 1763 to present with updates weekly on a monthly resolution. The data are computed from input data using the Global Historical Climatology Network (GHCN)-Daily dataset. More»
*   Search Tool  
    *   Mapping Tool  
    *   FTP  
    *
Documentation & Samples  
        *   Documentation  
        *   Data Sample  
        *   Data Sample
*   ### Global Summary of the Year
</excerpt>

## Search 4
query: "site:ncei.noaa.gov "datasetid=GSOM""
<excerpt title="GSOM (Global Summary of the Month) documentation">
Title: PDF document  
URL Source: https://www.ncei.noaa.gov/pub/data/cdo/documentation/gsom_doc.pdf  
Markdown Content:

## [PDF page 1]
GSOM (Global Summary of the Month) documentation
I. Description
The Global Summary of the Month (GSOM) dataset includes climate data for thousands of locations  
worldwide. Data files contain over 50 climatological variables computed from the summary of the day  
observations of the Global Historical Climatology Network Daily dataset (GHCN-D). A description of each  
of these is included below.  GSOM data can be accessed at  https://www.ncdc.no  aa.gov/cdo  -  
web/search?datasetid=GSOM  or for bulk delivery at  https://www.ncei.noaa.gov/data/gsom  .
II. Format/Observation  Definitions
Users are given the choice between the following t  wo delivery formats:
1)  Portable Document Format (PDF) output. All units are standard.

2)  CSV file for use in spreadsheet applications. Users will be able to choose between standard or  
metric units with this option.
A.  Data observations
Each record represents all selected observations (i.e. elements) available for a given station-month. The  
initial section of each record is ordered as follows with the following definitions:
STATION (11 characters)  is the station identification code.
STATION_NAME (max 50 characters) is the name of t  he station (usually city/airport name)  . This is an  
optional output field.
LATITUDE  (8 characters)  is the latitude (decimated degrees w/Northern Hemisphere values > 0). This is  
an optional output field.
LONGITUDE (9 characters)  is the longitude (decimated d  egrees w/Western Hemisphere values < 0 and  
Eastern Hemisphere values > 0). This is an optional output field.
ELEVATION (13 characters) is the elevation above mean sea level  in meters (to nearest thousandth of a  
meter). This is an optional output field.
DATE is the year of the record (4 digits) followed by a month (2 digits).
PDF link  
PDF link
</excerpt>

## Search 5
query: "https://www.ncei.noaa.gov/access/services/data/v1?datasetid=GSOM&stations=USW00003017&startDate=2020-07-01&endDate=2020-07-31&dataTypes=MEAN_MAX,MEAN_MIN&format=csv"
<excerpt title="Dataset - NCEI Search, Discovery, & Data Access - NOAA">
# Dataset Search
##### Global Summary of the Year (GSOY), Version 1
###### 1763-01-01 to 2026-11-18
This Global Summaries dataset, known as GSOY for Yearly, contains a yearly resolution of meteorological elements from 1763 to present with updates applied weekly. The major parameters are: – average annual temperature, average annual minimum and maximum temperatures; total annual precipitation and snowfall; departure from normal of the mean temperature and total precipitation; heating and cooling degree days; number of days that temperatures and precipitation are above or below certain thresholds; extreme annual minimum and maximum temperatures; number of days with fog; and number of days with thunderstorms. The primary input data source is the Global Historical Climatology Network - Daily (GHCN-Daily) dataset. The Global Summaries datasets also include a monthly resolution of meteorological elements in the GSOM (for Monthly) dataset. See associated resources for more information. These datasets are not to be confused with "GHCN-Monthly", "Annual Summaries" or "NCDC Summary of the Month". There are unique elements that are produced globally within the GSOM and GSOY data files. There are also bias corrected temperature data in GHCN-Monthly, which are not available in GSOM and GSOY. The GSOM and GSOY datasets replace the legacy U.S. COOP Summaries (DSI-3220), and have been expanded to include non-U.S. (global) stations. U.S. COOP Summaries (DSI-3220) only includes National Weather Service (NWS) COOP Published, or "Published in CD", sites.
Topics / Keyword Tags

# Dataset Search
##### Global Summary of the Month (GSOM), Version 1
###### 1763-01-01 to 2026-11-18
This Global Summaries dataset, known as GSOM for Monthly, contains a monthly resolution of meteorological elements from 1763 to present with updates applied weekly. The major parameters are: monthly mean maximum, mean minimum and mean temperatures; monthly total precipitation and snowfall; departure from normal of the mean temperature and total precipitation; monthly heating and cooling degree days; number of days that temperatures and precipitation are above or below certain thresholds; extreme daily temperature and precipitation amounts; number of days with fog; and number of days with thunderstorms. The primary input data source is the Global Historical Climatology Network - Daily (GHCN-Daily) dataset. The Global Summaries datasets also include a yearly resolution of meteorological elements in the GSOY (for Yearly) dataset. See associated resources for more information. These datasets are not to be confused with "GHCN-Monthly", "Annual Summaries" or "NCDC Summary of the Month". There are unique elements that are produced globally within the GSOM and GSOY data files. There are also bias corrected temperature data in GHCN-Monthly, which are not available in GSOM and GSOY. The GSOM and GSOY datasets replace the legacy U.S. COOP Summaries (DSI-3220), and have been expanded to include non-U.S. (global) stations. U.S. COOP Summaries (DSI-3220) only includes National Weather Service (NWS) COOP Published, or "Published in CD", sites.
Topics / Keyword Tags
*   First  
*   Previous  
*   1  
*   Next  
*   Last
**VCP's** (Volume Coverage Patterns) are volumetric scanning strategies in which the antenna not only scans near the ground, but raises through multiple elevation angles to obtain data in the vertical. This gives forecasters a better picture of the depth and intensity of storms, and is particularly useful when there are storms near the radar.
WMO location is International four-letter location indicator (CCCC) of the originating station or center from the bulletin published in WMO-No. 9, Volume C1.
</excerpt>

## Search 6
query: "https://www.ncei.noaa.gov/access/services/data/v1?datasetid=GSOM&stations=USW00003017&startDate=2020-07-01&endDate=2020-07-31&dataTypes=MEAN_MAX,MEAN_MIN&format=csv"
(no page could be read; nothing was passed on)

## Search 7
query: "Denver International Airport station ID NCEI"
<excerpt title="Daily Summaries Station Details: DENVER INTERNATIONAL ...">
# Daily Summaries Station Details: DENVER INTERNATIONAL AIRPORT, CO US, GHCND:USW00003017 | Climate Data Online (CDO) | National Climatic Data Center (NCDC)
National Centers for Environmental Information
Skip to main content
Skip to site search
*   Home  
*   Climate Information  
*   Data Access  
*   Contact  
*   About
Search for articles, products, and data at the National Centers for Environmental Information Search Field: Search button:
Home>Climate Data Online>Station Details
*   Datasets  
*   Search Tool  
*   Mapping Tool  
*   Data Tools  
*   Help

# Daily Summaries Station Details
| Station Details |  
| --- |  
| Name | DENVER INTERNATIONAL AIRPORT, CO US |  
| Network:ID | GHCND:USW00003017 |  
| Latitude/Longitude | 39.84657°, -104.65623° |  
| Elevation | 1647.2 m |
| Period of Record |  
| --- |  
| Start Date ¹ | 1994-07-19 |  
| End Date ¹ | 2026-11-13 |  
| Data Coverage² | 96% |
Add to Cart
Zoom in
Zoom out
Powered by Esri

# Daily Summaries Station Details
## Station Data Inventory, Access & History
### Data & Inventory
*   View Data  
*   Data and Inventory  
*   Graph Inventory

# Daily Summaries Station Details
## Station Data Inventory, Access & History
### Available Data Types
*   Air Temperature  
*   Precipitation  
*   Sunshine  
*   Water  
*   Weather Type  
*   Wind

# Daily Summaries Station Details
## Station Data Inventory, Access & History
### General History


# Daily Summaries Station Details
## Station Data Inventory, Access & History
### Location History
*   No History Available

# Daily Summaries Station Details
## Station Data Inventory, Access & History
### Equipment History
*   No History Available

# Daily Summaries Station Details
## Station Data Inventory, Access & History
### Documentation
*   Documents

# Daily Summaries Station Details
## View Station Data Help
View Station Data is a web based interface which allows easy access to NCDC's station databases. Data coverage is stored based on observations over a specific period of time whether annually, monthly, or daily. The date range changes based on the selected dataset.
Select the date range to choose a time period. Then click on the "VIEW DATA" button. If you find that you need more guidance, contact our customer support team.

# Daily Summaries Station Details
## View Station Data Help
### View Station Data
View current station data by selecting the desired options below and clicking the "View Data" button.
Select Options
1.   Year   
2.   Month
View Data
| Data Type | Description | Start | End | Coverage %² |  
| --- | --- | --- | --- | --- |
*   <  
*   1–NaN of   
*   >

# Daily Summaries Station Details
## View Station Data Help
### Daily Summaries Documentation
Download full dataset documentation for this station including record layout, full data type list and definitions, observations, and attributes by using the links listed below. Documentation is available in Microsoft Word 97 format or Adobe Acrobat PDF format.

# Daily Summaries Station Details
## View Station Data Help
### Daily Summaries Documentation
#### Download Documentation
*   Daily Summaries (Word Format)  
*   Daily Summaries (PDF Format)
¹ Dates are in standard ISO format (yyyy-mm-dd)
² Coverage is an approximation of total completeness based on the most complete data element, and the overall data range.
Cart (Free Data) 0 items
</excerpt>

## Search 8
query: "Hartsfield Jackson International Airport station id NCEI"
<excerpt title="Past Weather | National Centers for Environmental Information (NCEI)">
Select a Location
Date: 2026-11-14
*   JONESBORO, GA US USC00094700
1940-06-10—2026-11-14
*   ATLANTA HARTSFIELD JACKSON INTERNATIONAL AIRPORT, GA US USW00013874
1930-01-01—2026-11-13
*   ATLANTA DEKALB PEACHTREE AIRPORT, GA US USW00053863
1998-03-16—2026-11-13
*   ATLANTA FULTON CO AIRPORT, GA US USW00003888
1998-11-01—2026-11-13
*   TUCKER 1.3 ENE, GA US US1GADK0001
2008-04-30—2026-11-13
*   ELLENWOOD 2.5 NE, GA US US1GAHY0007
2008-10-28—2026-11-13
*   DECATUR 1.2 SE, GA US US1GADK0013
2008-10-29—2026-11-13
*   RIVERDALE 3.0 WSW, GA US US1GACN0005
2009-04-04—2026-11-13
*   DORAVILLE 2 NNE, GA US USC00092753
2009-10-01—2026-11-13
*   ATLANTA 4.4 E, GA US US1GADK0057
2019-07-01—2026-11-13
*   TUCKER 2.3 NNE, GA US US1GAGW0062

2020-07-24—2026-11-13
*   MARIETTA 4.0 WNW, GA US US1GACB0061
2020-08-12—2026-11-13
*   CHAMBLEE 1.2 SW, GA US US1GADK0061
2020-12-16—2026-11-13
*   MARIETTA 0.8 WSW, GA US US1GACB0064
2021-04-21—2026-11-13
*   DECATUR 2.6 NNE, GA US US1GADK0064
2022-02-07—2026-11-13
*   MARIETTA 4.2 SW, GA US US1GACB0070
2022-09-18—2026-11-13
*   FAIRBURN 4.7 WNW, GA US US1GAFT0074
2023-04-16—2026-11-13
*   ATLANTA 5.9 NE, GA US US1GAFT0076
2025-05-16—2026-11-13
*   ATLANTA 3.7 N, GA US US1GAFT0005
2007-06-08—2026-11-12
*   SANDY SPRINGS 3.2 WNW, GA US US1GACB0004
2008-05-05—2026-11-12
*   KENNESAW 5.6 SW, GA US US1GACB0006
2008-05-28—2026-11-12
*   ATLANTA 2.3 NE, GA US US1GAFT0024
</excerpt>

## Search 9
query: "Los Angeles International Airport station id NCEI usw"
<excerpt title="LOS ANGELES INTL AP (United States) | SSOD Explorer">
1.   Home  
2.   Explorers  
3.   SSOD
Skip to interactive explorer

## NOAA SSODv2 overview
Climate Explorer provides an **independent interface** for the **NOAA/NCEI SSODv2** global daily archive. Climate Explorer is not affiliated with NOAA. SSODv2 provides meteorological summaries across the **United States** (US states including Alaska and Hawaii, plus Puerto Rico, Guam and the US Virgin Islands), **Canada** (provinces and territories), and worldwide networks, featuring UTC-aligned temperature, wind, pressure, and precipitation. It is tailored for meteorological, climate, and environmental researchers analyzing multi-decade daily weather observations, extreme weather events, synoptic storm systems, and station time series.
NOAA/NCEI maintains and publishes SSODv2 summaries assembled from contributed synoptic reports. Climate Explorer retrieves, parses, and presents those records; NOAA/NCEI remains the authoritative source for the archive, summary definitions, and documentation.
Weather station **LOS ANGELES INTL AP** (ID USW00023174), United States. State/region: CA. Elevation: 29.6 m. Coordinates: 33.9381°N, -118.3867°E.
Data period: 1931 to 2026.
**Available parameters:** Daily observations including temperature, precipitation, wind, and related observations where available.
Pro Tip
Click the **Maximize button** in the top-right corner of the explorer frame to expand to **Full Screen mode** for optimal map and chart visibility. Click it again or press `Esc` to exit.
**Dataset facts**
Official source  
NOAA NCEI SSODv2.
Coverage  
Thousands of stations across US states (including Alaska and Hawaii), US territories, Canada, and worldwide; station periods of record extend across many decades.
Update frequency  
NOAA updates the archive daily.
Licence  
CC0 1.0 Universal Public Domain Dedication; retain NOAA/NCEI attribution and source metadata.
Important limitation  
SSOD’s UTC day may differ from a station’s local reporting day. NOAA also cautions that precipitation can be underreported in synoptic messages and that reported daily maximum and minimum temperatures may not capture the true daily extremes.
Professional Climate Services

## NOAA SSODv2 overview
### Need Multi-Station Bulk Data, APIs, or Custom Dashboards?
Interactive Explorers inspect one station or bounded window at a time. When research, risk modeling, or enterprise operations require full-network historical archives (Parquet, DuckDB, CSV), automated real-time ingestion & WIS 2.0 pipelines, spatial homogenization, or tailored Next.js, React, Shiny, and Python FastAPI dashboards, Climate Explorer builds custom production pipelines.
Bulk Archives & APIsCustom DashboardsMulti-Station ExtractionSpatial & Homogenization QC

## Explore selected US stations
Station context, checked observation coverage, and a reproducible example.
*   Central Park, New York City — UTC daily summaries  
*   Chicago O’Hare International Airport — UTC daily summaries  
*   Los Angeles International Airport — UTC daily summaries  
*   Phoenix Airport — UTC daily summaries  
*   Miami International Airport — UTC daily summaries  
*   Seattle–Tacoma Airport — UTC daily summaries

## About the selected station
### Los Angeles International Airport, United States — UTC daily summaries
This is the NOAA station named LOS ANGELES INTL AP, located near the Pacific coast in southwestern Los Angeles. Marine air and coastal cloud often moderate this airport site relative to downtown Los Angeles and inland valleys, so its readings should not be treated as basin-wide averages.
Station USW00023174 · California, United States Location 33.9381°N, 118.3867°W · 29.6 m elevation Inventory range 1931–2026; variable availability and continuity differ.
</excerpt>

## Search 10
query: "Chicago O'Hare airport station id NCEI"
<excerpt title="GARY - NCEI Search, Discovery, & Data Access - NOAA">
# NCEI Search, Discovery, & Data Access
Skip to feedbackSkip to main content
An official website of the United States government  Here's how you know
The .gov means it’s official.
Federal government websites often end in .gov or .mil. Before sharing sensitive information, make sure you’re on a federal government site.
The site is secure.
The **https://** ensures that you are connecting to the official website and that any information you provide is encrypted and transmitted securely.
1.   **NCEI Search, Discovery, & Data Access**  
2.   **Find A Station**  
3.   **Station Details**
*   **API Documentation**  
    *   Data ServiceOrder ServiceSearch ServiceSupport Service

*   **Order Status**  
*   **Cart**
Please Note: NCEI is currently moving its data and applications to the cloud. This upgrade may result in temporary data access delays. Please see our cloud migration overview and frequently asked questions for more information and resources. Check theNCEI Alerts page for impacted products and datasets.Current Impact: Expect delayed data archival and slower update cycles for many products.
Back

# GARY
Station Details
ID 20006468
Coordinates 41.6167, -87.4167
Aliases
GARY/CHICAGO AIRPORT
Identifiers
WBAN 04807 FAA GYY ICAO KGYY NCDCSTNID 20006468 GHCNH USW00004807
Period of Record
Begin Date March 1, 1907
End Date Active
Duration 119 years of record
Station Location
MapLibre | Sources: Esri, TomTom, Garmin, FAO, NOAA, USGS, © OpenStreetMap contributors, and the GIS User Community
Data plot coming soon

# GARY
##### Follow Us
*   @NOAANCEI  
*   @NOAAData  
*   @NOAANCEI  
*   News Feed

# GARY
##### Contact Us
*   [Email: ncei.info@noaa.gov](mailto:ncei.info@noaa.gov "Contact NCEI NOAA via email")  
*   [Phone: (828) 271-4800](tel:18282714800 "Call NCEI NOAA 828-271-4800")

*   Privacy Policy  
*   Freedom of Information Act  
*   Information Quality  
*   Disclaimer  
*   Take Our Survey  
*   Department of Commerce  
*   NOAA  
*   NESDIS
Help improve this site

# GARY
## NCEI Customer Experience Survey
This survey is designed to measure your level of satisfaction with ncei.noaa.gov. It consists of nine questions and should take approximately two to five minutes to complete.
Please do not use this survey to provide comments on or responses to rules, notices, solicitations or other official agency actions. Any information you provide will be used for the sole purpose of improving NOAA's digital products and services. You may also send us an email at [ncei-digital.experience@noaa.gov](mailto:ncei-digital.experience@noaa.gov).  
If you have comments concerning the accessibility of our website, please submit your feedback on our accessibility page.
A red asterisk (*) indicates a required field.

# GARY
## NCEI Customer Experience Survey
### Success
Thank you. Your feedback has been received.
</excerpt>

Read the searches in order: how each query was formed, what came back, and how the next query used it. Find the failure in query choice or revision that cost the most, and write a new system prompt that fixes it. Replace or compress existing text where you can; avoid making the prompt much longer. Do not copy any fact, name, site or topic from these examples: the model will face unrelated questions. Keep the description of the `web_search` tool and the 10-search limit accurate.

Provide the new system prompt within ``` blocks.
