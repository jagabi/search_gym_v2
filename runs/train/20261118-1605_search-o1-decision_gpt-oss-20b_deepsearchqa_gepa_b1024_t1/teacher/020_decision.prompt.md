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
out of the artists who participated in the 2023 The Art of Texas State Parks traveling art exhibit, which ones were from austin texas?

## Expected answer
Fidencio Duran, Malou Flato, Gordon Fowler, Terri Wells

## Grade 1.00

## Search 1 — query: "2023 Art of Texas State Parks traveling art exhibit artists Austin Texas"
### Rank 1 of 38 — 0.98 (passed on)
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
### Rank 2 of 38 — 0.98
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
### Rank 3 of 38 — 0.97
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
### Rank 4 of 38 — 0.97
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
### Rank 5 of 38 — 0.85
<excerpt title="The Art of Texas State Parks">
In 2023, the Texas Parks and Wildlife Department marks the 100th anniversary of the state park system. From its inception in 1923, the Texas park system has grown to 95 sites, covering more than 627,000 acres and comprising 74 state parks, 13 historic sites, and 8 natural areas. This vast collection of natural lands and public places now accommodates almost 9 million visitors each year.
_The Art of Texas State Parks_ celebrates this rich tradition, offering an engaging visual arts survey of Texas state parks as seen through the eyes of leading artists from across the state. Editors Andrew Sansom and Linda J. Reaves have collected original works from thirty of the state’s most influential artists. These stunning visual works are accompanied by a thoughtful essay by William E. Reaves on the time-honored legacy of landscape painting in Texas and by Sansom’s reflections on the vital place of landscape art in Texas conservation. Rounding out the collection, assistant state park director Kevin Good offers an informative profile of Texas state parks, and the work concludes with profiles of the artists whose pieces appear in this special centennial collection.
The centennial of the state parks system offers the perfect occasion to create a lasting visual record of Texas parks in art while memorializing the past and ongoing development of the distinctive collection of Lone Star parks and natural areas. _The Art of Texas State Parks_ offers readers increased awareness of Texas parklands and heightens their popular appeal through the elegant and inspired works of some of Texas’ finest contemporary artists.
Includes the work of these artists:

Randy Bacon, Abilene Mary Baxter, Marfa David Caton, Utopia Charles Criner, Houston Margie Crisp, Elgin Ric Dentinger, San Antonio Fidencio Duran, Austin Janet Eager Krueger, Encinal Joel R. Edwards, Waco Malou Flato, Austin Gordon Fowler, Austin Pat Gabriel, Fort Worth David R. Griffin, Dallas Brian Grimm, Fredericksburg Clemente F. Guzman III, San Antonio Karl E. Hall, Houston John Austin Hanna, Fredericksburg Billy Hassell, Fort Worth Hailey E. Herrera, Bryan Lee Jamison, Huntsville Denise LaRue Mahlke, Whitehouse Talmage Minter, Waco William B. Montgomery, Elgin Kermit Oliver, Waco Noe Perez, Corpus Christi Jeri Salter, Hutto Jim Stoker, San Antonio Bob Stuth-Wade, Dublin Terri M. Wells, Austin
_All author proceeds from the sale of this book will benefit the Texas Parks and Wildlife Foundation._
</excerpt>

## Search 2 — query: "Terri Wells Austin artist Texas State Parks Art of Texas State Parks"
### Rank 1 of 9 — 0.95 (passed on)
<excerpt title="Traveling Art Exhibit Honoring 100 Years of Texas State Parks Moves ...">
## May 23, 2023
### Media Contact: [TPWD News](mailto:news@tpwd.texas.gov "TPWD News"),Business Hours, 512-389-8030
_The Art of Texas State Parks_ is intended to increase public awareness of Texas parklands and heighten their popular appeal through the elegant and inspired works of Texas’ best contemporary painters. While the national park system has benefitted from their chroniclers in art, no such artistic record has yet been undertaken for state parks. The Centennial Celebration of Texas State Parks offers the perfect occasion to create a lasting visual record of Texas State Parks in art and, at the same time, memorialize the past and ongoing development of the distinctive collection of Lone Star parks and natural areas.
Participating artists include:**Randy Bacon** (Abilene); **Mary Baxter** (Marfa); **David Caton** (Utopia); **Charles Criner** (Houston); **Margie Crisp** (Elgin); **Ric Dentinger** (San Antonio/Santa Fe NM); **Fidencio Duran** (Austin); **Janet Eager Krueger** (Encinal); **Joel Edwards** (Waco); **Malou Flato** (Austin); **Gordon Fowler** (Austin); **Pat Gabriel** (Fort Worth); **David****Griffin** (Lubbock/ Dallas); **Brian Grimm** (Fredericksburg); **Clemente Guzman** (San Antonio); **Karl E. Hall** (Houston); **John Austin Hanna** (Fredericksburg); **Billy Hassell** (Fort Worth); **Hailey Herrera** (Bryan); **Lee Jamison** (Huntsville); **Denise Mahlke** (Whitehouse); **Jim Malone** (Fort Worth); **Talmage Minter** (Waco); **William Montgomery** (Elgin); **Kermit Oliver** (Waco); **Noe Perez** (Corpus Christi); **Jeri Salter** (Hutto); **Jim****Stoker** (San Antonio); **Bob Stuth-Wade** (Dublin); and **Terri Wells** (Austin).

## May 23, 2023
### Media Contact: [TPWD News](mailto:news@tpwd.texas.gov "TPWD News"),Business Hours, 512-389-8030
The exhibit can be seen at the Houston Museum of Natural Science May 26 – October 1. It will then be exhibited at the Panhandle Plains Museum in Canyon from Oct. 27 – Feb. 18, 2024. The exhibit will also be displayed in 2024 in College Station, Albany and Tyler. The commemorative book is available online through several sources, including Texas A&M Press and Amazon.
“It was a real pleasure to see the passion these artists brought to this project, and we’re thrilled these works will be on display at prestigious museums across Texas,” said Andrew Sansom, co-author of the commemorative book and founder of the Meadows Center for Water and the Environment at Texas State University. “It is our fervent hope that these works of art will inspire present and future generations of Texans to forever appreciate and protect their parks.”
Along with _The Art of Texas State Parks_, Texas Parks and Wildlife Foundation is partnering with TPWD to celebrate Texas State Parks all year long. H-E-B, the presenting sponsor of the Centennial Celebration, donated $1 million to help Texas State Parks engage all Texans in discovering and exploring their parks. For more information on the Centennial Celebration, including special community events at all Texas State Parks, the history of Texas State Parks and how to make a day visit or overnight reservation, visit TexasStateParks.org/100years.
</excerpt>
### Rank 2 of 9 — 0.94
<excerpt title="Traveling Art Exhibit Honoring 100 Years of Texas State Parks Moves ...">
## May 23, 2023
### Media Contact: [TPWD News](mailto:news@tpwd.texas.gov "TPWD News"),Business Hours, 512-389-8030
News ImageShare on FacebookShare Release URL
_**The Art of Texas State Parks at the Houston Museum of Natural Science May 26 – October 1.**_
**Note: This item is more than three years old.** Please take the publication date into consideration for any date references.
AUSTIN— In honor of the Centennial Celebration of Texas State Parks, the Houston Museum of Natural Science will display a new traveling art exhibit May 26 – October 1.
_The Art of Texas State Parks_ is a visual arts survey of state parks featuring more than 30 parks by some of Texas’ finest artists. Along with the traveling exhibit, the project also includes a commemorative book published by Texas A&M Press. Proceeds from book sales and the sale of the artwork through Foltz Fine Art in Houston will be donated to Texas Parks and Wildlife Foundation to benefit Texas State Parks.
The project was several years in the making. In anticipation of the 2023 Centennial Celebration of Texas State Parks, Texas Parks and Wildlife Foundation partnered with Texas Parks and Wildlife Department (TPWD), the Meadows Center for Water and the Environment at Texas State University, and the Bullock Texas State History Museum to present _The Art of Texas State Parks_. Thirty notable Texas artists were commissioned to create works celebrating parks across Texas. Additional support for the project is provided by H-E-B, presenting sponsor for the Texas State Parks Centennial Celebration.
“We hope that in displaying these extraordinary pieces, visitors will be inspired to get out, and enjoy and explore the stunning natural landscapes we’re fortunate to have right in our backyards,” said Texas Parks and Wildlife Department (TPWD) Executive Director David Yoskowitz, Ph.D. “We are grateful for the collaboration that is bringing _The Art of Texas State Parks_ to museums across Texas, spreading the message about these natural treasures that belong to us all.”

## May 23, 2023
### Media Contact: [TPWD News](mailto:news@tpwd.texas.gov "TPWD News"),Business Hours, 512-389-8030
_The Art of Texas State Parks_ is intended to increase public awareness of Texas parklands and heighten their popular appeal through the elegant and inspired works of Texas’ best contemporary painters. While the national park system has benefitted from their chroniclers in art, no such artistic record has yet been undertaken for state parks. The Centennial Celebration of Texas State Parks offers the perfect occasion to create a lasting visual record of Texas State Parks in art and, at the same time, memorialize the past and ongoing development of the distinctive collection of Lone Star parks and natural areas.
Participating artists include:**Randy Bacon** (Abilene); **Mary Baxter** (Marfa); **David Caton** (Utopia); **Charles Criner** (Houston); **Margie Crisp** (Elgin); **Ric Dentinger** (San Antonio/Santa Fe NM); **Fidencio Duran** (Austin); **Janet Eager Krueger** (Encinal); **Joel Edwards** (Waco); **Malou Flato** (Austin); **Gordon Fowler** (Austin); **Pat Gabriel** (Fort Worth); **David****Griffin** (Lubbock/ Dallas); **Brian Grimm** (Fredericksburg); **Clemente Guzman** (San Antonio); **Karl E. Hall** (Houston); **John Austin Hanna** (Fredericksburg); **Billy Hassell** (Fort Worth); **Hailey Herrera** (Bryan); **Lee Jamison** (Huntsville); **Denise Mahlke** (Whitehouse); **Jim Malone** (Fort Worth); **Talmage Minter** (Waco); **William Montgomery** (Elgin); **Kermit Oliver** (Waco); **Noe Perez** (Corpus Christi); **Jeri Salter** (Hutto); **Jim****Stoker** (San Antonio); **Bob Stuth-Wade** (Dublin); and **Terri Wells** (Austin).
</excerpt>
### Rank 3 of 9 — 0.54
<excerpt title="Terri Wells - About the Artist">
**www.terrimwells.com**
**Artist Statement**
_Nature’s light, movement, and color—deeply immersed, absorbed, contemplated—and the joy of that experience._
Known primarily for her plein air watercolors, Terri additionally creates studio oils and abstract sculptures directly related to her plein air work. She has an eye for nuanced, vibrant color, and memorable compositions.
**Career Highlights**
Texas State Parks Centennial Artist for TPWD &Art of Texas Parks
Maynard Dixon Country
Residencies:
The Brinton Museum
Thunderbird Foundation for the Arts
Plein Air Austin- President and Chairman of the Board 2005-08
**Education**
1982 Kent State University-BFA- Studio Art-Drawing and Painting
1981 Blossom Festival School of Art, Kent,Ohio 1981
1978-80 Iowa State University Design School
Over the years, many workshops with professional artists including Kenn Backhaus, Janet Fish, Joseph Zbukvic, Skip Whitcomb, Ray Roberts, Elizabeth Sandia, and Denise LaRue Mahlke.
Terri grew up in two worlds. Her appreciation for nature was heightened by frequent hikes through the fields, woods, meadows, and creek sides surrounding her parents' farm near Lake Geneva, Wisconsin. Her appreciation for the arts and city life was fostered by trips to the Art Institute of Chicago and the vast collection of public art on display throughout the city.
**Selected Exhibitions**
2023 _Treasures From the Collection,_ The Binton Museum, Big Horn, WY
2023-2025 _The Art of Texas Parks_, 6 Texas Museums
2021 _Contemporary Texas Landscapes,_ Foltz Fine Art, Houston, TX
2020 _The Texas Aesthetic,_ Foltz Fine Art, Houston, TX
2019 _Storied Land_ s, Foltz Fine Art, group show, Houston, TX
2019 The Brinton Museum, Brinton AIR, 6-person, Big Horn, WY
2019 Maynard Dixon Country, Mt. Carmel, UT
2018 Plein Air SW Salon, Dallas and Rockport, TX
2015 Maynard Dixon Camp Out, Mt. Carmel UT

2015 Plein Air SW Salon, Dallas and Rockport, TX
2013 America’s Parks Through the Beauty of Art, US touring show
2013 Plein Air SW Salon, Dallas and Rockport, TX
2010 Scottsdale’s Best and Brightest, Scottsdale, AZ
2010 Plein Air Austin at the Forsyth Museum, Bryan, TX
2010 Plein Air Austin, University of TX, Austin, TX 2008 EAST, Solo show, Austin, TX
**Selected Public Collections**
The Brinton Museum, Big Horn, WY
Thunderbird Foundation for the Arts, Mt. Carmel, UT
Lakeside Country Club, Houston, TX
</excerpt>
### Rank 4 of 9 — 0.54
<excerpt title="The Art of Texas State Parks">
In 2023, the Texas Parks and Wildlife Department marks the 100th anniversary of the state park system. From its inception in 1923, the Texas park system has grown to 95 sites, covering more than 627,000 acres and comprising 74 state parks, 13 historic sites, and 8 natural areas. This vast collection of natural lands and public places now accommodates almost 9 million visitors each year.
_The Art of Texas State Parks_ celebrates this rich tradition, offering an engaging visual arts survey of Texas state parks as seen through the eyes of leading artists from across the state. Editors Andrew Sansom and Linda J. Reaves have collected original works from thirty of the state’s most influential artists. These stunning visual works are accompanied by a thoughtful essay by William E. Reaves on the time-honored legacy of landscape painting in Texas and by Sansom’s reflections on the vital place of landscape art in Texas conservation. Rounding out the collection, assistant state park director Kevin Good offers an informative profile of Texas state parks, and the work concludes with profiles of the artists whose pieces appear in this special centennial collection.
The centennial of the state parks system offers the perfect occasion to create a lasting visual record of Texas parks in art while memorializing the past and ongoing development of the distinctive collection of Lone Star parks and natural areas. _The Art of Texas State Parks_ offers readers increased awareness of Texas parklands and heightens their popular appeal through the elegant and inspired works of some of Texas’ finest contemporary artists.
Includes the work of these artists:

Randy Bacon, Abilene Mary Baxter, Marfa David Caton, Utopia Charles Criner, Houston Margie Crisp, Elgin Ric Dentinger, San Antonio Fidencio Duran, Austin Janet Eager Krueger, Encinal Joel R. Edwards, Waco Malou Flato, Austin Gordon Fowler, Austin Pat Gabriel, Fort Worth David R. Griffin, Dallas Brian Grimm, Fredericksburg Clemente F. Guzman III, San Antonio Karl E. Hall, Houston John Austin Hanna, Fredericksburg Billy Hassell, Fort Worth Hailey E. Herrera, Bryan Lee Jamison, Huntsville Denise LaRue Mahlke, Whitehouse Talmage Minter, Waco William B. Montgomery, Elgin Kermit Oliver, Waco Noe Perez, Corpus Christi Jeri Salter, Hutto Jim Stoker, San Antonio Bob Stuth-Wade, Dublin Terri M. Wells, Austin
_All author proceeds from the sale of this book will benefit the Texas Parks and Wildlife Foundation._
</excerpt>
### Rank 5 of 9 — 0.47
<excerpt title="Art of Texas State Parks">
In celebration of 100 years of the Texas State Park System, the Texas Parks and Wildlife Department commissioned Texas visual artists to create works inspired by state parks and sites. Artists explored 65 parks, natural areas, and historic sites in the state park system. The results are some 30 paintings and drawings that are as diverse and unique as the ecosystems and history they portray.
These works are far more than a record of place, rather they represent the subject’s source of inspiration, beauty, and refuge—while inspiring a sense of duty to appreciate and preserve these places for future generations. Various types of media are employed by 30 artists to create works that focus on expansive vistas to intimate habitats and their flora and fauna.
Established in 1923 by the 38th Texas Legislature to provide conservation and management of public lands, the Texas State Park System has expanded to 89 sites that represent 640,000 acres of public land. These sites — 74 state parks, 6 state historic sites, and 9 state natural areas — preserve Texas’ landscapes, provide refuge and habitat for native plants and animals, and offer an increasingly urban population places to connect to the natural world.
The traveling exhibition of _The Art of Texas State Parks_ includes work by artists Randy Bacon, Mary Baxter, David Caton, Charles Criner, Margie Crisp, Ric Dentinger, Fidencio Duran, Joel R. Edwards, Malou Flato, Gordon Fowler, Pat Gabriel, David R. Griffin, Brian Grimm, Clemente F. Guzman III, Karl E. Hall, John Austin Hanna, Billy Hassell, Hailey E. Herrera, Lee Jamison, Denise LaRue Mahlke, Jim Malone, Talmage Minter, William B. Montgomery, Noe Perez, Jeri Salter, Jim Stoker, Bob Stuth-Wade, and Terri M. Wells.
The Art of Texas State Parks: A Centennial Exhibition is organized and sponsored by The Meadows Center for Water and the Environment at Texas State University. Exhibition partners include the Texas Parks and Wildlife Department and the Texas Parks and Wildlife Foundation. Additional community support is generously provided by Carolyn & Karl Rathjen, Jeff & Susan Jones, Nancy & Joe Foran in honor of Doris Miller & Don Fitzgibbons, Pam & Bob Tidwell, Scott Chase & Debra Witter, and Doris Miller & Don Fitzgibbons.
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
I'm studying the effects of product safety legislation on safety recalls during periods of economic turmoil, with a main focus on the Covid-19 pandemic in Australia and gas products. 

Give me a list of the PRA Numbers of all product safety recalls posted on www.productsafety.gov.au between 1 January 2020 and 1 July 2020 (inclusive) that have been labelled as containing the topic "Gas products and appliances". Exclude products that were not sold 'Nationally'.

The list should look like this: 2020/11111, 2020/11112, 2020/11115, 2020/11116, 2020/11117, 2020/11119, 2020/11125

## Expected answer
2020/18315, 2020/18164, 2020/18098

## Grade 0.00

## Search 1 — query: "productsafety.gov.au 2020 "Gas products and appliances" recall 2020/"
### Rank 1 of 13 — 0.20 (passed on)
<excerpt title="500 Series Cooker Grill and Cooktops for Caravans and Motorhomes">
# 500 Series Cooker Grill and Cooktops for Caravans and Motorhomes
## How to check if you’re affected
Compare the product name and identifiers below with the item you own. Check the official notice for the affected products and next steps.
Models
LIST

# 500 Series Cooker Grill and Cooktops for Caravans and Motorhomes
## Checked manually this time?
Follow brands and keywords in the app to receive alerts for matching official notices.
Turn on recall alerts

# 500 Series Cooker Grill and Cooktops for Caravans and Motorhomes
## Affected products
Product 1
This recall was updated on 28 October 2022 to confirm affected cookers and information about inspection and repairs. (Update 4, revised 28 Oct 2022) 500 Series Cooker/Grill and Cooktops Products were supplied to caravan, camper, motorhome manufacturers and directly to consumers. See attached Model list Cookers manufactured: • between 1 January 2019 and 31 May 2020 (inclusive) have been recalled – Follow instructions under What should consumers do? section below. • before 1 January 2019 are not subject to recall – consumers can continue to use these cookers as per the instructions for use provided with the appliance. • on or after 1 June 2020 are not subject to recall – consumers can continue to use these cookers as per the instructions for use provided with the appliance. To identify affected appliances, check the model number on the data plate. Open the glass lid and look for the data plate on the inside front left side of the lid.
Hazard
If the gas leaks in the presence of an ignition source this can lead to an explosion and/or fire, which may result in serious illness, injury or death. The defect has caused incidents that have caused serious injuries and burns.

# 500 Series Cooker Grill and Cooktops for Caravans and Motorhomes
## Where it was sold
Retailer information is not currently available in RecallScope. Check theofficial noticefor distribution details.
Location 1
AU · Australia
Affected area 1
AU · Australia

# 500 Series Cooker Grill and Cooktops for Caravans and Motorhomes
## Source & status
Source
ACCC
Tier
beta
Category
Home & Consumer
Official classification
Gas products and appliances, Caravan, motorhome and camper accessories

# 500 Series Cooker Grill and Cooktops for Caravans and Motorhomes
## Recall details
Recall number
40dbd67c-bdd3-41ff-8378-860f71e75c75
Source tier
beta

# 500 Series Cooker Grill and Cooktops for Caravans and Motorhomes
## Documents, notices & source
See the official notice and source documents for full details.
View full official notice
Something wrong on this page?Report incorrect data

# 500 Series Cooker Grill and Cooktops for Caravans and Motorhomes
## Related recalls
Home & Consumer
High

# 500 Series Cooker Grill and Cooktops for Caravans and Motorhomes
## Related recalls
### Yoyo (M) Portable Bluetooth Speakers
ACCC29 Sept 2026
Brand match
—
Markets
Australia
Home & Consumer
High

# 500 Series Cooker Grill and Cooktops for Caravans and Motorhomes
## Related recalls
### Two-stage LPG gas pressure regulator for Snowy River and Newgen caravans
ACCC17 Aug 2026
Brand match
—
Markets
Australia
Home & Consumer
High

# 500 Series Cooker Grill and Cooktops for Caravans and Motorhomes
## Related recalls
### Mistral Barrel Cyclonic Vacuum Cleaner – sold at Bunnings
ACCC10 Jun 2026
Brand match
—
Markets
Australia
Home & Consumer
High

# 500 Series Cooker Grill and Cooktops for Caravans and Motorhomes
## Related recalls
### Yoyo (M) Portable Bluetooth Speakers
ACCC29 Sept 2026
Brand match
—
Markets
Australia
Home & Consumer
High
</excerpt>
### Rank 2 of 13 — 0.18
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
### Rank 3 of 13 — 0.08
<excerpt title="Caravan and motorhome owners urged to check for deadly faulty water ...">
Consumers who experience difficulties obtaining a timely remedy should contact Coast to Coast Caravan and Leisure, their state or territory gas regulator or the ACCC online.

## Background
Coast to Coast Caravan and Leisure notified a recall for Suburban Recreational Vehicle Water Heaters on 15 November 2019 due to their serious safety hazards. 18,139 heaters have been sold across all states and territories in Australia mostly installed in caravans and RVs via certain caravan and motorhome retailers.
Gas regulators have been working with Coast to Coast Caravan and Leisure to identify a suitable safe replacement water heater. Replacement models initially proposed by Suburban, the overseas manufacturer, also failed testing. A safe model was finally produced, and approved for use in July 2020.
Remediation could not commence until the GTRC was satisfied of the safety of the replacement units. The supplier then needed to import sufficient units from the US manufacturer, at a time when their supply chains were impacted by the pandemic situation.
The supplier advises stocks of replacement units are now in hand and they are keen to get remediation happening quickly. To date, only 210 units have been remediated or scheduled for inspection, and the supplier would like to encourage greater consumer response to the recall.
The affected products are the Suburban Recreational Vehicle Water Heaters with model numbers SW6DEA, SW6DA, SW4DEA, SW4DA, SW4DECA, SW6DECA and SW6PA that have serial numbers between 181315552 and 193002648 (some serial numbers may end with a 'D') and between 8183311827 and 8190201139. They were manufactured between 4 April 2018 and 1 August 2019.
The Office of the Technical Regulator (SA) is the responsible regulator for this product. It is a member of the Gas Technical Regulators Committee (GTRC). The GTRC is composed of gas technical and safety regulators across Australia and aims to apply a consistent regulatory approach to improve gas safety, measurement and quality.
More information is available at Coast to Coast Caravan and Leisure — Suburban Recreational Vehicle Water Heaters Model SW6PA, SW6DEA, SW6DA, SW4DEA, SW4DA, SW4DECA and SW6DECA.
**Media enquiries:**

## Background
Media team - 1300 138 917
</excerpt>
### Rank 4 of 13 — 0.06
<excerpt title="500 Series Cooker Grill and Cooktops for Caravans and Motorhomes">
# This recall was updated on 28 October 2022 to confirm affected cookers and information about inspection and repairs. (Update 4, revised 28 Oct 2022) 500 Series Cooker/Grill and Cooktops Products were supplied to caravan, camper, motorhome manufacturers and directly to consumers. See attached Model list Cookers manufactured: • between 1 January 2019 and 31 May 2020 (inclusive) have been recalled – Follow instructions under What should consumers do? section below. • before 1 January 2019 are not subject to recall – consumers can continue to use these cookers as per the instructions for use provided with the appliance. • on or after 1 June 2020 are not subject to recall – consumers can continue to use these cookers as per the instructions for use provided with the appliance. To identify affected appliances, check the model number on the data plate. Open the glass lid and look for the data plate on the inside front left side of the lid | RecallScope
RecallScopeRecallsHow it worksWhat we coverOur sourcesPricingMoreGet the app
EN  
▾
EN  
▾
1.   Home  
2.   >Recalls  
3.   >Australia recalls  
4.   >Home & Consumer  
5.   >500 Series Cooker Grill and Cooktops for Caravans and Motorhomes

1.   Home  
2.   >…  
3.   >500 Series Cooker Grill and Cooktops for Caravans and Motorhomes
Image: ACCC recall notice

# 500 Series Cooker Grill and Cooktops for Caravans and Motorhomes
Official notice
23 Jun 2022
RecallScope risk estimate:HighACCC
An official ACCC notice concerns 500 Series Cooker Grill and Cooktops for Caravans and Motorhomes. If the gas leaks in the presence of an ignition source this can lead to an explosion and/or fire, which may result in serious illness, injury or death. The defect has caused incidents that have caused serious injuries and burns. Published 2022-06-23.

# 500 Series Cooker Grill and Cooktops for Caravans and Motorhomes
## What to do now
For cookers manufactured between 1 January 2019 and 31 May 2020 (inclusive) : 1. Turn the front left burner control knob to the off position, remove the knob and store it out of reach of other users. 2. DO NOT USE the front hotplate left burner. The other burners and the electric hotplate can be used. 3. Contact a Swift service agent to arrange an inspection and repairs (if required). Swift service agents information is available here: https://swiftappliancegroup.com.au/repairs-warranty/ If you are in a remote area or unable to access an approved Swift service agent, contact a licensed plumber or gasfitter and request they contact Swift for authorisation and instructions on how to conduct the remedial process. Contact details for Swift Appliance Group: • swiftrecall@outlook.com • 0412 821 912 (Monday to Thursday 8am to 4:30pm and Friday 8am to 1:30pm) • Register your details and receive updates: https://swiftappliancegroup.com.au/recall-register It is recommended that consumers install a gas leak detector inside the cupboard underneath the gas cooker unit if the caravan or motorhome is intended to travel off-road.
Recall number
40dbd67c-bdd3-41ff-8378-860f71e75c75
Official notice
2022-06-23
Watch this recall in the appOpen source hub ↗Report an error

# 500 Series Cooker Grill and Cooktops for Caravans and Motorhomes
## The hazard
If the gas leaks in the presence of an ignition source this can lead to an explosion and/or fire, which may result in serious illness, injury or death. The defect has caused incidents that have caused serious injuries and burns.

# 500 Series Cooker Grill and Cooktops for Caravans and Motorhomes
## How to check if you’re affected
Compare the product name and identifiers below with the item you own. Check the official notice for the affected products and next steps.
Models
LIST
</excerpt>
### Rank 5 of 13 — 0.04
<excerpt title="Caravan and motorhome owners urged to check for deadly faulty water ...">
Consumers are urged to check their caravans and recreational vehicles (RVs) for dangerous Suburban-branded water heaters which may emit deadly carbon monoxide.
The Suburban Recreational Vehicle water heater can operate using electricity or gas, and may produce unsafe levels of carbon monoxide when gas is used to generate the heat.
Carbon monoxide poisoning can cause death, and exposure for a short amount of time can lead to serious injuries. Carbon monoxide has no smell and is unlikely to be detected. It is also highly flammable and can explode on contact with a spark or flame.
The Gas Technical Regulators Committee (GTRC), with the ACCC’s assistance, is raising awareness of the need for repair of thousands of water heaters.
“Do not use the affected water heaters in gas mode under any circumstances,” ACCC Deputy Chair Delia Rickard said.
“It’s especially important to check your caravan’s water heater as soon as possible if you plan to go away during the summer holidays. It only takes a minute and it could save the lives of your loved ones.”
“We are concerned that a large number of deadly heaters remain in caravans and RVs because owners have not yet contacted Coast to Coast for an inspection. Coast to Coast Caravan and Leisure has recalled these heaters due to the serious hazards they present. Owners should not take this issue lightly and act quickly,” Ms Rickard said.
Consumers can check if their heater is affected by opening the exterior access door to the hot water service and checking the model and serial number located on the right hand side. They should then enter the serial number at the Coast to Coast website.
“Anyone with an affected water heater should urgently contact Coast to Coast Caravan and Leisure on 02 9645 7685 who will arrange for a licensed gas fitter to inspect their water heater free of charge,” Ms Rickard said.
Consumers will not have to cover any costs related to the supply and installation of the new water heater, or any required associated work, such as the modification of cavity and gas and/or water lines.
Coast to Coast Caravan and Leisure will check every unit, after being contacted by consumers, to ensure the water heater is properly installed and if needed, will replace the unit through a licenced gasfitter free of charge.

Consumers who experience difficulties obtaining a timely remedy should contact Coast to Coast Caravan and Leisure, their state or territory gas regulator or the ACCC online.
</excerpt>

## Search 2 — query: "site:productsafety.gov.au/recalls "Gas products and appliances" 2020"
### Rank 1 of 1 — 0.19 (passed on)
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

## Search 3 — query: "productsafety.gov.au/recalls 2020 "Gas products and appliances" "recall" "PRA""
(no page could be scored)

## Search 4 — query: "site:productsafety.gov.au "Gas products and appliances" 2020/"
### Rank 1 of 3 — 0.15 (passed on)
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
### Rank 2 of 3 — 0.05
<excerpt title="Caravan and motorhome owners urged to check for deadly faulty water ...">
Consumers who experience difficulties obtaining a timely remedy should contact Coast to Coast Caravan and Leisure, their state or territory gas regulator or the ACCC online.

## Background
Coast to Coast Caravan and Leisure notified a recall for Suburban Recreational Vehicle Water Heaters on 15 November 2019 due to their serious safety hazards. 18,139 heaters have been sold across all states and territories in Australia mostly installed in caravans and RVs via certain caravan and motorhome retailers.
Gas regulators have been working with Coast to Coast Caravan and Leisure to identify a suitable safe replacement water heater. Replacement models initially proposed by Suburban, the overseas manufacturer, also failed testing. A safe model was finally produced, and approved for use in July 2020.
Remediation could not commence until the GTRC was satisfied of the safety of the replacement units. The supplier then needed to import sufficient units from the US manufacturer, at a time when their supply chains were impacted by the pandemic situation.
The supplier advises stocks of replacement units are now in hand and they are keen to get remediation happening quickly. To date, only 210 units have been remediated or scheduled for inspection, and the supplier would like to encourage greater consumer response to the recall.
The affected products are the Suburban Recreational Vehicle Water Heaters with model numbers SW6DEA, SW6DA, SW4DEA, SW4DA, SW4DECA, SW6DECA and SW6PA that have serial numbers between 181315552 and 193002648 (some serial numbers may end with a 'D') and between 8183311827 and 8190201139. They were manufactured between 4 April 2018 and 1 August 2019.
The Office of the Technical Regulator (SA) is the responsible regulator for this product. It is a member of the Gas Technical Regulators Committee (GTRC). The GTRC is composed of gas technical and safety regulators across Australia and aims to apply a consistent regulatory approach to improve gas safety, measurement and quality.
More information is available at Coast to Coast Caravan and Leisure — Suburban Recreational Vehicle Water Heaters Model SW6PA, SW6DEA, SW6DA, SW4DEA, SW4DA, SW4DECA and SW6DECA.
**Media enquiries:**

## Background
Media team - 1300 138 917
</excerpt>
### Rank 3 of 3 — 0.03
<excerpt title="Caravan and motorhome owners urged to check for deadly faulty water ...">
Consumers are urged to check their caravans and recreational vehicles (RVs) for dangerous Suburban-branded water heaters which may emit deadly carbon monoxide.
The Suburban Recreational Vehicle water heater can operate using electricity or gas, and may produce unsafe levels of carbon monoxide when gas is used to generate the heat.
Carbon monoxide poisoning can cause death, and exposure for a short amount of time can lead to serious injuries. Carbon monoxide has no smell and is unlikely to be detected. It is also highly flammable and can explode on contact with a spark or flame.
The Gas Technical Regulators Committee (GTRC), with the ACCC’s assistance, is raising awareness of the need for repair of thousands of water heaters.
“Do not use the affected water heaters in gas mode under any circumstances,” ACCC Deputy Chair Delia Rickard said.
“It’s especially important to check your caravan’s water heater as soon as possible if you plan to go away during the summer holidays. It only takes a minute and it could save the lives of your loved ones.”
“We are concerned that a large number of deadly heaters remain in caravans and RVs because owners have not yet contacted Coast to Coast for an inspection. Coast to Coast Caravan and Leisure has recalled these heaters due to the serious hazards they present. Owners should not take this issue lightly and act quickly,” Ms Rickard said.
Consumers can check if their heater is affected by opening the exterior access door to the hot water service and checking the model and serial number located on the right hand side. They should then enter the serial number at the Coast to Coast website.
“Anyone with an affected water heater should urgently contact Coast to Coast Caravan and Leisure on 02 9645 7685 who will arrange for a licensed gas fitter to inspect their water heater free of charge,” Ms Rickard said.
Consumers will not have to cover any costs related to the supply and installation of the new water heater, or any required associated work, such as the modification of cavity and gas and/or water lines.
Coast to Coast Caravan and Leisure will check every unit, after being contacted by consumers, to ensure the water heater is properly installed and if needed, will replace the unit through a licenced gasfitter free of charge.

Consumers who experience difficulties obtaining a timely remedy should contact Coast to Coast Caravan and Leisure, their state or territory gas regulator or the ACCC online.
</excerpt>

## Search 5 — query: "2020 site:productsafety.gov.au/recalls "Gas products and appliances" "PRA""
### Rank 1 of 1 — 0.26 (passed on)
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

## Search 6 — query: ""Gas products and appliances" "Productsafety.gov.au" "2020""
### Rank 1 of 13 — 0.12 (passed on)
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
### Rank 2 of 13 — 0.06
<excerpt title="Caravan and motorhome owners urged to check for deadly faulty water ...">
Consumers who experience difficulties obtaining a timely remedy should contact Coast to Coast Caravan and Leisure, their state or territory gas regulator or the ACCC online.

## Background
Coast to Coast Caravan and Leisure notified a recall for Suburban Recreational Vehicle Water Heaters on 15 November 2019 due to their serious safety hazards. 18,139 heaters have been sold across all states and territories in Australia mostly installed in caravans and RVs via certain caravan and motorhome retailers.
Gas regulators have been working with Coast to Coast Caravan and Leisure to identify a suitable safe replacement water heater. Replacement models initially proposed by Suburban, the overseas manufacturer, also failed testing. A safe model was finally produced, and approved for use in July 2020.
Remediation could not commence until the GTRC was satisfied of the safety of the replacement units. The supplier then needed to import sufficient units from the US manufacturer, at a time when their supply chains were impacted by the pandemic situation.
The supplier advises stocks of replacement units are now in hand and they are keen to get remediation happening quickly. To date, only 210 units have been remediated or scheduled for inspection, and the supplier would like to encourage greater consumer response to the recall.
The affected products are the Suburban Recreational Vehicle Water Heaters with model numbers SW6DEA, SW6DA, SW4DEA, SW4DA, SW4DECA, SW6DECA and SW6PA that have serial numbers between 181315552 and 193002648 (some serial numbers may end with a 'D') and between 8183311827 and 8190201139. They were manufactured between 4 April 2018 and 1 August 2019.
The Office of the Technical Regulator (SA) is the responsible regulator for this product. It is a member of the Gas Technical Regulators Committee (GTRC). The GTRC is composed of gas technical and safety regulators across Australia and aims to apply a consistent regulatory approach to improve gas safety, measurement and quality.
More information is available at Coast to Coast Caravan and Leisure — Suburban Recreational Vehicle Water Heaters Model SW6PA, SW6DEA, SW6DA, SW4DEA, SW4DA, SW4DECA and SW6DECA.
**Media enquiries:**

## Background
Media team - 1300 138 917
</excerpt>
### Rank 3 of 13 — 0.03
<excerpt title="Caravan and motorhome owners urged to check for deadly faulty water ...">
Consumers are urged to check their caravans and recreational vehicles (RVs) for dangerous Suburban-branded water heaters which may emit deadly carbon monoxide.
The Suburban Recreational Vehicle water heater can operate using electricity or gas, and may produce unsafe levels of carbon monoxide when gas is used to generate the heat.
Carbon monoxide poisoning can cause death, and exposure for a short amount of time can lead to serious injuries. Carbon monoxide has no smell and is unlikely to be detected. It is also highly flammable and can explode on contact with a spark or flame.
The Gas Technical Regulators Committee (GTRC), with the ACCC’s assistance, is raising awareness of the need for repair of thousands of water heaters.
“Do not use the affected water heaters in gas mode under any circumstances,” ACCC Deputy Chair Delia Rickard said.
“It’s especially important to check your caravan’s water heater as soon as possible if you plan to go away during the summer holidays. It only takes a minute and it could save the lives of your loved ones.”
“We are concerned that a large number of deadly heaters remain in caravans and RVs because owners have not yet contacted Coast to Coast for an inspection. Coast to Coast Caravan and Leisure has recalled these heaters due to the serious hazards they present. Owners should not take this issue lightly and act quickly,” Ms Rickard said.
Consumers can check if their heater is affected by opening the exterior access door to the hot water service and checking the model and serial number located on the right hand side. They should then enter the serial number at the Coast to Coast website.
“Anyone with an affected water heater should urgently contact Coast to Coast Caravan and Leisure on 02 9645 7685 who will arrange for a licensed gas fitter to inspect their water heater free of charge,” Ms Rickard said.
Consumers will not have to cover any costs related to the supply and installation of the new water heater, or any required associated work, such as the modification of cavity and gas and/or water lines.
Coast to Coast Caravan and Leisure will check every unit, after being contacted by consumers, to ensure the water heater is properly installed and if needed, will replace the unit through a licenced gasfitter free of charge.

Consumers who experience difficulties obtaining a timely remedy should contact Coast to Coast Caravan and Leisure, their state or territory gas regulator or the ACCC online.
</excerpt>
### Rank 4 of 13 — 0.00
<excerpt title="Search results for: 'box 2560 site'">
# Search results for: 'box 2560 site'
### Popular Searches
*   Medical Dressings  
*   Medical Hygiene  
*   Syringes  
*   Casting Supplies  
*   Blood Collection  
*   IV Fluids  
*   Kidney Dishes & Trays  
*   Skin Closure  
*   TRT
Phlebotomy Supplies
*   Blood Bags  
*   Blood Collection Needle  
*   Blood Collection Sets  
*   Blood Collection Syringe  
*   Blood Transfusion Sets  
*   Capillary Tubes  
*   Microtainer Tubes  
*   Vacutainer Holder  
*   Vacutainer Tubes
Browse Laboratory Supplies
*   Specimen Jars  
*   Pipettors  
*   Centrifuge  
*   Microscope Slides  
*   Cytology  
*   Waste Bags  
*   Swabs
Browse Microscope Slides
*   Blood Dispenser  
*   Coverslips  
*   Slide Mailer  
*   Slides  
*   Slides Pencil  
*   Spreader Bar  
*   Tray & Storage Box







*   Home  
*   **Search Results for "box 2560 site"**
**Search Results for “box 2560 site”**0 Items
**No matching products**Try another search term or remove some filters.
**Filter Products**Clear all
Active filters
1.   Plaster Cast Type:6301Remove
Plaster Cast Type
1.   Artiflex Soft 2 items  
2.   Delta Cast Soft 4 items  
3.   Delta Lite Elite 3 items  
4.   Delta Lite Plus 4 items  
5.   Gypsona Plaster 5 items  
6.   Soffban Synthetic 2 items  
7.   Soffban Natural 1 item  
8.   Velband Bandage 2 items  
9.   Water Resistant 2 items
**My Wish List**
**Last Added Items**
1.   **** Add to CartAdd to Cart Remove This Item
Go to Wish List
You have no items in your wish list.
**TAMMEX**MEDICAL SUPPLIES  
Level 40 / 140 William Street Melbourne VIC 3000

# Search results for: 'box 2560 site'
### Shop
About UsShopping CartConditionsAdvanced Search

# Search results for: 'box 2560 site'
### Support
Contact usTrack an orderShipping & DeliveryReturns & RefundsAbout UsFAQ

# Search results for: 'box 2560 site'
### Account
Sign inCreate accountWishlistOrders
</excerpt>
### Rank 5 of 13 — 0.00
<excerpt title="Search results for: 'prep site point ash'">
# Search results for: 'prep site point ash'
### Popular Searches
**No matching products yet**Press Enter to search the full catalogue.
View all search results
My Cart
Skip to Content
Shop All CategoriesContact UsAbout UsMy AccountConditions
**Menu**
Shop All Categories›Contact Us›About Us›My Account›Conditions›My AccountMy Orders
‹**Shop All Categories**
Browse Categories
*   PPE  
*   Medical Furniture  
*   Monitoring & Diagnostics  
*   Consumables  
*   Laboratory Supplies
‹
**Category**View all →
Explore PPE
*   Face Coverings  
*   Medical Gloves  
*   Medical Gowns  
*   Scrubs
Browse Apparel
*   Apron Dispenser  
*   Disposable Apron  
*   Medical Gown  
*   Medical Hair Cap  
*   Medical Overshoe  
*   Modesty Wear  
*   Surgical Hood  
*   Theatre Cap
Explore Medical Furniture
*   Medical Carts  
*   Medical Lighting  
*   Examination Furniture  
*   Medical Trolleys  
*   Medical Privacy Screens  
*   Medical Stools
Medical Trolleys
*   Emergency Trolley  
*   Instrument Trolley  
*   Instrument Trolley + Draw  
*   Linen Trolley  
*   Oxygen Bottle Trolley
Medical Stools
*   AxisHealth  
*   Dalcross  
*   Paragon
Examanation Furniture
*   Examination Couch  
*   Medical Bed  
*   Medical Chair
Lighting
*   Diagnostics Torch  
*   Examination Room Lighting  
*   Loupe Lighting



*   Dermatoscope  
*   Otoscopes  
*   Ophthalmoscope  
*   Oximeters  
*   Patient Monitors  
*   Scales  
*   Stadiometers  
*   Stethoscopes  
*   Sphygmomanometers  
*   Thermometers
Patient Monitors
*   Blood Pressure Monitor  
*   ECG  
*   Vital Signs Monitor
Scales
*   Baby Scales  
*   Chair Scales  
*   Column Scales  
*   Flat Scales  
*   Handrail Scales
Browse Consumables
*   Medical Dressings  
*   Medical Hygiene  
*   Syringes  
*   Casting Supplies  
*   Blood Collection  
*   IV Fluids  
*   Kidney Dishes & Trays  
*   Skin Closure  
*   TRT
</excerpt>

## Search 7 — query: "site:productsafety.gov.au/recalls "Gas products and appliances" 2020/"
### Rank 1 of 1 — 0.18 (passed on)
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

## Search 8 — query: ""recalls" "2020" "Gas products and appliances" "productsafety.gov.au""
### Rank 1 of 10 — 0.16 (passed on)
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
### Rank 2 of 10 — 0.00
<excerpt title="Search results for: 'prep site point ash'">
# Search results for: 'prep site point ash'
The store will not work correctly when cookies are disabled.
Free shipping on orders over $99*Trusted by businesses nationwide Quick reorder & expert support Ships from the USA
Menu
Search
Searching...

# Search results for: 'prep site point ash'
### Products


# Search results for: 'prep site point ash'
### Categories


# Search results for: 'prep site point ash'
### Popular Searches
**No matching products yet**Press Enter to search the full catalogue.
View all search results
My Cart
Skip to Content
Shop All CategoriesContact UsAbout UsMy AccountConditions
**Menu**
Shop All Categories›Contact Us›About Us›My Account›Conditions›My AccountMy Orders
‹**Shop All Categories**
Browse Categories
*   PPE  
*   Medical Furniture  
*   Monitoring & Diagnostics  
*   Consumables  
*   Laboratory Supplies
‹
**Category**View all →
Explore PPE
*   Face Coverings  
*   Medical Gloves  
*   Medical Gowns  
*   Scrubs
Browse Apparel
*   Apron Dispenser  
*   Disposable Apron  
*   Medical Gown  
*   Medical Hair Cap  
*   Medical Overshoe  
*   Modesty Wear  
*   Surgical Hood  
*   Theatre Cap
Explore Medical Furniture
*   Medical Carts  
*   Medical Lighting  
*   Examination Furniture  
*   Medical Trolleys  
*   Medical Privacy Screens  
*   Medical Stools
Medical Trolleys
*   Emergency Trolley  
*   Instrument Trolley  
*   Instrument Trolley + Draw  
*   Linen Trolley  
*   Oxygen Bottle Trolley
Medical Stools
*   AxisHealth  
*   Dalcross  
*   Paragon
Examanation Furniture
*   Examination Couch  
*   Medical Bed  
*   Medical Chair
Lighting
*   Diagnostics Torch  
*   Examination Room Lighting  
*   Loupe Lighting



*   Dermatoscope  
*   Otoscopes  
*   Ophthalmoscope  
*   Oximeters  
*   Patient Monitors  
*   Scales  
*   Stadiometers  
*   Stethoscopes  
*   Sphygmomanometers  
*   Thermometers
Patient Monitors
*   Blood Pressure Monitor  
*   ECG  
*   Vital Signs Monitor
Scales
*   Baby Scales  
*   Chair Scales  
*   Column Scales  
*   Flat Scales  
*   Handrail Scales
Browse Consumables
*   Medical Dressings  
*   Medical Hygiene  
*   Syringes  
*   Casting Supplies  
*   Blood Collection  
*   IV Fluids  
*   Kidney Dishes & Trays  
*   Skin Closure  
*   TRT
</excerpt>
### Rank 3 of 10 — 0.00
<excerpt title="Search results for: 'site coat'">
# Search results for: 'site coat'
The store will not work correctly when cookies are disabled.
Free shipping on orders over $99*Trusted by businesses nationwide Quick reorder & expert support Ships from the USA
Menu
Search
Searching...

# Search results for: 'site coat'
### Products


# Search results for: 'site coat'
### Categories


# Search results for: 'site coat'
### Popular Searches
**No matching products yet**Press Enter to search the full catalogue.
View all search results
My Cart
Skip to Content
Shop All CategoriesContact UsAbout UsMy AccountConditions
**Menu**
Shop All Categories›Contact Us›About Us›My Account›Conditions›My AccountMy Orders
‹**Shop All Categories**
Browse Categories
*   PPE  
*   Medical Furniture  
*   Monitoring & Diagnostics  
*   Consumables  
*   Laboratory Supplies
‹
**Category**View all →
Explore PPE
*   Face Coverings  
*   Medical Gloves  
*   Medical Gowns  
*   Scrubs
Browse Apparel
*   Apron Dispenser  
*   Disposable Apron  
*   Medical Gown  
*   Medical Hair Cap  
*   Medical Overshoe  
*   Modesty Wear  
*   Surgical Hood  
*   Theatre Cap
Explore Medical Furniture
*   Medical Carts  
*   Medical Lighting  
*   Examination Furniture  
*   Medical Trolleys  
*   Medical Privacy Screens  
*   Medical Stools
Medical Trolleys
*   Emergency Trolley  
*   Instrument Trolley  
*   Instrument Trolley + Draw  
*   Linen Trolley  
*   Oxygen Bottle Trolley
Medical Stools
*   AxisHealth  
*   Dalcross  
*   Paragon
Examanation Furniture
*   Examination Couch  
*   Medical Bed  
*   Medical Chair
Lighting
*   Diagnostics Torch  
*   Examination Room Lighting  
*   Loupe Lighting



*   Dermatoscope  
*   Otoscopes  
*   Ophthalmoscope  
*   Oximeters  
*   Patient Monitors  
*   Scales  
*   Stadiometers  
*   Stethoscopes  
*   Sphygmomanometers  
*   Thermometers
Patient Monitors
*   Blood Pressure Monitor  
*   ECG  
*   Vital Signs Monitor
Scales
*   Baby Scales  
*   Chair Scales  
*   Column Scales  
*   Flat Scales  
*   Handrail Scales
Browse Consumables
*   Medical Dressings  
*   Medical Hygiene  
*   Syringes  
*   Casting Supplies  
*   Blood Collection  
*   IV Fluids  
*   Kidney Dishes & Trays  
*   Skin Closure  
*   TRT
</excerpt>
### Rank 4 of 10 — 0.00
<excerpt title="Search results for: 'site coat'">
# Search results for: 'site coat'
### Popular Searches
Phlebotomy Supplies
*   Blood Bags  
*   Blood Collection Needle  
*   Blood Collection Sets  
*   Blood Collection Syringe  
*   Blood Transfusion Sets  
*   Capillary Tubes  
*   Microtainer Tubes  
*   Vacutainer Holder  
*   Vacutainer Tubes
Browse Laboratory Supplies
*   Specimen Jars  
*   Pipettors  
*   Centrifuge  
*   Microscope Slides  
*   Cytology  
*   Waste Bags  
*   Swabs
Browse Microscope Slides
*   Blood Dispenser  
*   Coverslips  
*   Slide Mailer  
*   Slides  
*   Slides Pencil  
*   Spreader Bar  
*   Tray & Storage Box







*   Home  
*   **Search Results for "site coat"**
**Search Results for “site coat”**0 Items
**No matching products**Try another search term or remove some filters.
**Filter Products**Clear all
Active filters
1.   Category:Tammex MedicalRemove  
2.   Exudate Level:7102Remove  
3.   Dressing Shape:7176Remove
Category
Exudate Level
1.   Low 66 items  
2.   Moderate 94 items  
3.   Heavy 84 items
Dressing Shape
**My Wish List**
**Last Added Items**
1.   **** Add to CartAdd to Cart Remove This Item
Go to Wish List
You have no items in your wish list.
**TAMMEX**MEDICAL SUPPLIES  
Level 40 / 140 William Street Melbourne VIC 3000

# Search results for: 'site coat'
### Shop
About UsShopping CartConditionsAdvanced Search

# Search results for: 'site coat'
### Support
Contact usTrack an orderShipping & DeliveryReturns & RefundsAbout UsFAQ

# Search results for: 'site coat'
### Account
Sign inCreate accountWishlistOrders

# Search results for: 'site coat'
### Need help sourcing products?
Send us a quick message and we will help point you to the right range.
Contact support
© 2026 PilotTheme. All rights reserved.PrivacyTerms
R
−×
Find a product**›**Track my order**›**Talk to the team**›**
😊
😀  😃  😄  😁  😆  😅  😂  😊  🙂  🙃  😉  😍  🥰  😘  😎  🤩  🥳  😇  🤔  🤨  😐  😬  🙄  😴  😢  😭  😤  😡  🤯  😱  👍  👎  👏  🙌  👌  ✌️  💪  🙏  ❤️  💙  🎉  ✅  🔥  🚀  💯  👀  💡  ⭐  ✨
Powered by **◆ Pilot**
**Leave this chat?**  
This will disconnect the current conversation. You can start a new chat at any time.
No, stay Yes, leave
0
Google Rating**4.9**★★★★★Based on 330 reviews
</excerpt>
### Rank 5 of 10 — 0.00
<excerpt title="Search results for: 'prep site point ash'">
# Search results for: 'prep site point ash'
### Popular Searches
**No matching products yet**Press Enter to search the full catalogue.
View all search results
My Cart
Skip to Content
Shop All CategoriesContact UsAbout UsMy AccountConditions
**Menu**
Shop All Categories›Contact Us›About Us›My Account›Conditions›My AccountMy Orders
‹**Shop All Categories**
Browse Categories
*   PPE  
*   Medical Furniture  
*   Monitoring & Diagnostics  
*   Consumables  
*   Laboratory Supplies
‹
**Category**View all →
Explore PPE
*   Face Coverings  
*   Medical Gloves  
*   Medical Gowns  
*   Scrubs
Browse Apparel
*   Apron Dispenser  
*   Disposable Apron  
*   Medical Gown  
*   Medical Hair Cap  
*   Medical Overshoe  
*   Modesty Wear  
*   Surgical Hood  
*   Theatre Cap
Explore Medical Furniture
*   Medical Carts  
*   Medical Lighting  
*   Examination Furniture  
*   Medical Trolleys  
*   Medical Privacy Screens  
*   Medical Stools
Medical Trolleys
*   Emergency Trolley  
*   Instrument Trolley  
*   Instrument Trolley + Draw  
*   Linen Trolley  
*   Oxygen Bottle Trolley
Medical Stools
*   AxisHealth  
*   Dalcross  
*   Paragon
Examanation Furniture
*   Examination Couch  
*   Medical Bed  
*   Medical Chair
Lighting
*   Diagnostics Torch  
*   Examination Room Lighting  
*   Loupe Lighting



*   Dermatoscope  
*   Otoscopes  
*   Ophthalmoscope  
*   Oximeters  
*   Patient Monitors  
*   Scales  
*   Stadiometers  
*   Stethoscopes  
*   Sphygmomanometers  
*   Thermometers
Patient Monitors
*   Blood Pressure Monitor  
*   ECG  
*   Vital Signs Monitor
Scales
*   Baby Scales  
*   Chair Scales  
*   Column Scales  
*   Flat Scales  
*   Handrail Scales
Browse Consumables
*   Medical Dressings  
*   Medical Hygiene  
*   Syringes  
*   Casting Supplies  
*   Blood Collection  
*   IV Fluids  
*   Kidney Dishes & Trays  
*   Skin Closure  
*   TRT
</excerpt>

## Search 9 — query: "productsafety.gov.au/recalls 2020 "Gas products and appliances" "National""
(no page could be scored)

## Search 10 — query: ""Gas products and appliances" "2020" "productsafety.gov.au""
### Rank 1 of 12 — 0.13 (passed on)
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
### Rank 2 of 12 — 0.07
<excerpt title="Caravan and motorhome owners urged to check for deadly faulty water ...">
Consumers who experience difficulties obtaining a timely remedy should contact Coast to Coast Caravan and Leisure, their state or territory gas regulator or the ACCC online.

## Background
Coast to Coast Caravan and Leisure notified a recall for Suburban Recreational Vehicle Water Heaters on 15 November 2019 due to their serious safety hazards. 18,139 heaters have been sold across all states and territories in Australia mostly installed in caravans and RVs via certain caravan and motorhome retailers.
Gas regulators have been working with Coast to Coast Caravan and Leisure to identify a suitable safe replacement water heater. Replacement models initially proposed by Suburban, the overseas manufacturer, also failed testing. A safe model was finally produced, and approved for use in July 2020.
Remediation could not commence until the GTRC was satisfied of the safety of the replacement units. The supplier then needed to import sufficient units from the US manufacturer, at a time when their supply chains were impacted by the pandemic situation.
The supplier advises stocks of replacement units are now in hand and they are keen to get remediation happening quickly. To date, only 210 units have been remediated or scheduled for inspection, and the supplier would like to encourage greater consumer response to the recall.
The affected products are the Suburban Recreational Vehicle Water Heaters with model numbers SW6DEA, SW6DA, SW4DEA, SW4DA, SW4DECA, SW6DECA and SW6PA that have serial numbers between 181315552 and 193002648 (some serial numbers may end with a 'D') and between 8183311827 and 8190201139. They were manufactured between 4 April 2018 and 1 August 2019.
The Office of the Technical Regulator (SA) is the responsible regulator for this product. It is a member of the Gas Technical Regulators Committee (GTRC). The GTRC is composed of gas technical and safety regulators across Australia and aims to apply a consistent regulatory approach to improve gas safety, measurement and quality.
More information is available at Coast to Coast Caravan and Leisure — Suburban Recreational Vehicle Water Heaters Model SW6PA, SW6DEA, SW6DA, SW4DEA, SW4DA, SW4DECA and SW6DECA.
**Media enquiries:**

## Background
Media team - 1300 138 917
</excerpt>
### Rank 3 of 12 — 0.03
<excerpt title="Caravan and motorhome owners urged to check for deadly faulty water ...">
Consumers are urged to check their caravans and recreational vehicles (RVs) for dangerous Suburban-branded water heaters which may emit deadly carbon monoxide.
The Suburban Recreational Vehicle water heater can operate using electricity or gas, and may produce unsafe levels of carbon monoxide when gas is used to generate the heat.
Carbon monoxide poisoning can cause death, and exposure for a short amount of time can lead to serious injuries. Carbon monoxide has no smell and is unlikely to be detected. It is also highly flammable and can explode on contact with a spark or flame.
The Gas Technical Regulators Committee (GTRC), with the ACCC’s assistance, is raising awareness of the need for repair of thousands of water heaters.
“Do not use the affected water heaters in gas mode under any circumstances,” ACCC Deputy Chair Delia Rickard said.
“It’s especially important to check your caravan’s water heater as soon as possible if you plan to go away during the summer holidays. It only takes a minute and it could save the lives of your loved ones.”
“We are concerned that a large number of deadly heaters remain in caravans and RVs because owners have not yet contacted Coast to Coast for an inspection. Coast to Coast Caravan and Leisure has recalled these heaters due to the serious hazards they present. Owners should not take this issue lightly and act quickly,” Ms Rickard said.
Consumers can check if their heater is affected by opening the exterior access door to the hot water service and checking the model and serial number located on the right hand side. They should then enter the serial number at the Coast to Coast website.
“Anyone with an affected water heater should urgently contact Coast to Coast Caravan and Leisure on 02 9645 7685 who will arrange for a licensed gas fitter to inspect their water heater free of charge,” Ms Rickard said.
Consumers will not have to cover any costs related to the supply and installation of the new water heater, or any required associated work, such as the modification of cavity and gas and/or water lines.
Coast to Coast Caravan and Leisure will check every unit, after being contacted by consumers, to ensure the water heater is properly installed and if needed, will replace the unit through a licenced gasfitter free of charge.

Consumers who experience difficulties obtaining a timely remedy should contact Coast to Coast Caravan and Leisure, their state or territory gas regulator or the ACCC online.
</excerpt>
### Rank 4 of 12 — 0.00
<excerpt title="Search results for: 'prep site point ash'">
# Search results for: 'prep site point ash'
### Popular Searches
**No matching products yet**Press Enter to search the full catalogue.
View all search results
My Cart
Skip to Content
Shop All CategoriesContact UsAbout UsMy AccountConditions
**Menu**
Shop All Categories›Contact Us›About Us›My Account›Conditions›My AccountMy Orders
‹**Shop All Categories**
Browse Categories
*   PPE  
*   Medical Furniture  
*   Monitoring & Diagnostics  
*   Consumables  
*   Laboratory Supplies
‹
**Category**View all →
Explore PPE
*   Face Coverings  
*   Medical Gloves  
*   Medical Gowns  
*   Scrubs
Browse Apparel
*   Apron Dispenser  
*   Disposable Apron  
*   Medical Gown  
*   Medical Hair Cap  
*   Medical Overshoe  
*   Modesty Wear  
*   Surgical Hood  
*   Theatre Cap
Explore Medical Furniture
*   Medical Carts  
*   Medical Lighting  
*   Examination Furniture  
*   Medical Trolleys  
*   Medical Privacy Screens  
*   Medical Stools
Medical Trolleys
*   Emergency Trolley  
*   Instrument Trolley  
*   Instrument Trolley + Draw  
*   Linen Trolley  
*   Oxygen Bottle Trolley
Medical Stools
*   AxisHealth  
*   Dalcross  
*   Paragon
Examanation Furniture
*   Examination Couch  
*   Medical Bed  
*   Medical Chair
Lighting
*   Diagnostics Torch  
*   Examination Room Lighting  
*   Loupe Lighting



*   Dermatoscope  
*   Otoscopes  
*   Ophthalmoscope  
*   Oximeters  
*   Patient Monitors  
*   Scales  
*   Stadiometers  
*   Stethoscopes  
*   Sphygmomanometers  
*   Thermometers
Patient Monitors
*   Blood Pressure Monitor  
*   ECG  
*   Vital Signs Monitor
Scales
*   Baby Scales  
*   Chair Scales  
*   Column Scales  
*   Flat Scales  
*   Handrail Scales
Browse Consumables
*   Medical Dressings  
*   Medical Hygiene  
*   Syringes  
*   Casting Supplies  
*   Blood Collection  
*   IV Fluids  
*   Kidney Dishes & Trays  
*   Skin Closure  
*   TRT
</excerpt>
### Rank 5 of 12 — 0.00
<excerpt title="Search results for: 'prep site point ash'">
# Search results for: 'prep site point ash'
The store will not work correctly when cookies are disabled.
Free shipping on orders over $99*Trusted by businesses nationwide Quick reorder & expert support Ships from the USA
Menu
Search
Searching...

# Search results for: 'prep site point ash'
### Products


# Search results for: 'prep site point ash'
### Categories


# Search results for: 'prep site point ash'
### Popular Searches
**No matching products yet**Press Enter to search the full catalogue.
View all search results
My Cart
Skip to Content
Shop All CategoriesContact UsAbout UsMy AccountConditions
**Menu**
Shop All Categories›Contact Us›About Us›My Account›Conditions›My AccountMy Orders
‹**Shop All Categories**
Browse Categories
*   PPE  
*   Medical Furniture  
*   Monitoring & Diagnostics  
*   Consumables  
*   Laboratory Supplies
‹
**Category**View all →
Explore PPE
*   Face Coverings  
*   Medical Gloves  
*   Medical Gowns  
*   Scrubs
Browse Apparel
*   Apron Dispenser  
*   Disposable Apron  
*   Medical Gown  
*   Medical Hair Cap  
*   Medical Overshoe  
*   Modesty Wear  
*   Surgical Hood  
*   Theatre Cap
Explore Medical Furniture
*   Medical Carts  
*   Medical Lighting  
*   Examination Furniture  
*   Medical Trolleys  
*   Medical Privacy Screens  
*   Medical Stools
Medical Trolleys
*   Emergency Trolley  
*   Instrument Trolley  
*   Instrument Trolley + Draw  
*   Linen Trolley  
*   Oxygen Bottle Trolley
Medical Stools
*   AxisHealth  
*   Dalcross  
*   Paragon
Examanation Furniture
*   Examination Couch  
*   Medical Bed  
*   Medical Chair
Lighting
*   Diagnostics Torch  
*   Examination Room Lighting  
*   Loupe Lighting



*   Dermatoscope  
*   Otoscopes  
*   Ophthalmoscope  
*   Oximeters  
*   Patient Monitors  
*   Scales  
*   Stadiometers  
*   Stethoscopes  
*   Sphygmomanometers  
*   Thermometers
Patient Monitors
*   Blood Pressure Monitor  
*   ECG  
*   Vital Signs Monitor
Scales
*   Baby Scales  
*   Chair Scales  
*   Column Scales  
*   Flat Scales  
*   Handrail Scales
Browse Consumables
*   Medical Dressings  
*   Medical Hygiene  
*   Syringes  
*   Casting Supplies  
*   Blood Collection  
*   IV Fluids  
*   Kidney Dishes & Trays  
*   Skin Closure  
*   TRT
</excerpt>

# Example 4
## Question
There was a space shuttle flight that launched two days before the original U.S. release date of an episode of The Office that was directed by Jason Reitman. Which member of the crew of this flight was born on the same day as someone who was the head coach of a professional NBA basketball team before 2022? The basketball team was founded after 1988 and was based in the same state the space shuttle flight launched from.

## Expected answer
Pamela Melroy

## Grade 0.00

## Search 1 — query: "Jason Reitman directed episode of The Office""
### Rank 1 of 38 — 0.84 (passed on)
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
### Rank 2 of 38 — 0.81
<excerpt title="Jason Reitman">
| Year | Title | Director | Writer | Producer |  
| --- | --- | --- | --- | --- |  
| 2005 | _Thank You for Smoking_ | Yes | Yes | No |  
| 2007 | _Juno_ | Yes | No | No |  
| 2009 | _Up in the Air_ | Yes | Yes | Yes |  
| 2011 | _Young Adult_ | Yes | No | Yes |  
| 2013 | _Labor Day_ | Yes | Yes | Yes |  
| 2014 | _Men, Women & Children_ | Yes | Yes | Yes |  
| 2018 | _Tully_ | Yes | No | Yes |  
| _The Front Runner_ | Yes | Yes | Yes |  
| 2021 | _Ghostbusters: Afterlife_ | Yes | Yes | No |  
| 2024 | _Ghostbusters: Frozen Empire_ | No | Yes | Yes |  
| _Saturday Night_ | Yes | Yes | Yes |  
|  |
**Acting roles**
| Year | Title | Role |  
| --- | --- | --- |  
| 1988 | _Twins_ | Granger Grandson |  
| 1989 | _Ghostbusters II_ | Brownstone Boy #2 |  
| 1990 | _Kindergarten Cop_ | Kissing Boy |  
| 1993 | _Dave_ | Vice-president's Son |  
| 1997 | _[Fathers' Day](https://en.wikipedia.org/wiki/Fathers'\_Day\_(1997\_film) "Fathers' Day (1997 film)")_ | Wrong Kid in Alley |
| Year | Title | Notes |  
| --- | --- | --- |  
| 2007–2008 | _The Office_ | Episodes "Local Ad" and "Frame Toby" |  
| 2015 | _Casual_ | Also executive producer |  
| 2020 | _Home Movie: The Princess Bride_ | Miniseries |

## Awards and nominations
[edit]
**Academy Awards**
| Year | Title | Category | Result |  
| --- | --- | --- | --- |  
| 2008 | _Juno_ | Best Director | Nominated |  
| 2010 | _Up in the Air_ | Best Picture | Nominated |  
| Best Director | Nominated |  
| Best Adapted Screenplay | Nominated |
**BAFTA Awards**
| Year | Title | Category | Result |  
| --- | --- | --- | --- |  
| 2010 | _Up in the Air_ | Best Film | Nominated |  
| Best Adapted Screenplay | Won |
**Golden Globe Awards**
| Year | Title | Category | Result |  
| --- | --- | --- | --- |  
| 2010 | _Up in the Air_ | Best Director | Nominated |  
| Best Screenplay | Won |
**Other awards**
**Directed Academy Award performances**
| Year | Performer | Film | Result |  
| --- | --- | --- | --- |  
| **Academy Award for Best Actor** |  
| 2010 | George Clooney | _Up in the Air_ | Nominated |  
| **Academy Award for Best Actress** |  
| 2008 | Elliot Page[[a]](https://en.wikipedia.org/wiki/Jason_Reitman#cite_note-Elliot-40) | _Juno_ | Nominated |  
| **Academy Award for Best Supporting Actress** |  
| 2010 | Vera Farmiga | _Up in the Air_ | Nominated |  
| Anna Kendrick | Nominated |
*   List of oldest and youngest Academy Award winners and nominees — youngest nominees for Best Director  
*   List of Jewish Academy Award winners and nominees
1.   ↑Credited as Ellen Page
</excerpt>
### Rank 3 of 38 — 0.80
<excerpt title="Jason Reitman">
On October 11, 2024, Reitman directed and co-wrote alongside Kenan _Saturday Night_, a comedy biopic about the events directly preceding the live broadcast of _Saturday Night Live_'s first episode on October 11, 1975. Canadian comedian Dan Aykroyd was a member of that _SNL_ cast and describes the film as a "stand alone masterpiece."[[32]](https://en.wikipedia.org/wiki/Jason_Reitman#cite_note-32)
Reitman in 2012
Before his feature film career began, Jason Reitman wrote and directed six short films. He financed his first short film, _Operation_, with money he made by selling ads in desk calendars. The film premiered at the Sundance Film Festival in 1998.[[33]](https://en.wikipedia.org/wiki/Jason_Reitman#cite_note-advocates-33) He was a guest on _The Howard Stern Show_ on April 10, 2008; when he was asked if he would direct _Ghostbusters III_ and cast Howard, he said: "Do you know how many times I get asked if I want to do _Ghostbusters III_? Looking at my career so far, I mean, if you just looked at my two films, I would make the most boring _Ghostbusters_ movie. It would just be people talking about ghosts, there wouldn't be any ghost-busting in it." Stern, a friend of Ivan Reitman, also revealed that he had seen Jason's early short films and was impressed enough to offer him the opportunity to direct an episode of _Son of the Beach_ (a TV series he produced, a goofy parody of _Baywatch_), which Jason declined, citing that he was busy obtaining financing for _Thank You for Smoking_ at the time.

Reitman produced and directed the 2007 holiday season commercials for Wal-Mart with advertising agency Bernstein-Rein. He has also directed ads for Burger King, Nintendo, BMW and Buick.[[33]](https://en.wikipedia.org/wiki/Jason_Reitman#cite_note-advocates-33) In television, Reitman directed two episodes of _The Office_: "Local Ad" and "Frame Toby". Reitman also directed a three-part pretaped sketch for the NBC show _Saturday Night Live_ called "Death by Chocolate," about a walking candy bar, played by episode host Ashton Kutcher, who murders people; stabbing a homeless man, shooting a doctor, cutting off a life support machine on a coma victim and slicing Andy Samberg (dressed as a lumberjack) with a chainsaw. Since 2011, Reitman has directed the _Live Read_ series, a monthly live staged reading of film scripts as part of the Film Independent at LACMA.[[34]](https://en.wikipedia.org/wiki/Jason_Reitman#cite_note-LiveRead-34) In 2020, Reitman directed _The Princess Bride_, a television adaptation of novel of the same name for Quibi featuring an ensemble cast to raise money for World Central Kitchen.[[35]](https://en.wikipedia.org/wiki/Jason_Reitman#cite_note-35)
Reitman is a self-described libertarian.[[36]](https://en.wikipedia.org/wiki/Jason_Reitman#cite_note-36) He is a dual citizen of Canada and the United States. When Reitman was 16 and still in high school, he moved in with a woman 10 years his senior. They separated after 7 years.[[2]](https://en.wikipedia.org/wiki/Jason_Reitman#cite_note-WTF-Maron-2014-2)
</excerpt>
### Rank 4 of 38 — 0.77
<excerpt title="Jason Reitman">
Reitman produced and directed the 2007 holiday season commercials for Wal-Mart with advertising agency Bernstein-Rein. He has also directed ads for Burger King, Nintendo, BMW and Buick.[[33]](https://en.wikipedia.org/wiki/Jason_Reitman#cite_note-advocates-33) In television, Reitman directed two episodes of _The Office_: "Local Ad" and "Frame Toby". Reitman also directed a three-part pretaped sketch for the NBC show _Saturday Night Live_ called "Death by Chocolate," about a walking candy bar, played by episode host Ashton Kutcher, who murders people; stabbing a homeless man, shooting a doctor, cutting off a life support machine on a coma victim and slicing Andy Samberg (dressed as a lumberjack) with a chainsaw. Since 2011, Reitman has directed the _Live Read_ series, a monthly live staged reading of film scripts as part of the Film Independent at LACMA.[[34]](https://en.wikipedia.org/wiki/Jason_Reitman#cite_note-LiveRead-34) In 2020, Reitman directed _The Princess Bride_, a television adaptation of novel of the same name for Quibi featuring an ensemble cast to raise money for World Central Kitchen.[[35]](https://en.wikipedia.org/wiki/Jason_Reitman#cite_note-35)
Reitman is a self-described libertarian.[[36]](https://en.wikipedia.org/wiki/Jason_Reitman#cite_note-36) He is a dual citizen of Canada and the United States. When Reitman was 16 and still in high school, he moved in with a woman 10 years his senior. They separated after 7 years.[[2]](https://en.wikipedia.org/wiki/Jason_Reitman#cite_note-WTF-Maron-2014-2)

In 2000, when he was 23, Reitman and his next-door neighbor, writer Michele Lee began dating. They co-wrote the 2004 comedic short _Consent_.[[37]](https://en.wikipedia.org/wiki/Jason_Reitman#cite_note-37) Their daughter, Josie, was born in 2006.[[38]](https://en.wikipedia.org/wiki/Jason_Reitman#cite_note-NYDailyNews-2011-38) After 10 years of marriage, Reitman filed for divorce in June 2011 and as of 2014 is divorced.[[2]](https://en.wikipedia.org/wiki/Jason_Reitman#cite_note-WTF-Maron-2014-2)[[38]](https://en.wikipedia.org/wiki/Jason_Reitman#cite_note-NYDailyNews-2011-38) Reitman is currently in a relationship with Lorraine Nicholson.[[39]](https://en.wikipedia.org/wiki/Jason_Reitman#cite_note-39)
| Year | Title | Director | Writer | Producer | Actor | Role | Notes |  
| --- | --- | --- | --- | --- | --- | --- | --- |  
| 1998 | _Operation_ | Yes | Yes | Yes | Yes | Woodsy Freedom Fighter |  |  
| 1999 | _H@_ | Yes | Yes | No | No |  |  |  
| 2000 | _In God We Trust_ | Yes | Yes | executive | Yes | W.F.F. |  |  
| 2001 | _Gulp_ | Yes | Yes | No | No |  |  |  
| 2002 | _Uncle Sam_ | Yes | Yes | No | No |  | Documentary short |  
| 2004 | _Consent_ | Yes | Yes | No | No |  |  |  
|  |
</excerpt>
### Rank 5 of 38 — 0.77
<excerpt title="Jason Reitman">
In 2000, when he was 23, Reitman and his next-door neighbor, writer Michele Lee began dating. They co-wrote the 2004 comedic short _Consent_.[[37]](https://en.wikipedia.org/wiki/Jason_Reitman#cite_note-37) Their daughter, Josie, was born in 2006.[[38]](https://en.wikipedia.org/wiki/Jason_Reitman#cite_note-NYDailyNews-2011-38) After 10 years of marriage, Reitman filed for divorce in June 2011 and as of 2014 is divorced.[[2]](https://en.wikipedia.org/wiki/Jason_Reitman#cite_note-WTF-Maron-2014-2)[[38]](https://en.wikipedia.org/wiki/Jason_Reitman#cite_note-NYDailyNews-2011-38) Reitman is currently in a relationship with Lorraine Nicholson.[[39]](https://en.wikipedia.org/wiki/Jason_Reitman#cite_note-39)
| Year | Title | Director | Writer | Producer | Actor | Role | Notes |  
| --- | --- | --- | --- | --- | --- | --- | --- |  
| 1998 | _Operation_ | Yes | Yes | Yes | Yes | Woodsy Freedom Fighter |  |  
| 1999 | _H@_ | Yes | Yes | No | No |  |  |  
| 2000 | _In God We Trust_ | Yes | Yes | executive | Yes | W.F.F. |  |  
| 2001 | _Gulp_ | Yes | Yes | No | No |  |  |  
| 2002 | _Uncle Sam_ | Yes | Yes | No | No |  | Documentary short |  
| 2004 | _Consent_ | Yes | Yes | No | No |  |  |  
|  |

| Year | Title | Director | Writer | Producer |  
| --- | --- | --- | --- | --- |  
| 2005 | _Thank You for Smoking_ | Yes | Yes | No |  
| 2007 | _Juno_ | Yes | No | No |  
| 2009 | _Up in the Air_ | Yes | Yes | Yes |  
| 2011 | _Young Adult_ | Yes | No | Yes |  
| 2013 | _Labor Day_ | Yes | Yes | Yes |  
| 2014 | _Men, Women & Children_ | Yes | Yes | Yes |  
| 2018 | _Tully_ | Yes | No | Yes |  
| _The Front Runner_ | Yes | Yes | Yes |  
| 2021 | _Ghostbusters: Afterlife_ | Yes | Yes | No |  
| 2024 | _Ghostbusters: Frozen Empire_ | No | Yes | Yes |  
| _Saturday Night_ | Yes | Yes | Yes |  
|  |
**Acting roles**
| Year | Title | Role |  
| --- | --- | --- |  
| 1988 | _Twins_ | Granger Grandson |  
| 1989 | _Ghostbusters II_ | Brownstone Boy #2 |  
| 1990 | _Kindergarten Cop_ | Kissing Boy |  
| 1993 | _Dave_ | Vice-president's Son |  
| 1997 | _[Fathers' Day](https://en.wikipedia.org/wiki/Fathers'\_Day\_(1997\_film) "Fathers' Day (1997 film)")_ | Wrong Kid in Alley |
| Year | Title | Notes |  
| --- | --- | --- |  
| 2007–2008 | _The Office_ | Episodes "Local Ad" and "Frame Toby" |  
| 2015 | _Casual_ | Also executive producer |  
| 2020 | _Home Movie: The Princess Bride_ | Miniseries |
</excerpt>

## Search 2 — query: "Space shuttle launch October 23 2007"
### Rank 1 of 118 — 0.73 (passed on)
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
### Rank 2 of 118 — 0.70
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
### Rank 3 of 118 — 0.66
<excerpt title="October 23 - on this day in 2007, Discovery launched to the ...">
# October 23 - on this day in 2007,... - NASASpaceflight.com | Facebook
## NASASpaceflight.com's Post
October 23 - on this day in 2007, Discovery launched to the [International Space Station](https://www.facebook.com/ISS?__cft__[0]=AZh2ObtPj4RioWQunsylB9cv1aIsgJwK_nM7OxQ49mM4gd8aCtYFk1-1dHVRpMYOWCXpb3lH8R8SDLtBYpSpMNe77S_4NyxXsZPpFvdDTkBlJP3hrdriloxl5Y75o3Y4yWSZPcapqVBP4XzrYr88CUElBwy4VEhx&__tn__=-]K-R) for the STS-120 mission, with liftoff taking place from Launch Complex 39A at [NASA's Kennedy Space Center](https://www.facebook.com/NASAKennedy?__cft__[0]=AZh2ObtPj4RioWQunsylB9cv1aIsgJwK_nM7OxQ49mM4gd8aCtYFk1-1dHVRpMYOWCXpb3lH8R8SDLtBYpSpMNe77S_4NyxXsZPpFvdDTkBlJP3hrdriloxl5Y75o3Y4yWSZPcapqVBP4XzrYr88CUElBwy4VEhx&__tn__=-]K-R).
The Space Shuttle docked to the Destiny module for almost eleven days, delivering the Harmony module and other equipment to the orbital outpost.

# October 23 - on this day in 2007,... - NASASpaceflight.com | Facebook
## NASASpaceflight.com's Post
Discovery's launching and landing crew included Commander Pamela Melroy, Pilot George Zamka, and Mission Specialists, Douglas Wheelock, Stephanie Wilson, Scott Parazynski, and [ESA - European Space Agency](https://www.facebook.com/EuropeanSpaceAgency?__cft__[0]=AZh2ObtPj4RioWQunsylB9cv1aIsgJwK_nM7OxQ49mM4gd8aCtYFk1-1dHVRpMYOWCXpb3lH8R8SDLtBYpSpMNe77S_4NyxXsZPpFvdDTkBlJP3hrdriloxl5Y75o3Y4yWSZPcapqVBP4XzrYr88CUElBwy4VEhx&__tn__=-]K-R)'s Paolo Nespoli. For launch, the seventh seat was occupied by Daniel Tani, while for landing, it was taken by Clayton Anderson.
[](https://www.facebook.com/photo/?fbid=1798500188942677&set=a.529406782518697&__cft__[0]=AZh2ObtPj4RioWQunsylB9cv1aIsgJwK_nM7OxQ49mM4gd8aCtYFk1-1dHVRpMYOWCXpb3lH8R8SDLtBYpSpMNe77S_4NyxXsZPpFvdDTkBlJP3hrdriloxl5Y75o3Y4yWSZPcapqVBP4XzrYr88CUElBwy4VEhx&__tn__=EH-R)
![Image 3](blob:http://localhost/85d8b181a20aeb64a3afc2f1c39d2480)
</excerpt>
### Rank 4 of 118 — 0.65
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
### Rank 5 of 118 — 0.64
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

## Search 3 — query: "STS-120 crew list Pamela Melroy Michael Barr James van Hoften"
### Rank 1 of 1481 — 0.69 (passed on)
<excerpt title="20130010436.pdf">
## [PDF page 83]
Space Shuttle Processing Status Report  
Space Shuttle Processing Status Report #S-051107. Mission: STS-117 - 21st International  
Space Station Flight (13A) - S3/S4 Truss Segment Solar Arrays; Vehicle: Atlantis (OV-104);  
Location: Vehicle Assembly Building; Launch Date: Targeted for June 8, 2007; Launch Pad:  
39A; Crew: Sturckow, Archambault, Reilly, Swanson, Forrester, Olivas and Anderson;  
Inclination/Orbit Altitude: 51.6 degrees/122 nautical miles. In high bay No. I of the  
Vehicle Assembly Building, repairs to the foam on the hail-damaged external fuel tank ET-  
124 are nearly complete, and technicians and engineers are preparing Atlantis for its rollout  
to Launch Pad 39A, currently scheduled for May 16. Atlantis' three main engines, which  
were removed last week to allow for inspection of the  flow liners, have all been reinstalled,  
and fmal checkout and testing are under way.  Mission: STS-118 - 22nd International Space  
Station Flight (13A.l) - S5 Truss Segment; Vehicle: Endeavour (OV-105); Location: Orbiter  
Processing Facility Bay 2; Launch Date: Targeted for Aug. 9, 2007; Launch Pad: 39A; Crew:  
Kelly, Hobaugh, Williams, Morgan, Mastracchio, Caldwell and Drew; Inclination/Orbit  
Altitude: 51.6 degrees/I 22 nautical miles. Members of the STS-I 18 crew are in Orbiter  
Processing Facility bay No. 2 today and will be there Saturday for the crew equipment  
interface test. The test provides an opportunity for the crew to review equipment in the crew  
cabin and cargo bay of the orbiter, and to review in-flight maintenance procedures. Earlier  
in the week, technicians installed the tunnel adapter, which is located in the midbody  
between the external airlock and a container used to transport experiments and cargo.  
Completion of the installation signifies closeout of the orbiter's midbody. Technicians  

## [PDF page 83]
continued work this week on modifications to the orbiter's engine cutoff sensor wiring.
77

## [PDF page 84]
Work also continues on closeout of the orbiter maneuvering system and the orb'iter aft.  
Mission: STS-120 - 23rd International Space Station Flight (IOA) - U.S. Node 2; Vehicle:  
Discovery (OV-103); Location: Orbiter Processing Facility Bay 3; Launch Date: Targeted for  
Oct. 20, 2007; Launch Pad: 39A; Crew: Meiroy, Zamka, Parazynski, Wheelock, Wilson,  
Nespoli and Tam; Inclination/Orbit Altitude: 51.6 degrees/122 nautical miles. In Orbiter  
Processing Facility bay No. 3, workers continue modifications to the orbiter's engine cutoff  
sensor wiring. Functional testing of the atmospheric revitalization pressure control system,  
part of the orbiter's life support system, is under way. Workers are also preparing for  
servicing of the ammonia boiler, which is a heat exchanger that helps cool the hydraulic  
system. Web posted. (2007). [NASA's Space Shuttle Processing Status Report [Online].  
Available W'\V: http: / /www.nasa.gov/ centers / kennedy /shutdeoperations /status /  
2007/index.html [2007, May 11.]
</excerpt>
### Rank 2 of 1481 — 0.66
<excerpt title="20130010436.pdf">
## [PDF page 137]
Space Shuttle Processing Status Report  
Space Shuttle Processing Status Report #S-070607. Mission: ST S-118 - 22nd International  
Space Station Flight (13A.1) - S5 Truss Segment; Vehicle: Endeavour (OV-105); Location:  
Vehicle Assembly Building; Launch Date Targeted for Aug. 7, 2007; Launch Pad: 39A;  
Crew: Kelly, Hobaugh, Wiffiams, Morgan, Mastracchio, Caldwell and Drew; Inclination  
/Orbit Altitude: 51.6 degrees/122 nautical miles. On Monday morning, Endeavour rolled  
from Orbiter Processing Facility bay No. 2 to the Vehicle Assembly Building. On Tuesday,  
the orbiter was transferred via crane from the VAB transfer aisle to high bay No. I and  
attached to the external fuel tank/solid rocket booster stack. Mating and launch processing  
operations are under way in preparation for a rollout to Launch Pad 39A, which is currently  
targeted for no earlier than July 10. The STS-1 18 payload will be transferred to Launch Pad
131

## [PDF page 138]
39A early Saturday, weather permitting. Mission: STS-120 - 23rd International Space  
Station Flight (IOA) - U.S. Node 2; Vehicle: Discovery (OV-103); Location: Orbiter  
Processing Facility Bay 3; Launch Date: Targeted for Oct. 20, 2007; Launch Pad: 39A; Crew:  
Meiroy, Zamka, Parazynski, Wheelock, Wilson, Nespoli and Tarn; Inclination/Orbit  
Altitude: 51.6 degrees/122 nautical miles. In Orbiter Processing Facility bay No. 3, aft  
closeout work continues. The orbiter boom sensor system, which is the 50-foot robotic arm  
extension, was delivered to the bay this week and is being installed today. Floodlight  
electronic assemblies No. I and 2 were installed and mated this week. These units control  
the lights in the payload bay. Testing of the auxiliary power units is complete, along with  
testing of the external tank doors for proper closure and fit. Mission: STS-122 - 24th  
International Space Station Flight (IE) - Columbus Module; Vehicle: Atlantis (OV-104);  
Location: Orbiter Processing Facility Bay 1; Launch Date: Targeted for Dec. 6, 2007; Launch  
Pad: 39A; Crew: Frick, Poindexter, Schiegel, Eyharts, Love, Melvin and Waiheim; Inclination  
/Orbit Altitude: 51.6 degrees/122 nautical miles. Atlantis returned to Kennedy Space  
Center from the Dryden Flight Research Center landing site on Tuesday at 8:24 am. aboard  
the Shuttle Carrier Aircraft, a modified Boeing 747 airplane. The orbiter was demated from  
the aircraft and towed to Orbiter Processing Facility bay 1, arriving just after 5 p.m. on  
Wednesday following several weather delays. Operations are under way to remove the tail  
cone, which was installed for protection during the ferry flight. Window inspections are  
complete and soft covers have been installed. Workers are inspecting the orbiter's thermal  
protection system, including the wing leading edge reinforced carbon-carbon panels, as well
</excerpt>
### Rank 3 of 1481 — 0.65
<excerpt title="20130010436.pdf">
## [PDF page 178]
several other tasks will be completed. Mission: STS-120 - 23rd International Space Station  
Flight - U.S. Node 2; Vehicle: Discovery (OV-103); Location: Orbiter Processing Facility  
Bay 3; Launch Date: Targeted for Oct. 23, 2007; Launch Pad: 39A; Crew: Me]roy, Zamka,  
Parazynski, Wheelock, Wilson, Nespoli and Tam; Inclination/Orbit Altitude: 51.6  
degrees/122 nautical miles. In Orbiter Processing Facility bay No. 3 this week, forward,  
midbody and aft closeout work continues. The auxiliary power unit tank pressurization is  
complete. Freon coolant loop No. I and 2 top-off and sampling is finished. Technicians  
performed hydraulic operations to position the shuttle main engines for rollover. Testing of  
the orbital maneuvering system flight controls and gimbal system was successful. Functional  
testing of the radiators, located on the payload bay doors, is under way. Stacking of the  
STS-120 solid rocket boosters in the Vehicle Assembly Building is complete and closeout  
work is under way. Mission: STS-122 - 24th International Space Station Flight - Columbus  
Module; Vehicle: Atlantis (OV-104); Location: Orbiter Processing Facility Bay 1; Launch  
Date: Targeted for Dec. 6, 2007; Launch Pad: 39A; Crew: Frick, Poindexter, Schlegel,  
Eyharts, Love, Melvin and Watheim; Inclination/Orbit Altitude: 51.6 degrees/122 nautical  
miles. In Orbiter Processing Facility bay No. 1, work began this week on modifications to  
the orbiter's engine cutoff sensor wiring, which involves rerouting new wires and installing  
new resistors. Workers also continued installing new, stronger tiles, known as BRI tiles,  
around the main landing gear doors. Installation of the main propulsion system tanks is  
under way. Removal of the left-hand orbital maneuvering system pod to allow for a valve  
replacement is scheduled for later today. Web posted. (2007). [NASA's Space Shuttle
</excerpt>
### Rank 4 of 1481 — 0.65
<excerpt title="20130010436.pdf">
## [PDF page 90]
May 18:  Space Shuttle Processing Status Report  
Space Shuttle Processing Status Report #S-051807.  Mission: STS-117 - 21st International  
Space Station Flight (13A) - S3/S4 Truss Segment Solar Arrays; Vehicle: Atlantis (OV-1Q4);  
Location: Launch Pad 39A; Launch Date: Targeted for June 8, 2007; Crew: Sturckow,  
Archambault, Reilly, Swanson, Forrester, Olivas and Anderson; Inclination/Orbit Altitude:  
51.6 degrees/122 nautical miles. Space Shuttle Atlantis arrived back at Launch Pad 39A on  
Tuesday, following repairs to the foam on its hail-damaged external fuel tank. Mission STS-  
117 was originally targeted for launch in mid-March, before a severe thunderstorm in late  
February generated hail that pelted the tank, ET-124. Pad operations are proceeding on  
schedule. Launch pad validation is complete, and the S3/S4 payload has been installed in  
Atlantis' payload bay. Preparations have begun for hypergolic propellant loading, which is  
scheduled for next week. The orbiter weather protection curtain walls have been extended,  
providing additional protection to the vehicle. Mission: STS-118 - 22nd International  
Space Station Flight (13A.I) - S5 Truss Segment; Vehicle: Endeavour (OV-105)  
Location: Orbiter Processing Facility Bay 2; Launch Date: Targeted for Aug. 9, 2007; Launch  
Pad: 39A ; Crew: Kelly, Hobaugh, Williams, Morgan, Mastracchio, Caldwell and Drew;  
Inclination/Orbit Altitude: 51.6 degrees/I 22 nautical miles. Members of the STS-I 18 flight  
crew completed the crew equipment interface test last week, reviewing equipment in  
Endeavour's crew cabin and payload bay. Leak checks have been completed between the
84

## [PDF page 91]
crew module, airlock and tunnel adapter. The orbiter docking system centerline cameras,  
used during rendezvous and docking with the International Space Station, have been aligned.  
Technicians continue working to close out the orbiter  aft, the midbody and the left and right  
wings. Hydraulic operations are under way for aerosurface and landing gear positioning.  
Mission: STS-120 - 23rd International Space Station Flight (10A) - U.S. Node 2; Vehicle:  
Discovery (OV-103); Location: Orbiter Processing Facility Bay 3; Launch Date: Targeted for  
Oct. 20, 2007; Launch Pad: 39A; Crew: Meiroy, Zamka, Parazynski, Wheelock, Wilson,  
Nespoli and Tarn; Inclination/Orbit Altitude: 51.6 degrees/122 nautical miles. Servicing of  
the ammonia boiler system, a heat exchanger that helps cool the hydraulic system, was  
completed early this week. The drag chute, which helps slow the orbiter after landing on the  
runway, was installed. Functional testing of the atmospheric revitalization pressure control  
system, part of the orbiter's life support system, continued this week. The orbiter docking  
system mechanism has been tested and will be stowed for flight. Modifications to  
Discovery's engine cutoff sensor wiring continue. Web posted. (2007). [NASA's Space  
Shuttle Processing Status Report [Online]. Available WWW: http://wwv.nasa.gov/  
centers/kennedy /shuttleoperations /status /_2007 /index.html [2007, May 18.]
</excerpt>
### Rank 5 of 1481 — 0.65
<excerpt title="20130010436.pdf">
## [PDF page 120]
Caidwell and Drew; Inclination/Orbit Altitude: 51.6 degrees/122 nautical miles. In Orbiter  
Processing Facility Bay No. 2 this morning, workers installed metal structures called
114

## [PDF page 121]
"strongbacks" on Endeavour's payload bay doors to allow the doors to be cycled open and  
closed to verify non-interference with thermal tiles. The orbiter positive pressure test was  
successfully completed this week. Functional testing is complete on Endeavour's landing  
gear and on the external tank doors. Closeout of the orbiter's aft and forward sections is  
under way. In high bay No. I of the Vehicle Assembly Building, stacking of the solid rocket  
boosters for STS-1 18 is complete. Platforms are being configured for the mating of the  
external tank and solid rocket boosters, which is scheduled for Sunday. Mission: STS-120 -  
23rd International Space Station Flight (IOA) - U.S. Node 2; Vehicle: Discovery (OV-103);  
Location: Orbiter Processing Facility Bay 3; Launch Date: Targeted for Oct. 20, 2007;  
Launch Pad: 39A; Crew: Meiroy, Zamka, Parazynski, Wheelock, Wilson, Nespoli and Tani;  
Inclination/Orbit Altitude: 51.6 degrees/122 nautical miles. In Orbiter Processing Facility  
bay No. 3, aft closeout work is under way. Functional testing of the atmospheric  
revitalization pressure control system, part of the orbiter's life support system, is complete.  
Modifications to Discovery's engine cutoff sensor wiring continue, as does the installation of  
BRI tile around the main landing gear doors and external tank doors. Web posted. (2007).  
[NASA's Space Shuttle Processing Status Report [Online]. Available WWW:  
http: / /www.nasa.gov/centers /_kennedv/shuttJeoperations /status /2007 /index.html  [2007,  
June 15.]

## [PDF page 121]
Strikers get a hot welcome from weather on picket lines  
Thursday was the first day of possibly many on the picket lines for striking shuttle program  
workers. Members of the International Association of Machinists and Aerospace Workers  
Local 2061 began a strike Thursday morning over stalled contract negotiations with their  
employer, United Space Alliance, NASA's main shuttle contractor. "It's hot out here," Local  
2061 President Lew Jamieson said after a few hours on the picket line. No new contract  
talks had been scheduled between the two sides as of late Thursday. The union has about  
570 members who work at Kennedy Space Center in various shuttle support jobs,  
composing roughly 10 percent of the company's local workforce. The workers began  
picketing around the clock at entrances to Kennedy Space Center and at the company's  
offices in Cape Canaveral and Titusville. Some wore pins that stated "No Scabs," a reference  
to the company's plan to bring in replacement workers. The strike is not expected to affect  
the shuttle Atlantis mission, which launched Friday from the space center. Web posted.  
(2007). [Strikers get a hot welcome from weather on picket lines [Online]. Available WWW:  
http: / /www. floridatoday.com / [2007, June 15].]
</excerpt>

## Search 4 — query: ""Frame Toby" Jason Reitman episode original air date"
### Rank 1 of 85 — 0.94 (passed on)
<excerpt title="Frame Toby - Ultimate Pop Culture Wiki - Fandom">
| "**Frame Toby**" |  
| --- |  
| _The Office_ episode |  
| Episode no. | Season 5 Episode 9 |  
| Directed by | Jason Reitman |  
| Written by | Mindy Kaling |  
| Cinematography by | Matt Sohn |  
| Editing by | Dean Holland |  
| Production code | 508 |  
| Original air date | November 20,2008 |  
| Guest appearance(s) |  
| * Andy Buckley as David Wallace (voice) |  
| Episode chronology |  
| ←**Previous** "Business Trip"**Next**→ "The Surplus" |  
| _The Office_(American season 5) |  
| List of _The Office_(American TV series) episodes |
"**Frame Toby**" is the ninth episode of the fifth season of the television series_The Office_, and the show's eighty-first episode overall. The episode aired in the United States on November 20, 2008, on NBC.
On November 25, 2008, a producer's cut of "Frame Toby" was posted on NBC.com. This cut ran approximately four minutes longer than the original airing. After nearly a two-year absence, this is the first producer's cut since season three's "The Return".
In this episode, Michael has trouble accepting the fact that his least favorite employee, HR rep Toby, has returned to the office and enlists Dwight's help to frame him for using drugs so he will be fired. Meanwhile, Pam is disgusted over a mess left in the microwave that no one bothers to clean up, and Jim buys his parents' house – without telling Pam.
Michael's outburst when he discovers that Toby has returned became an internet meme after the episode aired.[[1]](https://ultimatepopculture.fandom.com/wiki/Frame_Toby#cite_note-1)_Scream 2_ was mentioned in the episode, with the character Michael Scott saying how much he loved it and drawing parallels to his life and that of the movie's heroine, Sidney Prescott.[[2]](https://ultimatepopculture.fandom.com/wiki/Frame_Toby#cite_note-2)

## Synopsis[]
Michael Scott (Steve Carell) learns that Toby Flenderson (Paul Lieberstein) is back as their HR representative and reacts very badly to it. He tries to get CFO David Wallace (Andy Buckley) to get rid of Toby, but David refuses. Michael tries to pretend to be friends with Toby, but finds himself unable to do so. Michael and Dwight Schrute (Rainn Wilson) attempt to set Toby up for jvolrc yrirjjdvek by using Pam Beesly (Jenna Fischer) as bait, but Pam defuses the scheme. Michael tries to provoke Toby into punching him, which proves fruitless. Finally, Michael decides to plant drugs in Toby's desk, and purchases what he believes to be marijuana for $500 from two Vance Refrigeration employees. Dwight calls the police, who arrive shortly afterward. Dwight leads the police to Toby's desk, which the police search. Michael, starting to feel guilty, tries to take the blame, but the police discover that the planted "marijuana" is really a bag of Caprese salad. After the police leave, Toby scolds Michael for wasting the cops' time when they could have been catching real criminals. Michael is disgusted that Toby is more worried about the cops' time than about being framed, and hates Toby more than ever.
Pam finds a mess in the microwave, and writes an anonymous memo telling everyone to keep it clean. Her coworkers consider the note snobbish – except for Angela Martin (Angela Kinsey), and Ryan Howard (B. J. Novak), who unsuccessfully tries to feign incompetence to manipulate Pam into cleaning it. Ryan later tells Kelly (Mindy Kaling) that they have to break up, saying he is going on a trip to Thailand, before asking for jvo one last time and for any extra cash she has.
</excerpt>
### Rank 2 of 85 — 0.87
<excerpt title="Exploring Frame Toby - The Office Field Guide - S5E9">
# Exploring Frame Toby - The Office Field Guide - S5E9
## Chapters
### The microwave debate ### The microwave debate 5:56


# Exploring Frame Toby - The Office Field Guide - S5E9
## Chapters
### The microwave debate
5:56

# Exploring Frame Toby - The Office Field Guide - S5E9
## Chapters
### Fairness and character ethics ### Fairness and character ethics 8:15


# Exploring Frame Toby - The Office Field Guide - S5E9
## Chapters
### Fairness and character ethics
8:15

# Exploring Frame Toby - The Office Field Guide - S5E9
## Chapters
### Jim and Pam's house ### Jim and Pam's house 9:50


# Exploring Frame Toby - The Office Field Guide - S5E9
## Chapters
### Jim and Pam's house
9:50

# Exploring Frame Toby - The Office Field Guide - S5E9
## Chapters
### Final verdict and outro ### Final verdict and outro 12:02


# Exploring Frame Toby - The Office Field Guide - S5E9
## Chapters
### Final verdict and outro
12:02
Sync to video time

# Exploring Frame Toby - The Office Field Guide - S5E9
## Exploring Frame Toby - The Office Field Guide - S5E9
Mulverine
Mulverine
973 Likes
45K Views
2021 Feb 4
Toby is back! Michael and Dwight try to figure out how to get rid of him again, Jim buys a house without talking to Pam about it, and the Angela, Andy and Dwight triangle gets a little more intense. #TheOffice is one of the greatest shows of the 2000s! I’m reviewing every episode with some background, trivia, the deeper meaning, and more. Today, we're looking at the #Frame#Toby episode. Thanks to our NBC overlords for their creation and ownership of the Office. The clips used here are for reviewing and education. Written by Mindy Kaling Directed by Jason Reitman Aired on November 20, 2008 Subscribe: https://www.youtube.com/mulverine?sub... Patreon: /mulverine Discord: /discord The Office - LoFi Mix by Dimitriii - /@dimitriii4599…...more
...more Show less
How this was made
Auto-dubbed
Audio tracks for some languages were automatically generated. Learn more

# Exploring Frame Toby - The Office Field Guide - S5E9
## Chapters
View all

# Exploring Frame Toby - The Office Field Guide - S5E9
## Chapters
### Episode introduction ### Episode introduction 0:00


# Exploring Frame Toby - The Office Field Guide - S5E9
## Chapters
### Episode introduction
0:00

# Exploring Frame Toby - The Office Field Guide - S5E9
## Chapters
### Recollections and oddities ### Recollections and oddities 1:16


# Exploring Frame Toby - The Office Field Guide - S5E9
## Chapters
### Recollections and oddities
1:16

# Exploring Frame Toby - The Office Field Guide - S5E9
## Chapters
### Minor details and trivia ### Minor details and trivia 3:35


# Exploring Frame Toby - The Office Field Guide - S5E9
## Chapters
### Minor details and trivia
3:35

# Exploring Frame Toby - The Office Field Guide - S5E9
## Chapters
### The microwave debate ### The microwave debate 5:56


# Exploring Frame Toby - The Office Field Guide - S5E9
## Chapters
### The microwave debate
5:56
Transcript
Follow along using the transcript.
Show transcript

# Exploring Frame Toby - The Office Field Guide - S5E9
## Chapters
### Mulverine 48.2K subscribers
VideosAbout Discord Patreon Youtube Subscription Twitch

# Exploring Frame Toby - The Office Field Guide - S5E9
## Video details
Date
Feb 4, 2021
Views
45,863
Likes
973

# Exploring Frame Toby - The Office Field Guide - S5E9
## Transcript
NaN / NaN
14:37
</excerpt>
### Rank 3 of 85 — 0.80
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
### Rank 4 of 85 — 0.55
<excerpt title="The Office (Season 5, Episode 9) - Frame Toby">
# ‎Frame Toby – The Office (Season 5, Episode 9) - Apple TV (AU)
Open TV
*   Apple TV  
*   MLS
Search
Sign In
Frame Toby
The Office

# Frame Toby
Comedy
**S5, E9:** Jim surprises Pam when he buys his parents' house; Michael tries to frame Toby by planting drugs on him when he discovers he's back at work; someone made a mess in the microwave and nobody will clean it.
MORE
**S5, E9:** Jim surprises Pam when he buys his parents' house; Michael tries to frame Toby by planting drugs on him when he discovers he's back at work; someone made a mess in the microwave and nobody will clean it.
27 May 2021 · 19m
StarringAndy Buckley, Lee Eisenberg, Patrick Faucette
DirectorJason Reitman

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
Released 2021 Run Time 19 min Rated M Region of Origin United States© 2005-2009 NBC Studios, Inc. and Universal Network Television LLC. All Rights Reserved.

# Frame Toby
## Cast & Crew
### Languages
Original Audio English, English (United Kingdom)Audio
English (United States) (AAC, ⁨Dolby 5.1⁩)
Subtitles
English (CC)

# Frame Toby
## Cast & Crew
### Accessibility
Closed captions refer to subtitles in available languages with the addition of relevant non-dialogue information.
Australia
Select a country or region

# Frame Toby
## Africa, Middle East, and India
See All
*   Algeria  
*   Angola  
*   Armenia  
*   Azerbaijan  
*   Bahrain  
*   Benin  
*   Botswana  
*   Burkina Faso  
*   Cameroun  
*   Cape Verde  
*   Chad  
*   Congo, The Democratic Republic Of The  
*   Congo, Republic of  
*   Côte d’Ivoire  
*   Egypt  
*   Eswatini  
*   Gabon  
*   Gambia  
*   Ghana  
*   Guinea-Bissau  
*   India  
*   Iraq  
*   Israel  
*   Jordan  
*   Kenya  
*   Kuwait  
*   Lebanon  
*   Liberia  
*   Libya  
*   Madagascar  
*   Malawi  
*   Mali  
*   Mauritania  
*   Mauritius  
*   Morocco  
*   Mozambique  
*   Namibia  
*   Niger (English)  
*   Nigeria  
*   Oman  
*   Qatar  
*   Rwanda  
*   São Tomé and Príncipe  
*   Saudi Arabia  
*   Senegal  
*   Seychelles  
*   Sierra Leone  
*   South Africa  
*   Sri Lanka  
*   Tajikistan  
*   Tanzania, United Republic Of  
*   Tunisia  
*   Turkmenistan  
*   Uganda  
*   United Arab Emirates  
*   Yemen  
*   Zambia  
*   Zimbabwe
</excerpt>
### Rank 5 of 85 — 0.27
<excerpt title="Transcript - Ep 155.5 - A Look Back on Frame Toby">
### **TRANSCRIPT**
[00:00:55] **Angela**Oh, that's so cool.
[00:00:56] **Jenna**I know.
[00:00:57] **Angela**We have photos in two cities.
[00:00:58] **Jenna**In two cities. That's the big time.
[00:01:01] **Angela**We're bicoastal.
[00:01:03] **Jenna**We are.
[00:01:03] **Angela**Right now wait a second. Right now we're bicoastal.
[00:01:06] **Jenna**Office Ladies has gone bicoastal.
[00:01:08] **Angela**That feels real boss lady.
[00:01:09] **Jenna**It does. I like it.
[00:01:11] **Angela**Me too. Well, since we're talking about being in offices, Jenna guess who's back at Dunder Mifflin?
[00:01:17] **Jenna**Toby.
[00:01:18] **Angela**Well, not everybody's happy about it.
[00:01:21] **Michael Scott**No, God! No, god, please! No! No! No! No!
[00:01:30] **Jenna**That's right. Today we are talking about Frame Toby. It is Season five, Episode nine. It is written by Mindy Kaling and directed by Jason Reitman. That's a good duo. I'm going to give you a summary.
[00:01:43] **Angela**I was hoping you would.
[00:01:45] **Jenna**Michael reacts poorly to the revelation that Toby is back at the Scranton branch.
[00:01:51] **Angela**I like the use of the word poorly.

### **TRANSCRIPT**
[00:01:54] **Jenna**I know. That's an understatement. So he and Dwight hatch a plan to frame Toby for drugs that Michael has purchased from the two Vance refrigeration employees, Gino and Leo. Pam is incensed by a mess that is left in the microwave by one of her coworkers- we don't know who. She leaves a pointed note which elicits mixed reactions from the fellow employees. Meanwhile, Ryan breaks up with Kelly and Jim surprises Pam with the news that he bought his parents house for them.
[00:02:28] **Angela**That's a lot.
[00:02:29] **Jenna**It's a lot. These headphones are tight.
[00:02:34] **Angela**Mm hmm.
[00:02:35] **Jenna**The headphones are tight in New York, I fixed them.
[00:02:39] **Jared**Do you want a different pair?
[00:02:40] **Jenna**No, I fixed 'em.
[00:02:42] **Angela**You guys, that was Jared in New York.
[00:02:44] **Jenna**Yeah. Jared is the Sam of New York.
[00:02:47] **Angela**Yeah. Sam, say hi.
[00:02:48] **Sam**Little dig at LA and our loose headphones.
[00:02:49] **Jenna**Why?
[00:02:51] **Angela**I think she likes them loose.
[00:02:53] **Jenna**I like a loose headphone.
[00:02:55] **Sam**Oh, in that case, take that, Jared.
[00:02:55] **Jenna**Jared's all squeezin my brain with the headphones here in New York. Should we go into fast facts?
[00:03:04] **Angela**I think we should.
</excerpt>

## Search 5 — query: "Orlando Magic head coach list full timeline"
### Rank 1 of 74 — 0.70 (passed on)
<excerpt title="A spot in Orlando Magic history: What will new coach add to this lineup?">
#### Chris Jent
*   **Years:** 2005  
*   **Regular season:** 5-13  
*   **Postseason:** 0-0  
*   **Of note:** Interim; first-year assistant was thrust into head coaching job at age 35 after Davis was let go; only head coach in franchise history whose entire NBA head coaching career consists of this single stint with the Magic.

#### Brian Hill
*   **Years:** 2005-07  
*   **Regular season:** 76-88  
*   **Postseason:** 0-4  
*   **Of note:** Only coach with two separate stints with team; after going 36-46 in 2005-06, led the Magic to the postseason the following year for the first time in four years.
The relationship between Orlando Magic coach Stan Van Gundy and star player Dwight Howard was rocky at the end of their time together. (AP Photo/El Nuevo Herald, David Santiago)

#### Stan Van Gundy
*   **Years:** 2007-12  
*   **Regular season:** 259-135  
*   **Postseason:** 31-28  
*   **Of note:** Franchise leader in regular-season winning percentage (.657) and playoff wins; led Magic on a run to the 2009 NBA Finals, where they lost in five games to the Lakers; only became coach when Billy Donovan backed out of his contract to return to the University of Florida; now calls NBA games for Amazon Prime.

#### Jacque Vaughn
*   **Years:** 2012-15  
*   **Regular season:** 58-158  
*   **Postseason:** 0-0  
*   **Of note:** Oversaw start of post-Dwight Howard rebuild; when he was hired at age 37, he was the youngest coach in the NBA at the time; helped early development of Victor Oladipo and Nikola Vucevic.

#### James Borrego
*   **Years:** 2015  
*   **Regular season:** 10-20  
*   **Postseason:** 0-0  
*   **Of note:** Interim; won his debut, 103-97 over Lakers; Magic held first four opponents under 100 points; later became Hornets head coach and first full-time Hispanic head coach in NBA history.

#### Scott Skiles
*   **Years:** 2015-16  
*   **Regular season:** 35-47  
*   **Postseason:** 0-0  
*   **Of note:** Former Magic player resigned unexpectedly after just one season; team improved by 10 wins in his lone season; speculation centers on a rift with management that led to his departure.

#### Frank Vogel
*   **Years:** 2016-18  
*   **Regular season:** 54-110  
*   **Postseason:** 0-0  
*   **Of note:** Was hired for his track record with defense as coach of the Pacers; tenure was complicated by a front office in transition; later won 2020 NBA title with the Lakers in the Orlando pandemic bubble.

#### Steve Clifford
*   **Years:** 2018-21  
*   **Regular season:** 96-131  
*   **Postseason:** 2-8  
*   **Of note:** Oversaw 17-win improvement in his first season from previous year; ended six-year playoff drought in his first season.

#### Jamahl Mosley
*   **Years:** 2021-26  
*   **Regular season:** 189-221  
*   **Postseason:** 7-12  
*   **Of note:** Second in coach of the year voting in 2023-24; won two Southeast Division titles; fired after three consecutive first-round playoff exits.
</excerpt>
### Rank 2 of 74 — 0.67
<excerpt title="Jamahl Mosley">
# Jamahl Mosley - USA Basketball
### Coach Academy
*   Frequently Asked Questions

# Jamahl Mosley - USA Basketball
### 3X Play
*   Rules & Standards

# Jamahl Mosley - USA Basketball
### On-Demand Courses
*   Frequently Asked Questions

# Jamahl Mosley - USA Basketball
### E-Learning
*   Frequently Asked Questions

# Jamahl Mosley - USA Basketball
### Coaching Resources
*   Skills and Drills  
        *   Youth Guidelines  
        *   Official USA Basketball Guidebook & E-Book

# Jamahl Mosley - USA Basketball
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

# Jamahl Mosley
*   Position**Coach**
_**As of Mar. 15, 2024**_
**Jamahl****Mosley**, the head coach of the Orlando Magic, fufilled his first head coaching assignment with USA Basketball as the head coach of the 2023 Men's Select Team. The team, made up of NBA and NBA G League talent, trainined with and against the 2023 Men's National Team ahead of the 2023 FIBA World Cup. This was his second time serving on a select team coaching staff. He was an assisntant with the 2021 Men's Select Team prior to the 2020 Olympic Games.
Mosley was named the head coach of the Magic in 2021. He was an assistant coach with the Dallas Mavericks prior to Orlando and also served as the head coach of Dallas' Summer League squad from 2017-19.
Mosley spent four seasons as an assistant coach for the Cleveland Cavaliers from 2010-14. Before joining the Cavaliers in July 2010, Mosley spent five seasons with the Denver Nuggets. His tenure began in player development and advance scouting before he became an assistant coach for his last three seasons with the franchise. The Nuggets reached the playoffs, winning 50 games or more, each of his final three years.
A native of Milwaukee, Mosley was a four-year letterman at University of Colorado (1997-2001). Named in 2000 All-Big 12 Conference third team, he is one of 33 players in CU history to score more than 1,000 points. Following his collegiate career, he played four seasons of professional basketball overseas, including two years for the Victoria Titans (Australia), one year with Baloncesto Leon (Spain) and one year in South Korea.

# Jamahl Mosley
## **Jamahl Mosley's USA Basketball Coaching Record**
**Event/Team****Role****Record****Finish**  
2023 Men's Select Team Head Coach N/A N/A  
2021 Men's Select Team Assistant Coach N/A N/A  
**TOTALS****N/A**N/A
**share**Share on TwitterShare on FacebookShare on Email

# Jamahl Mosley
## Related Content
Prev Slide Next Slide
![Image 62: USA Basketball](blob:http://localhost/b9a31d3949b1882a09ed2f8508d538f3)Play Video
August 6, 2023
</excerpt>
### Rank 3 of 74 — 0.65
<excerpt title="A spot in Orlando Magic history: What will new coach add to this lineup?">
The Orlando Magic fired head coach Jamahl Mosley on Monday. Since its inaugural season in 1989, the team has had 15 head coaches, including interim coaches.
The Magic have played 37 seasons and have made the playoffs 19 times. In the past 10 seasons, the Magic have made the playoffs five times.
It’s not an easy job and the firing of a coach is not always fair. Even Golden State Warriors coach Steve Kerr has said each NBA head coach’s tenure has “an expiration date.”
The search for a new coach, led by president of basketball operations Jeff Weltman, is getting started. Meanwhile, here’s a look at the Magic’s coaching history, from the beginning with Matt Goukas through Mosley’s time in Orlando:

#### Matt Guokas
*   **Years:** 1989-93  
*   **Regular season:** 111-217  
*   **Postseason:** 0-0  
*   **Of note:** Inaugural coach; oversaw early expansion years; team was 41-41 in his final season, the Magic’s first non-losing season, which was also Shaquille O’Neal’s rookie year.

#### Brian Hill
*   **Years:** 1993-97  
*   **Regular season:** 191-104  
*   **Postseason:** 18-18  
*   **Of note:** Led team to first NBA Finals (1995); 60-22 record in 1995-96 is franchise’s best regular-season record.

#### Richie Adubato
*   **Years:** 1997  
*   **Regular season:** 21-12  
*   **Postseason:** 2-3  
*   **Of note:** Interim; posted a .636 winning percentage after taking over for the fired Hill; Magic went on six-game winning streak after he became coach; was Magic’s radio color analyst from 2005-2020.
Gary W. Green, Orlando Sentinel
Matt Guokas was the Orlando Magic's first head coach. (Orlando Sentinel file)

#### Chuck Daly
*   **Years:** 1997-99  
*   **Regular season:** 74-58  
*   **Postseason:** 1-3  
*   **Of note:** Hall of Famer known for “Bad Boys” years with the Pistons; Magic went 33-17 in lockout-shortened 1998-99 season.

#### Doc Rivers
*   **Years:** 1999-2003  
*   **Regular season:** 171-168  
*   **Postseason:** 5-10  
*   **Of note:** 2000 Coach of the Year winner; led Magic to 41-41 mark in his debut season as a head coach.

#### Johnny Davis
*   **Years:** 2003-05  
*   **Regular season:** 51-84  
*   **Postseason:** 0-0  
*   **Of note:** Fired after a 21-game losing streak; was Magic Hall-of-Famer Dwight Howard’s first NBA coach and is credited with helping him transition from high school to the NBA.

#### Chris Jent
*   **Years:** 2005  
*   **Regular season:** 5-13  
*   **Postseason:** 0-0  
*   **Of note:** Interim; first-year assistant was thrust into head coaching job at age 35 after Davis was let go; only head coach in franchise history whose entire NBA head coaching career consists of this single stint with the Magic.
</excerpt>
### Rank 4 of 74 — 0.63
<excerpt title="Jamahl Mosley Bio">
Skip to content
*   HOME  
*   WHO WE ARE  
    *   ABOUT THE NBCA  
    *   NBCA LEADERSHIP  
    *   NBCA EXECUTIVES  
    *   MILESTONES

*   COACHES  
    *   HEAD COACHES  
    *   ASSISTANT COACHES

*   PARTNERS  
    *   CHARITABLE PARTNERS  
    *   CORPORATE PARTNERS

*   SPEAKING ENGAGEMENTS  
*   MEDIA  
    *   COACHES CORNER  
    *   AWARDS  
        *   CHUCK DALY LIFETIME ACHIEVEMENT AWARD  
        *   MICHAEL H. GOLDBERG NBCA COACH OF THE YEAR AWARD  
        *   TEX WINTER ASSISTANT COACH LIFETIME IMPACT AWARD  
        *   NBA COACH OF THE YEAR AWARD  
        *   NBA COACHES OF THE MONTH

    *   COACHES STORIES

*   NEWS
Jamahl Mosley BioNBA Coaches Association2026-10-01T23:21:31+00:00

### NEW ORLEANS PELICANS HEAD COACH
Jamahl Mosley is the Head Coach of the New Orleans Pelicans. On May 18, 2026, Mosley became the 9th Head Coach* in Pelicans history.
Prior to joining the Pelicans, Coach Mosley was the Head Coach of the Orlando Magic (2021-2026), where he led the team to three consecutive NBA Playoff berths (2024, 2025, 2026). Prior to joining the Magic, he was an Assistant Coach for the Dallas Mavericks under Head Coach Rick Carlisle (2014-2021), where he helped the team reach four NBA Playoff berths (2015, 2016, 2020, 2021). Prior to joining the Mavericks, Coach Mosley was an Assistant Coach for the Cleveland Cavaliers under Head Coaches Byron Scott (2010-2013) and Mike Brown (2013-2014). Prior to joining the Mavericks, he was a Player Development/Advance Scout (2005-2007) and an Assistant Coach (2007-2010) with the Denver Nuggets under Head Coach George Karl, where he helped the team reach at least 50 wins for three consecutive seasons (2007-2010), and five NBA Playoff berths (2006 2007, 2008, 2009, 2010), including an NBA Conference Finals appearance (2009).
Jamahl Mosley was born on October 6, 1978, in Milwaukee, Wisconsin. He attended and played at the University of Colorado, where he was selected to the Third-Team All-Big 12 (2000 & 2001). Coach Mosley also had a professional playing career with stops overseas in Australia, Spain, and Korea.
***Inclusive of Full-Time and Interim Head Coaches**
</excerpt>
### Rank 5 of 74 — 0.60
<excerpt title="Orlando Magic Coaches">
# Orlando Magic Coaches
## 15 Coaches
|  | Regular Season | Playoffs |  
| --- | --- | --- |  
| Rk | Coach | From | To | Yrs | G | W | L | W/L% | W > .500 | Plyfs | G | W | L | W/L% | Conf | Champ |  
| 1 | Richie Adubato | 1997 | 1997 | 1 | 33 | 21 | 12 | .636 | 4.5 | 1 | 5 | 2 | 3 | .400 | 0 | 0 |  
| 2 | James Borrego | 2015 | 2015 | 1 | 30 | 10 | 20 | .333 | -5.0 |  |  |  |  |  |  |  |  
| 3 | Steve Clifford | 2019 | 2021 | 3 | 227 | 96 | 131 | .423 | -17.5 | 2 | 10 | 2 | 8 | .200 | 0 | 0 |  
| 4 | Chuck Daly | 1998 | 1999 | 2 | 132 | 74 | 58 | .561 | 8.0 | 1 | 4 | 1 | 3 | .250 | 0 | 0 |  
| 5 | Johnny Davis | 2004 | 2005 | 2 | 135 | 51 | 84 | .378 | -16.5 |  |  |  |  |  |  |  |  
| 6 | Matt Guokas | 1990 | 1993 | 4 | 328 | 111 | 217 | .338 | -53.0 |  |  |  |  |  |  |  |
</excerpt>

## Search 6 — query: "STS-120 crew Pamela Melroy Scott Parazynski Charles van Hoften Kathryn?"
### Rank 1 of 102 — 0.68 (passed on)
<excerpt title="NASA Assigns Crew for Space Shuttle Mission STS-120">
# NASA Assigns Crew for Space Shuttle Mission STS-120 - SpaceNews
*   NewsOpen dropdown menu  
    *   Latest  
    *   Civil  
    *   Commercial  
    *   Launch  
    *   Military  
    *   Opinion  
    *   Policy & Politics

*   Video & AudioOpen dropdown menu  
    *   Virtual Events  
    *   Space Minds Podcast  
    *   Commerical Space Transformers  
    *   Leading Women

*   Newsletters  
*   Magazine  
*   EventsOpen dropdown menu  
    *   Virtual Events  
    *   Icon Awards  
    *   Events Calendar  
    *   Submit Your Event

*   SponsoredOpen dropdown menu  
    *   SN Focus

*   Press ReleasesOpen dropdown menu  
    *   Latest  
    *   Post a Press Release

*   Job Board  
*   Work With UsOpen dropdown menu  
    *   Advertise  
    *   Editorial Calendar  
    *   Ad Portal  
    *   Contact Us

*   MoreOpen dropdown menu  
    *   About SpaceNews  
    *   FAQs  
    *   Contact Us
Open Search
Search for:  Search
*   TOPICS:  
*   Artemis  
*   SpaceX  
*   NASA  
*   Golden Dome  
*   Europe  
*   China  
*   Funding Rounds  
*   Civil  
*   Commercial  
*   Launch  
*   Military
Home / **NASA Assigns Crew for Space Shuttle Mission STS-120**
Posted inPress Release

# NASA Assigns Crew for Space Shuttle Mission STS-120
bySpaceRefJune 19, 2006 July 15, 2024
*   Share on X (Opens in new window)X  
*   Share on LinkedIn (Opens in new window)LinkedIn  
*   Share on Facebook (Opens in new window)Facebook  
*   Share on Reddit (Opens in new window)Reddit  
*   [Email a link to a friend (Opens in new window)Email](mailto:?subject=%5BShared%20Post%5D%20NASA%20Assigns%20Crew%20for%20Space%20Shuttle%20Mission%20STS-120&body=https%3A%2F%2Fspacenews.com%2Fnasa-assigns-crew-for-space-shuttle-mission-sts-120%2F&share=email)
NASA has assigned crew members to the space shuttle flight that will launch an Italian-built U.S. module for the International Space Station.
Air Force Col. Pamela A. Melroy will command the STS-120 mission to take the Node 2 connecting module to the station. Melroy, a veteran shuttle pilot, is the second woman to command a shuttle. Marine Corps Col. George D. Zamka will serve as pilot. The flight’s mission specialists will be Scott E. Parazynski, Army Col. Douglas H. Wheelock, Navy Capt. Michael J. Foreman and Paolo A. Nespoli, a European Space Agency astronaut from Italy. Zamka, Wheelock, Foreman and Nespoli will be making their first spaceflight.
STS-120 will be Melroy’s third shuttle flight. The native of Palo Alto, Calif., served as pilot of missions STS-92 in 2000 and STS-112 in 2002, both flights to the space station. Zamka, a native of Jersey City, N.J., has a bachelor’s from the U.S. Naval Academy, Annapolis, Md., and a master’s from the Florida Institute of Technology, Melbourne, Fla.
</excerpt>
### Rank 2 of 102 — 0.65
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
### Rank 3 of 102 — 0.63
<excerpt title="NASA Assigns Crew for Space Shuttle Mission STS-120">
# NASA Assigns Crew for Space Shuttle Mission STS-120
bySpaceRefJune 19, 2006 July 15, 2024
*   Share on X (Opens in new window)X  
*   Share on LinkedIn (Opens in new window)LinkedIn  
*   Share on Facebook (Opens in new window)Facebook  
*   Share on Reddit (Opens in new window)Reddit  
*   [Email a link to a friend (Opens in new window)Email](mailto:?subject=%5BShared%20Post%5D%20NASA%20Assigns%20Crew%20for%20Space%20Shuttle%20Mission%20STS-120&body=https%3A%2F%2Fspacenews.com%2Fnasa-assigns-crew-for-space-shuttle-mission-sts-120%2F&share=email)
NASA has assigned crew members to the space shuttle flight that will launch an Italian-built U.S. module for the International Space Station.
Air Force Col. Pamela A. Melroy will command the STS-120 mission to take the Node 2 connecting module to the station. Melroy, a veteran shuttle pilot, is the second woman to command a shuttle. Marine Corps Col. George D. Zamka will serve as pilot. The flight’s mission specialists will be Scott E. Parazynski, Army Col. Douglas H. Wheelock, Navy Capt. Michael J. Foreman and Paolo A. Nespoli, a European Space Agency astronaut from Italy. Zamka, Wheelock, Foreman and Nespoli will be making their first spaceflight.
STS-120 will be Melroy’s third shuttle flight. The native of Palo Alto, Calif., served as pilot of missions STS-92 in 2000 and STS-112 in 2002, both flights to the space station. Zamka, a native of Jersey City, N.J., has a bachelor’s from the U.S. Naval Academy, Annapolis, Md., and a master’s from the Florida Institute of Technology, Melbourne, Fla.

# NASA Assigns Crew for Space Shuttle Mission STS-120
Parazynski, who also considers Palo Alto, Calif., his hometown along with Evergreen, Colo., will be making his fifth shuttle flight and is a veteran spacewalker. Wheelock, a native of Windsor, N.Y., is a West Point graduate with a master’s from Georgia Tech, Atlanta. Foreman is a Wadsworth, Ohio, native with a bachelor’s and a master’s from the U.S. Naval Academy and the U.S. Naval Postgraduate School, Monterey, Calif. Nespoli is a native of Milan, Italy. He has a bachelor’s and a master’s from the Polytechnic University of New York.
This crew announcement reflects reassignments of other astronauts to other missions and to technical and management positions within NASA.
Video of the STS-120 crew members will air on NASA TV’s Video File. For schedules, downlink information and links to streaming video, visit:
http://www.nasa.gov/ntv
For complete astronaut biographical information, visit:
http://www.jsc.nasa.gov/Bios
For more information about space shuttle missions and crews, visit
http://www.nasa.gov/shuttle

# NASA Assigns Crew for Space Shuttle Mission STS-120
### _Related_
Tagged: ISS,NASA HQ,space shuttle,U.S.

# NASA Assigns Crew for Space Shuttle Mission STS-120
## Post navigation
Previous Engineering Science Payload Delivered to Mars Phoenix Mission “PIT”
Next New State of the Art Software Will Safeguard ATV Rendezvous

# NASA Assigns Crew for Space Shuttle Mission STS-120
## Post navigation
#### Stellar Dispatch
all dispatches>>

# NASA Assigns Crew for Space Shuttle Mission STS-120
## Flexell Space and ALATYR Sign MoU to Explore Solar Power Solutions for Orbital Data Centers


# NASA Assigns Crew for Space Shuttle Mission STS-120
## All Points Logistics Announces Partnership with Expeditors for Space Prep Logistics Center at Kennedy Space Center


# NASA Assigns Crew for Space Shuttle Mission STS-120
## Cosmo Bee to flight-test Honeybee Hall thruster with D-Orbit in 2027
</excerpt>
### Rank 4 of 102 — 0.62
<excerpt title="The seven member STS-120 crew aboard space shuttle Discovery ...">
# The seven member STS-120... - International Space Station
## International Space Station's Post
MS3 Scott Parazynski... [http://go.nasa.gov/1kxeEdw](https://l.facebook.com/l.php?u=https%3A%2F%2Fgo.nasa.gov%2F1kxeEdw&h=AUDxXpyZDzmeozPeExLHVISwj9LiqjXiwr5158Kholph_NnfyFjTt12mXkWQJoYP6zEuUZQiBpqy8vsyLOmZOKg4uvv77FkfYetW5wW35-ahVKa59tFRxa_csI4gGDC7AphxEKh7HiO-YEsgkANwoBWt1EtYJ1QuLkxFHw&__tn__=-UK-R&c[0]=AUCFKNxiYIODrjlam6qx92pyDiouHIsZbN8CiQOgufJEWQjsAAxDb-aKKLOLW1sOHEOmc2xl-cJ4R_v1o9UPi5wKVBUldg11lVQSyfBqHm6tMi3LVkmfRf2Azqs9uuXNuUnli0UCQsg907Ok5_gJ9T16ShTR-5tRLanI7MCHvkRtQTgVSIUT5t1uoY_Meg)

# The seven member STS-120... - International Space Station
## International Space Station's Post
MS4 Paolo Nespoli... [http://go.nasa.gov/HrdYP7](https://l.facebook.com/l.php?u=https%3A%2F%2Fgo.nasa.gov%2FHrdYP7&h=AUBDCNjS6Viou7pphSi0jKhFogN7QK6v9ZS92k4x5TNbfvGPaRb70oQAHt2H8LLjcrGZTCRyaMcSS0UfnuIpRc5JC2yt58VMBK1WMt0EPSduazZQRen7oF6cRwNBwPREq_MqfsafNcMAjf-1ISWFpF6R4RmpZyKXHR6HTg&__tn__=-UK-R&c[0]=AUCFKNxiYIODrjlam6qx92pyDiouHIsZbN8CiQOgufJEWQjsAAxDb-aKKLOLW1sOHEOmc2xl-cJ4R_v1o9UPi5wKVBUldg11lVQSyfBqHm6tMi3LVkmfRf2Azqs9uuXNuUnli0UCQsg907Ok5_gJ9T16ShTR-5tRLanI7MCHvkRtQTgVSIUT5t1uoY_Meg)
Up crew member...
</excerpt>
### Rank 5 of 102 — 0.61
<excerpt title="The seven member STS-120 crew aboard space shuttle Discovery ...">
# The seven member STS-120... - International Space Station
## International Space Station's Post
MS2 Stephanie Wilson.... [http://go.nasa.gov/1h4IRuJ](https://l.facebook.com/l.php?u=https%3A%2F%2Fgo.nasa.gov%2F1h4IRuJ&h=AUBRU7WkmKo1XHYhTNjEvhNRy2RvwEkbyvDBMNpeWKUwvWeu7TNj06l1I6lbM5wWVglD0DEw7R27lBlNc3HBKd0R-Y-cvtfawgxtaj6wzPwrJWtO19RR_OYVF2LJGTmS53WBIs-vz3fLt6S-P03E_OBTkwtzzB6VGvMBpw&__tn__=-UK-R&c[0]=AUCFKNxiYIODrjlam6qx92pyDiouHIsZbN8CiQOgufJEWQjsAAxDb-aKKLOLW1sOHEOmc2xl-cJ4R_v1o9UPi5wKVBUldg11lVQSyfBqHm6tMi3LVkmfRf2Azqs9uuXNuUnli0UCQsg907Ok5_gJ9T16ShTR-5tRLanI7MCHvkRtQTgVSIUT5t1uoY_Meg)

# The seven member STS-120... - International Space Station
## International Space Station's Post
MS3 Scott Parazynski... [http://go.nasa.gov/1kxeEdw](https://l.facebook.com/l.php?u=https%3A%2F%2Fgo.nasa.gov%2F1kxeEdw&h=AUDxXpyZDzmeozPeExLHVISwj9LiqjXiwr5158Kholph_NnfyFjTt12mXkWQJoYP6zEuUZQiBpqy8vsyLOmZOKg4uvv77FkfYetW5wW35-ahVKa59tFRxa_csI4gGDC7AphxEKh7HiO-YEsgkANwoBWt1EtYJ1QuLkxFHw&__tn__=-UK-R&c[0]=AUCFKNxiYIODrjlam6qx92pyDiouHIsZbN8CiQOgufJEWQjsAAxDb-aKKLOLW1sOHEOmc2xl-cJ4R_v1o9UPi5wKVBUldg11lVQSyfBqHm6tMi3LVkmfRf2Azqs9uuXNuUnli0UCQsg907Ok5_gJ9T16ShTR-5tRLanI7MCHvkRtQTgVSIUT5t1uoY_Meg)
</excerpt>

## Search 7 — query: "STS-120 crew list"
### Rank 1 of 121 — 0.88 (passed on)
<excerpt title="Space Shuttle Flight 120 (STS-120) Post Flight Presentation Video">
# Space Shuttle Flight 120 (STS-120) Post Flight Presentation Video
Return to the Space Shuttle Video Library index
Space Shuttle Flight 121 Video
**Space Shuttle Flight 120 (STS-120) Post Flight Presentation, narrated by the astronauts (18 minutes).**
*   **Launch: October 23, 2007.**  
*   **Crew: Pamela Melroy, George D. Zamka, Scott E. Parazynski, Stephanie Wilson, Douglas H. Wheelock, Paolo A. Nespoli.
Launching ISS Expedition 16 Crew: Daniel M. Tani.
Landing ISS Expedition 16 Crew: Clayton Anderson.**
*   **Vehicle: Discovery.**
We are people from around the world dedicated to the creation of a spacefaring civilization. We are an independent nonprofit nonpartisan educational membership organization.

# Space Shuttle Flight 120 (STS-120) Post Flight Presentation Video
## About NSS
*   About NSS  
*   Mission & History  
*   Member Benefits  
*   NSS Leadership  
*   Alliances & Affiliates  
*   Corporate Documents  
*   NSS Logos  
*   Press Releases  
*   Awards  
*   Thought Leadership  
*   Contact NSS

# Space Shuttle Flight 120 (STS-120) Post Flight Presentation Video
## Publications
*   Ad Astra Magazine  
*   Downlink Newsletter  
*   Space Settlement Roadmap  
*   Space Settlement Journal  
*   Policy Documents  
*   Space 2.0  
*   Press Releases  
*   Book Reviews  
*   NSS Space Library  
*   Blog

# Space Shuttle Flight 120 (STS-120) Post Flight Presentation Video
## Get involved
*   Why Space Matters?  
*   Why Join?  
*   Why Donate?  
*   How to Donate  
*   Inside NSS (Member Sign-in)  
*   Be a Space Advocate  
*   Career Center  
*   Local Chapters  
*   Space Biz Plan  
*   Young Professionals  
*   Education  
*   Contests  
*   Volunteer  
*   Space Ambassadors  
*   Social Networks  
*   Orbital Settlement Design Project

# Space Shuttle Flight 120 (STS-120) Post Flight Presentation Video
## Our Goals
*   Defending Earth  
*   Space Solar Power  
*   Asteroid Resources  
*   Orbital Debris  
*   Space Settlement  
*   Mission & History

# Space Shuttle Flight 120 (STS-120) Post Flight Presentation Video
## Events & Contests
*   International Space Development Conference (ISDC)  
*   Space Settlement Summit  
*   NSS Space Forums  
*   Global Space Debates  
*   O’Neill Space Space Settlement Contest  
*   Space Settlement Design Competition  
*   March Storm / Fall Fury  
*   Space Biz Plan Contest  
*   Contests  
*   NSS Event Calendar

# Space Shuttle Flight 120 (STS-120) Post Flight Presentation Video
## Videos
*   Space Solar Power  
*   Defending Earth  
*   Space Settlement  
*   SpaceX Collier Trophy

# Space Shuttle Flight 120 (STS-120) Post Flight Presentation Video
## quick Links
*   Join NSS  
*   How to Donate  
*   Donate Now  
*   Renewal  
*   Member Benefits  
*   Volunteer  
*   Career Center  
*   Ad Astra Magazine  
*   Blog
FacebookX-twitterInstagramYoutubeLinkedin
©2026 nss.org. All rights reserved. NSS is a registered 501(c)(3) nonprofit organization.
*   Privacy  
*   Terms  
*   Contact Us
</excerpt>
### Rank 2 of 121 — 0.88
<excerpt title="Space Shuttle Flight 120 (STS-120) Post Flight Presentation Video">
# Space Shuttle Flight 120 (STS-120) Post Flight Presentation Video - NSS
## Latest Articles
Explore the NSS Blog
*   Book Reviews  
    *   Commercial Space  
    *   ISDC  
    *   NSS Chapter News  
    *   NSS Press Releases  
    *   Space Policy  
    *   Space Settlement  
    *   Space Solar Power  
    *   This Space Available

# Space Shuttle Flight 120 (STS-120) Post Flight Presentation Video - NSS
## Featured
Fiction
Non-Fiction
Children’s Books
*   NSS Gerard K. O’Neill Space Settlement Contest  
    *   International Space Settlement Design Competition  
    *   spUN Student Debates at ISDC  
    *   “Live in a Healthy Space” Design Competition  
    *   Goddard 100 Contest  
    *   [Martine Rothblatt Space Settlement in Our Lifetime Prize Business Plan Competition](https://spacebizplan.nss.org/details/?_gl=1*4iuyvo*_ga*MTk0NTAxMTk0OC4xNzYzNTIwMTcw*_ga_826R21W2LF*czE3NjM4MTE2NTIkbzIyJGcxJHQxNzYzODE1NTk2JGo1OSRsMCRoMA..*_ga_ZR7T5RKQZV*czE3NjM4MDEwOTAkbzIwJGcxJHQxNzYzODE1NTk2JGo1OSRsMCRoMA..)  
    *   Roadmap to Space Art Contest  
    *   Space Elevator Academic Challenge  
    *   Jim Baen Memorial Writing Contest  
    *   Reach for the Stars National Rocket Competition
Learn More
*   NSS YouTube Channel  
    *   NSS Forums  
    *   Space Settlement  
    *   Science and Futurism with Isaac Arthur  
    *   This Week in Space with Rod Pyle and Tariq Malik  
    *   Dear Earth: We’re Sorry for What We’ve Done to You…  
    *   Defending Earth  
    *   SpaceX Collier Trophy
*    About NSS  Close About NSS Open About NSS

# Space Shuttle Flight 120 (STS-120) Post Flight Presentation Video - NSS
## Featured
### About NSS
The National Space Society is the preeminent citizen’s voice on space exploration, development, and settlement. The NSS Vision is “People living and working in thriving communities beyond the Earth, and the use of the vast resources of space for the dramatic betterment of humanity.”

# Space Shuttle Flight 120 (STS-120) Post Flight Presentation Video - NSS
## Quick Links
*   About NSS  
    *   Mission & History  
    *   Our Strategies  
    *   Alliances & Affiliates  
    *   Awards  
    *   Thought Leadership  
    *   NSS Leadership  
    *   Corporate  
    *   Press Releases  
    *   Policy Documents  
    *   International Policy  
    *   Contact NSS

# Space Shuttle Flight 120 (STS-120) Post Flight Presentation Video - NSS
## DotCoMM Awards Gold Winner 2024
Join
RenewDonate

# Space Shuttle Flight 120 (STS-120) Post Flight Presentation Video
Return to the Space Shuttle Video Library index
Space Shuttle Flight 121 Video
**Space Shuttle Flight 120 (STS-120) Post Flight Presentation, narrated by the astronauts (18 minutes).**
*   **Launch: October 23, 2007.**  
*   **Crew: Pamela Melroy, George D. Zamka, Scott E. Parazynski, Stephanie Wilson, Douglas H. Wheelock, Paolo A. Nespoli.
Launching ISS Expedition 16 Crew: Daniel M. Tani.
Landing ISS Expedition 16 Crew: Clayton Anderson.**
*   **Vehicle: Discovery.**
We are people from around the world dedicated to the creation of a spacefaring civilization. We are an independent nonprofit nonpartisan educational membership organization.
</excerpt>
### Rank 3 of 121 — 0.86
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
### Rank 4 of 121 — 0.86
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
### Rank 5 of 121 — 0.83
<excerpt title="NASA Assigns Crew for Space Shuttle Mission STS-120">
# NASA Assigns Crew for Space Shuttle Mission STS-120 - SpaceNews
*   NewsOpen dropdown menu  
    *   Latest  
    *   Civil  
    *   Commercial  
    *   Launch  
    *   Military  
    *   Opinion  
    *   Policy & Politics

*   Video & AudioOpen dropdown menu  
    *   Virtual Events  
    *   Space Minds Podcast  
    *   Commerical Space Transformers  
    *   Leading Women

*   Newsletters  
*   Magazine  
*   EventsOpen dropdown menu  
    *   Virtual Events  
    *   Icon Awards  
    *   Events Calendar  
    *   Submit Your Event

*   SponsoredOpen dropdown menu  
    *   SN Focus

*   Press ReleasesOpen dropdown menu  
    *   Latest  
    *   Post a Press Release

*   Job Board  
*   Work With UsOpen dropdown menu  
    *   Advertise  
    *   Editorial Calendar  
    *   Ad Portal  
    *   Contact Us

*   MoreOpen dropdown menu  
    *   About SpaceNews  
    *   FAQs  
    *   Contact Us
Open Search
Search for:  Search
*   TOPICS:  
*   Artemis  
*   SpaceX  
*   NASA  
*   Golden Dome  
*   Europe  
*   China  
*   Funding Rounds  
*   Civil  
*   Commercial  
*   Launch  
*   Military
Home / **NASA Assigns Crew for Space Shuttle Mission STS-120**
Posted inPress Release

# NASA Assigns Crew for Space Shuttle Mission STS-120
bySpaceRefJune 19, 2006 July 15, 2024
*   Share on X (Opens in new window)X  
*   Share on LinkedIn (Opens in new window)LinkedIn  
*   Share on Facebook (Opens in new window)Facebook  
*   Share on Reddit (Opens in new window)Reddit  
*   [Email a link to a friend (Opens in new window)Email](mailto:?subject=%5BShared%20Post%5D%20NASA%20Assigns%20Crew%20for%20Space%20Shuttle%20Mission%20STS-120&body=https%3A%2F%2Fspacenews.com%2Fnasa-assigns-crew-for-space-shuttle-mission-sts-120%2F&share=email)
NASA has assigned crew members to the space shuttle flight that will launch an Italian-built U.S. module for the International Space Station.
Air Force Col. Pamela A. Melroy will command the STS-120 mission to take the Node 2 connecting module to the station. Melroy, a veteran shuttle pilot, is the second woman to command a shuttle. Marine Corps Col. George D. Zamka will serve as pilot. The flight’s mission specialists will be Scott E. Parazynski, Army Col. Douglas H. Wheelock, Navy Capt. Michael J. Foreman and Paolo A. Nespoli, a European Space Agency astronaut from Italy. Zamka, Wheelock, Foreman and Nespoli will be making their first spaceflight.
STS-120 will be Melroy’s third shuttle flight. The native of Palo Alto, Calif., served as pilot of missions STS-92 in 2000 and STS-112 in 2002, both flights to the space station. Zamka, a native of Jersey City, N.J., has a bachelor’s from the U.S. Naval Academy, Annapolis, Md., and a master’s from the Florida Institute of Technology, Melbourne, Fla.
</excerpt>

## Search 8 — query: "Pamela Melroy born"
### Rank 1 of 23 — 0.80 (passed on)
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
### Rank 2 of 23 — 0.77
<excerpt title="Pamela Anne Melroy">
# Pamela Anne Melroy
Skip navigation
Open today: 10:00 - 16:00
*   Our Blog  
*   Space News  
*   Buy a Gift Voucher  
*   FAQs  
*   Jobs

*   Shopping basket  
*   Show search form



*    Plan & Explore

# Pamela Anne Melroy
### Before you Visit
*   Opening Times  
    *   How to Find Us  
    *   Ticket Prices  
    *   Gift Vouchers  
    *   Using Your Free Annual Pass  
    *   Groups

# Pamela Anne Melroy
### At the Centre
*   Sir Patrick Moore Planetarium  
    *   Tetrastar Spaceport  
    *   Rocket Tower  
    *   Galleries and Exhibitions  
    *   Collections  
    *   The Shop  
    *   Boosters Café

# Pamela Anne Melroy
### Accessibility
*   Digital Guide  
    *   Facilities & Access Guide  
    *   When to Visit  
    *   Sensory Sessions  
    *   Accessible Afternoons
Close menu
*   What's on  
*   Venue Hire  
*   Schools

*   Our Blog  
*   Space News  
*   Buy a Gift Voucher  
*   FAQs  
*   Jobs
Book Now Book Now
**Admission Tickets****Annual Pass Return Visit**
Toggle menu
Search for... Search Hide search form
1.   Home  
2.   News  
3.   Astronauts  
4.   Pamela Anne Melroy

# Pamela Anne Melroy
**Pamela Anne Melroy (born September 17, 1961) is a retired United States Air Force officer and a former NASA astronaut. She served as pilot on Space Shuttle missions STS-92 and STS-112 and commanded mission STS-120 before leaving the agency in August 2009.**
After serving as Deputy Program Manager, Space Exploration Initiatives with Lockheed Martin, Melroy joined the Federal Aviation Administration in 2011, where she was a senior technical advisor and director of field operations for the FAA’s Office of Commercial Space Transportation.
**In 2013, she left the FAA and joined DARPA as Deputy Director of the Tactical Technology Office.**
*
National Space Centre

# Pamela Anne Melroy
## Find Out First
Be the first to hear about new events, shows and the latest from space.
First name
Last name
Email address
I would like to receive updates about:
- [x] Family Events 

- [x] Evening/Adult Events 

- [x] Space Science News
_By clicking Confirm Signup, I agree to receive emails from the National Space Centre about the topics I’ve ticked. I can unsubscribe at any time, and the Centre will never share my information with a third party._
Confirm Signup
The National Space Centre, Exploration Drive, SPACE CITY, Leicester LE4 5NS  
Tel: [(0)116 261 0261](tel:(0)1162610261)
Email: [info@spacecentre.co.uk](mailto:info@spacecentre.co.uk)
* * *

# Pamela Anne Melroy
## Find Out First
### About
*   Jobs  
*   Press  
*   Contact Us  
*   Terms and Conditions of Sale  
*   Privacy Policy  
*   EDI Policy  
*   Modern Slavery Statement  
*   Ethics Policy

# Pamela Anne Melroy
## Find Out First
### Other NSC Sites
*   Venue Hire  
*   Education  
*   NSC Creative  
*   National Space Academy
</excerpt>
### Rank 3 of 23 — 0.76
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
### Rank 4 of 23 — 0.73
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
### Rank 5 of 23 — 0.35
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

## Search 9 — query: "Orlando Magic head coach list"
### Rank 1 of 46 — 0.73 (passed on)
<excerpt title="A spot in Orlando Magic history: What will new coach add to this lineup?">
#### Chris Jent
*   **Years:** 2005  
*   **Regular season:** 5-13  
*   **Postseason:** 0-0  
*   **Of note:** Interim; first-year assistant was thrust into head coaching job at age 35 after Davis was let go; only head coach in franchise history whose entire NBA head coaching career consists of this single stint with the Magic.

#### Brian Hill
*   **Years:** 2005-07  
*   **Regular season:** 76-88  
*   **Postseason:** 0-4  
*   **Of note:** Only coach with two separate stints with team; after going 36-46 in 2005-06, led the Magic to the postseason the following year for the first time in four years.
The relationship between Orlando Magic coach Stan Van Gundy and star player Dwight Howard was rocky at the end of their time together. (AP Photo/El Nuevo Herald, David Santiago)

#### Stan Van Gundy
*   **Years:** 2007-12  
*   **Regular season:** 259-135  
*   **Postseason:** 31-28  
*   **Of note:** Franchise leader in regular-season winning percentage (.657) and playoff wins; led Magic on a run to the 2009 NBA Finals, where they lost in five games to the Lakers; only became coach when Billy Donovan backed out of his contract to return to the University of Florida; now calls NBA games for Amazon Prime.

#### Jacque Vaughn
*   **Years:** 2012-15  
*   **Regular season:** 58-158  
*   **Postseason:** 0-0  
*   **Of note:** Oversaw start of post-Dwight Howard rebuild; when he was hired at age 37, he was the youngest coach in the NBA at the time; helped early development of Victor Oladipo and Nikola Vucevic.

#### James Borrego
*   **Years:** 2015  
*   **Regular season:** 10-20  
*   **Postseason:** 0-0  
*   **Of note:** Interim; won his debut, 103-97 over Lakers; Magic held first four opponents under 100 points; later became Hornets head coach and first full-time Hispanic head coach in NBA history.

#### Scott Skiles
*   **Years:** 2015-16  
*   **Regular season:** 35-47  
*   **Postseason:** 0-0  
*   **Of note:** Former Magic player resigned unexpectedly after just one season; team improved by 10 wins in his lone season; speculation centers on a rift with management that led to his departure.

#### Frank Vogel
*   **Years:** 2016-18  
*   **Regular season:** 54-110  
*   **Postseason:** 0-0  
*   **Of note:** Was hired for his track record with defense as coach of the Pacers; tenure was complicated by a front office in transition; later won 2020 NBA title with the Lakers in the Orlando pandemic bubble.

#### Steve Clifford
*   **Years:** 2018-21  
*   **Regular season:** 96-131  
*   **Postseason:** 2-8  
*   **Of note:** Oversaw 17-win improvement in his first season from previous year; ended six-year playoff drought in his first season.

#### Jamahl Mosley
*   **Years:** 2021-26  
*   **Regular season:** 189-221  
*   **Postseason:** 7-12  
*   **Of note:** Second in coach of the year voting in 2023-24; won two Southeast Division titles; fired after three consecutive first-round playoff exits.
</excerpt>
### Rank 2 of 46 — 0.71
<excerpt title="NBA Head Coaches">
Skip to content
InstagramTwitterLinkedInFacebookYouTube
*   HOME  
*   WHO WE ARE  
    *   ABOUT THE NBCA  
    *   NBCA LEADERSHIP  
    *   NBCA EXECUTIVES  
    *   MILESTONES

*   COACHES  
    *   HEAD COACHES  
    *   ASSISTANT COACHES

*   PARTNERS  
    *   CHARITABLE PARTNERS  
    *   CORPORATE PARTNERS

*   SPEAKING ENGAGEMENTS  
*   MEDIA  
    *   COACHES CORNER  
    *   AWARDS  
        *   CHUCK DALY LIFETIME ACHIEVEMENT AWARD  
        *   MICHAEL H. GOLDBERG NBCA COACH OF THE YEAR AWARD  
        *   TEX WINTER ASSISTANT COACH LIFETIME IMPACT AWARD  
        *   NBA COACH OF THE YEAR AWARD  
        *   NBA COACHES OF THE MONTH

    *   COACHES STORIES

*   NEWS

## NBA Head Coaches
NBA Head CoachesNBA Coaches Association2026-08-13T18:42:26+00:00
**EASTERN CONFERENCE**

## ATLANTIC DIVISION


## JOE
MAZZULLA
Boston Celtics
BIO

## JORDI
FERNÁNDEZ
Brooklyn Nets
BIO

## MIKE
BROWN
New York Knicks
BIO

## NICK
NURSE
Philadelphia 76ers
BIO

## DARKO
RAJAKOVIĆ
Toronto Raptors
BIO

## CENTRAL DIVISION


## TIAGO
SPLITTER
Chicago Bulls
BIO

## KENNY
ATKINSON
Cleveland Cavaliers
BIO

## J.B.
BICKERSTAFF
Detroit Pistons
BIO

## RICK
CARLISLE
Indiana Pacers
BIO

## TAYLOR
JENKINS
Milwaukee Bucks
BIO

## SOUTHEAST DIVISION


## QUIN
SNYDER
Atlanta Hawks
BIO

## CHARLES
LEE
Charlotte Hornets
BIO

## ERIK
SPOELSTRA
Miami Heat
BIO

## SEAN
SWEENEY
Orlando Magic
BIO

## BRIAN
KEEFE
Washington Wizards
BIO
**WESTERN CONFERENCE**

## NORTHWEST DIVISION


## DAVID
ADELMAN
Denver Nuggets
BIO

## CHRIS
FINCH
Minnesota Timberwolves
BIO

## MARK
DAIGNEAULT
Oklahoma City Thunder
BIO

## MICAH
NORI
Portland Trail Blazers
BIO

## WILL
HARDY
Utah Jazz
BIO

## PACIFIC DIVISION


## STEVE
KERR
Golden State Warriors
BIO

## TYRONN
LUE
Los Angeles Clippers
BIO

## JJ
REDICK
Los Angeles Lakers
BIO

## JORDAN
OTT
Phoenix Suns
BIO

## DOUG
CHRISTIE
Sacramento Kings
BIO

## SOUTHWEST DIVISION


## DUSTY
MAY
Dallas Mavericks
BIO

## IME
UDOKA
Houston Rockets
BIO

## TUOMAS
IISALO
Memphis Grizzlies
BIO

## JAMAHL
MOSLEY
New Orleans Pelicans
BIO

## MITCH
JOHNSON
San Antonio Spurs
BIO
Go to Top
</excerpt>
### Rank 3 of 46 — 0.65
<excerpt title="Orlando Magic Coaches">
# Orlando Magic Coaches
## Full Site Menu
*   Return to Top
*   Players**In the News**: V. Wembanyama, L. James, K. Durant, J. Embiid, J. Harden, S. Curry, L. Dončić... **All-Time Greats**: E. Hayes, J. Stockton, H. Olajuwon, W. Chamberlain, D. Schayes, J. Havlicek... **Active Greats**: L. James, G. Antetokounmpo, N. Jokić, J. Harden, S. Curry, K. Durant...   
*   Teams**Atlantic**: Toronto, Boston, New York, Brooklyn, Philadelphia **Central**: Cleveland, Indiana, Detroit, Chicago, Milwaukee **Southeast**: Miami, Atlanta, Charlotte, Washington, Orlando **Northwest**: Oklahoma City, Portland, Utah, Denver, Minnesota **Pacific**: Golden State, Los Angeles Clippers, Sacramento, Phoenix, Los Angeles Lakers **Southwest**: San Antonio, Dallas, Memphis, Houston, New Orleans   
*   Seasons2025-26, 2024-25, 2023-24, 2022-23, 2021-22, 2020-21, 2019-20 ...    
*   LeadersSeason Points, Career Rebounds, Active Assists, Yearly Steals, Progressive Blocks ...   Or, view "Trailers" for Season Field Goal Pct, or Career Blocks Per Game   
*   NBA ScoresYesterday's Games and Scores from any date in BAA/NBA or ABA history   
*   NBA SchedulesTeam Schedules and League Schedules   
*   NBA StandingsToday's Standings and Standings for any date in history   
*   Stathead**Player Finders**: Season Finder, Game Finder, Streak Finder, Span Finder **Team Finders**: Season Finder, Game Finder, Streak Finder, Span Finder **Other Finders**: Versus Finder, Shot Finder **College Tools**: Player Season Finder, Player Game Finder, Team Season Finder, Team Game Finder   
*   CoachesRichie Guerin, Rudy Tomjanovich, Jim O'Brien, Mike Fratello, Alvin Gentry ...    
*   AwardsNBA MVP, All-NBA, Defensive Player of the Year, Rookie of the Year, All-Rookie, Hall of Fame ...
</excerpt>
### Rank 4 of 46 — 0.65
<excerpt title="Orlando Magic Coaches">
# Orlando Magic Coaches
## Full Site Menu
*   NBA ContractsMain Index, Team Payrolls, Player Contracts, Glossary ...    
*   Playoffs2026 NBA Playoffs, 2025 NBA Playoffs, 2024 NBA Playoffs, 2023 NBA Playoffs, 2022 NBA Playoffs, 2021 NBA Playoffs, 2020 NBA Playoffs, Playoffs Series History ...    
*   All-Star Games2026 All-Star Game, 2025 All-Star Game, 2024 All-Star Game, 2023 All-Star Game, 2022 All-Star Game, 2021 All-Star Game, 2020 All-Star Game ...    
*   NBA Draft2026 Draft2025 Draft, 2024 Draft, 2023 Draft, 2022 Draft, 2021 Draft, 2020 Draft ...    
*   FrivolitiesPlayers who played for multiple teams(WNBA), Birthdays, Colleges, High Schools, Milestone Watch ...    
*   ExecutivesDaryl Morey, Masai Ujiri, Pat Riley, Danny Ainge, Jon Horst ...    
*   RefereesJoe Forte, Tony Brothers, Dan Crawford, Ron Olesiak, David Jones ...    
*   G League StatsPlayers, Teams, Seasons, Leaders, Awards ...    
*   International Basketball StatsPlayers, Teams, Seasons, Leaders, Awards ...    
*   WNBAPlayers, Teams, Seasons, Leaders, Awards, All-Star Games, Executives ...    
*   NBLPlayers, Teams, Seasons, Leaders, Awards ...    
*   AboutGlossary, Contact and Media Information, Frequently Asked Questions about the NBA, WNBA and Basketball, NBA Data Coverage, ABA Data Coverage, ...    
*   Immaculate Grid (Men's) and Immaculate Grid (Women's)Put your basketball knowledge to the test with our daily basketball trivia games. Can you complete the grids? 
*   Basketball-Reference.com Blog and Articles

# Orlando Magic Coaches
## We're Social...for Statheads
[](tel://888-512-8907)  
**Site Last Updated:** Thursday, November 19, 5:01AM
Question, Comment, Feedback, or Correction?
Subscribe to our Free Email Newsletter
Subscribe to Stathead Basketball: Get your first month FREE _Your All-Access Ticket to the Basketball Reference Database_
Do you have a sports website? Or write about sports? We have tools and resources that can help you use sports data. Find out more.

# Orlando Magic Coaches
## FAQs, Tips & Tricks
*   **Sports Reference Knowledge Base**  
*   Do you have a blog? Join our linker program.  
*   Watch our How-To Videos to Become a Stathead  
*   Subscribe to Stathead and get access to more data than you can imagine
All logos are the trademark & property of their owners and not Sports Reference LLC. We present them here for purely educational purposes. Our reasoning for presenting offensive logos.
Logos were compiled by the amazing SportsLogos.net.
Data Provided By  the official stats partner of the NBA, NHL and MLB.
Copyright © 2000-2026 Sports Reference LLC. All rights reserved.
The SPORTS REFERENCE, STATHEAD, IMMACULATE GRID, and IMMACULATE FOOTY trademarks are owned exclusively by Sports Reference LLC. Use without license or authorization is expressly prohibited.
*   Sports Reference ®Hub  
*   Baseball  
*   Football(college)  
*   Basketball(college)  
*   Hockey  
*   Soccer  
*   Blog  
*   Stathead ®  
*   Immaculate Grid ®
About • Conditions & Terms of Service • Advertise With Us • Jobs at SR • Basketball-Reference.com T-Shirts & Store • Your Privacy Choices
Sports Reference Purpose: We will be the trusted source of information and tools that inspire and empower users to enjoy, understand, and share the sports they love.
Privacy Policy • Gambling Revenue Policy • Accessibility Policy • Use of Data
</excerpt>
### Rank 5 of 46 — 0.64
<excerpt title="Orlando Magic Coaches">
# Orlando Magic Coaches
## 15 Coaches
|  | Regular Season | Playoffs |  
| --- | --- | --- |  
| Rk | Coach | From | To | Yrs | G | W | L | W/L% | W > .500 | Plyfs | G | W | L | W/L% | Conf | Champ |  
| 1 | Richie Adubato | 1997 | 1997 | 1 | 33 | 21 | 12 | .636 | 4.5 | 1 | 5 | 2 | 3 | .400 | 0 | 0 |  
| 2 | James Borrego | 2015 | 2015 | 1 | 30 | 10 | 20 | .333 | -5.0 |  |  |  |  |  |  |  |  
| 3 | Steve Clifford | 2019 | 2021 | 3 | 227 | 96 | 131 | .423 | -17.5 | 2 | 10 | 2 | 8 | .200 | 0 | 0 |  
| 4 | Chuck Daly | 1998 | 1999 | 2 | 132 | 74 | 58 | .561 | 8.0 | 1 | 4 | 1 | 3 | .250 | 0 | 0 |  
| 5 | Johnny Davis | 2004 | 2005 | 2 | 135 | 51 | 84 | .378 | -16.5 |  |  |  |  |  |  |  |  
| 6 | Matt Guokas | 1990 | 1993 | 4 | 328 | 111 | 217 | .338 | -53.0 |  |  |  |  |  |  |  |
</excerpt>

## Search 10 — query: "George D. Zamka born"
### Rank 1 of 62 — 0.86 (passed on)
<excerpt title="Astronaut Biography: George D. Zamka">
# Astronaut Biography: George D. Zamka
News
By NASA
Published October 18, 2007
When you purchase through links on our site, we may earn an affiliate commission. Here’s how it works.
STS-120 pilot George D. Zamka poses for his preflight photo.(Image credit: NASA.)
Share
*    Copy link   
*   Facebook  
*   X  
*   Reddit  
*   Pinterest  
*   Flipboard  
*   [Email](mailto:?subject=I%20found%20this%20webpage&body=Hi,%20I%20found%20this%20webpage%20and%20thought%20you%20might%20like%20it%20https://www.space.com/4479-astronaut-biography-george-zamka.html)
Share this article
Join the conversation
Follow us
Add us as a preferred source on Google
Newsletter
Subscribe to our newsletter
**NAME:****George D. Zamka******Colonel, USMC******NASA Astronaut**
**PERSONALDATA:** Born in1962 in Jersey City, New Jersey. Raised in New York City;Irvington, New York; Medellin, Colombia and Rochester Hills, Michigan. Married to the former Elisa P.Walker of Mississippi. They have two children. He enjoysweight lifting, running, bicycling, scuba and boating. His mother, Sofia Zamkaand brother Conrad P. Zamka both live in Florida. His father, Conrad Zamka resides in Indiana.
**EDUCATION:** Graduated from Rochester Adams High School, Rochester Hills Michigan, in 1980; received a Bachelor of Science degree inMathematics from the United States Naval Academy in 1984; received a Masters of Science degree inEngineering Management from the Florida Institute of Technology in 1997.
Latest Videos From Space
View more
Watch full video here:
**ORGANIZATIONS:** United States Naval Academy Alumni Association, Marine Corps Association,and Society of Experimental Test Pilots.
</excerpt>
### Rank 2 of 62 — 0.82
<excerpt title="George D. Zamka (Major, USMC)">
# George D. Zamka (Major, USMC)
## Astronaut George D. Zamka
Previous | Home | Next
NAME: George D. Zamka (Major, USMC)
NASA Astronaut (Pilot Candidate)
PERSONAL DATA: Born June 29, 1962 in Jersey City, New Jersey, but considers Rochester, Michigan to behis hometown. Married to the former Elisa P. Walker of Raymond, Mississippi. They have one child. Recreational interests include weight lifting, running, bicycling, scuba and boating. His mother, Sofia Zamka, resides in Lake Mary, Florida. His father, Conrad Zamka resides in Indianapolis, Indiana.
EDUCATION: Graduated from Rochester Adams High School, Rochester Michigan, in 1980; received a Bachelor of Science degree in Mathematics from the United States Naval Academy in 1984; received a Masters of Science degree in Engineering Management from the Florida Institute of Technology in 1997.
ORGANIZATIONS: United States Naval Academy Alumni Association, Marine Corps Association, and Society of Experimental Test Pilots.
SPECIAL HONORS: Navy Strike Air Medal (6), Navy Commendation Medal with Combat V, and various other military service and campaign awards. Distinguished Graduate, United States Naval Academy. Commodore’s list and Academic Achievement Award, Training Air Wing Five.

# George D. Zamka (Major, USMC)
## Astronaut George D. Zamka
EXPERIENCE: Zamka was commissioned as a Second Lieutenant in the United States Marine Corps following graduation from the United States Naval Academy in May 1984. He graduated from the Marine Corps Basic School in December 1984. Upon completion of Naval Aviator training he reported to Navy Attack Squadron VA-128 for initial A-6 training in August of 1987. He then reported to Marine All Weather Attack Squadron VMA(AW)-242 in El Toro, California. While assigned to VMA(AW)-242, Zamka made an overseas deployment to Japan, Korea, and the Philippines. He attended the Marine Aviation Warfare and Tactics Instructor Course and was assigned as the Squadron Weapons and Tactics Instructor. In 1990, he was selected for and completed F/A-18 conversion training and was assigned to Marine All Weather Fighter Attack Squadron VMFA(AW)-121, also in El Toro, California. He flew the F/A-18D Night Attack Hornet during overseas deployments to Japan, Korea, Singapore, and Southwest Asia. Zamka flew 66 combat missions over occupied Kuwait and Iraq during Desert Storm. In 1993 he served as a forward air controller with First Battalion, Fifth Marines in Camp Pendleton, California and the 31st Marine Expeditionary Unit (Special Operations Capable) aboard USS Belleau Wood in the Western Pacific. He was selected to attend the United States Air Force Test Pilot School class 94A and graduated in December 1994. Zamka was then assigned as an F/A-18 test pilot/project officer and the F/A-18 Operations Officer for the Naval Strike Aircraft Test Squadron (NSATS). While assigned to NSATS, Zamka flew a wide variety of tests in the F/A-18 Hornet to include high angle of attack, loads, flutter, and weapon system programs. Major Zamka returned to VMFA(AW)-121 in 1998 and was serving as the Aircraft Maintenance Officer, deployed to Iwakuni, Japan when selected for the astronaut program. He has logged over 2700 flight hours in more than 30 different aircraft.

# George D. Zamka (Major, USMC)
## Astronaut George D. Zamka
NASA EXPERIENCE: Selected by NASA in June 1998, he reported for training in August 1998. Astronaut Candidate Training includes orientation briefings and tours, numerous scientific and technical briefings, intensive instruction in Shuttle and International Space Station systems, physiological training and ground school to prepare for T-38 flight training, as well as learning water and wilderness survival techniques. Zamka is currently assigned to the Astronaut Office Shuttle Operations Branch. He will serve in technical assignments until assigned to a space flight.
</excerpt>
### Rank 3 of 62 — 0.79
<excerpt title="George D. Zamka Facts for Kids">
| Quick facts for kids George Zamka |  
| --- |  
|  |  
| Born | George David Zamka June 29, 1962 (age 64) Jersey City, New Jersey, U.S. |  
| Other names | Zambo |  
| **Space career** |  
| NASA astronaut |  
| Rank | Colonel, USMC |  
| Time in space | 28d 20h 32m |  
| Selection | NASA Group 17 (1998) |  
| Missions | STS-120 STS-130 |  
| Mission insignia |  |
**George David "Zambo" Zamka** (born June 29, 1962) is a former NASAastronaut and a retired pilot from the United States Marine Corps. He was a skilled pilot who flew over 30 different types of aircraft, logging more than 3,500 flight hours.
Zamka traveled to space twice. In 2007, he was the pilot of the Space Shuttle _Discovery_ on a mission to the International Space Station (ISS). Later, in 2010, he returned to space as the commander of the Space Shuttle _Endeavour_ for mission STS-130.

## Contents
*   Early Life and Education  
*   Career as a Marine Corps Pilot  
*   Journey to Becoming an Astronaut  
    *   STS-120: First Spaceflight  
    *   STS-130: Commanding a Mission

*   Awards and Recognition  
*   See also

## Early Life and Education
George David Zamka was born in Jersey City, New Jersey. Because of his family, he grew up in many different places, including New York City, Medellin, Colombia, and Rochester Hills, Michigan. He has Colombian and Polish family roots. In 1980, he graduated from Rochester Adams High School in Michigan.
For fun, Zamka enjoys weightlifting, running, biking, scuba diving, and boating. He is married and has two children.
In 1984, Zamka earned a Bachelor of Science degree in mathematics from the United States Naval Academy. Later, in 1997, he received a Master of Science degree in engineering management from the Florida Institute of Technology.

## Career as a Marine Corps Pilot
After graduating from the Naval Academy in 1984, Zamka became an officer in the United States Marine Corps. He trained to fly the A-6E Intruder attack aircraft. He later learned to fly the F/A-18D Hornet fighter jet.
During Operation Desert Storm in 1991, Zamka flew 66 combat missions. He also served as a forward air controller, helping to coordinate air attacks from the ground. In 1994, he graduated from the U.S. Air Force Test Pilot School, where he learned to fly and test new aircraft.
Zamka retired from the Marine Corps in August 2010 as a Colonel after nearly 30 years of service. After his military career, he became the chairman of the board for the National Association of Spaceports.

## Journey to Becoming an Astronaut
Zamka visiting the Planetarium of Bogotá in Colombia.
NASA selected Zamka to become an astronaut in June 1998. He started his training in August of that year. At NASA, he held important roles, including leading the training for the Space Shuttle program. He also supervised the new astronaut candidates who were selected in 2004.

## Journey to Becoming an Astronaut
### STS-120: First Spaceflight
Zamka's first trip to space was in October 2007. He served as the pilot for mission STS-120 aboard the Space Shuttle _Discovery_. The mission's main goal was to deliver a new module, called _Harmony_, to the International Space Station. This module provided more living and working space for the astronauts on the station.
</excerpt>
### Rank 4 of 62 — 0.79
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
### Rank 5 of 62 — 0.78
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

# Example 5
## Question
I'm working on a guide for a RPG released on the DS, which was co-developed in 2007 by Square Enix and another company named after a planet. I'm stuck on getting one of the Secret Reports - specifically, Day 5 during the week when you partner with a character who doesn't go by a nickname. What is the name of the boss I need to defeat?

## Expected answer
Cornix Canor

## Grade 0.00

## Search 1 — query: "RPG released on DS 2007 co-developed by Square Enix and company named after a planet"
### Rank 1 of 253 — 0.61 (passed on)
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
### Rank 2 of 253 — 0.56
<excerpt title="enix – The RPG Square - WordPress.com">
## The History of Dragon Quest
In 2003, Enix merged with former rival Square and Square Enix partnered with Dark Cloud developer Level-5 to release one of the most critically acclaimed and successful instalment in the series. Dragon Quest VIII: Journey of the Cursed King released on the monumental PlayStation 2 and propelled Dragon Quest into a beautiful 3D cel-shaded world. The exploration was vast, the voice acting engaging and everything else great from the series was carried over and improved to make it one of the PS2’s best RPGs. Dragon Quest VIII also overhauled the dialogue in the English releases which has been carried over into the remakes of earlier games and new releases over the past few years.
Having found success with Level-5, Square Enix worked with them again to develop Dragon Quest IX: Sentinels of the Starry Skies for the impressive Nintendo DS. Originally planned to be an action-RPG, loyal fans disliked this direction so much that the idea was scrapped and a turn-based battle system was restored. Implementing an interesting take on multiplayer in what is predominantly a single player experience, Dragon Quest IX took the series to new heights and arguably it’s most popular era in English countries.
Unfortunately in the years since, remakes of DQ IV, V and VI were released on the Nintendo DS by Nintendo themselves to a less popular response in North America and the Massively Multiplayer Online (MMO) Dragon Quest X, as well as spin offs such as Dragon Quest Monsters have stayed in Japan only. With such a rich history of quality RPGs it would be a shame to not have any more Dragon Quest games translated into English. There is still hope as the action/ adventure spin off Dragon Quest Heroes is in development for 2015 on The PlayStation 3 and 4 and the next mainline instalment Dragon Quest XI has been confirmed to be returning to a traditional RPG on consoles. So if you are a fan of the series or love a great classic turn-based RPG, the history of Dragon Quest is worth a look into.
Filed under Dragon Quest Series, Editorial
Tagged as akira toriyama, dragon quest, enix, history, level-5, localisation, rpg, square enix, video game, yuji horii
January 12, 2013 · 2:13 PM

## The Rise of SquareSoft (Part 4) – No Going Back
After defining and revolutionising RPGs on the original PlayStation, Square went head first into the next generation by beginning work on the tenth instalment in the Final Fantasy series developed exclusively for the PlayStation 2. With much more powerful hardware, Final Fantasy X saw the introduction of voice acting, more realistic facial animations, fully 3D environments (replacing the pre-rendered ones used in Final Fantasy VII, VIII and IX) and had three different composers producing the soundtrack including Nobuo Uematsu. Final Fantasy X was a huge success and was seen as a giant leap forward for the series, while still keeping the features fans enjoyed, such as an engrossing narrative, memorable characters, mini-games, turn-based battles and a gigantic world to explore.
During the early 2000s online gaming was growing in popularity and Square announced the next numbered Final Fantasy game would be a completely online experience. Final Fantasy XI allowed players to created their own online avatars and take on quests to develop their character and progress through the main storyline. Final Fantasy XI became the most profitable entry in series and is still in operation 10 years after it’s release with new developments expanding the game.
After the critical success in Japan of Vagrant Story and Hironobu Sakaguchi’s pleasure with Yasumi Matsuno’s work as a game director, Sakaguchi decided that he would entrust Matsuno with the next mainline Final Fantasy game. Co-directed by Matsuno and Hiroyuki Ito, Final Fantasy XII was a massive change in direction for an offline Final Fantasy game. It featured a seamless battle system with no random battles, free camera control, was based in the world of Ivalice from Final Fantasy Tactics and put heavy emphasis on a political storyline. Due to creating the new battle system completely from scratch, Final Fantasy XII had a very long development cycle of around 6 years and during the time Matsuno fell ill leading to his resignation from Square. Final Fantasy XII was completed after he left and was still meet with huge success.
</excerpt>
### Rank 3 of 253 — 0.49
<excerpt title="enix – The RPG Square - WordPress.com">
## Tag Archives: enix
December 23, 2014 · 10:31 PM

## The History of Dragon Quest
Before there was Final Fantasy… There was Dragon Quest. Taking inspiration from western developed RPGs such as Wizardry and Ultima, designer Yuji Horii’s original Dragon Quest game established many foundations of the console RPG genre. Collaborating with manga artist Akira Toriyama and composer Koichi Sugiyama, Dragon Quest has stayed fiercely loyal to it’s traditions resulting in 10 mainline games and a plethora of spin-off titles. Dragon Quest is so popular in Japan that most titles are released on a weekend or public holiday so not to effect school children and people going to work!
Published by Enix the first four Dragon Quest games were released on the original Nintendo Entertainment System and localised in North American under the name Dragon Warrior due to copyright. The Dragon Warrior name was kept all the way up to Dragon Quest VII outside of Japan. The NES instalments featured a fully explorable overworld, dungeons, a simple yet satisfying narrative and a turn-based battle system. Different to Square’s Final Fantasy series, Dragon Quest utilises a first-person view for combat which allowed focus on the detailed enemy designs.Dragon Quest I-IV were initially developed in collaboration with Chunsoft. Yuji Horii’s own studio Armor Project co-develops all the mainline instalments.
Moving onto the Super Nintendo, Enix released Dragon Quest V and VI in Japan only. Both titles wouldn’t make their appearance in English speaking countries until years later in remakes for the Nintendo DS. Again Chunsoft developed Dragon Quest V, but from Dragon Quest VI onwards, which was made by Heartbeat the series had a rotation of developers. Heatbeat would also go on to co-develop Dragon Quest VII on the original PlayStation with ArtePiazza (who themselves would develop many remakes of earlier titles in the series).The massive Dragon Quest VII was released in North America and the next few games would follow suit.

## The History of Dragon Quest
In 2003, Enix merged with former rival Square and Square Enix partnered with Dark Cloud developer Level-5 to release one of the most critically acclaimed and successful instalment in the series. Dragon Quest VIII: Journey of the Cursed King released on the monumental PlayStation 2 and propelled Dragon Quest into a beautiful 3D cel-shaded world. The exploration was vast, the voice acting engaging and everything else great from the series was carried over and improved to make it one of the PS2’s best RPGs. Dragon Quest VIII also overhauled the dialogue in the English releases which has been carried over into the remakes of earlier games and new releases over the past few years.
Having found success with Level-5, Square Enix worked with them again to develop Dragon Quest IX: Sentinels of the Starry Skies for the impressive Nintendo DS. Originally planned to be an action-RPG, loyal fans disliked this direction so much that the idea was scrapped and a turn-based battle system was restored. Implementing an interesting take on multiplayer in what is predominantly a single player experience, Dragon Quest IX took the series to new heights and arguably it’s most popular era in English countries.
Unfortunately in the years since, remakes of DQ IV, V and VI were released on the Nintendo DS by Nintendo themselves to a less popular response in North America and the Massively Multiplayer Online (MMO) Dragon Quest X, as well as spin offs such as Dragon Quest Monsters have stayed in Japan only. With such a rich history of quality RPGs it would be a shame to not have any more Dragon Quest games translated into English. There is still hope as the action/ adventure spin off Dragon Quest Heroes is in development for 2015 on The PlayStation 3 and 4 and the next mainline instalment Dragon Quest XI has been confirmed to be returning to a traditional RPG on consoles. So if you are a fan of the series or love a great classic turn-based RPG, the history of Dragon Quest is worth a look into.
Filed under Dragon Quest Series, Editorial
Tagged as akira toriyama, dragon quest, enix, history, level-5, localisation, rpg, square enix, video game, yuji horii
January 12, 2013 · 2:13 PM
</excerpt>
### Rank 4 of 253 — 0.45
<excerpt title="Square-Enix Party 2007 News">
Square-Enix is hosting the Square-Enix Party 2007 this weekend, and for those of you who can't fly all the way to Japan, we've decided to help you out and show you what Square-Enix has in stock for 2007 and the future.
Let's start talking about Final Fantasy IV. Earlier this week, Square announced a 3D DS remake of the classic Final Fantasy RPG. During the SE Party, it was revealed that the game developer would be a studio called Matrix, which had previously worked in the development of FF III for the DS. Takashi Tokita will work as the executive producer of FF IV, instead of Hiromichi Tanaka. Asano Tomiya will return as the producer and Hiroyuki Itou will be the battle system supervisor. The Final Fantasy IV remake will also include voice acting.
New details regarding Final Fantasy Dissidia were also unveiled. During the SE Party, a trailer featuring a fierce battle between the Warrior of Light and Garland from Final Fantasy I was shown. The trailer then showed another fight, this time between Final Fantasy IX's Kuja and Zidane. As if those two battles weren't enough, just before the trailer ended, a silhouette of a man looking a lot like Sephiroth appeared standing on top of molten lava. Final Fantasy Dissidia will be released for the PSP.
Furthermore, a new trailer for Crisis Core showed the battle between Sephiroth, Angeal and Genesis and highlighted the scene were Zack is shot just outside of Midgar. Square-Enix also announced that they will be giving away interesting items such as a PSP machine when Final Fantasy Crisis Core hits store shelves later this year in Japan.
Final Fantasy XI fans will be happy to know that the new expansion pack will be called Crusaders of Altana in Japan and the North-American version will be named Wings of the Goddess. Square-Enix said that Crusaders of Altana will be released sometime in winter 2007.
A new trailer for Final Fantasy XIII was shown during the SE Party. Shiva and a creature similar to Ifrit were depicted among a couple of other familiar scenes. A new Final Fantasy Versus XIII trailer was unveiled. After a battle with some soldiers, the game's main character entered a building where he encountered a man dressed in a white robe. Before the trailer ended, the two men started a vicious battle.

Last but not least, the secret ending movie of Kingdom Hearts II Final Mix+ served as an introduction to fans waiting to hear more about the new KH project. After the movie ended, a screen appeared and said that new information would be available at the Tokyo Game Show 2007.
Stay sharp for more information regarding the Square-Enix Party 2007, here at RPGSite.
</excerpt>
### Rank 5 of 253 — 0.32
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

## Search 2 — query: "Square Enix Jupiter DS 2007 co-developed"
### Rank 1 of 67 — 0.65 (passed on)
<excerpt title="The World Ends with You[c] is an action role-playing game co-developed by ...">
•
Follow
* * *
The World Ends with You[c] is an action role-playing game co-developed by Square Enix and Jupiter for the Nintendo DS. Set in the modern-day Shibuya shopping district of Tokyo, The World Ends with You features a distinctive art style and urban fantasy elements inspired by Shibuya and its youth culture. Development was inspired by elements of Jupiter’s previous handheld game, Kingdom Hearts: Chain of Memories. It was released in Japan in July 2007, and in PAL regions and North America in April 2008. Later, an enhanced port by h.a.n.d. for mobile devices was released in 2012 under the title The World Ends with You: Solo Remix, while another enhanced port for the Nintendo Switch was released worldwide in 2018 under the title The World Ends with You: Final Remix.  
#twewy#ds#nintendo#squareenix#theworldendswithyou
Ts was all i played for like a month
Reply
Broooo I ordered it on eBay not knowing it would be in Japanese now I can't understand a thing 😭
Reply
Looks gay
Reply
The game with the best hardware use
Reply
TWEWY mentioned 🥹✨️ One of my biggest obsessions in the last decade (started with Solo Remix back in 2016✌️😅)
1 like
Reply
Behold, one of the top 5 games of all time
14 likes
Reply
PEAKKK
1 like
Reply
TEXTBOOK DEFINITION OF LUDONARRATIVE HARMONY
2 likes
Reply
Peak.
1 like
Reply
Twewy🔥
1 like
Reply
Greatest game of all time 🗣️
1 like
Reply
2 likes
Reply
2.5K 47
</excerpt>
### Rank 2 of 67 — 0.62
<excerpt title="The World Ends with You (game) | Square Enix Wiki - Fandom">
_**The World Ends with You**_
_{{{romaji}}}_  
**Developer(s)**Square Enix   
Jupiter  
**Publisher(s)**Square Enix  
**Release date(s)**  
**Genre**Action role-playing  
**Game modes**Single-player + 2-4 player Wireless DS Multi-Card Play  
**Ratings**CERO: A
ESRB: T
PEGI: 12+  
**Platform(s)**Nintendo DS
**The World Ends With You**,known in Japan as Subarashiki Kono Sekai (すばらしきこのせかい: It's a Wonderful World), is an action RPG released for the Nintendo DS console. Character designs are by Tetsuya Nomura and Gen Kobayashi.
The Japanese version was released on July 27, 2007, the European on April 18, 2008, and the North American version on April 22, 2008.

## Story[]
The story begins with Neku Sakuraba, a 15 year-old boy who wakes up in Shibuya, a shopping district of Tokyo, Japan. As he wonders why he's there, he opens his hand and realizes that he is holding a strange black badge. After flipping it it in his hand, the thoughts of the people around him began to enter his mind. Surprised, Neku realizes that he is able to read the minds of others, and thinks that it's because of the pin.
A cellphone rings in his pocket, and he can't remember if it's his or not. A short text message appears: "Reach 104. You have 60 minutes. Fail, and face erasure. -The Reapers". After discovering that he's unable delete the message, a timer of 60:00 minutes is burned onto his hand.
Neku is in Shibuya to play the Reapers' Game, a deadly game which spans a total of 7 days. All participants of this game have a "Player Pin", a pin with a skull embedded on it. The Reapers' Game has some certain rules and regulations, which prevent him from leaving the Shibuya district. If Neku is unable to complete the game and survive the 7 days, he will be erased from existence along with Shiki Misaki, his partner in the game.
The Reapers watch over their actions and force them to play each mission. In order to survive in Shibuya, Neku and Shiki have to defeat the "Noise", physical manifestations of people's negative thoughts, emotions, and feelings. The Noise are based on various animals and can also take the forms of objects and historical monuments in Shibuya.
Neku's psychic talents are essential not only to gather clues and hints from the people, but to also detect the Noise that sweep through the roads of Shibuya. During their week in Shibuya, Neku and Shiki run into other people who have become involved in the Reapers' Game, such as Joshua, Beat, and Rhyme.

## Characters[]
*   Neku Sakuraba  
*   Shiki Misaki  
*   Joshua  
*   Beat  
*   Rhyme

## Gameplay[]
The World Ends with You has an ispired gameplay to Kingdom Hearts: Chain of Memories.

## Gameplay[]
### Features[]
In the game, there is a pin collection system that allows Neku to use new abilities and skills obtained by collecting badges scattered throughout Shibuya, either through defeating Noise, buying them in stores, or by evolving them from other badges. Different pins mean different abilities. Players can also buy clothing and food for Neku and his partners in the stores located throughout Shibuya to increase their status points or for recovery.
A mini-game called Tin Pin Slammer is available throughout the game, which uses the pins collected from the main storyline.

## Music[]
The musical score in the game is composed by Takeharu Ishimoto. It includes a large variety of music with an influence of hip hop and techno. The main theme of the game is "Lullaby For You" by Japanese pop artist, Jyongri. Various vocal artists featured in the game includes SAWA, Makiko Noda, Leah, Ayuko Tanaka, Londeil "Taz" Hicks, Mai Matsuda, WAKAKO, Nurlie Nurly, Andy Kinlay, Hanaeryca, and Cameron Strother. The official soundtrack of the game was released on August 22, 2007.
</excerpt>
### Rank 3 of 67 — 0.55
<excerpt title="The World Ends with You">
_The World Ends with You_ was developed by the same team that created the _Kingdom Hearts_ series, with input from Jupiter,[[26]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-29) the company that developed _Kingdom Hearts: Chain of Memories_ for the Game Boy Advance. Development of the game started two and a half years before its Japanese release, during the development of _Kingdom Hearts II_ and as development of _Chain of Memories_ was concluding.[[27]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-roundtable1-30) At that time, Nintendo revealed their next handheld system, the Nintendo DS, but was not yet available to the market; Square Enix requested the team to develop a game specifically for the handheld system.[[27]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-roundtable1-30)

The creative team — consisting of director Tatsuya Kando, co-director Tomohiro Hasegawa, planning director Takeshi Arakawa, and creative producer and character designer Tetsuya Nomura — were able to experience the DS during the "Touch DS" event in November 2004.[[28]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-roundtable2-31) From this demonstration, they had envisioned a version of _Chain of Memories_ in which the card game aspects would be present on the bottom screen and an action role-playing game on the top. As they continued to work on the game, the developers realized that they wanted to use the touchscreen more, to make "a game that can only be played on the DS".[[28]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-roundtable2-31) However, they also encountered the problem that by focusing heavily on the touchscreen, the top screen would be ignored. From this, the idea of the dual-screen battle system arose.[[28]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-roundtable2-31) Several other options were explored for the top screen gameplay, including command-based battles or a rhythm game, but once they reviewed the game from the eyes of the player, they ultimately settled on the card-game approach with the player having the option to control the game if they wanted to.[[29]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-postmortem-32)

Even with the completion of the Japanese version of the game, the team felt the dual-screen system was too much for overseas audiences, and attempted to change the card-game mechanic into a special meter that would fill up with normal attacks from Neku, but this was not completed in time for release.[[29]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-postmortem-32) The team was able to alter the "information overload" of the numerous tutorials at the start of the game in the North American release, reducing the amount of text presented as well as allowing the tutorials to be skipped. The "Active Encounter" system, the ability for the player to select when and how to go into battle, was developed specifically to avoid the issues of "grinding" that are common with most standard RPG systems.[[29]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-postmortem-32) While they included the mechanics of being able to scan non-playable characters to see their thoughts, the team was not able to integrate this mechanic more into the game.[[29]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-postmortem-32)
</excerpt>
### Rank 4 of 67 — 0.53
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
| Release | July 27, 2007 |  
| Genre | Action role-playing |  
| Modes | Single-player, multiplayer (_Final Remix_) |
_**The World Ends with You**_[[c]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-4) is an action role-playing game co-developed by Square Enix and Jupiter for the Nintendo DS. Set in the modern-day Shibuya shopping district of Tokyo, _The World Ends with You_ features a distinctive art style and urban fantasy elements inspired by Shibuya and its youth culture. Development was inspired by elements of Jupiter's previous handheld game, _Kingdom Hearts: Chain of Memories_. It was released in Japan in July 2007, and in PAL regions and North America in April 2008. Later, an enhanced port by [h.a.n.d.](https://en.wikipedia.org/wiki/H.a.n.d. "H.a.n.d.") for mobile devices was released in 2012 under the title _**The World Ends with You: Solo Remix**_, while another enhanced port for the Nintendo Switch was released worldwide in 2018 under the title _**The World Ends with You: Final Remix**_.

In the story, protagonist Neku Sakuraba and his allies are forced to participate in a game that will determine their fate. The battle system uses many of the unique features of the Nintendo DS, including combat that takes place on both screens, and attacks performed by certain motions on the touchscreen or by shouting into the microphone. Elements of Japanese youth culture, such as fashion, food, and cell phones, are key aspects of the missions and character progression.
_The World Ends with You_ received critical acclaim upon release, with critics praising the graphics, soundtrack, and integration of gameplay into the Shibuya setting, with minor criticism directed at its learning curve and occasionally imprecise touch-screen controls. It is regarded as one of the best Nintendo DS games, and one of the greatest video games ever made. In the first week of its release, the game was the second best-selling DS title in Japan, and the top-selling DS title in North America. Shiro Amano, writer and artist of the _Kingdom Hearts_manga, later created a manga based on the video game. An anime adaptation by Square Enix, DOMERICA, and Shin-Ei Animation aired from April 10 to June 26, 2021.
The iPhone, iPad and Android versions were removed in July 2023.[[2]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-5)
A sequel, _Neo: The World Ends with You_, was released worldwide on Nintendo Switch and PlayStation 4 on July 27, 2021, and on Windows on September 28.
_The World Ends with You_ is an action role-playing game arranged into three chapters based on the three weeks that Neku is involved in the Reapers' Game, with each chapter further divided by each day of the week. The player controls Neku and his partner as they explore Shibuya to complete each day's mission. Although most missions require completion within a certain time for Neku and his partner, this timer is not correlated to the passage of time for the player.[[3]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-eurogamer_review-6)
</excerpt>
### Rank 5 of 67 — 0.49
<excerpt title="Jupiter Corporation - Picross Wiki">
_**Jupiter Corporation**_
Logo  
Founded June 11, 1992  
First nonogram release _Mario's Picross_ (1995)  
Latest nonogram release _Picross S: Konami Antiques Edition_ (2026)
_**Jupiter Corporation**_ (株式会社ジュピター _Kabushiki-gaisha Jupitā_), better known as simply _**Jupiter**_, is a Japanese video game company, and the main developers for the _Picross_ franchise of video games.

*   **_Mario's Picross_ (Game Boy, 1995)** - Co-developed with [Ape Inc.](https://picross.miraheze.org/wiki/Creatures_Inc. "Creatures Inc."), published by Nintendo  
*   **_Tamori no Picross_ (Satellaview, 1995)** - Co-developed with Ape Inc., published by Nintendo  
*   **_Mario no Super Picross_ (Super Famicom, 1995)** - Co-developed with Ape Inc., published by Nintendo  
*   **_NuPa: Numeric Paint Puzzle_ (PlayStation, 1996)** - Published by Tomy Company, Ltd.  
*   **_Picross 2_ (Game Boy, 1996)** - Co-developed with [Creatures Inc.](https://picross.miraheze.org/wiki/Creatures_Inc. "Creatures Inc."), published by Nintendo  
*   **_Satella de Picross_ (Satellaview, 1997)** - Published by Nintendo &St.GIGA  
*   **_Picross NP_ series (Super Famicom, 1999-2000)** - Co-developed and published by Nintendo  
*   **_Picross DS_ (Nintendo DS, 2007)** - Published by Nintendo  
*   **_Puzzlun_ (iOS, Android, Japanese phones, 2011)** - Published by MTI Ltd.  
*   **_Picross e_ series (Nintendo 3DS, 2011-2018)** - Self-published  
*   **_Club Nintendo Picross_ (Nintendo 3DS, 2012)** - Published by Nintendo  
*   **_Pictlogica Final Fantasy_ (iOS, Android, Nintendo 3DS, 2013)** - Published by Square Enix  
*   **_Club Nintendo Picross+_ (Nintendo 3DS, 2014)** - Published by Nintendo  
*   **_Smapic_ (iOS, Android, 2014)** - Self-published  
*   **_Pokémon Picross_ (Nintendo 3DS, 2015)** - Published by The Pokémon Company
</excerpt>

## Search 3 — query: "The World Ends with You "Secret Report" Day 5 boss"
### Rank 1 of 108 — 0.93 (passed on)
<excerpt title="how to find every Boss Noise, and get the secret ending">
It wouldn't be a TWEWY game without Secret Reports, and initially the**NEO: The World Ends With You Secret Reports**these seem like the most confusing to find yet. Luckily, this page is here to help you with the **secret report locations** and **finding every boss noise** to get you to the **NEO secret ending**.
Video 4
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
### Rank 2 of 108 — 0.92
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
### Rank 3 of 108 — 0.89
<excerpt title="Empty Urban Legends (Week 1, Day 5) | The World Ends With You | Fandom">
## Plot[]
The two reach Spain Hill and try to Erase the Noise but it becomes quickly clear that there are too many Noise in the area. They notice that Ai and Mina having an argument about something nearby and realize that their negative energy is attracting the Noise. The two's argument is stemmed from Ai's crush on Makoto. Mina had been talking with Makoto and found out that he wanted tickets to the following week's Slam-Off at Molco. So she had purchased tickets for him and Ai to go together. But unbeknownst to Mina, Ai had seen them together that day and assumed that Mina was trying to steal Makoto for herself.Based on scanning alone, it wasn't clear what Mina's true intentions were and Neku and Shiki believe what Ai does. Shiki doesn't feel that Ai should know what they see as the truth but Neku feels that it has to be said. He imprints of Ai to make her suggest that her and Mina play Reaper Creeper. Throughout the game of Reaper Creeper, Ai gets progressively madder at Mina and eventually tells her that she saw her and Makoto together. It's at this point that Mina comes clean with her plan. This shocks Ai and makes her apologize for her behavior but Mina also sees herself at fault for lying. With their argument now over, Neku and Shiki are able to Erase all the Noise in the area. After having seen Ai and Mina make up, it pushes Neku and Shiki to do the same. Neku finally expresses sadness for [Rhyme](https://twewy.fandom.com/wiki/Raimu_%22Rhyme%22_Bito "Raimu \"Rhyme\" Bito")'s Erasure.But then, they are confronted by Yodai Higashizawa who introduces himself as the Game Master. He came there because he was drawn to the negative emotions that Shiki felt. He then drew these out, talking about the jealousy, envy, and selfishness that she feels. He tells her that none of these facts about her will change if she is restored to life. This causes Shiki to run off but Neku is left confused about Higashizawa's final words. Higashizawa then confirms to Neku that he is dead and that The Reapers' Game is an examination to see if he is worthy at another chance at life. Higashizawa then leaves Neku, who is alone and in complete disbelief.

## Walkthrough[]
After the opening scene, move to the right where a businessman in a black suit stands. He’ll play Reaper Creeper; move the coin to any of the three spots, as the choice won’t mean much in particular. Remember to do it slowly as if the coin moves too fast, the man will believe he bumped the paper and retry. After playing, Neku and Shiki will receive the meme “Reaper Creeper”. The route to Spain Hill is blocked by a Reaper who will only put the wall down when two of the biggest Noise symbols are defeated. After fighting them, the Reaper will clear the route.At Spain Hill, fight some noise until Neku and Shiki talk about how the Noise won’t stop coming and the source is revealed to be two girls, Mina and Ai. Scan them and erase some of the orange Noise surrounding them. After the fight, talk to them and imprint “Reaper Creeper” on Ai. She’ll play Reaper Creeper with Mina; there’s no benefit to any of the choices over each other, but choosing White for all questions will get Mr. Ducky, needed for the post-game’s Secret Report. After the conversation ends and Ai and Mina make up, finish off the last Noise in the area.When the final Noise is erased, a Circle Pit Grizzly will attack. Defeat it to finish the chapter.
</excerpt>
### Rank 4 of 108 — 0.88
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
### Rank 5 of 108 — 0.88
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

## Search 4 — query: "The World Ends with You partner characters names"
### Rank 1 of 88 — 0.82 (passed on)
<excerpt title="The World Ends with You">
A player in the UG is invisible to the living in the RG, though one can sometimes read and influence their thoughts. The UG is frequented by creatures called "Noise", which are attracted by the negative feelings of the living. To progress in the Reapers' Game, players are often required to defeat Noise by killing or "erasing" them.[[4]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-ign_review-7) However, each Noise exists in two parallel universes, or "zones", simultaneously, and can only be defeated by two players simultaneously fighting and defeating the Noise from these separate zones. To do so, players are required to form a pact with another player to survive the Noise.[[11]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-Noise_zones-14) Players receive assignments via text messages sent to their cell phones, and their right hands are imprinted with a countdown indicating the time left in the mission.[[4]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-ign_review-7) After a day's mission is complete, the remaining players find themselves at the start of the next day's mission, having no sense of the time that has passed in between.

The player controls Neku Sakuraba (桜庭 音操, _Sakuraba Neku_; ネク _Neku_), an initially asocial teenage boy who claims that he does not "get" people, and rarely interacts with others at first. Computer-controlled characters make up the rest of the cast, which includes players paired with Neku.[[11]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-Noise_zones-14) In the first Game, Neku is paired with Shiki Misaki (美咲 四季, _Misaki Shiki_; シキ _Shiki_), a teenage girl who takes on the form of her best friend, as her physical appearance was her price of entry for the Game.[[12]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-15) In the second Game, Neku's partner is an intelligent and sly teenage boy, Yoshiya Kiryu (桐生 義弥, _Kiryū Yoshiya_), who prefers to be called Joshua (ヨシュア, _Yoshua_). Neku's final partner is Daisukenojo Bito (尾藤 大輔之丞, _Bitō Daisukenojō_), originally a player and ex-Reaper who calls himself "Beat" (ビイト, _Biito_).[[13]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-16) Beat became a Reaper to find a way to bring his younger sister, Raimu Bito (尾藤 来夢, _Bitō Raimu_) (nicknamed "Rhyme" (ライム, _Raimu_)), back to life, as she had sacrificed herself to save him from a Noise attack.[[14]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-17)Sanae Hanekoma (羽狛 早苗, _Hanekoma Sanae_; ハネコマ _Hanekoma_), the Producer, bound her soul to a pin from which her Noise could be summoned, and gave it to Beat. The final Game Master, Mitsuki Konishi (虚西 充妃, _Konishi Mitsuki_; コニシ _Konishi_), crushes her Noise form and transforms it back into a pin.
</excerpt>
### Rank 2 of 88 — 0.80
<excerpt title="The World Ends with You">
The player controls Neku Sakuraba (桜庭 音操, _Sakuraba Neku_; ネク _Neku_), an initially asocial teenage boy who claims that he does not "get" people, and rarely interacts with others at first. Computer-controlled characters make up the rest of the cast, which includes players paired with Neku.[[11]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-Noise_zones-14) In the first Game, Neku is paired with Shiki Misaki (美咲 四季, _Misaki Shiki_; シキ _Shiki_), a teenage girl who takes on the form of her best friend, as her physical appearance was her price of entry for the Game.[[12]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-15) In the second Game, Neku's partner is an intelligent and sly teenage boy, Yoshiya Kiryu (桐生 義弥, _Kiryū Yoshiya_), who prefers to be called Joshua (ヨシュア, _Yoshua_). Neku's final partner is Daisukenojo Bito (尾藤 大輔之丞, _Bitō Daisukenojō_), originally a player and ex-Reaper who calls himself "Beat" (ビイト, _Biito_).[[13]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-16) Beat became a Reaper to find a way to bring his younger sister, Raimu Bito (尾藤 来夢, _Bitō Raimu_) (nicknamed "Rhyme" (ライム, _Raimu_)), back to life, as she had sacrificed herself to save him from a Noise attack.[[14]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-17)Sanae Hanekoma (羽狛 早苗, _Hanekoma Sanae_; ハネコマ _Hanekoma_), the Producer, bound her soul to a pin from which her Noise could be summoned, and gave it to Beat. The final Game Master, Mitsuki Konishi (虚西 充妃, _Konishi Mitsuki_; コニシ _Konishi_), crushes her Noise form and transforms it back into a pin.

Besides the Composer and the Conductor, there are other high-ranking Reapers.[[15]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-18) For each week of the Game, Game Masters are assigned by the Conductor to lead the opposition to the players. Of the Game Masters opposing Neku, Sho Minamimoto (南師 猩, _Minamimoto Shō_; ミナミモト _Minamimoto_) is the most dangerous, as he willingly circumvents the rules in an attempt to supplant the Composer.[[16]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-19) While participating in the Games to earn promotions for their performance, the Reapers' goal is to ascend to the highest form of spiritual existence, the Angels.[[17]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-20) Angels supervise the Games and, if the stakes of a Game are particularly high, they send down one of their own to serve as the Producer.[[18]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-21) For the three weeks of the game's story, Sanae Hanekoma is the Producer. Disguised as a Shibuya café owner, he guides new players and narrates the "Secret Reports", which are obtained by completing additional missions after completing the game.
</excerpt>
### Rank 3 of 88 — 0.80
<excerpt title="The World Ends with You">
Besides the Composer and the Conductor, there are other high-ranking Reapers.[[15]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-18) For each week of the Game, Game Masters are assigned by the Conductor to lead the opposition to the players. Of the Game Masters opposing Neku, Sho Minamimoto (南師 猩, _Minamimoto Shō_; ミナミモト _Minamimoto_) is the most dangerous, as he willingly circumvents the rules in an attempt to supplant the Composer.[[16]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-19) While participating in the Games to earn promotions for their performance, the Reapers' goal is to ascend to the highest form of spiritual existence, the Angels.[[17]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-20) Angels supervise the Games and, if the stakes of a Game are particularly high, they send down one of their own to serve as the Producer.[[18]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-21) For the three weeks of the game's story, Sanae Hanekoma is the Producer. Disguised as a Shibuya café owner, he guides new players and narrates the "Secret Reports", which are obtained by completing additional missions after completing the game.

The game's story follows Neku over the three weeks that he plays the Game, paired with partners Shiki, Joshua, and Beat for each week, respectively. Neku is initially confused, as he does not know how he died or how he arrived at the UG. As he develops friendships with his partners, he starts to understand the rules of the Game. After the first week, only Shiki is allowed to return to the living, and she promises to meet Neku at the statue of Hachikō.[[19]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-22)[[20]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-23) He also recovers his entry fee, which was his memories, except for the events leading up to his death. However, Shiki has become what Neku values most, and she is used as his new entry fee for the second week; in addition, Beat defects to the Reapers in hopes of finding a way to resurrect Rhyme after she sacrifices herself to save him. During the second week, Neku recalls small details of his death; he eventually realizes that Sho Minamimoto, one of the Reapers he faced during the Game, shot him. At the end of the second week, Joshua seemingly sacrifices himself to save Neku from an explosion Minamimoto causes.
</excerpt>
### Rank 4 of 88 — 0.73
<excerpt title="The World Ends with You">
The game's story follows Neku over the three weeks that he plays the Game, paired with partners Shiki, Joshua, and Beat for each week, respectively. Neku is initially confused, as he does not know how he died or how he arrived at the UG. As he develops friendships with his partners, he starts to understand the rules of the Game. After the first week, only Shiki is allowed to return to the living, and she promises to meet Neku at the statue of Hachikō.[[19]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-22)[[20]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-23) He also recovers his entry fee, which was his memories, except for the events leading up to his death. However, Shiki has become what Neku values most, and she is used as his new entry fee for the second week; in addition, Beat defects to the Reapers in hopes of finding a way to resurrect Rhyme after she sacrifices herself to save him. During the second week, Neku recalls small details of his death; he eventually realizes that Sho Minamimoto, one of the Reapers he faced during the Game, shot him. At the end of the second week, Joshua seemingly sacrifices himself to save Neku from an explosion Minamimoto causes.

Because Joshua was never actually dead, the Game is nullified and Neku is forced to play the game a third time. His entry fee this time is all of the other players, meaning he cannot form any pacts and stands no chance against the Noise; however, Beat defects from the Reapers and rejoins Neku. Neku and Beat find that the Reapers and the population of Shibuya are wearing special red pins that brainwash them into thinking the same thoughts. Without any missions to complete, the two venture to the fabled "Shibuya River", which Joshua was looking for during the second week. At the river, they find Megumi Kitaniji (北虹 寵, _Kitaniji Megumi_; キタニジ _Kitaniji_), the Game's Conductor, who explains that he created the red pins in an attempt to remake Shibuya, which the Composer challenged him to do. If he fails, both he, and as a price for losing the Game, Shibuya, will be erased.[[21]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-24)[[22]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-25)
Joshua reappears and reveals himself to be the Composer, returning to Neku the missing part of his memory of his death: Joshua was the one who shot Neku and chose him to be his proxy in his challenge with Kitaniji. Minamimoto, who had been trying to usurp the position of Composer, attempted to kill Joshua in his weakened state as a human. After Kitaniji fails to defeat Neku by using his friends against him, Joshua gives Neku one last challenge: to shoot Joshua to determine the fate of Shibuya. Neku is too conflicted to make a choice, and Joshua shoots him down.[[23]](https://en.wikipedia.org/wiki/The_World_Ends_with_You#cite_note-26) Neku finds himself back at the scramble crossing, confused but alive.
</excerpt>
### Rank 5 of 88 — 0.71
<excerpt title="Which was y'all favorite partner : r/TWEWY">
# More posts you may like
*   "Annoyingly, Joshua is nothing like your last partner, Shiki." r/TWEWY•4y ago    ### "Annoyingly, Joshua is nothing like your last partner, Shiki."     419 upvotes ·36 comments
* * *
*   I love her r/wbycritics•7mo ago    ### I love her     160 upvotes ·9 comments
* * *
*   Wyatt r/DailyRankingsDrama•9d ago    ### Wyatt      2 upvotes ·8 comments
* * *
*   Favorite couple that are perfect for each other but other people don’t think so r/FavoriteCharacter•27d ago    ### Favorite couple that are perfect for each other but other people don’t think so      42 upvotes ·10 comments
* * *
*   His & Her's 🫶🏻 r/toyotasequoia•10mo ago    ### His & Her's 🫶🏻     109 upvotes ·14 comments
* * *
*   (Loved trope) Couple who actually love eachother r/TopCharacterTropes•4mo ago    ### (Loved trope) Couple who actually love eachother      184 upvotes ·96 comments
* * *
*   Who is your favorite couple of all time? r/FavoriteCharacter•8mo ago    ### Who is your favorite couple of all time?     43 upvotes ·84 comments
* * *
*   A duo I can guarantee you've never seen before r/YoutubeThumbs•9d ago    ### A duo I can guarantee you've never seen before     83 upvotes ·22 comments
* * *
*   I LOVE HER r/wbycritics•4mo ago    ### I LOVE HER     276 upvotes ·36 comments
* * *
*   Similar YouTubers but WLW? r/danandphil•17d ago    ### Similar YouTubers but WLW?    48 upvotes ·23 comments
* * *

# More posts you may like
*   So, i'm curious, which partner in TWEWY, would you pick if you had the option? Neku, Beat, Rhyme, Shiki, or Josh? r/TWEWY•2y ago    ### So, i'm curious, which partner in TWEWY, would you pick if you had the option? Neku, Beat, Rhyme, Shiki, or Josh?     96 upvotes ·26 comments
* * *
*   Vinny's thoughts on June's CM r/wotv_ffbe•5y ago    ### Vinny's thoughts on June's CM     15 upvotes ·12 comments
* * *
*   Which support champion do you dislike? r/supportlol•6y ago    ### Which support champion do you dislike?    46 upvotes ·68 comments
* * *
*   My Newest Favorite "Couple" !! r/WoT•2mo ago    Spoiler ### My Newest Favorite "Couple" !!    33 upvotes ·18 comments
* * *
*   Well, there is a player here. r/TWEWY•4mo ago    ### Well, there is a player here.      416 upvotes ·15 comments
* * *
*   [[Prompt Contest #1] [Avatar] Characters Need Masters and Amateurs And Everybody In Between](https://www.reddit.com/r/CharacterRant/comments/nnb0u0/prompt_contest_1_avatar_characters_need_masters/) r/CharacterRant•6y ago    ### [[Prompt Contest #1] [Avatar] Characters Need Masters and Amateurs And Everybody In Between](https://www.reddit.com/r/CharacterRant/comments/nnb0u0/prompt_contest_1_avatar_characters_need_masters/)    111 upvotes ·14 comments
* * *
*   More of my favorite guy r/TwinkleTwinkleCollect•2mo ago    ### More of my favorite guy     46 upvotes ·6 comments
* * *

# More posts you may like
## View Post in
हिन्दी
See more  See fewer
العربية
Slovenčina
Hrvatski
Čeština
Bahasa Indonesia
Public
Anyone can view, post, and comment to this community
0 0
</excerpt>

## Search 5 — query: "Tipsy Tose Hall Week 1 Day 5 boss noise "HEAD2HEAD" "The World Ends with You""
### Rank 1 of 32 — 0.93 (passed on)
<excerpt title="how to find every Boss Noise, and get the secret ending">
It wouldn't be a TWEWY game without Secret Reports, and initially the**NEO: The World Ends With You Secret Reports**these seem like the most confusing to find yet. Luckily, this page is here to help you with the **secret report locations** and **finding every boss noise** to get you to the **NEO secret ending**.
Video 4
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
### Rank 2 of 32 — 0.76
<excerpt title="Day 5 - Poach the True Golden Pig - Neo: The World Ends with You Guide">
## Change Your Fate!
With that you'll finally have done enough to change your fate. Press Y and choose change your fate to go back to where you were ambushed - but know you'll be walking into a fight. Prepare now!
This time, the DRS scheme doesn't go according to plan, giving the Wicked Twisters a fighting chance.

## Boss Fight - Deep Rivers Society and True Gold Pig
You'll be up against the DRS leader, Fuya, along with a few Deap Rivers Societists and the True Gold Pig.
**Pin Recommendations:**
*   **Poison Affinity Pins -**The main boss, Fuya, is weak to Poison, so Poison pins will help take him down quickly. **Icky Beam**is a Poison-affinity Y/Square pin dropped by the Scorpion Noise Break Stinger on Normal Difficulty.  
*   **Pins that deal extra damage to aerial opponents -**The DRS often float in the air to perform telekenetic moves, leaving them vulnerable to attacks that deal additional damage to airborne opponents, for example, Crater's Kiss.  
*   **Otherwise, your strongest pins should be fine!**
**Strategy:**
*   The true golden boar doesn't do much but run around aimlessly - focus on Fuya of the DRS.  
*   Fuya will occasionally leave mines behind. They will glow and wiggle when they're about to explode - get away from them before that can happen.  
*   The DNS will occasionally float into the air to charge attacks that swirl in pink and blue. This is your chance - hit them with charged attacks to potentially knock them down. Otherwise, they'll pelt you with long-distance rapid attacks.  
*   Midway through the fight, an entire field of mines will appear. **To avoid them**,run away from them, and keep your distance until after they explode. Make sure not to try to attack opponents during this time - even long-range attacks will pull you in that direction, potentially pulling you into the range of the bombs.

## After the Fight - End of Day 5
You have a conversation with Swallow deepening the mystery, and after a few more conversations, ultimately earn:
*   3 FP  
*   Social Network Add: Fuya Kawahara  
*   Social Network Add: Reaper Ayano Kamachi  
*   Social Network Add: Reaper Tanzo Kubo
That is the end of the chapter Head2Head.
*   On to Day 6 - Win the Scramble Slam

## After the Fight - End of Day 5
### Was this guide helpful?


## After the Fight - End of Day 5
### In This Guide
</excerpt>
### Rank 3 of 32 — 0.37
<excerpt title="HEAD2HEAD (Week 1, Day 5) - The World Ends with You Wiki - Fandom">
**Spoiler warning**: Plot and/or character details follow.
_"We will not allow ourselves to drift away when the going gets tough. If we merely float along wherever the river of life takes us, then we deserve to be trounced by the torrents of the downstream waters! We have just as much right to be here as anyone else! And we will fight for that right using the powers given to us, and return to the headwaters of the UG!"_— Fuya Kawahara as the Deep Rivers Society ambushes the Wicked Twisters  
**HEAD2HEAD** is a day in _NEO: The World Ends with You_.

## Events[]
*   Rindo receives a Trailer of being attacked by Pigs and the Deep Rivers Society.  
*   Sho Minamimoto convinces the Wicked Twisters to sabotage the rival teams.  
*   The Wicked Twisters meet Motoi Anazawa, who teaches them how to imprint.  
*   The Wicked Twisters imprint on Ryoji so he can better sell his gilded pig toys.  
*   The Wicked Twisters are ambushed by the Deep Rivers Society and Piggo Doobles.  
*   Rindo Replays several times through the day to distract Deep Rivers Societists and to prevent Ryoji from selling his pig toys.   
    *   The Societists at ~10:00 Tipsy Tose Hall are distracted by Fret Reminding them about an art exhibit.  
    *   Rindo purposefully imprints Ryoji with a bad slogan at ~11:00 Center Street so the gilded pig toys don't sell.  
    *   The Wicked Twisters defeat the same group of Societists from Day 3 they fought at ~12:00 Spain Hill.  
    *   The Societists at ~13:00 TOWER RECORDS are distracted by a historical lecture from Buddy Rapids.  
    *   The Societists at ~14:00 Scramble Crossing are distracted by Rindo giving them the password and a false signal.  
    *   The Societists at ~15:00 Center Street are distracted by Miss Ammonia Banks arriving at TOWER RECORDS.

*   Rindo changes their fate so the Deep Rivers Society doesn't have enough reinforcements to ambush the Wicked Twisters and defeats the team and the true golden pig.  
*   Fuya surrenders and breaks down into tears, to the Wicked Twisters' confusion.  
*   Shoka Sakurane finds and confronts Minamimoto but he scares her off.

## Events[]
### Sidequests[]
*   **Good Noise Hunting:** Nagi Dives into the mind of Yusei Iseya and erases the Noise possessing him.  
*   **Fangirl in Crisis:** Rindo imprints some advice on Yuika Kaga about how to play the newest chapter of Elegant Strategy.  
*   **Don You Forget About Me:** Fret Reminds the first customers of SPICY CURRY DON about the food they ate, finding that they wanted to try all the curry. Ken Doi is inspired to add the Triple Triad Plate to the menu.
</excerpt>
### Rank 4 of 32 — 0.34
<excerpt title="HEAD2HEAD (Week 1, Day 5) - The World Ends with You Wiki - Fandom">
## Events[]
### Sidequests[]
*   **Good Noise Hunting:** Nagi Dives into the mind of Yusei Iseya and erases the Noise possessing him.  
*   **Fangirl in Crisis:** Rindo imprints some advice on Yuika Kaga about how to play the newest chapter of Elegant Strategy.  
*   **Don You Forget About Me:** Fret Reminds the first customers of SPICY CURRY DON about the food they ate, finding that they wanted to try all the curry. Ken Doi is inspired to add the Triple Triad Plate to the menu.

## Plot[]
The mission for the day is to locate and erase a Golden Pig Noise. The Wicked Twisters follow reports on the Pig's location through the city, fighting Gilded Pig Noise as they do, which resemble the Golden Pig Noise but are worth far less. They encounter several unrelated events along the way which they dismiss, and briefly help a salesman sell plush pigs on a street corner using Imprint. When the Golden Pig is reported at Spain Hill, the Twisters are ambushed by the entire Deep Rivers Society and a huge number of Gilded Pigs in an unwinnable battle.
Rindo uses his Replay ability to relive the day, taking more interest in the other events in the city which provide opportunities to distract the members of the Deep Rivers Society with artistic exhibitions and lectures. He also realises that the flood of Gilded Pig Noise was caused by widespread disappointment with the plush pigs, and so sabotages the salesman's efforts instead. When they arrive at Spain Hill this time, only a few members of the Deep Rivers Society have turned up, and the Golden Pig is clearly apparent. The Twisters are able to erase the Golden Pig and defeat the Deep Rivers Society, and their leader surrenders, moving the Twisters into second place and the Deep River Society into last place. The leader breaks down in anguished tears after surrendering, to the confusion of Rindo, Fret and Nagi.

## Plot[]
### Sidequests[]
#### Good Noise Hunting[]


## Plot[]
### Sidequests[]
#### Fangirl in Crisis[]


## Plot[]
### Sidequests[]
#### Don You Forget About Me[]


## Walkthrough[]


## Noise[]


## Rewards[]


## Secret Reports[]


## Trivia[]
*   When distracting the Societists at the Scramble Crossing, one of the incorrect options for the password is "simple and clean", referencing the Hikaru Utada song of the same name that was the theme song for the 2002 game _Kingdom Hearts_.
| Days in _NEO: The World Ends with You_ |  
| --- |  
| **Prologue** | Prologue |  
| **Week 1** | Day 1 • Day 2 • Day 3 • Day 4 • **Day 5** • Day 6 • Day 7 |  
| **Week 2** | Day 1 • Day 2 • Day 3 • Day 4 • Day 5 • Day 6 • Day 7 |  
| **Week 3** | Day 1 • Day 2 • Day 3 • Day 4 • Day 5 • Day 6 • Day 7 • 7 Part 2 • 7 Part 3 |  
| **Extra** | _Another Day_ |
</excerpt>
### Rank 5 of 32 — 0.26
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

## Search 6 — query: "Tipsy Tose Hall boss Noise name HEAD2HEAD tip TU"
### Rank 1 of 40 — 0.91 (passed on)
<excerpt title="how to find every Boss Noise, and get the secret ending">
It wouldn't be a TWEWY game without Secret Reports, and initially the**NEO: The World Ends With You Secret Reports**these seem like the most confusing to find yet. Luckily, this page is here to help you with the **secret report locations** and **finding every boss noise** to get you to the **NEO secret ending**.
Video 4
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
### Rank 2 of 40 — 0.85
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
### Rank 3 of 40 — 0.85
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
### Rank 4 of 40 — 0.70
<excerpt title="Week 1, Day 5: Head to Head Chapter Guide and Walkthrough | NEO">
Video 5  
Video Muted
This is a walkthrough for Head to Head, Week 1, Day 5 of NEO: The World Ends with You. Learn more about the objectives of this chapter, puzzle solutions, tips for completion, as well as boss fight strategies!
| Previous Day | Current Day | Next Day |  
| --- | --- | --- |  
| Real Eyes Realize Real Lies | **Head to Head** | Into the Crossing |
| Week | 1 |  
| --- |  
| Day | 5 |  
| Boss | Fuya |  
| Description |  
| Struggling to earn the points they need, the Wicked Twisters follow Minamimoto's advice to steal points from rival teams. Rindo sets his sights on the Deep Rivers Society, but their leader, Fuya, gets the better of the gang, and their fortunes seem worse than ever. |
**Week 1 - Day 5**
| Event | Reward |  
| --- | --- |  
| After completing the Reaper's special mission in Tower Records Shibuya: Help the man decide where to buy the CD. | Tigres Assemble! |  
| After defeating the Noise for the Reaper guarding the entrance to Center Street district. | Righteous Rabbit |
|  | Objectives |  
| --- | --- |  
| 1 | Head towards Center Street. From your position, move towards the path to Center Street and this will trigger a cutscene. |  
| 2 |  * * * Scan and erase the golden pig. Activate your scanner and get near the golden pig symbol to initiate combat. Defeat the golden pig to move forward with the story. |
| 3 | Enter Center Street. Follow the waypoint to enter Center Street district. Along the way, you'll enter a conversation with the Deep Rivers Societist. |  
| --- |

| 4 |  * * * Interact with Ryoji. Upon entering Center Street, interact with Ryoji. You will also meet Motoi during this interaction. |  
| --- |  
| 5 | Scan and imprint Ryoji's thoughts. Activate your scanner and scan Ryoji's thoughts. You will then be prompted to imprint his thoughts. To do this, you need to collect keywords from other people's thoughts. Keep your scanner activated and look for NPCs with red thoughts bubbles above them. |  
| 6 |  * * * Put together words for Ryoji. After collecting the necessary keywords, return to Ryoji and combine the words high-quality and meet. This will imprint an idea on Ryoji's head. |  
| 7 | Continue looking for keywords for Ryoji. Activate your scanner once again and look for red thought bubbles for keywords. Some of them would require you to engage in battle this time by diving into their mind. |  
| 8 | Imprint Ryoji's thoughts again. Return to Ryoji and combine the phrase peace of mind and the word protect. |
| 9 |  * * * Enter Spain Hill. After gathering intel from Ryoji, follow the waypoint to enter Spain Hill district. |  
| --- |  
| 10 |  * * * Move upwards into the district. Use the stairs to get to the main street. Along the way, you'll encounter members from the Deep Rivers Societist and a man in a red shirt. |  
| 11 |  * * * Scan the area for the golden pig. Once you've reached main street, use your scanner and take the stairs outside the Parco building. In the balcony, get near the golden pig symbol to erase it. |
| 12 |  * * * Enter TOWER RECORDS. After erasing the golden pig, follow the waypoint to enter TOWER RECORDS district. Upon entering the district, talk to Deep Rivers Societists in the center of the crossing. |  
| --- |
</excerpt>
### Rank 5 of 40 — 0.58
<excerpt title="Week 1, Day 5: Head to Head Chapter Guide and Walkthrough | NEO">
| 13 | Talk to the Reaper. After talking with the Deep Rivers Societists, follow the waypoint and interact with the Reaper guarding the path to Scramble Crossing. |  
| --- |  
| 14 |  * * * Imprint the man's thoughts. The Reaper will be asking you to imprint the thoughts of the man in a suit near you. Scan for keywords around the district and then combine the words internet and buy. The Reaper will grant you passage after completing his special mission. |
| 15 |  * * * Scan and erase the golden pig. Once you're in Scramble Crossing, activate your scanner and erase the golden pig in the area. |  
| --- |
| 16 | Talk to the Reaper. After erasing the golden pig, talk to the Reaper guarding the path to Center Street. He will then ask you to erase the Noise he'll throw out at you. Defeat the Noise to gain entry to the district. |  
| --- |  
| 17 |  * * * Head to Shepherd House. Once you're in Center Street, go to Center Street and talk to the Deep Rivers Societists again. After the cutscene, you'll be engaging in combat to erase the golden pig. |
| 18 | Enter Spain Hill. After erasing the golden pig, follow the waypoint to return to Spain Hill district. |  
| --- |  
| 19 | Confront the leader of the Deep Rivers Society. Head upwards the main street and confront the leader of the Deep Rivers Society. This will then trigger a lengthy cutscene where you will be prompted to travel back in time once again at the end of it. |

| 20 |  * * * Talk to the Deep Rivers Societists again. Now in the past, head towards the entrance to Center Street and talk to the Deep Rivers Societists again. |  
| --- |  
| 21 | Travel back to Scramble Crossing. Use Rindo's powers to travel back in time to Scramble Crossing. Once there, check the shop next to the path to Center Street. |  
| 22 |  * * * Return to Tipsy Tose Hall. Travel back to Tipsy Tose Hall again using Rindo's powers and interact with the Deep Rivers Societists once again. Use Fret's powers this time to remind them. |  
| 23 | Travel back to Center Street. After reminding the Deep Rivers Societists, use Rindo's powers to travel back to Center Street. Dive inside the thoughts of the man in the suit and erase the Noise. |  
| 24 | Travel back to to the Deep Rivers Societist. After erasing the Noise, talk to the Deep Rivers Societists again. |  
| 25 |  * * * Travel back to TOWER RECORDS SHIBUYA. Use Rindo's powers to travel back to TOWER RECORDS SHIBUYA. Interact with the man in a white suit and imprint his thoughts. Activate your scanner to look around for keywords. Return to him and combine the words appropriate and time to proceed with the story. |  
| 26 | Return to Center Street again. Return to Center Street again and talk to the Deep Rivers Societist in front of the Shepherd House again. After the cutscene, return to Ryoji and imprint his thoughts again using keywords from other people. Combine the words soul and cry to imprint his thoughts. |  
| 27 | Return to Scramble Crossing again. After dealing with Ryoji, use Rindo's powers to return to Scramble Crossing again and talk the Deep Rivers Societists. You will then have to answer their secret riddle. Answer in order: The river, flows, swift and clear. |  
| 28 | Return to Tipsy Tose Hall. Use Rindo's powers once again and return to Tipsy Tose Hall. Talk to the man in a brown suit. |
</excerpt>

## Search 7 — query: "HEAD2HEAD Tipsy Tose Hall boss noise name""
### Rank 1 of 42 — 0.94 (passed on)
<excerpt title="how to find every Boss Noise, and get the secret ending">
It wouldn't be a TWEWY game without Secret Reports, and initially the**NEO: The World Ends With You Secret Reports**these seem like the most confusing to find yet. Luckily, this page is here to help you with the **secret report locations** and **finding every boss noise** to get you to the **NEO secret ending**.
Video 4
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
### Rank 2 of 42 — 0.87
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
### Rank 3 of 42 — 0.83
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
### Rank 4 of 42 — 0.80
<excerpt title="Week 1, Day 5: Head to Head Chapter Guide and Walkthrough | NEO">
Video 5  
Video Muted
This is a walkthrough for Head to Head, Week 1, Day 5 of NEO: The World Ends with You. Learn more about the objectives of this chapter, puzzle solutions, tips for completion, as well as boss fight strategies!
| Previous Day | Current Day | Next Day |  
| --- | --- | --- |  
| Real Eyes Realize Real Lies | **Head to Head** | Into the Crossing |
| Week | 1 |  
| --- |  
| Day | 5 |  
| Boss | Fuya |  
| Description |  
| Struggling to earn the points they need, the Wicked Twisters follow Minamimoto's advice to steal points from rival teams. Rindo sets his sights on the Deep Rivers Society, but their leader, Fuya, gets the better of the gang, and their fortunes seem worse than ever. |
**Week 1 - Day 5**
| Event | Reward |  
| --- | --- |  
| After completing the Reaper's special mission in Tower Records Shibuya: Help the man decide where to buy the CD. | Tigres Assemble! |  
| After defeating the Noise for the Reaper guarding the entrance to Center Street district. | Righteous Rabbit |
|  | Objectives |  
| --- | --- |  
| 1 | Head towards Center Street. From your position, move towards the path to Center Street and this will trigger a cutscene. |  
| 2 |  * * * Scan and erase the golden pig. Activate your scanner and get near the golden pig symbol to initiate combat. Defeat the golden pig to move forward with the story. |
| 3 | Enter Center Street. Follow the waypoint to enter Center Street district. Along the way, you'll enter a conversation with the Deep Rivers Societist. |  
| --- |

| 4 |  * * * Interact with Ryoji. Upon entering Center Street, interact with Ryoji. You will also meet Motoi during this interaction. |  
| --- |  
| 5 | Scan and imprint Ryoji's thoughts. Activate your scanner and scan Ryoji's thoughts. You will then be prompted to imprint his thoughts. To do this, you need to collect keywords from other people's thoughts. Keep your scanner activated and look for NPCs with red thoughts bubbles above them. |  
| 6 |  * * * Put together words for Ryoji. After collecting the necessary keywords, return to Ryoji and combine the words high-quality and meet. This will imprint an idea on Ryoji's head. |  
| 7 | Continue looking for keywords for Ryoji. Activate your scanner once again and look for red thought bubbles for keywords. Some of them would require you to engage in battle this time by diving into their mind. |  
| 8 | Imprint Ryoji's thoughts again. Return to Ryoji and combine the phrase peace of mind and the word protect. |
| 9 |  * * * Enter Spain Hill. After gathering intel from Ryoji, follow the waypoint to enter Spain Hill district. |  
| --- |  
| 10 |  * * * Move upwards into the district. Use the stairs to get to the main street. Along the way, you'll encounter members from the Deep Rivers Societist and a man in a red shirt. |  
| 11 |  * * * Scan the area for the golden pig. Once you've reached main street, use your scanner and take the stairs outside the Parco building. In the balcony, get near the golden pig symbol to erase it. |
| 12 |  * * * Enter TOWER RECORDS. After erasing the golden pig, follow the waypoint to enter TOWER RECORDS district. Upon entering the district, talk to Deep Rivers Societists in the center of the crossing. |  
| --- |
</excerpt>
### Rank 5 of 42 — 0.78
<excerpt title="How to Get All Secret Reports | Blue Noise (Boss Noise) Locations | NEO">
| Book | Overview |  
| --- | --- |  
| **"Secret Report No. 1"** (No. 084) | Enlarge **How to Obtain:** Scan near Hachiko in Scramble Crossing. Look for a blue Scorpion Noise. * * * Location (Chapter): Scramble Crossing (Week 1, Day 1) |  
|  |  
| **"Secret Report No. 2"** (No. 085) | Enlarge **How to Obtain:** Go up the stairs of the 104 Building and go left. Scan for the Gorilla Noise. * * * Location (Chapter): 104 Building (Week 1, Day 2) |  
|  |  
| **"Secret Report No. 3"** (No. 086) | Enlarge **How to Obtain:** Achieve 70% completion of Social network. * * * Location (Chapter): - |  
|  |  
| **"Secret Report No. 4"** (No. 087) | Enlarge **How to Obtain:** Achieve 80% completion of Social Network. * * * Location (Chapter): - |  
|  |  
| **"Secret Report No. 5"** (No. 088) | Enlarge **How to Obtain:** Scan near Tokyu Hands in Tipsy Tose Hall. Look for a blue Deep Rivers Society Noise. * * * Location (Chapter): Tipsy Tose Hall (Week 1, Day 5) |  
|  |  
| **"Secret Report No. 6"** (No. 089) | Enlarge **How to Obtain:** Achieve 90% completion of Social Network. * * * Location (Chapter): - |  
|  |  
| **"Secret Report No. 7"** (No. 090) | Enlarge **How to Obtain:** Go to TOWER RECORDS in Tower Records Shibuya. Scan and look for a blue Cervus Cantus Noise. * * * Location (Chapter): TOWER RECORDS SHIBUYA (Week 1, Day 7) |  
|  |
</excerpt>

## Search 8 — query: ""HEAD2HEAD" "Boss Noise" "The World Ends with You""
### Rank 1 of 10 — 0.87 (passed on)
<excerpt title="how to find every Boss Noise, and get the secret ending">
It wouldn't be a TWEWY game without Secret Reports, and initially the**NEO: The World Ends With You Secret Reports**these seem like the most confusing to find yet. Luckily, this page is here to help you with the **secret report locations** and **finding every boss noise** to get you to the **NEO secret ending**.
Video 4
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
### Rank 2 of 10 — 0.56
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
### Rank 3 of 10 — 0.24
<excerpt title="Table of Contents - The World Ends with You Wiki - Fandom">
## NEO: The World Ends with You Links[]
### Noise[]
_(Main Article: Noise)_
*   Noisepedia  
*   Noise Families

## NEO: The World Ends with You Links[]
### Chapters[]
_(Main Article: Days)_
*   Prologue  
*   Week 1 | Day 1: _theREAPERS'game_  
*   Week 1 | Day 2: _GeT✖TWISTeD_  
*   Week 1 | Day 3: _DeeP DivE_  
*   Week 1 | Day 4: _REAL(eyes/ize/lies)_  
*   Week 1 | Day 5: _HEAD2HEAD_  
*   Week 1 | Day 6: _in2 the ✖ing_  
*   Week 1 | Final Day: _GamE thEorY_  
*   Week 2 | Day 1: _New Game_  
*   Week 2 | Day 2: _LiVing LeGend_  
*   Week 2 | Day 3: _Sound♪Surfer_  
*   Week 2 | Day 4: _🡒urbaNlegendZ_  
*   Week 2 | Day 5: _noisrevni_  
*   Week 2 | Day 6: _desireDestination_  
*   Week 2 | Day 7: _CHECKMATE!_  
*   Week 3 | Day 1: _SuDDeN DeaTH_  
*   Week 3 | Day 2: _Dearly❤beloveD_  
*   Week 3 | Day 3: _re:START_  
*   Week 3 | Day 4: _come🡒🡐back_  
*   Week 3 | Day 5: _VisioN_  
*   Week 3 | Day 6: _🡐stabbed_  
*   Week 3 | Final Day: _S • B • Y_  
*   Week 3 | Final Day': _SHI • BU • YA_  
*   Week 3 | Final Day'': _SHIBUYA_  
*   Another Day: Party in the 'Buya

## NEO: The World Ends with You Links[]
### Miscellaneous[]
NEO: The World Ends with You Original Soundtrack
</excerpt>
### Rank 4 of 10 — 0.14
<excerpt title="Table of Contents - The World Ends with You Wiki - Fandom">
## The World Ends with You Links[]
### Combat[]
*   Stride Battle Cross System  
*   Puck  
*   Cross Combo  
*   Dash  
*   Dodge  
*   Guard  
*   Fusion  
*   SOS  
*   Attack  
*   Defense  
*   HP  
*   Bravery  
*   Drop Rate  
*   Level  
*   Negative statuses  
*   Resistance  
*   Battle Rankings  
*   Death  
*   Chain

## The World Ends with You Links[]
### Items[]
*   Shop List  
*   Thread list (Sortable)  
*   Food list (Sortable)  
*   Swag list (Sortable)  
*   Secret Reports

## The World Ends with You Links[]
### Items[]
#### Pins[]
*   Pin List  
*   Sortable Pin List  
*   Pin Damage  
*   Pin Damage  
*   Where to get  
*   Farming Guide  
*   Evolution Guide  
*   Evolution Table  
*   The Animation

## The World Ends with You Links[]
### Items[]
#### Brands[]
*   Mus Rattus  
*   D+B  
*   Tigre Punks  
*   Lapin Angelique  
*   Dragon Couture  
*   Hip Snake  
*   Pegaso  
*   Sheep Heavenly  
*   Jupiter of the Monkey  
*   Pavo Real  
*   Natural Puppy  
*   Wild Boar  
*   Gatito  
*   Mithril Scale  
*   Maiden Innocence

## The World Ends with You Links[]
### Noise[]
_(Main Article: Noise)_
*   Noise Report  
*   Noise List by Day and Location  
*   Noise Families  
*   Noise Abilities

## The World Ends with You Links[]
### Noise[]
#### Types[]
*   Chump Noise - Red  
*   Negative Noise - Yellow  
*   Pig Noise - Green  
*   Taboo Noise - Black  
*   Boss Noise - Blue  
*   Dissonance Noise - Purple

## The World Ends with You Links[]
### Chapters[]
_(Main Article: Days)_
*   Shiki, Day 1: _Reapers' Game_  
*   Shiki, Day 2: _Don't Kill Me_  
*   Shiki, Day 3: _Who 2 Trust_  
*   Shiki, Day 4: _Erased_  
*   Shiki, Day 5: _Empty Urban Legends_  
*   Shiki, Day 6: _Superiority/Inferiority_  
*   Shiki, Day 7: _Wakeless Dream_  
*   Joshua, Day 1: _Rulez_  
*   Joshua, Day 2: _Reapers_  
*   Joshua, Day 3: _Roaming The Streets_  
*   Joshua, Day 4: _Pinned_  
*   Joshua, Day 5: _Turf_  
*   Joshua, Day 6: _Beast on the Prowl_  
*   Joshua, Day 7: _Clash of Desires_  
*   Beat, Day 1: _Sensible, Senseless_  
*   Beat, Day 2: _Style_  
*   Beat, Day 3: _The Composer_  
*   Beat, Day 4: _Indelible Guilt_  
*   Beat, Day 5: _Vanishing Point_  
*   Beat, Day 6: _Stride_  
*   Beat, Day 7: _Game_  
*   Another Day: _This Day Ends With You!_  
*   A New Day: _Expert Mode, Dissonance, No Beginning and No End_
</excerpt>
### Rank 5 of 10 — 0.13
<excerpt title="how to find every Boss Noise, and get the secret ending">
## How to unlock Boss Noises & get Secret Reports in NEO: TWEWY
### **Secret Report 21:**
Defeat the boss noise found on Takeshita Street during Week 3, Final Day- S • B• Y. You can find the location below.

## How to unlock Boss Noises & get Secret Reports in NEO: TWEWY
### **Secret Report 22:**
Defeat the boss noise found on Takeshita Street during Week 3, Final Day' - SHI • BU • YA. You can find the location below.

## How to unlock Boss Noises & get Secret Reports in NEO: TWEWY
### **Secret Report 23:**
Defeat the boss noise found at TOKYU PLAZA during Week 3, Final Day'' - SHIBUYA. You'll have to refight the final boss, so plan accordingly. You can find the location below.

## How to unlock Boss Noises & get Secret Reports in NEO: TWEWY
### **Secret Report 24:**
The last Secret Report you'll receive, and thankfully you'll get it automatically once every other report is unlocked! Congratulations, enjoy the secret ending!

## NEO: The World Ends With You Secret Endings
There are actually two 'secret endings in NEO: The World Ends With You.
1.) After getting all Secret Reports, simply do the Final Day again (yes you have to speed through all the Replay setup). After the credits, you'll get a scene between two interesting characters.
2.) In the Another Day epilogue side-story chapter, to get the standard epilogue ending, you simply need to defeat three revisited bosses, followed by one final encounter by talking to Hishima at the Hachiko Statue. You'll get a quick ending with Rindo and company attending a concert.
However, a secret ending is also available here if you complete all the bonus objectives during the chapter in addition to the required bosses.
*   Find and defeat all 5 Pig Noise in the Another Day chapter.  
*   Find Rhyme at Dogenzaka and complete a 10-reduction Dive challenge.  
*   Find Coco at Takeshita Street to do a Boss Rush Time Trial.  
*   Find Minimimoto at Expressway Underpass to fight the game's secret boss.
Do these things (all in one run), and you'll get an additional ending after the credits roll. This is a quick one, perhaps teasing a character motivation in a potential eventual follow-up.
</excerpt>

For each search, read the top excerpt and the ones ranked below it, and judge whether the order is right for answering the question. An excerpt holding the answer, or a fact that leads to it, should outrank one that only repeats the query's words or covers the topic without a checkable fact. If none of the excerpts holds anything useful, that is the search's fault, not this instruction's. Find the ranking error that cost the most and write a new instruction that fixes it. Replace or compress existing text where you can; avoid making it much longer. Do not write the "Original question" or "Search query" lines; they are appended for you. Do not copy any fact, name, site or topic from these examples.

Provide the new instruction within ``` blocks.
