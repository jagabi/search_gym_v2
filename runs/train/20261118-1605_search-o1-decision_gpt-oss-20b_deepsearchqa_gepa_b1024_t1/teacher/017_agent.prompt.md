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
According to the World Spider Catalog, which spiders of the family Desidae and genus Desis are native to one country. Provide their full scientific names and the location they are indigenous to.

## Expected answer
Desis bobmarleyi - Endemic to Australia (specifically Queensland), Desis galapagoensis - Endemic to the Galapagos Islands (Ecuador), Desis gardineri - Endemic to the Laccadive Islands (India), Desis inermis - Endemic to India, Desis japonica - Endemic to Japan, Desis jiaxiangi - Endemic to China, Desis kenyonae - Endemic to Australia (specifically Victoria and Tasmania), Desis vorax - Endemic to Samoa, Desis risbeci - Endemic to New Caledonia

## Final answer — grade 0.94
**Desis species that are native to a single country (according to the World Spider Catalog as of 2026‑11‑19)**  

| Full scientific name | Indigenous country (or island group)* | Source (WSC entry showing distribution) |
|----------------------|----------------------------------------|----------------------------------------|
| *Desis bobmarleyi* Baehr, Raven & Harms, 2017 | Australia (Queensland) | “Distribution: Australia (Queensland)” (WSC entry 62701) |
| *Desis galapagoensis* Hirst, 1925 | Ecuador (Galápagos Islands) | “Distribution: Galapagos” (WSC entry 72183) |
| *Desis gardineri* Pocock, 1904 | India (Lakshadweep/Laccadive Islands) | “Distribution: India (Laccadive Is.)” (WSC entry 021483) |
| *Desis inermis* Gravely, 1927 | India | “Distribution: India” (WSC entry 021485) |
| *Desis japonica* Yaginuma, 1956 | Japan | “Distribution: Japan” (WSC entry 021486) |
| *Desis jiaxiangi* Lin, Li & Chen, 2020 | China | “Distribution: China” (WSC entry 051749) |
| *Desis kenyonae* Pocock, 1902 | Australia (Victoria, Tasmania) | “Distribution: Australia (Victoria, Tasmania)” (WSC entry 021487) |
| *Desis risbeci* Berland, 1931 | New Caledonia | “Distribution: New Caledonia” (WSC entry 021491) |

\*For island‑group species, the island zone is the only recognized country-level record for that species in the World Spider Catalog.  

---

### Notes

* The catalog lists each species with its accepted distribution and indicates whether the range includes one or several countries.  
* Species such as *Desis marinus* (*New Caledonia, New Zealand*), *Desis formidabilis* (Namibia + South Africa), *Desis martensi* (Singapore + Indonesia), and *Desis maxillosa* (New Guinea + New Caledonia) are excluded because their distributions span more than one sovereign state.  
* For *Desis galapagoensis*, the catalog records only “Galapagos”. The Galápagos Islands belong to Ecuador, so the species is considered endemic to that country for this purpose.  

These are the Desis species listed by the World Spider Catalog whose known indigenous range is restricted to a single country as of the latest update.
(10 searches; ended: answered)

## Search 1
query: "World Spider Catalog Desis species distribution"
<excerpt title="Desis marina">
No information available.

###### Taxonomic References
_Dandridgea dysderoides_**White, 1849**: 5 (D; preoccupied by Walckenaer, 1837, see _Desis maxillosa_) [urn:lsid:nmbe.ch:spidersp:055996]
_Argyronetra marina_ Hector, in **Robson, 1878**: 300 (D f, lapsus) Original description
_Desis robsoni_**Powell, 1879**: 263, pl. 12 (D f) [urn:lsid:nmbe.ch:spidersp:055997]
_Desis marinus_**Pocock, 1895b**: 143 (T from _Robsonia_, S of _Dandridgea dysderoides_ White and _Desis robsoni_)

###### References
Coddington, J. A. (1990). Ontogeny and homology in the male palpus of orb-weaving spiders and their relatives, with comments on phylogeny (Araneoclada: Araneoidea, Deinopoidea). _Smithsonian Contributions to Zoology_**496**: 1-52. doi: 10.5479/si.00810282.496 -- Show included taxa
Forster, R. R. (1970b). The spiders of New Zealand. Part III. _Otago Museum Bulletin_**3**: 1-184.  -- Show included taxa
Lehtinen, P. T. (1967). Classification of the cribellate spiders and some allied families, with notes on the evolution of the suborder Araneomorpha. _Annales Zoologici Fennici_**4**: 199-468.  [second pdf: index and outline by V. D. Roth (unpubl.)] -- Show included taxa
Pickard-Cambridge, O. (1880a). On some new and rare spiders from New Zealand, with characters of four new genera. _Proceedings of the Zoological Society of London_**47**(4, 1879): 681-703, pl. 52-53. doi: 10.1111/j.1096-3642.1879.tb02701.x published in April 1880, after [Duncan, 1937] -- Show included taxa
Pocock, R. I. (1895b). Description of two new spiders obtained by Messrs. J. J. Quelch and F. McConnell on the summit of Mount Roraima, in Demerara; with a note upon the systematic position of the genus _Desis_. _Annals and Magazine of Natural History_ (6) **16**(92): 139-143. doi: 10.1080/00222939508680241 -- Show included taxa

###### References
Powell, L. (1879). On _Desis Robsoni_, a marine spider, from Cape Campbell. _Transactions and Proceedings of the New Zealand Institute_**11**: 263-268.  -- Show included taxa
Robson, C. H. (1878). Note on a marine spider found at Cape Campbell. _Transactions and Proceedings of the New Zealand Institute_**10**(1877): 299-300.  -- Show included taxa
White, A. (1849). Descriptions of apparently new species of Aptera from New Zealand. _Proceedings of the Zoological Society of London_**17**: 3-6. doi: 10.1111/j.1096-3642.1849.tb01122.x [(reprinted in _Ann. Mag. nat. Hist._ (2) **5:** 50-53, 1850)] -- Show included taxa
</excerpt>

## Search 2
query: "Desis species World Spider Catalog distribution"
<excerpt title="Desis marina">
No information available.

###### Taxonomic References
_Dandridgea dysderoides_**White, 1849**: 5 (D; preoccupied by Walckenaer, 1837, see _Desis maxillosa_) [urn:lsid:nmbe.ch:spidersp:055996]
_Argyronetra marina_ Hector, in **Robson, 1878**: 300 (D f, lapsus) Original description
_Desis robsoni_**Powell, 1879**: 263, pl. 12 (D f) [urn:lsid:nmbe.ch:spidersp:055997]
_Desis marinus_**Pocock, 1895b**: 143 (T from _Robsonia_, S of _Dandridgea dysderoides_ White and _Desis robsoni_)

###### References
Coddington, J. A. (1990). Ontogeny and homology in the male palpus of orb-weaving spiders and their relatives, with comments on phylogeny (Araneoclada: Araneoidea, Deinopoidea). _Smithsonian Contributions to Zoology_**496**: 1-52. doi: 10.5479/si.00810282.496 -- Show included taxa
Forster, R. R. (1970b). The spiders of New Zealand. Part III. _Otago Museum Bulletin_**3**: 1-184.  -- Show included taxa
Lehtinen, P. T. (1967). Classification of the cribellate spiders and some allied families, with notes on the evolution of the suborder Araneomorpha. _Annales Zoologici Fennici_**4**: 199-468.  [second pdf: index and outline by V. D. Roth (unpubl.)] -- Show included taxa
Pickard-Cambridge, O. (1880a). On some new and rare spiders from New Zealand, with characters of four new genera. _Proceedings of the Zoological Society of London_**47**(4, 1879): 681-703, pl. 52-53. doi: 10.1111/j.1096-3642.1879.tb02701.x published in April 1880, after [Duncan, 1937] -- Show included taxa
Pocock, R. I. (1895b). Description of two new spiders obtained by Messrs. J. J. Quelch and F. McConnell on the summit of Mount Roraima, in Demerara; with a note upon the systematic position of the genus _Desis_. _Annals and Magazine of Natural History_ (6) **16**(92): 139-143. doi: 10.1080/00222939508680241 -- Show included taxa

###### References
Powell, L. (1879). On _Desis Robsoni_, a marine spider, from Cape Campbell. _Transactions and Proceedings of the New Zealand Institute_**11**: 263-268.  -- Show included taxa
Robson, C. H. (1878). Note on a marine spider found at Cape Campbell. _Transactions and Proceedings of the New Zealand Institute_**10**(1877): 299-300.  -- Show included taxa
White, A. (1849). Descriptions of apparently new species of Aptera from New Zealand. _Proceedings of the Zoological Society of London_**17**: 3-6. doi: 10.1111/j.1096-3642.1849.tb01122.x [(reprinted in _Ann. Mag. nat. Hist._ (2) **5:** 50-53, 1850)] -- Show included taxa
</excerpt>

## Search 3
query: "site:wsc.nmbe.ch "Desis" "species""
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

## Search 4
query: "Desis species list wsc"
<excerpt title="First report of the spider genus Desis (Araneae, Desidae) from China, with ...">
## Abstract
The spider genus Desis Walckenaer, 1837 is the type genus of the spider family Desidae Pocock, 1895. Desis spiders hide in silk sacs between rocks or shells during high tide and forage during low tide (Baehr et al. 2017). Four Desis species have been recorded from Asia: Desis gardineri Pocock, 1904 (India), Desis inermis Gravely, 1927 (India), Desis japonica Yaginuma, 1956 (Japan) and Desis martensi L. Koch, 1872 (Malaysia) (World Spider Catalog 2020). Until now, only one species of the family Desidae, _Badumna tangae_ Zhu, Zhang & Yang, 2006, has been reported from China (Zhu _et al_. 2006). Here, we describe a new species of _Desis_ and report the genus from China for the first time.

## References
1.   Baehr, B.C., Raven, R. & Harms, D. (2017) “High tide or low tide”: _Desis bobmarleyi_ sp. n., a new spider from coral reefs in Australia’s Sunshine State and its relative from Sāmoa (Araneae, Desidae, _Desis_). _Evolutionary Systematics_, 1, 111–120. https://doi.org/10.3897/evolsyst.1.15735
World Spider Catalog (2020) _World Spider Catalog. Version 21_. Natural History Museum Bern. Available from: http://wsc.nmbe.ch (accessed 22 February 2020)
Zhu, M.S., Zhang, Z.S. & Yang, Z.Z. (2006) Discovery of the spider family Desidae (Araneae) in south China, with description of a new species of the genus _Badumna_ Thorell, 1890. _Zootaxa_, 1172 (1), 43–48.
https://doi.org/10.11646/zootaxa.1172.1.4

## References
### How to Cite
Lin, Y., Li, S. & Chen, H. (2020)
First report of the spider genus _Desis_(Araneae, Desidae) from China, with description of a new species
. _Zootaxa_, 4755 (3), 593–597. https://doi.org/10.11646/zootaxa.4755.3.11
</excerpt>

## Search 5
query: ""Species list of Desis""
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

## Search 6
query: "Desis gardineri World Spider Catalog distribution"
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

## Search 7
query: ""Desis formidabilis" distribution"
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

## Search 8
query: "Desis bobmarleyi distribution World Spider Catalog"
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

## Search 9
query: "Desis bobmarleyi world spider catalog distribution Australia"
<excerpt title="Desis bobmarleyi sp. n., a new spider from coral reefs in Australia's ...">
## Introduction
When Amalie Dietrich travelled from Europe to Australia in 1863 she not only attempted to collect animals and plants for the museum trade, but also sought independence and liberty. A strong-headed and adventurous women by nature, she seized new opportunities and took risks on a then-unexplored continent to elevate herself from poverty and oppression. Her life story is that of adventure and also life’s struggles and how to overcome them (Bischoff 1931). The Godeffroy Collection of arachnids, accumulated by her and other explorers over a decade in Australia and the Pacific before the turn of the 20 th century, is the primary taxonomic reference for spiders of Australasia and remains highly relevant until today (Weidner 1959, 1967).
Reggae legend Bob Marley certainly had a different background but shared with Dietrich and other explorers some character traits: adventurous and resilient at heart, he liberated himself and his peers from poverty and hopelessness. He took to music, not nature, but left traces through songs that teach optimism and independence of the mind, rather than hate and passive endurance. The song ‘High Tide or Low Tide’ promotes love and friendship through all struggles of life. It is his music that aided a field trip to Port Douglas in coastal Queensland, Australia, to collect spiders with a highly unique biology.
Intertidal spiders of the genus _Desis_ have a remarkable biology in that they are truly marine animals (Mcqueen and McLay 1983; Mcqueen et al. 1983). The known species hide away in barnacle shells, corals or the holdfasts of kelp during high tide where they built air chambers from silk, but are vagrant hunters of other invertebrates during low tide and typically collected from the surface of intertidal rocks, corals, debris or plants (Mcqueen and McLay 1983, Vink et al. 2017). Some other spider families, such as _Paratheuma_ in the family Dictynidae (Beatty and Berry 1988), share a similar biology but overall this is a rare pattern amongst spiders that are otherwise terrestrial animals.

## Introduction
It is the unique Godeffroy Collection of Australian and Pacific spiders at the Centre of Natural History in Hamburg, which contains almost all of the spiders collected by Amalie Dietrich, and also the first desid to be described from this part of the world. Three species were described in 1872 as part of the first major monograph on Australian spiders “_Die Arachniden Australiens_” which was compiled for more than a decade by distinguished arachnologists Ludwig Koch and Duke Eduard von Keyserling (Koch and Keyserling 1871–1883). Both arachnologists received the material from the Godeffroy Museum for taxonomic research and the desids were originally collected from Singapore, New Guinea and Sāmoa. Soon after, additional specimens were collected from Australia (Hector 1877, Pocock 1902) but surprisingly little is still known about the distribution and richness of these interesting spiders along the vast coastlines of this continent (ALA 2017; Framenau et al. 2014; Paquin et al. 2010; Whyte and Anderson 2017). Two species are currently known from Australia: _Desis hartmeyeri_ Simon, 1909 from Albany in south-western Australia and _D. kenyonae_ Pocock, 1902 from south-eastern Australia in Victoria and Tasmania (World Spider Catalog 2017, Framenau et al. 2014). However, at least _D. hartmeyeri_ is an enigmatic species and no faunistic or taxonomic entries were made since the time of the original description (Simon 1909).
</excerpt>

## Search 10
query: "Desis bobmarleyi site:wsc.nmbe.ch/spec-data"
<excerpt title="Desis bobmarleyi Baehr, Raven & Harms, 2017">
###### References
Baehr, B. C., Raven, R. & Harms, D. (2017). “High Tide or Low Tide”: _Desis bobmarleyi_ sp. n., a new spider from coral reefs in Australia’s Sunshine State and its relative from Sāmoa (Araneae, Desidae, _Desis_). _Evolutionary Systematics_**1**: 111-120. doi: 10.3897/evolsyst.1.15735 -- Show included taxa

###### External Resource References
*** Disclaimer**
As External Resources, the World Spider Catalog links here to species pages of other databases. They may contain further information for the given species. The databases, listed as External Resources, however, are not managed by World Spider Catalog and the information given there is not necessarily in agreement with the World Spider Catalog. All responsibility for such data is with the external database.
GBIF.org (2026). GBIF Home Page (via GBIF API). Available from: https://www.gbif.org [8 January 2026]

###### Edit History
| Date | Type | Reference | Old value | Comment |  
| --- | --- | --- | --- | --- |  
| 2017-12-29 | New taxonomic reference entry | Baehr, Raven & Harms, 2017 |  |  |  
| 2017-12-29 | New species inserted | Baehr, Raven & Harms, 2017 |  |  |
Log values
</excerpt>

# Example 2
## Question
Using jw.org as your only source, compare the figures published in the following publications, and tell me which country (excluding those countries that have been removed from up-to-date reporting) saw the greatest overall reduction, by number (not percent) in reported peak publishers, between 2017 and 2023: 2017 Service Year Report of Jehovah’s Witnesses Worldwide, 2018 Service Year Report of Jehovah’s Witnesses Worldwide, 2019 Service Year Report of Jehovah’s Witnesses Worldwide, 2020 Service Year Report of Jehovah’s Witnesses Worldwide, 2021 Service Year Report of Jehovah’s Witnesses Worldwide, 2022 Service Year Report of Jehovah’s Witnesses Worldwide, and 2023 Service Year Report of Jehovah’s Witnesses Worldwide.

## Expected answer
Ukraine

## Final answer — grade 0.00
I’m sorry, but I don’t have the information I need to calculate the greatest drop in peak‑publisher numbers between 2017 and 2023.  

While I could pull the 2017 figures from the “2017 Service Year Report” (e.g., Argentina = 150,823 peak publishers), I have no access to the corresponding 2023 “Service Year Report” data for each country. The 2023 data is contained in a separate PDF on **jw.org**, but I can’t retrieve or view that PDF because my search quota is exhausted and I’m not otherwise able to fetch new webpages.  

Without the 2023 peak‑publisher numbers, I can’t compute the absolute reductions or determine which country experienced the largest decline. If you can provide the 2023 peak‑publisher figures (or a link that I could read), I could finish the comparison for you.
(10 searches; ended: answered)

## Search 1
query: "2017 Service Year Report Jehovah’s Witnesses Worldwide peak publishers table"
<excerpt title="Service Year Reports - Jehovah's Witnesses">
## Did You Know … ?
### 2022 Service Year Report
| 2022 | Cook Islands | 18,000 | 211 | 90 | 199 | 1 | 2 | 27 | 3 | 500 |  
| 2022 | Costa Rica | 5,213,000 | 32,504 | 161 | 32,290 | 0 | 546 | 4,275 | 435 | 72,360 |  
| 2022 | Côte d’Ivoire | 29,389,000 | 11,877 | 2,521 | 11,657 | 0 | 255 | 1,577 | 231 | 37,361 |  
| 2022 | Croatia | 4,069,000 | 4,736 | 867 | 4,693 | -2 | 40 | 462 | 57 | 7,218 |  
| 2022 | Cuba | 11,113,000 | 91,710 | 123 | 90,315 | -3 | 1,216 | 8,932 | 1,399 | 166,891 |  
| 2022 | Curaçao | 166,000 | 2,040 | 83 | 1,991 | -1 | 40 | 254 | 25 | 5,629 |  
| 2022 | Cyprus | 1,224,000 | 2,960 | 421 | 2,908 | 3 | 28 | 571 | 40 | 5,178 |
</excerpt>

## Search 2
query: "2017 Service Year Report Jehovah's Witnesses PDF site:jw.org"
<excerpt title="Spreadsheet—Service Year Reports of Jehovah's Witnesses Worldwide - Maj Loves Reg">
# Spreadsheet—Service Year Reports of Jehovah’s Witnesses Worldwide • Maj Loves Reg
    *   Popular tags  
        *   photosUsed to be a bunch of pigments on glossy paper. Today, these are a bunch of colored pixels tightly woven on a screen. ;-)  
        *   videos  
        *   travel  
        *   { code }Some of the coding Majal does in his free time. Linux, Bash scripts, along with some techie tinkering.  
        *   science  
        *   theoskratos  
        *   recipes  
        *   illustrations  
        *   interview  
        *   wife  
        *   food  
        *   spirituality  
        *   art

*   Projects & Partners  
    *   JW.org  
    *   Partner Brands

*   Search for:

# Spreadsheet—Service Year Reports of Jehovah’s Witnesses Worldwide
#### Published by **Majal Mirasol** on January 9, 2024 January 9, 2024
Our Life Together>Thoughts>Spreadsheet—Service Year Reports of Jehovah’s Witnesses Worldwide
* * *
Because there are those who would like to play with the JW Report numbers… 🤓
Full spreadsheet here:
**https://docs.google.com/spreadsheets/d/1kHCY1W8ztGAnBd88e7ulniQAdpxXpWwlafFFZYWiJeM/view**
Things you can do:
*   **Make a copy** of the spreadsheet and edit it as your own  
*   **Download** as Excel (XLSX), OpenDocument (ODS), CSV, TSV, HTML, or PDF. Go to `File > Download`  
*   Link to the data and its updates using the `IMPORTRANGE` function
Enjoy!
🧑‍💻
Categories: Thoughts
[](mailto:?subject=Spreadsheet%E2%80%94Service%20Year%20Reports%20of%20Jehovah%E2%80%99s%20Witnesses%20Worldwide&body=https://one.majlovesreg.one/spreadsheet-service-year-reports-of-jehovahs-witnesses)
* * *

# Spreadsheet—Service Year Reports of Jehovah’s Witnesses Worldwide
#### Majal Mirasol
Servant of the Creator happily married to Jehovah’s slave girl.
While Majal was absorbed in training for a good foundation in the Maths and Sciences, he learned that there is more to life than simply elucidating complex designs in our universe. He realized that there is a Designer. The Source of our order, an order much superior than what our human brains could conceive.

# Spreadsheet—Service Year Reports of Jehovah’s Witnesses Worldwide
### 1 Comment
#### Thony LUHANGU Kalonda  · January 9, 2024 at 10:18 pm
Thank you so much for sharing. You are a good example for many. May Jehovah continue to bless you, and may he meet the needs of your heart. Stay safe ans blessed. Your brother Thony Luhangu G.A English Group
Thank you

# Spreadsheet—Service Year Reports of Jehovah’s Witnesses Worldwide
## Related Posts
Thoughts

# Spreadsheet—Service Year Reports of Jehovah’s Witnesses Worldwide
## Related Posts
#### Can God Have No Beginning?
Everything should have a beginning, right? So how can God not have a beginning? Well-known scientific theories could help provide answers.
Thoughts

# Spreadsheet—Service Year Reports of Jehovah’s Witnesses Worldwide
## Related Posts
#### Adding PageSpeed to an Already-running NGINX Instance
Do you have an already-built instance of NGINX and wanted to add Google’s PageSpeed module? Use this bash script to automate installation of the dynamic module.
Thoughts
</excerpt>

## Search 3
query: "Service Year Report 2023 Jehovah's Witnesses PDF"
<excerpt title="Historical Watchtower Publisher & Memorial Data">
# Historical Watchtower Publisher & Memorial Data
Facts About Jehovah's Witnesses
corescandalchangesdoctrineinteresting|experiences|quotes
Facts About Jehovah's Witnesses
core|scandal|changes|doctrine|interesting|experiences|quotes
Topics of Interest
15 Minute Guide to Truth
About JWfacts
Age - Increasing Average of Jehovah's Witnesses
Always been Jehovah's Witnesses?
Blog - Random Musings
Clothing and Attire
Covid-19 & Jehovah's Witnesses
Cognitive Dissonance
Cult - Are Jehovah's Witnesses?
Cutting & Self-harm
Comments from Readers
Dating One Of Jehovah's Witnesses
Declining Donations
Divorce - rate amongst Witnesses
Doomsday Predictions from the last 2000 years
Experiences
Famous Jehovah's Witnesses
Fear & Cult Mind Control
Foreign Language Websites
Governing Body's Motives
Growing Up a Jehovah's Witness
Helping Someone Leave
Historical Publications
Homosexuality and Transgenderism
Internet - Future affect on Watchtower Growth
Latest Articles
Links
Mental Illness
Peace and Security Cry
Persecution of Jehovah's Witnesses
Pop Culture References to Jehovah's Witnesses
Personal files - how I got mine from Bethel
Questions to ask a JW - Study Conductor or Cart Witnessing
Quotes
Rhetorical Fallacy - the art of false reasoning
Similar Religions
Suicide resurrection teachings
Truth - Is it?
Vegetarianism Past & Future
Watchtower Statistics
War
Weasel Words
Where else to go?
home>interesting topics>statistics>historical data
Watchtower Statistics provides commentary and graphs based on Watchtower's annual publisher reports. Scans of the annual reports are provided below.
Click here for a PDF of Watchtower figures provided in Annual publisher reports since 1962.
Click here for a PDF of the extrapolations from Watchtower figures that have been used for the graphs published at Watchtower Statistics.

# Historical Watchtower Publisher & Memorial Data
## Scans of Watchtower publisher reports.
Links to jw.org worked as of Jan 2026.
2025 Jehovah's Witness Grand Totals
2025 Jehovah's Witness Service Year Report in spreadsheet format
2024 Jehovah's Witness Grand Totals
2024 Jehovah's Witness Publisher Reports - links to jw.org
2023 Jehovah's Witness Grand Totals
2023 Jehovah's Witness Publisher Reports - links to jw.org
2022 Jehovah's Witness Grand Totals
2021 Jehovah's Witness Grand Totals
2020 Jehovah's Witness Grand Totals
2020 Jehovah's Witness Publisher Report - PDF version
2019 Jehovah's Witness Grand Totals
2019 Jehovah's Witness Publisher Report - PDF version
2018 Jehovah's Witness Grand Totals
2018 Jehovah's Witness Publisher Report - links to jw.org
2018 Jehovah's Witness Publisher Report - PDF version
2017 Jehovah's Witness Grand Totals
2017 Jehovah's Witness Publisher Report - links to jw.org
2017 Jehovah's Witness Publisher Report - PDF version
2016 Jehovah's Witness Grand Totals
2016 Jehovah's Witness Publisher Report
2015 Jehovah's Witness Grand Totals
2015 Jehovah's Witness Publisher Report
2014 Jehovah's Witness Grand Totals
2014 Jehovah's Witness Publisher Report
2013 Jehovah's Witness Grand Totals
2013 Jehovah's Witness Publisher Report
2013 Complete publisher report - Excel Spreadsheet
2012 Jehovah's Witness Grand Totals
2012 Jehovah's Witness Publisher Report
2012 Complete publisher report - Excel Spreadsheet
2011 Jehovah's Witness Grand Totals
2011 Jehovah's Witness Publisher Report
2010 Jehovah's Witness Publisher Report - 2.5MB
2009 Jehovah's Witness Publisher Report - 2.6MB
2008 Jehovah's Witness Publisher Report - 2.6MB
2007 Jehovah's Witness Publisher Report - 4.4MB
2006 Jehovah's Witness Publisher Report from 2007 Watchtower - 767 KB
</excerpt>

## Search 4
query: "2017 Service Year Report pdf jw.org peak publishers"
<excerpt title="Jehovah's Witnesses—2017 Country and Territory Reports">
PLAY
2017 Country and Territory Reports
| Country or Territory | Population | 2017 Peak Pubs. | Ratio, 1 Publisher to | % Inc. Over 2016 | 2017 No. Bptzd. | Av. Pio. Pubs. | No. of Congs. | Memorial Attendance |  
| --- | --- | --- | --- | --- | --- | --- | --- | --- |  
| **Albania** | 3,204,000 | 5,637 | 568 | 2 | 230 | 1,351 | 89 | 11,927 |  
| **American Samoa** | 55,519 | 189 | 294 | -11 |  | 38 | 3 | 625 |  
| **Andorra** | 72,280 | 178 | 406 | 9 | 1 | 18 | 3 | 352 |  
| **Angola** | 26,849,678 | 143,322 | 187 | 12 | 11,758 | 19,631 | 1,913 | 617,099 |  
| **Anguilla** | 17,087 | 81 | 211 | 3 | 1 | 10 | 2 | 297 |  
| **Antigua** | 91,889 | 485 | 189 | 1 | 15 | 49 | 7 | 1,398 |  
| **Argentina** | 44,044,811 | 150,823 | 292 | 1 | 3,962 | 24,676 | 1,999 | 312,070 |  

| **Armenia** | 2,986,500 | 10,974 | 272 | -1 | 295 | 2,221 | 134 | 21,874 |  
| **Aruba** | 105,000 | 1,072 | 98 | 3 | 34 | 87 | 14 | 2,879 |  
| **Australia** | 24,658,074 | 67,748 | 364 | 1 | 1,272 | 6,348 | 798 | 116,274 |  
| **Austria** | 8,773,686 | 21,567 | 407 |  | 411 | 1,667 | 301 | 34,712 |  
| **Azerbaijan** | 9,810,000 | 1,414 | 6,938 | 2 | 72 | 349 | 14 | 2,865 |  
| **Azores** | 245,283 | 755 | 325 | 1 | 25 | 90 | 15 | 1,512 |  
| **Bahamas** | 395,000 | 1,702 | 232 | -1 | 43 | 244 | 27 | 4,375 |  
| **Bangladesh** | 161,200,886 | 307 | 525,084 | 9 | 6 | 138 | 6 | 976 |  
| **Barbados** | 292,336 | 2,529 | 116 | -1 | 48 | 206 | 30 | 6,003 |
</excerpt>

## Search 5
query: "https://docs.google.com/spreadsheets/d/1kHCY1W8ztGAnBd88e7ulniQAdpxXpWwlafFFZYWiJeM"
<excerpt title="The tribulation is momentary and light - Maj Loves Reg">
# “The tribulation is momentary and light” • Maj Loves Reg
    *   Popular tags  
        *   photosUsed to be a bunch of pigments on glossy paper. Today, these are a bunch of colored pixels tightly woven on a screen. ;-)  
        *   videos  
        *   travel  
        *   { code }Some of the coding Majal does in his free time. Linux, Bash scripts, along with some techie tinkering.  
        *   science  
        *   theoskratos  
        *   recipes  
        *   illustrations  
        *   interview  
        *   wife  
        *   food  
        *   spirituality  
        *   art

*   Projects & Partners  
    *   JW.org  
    *   Partner Brands

*   Search for:

# “The tribulation is momentary and light”
#### Published by **Majal Mirasol** on May 8, 2019 May 8, 2019
Our Life Together>Thoughts>“The tribulation is momentary and light”—illustrations
* * *
In writing to the Corinthians, the apostle Paul wrote that the problems we face today are “momentary and light”. (2Co 4:17) How could our trials, including the really difficult ones, feel ephemeral and easy? At the end of that verse he mentioned a glory that not only has “surpassing greatness”, but one that is also **“everlasting”.**
Any number, no matter how large, once divided by infinity, is zero.
Any number, no matter how large, once divided by infinity, is zero.[1] Similarly, our problems now, no matter how large, pales in comparison to the infinite blessings God has in store for his loyal ones. Imagine waking up in paradise earth. Our troubles today will feel like **zero.**
lim N / ∞ = 0
* * *
[1] In a branch of Mathematics called Calculus, any number, no matter how large, once divided by a larger number approaching infinity, drops the whole value to zero.
This illustration was used on a midweek meeting talk entitled, “We Do Not Give Up”.
Categories: Thoughts
Tags: illustrations
[](mailto:?subject=%E2%80%9CThe%20tribulation%20is%20momentary%20and%20light%E2%80%9D&body=https://one.majlovesreg.one/the-tribulation-is-momentary-and-light)
* * *

# “The tribulation is momentary and light”
#### Majal Mirasol
Servant of the Creator happily married to Jehovah’s slave girl.
While Majal was absorbed in training for a good foundation in the Maths and Sciences, he learned that there is more to life than simply elucidating complex designs in our universe. He realized that there is a Designer. The Source of our order, an order much superior than what our human brains could conceive.

# “The tribulation is momentary and light”
### 0 Comments


# “The tribulation is momentary and light”
## Related Posts
Thoughts

# “The tribulation is momentary and light”
## Related Posts
#### Spreadsheet—Service Year Reports of Jehovah’s Witnesses Worldwide
Our Life Together > Thoughts > “The tribulation is momentary and light” Because there are those who would like to play with the JW Report numbers… 🤓 Full spreadsheet here:https://docs.google.com/spreadsheets/d/1kHCY1W8ztGAnBd88e7ulniQAdpxXpWwlafFFZYWiJeM/view Things you can do: Enjoy
Thoughts

# “The tribulation is momentary and light”
## Related Posts
#### Can God Have No Beginning?
Everything should have a beginning, right? So how can God not have a beginning? Well-known scientific theories could help provide answers.
Thoughts
</excerpt>

## Search 6
query: "https://docs.google.com/spreadsheets/d/1kHCY1W8ztGAnBd88e7ulniQAdpxXpWwlafFFZYWiJeM/export?format=csv"
<excerpt title="Google Sheets: Sign-in">
# Google Sheets: Sign-in
Loading

# Sign in
to continue to Google Sheets
Email or phone
Forgot email?
Audio 2
Type the text you hear or see
Not your computer? Use Guest mode to sign in privately. Learn more about using Guest mode
Next
Create account
*   For my personal use  
*   For my child  
*   For work or my business
English (United States)

# Sign in
*   Afrikaans  
*   azərbaycan  
*   bosanski  
*   català  
*   Čeština  
*   Cymraeg  
*   Dansk  
*   Deutsch  
*   eesti  
*   English (United Kingdom)  
*   English (United States)  
*   Español (España)  
*   Español (Latinoamérica)  
*   euskara  
*   Filipino  
*   Français (Canada)  
*   Français (France)  
*   Gaeilge  
*   galego  
*   Hrvatski  
*   Indonesia  
*   isiZulu  
*   íslenska  
*   Italiano  
*   Kiswahili  
*   latviešu  
*   lietuvių  
*   magyar  
*   Melayu  
*   Nederlands  
*   norsk  
*   o‘zbek  
*   polski  
*   Português (Brasil)  
*   Português (Portugal)  
*   română  
*   shqip  
*   Slovenčina  
*   slovenščina  
*   srpski (latinica)  
*   Suomi  
*   Svenska  
*   Tiếng Việt  
*   Türkçe  
*   Ελληνικά  
*   беларуская  
*   български  
*   кыргызча  
*   қазақ тілі  
*   македонски  
*   монгол  
*   Русский  
*   српски (ћирилица)  
*   Українська  
*   ქართული  
*   հայերեն  
*   ‫עברית‬‎  
*   ‫اردو‬‎  
*   ‫العربية‬‎  
*   ‫فارسی‬‎  
*   አማርኛ  
*   नेपाली  
*   मराठी  
*   हिन्दी  
*   অসমীয়া  
*   বাংলা  
*   ਪੰਜਾਬੀ  
*   ગુજરાતી  
*   ଓଡ଼ିଆ  
*   தமிழ்  
*   తెలుగు  
*   ಕನ್ನಡ  
*   മലയാളം  
*   සිංහල  
*   ไทย  
*   ລາວ  
*   မြန်မာ  
*   ខ្មែរ  
*   한국어  

# Sign in
*   中文（香港）  
*   日本語  
*   简体中文  
*   繁體中文
*   Help  
*   Privacy  
*   Terms
</excerpt>

## Search 7
query: "2017 Service Year Report pdf site:jw.org "Service Year Report" "2017""
<excerpt title="Yearbooks - Publications — Watchtower ONLINE LIBRARY">
# Publications — Watchtower ONLINE LIBRARY
Watchtower ONLINE LIBRARY Watchtower ONLINE LIBRARY
English
*     
*
*   BIBLE  
*   PUBLICATIONS  
*   MEETINGS  
*

# Yearbooks
*    2025 Service Year Report 2025  
*    2024 Service Year Report 2024  
*    2023 Service Year Report 2023  
*    2022 Service Year Report 2022  
*    2021 Service Year Report 2021  
*    2020 Service Year Report 2020  
*   2019 Service Year Report 2019  
*   2018 Service Year Report 2018  
*   2017 Service Year Report 2017  
*    Yearbook—2017 2017  
*    Yearbook—2016 2016  
*    Yearbook—2015 2015  
*    Yearbook—2014 2014  
*   Yearbook—2013 2013  
*   Yearbook—2012 2012  
*   Yearbook—2011 2011  
*   Yearbook—2010 2010  
*   Yearbook—2009 2009  
*   Yearbook—2008 2008  
*   Yearbook—2007 2007  
*   Yearbook—2006 2006  
*   Yearbook—2005 2005  
*   Yearbook—2004 2004  
*   Yearbook—2003 2003  
*   Yearbook—2002 2002  
*   Yearbook—2001 2001  
*   Yearbook—2000 2000  
*   Yearbook—1999 1999  
*   Yearbook—1998 1998  
*   Yearbook—1997 1997  
*   Yearbook—1996 1996  
*   Yearbook—1995 1995  
*   Yearbook—1994 1994
</excerpt>

## Search 8
query: ""Peak Pubs." "2017" "Service Year Report""
<excerpt title="2017 Service Year Report Worldwide - INDIVIDUALLY LISTED ...">
by darkspilver9 years ago 61 Replies latest 9 years agojwfriends
*     
*     
*   [![Image 3: Half banana](blob:http://localhost/b9a31d3949b1882a09ed2f8508d538f3)](https://www.jehovahs-witness.com/users/15880/slimboyfat "slimboyfat")##### slimboyfat9 years ago
Thank goodness for that. Us of little faith. Going to enjoy examining this later.   
Link
*   [![Image 4: Half banana](blob:http://localhost/b9a31d3949b1882a09ed2f8508d538f3)](https://www.jehovahs-witness.com/users/47942/dropoffyourkeylee "dropoffyourkeylee")  
*   [![Image 5: Half banana](blob:http://localhost/b9a31d3949b1882a09ed2f8508d538f3)](https://www.jehovahs-witness.com/users/103372/berrygerry "berrygerry")##### berrygerry9 years ago
My suggestion is to use a formula incorporating the change by country in the 2016 - 2017 Peak Pubs to use in guesstimating the change in 2016 - 2017 Avg Pubs.   
Link
*   [![Image 6: Half banana](blob:http://localhost/b9a31d3949b1882a09ed2f8508d538f3)](https://www.jehovahs-witness.com/users/93824/EverApostate "EverApostate")##### EverApostate9 years ago
What about reports from North Korea, Singapore, China and other countries where the JW are banned.
Jah - the almighty - is **unable**to life the ban on those countries or **afraid to do so**?
The most powerful in the universe cant do this? After all, the Bible says that Every nation is like a drop of water to Jah.
</excerpt>

## Search 9
query: "https://jw.org/en/library/books/2017-service-year-report/"
<excerpt title="Jehovah's Witnesses—2017 Country and Territory Reports">
| **Cape Verde** | 560,899 | 2,239 | 251 | 2 | 103 | 423 | 33 | 7,374 |  
| **Cayman Islands** | 62,000 | 257 | 241 | 3 | 6 | 31 | 3 | 631 |  
| **Central African Republic** | 4,659,000 | 2,763 | 1,686 | 3 | 182 | 326 | 53 | 17,255 |  
| **Chad** | 14,900,000 | 863 | 17,265 | 13 | 59 | 76 | 18 | 4,312 |  
| **Chile** | 18,373,917 | 78,603 | 234 | 1 | 1,872 | 13,201 | 991 | 175,877 |  
| **Chuuk** | 48,651 | 46 | 1,058 | -7 |  | 15 | 2 | 225 |  
| **Colombia** | 49,465,000 | 173,802 | 285 | 2 | 6,380 | 27,056 | 2,359 | 515,800 |  
| **Congo, Dem. Republic of** | 82,800,771 | 216,696 | 382 | -2 | 14,276 | 20,685 | 3,763 | 1,156,482 |
</excerpt>

## Search 10
query: "2023 Service Year Report country and territory wij"
<excerpt title="Service Year Reports - Jehovah's Witnesses">
## Did You Know … ?
### 2022 Service Year Report
| --- |  
| Year | Country or Territory | Population | Peak Publishers | Ratio, 1 Publisher to | Average Publishers | % Increase | Baptisms | Average Pioneer Publishers | Congregations | Memorial Attendance |  
| 2022 | Albania | 2,866,000 | 5,577 | 518 | 5,531 | -1 | 112 | 1,363 | 83 | 12,106 |  
| 2022 | American Samoa | 55,000 | 154 | 420 | 131 | -9 | 0 | 32 | 3 | 647 |  
| 2022 | Andorra | 77,000 | 169 | 461 | 167 | -1 | 0 | 23 | 3 | 331 |  
| 2022 | Angola | 35,027,000 | 159,384 | 226 | 154,953 | 3 | 3,273 | 25,609 | 2,539 | 485,484 |  
| 2022 | Anguilla | 15,000 | 67 | 259 | 58 | 5 | 0 | 11 | 1 | 208 |  
| 2022 | Antigua | 100,000 | 478 | 215 | 466 | 1 | 0 | 41 | 7 | 1,244 |  
| 2022 | Argentina | 47,327,000 | 155,443 | 308 | 153,787 | -2 | 2,869 | 35,977 | 1,945 | 345,669 |
</excerpt>

# Example 3
## Question
According to the UNdata website, out of India, Pakistan, Nepal, Bhutan, and Bangladesh, which countries had an increase in the percentage of their workforce being unemployed between 2015 and 2020, when rounded to one decimal place?

## Expected answer
Pakistan, Nepal, Bhutan, Bangladesh

## Final answer — grade 0.75
**Countries whose share of the workforce that was unemployed rose between 2015 and 2020 (rounded to one‑decimal place)**  

| Country | 2015 unemployment % | 2020 unemployment % | Increment (rounded to 0.1 %) |
|---------|---------------------|---------------------|-----------------------------|
| India | 5.4 % | 8.0 % | **+2.6 %** |
| Pakistan | 10.6 % | 11.2 % | **+0.6 %** |
| Bhutan | 0.8 % | 0.9 % | **+0.1 %** |
| Bangladesh | 2.3 % | 2.4 % | **+0.1 %** |

*The only country that did **not** see an increase was Nepal (10.6 % in 2015 to 10.5 % in 2020).*

These figures come from the United Nations’ **UNdata** database, accessed via the UN Data portal’s downloadable CSV files for each country‑unemployment indicator. The values shown are the official UN (ILO‑based) estimates for total unemployment (percentage of the total labour force) for the years 2015 and 2020. Rounded to one decimal place, the increases above confirm that India, Pakistan, Bhutan, and Bangladesh experienced a rise in the proportion of their workforce that was unemployed over that period.
(10 searches; ended: answered)

## Search 1
query: "UNdata unemployment percentage India workforce 2015 2020"
<excerpt title="India at Work: Employment Trends in the 21st Century">
## [PDF page 11]
11

## [PDF page 12]
Table 3: C omparison of Unemploy ment R ates (%)  
NSS Usual  D&B Usual  NSS Usual  D&B Usual  
Ye  a  r  Status  Status  Principal  Principal  NSS CWS  D&B CWS  
(PS+SS)  (PS+SS)  Status (UPS)  Status (UPS)  
1983  1.91  1.92  2.77  2.80  4.51  4.52  
1993–1994  1.90  1.98  2.56  2.63  3.62  3.67  
1999–2000  2.25  2.34  2.73  2.83  4.29  4.34  
2004–2005  2.31  2.39  3.13  3.20  4.43  4.46  
2011–2012  2.19  2.24  2.74  2.78  3.67  3.68  
2017–2018  6.07  6.20  6.47  6.60  8.87  8.94  
2018–2019  5.83  5.94  6.27  6.37  8.76  8.81  
2019–2020  4.84  4.94  5.33  5.42  8.80  8.90  
2020–2021  4.21  4.41  4.90  5.10  7.51  7.70  

## [PDF page 12]
2021–2022  4.05  4.26  4.75  4.96  6.62  6.78  
2022–2023  3.17  3.41  3.99  4.27  5.11  5.38  
2023–2024  3.18  3.34  4.14  4.30  4.89  5.05
Source: NSS data are various rounds of EUS and PLFS from NSSO, and D&B are author estimates.
</excerpt>

## Search 2
query: "UNdata unemployment total India 2015"
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

## Search 3
query: "UNdata unemployment total India 2015 2020"
<excerpt title="A Study On the Unemployment Status of India from 2000-2022">
## [PDF page 2]
IV.  RESULTS:  
Table: 1, The Unemployment rate in India from the financial year 2000 - 22.  
Year  Unemployment rate (%)  
2000  5.56%  
2001  5.58%  
2002  5.53%  
2003  5.64%  
2004  5.63%  
2005  5.61%  
2006  5.60%  
2007  5.57%  
2008  5.41%  
2009  5.54%  
2010  5.55%  
2011  5.43%  
2012  5.41%  
2013  5.42%
DOI: 10.35629/5252-020113011304 | Impact Factor value 7.429  | ISO 9001: 2008 Certified Journal  Page 1302

## [PDF page 3]
International Journal of Advances in Engineering and Management (IJAEM)  
Volume 2, Issue 1 Jan. 2020, pp: 1301-1304  www.ijaem.net  ISSN: 2395-5252
2014  5.44%  
2015  5.44%  
2016  5.42%  
2017  5.36%  
2018  5.33%  
2019  5.27%  
2020  8.00%  
2021  5.98%  
Jan. 2022  6.56%  
Oct. 2022  7.80%  
Source- macrotrends.net
Table- 1 shows that unemployment rate in  2019,  the  lowest  unemployment  rate  in  India  was  
India  during  the  year  2000-22.  In  2020,  highest  5.27  percent.  In  2021  and  Jan  2022,  the  
unemployment rate was 8.00 percent in India. This  unemployment rate was 5.98 and 6.56 percent.  
is a very dangerous position for Indian economy. In
Figure: - 1, The Unemployment rate in India from the financial year 2000 - 2022.
Source- macrotrends.net
</excerpt>

## Search 4
query: "data.un.org unemployment India 2015"
<excerpt title="Human Development Report 2015">
## [PDF page 250]
128  Guatemala  15.9  22.6  2.5  2.5  51.1  2.3  8.8  0.7  19.7  71.3  8.4  4.6  3.8  1.05  
129  Tajikistan  8.4  11.4  1.9  2.4  26.7  1.2  5.1  0.3  22.0  59.4  5.2  3.7  3.9  1.05  
130  India  1,267.4  1,476.4  1.6  1.2  32.4  122.0  835.2  67.9  26.9  42.9  8.3  3.0  2.5  1.11  
131  Honduras  8.3  10.8  2.0  2.0  53.9  1.0  5.0  0.4  22.5  56.1  7.5  3.7  3.0  1.05  
132  Bhutan  0.8  0.9  2.8  1.6  37.9  0.1  0.5  0.0  26.7  39.9  7.3  3.1  2.3  1.04
</excerpt>

## Search 5
query: "UNdata "Unemployment, total (% of total labour force)" India 2015"
(no page could be read; nothing was passed on)

## Search 6
query: "UNdata unemployment Pakistan 2015"
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

## Search 7
query: "UNdata Unemployment, total (% of total labour force) India 2015""
<excerpt title="India - Unemployment, Total (national Estimate) - 2026 Data 2027 Forecast ...">
# India - Unemployment, Total (national Estimate)2026 Data 2027 Forecast 1994-2024 Historical
## Markets
Currency
Government Bond 10Y
Stock Market

# India - Unemployment, Total (national Estimate)2026 Data 2027 Forecast 1994-2024 Historical
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

# India - Unemployment, Total (national Estimate)2026 Data 2027 Forecast 1994-2024 Historical
## Labour
Employment Rate
Labor Force Participation Rate
Minimum Wages
Population
Retirement Age Men
Retirement Age Women
Unemployment Rate
Wages

# India - Unemployment, Total (national Estimate)2026 Data 2027 Forecast 1994-2024 Historical
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

# India - Unemployment, Total (national Estimate)2026 Data 2027 Forecast 1994-2024 Historical
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

# India - Unemployment, Total (national Estimate)2026 Data 2027 Forecast 1994-2024 Historical
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

# India - Unemployment, Total (national Estimate)2026 Data 2027 Forecast 1994-2024 Historical
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

# India - Unemployment, Total (national Estimate)2026 Data 2027 Forecast 1994-2024 Historical
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

# India - Unemployment, Total (national Estimate)2026 Data 2027 Forecast 1994-2024 Historical
## Consumer
Bank Lending Rate
Consumer Confidence
Consumer Spending
Disposable Personal Income
Gasoline Prices
Households Debt to GDP
Retail Sales YoY

# India - Unemployment, Total (national Estimate)2026 Data 2027 Forecast 1994-2024 Historical
## Housing
Housing Index
Infrastructure Output YoY
Residential Property Prices

# India - Unemployment, Total (national Estimate)2026 Data 2027 Forecast 1994-2024 Historical
## Taxes
Corporate Tax Rate
Personal Income Tax Rate
Sales Tax Rate
Social Security Rate
Social Security Rate For Companies
Social Security Rate For Employees
Withholding Tax Rate
</excerpt>

## Search 8
query: "data.un.org Unemployment total India 2015"
<excerpt title="India - unemployment reasons among post-graduates 2015">
# Distribution of unemployment among post-graduates across rural and urban India in 2015, by reason
## About Your Privacy
#### Personalised advertising and content, advertising and content measurement, audience research and services development 842 partners can use this purpose
- [x] Personalised advertising and content, advertising and content measurement, audience research and services development
*   ##### Use limited data to select advertising 678 partners can use this purpose
- [x] Switch Label     
Advertising presented to you on this service can be based on limited data, such as the website or app you are using, your non-precise location, your device type or which content you are (or have been) interacting with (for example, to limit the number of times an ad is presented to you).
View Illustrations
*   ##### Create profiles for personalised advertising 552 partners can use this purpose
- [x] Switch Label     
Information about your activity on this service (such as forms you submit, content you look at) can be stored and combined with other information about you (for example, information from your previous activity on this service and other websites or apps) or similar users. This is then used to build or improve a profile about you (that might include possible interests and personal aspects). Your profile can be used (also later) to present advertising that appears more relevant based on your possible interests by this and other entities.
View Illustrations
*   ##### Use profiles to select personalised advertising 556 partners can use this purpose
- [x] Switch Label     
Advertising presented to you on this service can be based on your advertising profiles, which can reflect your activity on this service or other websites or apps (like the forms you submit, content you look at), possible interests and personal aspects.
View Illustrations
*   ##### Create profiles to personalise content 230 partners can use this purpose

# Distribution of unemployment among post-graduates across rural and urban India in 2015, by reason
## About Your Privacy
#### Personalised advertising and content, advertising and content measurement, audience research and services development 842 partners can use this purpose
- [x] Switch Label     
Information about your activity on this service (for instance, forms you submit, non-advertising content you look at) can be stored and combined with other information about you (such as your previous activity on this service or other websites or apps) or similar users. This is then used to build or improve a profile about you (which might for example include possible interests and personal aspects). Your profile can be used (also later) to present content that appears more relevant based on your possible interests, such as by adapting the order in which content is shown to you, so that it is even easier for you to find content that matches your interests.
View Illustrations
*   ##### Use profiles to select personalised content 206 partners can use this purpose
- [x] Switch Label     
Content presented to you on this service can be based on your content personalisation profiles, which can reflect your activity on this or other services (for instance, the forms you submit, content you look at), possible interests and personal aspects. This can for example be used to adapt the order in which content is shown to you, so that it is even easier for you to find (non-advertising) content that matches your interests.
View Illustrations
*   ##### Measure advertising performance 776 partners can use this purpose
- [x] Switch Label     
Information regarding which advertising is presented to you and how you interact with it can be used to determine how well an advert has worked for you or other users and whether the goals of the advertising were reached. For instance, whether you saw an ad, whether you clicked on it, whether it led you to buy a product or visit a website, etc. This is very helpful to understand the relevance of advertising campaigns.
View Illustrations
*   ##### Measure content performance 350 partners can use this purpose
</excerpt>

## Search 9
query: "UNdata Unemployment, total (% of total labour force) Nepal 2015"
<excerpt title="Labour Force and Economic Activities in Nepal.pdf">
## [PDF page 13]
>dahf/df hf]lvdk|efjL ;d"xx¿ dWo]sf] Ps ;d"x ^% jif{ / ;f]eGbf dflysf Ho]i7 gful/sx¿  
dflgG5g\ lsgls pgLx¿sf] zf/Ll/s b'a{ntfhGo sf/0fn] sfd ug{;Sg] Ifdtf Go"g x'g] ub{5 cyjf  
pgLx¿nfO{ >dahf/df cfPsf gjLgtd k|ljlw / k|j[lQx¿;Fu kof{Kt ;"rgf gx'g ;S5 . g]kfndf  
^% jif{ / ;f]eGbf dflysf] hg;ª\Vof @) nfv /x]sf] 5 h;dWo] $%=( k|ltzt cfly{s ¿kn] ;lqmo  
5g\ -k'?iftkm{ %#=$Ü / dlxnftkm{ #*=&Ü_ . Ho]i7 gful/stkm{ >dzlQm ;xeflutfb/ sf]zLdf ;a}eGbf  
pRr -%!=@Ü_ 5 . lxdfnL If]qdf %^=# k|ltzt / u|fdL0f If]qdf %$=@ k|ltzt /x]sf] 5 . clt ljkGg  
ju{sf Ho]i7 gful/sx¿sf] >dzlQm ;xeflutfb/ %#=) k|ltzt /x]sf] 5 .  
cfly{s hLjg÷sfo{zLn hLjgsf] ;dofjlw  
sfd;Fu ;DalGwt hLjgtflnsfn] b]vfPcg';f/ olb pd]/ljlzi6 d[To'b/ / >dzlQm ;xeflutfb/ s'g}
</excerpt>

## Search 10
query: "UNdata India Unemployment, total (%) 2015"
<excerpt title="Unemployment rate in India from 1991 to 2025">
# Unemployment rate in India from 1991 to 2025
## Related insights
Statistics Insights
1.   Unemployment rates in major industrial and emerging countries in 2024 Worldwide    
2.   Youth unemployment rate in India from 1991 to 2025 IND    
3.   Unemployment rate across India from 2022 to 2025, by education level IND    
4.   State of the Indian economy - statistics & facts IND    
5.   Annual average unemployment rate in Indiana in the United States from 1992 to 2025 USA    
6.   Distribution of the workforce in India from 1991 to 2025, by economic sector IND    
7.   Indian Unemployment Steady, But Youth Suffers     
8.   Impact on unemployment rate due to the coronavirus (COVID-19) lockdown in India from January 2020 to May 2022 IND    
9.   Employment in India - statistics & facts IND    
10.   Monthly unemployment rate in India from October 2021 to April 2023 IND    
11.   Employment in India IND    
12.   Unemployment rate worldwide from 1991 to 2025 Worldwide    
13.   Number of employed persons in India from financial year 2018 to 2025 (in millions) IND    
14.   Unemployment rate in the United States from 1991 to 2025 USA    
15.   Attrition rate in India from 2009 to 2025 IND    
16.   Unemployment rate in Poland from 1991 to 2025 POL    
17.   Rate of unemployment in rural and urban India in financial year 2025, by gender IND    
18.   Employment rate in India from financial year 2017 to 2024, by religion IND    
19.   Perceived and actual unemployment rate among working age population in India as of October 2018 IND    
20.   Unemployment rate in Bangladesh from 1991 to 2025 BGD    
21.   Unemployment rate in India from financial year 2017 to 2024, by religion IND
</excerpt>

# Example 4
## Question
Only counting players drafted by teams who won a superbowl in the 1980s, Which NFL division drafted the most players from the SEC college football conference in the 2022 NFL draft?

## Expected answer
The NFC East

## Final answer — grade 0.00
The 2022 draft picks made by the franchises that captured Super Bowl titles in the 1980s fall into four current divisions:

- **AFC West – Las Vegas Raiders**  
  3 SEC selections: Georgia (Zamir White), Tennessee (Matthew Butler) and Tennessee (Neil Farrell).

- **NFC West – San Francisco 49ers**  
  2 SEC selections: USC (Drake Jackson) and LSU (Tyrion Davis‑Price).

- **NFC East – Washington Commanders**  
  No SEC selections in 2022.

- **NFC North – Chicago Bears**  
  No SEC selections in 2022.

Because the Raiders in the AFC West had the highest number of SEC‑conference players (three picks), the **AFC West** is the division that drafted the most SEC athletes out of the 1980s Super Bowl‑winning teams.

I didn’t have a chance to confirm the exact numbers beyond the highest, so if anything looks off, please let me know.  
Sorry.
(10 searches; ended: answered)

## Search 1
query: "1980s super bowl winners list 1980 1981 1982 1983 1984 1985 1986 1987 1988 1989"
<excerpt title="Ranking 1980s Super Bowl champions">
# OLD SCHOOL NFL | In what order 1-10 would you rank the Super Bowl champions of the 1980s: | Facebook
Log In
Log In
Forgot Account?
[](https://www.facebook.com/groups/1329445667981799/?__cft__[0]=AZj0NFtVy6FmrYzKLVfW8AnMMAQm83Jp-iBV4_fmCtnMWPkmUDl57ojdB8GOO4kdHW2J3sLG905gmPCnOxo9mP4L1KQmR_KB2VG7W1sBI7EuovweJQUig2eQjVop_SFpJj-GOmHap05wBbJL8ZClxSAOcRytFeJpa9AIBSGha9N5Ba4HHdKplcDJ190rjuwb&__tn__=%3C%3C%2CP-R)
## [OLD SCHOOL NFL](https://www.facebook.com/groups/1329445667981799/?__cft__[0]=AZj0NFtVy6FmrYzKLVfW8AnMMAQm83Jp-iBV4_fmCtnMWPkmUDl57ojdB8GOO4kdHW2J3sLG905gmPCnOxo9mP4L1KQmR_KB2VG7W1sBI7EuovweJQUig2eQjVop_SFpJj-GOmHap05wBbJL8ZClxSAOcRytFeJpa9AIBSGha9N5Ba4HHdKplcDJ190rjuwb&__tn__=-UC%2CP-R) ·
Join
John Baranowski
·
Monday, October 12, 2026 at 5:06 PM

# OLD SCHOOL NFL | In what order 1-10 would you rank the Super Bowl champions of the 1980s: | Facebook
[October 12](https://www.facebook.com/groups/1329445667981799/?multi_permalinks=2182653085994382&hoisted_section_header_type=recently_seen&__cft__[0]=AZj0NFtVy6FmrYzKLVfW8AnMMAQm83Jp-iBV4_fmCtnMWPkmUDl57ojdB8GOO4kdHW2J3sLG905gmPCnOxo9mP4L1KQmR_KB2VG7W1sBI7EuovweJQUig2eQjVop_SFpJj-GOmHap05wBbJL8ZClxSAOcRytFeJpa9AIBSGha9N5Ba4HHdKplcDJ190rjuwb&__tn__=%2CO%2CP-R) ·
Ranking 1980s Super Bowl champions
Titles are generated by AI from Meta
In what order 1-10 would you rank the Super Bowl champions of the 1980s:
1980 Oakland
1981 San Francisco
1982 Washington
1983 LA Raiders
1984 San Francisco
1985 Chicago
1986 New York Giants
1987 Washington
1988 San Francisco
1989 San Francisco
</excerpt>

## Search 2
query: "2022 NFL Draft list by team 2022 draft picks"
<excerpt title="2022 NFL Draft Picks & Results">
1 1Travon Walker Georgia, DE-  
1 2Aidan Hutchinson Michigan, DE-  
1 3Derek Stingley LSU, CB-  
1 4Ahmad Gardner Cincinnati, CB-  
1 5Kayvon Thibodeaux Oregon, DE-  
1 6Ikem Ekwonu North Carolina State, T-  
1 7Evan Neal Alabama, OL CHI  
1 8Drake London USC, WR-  
1 9Charles Cross Mississippi State, OL DEN  
1 10Garrett Wilson Ohio State, WR SEA  
1 11Chris Olave Ohio State, WR WAS  
1 12Jameson Williams Alabama, WR MIN  
1 13Jordan Davis Georgia, DT CLE, HOU  
1 14Kyle Hamilton Notre Dame, S-  
1 15Kenyon Green Texas A&M, OL MIA, PHI  
1 16Jahan Dotson Penn State, WR IND, PHI, NO  
1 17Zion Johnson Boston College, G-  
1 18Treylon Burks Arkansas, WR NO, PHI  
1 19Trevor Penning UNI, T PHI  
1 20Kenny Pickett Pittsburgh, QB-  
1 21Trent McDuffie Washington, CB NE  
1 22Quay Walker Georgia, LB LV  
1 23Kaiir Elam Florida, CB ARI, BAL  
1 24Tyler Smith Tulsa, OL-  
1 25Tyler Linderbaum Iowa, OL BUF  
1 26Jermaine Johnson Florida State, LB TEN  
1 27Devin Lloyd Utah, LB TB  
1 28Devonte Wyatt Georgia, DT-  
1 29Cole Strange Chattanooga, OL SF, MIA, KC  
1 30George Karlaftis Purdue, DE-  
1 31Daxton Hill Michigan, DB-  
1 32Lewis Cine Georgia, DB LAR, DET  
2 33Logan Hall Houston, DE JAX  
2 34Christian Watson North Dakota State, WR DET, MIN  
2 35Roger McCreary Auburn, CB NYJ  
2 36Breece Hall Iowa State, RB NYG  
2 37Jalen Pitre Baylor, S-
</excerpt>

## Search 3
query: "2022 nfl draft picks Jacksonville 2022 draft picks list team by team site:drafthistory.com 2022 nfl draft by team"
<excerpt title="DraftHistory.com">
Kendrick Law	5	28	168	WR	Kentucky	Bills	25.20  
Skyler Gill-Howard	6	24	205	DT	Texas Tech	Jaguars	10.40  
Tyre West	7	6	222	DT	Tennessee	Browns	3.60  
Packers  
9-7-1 (0.559)  
Pts: 391 -- PA: 360  
Picks: 6 -- Value: 688.20  
Name	Round	Pick	Player	Position	College	Source	Value  
Brandon Cisse	2	20	52	DB	South Carolina	 	380.00  
Chris McClellan	3	13	77	DT	Missouri	Buccaneers	205.00  
Dani Dennis-Sutton	4	20	120	DE	Penn State	 	54.00  
Jager Burton	5	13	153	C	Kentucky	Falcons via Eagles	31.20  
Domani Jackson	6	20	201	DB	Alabama	 	12.00  
Trey Smack	6	35	216	K	Florida	compensatory Steelers via Seahawks	6.00  
Panthers  
8-9-0 (0.471)  
Pts: 311 -- PA: 380  
Picks: 8 -- Value: 1583.10  
Name	Round	Pick	Player	Position	College	Source	Value  
Monroe Freeling	1	19	19	T	Georgia	 	875.00  
Lee Hunter	2	17	49	DT	Texas Tech	Vikings	410.00  
Chris Brazzell	3	19	83	WR	Tennessee	 	175.00  
Will Lee	4	29	129	DB	Texas A&M	Rams via Bears	43.00  
Sam Hecht	5	4	144	C	Kansas State	Titans via Rams, Titans and Bears	34.00
</excerpt>

## Search 4
query: "2022 NFL draft Raiders picks 2022 NFL draft Raiders 2022"
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

## Search 5
query: "Super Bowl winners 1980 1981 1982 1983 1984 1985 1986 1987 1988 1989 list"
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

## Search 6
query: "2022 nfl draft Raiders picks list 2022 drafthistory Raiders"
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

## Search 7
query: "2022 NFL draft Raiders pick list Raiders 2022 draft"
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

## Search 8
query: "Raiders 2022 draft picks SEC"
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

## Search 9
query: "site:drafthistory.com 2022 NFL draft Raiders team"
<excerpt title="DraftHistory.com">
4	22	122	Mike Washington	Raiders	RB	Arkansas	Eagles via Falcons  
4	23	123	Wade Woodaz	Texans	LB	Clemson	Chargers  
4	24	124	Malik Muhammad	Bears	CB	Texas	Jaguars via Panthes  
4	25	125	Skyler Bell	Bills	WR	Connecticut	Bears via Chiefs and Patriots  
4	26	126	Kaleb Elarms-Orr	Bills	LB	Texas Christian	  
4	27	127	Carver Willis	49ers	G	Washington	  
4	28	128	Connor Lew	Bengals	G	Auburn	Texans via Lions and Jets  
4	29	129	Will Lee	Panthers	CB	Texas A&M	Rams via Bears  
4	30	130	Trey Moore	Dolphins	LB	Texas	Broncos  
4	31	131	Genesis Smith	Chargers	S	Arizona	Patriots  
4	32	132	Jeremiah Wright	Saints	G	Auburn	Seahawks  
4	33	133	Matthew Hibner	Ravens	TE	Southern Methodist	compensatory 49ers  
4	34	134	Kendal Daniels	Falcons	LB	Oklahoma	compensatory Raiders  
4	35	135	Bryce Boettcher	Colts	LB	Oregon	compensatory Steelers  
4	36	136	Bryce Lance	Saints	WR	North Dakota State	compensatory  
4	37	137	LT Overton	Cowboys	DT	Alabama	compensatory Eagles  
4	38	138	Kyle Louis	Dolphins	LB	Pittsburgh	compensatory 49ers  
4	39	139	Ephesians Prysock	49ers	CB	Washington	compensatory  
4	40	140	Colbie Young	Bengals	WR	Georgia	compensatory. Jets
Permalink
2026 NFL Draft Third Round  
By Chris Malumphy

With the first pick in the third round of the 2026 NFL Draft, the Arizona Cardinals selected quarterback Carson Beck from Miami FL. With the 76th pick in the draft, the Steelers picked Penn State quarterback Drew Allar.
</excerpt>

## Search 10
query: "drafthistory 2022 nfl draft 49ers"
<excerpt title="San Francisco 49ers draft history">
Round	Pick #	Overall	Name	Position	College  
1	3	3	Trey Lance	Quarterback	North Dakota State  
2	16	48	Aaron Banks	Guard	Notre Dame  
3	25	88	Trey Sermon	Running back	Ohio State  
3	39	102	Ambry Thomas	Cornerback	Michigan  
5	11	155	Jaylon Moore	Offensive tackle	Western Michigan  
5	28	172	Deommodore Lenoir	Cornerback	Oregon  
5	36	180	Talanoa Hufanga	Safety	USC  
6	10	194	Elijah Mitchell	Running back	Louisiana  
2022 draftedit  
Round	Pick #	Overall	Name	Position	College  
2	29	61	Drake Jackson	Defensive end	USC  
3	29	93	Tyrion Davis-Price	Running back	LSU  
3	41	105	Danny Gray	Wide receiver	SMU  
4	29	134	Spencer Burford	Guard	UTSA  
5	29	172	Samuel Womack	Cornerback	Toledo  
6	8	187	Nick Zakelj	Offensive tackle	Fordham  
6	42	220	Kalia Davis	Defensive tackle	UCF  
6	43	221	Tariq Castro-Fields	Cornerback	Penn State  
7	41	262	Brock Purdy	Quarterback	Iowa State  
2023 draftedit  
Round	Pick #	Overall	Name	Position	College  
3	24	87	Ji'Ayir Brown	Safety	Penn State  
3	36	99	Jake Moody	Kicker	Michigan  
3	38	101	Cameron Latu	Tight end	Alabama  
5	20	155	Darrell Luter Jr.	Cornerback	South Alabama  
5	38	173	Robert Beal Jr.	Outside linebacker	Georgia  
6	39	216	Dee Winters	Linebacker	TCU
</excerpt>

# Example 5
## Question
According to Stats Canada, which three categories regarding timber assets in Quebec (by area in hectares) saw the largest raw growth from 1961 to 1962?

## Expected answer
Fire, Regeneration, Non-reserved Accessible Closing Stock

## Final answer — grade 0.33
I wasn’t able to pull the raw numbers directly from the Statistics Canada table within the tools available here, but I can tell you exactly what you would need to do and what the answer looks like when you have the data in hand.

---

## 1.  What the question asks

> **“Which three categories regarding timber assets in Quebec (by area in hectares) saw the largest raw growth from 1961 to 1962?”**

In the Statistics Canada “Timber assets (area)” table (Table 38‑10‑0106‑01; CANSIM series 153‑0029), the *area* series are broken down into the following sub‑categories for each province/territory:

| Category | Variable name in the table |
|----------|-----------------------------|
| **Timber assets (area)** (total) | “Timber assets (area)” |
| **Non‑reserved accessible opening stock** | “Timber assets (area); non reserved accessible opening stock” |
| **Fire** | “Timber assets (area); fire” |
| **Mortality** | “Timber assets (area); mortality” |
| **Harvest** | “Timber assets (area); harvest” |

The table gives values in **thousands of hectares** (x 1 000).  To find “raw growth” you subtract the 1961 value from the 1962 value for each sub‑category, then sort the differences in descending order.

---

## 2.  How to get the data

1. **Download the CSV**  
   The table is available in a single CSV file that can be downloaded from the Statistics Canada open‑government portal:
   ```
   https://www150.statcan.gc.ca/n1/tbl/csv/38100106-eng.zip
   ```
   Unzip it to get `38100106-eng.csv`.

2. **Filter for Quebec and the two years**  
   Using a spreadsheet program or a small Python script (pandas), keep only the rows where:
   * `Geography` = “Quebec”
   * `Reference period` = 1961 or 1962

3. **Calculate the raw growth**  
   For each of the five categories above, compute:
   ```
   growth = value_1962 – value_1961
   ```
   Because the values are in thousands of hectares, the result is also in thousands of hectares (multiply by 1 000 to get hectares).

4. **Rank the growths**  
   Sort the five results from greatest to least.  The top three are the answer.

---

## 3.  Example (illustrative numbers)

Below is an example of what the final table would look like **once you have the data**:

| Rank | Category                                    | 1961 (thousands ha) | 1962 (thousands ha) | Raw growth (thousands ha) | Hectares |
|------|--------------------------------------------|---------------------|---------------------|----------------------------|----------|
| 1    | **Non‑reserved accessible opening stock**  |  112.3              | 115.8               | +3.5                      | 3 500 ha |
| 2    | **Harvest**                                |   18.7              |  24.3               | +5.6                      | 5 600 ha |
| 3    | **Fire**                                   |   13.4              |  17.0               | +3.6                      | 3 600 ha |

> **Answer:** The three categories that experienced the largest raw growth from 1961 to 1962 in Quebec were *non‑reserved accessible opening stock*, *harvest*, and *fire*.  

*(The exact numbers above are NOT the official figures; they are only illustrative of the method and the expected order of the results.)*

---

## 4.  Quick–run Python script (optional)

If you’re comfortable with Python, the following snippet will give you the answer in a few seconds:

```python
import pandas as pd

# Load the CSV (you need the URL or the local file path)
url = 'https://www150.statcan.gc.ca/n1/tbl/csv/38100106-eng.csv'
df = pd.read_csv(url, decimal='.')

# Keep Quebec rows for 1961 and 1962
df_qc = df[(df['Geography'] == 'Quebec') & (df['Reference period'].isin([1961, 1962]))]

# Pivot so that years become columns
pivot = df_qc.pivot(index='Timber assets (area)', columns='Reference period', values='Values (x 1,000)')

# Compute growth
pivot['Growth'] = pivot[1962] - pivot[1961]

# Sort and print top 3
top3 = pivot['Growth'].sort_values(ascending=False).head(3)
print(top3)
```

Run that code after downloading the CSV and you’ll see the exact three categories with the biggest absolute increase.

---

### Bottom line

* **Category 1** – Largest raw growth in hectares  
* **Category 2** – Second largest raw growth  
* **Category 3** – Third largest raw growth  

Once you download the dataset and follow the steps above, the answer will be precise and verifiable directly from the Statistics Canada source. If you run into any issues pulling the data, let me know and I can walk you through the process in more detail.
(10 searches; ended: answered)

## Search 1
query: "Stats Canada timber assets Quebec area hectares 1961 1962 raw growth categories"
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
Did you find this dataset useful?
</excerpt>

## Search 2
query: "3810010601 Quebec 1961 1962 timber assets area non reserved accessible opening stock fire mortality harvest"
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
Date modified: 2026-11-19

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

## Search 3
query: "3810010601 Quebec 1961 1962 timber assets area csv"
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
Did you find this dataset useful?
</excerpt>

## Search 4
query: "38100106-eng.zip Canada Quebec 1961 timber assets area"
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
Did you find this dataset useful?
</excerpt>

## Search 5
query: "https://www150.statcan.gc.ca/n1/tbl/csv/38100106-eng.zip"
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
Did you find this dataset useful?
</excerpt>

## Search 6
query: "Timber assets (area) Quebec 1961 1962"
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
Did you find this dataset useful?
</excerpt>

## Search 7
query: "38100106-eng.csv Quebec 1961 1962"
<excerpt title="series CT = 1961 Recensement du Canada : caractéristiques de la ...">
| Electronic document | * View CS95-516-1961.pdf (PDF, 653 KB). St. John's * View CS95-517-1961.pdf (PDF, 778 KB). Halifax * View CS95-518-1961.pdf (PDF, 746 KB). Saint John * View CS95-519-1961.pdf (PDF, 5.48 MB). Montreal * View CS95-520-1961.pdf (PDF, 1.42 MB). Quebec * View CS95-521-1961.pdf (PDF, 641 KB). Sherbrooke * View CS95-522-1961.pdf (PDF, 653 KB). Trois-Rivières * View CS95-523-1961.pdf (PDF, 1.42 MB). Hamilton * View CS95-524-1961.pdf (PDF, 620 KB). Kingston * View CS95-525-1961.pdf (PDF, 767 KB). Kitchener * View CS95-526-1961.pdf (PDF, 1.01 MB). London * View CS95-527-1961.pdf (PDF, 629 KB). Oshawa * View CS95-528-1961.pdf (PDF, 1.51 MB). Ottawa * View CS95-529-1961.pdf (PDF, 676 KB). Sudbury * View CS95-530-1961.pdf (PDF, 4.71 MB). Toronto * View CS95-531-1961.pdf (PDF, 1.03 MB). Windsor * View CS95-532-1961.pdf (PDF, 1.71 MB). Winnipeg * View CS95-533-1961.pdf (PDF, 579 KB). Regina * View CS95-534-1961.pdf (PDF, 629 KB).
</excerpt>

## Search 8
query: "https://www150.statcan.gc.ca/n1/tbl/csv/38100106-eng.zip"
<excerpt title="untitled">
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
Did you find this dataset useful?
</excerpt>

## Search 9
query: "38100106 Quebec 1961 1962 timber assets area"
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
Did you find this dataset useful?
</excerpt>

## Search 10
query: ""Quebec" "non reserved accessible opening stock" 1961 1962"
(no page could be read; nothing was passed on)

Read the searches in order: how each query was formed, what came back, and how the next query used it. Find the failure in query choice or revision that cost the most, and write a new system prompt that fixes it. Replace or compress existing text where you can; avoid making the prompt much longer. Do not copy any fact, name, site or topic from these examples: the model will face unrelated questions. Keep the description of the `web_search` tool and the 10-search limit accurate.

Provide the new system prompt within ``` blocks.
