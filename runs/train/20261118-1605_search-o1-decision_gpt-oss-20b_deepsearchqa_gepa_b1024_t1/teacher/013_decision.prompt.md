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
According to the UNdata website, out of India, Pakistan, Nepal, Bhutan, and Bangladesh, which countries had an increase in the percentage of their workforce being unemployed between 2015 and 2020, when rounded to one decimal place?

## Expected answer
Pakistan, Nepal, Bhutan, Bangladesh

## Grade 0.75

## Search 1 — query: "UNdata unemployment percentage India workforce 2015 2020"
### Rank 1 of 134 — 0.20 (passed on)
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
### Rank 2 of 134 — 0.10
<excerpt title="UNdata">
#### Data Available as of 31 July 2025
*   Honduras  
*   Hungary  
*   Iceland  
*   India  
*   Indonesia  
*   Iran (Islamic Republic of)  
*   Iraq  
*   Ireland  
*   Isle of Man  
*   Israel  
*   Italy  
*   Jamaica  
*   Japan  
*   Jordan  
*   Kazakhstan  
*   Kenya  
*   Kiribati  
*   Kuwait  
*   Kyrgyzstan  
*   Lao People's Democratic Republic  
*   Latvia  
*   Lebanon  
*   Lesotho  
*   Liberia  
*   Libya  
*   Liechtenstein  
*   Lithuania  
*   Luxembourg  
*   Madagascar  
*   Malawi  
*   Malaysia  
*   Maldives  
*   Mali  
*   Malta  
*   Marshall Islands  
*   Martinique  
*   Mauritania  
*   Mauritius  
*   Mayotte  
*   Mexico  
*   Micronesia (Federated States of)  
*   Monaco  
*   Mongolia  
*   Montenegro  
*   Montserrat  
*   Morocco  
*   Mozambique  
*   Myanmar  
*   Namibia  
*   Nauru  
*   Nepal  
*   Netherlands  
*   New Caledonia  
*   New Zealand  
*   Nicaragua  
*   Niger  
*   Nigeria  
*   Niue  
*   Northern Mariana Islands  
*   Norway  
*   Oman  
*   Pakistan  
*   Palau  
*   Panama  
*   Papua New Guinea  
*   Paraguay  
*   Peru  
*   Philippines  
*   Poland  
*   Portugal  
*   Puerto Rico  
*   Qatar  
*   Republic of Korea  
*   Republic of Moldova  
*   Romania  
*   Russian Federation  
*   Rwanda  
*   Réunion  
*   Saint Helena  
*   Saint Kitts and Nevis  
*   Saint Lucia  
*   Saint Pierre and Miquelon  
*   Saint Vincent and the Grenadines  
*   Samoa  
*   San Marino  
*   Sao Tome and Principe  
*   Saudi Arabia  
*   Senegal  
*   Serbia  
*   Seychelles  
*   Sierra Leone  
*   Singapore  
*   Sint Maarten (Dutch part)  
*   Slovakia  
*   Slovenia  
*   Solomon Islands  
*   Somalia  
*   South Africa  
*   South Sudan  
*   Spain
</excerpt>
### Rank 3 of 134 — 0.10
<excerpt title="UNdata">
Population
*   Population, surface area and density  
*   PDF | CSVUpdated: 2-Mar-2026  
*   International migrants and refugees  
*   PDF | CSVUpdated: 22-Dec-2025  
*   Population growth, fertility, life expectancy and mortality  
*   PDF | CSVUpdated: 2-Mar-2026  
*   Population in the capital city, urban and rural areas  
*   PDF | CSV
National accounts
*   GDP and GDP per capita  
*   PDF | CSVUpdated: 22-Dec-2025  
*   GVA by kind of economic activity  
*   PDF | CSVUpdated: 22-Dec-2025
Education
*   Education at the primary, secondary and tertiary levels  
*   PDF | CSVUpdated: 22-Dec-2025  
*   Teaching staff at the primary, secondary and tertiary levels  
*   PDF | CSVUpdated: 22-Dec-2025  
*   Public expenditure on education  
*   PDF | CSVUpdated: 22-Dec-2025
Labour market
*   Labour force and unemployment  
*   PDF | CSVUpdated: 22-Dec-2025  
*   Employment by economic activity  
*   PDF | CSVUpdated: 22-Dec-2025
Price and production indices
*   Consumer price indices  
*   PDF | CSVUpdated: 22-Dec-2025  
*   Agricultural production indices  
*   PDF | CSVUpdated: 22-Dec-2025
International merchandise trade
*   Total imports, exports and balance of trade  
*   PDF | CSVUpdated: 22-Dec-2025  
*   Major Trading Partners  
*   PDF | CSVUpdated: 22-Dec-2025
Energy
*   Energy production, trade and consumption  
*   PDF | CSVUpdated: 22-Dec-2025
Crime
*   Intentional homicides and other crimes  
*   PDF | CSVUpdated: 22-Dec-2025
Gender
*   Seats held by women in national parliament  
*   PDF | CSVUpdated: 22-Dec-2025  
*   Ratio of girls to boys in primary, secondary and tertiary levels  
*   PDF | CSVUpdated: 22-Dec-2025
</excerpt>
### Rank 4 of 134 — 0.09
<excerpt title="Indian Youth Unemployment: Factors Driving Its Deepening">
# European Economic Letters
Since February 2020, the outbreak of Covid -19 in India has worsened the labour Market situation. The national shutdown 13
ISSN 2323 -5233
Vol 1 4, Issue 3 (202 4)
http://eelet.org.uk
bottomed the Labour Participation Rate to 41.9 per cent in March 2020 due to 9 million falls in labour force. It remained
around 36 percent in next month. This sudden exit happened due to informal nature of employment. The unemployment
was estimated to 8.7 percent in the same period, highest in the last three years w hich has increased three folds in the next
month around 23.5 percent. The longevity of this seasonal event turned it into cyclical event. The unemployment rate
reduced to 11.1 per cent (12.4 per cent urban and 10.6 per cent rural) in June 2020 after unlocking the economy in
different phases in current weekly status.
According the CMIE the employment of young population below 30 years has mainly impacted during this lockdown
and faced significant job loss, signi ficantly the rural young women. Four working women out of ten working women
have lost their job during lockdown according to a survey. The agriculture sector has already lost its capacity to absorb
workforce due to reducing economic activities in the sector and this pandemic has added to this crisis. The jobless growth
has been constantl y increasing during this period too. A study by Ashwini Deshpande (2020) concluded that even post
pandemic the women’s specifically rural women’s economic recovery is far behind than men.
Conclusion: Identification of youth unemployment determinants
The review of the present status of youth unemployment is reflecting the poor participation of females in labour force.
Less job creation and increasing youth ratio in NL ET are mainly due to sluggish employment growth. Labour
Productivity growth (output per worker) is negatively impacted if the worker is not employable. The long lockdown and
halt in economic activities due to Covid -19 are reflected in the economic growth rate. Thus, the study identifies the key
determinants of youth unemployment rate such as Growth Rate, Female Labour Force Participation Rate, Labour
Productivity growth and Employment Growth.
</excerpt>
### Rank 5 of 134 — 0.09
<excerpt title="UNdata">
#### Data Available as of 31 July 2025
*   Afghanistan  
*   Albania  
*   Algeria  
*   American Samoa  
*   Andorra  
*   Angola  
*   Anguilla  
*   Antigua and Barbuda  
*   Argentina  
*   Armenia  
*   Aruba  
*   Australia  
*   Austria  
*   Azerbaijan  
*   Bahamas  
*   Bahrain  
*   Bangladesh  
*   Barbados  
*   Belarus  
*   Belgium  
*   Belize  
*   Benin  
*   Bermuda  
*   Bhutan  
*   Bolivia (Plurinational State of)  
*   Bonaire, Sint Eustatius and Saba  
*   Bosnia and Herzegovina  
*   Botswana  
*   Brazil  
*   British Virgin Islands  
*   Brunei Darussalam  
*   Bulgaria  
*   Burkina Faso  
*   Burundi  
*   Cabo Verde  
*   Cambodia  
*   Cameroon  
*   Canada  
*   Cayman Islands  
*   Central African Republic  
*   Chad  
*   Channel Islands  
*   Chile  
*   China  
*   China, Hong Kong SAR  
*   China, Macao SAR  
*   Colombia  
*   Comoros  
*   Congo  
*   Cook Islands  
*   Costa Rica  
*   Croatia  
*   Cuba  
*   Curaçao  
*   Cyprus  
*   Czechia  
*   Côte d’Ivoire  
*   Democratic People's Republic of Korea  
*   Democratic Republic of the Congo  
*   Denmark  
*   Djibouti  
*   Dominica  
*   Dominican Republic  
*   Ecuador  
*   Egypt  
*   El Salvador  
*   Equatorial Guinea  
*   Eritrea  
*   Estonia  
*   Eswatini  
*   Ethiopia  
*   Falkland Islands (Malvinas)  
*   Faroe Islands  
*   Fiji  
*   Finland  
*   France  
*   French Guiana  
*   French Polynesia  
*   Gabon  
*   Gambia  
*   Georgia  
*   Germany  
*   Ghana  
*   Gibraltar  
*   Greece  
*   Greenland  
*   Grenada  
*   Guadeloupe  
*   Guam  
*   Guatemala  
*   Guinea  
*   Guinea-Bissau  
*   Guyana  
*   Haiti  
*   Holy See
</excerpt>

## Search 2 — query: "UNdata unemployment total India 2015"
### Rank 1 of 604 — 0.84 (passed on)
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
### Rank 2 of 604 — 0.83
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
### Rank 3 of 604 — 0.31
<excerpt title="India's unemployment rate highest in 5 years in 2015-16">
# India’s unemployment rate highest in 5 years in 2015-16
## The figures could be an alarm bell for BJP-ruled government at the Centre, which has taken a series of steps such as 'Make in India' to create jobs for inclusive growth in the country.
By:PTI
2 min read _New Delhi_ Sep 29, 2016 04:30 PM IST  First published on: Sep 29, 2016 at 04:29 PM IST
*   Make us preferred source on Google  
*   Share   
*   Comments   
*   Bookmark Bookmark   
*   Print
According to the fifth annual employment-unemployment survey at all-India level, about 77 per cent of the households were reported to be having no regular wage/salaried person. (representative image)  
Unemployment rate in India has shot up to a five-year high of 5 per cent in 2015-16, with the figure significantly higher at 8.7 per cent for women as compared to 4.3 per cent for men, says a report by Labour Bureau.The figures could be an alarm bell for BJP-ruled government at the Centre, which has taken a series of steps such as ‘Make in India’ to create jobs for inclusive growth in the country.
According to the fifth annual employment-unemployment survey at all-India level, about 77 per cent of the households were reported to be having no regular wage/salaried person.It said the unemployment rate was estimated to be 5 per cent at all-India level under the UPS (Usual Principal Status)approach.Unemployment rate was 4.9 per cent in 2013-14, 4.7 per cent (2012-13), 3.8 per cent (2011-12) and 9.3 per cent(2009-10). Labour Bureau did not bring out any such report for 2014-15.
Advertisement
</excerpt>
### Rank 4 of 604 — 0.31
<excerpt title="India's unemployment rate highest in 5 years in 2015-16">
# India’s unemployment rate highest in 5 years in 2015-16 | India News - The Indian Express
skip to content
Journalism of Courage
Subscribe
[Login](javascript:ssoUI.LoginEV();)
India
1.   News  
2.   India  
3.   India News  
4.   India's unemployment rate highest in 5 years in 2015-16
This is an archive article published on September 29, 2016

# India’s unemployment rate highest in 5 years in 2015-16
## The figures could be an alarm bell for BJP-ruled government at the Centre, which has taken a series of steps such as 'Make in India' to create jobs for inclusive growth in the country.
By:PTI
2 min read _New Delhi_ Sep 29, 2016 04:30 PM IST  First published on: Sep 29, 2016 at 04:29 PM IST
*   Make us preferred source on Google  
*   Share   
*   Comments   
*   Bookmark Bookmark   
*   Print
According to the fifth annual employment-unemployment survey at all-India level, about 77 per cent of the households were reported to be having no regular wage/salaried person. (representative image)  
Unemployment rate in India has shot up to a five-year high of 5 per cent in 2015-16, with the figure significantly higher at 8.7 per cent for women as compared to 4.3 per cent for men, says a report by Labour Bureau.The figures could be an alarm bell for BJP-ruled government at the Centre, which has taken a series of steps such as ‘Make in India’ to create jobs for inclusive growth in the country.
According to the fifth annual employment-unemployment survey at all-India level, about 77 per cent of the households were reported to be having no regular wage/salaried person.It said the unemployment rate was estimated to be 5 per cent at all-India level under the UPS (Usual Principal Status)approach.Unemployment rate was 4.9 per cent in 2013-14, 4.7 per cent (2012-13), 3.8 per cent (2011-12) and 9.3 per cent(2009-10). Labour Bureau did not bring out any such report for 2014-15.
Advertisement
</excerpt>
### Rank 5 of 604 — 0.16
<excerpt title="India's unemployment rate highest in 5 years in 2015-16">
# India’s unemployment rate highest in 5 years in 2015-16
## The figures could be an alarm bell for BJP-ruled government at the Centre, which has taken a series of steps such as 'Make in India' to create jobs for inclusive growth in the country.
“In rural sector, unemployment rate was 5.1 per cent whereas in urban sector, the rate was 4.9 per cent under the UPS approach,” the report said.The figure was significantly higher among females compared to males. Female unemployment rate was estimated to be 8.7 per cent, whereas for males it was 4.3 per cent.
In urban areas, female unemployment rate was estimated to be 12.1 per cent at pan-India level compared to 3.3 per cent for males and 10.3 per cent for transgenders.The survey was conducted across all states and union territories during April 2015 to December 2015.A total sample of 1,56,563 households were covered in the survey – 88,783 households in the rural sector and 67,780 in the urban sector.
TOP STORIES RIGHT NOW
A big change on the cards for provident fund withdrawals at retirement
Behind marijuana threat row, a hotelier’s revenge against ‘extortion’ by cops
'Pretty foolish': After Republicans' midterms loss, Elon Musk regrets funding Trump's party
Topping the chart among the states and union territories was Tripura (19.7 per cent) followed by Sikkim (18.1 per cent), Lakshadweep (16.1 per cent), Andaman & Nicobar islands(12.7 per cent), Kerala (12.5 per cent) and Himachal Pradesh(10.6 per cent).
*   Make us preferred source on Google  
*   Share   
*   Comments   
*   Bookmark Bookmark   
*   Print
__ Share
__
Whatsapp
__
twitter
__
Facebook
Latest Comment
Post Comment
Read Comments
search
Edition
*   IND  
*   INT
SUBSCRIBE FOR FULL ACCESS
Install IE App for better experience
Download
Featured
*   My Express  
*   Premium  
*   UPSC
Today's E-paper
Trending Topics

# India’s unemployment rate highest in 5 years in 2015-16
## The figures could be an alarm bell for BJP-ruled government at the Centre, which has taken a series of steps such as 'Make in India' to create jobs for inclusive growth in the country.
*   Mumbai News  
*   Delhi News  
*   Chandigarh News  
*   Bangalore News  
*   Lucknow News
News
Home
India
Opinion
Politics
World
Explained
Entertainment
Bollywood
Hollywood
Television
Tamil
Telugu
Malayalam
Regional
Web Stories
Movie Review
Business
Sports
Cricket
Live Score
Chess
Football
Cities
Delhi
Mumbai
Kolkata
Pune
Chandigarh
Ahmedabad
Lucknow
Chennai
Hyderabad
Bangalore
Technology
Lifestyle
The GenZ vibe
Health
Food
Fitness
Sleep 101
Pets
Relationships
Travel
Workplace
Fashion
Art
Books
Health
Education
Top 10
Shorts
My Express
Newsletter
Multimedia
Photos
Videos
Audio
Web Stories
Follow Us
*   Facebook  
*   X  
*   Instagram  
*   LinkedIn  
*   YouTube  
*   RSS
Link Subscription
Top Categories
</excerpt>

## Search 3 — query: "UNdata unemployment total India 2015 2020"
### Rank 1 of 82 — 0.49 (passed on)
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
### Rank 2 of 82 — 0.39
<excerpt title="A Study On the Unemployment Status of India from 2000-2022">
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

## [PDF page 3]
Figure-  1  shows  that  unemployment  rate  V.  CONCLUSION:  
in India during the year 2000-22. In 2020, highest  The  biggest  problem  in  India  is  
unemployment rate was 8.00 percent in India. This  unemployment. The issue becomes worse every day.  
was a very dangerous position for Indian economy.  If a person is actively looking for job but is having  
In October 2022, the  number of total  unemployed  no luck, they are said to be unemployed. According  
were  44.85  million  and  the unemployment  rate in  to the  CMIE  study,  India’s  unemployment  rate  is  
India was  7.8 percent. In  2021  and Jan  2022, the  expected  to  be  7.80  percent.  In  India,  the  only  
unemployment rate was 5.98 and 6.56 percent. This  states  with  unemployment  rates  above  20  percent  
current  position  of  unemployment  rate  is  a  very  are Rajasthan and Haryana in 2020. India will have  
dangerous for future of Indian economy.  the highest jobless rate at 8.0 percent.
DOI: 10.35629/5252-020113011304 | Impact Factor value 7.429  | ISO 9001: 2008 Certified Journal  Page 1303

## [PDF page 4]
International Journal of Advances in Engineering and Management (IJAEM)  
Volume 2, Issue 1 Jan. 2020, pp: 1301-1304  www.ijaem.net  ISSN: 2395-5252
</excerpt>
### Rank 3 of 82 — 0.21
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
### Rank 4 of 82 — 0.21
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
### Rank 5 of 82 — 0.18
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

## Search 4 — query: "data.un.org unemployment India 2015"
### Rank 1 of 1271 — 0.40 (passed on)
<excerpt title="Human Development Report 2015">
## [PDF page 250]
128  Guatemala  15.9  22.6  2.5  2.5  51.1  2.3  8.8  0.7  19.7  71.3  8.4  4.6  3.8  1.05  
129  Tajikistan  8.4  11.4  1.9  2.4  26.7  1.2  5.1  0.3  22.0  59.4  5.2  3.7  3.9  1.05  
130  India  1,267.4  1,476.4  1.6  1.2  32.4  122.0  835.2  67.9  26.9  42.9  8.3  3.0  2.5  1.11  
131  Honduras  8.3  10.8  2.0  2.0  53.9  1.0  5.0  0.4  22.5  56.1  7.5  3.7  3.0  1.05  
132  Bhutan  0.8  0.9  2.8  1.6  37.9  0.1  0.5  0.0  26.7  39.9  7.3  3.1  2.3  1.04
</excerpt>
### Rank 2 of 1271 — 0.38
<excerpt title="Human Development Report 2015">
## [PDF page 270]
130  India  52.2  54.2  ..  47.2  ..  28.1  ..  80.8  3.6  1.4  10.7  ..  8,821  ..  
131  Honduras  60.0  62.6  50.1  35.3  33.2  44.9  8.0  53.3  3.9  ..  8.0  41.4  9,564  34.9  
132  Bhutan  70.9  72.5  ..  62.2  ..  29.1  ..  53.1  2.1  ..  9.6  ..  11,438  ..  
133  Timor-Leste  36.2  37.9  ..  50.6  ..  39.8  2.4  69.6  3.9  0.4  14.8  ..  8,156  46.3  
134  Syrian Arab Republic  38.9  43.6  ..  14.3  46.2  53.0  ..  32.9  8.4  ..  35.8  ..  18,563  ..  
134  Vanuatu  ..  70.8  ..  60.5  ..  31.1  ..  70.0  4.6  ..  10.6  ..  ..  ..  
136  Congo  66.1  70.7  ..  35.4  ..  42.2  ..  75.1 e  ..  ..  ..  ..  ..  ..
</excerpt>
### Rank 3 of 1271 — 0.38
<excerpt title="Human Development Report 2015">
## [PDF page 63]
123  Micronesia (Federated States of)  ..  ..  ..  ..  ..  ..  ..  ..  ..  ..  
124  Guyana  16.4  7.1  0.8  ..  ..  2.1 h  1 h  0.0  ..  100.0  
125  Nicaragua  14.9 f  12.1  1.7  14.2  ..  25.8  42  0.0  84  23.7  
126  Morocco  8.3  ..  ..  13.3  ..  ..  ..  0.0  98  39.8  
126  Namibia  ..  19.4  4.2  30.9  ..  0.6 j  10 j  0.0  84  98.4  
128  Guatemala  25.8 e  8.8  0.3  18.8  ..  ..  ..  0.0  84  14.1  
129  Tajikistan  10.0  0.1  0.2  19.1  ..  ..  ..  9.2  140  80.2  
130  India  11.8  2.2  0.5  55.5  ..  6.0  2,140  0.0  84  24.1  
131  Honduras  14.0 e  ..  ..  18.8  33.4  2.1  ..  0.0  84  8.4  
132  Bhutan  2.9  ..  ..  14.1  ..  ..  ..  0.0  ..  3.2
</excerpt>
### Rank 4 of 1271 — 0.38
<excerpt title="Human Development Report 2015">
## [PDF page 228]
130  India  0.428  0.496  0.586  0.597  0.600  0.604  0.609  131  6  1.49  1.67  0.97  1.48  
131  Honduras  0.507  0.557  0.610  0.612  0.607  0.604  0.606  131  –4  0.95  0.91  –0.16  0.75  
132  Bhutan  ..  ..  0.573  0.582  0.589  0.595  0.605  134  ..  ..  ..  1.39  ..  
133  Timor-Leste  ..  0.468  0.600  0.611  0.604  0.601  0.595  133  1  ..  2.51  –0.22  ..  
134  Syrian Arab Republic  0.553  0.586  0.639  0.635  0.623  0.608  0.594  130  –15  0.58  0.88  –1.82  0.30  
134  Vanuatu  ..  ..  0.589  0.590  0.590  0.592  0.594  135  1  ..  ..  0.19  ..
</excerpt>
### Rank 5 of 1271 — 0.36
<excerpt title="Human Development Report 2015">
## [PDF page 282]
122  Cabo Verde  ..  ..  ..  ..  ..  ..  ..  ..  ..  ..  ..  ..  ..  ..  
123  Micronesia (Federated States of)  ..  ..  ..  ..  ..  ..  ..  ..  ..  ..  ..  ..  ..  ..  
124  Guyana  ..  ..  ..  ..  ..  ..  ..  ..  ..  ..  ..  ..  ..  ..  
125  Nicaragua  80  54  69  56  81  80  6.3  76  67  20  38  58  68  46  
126  Morocco  34  27  76  66  58  65  5.2  40  56  5  18  38 b  45  28  
126  Namibia  71  58  43  44  85  85  4.6  ..  ..  21  46  78  64  68  
128  Guatemala  70  49  72  50  82  84  6.5  77  72  41  36  37  55  41  
129  Tajikistan  71  60  82  83  73  73  4.9  67  49  37  49  ..  51  ..  
130  India  69  58  58  52  75  79  4.4  80  47  17  34  73  54  67
</excerpt>

## Search 5 — query: "UNdata "Unemployment, total (% of total labour force)" India 2015"
(no page could be scored)

## Search 6 — query: "UNdata unemployment Pakistan 2015"
### Rank 1 of 46 — 0.28 (passed on)
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
### Rank 2 of 46 — 0.19
<excerpt title="Unemployment rate in Pakistan 1991-2025">
# Unemployment rate in Pakistan from 1991 to 2025
## Related insights
Statistics Insights
1.   Unemployment rate in Pakistan from 2010 to 2021 PAK    
2.   Youth unemployment rate in Pakistan from 1991 to 2025 PAK    
3.   Unemployment rate in Bangladesh from 1991 to 2025 BGD    
4.   Unemployment rate in Iraq from 1991 to 2025 IRQ    
5.   Unemployment rate in Uzbekistan from 1991 to 2025 UZB    
6.   Unemployment rate in Iran from 1991 to 2025 IRN    
7.   Unemployment rate in Kazakhstan from 1991 to 2025 KAZ    
8.   Unemployment rate in Kuwait from 1991 to 2025 KWT    
9.   Unemployment rate in Azerbaijan from 1991 to 2025 AZE    
10.   Unemployment rate in Afghanistan from 1991 to 2025 AFG    
11.   Unemployment rate in Nepal from 1991 to 2025 NPL    
12.   Unemployment rate in selected world regions in 2025 Worldwide    
13.   Youth unemployment rate in Iraq from 1991 to 2025 IRQ    
14.   Unemployment rate in Tajikistan from 1991 to 2025 TJK    
15.   Unemployment rate in Kyrgyzstan from 1991 to 2025 Asia    
16.   Unemployment rate in Bahrain from 1991 to 2025 BHR    
17.   Unemployment rate in Qatar from 1991 to 2025 QAT    
18.   Youth unemployment rate in Kazakhstan from 1991 to 2025 KAZ    
19.   Youth unemployment rate in Uzbekistan from 1991 to 2025 UZB    
20.   Unemployment rate in Egypt from 1991 to 2025 EGY
</excerpt>
### Rank 3 of 46 — 0.17
<excerpt title="Unemployment rate in Pakistan 1991-2025">
# Pakistan unemployment rate 2025 | Statista
![Image 2](blob:http://localhost/24fb82e8a080522e54e44c445ed36de3)Statista Connect The grounding layer for enterprise AIBook a demo
API & MCP
*   All integrations  
*   Developer docs
Explore Statista Connect  
AI assistants
*   Research  
*   Strategy & Consulting  
*   Marketing  
*   Media & PR
Explore AI assistants
Solutions
Services & solutions
Who we serve & how we help Custom research and data-driven contentTop company rankings and ratingsQuality and transformation in healthcare
By function
*   Marketing  
*   Research & Development  
*   Strategy  
*   Sales
By use case
*   Find the fact  
*   Tell the story  
*   Win the pitch  
*   Understand the market  
*   Develop your strategy
By industry
*   Academia  
*   Agencies  
*   Consultancies  
*   Consumer goods  
*   Finance  
*   Tech
Statista+ services
*   Research solutions  
*   Strategy consulting  
*   Communication services
Explore Statista+
Resources
Get started & learn
*   About Statista  
*   First steps & help center  
*   Webinar & training hub  
*   Success stories
Pricing
Plans & access
*   Individuals & Small Teams  
*   Businesses & Enterprises  
*   Academia & Government
Ctrl+K
Ctrl+K
EN
Language & Database
English
German
Log inContact sales
Menu
Advertisement
1.   Economy & Politics  
2.   International  
3.   Unemployment rate in Pakistan from 1991 to 2025

# Unemployment rate in Pakistan from 1991 to 2025
Unemployment rate in Pakistan 1991-2025
Ask AI
Last update: Jul 6, 2026
Region: Pakistan
Statista Research Department
Survey time period: 1991 to 2025
In 2025, the unemployment rate in Pakistan was approximately 5.42 percent, a slight decrease from 5.49 percent the previous year.
**Unemployment as an economic key indicator**
The unemployment rate of a country represents the share of people without a job in the country’s labor force, i.e. unemployed persons among those who are able and/or willing to work. Among other factors, it takes population growth into account, and thus increases in the labor force, as well as the age of the population. A high unemployment rate usually indicates economic troubles, with a popular example being Greece, where the unemployment rate skyrocketed from 7.76 percent in 2008 to 27.5 percent as a result of the Great Recession.
**From plowshares to keyboards**
While Pakistan’s unemployment slumped below the one percent mark in 2010, it is now on the rise again and currently standing at just over four percent. Traditionally, most Pakistanis work in agriculture however, the lion’s share of the country’s GDP is generated by services, like tourism, banking, and IT. While agriculture is still important for Pakistan’s economy, the services sector is gaining ground in the country, and more and more people are moving to urban areas from the countryside to find jobs in the cities.
* * *
REPORT_DATA_PROBLEMREPORT_PROBLEM_LINK_TEXTORCOPYRIGHT_INFRINGEMENT_LINK_TEXT
</excerpt>
### Rank 4 of 46 — 0.15
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
### Rank 5 of 46 — 0.13
<excerpt title="Unemployment rate in Pakistan 1991-2025">
# Unemployment rate in Pakistan from 1991 to 2025
Unemployment rate in Pakistan 1991-2025
Ask AI
Last update: Jul 6, 2026
Region: Pakistan
Statista Research Department
Survey time period: 1991 to 2025
In 2025, the unemployment rate in Pakistan was approximately 5.42 percent, a slight decrease from 5.49 percent the previous year.
**Unemployment as an economic key indicator**
The unemployment rate of a country represents the share of people without a job in the country’s labor force, i.e. unemployed persons among those who are able and/or willing to work. Among other factors, it takes population growth into account, and thus increases in the labor force, as well as the age of the population. A high unemployment rate usually indicates economic troubles, with a popular example being Greece, where the unemployment rate skyrocketed from 7.76 percent in 2008 to 27.5 percent as a result of the Great Recession.
**From plowshares to keyboards**
While Pakistan’s unemployment slumped below the one percent mark in 2010, it is now on the rise again and currently standing at just over four percent. Traditionally, most Pakistanis work in agriculture however, the lion’s share of the country’s GDP is generated by services, like tourism, banking, and IT. While agriculture is still important for Pakistan’s economy, the services sector is gaining ground in the country, and more and more people are moving to urban areas from the countryside to find jobs in the cities.
* * *
REPORT_DATA_PROBLEMREPORT_PROBLEM_LINK_TEXTORCOPYRIGHT_INFRINGEMENT_LINK_TEXT

# Unemployment rate in Pakistan from 1991 to 2025
## Related insights
Statistics Insights
1.   Unemployment rate in Pakistan from 2010 to 2021 PAK    
2.   Youth unemployment rate in Pakistan from 1991 to 2025 PAK    
3.   Unemployment rate in Bangladesh from 1991 to 2025 BGD    
4.   Unemployment rate in Iraq from 1991 to 2025 IRQ    
5.   Unemployment rate in Uzbekistan from 1991 to 2025 UZB    
6.   Unemployment rate in Iran from 1991 to 2025 IRN    
7.   Unemployment rate in Kazakhstan from 1991 to 2025 KAZ    
8.   Unemployment rate in Kuwait from 1991 to 2025 KWT    
9.   Unemployment rate in Azerbaijan from 1991 to 2025 AZE    
10.   Unemployment rate in Afghanistan from 1991 to 2025 AFG    
11.   Unemployment rate in Nepal from 1991 to 2025 NPL    
12.   Unemployment rate in selected world regions in 2025 Worldwide    
13.   Youth unemployment rate in Iraq from 1991 to 2025 IRQ    
14.   Unemployment rate in Tajikistan from 1991 to 2025 TJK    
15.   Unemployment rate in Kyrgyzstan from 1991 to 2025 Asia    
16.   Unemployment rate in Bahrain from 1991 to 2025 BHR    
17.   Unemployment rate in Qatar from 1991 to 2025 QAT    
18.   Youth unemployment rate in Kazakhstan from 1991 to 2025 KAZ    
19.   Youth unemployment rate in Uzbekistan from 1991 to 2025 UZB    
20.   Unemployment rate in Egypt from 1991 to 2025 EGY
</excerpt>

## Search 7 — query: "UNdata Unemployment, total (% of total labour force) India 2015""
### Rank 1 of 99 — 0.17 (passed on)
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
### Rank 2 of 99 — 0.15
<excerpt title="India - Unemployment, Total (national Estimate) - 2026 Data 2027 Forecast ...">
# India - Unemployment, Total (national Estimate) - 2026 Data 2027 Forecast 1994-2024 Historical
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

# India - Unemployment, Total (national Estimate) - 2026 Data 2027 Forecast 1994-2024 Historical
##### **Members**
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

# India - Unemployment, Total (national Estimate)2026 Data 2027 Forecast 1994-2024 Historical
## Unemployment, total (% of total labor force) (national estimate) in India was reported at 4.173 % in 2024, according to the World Bank collection of development indicators, compiled from officially recognized sources. India - Unemployment, total (national estimate) - actual values, historical data, forecasts and projections were sourced from the World Bank on November of 2026.
%
5Y10Y25YMAX
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
2005 2014 2021
World Bank
Value Chg
India - Unemployment, Total (national Estimate)
Unemployment refers to the share of the labor force that is without work but available for and seeking employment. Definitions of labor force and unemployment differ by country.
India | World Bank Development Indicators
</excerpt>
### Rank 3 of 99 — 0.14
<excerpt title="India - Unemployment, Total (national Estimate) - 2026 Data 2027 Forecast ...">
# India - Unemployment, Total (national Estimate)2026 Data 2027 Forecast 1994-2024 Historical
## Unemployment, total (% of total labor force) (national estimate) in India was reported at 4.173 % in 2024, according to the World Bank collection of development indicators, compiled from officially recognized sources. India - Unemployment, total (national estimate) - actual values, historical data, forecasts and projections were sourced from the World Bank on November of 2026.
%
5Y10Y25YMAX
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
2005 2014 2021
World Bank
Value Chg
India - Unemployment, Total (national Estimate)
Unemployment refers to the share of the labor force that is without work but available for and seeking employment. Definitions of labor force and unemployment differ by country.
India | World Bank Development Indicators

# India - Unemployment, Total (national Estimate)2026 Data 2027 Forecast 1994-2024 Historical
## Unemployment, total (% of total labor force) (national estimate) in India was reported at 4.173 % in 2024, according to the World Bank collection of development indicators, compiled from officially recognized sources. India - Unemployment, total (national estimate) - actual values, historical data, forecasts and projections were sourced from the World Bank on November of 2026.
*   [[+] Agriculture & Rural Development](https://tradingeconomics.com/india/indicators-wb-data.html?g=agriculture+%26+rural+development)

*   [[+] Aid Effectiveness](https://tradingeconomics.com/india/indicators-wb-data.html?g=aid+effectiveness)

*   [[+] Development](https://tradingeconomics.com/india/indicators-wb-data.html?g=development)

*   [[+] Economy & Growth](https://tradingeconomics.com/india/indicators-wb-data.html?g=economy+%26+growth)

*   [[+] Education](https://tradingeconomics.com/india/indicators-wb-data.html?g=education)

*   [[+] Energy & Mining](https://tradingeconomics.com/india/indicators-wb-data.html?g=energy+%26+mining)

*   [[+] External Debt](https://tradingeconomics.com/india/indicators-wb-data.html?g=external+debt)

*   [[+] Financial Sector](https://tradingeconomics.com/india/indicators-wb-data.html?g=financial+sector)

*   [[+] Health](https://tradingeconomics.com/india/indicators-wb-data.html?g=health)

*   [[+] Infrastructure](https://tradingeconomics.com/india/indicators-wb-data.html?g=infrastructure)

*   [[+] Private Sector](https://tradingeconomics.com/india/indicators-wb-data.html?g=private+sector)

*   [[+] Public Sector](https://tradingeconomics.com/india/indicators-wb-data.html?g=public+sector)

# India - Unemployment, Total (national Estimate)2026 Data 2027 Forecast 1994-2024 Historical
## Unemployment, total (% of total labor force) (national estimate) in India was reported at 4.173 % in 2024, according to the World Bank collection of development indicators, compiled from officially recognized sources. India - Unemployment, total (national estimate) - actual values, historical data, forecasts and projections were sourced from the World Bank on November of 2026.
*   [[+] Urban Development](https://tradingeconomics.com/india/indicators-wb-data.html?g=urban+development)
CalendarForecastIndicatorsNews

# India - Unemployment, Total (national Estimate)2026 Data 2027 Forecast 1994-2024 Historical
## Markets
Currency
Government Bond 10Y
Stock Market
</excerpt>
### Rank 4 of 99 — 0.10
<excerpt title="Unemployment in India">
## Government policies
### Deen Dayal Antyodaya Yojana
42.   Jump up to: 12(a) More joblessness: ILO sees India's unemployment rate rising to 3.5% in 2018, Business Standard, Somesh Jha (24 January 2019);

## Government policies
### Deen Dayal Antyodaya Yojana
(b) Full Report: World Employment Social Outlook Report, International Labour Organization (2019), ISBN978-92-2-132952-7, pages 108-109, Appendix D and Southern Asia section  
43.   ↑"India's Unemployment Rate Drops to 7.2% in October-December 2022: Ministry of Statistics and Programme Implementation Report". _Job Freaker_. 25 February 2023. Retrieved 25 February 2023.  
44.   ↑"Unemployment rate drops to 7.2% in October-December 2022: Report". _Mint_. 25 February 2023. Retrieved 25 February 2023.  
45.   ↑No easy task for India’s labour reforms, East Asia Economic Forum, Pravakar Sahoo (12 November 2014)  
46.   Jump up to: 12Alakh N. Sharma (2006). "Flexibility, employment and labour market reforms in India". _Economic and Political Weekly_. **41** (21): 2078–2085. JSTOR4418262.  
47.   ↑How India got its funk, The Economist (22 August 2013)  
48.   ↑"Unemployment Statistics". _www.labour.gov.in_. Ministry of labour and employment. Retrieved 9 November 2018.  
49.   ↑Samrat Sharma (21 June 2021). "India's job market improves as virus ebbs". _India Today_. Retrieved 14 October 2021.  
50.   ↑National Rural Employment Programme, Yojanas Info  
51.   ↑Deen Dayal Antyodaya Yojana  
52.   ↑"Economic insecurity of youths to shape India's politics: Report". _The Times of India_. 22 November 2019. ISSN0971-8257. Retrieved 9 June 2026.  

## Government policies
### Deen Dayal Antyodaya Yojana
53.   ↑"Lok Sabha Elections 2019: Here are the 4 key issues". _The Economic Times_. Retrieved 9 June 2026.  
54.   ↑"Economic insecurity of youths to shape India's politics: Report". _The Times of India_. 22 November 2019. ISSN0971-8257. Retrieved 9 June 2026.
*   Periodic Labour Force Survey (2017–2018) by Ministry of Statistics and Programme Implementation
</excerpt>
### Rank 5 of 99 — 0.09
<excerpt title="India - Unemployment, Total (national Estimate) - 2026 Data 2027 Forecast ...">
# India - Unemployment, Total (national Estimate)2026 Data 2027 Forecast 1994-2024 Historical
## Taxes
Corporate Tax Rate
Personal Income Tax Rate
Sales Tax Rate
Social Security Rate
Social Security Rate For Companies
Social Security Rate For Employees
Withholding Tax Rate

# India - Unemployment, Total (national Estimate)2026 Data 2027 Forecast 1994-2024 Historical
## Health
Hospital Beds

# India - Unemployment, Total (national Estimate)2026 Data 2027 Forecast 1994-2024 Historical
## Climate
Precipitation
Temperature
More Indicators
National Statistics
World Bank
Indicators
Homepage
Countries
Indicators
Calendar
Forecasts
Ratings
Solutions
Data Subscriptions
API Access
Excel Add-In
Developer Account
Documentation
Pricing
About Us
Customers
Careers
Investors
Advertisers
About us
Privacy
English
Español
Português
Français
Deutsch
Italiano
Polski
Indonesian
Русский
Türkçe
العربية
简体中文
日本語
한국어
Copyright ©2026 TRADING ECONOMICS
All Rights Reserved
×
</excerpt>

## Search 8 — query: "data.un.org Unemployment total India 2015"
### Rank 1 of 1128 — 0.07 (passed on)
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
### Rank 2 of 1128 — 0.07
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
### Rank 3 of 1128 — 0.07
<excerpt title="India - unemployment reasons among post-graduates 2015">
# Distribution of unemployment among post-graduates across rural and urban India in 2015, by reason
## Related insights
Statistics Insights
Share of unemployed graduates across rural and urban India in 2015, by reason Bar chart with 3 data series. View as data table, Chart The chart has 1 X axis displaying categories. The chart has 1 Y axis displaying values. Data ranges from 12.33 to 61.91. Personal/family issues Others Non-availability of adequate remuneration End of interactive chart. * * * Visit the full version Preview
Distribution of rural and urban underemployment in India in 2015 Bar chart with 3 data series. View as data table, Chart The chart has 1 X axis displaying categories. The chart has 1 Y axis displaying values. Data ranges from 0.56 to 58.93. Did not get any work Worked for 1-5 months Worked for 6-11 months End of interactive chart. * * * Visit the full version Preview
Rate of unemployment in rural and urban India in financial year 2025, by gender Bar chart with 2 data series. View as data table, Chart The chart has 1 X axis displaying categories. The chart has 1 Y axis displaying values. Data ranges from 2.1 to 6.4. Rural Urban 0 2 4 6 8 10 End of interactive chart. * * * Visit the full version Preview
Rate of unemployment in urban India in financial year 2025, by state and union territory Bar chart with 3 bars. View as data table, Chart The chart has 1 X axis displaying categories. The chart has 1 Y axis displaying values. Data ranges from 12 to 15.6. Arunachal Pradesh Nagaland Andaman and Nicobar Islands 0 5 10 15 20 25 End of interactive chart. * * * Visit the full version Preview
</excerpt>
### Rank 4 of 1128 — 0.07
<excerpt title="India - unemployment reasons among post-graduates 2015">
# Distribution of unemployment among post-graduates across rural and urban India in 2015, by reason
## About Your Privacy
#### Personalised advertising and content, advertising and content measurement, audience research and services development 842 partners can use this purpose
- [x] Switch Label     
Information regarding which content is presented to you and how you interact with it can be used to determine whether the (non-advertising) content e.g. reached its intended audience and matched your interests. For instance, whether you read an article, watch a video, listen to a podcast or look at a product description, how long you spent on this service and the web pages you visit etc. This is very helpful to understand the relevance of (non-advertising) content that is shown to you.
View Illustrations
*   ##### Understand audiences through statistics or combinations of data from different sources 489 partners can use this purpose
- [x] Switch Label     
Reports can be generated based on the combination of data sets (like user profiles, statistics, market research, analytics data) regarding your interactions and those of other users with advertising or (non-advertising) content to identify common characteristics (for instance, to determine which target audiences are more receptive to an ad campaign or to certain contents).
View Illustrations
*   ##### Develop and improve services 576 partners can use this purpose
- [x] Switch Label     
Information about your activity on this service, such as your interaction with ads or content, can be very helpful to improve products and services and to build new products and services based on user interactions, the type of audience, etc. This specific purpose does not include the development or improvement of user profiles and identifiers.
View Illustrations
*   ##### Use limited data to select content 149 partners can use this purpose
- [x] Switch Label     
Content presented to you on this service can be based on limited data, such as the website or app you are using, your non-precise location, your device type, or which content you are (or have been) interacting with (for example, to limit the number of times a video or an article is presented to you).
View Illustrations
List of IAB Vendors

# Distribution of unemployment among post-graduates across rural and urban India in 2015, by reason
## About Your Privacy
#### Use precise geolocation data 248 partners can use this special feature
- [x] Use precise geolocation data
With your acceptance, your precise location (within a radius of less than 500 metres) may be used in support of the purposes explained in this notice.
List of IAB Vendors

# Distribution of unemployment among post-graduates across rural and urban India in 2015, by reason
## About Your Privacy
#### Identify devices based on information actively requested 137 partners can use this special feature
- [x] Identify devices based on information actively requested
With your acceptance, certain characteristics specific to your device might be requested and used to distinguish it from other devices (such as the installed fonts or plugins, the resolution of your screen) in support of the purposes explained in this notice.
List of IAB Vendors

# Distribution of unemployment among post-graduates across rural and urban India in 2015, by reason
## About Your Privacy
#### Ensure security, prevent and detect fraud, and fix errors 547 partners can use this special purpose
Always Active
Your data can be used to monitor for and prevent unusual and possibly fraudulent activity (for example, regarding advertising, ad clicks by bots), and ensure systems and processes work properly and securely. It can also be used to correct any problems you, the publisher or the advertiser may encounter in the delivery of content and ads and in your interaction with them.
List of IAB Vendors|View Illustrations
</excerpt>
### Rank 5 of 1128 — 0.07
<excerpt title="India - unemployment reasons among post-graduates 2015">
# Distribution of unemployment among post-graduates across rural and urban India in 2015, by reason
## About Your Privacy
#### Personalised advertising and content, advertising and content measurement, audience research and services development 842 partners can use this purpose
- [x] Switch Label     
Information regarding which content is presented to you and how you interact with it can be used to determine whether the (non-advertising) content e.g. reached its intended audience and matched your interests. For instance, whether you read an article, watch a video, listen to a podcast or look at a product description, how long you spent on this service and the web pages you visit etc. This is very helpful to understand the relevance of (non-advertising) content that is shown to you.
View Illustrations
*   ##### Understand audiences through statistics or combinations of data from different sources 489 partners can use this purpose
- [x] Switch Label     
Reports can be generated based on the combination of data sets (like user profiles, statistics, market research, analytics data) regarding your interactions and those of other users with advertising or (non-advertising) content to identify common characteristics (for instance, to determine which target audiences are more receptive to an ad campaign or to certain contents).
View Illustrations
*   ##### Develop and improve services 576 partners can use this purpose
- [x] Switch Label     
Information about your activity on this service, such as your interaction with ads or content, can be very helpful to improve products and services and to build new products and services based on user interactions, the type of audience, etc. This specific purpose does not include the development or improvement of user profiles and identifiers.
View Illustrations
*   ##### Use limited data to select content 149 partners can use this purpose
- [x] Switch Label     
Content presented to you on this service can be based on limited data, such as the website or app you are using, your non-precise location, your device type, or which content you are (or have been) interacting with (for example, to limit the number of times a video or an article is presented to you).
View Illustrations
List of IAB Vendors

# Distribution of unemployment among post-graduates across rural and urban India in 2015, by reason
## About Your Privacy
#### Use precise geolocation data 248 partners can use this special feature
- [x] Use precise geolocation data
With your acceptance, your precise location (within a radius of less than 500 metres) may be used in support of the purposes explained in this notice.
List of IAB Vendors

# Distribution of unemployment among post-graduates across rural and urban India in 2015, by reason
## About Your Privacy
#### Identify devices based on information actively requested 137 partners can use this special feature
- [x] Identify devices based on information actively requested
With your acceptance, certain characteristics specific to your device might be requested and used to distinguish it from other devices (such as the installed fonts or plugins, the resolution of your screen) in support of the purposes explained in this notice.
List of IAB Vendors

# Distribution of unemployment among post-graduates across rural and urban India in 2015, by reason
## About Your Privacy
#### Ensure security, prevent and detect fraud, and fix errors 547 partners can use this special purpose
Always Active
Your data can be used to monitor for and prevent unusual and possibly fraudulent activity (for example, regarding advertising, ad clicks by bots), and ensure systems and processes work properly and securely. It can also be used to correct any problems you, the publisher or the advertiser may encounter in the delivery of content and ads and in your interaction with them.
List of IAB Vendors|View Illustrations
</excerpt>

## Search 9 — query: "UNdata Unemployment, total (% of total labour force) Nepal 2015"
### Rank 1 of 410 — 0.34 (passed on)
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
### Rank 2 of 410 — 0.31
<excerpt title="Labour Force and Economic Activities in Nepal.pdf">
## [PDF page 11]
cGo dxTjk"0f{ sf/0fx¿df 3/wGbf -@*=$Ü_ / j[4fj:yf -!!=*Ü_ /x]sf 5g\ .  
/f]huf/Lsf] l:ylt -Status in employment_  
/fli6«o hgu0fgf @)&* cg';f/, /f]huf/sf] l:ylt rf/ k|d'v >]0fLx¿df juL{s[t ul/Psf] 5 h;df  
$@ nfv -@*=^Ü_, c¿sf] sfd ug]{, @ nfv -!=$Ü_ /f]huf/bftf, *@ nfv -%%=#Ü_ cfˆg} sfd ug]{  
/  @!  nfv  -!$=%Ü_  kl/jf/nfO{  ;3fpg]x¿  b]lvPsf  5g\  .  cGt/f{li6«o  >d  ;+u7gn]  …;fdflhs  
b[li6sf]0faf6 c;'/lIft /f]huf/LÚ nfO{ cfˆg} sfd ug]{ jf kl/jf/nfO{ ;3fpg] ;d"xnfO{ kl/eflift u/]sf]  
5 . hgu0fgf @)&* n] ! s/f]8 $ nfv -^(=(Ü_ >dzlQmnfO{ c;'/lIft /f]huf/Ldf ;+nUg b]vfPsf]  
5 h;df $( nfv k'?if -^#=@Ü_ / %$ nfv dlxnf -^#=@Ü_ /x]sf 5g\ .  
k|b]z:t/df t'ngf ubf{ s0ff{nLdf c;'/lIft /f]huf/L pRrtd -*$Ü_ 5 . u|fdL0f If]qdf c;'/lIft  

## [PDF page 11]
/f]huf/Lsf] cg'kft *$=* k|ltzt 5 . lzlIft JolQmx¿tkm{ c;'/lIft /f]huf/Lsf] cg'kft &^=% k|ltzt  
5 eg] clzlIft ju{df of] cg'kft &#=% k|ltzt /x]sf] 5 .
iv

## [PDF page 12]
k];f / cf}Bf]lus If]q -Occupation and industry_  
;du| cy{tGqnfO{ ljleGg cf}Bf]lus If]qx¿leq v08Ls/0f u/]/ ljZn]if0f ug]{ ul/G5 . o;/L x]bf{ s'n
</excerpt>
### Rank 3 of 410 — 0.31
<excerpt title="Labour Force and Economic Activities in Nepal.pdf">
## [PDF page 11]
ljZn]if0f ubf{ ljkGg ju{df kg]{ kl/jf/sf JolQmx¿df >dzlQm ;xeflutfb/ ;a}eGbf pRr -&)=!Ü_  
5 hxfF o;sf] dfg k'?iftkm{ &$=! k|ltzt / dlxnftkm{ ^^=% k|ltzt /x]sf] b]lvG5 .  
cS;/ a]/f]huf/L -Usual unemployment)  
g]kfndf !) jif{ jf ;f]eGbf dflysf] pd]/ ;d"xdf cS;/ a]/f]huf/ JolQmx¿sf] ;ª\Vof &,^&,^%*  
/x]sf] 5 h;df $,)),(@* k'?if / #,^^,&#) dlxnf /x]sf 5g\ . cfly{s ¿kn] ;lqmo hg;ª\Vofleq  
!%–^$ jif{sf] pd]/ ;d"xnfO{ ;d]6\bf cS;/ a]/f]huf/ JolQmx¿sf] ;ª\Vof &,!#,$&( /x]sf] 5 . ;du|  
a]/f]huf/Lb/ $=( k|ltzt 5 t/ o;nfO{ !%–^$ jif{ pd]/ ;d"xsf x]bf{ %=! k|ltzt /x]sf] 5 . kl5Nnf]  
!@ dlxgfdf !) jif{ / ;f]eGbf dflysf] hg;ª\Vofn] slt cjlw cfly{s sfd u/]sf] lyof] eGg] cfwf/df  
x]bf{ pNn]vgLo cyf{t\  $^ nfv  -@(=^Ü_ hg;ª\Vofn] ^ dlxgfeGbf sd ;do dfq sfd u/]sf]  
kfOof] .
</excerpt>
### Rank 4 of 410 — 0.30
<excerpt title="Labour Force and Economic Activities in Nepal.pdf">
## [PDF page 12]
u/]sf] 5 . ;x/L If]qdf s]jn @^=% k|ltzt dlxnf cS;/ /f]huf/ 5g\ eg] u|fdL0f If]qdf $%=! k|ltzt  
dlxnf cS;/ /f]huf/ 5g\ . cS;/ /f]huf/ hg;ª\Vofsf] pRrtd cg'kft -%(=^Ü_ pRr lzIff k|fKt  
;d"xdf / Go"gtd cg'kft -#*=%Ü_ cfwf/e"t lzIff k|fKt JolQmx¿df b]lvPsf] 5 .  
afnaflnsf / Ho]]i7 gful/ssf] cfly{s lqmofsnfk  
afnaflnsf / cfly{s lqmofsnfk  
g]kfnsf] sfg'gn] !* jif{eGbf d'lgsf pd]/sf ;a}nfO{ afnaflnsf dfg]sf] 5 . hgu0fgfdf !) jif{ /  
;f]eGbf dflysf] hg;ª\Vofaf6 dfq cfly{s sfd;DaGwL ljj/0f ;+sng ul/Psf] 5 . o; cy{df !)  
b]lv !& jif{;Ddsf afnaflnsfsf] >dzlQm ;xeflutfb/  -LFPR_ #@=! k|ltzt 5 -k'?iftkm{ #!=(Ü  
/ dlxnftkm{ #@=@Ü_ . s0ff{nL k|b]zdf afnaflnsfsf] LFPR ;a}eGbf pRr -#(=%Ü_ / dw];df ;a}eGbf  
sd -@^=(Ü_ 5 . o;}u/L, ef}uf]lns If]qcg';f/ x]bf{ lxdfndf LFPR ;a}eGbf pRr -#(=!Ü_ b]lvG5 .  

## [PDF page 12]
;x/L / u|fdL0f cfwf/df x]bf{ of] u|fdL0f If]qdf $)=# k|ltzt /x]sf] 5 .
v
</excerpt>
### Rank 5 of 410 — 0.29
<excerpt title="Labour Force and Economic Activities in Nepal.pdf">
## [PDF page 10]
dw]z k|b]zdf b]lvG5 -n}lËs ;dtf ;"rsM &)=&_, eg] ;a}eGbf sd s0ff{nL k|b]zdf -n}lËs ;dtf  
;"rsM (%=^_ /x]sf] 5 .  
;x/L  /  u|fdL0f  If]qdf  >dzlQm  ;xeflutfb/df  :ki6  cGt/  b]lvG5  .  u|fdL0f  If]qdf  >d  zlQm  
;xeflutfb/ ;a}eGbf pRr -&$=)Ü_ /x]sf] 5, To;kl5 cw{;x/L If]qdf -^#=^Ü_ / ;x/L If]qdf  
;a}eGbf sd -%*=)Ü_ b]lvPsf] 5 . n}lËs b[li6sf]0faf6 >dzlQm ;xeflutfb/sf] ;a}eGbf w]/} ljifdtf  
;x/L If]qdf ljBdfg /x]sf] b]lvG5 .  
lhNnf:t/df klg >dzlQm ;xeflutfb/df Jofks leGgtf b]lvG5 . o; ;"rssf] dfg ;a}eGbf pRr  
-(!=#Ü_ ;+v'jf;efdf /x]sf] 5 eg] ;a}eGbf sd -%@=*Ü_ dxf]Q/L lhNnfdf b]lvPsf] 5 . To;}u/L  
!%–^$ jif{ pd]/ ;d"xdf kg]{ hg;ª\Vofsf] >dzlQm ;xeflutfb/ &#=@ k|ltzt /x]sf] 5 -k'?iftkm{M  

## [PDF page 10]
*)=!Ü / dlxnftkm{ ^^=(Ü_ /x]sf] 5 . sfg'gtM :jLsfo{ geP tfklg !)–!$ jif{ pd]/ ;d"xsf  
afnaflnsfsf nflu >dzlQm ;xeflutfb/ @*=&Ü /x]sf] 5 . cfly{s ¿kn] ^% jif{ / ;f]eGbf dflysf]  
hg;ª\Vof klg ;lqmo b]lvG5 / of] pd]/ ;d"xdf >dzlQm ;xeflutfb/ $%=( k|ltzt /x]sf] 5  
-k'?iftkm{ %#=$Ü / dlxnftkm{ #*=$Ü_ .  
z}lIfs of]Uotfcg';f/ >dzlQm ;xeflutftb/ t'ngf ubf{ ;fdfGo cGt/ b]lvP tfklg pRrtd lzlIft  
hg;ª\Vofs} >dzlQm ;xeflutfb/ clwstd -&%=&Ü_ -k'?iftkm{ *!=@Ü / dlxnftkm{ ^&=(Ü_ /x]sf]  
5 . To;}u/L, >dzlQm ;xeflutfb/nfO{ 3/kl/jf/x¿sf] ;DkGgtfsf] tx -wealth index_ cg';f/  
iii
</excerpt>

## Search 10 — query: "UNdata India Unemployment, total (%) 2015"
### Rank 1 of 81 — 0.10 (passed on)
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
### Rank 2 of 81 — 0.10
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

# India Unemployment Rate
## The Indian unemployment rate tell to 4.9% in October of 2026 from 5.0% in the previous month, the lowest since February, and below the median market consensus that it would rise to 5.1%. The improvement was evidence of resilience in the Indian labor market as soaring energy prices and a weak rupee elevated consumer inflation to a three-year high in the period, driving the Reserve Bank of India to raise its benchmark policy rate. The urban unemployment rate fell to 6.7% form 6.9%, the first drop since May, while the rural unemployment rate was unchanged at 4.2%. The reduction in the unemployment rate took place in tandem with an increase in the labor force participation rate (55.7% vs 55.5% in September), the highest since February. source: Ministry of Statistics and Programme Implementation (MOSPI)
## Unemployment Rate in India decreased to 4.90 percent in October from 5 percent in September of 2026. Unemployment Rate in India averaged 7.33 percent from 2018 until 2026, reaching an all time high of 20.80 percent in June of 2020 and a record low of 4.70 percent in November of 2025. This page provides - India Unemployment Rate - actual values, historical data, forecast, chart, statistics, economic calendar and news. India Unemployment Rate - data, historical chart, forecasts and calendar of releases - was last updated on November of 2026.
</excerpt>
### Rank 3 of 81 — 0.08
<excerpt title="India Unemployment Rate">
# India Unemployment Rate
## The Indian unemployment rate tell to 4.9% in October of 2026 from 5.0% in the previous month, the lowest since February, and below the median market consensus that it would rise to 5.1%. The improvement was evidence of resilience in the Indian labor market as soaring energy prices and a weak rupee elevated consumer inflation to a three-year high in the period, driving the Reserve Bank of India to raise its benchmark policy rate. The urban unemployment rate fell to 6.7% form 6.9%, the first drop since May, while the rural unemployment rate was unchanged at 4.2%. The reduction in the unemployment rate took place in tandem with an increase in the labor force participation rate (55.7% vs 55.5% in September), the highest since February. source: Ministry of Statistics and Programme Implementation (MOSPI)
## Unemployment Rate in India decreased to 4.90 percent in October from 5 percent in September of 2026. Unemployment Rate in India averaged 7.33 percent from 2018 until 2026, reaching an all time high of 20.80 percent in June of 2020 and a record low of 4.70 percent in November of 2025. This page provides - India Unemployment Rate - actual values, historical data, forecast, chart, statistics, economic calendar and news. India Unemployment Rate - data, historical chart, forecasts and calendar of releases - was last updated on November of 2026.

# India Unemployment Rate
### Unemployment Rate in India decreased to 4.90 percent in October from 5 percent in September of 2026. Unemployment Rate in India is expected to be 4.90 percent by the end of this quarter, according to Trading Economics global macro models and analysts expectations. In the long-term, the India Unemployment Rate is projected to trend around 5.10 percent in 2027 and 5.00 percent in 2028, according to our econometric models.
| Calendar | GMT | Reference | Actual | Previous | Consensus | TEForecast |  
| --- | --- | --- | --- | --- | --- | --- |  
| 2026-10-15 | 10:30 AM | Unemployment Rate | Sep | 5% | 5% | 5.2% | 5.20% |  
| 2026-11-16 | 10:30 AM | Unemployment Rate | Oct | 4.9% | 5% | 5.1% | 5.1% |  
| 2026-12-15 | 10:30 AM | Unemployment Rate | Nov |  | 4.9% |  | 4.9% |
</excerpt>
### Rank 4 of 81 — 0.08
<excerpt title="Unemployment rate in India from 1991 to 2025">
# India unemployment rate 2025 | Statista
![Image 2](blob:http://localhost/24fb82e8a080522e54e44c445ed36de3)Statista Connect The grounding layer for enterprise AIBook a demo
API & MCP
*   All integrations  
*   Developer docs
Explore Statista Connect  
AI assistants
*   Research  
*   Strategy & Consulting  
*   Marketing  
*   Media & PR
Explore AI assistants
Solutions
Services & solutions
Who we serve & how we help Custom research and data-driven contentTop company rankings and ratingsQuality and transformation in healthcare
By function
*   Marketing  
*   Research & Development  
*   Strategy  
*   Sales
By use case
*   Find the fact  
*   Tell the story  
*   Win the pitch  
*   Understand the market  
*   Develop your strategy
By industry
*   Academia  
*   Agencies  
*   Consultancies  
*   Consumer goods  
*   Finance  
*   Tech
Statista+ services
*   Research solutions  
*   Strategy consulting  
*   Communication services
Explore Statista+
Resources
Get started & learn
*   About Statista  
*   First steps & help center  
*   Webinar & training hub  
*   Success stories
Pricing
Plans & access
*   Individuals & Small Teams  
*   Businesses & Enterprises  
*   Academia & Government
Ctrl+K
Ctrl+K
EN
Language & Database
English
German
Log inContact sales
Menu
Advertisement
1.   Economy & Politics  
2.   International  
3.   Unemployment rate in India from 1991 to 2025

# Unemployment rate in India from 1991 to 2025
Unemployment rate in India 1991-2025
Ask AI
Last update: Feb 25, 2026
Region: India
Statista Research Department
Survey time period: 1999 to 2024
India's annual unemployment rate in 2025 was estimated to be 4.22 percent in 2025, compared with 4.17 percent in the previous year.
**India's economy in comparison to other BRIC states**
India possesses one of the fastest-growing economies in the world and as a result, India is recognized as one of the G-20 major economies as well as a member of the BRIC countries, an association that is made up of rapidly growing economies. As well as India, three other countries, namely Brazil, Russia and China, are BRIC members. India’s manufacturing industry plays a large part in the development of its economy; however its services industry is the most significant economical factor. The majority of the population of India works in this sector. India’s notable economic boost can be attributed to significant gains over the past decade in regards to the efficiency of the production of goods as well as maintaining relatively low debt, particularly when compared to the total amount earned from goods and services produced throughout the years.
When considering individual development as a country, India progressed significantly over the years. However, in comparison to the other emerging countries in the BRIC group, India’s progress was rather minimal. While China experienced the most apparent growth, India’s efficiency and productivity remained somewhat stagnant over the course of 3 or 4 years. India also reported a rather large trade deficit over the past decade, implying that its total imports exceeded its total amount of exports, essentially forcing the country to borrow money in order to finance the nation. Most economists consider trade deficits a negative factor, especially in the long run and for developing or emerging countries.
* * *
REPORT_DATA_PROBLEMREPORT_PROBLEM_LINK_TEXTORCOPYRIGHT_INFRINGEMENT_LINK_TEXT
</excerpt>
### Rank 5 of 81 — 0.07
<excerpt title="Unemployment in India">
## Government policies
### Deen Dayal Antyodaya Yojana
42.   Jump up to: 12(a) More joblessness: ILO sees India's unemployment rate rising to 3.5% in 2018, Business Standard, Somesh Jha (24 January 2019);

## Government policies
### Deen Dayal Antyodaya Yojana
(b) Full Report: World Employment Social Outlook Report, International Labour Organization (2019), ISBN978-92-2-132952-7, pages 108-109, Appendix D and Southern Asia section  
43.   ↑"India's Unemployment Rate Drops to 7.2% in October-December 2022: Ministry of Statistics and Programme Implementation Report". _Job Freaker_. 25 February 2023. Retrieved 25 February 2023.  
44.   ↑"Unemployment rate drops to 7.2% in October-December 2022: Report". _Mint_. 25 February 2023. Retrieved 25 February 2023.  
45.   ↑No easy task for India’s labour reforms, East Asia Economic Forum, Pravakar Sahoo (12 November 2014)  
46.   Jump up to: 12Alakh N. Sharma (2006). "Flexibility, employment and labour market reforms in India". _Economic and Political Weekly_. **41** (21): 2078–2085. JSTOR4418262.  
47.   ↑How India got its funk, The Economist (22 August 2013)  
48.   ↑"Unemployment Statistics". _www.labour.gov.in_. Ministry of labour and employment. Retrieved 9 November 2018.  
49.   ↑Samrat Sharma (21 June 2021). "India's job market improves as virus ebbs". _India Today_. Retrieved 14 October 2021.  
50.   ↑National Rural Employment Programme, Yojanas Info  
51.   ↑Deen Dayal Antyodaya Yojana  
52.   ↑"Economic insecurity of youths to shape India's politics: Report". _The Times of India_. 22 November 2019. ISSN0971-8257. Retrieved 9 June 2026.  

## Government policies
### Deen Dayal Antyodaya Yojana
53.   ↑"Lok Sabha Elections 2019: Here are the 4 key issues". _The Economic Times_. Retrieved 9 June 2026.  
54.   ↑"Economic insecurity of youths to shape India's politics: Report". _The Times of India_. 22 November 2019. ISSN0971-8257. Retrieved 9 June 2026.
*   Periodic Labour Force Survey (2017–2018) by Ministry of Statistics and Programme Implementation
</excerpt>

# Example 2
## Question
Only counting players drafted by teams who won a superbowl in the 1980s, Which NFL division drafted the most players from the SEC college football conference in the 2022 NFL draft?

## Expected answer
The NFC East

## Grade 0.00

## Search 1 — query: "1980s super bowl winners list 1980 1981 1982 1983 1984 1985 1986 1987 1988 1989"
### Rank 1 of 121 — 0.82 (passed on)
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
### Rank 2 of 121 — 0.81
<excerpt title="Ranking 1980s Super Bowl champions">
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

# OLD SCHOOL NFL | In what order 1-10 would you rank the Super Bowl champions of the 1980s: | Facebook
[](https://www.facebook.com/photo/?fbid=28588529127423613&set=gm.2182653085994382&idorvanity=1329445667981799&__cft__[0]=AZj0NFtVy6FmrYzKLVfW8AnMMAQm83Jp-iBV4_fmCtnMWPkmUDl57ojdB8GOO4kdHW2J3sLG905gmPCnOxo9mP4L1KQmR_KB2VG7W1sBI7EuovweJQUig2eQjVop_SFpJj-GOmHap05wBbJL8ZClxSAOcRytFeJpa9AIBSGha9N5Ba4HHdKplcDJ190rjuwb&__tn__=EH-R)
![Image 3](blob:http://localhost/85d8b181a20aeb64a3afc2f1c39d2480)
![Image 4](blob:http://localhost/2b45e6f1a2ae097354c0b291152873d5)
All reactions:
81
38 comments
3 shares
Like
Comment
Share
Most relevant
Dk Jacob
85 bears
had something that comes
around only once in a lifetime …
See more
</excerpt>
### Rank 3 of 121 — 0.79
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
### Rank 4 of 121 — 0.75
<excerpt title="Super Bowl History (NFL)">
## Super Bowl Results
| IX  | January 12, 1975(1974) |  PITTSBURGH STEELERS | 16-6 |  Minnesota Vikings |  Tulane Stadium(3) New Orleans, LA(3) |  
| X  | January 18, 1976(1975) |  PITTSBURGH STEELERS (2) | 21-17 |  Dallas Cowboys |  Miami Orange Bowl(4) Miami,FL(4) |  
| XI  | January 9, 1977(1976) |  OAKLAND RAIDERS | 32-14 |  Minnesota Vikings |  Rose Bowl(1) Pasadena,CA(1) |  
| XII  | January 15, 1978(1977) |  Dallas Cowboys (3) | 27-10 |  DENVER BRONCOS |  Louisiana Superdome(1) New Orleans, LA(4) |  
| XIII  | January 21, 1979(1978) |  PITTSBURGH STEELERS (3) | 35-31 |  Dallas Cowboys |  Miami Orange Bowl(5) Miami,FL(5) |  
| XIV  | January 20, 1980(1979) |  PITTSBURGH STEELERS (4) | 31-19 |  LOS ANGELES RAMS |  Rose Bowl(2) Pasadena,CA(2) |  
| XV  | January 25, 1981(1980) |  OAKLAND RAIDERS (2) | 27-10 |  Philadelphia Eagles |  Louisiana Superdome(2) New Orleans, LA(5) |  
| XVI  | January 24, 1982(1981) |  San Francisco 49erS | 26-21 |  CINCINNATI BENGALS |  Pontiac Silverdome Pontiac,MI |  

## Super Bowl Results
| XVII  | January 30, 1983(1982) |  Washington Redskins | 27-17 |  MIAMI DOLPHINS |  Rose Bowl(3) Pasadena,CA(3) |  
| XVIII  | January 22, 1984(1983) |  Los Angeles Raiders (3) | 38-9 |  Washington Redskins |  Tampa Stadium(1) Tampa,FL(1) |  
| XIX  | January 20, 1985(1984) |  San Francisco 49erS (2) | 38-16 |  MIAMI DOLPHINS |  Stanford Stadium(4) Stanford,CA (1) |  
| XX  | January 26, 1986(1985) |  Chicago Bears | 46-10 |  NEW ENGLAND PATRIOTS |  Louisiana Superdome(3) New Orleans, LA(6) |  
| XXI  | January 25, 1987(1986) |  New York Giants | 39-20 |  DENVER BRONCOS |  Rose Bowl(4) Pasadena,CA(4) |  
| XXII  | January 31, 1988(1987) |  Washington Redskins (2) | 42-10 |  DENVER BRONCOS |  Jack Murphy Stadium(1) San Diego,CA(1) |  
| XXIII  | January 22, 1989(1988) |  SAN FRANCISCO 49ERS (3) | 20-16 |  CINCINNATI BENGALS |  Joe Robbie Stadium(1) Miami Gardens,FL (6) |  
| XXIV  | January 28, 1990(1989) |  SAN FRANCISCO 49ERS (4) | 55-10 |  DENVER BRONCOS |  Louisiana Superdome(4) New Orleans, LA(7) |
</excerpt>
### Rank 5 of 121 — 0.75
<excerpt title="Super Bowl History (NFL)">
## Super Bowl Results
| XVII  | January 30, 1983(1982) |  Washington Redskins | 27-17 |  MIAMI DOLPHINS |  Rose Bowl(3) Pasadena,CA(3) |  
| XVIII  | January 22, 1984(1983) |  Los Angeles Raiders (3) | 38-9 |  Washington Redskins |  Tampa Stadium(1) Tampa,FL(1) |  
| XIX  | January 20, 1985(1984) |  San Francisco 49erS (2) | 38-16 |  MIAMI DOLPHINS |  Stanford Stadium(4) Stanford,CA (1) |  
| XX  | January 26, 1986(1985) |  Chicago Bears | 46-10 |  NEW ENGLAND PATRIOTS |  Louisiana Superdome(3) New Orleans, LA(6) |  
| XXI  | January 25, 1987(1986) |  New York Giants | 39-20 |  DENVER BRONCOS |  Rose Bowl(4) Pasadena,CA(4) |  
| XXII  | January 31, 1988(1987) |  Washington Redskins (2) | 42-10 |  DENVER BRONCOS |  Jack Murphy Stadium(1) San Diego,CA(1) |  
| XXIII  | January 22, 1989(1988) |  SAN FRANCISCO 49ERS (3) | 20-16 |  CINCINNATI BENGALS |  Joe Robbie Stadium(1) Miami Gardens,FL (6) |  
| XXIV  | January 28, 1990(1989) |  SAN FRANCISCO 49ERS (4) | 55-10 |  DENVER BRONCOS |  Louisiana Superdome(4) New Orleans, LA(7) |
</excerpt>

## Search 2 — query: "2022 NFL Draft list by team 2022 draft picks"
### Rank 1 of 174 — 0.66 (passed on)
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
### Rank 2 of 174 — 0.64
<excerpt title="2022 NFL Draft Picks & Results">
2 38Arnold Ebiketie Penn State, DE CAR, NYJ, NYG  
2 39Kyler Gordon Washington, DB-  
2 40Boye Mafe Minnesota, DE DEN  
2 41Kenneth Walker Michigan State, RB-  
2 42Andrew Booth Clemson, CB WAS, IND  
2 43Wan'Dale Robinson Kentucky, WR ATL  
2 44John Metchie Alabama, WR CLE  
2 45David Ojabo Michigan, LB-  
2 46Josh Paschal Kentucky, DE MIN  
2 47Phidarian Mathis Alabama, DT IND  
2 48Jaquan Brisker Penn State, S LAC  
2 49Alontae Taylor Tennessee, DB-  
2 50Tyquan Thornton Baylor, WR MIA, KC  
2 51Cameron Jurgens Nebraska, OL-  
2 52George Pickens Georgia, WR-  
2 53Alec Pierce Cincinnati, WR LV, GB, MIN  
2 54Skyy Moore Western Michigan, WR NE  
2 55Trey McBride Colorado State, TE-  
2 56Sam Williams Ole Miss, DE-  
2 57Luke Goedeke Central Michigan, OL BUF  
2 58Troy Andersen Montana State, LB TEN  
2 59Ed Ingram LSU, G GB  
2 60Cam Taylor-Britt Nebraska, CB TB, BUF  
2 61Drake Jackson USC, LB-  
2 62Bryan Cook Cincinnati, S-  
2 63James Cook Georgia, RB CIN  
2 64Nik Bonitto Oklahoma, LB LAR  
3 65Luke Fortner Kentucky, G-  
3 66Brian Asamoah Oklahoma, LB DET  
3 67Joshua Ezeudu North Carolina, OL-  
3 68Martin Emerson Mississippi State, CB HOU  
3 69Nicholas Petit-Frere Ohio State, T NYJ  
3 70Chad Muma Wyoming, LB CAR  
3 71Velus Jones Tennessee, WR-  
3 72Abraham Lucas Washington State, OL-  
3 73Jelani Woods Virginia, TE WAS  
3 74Desmond Ridder Cincinnati, QB-  
3 75Christian Harris Alabama, LB DEN
</excerpt>
### Rank 3 of 174 — 0.62
<excerpt title="2022 NFL Draft Results: Team By Team">
### Green Bay Packers
Round 1: No. 22 (from Raiders) **Quay Walker**, LB (Georgia) (signed)
Round 1: No. 28 **Devonte Wyatt**, DT (Georgia) (signed)
Round 2: No. 34 (from Lions through Vikings)**Christian Watson**, WR (North Dakota State) (signed)
Round 3: No. 92**Sean Rhyan**, OL (UCLA) (signed)
Round 4: No. 132 **Romeo Doubs**, WR (Nevada) (signed)
Round 4: No. 140**Zach Tom**, OT (Wake Forest) (signed)
Round 5: No. 179(from Colts through Broncos)**Kingsley Enagbare**, DL (South Carolina) (signed)
Round 7: No. 228 (from Bears through Texans)**Tariq Carpenter**, LB (Georgia Tech) (signed)
Round 7: No. 234(from Browns through Lions and Broncos)**Jonathan Ford**, DT (Miami) (signed)
Round 7: No. 249**Rasheed Walker**, OT (Penn State) (signed)
Round 7: No. 258**Samori Toure**, WR (Nebraska) (signed)

### Houston Texans
Round 1: No. 3 **Derek Stingley Jr.**, CB (LSU) (signed)
Round 1: No. 15 (from Dolphins through Eagles) **Kenyon Green**, G (Texas A&M) (signed)
Round 2: No. 37**Jalen Pitre**, S (Baylor) (signed)
Round 2: No. 44(from Browns)**John Metchie III**, WR (Alabama) (signed)
Round 3: No. 75(from Broncos)**Christian Harris**, LB (Alabama) (signed)
Round 4: No. 107 (from Lions through Browns) **Dameon Pierce**, RB (Florida) (signed)
Round 5: No. 150(from Bears): **Thomas Booker**, DT (Stanford) (signed)
Round 5: No. 170 (from Buccaneers through Patriots): **Teagan Quitoriano**, TE (Oregon State) (signed)
Round 6: No. 205 (from Packers)**Austin Deculus**, OL (LSU) (signed)

### Indianapolis Colts
Round 2: No. 53 (from Raiders through Packers and Vikings)**Alec Pierce**, WR (Cincinnati) (signed)
Round 3: No. 73 (from Commanders)**Jelani Woods**, TE (Virginia) (signed)
Round 3: No. 77 (from Vikings)**Bernhard Raimann**, OT (Central Michigan)(signed)
Round 3: No. 96(from Rams through Broncos)**Nick Cross**, S (Maryland) (signed)
Round 5: No. 159**Eric Johnson**, DT (Missouri State)(signed)
Round 6: No. 192 (from Vikings)**Andrew Ogletree**, TE (Youngstown State)(signed)
Round 6: No. 216**Curtis Brooks**, DT (Cincinnati)(signed)
Round 7: No. 239**Rodney Thomas II**, S (Yale) (signed)

### Jacksonville Jaguars
Round 1: No. 1 **Travon Walker**, Edge (Georgia) (signed)
Round 1: No. 27 (from Buccaneers) **Devin Lloyd**, LB (Utah) (signed)
Round 3: No. 65**Luke Fortner**, C (Kentucky) (signed)
Round 3: No. 70 (from Panthers)**Chad Muma**, LB (Wyoming) (signed)
Round 5: No. 154 (from Commanders through Eagles): **Snoop Conner**, RB (Ole Miss) (signed)
Round 6: No. 197 (from Eagles)**Gregory Junior**, CB (Ouachita Baptist) (signed)
Round 7: No. 222**Montaric Brown**, CB (Arkansas) (signed)
</excerpt>
### Rank 4 of 174 — 0.61
<excerpt title="2022 NFL Draft Results: Team By Team">
### New Orleans Saints
Round 1: No. 11 (from Commanders) **Chris Olave**, WR (Ohio State) (signed)
Round 1: No. 19 (from Eagles) **Trevor Penning**, OT (Northern Iowa) (signed)
Round 2: No. 49**Alontae Taylor**, CB (Tennessee) (signed)
Round 5: No. 161 **D’Marco Jackson**, LB (Appalachian State) (signed)
Round 6: No. 194 (from Colts through Eagles)**Jordan Jackson**, DT (Air Force) (signed)
Round 6: No. —_Selection forfeited_

### New York Giants
Round 1: No. 5 **Kayvon Thibodeaux**, DE (Oregon) (signed)
Round 1: No. 7 (from Bears) **Evan Neal**, OT (Alabama) (signed)
Round 2: No. 43 (from Falcons)**Wan’Dale Robinson**, WR (Kentucky) (signed)
Round 3: No. 67**Joshua Ezeudu**, G (North Carolina) (signed)
Round 3: No. 81 (from Dolphins)**Cor’Dale Flott**, CB (LSU) (signed)
Round 4: No. 112 (from Bears) **Daniel Bellinger**, TE (San Diego State) (signed)
Round 4: No. 114 (from Falcons) **Dane Belton**, S (Iowa) (signed)
Round 5: No. 146 (from Jets) **Micah McFadden**, LB (Indiana) (signed)
Round 5: No. 147 **D.J. Davidson**, DT (Arizona State) (signed)
Round 5: No. 173 (from Chiefs through Ravens)**Marcus McKethan**, OG (North Carolina) (signed)
Round 6: No. 182**Darrian Beavers**, LB (Cincinnati) (signed)

### New York Jets
Round 1: No. 4 **Ahmad Gardner**, CB (Cincinnati) (signed)
Round 1: No. 10 (from Seahawks) **Garrett Wilson**, WR (Ohio State) (signed)
Round 1: No. 26 (from Titans) **Jermaine JohnsonII**, DE (Florida State) (signed)
Round 2: No. 36(from Giants) **Breece Hall**, RB (Iowa State) (signed)
Round 3: No. 101 (from Saints through Eagles and Titans)**Jeremy Ruckert**, TE (Ohio State) (signed)
Round 4: No. 111 (from Panthers) **Max Mitchell**, OT (Louisiana) (signed)
Round 4: No. 117 (from Vikings) **Michael Clemons**, DE (Texas A&M) (signed)

### Philadelphia Eagles
Round 1: No. 13 (from Browns through Texans) **Jordan Davis**, DT (Georgia) (signed)
Round 2: No. 51**Cam Jurgens**, C (Nebraska) (signed)
Round 3: No. 83**Nakobe Dean**, LB (Georgia) (signed)
Round 6: No. 181(from Lions): **Kyron Johnson**, LB (Kansas) (signed)
Round 6: No. 198(from Steelers through Jaguars): TE **Grant Calcaterra**, TE (SMU) (signed)

### Pittsburgh Steelers
Round 1: No. 20 **Kenny Pickett**, QB (Pittsburgh) (signed)
Round 2: No. 52**George Pickens**, WR (Georgia) (signed)
Round 3: No. 84**DeMarvin Leal**, DE (Texas A&M)(signed)
Round 4: No. 138**Calvin Austin III**, WR (Memphis) (signed)
Round 6: No. 208 (from Chiefs)**Connor Heyward**, TE (Michigan State) (signed)
Round 7: No. 225 (from Jets)**Mark Robinson**, LB (Ole Miss)(signed)
Round 7: No. 241**Chris Oladokun**, QB (South Dakota State)(signed)
</excerpt>
### Rank 5 of 174 — 0.59
<excerpt title="2022 NFL Draft Results: Team By Team">
The 2022 NFL Draft has arrived! As the picks come in, we’ll keep track of each team’s haul right here:

### Arizona Cardinals
Round 2: No. 55**Trey McBride**, TE (Colorado State) (signed)
Round 3: No. 87**Cameron Thomas**, DE (San Diego State) (signed)
Round 3: No. 100 (from Ravens)**Myjai Sanders**, DE (Cincinnati) (signed)
Round 6: No. 201**Keaontay Ingram**, RB (USC) (signed)
Round 6: No. 215**Lecitus Smith**, OG (Virginia Tech) (signed)
Round 7: No. 244**Christian Matthew**, CB (Valdosta State) (signed)
Round 7: No. 256**Jesse Luketa**, OLB (Penn State) (signed)
Round 7: No. 257**Marquis Hayes**, OG (Oklahoma) (signed)

### Atlanta Falcons
Round 1: No. 8 **Drake London**, WR (USC) (signed)
Round 2: No. 38(from Panthers through Jets and Giants)**Arnold Ebiketie**, OLB (Penn State) (signed)
Round 2: No. 58 (from Titans)**Troy Andersen**, LB (Montana State) (signed)
Round 3: No. 74**Desmond Ridder**, QB (Cincinnati) (signed)
Round 3: No. 82 (from Colts)**DeAngelo Malone**, LB (Western Kentucky) (signed)
Round 5: No. 151**Tyler Allgeier**, RB (BYU) (signed)
Round 6: No. 190**Justin Shaffer**, OG (Georgia) (signed)
Round 6: No. 213**John FitzPatrick**, TE (Georgia) (signed)

### Baltimore Ravens
Round 1: No. 14 **Kyle Hamilton**, S (Notre Dame) (signed)
Round 1: No. 25 (from Bills) **Tyler Linderbaum**, C (Iowa) (signed)
Round 2: No. 45**David Ojabo**, OLB (Michigan) (signed)
Round 3: No. 76**Travis Jones**, NT (Connecticut) (signed)
Round 4: No. 110 (from Giants) **Daniel Faalele**, OT (Minnesota) (signed)
Round 4: No. 119 **Jayln Armour-Davis**, CB (Alabama) (signed)
Round 4: No. 128 (from Cardinals)**Charlie Kolar**, TE (Iowa State) (signed)
Round 4: No. 130 (from Bills)**Jordan Stout**, P (Penn State) (signed)
Round 4: No. 139 **Isaiah Likely**, TE (Coastal Carolina) (signed)
Round 4: No. 141 **Damarion Williams**, CB (Houston) (signed)
Round 6: No. 196 (from Dolphins)**Tyler Badie**, RB (Missouri) (signed)

### Buffalo Bills
Round 1: No. 23 (from Cardinals through Ravens) **Kaiir Elam**, CB (Florida)(signed)
Round 2: No. 63 (from Bengals)**James Cook**, RB (Georgia)(signed)
Round 3: No. 89**Terrel Bernard**, LB (Baylor) (signed)
Round 5: No. 148 (from Bears) **Khalil Shakir**, WR (Boise State)(signed)
Round 6: No. 180 (from Jaguars through Buccaneers)**Matt Araiza**, P (San Diego State)(signed)
Round 6: No. 185 (from Panthers)**Christian Benford**, CB (Villanova)(signed)
Round 6: No. 209 (from Bengals)**Luke Tenuta**, OT (Virginia Tech)(signed)
Round 7: No. 231 (from Falcons)**Baylon Spector**, LB (Clemson)(signed)
</excerpt>

## Search 3 — query: "2022 nfl draft picks Jacksonville 2022 draft picks list team by team site:drafthistory.com 2022 nfl draft by team"
### Rank 1 of 548 — 0.31 (passed on)
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
### Rank 2 of 548 — 0.29
<excerpt title="Defensive Ends">
22	7	16	233	Andre Jones	Commanders	Louisiana-Lafayette  
 	23	7	23	240	Derek Parish	Jaguars	Houston  
2022	1	1	1	1	Travon Walker	Jaguars	Georgia  
 	2	1	2	2	Aidan Hutchinson	Lions	Michigan  
 	3	1	5	5	Kayvon Thibodeaux	Giants	Oregon  
 	4	1	26	26	Jermaine Johnson	Jets	Florida State  
 	5	1	30	30	George Karlaftis	Chiefs	Purdue  
 	6	2	14	46	Josh Paschal	Lions	Kentucky  
 	7	2	24	56	Sam Williams	Cowboys	Mississippi  
 	8	3	14	78	Alex Wright	Browns	Alabama-Birmingham  
 	9	3	23	87	Cameron Thomas	Cardinals	San Diego State  
 	10	3	36	100	Myjai Sanders	Cardinals	Cincinnati  
 	11	4	11	116	Eyioma Uwazurike	Broncos	Iowa State  
 	12	4	12	117	Micheal Clemons	Jets	Texas A&M  
 	13	5	22	165	Esezi Otomewo	Vikings	Minnesota  
 	14	5	31	174	Dominique Robinson	Bears	Miami (OH)  
 	15	5	36	179	Kingsley Enagbare	Packers	South Carolina  
 	16	6	10	189	Amare Barno	Panthers	Virginia Tech  
 	17	7	2	223	Isaiah Thomas	Browns	Oklahoma  
 	18	7	14	235	Daniel Hardy	Rams	Montana State  
 	19	7	27	248	Andre Anthony	Buccaneers	Louisiana State
</excerpt>
### Rank 3 of 548 — 0.28
<excerpt title="Wide Receivers">
28	7	2	219	Antoine Green	Lions	North Carolina  
 	29	7	11	228	Cotton Dowell	Titans	Tennessee-Martin  
 	30	7	27	244	Jalen Brooks	Cowboys	South Carolina  
 	31	7	36	253	Ronnie Bell	49ers	Michigan  
 	32	7	39	256	Grant DuBose	Packers	Charlotte  
2022	1	1	8	8	Drake London	Falcons	USC  
 	2	1	10	10	Garrett Wilson	Jets	Ohio State  
 	3	1	11	11	Chris Olave	Saints	Ohio State  
 	4	1	12	12	Jameson Williams	Lions	Alabama  
 	5	1	16	16	Jahan Dotson	Commanders	Penn State  
 	6	1	18	18	Treylon Burks	Titans	Arkansas  
 	7	2	2	34	Christian Watson	Packers	North Dakota State  
 	8	2	11	43	Wan'Dale Robinson	Giants	Kentucky  
 	9	2	12	44	John Metchie	Texans	Alabama  
 	10	2	18	50	Tyquan Thornton	Patriots	Baylor  
 	11	2	20	52	George Pickens	Steelers	Georgia  
 	12	2	21	53	Alec Pierce	Colts	Cincinnati  
 	13	2	22	54	Skyy Moore	Chiefs	Western Michigan  
 	14	3	7	71	Velus Jones	Bears	Tennessee  
 	15	3	24	88	Jalen Tolbert	Cowboys	South Alabama  
 	16	3	35	99	David Bell	Browns	Purdue  
 	17	3	41	105	Danny Gray	49ers	Southern Methodist
</excerpt>
### Rank 4 of 548 — 0.25
<excerpt title="DraftHistory.com">
Picks: 7 -- Value: 3798.80  
Name	Round	Pick	Player	Position	College	Source	Value  
Arvell Reese	1	5	5	DE	Ohio State	 	1700.00  
Francis Mauigoa	1	10	10	T	Miami (FL)	Bengals	1300.00  
Colton Hood	2	5	37	DB	Tennessee	 	530.00  
Malachi Fields	3	10	74	WR	Notre Dame	Chiefs via Browns	220.00  
Bobby Jamison-Travis	6	5	186	DT	Auburn	 	18.00  
J.C. Davis	6	11	192	T	Illinois	Dolphins	15.60  
Jack Kelly	6	12	193	LB	Brigham Young	Cowboys	15.20  
Jaguars  
13-4-0 (0.765)  
Pts: 474 -- PA: 336  
Picks: 10 -- Value: 888.50  
Name	Round	Pick	Player	Position	College	Source	Value  
Nate Boerkircher	2	24	56	TE	Texas A&M	 	340.00  
Albert Regis	3	17	81	DT	Texas A&M	Lions	185.00  
Emmanuel Pregnon	3	24	88	G	Oregon	 	150.00  
Jalen Huskey	3	36	100	DB	Maryland	special compensatory Lions	100.00  
Wesley Williams	4	19	119	DE	Duke	Panthers	56.00  
Tanner Koziol	5	24	164	TE	Houston	 	26.80  
Josh Cameron	6	10	191	WR	Baylor	Chiefs via Patriots	16.00  
C.J. Williams	6	22	203	WR	Stanford	Eagles via Texans and Eagles	11.20
</excerpt>
### Rank 5 of 548 — 0.24
<excerpt title="Wide Receivers">
4	2	2	34	Justin Hunter	Titans	Tennessee  
 	5	2	9	41	Robert Woods	Bills	USC  
 	6	2	27	59	Aaron Dobson	Patriots	Marshall  
 	7	3	12	74	Terrance Williams	Cowboys	Baylor  
 	8	3	14	76	Keenan Allen	Chargers	California  
 	9	3	16	78	Marquise Goodwin	Bills	Texas  
 	10	3	17	79	Markus Wheaton	Steelers	Oregon State  
 	11	3	30	92	Stedman Bailey	Rams	West Virginia  
 	12	4	4	101	Ace Sanders	Jaguars	South Carolina  
 	13	4	5	102	Josh Boyce	Patriots	Texas Christian  
 	14	4	26	123	Chris Harper	Seahawks	Kansas State  
 	15	4	31	128	Quinton Patton	49ers	Louisiana Tech  
 	16	5	2	135	Denard Robinson	Jaguars	Michigan  
 	17	5	11	144	Kenny Stills	Saints	Oklahoma  
 	18	5	28	161	Tavarres King	Broncos	Georgia  
 	19	6	3	171	Corey Fuller	Lions	Virginia Tech  
 	20	6	6	174	Ryan Swope	Cardinals	Texas A&M  
 	21	6	18	186	Justin Brown	Steelers	Oklahoma  
 	22	6	27	195	Alan Bonner	Texans	Jacksonville State  
 	23	6	29	197	Cobi Hamilton	Bengals	Arkansas  
 	24	7	3	209	Brice Butler	Raiders	San Diego State  
 	25	7	10	216	Charles Johnson	Packers	Grand Valley State
</excerpt>

## Search 4 — query: "2022 NFL draft Raiders picks 2022 NFL draft Raiders 2022"
### Rank 1 of 191 — 0.47 (passed on)
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
### Rank 2 of 191 — 0.42
<excerpt title="2022 NFL draft">
4	123	Los Angeles Chargers	Isaiah Spiller 	RB	Texas A&M	  
	4	124	Cleveland Browns	Cade York 	K	LSU
from Philadelphia via Houston[R4 – 15]
4	125	Miami Dolphins	Erik Ezukanma 	WR	Texas Tech
from Pittsburgh[R4 – 16]
4	126	Las Vegas Raiders	Neil Farrell Jr. 	DT	LSU
from Las Vegas via Minnesota[R4 – 17]
4	127	New England Patriots	Pierre Strong Jr. 	RB	South Dakota State	  
	4	128	Baltimore Ravens	Charlie Kolar 	TE	Iowa State
from Arizona[R4 – 18]
4	129	Dallas Cowboys	Jake Ferguson †	TE	Wisconsin	  
	4	130	Baltimore Ravens	Jordan Stout †	P	Penn State
from Buffalo[R4 – 19]
4	131	Tennessee Titans	Hassan Haskins 	RB	Michigan	  
	4	132	Green Bay Packers	Romeo Doubs 	WR	Nevada	  
	4	133	Tampa Bay Buccaneers	Jake Camarda 	P	Georgia	  
	4	134	San Francisco 49ers	Spencer Burford 	T	UTSA	  
	4	135	Kansas City Chiefs	Joshua Williams 	CB	Fayetteville State	  
	4	136	Cincinnati Bengals	Cordell Volson 	T	North Dakota State	  
	4	137	New England Patriots	Bailey Zappe 	QB	Western Kentucky
from LA Rams via Houston and Carolina[R4 – 20]
</excerpt>
### Rank 3 of 191 — 0.40
<excerpt title="2022 NFL draft">
Shook, Nick (August 31, 2021). "Vikings acquiring TE Chris Herndon from Jets in trade following Irv Smith Jr.'s knee injury". NFL.com. Retrieved August 31, 2021.  
Jump up to:  
 Smith, Eric (April 30, 2022). "New Vikings CB Akayleb Evans Ready to Learn From Patrick Peterson". NFL.com. Retrieved April 30, 2022.  
Jump up to:  
 Vashee, Rushil (April 30, 2022). "Panthers trade into 4th round, select LB Brandon Smith". USA Today.  
Jump up to:  
 Edwards, Levi (April 30, 2022). "Raiders trade up to No. 122, select RB Zamir White". Raiders.com.  
 Nogle, Kevin (May 1, 2021). "2021 NFL Draft: Texans Trade Recap". The Phinsider. Retrieved September 4, 2021.  
Jump up to:  
 Edwards, Levi (April 30, 2022). "Defensive lineman Neil Farrell Jr. selected after Raiders trade up to No. 126".  
 "2021 NFL Draft trade tracker: Full details of every move". NFL.com. April 29, 2021. Retrieved May 5, 2021.  
 McClain, John (April 9, 2020). "Texans acquire Brandin Cooks in trade with Rams". Texas Sports Nation. Houston Chronicle. Retrieved April 26, 2020.  
 "2021 NFL Draft: Texans Trade Recap". Houston Texans. April 30, 2021. Retrieved September 4, 2021.  
Jump up to:  
 Risdon, Jeff (September 1, 2021). "Full details of the Trinity Benson trade between the Lions and Broncos". Yahoo! Sports. Retrieved September 4, 2021.  
Jump up to:  
 Goldman, Charles (April 30, 2022). "Chiefs trade up with Seahawks for Kentucky OT Darian Kinnard at pick No. 145". USA Today.  
Jump up to:
</excerpt>
### Rank 4 of 191 — 0.40
<excerpt title="Photos: Meet the 2022 Las Vegas Raiders Draft Class">
# Photos: Meet the 2022 Las Vegas Raiders Draft Class
Skip to main content
Primary nav
*   News  
*   Team  
*   Schedule  
*   Multimedia  
*   Photos  
*   Raiderettes  
*   Community  
*   History  
*     
    *   Allegiant Stadium  
    *   Promotions  
    *   Fans  
    *   Fit  
    *   Raiders Foundation  
    *   Alumni Relations  
    *   Español  
    *   International  
    *   Connect With Us

*   TICKETS  
*   SHOP
Search
Open menu button Action related nav
*   Watch  
*   Tickets  
*   Shop  
*   My Account

*   Latest  
*   Purchase Photos  
*   Practice  
*   Gameday  
*   Top Shots  
*   Silver and Black and White  
*   177 Feet Up  
*   Cinema in Silver and Black  
*   Raiderettes  
*   Raiders on Instagram
Advertising
The picks are in and the 2022 Las Vegas Raiders Draft Class has been set. Check out photos of all six of the Silver and Black's newest rookies.
*     
*     
*   [](mailto:?subject=Photos:%20Meet%20the%202022%20Las%20Vegas%20Raiders%20Draft%20Class&body=https%3A%2F%2Fwww.raiders.com%2Fphotos%2Fphotos-meet-the-2022-raiders-draft-class-nfl "Send email")  
*   Copied!
1 / 6
**G Dylan Parham**
Third Round (90th overall)
Memphis
University of Memphis Athletics
2 / 6
**RB Zamir White**
Fourth Round (122th overall)
Georgia
John Bazemore/Associated Press
3 / 6
**DL Neil Farrell Jr.**
Fourth Round (126th overall)
LSU
Gerald Herbert/Associated Press
4 / 6
**DT Matthew Butler**
Fifth Round (175th overall)
Tennessee
Darron Cummings/Associated Press
5 / 6
**T Thayer Munford Jr.**
Seventh Round (238th overall)
Ohio State
Jay LaPrete/Associated Press
6 / 6

# Photos: Meet the 2022 Las Vegas Raiders Draft Class
**RB Brittain Brown**
Seventh Round (250th overall)
UCLA
Marcio Jose Sanchez/Associated Press
Advertising
This Ad will close in 3
Advertising
</excerpt>
### Rank 5 of 191 — 0.39
<excerpt title="2022 NFL draft">
Resolution JC-2A selection[g]
4	106	Tampa Bay Buccaneers	Cade Otton 	TE	Washington
from Jacksonville[R4 – 1]
4	107	Houston Texans	Dameon Pierce 	RB	Florida
from Detroit via Cleveland[R4 – 2]
4	108	Cleveland Browns	Perrion Winfrey 	DT	Oklahoma
from Houston[R4 – 3]
4	109	Seattle Seahawks	Coby Bryant 	CB	Cincinnati
from NY Jets[R4 – 4]
4	110	Baltimore Ravens	Daniel Faalele 	T	Minnesota
from NY Giants[R4 – 5]
4	111	New York Jets	Max Mitchell 	T	Louisiana
from Carolina[R4 – 6]
4	112	New York Giants	Daniel Bellinger 	TE	San Diego State
from Chicago[R4 – 7]
4	113	Washington Commanders	Percy Butler 	S	Louisiana	  
	4	114	New York Giants	Dane Belton 	S	Iowa
from Atlanta[R4 – 8]
4	115	Denver Broncos	Damarri Mathis 	CB	Pittsburgh	  
	4	116	Denver Broncos	Eyioma Uwazurike 	DT	Iowa State
from Seattle[R4 – 9]
4	117	New York Jets	Micheal Clemons 	DE	Texas A&M
from Minnesota[R4 – 10]
4	118	Minnesota Vikings	Akayleb Evans 	CB	Missouri
from Cleveland[R4 – 11]
4	119	Baltimore Ravens	Jalyn Armour-Davis 	CB	Alabama	  
	4	120	Carolina Panthers	Brandon Smith 	LB	Penn State
from New Orleans via Washington[R4 – 12]
4	121	New England Patriots	Jack Jones 	CB	Arizona State
from Miami via Kansas City[R4 – 13]
4	122	Las Vegas Raiders	Zamir White 	RB	Georgia
from Indianapolis via Minnesota[R4 – 14]
</excerpt>

## Search 5 — query: "Super Bowl winners 1980 1981 1982 1983 1984 1985 1986 1987 1988 1989 list"
### Rank 1 of 107 — 0.84 (passed on)
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
### Rank 2 of 107 — 0.84
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
### Rank 3 of 107 — 0.83
<excerpt title="Ranking 1980s Super Bowl champions">
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

# OLD SCHOOL NFL | In what order 1-10 would you rank the Super Bowl champions of the 1980s: | Facebook
[](https://www.facebook.com/photo/?fbid=28588529127423613&set=gm.2182653085994382&idorvanity=1329445667981799&__cft__[0]=AZj0NFtVy6FmrYzKLVfW8AnMMAQm83Jp-iBV4_fmCtnMWPkmUDl57ojdB8GOO4kdHW2J3sLG905gmPCnOxo9mP4L1KQmR_KB2VG7W1sBI7EuovweJQUig2eQjVop_SFpJj-GOmHap05wBbJL8ZClxSAOcRytFeJpa9AIBSGha9N5Ba4HHdKplcDJ190rjuwb&__tn__=EH-R)
![Image 3](blob:http://localhost/85d8b181a20aeb64a3afc2f1c39d2480)
![Image 4](blob:http://localhost/2b45e6f1a2ae097354c0b291152873d5)
All reactions:
81
38 comments
3 shares
Like
Comment
Share
Most relevant
Dk Jacob
85 bears
had something that comes
around only once in a lifetime …
See more
</excerpt>
### Rank 4 of 107 — 0.81
<excerpt title="Super Bowl History (NFL)">
## Super Bowl Results
| IX  | January 12, 1975(1974) |  PITTSBURGH STEELERS | 16-6 |  Minnesota Vikings |  Tulane Stadium(3) New Orleans, LA(3) |  
| X  | January 18, 1976(1975) |  PITTSBURGH STEELERS (2) | 21-17 |  Dallas Cowboys |  Miami Orange Bowl(4) Miami,FL(4) |  
| XI  | January 9, 1977(1976) |  OAKLAND RAIDERS | 32-14 |  Minnesota Vikings |  Rose Bowl(1) Pasadena,CA(1) |  
| XII  | January 15, 1978(1977) |  Dallas Cowboys (3) | 27-10 |  DENVER BRONCOS |  Louisiana Superdome(1) New Orleans, LA(4) |  
| XIII  | January 21, 1979(1978) |  PITTSBURGH STEELERS (3) | 35-31 |  Dallas Cowboys |  Miami Orange Bowl(5) Miami,FL(5) |  
| XIV  | January 20, 1980(1979) |  PITTSBURGH STEELERS (4) | 31-19 |  LOS ANGELES RAMS |  Rose Bowl(2) Pasadena,CA(2) |  
| XV  | January 25, 1981(1980) |  OAKLAND RAIDERS (2) | 27-10 |  Philadelphia Eagles |  Louisiana Superdome(2) New Orleans, LA(5) |  
| XVI  | January 24, 1982(1981) |  San Francisco 49erS | 26-21 |  CINCINNATI BENGALS |  Pontiac Silverdome Pontiac,MI |  

## Super Bowl Results
| XVII  | January 30, 1983(1982) |  Washington Redskins | 27-17 |  MIAMI DOLPHINS |  Rose Bowl(3) Pasadena,CA(3) |  
| XVIII  | January 22, 1984(1983) |  Los Angeles Raiders (3) | 38-9 |  Washington Redskins |  Tampa Stadium(1) Tampa,FL(1) |  
| XIX  | January 20, 1985(1984) |  San Francisco 49erS (2) | 38-16 |  MIAMI DOLPHINS |  Stanford Stadium(4) Stanford,CA (1) |  
| XX  | January 26, 1986(1985) |  Chicago Bears | 46-10 |  NEW ENGLAND PATRIOTS |  Louisiana Superdome(3) New Orleans, LA(6) |  
| XXI  | January 25, 1987(1986) |  New York Giants | 39-20 |  DENVER BRONCOS |  Rose Bowl(4) Pasadena,CA(4) |  
| XXII  | January 31, 1988(1987) |  Washington Redskins (2) | 42-10 |  DENVER BRONCOS |  Jack Murphy Stadium(1) San Diego,CA(1) |  
| XXIII  | January 22, 1989(1988) |  SAN FRANCISCO 49ERS (3) | 20-16 |  CINCINNATI BENGALS |  Joe Robbie Stadium(1) Miami Gardens,FL (6) |  
| XXIV  | January 28, 1990(1989) |  SAN FRANCISCO 49ERS (4) | 55-10 |  DENVER BRONCOS |  Louisiana Superdome(4) New Orleans, LA(7) |
</excerpt>
### Rank 5 of 107 — 0.79
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

## Search 6 — query: "2022 nfl draft Raiders picks list 2022 drafthistory Raiders"
### Rank 1 of 164 — 0.44 (passed on)
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
### Rank 2 of 164 — 0.43
<excerpt title="2022 NFL draft">
Mr. Irrelevant  
Notable undrafted playersedit  
Original NFL team	Player	Pos.	College	Notes  
Arizona Cardinals	Darrell Baker Jr. 	CB	Georgia Southern	  
Arizona Cardinals	Chandler Wooten 	LB	Auburn	  
Atlanta Falcons	Timmy Horne 	DT	Kansas State	  
Atlanta Falcons	Nate Landman 	LB	Colorado	  
Buffalo Bills	Alec Anderson 	T	UCLA	  
Buffalo Bills	Raheem Blackshear 	RB	Virginia Tech	  
Buffalo Bills	Ja'Marcus Ingram 	CB	Buffalo	  
Carolina Panthers	Arron Mosby 	LB	Fresno State	  
Chicago Bears	Jack Sanborn 	LB	Wisconsin	  
Chicago Bears	Jake Tonges 	TE	California	  
Chicago Bears	Jaylon Jones 	CB	Ole Miss	  
Cincinnati Bengals	Cal Adomitis 	LS	Pittsburgh	  
Cincinnati Bengals	Ben Brown 	C	Ole Miss	  
Cleveland Browns	D'Anthony Bell 	S	West Florida	  
Cleveland Browns	Brock Hoffman 	C	Virginia Tech	  
Dallas Cowboys	Brandon Aubrey †	K	Notre Dame	  
Played college soccer; drafted in 2022 USFL draft

Dallas Cowboys	Markquese Bell 	S	Florida A&M	  
Dallas Cowboys	Malik Davis 	RB	Florida	  
Denver Broncos	Brandon Johnson 	WR	UCF	  
Denver Broncos	Ja'Quan McMillian 	CB	East Carolina	  
Denver Broncos	Dondrea Tillman 	LB	IUP	  
Green Bay Packers	Tyler Goodson 	RB	Iowa	  
Houston Texans	Jake Hansen 	LB	Illinois	  
Houston Texans	Kurt Hinish 	DT	Notre Dame	  
Indianapolis Colts	Dallis Flowers 	CB	Pittsburg State	  
Indianapolis Colts	Ryan Van Demark 	T	UConn	  
Kansas City Chiefs	Mike Caliendo 	G	Western Michigan	  
Kansas City Chiefs	Jack Cochrane 	LB	South Dakota	  
Las Vegas Raiders	Isaiah Pola-Mao 	S	USC	  
Las Vegas Raiders	Luke Masterson 	LB	Wake Forest	  
Las Vegas Raiders	Sincere McCormick 	RB	UTSA	  
Las Vegas Raiders	Sam Webb 	CB	Missouri Western	  
Los Angeles Chargers	Stone Smartt 	TE	Old Dominion	  
Los Angeles Rams	Cameron Dicker †	K	Texas	  
Los Angeles Rams	Jake Hummel 	LB	Iowa State	  
Miami Dolphins	Kader Kohou 	CB	Texas A&M–Commerce	  
Minnesota Vikings	Ryan Wright 	P	Tulane	  
New England Patriots	Brenden Schooler †	S	Texas	  
New Orleans Saints	Abram Smith 	RB	Baylor	  
All-XFL Team 2023; drafted in 2023 XFL draft
</excerpt>
### Rank 3 of 164 — 0.42
<excerpt title="Photos: Meet the 2022 Las Vegas Raiders Draft Class">
# Photos: Meet the 2022 Las Vegas Raiders Draft Class
Skip to main content
Primary nav
*   News  
*   Team  
*   Schedule  
*   Multimedia  
*   Photos  
*   Raiderettes  
*   Community  
*   History  
*     
    *   Allegiant Stadium  
    *   Promotions  
    *   Fans  
    *   Fit  
    *   Raiders Foundation  
    *   Alumni Relations  
    *   Español  
    *   International  
    *   Connect With Us

*   TICKETS  
*   SHOP
Search
Open menu button Action related nav
*   Watch  
*   Tickets  
*   Shop  
*   My Account

*   Latest  
*   Purchase Photos  
*   Practice  
*   Gameday  
*   Top Shots  
*   Silver and Black and White  
*   177 Feet Up  
*   Cinema in Silver and Black  
*   Raiderettes  
*   Raiders on Instagram
Advertising
The picks are in and the 2022 Las Vegas Raiders Draft Class has been set. Check out photos of all six of the Silver and Black's newest rookies.
*     
*     
*   [](mailto:?subject=Photos:%20Meet%20the%202022%20Las%20Vegas%20Raiders%20Draft%20Class&body=https%3A%2F%2Fwww.raiders.com%2Fphotos%2Fphotos-meet-the-2022-raiders-draft-class-nfl "Send email")  
*   Copied!
1 / 6
**G Dylan Parham**
Third Round (90th overall)
Memphis
University of Memphis Athletics
2 / 6
**RB Zamir White**
Fourth Round (122th overall)
Georgia
John Bazemore/Associated Press
3 / 6
**DL Neil Farrell Jr.**
Fourth Round (126th overall)
LSU
Gerald Herbert/Associated Press
4 / 6
**DT Matthew Butler**
Fifth Round (175th overall)
Tennessee
Darron Cummings/Associated Press
5 / 6
**T Thayer Munford Jr.**
Seventh Round (238th overall)
Ohio State
Jay LaPrete/Associated Press
6 / 6

# Photos: Meet the 2022 Las Vegas Raiders Draft Class
**RB Brittain Brown**
Seventh Round (250th overall)
UCLA
Marcio Jose Sanchez/Associated Press
Advertising
This Ad will close in 3
Advertising
</excerpt>
### Rank 4 of 164 — 0.41
<excerpt title="2022 NFL draft">
Dallas Cowboys	Markquese Bell 	S	Florida A&M	  
Dallas Cowboys	Malik Davis 	RB	Florida	  
Denver Broncos	Brandon Johnson 	WR	UCF	  
Denver Broncos	Ja'Quan McMillian 	CB	East Carolina	  
Denver Broncos	Dondrea Tillman 	LB	IUP	  
Green Bay Packers	Tyler Goodson 	RB	Iowa	  
Houston Texans	Jake Hansen 	LB	Illinois	  
Houston Texans	Kurt Hinish 	DT	Notre Dame	  
Indianapolis Colts	Dallis Flowers 	CB	Pittsburg State	  
Indianapolis Colts	Ryan Van Demark 	T	UConn	  
Kansas City Chiefs	Mike Caliendo 	G	Western Michigan	  
Kansas City Chiefs	Jack Cochrane 	LB	South Dakota	  
Las Vegas Raiders	Isaiah Pola-Mao 	S	USC	  
Las Vegas Raiders	Luke Masterson 	LB	Wake Forest	  
Las Vegas Raiders	Sincere McCormick 	RB	UTSA	  
Las Vegas Raiders	Sam Webb 	CB	Missouri Western	  
Los Angeles Chargers	Stone Smartt 	TE	Old Dominion	  
Los Angeles Rams	Cameron Dicker †	K	Texas	  
Los Angeles Rams	Jake Hummel 	LB	Iowa State	  
Miami Dolphins	Kader Kohou 	CB	Texas A&M–Commerce	  
Minnesota Vikings	Ryan Wright 	P	Tulane	  
New England Patriots	Brenden Schooler †	S	Texas	  
New Orleans Saints	Abram Smith 	RB	Baylor	  
All-XFL Team 2023; drafted in 2023 XFL draft

New Orleans Saints	John Parker Romo 	K	Virginia Tech	  
New Orleans Saints	Lucas Krull 	TE	Pittsburgh	  
New Orleans Saints	Nephi Sewell 	LB	Utah	  
New Orleans Saints	Rashid Shaheed †	WR	Weber State	  
New Orleans Saints	Daniel Whelan 	P	UC Davis	  
New York Jets	Tony Adams 	S	Illinois	  
New York Jets	Zonovan Knight 	RB	NC State	  
Philadelphia Eagles	Josh Blackwell 	CB	Duke	  
Philadelphia Eagles	Reed Blankenship 	S	Middle Tennessee	  
Philadelphia Eagles	Britain Covey 	WR	Utah	  
Philadelphia Eagles	Josh Jobe 	CB	Alabama	  
Pittsburgh Steelers	Jaylen Warren 	RB	Oklahoma State	  
San Francisco 49ers	Jordan Mason 	RB	Georgia Tech	  
Tampa Bay Buccaneers	Dylan Cook 	T	Montana	  
Tennessee Titans	Tre Avery 	CB	Rutgers	  
Tennessee Titans	Julius Chestnut 	RB	Sacred Heart	  
Tennessee Titans	Jack Gibbens 	LB	Minnesota	  
Tennessee Titans	Xavier Newman-Johnson 	G	Baylor	  
Tennessee Titans	Ryan Stonehouse 	P	Colorado State	  
Tradesedit
(PD) indicates trades completed prior to the start of the draft (i.e. Pre-Draft), while (D) denotes trades which took place during the 2022 draft.
Round 1
</excerpt>
### Rank 5 of 164 — 0.40
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

## Search 7 — query: "2022 NFL draft Raiders pick list Raiders 2022 draft"
### Rank 1 of 192 — 0.50 (passed on)
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
### Rank 2 of 192 — 0.48
<excerpt title="2022 NFL draft">
Dallas Cowboys	Markquese Bell 	S	Florida A&M	  
Dallas Cowboys	Malik Davis 	RB	Florida	  
Denver Broncos	Brandon Johnson 	WR	UCF	  
Denver Broncos	Ja'Quan McMillian 	CB	East Carolina	  
Denver Broncos	Dondrea Tillman 	LB	IUP	  
Green Bay Packers	Tyler Goodson 	RB	Iowa	  
Houston Texans	Jake Hansen 	LB	Illinois	  
Houston Texans	Kurt Hinish 	DT	Notre Dame	  
Indianapolis Colts	Dallis Flowers 	CB	Pittsburg State	  
Indianapolis Colts	Ryan Van Demark 	T	UConn	  
Kansas City Chiefs	Mike Caliendo 	G	Western Michigan	  
Kansas City Chiefs	Jack Cochrane 	LB	South Dakota	  
Las Vegas Raiders	Isaiah Pola-Mao 	S	USC	  
Las Vegas Raiders	Luke Masterson 	LB	Wake Forest	  
Las Vegas Raiders	Sincere McCormick 	RB	UTSA	  
Las Vegas Raiders	Sam Webb 	CB	Missouri Western	  
Los Angeles Chargers	Stone Smartt 	TE	Old Dominion	  
Los Angeles Rams	Cameron Dicker †	K	Texas	  
Los Angeles Rams	Jake Hummel 	LB	Iowa State	  
Miami Dolphins	Kader Kohou 	CB	Texas A&M–Commerce	  
Minnesota Vikings	Ryan Wright 	P	Tulane	  
New England Patriots	Brenden Schooler †	S	Texas	  
New Orleans Saints	Abram Smith 	RB	Baylor	  
All-XFL Team 2023; drafted in 2023 XFL draft

New Orleans Saints	John Parker Romo 	K	Virginia Tech	  
New Orleans Saints	Lucas Krull 	TE	Pittsburgh	  
New Orleans Saints	Nephi Sewell 	LB	Utah	  
New Orleans Saints	Rashid Shaheed †	WR	Weber State	  
New Orleans Saints	Daniel Whelan 	P	UC Davis	  
New York Jets	Tony Adams 	S	Illinois	  
New York Jets	Zonovan Knight 	RB	NC State	  
Philadelphia Eagles	Josh Blackwell 	CB	Duke	  
Philadelphia Eagles	Reed Blankenship 	S	Middle Tennessee	  
Philadelphia Eagles	Britain Covey 	WR	Utah	  
Philadelphia Eagles	Josh Jobe 	CB	Alabama	  
Pittsburgh Steelers	Jaylen Warren 	RB	Oklahoma State	  
San Francisco 49ers	Jordan Mason 	RB	Georgia Tech	  
Tampa Bay Buccaneers	Dylan Cook 	T	Montana	  
Tennessee Titans	Tre Avery 	CB	Rutgers	  
Tennessee Titans	Julius Chestnut 	RB	Sacred Heart	  
Tennessee Titans	Jack Gibbens 	LB	Minnesota	  
Tennessee Titans	Xavier Newman-Johnson 	G	Baylor	  
Tennessee Titans	Ryan Stonehouse 	P	Colorado State	  
Tradesedit
(PD) indicates trades completed prior to the start of the draft (i.e. Pre-Draft), while (D) denotes trades which took place during the 2022 draft.
Round 1
</excerpt>
### Rank 3 of 192 — 0.48
<excerpt title="2022 NFL draft">
Mr. Irrelevant  
Notable undrafted playersedit  
Original NFL team	Player	Pos.	College	Notes  
Arizona Cardinals	Darrell Baker Jr. 	CB	Georgia Southern	  
Arizona Cardinals	Chandler Wooten 	LB	Auburn	  
Atlanta Falcons	Timmy Horne 	DT	Kansas State	  
Atlanta Falcons	Nate Landman 	LB	Colorado	  
Buffalo Bills	Alec Anderson 	T	UCLA	  
Buffalo Bills	Raheem Blackshear 	RB	Virginia Tech	  
Buffalo Bills	Ja'Marcus Ingram 	CB	Buffalo	  
Carolina Panthers	Arron Mosby 	LB	Fresno State	  
Chicago Bears	Jack Sanborn 	LB	Wisconsin	  
Chicago Bears	Jake Tonges 	TE	California	  
Chicago Bears	Jaylon Jones 	CB	Ole Miss	  
Cincinnati Bengals	Cal Adomitis 	LS	Pittsburgh	  
Cincinnati Bengals	Ben Brown 	C	Ole Miss	  
Cleveland Browns	D'Anthony Bell 	S	West Florida	  
Cleveland Browns	Brock Hoffman 	C	Virginia Tech	  
Dallas Cowboys	Brandon Aubrey †	K	Notre Dame	  
Played college soccer; drafted in 2022 USFL draft

Dallas Cowboys	Markquese Bell 	S	Florida A&M	  
Dallas Cowboys	Malik Davis 	RB	Florida	  
Denver Broncos	Brandon Johnson 	WR	UCF	  
Denver Broncos	Ja'Quan McMillian 	CB	East Carolina	  
Denver Broncos	Dondrea Tillman 	LB	IUP	  
Green Bay Packers	Tyler Goodson 	RB	Iowa	  
Houston Texans	Jake Hansen 	LB	Illinois	  
Houston Texans	Kurt Hinish 	DT	Notre Dame	  
Indianapolis Colts	Dallis Flowers 	CB	Pittsburg State	  
Indianapolis Colts	Ryan Van Demark 	T	UConn	  
Kansas City Chiefs	Mike Caliendo 	G	Western Michigan	  
Kansas City Chiefs	Jack Cochrane 	LB	South Dakota	  
Las Vegas Raiders	Isaiah Pola-Mao 	S	USC	  
Las Vegas Raiders	Luke Masterson 	LB	Wake Forest	  
Las Vegas Raiders	Sincere McCormick 	RB	UTSA	  
Las Vegas Raiders	Sam Webb 	CB	Missouri Western	  
Los Angeles Chargers	Stone Smartt 	TE	Old Dominion	  
Los Angeles Rams	Cameron Dicker †	K	Texas	  
Los Angeles Rams	Jake Hummel 	LB	Iowa State	  
Miami Dolphins	Kader Kohou 	CB	Texas A&M–Commerce	  
Minnesota Vikings	Ryan Wright 	P	Tulane	  
New England Patriots	Brenden Schooler †	S	Texas	  
New Orleans Saints	Abram Smith 	RB	Baylor	  
All-XFL Team 2023; drafted in 2023 XFL draft
</excerpt>
### Rank 4 of 192 — 0.48
<excerpt title="Photos: Meet the 2022 Las Vegas Raiders Draft Class">
# Photos: Meet the 2022 Las Vegas Raiders Draft Class
Skip to main content
Primary nav
*   News  
*   Team  
*   Schedule  
*   Multimedia  
*   Photos  
*   Raiderettes  
*   Community  
*   History  
*     
    *   Allegiant Stadium  
    *   Promotions  
    *   Fans  
    *   Fit  
    *   Raiders Foundation  
    *   Alumni Relations  
    *   Español  
    *   International  
    *   Connect With Us

*   TICKETS  
*   SHOP
Search
Open menu button Action related nav
*   Watch  
*   Tickets  
*   Shop  
*   My Account

*   Latest  
*   Purchase Photos  
*   Practice  
*   Gameday  
*   Top Shots  
*   Silver and Black and White  
*   177 Feet Up  
*   Cinema in Silver and Black  
*   Raiderettes  
*   Raiders on Instagram
Advertising
The picks are in and the 2022 Las Vegas Raiders Draft Class has been set. Check out photos of all six of the Silver and Black's newest rookies.
*     
*     
*   [](mailto:?subject=Photos:%20Meet%20the%202022%20Las%20Vegas%20Raiders%20Draft%20Class&body=https%3A%2F%2Fwww.raiders.com%2Fphotos%2Fphotos-meet-the-2022-raiders-draft-class-nfl "Send email")  
*   Copied!
1 / 6
**G Dylan Parham**
Third Round (90th overall)
Memphis
University of Memphis Athletics
2 / 6
**RB Zamir White**
Fourth Round (122th overall)
Georgia
John Bazemore/Associated Press
3 / 6
**DL Neil Farrell Jr.**
Fourth Round (126th overall)
LSU
Gerald Herbert/Associated Press
4 / 6
**DT Matthew Butler**
Fifth Round (175th overall)
Tennessee
Darron Cummings/Associated Press
5 / 6
**T Thayer Munford Jr.**
Seventh Round (238th overall)
Ohio State
Jay LaPrete/Associated Press
6 / 6

# Photos: Meet the 2022 Las Vegas Raiders Draft Class
**RB Brittain Brown**
Seventh Round (250th overall)
UCLA
Marcio Jose Sanchez/Associated Press
Advertising
This Ad will close in 3
Advertising
</excerpt>
### Rank 5 of 192 — 0.46
<excerpt title="2022 NFL draft">
Shook, Nick (August 31, 2021). "Vikings acquiring TE Chris Herndon from Jets in trade following Irv Smith Jr.'s knee injury". NFL.com. Retrieved August 31, 2021.  
Jump up to:  
 Smith, Eric (April 30, 2022). "New Vikings CB Akayleb Evans Ready to Learn From Patrick Peterson". NFL.com. Retrieved April 30, 2022.  
Jump up to:  
 Vashee, Rushil (April 30, 2022). "Panthers trade into 4th round, select LB Brandon Smith". USA Today.  
Jump up to:  
 Edwards, Levi (April 30, 2022). "Raiders trade up to No. 122, select RB Zamir White". Raiders.com.  
 Nogle, Kevin (May 1, 2021). "2021 NFL Draft: Texans Trade Recap". The Phinsider. Retrieved September 4, 2021.  
Jump up to:  
 Edwards, Levi (April 30, 2022). "Defensive lineman Neil Farrell Jr. selected after Raiders trade up to No. 126".  
 "2021 NFL Draft trade tracker: Full details of every move". NFL.com. April 29, 2021. Retrieved May 5, 2021.  
 McClain, John (April 9, 2020). "Texans acquire Brandin Cooks in trade with Rams". Texas Sports Nation. Houston Chronicle. Retrieved April 26, 2020.  
 "2021 NFL Draft: Texans Trade Recap". Houston Texans. April 30, 2021. Retrieved September 4, 2021.  
Jump up to:  
 Risdon, Jeff (September 1, 2021). "Full details of the Trinity Benson trade between the Lions and Broncos". Yahoo! Sports. Retrieved September 4, 2021.  
Jump up to:  
 Goldman, Charles (April 30, 2022). "Chiefs trade up with Seahawks for Kentucky OT Darian Kinnard at pick No. 145". USA Today.  
Jump up to:
</excerpt>

## Search 8 — query: "Raiders 2022 draft picks SEC"
### Rank 1 of 140 — 0.62 (passed on)
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
### Rank 2 of 140 — 0.61
<excerpt title="2022 NFL draft">
Resolution JC-2A selection[g]
4	106	Tampa Bay Buccaneers	Cade Otton 	TE	Washington
from Jacksonville[R4 – 1]
4	107	Houston Texans	Dameon Pierce 	RB	Florida
from Detroit via Cleveland[R4 – 2]
4	108	Cleveland Browns	Perrion Winfrey 	DT	Oklahoma
from Houston[R4 – 3]
4	109	Seattle Seahawks	Coby Bryant 	CB	Cincinnati
from NY Jets[R4 – 4]
4	110	Baltimore Ravens	Daniel Faalele 	T	Minnesota
from NY Giants[R4 – 5]
4	111	New York Jets	Max Mitchell 	T	Louisiana
from Carolina[R4 – 6]
4	112	New York Giants	Daniel Bellinger 	TE	San Diego State
from Chicago[R4 – 7]
4	113	Washington Commanders	Percy Butler 	S	Louisiana	  
	4	114	New York Giants	Dane Belton 	S	Iowa
from Atlanta[R4 – 8]
4	115	Denver Broncos	Damarri Mathis 	CB	Pittsburgh	  
	4	116	Denver Broncos	Eyioma Uwazurike 	DT	Iowa State
from Seattle[R4 – 9]
4	117	New York Jets	Micheal Clemons 	DE	Texas A&M
from Minnesota[R4 – 10]
4	118	Minnesota Vikings	Akayleb Evans 	CB	Missouri
from Cleveland[R4 – 11]
4	119	Baltimore Ravens	Jalyn Armour-Davis 	CB	Alabama	  
	4	120	Carolina Panthers	Brandon Smith 	LB	Penn State
from New Orleans via Washington[R4 – 12]
4	121	New England Patriots	Jack Jones 	CB	Arizona State
from Miami via Kansas City[R4 – 13]
4	122	Las Vegas Raiders	Zamir White 	RB	Georgia
from Indianapolis via Minnesota[R4 – 14]
</excerpt>
### Rank 3 of 140 — 0.58
<excerpt title="2022 NFL draft">
Mr. Irrelevant  
Notable undrafted playersedit  
Original NFL team	Player	Pos.	College	Notes  
Arizona Cardinals	Darrell Baker Jr. 	CB	Georgia Southern	  
Arizona Cardinals	Chandler Wooten 	LB	Auburn	  
Atlanta Falcons	Timmy Horne 	DT	Kansas State	  
Atlanta Falcons	Nate Landman 	LB	Colorado	  
Buffalo Bills	Alec Anderson 	T	UCLA	  
Buffalo Bills	Raheem Blackshear 	RB	Virginia Tech	  
Buffalo Bills	Ja'Marcus Ingram 	CB	Buffalo	  
Carolina Panthers	Arron Mosby 	LB	Fresno State	  
Chicago Bears	Jack Sanborn 	LB	Wisconsin	  
Chicago Bears	Jake Tonges 	TE	California	  
Chicago Bears	Jaylon Jones 	CB	Ole Miss	  
Cincinnati Bengals	Cal Adomitis 	LS	Pittsburgh	  
Cincinnati Bengals	Ben Brown 	C	Ole Miss	  
Cleveland Browns	D'Anthony Bell 	S	West Florida	  
Cleveland Browns	Brock Hoffman 	C	Virginia Tech	  
Dallas Cowboys	Brandon Aubrey †	K	Notre Dame	  
Played college soccer; drafted in 2022 USFL draft

Dallas Cowboys	Markquese Bell 	S	Florida A&M	  
Dallas Cowboys	Malik Davis 	RB	Florida	  
Denver Broncos	Brandon Johnson 	WR	UCF	  
Denver Broncos	Ja'Quan McMillian 	CB	East Carolina	  
Denver Broncos	Dondrea Tillman 	LB	IUP	  
Green Bay Packers	Tyler Goodson 	RB	Iowa	  
Houston Texans	Jake Hansen 	LB	Illinois	  
Houston Texans	Kurt Hinish 	DT	Notre Dame	  
Indianapolis Colts	Dallis Flowers 	CB	Pittsburg State	  
Indianapolis Colts	Ryan Van Demark 	T	UConn	  
Kansas City Chiefs	Mike Caliendo 	G	Western Michigan	  
Kansas City Chiefs	Jack Cochrane 	LB	South Dakota	  
Las Vegas Raiders	Isaiah Pola-Mao 	S	USC	  
Las Vegas Raiders	Luke Masterson 	LB	Wake Forest	  
Las Vegas Raiders	Sincere McCormick 	RB	UTSA	  
Las Vegas Raiders	Sam Webb 	CB	Missouri Western	  
Los Angeles Chargers	Stone Smartt 	TE	Old Dominion	  
Los Angeles Rams	Cameron Dicker †	K	Texas	  
Los Angeles Rams	Jake Hummel 	LB	Iowa State	  
Miami Dolphins	Kader Kohou 	CB	Texas A&M–Commerce	  
Minnesota Vikings	Ryan Wright 	P	Tulane	  
New England Patriots	Brenden Schooler †	S	Texas	  
New Orleans Saints	Abram Smith 	RB	Baylor	  
All-XFL Team 2023; drafted in 2023 XFL draft
</excerpt>
### Rank 4 of 140 — 0.57
<excerpt title="Photos: Meet the 2022 Las Vegas Raiders Draft Class">
# Photos: Meet the 2022 Las Vegas Raiders Draft Class
Skip to main content
Primary nav
*   News  
*   Team  
*   Schedule  
*   Multimedia  
*   Photos  
*   Raiderettes  
*   Community  
*   History  
*     
    *   Allegiant Stadium  
    *   Promotions  
    *   Fans  
    *   Fit  
    *   Raiders Foundation  
    *   Alumni Relations  
    *   Español  
    *   International  
    *   Connect With Us

*   TICKETS  
*   SHOP
Search
Open menu button Action related nav
*   Watch  
*   Tickets  
*   Shop  
*   My Account

*   Latest  
*   Purchase Photos  
*   Practice  
*   Gameday  
*   Top Shots  
*   Silver and Black and White  
*   177 Feet Up  
*   Cinema in Silver and Black  
*   Raiderettes  
*   Raiders on Instagram
Advertising
The picks are in and the 2022 Las Vegas Raiders Draft Class has been set. Check out photos of all six of the Silver and Black's newest rookies.
*     
*     
*   [](mailto:?subject=Photos:%20Meet%20the%202022%20Las%20Vegas%20Raiders%20Draft%20Class&body=https%3A%2F%2Fwww.raiders.com%2Fphotos%2Fphotos-meet-the-2022-raiders-draft-class-nfl "Send email")  
*   Copied!
1 / 6
**G Dylan Parham**
Third Round (90th overall)
Memphis
University of Memphis Athletics
2 / 6
**RB Zamir White**
Fourth Round (122th overall)
Georgia
John Bazemore/Associated Press
3 / 6
**DL Neil Farrell Jr.**
Fourth Round (126th overall)
LSU
Gerald Herbert/Associated Press
4 / 6
**DT Matthew Butler**
Fifth Round (175th overall)
Tennessee
Darron Cummings/Associated Press
5 / 6
**T Thayer Munford Jr.**
Seventh Round (238th overall)
Ohio State
Jay LaPrete/Associated Press
6 / 6

# Photos: Meet the 2022 Las Vegas Raiders Draft Class
**RB Brittain Brown**
Seventh Round (250th overall)
UCLA
Marcio Jose Sanchez/Associated Press
Advertising
This Ad will close in 3
Advertising
</excerpt>
### Rank 5 of 140 — 0.56
<excerpt title="2022 NFL draft">
Dallas Cowboys	Markquese Bell 	S	Florida A&M	  
Dallas Cowboys	Malik Davis 	RB	Florida	  
Denver Broncos	Brandon Johnson 	WR	UCF	  
Denver Broncos	Ja'Quan McMillian 	CB	East Carolina	  
Denver Broncos	Dondrea Tillman 	LB	IUP	  
Green Bay Packers	Tyler Goodson 	RB	Iowa	  
Houston Texans	Jake Hansen 	LB	Illinois	  
Houston Texans	Kurt Hinish 	DT	Notre Dame	  
Indianapolis Colts	Dallis Flowers 	CB	Pittsburg State	  
Indianapolis Colts	Ryan Van Demark 	T	UConn	  
Kansas City Chiefs	Mike Caliendo 	G	Western Michigan	  
Kansas City Chiefs	Jack Cochrane 	LB	South Dakota	  
Las Vegas Raiders	Isaiah Pola-Mao 	S	USC	  
Las Vegas Raiders	Luke Masterson 	LB	Wake Forest	  
Las Vegas Raiders	Sincere McCormick 	RB	UTSA	  
Las Vegas Raiders	Sam Webb 	CB	Missouri Western	  
Los Angeles Chargers	Stone Smartt 	TE	Old Dominion	  
Los Angeles Rams	Cameron Dicker †	K	Texas	  
Los Angeles Rams	Jake Hummel 	LB	Iowa State	  
Miami Dolphins	Kader Kohou 	CB	Texas A&M–Commerce	  
Minnesota Vikings	Ryan Wright 	P	Tulane	  
New England Patriots	Brenden Schooler †	S	Texas	  
New Orleans Saints	Abram Smith 	RB	Baylor	  
All-XFL Team 2023; drafted in 2023 XFL draft

New Orleans Saints	John Parker Romo 	K	Virginia Tech	  
New Orleans Saints	Lucas Krull 	TE	Pittsburgh	  
New Orleans Saints	Nephi Sewell 	LB	Utah	  
New Orleans Saints	Rashid Shaheed †	WR	Weber State	  
New Orleans Saints	Daniel Whelan 	P	UC Davis	  
New York Jets	Tony Adams 	S	Illinois	  
New York Jets	Zonovan Knight 	RB	NC State	  
Philadelphia Eagles	Josh Blackwell 	CB	Duke	  
Philadelphia Eagles	Reed Blankenship 	S	Middle Tennessee	  
Philadelphia Eagles	Britain Covey 	WR	Utah	  
Philadelphia Eagles	Josh Jobe 	CB	Alabama	  
Pittsburgh Steelers	Jaylen Warren 	RB	Oklahoma State	  
San Francisco 49ers	Jordan Mason 	RB	Georgia Tech	  
Tampa Bay Buccaneers	Dylan Cook 	T	Montana	  
Tennessee Titans	Tre Avery 	CB	Rutgers	  
Tennessee Titans	Julius Chestnut 	RB	Sacred Heart	  
Tennessee Titans	Jack Gibbens 	LB	Minnesota	  
Tennessee Titans	Xavier Newman-Johnson 	G	Baylor	  
Tennessee Titans	Ryan Stonehouse 	P	Colorado State	  
Tradesedit
(PD) indicates trades completed prior to the start of the draft (i.e. Pre-Draft), while (D) denotes trades which took place during the 2022 draft.
Round 1
</excerpt>

## Search 9 — query: "site:drafthistory.com 2022 NFL draft Raiders team"
### Rank 1 of 155 — 0.36 (passed on)
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
### Rank 2 of 155 — 0.33
<excerpt title="2022 NFL Draft Fourth Round">
## 2022 NFL Draft Fourth Round
##### By Chris Malumphy
| 4 | 17 | 122 | Zamir White | Raiders | RB | Georgia | Colts via Vikings |  
| 4 | 18 | 123 | Isaiah Spiller | Chargers | RB | Texas A&M |  |  
| 4 | 19 | 124 | Cade York | Browns | K | Louisiana State | Eagles via Texans |  
| 4 | 20 | 125 | Erik Ezukanma | Dolphins | WR | Texas Tech | Steelers |  
| 4 | 21 | 126 | Neil Farrell Jr. | Raiders | DT | Louisiana State |  |  
| 4 | 22 | 127 | Pierre Strong Jr. | Patriots | RB | South Dakota State |  |  
| 4 | 23 | 128 | Charlie Kolar | Ravens | TE | Iowa State | Cardinals |  
| 4 | 24 | 129 | Jake Ferguson | Cowboys | TE | Wisconsin |  |  
| 4 | 25 | 130 | Jordan Stout | Ravens | P | Penn State | Bills |  
| 4 | 26 | 131 | Hassan Haskins | Titans | RB | Michigan |  |  
| 4 | 27 | 132 | Romeo Doubs | Packers | WR | Nevada |  |  
| 4 | 28 | 133 | Jake Camarda | Buccaneers | P | Georgia |  |  
| 4 | 29 | 134 | Spencer Burford | 49ers | G | Texas-San Antonio |  |  
| 4 | 30 | 135 | Joshua Williams | Chiefs | CB | Fayetteville State |  |  
| 4 | 31 | 136 | Cordell Volson | Bengals | G | North Dakota State |  |  
| 4 | 32 | 137 | Bailey Zappe | Patriots | QB | Western Kentucky | Rams via Texans & Panthers |  
| 4 | 33 | 138 | Calvin Austin III | Steelers | WR | Memphis | compensatory |  

## 2022 NFL Draft Fourth Round
##### By Chris Malumphy
| 4 | 34 | 139 | Isaiah Likely | Ravens | TE | Coastal Carolina | compensatory |  
| 4 | 35 | 140 | Zach Tom | Packers | C | Wake Forest | compensatory |  
| 4 | 36 | 141 | Damarion Williams | Ravens | CB | Houston | compensatory |  
| 4 | 37 | 142 | Decobie Durant | Rams | CB | South Carolina State | compensatory |  
| 4 | 38 | 143 | Chigoziem Okonkwo | Titans | TE | Maryland | compensatory |
</excerpt>
### Rank 3 of 155 — 0.31
<excerpt title="DraftHistory.com">
Bauer Sharp	6	4	185	TE	Louisiana State	Raiders	18.40  
Cardinals  
3-14-0 (0.176)  
Pts: 355 -- PA: 488  
Picks: 7 -- Value: 3170.30  
Name	Round	Pick	Player	Position	College	Source	Value  
Jeremiyah Love	1	3	3	RB	Notre Dame	 	2200.00  
Chase Bisontis	2	2	34	G	Texas A&M	 	560.00  
Carson Beck	3	1	65	QB	Miami (FL)	 	265.00  
Kaleb Proctor	4	4	104	DT	SE Louisiana	 	86.00  
Reggie Virgil	5	3	143	WR	Texas Tech	 	34.50  
Karson Sharar	6	2	183	LB	Iowa	 	19.20  
Jayden Williams	7	1	217	T	Mississippi	 	5.60  
Chargers  
11-6-0 (0.647)  
Pts: 368 -- PA: 340  
Picks: 8 -- Value: 1296.10  
Name	Round	Pick	Player	Position	College	Source	Value  
Akheem Mesidor	1	22	22	DE	Miami (FL)	 	780.00  
Jake Slaughter	2	31	63	G	Florida	Patriots	276.00  
Brenen Thompson	4	5	105	WR	Mississippi State	Giants via Browns	84.00  
Travis Burke	4	17	117	T	Memphis	Vikings via Jaguars, Raiders and Texans	60.00  
Genesis Smith	4	31	131	DB	Arizona	Patriots	41.00  
Nick Barrett	5	5	145	DT	South Carolina	Giants via Browns	33.50
</excerpt>
### Rank 4 of 155 — 0.30
<excerpt title="DraftHistory.com">
Keyshaun Elliott	5	26	166	LB	Arizona State	49ers via Eagles, Jaguars and Panthers	26.00  
Jordan van den Berg	6	32	213	DT	Georgia Tech	Seahawks via Jaguars, Lions and Bills	7.20  
Bengals  
6-11-0 (0.353)  
Pts: 414 -- PA: 492  
Picks: 7 -- Value: 823.60  
Name	Round	Pick	Player	Position	College	Source	Value  
Cashius Howell	2	9	41	DE	Texas A&M	 	490.00  
Tacario Davis	3	8	72	DB	Washington	 	230.00  
Connor Lew	4	28	128	G	Auburn	Texans via Lions and Jets	44.00  
Colbie Young	4	40	140	WR	Georgia	compensatory. Jets	36.00  
Brian Parker	6	8	189	C	Duke	 	16.80  
Jack Endries	7	5	221	TE	Texas	Giants via Cowboys	4.00  
Landon Robinson	7	10	226	DT	Navy	 	2.80  
Bills  
12-5-0 (0.706)  
Pts: 481 -- PA: 365  
Picks: 10 -- Value: 1071.80  
Name	Round	Pick	Player	Position	College	Source	Value  
T.J. Parker	2	3	35	DE	Clemson	Titans	550.00  
Davison Igbinosun	2	30	62	DB	Ohio State	Broncos	284.00  
Jude Bowry	4	2	102	T	Boston College	Raiders	92.00  
Skyler Bell	4	25	125	WR	Connecticut	Bears via Chiefs and Patriots	47.00
</excerpt>
### Rank 5 of 155 — 0.28
<excerpt title="DraftHistory.com">
Daylen Everette	3	21	85	DB	Georgia	 	165.00  
Gennings Dunker	3	32	96	G	Iowa	Seahawks	116.00  
Kaden Wetjen	4	21	121	WR	Iowa	 	52.00  
Riley Nowakowski	5	29	169	TE	Indiana	Rams via Chiefs	24.80  
Gabe Rubio	6	29	210	DE	Notre Dame	Rams via Chiefs	8.40  
Robert Spears-Jennings	7	8	224	DB	Oklahoma	Saints via Patriots	3.00  
Eli Heidenreich	7	14	230	WR	Navy	Colts	2.40  
Texans  
12-5-0 (0.706)  
Pts: 404 -- PA: 295  
Picks: 8 -- Value: 1728.40  
Name	Round	Pick	Player	Position	College	Source	Value  
Keylan Rutledge	1	26	26	G	Georgia Tech	Bills	700.00  
Kayden McDonald	2	4	36	DT	Ohio State	Raiders	540.00  
Marlin Klein	2	27	59	TE	Michigan	 	310.00  
Febechi Nwaiwu	4	6	106	G	Oklahoma	Commanders	82.00  
Wade Woodaz	4	23	123	LB	Clemson	Chargers	49.00  
Kamari Ramsey	5	1	141	DB	USC	Raiders via Browns	35.50  
Lewis Bond	6	23	204	WR	Boston College	Chargers	10.80  
Aiden Fisher	7	27	243	LB	Indiana	49ers	1.10  
Titans  
3-14-0 (0.176)  
Pts: 284 -- PA: 478
</excerpt>

## Search 10 — query: "drafthistory 2022 nfl draft 49ers"
### Rank 1 of 239 — 0.41 (passed on)
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
### Rank 2 of 239 — 0.35
<excerpt title="2022 NFL Draft by Position">
## 2022 NFL Draft by Position
##### By Chris Malumphy
| 3 | 29 | 93 | 49ers | Tyrion Davis-Price | Louisiana State | 128.00 |  |  
| 3 | 34 | 98 | Commanders | Brian Robinson | Alabama | 108.00 | Saints; compensatory |  
| 4 | 2 | 107 | Texans | Dameon Pierce | Florida | 80.00 | Lions via Browns |  
| 4 | 17 | 122 | Raiders | Zamir White | Georgia | 50.00 | Colts via Vikings |  
| 4 | 18 | 123 | Chargers | Isaiah Spiller | Texas A&M | 49.00 |  |  
| 4 | 22 | 127 | Patriots | Pierre Strong | South Dakota State | 45.00 |  |  
| 4 | 26 | 131 | Titans | Hassan Haskins | Michigan | 41.00 |  |  
| 5 | 8 | 151 | Falcons | Tyler Allgeier | Brigham Young | 31.00 |  |  
| 5 | 11 | 154 | Jaguars | Snoop Conner | Mississippi | 30.80 | Commanders via Eagles |  
| 5 | 13 | 156 | Browns | Jerome Ford | Cincinnati | 30.00 | Ravens via Vikings |  
| 5 | 21 | 164 | Rams | Kyren Williams | Notre Dame | 26.80 | Patriots via Raiders |  
| 5 | 26 | 169 | Vikings | Ty Chandler | North Carolina | 24.80 | Titans |  
| 6 | 4 | 183 | Patriots | Kevin Harris | South Carolina | 19.20 | Texans |  
| 6 | 17 | 196 | Ravens | Tyler Badie | Missouri | 14.00 | Dolphins |  
| 6 | 22 | 201 | Cardinals | Keaontay Ingram | USC | 12.00 |  |
</excerpt>
### Rank 3 of 239 — 0.33
<excerpt title="2022 NFL Draft by Position">
## 2022 NFL Draft by Position
##### By Chris Malumphy
| 2 | 6 | 38 | Falcons | Arnold Ebiketie | Penn State | 520.00 | Panthers via Jets |  
| 2 | 8 | 40 | Seahawks | Boye Mafe | Minnesota | 500.00 | Broncos |  
| 2 | 13 | 45 | Ravens | David Ojabo | Michigan | 450.00 |  |  
| 2 | 26 | 58 | Falcons | Troy Andersen | Montana State | 320.00 | Titans |  
| 2 | 29 | 61 | 49ers | Drake Jackson | USC | 292.00 |  |  
| 2 | 32 | 64 | Broncos | Nik Bonitto | Oklahoma | 270.00 | Rams |  
| 3 | 2 | 66 | Vikings | Brian Asamoah | Oklahoma | 260.00 | Lions |  
| 3 | 6 | 70 | Jaguars | Chad Muma | Wyoming | 240.00 | Panthers |  
| 3 | 11 | 75 | Texans | Christian Harris | Alabama | 215.00 | Broncos |  
| 3 | 18 | 82 | Falcons | DeAngelo Malone | Western Kentucky | 180.00 | Colts |  
| 3 | 19 | 83 | Eagles | Nakobe Dean | Georgia | 175.00 |  |  
| 3 | 25 | 89 | Bills | Terrel Bernard | Baylor | 145.00 |  |  
| 3 | 38 | 102 | Dolphins | Channing Tindall | Georgia | 92.00 | 49ers; special compensatory |  
| 3 | 39 | 103 | Chiefs | Leo Chenal | Wisconsin | 88.00 | special compensatory |  
| 4 | 15 | 120 | Panthers | Brandon Smith | Penn State | 54.00 | Saints via Commanders |
</excerpt>
### Rank 4 of 239 — 0.31
<excerpt title="San Francisco 49ers 2022 Draft Picks">
# DRAFT TRACKER 2022
## Team Draft Picks
RND
PICK
PLAYER
RND 2
PICK 29
(61)
PLAYER DRAKE JACKSON
EDGE USC JR Junior

# DRAFT TRACKER 2022
## Team Draft Picks
### PLAYER ANALYSIS
Jackson lacks play strength but has the frame to add muscle and mass. He's a loose-limbed, restless pass rusher with the activity level to find angles and openings in both his primary and secondary rush. However, he lacks successful counters to do it consistently against stronger tackles. Jackson also lacks the take-on toughness and functional anchor needed to hold up at the point on run downs. He has developmental rush potential, but needs a major upgrade in grit and technique against the run.
Go to Player Page
RND 3
PICK 29
(93)
PLAYER TYRION DAVIS-PRICE
RB LSU JR Junior
Big, athletic back offering an enticing blend of size and explosiveness to go with an SEC pedigree. Davis-Price's early season tape was listless and lacking pro quality, but that changed over the second half of the year. He's an enigmatic back featuring urgency, indecisiveness, physicality and finesse on any given carry. He got much better as the season progressed and clearly finds a rhythm when given volume carries. Scouts say that staying motivated will be a major factor in future success. Davis-Price's athletic ability and hammerhead finishes will help him create yardage. He has the size and upside worthy of consideration in the middle rounds.
Go to Player Page
RND 3
PICK 41
(105)
PLAYER DANNY GRAY
WR SMU SR Senior
SP COMP
Two-year starter on the FBS level with athleticism and play speed to project a continuing ascent at the next level. Gray stepped into a top playmaking role for SMU in 2021 and showed an ability to work all three levels of the field. His long, gliding strides separate from coverage on attack-oriented routes but he has the bend and agility to become a quality target working underneath. He needs to get a little stronger and limit the focus drops, but Gray has an inside/outside skill set with intriguing upside as a future WR3 with more work.
Go to Player Page
RND 4
PICK 29
(134)
PLAYER SPENCER BURFORD
G TEXAS-SAN ANTONIO SR Senior
</excerpt>
### Rank 5 of 239 — 0.27
<excerpt title="San Francisco 49ers 2022 Draft Picks">
# DRAFT TRACKER 2022
## Team Draft Picks
### PLAYER ANALYSIS
Jackson lacks play strength but has the frame to add muscle and mass. He's a loose-limbed, restless pass rusher with the activity level to find angles and openings in both his primary and secondary rush. However, he lacks successful counters to do it consistently against stronger tackles. Jackson also lacks the take-on toughness and functional anchor needed to hold up at the point on run downs. He has developmental rush potential, but needs a major upgrade in grit and technique against the run.
Go to Player Page
RND 3
PICK 29
(93)
PLAYER TYRION DAVIS-PRICE
RB LSU JR Junior
Big, athletic back offering an enticing blend of size and explosiveness to go with an SEC pedigree. Davis-Price's early season tape was listless and lacking pro quality, but that changed over the second half of the year. He's an enigmatic back featuring urgency, indecisiveness, physicality and finesse on any given carry. He got much better as the season progressed and clearly finds a rhythm when given volume carries. Scouts say that staying motivated will be a major factor in future success. Davis-Price's athletic ability and hammerhead finishes will help him create yardage. He has the size and upside worthy of consideration in the middle rounds.
Go to Player Page
RND 3
PICK 41
(105)
PLAYER DANNY GRAY
WR SMU SR Senior
SP COMP
Two-year starter on the FBS level with athleticism and play speed to project a continuing ascent at the next level. Gray stepped into a top playmaking role for SMU in 2021 and showed an ability to work all three levels of the field. His long, gliding strides separate from coverage on attack-oriented routes but he has the bend and agility to become a quality target working underneath. He needs to get a little stronger and limit the focus drops, but Gray has an inside/outside skill set with intriguing upside as a future WR3 with more work.
Go to Player Page
RND 4
PICK 29
(134)
PLAYER SPENCER BURFORD
G TEXAS-SAN ANTONIO SR Senior
</excerpt>

# Example 3
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

# Example 4
## Question
According to the Our World in Data website's Maddison Project Database, out of Albania, Algeria, Angola, and Argentina, which countries had an increase in GDP per capita from 1985 to 2022 of more than $8000?

## Expected answer
Albania, Algeria

## Grade 0.50

## Search 1 — query: "Albania GDP per capita 1985 2022 Our World in Data Maddison"
### Rank 1 of 119 — 0.22 (passed on)
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
### Rank 2 of 119 — 0.21
<excerpt title="List of regions by past GDP (PPP) per capita">
### 1–1800 (Maddison Project)
| Brazil |  |  |  |  |  |  |  |  |  |  |  | 867 | 1,084 | 1,046 | 1,465 | 1,610 | 3,398 | 6,086 | 8,952 | 14,034 |  
| Venezuela |  |  |  |  |  |  |  |  |  |  | 1,073 | 1,884 | 1,769 | 1,750 | 2,942 | 3,885 | 12,116 | 15,540 | 14,448 | 10,710 |  
| Chile |  |  |  |  |  |  |  |  |  |  | 853 | 1,352 | 1,868 | 4,836 | 5,679 | 5,083 | 6,781 | 7,911 | 13,716 | 22,105 |  
| Argentina |  |  |  |  |  |  |  |  |  |  | 1,484 | 1,994 | 2,340 | 6,052 | 6,961 | 6,575 | 6,575 | 12,691 | 13,086 | 18,556 |  
| South Africa |  |  |  |  |  |  |  |  | 2,715 | 2,071 | 1,529 | 1,042 | 1,286 | 1,835 | 3,249 | 3,249 | 4,847 | 6,655 | 6,406 | 12,166 |  

### 1–1800 (Maddison Project)
| Australia |  |  |  |  |  |  |  |  |  |  |  | 3,148 | 5,217 | 8,220 | 8,389 | 9,159 | 14,013 | 20,527 | 30,690 | 49,831 |  
|  |
The following estimates are taken exclusively from the 2007 monograph _Contours of the World Economy, 1–2030 AD_ by the British economist Angus Maddison.[[3]](https://en.wikipedia.org/wiki/List_of_regions_by_past_GDP_(PPP)_per_capita#cite_note-3)
GDP (PPP) per capita in 1990 international dollars
</excerpt>
### Rank 3 of 119 — 0.18
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
### Rank 4 of 119 — 0.16
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
### Rank 5 of 119 — 0.10
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

# Albania GDP: $16bn
## Key Indicators for Albania
AfghanistanAlbaniaAlgeriaAngolaArgentinaArmeniaAustraliaAustriaAzerbaijanBahamas, TheBahrainBangladeshBelarusBelgiumBeninBhutanBoliviaBosnia and HerzegovinaBotswanaBrazilBruneiBulgariaBurkina FasoBurundiCabo VerdeCambodiaCameroonCanadaCentral African RepublicChadChileChinaColombiaComorosCongo, Dem. RepCongo, Rep.Costa RicaCote d'IvoireCroatiaCyprusCzechiaDenmarkDominican RepublicEcuadorEgyptEl SalvadorEstoniaEswatiniEthiopiaFinlandFranceGabonGambiaGeorgiaGermanyGhanaGreeceGuatemalaGuineaGuinea-BissauGuyanaHaitiHondurasHong KongHungaryIcelandIndiaIndonesiaIrelandIsraelItalyJamaicaJapanJordanKazakhstanKenyaKorea, Rep.KuwaitKyrgyzstanLaosLatviaLebanonLesothoLiberiaLibyaLithuaniaLuxembourgMadagascarMalawiMalaysiaMaliMaltaMauritaniaMauritiusMexicoMoldovaMongoliaMoroccoMozambiqueMyanmarNamibiaNepalNetherlandsNew ZealandNicaraguaNigerNigeriaNorth MacedoniaNorwayOmanPakistanPanamaPapua New GuineaParaguayPeruPhilippinesPolandPortugalQatarRomaniaRussiaRwandaSaudi ArabiaSenegalSerbiaSierra LeoneSingaporeSlovak RepublicSloveniaSouth AfricaSpainSri LankaSudanSurinameSwedenSwitzerlandTaiwanTajikistanTanzaniaThailandTogoTrinidad and TobagoTunisiaTürkiyeTurkmenistanUgandaUkraineUnited Arab EmiratesUnited KingdomUnited StatesUruguayUzbekistanVietnamYemen, Rep.ZambiaZimbabweSee all countries by region
**ALBANIA'S ECONOMICS**
**GDP Size**
Gross Domestic Product (GDP)
Share of Global GDP
**GDP Growth**
GDP CAGR Growth
Share of Global Growth
**GDP Data Quality**
GDP - Quality Rating
Informal Economy Size
GDP Data Base Year
System of National Accounts
Statistical Resources Index
Governance Index
**Wealth**
Income & Asset Wealth per Capita
GDP Per Capita by Country
GDP Per Capita CAGR Growth
</excerpt>

## Search 2 — query: "Albania gdp per capita 1985 2022 Our World in Data Maddison"
### Rank 1 of 119 — 0.24 (passed on)
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
### Rank 2 of 119 — 0.21
<excerpt title="List of regions by past GDP (PPP) per capita">
### 1–1800 (Maddison Project)
| Brazil |  |  |  |  |  |  |  |  |  |  |  | 867 | 1,084 | 1,046 | 1,465 | 1,610 | 3,398 | 6,086 | 8,952 | 14,034 |  
| Venezuela |  |  |  |  |  |  |  |  |  |  | 1,073 | 1,884 | 1,769 | 1,750 | 2,942 | 3,885 | 12,116 | 15,540 | 14,448 | 10,710 |  
| Chile |  |  |  |  |  |  |  |  |  |  | 853 | 1,352 | 1,868 | 4,836 | 5,679 | 5,083 | 6,781 | 7,911 | 13,716 | 22,105 |  
| Argentina |  |  |  |  |  |  |  |  |  |  | 1,484 | 1,994 | 2,340 | 6,052 | 6,961 | 6,575 | 6,575 | 12,691 | 13,086 | 18,556 |  
| South Africa |  |  |  |  |  |  |  |  | 2,715 | 2,071 | 1,529 | 1,042 | 1,286 | 1,835 | 3,249 | 3,249 | 4,847 | 6,655 | 6,406 | 12,166 |  

### 1–1800 (Maddison Project)
| Australia |  |  |  |  |  |  |  |  |  |  |  | 3,148 | 5,217 | 8,220 | 8,389 | 9,159 | 14,013 | 20,527 | 30,690 | 49,831 |  
|  |
The following estimates are taken exclusively from the 2007 monograph _Contours of the World Economy, 1–2030 AD_ by the British economist Angus Maddison.[[3]](https://en.wikipedia.org/wiki/List_of_regions_by_past_GDP_(PPP)_per_capita#cite_note-3)
GDP (PPP) per capita in 1990 international dollars
</excerpt>
### Rank 3 of 119 — 0.19
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
### Rank 4 of 119 — 0.16
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
### Rank 5 of 119 — 0.11
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

# Albania GDP: $16bn
## Key Indicators for Albania
AfghanistanAlbaniaAlgeriaAngolaArgentinaArmeniaAustraliaAustriaAzerbaijanBahamas, TheBahrainBangladeshBelarusBelgiumBeninBhutanBoliviaBosnia and HerzegovinaBotswanaBrazilBruneiBulgariaBurkina FasoBurundiCabo VerdeCambodiaCameroonCanadaCentral African RepublicChadChileChinaColombiaComorosCongo, Dem. RepCongo, Rep.Costa RicaCote d'IvoireCroatiaCyprusCzechiaDenmarkDominican RepublicEcuadorEgyptEl SalvadorEstoniaEswatiniEthiopiaFinlandFranceGabonGambiaGeorgiaGermanyGhanaGreeceGuatemalaGuineaGuinea-BissauGuyanaHaitiHondurasHong KongHungaryIcelandIndiaIndonesiaIrelandIsraelItalyJamaicaJapanJordanKazakhstanKenyaKorea, Rep.KuwaitKyrgyzstanLaosLatviaLebanonLesothoLiberiaLibyaLithuaniaLuxembourgMadagascarMalawiMalaysiaMaliMaltaMauritaniaMauritiusMexicoMoldovaMongoliaMoroccoMozambiqueMyanmarNamibiaNepalNetherlandsNew ZealandNicaraguaNigerNigeriaNorth MacedoniaNorwayOmanPakistanPanamaPapua New GuineaParaguayPeruPhilippinesPolandPortugalQatarRomaniaRussiaRwandaSaudi ArabiaSenegalSerbiaSierra LeoneSingaporeSlovak RepublicSloveniaSouth AfricaSpainSri LankaSudanSurinameSwedenSwitzerlandTaiwanTajikistanTanzaniaThailandTogoTrinidad and TobagoTunisiaTürkiyeTurkmenistanUgandaUkraineUnited Arab EmiratesUnited KingdomUnited StatesUruguayUzbekistanVietnamYemen, Rep.ZambiaZimbabweSee all countries by region
**ALBANIA'S ECONOMICS**
**GDP Size**
Gross Domestic Product (GDP)
Share of Global GDP
**GDP Growth**
GDP CAGR Growth
Share of Global Growth
**GDP Data Quality**
GDP - Quality Rating
Informal Economy Size
GDP Data Base Year
System of National Accounts
Statistical Resources Index
Governance Index
**Wealth**
Income & Asset Wealth per Capita
GDP Per Capita by Country
GDP Per Capita CAGR Growth
</excerpt>

## Search 3 — query: "Albania 1985 gdp per capita Maddison Our World in Data"
### Rank 1 of 184 — 0.30 (passed on)
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
### Rank 2 of 184 — 0.21
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
### Rank 3 of 184 — 0.20
<excerpt title="List of regions by past GDP (PPP) per capita">
### 1–1800 (Maddison Project)
| Brazil |  |  |  |  |  |  |  |  |  |  |  | 867 | 1,084 | 1,046 | 1,465 | 1,610 | 3,398 | 6,086 | 8,952 | 14,034 |  
| Venezuela |  |  |  |  |  |  |  |  |  |  | 1,073 | 1,884 | 1,769 | 1,750 | 2,942 | 3,885 | 12,116 | 15,540 | 14,448 | 10,710 |  
| Chile |  |  |  |  |  |  |  |  |  |  | 853 | 1,352 | 1,868 | 4,836 | 5,679 | 5,083 | 6,781 | 7,911 | 13,716 | 22,105 |  
| Argentina |  |  |  |  |  |  |  |  |  |  | 1,484 | 1,994 | 2,340 | 6,052 | 6,961 | 6,575 | 6,575 | 12,691 | 13,086 | 18,556 |  
| South Africa |  |  |  |  |  |  |  |  | 2,715 | 2,071 | 1,529 | 1,042 | 1,286 | 1,835 | 3,249 | 3,249 | 4,847 | 6,655 | 6,406 | 12,166 |  

### 1–1800 (Maddison Project)
| Australia |  |  |  |  |  |  |  |  |  |  |  | 3,148 | 5,217 | 8,220 | 8,389 | 9,159 | 14,013 | 20,527 | 30,690 | 49,831 |  
|  |
The following estimates are taken exclusively from the 2007 monograph _Contours of the World Economy, 1–2030 AD_ by the British economist Angus Maddison.[[3]](https://en.wikipedia.org/wiki/List_of_regions_by_past_GDP_(PPP)_per_capita#cite_note-3)
GDP (PPP) per capita in 1990 international dollars
</excerpt>
### Rank 4 of 184 — 0.17
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
### Rank 5 of 184 — 0.12
<excerpt title="GDP per capita, 2025">
# GDP per capita 2025
## Select countries and regions
*    - [x]  Barbados   $22,127   
*    - [x]  Mexico   $21,912   
*    - [x]  Upper-middle-income countries   $21,749   
*    - [x]  Bosnia and Herzegovina   $21,178   
*    - [x]  Armenia   $21,153   
*    - [x]  Latin America and Caribbean (WB)   $20,287   
*    - [x]  Brazil   $20,025   
*    - [x]  Palau   $19,699   
*    - [x]  Saint Vincent and the Grenadines   $19,483   
*    - [x]  Dominica   $19,409   
*    - [x]  Suriname   $19,357   
*    - [x]  Turkmenistan   $19,314   
*    - [x]  Gabon   $18,986   
*    - [x]  Colombia   $18,779   
*    - [x]  Grenada   $18,241   
*    - [x]  Mongolia   $17,773   
*    - [x]  Botswana   $17,687   
*    - [x]  Egypt   $17,265   
*    - [x]  Paraguay   $17,246   
*    - [x]  Moldova   $17,087   
*    - [x]  Iran   $16,834   
*    - [x]  Bhutan   $16,744   
*    - [x]  Kosovo   $16,461   
*    - [x]  Ukraine   $16,155   
*    - [x]  Peru   $16,079   
*    - [x]  Algeria   $15,883   
*    - [x]  Vietnam   $15,457
</excerpt>

## Search 4 — query: "https://ourworldindata.org/grapher/gdp-per-capita-maddison-project-database.csv"
### Rank 1 of 103 — 0.25 (passed on)
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
### Rank 2 of 103 — 0.19
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
### Rank 3 of 103 — 0.18
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
### Rank 4 of 103 — 0.14
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
### Rank 5 of 103 — 0.13
<excerpt title="Gross domestic product (GDP)">
# Gross domestic product (GDP)2022
## Frequently asked questions
#### How did Our World in Data process this data?
All data and visualizations on Our World in Data rely on data sourced from one or several original data providers. Preparing this original data involves several processing steps. Depending on the data, this can include standardizing country names and world region definitions, converting units, calculating derived indicators such as per capita measures, as well as adding or adapting metadata such as the name or the description given to an indicator.
At the link below you can find a detailed description of the structure of our data pipeline, including links to all the code used to prepare data across Our World in Data.
Read about our data pipeline

# Gross domestic product (GDP)2022
## Frequently asked questions
#### How did Our World in Data process this data?
##### Notes on our processing step for this indicator
Estimates of GDP are not provided directly from the source, so we obtained them by multiplying GDP per capita by population.

# Gross domestic product (GDP)2022
## Data sources
#### Bolt and van Zanden – Maddison Project Database
The Maddison Project Database provides information on comparative economic growth and income levels over the very long run. The 2023 version of this database covers 169 countries and the period up to 2022. The new estimates are presented and discussed in Bolt and Van Zanden (2024), "Maddison style estimates of the evolution of the world economy: A new 2023 update", Journal of Economic Surveys, 1–41.
Retrieved on
April 26, 2024
Retrieved from
https://www.rug.nl/ggdc/historicaldevelopment/maddison/releases/maddison-project-database-2023
Citation
This is the citation of the original data obtained from the source, prior to any processing or adaptation by Our World in Data.
```  
Bolt, Jutta and Jan Luiten van Zanden (2024), "Maddison style estimates of the evolution of the world economy: A new 2023 update", Journal of Economic Surveys, 1–41. DOI: 10.1111/joes.12618.  
The Maddison Project Database builds on the efforts of many researchers who have carefully reconstructed historical data on economic growth and population for individual countries. You can find the full list of sources in the original dataset.  
```

# Gross domestic product (GDP)2022
## How to cite
#### How to cite this page
To cite this page overall, including any descriptions, FAQs or explanations of the data authored by Our World in Data, please use the following citation:
`“Data Page: Gross domestic product (GDP)”, part of the following publication: Max Roser, Bertha Rohenkohl, Pablo Arriagada, Joe Hasell, Hannah Ritchie, and Esteban Ortiz-Ospina (2023) - “Economic Growth”. Data adapted from Bolt and van Zanden. Retrieved from https://archive.ourworldindata.org/20261102-112946/grapher/gdp-maddison-project-database.html [online resource] (archived on November 2, 2026).`
</excerpt>

## Search 5 — query: "gdp-per-capita-maddison-project-database.csv"
### Rank 1 of 39 — 0.09 (passed on)
<excerpt title="Global average GDP per capita over the long run - Our World in Data">
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
### Rank 2 of 39 — 0.09
<excerpt title="Global average GDP per capita over the long run - Our World in Data">
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
### Rank 3 of 39 — 0.08
<excerpt title="GDP per capita in constant PPP dollars - Gapminder">
## **Summary documentation of v28**
### Sources
GDP per capita measures the value of everything produced in a country during a year, divided by the number of people. The unit is in international dollars, fixed to 2017 prices. The data is adjusted for inflation and differences in the cost of living between countries, known as PPP dollars.
In more recent years, between 1990 and 2019, we usethe GDP per capita data from the World Bank, published in May 2022 in their World Development Indicators. Before the World Bank series starts in 1990, we have used several sources:
Maddison Project Database: The Maddison Project was started in March 2010 by a group of Angus Maddison’s close colleagues, with the aim of supporting an effective cooperation between scholars to continue Maddison’s work on measuring economic performance for different regions, time periods and subtopics. The MPD built on Maddison’s original dataset. The original estimates are kept intact, and only revised or adjusted when there is more and better information available. Currently, the database is maintained and improved by the Groningen Growth and Development Centre.We have used the data in their 2020 versionwhich provides information on comparative economic growth and income levels over a very long period. The 2020 version covers 169 countries and the period up to 2018.
Penn World Table: We use data from the Penn World Table version 10.0 of the Groningen Growth and Development Centre, which is a platform for research on economic growth and development.PWT version 10.0 is a database with information on relative levels of income, output, input, and productivity, covering 13 countries between 1950 and 2019.
Gapminder v27: This is the previous version of GDP per capita published by Gapminder, and which was based on World Bank, IMF, and historical time series from the Maddison Database Project 2018 version, PWT 9.1 and GM-GDP per Capita v14 (documented and detailed based on multiple sources but mostly based on Agnus Maddison). For more details on previous versions, see the documentations below. We use GM-GDP per Capita v27 for the historical time series which are not available in the Maddison Project database or Penn World Table.
</excerpt>
### Rank 4 of 39 — 0.08
<excerpt title="GDP per capita in constant PPP dollars - Gapminder">
## **Summary documentation of v28**
### How were the sources combined?
We first updated our historical estimates based on the new data released by the Maddison Project Database (MPD) and Penn World Table (PWT). We used MPD data wherever data is available. Otherwise, we used PWT estimates.
In general, we connected Gapminder historical data in version 27 to MPD/ PWT data and adjusted the data based on the earliest available year with data in MPD or PWT. We made an exception for countries with MPD data available for the year 1820 or earlier, where we then used MPD data without any adjustment.
After, we connected the historical estimates to World Bank data by smoothly transitioning our historic trend over a period of 30 years to reach World Bank data for the first year it is available.
That describes the principle followed for most countries, but then we made exceptions in 31 cases where we preferred the following adjustments: (i) to use Gapminder’s series instead of MPD for the period 1800 to the start of WB data as the MPD data were mostly interpolated series and this makes events in single years not showing up as dips or peaks in single years. (ii) To move smoothly between GM/PWT and MPD in case the discrepancy between the estimates in the sources was large or (iii) To use MPD/PWT series instead of WB for some years.
Our data continues into the future up to 2027, based on forecasts from theIMF, in their World Economic Outlook 2022, April edition. We have applied the IMF expected changes rates on WB estimates. Beyond that point we have extended the series up to 2050. Economic forecasts are never very reliable, and we do these projections only to visualize an “if-then-scenario”. If the current trends for each country continued up to 2027, and if all countries at the end of the IMF’s forecast will converge to a common global (and modest) growth rate of 2% per year, then what would the world look like? Answering this question visually helps us show how much richer the world would become even with a modest growth rate. We’re not claiming that this is what will happen.

## **Summary documentation of v27**
### Sources
**Data » Online spreadsheet with data for countries, regions and global total — v27**
GDP per capita measures the value of everything produced in a country during a year, divided by the number of people. The unit is in international dollars, fixed to 2017 prices. The data is adjusted for inflation and differences in the cost of living between countries, known as PPP dollars.
In more recent years, between 1990 and 2019, we usethe GDP per capita data from the World Bank, published in March 2021 in their World Development Indicators. Before the World Bank series starts in 1990, we have used several sources:
Maddison Project Database: The Maddison Project was started in March 2010 by a group of Angus Maddison’s close colleagues, with the aim of supporting an effective cooperation between scholars to continue Maddison’s work on measuring economic performance for different regions, time periods and subtopics. The MPD built on Maddison’s original dataset. The original estimates are kept intact, and only revised or adjusted when there is more and better information available. Currently, the database is maintained and improved by the Groningen Growth and Development Centre.We have used the data in their 2020 versionwhich provides information on comparative economic growth and income levels over a very long period. The 2020 version covers 169 countries and the period up to 2018.
Penn World Table: We use data from the Penn World Table version 10.0 of the Groningen Growth and Development Centre, which is a platform for research on economic growth and development.PWT version 10.0 is a database with information on relative levels of income, output, input, and productivity, covering 13 countries between 1950 and 2019.
</excerpt>
### Rank 5 of 39 — 0.08
<excerpt title="GDP per capita in constant PPP dollars - Gapminder">
Gapminder uses cookies to improve its statistics and user experience. By continuing to use the site you agree to our cookie policy. X Close
_Documentation — version 32_
**Data » Online spreadsheet with data for countries, regions and global total — v32 (PPP$2021)**

## **SUMMARY DOCUMENTATION OF V32**
### **Sources**
GDP per capita measures the value of everything produced in a country during a year, divided by the number of people. The unit is constant dollars adjusted for inflation in 2021’s prices. As the cost of living varies across countries, we use a currency called “international dollars”, which is adjusted for Purchasing Power Parity(PPP). This is a virtual currency that enables better comparisons. Such a dollar would buy in each country a comparable amount of goods and services as a U.S. dollar would buy in the United States. GDP per capita is the GDP divided by the population of the country, which gives a rough estimate of the average annual income of the citizens.
**Sources:**
Gapminder’s long GDP per capita series covers the period from 1800 up to the present year. These long series are produced by combining multiple different data sources.
**Period 1990 to 2024:**In more recent years, between 1990 and 2024, our series are identical to the GDP per capita data from the World Bank, published in July 2025 in their World Development Indicators. Before the World Bank series starts in 1990, we have used the following sources:
**Period 1820 to 1990:**The Maddison Project Database is based on Maddison’s original dataset with rough estimates of historical GDP per capita for most countries, maintained and improved by the Groningen Growth and Development Centre. We used the data in their 2023 version which provides information on comparative economic growth and income levels over a very long period. The 2023 version covers 169 countries and the period up to 2022. We use these numbers up to the first year with data from the World Bank (for most countries it’s usually 1990). When the two series are not matching, we bridge between the two series over a long period of decades to avoid introducing an artificial jump in the trend when shifting sources.

## **SUMMARY DOCUMENTATION OF V32**
### **Sources**
**Period 1950 to 2019:**In a few cases where neither World Bank nor Maddison have data, we fall back on estimates from the Penn World Table. We use data from the version PWT version 10.01 of the Groningen Growth and Development Centre, which is a platform for research on economic growth and development, covering 183 countries between 1950 and 2019. When shifting between sources we smooth the transition to avoid artificial trend-jumps.
**Gapminder’s additional estimates:**Whenever the above sources are missing we rely on the historic estimates we made in a previous version of this indicator: Gapminder GDP Per Capita v26. Most of these historic estimates haven’t been revised since they were produced and documented by Mattias Lindgren in version 14 in 2011: GM-GDP per Capita v14. In additional to these older estimates by Gapminder, we have produced some new estimates for countries that are currently undergoing crisis, like Afghanistan, Belarus, Burundi, Cuba, Guyana, Lebanon, Liechtenstein, Moldova, Monaco, North Korea, Russia, Syria, Ukraine, Venezuela, and Yemen.
</excerpt>

## Search 6 — query: "https://ourworldindata.org/grapher/gdp-per-capita-maddison-project-database.csv"
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
<excerpt title="untitled">

</excerpt>
### Rank 5 of 113 — 0.14
<excerpt title="untitled">

</excerpt>

## Search 7 — query: "gdp-per-capita-maddison-project-database.csv"
### Rank 1 of 39 — 0.09 (passed on)
<excerpt title="untitled">
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
### Rank 2 of 39 — 0.09
<excerpt title="untitled">

</excerpt>
### Rank 3 of 39 — 0.08
<excerpt title="untitled">

</excerpt>
### Rank 4 of 39 — 0.08
<excerpt title="untitled">

</excerpt>
### Rank 5 of 39 — 0.08
<excerpt title="untitled">

</excerpt>

## Search 8 — query: "gdp-per-capita-maddison-project-database.csv?download-format=csv"
### Rank 1 of 25 — 0.08 (passed on)
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
### Rank 2 of 25 — 0.08
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
### Rank 3 of 25 — 0.07
<excerpt title="Input data set: Historical country-level Gross Domestic Product (GDP)">
# Input data set: Historical country-level Gross Domestic Product (GDP)
Geiger, T., & Frieler, K. (2017). Continuous national Gross Domestic Product (GDP) time series for 195 countries: past observations (1850-2005) harmonized with future projections according to the Shared Socio-economic Pathways (2006-2100). https://doi.org/10.5880/PIK.2017.003
See also the DOI entry: http://pmd.gfz-potsdam.de/pik/showshort.php?id=escidoc:2313888
References:
Feenstra, Robert C., Robert Inklaar and Marcel P. Timmer (2015), "The Next Generation of the Penn World Table" American Economic Review, 105(10), 3150-3182, available for download at www.ggdc.net/pwt
Maddison Project Database, version 2018. Bolt, Jutta, Robert Inklaar, Herman de Jong and Jan Luiten van Zanden (2018), “Rebasing ‘Maddison’: new income comparisons and the shape of long-run economic development”, Maddison Project Working paper 10, available for download at www.ggdc.net/maddison.
World Development Indicators, https://data.worldbank.org/indicator/NY.GDP.MKTP.PP.KD, accessed Dec 13, 2018
Caveats
In addition to caveats mentioned in the references of the previously available data, following additional caveats arise:
1) The assessment of national GDP data between 2006 and 2016 by the different institutions can differ, despite data being reported in identical units.

2) For several countries either no or incomplete data is available beyond 2006. No data are available for countries with ISO codes [NCL, NRU, PYF, SOM]. Incomplete data are available for countries with ISO codes [ABW, BMU, CUB, ERI, PSE].
Download Instructions
For ISIMIP participants, these files are available for download on the DKRZ server using the path

# Input data set: Historical country-level Gross Domestic Product (GDP)
/work/bb0820/ISIMIP/ISIMIP2a/InputData/landuse_humaninfluences/gdp/
Data link
The data can be downloaded from the ISIMIP Repository: https://data.isimip.org/search/simulation_round/ISIMIP2a/subcategory/gdp/resolution/national/
**Cookies disclaimer** Our site saves small pieces of text information (cookies) on your device in order to deliver better content and for statistical purposes. You can disable the usage of cookies by changing the settings of your browser. By browsing our website without changing the browser settings you grant us permission to store that information on your device. Read more I agree
*   ISIMIP mailing lists  
*   Supporters  
*   News  
*   Impressum & Privacy  
*   Login
* * *
Website consultancy, design and implementation:
Matthias Brück brueck.io
Except where otherwise noted, content on this site is licensed under a Creative Commons Attribution 4.0 International license.
</excerpt>
### Rank 4 of 25 — 0.07
<excerpt title="Global average GDP per capita over the long run">
# Global average GDP per capita over the long run
## Sources and processing
### This data is based on the following sources
#### Eurostat, OECD, IMF, and World Bank – World Development Indicators
```  
International Comparison Program (ICP), World Bank (WB), uri: https://www.worldbank.org/en/programs/icp/data, note: This information is for ICP’s PPPs utilized in WDI, publisher: International Comparison Program (ICP), date accessed: May 30, 2024, date published: May 30, 2024;  
The Eurostat PPP Programme, Eurostat (ESTAT), uri: https://ec.europa.eu/eurostat/databrowser/explore/all/all_themes, publisher: Eurostat;  
The OECD PPP Programme, Organisation for Economic Co-operation and Development (OECD), uri: https://data-explorer.oecd.org/, publisher: OECD;  
Staff estimates, World Bank (WB);  
National Accounts data files, Organisation for Economic Co-operation and Development (OECD);  
World Economic Outlook database, International Monetary Fund (IMF). Indicator NY.GDP.PCAP.PP.KD (https://data.worldbank.org/indicator/NY.GDP.PCAP.PP.KD). World Development Indicators – World Bank (2026). Accessed on 2026-07-27.  
```

# Global average GDP per capita over the long run
## Sources and processing
### This data is based on the following sources
#### Bolt and van Zanden – Maddison Project Database
The Maddison Project Database provides information on comparative economic growth and income levels over the very long run. The 2023 version of this database covers 169 countries and the period up to 2022. The new estimates are presented and discussed in Bolt and Van Zanden (2024), "Maddison style estimates of the evolution of the world economy: A new 2023 update", Journal of Economic Surveys, 1–41.
Retrieved on
April 26, 2024
Retrieved from
https://www.rug.nl/ggdc/historicaldevelopment/maddison/releases/maddison-project-database-2023
Citation
This is the citation of the original data obtained from the source, prior to any processing or adaptation by Our World in Data.To cite data downloaded from this page, please use the suggested citation given inReuse This Workbelow.
```  
Bolt, Jutta and Jan Luiten van Zanden (2024), "Maddison style estimates of the evolution of the world economy: A new 2023 update", Journal of Economic Surveys, 1–41. DOI: 10.1111/joes.12618.  
The Maddison Project Database builds on the efforts of many researchers who have carefully reconstructed historical data on economic growth and population for individual countries. You can find the full list of sources in the original dataset.  
```
The Maddison Project Database provides information on comparative economic growth and income levels over the very long run. The 2023 version of this database covers 169 countries and the period up to 2022. The new estimates are presented and discussed in Bolt and Van Zanden (2024), "Maddison style estimates of the evolution of the world economy: A new 2023 update", Journal of Economic Surveys, 1–41.
Retrieved on
April 26, 2024
Retrieved from
https://www.rug.nl/ggdc/historicaldevelopment/maddison/releases/maddison-project-database-2023
Citation
</excerpt>
### Rank 5 of 25 — 0.07
<excerpt title="Global average GDP per capita over the long run">
# Global average GDP per capita over the long run
## Sources and processing
### This data is based on the following sources
#### Bolt and van Zanden – Maddison Project Database
The Maddison Project Database provides information on comparative economic growth and income levels over the very long run. The 2023 version of this database covers 169 countries and the period up to 2022. The new estimates are presented and discussed in Bolt and Van Zanden (2024), "Maddison style estimates of the evolution of the world economy: A new 2023 update", Journal of Economic Surveys, 1–41.
Retrieved on
April 26, 2024
Retrieved from
https://www.rug.nl/ggdc/historicaldevelopment/maddison/releases/maddison-project-database-2023
Citation
This is the citation of the original data obtained from the source, prior to any processing or adaptation by Our World in Data.To cite data downloaded from this page, please use the suggested citation given inReuse This Workbelow.
```  
Bolt, Jutta and Jan Luiten van Zanden (2024), "Maddison style estimates of the evolution of the world economy: A new 2023 update", Journal of Economic Surveys, 1–41. DOI: 10.1111/joes.12618.  
The Maddison Project Database builds on the efforts of many researchers who have carefully reconstructed historical data on economic growth and population for individual countries. You can find the full list of sources in the original dataset.  
```
The Maddison Project Database provides information on comparative economic growth and income levels over the very long run. The 2023 version of this database covers 169 countries and the period up to 2022. The new estimates are presented and discussed in Bolt and Van Zanden (2024), "Maddison style estimates of the evolution of the world economy: A new 2023 update", Journal of Economic Surveys, 1–41.
Retrieved on
April 26, 2024
Retrieved from
https://www.rug.nl/ggdc/historicaldevelopment/maddison/releases/maddison-project-database-2023
Citation

# Global average GDP per capita over the long run
## Sources and processing
### This data is based on the following sources
#### Bolt and van Zanden – Maddison Project Database
This is the citation of the original data obtained from the source, prior to any processing or adaptation by Our World in Data.To cite data downloaded from this page, please use the suggested citation given inReuse This Workbelow.
```  
Bolt, Jutta and Jan Luiten van Zanden (2024), "Maddison style estimates of the evolution of the world economy: A new 2023 update", Journal of Economic Surveys, 1–41. DOI: 10.1111/joes.12618.  
The Maddison Project Database builds on the efforts of many researchers who have carefully reconstructed historical data on economic growth and population for individual countries. You can find the full list of sources in the original dataset.  
```
</excerpt>

## Search 9 — query: "https://ourworldindata.org/grapher/gdp-per-capita-maddison-project-database.csv?download-format=csv"
### Rank 1 of 94 — 0.23 (passed on)
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
### Rank 2 of 94 — 0.19
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
### Rank 3 of 94 — 0.19
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
### Rank 4 of 94 — 0.17
<excerpt title="GDP per capita, 2023">
# GDP per capita 2023
## Reuse this work
### Download
#### Data API
##### Metadata URL (JSON format)
`https://ourworldindata.org/grapher/gdp-per-capita-penn-world-table.metadata.json?v=1&csvType=full&useColumnShortNames=false`

# GDP per capita 2023
## Reuse this work
### Download
#### Code examples
Examples of how to load this data into different data analysis tools.

# GDP per capita 2023
## Reuse this work
### Download
#### Code examples
##### Excel / Google Sheets
`=IMPORTDATA("https://ourworldindata.org/grapher/gdp-per-capita-penn-world-table.csv?v=1&csvType=full&useColumnShortNames=false")`

# GDP per capita 2023
## Reuse this work
### Download
#### Code examples
##### Python with Pandas
```  
import pandas as pd  
import requests

# Fetch the data.  
df = pd.read_csv("https://ourworldindata.org/grapher/gdp-per-capita-penn-world-table.csv?v=1&csvType=full&useColumnShortNames=false", storage_options = {'User-Agent': 'Our World In Data data fetch/1.0'})

# Fetch the metadata  
metadata = requests.get("https://ourworldindata.org/grapher/gdp-per-capita-penn-world-table.metadata.json?v=1&csvType=full&useColumnShortNames=false").json()  
```

# GDP per capita 2023
## Reuse this work
### Download
#### Code examples
##### R
```  
library(jsonlite)

# Fetch the data  
df <- read.csv("https://ourworldindata.org/grapher/gdp-per-capita-penn-world-table.csv?v=1&csvType=full&useColumnShortNames=false")

# Fetch the metadata  
metadata <- fromJSON("https://ourworldindata.org/grapher/gdp-per-capita-penn-world-table.metadata.json?v=1&csvType=full&useColumnShortNames=false")  
```

# GDP per capita 2023
## Reuse this work
### Download
#### Code examples
##### Stata
`import delimited "https://ourworldindata.org/grapher/gdp-per-capita-penn-world-table.csv?v=1&csvType=full&useColumnShortNames=false", encoding("utf-8") clear`
Leave us feedback
**Have a question?** You may find an answer in **FAQs**.
Message
Your name
Email address Your name and email will only be used to reply to you and not for any other purpose. If you do not give a valid email, we will not be able to reply to you.
Send message

# GDP per capita 2023
## Reuse this work
### Download
#### Our World in Data is free and accessible for everyone.
Help us do this work by making a donation.
Donate now
Our World in Data is a project ofGlobal Change Data Lab, a nonprofit based in the UK (Reg. Charity No. 1186433). Our charts, articles, and data are licensed underCC BY, unless stated otherwise. The source code for our tools and software is made publicly available for transparency and educational reference under acustom license. Re-use requires permission. Third-party materials, including some charts and data, are subject to third-party licenses. See ourFAQs for more details.

# GDP per capita 2023
## Reuse this work
### Download
#### Our World in Data is free and accessible for everyone.
##### Explore
*   Topics  
*   Data  
*   Data Insights

# GDP per capita 2023
## Reuse this work
### Download
#### Our World in Data is free and accessible for everyone.
##### Resources
*   Latest  
*   SDG Tracker  
*   Teaching with OWID

# GDP per capita 2023
## Reuse this work
### Download
#### Our World in Data is free and accessible for everyone.
##### About
*   About us  
*   Organization  
*   Funding  
*   Team  
*   Jobs  
*   FAQs
</excerpt>
### Rank 5 of 94 — 0.17
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

## Search 10 — query: "https://ourworldindata.org/grapher/gdp-per-capita-maddison-project-database.csv"
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

# Example 5
## Question
According to the CDC, which state had the lowest death rate per 100,000 people for both COVID-19 and Influenza/Pneumonia in 2020?

## Expected answer
Vermont

## Grade 0.00

## Search 1 — query: "CDC lowest death rate per 100,000 2020 COVID-19 state lowest influenza pneumonia death rate per 100k 2020"
### Rank 1 of 57 — 0.57 (passed on)
<excerpt title="Statistics of the COVID-19 pandemic in the United States">
## Measuring case and mortality rates
### Weekly all-cause deaths
Provisional COVID-19 deaths in the United States by age as of April 11, 2023| Age group | Death count | % of deaths |  
| --- | --- | --- |  
| All ages | 1,125,044 | 100% |  
| Under 1y | 471 | <0.1% |  
| 1-4y | 258 | <0.1% |  
| 5-14y | 479 | <0.1% |  
| 15-24y | 2,970 | 0.3% |  
| 25-34y | 12,210 | 1% |  
| 35-44y | 29,787 | 3% |  
| 45-54y | 70,753 | 7% |  
| 55-64y | 157,966 | 15% |  
| 65-74y | 252,945 | 23% |  
| 75-84y | 293,622 | 26% |  
| 85y and over | 303,583 | 26% |  
|  |
Number of COVID-19 deaths by sex and age as of April 12, 2023:[[52]](https://en.wikipedia.org/wiki/Statistics_of_the_COVID-19_pandemic_in_the_United_States#cite_note-cdc-demo-52)
COVID-19 deaths per million of the populations of each state, along with the District of Columbia and Puerto Rico,[[53]](https://en.wikipedia.org/wiki/Statistics_of_the_COVID-19_pandemic_in_the_United_States#cite_note-RealClearPolitics-53) as of February 9, 2023:

## Measuring case and mortality rates
### Weekly all-cause deaths
Arizona had the highest rate of Covid-related deaths in the country (464 deaths per 100,000 people). West Virginia (462 per 100,000) and Mississippi (453 per 100,000) were the second and third worst states. Hawaii, on the other hand, had the lowest adjusted Covid death rate at 147 deaths per 100,000 people. It was followed by Vermont (149 per 100,000) and Utah (170 per 100,000).[[53]](https://en.wikipedia.org/wiki/Statistics_of_the_COVID-19_pandemic_in_the_United_States#cite_note-RealClearPolitics-53)

## Vaccine distribution
[edit]
Vaccinations in the U.S. per day:[[49]](https://en.wikipedia.org/wiki/Statistics_of_the_COVID-19_pandemic_in_the_United_States#cite_note-GH-OWID-49)
Cumulative vaccine doses administered in the U.S.[[49]](https://en.wikipedia.org/wiki/Statistics_of_the_COVID-19_pandemic_in_the_United_States#cite_note-GH-OWID-49)

## Number of U.S. positive test individuals by state over time
[edit]
Data for all state charts sourced from the NY Times COVID Data, as of January 3,2023.[[47]](https://en.wikipedia.org/wiki/Statistics_of_the_COVID-19_pandemic_in_the_United_States#cite_note-NY_Times_COVID_19_Dataset-47) (This reference tends to include confirmed and suspected cases. This leads to some disparity with other sources).

## Number of U.S. positive test individuals by state over time
### > 6,000,000 positive test individuals
[edit]
</excerpt>
### Rank 2 of 57 — 0.13
<excerpt title="Statistics of the COVID-19 pandemic in the United States">
## Number of U.S. positive test individuals by state over time
### <400,000 positive test individuals
At the start of January 2023, when the US death toll had accumulated to over 1,120,000, the IHME projected that the death toll would reach 1,130,000 by April 1.[[68]](https://en.wikipedia.org/wiki/Statistics_of_the_COVID-19_pandemic_in_the_United_States#cite_note-68)
Epidemics of similar size (the number is the U.S. death toll):
*   HIV/AIDS in the United States: 700,000 as of 2018[[69]](https://en.wikipedia.org/wiki/Statistics_of_the_COVID-19_pandemic_in_the_United_States#cite_note-69)  
*   1918 Spanish Flu: 675,000[[70]](https://en.wikipedia.org/wiki/Statistics_of_the_COVID-19_pandemic_in_the_United_States#cite_note-CDC_past-70)
Other large epidemics:
*   1957–1958 influenza pandemic: 116,000[[70]](https://en.wikipedia.org/wiki/Statistics_of_the_COVID-19_pandemic_in_the_United_States#cite_note-CDC_past-70)  
*   1968 Hong Kong flu: 100,000[[70]](https://en.wikipedia.org/wiki/Statistics_of_the_COVID-19_pandemic_in_the_United_States#cite_note-CDC_past-70)

## Number of U.S. positive test individuals by state over time
### <400,000 positive test individuals
1.   ↑COVID-19 Deaths per 100K. U.S. News & World Report. Run your cursor over the map to see the dates and data for each state. "The data on this page is courtesy of USAFacts – a nonprofit, nonpartisan civic initiative – and includes information from the Centers for Disease Control and Prevention and state and local health departments. See a detailed methodology at the USAFacts website."  
2.   ↑"Cases, Data, and Surveillance". Centers for Disease Control and Prevention. February 11, 2020. Retrieved December 19, 2021.  
3.   ↑Iuliano, A. Danielle; Chang, Howard H.; Patel, Neha N.; Threlkel, Ryan; Kniss, Krista; Reich, Jeremy; Steele, Molly; Hall, Aron J.; Fry, Alicia M.; Reed, Carrie (July 13, 2021). "Estimating Under-recognized COVID-19 Deaths, United States, March 2020-May 2021 using an Excess Mortality Modelling Approach". _The Lancet Regional Health - Americas_. **1** 100019. doi:10.1016/j.lana.2021.100019. ISSN2667-193X. PMC8275579. PMID34386789.  
4.   ↑"Excess Deaths Associated with COVID-19". Centers for Disease Control and Prevention—National Center for Health Statistics. Retrieved July 21, 2020.
</excerpt>
### Rank 3 of 57 — 0.11
<excerpt title="Statistics of the COVID-19 pandemic in the United States">
## Number of U.S. positive test individuals by state over time
### <400,000 positive test individuals
1.   ↑COVID-19 Deaths per 100K. U.S. News & World Report. Run your cursor over the map to see the dates and data for each state. "The data on this page is courtesy of USAFacts – a nonprofit, nonpartisan civic initiative – and includes information from the Centers for Disease Control and Prevention and state and local health departments. See a detailed methodology at the USAFacts website."  
2.   ↑"Cases, Data, and Surveillance". Centers for Disease Control and Prevention. February 11, 2020. Retrieved December 19, 2021.  
3.   ↑Iuliano, A. Danielle; Chang, Howard H.; Patel, Neha N.; Threlkel, Ryan; Kniss, Krista; Reich, Jeremy; Steele, Molly; Hall, Aron J.; Fry, Alicia M.; Reed, Carrie (July 13, 2021). "Estimating Under-recognized COVID-19 Deaths, United States, March 2020-May 2021 using an Excess Mortality Modelling Approach". _The Lancet Regional Health - Americas_. **1** 100019. doi:10.1016/j.lana.2021.100019. ISSN2667-193X. PMC8275579. PMID34386789.  
4.   ↑"Excess Deaths Associated with COVID-19". Centers for Disease Control and Prevention—National Center for Health Statistics. Retrieved July 21, 2020.  

## Number of U.S. positive test individuals by state over time
### <400,000 positive test individuals
5.   ↑Woolf, Steven H.; Chapman, Derek A.; Sabo, Roy T. (April 2, 2021). "Excess Deaths From COVID-19 and Other Causes in the US, March 1, 2020, to January 2, 2021". _JAMA_. **325** (17): 1786–1789. doi:10.1001/jama.2021.5199. PMC8019132. PMID33797550. S2CID232763669.  
6.   ↑Multiple sources:
</excerpt>
### Rank 4 of 57 — 0.07
<excerpt title="Statistics of the COVID-19 pandemic in the United States">
## Measuring case and mortality rates
### Weekly all-cause deaths
[edit]
Weekly predicted deaths, non-COVID excess, and COVID-related excess deaths in the U.S. based on CDC data as of April 10,2023 which is "Predicted (weighted)" (rather than tabulated) and commonly takes 60 days to fully collate.[[48]](https://en.wikipedia.org/wiki/Statistics_of_the_COVID-19_pandemic_in_the_United_States#cite_note-48) As such, the data are split and the fields indicated by (*) are not confirmed, including both the 60-day window and any data from the CDC that had numerical inconsistencies (e.g. predicted + excess ≠ observed.) Also, key actions and milestones in the progression of the outbreak are annotated, selectively drawn from COVID-19 pandemic in the United States: Timeline.
Daily hospital and ICU occupancy numbers, as of January 3,2023:[[49]](https://en.wikipedia.org/wiki/Statistics_of_the_COVID-19_pandemic_in_the_United_States#cite_note-GH-OWID-49)
Scatterplot showing the relationship between GDP per capita and the COVID-19 case fatality rate for individual countries in 2022.
Number of COVID-19 deaths by age as of April 11, 2023:[[50]](https://en.wikipedia.org/wiki/Statistics_of_the_COVID-19_pandemic_in_the_United_States#cite_note-CDCdeaths-50)[[51]](https://en.wikipedia.org/wiki/Statistics_of_the_COVID-19_pandemic_in_the_United_States#cite_note-51)

## Measuring case and mortality rates
### Weekly all-cause deaths
Provisional COVID-19 deaths in the United States by age as of April 11, 2023| Age group | Death count | % of deaths |  
| --- | --- | --- |  
| All ages | 1,125,044 | 100% |  
| Under 1y | 471 | <0.1% |  
| 1-4y | 258 | <0.1% |  
| 5-14y | 479 | <0.1% |  
| 15-24y | 2,970 | 0.3% |  
| 25-34y | 12,210 | 1% |  
| 35-44y | 29,787 | 3% |  
| 45-54y | 70,753 | 7% |  
| 55-64y | 157,966 | 15% |  
| 65-74y | 252,945 | 23% |  
| 75-84y | 293,622 | 26% |  
| 85y and over | 303,583 | 26% |  
|  |
Number of COVID-19 deaths by sex and age as of April 12, 2023:[[52]](https://en.wikipedia.org/wiki/Statistics_of_the_COVID-19_pandemic_in_the_United_States#cite_note-cdc-demo-52)
COVID-19 deaths per million of the populations of each state, along with the District of Columbia and Puerto Rico,[[53]](https://en.wikipedia.org/wiki/Statistics_of_the_COVID-19_pandemic_in_the_United_States#cite_note-RealClearPolitics-53) as of February 9, 2023:
</excerpt>
### Rank 5 of 57 — 0.07
<excerpt title="Provisional Mortality Data — United States, 2020 | MMWR">
### **Summary**
Age-adjusted death rates differed by race/ethnicity. Overall age-adjusted death rates were lowest among Asian (457.9 per 100,000 population) and Hispanic persons (724.1) and highest among Black (1,105.3) and AI/AN persons (1,024.0). COVID-19–associated death rates were lowest among multiracial (31.8) and Asian persons (66.7) and highest among AI/AN (187.8) and Hispanic persons (164.3). COVID-19 was listed as the underlying cause of 345,323 deaths during 2020 and was the third leading underlying cause of death, after heart disease (690,882 deaths) and cancer (598,932) (Figure 2).

## Discussion
During January–December 2020, the estimated 2020 age-adjusted death rate increased for the first time since 2017, with an increase of 15.9% compared with 2019, from 715.2 to 828.7 deaths per 100,000 population. COVID-19 was the underlying or a contributing cause of 377,883 deaths (91.5 deaths per 100,000). COVID-19 death rates were highest among males, older adults, and AI/AN and Hispanic persons. The highest numbers of overall deaths and COVID-19 deaths occurred during April and December. COVID-19 was the third leading underlying cause of death in 2020, replacing suicide as one of the top 10 leading causes of death (_6_).
The findings in this report are subject to at least four limitations. First, data are provisional, and numbers and rates might change as additional information is received. Second, timeliness of death certificate submission can vary by jurisdiction. As a result, the national distribution of deaths might be affected by the distribution of deaths from jurisdictions reporting later, which might differ from those in the United States overall. Third, certain categories of race (i.e., AI/AN and Asian) and Hispanic ethnicity reported on death certificates might have been misclassified (_7_), possibly resulting in underestimates of death rates for some groups. Finally, the cause of death for certain persons might have been misclassified. Limited availability of testing for SARS-CoV-2, the virus that causes COVID-19, at the beginning of the COVID-19 pandemic might have resulted in an underestimation of COVID-19–associated deaths.
This report provides an overview of provisional U.S. mortality data for 2020. Provisional death estimates can give researchers and policymakers an early indication of shifts in mortality trends and provide actionable information sooner than the final mortality data that are released approximately 11 months after the end of the data year. These data can guide public health policies and interventions aimed at reducing numbers of deaths that are directly or indirectly associated with the COVID-19 pandemic and among persons most affected, including those who are older, male, or from disproportionately affected racial/ethnic minority groups.
* * *
1 National Center for Health Statistics, CDC.

## Discussion
All authors have completed and submitted the International Committee of Medical Journal Editors form for disclosure of potential conflicts of interest. No potential conflicts of interest were disclosed.
* https://www.cdc.gov/nchs/nvss/deaths.htm
† Based on death records received and processed as of March 21, 2021, for deaths occurring in the United States among U.S. residents. Data included in this analysis include >99% of deaths that occurred in 2020.
§ At the time of analysis, 1.1% of total NVSS deaths and 0.6% of COVID-19 deaths that occurred in the United States were among residents of U.S. territories and foreign countries.
</excerpt>

## Search 2 — query: "CDC COVID-19 death rate 2020 per 100,000 state Hawaii 2020"
### Rank 1 of 108 — 0.81 (passed on)
<excerpt title="COVID-19 Mortality in Adults Aged 65 and Over: United States, 2020">
**Data from the National Vital Statistics System**
*   In 2020, the death rate for COVID-19 among adults aged 85 and over (1,645.0 per 100,000 population) was 2.8 times higher than the rate for ages 75–84 (589.8), and 7 times higher than that for ages 65–74 (234.3).  
*   Age-adjusted death rates for COVID-19 were higher for men than women for all race and Hispanic-origin groups among adults aged 65 and over.  
*   In 2020, age-adjusted death rates due to COVID-19 in the population aged 65 and over ranged from 90.5 in Hawaii to 872.0 in New Jersey.  
*   Among adults aged 85 and over, 38.9% of COVID-19 deaths occurred in a nursing home or long-term care facility compared with 19.2% among adults aged 75–84 and 9.7% among those aged 65–74.
COVID-19 was the underlying cause of death for a total of 350,381 deaths in the United States in 2020 (1). Although COVID-19 can affect people of any age, older adults were especially impacted during the first year of the pandemic: 81% of COVID-19 deaths in 2020 (282,836) occurred among those aged 65 and over. In this age group, COVID-19 was the third leading cause of death, after heart disease and cancer (1). This report describes COVID-19 mortality in 2020 by selected characteristics in the population aged 65 and over.
_Keywords: older adults, death rates, race and ethnicity, National Vital Statistics System_

### How did death rates for COVID-19 vary by age group and sex among adults aged 65 and over in 2020?
*   The COVID-19 age-adjusted death rate for the age 65 and over population was 533.5 per 100,000 standard population. The rate was 1.5 times higher for men (666.8) than women (433.0) (Figure 1).  
*   COVID-19 death rates were higher for men compared with women for all age groups: 65–74 (309.6 men, 168.5 women), 75–84 (757.5 men, 458.5 women), and 85 and over (1,925.3 men, 1,485.5 women).  
*   In 2020, the death rate for COVID-19 among those aged 65 and over increased with age. The rate for adults aged 85 and over (1,645.0) was 2.8 times higher than the rate for those aged 75–84 (589.8) and 7 times higher than that for age group 65–74 (234.3).
Figure 1. COVID-19 death rates for adults aged 65 and over, by age group and sex: United States, 2020
1 Significantly higher than rates for women for all age groups (_p_< 0.05).
2 Age-adjusted death rate per 100,000 standard population.
NOTE: Access data table for Figure 1.
SOURCE: National Center for Health Statistics, National Vital Statistics System, Mortality.
</excerpt>
### Rank 2 of 108 — 0.78
<excerpt title="COVID-19 mortality in adults aged 65 and over: United States, 2020">
## [PDF page 2]
1,200  1,228.1  
1,127.0  
1,040.2
900  
768.2  
664.7  683.1  
600  542.1  608.1  563.1
307.8  371.1  379.4  
300
0  
Hispanic2  American Indian  Asian3  Black2  White3  
or Alaska  Native2  Native Hawaiianor Other Pacific  
Islander
Non-Hispanic
1Higher than rates for women for all race and Hispanic-origin groups (p < 0.05).  
2Significantly different from all other race and Hispanic-origin groups (p < 0.05).  
3Significantly different from all other race and Hispanic-origin groups except Native Hawaiian or Other Pacific Islander (p < 0.05).  
NOTES: Data for specified categories other than non-Hispanic single-race White and non-Hispanic single-race Black should be interpreted with caution because of  
inconsistencies between reporting these items on death certificates and on censuses and surveys. Access data table for Figure 2 at: https://www.cdc.gov/nchs/  
data/databriefs/db446-tables.pdf#2.  
SOURCE: National Center for Health Statistics, National Vital Statistics System, Mortality.
■   2   ■
PDF link

## [PDF page 3]
●  Among women aged 65 and over, the highest COVID-19 death rate was for non-Hispanic  
AIAN women (768.2), followed by non-Hispanic Black (683.1) and Hispanic  
(664.7) women.
●  Rates were lowest for women among non-Hispanic White (379.4), non-Hispanic NHOPI  
(371.1), and non-Hispanic Asian (307.8) women, although the rate for non-Hispanic NHOPI  
women was not significantly different from the other two groups.
How did COVID-19 age-adjusted death rates for adults aged 65 and over  
vary by state in 2020?
●  Among the 50 states and the District of Columbia (D.C.), age-adjusted COVID-19 death  
rates in the population aged 65 and over ranged from 90.5 in Hawaii to 872.0 in New Jersey.  
The average U.S. rate was 533.5 (Figure 3).
●  The states with the highest COVID-19 age-adjusted death rates for adults aged 65 and over  
in 2020 were New Jersey (872.0), South Dakota (844.5), North Dakota (834.3), New York  
(831.9), Connecticut (772.8), and Rhode Island (729.1).
●  The states with the lowest COVID-19 age-adjusted death rates for adults aged 65 and over  
were Hawaii (90.5), Vermont (113.9), Maine (142.8), Oregon (170.8), Alaska (234.1), and  
Washington (242.3).
Figure 3. Age-adjusted death rates due to COVID-19 for adults aged 65 and over, by state: United States, 2020
</excerpt>
### Rank 3 of 108 — 0.77
<excerpt title="COVID-19 mortality in adults aged 65 and over: United States, 2020">
## [PDF page 1]
Key findings  COVID-19 was the underlying cause of death for a total of 350,381 deaths  
in the United States in 2020 (1). Although COVID-19 can affect people of  
Data from the National  any age, older adults were especially impacted during the first year of the  
Vital Statistics System  pandemic: 81% of COVID-19 deaths in 2020 (282,836) occurred among  
●  those aged 65 and over. In this age group, COVID-19 was the third leading  
In 2020, the death rate  cause of death, after heart disease and cancer (1). This report describes  
for COVID-19 among adults  COVID-19 mortality in 2020 by selected characteristics in the population aged  
aged 85 and over (1,645.0 per  65 and over.  
100,000 population) was 2.8  
times higher than the rate for  
ages 75–84 (589.8), and  How did death rates for COVID-19 vary by age group and sex  
7 times higher than that for  among adults aged 65 and over in 2020?  
ages 65–74 (234.3).  
●  Age-adjusted death rates  ●  The COVID-19 age-adjusted death rate for the age 65 and over  
for COVID-19 were higher for  population was 533.5 per 100,000 standard population. The rate was  
men than women for all race  1.5 times higher for men (666.8) than women (433.0) (Figure 1).  
and Hispanic-origin groups  
among adults aged 65 and over.  Figure 1. COVID-19 death rates for adults aged 65 and over, by age group and sex:  
United States, 2020  
●  In 2020, age-adjusted death  
rates due to COVID-19 in the  Total  Men1  Women  
population aged 65 and over  2,000  1,925.3  

## [PDF page 1]
ranged from 90.5 in Hawaii to  1,645.0  
872.0 in New Jersey.  1,485.5  
1,500  
●  Among adults aged 85 and  
over, 38.9% of COVID-19  
deaths occurred in a nursing  1,000  
home or long-term care facility  757.5  
compared with 19.2% among  666.8  589.8  
adults aged 75–84 and 9.7%  533.5  458.5  
500  433.0  
among those aged 65–74.  234.3 309.6  
168.5
0  
65 and over2  65–74  75–84  85 and over
1Significantly higher than rates for women for all age groups (p < 0.05).  
2Age-adjusted death rate per 100,000 standard population.  
NOTE: Access data table for Figure 1 at: https://www.cdc.gov/nchs/data/databriefs/db446-tables.pdf#1.  
SOURCE: National Center for Health Statistics, National Vital Statistics System, Mortality.
U.S. DEPARTMENT OF HEALTH AND HUMAN SERVICES  
Centers for Disease Control and Prevention  
National Center for Health Statistics
NCHS reports can be downloaded from: https://www.cdc.gov/nchs/products/index.htm.
PDF link  
PDF link
</excerpt>
### Rank 4 of 108 — 0.75
<excerpt title="COVID-19 mortality in adults aged 65 and over: United States, 2020">
## [PDF page 3]
●  Among women aged 65 and over, the highest COVID-19 death rate was for non-Hispanic  
AIAN women (768.2), followed by non-Hispanic Black (683.1) and Hispanic  
(664.7) women.
●  Rates were lowest for women among non-Hispanic White (379.4), non-Hispanic NHOPI  
(371.1), and non-Hispanic Asian (307.8) women, although the rate for non-Hispanic NHOPI  
women was not significantly different from the other two groups.
How did COVID-19 age-adjusted death rates for adults aged 65 and over  
vary by state in 2020?
●  Among the 50 states and the District of Columbia (D.C.), age-adjusted COVID-19 death  
rates in the population aged 65 and over ranged from 90.5 in Hawaii to 872.0 in New Jersey.  
The average U.S. rate was 533.5 (Figure 3).
●  The states with the highest COVID-19 age-adjusted death rates for adults aged 65 and over  
in 2020 were New Jersey (872.0), South Dakota (844.5), North Dakota (834.3), New York  
(831.9), Connecticut (772.8), and Rhode Island (729.1).
●  The states with the lowest COVID-19 age-adjusted death rates for adults aged 65 and over  
were Hawaii (90.5), Vermont (113.9), Maine (142.8), Oregon (170.8), Alaska (234.1), and  
Washington (242.3).
Figure 3. Age-adjusted death rates due to COVID-19 for adults aged 65 and over, by state: United States, 2020

## [PDF page 3]
WA  
VT  NH  ME  
MT  ND  
OR  MN  
ID  SD  WINY  
WY  MI  CT  RIMA  
NE  IA  PA  
NV  IN  OH  NJ  
UT  COILDE  
CA  WV  VA  MD  
KS  MO  KY  DC
TN  NC  
AZ  NM  OK  AR  SC
MS  AL  GA  
TX  LA
FL  
AK  728.7–872.0  
631.7–728.6  
U.S. rate for ages  512.6–631.6  
65 and over: 533.5  413.2–512.5  
HI  248.5–413.1  
90.5–248.4
NOTES: Rate ranges represent the distribution of death rates at the following percentiles: less than 10th, 10th to less than 25th, 25th to less than 50th, 50th to less  
than 75th, 75th to less than 90th, and 90th and above. Access data table for Figure 3 at: https://www.cdc.gov/nchs/data/databriefs/db446-tables.pdf#3.  
SOURCE: National Center for Health Statistics, National Vital Statistics System, Mortality.
■   3   ■
PDF link
</excerpt>
### Rank 5 of 108 — 0.75
<excerpt title="COVID-19 Mortality in Adults Aged 65 and Over: United States, 2020">
### How did age-adjusted COVID-19 death rates vary by race and ethnicity and sex among adults aged 65 and over in 2020?
NOTES: Data for specified categories other than non-Hispanic single-race White and non-Hispanic single-race Black should be interpreted with caution because of inconsistencies between reporting these items on death certificates and on censuses and surveys. Access data table for Figure 2.
SOURCE: National Center for Health Statistics, National Vital Statistics System, Mortality.

### How did COVID-19 age-adjusted death rates for adults aged 65 and over vary by state in 2020?
*   Among the 50 states and the District of Columbia (D.C.), age-adjusted COVID-19 death rates in the population aged 65 and over ranged from 90.5 in Hawaii to 872.0 in New Jersey. The average U.S. rate was 533.5 (Figure 3).  
*   The states with the highest COVID-19 age-adjusted death rates for adults aged 65 and over in 2020 were New Jersey (872.0), South Dakota (844.5), North Dakota (834.3), New York (831.9), Connecticut (772.8), and Rhode Island (729.1).  
*   The states with the lowest COVID-19 age-adjusted death rates for adults aged 65 and over were Hawaii (90.5), Vermont (113.9), Maine (142.8), Oregon (170.8), Alaska (234.1), and Washington (242.3).
Figure 3. Age-adjusted death rates due to COVID-19 for adults aged 65 and over, by state: United States, 2020
NOTES: Rate ranges represent the distribution of death rates at the following percentiles: less than 10th, 10th to less than 25th, 25th to less than 50th, 50th to less than 75th, 75th to less than 90th, and 90th and above. Access data table for Figure 3.
SOURCE: National Center for Health Statistics, National Vital Statistics System, Mortality.

### For adults aged 65 and over who died of COVID-19 in 2020, what was the percent distribution by place of death?
*   In 2020, 66.2% of deaths due to COVID-19 among adults aged 65 and over occurred in a healthcare setting compared with 24.3% in a nursing home or long-term care facility and 4.7% at home (Figure 4).  
*   The percentage of COVID-19 deaths that occurred in a healthcare setting decreased with age, from 82.8% among adults aged 65–74, to 72.0% among those aged 75–84, and 49.4% for those aged 85 and over.  
*   The percentage of COVID-19 deaths that took place in a nursing home or long-term care facility increased with age, from 9.7% among adults aged 65–74, to 19.2% among adults aged 75–84, and 38.9% among those aged 85 and over.  
*   The percentage of COVID-19 deaths that occurred at home was similar by age, with 4.9% for age groups 65–74 and 85 and over, and 4.4% among those aged 75–84.
Figure 4. Percent distribution of place of death for COVID-19 deaths in adults aged 65 and over: United States, 2020
1 Significant increasing trend by age (_p_< 0.05).
2 Significant decreasing trend by age (_p_< 0.05).
NOTES: Total may not sum to 100 due to rounding. Access data table for Figure 4.
SOURCE: National Center for Health Statistics, National Vital Statistics System, Mortality.
</excerpt>

## Search 3 — query: "site:cdc.gov "COVID-19 deaths per 100,000" state 2020"
### Rank 1 of 477 — 0.63 (passed on)
<excerpt title="COVID-19 Mortality | Stats of the States">
# COVID-19 Mortality
## Mortality rates
### COVID-19 deaths per 100,000 total population (age-adjusted mortality rate)
| Location Sort by Location in ascending order | Death Rate Sort by Death Rate in ascending order | Deaths Sort by Deaths in ascending order |  
| --- | --- | --- |  
| Alabama | 8.5 | 566 |  
| Alaska | 8.7 | 57 |  
| Arizona | 6.1 | 650 |  
| Arkansas | 9.1 | 361 |  
| California | 6.3 | 2,991 |  
| Colorado | 5.7 | 374 |  
| Connecticut | 8.1 | 418 |  
| Delaware | 9.5 | 141 |  
| District of Columbia | 5.6 | 39 |  
| Florida | 6.4 | 2,456 |  
| Georgia | 7.3 | 891 |  
| Hawaii | 5.9 | 141 |  
| Idaho | 6.3 | 148 |  
| Illinois | 6.3 | 1,029 |  
| Indiana | 8.2 | 703 |  
| Iowa | 7.9 | 357 |  
| Kansas | 8.4 | 319 |  
| Kentucky | 11.1 | 631 |  
| Louisiana | 6.7 | 377 |  
| Maine | 9.7 | 213 |  
| Maryland | 7.2 | 573 |  
| Massachusetts | 7.3 | 696 |  
| Michigan | 7.2 | 972 |  
| Minnesota | 6.9 | 528 |  
| Mississippi | 10.8 | 404 |  
| Missouri | 7.7 | 636 |  
| Montana | 8 | 127 |  
| Nebraska | 7.7 | 191 |  
| Nevada | 6.1 | 237 |  
| New Hampshire | 7.5 | 156 |  

# COVID-19 Mortality
## Mortality rates
### COVID-19 deaths per 100,000 total population (age-adjusted mortality rate)
| New Jersey | 7 | 880 |  
| New Mexico | 9 | 262 |  
| New York | 6.9 | 1,913 |  
| North Carolina | 8.4 | 1,136 |  
| North Dakota | 6.4 | 68 |  
| Ohio | 7.9 | 1,260 |  
| Oklahoma | 9.6 | 469 |  
| Oregon | 6.7 | 388 |  
| Pennsylvania | 8.2 | 1,564 |  
| Rhode Island | 6.4 | 101 |  
| South Carolina | 8.1 | 585 |  
| South Dakota | 8.8 | 105 |  
| Tennessee | 9 | 789 |  
| Texas | 6.2 | 1,901 |  
| Utah | 5.7 | 161 |  
| Vermont | 8 | 79 |  
| Virginia | 8.1 | 890 |  
| Washington | 6.8 | 627 |  
| West Virginia | 11.2 | 300 |  
| Wisconsin | 6.3 | 494 |  
| Wyoming | 9.4 | 72 |
Download Map (PNG)Download Data (CSV)
Skipped data table.
</excerpt>
### Rank 2 of 477 — 0.58
<excerpt title="COVID-19 Mortality | Stats of the States">
# COVID-19 Mortality
## Mortality rates
### COVID-19 deaths per 100,000 total population (age-adjusted mortality rate)
*   5.6 - 9.4  
*   9.4 - 16.8  
*   18.9 - 54.6  
*   54.6 - 87.1  
*   87.3 - 158.8
Skip Data Table
Data Table
Data table showing data for the United States Map figure.

# COVID-19 Mortality
## Mortality rates
### COVID-19 deaths per 100,000 total population (age-adjusted mortality rate)
| Location Sort by Location in ascending order | Death Rate Sort by Death Rate in ascending order | Deaths Sort by Deaths in ascending order |  
| --- | --- | --- |  
| Alabama | 8.5 | 566 |  
| Alaska | 8.7 | 57 |  
| Arizona | 6.1 | 650 |  
| Arkansas | 9.1 | 361 |  
| California | 6.3 | 2,991 |  
| Colorado | 5.7 | 374 |  
| Connecticut | 8.1 | 418 |  
| Delaware | 9.5 | 141 |  
| District of Columbia | 5.6 | 39 |  
| Florida | 6.4 | 2,456 |  
| Georgia | 7.3 | 891 |  
| Hawaii | 5.9 | 141 |  
| Idaho | 6.3 | 148 |  
| Illinois | 6.3 | 1,029 |  
| Indiana | 8.2 | 703 |  
| Iowa | 7.9 | 357 |  
| Kansas | 8.4 | 319 |  
| Kentucky | 11.1 | 631 |  
| Louisiana | 6.7 | 377 |  
| Maine | 9.7 | 213 |  
| Maryland | 7.2 | 573 |  
| Massachusetts | 7.3 | 696 |  
| Michigan | 7.2 | 972 |  
| Minnesota | 6.9 | 528 |  
| Mississippi | 10.8 | 404 |  
| Missouri | 7.7 | 636 |  
| Montana | 8 | 127 |  
| Nebraska | 7.7 | 191 |  
| Nevada | 6.1 | 237 |  
| New Hampshire | 7.5 | 156 |
</excerpt>
### Rank 3 of 477 — 0.55
<excerpt title="The Town-Level Prevalence of Chronic Lung Conditions and Death ...">
##  Tables
| Factor | Both states | Connecticut | Rhode Island | _t_ Statistic |  
| --- | --- | --- | --- | --- |  
| No. of communities | 208 | 169 | 39 | — |  
| **Variable** |  
| Population aged ≥65 y with asthma, % | 13.8 | 13.7 | 14.5 | −2.29 a |  
| Population aged ≥65 y with COPD, % | 21.2 | 20.9 | 22.2 | −1.69 |  
| COVID-19 death rates per 100,000 people | 200.2 | 196.9 | 214.4 | −0.53 |  
| **Characteristic** |  
| Total population, no. (SD) | 22,299 (26,832) | 21,192 (25,564) | 27,093 (31,679) | −1.24 |  
| Population aged ≥65 y, no. (SD) | 3,662 (3,591) | 3,477 (3,463) | 4,467 (4,051) | 1.56 |  
| Race and ethnicity of population aged ≥65 y, % |  
| African American | 2.9 | 3.2 | 1.7 | 1.40 |  
| Asian | 1.5 | 1.6 | 1.1 | 1.70 |  
| Hispanic/Latino | 2.9 | 2.9 | 2.8 | 0.11 |  
| Other b | 1.6 | 1.5 | 2.1 | −1.17 |  
| White | 93.9 | 93.6 | 95.2 | −1.05 |  
| Education of population aged ≥65 y, % |
</excerpt>
### Rank 4 of 477 — 0.53
<excerpt title="The Town-Level Prevalence of Chronic Lung Conditions and Death ...">
##  Tables
Table 1. Descriptive Statistics for Study Sample and Bivariate Analyses, by State, Study of Town-Level Prevalence of Chronic Lung Conditions and Death From COVID-19 Among Older Adults in Connecticut and Rhode Island

##  Tables
| Factor | Both states | Connecticut | Rhode Island | _t_ Statistic |  
| --- | --- | --- | --- | --- |  
| No. of communities | 208 | 169 | 39 | — |  
| **Variable** |  
| Population aged ≥65 y with asthma, % | 13.8 | 13.7 | 14.5 | −2.29 a |  
| Population aged ≥65 y with COPD, % | 21.2 | 20.9 | 22.2 | −1.69 |  
| COVID-19 death rates per 100,000 people | 200.2 | 196.9 | 214.4 | −0.53 |  
| **Characteristic** |  
| Total population, no. (SD) | 22,299 (26,832) | 21,192 (25,564) | 27,093 (31,679) | −1.24 |  
| Population aged ≥65 y, no. (SD) | 3,662 (3,591) | 3,477 (3,463) | 4,467 (4,051) | 1.56 |  
| Race and ethnicity of population aged ≥65 y, % |  
| African American | 2.9 | 3.2 | 1.7 | 1.40 |  
| Asian | 1.5 | 1.6 | 1.1 | 1.70 |  
| Hispanic/Latino | 2.9 | 2.9 | 2.8 | 0.11 |  
| Other b | 1.6 | 1.5 | 2.1 | −1.17 |  
| White | 93.9 | 93.6 | 95.2 | −1.05 |  
| Education of population aged ≥65 y, % |
</excerpt>
### Rank 5 of 477 — 0.38
<excerpt title="The Town-Level Prevalence of Chronic Lung Conditions and Death ...">
## Results
Across all towns in both states, the average rate of COVID-19 deaths per 100,000 people was 200.2 deaths per town (Table 1). The prevalence of asthma was 13.8%, and the prevalence of COPD was 21.2%. The average town population was 22,299 people and 3,662 people aged 65 years or older. Most of the overall sample was White (93.9%) and had attained some college (53.5%). Of the population aged 65 years or older, 23.5% had obesity and 10.1% had tobacco use disorder. In addition, 11.5% of the overall sample were not US born, 2.5% commuted to work using public transportation, and 6.0% of the population aged 65 years or older were living in poverty. The average household size was 2.5 people per home and did not differ across the 2 states. Finally, 19.7% of the overall sample lived in rural counties; 24.3% of the sample in Connecticut lived in rural counties, whereas Rhode Island had no rural counties (_P_< .001 for difference between 2 states).

## Results
Overall, the Connecticut sample was slightly more diverse, healthier, and wealthier than the Rhode Island sample. Connecticut had an average of 196.9 deaths per 100,000 people from COVID-19 per town (vs 214.4 in Rhode Island and 200.2 overall). In bivariate analyses, we found a significant difference in the prevalence of asthma among adults aged 65 years or older by state (Connecticut, 13.7%; Rhode Island, 14.5%) and in the overall sample (13.8%). Compared with Rhode Island, Connecticut had a lower rate of COPD (20.9%) and a higher rate of people aged 65 years or older with a graduate or professional degree (18.1%). The average town population aged 65 years or older in Connecticut (n = 3,477) was lower than in Rhode Island (n = 4,467) and overall (n = 3,662). We found a significant difference between states for rates of obesity and poverty; among residents aged 65 years or older, Connecticut had a lower prevalence of obesity (22.3%) and a lower rate of residents aged 65 years or older living in poverty (5.3%). Finally, Connecticut had a lower rate of non–US-born residents (9.0%).
Rhode Island had a higher prevalence than Connecticut of asthma (14.5%), COPD (22.2%), and obesity (28.3%) among people aged 65 years or older. Towns in Rhode Island had worse health, were poorer, older, and less educated than towns in Connecticut. In Rhode Island, of the population aged 65 years or older, 8.7% lived in poverty and 16.3% had less than a high school diploma. Finally, Rhode Island had more than twice as many non–US-born residents as Connecticut (22.4% vs 9.0%).
</excerpt>

## Search 4 — query: "CDC influenza pneumonia deaths per 100,000 2020 state"
### Rank 1 of 67 — 0.35 (passed on)
<excerpt title="Influenza and Pneumonia Deaths and Death Rates per 100000 Population">
# Locations
Vermont
Virginia
Washington
West Virginia
Wisconsin
Wyoming
48,139
6,506
41,627
956
101
855
70
14
56
1,009
134
875
670
80
590
5,535
578
4,957
381
97
284
716
66
650
173
22
151
48
N/A
42
3,093
421
2,672
1,297
181
1,116
250
22
228
171
44
127
1,936
175
1,761
953
137
816
533
94
439
459
59
400
740
124
616
634
94
540
222
40
182
727
96
631
1,058
179
879
1,405
230
1,175
490
122
368
701
80
621
1,045
137
908
135
35
100
296
50
246
556
79
477
177
36
141
1,235
131
1,104
390
46
344
4,153
425
3,728
1,704
266
1,438
101
21
80
1,790
244
1,546
679
106
573
346
97
249

# Locations
2,289
330
1,959
141
30
111
665
125
540
160
41
119
1,360
169
1,191
3,326
399
2,927
299
47
252
81
25
56
1,052
149
903
762
122
640
481
68
413
616
121
495
73
17
56

# Locations
## Data Table
To view data, please select some geographies from the sidebar.
</excerpt>
### Rank 2 of 67 — 0.24
<excerpt title="Influenza and Pneumonia Deaths and Death Rates per 100000 Population">
# Locations
## Influenza and Pneumonia Deaths and Death Rates per 100,000 Population
### 2021
| Tennessee | 1225 | 42 | 1183 | 14.9 | 0.5 | 14.4 |  
| Texas | 2938 | 78 | 2860 | 10.5 | 0.3 | 10.2 |  
| Utah | 215 | N/A | N/A | 8.1 | N/A | 8.1 |  
| Vermont | 38 | 0 | 38 | 4.5 | N/A | 4.5 |  
| Virginia | 963 | 15 | 948 | 9.7 | NSD | 9.5 |  
| Washington | 496 | N/A | N/A | 5.9 | N/A | 5.8 |  
| West Virginia | 413 | N/A | N/A | 16.5 | N/A | 16.5 |  
| Wisconsin | 550 | N/A | N/A | 7.5 | N/A | 7.4 |  
| Wyoming | 79 | N/A | N/A | 11.9 | N/A | 11.8 |

# Locations
## Influenza and Pneumonia Deaths and Death Rates per 100,000 Population
### Notes
Causes of death attributable to flu and pneumonia include ICD-10 Codes J09-J18. Causes of death attributable to influenza specifically include ICD-10 codes J09, J10.0, J10.1, J10.8, J11.0, J11.1, and J11.8. Causes of death attributable to pneumonia specifically include ICD-10 codes J12.0, J12.1, J12.2, J12.3, J12.8, J12.9, J13, J14, J15.0, J15.1, J15.2, J15.3, J15.4, J15.5, J15.6, J15.7, J15.8, J15.9, J16.0, J16.8, J18.0, J18.1, J18.2, J18.8, and J18.9. Rates presented in this data table represent rates per 100,000 population and are age-adjusted to the 2000 U.S. standard population age distribution. Since death rates are affected by the population composition of a given area, age-adjusted death rates should be used for comparisons between areas because they control for differences in population composition.

# Locations
## Influenza and Pneumonia Deaths and Death Rates per 100,000 Population
### Sources
Centers for Disease Control and Prevention, National Center for Health Statistics. Underlying Cause of Death 1999-2024 on CDC WONDER Online Database. Data are from the Multiple Cause of Death Files, 1999-2024, as compiled from data provided by the 57 vital statistics jurisdictions through the Vital Statistics Cooperative Program. Accessed at https://wonder.cdc.gov/ucd-icd10-expanded.html on February 18, 2026.

# Locations
## Influenza and Pneumonia Deaths and Death Rates per 100,000 Population
### Definitions
**N/A**: Data not available due to suppression constraints. Please click here for further details. **NSD**: Not sufficient data. Figure does not meet standard of reliability or precision; based on fewer than 20 deaths in the numerator. Please click here for further details.
</excerpt>
### Rank 3 of 67 — 0.23
<excerpt title="Influenza and Pneumonia Deaths and Death Rates per 100000 Population">
# Locations
## Influenza and Pneumonia Deaths and Death Rates per 100,000 Population
### 2021
| Location | Influenza and Pneumonia Deaths | Influenza Deaths | Pneumonia Deaths | Influenza and Pneumonia Deaths | Influenza Deaths | Pneumonia Deaths |  
| --- | --- | --- | --- | --- | --- | --- |  
| United States | 41917 | 608 | 41309 | 10.5 | 0.1 | 10.4 |  
| Alabama | 1034 | 22 | 1012 | 16.8 | 0.4 | 16.5 |  
| Alaska | 42 | N/A | N/A | 7.2 | N/A | 7.1 |  
| Arizona | 932 | N/A | N/A | 10.2 | N/A | 10.1 |  
| Arkansas | 534 | N/A | N/A | 14.7 | N/A | 14.5 |  
| California | 4638 | 29 | 4609 | 10.5 | 0.1 | 10.5 |  
| Colorado | 290 | 10 | 280 | 4.8 | NSD | 4.6 |  
| Connecticut | 406 | N/A | N/A | 8.3 | N/A | 8.2 |  
| Delaware | 118 | 0 | 118 | 8.6 | N/A | 8.6 |  
| District of Columbia | 65 | 0 | 65 | 10 | N/A | 10 |  
| Florida | 2845 | 53 | 2792 | 8.8 | 0.1 | 8.6 |  
| Georgia | 1273 | 26 | 1247 | 11.3 | 0.2 | 11.1 |  
| Hawaii | 210 | 0 | 210 | 9.8 | N/A | 9.8 |
</excerpt>
### Rank 4 of 67 — 0.20
<excerpt title="Stats of the States - Influenza/Pneumonia Mortality">
# Influenza/Pneumonia Mortality by State
Print
Related Pages
1 The number of deaths per 100,000 total population.
Source: https://wonder.cdc.gov
States are categorized from highest rate to lowest rate. Although adjusted for differences in age-distribution and population size, rankings by state do not take into account other state specific population characteristics that may affect the level of mortality. When the number of deaths is small, rankings by state may be unreliable due to instability in death rates.
Last Reviewed: March 1, 2022
Source: CDC/National Center for Health Statistics
*   Facebook  
*   Twitter  
*   LinkedIn  
*   Syndicate
homeNCHS Pressroom
*   Weekly COVID-19 Mortality Overview  
*   2024 Release Schedule  
*   Upcoming  
*   Publications Archives  
*   QuickStats Archives  
*   Stats of the States  
*   Most Recent Data on Health Topics  
*   Statcasts  
*   Videos  
*   Press Release Archives  
*   NCHS Blog  
*   Join NCHS Media List
Related Sites
*   CDC Online Newsroom  
*   FastStats  
*   NCHS Publications and Products

*   About CDC  
*   Contact Us  
*   [800-232-4636](tel:8002324636)
FacebookTwitterInstagramLinkedInYoutubePinterestSnapchat

# Influenza/Pneumonia Mortality by State
*   CONTACT CDC Contact Us   Call 800-232-4636   Email Us      
*   ABOUT CDC

    *   About CDC  
    *   Jobs  
    *   Funding

*   POLICIES

    *   Accessibility  
    *   External Links  
    *   Privacy  
    *   Policies  
    *   No Fear Act  
    *   FOIA  
    *   OIG  
    *   Nondiscrimination  
    *   Vulnerability Disclosure Policy  
    *   Public Health Publications

*   CONNECT WITH US

    

    *   Facebook  
    *   Twitter  
    *   Instagram  
    *   LinkedIn

    

    *   Youtube  
    *   Pinterest  
    *   Snapchat  
    *   Email

*   LANGUAGES

    *   Español  
    *   繁體中文  
    *   Tiếng Việt  
    *   한국어  
    *   Tagalog  
    *   Русский  
    *   العربية  
    *   Kreyòl Ayisyen  
    *   Français  
    *   Polski  
    *   Português  
    *   Italiano  
    *   Deutsch  
    *   日本語  
    *   فارسی  
    *   English

*   U.S. Department of Health & Human Services  
*   Accessibility  
*   External Links  
*   Privacy  
*   Policies  
*   No Fear Act  
*   FOIA  
*   Nondiscrimination  
*   OIG  
*   Vulnerability Disclosure Policy  
*   Public Health Publications  
*   USA.gov
</excerpt>
### Rank 5 of 67 — 0.19
<excerpt title="Influenza and Pneumonia Deaths and Death Rates per 100000 Population">
# Locations
## Influenza and Pneumonia Deaths and Death Rates per 100,000 Population
### 2021
| Idaho | 161 | N/A | N/A | 7.8 | N/A | 7.7 |  
| Illinois | 1681 | N/A | N/A | 11 | N/A | 10.9 |  
| Indiana | 728 | 11 | 717 | 9.2 | NSD | 9.1 |  
| Iowa | 366 | 11 | 355 | 8.7 | NSD | 8.4 |  
| Kansas | 396 | 10 | 386 | 11.1 | NSD | 10.9 |  
| Kentucky | 739 | N/A | N/A | 13.8 | N/A | 13.6 |  
| Louisiana | 647 | 12 | 635 | 12.2 | NSD | 12 |  
| Maine | 211 | N/A | N/A | 10.6 | N/A | 10.4 |  
| Maryland | 629 | N/A | N/A | 8.7 | N/A | 8.6 |  
| Massachusetts | 817 | 14 | 803 | 9.1 | NSD | 9 |  
| Michigan | 1321 | 13 | 1308 | 10.4 | NSD | 10.3 |  
| Minnesota | 392 | N/A | N/A | 5.7 | N/A | 5.6 |  
| Mississippi | 697 | 18 | 679 | 20 | NSD | 19.5 |  
| Missouri | 884 | 13 | 871 | 11.5 | NSD | 11.3 |  
| Montana | 105 | N/A | N/A | 7.5 | N/A | 7.3 |
</excerpt>

## Search 5 — query: "Influenza and Pneumonia Mortality 2020 state lowest death rate per 100,000"
### Rank 1 of 34 — 0.31 (passed on)
<excerpt title="Influenza and Pneumonia Deaths and Death Rates per 100000 Population">
# Locations
Vermont
Virginia
Washington
West Virginia
Wisconsin
Wyoming
48,139
6,506
41,627
956
101
855
70
14
56
1,009
134
875
670
80
590
5,535
578
4,957
381
97
284
716
66
650
173
22
151
48
N/A
42
3,093
421
2,672
1,297
181
1,116
250
22
228
171
44
127
1,936
175
1,761
953
137
816
533
94
439
459
59
400
740
124
616
634
94
540
222
40
182
727
96
631
1,058
179
879
1,405
230
1,175
490
122
368
701
80
621
1,045
137
908
135
35
100
296
50
246
556
79
477
177
36
141
1,235
131
1,104
390
46
344
4,153
425
3,728
1,704
266
1,438
101
21
80
1,790
244
1,546
679
106
573
346
97
249

# Locations
2,289
330
1,959
141
30
111
665
125
540
160
41
119
1,360
169
1,191
3,326
399
2,927
299
47
252
81
25
56
1,052
149
903
762
122
640
481
68
413
616
121
495
73
17
56

# Locations
## Data Table
To view data, please select some geographies from the sidebar.
</excerpt>
### Rank 2 of 34 — 0.20
<excerpt title="Influenza and Pneumonia Deaths and Death Rates per 100000 Population">
# Locations
## Influenza and Pneumonia Deaths and Death Rates per 100,000 Population
### 2021
| Tennessee | 1225 | 42 | 1183 | 14.9 | 0.5 | 14.4 |  
| Texas | 2938 | 78 | 2860 | 10.5 | 0.3 | 10.2 |  
| Utah | 215 | N/A | N/A | 8.1 | N/A | 8.1 |  
| Vermont | 38 | 0 | 38 | 4.5 | N/A | 4.5 |  
| Virginia | 963 | 15 | 948 | 9.7 | NSD | 9.5 |  
| Washington | 496 | N/A | N/A | 5.9 | N/A | 5.8 |  
| West Virginia | 413 | N/A | N/A | 16.5 | N/A | 16.5 |  
| Wisconsin | 550 | N/A | N/A | 7.5 | N/A | 7.4 |  
| Wyoming | 79 | N/A | N/A | 11.9 | N/A | 11.8 |

# Locations
## Influenza and Pneumonia Deaths and Death Rates per 100,000 Population
### Notes
Causes of death attributable to flu and pneumonia include ICD-10 Codes J09-J18. Causes of death attributable to influenza specifically include ICD-10 codes J09, J10.0, J10.1, J10.8, J11.0, J11.1, and J11.8. Causes of death attributable to pneumonia specifically include ICD-10 codes J12.0, J12.1, J12.2, J12.3, J12.8, J12.9, J13, J14, J15.0, J15.1, J15.2, J15.3, J15.4, J15.5, J15.6, J15.7, J15.8, J15.9, J16.0, J16.8, J18.0, J18.1, J18.2, J18.8, and J18.9. Rates presented in this data table represent rates per 100,000 population and are age-adjusted to the 2000 U.S. standard population age distribution. Since death rates are affected by the population composition of a given area, age-adjusted death rates should be used for comparisons between areas because they control for differences in population composition.

# Locations
## Influenza and Pneumonia Deaths and Death Rates per 100,000 Population
### Sources
Centers for Disease Control and Prevention, National Center for Health Statistics. Underlying Cause of Death 1999-2024 on CDC WONDER Online Database. Data are from the Multiple Cause of Death Files, 1999-2024, as compiled from data provided by the 57 vital statistics jurisdictions through the Vital Statistics Cooperative Program. Accessed at https://wonder.cdc.gov/ucd-icd10-expanded.html on February 18, 2026.

# Locations
## Influenza and Pneumonia Deaths and Death Rates per 100,000 Population
### Definitions
**N/A**: Data not available due to suppression constraints. Please click here for further details. **NSD**: Not sufficient data. Figure does not meet standard of reliability or precision; based on fewer than 20 deaths in the numerator. Please click here for further details.
</excerpt>
### Rank 3 of 34 — 0.18
<excerpt title="Stats of the States - Influenza/Pneumonia Mortality">
# Restored CDC | Stats of the States - Influenza/Pneumonia Mortality
**Original site:**www.cdc.gov/nchs/pressroom/sosmap/flu_pneumonia_mortality/flu_pneumonia.htm | **RestoredCDC.org** is an independent project, not affiliated with CDC or any federal entity. Visit CDC.gov for free official information. Due to archival on **January 6, 2025**, recent outbreak data is unavailable. Videos are not restored. Access data.restoredcdc.org for restored data. Use of this site implies acceptance of this disclaimer.
[[More]](javascript:void(0);)
About UsReport BugCompare Content
Skip directly to site contentSkip directly to search
Español | Other Languages
Here's how you know
**Official websites use .gov**
A .gov website belongs to an official government organization in the United States.
**Secure .gov websites use HTTPS**
A lock (  ) or https:// means you've safely connected to the .gov website. Share sensitive information only on official, secure websites.
Search
Submit
National Center for Health Statistics

# Influenza/Pneumonia Mortality by State
Print
Related Pages
1 The number of deaths per 100,000 total population.
Source: https://wonder.cdc.gov
States are categorized from highest rate to lowest rate. Although adjusted for differences in age-distribution and population size, rankings by state do not take into account other state specific population characteristics that may affect the level of mortality. When the number of deaths is small, rankings by state may be unreliable due to instability in death rates.
Last Reviewed: March 1, 2022
Source: CDC/National Center for Health Statistics
*   Facebook  
*   Twitter  
*   LinkedIn  
*   Syndicate
homeNCHS Pressroom
*   Weekly COVID-19 Mortality Overview  
*   2024 Release Schedule  
*   Upcoming  
*   Publications Archives  
*   QuickStats Archives  
*   Stats of the States  
*   Most Recent Data on Health Topics  
*   Statcasts  
*   Videos  
*   Press Release Archives  
*   NCHS Blog  
*   Join NCHS Media List
Related Sites
*   CDC Online Newsroom  
*   FastStats  
*   NCHS Publications and Products

*   About CDC  
*   Contact Us  
*   [800-232-4636](tel:8002324636)
FacebookTwitterInstagramLinkedInYoutubePinterestSnapchat
</excerpt>
### Rank 4 of 34 — 0.18
<excerpt title="Major Article Two decades of influenza and pneumonia mortality trends: ...">
## Highlights
*   •  
In 20th century, influenza & pneumonia were leading causes of infectious death in US.

*   •  
Past research has examined mortality trends of geographical racial disparities.

*   •  
Over the study period, death rates from influenza and pneumonia declined in the US.

*   •  
Males consistently exhibited higher mortality rates than females.

*   •  
NH American Indians had the highest mortality rates, while Hispanics had the lowest.

## Highlights
### Background
In the 20th century, influenza and pneumonia constituted the largest proportion of infectious disease deaths in the United States. Despite progress in management, US mortality trends for these diseases have not been thoroughly investigated.

## Highlights
### Objectives
We aim to examine the patterns of influenza and pneumonia-related deaths among US residents.

## Highlights
### Methods
Crude death rates and age-adjusted mortality rates (AAMRs) per 100,000 individuals were calculated using influenza and pneumonia mortality data (International Classification of Diseases, 10th revision codes: J09-J18) from the CDC WONDER database. Annual percentage changes with a 95% confidence interval were determined using joinpoint regression analysis. Average annual percentage changes were computed as the weighted average of annual percentage changes.

## Highlights
### Results
From 1999 to 2020, US influenza and pneumonia deaths totaled 1,257,088 (AAMR: 17.09), with a significantly decreasing AAMR (−2.94). Males had a higher AAMR (20.13) than females (15.02). Non-Hispanic American Indians had the highest AAMR (20.44), while Hispanics had the lowest AAMR (13.91). The Northeast had the highest AAMR (18.02). All other regions had similar AAMRs. Rural regions had a consistently higher AAMR (19.80) than urban regions (AAMR: 16.51).

## Highlights
### Conclusion
Tailoring interventions toward high-risk groups can enhance the effectiveness of preventive measures, vaccination, and health care access.

## Access through your organization
Check access to the full text by signing in through your organization.
Access through**your organization**

## Section snippets


## Background
Influenza and pneumonia are both respiratory infections. Previous studies have shown that rates of pneumonia and influenza are temporally related; this is due to superinfection by a bacterial pathogen following a viral infection.1, 2, 3 In the 20th century, the largest proportion of deaths caused by infectious diseases in the United States were due to influenza and pneumonia.4 In 2018, influenza and pneumonia ranked as the eighth leading causes of mortality in the United States, accounting for

## Study design
In this descriptive research, data on influenza and pneumonia mortality were sourced from the Centers for Disease Control and Prevention Wide-Ranging Online Data for Epidemiologic Research (CDC WONDER) database.10 This database is an expansive and authoritative online repository containing public-use datasets covering mortality (deaths), cancer incidence, HIV and AIDS, tuberculosis, natality (births), census data, and various other topics spanning all states of the United States of America as
</excerpt>
### Rank 5 of 34 — 0.18
<excerpt title="How many people get the flu?">
During the 2022–2023 US flu season, an estimated 31.91 million people experienced symptoms of the influenza virus.
After two years of unusually low levels of recorded flu activity, cases jumped from 2022 to 2023, according to preliminary Centers for Disease Control and Prevention (CDC) estimates.

## When is the flu season?
The CDC determines the start and end of flu season by monitoring flu activity — illnesses, medical visits, and hospitalizations — through its influenza surveillance systems. Most seasons begin in October, peak between December and February, and continue through May.
The 2022–23 flu season began in October 2022 and continued until early September 2023, according to the CDC. Nearly 85% of cases during this season were recorded between October and January based on data from the National Center for Health Statistics.
For context, flu activity during the [2021-2022 season](https://www.cdc.gov/flu/season/faq-flu-season-2021-2022.htm#:~:text=Nationally%2C%20flu%20activity%20during%20the,the%20second%20in%20April%202022.) began to increase in November and remained elevated until mid-June.

## When is the flu season?
### Why were flu cases so low during the pandemic?
The CDC attributed low flu activity during the pandemic to COVID-19 mitigation efforts that are also effective in slowing the spread of the flu, such as the use of face masks, staying home, reduced travel, school closures, and more**.** As a result, estimates of those impacted by the 2021–22 flu season are as much as 90% lower than in past years.
The CDC described flu activity in the 2020–21 flu season as “unusually low.” It was the lowest flu activity since the CDC first began collecting data in 1997.
Flu cases rebounded during the 2021–22 season compared to the previous year, but were the second lowest in over a decade.

## How many people die from the flu?
The CDC estimates that between 12,000 and 52,000 people died of the flu annually between 2010 and 2020. The 2017–18 flu season had more related deaths than any other season: an estimated 52,000.
According to CDC data, the flu led to 15 million medical visits, over 360,000 hospitalizations, and 21,410 deaths during the 2022–23 season.
Since not everyone sick with the flu visits a doctor, and not all flu deaths occur in the hospital, the CDC uses mathematical modeling based on its surveillance data to estimate the total number of illnesses and deaths. This model considers factors like testing frequency, the likelihood of seeking medical care, and underreporting on death certificates.
The flu can lead to death by pneumonia, congestive heart failure, or chronic obstructive pulmonary disease — in which case flu testing may occur too late or not at all. The CDC says, “Only counting deaths where influenza was recorded on a death certificate would be a gross underestimation of influenza’s true impact.”
During the 2017–18 flu season, the mortality surveillance system recorded 15,620 deaths via death certificates, the most deaths in the last five years. By comparison, it recorded 9,843 deaths in the 2022–23 season.

## Which state has the most flu deaths?
The CDC also provides mortality data at the state level, but nationwide data releases are delayed. The latest data from CDC Wonder is from 2020.
Kansas, West Virginia, and North Dakota had 2020’s highest age-adjusted death rates.

## Which state has the most flu deaths?
### **How does flu risk vary by age?**
For the 2022–23 season, 26.6 per 100,000 Americans 65 and older died from the flu. That mortality rate was more than three times higher than any other age group.
In total, an estimated 15,399 Americans 65 and older died from the flu during the 2022-23 season, nearly 72% of all flu-related deaths.
</excerpt>

## Search 6 — query: "CDC site:cdc.gov "flu and pneumonia deaths" 2020 "per 100,000""
### Rank 1 of 1 — 0.28 (passed on)
<excerpt title="Death Data Maps | Stats of the States">
## Key points
*   The National Vital Statistics System provides a range of death-related statistics based on data from death certificates.  
*   Find U.S. maps with state and District of Columbia data for 17 causes of death, including chronic diseases, infectious diseases, and injuries.  
*   A map of state-level infant death data also is available.

## Leading causes of death
The National Vital Statistics System (NVSS) receives, analyzes, and shares data about deaths across the nation. NVSS experts use these data to determine the leading causes of death—the diseases, injuries, and other causes that lead to the most deaths each year.
Stats of the States provides U.S. maps featuring state-level data for 17 of the most common causes of death.

## Chronic diseases
Map of Alzheimer's disease deaths per 100,000 total population for each state
Map of cancer deaths per 100,000 total population for each state
Map of chronic lower respiratory disease deaths per 100,000 total population for each state
Map of chronic liver disease deaths per 100,000 total population for each state
Map of diabetes deaths per 100,000 total population for each state
Map of heart disease deaths per 100,000 total population for each state
Map of deaths from high blood pressure per 100,000 total population for each state
Map of kidney disease deaths per 100,000 total population for each state
Map of Parkinson's disease deaths per 100,000 total population for each state
Map of deaths from stroke per 100,000 total population for each state

## Infectious diseases
Map of COVID-19 deaths per 100,000 total population for each state
Map of flu and pneumonia deaths per 100,000 total population for each state

## Injuries
Map of accident deaths per 100,000 total population for each state
Map of drug overdose deaths per 100,000 total population for each state
Map of deaths by firearms per 100,000 total population for each state
Map of deaths by homicide per 100,000 total population for each state
Map of deaths by suicide per 100,000 total population for each state

## Infant deaths
When a baby dies within a year of birth, the death is classified as an infant death. This map features NVSS data about infant deaths from all causes.
Map of infant deaths per 1,000 live births for each state
Apr. 15, 2026
Content Source:
National Center for Health Statistics
About this page
Published: August 20, 2025
Updated: April 15, 2026
This page was last updated on this date. Updates may include minor edits, image changes, or other modifications to page content.
Reviewed: April 15, 2026
The information on this page was last reviewed by subject matter experts to ensure accuracy.

## Related Pages
*   Accident Mortality  
*   Alzheimer's Disease Mortality  
*   Cancer Mortality  
*   Chronic Lower Respiratory Disease Mortality  
*   Cirrhosis and Chronic Liver Disease Mortality
</excerpt>

## Search 7 — query: "flu-pneumonia.csv dlt.cdc.gov"
### Rank 1 of 153 — 0.06 (passed on)
<excerpt title="hrbrmstr/cdcfluview: :mask: R package to Retrieve U.S. Flu Season ...">
# current version
## # week_start <date>
##  6 Census Regi… East Sout…  1997    40       0.0542         0.0689       0        NA         3        0        NA      0  
##  7 Census Regi… West Sout…  1997    40       1.02           0.747        2        NA         1        2        NA      0  
##  8 Census Regi… Mountain    1997    40       2.26           2.28        87        NA        71       71        NA     15  
##  9 Census Regi… Pacific     1997    40       2.05           3.23        26        NA        17       36        NA      1  
## 10 Census Regi… New Engla…  1997    41       0.643          0.816       14        NA        14       29        NA      0  
## # … with 11,087 more rows, and 4 more variables: ilitotal <dbl>, num_of_providers <dbl>, total_patients <dbl>,  
## #   week_start <date>  
```

# current version
## # week_start <date>
```  
## Rows: 29,793  
## Columns: 16  
## $ region_type      <chr> "States", "States", "States", "States", "States", "States", "States", "States", "States", "St…  
## $ region           <chr> "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delawar…  
## $ year             <int> 2010, 2010, 2010, 2010, 2010, 2010, 2010, 2010, 2010, 2010, 2010, 2010, 2010, 2010, 2010, 201…  
## $ week             <int> 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 4…  
## $ weighted_ili     <dbl> NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, N…  
## $ unweighted_ili   <dbl> 2.1347700, 0.8751460, 0.6747210, 0.6960560, 1.9541200, 0.6606840, 0.0783085, 0.1001250, 2.808…
</excerpt>
### Rank 2 of 153 — 0.05
<excerpt title="hrbrmstr/cdcfluview: :mask: R package to Retrieve U.S. Flu Season ...">
# current version
## # week_start <date>
```  
## Rows: 29,793  
## Columns: 16  
## $ region_type      <chr> "States", "States", "States", "States", "States", "States", "States", "States", "States", "St…  
## $ region           <chr> "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delawar…  
## $ year             <int> 2010, 2010, 2010, 2010, 2010, 2010, 2010, 2010, 2010, 2010, 2010, 2010, 2010, 2010, 2010, 201…  
## $ week             <int> 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 4…  
## $ weighted_ili     <dbl> NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, N…  
## $ unweighted_ili   <dbl> 2.1347700, 0.8751460, 0.6747210, 0.6960560, 1.9541200, 0.6606840, 0.0783085, 0.1001250, 2.808…
</excerpt>
### Rank 3 of 153 — 0.05
<excerpt title="hrbrmstr/cdcfluview: :mask: R package to Retrieve U.S. Flu Season ...">
# current version
## 9 60 0.061 0.064 0.143 1 27 10440 73066 10467


# current version
## 10 60 0.062 0.065 0.157 1 35 12048 77136 12083


# current version
## # … with 388 more rows, and 10 more variables: weeknumber <chr>, geo_description <chr>, age_label <chr>,


# current version
## # week_start <date>, week_end <date>, year_week_num <int>, mmwrid <chr>, coverage_area <chr>, region_name <chr>,


# current version
## # callout <chr>
select(nat_pi, week_end, percent_pni, baseline, threshold) %>%   
  gather(measure, value, -week_end) %>%   
  ggplot(aes(week_end, value)) +   
  geom_line(aes(group=measure, color=measure)) +   
  scale_y_percent() +  
  scale_color_ipsum(name = NULL, labels=c("Baseline", "Percent P&I", "Threshold")) +  
  labs(x=NULL, y="% of all deaths due to P&I",  
       title="Percentage of all deaths due to pneumonia and influenza, National Summary") +  
  theme_ipsum_rc(grid="XY") +  
  theme(legend.position="bottom")
(st_pi <- pi_mortality("state", years=2015))

# current version
## # A tibble: 2,704 x 19


# current version
## seasonid baseline threshold percent_pni percent_complete number_influenza number_pneumonia all_deaths total_pni


# current version
## <chr> <dbl> <dbl> <dbl> <dbl> <dbl> <dbl> <dbl> <dbl>


# current version
## 1 55 NA NA 0.046 0.962 0 43 935 43


# current version
## 2 55 NA NA 0.036 0.835 0 29 811 29


# current version
## 3 55 NA NA 0.054 0.833 0 44 809 44


# current version
## 4 55 NA NA 0.07 0.947 0 64 920 64


# current version
## 5 55 NA NA 0.053 0.926 0 48 900 48


# current version
## 6 55 NA NA 0.057 0.987 0 55 959 55


# current version
## 7 55 NA NA 0.052 1 0 53 1023 53


# current version
## 8 55 NA NA 0.063 1 1 62 1002 63


# current version
## 9 55 NA NA 0.0560 0.95 0 52 923 52


# current version
## 10 55 NA NA 0.054 0.954 0 50 927 50


# current version
## # … with 2,694 more rows, and 10 more variables: weeknumber <chr>, geo_description <chr>, age_label <chr>,


# current version
## # week_start <date>, week_end <date>, year_week_num <int>, mmwrid <chr>, coverage_area <chr>, region_name <chr>,
</excerpt>
### Rank 4 of 153 — 0.04
<excerpt title="hrbrmstr/cdcfluview: :mask: R package to Retrieve U.S. Flu Season ...">
# current version
## 8 Delaware "http://dhss.delaware.gov/d… Weekly Influe… 1 Minimal 2017-10-07 2017-… 40


# current version
## 9 District of… "https://dchealth.dc.gov/no… Influenza Inf… 2 Minimal 2017-10-07 2017-… 40


# current version
## 10 Florida "http://www.floridahealth.g… Weekly Influe… 1 Minimal 2017-10-07 2017-… 40


# current version
## # … with 2,795 more rows
xdf <- map_df(2008:2017, ili_weekly_activity_indicators)
count(xdf, weekend, activity_level_label) %>%   
  complete(weekend, activity_level_label) %>%   
  ggplot(aes(weekend, activity_level_label, fill=n)) +   
  geom_tile(color="#c2c2c2", size=0.1) +  
  scale_x_date(expand=c(0,0)) +  
  viridis::scale_fill_viridis(name="# States", na.value="White") +  
  labs(x=NULL, y=NULL, title="Weekly ILI Indicators (all states)") +  
  coord_fixed(100/1) +  
  theme_ipsum_rc(grid="") +  
  theme(legend.position="bottom")

# current version
## # … with 2,795 more rows
### Pneumonia and Influenza Mortality Surveillance
(nat_pi <- pi_mortality("national"))

# current version
## # A tibble: 398 x 19


# current version
## seasonid baseline threshold percent_pni percent_complete number_influenza number_pneumonia all_deaths total_pni


# current version
## <chr> <dbl> <dbl> <dbl> <dbl> <dbl> <dbl> <dbl> <dbl>


# current version
## 1 60 0.053 0.0560 0.081 1 8 4825 59682 4833


# current version
## 2 60 0.054 0.057 0.084 1 12 5173 61641 5185


# current version
## 3 60 0.055 0.0580 0.086 1 16 5208 60467 5224


# current version
## 4 60 0.0560 0.059 0.091 1 15 5642 62047 5657


# current version
## 5 60 0.057 0.06 0.0970 1 21 6142 63280 6163


# current version
## 6 60 0.0580 0.061 0.105 1 21 7075 67380 7096


# current version
## 7 60 0.059 0.062 0.117 1 20 8040 68644 8060


# current version
## 8 60 0.06 0.063 0.132 1 30 9400 71440 9430


# current version
## 9 60 0.061 0.064 0.143 1 27 10440 73066 10467
</excerpt>
### Rank 5 of 153 — 0.04
<excerpt title="hrbrmstr/cdcfluview: :mask: R package to Retrieve U.S. Flu Season ...">
# current version
## # week_start <date>, week_end <date>, year_week_num <int>, mmwrid <chr>, coverage_area <chr>, region_name <chr>,


# current version
## # callout <chr>
(reg_pi <- pi_mortality("region", years=2015))

# current version
## # A tibble: 520 x 19


# current version
## seasonid baseline threshold percent_pni percent_complete number_influenza number_pneumonia all_deaths total_pni


# current version
## <chr> <dbl> <dbl> <dbl> <dbl> <dbl> <dbl> <dbl> <dbl>


# current version
## 1 55 0.064 0.071 0.07 1 0 178 2525 178


# current version
## 2 55 0.065 0.072 0.064 1 0 160 2512 160


# current version
## 3 55 0.066 0.073 0.0580 1 1 141 2457 142


# current version
## 4 55 0.067 0.074 0.07 0.989 0 171 2426 171


# current version
## 5 55 0.068 0.075 0.065 1 2 166 2565 168


# current version
## 6 55 0.069 0.077 0.067 0.985 1 162 2415 163


# current version
## 7 55 0.071 0.078 0.079 1 0 198 2491 198


# current version
## 8 55 0.072 0.079 0.072 1 1 176 2468 177


# current version
## 9 55 0.073 0.081 0.067 0.96 3 154 2353 157


# current version
## 10 55 0.075 0.0820 0.062 0.996 0 151 2441 151


# current version
## # … with 510 more rows, and 10 more variables: weeknumber <chr>, geo_description <chr>, age_label <chr>,


# current version
## # week_start <date>, week_end <date>, year_week_num <int>, mmwrid <chr>, coverage_area <chr>, region_name <chr>,


# current version
## # callout <chr>
### Retrieve metadata about U.S. State CDC Provider Data
state_data_providers()

# current version
## # A tibble: 59 x 5


# current version
## statename statehealthdeptname url statewebsitename statefluphonenum


# current version
## * <chr> <chr> <chr> <chr> <chr>


# current version
## 1 Alabama Alabama Department of Publi… "http://adph.org/influenza/" Influenza Surveillance 334-206-5300


# current version
## 2 Alaska State of Alaska Health and … "http://dhss.alaska.gov/dph/Epi/i… Influenza Surveillanc… 907-269-8000
</excerpt>

## Search 8 — query: "District of Columbia influenza pneumonia deaths per 100,000 2020"
### Rank 1 of 85 — 0.62 (passed on)
<excerpt title="Demographic and regional trends in pneumonia and sepsis related ...">
## 3 Results
### 3.4 Pneumonia and sepsis-related AAMR stratified by age group
Pneumonia and sepsis-related mortality rates varied significantly across age groups, with older adults experiencing the highest crude death rates per 100,000 population with an overall AAMR of 68.08 (95% CI: 67.91 to 68.25) (Supplementary Figure 3). Among 25–44-year-old adults, the AAMRs remained steady from 1999 to 2018 with an APC of 0.95 (95% CI: 0.15 to 1.77) (_p-_ value: 0.023), which then increased from 2018 to 2020 with an APC of 27.40 (95% CI: 1.64 to 59.70) (_p-_ value: 0.037). The AAMR values for 45–64-year-old adults inclined steadily till 2018 with an APC of 1.96 (95% CI: 1.58 to 2.33) (_p-_ value < 0.0001) and culminated in a sudden surge from 2018 to 2020 with an APC of 24.67 (95% CI: 13.16 to 37.34) (_p-_ value: 0.0001). Older adults (65–85 + years) experienced a significant surge from 2012 to 2020 with an APC of 3.66 (95% CI: 1.59 to 5.76) (_p-_ value: 0.001). Overall, the mortality rates followed an expected pattern, with older age groups exhibiting sustained high mortality rates (Supplementary Tables 3, 9).

## 3 Results
### 3.5 Pneumonia and sepsis-related AAMR stratified by geographic region
Mortality trends showed significant disparities across the different states, with Vermont having the lowest AAMR of 8.46 (95% CI: 7.90 to 9.01) and the District of Columbia having the highest AAMR of 26.96 (95% CI: 25.85 to 28.08) (Figure 3, Supplementary Table 6). States that fell into the top 90th percentile were the District of Columbia, Kentucky, Nevada, West Virginia, and Tennessee, compared with states that fell into the lower 10th percentile, including Vermont, Minnesota, Montana, Oregon, and Wisconsin.
Figure 3
</excerpt>
### Rank 2 of 85 — 0.42
<excerpt title="Influenza and Pneumonia Deaths and Death Rates per 100000 Population">
# Locations
## Influenza and Pneumonia Deaths and Death Rates per 100,000 Population
### 2021
| Location | Influenza and Pneumonia Deaths | Influenza Deaths | Pneumonia Deaths | Influenza and Pneumonia Deaths | Influenza Deaths | Pneumonia Deaths |  
| --- | --- | --- | --- | --- | --- | --- |  
| United States | 41917 | 608 | 41309 | 10.5 | 0.1 | 10.4 |  
| Alabama | 1034 | 22 | 1012 | 16.8 | 0.4 | 16.5 |  
| Alaska | 42 | N/A | N/A | 7.2 | N/A | 7.1 |  
| Arizona | 932 | N/A | N/A | 10.2 | N/A | 10.1 |  
| Arkansas | 534 | N/A | N/A | 14.7 | N/A | 14.5 |  
| California | 4638 | 29 | 4609 | 10.5 | 0.1 | 10.5 |  
| Colorado | 290 | 10 | 280 | 4.8 | NSD | 4.6 |  
| Connecticut | 406 | N/A | N/A | 8.3 | N/A | 8.2 |  
| Delaware | 118 | 0 | 118 | 8.6 | N/A | 8.6 |  
| District of Columbia | 65 | 0 | 65 | 10 | N/A | 10 |  
| Florida | 2845 | 53 | 2792 | 8.8 | 0.1 | 8.6 |  
| Georgia | 1273 | 26 | 1247 | 11.3 | 0.2 | 11.1 |  
| Hawaii | 210 | 0 | 210 | 9.8 | N/A | 9.8 |
</excerpt>
### Rank 3 of 85 — 0.40
<excerpt title="Influenza and Pneumonia Deaths and Death Rates per 100000 Population">
# Locations
## Influenza and Pneumonia Deaths and Death Rates per 100,000 Population
### 2024
| Location | Influenza and Pneumonia Deaths | Influenza Deaths | Pneumonia Deaths | Influenza and Pneumonia Deaths | Influenza Deaths | Pneumonia Deaths |  
| --- | --- | --- | --- | --- | --- | --- |  
| United States | 48139 | 6506 | 41627 | 11.2 | 1.6 | 9.6 |  
| Alabama | 956 | 101 | 855 | 14.5 | 1.6 | 12.9 |  
| Alaska | 70 | 14 | 56 | 10.4 | 2.1 | 8.2 |  
| Arizona | 1009 | 134 | 875 | 10 | 1.4 | 8.6 |  
| Arkansas | 670 | 80 | 590 | 17.1 | 2 | 15.1 |  
| California | 5535 | 578 | 4957 | 11.6 | 1.3 | 10.4 |  
| Colorado | 381 | 97 | 284 | 5.9 | 1.4 | 4.4 |  
| Connecticut | 716 | 66 | 650 | 13.9 | 1.3 | 12.6 |  
| Delaware | 173 | 22 | 151 | 11.8 | 1.5 | 10.3 |  
| District of Columbia | 48 | N/A | 42 | 6.8 | N/A | 6 |  
| Florida | 3093 | 421 | 2672 | 8.5 | 1.2 | 7.3 |  
| Georgia | 1297 | 181 | 1116 | 10.4 | 1.4 | 8.9 |
</excerpt>
### Rank 4 of 85 — 0.40
<excerpt title="Demographic and regional trends in pneumonia and sepsis related ...">
## 3 Results
### 3.5 Pneumonia and sepsis-related AAMR stratified by geographic region
Mortality trends showed significant disparities across the different states, with Vermont having the lowest AAMR of 8.46 (95% CI: 7.90 to 9.01) and the District of Columbia having the highest AAMR of 26.96 (95% CI: 25.85 to 28.08) (Figure 3, Supplementary Table 6). States that fell into the top 90th percentile were the District of Columbia, Kentucky, Nevada, West Virginia, and Tennessee, compared with states that fell into the lower 10th percentile, including Vermont, Minnesota, Montana, Oregon, and Wisconsin.
Figure 3

## 3 Results
### 3.5 Pneumonia and sepsis-related AAMR stratified by geographic region
Over the course of the study, the South and Midwest regions experienced an incline from 1999 to 2018 with an APC of 0.78 (95% CI: 0.22 to 1.34) (_p-_ value: 0.009) and 0.91 (95% CI: 0.38 to 1.45) (_p-_ value: 0.002), respectively, following a significant surge in both from 2018 to 2020 with an APC of 19.50 (95% CI: 3.29 to 38.25) (_p-_ value: 0.019) and 18.35 (95% CI: 2.10 to 37.19) (_p-_ value: 0.028), respectively. While the western region had a steady increase with an APC of 1.27 (95% CI: 0.67 to 1.87) (_p-_ value: 0.0002). The only decline was observed in the Northeast region from 1999 to 2011 with an APC of −1.28 (95% CI: −2.47 to −0.07) (_p-_ value: 0.039), followed by a surge from 2011 to 2020 with an APC of 2.73 (95% CI: 1.04 to 4.45) (_p-_ value: 0.003).
</excerpt>
### Rank 5 of 85 — 0.37
<excerpt title="Influenza and Pneumonia Deaths and Death Rates per 100000 Population">
# Locations
## Influenza and Pneumonia Deaths and Death Rates per 100,000 Population
### 2022
| Location | Influenza and Pneumonia Deaths | Influenza Deaths | Pneumonia Deaths | Influenza and Pneumonia Deaths | Influenza Deaths | Pneumonia Deaths |  
| --- | --- | --- | --- | --- | --- | --- |  
| United States | 47052 | 5944 | 41108 | 11.3 | 1.5 | 9.8 |  
| Alabama | 957 | 93 | 864 | 14.9 | 1.5 | 13.4 |  
| Alaska | 75 | 18 | 57 | 10.4 | NSD | 7.8 |  
| Arizona | 962 | 95 | 867 | 10.1 | 1.1 | 9 |  
| Arkansas | 653 | 105 | 548 | 17.2 | 2.9 | 14.3 |  
| California | 5308 | 518 | 4790 | 11.5 | 1.1 | 10.3 |  
| Colorado | 469 | 120 | 349 | 7.3 | 1.9 | 5.4 |  
| Connecticut | 563 | 61 | 502 | 11.2 | 1.3 | 9.9 |  
| Delaware | 146 | 15 | 131 | 10.1 | NSD | 8.8 |  
| District of Columbia | 58 | N/A | N/A | 8.5 | N/A | 7.8 |  
| Florida | 2887 | 230 | 2657 | 8.3 | 0.7 | 7.6 |  
| Georgia | 1333 | 129 | 1204 | 11.3 | 1.1 | 10.2 |
</excerpt>

## Search 9 — query: "CDC influenza pneumonia deaths per 100,000 2020 list states"
### Rank 1 of 73 — 0.41 (passed on)
<excerpt title="Influenza and Pneumonia Deaths and Death Rates per 100000 Population">
# Locations
Vermont
Virginia
Washington
West Virginia
Wisconsin
Wyoming
48,139
6,506
41,627
956
101
855
70
14
56
1,009
134
875
670
80
590
5,535
578
4,957
381
97
284
716
66
650
173
22
151
48
N/A
42
3,093
421
2,672
1,297
181
1,116
250
22
228
171
44
127
1,936
175
1,761
953
137
816
533
94
439
459
59
400
740
124
616
634
94
540
222
40
182
727
96
631
1,058
179
879
1,405
230
1,175
490
122
368
701
80
621
1,045
137
908
135
35
100
296
50
246
556
79
477
177
36
141
1,235
131
1,104
390
46
344
4,153
425
3,728
1,704
266
1,438
101
21
80
1,790
244
1,546
679
106
573
346
97
249

# Locations
2,289
330
1,959
141
30
111
665
125
540
160
41
119
1,360
169
1,191
3,326
399
2,927
299
47
252
81
25
56
1,052
149
903
762
122
640
481
68
413
616
121
495
73
17
56

# Locations
## Data Table
To view data, please select some geographies from the sidebar.
</excerpt>
### Rank 2 of 73 — 0.27
<excerpt title="Influenza and Pneumonia Deaths and Death Rates per 100000 Population">
# Locations
## Influenza and Pneumonia Deaths and Death Rates per 100,000 Population
### 2021
| Tennessee | 1225 | 42 | 1183 | 14.9 | 0.5 | 14.4 |  
| Texas | 2938 | 78 | 2860 | 10.5 | 0.3 | 10.2 |  
| Utah | 215 | N/A | N/A | 8.1 | N/A | 8.1 |  
| Vermont | 38 | 0 | 38 | 4.5 | N/A | 4.5 |  
| Virginia | 963 | 15 | 948 | 9.7 | NSD | 9.5 |  
| Washington | 496 | N/A | N/A | 5.9 | N/A | 5.8 |  
| West Virginia | 413 | N/A | N/A | 16.5 | N/A | 16.5 |  
| Wisconsin | 550 | N/A | N/A | 7.5 | N/A | 7.4 |  
| Wyoming | 79 | N/A | N/A | 11.9 | N/A | 11.8 |

# Locations
## Influenza and Pneumonia Deaths and Death Rates per 100,000 Population
### Notes
Causes of death attributable to flu and pneumonia include ICD-10 Codes J09-J18. Causes of death attributable to influenza specifically include ICD-10 codes J09, J10.0, J10.1, J10.8, J11.0, J11.1, and J11.8. Causes of death attributable to pneumonia specifically include ICD-10 codes J12.0, J12.1, J12.2, J12.3, J12.8, J12.9, J13, J14, J15.0, J15.1, J15.2, J15.3, J15.4, J15.5, J15.6, J15.7, J15.8, J15.9, J16.0, J16.8, J18.0, J18.1, J18.2, J18.8, and J18.9. Rates presented in this data table represent rates per 100,000 population and are age-adjusted to the 2000 U.S. standard population age distribution. Since death rates are affected by the population composition of a given area, age-adjusted death rates should be used for comparisons between areas because they control for differences in population composition.

# Locations
## Influenza and Pneumonia Deaths and Death Rates per 100,000 Population
### Sources
Centers for Disease Control and Prevention, National Center for Health Statistics. Underlying Cause of Death 1999-2024 on CDC WONDER Online Database. Data are from the Multiple Cause of Death Files, 1999-2024, as compiled from data provided by the 57 vital statistics jurisdictions through the Vital Statistics Cooperative Program. Accessed at https://wonder.cdc.gov/ucd-icd10-expanded.html on February 18, 2026.

# Locations
## Influenza and Pneumonia Deaths and Death Rates per 100,000 Population
### Definitions
**N/A**: Data not available due to suppression constraints. Please click here for further details. **NSD**: Not sufficient data. Figure does not meet standard of reliability or precision; based on fewer than 20 deaths in the numerator. Please click here for further details.
</excerpt>
### Rank 3 of 73 — 0.27
<excerpt title="Influenza and Pneumonia Deaths and Death Rates per 100000 Population">
# Locations
## Influenza and Pneumonia Deaths and Death Rates per 100,000 Population
### 2021
| Location | Influenza and Pneumonia Deaths | Influenza Deaths | Pneumonia Deaths | Influenza and Pneumonia Deaths | Influenza Deaths | Pneumonia Deaths |  
| --- | --- | --- | --- | --- | --- | --- |  
| United States | 41917 | 608 | 41309 | 10.5 | 0.1 | 10.4 |  
| Alabama | 1034 | 22 | 1012 | 16.8 | 0.4 | 16.5 |  
| Alaska | 42 | N/A | N/A | 7.2 | N/A | 7.1 |  
| Arizona | 932 | N/A | N/A | 10.2 | N/A | 10.1 |  
| Arkansas | 534 | N/A | N/A | 14.7 | N/A | 14.5 |  
| California | 4638 | 29 | 4609 | 10.5 | 0.1 | 10.5 |  
| Colorado | 290 | 10 | 280 | 4.8 | NSD | 4.6 |  
| Connecticut | 406 | N/A | N/A | 8.3 | N/A | 8.2 |  
| Delaware | 118 | 0 | 118 | 8.6 | N/A | 8.6 |  
| District of Columbia | 65 | 0 | 65 | 10 | N/A | 10 |  
| Florida | 2845 | 53 | 2792 | 8.8 | 0.1 | 8.6 |  
| Georgia | 1273 | 26 | 1247 | 11.3 | 0.2 | 11.1 |  
| Hawaii | 210 | 0 | 210 | 9.8 | N/A | 9.8 |
</excerpt>
### Rank 4 of 73 — 0.26
<excerpt title="Influenza and Pneumonia Deaths and Death Rates per 100000 Population">
# Locations
Locations
- [x] United States
States Clear All Selections
- [x] Select All

- [x] Alabama

- [x] Alaska

- [x] Arizona

- [x] Arkansas

- [x] California

- [x] Colorado

- [x] Connecticut

- [x] Delaware

- [x] District of Columbia

- [x] Florida

- [x] Georgia

- [x] Hawaii

- [x] Idaho

- [x] Illinois

- [x] Indiana

- [x] Iowa

- [x] Kansas

- [x] Kentucky

- [x] Louisiana

- [x] Maine

- [x] Maryland

- [x] Massachusetts

- [x] Michigan

- [x] Minnesota

- [x] Mississippi

- [x] Missouri

- [x] Montana

- [x] Nebraska

- [x] Nevada

- [x] New Hampshire

- [x] New Jersey

- [x] New Mexico

- [x] New York

- [x] North Carolina

- [x] North Dakota

- [x] Ohio

- [x] Oklahoma

- [x] Oregon

- [x] Pennsylvania

- [x] Rhode Island

- [x] South Carolina

- [x] South Dakota

- [x] Tennessee

- [x] Texas

- [x] Utah

- [x] Vermont

- [x] Virginia

- [x] Washington

- [x] West Virginia

- [x] Wisconsin

- [x] Wyoming
Tools:
*   Table  
*   Map  
*   Trend Graph
Location
Influenza and Pneumonia Deaths
Influenza Deaths
Pneumonia Deaths
United States
Alabama
Alaska
Arizona
Arkansas
California
Colorado
Connecticut
Delaware
District of Columbia
Florida
Georgia
Hawaii
Idaho
Illinois
Indiana
Iowa
Kansas
Kentucky
Louisiana
Maine
Maryland
Massachusetts
Michigan
Minnesota
Mississippi
Missouri
Montana
Nebraska
Nevada
New Hampshire
New Jersey
New Mexico
New York
North Carolina
North Dakota
Ohio
Oklahoma
Oregon
Pennsylvania
Rhode Island
South Carolina
South Dakota
Tennessee
Texas
Utah
</excerpt>
### Rank 5 of 73 — 0.23
<excerpt title="Influenza and Pneumonia Deaths and Death Rates per 100000 Population">
# Locations
## Influenza and Pneumonia Deaths and Death Rates per 100,000 Population
### 2021
| Idaho | 161 | N/A | N/A | 7.8 | N/A | 7.7 |  
| Illinois | 1681 | N/A | N/A | 11 | N/A | 10.9 |  
| Indiana | 728 | 11 | 717 | 9.2 | NSD | 9.1 |  
| Iowa | 366 | 11 | 355 | 8.7 | NSD | 8.4 |  
| Kansas | 396 | 10 | 386 | 11.1 | NSD | 10.9 |  
| Kentucky | 739 | N/A | N/A | 13.8 | N/A | 13.6 |  
| Louisiana | 647 | 12 | 635 | 12.2 | NSD | 12 |  
| Maine | 211 | N/A | N/A | 10.6 | N/A | 10.4 |  
| Maryland | 629 | N/A | N/A | 8.7 | N/A | 8.6 |  
| Massachusetts | 817 | 14 | 803 | 9.1 | NSD | 9 |  
| Michigan | 1321 | 13 | 1308 | 10.4 | NSD | 10.3 |  
| Minnesota | 392 | N/A | N/A | 5.7 | N/A | 5.6 |  
| Mississippi | 697 | 18 | 679 | 20 | NSD | 19.5 |  
| Missouri | 884 | 13 | 871 | 11.5 | NSD | 11.3 |  
| Montana | 105 | N/A | N/A | 7.5 | N/A | 7.3 |
</excerpt>

For each search, read the top excerpt and the ones ranked below it, and judge whether the order is right for answering the question. An excerpt holding the answer, or a fact that leads to it, should outrank one that only repeats the query's words or covers the topic without a checkable fact. If none of the excerpts holds anything useful, that is the search's fault, not this instruction's. Find the ranking error that cost the most and write a new instruction that fixes it. Replace or compress existing text where you can; avoid making it much longer. Do not write the "Original question" or "Search query" lines; they are appended for you. Do not copy any fact, name, site or topic from these examples.

Provide the new instruction within ``` blocks.
