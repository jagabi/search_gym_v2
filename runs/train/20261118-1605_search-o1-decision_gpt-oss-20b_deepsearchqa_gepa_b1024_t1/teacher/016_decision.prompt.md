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
Of the natural sites on the UNESCO list of World Heritage in Danger, only a few sites are located in one of the original members of the United Nations. In which country is the site with the largest reported area according to Protected Planet?

## Expected answer
Mexico

## Grade 0.00

## Search 1 — query: "original members of the United Nations 51 founding members 1945 list"
### Rank 1 of 146 — 0.61 (passed on)
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
### Rank 2 of 146 — 0.58
<excerpt title="Member states of the United Nations">
The UN officially came into existence on 24 October 1945, after ratification of the United Nations Charter by the five permanent members of the United Nations Security Council (the Republic of China, France, the Soviet Union, the United Kingdom, and the United States) and a majority of the other signatories.[[12]](https://en.wikipedia.org/wiki/Member_states_of_the_United_Nations#cite_note-13) A total of 51 original members (or founding members) joined that year; 50 of them signed the Charter at the United Nations Conference on International Organization in San Francisco on 26 June 1945, while Poland, which was not represented at the conference, signed it on 15 October 1945.[[13]](https://en.wikipedia.org/wiki/Member_states_of_the_United_Nations#cite_note-14)[[14]](https://en.wikipedia.org/wiki/Member_states_of_the_United_Nations#cite_note-originalmembers-15)

The original members of the United Nations were: France (then the Provisional Government), Russia (then the Soviet Union), China (then Republic of China), the United Kingdom, the United States—these first five forming the Security Council—Argentina, Australia, Belarus (then the Byelorussian SSR), Belgium, Bolivia, Brazil (then the Vargas Era Brazil), Canada, Chile (then the 1925–73 Presidential Republic), Colombia, Costa Rica, Cuba (then the 1902–59 Republic), Czechoslovakia (then the Third Republic), Denmark, the Dominican Republic, Ecuador, Egypt (then the Kingdom of Egypt), El Salvador, Ethiopia (then the Ethiopian Empire), Greece (then the Kingdom of Greece), Guatemala, Haiti (then the 1859–1957 Republic), Honduras, India (then the British Raj), Iran (then the Imperial State of Iran), Iraq (then the Kingdom of Iraq), Lebanon, Liberia, Luxembourg, Mexico, the Netherlands, New Zealand (then the Dominion of New Zealand), Nicaragua, Norway, Panama, Paraguay, Peru, the Philippines (then the Commonwealth), Poland (then the Provisional Government of National Unity), Saudi Arabia, South Africa (then the Union of South Africa), Syria (then the Mandatory Republic), Turkey, Ukraine (then the Ukrainian SSR), Uruguay, Venezuela and Yugoslavia (then the Democratic Federal Yugoslavia).[[14]](https://en.wikipedia.org/wiki/Member_states_of_the_United_Nations#cite_note-originalmembers-15)
Among the original members, 49 are either still UN members or had their memberships in the UN continued by a successor state_(see table below)_; for example, the membership of the Soviet Union was continued by the Russian Federation after its dissolution _(see the section Former members: Union of Soviet Socialist Republics)_. The other two original members, Czechoslovakia and Yugoslavia (i.e., the Socialist Federal Republic of Yugoslavia), had been dissolved and their memberships in the UN not continued from 1992 by any one successor state _(see the sections Former members: Czechoslovakia and Former members: Yugoslavia)_.[[14]](https://en.wikipedia.org/wiki/Member_states_of_the_United_Nations#cite_note-originalmembers-15)
</excerpt>
### Rank 3 of 146 — 0.57
<excerpt title="Where can I find information about the founding members of the UN?">
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
### Rank 4 of 146 — 0.57
<excerpt title="Where can I find information about the founding members of the UN?">
## Founding Member States
| Colombia | 26 June 1945 | 5 Nov. 1945 |  |  
| Costa Rica | 26 June 1945 | 2 Nov. 1945 |  |  
| Ecuador | 26 June 1945 | 21 Dec. 1945 |  |  
| Ethiopia | 26 June 1945 | 13 Nov. 1945 |  |  
| Greece | 26 June 1945 | 25 Oct. 1945 |  |  
| Guatemala | 26 June 1945 | 21 Nov. 1945 |  |  
| Honduras | 26 June 1945 | 17 Nov. 1945 |  |  
| India | 26 June 1945 | 30 Oct. 1945 |  |  
| Iraq | 26 June 1945 | 21 Dec. 1945 |  |  
| Liberia | 26 June 1945 | 2 Nov. 1945 |  |  
| Mexico | 26 June 1945 | 7 Nov. 1945 |  |  
| Netherlands | 26 June 1945 | 10 Dec. 1945 | Netherlands (Kingdom of the) |  
| Norway | 26 June 1945 | 27 Nov. 1945 |  |  
| Panama | 26 June 1945 | 13 Nov. 1945 |  |  
| Peru | 26 June 1945 | 31 Oct. 1945 |  |  
| Union of South Africa | 26 June 1945 | 7 Nov. 1945 | South Africa |  
| Uruguay | 26 June 1945 | 18 Dec. 1945 |  |  
| Venezuela | 26 June 1945 | 15 Nov. 1945 | Bolivarian Republic of Venezuela |
</excerpt>
### Rank 5 of 146 — 0.56
<excerpt title="Member states of the United Nations">
In principle, only sovereign states can become UN members,[[8]](https://en.wikipedia.org/wiki/Member_states_of_the_United_Nations#cite_note-United_Nations-9) and currently, all UN members are sovereign states. Although five members were not sovereign when they joined the UN, they all subsequently became fully independent between 1946 and 1991.[[9]](https://en.wikipedia.org/wiki/Member_states_of_the_United_Nations#cite_note-10) Because a state can only be admitted to membership in the UN by the approval of the Security Council and the General Assembly,[[10]](https://en.wikipedia.org/wiki/Member_states_of_the_United_Nations#cite_note-11)[[8]](https://en.wikipedia.org/wiki/Member_states_of_the_United_Nations#cite_note-United_Nations-9)a number of states that are considered sovereign according to the Montevideo Convention are not members of the UN. This is because the UN does not consider them to possess sovereignty, mainly due to the lack of international recognition or due to opposition from one of the permanent members.
In addition to the member states, the UN also invites non-member states to become observer states at the UN General Assembly,[[11]](https://en.wikipedia.org/wiki/Member_states_of_the_United_Nations#cite_note-12) allowing them to participate and speak in General Assembly meetings, but not vote. Observers are generally intergovernmental organizations and international organizations and entities whose statehood or sovereignty is not precisely defined.
The world in 1945, after World War II. In light blue, the founding members of the United Nations. In dark blue, protectorates and territories of the founding members.

The UN officially came into existence on 24 October 1945, after ratification of the United Nations Charter by the five permanent members of the United Nations Security Council (the Republic of China, France, the Soviet Union, the United Kingdom, and the United States) and a majority of the other signatories.[[12]](https://en.wikipedia.org/wiki/Member_states_of_the_United_Nations#cite_note-13) A total of 51 original members (or founding members) joined that year; 50 of them signed the Charter at the United Nations Conference on International Organization in San Francisco on 26 June 1945, while Poland, which was not represented at the conference, signed it on 15 October 1945.[[13]](https://en.wikipedia.org/wiki/Member_states_of_the_United_Nations#cite_note-14)[[14]](https://en.wikipedia.org/wiki/Member_states_of_the_United_Nations#cite_note-originalmembers-15)
</excerpt>

## Search 2 — query: "UNESCO World Heritage in Danger natural sites list 2024 protected planet area largest"
### Rank 1 of 244 — 0.74 (passed on)
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
### Rank 2 of 244 — 0.72
<excerpt title="List of World Heritage in Danger">
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

The site is located a few kilometers southwest of Jerusalem, in the central highlands between Nablus and Hebron. The landscape of Battir includes a series of cultivated valleys, known as widian, characterized by stone terraces, some of which are used for growing grapes and olive trees for the market. The development of terraced agriculture and irrigation in such a mountainous area is supported by a network of channels supplied by underground water sources. A traditional distribution system is used to collect water from the springs near the village of Battir and supply it to each household via a network of canals.
Palestine: Land of Olives and Vines – Cultural Landscape of Southern Jerusalem, Battir
Area of the heritage property: 349 hectares. Buffer zone area: 624 hectares.
25. Hebron/Al-Khalil Old Town
Country: Palestine. Inscribed in 2017 as a cultural heritage site and a World Heritage in Danger site. Criteria: (ii)(iv)(vi)
26
Hebron is a city in the West Bank region of Palestine and a holy city in Judaism second only to Jerusalem, located 30 kilometers south of Jerusalem at an altitude of 930 meters. The Old City of Hebron is characterized by narrow, winding streets, flat-roofed stone houses, and ancient markets. The most famous historical site in Hebron is the Cave of the Patriarchs, considered sacred by Judaism, Christianity, and Islam. The neighborhoods within the old town are divided according to ethnicity, religion, and occupation, with rooms in the buildings arranged in a tree-like pattern. Both the architectural style and interior decorations are unique.
Between 1250 and 1517, the use of local limestone was the building material for the construction of the ancient city of Hebron. The heritage center of the city is the site of Abraham, with a structure built in the 1st century to protect the tombs of Abraham, Isaac, and their families. This place became a pilgrimage site for three religions: Judaism, Christianity, and Islam. The town is situated at the crossroads of trade routes linking southern Palestine, Sinai, eastern Jordan, and the north of the Arabian Peninsula. Although the subsequent Ottoman period (1517-1917) saw the expansion of the town and the addition of many new buildings.
Hebron/Al-Khalil Old Town
</excerpt>
### Rank 3 of 244 — 0.70
<excerpt title="List of World Heritage in Danger">
The site is located a few kilometers southwest of Jerusalem, in the central highlands between Nablus and Hebron. The landscape of Battir includes a series of cultivated valleys, known as widian, characterized by stone terraces, some of which are used for growing grapes and olive trees for the market. The development of terraced agriculture and irrigation in such a mountainous area is supported by a network of channels supplied by underground water sources. A traditional distribution system is used to collect water from the springs near the village of Battir and supply it to each household via a network of canals.
Palestine: Land of Olives and Vines – Cultural Landscape of Southern Jerusalem, Battir
Area of the heritage property: 349 hectares. Buffer zone area: 624 hectares.
25. Hebron/Al-Khalil Old Town
Country: Palestine. Inscribed in 2017 as a cultural heritage site and a World Heritage in Danger site. Criteria: (ii)(iv)(vi)
26
Hebron is a city in the West Bank region of Palestine and a holy city in Judaism second only to Jerusalem, located 30 kilometers south of Jerusalem at an altitude of 930 meters. The Old City of Hebron is characterized by narrow, winding streets, flat-roofed stone houses, and ancient markets. The most famous historical site in Hebron is the Cave of the Patriarchs, considered sacred by Judaism, Christianity, and Islam. The neighborhoods within the old town are divided according to ethnicity, religion, and occupation, with rooms in the buildings arranged in a tree-like pattern. Both the architectural style and interior decorations are unique.
Between 1250 and 1517, the use of local limestone was the building material for the construction of the ancient city of Hebron. The heritage center of the city is the site of Abraham, with a structure built in the 1st century to protect the tombs of Abraham, Isaac, and their families. This place became a pilgrimage site for three religions: Judaism, Christianity, and Islam. The town is situated at the crossroads of trade routes linking southern Palestine, Sinai, eastern Jordan, and the north of the Arabian Peninsula. Although the subsequent Ottoman period (1517-1917) saw the expansion of the town and the addition of many new buildings.
Hebron/Al-Khalil Old Town

Area of the heritage property: 20.6 hectares. Buffer zone area: 152.2 hectares.
26. Fortifications on the Caribbean Side of Panama: Portobelo-San Lorenzo
State Party: Panama. Inscribed as a Cultural Heritage site in December 1980. Inscribed on the List of World Heritage in Danger in 2012. Criteria for Inscription: (i)(iv)
27
As excellent examples of military architecture from the 17th and 18th centuries, these Panamanian fortresses on the Caribbean coast formed part of the defensive system constructed by the Spanish Crown to protect transatlantic trade.
Fortifications on the Caribbean Coast of Panama
27. Chan Chan Archaeological Zone
State Party: Peru. Inscribed as a Cultural Heritage site and simultaneously placed on the List of World Heritage in Danger in December 1986. Criteria for Inscription: (i)(iii)
28
Chan Chan was the capital of the Chimor Kingdom, which reached its zenith in the 15th century before being absorbed by the
Inca Empire
. The layout of this vast pre-Columbian city reflects a strict political and social strategy, divided into nine 'citadels' or 'palace compounds', each an independent unit.
Chan Chan Archaeological Zone
Core Zone: 1,415 hectares.
28. Niokolo-Koba National Park
State Party: Senegal. Inscribed as a Natural Heritage site in December 1981. Inscribed on the List of World Heritage in Danger in 2007. Criteria for Inscription: (x)
Niokolo-Koba National Park is located in a well-watered area along the Gambia River. Its gallery forests and savannas are home to a wide variety of wildlife, including the largest antelope in the world, the Derby eland, as well as chimpanzees, lions, leopards, and a significant population of elephants, along with numerous birds, reptiles, and amphibians.
Niokolo-Koba National Park
Core Zone: 913,000 hectares.
29. Medieval Monuments in Kosovo
</excerpt>
### Rank 4 of 244 — 0.70
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
### Rank 5 of 244 — 0.69
<excerpt title="List of World Heritage in Danger">
Area of the heritage property: 20.6 hectares. Buffer zone area: 152.2 hectares.
26. Fortifications on the Caribbean Side of Panama: Portobelo-San Lorenzo
State Party: Panama. Inscribed as a Cultural Heritage site in December 1980. Inscribed on the List of World Heritage in Danger in 2012. Criteria for Inscription: (i)(iv)
27
As excellent examples of military architecture from the 17th and 18th centuries, these Panamanian fortresses on the Caribbean coast formed part of the defensive system constructed by the Spanish Crown to protect transatlantic trade.
Fortifications on the Caribbean Coast of Panama
27. Chan Chan Archaeological Zone
State Party: Peru. Inscribed as a Cultural Heritage site and simultaneously placed on the List of World Heritage in Danger in December 1986. Criteria for Inscription: (i)(iii)
28
Chan Chan was the capital of the Chimor Kingdom, which reached its zenith in the 15th century before being absorbed by the
Inca Empire
. The layout of this vast pre-Columbian city reflects a strict political and social strategy, divided into nine 'citadels' or 'palace compounds', each an independent unit.
Chan Chan Archaeological Zone
Core Zone: 1,415 hectares.
28. Niokolo-Koba National Park
State Party: Senegal. Inscribed as a Natural Heritage site in December 1981. Inscribed on the List of World Heritage in Danger in 2007. Criteria for Inscription: (x)
Niokolo-Koba National Park is located in a well-watered area along the Gambia River. Its gallery forests and savannas are home to a wide variety of wildlife, including the largest antelope in the world, the Derby eland, as well as chimpanzees, lions, leopards, and a significant population of elephants, along with numerous birds, reptiles, and amphibians.
Niokolo-Koba National Park
Core Zone: 913,000 hectares.
29. Medieval Monuments in Kosovo

State Party: Serbia Inscribed as a cultural heritage site in July 2004. Inscribed on the List of World Heritage in Danger in 2006. Criteria for inscription: (ii)(iii)(iv)
29
The Medieval Monuments in Kosovo comprise four components, which present the zenith of Byzantine and Romanesque ecclesiastical culture, which developed in the Balkans between the 13th and the 17th centuries. Their wall paintings exhibit a distinctive style. The Patriarchate of Peć Monastery complex, located on the outskirts of Peć, consists of a group of four churches with domed roofs decorated with murals. The 13th-century frescoes of the Church of the Holy Apostles are an exceptional example of the so-called Palaiologan Renaissance. The frescoes in the Church of the Virgin of Ljeviša, dating from the early 14th century, mark a new style, known as the Palaiologan Renaissance, which combines influences from the Eastern Orthodox Byzantine tradition with those of Western Romanesque art. The style played a decisive role in the subsequent development of art in the Balkans.
Medieval Monuments in Kosovo
Core zone: 2.88 hectares Buffer zone: 115 hectares
30. East Rennell
State Party: Solomon Islands Inscribed as a natural heritage site in December 1998. Inscribed on the List of World Heritage in Danger in 2013. Criteria for inscription: (ix)
30
East Rennell is the southern third of Rennell Island, the southernmost island in the Solomon Islands group in the western Pacific. Rennell Island is 86 km long and 15 km wide, and is the world's largest raised coral atoll. The site covers approximately 37,000 hectares of land and a marine area extending 3 nautical miles. The most significant feature of the island is Lake Tegano, a former lagoon on the atoll. This 15,500-hectare lake, the largest in the insular Pacific, is brackish and contains many rugged limestone islands and endemic species. Much of the island is covered with dense forest, averaging 20 meters in height. Combined with the strong effects of frequent cyclones, the site is a true natural laboratory for scientific study. The island is under customary ownership and management.
</excerpt>

## Search 3 — query: "UNESCO natural World Heritage in Danger list 2026 protected planet area"
### Rank 1 of 75 — 0.67 (passed on)
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
### Rank 2 of 75 — 0.31
<excerpt title="Pyrénées - Mont Perdu">
# Pyrénées - Mont Perdu | Protected Planet
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

# Pyrénées - Mont Perdu
145590  SITE ID
306.39 km²  Reported Area
Type  Terrestrial and Inland Waters Protected Areas
Location France, Spain
Read an assessment of this site by visiting the IUCN World Heritage Outlook Link

# Pyrénées - Mont Perdu
## citation
UNEP-WCMC (2026). Protected Area Profile for Pyrénées - Mont Perdu from the World Database on Protected Areas, November 2026. Available at: www.protectedplanet.net

# Pyrénées - Mont Perdu
## citation
### Explore
ResourcesWDPCA

# Pyrénées - Mont Perdu
## citation
### General Info
AboutLegalPrivacy policy

# Pyrénées - Mont Perdu
## citation
### Follow us


# Pyrénées - Mont Perdu
## citation
### Get in touch
[protectedareas@unep-wcmc.org](mailto:protectedareas@unep-wcmc.org "Email: protectedareas@unep-wcmc.org")
©ProtectedPlanet 2014-2026. All rights reserved
Downloads
Citation  
UNEP-WCMC and IUCN (2026), Protected Planet: The World Database on Protected and Conserved Areas (WDPCA) [Online], November 2026, Cambridge, UK: UNEP-WCMC and IUCN. Available at: www.protectedplanet.net.
</excerpt>
### Rank 3 of 75 — 0.17
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
### Rank 4 of 75 — 0.11
<excerpt title="Natural World Heritage - resource">
Issues brief
*   **Natural World Heritage sites** are **globally recognised as the most significant protected areas on Earth**.  
*   These sites provide life-supporting benefits to millions of people –**90% of sites provide jobs**, **two-thirds are crucial sources of water** and about **half help prevent natural disasters** such as floods or landslides.  
*   Natural World Heritage sites are **under increasing pressure from climate change, infrastructure development, mining, poaching** and other threats.  
*   To protect sites from threats, **investment in their protection and management** is urgently needed. Closely **monitoring the status of sites, World Heritage-specific biodiversity targets, and adopting IUCN Green List standards** for site management can also help.  
*   **These sites are a litmus test** for our ability as a conservation community to protect biodiversity and pass on nature’s treasures to the next generation.
November 2018

### What is the issue?
One in five (23%) sites on the UNESCO World Heritage List are natural sites, most often protected areas such as national parks or nature reserves. Natural World Heritage sites are **globally recognised as the planet’s most significant protected areas**. There are 252 natural World Heritage sites around the globe, including iconic places such as Australia’s Great Barrier Reef, Yellowstone National Park in the United States, Virunga National Park in the Democratic Republic of the Congo or the Tropical Rainforest Heritage of Sumatra in Indonesia. Natural World Heritage sites account for 8% of the total surface covered by all 230,000+ protected areas worldwide.
Almost every country has signed the World Heritage Convention, committing to the best level of protection for these sites. Yet**natural World Heritage sites are under increasing pressure. Invasive species, climate change and the negative impacts of tourism are currently the three most significant threats**to natural World Heritage, according to the IUCN World Heritage Outlook, the first ever assessment of all listed natural sites.
**Climate change is the fastest growing threat to natural World Heritage**, with the number of sites highly threatened by climate change almost doubling in the three years between 2014 and 2017. Coral reefs and glaciers are among the most affected ecosystems. In 2016, up to 85% of all reefs surveyed had been impacted by climate change. The Great Barrier Reef, the largest reef on Earth, has suffered widespread bleaching due to the increase in global sea surface temperature. Retreating glaciers threaten the very reason why Tanzania’s Kilimanjaro National Park, home to Africa’s highest peak, is on the World Heritage List. Climate change is also by far the largest potential threat to natural World Heritage, meaning more sites will likely suffer impacts in the near future.
IUCN World Heritage Outlook 2 (2017)

### What is the issue?
**Pressure on natural World Heritage from planned infrastructure is also increasing**. Major development such as the construction of roads, dams, tourism facilities, mining and oil and gas projects is among the top potential threats. For instance, Bangladesh's Sundarbans, a vast mangrove forest home to the royal Bengal tiger, could be severely altered by impacts of the Rampal coal-fired power plant proposed near the site. The proposed Stiegler’s Gorge dam could cause irreversible damage to important habitats in Tanzania's Selous Game Reserve, home to the Critically Endangered black rhinoceros.
**The protection and management of natural World Heritage are becoming less effective**. In 2017, fewer than half (48%) of the sites were assessed as having effective protection and management, down from 54% in 2014. Lack of guarantee for long-term finance is the most challenging aspect of protection and management – an issue assessed as being of concern for 118 natural World Heritage sites.
Growing threats and declining protection and management present a worrying combination for natural World Heritage sites. If natural World Heritage sites are not adequately conserved, their unique values could be irreversibly damaged or lost.
IUCN World Heritage Outlook 2 (2017)
</excerpt>
### Rank 5 of 75 — 0.10
<excerpt title="Natural World Heritage">
# Natural World Heritage
## Nature’s most precious gifts
Natural World Heritage sites are critical for the conservation of ecosystem integrity and biodiversity. While they make up less than 1% of the Earth’s surface, they harbor more than 1/5 of mapped global species richness. This includes over 75,000 species of plants, and over 30,000 species of mammals, birds, fishes, reptiles and amphibians. These sites also represent a safe haven for some of the most threatened species on Earth. They are estimated to protect over 20,000 globally threatened species, including some of the last individuals of many iconic species. Today, up to 1/3 of remaining elephants, tigers and pandas can be found in these sites, as well as at least 1 in 10 great apes, giraffes, lions and rhinos. For some species on the brink of extinction, World Heritage sites have become the last line of defense. They are home to all remaining Javan rhinos, vaquitas (the world's smallest cetacean) and pink iguanas, as well as more than half of all Sumatran rhinos, Sumatran orangutans and mountain gorillas.
Millions of people are directly dependent on the countless benefits and services these sites can provide, supporting livelihoods and wellbeing. Over 90% of listed natural sites create jobs and provide income from tourism and recreation. Two-thirds of natural sites are crucial sources of water, and about half help prevent hazards such as floods or landslides. They also have a central role in climate regulation and carbon sequestration as World Heritage forests absorb approximately 190 million tons of CO2 each year (equivalent to half the United Kingdom’s annual CO2 emissions from fossil fuels). Marine and coastal sites are also critical to mitigating climate impacts storing 1.3 billion tons of carbon (known as blue carbon) in seagrass meadows, tidal marshes and mangroves, representing 15% of global blue carbon assets.

# Natural World Heritage
## A threatened paradise
Natural World Heritage sites account for around 8% of the total surface area covered by all 280,000+ terrestrial and marine protected areas worldwide. Yet they are under increasing pressure. According to IUCN, the official advisory body on nature under the World Heritage Convention, climate change, invasive species and the negative impacts of tourism are currently the three most significant threats. Other major threats include poaching, planned infrastructure such as roads, dams, mining, oil and gas projects, and conflicts.
To date 16 natural World Heritage sites are on the List of World Heritage in Danger. Climate change is however the fastest growing threat to natural World Heritage, with the number of sites highly threatened by climate change almost doubling in the last decade. Every 1°C increase in temperature could double the number of species exposed to dangerous climate conditions. Forests, coral reefs and glaciers are among some of the most affected ecosystems. Wetlands, low-lying deltas, permafrost and fire sensitive ecosystems are also affected.
Almost 2/3 of forests found in World Heritage sites are threatened by land use pressures and climate-related hazards such as wildfires. A first global scientific assessment of greenhouse gas emissions and sequestration in World Heritage forests revealed that at least 10 sites were net carbon sources since 2000 and that one single climate-related hazard could make a forest site from a carbon sink to source.
World Heritage-listed coral reefs, such as theGreat Barrier Reef (Australia)(the world's largest coral reef system), theAldabra Atoll (Seychelles)in the Indian Ocean (the world's second-largest coral atoll) and the Belize Barrier Reef (Belize)in the Atlantic (the largest barrier reef in the northern hemisphere) have been affected by devastating mass coral bleaching events over the past decades. A first global scientific assessment of the impacts of climate change on World Heritage coral reefs revealed that by 2040, all World Heritage-listed coral reefs could face annual severe bleaching events at least twice a decade.
</excerpt>

## Search 4 — query: "UNESCO World Heritage in Danger natural sites list 2024"
### Rank 1 of 94 — 0.65 (passed on)
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
### Rank 2 of 94 — 0.39
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
### Rank 3 of 94 — 0.33
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
### Rank 4 of 94 — 0.29
<excerpt title="Chart: Where UNESCO World Heritage Is In Danger">
UNESCO World Heritage
A look at the current list of cultural UNESCO World Heritage sites in danger shows that most are located in war zones and unstable states, like Syria, Lebanon, Afghanistan, Iraq, Yemen, Venezuela, Libya, Mali, Ukraine and Palestine. The latter in 2024 saw one site added - the Saint Hilarion Monastery or Tell Umm Amer. One of the earliest monastic sites in the Middle East which dates back to the 4th century is located in a coastal region in the Gaza strip and is therefore currently located in an active conflict zone.
In 2023, the historic city centers of Ukrainian cities Lviv, Kiev and Odessa were added to the list due to the ongoing war there. Other World Heritage monuments are threatened by construction projects, like historic sites in Egypt and Uzbekistan as well as the Vienna historic center, where UNESCO is taking issue with the construction of a large new hotel. Increased development in the city was also the reason why Liverpool in the UK lost its World Heritage status in 2021.
Venice and its lagoon was not added to the World Heritage in danger list after having been nominated last year. It would have been the only cultural heritage entry where climate change was having a significant impact. Nepalese pilgrimage site Lumbibi, known as the birthplace of the Buddha, was recommended for inclusion due to disrepair, but was also ultimately not included. The same is true for UK site Stonehenge, which is in the eyes of the UNESCO threatened by the construction of a new motorway tunnel. After having received a warning in 2023, the site was recommended for in-danger status this year but the decision was postponed until 2026. Among the sites receiving grave warnings in 2024 was the historic city of Budapest, Hungary, three natural sites in Russia including Lake Baikal, one Europe's last primeval forests, Bialowieza of Eastern Poland and Belarus as well as another UK property, Derwent Valley Mills in Derbyshire in Central England - due to construction planned within the 18th-century cotton spinning site.
Description
This chart shows cultural UNESCO World Heritage sites listed as "in danger" and year they were added to that list.
Report
Download Chart
URL to be used as reference link:
HTML code to embed chart
Can I integrate infographics into my blog or website?

Yes, Statista allows the easy integration of many infographics on other websites. Simply copy the HTML code that is shown for the relevant statistic in order to integrate it. Our standard is 660 pixels, but you can customize how the statistic is displayed to suit your site by setting the width and the display size. Please note that the code must be integrated into the HTML code (not only the text) for WordPress pages and other CMS sites.

## FAQ
*   The Statista "Chart of the Day", made available under the Creative Commons License CC BY-ND 3.0, may be used and displayed without charge by all commercial and non-commercial websites. Use is, however, only permitted with proper attribution to Statista. When publishing one of these graphics, please include a backlink to the respective infographic URL. More Information

*   The Statista "Chart of the Day" currently focuses on two sectors: "Media and Technology", updated daily and featuring the latest statistics from the media, internet, telecommunications and consumer electronics industries; and "Economy and Society", which current data from the United States and around the world relating to economic and political issues as well as sports and entertainment.

*   For individual content and infographics in your Corporate Design, please visit our agency website www.statista.design

## FAQ
### Statista Content & Design
Need infographics, animated videos, presentations, data research or social media charts?
More Information
</excerpt>
### Rank 5 of 94 — 0.23
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

## Search 5 — query: "Protected Planet Great Barrier Reef area"
### Rank 1 of 30 — 0.84 (passed on)
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
### Rank 2 of 30 — 0.74
<excerpt title="Great Barrier Reef Coast">
# Great Barrier Reef Coast | Protected Planet
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

# Great Barrier Reef Coast
555548204  SITE ID
62755.69 km²  Reported Area
Type  Marine and Coastal Protected Areas
Location Australia
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

# Great Barrier Reef Coast
## Choose a Parcel
The marine protected area consists of different parcels or zones. Please select from the dropdown to see descriptive data for each parcel.
Parcel ID
555548204_1

# Great Barrier Reef Coast
## Attributes
*   Name Great Barrier Reef Coast  
*   English Name Great Barrier Reef Coast  
*   English Designation Marine Park  
*   IUCN Management Category Ia  
*   Status Designated  
*   Type of Designation National  
*   Status Year 2004  
*   Governance Type Sub-national ministry or agency  
*   Governance Subtype Not Applicable  
*   Management Authority AU-QLD_DES  
*   Management Plan Not Reported  
*   Ownership Type Not Reported  
*   Ownership Subtype Not Applicable  
*   International Criteria Not Applicable  
*   Inland Waters Not Applicable  
*   Supplementary Information Not Applicable
</excerpt>
### Rank 3 of 30 — 0.71
<excerpt title="Managing and protecting the Great Barrier Reef Marine Park">
# We are the Reef Authority | Managing and protecting the Great Barrier Reef Marine Park - YouTube
## Climate change
•
•
United Nations • Climate change refers to long-term shifts in temperatures and weather patterns. Human activities have been the main driver of climate change, primarily due to the burning of fossil fuels like coal, oil and gas.

# We are the Reef Authority | Managing and protecting the Great Barrier Reef Marine Park
Great Barrier Reef Marine Park Authority
Great Barrier Reef Marine Park Authority
2.83K subscribers
Subscribe
Subscribed
3
Download
1.9K views 6mo ago#GreatBarrierReef#ReefAuthority#LovetheReef
1,995 views • Apr 27, 2026 • #GreatBarrierReef #ReefAuthority #LovetheReef
For over 50 years, the Great Barrier Reef Marine Park Authority (the Reef Authority) has had the privilege of managing the Great Barrier Reef World Heritage Area. Covering 344,400 square kilometres in area, the Great Barrier Reef Marine Park is one of the planet’s most diverse and iconic ecosystems. As Australia’s lead managers of the Great Barrier Reef, we work with government, industry and the …more
more

# We are the Reef Authority | Managing and protecting the Great Barrier Reef Marine Park
## Featured places


# Great Barrier Reef Marine Park #### National park 4.7(3.5K)
Transcript
Follow along using the transcript.
Show transcript

# Great Barrier Reef Marine Park #### National park 4.7(3.5K)
### Great Barrier Reef Marine Park Authority 2.83K subscribers
VideosAbout Instagram Facebook Twitter

# Great Barrier Reef Marine Park #### National park 4.7(3.5K)
## Video details
Date
Apr 27, 2026
Views
1,995
Likes
3
How this was made
Auto-dubbed
Show less
#GreatBarrierReef#ReefAuthority#LovetheReef

# We are the Reef Authority | Managing and protecting the Great Barrier Reef Marine Park
1,995 views 1.9K views
Apr 27, 2026
3
Download
Comments are turned off. Learn more

# We are the Reef Authority | Managing and protecting the Great Barrier Reef Marine Park
## In this video
Transcript

# We are the Reef Authority | Managing and protecting the Great Barrier Reef Marine Park
## We are the Reef Authority | Managing and protecting the Great Barrier Reef Marine Park
Great Barrier Reef Marine Park Authority
Great Barrier Reef Marine Park Authority
3 Likes
1.9K Views
Apr 27 2026
For over 50 years, the Great Barrier Reef Marine Park Authority (the Reef Authority) has had the privilege of managing the Great Barrier Reef World Heritage Area. Covering 344,400 square kilometres in area, the Great Barrier Reef Marine Park is one of the planet’s most diverse and iconic ecosystems. As Australia’s lead managers of the Great Barrier Reef, we work with government, industry and the community to protect this great natural wonder. The Great Barrier Reef Marine Park Act 1975 guides our management, balancing environmental protection with reasonable activities, such as tourism, shipping and fishing. We are Reef stewards, compliance officers, community educators, government advisors, data analysts, strategic policymakers, and science-led managers championing the Reef. Using the best available science, we work to protect values, reduce threats, and improve the current and long-term outlook for the Reef and the communities that depend on it. A range of regulatory tools enable us to manage multiple activities in the Marine Park, including our Zoning Plan, plans of management, permits and policies, as well as a range of partnerships and management arrangements. We are part of the Climate Change, Energy, the Environment and Water portfolio reporting directly to the Australian Government’s Minister for the Environment. Our vision A healthy Great Barrier Reef for future generations. Our purpose Provide for the long-term protection, ecologically sustainable use, understanding and enjoyment of the Great Barrier Reef for all Australians and the international community through the care and development of the Marine Park. Find out more about the Reef Authority, and the Marine Park here - www.gbrmpa.gov.au #ReefAuthority#GreatBarrierReef#LovetheReef…...more
...more Show less

# We are the Reef Authority | Managing and protecting the Great Barrier Reef Marine Park
## Featured places


# Great Barrier Reef Marine Park #### National park 4.7(3.5K)
Transcript
Follow along using the transcript.
Show transcript
</excerpt>
### Rank 4 of 30 — 0.65
<excerpt title="Great Barrier Reef: Why It Matters & How We Can Protect It">
# Great Barrier Reef: Why It Matters & How We Can Protect It
*   Support Us  
*   Get involved  
*   What we do  
*   About us
Back
*   Support Us
Donate
*   Make a Donation  
*   Give in your will  
*   Shop for gifts and apparel  
*   More ways to give
Adopt
*   Koala  
*   Platypus  
*   Whale  
*   Glossy Black Cockatoo  
*   Tiger  
*   All species
Partner with us
*   Partnerships  
*   Workplace Giving
Back
*   Get involved
Community involvement
*   Fundraise for WWF  
*   Join an Event  
*   Livestream
Reduce your impact
*   Calculate Your Ecological Footprint  
*   Reduce Your Plastic Use  
*   Change The Way You Live  
*   Scat Chat with WWF
Take Action
*   We All Need Trees  
*   Protect Aussie Wildlife  
*   Protect our Oceans  
*   Plastic Free July
Back
*   What we do
OUR STRATEGY
*   Regenerate Nature by 2030  
*   Regenerative Sky  
*   Regenerative Country  
*   Regenerative Saltwater  
*   Inclusive Conservation
Where we work
*   Climate  
*   Species  
*   Oceans  
*   Caring on Country  
*   Climate Nature and Communities
Resources
*   Living Planet Report  
*   Resource Library  
*   Annual Report  
*   Nature Wallpapers
Back
*   About us
Latest stories
*   News  
*   Blogs
About WWF-Australia
*   History  
*   Leaders  
*   Jobs  
*   Contact WWF  
*   FAQ  
*   Policies
VISIT OUR SHOPADOPT NOWDONATE NOW
Clown fish swimming in the Great Barrier Reef, Queensland, Australia. © Shutterstock / Andrey Nosik / WWF

# Great Barrier Reef
The Great Barrier Reef is the world's largest coral reef system and a UNESCO World Heritage Site. Spanning 344,400km², it's home to thousands of species and supports 60,000 jobs. But climate change, pollution, and overfishing threaten its survival. Here's what you need to know—and how you can help WWF‑Australia protect it.
BREAKING NEWS
The fourth global mass bleaching event was confirmed, the second in 10 years. This is the fifth mass bleaching event the Great Barrier Reef has experienced in just eight years, and the 2024 event is feared to be the most widespread and damaging to date.
“The coral crisis is a climate crisis. We must act urgently to stop burning fossil fuels or we will lose coral reefs worldwide.” - Pepe Clarke, WWF Oceans Practice Leader.
Read the full story here.

# Great Barrier Reef
## Quick Summary
*   **Size:**344,400km²—visible from space

*   **Biodiversity:**1,600+ fish species, 133 sharks and rays, 30 whales and dolphins, 6 of 7 marine turtle species

*   **Age:**Began taking shape 8,000 years ago after the last ice age

*   **Economic Value:**$6.4 billion annually, 60,000 jobs

*   **Cultural Significance:**70 Traditional Custodian groups whose Sea Country includes the Great Barrier Reef Marine Park

*   **Main Threats:**Climate change, coral bleaching, pollution, and overfishing

*   **WWF Actions:**Net-Free Reef campaign, plastic bans, Regenerative Saltwater plan

*   **How You Can Help:**Reduce plastic, advocate for climate action, support WWF programs
</excerpt>
### Rank 5 of 30 — 0.62
<excerpt title="Great Barrier Reef Marine Park">
The Great Barrier Reef Marine Park is located on the northeastern coast of Australia spanning over 2300 Kilometers of coast, covering over 14 degrees latitude, and expanding from 60 Kilometers to 250 Kilometers from the coast line. The park covers 344,400 km2 in area with the average depth of 35 meters, and its deepest depth to be over 2000 meters, see the below map from MPAtlas for more geographical information. The Great Barrier Reef is known to be the largest living structure on the planet with thousands of different species it makes it one of the most complex natural ecosystems in the world. There are 14 coastal ecosystems that are important to the function of the Reef: coral reefs, lagoon floor, islands, open water, seagrasses, coastline, estuaries, freshwater wetlands, forested floodplain, heath and shrublands, grass and sedgelands, woodlands, forests and rainforests. These coastal ecosystems provide the interconnections that support the physical, biological and biogeochemical process that underpin the ecosystem health of the Great Barrier Reef World Heritage. For an in-depth look into the history of the Great Barrier Reef click here.
The Great Barrier Reef Marine Park (GBRMP)became a Marine Protected Area for several reasons. The GBRMP is home to thousands of different marine species which are depleting, threatened, rare or endangered species and populations. This is to ensure the long-term viability and maintaining the genetic diversity of the marine populations of the Great Barrier Reef.
For a complete list of protected species click here and jump to page 13. The following video outlines some of the unique biodiversity found within the Great Barrier Reef.For more information on ecosystems clickhere.

The GBRMPAis responsible for ensuring the Great Barrier Reef Marine Park — one of the world's greatest natural treasures — is protected for the future. (GBRMPA, 2016).As a World Heritage Area, the Reef is recognized internationally for its outstanding universal value. The GBMPA has a 25 year management plan which outlines a mix of on-ground work, policies, strategies and engagement. This plan includes: increasing compliance focus to ensure zoning rules are followed controlling crown-of-thorns starfish outbreaks; ensuring cumulative impacts are considered when assessing development proposals; setting clear targets for action and measuring our success; monitoring the health of the ecosystem on a Reef-wide scale; implementing a Reef Recovery program to restore sites of high environmental value in regional areas. The plan also recognizes the variability of the Reef over such a large area and the variability of the issues and interests of communities and industries in each area. (UNESCO, 2015).
In 2012 The World Heritage Committee announced that the Great Barrier Reef Marine Park was “with a view to consider, in the absence of substantial progress, the possible inscription of the property on the List of World Heritage in Danger”. After this announcement, over the course of four years The Great Barrier Reef Marine Park was listed on the “in Danger list” and at risk of losing its World Heritage status. On July 1st, 2015, Federal Minister for the Environment of Australia, Greg Hunt, announced through a media release “Final World Heritage Committee decision praises Australia and unanimously rejects "in danger" listing for Great Barrier Reef”. Even with this announcement the Australian Government must continue to actively enforce its new management plan and continue to submit every 5 years reports to the World Heritage Committee on developments and progress.

The Australian and Queensland governments’ have been developing the [Reef 2050 Long-Term Sustainability Plan](http://www.gbrmpa.gov.au/managing-the-reef/reef-2050.) which provides an overarching strategy for managing the Great Barrier Reef and coordinate the actions and guides towards the adaptation of the 2050 management plan. (GBRMPA, 2016) The plan has been developed in close consultation with partners, including Traditional Owners and the resources, ports, fishing, agriculture, local government, and research and conservation sectors. The plan even included public input occurred through a six-week consultation period, with more than 6000 submissions received. The plan responds to the challenges facing the Reef and presents actions to protect its values, health and resilience while allowing ecologically sustainable use. It addresses the findings of the Great Barrier Reef Marine Park Authority’s Outlook Report 2014 and builds on the comprehensive strategic environmental assessment.
</excerpt>

## Search 6 — query: "List of World Heritage in Danger natural sites countries"
### Rank 1 of 49 — 0.50 (passed on)
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
### Rank 2 of 49 — 0.44
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
### Rank 3 of 49 — 0.32
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
*   Dark  

*   XY basemap dd ddm dms mgrs usng utm No position
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

# List of World Heritage in Danger
##### Côte d'Ivoire
*   Mount Nimba Strict Nature Reserve (1992) *
</excerpt>
### Rank 4 of 49 — 0.31
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
### Rank 5 of 49 — 0.30
<excerpt title="Heritage at Risk: 4 UNESCO Sites Under Threat">
## **Impact of Climate Change and Human Destruction**
### **2. The Galápagos Islands, Ecuador**
The Galápagos Islands, famous for their unique ecosystems, are threatened by invasive species, overfishing, and climate change. Invasive species such as goats and rats disrupt local ecosystems by preying on native wildlife and competing for resources.
For instance, the iconic Galápagos tortoise has faced significant population declines due to hunting, habitat destruction, and competition with invasive species like goats. As ecosystem engineers and large vertebrates, Galápagos tortoises play a crucial role in maintaining the health of the island’s ecosystems. Their sensitivity to environmental changes makes them valuable indicators of ecological disturbances. Conservation efforts are ongoing to protect and restore their populations.
Giant Galapagos Tortoise. Photo: Xavier Castro/Galápagos Conservancy.
A study published in 2021 by the Galápagos Conservancy highlights that these invasions have led to declines in native species populations. Furthermore, climate change is causing ocean acidification and rising sea levels, which threaten the delicate balance of the islands’ ecosystems.

## **Impact of Climate Change and Human Destruction**
### **3. Venice, Italy**
Venice, a UNESCO World Heritage Site since 1987, is celebrated for its unique architecture and intricate canal system, yet it faces significant threats to its structural integrity and cultural heritage.
Venice flooded during high tide.
Rising sea levels, exacerbated by climate change, have exacerbated flooding, causing extensive damage to buildings and infrastructure. In addition, the city is also sinking due to geological processes and groundwater extraction.
Overtourism adds another layer of pressure, with millions of visitors yearly contributing to wear and tear on historic sites and overcrowding. Pollution from boats and industrial activities threatens the marine ecosystem while large cruise ships raise concerns about environmental and structural impacts.
Initiatives such as the MOSE project, which features a sophisticated system of movable barriers designed to be raised during extreme tidal events to protect the Venetian Lagoon from flooding, are crucial for safeguarding the city. However, ongoing commitment is vital to ensure that this iconic site is preserved for future generations.
Aerial view of the MOSE Project in Venice, Porto di Lido (Channel north of Lido) in Mid-2009. Photo: Wikimedia Commons.

## **Impact of Climate Change and Human Destruction**
### **4. Ancient City of Aleppo, Syria**
Political instability in regions experiencing conflict can also put heritage sites at risk. Many sites struggle with limited resources for maintenance and conservation, hindering efforts to protect these treasures from decay.
The Ancient City of Aleppo is one of the oldest continuously inhabited cities in the world, with a rich history reflected in its historic architecture, including the Citadel of Aleppo and the Great Mosque. However, the ongoing Syrian Civil War has resulted in extensive damage to the city’s cultural heritage.
The citadel overlooking the city, Aleppo. Photo: Wikimedia Commons.
According to reports from the UNESCO World Heritage Centre, many historic buildings have been destroyed or severely damaged due to military actions, looting, and neglect. The lack of adequate resources for restoration and protection compounds the risk, with the site now listed as a UNESCO World Heritage site in danger.

## **Outlook**
These are just some of the many sites that are at risk due to climate change and human activities. The threats they face are not just isolated challenges; they reflect broader patterns of environmental degradation and cultural loss that impact communities worldwide.
As we continue to witness the accelerating impacts of climate change – such as rising sea levels, extreme weather events, and habitat destruction – it becomes increasingly clear that urgent action is necessary.
Preserving these UNESCO Heritage Sites is crucial not only for protecting their inherent beauty and historical significance but also for maintaining the cultural narratives and biodiversity they represent. It requires a collective effort from governments and individuals to advocate for sustainable practices, invest in conservation, and promote awareness of the importance of these sites.

## **This story is funded by readers like you**
Our non-profit newsroom provides climate coverage free of charge and advertising. Your one-off or monthly donations play a crucial role in supporting our operations, expanding our reach, and maintaining our editorial independence.
About EO | Mission Statement | Impact & Reach | Write for us
</excerpt>

## Search 7 — query: "natural sites on UNESCO List of World Heritage in Danger 2025 site name area"
### Rank 1 of 95 — 0.66 (passed on)
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
### Rank 2 of 95 — 0.53
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
### Rank 3 of 95 — 0.46
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
### Rank 4 of 95 — 0.40
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
### Rank 5 of 95 — 0.25
<excerpt title="56 Sites Are on UNESCO's List of World Heritage in Danger">
Jerusalem, which became a UNESCO World Heritage site in 1981, is on UNESCO’s in-danger list.
Photo by John Theodor/Shutterstock
The Taj Mahal, Cinque Terre, Yellowstone National Park—you’re bound to recognize many places on the United Nations Educational, Scientific, and Cultural Organization (UNESCO) World Heritage List. The list includes 1,199 natural and cultural sights of significance from 195 countriesaround the world that are considered to be of universal value and meet at least one of UNESCO’s 10 selection criteria (such as bearing unique testimony to a civilization or exemplifying significant ecological processes).
In 2022, UNESCO declared climate change to be thenumber one threat to natural World Heritage sites. The organization stated that climate change has already negatively impacted 34 percent of all sites.
However, that’s not the only threat. In fact, UNESCO maintains a list of World Heritage sites at risk.
According to Article 11 of the UNESCO World Heritage Convention, places qualify for the in-danger list if they face threats such as disappearance due to rapid urban or tourist development projects, land destruction, or the outbreak or prospect of an armed conflict. The full list now includes 56 World Heritage sites.
Here are a few standouts that represent the diversity of risks that can put a spot on the watch list. While UNESCO accepts general donations to protect its World Heritage sites, plenty of the listed in-danger sites accept individual donations, too.

### Old City of Jerusalem and its walls
Jerusalem has major significance for Judaism, Christianity, and Islam as the site of important events in each religion’s history. The ancient city became a UNESCO World Heritage site in 1981 and includes monuments such as the Wailing Wall, the Church of the Holy Sepulchre, and the Dome of the Rock.
A year after Jerusalem’s inscription, the city was added to the in-danger list due to a number of factors, including the deterioration of the city’s monuments and the impact of archaeological excavations.
Virunga National Park is home to a number of diverse landforms, including volcanoes.
Photo by Marian Galovic/Shutterstock

### Virunga National Park, Democratic Republic of the Congo
**Donate:**Virunga National Park
Virunga National Park, inscribed as a UNESCO World Heritage site in 1979 and located on the eastern section of the Congo Basin, is home to more than 1,000 species (including a third of the world’s endangered mountain gorillas). Unfortunately, the park was added to UNESCO’s in-danger list in 1994 due to the effects of the Rwandan genocide. Following the outbreak of war in Rwanda, the surge in refugees to the Democratic Republic of the Congo led to increased deforestation and poaching at the site—which still threaten the national park today.
Everglades National Park is the only UNESCO World Heritage site in the USA on the in-danger list.
Photo by Brian Lasenby/Shutterstock

### Everglades National Park, United States
**Donate:**Everglades National Park
Florida’s Everglades National Park is the largest subtropical wilderness in the United States; it has been a UNESCO World Heritage site since 1979. In 1993, the area was added to the in-danger list because of damage caused by Hurricane Andrew and then removed in 2007. However, the site was added back to the list in 2010 due to concerns over the deterioration of its aquatic ecosystem.
The breakdown of its ecosystem has been attributed to factors like pollution, lower water levels from neighboring agricultural activities, a reduction of marine and estuarine biodiversity, and changes in water flow volume.
You can see examples of Vienna’s baroque architecture at the Belvedere.
Photo by Mistervlad/Shutterstock
</excerpt>

## Search 8 — query: "List of World Heritage in Danger natural sites Wikipedia list 2026"
### Rank 1 of 168 — 0.39 (passed on)
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
### Rank 2 of 168 — 0.36
<excerpt title="1978 (1st list - 2nd session)">
Turkey	Sardis and the Lydian Tumuli of Bin Tepe	Cultural	1731  
 United Arab Emirates	Faya Palaeolandscape	Cultural	1735  
 Vietnam	Yen Tu-Vinh Nghiem-Con Son, Kiep Bac Complex of Monuments and Landscapes	Cultural	1732  
2026 (48th session)edit
The 48th session was held in Busan, on 19–29 July 2026.[15]
Host:  South Korea
25 Sites (19 cultural, 5 natural, 1 mixed).

Country	Site	Category	UNESCO Reference no.  
 Brazil	Amazonia Theaters	Cultural	1774  
 China	Jingdezhen Handicraft Porcelain Industry Sites	Cultural	1765  
 Comoros	Historical Sultanates of the Comoros (F)	Cultural	1768  
 Denmark	The Bony Fish Fossils of the Western Limfjord – Evolution and Climate Adaptation in the Earliest Eocene	Natural	1758  
 Finland	Aalto Works	Cultural	1752  
 France	Beaches of the D-Day Landings, Normandy, 1944	Cultural	1581  
Royal Capetian Fortresses of Languedoc	Cultural	1755  
 Greece	The wider area of Mount Olympus	Mixed	1719  
 India	Ancient Buddhist Site of Sarnath	Cultural	927  
 Iran	Alamūt Castle and Related Fortifications	Cultural	1770  
 Italy	The system of Italian-style condominio theatres of the 18th and 19th centuries in Central Italy	Cultural	1762  
 Japan	Ancient Capitals of Asuka and Fujiwara	Cultural	1757  
 Jordan	Aqaba Marine Reserve	Natural	1742  
 Kazakhstan	Rocky Mosques of Mangyshlak Peninsula	Cultural	1760  
 Lebanon	Mount Amel Castles	Cultural	1810  
 Mongolia	The Cemetery Complexes of the Xiongnu Nobility	Cultural	1759  
 Palestine	Sebastia	Cultural	1809  
 Poland	Gdynia Modernist City Centre	Cultural	1715  
 Sao Tome and Principe	The Roças of Sao Tome and Principe: Colonial Agricultural System and Forced Migration (F)	Cultural	1750  
 South Korea	Getbol, Korean Tidal Flats (Phase II)	Natural	1591  
 South Sudan	Boma-Badingilo Migratory Landscape (F)	Natural	1808  
 Thailand	Wat Phra Mahathat Woramahawihan, Nakhon Si Thammarat	Cultural	1761  
 Tunisia	Village of Sidi Bou Saïd	Cultural	1769  
 United Arab Emirates	Wadi Wurayah	Natural	1724  
 United States	Okefenokee National Wildlife Refuge	Natural	1751
</excerpt>
### Rank 3 of 168 — 0.32
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
### Rank 4 of 168 — 0.31
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
### Rank 5 of 168 — 0.30
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

## Search 9 — query: ""natural sites" "List of World Heritage in Danger""
### Rank 1 of 87 — 0.62 (passed on)
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
### Rank 2 of 87 — 0.44
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
### Rank 3 of 87 — 0.32
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
### Rank 4 of 87 — 0.31
<excerpt title="Natural World Heritage">
# Natural World Heritage
## Nature’s most precious gifts
Natural World Heritage sites are critical for the conservation of ecosystem integrity and biodiversity. While they make up less than 1% of the Earth’s surface, they harbor more than 1/5 of mapped global species richness. This includes over 75,000 species of plants, and over 30,000 species of mammals, birds, fishes, reptiles and amphibians. These sites also represent a safe haven for some of the most threatened species on Earth. They are estimated to protect over 20,000 globally threatened species, including some of the last individuals of many iconic species. Today, up to 1/3 of remaining elephants, tigers and pandas can be found in these sites, as well as at least 1 in 10 great apes, giraffes, lions and rhinos. For some species on the brink of extinction, World Heritage sites have become the last line of defense. They are home to all remaining Javan rhinos, vaquitas (the world's smallest cetacean) and pink iguanas, as well as more than half of all Sumatran rhinos, Sumatran orangutans and mountain gorillas.
Millions of people are directly dependent on the countless benefits and services these sites can provide, supporting livelihoods and wellbeing. Over 90% of listed natural sites create jobs and provide income from tourism and recreation. Two-thirds of natural sites are crucial sources of water, and about half help prevent hazards such as floods or landslides. They also have a central role in climate regulation and carbon sequestration as World Heritage forests absorb approximately 190 million tons of CO2 each year (equivalent to half the United Kingdom’s annual CO2 emissions from fossil fuels). Marine and coastal sites are also critical to mitigating climate impacts storing 1.3 billion tons of carbon (known as blue carbon) in seagrass meadows, tidal marshes and mangroves, representing 15% of global blue carbon assets.

# Natural World Heritage
## A threatened paradise
Natural World Heritage sites account for around 8% of the total surface area covered by all 280,000+ terrestrial and marine protected areas worldwide. Yet they are under increasing pressure. According to IUCN, the official advisory body on nature under the World Heritage Convention, climate change, invasive species and the negative impacts of tourism are currently the three most significant threats. Other major threats include poaching, planned infrastructure such as roads, dams, mining, oil and gas projects, and conflicts.
To date 16 natural World Heritage sites are on the List of World Heritage in Danger. Climate change is however the fastest growing threat to natural World Heritage, with the number of sites highly threatened by climate change almost doubling in the last decade. Every 1°C increase in temperature could double the number of species exposed to dangerous climate conditions. Forests, coral reefs and glaciers are among some of the most affected ecosystems. Wetlands, low-lying deltas, permafrost and fire sensitive ecosystems are also affected.
Almost 2/3 of forests found in World Heritage sites are threatened by land use pressures and climate-related hazards such as wildfires. A first global scientific assessment of greenhouse gas emissions and sequestration in World Heritage forests revealed that at least 10 sites were net carbon sources since 2000 and that one single climate-related hazard could make a forest site from a carbon sink to source.
World Heritage-listed coral reefs, such as theGreat Barrier Reef (Australia)(the world's largest coral reef system), theAldabra Atoll (Seychelles)in the Indian Ocean (the world's second-largest coral atoll) and the Belize Barrier Reef (Belize)in the Atlantic (the largest barrier reef in the northern hemisphere) have been affected by devastating mass coral bleaching events over the past decades. A first global scientific assessment of the impacts of climate change on World Heritage coral reefs revealed that by 2040, all World Heritage-listed coral reefs could face annual severe bleaching events at least twice a decade.
</excerpt>
### Rank 5 of 87 — 0.21
<excerpt title="Sites In Danger">
Unfortunately, Africa has more than its fair share of world heritage sites inscribed on the official List of World Heritage In Danger. Of the 39 sites on the global Danger list, 17 (44%) are in Africa (see list below). Four additional African sites have been included on the Danger List in the past, but are now sufficiently recovered to allow their removal. The high number of African sites reflects the particular challenges of this continent, especially the occurrence of periodic civil unrest and war. Twelve of Africa’s endangered sites are natural, while only three are cultural. Cultural sites normally fare better than natural ones through periods of unrest as there is normally no reason for wilfully damaging them. In general they are more likely to be threatened by accidental damage or structural deterioration due to neglect. But the recent destruction of some of the famous mausoleums in the ancient Malian town of Timbuktu show that religious extremism can also contribute to the loss of heritage.
Natural sites are vulnerable during periods of unrest because they are commonly viewed as a source of free meat and other resources. At these times management becomes impossible and a proliferation of guns enables rebel groups, defending armies or opportunistic civilian populations to exploit park resources. The current problems at sites in Central African Republic, Cote D’Ivoire, Congo, Ethiopia, Niger and Madagascar all began during periods of civil unrest, and are likely to continue long after the cessation of conflict. Even if park infrastructure and management can be restored fairly quickly, animal populations take many years to recover.
**Main Threats to Africa’s World Heritage Sites**
Some of the threats to specific places are highlighted in the corresponding page of the website, but here is an overview of the ‘Top 10’ key threats affecting Africa’s world heritage sites. In some cases, a threat associated with a particular place has not yet reached levels that warrant a site’s Danger listing, but early recognition of emerging issues should help keep sites off the list.
**Mining and mineral exploitation**. The present boom in commodity prices has resulted in a huge surge in mineral exploration activity across Africa and, despite the provisions of the Convention, many governments regard world heritage sites as legitimate places for exploration. Sites that are currently threatened by mining or mineral exploration (inside their boundaries or close-by) include Mount Nimba, the Rwenzori Mountains, Virunga, Lake Turkana, Banc D’Arguin, iSimangaliso, Mana Pools and Selous.

**Dam-building, water diversion and abstraction**. Water is needed everywhere – for power generation, agricultural irrigation and industrial development. The Egyptian plan to dam the Nile, developed in the 1950s and implemented in the 60s, was probably the single most important driving force behind the world heritage movement, bringing nations together to save the magnificent Nubian monuments from the rising waters of Lake Nasser. Today, as development elsewhere in Africa gathers momentum and investment in the continent increases, the rivers and wetlands that sustain some of the continent’s most important world heritage sites are being dammed and their life-sustaining water diverted to giant irrigation schemes. The vast cost of these schemes may have slowed the pace of such developments in the past, but many are now attracting renewed attention. Sites that are threatened by dam-building, water diversion and abstraction include Victoria Falls, Lake Ichkeul, Lake Turkana, Djoudj, iSimangaliso, Mana Pools, the Kenya Lake System, Niokolo-Koba and Selous. Abu Mena is a special case, where water diverted from the Nile for irrigation is incidentally affecting the foundations of this archaeological site.
**Roads and infrastructure development**. Plans for major new roads through world heritage sites – such as the infamous motorway scheme that would have passed through the Giza Pyramids’ site, or the new Serengeti highway – tend to attract strong opposition and the threat they pose can often be averted through a combination of approaches involving the international media, public protest, diplomatic and political channels. But other major schemes, such as the new port and infrastructure corridor which is set to transform Lamu Old Town may go ahead regardless. There are many smaller infrastructure development projects that are progressively eroding the wilderness values of natural heritage sites across the continent and others that impact cultural heritage. Sites that are threatened by road-building and other infrastructure developments include those mentioned above as well as the Simien Mountains, Selous, Okapi and Timgad.
</excerpt>

## Search 10 — query: "natural sites in the UNESCO List of World Heritage in Danger 2026 "natural""
### Rank 1 of 83 — 0.71 (passed on)
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
### Rank 2 of 83 — 0.40
<excerpt title="UNESCO has expanded its World Heritage List with 25 new sites ...">
# Instagram
Log In
Sign Up
Never miss a post from afarmedia
Sign up for Instagram to stay in the loop.
By continuing, you agree to Instagram's Terms of Use and Privacy Policy.
Sign up
Log in
*           
*
afarmedia
•
Follow
* * *
afarmedia15w
UNESCO has expanded its World Heritage List with 25 new sites for 2026. This year's additions include the first U.S. addition since 2023: the Okefenokee National Wildlife Refuge, a sprawling 400,000-acre wetland spanning Georgia and Florida that's home to American alligators, black bears, river otters, and one of North America's most biodiverse ecosystems.
In Greece, Mount Olympus joins the list recognized both as the legendary home of the Olympian gods and for its dramatic alpine landscapes. From India's ancient Buddhist site of Sarnath to Poland's modernist city center of Gdynia, the 25 new UNESCO sites showcase the remarkable diversity of the world's cultural heritage and natural wonders.
Tap the link in bio for the full list.
Story by Pat Tompkins
Photo by Vasileios Triantafyllou, © Protected Area Management Units; Michael Lusk, © Public Domain; Michel Dehaye; Maija Holma, © Alvar Aalto Foundation
seangauthier15w
Not so ironically, the USA is leaving UNESCO at the end of this year.
Like
Reply
277 1
August 1
Log in to like or comment.
* * *
More posts from afarmedia
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
### Rank 3 of 83 — 0.40
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
### Rank 4 of 83 — 0.28
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
### Rank 5 of 83 — 0.25
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
*   Dark  

*   XY basemap dd ddm dms mgrs usng utm No position
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

# List of World Heritage in Danger
##### Côte d'Ivoire
*   Mount Nimba Strict Nature Reserve (1992) *
</excerpt>

# Example 2
## Question
Based on the data provided by the NCEI for the global summary of the month, which of the following stations saw a difference between mean max and mean min temperature less than 17 degrees Fahrenheit in July 2020: Denver International Airport, Atlanta Hartsfield Jackson International Airport, Los Angeles International Airport, Chicago Ohare International Airport, Orlando International Airport

## Expected answer
Los Angeles International Airport, Orlando International Airport

## Grade 0.00

## Search 1 — query: "Global Summary of the Month 2020 July station Denver International Airport mean max mean min temperature"
### Rank 1 of 78 — 0.59 (passed on)
<excerpt title="Geography of Denver">
| * v * t * e Climate data for Denver (DIA; elev 5414 ft), 1991−2020 normals,[[a]](https://en.wikipedia.org/wiki/Geography_of_Denver#cite_note-7) extremes 1872−present[[b]](https://en.wikipedia.org/wiki/Geography_of_Denver#cite_note-8) |  
| --- |  
| Month | Jan | Feb | Mar | Apr | May | Jun | Jul | Aug | Sep | Oct | Nov | Dec | Year |  
| Record high °F (°C) | 76 (24) | 80 (27) | 87 (31) | 90 (32) | 95 (35) | 105 (41) | 105 (41) | 105 (41) | 101 (38) | 90 (32) | 83 (28) | 79 (26) | 105 (41) |  
| Mean maximum °F (°C) | 65.0 (18.3) | 67.1 (19.5) | 74.7 (23.7) | 80.8 (27.1) | 88.3 (31.3) | 96.5 (35.8) | 99.6 (37.6) | 96.9 (36.1) | 92.9 (33.8) | 84.1 (28.9) | 73.6 (23.1) | 65.3 (18.5) | 100.6 (38.1) |  

| Mean daily maximum °F (°C) | 44.6 (7.0) | 45.7 (7.6) | 55.7 (13.2) | 61.7 (16.5) | 71.2 (21.8) | 83.4 (28.6) | 89.9 (32.2) | 87.5 (30.8) | 79.6 (26.4) | 65.3 (18.5) | 52.9 (11.6) | 44.0 (6.7) | 65.1 (18.4) |  
| Daily mean °F (°C) | 31.7 (−0.2) | 32.7 (0.4) | 41.6 (5.3) | 47.8 (8.8) | 57.4 (14.1) | 68.2 (20.1) | 75.1 (23.9) | 72.9 (22.7) | 64.8 (18.2) | 51.1 (10.6) | 39.4 (4.1) | 31.2 (−0.4) | 51.2 (10.6) |  
| Mean daily minimum °F (°C) | 18.7 (−7.4) | 19.7 (−6.8) | 27.5 (−2.5) | 33.9 (1.1) | 43.6 (6.4) | 53.0 (11.7) | 60.2 (15.7) | 58.3 (14.6) | 50.0 (10.0) | 37.0 (2.8) | 26.0 (−3.3) | 18.4 (−7.6) | 37.2 (2.9) |
</excerpt>
### Rank 2 of 78 — 0.49
<excerpt title="Geography of Denver">
| Climate data for Denver Water Department (elevation 5225 ft), 1991–2020 normals, extremes 1997–present |  
| --- |  
| Month | Jan | Feb | Mar | Apr | May | Jun | Jul | Aug | Sep | Oct | Nov | Dec | Year |  
| Record high °F (°C) | 77 (25) | 78 (26) | 85 (29) | 91 (33) | 99 (37) | 107 (42) | 108 (42) | 104 (40) | 102 (39) | 90 (32) | 84 (29) | 76 (24) | 108 (42) |  
| Mean daily maximum °F (°C) | 48.5 (9.2) | 49.0 (9.4) | 57.9 (14.4) | 64.1 (17.8) | 73.0 (22.8) | 85.3 (29.6) | 91.4 (33.0) | 89.6 (32.0) | 81.6 (27.6) | 67.6 (19.8) | 55.9 (13.3) | 47.3 (8.5) | 67.6 (19.8) |  

| Mean daily minimum °F (°C) | 21.3 (−5.9) | 21.7 (−5.7) | 29.6 (−1.3) | 36.2 (2.3) | 45.9 (7.7) | 55.8 (13.2) | 61.8 (16.6) | 60.1 (15.6) | 50.7 (10.4) | 37.7 (3.2) | 27.6 (−2.4) | 20.6 (−6.3) | 39.1 (4.0) |  
| Record low °F (°C) | −15 (−26) | −14 (−26) | −2 (−19) | 8 (−13) | 20 (−7) | 36 (2) | 49 (9) | 40 (4) | 22 (−6) | 4 (−16) | −8 (−22) | −13 (−25) | −15 (−26) |  
| Average precipitation inches (mm) | 0.43 (11) | 0.60 (15) | 1.13 (29) | 1.98 (50) | 2.65 (67) | 1.73 (44) | 1.90 (48) | 1.81 (46) | 1.20 (30) | 1.16 (29) | 0.78 (20) | 0.48 (12) | 15.85 (401) |  

| Average snowfall inches (cm) | 5.5 (14) | 8.4 (21) | 9.2 (23) | 5.0 (13) | 0.9 (2.3) | 0 (0) | 0 (0) | 0 (0) | 0 (0) | 2.5 (6.4) | 4.4 (11) | 4.8 (12) | 40.7 (102.7) |  
| Source: xmACIS2 |
</excerpt>
### Rank 3 of 78 — 0.41
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
*   #### Warm, sunny Wednesday in Philadelphia region   
*   #### Spencer Gibson sworn in as Denver's new postmaster   
*   #### Coldest temperatures so far this season to arrive in North Texas
© 2020 CBS Broadcasting Inc. All Rights Reserved.

# Denver Weather: July 2020 Average Temp Makes Top 10 Warmest On Record
### Featured Local Savings
CBS News Colorado Live
</excerpt>
### Rank 4 of 78 — 0.39
<excerpt title="Geography of Denver">
| Average snowfall inches (cm) | 5.5 (14) | 8.4 (21) | 9.2 (23) | 5.0 (13) | 0.9 (2.3) | 0 (0) | 0 (0) | 0 (0) | 0 (0) | 2.5 (6.4) | 4.4 (11) | 4.8 (12) | 40.7 (102.7) |  
| Source: xmACIS2 |

| Climate data for Central Park, Denver, 1991–2020 normals |  
| --- |  
| Month | Jan | Feb | Mar | Apr | May | Jun | Jul | Aug | Sep | Oct | Nov | Dec | Year |  
| Mean daily maximum °F (°C) | 46.5 (8.1) | 47.5 (8.6) | 56.4 (13.6) | 62.5 (16.9) | 71.7 (22.1) | 84.1 (28.9) | 90.2 (32.3) | 87.9 (31.1) | 80.1 (26.7) | 66.7 (19.3) | 54.8 (12.7) | 45.9 (7.7) | 66.2 (19.0) |  
| Mean daily minimum °F (°C) | 17.6 (−8.0) | 19.3 (−7.1) | 27.1 (−2.7) | 33.7 (0.9) | 43.4 (6.3) | 52.9 (11.6) | 59.3 (15.2) | 57.2 (14.0) | 48.2 (9.0) | 35.7 (2.1) | 25.5 (−3.6) | 17.7 (−7.9) | 36.5 (2.5) |  

| Average precipitation inches (mm) | 0.46 (12) | 0.53 (13) | 1.12 (28) | 1.67 (42) | 2.29 (58) | 1.68 (43) | 2.12 (54) | 1.83 (46) | 1.51 (38) | 0.98 (25) | 0.70 (18) | 0.47 (12) | 15.36 (390) |  
| Average snowfall inches (cm) | 6.4 (16) | 7.6 (19) | 8.8 (22) | 6.2 (16) | 1.4 (3.6) | 0 (0) | 0 (0) | 0 (0) | 0.8 (2.0) | 3.9 (9.9) | 7.3 (19) | 6.6 (17) | 49.0 (124) |  
| Source: NOAA[[12]](https://en.wikipedia.org/wiki/Geography_of_Denver#cite_note-NOAAtwo-14) |
</excerpt>
### Rank 5 of 78 — 0.27
<excerpt title="Geography of Denver">
| Mean daily maximum °F (°C) | 44.6 (7.0) | 45.7 (7.6) | 55.7 (13.2) | 61.7 (16.5) | 71.2 (21.8) | 83.4 (28.6) | 89.9 (32.2) | 87.5 (30.8) | 79.6 (26.4) | 65.3 (18.5) | 52.9 (11.6) | 44.0 (6.7) | 65.1 (18.4) |  
| Daily mean °F (°C) | 31.7 (−0.2) | 32.7 (0.4) | 41.6 (5.3) | 47.8 (8.8) | 57.4 (14.1) | 68.2 (20.1) | 75.1 (23.9) | 72.9 (22.7) | 64.8 (18.2) | 51.1 (10.6) | 39.4 (4.1) | 31.2 (−0.4) | 51.2 (10.6) |  
| Mean daily minimum °F (°C) | 18.7 (−7.4) | 19.7 (−6.8) | 27.5 (−2.5) | 33.9 (1.1) | 43.6 (6.4) | 53.0 (11.7) | 60.2 (15.7) | 58.3 (14.6) | 50.0 (10.0) | 37.0 (2.8) | 26.0 (−3.3) | 18.4 (−7.6) | 37.2 (2.9) |  

| Mean minimum °F (°C) | −3.8 (−19.9) | −1.5 (−18.6) | 9.5 (−12.5) | 19.8 (−6.8) | 30.2 (−1.0) | 41.9 (5.5) | 51.4 (10.8) | 48.8 (9.3) | 35.9 (2.2) | 19.6 (−6.9) | 5.4 (−14.8) | −3.4 (−19.7) | −11.0 (−23.9) |  
| Record low °F (°C) | −29 (−34) | −25 (−32) | −11 (−24) | −2 (−19) | 19 (−7) | 30 (−1) | 42 (6) | 40 (4) | 17 (−8) | −2 (−19) | −18 (−28) | −25 (−32) | −29 (−34) |  
| Average precipitation inches (mm) | 0.38 (9.7) | 0.41 (10) | 0.86 (22) | 1.68 (43) | 2.16 (55) | 1.94 (49) | 2.14 (54) | 1.58 (40) | 1.35 (34) | 0.99 (25) | 0.64 (16) | 0.35 (8.9) | 14.48 (368) |
</excerpt>

## Search 2 — query: "Global Summary of the Month July 2020 Denver mean maximum mean minimum"
### Rank 1 of 58 — 0.66 (passed on)
<excerpt title="July Year: 2020 Temperature - Colorado Climate Center">
Title: PDF document  
URL Source: https://climate.colostate.edu/pdfs/Wx_Stn_Monthly_Summary_Form_July_2020.pdf  
Markdown Content:

## [PDF page 1]
Colorado State University, Fort Collins, CO Weather Station  
Monthly Summary Report
Month: July  
Year: 2020
Temperature:  
Mean Tmax was 89.1°F which is 2.5° above the 1981-2010 normal for the  
month.  This is the 16th warmest in the 132-year record (1889-2020), tied  
with 1966.  The last July this warm or warmer was 2017 with 89.3°F.
Mean Tmin was 58.6°F which is 0.1° above the 1981-2010 normal for the  
month.  This is the 23rd warmest in the 132-year record (1889-2020), tied  
with 1984.  The last July this warm or warmer was 2019 with 59.0°F.
Mean Tmean was 73.8°F which is 1.2° above the 1981-2010 the normal for the  
month.  This is the 16th warmest in the 132-year record (1889-2020).  The  
last July this warm or warmer was 2019 with 74.0°F.
The maximum daily temperature for the month was 99°F and occurred on  
July 10, 2020.  
The minimum daily temperature for the month was 50°F and occurred on  
July 1, 2020.

## [PDF page 2]
Figure 1: July temperature time series.
Misc. Temperature (record status, thresholds, etc.):
No temperature records for July 2020
90F Degree Days:  
July 2020 had 17 days at or above 90F.  The average number of  
days in the 90s for  July is 9.
Through the end of July, there have been 26 days at or above 90F  
this summer.  The avera  ge number of days in the 90s through July  
is 13.

## [PDF page 3]
Precipitation and Snowfall:  
Total monthly precipitation was 0.15” which is 1.56” below the 1981-2010  
normal for the month (9% of normal).  This ranks as the 5th driest in the 132-  
year record (1889-2020).  The last July this parched was 2002 with 0.07” of  
precipitation.
Figure 2: Top 10 driest July precipitation  
totals on record.
Water year precipitation through July totaled 11.02” which is 2.15” below  
the 1981-2010 normal for the water year (84% of normal).  This ranks as the  
53rd driest start to a water year in the 131-year record (1890-2020).  The last  
water year this dry or drier through July was 2013 with 11.00” of  
precipitation.
July had 5 days with measurable precipitation (≥ 0.01”) and 14 days with a  
trace of precipitation (less than 0.01”)

## [PDF page 4]
Figure 3: July precipitation  time series.
Misc. Precipitation (predominant type, record status, etc.):
No precipitation records for July.
The highest one-day precipitation total for July 2020 was 0.06” falling on  
July 13th (cue sad trombone).
</excerpt>
### Rank 2 of 58 — 0.60
<excerpt title="Denver, Colorado">
*   Home>  
*   North and Central America>  
*   United States of America>  
*   Denver, Colorado
Denver, Colorado✚
Denver, Colorado✚
6°C
20%
S 9 km/h
N.B.
Thu, Nov 19, 2026 1:58 AM (Local Time)
wxphoto
19 Nov
(Thu)
-2°C | 13°C
Sunny Periods
20 Nov
(Fri)
2°C | 16°C
Sunny
21 Nov
(Sat)
-1°C | 8°C
Sleet
22 Nov
(Sun)
-4°C | 8°C
Sunny
23 Nov
(Mon)
-3°C | 8°C
Sunny Periods
24 Nov
(Tue)
-3°C | 8°C
Snow Showers
25 Nov
(Wed)
-4°C | 9°C
Sunny Periods
Sunrise
Sunset
Issued at 11:46 AM (Local Time) Nov 18, 2026
The boundaries and names shown and the designations used do not imply official endorsement or acceptance by WMO or the United Nations.
Click a city on the map to see forecast and/or climatological information.
19 Nov 2026
Sunrise
6:49 AM
Sunset
4:41 PM
N.B.

| Month | Mean Daily Minimum Temperature (°C) | Mean Daily Maximum Temperature (°C) | Mean Total Rainfall (mm) | Mean Number of Rain Days |  
| --- | --- | --- | --- | --- |  
| Jan | -8.1 | 6.7 | 10.4 | 4.1 |  
| Feb | -7.3 | 7.9 | 9.4 | 5.3 |  
| Mar | -3.1 | 12.4 | 23.4 | 5.9 |  
| Apr | 0.7 | 16.4 | 43.4 | 9.1 |  
| May | 5.9 | 21.9 | 53.8 | 9.4 |  
| Jun | 11.3 | 28.0 | 50.3 | 8.4 |  
| Jul | 14.9 | 31.9 | 54.9 | 8.3 |  
| Aug | 14.4 | 30.7 | 42.9 | 8.6 |  
| Sep | 9.1 | 25.8 | 24.4 | 6.5 |  
| Oct | 2.6 | 18.5 | 25.9 | 5.3 |  
| Nov | -4.2 | 11.2 | 15.5 | 4.7 |  
| Dec | -8.3 | 6.0 | 8.9 | 4.1 |
Back to top
</excerpt>
### Rank 3 of 58 — 0.22
<excerpt title="July 2020 Climate Summary">
# Below are the overview stats from July 2020 for our 10 climate sites.
**July 2020 Temperature Climate Statistics**  
**Climate Site****Average Temperature****Normal Temperature****DFN (Departure**
**From Normal)**  
**Athens**83.1 80.6**+2.5**  
**Atlanta**82.1 80.2**+1.9**  
**Columbus**83.7 82.5**+1.2**  
**Macon**83.6 81.8**+1.8**  
**Cartersville**81.8 78.3**+3.5**  
**Dekalb Peachtree Arpt**80.6 79.8**+0.8**  
**Fulton County Arpt**80.8 79.8**+1.0**  
**Gainesville**80.4 78.8**+1.6**  
**Peachtree City**80.7 79.3**+1.4**  
**Rome**82.3 79.4**+2.9**

# Below are the overview stats from July 2020 for our 10 climate sites.
**July 2020 Temperature Climate Statistics**  
**Climate Site****Maximum Temperature****Max T Date****Minimum Temperature****Min T Date**  
**Athens**102 7/20 67 7/12  
**Atlanta**95 7/18,7/19,7/20,7/21 68 7/13  
**Columbus**99 7/19 70 7/13,7/26  
**Macon**102 7/20 67 7/12  
**Cartersville**99 7/20*65 7/12*  
**Dekalb Peachtree Arpt**96 7/20 65 7/12  
**Fulton Co Arpt**96 7/20 66 7/12  
**Gainesville**95 7/17*,7/18,7/20 66 7/12  
**Peactree City**96 7/20 64 7/12  
**Rome**99 7/17,7/19,7/20*66 7/12,7/13
_*Indicates a daily record was set_
**July 2020 Precipitation Climate Statistics**  
**Climate Site****Total Precipitation****Normal Precipitation****DFN (Departure**
</excerpt>
### Rank 4 of 58 — 0.15
<excerpt title="July 2020 Climate Summary">
# Below are the overview stats from July 2020 for our 10 climate sites.
**July 2020 Temperature Climate Statistics**  
**Climate Site****Maximum Temperature****Max T Date****Minimum Temperature****Min T Date**  
**Athens**102 7/20 67 7/12  
**Atlanta**95 7/18,7/19,7/20,7/21 68 7/13  
**Columbus**99 7/19 70 7/13,7/26  
**Macon**102 7/20 67 7/12  
**Cartersville**99 7/20*65 7/12*  
**Dekalb Peachtree Arpt**96 7/20 65 7/12  
**Fulton Co Arpt**96 7/20 66 7/12  
**Gainesville**95 7/17*,7/18,7/20 66 7/12  
**Peactree City**96 7/20 64 7/12  
**Rome**99 7/17,7/19,7/20*66 7/12,7/13
_*Indicates a daily record was set_
**July 2020 Precipitation Climate Statistics**  
**Climate Site****Total Precipitation****Normal Precipitation****DFN (Departure**

# Below are the overview stats from July 2020 for our 10 climate sites.
**From Normal)**  
**Athens**1.90 4.47**-2.57**  
**Atlanta**2.60 5.27**-2.67**  
**Columbus**3.49 4.76**-1.27**  
**Macon**1.85 4.95**-3.10**  
**Cartersville**1.50 4.66**-3.16**  
**Dekalb Peachtree Arpt**5.03 5.02**+0.01**  
**Fulton County Arpt**2.96 5.06**-2.10**  
**Gainesville**4.13 4.51**-0.38**  
**Peachtree City**3.22 5.26**-2.04**  
**Rome**2.42 4.32**-1.90**
**July 2020 Precipitation Climate Statistics**  
**Climate Site****Maximum Daily Precip****Max P Date**  
**Athens**1.26 7/6  
**Atlanta**1.21 7/6  
**Columbus**1.96 7/25  
**Macon**1.29 7/6  
**Cartersville**0.53 7/21  
**Dekalb Peachtree Arpt**2.08 7/21*  
**Fulton Co Arpt**1.82 7/9  
**Gainesville**1.71 7/31  
**Peachtree City**1.09 7/25  
**Rome**1.64 7/25
_*Indicates a daily record was set;**BOLD**indicates an all time August record_
_**Data prepared by NWS Peachtree City/Atlanta.**_
</excerpt>
### Rank 5 of 58 — 0.14
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

## Search 3 — query: "Denver International Airport July 2020 mean daily maximum temperature NCEI"
### Rank 1 of 51 — 0.22 (passed on)
<excerpt title="NWS Boulder Denver Daily Normals and Records July">
**National Weather Service - Denver/Boulder, Colorado**
**Denver Area Normals & Extremes for July**
**January | February | March | April | May | June | July | August | September | October | November | December**  
**Date****Normal High****Record High****Year Set****Record Warmest Minimum****Year Set****Normal Low****Record Low****Year Set****Record Coldest Maximum****Year Set****Maximum Precipitation****Year Set****Maximum Snowfall****Year Set**

**1**88 102 1990## 70 1881 58**46**1995^## 64 1908**1.25**1873**0.0**- **2**88 101 2012^## 69 2002^58**44**1997## 62 1906**1.34**1919**0.0**- **3**89 101 1874## 77 1881 58**46**1872## 54 1972**1.12**1909**0.0**- **4**89 102 1874## 70 1877 58**42***1903## 59 1972**1.84**2010**0.0**- **5**89 101 1989## 71 1930 59**43**1972## 62 1960**1.04**1900**0.0**- **6**89 103 1973## 68 1988^59**44**1908## 58 1904**1.01**2001**0.0**- **7**89 102 1989## 68 1903 59**43**1952## 65 1952^**1.41**1988**0.0**- **8**90 103 1989## 70 2005 59**45**1952## 57 1929**0.93**1909**0.0**-
</excerpt>
### Rank 2 of 51 — 0.18
<excerpt title="NWS Boulder Denver Daily Normals and Records July">
**17**91 102 2010## 72 2019 61**45**1872## 62 1872**0.89**1986**0.0**- **18**91 100 2022## 72 2022 61**48**1902## 63 1912**1.05**1958**0.0**- **19**91 101 2019^## 72 1881 61**48**1897## 57 1897**1.51**1985**0.0**- **20**91 105#2005## 73 1934 61**43**1897## 66 1915**1.09**1965**0.0**- **21**91 104 2005## 72 1934 61**51**1988^## 62 1930**1.36**1874**0.0**- **22**91 102 2005## 70 2022^61**49**1990^## 63 1895**1.53**1895**0.0**- **23**90 102 2005## 70 1982^61**49**1961## 65 1991**1.44**2001**0.0**- **24**90 100 2003## 71 1940 61**49**2004## 58 2004**1.06**1973**0.0**-

**25**90 101 2026## 73 2003 61**51**1973^## 72 1977**2.69**1998**0.0**- **26**90 103 2026## 70 1931 61**51**1971^## 64 1874**0.76**1874**0.0**- **27**90 98 1964## 74 2026 61**51**1958## 65 1963**1.37**1955**0.0**- **28**90 100 2021## 71 1931 61**49**1892## 63 1892**2.21**1910**0.0**- **29**90 99 2024^## 71 1943 61**47**1971## 58 1971**1.80**2014**0.0**- **30**90 101 2005## 70 1943 61**43**1971## 62 2014**2.71**1997**0.0**- **31**90 100 1889## 70 1966^61**42***1873## 62 1995**2.59**1919**0.0**-
**The Normal High and Low Temperatures are calculated from 1991-2020 data.**
**The Temperature Extremes range from 1872-Present**
**^ - Also in Previous Years**
**# - Highest Temperatures of the Month: 105° on 7/20/2005 (Ties the highest temperature in Denver)**
</excerpt>
### Rank 3 of 51 — 0.17
<excerpt title="NWS Boulder Denver Daily Normals and Records July">
**1**88 102 1990## 70 1881 58**46**1995^## 64 1908**1.25**1873**0.0**- **2**88 101 2012^## 69 2002^58**44**1997## 62 1906**1.34**1919**0.0**- **3**89 101 1874## 77 1881 58**46**1872## 54 1972**1.12**1909**0.0**- **4**89 102 1874## 70 1877 58**42***1903## 59 1972**1.84**2010**0.0**- **5**89 101 1989## 71 1930 59**43**1972## 62 1960**1.04**1900**0.0**- **6**89 103 1973## 68 1988^59**44**1908## 58 1904**1.01**2001**0.0**- **7**89 102 1989## 68 1903 59**43**1952## 65 1952^**1.41**1988**0.0**- **8**90 103 1989## 70 2005 59**45**1952## 57 1929**0.93**1909**0.0**-

**9**90 100 2024^## 68 1903 60**43**1876## 62 2006^**1.34**1990**0.0**- **10**90 102 2016## 70 1939^60**45**1895## 53 1895**2.35**1998**0.0**- **11**90 102 1954## 71 1931 60**49**1961^## 59 1895**1.64**1872**0.0**- **12**90 102 2024## 70 1893 60**48**1987^## 62 1987^**0.63**1935**0.0**- **13**90 100 2003## 70 1900 60**47**1987## 60 1930**1.03**2011**0.0**- **14**90 101 2024## 70 2024^61**49**1952## 67 1973^**2.00**1912**0.0**- **15**90 101 2006## 72 1881 61**48**1973## 67 1906**0.97**1992**0.0**- **16**90 103 2006## 70 1881 61**51**1962^## 65 1887**1.38**1923**0.0**-
</excerpt>
### Rank 4 of 51 — 0.14
<excerpt title="NWS Boulder Denver Daily Normals and Records July">
**25**90 101 2026## 73 2003 61**51**1973^## 72 1977**2.69**1998**0.0**- **26**90 103 2026## 70 1931 61**51**1971^## 64 1874**0.76**1874**0.0**- **27**90 98 1964## 74 2026 61**51**1958## 65 1963**1.37**1955**0.0**- **28**90 100 2021## 71 1931 61**49**1892## 63 1892**2.21**1910**0.0**- **29**90 99 2024^## 71 1943 61**47**1971## 58 1971**1.80**2014**0.0**- **30**90 101 2005## 70 1943 61**43**1971## 62 2014**2.71**1997**0.0**- **31**90 100 1889## 70 1966^61**42***1873## 62 1995**2.59**1919**0.0**-
**The Normal High and Low Temperatures are calculated from 1991-2020 data.**
**The Temperature Extremes range from 1872-Present**
**^ - Also in Previous Years**
**# - Highest Temperatures of the Month: 105° on 7/20/2005 (Ties the highest temperature in Denver)**

*** - Lowest Temperature of the Month: 42° on 7/4/1903 and 7/31/1873**
**- The July Mean Temperature is 75.1° (from 1991-2020 data)**
**- Data collected at the Downtown City Office from 1872 thru December 1948, then at the Stapleton Airport Office from**
**January 1950 thru February 1995, then at Denver International Airport from March 1995 to Present.**
**Updated: 7/27/2026**
</excerpt>
### Rank 5 of 51 — 0.13
<excerpt title="NWS Boulder Denver Daily Normals and Records July">
**9**90 100 2024^## 68 1903 60**43**1876## 62 2006^**1.34**1990**0.0**- **10**90 102 2016## 70 1939^60**45**1895## 53 1895**2.35**1998**0.0**- **11**90 102 1954## 71 1931 60**49**1961^## 59 1895**1.64**1872**0.0**- **12**90 102 2024## 70 1893 60**48**1987^## 62 1987^**0.63**1935**0.0**- **13**90 100 2003## 70 1900 60**47**1987## 60 1930**1.03**2011**0.0**- **14**90 101 2024## 70 2024^61**49**1952## 67 1973^**2.00**1912**0.0**- **15**90 101 2006## 72 1881 61**48**1973## 67 1906**0.97**1992**0.0**- **16**90 103 2006## 70 1881 61**51**1962^## 65 1887**1.38**1923**0.0**-

**17**91 102 2010## 72 2019 61**45**1872## 62 1872**0.89**1986**0.0**- **18**91 100 2022## 72 2022 61**48**1902## 63 1912**1.05**1958**0.0**- **19**91 101 2019^## 72 1881 61**48**1897## 57 1897**1.51**1985**0.0**- **20**91 105#2005## 73 1934 61**43**1897## 66 1915**1.09**1965**0.0**- **21**91 104 2005## 72 1934 61**51**1988^## 62 1930**1.36**1874**0.0**- **22**91 102 2005## 70 2022^61**49**1990^## 63 1895**1.53**1895**0.0**- **23**90 102 2005## 70 1982^61**49**1961## 65 1991**1.44**2001**0.0**- **24**90 100 2003## 71 1940 61**49**2004## 58 2004**1.06**1973**0.0**-
</excerpt>

## Search 4 — query: "DENVER International Airport July 2020 mean temperature report pdf"
### Rank 1 of 42 — 0.59 (passed on)
<excerpt title="July Year: 2020 Temperature - Colorado Climate Center">
Title: PDF document  
URL Source: https://climate.colostate.edu/pdfs/Wx_Stn_Monthly_Summary_Form_July_2020.pdf  
Markdown Content:

## [PDF page 1]
Colorado State University, Fort Collins, CO Weather Station  
Monthly Summary Report
Month: July  
Year: 2020
Temperature:  
Mean Tmax was 89.1°F which is 2.5° above the 1981-2010 normal for the  
month.  This is the 16th warmest in the 132-year record (1889-2020), tied  
with 1966.  The last July this warm or warmer was 2017 with 89.3°F.
Mean Tmin was 58.6°F which is 0.1° above the 1981-2010 normal for the  
month.  This is the 23rd warmest in the 132-year record (1889-2020), tied  
with 1984.  The last July this warm or warmer was 2019 with 59.0°F.
Mean Tmean was 73.8°F which is 1.2° above the 1981-2010 the normal for the  
month.  This is the 16th warmest in the 132-year record (1889-2020).  The  
last July this warm or warmer was 2019 with 74.0°F.
The maximum daily temperature for the month was 99°F and occurred on  
July 10, 2020.  
The minimum daily temperature for the month was 50°F and occurred on  
July 1, 2020.

## [PDF page 2]
Figure 1: July temperature time series.
Misc. Temperature (record status, thresholds, etc.):
No temperature records for July 2020
90F Degree Days:  
July 2020 had 17 days at or above 90F.  The average number of  
days in the 90s for  July is 9.
Through the end of July, there have been 26 days at or above 90F  
this summer.  The avera  ge number of days in the 90s through July  
is 13.

## [PDF page 3]
Precipitation and Snowfall:  
Total monthly precipitation was 0.15” which is 1.56” below the 1981-2010  
normal for the month (9% of normal).  This ranks as the 5th driest in the 132-  
year record (1889-2020).  The last July this parched was 2002 with 0.07” of  
precipitation.
Figure 2: Top 10 driest July precipitation  
totals on record.
Water year precipitation through July totaled 11.02” which is 2.15” below  
the 1981-2010 normal for the water year (84% of normal).  This ranks as the  
53rd driest start to a water year in the 131-year record (1890-2020).  The last  
water year this dry or drier through July was 2013 with 11.00” of  
precipitation.
July had 5 days with measurable precipitation (≥ 0.01”) and 14 days with a  
trace of precipitation (less than 0.01”)

## [PDF page 4]
Figure 3: July precipitation  time series.
Misc. Precipitation (predominant type, record status, etc.):
No precipitation records for July.
The highest one-day precipitation total for July 2020 was 0.06” falling on  
July 13th (cue sad trombone).
</excerpt>
### Rank 2 of 42 — 0.46
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
*   #### Warm, sunny Wednesday in Philadelphia region   
*   #### Spencer Gibson sworn in as Denver's new postmaster   
*   #### Coldest temperatures so far this season to arrive in North Texas
© 2020 CBS Broadcasting Inc. All Rights Reserved.

# Denver Weather: July 2020 Average Temp Makes Top 10 Warmest On Record
### Featured Local Savings
CBS News Colorado Live
</excerpt>
### Rank 3 of 42 — 0.40
<excerpt title="May 2020 Climate Summary">
## [PDF page 4]
of S outh Dakota, and southeastern North Dakota. Across  Above: The three -month temperature probability outlook (top), the  
par ts of the western U.S., there is an increased chance for be-  three -month precipitation probability outlook (middle), and the U.S.  
low-normal precipitation. I  n the High P lains, this inc ludes  Seasonal Drought Outlook (bottom). For more information on these  
western Colorado, much of Wyoming, and far western Nor th  outlooks, produced by the Climate Prediction Center, see:  
Dakota.  Elsewhere, there are equal chances for above-,  http://www.cpc.ncep.noaa.gov.  
below-, and near-normal precipitation through August.  
Drought  
The May 21st Seasonal Drought O utlook indicates that drought is expected to persist or develop across much  
of the West and isolated areas of the P lains. Drought may improve or be removed across portions of the south-  
ern U.S., part of F lorida, and portions of the P lains. In the High Plains region, drought conditions are expect-  
ed to persist across much of Colorado, western Kansas, west-central North Dakota, and northern South Dakota.  
Drought conditions may improve or be removed across portions of west-central Kansas over the next three months.

## [PDF page 5]
Station Summaries: By the Numbers
Colorado  Temperatures (degrees F)  Precipitation (inches)  
Averages  Extremes  Totals  
Max  Min  Mean  Depart  High  Date  Low  Date  Obs  Depart  % Norm
Akron  Washington  County Airport  71.6  43.4  57.5  0.4  92  05/31  29  05/09  2.84  -0.08  97  
Alamosa San Luis Airport  79.2  36.3  57.7  6.5  87  05/18  27  05/21  0.23  -0.35  40  
Colorado Springs Municipal Airport  74.1  44.3  59.2  3.3  89  05/19+  32  05/09  1.15  -0.88  57  
Denver  International Airport  75.0  44.2  59.6  2.5  92  05/19  30  05/05  1.65  -0.47  78  
Grand Junction Walker Field Airport  81.5  50.2  65.8  4.2  94  05/29  37  05/05  0.10  -0.78  11  
Pueblo  Memorial Airport  82.1  47.9  65.0  4.6  97  05/30  36  05/09  0.27  -1.24  18
</excerpt>
### Rank 4 of 42 — 0.35
<excerpt title="May 2020 Climate Summary">
## [PDF page 5]
Station Summaries: By the Numbers
Colorado  Temperatures (degrees F)  Precipitation (inches)  
Averages  Extremes  Totals  
Max  Min  Mean  Depart  High  Date  Low  Date  Obs  Depart  % Norm
Akron  Washington  County Airport  71.6  43.4  57.5  0.4  92  05/31  29  05/09  2.84  -0.08  97  
Alamosa San Luis Airport  79.2  36.3  57.7  6.5  87  05/18  27  05/21  0.23  -0.35  40  
Colorado Springs Municipal Airport  74.1  44.3  59.2  3.3  89  05/19+  32  05/09  1.15  -0.88  57  
Denver  International Airport  75.0  44.2  59.6  2.5  92  05/19  30  05/05  1.65  -0.47  78  
Grand Junction Walker Field Airport  81.5  50.2  65.8  4.2  94  05/29  37  05/05  0.10  -0.78  11  
Pueblo  Memorial Airport  82.1  47.9  65.0  4.6  97  05/30  36  05/09  0.27  -1.24  18
</excerpt>
### Rank 5 of 42 — 0.17
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

## Search 5 — query: "Denver International Airport July 2020 mean max mean min temperature site:ncei.noaa.gov"
### Rank 1 of 240 — 0.13 (passed on)
<excerpt title="Monthly Climate Reports | National Climate Report | July 2021">
# Monthly Climate Reports
## National Climate Report
2018 National Climate National Climate Report for September 2018 Access NowOctober 2018 National Climate National Climate Report for October 2018 Access NowNovember 2018 National Climate National Climate Report for November 2018 Access NowDecember 2018 National Climate National Climate Report for December 2018 Access NowAnnual 2018 National Climate National Climate Report for Annual 2018 Access NowJanuary 2019 National Climate National Climate Report for January 2019 Access NowFebruary 2019 National Climate National Climate Report for February 2019 Access NowMarch 2019 National Climate National Climate Report for March 2019 Access NowApril 2019 National Climate National Climate Report for April 2019 Access NowMay 2019 National Climate National Climate Report for May 2019 Access NowJune 2019 National Climate National Climate Report for June 2019 Access NowJuly 2019 National Climate National Climate Report for July 2019 Access NowAugust 2019 National Climate National Climate Report for August 2019 Access NowSeptember 2019 National Climate National Climate Report for September 2019 Access NowOctober 2019 National Climate National Climate Report for October 2019 Access NowNovember 2019 National Climate National Climate Report for November 2019 Access NowDecember 2019 National Climate National Climate Report for December 2019 Access NowAnnual 2019 National Climate National Climate Report for Annual 2019 Access NowJanuary 2020 National Climate National Climate Report for January 2020 Access NowFebruary 2020 National Climate National Climate Report for February 2020 Access NowMarch 2020 National Climate National Climate Report for March 2020 Access NowApril 2020 National Climate National Climate Report for April 2020 Access NowMay 2020 National Climate National Climate Report for May 2020 Access NowJune 2020 National Climate National Climate Report for June 2020 Access NowJuly 2020 National Climate National Climate Report for July 2020 Access NowAugust
</excerpt>
### Rank 2 of 240 — 0.10
<excerpt title="Monthly Climate Reports | National Climate Report | February 2020">
# Monthly Climate Reports
## National Climate Report
2018 National Climate National Climate Report for September 2018 Access NowOctober 2018 National Climate National Climate Report for October 2018 Access NowNovember 2018 National Climate National Climate Report for November 2018 Access NowDecember 2018 National Climate National Climate Report for December 2018 Access NowAnnual 2018 National Climate National Climate Report for Annual 2018 Access NowJanuary 2019 National Climate National Climate Report for January 2019 Access NowFebruary 2019 National Climate National Climate Report for February 2019 Access NowMarch 2019 National Climate National Climate Report for March 2019 Access NowApril 2019 National Climate National Climate Report for April 2019 Access NowMay 2019 National Climate National Climate Report for May 2019 Access NowJune 2019 National Climate National Climate Report for June 2019 Access NowJuly 2019 National Climate National Climate Report for July 2019 Access NowAugust 2019 National Climate National Climate Report for August 2019 Access NowSeptember 2019 National Climate National Climate Report for September 2019 Access NowOctober 2019 National Climate National Climate Report for October 2019 Access NowNovember 2019 National Climate National Climate Report for November 2019 Access NowDecember 2019 National Climate National Climate Report for December 2019 Access NowAnnual 2019 National Climate National Climate Report for Annual 2019 Access NowJanuary 2020 National Climate National Climate Report for January 2020 Access NowFebruary 2020 National Climate National Climate Report for February 2020 Access NowMarch 2020 National Climate National Climate Report for March 2020 Access NowApril 2020 National Climate National Climate Report for April 2020 Access NowMay 2020 National Climate National Climate Report for May 2020 Access NowJune 2020 National Climate National Climate Report for June 2020 Access NowJuly 2020 National Climate National Climate Report for July 2020 Access NowAugust
</excerpt>
### Rank 3 of 240 — 0.06
<excerpt title="U.S. Climate Normals - National Centers for Environmental Information">
## Daily Gridded Normals
### Variables and Values
The variables available as daily normals include daily maximum, minimum, and mean temperatures and daily average, month-to-date, and year-to date precipitation totals. The same smoothing methods that are used to generate daily normals for observation stations have been applied to the values for each grid cell to make them transition smoothly from one day to another. The daily temperature normals are constrained so their monthly averages equal the monthly temperature normals, and the daily precipitation normals are adjusted to total to the monthly precipitation normals.

## Daily Gridded Normals
### Time Frames
The 30-year normal set is derived from daily values for 1991–2020. There are also 15-year normals for 2006–2020 that provide a more recent period of reference. The data are found in six netCDF files for each normal set. Each data file has grids for 365 calendar days and is approximately 1.2 GB in size. February 29 values are provided for the three temperature datasets and daily precipitation, and are simply the average of February 28 and March 1 values.
_**Figure 2:**An example of 1991–2020 daily gridded normals for May 1 mean temperature (°F)._
Daily Gridded Normals Data Table
| 1991–2020 Daily Normals | 2006–2020 Daily Normals |  
| --- | --- |  
| Daily Precipitation | Daily Precipitation |  
| Month-to-Date Precipitation | Month-to-Date Precipitation |  
| Year-to-Date Precipitation | Year-to-Date Precipitation |  
| Maximum Temperature | Maximum Temperature |  
| Minimum Temperature | Minimum Temperature |  
| Mean Temperature | Mean Temperature |

## Daily Gridded Normals
### Resources
*   See the Daily Gridded Normals Readme for a description of the file contents and structure  
*   For more information about the production of the dataset, see the Daily Gridded Normals Documentation

## ENSO Gridded Climate Normals
ENSO Normals 2020 is a monthly climatology product that covers the contiguous United States. These monthly climate normals are provided for five different phase categories of ENSO: Strong La Niña, Weak La Niña, Neutral, Weak El Niño, and Strong El Niño. The resulting climatologies are centered around a 15-yr running average (instead of the traditional 30-year normal) to account for the impacts of climate change. Arguez et al. (2019) describes the methods used to generate the ENSO normals in detail.
ENSO Status: 1950–2020
The product suite includes monthly climate normals of daily maximum temperature, daily minimum temperature, and precipitation. In addition to the monthly ENSO-adjusted normals, quantile values are provided for the 10th, 25th, 75th, and 90th percentiles. The product is intended for users in climate-sensitive industries and activities to plan for a broad array of possible ENSO impacts in a changing climate.
The data are in three netCDF files, one each for maximum temperature, minimum temperature, and precipitation. Each data file is approximately 1.1 GB.
*   ENSO_MaxTemp  
*   ENSO_MinTemp  
*   ENSO_Precip

## ENSO Gridded Climate Normals
### Resources
*   See theENSO Normals Readme for a description of file contents and structure.  
*   For more information about the production of the dataset, see the ENSO Normals Documentation.
</excerpt>
### Rank 4 of 240 — 0.06
<excerpt title="Monthly Climate Reports | National Climate Report | July 2021">
# Monthly Climate Reports | National Climate Report | July 2021 | National Centers for Environmental Information (NCEI)
Skip to main content
NOAA's National Centers for Environmental Information

# Monthly Climate Reports
1.   Home  
2.   Climate Monitoring  
3.   Monthly Climate Reports  
4.   National Climate  
5.   July 2021
*   Monthly Report  
*   Summary Info  
*   Climate Briefings  
*   RSS
Use the form below to select from a collection of monthly summaries recapping climate-related occurrences on both a global and national scale.
Report:
Year:
Month:

# Monthly Climate Reports
## National Climate Report
July 2021
*   All  
*   National  
*   Global
National
Assessing the U.S. Climate Monthly assessment of the National Climate Access NowNational Climate Report An analysis of national temperatures and precipitation each month, placing the data into a historical perspective Access NowDrought Report A monthly discussion of U.S. drought status, with narrative and graphics Access NowWildfires Report A summary of wildfires in the U.S. and related weather and climate conditions Access NowNational Snow and Ice Report A national view of snow and ice conditions by month, placing the data and significant events into a historical perspective Access NowTornadoes Report A summary of tornadic activity in the Contiguous U.S. Access NowSynoptic Discussion A summary of synoptic activity in the U.S. Access Now
Global
Assessing the Global Climate Monthly assessment of the Global Climate Access NowGlobal Climate Report An analysis of global temperatures and precipitation, placing the data into a historical perspective Access NowGlobal Drought Narrative A monthly narrative on the state of global drought Access NowUpper Air Report Tropospheric and stratospheric temperatures, with data placed into historical perspective Access NowTropical Cyclones Report A breakdown of hurricanes, typhoons, cyclones, and tropical storms across the globe Access NowGlobal Snow and Ice Report A global view of snow and ice, placing the data into a historical perspective Access Now
Discontinued
Regional Analysis A summary of global regional temperature anomalies, placing the data into a historical perspective Access NowGlobal Hazards Weather-related hazards and disasters around the world Access NowEl Niño/Southern Oscillation Atmospheric and oceanic conditions related to ENSO Access Now
All20262025202420232022202120202019201820172016201520142013201220112010200920082007200620052004200320022001200019991998
</excerpt>
### Rank 5 of 240 — 0.06
<excerpt title="Monthly Climate Reports | National Climate Report | May 2020">
### Regional Highlights
#### High Plains Region _(Information provided by the High Plains Regional Climate Center)_
*   Temperatures varied across the High Plains during the month of May, with below-normal temperatures across roughly the eastern half of the region, and above-normal temperatures across the western half. The dividing line between the above- and below-normal temperatures generally extended from north-central Wyoming through southwestern Kansas. Although temperature departures did reach upwards of 6.0 degrees F (3.3 degrees C) below normal in some isolated areas in the east, this was not enough for widespread records to occur. To the west, however, where temperature departures were up to 6.0 degrees F (3.3 degrees C) above normal, many locations ranked in the top 10 warmest Mays on record. One of these locations was Alamosa, CO, which is located in south-central Colorado, just to the southwest of the Great Sand Dunes National Park and Preserve. With an average temperature of 57.7 degrees F (14.3 degrees C), Alamosa had its warmest May on record. The previous record occurred in both May 1996 and May 1984 with an average monthly temperature of 55.2 degrees F (12.9 degrees C) (period of record 1906-present). Interestingly, only two days during the month of May 2020 were below normal in Alamosa - May 21st and May 25th. Other locations that ranked in the top 10 warmest Mays on record included Pueblo, CO (6th warmest); Colorado Springs, CO (9th warmest); and Grand Junction, CO (9th warmest). While Denver, CO did not rank in the top 10 warmest Mays, Denver did observe its first 90.0 degrees F (32.2 degrees C) day three weeks earlier than average.  
*

### Regional Highlights
#### High Plains Region _(Information provided by the High Plains Regional Climate Center)_
Overall, May was a dry month across the High Plains region, with only a few areas receiving near normal to above-normal precipitation. Much of Wyoming, southern and western Colorado, western Kansas, and western North Dakota had precipitation totals of less than 50 percent of normal, which contributed to the degradation of drought conditions in these areas. May precipitation deficits were in excess of 1.50 inches (38 mm) in parts of east-central Wyoming and southwestern North Dakota. The dry conditions led to several locations ranking in the top 10 driest Mays on record. For instance, Lander, WY, which has a period of record extending back to 1892, tied for its driest May on record with only 0.06 inches (2 mm) of precipitation. May is typically the wettest month of the year in Lander, so it will be difficult to overcome deficits in the short term. Other locations ranking in the top 10 included Casper, WY (driest); Pueblo, CO (5th driest); Grand Junction, CO (10th driest); and Sheridan, WY (10th driest). Although dry conditions were widespread, there were some areas that received above-normal precipitation, such as central and northern Nebraska, central South Dakota, and eastern Kansas. In these areas, precipitation totals were up to 200 percent of normal. One particularly wet location was Parsons, KS, which is located in the southeast corner of the state. The Parsons 2 NW COOP station received 12.66 inches (322 mm) of precipitation this month, which was 6.73 inches (171 mm) above normal, or 213 percent of normal precipitation. Although this was enough to rank as the 4th wettest May on record, last year’s record-setting amount of 19.27 inches (489 mm) firmly held (period of record 1925-present). A nearby Kansas Mesonet station, called Parsons, received slightly more precipitation, with 13.72 inches (348 mm). Interestingly, May was a quiet month for severe weather, not just for the High Plains region, but for the nation as a whole.
</excerpt>

## Search 6 — query: "USW00003017 July 2020 mean daily max mean daily min"
### Rank 1 of 23 — 0.26 (passed on)
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
*   #### Warm, sunny Wednesday in Philadelphia region   
*   #### Spencer Gibson sworn in as Denver's new postmaster   
*   #### Coldest temperatures so far this season to arrive in North Texas
© 2020 CBS Broadcasting Inc. All Rights Reserved.

# Denver Weather: July 2020 Average Temp Makes Top 10 Warmest On Record
### Featured Local Savings
CBS News Colorado Live
</excerpt>
### Rank 2 of 23 — 0.13
<excerpt title="Denver, CO Weather History">
# Denver, CO
## Summary
| Temperature (°C) | Max | Average | Min |  
| --- | --- | --- | --- |  
| Max Temperature | 24 | 16.32 | 8 |  
| Avg Temperature | 12.88 | 9.03 | 5.84 |  
| Min Temperature | 8 | 4.05 | 1 |
| Precipitation (mm) | Max | Average | Min | Sum |  
| --- | --- | --- | --- | --- |  
| Precipitation | 2.01 | 0.2 | 0 | 3.82 |
| Dew Point (°C) | Max | Average | Min |  
| --- | --- | --- | --- |  
| Dew Point | 6.2 | -2.63 | -15.67 |
| Wind (km/h) | Max | Average | Min |  
| --- | --- | --- | --- |  
| Wind | 48 | 24.16 | 15 |  
| Gust Wind | 61 | 48.38 | 39 |
| Sea Level Pressure (hPa) | Max | Average | Min |  
| --- | --- | --- | --- |  
| Sea Level Pressure | 831.7 | 826.17 | 818.14 |

# Denver, CO
## Daily Observations
| Date | Temp High/Low | Dew Pt High/Low | Humidity | Wind | Max Wind | Wind Gust | Pressure | Precip. | Condition |  
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |  
| 11/1/2026 | 15 °C / 8 °C | 9 °C / 5 °C | 80 % |  | 26 km/h | - | 818.45 hPa | 1.26 mm |  |  
| 11/2/2026 | 10 °C / 6 °C | 7 °C / -1 °C | 70 % |  | 48 km/h | - | 822.11 hPa | 2.53 mm |  |  
| 11/3/2026 | 13 °C / 4 °C | 3 °C / 0 °C | 67 % |  | 26 km/h | - | 828.21 hPa | 0.03 mm |  |  
| 11/4/2026 | 13 °C / 2 °C | 2 °C / 0 °C | 72 % |  | 17 km/h | - | 824.32 hPa | 0 mm |  |  
| 11/5/2026 | 15 °C / 1 °C | 1 °C / -4 °C | 59 % |  | 20 km/h | - | 828.5 hPa | 0 mm |  |  
| 11/6/2026 | 15 °C / 3 °C | 1 °C / -4 °C | 53 % |  | 17 km/h | - | 829.71 hPa | 0 mm |  |
</excerpt>
### Rank 3 of 23 — 0.07
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
Golden Triangle Station1°Change station

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
| Max Temperature | 24 | 16.32 | 8 |  
| Avg Temperature | 12.88 | 9.03 | 5.84 |  
| Min Temperature | 8 | 4.05 | 1 |
| Precipitation (mm) | Max | Average | Min | Sum |  
| --- | --- | --- | --- | --- |  
| Precipitation | 2.01 | 0.2 | 0 | 3.82 |
| Dew Point (°C) | Max | Average | Min |  
| --- | --- | --- | --- |  
| Dew Point | 6.2 | -2.63 | -15.67 |
| Wind (km/h) | Max | Average | Min |  
| --- | --- | --- | --- |  
| Wind | 48 | 24.16 | 15 |  
| Gust Wind | 61 | 48.38 | 39 |
| Sea Level Pressure (hPa) | Max | Average | Min |  
| --- | --- | --- | --- |  
| Sea Level Pressure | 831.7 | 826.17 | 818.14 |
</excerpt>
### Rank 4 of 23 — 0.07
<excerpt title="Monthly Climate Reports | National Climate Report | July 2020">
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
### Rank 5 of 23 — 0.06
<excerpt title="U.S. Climate Normals - National Centers for Environmental Information">
## Daily Gridded Normals
### Variables and Values
The variables available as daily normals include daily maximum, minimum, and mean temperatures and daily average, month-to-date, and year-to date precipitation totals. The same smoothing methods that are used to generate daily normals for observation stations have been applied to the values for each grid cell to make them transition smoothly from one day to another. The daily temperature normals are constrained so their monthly averages equal the monthly temperature normals, and the daily precipitation normals are adjusted to total to the monthly precipitation normals.

## Daily Gridded Normals
### Time Frames
The 30-year normal set is derived from daily values for 1991–2020. There are also 15-year normals for 2006–2020 that provide a more recent period of reference. The data are found in six netCDF files for each normal set. Each data file has grids for 365 calendar days and is approximately 1.2 GB in size. February 29 values are provided for the three temperature datasets and daily precipitation, and are simply the average of February 28 and March 1 values.
_**Figure 2:**An example of 1991–2020 daily gridded normals for May 1 mean temperature (°F)._
Daily Gridded Normals Data Table
| 1991–2020 Daily Normals | 2006–2020 Daily Normals |  
| --- | --- |  
| Daily Precipitation | Daily Precipitation |  
| Month-to-Date Precipitation | Month-to-Date Precipitation |  
| Year-to-Date Precipitation | Year-to-Date Precipitation |  
| Maximum Temperature | Maximum Temperature |  
| Minimum Temperature | Minimum Temperature |  
| Mean Temperature | Mean Temperature |

## Daily Gridded Normals
### Resources
*   See the Daily Gridded Normals Readme for a description of the file contents and structure  
*   For more information about the production of the dataset, see the Daily Gridded Normals Documentation

## ENSO Gridded Climate Normals
ENSO Normals 2020 is a monthly climatology product that covers the contiguous United States. These monthly climate normals are provided for five different phase categories of ENSO: Strong La Niña, Weak La Niña, Neutral, Weak El Niño, and Strong El Niño. The resulting climatologies are centered around a 15-yr running average (instead of the traditional 30-year normal) to account for the impacts of climate change. Arguez et al. (2019) describes the methods used to generate the ENSO normals in detail.
ENSO Status: 1950–2020
The product suite includes monthly climate normals of daily maximum temperature, daily minimum temperature, and precipitation. In addition to the monthly ENSO-adjusted normals, quantile values are provided for the 10th, 25th, 75th, and 90th percentiles. The product is intended for users in climate-sensitive industries and activities to plan for a broad array of possible ENSO impacts in a changing climate.
The data are in three netCDF files, one each for maximum temperature, minimum temperature, and precipitation. Each data file is approximately 1.1 GB.
*   ENSO_MaxTemp  
*   ENSO_MinTemp  
*   ENSO_Precip

## ENSO Gridded Climate Normals
### Resources
*   See theENSO Normals Readme for a description of file contents and structure.  
*   For more information about the production of the dataset, see the ENSO Normals Documentation.
</excerpt>

## Search 7 — query: "Atlanta airport July 2020 mean Tmax mean Tmin USW0001284"
### Rank 1 of 42 — 0.03 (passed on)
<excerpt title="Severe thunderstorms moving through metro Atlanta have forced a ...">
•
Follow
* * *
Severe thunderstorms moving through metro Atlanta have forced a temporary ground stop at Hartsfield-Jackson Atlanta International Airport this morning, delaying thousands of travelers.  
Reminder: TSA employees are still working without pay due to the partial government shutdown. Staffing shortages are contributing to long security lines.
📷 @garrettdrake
Get the government out of airport security and this won't be a problem
Reply
I’ve got to fly tomorrow, so will someone be there to tell you where the end of the line is? Is it crazy to think about taking a bag? Or does that make any difference?
Reply
THANK A DEMOCRATIC
Reply
Reply
Reply
We keep telling people GA is full, don't come here.
Reply
Been there - done that
Reply
I went through in under 2 minutes on Saturday. And I’m on my way back now, so you all better be out of my way!
Reply
The turned the government employee services back on just to make the employees collect money.
Reply
TWO HOURS!!??
Reply
Yup! Madness everywhere. Using the Queue Travel app is the ONLY app that tells you the TSA wait time AND calculates when to arrive at the airport to avoid missing your flight.
Reply
Yall stay home or drive to ur destination 😭😭😭😂💀😵‍💫
1 like
Reply
11.7K 507
</excerpt>
### Rank 2 of 42 — 0.03
<excerpt title="The Federal Aviation Administration issued a ground stop at Hartsfield ...">
# Instagram
Log In
Sign Up
Never miss a post from wsbtv
Sign up for Instagram to stay in the loop.
By continuing, you agree to Instagram's Terms of Use and Privacy Policy.
Sign up
Log in
wsbtv
•
Follow
* * *
wsbtv18w
The Federal Aviation Administration issued a ground stop at Hartsfield-Jackson Atlanta International Airport due to thunderstorms in the area. More details at link in bio
onlyonejeff18w
Aaaaaahhhhhhh Im on the ramp…not sure about that. Operations still moving forward, matter of fact as of the current time, 1811 hrs, its about to get very busy in next few hrs.
3 likes
Reply
770 2
July 12
Log in to like or comment.
* * *
More posts from wsbtv
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
### Rank 3 of 42 — 0.02
<excerpt title="Atlanta, Hartsfield - Jackson Atlanta International Airport">
### The data displayed on this page is considered preliminary and is subject to quality control review and adjustment.


### We are aware that the download data feature is not available. At this time, there is no estimate on when this will return.
**Font:****A****A****A**Advanced Options About This Page
* * *
Unit of
Measurement Number of Hours
to Retrieve Page Headers See Chart Permanent
Chart Gather Historical
Data Observation
Type Show Only
Hourly Data Font Size Precip.
View  
Standard (w/mph)
Metric
Standard (w/kts)Standard
Minimal
None On
Off On Tabular
METARs
(NWS/FAA Only)Yes
No Full
Standard
Measured
General Information
Charts
Options/Settings
Color Coding
Cloud Information
Precipitation
Snow
Download Data
Contact
By default, this page will load with all station data collected in the last 72 hours, with the station identifier as the "site" variable in the URL
Example: https://www.weather.gov/wrh/timeseries?site=kslc
If the station reports Temperature, Relative Humidity, or Dew Point Temperature, a chart will be available with those elements to examine.
Below the chart, a table will appear with 72 hours worth of data from that station. Hovering over certain headings will reveal a "magnifying glass" cursor. That means that if you click on that heading, data for that element will load into the chart. **Note**: Data availability varies by station.
**Pages With and Without Chart**
The default station chart contains Temperature, Dew Point Temperature, and Relative Humidity. If a station has not reported any of those elements during the requested period, no chart will be available.
A chart other than the default may be selected by clicking the "Advanced Options" button and selecting an option from the "Permanent Chart" drop down menu.
The chart has a limitation where 1000 data points per element can be displayed. For longer duration datasets, with multiple reports per hour, this will exceed the charting capability. Therefore, data will be trimmed when it exceeds 1000 datapoints, and will then display every 2nd, 3rd, etc point. If you require high resolution charts, the "Historical Data" option will be helpful.

### We are aware that the download data feature is not available. At this time, there is no estimate on when this will return.
*   Example 1: A NWS ASOS reports 12 - 13 times an hour. After 76 hours, data will be trimmed in the chart.  
*   Example 2: A station that reports 4 times an hour will begin trimming data after 250 hours.
To view charts for additional elements, using a mouse, move the cursor over the element headings. If a "magnifying glass" cursor appears, it means that if you click on that heading, data for that element will load into the chart. See image below.
The following weather elements are available for viewing in a chart. **Note**: Data availability varies by station.
*   Temperature  
*   Dew Point Temperature  
*   Relative Humidity  
*   Wind Chill  
*   Wind Direction  
*   Wind Speed and Gusts  
*   Fuel Temperature  
*   Fuel Moisture  
*   Sea Level Pressure  
*   Altimeter Setting  
*   Station Pressure  
*   Solar Radiation  
*   Soil Temperature*   Road Temperature  
*   Road Sub-Surface Temperature  
*   Accumulated Precipitation  
*   One Minute Precipitation  
*   Five Minute Precipitation  
*   Ten Minute Precipitation  
*   Fifteen Minute Precipitation  
*   Thirty Minute Precipitation  
*   One Hour Precipitation  
*   Snow Depth  
*   Snow Interval  
*   Snow-Water Equivalent  
*   Water Temperature  
**Mouse over Chart Headings to reveal Magnifying Glass, Then Click for Chart**
Clicking the "Settings" icon will open an area where you can select different viewing parameters.
</excerpt>
### Rank 4 of 42 — 0.02
<excerpt title="Ground stop issued at Hartsfield-Jackson Atlanta International Airport ...">
By
Alex Sanz Managing Editor, CBS News Atlanta  
Alex Sanz is a veteran journalist and managing editor of CBS Atlanta. He works closely with journalists across the newsroom to deliver original reporting and compelling, high-impact storytelling across broadcast, digital and streaming platforms.
Read Full Bio
Updated on: November 13, 2026 / 6:56 PM EST / CBS Atlanta
Add CBS News on Google
Hartsfield-Jackson Atlanta International Airport has been put under a ground stop due to an unusual alert by the Federal Aviation Administration.
Atlanta is just one of the airports across the country reporting closures or ground stops on Friday afternoon. While the FAA's website noted that Hartsfield-Jackson was under a "departure delay," the airport confirmed with CBS News Atlanta that all outgoing flights have been stopped.
The federal agency wrote in an alert that the ground stop was "due to extraordinary circumstances and for reasons of safety."
According to a post on X by Transportation Secretary Sean Duffy, the nationwide ground stop is due to a communication issue impacting all air traffic control centers.
"FAA technicians are investigating the issue," Duffy wrote.
At a press conference after the alert was issued, U.S. Secretary of Homeland Security Markwayne Mullin said that the public had no reason to be afraid and that the situation was connection with a telecommunication outage.
"There was no indication as of yet this was a nefarious attack against us," Mullin said.
In a statement, Atlanta airport officials say that arriving flights will be permitted to land, but departures are temporarily suspended. Travelers should check with their airlines for any updates to their flights this evening.
According to Flight Aware, more than 3,000 planes are in the air over the U.S. While those planes may land, they might not necessarily find an open jet bridge to deplane once they get to the gates. More than 380 departing flights were delayed and 187 were cancelled as of 7 p.m. Hundreds more arriving flights were also seeing delays.

## Atlanta deploying emergency personnel to airport
While the ground stop remains ongoing, the city of Atlanta says its police and fire departments will deploy additional emergency personnel and resources to the airport to support operations.
"The safety and well-being of passengers, airport employees and flight crew remain our highest priority," city officials said in a press release.
Authorities said they are closely monitoring the situation.

## United and American respond to flight issues
United and American Airlines said in statements on X that flights already in the air will continue.
United Airlines said while domestic flights will not depart, "international departures are being managed on a case-by-case basis by the FAA."
American Airlines said it expects disruptions for the rest of the day.
"It will be all hands on deck across American to get customers on their way as soon as possible when the FAA lifts this nationwide ground stop," the airline said.

## A rare nationwide ground stop
Nationwide ground stops are rare, with only two since 2001. There was a nationwide ground stop on Sept. 11 because of the terrorist attacks at the World Trade Center and at the Pentagon.
Another ground stop in 2023 paused departures nationwide after the outage of a critical pilot notification system.
_This is a developing story. Check back with CBS News Atlanta for more updates._
The Associated Press contributed to this report.
In:
*   Hartsfield-Jackson Atlanta International Airport  
*   Atlanta
</excerpt>
### Rank 5 of 42 — 0.02
<excerpt title="Conditions improving at Atlanta airport after national ground stop ⬇️">
# Conditions improving at Atlanta... - News 12 26 Augusta | Facebook
## News 12 26 Augusta's Post
[3d](https://www.facebook.com/wrdwtv/posts/pfbid0eWTvkuRM2brHfKkwRELitLo4efjujTxw4Y7CbenNqKDcvgT8jm9Ue4454NMseJiul?__cft__[0]=AZiHTt08THca5jT1HDTNrP5auuK3A3ns5Up1m3or0IN1NZBf_NV2Hl3COCu5J6bJCRNTwge88Y6i8t2Kde6WG9ww5T0avUFdvBIeh6EHAwb7fCHT74eMlLRrVhT1ioDXhlZeCZ_6XVtNrxHU2nPx2ivalUN5IT8P&__tn__=%2CO%2CP-R) ·
Conditions improving at Atlanta airport after national ground stop
[](https://www.facebook.com/photo/?fbid=1577845414389330&set=a.645212924319255&__cft__[0]=AZiHTt08THca5jT1HDTNrP5auuK3A3ns5Up1m3or0IN1NZBf_NV2Hl3COCu5J6bJCRNTwge88Y6i8t2Kde6WG9ww5T0avUFdvBIeh6EHAwb7fCHT74eMlLRrVhT1ioDXhlZeCZ_6XVtNrxHU2nPx2ivalUN5IT8P&__tn__=EH-R)
![Image 4](blob:http://localhost/520c193f0276d495fb772a9afb8b220d)
![Image 5](blob:http://localhost/85d8b181a20aeb64a3afc2f1c39d2480)
All reactions:
5
1 comment

# Conditions improving at Atlanta... - News 12 26 Augusta | Facebook
## News 12 26 Augusta's Post
Like
Comment
Most relevant
[](https://www.facebook.com/wrdwtv?comment_id=Y29tbWVudDoxNTc3ODQ1NDI3NzIyNjYyXzI2NTEwNzI0MjIwNjUyNjc%3D&__cft__[0]=AZiHTt08THca5jT1HDTNrP5auuK3A3ns5Up1m3or0IN1NZBf_NV2Hl3COCu5J6bJCRNTwge88Y6i8t2Kde6WG9ww5T0avUFdvBIeh6EHAwb7fCHT74eMlLRrVhT1ioDXhlZeCZ_6XVtNrxHU2nPx2ivalUN5IT8P&__tn__=R]-R)
Author
[News 12 26 Augusta](https://www.facebook.com/wrdwtv?comment_id=Y29tbWVudDoxNTc3ODQ1NDI3NzIyNjYyXzI2NTEwNzI0MjIwNjUyNjc%3D&__cft__[0]=AZiHTt08THca5jT1HDTNrP5auuK3A3ns5Up1m3or0IN1NZBf_NV2Hl3COCu5J6bJCRNTwge88Y6i8t2Kde6WG9ww5T0avUFdvBIeh6EHAwb7fCHT74eMlLRrVhT1ioDXhlZeCZ_6XVtNrxHU2nPx2ivalUN5IT8P&__tn__=R]-R)
</excerpt>

## Search 8 — query: "NCEI monthly data MLY_TMAX station USW00003017 2020-07"
### Rank 1 of 21 — 0.06 (passed on)
<excerpt title="NCEI Past Weather Tool">
# NCEI Past Weather Tool | Drought.gov
*   Drought Basics  
    *   Short-Term vs Long-Term Drought  
    *   Ecological Drought  
    *   Flash Drought  
    *   Snow Drought  
    *   Soil Moisture and Drought  
    *   Historical Drought  
    *   Monitoring Drought  
    *   Resources for Teachers and Students
Drought Research in Action
*   Funding Opportunities  
    *   National Coordinated Soil Moisture Monitoring Network  
    *   Understanding Upper Missouri River Basin Soil Moisture and Snowpack  
    *   Resources for Soil Moisture Network Operators  
    *   NIDIS Drought and Wildland Fire Nexus (NDAWN)  
    *   Drought Assessment in a Changing Climate  
    *   Communicating About Drought  
    *   Drought Relief, Recovery, and Support
*   About
What is NIDIS? NIDIS is a multi-agency partnership that coordinates drought monitoring, forecasting, planning, and information at national, state, and local levels across the country.     
    *   About NIDIS  
    *   Who We Are  
    *   Partners  
    *   Tribal Engagement  
    *   About the U.S. Drought Portal  
    *   Integrated Information Systems
What is Drought Early Warning?
A drought early warning system (DEWS) utilizes new and existing networks of federal, tribal, state, local, and academic partners to make climate and drought science accessible and useful for decision makers and stakeholders.
*   Drought Early Warning  
    *   Drought Early Warning Activities
*   News and Events
News & Events View the latest drought-related news, upcoming events, and recordings and summaries of past webinars.     
    *   Latest News  
    *   Upcoming Webinars & Events  
    *   Past Events
Local Drought Information
Get timely updates on local drought conditions, outlooks, and impacts from NIDIS and its partners.
*   Sign Up for NIDIS Emails  
    *   Regional Drought Status Updates  
    *   National Weather Service Drought Information Statements
*   Mobile Social
Site Section
Data & Maps

# NCEI Past Weather Tool
Associated Agencies
National Oceanic and Atmospheric Administration (NOAA) National Centers for Environmental Information
Data Coverage
Global
Data Type
Land-based Station
Period of Record
1763–Present (Varies by Station)
File Format
pdf
text (ascii)
csv
json
xml
The NOAA National Centers for Environmental Information (NCEI) Past Weather Tool allows users to search for historical temperature, precipitation, snowfall, and snow depth data for individual weather stations across the United States, as well as many international locations. Stations are part of the GHCN (Global Historical Climatology Network)-Daily dataset.

# NCEI Past Weather Tool
## Access
Past Weather Tool

# NCEI Past Weather Tool
## How To
*   Use the search bar to enter a location of interest (e.g., city, address, zip code). Or, use the map to find a location by using zoom/pan or Shift+Click+Drag and then click "Search this area.” A set of stations from that location will be displayed (if any exist). Select the desired station from the list or from the map to view available daily data for that station.  
*   Adjust the date in the “Selected Date” field and select a dataset (average temperature, maximum temperature, minimum temperature, precipitation, snowfall, or snow depth) to view a time series for that indicator.  
*   Above the time series, click the “1 year” button to view a time series for 1 year through the selected date. Click the button with the selected date to view the values on that date every year over the full period of record for that station (e.g., the average temperature every August 25 from 1962 to 2021 for Lakewood, CO).  
*   Use the links below the time series to download the data or a PDF monthly weather report for that station.  
*   For more information, click the “i” icon next to the station name. A popup will provide links to station history and further details through the Historical Observing Metadata Repository (HOMR).
</excerpt>
### Rank 2 of 21 — 0.06
<excerpt title="U.S. Climate Normals">
## Source Grids
There are two types of monthly gridded normals for the contiguous United States. One set expresses the averages for 1991–2020, 2006–2020, and 1901–2000. The second consists of averages and other statistics conditioned by the El Niño/Southern Oscillation (ENSO) phase. The nClimGrid dataset (Vose et al. 2014) was the input for both sets of gridded normals.
The nClimGrid dataset contains monthly gridded temperature and precipitation. Vose et al. used climatologically aided interpolation to transform NCEI’s extensive collection of station temperature and precipitation values into nClimGrid monthly grids at a 1/24 degree latitude/longitude spatial resolution (about 4km) covering the contiguous United States.

## Monthly Gridded Climate Normals
The nClimGrid monthly data provides a nearly homogenous temperature time series and a serially complete precipitation record. Unlike complex station climate normals, monthly gridded normals are simple averages of the maximum temperature, minimum temperature, mean temperature, and precipitation totals for each month of the year.
The 30-year normal is an average of months from 1991 to 2020. For example, the 30-year January maximum temperature normal is the average of the 30 January values between 1991 and 2020. This is the gridded monthly normal to use for most activities that require spatially complete or high-resolution climatologies. For users who require representation of a period closer to the present, a normal for 2006–2020 is also provided. For longer term climate change study comparisons, we also produced the 20th Century Baseline, a set of averages from 1901–2000. Climate normals for climate seasons of March-April-May, June-July-August, September-October-November, December-January-February and annual periods are also available.
_**Figure 1:** An example of 1991-2020 monthly gridded normals for April mean temperature (°F) and precipitation (inches). The data are found in four netCDF files for each normal or baseline set, one each for maximum temperature, minimum temperature, mean temperature, and precipitation. Each data file is approximately 275 MB._
Monthly Gridded Normals Data Table
| 1991–2020 Monthly Normals | 2006–2020 Monthly Normals | 1901–2000 Monthly Baseline |  
| --- | --- | --- |  
| Precipitation | Precipitation | Precipitation |  
| Maximum Temperature | Maximum Temperature | Maximum Temperature |  
| Minimum Temperature | Minimum Temperature | Minimum Temperature |  
| Mean Temperature | Mean Temperature | Mean Temperature |

## Monthly Gridded Climate Normals
### Resources
*   See the Monthly Gridded Normals Readme for a description of the file contents and structure.  
*   For more information about the production of the dataset, see the Monthly Gridded Normals Documentation.

## Daily Gridded Normals
The Daily Gridded Climate Normals Dataset is derived from the nClimGrid Daily Dataset, and can be used to calculate daily anomalies or examine the climatology of individual days of the year.

## Daily Gridded Normals
### Variables and Values
The variables available as daily normals include daily maximum, minimum, and mean temperatures and daily average, month-to-date, and year-to date precipitation totals. The same smoothing methods that are used to generate daily normals for observation stations have been applied to the values for each grid cell to make them transition smoothly from one day to another. The daily temperature normals are constrained so their monthly averages equal the monthly temperature normals, and the daily precipitation normals are adjusted to total to the monthly precipitation normals.
</excerpt>
### Rank 3 of 21 — 0.05
<excerpt title="nClimGrid-Daily | National Centers for Environmental Information (NCEI)">
NCEI’s nClimGrid-Daily product contains gridded fields and area averages of daily maximum, minimum, and average temperatures (Tmax, Tmin, and Tavg) and daily precipitation amount (Prcp) for the Contiguous United States (CONUS) from January 1, 1951–present.
The dataset is designed for climate monitoring and other applications that rely on placing event-specific meteorological patterns into a long-term historical context. Data are derived from morning and midnight observations from the Global Historical Climatology Network-daily (GHCNd) dataset, and contain processing techniques that address the spatial and temporal variations that affect the quality and homogeneity of the fields.

## Current Version
The current version of nClimGrid-Daily is v1.0.0, which supersedes the public beta version that was previously available. V1 contains auxiliary observation counts at each grid point that indicate uncertainty related to observation density, as well as enhanced documentation and census tract averages based on the 2020 U.S. Census.

## How do I access NClimGrid


## Contact
### Updates
There are two ways to get alerts about nClimGrid-Daily updates dataset updates, outages, and other relevant information:
1.   Fill out our User Registration Form  
2.   Subscribe to API Alerts at https://www.ncei.noaa.gov/alerts/nclimgriddaily/api (requires programming experience)

## Contact
### Feedback
You can submit feedback and questions via the nClimGrid-Daily User Registration Form, or by emailing [ncei.grids@noaa.gov](mailto:ncei.grids@noaa.gov).

## How to Cite
Durre, I., M. F. Squires, R. S. Vose, A. Arguez, W. S. Gross, J. R. Rennie, and C. J. Schreck, 2022b: NOAA's nClimGrid-Daily Version 1 – Daily gridded temperature and precipitation for the Contiguous United States since 1951. NOAA National Centers for Environmental Information, since 6 May 2022, https://doi.org/10.25921/c4gt-r169.
Data are derived from morning and midnight observations from the Global Historical Climatology Network-daily (GHCNd) dataset, and contains processing techniques that address spatial and temporal variations that affect the quality and homogeneity of the fields.
Area averages are available for common regional groupings, including census tracts, counties, climate divisions, states, major hydrologic units, and Weather Forecast Office regions. Data are also available for report-specific regions from NCEI's climate monitoring reports and the Fifth National Climate Assessment (NCA5).
The nClimGrid-Daily auxiliary product provides daily gridded fields of counts of the number of Tmax, Tmin, and Prcp observations within 48.3 km (30 miles) of each grid point. These counts were designed to help the U.S. Army Corps of Engineers determine uncertainty in the grid point estimates.

## Daily Grids
Gridded fields for this product are bundled into one Network Common Data Format (NetCDF) file per month, and area averages are stored in Comma-Separated Value (CSV) files for each variable, region, and month.
Download Daily Grids

## Auxiliary Data
The nClimGrid-Daily-Auxiliary folder contains one netCDF file for each month of the time scale, with each file providing the observation counts for Tmax, Tmin, and Prcp at each grid point for each day of the month.
*   **User Guide****:** Provides basic information, references with additional information, and points of contact for the collection and processing of nClimGrid-Daily.  
*   **Journal Article (Durre et al. 2022)****:** Daily High-Resolution Temperature and Precipitation Fields for the Contiguous United States from 1951 to Present (doi: 10.1175/JTECH-D-22-0024.1)

## Spatial Resolution
The gridded fields cover the land area between approximately 24°N and 49°N and between 67°W and 125°W at a resolution of 1/24 of a degree (0.0417°).
_Precipitation accumulation and average temperature for the contiguous United States on September 2nd, 2021, when Hurricane Ida brought more than three inches of rain to areas in the Northeast._
</excerpt>
### Rank 4 of 21 — 0.05
<excerpt title="NCEI Past Weather Tool">
# NCEI Past Weather Tool
## How To
*   Use the search bar to enter a location of interest (e.g., city, address, zip code). Or, use the map to find a location by using zoom/pan or Shift+Click+Drag and then click "Search this area.” A set of stations from that location will be displayed (if any exist). Select the desired station from the list or from the map to view available daily data for that station.  
*   Adjust the date in the “Selected Date” field and select a dataset (average temperature, maximum temperature, minimum temperature, precipitation, snowfall, or snow depth) to view a time series for that indicator.  
*   Above the time series, click the “1 year” button to view a time series for 1 year through the selected date. Click the button with the selected date to view the values on that date every year over the full period of record for that station (e.g., the average temperature every August 25 from 1962 to 2021 for Lakewood, CO).  
*   Use the links below the time series to download the data or a PDF monthly weather report for that station.  
*   For more information, click the “i” icon next to the station name. A popup will provide links to station history and further details through the Historical Observing Metadata Repository (HOMR).

# NCEI Past Weather Tool
## Documentation
All stations are part of the GHCN (Global Historical Climatology Network)-Daily dataset. GHCN-Daily data may lag by a few days due to a comprehensive set of quality assurance checks. Only data with blank quality flags (i.e., that did not fail any quality assurance checks) are returned.
Partner(s)

# NCEI Past Weather Tool
## Documentation
#### National Centers for Environmental Information (NCEI)


# NCEI Past Weather Tool
## Documentation
#### National Environmental Satellite, Data, and Information Service (NESDIS)
Representative Image
Past Weather Tool
Stay Connected
Subscribe to NIDIS emails for the latest regional drought updates, webinars, and news. Or, sign up to receive drought alerts when the U.S. Drought Monitor or U.S. Drought Outlook updates for your city/zip code.
Sign Up For Emails
Drought.gov
National Integrated Drought Information System
A multi-agency partnership that coordinates drought monitoring, forecasting, planning, and information at national, state, and local scales.
Feedback

# NCEI Past Weather Tool
## Documentation
#### Help Improve This Site ✖Close
*   Contact Us  
*   Satisfaction Survey  
*   Data Download

# NCEI Past Weather Tool
## Footer Submenu
*   Accessibility  
*   Disclaimer  
*   FOIA  
*   Information Quality  
*   Protecting Your Privacy  
*   USA.gov
</excerpt>
### Rank 5 of 21 — 0.05
<excerpt title="NCEI Past Weather Tool">
# NCEI Past Weather Tool | Drought.gov
Skip to main content
An official website of the United States government
Here’s how you know
Here's how you know
**The .gov means it’s official.**
Federal government websites often end in .gov or .mil. Before sharing sensitive information, make sure you’re on a federal government site.
**The site is secure.**
The **https://** ensures that you are connecting to the official website and that any information you provide is encrypted and transmitted securely.
Drought.gov
National Integrated Drought Information System
Open Search Bar Menu
Query Search
Query Search
Close
*   Mobile Branding  Drought.gov    
National Integrated Drought Information System     
*   Data and Maps
Find Data   
    *   Current Conditions  
    *   Drought Impacts  
    *   Historical Information  
    *   Outlooks and Forecasts  
    *   All Data
Explore More Current Conditions
*   Agriculture  
    *   Fire  
    *   Paleoclimate  
    *   Public Health  
    *   Snow Drought  
    *   Soil Moisture  
    *   Temperature & Precipitation  
    *   Vegetation  
    *   Water Supply
*   By SectorAgriculture  Ecosystems  Energy  Hazard Planning & Preparedness  Manufacturing  Navigation and Transportation  Public Health  Recreation and Tourism  Water Utilities  Wildfire Management      
*   By Location
Select a Location Location Search     
    *   Select a State
Browse by scale
*   International  
    *   National  
    *   Tribal  
    *   Watershed  
    *   Regional  
    *   State  
    *   County  
    *   Local
Browse by Regional Drought Early Warning System (DEWS)
*   California-Nevada  
    *   Intermountain West  
    *   Mid-Atlantic  
    *   Midwest  
    *   Missouri River Basin  
    *   Northeast  
    *   Pacific Northwest  
    *   Southeast  
    *   Southern Plains
*   Research and Learn
Science & Reports NIDIS supports drought research through advancing the scientific understanding of the mechanisms that lead to drought as well as improving the coordination and delivery of drought information.     
    *   Advancing Drought Early Warning through Interdisciplinary Research  
    *   Featured Reports and Outlooks  
    *   All Documents and Reports
What is Drought?
</excerpt>

## Search 9 — query: ""Denver International Airport" "July 2020" "mean daily maximum" "NCEI""
(no page could be scored)

## Search 10 — query: "USW00003017 2020 July PDF monthly summary"
### Rank 1 of 37 — 0.25 (passed on)
<excerpt title="Summary of Monthly Normals 1991-2020">
# Summary of Monthly Normals


# 1991-2020
Generated on 11/19/2026
Precipitation (in.)
Totals Mean Number of Days
Precipitation Probabilities
Probability that precipitation will be
equal to or less than
the indicated amount
Means Daily Precipitation Monthly Precipitation
vs. Probability Levels
Month Mean >= 0.01 >= 0.10 >= 0.50 >= 1.00 0.25 0.50 0.75
01 0.38 4.4 1.3 0.0 0.0 0.23 0.34 0.53
02 0.41 5.5 1.5 0.0 0.0 0.18 0.31 0.58
03 0.86 6.2 2.5 0.3 0.0 0.40 0.80 1.08
04 1.68 9.0 4.4 0.8 0.4 0.89 1.35 2.45
05 2.16 10.4 5.3 1.5 0.4 1.32 1.77 2.92
06 1.94 8.1 4.2 1.2 0.2 0.75 1.72 2.53
07 2.14 8.3 4.2 1.2 0.6 0.94 1.41 3.53
08 1.58 7.5 3.6 1.0 0.2 0.82 1.22 2.55
09 1.35 6.0 2.7 0.6 0.1 0.40 0.86 1.45
10 0.99 5.3 2.5 0.5 0.1 0.50 0.89 1.34

# 1991-2020
11 0.64 4.6 1.8 0.1 0.0 0.32 0.47 0.70
12 0.35 4.4 1.4 0.0 0.0 0.14 0.28 0.54
Summary 14.48 79.7 35.4 7.2 2.0 6.89 11.42 20.20
Empty or blank cells indicate data is missing or insufficient occurrences to compute value U.S. Department of Commerce National Centers for Environmental Information
National Oceanic & Atmospheric Administration 151 Patton Avenue
National Environmental Satellite, Data, and Information Service Asheville, North Carolina 28801
Current Location: Elev: 5414 ft. Lat: 39.8328° N Lon: 104.6575° W
Station: DENVER INTL AP, CO US USW00003017

# Summary of Monthly Normals
</excerpt>
### Rank 2 of 37 — 0.21
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
### Rank 3 of 37 — 0.18
<excerpt title="Summary of Monthly Normals 1991-2020">
U.S. Department of Commerce National Centers for Environmental Information
National Oceanic & Atmospheric Administration 151 Patton Avenue
National Environmental Satellite, Data, and Information Service Asheville, North Carolina 28801
Current Location: Elev: 5414 ft. Lat: 39.8328° N Lon: 104.6575° W
Station: DENVER INTL AP, CO US USW00003017

# Summary of Monthly Normals


# 1991-2020
Generated on 11/19/2026
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
### Rank 4 of 37 — 0.17
<excerpt title="July 2020 - Monthly Climate Summary">
### Daily Data Report
7/16/2020 87 60 73.5<-4 0 9 0  
7/17/2020 93 72 82.5<4.9 0 18 0  
7/18/2020 94 73 83.5<5.9 0 19 T  
7/19/2020 95 68 81.5<3.8 0 17 1.55  
7/20/2020 85 69 77<-0.7 0 12 0.32  
7/21/2020 88 71 79.5<1.8 0 15 T  
7/22/2020 88 70 79<1.3 0 14 0  
7/23/2020 90 72 81<3.3 0 16 0.06  
7/24/2020 90 70 80<2.3 0 15 0  
7/25/2020 91 72 81.5<3.8 0 17 T  
7/26/2020 91 72 81.5<3.8 0 17 0  
7/27/2020 88 70 79<1.3 0 14 0.83  
7/28/2020 86 69 77.5<-0.2 0 13 0  
7/29/2020 89 72 80.5<2.8 0 16 0.3  
7/30/2020 82 70 76<-1.7 0 11 1.44  

### Daily Data Report
7/31/2020 72 64 68<-9.7 0 3 0.19  
Sum 2748 2155-<-0 444 4.83  
Average 88.6 69.5 79.1<1.8---  
Normal 88.1 66.5 77.3<-1 382 4.44
</excerpt>
### Rank 5 of 37 — 0.17
<excerpt title="July 2020 - Monthly Climate Summary">
### Daily Data Report
7/15/2020 94 76 85<6.8 0 20 0  
7/16/2020 94 70 82<3.8 0 17 1.45  
7/17/2020 82 73 77.5<-0.8 0 13 0.27  
7/18/2020 90 71 80.5<2.2 0 16 0  
7/19/2020 92 74 83<4.7 0 18 0  
7/20/2020 93 73 83<4.7 0 18 0  
7/21/2020 90 70 80<1.7 0 15 1.28  
7/22/2020 86 71 78.5<0.2 0 14 0.3  
7/23/2020 91 69 80<1.6 0 15 0.2  
7/24/2020 91 69 80<1.6 0 15 0  
7/25/2020 89 72 80.5<2.1 0 16 0  
7/26/2020 91 72 81.5<3.1 0 17 0  
7/27/2020 89 73 81<2.7 0 16 0.07  
7/28/2020 86 73 79.5<1.2 0 15 0.01  
7/29/2020 89 73 81<2.7 0 16 0.16  

### Daily Data Report
7/30/2020 90 73 81.5<3.2 0 17 T  
7/31/2020 84 67 75.5<-2.8 0 11 0.14  
Sum 2777 2170-<-0 467 5.06  
Average 89.6 70 79.8<1.8---  
Normal 89.5 66.6 78<-0 405 3.55
Vichy, MO Daily Data
</excerpt>

# Example 3
## Question
Everdina de Weert was born in the The Netherlands in June of 1918. Who are her grandparents and in what years and cities did each pair of grandparents get married?

## Expected answer
Dirk Smaling and Willemina Dohmen married 1874 in Zwolle, Albertus de Weert and Hendrikje Beeuwkes married 1880 in Apeldoorn

## Grade 0.00

## Search 1 — query: "Everdina de Weert born June 1918 Netherlands grandparents married city year""
### Rank 1 of 1506 — 0.32 (passed on)
<excerpt title="Dutch Emigrant Families Assisted by the Immigration Committee of the ...">
## [PDF page 48]
Origin: Honselersdijk, Zuid Holland -- Arrival  Origin: Apeldoorn, Gelderland -- Arrival year:  
year: 1961  1951  
Destination: 4237 SE Weidler St, Portland  Destination: 169 Third St, Port Credit, Ontario  
Oregon  Brandsma, Duut  
Branderhorst, Jan G - born: 27 Feb 1917  Family Size: 1; Religion: Christian Reformed  
Spouse: Vanden Berg - Family Size: 13;  Origin: Helpman, Groningen -- Arrival year:  
Religion: Christian Reformed  1952  
Children: Herman; Geertje; Everdina; Frans;  Destination: Edmonton, Alberta  
Hilde; Gertjan; Trudy; Evert; Peter; Cornelis;  Brandsma, Reinder - born: 9 Feb 1926  
Sonja; Johan  Family Size: 1; Religion: Christian Reformed  
Origin: Honselersdijk, Zuid Holland -- Arrival  Origin: Uithuizen, Groningen -- Arrival year:  
year: 1961  1950  
Destination: 4227 SE Weidler St, Portland,  Sponsor: Stetson H A - Destination: Fort  
Oregon  Saskatchewan, Alberta  
Branderhorst, Johanna P - born: 24 Aug  Brandsma, Stoffer  
1929  Family Size: 1; Religion: Christian Reformed  
Spouse: Thur - Family Size: 3; Religion:  Origin: Uithuizen, Groningen -- Arrival year:  
Christian Reformed  1953  
Children: Pieternella; Johannes  Destination: Smithers, British Columbia  
Origin: Genderen, Noord Brabant -- Arrival  Brandt, Ailco  
year: 1958  Family Size: 2; Religion: Christian Reformed  
Destination: Revelstoke, British Columbia  Origin: Winsum, Groningen -- Arrival year:  
Branderhorst, Johannes  1952  
Family Size: 6; Religion: Christian Reformed  Sponsor: Aukema John - Destination: RR 1,
</excerpt>
### Rank 2 of 1506 — 0.28
<excerpt title="Dutch Emigrant Families Assisted by the Immigration Committee of the ...">
## [PDF page 47]
Destination: Kitchener, Ontario  Origin: Winsum, Groningen -- Arrival year:  
Brand, Hendrik J - born: 6 Apr 1930  1953  
Family Size: 1; Religion: Christian Reformed  Destination: Neerlandia, Alberta  
Origin: Mijndrecht, Zuid Holland -- Arrival year:  Branderhorst, Evert J - born: 17 Mar 1915  
1953  Spouse: Vander Ende - Family Size: 7;  
Destination: London, Ontario  Religion: Christian Reformed  
Brand, Jasper  Children: Everdina; Tom; Nelly; Maria;  
Family Size: 11; Religion: Christian Reformed  Herman; Evert
47  © 2015, Archives, Calvin College

## [PDF page 48]
Origin: Honselersdijk, Zuid Holland -- Arrival  Origin: Apeldoorn, Gelderland -- Arrival year:  
year: 1961  1951  
Destination: 4237 SE Weidler St, Portland  Destination: 169 Third St, Port Credit, Ontario  
Oregon  Brandsma, Duut  
Branderhorst, Jan G - born: 27 Feb 1917  Family Size: 1; Religion: Christian Reformed  
Spouse: Vanden Berg - Family Size: 13;  Origin: Helpman, Groningen -- Arrival year:  
Religion: Christian Reformed  1952  
Children: Herman; Geertje; Everdina; Frans;  Destination: Edmonton, Alberta  
Hilde; Gertjan; Trudy; Evert; Peter; Cornelis;  Brandsma, Reinder - born: 9 Feb 1926  
Sonja; Johan  Family Size: 1; Religion: Christian Reformed  
Origin: Honselersdijk, Zuid Holland -- Arrival  Origin: Uithuizen, Groningen -- Arrival year:  
year: 1961  1950  
Destination: 4227 SE Weidler St, Portland,  Sponsor: Stetson H A - Destination: Fort  
Oregon  Saskatchewan, Alberta  
Branderhorst, Johanna P - born: 24 Aug  Brandsma, Stoffer  
1929  Family Size: 1; Religion: Christian Reformed  
Spouse: Thur - Family Size: 3; Religion:  Origin: Uithuizen, Groningen -- Arrival year:  
Christian Reformed  1953  
Children: Pieternella; Johannes  Destination: Smithers, British Columbia  
Origin: Genderen, Noord Brabant -- Arrival  Brandt, Ailco  
year: 1958  Family Size: 2; Religion: Christian Reformed  
Destination: Revelstoke, British Columbia  Origin: Winsum, Groningen -- Arrival year:  
Branderhorst, Johannes  1952  
Family Size: 6; Religion: Christian Reformed  Sponsor: Aukema John - Destination: RR 1,
</excerpt>
### Rank 3 of 1506 — 0.21
<excerpt title="Dutch Emigrant Families Assisted by the Immigration Committee of the ...">
## [PDF page 253]
Origin: Barendrecht, Zuid Holland -- Arrival  Origin: Groningen, Groningen -- Arrival year:  
year: 1957  1954  
Sponsor: Van Dyk B - Destination: Box 71, St  Destination: 455 Superior St, Sarnia, Ontario  
Davids, Ontario  Nierop, Grietje E - born: 27 Aug 1928  
Nienhuis, E  Family Size: 1; Religion: Christian Reformed  
Spouse: Kruize - Family Size: 1; Religion:  Origin: Bennekom, Gelderland -- Arrival year:  
Christian Reformed  1960  
Origin: Spijk, Groningen -- Arrival year: 1959  Sponsor: Knoller H F - Destination: 633 10th  
Destination: Vauxhall, Alberta  Ave, South Burnaby, British Columbia  
Nienhuis, Elsje  Nierop, Klaas  
Spouse: Sterenberg - Family Size: 1; Religion:  Family Size: 1; Religion: Christian Reformed  
Christian Reformed  Origin: Andijk, Zuid Holland -- Arrival year:  
Origin: Spijk, Groningen -- Arrival year: 1954  1952  
Nienhuis, G  Sponsor: De Jong A - Destination: 1814  
Spouse: Buwalda - Family Size: 1; Religion:  Nanaimo St, New Westminster, British  
Christian Reformed  Columbia  
Origin: Ulrum, Groningen -- Arrival year: 1954  Nierop, Willem  
Sponsor: Gramms E G - Destination: Box 509,  Family Size: 1; Religion: Christian Reformed  
Calgary, Alberta  Origin: Andijk, Noord Holland -- Arrival year:  
Nienhuis, Hendrikus J - born: 15 Jan 1932  1954  
Family Size: 1; Religion: Christian Reformed  Sponsor: Nierop K - Destination: Westminster,  
Origin: Groningen, Groningen -- Arrival year:  British Columbia  
1954  Nieuwenhout, Jantje  

## [PDF page 253]
Destination: 455 Superior St, Sarnia, Ontario  Spouse: Tinge - Family Size: 1; Religion:  
Nienhuis, Jan - born: 10 Jun 1918  Christian Reformed  
Spouse: Nauta - Family Size: 4; Religion:  Origin: Leeuwarden, Friesland -- Arrival year:  
Christian Reformed  1953  
Origin: Assen, Drenthe -- Arrival year: 1951  Destination: 11215 93rd St, Edmonton, Alberta  
Destination: Ripon, California  Nieuwenhuis, A  
Nienhuis, Martje - born: 13 May 1916  Spouse: Kollen - Family Size: 1; Religion:  
Spouse: Snip - Family Size: 1; Religion:  Christian Reformed  
Christian Reformed  Origin: Ommen, Drenthe -- Arrival year: 1948
253  © 2015, Archives, Calvin College
</excerpt>
### Rank 4 of 1506 — 0.17
<excerpt title="Dutch Emigrant Families Assisted by the Immigration Committee of the ...">
## [PDF page 428]
Vander Wees, Geertruida  Spouse: Lagendyk - Family Size: 1; Religion:  
Spouse: Storm - Family Size: 1; Religion:  Christian Reformed  
Christian Reformed  Origin: Bennekom, Gelderland -- Arrival year:  
Origin: Loosduinen, Zuid Holland -- Arrival  1954  
year: 1951  Destination: Vancouver, British Columbia  
Destination: Fort William, Ontario  Vander Wekken, Johannes  
Vander Wees, Johannes  Family Size: 1; Religion: Christian Reformed  
Spouse: Vander Sar - Family Size: 5; Religion:  Origin: Bennebroek, Gelderland -- Arrival year:
428  © 2015, Archives, Calvin College

## [PDF page 429]
1954  Alberta  
Destination: Edmonton, Alberta  Vander Werf, J G  
Vander Wel, Cornelia M  Family Size: 7; Religion: Christian Reformed  
Family Size: 1; Religion: Christian Reformed  Origin: Nijemirdum, Friesland -- Arrival year:  
Origin: De Lier, Zuid Holland -- Arrival year:  1952  
1953  Sponsor: Jacobs C A - Destination: RR 1,  
Sponsor: Vermeer C - Destination: RR 1,  Smithville, Ontario  
Grimsby, Ontario  Vander Werf, Johanna - born: 5 May 1938  
Vander Wel, Cornelia Maria - born: 22 Jun  Family Size: 1; Religion: Christian Reformed  
1918  Origin: Utrecht, Utrecht -- Arrival year: 1958  
Family Size: 1; Religion: Presbyterian  Sponsor: Wouters B G - Destination: 12220  
Origin: Vleuten, Utrecht -- Arrival year: 1949  88th St, Edmonton, Alberta  
Destination: 15 Grange St, Leamington,  Vander Werf, Simkje - born: 23 Aug 1910  
Ontario  Spouse: Span - Family Size: 1; Religion:  
Vander Wel, Cornelis F  Christian Reformed  
Family Size: 1; Religion: Christian Reformed  Origin: Akkerwoude, Friesland -- Arrival year:  
Origin: De Meern, Utrecht -- Arrival year: 1950  1951  
Destination: Kingsville, Ontario  Destination: Edmonton, Alberta  
Vander Wel, Douwe Siebe - born: 24 Oct  Vander Werf, T  
1922  Family Size: 1; Religion: Reformed  
Family Size: 2; Religion: Christian Reformed  Arrival year: 1948  
Arrival year: 1948  Sponsor: MacCab J A - Destination: RR 1,  
Sponsor: Fingland H - Destination: Deseronto,  Tillsonburg, Ontario  
Ontario  Vander Werf, Trijntje
</excerpt>
### Rank 5 of 1506 — 0.17
<excerpt title="Dutch Emigrant Families Assisted by the Immigration Committee of the ...">
## [PDF page 429]
1954  Alberta  
Destination: Edmonton, Alberta  Vander Werf, J G  
Vander Wel, Cornelia M  Family Size: 7; Religion: Christian Reformed  
Family Size: 1; Religion: Christian Reformed  Origin: Nijemirdum, Friesland -- Arrival year:  
Origin: De Lier, Zuid Holland -- Arrival year:  1952  
1953  Sponsor: Jacobs C A - Destination: RR 1,  
Sponsor: Vermeer C - Destination: RR 1,  Smithville, Ontario  
Grimsby, Ontario  Vander Werf, Johanna - born: 5 May 1938  
Vander Wel, Cornelia Maria - born: 22 Jun  Family Size: 1; Religion: Christian Reformed  
1918  Origin: Utrecht, Utrecht -- Arrival year: 1958  
Family Size: 1; Religion: Presbyterian  Sponsor: Wouters B G - Destination: 12220  
Origin: Vleuten, Utrecht -- Arrival year: 1949  88th St, Edmonton, Alberta  
Destination: 15 Grange St, Leamington,  Vander Werf, Simkje - born: 23 Aug 1910  
Ontario  Spouse: Span - Family Size: 1; Religion:  
Vander Wel, Cornelis F  Christian Reformed  
Family Size: 1; Religion: Christian Reformed  Origin: Akkerwoude, Friesland -- Arrival year:  
Origin: De Meern, Utrecht -- Arrival year: 1950  1951  
Destination: Kingsville, Ontario  Destination: Edmonton, Alberta  
Vander Wel, Douwe Siebe - born: 24 Oct  Vander Werf, T  
1922  Family Size: 1; Religion: Reformed  
Family Size: 2; Religion: Christian Reformed  Arrival year: 1948  
Arrival year: 1948  Sponsor: MacCab J A - Destination: RR 1,  
Sponsor: Fingland H - Destination: Deseronto,  Tillsonburg, Ontario  
Ontario  Vander Werf, Trijntje
</excerpt>

## Search 2 — query: ""Everdina de Weert" 1918 grandparents"
(no page could be scored)

## Search 3 — query: "Everdina de Weert genealogy"
### Rank 1 of 86 — 0.40 (passed on)
<excerpt title="Everdina van de WEERTHOF (1892–1978) • FamilySearch">
## Everdina van de WEERTHOF
Female
30 April 1892–30 December 1978
•
When Everdina van de WEERTHOF was born on 30 April 1892, in Ede, Gelderland, Netherlands, her father, Willem van de WEERTHOF, was 27 and her mother, Marretje Jansen, was 24. She married Marinus Slagmolen on 26 February 1916, in Ede, Gelderland, Netherlands. They were the parents of at least 1 son and 3 daughters. She died on 30 December 1978, at the age of 86.
Marriage
26 February 1916 Ede, Gelderland, Netherlands

## Everdina van de WEERTHOF
### Children (4)
As a nonprofit, we offer free help to those looking to learn the details of their family story.
Create a FREE Account
There are no historical documents attached to Everdina.

## Everdina van de WEERTHOF
### 1899 · Hague Peace Convention
Age 7
The Hague Peace Convention was a series conferences that produced treaties and declarations. The convention took place in Hague, Netherlands. The conferences were among the first formal statements of the laws of war and war crimes in secular international law.

## Everdina van de WEERTHOF
### 1904 · Weerdinge Couple Found in Bog
Age 12
Two skeletons were found next to each other in Drenthe, Netherlands. The skeletons were dated back to between 160 BC and 220 AD. One of the skeletons was thought to be a female and the other a male so scientists called them the Weerdinge couple or Mr. and Mrs. Veenstra. It was determined that both skeletons were men and the name was changed to Weerdinge Men.

## Everdina van de WEERTHOF
### 1917
Age 25
WWI. Despite Dutch neutrality in World War I (1914-18), the Netherlands suffers from severe food shortages, triggering street riots.
1860
1880
1900
1920
1940
1960
1980
2000
2020
Marinus Slagmolen
1886–1953
Everdina van de WEERTHOF
1892–1978
Marriage: 26 February 1916
Cornelia Maria Slagmolen
1916–Deceased
Marretje Slagmolen
1917–2019
Dirkje Johanna Gijsberta Slagmolen
1918–Deceased
Gijsbertus Slagmolen
1921–1989

## Everdina van de WEERTHOF
### Siblings (2)
Some characteristic forenames: Vietnamese Anh, Thanh, Hung, Minh, Vinh, Dung, Hue, Huong, Lan, Quang, Tan, Thuy, Hong, Chi, Hang, Ho, Pok, Sang, Bai, Chin, Ching, Chu, Chuan, Dong.
Vietnamese (**Vạn**): from the Chinese surname 萬, see Wan 1.
Vietnamese (**Văn**): from the Chinese surnames 文 or 聞, see Wen 2 and 3, and also 5 below.
Dictionary of American Family Names © Patrick Hanks 2003, 2006.
**Possible Related Names**
</excerpt>
### Rank 2 of 86 — 0.23
<excerpt title="DE JONGH FAMILY TREE">
## [PDF page 29]
Penciled annotation to Family Notes reads: "Winnie married a Skouras boy in Athens; he was killed while a  
hostage during [World War] II. The Skouras family in America had Winnie and her son come over to the  
States." Cousin Colin Fraser (102) writes: "Winnie told me that she had a tough time during the occupation  
[of Greece in World War II] after her husband was shot. However, by the time I arrived [1948] they (Winnie,  
Eva and the baby boy) were living in a very nice house outside Athens ... not far from Aunt Dora." (Eva is  
spouse of Eric de Jongh, 70; Aunt Dora is Dora de Jongh C see Sophia Dorothea "Dora" Purser in H&D, PFT.)  
As reported in letter dated 31-8-1955 from Dora to her daughter Dorothy Daniëls (see Dorothy Sophia de  
Jongh in H&D), Winnie married Ed Herscher after having worked some years at Greek Embassy in  
Washington and the couple visited Greece on their honeymoon. While there they went for a cruise on the  
yacht of Tommy Rees, son of Henry Richard de Jongh's (1862-1935 - see H&D) business associate Thomas  
Bowen Rees.
..... Skouras was owner of chain of cinemas. Killed in WW II "while a hostage" (penciled notation in Family  
Notes). According to Douglas Oscar Fraser (101) he was "shot by nazis as suspected spy for Allies". Ed was  
"attorney and property owner" (Douglas).
Issue (1):
143 i. Thanos "Tommy"7 Skouras, b. ca. 1941.
----------------------------------------------------------------------------------------------------
HENRY AND DORA AND THEIR DESCENDANTS
(NB: Place of birth, marriage and death for all individuals prior to 1922 is Smyrna unless otherwise noted.)
Generation No. 4

## [PDF page 29]
1. Henry Richard de Jongh b. 17-12-1862, d. 16-8-1935 in Athens, Greece, m. 17-6-1891 Sophia Dorothea  
"Dora" Purser b. 28-7-1870, d. 30-8-1964 in Athens.
Shipowner, industrialist. Director of Egypt & Levant Steamship Co. Ltd., manager of Thomas Bowen Rees &  
Co. Ltd. Built "De Jongh house" in Boudjah around turn of century. Left TBR after WWI, moved to Nice, France  
after Great Fire and to Athens in 1926, where he launched Laïs knitwear factory and built "the big house"  
aka Villa Pikrodafne in Psihikó. Boudjah house still stands, owned by Turkish state, well maintained but  
currently (2001) unused and empty. Villa P. apparently torn down to make way for new Chinese embassy  
after serving many years as South African embassy. Ultimate fate or current (2001) status of Laïs factory  
unknown.
Dora was daughter of Edward and Sophia Purser. Edward (1821-1906), Anglo-Irish, was chief engineer and  
general manager of Smyrna-Aidin "Ottoman" Railway; Sophia was from Andros, Greece. Order of Dora's  
formal given names was somehow switched in course of life: early records call her Sophia Dorothea, later  
ones Dorothea Sophia. Villa Rhododaphne, smaller house in Psyhikó where she lived after Henry's death, still  
exists (October 2001) as private residence under new ownership.
Issue:
</excerpt>
### Rank 3 of 86 — 0.19
<excerpt title="DE JONGH FAMILY TREE">
## [PDF page 30]
3. Dorothy Sophia de Jongh b. 17-8-1893, d. 19-8-1981 in Zevenaar, Netherlands, m. 12-7-1921 in Shanghai,  
China Willem Alouisius Augustinus Maria Daniëls b. 18-12-1888 in Nijmegen, Netherlands, d. 20-3-1969 in  
Arnhem, Netherlands. Willem was Dutch diplomat.
Issue:
+ 11 i. Joanna Maria Dorothea "Joanne" Daniëls, b. 23-2-1924 in Shanghai, China, d. 16-2-1993  
in Washington, DC, USA.

+ 12 ii. Catherina Henriëtta "Trinette" Daniëls, b. 12-6-1925 in Nice, France.

+ 13 iii. Godelieve Willemien "Lee" Daniëls, b. 8-8-1928 in Arnhem, Netherlands.
14 iv. Willem Hendrik Daniels, b. 30-7-1934 in Singapore, Straits Settlements, m. 26-5-1966 in  
Athens, Greece Martha Katherine Kirmss, b. 9-9-1942 in Brooklyn, New York, USA. Div. 1972.  
Publishing manager, labourer, translator. Lives in Netherlands.
4. Helen Marian de Jongh b. 30-8-1895, d. 29-11-1982 in Rome, Italy, m. 21-8-1920 Edoardo Sebastiano  
Niccolò "Eddy" Rossi b. 9-2-1892 in Padua, Italy, d. 9-2-1962 in Rome.
Eddy ("Edo" in Italian) was Italian army officer.
Issue:
+ 15 i. Paola Vittoria Dorotea Luisa Rossi, b. 27-6-1921.

## [PDF page 30]
16 ii. Patrizio Rossi, b. 1923 in Rome, d. 1923 in Rome.
</excerpt>
### Rank 4 of 86 — 0.18
<excerpt title="DE JONGH FAMILY TREE">
## [PDF page 29]
1. Henry Richard de Jongh b. 17-12-1862, d. 16-8-1935 in Athens, Greece, m. 17-6-1891 Sophia Dorothea  
"Dora" Purser b. 28-7-1870, d. 30-8-1964 in Athens.
Shipowner, industrialist. Director of Egypt & Levant Steamship Co. Ltd., manager of Thomas Bowen Rees &  
Co. Ltd. Built "De Jongh house" in Boudjah around turn of century. Left TBR after WWI, moved to Nice, France  
after Great Fire and to Athens in 1926, where he launched Laïs knitwear factory and built "the big house"  
aka Villa Pikrodafne in Psihikó. Boudjah house still stands, owned by Turkish state, well maintained but  
currently (2001) unused and empty. Villa P. apparently torn down to make way for new Chinese embassy  
after serving many years as South African embassy. Ultimate fate or current (2001) status of Laïs factory  
unknown.
Dora was daughter of Edward and Sophia Purser. Edward (1821-1906), Anglo-Irish, was chief engineer and  
general manager of Smyrna-Aidin "Ottoman" Railway; Sophia was from Andros, Greece. Order of Dora's  
formal given names was somehow switched in course of life: early records call her Sophia Dorothea, later  
ones Dorothea Sophia. Villa Rhododaphne, smaller house in Psyhikó where she lived after Henry's death, still  
exists (October 2001) as private residence under new ownership.
Issue:

## [PDF page 29]
+ 2 i. Edward David "Eddie" de Jongh, b. 9-4-1892, d. 18-7-1964 in Australia.

+ 3 ii. Dorothy Sophia de Jongh, b. 17-8-1893, d. 19-8-1981 in Zevenaar, Netherlands.

+ 4 iii. Helen Marian de Jongh, b. 30-8-1895, d. 29-11-1982 in Rome, Italy.

+ 5 iv. Henry Richard de Jongh, b. 6-2-1897, d. 6-1-1972 in Sevenoaks, England.
</excerpt>
### Rank 5 of 86 — 0.17
<excerpt title="DE JONGH FAMILY TREE">
## [PDF page 20]
Heather Lovelock (see Heather Rosemary Whittall, 91) reports that he was chief engineer on the Delta Light  
Railway in Egypt. On daughter Dorothy Jane's birth certificate his place of residence is registered as Smyrna  
(see Dorothy notes for further Egyptian reference).
Issue:
+ 61 i. Dorothy Jane "Dolly"5 Peacock, b. 7-10-1889, d. 6-10-1960 England.

+ C ii.  Phyllis Peacock, 1891-1964, cont. in H&D as spouse of Edward David de Jongh.

+ 62 iii. Ida Peacock, b. 10-12-1893.

+ 63 iv. Daisy Peacock, b. 1895, d. Iskenderun, Turkey.

+ 64 v. Frank Peacock, b. 10-3-1896.
43. David Richard4 "Dicko" de Jongh (David Richard3, John2, "John's Father"1), b. 18-12-1857, d. 15-12-1918,  
m. (1) 25-4-1888 Charlotte Louisa Barker b. 20-10-1859, d. 18-9-1888, "no issue", (2) 14-11-1889 Aydin, Ottoman  
Empire Joanna Loiza b. 1867.
Middle name shown in Family Notes is John. Richard is name entered in StPaul, corroborated by middle  
initial R. inscribed on gravestone photographed September 2001 at All Saints cemetery, Boudjah by White.  
Occupation: banker (StPaul).
Charlotte was daughter of Richard and Mary Barker (cf. notes on Althea Barker, gen-3 C full name and  
dates from Listing and White). Joanna was daughter of Elia and Helene Loiza; NLCA file gives year of birth,  
spells name Ioanna Louizou.
Issue (2):

## [PDF page 20]
+ 65 i. Frederick Rowland5 "Freddie" de Jongh, b. 16-12-1890, d. ca. 1965 ?-Alexandria, Egypt.

+ 66 ii. Richard David de Jongh, b. 4-10-1891 d. 1965 Athens, Greece.

+ 67 iii. Louisa "Loulou" de Jongh, b. 10-3-1893, d. ca. 1967.
68 iv. Henry George "Harry" de Jongh, b. 10-9-1897, d. Athens, Greece 9-1-1958, m. 9-9-1932  
Priraeus, Greece Margarita "Rita" Mandoglou b. 4-5-1910 Adrianople, Ottoman Empire. "No  
issue". Dates of marriage and death (in Kallithea district of Athens) obtained from NLCA,  
whose records describe him as "employé ['clerk'] - unemployed". Received Dutch passport in  
1947 valid for four years. Family Notes entry for "Rita (Greek)" supplemented by NLCA.
44. Oscar John4 de Jongh (David Richard3, John2, "John's Father"1), b. 15-12-1859, d. 10-9-1922, m. Cleofe  
Brufel d. 10-9-1922.
</excerpt>

## Search 4 — query: ""Everdina de Weert" 1918 June"
(no page could be scored)

## Search 5 — query: ""de Weert" Everdina 1918"
### Rank 1 of 1010 — 0.30 (passed on)
<excerpt title="Genealogie Familie van Roekel">
i. Gerritje Mekking 1866-1921 tr 1893 Martijn Adams 1867-1935
a. Willem Adams 1894-1948 tr 1921 Jacomina Christina van den Berg 1896-
b. Gerrit Adams 1895-1949 tr 1922 Gerritje de Weerd 1894-1945
c. Gijsbertus Adams 1896
d. Anna Lucretia Maria Adams 1896
e. Anna Lucretia Maria Adams 1897- tr 1924 David Ludovicus Minjauw 1898-
j. Everdina Mekking 1867-8
k. Caspard Mekking 1871- tr 1896 Jantje Waanders 1873-
a. Christina Johanna Mekking 1897- tr 1918 Arend Jan Tesink 1894-
j. Jantje van Silfhout 1825-1900 tr 1853 Arnoldus Jacob Beekhuizen 1823-1911
a. Hendrika Beekhuizen 1853-4
b. Everdina van Beekhuizen 1855-
a. Dirk Roozeboom 1877- tr 1897 Jannetje van de Haar 1877-
b. Jantje Roozeboom 1879-
c. Bartha Roozeboom 1880-1942 tr 1912 Willem Reede 1883-1946
d. Arnolda Roozeboom 1881- tr 1906 Hendrik Jan Tieben 1883
e. Leendert Roozeboom 1883-
f. Johanna Willemina Roozeboom 1885-
g. Gerrit Roozeboom 1887-
h. Gijsbert Roozeboom 1889-
i. Maria Roozeboom 1889-91
</excerpt>
### Rank 2 of 1010 — 0.29
<excerpt title="van de Weert">
3. Willem van de Weert, geb./ged. Scherpenzeel 03-10/01-11-1857, volgt IVa

4. Gijs van de Weert, geb./ged. Scherpenzeel 11-12-1859/29-04-1860, ov. Scherpenzeel 22-05-1864

5. Willemijntje van de Weert, geb./ged. Scherpenzeel 07/25-01-1863, ov. Scherpenzeel 06-01-1867

6. Albert van de Weert, geb./ged. Scherpenzeel 07/25-01-1863, volgt IVb

7. Gijsbert van de Weert, geb./ged. Scherpenzeel 04/24-09-1865, ov. Scherpenzeel 16-03-1866
IVa
Willem van de Weert, geb./ged. Scherpenzeel 03-10/01-11-1857, klompenmaker/vrachtrijder, ov. Scherpenzeel 17-04-1940, begr. Glashorst graf nr. 450, tr. Scherpenzeel 16-09-1882 Teuntje Tins, geb. Woudenberg 10-05-1857, ov. Scherpenzeel 20-10-1933, dr. van Evert Tins en Lutje van Ginkel
Uit dit huw.:

1. Teunis van de Weert, geb./ged. Scherpenzeel 09-01/29-04-1883, ov. Scherpenzeel 25-05-1908, begr. Glashorst graf nr. 237

2. Lena Everdina van de Weert, geb./ged. Scherpenzeel 07-12-1887/29-01-1888, tr. Scherpenzeel 16-10-1915 Cornelis Bruggink, geb. Woudenberg 27-07-1889, koopman, zn. van Jan Bruggink en Alida van Donkelaar
Lidm. Scherpenzeel 16-03-1913: Lena Everdina van de Weert.
3. Evert van de Weert, geb./ged. Scherpenzeel 11-07/28-08-1892, schilder, tr. Veenendaal 18-03-1916 Hendrina Filippina Huijdink, geb. Veenendaal 1892, dr. van Jan Huijdink en Dirkje Schoeman
Uit dit huw.:
1. Dirk van de Weert, geb. Scherpenzeel 19-10-1920

4. Elisabeth van de Weert, geb./ged. Scherpenzeel 29-10/02-12-1894, tr. Scherpenzeel 24-04-1920 Elbertus Steinmann, geb. Woudenberg 13-05-1894, arbeider, zn. van Gijsbert Steinmann en Anna Gazenbeek

5. Maria van de Weert, geb./ged. Scherpenzeel 04/21-06-1896, tr. Scherpenzeel 11-05-1918 Willem Bruggink, geb. Woudenberg 25-05-1893, arbeider, zn. van Willem Bruggink en Gerritje Ploeg
</excerpt>
### Rank 3 of 1010 — 0.27
<excerpt title="R.K. DOOPBOEK TIEL 1831-1852">
# Historische en genealogische werkgroep voor de Betuwe en Bommelerwaard 1995
Corneliae Hijzelaar , echtelieden, getuigen: Joannes Hijzelaar en Henrica Kulhout .Gedoopt 5 October, Joannes Wilhelmus , zoon van Wilhelmi van Uden en van Joannae van Elk , echtelieden, getuigen: Fransciscus van Uden en Gerarda van der Wielen .Gedoopt 5 October, Petronella , dochter van Marini Teunissen en van Gertrudae Dekkers ,echtelieden, getuigen: Gerardus Dekkers en Gertruda Dekkers .Gedoopt 18 October, Cristiana Joanna , dochter van Joannis de Prins en van Martina van IJssendooren , echtelieden, getuigen: Joannes van IJssendooren en Maria Domicino .Gedoopt 23 October, Wilhelmus , zoon van Joannis van Rijn en van Elisabetae Janssen ,echtelieden, getuigen: Joannes Dijkman en Maria Dijkman .Gedoopt 28 October Joannes , zoon van Reinerii Janssen en van Henricae Petersen ,echtelieden, getuige: Gijsberta Zondag .Gedoopt 4 November, Martinus , zoon van Arnoldi van Varik , niet katholiek, en van Mariae van der Lest , echtelieden, getuigen: Christianus van Aa en Jacomina van der Lest .Gedoopt 13 November, Petronella , zoon van Nicolai van Gemert en van Arnoldae Kooijmans , echtelieden, getuigen: Joannes Kooijmans en Maria Kooijmans .Gedoopt 27 November, Margareta , dochter van Wilhelmi van Daalen en van Margaretae Kooijmans , echtelieden, getuigen: Joannes van Daalen en Arnolda van Daalen .Gedoopt 30 November, Cornelia Everdina , dochter van Joannis de Weert en van Margaretae Roemer , niet katholiek, echtelieden,
</excerpt>
### Rank 4 of 1010 — 0.26
<excerpt title="Genealogie de Jong">
## **Auteur Piet Heres Website:www.pietheres.nl (voor email zie website)**
**6 Arie de Jong**, geboren op 20-11-1887 in Stoutenburg [bron: Aktenr 26]. Arie is overleden op 30-07-1888 in Stoutenburg, 8 maanden oud [bron: Aktenr 15].
**7 Johanna de Jong**, geboren op 19-02-1890 in Stoutenburg [bron: Aktenr 5]. Johanna is overleden op 25-05-1895 in Stoutenburg, 5 jaar oud [bron: Aktenr 10].
**8 Cornelis Jacobus (Cees) de Jong**, geboren op 04-05-1892 in Stoutenburg. Volgt VI-z.
**9 Arnoldus de Jong**, geboren op 06-01-1895 in Stoutenburg [bron: Aktenr 1]. Arnoldus is overleden op 14-09-1895 in Stoutenburg, 8 maanden oud [bron: Aktenr 16].
**V-u Arend de Jong** is geboren in 1827 in Doesburg, zoon van Jacob de Jong (zie IV-o) en Catharina Bakker. Arend is overleden op 02-04-1907 in Apeldoorn (buurtschap Wormen), 79 of 80 jaar oud [bron: Aktenr 170].
Beroep:
Schipper
Arend trouwde, 28 of 29 jaar oud, op 23-01-1856 in Hattem [bron: Aktenr 1] met Catharina de Weert, 22 of 23 jaar oud. Catharina is geboren in 1833 in Amsterdam, dochter van Gerrit de Weert (Hendriks) en Harmina de Jong (zie III-i,2). Catharina is overleden op 15-04-1923 in Apeldoorn, 89 of 90 jaar oud [bron: Aktenr 197].
Kinderen van Arend en Catharina:

## **Auteur Piet Heres Website:www.pietheres.nl (voor email zie website)**
**1 Jacob Dirk de Jong**, geboren op 19-12-1856 in Apeldoorn. Volgt VI-aa.
**2 Hermina de Jong**, geboren op 25-10-1859 in Heerde [bron: Aktenr 147]. Hermina is overleden op 25-10-1911 in Wijhe, 52 jaar oud [bron: Aktenr 66].
Notitie bij Hermina:Aan boord geboren
Hermina trouwde, 20 jaar oud, op 26-02-1880 in Hattem [bron: Aktenr 3] met Koendert Harmen Scholten, 22 jaar oud. Koendert is geboren op 16-03-1857 in Veessen (Gem. Heerde) [bron: Aktenr 24], zoon van Harm Scholten en Gerritje Steenbergen. Koendert is overleden op 20-04-1915 in Amsterdam, 58 jaar oud [bron: Aktenr 23].
Beroep:
Schipper
**3 Catharina de Jong**, geboren op 02-04-1864 in Apeldoorn [bron: Aktenr 1266]. Catharina is overleden op 19-06-1892 in Amsterdam, 28 jaar oud [bron: Aktenr 63]. Zij is begraven in Hattem.
**4 Arendina de Jong**, geboren op 04-04-1866 in Apeldoorn [bron: Aktenr 125]. Arendina is overleden.
</excerpt>
### Rank 5 of 1010 — 0.24
<excerpt title="Genealogie Familie van Roekel">
a. Hendrik Ansink 1869-1937 tr 1895 Abigaël Henriëtte van Silfhout 1869-1937 tr 1919 Hendrikje van Velsen 1882-
b. Johan Ansink 1870- tr 1900 Cornelia van de Weerd 1879-1918 tr 1918 Gerritje Rijken 1878-
c. Jacob Ansink 1872-1927 tr 1905 Johanna Cornelia Heij 1877-
d. NN Ansink 1874
e. Jenneke Ansink 1876-1945 tr 1897 Hendrikus van Aggelen 1876-1956
f. Wouter Ansink 1877-1943 tr NN Kelderman
g. Willem Ansink 1880
h. Herman Ansink 1880
i. Willemina Ansink 1881
j. Willemina Ansink 1884-
k. Harmen Ansink 1886-1945 tr 1909 Petronella Alida Bouman 1884-1941
l. Evert Ansink 1887- tr 1914 Neeltje van Barneveld 1890-
m. Gerrit Ansink 1891- tr 1913 Janna van den Brink 1894-
n. Gijsbert Ansink 1892-
c. Gerritje Ansink 1840-96 tr 1871 Peel Snijders 1845-
a. Maartje Johanna Snijder 1873-1947 tr 1899 Melle Eesges van der Schaaf 1868-1940
b. Hendrik Hermanus Snijder 1875-1928 tr 1902 Mensina Johanna van de Sluis 1877-
</excerpt>

## Search 6 — query: ""Everdina" "de Weert" genealogy"
### Rank 1 of 4 — 0.09 (passed on)
<excerpt title="Everdina De Weert Grandparents">
# Everdina De Weert Grandparents
[[](https://www.instagram.com/kasumikriss) kasumikriss 925K Long awaited parent reveal! 🙈 Did you expected my parents to look this way? #parents #dominican #dutch #mixedgirl #mixedrace #curlyhair #genetics #ancestry #mixedracebabies](https://www.instagram.com/reel/DH4Q59zuUss/?utm_source=popular_topic_grid)

# Everdina De Weert Grandparents
[[](https://www.instagram.com/whitemendatingblackwomenclub) whitemendatin... 817K We’re the Wilders. I’m Jeena and my husband is Drue👸🏾🤴🏼We’re a multicultural family and we don’t match but it does not affect the love we have for each other. ⁣⁣ We have been married for 8 years but we met when we were 17 yrs old. Dude stalked me on Facebook for five years before he ever had the courage to ask me out. ⁣⁣⁣I’m Haitian! ⁣⁣ ⁣⁣We have five beautiful children. ⁣⁣ ⁣⁣We officially adopted our beautiful daughter in Oct of 2019. ⁣⁣ I love nicknames. My children also go by nicknames on social media. Panda, Badger, White Tiger & Cow. If you notice all of these animals are black and white. ⁣⁣ We love to wear matching outfits. I’m pretty my children will end up in therapy wearing mismatch clothes on purpose because of this. ⁣⁣ My older daughters are twins, more specifically #virtualtwins! We’re pretty much the Modern All American Family. @jeenawilder ⁣⁣ .⁣⁣ .⁣⁣ .⁣⁣ .⁣⁣ .⁣⁣ #familygoals #blackqueen #interracialmarriage #interracialfamily #virtualtwins #twinning #matching #whitemendatingblackwomen #matchingoutfits #interracialcouple #multiculturalfamily #relationshipgoals #interracialcouples #family #blackwhitedating #blackwomendatingwhitemen #blendedfamily #adoptionmom #transracialadoption #parenthood #everydaymom #realmotherhood #representationmatters #blackwomenmatter #melanin #familesareforever #lovewins #biracialbabies #adoption ⁣⁣#lovehasnocolor](https://www.instagram.com/reel/CsoJVlQNZ3q/?utm_source=popular_topic_grid)
Get the full experience
Sign up for Instagram
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

# Everdina De Weert Grandparents
Threads
Contact Uploading & Non-Users
Meta Verified
English
© 2026 Instagram from Meta
</excerpt>
### Rank 2 of 4 — 0.03
<excerpt title="Everdina De Weert Grandparents">
# Everdina De Weert Grandparents
[[](https://www.instagram.com/bringing_history_to_life) bringing_hist... 14.1K An unknown father with his two daughters, photographed around 1900, posed closely together in a studio setting. The father sits centered, wearing a dark suit with a neatly trimmed mustache and beard, while his daughters lean in from either side, dressed in light, decorative gowns with lace, gloves, and carefully styled hair. Their relaxed smiles and physical closeness suggest affection and familiarity rather than stiff formality. Family portraits like this were often taken to mark stability, prosperity, or a milestone moment, especially at the turn of the century when photography was becoming more accessible. The daughters’ fashionable dresses point to a comfortable middle-class life, likely in an urban or town environment where studios were common. Though their names are unknown, the image preserves a quiet moment of family connection, capturing how love, pride, and identity were expressed through early photography. #UnknownFamily #VictorianFamily #Circa1900 #VintagePhotography #FamilyHistory #EdwardianEra #OldPhotos #HistoricalPortrait #ThenAndNow #BringingHistoryToLife](https://www.instagram.com/reel/DTaOyvlkWwH/?utm_source=popular_topic_grid)
[[](https://www.instagram.com/arndreaking_official) arndreaking_o... My most important job is to keep Yolanda Renee's grandparents’ memory alive for her and guide her through the many expectations that fall on her shoulders. No matter what else I accomplish in my life, I am fulfilling my purpose and living my legacy for her.](https://www.instagram.com/reel/DKh7eoaIt0x/?utm_source=popular_topic_grid)
[[](https://www.instagram.com/wehrmacht_archive0) wehrmacht_arc... 1,510 Hitler appears with Verena Wagner (later Lafferentz-Wagner), younger daughter of Siegfried Wagner, a granddaughter of Richard Wagner, and a great-granddaughter of Franz Liszt.](https://www.instagram.com/reel/DWthpiFj8kc/?utm_source=popular_topic_grid)

# Everdina De Weert Grandparents
[[](https://www.instagram.com/kasumikriss) kasumikriss 925K Long awaited parent reveal! 🙈 Did you expected my parents to look this way? #parents #dominican #dutch #mixedgirl #mixedrace #curlyhair #genetics #ancestry #mixedracebabies](https://www.instagram.com/reel/DH4Q59zuUss/?utm_source=popular_topic_grid)
</excerpt>
### Rank 3 of 4 — 0.03
<excerpt title="Everdina De Weert Grandparents">
# Everdina De Weert Grandparents
Log In
Sign Up
Watch reels about everdina de weert grandparents from people around the world.
[[](https://www.instagram.com/cinemathenvsnow) cinemathenvsnow 8.9M From red carpets to real-life moments, these legendary parents didn’t just create stars — they raised powerful daughters who are rewriting their own stories ✨ Some inherited the spotlight, some inherited the strength, and some inherited the courage to become something completely different. Behind every confident smile is a parent who guided, protected, and believed long before the world applauded. Fame can open doors, but values, discipline, and love shape who walks through them. These father-daughter and mother-daughter bonds remind us that legacy isn’t just about last names — it’s about lessons, resilience, and unconditional support. Watching these daughters grow from tiny hands holding their parents’ fingers to independent women owning their space in the world is pure magic. Different journeys, same roots — family first, always 🤍 Because no matter how famous you become, being someone’s daughter is the role that stays forever. #CelebrityFamily #FatherDaughterBond #HollywoodLegacy #StarKids #FamilyGoals](https://www.instagram.com/reel/DTIgMDfkt-T/?utm_source=popular_topic_grid)
[[](https://www.instagram.com/famdeweijer) famdeweijer 81K En? vonden jullie van de eerste aflevering? #daargaanzeweer #rtl4 #reality @masiacalmarques](https://www.instagram.com/reel/DF9r5BpN2gk/?utm_source=popular_topic_grid)

# Everdina De Weert Grandparents
[[](https://www.instagram.com/whitemendatingblackwomenclub) whitemendatin... 19.7M We’re the Wilders. I’m Jeena and my husband is Drue! We’re a multicultural family and we don’t match but it does not affect the love we have for each other. ⁣⁣ We have been married for 8 years but we met when we were 17 yrs old. Dude stalked me on Facebook for five years before he ever had the courage to ask me out. ⁣⁣⁣I’m Haitian! ⁣⁣ ⁣⁣We have five beautiful children. ⁣⁣ ⁣⁣We officially adopted our beautiful daughter in Oct of 2019. ⁣⁣ I love nicknames. My children also go by nicknames on social media. Panda, Badger, White Tiger & Cow. If you notice all of these animals are black and white. ⁣⁣ We love to wear matching outfits. I’m pretty my children will end up in therapy wearing mismatch clothes on purpose because of this. ⁣⁣ My older daughters are twins, more specifically #virtualtwins! We’re pretty much the Modern All American Family. @jeenawilder ⁣⁣Happy holidays 🎄🎅Love you guys always 😘🙏🏾❤️🖤🤍💜💙💚💛🤎🧡 . . . .⁣⁣ .⁣⁣ .⁣⁣ .⁣⁣ .⁣ #familygoals #blackqueen #interracialmarriage #interracialfamily #virtualtwins #twinning #matching #whitemendatingblackwomen #matchingoutfits #interracialcouple #multiculturalfamily #relationshipgoals #interracialcouples #family #blackwhitedating #blackwomendatingwhitemen #blendedfamily #adoptionmom #transracialadoption #parenthood #christmas #twins #representationmatters #blackwomenmatter #melanin #familesareforever #lovewins #biracialbabies #adoption ⁣⁣#lovehasnocolor](https://www.instagram.com/reel/C1POVY_uI2U/?utm_source=popular_topic_grid)
</excerpt>
### Rank 4 of 4 — 0.02
<excerpt title="Everdina De Weert Grandparents">
# Everdina De Weert Grandparents
[[](https://www.instagram.com/whitemendatingblackwomenclub) whitemendatin... 19.7M We’re the Wilders. I’m Jeena and my husband is Drue! We’re a multicultural family and we don’t match but it does not affect the love we have for each other. ⁣⁣ We have been married for 8 years but we met when we were 17 yrs old. Dude stalked me on Facebook for five years before he ever had the courage to ask me out. ⁣⁣⁣I’m Haitian! ⁣⁣ ⁣⁣We have five beautiful children. ⁣⁣ ⁣⁣We officially adopted our beautiful daughter in Oct of 2019. ⁣⁣ I love nicknames. My children also go by nicknames on social media. Panda, Badger, White Tiger & Cow. If you notice all of these animals are black and white. ⁣⁣ We love to wear matching outfits. I’m pretty my children will end up in therapy wearing mismatch clothes on purpose because of this. ⁣⁣ My older daughters are twins, more specifically #virtualtwins! We’re pretty much the Modern All American Family. @jeenawilder ⁣⁣Happy holidays 🎄🎅Love you guys always 😘🙏🏾❤️🖤🤍💜💙💚💛🤎🧡 . . . .⁣⁣ .⁣⁣ .⁣⁣ .⁣⁣ .⁣ #familygoals #blackqueen #interracialmarriage #interracialfamily #virtualtwins #twinning #matching #whitemendatingblackwomen #matchingoutfits #interracialcouple #multiculturalfamily #relationshipgoals #interracialcouples #family #blackwhitedating #blackwomendatingwhitemen #blendedfamily #adoptionmom #transracialadoption #parenthood #christmas #twins #representationmatters #blackwomenmatter #melanin #familesareforever #lovewins #biracialbabies #adoption ⁣⁣#lovehasnocolor](https://www.instagram.com/reel/C1POVY_uI2U/?utm_source=popular_topic_grid)

# Everdina De Weert Grandparents
[[](https://www.instagram.com/bringing_history_to_life) bringing_hist... 14.1K An unknown father with his two daughters, photographed around 1900, posed closely together in a studio setting. The father sits centered, wearing a dark suit with a neatly trimmed mustache and beard, while his daughters lean in from either side, dressed in light, decorative gowns with lace, gloves, and carefully styled hair. Their relaxed smiles and physical closeness suggest affection and familiarity rather than stiff formality. Family portraits like this were often taken to mark stability, prosperity, or a milestone moment, especially at the turn of the century when photography was becoming more accessible. The daughters’ fashionable dresses point to a comfortable middle-class life, likely in an urban or town environment where studios were common. Though their names are unknown, the image preserves a quiet moment of family connection, capturing how love, pride, and identity were expressed through early photography. #UnknownFamily #VictorianFamily #Circa1900 #VintagePhotography #FamilyHistory #EdwardianEra #OldPhotos #HistoricalPortrait #ThenAndNow #BringingHistoryToLife](https://www.instagram.com/reel/DTaOyvlkWwH/?utm_source=popular_topic_grid)
[[](https://www.instagram.com/arndreaking_official) arndreaking_o... My most important job is to keep Yolanda Renee's grandparents’ memory alive for her and guide her through the many expectations that fall on her shoulders. No matter what else I accomplish in my life, I am fulfilling my purpose and living my legacy for her.](https://www.instagram.com/reel/DKh7eoaIt0x/?utm_source=popular_topic_grid)
[[](https://www.instagram.com/wehrmacht_archive0) wehrmacht_arc... 1,510 Hitler appears with Verena Wagner (later Lafferentz-Wagner), younger daughter of Siegfried Wagner, a granddaughter of Richard Wagner, and a great-granddaughter of Franz Liszt.](https://www.instagram.com/reel/DWthpiFj8kc/?utm_source=popular_topic_grid)
</excerpt>

## Search 7 — query: ""Everdina de Weert" obituary"
### Rank 1 of 4 — 0.09 (passed on)
<excerpt title="Everdina De Weert Grandparents - Instagram">
# Everdina De Weert Grandparents
[[](https://www.instagram.com/kasumikriss) kasumikriss 925K Long awaited parent reveal! 🙈 Did you expected my parents to look this way? #parents #dominican #dutch #mixedgirl #mixedrace #curlyhair #genetics #ancestry #mixedracebabies](https://www.instagram.com/reel/DH4Q59zuUss/?utm_source=popular_topic_grid)

# Everdina De Weert Grandparents
[[](https://www.instagram.com/whitemendatingblackwomenclub) whitemendatin... 817K We’re the Wilders. I’m Jeena and my husband is Drue👸🏾🤴🏼We’re a multicultural family and we don’t match but it does not affect the love we have for each other. ⁣⁣ We have been married for 8 years but we met when we were 17 yrs old. Dude stalked me on Facebook for five years before he ever had the courage to ask me out. ⁣⁣⁣I’m Haitian! ⁣⁣ ⁣⁣We have five beautiful children. ⁣⁣ ⁣⁣We officially adopted our beautiful daughter in Oct of 2019. ⁣⁣ I love nicknames. My children also go by nicknames on social media. Panda, Badger, White Tiger & Cow. If you notice all of these animals are black and white. ⁣⁣ We love to wear matching outfits. I’m pretty my children will end up in therapy wearing mismatch clothes on purpose because of this. ⁣⁣ My older daughters are twins, more specifically #virtualtwins! We’re pretty much the Modern All American Family. @jeenawilder ⁣⁣ .⁣⁣ .⁣⁣ .⁣⁣ .⁣⁣ .⁣⁣ #familygoals #blackqueen #interracialmarriage #interracialfamily #virtualtwins #twinning #matching #whitemendatingblackwomen #matchingoutfits #interracialcouple #multiculturalfamily #relationshipgoals #interracialcouples #family #blackwhitedating #blackwomendatingwhitemen #blendedfamily #adoptionmom #transracialadoption #parenthood #everydaymom #realmotherhood #representationmatters #blackwomenmatter #melanin #familesareforever #lovewins #biracialbabies #adoption ⁣⁣#lovehasnocolor](https://www.instagram.com/reel/CsoJVlQNZ3q/?utm_source=popular_topic_grid)
Get the full experience
Sign up for Instagram
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

# Everdina De Weert Grandparents
Threads
Contact Uploading & Non-Users
Meta Verified
English
© 2026 Instagram from Meta
</excerpt>
### Rank 2 of 4 — 0.03
<excerpt title="Everdina De Weert Grandparents - Instagram">
# Everdina De Weert Grandparents
Log In
Sign Up
Watch reels about everdina de weert grandparents from people around the world.
[[](https://www.instagram.com/cinemathenvsnow) cinemathenvsnow 8.9M From red carpets to real-life moments, these legendary parents didn’t just create stars — they raised powerful daughters who are rewriting their own stories ✨ Some inherited the spotlight, some inherited the strength, and some inherited the courage to become something completely different. Behind every confident smile is a parent who guided, protected, and believed long before the world applauded. Fame can open doors, but values, discipline, and love shape who walks through them. These father-daughter and mother-daughter bonds remind us that legacy isn’t just about last names — it’s about lessons, resilience, and unconditional support. Watching these daughters grow from tiny hands holding their parents’ fingers to independent women owning their space in the world is pure magic. Different journeys, same roots — family first, always 🤍 Because no matter how famous you become, being someone’s daughter is the role that stays forever. #CelebrityFamily #FatherDaughterBond #HollywoodLegacy #StarKids #FamilyGoals](https://www.instagram.com/reel/DTIgMDfkt-T/?utm_source=popular_topic_grid)
[[](https://www.instagram.com/famdeweijer) famdeweijer 81K En? vonden jullie van de eerste aflevering? #daargaanzeweer #rtl4 #reality @masiacalmarques](https://www.instagram.com/reel/DF9r5BpN2gk/?utm_source=popular_topic_grid)

# Everdina De Weert Grandparents
[[](https://www.instagram.com/whitemendatingblackwomenclub) whitemendatin... 19.7M We’re the Wilders. I’m Jeena and my husband is Drue! We’re a multicultural family and we don’t match but it does not affect the love we have for each other. ⁣⁣ We have been married for 8 years but we met when we were 17 yrs old. Dude stalked me on Facebook for five years before he ever had the courage to ask me out. ⁣⁣⁣I’m Haitian! ⁣⁣ ⁣⁣We have five beautiful children. ⁣⁣ ⁣⁣We officially adopted our beautiful daughter in Oct of 2019. ⁣⁣ I love nicknames. My children also go by nicknames on social media. Panda, Badger, White Tiger & Cow. If you notice all of these animals are black and white. ⁣⁣ We love to wear matching outfits. I’m pretty my children will end up in therapy wearing mismatch clothes on purpose because of this. ⁣⁣ My older daughters are twins, more specifically #virtualtwins! We’re pretty much the Modern All American Family. @jeenawilder ⁣⁣Happy holidays 🎄🎅Love you guys always 😘🙏🏾❤️🖤🤍💜💙💚💛🤎🧡 . . . .⁣⁣ .⁣⁣ .⁣⁣ .⁣⁣ .⁣ #familygoals #blackqueen #interracialmarriage #interracialfamily #virtualtwins #twinning #matching #whitemendatingblackwomen #matchingoutfits #interracialcouple #multiculturalfamily #relationshipgoals #interracialcouples #family #blackwhitedating #blackwomendatingwhitemen #blendedfamily #adoptionmom #transracialadoption #parenthood #christmas #twins #representationmatters #blackwomenmatter #melanin #familesareforever #lovewins #biracialbabies #adoption ⁣⁣#lovehasnocolor](https://www.instagram.com/reel/C1POVY_uI2U/?utm_source=popular_topic_grid)
</excerpt>
### Rank 3 of 4 — 0.02
<excerpt title="Everdina De Weert Grandparents - Instagram">
# Everdina De Weert Grandparents
[[](https://www.instagram.com/bringing_history_to_life) bringing_hist... 14.1K An unknown father with his two daughters, photographed around 1900, posed closely together in a studio setting. The father sits centered, wearing a dark suit with a neatly trimmed mustache and beard, while his daughters lean in from either side, dressed in light, decorative gowns with lace, gloves, and carefully styled hair. Their relaxed smiles and physical closeness suggest affection and familiarity rather than stiff formality. Family portraits like this were often taken to mark stability, prosperity, or a milestone moment, especially at the turn of the century when photography was becoming more accessible. The daughters’ fashionable dresses point to a comfortable middle-class life, likely in an urban or town environment where studios were common. Though their names are unknown, the image preserves a quiet moment of family connection, capturing how love, pride, and identity were expressed through early photography. #UnknownFamily #VictorianFamily #Circa1900 #VintagePhotography #FamilyHistory #EdwardianEra #OldPhotos #HistoricalPortrait #ThenAndNow #BringingHistoryToLife](https://www.instagram.com/reel/DTaOyvlkWwH/?utm_source=popular_topic_grid)
[[](https://www.instagram.com/arndreaking_official) arndreaking_o... My most important job is to keep Yolanda Renee's grandparents’ memory alive for her and guide her through the many expectations that fall on her shoulders. No matter what else I accomplish in my life, I am fulfilling my purpose and living my legacy for her.](https://www.instagram.com/reel/DKh7eoaIt0x/?utm_source=popular_topic_grid)
[[](https://www.instagram.com/wehrmacht_archive0) wehrmacht_arc... 1,510 Hitler appears with Verena Wagner (later Lafferentz-Wagner), younger daughter of Siegfried Wagner, a granddaughter of Richard Wagner, and a great-granddaughter of Franz Liszt.](https://www.instagram.com/reel/DWthpiFj8kc/?utm_source=popular_topic_grid)

# Everdina De Weert Grandparents
[[](https://www.instagram.com/kasumikriss) kasumikriss 925K Long awaited parent reveal! 🙈 Did you expected my parents to look this way? #parents #dominican #dutch #mixedgirl #mixedrace #curlyhair #genetics #ancestry #mixedracebabies](https://www.instagram.com/reel/DH4Q59zuUss/?utm_source=popular_topic_grid)
</excerpt>
### Rank 4 of 4 — 0.02
<excerpt title="Everdina De Weert Grandparents - Instagram">
# Everdina De Weert Grandparents
[[](https://www.instagram.com/whitemendatingblackwomenclub) whitemendatin... 19.7M We’re the Wilders. I’m Jeena and my husband is Drue! We’re a multicultural family and we don’t match but it does not affect the love we have for each other. ⁣⁣ We have been married for 8 years but we met when we were 17 yrs old. Dude stalked me on Facebook for five years before he ever had the courage to ask me out. ⁣⁣⁣I’m Haitian! ⁣⁣ ⁣⁣We have five beautiful children. ⁣⁣ ⁣⁣We officially adopted our beautiful daughter in Oct of 2019. ⁣⁣ I love nicknames. My children also go by nicknames on social media. Panda, Badger, White Tiger & Cow. If you notice all of these animals are black and white. ⁣⁣ We love to wear matching outfits. I’m pretty my children will end up in therapy wearing mismatch clothes on purpose because of this. ⁣⁣ My older daughters are twins, more specifically #virtualtwins! We’re pretty much the Modern All American Family. @jeenawilder ⁣⁣Happy holidays 🎄🎅Love you guys always 😘🙏🏾❤️🖤🤍💜💙💚💛🤎🧡 . . . .⁣⁣ .⁣⁣ .⁣⁣ .⁣⁣ .⁣ #familygoals #blackqueen #interracialmarriage #interracialfamily #virtualtwins #twinning #matching #whitemendatingblackwomen #matchingoutfits #interracialcouple #multiculturalfamily #relationshipgoals #interracialcouples #family #blackwhitedating #blackwomendatingwhitemen #blendedfamily #adoptionmom #transracialadoption #parenthood #christmas #twins #representationmatters #blackwomenmatter #melanin #familesareforever #lovewins #biracialbabies #adoption ⁣⁣#lovehasnocolor](https://www.instagram.com/reel/C1POVY_uI2U/?utm_source=popular_topic_grid)

# Everdina De Weert Grandparents
[[](https://www.instagram.com/bringing_history_to_life) bringing_hist... 14.1K An unknown father with his two daughters, photographed around 1900, posed closely together in a studio setting. The father sits centered, wearing a dark suit with a neatly trimmed mustache and beard, while his daughters lean in from either side, dressed in light, decorative gowns with lace, gloves, and carefully styled hair. Their relaxed smiles and physical closeness suggest affection and familiarity rather than stiff formality. Family portraits like this were often taken to mark stability, prosperity, or a milestone moment, especially at the turn of the century when photography was becoming more accessible. The daughters’ fashionable dresses point to a comfortable middle-class life, likely in an urban or town environment where studios were common. Though their names are unknown, the image preserves a quiet moment of family connection, capturing how love, pride, and identity were expressed through early photography. #UnknownFamily #VictorianFamily #Circa1900 #VintagePhotography #FamilyHistory #EdwardianEra #OldPhotos #HistoricalPortrait #ThenAndNow #BringingHistoryToLife](https://www.instagram.com/reel/DTaOyvlkWwH/?utm_source=popular_topic_grid)
[[](https://www.instagram.com/arndreaking_official) arndreaking_o... My most important job is to keep Yolanda Renee's grandparents’ memory alive for her and guide her through the many expectations that fall on her shoulders. No matter what else I accomplish in my life, I am fulfilling my purpose and living my legacy for her.](https://www.instagram.com/reel/DKh7eoaIt0x/?utm_source=popular_topic_grid)
[[](https://www.instagram.com/wehrmacht_archive0) wehrmacht_arc... 1,510 Hitler appears with Verena Wagner (later Lafferentz-Wagner), younger daughter of Siegfried Wagner, a granddaughter of Richard Wagner, and a great-granddaughter of Franz Liszt.](https://www.instagram.com/reel/DWthpiFj8kc/?utm_source=popular_topic_grid)
</excerpt>

## Search 8 — query: "Everdina de Weert 1918" genealogie""
### Rank 1 of 82 — 0.34 (passed on)
<excerpt title="Everdina van de WEERTHOF (1892–1978) • FamilySearch">
## Everdina van de WEERTHOF
Female
30 April 1892–30 December 1978
•
When Everdina van de WEERTHOF was born on 30 April 1892, in Ede, Gelderland, Netherlands, her father, Willem van de WEERTHOF, was 27 and her mother, Marretje Jansen, was 24. She married Marinus Slagmolen on 26 February 1916, in Ede, Gelderland, Netherlands. They were the parents of at least 1 son and 3 daughters. She died on 30 December 1978, at the age of 86.
Marriage
26 February 1916 Ede, Gelderland, Netherlands

## Everdina van de WEERTHOF
### Children (4)
As a nonprofit, we offer free help to those looking to learn the details of their family story.
Create a FREE Account
There are no historical documents attached to Everdina.

## Everdina van de WEERTHOF
### 1899 · Hague Peace Convention
Age 7
The Hague Peace Convention was a series conferences that produced treaties and declarations. The convention took place in Hague, Netherlands. The conferences were among the first formal statements of the laws of war and war crimes in secular international law.

## Everdina van de WEERTHOF
### 1904 · Weerdinge Couple Found in Bog
Age 12
Two skeletons were found next to each other in Drenthe, Netherlands. The skeletons were dated back to between 160 BC and 220 AD. One of the skeletons was thought to be a female and the other a male so scientists called them the Weerdinge couple or Mr. and Mrs. Veenstra. It was determined that both skeletons were men and the name was changed to Weerdinge Men.

## Everdina van de WEERTHOF
### 1917
Age 25
WWI. Despite Dutch neutrality in World War I (1914-18), the Netherlands suffers from severe food shortages, triggering street riots.
1860
1880
1900
1920
1940
1960
1980
2000
2020
Marinus Slagmolen
1886–1953
Everdina van de WEERTHOF
1892–1978
Marriage: 26 February 1916
Cornelia Maria Slagmolen
1916–Deceased
Marretje Slagmolen
1917–2019
Dirkje Johanna Gijsberta Slagmolen
1918–Deceased
Gijsbertus Slagmolen
1921–1989

## Everdina van de WEERTHOF
### Siblings (2)
Some characteristic forenames: Vietnamese Anh, Thanh, Hung, Minh, Vinh, Dung, Hue, Huong, Lan, Quang, Tan, Thuy, Hong, Chi, Hang, Ho, Pok, Sang, Bai, Chin, Ching, Chu, Chuan, Dong.
Vietnamese (**Vạn**): from the Chinese surname 萬, see Wan 1.
Vietnamese (**Văn**): from the Chinese surnames 文 or 聞, see Wen 2 and 3, and also 5 below.
Dictionary of American Family Names © Patrick Hanks 2003, 2006.
**Possible Related Names**
</excerpt>
### Rank 2 of 82 — 0.24
<excerpt title="Genealogie Familie van Roekel - Naamlijst W">
**Wilde:** Aalbert 1922, Adriana 1925, Ahasserus 1913, Claas 1623, Dirk 1915, Elizabeth 1931, Engbert 1892, Evert 18901917, Gerrit 1930, Gijsbertus 1893, Johannes 1835, Wabbo 1908;
**Wildeboer:** Aaltje 1907, Fijchien 1830;
**Wildekamp:**

Aertien 1688, Annetta 1878 Arnolda 1866, Bartje 1833, Berendina Everdina 1911, Betje 18771886, Dirk 1921, Elisabeth 1887, Everdina 190419201927, Evert 1841186519001918, Evertje 1851, Geertjen X, Geesje 1816, Gerrit 169817341770179818221886189819131948X, Gerritje 18491926, Gijsbert 17301732, Gijsbertus 1914, Gijsje 1884, Hendrik 18331921, Hendrika 1874, Hendrikus 18911925, Huibert 1735, Jan 1835184318451860XXX, Janna 1775, Jantjen 1772, Jenneke 17961811, Jochem 185718961910, Johan 1919, Johanna 18671874, Joost 1782, Lambarta 1893, Lambertus 1898, Luitje 1782, Lijsbeth 1769, Maria 1783179518781884, Marina 1879, Metje 18291852, Neeltje 17941819, Nolda 1855, Peter 1778184718891919, Steven 18131880, Trijntje X, Wilhelmina 1938, Willem 182418551863,
</excerpt>
### Rank 3 of 82 — 0.20
<excerpt title="Genealogie Familie van Roekel - Naamlijst W">
**Weening:** Berendina Fredrika1885, Everdina 1879, Johanna 1871;
**Weenink:** zie Weening;
**Weerd(t):**

Aaldert Johan 1910, Aaltje 18191902, Aantje 1877, Aart 18781908, Aartje 18731927, Albertha 1904, Aldert Carl 1916, Alice 19021920X, Anna X, Anneke 1913, Annetta 1926, Annette Marie 1918, Anthonie 1909, Antonia 1902, Antonie 18941898, Arend 1859, Arend Jan 1919, Arie 1891, Arien 1907, Aris 1915, Arisje 18521856, Arthur C 1904, Bartha 1861, Belia 1881, Bert 18911916, Bertha 18991901, Bertus 1928, Betje 1903, Betsy X, Bonnie Jo 1952, Breunis 1889, Catharina 1906, Charles 1922, Chester Loyd 1928, Christiaan 1892190019101911, Cientje 1888, Clarence H 1921, Clifford Herman 1916, Cornelia 18791886191619351939, Cornelis 1877188518991919, Delia 1916, Dena 1903, Derk 18931897, Derkje 18901929, Dick 1920, Dilia 19171942, Dirk 1902, Edward 1903, Elisabeth 1923, Elizabeth 1836, Esther 1921, Esther Martena 1936, Eugene Quinly 1926,
</excerpt>
### Rank 4 of 82 — 0.19
<excerpt title="Genealogie Familie van Roekel - Naamlijst W">
**Wassink:** Albertus 1923, Arend 1908, Arned C 1925, Cornelis 18811909, Cornelius 1928, Dorus 18751912, Elsje 1888, Geesje Frederika 1916, Gerrit Jan 1907, Gerritje Antje 1922, Gerritje Johanna 1901, Gesina Berendina 1905, Geurt 1901, Helena 1912, Helmig Jan 1900, Hendrika Theodora 1907, Jan 1898186019161918, Jan Willem 1920, Klazina Alberta 1903, Maria 1921, Mina 1912, Wilhelmina Gijsberta 1910, Willem 1892;
**Wassinkmaat:** Aaltje 1892, Berendina 18881894, Gerrit 1889, Gerritje 1927, Gijsbert 18651932, Jan 1899, Jannetje 1918, Jantje 1903, Maartje 1896, Mientje 1897, Reiniera 1916;
**Waswick:** Archie 1907;
**Waterboer:** Aart X;
**Wateringen:** Maartje 1635;
**Waternaast:** Neeltje 1685;
**Watrin:** Justina 1899;
**Watson:** Lucia 1909;
**Wattez:** Grietje 1903;
**Wavere:** zie zie Wavrin;

**Wavrin:** Ancillia 1128, Goswin 1143, Hellin I 1130, Hellin II 1195, Hildiarde 1153, Marie 12751272, Robert I 11601245, Robert II 1215, Robert III 1251, Roger I 1040, Roger II 1063, Roger III 1090;
**Waijboer:** Antje 1839;
**Waijer:** Geertruijd 1660;
**Webb:** Henry 1917;
**Webber:** Martha 1899;
**Weber:** Christina 1860, Frederike 1884, Jan Cornelis 1919, Johannes 1839, Lodewijk Albertus 1906, Paul 1903, Simon 1884;
**Wechel:** Clarence 1907;
**Wechgelaer:** Josinus Albertus 1892,
**Wedema:** Christina X;
**Wedemeijer:** Maarten 1899;
**Weduwen:** Ellen Marie 1908;
**Weegenaar:** Aaltje 1735;
**Weeda:** Cornelis 1610, Jan X;
**Weede:** Jan Willem 1916, Johanna Maria 1805, Willem 12801310;
**Weekhout:** Sophia 1906;
**Weelde:**Weelden;
**Weelden:** Anna Elizabeth 1929, Anneke 1913, Antonia 1915, Arnolda 1892, Johanna X, Peter Alvin 1927, Ray 1925, Richard William 1924, Sylvia 1916;
**Weel:** Anna Stoffelina Elisabeth 1904;
**Weele:** Herman 1896, Jacobus Jacob 1904;

**Weening:** Berendina Fredrika1885, Everdina 1879, Johanna 1871;
**Weenink:** zie Weening;
**Weerd(t):**
</excerpt>
### Rank 5 of 82 — 0.13
<excerpt title="Genealogie Familie van Roekel - Naamlijst W">
Eva 1905, Everdina 1914, Evert 18161898, Evertje Anthonia 1921, Fanny Sandrene 1907, Fokko Nicolaus Bernardus 1893, Fred 1924, Fijtje 1839, Garlene Frances 1928, Garrit X, Geertje 18951907, Geertruida 18581884, Gerald 1927, Gerard 1939, Gerret 1803, Gerrie 1930, Gerrigje 19111917, Gerrit 18031876187918881910191719171920X, Gerrit Jan 190119181930, Gerritje 1824185318661877188618901893191419211932, Gertrude J 1921, Gertrude Hazel 1918, Geurt 1904, Geusje 1830, Gordon 1937, Goudje 1908, Grietje 18821906, Guus XX, Gijsbert 18551883188719011917, Gijsbertje 189819171925, Harm 1905, Harmen 181518751891, Harold 1930, Harriet Alice 1892, Harriet Ruth 1933, Harry G 1900, Hattie 1889, Helen Ethel 1921, Hendrik 18651869187418811904191919201929, Hendrik Gerrit 1900, Hendrik Jan 1888, Hendrika 1912,
</excerpt>

## Search 9 — query: ""de Weert" "born" 1918 "Everdina""
(no page could be scored)

## Search 10 — query: ""Everdina de Weert" 1918 "June""
(no page could be scored)

# Example 4
## Question
In The Muppet Movie, which actor who cameoed in the county fair scene has at least one star on the Walk of Fame, an Emmy, and a Golden Globe?

## Expected answer
Bob Hope

## Grade 0.00

## Search 1 — query: ""The Muppet Movie" county fair scene cameo"
### Rank 1 of 46 — 0.77 (passed on)
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
### Rank 2 of 46 — 0.73
<excerpt title="The Muppet Movie - Warren Watched A Movie">
There are more catchy songs in this movie than you would find in just about any Disney film. While “_Rainbow Connection_” is the best, there are plenty that you will find yourself humming or tapping your feet along with. Paul Williams and Kenneth Asher crafted a grossly underrated soundtrack. Have you ever heard “_Movin’ Right Along_”? Try _NOT_ to sing along with that when it comes on!
Video 8
One of the big draws in my opinion are the numerous celebrity cameos present in this film. Dom DeLuise plays the Hollywood agent who inspires Kermit to go to Hollywood. James Coburn as the owner of the El Sleezo Café. Madeline Kahn is all but Lili von Shtupp from **Blazing Saddles**. Telly Savalas is a tough at the El Sleezo. Carol Kane shows up when summoned by her character’s name of “Myth.” Paul Williams is a pianist in the El Sleezo. Milton Berle is used car salesman Mad Man Mooney. Elliott Gould is the announcer at the Bogen County Beauty Pageant. Edgar Bergen and Charlie McCarthy play judges at the Bogen County Beauty Pageant. Bob Hope is an ice cream vendor at the Bogen County Fair. Richard Pryor is a balloon vendor at the Bogen County Fair. Steve Martin is a jerky waiter working at a restaurant. Mel Brooks is mad scientist Professor Max Krassman who is hired by the story’s villain. Cloris Leachman is studio secretary Miss Tracy. And the great Orson Welles is Hollywood producer and studio executive Lew Lord.
They may not all be known to the general audience today, but this was some great talent of the era showing up for a brief joke. I admit when I first saw this I didn’t know who all of them were as I was either too young or just not aware of their work. James Coburn was probably the biggest surprise to me as an adult. I remember the scene he shows up in very well but until I watched it again having been exposed to some of his work, I did not know who he was. He executes his moment perhaps as good as any of the professional comedians.

But we’re not limited to human celebrities showing up here. Oh no! I do believe just about every member of the cast of **_The Muppet Show_** makes an appearance-small or large. While the narrative does focus on the core members of the cast it gives a little bit of a shout out to everyone they can easily fit in without making the appearance feel forced. They even manage a cameo by Big Bird who in a bit of a metajoke is on his way to break into public television.
The genius of this film is that it’s not only great comedy for adults but great comedy for kids as well. It’s something you can watch and enjoy as a group or by yourself. There’s nothing horribly inappropriate or generally offensive. It’s safe comedy that’s actually funny. And it is family friendly stuff that doesn’t treat any potential viewers as emotionally fragile or stupid.
**The Muppet Movie** is alternately moving and silly fun filled with humor that you might feel a little guilty laughing over. Entertainment was clearly the goal as everyone was just have fun up on screen. That joy translates to the audience. And mixed in with all that is a message of friendship, following your dreams, and the responsibility that comes from others believing in you.
The villain of this all is businessman, entrepreneur, and fried frog leg restaurateur Doc Hopper (Charles Durning) who is a genuine threat to Kermit the Frog. Doc Hopper runs a chain of fried frog leg restaurants and wants to use Kermit as a singing and dancing spokesman. As a kid you will think this was just mean. As an adult you realize just how messed up that is.
And as I said this movie packs some real filling in the whole film. There is an important scene in the desert where the group’s car has broken down and it looks like they will not make it to the auditions to get the standard rich and famous contract. Kermit is feeling the weight of the responsibilities he has inadvertently taken on to not only himself, but others and he has an internal dialogue that’s not only moving but offers a great moral lesson. All this in a movie with fuzzy puppets.
</excerpt>
### Rank 3 of 46 — 0.71
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
### Rank 4 of 46 — 0.55
<excerpt title="Celebrate 40 Years of The Muppet Movie with These “ ...">
**Speaking of James Frawley…**The director of _The Muppet Movie_ is himself suitably colorful—perfect for wrangling a host of hilarious, human-esque characters! Frawley got his start on stage in the acclaimed 1960s off-Broadway improvisational troupe The Premise, later appearing on TV’s _Gunsmoke_, _Outer Limits_, and _The Danny Kaye Show_. In the meantime, Frawley was cultivating his skills as a photographer; helming an acclaimed short film called _J-24_ led Frawley to directing, and he eventually won an Emmy Award as director on the fan-favorite ‘60s sitcom _The Monkees_.
**Just a Frog and His Banjo…**_The Muppet Movie_ memorably opens with Kermit the Frog, perched on a log in the lush green swamp he calls “home,” playing his banjo and singing one of his now signature tunes: “Rainbow Connection.” Ever wonder how they managed to film that scene? The man behind the frog, Jim Henson, spent three full days under water inside a specially constructed “bathysphere,” operating Kermit through rubber-sleeved arms! According to the film’s press notes, the submersible was made from two aluminum jet-engine containers and was wired for both sight (a video monitor which enabled Henson to see Kermit’s performance) and sound (Henson’s microphone hookup).
**Even Muppets Need Transportation…**Did you know that Fozzie Bear drives two different cars in _The Muppet Movie_? One is a 1947 Ford “Woody” station wagon, and the other is a 1951 Studebaker Champion. Meanwhile, Gonzo and his chicken companion Camilla drive a 1969 Citreon plumbing repair truck, while later in the film, Dr. Teeth and the Electric Mayhem are seen tooling around in a brightly painted 1961 International school bus.

**Special Guest Cameos A-Plenty…**Most Muppet fans are familiar with _The Muppet Movie_’s cavalcade of guest appearances—from radio/ventriloquist legend Edgar Bergen (in his final film appearance) and Madeline Kahn to Steve Martin, Richard Pryor, and Mel Brooks, the film boasts a veritable “who’s who” of comedy talent. One such cameo is Oscar nominee Elliott Gould; according to the film’s press material, Gould was once asked to emcee the Miss Universe Pageant, which he declined due to a busy filming schedule. But the pageant world came ‘round again—albeit fictitiously—when Gould was asked to appear in _The Muppet Movie_ as the host of the quaint Bogen County Fair’s beauty contest… won by Miss Piggy, of course!
**Some Hollywood History…**The film follows the Muppets on their journey to Hollywood, as they dream of big-screen stardom—all the while pursued by the flamboyantly evil Doc Hopper (Charles Durning), a fast-food tycoon who wants Kermit to star in his commercials. The climactic scene where Kermit and friends finally face off against Doc and his henchmen is portrayed in classic western-film style… and was even shot at the very same location as the showdown in Gary Cooper’s iconic 1952 western _High Noon_.
**A Truly Lasting Legacy…**In 2009, _The Muppet Movie_ was named to the prestigious National Film Registry by the Library of Congress. So what exactly does that mean? Every year since 1988, the registry’s Preservation Board selects 25 films—deemed “culturally, historically, or aesthetically significant”—that showcase the enduring range and diversity of American film heritage, all in an effort to increase awareness for its preservation. We’re sure any Muppet fan would agree: Preserving _The Muppet Movie_ for future generations is a _fantastic_ idea!
Want to keep celebrating this Muppetational milestone? Check out our 10 Fan-tastic Milestones Pin Set, which features an exclusive pin celebrating 40 years of _The Muppet Movie._
</excerpt>
### Rank 5 of 46 — 0.45
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

## Search 2 — query: "Mel Brooks walk of fame"
### Rank 1 of 75 — 0.62 (passed on)
<excerpt title="Mel Brooks">
Mel Brooks (born Melvin James Kaminsky; June 28, 1926) is an American actor, comedian, filmmaker, songwriter and playwright. With a career spanning nine decades, he is known for a variety of successful farces and parodies.[1] A recipient of numerous accolades, he is one of the few people to win the EGOT (Emmy, Grammy, Oscar and Tony) awards. He received a Kennedy Center Honor in 2009, a Hollywood Walk of Fame star in 2010, the AFI Life Achievement Award in 2013, a British Film Institute Fellowship in 2015, a National Medal of Arts in 2016 and a BAFTA Fellowship in 2017.
Brooks began his career as a writer for Sid Caesar's Your Show of Shows, where he worked with Mel Tolkin, Neil Simon and Carl Reiner. Reiner and Brooks co-created the comedy sketch The 2000 Year Old Man and shared the Grammy Award for Best Comedy Album for The 2000 Year Old Man in the Year 2000. With Buck Henry, he created the spy spoof Get Smart.
Brooks won the Academy Award for Best Original Screenplay for The Producers (1967). After The Twelve Chairs (1970), he made a string of successful comedies: Blazing Saddles and Young Frankenstein (both 1974), Silent Movie (1976), High Anxiety (1977), History of the World, Part I (1981) and Spaceballs (1987).[2] His musical adaptation of The Producers ran on Broadway from 2001 to 2007 and won 12 Tony Awards. It was adapted as a film in 2005. Through his company, Brooksfilms, he produced David Lynch's The Elephant Man (1980), David Cronenberg's The Fly (1986) and David Jones's 84 Charing Cross Road (1987). With Anne Bancroft, he starred in To Be or Not To Be (1983), a remake of Ernst Lubitsch's 1942 film.
</excerpt>
### Rank 2 of 75 — 0.61
<excerpt title="Mel Brooks">
Brooks is one of the few people to have received an Emmy, Grammy, Oscar and Tony (EGOT).[124] He received Emmys in 1997, 1998 and 1999 for Outstanding Guest Actor in a Comedy Series for his role of Uncle Phil on Mad About You.[60] He and Carl Reiner won a Grammy for Best Spoken Comedy Album for The 2000 Year Old Man in the Year 2000 . He won another in 2002 for Best Musical Show Album for the cast album of The Producers and for Best Long Form Music Video for the DVD Recording the Producers: A Musical Romp with Mel Brooks. He won his Oscar, for Best Original Screenplay in 1968, for The Producers.[125] He won three Tonys, for Best Original Score, Best Book of a Musical and Best Musical for the stage adaptation of The Producers.
Brooks won Hugo and Nebula awards for Young Frankenstein.[126] In a 2005 Channel 4 poll to find The Comedian's Comedian, he was voted No. 50 of the top 50 comedy acts ever by fellow comedians and comedy insiders.[127]
In December 2009, Brooks was feted at the Kennedy Center Honors at the John F. Kennedy Center for the Performing Arts in Washington, DC.[128] He was inducted into the Hollywood Walk of Fame in April 2010, with a motion pictures star located at 6712 Hollywood Boulevard.[129][130] In 2018, Brooks received the Polish Gold Gloria Artis Medal for Merit to Culture.[131]

The American Film Institute presented Brooks with the AFI Life Achievement Award in June 2013.[132][133] In 2014 Brooks was honored in a handprint and footprint ceremony at TCL Chinese Theatre. His handprints include a six-fingered left hand as he wore a prosthetic finger when making his prints.[134] In March 2015 he received a British Film Institute Fellowship from the British Film Institute.[135] In 2024, Nathan Lane and Matthew Broderick presented Brooks with an Honorary Oscar.[136] The AFI lists three of Brooks's films on its AFI's 100 Years...100 Laughs list: Blazing Saddles (number 6), The Producers (number 11) and Young Frankenstein (number 13).[137] In 2026, to celebrate Brooks's centenary, it moved Blazing Saddles to first place, displacing Billy Wilder's Some Like It Hot (1959).[138]
</excerpt>
### Rank 3 of 75 — 0.55
<excerpt title="Mel Brooks">
Brooks has often expressed pride in being Jewish. In 2021, Brooks told NPR's Terry Gross: "I love being a Jew, I love Jewish humor..."[93]
Regarding religion, Brooks stated, "I'm rather secular. I'm basically Jewish. But I think I'm Jewish not because of the Jewish religion at all. I think it's the relationship with the people and the pride I have. The tribe surviving so many misfortunes, and being so brave and contributing so much knowledge to the world and showing courage".[118] He says "Look at Jewish history: Unrelieved lamenting would be intolerable. So, for every ten Jews beating their breast, God designated one to be crazy and amuse the breast-beaters. By the time I was five I knew I was that one."[119]
On Jewish films, Brooks said, "They can be anything and anywhere ... if there's a tribal thing, like, the 'please God, protect us' feeling ... we don't know where and how it's gonna come out. Avatar was a Jewish movie ... these people on the run, chasing—and being pursued".[120]
Political viewsedit
Brooks endorsed Joe Biden in the 2020 presidential election in his first-ever public endorsement of a political candidate.[121][122] He endorsed Kamala Harris in the 2024 presidential election.[123]
Accoladesedit  
Main articles: Mel Brooks on screen and stage and List of awards and nominations received by Mel Brooks  
Brooks at his Hollywood Walk of Fame ceremony in 2010
Blazing Saddles, Young Frankenstein and The Producers were selected for preservation in the National Film Registry. He received the Screen Laurel from the Writers Guild of America in 2003.[50]

Brooks is one of the few people to have received an Emmy, Grammy, Oscar and Tony (EGOT).[124] He received Emmys in 1997, 1998 and 1999 for Outstanding Guest Actor in a Comedy Series for his role of Uncle Phil on Mad About You.[60] He and Carl Reiner won a Grammy for Best Spoken Comedy Album for The 2000 Year Old Man in the Year 2000 . He won another in 2002 for Best Musical Show Album for the cast album of The Producers and for Best Long Form Music Video for the DVD Recording the Producers: A Musical Romp with Mel Brooks. He won his Oscar, for Best Original Screenplay in 1968, for The Producers.[125] He won three Tonys, for Best Original Score, Best Book of a Musical and Best Musical for the stage adaptation of The Producers.
Brooks won Hugo and Nebula awards for Young Frankenstein.[126] In a 2005 Channel 4 poll to find The Comedian's Comedian, he was voted No. 50 of the top 50 comedy acts ever by fellow comedians and comedy insiders.[127]
In December 2009, Brooks was feted at the Kennedy Center Honors at the John F. Kennedy Center for the Performing Arts in Washington, DC.[128] He was inducted into the Hollywood Walk of Fame in April 2010, with a motion pictures star located at 6712 Hollywood Boulevard.[129][130] In 2018, Brooks received the Polish Gold Gloria Artis Medal for Merit to Culture.[131]
</excerpt>
### Rank 4 of 75 — 0.51
<excerpt title="Mel Brooks">
Max Brooks [@maxbrooksauthor] (October 21, 2020). "My father, @MelBrooks, is 94. He has never made a political video. Until now. / #MelBrooks4JoeBiden / #BidenHarris / #GrassrootsDemHQ" (Tweet) – via Twitter.  
 @MelBrooks (September 12, 2024). "I don't have a cat, so a dog will have to do! But like Taylor Swift I'm all in for @KamalaHarris & @Tim_Walz! #VoteBlue" (Tweet). Retrieved October 27, 2024 – via X (formerly Twitter).  
 Simonson, Robert (June 4, 2001). "With Producers, Mel Brooks Has Won Tony, Oscar, Grammy and Emmy". Playbill. Archived from the original on February 19, 2017. Retrieved January 1, 2010.  
 "The 41st Academy Awards (1969) Nominees and Winners". Academy of Motion Picture Arts and Sciences. December 21, 2014. Archived from the original on March 21, 2016. Retrieved November 4, 2024.  
 Reginald, Robert (1981). Science Fiction & Fantasy Awards. Borgo Press. p. 46. ISBN 978-0893709068. Retrieved August 13, 2018 – via Google Books.  
 "Cook is voted comedians' comedian". Evening Standard. January 4, 2005. Archived from the original on January 3, 2019. Retrieved October 4, 2019.  
 "Mel Brooks laughs his way to Kennedy Center honor". The Washington Post. December 6, 2009. Archived from the original on November 9, 2012. Retrieved November 1, 2012.  
 "Hollywood Walk of Fame – Mel Brooks". Hollywood Walk of Fame. Hollywood Chamber of Commerce. Archived from the original on September 1, 2017. Retrieved November 30, 2017.
</excerpt>
### Rank 5 of 75 — 0.47
<excerpt title="Mel Brooks Gets Star on Hollywood Walk of Fame">
# Mel Brooks Gets Star on Hollywood Walk of Fame
Customers
[![Image 3: logo](blob:http://localhost/ca36a5413022ff6a0101cbd4c0c92e06)](https://www.backstage.com/)
*   Find Jobs  
*   Find Talent  
*   Resources     
*   Agents  
*   [![Image 4: Backstage icon](blob:http://localhost/3640b78be138c80a8725e9848a41c0c0)Community NEW](https://www.backstage.com/community/)

*   New Grow with UGC     
*   Join     
*   Post a Job  
*   Sign in  
*
Content For:Actors + PerformersBrands + CreativesCastingCreatorsCrewVoiceover
Categories:
*   Advice  
*   Awards  
*   Casting News  
*   Features  
*   Getting Started  
*   Industry  
*   More...
Topics:
*   Agent Resources + Advice  
*   Audition Advice  
*   Casting  
*   Crew 101  
*   Education  
*   Money  
*   More...
Specialties:
*   Acting  
*   Background + Extras  
*   Influencer  
*   Modeling  
*   Agency  
*   Agent  
*   More...
Mediums:
*   Commercials  
*   Digital Media  
*   Film  
*   Television  
*   Theater  
*   Brand Sites  
*   More...
Series:
*   Backstage Experts  
*   Backstage Guides  
*   How to Get Cast On  
*   Now Casting  
*   #ICastIt  
*   #IGotCast  
*   More...

*   Actors + Performers
By Backstage Staff | Last Updated: November 5, 2019

# Mel Brooks Gets Star on Hollywood Walk of Fame
[](mailto:?subject=Mel%20Brooks%20Gets%20Star%20on%20Hollywood%20Walk%20of%20Fame&body=TITLE%3A%20'Mel%20Brooks%20Gets%20Star%20on%20Hollywood%20Walk%20of%20Fame'%20via%20Backstage.com%0A%0ALINK%20TO%3A%20https%3A%2F%2Fwww.backstage.com%2Fmagazine%2Farticle%2Fmel-brooks-gets-star-hollywood-walk-fame-57274%2F%0A%0ADESCRIPTION%3A%20The%20comedian%2C%20actor%20and%20producer%20who%20gave%20the%20world%20%22Blazing%20Saddles%2C%22%20%22Young%20Frankenstein%22%20and%20%22The%20Producers%22%20got%20a%20star%20Friday%20on%20the%20Hollywood%20Walk%20of%20Fame.)
[![Image 5: Google logo](blob:http://localhost/f0f56400545334337c03287a57681a5f)Add us](https://www.google.com/preferences/source?q=backstage.com)
Photo Source: Frederick M. Brown
LOS ANGELES – Nobody could say people walk all over Mel Brooks. Until now.
The comedian, actor and producer who gave the world "Blazing Saddles," "Young Frankenstein" and "The Producers" got a star Friday on the Hollywood Walk of Fame.
Brooks received the 2,406th star during a ceremony in front of the Egyptian Theatre. His son, Max, and friend, Carl Reiner, attended.
Brooks, who's 83, has won Emmy, Grammy, Oscar and Tony awards.
</excerpt>

## Search 3 — query: "Mel Brooks Golden Globe award"
### Rank 1 of 50 — 0.47 (passed on)
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
### Rank 2 of 50 — 0.43
<excerpt title="Mel Brooks hams it up for the camera alongside, Inger Stevens & George ...">
# That’s Entertainment! | Mel Brooks hams it up for the camera alongside, Inger Stevens & George Segal while attending the Golden Globe Awards | Facebook
[#Icons](https://www.facebook.com/hashtag/icons?__eep__=6&__cft__[0]=AZgx6yg4ePs6hXT62NvPcImJ5puQJbPoGKc9rCdKdyEo29ZeUqFyTBDbcmKJVmZTerHBtuIJ30dAi1QK6aVp7g8GWuO5J_W1SI8c3c6KE3xdnuMEwuiFXJIdhcHrvcAi1wdDUK-tbIc7Yuy8w2nQ1I3IMrIz7pwQdMoVlzje06_tiZJ4A9d5eHk9yJxAruvC&__tn__=*NK-R)
[#ClassicHollywood](https://www.facebook.com/hashtag/classichollywood?__eep__=6&__cft__[0]=AZgx6yg4ePs6hXT62NvPcImJ5puQJbPoGKc9rCdKdyEo29ZeUqFyTBDbcmKJVmZTerHBtuIJ30dAi1QK6aVp7g8GWuO5J_W1SI8c3c6KE3xdnuMEwuiFXJIdhcHrvcAi1wdDUK-tbIc7Yuy8w2nQ1I3IMrIz7pwQdMoVlzje06_tiZJ4A9d5eHk9yJxAruvC&__tn__=*NK-R)

# That’s Entertainment! | Mel Brooks hams it up for the camera alongside, Inger Stevens & George Segal while attending the Golden Globe Awards | Facebook
[#thatsentertainment](https://www.facebook.com/hashtag/thatsentertainment?__eep__=6&__cft__[0]=AZgx6yg4ePs6hXT62NvPcImJ5puQJbPoGKc9rCdKdyEo29ZeUqFyTBDbcmKJVmZTerHBtuIJ30dAi1QK6aVp7g8GWuO5J_W1SI8c3c6KE3xdnuMEwuiFXJIdhcHrvcAi1wdDUK-tbIc7Yuy8w2nQ1I3IMrIz7pwQdMoVlzje06_tiZJ4A9d5eHk9yJxAruvC&__tn__=*NK-R)
[](https://www.facebook.com/photo/?fbid=9896999673691038&set=gm.1982199612523371&idorvanity=975683823174960&__cft__[0]=AZgx6yg4ePs6hXT62NvPcImJ5puQJbPoGKc9rCdKdyEo29ZeUqFyTBDbcmKJVmZTerHBtuIJ30dAi1QK6aVp7g8GWuO5J_W1SI8c3c6KE3xdnuMEwuiFXJIdhcHrvcAi1wdDUK-tbIc7Yuy8w2nQ1I3IMrIz7pwQdMoVlzje06_tiZJ4A9d5eHk9yJxAruvC&__tn__=EH-R)
![Image 2](blob:http://localhost/85d8b181a20aeb64a3afc2f1c39d2480)
</excerpt>
### Rank 3 of 50 — 0.42
<excerpt title="List of awards and nominations received by Mel Brooks">
From Wikipedia, the free encyclopedia
Mel Brooks awards and nominations  
Brooks receiving a star on the Hollywood Walk of Fame in 2010
| Awards and nominations |  
| --- |  
| Award | Wins | Nominations |  
| Academy Awards | 1 | 3 |  
| BAFTA Awards | 0 | 1 |  
| Emmy Awards | 4 | 15 |  
| Drama Desk Awards | 3 | 4 |  
| Golden Globes | 0 | 6 |  
| Grammy Awards | 3 | 10 |  
| Laurence Olivier Awards | 1 | 1 |  
| Tony Awards | 3 | 3 |  
| WGA Awards | 2 | 6 |  
| Other | 10 | 13 |  
|  |  
Totals[[a]](https://en.wikipedia.org/wiki/List_of_awards_and_nominations_received_by_Mel_Brooks#cite_note-1)  
Wins 27  
Nominations 62  
Note
1.   ↑Certain award groups do not simply award one winner. They acknowledge several different recipients, have runners-up, and have third place. Since this is a specific recognition and is different from losing an award, runner-up mentions are considered wins in this award tally. For simplification and to avoid errors, each award in this list has been presumed to have had a prior nomination.
The following is a **list of awards and nominations received by Mel Brooks**.

Mel Brooks is an American actor, writer, director, producer, comedian, and composer. Over his 70 year career in film, theatre, and television Brooks has won an Academy Award (plus an Academy Honorary Award), four Emmy Awards, three Tony Awards, three Grammy Awards, and has been nominated for six Golden Globe Awards and one BAFTA Award. With his Tony wins for _The Producers_ in 2001, he became one of only eight people (now 21) who have won an Emmy, Grammy, Oscar and Tony Award.[[1]](https://en.wikipedia.org/wiki/List_of_awards_and_nominations_received_by_Mel_Brooks#cite_note-2) Additionally, he has received a Kennedy Center Honor in 2009, a Hollywood Walk of Fame star in 2010, the 41st AFI Life Achievement Award in 2013, a British Film Institute Fellowship in 2015, a National Medal of Arts in 2016, and a BAFTA Fellowship in 2017.
Brooks won the Academy Award for Best Original Screenplay for his satirical black comedy film _The Producers_ (1967) and was nominated for the Academy Award for Best Adapted Screenplay for the comedy horror film _Young Frankenstein_ (1974) and Best Original Song for the title theme to Western comedy film _Blazing Saddles_ (1974). He was nominated for the BAFTA Award for Best Screenplay for _Blazing Saddles_. Brooks has received six competitive Golden Globe Award nominations without a win. He won two Writers Guild of America Awards for Best Original Screenplay for _The Producers_ and _Blazing Saddles_.
He adapted _The Producers_ into a commercially and critically successful 2001 musical on Broadway starring Nathan Lane and Matthew Broderick. At the 55th Tony Awards he received three Tony Awards for Best Musical, Best Book of a Musical, and Best Original Score. Brooks also received three Drama Desk Awards, a Drama League Award, a New York Film Critics Circle Award, and two Outer Critics Circle Awards. The production transferred to the West End in London where Brooks won the Laurence Olivier Award for Best New Musical in 2005.
</excerpt>
### Rank 4 of 50 — 0.40
<excerpt title="Mel Brooks hams it up for the camera alongside, Inger Stevens & George ...">
# That’s Entertainment! | Mel Brooks hams it up for the camera alongside, Inger Stevens & George Segal while attending the Golden Globe Awards | Facebook
Log In
Log In
Forgot Account?
[](https://www.facebook.com/groups/975683823174960/?__cft__[0]=AZgx6yg4ePs6hXT62NvPcImJ5puQJbPoGKc9rCdKdyEo29ZeUqFyTBDbcmKJVmZTerHBtuIJ30dAi1QK6aVp7g8GWuO5J_W1SI8c3c6KE3xdnuMEwuiFXJIdhcHrvcAi1wdDUK-tbIc7Yuy8w2nQ1I3IMrIz7pwQdMoVlzje06_tiZJ4A9d5eHk9yJxAruvC&__tn__=%3C%3C%2CP-R)
## [That’s Entertainment!](https://www.facebook.com/groups/975683823174960/?__cft__[0]=AZgx6yg4ePs6hXT62NvPcImJ5puQJbPoGKc9rCdKdyEo29ZeUqFyTBDbcmKJVmZTerHBtuIJ30dAi1QK6aVp7g8GWuO5J_W1SI8c3c6KE3xdnuMEwuiFXJIdhcHrvcAi1wdDUK-tbIc7Yuy8w2nQ1I3IMrIz7pwQdMoVlzje06_tiZJ4A9d5eHk9yJxAruvC&__tn__=-UC%2CP-R) ·
Join
Will Chambers
·
Admin
·
Sunday, May 18, 2025 at 3:46 PM

# That’s Entertainment! | Mel Brooks hams it up for the camera alongside, Inger Stevens & George Segal while attending the Golden Globe Awards | Facebook
[May 18, 2025](https://www.facebook.com/groups/975683823174960/?multi_permalinks=1982199612523371&hoisted_section_header_type=recently_seen&__cft__[0]=AZgx6yg4ePs6hXT62NvPcImJ5puQJbPoGKc9rCdKdyEo29ZeUqFyTBDbcmKJVmZTerHBtuIJ30dAi1QK6aVp7g8GWuO5J_W1SI8c3c6KE3xdnuMEwuiFXJIdhcHrvcAi1wdDUK-tbIc7Yuy8w2nQ1I3IMrIz7pwQdMoVlzje06_tiZJ4A9d5eHk9yJxAruvC&__tn__=%2CO%2CP-R) ·
Mel Brooks hams it up for the camera alongside, Inger Stevens & George Segal while attending the Golden Globe Awards.
1965
[#LivingLegend](https://www.facebook.com/hashtag/livinglegend?__eep__=6&__cft__[0]=AZgx6yg4ePs6hXT62NvPcImJ5puQJbPoGKc9rCdKdyEo29ZeUqFyTBDbcmKJVmZTerHBtuIJ30dAi1QK6aVp7g8GWuO5J_W1SI8c3c6KE3xdnuMEwuiFXJIdhcHrvcAi1wdDUK-tbIc7Yuy8w2nQ1I3IMrIz7pwQdMoVlzje06_tiZJ4A9d5eHk9yJxAruvC&__tn__=*NK-R)
</excerpt>
### Rank 5 of 50 — 0.40
<excerpt title="Mel Brooks hams it up for the camera alongside, Inger Stevens & George ...">
# That’s Entertainment! | Mel Brooks hams it up for the camera alongside, Inger Stevens & George Segal while attending the Golden Globe Awards | Facebook
[May 18, 2025](https://www.facebook.com/groups/975683823174960/?multi_permalinks=1982199612523371&hoisted_section_header_type=recently_seen&__cft__[0]=AZgx6yg4ePs6hXT62NvPcImJ5puQJbPoGKc9rCdKdyEo29ZeUqFyTBDbcmKJVmZTerHBtuIJ30dAi1QK6aVp7g8GWuO5J_W1SI8c3c6KE3xdnuMEwuiFXJIdhcHrvcAi1wdDUK-tbIc7Yuy8w2nQ1I3IMrIz7pwQdMoVlzje06_tiZJ4A9d5eHk9yJxAruvC&__tn__=%2CO%2CP-R) ·
Mel Brooks hams it up for the camera alongside, Inger Stevens & George Segal while attending the Golden Globe Awards.
1965
[#LivingLegend](https://www.facebook.com/hashtag/livinglegend?__eep__=6&__cft__[0]=AZgx6yg4ePs6hXT62NvPcImJ5puQJbPoGKc9rCdKdyEo29ZeUqFyTBDbcmKJVmZTerHBtuIJ30dAi1QK6aVp7g8GWuO5J_W1SI8c3c6KE3xdnuMEwuiFXJIdhcHrvcAi1wdDUK-tbIc7Yuy8w2nQ1I3IMrIz7pwQdMoVlzje06_tiZJ4A9d5eHk9yJxAruvC&__tn__=*NK-R)

# That’s Entertainment! | Mel Brooks hams it up for the camera alongside, Inger Stevens & George Segal while attending the Golden Globe Awards | Facebook
[#Icons](https://www.facebook.com/hashtag/icons?__eep__=6&__cft__[0]=AZgx6yg4ePs6hXT62NvPcImJ5puQJbPoGKc9rCdKdyEo29ZeUqFyTBDbcmKJVmZTerHBtuIJ30dAi1QK6aVp7g8GWuO5J_W1SI8c3c6KE3xdnuMEwuiFXJIdhcHrvcAi1wdDUK-tbIc7Yuy8w2nQ1I3IMrIz7pwQdMoVlzje06_tiZJ4A9d5eHk9yJxAruvC&__tn__=*NK-R)
[#ClassicHollywood](https://www.facebook.com/hashtag/classichollywood?__eep__=6&__cft__[0]=AZgx6yg4ePs6hXT62NvPcImJ5puQJbPoGKc9rCdKdyEo29ZeUqFyTBDbcmKJVmZTerHBtuIJ30dAi1QK6aVp7g8GWuO5J_W1SI8c3c6KE3xdnuMEwuiFXJIdhcHrvcAi1wdDUK-tbIc7Yuy8w2nQ1I3IMrIz7pwQdMoVlzje06_tiZJ4A9d5eHk9yJxAruvC&__tn__=*NK-R)
</excerpt>

## Search 4 — query: "Dom DeLuise Walk of Fame Emmy Golden Globe"
### Rank 1 of 27 — 0.84 (passed on)
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
### Rank 2 of 27 — 0.53
<excerpt title="⭐ Dom DeLuise is seen showing his star on the Hollywood Walk of Fame ...">
# OldLight - ⭐ Dom DeLuise is seen showing his star on the... | Facebook
## OldLight's Post
com/hashtag/vintagephoto?__eep__=6&__cft__[0]=AZh3-tnqoqe2XUEodfD55ASb3GHjVOGJHz8RT2fRqil2cdgLbpdVW9lHXuYRWhnsw6kLWuk7eHeO1pRxKOY5MFMn9DqESTtpwv2yoelHDgjm_3qvnZjppO-hJCnvAk-qbnWtrf5dLZnRtvv9rWWvYfPyyUFPGpPN&__tn__=*NK-R)[#FilmHistory](https://www.facebook.com/hashtag/filmhistory?__eep__=6&__cft__[0]=AZh3-tnqoqe2XUEodfD55ASb3GHjVOGJHz8RT2fRqil2cdgLbpdVW9lHXuYRWhnsw6kLWuk7eHeO1pRxKOY5MFMn9DqESTtpwv2yoelHDgjm_3qvnZjppO-hJCnvAk-qbnWtrf5dLZnRtvv9rWWvYfPyyUFPGpPN&__tn__=*NK-R)[#HollywoodHistory](https://www.facebook.com/hashtag/hollywoodhistory?__eep__=6&__cft__[0]=AZh3-tnqoqe2XUEodfD55ASb3GHjVOGJHz8RT2fRqil2cdgLbpdVW9lHXuYRWhnsw6kLWuk7eHeO1pRxKOY5MFMn9DqESTtpwv2yoelHDgjm_3qvnZjppO-hJCnvAk-qbnWtrf5dLZnRtvv9rWWvYfPyyUFPGpPN&__tn__=*NK-R)[#ComedyHistory](https://www.facebook.
</excerpt>
### Rank 3 of 27 — 0.49
<excerpt title="⭐ Dom DeLuise is seen showing his star on the Hollywood Walk of Fame ...">
# OldLight - ⭐ Dom DeLuise is seen showing his star on the... | Facebook
## OldLight's Post
com/hashtag/comedyhistory?__eep__=6&__cft__[0]=AZh3-tnqoqe2XUEodfD55ASb3GHjVOGJHz8RT2fRqil2cdgLbpdVW9lHXuYRWhnsw6kLWuk7eHeO1pRxKOY5MFMn9DqESTtpwv2yoelHDgjm_3qvnZjppO-hJCnvAk-qbnWtrf5dLZnRtvv9rWWvYfPyyUFPGpPN&__tn__=*NK-R)[#OldHollywood](https://www.facebook.com/hashtag/oldhollywood?__eep__=6&__cft__[0]=AZh3-tnqoqe2XUEodfD55ASb3GHjVOGJHz8RT2fRqil2cdgLbpdVW9lHXuYRWhnsw6kLWuk7eHeO1pRxKOY5MFMn9DqESTtpwv2yoelHDgjm_3qvnZjppO-hJCnvAk-qbnWtrf5dLZnRtvv9rWWvYfPyyUFPGpPN&__tn__=*NK-R)
[](https://www.facebook.com/photo/?fbid=1380415687438464&set=a.457209216425787&__cft__[0]=AZh3-tnqoqe2XUEodfD55ASb3GHjVOGJHz8RT2fRqil2cdgLbpdVW9lHXuYRWhnsw6kLWuk7eHeO1pRxKOY5MFMn9DqESTtpwv2yoelHDgjm_3qvnZjppO-hJCnvAk-qbnWtrf5dLZnRtvv9rWWvYfPyyUFPGpPN&__tn__=EH-R)

# OldLight - ⭐ Dom DeLuise is seen showing his star on the... | Facebook
## OldLight's Post
![Image 3](blob:http://localhost/85d8b181a20aeb64a3afc2f1c39d2480)
![Image 4](blob:http://localhost/2b45e6f1a2ae097354c0b291152873d5)
All reactions:
2
Like
Comment
![Image 5](blob:http://localhost/85d8b181a20aeb64a3afc2f1c39d2480)
![Image 6](blob:http://localhost/2b45e6f1a2ae097354c0b291152873d5)
All reactions:
2
Like
Comment
</excerpt>
### Rank 4 of 27 — 0.48
<excerpt title="⭐ Dom DeLuise is seen showing his star on the Hollywood Walk of Fame ...">
# OldLight - ⭐ Dom DeLuise is seen showing his star on the... | Facebook
## OldLight's Post
[March 31](https://www.facebook.com/OldlightFB/posts/pfbid0LweL1T8x7CemGyPPEDzuaxoobgURbQGMtjqmiNwa35naHeBWyWYtJUWooY2mqg8hl?__cft__[0]=AZh3-tnqoqe2XUEodfD55ASb3GHjVOGJHz8RT2fRqil2cdgLbpdVW9lHXuYRWhnsw6kLWuk7eHeO1pRxKOY5MFMn9DqESTtpwv2yoelHDgjm_3qvnZjppO-hJCnvAk-qbnWtrf5dLZnRtvv9rWWvYfPyyUFPGpPN&__tn__=%2CO%2CP-R) ·
Dom DeLuise is seen showing his star on the Hollywood Walk of Fame, captured in a moment that reflects recognition built through years of work in film and television.
The image highlights a personal connection to a public honor, where achievement is represented in a simple, tangible form on the street.
It suggests a mix of pride and humor, consistent with a career known for warmth and expressive performance.

# OldLight - ⭐ Dom DeLuise is seen showing his star on the... | Facebook
## OldLight's Post
[#DomDeLuise](https://www.facebook.com/hashtag/domdeluise?__eep__=6&__cft__[0]=AZh3-tnqoqe2XUEodfD55ASb3GHjVOGJHz8RT2fRqil2cdgLbpdVW9lHXuYRWhnsw6kLWuk7eHeO1pRxKOY5MFMn9DqESTtpwv2yoelHDgjm_3qvnZjppO-hJCnvAk-qbnWtrf5dLZnRtvv9rWWvYfPyyUFPGpPN&__tn__=*NK-R)[#HollywoodWalkOfFame](https://www.facebook.com/hashtag/hollywoodwalkoffame?__eep__=6&__cft__[0]=AZh3-tnqoqe2XUEodfD55ASb3GHjVOGJHz8RT2fRqil2cdgLbpdVW9lHXuYRWhnsw6kLWuk7eHeO1pRxKOY5MFMn9DqESTtpwv2yoelHDgjm_3qvnZjppO-hJCnvAk-qbnWtrf5dLZnRtvv9rWWvYfPyyUFPGpPN&__tn__=*NK-R)[#ClassicHollywood](https://www.facebook.com/hashtag/classichollywood?__eep__=6&__cft__[0]=AZh3-tnqoqe2XUEodfD55ASb3GHjVOGJHz8RT2fRqil2cdgLbpdVW9lHXuYRWhnsw6kLWuk7eHeO1pRxKOY5MFMn9DqESTtpwv2yoelHDgjm_3qvnZjppO-hJCnvAk-qbnWtrf5dLZnRtvv9rWWvYfPyyUFPGpPN&__tn__=*NK-R)[#VintagePhoto](https://www.facebook.
</excerpt>
### Rank 5 of 27 — 0.48
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

## Search 5 — query: ""county fair" "The Muppet Movie" cameo"
### Rank 1 of 44 — 0.74 (passed on)
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
### Rank 2 of 44 — 0.62
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
### Rank 3 of 44 — 0.62
<excerpt title="Celebrate 40 Years of The Muppet Movie with These “ ...">
**Speaking of James Frawley…**The director of _The Muppet Movie_ is himself suitably colorful—perfect for wrangling a host of hilarious, human-esque characters! Frawley got his start on stage in the acclaimed 1960s off-Broadway improvisational troupe The Premise, later appearing on TV’s _Gunsmoke_, _Outer Limits_, and _The Danny Kaye Show_. In the meantime, Frawley was cultivating his skills as a photographer; helming an acclaimed short film called _J-24_ led Frawley to directing, and he eventually won an Emmy Award as director on the fan-favorite ‘60s sitcom _The Monkees_.
**Just a Frog and His Banjo…**_The Muppet Movie_ memorably opens with Kermit the Frog, perched on a log in the lush green swamp he calls “home,” playing his banjo and singing one of his now signature tunes: “Rainbow Connection.” Ever wonder how they managed to film that scene? The man behind the frog, Jim Henson, spent three full days under water inside a specially constructed “bathysphere,” operating Kermit through rubber-sleeved arms! According to the film’s press notes, the submersible was made from two aluminum jet-engine containers and was wired for both sight (a video monitor which enabled Henson to see Kermit’s performance) and sound (Henson’s microphone hookup).
**Even Muppets Need Transportation…**Did you know that Fozzie Bear drives two different cars in _The Muppet Movie_? One is a 1947 Ford “Woody” station wagon, and the other is a 1951 Studebaker Champion. Meanwhile, Gonzo and his chicken companion Camilla drive a 1969 Citreon plumbing repair truck, while later in the film, Dr. Teeth and the Electric Mayhem are seen tooling around in a brightly painted 1961 International school bus.

**Special Guest Cameos A-Plenty…**Most Muppet fans are familiar with _The Muppet Movie_’s cavalcade of guest appearances—from radio/ventriloquist legend Edgar Bergen (in his final film appearance) and Madeline Kahn to Steve Martin, Richard Pryor, and Mel Brooks, the film boasts a veritable “who’s who” of comedy talent. One such cameo is Oscar nominee Elliott Gould; according to the film’s press material, Gould was once asked to emcee the Miss Universe Pageant, which he declined due to a busy filming schedule. But the pageant world came ‘round again—albeit fictitiously—when Gould was asked to appear in _The Muppet Movie_ as the host of the quaint Bogen County Fair’s beauty contest… won by Miss Piggy, of course!
**Some Hollywood History…**The film follows the Muppets on their journey to Hollywood, as they dream of big-screen stardom—all the while pursued by the flamboyantly evil Doc Hopper (Charles Durning), a fast-food tycoon who wants Kermit to star in his commercials. The climactic scene where Kermit and friends finally face off against Doc and his henchmen is portrayed in classic western-film style… and was even shot at the very same location as the showdown in Gary Cooper’s iconic 1952 western _High Noon_.
**A Truly Lasting Legacy…**In 2009, _The Muppet Movie_ was named to the prestigious National Film Registry by the Library of Congress. So what exactly does that mean? Every year since 1988, the registry’s Preservation Board selects 25 films—deemed “culturally, historically, or aesthetically significant”—that showcase the enduring range and diversity of American film heritage, all in an effort to increase awareness for its preservation. We’re sure any Muppet fan would agree: Preserving _The Muppet Movie_ for future generations is a _fantastic_ idea!
Want to keep celebrating this Muppetational milestone? Check out our 10 Fan-tastic Milestones Pin Set, which features an exclusive pin celebrating 40 years of _The Muppet Movie._
</excerpt>
### Rank 4 of 44 — 0.56
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
### Rank 5 of 44 — 0.36
<excerpt title="The Muppet Movie">
| Box office | $76.7 million[[7]](https://en.wikipedia.org/wiki/The_Muppet_Movie#cite_note-8)[[8]](https://en.wikipedia.org/wiki/The_Muppet_Movie#cite_note-9) |
_**The Muppet Movie**_ is a 1979 musicalroadcomedy film, directed by James Frawley and produced by Jim Henson, and the first theatrical film to feature the Muppets. A co-production between the United Kingdom and the United States, the film was written by _The Muppet Show_ writers Jerry Juhl and Jack Burns. Produced during the third season of _The Muppet Show_, the film tells the origin story of the Muppets, as Kermit the Frog embarks on a cross-country trip to Los Angeles, encountering several of the Muppets—who all share the same ambition of finding success in professional show business—along the way while being pursued by Doc Hopper, a greedy restaurateur with intentions of recruiting Kermit to promote his frog legs business.
The film stars Muppet performers Henson, Frank Oz, Jerry Nelson, Richard Hunt, and Dave Goelz, as well as Charles Durning and Austin Pendleton, and it features cameo appearances by Bob Hope, Dom DeLuise, James Coburn, Cloris Leachman, Richard Pryor, Telly Savalas, Edgar Bergen (in his final film appearance before his death), Orson Welles, Madeline Kahn, Milton Berle, Carol Kane, Steve Martin, Mel Brooks, Elliott Gould, and Paul Williams. Notable for its surreal humour, meta-references and prolific use of cameos, _The Muppet Movie_ was released by Associated Film Distribution in the United Kingdom on May 31, 1979, and in the United States on June 22, 1979.
The film received critical praise, including two Academy Award nominations for Paul Williams and Kenneth Ascher's musical score and their song "Rainbow Connection". The film grossed $76.7 million worldwide against an $8 million budget. _The Muppet Movie_ was followed by seven feature films starring the Muppets as well as several more television series and media. In 2009, the film was deemed "culturally, historically, or aesthetically significant" by the Library of Congress and selected for preservation in the National Film Registry.
</excerpt>

## Search 6 — query: "Bob Hope Golden Globe award"
### Rank 1 of 53 — 0.61 (passed on)
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
### Rank 2 of 53 — 0.59
<excerpt title="List of awards and nominations received by Bob Hope">
### Memorials and tributes
*   The Bob Hope Theatre, an amateur theatre (although professional musicians receive payment) in Eltham, London, where he was born. He personally funded the theatre in 1980 to develop further projects for the venue.  
*   Blue plaque at 44, Craigton Road Eltham, London, Hope's place of birth.  
*   The Bob Hope Theatre, an on-base movie theatre and lecture hall at Marine Corps Air Station Miramar, San Diego, California.[[21]](https://en.wikipedia.org/wiki/List_of_awards_and_nominations_received_by_Bob_Hope#cite_note-mccsmiramar-21)  
*   Hope had a long and close association with Southern Methodist University in Dallas. His donations of over $800,000 enabled the opening of the Bob Hope Theatre in the Owen Fine Arts Center of the Meadows School of the Arts, and two theater scholarships and an award are named in his honor.[[22]](https://en.wikipedia.org/wiki/List_of_awards_and_nominations_received_by_Bob_Hope#cite_note-Southern_Methodist_University-22)  
*   "The Bob Hope Chow Hall", the dining facility at Camp Lemonnier, Djibouti, Africa.[[23]](https://en.wikipedia.org/wiki/List_of_awards_and_nominations_received_by_Bob_Hope#cite_note-23)  
*   Bob Hope Primary School, a primary school located on Kadena US Air Force Base, in Okinawa, Japan.  
*   The historic Bob Hope Patriotic Hall building on Figueroa Street in Los Angeles County was named in his honor on August 3, 2003, by the Los Angeles County Board of Supervisors.[[24]](https://en.wikipedia.org/wiki/List_of_awards_and_nominations_received_by_Bob_Hope#cite_note-Molina_2009-24)  
*   In a bill passed by Congress in 2008, the research library at the Ellis Island Immigration Museum was renamed the Bob Hope Memorial Library.[[25]](https://en.wikipedia.org/wiki/List_of_awards_and_nominations_received_by_Bob_Hope#cite_note-Chan_2008-25)  

### Memorials and tributes
*   At the U.S. Naval Academy, Alumni Hall is home to the Bob Hope Performing Arts Center.[[26]](https://en.wikipedia.org/wiki/List_of_awards_and_nominations_received_by_Bob_Hope#cite_note-FOOTNOTEBlake2010135-26)  
*   In 2009 "A National Salute to Bob Hope and the Military" was dedicated in San Diego, California.[[27]](https://en.wikipedia.org/wiki/List_of_awards_and_nominations_received_by_Bob_Hope#cite_note-portofsandiego_tribute-27)

### Stars on the Hollywood Walk of Fame
[edit]
*   For contributions to the live theater, radio, motion picture, and television, Hope was honored with four stars on the Hollywood Walk of Fame.[[28]](https://en.wikipedia.org/wiki/List_of_awards_and_nominations_received_by_Bob_Hope#cite_note-HWOFDB-28)  
*   _Motion picture star_ at 6541 Hollywood Blvd.  
*   _Radio star_ at 6141 Hollywood Blvd.  
*   _TV star_ at 6758 Hollywood Blvd.  
*   _Live theatre special plaque_ at 7021 Hollywood Blvd.

### Golden Globe Awards
[edit]
*   Special Achievement Award 1958 "For an Ambassador of Good Will."[[29]](https://en.wikipedia.org/wiki/List_of_awards_and_nominations_received_by_Bob_Hope#cite_note-29)  
*   Cecil B. DeMille Award 1963 [[30]](https://en.wikipedia.org/wiki/List_of_awards_and_nominations_received_by_Bob_Hope#cite_note-30)
Hope received more than 50 honorary degrees. These include:
</excerpt>
### Rank 3 of 53 — 0.50
<excerpt title="List of awards and nominations received by Bob Hope">
### Golden Globe Awards
24.   ↑Chan, Sewell (November 24, 2008). "Thanks for the Ellis Island Memories ... Bob Hope?". _The New York Times_. Retrieved August 15, 2012.  
25.   ↑Blake 2010, p.135.  
26.   ↑"A Tribute to Bob Hope: Thanks for the Memories". Unified Port of San Diego. July 8, 2009. Retrieved August 16, 2012.  
27.   ↑"Bob Hope". The Hollywood Walk of Fame database. Retrieved August 15, 2012.  
28.   ↑"Bob Hope". _IMDb_.  
29.   ↑"Bob Hope".  
30.   ↑"Bob | Bob Hope". _bobhope.org_. Archived from the original on October 5, 2016.  
31.   [↑](https://en.wikipedia.org/wiki/List_of_awards_and_nominations_received_by_Bob_Hope#cite_ref-FOOTNOTE''TV_Guide_Book_of_Lists''2007188_32-0 "Jump up")_TV Guide Book of Lists_ 2007, p.188.
*   Blake, Allison (2010). _Explorer's Guide Baltimore, Annapolis & The Chesapeake Bay: A Great Destination_. Explorer's Guides. Woodstock, VT: Countryman Press. ISBN978-1-58157-112-7.  
*   Grudens, Richard (2002). _The Spirit of Bob Hope: One Hundred Years, One Million Laughs_. Sioux Falls, SD: Pine Hill Press. ISBN978-1-57579-227-9.  
*   _TV Guide Book of Lists_. Philadelphia, PA: Running Press. 2007. ISBN978-0-7624-3007-9.
Preceded by**Oscarshost**
12th Academy AwardsSucceeded by  
Preceded by**Oscarshost**
14th and 15th Academy AwardsSucceeded by  
Preceded by**Oscarshost**

### Golden Globe Awards
17th (with John Cromwell) and 18th Academy Awards (with James Stewart)Succeeded by  
Preceded by**Oscarshost**
25th Academy Awards (with Conrad Nagel)Succeeded by  
Preceded by**Oscarshost**
27th Academy Awards (with Thelma Ritter)Succeeded by  
Preceded by**Oscarshost**
30th (with Jack Lemmon, David Niven, Rosalind Russell, and James Stewart), 31st (with Jerry Lewis, David Niven, Laurence Olivier, Tony Randall, and Mort Sahl), 32nd, 33rd, and 34th Academy AwardsSucceeded by  
Preceded by**Oscarshost**
37th, 38th, 39th, and 40th Academy AwardsSucceeded by  
Preceded by**Oscarshost**
47th Academy Awards (with [Sammy Davis, Jr.](https://en.wikipedia.org/wiki/Sammy_Davis,_Jr. "Sammy Davis, Jr."), Shirley MacLaine, and Frank Sinatra)Succeeded by  
Preceded by**Oscarshost**
50th Academy AwardsSucceeded by  
Awards  
Preceded by**Sylvanus Thayer Award recipient**
1968 Succeeded by  
Preceded by**Jean Hersholt Humanitarian Award**
1959 Succeeded by  
Preceded by**Recipient of The Ronald Reagan Freedom Award**
1997 Succeeded by
</excerpt>
### Rank 4 of 53 — 0.46
<excerpt title="List of awards and nominations received by Bob Hope">
### Golden Globe Awards
| Nevada | **11 June 1970** | UNLV | Doctor of Humane Letters (DHL) |  
| Tennessee | **25 May 1971** | Bethel College | Doctor of Humane Letters (DHL) |  
| New York | **30 May 1971** | St. Bonaventure University | Doctor of Laws (LL.D.) |  
| California | **12 June 1971** | Santa Clara University | Doctor of Humane Letters (DHL) |  
| Florida | **6 April 1972** | Jacksonville University | Doctor of Fine Arts (DFA) |  
| Ohio | **1 June 1972** | Wilberforce University | Doctor of Humane Letters (DHL) |  
| California | **12 April 1973** | Pepperdine University | Doctor of Laws (LL.D.) |  
| Missouri | **27 May 1973** | Drury College | Doctor of Humane Service |  
| West Virginia | **10 May 1974** | Salem College | Doctor of International Relations |  
| Indiana | **12 May 1974** | Indiana University | Doctor of Humane Letters (DHL) |  
| Florida | **19 February 1975** | Florida Southern College | Doctor of Humane Letters (DHL) |  
| Michigan | **18 May 1975** | Northwood Institute | Doctor of Humane Letters (DHL) |  
| Vermont | **24 May 1975** | Norwich University | Doctor of Humane Letters (DHL) |  
| Pennsylvania | **1 June 1975** | University of Scranton | Doctor of Laws (LL.D.) |  
| Utah | **5 June 1975** | Utah State University | Doctor of Humane Letters (DHL) |  
| New York | **28 April 1976** | Mercy College | Doctor of Humane Letters (DHL) |  
| Iowa | **9 May 1976** | St. Ambrose College | Doctor of Public Service |  
| Ohio | **30 May 1976** | John Carroll University | Doctor of Humane Letters (DHL) |
</excerpt>
### Rank 5 of 53 — 0.44
<excerpt title="List of awards and nominations received by Bob Hope">
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

## Search 7 — query: "Milton Berle Emmy award Golden Globe award"
### Rank 1 of 78 — 0.67 (passed on)
<excerpt title="Milton Berle - Comedians">
Milton Berle was an American comedian and actor.
Berle's career as an entertainer spanned over 80 years, first in silent films and on stage as a child actor, then in radio, movies and television. As the host of NBC's Texaco Star Theatre (1948-55), he was the first major American television star and was known to millions of viewers as "Uncle Miltie" and "Mr. Television" during the first Golden Age of Television. He was honored with two stars on the Hollywood Walk of Fame for his work in both radio and TV.
Berle won the Emmy for Most Outstanding Kinescoped Personality in 1950. In 1979, Berle was awarded a special Emmy Award, titled "Mr. Television." He was twice nominated for Emmys for his acting, in 1962 and 1995.
Berle was inducted into the Television Hall of Fame in 1984. On December 5, 2007, Berle was inducted into the California Hall of Fame.
</excerpt>
### Rank 2 of 78 — 0.65
<excerpt title="Milton Berle">
## Final role and death
*   Berle won the Emmy for Most Outstanding Kinescoped Personality in 1950, the same year his show, the _Texaco Star Theater_, won the Emmy for Best Kinescope Show.[[102]](https://en.wikipedia.org/wiki/Milton_Berle#cite_note-102) He was twice nominated for Emmys for his acting, in 1962 and 1995.[[103]](https://en.wikipedia.org/wiki/Milton_Berle#cite_note-103)[[104]](https://en.wikipedia.org/wiki/Milton_Berle#cite_note-104) In 1979, Berle was awarded a special Emmy Award, titled "Mr. Television."[[105]](https://en.wikipedia.org/wiki/Milton_Berle#cite_note-105)  
*   The Hollywood Walk of Fame, on February 8, 1960, inducted Berle with two stars, for television and radio.[[106]](https://en.wikipedia.org/wiki/Milton_Berle#cite_note-106)  
*   Berle was in the first group of inductees into the Television Hall of Fame in 1984.[[107]](https://en.wikipedia.org/wiki/Milton_Berle#cite_note-107)  
*   On December 5, 2007, California Governor Arnold Schwarzenegger and First Lady Maria Shriver inducted Berle into the California Hall of Fame, located at The California Museum for History, Women and the Arts.[[108]](https://en.wikipedia.org/wiki/Milton_Berle#cite_note-108)

## Final role and death
*   _Earl Carroll's Vanities of 1932_ (1932) – revue – in the roles of "Mortimer" in the sketch "Mourning Becomes Impossible", "Joe Miller, Jr." in "What Price Jokes", "Frank" in "Two Sailors", "Paul" in "The Cabinet of Doctor X", the "Announcer" in "Studio W.M.C.A." the "Defendant" in "Trial by Jury" and "Milton" in "The Bar Relief"  
*   _Saluta_ (1934) – musical – co-lyricist and performer cast in the role of "'Windy' Walker"  
*   _See My Lawyer_ (1939) – play – performer cast in the role of "Arthur Lee"  
*   _Ziegfeld Follies of 1943_ (1943) – revue – performer in the role of "Cecil" in _Counter Attack_, "J. Pierswift Armour" in _The Merchant of Venison_, "Perry Johnson" in _Loves-A-Poppin_, "Escamillio" in _Carmen in Zoot_, "Charlie Grant" _Mr Grant Goes To Washington_, "'The Micromaniac' Singer" and "'Hold That Smile' Dancer"  
*   _I'll Take the High Road_ (1943) – play – co-producer  
*   _Seventeen_ (1951) – musical – co-producer  
*   _The Goodbye People_ (1968) – performer cast in the role of "Max Silverman"
</excerpt>
### Rank 3 of 78 — 0.63
<excerpt title="Milton Berle">
## Final role and death
[edit]
The crypt of Milton Berle, at Hillside Memorial Park
Berle guest-starred as Uncle Leo in the _Kenan & Kel_ special "Two Heads Are Better than None", which premiered in 2000. This would be his last acting role._[citation needed_]
In April 2001, Berle announced that a malignant tumor had been found in his colon, but he had declined surgery.[[94]](https://en.wikipedia.org/wiki/Milton_Berle#cite_note-94) Berle's wife said the tumor was growing so slowly that it would take 10 to 12 years to affect him in any significant or life-threatening way. One year after the announcement, on March 27, 2002, Berle died in Los Angeles from colon cancer. He died on the same day as Dudley Moore and Billy Wilder.[[84]](https://en.wikipedia.org/wiki/Milton_Berle#cite_note-wp-84)[[95]](https://en.wikipedia.org/wiki/Milton_Berle#cite_note-95)
Berle reportedly left arrangements to be buried with his second wife, Ruth, at Mount Sinai Memorial Park Cemetery in Burbank, but his body was cremated and interred at Hillside Memorial Park Cemetery in Culver City. Warren Cowan, Berle's publicist, told _The New York Times_, "I only know he told me he bought plots at Hillside, and it was his idea."[[96]](https://en.wikipedia.org/wiki/Milton_Berle#cite_note-96) Many celebrities attended his funeral.[[97]](https://en.wikipedia.org/wiki/Milton_Berle#cite_note-97)[[98]](https://en.wikipedia.org/wiki/Milton_Berle#cite_note-98) In addition to his third wife, Lorna Adams, Berle was survived by his three children and extended family.[[99]](https://en.wikipedia.org/wiki/Milton_Berle#cite_note-99)[[100]](https://en.wikipedia.org/wiki/Milton_Berle#cite_note-100)[[101]](https://en.wikipedia.org/wiki/Milton_Berle#cite_note-101)

## Final role and death
*   Berle won the Emmy for Most Outstanding Kinescoped Personality in 1950, the same year his show, the _Texaco Star Theater_, won the Emmy for Best Kinescope Show.[[102]](https://en.wikipedia.org/wiki/Milton_Berle#cite_note-102) He was twice nominated for Emmys for his acting, in 1962 and 1995.[[103]](https://en.wikipedia.org/wiki/Milton_Berle#cite_note-103)[[104]](https://en.wikipedia.org/wiki/Milton_Berle#cite_note-104) In 1979, Berle was awarded a special Emmy Award, titled "Mr. Television."[[105]](https://en.wikipedia.org/wiki/Milton_Berle#cite_note-105)  
*   The Hollywood Walk of Fame, on February 8, 1960, inducted Berle with two stars, for television and radio.[[106]](https://en.wikipedia.org/wiki/Milton_Berle#cite_note-106)  
*   Berle was in the first group of inductees into the Television Hall of Fame in 1984.[[107]](https://en.wikipedia.org/wiki/Milton_Berle#cite_note-107)  
*   On December 5, 2007, California Governor Arnold Schwarzenegger and First Lady Maria Shriver inducted Berle into the California Hall of Fame, located at The California Museum for History, Women and the Arts.[[108]](https://en.wikipedia.org/wiki/Milton_Berle#cite_note-108)
</excerpt>
### Rank 4 of 78 — 0.51
<excerpt title="Milton Berle wins 'Mr. Television' award at the Emmys - UPI">
# Photo: Milton Berle wins "Mr. Television" award at the Emmys - ARKFPL19790909075 - UPI.com
- [x]
*      
*   U.S. News  
*   World News- [x]   
    *   Korea Regional Review  
    *   Latin America Region

*   Odd News  
*   Entertainment- [x]   
    *   Movies  
    *   Music  
    *   TV

*   Sports- [x]   
    *   NFL  
    *   MLB  
    *   NBA  
    *   Soccer

*   Voices  
*   Photos- [x]   
    *   News  
    *   US News  
    *   World News  
    *   Entertainment  
    *   Sports

*   Archive- [x]   
    *   Almanac

*     
*   - [x]
Trending
Malicious software
Iran, Kuwait
Apple outage
'DWTS' finale
Canyon crash
'Sugah' trailer
WWE 'Raw'
Voyager 1
'Unicorn' deer
https://www.upi.com/News_Photos/lp/9e2247924f32c01e759858f0ec2420b2/https://www.upi.com/News_Photos/view/upi/9e2247924f32c01e759858f0ec2420b2/Milton-Berle-wins-Mr-Television-award-at-the-Emmys/Milton Berle born 12 July 1908, died 27 March 2002, Emmy award, American, comedian, born Milton Berlinger, manic host of NBC's Texaco Star Theater (1948-1955), first major star of television, known as Uncle Miltie, Mr. Television UPI UPI https://cdnph.upi.com/pv/upi/9e2247924f32c01e759858f0ec2420b2/Milton-Berle.jpg
Home / Photos

# Milton Berle wins "Mr. Television" award at the Emmys
Milton Berle holds his "Mr. Television" Special Tribute that was awarded him at the 31st annual Emmy Awards on September 9, 1979 in Pasadena. (UPI Photo/Glenn Waggner/Files)
License Photo
Back to top
About UPIContactCorrectionsAdvertisements
Copyright © 2026 United Press International, Inc. All Rights Reserved.
Terms of UsePrivacy Policy
Privacy Manager
CLOSE X
</excerpt>
### Rank 5 of 78 — 0.49
<excerpt title="Milton Berle">
## Selected filmography
88.   ↑Cox, R.L. _The Verdict Is In_. Heritage Committee, California (1983), p. 241.  
89.   ↑Sutton, M.A. _Aimee Semple McPherson and the Resurrection of Christian America_. Harvard University Press (2009), p. 271.  
90.   ↑Cox (2008), pp. 240-41  
91.   ↑"Obituary Milton Berle". _The Guardian_. March 29, 2002. Retrieved September 11, 2025.  
92.   ↑Amos, David (September 16, 2010). "More About Oscar Levant". _San Diego Jewish World_. Retrieved August 14, 2021.  
93.   ↑Jet, October 1, 1964  
94.   ↑"Milton Berle diagnosed with cancerous tumor". _CNN_. April 25, 2001. Archived from the original on January 21, 2012. Retrieved December 6, 2007.  
95.   ↑"'Mr. Television', Milton Berle, dead at 93". CNN. March 28, 2002. Archived from the original on June 5, 2004. Retrieved January 27, 2009.  
96.   ↑"Boldface Names". _New York Times_. March 29, 2002.  
97.   ↑"Berle's Pals Rise To The Occasion". _CBS News_. April 2, 2002.  
98.   ↑"Berle laid to rest amid fond laughter". _Deseret News_. April 2, 2002.  
99.   ↑"Milton Berle, TV's First Star As 'Uncle Miltie,' Dies at 93". _The New York Times_. March 28, 2002.  

## Selected filmography
100.   ↑"Archived copy". Archived from the original on May 25, 2014. Retrieved May 24, 2014.`{{cite web}}`: CS1 maint: archived copy as title (link)  
101.   ↑Natale, Richard (March 27, 2002). "'Mr. TV' Milton Berle dies". _Variety.com_. Retrieved June 24, 2014.  
102.   ↑"2nd Emmy Awards Nominees and Winners". _Emmys.com_.  
103.   ↑"14th Emmy Awards Nominees and Winners". _Emmys.com_.  
104.   ↑"47th Emmy Awards Nominees and Winners". _Emmys.com_.  
105.   ↑Saxon, Reed (September 22, 2019). "A look back at some earlier Emmy Awards". _Tucson.com_.  
106.   ↑"Milton Berle | Hollywood Walk of Fame". _www.walkoffame.com_. Archived from the original on February 3, 2014. Retrieved January 15, 2022.  
107.   ↑"Milton Berle Hall of Fame Induction 1984". _Emmys.com_.  
108.   ↑Berle inducted into California Hall of FameArchived January 10, 2008, at the Wayback Machine, California Museum.  
109.   ↑"_Milton Berle Hides Out at The Ricardo's_". Classic TV Archives. Retrieved October 22, 2016._[permanent dead link_]
</excerpt>

## Search 8 — query: "Cloris Leachman walk of fame"
### Rank 1 of 85 — 0.73 (passed on)
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
### Rank 2 of 85 — 0.72
<excerpt title="Cloris Leachman">
## Early life and education
### 1989–2021: Later career and final roles
One of Leachman's final roles was as Zorya Vechernyaya, one of the "old gods" who represented the evening star, in season one (2019) of the Showtime series _American Gods_. Leachman appears in the film _Not to Forget_ (2021). The movie, directed by Valerio Zanoli, stars Karen Grassle and five Academy Award winners: Leachman, [Louis Gossett Jr.](https://en.wikipedia.org/wiki/Louis_Gossett_Jr. "Louis Gossett Jr."), [Tatum O'Neal](https://en.wikipedia.org/wiki/Tatum_O'Neal "Tatum O'Neal"), George Chakiris, and Olympia Dukakis.[[36]](https://en.wikipedia.org/wiki/Cloris_Leachman#cite_note-36)[[37]](https://en.wikipedia.org/wiki/Cloris_Leachman#cite_note-37) In 2020 Leachman played the declining grandmother of a budding drag queen, who is struggling to cling to her last shred of freedom, in _Jump, Darling_.
On May 14, 2006, she was awarded an honorary doctorate in fine arts from Drake University.[[38]](https://en.wikipedia.org/wiki/Cloris_Leachman#cite_note-38)

## Acting credits and awards
[edit]
*   Leachman was inducted into the Television Academy Hall of Fame in 2011. That same year, she was ranked number 23 on the TV Guide Network special _Funniest Women on TV_.[[39]](https://en.wikipedia.org/wiki/Cloris_Leachman#cite_note-39)  
*   On June 20, 2014, Leachman received an honorary degree from her alma mater, Northwestern University.[[40]](https://en.wikipedia.org/wiki/Cloris_Leachman#cite_note-40)  
*   In 2017, she received PETA's Lifetime Achievement Award for her dedication to animal-rights issues.[[41]](https://en.wikipedia.org/wiki/Cloris_Leachman#cite_note-41)  
*   She was awarded a Star on the Hollywood Walk of Fame in the Television Category on September 22, 1980, at 6435 Hollywood Boulevard.[[42]](https://en.wikipedia.org/wiki/Cloris_Leachman#cite_note-42)
Leachman in November 2015
From 1953 to 1978, Leachman was married to Hollywood impresarioGeorge Englund. Her former mother-in-law was character actress Mabel Albertson. The marriage produced four sons and one daughter: Bryan (died 1986), Morgan, Adam, Dinah, and George. Some of them are in show business. Her son Morgan played Dylan on _Guiding Light_ for several years. The Englunds were Bel Air neighbors of Judy Garland, Sidney Luft, and their children, Lorna and Joey Luft, during the early 1960s. Lorna Luft stated in her memoir _Me and My Shadows: A Family Memoir_ that Leachman was "the kind of mom I'd only seen on TV". Knowing of the turmoil at the Luft home, but never mentioning it, Leachman prepared meals for the children and made them feel welcome when they needed a place to stay.[[43]](https://en.wikipedia.org/wiki/Cloris_Leachman#cite_note-43)
</excerpt>
### Rank 3 of 85 — 0.67
<excerpt title="Cloris Leachman">
## Acting credits and awards
41.   ↑Huver, Scott (June 12, 2017). "Cloris Leachman Honored With PETA's Lifetime Achievement Award". _The Hollywood Reporter_.  
42.   ↑"Cloris Leachman". _Hollywood Walk of Fame_. October 25, 2019. Retrieved January 28, 2021.  
43.   ↑Lorna Luft, _Me and My Shadows: A Family Memoir_, Simon & Schuster, 1998  
44.   ↑Petit, Chris (December 31, 2005). "Bad old boys". _Guardian Unlimited_. London. Retrieved August 17, 2007.  
45.   ↑"Cloris Leachman's Salad Days". PETA. March 31, 2009.  
46.   ↑"Cloris Leachman Reminds You That Cats Can't Use Condoms". _TheaterMania_. February 20, 2013.  
47.   ↑"About". _Anabel Englund_. Archived from the original on April 21, 2014.  
48.   ↑Charaipotra, Sona (March 30, 2009). "America's Dirtiest Dancer". _The Daily Beast_. Retrieved December 28, 2016.  
49.   ↑Ollivier, Debra (June 20, 2012). "Cloris Leachman: 'I Don't Believe In God And I'm Very Relieved I Don't'". _Huffington Post_.  
50.   ↑"Cloris Leachman Died of a Stroke and COVID Was a Contributing Condition: Medical Examiner". People. Retrieved February 19, 2021.  
51.   12"Cloris Leachman's Cause of Death Was Stroke, COVID-19 Contributed". Entertainment Online. February 18, 2021. Retrieved February 19, 2021.  

## Acting credits and awards
52.   ↑Quinn, Dave. "Cloris Leachman, Oscar Winner and Mary Tyler Moore Show Star, Dies at 94". _People_. Retrieved January 28, 2021.  
53.   ↑Bernstein, Adam. "Cloris Leachman, Oscar-winning actress who played Frau Blücher (neighhh!) in 'Young Frankenstein,' dies at 94"– via www.washingtonpost.com.  
54.   ↑Carmel Dagan (January 27, 2021). "Cloris Leachman, Emmy and Oscar Winner, Dies at 94". _Variety_. Retrieved January 27, 2021.  
55.   ↑"Cloris Leachman, Oscar-winning actress and prolific TV star, dies at 94". _Los Angeles Times_. January 27, 2021.  
56.   ↑_Cloris: My Autobiography_. Kensington. March 2009. ISBN978-0-7582-2963-2.
</excerpt>
### Rank 4 of 85 — 0.27
<excerpt title="The Best of Cloris Leachman (1926-2021) - Blog">
# The Best of Cloris Leachman(1926-2021) - Blog - The Film Experience
## The Best of Cloris Leachman(1926-2021)
Over her very long career she won the Oscar and BAFTA (_The Last Picture Show_, 1971), the Globe (_Phyllis_, 1985), a daytime Emmy (_After School Special: The Woman Who Willed a Miracle_, 1983) and eight PrimeTime Emmys for both guest spots, series regular gigs, and telefilms (_A Brand New Life_, 1973; _Mary Tyler Moore_, 1974 and 1975; _Cher,_ 1975, _SAG 50th Anniversary Celebration_, 1984, _Promised Land,_ 1998, _Malcolm in the Middle_, 2002 and 2006).
Here are 10 personal favourite Cloris Leachman roles though I haven't seen even half of her filmography -- she worked A LOT -- but her best role may have been herself given her entertaining nature on _The Muppet Show_ and _Cher_ and other variety-ready appearances on awards shows and a dozen years back on _Dancing with the Stars_.
**"Christina Bailey" in _Kiss Me Deadly_ (1955)**Her official film debut came as a doomed hitchhiker in this classic noir.
****"Phyllis Lindstrom" on**_The Mary Tyler Moore Show_**(1970-1975) and the spin-off**_Phyllis_**(1975-1977)****This landlady role won Cloris five Emmy nominations and two wins plus a Golden Globe over the seven years she played it.
****
**"Ruth Popper" in _The Last Picture Show_ (1971)**She's sensational as a repressed housewife having a sexual affair with a high school senior. But really, every actor is sensational in this Peter Bogdanovich classic; it's one of the greatest ensemble dramas in film history.
</excerpt>
### Rank 5 of 85 — 0.27
<excerpt title="Stage and Screen Star Cloris Leachman Passes Away at 94">
# Stage and Screen Star Cloris Leachman Passes Away at 94
Eight-time Emmy winner entertained generations of audiences.
Image: Courtesy of Northwestern University Archives
February 1, 2021
People
1 Response
*   Facebook  
*   Twitter  
*   Pinterest  
*   LinkedIn
**Cloris Leachman**’48, ’14 H died at her home in Encinitas, Cali., on Jan.27 at age 94. The Academy Award, Golden Globe and Emmy-winning actress was best known for her comedic television roles in _The Mary Tyler Moore Show_, _The Facts of Life_ and _Malcolm in the Middle_.
Born and raised in Des Moines, Iowa, Leachman acted in local children’s theater starting at age 7. She enrolled in the School of Communication at Northwestern, where she studied theater and appeared in the Waa-Mu Show.
Leachman stepped away from Northwestern to enter the world of beauty pageants — she was a Miss America finalist in 1946 — and later professional acting, first on Broadway in productions of _South Pacific_ and _As You Like It_ and then on TV and in films.
Credit: Courtesy of Northwestern University Archives
Leachman won eight Primetime Emmy Awards — most prominently for her role as Phyllis Lindstrom on _The Mary Tyler Moore Show_ — and received 22 nominations.
She had roles in dozens of films, including _The Last Picture Show_, for which she won an Oscar for best supporting actress. She had several roles in Mel Brooks films, including _History of the World, Part 1_ and _Young Frankenstein_, in which she played the memorable Frau Blücher.
Leachman was inducted into the Television Academy Hall of Fame in 2011 and even at the end of her life remained active in the entertainment industry, appearing in the 2019 revival of _Mad About You_. In 2008 she made an appearance on _Dancing with the Stars_, where she finished seventh. At 82, she was the oldest contestant to ever appear on the show. Leachman had roles in several films now in postproduction and slated for release in 2021.
She was awarded an honorary degree from Northwestern in 2014.

# Stage and Screen Star Cloris Leachman Passes Away at 94
Leachman is survived by her sons, Morgan, Adam and George Englund, a daughter, Dinah Englund, and seven grandchildren.
Leachman enchants in the Waa-Mu Show at Northwestern. Credit: Courtesy of Northwestern University Archives
**Related Topics:**Arts & Entertainment
Share this Northwestern story with your friends via...
*   Facebook  
*   Twitter  
*   Pinterest  
*   LinkedIn

# Stage and Screen Star Cloris Leachman Passes Away at 94
### Reader Responses
*   I gave a Commencement speech at Northwestern in the 1980s and reminisced about roommates my wife, Jo, and I had as undergraduates in the ’40s. Jo’s roommate was Cloris Leachman [In Memoriam, spring 2021]; my roommate was Sandy Vanocur, who became NBC White House correspondent during the Kennedy administration. I told the students that Jo and I went to Northwestern decades too soon, because if we went to Northwestern now, my roommate would be Cloris Leachman. Cloris heard about it and sent me a telegram saying this was the worst insult of her life and that her roommate would have been Sandy Vanocur!   
—**Newt Minow ’49 ’50 JD, ’65 H** Chicago, via Northwestern Magazine
No one has commented on this page yet.

# Stage and Screen Star Cloris Leachman Passes Away at 94
### Submit a Response
Response
Name
City, State (Country if not U.S.)
Email (will not be published)
Degree
Northwestern School
Year of Graduation
Degree (Secondary)
Northwestern School (Secondary)
Year of Graduation (Secondary)
Security Verification
Check out these related stories...
People & Profiles
</excerpt>

## Search 9 — query: "Dom DeLuise walk of fame"
### Rank 1 of 30 — 0.52 (passed on)
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
### Rank 2 of 30 — 0.51
<excerpt title="Caught By The Reaper – Dom DeLuise">
DeLuise became known as a scene stealer, his boyish energy bringing with it something unforeseeably funny. His professionalism allowed him to play the ideal platform for ensemble scenes. Grossly scratching himself, falling from his emperor’s couch and childishly taking a ‘treasure bath’ as Nero in Mel Brooks’ History of the World – Part 1, his hammish performance actually holds the entire scene together, despite director Mel Brooks’ halting ancient stand-up routine and clumsy side plots. As the very Italian magician Dominick the Great , he was a confidently sneaky magic man, bossing both audience and volunteer, as he disguises the fact that he can’t do magic. (In fact, he could do magic perfectly well, as evidenced on this episode of The Johnny Carson Show).
Born in Brooklyn of Italian immigrant parents, DeLuise’s father was a garbage collector who never learned to speak English. (According to some sources, directing his father’s temper was one reason DeLuise learned to be funny.) After graduating from Manhattan’s High School of Performing Arts, DeLuise went on to study biology at Tufts University, with the aim of being a teacher. Showbiz beckoned and soon he was appearing on daytime TV shows like Tinker’s Workshop and the Shari Lewis Show in the late 1950s. After a Broadway debut in 1963, DeLuise’s career alternated from big screen to small. He was a natural comedian given few serious roles (1964’s Fail-Safe) but in love with drama, saying, “I’m actually a thin serious person but I play fat and funny, but only for the movies.”

DeLuise is best known to most as a stalwart of Mel Brooks in The Twelve Chairs, Blazing Saddles, Silent Movie, History of the World – Part 1 and Robin Hood: Men in Tights. DeLuise also worked with Burt Reynolds, who was a fan and a friend, in Smokey and the Bandit II, Cannonball Run and The Best Little Whorehouse in Texas. Yet DeLuise’s career spanned an enormous range of entertainment, from directing two feature films, TV production and authoring seven books for children to doing voiceovers for animated features and performing in operas. He contributed to a syndicated radio programme about home improvement. But his overwhelming love from an early age – “When I was 14 years old, I decided I could cook. It was either that or puberty” – was for cooking and food, becoming well known as a celebrity chef with cookery programmes and books.
DeLuise was a common man’s Zero Mostel – rarely sophisticated but always hilarious. His intellect focused on broad comedy, on displays of physical mirth that used his bulk, which increased with age, as a comedy implement. Popping and locking with The Jackson 5 for a snappy rendition of That’s The Way I Like It DeLuise’s physical grace belied his size. As he grew older, his weight became a health concern. Ballooning to 325 lbs (23 stone), he had to lose 100 lbs in order to safely have his hip replaced in 1993. DeLuise openly talked about his battle with weight, once quipping, “When I was a kid, if I had a fever, had a cold, had a fight, had a fall, had a cut, was depressed, had a disappointment, fell off a truck, woke up with a headache…no matter what the situation, my mother’s solution was always, ‘Eat this, it’ll make you feel better.’” His mother’s solution became the titles of two of his cookbooks.
With a well-deserved star on Hollywood’s Walk of Fame, DeLuise’s career is remarkable, but it is his unstoppable sense of joy that was his trademark.
[Dom DeLuise died in his sleep after complications of cancer. He is survived by his wife, actress Carol Arthur, and his sons, actor, writer, director Peter DeLuise, and actors David DeLuise and Michael DeLuise.]
</excerpt>
### Rank 3 of 30 — 0.50
<excerpt title="⭐ Dom DeLuise is seen showing his star on the Hollywood Walk of Fame ...">
# OldLight - ⭐ Dom DeLuise is seen showing his star on the... | Facebook
## OldLight's Post
com/hashtag/vintagephoto?__eep__=6&__cft__[0]=AZh3-tnqoqe2XUEodfD55ASb3GHjVOGJHz8RT2fRqil2cdgLbpdVW9lHXuYRWhnsw6kLWuk7eHeO1pRxKOY5MFMn9DqESTtpwv2yoelHDgjm_3qvnZjppO-hJCnvAk-qbnWtrf5dLZnRtvv9rWWvYfPyyUFPGpPN&__tn__=*NK-R)[#FilmHistory](https://www.facebook.com/hashtag/filmhistory?__eep__=6&__cft__[0]=AZh3-tnqoqe2XUEodfD55ASb3GHjVOGJHz8RT2fRqil2cdgLbpdVW9lHXuYRWhnsw6kLWuk7eHeO1pRxKOY5MFMn9DqESTtpwv2yoelHDgjm_3qvnZjppO-hJCnvAk-qbnWtrf5dLZnRtvv9rWWvYfPyyUFPGpPN&__tn__=*NK-R)[#HollywoodHistory](https://www.facebook.com/hashtag/hollywoodhistory?__eep__=6&__cft__[0]=AZh3-tnqoqe2XUEodfD55ASb3GHjVOGJHz8RT2fRqil2cdgLbpdVW9lHXuYRWhnsw6kLWuk7eHeO1pRxKOY5MFMn9DqESTtpwv2yoelHDgjm_3qvnZjppO-hJCnvAk-qbnWtrf5dLZnRtvv9rWWvYfPyyUFPGpPN&__tn__=*NK-R)[#ComedyHistory](https://www.facebook.
</excerpt>
### Rank 4 of 30 — 0.48
<excerpt title="⭐ Dom DeLuise is seen showing his star on the Hollywood Walk of Fame ...">
# OldLight - ⭐ Dom DeLuise is seen showing his star on the... | Facebook
## OldLight's Post
com/hashtag/comedyhistory?__eep__=6&__cft__[0]=AZh3-tnqoqe2XUEodfD55ASb3GHjVOGJHz8RT2fRqil2cdgLbpdVW9lHXuYRWhnsw6kLWuk7eHeO1pRxKOY5MFMn9DqESTtpwv2yoelHDgjm_3qvnZjppO-hJCnvAk-qbnWtrf5dLZnRtvv9rWWvYfPyyUFPGpPN&__tn__=*NK-R)[#OldHollywood](https://www.facebook.com/hashtag/oldhollywood?__eep__=6&__cft__[0]=AZh3-tnqoqe2XUEodfD55ASb3GHjVOGJHz8RT2fRqil2cdgLbpdVW9lHXuYRWhnsw6kLWuk7eHeO1pRxKOY5MFMn9DqESTtpwv2yoelHDgjm_3qvnZjppO-hJCnvAk-qbnWtrf5dLZnRtvv9rWWvYfPyyUFPGpPN&__tn__=*NK-R)
[](https://www.facebook.com/photo/?fbid=1380415687438464&set=a.457209216425787&__cft__[0]=AZh3-tnqoqe2XUEodfD55ASb3GHjVOGJHz8RT2fRqil2cdgLbpdVW9lHXuYRWhnsw6kLWuk7eHeO1pRxKOY5MFMn9DqESTtpwv2yoelHDgjm_3qvnZjppO-hJCnvAk-qbnWtrf5dLZnRtvv9rWWvYfPyyUFPGpPN&__tn__=EH-R)

# OldLight - ⭐ Dom DeLuise is seen showing his star on the... | Facebook
## OldLight's Post
![Image 3](blob:http://localhost/85d8b181a20aeb64a3afc2f1c39d2480)
![Image 4](blob:http://localhost/2b45e6f1a2ae097354c0b291152873d5)
All reactions:
2
Like
Comment
![Image 5](blob:http://localhost/85d8b181a20aeb64a3afc2f1c39d2480)
![Image 6](blob:http://localhost/2b45e6f1a2ae097354c0b291152873d5)
All reactions:
2
Like
Comment
</excerpt>
### Rank 5 of 30 — 0.46
<excerpt title="⭐ Dom DeLuise is seen showing his star on the Hollywood Walk of Fame ...">
# OldLight - ⭐ Dom DeLuise is seen showing his star on the... | Facebook
## OldLight's Post
[March 31](https://www.facebook.com/OldlightFB/posts/pfbid0LweL1T8x7CemGyPPEDzuaxoobgURbQGMtjqmiNwa35naHeBWyWYtJUWooY2mqg8hl?__cft__[0]=AZh3-tnqoqe2XUEodfD55ASb3GHjVOGJHz8RT2fRqil2cdgLbpdVW9lHXuYRWhnsw6kLWuk7eHeO1pRxKOY5MFMn9DqESTtpwv2yoelHDgjm_3qvnZjppO-hJCnvAk-qbnWtrf5dLZnRtvv9rWWvYfPyyUFPGpPN&__tn__=%2CO%2CP-R) ·
Dom DeLuise is seen showing his star on the Hollywood Walk of Fame, captured in a moment that reflects recognition built through years of work in film and television.
The image highlights a personal connection to a public honor, where achievement is represented in a simple, tangible form on the street.
It suggests a mix of pride and humor, consistent with a career known for warmth and expressive performance.

# OldLight - ⭐ Dom DeLuise is seen showing his star on the... | Facebook
## OldLight's Post
[#DomDeLuise](https://www.facebook.com/hashtag/domdeluise?__eep__=6&__cft__[0]=AZh3-tnqoqe2XUEodfD55ASb3GHjVOGJHz8RT2fRqil2cdgLbpdVW9lHXuYRWhnsw6kLWuk7eHeO1pRxKOY5MFMn9DqESTtpwv2yoelHDgjm_3qvnZjppO-hJCnvAk-qbnWtrf5dLZnRtvv9rWWvYfPyyUFPGpPN&__tn__=*NK-R)[#HollywoodWalkOfFame](https://www.facebook.com/hashtag/hollywoodwalkoffame?__eep__=6&__cft__[0]=AZh3-tnqoqe2XUEodfD55ASb3GHjVOGJHz8RT2fRqil2cdgLbpdVW9lHXuYRWhnsw6kLWuk7eHeO1pRxKOY5MFMn9DqESTtpwv2yoelHDgjm_3qvnZjppO-hJCnvAk-qbnWtrf5dLZnRtvv9rWWvYfPyyUFPGpPN&__tn__=*NK-R)[#ClassicHollywood](https://www.facebook.com/hashtag/classichollywood?__eep__=6&__cft__[0]=AZh3-tnqoqe2XUEodfD55ASb3GHjVOGJHz8RT2fRqil2cdgLbpdVW9lHXuYRWhnsw6kLWuk7eHeO1pRxKOY5MFMn9DqESTtpwv2yoelHDgjm_3qvnZjppO-hJCnvAk-qbnWtrf5dLZnRtvv9rWWvYfPyyUFPGpPN&__tn__=*NK-R)[#VintagePhoto](https://www.facebook.
</excerpt>

## Search 10 — query: "Milton Berle Golden Globe award winner"
### Rank 1 of 79 — 0.46 (passed on)
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
### Rank 2 of 79 — 0.41
<excerpt title="Milton Berle">
## Final role and death
*   Berle won the Emmy for Most Outstanding Kinescoped Personality in 1950, the same year his show, the _Texaco Star Theater_, won the Emmy for Best Kinescope Show.[[102]](https://en.wikipedia.org/wiki/Milton_Berle#cite_note-102) He was twice nominated for Emmys for his acting, in 1962 and 1995.[[103]](https://en.wikipedia.org/wiki/Milton_Berle#cite_note-103)[[104]](https://en.wikipedia.org/wiki/Milton_Berle#cite_note-104) In 1979, Berle was awarded a special Emmy Award, titled "Mr. Television."[[105]](https://en.wikipedia.org/wiki/Milton_Berle#cite_note-105)  
*   The Hollywood Walk of Fame, on February 8, 1960, inducted Berle with two stars, for television and radio.[[106]](https://en.wikipedia.org/wiki/Milton_Berle#cite_note-106)  
*   Berle was in the first group of inductees into the Television Hall of Fame in 1984.[[107]](https://en.wikipedia.org/wiki/Milton_Berle#cite_note-107)  
*   On December 5, 2007, California Governor Arnold Schwarzenegger and First Lady Maria Shriver inducted Berle into the California Hall of Fame, located at The California Museum for History, Women and the Arts.[[108]](https://en.wikipedia.org/wiki/Milton_Berle#cite_note-108)

## Final role and death
*   _Earl Carroll's Vanities of 1932_ (1932) – revue – in the roles of "Mortimer" in the sketch "Mourning Becomes Impossible", "Joe Miller, Jr." in "What Price Jokes", "Frank" in "Two Sailors", "Paul" in "The Cabinet of Doctor X", the "Announcer" in "Studio W.M.C.A." the "Defendant" in "Trial by Jury" and "Milton" in "The Bar Relief"  
*   _Saluta_ (1934) – musical – co-lyricist and performer cast in the role of "'Windy' Walker"  
*   _See My Lawyer_ (1939) – play – performer cast in the role of "Arthur Lee"  
*   _Ziegfeld Follies of 1943_ (1943) – revue – performer in the role of "Cecil" in _Counter Attack_, "J. Pierswift Armour" in _The Merchant of Venison_, "Perry Johnson" in _Loves-A-Poppin_, "Escamillio" in _Carmen in Zoot_, "Charlie Grant" _Mr Grant Goes To Washington_, "'The Micromaniac' Singer" and "'Hold That Smile' Dancer"  
*   _I'll Take the High Road_ (1943) – play – co-producer  
*   _Seventeen_ (1951) – musical – co-producer  
*   _The Goodbye People_ (1968) – performer cast in the role of "Max Silverman"
</excerpt>
### Rank 3 of 79 — 0.41
<excerpt title="Why didn't the show win more Emmys or Golden Globes?">
# Why didn't the show win more Emmys or Golden Globes? : r/BeverlyHills90210
Skip to main contentWhy didn't the show win more Emmys or Golden Globes? : r/BeverlyHills90210
Open menu Open navigationGo to Reddit Home
r/BeverlyHills90210
Sign UpSign up for RedditLog InLog in to Reddit
Expand user menu Open settings menu
Go to BeverlyHills90210
r/BeverlyHills90210•4y ago
u/nuraman00

# Why didn't the show win more Emmys or Golden Globes?
Between the actors, writers, directors, music, producers, the only Emmy it was nominated for was a guest role, with Milton Berle.
https://en.wikipedia.org/wiki/Beverly_Hills,_90210#Awards_and_nominations
It only had 1 Emmy nomination, and 4 Golden Globe nominations. It couldn't get any more nominations, or awards, for the Emmys or Golden Globes?
Read more
Share
airbnb•Ad
호스팅, 참 좋죠. 근데 혼자 다 하려니 막막하신가요? 다행히 공동 호스트가 도와드릴 수 있어요.
Sign Up
airbnb.co.kr
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
kminogues
•4y ago
I love the show, but it is not Emmy worthy, in my opinion. I mean, let’s be honest.
Reply  Share
nuraman00
•4y ago
Here's what won an Emmy from 1991-2000. I haven't seen these shows.
https://en.wikipedia.org/wiki/Primetime_Emmy_Award_for_Outstanding_Drama_Series#1990s
L.A. Law;
Northern Exposure;
Picket Fences;
Picket Fences;
NYPD Blue,
E.R.;
Law & Order;
The Practice;
The Practice;
The West Wing.
It didn't even get a nomination.
Here's what won a Golden Globe:
https://en.wikipedia.org/wiki/Golden_Globe_Award_for_Best_Television_Series_%E2%80%93_Drama
Northern Exposure,
Northern Exposure,
NYPD Blue,
The X-Files
Party Of Five
The X-Files
The X-Files
The Practice
The Sopranos
The West Wing
It did receive a nomination in 1991, 1992. That is more acceptable.
Reply  Share
kminogues
•4y ago
Shows like NYPD Blue, ER and The Practice are in a completely different realm than 90210, so I can see why they were nominated repeatedly. And I mean, comparing their level and degree of writing and acting and directing to 90210 is like comparing caviar to a breakfast cereal. That’s not to say that I particularly like those shows, but they’re definitely in another league. I mean, the whole episode of the guy in the freezer the gang thinks is dead? Or the cheesy stuff like Colin’s blind dad coming to town or David’s ridiculous orange juice meth storyline? Emmy worthy?
I feel shows like 90210 is why the Teen Choice Awards were created. So they could properly be recognized.
Reply  Share
8 more replies
8 more replies
8 more replies
rachel_ct
•4y ago
</excerpt>
### Rank 4 of 79 — 0.36
<excerpt title="Milton Berle">
### Life after _The Milton Berle Show_
On April 14, 1979, Berle guest-hosted NBC's _Saturday Night Live_. Berle's long-standing reputation for taking control of an entire television production—whether invited to do so or not—was a cause of stress on the set. He appeared skeptical about the show's satirical bent. One of the show's writers, Rosie Shuster, described the rehearsals for the Berle _SNL_ show and the telecast as "watching a comedy train accident in slow motion on a loop." Upstaging, camera mugging, doing spit-takes, inserting old comedy bits, and climaxing the show with a maudlin performance of "September Song" complete with a pre-arranged standing ovation, something producer Lorne Michaels had never sanctioned, resulted in Berle being banned from hosting the show again. The episode was barred from being rerun until surfacing in 2003 because Michaels thought it brought down the show's reputation.[[51]](https://en.wikipedia.org/wiki/Milton_Berle#cite_note-51)[[52]](https://en.wikipedia.org/wiki/Milton_Berle#cite_note-52)
As a guest star on _The Muppet Show_,[[53]](https://en.wikipedia.org/wiki/Milton_Berle#cite_note-53) Berle was upstaged by the heckling theater critics Statler and Waldorf.[[54]](https://en.wikipedia.org/wiki/Milton_Berle#cite_note-54)
The Statler and Waldorf puppets were reportedly inspired by a recurring character named Sidney Spritzer, portrayed by comedian Irving Benson, who regularly heckled Berle from a theater box seat during episodes of The Milton Berle Show in the 1960s.[[55]](https://en.wikipedia.org/wiki/Milton_Berle#cite_note-Smith2011-55) Berle later made a cameo appearance in _The Muppet Movie_ (1979), playing a used car salesman who trades Fozzie Bear’s 1951 Studebaker for a station wagon.[[56]](https://en.wikipedia.org/wiki/Milton_Berle#cite_note-IMDbMuppetMovie-56)
</excerpt>
### Rank 5 of 79 — 0.35
<excerpt title="Make Room For Granddaddy - Golden Globes">
# Make Room For Granddaddy - Golden Globes
*     
*     
*     
*     
*   

*   The Show  
    *   Awards Database  
    *   2026 Nominations  
    *   Winners/Nominees  
    *   Carol Burnett Award  
    *   Cecil B. DeMille Award  
    *   LIVE Coverage  
        *   LIVE Coverage 2024  
        *   LIVE Coverage 2025  
        *   LIVE Coverage 2026

*   News  
    *   Latest News  
    *   Video Gallery  
    *   Photo Gallery

*   History  
    *   Golden Globes History

*   About  
    *   Award Rules and Entry Forms  
    *   Media Info  
    *   Publicist Info  
    *   Publicist Application  
    *   Voter Application  
    *   Voter Info  
    *   Golden Globes Leadership Team  
    *   Contact Us  
    *   FAQs
Skip to content
The 83rd Annual Golden Globes® Now Streaming On Demand
Awards Database
1 Nomination
0 Wins

# Make Room For Granddaddy
In a sequel to The Danny Thomas Show, cast members were reunited for more domestic predicaments. It showcased the appearances of such high-powered guests as Bob Hope, Lucille Ball, Frank Sinatra and Milton Berle.
* * *
| Role | Credit |  
| --- | --- |  
| **Cast:** | Danny Thomas , Frank Sinatra , Lucille Ball , Diana Ross , Sammy Davis Jr. , Bob Hope |

# Make Room For Granddaddy
## Golden Globe Awards
*     1971 Nominee   Best Performance by an Actor in a Television Series - Musical or Comedy    
    *   Make Room For Granddaddy  
    *   Danny Thomas
</excerpt>

# Example 5
## Question
Of the five countries with the highest per capita death toll from COVID-19 (cumulative as of 2023, according to Johns Hopkins), which have a trade deficit of less than 10 billion dollars (according to most recent 2022 numbers from WITS, not including services), have population of less than 20 million (according to most recent 2023 numbers from Macrotrends), and for each of these countries: which years between 2004 and 2022 do they have less than or equal to -3 for the GDP growth (according to WITS)?

## Expected answer
Hungary: 2009, 2020, Bulgaria: 2009, 2020, Bosnia and Herzegovina: 2009, 2020, North Macedonia: 2020

## Grade 0.00

## Search 1 — query: "Johns Hopkins cumulative COVID-19 deaths per capita 2023 top countries per capita death toll"
### Rank 1 of 45 — 0.23 (passed on)
<excerpt title="COVID-19 deaths per capita by country">
# Coronavirus (COVID-19) deaths worldwide per one million population as of July 13, 2022, by country
## Where are these numbers coming from?
The numbers shown here were collected by Johns Hopkins University, a source that manually checks the data with domestic health authorities. For the majority of countries, this is from national authorities. In some cases, like China, the United States, Canada or Australia, city reports or other various state authorities were consulted. In this statistic, these separately reported numbers were put together. For more information or other freely accessible content, please visit our dedicated Facts and Figures page.
* * *
REPORT_DATA_PROBLEMREPORT_PROBLEM_LINK_TEXTORCOPYRIGHT_INFRINGEMENT_LINK_TEXT

# Coronavirus (COVID-19) deaths worldwide per one million population as of July 13, 2022, by country
## Related insights
Statistics Insights
1.   Coronavirus (COVID-19) death rate in countries with confirmed deaths and over 1,000 reported cases as of April 26, 2022, by country Worldwide    
2.   Number of people deceased as a result of the coronavirus worldwide as of June 12, 2022, by continent Worldwide    
3.   COVID-19 Deaths Per 100,000 Inhabitants: A Comparison     
4.   Cumulative number of coronavirus (COVID-19) deaths in France, Germany, Italy, Spain and the United Kingdom (as of July 7, 2022) FRA +4    
5.   Number and change of coronavirus (COVID-19) cases and deaths among the most impacted countries worldwide as of November 14, 2022 Worldwide    
6.   The Countries With the Highest COVID-19 Death Toll     
7.   The Countries Currently Worst Hit By COVID-19 Deaths     
8.   Average number of deaths from COVID-19 over the last seven days in select countries worldwide from March 1 to October 27, 2020 Worldwide    
9.   Covid-19: Countries in Europe with the most deaths     
10.   Weekly number of confirmed cases and deaths caused by coronavirus (COVID-19) in Peru between May 2020 and July 2022 PER    
11.   Number of novel coronavirus COVID-19 infection, death and recovery cases in Greater China as of June 7, 2022, by region CHN +3    
12.   COVID-19 Cases per Million Inhabitants: A Comparison     
13.   Where COVID Tallies Are Highest Relative to Population     
14.   How Excess Mortality Compares     
15.   World Reaches Five Million COVID-19 Deaths     
16.   Number of coronavirus (COVID-19) deaths in the African continent as of November 18, 2022, by country Africa
</excerpt>
### Rank 2 of 45 — 0.23
<excerpt title="COVID-19 deaths per capita by country">
# Coronavirus (COVID-19) deaths worldwide per one million population as of July 13, 2022, by country
## The difficulties of death figures
This table aims to provide a complete picture on the topic, but it very much relies on data that has become more difficult to compare. As the coronavirus pandemic developed across the world, countries already used different methods to count fatalities, and they sometimes changed them during the course of the pandemic. On April 16, for example, the Chinese city of Wuhan added a 50 percent increase in their death figures to account for community deaths. These deaths occurred outside of hospitals and went unaccounted for so far. The state of New York did something similar two days before, revising their figures with 3,700 new deaths as they started to include “assumed” coronavirus victims. The United Kingdom started counting deaths in care homes and private households on April 29, adjusting their number with about 5,000 new deaths (which were corrected lowered again by the same amount on August 18). This makes an already difficult comparison even more difficult. Belgium, for example, counts suspected coronavirus deaths in their figures, whereas other countries have not done that (yet). This means two things. First, it could have a big impact on both current as well as future figures. On April 16 already, UK health experts stated that if their numbers were corrected for community deaths like in Wuhan, the UK number would change from 205 to “above 300”. This is exactly what happened two weeks later. Second, it is difficult to pinpoint exactly which countries already have “revised” numbers (like Belgium, Wuhan or New York) and which ones do not. One work-around could be to look at (freely accessible) timelines that track the reported daily increase of deaths in certain countries. Several of these are available on our platform, such as for Belgium, Italy and Sweden. A sudden large increase might be an indicator that the domestic sources changed their methodology.

# Coronavirus (COVID-19) deaths worldwide per one million population as of July 13, 2022, by country
## Where are these numbers coming from?
The numbers shown here were collected by Johns Hopkins University, a source that manually checks the data with domestic health authorities. For the majority of countries, this is from national authorities. In some cases, like China, the United States, Canada or Australia, city reports or other various state authorities were consulted. In this statistic, these separately reported numbers were put together. For more information or other freely accessible content, please visit our dedicated Facts and Figures page.
* * *
REPORT_DATA_PROBLEMREPORT_PROBLEM_LINK_TEXTORCOPYRIGHT_INFRINGEMENT_LINK_TEXT
</excerpt>
### Rank 3 of 45 — 0.20
<excerpt title="COVID-19 deaths per capita by country">
# Coronavirus (COVID-19) deaths worldwide per one million population as of July 13, 2022, by country
## Related insights
Statistics Insights
1.   Coronavirus (COVID-19) death rate in countries with confirmed deaths and over 1,000 reported cases as of April 26, 2022, by country Worldwide    
2.   Number of people deceased as a result of the coronavirus worldwide as of June 12, 2022, by continent Worldwide    
3.   COVID-19 Deaths Per 100,000 Inhabitants: A Comparison     
4.   Cumulative number of coronavirus (COVID-19) deaths in France, Germany, Italy, Spain and the United Kingdom (as of July 7, 2022) FRA +4    
5.   Number and change of coronavirus (COVID-19) cases and deaths among the most impacted countries worldwide as of November 14, 2022 Worldwide    
6.   The Countries With the Highest COVID-19 Death Toll     
7.   The Countries Currently Worst Hit By COVID-19 Deaths     
8.   Average number of deaths from COVID-19 over the last seven days in select countries worldwide from March 1 to October 27, 2020 Worldwide    
9.   Covid-19: Countries in Europe with the most deaths     
10.   Weekly number of confirmed cases and deaths caused by coronavirus (COVID-19) in Peru between May 2020 and July 2022 PER    
11.   Number of novel coronavirus COVID-19 infection, death and recovery cases in Greater China as of June 7, 2022, by region CHN +3    
12.   COVID-19 Cases per Million Inhabitants: A Comparison     
13.   Where COVID Tallies Are Highest Relative to Population     
14.   How Excess Mortality Compares     
15.   World Reaches Five Million COVID-19 Deaths     
16.   Number of coronavirus (COVID-19) deaths in the African continent as of November 18, 2022, by country Africa
</excerpt>
### Rank 4 of 45 — 0.19
<excerpt title="Cumulative Cases - Johns Hopkins Coronavirus Resource Center">
## Cumulative Cases By Days Since 50th Confirmed Case
Charting the outbreak day by day in each country allows us to see the succession of events as a global story. Because the epidemic began at different times in different countries, viewing each country’s curve from the same starting point can allow us to more easily compare countries. The starting point for this chart is the day on which the 50th case was confirmed in each country, with the trend lines following the number of days since that event. As with the graph above, use the dropdown menus to visualize confirmed cases or deaths (totals or per 100,000 population), and linear or logarithmic scale.

## Cumulative Cases By Date
For the twenty countries with the highest absolute daily number of deaths, the lines below show the cumulative number of cases or deaths reported in that country at each date in time. Use the two dropdown menus to see either confirmed cases or deaths (absolute numbers or per 100,000 population), and linear or logarithmic scales. Increases in deaths may happen two or more weeks after the corresponding increase in cases, but the number of deaths may be more reliable than confirmed cases because deaths are more likely to be accurately reported. The logarithmic scale helps visualize early exponential growth.

## Cumulative Cases By Date
### US
Yesterday's data (9/14/2022)
New Cases:46,931
Deaths:590
The first case of COVID-19 in US was reported 1142 days ago on 1/22/2020. Yesterday, the country reported 46,931 new confirmed cases and 590 deaths.

## Cumulative Cases By Date
### Russia
Yesterday's data (9/14/2022)
New Cases:12,385
Deaths:38
The first case of COVID-19 in Russia was reported 1133 days ago on 1/31/2020. Yesterday, the country reported 12,385 new confirmed cases and 38 deaths.

## Cumulative Cases By Date
### Korea, South
Yesterday's data (9/14/2022)
New Cases:10,335
Deaths:12
The first case of COVID-19 in Korea, South was reported 1142 days ago on 1/22/2020. Yesterday, the country reported 10,335 new confirmed cases and 12 deaths.

## Cumulative Cases By Date
### Japan
Yesterday's data (9/14/2022)
New Cases:9,834
Deaths:80
The first case of COVID-19 in Japan was reported 1142 days ago on 1/22/2020. Yesterday, the country reported 9,834 new confirmed cases and 80 deaths.

## Cumulative Cases By Date
### Germany
Yesterday's data (9/14/2022)
New Cases:7,829
Deaths:127
The first case of COVID-19 in Germany was reported 1137 days ago on 1/27/2020. Yesterday, the country reported 7,829 new confirmed cases and 127 deaths.

## Cumulative Cases By Date
### Austria
Yesterday's data (9/14/2022)
New Cases:5,283
Deaths:21
The first case of COVID-19 in Austria was reported 1108 days ago on 2/25/2020. Yesterday, the country reported 5,283 new confirmed cases and 21 deaths.

## Cumulative Cases By Date
### France
Yesterday's data (9/14/2022)
New Cases:6,308
Deaths:11
The first case of COVID-19 in France was reported 1140 days ago on 1/24/2020. Yesterday, the country reported 6,308 new confirmed cases and 11 deaths.
</excerpt>
### Rank 5 of 45 — 0.17
<excerpt title="COVID-19 deaths per capita by country">
# Coronavirus (COVID-19) deaths worldwide per one million population as of July 13, 2022, by country
## Related insights
17.   Number of deaths due to the novel coronavirus (COVID-19) in Latin America and the Caribbean as of May 11, 2025, by country Latin America and the Caribbean    
18.   Distribution of deaths due to the coronavirus (COVID-19) in Belgium as of March 23, 2022, by region BEL    
19.   Number of novel coronavirus COVID-19 cumulative confirmed and death cases in China from January 20, 2020 to June 6, 2022 CHN    
20.   U.S. COVID-19 Deaths Could Be Far Higher Than Reported     
21.   Coronavirus (COVID-19) disease pandemic- Statistics & Facts Worldwide    
22.   The Varying Impact of the Coronavirus     
23.   Share of confirmed coronavirus cases and deaths in Belgium by gender, as of March 23, 2022 BEL    
24.   Number of novel coronavirus (COVID-19) deaths worldwide as of May 2, 2023, by country and territory Worldwide    
25.   Cases and deaths of coronavirus (COVID-19) in the top 20 economic powers worldwide as of July 23, 2021 Worldwide    
26.   The Countries With The Most COVID-19 Cases     
27.   Mean number of excess deaths associated with COVID-19 from all-causes in 2020 and 2021 in select countries worldwide (per 100,000 population) Worldwide    
28.   Number of people who died due to coronavirus (COVID-19) worldwide as of August 18, 2023, by country Worldwide    
29.   Number of COVID-19 deaths in Belgium by age, as of March 23, 2022 BEL    
30.   Rate of COVID-19 cases in the most impacted countries worldwide as of December 22, 2022* (per million population) Worldwide    
31.   How Big Is China's Covid Wave Really?
</excerpt>

## Search 2 — query: "top 5 countries per capita COVID deaths cumulative 2023 Johns Hopkins""
### Rank 1 of 125 — 0.75 (passed on)
<excerpt title="COVID-19 pandemic by country and territory">
Venezuela	207	5,856	552,810  
	Mauritania	204	997	63,891  
	Zambia	202	4,078	349,892  
	Afghanistan	197	7,998	235,214  
	Comoros	193	161	9,109  
	Kiribati	183	24	5,085  
	Cambodia	177	3,056	139,326  
	Bangladesh	174	29,531	2,052,280  
	Macau	174	121	3,514  
	Djibouti	166	189	15,690  
	Algeria	151	6,881	272,440  
	Kyrgyzstan	147	1,024	88,953  
	Samoa	144	31	17,057  
	Gambia	141	372	12,627  
	Syria	140	3,163	57,423  
	Cook Islands	135	2	7,375  
	Malawi	130	2,686	89,168  
	Gabon	126	307	49,069  
	Pakistan	125	30,656	1,580,631  
	Tonga	123	13	16,992  
	Senegal	111	1,972	89,440  
	Rwanda	107	1,468	133,274  
	Kenya	104	5,689	344,162  
	Sudan	102	5,046	63,993  
	Equatorial Guinea	101	183	17,130
</excerpt>
### Rank 2 of 125 — 0.75
<excerpt title="COVID-19 pandemic by country and territory">
Libya	5,710	6,017	6,261  
	China	5,699	5,700	6,233  
	Kenya	5,376	5,583	5,639  
	Venezuela	5,324	5,440	5,633  
	Palestine	4,934	5,104	5,513  
	Zimbabwe	4,997	5,338	5,395  
	Latvia	4,570	4,873	5,224  
	Australia	2,239	3,758	5,171  
	Denmark	3,266	3,755	4,612  
	Dominican Republic	4,247	4,307	4,368  
	Oman	4,116	4,146	4,244  
	Puerto Rico	3,305	3,855	4,110  
	El Salvador	3,824	3,899	4,071  
	Namibia	3,616	3,967	4,009  
	Zambia	3,730	3,917	3,952  
	Sudan	3,337	3,533	3,909  
	Trinidad and Tobago	2,850	3,404	3,628  
	Uganda	3,294	3,538	3,588  
	Albania	3,217	3,346	3,469  
	Nigeria	3,031	3,136	3,142  
	Kosovo	2,980	3,005	3,104  
	Syria	2,897	2,989	3,075  
	Cambodia	3,012	3,015	3,032
</excerpt>
### Rank 3 of 125 — 0.72
<excerpt title="COVID-19 pandemic by country and territory">
Updated November 5, 2026.  
COVID-19 cases, deaths, and rates by location[22]  
	Country	Deaths / million	Deaths	Cases  
	World[a]	894	7,117,473	779,452,126  
	Peru	6,604	221,073	4,533,878  
	Bulgaria	5,681	38,778	1,341,082  
	North Macedonia	5,429	9,991	352,093  
	Bosnia and Herzegovina	5,123	16,419	404,289  
	Hungary	5,072	49,124	2,240,998  
	Croatia	4,813	18,806	1,371,707  
	Slovenia	4,686	9,914	1,367,017  
	Georgia	4,519	17,151	1,864,337  
	Montenegro	4,317	2,654	251,280  
	Czech Republic	4,122	43,995	4,887,735  
	Latvia	4,116	7,743	977,810  
	Moldova	4,042	12,290	656,473  
	Slovakia	3,910	21,401	1,890,156  
	Greece	3,866	40,256	5,874,300  
	San Marino	3,693	126	25,292  
	United States	3,631	1,240,149	103,436,829
</excerpt>
### Rank 4 of 125 — 0.70
<excerpt title="COVID-19 pandemic by country and territory">
Iran	1,640	146,837	7,627,863  
	Switzerland	1,611	14,170	4,492,849  
	Guyana	1,596	1,312	75,880  
	Collectivity of Saint Martin	1,591	46	12,324  
	Antigua and Barbuda	1,572	146	9,106  
	Jersey	1,555	161	66,391  
	Luxembourg	1,530	1,000	402,360  
	United States Virgin Islands	1,525	132	25,389  
	Cyprus	1,450	1,364	719,150  
	Caribbean Netherlands	1,430	41	11,922  
	Canada	1,424	55,282	4,819,055  
	Namibia	1,422	4,110	172,557  
	Israel	1,395	12,707	4,841,841  
	French Guiana	1,384	413	98,041  
	Isle of Man	1,378	116	38,008  
	Seychelles	1,370	172	51,899  
	Netherlands	1,283	22,986	8,658,086  
	Jamaica	1,279	3,634	157,710  
	Albania	1,275	3,608	337,234  
	Jordan	1,254	14,122	1,746,997  
	Saint Vincent and the Grenadines	1,214	124	9,674
</excerpt>
### Rank 5 of 125 — 0.67
<excerpt title="COVID-19 pandemic by country and territory">
Switzerland	11,921	12,372	12,683  
	Nepal	11,594	11,752	11,938  
	Moldova	10,275	10,666	11,228  
	Honduras	10,434	10,504	10,775  
	Israel	8,258	8,990	10,234  
	Lebanon	9,119	9,606	10,091  
	Azerbaijan	8,358	8,734	9,417  
	North Macedonia	7,976	8,439	9,025  
	Saudi Arabia	8,877	8,940	8,998  
	Cuba	8,322	8,399	8,494  
	Armenia	7,975	8,056	8,478  
	Lithuania	7,404	7,891	8,431  
	South Korea	5,625	6,772	8,170  
	Panama	7,427	7,716	8,079  
	Costa Rica	7,357	7,555	8,031  
	Afghanistan	7,356	7,414	7,598  
	Ethiopia	6,926	7,337	7,462  
	Slovenia	6,124	6,457	7,049  
	Uruguay	6,169	6,459	6,977  
	Algeria	6,271	6,579	6,835  
	Ireland	6,070	6,346	6,497  
	Belarus	5,578	6,052	6,480
</excerpt>

## Search 3 — query: "COVID-19 cumulative deaths per capita top countries 2023 Johns Hopkins"
### Rank 1 of 50 — 0.63 (passed on)
<excerpt title="Mortality Analyses - Johns Hopkins Coronavirus Resource Center">
## Cases and mortality by country
| Zimbabwe | 264,276 | 5,671 | 2.1% | 38.16 |  
| Burma | 633,950 | 19,490 | 3.1% | 35.82 |  
| Sao Tome and Principe | 6,281 | 77 | 1.2% | 35.13 |  
| Lesotho | 34,790 | 723 | 2.1% | 33.75 |  
| Singapore | 2,235,294 | 1,722 | 0.1% | 29.43 |  
| Marshall Islands | 15,649 | 17 | 0.1% | 29.10 |  
| Saudi Arabia | 830,127 | 9,618 | 1.2% | 27.63 |  
| Egypt | 515,759 | 24,812 | 4.8% | 24.25 |  
| Qatar | 495,090 | 688 | 0.1% | 23.88 |  
| United Arab Emirates | 1,053,213 | 2,349 | 0.2% | 23.75 |  
| Solomon Islands | 24,575 | 153 | 0.6% | 23.44 |  
| Zambia | 343,135 | 4,057 | 1.2% | 22.07 |  
| Mauritania | 63,668 | 997 | 1.6% | 21.44 |  
| Venezuela | 552,162 | 5,854 | 1.1% | 20.59 |  
| Afghanistan | 209,451 | 7,896 | 3.8% | 20.28 |
</excerpt>
### Rank 2 of 50 — 0.62
<excerpt title="Mortality Analyses - Johns Hopkins Coronavirus Resource Center">
## Cases and mortality by country
| Belgium | 4,739,365 | 33,814 | 0.7% | 294.22 |  
| Argentina | 10,044,957 | 130,472 | 1.3% | 288.68 |  
| Colombia | 6,359,093 | 142,339 | 2.2% | 279.74 |  
| Paraguay | 808,401 | 19,878 | 2.5% | 278.69 |  
| Ukraine | 5,711,929 | 119,283 | 2.1% | 272.75 |  
| Russia | 22,075,858 | 388,478 | 1.8% | 266.20 |  
| Mexico | 7,483,444 | 333,188 | 4.5% | 260.73 |  
| Portugal | 5,570,473 | 26,266 | 0.5% | 257.59 |  
| Spain | 13,770,429 | 119,479 | 0.9% | 255.54 |  
| France | 39,866,718 | 166,176 | 0.4% | 254.68 |  
| Tunisia | 1,151,126 | 29,341 | 2.5% | 248.26 |  
| Austria | 5,961,143 | 21,970 | 0.4% | 243.94 |  
| Suriname | 82,467 | 1,404 | 1.7% | 239.33 |
</excerpt>
### Rank 3 of 50 — 0.60
<excerpt title="Mortality Analyses - Johns Hopkins Coronavirus Resource Center">
## Cases and mortality by country
| Sweden | 2,699,339 | 23,777 | 0.9% | 235.43 |  
| Liechtenstein | 21,432 | 89 | 0.4% | 233.37 |  
| Saint Lucia | 30,004 | 409 | 1.4% | 222.73 |  
| Estonia | 615,433 | 2,946 | 0.5% | 222.08 |  
| Uruguay | 1,034,303 | 7,617 | 0.7% | 219.27 |  
| Andorra | 47,890 | 165 | 0.3% | 213.55 |  
| Bahamas | 37,491 | 833 | 2.2% | 211.83 |  
| Grenada | 19,680 | 238 | 1.2% | 211.52 |  
| Serbia | 2,500,142 | 17,881 | 0.7% | 204.65 |  
| Ecuador | 1,057,121 | 36,014 | 3.4% | 204.13 |  
| Germany | 38,249,060 | 168,935 | 0.4% | 203.16 |  
| Barbados | 106,798 | 579 | 0.5% | 201.48 |  
| Panama | 1,031,731 | 8,609 | 0.8% | 199.52 |  
| Luxembourg | 317,367 | 1,220 | 0.4% | 194.90 |
</excerpt>
### Rank 4 of 50 — 0.59
<excerpt title="Mortality Analyses - Johns Hopkins Coronavirus Resource Center">
## Cases and mortality by country
| Bolivia | 1,194,277 | 22,365 | 1.9% | 191.60 |  
| Malta | 117,610 | 828 | 0.7% | 187.53 |  
| Costa Rica | 1,209,725 | 9,245 | 0.8% | 181.48 |  
| Kosovo | 273,312 | 3,211 | 1.2% | 177.37 |  
| Ireland | 1,704,502 | 8,708 | 0.5% | 176.35 |  
| Seychelles | 50,665 | 172 | 0.3% | 174.90 |  
| Belize | 70,757 | 688 | 1.0% | 173.03 |  
| South Africa | 4,067,067 | 102,595 | 2.5% | 172.98 |  
| Iran | 7,572,311 | 144,933 | 1.9% | 172.55 |  
| Monaco | 16,121 | 67 | 0.4% | 170.73 |  
| Guyana | 73,075 | 1,298 | 1.8% | 165.02 |  
| Switzerland | 4,413,911 | 14,210 | 0.3% | 164.19 |  
| Finland | 1,463,644 | 8,967 | 0.6% | 161.84 |  
| Namibia | 171,156 | 4,090 | 2.4% | 160.97 |
</excerpt>
### Rank 5 of 50 — 0.59
<excerpt title="Mortality Analyses - Johns Hopkins Coronavirus Resource Center">
## Cases and mortality by country
| Guatemala | 1,238,247 | 20,182 | 1.6% | 112.65 |  
| Honduras | 472,250 | 11,111 | 2.4% | 112.18 |  
| West Bank and Gaza | 703,228 | 5,708 | 0.8% | 111.89 |  
| Saint Vincent and the Grenadines | 9,589 | 123 | 1.3% | 110.86 |  
| Cyprus | 650,685 | 1,330 | 0.2% | 110.16 |  
| Dominica | 15,760 | 74 | 0.5% | 102.79 |  
| Kazakhstan | 1,498,668 | 19,071 | 1.3% | 101.57 |  
| Azerbaijan | 828,825 | 10,138 | 1.2% | 99.99 |  
| Fiji | 68,898 | 883 | 1.3% | 98.50 |  
| Norway | 1,479,506 | 5,213 | 0.4% | 96.16 |  
| Libya | 507,187 | 6,437 | 1.3% | 93.68 |  
| Bahrain | 710,693 | 1,553 | 0.2% | 91.27 |  
| Oman | 399,449 | 4,628 | 1.2% | 90.63 |  
| Saint Kitts and Nevis | 6,597 | 47 | 0.7% | 88.36 |
</excerpt>

## Search 4 — query: "top 5 countries per capita covid deaths Johns Hopkins 2023"
### Rank 1 of 114 — 0.73 (passed on)
<excerpt title="COVID-19 pandemic by country and territory">
Venezuela	207	5,856	552,810  
	Mauritania	204	997	63,891  
	Zambia	202	4,078	349,892  
	Afghanistan	197	7,998	235,214  
	Comoros	193	161	9,109  
	Kiribati	183	24	5,085  
	Cambodia	177	3,056	139,326  
	Bangladesh	174	29,531	2,052,280  
	Macau	174	121	3,514  
	Djibouti	166	189	15,690  
	Algeria	151	6,881	272,440  
	Kyrgyzstan	147	1,024	88,953  
	Samoa	144	31	17,057  
	Gambia	141	372	12,627  
	Syria	140	3,163	57,423  
	Cook Islands	135	2	7,375  
	Malawi	130	2,686	89,168  
	Gabon	126	307	49,069  
	Pakistan	125	30,656	1,580,631  
	Tonga	123	13	16,992  
	Senegal	111	1,972	89,440  
	Rwanda	107	1,468	133,274  
	Kenya	104	5,689	344,162  
	Sudan	102	5,046	63,993  
	Equatorial Guinea	101	183	17,130
</excerpt>
### Rank 2 of 114 — 0.73
<excerpt title="COVID-19 pandemic by country and territory">
Libya	5,710	6,017	6,261  
	China	5,699	5,700	6,233  
	Kenya	5,376	5,583	5,639  
	Venezuela	5,324	5,440	5,633  
	Palestine	4,934	5,104	5,513  
	Zimbabwe	4,997	5,338	5,395  
	Latvia	4,570	4,873	5,224  
	Australia	2,239	3,758	5,171  
	Denmark	3,266	3,755	4,612  
	Dominican Republic	4,247	4,307	4,368  
	Oman	4,116	4,146	4,244  
	Puerto Rico	3,305	3,855	4,110  
	El Salvador	3,824	3,899	4,071  
	Namibia	3,616	3,967	4,009  
	Zambia	3,730	3,917	3,952  
	Sudan	3,337	3,533	3,909  
	Trinidad and Tobago	2,850	3,404	3,628  
	Uganda	3,294	3,538	3,588  
	Albania	3,217	3,346	3,469  
	Nigeria	3,031	3,136	3,142  
	Kosovo	2,980	3,005	3,104  
	Syria	2,897	2,989	3,075  
	Cambodia	3,012	3,015	3,032
</excerpt>
### Rank 3 of 114 — 0.70
<excerpt title="COVID-19 pandemic by country and territory">
Updated November 5, 2026.  
COVID-19 cases, deaths, and rates by location[22]  
	Country	Deaths / million	Deaths	Cases  
	World[a]	894	7,117,473	779,452,126  
	Peru	6,604	221,073	4,533,878  
	Bulgaria	5,681	38,778	1,341,082  
	North Macedonia	5,429	9,991	352,093  
	Bosnia and Herzegovina	5,123	16,419	404,289  
	Hungary	5,072	49,124	2,240,998  
	Croatia	4,813	18,806	1,371,707  
	Slovenia	4,686	9,914	1,367,017  
	Georgia	4,519	17,151	1,864,337  
	Montenegro	4,317	2,654	251,280  
	Czech Republic	4,122	43,995	4,887,735  
	Latvia	4,116	7,743	977,810  
	Moldova	4,042	12,290	656,473  
	Slovakia	3,910	21,401	1,890,156  
	Greece	3,866	40,256	5,874,300  
	San Marino	3,693	126	25,292  
	United States	3,631	1,240,149	103,436,829
</excerpt>
### Rank 4 of 114 — 0.69
<excerpt title="COVID-19 pandemic by country and territory">
Iran	1,640	146,837	7,627,863  
	Switzerland	1,611	14,170	4,492,849  
	Guyana	1,596	1,312	75,880  
	Collectivity of Saint Martin	1,591	46	12,324  
	Antigua and Barbuda	1,572	146	9,106  
	Jersey	1,555	161	66,391  
	Luxembourg	1,530	1,000	402,360  
	United States Virgin Islands	1,525	132	25,389  
	Cyprus	1,450	1,364	719,150  
	Caribbean Netherlands	1,430	41	11,922  
	Canada	1,424	55,282	4,819,055  
	Namibia	1,422	4,110	172,557  
	Israel	1,395	12,707	4,841,841  
	French Guiana	1,384	413	98,041  
	Isle of Man	1,378	116	38,008  
	Seychelles	1,370	172	51,899  
	Netherlands	1,283	22,986	8,658,086  
	Jamaica	1,279	3,634	157,710  
	Albania	1,275	3,608	337,234  
	Jordan	1,254	14,122	1,746,997  
	Saint Vincent and the Grenadines	1,214	124	9,674
</excerpt>
### Rank 5 of 114 — 0.67
<excerpt title="Mortality Analyses - Johns Hopkins Coronavirus Resource Center">
## Cases and mortality by country
| Country | Confirmed | Deaths | Case-Fatality | Deaths/100K pop. |  
| --- | --- | --- | --- | --- |  
| Peru | 4,487,553 | 219,539 | 4.9% | 665.84 |  
| Bulgaria | 1,297,523 | 38,228 | 2.9% | 550.17 |  
| Hungary | 2,196,804 | 48,762 | 2.2% | 504.76 |  
| Bosnia and Herzegovina | 401,729 | 16,280 | 4.1% | 496.22 |  
| North Macedonia | 346,852 | 9,662 | 2.8% | 463.77 |  
| Montenegro | 288,808 | 2,808 | 1.0% | 447.09 |  
| Croatia | 1,269,326 | 17,987 | 1.4% | 438.14 |  
| Georgia | 1,827,537 | 16,971 | 0.9% | 425.43 |  
| Czechia | 4,618,256 | 42,491 | 0.9% | 396.78 |  
| Slovakia | 2,667,551 | 21,035 | 0.8% | 387.05 |  
| San Marino | 23,616 | 122 | 0.5% | 359.48 |  
| Lithuania | 1,307,448 | 9,596 | 0.7% | 352.50 |
</excerpt>

## Search 5 — query: "per capita covid deaths top countries list Johns Hopkins July 2022 per 100,000"
### Rank 1 of 86 — 0.69 (passed on)
<excerpt title="COVID-19 deaths per capita by country">
# Coronavirus (COVID-19) deaths worldwide per one million population as of July 13, 2022, by country
| South Africa | 3,997,975 | 2,191 | 101,880 | 59.31 | 33 | 0.56 | 0 | 1,717.79 |  
| Germany | 29,308,100 | 634,888 | 142,139 | 83.24 | 620 | 7.45 | 104 | 1,707.57 |  
| Iran | 7,255,017 | 13,369 | 141,451 | 83.99 | 43 | 0.51 | 7 | 1,684.08 |  
| Costa Rica | 904,934 | 0 | 8,525 | 5.09 | 0 | 0 | 0 | 1,673.5 |  
| Switzerland | 3,861,756 | 55,982 | 13,848 | 8.64 | 13 | 1.51 | 4 | 1,603.35 |  
| Namibia | 169,253 | 0 | 4,068 | 2.54 | 3 | 1.18 | 3 | 1,601 |  
| Lebanon | 1,126,411 | 8,871 | 10,479 | 6.83 | 9 | 1.32 | 2 | 1,535.29 |  
| Ireland | 1,614,631 | 14,017 | 7,536 | 4.99 | 37 | 7.41 | 0 | 1,508.79 |
</excerpt>
### Rank 2 of 86 — 0.69
<excerpt title="NUMBER ONE IN DEATH - AMERICA AND COVID">
**WORLD FUTURE FUND
**http://www.worldfuturefund.org****
INTRODUCTIONDESCRIPTIONCITIZEN GUIDESREADING LISTSITE INDEX  
REPORTSNEWSMULTIMEDIASEARCHHOW TO CONTRIBUTEHELP WANTED
VOLUNTEERSGRANTSPUBLICATIONS PRINCIPLESCOPYRIGHT NOTICECONTACT US
* * *

## AMERICA AND COVID


## A GRIM AND SHAMEFUL RECORD
* * *

## A SHOCKING REALITY


## AMERICA HAS HIGHER DEATH RATE


## THAN MANY MAJOR POOR COUNTRIES
**U.S. COVID DEATH RATES COMPARED TO**
**NATIONS WITH A HIGH POPULATION**
**Country****Deaths/100K Pop**  
United States 335  
Brazil 328  
Russia 265  
Mexico 260  
Indonesia 59  
India 38  
Bangladesh 18  
Pakistan 14  
China 5  
Nigeria 1
Source: Covid Death Rate (Johns Hopkins)
**NUMBER OF COVID DEATHS BY COUNTRY**
**Country****Deaths**  
United States 1,113,236  
Brazil 697,626  
India 530,748  
Russia 387,449  
Mexico 332,483  
Peru 219,214  
United Kingdom 217,658  
Italy 187,272  
Germany 166,526  
France 165,541
Source: Covid Death Rate (Johns Hopkins)
**U.S. COVID DEATH RATES COMPARED TO**
**NATIONS WITH HIGH GDP PER CAPITA**
**Country****Deaths/100K Pop**  
United States 335  
United Kingdom 320  
Italy 308  
France 253  
Sweden 228  
Germany 199  
Canada 132  
South Korea 65  
Japan 52
Source: Covid Death Rate (Johns Hopkins)
**ABOUT THE DATA**
The data above is from Johns Hopkin's website. It represents the number of deaths per 100,000 people in the population.
Also even in absolute numbers, the U.S. has the highest number of people dead from Covid 19.
* * *
**THE HIGH COVID DEATH RATE IN THE U.S.**
The United States is in the top ten countries ranked by Covid 19 death rates.
Life expectancy in the U.S. is also at a 25-year low.
There are serious problems with America's health care system.
In a country where over a million people have been killed by Covid, it's time to provide health care for all.
* * *
**LINKS**

## THAN MANY MAJOR POOR COUNTRIES
Covid Death Rate (Johns Hopkins)
Covid Death Rate by Country (Wikipedia)
Coronavirus (COVID-19) deaths worldwide per one million population as of July 13, 2022, by country (Statista)
Countries where COVID-19 has spread (Worldometer)
People With Long Covid Face Barriers to Government Disability Benefits (KHN, 11-9-22)
Covid-19 and overdose deaths drive U.S. life expectancy to a 25-year low (Politico, 12-22-22)
</excerpt>
### Rank 3 of 86 — 0.68
<excerpt title="Mortality Analyses - Johns Hopkins Coronavirus Resource Center">
## Cases and mortality by country
| Country | Confirmed | Deaths | Case-Fatality | Deaths/100K pop. |  
| --- | --- | --- | --- | --- |  
| Peru | 4,487,553 | 219,539 | 4.9% | 665.84 |  
| Bulgaria | 1,297,523 | 38,228 | 2.9% | 550.17 |  
| Hungary | 2,196,804 | 48,762 | 2.2% | 504.76 |  
| Bosnia and Herzegovina | 401,729 | 16,280 | 4.1% | 496.22 |  
| North Macedonia | 346,852 | 9,662 | 2.8% | 463.77 |  
| Montenegro | 288,808 | 2,808 | 1.0% | 447.09 |  
| Croatia | 1,269,326 | 17,987 | 1.4% | 438.14 |  
| Georgia | 1,827,537 | 16,971 | 0.9% | 425.43 |  
| Czechia | 4,618,256 | 42,491 | 0.9% | 396.78 |  
| Slovakia | 2,667,551 | 21,035 | 0.8% | 387.05 |  
| San Marino | 23,616 | 122 | 0.5% | 359.48 |  
| Lithuania | 1,307,448 | 9,596 | 0.7% | 352.50 |
</excerpt>
### Rank 4 of 86 — 0.68
<excerpt title="COVID-19 deaths per capita by country">
# Coronavirus (COVID-19) deaths worldwide per one million population as of July 13, 2022, by country
| Ethiopia | 490,557 | 901 | 7,552 | 114.96 | 8 | 0.07 | 0 | 65.69 |  
| Liberia | 7,502 | 2 | 294 | 5.06 | 0 | 0 | 0 | 58.13 |  
| Angola | 101,320 | 0 | 1,900 | 32.87 | 0 | 0 | 0 | 57.81 |  
| Madagascar | 66,098 | 311 | 1,403 | 27.69 | 2 | 0.07 | 0 | 50.67 |  
| Uzbekistan | 241,814 | 618 | 1,637 | 34.23 | 0 | 0 | 0 | 47.82 |  
| Ghana | 167,215 | 669 | 1,456 | 31.07 | 4 | 0.13 | 3 | 46.86 |  
| Nicaragua | 14,721 | 31 | 243 | 6.62 | 1 | 0.15 | 0 | 36.68 |  
| Mali | 31,192 | 16 | 737 | 20.25 | 0 | 0 | 0 | 36.39 |  
| Guinea | 37,358 | 235 | 445 | 13.13 | 2 | 0.15 | 2 | 33.88 |  
| Togo | 37,636 | 143 | 275 | 8.28 | 0 | 0 | 0 | 33.22 |
</excerpt>
### Rank 5 of 86 — 0.68
<excerpt title="COVID-19 deaths per capita by country">
# Coronavirus (COVID-19) deaths worldwide per one million population as of July 13, 2022, by country
| Italy | 19,667,320 | 728,549 | 169,390 | 59.55 | 692 | 11.62 | 157 | 2,844.31 |  
| Greece | 3,843,142 | 88,068 | 30,476 | 10.72 | 127 | 11.85 | 0 | 2,844.09 |  
| Belgium | 4,320,107 | 54,811 | 32,015 | 11.56 | 63 | 5.45 | 0 | 2,770.42 |  
| Colombia | 6,198,848 | 23,667 | 140,202 | 50.88 | 132 | 2.59 | 0 | 2,755.39 |  
| United Kingdom¹ | 22,883,995 | 142,930 | 180,718 | 67.22 | 301 | 4.48 | 0 | 2,688.64 |  
| Paraguay | 673,829 | 12,988 | 19,036 | 7.13 | 42 | 5.89 | 0 | 2,668.9 |  
| Russia | 18,198,890 | 22,758 | 373,942 | 144.1 | 302 | 2.1 | 46 | 2,594.94 |
</excerpt>

## Search 6 — query: "top five countries per capita covid deaths Johns Hopkins 2023 list"
### Rank 1 of 164 — 0.74 (passed on)
<excerpt title="COVID-19 pandemic by country and territory">
Venezuela	207	5,856	552,810  
	Mauritania	204	997	63,891  
	Zambia	202	4,078	349,892  
	Afghanistan	197	7,998	235,214  
	Comoros	193	161	9,109  
	Kiribati	183	24	5,085  
	Cambodia	177	3,056	139,326  
	Bangladesh	174	29,531	2,052,280  
	Macau	174	121	3,514  
	Djibouti	166	189	15,690  
	Algeria	151	6,881	272,440  
	Kyrgyzstan	147	1,024	88,953  
	Samoa	144	31	17,057  
	Gambia	141	372	12,627  
	Syria	140	3,163	57,423  
	Cook Islands	135	2	7,375  
	Malawi	130	2,686	89,168  
	Gabon	126	307	49,069  
	Pakistan	125	30,656	1,580,631  
	Tonga	123	13	16,992  
	Senegal	111	1,972	89,440  
	Rwanda	107	1,468	133,274  
	Kenya	104	5,689	344,162  
	Sudan	102	5,046	63,993  
	Equatorial Guinea	101	183	17,130
</excerpt>
### Rank 2 of 164 — 0.73
<excerpt title="COVID-19 pandemic by country and territory">
Libya	5,710	6,017	6,261  
	China	5,699	5,700	6,233  
	Kenya	5,376	5,583	5,639  
	Venezuela	5,324	5,440	5,633  
	Palestine	4,934	5,104	5,513  
	Zimbabwe	4,997	5,338	5,395  
	Latvia	4,570	4,873	5,224  
	Australia	2,239	3,758	5,171  
	Denmark	3,266	3,755	4,612  
	Dominican Republic	4,247	4,307	4,368  
	Oman	4,116	4,146	4,244  
	Puerto Rico	3,305	3,855	4,110  
	El Salvador	3,824	3,899	4,071  
	Namibia	3,616	3,967	4,009  
	Zambia	3,730	3,917	3,952  
	Sudan	3,337	3,533	3,909  
	Trinidad and Tobago	2,850	3,404	3,628  
	Uganda	3,294	3,538	3,588  
	Albania	3,217	3,346	3,469  
	Nigeria	3,031	3,136	3,142  
	Kosovo	2,980	3,005	3,104  
	Syria	2,897	2,989	3,075  
	Cambodia	3,012	3,015	3,032
</excerpt>
### Rank 3 of 164 — 0.69
<excerpt title="COVID-19 pandemic by country and territory">
Iran	1,640	146,837	7,627,863  
	Switzerland	1,611	14,170	4,492,849  
	Guyana	1,596	1,312	75,880  
	Collectivity of Saint Martin	1,591	46	12,324  
	Antigua and Barbuda	1,572	146	9,106  
	Jersey	1,555	161	66,391  
	Luxembourg	1,530	1,000	402,360  
	United States Virgin Islands	1,525	132	25,389  
	Cyprus	1,450	1,364	719,150  
	Caribbean Netherlands	1,430	41	11,922  
	Canada	1,424	55,282	4,819,055  
	Namibia	1,422	4,110	172,557  
	Israel	1,395	12,707	4,841,841  
	French Guiana	1,384	413	98,041  
	Isle of Man	1,378	116	38,008  
	Seychelles	1,370	172	51,899  
	Netherlands	1,283	22,986	8,658,086  
	Jamaica	1,279	3,634	157,710  
	Albania	1,275	3,608	337,234  
	Jordan	1,254	14,122	1,746,997  
	Saint Vincent and the Grenadines	1,214	124	9,674
</excerpt>
### Rank 4 of 164 — 0.69
<excerpt title="COVID-19 pandemic by country and territory">
Updated November 5, 2026.  
COVID-19 cases, deaths, and rates by location[22]  
	Country	Deaths / million	Deaths	Cases  
	World[a]	894	7,117,473	779,452,126  
	Peru	6,604	221,073	4,533,878  
	Bulgaria	5,681	38,778	1,341,082  
	North Macedonia	5,429	9,991	352,093  
	Bosnia and Herzegovina	5,123	16,419	404,289  
	Hungary	5,072	49,124	2,240,998  
	Croatia	4,813	18,806	1,371,707  
	Slovenia	4,686	9,914	1,367,017  
	Georgia	4,519	17,151	1,864,337  
	Montenegro	4,317	2,654	251,280  
	Czech Republic	4,122	43,995	4,887,735  
	Latvia	4,116	7,743	977,810  
	Moldova	4,042	12,290	656,473  
	Slovakia	3,910	21,401	1,890,156  
	Greece	3,866	40,256	5,874,300  
	San Marino	3,693	126	25,292  
	United States	3,631	1,240,149	103,436,829
</excerpt>
### Rank 5 of 164 — 0.66
<excerpt title="COVID-19 pandemic by country and territory">
Switzerland	11,921	12,372	12,683  
	Nepal	11,594	11,752	11,938  
	Moldova	10,275	10,666	11,228  
	Honduras	10,434	10,504	10,775  
	Israel	8,258	8,990	10,234  
	Lebanon	9,119	9,606	10,091  
	Azerbaijan	8,358	8,734	9,417  
	North Macedonia	7,976	8,439	9,025  
	Saudi Arabia	8,877	8,940	8,998  
	Cuba	8,322	8,399	8,494  
	Armenia	7,975	8,056	8,478  
	Lithuania	7,404	7,891	8,431  
	South Korea	5,625	6,772	8,170  
	Panama	7,427	7,716	8,079  
	Costa Rica	7,357	7,555	8,031  
	Afghanistan	7,356	7,414	7,598  
	Ethiopia	6,926	7,337	7,462  
	Slovenia	6,124	6,457	7,049  
	Uruguay	6,169	6,459	6,977  
	Algeria	6,271	6,579	6,835  
	Ireland	6,070	6,346	6,497  
	Belarus	5,578	6,052	6,480
</excerpt>

## Search 7 — query: "Johns Hopkins cumulative per capita covid deaths July 2022 list by country statista top per capita"
### Rank 1 of 114 — 0.59 (passed on)
<excerpt title="COVID-19 deaths per capita by country">
# Coronavirus (COVID-19) deaths worldwide per one million population as of July 13, 2022, by country
| South Africa | 3,997,975 | 2,191 | 101,880 | 59.31 | 33 | 0.56 | 0 | 1,717.79 |  
| Germany | 29,308,100 | 634,888 | 142,139 | 83.24 | 620 | 7.45 | 104 | 1,707.57 |  
| Iran | 7,255,017 | 13,369 | 141,451 | 83.99 | 43 | 0.51 | 7 | 1,684.08 |  
| Costa Rica | 904,934 | 0 | 8,525 | 5.09 | 0 | 0 | 0 | 1,673.5 |  
| Switzerland | 3,861,756 | 55,982 | 13,848 | 8.64 | 13 | 1.51 | 4 | 1,603.35 |  
| Namibia | 169,253 | 0 | 4,068 | 2.54 | 3 | 1.18 | 3 | 1,601 |  
| Lebanon | 1,126,411 | 8,871 | 10,479 | 6.83 | 9 | 1.32 | 2 | 1,535.29 |  
| Ireland | 1,614,631 | 14,017 | 7,536 | 4.99 | 37 | 7.41 | 0 | 1,508.79 |
</excerpt>
### Rank 2 of 114 — 0.59
<excerpt title="COVID-19 deaths per capita by country">
# Coronavirus (COVID-19) deaths worldwide per one million population as of July 13, 2022, by country
COVID-19 cases and deaths per million in 210 countries as of July 13, 2022
Ask AI
Last update: Jul 13, 2022
Region: Worldwide
Statista Research Department
Survey time period: Data as of July 13, 2022, 10:21 CET
Switch chart type
Table
All categories
Download
Press Enter or Space on a column header to sort.

# Coronavirus (COVID-19) deaths worldwide per one million population as of July 13, 2022, by country
| Characteristics | Confirmed cases (absolute) | Cases in last 7 days | Confirmed deaths (absolute) | Population (in millions) | Deaths in last 7 days | Deaths per million (last 7 days) | Daily increase (# deaths) | Deaths per million (total) |  
| --- | --- | --- | --- | --- | --- | --- | --- | --- |  
| Peru | 3,691,213 | 47,014 | 213,714 | 32.97 | 121 | 3.67 | 19 | 6,481.71 |  
| Bulgaria | 1,180,636 | 5,554 | 37,279 | 6.93 | 18 | 2.6 | 2 | 5,376.25 |  
| Bosnia and Herzegovina | 379,982 | 850 | 15,810 | 3.28 | 2 | 0.61 | 0 | 4,818.92 |  
| Hungary | 1,932,788 | 4,663 | 46,661 | 9.75 | 14 | 1.44 | 0 | 4,785.86 |  
| Georgia | 1,662,299 | 0 | 16,844 | 3.71 | 0 | 0 | 0 | 4,535.27 |  
| North Macedonia | 316,729 | 1,935 | 9,337 | 2.07 | 10 | 4.83 | 2 | 4,505.12 |  
| Moldova | 521,182 | 861 | 11,570 | 2.62 | 3 | 1.14 | 0 | 4,415.2 |
</excerpt>
### Rank 3 of 114 — 0.58
<excerpt title="COVID-19 deaths per capita by country">
# Coronavirus (COVID-19) deaths worldwide per one million population as of July 13, 2022, by country
| Italy | 19,667,320 | 728,549 | 169,390 | 59.55 | 692 | 11.62 | 157 | 2,844.31 |  
| Greece | 3,843,142 | 88,068 | 30,476 | 10.72 | 127 | 11.85 | 0 | 2,844.09 |  
| Belgium | 4,320,107 | 54,811 | 32,015 | 11.56 | 63 | 5.45 | 0 | 2,770.42 |  
| Colombia | 6,198,848 | 23,667 | 140,202 | 50.88 | 132 | 2.59 | 0 | 2,755.39 |  
| United Kingdom¹ | 22,883,995 | 142,930 | 180,718 | 67.22 | 301 | 4.48 | 0 | 2,688.64 |  
| Paraguay | 673,829 | 12,988 | 19,036 | 7.13 | 42 | 5.89 | 0 | 2,668.9 |  
| Russia | 18,198,890 | 22,758 | 373,942 | 144.1 | 302 | 2.1 | 46 | 2,594.94 |
</excerpt>
### Rank 4 of 114 — 0.52
<excerpt title="COVID-19 deaths per capita by country">
# Coronavirus (COVID-19) deaths worldwide per one million population as of July 13, 2022, by country
| Zambia | 327,102 | 843 | 4,008 | 18.38 | 1 | 0.05 | 0 | 218.02 |  
| Mauritania | 61,403 | 914 | 986 | 4.65 | 2 | 0.43 | 0 | 212.06 |  
| Venezuela | 528,566 | 1,492 | 5,741 | 28.44 | 6 | 0.21 | 0 | 201.89 |  
| Afghanistan | 183,272 | 479 | 7,728 | 38.93 | 3 | 0.08 | 0 | 198.52 |  
| Cambodia | 136,374 | 73 | 3,056 | 16.72 | 0 | 0 | 0 | 182.79 |  
| Syria | 55,957 | 20 | 3,150 | 17.5 | 0 | 0 | 0 | 179.99 |  
| Bangladesh | 1,991,031 | 8,059 | 29,212 | 164.69 | 31 | 0.19 | 9 | 177.38 |  
| Algeria | 266,303 | 130 | 6,875 | 43.85 | 0 | 0 | 0 | 156.78 |  
| Gambia | 12,009 | 7 | 365 | 2.42 | 0 | 0 | 0 | 151.03 |
</excerpt>
### Rank 5 of 114 — 0.52
<excerpt title="COVID-19 deaths per capita by country">
# Coronavirus (COVID-19) deaths worldwide per one million population as of July 13, 2022, by country
| Zimbabwe | 255,981 | 226 | 5,565 | 14.86 | 7 | 0.47 | 0 | 374.42 |  
| Lesotho | 34,040 | 102 | 702 | 2.14 | 3 | 1.4 | 0 | 327.69 |  
| Saudi Arabia | 800,869 | 2,929 | 9,223 | 34.81 | 11 | 0.32 | 2 | 264.92 |  
| Singapore | 1,540,778 | 54,814 | 1,437 | 5.69 | 16 | 2.81 | 5 | 252.73 |  
| Japan | 9,806,971 | 365,800 | 31,466 | 125.84 | 118 | 0.94 | 23 | 250.06 |  
| Egypt | 515,645 | 0 | 24,725 | 102.33 | 1 | 0.01 | 1 | 241.61 |  
| Qatar | 390,055 | 4,225 | 680 | 2.88 | 1 | 0.35 | 0 | 236.02 |  
| United Arab Emirates | 966,075 | 11,383 | 2,324 | 9.89 | 5 | 0.51 | 0 | 234.98 |
</excerpt>

## Search 8 — query: "Costa Rica 2022 trade deficit WITS goods $B"
### Rank 1 of 118 — 0.79 (passed on)
<excerpt title="What is the value of US trade with Costa Rica?">
## What is the trade balance with Costa Rica?
The US has had a trade deficit with Costa Rica every year from 2019 through 2025. The 2025 deficit was $6.75 billion, an increase from 2024's deficit of $4.95 billion.
The trade deficit with Costa Rica increased to $6.75B in 2025.

## What is the trade balance with Costa Rica?
| Year | Exports | Imports | Trade balance |  
| --- | --- | --- | --- |  
| 2006 | 5.062E9 | 5.181E9 | -1.19E8 |  
| 2007 | 5.685E9 | 5.506E9 | 1.79E8 |  
| 2008 | 6.954E9 | 5.673E9 | 1.281E9 |  
| 2009 | 5.888E9 | 7.3E9 | -1.413E9 |  
| 2010 | 6.515E9 | 1.0507E10 | -3.992E9 |  
| 2011 | 7.491E9 | 1.2003E10 | -4.512E9 |  
| 2012 | 8.647E9 | 1.4101E10 | -5.453E9 |  
| 2013 | 8.73E9 | 1.3987E10 | -5.257E9 |  
| 2014 | 8.487E9 | 1.1628E10 | -3.141E9 |  
| 2015 | 7.711E9 | 6.836E9 | 8.75E8 |  
| 2016 | 7.736E9 | 6.903E9 | 8.33E8 |  
| 2017 | 7.932E9 | 7.132E9 | 8.01E8 |  
| 2018 | 8.348E9 | 8.162E9 | 1.86E8 |  

## What is the trade balance with Costa Rica?
| 2019 | 8.166E9 | 8.254E9 | -8.8E7 |  
| 2020 | 6.838E9 | 7.301E9 | -4.63E8 |  
| 2021 | 9.056E9 | 9.753E9 | -6.98E8 |  
| 2022 | 1.1239E10 | 1.316E10 | -1.921E9 |  
| 2023 | 1.1428E10 | 1.5192E10 | -3.764E9 |  
| 2024 | 1.2195E10 | 1.7143E10 | -4.948E9 |  
| 2025 | 1.2946E10 | 1.9691E10 | -6.745E9 |
</excerpt>
### Rank 2 of 118 — 0.79
<excerpt title="Trade Profile - Costa Rica - International Trade Portal">
# Costa Rica: Trade Profile
## Foreign Trade in Figures
| Foreign Trade Indicators | 2021 | 2022 | 2023 | 2024 | 2025 |  
| --- | --- | --- | --- | --- | --- |  
| Imports of Goods (million USD) | 20,728 | 22,685 | 24,039 | 26,484 | 27,482 |  
| Exports of Goods (million USD) | 15,494 | 16,597 | 19,025 | 21,688 | 26,431 |  
| Imports of Services (million USD) | 4,269 | 5,886 | 6,879 | 7,708 | 8,637 |  
| Exports of Services (million USD) | 9,164 | 13,634 | 15,557 | 17,073 | 18,083 |  
| Imports of Goods and Services (Annual % Change) | 19 | 11 | 7 | 5 | 6 |  
| Exports of Goods and Services (Annual % Change) | 16 | 16 | 11 | 6 | 9 |  
| Trade Balance (million USD) | -2,844 | -4,901 | -3,163 | -2,505 | -925 |  
| Foreign Trade (in % of GDP) | 70 | 79 | 71 | 70 | 71 |  
| Imports of Goods and Services (in % of GDP) | 34 | 38 | 33 | 32 | 33 |  
| Exports of Goods and Services (in % of GDP) | 36 | 41 | 38 | 38 | 39 |
Source: WTO – World Trade Organisation  ; World Bank  - Latest available data.
</excerpt>
### Rank 3 of 118 — 0.76
<excerpt title="Costa Rica Trade Summary 2022 | WITS | Text - World Bank">
Loading..
Country and Region
Year
_Forat a glancei.e. latest available trade, tariff, trade barriers and other trade related dataClick Here_.
Please note the exports, imports and tariff data are based on reported data and not gap filled. Please check the Data Availabilityfor coverage.
*   TABLE  
*   TEXT

#### Imports/Exports


#### Products


### Overall Exports and Imports for Costa Rica 2022
**Exports and imports of Costa Rica**in 2022 are below, along with number of countries and products
*   The total value of **exports** (FoB) was 15,320 million.  
*    The total value of **imports** (CIF) was 21,140 million.   
*   At the **HS6 digit** level, 2,892 products were exported to 156 countries and 4,028 products were imported from 209 countries.

## Costa Rica top 5 Export and Import partners 2022


## Costa Rica **Top 5 Products**exports imports at HS 6 digit level 2022
The **top five exported** HS 6 digit level products to world by Costa Rica along with trade value are:
1.   **Costa Rica exported Needles, catheters, cannulae and the like, nes** , worth 1,996,182.83 (US$ Thousands).   
2.   **Costa Rica exported Instruments and appliances used in medical or v** , worth 1,894,263.24 (US$ Thousands).   
3.   **Costa Rica exported Artificial parts of the body, nes** , worth 1,052,322.19 (US$ Thousands).   
4.   **Costa Rica exported Pineapples, fresh or dried** , worth 1,038,282.41 (US$ Thousands).   
5.   **Costa Rica exported Bananas, including plantains, fresh or dried** , worth 1,018,065.41 (US$ Thousands).
The **top five imported** HS 6 digit level products from world by Costa Rica along with trade value are
1.   **Costa Rica imported Petroleum oils, etc, (excl. crude); preparation** , worth 2,481,387.91 (US$ Thousands).   
2.   **Costa Rica imported Other medicaments of mixed or unmixed products,** , worth 607,515.82 (US$ Thousands).   
3.   **Costa Rica imported Transmission apparatus, for radioteleph incorpo** , worth 561,794.39 (US$ Thousands).   
4.   **Costa Rica imported Other articles of plastics, nes** , worth 324,702.83 (US$ Thousands).   
5.   **Costa Rica imported Maize (excl. seed)** , worth 292,031.02 (US$ Thousands).
</excerpt>
### Rank 4 of 118 — 0.76
<excerpt title="What is the value of US trade with Costa Rica?">
## What is the trade balance with Costa Rica?
| 2019 | 8.166E9 | 8.254E9 | -8.8E7 |  
| 2020 | 6.838E9 | 7.301E9 | -4.63E8 |  
| 2021 | 9.056E9 | 9.753E9 | -6.98E8 |  
| 2022 | 1.1239E10 | 1.316E10 | -1.921E9 |  
| 2023 | 1.1428E10 | 1.5192E10 | -3.764E9 |  
| 2024 | 1.2195E10 | 1.7143E10 | -4.948E9 |  
| 2025 | 1.2946E10 | 1.9691E10 | -6.745E9 |

## What does the US import from Costa Rica?
In 2025, 71.2% of imports from Costa Rica to the US were goods. The largest category was capital goods (tools used for the production process, like machinery and equipment), accounting for $8.64 billion. The top three imports were capital goods, food, feeds, and beverages, and consumer goods (goods and services purchased by individuals for personal use, like clothing and cellphones). These categories accounted for $12.3 billion of total imports.
The other 28.8% were services, with travel being the largest service category. Travel (money leaving the US by Americans spending on things like like lodging, meals, transportation, and entertainment abroad) accounted for $2.88 billion.
Capital goods made up 43.9% of US imports from Costa Rica in 2025.
| Category | Detail | Value |  
| --- | --- | --- |  
| Goods | Automotive vehicles and parts | 2.2E8 |  
| Goods | Capital goods | 8.641E9 |  
| Goods | Consumer goods | 1.55E9 |  
| Goods | Food, feeds, and beverages | 2.095E9 |  
| Goods | Industrial supplies and materials | 4.8E8 |  
| Goods | Nonmonetary gold | 1.22E8 |  
| Goods | Other merchandise | 9.09E8 |  
| Services | Use of intellectual property | 7000000.0 |  
| Services | Construction | 1.6E7 |  
| Services | Financial services | 8.9E7 |  
| Services | Government goods and services | 9000000.0 |  
| Services | Mainantence and repair services | 1.2E7 |  
| Services | Business services | 1.462E9 |  
| Services | Personal, cultural, and recreational services | 2000000.0 |  
| Services | Telecommunications and information services | 7.1E8 |  
| Services | Transport | 4.87E8 |  
| Services | Travel | 2.879E9 |
</excerpt>
### Rank 5 of 118 — 0.71
<excerpt title="Trade Profile - Costa Rica - International Trade Portal">
# Costa Rica: Trade Profile
## Foreign Trade in Figures
According to preliminary data from Costa Rica's Institute of Statistics, foreign trade in 2023 revealed an export customs value of USD 19.211 billion, while imports amounted to USD 26.396 billion, resulting in a trade deficit of approximately USD 7.185 billion. The country's structural deficit is due to the fact that a large proportion of manufactured exports depend on imported inputs, as well as the reliance on imports of consumer goods. According to estimates, Costa Rica should maintain a trade deficit over the medium term. Exports are expected to perform strongly on increased external demand for both capital and agricultural goods, mainly medical devices, pineapples, and bananas. However, that increase should not offset the growth in imports, driven by demand for capital goods and commodities, notably hydrocarbons. On the services side, tourism is a major export earner: the latest data from the WTO shows that Costa Rica is a net service exporter (USD 5.5 billion in imports against USD 11.8 billion in exports in 2022). Therefore, when computing goods and services, the World Bank estimated the country’s trade balance to be positive by 1.5% of GDP in 2022.

# Costa Rica: Trade Profile
## Foreign Trade in Figures
| Foreign Trade Indicators | 2021 | 2022 | 2023 | 2024 | 2025 |  
| --- | --- | --- | --- | --- | --- |  
| Imports of Goods (million USD) | 20,728 | 22,685 | 24,039 | 26,484 | 27,482 |  
| Exports of Goods (million USD) | 15,494 | 16,597 | 19,025 | 21,688 | 26,431 |  
| Imports of Services (million USD) | 4,269 | 5,886 | 6,879 | 7,708 | 8,637 |  
| Exports of Services (million USD) | 9,164 | 13,634 | 15,557 | 17,073 | 18,083 |  
| Imports of Goods and Services (Annual % Change) | 19 | 11 | 7 | 5 | 6 |  
| Exports of Goods and Services (Annual % Change) | 16 | 16 | 11 | 6 | 9 |  
| Trade Balance (million USD) | -2,844 | -4,901 | -3,163 | -2,505 | -925 |  
| Foreign Trade (in % of GDP) | 70 | 79 | 71 | 70 | 71 |  
| Imports of Goods and Services (in % of GDP) | 34 | 38 | 33 | 32 | 33 |  
| Exports of Goods and Services (in % of GDP) | 36 | 41 | 38 | 38 | 39 |
Source: WTO – World Trade Organisation  ; World Bank  - Latest available data.
</excerpt>

## Search 9 — query: "Johns Hopkins Covid deaths per capita table list top countries 2023"
### Rank 1 of 123 — 0.65 (passed on)
<excerpt title="Mortality Analyses - Johns Hopkins Coronavirus Resource Center">
## Cases and mortality by country
| Zimbabwe | 264,276 | 5,671 | 2.1% | 38.16 |  
| Burma | 633,950 | 19,490 | 3.1% | 35.82 |  
| Sao Tome and Principe | 6,281 | 77 | 1.2% | 35.13 |  
| Lesotho | 34,790 | 723 | 2.1% | 33.75 |  
| Singapore | 2,235,294 | 1,722 | 0.1% | 29.43 |  
| Marshall Islands | 15,649 | 17 | 0.1% | 29.10 |  
| Saudi Arabia | 830,127 | 9,618 | 1.2% | 27.63 |  
| Egypt | 515,759 | 24,812 | 4.8% | 24.25 |  
| Qatar | 495,090 | 688 | 0.1% | 23.88 |  
| United Arab Emirates | 1,053,213 | 2,349 | 0.2% | 23.75 |  
| Solomon Islands | 24,575 | 153 | 0.6% | 23.44 |  
| Zambia | 343,135 | 4,057 | 1.2% | 22.07 |  
| Mauritania | 63,668 | 997 | 1.6% | 21.44 |  
| Venezuela | 552,162 | 5,854 | 1.1% | 20.59 |  
| Afghanistan | 209,451 | 7,896 | 3.8% | 20.28 |
</excerpt>
### Rank 2 of 123 — 0.63
<excerpt title="COVID-19 pandemic by country and territory - Wikipedia">
Iran	1,640	146,837	7,627,863  
	Switzerland	1,611	14,170	4,492,849  
	Guyana	1,596	1,312	75,880  
	Collectivity of Saint Martin	1,591	46	12,324  
	Antigua and Barbuda	1,572	146	9,106  
	Jersey	1,555	161	66,391  
	Luxembourg	1,530	1,000	402,360  
	United States Virgin Islands	1,525	132	25,389  
	Cyprus	1,450	1,364	719,150  
	Caribbean Netherlands	1,430	41	11,922  
	Canada	1,424	55,282	4,819,055  
	Namibia	1,422	4,110	172,557  
	Israel	1,395	12,707	4,841,841  
	French Guiana	1,384	413	98,041  
	Isle of Man	1,378	116	38,008  
	Seychelles	1,370	172	51,899  
	Netherlands	1,283	22,986	8,658,086  
	Jamaica	1,279	3,634	157,710  
	Albania	1,275	3,608	337,234  
	Jordan	1,254	14,122	1,746,997  
	Saint Vincent and the Grenadines	1,214	124	9,674
</excerpt>
### Rank 3 of 123 — 0.62
<excerpt title="COVID-19 pandemic by country and territory - Wikipedia">
Venezuela	207	5,856	552,810  
	Mauritania	204	997	63,891  
	Zambia	202	4,078	349,892  
	Afghanistan	197	7,998	235,214  
	Comoros	193	161	9,109  
	Kiribati	183	24	5,085  
	Cambodia	177	3,056	139,326  
	Bangladesh	174	29,531	2,052,280  
	Macau	174	121	3,514  
	Djibouti	166	189	15,690  
	Algeria	151	6,881	272,440  
	Kyrgyzstan	147	1,024	88,953  
	Samoa	144	31	17,057  
	Gambia	141	372	12,627  
	Syria	140	3,163	57,423  
	Cook Islands	135	2	7,375  
	Malawi	130	2,686	89,168  
	Gabon	126	307	49,069  
	Pakistan	125	30,656	1,580,631  
	Tonga	123	13	16,992  
	Senegal	111	1,972	89,440  
	Rwanda	107	1,468	133,274  
	Kenya	104	5,689	344,162  
	Sudan	102	5,046	63,993  
	Equatorial Guinea	101	183	17,130
</excerpt>
### Rank 4 of 123 — 0.61
<excerpt title="Mortality Analyses - Johns Hopkins Coronavirus Resource Center">
## Cases and mortality by country
| Country | Confirmed | Deaths | Case-Fatality | Deaths/100K pop. |  
| --- | --- | --- | --- | --- |  
| Peru | 4,487,553 | 219,539 | 4.9% | 665.84 |  
| Bulgaria | 1,297,523 | 38,228 | 2.9% | 550.17 |  
| Hungary | 2,196,804 | 48,762 | 2.2% | 504.76 |  
| Bosnia and Herzegovina | 401,729 | 16,280 | 4.1% | 496.22 |  
| North Macedonia | 346,852 | 9,662 | 2.8% | 463.77 |  
| Montenegro | 288,808 | 2,808 | 1.0% | 447.09 |  
| Croatia | 1,269,326 | 17,987 | 1.4% | 438.14 |  
| Georgia | 1,827,537 | 16,971 | 0.9% | 425.43 |  
| Czechia | 4,618,256 | 42,491 | 0.9% | 396.78 |  
| Slovakia | 2,667,551 | 21,035 | 0.8% | 387.05 |  
| San Marino | 23,616 | 122 | 0.5% | 359.48 |  
| Lithuania | 1,307,448 | 9,596 | 0.7% | 352.50 |
</excerpt>
### Rank 5 of 123 — 0.61
<excerpt title="Mortality Analyses - Johns Hopkins Coronavirus Resource Center">
## Cases and mortality by country
| Belgium | 4,739,365 | 33,814 | 0.7% | 294.22 |  
| Argentina | 10,044,957 | 130,472 | 1.3% | 288.68 |  
| Colombia | 6,359,093 | 142,339 | 2.2% | 279.74 |  
| Paraguay | 808,401 | 19,878 | 2.5% | 278.69 |  
| Ukraine | 5,711,929 | 119,283 | 2.1% | 272.75 |  
| Russia | 22,075,858 | 388,478 | 1.8% | 266.20 |  
| Mexico | 7,483,444 | 333,188 | 4.5% | 260.73 |  
| Portugal | 5,570,473 | 26,266 | 0.5% | 257.59 |  
| Spain | 13,770,429 | 119,479 | 0.9% | 255.54 |  
| France | 39,866,718 | 166,176 | 0.4% | 254.68 |  
| Tunisia | 1,151,126 | 29,341 | 2.5% | 248.26 |  
| Austria | 5,961,143 | 21,970 | 0.4% | 243.94 |  
| Suriname | 82,467 | 1,404 | 1.7% | 239.33 |
</excerpt>

## Search 10 — query: "worldometer covid death rate per capita top countries 2023"
### Rank 1 of 269 — 0.56 (passed on)
<excerpt title="Covid total deaths per million around the world">
Total Covid deaths per million people.
| Countries | Latest value | Reference | Three months ago | One year ago |  
| --- | --- | --- | --- | --- |  
| Afghanistan | 192 | Mar / 2023 | 191 | 186 |  
| Albania | 1268 | Mar / 2023 | 1265 | 1229 |  
| Algeria | 153 | Mar / 2023 | 153 | 153 |  
| Andorra | 1991 | Mar / 2023 | 1979 | 1916 |  
| Angola | 54 | Mar / 2023 | 54 | 53 |  
| Antigua and Barbuda | 1557 | Mar / 2023 | 1557 | 1440 |  
| Argentina | 2867 | Mar / 2023 | 2859 | 2820 |  
| Armenia | 3144 | Mar / 2023 | 3133 | 3098 |  
| Aruba | 2696 | Mar / 2023 | 2630 | 1991 |  
| Australia | 745 | Mar / 2023 | 681 | 257 |  
| Austria | 2476 | Mar / 2023 | 2406 | 2105 |  
| Azerbaijan | 983 | Mar / 2023 | 966 | 936 |  
| Bahamas | 2032 | Mar / 2023 | 2032 | 1922 |  
| Bahrain | 1043 | Mar / 2023 | 1043 | 998 |  
| Bangladesh | 172 | Mar / 2023 | 172 | 170 |  
| Barbados | 2056 | Mar / 2023 | 2017 | 1175 |
</excerpt>
### Rank 2 of 269 — 0.56
<excerpt title="Covid total deaths per million around the world">
| Trinidad and Tobago | 2856 | Mar / 2023 | 2797 | 2443 |  
| Tunisia | 2376 | Mar / 2023 | 2370 | 2292 |  
| Turkey | 1188 | Mar / 2023 | 1188 | 1148 |  
| USA | 3302 | Mar / 2023 | 3200 | 2883 |  
| Uganda | 77 | Mar / 2023 | 77 | 76 |  
| Ukraine | 2813 | Mar / 2023 | 2791 | 2719 |  
| United Arab Emirates | 249 | Mar / 2023 | 249 | 244 |  
| United Kingdom | 3128 | Mar / 2023 | 2975 | 2496 |  
| Uruguay | 2227 | Mar / 2023 | 2209 | 2091 |  
| Uzbekistan | 47 | Mar / 2023 | 47 | 47 |  
| Vanuatu | 43 | Mar / 2023 | 43 | 6 |  
| Venezuela | 207 | Mar / 2023 | 206 | 201 |  
| Vietnam | 440 | Mar / 2023 | 440 | 432 |  
| Yemen | 64 | Mar / 2023 | 64 | 64 |  
| Zambia | 203 | Mar / 2023 | 201 | 198 |  
| Zimbabwe | 348 | Mar / 2023 | 345 | 333 |
</excerpt>
### Rank 3 of 269 — 0.55
<excerpt title="Covid total deaths per million around the world">
| Cape Verde | 696 | Mar / 2023 | 695 | 676 |  
| Central African Republic | 20 | Mar / 2023 | 20 | 20 |  
| Chad | 11 | Mar / 2023 | 11 | 11 |  
| Chile | 3290 | Mar / 2023 | 3221 | 2880 |  
| China | 85 | Mar / 2023 | 34 | 9 |  
| Colombia | 2750 | Mar / 2023 | 2741 | 2691 |  
| Comoros | 191 | Mar / 2023 | 191 | 191 |  
| Costa Rica | 1797 | Mar / 2023 | 1754 | 1600 |  
| Croatia | 4477 | Mar / 2023 | 4363 | 3861 |  
| Cuba | 761 | Mar / 2023 | 761 | 759 |  
| Cyprus | 1506 | Mar / 2023 | 1404 | 1062 |  
| Czechia | 4065 | Mar / 2023 | 4017 | 3791 |  
| Democratic Republic of the Congo | 15 | Mar / 2023 | 15 | 14 |  
| Denmark | 1424 | Mar / 2023 | 1323 | 964 |  
| Djibouti | 169 | Mar / 2023 | 169 | 169 |  
| Dominica | 1017 | Mar / 2023 | 1017 | 866 |  
| Dominican Republic | 390 | Mar / 2023 | 390 | 390 |
</excerpt>
### Rank 4 of 269 — 0.54
<excerpt title="Covid total deaths per million around the world">
| Slovenia | 4353 | Mar / 2023 | 4173 | 3520 |  
| Solomon Islands | 211 | Mar / 2023 | 211 | 184 |  
| Somalia | 77 | Mar / 2023 | 77 | 77 |  
| South Africa | 1713 | Mar / 2023 | 1713 | 1670 |  
| South Korea | 661 | Mar / 2023 | 622 | 313 |  
| Spain | 2527 | Mar / 2023 | 2485 | 2181 |  
| Sri Lanka | 771 | Mar / 2023 | 770 | 755 |  
| Sudan | 107 | Mar / 2023 | 107 | 105 |  
| Suriname | 2272 | Mar / 2023 | 2254 | 2142 |  
| Swaziland | 1186 | Mar / 2023 | 1183 | 1160 |  
| Sweden | 2262 | Mar / 2023 | 2113 | 1753 |  
| Switzerland | 1599 | Mar / 2023 | 1588 | 1497 |  
| Syria | 143 | Mar / 2023 | 143 | 142 |  
| Tajikistan | 13 | Mar / 2023 | 13 | 13 |  
| Tanzania | 13 | Mar / 2023 | 13 | 12 |  
| Thailand | 473 | Mar / 2023 | 470 | 351 |  
| Togo | 33 | Mar / 2023 | 33 | 31 |  
| Tonga | 112 | Mar / 2023 | 112 | 56 |
</excerpt>
### Rank 5 of 269 — 0.54
<excerpt title="No deaths or no data">
Updated November 5, 2026.  
COVID-19 cases, deaths, and rates by location[22]  
	Country	Deaths / million	Deaths	Cases  
	World[a]	894	7,117,473	779,452,126  
	Peru	6,604	221,073	4,533,878  
	Bulgaria	5,681	38,778	1,341,082  
	North Macedonia	5,429	9,991	352,093  
	Bosnia and Herzegovina	5,123	16,419	404,289  
	Hungary	5,072	49,124	2,240,998  
	Croatia	4,813	18,806	1,371,707  
	Slovenia	4,686	9,914	1,367,017  
	Georgia	4,519	17,151	1,864,337  
	Montenegro	4,317	2,654	251,280  
	Czech Republic	4,122	43,995	4,887,735  
	Latvia	4,116	7,743	977,810  
	Moldova	4,042	12,290	656,473  
	Slovakia	3,910	21,401	1,890,156  
	Greece	3,866	40,256	5,874,300  
	San Marino	3,693	126	25,292  
	United States	3,631	1,240,149	103,436,829
</excerpt>

For each search, read the top excerpt and the ones ranked below it, and judge whether the order is right for answering the question. An excerpt holding the answer, or a fact that leads to it, should outrank one that only repeats the query's words or covers the topic without a checkable fact. If none of the excerpts holds anything useful, that is the search's fault, not this instruction's. Find the ranking error that cost the most and write a new instruction that fixes it. Replace or compress existing text where you can; avoid making it much longer. Do not write the "Original question" or "Search query" lines; they are appended for you. Do not copy any fact, name, site or topic from these examples.

Provide the new instruction within ``` blocks.
