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
Of all the botanists who have papers in the “papers of individual botanists” section of the Sherardian Library (MSS. Sherard 26-448), which ones never held the position of Sherardian Professor of Botany?  Please list their full names in the order that their work appears in the Sherardian Library.

## Expected answer
Robert Morison, Jacob Bobart the Younger, William Sherard, George Claridge Druce

## Grade 0.43

## Search 1 — query: ""MSS. Sherard 26-448" "Sherardian Library""
(no page could be scored)

## Search 2 — query: "Sherardian Library papers of individual botanists list "MSS. Sherard 26-448""
(no page could be scored)

## Search 3 — query: ""Sherardian Professor of Botany" holders"
### Rank 1 of 15 — 0.64 (passed on)
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
### Rank 2 of 15 — 0.61
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
### Rank 3 of 15 — 0.52
<excerpt title="NATURE">
## [PDF page 1]
dollars,  intuitions,  exceptional  muscles  or  remarkable  who  was  then  Sherardian  professor  of  botany,  early  
characters.  We  gravitate  to  the  groupings  in  which  recognized  Farmer's  intellectual  gifts  and  fostered  
these  are  key  values.  his  botanical  development  in  every  way.  Farmer  
Man  in  his  dawn  was  certainly  not  so  collectively  would  often  speak  in  warm  tones  of  the  inspiring  
maladjusted  as  the  man  of  our  own  time.  Contem­  influence  of  his  old  teacher,  who  was  both  botanist  
porary  man  en masse  is  definitely  a  degenerate and  gardener.  In  1889  he  was  elected  to  a  fellowship  
creature,  in  the  sense  that  he  presents  no  collective  at  Magdalen.  
resistance  in  the  face  of change.  He  experiments  only  When  Huxley  retired  from  the  headship  of  the  
feebly  in  adaptation  ;  he  persists  in  his  follies.  Biology  Department  of  the  Royal  College  of  Science  
But  since  we  have  some  two  thousand  millions  of  at  South  Kensington  the  chair  was  replaced  by  two  
him  varying  about  the  average  cases  of  any  particular  assistant  professorships,  the  botanical  one  being  
quality,  whatever  it  may  be,  the  exceptional  instances  filled  by  the  late  D.  H.  Scott.  When  Scott  retired  in  
are  likely  to  have  a  wider  range  than  in  any  previous  1892  he  was  succeeded  by  Farmer,  the  position  being
</excerpt>
### Rank 4 of 15 — 0.32
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
### Rank 5 of 15 — 0.06
<excerpt title="NATURE">
## [PDF page 1]
Every  living  thing,  in  obedience  to  its  hormic  urge,  much  for  the  development  of  botany  and  for  the  
seeks  to  assert  itself  over  other  things  that  move  extension  of  its  applications.  
other  life  or  over  inanimate  things  that  John  Bretland  Farmer  was  born  on  April  5,  1865,  
are  imagined  as  having  life.  "This,"  in  effect  says  at  Atherstone  and  was  for  a  time  at  the  Atherstone  
life,  emerging  to  a  consciousness  of  others,  "is  not  Grammar  School,  but  was  later  educated  privately.  
going  to  beat  me."  This  primitive  uneasiness  to  A  country  upbringing  and a  knowledge  of the farmer's:  
reassure  oneself  that  one  has  the  upper  hand  of  the  outlook  was  of  great  value  to  him  in  his  later efforts:  
not.me  is  still  far  more  persistent  than  any  other  to  use  botany  for  the  advancement  of  agriculture.  
urge.  We  assert  these  selves  through  a  huge  miscel·  He  went  to  Magdalen  College,  Oxford,  in  1883,  and  
lany  of claims.  The  claims  we  make  depend  upon  our  took  a  first-class  in  the  Honours  School  of  Natural  
upbringing  and  the  ideas  imposed  on  us.  We  pride  Science  in  1887.  In  that  year  he  was  appointed  
ourselves  on  'race',  country,  class,  family,  'set'  or  demonstrator  in  the University,  for  Bayley  Balfour,
</excerpt>

## Search 4 — query: ""MSS. Sherard 26-448" botanist papers list"
(no page could be scored)

## Search 5 — query: ""MSS. Sherard" "26-448""
(no page could be scored)

## Search 6 — query: ""Papers of Robert Morison" "MSS. Sherard 26-448""
(no page could be scored)

## Search 7 — query: ""MSS. Sherard 26-448" list"
(no page could be scored)

## Search 8 — query: ""Papers of" "individual botanists" Oxford"
### Rank 1 of 403 — 0.34 (passed on)
<excerpt title="An Annotated Bibliography on Southeastern American Botanical ...">
## [PDF page 9]
8
Botanists Included

## [PDF page 9]
Abbot, John  LeConte, John Eatton  
Baldwin, William  LeConte, Louis  
Banister, John  Le Page du Pratz, Antoine Simon  
Barton, Benjamin Smith  Lord, Joseph  
Bartram, John  Lyon, John  
Bartram, William  McBride, James  
Baudry des Lozières, Louis Narcisse  Michaux, André  
Bohun, Edmund  Michaux, François André  
Bolzius, Johann Martin  Mitchell, John  
Bosc, Louis Augustin Guillaume  Nuttall, Thomas  
Boykin, Samuel  Oemler, Augustus Gottlieb  
Brahm, John William Gerard de  Palisot de Beauvois, Ambroise-  
Brickell, John (fl. 1720s-1740s)  Marie-François-Joseph  
Brickell, John (1748-1809)  Pursh, Frederick Traugott  
Butel-Dumont, George Marie  Raffeneau-Delile, Alire  
Castiglioni, Luigi  Reck, Philip Georg Frederich von  
Catesby, Mark  Robin, Charles-Cesar  
Clayton, Rev. John (1657-1725)  Romans, Bernard  
Clayton, John (1686?-1773)  Schöpf, Johann David  
Corrêa da Serra, José Francisco  Schweinitz, Lewis David von  
Custis, Peter  Shecut, John Linnaeus Edwards Whitridge  
Dale, Thomas  Strachey, William  
Dobbs, Arthur  Tradescant, John, the Younger  
Drayton, John  Walter, Thomas  
Ellicott, Andrew  Whitlaw, Charles  
Elliott, Stephen  Williams, Hannah English  
Ellis, Robert  Wray, Thomas Jarram  
Enslen, Aloysius  Young, William, Jr.  
Franklin, George  
Fraser, John  
Gambold, Anna Rosina Kleist  
Garden, Alexander  
Gilmer, Francis Walker  
Glover, Thomas  
Greenway, James  
Habersham, Richard Wylly  
Harriot, Thomas  
Herbemont, Nicholas  
Jackson, James  
Jefferson, Thomas  
Kinn, Matthias  

## [PDF page 9]
Kramsch, Samuel Gottlieb  
Lawson, John

## [PDF page 10]
9
Organization and Format
Entries for works follow the Author-Date Reference List format given in The Chicago
Manual of Style, 14th edition (University of Chicago Press, 1993), with the exception that full
names of authors are given when available.  Abbreviation has been kept to a minimum.  An
asterisk preceding an entry indicates that the source has been searched for references to all
persons here listed, and their entries annotated accordingly.  Entries for persons are
organized as follows:
Firstname Lastname
(alternative spellings)
b. place of birth, year of birth; d. place of death, year of death.
Portrait:  brief citation for a published likeness.
Handwriting:  brief citation for a published handwriting sample.
Papers:  list of institutions housing papers of the botanist.
Herbarium:  list of institutions housing specimens collected by the botanist.  Neither
this nor the list under “Papers” is intended to be exhaustive, but only to
point researchers to major collections.  Consult Taxonomic Literature and Index
Herbariorum for more complete information.
Eponymy:  list of generic names of plants and fungi which commemorate the
botanist.  The generic name is followed by its author(s) and by a parenthetical
statement giving the family of the organism as well as an indication of higher
taxon if it is a non-phanerogam (e.g. Musci, Fungi).
</excerpt>
### Rank 2 of 403 — 0.25
<excerpt title="An Annotated Bibliography on Southeastern American Botanical ...">
## [PDF page 10]
9
Organization and Format
Entries for works follow the Author-Date Reference List format given in The Chicago
Manual of Style, 14th edition (University of Chicago Press, 1993), with the exception that full
names of authors are given when available.  Abbreviation has been kept to a minimum.  An
asterisk preceding an entry indicates that the source has been searched for references to all
persons here listed, and their entries annotated accordingly.  Entries for persons are
organized as follows:
Firstname Lastname
(alternative spellings)
b. place of birth, year of birth; d. place of death, year of death.
Portrait:  brief citation for a published likeness.
Handwriting:  brief citation for a published handwriting sample.
Papers:  list of institutions housing papers of the botanist.
Herbarium:  list of institutions housing specimens collected by the botanist.  Neither
this nor the list under “Papers” is intended to be exhaustive, but only to
point researchers to major collections.  Consult Taxonomic Literature and Index
Herbariorum for more complete information.
Eponymy:  list of generic names of plants and fungi which commemorate the
botanist.  The generic name is followed by its author(s) and by a parenthetical
statement giving the family of the organism as well as an indication of higher
taxon if it is a non-phanerogam (e.g. Musci, Fungi).

## [PDF page 11]
10
List of references pertaining to the botanist which are cited elsewhere in the
bibliography.  These are given as: Author (or title in the case of certain major
reference works) Year, location in the present bibliography.  For works cited in Parts
I and II, the location is given according to the table of contents.  So, for instance,
“Gifford 1975, IA” refers to Gifford’s article “The Charleston Physician-Naturalists”
in the Bulletin of Medical History.  For works cited in Part III, the last name of the
botanist under which the work is cited in full replaces the alpha-numeric designation.
On occasion, these works call for more detailed comment, which is given
immediately below the list in the same small typeface.
</excerpt>
### Rank 3 of 403 — 0.22
<excerpt title="An Annotated Bibliography on Southeastern American Botanical ...">
## [PDF page 30]
b. Twigworth, Gloucestershire, England, 1650; d. Roanoke River, Virginia, 1692.  
Handwriting:  Ewan and Ewan, 1970, p. 146.  
Papers:  British Museum (Natural History); Bodleian Library.  
Herbarium:  British Museum (Natural History); Oxford; South Kinsington.  
Eponymy:  Banisteria L. (nom. rej., Malpighiaceae), Banisteriaecarpum Kräusel (fossil,  
Malpighiaceae), Banisterioides Dubard & Dop (Malpighiaceae), Banisteriophyllum  
Ettingshausen (fossil, Malpighiaceae), Banisteriopsis C. B. Robinson ex J. K. Small  
(Malpighiaceae), Banisterodes O. Kuntze (nom. rej., Polygalaceae).

## [PDF page 31]
30
Goode 1886, IA  Ewan 1969, IIA  
Kastner 1977, IA  Humphrey 1961, IIA  
Stearns 1970, IA  Lamson-Scribner 1893, IIA  
Elliott 1979, IB  Lanjouw & Stafleu 1954, IIA  
Garraty & Carnes 1999, IB  Pennell 1950, IIA  
Gillispie 1970, IB  Barnhart 1965, IIB  
Johnson 1957, IB  Desmond 1994, IIB  
Sterling 1997, IB  Stafleu & Cowan, IIC  
Appleton’s Cyclopaedia, IB  Barton, 1793  
Who Was Who in America, IB  Pulteney, 1790, Catesby ( 2:  
Barnhart 1909, IIA  55-57)  
Brendel 1879, IIA  Berkeley & Berkeley, 1968, Rev.  
Clokie 1964, IIA  John Clayton  
Crowley 1976, IIA  Graustein 1967, Nuttall  
Dandy 1958, IIA  Ewan in Pursh 1979, Pursh
Banister, John. 1907.  Banister’s Catalogue of Virginia Plants.  Ed. Ivar Tidestrom.  
Washington, D.C.  
Reprinting of Banister’s Catalogue from Ray 1688, below, with brief preface by  
Tidestrom.
</excerpt>
### Rank 4 of 403 — 0.22
<excerpt title="An Annotated Bibliography on Southeastern American Botanical ...">
## [PDF page 33]
32
Benjamin Smith Barton
b. Lancaster, Pennsylvania, 1766; d. Philadelphia, 1815.  
Portrait: Kelly, cited in part II, also W. P. C. Barton, below.  
Handwriting:  Barton, ed. McAtee and Middleton, both cited below.  
Papers:  Historical Society of Pennsylvania; American Philosophical Society; Boston Public  
Library; Library of Congress.  
Herbarium:  Academy of Natural Sciences.  
Eponymy:  Bartonia Mühlenberg ex Willdenow (Gentianaceae); Bartonia Pursh ex Sims  
(Loasaceae); Bartonia Smith (Pontederiaceae).

## [PDF page 33]
Kastner 1977, IA  Hooker 1825, IIA  
Stearns 1970, IA  Humphrey 1961, IIA  
Drake 1876, IB  Kelly 1914, IIA  
Duychinck 1856, IB  Lanjouw & Stafleu 1954, IIA  
Elliott 1979, IB  Mears 1978, IIA  
Garraty & Carnes 1999, IB  Pennell 1950, IIA  
Gillispie 1970, IB  Rafinesque 1836, IIA  
Johnson 1957, IB  Rogers & Saunders 1984, IIA  
Kelly & Burage 1928, IB  Barnhart 1965, IIB  
National Cyclopaedia 8, IB  Stafleu & Cowan, IIC  
Sterling 1997, IB  Stafleu & Mennega, IIC  
Who Was Who in America, IB  Darlington 1843, Baldwin  
Bell 1955, IC  Darlington 1849, John Bartram  
Anon. 1821, IIA  Harper, 1945, Wm. Bartram  
Barnhart 1909, IIA  Graustein 1967, Nuttall  
Brendel 1879, IIA  Pennell, 1936, Nuttall  
Ewan 1969, IIA  Barnhart 1934, Schweinitz  
Harshberger 1899, IIA
Anon.  1798.  [Review of] Collections for an essay toward a materia medica of the United States.  
Medical Repository 2(1): 70-74.  
Very favorable review and summary of Barton’s Collections.  Notes the  
significance of Barton as an American-born scientist addressing the flora of his  
native land.

## [PDF page 33]
Barton, Benjamin Smith.  1793.  Botanical description of the Podophyllum diphyllum of  
Linnaeus, in a letter to Charles Peter Thunberg, M.D. Knight of the Order of Wasa,  
Professor of Medicine and Botany in the University of Upsal, &c. &c.  Transactions of the  
Philosophical Society of America 3: 334-348.  
Considers this plant allied to, but distinct from, the Linnean genera Podophyllum  
and Sanguinaria.  Erects a new genus, Jeffersonia, named for Thomas Jefferson.  
“In the various departments of this science [natural history], but especially in  
botany and zoology, the information of this gentleman is equaled by that of few  
persons in the United-States.”  See Graustein, 1961, below, regarding André  
Michaux’s intent to publish this species.
</excerpt>
### Rank 5 of 403 — 0.19
<excerpt title="An Annotated Bibliography on Southeastern American Botanical ...">
## [PDF page 37]
36
John Bartram
b. Darby, Pennsylvania, 1699; d. Kingsessing, Pennsylvania, 1777.  
Portrait:  Stewart, cited below.  
Handwriting:  Buck & McLean, cited below.  
Papers:  Royal Society of London; American Philosophical Society; University of  
Pennsylvania; Historical Society of Pennsylvania; Academy of Natural Sciences,  
Philadelphia.  
Herbarium:  British Museum (Natural History); Linnean Herbarium; Oxford.  
Eponymy:  Bartramia J. Hedwig (Musci, Bartramiaceae); Bartramia L. (Tiliaceae); Bartramia  R.  
A. Salisbury (Scrophulariaceae); Bartramia Ellis (Primulaceae).

## [PDF page 37]
Goode 1886, IA  Dandy 1958, IIA  
Kastner 1977, IA  Ewan 1969, IIA  
Stearns 1970, IA  Harshberger 1899, IIA  
Drake 1876, IB  Hooker 1825, IIA  
Duychinck 1856, IB  Humphrey 1961, IIA  
Elliott 1979, IB  Kelly 1914, IIA  
Garraty & Carnes 1999, IB  Lamson-Scribner 1893, IIA  
Gillispie 1970, IB  Lanjouw & Stafleu 1954, IIA  
Johnson 1957, IB  Pennell 1935, IIA  
Kelly & Burage 1928, IB  Pennell 1950, IIA  
National Cyclopaedia 7, IB  Rogers & Saunders 1984, IIA  
Sterling 1970, IB  Totten 1956, IIA  
Appleton’s Cyclopaedia, IB  Wilbert 1908, IIA  
Who Was Who in America, IB  Barnhart 1965, IIB  
Bell 1955, IC  Desmond 1994, IIB  
Anon. 1821, IIA  Stafleu & Cowan, IIC  
Barnhart 1909, IIA  Stafleu & Mennega, IIC  
Barnhart 1917, IIA  Darlington 1843, Baldwin  
Brendel 1879, IIA  Darlington 1849, John Bartram  
Clokie 1964, IIA  Graustein 1967, Nuttall  
Crowley 1976, IIA  Ewan in Pursh 1979, Pursh

## [PDF page 37]
Anon.  1899.  History of John Bartram.  Meehan’s Monthly 9: 96.  
Criticizes the use of the “Letter of a Russian Gentleman” as factual data in  
Bartram biographies.  Bartram, it is argued, was not the “ignoramus” depicted in  
the Crèvecoeur account, nor did he come to the study of botany as late in life as
Barnhart, John Hendley.  1931a.  Significance of John Bartram’s work to botanical and  
horticultural knowledge.  Bartonia 12, supplement: 24-34.  
Asserts that John Bartram’s greatest achievement was not his garden, but “his  
tireless search among the wilds of Atlantic North America for plants, especially  
woody ones, hardy in this climate, that might be desireable additions to the  
gardens of the Old World.”  Lists some of the plants sent to Collinson and also  
comments on Bartram’s pollination studies.
</excerpt>

## Search 9 — query: ""Papers of" "Sherardian" "MSS. Sherard""
(no page could be scored)

## Search 10 — query: ""MSS Sherard 26-448""
(no page could be scored)

# Example 2
## Question
Among all countries led by a female head of state as of June 2024, identify those which are island nations that gained their independence from Great Britain and list them in the chronological order in which they did.

## Expected answer
Trinidad & Tobago, Malta, Barbados, Dominica

## Grade 0.75

## Search 1 — query: "female head of state island nation independence from Britain 2024"
### Rank 1 of 73 — 0.78 (passed on)
<excerpt title="Barbados became a republic on Tuesday, cutting ties with Queen ...">
•
Follow
* * *
Barbados became a republic on Tuesday, cutting ties with Queen Elizabeth II and casting off the last major vestige of its colonial past.  
The Caribbean island nation swore in its first president, Sandra Mason, a former governor general who had been appointed by the queen. At a ceremony attended by Prince Charles and Rihanna, a 21-gun salute rang out as the national anthem played. The red, yellow and navy blue royal flag was lowered — exactly 55 years after Barbados gained independence from Britain.
Barbados, a democracy of about 300,000 people, announced in September that it would become the latest Caribbean island to remove Queen Elizabeth as head of state. It joins Trinidad and Tobago, which became independent in 1962 and a republic in 1976; Dominica, which gained full independence as a republic in 1978; and the South American country of Guyana, which gained independence in 1966 and became a republic in 1970.
Australia, Canada, Jamaica, New Zealand and Papua New Guinea are among the nations that still call the queen their head of state. Barbados will remain part of the Commonwealth, a voluntary association of 54 countries with roots in the British Empire.
Tap the link in our bio to read more about Barbados’s formal uncoupling from Britain.
And the forst president is a woman! 👏👏👏
1 like
Reply
Yesss free from the Brittain's. Congratulations Barbados, and Rihanna has put Barbados up high. She is a beautiful soul grounded on her roots who has been a very productive person in society here in the US, and wherever she goes, as a singer, fashion designer and much more. She deserves to be honored as a Hero in her country. 👏👏👏👏👏👏👏👏👏
Reply
❤️❤️❤️❤️
Reply
start of their debacle
Reply
Congratulations to Barbados and the New President, Mrs. Sandra Mason. Salute 🖤
Reply
Reply
🙌❤️ ‼️‼️ 🇧🇧
Reply
Wait a minute, Canada ?
Reply
Freeeeee Barbados !!!!❤️
Reply
Congratulations. Good luck. So proud.
Reply

🙌 PosiPower is loving it!
Reply
Still gives the speech in English
Reply
37.3K 346
</excerpt>
### Rank 2 of 73 — 0.76
<excerpt title="The Caribbean island state of Barbados officially became a ...">
# Video
## Related videos
[](https://www.facebook.com/watch/100064492880345/?__cft__[0]=AZgPFLV8WKJcYBJAVDc619-AbYXqt4ScVZAsRp6I5QZWdDzNLAr82L_Z1NCm4Z1pbmZwfB_XCwFy9W658eGo5axGcvgKS2tReKYpH_UL9C-p6bmlAZRdcKAqX85ArRmBHt_sNhVgQSs4rZy8xZcgxw)
[Powerful waves battered the coast of Santa Cruz County, creating dangerous conditions at beaches along Northern California. Footage showed heavy surf crashing along the shoreline. Authorities urged the public to stay away from the coast as rough surf was expected to continue through the weekend.](https://www.facebook.com/100064492880345/videos/1550809170297572/?__so__=permalink&__cft__[0]=AZgPFLV8WKJcYBJAVDc619-AbYXqt4ScVZAsRp6I5QZWdDzNLAr82L_Z1NCm4Z1pbmZwfB_XCwFy9W658eGo5axGcvgKS2tReKYpH_UL9C-p6bmlAZRdcKAqX85ArRmBHt_sNhVgQSs4rZy8xZcgxw)

# Video
## Related videos
[A News](https://www.facebook.com/watch/100064492880345/?__cft__[0]=AZgPFLV8WKJcYBJAVDc619-AbYXqt4ScVZAsRp6I5QZWdDzNLAr82L_Z1NCm4Z1pbmZwfB_XCwFy9W658eGo5axGcvgKS2tReKYpH_UL9C-p6bmlAZRdcKAqX85ArRmBHt_sNhVgQSs4rZy8xZcgxw&__cft__[1]=AZgPFLV8WKJcYBJAVDc619-AbYXqt4ScVZAsRp6I5QZWdDzNLAr82L_Z1NCm4Z1pbmZwfB_XCwFy9W658eGo5axGcvgKS2tReKYpH_UL9C-p6bmlAZRdcKAqX85ArRmBHt_sNhVgQSs4rZy8xZcgxw)
1.9K views
·
3d ago
Pages
Businesses
Media/news company
A News
Videos
The Caribbean island state of Barbados officially became a republic on Tuesday as its first President Sandra Mason, elected in October, replaced British Queen Elizabeth II as head of state. Tim Wilson analyzed Barbados’ independence process.
Home
Live
Explore
*   Privacy ·   
*   Terms ·   
*   Advertising ·   
*   Ad Choices ·   
*   Cookies ·   
*   More
See more on Facebook
See more on Facebook
Email or phone number
Password
Log In
Forgot password?
or
Create new account
</excerpt>
### Rank 3 of 73 — 0.73
<excerpt title="The Caribbean island state of Barbados officially became a ...">
# The Caribbean island state of #Barbados officially became a republic on Tuesday as its first President #SandraMason, elected in October, replaced British #Queen Elizabeth II as head of state. Tim Wilson analyzed Barbados’ #independence process. | A News | Facebook
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
The Caribbean island state of Barbados officially became a republic on Tuesday as its first President Sandra Mason, elected in October, replaced British Queen Elizabeth II as head of state. Tim Wilson analyzed Barbados’ independence process.
Like
Comment
Share
![Image 2](blob:http://localhost/85d8b181a20aeb64a3afc2f1c39d2480)
15
·
300 views

# Video
## **A News**
Wednesday, December 1, 2021 at 9:30 AM
December 1, 2021 ·
Follow
The Caribbean island state of #Barbados officially became a republic on Tuesday as its first Preside…
See more

# Video
## Comments


# Video
## Related Reels
A News 9.2K
A News 3.2K
A News 10K
A News 69K
A News 12K
A News 9.3K
A News 22K
A News 33K
A News 9.1K
A News 6.1K
A News 37K
A News 16K

# Video
## Related videos
[ 42:37](https://www.facebook.com/100064492880345/videos/2962433230780485/?__so__=permalink&__cft__[0]=AZgtzi67zoZjDaY_IdKQgzFEyQl3KpiZz94w8D1aoZeucmTzU6JJvubNcIurlLApjuRjXCu_LD2mkGfAMIoXqf2bIHXGSIlvf7CyEGOcY_7uCYNwjABeDr3mlDGEkejCxDxg3uWF4x4nBXPNdkvlVQ)
[](https://www.facebook.com/watch/100064492880345/?__cft__[0]=AZgtzi67zoZjDaY_IdKQgzFEyQl3KpiZz94w8D1aoZeucmTzU6JJvubNcIurlLApjuRjXCu_LD2mkGfAMIoXqf2bIHXGSIlvf7CyEGOcY_7uCYNwjABeDr3mlDGEkejCxDxg3uWF4x4nBXPNdkvlVQ)
[Türkiye’s Diplomacy: Europe faces growing unrest and cyber threats, while Trump, Putin and Xi prepare to meet in Shenzhen as oil hovers near $93.](https://www.facebook.com/100064492880345/videos/2962433230780485/?__so__=permalink&__cft__[0]=AZgtzi67zoZjDaY_IdKQgzFEyQl3KpiZz94w8D1aoZeucmTzU6JJvubNcIurlLApjuRjXCu_LD2mkGfAMIoXqf2bIHXGSIlvf7CyEGOcY_7uCYNwjABeDr3mlDGEkejCxDxg3uWF4x4nBXPNdkvlVQ)
</excerpt>
### Rank 4 of 73 — 0.71
<excerpt title="Barbados has removed Queen Elizabeth as its head of state ...">
# CGTN America - Barbados has removed Queen Elizabeth as its... | Facebook
Log In
Log In
Forgot Account?

# CGTN America - Barbados has removed Queen Elizabeth as its... | Facebook
## CGTN America's Post
* * *
[](https://www.facebook.com/stories/107376664754257/UzpfSVNDOjE2MTYwMTUwMDA1NDUxNTM=/?view_single=false&__cft__[0]=AZhaYbgQ2elQzDQHVOyrZUh2E77sgoAos1CLDJbTFl-x-cZRoMVBH7B5lylvJb9ywYvnQCWWXYyqiXbSFk3z7N_BdiA39aM6KCqxpwflzhx3Cjuf414eqzWGFsLT_wF_ugtr9gQYRf8xKCdpk4dNiA8PhlpEykAq&__tn__=%3C%3C%2CP-R)
### [**CGTN America**](https://www.facebook.com/cgtnamerica?__cft__[0]=AZhaYbgQ2elQzDQHVOyrZUh2E77sgoAos1CLDJbTFl-x-cZRoMVBH7B5lylvJb9ywYvnQCWWXYyqiXbSFk3z7N_BdiA39aM6KCqxpwflzhx3Cjuf414eqzWGFsLT_wF_ugtr9gQYRf8xKCdpk4dNiA8PhlpEykAq&__tn__=-UC%2CP-R)
**China state-controlled media**
·
Thursday, October 21, 2021 at 6:43 PM

# CGTN America - Barbados has removed Queen Elizabeth as its... | Facebook
## CGTN America's Post
[October 21, 2021](https://www.facebook.com/cgtnamerica/posts/pfbid02BeN2pDiaYmksZkQ5iYnAAdt4bjFH7NX7JWNsgCFy9xQDZyD3sVZwwJvVdqqE8RDAl?__cft__[0]=AZhaYbgQ2elQzDQHVOyrZUh2E77sgoAos1CLDJbTFl-x-cZRoMVBH7B5lylvJb9ywYvnQCWWXYyqiXbSFk3z7N_BdiA39aM6KCqxpwflzhx3Cjuf414eqzWGFsLT_wF_ugtr9gQYRf8xKCdpk4dNiA8PhlpEykAq&__tn__=%2CO%2CP-R) ·
Barbados has removed Queen Elizabeth as its head of state by electing its first-ever president Dame Sandra Mason, 72, in preparation to become a republic. The government said it was time for Barbados to “fully leave our colonial past behind.”
Mason, who until now has been serving as the governor-general of Barbados, is set to be sworn in as president on November 30, the country’s 55th anniversary of independence from Britain.
[](https://www.facebook.com/photo/?fbid=4414096345352270&set=a.633174798841105&__cft__[0]=AZhaYbgQ2elQzDQHVOyrZUh2E77sgoAos1CLDJbTFl-x-cZRoMVBH7B5lylvJb9ywYvnQCWWXYyqiXbSFk3z7N_BdiA39aM6KCqxpwflzhx3Cjuf414eqzWGFsLT_wF_ugtr9gQYRf8xKCdpk4dNiA8PhlpEykAq&__tn__=EH-R)
</excerpt>
### Rank 5 of 73 — 0.70
<excerpt title="Barbados has removed Queen Elizabeth as its head of state ...">
# CGTN America - Barbados has removed Queen Elizabeth as its... | Facebook
## CGTN America's Post
[October 21, 2021](https://www.facebook.com/cgtnamerica/posts/pfbid02BeN2pDiaYmksZkQ5iYnAAdt4bjFH7NX7JWNsgCFy9xQDZyD3sVZwwJvVdqqE8RDAl?__cft__[0]=AZhaYbgQ2elQzDQHVOyrZUh2E77sgoAos1CLDJbTFl-x-cZRoMVBH7B5lylvJb9ywYvnQCWWXYyqiXbSFk3z7N_BdiA39aM6KCqxpwflzhx3Cjuf414eqzWGFsLT_wF_ugtr9gQYRf8xKCdpk4dNiA8PhlpEykAq&__tn__=%2CO%2CP-R) ·
Barbados has removed Queen Elizabeth as its head of state by electing its first-ever president Dame Sandra Mason, 72, in preparation to become a republic. The government said it was time for Barbados to “fully leave our colonial past behind.”
Mason, who until now has been serving as the governor-general of Barbados, is set to be sworn in as president on November 30, the country’s 55th anniversary of independence from Britain.
[](https://www.facebook.com/photo/?fbid=4414096345352270&set=a.633174798841105&__cft__[0]=AZhaYbgQ2elQzDQHVOyrZUh2E77sgoAos1CLDJbTFl-x-cZRoMVBH7B5lylvJb9ywYvnQCWWXYyqiXbSFk3z7N_BdiA39aM6KCqxpwflzhx3Cjuf414eqzWGFsLT_wF_ugtr9gQYRf8xKCdpk4dNiA8PhlpEykAq&__tn__=EH-R)

# CGTN America - Barbados has removed Queen Elizabeth as its... | Facebook
## CGTN America's Post
![Image 2](blob:http://localhost/85d8b181a20aeb64a3afc2f1c39d2480)
![Image 3](blob:http://localhost/2b45e6f1a2ae097354c0b291152873d5)
All reactions:
38
3 comments
11 shares
Like
Comment
Most relevant
Jeffrey Tham
Viva la Barbados.
*   [5y](https://www.facebook.com/cgtnamerica/posts/pfbid02BeN2pDiaYmksZkQ5iYnAAdt4bjFH7NX7JWNsgCFy9xQDZyD3sVZwwJvVdqqE8RDAl?comment_id=4417609131667658&__cft__[0]=AZhaYbgQ2elQzDQHVOyrZUh2E77sgoAos1CLDJbTFl-x-cZRoMVBH7B5lylvJb9ywYvnQCWWXYyqiXbSFk3z7N_BdiA39aM6KCqxpwflzhx3Cjuf414eqzWGFsLT_wF_ugtr9gQYRf8xKCdpk4dNiA8PhlpEykAq&__tn__=R]-R)
</excerpt>

## Search 2 — query: "Barbados independence 30 November 1966"
### Rank 1 of 124 — 0.81 (passed on)
<excerpt title="Barbados Independence Celebrations">
# Barbados Independence
        *   Adventure  
        *   Beaches  
        *   Family  
        *   Festivals  
        *   Food  
        *   History & Culture  
        *   Nature  
        *   Nightlife  
        *   Respite  
        *   Romance  
        *   Shopping  
        *   Sights  
        *   Sports

    *   Essentials

        *   Documents You Need  
        *   Book A Flight  
        *   Find A Place To Stay  
        *   On Arrival At Airport  
        *   What To Do  
        *   Don't Miss!  
        *   What Events Are On?  
        *   On Departure  
        *   Your Next Trip!

    *   Insider Tips

        *   Best Areas To Stay  
        *   Beach Guide  
        *   Beyond The Beach  
        *   Cook Like A Local  
        *   Local Chatbot Guides  
        *   Health & Wellness  
        *   Fast Track Arrivals  
        *   Meet Our Artisans  
        *   World Heritage Site

*   Deals

    *   Stay

        *   Hotels & Resorts  
        *   Self Catering Apts & Hotels  
        *   Guest Houses  
        *   Villas & Vacation Rentals  
        *   Long Term Rentals  
        *   Real Estate

    *   Play

        *   Activities & Attractions  
        *   Car Rentals  
        *   Dining & Entertainment  
        *   Shopping  
        *   Tours & Sightseeing  
        *   Weddings & Romance

    *   Flights

        *   ✈️ Expedia Flight Deals  
        *   Google Flights
CLOSE

# ★ About Barbados ★
*   Preparing The Trip  
*   Travel Documents  
*   Flights & Travel  
*   Airport Services  
*   All About Barbados  
*   Getting Married  
*   Weather  
*   Barbados Maps  
*   Barbados Chatbots  
*   Why is Barbados so famous?  
*   Long Stay Visitors  
*   Barbados Holidays

*   ### Travel Services

*   Vacation Specials  
*   Holiday Themes  
*   Brochures
Home ›› About Barbados ››

# Barbados Independence Celebrations
*   Preparing The Trip  
*   Travel Documents  
*   Flights & Travel  
*   Airport Services  
*   All About Barbados  
*   Getting Married  
*   Weather  
*   Barbados Maps  
*   Barbados Chatbots  
*   Why is Barbados so famous?  
*   Long Stay Visitors  
*   Barbados holidays  
*   Vacation Specials  
*   Holiday Themes  
*   Brochures
×

# Barbados Independence Celebrations
## History
After the first English settlement at Holetown in 1627, Barbados remained a **British colony** until achieving **independence** from Britain on **November 30 th 1966**.
That first independence ceremony was accompanied by the raising of the Barbados national flag, and playing of the national anthem for the first time. November 30 th is celebrated as Independence Day and is a national holiday in Barbados.
On November 30 th 2021, Barbados became **a Republic**. The island remains a member of the Commonwealth of Nations.
</excerpt>
### Rank 2 of 124 — 0.77
<excerpt title="Barbados Gains Independence - 1966 | Today In History | 30 Nov 17">
Back  KR
Search with your voice
Sign in
KR
Barbados Gains Independence - 1966 | Today In History | 30 Nov 17
0:02 / 1:17
•Watch full video
5:4518:045:3222:394:495:0744:2852:4116:4317:329:4613:38
AP Archive
6.06M subscribers
Download
4K views 8y ago
4,074 views • Nov 29, 2017
On November 30, 1966, the former British colony of Barbados became independent. You can license this story through AP Archive: http://www.aparchive.com/metadata/you...…
more
more

## 2 Comments
Sort comments
Sort by
Add a comment...

## 2 Comments
### @chrissystewart6268
3 years ago
Happy 56 years of Independence🇧🇧🇧🇧🇧🇧 from Chrissy Stewart🇺🇸 I wish the beautiful people best wishes. Every year of Nov. 30th I will keep wishing happy independence day in 🇧🇧
Like
Dislike

## 2 Comments
### @revinhatol
4 years ago
#ItHappenedOnAWednesdayClear
Like
Dislike
Top is selected, so you'll see featured comments

## Comments 2


## Barbados Gains Independence - 1966 | Today In History | 30 Nov 17
AP Archive
33 Likes
4K Views
2017 Nov 29
On November 30, 1966, the former British colony of Barbados became independent. You can license this story through AP Archive: http://www.aparchive.com/metadata/you... Find out more about AP Archive: http://www.aparchive.com/HowWeWork Follow us on social: Twitter: /ap_archive​ Facebook: /aparchives​ Google+: https://plus.google.com/b/10201102858... Tumblr: https://aparchives.tumblr.com/​

## Barbados Gains Independence - 1966 | Today In History | 30 Nov 17
### AP Archive 6.06M subscribers
VideosAboutLinkedIn

## Video details
Date
Nov 29, 2017
Views
4,074
Likes
33

## Video details
### ADHD Child vs. Non-ADHD Child Interview
Mental Health Matters
30M 11y ago

## Video details
### Why Japan's yen is becoming a problem for the US I Business Beyond
DW News
1.8M 12d ago

## Video details
### The life, legacy & assassination of an African revolutionary - Lisa Janae Bacon
TED-Ed
588K 6y ago

## Video details
### We Sent 18 Squishy Toys To A Lab. Here’s What We Found | Talking Point
CNA Insider
2.7M 9d ago

## Video details
### “1년 전 약속대로..”... 대통령 한마디에 시진핑 ‘활짝’
JTV뉴스
633K 9h ago

## Video details
### Port of Spain in Trinidad (1970-1979) | British Pathé
British Pathé
149K 12y ago

## Video details
### [[4th Anniversary of the Itaewon Tragedy] Itaewon Tragedy 'Undisclosed Files'... A Portrait of a F...](https://www.youtube.com/watch?v=ZV-vHw6rA24&pp=ugUHEgVlbi1VUw%3D%3D)
뉴스타파 Newstapa
4.1M 3w ago
Auto-dubbed
</excerpt>
### Rank 3 of 124 — 0.76
<excerpt title="Barbados - Countries">
Barbados - Countries
1.   Home  
2.   Countries  
3.   A Guide to the United States’ History of Recognition, Diplomatic, and Consular Relations, by Country, since 1776: Barbados

## A Guide to the United States’ History of Recognition, Diplomatic, and Consular Relations, by Country, since 1776: Barbados


## Summary
The United States maintained a consular presence in Barbados beginning June 11, 1823, when Barbados was still a British colony. Following widespread Caribbean decolonization throughout the 1960s and 1970s, the United States has used Bridgetown as a base for diplomatic relations with Barbados and the region.
Modern Flag of Barbados

## Recognition
### U.S. Recognition of Barbados’ Independence, 1966.
Following a June 1966 constitutional conference with Great Britain at which Barbados negotiated its independence, Barbados because an independent state within the British Commonwealth on November 30, 1966. The United States recognized Barbados’ independence that same day when it opened the American Embassy in Bridgetown.

## Recognition
### Diplomatic Relations
#### Establishment of Diplomatic Relations and the American Embassy in Barbados, 1966.
The U.S. Embassy at Bridgetown was established on November 30, 1966, with George Dolgin as Chargé d’Affaires ad interim.

## Resources
*   CIA World Factbook: Barbados  
*   Department of State Country Information: Barbados
</excerpt>
### Rank 4 of 124 — 0.74
<excerpt title="Barbados gains independence from the UK and adopts its 'Broken Trident ...">
# More posts you may like
Related posts
*   30 November 1966: Barbados gains independence from the UK and adopts its ‘Broken Trident’ flag, symbolising the severing of colonial ties r/vexillology•1y ago    ### 30 November 1966: Barbados gains independence from the UK and adopts its ‘Broken Trident’ flag, symbolising the severing of colonial ties      159 upvotes ·11 comments
* * *
*    airbnb  •Ad    Introvert tip: Book somewhere where your phone "doesn't work".       airbnb.com Book Now
* * *
*   30 November 1966: Barbados gains independence from the UK and adopts a flag symbolising the severing of colonial status r/vexillology•4y ago    ### 30 November 1966: Barbados gains independence from the UK and adopts a flag symbolising the severing of colonial status      26 upvotes ·3 comments
* * *
*   19 September 1983: Saint Kitts and Nevis gains independence from the UK and adopts a new flag r/vexillology•2y ago    ### 19 September 1983: Saint Kitts and Nevis gains independence from the UK and adopts a new flag      31 upvotes ·5 comments
* * *
*   25 November 1975: Suriname gains independence from the Netherlands and adopts a new flag r/vexillology•2y ago    ### 25 November 1975: Suriname gains independence from the Netherlands and adopts a new flag      21 upvotes ·3 comments
* * *
*   3 November 1978: Dominica gains independence from the UK and adopts a new flag r/vexillology•2y ago    ### 3 November 1978: Dominica gains independence from the UK and adopts a new flag      17 upvotes ·5 comments
* * *
*   The Fabian Plot: How Tony Blair and the Elites DESTROYED Britain r/ukpolitics•1y ago    ### The Fabian Plot: How Tony Blair and the Elites DESTROYED Britain      38 comments
* * *

# More posts you may like
*   Has Barbados gotten better since their independence with the United Kingdom? r/AskTheWorld•3y ago    ### Has Barbados gotten better since their independence with the United Kingdom?    9 upvotes ·14 comments
* * *
*   Do's and Don'ts for Tourists in Barbados? ☀️🌴 r/Barbados•2y ago    ### Do's and Don'ts for Tourists in Barbados? ☀️🌴    41 upvotes ·67 comments
* * *
*   29 September 1967: Anguilla adopts its Dolphin Flag, following its recent declaration of independence from the UK in protest at neglect by St Kitts r/vexillology•2y ago    ### 29 September 1967: Anguilla adopts its Dolphin Flag, following its recent declaration of independence from the UK in protest at neglect by St Kitts      20 upvotes ·2 comments
* * *
*   British protectorates r/maldives•14d ago    ### British protectorates     19 upvotes ·36 comments
* * *
*   1965: the British Army invades Rhodesia, in order to overthrow the White racist goverment and give power to blacks r/AlternateHistory•2y ago    ### 1965: the British Army invades Rhodesia, in order to overthrow the White racist goverment and give power to blacks     254 upvotes ·96 comments
* * *
*   10 September 1967. Gibraltar held a referendum on whether to pass under Spanish sovereignty or retain its link with Britain. The result was extraordinary: 12,138 voted to remain British. Just 44 voted for Spanish sovereignty. Turnout was 96.6%.r/ThisDayInHistory•2mo ago    ### 10 September 1967. Gibraltar held a referendum on whether to pass under Spanish sovereignty or retain its link with Britain. The result was extraordinary: 12,138 voted to remain British. Just 44 voted for Spanish sovereignty. Turnout was 96.6%.      1K upvotes ·353 comments
* * *
</excerpt>
### Rank 5 of 124 — 0.74
<excerpt title="Barbados gains independence from the UK and adopts its 'Broken Trident ...">
# People also ask about section
People also ask about
Meaning of Barbados Broken Trident flag
Best resources on Barbados flag symbolism
Comparison of flags with tridents
Most iconic flags and their stories
Symbolism behind national flags

# More posts you may like
Related posts
*   30 November 1966: Barbados gains independence from the UK and adopts its ‘Broken Trident’ flag, symbolising the severing of colonial ties r/vexillology•1y ago    ### 30 November 1966: Barbados gains independence from the UK and adopts its ‘Broken Trident’ flag, symbolising the severing of colonial ties      159 upvotes ·11 comments
* * *
*    airbnb  •Ad    Introvert tip: Book somewhere where your phone "doesn't work".       airbnb.com Book Now
* * *
*   30 November 1966: Barbados gains independence from the UK and adopts a flag symbolising the severing of colonial status r/vexillology•4y ago    ### 30 November 1966: Barbados gains independence from the UK and adopts a flag symbolising the severing of colonial status      26 upvotes ·3 comments
* * *
*   19 September 1983: Saint Kitts and Nevis gains independence from the UK and adopts a new flag r/vexillology•2y ago    ### 19 September 1983: Saint Kitts and Nevis gains independence from the UK and adopts a new flag      31 upvotes ·5 comments
* * *
*   25 November 1975: Suriname gains independence from the Netherlands and adopts a new flag r/vexillology•2y ago    ### 25 November 1975: Suriname gains independence from the Netherlands and adopts a new flag      21 upvotes ·3 comments
* * *
*   3 November 1978: Dominica gains independence from the UK and adopts a new flag r/vexillology•2y ago    ### 3 November 1978: Dominica gains independence from the UK and adopts a new flag      17 upvotes ·5 comments
* * *
*   The Fabian Plot: How Tony Blair and the Elites DESTROYED Britain r/ukpolitics•1y ago    ### The Fabian Plot: How Tony Blair and the Elites DESTROYED Britain      38 comments
* * *
</excerpt>

## Search 3 — query: "female president of Dominica 2024"
### Rank 1 of 56 — 0.86 (passed on)
<excerpt title="Dominica | 79th session - General Debate - the United Nations">
# Dominica | 79th session - General Debate
Skip to main content / navigation
Welcome to the United Nations
*   العربية  
*   中文  
*   English  
*   Français  
*   Русский  
*   Español
General Debate
General Assembly
English Search
*   العربية  
*   中文  
*   English  
*   Français  
*   Русский  
*   Español
Search
Find
General Debate
General Assembly

# Dominica | 79th session - General Debate
## MENU
*   General Debate  
*   All Sessions  
*   General Assembly  
*   UN Journal  
*   UN News  
*   MEETINGS COVERAGE

# Dominica | 79th session - General Debate
## English Language
*   العربية  
*   中文  
*   English  
*   Français  
*   Русский  
*   Español

# Dominica | 79th session - General Debate
## Search
Search
Find
1.   Home  
2.   79th session  
3.   Dominica
*   **Statement**(active tab)
Statement
Dominica
Her Excellency
Sylvanie Burton
President
25 September 2024
Kaltura
[Video 3](blob:https://gadebate.un.org/1659cfec-ef1a-4a71-a56b-32063c19fc71)
Play
Play
Show Transcript
Share
00:00
Play
Seek 10 seconds backwards
Seek 10 seconds forward
00:00 / 23:31
Mute
Volume control
Press TAB to open volume control Use the arrows to control the volume
Audio
Enable Captions
Settings
Turn on Picture in picture
Show Full screen
More transcript options
Popout transcript
Hide Transcript
Skip transcript
Activates to move focus to the Resume AutoScroll button
00:00
[Transcription automatique : des erreurs sont possibles] Président de la République du Sénégal.
00:07
L'Assemblée va écouter l'allocution
00:10
de Son Excellence Sylvanie Burton,
00:13
Présidente du Commonwealth de Dominique.
00:16
Je prie le protocole de bien vouloir escorter Son Excellence
00:21
et l'invite à prendre la parole devant l'Assemblée.
00:42
Madame Présidente.
00:43
Madame la Présidente, Mabrika, Mabrika.
00:48
Je vous salue dans la langue du peuple Kalinago, mon peuple,
00:55
les premiers peuples des Caraïbes,
00:59
dont je suis fière d'être la descendante.
01:02
Je vous salue chaleureusement au nom des citoyens de l'île
01:05
de la nature des Caraïbes,
01:07
et patrie de la médaille d'or olympique Teahla Fongatsong,
01:12
le Commonwealth de Dominique.
01:15
</excerpt>
### Rank 2 of 56 — 0.85
<excerpt title="Dominica | 79th session - General Debate - the United Nations">
# Dominica | 79th session - General Debate
## Search
Search
Find
1.   Home  
2.   79th session  
3.   Dominica
*   **Statement**(active tab)
Statement
Dominica
Her Excellency
Sylvanie Burton
President
25 September 2024
Kaltura
[Video 3](blob:https://gadebate.un.org/1659cfec-ef1a-4a71-a56b-32063c19fc71)
Play
Play
Show Transcript
Share
00:00
Play
Seek 10 seconds backwards
Seek 10 seconds forward
00:00 / 23:31
Mute
Volume control
Press TAB to open volume control Use the arrows to control the volume
Audio
Enable Captions
Settings
Turn on Picture in picture
Show Full screen
More transcript options
Popout transcript
Hide Transcript
Skip transcript
Activates to move focus to the Resume AutoScroll button
00:00
[Transcription automatique : des erreurs sont possibles] Président de la République du Sénégal.
00:07
L'Assemblée va écouter l'allocution
00:10
de Son Excellence Sylvanie Burton,
00:13
Présidente du Commonwealth de Dominique.
00:16
Je prie le protocole de bien vouloir escorter Son Excellence
00:21
et l'invite à prendre la parole devant l'Assemblée.
00:42
Madame Présidente.
00:43
Madame la Présidente, Mabrika, Mabrika.
00:48
Je vous salue dans la langue du peuple Kalinago, mon peuple,
00:55
les premiers peuples des Caraïbes,
00:59
dont je suis fière d'être la descendante.
01:02
Je vous salue chaleureusement au nom des citoyens de l'île
01:05
de la nature des Caraïbes,
01:07
et patrie de la médaille d'or olympique Teahla Fongatsong,
01:12
le Commonwealth de Dominique.
01:15
</excerpt>
### Rank 3 of 56 — 0.84
<excerpt title="The United States congratulates Sylvanie Burton on her ascension to ...">
# The United States congratulates... - U.S. Embassy Bridgetown | Facebook
Log In
Log In
Forgot Account?

# The United States congratulates... - U.S. Embassy Bridgetown | Facebook
## U.S. Embassy Bridgetown's Post
* * *
[](https://www.facebook.com/USEmbassyBridgetown?__cft__[0]=AZhpj3juixzozywOGWCtebiFVvR7WTqpFI_k6seXrOlinIKpbbWYpiQgfK48pJ31RoWvAx8iyrHLIJLmnhbQQk2YC0S9Em-rAyLyz5f082HwsTERz8bnldw_3AgIsHZnIeuGoca9gKt8B51OL9L93lXvc1RFx1g&__tn__=%3C%3C%2CP-R)
### [**U.S. Embassy Bridgetown**](https://www.facebook.com/USEmbassyBridgetown?__cft__[0]=AZhpj3juixzozywOGWCtebiFVvR7WTqpFI_k6seXrOlinIKpbbWYpiQgfK48pJ31RoWvAx8iyrHLIJLmnhbQQk2YC0S9Em-rAyLyz5f082HwsTERz8bnldw_3AgIsHZnIeuGoca9gKt8B51OL9L93lXvc1RFx1g&__tn__=-UC%2CP-R)
Thursday, September 28, 2023 at 7:03 PM

# The United States congratulates... - U.S. Embassy Bridgetown | Facebook
## U.S. Embassy Bridgetown's Post
[September 28, 2023](https://www.facebook.com/USEmbassyBridgetown/posts/pfbid0eSKCmy6ouvT4MP9LFSNQiqPNALejRgj43rQSryiEMksE5FEGKnmtr5GivfLMGHqsl?__cft__[0]=AZhpj3juixzozywOGWCtebiFVvR7WTqpFI_k6seXrOlinIKpbbWYpiQgfK48pJ31RoWvAx8iyrHLIJLmnhbQQk2YC0S9Em-rAyLyz5f082HwsTERz8bnldw_3AgIsHZnIeuGoca9gKt8B51OL9L93lXvc1RFx1g&__tn__=%2CO%2CP-R) ·
The United States congratulates Sylvanie Burton on her ascension to President-elect of Dominica.  She has made history as Dominica’s first female and first indigenous President-elect. The United States looks forward to working with President-elect Burton and the Government of Dominica to further strengthen democracy, improve citizen security, and foster sustainable growth and inclusive economic prosperity.
[](https://www.facebook.com/photo/?fbid=630034952642737&set=a.190738909905679&__cft__[0]=AZhpj3juixzozywOGWCtebiFVvR7WTqpFI_k6seXrOlinIKpbbWYpiQgfK48pJ31RoWvAx8iyrHLIJLmnhbQQk2YC0S9Em-rAyLyz5f082HwsTERz8bnldw_3AgIsHZnIeuGoca9gKt8B51OL9L93lXvc1RFx1g&__tn__=EH-R)
</excerpt>
### Rank 4 of 56 — 0.84
<excerpt title="The United States congratulates Sylvanie Burton on her ascension to ...">
# The United States congratulates... - U.S. Embassy Bridgetown | Facebook
## U.S. Embassy Bridgetown's Post
[September 28, 2023](https://www.facebook.com/USEmbassyBridgetown/posts/pfbid0eSKCmy6ouvT4MP9LFSNQiqPNALejRgj43rQSryiEMksE5FEGKnmtr5GivfLMGHqsl?__cft__[0]=AZhpj3juixzozywOGWCtebiFVvR7WTqpFI_k6seXrOlinIKpbbWYpiQgfK48pJ31RoWvAx8iyrHLIJLmnhbQQk2YC0S9Em-rAyLyz5f082HwsTERz8bnldw_3AgIsHZnIeuGoca9gKt8B51OL9L93lXvc1RFx1g&__tn__=%2CO%2CP-R) ·
The United States congratulates Sylvanie Burton on her ascension to President-elect of Dominica.  She has made history as Dominica’s first female and first indigenous President-elect. The United States looks forward to working with President-elect Burton and the Government of Dominica to further strengthen democracy, improve citizen security, and foster sustainable growth and inclusive economic prosperity.
[](https://www.facebook.com/photo/?fbid=630034952642737&set=a.190738909905679&__cft__[0]=AZhpj3juixzozywOGWCtebiFVvR7WTqpFI_k6seXrOlinIKpbbWYpiQgfK48pJ31RoWvAx8iyrHLIJLmnhbQQk2YC0S9Em-rAyLyz5f082HwsTERz8bnldw_3AgIsHZnIeuGoca9gKt8B51OL9L93lXvc1RFx1g&__tn__=EH-R)

# The United States congratulates... - U.S. Embassy Bridgetown | Facebook
## U.S. Embassy Bridgetown's Post
![Image 4](blob:http://localhost/85d8b181a20aeb64a3afc2f1c39d2480)
![Image 5](blob:http://localhost/2b45e6f1a2ae097354c0b291152873d5)
All reactions:
14
8 comments
3 shares
Like
Comment
Most relevant
Dawn Atley
Congratulations  are in order President -elect Slyvanie Burton!
*   [3y](https://www.facebook.com/USEmbassyBridgetown/posts/pfbid0eSKCmy6ouvT4MP9LFSNQiqPNALejRgj43rQSryiEMksE5FEGKnmtr5GivfLMGHqsl?comment_id=1362024807729561&__cft__[0]=AZhpj3juixzozywOGWCtebiFVvR7WTqpFI_k6seXrOlinIKpbbWYpiQgfK48pJ31RoWvAx8iyrHLIJLmnhbQQk2YC0S9Em-rAyLyz5f082HwsTERz8bnldw_3AgIsHZnIeuGoca9gKt8B51OL9L93lXvc1RFx1g&__tn__=R]-R)
1
![Image 7](blob:http://localhost/2b45e6f1a2ae097354c0b291152873d5)
</excerpt>
### Rank 5 of 56 — 0.84
<excerpt title="Head of State">
# Head of State - Government of Dominica Web Portal
*    ePortal  
*    Webmail  
*    Govt Directory
Search
1.    You are here:   
2.   Home  
3.   About Dominica  
4.   Head of State

# Head of State
Her Excellency
Sylvanie Burton
_Her Excellency Sylvanie Burton_
On Monday, October 2nd 2023, Her Excellency President **Sylvanie Burton** was inaugurated at the State House, following her receipt of the Dominica Award Of Honour a day prior. Mrs. Burton's election was decisively confirmed with a 20-5 vote during the Fifth Meeting of The First Session of The Eleventh Parliament on September 27, 2023. Notably, she has made history as both the first female and the first indigenous individual to assume the esteemed role of President of Dominica.
Hailing from Salybia, within the Kalinago Territory, Mrs. Burton has an illustrious background in public service. Her most recent position was that of Permanent Secretary in the Ministry of Environment, Rural Modernization, Kalinago Upliftment, and Constituency Empowerment.
Visit the website of the Office of the President to read more.

# Head of State
### Related Pages
*   Country Profile  
*   Head of Government  
*   Head of State  
*   National Symbols  
*   Public Holidays

# Head of State
### Current Weather
Loading weather...
30°C (86°F)
Source: weather.gov.dm

# Head of State
### Contact Us
Address
Ground Floor
Government Headquarters
Kennedy Avenue
Roseau
Commonwealth of Dominica
Email
cscentre@dominica.gov.dm
Phone
+1 767 266 3000 / 3500
Fax
+1 767 448 5044

# Head of State
### Useful Links
*   Notices  
*   Vacancies  
*   Scholarships  
*   Government Directory  
*   Government Publications  
*   Services

*   Privacy & Copyright Notices  
*   Disclaimer  
*   Opt-out of Tracking
Copyright © 2026 - Government of the Commonwealth of Dominica
Search
*   Home  
*   Laws  
*   Forms  
*   Ministries  
    *   Agriculture, Fisheries, Blue and Green Economy  
    *   Culture, Youth, Sports and Community Development  
    *   Education, Human Resource Planning, Vocational Training and National Excellence  
    *   Environment, Rural Modernisation, Kalinago Upliftment and Constituency Empowerment  
    *   Finance, Economic Development, Climate Resilience and Social Security  
    *   Foreign Affairs, International Business, Trade and Energy  
    *   Health, Wellness and Social Services  
    *   Housing and Urban Development  
    *   Investment and Governance  
    *   Labour, Public Service Reform, Social Partnership, Entrepreneurship and Small Business Development  
    *   National Security and Legal Affairs  
    *   Public works, Public Utilities and Digital Economy  
    *   Tourism

*   Departments  
    *   Audit Department  
    *   Chambers of the Attorney General  
    *   Electoral Office  
    *   Establishment, Personnel and Training Department  
    *   Government Information Service  
    *   House of Assembly  
    *   Office of the President  
    *   Office of the Prime Minister  
    *   Public and Police Service Commissions

*   About Dominica  
    *   Country Profile  
    *   Head of Government  
    *   Head of State  
    *   National Symbols  
        *   Coat of Arms  
        *   National Anthem  
        *   National Bird  
        *   National Flag  
        *   National Flower  
        *   National Pledge  
        *   National Prayer

    *   Public Holidays

*   Contact Us
</excerpt>

## Search 4 — query: "female governor general of Belize 2024"
### Rank 1 of 61 — 0.72 (passed on)
<excerpt title="Froyla Tzalam">
From Wikipedia, the free encyclopedia
| Her ExcellencyDame Froyla Tzalam GCMG |  
| --- |  
|  Tzalam in 2022 |  
|  |  
| 3rd Governor-General of Belize |  
| **Incumbent** |  
| **Assumed office** 27 May 2021 |  
| Monarchs | Elizabeth II Charles III |  
| Prime Minister | Johnny Briceño |  
| Preceded by | Sir Colville Young |  
| Personal details |  
| Born | 27 July 1971 (age 55) San Antonio, British Honduras (now Belize) |  
| Party | Independent |  
| Spouse | Daniel Mendez[[1]](https://en.wikipedia.org/wiki/Froyla_Tzalam#cite_note-1) |  
| Children | 2[[2]](https://en.wikipedia.org/wiki/Froyla_Tzalam#cite_note-2) |  
| Education | Trinity University (BA) University of Sussex (MA) |  
|  |
Dame **Froyla Tzalam**GCMG (born July 27, 1971) is a BelizeanMopan Mayaanthropologist and community leader, who has served as the third governor-general of Belize since 27 May 2021.
She is the first indigenous person of Maya descent to serve as governor-general of any country in the history of the Commonwealth of Nations.[[3]](https://en.wikipedia.org/wiki/Froyla_Tzalam#cite_note-3)[[4]](https://en.wikipedia.org/wiki/Froyla_Tzalam#cite_note-4)
Tzalam is from the village of San Antonio, Toledo. She graduated with a BA degree in Anthropology from Trinity University, Texas. This was followed by a MA degree in Rural Development from University of Sussex.[[5]](https://en.wikipedia.org/wiki/Froyla_Tzalam#cite_note-5)

She was Director of the African-Maya History Program in the Belize Ministry for Education and then Director of the Belize Institute of Social and Cultural Research. She became the executive director of the Sarstoon Temash Institute for Indigenous Management (SATIIM) in 2014.[[6]](https://en.wikipedia.org/wiki/Froyla_Tzalam#cite_note-6)[[7]](https://en.wikipedia.org/wiki/Froyla_Tzalam#cite_note-7)
Tzalam was shortlisted for nomination to the Senate in January 2017, but declined in order to concentrate on her work with SATIIM.[[8]](https://en.wikipedia.org/wiki/Froyla_Tzalam#cite_note-8)
</excerpt>
### Rank 2 of 61 — 0.72
<excerpt title="Froyla Tzalam">
## Governor-General of Belize
1.   ↑"Prime Minister John Briceño Independence Day Address 2021". 21 September 2021.  
2.   ↑"Heartiest congratulations to Her Excellency Froyla Tzalam on her appointment as Governor General!! Ms. Tzalam is a woman of substance, of keen intellect, and of deep and abiding commitment to Belize and all our people. She will surely do us proud in executing her duties as our country's highest official. We wish her, her husband Daniel Mendez, and her lovely children Yasil and Yanil all of God's richest blessings today... - Ministry of Human Development, Families and Indigenous Peoples' Affairs". Retrieved 21 August 2023– via Facebook.  
3.   ↑"First Woman of Maya Descent Elected as Governor - General in the Commonwealth". 31 May 2021. Retrieved 21 August 2023.  
4.   ↑"Congratulatory Outpouring for GG Froyla T'zalam". Channel 5 Belize. Archived from the original on 17 April 2023. Retrieved 21 August 2023.  
5.   ↑"froyla tzalam". _Namati_.  
6.   ↑"SATIIM Congratulates Froyla Tz'alam as Belize's First Mopan Governor General". Retrieved 1 December 2025– via Facebook.  
7.   ↑"Staff & Board of Directors". SATIIM.  
8.   ↑"SATIIM's Froyla Tzalam Explains Decision to Decline Nomination". Channel 5 Belize. 6 January 2017. Archived from the original on 24 April 2021. Retrieved 24 April 2021.  
9.   ↑"PM Confirms Nomination of Froyla Tzalam as the next Governor General". _lovefm.com_. 22 April 2021. Archived from the original on 23 April 2021. Retrieved 23 April 2021.  
10.   ↑"Court circular: March 21, 2022". _The Times_.  

## Governor-General of Belize
11.   ↑"Governor General Froyla T'zalam Bestowed Title of Dame". Channel 5 Belize. Archived from the original on 11 June 2022. Retrieved 21 August 2023.  
12.   ↑@royalinstablog (23 March 2022). "Investiture Ceremony" (Tweet) – via Twitter.  
13.   ↑"GG attends the Queen's Platinum Jubilee". _Amandala Newspaper_. 4 June 2022.  
14.   ↑"Governor General Dame Froyla Tzalam issues statement following the passing of Queen Elizabeth II; Flags to be flown at half-mast". _Breaking Belize News_. 8 September 2022.  
15.   ↑"GG Froyla Tzalam to Attend The Queen's Funeral". _LoveFM_. 9 September 2022. Archived from the original on 12 September 2022. Retrieved 12 September 2022.  
16.   ↑"Principal Attendance at the Coronation of Their Majesties King Charles III and Queen Camilla, Saturday 6th May 2023". _The Coronation Roll_. Government of the United Kingdom. Archived from the original on 5 May 2024. Retrieved 3 May 2024.
</excerpt>
### Rank 3 of 61 — 0.68
<excerpt title="Froyla Tzalam Biography">
## Politician
Governor-General of Belize
2000 -today
EN.WIKIPEDIA PAGE VIEWS (PV)
1.   Memorability Metrics  
2.   Data Insights  
3.   Trending Activity  
4.   Page views of Froyla Tzalam by language  
5.   Among Politicians  
6.   Contemporaries  
7.   In Belize  
8.   Among Politicians In Belize

## Politician
### Froyla Tzalam
Her biography is available in 24 different languages on Wikipedia (up from 21 in 2024). Froyla Tzalam is the 16,609th most popular politician (up from 18,923rd in 2024), the 8th most popular biography from Belize (up from 9th in 2019) and the 8th most popular Belizean Politician.

## Politician
### Froyla Tzalam
#### Memorability Metrics


## Politician
### Froyla Tzalam
#### 72k
Page Views
Past 12 months

## Politician
### Froyla Tzalam
#### 53.14
HPI
Historical Popularity Index

## Politician
### Froyla Tzalam
#### Data Insights


## Politician
### Froyla Tzalam
#### +32k
Froyla Tzalam climbed 32,471 places in Pantheon's global HPI ranking, from #100,323 to #67,978.

## Politician
### Froyla Tzalam
#### Page views of Froyla Tzalam by language


## Politician
### Froyla Tzalam
#### Among Politicians
Among politicians, Froyla Tzalam ranks **16,602** out of 20,022.Before her are Patrick Achi, Maria do Carmo Silveira, Joseph Lyons, Eanfrith of Bernicia, Laurent Nkunda,  and Matthias Platzeck.After her are David Owen, Alexei Kudrin, Alain Madelin, Sinan Oğan, Arthur Whitten Brown,  and Alexandre de Moraes.
*

## Patrick Achi
1955 -Present
**HPI:**53.15
**Rank:**16,603
*

## Maria do Carmo Silveira
1961 -Present
**HPI:**53.15
**Rank:**16,604
*

## Joseph Lyons
1879 -1939
**HPI:**53.14
**Rank:**16,605
*

## Eanfrith of Bernicia
590 -634
**HPI:**53.14
**Rank:**16,606
*

## Laurent Nkunda
1967 -Present
**HPI:**53.14
**Rank:**16,607
*

## Matthias Platzeck
1953 -Present
**HPI:**53.14
**Rank:**16,608
*

## Froyla Tzalam
2000 -Present
**HPI:**53.14
**Rank:**16,609
*

## David Owen
1938 -Present
**HPI:**53.14
**Rank:**16,610
*

## Alexei Kudrin
1960 -Present
**HPI:**53.14
**Rank:**16,611
*

## Alain Madelin
1946 -Present
**HPI:**53.14
**Rank:**16,612
*

## Sinan Oğan
1967 -Present
**HPI:**53.13
**Rank:**16,613
*

## Arthur Whitten Brown
1886 -1948
**HPI:**53.13
**Rank:**16,614
*

## Alexandre de Moraes
1968 -Present
**HPI:**53.12
**Rank:**16,615
</excerpt>
### Rank 4 of 61 — 0.67
<excerpt title="Queen Samantha Ramirez and the Governor General of Belize, Her ...">
# Queen Samantha Ramirez and the Governor... - Queen of the Bay | Facebook
## Queen of the Bay's Post
* * *
[](https://www.facebook.com/OfficialQueenoftheBay?__cft__[0]=AZjMJzmzUdW8NX-tp4pLdKsVDu6kCB6YpMNDB_ZcncfI5-3a41AlqFrI129D63XVMvvCl4HBFvrJZCRhCFtttchD6FL3yAA2OqTYqqUbmc7DWsBxh24paHkieD3LtuTrxipkVraPKerZ1wmMD_uHANvPmg89f71n&__tn__=%3C%3C%2CP-R)
### **[Queen of the Bay](https://www.facebook.com/OfficialQueenoftheBay?__cft__[0]=AZjMJzmzUdW8NX-tp4pLdKsVDu6kCB6YpMNDB_ZcncfI5-3a41AlqFrI129D63XVMvvCl4HBFvrJZCRhCFtttchD6FL3yAA2OqTYqqUbmc7DWsBxh24paHkieD3LtuTrxipkVraPKerZ1wmMD_uHANvPmg89f71n&__tn__=-]C%2CP-R)** is with **[Samantha Ramirez](https://www.facebook.com/nice.pretty.sammy?__cft__[0]=AZjMJzmzUdW8NX-tp4pLdKsVDu6kCB6YpMNDB_ZcncfI5-3a41AlqFrI129D63XVMvvCl4HBFvrJZCRhCFtttchD6FL3yAA2OqTYqqUbmc7DWsBxh24paHkieD3LtuTrxipkVraPKerZ1wmMD_uHANvPmg89f71n&__tn__=-]C%2CP-R)**.
Tuesday, August 25, 2026 at 11:00 PM

# Queen Samantha Ramirez and the Governor... - Queen of the Bay | Facebook
## Queen of the Bay's Post
[August 25](https://www.facebook.com/OfficialQueenoftheBay/posts/pfbid02zGWpSUi7uX396ZNETL87QVzsQyW5outYq4fMzHENdFonTmZCZdmg7aqXbysaCEibl?__cft__[0]=AZjMJzmzUdW8NX-tp4pLdKsVDu6kCB6YpMNDB_ZcncfI5-3a41AlqFrI129D63XVMvvCl4HBFvrJZCRhCFtttchD6FL3yAA2OqTYqqUbmc7DWsBxh24paHkieD3LtuTrxipkVraPKerZ1wmMD_uHANvPmg89f71n&__tn__=%2CO%2CP-R) ·
Queen Samantha Ramirez and the Governor General of Belize, Her Excellency, Dame Froyla Tzalam.
The Governor General visit was a moment of wisdom, inspiration, and motivation to be an ambassador for our communities and country. Her excellency is an exemplary woman, and is always a sought-after visit during pageant week.
[](https://www.facebook.com/photo/?fbid=1998725774399704&set=a.668788180726810&__cft__[0]=AZjMJzmzUdW8NX-tp4pLdKsVDu6kCB6YpMNDB_ZcncfI5-3a41AlqFrI129D63XVMvvCl4HBFvrJZCRhCFtttchD6FL3yAA2OqTYqqUbmc7DWsBxh24paHkieD3LtuTrxipkVraPKerZ1wmMD_uHANvPmg89f71n&__tn__=EH-R)
</excerpt>
### Rank 5 of 61 — 0.67
<excerpt title="Froyla Tzalam Facts for Kids">
| Quick facts for kids Her ExcellencyDame Froyla Tzalam GCMG |  
| --- |  
|  Tzalam in 2022 |  
|  |  
| 3rd Governor-General of Belize |  
| **Incumbent** |  
| **Assumed office** 27 May 2021 |  
| Monarch | Elizabeth II Charles III |  
| Prime Minister | Johnny Briceño |  
| Preceded by | Sir Colville Young |  
| Personal details |  
| Born | San Antonio, Toledo, British Honduras (now Belize) |  
| Spouse | Daniel Mendez |  
| Children | 2 |  
| Alma mater | Trinity University (BA) University of Sussex (MA) |  
|  |
**Dame Froyla Tzalam** is a very important leader in Belize. She is a Mopan Mayaanthropologist, which means she studies human societies and cultures. She is also a community leader. Since May 27, 2021, she has been the third governor-general of Belize.
She is the first person from an indigenous (native) background, specifically of Maya descent, to become a governor-general in any country that is part of the Commonwealth of Nations. The Commonwealth is a group of countries that used to be part of the British Empire.

## Contents
*   Early Life and Education  
*   Her Work Before Becoming Governor-General  
*   Becoming Governor-General  
    *   Important Moments as Governor-General  
        *   Meeting Royal Family Members  
        *   Serving Under Two Monarchs

*   See also

## Early Life and Education
Froyla Tzalam grew up in a village called San Antonio, Toledo in Belize. She went to Trinity University in Texas, USA. There, she earned a degree in Anthropology.
After that, she continued her studies at the University of Sussex in the United Kingdom. She earned a master's degree in Rural Development. This field of study focuses on improving life in country areas.

## Her Work Before Becoming Governor-General
Before becoming Governor-General, Froyla Tzalam was the executive director of an organization called the Sarstoon Temash Institute for Indigenous Management (SATIIM). This group works to protect the rights and lands of indigenous people in Belize.
She was considered for a role in the Senate in 2017. The Senate is part of the government that helps make laws. However, she decided not to take the position. She wanted to keep focusing on her important work with SATIIM.

## Becoming Governor-General
| Viceregal styles of **Dame Froyla Tzalam (2021–present)** |  
| --- |  
|  |  
| Reference style | Her Excellency |  
| Spoken style | Your Excellency |
On April 22, 2021, the Prime Minister of Belize, John Briceno, announced that Froyla Tzalam would be the next Governor-General. She took over from Sir Colville Young. She is the third person to hold this important job and the second woman.

## Becoming Governor-General
### Important Moments as Governor-General
#### Meeting Royal Family Members
Dame Froyla meeting Dame Cindy Kiro, Governor-General of New Zealand, in London, 2022
In March 2022, Dame Froyla Tzalam received a special honor. She was made a Dame Grand Cross of the Order of St Michael and St George by Prince William, Duke of Cambridge. He gave her this award on behalf of Elizabeth II, who was the Queen of Belize at the time. This happened during a special visit by Prince William to Belize.
In June 2022, she traveled to the United Kingdom. She attended the Queen's Platinum Jubilee celebrations in London. This event celebrated Queen Elizabeth II's 70 years on the throne.

## Becoming Governor-General
### Important Moments as Governor-General
#### Serving Under Two Monarchs
When Elizabeth II passed away in September 2022, Dame Froyla Tzalam became the first Governor-General of Belize to serve under two different monarchs. She served under Queen Elizabeth II and then under Charles III.
She spoke about the Queen, saying she was "much loved and respected." Dame Froyla also represented Belize at the Queen's state funeral in the United Kingdom. In 2023, she attended the Coronation of King Charles III alongside Minister Francis Fonseca.
</excerpt>

## Search 5 — query: "Jamaica governor general 2024 female"
### Rank 1 of 39 — 0.68 (passed on)
<excerpt title="Paula Llewellyn, the first female Governor General of Jamaica and ...">
•
Follow
* * *
Paula Llewellyn, the first female Governor General of Jamaica and last Governor General of Jamaica and the first President of the Republic of Jamaica, is my recommendation.
Jamaica is approaching a moment where a thoughtful generational transition in the Office of the Head of State is both natural and necessary. Sir Patrick Allen has served the nation with dignity, integrity, and a deep sense of duty.  
His contribution to Jamaica’s civic life is unquestionable, and the country owes him profound gratitude. However, time and circumstance now suggest that it is appropriate for him to step back and prioritize his health and well-being.
Recent public ceremonies, including the annual National Honours event at King’s House, have underscored the growing physical demands of the office. The visible reliance on a cane and the rigours of extended ceremonial and administrative duties highlight an unavoidable reality: the role of Head of State requires sustained mobility, stamina, and daily engagement at the highest level.
This moment calls for renewal, not criticism. Jamaica would benefit from a younger Head of State who is fully able to carry out the day-to-day responsibilities of the office with energy, visibility, and continuity. Paula represents that necessary transition. She embodies the balance of maturity, competence, and vitality required to serve the nation effectively at this stage in its development.
Supporting Paula as the next Head of State is not a rejection of Sir Patrick Allen’s legacy; it is a respectful acknowledgment of it—allowing him to retire with honour, while ensuring that the office remains fully functional, responsive, and forward-looking in service of the Jamaican people.
I thought the Governor General was appointed by the crown, but apparently they are chosen by the prime minister and is then appointed by the Crown. We learn something everyday
1 like
Reply
I’ll circle back. Comment here or like.
2 likes
Reply
9 3
</excerpt>
### Rank 2 of 39 — 0.51
<excerpt title="Ngozi Wright wants to become the first female Governor-General of ...">
# Ngozi Wright wants to become the first... - Sim Soul Sessions | Facebook
Log In
Log In
Forgot Account?

# Ngozi Wright wants to become the first... - Sim Soul Sessions | Facebook
## Sim Soul Sessions's Post
* * *
[](https://www.facebook.com/stories/103547891776530/UzpfSVNDOjM3Njk0NDgxNDY1MzY1MTM=/?view_single=false&__cft__[0]=AZgf4eaRF4GcgIfO9TJjLcOlgF93jA9I-mJAFid1R-bC_127p5wRff54SDTLG3J6nGZcRL3sbxUk9QJ5y4IRgeUlkzELRxtljBPHdgMQtMMVAFmfHKS_qV-_I0numMMMagfKBgBf3XBbioB86NXGDVlYhhPgdpGR&__tn__=%3C%3C%2CP-R)
### [**Sim Soul Sessions**](https://www.facebook.com/simsoulsessions?__cft__[0]=AZgf4eaRF4GcgIfO9TJjLcOlgF93jA9I-mJAFid1R-bC_127p5wRff54SDTLG3J6nGZcRL3sbxUk9QJ5y4IRgeUlkzELRxtljBPHdgMQtMMVAFmfHKS_qV-_I0numMMMagfKBgBf3XBbioB86NXGDVlYhhPgdpGR&__tn__=-UC%2CP-R)
Friday, May 9, 2025 at 4:24 PM

# Ngozi Wright wants to become the first... - Sim Soul Sessions | Facebook
## Sim Soul Sessions's Post
[May 9, 2025](https://www.facebook.com/simsoulsessions/posts/pfbid02U5mTGGuyNqjWPEn8rtYTzWh8KsMX898TgdiRqL7ErMaAEcth7AjUNk8YxVigm1nnl?__cft__[0]=AZgf4eaRF4GcgIfO9TJjLcOlgF93jA9I-mJAFid1R-bC_127p5wRff54SDTLG3J6nGZcRL3sbxUk9QJ5y4IRgeUlkzELRxtljBPHdgMQtMMVAFmfHKS_qV-_I0numMMMagfKBgBf3XBbioB86NXGDVlYhhPgdpGR&__tn__=%2CO%2CP-R) ·
Ngozi Wright wants to become the first female Governor-General of Jamaica. She hopes to make changes in the country that she believes the position would empower her to achieve. “To see a change,” she says, “you have to be the change.”
Ackeef Nugent wants to have his school, become an actor, and also serve as a Member of Parliament, because he feels strongly about helping his community.
Watch their FULL soul session now on our YouTube channel. [#SimSoulSessions](https://www.facebook.com/hashtag/simsoulsessions?__eep__=6&__cft__[0]=AZgf4eaRF4GcgIfO9TJjLcOlgF93jA9I-mJAFid1R-bC_127p5wRff54SDTLG3J6nGZcRL3sbxUk9QJ5y4IRgeUlkzELRxtljBPHdgMQtMMVAFmfHKS_qV-_I0numMMMagfKBgBf3XBbioB86NXGDVlYhhPgdpGR&__tn__=*NK-R)
</excerpt>
### Rank 3 of 39 — 0.49
<excerpt title="Ngozi Wright wants to become the first female Governor-General of ...">
# Ngozi Wright wants to become the first... - Sim Soul Sessions | Facebook
## Sim Soul Sessions's Post
[May 9, 2025](https://www.facebook.com/simsoulsessions/posts/pfbid02U5mTGGuyNqjWPEn8rtYTzWh8KsMX898TgdiRqL7ErMaAEcth7AjUNk8YxVigm1nnl?__cft__[0]=AZgf4eaRF4GcgIfO9TJjLcOlgF93jA9I-mJAFid1R-bC_127p5wRff54SDTLG3J6nGZcRL3sbxUk9QJ5y4IRgeUlkzELRxtljBPHdgMQtMMVAFmfHKS_qV-_I0numMMMagfKBgBf3XBbioB86NXGDVlYhhPgdpGR&__tn__=%2CO%2CP-R) ·
Ngozi Wright wants to become the first female Governor-General of Jamaica. She hopes to make changes in the country that she believes the position would empower her to achieve. “To see a change,” she says, “you have to be the change.”
Ackeef Nugent wants to have his school, become an actor, and also serve as a Member of Parliament, because he feels strongly about helping his community.
Watch their FULL soul session now on our YouTube channel. [#SimSoulSessions](https://www.facebook.com/hashtag/simsoulsessions?__eep__=6&__cft__[0]=AZgf4eaRF4GcgIfO9TJjLcOlgF93jA9I-mJAFid1R-bC_127p5wRff54SDTLG3J6nGZcRL3sbxUk9QJ5y4IRgeUlkzELRxtljBPHdgMQtMMVAFmfHKS_qV-_I0numMMMagfKBgBf3XBbioB86NXGDVlYhhPgdpGR&__tn__=*NK-R)

# Ngozi Wright wants to become the first... - Sim Soul Sessions | Facebook
## Sim Soul Sessions's Post
[](https://l.facebook.com/l.php?u=https%3A%2F%2Fyoutu.be%2FX1Qz1ozgsss%3Fsi%3DexP1ECzKGtrPliw8&h=AUAmRGGItVaQsjIr69pLqNfZEwTPyRZ7hsnjnCGD6NYpFFYrWjUCgYP6UzP0HgFOlY-llCfzSarK86xccKiKJPyLb6n4xNQK4zRJ_QTN3w9ug1o8jl5lY4hP63ivc14gZzfb7JEZ1LWmpuL2-6FdA88QLzM93UEH_OD-Ng&__tn__=H-R&c[0]=AUCjfQ9dkxFss_Quudb46Sg0Fh9yp7lbSziwrkJzrWrRc5GhxEiiGobKcRAxeBS3l9YJ7BAF4u26FZn_mPBW6GF6F7QIBjwtorWok5yDoC284V8mBsa-YNR3owdBlQSaZ40wO5lgvRnshT-YkHkIUDWzETWBldzeDFtJ2N9igBOdeHtU3O8ALO4UZVBdvYM)
</excerpt>
### Rank 4 of 39 — 0.45
<excerpt title="Paula Llewellyn Tipped To Become The Next Governor General">
# Good Riddance Paula | Paula Llewellyn Tipped To Become The Next Governor General - YouTube
## Good Riddance Paula | Paula Llewellyn Tipped To Become The Next Governor General
the Questions He Doesn't Want to Hear Senator Reverend Raphael Warnock 2.7M • 8d ago Live Playlist ()Mix (50+)9:32 Deon Jackson Miller CALLS OUT Andrew Holness & Desmond McKenzie Over Beenie Man!Michy Dex Commentary 14K • 1d ago Live Playlist ()Mix (50+)31:20 Economic Update: Professor Wolff and Hasan Piker on Socialism in America Democracy At Work and RichardDWolff 380K • 1d ago Live Playlist ()Mix (50+)[52:47 [TVCHOSUN LIVE] 11월 18일 (수) #뉴스9 - '계엄 표결 방해' 추경호 1심 무죄 뉴스TVCHOSUN 4.2K • 56 min ago Live Playlist ()Mix (50+)](https://www.youtube.com/watch?v=mz1mKDc5bIs)39:29 MIA MOTTLEY IS NOT HOLDING BACK! 🔥 HER MESSAGE HAS THE WORLD TALKING!Likkle But Wi Tallawah Reacts 9.5K • 1d ago Live Playlist ()Mix (50+)

# Good Riddance Paula | Paula Llewellyn Tipped To Become The Next Governor General
Michy Dex Commentary
Michy Dex Commentary
21K subscribers
Join
Subscribe
Subscribed
10
Download
431 views 1y ago#PaulaLlewellyn#JamaicaPolitics#GovernorGeneral
431 views • Sep 23, 2025 • #PaulaLlewellyn #JamaicaPolitics #GovernorGeneral
Jamaica — it’s the end of an era! After 41 years in public service and 17 years as Director of Public Prosecutions, Paula Llewellyn has officially stepped down. …more
more
Transcript
Follow along using the transcript.
Show transcript

# Good Riddance Paula | Paula Llewellyn Tipped To Become The Next Governor General
### Michy Dex Commentary 21K subscribers
VideosAbout

# Good Riddance Paula | Paula Llewellyn Tipped To Become The Next Governor General
## Video details
Date
Sep 23, 2025
Views
431
Likes
10
Show less
#PaulaLlewellyn#JamaicaPolitics#GovernorGeneral

# Good Riddance Paula | Paula Llewellyn Tipped To Become The Next Governor General
431 views 431 views
Sep 23, 2025
10
Download

# Good Riddance Paula | Paula Llewellyn Tipped To Become The Next Governor General
## 3 Comments
Sort comments
Sort by
Top Show featured commentsNewest Show recent comments, including potential spam
Add a comment...

# Good Riddance Paula | Paula Llewellyn Tipped To Become The Next Governor General
## 3 Comments
### @LuckiBrown
1 year ago
A long time you fi go
Show less Read more
Like
1
Dislike
Reply

# Good Riddance Paula | Paula Llewellyn Tipped To Become The Next Governor General
## 3 Comments
### @DaneSammy
1 year ago
Paula holding on power so that she can clean up Andrew Holness dirty deeds
Show less Read more
Like
1
Dislike
Reply
Top is selected, so you'll see featured comments

# Good Riddance Paula | Paula Llewellyn Tipped To Become The Next Governor General
## Comments 3
Top Show featured commentsNewest Show recent comments, including potential spam

# Good Riddance Paula | Paula Llewellyn Tipped To Become The Next Governor General
## In this video
Transcript
</excerpt>
### Rank 5 of 39 — 0.44
<excerpt title="Paula Llewellyn Tipped To Become The Next Governor General">
# Good Riddance Paula | Paula Llewellyn Tipped To Become The Next Governor General
## In this video
Transcript

# Good Riddance Paula | Paula Llewellyn Tipped To Become The Next Governor General
## Good Riddance Paula | Paula Llewellyn Tipped To Become The Next Governor General
Michy Dex Commentary
Michy Dex Commentary
10 Likes
431 Views
2025 Sep 23
Jamaica — it’s the end of an era! After 41 years in public service and 17 years as Director of Public Prosecutions, Paula Llewellyn has officially stepped down. But instead of praise, many Jamaicans are saying good riddance! For years, she was accused of shielding Andrew Holness and protecting police officers, while ordinary people cried out for justice and got none. Now, the whispers are loud — she’s allegedly tipped to become Jamaica’s next female Governor General. But the people are asking: what can go so? After covering up for the powerful, can she really be rewarded with one of the highest offices in the land? Jamaicans are clear: enough is enough. They want real change, not recycled faces of injustice. 👉 Stay tuned for more! Don’t forget to like, share, comment, and subscribe for the latest right here on Michy Dex .#PaulaLlewellyn, #JamaicaPolitics, #GovernorGeneral, #JusticeForJamaica…...more
...more Show less
Transcript
Follow along using the transcript.
Show transcript

# Good Riddance Paula | Paula Llewellyn Tipped To Become The Next Governor General
## Good Riddance Paula | Paula Llewellyn Tipped To Become The Next Governor General
### Michy Dex Commentary 21K subscribers
VideosAbout

# Good Riddance Paula | Paula Llewellyn Tipped To Become The Next Governor General
## Video details
Date
Sep 23, 2025
Views
431
Likes
10

# Good Riddance Paula | Paula Llewellyn Tipped To Become The Next Governor General
## Transcript
NaN / NaN
13:27

# Good Riddance Paula | Paula Llewellyn Tipped To Become The Next Governor General
## Transcript
### Fox News Slowly Realizes Republicans Are SCREWED
TYT Investigates
3M 11d ago
14:21 New

# Good Riddance Paula | Paula Llewellyn Tipped To Become The Next Governor General
## Transcript
### Who’s Really Disrupting Parliament? Government Ministers Defend Their Record | All Angles Segment 1
Television Jamaica
22K 5d ago
9:32:19 New

# Good Riddance Paula | Paula Llewellyn Tipped To Become The Next Governor General
## Transcript
### Sitting In the House of Repressentatives
Michy Dex Commentary
17K Streamed 8h ago
43:35 New

# Good Riddance Paula | Paula Llewellyn Tipped To Become The Next Governor General
## Transcript
### SHE NEVER GAVE UP ON TERRO FABULOUS & HE IS NOW BACK IN AMERICAN - KAMLA McINTYRE
SoundChat Radio by Irish & Chin Inc.
72K 18h ago
22:04

# Good Riddance Paula | Paula Llewellyn Tipped To Become The Next Governor General
## Transcript
### Georgia veteran deported to Jamaica fights to return home
11Alive
61K 2w ago
18:26 New

# Good Riddance Paula | Paula Llewellyn Tipped To Become The Next Governor General
## Transcript
### 'I'm Not Finished Yet' Cory Booker Clashes With Republicans On Release Of Epstein Files | N18G
CNN-News18
156K 17h ago
19:47 New

# Good Riddance Paula | Paula Llewellyn Tipped To Become The Next Governor General
## Transcript
### 'Putin couldn't have imagined' how bad Ukrainian strikes would get for the Kremlin | Bill Browder
Frontline
629K 1d ago
10:39

# Good Riddance Paula | Paula Llewellyn Tipped To Become The Next Governor General
## Transcript
### Asking RFK Jr. the Questions He Doesn't Want to Hear
Senator Reverend Raphael Warnock
2.7M 8d ago
9:32 New
</excerpt>

## Search 6 — query: "current governor general of Trinidad and Tobago 2024 female"
### Rank 1 of 88 — 0.63 (passed on)
<excerpt title="The Office of the President of the Republic of Trinidad and Tobago">
Christine Carla Kangaloo became the seventh President of the Republic of Trinidad and Tobago on March 20, 2023.
Born on December 1, 1961, in San Fernando, Her Excellency is the fifth of seven children of Carlyle and Barbara Kangaloo. Her Excellency attended Grant Memorial Presbyterian Primary School and St. Joseph’s Convent, San Fernando. She graduated with Honours in Law from the University of the West Indies in 1983 and obtained her Legal Education Certificate from the Hugh Wooding Law School in 1985, the same year she was admitted to practice law.
Having qualified as a practicing attorney, Her Excellency worked in her father’s law practice from 1985 to 1992, and briefly again between 1996 to 1998. Her Excellency also worked at an established law firm in San Fernando between 1988 to 2005. With the exception of those two (2) experiences in the private sector, Her Excellency’s working life has been all about public service.
Her Excellency’s public service career began in 1992, when she entered the Judiciary as an Assistant Registrar of the Supreme Court. It continued in the way of Parliamentary service, which began in 2001 when Her Excellency was appointed an Opposition Senator. Her Excellency subsequently served as Vice President of the Senate (2002), Government Senator and Minister in the Office of the Prime Minister (2002–2005), Minister of Legal Affairs (2005–2007), and Minister of Science, Technology and Tertiary Education (2007–2010). From 2007 to 2010, Her Excellency also served as the Member of Parliament for Pointe-a-Pierre. In 2015, Her Excellency was elected President of the Senate and, during this time, acted as President of the Republic of Trinidad and Tobago on thirty-three occasions. Her Excellency is the first person to have held the posts of Vice President and President of the Senate before becoming President.
Her Excellency’s long and varied career in public life has given her a unique and a comprehensive appreciation of the system and the mechanics of government, of public service, and of the needs of the citizens of Trinidad and Tobago.

Her Excellency’s Presidency is built on her formidable foundation of public service and her unique and varied experiences in that sphere. With the benefit of Her Excellency’s singular experiences and exposure, Her Excellency, in her address to the nation on the occasion of her inauguration as President, pledged to demystify and increase public awareness —especially among the youth— about the role of the President, and to make the Office of the President more accessible. To this end, Her Excellency has visited over 50 schools across Trinidad and Tobago to educate students about the Presidency, a mission which Her Excellency is still actively carrying out. Her Excellency envisions President’s House as a space for cultural, intellectual, and artistic exploration, and has successfully advocated for the recognition of the steel pan as the national instrument of Trinidad and Tobago. Her Excellency also pledged during her inaugural address to advocate for the widespread adoption of the ‘Panyard Model’ as a means of introducing discipline and the structure into the lives of our nation’s youth. True to that pledge, each year since 2024, Her Excellency has put on a ‘Pan Camp’, based on the ‘Panyard Model’, for young persons who have never previously played the instrument, and who come together for a week at The President’s House to learn how to do so, and to learn life skills in general. In keeping with her pledge to make the Office of the President more accessible, Her Excellency also regularly hosts concerts in the Band Stand adjacent to The President’s House, which are open to members of the public and which showcase not only the steelband, but all aspects of the country’s culture. In addition, Her Excellency has launched ‘Storytime’ at The President’s House to promote literacy and confidence among children; and Her Excellency hosts numerous school tours and cultural and religious events at President’s House.
</excerpt>
### Rank 2 of 88 — 0.61
<excerpt title="Christine Kangaloo">
| | Ministerial offices | | --- | | | | 8th Minister of Science, Technology and Tertiary Education | | **In office** 8 November 2007–25 May 2010 | | Preceded by | Mustapha Abdul-Hamid | | Succeeded by | Fazal Karim | | 8th Minister of Legal Affairs | | **In office** 14 May 2005–7 November 2007 | | Preceded by | Peter Taylor | | Succeeded by | Prakash Ramadhar | | 6th Minister in the Office of the Prime Minister (Social Services Delivery) | | **In office** 15 October 2002–13 May 2005 | | Preceded by | Position established | | Succeeded by | Position abolished | |  
| Personal details |  
| Born | 1 December 1961 (age 64)[[1]](https://en.wikipedia.org/wiki/Christine_Kangaloo#cite_note-auto-1) San Fernando, Trinidad and Tobago[[1]](https://en.wikipedia.org/wiki/Christine_Kangaloo#cite_note-auto-1) |  
| Party | Independent (since 2025)[[a]](https://en.wikipedia.org/wiki/Christine_Kangaloo#cite_note-3) |  
| Other political affiliations | [People's National Movement](https://en.wikipedia.org/wiki/People's_National_Movement "People's National Movement") (2001–2015) |  
| Spouse | Kerwyn Garcia ​ (m.1998)​ [[1]](https://en.wikipedia.org/wiki/Christine_Kangaloo#cite_note-auto-1) |  
| Education | * University of the West Indies (LL.B.) * Hugh Wooding Law School (LEC) |  
| Profession | * Politician * lawyer |  
| Awards | * Order of the Republic of Trinidad and Tobago (2023) * Pravasi Bharatiya Samman (2025) |  
|  |

**Christine Carla Kangaloo**ORTT (born 1 December 1961) is a Trinidadian lawyer and politician who is serving as the President of Trinidad and Tobago since 2023.[[3]](https://en.wikipedia.org/wiki/Christine_Kangaloo#cite_note-ExpressBio-4) Upon succeeding Paula-Mae Weekes on 20 March 2023, she became the first woman in the Americas to succeed another woman as Head of State.[[4]](https://en.wikipedia.org/wiki/Christine_Kangaloo#cite_note-OTP_Bio-5)[[5]](https://en.wikipedia.org/wiki/Christine_Kangaloo#cite_note-NewsdayInauguration-6) Globally, she is the second woman to achieve this feat in a parliamentary republic, following Ireland's Mary McAleese, who succeeded Mary Robinson in 1997.[[6]](https://en.wikipedia.org/wiki/Christine_Kangaloo#cite_note-CWWL-7) Additionally, she is the first woman of Indian ancestry to serve as a president of a country in the Americas.[[7]](https://en.wikipedia.org/wiki/Christine_Kangaloo#cite_note-PIB_Acceptance-8)[[8]](https://en.wikipedia.org/wiki/Christine_Kangaloo#cite_note-Pravasi_2025-9)
Prior to her presidency, Kangaloo had an extensive career in public service and the legal profession. She served as an Assistant Registrar of the Supreme Court (1992–1996) before entering Parliament as an Opposition Senator in 2001.[[9]](https://en.wikipedia.org/wiki/Christine_Kangaloo#cite_note-TTParl_Kangaloo-10) She subsequently held multiple ministerial portfolios, including Minister of Legal Affairs (2005–2007) and Minister of Science, Technology and Tertiary Education (2007–2010), and served as the Member of Parliament for Pointe-à-Pierre.[[10]](https://en.wikipedia.org/wiki/Christine_Kangaloo#cite_note-GenU_Bio-11)
</excerpt>
### Rank 3 of 88 — 0.60
<excerpt title="Christine Kangaloo">
**Christine Carla Kangaloo**ORTT (born 1 December 1961) is a Trinidadian lawyer and politician who is serving as the President of Trinidad and Tobago since 2023.[[3]](https://en.wikipedia.org/wiki/Christine_Kangaloo#cite_note-ExpressBio-4) Upon succeeding Paula-Mae Weekes on 20 March 2023, she became the first woman in the Americas to succeed another woman as Head of State.[[4]](https://en.wikipedia.org/wiki/Christine_Kangaloo#cite_note-OTP_Bio-5)[[5]](https://en.wikipedia.org/wiki/Christine_Kangaloo#cite_note-NewsdayInauguration-6) Globally, she is the second woman to achieve this feat in a parliamentary republic, following Ireland's Mary McAleese, who succeeded Mary Robinson in 1997.[[6]](https://en.wikipedia.org/wiki/Christine_Kangaloo#cite_note-CWWL-7) Additionally, she is the first woman of Indian ancestry to serve as a president of a country in the Americas.[[7]](https://en.wikipedia.org/wiki/Christine_Kangaloo#cite_note-PIB_Acceptance-8)[[8]](https://en.wikipedia.org/wiki/Christine_Kangaloo#cite_note-Pravasi_2025-9)
Prior to her presidency, Kangaloo had an extensive career in public service and the legal profession. She served as an Assistant Registrar of the Supreme Court (1992–1996) before entering Parliament as an Opposition Senator in 2001.[[9]](https://en.wikipedia.org/wiki/Christine_Kangaloo#cite_note-TTParl_Kangaloo-10) She subsequently held multiple ministerial portfolios, including Minister of Legal Affairs (2005–2007) and Minister of Science, Technology and Tertiary Education (2007–2010), and served as the Member of Parliament for Pointe-à-Pierre.[[10]](https://en.wikipedia.org/wiki/Christine_Kangaloo#cite_note-GenU_Bio-11)

Christine Kangaloo was born into a PresbyterianIndo-Trinidadian family to Carlyle and Barbara Kangaloo and she is the fifth of their seven children.[[1]](https://en.wikipedia.org/wiki/Christine_Kangaloo#cite_note-auto-1)[[11]](https://en.wikipedia.org/wiki/Christine_Kangaloo#cite_note-12)[[12]](https://en.wikipedia.org/wiki/Christine_Kangaloo#cite_note-13) In 2018, she and her husband converted to Roman Catholicism.[[13]](https://en.wikipedia.org/wiki/Christine_Kangaloo#cite_note-14) She graduated from the University of the West Indies and Hugh Wooding Law School and with a degree in law. Christine Kangaloo began her legal career in 1985, working alongside her father, Carlyle at his law firm in San Fernando, Trinidad.[[14]](https://en.wikipedia.org/wiki/Christine_Kangaloo#cite_note-GenUnlimited2023-15) Their professional partnership continued until his passing in 1996.[[14]](https://en.wikipedia.org/wiki/Christine_Kangaloo#cite_note-GenUnlimited2023-15)
</excerpt>
### Rank 4 of 88 — 0.53
<excerpt title="Christine Kangaloo">
14.   12"H.E. Ms. Christine Carla Kangaloo". _Generation Unlimited_. UNICEF. Retrieved 29 June 2025.  
15.   ↑"Kangaloo to act as President of Trinidad & Tobago". _Trinidad and Tobago Government News_. Retrieved 15 July 2020._[permanent dead link_]  
16.   ↑"The Trinidad Guardian -Online Edition Ver 2.0". _Trinidad and Tobago Guardian_. Archived from the original on 17 July 2020. Retrieved 15 July 2020.  
17.   ↑"The Trinidad Guardian -Online Edition Ver 2.0". _Trinidad and Tobago Guardian_. Archived from the original on 15 July 2020. Retrieved 15 July 2020.  
18.   ↑Lord, Richard. "?PM: Two elections coming this year". _Trinidad and Tobago Guardian_. Retrieved 15 July 2020.  
19.   ↑"Battle over Marabella sports ground". _Trinidad and Tobago Newsdday_. 5 March 2008. Retrieved 15 July 2020.  
20.   ↑"T&T Guardian". Retrieved 15 July 2020– via Facebook.  
21.   ↑"Trinidad and Tobago Parliament". Trinidad and Tobago Parliament. Archived from the original on 1 April 2018. Retrieved 15 July 2020.  
22.   ↑"96.1 WEFM". Retrieved 15 July 2020– via Facebook.  
23.   ↑"Photos of the Day: President Inauguration". Trinidad and Tobago Newsday. 21 March 2023. Retrieved 24 March 2023.  
24.   ↑"Ms. Christine Kangaloo elected President of the Republic of Trinidad and Tobago". _Parliament of Trinidad and Tobago_. 20 January 2023. Retrieved 12 March 2026.
*   Parliamentary ProfileArchived 5 October 2015 at the Wayback Machine, Trinidad and Tobago Parliament website
</excerpt>
### Rank 5 of 88 — 0.46
<excerpt title="A Year in the Life of the 7th President. Her Excellency Christine Carla ...">
# Video
## Related videos
[ 0:39](https://www.facebook.com/100064534549298/videos/1170884428930037/?__so__=permalink&__cft__[0]=AZgVuKwR91qGab72lT31Du1STS09glPF6_h57pKc-l1TvcHW5i-olptqIBwvmPGxzKvg0MJXdGKN__lh0S_pWWxeBJ_OIcEnWsZDfn6sYPIUlgThQCm1d4F60JDsKukv5nCh6ZFIpqTvUZ_iWgrBhQ)
[](https://www.facebook.com/watch/100064534549298/?__cft__[0]=AZgVuKwR91qGab72lT31Du1STS09glPF6_h57pKc-l1TvcHW5i-olptqIBwvmPGxzKvg0MJXdGKN__lh0S_pWWxeBJ_OIcEnWsZDfn6sYPIUlgThQCm1d4F60JDsKukv5nCh6ZFIpqTvUZ_iWgrBhQ)

# Video
## Related videos
[#Happeningnow Her Excellency Christine Carla Kangaloo, ORTT, President of the Republic of Trinidad and Tobago is attending the 'No Smoking No Vaping Education Initiative' organised by the Trinidad and Tobago Cancer Society, in collaboration with Scotiabank, at Holy Name Convent, Port of Spain. The campaign, which targets secondary school students, aims to raise awareness to teens and parents on the health effects and dangers associated with vaping and smoking. Holy Name Convent POS Trinidad and Tobago Cancer Society](https://www.facebook.com/100064534549298/videos/1170884428930037/?__so__=permalink&__cft__[0]=AZgVuKwR91qGab72lT31Du1STS09glPF6_h57pKc-l1TvcHW5i-olptqIBwvmPGxzKvg0MJXdGKN__lh0S_pWWxeBJ_OIcEnWsZDfn6sYPIUlgThQCm1d4F60JDsKukv5nCh6ZFIpqTvUZ_iWgrBhQ)
</excerpt>

## Search 7 — query: "Dominica independence 1978 date"
### Rank 1 of 42 — 0.82 (passed on)
<excerpt title="Commonwealth of Dominica: Independence Celebrations">
# Commonwealth of Dominica: Independence Celebrations
**Google Translate:**
English▼
EnglishالعربيةFrançaisEspañol
*     
*     
*     
*     
*     
*
**Switch Language:**
Select your language
EN

# Commonwealth of Dominica: Independence Celebrations
*   FR  
*   EN



  
*   Who we are 

    *   About Us  
    *   Policies

        *   Gender Policy  
        *   Sexual Exploitation, Abuse and Harassment Policy  
        *   Grievance Redress  
        *   Environmental and Social Safeguards Framework  
        *   Whistleblower Policy  
        *   Anti-fraud Policy  
        *   Misuse of Funds Policy

    *   Member States  
    *   FAQs  
    *   Logos  
    *   Leadership Team  
    *   Strategic Priorities  
    *   Our History  
    *   Our Structure  
    *   Institutions  
    *   Development Partners

*   Our Work 

    *   Economic Affairs

        *   Regional Integration  
        *   Agriculture  
        *   Business Development  
        *   Tourism  
        *   Trade  
        *   Statistics

    *   Environmental Sustainability

        *   Biodiversity  
        *   Climate and Disaster Resilience  
        *   Energy  
        *   Oceans Governance

    *   Human and Social

        *   Health  
        *   Gender Equality  
        *   Education  
        *   Social Inclusion and Protection  
        *   Youth

    *   Diplomatic

        *   Embassies to the European Union  
        *   Eastern Carbbean Liaison Service  
        *   International Relations  
        *   Geneva Mission  
        *   Embassies to Morocco

    *   Projects / Initiatives  
    *   Legal and Governance  
    *   Knowledge Centre

*   News

    *   Newsroom  
    *   Newslink  
    *   E- News Bulletins  
    *   Green Link Newsletter  
    *   OECS Integrates  
    *   OECS Boxing Championship  
    *   Miss OECS Pageant

*   Opportunities

    *   For Job Seekers

        *   External Vacancies  
        *   Open Position  
        *   Full Time Consultant Position

    *   For Consultants 

        *   Current Tenders  
        *   Procurement Procedures  
        *   Procurement Plan  
        *   Grants Awarded  
        *   Register Here  
        *   Contracts Awarded

    *   Regional

*   Contact Us

# Commonwealth of Dominica: Independence Celebrations
## Festivals and Events Commonwealth of Dominica: Independence Celebrations
*     
*     
*   [](javascript:void((function()%7Bvar%20e=document.createElement('script');e.setAttribute('type','text/javascript');e.setAttribute('charset','UTF-8');e.setAttribute('src','http://assets.pinterest.com/js/pinmarklet.js?r='+Math.random()*99999999);document.body.appendChild(e)%7D)());)

# Commonwealth of Dominica: Independence Celebrations
## Festivals and Events Commonwealth of Dominica: Independence Celebrations
##### Short Overview
Every year, Dominica commemorates its Independence with a season of cultural activities from September to November. These celebrations portray vivid examples of the island's cultural influences. The traditional dances display European traces in Hill & Toe, Waltz, and Quadrille; and borrow from African native dances in Bèlè.
This mélange of Creole culture predominates at this time of year, as villages and communities throughout the island compete to show their superiority in preserving and developing different cultural expressions. Certain days, such as Kwèyòl Day, Heritage Day, and National Day promote different aspects of the island's cultural heritage. The government also holds parades and rallies for all to express their allegiance to the country.
Dominica received its independence from Britain on November 3rd 1978.
</excerpt>
### Rank 2 of 42 — 0.82
<excerpt title="Happy Independence Day, #Dominica! 🇩🇲 On November 3, 1978 ...">
# Happy... - Caribbean Community Climate Change Centre | Facebook
Log In
Log In
Forgot Account?

# Happy... - Caribbean Community Climate Change Centre | Facebook
## Caribbean Community Climate Change Centre's Post
* * *
[](https://www.facebook.com/stories/553080905569097/UzpfSVNDOjE0MDU2NDUxNTQ2OTg4NDQ=/?view_single=false&__cft__[0]=AZhOEYGKF8b8lpmZ5t_u6wOUq8i1w2bvr6y-xO8LumVi5-oe3M3FTnhLdD5zSoYtiKJQyl1Q-2DzUMGhZzXrsA53w6KoPVRnD6-El74Ng7KpRfgru0LFsXJonv-cBCLXfc6M55a7S7tIHPT6kXX_0rp1IzAD7rke&__tn__=%3C%3C%2CP-R)
### [**Caribbean Community Climate Change Centre**](https://www.facebook.com/caricomclimate?__cft__[0]=AZhOEYGKF8b8lpmZ5t_u6wOUq8i1w2bvr6y-xO8LumVi5-oe3M3FTnhLdD5zSoYtiKJQyl1Q-2DzUMGhZzXrsA53w6KoPVRnD6-El74Ng7KpRfgru0LFsXJonv-cBCLXfc6M55a7S7tIHPT6kXX_0rp1IzAD7rke&__tn__=-UC%2CP-R)
Tuesday, November 3, 2026 at 12:00 PM

# Happy... - Caribbean Community Climate Change Centre | Facebook
## Caribbean Community Climate Change Centre's Post
[November 3 at 12:00 PM](https://www.facebook.com/caricomclimate/posts/pfbid02w79iiCWXBEUbk6STLjWPJ5J5iy9AZFLmuvZR2UwyxVXywHGU2xc6Gd1M9WAZgckZl?__cft__[0]=AZhOEYGKF8b8lpmZ5t_u6wOUq8i1w2bvr6y-xO8LumVi5-oe3M3FTnhLdD5zSoYtiKJQyl1Q-2DzUMGhZzXrsA53w6KoPVRnD6-El74Ng7KpRfgru0LFsXJonv-cBCLXfc6M55a7S7tIHPT6kXX_0rp1IzAD7rke&__tn__=%2CO%2CP-R) ·
Happy Independence Day, [#Dominica](https://www.facebook.com/hashtag/dominica?__eep__=6&__cft__[0]=AZhOEYGKF8b8lpmZ5t_u6wOUq8i1w2bvr6y-xO8LumVi5-oe3M3FTnhLdD5zSoYtiKJQyl1Q-2DzUMGhZzXrsA53w6KoPVRnD6-El74Ng7KpRfgru0LFsXJonv-cBCLXfc6M55a7S7tIHPT6kXX_0rp1IzAD7rke&__tn__=*NK-R)!
On November 3, 1978, Dominica proudly claimed its sovereignty, raising the green flag of the "Nature Island" of the Caribbean. Shaped by 365 rivers, misty rainforest peaks, and a rich Kalinago heritage, Dominica’s spirit is woven into the soul of its Creole traditions, the legendary Boiling Lake, and the joyous cadence of its independence cultural celebrations.
</excerpt>
### Rank 3 of 42 — 0.81
<excerpt title="Happy Independence Day, Dominica! 🇩🇲 To all Dominicans, at home and ...">
# NWE - Happy Independence Day, Dominica! 🇩🇲 To all... | Facebook
Log In
Log In
Forgot Account?

# NWE - Happy Independence Day, Dominica! 🇩🇲 To all... | Facebook
## NWE's Post
* * *
[](https://www.facebook.com/NWEworldwide?__cft__[0]=AZgsfvVuiGYHwIYBHQxLvrUMoXaY0VAGIGc6IAgBa2iK46X_37oNfKjIdn5pWvVSVljPsE-1PNmACvW95ebwAY2hujvWTc29lqZa8ywA_ffZzdX9MepFTUSYJuajjQHjfm2vO62ZPetgXN_Yf8Va_LKyrU6gmVpK&__tn__=%3C%3C%2CP-R)
### **[NWE](https://www.facebook.com/NWEworldwide?__cft__[0]=AZgsfvVuiGYHwIYBHQxLvrUMoXaY0VAGIGc6IAgBa2iK46X_37oNfKjIdn5pWvVSVljPsE-1PNmACvW95ebwAY2hujvWTc29lqZa8ywA_ffZzdX9MepFTUSYJuajjQHjfm2vO62ZPetgXN_Yf8Va_LKyrU6gmVpK&__tn__=-]C%2CP-R)** is in **[Dominica](https://www.facebook.com/Dominica-108585965832328/?__cft__[0]=AZgsfvVuiGYHwIYBHQxLvrUMoXaY0VAGIGc6IAgBa2iK46X_37oNfKjIdn5pWvVSVljPsE-1PNmACvW95ebwAY2hujvWTc29lqZa8ywA_ffZzdX9MepFTUSYJuajjQHjfm2vO62ZPetgXN_Yf8Va_LKyrU6gmVpK&__tn__=kC%2CP-R)**.

# NWE - Happy Independence Day, Dominica! 🇩🇲 To all... | Facebook
## NWE's Post
Tuesday, November 3, 2026 at 11:32 PM
[November 3 at 11:32 PM](https://www.facebook.com/NWEworldwide/posts/pfbid02V3FDjEKUzBcFzH4i7FVQ2W3P2ku2NFAbQE88LicFedT3xQbrG2tEQ6tNxagFEe9Jl?__cft__[0]=AZgsfvVuiGYHwIYBHQxLvrUMoXaY0VAGIGc6IAgBa2iK46X_37oNfKjIdn5pWvVSVljPsE-1PNmACvW95ebwAY2hujvWTc29lqZa8ywA_ffZzdX9MepFTUSYJuajjQHjfm2vO62ZPetgXN_Yf8Va_LKyrU6gmVpK&__tn__=%2CO%2CP-R) ·
Happy Independence Day, Dominica!
To all Dominicans, at home and around the world.
On 3 November, Dominica marked 48 years of independence since 1978.
Between Guadeloupe and Martinique lies the Caribbean’s Nature Island, known for its volcanic landscapes, rainforests and waterfalls.
Its story is also carried by its people: through Creole dress, music, dance, food and craft shared across generations. From the colours of its flag to the traditions celebrated in its streets, there is so much to discover and so much to be proud of.
Sending love to Dominicans everywhere. Where are you celebrating from?
Photos:
</excerpt>
### Rank 4 of 42 — 0.79
<excerpt title="Commonwealth of Dominica: Independence Celebrations">
# Commonwealth of Dominica: Independence Celebrations
## Festivals and Events Commonwealth of Dominica: Independence Celebrations
##### Short Overview
Every year, Dominica commemorates its Independence with a season of cultural activities from September to November. These celebrations portray vivid examples of the island's cultural influences. The traditional dances display European traces in Hill & Toe, Waltz, and Quadrille; and borrow from African native dances in Bèlè.
This mélange of Creole culture predominates at this time of year, as villages and communities throughout the island compete to show their superiority in preserving and developing different cultural expressions. Certain days, such as Kwèyòl Day, Heritage Day, and National Day promote different aspects of the island's cultural heritage. The government also holds parades and rallies for all to express their allegiance to the country.
Dominica received its independence from Britain on November 3rd 1978.

# Commonwealth of Dominica: Independence Celebrations
## Festivals and Events Commonwealth of Dominica: Independence Celebrations
### Property ID COM231004R698


# Commonwealth of Dominica: Independence Celebrations
## Festivals and Events Commonwealth of Dominica: Independence Celebrations
### Property Rent
$ 0 / Month
$ 0 (Price Per Unit)
* * *

# Commonwealth of Dominica: Independence Celebrations
## Festivals and Events Commonwealth of Dominica: Independence Celebrations
### Commonwealth of Dominica


# Commonwealth of Dominica: Independence Celebrations
## Festivals and Events Commonwealth of Dominica: Independence Celebrations
### Property Enquiry Request For Visit
- [x]  I agree with the Terms of Use and Privacy Policy and I declare that I have read the information that is required in accordance with Article 13 of GDPR.
Submit
Morne Fortune, Castries, Saint Lucia
Phone:+1 (758) 455-6327
Contact the OECS Commission
External Vacancies
Events
FAQs
OECS Laissez-Passer Certificate
Grievance RedressIntranet
Subscribe to OECS Newsletter
- [x] I agree with the Terms of Use and agree to receive email bulletins for email, direct email and customized online marketing and I declare that I have read the information that is required in accordance with Article 13 of GDPR.
Subscribe
*     
*     
*     
*     
*     
*
© 2023 Organisation of Eastern Caribbean States.
</excerpt>
### Rank 5 of 42 — 0.78
<excerpt title="November 3 In 1978, Dominica achieved full independence ...">
# Today in History: November 3 In 1978, Dominica achieved full independence, with Patrick Roland John as its first prime minister. Dominica was in a long fight for independence first ruled by the Spanish, then the French and then the British, before finally obtaining independence. #ournews_nov03 #OurNews | Our News Bahamas | Facebook
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
Today in History: November 3
Like
Comment
Share
![Image 2](blob:http://localhost/85d8b181a20aeb64a3afc2f1c39d2480)
5
·
432 views

# Video
## **Our News Bahamas**
Thursday, November 3, 2022 at 11:23 PM
November 3, 2022 ·
Follow
Today in History: November 3…
See more

# Video
## Comments


# Video
## Related Reels
Our News Bahamas 16K
Our News Bahamas 10K
Our News Bahamas 24K
Our News Bahamas 8.6K
Our News Bahamas 9.5K
Our News Bahamas 32K
Our News Bahamas 7.2K
Our News Bahamas 7.3K
Our News Bahamas 3.2K
Our News Bahamas 12K
Our News Bahamas 24K
Our News Bahamas 12K

# Video
## Related videos
[ 0:55](https://www.facebook.com/100064811853640/videos/992773780079473/?__so__=permalink&__cft__[0]=AZhx3_fLmwZlD1e_hsQF5qOnO3yW-miquQikjPIckvnm1oCrUojasetpNDI6fqc2xuywNe1nM1V7SFakss6-HMgkUGVO7ahtbw_OyECTfqkjZbxPGXMD_YyApTCHvp1929z0z2fWWoFnLH-y0tEYUA)
[](https://www.facebook.com/watch/100064811853640/?__cft__[0]=AZhx3_fLmwZlD1e_hsQF5qOnO3yW-miquQikjPIckvnm1oCrUojasetpNDI6fqc2xuywNe1nM1V7SFakss6-HMgkUGVO7ahtbw_OyECTfqkjZbxPGXMD_YyApTCHvp1929z0z2fWWoFnLH-y0tEYUA)
[Celebrities Hit Baha Mar Red Carpet as $50K Donation Supports Bahamian Youth](https://www.facebook.com/100064811853640/videos/992773780079473/?__so__=permalink&__cft__[0]=AZhx3_fLmwZlD1e_hsQF5qOnO3yW-miquQikjPIckvnm1oCrUojasetpNDI6fqc2xuywNe1nM1V7SFakss6-HMgkUGVO7ahtbw_OyECTfqkjZbxPGXMD_YyApTCHvp1929z0z2fWWoFnLH-y0tEYUA)
</excerpt>

## Search 8 — query: "Governor General of the Bahamas 2024 female"
### Rank 1 of 38 — 0.79 (passed on)
<excerpt title="Office of the Governor-General">
# Governor General
*   Home  
*   [Governor General](javascript:void(0);)

*
[](javascript:void(0) "Share")  
    *     
    *     
    *

# Governor General
#### The Government
Overview and Structure of the Government
*   Structure of the Branches of Government  
*   Governor General
The Judiciary
*   Overview of Judicial Branch  
*   The Judicature
Table of Precedence for The Commonwealth of The Bahamas
The Executive Branch
*   Prime Minister  
*   The Cabinet  
*   Members of Parliament and Senators  
*   Cabinet Ministers
Central Government
*   PSC Regulations  
*   General Orders
The Legislative Branch
*   About the Parliament  
*   The Senate  
*   Senators  
*   The House of Assembly
Local Government
HER EXCELLENCY
**THE MOST HON. CYNTHIA ALEXANDRIA**
**PRATT, ON, GCMG, CB, CD, JP**
**GOVERNOR-GENERAL**
Governor-General,
The Office of The Government House
Government Hill
P.O. Box N-8301
Nassau, N.P., The Bahamas
**Ph:**[(242)-322-1875-7](tel:24232218757), [(242)-356-0254](tel:2423560254)
**Fax:** (242)-322-4659
* * *
*   Duties of the Governor-General  
*   Previous Governors-General

# Governor General
### Quick Useful Links
*   Budget Performance Reports  
*   Budget Documents  
*   Preparing Your Home and Family for a Hurricane  
*   General Orders  
*   Request for Expression of Interest  
*   Hurricane Shelter Listing 2025  
*   Install the BNEA APP  
*   COVID-19 Frequent Asked Questions  
*   Department of Labour’s Jobseekers Portal  
*   Celebrate Bahamas  
*   Amended Government Resolution for RBC $80M  
*   General Borrowing Resolution FY2026-27  
*   Resolution - Blue Economy  
*   Resolution - BMC NIB 2026  
*   Resolution - BMC RBC  
*   Resolution - ELA NIB
[Load More](javascript:;)

# Governor General
## For Website Technical Support
#### Call and speak to a DICT Customer service agent.
[+1 242 604 4688](tel:+12426044688 "Call us on: +1 242 604 4688")

# Governor General
## For Website Technical Support
#### Need to reach the DICT? Send us an email.
[support@bahamas.gov.bs](mailto:support@bahamas.gov.bs "Email us on: support@bahamas.gov.bs")

# Governor General
## For Website Technical Support
#### Get in touch with our DICT support team.
get in touch

# Governor General
## For Website Technical Support
#### Explore frequently asked questions.
ask question

# Governor General
## For Website Technical Support
#### Browse
*   Budget Press Releases  
*   The Government  
*   Agencies  
*   Services  
*   Bahamas  
*   News and Press Release

# Governor General
## For Website Technical Support
#### Help
*   EServices  
*   Help Portal  
*   Contact Us  
*   FAQs  
*   State Directory  
*   Customer Service
</excerpt>
### Rank 2 of 38 — 0.76
<excerpt title="SAU Alumna Cynthia “Mother” Pratt Will Serve as Bahamas Governor ...">
# SAU Alumna Cynthia “Mother” Pratt Will Serve as Bahamas Governor General - Saint Augustine's University
*     
*     
*     
*     
*   

*   Alumni  
*   Faculty & Staff  
*   Media  
*   Parents & Guardians  
*   Visitors

# SAU Alumna Cynthia “Mother” Pratt Will Serve as Bahamas Governor General - Saint Augustine's University
### Welcome
**Forgot password?**  
Not a member? **Join today**
[](javascript:;)
*   About SAU  
    *   SAU at a Glance  
    *   SAU & Raleigh  
    *   Strategic Plan  
    *   University Leadership  
    *   History  
    *   Faculty & Staff Directory  
    *   Campus Safety  
    *   SAU & the Episcopal Church  
    *   Offices & Departments  
    *   Consumer Information  
    *   University Compliance  
    *   Title IX

*   Academics  
    *   Programs  
    *   Professional Studies & Services  
    *   Certification/Non-Credit Course  
    *   Student Portal  
    *   Library  
    *   Academic Calendar  
    *   Registrar  
    *   University Catalog  
    *   Accreditation

*   Admissions & Financial Aid  
    *   Apply  
    *   Admissions  
    *   Financial Aid and Scholarships  
    *   Registration  
    *   Open House  
    *   Recruitment Viewbook  
    *   Tuition and Fees  
    *   Veterans Affairs

*   Students  
    *   Student Services  
    *   Student Accounts  
    *   Student Portal  
    *   Self-Service Tutorials  
    *   Library  
    *   Commencement  
    *   Parents  
    *   Email  
    *   Brightspace  
    *   Reset SAU Email Password

*   Athletics  
*   Giving  
*   News

# SAU Alumna Cynthia “Mother” Pratt Will Serve as Bahamas Governor General - Saint Augustine's University
## Latest Blog
22 Aug 2023
*   staugadmin  
*   Alumni, General

# SAU Alumna Cynthia “Mother” Pratt Will Serve as Bahamas Governor General - Saint Augustine's University
## SAU Alumna Cynthia “Mother” Pratt Will Serve as Bahamas Governor General
Bahamas Prime Minister announced SAU class of 1983 alumna Cynthia “Mother” Pratt will serve as the Bahamas’ next governor-general. Her position will be effective September 1.
Mother Pratt’s leadership and contributions to nursing, education, politics, sports, and religion are well known throughout the Bahamas. She was the first woman to serve as deputy prime minister and the first woman to serve as minister of national security.
Read more**here**.
Previous ArticleNext Article

# SAU Alumna Cynthia “Mother” Pratt Will Serve as Bahamas Governor General - Saint Augustine's University
## SAU Alumna Cynthia “Mother” Pratt Will Serve as Bahamas Governor General
### SAINT AUGUSTINE’S UNIVERSITY
1315 Oakwood Avenue
Raleigh, NC 27610-2298
919.516.4000
*     
*     
*   [](https://www.linkedin.com/school/saint-augustine's-college/)  
*     
*

# SAU Alumna Cynthia “Mother” Pratt Will Serve as Bahamas Governor General - Saint Augustine's University
## SAU Alumna Cynthia “Mother” Pratt Will Serve as Bahamas Governor General
### Information For:
*   Alumni  
*   Faculty & Staff  
*   Media  
*   Parents & Guardians  
*   Visitors
</excerpt>
### Rank 3 of 38 — 0.76
<excerpt title="Cynthia A. Pratt">
## Early life and education
After retiring from the College of The Bahamas, Pratt entered politics and became a Member of Parliament in 1997 representing the constituency of St. Cecilia.[[1]](https://en.wikipedia.org/wiki/Cynthia_A._Pratt#cite_note-bgov-1) She served for 15 years as the Member of Parliament for the St. Cecilia constituency.[[2]](https://en.wikipedia.org/wiki/Cynthia_A._Pratt#cite_note-2)
In 2002, following the victory of the Progressive Liberal Party in the national elections, Pratt became the first female Deputy Prime Minister of the Bahamas, a role she served till 2007. She served as acting Prime Minister in 2005 when PM Perry Christie suffered a stroke.[[3]](https://en.wikipedia.org/wiki/Cynthia_A._Pratt#cite_note-3)
Pratt was also the first woman to serve as the Minister of National Security.[[1]](https://en.wikipedia.org/wiki/Cynthia_A._Pratt#cite_note-bgov-1) She held the portfolio from 2002 to 2007.[[4]](https://en.wikipedia.org/wiki/Cynthia_A._Pratt#cite_note-secminbah-4)
Pratt served as the deputy to the Governor-General of the Bahamas on several occasions.[[5]](https://en.wikipedia.org/wiki/Cynthia_A._Pratt#cite_note-opm-5)
In August 2023, Prime Minister Philip Davis announced that he had recommended to King Charles III that Pratt be appointed as the next Governor-General of the Bahamas.[[5]](https://en.wikipedia.org/wiki/Cynthia_A._Pratt#cite_note-opm-5) On 1 September 2023, Pratt was sworn in as the 12th Governor-General of the Bahamas during a ceremony at Government House.[[6]](https://en.wikipedia.org/wiki/Cynthia_A._Pratt#cite_note-6) In her inaugural address as governor-general, Pratt said, "As a mother my eyes and ears are always open to the needs of our young people and the importance of doing all we can to uplift them so that as they grow into adulthood and inherit full responsibility for the continued development of our nation".[[7]](https://en.wikipedia.org/wiki/Cynthia_A._Pratt#cite_note-7)

## Early life and education
Pratt was married to Joseph B. Pratt until his death. They had six children (including a deceased adopted son).[[1]](https://en.wikipedia.org/wiki/Cynthia_A._Pratt#cite_note-bgov-1)
On 10 November 2017, Pratt launched her biography, _An Ordinary Woman from the Heart of the Inner City_, published by Scholar Books. Publisher Albert Cox reported at the launch that 35,000 copies had been sold already. Vernon Lynch, brother of actor Eddie Murphy, said he would make Pratt's book into a movie.[[8]](https://en.wikipedia.org/wiki/Cynthia_A._Pratt#cite_note-8)
Pratt is an ordained Minister of the Gospel.[[1]](https://en.wikipedia.org/wiki/Cynthia_A._Pratt#cite_note-bgov-1)
In 2018, Pratt was appointed as a Companion of the Order of Distinction (CD).[[9]](https://en.wikipedia.org/wiki/Cynthia_A._Pratt#cite_note-9) In the 2023 Independence Honours, Pratt was appointed as a Companion of the Order of the Bahamas (CB).[[10]](https://en.wikipedia.org/wiki/Cynthia_A._Pratt#cite_note-10)
Upon taking office as governor-general, Pratt was conferred with the Order of the Nation (ON), and was sworn in as chancellor of the National Honours Society of The Bahamas.[[11]](https://en.wikipedia.org/wiki/Cynthia_A._Pratt#cite_note-11)
She was appointed Dame Grand Cross of the Order of St Michael and St George (GCMG) in February 2024.[[12]](https://en.wikipedia.org/wiki/Cynthia_A._Pratt#cite_note-12)
</excerpt>
### Rank 4 of 38 — 0.75
<excerpt title="PRESS RELEASE - THE GOVERNOR GENERAL OF THE BAHAMAS TO ...">
# PRESS... - Ministry of International Relations, Botswana | Facebook
## Ministry of International Relations, Botswana's Post
[July 25, 2024](https://www.facebook.com/MinistryofInternationalAffairsBW/posts/pfbid02VinCJbXu4LJEHsvN5yD9La9K1NSb4jLva2bGgbHMYmy1RNyh5j9ic1wrnWSJ7b29l?__cft__[0]=AZiWmuIlgC2kC7wCssDEj_vK0z7TuAqsZ0OpphX5RaS4LD36LYjFDOVqi4BD2gOhaSiD8w8MI-PIorP4LPz8rd90aVXK8QNeWxkCuWVlOThWVJz5wRXgNFF1r8xsnEbJCw3yrKv3tXzehFkXTlXX22uCw3i-GHw&__tn__=%2CO%2CP-R) ·
PRESS RELEASE - THE GOVERNOR GENERAL OF THE BAHAMAS TO UNDERTAKE A STATE VISIT TO BOTSWANA
GABORONE, 25th July 2024: Her Excellency the Most Honourable Dame Cynthia Alexandria Pratt, Governor General of the Commonwealth of The Bahamas, will undertake a State Visit to Botswana, from 29th July to 2nd August 2024, at the invitation of His Excellency Dr. Mokgweetsi Eric Keabetswe Masisi, President of the Republic of Botswana.
The State Visit aims to further strengthen the existing bilateral relations between Botswana and The Bahamas, as well as explore areas for enhanced cooperation such as in the tourism, finance, trade and investment sectors. While in Botswana, the Governor General will hold Official Talks with President Masisi, and also receive progress updates on the implementation of decisions emanating from the Official Visit to Botswana by The Right Honourable Phillip E. Davis, Prime Minister of The Bahamas, in March 2024, as well as the State Visit undertaken by President Masisi to The Bahamas, in September 2023. Additionally, the Governor General will among others, visit the Diamond Trading Company Botswana (DTCB).

# PRESS... - Ministry of International Relations, Botswana | Facebook
## Ministry of International Relations, Botswana's Post
Botswana and The Bahamas established formal diplomatic relations in May 2006. Over the years, the two countries have enjoyed cordial relations, and have cooperated in various areas including education, particularly in the higher learning sector.
The Governor General will be accompanied by the Minister of Foreign Affairs, Honourable Frederick A. Mitchell, and Senior Government Officials.
</excerpt>
### Rank 5 of 38 — 0.75
<excerpt title="SAU Alumna Cynthia “Mother” Pratt Will Serve as Bahamas Governor ...">
# SAU Alumna Cynthia “Mother” Pratt Will Serve as Bahamas Governor General - Saint Augustine's University
## SAU Alumna Cynthia “Mother” Pratt Will Serve as Bahamas Governor General
### Information For:
*   Alumni  
*   Faculty & Staff  
*   Media  
*   Parents & Guardians  
*   Visitors

# SAU Alumna Cynthia “Mother” Pratt Will Serve as Bahamas Governor General - Saint Augustine's University
## SAU Alumna Cynthia “Mother” Pratt Will Serve as Bahamas Governor General
### Quick Links
*   Apply  
*   Registration  
*   Employment  
*   Coronavirus Information  
*   Commencement  
*   Request a Transcript  
*   Saint Augustine’s Chapel  
*   Giving  
*   Strategic Plan  
*   Student Complaints  
*   Events  
*   University Compliance  
*   Policies and Procedures  
*   Privacy Statement

# SAU Alumna Cynthia “Mother” Pratt Will Serve as Bahamas Governor General - Saint Augustine's University
## SAU Alumna Cynthia “Mother” Pratt Will Serve as Bahamas Governor General
### Resources
*   Campus Safety  
*   Student Portal  
*   Employee Portal  
*   Brightspace  
*   Office 365  
*   Campus Store  
*   Faculty & Staff Directory  
*   Map  
*   Marketing Service Forms  
*   The Prezell R. Robinson Library  
*   Joseph G. Gordon Health Center  
*   Space Reservations  
*   Technology Support  
*   Title IX
© Copyright 2022 Saint Augustine's University
Notifications
</excerpt>

## Search 9 — query: "Trinidad and Tobago independence date 1962"
### Rank 1 of 159 — 0.84 (passed on)
<excerpt title="Trinidad and Tobago">
Its mission statement is to "defend the sovereign good of The Republic of Trinidad and Tobago, contribute to the development of the national community and support the State in the fulfilment of its national and international objectives". The Defence Force has been engaged in domestic incidents, such as the Black Power Movement of 1970 and Jamaat al Muslimeen coup attempt, and international missions, such as the United Nations Mission in Haiti between 1993 and 1996.
In 2019, Trinidad and Tobago signed the UN treaty on the Prohibition of Nuclear Weapons.[140]
Trinidad and Tobago is the 87th most peaceful country in the world, according to the 2024 Global Peace Index.[141]
Foreign relationsedit  
Further information: Foreign relations of Trinidad and Tobago  
Diplomatic missions of Trinidad and Tobago
Trinidad and Tobago maintains close relations with its Caribbean neighbours and major North American and European trading partners. As the most industrialised and second-largest country in the Anglophone Caribbean, Trinidad and Tobago has taken a leading role in the Caribbean Community (CARICOM), and strongly supports CARICOM economic integration efforts. It also is active in the Summit of the Americas process and supports the establishment of the Free Trade Area of the Americas, lobbying other nations for seating the Secretariat in Port of Spain.[142]
As a member of CARICOM, Trinidad and Tobago strongly backed efforts by the United States to bring political stability to Haiti, contributing personnel to the Multinational Force in 1994. After its 1962 independence from the United Kingdom, Trinidad and Tobago joined the United Nations and Commonwealth of Nations. In 1967 it became the first Commonwealth country to join the Organization of American States (OAS).[143] In 1995 Trinidad played host to the inaugural meeting of the Association of Caribbean States and has become the seat of this 35-member grouping, which seeks to further economic progress and integration among its states. In international forums, Trinidad and Tobago has defined itself as having an independent voting record, but often supports US and EU positions.[144][145]
Law enforcement and crimeedit  
Main article: Crime in Trinidad and Tobago
</excerpt>
### Rank 2 of 159 — 0.83
<excerpt title="Trinidad and Tobago">
Trinidad and Tobago,[d] officially the Republic of Trinidad and Tobago, is the southernmost archipelagic country in the Caribbean, comprising the main islands of Trinidad and Tobago, along with several smaller islets. The capital city is Port of Spain, while its largest and most populous municipality is Chaguanas. Trinidad and Tobago comprises the southernmost islands of the Caribbean eastern islands chain,[11] and it is close to the continent of South America, being north to northeast of Venezuela and northwest of Guyana.[11]
Trinidad and Tobago is located six nautical miles (11 km; 6.9 mi) north to northeast off the coast of Venezuela, 70 nautical miles (130 km; 81 mi) south of Grenada, and 155 nautical miles (287 km; 178 mi) southwest of Barbados.[12][13][14] Indigenous peoples inhabited Trinidad for centuries prior to Spanish colonisation, following the arrival of Christopher Columbus in 1498. Spanish governor José María Chacón surrendered the island to a British fleet under Ralph Abercromby's command in 1797.[15] Trinidad and Tobago were ceded to Britain in 1802 under the Treaty of Amiens as separate states and unified in 1889.[16] Trinidad and Tobago obtained independence in 1962, and became a republic in 1976.[17][12]
Unlike most Caribbean countries and territories, which rely heavily on tourism, the economy is primarily industrial, based on large reserves of oil and gas.[18][19] The country sees fewer hurricanes than most of the Caribbean because it is farther south.
Trinidad and Tobago is well known for its African and Indian cultures, reflected in its large and famous Carnival, Diwali, and Hosay celebrations, as well as being the birthplace of the steelpan, the limbo, and musical styles such as calypso, soca, rapso, chutney, and chutney soca.
Toponymyedit
</excerpt>
### Rank 3 of 159 — 0.79
<excerpt title="Trinidad and Tobago">
• Province of the West Indies Federation  
	3 January 1958 – 14 January 1962
• Independence  
	31 August 1962
• Joined the Caribbean Community at the Treaty of Chaguaramas  
	1 August 1973
• Republic  
	1 August 1976[c]  
Area
• Total  
	5,131 km2 (1,981 sq mi) (164th)
• Water (%)  
	negligible  
Population
• 2025 estimate  
	1,512,779[7] (154th)
• Density  
	294/km2 (761.5/sq mi) (34th)  
GDP (PPP)	2023 estimate
• Total  
	 $43.658 billion[8] (126th)
• Per capita  
	 $30,718[8] (58th)  
GDP (nominal)	2023 estimate
• Total  
	 $27.887 billion[8] (107th)
• Per capita  
	 $19,621[8] (47th)  
Gini (2012)	39.0[9]  
medium inequality  
HDI (2023)	 0.807[10]  
very high (72nd)  
Currency	Trinidad and Tobago dollar (TTD)  
Time zone	UTC-4 (AST)  
Date format	dd/mm/yyyy  
Calling code	+1  
ISO 3166 code	TT  
Internet TLD	.tt
</excerpt>
### Rank 4 of 159 — 0.79
<excerpt title="August 31, 1962 — T&T's moment of destiny">
# August 31, 1962 — T&T’s moment of destiny
## Publications
### Contact us
[Send us an e-mail here](mailto:newsroom@guardian.co.tt) or call us at [+1-(868)-235-5668 / +1-(868)-225-4465](tel:+1-(868)-235-5668)

# August 31, 1962 — T&T’s moment of destiny
## Publications
### Follow us
Recommended for you
원본 텍스트
번역 평가
보내주신 의견은 Google 번역을 개선하는 데 사용됩니다.
</excerpt>
### Rank 5 of 159 — 0.78
<excerpt title="Happy Independence Day, Trinidad and Tobago! ❤️🖤🤍 On August 31 ...">
# Instagram
Log In
Sign Up
Never miss a post from ontariondp
Sign up for Instagram to stay in the loop.
By continuing, you agree to Instagram's Terms of Use and Privacy Policy.
Sign up
Log in
ontariondp
•
Follow
* * *
ontariondp11w
Happy Independence Day, Trinidad and Tobago! ❤️🖤🤍
On August 31, 1962, Trinidad and Tobago became independent from British rule. This was the beginning of a new chapter for this twin-island nation.
Today, we celebrate what makes Trinidad and Tobago shine, from the people to the history and communities that carry the spirit of this nation around the world.
Wishing everyone celebrating a joyful Independence Day!

# Instagram
## No comments yet.
Start the conversation.
August 31
Log in to like or comment.
* * *
More posts from ontariondp
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

## Search 10 — query: "Barbados independence 1966 November 30 1966"
### Rank 1 of 135 — 0.74 (passed on)
<excerpt title="Barbados gains independence from the UK and adopts its 'Broken Trident ...">
# People also ask about section
People also ask about
Meaning of Barbados Broken Trident flag
Best resources on Barbados flag symbolism
Comparison of flags with tridents
Most iconic flags and their stories
Symbolism behind national flags

# More posts you may like
Related posts
*   30 November 1966: Barbados gains independence from the UK and adopts its ‘Broken Trident’ flag, symbolising the severing of colonial ties r/vexillology•1y ago    ### 30 November 1966: Barbados gains independence from the UK and adopts its ‘Broken Trident’ flag, symbolising the severing of colonial ties      159 upvotes ·11 comments
* * *
*    airbnb  •Ad    Introvert tip: Book somewhere where your phone "doesn't work".       airbnb.com Book Now
* * *
*   30 November 1966: Barbados gains independence from the UK and adopts a flag symbolising the severing of colonial status r/vexillology•4y ago    ### 30 November 1966: Barbados gains independence from the UK and adopts a flag symbolising the severing of colonial status      26 upvotes ·3 comments
* * *
*   19 September 1983: Saint Kitts and Nevis gains independence from the UK and adopts a new flag r/vexillology•2y ago    ### 19 September 1983: Saint Kitts and Nevis gains independence from the UK and adopts a new flag      31 upvotes ·5 comments
* * *
*   25 November 1975: Suriname gains independence from the Netherlands and adopts a new flag r/vexillology•2y ago    ### 25 November 1975: Suriname gains independence from the Netherlands and adopts a new flag      21 upvotes ·3 comments
* * *
*   3 November 1978: Dominica gains independence from the UK and adopts a new flag r/vexillology•2y ago    ### 3 November 1978: Dominica gains independence from the UK and adopts a new flag      17 upvotes ·5 comments
* * *
*   The Fabian Plot: How Tony Blair and the Elites DESTROYED Britain r/ukpolitics•1y ago    ### The Fabian Plot: How Tony Blair and the Elites DESTROYED Britain      38 comments
* * *
</excerpt>
### Rank 2 of 135 — 0.74
<excerpt title="Barbados Gains Independence - 1966 | Today In History | 30 Nov 17">
Back  KR
Search with your voice
Sign in
KR
Barbados Gains Independence - 1966 | Today In History | 30 Nov 17
0:02 / 1:17
•Watch full video
5:4518:045:3222:394:495:0744:2852:4116:4317:329:4613:38
AP Archive
6.06M subscribers
Download
4K views 8y ago
4,074 views • Nov 29, 2017
On November 30, 1966, the former British colony of Barbados became independent. You can license this story through AP Archive: http://www.aparchive.com/metadata/you...…
more
more

## 2 Comments
Sort comments
Sort by
Add a comment...

## 2 Comments
### @chrissystewart6268
3 years ago
Happy 56 years of Independence🇧🇧🇧🇧🇧🇧 from Chrissy Stewart🇺🇸 I wish the beautiful people best wishes. Every year of Nov. 30th I will keep wishing happy independence day in 🇧🇧
Like
Dislike

## 2 Comments
### @revinhatol
4 years ago
#ItHappenedOnAWednesdayClear
Like
Dislike
Top is selected, so you'll see featured comments

## Comments 2


## Barbados Gains Independence - 1966 | Today In History | 30 Nov 17
AP Archive
33 Likes
4K Views
2017 Nov 29
On November 30, 1966, the former British colony of Barbados became independent. You can license this story through AP Archive: http://www.aparchive.com/metadata/you... Find out more about AP Archive: http://www.aparchive.com/HowWeWork Follow us on social: Twitter: /ap_archive​ Facebook: /aparchives​ Google+: https://plus.google.com/b/10201102858... Tumblr: https://aparchives.tumblr.com/​

## Barbados Gains Independence - 1966 | Today In History | 30 Nov 17
### AP Archive 6.06M subscribers
VideosAboutLinkedIn

## Video details
Date
Nov 29, 2017
Views
4,074
Likes
33

## Video details
### ADHD Child vs. Non-ADHD Child Interview
Mental Health Matters
30M 11y ago

## Video details
### Why Japan's yen is becoming a problem for the US I Business Beyond
DW News
1.8M 12d ago

## Video details
### The life, legacy & assassination of an African revolutionary - Lisa Janae Bacon
TED-Ed
588K 6y ago

## Video details
### We Sent 18 Squishy Toys To A Lab. Here’s What We Found | Talking Point
CNA Insider
2.7M 9d ago

## Video details
### “1년 전 약속대로..”... 대통령 한마디에 시진핑 ‘활짝’
JTV뉴스
633K 9h ago

## Video details
### Port of Spain in Trinidad (1970-1979) | British Pathé
British Pathé
149K 12y ago

## Video details
### [[4th Anniversary of the Itaewon Tragedy] Itaewon Tragedy 'Undisclosed Files'... A Portrait of a F...](https://www.youtube.com/watch?v=ZV-vHw6rA24&pp=ugUHEgVlbi1VUw%3D%3D)
뉴스타파 Newstapa
4.1M 3w ago
Auto-dubbed
</excerpt>
### Rank 3 of 135 — 0.72
<excerpt title="Barbados gains independence from the UK and adopts its 'Broken Trident ...">
# More posts you may like
Related posts
*   30 November 1966: Barbados gains independence from the UK and adopts its ‘Broken Trident’ flag, symbolising the severing of colonial ties r/vexillology•1y ago    ### 30 November 1966: Barbados gains independence from the UK and adopts its ‘Broken Trident’ flag, symbolising the severing of colonial ties      159 upvotes ·11 comments
* * *
*    airbnb  •Ad    Introvert tip: Book somewhere where your phone "doesn't work".       airbnb.com Book Now
* * *
*   30 November 1966: Barbados gains independence from the UK and adopts a flag symbolising the severing of colonial status r/vexillology•4y ago    ### 30 November 1966: Barbados gains independence from the UK and adopts a flag symbolising the severing of colonial status      26 upvotes ·3 comments
* * *
*   19 September 1983: Saint Kitts and Nevis gains independence from the UK and adopts a new flag r/vexillology•2y ago    ### 19 September 1983: Saint Kitts and Nevis gains independence from the UK and adopts a new flag      31 upvotes ·5 comments
* * *
*   25 November 1975: Suriname gains independence from the Netherlands and adopts a new flag r/vexillology•2y ago    ### 25 November 1975: Suriname gains independence from the Netherlands and adopts a new flag      21 upvotes ·3 comments
* * *
*   3 November 1978: Dominica gains independence from the UK and adopts a new flag r/vexillology•2y ago    ### 3 November 1978: Dominica gains independence from the UK and adopts a new flag      17 upvotes ·5 comments
* * *
*   The Fabian Plot: How Tony Blair and the Elites DESTROYED Britain r/ukpolitics•1y ago    ### The Fabian Plot: How Tony Blair and the Elites DESTROYED Britain      38 comments
* * *

# More posts you may like
*   Has Barbados gotten better since their independence with the United Kingdom? r/AskTheWorld•3y ago    ### Has Barbados gotten better since their independence with the United Kingdom?    9 upvotes ·14 comments
* * *
*   Do's and Don'ts for Tourists in Barbados? ☀️🌴 r/Barbados•2y ago    ### Do's and Don'ts for Tourists in Barbados? ☀️🌴    41 upvotes ·67 comments
* * *
*   29 September 1967: Anguilla adopts its Dolphin Flag, following its recent declaration of independence from the UK in protest at neglect by St Kitts r/vexillology•2y ago    ### 29 September 1967: Anguilla adopts its Dolphin Flag, following its recent declaration of independence from the UK in protest at neglect by St Kitts      20 upvotes ·2 comments
* * *
*   British protectorates r/maldives•14d ago    ### British protectorates     19 upvotes ·36 comments
* * *
*   1965: the British Army invades Rhodesia, in order to overthrow the White racist goverment and give power to blacks r/AlternateHistory•2y ago    ### 1965: the British Army invades Rhodesia, in order to overthrow the White racist goverment and give power to blacks     254 upvotes ·96 comments
* * *
*   10 September 1967. Gibraltar held a referendum on whether to pass under Spanish sovereignty or retain its link with Britain. The result was extraordinary: 12,138 voted to remain British. Just 44 voted for Spanish sovereignty. Turnout was 96.6%.r/ThisDayInHistory•2mo ago    ### 10 September 1967. Gibraltar held a referendum on whether to pass under Spanish sovereignty or retain its link with Britain. The result was extraordinary: 12,138 voted to remain British. Just 44 voted for Spanish sovereignty. Turnout was 96.6%.      1K upvotes ·353 comments
* * *
</excerpt>
### Rank 4 of 135 — 0.70
<excerpt title="Barbados Independence Day">
# Barbados Independence Day
## Sidebar
×
*   Home  
*   About Us  
    *   Mission Statement  
    *   Our Executive  
    *   Organization Structure  
        *   Governance  
        *   Committees

*   Events  
*   Member Organizations  
    *   Antigua and Barbuda Cultural Association of BC  
    *   Barbados Cultural Association of BC  
    *   Grenadian Cultural Association of BC  
    *   Guyanese Canadian Cultural Association of BC  
    *   Haitian Canadian Cultural Association of BC  
    *   Jamaican Canadian Cultural Association of BC  
    *   St. Kitts/Nevis Cultural Association of BC  
    *   St. Vincent and the Grenadines Cultural Society of BC  
    *   Trinidad and Tobago Cultural Society of BC  
    *   Associate Members

*   Contact Us  
*   Membership  
    *   Membership Applications

*   Photos

*   Log in
BCOCCA

# Barbados Independence Day
## Sidebar
*   Home  
*   About Us  
    *   Mission Statement  
    *   Our Executive  
    *    Organization Structure  
        *   Governance  
        *   Committees

*   Events  
*   Member Organizations  
    *   Antigua and Barbuda Cultural Association of BC  
    *   Barbados Cultural Association of BC  
    *   Grenadian Cultural Association of BC  
    *   Guyanese Canadian Cultural Association of BC  
    *   Haitian Canadian Cultural Association of BC  
    *   Jamaican Canadian Cultural Association of BC  
    *   St. Kitts/Nevis Cultural Association of BC  
    *   St. Vincent and the Grenadines Cultural Society of BC  
    *   Trinidad and Tobago Cultural Society of BC  
    *   Associate Members

*   Contact Us  
*   Membership  
    *   Membership Applications

*   Photos

*   Home  
*   About Us

    *   Mission Statement  
    *   Our Executive  
    *    Organization Structure

        *   Governance  
        *   Committees

*   Events  
*   Member Organizations

    *   Antigua and Barbuda Cultural Association of BC  
    *   Barbados Cultural Association of BC  
    *   Grenadian Cultural Association of BC  
    *   Guyanese Canadian Cultural Association of BC  
    *   Haitian Canadian Cultural Association of BC  
    *   Jamaican Canadian Cultural Association of BC  
    *   St. Kitts/Nevis Cultural Association of BC  
    *   St. Vincent and the Grenadines Cultural Society of BC  
    *   Trinidad and Tobago Cultural Society of BC  
    *   Associate Members     

*   Contact Us  
*   Membership

    *   Membership Applications

*   Photos

# Barbados Independence Day
## Events Calendar
*   [](javascript:void(0); "Print")
By Year
By Month
By Week
Today
Jump to month
Jump to month
Barbados Independence Day
Monday 30 November 2026
Previous Repeat
Next Repeat
Hits : 18523
November 30 is a national holiday in Barbados as it celebrates the nation achieving independence from Britain on**30****November 1966**.
HAPPY INDEPENCEE BARBADOS
Copyright © 2026 BCOCCA. All Rights Reserved. Designed by Griffin Communications.Joomla! is Free Software released under the GNU General Public License.
</excerpt>
### Rank 5 of 135 — 0.69
<excerpt title="Barbados - Independence Order 1966">
Title: PDF document  
URL Source: https://constitutionnet.org/sites/default/files/Barbados%20-%20Independence%20Order%201966.pdf  
Markdown Content:

## [PDF page 1]
STATUTORY INSTRUMENTS  
1966 No. 1455
CARIBBEAN AND NORTH ATLANTIC TERRITORIES
The Barbados Independence Order 1966
Made 22nd November 1966
Laid before Parliament 22nd November 1966
Coming into Operation 30th November 1966
At the Court at Buckingham Palace, the 22nd day of November 1966
Present,
The Queen's Most Excellent Majesty in Council
Her Majesty, by virtue and in exercise of the powers vested in Her by section 5 of the  
Barbados Independence Act 1966 and of all other powers enabling Her in that behalf, is  
pleased, by and with the advice of Her Privy Council, to order, and it is hereby ordered, as  
follows:
Citation commencement and construction
1. 1. This Order may be cited as the Barbados Independence Order 1966.

2. This order shall come into operation on 30th November 1966 (in this Order referred to as  
"the appointed day"):
Provided that the Governor may at any time after 22nd November 1966 exercise any of the  
powers conferred upon the Governor General by sections 4(3) and 10(1) of this Order and  
sections 60(1), 89(2), 90(1) and 91(1) of the Constitution set out in the Schedule to this Order  
(in this Order referred to as "the Constitution") to such extent as any, in his opinion, be  
necessity or expedient to enable the Constitution to function as from the appointed day.

## [PDF page 1]
3. For the purposes of the exercise by the Governor under the proviso to subsection (2) of  
the powers conferred by the said sections 89(2), 90(1) and 91(1), the references therein to  
the Prime Minister and the Leader of the Opposition shall be construed as if they were  
references respectively to the Premier and to the Leader of the Opposition as defined for the  
purposes of Schedule 2 to the Barbados (Letters Patent Consolidation) Order 1964(b); and  
the other powers referred to in that proviso shall be exercised by the Governor acting in  
accordance with the advice of the Premier.

4. Save where the context otherwise requires, expressions used in sections 1 to 12 of this  
Order have the same meaning as in the Constitution and the provisions of section 117 of the  
Constitution shall apply for the purposes of interpreting those sections as they apply for the  
purposes of interpreting those sections as they apply for the purposes of interpreting the  
Constitution.
Revocations and Amendments
</excerpt>

# Example 3
## Question
According to Stats Canada, which three categories regarding timber assets in Quebec (by area in hectares) saw the largest raw growth from 1961 to 1962?

## Expected answer
Fire, Regeneration, Non-reserved Accessible Closing Stock

## Grade 0.00

## Search 1 — query: "Statistics Canada timber assets Quebec 1961 1962 area hectares growth categories"
### Rank 1 of 231 — 0.07 (passed on)
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
### Rank 2 of 231 — 0.06
<excerpt title="The State of Canada's Forests ANNUAL REPORT 2023">
## [PDF page 95]
Pulp and paper products  334,480,786  Pulp and paper products  346,157,598  
Wood-fabricated materials  646,499,605  Wood-fabricated materials  390,120,109  
Total value of domestic exports  985,104,724  Total value of domestic exports  737,871,029  
Value of imports (dollars, 2022)  Value of imports (dollars, 2022)  
Primary wood products  6,043,813  Primary wood products  7,824,136  
Pulp and paper products  80,659,606  Pulp and paper products  606,038,641  
Wood-fabricated materials  43,278,023  Wood-fabricated materials  211,365,356  
Total value of imports  129,981,442  Total value of imports  825,228,133
Annual Report 2023 | 89

## [PDF page 96]
Ontario  Québec  
Population (January 2022)  15,262,660  Population (January 2022)  8,751,352  
Arboreal emblem  Eastern white pine  Arboreal emblem  Yellow birch  
Disturbance  Disturbance  
Insects (hectares, 2021)     Insects (hectares, 2021)  
Area defoliated by insects and  Area defoliated by insects and  
containing beetle-killed trees  3,510,908  containing beetle-killed trees  2,463,419  
Fire (2022)  Fire (2022)  
Area burned (hectares)  2,561Area burned (hectares)  29,638  
Number of fires  275Number of fires  449  
Forest management  Forest management  
Harvesting (2021)  Harvesting (2021)  
Area harvested (hectares)  119,506  Area harvested (hectares)  215,592  
Volume harvested (cubic metres)  14,172,503  Volume harvested (cubic metres)  28,438,705  
Regeneration (hectares, 2021)  Regeneration (hectares, 2021)  
Area planted  59,508Area planted  69,268  
Area seeded  8,095Area seeded  16  
Third-party certification (hectares, 2022)   Third-party certification (hectares, 2022)  
Area certified  27,566,149Area certified  42,964,184  
Domestic economic impact  Domestic economic impact  
Housing starts (number, 2022)  96,080  Housing starts (number, 2022)  57,107
</excerpt>
### Rank 3 of 231 — 0.04
<excerpt title="Timber trends and prospects for North America">
## United States harvest trends
**Region****Softwood****Hardwood****Total**  
**Atlantic provinces**  
Potential net growth 12.3 6.6 18.9  
Removals 12.5 1.8 14.3  
**Quebec and Ontario**  
Potential net growth 52.8 23.6 76.4  
Removals 52.7 10.9 63.6  
**Total eastern Canada**  
Potential net growth 65.1 30.2 95.3  
Removals 65.2 12.7 77.9  
**Prairie provinces**  
Potential net growth-0.7-4.9-5.1  
Removals 12.3 1.4 13.7  
**British Columbia**  
Potential net growth 92.2 5.3 97.5  
Removals 76.9*76.9  
**Northwest Territories**  
Potential net growth 4.6 1.8 6.4  
Removals******  
**Total western Canada**  
Potential net growth 96.6 2.2 98.8  
Removals 89.2 1.4 90.6  
**Total Canada**  
Potential net growth 161.7 32.4 194.1  
Removals 154.4 14.1 168.5
* Hardwood included with softwood
** Under 50 000 m³
**Oak-dominated hardwood forests in the eastern United States**

## Canadian harvest trends
Total Canadian roundwood production rose from about 93 million m³ in 1960 to about 169 million m³ by 1985. The largest production increases have been registered in western Canada; the harvest in British Columbia and in the prairie provinces virtually doubled over the period. A breakdown of total removals between softwood and hardwood is only available from 1970 but, since then, softwood production has remained at about 91 percent of the total.
**Major factors affecting future Canadian supplies**
In contrast to the United States, Canadian forests are still heavily weighted toward old-growth natural forest. The estimated volumes of mature and overmature timber are theoretically sufficient to maintain current average harvest rates for many decades, or at least to permit continued expansion of the harvest in the short term. Unfortunately, this largely physical assessment gives a somewhat unrealistic perspective on timber supply potential. There are wide variations in the quality and condition of the resource and there is limited accessibility and difficult terrain in many regions. In addition, other competing uses for the land base and growing stock as well as the environmental sensitivity of certain areas may limit harvesting operations, although these areas may not be formally reserved for other uses.
A second important factor is that each provincial forest management agency bases its harvesting policies on an independent assessment of the potential of its resource to support continuous commercial harvesting. These assessments attempt to incorporate the economic as well as the long-term physical limitations of the resource in establishing an Annual Allowable Cut (AAC). This has significant implications for the speed with which the current mature and overmature inventory can be depleted.
**Future prospects for Canadian timber supplies: provincial analyses**
</excerpt>
### Rank 4 of 231 — 0.03
<excerpt title="The State of Canada's Forests ANNUAL REPORT 2023">
## [PDF page 96]
Ontario  Québec  
Population (January 2022)  15,262,660  Population (January 2022)  8,751,352  
Arboreal emblem  Eastern white pine  Arboreal emblem  Yellow birch  
Disturbance  Disturbance  
Insects (hectares, 2021)     Insects (hectares, 2021)  
Area defoliated by insects and  Area defoliated by insects and  
containing beetle-killed trees  3,510,908  containing beetle-killed trees  2,463,419  
Fire (2022)  Fire (2022)  
Area burned (hectares)  2,561Area burned (hectares)  29,638  
Number of fires  275Number of fires  449  
Forest management  Forest management  
Harvesting (2021)  Harvesting (2021)  
Area harvested (hectares)  119,506  Area harvested (hectares)  215,592  
Volume harvested (cubic metres)  14,172,503  Volume harvested (cubic metres)  28,438,705  
Regeneration (hectares, 2021)  Regeneration (hectares, 2021)  
Area planted  59,508Area planted  69,268  
Area seeded  8,095Area seeded  16  
Third-party certification (hectares, 2022)   Third-party certification (hectares, 2022)  
Area certified  27,566,149Area certified  42,964,184  
Domestic economic impact  Domestic economic impact  
Housing starts (number, 2022)  96,080  Housing starts (number, 2022)  57,107
</excerpt>
### Rank 5 of 231 — 0.03
<excerpt title="Timber trends and prospects for North America">
## United States harvest trends
Timber sale offerings from public lands are usually determined by institutional constraints rather than by the market. As a general rule, these institutional constraints are aimed at a sustained volume of timber output. On this basis, harvests from national forest lands may gradually increase over time. However, there is a degree of uncertainty in this forecast. In both the west and the south, these lands provide habitats for a number of animal species considered to be threatened or endangered. Timber management activities must be altered to ensure conservation of these species' habitats and this may have the effect of reducing timber available for sale.
**Future prospects for United States timber supplies**
Given the constraints on supplies from public lands, any increases in harvests up to 2005 must almost certainly come from private lands. In the east, the timber inventories on private ownerships have been growing for decades, and there is volume available to respond to demand increases. In the west, the old-growth inventories on private ownerships are being rapidly depleted, and by 2000 they will be largely gone. After 2010, plantations initiated in the past ten years will reach merchantable size in the south and the Pacific northwest. Given the level of planting and forest management in the past decade, there is every reason to be optimistic about the long-term timber supply. In the interim, high demand could create opportunities for a more intensive use of hardwoods. It could also create trade opportunities for other suppliers such as Canada.
**TABLE 2. Canada's potential net annual growth and removal balances, by region in 1985 (million m³)**

## United States harvest trends
**Region****Softwood****Hardwood****Total**  
**Atlantic provinces**  
Potential net growth 12.3 6.6 18.9  
Removals 12.5 1.8 14.3  
**Quebec and Ontario**  
Potential net growth 52.8 23.6 76.4  
Removals 52.7 10.9 63.6  
**Total eastern Canada**  
Potential net growth 65.1 30.2 95.3  
Removals 65.2 12.7 77.9  
**Prairie provinces**  
Potential net growth-0.7-4.9-5.1  
Removals 12.3 1.4 13.7  
**British Columbia**  
Potential net growth 92.2 5.3 97.5  
Removals 76.9*76.9  
**Northwest Territories**  
Potential net growth 4.6 1.8 6.4  
Removals******  
**Total western Canada**  
Potential net growth 96.6 2.2 98.8  
Removals 89.2 1.4 90.6  
**Total Canada**  
Potential net growth 161.7 32.4 194.1  
Removals 154.4 14.1 168.5
* Hardwood included with softwood
** Under 50 000 m³
**Oak-dominated hardwood forests in the eastern United States**
</excerpt>

## Search 2 — query: "Table 38-10-0106-01 Quebec timber assets area 1961 1962"
### Rank 1 of 2 — 0.26 (passed on)
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
### Rank 2 of 2 — 0.02
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

## Search 3 — query: "3810010601 csv"
### Rank 1 of 36 — 0.03 (passed on)
<excerpt title="What's a CSV file? - Sage Intacct">
A CSV (comma-separated values) file is a plain text file that stores tabular data, such as numbers and text. Each line in the file represents one data record, and each record consists of the same number of fields separated by commas. For example, a CSV file might contain a list of customers with their names, email addresses, and phone numbers.
Here’s an example of the content in a CSV file:
Copy
Content in a CSV file
`Name,Email Address,Phone NumberJohn Doe,johndoe@example.com,123-456-7890Jane Smith,janesmith@example.com,987-654-3210`
Microsoft Excel is a spreadsheet program that can be used to open, edit, and create CSV files. When you open a CSV file in Excel, the data is automatically formatted into a table with rows and columns. You can then use Excel features to analyze and manipulate the data.
The image below shows the difference between what a CSV files looks like in Excel, and what a CSV file looks like when opened with a text editor.
1.   An Intacct CSV file opened in Excel.

2.   The same Intacct CSV file opened in a text editor.
The extra commas shown in this image are present because there are blank fields in the file. A comma in a CSV file represents a blank cell in Excel.
</excerpt>
### Rank 2 of 36 — 0.02
<excerpt title="CSV (Comma-Separated Values) Files | PhoenixAI Glossary">
## What Are CSV (Comma-Separated Values) Files
### Understanding the CSV Format
CSV (comma-separated values) files serve as a simple method for storing data. Each CSV file contains records separated by line breaks. Commas separate the fields within each record. This structure makes CSV files easy to read and write. Users can open CSV files in text editors or spreadsheet applications like Excel. Excel handles CSV files efficiently, allowing users to manipulate data with ease. The CSV format supports data exchange between different systems. Users often choose CSV files for their compatibility and simplicity.

## What Are CSV (Comma-Separated Values) Files
### Understanding the CSV Format
#### Common Use Cases
CSV files are plain-text files that find use in various industries. Financial services frequently use CSV files to import and export data. Organizations rely on CSV files for data analysis and reporting. Users can export a CSV file from Excel to share data with others. CSV files are also popular for managing large datasets. The CSV format allows users to handle data without complex software. Users can create CSV files in Google Sheets and other applications. The CSV file extension is ".csv," indicating its format. Users can easily find the CSV file they need by searching for this extension.

## What Are CSV (Comma-Separated Values) Files
### History and Evolution
#### Origins of CSV Files
The origins of CSV files trace back to the early 1970s. Developers created CSV files to simplify data storage and sharing. The CSV format's simplicity made it accessible to many users. CSV files became a standard for exchanging tabular data. The CSV file structure remains unchanged since its inception. Users appreciate the CSV format for its straightforward design.

## What Are CSV (Comma-Separated Values) Files
### History and Evolution
#### Evolution in Data Management
CSV files have evolved with advancements in data management. The CSV format continues to play a vital role in dataset management. Users often choose CSV files for their compatibility with various systems. Excel files can be converted into CSV files for easier data handling. Users can export a CSV file from Excel to integrate data into other applications. The CSV file unique ability to store data in a flat file format makes it versatile. Users can select CSV or TSV formats based on their needs. The CSV file reports data in a way that is easy to understand. Excel handles CSV files by providing tools for data manipulation and analysis. Users can find the CSV file in Microsoft applications for seamless integration.

## How to Create and Edit CSV Files
### Tools and Software
#### Using Spreadsheet Applications
Spreadsheet applications like Google Sheets and Microsoft Excel offer powerful tools for creating and editing CSV files. Users can easily create a CSV file by entering data into cells and exporting the document in CSV format. The process involves selecting "File" from the menu, choosing "Download," and then selecting "Comma-separated values (.csv)." This method ensures compatibility across different systems. Users can open a CSV file in these applications to view and manipulate data efficiently. The spreadsheet interface provides a user-friendly way to organize information in a tabular format.

## How to Create and Edit CSV Files
### Tools and Software
#### Text Editors and Code Editors
Text editors such as Notepad or TextEdit provide a straightforward approach to editing CSV files. Users can open a CSV file directly in these editors to make quick changes. Code editors like Visual Studio Code offer additional features for developers working with CSV files. These editors support syntax highlighting and plugins that enhance CSV file management. Users can benefit from the simplicity of text editors when dealing with smaller datasets. Code editors become essential for more complex tasks involving data manipulation.

## How to Create and Edit CSV Files
### Best Practices for Editing
#### Maintaining Data Integrity
Maintaining data integrity is crucial when working with CSV files. Users should ensure that each row in a CSV table represents a complete record. Consistent use of commas as delimiters prevents data misalignment. Users must avoid inserting extra spaces or characters that could disrupt the CSV table structure. Regularly saving changes helps prevent data loss during editing sessions. Users should always verify the accuracy of data entries before finalizing the CSV file.

## How to Create and Edit CSV Files
### Best Practices for Editing
#### Avoiding Common Mistakes
Avoiding common mistakes enhances the reliability of CSV files. Users should refrain from using special characters that may confuse the CSV file format. Quotation marks can enclose fields containing commas to maintain proper separation. Users should be cautious when editing CSV files in spreadsheet applications. Automatic formatting may alter data unintentionally. Users should disable features like automatic date conversion to preserve original data formats. Regularly checking the CSV file in a text editor ensures that no unintended changes occur.
</excerpt>
### Rank 3 of 36 — 0.02
<excerpt title="Comma-separated values">
From Wikipedia, the free encyclopedia
| Comma-separated values |  
| --- |  
|  |  
| Filename extension | `.csv` |  
| Internet media type | `text/csv`[[1]](https://en.wikipedia.org/wiki/Comma-separated_values#cite_note-rfc4180-1) |  
| Uniform Type Identifier(UTI) | public.comma-separated-values-text[[2]](https://en.wikipedia.org/wiki/Comma-separated_values#cite_note-appleuti-2) |  
| UTI conformation | public.delimited-values-text[[2]](https://en.wikipedia.org/wiki/Comma-separated_values#cite_note-appleuti-2) |  
| Type of format | multi-platform, serial data streams |  
| Container for | database information organized as field separated lists |  
| Standard | RFC4180 |
**Comma-separated values** (**CSV**) is a plain textdataformat for storing tabular data where the fields (values) of a record are separated by a comma as the delimiter and each record is a line (i.e. newline is the delimiter). CSV is commonly used in software that generally deals with tabular data such as a database or a spreadsheet.[[3]](https://en.wikipedia.org/wiki/Comma-separated_values#cite_note-3) Benefits cited for using CSV include simplicity of use and human readability.[[4]](https://en.wikipedia.org/wiki/Comma-separated_values#cite_note-4) CSV is a form of delimiter-separated values. A **CSV file** is a file that contains CSV-formatted data.
CSV is not limited to a particular character encoding[[1]](https://en.wikipedia.org/wiki/Comma-separated_values#cite_note-rfc4180-1) but should be and is commonly used with UTF-8, particularly because it does not provide a way to indicate the character encoding.

The CSV format predates personal computers by more than a decade. The IBMFortran (level H extended) compiler under OS/360 supported list-directed ("free-form") input/output, with commas between values, in 1972.[[5]](https://en.wikipedia.org/wiki/Comma-separated_values#cite_note-5) List-directed input/output was defined in FORTRAN 77, approved in 1978. List-directed input used commas or spaces for delimiters, so unquoted character strings could not contain commas or spaces.[[6]](https://en.wikipedia.org/wiki/Comma-separated_values#cite_note-6)
The term "comma-separated value" and the "CSV" abbreviation were in use by 1983.[[7]](https://en.wikipedia.org/wiki/Comma-separated_values#cite_note-7) The manual for the Osborne Executive computer, which bundled the SuperCalc spreadsheet, documents the CSV quoting convention that allows strings to contain embedded commas.[[8]](https://en.wikipedia.org/wiki/Comma-separated_values#cite_note-8)
Comma-separated value lists are easier to type (for example into punched cards) than fixed-column-aligned data, and they were less prone to producing incorrect results if a value was punched one column off from its intended location.
Comma separated files are used for the interchange of database information between machines of two different architectures. The plain-text character of CSV files largely avoids incompatibilities such as byte-order and word size. The files are largely human-readable, so it is easier to deal with them in the absence of perfect documentation or communication.[[9]](https://en.wikipedia.org/wiki/Comma-separated_values#cite_note-9)
The main standardization initiative—transforming "_de facto_ fuzzy definition" into a more precise and _de jure_ one—was in 2005, with RFC4180, defining CSV as a MIME Content Type.[[10]](https://en.wikipedia.org/wiki/Comma-separated_values#cite_note-10) Later, in 2013, some of RFC 4180's deficiencies were tackled by a W3C recommendation.[[11]](https://en.wikipedia.org/wiki/Comma-separated_values#cite_note-11)
</excerpt>
### Rank 4 of 36 — 0.02
<excerpt title="Comma-separated values">
The CSV format predates personal computers by more than a decade. The IBMFortran (level H extended) compiler under OS/360 supported list-directed ("free-form") input/output, with commas between values, in 1972.[[5]](https://en.wikipedia.org/wiki/Comma-separated_values#cite_note-5) List-directed input/output was defined in FORTRAN 77, approved in 1978. List-directed input used commas or spaces for delimiters, so unquoted character strings could not contain commas or spaces.[[6]](https://en.wikipedia.org/wiki/Comma-separated_values#cite_note-6)
The term "comma-separated value" and the "CSV" abbreviation were in use by 1983.[[7]](https://en.wikipedia.org/wiki/Comma-separated_values#cite_note-7) The manual for the Osborne Executive computer, which bundled the SuperCalc spreadsheet, documents the CSV quoting convention that allows strings to contain embedded commas.[[8]](https://en.wikipedia.org/wiki/Comma-separated_values#cite_note-8)
Comma-separated value lists are easier to type (for example into punched cards) than fixed-column-aligned data, and they were less prone to producing incorrect results if a value was punched one column off from its intended location.
Comma separated files are used for the interchange of database information between machines of two different architectures. The plain-text character of CSV files largely avoids incompatibilities such as byte-order and word size. The files are largely human-readable, so it is easier to deal with them in the absence of perfect documentation or communication.[[9]](https://en.wikipedia.org/wiki/Comma-separated_values#cite_note-9)
The main standardization initiative—transforming "_de facto_ fuzzy definition" into a more precise and _de jure_ one—was in 2005, with RFC4180, defining CSV as a MIME Content Type.[[10]](https://en.wikipedia.org/wiki/Comma-separated_values#cite_note-10) Later, in 2013, some of RFC 4180's deficiencies were tackled by a W3C recommendation.[[11]](https://en.wikipedia.org/wiki/Comma-separated_values#cite_note-11)
</excerpt>
### Rank 5 of 36 — 0.02
<excerpt title="How to open a CSV-File - Circula Help Center">
# How to open a CSV-File | Circula Help Center
Skip to main content
Circula Home Page
English
Circula Home Page
English
Search for articles...
1.   All Collections   
2.   💶 Expenses & Travel Expenses   
3.   📤 Export Expenses   
4.   🧾 Expense Export   
5.   How to open a CSV-File

# How to open a CSV-File
How to open a CSV export file correctly
Written by Özge E.
May 26, 2026
Table of contents
What is a CSV file?Downloading a CSV-Export in Circula1. Via the "Reports" tab2. Via the "Approve & Control" tabHow to open a CSV-File in ExcelHow to open a CSV-File in Google SheetsDo you still have questions?
**At a glance**
*   A CSV file is mainly used when merging large amounts of data.   
*   CSV files can be opened with tools such as Excel or Google Sheets.
* * *

# What is a CSV file?
A CSV (comma-separated-values) file is a text file with a specific format that can be used to save data in tables. The extension of the file name is .**csv**. This format is mainly used because it can easily merge text formats into large amounts of data.
* * *

# Downloading a CSV-Export in Circula
**Note**
*   Not only users with the role of accountant can download CSV files on Circula. Users can also download their own expenses as CSV files. You can find more information about the CSV report for users here.   
*   Users with the role of an accountant, have various options for downloading a CSV file.
**Important**
*   This article refers to the downloading of CSV files by users with the role of accountant.

# Downloading a CSV-Export in Circula
## 1. Via the "Reports" tab
1.   Go to the "**_Reports_**" tab in your Circula app.   _Reports in the web app_    
2.   Click on the three dots in the column of the report that you would like to download as a CSV file and click on "**_Export as CSV_**".   _Exporting as CSV_    
3.   Now you can open the CSV file on your computer.

# Downloading a CSV-Export in Circula
## 2. Via the "Approve & Control" tab
1.   Go to the "**_Approve & Control_**" tab in your Circula app and then click on "**_All_**". You will see a list with all expenses.   _Approve & Control in the web app_    
2.   Either click on the small arrow next to "Submitter" and select all expenses, or manually click on the expenses you want to export.   _Selected expenses in the web app_    
3.   Click on the "Download as CSV" to download your CSV file.   _Downloading the CSV file_    
4.   Now you can open the CSV file on your computer.
* * *

# How to open a CSV-File in Excel
1.   Open your Microsoft Excel and click on "**_Data_**" in the menu bar.   
2.   Now click on "**_Get data_**" on the far left and choose "**_Import data_**" from the drop-down menu.   
3.   A new window will open, where you can choose the data source, click on "**_Text/CSV_**".   
4.   Select the export file and click on "**_Next_**".   
5.   Your default settings should already be set correctly for the CSV format. However, if they are not, please adjust them as follows:
*   File origin: 60051: Unicode (UTF-8)   
*   Delimiter: Semicolon   
*   Data type detection: Based on the first 200 rows
6. Now please click on "**_Load_**" in the lower right corner.

7. Your CSV file should now open in the correct format and be readable.
* * *
</excerpt>

## Search 4 — query: "Timber assets area Quebec 1961 1962 1961 commercial timber assets Quebec"
### Rank 1 of 1721 — 0.11 (passed on)
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
### Rank 2 of 1721 — 0.10
<excerpt title="Quebec's Forest Regimes: Lessons for a Return to Prosperity">
## [PDF page 13]
inequitably.11  The criticisms expressed by the Department, to the ef-  
fect that concession holders were under-utilizing the  
The gover nment also criticized concession holders on  trees in public forests, led to the publication of a White  
the grounds that they only harvested the species they  Paper in the early 1970s. In this document, the gover n-  
needed without even selling so-called “secondary” spe-  ment revealed its intention to revoke all forest conces-  
cies like deciduous trees to third parties that could have  sions and to take over more responsibility itself in order  
used them to supply sawmills.12 According to the Depart-  to maximize the harvest of public forests. This was a de-  
ment, this exclusive right covering all tree species did  cisive moment in the gover nance of the public forests  
not allow for the growing needs of this industry to be  that reﬂ ected the vision of the role of gover nment that  
met.  prevailed at the time.
10.  Roland Royer, “Pourquoi abolir les concessions forestières?” Presentation by  
the Chief Forester of Consolidated Bathurst Limited at the meeting of the  13.  Roland Royer, op. cit., footnote 10, pp. 7 and 17.  
Association forestière québécoise, December 27, 1972, pp. 6-7.  14.  Bureau du forestier en chef, Le portrait de la forêt feuillue et mixte à feuillus  
11.  Quebec Department of Lands and Forests, op. cit., footnote 2, p. 38.durs au Québec : Survol historique, January 2015, pp. 30-36.  
12.  Ibid., pp. 30-33.  15.  Ibid., p. 44.
Montreal Economic Institute  11

## [PDF page 14]
Quebec’s Forest Regimes: Lessons for a Retur n to Prosperity
Figure 1-2
Evolution of forestry area in the province, by kind of tenure, 1961-1985
350,000
300,000
250,000
200,000
150,000
100,000
50,000
0
Forest concessions  Public forest reserves
Source: Michel Duchesneau, Gestion de la forêt publique et modes d’allocation de la matière ligneuse avant 1986, Report prepared for the Commission for the Study of  
Public Forest Management in Quebec, May 2004, p. 11.
</excerpt>
### Rank 3 of 1721 — 0.08
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
### Rank 4 of 1721 — 0.07
<excerpt title="Quebec's Forest Regimes: Lessons for a Return to Prosperity">
## [PDF page 14]
Quebec’s Forest Regimes: Lessons for a Retur n to Prosperity
Figure 1-2
Evolution of forestry area in the province, by kind of tenure, 1961-1985
350,000
300,000
250,000
200,000
150,000
100,000
50,000
0
Forest concessions  Public forest reserves
Source: Michel Duchesneau, Gestion de la forêt publique et modes d’allocation de la matière ligneuse avant 1986, Report prepared for the Commission for the Study of  
Public Forest Management in Quebec, May 2004, p. 11.

## [PDF page 14]
Paradoxically, the Quebec Minister of Lands and Forests  
“The gover nment declared in the early  had proposed the creation of a Forest Management  
1960s that the exclusive logging rights  Company on the grounds that the gover nment had a  
did not allow for the public forests to  reputation as a bad manager. He had even highlighted  
the “disappointing experience with departmental ad-  
be harvested to their full potential.”  ministration of the public forest reserves [‘forêts do-  
maniales’] and the weight of gover nmental administration”  
In particular, the Department stated that “in an era of  all while admitting that the Department “had behaved  
command economies and of planning, it is much more  like the least efﬁ cient of the concession holders, and  
efﬁ cient to proceed, in the granting of forest conces-  was not meeting the conditions that it required of  
sions, according to particular laws, with conditions de-  them.”18 At the same time, the Department declared  
ter mined by the legislature.”16 From this perspective,  that a “concer n for realism and efﬁ ciency” encouraged  
the Department considered it altogether natural for the  the gover nment to preserve for a time the participation  
gover nment to want to take over the management of  of private enterprise to take advantage of its experience  
the forests that belong to it.17 The emergence of this  and of the skills acquired by the holders of forest con-  
new paradigm left marks that can still be seen.  cessions.19 Disregarding the positive elements inherent
18.  Speech by the Minister of Lands and Forests, cited in Roland Royer, op. cit.,  
16.  Ibid.  footnote 10, p. 10.  
17.  Quebec Department of Lands and Forests, Exposé sur la politique  19.  Quebec Department of Lands and Forests, Exposé sur la politique  
forestière : Tome 2—Réforme et programme d’action, 1972, pp. 32-33.  forestière : Tome 1—Prospective et problématique, 1971, p. 155.
12  Montreal Economic Institute
</excerpt>
### Rank 5 of 1721 — 0.05
<excerpt title="Le travailleur forestier québécois">
## [PDF page 291]
La technologie et la modernisation  : la rationalité économique  2
Mécanisation de l’opération de débusquage  
Chevaux
Année  Provinces de  Débusqueuses  
d’activité  Ontario  Québec  l’Atlantique  Total  Québec  
1959  300  6 402  1 437  8 139  24  
1960  288  5 935  1 245  7 469  62  
1961  226  5 329  1 125  6 680  115  
1962  203  4 476  895  5 574  165  
1963  227  3 381  808  4 416  453  
1964  82  2 894  500  3 476  1 003  
1965  60  2 137  250  2 447  2 160  
1966  15  1 569  175  1 759  2 486  
1969  -–  -–  -–  -–  3 550  
1971  -–  -–  -–  -–  3 709
Sources  :  D.R.  Campbell  et  Edward  B.  Power,  1966.  
J.R.  Hughes,  1970,  p.  233-238.

## [PDF page 291]
prédire  avec  précision  et  de  contrôler  les  résultats  de  leurs  activités  
de  production  à  la  suite  de  l’incertitude  créée  par  les  variations  
considérables rencontrées dans la matière première (densité et nature  
des peuplements et autres éléments liés à la foresterie), les désastres  
écologiques  (feux  de  forêt,  épidémies),  l’environnement  physique  
(conditions  climatiques,  topographie,  facilité  d’accès,  distances)  et  
l’environnement  socioéconomique  (marché  de  la  main-d’œuvre  et  
d e s  p r o d u i t s ,  m a r c h é  d e s  é q u i p e m e n t s ,  e t c . )6.  L’ e x i s t e n c e  d e  c e s  
conditions  et  l’impossibilité  d’en  modifier  complètement  la  nature
6.  Par  opposition,  l’environnement  industriel  créé  dans  une  usine  de  pâtes  et  
papiers est un environnement artificiel dont la nature et les caractéristiques ont  
été soigneusement planifiées et sont contrôlées de manière à assurer le fonction-  
nement  le  plus  rationnel  et  le  plus  efficace  possible  du  système  de  production.
©  2005  –  Presses  de  l’Université  du  Québec  
Édifice  Le  Delta  I,  2875,  boul.  Laurier,  bureau  450,  Sainte-Foy,  Québec  G1V  2M2  • Tél. :  (418)  657-4399  –  www.puq.ca
</excerpt>

## Search 5 — query: "38100106-eng.zip"
### Rank 1 of 1296 — 0.19 (passed on)
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
### Rank 2 of 1296 — 0.14
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
### Rank 3 of 1296 — 0.07
<excerpt title="業績">
2023 WJOG9416L DRAGON Thoracic Docetaxel Plus Ramucirumab With Primary Prophylactic Pegylated Granulocyte-Colony Stimulating Factor Support for Elderly Patients With Advanced NSCLC: A Multicenter Prospective Single Arm Phase 2 Trial: DRAGON Study (WJOG9416L)Motoko Tachihara JTO Clin Res Rep https://pubmed.ncbi.nlm.nih.gov/37822699/  
2023 WJOG8916G GI A multicenter phase II trial of trifluridine/tipiracil in combination with cetuximab rechallenge in patients with RAS wild-type metastatic colorectal cancer refractory to prior anti-EGFR antibodies： the WJOG8916G trial Naoki Izawa Target Oncol https://pubmed.ncbi.nlm.nih.gov/37148491/  
2023 WJOG5108LFS Thoracic Overall survival analysis of patients enrolled in a randomized phase III trial comparing gefitinib and erlotinib for previously treated advanced lung adenocarcinoma (WJOG5108LFS)Nobuyuki Katakami Int J Clin Oncol https://pubmed.ncbi.nlm.nih.gov/36414827/  
2023 WJOG15822G RETRIEVE GI Randomised phase II trial of trifluridine/tipiracil (FTD/TPI) plus ramucirumab (RAM)versus trifluridine/tipiracil for previously treated patients with advanced gastricor esophagogastric junction adenocarcinoma (RETRIEVE study, WJOG15822G)Naoki Takahashi BMC Cancer https://pubmed.ncbi.nlm.nih.gov/37543568/  
2023 WJOG15421L REVEAL Thoracic Biomarker Testing in Patients With Unresectable Advanced or Recurrent Non–Small Cell Lung Cancer Tomohiro Sakamoto JAMA Netw Open https://pubmed.ncbi.nlm.nih.gov/38100106/  

2023 WJOG14720L B-DASH Thoracic Randomized, open-label phase II study of brigatinib and carboplatin plus pemetrexed and brigatinib alone for chemotherapy-naive patients with ALK-rearranged non-squamous non-small cell lung cancer: treatment rationale and protocol design of the B-DASH study (WJOG 14720 L)Kazushige Wakuda BMC Cancer https://pubmed.ncbi.nlm.nih.gov/37749521/  
2023 WJOG14520G GI Trifluridine/Tipiracil Plus Bevacizumab for Vulnerable Patients With Pretreated Metastatic Colorectal Cancer: A Retrospective Study (WJOG14520G)Yosuke Kito Oncologist https://pubmed.ncbi.nlm.nih.gov/37950903/  
2023 WJOG14320B ERICA Breast Multicentre, randomised, double-blind, placebo-controlled phase II study of prophylactic olanzapine for patients with metastatic breast cancer receiving T-DXd treatment: protocol for the ERICA study (WJOG14320B)Hitomi Sakai BMJ Open https://pubmed.ncbi.nlm.nih.gov/37012013/  
2023 WJOG13119L Thoracic Significance of micro-EGFR T790M mutations on EGFR-tyrosine kinase inhibitor efficacy in non-small cell lung cancer Takeshi Masuda Sci Rep https://pubmed.ncbi.nlm.nih.gov/37957228/  
2023 WJOG12319LTR Thoracic Lack of Association of Plasma Levels of Soluble Programmed Cell Death Protein 1, Programmed Death-Ligand 1, and CTLA-4 With Survival for Stage II to IIIA NSCLC After Complete Resection and Adjuvant Chemotherapy Junko Tanizaki JTO Clin Res Rep https://pubmed.ncbi.nlm.nih.gov/38029041/
</excerpt>
### Rank 4 of 1296 — 0.05
<excerpt title="業績">
2024 WJOG11018G GI A Phase II Study of FOLFIRI Plus Ziv-Aflibercept After Trifluridine/Tipiracil Plus Bevacizumab in Patients with Metastatic Colorectal Cancer: WJOG 11018G Toshihiko Matsumoto Target Oncol https://pubmed.ncbi.nlm.nih.gov/38427280/  
2024 WJOG10417GTR GI Myeloid subsets impede the efficacy of anti-PD1 therapy in patients with advanced gastric cancer (WJOG10417GTR study)Hirokazu Shojii J Immunother Cancer https://pubmed.ncbi.nlm.nih.gov/39489543/  
2024 JCOG1404/WJOG8214L AGAIN Thoracic Randomized Phase III Study of EGFR Tyrosine Kinase Inhibitor and Intercalated Platinum-doublet Chemotherapy for Non-small Cell Lung Cancer Harboring EGFR Mutation Shintaro Kanda Clin Cancer Res https://pubmed.ncbi.nlm.nih.gov/40162917/  
2023 WJOG15221M ALLBREAK Basket First experience of a fully decentralized clinical trial: The dawn of a new era in oncology Hiroya Taniguchi Cancer Sci https://pubmed.ncbi.nlm.nih.gov/36971104/  
2023 WJOGG11619L DOLPHIN Thoracic Durvalumab Plus Concurrent Radiotherapy for Treatment of Locally Advanced Non–Small Cell Lung Cancer. The DOLPHIN Phase 2 Nonrandomized Controlled Trial.Motko Tachihara JAMA Oncol https://pubmed.ncbi.nlm.nih.gov/37676681/  
2023 WJOG9616L Thoracic Nivolumab Retreatment in Non–Small Cell Lung Cancer Patients Who Responded to Prior Immune Checkpoint Inhibitors and Had ICI-Free Intervals (WJOG9616L)Hiroaki Akamatsu Clin Cancer Res https://pubmed.ncbi.nlm.nih.gov/35762926/  

2023 WJOG9416L DRAGON Thoracic Docetaxel Plus Ramucirumab With Primary Prophylactic Pegylated Granulocyte-Colony Stimulating Factor Support for Elderly Patients With Advanced NSCLC: A Multicenter Prospective Single Arm Phase 2 Trial: DRAGON Study (WJOG9416L)Motoko Tachihara JTO Clin Res Rep https://pubmed.ncbi.nlm.nih.gov/37822699/  
2023 WJOG8916G GI A multicenter phase II trial of trifluridine/tipiracil in combination with cetuximab rechallenge in patients with RAS wild-type metastatic colorectal cancer refractory to prior anti-EGFR antibodies： the WJOG8916G trial Naoki Izawa Target Oncol https://pubmed.ncbi.nlm.nih.gov/37148491/  
2023 WJOG5108LFS Thoracic Overall survival analysis of patients enrolled in a randomized phase III trial comparing gefitinib and erlotinib for previously treated advanced lung adenocarcinoma (WJOG5108LFS)Nobuyuki Katakami Int J Clin Oncol https://pubmed.ncbi.nlm.nih.gov/36414827/  
2023 WJOG15822G RETRIEVE GI Randomised phase II trial of trifluridine/tipiracil (FTD/TPI) plus ramucirumab (RAM)versus trifluridine/tipiracil for previously treated patients with advanced gastricor esophagogastric junction adenocarcinoma (RETRIEVE study, WJOG15822G)Naoki Takahashi BMC Cancer https://pubmed.ncbi.nlm.nih.gov/37543568/  
2023 WJOG15421L REVEAL Thoracic Biomarker Testing in Patients With Unresectable Advanced or Recurrent Non–Small Cell Lung Cancer Tomohiro Sakamoto JAMA Netw Open https://pubmed.ncbi.nlm.nih.gov/38100106/
</excerpt>
### Rank 5 of 1296 — 0.05
<excerpt title="Full text of Commercial and Financial Chronicle : March 13, 1961 - FRASER">
#
40,700
-
90
90
130
16,000
28 Vt
38%
500
57%
38,100
106 Vt
106
94%
56 Vs
57%
283/4
*92 Va
29%  
93
54:
106 Va
37
,
82%
>
'
,*19%
,
840
10 Vt
9%
10
220
39,300
38
%
x82
82%
1 20
5,700
96 Vs
*94%
%
93
106
65 %
96
65 Vs  
96
*94%
.
,
28 %  
92%  
53%
28 Va
10,700  
'
•85
84
'
10%
735/8
26 Vt
253/8  
<
150
6,100  
3,300
18%
13%
104 5/8
*93  
94.%  
54  
55%  
xl06  
106  
37%  
38%
,
*109
110
*109
110
443/4  
42
" '*19%  
57 Vs
763/4
19%
46%
*
"
36%
X76%
307/a
31%
28 %
— —V
77
•
-
237/a
24%
46%
■
7,000
38 Vs
37%
38%
*109
—
50
39,100
23%
35%
47
19 Vt
19%  
47
2,800
843/s '
-
</excerpt>

## Search 6 — query: "38100106-eng.csv"
(no page could be scored)

## Search 7 — query: "https://www150.statcan.gc.ca/n1/tbl/csv/38100106-eng.csv"
### Rank 1 of 24 — 0.22 (passed on)
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
### Rank 2 of 24 — 0.16
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
### Rank 3 of 24 — 0.11
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
### Rank 4 of 24 — 0.10
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

## Search 8 — query: "38100106-eng.zip statistics canada"
### Rank 1 of 38 — 0.09 (passed on)
<excerpt title="Open Government Portal - Canada.ca">
### Organization
*   Office of the Administrator of the Ship-source Oil Pollution Fund; (operating under the name) Ship and Rail Compensation Canada
6
*   Office of the Auditor General of Canada
381
*   Office of the Commissioner of Lobbying of Canada
26
*   Office of the Commissioner of Official Languages
22
*   Office of the Information Commissioner of Canada
4
*   Office of the Intelligence Commissioner
7
*   Office of the Privacy Commissioner of Canada
51
*   Office of the Secretary to the Governor General
1
*   Office of the Superintendent of Financial Institutions Canada
37
*   Pacific Economic Development Canada
5
*   Pacific Pilotage Authority Canada
2
*   Parks Canada
599
*   Parole Board of Canada
19
*   Patented Medicine Prices Review Board Canada
17
*   Polar Knowledge Canada
3
*   Prairies Economic Development Canada
11
*   Privy Council Office
5
*   Public Health Agency of Canada
761
*   Public Prosecution Service of Canada
8
*   Public Safety Canada
14
*   Public Service Commission of Canada
134
*   Public Services and Procurement Canada
242
*   RCMP External Review Committee
2
*   Royal Canadian Mint
8
*   Royal Canadian Mounted Police
104
*   Secretariat of the National Security and Intelligence Committee of Parliamentarians
7
*   Shared Services Canada
117
*   Social Sciences and Humanities Research Council of Canada
10
*   Standards Council of Canada
12
*   Statistics Canada
10271
*   Telefilm Canada
10
*   The Correctional Investigator Canada
2
*   The National Battlefields Commission
1
*   The Seaway International Bridge Corporation
10
*   Transport Canada
49
*   Transportation Safety Board of Canada
446
*   Treasury Board of Canada Secretariat
316
*   Vancouver Fraser Port Authority
1
*   Veterans Affairs Canada
126
*   Veterans Review and Appeal Board
23
*   Western Economic Diversification Canada
18
*   Windsor-Detroit Bridge Authority
4
*   Women and Gender Equality Canada
27

### Portal Type
*   Open Data
10241
*   Open Information
30

### Collection Type
*   API
1
*   Briefing packages for Parliamentary Committee appearances for deputy heads
1
*   Geospatial
144
*   Institutional Accessibility plans
1
*   Non-Spatial
10013
*   Open Maps
83
*   Publications
27
*   Reports Tabled in Parliament
1

### Jurisdiction
*   Federal
10271
</excerpt>
### Rank 2 of 38 — 0.03
<excerpt title="Canada's national statistical agency">
# Statistics Canada: Canada's national statistical agency
*   Skip to main content  
*   Skip to footer  
*   Switch to basic HTML version

# Statistics Canada: Canada's national statistical agency
## Language selection


# Statistics Canada: Canada's national statistical agency
## WxT Language switcher
*   Français fr
/ Gouvernement du Canada

# Statistics Canada: Canada's national statistical agency
## Search and menus
*   Search and menus
Search and menus

# Statistics Canada: Canada's national statistical agency
## WxT Search form
Search Statistics Canada
Search

# Statistics Canada: Canada's national statistical agency
## WxT Search form
### Language selection
*   Français fr

# Statistics Canada: Canada's national statistical agency
## WxT Search form
### Topics menu
*   Subjects  
*   Data  
*   Analysis  
*
Reference  
    *   Reference resources  
    *   Standards, data sources and methods  
    *   Reference – Main page
*   Geography  
*
Census  
    *   Census of Population  
    *   Census of Agriculture  
    *   Census of Environment  
    *   Census engagement  
    *   Census – Main page
*
Surveys and statistical programs  
    *   Information for survey participants  
    *   Results and documentation of surveys and statistical programs  
    *   Using new and existing data for official statistics  
    *   Surveys and statistical programs – Main page
*   About StatCan  
*   Canada.ca

# Statistics Canada: Canada's national statistical agency
## WxT Search form
### About this site
*
Statistics Canada  
    *   Contact StatCan  
    *   Trust Centre
*   Contact StatCan  
*   Trust Centre  
*
Government of Canada  
    *   All contacts  
    *   Departments and agencies  
    *   About government  
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
*   All contacts  
*   Departments and agencies  
*   About government  
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
*
Government of Canada Corporate  
    *   Social media  
    *   Mobile applications  
    *   About Canada.ca  
    *   Terms and conditions  
    *   Privacy
*   Social media  
*   Mobile applications  
*   About Canada.ca  
*   Terms and conditions  
*   Privacy
Close Close overlay
× Close: Search and menus (escape key)

# Statistics Canada: Canada's national statistical agency
## WxT Search form
Search Statistics Canada
Search
</excerpt>
### Rank 3 of 38 — 0.03
<excerpt title="Open Government Portal - Canada.ca">
### Jurisdiction
*   Federal
10271

### Keywords
*   table
8277
*   business performance and ownership
1452
*   census of population
1428
*   labour
1092
*   business dynamics
1014
*   health
1014
*   economic accounts
807
*   current business conditions
666
*   agriculture and food
535
*   income pensions spending and wealth
507
*   science and technology
502
*   national accounts and gross domestic product
451
*   municipal and local data
443
*   employment and unemployment
428
*   education training and learning
407
*   financial statements and performance
406
*   population and demography
397
*   prices and price indexes
393
*   innovation and business strategy
386
*   construction
360
*   business and consumer services and culture
357
*   transportation
347
*   housing
343
*   society and community
335
*   environment
332
*   immigration and ethnocultural diversity
331
*   children and youth
310
*   earnings wages and non-wage benefits
285
*   digital economy and society
281
*   household family and personal income
278
*   government
270
*   international trade
254
*   manufacturing
245
*   crime and justice
236
*   small and medium sized business
236
*   gross domestic product by income and by expenditure accounts
230
*   producer price indexes
225
*   business and consumer services
210
*   indigenous peoples
206
*   road transportation
202
*   employment by occupation industry or sector
199
*   merchandise imports and exports
196
*   languages
194
*   health care services
169
*   postsecondary education
169
*   immigrants and non-permanent residents
167
*   diseases and physical health conditions
164
*   hours of work and work arrangements
162

### Keywords
*   Census of population
159
*   mobility and migration
150

### Subject
*   Economics and Industry
4070
*   Persons
2789
*   Health and Safety
1035
*   Labour
964
*   Society and Culture
650
*   Agriculture
554
*   Science and Technology
507
*   Government and Politics
425
*   Transport
424
*   Education and Training
416
*   Nature and Environment
351
*   Information and Communications
289
*   Law
240
*   Language and Linguistics
197
*   Processes
4
*   Form Descriptors
3

### Format
*   CSV
8464
*   DOCX
1
*   E00
3
*   ESRI REST
68
*   FGDB/GDB
68
*   GML
182
*   GeoPackage
3
*   HDF
1
*   HTML
8995
*   JSON
2
*   MXD
43
*   MapInfo
2
*   Other
232
*   PDF
71
*   SAS
7
*   SHP
195
*   TXT
16
*   WMS
66
*   XLS
9
*   XLSX
7
*   XML
9775
*   ZIP
13

### Update Frequency
*   As Needed
4810
*   Annually
2684
*   Unknown
1127
*   Monthly
869
*   Quarterly
624
*   Biannually
86
*   Weekly
30
*   Not Planned
14
*   Irregular
11
*   Daily
10
*   Continual
3
*   Every two years
1
*   Every three years
1
*   Every five years
1
</excerpt>
### Rank 4 of 38 — 0.03
<excerpt title="Canada's national statistical agency">
# Statistics Canada: Canada's national statistical agency
## WxT Search form
Search Statistics Canada
Search

# Statistics Canada: Canada's national statistical agency
## Topics menu
*   Subjects  
*   Data  
*   Analysis  
*   Reference  
    *   Reference resources  
    *   Standards, data sources and methods  
    *   Reference – Main page

*   Geography  
*   Census  
    *   Census of Population  
    *   Census of Agriculture  
    *   Census of Environment  
    *   Census engagement  
    *   Census – Main page

*   Surveys and statistical programs  
    *   Information for survey participants  
    *   Results and documentation of surveys and statistical programs  
    *   Using new and existing data for official statistics  
    *   Surveys and statistical programs – Main page

*   About StatCan  
*   Canada.ca

# Statistics Canada
Statistics Canada is the national statistical office. The agency ensures Canadians have the key information on Canada's economy, society and environment that they require to function effectively as citizens and decision makers.
Read the news in _The Daily_
Sign in to My StatCan
Sign in to My StatCan
* * *
* * *

# Statistics Canada
## Key indicators
Quarterly population estimate(*)
41,798,407
0.2%
July 1, 2026
(period-to-period change)
Consumer Price Index
3.1%
October 2026
(12-month change)
Unemployment rate
6.7%
0.2 pts
October 2026
(monthly change)
Real GDP by expenditure
0.8%
Second quarter 2026
(quarterly change)
More: Key indicators

# Statistics Canada
## Most requested
*   List of surveys in collection  
*   Major economic indicators  
*   Quality of Life Hub  
*   Juristat  
*   Health Reports  
*   Census of Population Profile, 2021  
*   North American Industry Classification System (NAICS) Canada 2022 Version 1.0  
*   Fill out a survey

# Statistics Canada
## Notifications
**Notice:** Some sections of the Statistics Canada website will be unavailable on Saturday, November 21, 2026 between 7:00 a.m. and 12:00 p.m. and on Monday, November 23, 2026 between 4:00 p.m. and 4:30 p.m. (Eastern time) due to maintenance. We apologize for any inconvenience.

# Statistics Canada
## Services and information
### Subjects and data hubs
Consult our list of subjects and data hubs to find related data, analysis and reference resources.

# Statistics Canada
## Services and information
### Data
Find the data you are looking for, such as data tables, microdata and data visualizations, on a wide range of subjects.

# Statistics Canada
## Services and information
### Analysis
Take a look at our latest publications and articles that analyze the results of our surveys.

# Statistics Canada
## Services and information
### Reference
Consult our documentation to help you understand and interpret our surveys and data.

# Statistics Canada
## Services and information
### Geography
Take a look at our maps to find data, analysis and reference resources for a specific region or area.

# Statistics Canada
## Services and information
### Census
Discover the story of our country and its people using census data collected every five years.

# Statistics Canada
## Services and information
### Surveys and statistical programs
Find everything you need to know about a specific survey or a statistical program.

# Statistics Canada
## Services and information
### Customized products and services
Statistics Canada offers a variety of customized products and services serving clients in Canada and around the world.

# Statistics Canada
## Services and information
### Events and training
Register and attend our workshops, conferences and training that are organized in many Canadian cities.

# Statistics Canada
## Contact us
*   Contact Statistics Canada
</excerpt>
### Rank 5 of 38 — 0.02
<excerpt title="Postal Code Conversion File [Canada], March 2025, Census of Canada 2021">
# Postal Code Conversion File [Canada], March 2025, Census of Canada 2021
|  |  PCCF_FCCP_202503-eng.pdf Documentation/Adobe PDF - 567.1 KB Published Mar 18, 2025 1,140 Downloads MD5: 2f1...f34 Data Documentation - Reference Guide Data | Preview "Documentation/PCCF_FCCP_202503-eng.pdf"Access File * File Access * Public * Download Options * Adobe PDF * Download Metadata * Data File Citation * Download EndNote XML * Download RIS * Download BibTeX |  
|  | PCCF_FCCP_V2503_2021_sav.zip SPSS/ZIP Archive - 33.8 MB Published Mar 18, 2025 108 Downloads MD5: 14f...76c Access granted only to Odesi and DLI subscribers Data | Access File * File Access * Restricted * Users may not request access to files. * Download Metadata * Data File Citation * Download EndNote XML * Download RIS * Download BibTeX |  
|  | PCCF_retired_FCCP_retraite_V2503_2021_sav.zip SPSS/ZIP Archive - 2.1 MB Published Mar 18, 2025 98 Downloads MD5: 8d1...643 Access granted only to Odesi and DLI subscribers Data | Access File * File Access * Restricted * Users may not request access to files. * Download Metadata * Data File Citation * Download EndNote XML * Download RIS * Download BibTeX |  
|  | PCCF_FCCP_V2503_2021.txt TXT/Plain Text - 286.7 MB Published Mar 18, 2025 129 Downloads MD5: 5d5...98d Access granted only to Odesi and DLI subscribers Data | Access File * File Access * Restricted * Users may not request access to files. * Download Metadata * Data File Citation * Download EndNote XML * Download RIS * Download BibTeX |  

# Postal Code Conversion File [Canada], March 2025, Census of Canada 2021
|  | PCCF_retired_FCCP_retraite_V2503_2021.txt TXT/Plain Text - 14.9 MB Published Mar 18, 2025 98 Downloads MD5: 436...a5a Access granted only to Odesi and DLI subscribers Data | Access File * File Access * Restricted * Users may not request access to files. * Download Metadata * Data File Citation * Download EndNote XML * Download RIS * Download BibTeX |
Export Metadata
*   DataCite  
*   Schema.org JSON-LD  
*   DDI Codebook v2  
*   OAI_ORE  
*   DDI PDF Codebook  
*   OpenAIRE  
*   Croissant  
*   Dublin Core  
*   DDI HTML Codebook  
*   JSON
Citation Metadata
| Persistent Identifier | doi:10.5683/SP3/OHYOJV |  
| --- |  
| Publication Date | 2025-03-18 |  
| Title | Postal Code Conversion File [Canada], March 2025, Census of Canada 2021 |  
| Subtitle | Postal Code Conversion File, March 2025, Census of Canada 2021 |  
| Alternative Title | PCCF March 2025 |  
| Author | Statistics Canada. Geography Division |  
| Point of Contact | Use email button above to contact. Odesi Service |
</excerpt>

## Search 9 — query: "https://www150.statcan.gc.ca/n1/tbl/csv/38100106-eng.zip"
### Rank 1 of 19 — 0.05 (passed on)
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
### Rank 2 of 19 — 0.04
<excerpt title="Full Table Download (CSV) User Guide">
## Table of contents
Table of contents
*   Revision History  
*   Purpose  
*   Objectives/Requirements  
*   General Information  
*   Data File (non-Census cubes)  
    *   Data File Record Layout (non-Census cubes)

*   Metadata File (non-Census cubes)  
    *   Metadata File Record Layout (non-Census cubes)

*   Data File (Census of Population cubes: 98-XXXX-XX)  
    *   Transposition  
    *   Record Layout  
    *   Data File Record Layout (Census of Population cubes: 98-XXXX-XX)

*   Metadata File (Census of Population cubes: 98-XXXX-XX)  
    *   Metadata File Record Layout (Census of Population cubes: 98-XXXX-XX)

*   Appendices  
    *   Appendix A - Frequency  
    *   Appendix B - Units of Measure  
    *   Appendix C - Scalar Factors

## Revision History
Revision History
| Date | Version | Description | Author |  
| --- | --- | --- | --- |  
| December 2017 | 1.0 | User Guide | Dissemination Division |  
| April 2018 | 1.1 | Edits | Dissemination Division |  
| April 2022 | 2.0 | Updated Guide | Dissemination Division/Census |

## Purpose
The purpose of this document is to provide users with a guide to the full table downloadable output files available from the Statistics Canada website.

## Objectives/Requirements
The general requirements for the full table download are
*   Users can access and download an entire updated data table in CSV (.csv) format from Statistics Canada's website, via a download options button.  
*   Updated data is available at 8:30am on release day  
*   Users receive all data and relevant metadata.

## General Information
*   Download files are unilingual; there is a separate English and French version for each table.  
*   Previously used CANSIM table numbers have been replaced by numeric Product Identification codes, called PIDs. Each table has a unique PID.  
*   English downloads are in CSV format and use commas as the separator. French downloads are also in CSV format but use semi-colons as the separator. This is by design to accommodate the decimal display standard in French, which uses a comma (,) instead of the period (.) used in English.  
*   Data is 'bundled' in a .zip format containing 2 .csv files; a data file containing both data and textual 'stub' information, and a corresponding metadata file. Users receive both on download.  
*   The .zip filename has the format 'PID-eng.zip' in English and 'PID-fra.zip' in French. The filenames for the data and metadata files have the structures "PID.csv and PID_Metadata.csv', in both English and French.  
*   Some information (i.e. dimension names, member names) appears in both the data and metadata file. This redundancy is by design. It accommodates the advanced user who requires the ability to sort and filter on the data, and it also allows the novice user to understand the information being presented through the presence of basic descriptions.  
*   For 2021 Census cubes (98-XXXX-XX) there have been changes introduced in both the metadata and data files, which makes the record layouts for both files different than non-Census cubes.These differences have been described in this document.
</excerpt>
### Rank 3 of 19 — 0.04
<excerpt title="Statistics Canada Data Tables">
Repository details
*   General  
*   Institutions  
*   Terms  
*   Standards
Name of repository
**Statistics Canada Data Tables**
Additional name(s)
*    formerly: CANSIM   
*    Statistics Canada’s main socioeconomic time series database   
*    Statcan Data Tables   
*    formerly: Canadian Socio-economic Information Management System
Repository URL
Subject(s)
*   [Humanities and Social Sciences](https://www.re3data.org/search?subjects[]=1 "Search with subject 'Humanities and Social Sciences'")  
*   [Social Sciences](https://www.re3data.org/search?subjects[]=123 "Search with subject 'Social Sciences'")  
*   [Empirical Social Research](https://www.re3data.org/search?subjects[]=12302 "Search with subject 'Empirical Social Research'")  
*   [Statistics and Econometrics](https://www.re3data.org/search?subjects[]=12406 "Search with subject 'Statistics and Econometrics'")  
*   [Social and Behavioural Sciences](https://www.re3data.org/search?subjects[]=12 "Search with subject 'Social and Behavioural Sciences'")  
*   [Economics](https://www.re3data.org/search?subjects[]=124 "Search with subject 'Economics'")
Description
CANSIM is Statistics Canada's key socioeconomic database. Updated daily, CANSIM provides fast and easy access to a large range of the latest statistics available in Canada. Before June 2018, the Data Tables collection was called CANSIM. That name was retired, but the content is still available. CANSIM tables have been given new numbers, but you can still search the Data Tables using the old CANSIM table and vector numbers (or use this Concordance to look up the new table number).
Repository type(s)
*    institutional
Mission statement for designated community
Research data repository language(s)
*    English   
*    French
Data and/or service provider
*    dataProvider

## Institutions (1)
Institution name
Additional name(s)
*    Gouvernement du Canada, Statistique Canada
Country
Type(s) of responsibility
*    general   
*    technical
Type of institution
non-profit

## Policies (4)
Policy name
Policy name
Policy name
Policy name

## Database access
Type of access to research data repository
open

## Data access (1)
Type of access to data
open

## Data licenses (2)
Data license
Data license

## Data upload (1)
Type of data upload
restricted
Data upload restriction type(s)
*    other
Persistent identifier system(s)
*    none
Versioning
yes
Data citation guideline
Enhanced publication
yes

## Remarks
Remarks
Other resources to help you find Statistics Canada data and information (https://www.statcan.gc.ca/en/about/statcan): Summary tables, Census Profile, Census Data, Canadian International Merchandise Trade Database, NHS Profile, National Household Survey Data
Entry date
2016-06-21
Last update
2024-05-22

## Remarks
#### Cite this re3data.org record:
re3data.org: Statistics Canada Data Tables; editing status 2024-05-22; re3data.org - Registry of Research Data Repositories. https://doi.org/10.17616/R3NH17 last accessed: 2026-11-18
</excerpt>
### Rank 4 of 19 — 0.03
<excerpt title="Canada's national statistical agency">
# Statistics Canada: Canada's national statistical agency
*   Skip to main content  
*   Skip to footer  
*   Switch to basic HTML version

# Statistics Canada: Canada's national statistical agency
## Language selection


# Statistics Canada: Canada's national statistical agency
## WxT Language switcher
*   Français fr
/ Gouvernement du Canada

# Statistics Canada: Canada's national statistical agency
## Search and menus
*   Search and menus
Search and menus

# Statistics Canada: Canada's national statistical agency
## WxT Search form
Search Statistics Canada
Search

# Statistics Canada: Canada's national statistical agency
## WxT Search form
### Language selection
*   Français fr

# Statistics Canada: Canada's national statistical agency
## WxT Search form
### Topics menu
*   Subjects  
*   Data  
*   Analysis  
*
Reference  
    *   Reference resources  
    *   Standards, data sources and methods  
    *   Reference – Main page
*   Geography  
*
Census  
    *   Census of Population  
    *   Census of Agriculture  
    *   Census of Environment  
    *   Census engagement  
    *   Census – Main page
*
Surveys and statistical programs  
    *   Information for survey participants  
    *   Results and documentation of surveys and statistical programs  
    *   Using new and existing data for official statistics  
    *   Surveys and statistical programs – Main page
*   About StatCan  
*   Canada.ca

# Statistics Canada: Canada's national statistical agency
## WxT Search form
### About this site
*
Statistics Canada  
    *   Contact StatCan  
    *   Trust Centre
*   Contact StatCan  
*   Trust Centre  
*
Government of Canada  
    *   All contacts  
    *   Departments and agencies  
    *   About government  
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
*   All contacts  
*   Departments and agencies  
*   About government  
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
*
Government of Canada Corporate  
    *   Social media  
    *   Mobile applications  
    *   About Canada.ca  
    *   Terms and conditions  
    *   Privacy
*   Social media  
*   Mobile applications  
*   About Canada.ca  
*   Terms and conditions  
*   Privacy
Close Close overlay
× Close: Search and menus (escape key)

# Statistics Canada: Canada's national statistical agency
## WxT Search form
Search Statistics Canada
Search
</excerpt>
### Rank 5 of 19 — 0.03
<excerpt title="Full Table Download (CSV) User Guide">
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

## Data File(non-Census cubes)
### Data File Record Layout(non-Census cubes)
Ref_date
Reference period for the series being released. Spanned reference periods (2011/12) will be displayed in the same format as on the website.
Dimension name
Name of dimension. There can be up to 10 dimensions in a data table.
(i.e. Geography)
DGUID
Dissemination Geography Unique Identifier - DGUID.
It is an alphanumeric code, composed of four components.It varies from 10 to 20 characters in length. The first 9 characters are fixed in composition and length.
Vintage (4) + Type (1) + Schema (4) + **Geographic Unique Identifier (2-11) :**
VVVV T SSSS**GGGGGGGGGGG**
Unit of measure
The unit of measure applied to a member given in text. There can be multiple units of measure in a table. See Appendix B.
(i.e. acres, hectares)
Unit of measure ID
The unique reference code associated with a particular unit of measure. See Appendix B.
(i.e. 28 = acres)
Scalar factor
The scalar factor associated with a data series, displayed as text. There can be multiple scalar factors in a table. See Appendix C.
(i.e. hundreds)
Scalar_ID
The unique numeric reference code associated with a particular scalar factor. See Appendix C.
(i.e. 2 = hundreds)
Vector
Unique variable length reference code time-series identifier, consisting of the letter 'V', followed by up to 10 digits. (i.e. V1234567890, V1, etc.)
Coordinate
Concatenation of the member ID values for each dimension.
One value per dimension.
Maximum of 10 dimensions.
(i.e. 1.1.1.36.1)
Value
Data point value (the decimal is applied to the value where applicable)
(i.e. 12397.13)
Status
Shows various states of a data value using symbols. These symbols are described in the symbol legend and notes contained in the metadata file. Some symbols accompany a data value while others replace a data value. i.e. – A, B, C, D, E, F,.., X, 0s
Standard table symbols
Symbol
</excerpt>

## Search 10 — query: "38100106-eng.zip statistics canada wget"
### Rank 1 of 75 — 0.06 (passed on)
<excerpt title="Web Data Service (WDS) User Guide">
## Data Access; changes today, over time and complete data
### getDataFromVectorByReferencePeriodRange
"refPerRaw2": "",  
"value": 528800.0,  
"decimals": 0,  
"scalarFactorCode": 0,  
"symbolCode": 0,  
"statusCode": 0,  
"securityLevelCode": 0,  
"releaseTime": "2020-09-29T08:30",  
"frequencyCode": 9  
},        … repeating for every datapoint  
]  
}  
},  
… repeating for every vector requested  
]  
```

## Data Access; changes today, over time and complete data
### getFullTableDownloadCSV
For users who require the full table/cube of extracted time series, a static file download is available in both CSV and SDMX (XML) formats. Both return a link to the ProductId (PID) supplied in the URL. The CSV version also lets users select either the English (en) or French (fr) versions. The example uses English as the desired output language for CSV. In the case of accessing an SDMX full table download, it does not require a language selection due to being a bilingual format.
```  
GET URL:  
https://www150.statcan.gc.ca/t1/wds/rest/getFullTableDownloadCSV/14100287/en  
```
`RESULT:`
```  
{  
"status": "SUCCESS",  
"object": "https://www150.statcan.gc.ca/n1/tbl/csv/14100287-eng.zip"  
}  
```

## Data Access; changes today, over time and complete data
### getFullTableDownloadSDMX
```  
GET URL:  
https://www150.statcan.gc.ca/t1/wds/rest/getFullTableDownloadSDMX/14100287  
```
`RESULT:`
```  
{  
"status": "SUCCESS",  
"object": "https://www150.statcan.gc.ca/n1/tbl/sdmx/14100287-SDMX.zip"  
}  
```

## Supplemental Information
Code Sets provide additional information to describe the information such as scales, frequencies and symbols. Use method getCodeSets to access the most recent version of the code sets with descriptions (English and French) for all possible codes.

## Supplemental Information
### getCodeSets
```  
GET URL:  
https://www150.statcan.gc.ca/t1/wds/rest/getCodeSets  
```
`RESULT:`
```  
{  
"status": "SUCCESS",  
"object": {  
"scalar": [  
{  
"scalarFactorCode": 0,  
"scalarFactorDescEn": "units ",  
"scalarFactorDescFr": "unités"  
},  
… repeating objects  
],  
"frequency":   
{  
"frequencyCode": 1,  
"frequencyDescEn": "Daily",  
"frequencyDescFr": "Quotidien"  
},  
… repeating objects  
```
</excerpt>
### Rank 2 of 75 — 0.05
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
### Rank 3 of 75 — 0.04
<excerpt title="The Open Database of Addresses">
**Catalogue number:**46260001
**Issue number:** 2021001
The Open Database of Addresses (ODA) is a collection of open address point data and is made available under the Open Government License - Canada.
Statistics Canada acknowledges the many local governments that produce public address listings, which are the source of the ODA. These addresses will also be integrated into a new National Address Register (NAR) of residential and non-residential addresses, to be made available later this year by Statistics Canada. Compiled from a multitude of sources, The NAR will be a comprehensive and standardized source of publicly-available addresses and related geographic coding. It is part of the Data Strategy for the Federal Public Service.
The ODA brings together 99 datasets originating from various government sources of open data. This database aims to provide enhanced access to a harmonized listing of address data across Canada by making it available as open data. This database is a component of the Linkable Open Data Environment (LODE).

## Data sources and methodology
The inputs for the ODA are datasets provided by municipal, regional or provincial sources available to the general public through open government portals under various types of open data licenses. The current version of the database (version 1.0) contains approximately 10 million records and includes provinces and territories where open address data were found during the collection period (January to April, 2021).
Individual datasets sourced from their respective open data portals were processed and harmonized into the ODA. The data sources used do not deploy a uniform standardization system. The ODA harmonizes addresses by converting them to a uniform standard.
To see the full list of variables provided by a given data provider, please visit their open data portals which are linked in the metadata document that accompanies the ODA.
The variables included in the ODA are as follows:
*   Source Index  
*   ODA Index  
*   Group Index  
*   Civic Number  
*   Street (including street type and direction)  
*   Street Name  
*   Street Type  
*   Street Direction  
*   Unit  
*   Full Address  
*   Postal Code  
*   City  
*   Processed City  
*   Standardized Street Name  
*   Standardized Street Type  
*   Standardized Street Direction  
*   Provider  
*   Census Subdivision Name  
*   Census Subdivision Unique Identifier  
*   Province or Territory Unique Identifier  
*   Latitude  
*   Longitude
For more information on how the addresses and variables were compiled, see the metadata that accompanies the ODA.

## Downloading the ODA
For ease of download, the ODA and accompanying metadata document is provided by province and territory as a zipped CSV.
*   Alberta  
*   British Columbia  
*   Manitoba  
*   New Brunswick  
*   Northwest Territories  
*   Nova Scotia  
*   Ontario  
*   Prince Edward Island  
*   Quebec  
*   Saskatchewan
</excerpt>
### Rank 4 of 75 — 0.04
<excerpt title="Statistics Canada - Web Data Service (API) - Open Government Portal">
# Statistics Canada - Web Data Service (API) - Open Government Portal
## Menu
    *   Food and nutrition  
    *   Drug and health products  
    *   Vaccines and immunization  
    *   Diseases and conditions  
    *   Health system and services  
    *   Product safety  
    *   Healthy living  
    *   Health risks and safety  
    *   Health science, research and data  
    *   Indigenous health

    *   Most requested  
        *   Canadian Dental Care Plan  
        *   Recalls and safety alerts  
        *   Canada's food guide  
        *   Autism

*   Taxes  
    *   Taxes: home

    *   Income tax  
    *   Payments  
    *   Tax credits and benefits for individuals  
    *   GST/HST  
    *   Payroll  
    *   Business number  
    *   Charities and giving  
    *   Savings and pension plans  
    *   Excise and specialty taxes  
    *   Scams and fraud  
    *   Support in difficult situations  
    *   Compliance and enforcement  
    *   CRA Service feedback

    *   Most requested  
        *   Ready to file your GST/HST return  
        *   Find benefit payment dates  
        *   Forms and publications  
        *   Make a payment to the CRA

*   Environment and natural resources  
    *   Environment and natural resources: home

    *   Weather and hazards  
    *   Climate change  
    *   Energy  
    *   Natural resources  
    *   Agricultural production tools and data  
    *   Environment and sustainability in agriculture  
    *   Fisheries  
    *   Wildlife, plants and species  
    *   Pollution and waste management  
    *   Environmental conservation and protection  
    *   Environment statistics  
    *   Water and the environment

    *   Most requested  
        *   Local weather forecast  
        *   Fuel-efficient vehicles  
        *   Home energy efficiency  
        *   Prepare for severe weather  
        *   Download WeatherCAN

*   National security and defence  
    *   National security and defence Defence: home

    *   National security  
    *   Canadian Armed Forces  
    *   Jobs in national security and defence  
    *   Services and benefits  
    *   Cyber security  
    *   Defence equipment purchases and upgrades  
    *   Protecting the Canadian border  
    *   Transportation security
</excerpt>
### Rank 5 of 75 — 0.04
<excerpt title="Statistics Canada - Web Data Service (API) - Open Government Portal">
# Statistics Canada - Web Data Service (API) - Open Government Portal
## You are here:
1.   Canada.ca  
2.   Open Government  
3.   Search
Open Data

# Statistics Canada - Web Data Service (API)
Statistics Canada - Web Data Service (API)Statistics Canada has developed a Web Data Service that provides access to data and metadata that we release each business day. This is a good option for users who want to consume a discrete amount of data points updates to Statistics Canada data. To obtain information on how to use and consume our Web Data Service, please read the Web Data Service User Guide. 2021-03-11 Statistics Canada STATCAN.infostats-infostats.STATCAN@canada.ca Government and Politics Processes API WDS Application Programmer Interface REST JSON Web Data Service (WDS)HTML https://www.statcan.gc.ca/eng/developers/wds Web Data Service (WDS)HTML https://www.statcan.gc.ca/fra/developpeurs/sdw getCodeSets JSON https://www150.statcan.gc.ca/t1/wds/rest/getCodeSets api.canada.ca JSON https://statcan.api.canada.ca/en/detail?api=statcan-web-data-service getAllCubesListLite JSON https://www150.statcan.gc.ca/t1/wds/rest/getAllCubesListLite
Statistics Canada has developed a Web Data Service that provides access to data and metadata that we release each business day. This is a good option for users who want to consume a discrete amount of data points updates to Statistics Canada data.
To obtain information on how to use and consume our Web Data Service, please read the Web Data Service User Guide.
*   **Publisher - Current Organization Name:** Statistics Canada   
*   **Licence:**Open Government Licence - Canada

# Statistics Canada - Web Data Service (API)
## Data and Resources
Search
*   Web Data Service (WDS)HTML English  Guide  HTML
[Explore](javascript:void(0);)  
    *   More information  
    *   Go to resource
*   Web Data Service (WDS)HTML French  Guide  HTML
[Explore](javascript:void(0);)  
    *   More information  
    *   Go to resource
*   getCodeSets JSON English  French  API  JSON
[Explore](javascript:void(0);)  
    *   More information  
    *   Go to resource
*   api.canada.ca JSON English  French  API  JSON
[Explore](javascript:void(0);)  
    *   More information  
    *   Go to resource
*   getAllCubesListLite JSON English  French  API  JSON
[Explore](javascript:void(0);)  
    *   More information  
    *   Go to resource
Similar records
Did you find this dataset useful?
This dataset is rated 9 time(s) with an average rating of **Good**
</excerpt>

# Example 4
## Question
What beach in Florida allows for alcohol consumption year-round, except in the month of March?

## Expected answer
Panama City Beach

## Grade 1.00

## Search 1 — query: "Florida beach allows alcohol consumption year-round except March"
### Rank 1 of 33 — 0.98 (passed on)
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
### Rank 2 of 33 — 0.98
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
### Rank 3 of 33 — 0.96
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
###### Widespread outage hits Apple services, including Apple Pay, iCloud


# No booze on the beach for the month of March in PCB
#### Most Read
###### BCSO holds press conference, announces arrests in two separate investigations


# No booze on the beach for the month of March in PCB
#### Most Read
###### Blood pressure medication recalled over possible metal contamination


# No booze on the beach for the month of March in PCB
#### Most Read
###### Bay County film commissioner shares what’s filming locally


# No booze on the beach for the month of March in PCB
#### Most Read
###### Wanted man arrested after being found beneath Holmes County home, deputies say


# No booze on the beach for the month of March in PCB
#### Most Read
###### Classified communications network at National Security Agency goes down, defense official says


# No booze on the beach for the month of March in PCB
#### Most Read
###### Nationwide Emergency Alert System test to take place Tuesday. Here’s what will happen


# No booze on the beach for the month of March in PCB
#### Most Read
###### Lynn Haven’s Winter Wonderland moves to new location for their biggest holiday market yet


# No booze on the beach for the month of March in PCB
#### Latest News
###### Local captain honored for catching first fish from the SS United States reef
</excerpt>
### Rank 4 of 33 — 0.63
<excerpt title="No booze on the beach for the month of March in PCB">
# No booze on the beach for the month of March in PCB
#### Latest News
###### Local captain honored for catching first fish from the SS United States reef


# No booze on the beach for the month of March in PCB
#### Latest News
###### Grand Boulevard is hosting a holiday parade and more


# No booze on the beach for the month of March in PCB
#### Latest News
###### Construction causes southbound delays near DeFuniak Springs


# No booze on the beach for the month of March in PCB
#### Latest News
###### Grand Boulevard is hosting a holiday parade and more


# No booze on the beach for the month of March in PCB
#### Latest News
###### Gulf Coast State College hosts Drop Anchor event for prospective students


# No booze on the beach for the month of March in PCB
#### Latest News
###### GCSC hosts open house, annual drop anchor event


# No booze on the beach for the month of March in PCB
#### Latest News
###### Panama City Beach Chamber of Commerce packs food bags for Anchorage Children’s Home


# No booze on the beach for the month of March in PCB
#### Latest News
###### Panama City commissioners discuss flooding, approve funding for school zone beacons
News
Sports
Weather
Contact Us
Advertise with Us
Programming
Shop Local
Submit Photos & Video
Find a Job
Hurricane
Facebook
Twitter
Instagram
*   WJHG  
*   8195 Front Beach Road  
*   Panama City Beach, FL 32407  
*   (850) 234-7777
Public Inspection File
[publicfile@wjhg.com - (850) 234-7777](mailto:publicfile@wjhg.com)
Closed Captioning/Audio Description
Terms of Service
Privacy Policy
EEO Statement
FCC Applications
Advertising
Digital Marketing
Click here to learn more about our approach to artificial intelligence.
A Gray Local Media Station © 2002-2026
</excerpt>
### Rank 5 of 33 — 0.54
<excerpt title="Spring break 2026 is coming. Can you drink alcohol on Florida beaches?">
Spring break season is almost here in Florida, bringing hordes of tourists to soak up the sun at our coasts. But are you allowed to crack open a cold one on the beach?
Here's what to know before you pack your cooler full of drinks and head out on your vacation to one of Florida's beaches.

## What are Florida's laws regarding alcoholic beverages in public?
According to Florida's Open Container laws,the public consumption of alcohol is generally prohibited, which includes spaces such as parks, streets, or even beaches. Depending on where you are, you can be cited for possessing an open alcoholic beverage while in public.
However,[Florida law firm HP Defenders](https://www.hpdefenders.com/blog/can-you-drink-alcohol-on-florida-beaches/#:~:text=So%2C%20can%20you%20drink%20alcohol,designated%20areas%20on%20certain%20beaches.)writes that exceptions do exist, with certain beaches having designated areas where alcohol consumption is allowed.

## Which Florida beaches allow alcohol during spring break months?
ABC Winesshared an updated list last year of where you can bring booze on your beach day (responsibly!) and their restrictions:

## Beaches on Florida's East Coast
Beachside communities are feeling the effects of spring break with crowds, tourists and traffic jams beachside. Crowds pack the beach near the Westgate Cocoa Beach Pier.
*   **Flagler Beach:**Alcoholic beverages are permitted on the beach.

*   **Cocoa Beach:**Alcoholic beverages are permitted on the beach.

*   **Playalinda Beach:**Alcoholic beverages are permitted on the beach.

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
University students enjoy spring break near Señor Frogs Mexican Food & Fiesta in Panama City Beach, Fla., March 18, 2025. (Tyler Orsburn/News Herald)
*   **Pensacola Beach:**Alcoholic beverages are permitted on the beach, omitting an alcohol-free zone located on a "... portion of the beach on the Gulf of Mexico on Pensacola Beach extending 320 feet west of the existing Pensacola Beach Gulf Pier and 225 feet north of the shoreline to the sand fencing, encompassing an area approximately 1.75 acres" (Escambia County, Code of Ordinance, Chapter 6, Sec. 6-3. - Alcohol-free zone).

*   **Perdido Key:** Alcoholic beverages are permitted on the sandy areas of the beach.

*   **Shell Island:** Alcoholic beverages are permitted year-round.
</excerpt>

# Example 5
## Question
What US presidential election years from 1930-2020 elected US democratic presidents who served two full terms and were succeeded by a republican president, while in the same election year, a female American gymnast won the Olympic All-Around Gold medal?

## Expected answer
2008, 2012

## Grade 1.00

## Search 1 — query: "1996 Olympics women's all-around gold winner"
### Rank 1 of 86 — 0.89 (passed on)
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
### Rank 2 of 86 — 0.87
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
### Rank 3 of 86 — 0.77
<excerpt title="Magnificent Seven (gymnastics)">
The secondary story, often overlooked by the public, is that both Strug and Moceanu were in a tight contest with each other and with Dawes to qualify to the individual All-Around competition. Only three gymnasts per country could advance to the All-Around final, and had Strug not vaulted again, she would have finished fourth behind Miller, Dawes, and Moceanu. Exactly how this may have played a factor is unknown, but unlike the other U.S. gymnasts who opted to perform an easier vault first, Moceanu and Strug both performed their harder Yurchenko 1.5 for both attempts, despite warming up the easier Yurchenko half. Karolyi's strategy may have been to maximize the scores of his own gymnasts for All-Around qualification, rather than secure safe vault scores for the team first. Moceanu and Strug needed vault scores of 9.450 and 9.775 respectively to qualify ahead of Dawes.
Strug walked around, trying to shake off the injury to her ankle, as she headed back to the start of the vaulting runway with Karolyi's and her teammates' encouragement. With the scores of the three best Russian floor workers yet to be posted, Strug needed to vault a second time to secure the gold medal for her team and prevent the Russians from catching up. She performed the second vault well and nearly stuck the landing, however, she immediately lifted her injured leg and collapsed in pain, needing to be carried off the podium. Strug scored a 9.712, securing the gold medal, and the crowd erupted with cheers. This image of Strug's vault instantly became the most enduring moment of the 1996 Olympics and one of the most celebrated moments in American Olympic history. Strug not only qualified for vault finals but also for the All-Around competition. In a twist of irony, the vault that secured her place in the All-Around also prohibited her from participating as she was too injured to compete, and Moceanu took her place. Miller took her place in the vault finals, and Dawes took her place in the floor finals. Additionally, Dawes qualified for vault finals during this competition, earning the team's high vault score of 9.762.

Strug was immediately carried away to a hospital tent, however, Karolyi, adamant that she not miss the medal ceremony, eventually carried her to the podium behind the team. Miller moved out of her assigned place in line (based on height) to Strug's left side to help lift Strug onto the podium along with Moceanu who was on Strug's right. Because of being whisked away from the team and the thick bandage on her leg, Strug didn't have time to put the pants of her warm-up suit on and thus was the only one not wearing them. Because of these factors, the resulting team photographs show a less uniform look amongst the teammates than in other years.
Despite Strug's heroic vault, Miller was the team's highest-scoring member of the team competition, earning the second-highest two-day total in the entire competition (78.028, behind Lilia Podkopayeva's 78.061). However, Dawes (39.187) was the team's highest-scoring member during the optionals portion of the competition (only Simona Amânar's optionals score of 39.387 was higher than that of Dawes), and Strug's optionals total (39.073) also narrowly outscored Miller's (38.967).
The team's gold medal victory was considered phenomenal for the United States because Russia (in its incarnations as the Soviet Union and Unified Team) had won the event in every Olympics it had entered since 1952. Furthermore, the United States had never won the event in either the Olympics or the World Championships, yet in Atlanta, they fielded the deepest American team in history up to that point and upstaged both the Russians and the reigning World Champions Romanians.
Winning the gold medal instantly endeared the team to the American public, and tours, endorsement deals, interviews, and televised specials followed, earning them all a secure place in American Olympic and gymnastics history.
</excerpt>
### Rank 4 of 86 — 0.77
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
### Rank 5 of 86 — 0.74
<excerpt title="Magnificent Seven (gymnastics)">
The **Magnificent Seven** was the 1996 [United States Olympic women's gymnastics team](https://en.wikipedia.org/wiki/United_States_women's_national_artistic_gymnastics_team "United States women's national artistic gymnastics team") that won the first-ever gold medal for the United States in the [women's team competition](https://en.wikipedia.org/wiki/Gymnastics_at_the_1996_Summer_Olympics_%E2%80%93_Women's_artistic_team_all-around "Gymnastics at the 1996 Summer Olympics – Women's artistic team all-around") at the 1996 Summer Olympics in Atlanta. The seven members of the team were Shannon Miller, Dominique Moceanu, Dominique Dawes, Kerri Strug, Amy Chow, Jaycie Phelps, and team captain Amanda Borden. Miller, Chow, and Dawes also won an individual gold, silver, and bronze medals respectively in Atlanta. The team is perhaps best known for Strug sticking the landing of a vault to clinch the gold medal while injured.
The leader of the Magnificent Seven is often said to be Shannon Miller, the second most decorated American gymnast in history and that year's reigning national champion.[[1]](https://en.wikipedia.org/wiki/Magnificent_Seven_(gymnastics)#cite_note-1) The other two individual stars on the team were Dominique Dawes and Dominique Moceanu, the previous two national champions (in 1994 and 1995 respectively). However, Kerri Strug eventually qualified for the individual all-around over Moceanu.
The other three members on the team were less heralded. Nevertheless, they were an integral part of the team's success. Amy Chow had the highest difficulty of anyone on the team, most notably on the uneven bars. Jaycie Phelps provided clean lines and solid gymnastics on all four events. The final member to qualify for the team, Amanda Borden, was named team captain.[[2]](https://en.wikipedia.org/wiki/Magnificent_Seven_(gymnastics)#cite_note-2)[[3]](https://en.wikipedia.org/wiki/Magnificent_Seven_(gymnastics)#cite_note-3)

The highest two scoring athletes on the team during the compulsories did not even perform at the Olympic Trials. Both Miller and Moceanu had been sidelined with injuries but were named to the team anyway, proving that the petition system was in the team's best interest.
The team compulsories took place on July 21, 1996. Unlike in the 1992 Games, when two athletes from each country participated in each session, in these Games, teams competed together. The United States team competed in the third session, with Russia and China left to compete in the fourth session. Romania had already competed in the first session, so the United States team could only chase their already posted scores. The top four teams would compete in the last session during the optionals. Ultimately, Ukraine, not China, earned this fourth spot along with the United States, Russia, and Romania.
With seven athletes on each team for the first and only time, each team (other than Romania who had only six members because of an injury) put their six best team members up on each event. Of these six scores, only the top five would count. On the United States team in both compulsories and optionals, Miller, Moceanu, Dawes, Strug, and Phelps competed on all four events while Chow only competed on bars and vault and Borden only competed on beam and floor. The United States started their meet on uneven bars with no major misses. Miller earned the highest score of 9.775, and Strug's score of 9.675 was dropped.
Following uneven bars, the team moved to the balance beam where Strug led off with a shaky performance. Borden and Dawes followed, each with noticeable errors. Phelps, who won the compulsory round at the Olympic Trials (although neither Miller or Moceanu competed at this event), was next. Although known for her beautiful technique, she looked shaky from the start of the routine and fell off the beam during the fouette jump element. Although she finished strongly, her low score of 9.012 was dropped. Miller followed with a routine that appeared to be flawless and earned the overall high beam score of the competition, 9.737. Moceanu anchored the United States and with only minor errors and impeccable form on certain elements earned a 9.687.
</excerpt>

## Search 2 — query: "2008 Olympics women's artistic individual all-around gold medalist"
### Rank 1 of 67 — 0.87 (passed on)
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
### Rank 2 of 67 — 0.86
<excerpt title="Artistic Gymnastics at the 2008 Summer Olympics">
# Artistic Gymnastics at the 2008 Summer Olympics
## Medals
| Event | Gold | Silver | Bronze |  
| --- | --- | --- | --- |  
| All-Around, Individual, Men | Yang Wei | CHN | Kohei Uchimura | JPN | Benoît Caranobe | FRA |  
| Team, Men | People's Republic of China | CHN | Japan | JPN | United States | USA |  
| Floor Exercise, Men | Zou Kai | CHN | Gervasio Deferr | ESP | Anton Golotsutskov | RUS |  
| Vault, Men | Leszek Blanik | POL | Thomas Bouhail | FRA | Anton Golotsutskov | RUS |  
| Parallel Bars, Men | Li Xiaopeng | CHN | Yu Won-Cheol | KOR | Anton Fokin | UZB |  
| Horizontal Bar, Men | Zou Kai | CHN | Jonathan Horton | USA | Fabian Hambüchen | GER |  
| Rings, Men | Chen Yibing | CHN | Yang Wei | CHN | Oleksandr Vorobiov | UKR |  
| Pommel Horse, Men | Xiao Qin | CHN | Filip Ude | CRO | Louis Smith | GBR |  
| All-Around, Individual, Women | Nastia Liukin | USA | Shawn Johnson | USA | Yang Yilin | CHN |  
| Team, Women | People's Republic of China | CHN | United States | USA | Romania | ROU |  
| Floor Exercise, Women | Sandra Izbașa | ROU | Shawn Johnson | USA | Nastia Liukin | USA |  
| Vault, Women | Hong Un-Jong | PRK | Oksana Chusovitina | GER | Cheng Fei | CHN |  
| Uneven Bars, Women | He Kexin | CHN | Nastia Liukin | USA | Yang Yilin | CHN |  
| Balance Beam, Women | Shawn Johnson | USA | Nastia Liukin | USA | Cheng Fei | CHN |

# Artistic Gymnastics at the 2008 Summer Olympics
## Medal table
| NOC | Gold | Silver | Bronze | Total |  
| --- | --- | --- | --- | --- |  
| People's Republic of China |  CHN | 9 | 1 | 4 | 14 |  
| United States |  USA | 2 | 6 | 2 | 10 |  
| Romania |  ROU | 1 | 0 | 1 | 2 |  
| Democratic People's Republic of Korea |  PRK | 1 | 0 | 0 | 1 |  
| Poland |  POL | 1 | 0 | 0 | 1 |  
| Japan |  JPN | 0 | 2 | 0 | 2 |  
| France |  FRA | 0 | 1 | 1 | 2 |  
| Germany |  GER | 0 | 1 | 1 | 2 |  
| Croatia |  CRO | 0 | 1 | 0 | 1 |  
| Republic of Korea |  KOR | 0 | 1 | 0 | 1 |  
| Spain |  ESP | 0 | 1 | 0 | 1 |  
| Russian Federation |  RUS | 0 | 0 | 2 | 2 |  
| Great Britain |  GBR | 0 | 0 | 1 | 1 |  
| Ukraine |  UKR | 0 | 0 | 1 | 1 |  
| Uzbekistan |  UZB | 0 | 0 | 1 | 1 |

# Artistic Gymnastics at the 2008 Summer Olympics
## Medal table
### Did you know?
Until 1992, the Winter Olympics were held in the same year as the Summer Olympics. In 1986, the IOC voted to change this, allow a better spread of media attention and sponsor money.
Login | Statistics | About | Image Credits | FAQ | Feedback
© OlyMADMen 2006 — 2026
</excerpt>
### Rank 3 of 67 — 0.82
<excerpt title="Gymnastics at the 2008 Summer Olympics – Women's artistic ...">
From Wikipedia, the free encyclopedia
| Women's artistic individual all-around at the Games of the XXIX Olympiad |  
| --- |  
|  Medal ceremony |  
| Venue | Beijing National Indoor Stadium |  
| Date | 15 August 2008 |  
| Competitors | 24 from 14 nations |  
| Medalists |  
| |  | | Nastia Liukin | United States | | --- | |  | | Shawn Johnson | United States | |  | | Yang Yilin | China | |  
| ←[2004](https://en.wikipedia.org/wiki/Gymnastics_at_the_2004_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 2004 Summer Olympics – Women's artistic individual all-around") [2012](https://en.wikipedia.org/wiki/Gymnastics_at_the_2012_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 2012 Summer Olympics – Women's artistic individual all-around")→ |
**Women's artistic individual all-around** competition at the 2008 Summer Olympics was held on August 15. at the Beijing National Indoor Stadium.[[1]](https://en.wikipedia.org/wiki/Gymnastics_at_the_2008_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around#cite_note-SR-1)
For each competitor in the women's qualification, the scores[[2]](https://en.wikipedia.org/wiki/Gymnastics_at_the_2008_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around#cite_note-2) for all four apparatus were summed to give an all-around qualification score. The top 24 competitors moved on to the individual all-around final, though nations were limited to two competitors each even if more qualified. In the individual all-around final, each gymnast competed on each apparatus again. Only scores from the final were used to determine final rankings.
</excerpt>
### Rank 4 of 67 — 0.81
<excerpt title="Liukin wins gold, Johnson silver in women's all-around at 2008 Olympic ...">
## Nastia Liukin of Parker, Texas, and Shawn Johnson of West Des Moines, Iowa, won the gold and silver medals, respectively, at the 2008 Olympic Games in Beijing, China, becoming the first U.S. women to go 1-2 in the all-around at an Olympic Games.
Because they finished 1-2 in the qualification round, Johnson and Liukin competed in the Olympic order (vault, uneven bars, balance beam and floor exercise) in the finals. Johnson scored a 15.875 for her Yurchenko 2.5 vault, and Liukin earned a 15.025 for her Yurchenko 1.5. After one rotation, Romania’s Steliana Nistor was first with a 15.975, followed by Johnson in second and Italy’s Vanessa Ferrari in third with a 15.600. Liukin was 10th.
Moving to the uneven bars where she has a 7.7 start value, Liukin posted a 16.650 for her routine that includes beautiful pirouette work. Johnson stuck her layout double double dismount for a score of 15.275. Yang moved into first place after the second rotation with a score of 31.900 with Liukin in second with a 31.675 and Nistor in third with a 31.525. Johnson dropped to fifth with a 31.150.
Liukin opened her beam routine with a front aerial to flip flop layout and posted a 16.125 to take the lead with a score of 47.800 heading into the fourth and final rotation. With a score of 16.050 for her balance beam routine that includes full in dismount, Johnson moved into third place with a 47.200. Yang dropped to second with a 47.650.
Johnson and Liukin scored identical 15.525s on floor exercise in the final rotation to secure gold and silver. Yang, who scored a 15.000 on floor, fell one spot to third place.

## Nastia Liukin of Parker, Texas, and Shawn Johnson of West Des Moines, Iowa, won the gold and silver medals, respectively, at the 2008 Olympic Games in Beijing, China, becoming the first U.S. women to go 1-2 in the all-around at an Olympic Games.
Johnson and Liukin will compete in the balance beam and floor exercise finals. Alicia Sacramone of Winchester, Mass., is in the vault final, and Liukin will compete on the uneven bars. The individual event finals are Aug. 17-19 at 6 p.m. Alexander Artemev of Highlands Ranch, Colo., will compete in the pommel horse finals on Aug. 17 and Jonathan Horton of Houston is in the horizontal bar finals on Aug. 19.
Erin Blanchard of Lafayette, La., and Chris Estrada of Colorado Springs, Colo., will compete tomorrow in the trampoline qualification round at 11 a.m. for the women and 12:15 p.m. for the men.
**2008 Olympic Games
National Indoor Stadium
Beijing, China
Aug. 15, 2008
Women’s all-around final results**
**1. LIUKIN Nastia, USA, 63.325
</excerpt>
### Rank 5 of 67 — 0.81
<excerpt title="Individual all-around artistic gymnastics at the Olympics">
# Individual all-around artistic gymnastics at the Olympics
## Medalists
### Women
| 1988 Seoul [details](https://en.wikipedia.org/wiki/Gymnastics_at_the_1988_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 1988 Summer Olympics – Women's artistic individual all-around") | Yelena Shushunova Soviet Union | Daniela Silivaş Romania | Svetlana Boginskaya Soviet Union |  
| 1992 Barcelona [details](https://en.wikipedia.org/wiki/Gymnastics_at_the_1992_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 1992 Summer Olympics – Women's artistic individual all-around") | Tatiana Gutsu Unified Team | Shannon Miller United States | Lavinia Miloșovici Romania |  
| 1996 Atlanta [details](https://en.wikipedia.org/wiki/Gymnastics_at_the_1996_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 1996 Summer Olympics – Women's artistic individual all-around") | Lilia Podkopayeva Ukraine | Gina Gogean Romania | Simona Amânar Romania * * * Lavinia Miloșovici Romania |  
| 2000 Sydney [details](https://en.wikipedia.org/wiki/Gymnastics_at_the_2000_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 2000 Summer Olympics – Women's artistic individual all-around") | Simona Amânar Romania | Maria Olaru Romania | Liu Xuan China |  
| 2004 Athens [details](https://en.wikipedia.org/wiki/Gymnastics_at_the_2004_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 2004 Summer Olympics – Women's artistic individual all-around") | Carly Patterson United States | Svetlana Khorkina Russia | Zhang Nan China |  

# Individual all-around artistic gymnastics at the Olympics
## Medalists
### Women
| 2008 Beijing [details](https://en.wikipedia.org/wiki/Gymnastics_at_the_2008_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 2008 Summer Olympics – Women's artistic individual all-around") | Nastia Liukin United States | Shawn Johnson United States | Yang Yilin China |  
| 2012 London [details](https://en.wikipedia.org/wiki/Gymnastics_at_the_2012_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 2012 Summer Olympics – Women's artistic individual all-around") | Gabby Douglas United States | Viktoria Komova Russia | Aliya Mustafina Russia |  
| 2016 Rio de Janeiro [details](https://en.wikipedia.org/wiki/Gymnastics_at_the_2016_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 2016 Summer Olympics – Women's artistic individual all-around") | Simone Biles United States | Aly Raisman United States | Aliya Mustafina Russia |  
| 2020 Tokyo [details](https://en.wikipedia.org/wiki/Gymnastics_at_the_2020_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 2020 Summer Olympics – Women's artistic individual all-around")[[3]](https://en.wikipedia.org/wiki/Individual_all-around_artistic_gymnastics_at_the_Olympics#cite_note-4) | Sunisa Lee United States | Rebeca Andrade Brazil | Angelina Melnikova ROC |
</excerpt>

## Search 3 — query: "1992 women's all-around gold gymnast"
### Rank 1 of 85 — 0.89 (passed on)
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
### Rank 2 of 85 — 0.86
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
### Rank 3 of 85 — 0.80
<excerpt title="After a dominant performance at the 1992 Olympic Games, Shannon ...">
# After a dominant performance at the 1992 Olympic Games, Shannon Miller returned to domestic competition and won her first U.S. Senior All-Around National Title in 1993! Do you think the 2025 #XfinityChamps will see another first-time winner!? Join us in NOLA to find out ➡️ link in bio! | USA Gymnastics | Facebook
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
After a dominant performance at the 1992 Olympic Games, Shannon Miller returned to domestic competition and won her first U.S. Senior All-Around National Title in 1993! Do you think the 2025 #XfinityChamps will see another first-time winner!? Join us in NOLA to find out ➡️ link in bio!
Like
Comment
Share
![Image 2](blob:http://localhost/85d8b181a20aeb64a3afc2f1c39d2480)
![Image 3](blob:http://localhost/2b45e6f1a2ae097354c0b291152873d5)
4.1K
·
133 comments
·
168K views

# Video
## **[USA Gymnastics](https://www.facebook.com/USAGymnastics?__tn__=-]C)
Accounts with a verified badge have been authenticated and can be Meta Verified subscribers or notable persons or brands.**
Friday, June 6, 2025 at 9:01 PM
June 6, 2025 ·
Follow
After a dominant performance at the 1992 Olympic Games, Shannon Miller returned to domestic competit…
See more

# Video
## Comments
Most relevant
Jennifer Glover
Shannon miller GOAT
*   1y
Erica S-Prz
She will forever be my favorite female gymnast.
*   1y
View more comments
2 of 71

# Video
## Related Reels
USA Gymnastics 96K
USA Gymnastics 218K
</excerpt>
### Rank 4 of 85 — 0.73
<excerpt title="Gymnastics at the 1992 Summer Olympics – Women's artistic ...">
| 10 | Kim Zmeskal(USA) | 9.937 | 9.900 | 9.800 | 9.775 | 39.412 |  
| 11 | Sylvia Mitova(BUL) | 9.862 | 9.825 | 9.825 | 9.887 | 39.399 |  
| 12 | Betty Okino(USA) | 9.825 | 9.850 | 9.850 | 9.862 | 39.387 |  
| 13 | Cristina Fraguas(ESP) | 9.837 | 9.800 | 9.800 | 9.887 | 39.324 |  
| 14 | Li Li(CHN) | 9.825 | 9.837 | 9.750 | 9.850 | 39.262 |  
| 15 | Andrea Molnár(HUN) | 9.950 | 9.800 | 9.687 | 9.800 | 39.237 |  
| 16 | Stella Umeh(CAN) | 9.850 | 9.812 | 9.700 | 9.850 | 39.212 |  
| 17 | Mari Kosuge(JPN) | 9.887 | 9.775 | 9.800 | 9.700 | 39.162 |  
| 18 | Luisa Portocarrero(GUA) | 9.812 | 9.812 | 9.725 | 9.812 | 39.161 |  
| 19 | Monique Allen(AUS) | 9.737 | 9.837 | 9.737 | 9.775 | 39.086 |
</excerpt>
### Rank 5 of 85 — 0.73
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
Remember she fell on her mount
right off the bat. She's gotta
0:00 / 0:00
Her dismount is unreal. 🤯 Tatiana Gutsu was the 1992 Olympic all-around champion for a reason! • • #olympics #balancebeam #beam #dismount #gymnast #acrobatics #gymnastics #acro #tumbling
Like
Comment
Share
![Image 2](blob:http://localhost/85d8b181a20aeb64a3afc2f1c39d2480)
![Image 3](blob:http://localhost/2b45e6f1a2ae097354c0b291152873d5)
7.8K
·
210 comments
·
359K views

# Video
## **[Gymnastics Direct](https://www.facebook.com/gymnasticsdirect?__tn__=-]C)**
Wednesday, May 28, 2025 at 5:14 AM
May 28, 2025 ·
Follow
Her dismount is unreal.  Tatiana Gutsu was the 1992 Olympic all-around champion for a reason!…
See more

# Video
## Comments
Most relevant
Lauragh Hawkins
Times when gymnastics was gymnastics and not the light touches, mistakes and inadequacy i see these days. I mean you can tell by the crowds!
*   1y
35
![Image 5](blob:http://localhost/520c193f0276d495fb772a9afb8b220d)![Image 6](blob:http://localhost/85d8b181a20aeb64a3afc2f1c39d2480)
View all 5 replies
Nikki Gray
Am I the only one thinking “that music was in The Cutting Edge!”
*   1y
71
![Image 8](blob:http://localhost/2b45e6f1a2ae097354c0b291152873d5)![Image 9](blob:http://localhost/520c193f0276d495fb772a9afb8b220d)![Image 10](blob:http://localhost/85d8b181a20aeb64a3afc2f1c39d2480)
View all 15 replies
View more comments
2 of 107

# Video
## Related Reels
Gymnastics Direct 3.5K
Gymnastics Direct 2.7K
Gymnastics Direct 116K
Gymnastics Direct 1.9K
Gymnastics Direct 2.7K
Gymnastics Direct 2K
Gymnastics Direct 4.4K
Gymnastics Direct 4.6K
Gymnastics Direct 4K
</excerpt>

## Search 4 — query: "1932 women's artistic individual all-around gold medalist"
### Rank 1 of 76 — 0.25 (passed on)
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
### Rank 2 of 76 — 0.23
<excerpt title="Olympic Games History - Women">
| Team | AA | VT | UB | BB | FX |  
| --- | --- | --- | --- | --- | --- |  
| 1. Soviet Union 2. Hungary 3. Czechoslovakia | 1. Maria Gorokhovskaya (URS) 2. Nina Botsharova (URS) 3. Margit Korondi (HUN) | 1. Ekaterina Kalintshuk (URS) 2. Maria Gorokhovskaya (URS) 3. Galina Minaitsheva (URS) | 1. Margit Korondi (HUN) 2. Maria Gorokhovskaya (URS) 3. Agnes Keleti (HUN) | 1. Nina Botsharova (URS) 2. Maria Gorokhovskaya (URS) 3. Margit Korondi (HUN) | 1. Agnes Keleti (HUN) 2. Maria Gorokhovskaya (URS) 3. Margit Korondi (HUN) |
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
| Team | AA | VT | UB | BB | FX |  
| --- | --- | --- | --- | --- | --- |  
| 1. Czechoslovakia 2. Hungary 3. **USA** |  |  |  |  |  |
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
| Team | AA | VT | UB | BB | FX |  
| --- | --- | --- | --- | --- | --- |  
| 1. Germany 2. Czechoslovakia 3. Hungary |  |  |  |  |  |
Full Results
_July 31 – August 13, 1932_ _Los Angeles, California **·**Olympic Stadium_
**Results at a Glance**
| Team | AA | VT | UB | BB | FX |  
| --- | --- | --- | --- | --- | --- |  
| No records of women competing. |  |  |  |  |  |
Full Results
_July 29 – August 11, 1928_ _Amsterdam, The Netherlands **·**Olympic Stadium_
**Results at a Glance**
| Team | AA | VT | UB | BB | FX |  
| --- | --- | --- | --- | --- | --- |  
| 1. Netherlands 2. Italy 3. Great Britain |  |  |  |  |  |
Full Results
</excerpt>
### Rank 3 of 76 — 0.20
<excerpt title="Individual all-around artistic gymnastics at the Olympics">
# Individual all-around artistic gymnastics at the Olympics
## Medalists
### Women
| 1988 Seoul [details](https://en.wikipedia.org/wiki/Gymnastics_at_the_1988_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 1988 Summer Olympics – Women's artistic individual all-around") | Yelena Shushunova Soviet Union | Daniela Silivaş Romania | Svetlana Boginskaya Soviet Union |  
| 1992 Barcelona [details](https://en.wikipedia.org/wiki/Gymnastics_at_the_1992_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 1992 Summer Olympics – Women's artistic individual all-around") | Tatiana Gutsu Unified Team | Shannon Miller United States | Lavinia Miloșovici Romania |  
| 1996 Atlanta [details](https://en.wikipedia.org/wiki/Gymnastics_at_the_1996_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 1996 Summer Olympics – Women's artistic individual all-around") | Lilia Podkopayeva Ukraine | Gina Gogean Romania | Simona Amânar Romania * * * Lavinia Miloșovici Romania |  
| 2000 Sydney [details](https://en.wikipedia.org/wiki/Gymnastics_at_the_2000_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 2000 Summer Olympics – Women's artistic individual all-around") | Simona Amânar Romania | Maria Olaru Romania | Liu Xuan China |  
| 2004 Athens [details](https://en.wikipedia.org/wiki/Gymnastics_at_the_2004_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 2004 Summer Olympics – Women's artistic individual all-around") | Carly Patterson United States | Svetlana Khorkina Russia | Zhang Nan China |  

# Individual all-around artistic gymnastics at the Olympics
## Medalists
### Women
| 2008 Beijing [details](https://en.wikipedia.org/wiki/Gymnastics_at_the_2008_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 2008 Summer Olympics – Women's artistic individual all-around") | Nastia Liukin United States | Shawn Johnson United States | Yang Yilin China |  
| 2012 London [details](https://en.wikipedia.org/wiki/Gymnastics_at_the_2012_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 2012 Summer Olympics – Women's artistic individual all-around") | Gabby Douglas United States | Viktoria Komova Russia | Aliya Mustafina Russia |  
| 2016 Rio de Janeiro [details](https://en.wikipedia.org/wiki/Gymnastics_at_the_2016_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 2016 Summer Olympics – Women's artistic individual all-around") | Simone Biles United States | Aly Raisman United States | Aliya Mustafina Russia |  
| 2020 Tokyo [details](https://en.wikipedia.org/wiki/Gymnastics_at_the_2020_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 2020 Summer Olympics – Women's artistic individual all-around")[[3]](https://en.wikipedia.org/wiki/Individual_all-around_artistic_gymnastics_at_the_Olympics#cite_note-4) | Sunisa Lee United States | Rebeca Andrade Brazil | Angelina Melnikova ROC |
</excerpt>
### Rank 4 of 76 — 0.20
<excerpt title="Individual all-around artistic gymnastics at the Olympics">
# Individual all-around artistic gymnastics at the Olympics
## References
[2024](https://en.wikipedia.org/wiki/Gymnastics_at_the_2024_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 2024 Summer Olympics – Women's artistic individual all-around"): Simone Biles(USA) |

# Individual all-around artistic gymnastics at the Olympics
## References
| show * v * t * e Gymnastics at the Summer Olympics |  
| --- |  
| Editions | * 1896 * 1900 * 1904 * 1906 (Intercalated) * 1908 * 1912 * 1920 * 1924 * 1928 * 1932 * 1936 * 1948 * 1952 * 1956 * 1960 * 1964 * 1968 * 1972 * 1976 * 1980 * 1984 * 1988 * 1992 * 1996 * 2000 * 2004 * 2008 * 2012 * 2016 * gymnasts * 2020 * gymnasts * 2024 * gymnasts * 2028 * gymnasts |    |  
| Gymnasts | | Artistic | | Female | | Africa | * Algeria * Egypt * South Africa | | --- | | Americas | * Brazil * Canada * United States | | Asia | * China * Japan * South Korea * Uzbekistan | | Europe | * Bulgaria * France * Germany * Great Britain * Hungary * Italy * Netherlands * Romania * Russia * _Soviet Union_ * Spain * Switzerland * Ukraine | | Oceania | * Australia * New Zealand | | | --- | | Male | * Armenia * Brazil * Germany * Great Britain * Russia * Turkey * Ukraine * United States | | | --- | | Rhythmic | * Brazil | |  
| Artistic events | * Team all-around * Individual all-around * Vault * Floor * Pommel horse * Rings * Parallel bars * Horizontal bar * Uneven bars * Balance beam |  
| Rhythmic events | * Individual all-around * Group |  
| Trampoline events | * Individual |  
| Discontinued events | * Team horizontal bar * Team parallel bars * Team free system * Team Swedish system * Team portable apparatus * Rope climbing * Club swinging * Combined * Triathlon * Indian clubs * Sidehorse vault * Tumbling |  

# Individual all-around artistic gymnastics at the Olympics
## References
| * List of medalists * men * women * List of venues |
Retrieved from "https://en.wikipedia.org/w/index.php?title=Individual_all-around_artistic_gymnastics_at_the_Olympics&oldid=1379732207"
Categories:
*   Olympic artistic gymnastics events  
*   All-around artistic gymnastics
Hidden categories:
*   Articles with short description  
*   Short description matches Wikidata  
*   Articles needing additional references from June 2026  
*   All articles needing additional references  
*   Use dmy dates from March 2021  
*   Articles with hCards

*    This page was last edited on 11 October 2026, at 16:50(UTC).  
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
Individual all-around artistic gymnastics at the Olympics
1 languageAdd topic
</excerpt>
### Rank 5 of 76 — 0.20
<excerpt title="Individual all-around artistic gymnastics at the Olympics">
# Individual all-around artistic gymnastics at the Olympics
## Medalists
### Women
| 1968 Mexico City [details](https://en.wikipedia.org/wiki/Gymnastics_at_the_1968_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 1968 Summer Olympics – Women's artistic individual all-around") | Věra Čáslavská Czechoslovakia | Zinaida Voronina Soviet Union | Natalia Kuchinskaya Soviet Union |  
| 1972 Munich [details](https://en.wikipedia.org/wiki/Gymnastics_at_the_1972_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 1972 Summer Olympics – Women's artistic individual all-around") | Ludmilla Tourischeva Soviet Union | Karin Janz East Germany | Tamara Lazakovich Soviet Union |  
| 1976 Montreal [details](https://en.wikipedia.org/wiki/Gymnastics_at_the_1976_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 1976 Summer Olympics – Women's artistic individual all-around") | Nadia Comăneci Romania | Nellie Kim Soviet Union | Ludmilla Tourischeva Soviet Union |  
| 1980 Moscow [details](https://en.wikipedia.org/wiki/Gymnastics_at_the_1980_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 1980 Summer Olympics – Women's artistic individual all-around") | Elena Davydova Soviet Union | Nadia Comăneci Romania * * * Maxi Gnauck East Germany | Not awarded |  
| 1984 Los Angeles [details](https://en.wikipedia.org/wiki/Gymnastics_at_the_1984_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 1984 Summer Olympics – Women's artistic individual all-around") | Mary Lou Retton United States | Ecaterina Szabo Romania | Simona Păucă Romania |
</excerpt>

## Search 5 — query: "2020 Olympic women's artistic individual all-around gold medalist"
### Rank 1 of 115 — 0.83 (passed on)
<excerpt title="Sunisa Lee">
2024 Paris[Uneven Bars](https://en.wikipedia.org/wiki/Gymnastics_at_the_2024_Summer_Olympics_%E2%80%93_Women's_uneven_bars "Gymnastics at the 2024 Summer Olympics – Women's uneven bars") World Championships 2019 StuttgartTeam 2019 Stuttgart Floor Exercise 2019 Stuttgart Uneven Bars Representing the [Auburn Tigers](https://en.wikipedia.org/wiki/Auburn_Tigers_women's_gymnastics "Auburn Tigers women's gymnastics") [NCAA Championships](https://en.wikipedia.org/wiki/NCAA_Women's_Gymnastics_Championships "NCAA Women's Gymnastics Championships") [2022 Fort Worth](https://en.wikipedia.org/wiki/2022_NCAA_Women's_Gymnastics_Championship "2022 NCAA Women's Gymnastics Championship")Balance Beam 2022 Fort Worth All-Around |
|  |  
| Awards | _See awards_ |

**Sunisa** "**Suni**" **Phabsomphou Lee**[[a]](https://en.wikipedia.org/wiki/Sunisa_Lee#cite_note-1) (born March 9, 2003)[[1]](https://en.wikipedia.org/wiki/Sunisa_Lee#cite_note-2)[[2]](https://en.wikipedia.org/wiki/Sunisa_Lee#cite_note-msnbc.com-3) is an American artistic gymnast. She is the 2020 Olympic [all-around](https://en.wikipedia.org/wiki/Gymnastics_at_the_2020_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 2020 Summer Olympics – Women's artistic individual all-around") gold medalist and [uneven bars](https://en.wikipedia.org/wiki/Gymnastics_at_the_2020_Summer_Olympics_%E2%80%93_Women's_uneven_bars "Gymnastics at the 2020 Summer Olympics – Women's uneven bars") bronze medalist and the 2024 Olympic [all-around](https://en.wikipedia.org/wiki/Gymnastics_at_the_2024_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 2024 Summer Olympics – Women's artistic individual all-around") and [uneven bars](https://en.wikipedia.org/wiki/Gymnastics_at_the_2024_Summer_Olympics_%E2%80%93_Women's_uneven_bars "Gymnastics at the 2024 Summer Olympics – Women's uneven bars") bronze medalist. She was the 2019 World Championship silver medalist on the floor and bronze medalist on uneven bars. Lee was a part of the "Golden Girls" that won gold at the 2024 Summer Olympics.[[3]](https://en.wikipedia.org/wiki/Sunisa_Lee#cite_note-4) She was also a member of the teams that won gold at the 2019 World Championships and silver at the 2020 Summer Olympics. She is also a two-time U.S. national champion on the uneven bars.
</excerpt>
### Rank 2 of 115 — 0.82
<excerpt title="Gymnastics at the 2020 Summer Olympics – Women's artistic ...">
| Rank | Gymnast |  |  |  |  | Total |  
| --- | --- | --- | --- | --- | --- | --- |  
| **** | Sunisa Lee(USA) | 14.600 (=5) | 15.300 (1) | 13.833 (2) | 13.700 (=5) | **57.433** |  
| **** | Rebeca Andrade(BRA) | 15.300 (1) | 14.666 (5) | 13.666 (5) | 13.666 (7) | **57.298** |  
| **** | Angelina Melnikova(ROC) | 14.633 (4) | 14.900 (3) | 13.700 (4) | 13.966 (2) | **57.199** |  
| **4** | Vladislava Urazova(ROC) | 14.500 (=9) | 14.866 (4) | 14.200 (1) | 13.400 (10) | **56.966** |  
| **5** | Mai Murakami(JPN) | 14.533 (8) | 13.733 (12) | 13.766 (3) | 14.000 (1) | **56.032** |  
| **6** | Nina Derwael(BEL) | 13.900 (19) | 15.266 (2) | 13.366 (6) | 13.433 (9) | **55.965** |  
| **7** | Tang Xijing(CHN) | 14.233 (16) | 14.233 (8) | 13.066 (9) | 12.966 (18) | **54.498** |
</excerpt>
### Rank 3 of 115 — 0.82
<excerpt title="Gymnastics at the 2020 Summer Olympics – Women's artistic ...">
The competition was held over two days, Sunday, 25 July and Thursday, 29 July. The qualifying round (for all women's gymnastics events) was the first day; the all-around final was on the second day.[[1]](https://en.wikipedia.org/wiki/Gymnastics_at_the_2020_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around#cite_note-dates-1)
| Date | Time | Round | Subdivision |  
| --- | --- | --- | --- |  
| 25 July | 10:00 | **Qualification** | Subdivision 1 |  
| 11:50 | Subdivision 2 |  
| 15:10 | Subdivision 3 |  
| 17:05 | Subdivision 4 |  
| 20:20 | Subdivision 5 |  
| 29 July | 19:50 | **Final** | – |  
| All times are local time (UTC+09:00). |
The gymnasts who ranked in the top twenty-four qualified for the final round. In cases where more than two gymnasts from the same NOC were in the top twenty-four, only the top two ranked among them would qualify to the final round, while the others would be excluded; the next-best ranked gymnast would qualify instead.

| Rank | Gymnast |  |  |  |  | Total | Results |  
| --- | --- | --- | --- | --- | --- | --- | --- |  
| **1** | Simone Biles(USA) | 14.966 | 14.566 | 14.066 | 14.133 | **57.731** | **Q W**[[5]](https://en.wikipedia.org/wiki/Gymnastics_at_the_2020_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around#cite_note-biles-5) |  
| **2** | Rebeca Andrade(BRA) | 15.400 | 14.200 | 13.733 | 14.066 | **57.399** | **Q** |  
| **3** | Sunisa Lee(USA) | 14.333 | 15.200 | 14.200 | 13.433 | **57.166** | **Q** |  
| **4** | Angelina Melnikova(ROC) | 14.466 | 14.933 | 13.733 | 14.000 | **57.132** | **Q** |  
| **5** | Vladislava Urazova(ROC) | 14.600 | 14.866 | 14.000 | 13.633 | **57.099** | **Q** |  
| **6** | Viktoria Listunova(ROC) | 14.300 | 14.766 | 13.866 | 14.000 | **56.932** | **–** |  
| **7** | Nina Derwael(BEL) | 13.900 | 15.366 | 13.766 | 13.566 | **56.598** | **Q** |
</excerpt>
### Rank 4 of 115 — 0.81
<excerpt title="Gymnastics at the 2020 Summer Olympics – Women's artistic ...">
| Rank | Gymnast |  |  |  |  | Total | Results |  
| --- | --- | --- | --- | --- | --- | --- | --- |  
| **1** | Simone Biles(USA) | 14.966 | 14.566 | 14.066 | 14.133 | **57.731** | **Q W**[[5]](https://en.wikipedia.org/wiki/Gymnastics_at_the_2020_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around#cite_note-biles-5) |  
| **2** | Rebeca Andrade(BRA) | 15.400 | 14.200 | 13.733 | 14.066 | **57.399** | **Q** |  
| **3** | Sunisa Lee(USA) | 14.333 | 15.200 | 14.200 | 13.433 | **57.166** | **Q** |  
| **4** | Angelina Melnikova(ROC) | 14.466 | 14.933 | 13.733 | 14.000 | **57.132** | **Q** |  
| **5** | Vladislava Urazova(ROC) | 14.600 | 14.866 | 14.000 | 13.633 | **57.099** | **Q** |  
| **6** | Viktoria Listunova(ROC) | 14.300 | 14.766 | 13.866 | 14.000 | **56.932** | **–** |  
| **7** | Nina Derwael(BEL) | 13.900 | 15.366 | 13.766 | 13.566 | **56.598** | **Q** |
</excerpt>
### Rank 5 of 115 — 0.81
<excerpt title="Sunisa Lee">
**Sunisa** "**Suni**" **Phabsomphou Lee**[[a]](https://en.wikipedia.org/wiki/Sunisa_Lee#cite_note-1) (born March 9, 2003)[[1]](https://en.wikipedia.org/wiki/Sunisa_Lee#cite_note-2)[[2]](https://en.wikipedia.org/wiki/Sunisa_Lee#cite_note-msnbc.com-3) is an American artistic gymnast. She is the 2020 Olympic [all-around](https://en.wikipedia.org/wiki/Gymnastics_at_the_2020_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 2020 Summer Olympics – Women's artistic individual all-around") gold medalist and [uneven bars](https://en.wikipedia.org/wiki/Gymnastics_at_the_2020_Summer_Olympics_%E2%80%93_Women's_uneven_bars "Gymnastics at the 2020 Summer Olympics – Women's uneven bars") bronze medalist and the 2024 Olympic [all-around](https://en.wikipedia.org/wiki/Gymnastics_at_the_2024_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 2024 Summer Olympics – Women's artistic individual all-around") and [uneven bars](https://en.wikipedia.org/wiki/Gymnastics_at_the_2024_Summer_Olympics_%E2%80%93_Women's_uneven_bars "Gymnastics at the 2024 Summer Olympics – Women's uneven bars") bronze medalist. She was the 2019 World Championship silver medalist on the floor and bronze medalist on uneven bars. Lee was a part of the "Golden Girls" that won gold at the 2024 Summer Olympics.[[3]](https://en.wikipedia.org/wiki/Sunisa_Lee#cite_note-4) She was also a member of the teams that won gold at the 2019 World Championships and silver at the 2020 Summer Olympics. She is also a two-time U.S. national champion on the uneven bars.

In NCAA Gymnastics, she competed for the Auburn Tigers[gymnastics](https://en.wikipedia.org/wiki/Auburn_Tigers_women's_gymnastics "Auburn Tigers women's gymnastics") team, winning a SEC title on uneven bars and an [NCAA championship](https://en.wikipedia.org/wiki/NCAA_women's_gymnastics_tournament "NCAA women's gymnastics tournament") on balance beam. She is the third female gymnast to win NCAA, World, and Olympic championship titles, after Kyla Ross and Madison Kocian.[[4]](https://en.wikipedia.org/wiki/Sunisa_Lee#cite_note-5)
Lee is the first Hmong-American Olympian. She is also reported to be the first woman of Hmong descent[[5]](https://en.wikipedia.org/wiki/Sunisa_Lee#cite_note-:7-6) and first Asian American woman to win the Olympic all-around title.[[6]](https://en.wikipedia.org/wiki/Sunisa_Lee#cite_note-:8-7) She is a six-time member of the [U.S. women's national gymnastics team](https://en.wikipedia.org/wiki/United_States_women's_national_gymnastics_team "United States women's national gymnastics team"), and with nine world championship and Olympic medals, she is the [seventh-most-decorated American female gymnast](https://en.wikipedia.org/wiki/United_States_women's_national_artistic_gymnastics_team#Most_decorated_gymnasts "United States women's national artistic gymnastics team").[[7]](https://en.wikipedia.org/wiki/Sunisa_Lee#cite_note-8)
</excerpt>

## Search 6 — query: "Barack Obama served two terms 2009 2017"
### Rank 1 of 138 — 0.68 (passed on)
<excerpt title="Presidency of Barack Obama">
Barack Obama's tenure as the 44th president of the United States began with his first inauguration on January 20, 2009, and ended on January 20, 2017. Obama, a Democrat from Illinois, took office after defeating the Republican nominee John McCain in the 2008 presidential election. Four years later, he won re-election in the 2012 presidential election, after defeating the Republican nominee Mitt Romney. Alongside Obama's presidency, the Democratic Party also held their majorities in the House of Representatives during the 111th U.S. Congress following the 2008 elections, thereby attained an overall federal government trifecta. Obama is the first African American president, the first multiracial president, the first non-white president,[a] and the first president born in Hawaii. Obama was constitutionally limited to two terms (the second re-elected Democrat President to be so) and was succeeded by Republican Donald Trump, who won the 2016 presidential election against Obama's preferred successor, Hillary Clinton. Historians and political scientists rank him among the upper tier in historical rankings of American presidents.
Obama's accomplishments during the first 100 days of his presidency included signing the Lilly Ledbetter Fair Pay Act of 2009; relaxing the statute of limitations for equal-pay lawsuits;[2] signing into law the expanded Children's Health Insurance Program (S-CHIP); winning approval of a congressional budget resolution that put Congress on record as dedicated to dealing with major health care reform legislation in 2009; implementing new ethics guidelines designed to significantly curtail the influence of lobbyists on the executive branch; breaking from the Bush administration on a number of policy fronts, except for Iraq, in which he followed through on Bush's Iraq withdrawal of US troops;[3] supporting the UN declaration on sexual orientation and gender identity; and lifting the 7½-year ban on federal funding for embryonic stem cell research.[4] Obama also ordered the closure of the Guantanamo Bay detention camp, in Cuba, though it remained open throughout his presidency. He lifted some travel and money restrictions to the island.[3]

Obama signed many landmark bills into law during his first two years in office. The main reforms include: the Affordable Care Act, sometimes referred to as "the ACA" or "Obamacare", the Dodd–Frank Wall Street Reform and Consumer Protection Act, and the Don't Ask, Don't Tell Repeal Act of 2010. The American Recovery and Reinvestment Act and Tax Relief, Unemployment Insurance Reauthorization, and Job Creation Act served as economic stimuli amidst the Great Recession. After a lengthy debate over the national debt limit, he signed the Budget Control Act of 2011 and the American Taxpayer Relief Act of 2012. In foreign policy, he increased US troop levels in Afghanistan, reduced nuclear weapons with the United States–Russia New START treaty, and ended military involvement in the Iraq War. He gained widespread praise for ordering Operation Neptune Spear, the raid that killed Osama bin Laden, who was responsible for the September 11 attacks. In 2011, Obama ordered the drone-strike killing in Yemen of al-Qaeda operative Anwar al-Awlaki, who was an American citizen. He ordered military involvement in Libya in order to implement UN Security Council Resolution 1973, contributing to the overthrow of Muammar Gaddafi.
</excerpt>
### Rank 2 of 138 — 0.61
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
### Rank 3 of 138 — 0.60
<excerpt title="President Barack Obama | whitehouse.gov">
# President Barack Obama | whitehouse.gov
## People
*   President Barack Obama  
*   Vice President Joe Biden  
*   First Lady Michelle Obama  
*   Dr. Jill Biden  
*   The Cabinet  
*   Executive Office of the President  
*   Senior White House Leadership  
*   Other Advisory Boards

# President Barack Obama
Barack Obama is the 44th President of the United States. His story is the American story -- values from the heartland, a middle-class upbringing in a strong family, hard work and education as the means of getting ahead, and the conviction that a life so blessed should be lived in service to others.
Download Low-res (296 KB)
Download Hi-res (1256 KB)
Barack H. Obama is the 44th President of the United States.
His story is the American story — values from the heartland, a middle-class upbringing in a strong family, hard work and education as the means of getting ahead, and the conviction that a life so blessed should be lived in service to others.
With a father from Kenya and a mother from Kansas, President Obama was born in Hawaii on August 4, 1961. He was raised with help from his grandfather, who served in Patton's army, and his grandmother, who worked her way up from the secretarial pool to middle management at a bank.
After working his way through college with the help of scholarships and student loans, President Obama moved to Chicago, where he worked with a group of churches to help rebuild communities devastated by the closure of local steel plants.
He went on to attend law school, where he became the first African-American president of the _Harvard Law Review_. Upon graduation, he returned to Chicago to help lead a voter registration drive, teach constitutional law at the University of Chicago, and remain active in his community.
President Obama's years of public service are based around his unwavering belief in the ability to unite people around a politics of purpose. In the Illinois State Senate, he passed the first major ethics reform in 25 years, cut taxes for working families, and expanded health care for children and their parents. As a United States Senator, he reached across the aisle to pass groundbreaking lobbying reform, lock up the world's most dangerous weapons, and bring transparency to government by putting federal spending online.
He was elected the 44th President of the United States on November 4, 2008, and sworn in on January 20, 2009. After being re-elected in 2012, President Obama is currently serving his second and final term, which will end in January 2017. See photos from the President's second inauguration here.
</excerpt>
### Rank 4 of 138 — 0.58
<excerpt title="OnThisDay in 1961, Barack Obama was born. After serving as a senator ...">
•
Follow
* * *
#OnThisDay in 1961, Barack Obama was born. After serving as a senator for Illinois, he was elected 44th President of the United States and served from 2009 to 2017. Obama was the first Black American elected President of the United States in history. He was awarded the Nobel Peace Prize for his efforts during the first year of his presidency.   
📸 Collection of the Smithsonian National Museum of African American History and Culture, Gift of Platon, © Platon.
💜✨
Reply
🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥
Reply
Happy birthday President Obama!
Reply
❤️
Reply
🎉❤️
Reply
❤️❤️Happy Birthday!!
Reply
Happy Birthday President Obama!! 🎉
Reply
Happy Birthday President Obama 🎂🎁🎉
Reply
Happy birthday to the GOAT
1 like
Reply
🥳🍰♥️
Reply
Happy birthday President Obama 🎉🎉🎉🎉
4 likes
Reply
❤️Happy Birthday!
Reply
1.9K 22
</excerpt>
### Rank 5 of 138 — 0.57
<excerpt title="Presidency of Barack Obama">
After his transition period, Obama entered office with an approval rating of 82% according to Gallup,[490] Obama's approval rating fell to 69% after he took office and announced his first policy decisions.[491] Obama received the support of 90% of Democrats, 60% of independents, and 40% of Republicans in January 2009 polls.[491] By December 2009, Obama's approval rating had fallen to 51%, with Obama receiving approval from roughly 85% of Democrats, 45% of independents, and just 18% of Republicans.[491] In July 2010, after the passage of the Dodd-Frank and Obamacare, Obama's approval rating stood at 45%, with 47% disapproving.[491] Obama's approval rating would remain stable until the 2010 elections,[491] when Republicans won major gains in both houses of Congress and took control of the House.[468] Obama's approval ratings climbed back to 50% in January 2011, but fell to 40% in August 2011 following the 2011 debt-ceiling crisis.[491] Obama's approval ratings slowly increased during 2012, and they rose above 50% shortly before the 2012 election, in which Obama defeated Mitt Romney.[491] After his re-election, Obama's approval ratings reached 57%, but that number fell into the low 40s after the federal government shutdown in October 2013.[491] Obama's approval ratings remained in the mid-to-low 40s until the 2014 elections, when Republicans won gains in both houses of Congress and took control of the Senate.[491] In 2015, Obama's approval ratings climbed to the mid-to-high 40s, with his approval and disapproval ratings roughly matching each other.[491] His approval ratings rose into the 50s during the 2016 presidential campaign, and Obama registered a 57% approval rating in November 2016.[491] In a Gallup poll taken in the final week of his presidency, Obama registered a 95% approval rating with Democrats,

a 61% approval rating with independents, and a 14% approval rating with Republicans.[491]
Obama's election also provoked a reaction to his race, birthplace, and religion. As president, Obama faced numerous taunts and racial innuendos, though most overt racist comments were limited to a small fringe.[492] Donald Trump theorized that Obama had been born in Kenya; an April 2011 CNN poll taken shortly before Obama released his long-form birth certificate found that 40% of Republicans believed that Obama had been born in Kenya.[481] Many of these "birthers" argued that because Obama was (allegedly) not a citizen, he was not eligible to serve as president under the natural-born-citizen requirements of the Constitution. Despite Obama's release of his long-form birth certificate, which affirmed that Obama was born in Hawaii, a 2015 CNN poll found that 20% of Americans believed that Obama was born outside of the country.[493] Many also claimed that Obama practiced Islam, and a 2015 CNN poll found that 29% of Americans and 43% of Republicans believed Obama to be a Muslim.[493] Even prior to his election as president, Obama had clarified that he was a long-time member of a church affiliated with the United Church of Christ, a mainline Protestant denomination.[494]
</excerpt>

## Search 7 — query: "1932 women's artistic individual all-around gold medalist USA"
### Rank 1 of 146 — 0.25 (passed on)
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
### Rank 2 of 146 — 0.21
<excerpt title="Individual all-around artistic gymnastics at the Olympics">
# Individual all-around artistic gymnastics at the Olympics
## Medalists
### Women
| 1988 Seoul [details](https://en.wikipedia.org/wiki/Gymnastics_at_the_1988_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 1988 Summer Olympics – Women's artistic individual all-around") | Yelena Shushunova Soviet Union | Daniela Silivaş Romania | Svetlana Boginskaya Soviet Union |  
| 1992 Barcelona [details](https://en.wikipedia.org/wiki/Gymnastics_at_the_1992_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 1992 Summer Olympics – Women's artistic individual all-around") | Tatiana Gutsu Unified Team | Shannon Miller United States | Lavinia Miloșovici Romania |  
| 1996 Atlanta [details](https://en.wikipedia.org/wiki/Gymnastics_at_the_1996_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 1996 Summer Olympics – Women's artistic individual all-around") | Lilia Podkopayeva Ukraine | Gina Gogean Romania | Simona Amânar Romania * * * Lavinia Miloșovici Romania |  
| 2000 Sydney [details](https://en.wikipedia.org/wiki/Gymnastics_at_the_2000_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 2000 Summer Olympics – Women's artistic individual all-around") | Simona Amânar Romania | Maria Olaru Romania | Liu Xuan China |  
| 2004 Athens [details](https://en.wikipedia.org/wiki/Gymnastics_at_the_2004_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 2004 Summer Olympics – Women's artistic individual all-around") | Carly Patterson United States | Svetlana Khorkina Russia | Zhang Nan China |  

# Individual all-around artistic gymnastics at the Olympics
## Medalists
### Women
| 2008 Beijing [details](https://en.wikipedia.org/wiki/Gymnastics_at_the_2008_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 2008 Summer Olympics – Women's artistic individual all-around") | Nastia Liukin United States | Shawn Johnson United States | Yang Yilin China |  
| 2012 London [details](https://en.wikipedia.org/wiki/Gymnastics_at_the_2012_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 2012 Summer Olympics – Women's artistic individual all-around") | Gabby Douglas United States | Viktoria Komova Russia | Aliya Mustafina Russia |  
| 2016 Rio de Janeiro [details](https://en.wikipedia.org/wiki/Gymnastics_at_the_2016_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 2016 Summer Olympics – Women's artistic individual all-around") | Simone Biles United States | Aly Raisman United States | Aliya Mustafina Russia |  
| 2020 Tokyo [details](https://en.wikipedia.org/wiki/Gymnastics_at_the_2020_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 2020 Summer Olympics – Women's artistic individual all-around")[[3]](https://en.wikipedia.org/wiki/Individual_all-around_artistic_gymnastics_at_the_Olympics#cite_note-4) | Sunisa Lee United States | Rebeca Andrade Brazil | Angelina Melnikova ROC |
</excerpt>
### Rank 3 of 146 — 0.21
<excerpt title="Individual all-around artistic gymnastics at the Olympics">
# Individual all-around artistic gymnastics at the Olympics
## References
[2024](https://en.wikipedia.org/wiki/Gymnastics_at_the_2024_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 2024 Summer Olympics – Women's artistic individual all-around"): Simone Biles(USA) |

# Individual all-around artistic gymnastics at the Olympics
## References
| show * v * t * e Gymnastics at the Summer Olympics |  
| --- |  
| Editions | * 1896 * 1900 * 1904 * 1906 (Intercalated) * 1908 * 1912 * 1920 * 1924 * 1928 * 1932 * 1936 * 1948 * 1952 * 1956 * 1960 * 1964 * 1968 * 1972 * 1976 * 1980 * 1984 * 1988 * 1992 * 1996 * 2000 * 2004 * 2008 * 2012 * 2016 * gymnasts * 2020 * gymnasts * 2024 * gymnasts * 2028 * gymnasts |    |  
| Gymnasts | | Artistic | | Female | | Africa | * Algeria * Egypt * South Africa | | --- | | Americas | * Brazil * Canada * United States | | Asia | * China * Japan * South Korea * Uzbekistan | | Europe | * Bulgaria * France * Germany * Great Britain * Hungary * Italy * Netherlands * Romania * Russia * _Soviet Union_ * Spain * Switzerland * Ukraine | | Oceania | * Australia * New Zealand | | | --- | | Male | * Armenia * Brazil * Germany * Great Britain * Russia * Turkey * Ukraine * United States | | | --- | | Rhythmic | * Brazil | |  
| Artistic events | * Team all-around * Individual all-around * Vault * Floor * Pommel horse * Rings * Parallel bars * Horizontal bar * Uneven bars * Balance beam |  
| Rhythmic events | * Individual all-around * Group |  
| Trampoline events | * Individual |  
| Discontinued events | * Team horizontal bar * Team parallel bars * Team free system * Team Swedish system * Team portable apparatus * Rope climbing * Club swinging * Combined * Triathlon * Indian clubs * Sidehorse vault * Tumbling |  

# Individual all-around artistic gymnastics at the Olympics
## References
| * List of medalists * men * women * List of venues |
Retrieved from "https://en.wikipedia.org/w/index.php?title=Individual_all-around_artistic_gymnastics_at_the_Olympics&oldid=1379732207"
Categories:
*   Olympic artistic gymnastics events  
*   All-around artistic gymnastics
Hidden categories:
*   Articles with short description  
*   Short description matches Wikidata  
*   Articles needing additional references from June 2026  
*   All articles needing additional references  
*   Use dmy dates from March 2021  
*   Articles with hCards

*    This page was last edited on 11 October 2026, at 16:50(UTC).  
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
Individual all-around artistic gymnastics at the Olympics
1 languageAdd topic
</excerpt>
### Rank 4 of 146 — 0.20
<excerpt title="Individual all-around artistic gymnastics at the Olympics">
# Individual all-around artistic gymnastics at the Olympics
## Medalists
### Women
| 1968 Mexico City [details](https://en.wikipedia.org/wiki/Gymnastics_at_the_1968_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 1968 Summer Olympics – Women's artistic individual all-around") | Věra Čáslavská Czechoslovakia | Zinaida Voronina Soviet Union | Natalia Kuchinskaya Soviet Union |  
| 1972 Munich [details](https://en.wikipedia.org/wiki/Gymnastics_at_the_1972_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 1972 Summer Olympics – Women's artistic individual all-around") | Ludmilla Tourischeva Soviet Union | Karin Janz East Germany | Tamara Lazakovich Soviet Union |  
| 1976 Montreal [details](https://en.wikipedia.org/wiki/Gymnastics_at_the_1976_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 1976 Summer Olympics – Women's artistic individual all-around") | Nadia Comăneci Romania | Nellie Kim Soviet Union | Ludmilla Tourischeva Soviet Union |  
| 1980 Moscow [details](https://en.wikipedia.org/wiki/Gymnastics_at_the_1980_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 1980 Summer Olympics – Women's artistic individual all-around") | Elena Davydova Soviet Union | Nadia Comăneci Romania * * * Maxi Gnauck East Germany | Not awarded |  
| 1984 Los Angeles [details](https://en.wikipedia.org/wiki/Gymnastics_at_the_1984_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 1984 Summer Olympics – Women's artistic individual all-around") | Mary Lou Retton United States | Ecaterina Szabo Romania | Simona Păucă Romania |
</excerpt>
### Rank 5 of 146 — 0.18
<excerpt title="Individual all-around artistic gymnastics at the Olympics">
# Individual all-around artistic gymnastics at the Olympics
## Medalists
### Women
[edit]
| Games | Gold | Silver | Bronze |  
| --- | --- | --- | --- |  
| 1952 Helsinki [details](https://en.wikipedia.org/wiki/Gymnastics_at_the_1952_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 1952 Summer Olympics – Women's artistic individual all-around") | Maria Gorokhovskaya Soviet Union | Nina Bocharova Soviet Union | Margit Korondi Hungary |  
| 1956 Melbourne [details](https://en.wikipedia.org/wiki/Gymnastics_at_the_1956_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 1956 Summer Olympics – Women's artistic individual all-around") | Larisa Latynina Soviet Union | Ágnes Keleti Hungary | Sofia Muratova Soviet Union |  
| 1960 Rome [details](https://en.wikipedia.org/wiki/Gymnastics_at_the_1960_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 1960 Summer Olympics – Women's artistic individual all-around") | Larisa Latynina Soviet Union | Sofia Muratova Soviet Union | Polina Astakhova Soviet Union |  
| 1964 Tokyo [details](https://en.wikipedia.org/wiki/Gymnastics_at_the_1964_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 1964 Summer Olympics – Women's artistic individual all-around") | Věra Čáslavská Czechoslovakia | Larisa Latynina Soviet Union | Polina Astakhova Soviet Union |  

# Individual all-around artistic gymnastics at the Olympics
## Medalists
### Women
| 1968 Mexico City [details](https://en.wikipedia.org/wiki/Gymnastics_at_the_1968_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 1968 Summer Olympics – Women's artistic individual all-around") | Věra Čáslavská Czechoslovakia | Zinaida Voronina Soviet Union | Natalia Kuchinskaya Soviet Union |  
| 1972 Munich [details](https://en.wikipedia.org/wiki/Gymnastics_at_the_1972_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 1972 Summer Olympics – Women's artistic individual all-around") | Ludmilla Tourischeva Soviet Union | Karin Janz East Germany | Tamara Lazakovich Soviet Union |  
| 1976 Montreal [details](https://en.wikipedia.org/wiki/Gymnastics_at_the_1976_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 1976 Summer Olympics – Women's artistic individual all-around") | Nadia Comăneci Romania | Nellie Kim Soviet Union | Ludmilla Tourischeva Soviet Union |  
| 1980 Moscow [details](https://en.wikipedia.org/wiki/Gymnastics_at_the_1980_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 1980 Summer Olympics – Women's artistic individual all-around") | Elena Davydova Soviet Union | Nadia Comăneci Romania * * * Maxi Gnauck East Germany | Not awarded |  
| 1984 Los Angeles [details](https://en.wikipedia.org/wiki/Gymnastics_at_the_1984_Summer_Olympics_%E2%80%93_Women's_artistic_individual_all-around "Gymnastics at the 1984 Summer Olympics – Women's artistic individual all-around") | Mary Lou Retton United States | Ecaterina Szabo Romania | Simona Păucă Romania |
</excerpt>

## Search 8 — query: "1996 women's all-around gold medal 1996 olympics all around winner"
### Rank 1 of 72 — 0.87 (passed on)
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
### Rank 2 of 72 — 0.87
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
### Rank 3 of 72 — 0.78
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
### Rank 4 of 72 — 0.57
<excerpt title="REMEMBER THIS? One of Atlanta '96's signature nights unfolded at the ...">
# REMEMBER THIS? One of Atlanta ’96’s... - Atlanta News First | Facebook
## Atlanta News First's Post
*   [16w](https://www.facebook.com/AtlantaNewsFirst/posts/pfbid0z3r7WC4Ref9kwAUCMap1xWnBYwLRygX1TXJ6gcPTEmaSyAziC2vRiSzShHLvmyMdl?comment_id=980462971715550&__cft__[0]=AZjSd9YzMFxYAOHE1zK-5EYIkO-EiQWieMo6cojJl5JwzksnUc8AV6hPLr2Q7gz1CzT4_wZWP-_blAXGi6Y6VRsSDrFcS5JCY21cu09hXLVevvDbBdC5XgazgQs8s9j9HHwZIYVwaBwl1WqUlGqFm5vc4x1SBAtR&__tn__=R]-R)
Marsha Kindrachuk Loversky
I was there when Kerri Strug stuck that landing on her injured ankle.
*   [16w](https://www.facebook.com/AtlantaNewsFirst/posts/pfbid0z3r7WC4Ref9kwAUCMap1xWnBYwLRygX1TXJ6gcPTEmaSyAziC2vRiSzShHLvmyMdl?comment_id=1010528991854471&__cft__[0]=AZjSd9YzMFxYAOHE1zK-5EYIkO-EiQWieMo6cojJl5JwzksnUc8AV6hPLr2Q7gz1CzT4_wZWP-_blAXGi6Y6VRsSDrFcS5JCY21cu09hXLVevvDbBdC5XgazgQs8s9j9HHwZIYVwaBwl1WqUlGqFm5vc4x1SBAtR&__tn__=R]-R)
4

# REMEMBER THIS? One of Atlanta ’96’s... - Atlanta News First | Facebook
## Atlanta News First's Post
![Image 7](blob:http://localhost/85d8b181a20aeb64a3afc2f1c39d2480)
Rob McCullough
I was there that night. Less than 20 yards from the Kerri Strug when she made that amazing run on the pommel horse.
*   [16w](https://www.facebook.com/AtlantaNewsFirst/posts/pfbid0z3r7WC4Ref9kwAUCMap1xWnBYwLRygX1TXJ6gcPTEmaSyAziC2vRiSzShHLvmyMdl?comment_id=1720462092478763&__cft__[0]=AZjSd9YzMFxYAOHE1zK-5EYIkO-EiQWieMo6cojJl5JwzksnUc8AV6hPLr2Q7gz1CzT4_wZWP-_blAXGi6Y6VRsSDrFcS5JCY21cu09hXLVevvDbBdC5XgazgQs8s9j9HHwZIYVwaBwl1WqUlGqFm5vc4x1SBAtR&__tn__=R]-R)
Josh Stanley
On a bad ankle!!!!!
</excerpt>
### Rank 5 of 72 — 0.49
<excerpt title="I rewatched the 1996 Olympic Team Final and I have THOUGHTS">
# Comments Section
I feel like with so many of these comments, you are viewing the final with a lens looking back from the future rather than looking at the event from the lens at the time. For example, not a lot of athletes could do a Yurchenko 1.5 when it was valued at a 9.9 in 1993 and that was a huge change at the time that not everyone could easily get a 10.0 start value on vault. And two chances on vault had been the norm for many, many years before that. Having to average the vaults in the AA final for the first time that quad was again a revolutionary change. It might help to take a step back and view 1996 with a lens of how the sport had evolved since before re comments 1, 5, 6.
Regarding the NBC narrative, I wouldn’t completely blame NBC. While it is true with the benefit of hindsight that Kerri did not need to vault, that was not actually known at the time she vaulted. When Kerri vaulted, they were still waiting for Dolgopolova’s score and Russia still had Kotchetkova and Galieva to go on floor. With high scores, Russia still could have won without a hit vault from Kerri. Now Russia did not get those high scores, but there was no way to know that would happen. Here is an analysis that lays it all out quite clearly.
We are in complete agreement on how disgusting Bela and Steve are though. It’s really hard to watch.
skatelikevirtue
•5y ago
This.
6 more replies
6 more replies
6 more replies
balletbeginner
•5y ago
Vaulting off the horse was substantially harder than off the table. Vaulting is a very different event now.
[deleted]
•5y ago
2 vault attempts were the norm until the following quad or so. They're still the norm in non-elite gymnastics. You can do the same or different, and the best score counts. Honestly I would prefer seeing that at the elite level.
ArnoldRimmersBeam
•5y ago

# Comments Section
At the time Kerri vaulted, the US could very well have still lost the gold. That was a huge part of why it was so dramatic. There were two Russians still left to compete and I don't think Dolgolopova's score had flashed up when she went, since it was another minute before Kotchetkova went up. The average score the final three Russians would've needed to beat the US if Moceanu's 9.2 counted was something like 9.818, and this was after the US and Romania had racked up the 9.8s on floor. It was a much higher scoring event than vault in Atlanta. NBC are a sewer, but portraying it as Kerri needing to vault to win is an accurate reflection of how the situation would have seemed when playing out in real time.
Specific-Value-2896
•5y ago
Was it actually aired in real time? Back then (pre internet. Or at least pre the internet being ubiquitous) it was easy to get away with showing tape delays. You still want the commentary to seem live, but you could also add stuff for dramatic effect.
11 more replies
11 more replies
11 more replies
More replies
vesperholly
•5y ago
1996 still offends me because Dina Kotchetkova walked away with ZERO individual medals and Zzzzzina Gogean got 3 😡
ArnoldRimmersBeam
•5y ago
It's been 25 years and I still don't understand why she did the Yurchenko 1.5 instead of the piked barani in the AA. There's a fair chance that skill selection cost her the silver.
More replies
emr830
•5y ago
That’s just how it was back then. I started competing not long before me, that’s how the sport was at the time and it’s evolved. Some of it’s disturbing (Karolyi stuff) but 🤷‍♀️
Scatheli
•5y ago
</excerpt>

## Search 9 — query: "2012 women's all-around Olympic gold medalist"
### Rank 1 of 50 — 0.87 (passed on)
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
### Rank 2 of 50 — 0.86
<excerpt title="Gymnastics at the 2012 Summer Olympics – Women's artistic ...">
## Qualification results
| Rank | Gymnast |  |  |  |  | Total |  
| --- | --- | --- | --- | --- | --- | --- |  
|  | Gabby Douglas(USA) | 15.966 (1) | 15.733 (3) | 15.500 (1) | 15.033 (4) | **62.232** |  
|  | Viktoria Komova(RUS) | 15.466 (3) | 15.966 (2) | 15.441 (2) | 15.100 (3) | **61.973** |  
|  | Aliya Mustafina(RUS) | 15.233 (5) | 16.100 (1) | 13.633 (18) | 14.600 (6) | **59.566*** |  
| 4 | Aly Raisman(USA) | 15.900 (2) | 14.333 (=9) | 14.200 (10) | 15.133 (2) |  
| 5 | Sandra Izbașa(ROU) | 15.333 (4) | 13.900 (=17) | 14.400 (=7) | 15.200 (1) | **58.833** |  
| 6 | Deng Linlin(CHN) | 14.900 (9) | 14.266 (12) | 15.300 (3) | 13.933 (=13) | **58.399** |  
| 7 | Huang Qiushuang(CHN) | 14.916 (8) | 15.133 (5) | 14.133 (=12) | 13.933 (=13) | **58.115** |
</excerpt>
### Rank 3 of 50 — 0.86
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
Through 1956, all Olympic field hockey gold medals were won by either Great Britain or India. They had never played each other until the 1948 Olympics, when India beat the hosts 4-0.
Login | Statistics | About | Image Credits | FAQ | Feedback
© OlyMADMen 2006 — 2026
</excerpt>
### Rank 4 of 50 — 0.81
<excerpt title="On this day in history, Gabby Douglas won the all-around at the 2012 ...">
# On this day in history, Gabby Douglas won the all-around at the 2012 Olympic Games. Here she is flying on uneven bars earlier that summer! #unevenbars #gabbydouglas #usagym #usagymnastics #releaseskills | Mr. Olympics | Facebook
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
On this day in history, Gabby Douglas won the all-around at the 2012 Olympic Games. Here she is flying on uneven bars earlier that summer! #unevenbars #gabbydouglas #usagym #usagymnastics #releaseskills
Like
Comment
Share
![Image 1](blob:http://localhost/85d8b181a20aeb64a3afc2f1c39d2480)
![Image 2](blob:http://localhost/2b45e6f1a2ae097354c0b291152873d5)
1.5K
·
20 comments
·
70K views

# Video
## **Mr. Olympics**
Sunday, August 2, 2026 at 3:30 PM
August 2 ·
Follow
On this day in history, Gabby Douglas won the all-around at the 2012 Olympic Games. Here she is flyi…
See more

# Video
## Comments
Most relevant
Sarah Shakespeare
Gabby, Suni, and Shilese are the best bar workers of the latest generations of gymnasts! Gabby just flew, it was so easy for her.
*   15w
16
![Image 3](blob:http://localhost/85d8b181a20aeb64a3afc2f1c39d2480)
View all 3 replies
Ken Scott
That was a high bar show. And releases in both directions!
*   13w
2
![Image 4](blob:http://localhost/85d8b181a20aeb64a3afc2f1c39d2480)
View more comments
2 of 16

# Video
## Related videos
[ 1:00](https://www.facebook.com/61588075031279/videos/1730106301541448/?__so__=permalink&__cft__[0]=AZiX1Ni_9LQQ_p84O1AHKrB0l7am2_C1SMDJ1feOHpxlSCfCewbEh7WvfaVWCjCSRAokwNIpZY3OEew9_iKhXDl7t4epMb0Qbo2pjJdWmK1ACfZ1WXeuCZ2qzCqEE4UmrPCdtONVmJ8NTFQSIDcAfQ)
[](https://www.facebook.com/watch/61588075031279/?__cft__[0]=AZiX1Ni_9LQQ_p84O1AHKrB0l7am2_C1SMDJ1feOHpxlSCfCewbEh7WvfaVWCjCSRAokwNIpZY3OEew9_iKhXDl7t4epMb0Qbo2pjJdWmK1ACfZ1WXeuCZ2qzCqEE4UmrPCdtONVmJ8NTFQSIDcAfQ)
</excerpt>
### Rank 5 of 50 — 0.81
<excerpt title="Women's All-Around final at London 2012!">
# Women's All-Around final at London 2012!
## Chapters
### Drama on the balance beam ### Drama on the balance beam 2:06


# Women's All-Around final at London 2012!
## Chapters
### Drama on the balance beam
2:06

# Women's All-Around final at London 2012!
## Chapters
### Mustafina floor performance ### Mustafina floor performance 3:12


# Women's All-Around final at London 2012!
## Chapters
### Mustafina floor performance
3:12

# Women's All-Around final at London 2012!
## Chapters
### Douglas floor exercise ### Douglas floor exercise 4:10


# Women's All-Around final at London 2012!
## Chapters
### Douglas floor exercise
4:10

# Women's All-Around final at London 2012!
## Chapters
### Final standings and medals ### Final standings and medals 5:21


# Women's All-Around final at London 2012!
## Chapters
### Final standings and medals
5:21

# Women's All-Around final at London 2012!
## Chapters
### Olympic Games 16.7M subscribers
VideosAbout
36:17 36:17Gabby Douglas 🇺🇸 - The First African American Olympic All-Around Champion | Athlete Highlights by Olympic Games

# Women's All-Around final at London 2012!
## Video details
Date
Jul 27, 2021
Views
43,965
Likes
628
Show less
#Beijing2022#Tokyo2020

# Women's All-Around final at London 2012!
43,965 views 43K views
Jul 27, 2021
628
Download

# Women's All-Around final at London 2012!
## 54 Comments
Sort comments
Sort by
Top Show featured commentsNewest Show recent comments, including potential spam
Add a comment...

# Women's All-Around final at London 2012!
## 54 Comments
### @tatilalima2874
5 years ago
Look at Mustafina's level, she fell off the balance beam and was on the podium in an Olympics. please everyone stand up to applaud her
Show less Read more
Like
16
Dislike
Reply

# Women's All-Around final at London 2012!
## 54 Comments
### @silviokunst7630
5 years ago
Dear Olympic Channel, PLEASE upload all Tokyo 2021 Artistic and Rhythmic Gymnastics FULL REPLAYS like you did with London 2012. All the qualifications and All the finals too, please.
Show less Read more
Like
34
Dislike
Reply

# Women's All-Around final at London 2012!
## 54 Comments
### @alvinmehmedi7750
5 years ago
I want see the Tokyo 2020 olympics gymnastic
Show less Read more
Like
54
Dislike
Reply
1 reply
Hide replies
1 reply

# Women's All-Around final at London 2012!
## 54 Comments
### @M_SC
5 years ago
I watched 4 minutes before I realized it was the wrong Olympics
Show less Read more
Like
48
Dislike
Reply
1 reply
Hide replies
1 reply

# Women's All-Around final at London 2012!
## 54 Comments
### @An-eb8uk
5 years ago
Unpopular but I loved the pink leos!
Show less Read more
Like
16
Dislike
Reply

# Women's All-Around final at London 2012!
## 54 Comments
### @narasimharaju7581
5 years ago
Gabriel Douglas is awesome
Show less Read more
Like
12
Dislike
Reply
2 replies
Hide replies
2 replies
</excerpt>

For each search, read the top excerpt and the ones ranked below it, and judge whether the order is right for answering the question. An excerpt holding the answer, or a fact that leads to it, should outrank one that only repeats the query's words or covers the topic without a checkable fact. If none of the excerpts holds anything useful, that is the search's fault, not this instruction's. Find the ranking error that cost the most and write a new instruction that fixes it. Replace or compress existing text where you can; avoid making it much longer. Do not write the "Original question" or "Search query" lines; they are appended for you. Do not copy any fact, name, site or topic from these examples.

Provide the new instruction within ``` blocks.
