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
Between Earth's moon and Mars' moons, name all features that share a namesake with pre-20th century literary figures (names inspired by them), specifically, those who were known to primarily write fiction or poetry, and whose names were approved in 1973. Use https://planetarynames.wr.usgs.gov/ to source your info.

## Expected answer
Brontë (lunar crater, earth's moon) 
Shakespeare (lunar crater, earth's moon) 
Swift (crater, mars' moon deimos)
Voltaire (crater, mars' moon deimos)
Lucian (crater, earth's moon)

## Grade 0.33

## Search 1 — query: "Moon feature approved 1973 literary name"
### Rank 1 of 53 — 0.32 (passed on)
<excerpt title="Pluto's Largest Moon, Charon, Gets Its First Official Feature Names">
The approved Charon names focus on the literature and mythology of exploration. They are listed here:
**Argo Chasma** is named for the ship sailed by Jason and the Argonauts, in the epic Greek poem Argonautica, during their quest for the Golden Fleece.
**Butler Mons** honours Octavia E. Butler, the first science fiction writer to win a MacArthur fellowship, and whose Xenogenesis trilogy describes humankind’s departure from Earth and subsequent return.
**Caleuche Chasma** is named for the mythological ghost ship that travels the seas around the small island of Chiloé, off the coast of Chile; according to legend, the Caleuche explores the coastline collecting the dead, who then live aboard it forever.
**Clarke Montes** honours Sir Arthur C. Clarke, the prolific science fiction writer and futurist whose novels and short stories (including _2001: A Space Odyssey_) were imaginative depictions of space exploration.
**Dorothy Crater** recognizes the protagonist in the series of children’s novels, by L. Frank Baum, that follows Dorothy Gale’s travels to and adventures in the magical world of Oz.
**Kubrick Mons** honours film director Stanley Kubrick, whose iconic _2001: A Space Odyssey_ tells the story of humanity’s evolution from tool-using hominids to space explorers and beyond.
**Mandjet Chasma** is named for one of the boats in Egyptian mythology that carried the sun god Ra (Re) across the sky each day — making it one of the earliest mythological examples of a vessel of space travel.
**Nasreddin Crater** is named for the protagonist in thousands of humorous folktales told throughout the Middle East, southern Europe and parts of Asia.
**Nemo Crater** is named for the captain of the Nautilus, the submarine in Jules Verne’s novels _Twenty Thousand Leagues Under the Sea_ (1870) and _The Mysterious Island_ (1874).
**Pirx Crater** is named for the main character in a series of short stories by Stanislaw Lem, who travels between the Earth, Moon and Mars.
**Revati Crater** is named for the main character in the Hindu epic narrative Mahabharata — widely regarded as the first in history (circa 400 BC) to include the concept of time travel.

**Sadko Crater** recognizes the adventurer who travelled to the bottom of the sea in the medieval Russian epic Bylina.

## More information
The IAU is the international astronomical organisation that brings together more than 10 000 professional astronomers from almost 100 countries. Its mission is to promote and safeguard the science of astronomy in all its aspects through international cooperation. The IAU also serves as the internationally recognised authority for assigning designations to celestial bodies and the surface features on them. Founded in 1919, the IAU is the world's largest professional body for astronomers.
The New Horizons spacecraft is currently 6.16 billion kilometres from Earth, speeding toward a New Year’s Day 2019 encounter with the Kuiper Belt object (486958) 2014 MU69, which orbits about 1.6 billion kilometres beyond Pluto. This flyby will be the centrepiece of New Horizons’ extended mission through the Kuiper Belt, and will be the farthest planetary encounter — with the most primitive object ever encountered — in spaceflight history.
For more on the New Horizons mission, visit www.nasa.gov/newhorizons and http://pluto.jhuapl.edu.
</excerpt>
### Rank 2 of 53 — 0.29
<excerpt title="Pluto's Moon Charon Gets First Official Feature Names">
Butler Mons honors Octavia E. Butler, the first science fiction writer to win a MacArthur fellowship, and whose Xenogenesis trilogy describes humankind’s departure from Earth and subsequent return.
Caleuche Chasma is named for the mythological ghost ship that travels the seas around the small island of Chiloé, off the coast of Chile; according to legend the Caleuche explores the coastline collecting the dead, who then live aboard it forever.
Clarke Montes honors Sir Arthur C. Clarke, the prolific science fiction writer and futurist whose novels and short stories (including “2001: A Space Odyssey”) were imaginative depictions of space exploration.
Dorothy Crater recognizes the protagonist in the series of children’s novels, by L. Frank Baum, that follows Dorothy Gale’s travels to and adventures in the magical world of Oz.
Kubrick Mons honors film director Stanley Kubrick, whose iconic “2001: A Space Odyssey” tells the story of humanity’s evolution from tool-using hominids to space explorers and beyond.
Mandjet Chasma is named for one of the boats in Egyptian mythology that carried the sun god Ra (Re) across the sky each day – making it one of the earliest mythological examples of a vessel of space travel.
Nasreddin Crater is named for the protagonist in thousands of humorous folktales told throughout the Middle East, southern Europe and parts of Asia.
Nemo Crater is named for the captain of the Nautilus, the submarine in Jules Verne’s novels Twenty Thousand Leagues Under the Sea (1870) and The Mysterious Island (1874).
Pirx Crater is named for the main character in a series of short stories by Stanislaw Lem, who travels between the Earth, Moon and Mars.
Revati Crater is named for the main character in the Hindu epic narrative Mahabharata — widely regarded as the first in history (circa 400 BC) to include the concept of time travel.
Sadko Crater recognizes the adventurer who traveled to the bottom of the sea in the medieval Russian epic Bylina.

The New Horizons spacecraft is currently 3.83 billion miles (6.16 billion kilometers) from Earth, speeding toward a New Year’s Day 2019 encounter with “Ultima Thule,” a Kuiper Belt object orbiting a billion miles (about 1.6 billion kilometers) beyond Pluto. The centerpiece of New Horizons’ extended mission through the Kuiper Belt, the Ultima flyby will be the farthest planetary encounter – with the most primitive object ever encountered – in spaceflight history.
For more on the New Horizons mission, visit http://www.nasa.gov/newhorizons and http://pluto.jhuapl.edu.
</excerpt>
### Rank 3 of 53 — 0.18
<excerpt title="Lunar Imaginaries and Realities in Nancy Holt's 'Moon Book'">
Above the Wells excerpt, Holt includes a postcard of Buzz Aldrin on the lunar surface (_Fig. 4_). Next to Aldrin’s image is a caption that reads, “The Conquest of the Moon by Apollo XI.” It is unclear whether Holt penned this caption or typed out the text from the back of the postcard.10The artist, who had previously worked as a copyeditor, wielded language with the utmost precision, so she chose the wording, whether or not it was her original phrase.11With this textual choice of “conquest,” Holt invokes the history of colonization and U.S. imperialism on Earth as it extended into space. Apollo 11’s planting of an American flag into the Moon’s crust served the project of U.S. cultural imperialism under the optics of global advancement for mankind, ushering in a new era of the cultural mining operation on the Moon, where geopolitical realities now chafed against the imagined lunar landscape. The pairing of the Bastos tobacco and _Dune_ advertisements on page six broadens Holt’s critique of imperialism beyond the United States. Apollo 15’s 1971 mission named one of the Moon’s craters after Frank Herbert’s _Dune_, a recent development that the publishing house capitalized on to boost sales of the 1965 novel. Both the advertising strategy and colonial act of naming a lunar crater miss the novel’s central critique of the exploitation of people and resources under an insatiable galactic empire. Amid Algeria’s fight for independence from French colonial rule following World War II, the Bastos Tobacco Company moved its operations from Algeria to locations in central Africa, noted in the advertisement Holt selected, mirroring the expansionist practices critiqued in _Dune_.12Holt’s pairing of these advertisements highlights the Moon’s status in this period as a site of imaginative investment, demonstrative of the earthly lust for extraterrestrial resources and land.

Holt said that her work was about “bringing the sky down to earth.”13Though _Moon Book_ is a small artwork, it teases out a number of central concerns in Holt’s practice and informs how the Moon might function in Holt’s site-specific work _Sun Tunnels__,_ begun in 1973. At night, the Sun’s light reflects off the Moon, perhaps shining through the constellation holes along the top of each tunnel and allowing nighttime visitors to walk on the Moon or some stars by walking upon their light projected along the tunnel floors, as Holt suggested (_Fig. 5_).14Holt’s placement of _Sun Tunnels_ in Utah ties into David Bourdon’s concept of the American West as a “lunar landscape,” with Holt echoing similar sentiments about her land being akin to the surface of the Moon.15Holt’s sharp critique of U.S. imperialism softens from _Moon Book_ into _Sun Tunnels_. Yet through the ephemerality of _Sun Tunnels’_ nighttime lunar projections, Holt subtly emphasizes the impossibility of human control of the universe. In our present moment, when billionaires launch themselves and celebrities into space in corporate-branded spacecrafts and discuss plans for colonizing Mars, Holt’s reminds us of the limitations of human dominion over nature, terrestrial and extraterrestrial. Through _Moon Book_ and _Sun Tunnels_, Holt asserts the fullness of the Moon as a place of its own making, in contrast to the cultural constructions applied to its cratered surface.

## About the Author
Brooke Eastman is a PhD candidate in Art History at Washington University in St. Louis. Her dissertation examines Land Art's relationships to legal and cultural conceptions of property in the U.S. and utilizes a land-centered approach to restore Indigenous land histories and epistemologies to the sites of these Earthworks. She holds a Harvey Fellowship in American Culture Studies and a Dean's Distinguished Graduate Fellowship. Brooke has held curatorial positions at the Pulitzer Arts Foundation and Leighton House Museum. She holds a BA in History of Art from Yale University and a MA in History of Art from The Courtauld Institute of Art.
</excerpt>
### Rank 4 of 53 — 0.16
<excerpt title="Unofficial Names - The Moon">
## Informal Geologic Surface Formation Names
_The following terms apply more to surface types or textures than to specific features. Most were originally named after a surface feature near which they appeared, but scientists may apply them to similar textures appearing elsewhere on the Moon._
-
Aires Elliptiques  
(observed by G.Delmotte and cartographed by F.C.Lamech). See also page LPOD Miscellany (item *A Ghost Basin Rim?*).
- Apennine Bench Formation

 - Cayley Formation

 -

Frau Mauro Formation
-
Lunar Ellipse of Fire  
(proposed by Farouk El-Baz, _Sky and Telescope_; june 1973).
-
Maunder Formation  
(in Mare Orientale).
- Telemann Formation/ Telemann Unit (northwest of Oceanus Procellarum, near Markov and Sinus Roris).

## Additional Information
See also: Invalid names on the Lunar Topographic Orthophotomaps.
*   This is an alphabetic overview of all the names on the LTO-maps which were not accepted by the International Astronomical Union (IAU). Some of those non-IAU names were also printed on the much more detailed Lunar Topophotomaps. Danny Caes explored each one of the Lunar Topographic Orthophotomaps and Lunar Topophotomaps, and included the numbers of the maps at the corresponding names.
Another important source is the book _Mapping and Naming the Moon; a History of Lunar Cartography and Nomenclature_ by E.A.Whitaker (Cambridge, 2000), and the atlas _The Moon_ by Hugh Percy Wilkins and Patrick Moore.
**More sources**:
- _Op Ontdekking in het Maanland_, by A.J.M.Wanders (Het Spectrum, 1949). Wanders' greenish-colored moonmap shows Riccioli's "terra"-names, and some of Krieger's subdivisions in the Carpathians and the Riphaeus range.

 - _Maanmonografieen_, by Harry de Meyer (1969 version) and Tony Dethier (1989 version). Both books are goldmines for those who want to explore Wilkins's "new" nomenclature!

 - The _Hallwag_ moonmap by Hans Schwarzenbach. Shows many of Wilkins's "new" names!

 - The _Rand McNally_ moonmap. Shows some unofficial names of very mysterious origin (!), and also Wilkins's "new" names.

 - The _Falk_ moonmap. A cornucopia of unofficial names! (Lamech's, Wilkins's, Krieger's, etc...).

## LPOD Articles
* * *
</excerpt>
### Rank 5 of 53 — 0.15
<excerpt title="Unofficial Names - The Moon">
From The Moon
Jump to: navigation, search
*   1 Unofficial, Informal and Discontinued Names  
    *   1.1 Description  
    *   1.2 Discontinued IAU Surface Feature Names  
    *   1.3 The world's most complete ABC of Unofficial Lunar Nomenclature, Discontinued Nomenclature, disallowed names, proposed names, and nicknames (maintained by Danny Caes)  
    *   1.4 Informal Geologic Surface Formation Names  
    *   1.5 Additional Information  
    *   1.6 LPOD Articles

## Unofficial, Informal and Discontinued Names


## Description
By international agreement, names for surface features on the Moon are not "official" unless they are currently approved by the IAU. In addition to these official names, there are many informal and unofficial names, and some once-official names that have been dropped. Some are in widespread use; others are not. The _the-Moon Wiki_ includes lists of many of these. The present page also lists some informal/unofficial descriptive names that have been used by geologists and may not be specific to a particular feature. Unlike official IAU surface feature names, there is no universally agreed upon definition of what the unofficial names refer to. You may, therefore, well encounter some of these names used in ways other than that described here.

## Discontinued IAU Surface Feature Names
_(partial list)_
Al-Tusi (King Y)
Cape Banat (aka Promontorium Banat)
Dorsum Lambert (disallowed name)
Eppinger (Euclides D)
Hercynian Mountains/ Montes Hercynii
J. Cassini
Mare Hiemis
Mare Novum
Mare Parvum
Mons Serao
Montes D'Alembert
Montes Doerfel
Montes Leibnitz
Montes Secchi
Montes Sovietici
Oriani
Palus Nebularum
Pietrosul Bay
Promontorium Banat (Cape Banat).
Promontorium Lavinium
Promontorium Olivium
Rima Burckhardt
Rima Byrgius
Riphaeus Boreus
Riphaeus Medius
Riphaeus Major
Riphaeus Minor
Schneckenberg
Sinus Gay-Lussac
Timoleon
Ural
W. Pickering (Messier A)
*   _Note: over the years many formerly lettered craters have been given individual names. Also in 1973, nearly all the Greek-lettered names for elevated features on the lunar surface were dropped. These former letter designations form the vast bulk of the discontinued IAU names, but they are not listed here_

## The world's most complete ABC of Unofficial Lunar Nomenclature, Discontinued Nomenclature, disallowed names, proposed names, and nicknames (maintained by Danny Caes)
*   Optical Feature Names (Clair-Obscur phenomenae)  
*   Unofficial Names (A to F) (+ link to page of proposed names)  
*   Unofficial Names (G to L) (+ small interview)  
*   Unofficial Names (M to R) (+ list of people behind Unofficial/Informal/Discontinued Nomenclature)  
*   Unofficial Names (S to Z) (+ miscellaneous Info)
Note:
An earlier version of Danny's ABC was compiled in 2000, while reading E.A.Whitaker's book _Mapping and Naming the Moon._ Danny's early interpretation of Whitaker's many lists (lunar nomenclature) and his early list of unofficial lunar nomenclature and nicknames was online in an ancient _GeoCities_ site.

## Informal Geologic Surface Formation Names
_The following terms apply more to surface types or textures than to specific features. Most were originally named after a surface feature near which they appeared, but scientists may apply them to similar textures appearing elsewhere on the Moon._
-
Aires Elliptiques  
(observed by G.Delmotte and cartographed by F.C.Lamech). See also page LPOD Miscellany (item *A Ghost Basin Rim?*).
- Apennine Bench Formation

 - Cayley Formation

 -
</excerpt>

## Search 2 — query: "1973 lunar feature literary name site:planetarynames.wr.usgs.gov"
### Rank 1 of 74 — 0.13 (passed on)
<excerpt title="Categories (Themes) for Naming Features on Planets and Satellites">
##  Mercury
Catenae Radio telescope facilities  
Craters Artists, musicians, painters, and authors who have made outstanding or fundamental contributions to their field and have been recognized as art historically significant figures for more than 50 years  
Dorsa Scientists who have contributed to the study of Mercury  
Faculae Word for "snake" in various languages  
Fossae Significant works of architecture  
Montes Word for "hot" in various languages  
Planitiae, plana Names for Mercury (either the planet or the god) in various languages  
Rupēs Ships of discovery or scientific expeditions  
Valles Abandoned cities (or towns or settlements) of antiquity

##  Venus
Astra Goddesses, miscellaneous  
Chasmata Goddesses of hunt; moon goddesses  
Colles Sea goddesses  
Coronae Fertility and earth goddesses  
Craters Women who have made outstanding or fundamental contributions to their field (over 20 km); Common female first names (under 20 km)  
Dorsa Sky goddesses  
Farra Water goddesses  
Fluctūs Goddesses, miscellaneous  
Fossae Goddesses of war  
Labyrinthi Goddesses, miscellaneous  
Lineae Goddesses of war  
Montes Goddesses, miscellaneous (also one physicist)  
Paterae Famous women  
Planitiae Mythological heroines  
Plana Goddesses of prosperity  
Regiones Giantesses and Titanesses (also two Greek alphanumeric)  
Rupēs Goddesses of hearth and home  
Tesserae Goddesses of fate and fortune  
Terrae Goddesses of love  
Tholi Goddesses, miscellaneous  
Undae Desert goddesses  
Valles Word for planet Venus in various world languages (400 km and longer); River goddesses (less than 400 km in length)

##  The Moon
Note: During the 360-year history of lunar nomenclature, various names were given that do not conform to the present naming scheme, including the special action of 1970 to commemorate six astronauts and six cosmonauts while they were still living. The themes below will be followed for future naming with adherence to the current IAU Rules and Conventions (https://planetarynames.wr.usgs.gov/Page/Rules).
Craters Scientists, engineers, and explorers, as well as other persons connected with astronomy, planetary, or space research who have made outstanding or fundamental contributions to their field. Russian cosmonauts are commemorated by craters in and around Mare Moscoviense. American astronauts are commemorated by craters in and around the crater Apollo. Appropriate locations will be provided in the future for other space-faring nations. First names are used for small craters of special interest.  
Lacūs, maria, paludes, sinūs, and oceani Latin terms describing weather and other abstract concepts  
Montes Terrestrial mountain ranges, nearby craters, and scientists who have made outstanding or fundamental contributions to their fields  
Rupēs, valles Nearby craters or other landforms  
Dorsa Geoscientists  
Catenae and rimae Nearby craters  
Satellite Features Craters lettered after nearby prominent named craters

##  Mars and Martian Satellites
###  Mars
Albedo Features Names from classical mythology assigned by Schiaparelli and Antoniadi  
Large craters (approximately 50 km and larger)Scientists, especially those who have contributed significantly to the study of Mars; writers and others who have contributed to the lore of Mars  
Small craters (approximately 50 km and smaller)Small towns and villages of the world with populations of approximately 100,000 or less. This category is simply a large source of crater names. No commemoration of specific towns or villages is intended.  
Smaller features within a larger named feature The normal naming convention shall be suspended and instead their names shall be chosen so that they bear a mnemonic relationship to the given name of the larger feature, followed by the appropriate descriptor term (crater, cavus, patera, etc.).  
Large valles Name for Mars/star in various languages  
Small valles Classical or modern names of rivers  
Other features From a nearby named albedo feature on Schiaparelli or Antoniadi maps. If no nearby albedo feature name is available, then from a nearby named crater.
</excerpt>
### Rank 2 of 74 — 0.09
<excerpt title="Categories (Themes) for Naming Features on Planets and Satellites">
##  Satellites of Uranus
###  Miranda
Characters, places from Shakespeare's plays

##  Satellites of Uranus
###  Ariel
Light spirits (individual and class)

##  Satellites of Uranus
###  Umbriel
Dark spirits (individual)

##  Satellites of Uranus
###  Titania
Female Shakespearean characters, places

##  Satellites of Uranus
###  Oberon
Shakespearean tragic heroes and places

##  Satellites of Uranus
###  Small Satellites
Names of characters from Shakespeare's plays and from Pope's "Rape of the Lock."

##  Satellites of Neptune
###  Proteus
Water-related spirits, gods, goddesses (excluding Greek and Roman names)

##  Satellites of Neptune
###  Triton
Aquatic names, excluding Roman and Greek. Possible categories include worldwide aquatic spirits, terrestrial fountains or fountain locations, terrestrial aquatic features, terrestrial geysers or geyser locations, terrestrial islands.

##  Satellites of Neptune
###  Nereid
Individual nereids

##  Satellites of Neptune
###  Small Satellites
Gods and goddesses associated with Neptune/Poseidon mythology or generic mythological aquatic beings

##  Pluto and Plutonian Satellites
###  Pluto
Faculae, labyrinthi, maculae, and sulci Gods, goddesses, and other beings associated with the Underworld from mythology, folklore and literature  
Cavi, dorsa, lacūs, and paterae Names for the Underworld and for Underworld locales from mythology, folklore and literature  
Fluctūs, fossae, and valles Heroes and other explorers of the Underworld  
Craters and regiones Scientists and engineers associated with Pluto and the Kuiper Belt  
Colles, lineae, planitiae, and terrae Pioneering space missions and spacecraft  
Montes, paludes, rupēs Historic pioneers who crossed new horizons in the exploration of the Earth, sea and sky

##  Pluto and Plutonian Satellites
###  Charon
Maculae, plana, planitiae, regiones, and terrae Destinations and milestones of fictional space and other exploration  
Chasmata Fictional and mythological vessels of space and other exploration  
Craters Fictional and mythological voyagers, travelers and explorers  
Montes and dorsa Authors and artists associated with space exploration, especially Pluto and the Kuiper Belt

##  Pluto and Plutonian Satellites
###  Styx
River gods

##  Pluto and Plutonian Satellites
###  Nix
Deities of the night

##  Pluto and Plutonian Satellites
###  Kerberos
Dogs from literature, mythology and history

##  Pluto and Plutonian Satellites
###  Hydra
Legendary serpents and dragons

##  Asteroids
###  (1) Ceres
Craters Gods and goddesses of agriculture and vegetation from world mythology  
Other features Names of agricultural festivals of the world

##  Asteroids
###  (4) Vesta
Craters Names historically associated with the Roman goddess Vesta (vestal virgins, people associated with vestal virgins) and famous Roman women. Approved names are not meant to commemorate individuals, but merely as names for surface features.  
Regiones Discoverer of Vesta, and scientists who have contributed to the exploration and study of Vesta  
Other features Places and festivals associated with vestal virgins

##  Asteroids
###  (21) Lutetia
Craters Cities of the Roman Empire and adjacent parts of Europe at the time of Lutetia (52 BC - 360 AD)  
Regiones Discoverer of Lutetia, and provinces of the Roman Empire at the time of Lutetia  
Other features Rivers of the Roman Empire and adjacent parts of Europe at the time of Lutetia

##  Asteroids
###  (243) Ida
Craters Caverns and grottos of the world  
Dorsa Galileo project participants  
Regiones Discoverer of Ida and places associated with the discoverer

##  Asteroids
###  (243) Ida I Dactyl
Craters Idaean dactyls
</excerpt>
### Rank 3 of 74 — 0.09
<excerpt title="Sources of Planetary Names - USGS.gov">
164.Madame Bovary, by Gustave Flaubert: Random House Publications, New York, 1957.  
165.Galileo's Daughter, by Dava Sobel: Chivers Press, Bath, England, 2000.  
166.The New Grove Dictionary of Opera, edited by Stanley Sadie: Macmillan Press, London, 1992.  
167.Astronomiche Nachrichten, vol. 276, page 192, 1948.  
168.Sky and Telescope, New Track Media LLC, Cambridge, MA.  
169.Palanga, Svarbiausois Zintos, by S. Markelyte: Mintis, Vilnius, pages 23-29, 1987.  
170.Myths and Legends of the Ancient Slavs (in Russian), by A. Asov: Nauka i Religiya Publications, Moscow, 1998.  
171.Divine Horsemen: Voodoo Gods of Haiti, by Maya Deren: Chelsea House Publishers, New York, 1970.  
172.Notable Women in the Physical Sciences: A Biographical Dictionary, edited by Benjamin F. Shearer and Barbara S. Shearer, Greenwood Press, Westport CT and London, 1997.  
173.The Columbia Gazetteer of the World, edited by Saul B. Cohen: Columbia University Press, New York, 1998.  
174.Guide to the Gods, by Marjorie Leach: ABC-CLIO, Santa Barbara, 1992.  
175.The Encyclopeadia of Islam, edited by H.A.R. Gibb et al., E.J. Brill Academic Publishers: The Netherlands,1960 (and other editions).  
176.The Great Soviet Encyclopedia: Translation of the Third Edition: Macmillan, Inc., New York, 1975.  
177.The Argonautica, by Valerius Flaccus (with an English translation by J.H. Mozley): The Loeb Classical Library, Cambridge (Mass.), 1934.  
178.Hyginus: Fabulae, edited by Peter K. Marshall: Stuttgart, 1993.
</excerpt>
### Rank 4 of 74 — 0.08
<excerpt title="Sources of Planetary Names - USGS.gov">
299.Dictionary of American Naval Fighting Ships, ed. by James L. Mooney: Naval History Center, 1991.  
300.New Frontiers in Ocean Exploration: The E/V Nautilus and NOAA Ship Okeanos Explorer 2011 Field Season, by K. Bell, K. Elliott, C. Martinez, and S. Fuller: Oceanography, Vol. 25, No. 1, Supplement, March 2012.  
301.Polar Icebreakers in a Changing World, by the National Research Council: National Academies Press, District of Columbia, 2007.  
302.Anne Seymour Damer: a woman of art and fashion, 1748-1828, by Percy Noble: Kegan Paul, Trench, Trubner and Co., London, 1908.  
303.Erté, Things I Remember: An Autobiography: Quadrangle/The New York Times Book Co., 1975.  
304.The Art of the Piano: Its Performers, Literature and Recordings, Volume 1, by David Dubal: Amadeus Press, Cambridge, 2004.  
305.The Tea Ceremony, by Sen’ō Tanaka, Sendō Tanaka, and Edwin Reischauer: Kodansha International, 2000.  
306.Art and Nationalism in Colonial India 1850-1922, by Partha Mitter: Cambridge, 1994.  
307.Eos, vol. 74. no. 28, July 13, 1993.  
308.Quarterly Journal of the Royal Astronomical Society, vol. 3, p. 48.  
309.Mariner 9 Areographic Coordinate System, by G. de Vaucoulers, M.E. Davies, and F.M. Sturms, Jr.: JGR, 78, 4395-4404, 1973.  
310.Journal of the Royal Astronomical Society of Canada, Vol. 104, No. 6, p. 251, December 2010.
</excerpt>
### Rank 5 of 74 — 0.08
<excerpt title="Sources of Planetary Names - USGS.gov">
179.Reader's Digest Wide World Atlas: Reader's Digest Association, New York, 1979.  
180.Atlas SSSR, 2nd edition, Moscow, GUGK, 1983 (in Russian).  
181.Samuel Taylor Coleridge, The Major Works, by Samuel Taylor Coleridge: Oxford University Press, Oxford, 1983.  
182.Oxford Classical Dictionary: Oxford University Press, London, 1968.  
183.The Discovery of the Correct Birth Date for Selenographer Thomas Gwyn Empy Elger, by Robert A. Garfinkle: Journal of the British Astronomical Association, April, 2006.  
184.NIH Record (National Institute of Health newsletter), March 8, 1988, page 7.  
185.Astrid Lindgren, by Eva-Marie Metcalf: Twayne Publishers, New York, 1995.  
186.Alaska Atlas and Gazetteer: DeLorme, Yarmouth, Maine, 1998.  
187.Asteroids III, edited by William F. Bottke, Jr., Alberto Cellino, Paolo Paolicchi, and Richard P. Binzel: University of Arizona Press, Tucson, 2002.  
188.Wilhelmine Wittes Präzisionsrelief des Mondes. Eine Pionierarbeit im Urteil der Wissenschaft, by Jürgen Blunck, in Beiträge zur Astronomiegeschichte, Bd.8, Frankfurt a.M. 2006, Acta Historica Astronomiae, vol.29, pp.150-180.  
189.Who's Who on the Moon, by Elijah E. Cocks and Josiah C. Cocks: Tudor Publishers, Greensboro, 1995.  
190.Laurent Cassegrain Commemorated at Chaudon, by P.D. Hingley: Astronomy and Geophysics, vol. 40, number 1, February 1999.  
191.Gulliver's Travels, by Jonathan Swift: Holt, Rinehart, and Winston, New York, 1967.
</excerpt>

## Search 3 — query: "site:planetarynames.wr.usgs.gov "approved 1973" "Moon" "Crater""
### Rank 1 of 8 — 0.63 (passed on)
<excerpt title="Nomenclature Search Results">
Alder	Moon	82.12	-48.63	-177.88	Crater, craters	1979	Kurt; German organic chemist; Nobel laureate (1902-1958).  
Aldrin	Moon	2.80	1.41	22.09	Crater, craters	1970	Edwin Eugene, Jr. ("Buzz"); American astronaut (1930-Live).  
Alekhin	Moon	74.82	-67.94	-131.85	Crater, craters	1970	Nikolaj Pavlovich; Soviet rocket designer, engineer (1913-1964).  
Alexander	Moon	94.80	40.25	13.69	Crater, craters	1935	Alexander the Great, of Macedon; Greek geographer (356-323 B.C.).  
Alfraganus	Moon	20.52	-5.42	18.97	Crater, craters	1935	Al-Fargani, Abu'l-'Abbās Ahmad Ibn Muhammad Ibn Kathīr; Persian astronomer (unkn-c. 840).  
Alhazen	Moon	34.65	15.91	71.83	Crater, craters	1935	Abū Ali Al-Hasan Ibn Al Haitham; Iraqi mathematician (987-1038).  
Aliacensis	Moon	79.65	-30.60	5.13	Crater, craters	1935	D'Ailly, Pierre; French geographer (1350-1420).  
Al-Khwarizmi	Moon	56.25	7.02	107.01	Crater, craters	1973	Abū Ja'far Muhammad Ibn Mūsā; Iraqi mathematician (unkn-after 847).
</excerpt>
### Rank 2 of 8 — 0.62
<excerpt title="Nomenclature Search Results">
An official website of the United States government
Here’s how you know  
Search  
Gazetteer  
of Planetary  
Nomenclature  
Home  
About  
Nomenclature  
Documentation  
Images and GIS Data  
Advanced Search  
Name Request Instructions  
News  
Nomenclature Search Results  
Target: Moon   
Feature Type: Crater, craters
Go back and Refine your Search
1 - 50 of 1666 results   Results Per Page:   
25  
50  
100  
200  
500  
Add/Remove Columns  
Feature Name
Target
Diameter
Center Latitude
Center Longitude
Feature Type
Approval Date
Origin

8 Homeward	Moon	12.52	-12.02	97.09	Crater, craters	Oct 05, 2018	Crater visible in the iconic “Earthrise” colour photograph, taken aboard Apollo 8 by W. A. Anders on December 24, 1968, symbolizes the safe return to Earth of Apollo 8. The crater was previously designated Ganskiy (Hansky) M.  
Abbe	Moon	63.98	-57.58	174.77	Crater, craters	1970	Ernst Karl; German optician, physicist, astronomer (1840-1905).  
Abbot	Moon	10.40	5.56	54.74	Crater, craters	1973	Charles Greeley; American astrophysicist (1872-1973).  
[Abduh]	Moon	0.00	14.70	39.00	Crater, craters	-	Mohammed; Egyptian writer (1849-1905).  
Abel	Moon	137.35	-34.63	85.78	Crater, craters	1964	Niels Henrik; Norwegian mathematician (1802-1829).  
Abenezra	Moon	43.19	-20.99	11.89	Crater, craters	1935	Abraham ben Meir Ibn Ezra; Spanish mathematician, astronomer (1092-1164/1167).  
Abetti	Moon	1.60	20.11	27.82	Crater, craters	1976	Antonio; Italian astronomer (1846-1928); Giorgio; Italian astronomer (1882-1982).
</excerpt>
### Rank 3 of 8 — 0.60
<excerpt title="Nomenclature Search Results">
8 Homeward	Moon	12.52	-12.02	97.09	Crater, craters	Oct 05, 2018	Crater visible in the iconic “Earthrise” colour photograph, taken aboard Apollo 8 by W. A. Anders on December 24, 1968, symbolizes the safe return to Earth of Apollo 8. The crater was previously designated Ganskiy (Hansky) M.  
Abbe	Moon	63.98	-57.58	174.77	Crater, craters	1970	Ernst Karl; German optician, physicist, astronomer (1840-1905).  
Abbot	Moon	10.40	5.56	54.74	Crater, craters	1973	Charles Greeley; American astrophysicist (1872-1973).  
[Abduh]	Moon	0.00	14.70	39.00	Crater, craters	-	Mohammed; Egyptian writer (1849-1905).  
Abel	Moon	137.35	-34.63	85.78	Crater, craters	1964	Niels Henrik; Norwegian mathematician (1802-1829).  
Abenezra	Moon	43.19	-20.99	11.89	Crater, craters	1935	Abraham ben Meir Ibn Ezra; Spanish mathematician, astronomer (1092-1164/1167).  
Abetti	Moon	1.60	20.11	27.82	Crater, craters	1976	Antonio; Italian astronomer (1846-1928); Giorgio; Italian astronomer (1882-1982).
</excerpt>
### Rank 4 of 8 — 0.14
<excerpt title="Nomenclature Search Results">
Abulfeda	Moon	62.23	-13.87	13.91	Crater, craters	1935	Ismail Ibn Abū al-Fidā; Syrian geographer (1273-1331).  
Abul Wáfa	Moon	54.18	0.96	116.63	Crater, craters	1970	Abū al-Wafā al-Būzajāni; Persian mathematician, astronomer (940-998).  
Acosta	Moon	13.06	-5.65	60.14	Crater, craters	1976	Cristobal; Portuguese doctor, natural historian (1515-1580).  
Adams	Moon	63.27	-31.89	68.39	Crater, craters	1970	John Couch; British astronomer (1819-1892); Charles Hitchcock; American astronomer (1868-1951); Walter Sydney; American astronomer (1876-1956).  
Aepinus	Moon	16.74	87.96	-109.69	Crater, craters	Jan 22, 2009	Franz Maria Ulrich Theodor Hoch; German-Russian astronomer (1724-1802).  
Agatharchides	Moon	51.98	-19.85	-31.11	Crater, craters	1935	Agatharchides of Cnidos; Greek geographer (c. 116 B.C.).  
Agrippa	Moon	43.75	4.10	10.47	Crater, craters	1935	Greek astronomer (unkn-fl. A.D. 92).  
Airy	Moon	38.90	-18.14	5.61	Crater, craters	1935	George Biddell; British astronomer (1801-1892).
</excerpt>
### Rank 5 of 8 — 0.12
<excerpt title="Nomenclature Search Results">
Anders' Earthrise	Moon	40.15	-11.73	100.47	Crater, craters	Oct 05, 2018	Crater visible in the foreground of the iconic “Earthrise” colour photograph, taken aboard Apollo 8 by W. A. Anders on December 24, 1968, showing the Earth and part of the Moon’s surface. The crater was previously designated Pasteur T.  
Anderson	Moon	105.33	15.50	170.79	Crater, craters	1970	John August; American astronomer (1876-1959).  
Andersson	Moon	13.42	-49.95	-95.46	Crater, craters	1985	Leif Erland; American astronomer (1943-1979).  
  1 - 50 of 1666 results
Download all your search results in one of the follow formats (need help?):
CSV (comma separated values) for importing into Excel
Return to top  
About  
Introduction  
History & References  
How Names are Approved  
IAU Working Group and Task Group Members  
FAQ  
Acknowledgements  
Related Resources  
Contact Us  
Nomenclature  
Mercury  
Venus  
The Moon  
Mars System  
Asteroids  
Jupiter System  
Saturn System  
Uranus System  
Neptune System  
Pluto System  
Ring and Ring Gap Nomenclature  
Planet and Satellite Names, Discoverers, and Themes  
Documentation  
IAU Rules  
Database Fields Descriptions  
Abbreviations  
References  
Surface Feature Categories (Themes)  
Descriptor Terms  
Target Coordinate Systems  
Help using the Website  
Images and GIS Data  
Images showing named features  
1:5 Million-Scale Maps of Mercury  
Venus 1:5 million-scale Magellan Imagery  
Venus 1:10 million-scale Quadrangles  
1:1 Million-Scale Maps of the Moon  
Moon 1:10 million-scale Shaded Relief and Color-coded Topography  
Mars 1:5 million-scale THEMIS Images  
GIS Downloads  
Other  
Advanced Search  
Name Request Instructions  
News

USGS Astrogeology Science Center  
The National Aeronautics and Space Administration (NASA)  
International Astronomical Union (IAU)
The Gazetteer of Planetary Nomenclature website is maintained by the USGS Astrogeology Science Center. This work is performed on behalf of the International Astronomical Union's Working Group for Planetary System Nomenclature and is supported by the National Aeronautics and Space Administration under an Interagency Agreement.
Contact Us  
Administrator Log In  
DOI Privacy Policy  
Legal  
Accessibility  
Site Map  
Contact USGS  
U.S. Department of the Interior  
DOI Inspector General  
White House  
E-gov  
No Fear Act  
FOIA  
Follow  
Twitter  
Facebook  
GitHub  
Flickr  
YouTube  
Instagram
</excerpt>

## Search 4 — query: "Moon 1973 "Planetary Names" "Approved 1973" "Crater" "Lunar""
### Rank 1 of 24 — 0.29 (passed on)
<excerpt title="e82aec54...23c6ad">
### Task b3e2e0f9
Diameters are the Search Results values specified in the question. | Feature | Body | Woman | Earliest Nobel year | Approval year | Interval, years | Diameter, km | Sources | |---|---|---|---:|---:|---:|---:|---| | Mistral | Mercury | Gabriela Mistral | 1945 | 1976 | 31 | 102.00 | [[1]][[7]][[12]] | | Cori | Moon | Gerty Cori | 1947 | 1979 | 32 | 67.22 | [[1]][[2]][[5]][[9]] | | Cori | Venus | Gerty Cori | 1947 | 1991 | 44 | 56.10 | [[1]][[6]] | | Balch | Venus | Emily Greene Balch | 1946 | 1994 | 48 | 40.00 | [[1]][[6]] | | Buck | Venus | Pearl S.

### Task b3e2e0f9
Buck | 1938 | 1991 | 53 | 21.80 | [[1]][[6]] | | Joliot-Curie | Venus | Irène Joliot-Curie | 1935 | 1991 | 56 | 91.10 | [[1]][[6]] | | Undset | Venus | Sigrid Undset | 1928 | 1985 | 57 | 20.00 | [[1]][[6]] | | Sklodowska | Moon | Marie Curie | 1903 | 1961 | 58 | 125.55 | [[1]][[3]][[5]][[10]] | | Deledda | Venus | Grazia Deledda | 1926 | 1985 | 59 | 32.00 | [[1]][[4]][[6]] | | Addams | Venus | Jane Addams | 1931 | 1994 | 63 | 87.00 | [[1]][[6]] | | Sklodowska | Mars | Marie Curie | 1903 | 1973 | 70 | 109.72 | [[1]][[3]][[8]][[13]] | | Lagerlöf | Venus | Selma Lagerlöf | 1909 | 1985 | 76 | 56.00 | [[1]][[6]] | | von Suttner | Venus | Bertha von Suttner | 1905 | 1994 | 89 | 24.00 | [[1]][[6]] | Several plausible extra entries fail the conditions. **Curie on the Moon** and **Curie on Mars** identify Pierre Curie, so neither is an entry for Marie. **Joliot on the Moon** identifies Frédéric Joliot-Curie, so it is not an entry for Irène. The lunar **[Undest]** identifies Sigrid, but its record explicitly says the name was never approved by the IAU. It is excluded despite its namesake.
</excerpt>
### Rank 2 of 24 — 0.26
<excerpt title="e82aec54...23c6ad">
### Task b3e2e0f9
https://planetarynames.wr.usgs.gov/Feature/3929
Status and Origin Approval Status Adopted by IAU Approval Date 1976 Continent South and Central America Ethnicity Chile Origin Gabriela; Chilean poet (1889-1957). Reference [59] - The New Encyclopaedia Britannica: Encyclopaedia Britannica Inc., Chicago, 1974, 1993.
https://planetarynames.wr.usgs.gov/Feature/5593
Status and Origin Approval Status Adopted by IAU Approval Date 1973 Continent Europe Ethnicity Poland Origin Marie; Polish-born French chemist (Mme P. Curie) (1867-1934). Reference [68] - World Who's Who in Science, edited by Allen G. Debus: Western Publishing Company, Hannibal, Mo., 1968: New York, 1973.
https://planetarynames.wr.usgs.gov/Feature/1351
Status and Origin Approval Status Adopted by IAU Approval Date 1973 Continent Europe Ethnicity France Origin Pierre; French physicist-chemist (1859-1906). Reference [68] - World Who's Who in Science, edited by Allen G. Debus: Western Publishing Company, Hannibal, Mo., 1968: New York, 1973.
Gazetteer: Sklodowska A, Moon
Basic Info Feature Name Sklodowska A Clean Name Sklodowska A Feature ID 13132 Target Moon Feature Type Satellite Feature
Status and Origin Approval Status Adopted by IAU Approval Date 2006 Continent Europe Ethnicity Poland Origin Marie (Madame Curie); Polish physicist, chemist, Nobel laureate (1867-1934). Reference -

### Validator evidence
Scoring rows
validator
status
score
cost
time
5Cm4fATs...koT7Rt  
ok
Deep judge 0.000 cost $0.3679 time 4m 23s
The final synthesis step could not run to completion; the gathered source-backed evidence supports the following points:  
[[1]] # Gazetteer of Planetary Nomenclature  
September 10, 2018

## Gazetteer of Planetary Nomenclature
### This gazetteer contains detailed information about all names of topographic and albedo features on planets and satellites that the International Astronomical U
[[2]] # Gazetteer of Planetary Nomenclature

## Nomenclature News
The IAU Working Group for Planetary System Nomenclature has approved the name Mirabilis Rupes for a featur  
[[3]] # Nomenclature  
Explore the database of IAU-approved planetary names by clicking on the target planet/planetary system tabs in the navigation menu, or by using the Advanced Search. The target pages show approved surface feature names for each body organized by  
[[4]] # Gazetteer of Planetary Nomenclature  
The combined logos of the USGS, NASA, and the IAU  
_Gazetteer  
of Planetary  
Nomenclature_  
Search Search
...
The IAU Working Group for Planetary System Nomencl  
[[5]] # Advanced Nomenclature Search  
|**System:** |All Asteroids Earth Jupiter Mars Mercury Neptune Pluto Saturn Uranus Venus |  
| --- | --- | --- | --- |  
| |or |  
|**Target:** |All Amalthea Ariel Arrokoth Bennu Callisto Ceres Charon Dactyl Deimos Didymos Dimorphos Di  
[[6]] # Gazetteer of Planetary Nomenclature
The IAU Working Group for Planetary System Nomenclature has approved the name Mirabilis Rupes for a featur  
[[7]] # Target: The Moon
</excerpt>
### Rank 3 of 24 — 0.25
<excerpt title="e82aec54...23c6ad">
### Task b3e2e0f9
Buck | 1938 | 1991 | 53 | 21.80 | [[1]][[6]] | | Joliot-Curie | Venus | Irène Joliot-Curie | 1935 | 1991 | 56 | 91.10 | [[1]][[6]] | | Undset | Venus | Sigrid Undset | 1928 | 1985 | 57 | 20.00 | [[1]][[6]] | | Sklodowska | Moon | Marie Curie | 1903 | 1961 | 58 | 125.55 | [[1]][[3]][[5]][[10]] | | Deledda | Venus | Grazia Deledda | 1926 | 1985 | 59 | 32.00 | [[1]][[4]][[6]] | | Addams | Venus | Jane Addams | 1931 | 1994 | 63 | 87.00 | [[1]][[6]] | | Sklodowska | Mars | Marie Curie | 1903 | 1973 | 70 | 109.72 | [[1]][[3]][[8]][[13]] | | Lagerlöf | Venus | Selma Lagerlöf | 1909 | 1985 | 76 | 56.00 | [[1]][[6]] | | von Suttner | Venus | Bertha von Suttner | 1905 | 1994 | 89 | 24.00 | [[1]][[6]] | Several plausible extra entries fail the conditions. **Curie on the Moon** and **Curie on Mars** identify Pierre Curie, so neither is an entry for Marie. **Joliot on the Moon** identifies Frédéric Joliot-Curie, so it is not an entry for Irène. The lunar **[Undest]** identifies Sigrid, but its record explicitly says the name was never approved by the IAU. It is excluded despite its namesake.

### Task b3e2e0f9
[[5]][[8]][[11]][[14]] Generic given names also do not establish a commemorated laureate under the question's Origin rule. Satellite entries are excluded by Feature Type: for example, Sklodowska A actually identifies Marie in its Origin, but its Feature Type is **Satellite Feature**, rather than **Crater, craters**. [[15]] The distinction between a designated prize year and receipt date affects Deledda: her facts page calls it the **1926** prize and states that she received it in **1927**. Her interval is therefore 1985−1926 = 59 years. [[4]][[6]] ## Original mean and diameter gap The thirteen intervals sum to 31 + 32 + 44 + 48 + 53 + 56 + 57 + 58 + 59 + 63 + 70 + 76 + 89 = **736 years**. Thus the original mean is **736/13 = 56.6153846… years**. In the complete ordered population, the closest interval strictly below it is 56, belonging to Joliot-Curie on Venus, and the closest strictly above it is 57, belonging to Undset on Venus. Their Search Results diameters are 91.10 km and 20.00 km, respectively. [[6]] Therefore the original diameter gap is **|91.10 − 20.00| = 71.10 km**. ## Establishing the greatest attainable change There are eleven represented women, so the question considers **11×10/2 = 55 unordered pairs**. An omission removes all entries for either woman; the two entries each for Marie Curie and Gerty Cori must be removed together. [[2]][[3]][[5]][[6]][[8]] The largest eligible diameter is the lunar Sklodowska's 125.55 km and the smallest is Undset's 20.00 km. Consequently, no remaining population can have a diameter gap greater than **105.55 km**.
</excerpt>
### Rank 4 of 24 — 0.20
<excerpt title="e82aec54...23c6ad">
### Task b3e2e0f9
https://planetarynames.wr.usgs.gov/SearchResults?Target=20_Mars&Feature%20Type=9_Crater,%20craters
1351 Curie Curie Mars 111.11 28.78 355.25 29.72 27.85 356.33 354.19 Planetocentric, +East, 0 - 360 Europe France Crater, craters AA mc11 Approved 1973 [68] Pierre; French physicist-chemist (1859-1906).
5593 Sklodowska Sklodowska Mars 109.72 33.52 357.05 34.45 32.60 358.16 355.94 Planetocentric, +East, 0 - 360 Europe Poland Crater, craters AA mc04 Approved 1973 [68] Marie; Polish-born French chemist (Mme P. Curie) (1867-1934).
https://planetarynames.wr.usgs.gov/Feature/1308
Status and Origin Approval Status Adopted by IAU Approval Date 1979 Continent Europe Ethnicity Czechoslovakia Origin Gerty Theresa Radnitz; Czech-American physiologist; Nobel laureate (1896-1957). Reference -
https://planetarynames.wr.usgs.gov/Feature/5592
Status and Origin Approval Status Adopted by IAU Approval Date 1961 Continent Europe Ethnicity Poland Origin Marie (Madame Curie); Polish physicist, chemist, Nobel laureate (1867-1934). Reference -
https://planetarynames.wr.usgs.gov/Feature/6923
Status and Origin Approval Status Never approved by the IAU Approval Date 1984 Continent Europe Ethnicity Norway Origin Sigrid; Norwegian novelist; Nobel laureate (1882-1949). Reference [75] - Webster's Biographical Dictionary: G. and C. Merriam Company, Springfield, Mass., 1974 (and other editions).

### Task b3e2e0f9
https://planetarynames.wr.usgs.gov/Feature/3929
Status and Origin Approval Status Adopted by IAU Approval Date 1976 Continent South and Central America Ethnicity Chile Origin Gabriela; Chilean poet (1889-1957). Reference [59] - The New Encyclopaedia Britannica: Encyclopaedia Britannica Inc., Chicago, 1974, 1993.
https://planetarynames.wr.usgs.gov/Feature/5593
Status and Origin Approval Status Adopted by IAU Approval Date 1973 Continent Europe Ethnicity Poland Origin Marie; Polish-born French chemist (Mme P. Curie) (1867-1934). Reference [68] - World Who's Who in Science, edited by Allen G. Debus: Western Publishing Company, Hannibal, Mo., 1968: New York, 1973.
https://planetarynames.wr.usgs.gov/Feature/1351
Status and Origin Approval Status Adopted by IAU Approval Date 1973 Continent Europe Ethnicity France Origin Pierre; French physicist-chemist (1859-1906). Reference [68] - World Who's Who in Science, edited by Allen G. Debus: Western Publishing Company, Hannibal, Mo., 1968: New York, 1973.
Gazetteer: Sklodowska A, Moon
Basic Info Feature Name Sklodowska A Clean Name Sklodowska A Feature ID 13132 Target Moon Feature Type Satellite Feature
Status and Origin Approval Status Adopted by IAU Approval Date 2006 Continent Europe Ethnicity Poland Origin Marie (Madame Curie); Polish physicist, chemist, Nobel laureate (1867-1934). Reference -
</excerpt>
### Rank 5 of 24 — 0.15
<excerpt title="e82aec54...23c6ad">
### Task b3e2e0f9
**Seven unordered pairs of women** attain the greatest absolute change in the diameter gap. Each produces a remaining gap of **1.80 km**, between **Buck on Venus** and **Undset on Venus**, compared with the full population's **71.10 km** gap. The maximum change is therefore **69.30 km**. The count includes two pairs for which Joliot-Curie remains in the population but its interval equals the new mean, so it is neither strict boundary. These are calculated results from the complete population established below. [[1]][[5]][[6]][[7]][[8]] ## Establishing the eligible population For the question’s 16 October 2026 scope, the historical Nobel restriction identifies eleven women: Marie Curie, Bertha von Suttner, Selma Lagerlöf, Grazia Deledda, Sigrid Undset, Jane Addams, Irène Joliot-Curie, Pearl S. Buck, Gabriela Mistral, Emily Greene Balch and Gerty Cori. NobelPrize.org's list of women laureates supplies their designated prize years. Marie Curie appears with both 1903 and 1911; the question's earliest-year rule therefore requires 1903. [[1]][[3]] I matched those identities against the complete Gazetteer crater Search Results tables for the four specified bodies, retaining approved entries whose Origin identifies the woman. This yields **thirteen feature entries**: nine on Venus, two on the Moon, one on Mercury and one on Mars. The count is by feature, so Cori and Sklodowska each contribute two observations. [[5]][[6]][[7]][[8]] Two identity connections matter. The Moon's Cori identifies **Gerty Theresa Radnitz**, while NobelPrize.org identifies the laureate as **Gerty Theresa Cori, née Radnitz**. Both Cori entries therefore belong to the same woman. [[2]][[5]][[6]][[9]] The lunar Sklodowska identifies Marie (Madame Curie), and the Martian Sklodowska identifies Marie, Mme P. Curie; both use her earliest Nobel year, 1903. [[3]][[5]][[8]][[10]][[13]] The following table gives the complete qualifying population. The interval column is calculated as approval year minus earliest designated prize year.

### Task b3e2e0f9
Diameters are the Search Results values specified in the question. | Feature | Body | Woman | Earliest Nobel year | Approval year | Interval, years | Diameter, km | Sources | |---|---|---|---:|---:|---:|---:|---| | Mistral | Mercury | Gabriela Mistral | 1945 | 1976 | 31 | 102.00 | [[1]][[7]][[12]] | | Cori | Moon | Gerty Cori | 1947 | 1979 | 32 | 67.22 | [[1]][[2]][[5]][[9]] | | Cori | Venus | Gerty Cori | 1947 | 1991 | 44 | 56.10 | [[1]][[6]] | | Balch | Venus | Emily Greene Balch | 1946 | 1994 | 48 | 40.00 | [[1]][[6]] | | Buck | Venus | Pearl S.
</excerpt>

## Search 5 — query: "Phobos feature approved 1973 literary name"
### Rank 1 of 115 — 0.58 (passed on)
<excerpt title="Phobos (moon)">
## Physical characteristics
| Shklovsky | 24°N 112°E / 24°N 112°E | 2 | 2011 | Iosif Shklovsky, Soviet astronomer (1916–1985) | WGPSN |  
| Skyresh | 52°30′N 40°00′E / 52.5°N 40°E | 1.5 | 2006 | Skyresh Bolgolam; High Admiral of the Lilliput council who opposed Gulliver's plea for freedom and accused him of being a traitor in _Gulliver's Travels_ | WGPSN |  
| Stickney | 1°N 49°W / 1°N 49°W | 9 | 1973 | Angeline Stickney (1830–1892); wife of American astronomer Asaph Hall (see Hall crater) | WGPSN |  
| Todd | 9°S 153°W / 9°S 153°W | 2.6 | 1973 | David Peck Todd; American astronomer (1855–1939) | WGPSN |  
| Wendell | 1°S 132°W / 1°S 132°W | 1.7 | 1973 | Oliver Wendell; American astronomer (1845–1912) | WGPSN |

## Physical characteristics
There is one named regio, _Laputa Regio_, and one named planitia, _Lagado Planitia_; both are named after places in _Gulliver's Travels_ (the fictional [Laputa](https://en.wikipedia.org/wiki/Gulliver's_Travels#Part_III:_A_Voyage_to_Laputa,_Balnibarbi,_Luggnagg,_Glubbdubdrib_and_Japan "Gulliver's Travels"), a flying island, and Lagado, imaginary capital of the fictional nation Balnibarbi).[[55]](https://en.wikipedia.org/wiki/Phobos_(moon)#cite_note-57) The only named ridge on Phobos is _Kepler Dorsum_, named after the astronomer Johannes Kepler.[[56]](https://en.wikipedia.org/wiki/Phobos_(moon)#cite_note-58)
</excerpt>
### Rank 2 of 115 — 0.57
<excerpt title="Phobos (moon)">
## Physical characteristics
The unique Kaidun meteorite that fell on a Soviet military base in Yemen in 1980 has been hypothesised to be a piece of Phobos, but this could not be verified because little is known about the exact composition of Phobos.[[51]](https://en.wikipedia.org/wiki/Phobos_(moon)#cite_note-53)[[52]](https://en.wikipedia.org/wiki/Phobos_(moon)#cite_note-54)
Geological features on Phobos are named after astronomers who studied Phobos and people and places from Jonathan Swift's _[Gulliver's Travels](https://en.wikipedia.org/wiki/Gulliver's\_Travels "Gulliver's Travels")_.[[53]](https://en.wikipedia.org/wiki/Phobos_(moon)#cite_note-55) Some craters have been named, and are listed in the following map and table.[[54]](https://en.wikipedia.org/wiki/Phobos_(moon)#cite_note-56)
Named craters on Phobos

## Physical characteristics
| Crater | Coordinates | Diameter (km) | Approval Year | Eponym | Ref |  
| --- | --- | --- | --- | --- | --- |  
| Clustril | 60°N 91°W / 60°N 91°W | 3.4 | 2006 | Character in Lilliput who informed Flimnap that his wife had visited Gulliver privately in Jonathan Swift's novel _[Gulliver's Travels](https://en.wikipedia.org/wiki/Gulliver's\_Travels "Gulliver's Travels")_ | WGPSN |  
| D'Arrest | 39°S 179°W / 39°S 179°W | 2.1 | 1973 | [Heinrich Louis d'Arrest](https://en.wikipedia.org/wiki/Heinrich_Louis_d'Arrest "Heinrich Louis d'Arrest"); German/Danish astronomer (1822–1875) | WGPSN |  
| Drunlo | 36°30′N 92°00′W / 36.5°N 92°W | 4.2 | 2006 | Character in Lilliput who informed Flimnap that his wife had visited Gulliver privately in _Gulliver's Travels_ | WGPSN |  
| Flimnap | 60°N 10°E / 60°N 10°E | 1.5 | 2006 | Treasurer of Lilliput in _Gulliver's Travels_ | WGPSN |  
| Grildrig | 81°N 165°E / 81°N 165°E | 2.6 | 2006 | Name given to Gulliver by the farmer's daughter Glumdalclitch in the giants' country Brobdingnag in _Gulliver's Travels_ | WGPSN |
</excerpt>
### Rank 3 of 115 — 0.49
<excerpt title="Phobos (moon)">
## Physical characteristics
| Gulliver | 62°N 163°W / 62°N 163°W | 5.5 | 2006 | Lemuel Gulliver; surgeon captain and voyager in _Gulliver's Travels_ | WGPSN |  
| Hall | 80°S 150°E / 80°S 150°E | 5.4 | 1973 | Asaph Hall; American astronomer discoverer of Phobos and Deimos (1829–1907) | WGPSN |  
| Limtoc | 11°S 54°W / 11°S 54°W | 2 | 2006 | General in Lilliput who prepared articles of impeachment against Gulliver in _Gulliver's Travels_ | WGPSN |  
| Öpik | 7°S 63°E / 7°S 63°E | 2 | 2011 | Ernst J. Öpik, Estonian astronomer (1893–1985) | WGPSN |  
| Reldresal | 41°N 39°W / 41°N 39°W | 2.9 | 2006 | Secretary for Private Affairs in Lilliput; Gulliver's friend in _Gulliver's Travels_ | WGPSN |  
| Roche | 53°N 177°E / 53°N 177°E | 2.3 | 1973 | Édouard Roche; French astronomer (1820–1883) | WGPSN |  
| Sharpless | 27°30′S 154°00′W / 27.5°S 154°W | 1.8 | 1973 | Bevan Sharpless; American astronomer (1904–1950) | WGPSN |  

## Physical characteristics
| Shklovsky | 24°N 112°E / 24°N 112°E | 2 | 2011 | Iosif Shklovsky, Soviet astronomer (1916–1985) | WGPSN |  
| Skyresh | 52°30′N 40°00′E / 52.5°N 40°E | 1.5 | 2006 | Skyresh Bolgolam; High Admiral of the Lilliput council who opposed Gulliver's plea for freedom and accused him of being a traitor in _Gulliver's Travels_ | WGPSN |  
| Stickney | 1°N 49°W / 1°N 49°W | 9 | 1973 | Angeline Stickney (1830–1892); wife of American astronomer Asaph Hall (see Hall crater) | WGPSN |  
| Todd | 9°S 153°W / 9°S 153°W | 2.6 | 1973 | David Peck Todd; American astronomer (1855–1939) | WGPSN |  
| Wendell | 1°S 132°W / 1°S 132°W | 1.7 | 1973 | Oliver Wendell; American astronomer (1845–1912) | WGPSN |
</excerpt>
### Rank 4 of 115 — 0.32
<excerpt title="Asaph Hall and Two Moons I Would Not Go Anywhere Near">
**11.** There’s a curious murkiness in the history of the naming of the moons that begins with the discovery and continues beyond the official, or quasi-official, assignment of the names. The discovery itself is well documented, and the assignment of the names is similarly well documented. In between, the facts get murky. What’s clear is that the names that Asaph Hall chose _were suggested_ to Asaph Hall. Asaph Hall states this himself in a letter (undated, but from shortly after the discovery) that describes the provenance of the suggestion and gives credit:
> “…of various names that have been proposed for these satellites, I have chosen those suggested by Mr. Madan of Eton, viz., Deimos for the outer satellite, Phobos for the inner satellite…These lines [from which the names are drawn] occur in the 15 th book of the _Iliad_ when Ares is preparing to descend to the Earth to avenge the death of his son. Bryant’s translation is as follows: ‘He spake, and summoned Fear and Flight to yoke his steeds, and put his glorious armor on.'”
The “Mr. Madan” referred to here is Henry George Madan, an English chemist and for two decades the science master at Eton College. I note in passing that Henry George Madan died in 1901 at the age of 63, a few months after being knocked down by a railroad boxcar, which led to the amputation of his arm, from which he never fully recovered.

**12.** Because Asaph Hall knew Greek, and knew the _Iliad_ in Greek, it was entirely in his power to make an informed choice of names, on his own, without resorting to someone else’s suggestion. If for whatever reason he was uncomfortable in choosing on his own, he easily could have consulted with Chloe Angeline Stickney Hall, his wife, who read Greek and knew the _Iliad_. If he decided that neither he nor Chloe Angeline Stickney Hall were up to the task of drawing from Greek so as to bestow permanent names on major nearby natural satellites, he easily could have sought the guidance of an expert. Instead, he went with a suggestion from someone who had no special expertise in Greek, a chemist who, at best, happened to know Greek just as Asaph Hall happened to know Greek and Chloe Angeline Stickney Hall happened to know Greek, that is, recreationally. Quite possibly Henry George Madan’s command of Greek was in fact inferior to Asaph Hall’s command and Chloe Angeline Stickney Hall’s command. There’s no evidence that after learning Greek as a pedagogical requirement, Henry George Madan went on to read Greek aloud to his family in the evening at the hearth. All that’s certain is that Henry George Madan knew the passage in the _Iliad_ and the Greek names translated as “Fear” and “Flight” in the translation that Asaph Hall quotes.
_Asaph Hall_
</excerpt>
### Rank 5 of 115 — 0.32
<excerpt title="Phobos (moon)">
## Physical characteristics
Many grooves and streaks cover the oddly shaped surface. The grooves are typically less than 30 metres (98 ft) deep, 100 to 200 metres (330 to 660 ft) wide, and up to 20 kilometres (12 mi) in length, and were originally assumed to have been the result of the same impact that created Stickney. Analysis of results from the _Mars Express_ spacecraft revealed that the grooves are not radial to Stickney, but are centered on the leading apex of Phobos in its orbit (which is not far from Stickney). Researchers suspected that they had been excavated by material ejected into space by impacts on the surface of Mars. The grooves thus formed as crater chains, and all of them fade away as the trailing apex of Phobos is approached. They have been grouped into 12 or more families of varying age, presumably representing at least 12 Martian impact events.[[46]](https://en.wikipedia.org/wiki/Phobos_(moon)#cite_note-grooves_origin-48) In November 2018, based on computational probability analysis, astronomers concluded that the many grooves on Phobos were caused by boulders ejected from the asteroid impact that created Stickney crater. These boulders rolled in a predictable pattern on the surface of the moon.[[47]](https://en.wikipedia.org/wiki/Phobos_(moon)#cite_note-UT-20181120-49)[[48]](https://en.wikipedia.org/wiki/Phobos_(moon)#cite_note-PSS-20181116-50)
Faint dust rings produced by Phobos and Deimos have long been predicted but attempts to observe these rings have, to date, failed.[[49]](https://en.wikipedia.org/wiki/Phobos_(moon)#cite_note-51) Images from _Mars Global Surveyor_ indicate that Phobos is covered with a layer of fine-grained regolith at least 100 metres thick; it is hypothesised to have been created by impacts from other bodies, but it is not known how the material stuck to an object with almost no gravity.[[50]](https://en.wikipedia.org/wiki/Phobos_(moon)#cite_note-52)

## Physical characteristics
The unique Kaidun meteorite that fell on a Soviet military base in Yemen in 1980 has been hypothesised to be a piece of Phobos, but this could not be verified because little is known about the exact composition of Phobos.[[51]](https://en.wikipedia.org/wiki/Phobos_(moon)#cite_note-53)[[52]](https://en.wikipedia.org/wiki/Phobos_(moon)#cite_note-54)
Geological features on Phobos are named after astronomers who studied Phobos and people and places from Jonathan Swift's _[Gulliver's Travels](https://en.wikipedia.org/wiki/Gulliver's\_Travels "Gulliver's Travels")_.[[53]](https://en.wikipedia.org/wiki/Phobos_(moon)#cite_note-55) Some craters have been named, and are listed in the following map and table.[[54]](https://en.wikipedia.org/wiki/Phobos_(moon)#cite_note-56)
Named craters on Phobos
</excerpt>

## Search 6 — query: ""Approval Date" 1973 Moon crater site:planetarynames.wr.usgs.gov"
### Rank 1 of 290 — 0.69 (passed on)
<excerpt title="Nomenclature Search Results">
Alder	Moon	82.12	-48.63	-177.88	Crater, craters	1979	Kurt; German organic chemist; Nobel laureate (1902-1958).  
Aldrin	Moon	2.80	1.41	22.09	Crater, craters	1970	Edwin Eugene, Jr. ("Buzz"); American astronaut (1930-Live).  
Alekhin	Moon	74.82	-67.94	-131.85	Crater, craters	1970	Nikolaj Pavlovich; Soviet rocket designer, engineer (1913-1964).  
Alexander	Moon	94.80	40.25	13.69	Crater, craters	1935	Alexander the Great, of Macedon; Greek geographer (356-323 B.C.).  
Alfraganus	Moon	20.52	-5.42	18.97	Crater, craters	1935	Al-Fargani, Abu'l-'Abbās Ahmad Ibn Muhammad Ibn Kathīr; Persian astronomer (unkn-c. 840).  
Alhazen	Moon	34.65	15.91	71.83	Crater, craters	1935	Abū Ali Al-Hasan Ibn Al Haitham; Iraqi mathematician (987-1038).  
Aliacensis	Moon	79.65	-30.60	5.13	Crater, craters	1935	D'Ailly, Pierre; French geographer (1350-1420).  
Al-Khwarizmi	Moon	56.25	7.02	107.01	Crater, craters	1973	Abū Ja'far Muhammad Ibn Mūsā; Iraqi mathematician (unkn-after 847).
</excerpt>
### Rank 2 of 290 — 0.67
<excerpt title="Nomenclature Search Results">
An official website of the United States government
Here’s how you know  
Search  
Gazetteer  
of Planetary  
Nomenclature  
Home  
About  
Nomenclature  
Documentation  
Images and GIS Data  
Advanced Search  
Name Request Instructions  
News  
Nomenclature Search Results  
Target: Moon   
Feature Type: Crater, craters
Go back and Refine your Search
1 - 50 of 1666 results   Results Per Page:   
25  
50  
100  
200  
500  
Add/Remove Columns  
Feature Name
Target
Diameter
Center Latitude
Center Longitude
Feature Type
Approval Date
Origin

8 Homeward	Moon	12.52	-12.02	97.09	Crater, craters	Oct 05, 2018	Crater visible in the iconic “Earthrise” colour photograph, taken aboard Apollo 8 by W. A. Anders on December 24, 1968, symbolizes the safe return to Earth of Apollo 8. The crater was previously designated Ganskiy (Hansky) M.  
Abbe	Moon	63.98	-57.58	174.77	Crater, craters	1970	Ernst Karl; German optician, physicist, astronomer (1840-1905).  
Abbot	Moon	10.40	5.56	54.74	Crater, craters	1973	Charles Greeley; American astrophysicist (1872-1973).  
[Abduh]	Moon	0.00	14.70	39.00	Crater, craters	-	Mohammed; Egyptian writer (1849-1905).  
Abel	Moon	137.35	-34.63	85.78	Crater, craters	1964	Niels Henrik; Norwegian mathematician (1802-1829).  
Abenezra	Moon	43.19	-20.99	11.89	Crater, craters	1935	Abraham ben Meir Ibn Ezra; Spanish mathematician, astronomer (1092-1164/1167).  
Abetti	Moon	1.60	20.11	27.82	Crater, craters	1976	Antonio; Italian astronomer (1846-1928); Giorgio; Italian astronomer (1882-1982).
</excerpt>
### Rank 3 of 290 — 0.61
<excerpt title="Nomenclature Search Results">
8 Homeward	Moon	12.52	-12.02	97.09	Crater, craters	Oct 05, 2018	Crater visible in the iconic “Earthrise” colour photograph, taken aboard Apollo 8 by W. A. Anders on December 24, 1968, symbolizes the safe return to Earth of Apollo 8. The crater was previously designated Ganskiy (Hansky) M.  
Abbe	Moon	63.98	-57.58	174.77	Crater, craters	1970	Ernst Karl; German optician, physicist, astronomer (1840-1905).  
Abbot	Moon	10.40	5.56	54.74	Crater, craters	1973	Charles Greeley; American astrophysicist (1872-1973).  
[Abduh]	Moon	0.00	14.70	39.00	Crater, craters	-	Mohammed; Egyptian writer (1849-1905).  
Abel	Moon	137.35	-34.63	85.78	Crater, craters	1964	Niels Henrik; Norwegian mathematician (1802-1829).  
Abenezra	Moon	43.19	-20.99	11.89	Crater, craters	1935	Abraham ben Meir Ibn Ezra; Spanish mathematician, astronomer (1092-1164/1167).  
Abetti	Moon	1.60	20.11	27.82	Crater, craters	1976	Antonio; Italian astronomer (1846-1928); Giorgio; Italian astronomer (1882-1982).
</excerpt>
### Rank 4 of 290 — 0.23
<excerpt title="Advanced Nomenclature Search - Planetary Names - USGS.gov">
# Planetary Names
An official website of the United States government
Here’s how you know
Here’s how you know
**Official websites use .gov**
A **.gov** website belongs to an official government organization in the United States.
**Secure .gov websites use HTTPS**
A **lock** ( ) or **https://** means you’ve safely connected to the .gov website. Share sensitive information only on official, secure websites.
Search
_Gazetteer
of Planetary
Nomenclature_
Search
*   Home  
*   About  
*   Nomenclature  
*   Documentation  
*   Images and GIS Data  
*   Advanced Search  
*   Name Request Instructions  
*   News
_Gazetteer of Planetary Nomenclature_
Menu
_Gazetteer
of Planetary
Nomenclature_
Search
*   Home  
*   About  
*   Nomenclature  
*   Documentation  
*   Images and GIS Data  
*   Advanced Search  
*   Name Request Instructions  
*   News

# Planetary Names
## Advanced Nomenclature Search
* * *
This search engine searches the database of planetary surface feature names. Here are links with more information about the names of planets and their moons and information about the names of rings and ring gaps. | **System:** |  |  
| --- |  
|  | or |  
| **Target:** |  |  
| **Latitude and Longitude:** Must specify a single target to identify features that intersect with the latitude/longitude parameters set here. | Coordinate System: not sure? | Latitude: | Longitude: |  
| **Feature Type:** |  |  
| **Feature Name:** |  |  
| **Approval Status:** |  |  
| **Feature Diameter (km):** | Minimum | Maximum |  
| **Approval Date:** | Beginning Approval Date mm/dd/yyyy | Ending Approval Date mm/dd/yyyy |  
| **Continent:** |  |  
| **Ethnicity:** |  |  
| **Reference:** |  |  
|  | Clear | Search |
Return to top

# Planetary Names
## Advanced Nomenclature Search
#### About
*   Introduction  
*   History & References  
*   How Names are Approved  
*   IAU Working Group and Task Group Members  
*   FAQ  
*   Acknowledgements  
*   Related Resources  
*   Contact Us

# Planetary Names
## Advanced Nomenclature Search
#### Nomenclature
*   Mercury  
*   Venus  
*   The Moon  
*   Mars System  
*   Asteroids  
*   Jupiter System  
*   Saturn System  
*   Uranus System  
*   Neptune System  
*   Pluto System  
*   Ring and Ring Gap Nomenclature  
*   Planet and Satellite Names, Discoverers, and Themes

# Planetary Names
## Advanced Nomenclature Search
#### Documentation
*   IAU Rules  
*   Database Fields Descriptions  
*   Abbreviations  
*   References  
*   Surface Feature Categories (Themes)  
*   Descriptor Terms  
*   Target Coordinate Systems  
*   Help using the Website

# Planetary Names
## Advanced Nomenclature Search
#### Images and GIS Data
*   Images showing named features  
*   1:5 Million-Scale Maps of Mercury  
*   Venus 1:5 million-scale Magellan Imagery  
*   Venus 1:10 million-scale Quadrangles  
*   1:1 Million-Scale Maps of the Moon  
*   Moon 1:10 million-scale Shaded Relief and Color-coded Topography  
*   Mars 1:5 million-scale THEMIS Images  
*   GIS Downloads
</excerpt>
### Rank 5 of 290 — 0.12
<excerpt title="Nomenclature Search Results">
Anders' Earthrise	Moon	40.15	-11.73	100.47	Crater, craters	Oct 05, 2018	Crater visible in the foreground of the iconic “Earthrise” colour photograph, taken aboard Apollo 8 by W. A. Anders on December 24, 1968, showing the Earth and part of the Moon’s surface. The crater was previously designated Pasteur T.  
Anderson	Moon	105.33	15.50	170.79	Crater, craters	1970	John August; American astronomer (1876-1959).  
Andersson	Moon	13.42	-49.95	-95.46	Crater, craters	1985	Leif Erland; American astronomer (1943-1979).  
  1 - 50 of 1666 results
Download all your search results in one of the follow formats (need help?):
CSV (comma separated values) for importing into Excel
Return to top  
About  
Introduction  
History & References  
How Names are Approved  
IAU Working Group and Task Group Members  
FAQ  
Acknowledgements  
Related Resources  
Contact Us  
Nomenclature  
Mercury  
Venus  
The Moon  
Mars System  
Asteroids  
Jupiter System  
Saturn System  
Uranus System  
Neptune System  
Pluto System  
Ring and Ring Gap Nomenclature  
Planet and Satellite Names, Discoverers, and Themes  
Documentation  
IAU Rules  
Database Fields Descriptions  
Abbreviations  
References  
Surface Feature Categories (Themes)  
Descriptor Terms  
Target Coordinate Systems  
Help using the Website  
Images and GIS Data  
Images showing named features  
1:5 Million-Scale Maps of Mercury  
Venus 1:5 million-scale Magellan Imagery  
Venus 1:10 million-scale Quadrangles  
1:1 Million-Scale Maps of the Moon  
Moon 1:10 million-scale Shaded Relief and Color-coded Topography  
Mars 1:5 million-scale THEMIS Images  
GIS Downloads  
Other  
Advanced Search  
Name Request Instructions  
News

USGS Astrogeology Science Center  
The National Aeronautics and Space Administration (NASA)  
International Astronomical Union (IAU)
The Gazetteer of Planetary Nomenclature website is maintained by the USGS Astrogeology Science Center. This work is performed on behalf of the International Astronomical Union's Working Group for Planetary System Nomenclature and is supported by the National Aeronautics and Space Administration under an Interagency Agreement.
Contact Us  
Administrator Log In  
DOI Privacy Policy  
Legal  
Accessibility  
Site Map  
Contact USGS  
U.S. Department of the Interior  
DOI Inspector General  
White House  
E-gov  
No Fear Act  
FOIA  
Follow  
Twitter  
Facebook  
GitHub  
Flickr  
YouTube  
Instagram
</excerpt>

## Search 7 — query: "site:planetarynames.wr.usgs.gov "Approved 1973" "Moon" "author""
(no page could be scored)

## Search 8 — query: "site:planetarynames.wr.usgs.gov Phobos "Approved 1973""
(no page could be scored)

## Search 9 — query: "Moon feature 1973 "literary" "planetarynames.wr.usgs.gov""
### Rank 1 of 218 — 0.47 (passed on)
<excerpt title="Mercury Craters Named after Tajik-Persian Poets">
# Nomenclature as a Form of Preserving Cultural Heritage
4.  These findings may inform science -education and public outreach initiatives in Tajikistan
and may serve as a foundation for developing proposals to name additional Solar System
objects after outstanding figures of Tajik culture not yet represented in plane tary
nomenclature.
Acknowledgements
The author thanks the staff of the USGS Astrogeology Science Center for maintaining
the publicly accessible IAU Gazetteer of Planetary Nomenclature and the IAU Minor Planet
Center for open access to the MPC Orbit Database. BepiColombo is a joint ESA/JAXA
mission.
References

# Nomenclature as a Form of Preserving Cultural Heritage
> 1. Schmadel L.D. Dictionary of Minor Planet Names. 6th ed. Berlin; Heidelberg: Springer, 2012.  
> 2. Merlin J.C. The naming of minor planets: multicultural relationships // Proceedings of the  
> International Astronomical Union. 2009. Vol. 5, No. S260. Pp. 218 –224.  
> 3. El -Baz F. Al -Khwarizmi: A new -found basin on the lunar far side // Science. 1973. Vol. 180, No.  
> 4091. Pp. 1173 –1176.  
> 4. Stöffler D. et al. Cratering history and lunar chronology // Reviews in Mineralogy and  
> Geochemistry. 2006. Vol. 60, No. 1. Pp. 519 –596.  
> 5. Spain D. Alfraganus // The Six -Inch Lunar Atlas: A Pocket Field Guide. New York: Springer,  
> 2009. Pp. 79 –82.  
> 6. Bakhromzod R. Ahmad Al -Fergani and his place in the development of astronomy // Heritage of  
> Ancestors. 2022. No. 24. Pp. 36 –37. (In Tajik)  
> 7. Rozenfeld B.A., Sergeeva N.D. Ahmad al -Fergani. IX century. 1998. (In Russian)  
> 8. IAU Working Group for Planetary System Nomenclature (WGPSN). Gazetteer of Planetary  
> Nomenclature. USGS Astrogeology Research Program. URL:  
> https://planetarynames.wr.usgs.gov (accessed 15 March 2025).
15
9. Minor Planet Center (MPC). MPC Orbit Database. Smithsonian Astrophysical Observatory. URL:
https://www.minorplanetcenter.net (accessed 15 March 2025).
</excerpt>
### Rank 2 of 218 — 0.39
<excerpt title="Mercury Craters Named after Tajik-Persian Poets">
# Nomenclature as a Form of Preserving Cultural Heritage
> 1. Schmadel L.D. Dictionary of Minor Planet Names. 6th ed. Berlin; Heidelberg: Springer, 2012.  
> 2. Merlin J.C. The naming of minor planets: multicultural relationships // Proceedings of the  
> International Astronomical Union. 2009. Vol. 5, No. S260. Pp. 218 –224.  
> 3. El -Baz F. Al -Khwarizmi: A new -found basin on the lunar far side // Science. 1973. Vol. 180, No.  
> 4091. Pp. 1173 –1176.  
> 4. Stöffler D. et al. Cratering history and lunar chronology // Reviews in Mineralogy and  
> Geochemistry. 2006. Vol. 60, No. 1. Pp. 519 –596.  
> 5. Spain D. Alfraganus // The Six -Inch Lunar Atlas: A Pocket Field Guide. New York: Springer,  
> 2009. Pp. 79 –82.  
> 6. Bakhromzod R. Ahmad Al -Fergani and his place in the development of astronomy // Heritage of  
> Ancestors. 2022. No. 24. Pp. 36 –37. (In Tajik)  
> 7. Rozenfeld B.A., Sergeeva N.D. Ahmad al -Fergani. IX century. 1998. (In Russian)  
> 8. IAU Working Group for Planetary System Nomenclature (WGPSN). Gazetteer of Planetary  
> Nomenclature. USGS Astrogeology Research Program. URL:  
> https://planetarynames.wr.usgs.gov (accessed 15 March 2025).
15
9. Minor Planet Center (MPC). MPC Orbit Database. Smithsonian Astrophysical Observatory. URL:
https://www.minorplanetcenter.net (accessed 15 March 2025).
</excerpt>
### Rank 3 of 218 — 0.27
<excerpt title="The Benefits of Geographical Names Standardization">
## [PDF page 37]
NO. 49  NOVEMBER 2015
from 7 countries (South Africa 18, Zimbabwe and Slovenia  Bertie NEETHLING, Joan STEENKAMP & Theodorus DU  
2 each, USA, Brazil, Italy and Austria 1 each). Nineteen  PLESSIS, Theodorus DU PLESSIS (all South Africa), Cosimo  
papers were presented by (in the sequence of  PALAGIANO (Italy), Paulo de MENEZES (Brazil), Corrie  
presentation) Peter RAPER, Barbara MEIRING (both South  GELDENHUYS and Sibusiso NTULI (both South Africa).  
Africa), Peter JORDAN (Austria), Lucie MÖLLER, Johann  Trueman KUBHEKA (South Africa) gave a dinner speech.  
LUBBE (both South Africa), Matjaž GERŠIČ & Drago KLADNIK  
(Slovenia), Carol LOMBARD (USA), Burgert SENEKAL (South  
Africa), Tendai MANGENA & Prosper  MUZAMBI (Zimbabwe),  Peter JORDAN  
Johan Lodewyk MARAIS & Christa MORRISON, Adrian  Commission vice-chair  
KOOPMAN (all South Africa), Kizito MUCHEMWA (Zimbabwe),  Email: Peter.Jordan@oeaw.ac.at

## [PDF page 37]
In 1973 the  International Astronomical Union (IAU)  
established Working Group for Planetary System  
Nomenclature (WGPSN) which is responsible for naming  
surface features on the bodies in the  solar system. WGPSN is  
headed by a president who now is Dr. Rita Schulz from  
Germany. The undersigned is a Norwegian member of the  
working group and served between 1991 and 2006 as  
president. WGPSN selects names on the recommendations of  
six  expert groups for the Moon, Mercury, Venus, Mars, the  
outer planets,  and the small bodies (satellites, asteroids and  
comets).  More information about WGPSN and a list of all  
approved names can be found at the website  
http://planetarynames.wr.usgs.gov/.  
Pluto. Picture taken by the spacecraft New Horizons, July 2015  
Until 1970 only craters, mountains and plains on the Moon  
and some fuzzy features on Mars had received names. When  
spacecraft began to map the heavenly bodies in much detail,  
a great need for new names arose.  The custom of naming  honoring Maxwell for finding the laws of electromagnetism that  
craters and other features on the Mo  on for distinguished  made it possible to penetrate the thick atmosphere on Venus  
persons was continued and extended to other bodies.  A Latin  with radar.  On Mars the most prominent feature is  the  3000  
word is put before or after a person's name to identify the type  km long Valles Marineris  named for the spacecraft that  
of topographic or geologic feature; e.g. the mountain  Mons  mapped that valley. Jupiter's ice covered moon Callisto has  
Hansteen or the valley Vallis Bohr. Many new Latin words  received many names from Norse mythology, e.g. Valhalla  
were introduced to describe the variety of landforms  Regio, while the sulphur sputtering moon Io has borrowed  
uncovered on planets, satellites and asteroids.  names of mythological gods and creatures associated with  
volcanoes, fire, thunder and other destructive forces.  
A number of guidelines and rules have been established (see
</excerpt>
### Rank 4 of 218 — 0.24
<excerpt title="Planetary nomenclature">
## Categories for naming features on planets and satellites
| Feature type | Naming convention |  
| --- | --- |  
| Craters | Craters are generally named after deceased scientists, scholars, artists and explorers who have made outstanding or fundamental contributions to their field. Additionally, craters in or around Mare Moscoviense are named after deceased Russian cosmonauts and craters in and around Apollo crater are named after deceased American astronauts (see Space accidents and incidents). This convention may be extended if other space-faring countries suffer fatalities in spaceflight. |  
| Lacūs, Maria, Paludes, Sinūs | These features are assigned names which are Latin terms describing weather and other abstract concepts. |  
| Montes | Montes are named after terrestrial mountain ranges or nearby craters. |  
| Rupēs | Rupēs are named after nearby mountain ranges (see above). |  
| Valles | Valles are named after nearby features. |  
| Others | Features that don't fall into any of the above categories are named after nearby craters. |

## Categories for naming features on planets and satellites
### Mars and martian satellites
[edit]
Early map of Mars by Giovanni Schiaparelli, which depicts classical albedo features
| Feature type | Naming convention |  
| --- | --- |  
| Large craters | Deceased scientists who have contributed to the study of Mars; writers and others who have contributed to the lore of Mars |  
| Small craters | Villages of the world with a population of less than 100,000. |  
| Large valles | Name for Mars/star in various languages |  
| Small valles | Classical or modern names of rivers |  
| Other features | From nearest named albedo feature on Schiaparelli or Antoniadi maps. See Classical albedo features on Mars for a list. |
When space probes have landed on Mars, individual small features such as rocks, dunes, and hollows have often been given informal names. Many of these are frivolous: features have been named after ice cream (such as Cookies N Cream); cartoon characters (such as SpongeBob SquarePants and Patrick); and 1970s music acts (such as ABBA and the Bee Gees).[[7]](https://en.wikipedia.org/wiki/Planetary_nomenclature#cite_note-8)
The two named craters on Deimos
Features on Deimos are named after authors who wrote about Martian satellites. There are currently two named features on Deimos–Swift crater and Voltaire crater– after Jonathan Swift and Voltaire who predicted the presence of Martian moons.
All features on Phobos are named after scientists involved with the discovery, dynamics, or properties of the Martian satellites or people and places from Jonathan Swift's _[Gulliver's Travels](https://en.wikipedia.org/wiki/Gulliver's\_Travels "Gulliver's Travels")_.
People and places associated with the Amalthea myth.
Features on Thebe are named after people and places associated with the Thebe myth. There is only one named feature on Thebe–Zethus Crater.
</excerpt>
### Rank 5 of 218 — 0.24
<excerpt title="Planetary nomenclature">
## Categories for naming features on planets and satellites
### Mars and martian satellites
[edit]
Early map of Mars by Giovanni Schiaparelli, which depicts classical albedo features
| Feature type | Naming convention |  
| --- | --- |  
| Large craters | Deceased scientists who have contributed to the study of Mars; writers and others who have contributed to the lore of Mars |  
| Small craters | Villages of the world with a population of less than 100,000. |  
| Large valles | Name for Mars/star in various languages |  
| Small valles | Classical or modern names of rivers |  
| Other features | From nearest named albedo feature on Schiaparelli or Antoniadi maps. See Classical albedo features on Mars for a list. |
When space probes have landed on Mars, individual small features such as rocks, dunes, and hollows have often been given informal names. Many of these are frivolous: features have been named after ice cream (such as Cookies N Cream); cartoon characters (such as SpongeBob SquarePants and Patrick); and 1970s music acts (such as ABBA and the Bee Gees).[[7]](https://en.wikipedia.org/wiki/Planetary_nomenclature#cite_note-8)
The two named craters on Deimos
Features on Deimos are named after authors who wrote about Martian satellites. There are currently two named features on Deimos–Swift crater and Voltaire crater– after Jonathan Swift and Voltaire who predicted the presence of Martian moons.
All features on Phobos are named after scientists involved with the discovery, dynamics, or properties of the Martian satellites or people and places from Jonathan Swift's _[Gulliver's Travels](https://en.wikipedia.org/wiki/Gulliver's\_Travels "Gulliver's Travels")_.
People and places associated with the Amalthea myth.
Features on Thebe are named after people and places associated with the Thebe myth. There is only one named feature on Thebe–Zethus Crater.
</excerpt>

## Search 10 — query: "https://planetarynames.wr.usgs.gov/SearchResults?Approval+Date+End=1973&Approval+Date+Start=1973&Target=16_Moon"
### Rank 1 of 2464 — 0.78 (passed on)
<excerpt title="Nomenclature Search Results">
10964Lubiniezky HLubiniezky H Moon 4.29-17.01-21.21-16.94-17.08-21.14-21.28 Planetographic, +East, -180 - 180 Europe Poland Satellite Feature SFLAC-94Approved 2006[66]Stanislaus; Polish astronomer (1623-1675).Oct 18, 2010  
3503LucianLucian Moon 6.85 14.34 36.78 14.45 14.23 36.90 36.67 Planetographic, +East, -180 - 180 Europe Greek Crater, craters AALAC-61Approved 1973-Of Samosata; Greek writer (125-190).Oct 18, 2010  
3505LucretiusLucretius Moon 64.61-8.22-121.24-7.16-9.29-120.17-122.32 Planetographic, +East, -180 - 180 Europe Roman Crater, craters AALAC-89Approved 1970[182]Titus Lucretius Carus; Roman scientific philosopher (c. 94-55 B.C.).Oct 18, 2010  
10965Lucretius CLucretius C Moon 21.69-3.80-114.82-3.44-4.16-114.46-115.18 Planetographic, +East, -180 - 180 Europe Roman Satellite Feature SFLAC-89Approved 2006[182]Titus Lucretius Carus; Roman scientific philosopher (c. 94-55 B.C.).Oct 18, 2010  

10966Lucretius ULucretius U Moon 23.27-7.80-124.18-7.42-8.18-123.79-124.57 Planetographic, +East, -180 - 180 Europe Roman Satellite Feature SFLAC-89Approved 2006[182]Titus Lucretius Carus; Roman scientific philosopher (c. 94-55 B.C.).Oct 18, 2010  
3508LudwigLudwig Moon 23.29-7.72 97.45-7.34-8.11 97.84 97.07 Planetographic, +East, -180 - 180 Europe Germany Crater, craters AALAC-82Approved 1973-Carl Friedrich Wilhelm; German physiologist (1816-1895).Oct 18, 2010  
3521LundmarkLundmark Moon 103.44-38.87 152.56-37.21-40.57 154.58 150.71 Planetographic, +East, -180 - 180 Europe Sweden Crater, craters AALAC-118Approved 1970-Knut Emil; Swedish astronomer (1889-1958).Oct 18, 2010  
10967Lundmark BLundmark B Moon 37.53-37.43 153.68-36.87-37.98 154.42 152.94 Planetographic, +East, -180 - 180 Europe Sweden Satellite Feature SFLAC-118Approved 2006-Knut Emil; Swedish astronomer (1889-1958).Oct 18, 2010
</excerpt>
### Rank 2 of 2464 — 0.77
<excerpt title="Nomenclature Search Results">
10960Lubiniezky DLubiniezky D Moon 7.05-16.52-23.49-16.41-16.64-23.36-23.61 Planetographic, +East, -180 - 180 Europe Poland Satellite Feature SFLAC-94Approved 2006[66]Stanislaus; Polish astronomer (1623-1675).Oct 18, 2010  
10961Lubiniezky ELubiniezky E Moon 37.24-16.61-27.38-16.00-17.22-26.74-28.02 Planetographic, +East, -180 - 180 Europe Poland Satellite Feature SFLAC-94Approved 2006[66]Stanislaus; Polish astronomer (1623-1675).Oct 18, 2010  
10962Lubiniezky FLubiniezky F Moon 7.02-18.34-21.86-18.23-18.46-21.73-21.98 Planetographic, +East, -180 - 180 Europe Poland Satellite Feature SFLAC-94Approved 2006[66]Stanislaus; Polish astronomer (1623-1675).Oct 18, 2010  
10963Lubiniezky GLubiniezky G Moon 3.65-15.36-20.28-15.30-15.42-20.21-20.34 Planetographic, +East, -180 - 180 Europe Poland Satellite Feature SFLAC-76Approved 2006[66]Stanislaus; Polish astronomer (1623-1675).Oct 18, 2010  

10964Lubiniezky HLubiniezky H Moon 4.29-17.01-21.21-16.94-17.08-21.14-21.28 Planetographic, +East, -180 - 180 Europe Poland Satellite Feature SFLAC-94Approved 2006[66]Stanislaus; Polish astronomer (1623-1675).Oct 18, 2010  
3503LucianLucian Moon 6.85 14.34 36.78 14.45 14.23 36.90 36.67 Planetographic, +East, -180 - 180 Europe Greek Crater, craters AALAC-61Approved 1973-Of Samosata; Greek writer (125-190).Oct 18, 2010  
3505LucretiusLucretius Moon 64.61-8.22-121.24-7.16-9.29-120.17-122.32 Planetographic, +East, -180 - 180 Europe Roman Crater, craters AALAC-89Approved 1970[182]Titus Lucretius Carus; Roman scientific philosopher (c. 94-55 B.C.).Oct 18, 2010  
10965Lucretius CLucretius C Moon 21.69-3.80-114.82-3.44-4.16-114.46-115.18 Planetographic, +East, -180 - 180 Europe Roman Satellite Feature SFLAC-89Approved 2006[182]Titus Lucretius Carus; Roman scientific philosopher (c. 94-55 B.C.).Oct 18, 2010
</excerpt>
### Rank 3 of 2464 — 0.76
<excerpt title="Nomenclature Search Results">
5451ShahinazShahinaz Moon 15.99 7.58 122.42 7.84 7.32 122.64 122.20 Planetographic, +East, -180 - 180 Asia Turkey Crater, craters AALAC-65Approved 1979-Turkish female name.Oct 18, 2010  
5455ShakespeareShakespeare Moon 0.54 20.24 30.82 20.25 20.23 30.83 30.81 Planetographic, +East, -180 - 180 Europe Great Britain Astronaut-named features LFLAC-43Approved 1973[59]Astronaut-named feature, Apollo 17 site.None Oct 25, 2010  
5461ShalerShaler Moon 48.47-32.89-85.27-32.18-33.61-84.32-86.22 Planetographic, +East, -180 - 180 North America American Crater, craters AALAC-109Approved 1964[89]Nathaniel Southgate; American geologist, paleontologist (1841-1906).Oct 18, 2010  
5468ShapleyShapley Moon 24.82 9.35 56.83 9.76 8.94 57.25 56.42 Planetographic, +East, -180 - 180 North America American Crater, craters AALAC-62Approved 1973-Harlow; American astronomer (1885-1972).Oct 18, 2010  

5469SharonovSharonov Moon 75.12 12.37 173.10 13.61 11.13 174.37 171.83 Planetographic, +East, -180 - 180 Europe Soviet Crater, craters AALAC-68Approved 1970[89]Vsevolod Vasilievich; Soviet astronomer (1901-1964).Oct 18, 2010  
13056Sharonov DSharonov D Moon 16.35 13.40 175.15 13.67 13.13 175.42 174.87 Planetographic, +East, -180 - 180 Europe Soviet Satellite Feature SFLAC-68Approved 2006[89]Vsevolod Vasilievich; Soviet astronomer (1901-1964).Oct 18, 2010  
13057Sharonov FSharonov F Moon 13.37 12.26 175.92 12.48 12.04 176.15 175.70 Planetographic, +East, -180 - 180 Europe Soviet Satellite Feature SFLAC-68Approved 2006[89]Vsevolod Vasilievich; Soviet astronomer (1901-1964).Oct 18, 2010  
13058Sharonov XSharonov X Moon 42.66 13.86 172.47 14.56 13.15 173.20 171.75 Planetographic, +East, -180 - 180 Europe Soviet Satellite Feature SFLAC-68Approved 2006[89]Vsevolod Vasilievich; Soviet astronomer (1901-1964).Oct 18, 2010
</excerpt>
### Rank 4 of 2464 — 0.69
<excerpt title="Nomenclature Search Results">
13054Seneca GSeneca G Moon 20.66 29.48 83.23 29.82 29.14 83.62 82.84 Planetographic, +East, -180 - 180 Europe Roman Satellite Feature SFLAC-45Approved 2006[67]Lucius Annaeus; Roman philosopher, natural scientist (4 B.C.- A.D. 65).Oct 18, 2010  
5446SeyfertSeyfert Moon 102.63 29.26 114.34 30.96 27.57 116.27 112.40 Planetographic, +East, -180 - 180 North America American Crater, craters AALAC-47Approved 1970-Carl Keenan; American astronomer (1911-1960).Oct 18, 2010  
13055Seyfert ASeyfert A Moon 51.97 30.56 115.08 31.38 29.74 116.07 114.08 Planetographic, +East, -180 - 180 North America American Satellite Feature SFLAC-47Approved 2006-Carl Keenan; American astronomer (1911-1960).Oct 18, 2010  
5450ShackletonShackleton Moon 20.92-89.67 129.78-89.32-90.00-148.70 48.29 Planetographic, +East, -180 - 180 Europe Great Britain Crater, craters AALAC-144Approved 1994[68]Sir Ernest Henry; Irish-born British Antarctic explorer (1874-1922).Oct 04, 2023  

5451ShahinazShahinaz Moon 15.99 7.58 122.42 7.84 7.32 122.64 122.20 Planetographic, +East, -180 - 180 Asia Turkey Crater, craters AALAC-65Approved 1979-Turkish female name.Oct 18, 2010  
5455ShakespeareShakespeare Moon 0.54 20.24 30.82 20.25 20.23 30.83 30.81 Planetographic, +East, -180 - 180 Europe Great Britain Astronaut-named features LFLAC-43Approved 1973[59]Astronaut-named feature, Apollo 17 site.None Oct 25, 2010  
5461ShalerShaler Moon 48.47-32.89-85.27-32.18-33.61-84.32-86.22 Planetographic, +East, -180 - 180 North America American Crater, craters AALAC-109Approved 1964[89]Nathaniel Southgate; American geologist, paleontologist (1841-1906).Oct 18, 2010  
5468ShapleyShapley Moon 24.82 9.35 56.83 9.76 8.94 57.25 56.42 Planetographic, +East, -180 - 180 North America American Crater, craters AALAC-62Approved 1973-Harlow; American astronomer (1885-1972).Oct 18, 2010
</excerpt>
### Rank 5 of 2464 — 0.63
<excerpt title="Nomenclature Search Results">
883BrisbaneBrisbane Moon 44.32-49.20 68.76-48.47-49.93 69.88 67.64 Planetographic, +East, -180 - 180 Europe Scotland Crater, craters AALAC-128Approved 1935[68]Sir Thomas Makdougall; Scottish astronomer (1773-1860).Oct 18, 2010  
7953Brisbane EBrisbane E Moon 57.35-50.26 71.41-49.32-51.21 72.89 69.93 Planetographic, +East, -180 - 180 Europe Scotland Satellite Feature SFLAC-129Approved 2006[68]Sir Thomas Makdougall; Scottish astronomer (1773-1860).Oct 18, 2010  
7954Brisbane HBrisbane H Moon 43.70-50.37 65.12-49.66-51.07 65.95 64.28 Planetographic, +East, -180 - 180 Europe Scotland Satellite Feature SFLAC-128Approved 2006[68]Sir Thomas Makdougall; Scottish astronomer (1773-1860).Oct 18, 2010  
7955Brisbane XBrisbane X Moon 20.07-50.58 67.98-50.25-50.92 68.50 67.46 Planetographic, +East, -180 - 180 Europe Scotland Satellite Feature SFLAC-128Approved 2006[68]Sir Thomas Makdougall; Scottish astronomer (1773-1860).Oct 18, 2010  

7956Brisbane YBrisbane Y Moon 16.11-51.47 70.17-51.21-51.74 70.60 69.74 Planetographic, +East, -180 - 180 Europe Scotland Satellite Feature SFLAC-129Approved 2006[68]Sir Thomas Makdougall; Scottish astronomer (1773-1860).Oct 18, 2010  
7957Brisbane ZBrisbane Z Moon 64.73-52.89 72.82-51.83-53.96 74.59 71.06 Planetographic, +East, -180 - 180 Europe Scotland Satellite Feature SFLAC-129Approved 2006[68]Sir Thomas Makdougall; Scottish astronomer (1773-1860).Oct 18, 2010  
887BronkBronk Moon 66.16 25.90-134.67 26.99 24.81-133.46-135.88 Planetographic, +East, -180 - 180 North America American Crater, craters AALAC-52Approved 1979[68]Detlev Wulf; American neurophysiologist (1897-1975).Oct 18, 2010  
889BrontëBronte Moon 0.21 20.17 30.67 20.18 20.17 30.68 30.67 Planetographic, +East, -180 - 180 North America American Astronaut-named features LFLAC-43Approved 1973[60]Astronaut-named feature, Apollo 17 site.None Oct 25, 2010
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
According to the UNdata website, out of India, Pakistan, Nepal, Bhutan, and Bangladesh, which countries had an increase in the percentage of their workforce being unemployed between 2015 and 2020, when rounded to one decimal place?

## Expected answer
Pakistan, Nepal, Bhutan, Bangladesh

## Grade 0.00

## Search 1 — query: "UNdata unemployment rate India 2015 2020"
### Rank 1 of 86 — 0.24 (passed on)
<excerpt title="Impact of COVID−19 Lockdown on Unemployment in India−A before, ...">
### Results And Discussion Related To Urban Unemployment Rate
| Table 7 Monthly Urban Unemployment Rate In India (In %) |  
| --- |  
| Year / Month | Jan | Feb | Mar | Apr | May | June | July | Aug | Sep | Oct | Nov | Dec |  
| 2016 | 10.44 | 10.38 | 11.56 | 11.22 | 12.1 | 10.27 | 11.12 | 11.17 | 9.76 | 7.6 | 7.62 | 7.63 |  
| 2017 | 7.67 | 6.38 | 5.78 | 4.19 | 4.85 | 4.84 | 4.14 | 5.08 | 5.7 | 5.98 | 5.41 | 5.36 |  
| 2018 | 6.24 | 6.59 | 6.1 | 6.19 | 6.18 | 6.64 | 6.15 | 6.72 | 7.38 | 7.12 | 7.33 | 7.48 |  
| 2019 | 8.58 | 7.69 | 7.72 | 7.57 | 8.58 | 8.26 | 8.3 | 9.71 | 9.58 | 8.27 | 8.88 | 9.02 |  
| 2020 | 9.7 | 8.65 | 9.41 | **_24.95_** | **_23.14_** | **_11.68_** | **_9.37_** | **_9.83_** | **_8.45_** | **_7.18_** | **_7.07_** | **_8.84_** |
</excerpt>
### Rank 2 of 86 — 0.20
<excerpt title="Impact of COVID−19 Lockdown on Unemployment in India−A before, ...">
### Results and Discussion
This section is divided into three sections by taking each type of unemployment rate series at one time. The three series that are considered in the study are; (i) Total Unemployment Rate in %, (ii) Rural Unemployment Rate in %, (iii) Urban Unemployment Rate in %

### Results and Discussion Related To Total Unemployment Rate
Data collected from Centre for Monitoring Indian Economy (CMIE) related to total unemployment rate (%) in India is given below **Table 1**.
| Table 1 Monthly Total Unemployment Rate In India (In %) |  
| --- |  
| Year / Month | Jan | Feb | Mar | Apr | May | June | July | Aug | Sep | Oct | Nov | Dec |  
| **2016** | 8.72 | 8.46 | 8.73 | 8.9 | 9.65 | 8.91 | 8.51 | 9.59 | 8.43 | 6.71 | 6.51 | 6.4 |  
| **2017** | 5.93 | 5.01 | 4.67 | 3.87 | 4.03 | 4.12 | 3.37 | 4.07 | 4.63 | 5 | 4.72 | 4.74 |  
| **2018** | 5.01 | 5.87 | 6 | 5.57 | 5.14 | 5.75 | 5.66 | 6.27 | 6.47 | 6.83 | 6.65 | 7.02 |  
| **2019** | 6.86 | 7.2 | 6.65 | 7.35 | 7.03 | 7.87 | 7.34 | 8.19 | 7.14 | 8.1 | 7.23 | 7.6 |  
| **2020** | 7.22 | 7.76 | 8.75 | **_23.52_** | **_21.73_** | **_10.18_** | **_7.4_** | **_8.35_** | **_6.68_** | **_7.02_** | **_6.5_** | **_9.06_** |  

### Results and Discussion Related To Total Unemployment Rate
| **2021** | **_6.52_** | **_6.89_** | **_6.5_** | **_7.97_** | **_11.84_** | **_9.17_** | 6.96 | 8.32 | 6.86 | 7.74 | 6.97 | 7.91 |  
| **2022** | 6.56 | 8.11 | 7.57 | 7.83 | 7.14 | 7.83 | 6.83 | 8.28 | 6.43 | 7.92 | 8.03 | 8.3 |
As mentioned in the research methodology section, the data set is divided into three phases i.e. (i) Before the Lockdown Phase (ii) During the Lockdown Phase, and (iii) After the Lockdown Phase. The highest and lowest total unemployment rates in before the lockdown phase are 9.65% and 3.37%.During the lockdown phase, the highest and lowest total unemployment rates observed are 23.52% and 6.5%.
However, the highest and lowest total unemployment rates recorded after the lockdown phase in India are 8.32% and 6.56%. On calculation, the mean total unemployment rate for before, during and after the lockdown phases are found to be 6.63%, 9.95% and 7.53% respectively. The data related to these phases are tested for their normality and homogeneity of variances and the results are tabulated below **Table 2**.
</excerpt>
### Rank 3 of 86 — 0.17
<excerpt title="Unemployment rate in India from 1991 to 2025">
# Unemployment rate in India from 1991 to 2025
Unemployment rate in India 1991-2025
Ask AI
Last update: Feb 25, 2026
Region: India
Statista Research Department
Survey time period: 1999 to 2024
Switch chart type
Line
Column
Table
All categories
Download
Line chart with 35 data points.
View as data table, Chart
The chart has 1 X axis displaying categories.
The chart has 1 Y axis displaying Unemployment rate. Data ranges from 4.17 to 7.86.
1991 1993 1995 1997 1999 2001 2003 2005 2007 2009 2011 2013 2015 2017 2019 2021 2023 2025
4 5 6 7 8 9
7.64%
7.65%
7.66%
7.59%
7.57%
7.54%
7.57%
7.6%
7.58%
7.59%
7.61%
7.68%
7.63%
7.6%
7.55%
7.55%
7.56%
7.63%
7.64%
7.63%
7.61%
7.65%
7.68%
7.66%
7.63%
7.61%
7.63%
7.65%
6.51%
7.86%
6.38%
4.82%
4.17%
4.17%
4.22%
End of interactive chart.
India's annual unemployment rate in 2025 was estimated to be 4.22 percent in 2025, compared with 4.17 percent in the previous year.
</excerpt>
### Rank 4 of 86 — 0.14
<excerpt title="Impact of COVID−19 Lockdown on Unemployment in India−A before, ...">
### Results And Discussion Related To Urban Unemployment Rate
Data collected from Centre for Monitoring Indian Economy (CMIE) related to urban unemployment rate (%) in India is given below **Table 7**.
This dataset is also divided into three phases i.e. (i) Before the Lockdown Phase (ii) During the Lockdown Phase, and (iii) After the Lockdown Phase. The highest and lowest urban unemployment rates in before the lockdown phase are 12.1% and 4.14%.During the lockdown phase, the highest and lowest rural unemployment rates observed are 24.95% and 6.99%. However, the highest and lowest rural unemployment rates recorded after the lockdown phase in India are 10.09% and 7.32%.

### Results And Discussion Related To Urban Unemployment Rate
| Table 7 Monthly Urban Unemployment Rate In India (In %) |  
| --- |  
| Year / Month | Jan | Feb | Mar | Apr | May | June | July | Aug | Sep | Oct | Nov | Dec |  
| 2016 | 10.44 | 10.38 | 11.56 | 11.22 | 12.1 | 10.27 | 11.12 | 11.17 | 9.76 | 7.6 | 7.62 | 7.63 |  
| 2017 | 7.67 | 6.38 | 5.78 | 4.19 | 4.85 | 4.84 | 4.14 | 5.08 | 5.7 | 5.98 | 5.41 | 5.36 |  
| 2018 | 6.24 | 6.59 | 6.1 | 6.19 | 6.18 | 6.64 | 6.15 | 6.72 | 7.38 | 7.12 | 7.33 | 7.48 |  
| 2019 | 8.58 | 7.69 | 7.72 | 7.57 | 8.58 | 8.26 | 8.3 | 9.71 | 9.58 | 8.27 | 8.88 | 9.02 |  
| 2020 | 9.7 | 8.65 | 9.41 | **_24.95_** | **_23.14_** | **_11.68_** | **_9.37_** | **_9.83_** | **_8.45_** | **_7.18_** | **_7.07_** | **_8.84_** |
</excerpt>
### Rank 5 of 86 — 0.13
<excerpt title="Impact of COVID−19 Lockdown on Unemployment in India−A before, ...">
### Results And Discussion Related To Rural Unemployment Rate
Data collected from Centre for Monitoring Indian Economy (CMIE) related to rural unemployment rate (%) in India is given below **Table 4**.

### Results And Discussion Related To Rural Unemployment Rate
| Table 4 Monthly Rural Unemployment Rate In India (In %) |  
| --- |  
| Year / Month | Jan | Feb | Mar | Apr | May | June | July | Aug | Sep | Oct | Nov | Dec |  
| 2016 | 7.92 | 7.55 | 7.36 | 7.79 | 8.52 | 8.26 | 7.22 | 8.85 | 7.82 | 6.29 | 5.96 | 5.82 |  
| 2017 | 5.11 | 4.35 | 4.14 | 3.72 | 3.65 | 3.78 | 3.01 | 3.59 | 4.13 | 4.52 | 4.39 | 4.46 |  
| 2018 | 4.43 | 5.53 | 5.95 | 5.29 | 4.65 | 5.32 | 5.42 | 6.06 | 6.05 | 6.69 | 6.32 | 6.8 |  
| 2019 | 6.05 | 6.97 | 6.15 | 7.25 | 6.3 | 7.69 | 6.9 | 7.48 | 5.99 | 8.02 | 6.45 | 6.93 |  
| 2020 | 6.06 | 7.34 | 8.44 | **_22.89_** | **_21.11_** | **_9.49_** | **_6.51_** | **_7.65_** | **_5.88_** | **_6.95_** | **_6.24_** | **_9.15_** |  

### Results And Discussion Related To Rural Unemployment Rate
| 2021 | **_5.81_** | **_6.85_** | **_6.15_** | **_7.13_** | **_10.55_** | **_8.75_** | 6.34 | 7.64 | 6.04 | 7.91 | 6.41 | 7.28 |  
| 2022 | 5.83 | 8.37 | 7.24 | 7.18 | 6.63 | 8.07 | 6.17 | 7.68 | 5.83 | 8.19 | 7.61 | 7.44 |
This dataset is also divided into three phases i.e. (i) Before the Lockdown Phase (ii) During the Lockdown Phase, and (iii) After the Lockdown Phase. The highest and lowest rural unemployment rates in before the lockdown phase are 8.85% and 3.01%.During the lockdown phase, the highest and lowest rural unemployment rates observed are 22.89% and 5.81%.
However, the highest and lowest rural unemployment rates recorded after the lockdown phase in India are 8.37% and 5.83%. On calculation, the mean rural unemployment rate for before, during and after the lockdown phases are found to be 6.09%, 9.40% and 7.10% respectively. The data related to these phases are tested for their normality and homogeneity of variances and the results are tabulated below **Table 5**.
</excerpt>

## Search 2 — query: "UNdata unemployment total India 2015"
### Rank 1 of 69 — 0.19 (passed on)
<excerpt title="Unemployment rate in India from 1991 to 2025">
# Unemployment rate in India from 1991 to 2025
Unemployment rate in India 1991-2025
Ask AI
Last update: Feb 25, 2026
Region: India
Statista Research Department
Survey time period: 1999 to 2024
Switch chart type
Line
Column
Table
All categories
Download
Line chart with 35 data points.
View as data table, Chart
The chart has 1 X axis displaying categories.
The chart has 1 Y axis displaying Unemployment rate. Data ranges from 4.17 to 7.86.
1991 1993 1995 1997 1999 2001 2003 2005 2007 2009 2011 2013 2015 2017 2019 2021 2023 2025
4 5 6 7 8 9
7.64%
7.65%
7.66%
7.59%
7.57%
7.54%
7.57%
7.6%
7.58%
7.59%
7.61%
7.68%
7.63%
7.6%
7.55%
7.55%
7.56%
7.63%
7.64%
7.63%
7.61%
7.65%
7.68%
7.66%
7.63%
7.61%
7.63%
7.65%
6.51%
7.86%
6.38%
4.82%
4.17%
4.17%
4.22%
End of interactive chart.
India's annual unemployment rate in 2025 was estimated to be 4.22 percent in 2025, compared with 4.17 percent in the previous year.

# Unemployment rate in India from 1991 to 2025
**India's economy in comparison to other BRIC states**
India possesses one of the fastest-growing economies in the world and as a result, India is recognized as one of the G-20 major economies as well as a member of the BRIC countries, an association that is made up of rapidly growing economies. As well as India, three other countries, namely Brazil, Russia and China, are BRIC members. India’s manufacturing industry plays a large part in the development of its economy; however its services industry is the most significant economical factor. The majority of the population of India works in this sector. India’s notable economic boost can be attributed to significant gains over the past decade in regards to the efficiency of the production of goods as well as maintaining relatively low debt, particularly when compared to the total amount earned from goods and services produced throughout the years.
When considering individual development as a country, India progressed significantly over the years. However, in comparison to the other emerging countries in the BRIC group, India’s progress was rather minimal. While China experienced the most apparent growth, India’s efficiency and productivity remained somewhat stagnant over the course of 3 or 4 years. India also reported a rather large trade deficit over the past decade, implying that its total imports exceeded its total amount of exports, essentially forcing the country to borrow money in order to finance the nation. Most economists consider trade deficits a negative factor, especially in the long run and for developing or emerging countries.
* * *
Source link:worldbank.orgRegion:India
Details Share Copy data Copy for AI
Problem with the data?Report a problemorNotice of copyright infringement
</excerpt>
### Rank 2 of 69 — 0.12
<excerpt title="India Unemployment Rate">
# India Unemployment Rate
*
CalendarNews
Markets
*   Commodities  
*   Indexes  
*   Shares  
*   Currencies  
*   Crypto  
*   Bonds  
*   Earnings
IndicatorsCountries
Forecasts
*   Commodities  
*   Indexes  
*   Currencies  
*   Crypto  
*   Bonds  
*   Countries  
*   Indicators

  
*
**DATA PLANS** Download historical data for 20 million indicators using your browser.
Subscription Plans|Features
**API GATEWAY** Direct access to our data from your apps using any programing language.
Features|Docs|Developer
Already a user? **Login**
Light Dark System
Notifications Alerts for major calendar releases, even when this tab is minimised or in the background.
Calendar
News
Markets
*   Commodities  
*   Indexes  
*   Shares  
*   Currencies  
*   Crypto  
*   Bonds  
*   Earnings  
*   Holidays
Countries
*   United States  
*   United Kingdom  
*   Euro Area  
*   Australia  
*   Canada  
*   Japan  
*   China  
*   Brazil  
*   Russia  
*   India  
*   More Countries
Indicators
*   Interest Rate  
*   Inflation Rate  
*   Unemployment Rate  
*   GDP Growth  
*   GDP per Capita  
*   Current Account  
*   Gold Reserves  
*   Government Debt  
*   Crude Oil Production  
*   Gasoline Prices  
*   Credit Rating  
*   More Indicators
Forecasts
*   Markets & Indicators  
*   Countries  
*   Countries  
*   Indicators  
*   Commodities  
*   Indexes  
*   Currencies  
*   Crypto  
*   Bonds
Solutions
*   Data Subscriptions  
*   API Access  
*   Pricing
Apps
*   App Store  
*   Google Play  
*   Twitter
About
*   Customers  
*   Investors  
*   Careers  
*   About us  
*   Contact
*   Summary  
*   Stats  
*   Forecast  
*   Consensus  
*   Calendar  
*   Alerts  
*   Download  
    *   Download Data  
    *   Excel Add-in  
    *   API Access

# India Unemployment Rate
## The Indian unemployment rate tell to 4.9% in October of 2026 from 5.0% in the previous month, the lowest since February, and below the median market consensus that it would rise to 5.1%. The improvement was evidence of resilience in the Indian labor market as soaring energy prices and a weak rupee elevated consumer inflation to a three-year high in the period, driving the Reserve Bank of India to raise its benchmark policy rate. The urban unemployment rate fell to 6.7% form 6.9%, the first drop since May, while the rural unemployment rate was unchanged at 4.2%. The reduction in the unemployment rate took place in tandem with an increase in the labor force participation rate (55.7% vs 55.5% in September), the highest since February. source: Ministry of Statistics and Programme Implementation (MOSPI)
## Unemployment Rate in India decreased to 4.90 percent in October from 5 percent in September of 2026. Unemployment Rate in India averaged 7.33 percent from 2018 until 2026, reaching an all time high of 20.80 percent in June of 2020 and a record low of 4.70 percent in November of 2025. This page provides - India Unemployment Rate - actual values, historical data, forecast, chart, statistics, economic calendar and news. India Unemployment Rate - data, historical chart, forecasts and calendar of releases - was last updated on November of 2026.
</excerpt>
### Rank 3 of 69 — 0.10
<excerpt title="India Unemployment Rate">
# India Unemployment Rate
## The Indian unemployment rate tell to 4.9% in October of 2026 from 5.0% in the previous month, the lowest since February, and below the median market consensus that it would rise to 5.1%. The improvement was evidence of resilience in the Indian labor market as soaring energy prices and a weak rupee elevated consumer inflation to a three-year high in the period, driving the Reserve Bank of India to raise its benchmark policy rate. The urban unemployment rate fell to 6.7% form 6.9%, the first drop since May, while the rural unemployment rate was unchanged at 4.2%. The reduction in the unemployment rate took place in tandem with an increase in the labor force participation rate (55.7% vs 55.5% in September), the highest since February. source: Ministry of Statistics and Programme Implementation (MOSPI)
## Unemployment Rate in India decreased to 4.90 percent in October from 5 percent in September of 2026. Unemployment Rate in India averaged 7.33 percent from 2018 until 2026, reaching an all time high of 20.80 percent in June of 2020 and a record low of 4.70 percent in November of 2025. This page provides - India Unemployment Rate - actual values, historical data, forecast, chart, statistics, economic calendar and news. India Unemployment Rate - data, historical chart, forecasts and calendar of releases - was last updated on November of 2026.

# India Unemployment Rate
### Unemployment Rate in India decreased to 4.90 percent in October from 5 percent in September of 2026. Unemployment Rate in India is expected to be 5.50 percent by the end of this quarter, according to Trading Economics global macro models and analysts expectations. In the long-term, the India Unemployment Rate is projected to trend around 5.40 percent in 2027, according to our econometric models.
%
1Y3Y5Y10YMAX
Export
API
OK
*   

*   

*   

*   

*   

*
Loading...
Nov Dec 2026 Feb Mar Apr May Jun Jul Aug Sep Oct
Ministry of Statistics and Programme Implementation (MOSPI)
Value Chg
What will the Nov 2026 Unemployment Rate be versus the prior 4.9%?
Below Same Above
| Calendar | GMT | Reference | Actual | Previous | Consensus | TEForecast |  
| --- | --- | --- | --- | --- | --- | --- |  
| 2026-10-15 | 10:30 AM | Unemployment Rate | Sep | 5% | 5% | 5.2% | 5.20% |  
| 2026-11-16 | 10:30 AM | Unemployment Rate | Oct | 4.9% | 5% | 5.1% | 5.1% |  
| 2026-12-15 | 10:30 AM | Unemployment Rate | Nov |  | 4.9% |  |  |
</excerpt>
### Rank 4 of 69 — 0.10
<excerpt title="Unemployment rate in India from 1991 to 2025">
# Unemployment rate in India from 1991 to 2025
## Related insights
Number of employed persons in India from financial year 2018 to 2025 in millions Line chart with 3 data points. View as data table, Chart The chart has 1 X axis displaying categories. The chart has 1 Y axis displaying values. Data ranges from 811.97 to 913.33. FY 2018 FY 2019 FY 2020 End of interactive chart. * * * Visit the full version Preview
Unemployment rate in the United States from 1991 to 2025 * * * PREVIEW
Attrition rate in India from 2009 to 2025 * * * PREVIEW
Unemployment rate in Poland from 1991 to 2025 * * * PREVIEW
Rate of unemployment in rural and urban India in financial year 2025, by gender * * * PREVIEW
Employment rate in India from financial year 2017 to 2024, by religion * * * PREVIEW
Perceived and actual unemployment rate among working age population in India as of October 2018 * * * PREVIEW
Unemployment rate in Bangladesh from 1991 to 2025 * * * PREVIEW
Unemployment rate in India from financial year 2017 to 2024, by religion * * * PREVIEW
Unemployment rate in Brazil from 1991 to 2025 * * * PREVIEW
Unemployment rate in Japan from 1991 to 2025 * * * PREVIEW
Unemployment rate in Brazil from 1991 to 2031 * * * PREVIEW
Unemployment rate in France from 1991 to 2025 * * * PREVIEW
Unemployment rate in Delhi in India from financial year 2021 to 2024, by gender * * * PREVIEW
Distribution of employment across India from 2021 to 2025, by employment type * * * PREVIEW
Rate of unemployment in urban India in financial year 2025, by state and union territory * * * PREVIEW
</excerpt>
### Rank 5 of 69 — 0.07
<excerpt title="India Unemployment Rate">
# India Unemployment Rate
## GDP
Fiscal Year GDP Growth
GDP
GDP Constant Prices
GDP from Agriculture
GDP from Construction
GDP from Manufacturing
GDP from Mining
GDP from Public Administration
GDP from Utilities
GDP Growth Rate
GDP Growth Rate YoY
GDP per Capita
GDP per Capita PPP
Gross Fixed Capital Formation
Gross National Product

# India Unemployment Rate
## Labour
Employment Rate
Labor Force Participation Rate
Minimum Wages
Population
Retirement Age Men
Retirement Age Women
Unemployment Rate
Wages

# India Unemployment Rate
## Prices
Consumer Food Price Index (CFPI)
Consumer Price Index CPI
CPI Clothing and Footwear
CPI Education Services
CPI Housing and Utilities
CPI Recreation, Sport and Culture
CPI Restaurants and Accommodation Services
CPI Transport
Export Prices
Food Inflation
Import Prices
Inflation Expectations
Inflation Rate MoM
Inflation Rate YoY
Producer Prices
Producer Prices MoM
Producer Prices YoY
Wholesale Price Index
Wholesale Prices MoM
Wholesale Prices YoY
WPI Food Index YoY
WPI Fuel YoY
WPI Manufacturing YoY

# India Unemployment Rate
## Money
Bank Loan Growth YoY
Cash Reserve Ratio
Central Bank Balance Sheet
Foreign Exchange Reserves
Interbank Rate
M3 Money Supply YoY
Money Supply M0
Money Supply M1
Money Supply M2
RBI Interest Rate
Reverse Repo Rate

# India Unemployment Rate
## Trade
Balance of Trade
Capital Flows
Crude Oil Production
Current Account
Current Account to GDP
Exports
Exports by Category
Exports by Country
External Debt
Foreign Direct Investment
Gold Reserves
Imports
Imports by Category
Imports by Country
Remittances
Terms of Trade
Terrorism Index
Tourist Arrivals
Weapons Sales

# India Unemployment Rate
## Government
Corruption Index
Corruption Rank
Credit Rating
Fiscal Expenditure
Government Budget
Government Budget Value
Government Debt to GDP
Government Revenues
Government Spending
Government Spending to GDP
Holidays
Military Expenditure

# India Unemployment Rate
## Business
Business Confidence
Capacity Utilization
Car Production
Car Sales
Changes in Inventories
Composite Leading Indicator
Deposit Growth YoY
Electricity Production
Industrial Production Mom
Industrial Production YoY
Manufacturing Production YoY
Mining Production
Passenger Vehicle Sales
Steel Production

# India Unemployment Rate
## Consumer
Bank Lending Rate
Consumer Confidence
Consumer Spending
Disposable Personal Income
Gasoline Prices
Households Debt to GDP
Retail Sales YoY

# India Unemployment Rate
## Housing
Housing Index
Infrastructure Output YoY
Residential Property Prices

# India Unemployment Rate
## Taxes
Corporate Tax Rate
Personal Income Tax Rate
Sales Tax Rate
Social Security Rate
Social Security Rate For Companies
Social Security Rate For Employees
Withholding Tax Rate

# India Unemployment Rate
## Health
Hospital Beds
</excerpt>

## Search 3 — query: "UNdata unemployment India 2015 2020 "Unemployment, total (% of total labour force)""
(no page could be scored)

## Search 4 — query: "UNdata "Unemployment, total (% of total labour force)" India 2015"
(no page could be scored)

## Search 5 — query: "UNdata unemployment Pakistan 2015 total labour force"
### Rank 1 of 71 — 0.27 (passed on)
<excerpt title="Unemployment & Youth Joblessness in Pakistan">
**Rising Unemployment and Youth Joblessness in Pakistan: Structural Challenges and Gender Disparities in the Labor Market**
_Islamabad, February13 th, 2026_
Drawing on the latest _Pakistan Labor Force Survey 2024–25_ published by the Pakistan Bureau of Statistics (PBS), this edition of Gallup Pakistan’s Big Data Analysis series examines how Pakistan’s labor force participation has evolved over the last four years. With the labor force expanding from 71.8 million in 2020–21 to 85.6 million in 2024–25, participation rates have risen nationwide, driven significantly by women and rural populations. The results highlight both progress and persistent structural inequalities in Pakistan’s labor market. (All labor market figures are based on the 13th ICLS framework unless otherwise specified.)
**Key Findings:**
1.   Pakistan’s unemployment rate increased from 6.3% to 6.9% between 2020–21 and 2024–25, with women and youth experiencing the highest levels of joblessness.
*   Female unemployment rose to 9.7%, almost four percentage points higher than men.  
*   Youth unemployment (15–24 years) stands at 12.5%, with young women exceeding 13%, signaling structural barriers to entry.  
*   Urban unemployment remains substantially higher (8.0%) than rural (6.3%), with urban women facing as much as 17–18% unemployment.  
*   Underemployment is low at 1.6%, but higher among women, reflecting limited access to adequate working hours.

*   Trends since 2015 suggest job creation has slowed relative to population and labor force growth, intensifying youth competition for fewer quality jobs.
</excerpt>
### Rank 2 of 71 — 0.14
<excerpt title="Youth Unemployment Rate for Pakistan (SLUEM1524ZSPAK)">
# Youth Unemployment Rate for Pakistan (SLUEM1524ZSPAK)
#### Add the minimum, maximum, and average calculations of selected bars to the graph
##### Bar 1
###### Line details & color
Line style, thickness, color and position
Customize
Line style
Width
Color
Mark type
Width
Y-Axis position
Left
Right
Bottom

# Youth Unemployment Rate for Pakistan (SLUEM1524ZSPAK)
#### Add the minimum, maximum, and average calculations of selected bars to the graph
##### Bar 2
###### Youth Unemployment Rate for Pakistan Vintage: 2026-02-25


# Youth Unemployment Rate for Pakistan (SLUEM1524ZSPAK)
#### Add the minimum, maximum, and average calculations of selected bars to the graph
##### Bar 2
###### Line details & color
Line style, thickness, color and position
Customize
Line style
Width
Color
Mark type
Width
Y-Axis position
Left
Right
Bottom
Fullscreen
**Data in this graph are copyrighted. Please review the copyright information in the series notes before sharing.**
Share Graph
*   Custom Graph Link  
*   Embed in Website  
*   Graph Image Link

# Youth Unemployment Rate for Pakistan (SLUEM1524ZSPAK)
## Notes
**Title****Release Dates**
* * *
Youth Unemployment Rate for Pakistan 2015-12-22 2026-02-25
**Source**
* * *
World Bank2015-12-22 2026-02-25
**Release**
* * *
World Development Indicators2015-12-22 2026-02-25
**Units**
* * *
Percent 2015-12-22 2026-02-25
**Frequency**
* * *
Annual 2015-12-22 2026-02-25
**Seasonal Adjustment**
* * *
Not Seasonally Adjusted 2015-12-22 2026-02-25
**Notes**
* * *
Youth unemployment refers to the share of the labor force ages 15-24 without work but available for and seeking employment (modeled ILO estimate).
Source Indicator: SL.UEM.1524.ZS 2015-12-22 2026-02-25

# Youth Unemployment Rate for Pakistan (SLUEM1524ZSPAK)
## Release Tables


# Youth Unemployment Rate for Pakistan (SLUEM1524ZSPAK)
## Related Data and Content
### Data Suggestions Based On Your Search
**Inflation, consumer prices for Pakistan**
**Employment to Population Ratio for Pakistan**
**Consumer Price Index for Pakistan**
**Gross Domestic Product for Pakistan**
**Population Growth for Pakistan**
**Consumer Price Inflation for Pakistan**
**Gross Domestic Product for Bahamas**
**Literacy Rate, Adult Total for Pakistan**
See More...
* * *

# Youth Unemployment Rate for Pakistan (SLUEM1524ZSPAK)
## Related Data and Content
### Content Suggestions
**Infra-Annual Labor Statistics: Unemployment Rate Total: From 15 to 64 Years for Japan**
FRED Series
**Youth Unemployment Rate for Pakistan**

# Youth Unemployment Rate for Pakistan (SLUEM1524ZSPAK)
## Related Data and Content
### Related Categories
Unemployment RatePopulation, Employment, & Labor MarketsIndicatorsInternational Data

# Youth Unemployment Rate for Pakistan (SLUEM1524ZSPAK)
## Related Data and Content
### Releases
More Series from World Development Indicators

# Youth Unemployment Rate for Pakistan (SLUEM1524ZSPAK)
## Related Data and Content
### Tags
Pakistan15 to 24 YearsWorld Development IndicatorsUnemploymentWorld BankRateAnnualNationPublic Domain: Citation RequestedNot Seasonally Adjusted
</excerpt>
### Rank 3 of 71 — 0.14
<excerpt title="Labour Force Statistics">
# Labour Force Statistics - Pakistan Bureau of Statistics
## Sustainable Developments Goals (SDGs)
5.5.2 Proportion of women in Managerial Positions
**Definition:-** This indicator refers to the proportion of females in the total number of persons employed in managerial positions.
Select Province: Pakistan
5.5.2 Proportion of women in senior and middle management positions
**Definition:-**This indicator refers to the proportion of females in the total number of persons employed in senior and middle management positions.
Select Province: Pakistan
8.3.1 Proportion of Informal Employment in Total Employment and Non-Agriculture Employment
**Definition:**The indicator presents the share of employment which is classified as informal employment in the total economy and separately in agriculture and in non-agriculture.
Select Province/Area: Pakistan
Indicator:- 8.5.1 Average Hourly Earnings of Employees by Sex, Age and Occupation
**Definition:-** This indicator provides information on the mean hourly earnings from paid employment of employees by sex, occupation, age and disability status.
Select Age Group: Total (All Ages)
8.5.2 Unemployment Rae by Sex, Age and Region
**Definition:-**This unemployment rate conveys the percentage of persons in the labour force who are unemployed.
Select Area: Total
Indicator: 8.6.1: Proportion of youth (aged 15-24 years) not in education, employment or training
Cannot be calculated due to the absence of a training variable. The LFS rounds from 2014-15 to 2018-19 did not capture information on persons currently receiving training.
8.8.1 Non-Fatal Occupational Injury incidence rate per 100,000 workers
**Definition:** This indicator provides information on the number of non-fatal occupational injuries per 100,000 workers in the reference group during the reference period. It is a measure of the personal likelihood or risk of having a non-fatal occupational injury for each worker in the reference group.The number of occupational injuries expressed per a given number of workers in the reference group is also known as the incidence rate of occupational injuries.
Select Migrant Status: Total Select Province: Pakistan
Indicator: 8.9.2: Proportion of Employed persons in the tourism industries
</excerpt>
### Rank 4 of 71 — 0.13
<excerpt title="Labour Force Statistics">
# Labour Force Statistics - Pakistan Bureau of Statistics
## Percentage Distribution Tables
1.   Percentage distribution of population by age, sex and area: Pakistan & Provinces  
2.   Percentage distribution of population by sex, area and province  
3.   Percentage distribution of population by age, sex, literacy and level of education Pakistan & Provinces, Rural & Urban  
4.   Percentage distribution of population 10 years of age and over by age, sex and marital status: Pakistan & Provinces, Rural & Urban  
5.   Percentage distribution of disable population by age, sex and area : Pakistan & Provinces  
6.   Percentage distribution of total population 10 years of age and over by age, sex , area and nature of activities Pakistan & Provinces  
7.   Percentage distribution of civilian labour force 10 years of age and over by age, sex, area and nature of activities : Pakistan & Provinces  
8.   Percentage distribution of population 10 years of age and over by level of education, sex and nature of activities: Pakistan & Provinces, Rural & Urban  
9.   Percentage distribution of population 10 years of age and over by migration status, sex, area and provinces  
10.   Percentage distribution of migrant population 10 years of age and over by place of present and previous residence, area, sex and provinces  
11.   Percentage distribution of migrant population 10 years and over by place of present and previous residence, area, sex and provinces  
12.   Percentage distribution of migrant population 10 years and over by place of present and previous residence, area, sex and provinces  
13.   Percentage distribution of migrant population 10 years of age and over by place of present and previous residence, area, sex and provinces  
14.   Percentage distribution of migrant population 10 years of age and over by main reasons of migration, sex and area  
15.   Percentage, distribution of migrant employed persons 10 years of age and over by employment status, number of hours worked during reference week and sex.  
16.   Labour force participation rates and un-employment rates by age, sex and area Pakistan & Provinces  
17.   Percentage distribution of employed persons 10 years of age and over by major industry division, sex and area: Pakistan & Provinces
</excerpt>
### Rank 5 of 71 — 0.12
<excerpt title="Labour Force Statistics">
# Labour Force Statistics - Pakistan Bureau of Statistics
## Sustainable Developments Goals (SDGs)
Select Age Group: Total (All Ages)
8.5.2 Unemployment Rae by Sex, Age and Region
**Definition:-**This unemployment rate conveys the percentage of persons in the labour force who are unemployed.
Select Area:
8.5.2 Unemployment Rae by Sex, Age and Region
**Definition:-**This unemployment rate conveys the percentage of persons in the labour force who are unemployed.
Select Area:
Total
Indicator: 8.6.1: Proportion of youth (aged 15-24 years) not in education, employment or training
Cannot be calculated due to the absence of a training variable. The LFS rounds from 2014-15 to 2018-19 did not capture information on persons currently receiving training.
8.8.1 Non-Fatal Occupational Injury incidence rate per 100,000 workers
**Definition:** This indicator provides information on the number of non-fatal occupational injuries per 100,000 workers in the reference group during the reference period. It is a measure of the personal likelihood or risk of having a non-fatal occupational injury for each worker in the reference group.The number of occupational injuries expressed per a given number of workers in the reference group is also known as the incidence rate of occupational injuries.
Select Migrant Status: Total Select Province: Pakistan
Indicator 9.2.2: Manufacturing employment as a proportion of total employment
**Definition:-** The employed persons comprise “all persons of working age who, during a short reference period, were engaged in any activity to produce goods or provide services for pay or profit” (ILO, 2023). The indicator shows the number of persons employed in tourism industries in any of their jobs. The tourism industries comprise all establishments for which the principal activity is a tourism characteristic activity, as defined in the International Recommendations for Tourism Statistics 2008 (IRTS 2008) (United Nations and World Tourism Organization, 2010).
Select Province: Pakistan Select Measure: Number of Total Employed
Indicator: 8.9.2: Proportion of Employed persons in the tourism industries
**Definitions:** This indicator presents the share of manufacturing employment in total employment.
Select Province: Pakistan
</excerpt>

## Search 6 — query: "UNdata unemployment 2015 India 2020"
### Rank 1 of 64 — 0.23 (passed on)
<excerpt title="Picture This: India's unemployment rate in 2020 highest since 1991">
# Picture This: India’s unemployment rate in 2020 highest since 1991
India’s unemployment rate rose sharply in 2020 to reach the highest it has been since 1991, according to the International Labour Organization’s (ILO) ILOSTAT database. The Figure above tracks India’s unemployment rate (percentage of total labour force) between 1991 and 2020. It tracks the data for nine countries other than India. These are Bangladesh, […]
Published May 27, 2021
Cite this article ↓
India’s unemployment rate rose sharply in 2020 to reach the highest it has been since 1991, according to the International Labour Organization’s (ILO) ILOSTAT database.
The Figure above tracks India’s unemployment rate (percentage of total labour force) between 1991 and 2020. It tracks the data for nine countries other than India. These are Bangladesh, Pakistan, Sri Lanka (from India’s neighbourhood), Brazil, China, and Russia (from BRICS), United Kingdom, United States of America, and Germany (from OECD).
You can add or remove any of these countries in the chart above by clicking on the name in the legend.
India’s unemployment rate rose between 2008 (5.36 percent) and 2010 (5.65 percent) and then fell between 2013 (5.67 percent) and 2019 (5.27 percent). It then rose sharply to 7.11 percent in the pandemic year. This is the highest it has been since 1991.
India has had the highest unemployment rate in its immediate neighbourhood while among BRICS nations, Brazil’s unemployment rate has risen sharply between 2014 (6.66 percent) and 2020 (13.67 percent).
When compared to United States, United Kingdom, and Germany, India had a higher unemployment rate than the other three between 2015 and 2019 but in 2020, US had higher unemployment rate than India.
* * *

# Picture This: India’s unemployment rate in 2020 highest since 1991
**To cite this analysis:**Team CEDA (2021). “Picture This: India’s unemployment rate in 2020 highest since 1991”_Centre for Economic Data and Analysis (CEDA), Ashoka University._ Published onceda.ashoka.edu.in
[![Image 9](blob:http://localhost/344e6bea39796d7acb6453115ce58bc9)](https://ceda.ashoka.edu.in/picture-this-indias-unemployment-rate-in-2020-highest-since-1991/)
Dhara Shah
Republish Block
Oct 3, 2024
If you wish to republish this article or use an extract or chart, please read CEDA’s republishing guidelines.
[![Image 11](blob:http://localhost/344b977082d31d71116873d1871f5252)137](https://ceda.ashoka.edu.in/picture-this-indias-unemployment-rate-in-2020-highest-since-1991/)
Linked references
Is COVID-19 “The Great Leveler”? The Critical Role of Social Identity in Lockdown- induced Job Losses
The Covid-19 Pandemic and Lockdown: First Effects on Gender Gaps in Employment and Domestic Work in India
Political Institutions and Policy Responses During a Crisis
Epidemics: A Tale of Two Workers
Here Today, Gone Tomorrow: COVID-19 and Supply Chain Disruption
The COVID-19 Pandemic and Gendered Division of Paid and Unpaid Work: Evidence from India
India as Belindia
Measuring Work: Comparing Employment-Unemployment Surveys with Time Use Surveys
Employment in 2020: Monthly changes by gender, sector and occupation
The Interstate Variation in Mortality from COVID-19 in India
Covid-19: Is India reporting fewer cases because of lower testing?
India’s Budget 2021-22: A Passing Grade
Covid-19 and lockdown: Impact on household and individual wage income
</excerpt>
### Rank 2 of 64 — 0.21
<excerpt title="Picture This: India's unemployment rate in 2020 highest since 1991">
# Picture This: India’s unemployment rate in 2020 highest since 1991 » CEDA


# Picture This: India’s unemployment rate in 2020 highest since 1991 | CEDA
Made in Humane Club
[![Image 5: logo](blob:http://localhost/346dadc7249b4f18bcd4f1d0d397bce6)](https://ceda.ashoka.edu.in/)
*   Themes  
    *   Work and Wages  
    *   Agrarian Economy  
    *   Human Development  
    *   Public Finance  
    *   Household Economics  
    *   Data Notes

*   Data Portal  
    *   Socio-Economic Data Tool  
    *   Agri Market Data Tool  
    *   Daily Food Prices Data Tool  
    *   EcoMeter  
    *   Enterprise Tracker

*   Initiatives  
    *   Women and Work

*   About Us  
    *   People  
    *   In the News  
    *   Careers  
    *   Contact  
    *   Republishing Guidelines

*   [[×](javascript:void(0) "검색창 내용 지우기") 맞춤검색 정렬 기준 Relevance Date](https://ceda.ashoka.edu.in/picture-this-indias-unemployment-rate-in-2020-highest-since-1991/#)
![Image 7](blob:http://localhost/346dadc7249b4f18bcd4f1d0d397bce6)
Work and Wages

# Picture This: India’s unemployment rate in 2020 highest since 1991
India’s unemployment rate rose sharply in 2020 to reach the highest it has been since 1991, according to the International Labour Organization’s (ILO) ILOSTAT database. The Figure above tracks India’s unemployment rate (percentage of total labour force) between 1991 and 2020. It tracks the data for nine countries other than India. These are Bangladesh, […]
Published May 27, 2021
Cite this article ↓
India’s unemployment rate rose sharply in 2020 to reach the highest it has been since 1991, according to the International Labour Organization’s (ILO) ILOSTAT database.
The Figure above tracks India’s unemployment rate (percentage of total labour force) between 1991 and 2020. It tracks the data for nine countries other than India. These are Bangladesh, Pakistan, Sri Lanka (from India’s neighbourhood), Brazil, China, and Russia (from BRICS), United Kingdom, United States of America, and Germany (from OECD).
You can add or remove any of these countries in the chart above by clicking on the name in the legend.
India’s unemployment rate rose between 2008 (5.36 percent) and 2010 (5.65 percent) and then fell between 2013 (5.67 percent) and 2019 (5.27 percent). It then rose sharply to 7.11 percent in the pandemic year. This is the highest it has been since 1991.
India has had the highest unemployment rate in its immediate neighbourhood while among BRICS nations, Brazil’s unemployment rate has risen sharply between 2014 (6.66 percent) and 2020 (13.67 percent).
When compared to United States, United Kingdom, and Germany, India had a higher unemployment rate than the other three between 2015 and 2019 but in 2020, US had higher unemployment rate than India.
* * *
</excerpt>
### Rank 3 of 64 — 0.15
<excerpt title="Impact of COVID−19 Lockdown on Unemployment in India−A before, ...">
### Results And Discussion Related To Urban Unemployment Rate
| Table 7 Monthly Urban Unemployment Rate In India (In %) |  
| --- |  
| Year / Month | Jan | Feb | Mar | Apr | May | June | July | Aug | Sep | Oct | Nov | Dec |  
| 2016 | 10.44 | 10.38 | 11.56 | 11.22 | 12.1 | 10.27 | 11.12 | 11.17 | 9.76 | 7.6 | 7.62 | 7.63 |  
| 2017 | 7.67 | 6.38 | 5.78 | 4.19 | 4.85 | 4.84 | 4.14 | 5.08 | 5.7 | 5.98 | 5.41 | 5.36 |  
| 2018 | 6.24 | 6.59 | 6.1 | 6.19 | 6.18 | 6.64 | 6.15 | 6.72 | 7.38 | 7.12 | 7.33 | 7.48 |  
| 2019 | 8.58 | 7.69 | 7.72 | 7.57 | 8.58 | 8.26 | 8.3 | 9.71 | 9.58 | 8.27 | 8.88 | 9.02 |  
| 2020 | 9.7 | 8.65 | 9.41 | **_24.95_** | **_23.14_** | **_11.68_** | **_9.37_** | **_9.83_** | **_8.45_** | **_7.18_** | **_7.07_** | **_8.84_** |
</excerpt>
### Rank 4 of 64 — 0.14
<excerpt title="Since 2014, India has lost 3.64 Cr jobs. Unemployment is at a 45-year high. ...">
# DK Shivakumar - Since 2014, India has lost 3.64 Cr jobs.... | Facebook
## DK Shivakumar's Post
[January 31, 2020](https://www.facebook.com/DKShivakumar.official/posts/pfbid0PcwVVB6Ga8XvtXN2H3RgnMw7XrUnvjdquC4B7jS9N1x3Vnc7TwZGBnrRdej6smSFl?__cft__[0]=AZjnCBJfCZ4xSsUvV0rreTcu0UsVRB7wDBcEPV7yLjULz5EOiKs4qGxgtITRdNPdBDEAIp9DUffQXBaDvUemGs67_cQx229DMpRqqnd5zfwRlXhAYAc7ZMh1Ltt0Ld5tl1roobsOV1iAn7huqDr963DKHPRAXQ7G&__tn__=%2CO%2CP-R) ·
Since 2014, India has lost 3.64 Cr jobs. Unemployment is at a 45-year high. Lack of Jobs is now India's biggest problem.
Youth Congress has launched National Register for Unemployment (NRU)
Give a Missed Call to  8151994411 & ask the central govt to announce NRU in [#Budget2020](https://www.facebook.com/hashtag/budget2020?__eep__=6&__cft__[0]=AZjnCBJfCZ4xSsUvV0rreTcu0UsVRB7wDBcEPV7yLjULz5EOiKs4qGxgtITRdNPdBDEAIp9DUffQXBaDvUemGs67_cQx229DMpRqqnd5zfwRlXhAYAc7ZMh1Ltt0Ld5tl1roobsOV1iAn7huqDr963DKHPRAXQ7G&__tn__=*NK-R)
</excerpt>
### Rank 5 of 64 — 0.14
<excerpt title="Impact of COVID−19 Lockdown on Unemployment in India−A before, ...">
### Results and Discussion
This section is divided into three sections by taking each type of unemployment rate series at one time. The three series that are considered in the study are; (i) Total Unemployment Rate in %, (ii) Rural Unemployment Rate in %, (iii) Urban Unemployment Rate in %

### Results and Discussion Related To Total Unemployment Rate
Data collected from Centre for Monitoring Indian Economy (CMIE) related to total unemployment rate (%) in India is given below **Table 1**.
| Table 1 Monthly Total Unemployment Rate In India (In %) |  
| --- |  
| Year / Month | Jan | Feb | Mar | Apr | May | June | July | Aug | Sep | Oct | Nov | Dec |  
| **2016** | 8.72 | 8.46 | 8.73 | 8.9 | 9.65 | 8.91 | 8.51 | 9.59 | 8.43 | 6.71 | 6.51 | 6.4 |  
| **2017** | 5.93 | 5.01 | 4.67 | 3.87 | 4.03 | 4.12 | 3.37 | 4.07 | 4.63 | 5 | 4.72 | 4.74 |  
| **2018** | 5.01 | 5.87 | 6 | 5.57 | 5.14 | 5.75 | 5.66 | 6.27 | 6.47 | 6.83 | 6.65 | 7.02 |  
| **2019** | 6.86 | 7.2 | 6.65 | 7.35 | 7.03 | 7.87 | 7.34 | 8.19 | 7.14 | 8.1 | 7.23 | 7.6 |  
| **2020** | 7.22 | 7.76 | 8.75 | **_23.52_** | **_21.73_** | **_10.18_** | **_7.4_** | **_8.35_** | **_6.68_** | **_7.02_** | **_6.5_** | **_9.06_** |  

### Results and Discussion Related To Total Unemployment Rate
| **2021** | **_6.52_** | **_6.89_** | **_6.5_** | **_7.97_** | **_11.84_** | **_9.17_** | 6.96 | 8.32 | 6.86 | 7.74 | 6.97 | 7.91 |  
| **2022** | 6.56 | 8.11 | 7.57 | 7.83 | 7.14 | 7.83 | 6.83 | 8.28 | 6.43 | 7.92 | 8.03 | 8.3 |
As mentioned in the research methodology section, the data set is divided into three phases i.e. (i) Before the Lockdown Phase (ii) During the Lockdown Phase, and (iii) After the Lockdown Phase. The highest and lowest total unemployment rates in before the lockdown phase are 9.65% and 3.37%.During the lockdown phase, the highest and lowest total unemployment rates observed are 23.52% and 6.5%.
However, the highest and lowest total unemployment rates recorded after the lockdown phase in India are 8.32% and 6.56%. On calculation, the mean total unemployment rate for before, during and after the lockdown phases are found to be 6.63%, 9.95% and 7.53% respectively. The data related to these phases are tested for their normality and homogeneity of variances and the results are tabulated below **Table 2**.
</excerpt>

## Search 7 — query: "Unemployment, total (% of total labour force) UNdata India 2020"
### Rank 1 of 56 — 0.80 (passed on)
<excerpt title="India - Unemployment, total (% of total labor force) (modeled ILO estimate)">
Unemployment, total (% of total labor force) (modeled ILO estimate) in India was 5.98 as of 2021. Its highest value over the past 30 years was 8.00 in 2020, while its lowest value was 5.27 in 2019.
**Definition:** Unemployment refers to the share of the labor force that is without work but available for and seeking employment.
**Source:** International Labour Organization, ILOSTAT database. Data retrieved in December 2019.
See also:
*   Thematic map  
*   Country comparison  
*   Country ranking  
*   Download data to Excel
1990
1992
1994
1996
1998
2000
2002
2004
2006
2008
2010
2012
2014
2016
2018
2020
2022
0.00
2.00
4.00
6.00
8.00
10.00

| Year | Value |  
| --- | --- |  
| 1991 | 5.60 |  
| 1992 | 5.73 |  
| 1993 | 5.69 |  
| 1994 | 5.74 |  
| 1995 | 5.76 |  
| 1996 | 5.74 |  
| 1997 | 5.61 |  
| 1998 | 5.67 |  
| 1999 | 5.74 |  
| 2000 | 5.56 |  
| 2001 | 5.58 |  
| 2002 | 5.53 |  
| 2003 | 5.64 |  
| 2004 | 5.63 |  
| 2005 | 5.61 |  
| 2006 | 5.60 |  
| 2007 | 5.57 |  
| 2008 | 5.41 |  
| 2009 | 5.54 |  
| 2010 | 5.55 |  
| 2011 | 5.43 |  
| 2012 | 5.41 |  
| 2013 | 5.42 |  
| 2014 | 5.44 |  
| 2015 | 5.44 |  
| 2016 | 5.42 |  
| 2017 | 5.36 |  
| 2018 | 5.33 |  
| 2019 | 5.27 |  
| 2020 | 8.00 |  
| 2021 | 5.98 |
</excerpt>
### Rank 2 of 56 — 0.79
<excerpt title="India - Unemployment, total (% of total labor force) (modeled ILO estimate)">
| Year | Value |  
| --- | --- |  
| 1991 | 5.60 |  
| 1992 | 5.73 |  
| 1993 | 5.69 |  
| 1994 | 5.74 |  
| 1995 | 5.76 |  
| 1996 | 5.74 |  
| 1997 | 5.61 |  
| 1998 | 5.67 |  
| 1999 | 5.74 |  
| 2000 | 5.56 |  
| 2001 | 5.58 |  
| 2002 | 5.53 |  
| 2003 | 5.64 |  
| 2004 | 5.63 |  
| 2005 | 5.61 |  
| 2006 | 5.60 |  
| 2007 | 5.57 |  
| 2008 | 5.41 |  
| 2009 | 5.54 |  
| 2010 | 5.55 |  
| 2011 | 5.43 |  
| 2012 | 5.41 |  
| 2013 | 5.42 |  
| 2014 | 5.44 |  
| 2015 | 5.44 |  
| 2016 | 5.42 |  
| 2017 | 5.36 |  
| 2018 | 5.33 |  
| 2019 | 5.27 |  
| 2020 | 8.00 |  
| 2021 | 5.98 |

**Development Relevance:**Paradoxically, low unemployment rates can disguise substantial poverty in a country, while high unemployment rates can occur in countries with a high level of economic development and low rates of poverty. In countries without unemployment or welfare benefits people eke out a living in vulnerable employment. In countries with well-developed safety nets workers can afford to wait for suitable or desirable jobs. But high and sustained unemployment indicates serious inefficiencies in resource allocation. Youth unemployment is an important policy issue for many economies. Young men and women today face increasing uncertainty in their hopes of undergoing a satisfactory transition in the labour market, and this uncertainty and disillusionment can, in turn, have damaging effects on individuals, communities, economies and society at large. Unemployed or underemployed youth are less able to contribute effectively to national development and have fewer opportunities to exercise their rights as citizens. They have less to spend as consumers, less to invest as savers and often have no "voice" to bring about change in their lives and communities. Widespread youth unemployment and underemployment also prevents companies and countries from innovating and developing competitive advantages based on human capital investment, thus undermining future prospects. Unemployment is a key measure to monitor whether a country is on track to achieve the Sustainable Development Goal of promoting sustained, inclusive and sustainable economic growth, full and productive employment and decent work for all. [SDG Indicator 8.5.2]
</excerpt>
### Rank 3 of 56 — 0.27
<excerpt title="Impact of COVID−19 Lockdown on Unemployment in India−A before, ...">
### Results and Discussion
This section is divided into three sections by taking each type of unemployment rate series at one time. The three series that are considered in the study are; (i) Total Unemployment Rate in %, (ii) Rural Unemployment Rate in %, (iii) Urban Unemployment Rate in %

### Results and Discussion Related To Total Unemployment Rate
Data collected from Centre for Monitoring Indian Economy (CMIE) related to total unemployment rate (%) in India is given below **Table 1**.
| Table 1 Monthly Total Unemployment Rate In India (In %) |  
| --- |  
| Year / Month | Jan | Feb | Mar | Apr | May | June | July | Aug | Sep | Oct | Nov | Dec |  
| **2016** | 8.72 | 8.46 | 8.73 | 8.9 | 9.65 | 8.91 | 8.51 | 9.59 | 8.43 | 6.71 | 6.51 | 6.4 |  
| **2017** | 5.93 | 5.01 | 4.67 | 3.87 | 4.03 | 4.12 | 3.37 | 4.07 | 4.63 | 5 | 4.72 | 4.74 |  
| **2018** | 5.01 | 5.87 | 6 | 5.57 | 5.14 | 5.75 | 5.66 | 6.27 | 6.47 | 6.83 | 6.65 | 7.02 |  
| **2019** | 6.86 | 7.2 | 6.65 | 7.35 | 7.03 | 7.87 | 7.34 | 8.19 | 7.14 | 8.1 | 7.23 | 7.6 |  
| **2020** | 7.22 | 7.76 | 8.75 | **_23.52_** | **_21.73_** | **_10.18_** | **_7.4_** | **_8.35_** | **_6.68_** | **_7.02_** | **_6.5_** | **_9.06_** |  

### Results and Discussion Related To Total Unemployment Rate
| **2021** | **_6.52_** | **_6.89_** | **_6.5_** | **_7.97_** | **_11.84_** | **_9.17_** | 6.96 | 8.32 | 6.86 | 7.74 | 6.97 | 7.91 |  
| **2022** | 6.56 | 8.11 | 7.57 | 7.83 | 7.14 | 7.83 | 6.83 | 8.28 | 6.43 | 7.92 | 8.03 | 8.3 |
As mentioned in the research methodology section, the data set is divided into three phases i.e. (i) Before the Lockdown Phase (ii) During the Lockdown Phase, and (iii) After the Lockdown Phase. The highest and lowest total unemployment rates in before the lockdown phase are 9.65% and 3.37%.During the lockdown phase, the highest and lowest total unemployment rates observed are 23.52% and 6.5%.
However, the highest and lowest total unemployment rates recorded after the lockdown phase in India are 8.32% and 6.56%. On calculation, the mean total unemployment rate for before, during and after the lockdown phases are found to be 6.63%, 9.95% and 7.53% respectively. The data related to these phases are tested for their normality and homogeneity of variances and the results are tabulated below **Table 2**.
</excerpt>
### Rank 4 of 56 — 0.26
<excerpt title="Picture This: India's unemployment rate in 2020 highest since 1991">
# Picture This: India’s unemployment rate in 2020 highest since 1991
India’s unemployment rate rose sharply in 2020 to reach the highest it has been since 1991, according to the International Labour Organization’s (ILO) ILOSTAT database. The Figure above tracks India’s unemployment rate (percentage of total labour force) between 1991 and 2020. It tracks the data for nine countries other than India. These are Bangladesh, […]
Published May 27, 2021
Cite this article ↓
India’s unemployment rate rose sharply in 2020 to reach the highest it has been since 1991, according to the International Labour Organization’s (ILO) ILOSTAT database.
The Figure above tracks India’s unemployment rate (percentage of total labour force) between 1991 and 2020. It tracks the data for nine countries other than India. These are Bangladesh, Pakistan, Sri Lanka (from India’s neighbourhood), Brazil, China, and Russia (from BRICS), United Kingdom, United States of America, and Germany (from OECD).
You can add or remove any of these countries in the chart above by clicking on the name in the legend.
India’s unemployment rate rose between 2008 (5.36 percent) and 2010 (5.65 percent) and then fell between 2013 (5.67 percent) and 2019 (5.27 percent). It then rose sharply to 7.11 percent in the pandemic year. This is the highest it has been since 1991.
India has had the highest unemployment rate in its immediate neighbourhood while among BRICS nations, Brazil’s unemployment rate has risen sharply between 2014 (6.66 percent) and 2020 (13.67 percent).
When compared to United States, United Kingdom, and Germany, India had a higher unemployment rate than the other three between 2015 and 2019 but in 2020, US had higher unemployment rate than India.
* * *

# Picture This: India’s unemployment rate in 2020 highest since 1991
**To cite this analysis:**Team CEDA (2021). “Picture This: India’s unemployment rate in 2020 highest since 1991”_Centre for Economic Data and Analysis (CEDA), Ashoka University._ Published onceda.ashoka.edu.in
[![Image 9](blob:http://localhost/344e6bea39796d7acb6453115ce58bc9)](https://ceda.ashoka.edu.in/picture-this-indias-unemployment-rate-in-2020-highest-since-1991/)
Dhara Shah
Republish Block
Oct 3, 2024
If you wish to republish this article or use an extract or chart, please read CEDA’s republishing guidelines.
[![Image 11](blob:http://localhost/344b977082d31d71116873d1871f5252)137](https://ceda.ashoka.edu.in/picture-this-indias-unemployment-rate-in-2020-highest-since-1991/)
Linked references
Is COVID-19 “The Great Leveler”? The Critical Role of Social Identity in Lockdown- induced Job Losses
The Covid-19 Pandemic and Lockdown: First Effects on Gender Gaps in Employment and Domestic Work in India
Political Institutions and Policy Responses During a Crisis
Epidemics: A Tale of Two Workers
Here Today, Gone Tomorrow: COVID-19 and Supply Chain Disruption
The COVID-19 Pandemic and Gendered Division of Paid and Unpaid Work: Evidence from India
India as Belindia
Measuring Work: Comparing Employment-Unemployment Surveys with Time Use Surveys
Employment in 2020: Monthly changes by gender, sector and occupation
The Interstate Variation in Mortality from COVID-19 in India
Covid-19: Is India reporting fewer cases because of lower testing?
India’s Budget 2021-22: A Passing Grade
Covid-19 and lockdown: Impact on household and individual wage income
</excerpt>
### Rank 5 of 56 — 0.23
<excerpt title="Picture This: India's unemployment rate in 2020 highest since 1991">
# Picture This: India’s unemployment rate in 2020 highest since 1991 » CEDA


# Picture This: India’s unemployment rate in 2020 highest since 1991 | CEDA
Made in Humane Club
[![Image 5: logo](blob:http://localhost/346dadc7249b4f18bcd4f1d0d397bce6)](https://ceda.ashoka.edu.in/)
*   Themes  
    *   Work and Wages  
    *   Agrarian Economy  
    *   Human Development  
    *   Public Finance  
    *   Household Economics  
    *   Data Notes

*   Data Portal  
    *   Socio-Economic Data Tool  
    *   Agri Market Data Tool  
    *   Daily Food Prices Data Tool  
    *   EcoMeter  
    *   Enterprise Tracker

*   Initiatives  
    *   Women and Work

*   About Us  
    *   People  
    *   In the News  
    *   Careers  
    *   Contact  
    *   Republishing Guidelines

*   [[×](javascript:void(0) "검색창 내용 지우기") 맞춤검색 정렬 기준 Relevance Date](https://ceda.ashoka.edu.in/picture-this-indias-unemployment-rate-in-2020-highest-since-1991/#)
![Image 7](blob:http://localhost/346dadc7249b4f18bcd4f1d0d397bce6)
Work and Wages

# Picture This: India’s unemployment rate in 2020 highest since 1991
India’s unemployment rate rose sharply in 2020 to reach the highest it has been since 1991, according to the International Labour Organization’s (ILO) ILOSTAT database. The Figure above tracks India’s unemployment rate (percentage of total labour force) between 1991 and 2020. It tracks the data for nine countries other than India. These are Bangladesh, […]
Published May 27, 2021
Cite this article ↓
India’s unemployment rate rose sharply in 2020 to reach the highest it has been since 1991, according to the International Labour Organization’s (ILO) ILOSTAT database.
The Figure above tracks India’s unemployment rate (percentage of total labour force) between 1991 and 2020. It tracks the data for nine countries other than India. These are Bangladesh, Pakistan, Sri Lanka (from India’s neighbourhood), Brazil, China, and Russia (from BRICS), United Kingdom, United States of America, and Germany (from OECD).
You can add or remove any of these countries in the chart above by clicking on the name in the legend.
India’s unemployment rate rose between 2008 (5.36 percent) and 2010 (5.65 percent) and then fell between 2013 (5.67 percent) and 2019 (5.27 percent). It then rose sharply to 7.11 percent in the pandemic year. This is the highest it has been since 1991.
India has had the highest unemployment rate in its immediate neighbourhood while among BRICS nations, Brazil’s unemployment rate has risen sharply between 2014 (6.66 percent) and 2020 (13.67 percent).
When compared to United States, United Kingdom, and Germany, India had a higher unemployment rate than the other three between 2015 and 2019 but in 2020, US had higher unemployment rate than India.
* * *
</excerpt>

## Search 8 — query: "UNdata "Unemployment, total (% of total labour force)" India 2015"
(no page could be scored)

## Search 9 — query: "UNdata unemployment India 2015 "Unemployment, total (% of total labour force)""
### Rank 1 of 543 — 0.20 (passed on)
<excerpt title="Report - labourbureau.gov.in">
## [PDF page 160]
11  Jammu & Kashmir  41.9  55.1  0.7  2.3  
12  Jharkhand  34.9  57.8  6.1  1.3  
13  Karnataka  61.3  37.5  -  1.3  
14  Kerala  42.1  44.9  -  13.1  
15  Madhya Pradesh  31.4  65.4  1.2  2.1
16  Maharashtra  53.7  45.4  0.2  0.6  
17  Manipur  30.3  66.2  0.7  2.9  
18  Meghalaya  58.4  40  -  1.6  
19  Mizoram  49.9  47.9  1.6  0.6  
20  Nagaland  62.2  29.6  3.4  4.8
21  Odisha  35.5  62.1  0.9  1.5  
22  Punjab  44.1  46.1  -  9.8  
23  Rajasthan  52.8  39  5.2  3  
24  Sikkim  65.4  24.6  0.7  9.3  
25  Tamil Nadu  69.7  28.2  -  2.1

## [PDF page 160]
26  Telangana  52.3  47.7  -  0  
27  Tripura  44.5  45.8  3.3  6.5  
28  Uttarakhand  39.9  49.1  -  11  
29  Uttar Pradesh  61.2  35.9  1.2  1.7  
30  West Bengal  33.9  62.2  1.5  2.4
31  A & N Islands  53  11.9  5.8  29.3  
32  Chandigarh  100  -  -  -  
33  Dadra & Nagar Haveli  88.2  10  -  1.8  
34  Daman & Diu  100  -  -  -  
35  Lakshadweep  97.4  2.6  -  -  
36  Puducherry  ----
All India  45.1  51.2  1.7  2.1
110
</excerpt>
### Rank 2 of 543 — 0.19
<excerpt title="Report - labourbureau.gov.in">
## [PDF page 155]
11  Jammu & Kashmir  46.4  47.9  0.8  4.8  
12  Jharkhand  38.6  50.9  7.8  2.7  
13  Karnataka  65.5  32.7  -  1.8  
14  Kerala  41.6  40.4  0.4  17.6  
15  Madhya Pradesh  33.2  62.3  0.9  3.6
16  Maharashtra  53.5  45.5  0.2  0.7  
17  Manipur  27.9  68.9  0.5  2.6  
18  Meghalaya  59.3  34.5  0.7  5.5  
19  Mizoram  57.4  38.9  1.5  2.1  
20  Nagaland  63.6  26.2  2.8  7.4
21  Odisha  35  61.5  1.1  2.4  
22  Punjab  64.9  25.5  -  9.6  
23  Rajasthan  54.7  35.3  7  3.1  
24  Sikkim  56  27.5  0.8  15.8  
25  Tamil Nadu  77.6  20.1  -  2.3

## [PDF page 155]
26  Telangana  57  42.3  -  0.7  
27  Tripura  37.4  39.8  13.3  9.6  
28  Uttarakhand  46.5  44.4  -  9  
29  Uttar Pradesh  62.1  33.1  1.8  2.9  
30  West Bengal  36.1  59.7  1.3  2.9
31  A & N Islands  61.3  7.7  3.8  27.2  
32  Chandigarh  94.3  -  -  5.7  
33  Dadra & Nagar Haveli  89.5  7.5  -  3  
34  Daman & Diu  97.3  -  -  2.7  
35  Lakshadweep  68.3  14.4  12.8  4.5  
36  Puducherry  100  -  -  -
All India  46  49.4  1.9  2.7
105
</excerpt>
### Rank 3 of 543 — 0.18
<excerpt title="Report - labourbureau.gov.in">
## [PDF page 159]
11  Jammu & Kashmir  42.5  51.4  0.9  5.2  
12  Jharkhand  35.5  54.4  8.5  1.6  
13  Karnataka  60.7  37.8  -  1.6  
14  Kerala  34.4  48.3  0.5  16.7  
15  Madhya Pradesh  30.8  64.4  1  3.8
16  Maharashtra  47.3  51.8  0.3  0.6  
17  Manipur  32.4  64.5  0.6  2.5  
18  Meghalaya  54.3  41.8  0.1  3.9  
19  Mizoram  42.6  55.6  1.4  0.4  
20  Nagaland  60.2  31.1  2.4  6.3
21  Odisha  32.8  63.7  1.2  2.3  
22  Punjab  37.1  54.9  -  8  
23  Rajasthan  53.2  36.4  7.3  3.1  
24  Sikkim  52.9  29.7  0.5  17  
25  Tamil Nadu  64.3  32.3  -  3.4

## [PDF page 159]
26  Telangana  49.6  50.4  -  0  
27  Tripura  36.6  40.3  13.5  9.6  
28  Uttarakhand  38.6  51  -  10.4  
29  Uttar Pradesh  58.6  36.7  2  2.7  
30  West Bengal  33.6  62.4  1.4  2.5
31  A & N Islands  54  9.5  4.7  31.8  
32  Chandigarh  78.5  -  -  21.5  
33  Dadra & Nagar Haveli  88.9  8.8  -  2.3  
34  Daman & Diu  100  -  -  -  
35  Lakshadweep  98.6  1.4  -  -  
36  Puducherry  ----
All India  41.6  53.8  2  2.5
109
</excerpt>
### Rank 4 of 543 — 0.17
<excerpt title="Report - labourbureau.gov.in">
## [PDF page 185]
16  Maharashtra  59.1  39.2  1  0.8  
17  Manipur  100  -  -  -  
18  Meghalaya  26  74  -  -  
19  Mizoram  92.1  7.9  -  -  
20  Nagaland  58.3  37.2  -  4.5
21  Odisha  56.5  26.7  4  12.8  
22  Punjab  74.7  9.9  0.2  15.2  
23  Rajasthan  66.3  19.1  6.8  7.8  
24  Sikkim  33.5  40.2  -  26.3  
25  Tamil Nadu  61.8  29.9  -  8.3
26  Telangana  46.3  48.2  1.1  4.4  
27  Tripura  39.1  21.8  10.1  29  
28  Uttarakhand  70.4  15.1  -  14.5  
29  Uttar Pradesh  45.8  23.3  4.1  26.8  
30  West Bengal  48.7  40  2.8  8.5
31  A & N Islands  59.7  3.4  1.6  35.2  
32  Chandigarh  89.6  -  -  10.4  
33  Dadra & Nagar Haveli  ----  
34  Daman & Diu  100  -  -  -  
35  Lakshadweep  100  -  -  -  
36  Puducherry  ----

## [PDF page 185]
All India  53.1  36.9  1.9  8.1
135
</excerpt>
### Rank 5 of 543 — 0.17
<excerpt title="Report - labourbureau.gov.in">
## [PDF page 161]
16  Maharashtra  36.1  63  0.3  0.6  
17  Manipur  47.6  52.4  -  -  
18  Meghalaya  47.4  44.7  0.1  7.7  
19  Mizoram  33.8  64.8  1.3  0.2  
20  Nagaland  56.6  34  0.5  8.9
21  Odisha  22.9  69.6  2.4  5.1  
22  Punjab  7  93  -  -  
23  Rajasthan  54.7  26.1  15.8  3.3  
24  Sikkim  26.6  40.3  -  33.1  
25  Tamil Nadu  56.7  38.2  -  5.2
26  Telangana  45.2  54.8  -  -  
27  Tripura  15.4  25.6  40.9  18.1  
28  Uttarakhand  24.8  70.6  -  4.6  
29  Uttar Pradesh  33.9  44.4  9.7  11.9  
30  West Bengal  33.2  62.8  1.2  2.8

## [PDF page 161]
31  A & N Islands  58.2  -  -  41.8  
32  Chandigarh  -  -  -  100  
33  Dadra & Nagar Haveli  91.5  4.2  -  4.2  
34  Daman & Diu  100  -  -  -  
35  Lakshadweep  100  -  -  -  
36  Puducherry  ----
All India  32.5  60.8  2.9  3.8
111
</excerpt>

## Search 10 — query: "UNdata India unemployment total 2020 sl.uem.totl.zs"
### Rank 1 of 35 — 0.74 (passed on)
<excerpt title="India - Unemployment, total (% of total labor force) (modeled ILO estimate)">
Unemployment, total (% of total labor force) (modeled ILO estimate) in India was 5.98 as of 2021. Its highest value over the past 30 years was 8.00 in 2020, while its lowest value was 5.27 in 2019.
**Definition:** Unemployment refers to the share of the labor force that is without work but available for and seeking employment.
**Source:** International Labour Organization, ILOSTAT database. Data retrieved in December 2019.
See also:
*   Thematic map  
*   Country comparison  
*   Country ranking  
*   Download data to Excel
1990
1992
1994
1996
1998
2000
2002
2004
2006
2008
2010
2012
2014
2016
2018
2020
2022
0.00
2.00
4.00
6.00
8.00
10.00

| Year | Value |  
| --- | --- |  
| 1991 | 5.60 |  
| 1992 | 5.73 |  
| 1993 | 5.69 |  
| 1994 | 5.74 |  
| 1995 | 5.76 |  
| 1996 | 5.74 |  
| 1997 | 5.61 |  
| 1998 | 5.67 |  
| 1999 | 5.74 |  
| 2000 | 5.56 |  
| 2001 | 5.58 |  
| 2002 | 5.53 |  
| 2003 | 5.64 |  
| 2004 | 5.63 |  
| 2005 | 5.61 |  
| 2006 | 5.60 |  
| 2007 | 5.57 |  
| 2008 | 5.41 |  
| 2009 | 5.54 |  
| 2010 | 5.55 |  
| 2011 | 5.43 |  
| 2012 | 5.41 |  
| 2013 | 5.42 |  
| 2014 | 5.44 |  
| 2015 | 5.44 |  
| 2016 | 5.42 |  
| 2017 | 5.36 |  
| 2018 | 5.33 |  
| 2019 | 5.27 |  
| 2020 | 8.00 |  
| 2021 | 5.98 |
</excerpt>
### Rank 2 of 35 — 0.70
<excerpt title="India - Unemployment, total (% of total labor force) (modeled ILO estimate)">
| Year | Value |  
| --- | --- |  
| 1991 | 5.60 |  
| 1992 | 5.73 |  
| 1993 | 5.69 |  
| 1994 | 5.74 |  
| 1995 | 5.76 |  
| 1996 | 5.74 |  
| 1997 | 5.61 |  
| 1998 | 5.67 |  
| 1999 | 5.74 |  
| 2000 | 5.56 |  
| 2001 | 5.58 |  
| 2002 | 5.53 |  
| 2003 | 5.64 |  
| 2004 | 5.63 |  
| 2005 | 5.61 |  
| 2006 | 5.60 |  
| 2007 | 5.57 |  
| 2008 | 5.41 |  
| 2009 | 5.54 |  
| 2010 | 5.55 |  
| 2011 | 5.43 |  
| 2012 | 5.41 |  
| 2013 | 5.42 |  
| 2014 | 5.44 |  
| 2015 | 5.44 |  
| 2016 | 5.42 |  
| 2017 | 5.36 |  
| 2018 | 5.33 |  
| 2019 | 5.27 |  
| 2020 | 8.00 |  
| 2021 | 5.98 |

**Development Relevance:**Paradoxically, low unemployment rates can disguise substantial poverty in a country, while high unemployment rates can occur in countries with a high level of economic development and low rates of poverty. In countries without unemployment or welfare benefits people eke out a living in vulnerable employment. In countries with well-developed safety nets workers can afford to wait for suitable or desirable jobs. But high and sustained unemployment indicates serious inefficiencies in resource allocation. Youth unemployment is an important policy issue for many economies. Young men and women today face increasing uncertainty in their hopes of undergoing a satisfactory transition in the labour market, and this uncertainty and disillusionment can, in turn, have damaging effects on individuals, communities, economies and society at large. Unemployed or underemployed youth are less able to contribute effectively to national development and have fewer opportunities to exercise their rights as citizens. They have less to spend as consumers, less to invest as savers and often have no "voice" to bring about change in their lives and communities. Widespread youth unemployment and underemployment also prevents companies and countries from innovating and developing competitive advantages based on human capital investment, thus undermining future prospects. Unemployment is a key measure to monitor whether a country is on track to achieve the Sustainable Development Goal of promoting sustained, inclusive and sustainable economic growth, full and productive employment and decent work for all. [SDG Indicator 8.5.2]
</excerpt>
### Rank 3 of 35 — 0.17
<excerpt title="Unemployment, total (% of total labor force) (modeled ILO estimate)">
Code SL.UEM.TOTL.ZS  
Indicator Name Unemployment, total (% of total labor force) (modeled ILO estimate)  
Long definition Unemployment refers to the share of the labor force that is without work but available for and seeking employment.  
Source ILO Modelled Estimates database (ILOEST), International Labour Organization (ILO), uri: https://ilostat.ilo.org/data/bulk/, publisher: ILOSTAT, type: external database, date accessed: January 17, 2026  
Topic Social Protection & Labor: Unemployment  
Dataset WB_WDI  
Unit of measure% of total labor force  
Periodicity Annual  
Reference period 1991-2025  
Aggregation method Weighted average  

Statistical concept and methodology Methodology: The unemployment rate is calculated by expressing the number of unemployed persons as a percentage of the total number of persons in the labor force. The labor force (formerly known as the economically active population) is the sum of the number of persons employed and the number of persons unemployed. The series is part of the "ILO modeled estimates database," including nationally reported observations and imputed data for countries with missing data, primarily to capture regional and global trends with consistent country coverage. Country-reported microdata is based mainly on nationally representative labor force surveys, with other sources (e.g., household surveys and population censuses) considering differences in the data source, the scope of coverage, methodology, and other country-specific factors. Country analysis requires caution where limited nationally reported data are available. A series of models are also applied to impute missing observations and make projections. However, imputed observations are not based on national data, are subject to high uncertainty, and should not be used for country comparisons or rankings. For more information: https://ilostat.ilo.org/resources/concepts-and-definitions/ilo-modelled-estimates/ Statistical concept(s): The unemployed comprise all persons of working age who were: a) without work during the reference period, i.e. were not in paid employment or self-employment; b) currently available for work, i.e. were available for paid employment or self-employment during the reference period; and c) seeking work, i.e. had taken specific steps in a specified recent period to seek paid employment or self-employment. Future starters, that is, persons who did not look for work but have a future labor market stake (made arrangements for a future job start) are also counted as unemployed, as are participants in skills training or retraining schemes within employment promotion programs, who on that basis, were “not in employment”, not “currently available” and did not “seek employment” because they had a job offer to start within a short subsequent period generally not greater than three months. The unemployed also include persons “not in employment” who carried out activities to migrate abroad in order to work for pay or profit but who were still waiting for the opportunity to leave. Employment comprises all persons of working age who during a specified brief period, such as one week or one day, were in the following categories: a) paid employment (whether at work or with a job but not at work); or b) self-employment (whether at work or with an enterprise but not at work).

The working-age population is the population above the legal working age, but for statistical purposes it comprises all persons above a specified minimum age threshold for which an inquiry on economic activity is made. To promote international comparability, the working-age population is often defined as all persons aged 15 and older, but this may vary from country to country based on national laws and practices (some countries also apply an upper age limit).
</excerpt>
### Rank 4 of 35 — 0.15
<excerpt title="Youth Unemployment Rate for India (SLUEM1524ZSIND) - FRED">
#
Youth Unemployment Rate for India (SLUEM1524ZSIND)
Observations
2025: 16.022 | Percent, Not Seasonally Adjusted |  Annual
Updated: Feb 25, 2026 2:41 PM CST
Next Release Date: Not Available
Observations
2025:16.022
Updated: Feb 25, 2026 2:41 PM CST
Next Release Date: Not Available
2025:16.022  
2024:15.746  
2023:15.595  
2022:17.732  
2021:20.824  
View All
Units:
Percent,
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
(a)Youth Unemployment Rate for India,Percent,Not Seasonally Adjusted(SLUEM1524ZSIND)
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
###### Youth Unemployment Rate for India
</excerpt>
### Rank 5 of 35 — 0.13
<excerpt title="Unemployment rate in India | DataPulse">
# Unemployment rate in India | DataPulse
DataPulseData Intelligence ResearchMorning EditionSaved 0LibrarySign in
Statistics/Education & Employment/India

# Unemployment rate in India
4.22%
Latest reported value · 2025 · % of labor force
Coverage 2000–2025
Indicator SL.UEM.TOTL.ZS
Updated 8 Oct 2026
Save on this device Save workspace Print / PDF
line bar table
Years–
CSV XLSX PPTX PNG
Compare India
Unemployment rate
% of labor force · 2000–2025
Source: World Bank. No missing observations in range.

# Unemployment rate in India
## About this statistic
Unemployment refers to the share of the labor force that is without work but available for and seeking employment.

# Unemployment rate in India
## Methodology
Unemployment refers to the share of the labor force that is without work but available for and seeking employment. Annual observations as supplied by World Development Indicators. Missing observations are retained as null, never imputed. Values may be revised by the source. Review original source metadata for estimation methods and country comparability.
Source record
Publisher ILO Modelled Estimates database (ILOEST), International Labour Organization (ILO)ilostat.ilo.org/data/bulk/
Full source note  
ILO Modelled Estimates database (ILOEST), International Labour Organization (ILO), uri: https://ilostat.ilo.org/data/bulk/, publisher: ILOSTAT, type: external database, date accessed: January 17, 2026
Dataset World Bank
Observation frequency / latest period annual · 2025
Source publication (provider timestamp)Not supplied by provider
Source record updated 2026-10-08
Retrieved 10 Oct 2026
License World Bank dataset terms apply (generally CC BY 4.0, subject to indicator-specific third-party terms).Dataset terms of use
View original indicator
Cite
APA MLA Chicago
ILO Modelled Estimates database (ILOEST), International Labour Organization (ILO). (2026). Unemployment rate: India, 2000–2025 [Data set]. World Bank. Retrieved November 18, 2026, from https://data.worldbank.org/indicator/SL.UEM.TOTL.ZS?locations=IND
Copy citation

# Unemployment rate in India
## Related statistics
Government education expenditure in India
India/Education & Employment/2000–2022
4.1%
2022 · % of GDP
DataPulse
Public statistics from official sources, including the World Bank and ONS. Every figure links to its original indicator and license. Browsing and exports are free with no account. Sign in to sync bookmarks and build private collections.
Powered by IMI International
Morning EditionAll dataStatisticsTopicsReportsCountriesBrand PulseSponsorship RadarConsumer InsightsMarket InsightseCommerce InsightsResearchMorning Edition
World Bank Open DataOffice for National StatisticsDataset terms of use
4%
</excerpt>

# Example 4
## Question
Based on the data provided by the NCEI for the global summary of the month, which of the following stations saw a difference between mean max and mean min temperature less than 17 degrees Fahrenheit in July 2020: Denver International Airport, Atlanta Hartsfield Jackson International Airport, Los Angeles International Airport, Chicago Ohare International Airport, Orlando International Airport

## Expected answer
Los Angeles International Airport, Orlando International Airport

## Grade 0.50

## Search 1 — query: "NCEI July 2020 global summary Denver International Airport mean max mean min"
### Rank 1 of 22 — 0.16 (passed on)
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
### Rank 2 of 22 — 0.14
<excerpt title="Summary of Monthly Normals 1991-2020">
U.S. Department of Commerce National Centers for Environmental Information
National Oceanic & Atmospheric Administration 151 Patton Avenue
National Environmental Satellite, Data, and Information Service Asheville, North Carolina 28801
Current Location: Elev: 5414 ft. Lat: 39.8328° N Lon: 104.6575° W
Station: DENVER INTL AP, CO US USW00003017

# Summary of Monthly Normals


# 1991-2020
Generated on 11/18/2026
Temperature (°F)
Cooling Degree Days Heating Degree Days
Mean Base (above) Base (above) Mean Number of Days
Month Daily
Max Daily
Min Mean
Long
Term
Max
Std Dev
Long
Term
Min Std
Dev
Long
Term
Avg Std
Dev
55 57 60 65 70 72 55 57 60 65 Max
>=
100
Max
>=
90
Max
>=
50
Max
<=
32
Min
<=
32
Min
<=
0
01 44.6 18.7 31.7 4.3 3.0 3.6 0.3 0.1 0.0 0.0 0.0 0.0 724.3 786.1 878.9 1033.9 0.0 0.0 11.3 5.0 29.0 2.0
02 45.7 19.7 32.7 5.6 3.5 4.3 1.3 0.6 0.1 0.0 0.0 0.0 625.3 680.6 764.2 904.2 0.0 0.0 11.1 5.3 26.1 1.6
03 55.7 27.5 41.6 4.2 3.0 3.4 9.5 5.2 1.7 0.0 0.0 0.0 425.1 482.9 572.3 725.6 0.0 0.0 21.2 1.7 23.2 0.2
</excerpt>
### Rank 3 of 22 — 0.12
<excerpt title="Summary of Monthly Normals 1991-2020">
# 1991-2020
Generated on 11/18/2026
Temperature (°F)
Cooling Degree Days Heating Degree Days
Mean Base (above) Base (above) Mean Number of Days
Month Daily
Max Daily
Min Mean
Long
Term
Max
Std Dev
Long
Term
Min Std
Dev
Long
Term
Avg Std
Dev
55 57 60 65 70 72 55 57 60 65 Max
>=
100
Max
>=
90
Max
>=
50
Max
<=
32
Min
<=
32
Min
<=
0
01 44.6 18.7 31.7 4.3 3.0 3.6 0.3 0.1 0.0 0.0 0.0 0.0 724.3 786.1 878.9 1033.9 0.0 0.0 11.3 5.0 29.0 2.0
02 45.7 19.7 32.7 5.6 3.5 4.3 1.3 0.6 0.1 0.0 0.0 0.0 625.3 680.6 764.2 904.2 0.0 0.0 11.1 5.3 26.1 1.6
03 55.7 27.5 41.6 4.2 3.0 3.4 9.5 5.2 1.7 0.0 0.0 0.0 425.1 482.9 572.3 725.6 0.0 0.0 21.2 1.7 23.2 0.2

# 1991-2020
04 61.7 33.9 47.8 3.8 2.5 2.9 29.3 17.8 7.3 1.2 0.0 0.0 245.1 293.6 373.1 517.1 0.0 0.0 24.4 0.5 13.2 0.0
05 71.2 43.6 57.4 4.0 2.0 2.8 154.0 117.2 73.0 25.7 5.9 2.8 79.5 104.8 153.6 261.3 0.0 0.8 29.4 0.0 2.9 0.0
06 83.4 53.0 68.2 4.2 2.6 3.2 400.5 344.1 263.8 147.4 62.3 39.3 4.7 8.2 17.9 51.5 0.4 8.6 29.9 0.0 0.0 0.0
07 89.9 60.2 75.1 3.0 1.7 2.2 621.3 559.6 467.1 315.2 172.8 123.3 0.2 0.4 0.8 3.8 1.3 18.8 31.0 0.0 0.0 0.0
</excerpt>
### Rank 4 of 22 — 0.07
<excerpt title="Summary of Monthly Normals 1991-2020">
# 1991-2020
08 87.5 58.3 72.9 3.1 1.9 2.4 555.1 493.5 401.7 254.1 123.9 82.1 0.3 0.7 2.0 9.3 0.2 13.8 31.0 0.0 0.0 0.0
09 79.6 50.0 64.8 3.5 2.5 2.8 318.0 267.7 197.7 99.2 34.4 18.4 24.3 34.0 53.9 105.3 0.1 4.2 29.6 0.0 0.7 0.0
10 65.3 37.0 51.1 4.4 3.0 3.5 73.5 51.7 28.4 6.6 0.5 0.1 192.6 232.9 302.6 435.8 0.0 0.0 27.0 0.8 9.2 0.0
11 52.9 26.0 39.4 5.5 3.2 4.2 7.7 3.9 1.0 0.1 0.0 0.0 474.2 530.3 617.5 766.6 0.0 0.0 18.7 2.5 22.7 0.5

# 1991-2020
12 44.0 18.4 31.2 3.7 3.1 3.1 0.2 0.1 0.0 0.0 0.0 0.0 737.6 799.4 892.5 1047.6 0.0 0.0 11.1 6.4 29.2 1.9
Summary 65.1 37.2 51.2 4.1 2.7 3.2 2171 1862 1442 850 400 266 3533 3954 4629 5862 2.0 46.2 275.7 22.2 156.2 6.2
Empty or blank cells indicate data is missing or insufficient occurrences to compute value U.S. Department of Commerce National Centers for Environmental Information
National Oceanic & Atmospheric Administration 151 Patton Avenue
National Environmental Satellite, Data, and Information Service Asheville, North Carolina 28801
Current Location: Elev: 5414 ft. Lat: 39.8328° N Lon: 104.6575° W
Station: DENVER INTL AP, CO US USW00003017

# Summary of Monthly Normals
</excerpt>
### Rank 5 of 22 — 0.07
<excerpt title="Monthly Climate Reports | Global Climate Report | July 2020">
# Monthly Climate Reports | National Centers for Environmental Information (NCEI)
Skip to main content
NOAA's National Centers for Environmental Information

# Monthly Climate Reports
1.   Home  
2.   Climate Monitoring  
3.   Monthly Climate Reports
Use the form below to select from a collection of monthly summaries recapping climate-related occurrences on both a global and national scale.
Report:
Year:
Month:
FOLLOW US
*   @NOAANCEI   
*   @NOAAData   
*   @NOAANCEI   
*   News Feed
CONTACT US
*   [Email: ncei.info@noaa.gov](mailto:ncei.info@noaa.gov)  
*   [Phone: (828) 271-4800](tel:8282714800)
</excerpt>

## Search 2 — query: "Denver 2020 July temp max temp min global summary of the month"
### Rank 1 of 25 — 0.71 (passed on)
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
### Rank 2 of 25 — 0.71
<excerpt title="Denver Weather: July 2020 Average Temp Makes Top 10 Warmest On ...">
# Denver Weather: July 2020 Average Temp Makes Top 10 Warmest On Record - CBS Colorado
*   Latest News  
*   Your Investigators  
*   Politics  
*   Health  
*   Business  
*   News Team  
*   Share A News Tip  
*   Making Ends Meet  
*   Colorado 150  
*   Elevating Black Voices  
*   Elevating Latino Voices

*   First Alert Weather  
*   School Closings  
*   Weather Cams  
*   Share Weather Pics  
*   Dog Walk Forecast  
*   Weather School

*   All Sports  
*   Denver Broncos  
*   Denver Nuggets  
*   Colorado Rockies  
*   Colorado Avalanche  
*   CBS Sports HQ  
*   Odds

*   Jefferson County News  
*   Arapahoe County News  
*   Adams County News  
*   Douglas County News  
*   Northern Colorado News  
*   Aurora News  
*   Denver News  
*   Boulder & Broomfield News  
*   Colorado Mountain News

*   Contests  
*   Colorado Review  
*   Colorado 150  
*   Adopt A Pet  
*   Your Local Dish  
*   Wednesday's Child  
*   Colorado Gives Day  
*   Toy Drive  
*   Advertise with Us  
*   TV Program Guide  
*   Sponsored Events  
*   Sign Up for Alerts  
*   Employment  
*   Contact Us  
*   Memorials
[[Video 2](blob:https://www.cbsnews.com/bcb5d9fa-abf6-48d6-944f-95a7e91b9103)](https://www.cbsnews.com/colorado/video/strong-winds-and-fire-danger-whips-up-wednesday/ "Watch CBS News")
FIRST ALERT WEATHER Red Flag Warning in effect across Colorado for strong winds, fire danger on Wednesday
Local News

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
</excerpt>
### Rank 3 of 25 — 0.61
<excerpt title="Denver Colorado Weather & Temperature Info">
# Weather & Climate Info
*   Home|  
*   About Denver|  
*   Resources|  
*   Weather|
Share
The biggest surprise for visitors to Denver is the climate. The arid conditions bring only 8 to 15 inches of annual precipitation and locals wake up to more than 300 days of sunshine a year. That’s more annual hours of sun than Miami and San Diego.
Winters are mild with an average daily high temperature of 45 degrees Fahrenheit and days reaching 60 degrees are not uncommon. Snow doesn't stay on the ground long in Denver so golf courses and outdoor cafes are able to stay open all year.
In summer, Denver enjoys low relative humidity, making for beautiful, sun-filled days and cool, comfortable evenings. The average daily high temperature in August is a mild 86 degrees Fahrenheit. The mild weather is due in part to the city's altitude: 5,280 feet above sea level, or exactly a mile high. Interested in having a mile-high experience? Check out these**fun places**.

# Weather & Climate Info
**Month****Avg. High (F° / C°)****Avg. Low (F° / C°)****Avg. Precip (in / mm)**  
JANUARY 47°F / 8.3C°16°F / -8.9C°0.64 in. / 16.3 mm  
FEBRUARY 49°F / 9.4C°18°F / -7.9C°0.73 in. / 18.5 mm  
MARCH 56°F / 13.3C°25°F / -3.9C°1.88 in. / 47.8 mm  
APRIL 62°F / 16.7C°33°F / 0.6C°2.20 in. / 55.9 mm  
MAY 72°F / 22.2C°42°F / 5.2C°2.56 in. / 65 mm  
JUNE 81°F / 27.2C°50°F / 10C°2.05 in. / 52.1 mm  
JULY 88°F / 31.1C°56°F / 13.3C°1.68 in. / 42.7 mm  
AUGUST 86°F / 30C°54°F / 12.2C°2.01 in. / 51.1 mm  
SEPTEMBER 78°F / 25.6C°44°F / 6.7C°1.13 in. / 28.7 mm  
OCTOBER 66°F / 18.9C°33°F / 0.6C°1.43 in. / 36.3 mm  
NOVEMBER 54°F / 12.2C°23°F / -5C°1.09 in. / 27.7 mm  
DECEMBER 46°F / 7.8C°16°F / -8.9C°0.83 in. / 21.1 mm

# Weather & Climate Info
## Tourist Information Centers
If you're offline and looking for that personal touch, head to one of the city's conveniently located tourist centers. There, you'll find…
about Tourist Information Centers

# Weather & Climate Info
## High-Altitude Tips
Denver really is a mile high, but most people don’t even notice the altitude difference. The air is just thinner and dryer. In fact, many people…
about High-Altitude Tips

# Weather & Climate Info
## Dog-Friendly Denver
Explore the best of pet-friendly Denver! Denver is home to dozens of pet-friendly activities and destinations, including dog-friendly hotels and dog…
about Dog-Friendly Denver

# Weather & Climate Info
## Retail Marijuana FAQ
As of Jan. 1, 2014, it is legal in Denver for adults over 21 to purchase marijuana for recreational use. Other municipalities in Colorado also allow…
about Retail Marijuana FAQ
</excerpt>
### Rank 4 of 25 — 0.39
<excerpt title="Denver Climatological Preview for July">
### **A Preview of Thornton's July Weather - A Hot and Stormy Month**
The Climate Prediction Center 's long range forecast unfortunately points to warmer than normal weather conditions for July. Temperature outlooks give almost the entire state a 40 to 50% chance of seeing overall above average temperatures. In terms of precipitation, the agency gives equal chances of below, above or at normal levels.
**For More Information**
Temperature Normals and Extremes for July
Monthly Temperature, Rainfall and Snowfall Extremes for July
**JULY AVERAGE STATISTICS *
Normals & Means, 1981 - 2010**
TEMPERATURE  
AVERAGE HIGH 89.4  
AVERAGE LOW 58.9  
MONTHLY MEAN 74.2  
DAYS WITH HIGH 90 OR ABOVE 16  
DAYS WITH HIGH 32 OR BELOW 0  
DAYS WITH LOW 32 OR BELOW 0  
DAYS WITH LOWS ZERO OR BELOW 0
PRECIPITATION  
MONTHLY MEAN 2.16 INCHES  
DAYS WITH MEASURABLE PRECIPITATION 8  
AVERAGE SNOWFALL 0  
DAYS WITH 1.0 INCH OR MORE SNOWFALL 0
MISCELLANEOUS JULY AVERAGES  
HEATING DEGREE DAYS 6  
COOLING DEGREES DAYS 289  
WIND SPEED (MPH)8.3 MPH  
WIND DIRECTION SOUTH  
DAYS WITH THUNDERSTORMS 11  
DAYS WITH DENSE FOG 0* (Less than 1)  
PERCENT OF SUNSHINE POSSIBLE 71

### **A Preview of Thornton's July Weather - A Hot and Stormy Month**
JULY EXTREMES  
RECORD HIGH 105 ON 7/20/2005 (TIES AS HOTTEST DENVER TEMPERATURE)  
RECORD LOW 42 ON 7/4/1903 AND 7/31/1873  
WARMEST 78.9 IN 2012  
COLDEST 67.4 IN 1895  
WETTEST 6.41 INCHES IN 1965  
MAXIMUM 24 HOUR MOISTURE 3.43 INCHES IN 1951  
DRIEST 0.01 IN 1901  
SNOWIEST (Could include hail)NO SNOWFALL EVER RECORDED IN JULY  
LEAST SNOWIEST NO SNOWFALL EVER RECORDED IN JULY
* Historical weather statistics gathered from the National Weather Service's Denver / Boulder forecast office data archives.
</excerpt>
### Rank 5 of 25 — 0.39
<excerpt title="Denver, CO Weather History">
# Denver, CO Weather History | Weather Underground
Home
Sensor Network
1.   Weather Station Network  
2.   PWS Buying Guide  
3.   Connect a Weather Station  
4.   Air Quality Sensors
Maps & Radar
1.   Wundermap  
2.   Interactive Radar  
3.   Interactive Satellite  
4.   Radar Maps  
5.   Full Maps Catalog
Severe Weather
1.   Hurricane & Tropical Cyclones  
2.   U.S. Severe Weather Map  
3.   Convective Outlook  
4.   Wildfires  
5.   Preparedness
News & Blogs
1.   Category 6  
2.   Videos  
3.   Weather Infographics  
4.   Weather Posters
Mobile Apps
1.   Weather Underground for iOS  
2.   Weather Underground for Android  
3.   All Mobile Apps
More
1.   Severe Weather  
    1.   Hurricane & Tropical Cyclones  
    2.   U.S. Severe Weather Map  
    3.   Convective Outlook  
    4.   Wildfires  
    5.   Preparedness

2.   News & Blogs  
    1.   Category 6  
    2.   Videos  
    3.   Weather Infographics  
    4.   Weather Posters

3.   Mobile Apps  
    1.   Weather Underground for iOS  
    2.   Weather Underground for Android  
    3.   All Mobile Apps

4.   Historical Weather  
5.   Discord  
6.   Legacy Site
Log InGo Ad Free
Log InGo Ad Free1.   Sensor Network  
2.   Maps & Radar  
3.   Severe Weather  
4.   News & Blogs  
Mobile AppsHistorical WeatherDiscordLegacy Site 5.   Settings
Favorites
Units°F°C Hybrid Density Comfortable Compact Appearance Auto Light DarkMember Settings
Elev **1599** m, **39.734** °N **104.991** °W

# Denver, CO
Golden Triangle Station8°Change station

# Denver, CO
## Change station
Finding stations near Denver, CO…
Hide offline- [x]
Map List
*   In use  
*   Live, °C  
*   Offline
Current station
Nearby · by distance
No other stations in view. Zoom the map out to see more.
TodayHourly10 15-DayCalendarHistory
Daily Weekly Monthly
View

# Denver, CO
## Summary
| Temperature (°C) | Max | Average | Min |  
| --- | --- | --- | --- |  
| Max Temperature | 24 | 16.78 | 12 |  
| Avg Temperature | 12.88 | 9.19 | 5.84 |  
| Min Temperature | 8 | 4.06 | 1 |
| Precipitation (mm) | Max | Average | Min | Sum |  
| --- | --- | --- | --- | --- |  
| Precipitation | 2.01 | 0.21 | 0 | 3.82 |
| Dew Point (°C) | Max | Average | Min |  
| --- | --- | --- | --- |  
| Dew Point | 6.2 | -1.71 | -7.82 |
| Wind (km/h) | Max | Average | Min |  
| --- | --- | --- | --- |  
| Wind | 48 | 23.94 | 15 |  
| Gust Wind | 61 | 48.38 | 39 |
| Sea Level Pressure (hPa) | Max | Average | Min |  
| --- | --- | --- | --- |  
| Sea Level Pressure | 831.7 | 826.04 | 818.14 |
</excerpt>

## Search 3 — query: "NCEI global summary of the month 2020 July mean max mean min station"
### Rank 1 of 50 — 0.20 (passed on)
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
### Rank 2 of 50 — 0.16
<excerpt title="Datasets | Climate Data Online (CDO)">
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
### Rank 3 of 50 — 0.13
<excerpt title="Datasets | Climate Data Online (CDO)">
# Climate Data Online: Dataset Discovery
## Climate Data Online
Level-2 NEXRAD data include three meteorological base data quantities: reflectivity, mean radial velocity, and spectrum width. With the advent of dual polarization beginning in 2011, additional base products of differential reflectivity, correlation coefficient and differential phase are available. NEXRAD Level 3 products are used to remotely detect atmospheric features, such as precipitation, precipitation-type, storms, turbulence and wind, for operational forecasting and data research analysis. More»
*   Search Tool  
    *   Mapping Tool
* * *

# Climate Data Online: Dataset Discovery
## Legacy Applications
The datasets listed below are for older system access and aren't directly accessible with the current Climate Data Online toolset, but are available through legacy servers and application.
An error occurred while loading dataset metadata. Try refreshing the page, and if the problem persists contact customer support.
*   ### Climate Indices
The U.S. Climate Divisional Dataset is the only long-term temporally and spatially complete dataset from 1895 to the present for the Contiguous United States (CONUS) from NCEI. The dataset provides temperature, precipitation and drought indices, as well as heating and cooling degree days. Coverage is provided for U.S. climate divisions, states, multi-state regions, and the nation. Text output, and static and interactive graphs are available. More»
*   Mapping Tool  
    *   FTP  
    *
Documentation & Samples  
        *   Documentation
*   ### Global Climate Station Summaries
The Global Climate Station Summaries are simple indicators of observational averages which include climatic data summarizations and frequency distributions. These typically are statistical analyses of station data over 5-, 10-, 20-, 30-year or longer time periods or for customized periods. Summaries for the following weather elements are available: Ceiling-visibility, dew point statistics, flying conditions, relative humidity, sky cover, sea-level pressure, station pressure, temperature, wind speed / direction, and present weather. Data were derived from stations observing global hourly data. These data may have conditions placed on their international commercial use. For details, please see WMO Resolution 40 or contact NCEI. More»
*   Mapping Tool  
    *
Documentation & Samples  
        *   Documentation  
        *   Data Sample
*   ### Global Hourly Data
Integrated Surface Data provides a long-term record of hourly, sub-hourly and synoptic weather observations from station networks around the world. Observation sources include the World Meteorological Organization, Automated Surface Observing System, Automated Weather Observing Stations, US Climate Reference Network, and others. Weather elements observed include sky conditions, visibility, weather type, dry bulb, wet bulb, and dew point temperatures, relative humidity, wind speed and direction, wind gusts, station and sea level pressure, altimeter, and precipitation. Online data are typically delayed for 24 hours. More»
*   Search Tool  
    *   Mapping Tool  
    *   FTP  
    *
</excerpt>
### Rank 4 of 50 — 0.11
<excerpt title="Monthly Climate Reports | Global Climate Report | July 2020">
# Monthly Climate Reports | National Centers for Environmental Information (NCEI)
Skip to main content
NOAA's National Centers for Environmental Information

# Monthly Climate Reports
1.   Home  
2.   Climate Monitoring  
3.   Monthly Climate Reports
Use the form below to select from a collection of monthly summaries recapping climate-related occurrences on both a global and national scale.
Report:
Year:
Month:
FOLLOW US
*   @NOAANCEI   
*   @NOAAData   
*   @NOAANCEI   
*   News Feed
CONTACT US
*   [Email: ncei.info@noaa.gov](mailto:ncei.info@noaa.gov)  
*   [Phone: (828) 271-4800](tel:8282714800)
</excerpt>
### Rank 5 of 50 — 0.11
<excerpt title="Datasets | Climate Data Online (CDO)">
# Climate Data Online: Dataset Discovery
## Legacy Applications
The datasets listed below are for older system access and aren't directly accessible with the current Climate Data Online toolset, but are available through legacy servers and application.
An error occurred while loading dataset metadata. Try refreshing the page, and if the problem persists contact customer support.
*   ### Climate Indices
The U.S. Climate Divisional Dataset is the only long-term temporally and spatially complete dataset from 1895 to the present for the Contiguous United States (CONUS) from NCEI. The dataset provides temperature, precipitation and drought indices, as well as heating and cooling degree days. Coverage is provided for U.S. climate divisions, states, multi-state regions, and the nation. Text output, and static and interactive graphs are available. More»
*   Mapping Tool  
    *   FTP  
    *
Documentation & Samples  
        *   Documentation
*   ### Global Climate Station Summaries
The Global Climate Station Summaries are simple indicators of observational averages which include climatic data summarizations and frequency distributions. These typically are statistical analyses of station data over 5-, 10-, 20-, 30-year or longer time periods or for customized periods. Summaries for the following weather elements are available: Ceiling-visibility, dew point statistics, flying conditions, relative humidity, sky cover, sea-level pressure, station pressure, temperature, wind speed / direction, and present weather. Data were derived from stations observing global hourly data. These data may have conditions placed on their international commercial use. For details, please see WMO Resolution 40 or contact NCEI. More»
*   Mapping Tool  
    *
Documentation & Samples  
        *   Documentation  
        *   Data Sample
*   ### Global Hourly Data
Integrated Surface Data provides a long-term record of hourly, sub-hourly and synoptic weather observations from station networks around the world. Observation sources include the World Meteorological Organization, Automated Surface Observing System, Automated Weather Observing Stations, US Climate Reference Network, and others. Weather elements observed include sky conditions, visibility, weather type, dry bulb, wet bulb, and dew point temperatures, relative humidity, wind speed and direction, wind gusts, station and sea level pressure, altimeter, and precipitation. Online data are typically delayed for 24 hours. More»
*   Search Tool  
    *   Mapping Tool  
    *   FTP  
    *
</excerpt>

## Search 4 — query: "site:ncei.noaa.gov "datasetid=GSOM""
### Rank 1 of 16 — 0.15 (passed on)
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
### Rank 2 of 16 — 0.14
<excerpt title="GSOM (Global Summary of the Month) documentation">
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

## [PDF page 2]
GHCN-Daily Dataset Measurement Flag (M) These flags that pertain to temperature, precipitation and  
wind measurement are given in the attribute fields following many of the data variables described  
below as noted.
Blank = no measurement information applicable
A =  value in precipitation or snow is a multi  -day total, accumulated since last measurement  
(used on Daily Form pdf file)  
B = precipitation total formed from two twelve  -hour totals  
D = precipitation total formed from four six  -hour totals  
H = represents highest or lowest hourly temperature (TMAX or TMIN)  or average o  f hourly values  
(TAVG)  
K = converted from knots  
L = temperature appears to be lagged with respect to reported  hour of observation  
O = converted from oktas  
P = identified as "missing presumed zero" in DSI 3200 and 3206  
T = trace of precipitation, snowfall, or snow depth  
W = converted from 16  -point WBAN code (for wind direction)
Table A (variables)
AWND – Monthly Average Wind Speed. Given in miles per hour for PDF output and miles per hour or  
meters per second  depending on user specification  for CSV output. Missing if more than 5 days within  
the month are missing or flagged or if more than 3 consecutive values with  in the month are missing or  
flagged.
AWND_ATTRIBUTES  – a,S where:
a = DaysMissing (Numeric value): The number of days (from 1 to 5) missing or flagged is provided  
S = GHCN-Daily Dataset Source Code (values are given  below in Table B)
CDSD – Cooling Degree Days (season  -to-date). Running total of monthly cooling degree days through the  
end of the most recent month.  Each month is summed to produce a  season-to-date total. Season starts  
in January in Northern Hemisphere and July in Southern Hemisphere. Given in Fahrenheit degrees in  
PDF output and Celsius or Fahrenheit degrees depending on user specification  in CSV output.
CDSD_ATTRIBUTES – S where:
S = GHCN-Daily Dataset Source Code (values are given below in Table B  )
</excerpt>
### Rank 3 of 16 — 0.12
<excerpt title="GSOM (Global Summary of the Month) documentation">
## [PDF page 8]
PRCP – Total Monthly Precipitation. Given in inches for PDF output. CSV output is in inches or  
millimeters  depending on user  specification.  Measurement Flags: T is used for trace amount, a is used  
for any accumulation within a month that includes missing days. If no days are missing, no flag is used.
PRCP_ATTRIBUTES  = a,M,Q,S where:
a = DaysMissing (Numeric value): The number  of days (from 1 to 5) missing or flagged is provided  
M = GHCN-Daily Dataset Measurement Flag (values are given below in Table C)  
Q = GHCN  -Daily Dataset Quality Flag (values are given below in Table D)  
S = GHCN-Daily Dataset Source Code (values are given b  elow in Table B)
PSUN – Monthly Average of the daily percents of possible sunshine  .

## [PDF page 9]
PSUN_ATTRIBUTES – a,S where:
a = DaysMissing (Numeric value): The number of days (from 1 to 5) missing or flagged is provided  
S = GHCN-Daily Dataset Source Code (values are given below in Table B)
SNOW – Total Monthly Snowfall. Given in inches for PDF output. CSV output is in inches or millimeters  
depending on user specification. Measurement Flags: T is used for trace amount, a is used for any  
accumulation within a month that includes missing days. If no days are missing, no flag is used. Source  
Flag: Source flag from GHCN-Daily (see separate documentation for GHCN-Daily). Days Miss Flag:  
Number of days missing or flagged.
SNOW_ATTRIBUTES = a,M,Q,S where:
a = DaysMissing  (Numeric value): The number of days (from 1 to 5) missing or flagged is provided  
M = GHCN-Daily Dataset Measurement Flag (values are given below in Table C)  
Q = GHCN  -Daily Dataset Quality Flag (values are given below in Table D)  
S = GHCN-Daily Dataset Sou  rce Code (values are given below in Table B)
TAVG – Average Monthly Temperature. Computed by adding  the unrounded monthly/annual maximum  
and minimum temperatures and dividing by 2.  Fahrenheit units on PDF output. CSV output is  Fahrenheit  
or Celsius units  depending on user specification  . Missing if more than 5 days within the month are  
missing or flagged or if more than 3 consecutive values within the month are missing or flagged.
TAVG_ATTRIBUTES  – a,S where:
a = DaysMissing (Numeric value): The number o  f days (from 1 to 5) missing or flagged is provided  
S = GHCN-Daily Dataset Source Code (values are given below in Table B)
TMAX – Monthly Maximum Temperature.  Average of daily maximum temperature given in Fahrenheit  
on PDF output. CSV output is given in  Fahrenheit or Celsius depending on user specification. Missing if  
more than 5 days within the month are missing or flagged or if more than 3 consecutive values within  
the month are missing or flagged.
TMAX_ATTRIBUTES  = a,M,Q,S where:

## [PDF page 9]
a = DaysMissing (Nu  meric value): The number of days (from 1 to 5) missing or flagged is provided  
M = GHCN-Daily Dataset Measurement Flag (values are given below in Table C)  
Q = GHCN  -Daily Dataset Quality Flag (values are given below in Table D)  
S = GHCN-Daily Dataset Source  Code (values are given below in Table B)
TMIN – Monthly Minimum Temperature.  Average of daily m  inimum temperature given in Fahrenheit  
units on PDF output. CSV output is given in  Fahrenheit or Celsius units depending on user specification  .  
Missing if more than 5 days within the month are missing or flagged or if more than 3 consecutive values  
within the month are missing or flagged.
TMIN_ATTRIBUTES = a,M,Q,S where:
a = DaysMissing (Numeric value): The number of days (from 1 to 5) missing or flagged is p  rovided
</excerpt>
### Rank 4 of 16 — 0.07
<excerpt title="GSOM (Global Summary of the Month) documentation">
## [PDF page 9]
a = DaysMissing (Nu  meric value): The number of days (from 1 to 5) missing or flagged is provided  
M = GHCN-Daily Dataset Measurement Flag (values are given below in Table C)  
Q = GHCN  -Daily Dataset Quality Flag (values are given below in Table D)  
S = GHCN-Daily Dataset Source  Code (values are given below in Table B)
TMIN – Monthly Minimum Temperature.  Average of daily m  inimum temperature given in Fahrenheit  
units on PDF output. CSV output is given in  Fahrenheit or Celsius units depending on user specification  .  
Missing if more than 5 days within the month are missing or flagged or if more than 3 consecutive values  
within the month are missing or flagged.
TMIN_ATTRIBUTES = a,M,Q,S where:
a = DaysMissing (Numeric value): The number of days (from 1 to 5) missing or flagged is p  rovided

## [PDF page 10]
M = GHCN-Daily Dataset Measurement Flag (values are given below in Table C)  
Q = GHCN-Daily Dataset Quality Flag (values are given below in Table D)  
S = GHCN-Daily Dataset Source Code (values are given below in Table B)
TSUN – Monthly total sunshine in minutes.
TSUN_ATTRIBUTES – a,S where:
a = DaysMissing (Numeric value): The number of days (from 1 to 5) missing or flagged is provided  
S = GHCN-Daily Dataset Source Code (values are given below in Table B)
WDF1 – Wind Direction for Maximum Wind Speed/Fastest 1-Minute (WSF1). Given in 360-degree  
compass point directions (e.g. 360 = north, 180 = south, etc.). Missing if more than 5 days within the  
month are missing or flagged or if more than 3 consecutive values within the month are missing or  
flagged.
WDF1_ATTRIBUTES – a,S where:
a = DaysMissing (Numeric value): The number of days (from 1 to 5) missing or flagged is provided  
S = GHCN-Daily Dataset Source Code (values are given below in Table B)
WDF2 – Wind Direction for Maximum Wind Speed/Fastest 2-Minute (WSF2). Given in 360-degree  
compass point directions (e.g. 360 = north, 180 = south, etc.). Missing if more than 5 days within the  
month are missing or flagged or if more than 3 consecutive values within the month are missing or  
flagged.
WDF2_ATTRIBUTES  – a,S where:
a = DaysMissing (Numeric value): The number of days (from 1 to 5) missing or flagged is provided  
S = GHCN-Daily Dataset Source Code (values are given below in Table B)
WDF5 – Wind Direction for Peak Wind Gust Speed  – Fastest 5-second (WSF5). Given in 360  -degree  
compass point directions (e.g. 360 = north, 180 = south, etc.).  Missing if more than 5 days within the  
month are missing or flagged or if more than 3 consecutive values within the month are missing or  
flagged.

## [PDF page 10]
WDF5_ATTRIBUTES – a,S where:
a = DaysMissing (Numeric value): The number of days (from 1 to 5) missing or flagged is provided  
S = GHCN-Daily Dataset Source Code (values are given below in Table B)
WDFG – Wind Direction for Peak Wind Gust Speed (WSFG). Given in 360  -degree compass point  
directions (e.g. 360 = north, 180 = south, etc.).  Missing if more than 5 days within the month are missing  
or flagged or if more than 3 consecutive values within the month are missing or flagged.
WDFG_ATTRIBUTES – a,S where:
a = DaysMissing (Numeric value): The number of days (from 1 to 5) missing or flagged is provided
</excerpt>
### Rank 5 of 16 — 0.07
<excerpt title="GSOM (Global Summary of the Month) documentation">
## [PDF page 4]
a = DaysMissing (Numeric value): The number of days (from 1 to 5) missing or flagged is provided  
M = GHCN-Daily Dataset Measurement Flag  (values are given below in Table C)  
S = GHCN-Daily Dataset Source Code (values are given below in Table B)  
cc = two-digit date during the month when the EMNT value occurred (always latest date if more than  
one occurrence)

## [PDF page 5]
d = + if there is more than one date of occurrence, blank if only one date of occurrence
EMSN – Highest daily snowfall in the month. Given in inches for PDF output. CSV output is in inches or  
millimeters depending on user specification.
EMSN_ATTRIBUTES – a,M,S,cc,d where:
a = DaysMissing (Numeric value): The number of days (from 1 to 5) missing or flagged is provided  
M = GHCN-Daily Dataset Measurement Flag (values are given below in Table C)  
S = GHCN-Daily Dataset Source Code (values are given below in Table B)  
cc = two-digit date during the month when the EMNT value occurred (always latest date if more than  
one occurrence)  
d = + if there is more than one date of occurrence, blank if only one date of occurrence
EMXP – Highest daily total of precipitation in the month. Given in inches for PDF output. CSV output is in  
inches or millimeters depending on user specification.
EMXP_ATTRIBUTES – a,M,S,cc,d where:
a = DaysMissing (Numeric value): The number of days (from 1 to 5) missing or flagged is provided  
M = GHCN-Daily Dataset Measurement Flag (values are given below in Table C)  
S = GHCN-Daily Dataset Source Code (values ar  e given below in Table B)  
cc = two-digit date during the month when the EMNT value occurred (always latest date if more than  
one occurrence)  
d = + if there is more than one date of occurrence, blank if only one date of occurrence
EMXT – Extreme maximum temperature for month. Highest daily maximum temperature for the month.  
Given in Fahrenheit units on PDF output. CSV output is Fahrenheit or Celsius units depending on user  
specification.
EMXT_ATTRIBUTES – a,S,cc,d where:
a = DaysMissing (Numeric value): The number of days (from 1 to 5) missing or flagged is provided  
S = GHCN-Daily Dataset Source Code (values are given below in Table B)  
cc = two-digit date during the month when the EMNT value occurred (always latest date if more than  
one occurrence)  
d = + if there is more than one date of occurrence, blank if only one date of occurrence

## [PDF page 5]
EVAP – Total Monthly Evaporation. Given in inches for PDF output. CSV output is in inches or millimeters  
depending on user specification.  Measurement Flags: T is used for tr  ace amount, a is used for any  
accumulation within a month that includes missing days. If no days are missing, no flag is used. Source  
Flag: Source flag from GHCN-Daily (see separate documentation for GHCN  -Daily). Days Miss Flag:  
Number of days missing or flagged.
EVAP_ATTRIBUTES = a,M,Q,S where:
a = DaysMissing (Numeric value): The number of days (from 1 to 5) missing or flagged is provided  
M = GHCN-Daily Dataset Measurement Flag (values are given below in Table C)
</excerpt>

## Search 5 — query: "https://www.ncei.noaa.gov/access/services/data/v1?datasetid=GSOM&stations=USW00003017&startDate=2020-07-01&endDate=2020-07-31&dataTypes=MEAN_MAX,MEAN_MIN&format=csv"
### Rank 1 of 50 — 0.10 (passed on)
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
### Rank 2 of 50 — 0.09
<excerpt title="Dataset - NCEI Search, Discovery, & Data Access - NOAA">
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

# Dataset Search
##### Global Summary of the Month (GSOM), Version 1
###### 1763-01-01 to 2026-11-18
Find out more  
WMO Telecommunications Abbreaviated Heading TTAAii from WMO No. 386 Manual on the Global Telecommunication System
Find out more If your search results exceed the order size restrictions of this dataset certain actions like 'Select All' may be disabled. Order sizes are restricted to reduce wait times. Each dataset has a **file count limit.** Orders are only certifiable up to **7 days after completion.** If this time frame has passed you will need to reorder the data to start the certification process.   
Orders can be downloaded up to **7 days after completion.** If this time frame has expired you need to reorder the data to download it again.
If your search results exceed the order size restrictions of this dataset certain actions like "Select All" may be disabled. Order sizes are restricted to reduce wait times. Each dataset has a **file count limit.** Downloadable  Search and download data immediately.  Orderable  Request data be retrieved, subsetted, or converted.  Certifiable  Data that can be legally certified, for a fee.

# Dataset Search
##### Follow Us
*   @NOAANCEI  
*   @NOAAData  
*   @NOAANCEI  
*   News Feed

# Dataset Search
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
</excerpt>
### Rank 3 of 50 — 0.06
<excerpt title="Dataset - NCEI Search, Discovery, & Data Access - NOAA">
# NCEI Search, Discovery, & Data Access
Skip to feedbackSkip to main content
An official website of the United States government  Here's how you know
The .gov means it’s official.
Federal government websites often end in .gov or .mil. Before sharing sensitive information, make sure you’re on a federal government site.
The site is secure.
The **https://** ensures that you are connecting to the official website and that any information you provide is encrypted and transmitted securely.
1.   **NCEI Search, Discovery, & Data Access**  
2.   **Collection Search**
*   **API Documentation**  
    *   Data ServiceOrder ServiceSearch ServiceSupport Service

*   **Order Status**  
*   **Cart**
Please Note: NCEI is currently moving its data and applications to the cloud. This upgrade may result in temporary data access delays. Please see our cloud migration overview and frequently asked questions for more information and resources. Check theNCEI Alerts page for impacted products and datasets.Current Impact: Expect delayed data archival and slower update cycles for many products.

# NCEI Search, Discovery, & Data Access
## Search Options
Use the following search options to narrow down your results.
*   Dataset Search   Datasets   GSOY   
*      
*      
*   When  Start Date  - [x] Select Date Range     
*      
*   Where  Ex: North Carolina    
*      
*      
*   Accessibility  - [x] Downloadable  - [x] Orderable  - [x] Certifiable    
*      
*      
*      
*      
*
Advanced Options
Clear All Searches

# Dataset Search
Search some of our most popular datasets by name or by any of the search options.
2 collections found
Showing **2** of 2 available collections
MapLibre

# Dataset Search
##### Global Summary of the Year (GSOY), Version 1
###### 1763-01-01 to 2026-11-18
This Global Summaries dataset, known as GSOY for Yearly, contains a yearly resolution of meteorological elements from 1763 to present with updates applied weekly. The major parameters are: – average annual temperature, average annual minimum and maximum temperatures; total annual precipitation and snowfall; departure from normal of the mean temperature and total precipitation; heating and cooling degree days; number of days that temperatures and precipitation are above or below certain thresholds; extreme annual minimum and maximum temperatures; number of days with fog; and number of days with thunderstorms. The primary input data source is the Global Historical Climatology Network - Daily (GHCN-Daily) dataset. The Global Summaries datasets also include a monthly resolution of meteorological elements in the GSOM (for Monthly) dataset. See associated resources for more information. These datasets are not to be confused with "GHCN-Monthly", "Annual Summaries" or "NCDC Summary of the Month". There are unique elements that are produced globally within the GSOM and GSOY data files. There are also bias corrected temperature data in GHCN-Monthly, which are not available in GSOM and GSOY. The GSOM and GSOY datasets replace the legacy U.S. COOP Summaries (DSI-3220), and have been expanded to include non-U.S. (global) stations. U.S. COOP Summaries (DSI-3220) only includes National Weather Service (NWS) COOP Published, or "Published in CD", sites.
Topics / Keyword Tags
</excerpt>
### Rank 4 of 50 — 0.04
<excerpt title="Dataset - NCEI Search, Discovery, & Data Access - NOAA">
# Dataset Search
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

# Dataset Search
## NCEI Customer Experience Survey
This survey is designed to measure your level of satisfaction with ncei.noaa.gov. It consists of nine questions and should take approximately two to five minutes to complete.
Please do not use this survey to provide comments on or responses to rules, notices, solicitations or other official agency actions. Any information you provide will be used for the sole purpose of improving NOAA's digital products and services. You may also send us an email at [ncei-digital.experience@noaa.gov](mailto:ncei-digital.experience@noaa.gov).  
If you have comments concerning the accessibility of our website, please submit your feedback on our accessibility page.
A red asterisk (*) indicates a required field.

# Dataset Search
## NCEI Customer Experience Survey
### Success
Thank you. Your feedback has been received.

# Dataset Search
## NCEI Customer Experience Survey
### Error
alert message
It was easy to complete what I needed to do. *
👍 Yes
👎 No
It took a reasonable amount of time to do what I needed to do. *
Select one
Strongly Disagree
Disagree
Neutral
Agree
Strongly Agree
I am satisfied with the information/service I received from NCEI. *
Select one
Strongly Disagree
Disagree
Neutral
Agree
Strongly Agree
To help us address your feedback, please share the web address/link (URL) of a page that you are referring to.
Paste link below:
This site is well organized *
Select one
Strongly Disagree
Disagree
Neutral
Agree
Strongly Agree
What is your primary reason for visiting this site? *
Which category best describes you? *
How often do you visit this site? *
If you were unable to accomplish your task, let us know why.
Choose One
The website was not user-friendly or easy to navigate
Technical difficulties
I couldn't find the information I was looking for
The site's design was confusing
The site did not support the browser or device I was using
Other
Enter other text
Do you have suggestions for improving this website?   1000 characters allowed
Submit
* * *
To provide feedback outside of the scope of this survey, please contact us at [ncei-digital.experience@noaa.gov](mailto:%20ncei-digital.experience@noaa.gov).
This survey is designed to measure your level of satisfaction with the NCEI website. It consists of nine questions and should take approximately two to five minutes to complete. Please do not use this survey to provide comments on or responses to rules, notices, solicitations or other official agency actions. Any information you provide will be used to for the sole purpose of improving NOAA's digital products and services.
An official form of the United States government. Provided by Touchpoints
OMB Approval #0690-0030 · Expiration Date 09/30/2029
</excerpt>
### Rank 5 of 50 — 0.04
<excerpt title="MSHR - National Centers for Environmental Information (NCEI)">
# Master Station History Report
## MSHR
|  |  
| --- |  
| Theme keywords | Global Change Master Directory (GCMD) Science Keywords * Earth Science > Atmosphere > Altitude > Station Height * Earth Science > Human Dimensions > Infrastructure |  
| Data Center keywords | Global Change Master Directory (GCMD) Data Center Keywords * DOC/NOAA/NESDIS/NCEI > National Centers for Environmental Information, NESDIS, NOAA, U.S. Department of Commerce * DOC/NOAA/NESDIS/NCDC > National Climatic Data Center, NESDIS, NOAA, U.S. Department of Commerce |  
| Platform keywords | Global Change Master Directory (GCMD) Platform Keywords * Meteorological Stations * In Situ Land-based Platforms > Weather Stations/Networks > Weather Stations * In Situ Land-based Platforms > Ocean Platform/Ocean Stations > Coastal Stations * Fixed Observation Stations * Ground Stations |  
| Instrument keywords | Global Change Master Directory (GCMD) Instrument Keywords * In Situ/Laboratory Instruments > Temperature/Humidity Sensors > Thermometer * Rain Gauges |  
| Place keywords | Global Change Master Directory (GCMD) Location Keywords * Continent > North America > United States Of America * Geographic Region > Global |  
| Project keywords | Global Change Master Directory (GCMD) Project Keywords * GHCN > Global Historical Climatology Network |  
| Stratum keywords | Global Change Master Directory (GCMD) Location Keywords * Vertical Location > Land Surface |

# Master Station History Report
## MSHR
|  |  
| --- |  
| Use Constraints | * Cite this dataset when used as a source. * This dataset continues to be produced to support legacy processing systems. Users are advised, when possible, to use the Enhanced Master Station History Report. * Use liability: NOAA and NCEI cannot provide any warranty as to the accuracy, reliability, or completeness of furnished data. Users assume responsibility to determine the usability of these data. The user is responsible for the results of any application of this data for other than its intended purpose. |  
| Access Constraints | * Distribution liability: NOAA and NCEI make no warranty, expressed or implied, regarding these data, nor does the fact of distribution constitute such a warranty. NOAA and NCEI cannot assume liability for any damages caused by any errors or omissions in these data. If appropriate, NCEI can only certify that the data it distributes are an authentic copy of the records that were accepted for inclusion in the NCEI archives. |  
| Fees | * In most cases, electronic downloads of the data are free. However, fees may apply for custom orders, data certifications, copies of analog materials, and data distribution on physical media. |
Lineage information for: dataset Lineage Statement The Master Station History Report is a list of basic, historical information for every station in the Station History database. The data incorporates data from multiple sources, primarily the National Weather Service (NWS) Cooperative Observing Program. The report is created from data entered into the Master Station History Database. The database incorporates station history information from physical/analog forms and digitally submitted station history information.
Lineage information for: repository Processing Steps*   2015-04-22T00:00:00 - NOAA created the National Centers for Environmental Information (NCEI) by merging NOAA's National Climatic Data Center (NCDC), National Geophysical Data Center (NGDC), and National Oceanographic Data Center (NODC), including the National Coastal Data Development Center (NCDDC), per the Consolidated and Further Continuing Appropriations Act, 2015, Public Law 113-235. NCEI launched publicly on April 22, 2015.
Last Modified: 2023-06-23

# Master Station History Report
## MSHR
For questions about the information on this page, please email: [ncei.info@noaa.gov](mailto:ncei.info@noaa.gov?Master%20Station%20History%20Report)
*   About  
*   Contact  
*   Employment  
*   Site Map

*   Privacy  
*   FOIA  
*   Information Quality  
*   Disclaimer

*   Take Our Survey  
*   Department of Commerce  
*   NOAA  
*   NESDIS
Department of Commerce>NOAA>NESDIS>NCEI
</excerpt>

## Search 6 — query: "https://www.ncei.noaa.gov/access/services/data/v1?datasetid=GSOM&stations=USW00003017&startDate=2020-07-01&endDate=2020-07-31&dataTypes=MEAN_MAX,MEAN_MIN&format=csv"
(no page could be scored)

## Search 7 — query: "Denver International Airport station ID NCEI"
### Rank 1 of 210 — 0.51 (passed on)
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
### Rank 2 of 210 — 0.22
<excerpt title="Denver International Airport">
Jump to content  
Main menu  
Search  
Donate  
Create account  
Log in  
Contents hide  
(Top)  
History  
Facilities  
Toggle Facilities subsection  
Terminal  
Security  
Art and aesthetics  
Ground transportation  
Conspiracy theories  
Toggle Conspiracy theories subsection  
Theories  
Airlines and destinations  
Toggle Airlines and destinations subsection  
Passenger  
Cargo  
Statistics  
Toggle Statistics subsection  
Top destinations  
Airline market share  
Annual traffic  
Accidents and incidents  
See also  
References  
External links  
Denver International Airport  
49 languages  
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
This article is about the current airport open since 1995. For the previous airport, see Stapleton International Airport.  
"Denver Airport" redirects here. For the rail station, see Denver Airport station.  
Denver International Airport
Aerial view in 2023
IATA: DENICAO: KDENFAA LID: DENWMO: 72565
Summary  
Airport type	Public  
Owner	City & County of Denver  
Operator	City & County of Denver Department of Aviation  
Serves	  
Denver metropolitan area  
Front Range Urban Corridor
Location	Northeast Denver, Colorado, U.S.  
Opened	February 28, 1995; 31 years ago  
Hub for	United Airlines  
Operating base for	  
Frontier Airlines  
Southwest Airlines[1]
Time zone	MST (UTC−07:00)  
 • Summer (DST)	MDT (UTC−06:00)  
Elevation AMSL	5,434 ft (1,656 m)  
Coordinates	39°51′42″N 104°40′23″W  
Public transit access	  at Denver Airport  
Website	flydenver.com  
Maps
FAA airport diagram
Wikimedia | © OpenStreetMap  
Interactive map of Denver International Airport
Runways
</excerpt>
### Rank 3 of 210 — 0.15
<excerpt title="Denver, Denver International Airport">
Nov 17, 7:40 am	34	28	80	31	S	3	10.00	 	SCT001 SCT003	 	24.55	29.96	 	 	 	   
Nov 17, 7:35 am	34	28	80	31	SW	3	10.00	 	SCT001 SCT003	 	24.55	29.96	 	 	 	   
Nov 17, 7:30 am	36	28	75	33	SSE	3	10.00	 	SCT001 SCT003	 	24.55	29.96	 	 	 	   
Nov 17, 7:25 am	36	28	75	30	WSW	7	10.00	 	SCT001 SCT003	 	24.55	29.96	 	 	 	   
Nov 17, 7:20 am	34	28	80	27	WSW	8	10.00	 	SCT001 SCT003	 	24.55	29.96	 	 	 	   
Nov 17, 7:15 am	34	28	80	28	WSW	7	10.00	 	SCT001 SCT003	 	24.55	29.96	 	 	 	   
Nov 17, 7:10 am	34	28	80	27	WSW	8	10.00	 	CLR	 	24.55	29.96
</excerpt>
### Rank 4 of 210 — 0.14
<excerpt title="Denver, Denver International Airport">
Nov 16, 9:40 am	50	34	54	47	W	7	10.00	 	CLR	 	24.73	30.18	 	 	 	   
Nov 16, 9:35 am	48	34	57	46	W	5	10.00	 	CLR	 	24.73	30.18	 	 	 	   
Nov 16, 9:30 am	50	34	54	47	W	7	10.00	 	CLR	 	24.73	30.18	 	 	 	   
Nov 16, 9:25 am	48	35	62	45	W	7	10.00	 	CLR	 	24.73	30.18	 	 	 	   
Nov 16, 9:20 am	48	35	62	45	W	7	10.00	 	CLR	 	24.73	30.18	 	 	 	   
Nov 16, 9:15 am	48	34	57	45	W	7	10.00	 	CLR	 	24.73	30.18	 	 	 	   
Nov 16, 9:10 am	46	35	66	44	W	6	10.00	 	CLR	 	24.73	30.18	 	 	 	   
Nov 16, 9:05 am	46	34	61	44	W	6	10.00	 	CLR	 	24.73	30.18
</excerpt>
### Rank 5 of 210 — 0.14
<excerpt title="Denver, Denver International Airport">
Nov 18, 7:05 am	41	19	41	39	WSW	3	10.00	 	CLR	 	24.51	29.91	 	 	 	   
Nov 18, 7:00 am	39	19	44	34	WSW	7	10.00	 	CLR	 	24.50	29.90	 	 	 	   
Nov 18, 6:55 am	39	19	44	34	WSW	7	10.00	 	CLR	 	24.50	29.90	 	 	 	   
Nov 18, 6:53 am	40	19	43	35	WSW	7	10.00	 	FEW080 FEW150 FEW220	1010.90	24.50	29.90	 	 	 	   
Nov 18, 6:50 am	39	19	44	34	WSW	7	10.00	 	FEW080	 	24.50	29.90	 	 	 	   
Nov 18, 6:45 am	41	19	41	35	W	9	10.00	 	FEW080	 	24.50	29.90	 	 	 	   
Nov 18, 6:40 am	43	19	39	37	W	10	10.00	 	FEW080	 	24.50	29.90
</excerpt>

## Search 8 — query: "Hartsfield Jackson International Airport station id NCEI"
### Rank 1 of 594 — 0.77 (passed on)
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
### Rank 2 of 594 — 0.68
<excerpt title="Find A Station - NCEI Search, Discovery, & Data Access - NOAA">
Automated Surface Observing System One Minute Page 1  
+3  
GHCND  
:  
USW00024030  
GHCND  
:  
USW00024030  
+14  
Jul 1928 - Present  
41.0993, -102.9864  
 View Details  
 Select  
ATLANTA HARTSFIELD-JACKSON INTERNATIONAL AIRPORT  
ATLANTA HARTSFIELD INTERNATIONAL AIRPORT  
ATLANTA WSFO  
+4  
Automated Surface Observing System Five Minute  
Automated Surface Observing System One Minute Page 1  
+3  
GHCND  
:  
USW00013874  
GHCNMLT  
:  
USW00013874  
+8  
Nov 1928 - Present  
33.6297, -84.4422  
 View Details  
 Select  
BIRMINGHAM ARPT ASOS  
BIRMINGHAM FAA AP  
BIRMINHAM WSO AP  
+3  
Automated Surface Observing System One Minute Page 2  
COOP Data / Record of Climatological Observations Publication  
+1  
GHCND  
:  
USW00013876  
GHCNMLT  
:  
USW00013876  
+8  
Nov 1928 - Present  
33.5654, -86.7449  
 View Details  
 Select  
GREENSBORO/PIEDMONT TRIAD INTERNATIONAL AIRPORT  
GREENSBORO AP  
GREENSBORO WSO AIRPORT  
+4  
Automated Surface Observing System One Minute Page 2  
COOP Data / Record of Climatological Observations Publication  
+1  
GHCND  
:  
USW00013723  
GHCNMLT  
:  
USW00013723  
+8  
Nov 1928 - Present  
36.0969, -79.9432  
 View Details  
 Select  
LARAMIE AP  
LARAMIE REGIONAL AP  
LARAMIE FAA AIRPORT  
+4  
Automated Surface Observing System Five Minute  
Automated Surface Observing System One Minute Page 1  
+3
</excerpt>
### Rank 3 of 594 — 0.55
<excerpt title="Past Weather | National Centers for Environmental Information (NCEI)">
1998-06-17—2026-11-02
*   ATLANTA 3.2 S, GA US US1GAFT0037
2001-06-10—2026-10-31
*   NORTH DECATUR 3.0 NNE, GA US US1GADK0007
2008-07-14—2026-10-18
*   MARIETTA 8.3 NE, GA US US1GACB0016
2009-03-04—2026-09-04
*   JONESBORO 1.0 N, GA US US1GACN0009
2023-02-10—2026-03-13
*   SMYRNA 0.2 ESE, GA US US1GACB0068
2022-06-17—2025-09-26
*   DECATUR 2.6 NE, GA US US1GADK0041
2015-09-25—2025-05-21
*   DUNWOODY 1.2 SW, GA US US1GADK0036
2014-05-26—2024-12-16
*   TUCKER 2.3 W, GA US US1GADK0002
2008-05-01—2024-09-26
*   MARIETTA 5.8 W, GA US US1GACB0074
2023-08-30—2024-08-15
*   NORTH DECATUR 2.6 N, GA US US1GADK0009
2008-09-04—2024-08-08
*   COLLEGE PARK 1.6 NNW, GA US US1GAFT0067
</excerpt>
### Rank 4 of 594 — 0.54
<excerpt title="Daily Summaries Station Details: ATLANTA HARTSFIELD JACKSON ...">
# Daily Summaries Station Details: ATLANTA HARTSFIELD JACKSON INTERNATIONAL AIRPORT, GA US, GHCND:USW00013874 | Climate Data Online (CDO) | National Climatic Data Center (NCDC)
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
| Name | ATLANTA HARTSFIELD JACKSON INTERNATIONAL AIRPORT, GA US |  
| Network:ID | GHCND:USW00013874 |  
| Latitude/Longitude | 33.62972°, -84.44224° |  
| Elevation | 308.2 m |
| Period of Record |  
| --- |  
| Start Date ¹ | 1930-01-01 |  
| End Date ¹ | 2026-11-13 |  
| Data Coverage² | 100% |
Add to Cart
Zoom in
Zoom out
Esri, CGIAR, USGS
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
*   Sky cover & clouds  
*   Sunshine  
*   Water  
*   Weather Type  
*   Wind

# Daily Summaries Station Details
## Station Data Inventory, Access & History
### General History
*   1928 to Present

# Daily Summaries Station Details
## Station Data Inventory, Access & History
### Location History
*   1928 to Present

# Daily Summaries Station Details
## Station Data Inventory, Access & History
### Equipment History
*   1928 to Present

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
### Rank 5 of 594 — 0.50
<excerpt title="Normals Hourly Station Details: ATLANTA HARTSFIELD JACKSON ...">
# Normals Hourly Station Details: ATLANTA HARTSFIELD JACKSON INTERNATIONAL AIRPORT, GA US, GHCND:USW00013874 | Climate Data Online (CDO) | National Climatic Data Center (NCDC)
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

# Normals Hourly Station Details
| Station Details |  
| --- |  
| Name | ATLANTA HARTSFIELD JACKSON INTERNATIONAL AIRPORT, GA US |  
| Network:ID | GHCND:USW00013874 |  
| Latitude/Longitude | 33.62972°, -84.44224° |  
| Elevation | 308.2 m |
| Period of Record |  
| --- |  
| Start Date ¹ | 2010-01-01 |  
| End Date ¹ | 2010-12-31 |  
| Data Coverage² | 100% |
Add to Cart
Zoom in
Zoom out
Esri, CGIAR, USGS
Powered by Esri

# Normals Hourly Station Details
## Station Data Inventory, Access & History
### Available Data Types
*   Air Temperature  
*   Degree Days  
*   Pressure  
*   Sky cover & clouds  
*   Wind

# Normals Hourly Station Details
## Station Data Inventory, Access & History
### General History
*   1928 to Present

# Normals Hourly Station Details
## Station Data Inventory, Access & History
### Location History
*   1928 to Present

# Normals Hourly Station Details
## Station Data Inventory, Access & History
### Equipment History
*   1928 to Present

# Normals Hourly Station Details
## Station Data Inventory, Access & History
### Documentation
*   Documents

# Normals Hourly Station Details
## View Station Data Help
View Station Data is a web based interface which allows easy access to NCDC's station databases. Data coverage is stored based on observations over a specific period of time whether annually, monthly, or daily. The date range changes based on the selected dataset.
Select the date range to choose a time period. Then click on the "VIEW DATA" button. If you find that you need more guidance, contact our customer support team.
</excerpt>

## Search 9 — query: "Los Angeles International Airport station id NCEI usw"
### Rank 1 of 72 — 0.67 (passed on)
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
### Rank 2 of 72 — 0.62
<excerpt title="Daily Summaries Station Details: LOS ANGELES INTERNATIONAL ...">
# Daily Summaries Station Details: LOS ANGELES INTERNATIONAL AIRPORT, CA US, GHCND:USW00023174 | Climate Data Online (CDO) | National Climatic Data Center (NCDC)
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
| Name | LOS ANGELES INTERNATIONAL AIRPORT, CA US |  
| Network:ID | GHCND:USW00023174 |  
| Latitude/Longitude | 33.93816°, -118.3866° |  
| Elevation | 29.7 m |
| Period of Record |  
| --- |  
| Start Date ¹ | 1944-01-01 |  
| End Date ¹ | 2026-11-13 |  
| Data Coverage² | 99% |
Add to Cart
Zoom in
Zoom out
Esri, CGIAR, USGS
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
*   Sky cover & clouds  
*   Sunshine  
*   Water  
*   Weather Type  
*   Wind

# Daily Summaries Station Details
## Station Data Inventory, Access & History
### General History
*   1930 to Present

# Daily Summaries Station Details
## Station Data Inventory, Access & History
### Location History
*   1930 to Present

# Daily Summaries Station Details
## Station Data Inventory, Access & History
### Equipment History
*   1930 to Present

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
### Rank 3 of 72 — 0.53
<excerpt title="LOS ANGELES INTL AP (United States) | SSOD Explorer">
## About the selected station
### Los Angeles International Airport, United States — UTC daily summaries
This is the NOAA station named LOS ANGELES INTL AP, located near the Pacific coast in southwestern Los Angeles. Marine air and coastal cloud often moderate this airport site relative to downtown Los Angeles and inland valleys, so its readings should not be treated as basin-wide averages.
Station USW00023174 · California, United States Location 33.9381°N, 118.3867°W · 29.6 m elevation Inventory range 1931–2026; variable availability and continuity differ.

## About the selected station
### Los Angeles International Airport, United States — UTC daily summaries
#### What is available in the checked year
The checked 2025 file contains 362 rows across 362 of 365 UTC dates. Missing dates: 30 Aug, 31 Aug, 01 Sep. This check does not establish completeness for earlier years.
2025 station file availability · Source: NOAA/NCEI SSODv2
| Variable | Available numeric values | Dates represented |  
| --- | --- | --- |  
| Mean temperature | 361 numeric summaries | 361 of 365 UTC dates |  
| Reported maximum temperature | 361 numeric summaries | 361 of 365 UTC dates |  
| Reported minimum temperature | 361 numeric summaries | 361 of 365 UTC dates |  
| Precipitation | 262 numeric summaries | 262 of 365 UTC dates |
Verified in the 2025 file only. A supplied daily summary is not a guarantee of complete extremes or precipitation. Missing dates and values remain unavailable, not zero.

## About the selected station
### Los Angeles International Airport, United States — UTC daily summaries
#### A full month of daily observations
The full July 2025 example contains all 31 UTC daily summaries. Daily mean temperature ranges from 17.8 to 20.1 °C (64.0 to 68.2 °F). NOAA's supplied counts show 24 hourly values for each daily mean. Reported minima and maxima still require the SSOD limitations below.
Interactive chart ready. Hover for values, drag to zoom, or use the table below.
Fixed example: 1–31 July 2025, UTC. Source: NOAA/NCEI SSODv2. Hover for values or drag to zoom. Changing the explorer dates does not change this example.
1–31 July 2025 · Source: NOAA/NCEI SSODv2 daily summaries
</excerpt>
### Rank 4 of 72 — 0.29
<excerpt title="LOS ANGELES INTL AP (United States) | SSOD Explorer">
## Interpret the display responsibly
### Data source
*   NOAA NCEI SSODv2 product description and access options.  
*   NOAA SSODv2 documentation.

## Interpret the display responsibly
### Frequently Asked Questions
**What is the SSOD dataset?**
SSOD stands for Synoptic Summary of the Day. It is a comprehensive database maintained by NOAA providing daily weather observations aligned to UTC.
**Why is UTC alignment important?**
It aligns all aggregations to a UTC calendar day (00:00 to 23:59 UTC) rather than local climatological days, supporting consistent comparisons between stations in different time zones.
**Does SSOD include daily weather observations for the United States and Canada?**
Yes. Select **United States** or **Canada** (or Puerto Rico, Guam, US Virgin Islands) in the country filter, then use **Find Station** to search by station name or GHCN identifier. US GHCN IDs such as `USW00094908` embed the 5-digit WBAN number.
**Can SSOD alone confirm an official daily record?**
No.SSOD is useful for screening and reconstructing UTC-day sequences, but NOAA notes that synoptic precipitation may be underreported and that maximum or minimum temperature may not capture the true daily extreme. Verify record claims with the responsible national meteorological service or an appropriate daily climate product.
**Does Climate Explorer produce the SSOD summaries?**
No.Climate Explorer is an independent interface and is not affiliated with NOAA. NOAA/NCEI maintains and publishes SSODv2 summaries assembled from contributed synoptic reports; Climate Explorer retrieves, parses, and presents those records.
</excerpt>
### Rank 5 of 72 — 0.24
<excerpt title="metar klax">
Angel Peak, NV
LAS VEGAS : 122.4
BAGDAD : 122.5
PEACH SPRINGS : 122.25
SELIGMAN : 122.6
PRESCOTT : 122.2
Opal Mtn, NV
Potosi, NV
MOUNT POTOSI : 122.6
Black Mtn, NV
AJO : 122.65
JULIAN : 122.6
BLACK METAL PEAK : 122.55
BARSTOW : 122.3
PEARBLOSSOM : 122.2
Mojave Air and Space Port, CA
RAND MTN : 122.4
El Paso, CA
DEATH VALLEY : 122.2
Buffalo Bump, CA
Talega, CA
Signal Peak, CA
Bell Canyon, CA
Chino Hills, CA
Santiago Peak CalOES, CA
SANTA ANA : 122.45
Mt San Miguel, CA
Otay Mtn, CA
SAN DIEGO : 122.2
Gillespie Field, CA
Mesa Grande, CA
Coronado Hills, CA
SAN LUIS OBISPO : 122.4
BAKERSFIELD : 122.5
Mebane, CA
Templeton, CA
Parkfield, CA
Williams Hill, CA
Halls Ridge, CA
BIG SUR : 122.2
Millers Ranch, CA
Sulphur Mtn Willet, CA
UCSB Campus, CA
Dangermond, CA
LAKE HUGHES : 122.3
Orcutt, CA
Plowshare Peak, CA
Avalon, CA
KLAX
Los Angeles Intl, CA
Ridgeline, CA
Laguna Peak, CA
Topanga Peak, CA
Butler Hill, CA
Pilot Peak, NV
CURRANT : 122.3
Mammoth Mtn, CA
BRYCE CANYON : 122.2
Cedar City Hospital, UT
TONOPAH : 122.5
Queen Bee, CA
</excerpt>

## Search 10 — query: "Chicago O'Hare airport station id NCEI"
### Rank 1 of 174 — 0.71 (passed on)
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
### Rank 2 of 174 — 0.49
<excerpt title="Daily Summaries Station Details">
# Daily Summaries Station Details: CHICAGO OHARE INTERNATIONAL AIRPORT, IL US, GHCND:USW00094846 | Climate Data Online (CDO) | National Climatic Data Center (NCDC)
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
| Name | CHICAGO OHARE INTERNATIONAL AIRPORT, IL US |  
| Network:ID | GHCND:USW00094846 |  
| Latitude/Longitude | 41.96017°, -87.93164° |  
| Elevation | 204.8 m |
| Period of Record |  
| --- |  
| Start Date ¹ | 1946-10-09 |  
| End Date ¹ | 2026-11-13 |  
| Data Coverage² | 85% |
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
*   Sky cover & clouds  
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
### Rank 3 of 174 — 0.40
<excerpt title="CHICAGO OHARE INTL AP (United States) - SSOD - Climate Explorer">
1.   Home  
2.   Explorers  
3.   SSOD
Skip to interactive explorer

## NOAA SSODv2 overview
Climate Explorer provides an **independent interface** for the **NOAA/NCEI SSODv2** global daily archive. Climate Explorer is not affiliated with NOAA. SSODv2 provides meteorological summaries across the **United States** (US states including Alaska and Hawaii, plus Puerto Rico, Guam and the US Virgin Islands), **Canada** (provinces and territories), and worldwide networks, featuring UTC-aligned temperature, wind, pressure, and precipitation. It is tailored for meteorological, climate, and environmental researchers analyzing multi-decade daily weather observations, extreme weather events, synoptic storm systems, and station time series.
NOAA/NCEI maintains and publishes SSODv2 summaries assembled from contributed synoptic reports. Climate Explorer retrieves, parses, and presents those records; NOAA/NCEI remains the authoritative source for the archive, summary definitions, and documentation.
Weather station **CHICAGO OHARE INTL AP** (ID USW00094846), United States. State/region: IL. Elevation: 204.8 m. Coordinates: 41.9603°N, -87.9317°E.
Data period: 1946 to 2026.
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
### Chicago O'Hare International Airport, United States — UTC daily summaries
This is the NOAA station named CHICAGO OHARE INTL AP. The airport record describes its observing site. Downtown Chicago, the Lake Michigan shoreline, and other nearby stations should not be assumed to have identical conditions.
Station USW00094846 · Illinois, United States Location 41.9603°N, 87.9317°W · 204.8 m elevation Inventory range 1946–2026; variable availability and continuity differ.
</excerpt>
### Rank 4 of 174 — 0.36
<excerpt title="CHICAGO OHARE INTL AP (United States) - SSOD - Climate Explorer">
## About the selected station
### Chicago O'Hare International Airport, United States — UTC daily summaries
This is the NOAA station named CHICAGO OHARE INTL AP. The airport record describes its observing site. Downtown Chicago, the Lake Michigan shoreline, and other nearby stations should not be assumed to have identical conditions.
Station USW00094846 · Illinois, United States Location 41.9603°N, 87.9317°W · 204.8 m elevation Inventory range 1946–2026; variable availability and continuity differ.

## About the selected station
### Chicago O'Hare International Airport, United States — UTC daily summaries
#### What is available in the checked year
The checked 2025 file contains 362 rows across 362 of 365 UTC dates. Missing dates: 30 Aug, 31 Aug, 01 Sep. This check does not establish completeness for earlier years.
2025 station file availability · Source: NOAA/NCEI SSODv2
| Variable | Available numeric values | Dates represented |  
| --- | --- | --- |  
| Mean temperature | 361 numeric summaries | 361 of 365 UTC dates |  
| Reported maximum temperature | 361 numeric summaries | 361 of 365 UTC dates |  
| Reported minimum temperature | 361 numeric summaries | 361 of 365 UTC dates |  
| Precipitation | 297 numeric summaries | 297 of 365 UTC dates |
Verified in the 2025 file only. A supplied daily summary is not a guarantee of complete extremes or precipitation. Missing dates and values remain unavailable, not zero.

## About the selected station
### Chicago O'Hare International Airport, United States — UTC daily summaries
#### A full month of daily observations
The full July 2025 example contains all 31 UTC daily summaries. Daily mean temperature ranges from 20.0 to 29.7 °C (68.0 to 85.5 °F). NOAA's supplied counts show 24 hourly values for each daily mean. Reported minima and maxima still require the SSOD limitations below.
Interactive chart ready. Hover for values, drag to zoom, or use the table below.
Fixed example: 1–31 July 2025, UTC. Source: NOAA/NCEI SSODv2. Hover for values or drag to zoom. Changing the explorer dates does not change this example.
1–31 July 2025 · Source: NOAA/NCEI SSODv2 daily summaries
</excerpt>
### Rank 5 of 174 — 0.21
<excerpt title="CHICAGO OHARE INTL AP (United States) - SSOD - Climate Explorer">
## About the selected station
### Chicago O'Hare International Airport, United States — UTC daily summaries
#### A full month of daily observations
The full July 2025 example contains all 31 UTC daily summaries. Daily mean temperature ranges from 20.0 to 29.7 °C (68.0 to 85.5 °F). NOAA's supplied counts show 24 hourly values for each daily mean. Reported minima and maxima still require the SSOD limitations below.
Interactive chart ready. Hover for values, drag to zoom, or use the table below.
Fixed example: 1–31 July 2025, UTC. Source: NOAA/NCEI SSODv2. Hover for values or drag to zoom. Changing the explorer dates does not change this example.
1–31 July 2025 · Source: NOAA/NCEI SSODv2 daily summaries

## About the selected station
### Chicago O'Hare International Airport, United States — UTC daily summaries
#### A full month of daily observations
| UTC date | Mean · °C (°F) | Reported min · °C (°F) | Reported max · °C (°F) | Hourly values for mean |  
| --- | --- | --- | --- | --- |  
| 2025-07-01 | 26.5 (79.7) | 21.7 (71.1) | 30.6 (87.1) | 24 |  
| 2025-07-02 | 27.0 (80.6) | 21.7 (71.1) | 32.8 (91.0) | 24 |  
| 2025-07-03 | 28.2 (82.8) | 22.2 (72.0) | 33.9 (93.0) | 24 |  
| 2025-07-04 | 27.6 (81.7) | 23.3 (73.9) | 32.8 (91.0) | 24 |  
| 2025-07-05 | 29.7 (85.5) | 25.0 (77.0) | 34.4 (93.9) | 24 |  
| 2025-07-06 | 26.3 (79.3) | 21.1 (70.0) | 31.7 (89.1) | 24 |  
| 2025-07-07 | 22.2 (72.0) | 18.3 (64.9) | 27.8 (82.0) | 24 |
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
