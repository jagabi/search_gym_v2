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
I'm studying the effects of product safety legislation on safety recalls during periods of economic turmoil, with a main focus on the Covid-19 pandemic in Australia and gas products. 

Give me a list of the PRA Numbers of all product safety recalls posted on www.productsafety.gov.au between 1 January 2020 and 1 July 2020 (inclusive) that have been labelled as containing the topic "Gas products and appliances". Exclude products that were not sold 'Nationally'.

The list should look like this: 2020/11111, 2020/11112, 2020/11115, 2020/11116, 2020/11117, 2020/11119, 2020/11125

## Expected answer
2020/18315, 2020/18164, 2020/18098

## Grade 0.00

## Search 1 — query: "productsafety.gov.au gas products and appliances 2020 site:productsafety.gov.au"
### Rank 1 of 528 — 0.11 (passed on)
<excerpt title="Auto-Trail Motorhomes">
Title: PDF document  
URL Source: https://www.productsafety.gov.au/system/files/recall/Updated%20recall%20advertisement%20-%207%20June%202024.pdf  
Markdown Content:

## [PDF page 1]
Auto-Trail Motorhomes
AutoTrail -  MyRV NB (V  ariants: Apache, FB, Delaware)  
MyRV - Fiat Ducato II Series (V  ariants: FB, EB, EKS, Imala,  
MyRV - Delaware, Scout) AL-KO Fiat Ducato II TA (Comanche)  
MyRV - AL-K  O Fiat Ducato II SA (Delaware, Scout)
Supplied by MyRV Pty Ltd and  sold by Elite RV  
between 3 August 2012 and 20 November 2020
Defects: Liquefied  Petroleum Gas (LPG) is  a colourless, highly flammable gas that may  leak  
and build up inside the caravan  where the consumer gas piping is located inside the caravan.
Some models may h  ave defects in relation to the relevant  gas safety standard for installation in  
caravans for non-propulsive purposes:
1.  LP Gas cylinder compartments are not correctly sealed or vented.  
2.  Ventilation of the living area is not sized or located correctly.  
3.  Gas safety labelling does not comply with the requirements for gas systems in  
recreational vehicles.  
Hazards:  In the event of a gas leak, the following may occur:  
1.  Incorrect LP gas cylinder storage and venting increases the risk of any leaking gas  not  
dispersing or being diluted to safe levels. Any build-up of LP  Gas increases the risk of fire  
or explosion.  
2.  Insufficient ventilation provisions  may cause a build-up of products of combustion from gas  
appliances w  ithin the motorhome and there may be risk of carbon monoxide poisoning,  
which could result in serious illness, injury or death.
What to do: Consumers can continue to use their gas appliances but s  hould have the  
windows, door or roof vent open for more ventilation until the vehicle is  repaired.
Owners should contact their nearest Elite RV Service Centre (https://www.auto-trail.com.au/  
contact-auto-trail-australia/) to arrange for modifications to the installation, free of charge.
Contact details: For further information, consumers can contact Elite RV on 07 5593 6140  
or at service@eliterv.com.au.
</excerpt>
### Rank 2 of 528 — 0.10
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
### Rank 3 of 528 — 0.10
<excerpt title="Role of the ACCC and government in recalls">
## Sometimes another government agency leads the recall
### Agricultural and veterinary products, food, therapeutic goods, and road vehicles
For the following products, the specialist agency, and not the ACCC, is the lead agency for the recall and other safety issues.
For these products, the specialist agency:
*   assesses the recall and publishes the recall on its website  
*   decides whether to intervene in the recall and what actions to take.
The specialist agency’s guidelines, and not these guidelines, apply to the recall. Suppliers need to check the specialist agency’s recall guidelines, as updated from time to time, to understand what they have to do when conducting the recall.
| Product | Specialist (lead) agency | Recall resources |  
| --- | --- | --- |  
| Agricultural and veterinary chemical products | Australian Pesticides and Veterinary Medicines Authority | * Recall website * Guidelines For recalling Agricultural and Veterinary Chemical Products |  
| Food | Food Standards Australia New Zealand (FSANZ) is the coordinating authority working with the relevant state or territory food agency. | * Recall website * Food Industry Recall protocol Notification of the recall to the ACCC is done by FSANZ on behalf of the food business undertaking the recall. |  
| Therapeutic goods | Therapeutic Goods Administration | * Recall website * Uniform recall procedure for therapeutic goods |  
| Road vehicles and approved road vehicle parts | Department of Infrastructure, Transport, Regional Development, Communications, Sport and the Arts | * Recalls website * Recalls policy Recall notices for road vehicles and approved road vehicles parts are received by the Department, and not the ACCC, under the Australian Consumer Law. |

## Sometimes another government agency leads the recall
### Gas appliances, electrical and building products
For an electrical product, gas appliance or building product recall, a state or territory regulator is designated as the point of contact (home regulator).
For electrical products and gas appliances, the home regulator is usually the regulator located where the initial incident occurred or where the recalling supplier is located.
A number of things happen when a supplier notifies the ACCC of a recall:
*   The ACCC will seek advice from the home regulator to make sure that the wording in the recall notice is accurate and suitable to the risk. The ACCC will publish the agreed notice on the ACCC Product Safety website.  
*   Both the home regulator and the ACCC monitors the recall. Suppliers provide progress reports to both the home regulator and the ACCC. The home regulator liaises with the other state and territory regulators.  
*   Information given to us will usually be shared with the home regulator. This is to assist us in understanding the risk, hazard, use and misuse of the product.  
*   Both this guideline and the state and territory regulator’s guideline apply to the recall.
| Product | Specialist agency |  
| --- | --- |  
| Building products | For more information, contact your state and territory building and plumbing administrations.For suppliers in the Northern Territory, contact Northern Territory Consumer Affairs. |  
| Electrical products | For more information, contact your state or territory electrical safety regulator. The Electrical Regulatory Authorities Council Recall Guidelines published by the Electrical Regulatory Authorities Council also apply to the recall. |  
| Gas appliances | For more information, contact your state or territory gas appliance safety regulator. The Gas Technical Regulators Committee Recall Guidelines published by the Gas Technical Regulators Committee also apply to the recall. |

## Sometimes another government agency leads the recall
### Other products
For other products covered by a specialist regime, you need to contact the specialist agency to understand your obligations. This includes the following specialist agencies:
| Product | Specialist agency |  
| --- | --- |  
| Asbestos | State or territory work health safety regulator. |  
| Chemicals - industrial chemicals | Australian Industrial Chemicals Introduction Scheme |  
| Poisons | State and territory poisons regulators Some state and territory regulators may not have recall powers and may collaborate with state consumer affairs to recall a product. |
See more information about the Australian product safety system, including a list of specialist agencies.
</excerpt>
### Rank 4 of 528 — 0.08
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
### Rank 5 of 528 — 0.08
<excerpt title="Conducting a consumer product safety recall">
## [PDF page 59]
Gas appliances, elec trical and building produc ts  
For an electrical product, gas appliance or building product recall, a state or territor y regulator is  
designated as the point of contact (home regulator).
For electrical products and gas appliances, the home regulator is usually the regulator located where  
the initial incident occurred or where the recalling supplier is located.
When a supplier notifies the ACCC of a recall  
	the ACCC will seek advice from the home regulator to make sure that the wording in the recall  
notice is accurate and suitable to the risk . The ACCC will publish the agreed notice on the Product  
S afet y Australia website  
	both the home regulator and the ACCC monitors the recall. Suppliers provide progress repor  ts  
to both the home regulator and the ACCC. The home regulator liaises with the other state and  
te r r i to r  y  r e g u l a to r s  
	information given to us will usually be shared with the home regulator. This is to assist us in  
understanding the risk , hazard, use and misuse of the product  
	both this guideline and the state and territor y regulator ’s guideline apply to the recall.
Product  Specialist agency
Building products  C ontact your state and territor y building and plumbing administrations fo r  
more information. For suppliers in the Nor thern Territor y, contact Nor thern  
Territor y Consumer Af fairs.
Electrical products  C ontact your state or territor y ele ctrical safet y regulator for more  
information.  
T he Ele ctrical Regulator y Authorities C ouncil Re call Guidelines published by  
the Ele ctrical Regulator y Authorities C ouncil also apply to the re call.
Gas appliances  C ontact your state or territor y gas appliance safet y regulator for more  
information.  
T he Gas Te chnical Regulators C ommit te e Re call Guidelines published by  
the Gas Te chnical Regulators C ommit te e also apply to the re call.
O ther produc ts  
For other products covered by a specialist regime, you need to contact the specialist agency to  
understand your obligations. This includes the following specialist agencies:
Product  Specialist agency
Asbestos  S tate or territor y work health safet y regulator.

## [PDF page 59]
Chemicals – Industrial  Australian Industrial Chemicals Introduction S cheme.  
chemic als
Poisons  S tate and territor y poisons regulators. S ome state and territor y regulators  
may not have re call powers and may collaborate with state consumer  
af fairs to re call a product.
You can find fur  ther information about the Australian product safet y system and a list of spe cialist  
agencies on the Product S afet y Australia website.
54
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

## Search 2 — query: "2020/ gas products and appliances"productsafety.gov.au""
### Rank 1 of 95 — 0.12 (passed on)
<excerpt title="Product Recall">
*   Back to Home  
*   Back to Product Support  
*    Product Recall

## Black Tempered Glass Gas Cooktops (Certificate number AGA 8145 G)
WHG638BC & WHG958BC Electrolux Home Products Pty Ltd, is recalling Westinghouse Models WHG638BC & WHG958BC Black Tempered Glass Gas Cooktops. Supplied from February 2020. The model and serial number is visible on the base of the unit.
WHAT IS THE DEFECT? The glass in the cooktop does not comply with the Domestic Gas Cooking Appliances Standard. If the glass breaks it may shatter into fragments and shards that may hit people using the cooktop or people near by.
WHAT IS THE HAZARD? The glass may break into sharp fragments or shards and pose a risk of serious injury. **Incidents causing injury have occurred.**
ACTION REQUIRED? Consumers should check the model number of their cooktop to see if it is affected.
If it is a Westinghouse Black Glass Gas Cooktop Model WHG638BC or WHG958BC, please contact us here at Electrolux to arrange for a refund or for a service technician to attend free of charge to replace the product.
Please see https://www.productsafety.gov.au/recalls/electrolux-home-products-pty-ltd-%E2%80%94-westinghouse-black-tempered-glass-gas-cooktop for full details.
Please contact us by calling the toll-free number [1800 001 218](tel: 1800 001 218) between 8am and 7pm EST Mon-Fri or emailing us at [productrecall@electrolux.com](mailto:productrecall@electrolux.com).
For further information, please Download the recall notice.

## Book Service And Repair
Built by experts — repaired by experts, nobody knows your appliance better than us.
You can trust us to deliver the best possible quality of care, every day for both warranty and out of warranty service and repairs. That's our promise to you.
Built by experts — repaired by experts, nobody knows your appliance better than us.
You can trust us to deliver the best possible quality of care, every day for both warranty and out of warranty service and repairs. That's our promise to you.
No Results

## Book Service And Repair
### Contact Us
Our Customer Care team is available 7 days a week
MON to FRI 8AM - 7PM
SAT 9AM - 2PM
SUN 10AM - 2PM

## Book Service And Repair
### Enquire Online
Contact Westinghouse 24/7. Send us your comments or questions. We're always happy to help.

## Book Service And Repair
### Warranty Information
See what is covered in your appliance warranty and make sure you're covered.
</excerpt>
### Rank 2 of 95 — 0.12
<excerpt title="GAS SAFETY RECALL">
Title: PDF document  
URL Source: https://qga.org.au/images/blog/R-Gas%20Safety%20Recall%20-%20Swift%20Appliance%20Group%20500%20Series%20Cooker-Grill%20&%20Cooktops.pdf  
Markdown Content:

## [PDF page 1]
GAS SAFETY RECALL
Swift Appliance Group 500 Series Cooker/Grill and Cooktops
Model Numbers 502BHSP, 502BHFW, 502DHSP, 502RHSP, 502SHFW, 502SHW,  
502WBHSP, 503BHSPM, 503BHSP, 503BHSPMLG, 503BHSW, 503DHSP, 503RHSP,  
503SHSPM, 503SHSW and 503BHSPN
IDENTIFICATION: The information in this recall advertisement will be updated when more  
infomation is available.
Approval Number AGA  6488G - Data plate located on the inside front left side of the lid.
Products supplied to consumers, caravan, camper and motorhome manufacturers between  
01/01/2019 and 1/06/2020.
DEFECT: A part of the gas supply pipe may break or develop a hole.  This may cause a gas  
leak.
HAZARD: If the gas leaks in the presence of an ignition source this may lead to an explosion and/  
or fire, which may result in serious illness, injury or death. The defect has caused incidents that  
have caused serious injuries and burns.
If gas leaks and builds up in an enclosed area, such as a motorhome or caravan, asphyxiation  
may occur.
ACTION REQUIRED:  
Consumers should check if their appliance is affected and if so immediately turn off  the  
appliance and do not operate it  on gas. The gas supply to the appliance  can be isolated at the  
gas isolation valve, adjacent to the appliance  .
To identify affected appliances, open the glass lid and check the model number on the data  
plate that is on the inside front left side of the lid.
Consumers must ensure that Gas Cooker units are serviced and tested every 2-3 years.

## [PDF page 1]
For further information, consumers with affected appliances can contact Swift Appliance Group  
by  phone  on  0412  821  912  (Monday  to  Friday  9am  to  5pm),  via  email  at  
swiftrecall@outlook.com  or  visit  https://www.swiftappliancegroup.com.au to  register  
their details to be advised of remedial actions when they are available as the remedial process  
has not yet been finalised.  Version 1 - 22 June 2022
See www.productsafety.gov.au  for Australian product recall information
</excerpt>
### Rank 3 of 95 — 0.08
<excerpt title="Role of the ACCC and government in recalls">
## Sometimes another government agency leads the recall
### Agricultural and veterinary products, food, therapeutic goods, and road vehicles
For the following products, the specialist agency, and not the ACCC, is the lead agency for the recall and other safety issues.
For these products, the specialist agency:
*   assesses the recall and publishes the recall on its website  
*   decides whether to intervene in the recall and what actions to take.
The specialist agency’s guidelines, and not these guidelines, apply to the recall. Suppliers need to check the specialist agency’s recall guidelines, as updated from time to time, to understand what they have to do when conducting the recall.
| Product | Specialist (lead) agency | Recall resources |  
| --- | --- | --- |  
| Agricultural and veterinary chemical products | Australian Pesticides and Veterinary Medicines Authority | * Recall website * Guidelines For recalling Agricultural and Veterinary Chemical Products |  
| Food | Food Standards Australia New Zealand (FSANZ) is the coordinating authority working with the relevant state or territory food agency. | * Recall website * Food Industry Recall protocol Notification of the recall to the ACCC is done by FSANZ on behalf of the food business undertaking the recall. |  
| Therapeutic goods | Therapeutic Goods Administration | * Recall website * Uniform recall procedure for therapeutic goods |  
| Road vehicles and approved road vehicle parts | Department of Infrastructure, Transport, Regional Development, Communications, Sport and the Arts | * Recalls website * Recalls policy Recall notices for road vehicles and approved road vehicles parts are received by the Department, and not the ACCC, under the Australian Consumer Law. |

## Sometimes another government agency leads the recall
### Gas appliances, electrical and building products
For an electrical product, gas appliance or building product recall, a state or territory regulator is designated as the point of contact (home regulator).
For electrical products and gas appliances, the home regulator is usually the regulator located where the initial incident occurred or where the recalling supplier is located.
A number of things happen when a supplier notifies the ACCC of a recall:
*   The ACCC will seek advice from the home regulator to make sure that the wording in the recall notice is accurate and suitable to the risk. The ACCC will publish the agreed notice on the ACCC Product Safety website.  
*   Both the home regulator and the ACCC monitors the recall. Suppliers provide progress reports to both the home regulator and the ACCC. The home regulator liaises with the other state and territory regulators.  
*   Information given to us will usually be shared with the home regulator. This is to assist us in understanding the risk, hazard, use and misuse of the product.  
*   Both this guideline and the state and territory regulator’s guideline apply to the recall.
| Product | Specialist agency |  
| --- | --- |  
| Building products | For more information, contact your state and territory building and plumbing administrations.For suppliers in the Northern Territory, contact Northern Territory Consumer Affairs. |  
| Electrical products | For more information, contact your state or territory electrical safety regulator. The Electrical Regulatory Authorities Council Recall Guidelines published by the Electrical Regulatory Authorities Council also apply to the recall. |  
| Gas appliances | For more information, contact your state or territory gas appliance safety regulator. The Gas Technical Regulators Committee Recall Guidelines published by the Gas Technical Regulators Committee also apply to the recall. |

## Sometimes another government agency leads the recall
### Other products
For other products covered by a specialist regime, you need to contact the specialist agency to understand your obligations. This includes the following specialist agencies:
| Product | Specialist agency |  
| --- | --- |  
| Asbestos | State or territory work health safety regulator. |  
| Chemicals - industrial chemicals | Australian Industrial Chemicals Introduction Scheme |  
| Poisons | State and territory poisons regulators Some state and territory regulators may not have recall powers and may collaborate with state consumer affairs to recall a product. |
See more information about the Australian product safety system, including a list of specialist agencies.
</excerpt>
### Rank 4 of 95 — 0.06
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
### Rank 5 of 95 — 0.06
<excerpt title="ACCC: Home">
# We are Australia's national competition, consumer, fair trading and product safety regulator.
### We allege major Australian egg producers engaged in cartel and other anti-competitive conduct
We allege that since at least October 2020 key egg suppliers and producers coordinated on a range of business decisions in a way that likely substantially reduced competition for many years.The alleged conduct related to the production and supply of eggs including free-range, cage and organic eggs.

# We are Australia's national competition, consumer, fair trading and product safety regulator.
### Kmart in court over safety concerns with cosmetic nail glue and button battery products
We allege that Kmart sold millions of units of cosmetic nail glue without adequate warnings and thousands of units of button battery products which did not comply with mandatory standards.

# We are Australia's national competition, consumer, fair trading and product safety regulator.
### ACCC issues Linfox Armaguard with interim direction to support ongoing access to cash
The ACCC has today given Linfox Armaguard Pty Ltd (Armaguard) an interim direction that requires it to continue to supply cash in transit services and provide access to its facilities to its customers across Australia, and that sets the terms on which Armaguard provides these services.
View all news
> “We prioritise the issues impacting the Australian economy, consumers and businesses in Australia.”  
>   
>   
> ACCC Chair Gina Cass-Gottlieb

# We are Australia's national competition, consumer, fair trading and product safety regulator.
## Our priorities
### Mergers and acquisitions
A new mandatory merger control regime for notifying and assessing acquisitions is in effect from 1 January 2026.
Thenew regimeis designed to strengthen Australia’s merger control and provide more certainty and transparency.

# We are Australia's national competition, consumer, fair trading and product safety regulator.
## Our priorities
### Misleading pricing
Businesses must communicate clear and accurate prices prior to consumers booking, ordering or purchasing. They must not mislead consumers about their prices.

# We are Australia's national competition, consumer, fair trading and product safety regulator.
## Our priorities
### Greenwashing and environmental claims
Consumers are now, more than ever, making purchasing decisions on environmental grounds.
We'll be investigating a number of businesses for making potentially false or misleading environmental claims.

# We are Australia's national competition, consumer, fair trading and product safety regulator.
## Work on some of the biggest issues facing consumers and businesses.
Join our team of smart and dedicated people from all walks of life to collaborate on meaningful matters and make a significant and lasting impact for all of Australia.
Why work here?View all vacancies

# We are Australia's national competition, consumer, fair trading and product safety regulator.
## Related sites
### Product Safety
Find recalled products, safety information about different products, and report unsafe products.

# We are Australia's national competition, consumer, fair trading and product safety regulator.
## Related sites
### Scamwatch
Find out how to recognise, avoid and report scams.

# We are Australia's national competition, consumer, fair trading and product safety regulator.
## Related sites
### Consumer Data Right
Find out about the Consumer Data Right, which gives you the right to share your data between service providers of your choosing.
ACCC Consumer Rights FacebookACCC TwitterACCC InstagramACCC YouTubeACCC Linkedin
The ACCC acknowledges the Traditional Custodians of the lands across Australia on which we live and work. We acknowledge their connection to this Country and pay our respect to Elders past, present and emerging.

# We are Australia's national competition, consumer, fair trading and product safety regulator.
## Footer menu
ACCC © Commonwealth of Australia
*   Accessibility  
*   Cookies  
*   Disclaimer and copyright  
*   Glossary  
*   Vulnerability disclosure  
*   Privacy
</excerpt>

## Search 3 — query: "recall "gas products" "2020" site:productsafety.gov.au/recalls"
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

## Search 4 — query: ""Gas products and appliances" "PRA" 2020 productsafety.gov.au"
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

## Search 5 — query: ""Gas products and appliances" site:productsafety.gov.au/recalls 2020"
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

## Search 6 — query: "2020/ gas products and appliances "productsafety.gov.au/recalls""
### Rank 1 of 272 — 0.29 (passed on)
<excerpt title="Behavioural study on strategies to improve the effectiveness of product ...">
## [PDF page 52]
France  https://www.economie.gouv.fr/dgccrf/securite/avis-rappels-  
produits
Germany  www.rueckrufe.de
Hungary  https://fogyasztovedelem.kormany.hu/#/veszelyes_termekek_  
Iceland  https://www.neytendastofa.is/neytendur/solubonn-innkollun-  
voru/  
Ireland  https://www.ccpc.ie/consumers/product-safety/product-recalls/
Latvia  https://www.ptac.gov.lv/lv/jaunumi?category%5B103%5D=103
Luxembourg  https://portail-qualite.public.lu/fr/alertes.html
Malta  https://mccaa.org.mt/Section/Content?contentId=4407
45
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

## [PDF page 53]
Final report
Country  Link to the national recall database
The Netherlands  https://terugroepregister.rdw.nl/Pages/Terugroepregister.aspx  
(motor vehicles)
Norway  https://farligeprodukter.no/
Poland  http://publikacje.uokik.gov.pl/hermes3_pub/
Romania  https://anpc.ro/categorie/44/retrageri  -voluntare-de-produse
Slovenia  https://www.gov.si/zbirke/seznami/nevarni-proizvodi/  
https://www.konsumentverket.se/aktuellt/aterkallelser-av-  
varor/  
Sweden  https://www.elsakerhetsverket.se/privatpersoner/dina-  
elprodukter/forsaljningsforbud/ (electrical products)
Non-EU countries
Australia  https://www.productsafety.gov.au/recalls  
Canada  https://healthycanadians.gc.ca/recall-alert-rappel-avis/index-  
eng.php  
UK  https://productrecall.campaign.gov.uk/
US  https://www.cpsc.gov/Recalls
NZ  https://www.recalls.govt.nz/
Figure  20: Example of  the user-friendly national database for recalls and safety alerts  
(Canada)124
46
PDF link  
PDF link  
PDF link  
PDF link  
PDF link  
PDF link
</excerpt>
### Rank 2 of 272 — 0.28
<excerpt title="Behavioural study on strategies to improve the effectiveness of product ...">
## [PDF page 53]
Final report
Country  Link to the national recall database
The Netherlands  https://terugroepregister.rdw.nl/Pages/Terugroepregister.aspx  
(motor vehicles)
Norway  https://farligeprodukter.no/
Poland  http://publikacje.uokik.gov.pl/hermes3_pub/
Romania  https://anpc.ro/categorie/44/retrageri  -voluntare-de-produse
Slovenia  https://www.gov.si/zbirke/seznami/nevarni-proizvodi/  
https://www.konsumentverket.se/aktuellt/aterkallelser-av-  
varor/  
Sweden  https://www.elsakerhetsverket.se/privatpersoner/dina-  
elprodukter/forsaljningsforbud/ (electrical products)
Non-EU countries
Australia  https://www.productsafety.gov.au/recalls  
Canada  https://healthycanadians.gc.ca/recall-alert-rappel-avis/index-  
eng.php  
UK  https://productrecall.campaign.gov.uk/
US  https://www.cpsc.gov/Recalls
NZ  https://www.recalls.govt.nz/
Figure  20: Example of  the user-friendly national database for recalls and safety alerts  
(Canada)124
46
PDF link  
PDF link  
PDF link  
PDF link  
PDF link  
PDF link

## [PDF page 54]
Final report
Figure 21: Example of the user-friendly national database for recalls (Norway)125
Efforts are also made to make these databases more user  -friendly for mobile users and/or  
link them with mobile applications.
Indeed, mobile technology is the key to reach consumers according to the Health Canada  
report (2018). Canadians seem to prefer mob  ile communication compared to other means  
for this purpose. The Canadian Food and Safety Inspection Agency reported that 89% of  
visitors to their homepage were using mobile browsers. They also reported that 83% of  
the traffic to their recalls’ pages came f  rom Facebook126. In general, there are around 7  
million annual visits on the current recall safety portal, most of which are accessed via  
mobile.127  This led to a project aimed  at  optimising the public  recalls and safety alerts  
website. Initiated in 2018, the project entered a second round in 2019 with the aim to  
improve the search solution by using open source technology.  128
Additionally, some of the national authorities, such as Austria, France, the US and Canada  
have  undertaken  projects  to  develop  recall  app  s  to  facilitate  communication  with  
consumers. Below we provide some examples from these countries.
Figure 22: Example of the mobile app for recalls and safety alerts warnings (Austria)
126  Government  of  Canada  (2018),  Project  summary:  Recalls  and  safety  alerts,  available  at:  
https://blog.canada.ca/research  -summaries/recalls-research-summary.html  
127 Government of Canada (2018), Recalls and safety alerts: An optimization project to better protect Canadians,  
available at:  https://blog.canada.ca/2018/10/18/recalls-safety-alerts.html  
128 Government of Canada (2020), Research summary: Recalls and safety alerts search optimization, Round 2,  
available at: https://blog.canada.ca/research-summaries/recalls-safety-alerts-research-summary.html
47
</excerpt>
### Rank 3 of 272 — 0.16
<excerpt title="Product Recall">
*   Back to Home  
*   Back to Product Support  
*    Product Recall

## Black Tempered Glass Gas Cooktops (Certificate number AGA 8145 G)
WHG638BC & WHG958BC Electrolux Home Products Pty Ltd, is recalling Westinghouse Models WHG638BC & WHG958BC Black Tempered Glass Gas Cooktops. Supplied from February 2020. The model and serial number is visible on the base of the unit.
WHAT IS THE DEFECT? The glass in the cooktop does not comply with the Domestic Gas Cooking Appliances Standard. If the glass breaks it may shatter into fragments and shards that may hit people using the cooktop or people near by.
WHAT IS THE HAZARD? The glass may break into sharp fragments or shards and pose a risk of serious injury. **Incidents causing injury have occurred.**
ACTION REQUIRED? Consumers should check the model number of their cooktop to see if it is affected.
If it is a Westinghouse Black Glass Gas Cooktop Model WHG638BC or WHG958BC, please contact us here at Electrolux to arrange for a refund or for a service technician to attend free of charge to replace the product.
Please see https://www.productsafety.gov.au/recalls/electrolux-home-products-pty-ltd-%E2%80%94-westinghouse-black-tempered-glass-gas-cooktop for full details.
Please contact us by calling the toll-free number [1800 001 218](tel: 1800 001 218) between 8am and 7pm EST Mon-Fri or emailing us at [productrecall@electrolux.com](mailto:productrecall@electrolux.com).
For further information, please Download the recall notice.

## Book Service And Repair
Built by experts — repaired by experts, nobody knows your appliance better than us.
You can trust us to deliver the best possible quality of care, every day for both warranty and out of warranty service and repairs. That's our promise to you.
Built by experts — repaired by experts, nobody knows your appliance better than us.
You can trust us to deliver the best possible quality of care, every day for both warranty and out of warranty service and repairs. That's our promise to you.
No Results

## Book Service And Repair
### Contact Us
Our Customer Care team is available 7 days a week
MON to FRI 8AM - 7PM
SAT 9AM - 2PM
SUN 10AM - 2PM

## Book Service And Repair
### Enquire Online
Contact Westinghouse 24/7. Send us your comments or questions. We're always happy to help.

## Book Service And Repair
### Warranty Information
See what is covered in your appliance warranty and make sure you're covered.
</excerpt>
### Rank 4 of 272 — 0.16
<excerpt title="PRODUCT SAFETY RECALL WESTINGHOUSE WHG638BC & ...">
# IMPORTANT NOTICE:... - Westinghouse Appliances Australia | Facebook
## Westinghouse Appliances Australia's Post
Please contact us by calling the toll-free number 1800 001 218 between 8am and 7pm EST Mon-Fri or emailing us at productrecall@electrolux.com.
For full details,
please visit our website [https://www.westinghouse.com.au/support/product-recall/](https://l.facebook.com/l.php?u=https%3A%2F%2Fwww.westinghouse.com.au%2Fsupport%2Fproduct-recall%2F&h=AUC1gTgTyp4DLygO7kDF9GC99me6-REd4_ljJyerSr1MFxAg5cFqCx0h8PvX6CyCQlrf50WUokSkJQu5xhNWShsv9_oNDYwe5g3FsbSQHU56dYTxLGVkz6VeHFJluo97VJM4eMfgPFgSF0AmLzblm2lvzfMiNHt_HJDqxw&__tn__=-UK-R&c[0]=AUCXGVLXERR0nbfFNBiaAmUMmqNPaUDGDgvkUXXfJMz9xmLdHpnjnTGM59A75MGJPCiTlMnZSO_q1gZQhaakqoGVawNcjiept9SUg3w3SFyfjSN3dGbfu-a6dvG1bKIep-KTyUMyq4uOVdSHTSNa4KAokZmogqGz-V9Rc-xeDkynXreqrpltGt0o7Ha0k4c)

# IMPORTANT NOTICE:... - Westinghouse Appliances Australia | Facebook
## Westinghouse Appliances Australia's Post
or the product safety website [https://www.productsafety.gov.au/.../electrolux-home...](https://l.facebook.com/l.php?u=https%3A%2F%2Fwww.productsafety.gov.au%2Frecalls%2Felectrolux-home-products-pty-ltd-%25E2%2580%2594-westinghouse-black-tempered-glass-gas-cooktop&h=AUD8rMu_J6v2GHbhLuOaQYfmLL-DT5-nLH6yP0IB34dqfbnN8LxrASwT-7DKD-jt3nGn1mzZsjYKoDl-Uo3iGdQtAmN5ZLdqqhx_ofOmgrByfDMKXnFr3itOAae8a8xDc72M2TJR7tTNLYfpkF5j4sDKGXardsiTaM74sg&__tn__=-UK-R&c[0]=AUCXGVLXERR0nbfFNBiaAmUMmqNPaUDGDgvkUXXfJMz9xmLdHpnjnTGM59A75MGJPCiTlMnZSO_q1gZQhaakqoGVawNcjiept9SUg3w3SFyfjSN3dGbfu-a6dvG1bKIep-KTyUMyq4uOVdSHTSNa4KAokZmogqGz-V9Rc-xeDkynXreqrpltGt0o7Ha0k4c).
</excerpt>
### Rank 5 of 272 — 0.12
<excerpt title="PRODUCT SAFETY RECALL WESTINGHOUSE WHG638BC & ...">
# IMPORTANT NOTICE:... - Westinghouse Appliances Australia | Facebook
## Westinghouse Appliances Australia's Post
or the product safety website [https://www.productsafety.gov.au/.../electrolux-home...](https://l.facebook.com/l.php?u=https%3A%2F%2Fwww.productsafety.gov.au%2Frecalls%2Felectrolux-home-products-pty-ltd-%25E2%2580%2594-westinghouse-black-tempered-glass-gas-cooktop&h=AUD8rMu_J6v2GHbhLuOaQYfmLL-DT5-nLH6yP0IB34dqfbnN8LxrASwT-7DKD-jt3nGn1mzZsjYKoDl-Uo3iGdQtAmN5ZLdqqhx_ofOmgrByfDMKXnFr3itOAae8a8xDc72M2TJR7tTNLYfpkF5j4sDKGXardsiTaM74sg&__tn__=-UK-R&c[0]=AUCXGVLXERR0nbfFNBiaAmUMmqNPaUDGDgvkUXXfJMz9xmLdHpnjnTGM59A75MGJPCiTlMnZSO_q1gZQhaakqoGVawNcjiept9SUg3w3SFyfjSN3dGbfu-a6dvG1bKIep-KTyUMyq4uOVdSHTSNa4KAokZmogqGz-V9Rc-xeDkynXreqrpltGt0o7Ha0k4c).

# IMPORTANT NOTICE:... - Westinghouse Appliances Australia | Facebook
## Westinghouse Appliances Australia's Post
[](https://www.facebook.com/photo/?fbid=1489204783242987&set=pcb.3801347183322685&__cft__[0]=AZiM8DomYQ7b-zEeGGcwf-pNvKUGI5KUFuNYPcA0Rv6osisJ8_ntW_3n4POlgFvZTn85OIo8jvZng5Xu4YHV4vhjU-I-rz5-xBhkfVN_u8yJpoU34jbWaJiAk0Qihhdt8Gq7p02mVay3ACr0JwaCyuZUY8Nudnaa&__tn__=*b0H-R)
[](https://www.facebook.com/photo/?fbid=1489204786576320&set=pcb.3801347183322685&__cft__[0]=AZiM8DomYQ7b-zEeGGcwf-pNvKUGI5KUFuNYPcA0Rv6osisJ8_ntW_3n4POlgFvZTn85OIo8jvZng5Xu4YHV4vhjU-I-rz5-xBhkfVN_u8yJpoU34jbWaJiAk0Qihhdt8Gq7p02mVay3ACr0JwaCyuZUY8Nudnaa&__tn__=*b1H-R)
![Image 3](blob:http://localhost/85d8b181a20aeb64a3afc2f1c39d2480)
![Image 4](blob:http://localhost/b2a9e322d16c8b9e64f4456e8bf93e51)
All reactions:
7
23 comments
1 share
Like
Comment
Most relevant
</excerpt>

## Search 7 — query: "2020 gas products and appliances "recall" "productsafety.gov.au""
### Rank 1 of 127 — 0.30 (passed on)
<excerpt title="Product Recall">
*   Back to Home  
*   Back to Product Support  
*    Product Recall

## Black Tempered Glass Gas Cooktops (Certificate number AGA 8145 G)
WHG638BC & WHG958BC Electrolux Home Products Pty Ltd, is recalling Westinghouse Models WHG638BC & WHG958BC Black Tempered Glass Gas Cooktops. Supplied from February 2020. The model and serial number is visible on the base of the unit.
WHAT IS THE DEFECT? The glass in the cooktop does not comply with the Domestic Gas Cooking Appliances Standard. If the glass breaks it may shatter into fragments and shards that may hit people using the cooktop or people near by.
WHAT IS THE HAZARD? The glass may break into sharp fragments or shards and pose a risk of serious injury. **Incidents causing injury have occurred.**
ACTION REQUIRED? Consumers should check the model number of their cooktop to see if it is affected.
If it is a Westinghouse Black Glass Gas Cooktop Model WHG638BC or WHG958BC, please contact us here at Electrolux to arrange for a refund or for a service technician to attend free of charge to replace the product.
Please see https://www.productsafety.gov.au/recalls/electrolux-home-products-pty-ltd-%E2%80%94-westinghouse-black-tempered-glass-gas-cooktop for full details.
Please contact us by calling the toll-free number [1800 001 218](tel: 1800 001 218) between 8am and 7pm EST Mon-Fri or emailing us at [productrecall@electrolux.com](mailto:productrecall@electrolux.com).
For further information, please Download the recall notice.

## Book Service And Repair
Built by experts — repaired by experts, nobody knows your appliance better than us.
You can trust us to deliver the best possible quality of care, every day for both warranty and out of warranty service and repairs. That's our promise to you.
Built by experts — repaired by experts, nobody knows your appliance better than us.
You can trust us to deliver the best possible quality of care, every day for both warranty and out of warranty service and repairs. That's our promise to you.
No Results

## Book Service And Repair
### Contact Us
Our Customer Care team is available 7 days a week
MON to FRI 8AM - 7PM
SAT 9AM - 2PM
SUN 10AM - 2PM

## Book Service And Repair
### Enquire Online
Contact Westinghouse 24/7. Send us your comments or questions. We're always happy to help.

## Book Service And Repair
### Warranty Information
See what is covered in your appliance warranty and make sure you're covered.
</excerpt>
### Rank 2 of 127 — 0.28
<excerpt title="GAS SAFETY RECALL">
Title: PDF document  
URL Source: https://qga.org.au/images/blog/R-Gas%20Safety%20Recall%20-%20Swift%20Appliance%20Group%20500%20Series%20Cooker-Grill%20&%20Cooktops.pdf  
Markdown Content:

## [PDF page 1]
GAS SAFETY RECALL
Swift Appliance Group 500 Series Cooker/Grill and Cooktops
Model Numbers 502BHSP, 502BHFW, 502DHSP, 502RHSP, 502SHFW, 502SHW,  
502WBHSP, 503BHSPM, 503BHSP, 503BHSPMLG, 503BHSW, 503DHSP, 503RHSP,  
503SHSPM, 503SHSW and 503BHSPN
IDENTIFICATION: The information in this recall advertisement will be updated when more  
infomation is available.
Approval Number AGA  6488G - Data plate located on the inside front left side of the lid.
Products supplied to consumers, caravan, camper and motorhome manufacturers between  
01/01/2019 and 1/06/2020.
DEFECT: A part of the gas supply pipe may break or develop a hole.  This may cause a gas  
leak.
HAZARD: If the gas leaks in the presence of an ignition source this may lead to an explosion and/  
or fire, which may result in serious illness, injury or death. The defect has caused incidents that  
have caused serious injuries and burns.
If gas leaks and builds up in an enclosed area, such as a motorhome or caravan, asphyxiation  
may occur.
ACTION REQUIRED:  
Consumers should check if their appliance is affected and if so immediately turn off  the  
appliance and do not operate it  on gas. The gas supply to the appliance  can be isolated at the  
gas isolation valve, adjacent to the appliance  .
To identify affected appliances, open the glass lid and check the model number on the data  
plate that is on the inside front left side of the lid.
Consumers must ensure that Gas Cooker units are serviced and tested every 2-3 years.

## [PDF page 1]
For further information, consumers with affected appliances can contact Swift Appliance Group  
by  phone  on  0412  821  912  (Monday  to  Friday  9am  to  5pm),  via  email  at  
swiftrecall@outlook.com  or  visit  https://www.swiftappliancegroup.com.au to  register  
their details to be advised of remedial actions when they are available as the remedial process  
has not yet been finalised.  Version 1 - 22 June 2022
See www.productsafety.gov.au  for Australian product recall information
</excerpt>
### Rank 3 of 127 — 0.15
<excerpt title="Role of the ACCC and government in recalls">
## Sometimes another government agency leads the recall
### Agricultural and veterinary products, food, therapeutic goods, and road vehicles
For the following products, the specialist agency, and not the ACCC, is the lead agency for the recall and other safety issues.
For these products, the specialist agency:
*   assesses the recall and publishes the recall on its website  
*   decides whether to intervene in the recall and what actions to take.
The specialist agency’s guidelines, and not these guidelines, apply to the recall. Suppliers need to check the specialist agency’s recall guidelines, as updated from time to time, to understand what they have to do when conducting the recall.
| Product | Specialist (lead) agency | Recall resources |  
| --- | --- | --- |  
| Agricultural and veterinary chemical products | Australian Pesticides and Veterinary Medicines Authority | * Recall website * Guidelines For recalling Agricultural and Veterinary Chemical Products |  
| Food | Food Standards Australia New Zealand (FSANZ) is the coordinating authority working with the relevant state or territory food agency. | * Recall website * Food Industry Recall protocol Notification of the recall to the ACCC is done by FSANZ on behalf of the food business undertaking the recall. |  
| Therapeutic goods | Therapeutic Goods Administration | * Recall website * Uniform recall procedure for therapeutic goods |  
| Road vehicles and approved road vehicle parts | Department of Infrastructure, Transport, Regional Development, Communications, Sport and the Arts | * Recalls website * Recalls policy Recall notices for road vehicles and approved road vehicles parts are received by the Department, and not the ACCC, under the Australian Consumer Law. |

## Sometimes another government agency leads the recall
### Gas appliances, electrical and building products
For an electrical product, gas appliance or building product recall, a state or territory regulator is designated as the point of contact (home regulator).
For electrical products and gas appliances, the home regulator is usually the regulator located where the initial incident occurred or where the recalling supplier is located.
A number of things happen when a supplier notifies the ACCC of a recall:
*   The ACCC will seek advice from the home regulator to make sure that the wording in the recall notice is accurate and suitable to the risk. The ACCC will publish the agreed notice on the ACCC Product Safety website.  
*   Both the home regulator and the ACCC monitors the recall. Suppliers provide progress reports to both the home regulator and the ACCC. The home regulator liaises with the other state and territory regulators.  
*   Information given to us will usually be shared with the home regulator. This is to assist us in understanding the risk, hazard, use and misuse of the product.  
*   Both this guideline and the state and territory regulator’s guideline apply to the recall.
| Product | Specialist agency |  
| --- | --- |  
| Building products | For more information, contact your state and territory building and plumbing administrations.For suppliers in the Northern Territory, contact Northern Territory Consumer Affairs. |  
| Electrical products | For more information, contact your state or territory electrical safety regulator. The Electrical Regulatory Authorities Council Recall Guidelines published by the Electrical Regulatory Authorities Council also apply to the recall. |  
| Gas appliances | For more information, contact your state or territory gas appliance safety regulator. The Gas Technical Regulators Committee Recall Guidelines published by the Gas Technical Regulators Committee also apply to the recall. |

## Sometimes another government agency leads the recall
### Other products
For other products covered by a specialist regime, you need to contact the specialist agency to understand your obligations. This includes the following specialist agencies:
| Product | Specialist agency |  
| --- | --- |  
| Asbestos | State or territory work health safety regulator. |  
| Chemicals - industrial chemicals | Australian Industrial Chemicals Introduction Scheme |  
| Poisons | State and territory poisons regulators Some state and territory regulators may not have recall powers and may collaborate with state consumer affairs to recall a product. |
See more information about the Australian product safety system, including a list of specialist agencies.
</excerpt>
### Rank 4 of 127 — 0.11
<excerpt title="Conducting a consumer product safety recall">
## [PDF page 59]
Gas appliances, elec trical and building produc ts  
For an electrical product, gas appliance or building product recall, a state or territor y regulator is  
designated as the point of contact (home regulator).
For electrical products and gas appliances, the home regulator is usually the regulator located where  
the initial incident occurred or where the recalling supplier is located.
When a supplier notifies the ACCC of a recall  
	the ACCC will seek advice from the home regulator to make sure that the wording in the recall  
notice is accurate and suitable to the risk . The ACCC will publish the agreed notice on the Product  
S afet y Australia website  
	both the home regulator and the ACCC monitors the recall. Suppliers provide progress repor  ts  
to both the home regulator and the ACCC. The home regulator liaises with the other state and  
te r r i to r  y  r e g u l a to r s  
	information given to us will usually be shared with the home regulator. This is to assist us in  
understanding the risk , hazard, use and misuse of the product  
	both this guideline and the state and territor y regulator ’s guideline apply to the recall.
Product  Specialist agency
Building products  C ontact your state and territor y building and plumbing administrations fo r  
more information. For suppliers in the Nor thern Territor y, contact Nor thern  
Territor y Consumer Af fairs.
Electrical products  C ontact your state or territor y ele ctrical safet y regulator for more  
information.  
T he Ele ctrical Regulator y Authorities C ouncil Re call Guidelines published by  
the Ele ctrical Regulator y Authorities C ouncil also apply to the re call.
Gas appliances  C ontact your state or territor y gas appliance safet y regulator for more  
information.  
T he Gas Te chnical Regulators C ommit te e Re call Guidelines published by  
the Gas Te chnical Regulators C ommit te e also apply to the re call.
O ther produc ts  
For other products covered by a specialist regime, you need to contact the specialist agency to  
understand your obligations. This includes the following specialist agencies:
Product  Specialist agency
Asbestos  S tate or territor y work health safet y regulator.

## [PDF page 59]
Chemicals – Industrial  Australian Industrial Chemicals Introduction S cheme.  
chemic als
Poisons  S tate and territor y poisons regulators. S ome state and territor y regulators  
may not have re call powers and may collaborate with state consumer  
af fairs to re call a product.
You can find fur  ther information about the Australian product safet y system and a list of spe cialist  
agencies on the Product S afet y Australia website.
54
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
### Rank 5 of 127 — 0.10
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

## Search 8 — query: "site:productsafety.gov.au/recalls "Gas products and appliances" "2020""
### Rank 1 of 1 — 0.10 (passed on)
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

## Search 9 — query: ""2020/" "Gas products and appliances" site:productsafety.gov.au/recalls"
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

## Search 10 — query: ""2020/" "Gas products and appliances" "PRA number""
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

# Example 2
## Question
From the Space Shuttle program, for the space shuttle with the most number of orbital flights, how many Commanders commanded exactly two of those flights?

## Expected answer
5

## Grade 0.00

## Search 1 — query: "Space Shuttle orbital flight numbers by orbiter Discovery"
### Rank 1 of 119 — 0.60 (passed on)
<excerpt title="Space Shuttle orbiter">
## Shuttle Orbiter Specifications (OV-105)
### Operational orbiters
[edit]
*   _Columbia_ was first launched on April 12, 1981. On February 1, 2003, _Columbia_disintegrated during re-entry on its 28th spaceflight.

*   _Challenger_ was first launched on April 4, 1983. On January 28, 1986, it disintegrated 73 seconds after launch on its 10th mission.

*   _Discovery_ was first launched on August 30, 1984. It flew 39 missions, and was NASA's "Return to Flight" vehicle, following the accidental destructions of _Challenger_ and _Columbia_. _Discovery_ completed its last mission, STS-133, in March 2011. It is currently on display at the Smithsonian'sNational Air and Space Museum Steven F. Udvar-Hazy Center, near Dulles International Airport.

*   _Atlantis_ was first launched on October 3, 1985. It flew 33 spaceflights including the final Space Shuttle mission, STS-135, in July 2011.

*   _Endeavour_ was first launched on May 7, 1992. It flew 25 spaceflights, the final being STS-134, launched May 16, 2011.

## Shuttle Orbiter Specifications (OV-105)
### Operational orbiters
| Test Articles |  
| --- |  
| Picture | OVD | Name | Notes |  
|  | OV-095 | - | Simulator for actual flight hardware and software system testing and training located in the Shuttle Avionics Integration Laboratory |  
|  | OV-098[[a]](https://en.wikipedia.org/wiki/Space_Shuttle_orbiter#cite_note-52) | _Pathfinder_ | Orbiter simulator for moving and handling tests. Currently on display at the U.S. Space & Rocket Center. |  
|  | MPTA-098 | – | Testbed for propulsion and fuel delivery systems. Currently mounted onto Pathfinder at the U.S. Space & Rocket Center. |  
|  | STA-099 | – | Structural test article used for stress and thermal testing, later became _Challenger_ |  
|  | OV-101 | _Enterprise_ | First atmospheric free flight August 12, 1977. Used for approach and landing tests, not suitable for spaceflight. Formerly located at the Steven F. Udvar-Hazy Center, the orbiter is currently located on the flight deck of the USS _Intrepid_ (CV-11) at the Intrepid Sea, Air & Space Museum in New York City.[[27]](https://en.wikipedia.org/wiki/Space_Shuttle_orbiter#cite_note-NASA_release_11-107-27) |
In addition to the operational orbiters and test articles produced for use in the Shuttle program, there are also various mockup replicas on display throughout the United States:
Key  
‡Test vehicle  
†Lost

## Shuttle Orbiter Specifications (OV-105)
### Flight history timeline
[edit]
*   Space Shuttle for program history and description of operations  
*   Buran program (USSR's reusable shuttle program)  
*   Dream Chaser  
*   SpaceX Starship (spacecraft)
1.   ↑Unofficial honorary designation_[citation needed_]
</excerpt>
### Rank 2 of 119 — 0.57
<excerpt title="Space Shuttle orbiter">
## Shuttle Orbiter Specifications (OV-105)
### Orbiter Vehicle Designation
| Orbiter vehicles | Test articles |  
| --- | --- |  
| Designation | Vehicle | Designation | Vehicle |  
| OV-099[[a]](https://en.wikipedia.org/wiki/Space_Shuttle_orbiter#cite_note-45) | _Challenger_ | OV-095 | Shuttle Avionics Integration Laboratory (SAIL) mockup |  
| OV-101 | _Enterprise_ | STA-096 | ECLSS Structural Test Article |  
| OV-102 | _Columbia_ | STA-097 | Vibro Acoustic Structural Test Article |  
| OV-103 | _Discovery_ | OV-098[[b]](https://en.wikipedia.org/wiki/Space_Shuttle_orbiter#cite_note-46) | _Pathfinder_ |  
| OV-104 | _Atlantis_ | MPTA-098 | Main Propulsion Test Article |  
| OV-105 | _Endeavour_ |  |  
| 1. ↑Formerly known as **STA-099**. 2. ↑Retroactive honorary designation_[citation needed_] |

## Shuttle Orbiter Specifications (OV-105)
### Operational orbiters
[edit]
*   _Columbia_ was first launched on April 12, 1981. On February 1, 2003, _Columbia_disintegrated during re-entry on its 28th spaceflight.

*   _Challenger_ was first launched on April 4, 1983. On January 28, 1986, it disintegrated 73 seconds after launch on its 10th mission.

*   _Discovery_ was first launched on August 30, 1984. It flew 39 missions, and was NASA's "Return to Flight" vehicle, following the accidental destructions of _Challenger_ and _Columbia_. _Discovery_ completed its last mission, STS-133, in March 2011. It is currently on display at the Smithsonian'sNational Air and Space Museum Steven F. Udvar-Hazy Center, near Dulles International Airport.

*   _Atlantis_ was first launched on October 3, 1985. It flew 33 spaceflights including the final Space Shuttle mission, STS-135, in July 2011.

*   _Endeavour_ was first launched on May 7, 1992. It flew 25 spaceflights, the final being STS-134, launched May 16, 2011.
</excerpt>
### Rank 3 of 119 — 0.54
<excerpt title="Space Shuttle fleet">
### Challenger
_Challenger_ started its career as Structural Test Article STA-099. After studying the work needed to make _Enterprise_ space-worthy , NASA calculated that it was less expensive to rebuild STA-099 as OV-099.
_Challenger_ made its first flight on the STS-6 mission in April 1983 and became the workhorse of NASA's fleet during the early years of Shuttle operations: _Challenger_ flew on 85% of all missions up to 1985.
_Challenger_ was destroyed during the launch of its tenth mission, on 28 January 1986, killing all seven members of the crew.
It completed nine flights before the last ill-fated launch, totalling 62 days 07 hours 56 minutes 15 seconds. _Challenger_ orbited Earth 995 times.
* * *
The Space Shuttle Discovery approaches the International Space Station for docking

### Discovery
_Discovery_ (OV-103) was the hardest-working Shuttle, with 39 successful missions during 27 years of service since its debut in August 1984.
It was the third operational vehicle following _Columbia_ and _Challenger_, and had the honour of delivering the Hubble Space Telescope into orbit. It was the Shuttle tasked with the two ‘return to flight’ missions after the _Challenger_ and _Columbia_ accidents.
_Discovery_ was officially decommissioned after the STS-133 mission last February. After months of preparation, it will be handed over to the Smithsonian Institution’s National Air and Space Museum. _Discovery_ will replace _Enterprise_ at the Steven F. Udvar-Hazy Center in Virginia, near Washington Dulles Airport.
_Discovery_ made 5830 orbits and spent in total more than a year on missions: 365 days 12 hours 53 minutes 34 seconds.
* * *
View of Space Shuttle Atlantis ahead of the STS-122 mission

### Atlantis
_Atlantis_ (OV-104) was the fourth vehicle. Since October 1985 it has flown 32 missions and will make the last, STS-135.
In 1989, it deployed Magellan to Venus and Galileo to Jupiter; it lofted the Compton Gamma Ray Observatory to orbit in 1991. _Atlantis_ was the first Shuttle to dock with a space station, when it linked up with Russia’s Mir in 1995. It also delivered Europe’s Columbus laboratory to the International Space Station in 2008.
According to statistics, _Atlantis_ was built in about half the time it took to complete the first operational craft, _Columbia_. _Atlantis_ has had the fewest technical problems.
After its last flight, it will be handed over to the Kennedy Space Center Visitor Complex for display.
Before STS-135, _Atlantis_ has accumulated 293 days 18 hours 29 minutes 37 seconds in flight, and circled Earth 4648 times.
* * *
Endeavour landing at NASA's Kennedy Space Center, Florida

### Endeavour
_Endeavour_ (OV-105) is the youngest fleet member, making its maiden voyage in May 1992. It was built as a replacement for _Challenger_ (lost in 1986) using the spare structural parts of _Discovery_ and _Atlantis_.
It was the first Shuttle at the International Space Station, in 1998, delivering Node-1, the Station’s first US element.
_Endeavour_ flew its final mission last May, STS-134, and it has been decommissioned. Its Canadarm will be sent to Canada, and the Shuttle itself will be given to the California Science Center in Los Angeles – not far from Palmdale, where it was built, and Edwards Air Force Base, the second landing strip for returning Shuttles.
_Endeavour_ completed 25 missions with 4677 orbits and spent in total 296 days 2 hours 18 minutes 35 seconds in flight.
* * *

## Related links
### A video to the Space Shuttle from the European astronauts


## Related links
### Tribute page to the Space Shuttle
shuttle

## Related links
### Human Spaceflight
Leading Europe's human journey into the Solar System, with astronauts, robots and spacecraft as explorers.
</excerpt>
### Rank 4 of 119 — 0.53
<excerpt title="List of all Space Shuttle Flights">
### Orbital Flights
*    18. 51-G Discovery (3 comsats) Pad A Jun 17, 1985 (MORELOS-A; Arabsat A, Telstar 3D, Spartan)   
*    17. 51-B Challenger (Spacelab-3) Pad A May 6, 1985 (Spacelab-3)   
*    16. 51-D Discovery (2 Comsats) Pad A Apr 12, 1985 (TELESAT-I; SYNCOM IV-3)   
*    15. 51-C Discovery (DoD) Pad A Jan 24, 1984 (classified DoD 1)   
*    14. 51-A Discovery (2 Comsats) Pad A Nov 8, 1984 (TELESAT-H, SYNCOM IV -1)   
*    13. 41-G Challenger (ERBS, OSTA) Pad A Oct 5, 1985 (ERBS, OSTA-3)   
*    12. 41-D Discovery (3 Comsats) Pad A Sep 5, 1984 (SBS-D; SYNCOM IV-2; TELSTAR)   
*    11. 41-C Challenger (LDEF, SMM) Pad A Apr 13, 1984 (LDEF exposure, Solar Max repair)   
*    10. 41-B Challenger (Sats; MMU) Pad A Feb 3, 1984 (Westar 6, Palapa-B2; MMU EVAs)   
*    9. STS-9 Columbia (Spacelab-1) Pad A Nov 28, 1983 (Spacelab-1)   
*    8. STS-8 Challenger (Insat 1-B) Pad A Aug 30, 1983 (Insat 1-B)   
*    7. STS-7 Challenger (2 comsats) Pad A Jun 18, 1983 (Anik C-2, Palapa B1)   

### Orbital Flights
*    6. STS-6 Challenger (TDRS-1) Pad A Apr 4, 1983 (TDRS-1)   
*    5. STS-5 Columbia (ANIK, SBS) Pad A Nov 11, 1982 (Anik C-3, SBS-C)   
*    4. STS-4 Columbia (DoD/CFES) Pad A Jun 27, 1982 (DoD/CFES)   
*    3. STS-3 Columbia (OSS-1) Pad A Mar 22, 1982 (OSS-1 Pallet)   
*    2. STS-2 Columbia (OSTA-1) Pad A Nov 12, 1981 (OSTA-1 on Spacelab Pallet)   
*    1. STS-1 Columbia (STS Test) Pad A Apr 12, 1981 (First Shuttle Flight; system test)   
 International Space Station (ISS) flies in an orbit inclined 51.60 degrees to Earth's equator, as did Mir, while the Hubble Space Telescope (HST) is in a 28.47 degrees inclined orbit.
</excerpt>
### Rank 5 of 119 — 0.52
<excerpt title="List of all Space Shuttle Flights">
### Orbital Flights
*    42. STS-43 Atlantis (TDRS, SSBUV) Pad A Aug 2, 1991 (TDRS-E, SSBUV)   
*    41. STS-40 Columbia (SLS-1) Pad B Jun 5, 1991 (Spacelab SLS-1)   
*    40. STS-39 Discovery (DoD+sats) Pad A Apr 28, 1991 (class. DoD 8, AFP675, IBSS, SPAS-II)   
*    39. STS-37 Atlantis ([C]GRO) Pad B Apr 9, 1991 ([Compton] Gamma Ray Observatory)   
*    38. STS-35 Columbia (Astro-1) Pad B Dec 2, 1990 (Astro-1)   
*    37. STS-38 Atlantis (DoD) Pad A Nov 15, 1990 (classified DoD 7)   
*    36. STS-41 Discovery (Ulysses) Pad B Oct 6, 1990 (Ulysses)   
*    35. STS-31 Discovery (HST deploy) Pad B Apr 24, 1990 (Hubble Space Telescope - HST deploy)   
*    34. STS-36 Atlantis (DoD) Pad A Feb 28, 1990 (classified DoD 6)   
*    33. STS-32 Columbia (Syncom,LDEF) Pad A Jan 9, 1990 (SYNCOM IV-F5, LDEF Retrieval)   
*    32. STS-33 Discovery (DoD) Pad B Nov 22, 1989 (classified DoD 5)   
*    31. STS-34 Atlantis (Galileo) Pad B Oct 18, 1989 (Galileo, SSBUV)
</excerpt>

## Search 2 — query: "Discovery shuttle missions commander list STS-"
### Rank 1 of 179 — 0.43 (passed on)
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
### Rank 2 of 179 — 0.40
<excerpt title="Space Shuttle Information">
AUSSAT-2 Deployed three satellites.  
STS-61-C Columbia 12JAN1986 18JAN1986 6SATCOM-KU1
CHAMP Deployed SATCOM-KU1 satellite.  
STS-51-L Challenger 28JAN1986---0TDRS-A Explosion 73 seconds after liftoff.

Loss of vehicle and crew.  
STS-26 Discovery 29SEP1988 3OCT1988 4TDRS-C Deployment of TDRS-C (TDRS-3).  
STS-27 Atlantis 2DEC1988 6DEC1988 4LACROSSE-1 Classified DoD mission.  
STS-29 Discovery 13MAR1989 18MAR1989 5TDRS-D Deployment of TDRS-D (TDRS-4).  
STS-30 Atlantis 4MAY1989 8MAY1989 4Magellan / IUS Launch of Venus Radar Mapper.  
STS-28 Columbia 8AUG1989 13AUG1989 5SDS-B1 Classified DoD mission.  
STS-34 Atlantis 18OCT1989 23OCT1989 5Galileo / IUS Launch of Jupiter Orbiter.  
STS-33 Discovery 22NOV1989 27NOV1989 5ORION-2 Classified DoD mission.  
STS-32 Columbia 9JAN1990 20JAN1990 11SYNCOM IV-F5 LDEF Retrieval.  
STS-36 Atlantis 28FEB1990 4MAR1990 4Classified DoD mission.  
STS-31 Discovery 24APR1990 29APR1990 5HSTHubble Space Telescope deployment.  
STS-41 Discovery 6OCT1990 10OCT1990 4Ulysses Launch of Solar Probe.  
STS-38 Atlantis 15NOV1990 20NOV1990 5SDS-B2 Classified DoD mission.  
STS-35 Columbia 2DEC1990 10DEC1990 9ASTRO-1 Astronomical observations.  
STS-37 Atlantis 5APR1991 11APR1991 6GRO Deployment of the Compton Gamma Ray Observatory.
</excerpt>
### Rank 3 of 179 — 0.35
<excerpt title="Space Shuttle Information">
Deployed OAST-1 solar wing.  
STS-41-G Challenger 5OCT1984 13OCT1984 8OSTA-3
ERBS Deployed two satellites.
Conducted Orbital Refueling experiment.  
STS-51-A Discovery 8NOV1984 16NOV1984 8ANIK-D2
LEASAT-1 Deployed two satellites.
Retrieved PALAPA-B2 and WESTAR-VI.  
STS-51-C Discovery 24JAN1985 27JAN1985 3DoD 85-1 DoD mission.  
STS-51-D Discovery 12APR1985 19APR1985 7LEASAT-3
ANIK-E2 Deployed two satellites.  
STS-51-B Challenger 29APR1985 6MAY1985 7Spacelab-3 Spacelab-3.  
STS-51-G Discovery 17JUN1985 24JUN1985 7MORELOS-A
ARABSAT-1B
TELSTAR-3D Deployed three satellites.  
STS-51-F Challenger 29JUL1985 6AUG1985 8Spacelab-2 Spacelab-2.  
STS-51-I Discovery 27AUG1985 3SEP1985 7ASC-1
AUSSAT-1
LEASAT-4 Deployed three satellites.
Repaired and redeployed LEASAT-3.  
STS-51-J Atlantis 3OCT1985 7OCT1985 4DoD Mission.  
STS-61-A Challenger 30OCT1985 6NOV1985 7Spacelab-D1 German Spacelab mission.
Eight person crew.  
STS-61-B Atlantis 26NOV1985 3DEC1985 7MORELOS-B
SATCOM-KU2

AUSSAT-2 Deployed three satellites.  
STS-61-C Columbia 12JAN1986 18JAN1986 6SATCOM-KU1
CHAMP Deployed SATCOM-KU1 satellite.  
STS-51-L Challenger 28JAN1986---0TDRS-A Explosion 73 seconds after liftoff.
</excerpt>
### Rank 4 of 179 — 0.32
<excerpt title="Space Shuttle Information">
STS-112 Atlantis 7OCT2002 18OCT2002 11S1 TrussISS Assembly Mission 9A  
STS-113 Endeavour 23NOV2002 7DEC2002 14P1 TrussISS Assembly Mission 11A  
STS-107 Columbia 16JAN2003 1FEB2003 16SpaceHab-DM Columbia was destroyed during re-entry.  
STS-114 Discovery 26JUL2005 9AUG2005 14MPLMISS Assembly Mission LF 1  
STS-121 Discovery 4JUL2006 17JUL2006 13MPLMISS Assembly Mission ULF 1.1  
STS-115 Atlantis 9SEP2006 21SEP2006 12P3/P4 TrussISS Assembly Mission 12A  
STS-116 Discovery 9DEC2006 22DEC2006 13P5 TrussISS Assembly Mission 12A.1  
STS-117 Atlantis 8JUN2007 22JUN2007 14S3/S4 TrussISS Assembly Mission 13A  
STS-118 Endeavour 8AUG2007 21AUG2007 13S5 TrussISS Assembly Mission 13A.1  
STS-120 Discovery 23OCT2007 7NOV2007 15Node 2ISS Assembly Mission 10A  
STS-122 Atlantis 7FEB2008 20FEB2008 13Columbus LabISS Assembly Mission 1E  
STS-123 Endeavour 11MAR2008 26MAR2008 16ELM-PSISS Assembly Mission 1J/A  
STS-124 Discovery 31MAY2008 14JUN2008 14Kibo PM
</excerpt>
### Rank 5 of 179 — 0.32
<excerpt title="List of all Space Shuttle Flights">
### Orbital Flights
*    42. STS-43 Atlantis (TDRS, SSBUV) Pad A Aug 2, 1991 (TDRS-E, SSBUV)   
*    41. STS-40 Columbia (SLS-1) Pad B Jun 5, 1991 (Spacelab SLS-1)   
*    40. STS-39 Discovery (DoD+sats) Pad A Apr 28, 1991 (class. DoD 8, AFP675, IBSS, SPAS-II)   
*    39. STS-37 Atlantis ([C]GRO) Pad B Apr 9, 1991 ([Compton] Gamma Ray Observatory)   
*    38. STS-35 Columbia (Astro-1) Pad B Dec 2, 1990 (Astro-1)   
*    37. STS-38 Atlantis (DoD) Pad A Nov 15, 1990 (classified DoD 7)   
*    36. STS-41 Discovery (Ulysses) Pad B Oct 6, 1990 (Ulysses)   
*    35. STS-31 Discovery (HST deploy) Pad B Apr 24, 1990 (Hubble Space Telescope - HST deploy)   
*    34. STS-36 Atlantis (DoD) Pad A Feb 28, 1990 (classified DoD 6)   
*    33. STS-32 Columbia (Syncom,LDEF) Pad A Jan 9, 1990 (SYNCOM IV-F5, LDEF Retrieval)   
*    32. STS-33 Discovery (DoD) Pad B Nov 22, 1989 (classified DoD 5)   
*    31. STS-34 Atlantis (Galileo) Pad B Oct 18, 1989 (Galileo, SSBUV)
</excerpt>

## Search 3 — query: "Discovery STS mission commander list"
### Rank 1 of 196 — 0.67 (passed on)
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
### Rank 2 of 196 — 0.36
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
### Rank 3 of 196 — 0.34
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
### Rank 4 of 196 — 0.31
<excerpt title="Space Shuttle Mission Chronology: Part 1 — 1999-2011">
Crew consisted of Commander Steven W. Lindsey, Mission Specialist Piers J. Sellers, Pilot Mark E. Kelly, Mission Specialists Thomas Reiter, Lisa M. Nowak, Stephanie D. Wilson and Michael E. Fossum.
**2005**
**STS-114 Return to Flight**
**Mission:** International Space Station Assembly Flight LF1
**Space Shuttle:**Discovery
**Launch Pad:**39B
**Launched:**July 26, 2005, 10:39:00 a.m. EDT
**Landing Site:**Edwards Air Force Base, Calif.
**Landing:**Aug. 9, 2005, 5:11:22 a.m. PDT
**Mission Duration:**13 days, 21 hours, 32 minutes and 48 seconds
Discovery's seven-member Return to Flight crew arrived at the International Space Station on July 28. The crewmembers' primary objectives were to test and evaluate new safety procedures and conduct assembly and maintenance tasks on the Station. A late addition to the timeline tasked the crew with first ever on-orbit repair of the Shuttle heat shield.
Two crewmembers, Steve Robinson and Soichi Noguchi, ventured outside the Shuttle three times on spacewalks.
Crew consisted of Commander Eileen Collins, Pilot James Kelly, Mission Specialists Charles Camarda, Wendy Lawrence, Soichi Noguchi, Stephen Robinson and Andrew Thomas.
**2003**
**STS-107**
**Mission:** Space Research
**Space Shuttle:**Columbia
**Launch Pad:**39A
**Launched:**Jan. 16, 2003, 9:39 a.m. CST
**Mission Duration:**15 days, 22 hours, 20 minutes
Columbia and crew lost during entry 16 minutes before landing Feb. 1, 2003
**Orbit Altitude:**150 nautical miles
**Orbit Inclination:**39 degrees
Columbia broke up during re-entry over East Texas at about 9 a.m. EST, February 1, 2003, 16 minutes prior to the scheduled touchdown at Kennedy Space Center, Fla. A seven-month investigation followed, including a four month search across Texas to recover debris.
</excerpt>
### Rank 5 of 196 — 0.30
<excerpt title="Five astronauts launched aboard the Space Shuttle Discovery on March ...">
# Five... - Blast From The Past: Space Shuttle Program | Facebook
[March 10](https://www.facebook.com/Shuttle1701/posts/pfbid0j3bfng1KzFLmGcRbqovJSS6mhk9ZNBT7CgbcTZf5onXQMon1a2JapXDEs6LYmJHl?__cft__[0]=AZg5TTqDhijsvb18wvrtKkR7c9IJZm2b5jBBVRwxsYvwFE-BMDqddvnA_3oyvoHeFkp2aLT31NA3HYVHs14gmJeevfWclxpsHEpntbzGrK6cnbyXzxOdGL64MK2DcsE6yf5HYEWAR4ysqrzbkjVR7AxwPouLRjC1&__tn__=%2CO%2CP-R) ·
Five astronauts launched aboard the Space Shuttle Discovery on March 13, 1989 at 9:57 am (EST) for the STS-29 mission. Included were James P. Bagian, mission specialist 1; Robert C. Springer, mission specialist 3; James F. (Jim) Buchli, mission specialist 2; John E. Blaha, pilot; and Michael L. Coats, commander. The mission’s primary payload was the Tracking and Data Relay Satellite-4 (TDRS-4). Photo credit: NASA.
[](https://www.facebook.com/photo/?fbid=1449308213905690&set=a.463704965799358&__cft__[0]=AZg5TTqDhijsvb18wvrtKkR7c9IJZm2b5jBBVRwxsYvwFE-BMDqddvnA_3oyvoHeFkp2aLT31NA3HYVHs14gmJeevfWclxpsHEpntbzGrK6cnbyXzxOdGL64MK2DcsE6yf5HYEWAR4ysqrzbkjVR7AxwPouLRjC1&__tn__=EH-R)

# Five... - Blast From The Past: Space Shuttle Program | Facebook
![Image 2](blob:http://localhost/85d8b181a20aeb64a3afc2f1c39d2480)
![Image 3](blob:http://localhost/2b45e6f1a2ae097354c0b291152873d5)
All reactions:
396
3 comments
21 shares
Like
Comment
Blast From The Past: Space Shuttle Program limited who can comment on this post.
Most relevant
[](https://www.facebook.com/joe.prowse.871128?comment_id=Y29tbWVudDoxNDQ5MzA4Mjc3MjM5MDE3Xzc4NDUwNjg3NzYwNTIyMg%3D%3D&__cft__[0]=AZg5TTqDhijsvb18wvrtKkR7c9IJZm2b5jBBVRwxsYvwFE-BMDqddvnA_3oyvoHeFkp2aLT31NA3HYVHs14gmJeevfWclxpsHEpntbzGrK6cnbyXzxOdGL64MK2DcsE6yf5HYEWAR4ysqrzbkjVR7AxwPouLRjC1&__tn__=R]-R)
</excerpt>

## Search 4 — query: "List of Space Shuttle missions Discovery commander"
### Rank 1 of 137 — 0.57 (passed on)
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
### Rank 2 of 137 — 0.34
<excerpt title="Space Shuttle Mission Chronology: Part 1 — 1999-2011">
**Mission:**Hubble Space Telescope Servicing
**Space Shuttle:**Discovery
**Launch Pad:**39B
**Launched:**Dec. 19, 1999, 6:50 p.m. CST
**Launch Launch Window:**42 minutes
**EVAs:**3 spacewalks
**Landing:**Dec. 27, 1999, 6:01 p.m. CST
**Mission Duration:**7 days, 23 hours,10 minutes, 47 seconds
In December 1999, Space Shuttle Discovery spent eight days in orbit on a mission to service the Hubble Space Telescope. Two teams of space walkers spent more than 24 hours conducting extravehicular activities, or EVAs, installing new equipment and performing other maintenance tasks to upgrade the space-based observatory.
The seven-member crew was commanded by Curtis Brown and piloted by Scott Kelly. Jean-Francois Clervoy was the primary robotic arm operator, and the four space walkers were Mike Foale, John Grunsfeld, Claude Nicollier and Steve Smith. Clervoy and Nicollier represented the European Space Agency.
**STS-93
Mission:**Chandra X-Ray Observatory Deployment
**Space Shuttle:**Columbia
**Launch Pad:**39B
**Launched:**July 22, 1999**,**11:31 p.m. CDT
**Launch Window:**116 minutes
**Landing:**July 27, 1999**,**10:20 pm CDT
**Mission Duration:**4 days, 22 hours, 50 minutes
The purpose of the five-day mission was to deploy the Chandra X-Ray Observatory.
However, when Columbia reached orbit, it was 11 kilometers (7 miles) short of its target. This was due to premature main engine cutoff an instant before the scheduled cutoff. Columbia eventually reached its proper altitude and continued its mission.
On Flight Day 1, the shuttle crew successfully deployed Chandra. The observatory was propelled into orbit by a two-stage Inertial Upper Stage, or IUS.
During the rest of the mission the crew activated secondary payloads and experiments, including the Southwest Ultraviolet Imaging System which was used to capture ultraviolet imagery of Earth, the Moon, Mercury, Venus and Jupiter.
</excerpt>
### Rank 3 of 137 — 0.34
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
### Rank 4 of 137 — 0.33
<excerpt title="Space Shuttle Mission Chronology: Part 1 — 1999-2011">
Crew consisted of Commander Steven W. Lindsey, Mission Specialist Piers J. Sellers, Pilot Mark E. Kelly, Mission Specialists Thomas Reiter, Lisa M. Nowak, Stephanie D. Wilson and Michael E. Fossum.
**2005**
**STS-114 Return to Flight**
**Mission:** International Space Station Assembly Flight LF1
**Space Shuttle:**Discovery
**Launch Pad:**39B
**Launched:**July 26, 2005, 10:39:00 a.m. EDT
**Landing Site:**Edwards Air Force Base, Calif.
**Landing:**Aug. 9, 2005, 5:11:22 a.m. PDT
**Mission Duration:**13 days, 21 hours, 32 minutes and 48 seconds
Discovery's seven-member Return to Flight crew arrived at the International Space Station on July 28. The crewmembers' primary objectives were to test and evaluate new safety procedures and conduct assembly and maintenance tasks on the Station. A late addition to the timeline tasked the crew with first ever on-orbit repair of the Shuttle heat shield.
Two crewmembers, Steve Robinson and Soichi Noguchi, ventured outside the Shuttle three times on spacewalks.
Crew consisted of Commander Eileen Collins, Pilot James Kelly, Mission Specialists Charles Camarda, Wendy Lawrence, Soichi Noguchi, Stephen Robinson and Andrew Thomas.
**2003**
**STS-107**
**Mission:** Space Research
**Space Shuttle:**Columbia
**Launch Pad:**39A
**Launched:**Jan. 16, 2003, 9:39 a.m. CST
**Mission Duration:**15 days, 22 hours, 20 minutes
Columbia and crew lost during entry 16 minutes before landing Feb. 1, 2003
**Orbit Altitude:**150 nautical miles
**Orbit Inclination:**39 degrees
Columbia broke up during re-entry over East Texas at about 9 a.m. EST, February 1, 2003, 16 minutes prior to the scheduled touchdown at Kennedy Space Center, Fla. A seven-month investigation followed, including a four month search across Texas to recover debris.
</excerpt>
### Rank 5 of 137 — 0.32
<excerpt title="Space Shuttle Mission Chronology: Part 1 — 1999-2011">
**2007**
**STS-120
Launched:**Oct. 23, 2007, 11:38 a.m. EDT
**Landing:**Nov. 7, 2007, 1:01 p.m. EST
**Space Shuttle:**Discovery
**Mission Number:**STS-120 (120th space shuttle flight)
**Launch Launch Window:**10 minutes
**Launch Pad:**39A
**Mission Duration:**15 days, 2 hours, 23 minutes
**Landing Site:**KSC
**Inclination/Altitude:**51.6 degrees/122 nautical miles
**Primary Payload:**23rd station flight (10A), U.S. Node 2
STS-120 was the 23rd shuttle mission to the International Space Station, and launched an Italian-built U.S. multi-port module for the station.
Retired Air Force Col. Pamela A. Melroy commanded the STS-120 mission which took the Harmony Node 2 connecting module to the station. Melroy, a veteran shuttle pilot, was the second woman to command a shuttle. Marine Corps Col. George D. Zamka served as pilot. The flight's mission specialists were Scott E. Parazynski, Army Col. Douglas H. Wheelock, Stephanie D. Wilson and Paolo A. Nespoli, a European Space Agency astronaut from Italy. Zamka, Wheelock and Nespoli were making their first spaceflight.
Expedition 15/16 Flight Engineer Clayton Anderson returned to Earth from the space station aboard shuttle mission STS-120. That flight carried his replacement, Daniel Tani, to the station.
**STS-118
Launched:**Aug. 8, 2007, 6:36 p.m. EDT
**Landing:**Aug. 21, 2007, 12:33 p.m. EDT
**Space Shuttle:**Endeavour
**Mission Number:**STS-118 (119th space shuttle flight)
**Launch Launch Window:**10 minutes
**Launch Pad:**39A
**Mission Duration:**12 days, 17 hours, 55 minutes
**Landing Site:**KSC

**Inclination/Altitude:**51.6 degrees/122 nautical miles
**Primary Payload:**22nd station flight (13A.1), S5 Truss
Space Shuttle Endeavour's STS-118 mission was the 22nd shuttle flight to the International Space Station. It continued space station construction by delivering a third starboard truss segment.
U.S. Navy Commander Scott J. Kelly commanded the seven-person crew of STS-118. U.S. Marine Corps Colonel Charles O. Hobaugh was Endeavour's pilot. Veteran astronauts Richard A. Mastracchio and Dr. Dafydd (Dave) Williams of the Canadian Space Agency returned to space for their second missions. Barbara R. Morgan, Tracy E. Caldwell, Ph. D., and Benjamin Alvin Drew rounded out the crew as mission specialists.
**STS-117
Launched:**June 8, 2007, 7:38 p.m. EDT
**Landing:**June 22, 2007, 3:49 p.m. EDT
**Space Shuttle:**Atlantis
**Mission Number:**STS-117 (118th shuttle flight)
**Launch Launch Window:**10 minutes
**Launch Pad:**39A
**Mission Duration:**14 days
**Landing Site:**Edwards Air Force Base, Calif.
**Inclination/Altitude:**51.6 degrees/122 nautical miles
**Primary Payload:**21st station flight (13A), S3/S4 Truss
Frederick Sturckow, a Marine colonel, commanded STS-117. The mission delivered the second and third starboard truss segments (S3/S4) and another pair of solar arrays to the space station. Pilot Lee Archambault, an Air Force colonel, joined Sturckow in the shuttle’s cockpit. Mission specialists James Reilly II, Ph.D., Patrick Forrester, Steven Swanson, Ph.D., and John D. Olivas, Ph.D., rounded out the crew. STS-117 was the 21st shuttle mission to the International Space Station.
</excerpt>

## Search 5 — query: ""Discovery" STS commander""
### Rank 1 of 66 — 0.36 (passed on)
<excerpt title="Remembering Henry Warren “Hank” Hartsfield, Jr. Discovery's First ...">
Henry W. “Hank” Hartsfield, Jr.: USAF Pilot, NASA Astronaut, Executive.
Henry “Hank” Hartsfield served as commander of the first mission of Space Shuttle _Discovery_, now on display at the Museum’s Steven F. Udvar-Hazy Center. The six-day STS-41D mission began on August 30, 1984. An earlier launch attempt ended with the first on-the-pad abort just four seconds before launch. The first _Discovery_ crew successfully deployed three communications satellites, tested a towering solar array, and used the IMAX® motion picture camera in orbit.
The crew _of Discovery_’s first mission, STS-41D, 1984:
Charles D. Walker and Judith A. Resnik behind (l to r) Richard M. (Mike) Mullane, Steven A. Hawley, Henry W. Hartsfield, Jr. and Michael L. Coats.
Hartsfield loading film into the IMAX camera on the STS-41D mission.
Hartsfield was the first native of Alabama to become an astronaut. He graduated from the USAF Test Pilot School and served in the Air Force for 22 years. He logged more than 7,400 hours flying time, mostly in fighter jets (F-86, F-100, F-104, F-105, F-106) and in the T-33 and T-38 training jets. He was selected to be a military astronaut in the USAF Manned Orbital Laboratory program but was reassigned to NASA in 1969 when it was cancelled. As an astronaut Hartsfield supported the Apollo 16 mission and three Skylab missions before transitioning to the orbital flight test team for the new space shuttle program. His first spaceflight occurred in 1982; with commander Thomas K. Mattingly, he piloted _Columbia_ on its fourth and final orbital test flight, STS-4. President Ronald Reagan greeted the crew upon landing, and NASA declared the shuttle “operational” – ready for routine spaceflight.
STS-4 pilot Hartsfield (left) and commander T.K. Mattingly.

President and First Lady Reagan share a meeting with Astronauts Thomas K. Mattingly II, right, and Henry W. Hartsfield Jr., after the successful landing of the Space Shuttle Columbia at Edwards Air Force Base. Besides the Columbia, pictures, the new Space Shuttle Challenger and the Enterprise (vehicle used for test flights in the lower atmosphere in 1977), were also present at Edwards AFB. The latter served as a backdrop for the President’s podium from which he made a brief speech.
The _Discovery_ mission was his second flight. Hartsfield flew his last shuttle mission on _Challenger_ as commander of STS-61A in 1985, the last successful flight of this vehicle. This scientific research mission carried more than 75 experiments. Designated Spacelab D-1, it was the first shuttle mission operated for Germany and the European Space Agency, and it was the first with an eight-member crew. Altogether he spent 483 hours (20 days) in space.
The crew of STS-61A:
(l to r, front) Reinhard Furrer, Bonnie J. Dunbar, James F. Buchli, Henry W. Hartsfield Jr
(l to r, back) Steven R. Nagel, Guion S. Bluford Jr., Ernst Messerschmid, Wubbo Ockels
After the 1986 _Challenger_ tragedy, Hartsfield held a series of NASA management positions until 1998. He worked on the International Space Station program and the future-oriented Human Exploration and Development of Space enterprise before moving on to become an executive with Raytheon Corp. until his retirement in 2005. He received numerous military and civilian awards during his long career.
Comments? Contact Us

## You may also like
</excerpt>
### Rank 2 of 66 — 0.30
<excerpt title="STS-133">
**STS-133** (ISS assembly flight **ULF5**)[[6]](https://en.wikipedia.org/wiki/STS-133#cite_note-manifest-6) was the 133rd mission in NASA's Space Shuttle program; during the mission, Space Shuttle _Discovery_ docked with the International Space Station. It was _Discovery_'s 39th and final mission. The mission launched on February 24, 2011, and landed on March 9, 2011. The crew consisted of six American astronauts, all of whom had been on prior spaceflights, headed by Commander Steven Lindsey. The crew joined the long-duration six person crew of Expedition 26, who were already aboard the space station.[[7]](https://en.wikipedia.org/wiki/STS-133#cite_note-sched-7) About a month before lift-off, one of the original crew members, Tim Kopra, was injured in a bicycle accident. He was replaced by Stephen Bowen.
The mission transported several items to the space station, including the Permanent Multipurpose Module_Leonardo_, which was left permanently docked to one of the station's ports. The shuttle also carried the third of four ExPRESS Logistics Carriers to the ISS, as well as a humanoid robot called Robonaut.[[8]](https://en.wikipedia.org/wiki/STS-133#cite_note-outerspace-20110219-8) The mission marked both the 133rd flight of the Space Shuttle program and the 39th and final flight of _Discovery_, with the orbiter completing a cumulative total of a whole year (365 days) in space.
The mission was affected by a series of delays due to technical problems with the external tank and, to a lesser extent, the payload. The launch, initially scheduled for September 2010, was pushed back to October, then to November, then finally to February 2011.

NASA announced the STS-133 crew on September 18, 2009, and training began in October 2009. The original crew consisted of commander Steven Lindsey, pilot Eric Boe, and mission specialists Alvin Drew, Timothy Kopra, Michael Barratt, and Nicole Stott. However, on January 19, 2011, about a month before launch, it was announced that Stephen Bowen would replace original crew member Tim Kopra, after Kopra was injured in a bicycle accident.[[11]](https://en.wikipedia.org/wiki/STS-133#cite_note-koprareplacement-11) All six crew members had flown at least one spaceflight before; five of the crew members, all but commander Steven Lindsey, were part of NASA's Astronaut Group 18, all being selected in the year 2000.[[12]](https://en.wikipedia.org/wiki/STS-133#cite_note-12)
The mission commander, Steven Lindsey, handed over his position as Chief of the Astronaut Office position to Peggy Whitson in order to lead the mission.[[13]](https://en.wikipedia.org/wiki/STS-133#cite_note-133crew-13) For the first time, two mission crew members were in space when a crew assignment announcement was made, as Nicole Stott and Michael Barratt were aboard the ISS as part of the Expedition 20 crew.[[13]](https://en.wikipedia.org/wiki/STS-133#cite_note-133crew-13) During STS-133, Alvin Drew became the last African-American astronaut to fly on the Space Shuttle, as no African-Americans were among the crews of STS-134 and STS-135. Having flown onboard _Atlantis_'STS-132 mission, Bowen became the first and the only NASA astronaut to be launched on two consecutive missions, until Doug Hurley launched aboard Crew Dragon Demo-2 in May 2020, after having previously launched on STS-135.
*
The crew poses for a photo at the KSC (including Bowen).
*
Mission poster (with Kopra instead of Bowen).
*

Lindsey, far left, presents a montage to Barack Obama as crew members Barratt, Boe, Stott and Bowen look on.
</excerpt>
### Rank 3 of 66 — 0.28
<excerpt title="Our annual tribute series honoring lost astronauts and cosmonauts ...">
# Space Hipsters | Our annual tribute series honoring lost astronauts and cosmonauts continues with Sam Mundell honoring STS-107 commander Rick Husband, lost with Columb... | Facebook
His Air Force career saw him gain 3800 flight hours, and he was a fight instructor and test pilot.
However, higher and faster was calling, and Rick made a number of attempts to realise his boyhood dream. Application number four was the lucky one...and Rick was selected for the Astronaut Corps in December 1994.
His first mission was on STS-96 Discovery (pilot) and he spent 10 days in space.
Rick was assigned to STS-107 Columbia as its commander and the launch was on Jan 16th 2003. Rick and the crew spent 16 days in space, carrying out a number of experiments.
During re-entry on 1 Feb 2003, Columbia broke up, and Rick and the rest of the crew died.
Rick was survived by his wife and two children.
His memory lives on, Asteroid 51823Rickhusband is named after him, as is SS Rick Husband, the Cygnus CRS OA-6 unmanned re-supply ship.
Sources: spaceflight inside
NASA
Tshaonline
![Image 5](blob:http://localhost/c228214878b3eaebe7a83f7398b606a3)
![Image 6](blob:http://localhost/85d8b181a20aeb64a3afc2f1c39d2480)
![Image 7](blob:http://localhost/2b45e6f1a2ae097354c0b291152873d5)
All reactions:
35
1 comment
Like
Comment
Share
Most relevant
Brent Casteel
Eternal in our hearts and memories...

# Space Hipsters | Our annual tribute series honoring lost astronauts and cosmonauts continues with Sam Mundell honoring STS-107 commander Rick Husband, lost with Columb... | Facebook
*   [2y](https://www.facebook.com/groups/spacehipsters/posts/7364359990275487/?comment_id=7374234265954726&__cft__[0]=AZjzV7n4tcoNkjo6QZl1VYdv2dCYrqrXcE8NAGvLTtcA2QsB4GWU3ojptS0GWF0otj0BxGD5Cu9bg560NXn1KU6WhQKsw4gnDgPi6J9IeiwtYBpMoqgt6WndCRPz7_e_3T_ZCbI17zaghL36iflGe2cZOw-7XtNYWmgp6whfgR11Ov6kz84tkB2T5FrbBlst7IgLnkHOae8Tmbwr_bXQeSGSFFQy&__tn__=R]-R)
See more on Facebook
See more on Facebook
Email or phone number
Password
Log In
Forgot password?
or
Create new account
</excerpt>
### Rank 4 of 66 — 0.28
<excerpt title="DoD Support to STS-114 (Discovery, LF1)">
U.S. Northern Command is the focal point for military emergency support to the Space Shuttle. Support includes astronaut rescue and recovery and orbiter recovery. USNORTHCOM, established in 2002 and fully operational Sept. 11, 2003, coordinates U.S. military for the Department of Defense efforts to assist the Space Shuttle astronauts in the event of an emergency. All information on DoD units and NORAD contained in this release is subject to change.
**Launch Facts**
STS-114 will be the 114th Shuttle mission and the 31st flight for Discovery. Launch will occur at Launch Pad 39B - Kennedy Space Center, Fla. The Return to Flight mission will take Shuttle Commander Eileen Collins and six crew members to the International Space Station. The mission is the first of two test flights to evaluate new thermal protection system inspection and repair techniques and to deliver supplies and equipment to the station.
**Launch Window:**NASA announced July 13 to 31 as the launch window for the Space Shuttle Discovery mission.
Launch Slip Opportunities: 24 or 48 hour scrub possible
Landing: Duration of the STS-114 mission is 12 days after launch
**NORAD Launch Support**
Six F-16s from the U.S. Air Force, enforcing FAA established TFR with center point being NASA KSC 39B
**Launch Contingency Support**
USNORTHCOM provides a variety of support throughout launch, on-orbit and landing. In cooperation with NASA and the DoD Manned Space Flight Support Office (DDMS), USNORTHCOM has developed plans to locate and retrieve the astronauts if they have a pad or launch emergency, are forced to bailout of the shuttle, or have to return for landing. Numerous Air Force, Navy, Marine Corps, and Coast Guard aircraft and Navy and Coast Guard ships are pre-positioned or on standby to quickly launch to conduct search and rescue operations. For STS-114, the following DOD and DHS assets are supporting the mission:
20 US Air Force Pararescue personnel (38th RQS, Moody Air Force Base, Ga.; 48th RQS, Davis-Monthan Air Force Base, Ariz.; 58th RQS, Nellis Air Force Base, NV)

1 US Air Force Reserve/US Air National Guard HC-130 (39th RQS (AFRC), Patrick Air Force Base, Fla.; and 1 Air National Guard HC-130 (102nd RQS, F.S. Gabreski Airport N.Y.)
4 US Air Force Reserve HH-60s (301st RQS, Patrick Air Force Base, Fla.)
1 US Marine Corps KC-130 (VMGR 252, Marine Corps Air Station Cherry Point, N.C.)
1 US Navy Surface Combatant (USS Gettysburg (CG 64), Mayport, Fla.) (Capable of commanding and conducing search and rescue with embarked SH-60)
2 US Navy P-3s (Naval Air Station Brunswick, Maine and NAS Jacksonville, Fla.)
2 US Navy E-2 Cs (at Patrick AFB, Fla., based at NAS Norfolk) VAW 121, NAS Norfolk, Va.
1 US Navy Combat Camera (Fleet Combat Camera Atlantic)
The United States Navy’s Fleet Area Control and Surveillance Center at Naval Air Station Jacksonville, Fla., and Naval Meteorology and Oceanography Center and Naval Air Station Norfolk, Va., and the United States Air Force’s Rescue Coordination Center will also be in direct support to Commander, U.S. Northern Command.
**Launch Abort Sites (LAS) and East Coast Launch Abort Landing Sites (ECALS)**
Additionally U.S. military units at the following Shuttle Launch Abort Sites are on alert to support an emergency landing during the launch phase for STS-114. These bases lie near the intended flight path for STS-114:
Atlantic City International Airport, N.J.
Oceana Naval Air Station, Va.
Dover Air Force Base, Del.
Otis Air National Guard Base, Mass.
F. S. Gabreski Airport, N.Y.
Pease Air National Guard Base, N.H.
Marine Corps Air Station Cherry Point, N.C.
**DOD Augmented/Emergency Landing Sites**
If the shuttle experiences an on-orbit emergency and has to land immediately, NASA has established several civilian and military landing sites around the world. US military personnel at the following locations are prepared to support an emergency landing of the shuttle:
</excerpt>
### Rank 5 of 66 — 0.25
<excerpt title="Brian Duffy">
# Brian Duffy
Duffy next commanded STS-92 Discovery, launched on Oct. 11, 2000. During the 13-day International Space Station (ISS) assembly flight, the seven-member crew attached the Z1 Truss and Pressurized Mating Adapter 3 to the ISS using Discovery’s robotic arm and performed four space walks to configure these elements. This expansion of the ISS opened the door for future assembly missions and prepared the station for its first resident crew.
During his time with NASA, Duffy served as spacecraft communicator (CAPCOM) in Mission Control for numerous space shuttle missions. He also served as Assistant Director (Technical) and Deputy Director (Acting) of the Johnson Space Center (JSC). Duffy retired from the Air Force and NASA in 2001. He has served as Vice President and Associate Program Manager for the Lockheed Martin Corporation.
Currently Vice President and JSC Program Manager for Exploration Systems at Orbital ATK, Duffy is interested in making more flights into space.
Choose your language
Open: 9 AM to 5 PM
Kennedy Space Center Visitor Complex
Space Commerce Way, Merritt Island, FL 32953
[1.855.433.4210](tel:1.855.433.4210)
*   Like us on Facebook  
*   Follow us on Instagram  
*   Follow us on X  
*   Subscribe on YouTube
Sign up to our newsletter

# Brian Duffy
*   Park Info  
    *   Hours of Operation  
    *   Directions  
    *   Security  
    *   Accessibility  
    *   Official Apps  
    *   Lost and Found  
    *   Inclement Weather Warnings

*   Visit Us  
    *   Buy Admission Tickets  
    *   Buy Annual Passes  
    *   Enhance Your Visit  
    *   Hotel Packages  
    *   Corporate Events  
    *   Weddings and Social Events  
    *   Itineraries  
    *   

*   Things To Do  
    *   Visitor Complex Map  
    *   Explore Attractions  
    *   Dining  
    *   Shopping  
    *   Education Programs

*   About KSC  
    *   About  
    *   Frequently Asked Questions  
    *   Media Room  
    *   Partners  
    *   NASA.gov  
    *   Greenpath's Environmental Focus  
    *   Careers

*   Contact Us  
    *   Get in Touch

# Brian Duffy
### Park Info
*   Hours of Operation  
*   Directions  
*   Security  
*   Accessibility  
*   Official Apps  
*   Lost and Found  
*   Inclement Weather Warnings

# Brian Duffy
### Visit Us
*   Buy Admission Tickets  
*   Buy Annual Passes  
*   Enhance Your Visit  
*   Hotel Packages  
*   Corporate Events  
*   Weddings and Social Events  
*   Itineraries  
*

# Brian Duffy
### Things To Do
*   Visitor Complex Map  
*   Explore Attractions  
*   Dining  
*   Shopping  
*   Education Programs

# Brian Duffy
### About KSC
*   About  
*   Frequently Asked Questions  
*   Media Room  
*   Partners  
*   NASA.gov  
*   Greenpath's Environmental Focus  
*   Careers
</excerpt>

## Search 6 — query: ""Discovery" "Space Shuttle" commander of STS"
### Rank 1 of 60 — 0.60 (passed on)
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
### Rank 2 of 60 — 0.35
<excerpt title="Space shuttle discovery sts-70 launch july 13 1995">
# July 13th - on this day in 1995,... - NASASpaceflight.com | Facebook
## NASASpaceflight.com's Post
Discovery's five-member crew included Commander Terence Henricks, Pilot Kevin Kregel, and Mission Specialists, [Don Thomas](https://www.facebook.com/drdonthomas?__cft__[0]=AZh1B8dvH-fhxQvntSXFoU5hfPKAiyiXWYyzQKdIdgAgz339CC2QfRy9W7godXH-U1Gy4FJbYytdrUvlQ0ljVkB8ItfDOnSalNI2pT4k3hqnvXrkDmvtSZ8xVtEwFIsnU8yl3w6RXJSRuOZNmbmRElz4M-b84oC9&__tn__=-]K-R), Nancy Currie-Gregg, and Mary Weber.
STS-70 was the final of seven Space Shuttle missions to deploy a Tracking And Data Relay Satellite (TDRS), TDRS-G.
[](https://www.facebook.com/photo/?fbid=1693902172735813&set=a.529406782518697&__cft__[0]=AZh1B8dvH-fhxQvntSXFoU5hfPKAiyiXWYyzQKdIdgAgz339CC2QfRy9W7godXH-U1Gy4FJbYytdrUvlQ0ljVkB8ItfDOnSalNI2pT4k3hqnvXrkDmvtSZ8xVtEwFIsnU8yl3w6RXJSRuOZNmbmRElz4M-b84oC9&__tn__=EH-R)
![Image 2](blob:http://localhost/85d8b181a20aeb64a3afc2f1c39d2480)
![Image 3](blob:http://localhost/2b45e6f1a2ae097354c0b291152873d5)

# July 13th - on this day in 1995,... - NASASpaceflight.com | Facebook
## NASASpaceflight.com's Post
All reactions:
502
20 comments
48 shares
Like
Comment
Most relevant
Christopher Stone
The "Woodpecker" mission. Woodpeckers punched holes in the external tank and had to be delayed while it was repaired. They had a special patch made with Woody Woodpecker on it.
*   [18w](https://www.facebook.com/NASASpaceflight/posts/pfbid0ern4XNAKsGKuKnMhUUUXRd5ddqEp8CY4kB1GfNvS3DqZXXtgU2hHeTF2X6Y3j4iRl?comment_id=27440889642241001&__cft__[0]=AZh1B8dvH-fhxQvntSXFoU5hfPKAiyiXWYyzQKdIdgAgz339CC2QfRy9W7godXH-U1Gy4FJbYytdrUvlQ0ljVkB8ItfDOnSalNI2pT4k3hqnvXrkDmvtSZ8xVtEwFIsnU8yl3w6RXJSRuOZNmbmRElz4M-b84oC9&__tn__=R]-R)
2
![Image 4](blob:http://localhost/520c193f0276d495fb772a9afb8b220d)![Image 5](blob:http://localhost/2b45e6f1a2ae097354c0b291152873d5)
NASASpaceflight.com replied
·
4 Replies
</excerpt>
### Rank 3 of 60 — 0.35
<excerpt title="Space shuttle discovery sts-70 launch july 13 1995">
# July 13th - on this day in 1995,... - NASASpaceflight.com | Facebook
## NASASpaceflight.com's Post
[July 13](https://www.facebook.com/NASASpaceflight/posts/pfbid0ern4XNAKsGKuKnMhUUUXRd5ddqEp8CY4kB1GfNvS3DqZXXtgU2hHeTF2X6Y3j4iRl?__cft__[0]=AZh1B8dvH-fhxQvntSXFoU5hfPKAiyiXWYyzQKdIdgAgz339CC2QfRy9W7godXH-U1Gy4FJbYytdrUvlQ0ljVkB8ItfDOnSalNI2pT4k3hqnvXrkDmvtSZ8xVtEwFIsnU8yl3w6RXJSRuOZNmbmRElz4M-b84oC9&__tn__=%2CO%2CP-R) ·
July 13th - on this day in 1995, Discovery launched for the STS-70 mission, lifting off from Launch Complex 39B at [NASA's Kennedy Space Center](https://www.facebook.com/NASAKennedy?__cft__[0]=AZh1B8dvH-fhxQvntSXFoU5hfPKAiyiXWYyzQKdIdgAgz339CC2QfRy9W7godXH-U1Gy4FJbYytdrUvlQ0ljVkB8ItfDOnSalNI2pT4k3hqnvXrkDmvtSZ8xVtEwFIsnU8yl3w6RXJSRuOZNmbmRElz4M-b84oC9&__tn__=-]K-R). The launch occurred only six days after Atlantis had concluded STS-71, making this the fastest turnaround between flights in the history of the Space Shuttle program.

# July 13th - on this day in 1995,... - NASASpaceflight.com | Facebook
## NASASpaceflight.com's Post
Discovery's five-member crew included Commander Terence Henricks, Pilot Kevin Kregel, and Mission Specialists, [Don Thomas](https://www.facebook.com/drdonthomas?__cft__[0]=AZh1B8dvH-fhxQvntSXFoU5hfPKAiyiXWYyzQKdIdgAgz339CC2QfRy9W7godXH-U1Gy4FJbYytdrUvlQ0ljVkB8ItfDOnSalNI2pT4k3hqnvXrkDmvtSZ8xVtEwFIsnU8yl3w6RXJSRuOZNmbmRElz4M-b84oC9&__tn__=-]K-R), Nancy Currie-Gregg, and Mary Weber.
STS-70 was the final of seven Space Shuttle missions to deploy a Tracking And Data Relay Satellite (TDRS), TDRS-G.
[](https://www.facebook.com/photo/?fbid=1693902172735813&set=a.529406782518697&__cft__[0]=AZh1B8dvH-fhxQvntSXFoU5hfPKAiyiXWYyzQKdIdgAgz339CC2QfRy9W7godXH-U1Gy4FJbYytdrUvlQ0ljVkB8ItfDOnSalNI2pT4k3hqnvXrkDmvtSZ8xVtEwFIsnU8yl3w6RXJSRuOZNmbmRElz4M-b84oC9&__tn__=EH-R)
![Image 2](blob:http://localhost/85d8b181a20aeb64a3afc2f1c39d2480)
![Image 3](blob:http://localhost/2b45e6f1a2ae097354c0b291152873d5)
</excerpt>
### Rank 4 of 60 — 0.29
<excerpt title="Discovery: Champion of the Space Shuttle Fleet">
Discovery astronaut servicing the Hubble Space Telescope (1997-02-21) by NASA**Smithsonian's National Air and Space Museum**
Discovery returned in both 1997 and 1999 to service Hubble.
_Image: The installation of new instruments in 1997 extended Hubble's wavelength range into the near infrared for imaging and spectroscopy, allowing us to probe the most distant reaches of the universe._
[](https://artsandculture.google.com/asset/button-space-manufacturer-mcdonnell-douglas/6AGVjBPl6vqOww "Button, \"SPACE MANufacturer\", McDonnell Douglas Button, \"SPACE MANufacturer\", McDonnell Douglas")
Show less Read more
Charles Walker, a McDonnell Douglas engineer, became the first non-astronaut to fly on a shuttle when he joined the Discovery crew as a payload specialist on its first flight.
Show less Read more
A few dignitaries flew shuttle missions. The crew of STS-51D included Senator Jake Garn, seen on the far left.
_Image: From left to right are Jake Garn, Jeff Hoffman, Don Williams, Rhea Seddon, Karol “Bo” Bobko, Dave Griggs, and Charlie Walker._
Show less Read more
In 1998, then U.S. Senator John H. Glenn, Jr., the first American to orbit the Earth, became the oldest person to go into space at age 77.
_Image: STS-95 Payload Specialist John Glenn positions himself to take photos from Discovery's aft flight deck windows._
Return to Flight Launch of Discovery by NASA**Smithsonian's National Air and Space Museum**
After both the Challenger and Columbia tragedies, Discovery served as the Shuttle Program's Return-to-Flight vehicle in 1988 and 2005.
_Image: Return-to-Flight launch of the Space Shuttle Discovery on September 29, 1988._
Show less Read more
The first African American Shuttle Commander, Frederick Gregory, commanded Discovery during STS-33 in 1989.

_Image: The astronauts of STS-33. Photographed from left to right are Kathryn C. Thornton, mission specialist 3; Manley L. (Sonny) Carter, mission specialist 2; Frederick D. Gregory, commander; John E. Blaha, pilot; and F. Story Musgrave, mission specialist 1._
Show less Read more
On April 8, 1993, astronaut Ellen Ochoa became the first Hispanic woman in space as a crewmember on the STS-56 Discovery. She flew aboard the shuttle four times, and spent over 1,000 hours in space.
_Image: Astronaut Ellen Ochoa, STS-96 mission specialist, in the SpaceHab module aboard the Earth-orbiting Space Shuttle Discovery, 1999._
Show less Read more
In 1995, Dr. Bernard A. Harris, Jr. suited up and stepped out of Discovery to become the first African American to walk in space.
_Image: STS-63 astronauts Bernard A. Harris, Jr., payload commander (right), and C. Michael Foale, mission specialist (left), are ready to exit Discovery's airlock for a spacewalk._
Show less Read more
Discovery was piloted by the first female spacecraft pilot, Eileen Collins, in 1995.
_Image: Annie Leibovitz took this photo of Eileen Collins at NASA's Johnson Space Center in Houston, Texas, during training._
International Space Station seen from Space Shuttle Discovery (1999-06-03) by NASA**Smithsonian's National Air and Space Museum**
Discovery made the first ever docking with the International Space Station in 1999.
_Image: A STS-96 crew member aboard Discovery took this image of the International Space Station._
Space Shuttle Discovery by NASA**Smithsonian's National Air and Space Museum**
Discovery flew the 100th overall shuttle mission in 2000, one of a number of flights involved in the construction of the International Space Station.
_Image: Space Shuttle Discovery stands ready for launch of mission STS-92, the fifth flight for construction of the International Space Station._
</excerpt>
### Rank 5 of 60 — 0.29
<excerpt title="Discovery: Champion of the Space Shuttle Fleet">
Flying more missions than any other shuttle, Discovery carried out every type of mission NASA had to offer, spending a total of 365 days in space, and checking off many firsts in spaceflight.
Space Shuttle Discovery**Smithsonian's National Air and Space Museum**
Discovery has earned a place of honor in the collection of national treasures preserved by the Smithsonian's National Air and Space Museum.
Space Shuttle STS-41D Launch (1984) by NASA**Smithsonian's National Air and Space Museum**
The longest-serving orbiter, Discovery flew 39 times from 1984 through 2011 — more missions than any of its sister ships — spending altogether 365 days in space.
_Image: Discovery's maiden launch in 1984 from the Kennedy Space Center._
Discovery Launches on Final Flight STS-133 by NASA**Smithsonian's National Air and Space Museum**
Discovery also flew every type of mission during the space shuttle era and has a record of distinctions, representing the full scope of human spaceflight from 1981-2011.
_Image: Discovery's final liftoff (STS-133) in 2011, delivering new sections of the International Space Station._
Mir Cosmonaut views Discovery by NASA**Smithsonian's National Air and Space Museum**
Discovery made the first shuttle visit to the Russian Mir space station (a rendezvous without docking) in February of 1995.
_Image: A Mir Cosmonaut views Discovery on February 6, 1995._
Space Shuttle Discovery (1998-06-03) by NASA**Smithsonian's National Air and Space Museum**
Discovery also made the final docking visit to Mir on June 3, 1998.
_Image: The Space Shuttle Discovery approaches Russia's Mir space station in this photograph taken from the Mir._
Deployment of Hubble Space Telescope by NASA**Smithsonian's National Air and Space Museum**
Discovery deployed the extraordinary Hubble Space Telescope in 1990. Hubble is the only telescope designed to be serviced in space.
_Image: Hubble Space Telescope being deployed on April 25, 1990, from the payload bay of Space Shuttle Discovery (STS-31)._

Discovery astronaut servicing the Hubble Space Telescope (1997-02-21) by NASA**Smithsonian's National Air and Space Museum**
Discovery returned in both 1997 and 1999 to service Hubble.
_Image: The installation of new instruments in 1997 extended Hubble's wavelength range into the near infrared for imaging and spectroscopy, allowing us to probe the most distant reaches of the universe._
[](https://artsandculture.google.com/asset/button-space-manufacturer-mcdonnell-douglas/6AGVjBPl6vqOww "Button, \"SPACE MANufacturer\", McDonnell Douglas Button, \"SPACE MANufacturer\", McDonnell Douglas")
Show less Read more
Charles Walker, a McDonnell Douglas engineer, became the first non-astronaut to fly on a shuttle when he joined the Discovery crew as a payload specialist on its first flight.
Show less Read more
A few dignitaries flew shuttle missions. The crew of STS-51D included Senator Jake Garn, seen on the far left.
_Image: From left to right are Jake Garn, Jeff Hoffman, Don Williams, Rhea Seddon, Karol “Bo” Bobko, Dave Griggs, and Charlie Walker._
Show less Read more
In 1998, then U.S. Senator John H. Glenn, Jr., the first American to orbit the Earth, became the oldest person to go into space at age 77.
_Image: STS-95 Payload Specialist John Glenn positions himself to take photos from Discovery's aft flight deck windows._
Return to Flight Launch of Discovery by NASA**Smithsonian's National Air and Space Museum**
After both the Challenger and Columbia tragedies, Discovery served as the Shuttle Program's Return-to-Flight vehicle in 1988 and 2005.
_Image: Return-to-Flight launch of the Space Shuttle Discovery on September 29, 1988._
Show less Read more
The first African American Shuttle Commander, Frederick Gregory, commanded Discovery during STS-33 in 1989.
</excerpt>

## Search 7 — query: "Discovery 39 flights orbiter"
### Rank 1 of 83 — 0.60 (passed on)
<excerpt title="Space Shuttle Discovery">
| _Discovery_ |  
| --- |  
|  _Discovery_ in orbit in 2011, during STS-133, the orbiter's final flight |  
| Type | Spaceplane |  
| Class | Space Shuttle orbiter |  
| Eponym | * _Discovery_ (1602) * HMS _Discovery_(1774) |  
| Serial no. | OV-103 |  
| Owner | NASA |  
| Manufacturer | Rockwell International |  
| Specifications |  
| Dry mass | 78,000 kilograms (172,000 lb) |  
| Rocket | Space Shuttle |  
| History |  
| First flight | * August 30 – September 5, 1984 * STS-41-D |  
| Last flight | * February 24 – March 9, 2011 * STS-133 |  
| Flights | 39 |  
| Flight time | 8,783 hours |  
| Travelled | 238,539,663 kilometres (148,221,675 mi) around Earth[[1]](https://en.wikipedia.org/wiki/Space_Shuttle_Discovery#cite_note-NASAfacts-1) |  
| Orbits | 5,830 around Earth |  
| Fate | Retired |  
| Location | * Steven F. Udvar-Hazy Center * Chantilly, Virginia |  
| Space Shuttle orbiters |  
| ←_Challenger_ _Atlantis_→ |
Space Shuttle _Discovery_ at the Steven F. Udvar-Hazy Center
_Discovery_ rollout ceremony in October 1983
Discovery and SCA 905 at Vandenberg Air Force Base, November 6, 1983

**Space Shuttle _Discovery_** (Orbiter Vehicle Designation: **OV-103**) is a retired American Space Shuttle orbiter. The spaceplane was one of the orbiters from NASA's Space Shuttle program and the third of five fully operational orbiters to be built.[[2]](https://en.wikipedia.org/wiki/Space_Shuttle_Discovery#cite_note-ov103-2) Its first mission, STS-41-D, flew from August 30 to September 5, 1984. Over 27 years of service it launched and landed 39 times, aggregating more spaceflights than any other spacecraft as of December 2024.[[3]](https://en.wikipedia.org/wiki/Space_Shuttle_Discovery#cite_note-Guinness_most_spaceflights-3) The Space Shuttle launch vehicle had three main components: the Space Shuttle orbiter, a single-use central fuel tank, and two reusable solid rocket boosters. Nearly 25,000 heat-resistant tiles cover the orbiter to protect it from high temperatures on re-entry.[[4]](https://en.wikipedia.org/wiki/Space_Shuttle_Discovery#cite_note-4)
_Discovery_ became the third operational orbiter to enter service, preceded by _Columbia_ and _Challenger_.[[5]](https://en.wikipedia.org/wiki/Space_Shuttle_Discovery#cite_note-5) After the _Challenger_ and _Columbia_ accidents, _Discovery_ became the oldest surviving orbiter. It embarked on its final mission, STS-133, on February 24, 2011, and touched down for the last time at Kennedy Space Center on March 9,[[6]](https://en.wikipedia.org/wiki/Space_Shuttle_Discovery#cite_note-6) having spent a cumulative total of nearly a full year in space. _Discovery_ performed both research and International Space Station (ISS) assembly missions, and also carried the Hubble Space Telescope into orbit among other satellites.
_Discovery_ was the first operational shuttle to be retired, followed by _Endeavour_ and then _Atlantis_. The shuttle is now on display at the Steven F. Udvar-Hazy Center of the SmithsonianNational Air and Space Museum.
</excerpt>
### Rank 2 of 83 — 0.59
<excerpt title="Space Shuttle Discovery (OV-103)">
The global defense reference actively compiled since 2003
MENU

## Reusable Space Shuttle Orbiter
### United States | 1984
#### "Space Shuttle Discovery became the third American shuttle to enter service, joining the Columbia and the Challenger - both later lost in accidents."
Authored By: Staff Writer | Last Edited: 05/21/2018 | Content ©www.MilitaryFactory.com | The following text is exclusive to this site; No A.I. was used in the generation of this content.
Six reusable space shuttle orbiters were built for the United States space program by Rockwell International - these becoming Atlantis, Challenger, Colombia, Discovery, Enterprise and Endeavor. Two were lost during missions (Colombia and Challenger) while four served their terms and retired as museum showpieces. Discovery, given the Orbiter Vehicle Designation of "OV-103", was born through a contract awarded on January 29th, 1979 and recorded its first mission on August 30th, 1984. Its final mission occurred on February 24th, 2011.  
A total of 39 missions were flown by Discovery and involved some 252 crewmen covering just over one year of time in space (365 days, 22 hours). Her retired frame is on exhibit at the Steven F. Udvar-Hazy Center in Chantilly, Virginia (2016).
Discovery was of a slightly modified, lighter design compared to Columbia by the time it entered formal service, benefitting from testing completed on the frames of Columbia, Challenger and Enterprise prior. In 1983 she was to receive the liquid-fueled "Centaur-G" booster system but the Challenger incident derailed this installation. In 1995, she underwent a major refit to keep her a viable spacecraft for the near future.

## Reusable Space Shuttle Orbiter
### United States | 1984
#### "Space Shuttle Discovery became the third American shuttle to enter service, joining the Columbia and the Challenger - both later lost in accidents."
During her time aloft, Discovery managed several notable achievements for itself, her crews and the United States space program. STS-41-D marked the second American woman in space, Judith Resnick (she would tragically perish in the Challenger disaster later). STS-31 saw the launching of the Hubble Space Telescope and STS-63 marked the first time the shuttle would be piloted by a female. STS-95 marked the return of astronaut John Glenn into space, then aged 77, making him the oldest man to accomplish the feat. STS-96 saw Discovery become the first shuttle to dock with the International Space Station (thirteen total docking actions were eventually recorded) and STS-92 became the 100th mission completed by the space shuttle program. STS-133 went down in history as Discovery's final mission.
On several occasions, and during warmer ties with the Russians, Discovery also docked with the Soviet-Russian space station "Mir".
STS-26 and STS-114 became notable missions in their own right for it was Discovery that put the American space program back on track following the mission disasters of Challenger and Columbia.
The end of Discovery's career finally arrived on March 9th, 2011 when she was formally decommissioned from active service in the NASA orbiter fleet. The enter fleet has since been retired from active service.
Content ©MilitaryFactory.com; No Reproduction Permitted.
Global customers who have evaluated and/or operated the Space Shuttle Discovery (OV-103). Nations are displayed by flag, each linked to their respective national aircraft listing.   
Total Production: 1 Units
Contractor(s): Boeing Company / Rockwell International - USA
[ United States (retired) ]
Propulsion
3 x Rocketdyne Block II SSMEs developing 393,800lbs of thrust (1,181,400lbs at launch); 2 x Orbital Maneuvering Engines developing 12,000lbs of thrust.
Maximum Speed
17,318 mph
</excerpt>
### Rank 3 of 83 — 0.53
<excerpt title="Space Shuttle Discovery">
## Features and upgrades
Texas senators John Cornyn and Ted Cruz added a provision to the 2025 One Big Beautiful Bill Act to spend $85 million to relocate a space vehicle that has flown astronauts into space, presumably _Discovery_ because of the sponsors of the provision and previous legislation attempts, from the Udvar-Hazy Center to the Space Center Houston Museum in Texas.[[30]](https://en.wikipedia.org/wiki/Space_Shuttle_Discovery#cite_note-30)[[31]](https://en.wikipedia.org/wiki/Space_Shuttle_Discovery#cite_note-31) While the Smithsonian estimated that the total cost of the transfer would be approximately $325 million, they also countered that ownership of the shuttle had been transferred to the museum and was no longer federal property, and that Congress did not have the ability to force a transfer.[[32]](https://en.wikipedia.org/wiki/Space_Shuttle_Discovery#cite_note-32)[[33]](https://en.wikipedia.org/wiki/Space_Shuttle_Discovery#cite_note-33)

## Features and upgrades
By its last mission, _Discovery_ had flown 149 million mi (240 million km) in 39 missions, completed 5,830 orbits, and spent 365 days in orbit over 27 years.[[34]](https://en.wikipedia.org/wiki/Space_Shuttle_Discovery#cite_note-slt-34)_Discovery_ flew more flights than any other Orbiter Shuttle, including four in 1985 alone. _Discovery_ flew both "return to flight" missions after the _Challenger_ and _Columbia_ disasters: STS-26 in 1988, STS-114 in 2005, and STS-121 in 2006. _Discovery_ flew the ante-penultimate mission of the Space Shuttle program, STS-133, having launched on February 24, 2011. _Endeavour_ flew STS-134 and _Atlantis_ performed STS-135, NASA's last Space Shuttle mission. On February 24, 2011, Space Shuttle _Discovery_ launched from Kennedy Space Center's Launch Complex 39-A to begin its final orbital flight.[[35]](https://en.wikipedia.org/wiki/Space_Shuttle_Discovery#cite_note-ares6-35)
‡ Longest shuttle mission for _Discovery_
– shortest shuttle mission for _Discovery_
</excerpt>
### Rank 4 of 83 — 0.52
<excerpt title="Space Shuttle Discovery">
**Space Shuttle _Discovery_** (Orbiter Vehicle Designation: **OV-103**) is a retired American Space Shuttle orbiter. The spaceplane was one of the orbiters from NASA's Space Shuttle program and the third of five fully operational orbiters to be built.[[2]](https://en.wikipedia.org/wiki/Space_Shuttle_Discovery#cite_note-ov103-2) Its first mission, STS-41-D, flew from August 30 to September 5, 1984. Over 27 years of service it launched and landed 39 times, aggregating more spaceflights than any other spacecraft as of December 2024.[[3]](https://en.wikipedia.org/wiki/Space_Shuttle_Discovery#cite_note-Guinness_most_spaceflights-3) The Space Shuttle launch vehicle had three main components: the Space Shuttle orbiter, a single-use central fuel tank, and two reusable solid rocket boosters. Nearly 25,000 heat-resistant tiles cover the orbiter to protect it from high temperatures on re-entry.[[4]](https://en.wikipedia.org/wiki/Space_Shuttle_Discovery#cite_note-4)
_Discovery_ became the third operational orbiter to enter service, preceded by _Columbia_ and _Challenger_.[[5]](https://en.wikipedia.org/wiki/Space_Shuttle_Discovery#cite_note-5) After the _Challenger_ and _Columbia_ accidents, _Discovery_ became the oldest surviving orbiter. It embarked on its final mission, STS-133, on February 24, 2011, and touched down for the last time at Kennedy Space Center on March 9,[[6]](https://en.wikipedia.org/wiki/Space_Shuttle_Discovery#cite_note-6) having spent a cumulative total of nearly a full year in space. _Discovery_ performed both research and International Space Station (ISS) assembly missions, and also carried the Hubble Space Telescope into orbit among other satellites.
_Discovery_ was the first operational shuttle to be retired, followed by _Endeavour_ and then _Atlantis_. The shuttle is now on display at the Steven F. Udvar-Hazy Center of the SmithsonianNational Air and Space Museum.

The name _Discovery_ was chosen to carry on a tradition based on ships of exploration,[[2]](https://en.wikipedia.org/wiki/Space_Shuttle_Discovery#cite_note-ov103-2) primarily HMS _Discovery_,[[7]](https://en.wikipedia.org/wiki/Space_Shuttle_Discovery#cite_note-7) one of the ships commanded by Captain James Cook during his third and final major voyage from 1776 to 1779, and Henry Hudson's _Discovery_,[[2]](https://en.wikipedia.org/wiki/Space_Shuttle_Discovery#cite_note-ov103-2) which was used in 1610–1611 to explore Hudson Bay and search for a Northwest Passage. Other ships bearing the name have included HMS _Discovery_[[8]](https://en.wikipedia.org/wiki/Space_Shuttle_Discovery#cite_note-8) of the 1875–1876 British Arctic Expedition to the North Pole, and RRS _Discovery_, which carried the 1901–1904 _Discovery_ Expedition to Antarctica, led by Captain Scott.[[9]](https://en.wikipedia.org/wiki/Space_Shuttle_Discovery#cite_note-pao-9)
Space Shuttle _Discovery_ launched the Hubble Space Telescope and conducted the second and third Hubble service missions. It also launched the _Ulysses_ probe and three TDRS satellites. Twice _Discovery_ was chosen as the "Return To Flight" Orbiter, first in 1988 after the loss of _Challenger_ in 1986, and then again for the twin "Return To Flight" missions in July 2005 and July 2006 after the _Columbia_ disaster in 2003. Project Mercury astronaut John Glenn, who was 77 at the time, flew with _Discovery_ on STS-95 in 1998, making him the oldest person to go into space at that time in history.[[10]](https://en.wikipedia.org/wiki/Space_Shuttle_Discovery#cite_note-over-10)
</excerpt>
### Rank 5 of 83 — 0.48
<excerpt title="Forty Years of Discovery">
No, _Discovery_ doesn’t make sandwiches or have a way to cook bacon. But it does have a very special thermal tile that has the name BLT (Boundary Layer Transition). Towards the end of the Space Shuttle program, engineers, mostly from the NASA Langley Research Center, wanted to see what changes might occur during reentry by intentionally disrupting the flow of plasma on the underside of the orbiter’s wings. Engineers needed to test this on repeated missions, and _Discovery_ became the primary vehicle for tests over four missions, though _Atlantis_ and _Endeavour_ also flew missions with a BLT tile (which you can still see on the underside of their port wings). Information from embedded sensors and telemetry data gathered from a jet aircraft flying next to the orbiter during landing would indicate how changing the flow of plasma altered the vehicle’s stability. Changing the size of this raised bump, as well as vehicle speed and altitude, from one mission to the next gave engineers information to augment data gathered during the loss of _Columbia_ in 2003. In that case, plasma flow was drastically disrupted by a hole on the port wing leading edge, causing the vehicle to spin out of control and break apart. The BLT tests provided information for future missions on the effect of surface disruptions during reentry, making it possible to determine a safe course of action if damage was found on the thermal protection system.
The small finger-sized bump is embedded in a tile with built-in sensors on the underside of _Discovery_’s port wing.
**Velcro**
Since visitors can’t climb around inside _Discovery_, be assured that nearly every working surface in the crew compartment has plenty of VELCRO® to secure small items. Most of that material is blue, and the International Space Station features mostly white squares, though some blue can be found. What I learned from occasional trips inside the orbiter with engineers is that there is also yellow VELCRO® in a few spots. I happened to notice one piece above the window directly in front of the pilot’s seat when we were last on the flight deck in early 2022. These infrequent yellow squares are not standard positions, but in crew preferred locations, making the ones in _Discovery_ reminders of the final crew to fly in 2011. Each crewmember on each mission would have different spots they might find the material useful, so each orbiter would have yellow squares in different locations.

A piece of yellow VELCRO® remains above a window, placed there at the request of _Discovery_’s last pilot, Eric Boe.
**Nicknames**
Each orbiter has its own name, like sailing vessels throughout history. _Enterprise_ had been used on an aircraft carrier but was notably selected for its connection to the trailblazing space adventures by the spacecraft of the same name on the television show _Star Trek_. _Columbia_, _Challenger_, _Discovery_, _Atlantis_, and _Endeavour_ had all been names used on sailing vessels from the 17th through early 20th centuries. But beyond just formal names like those, like our own personal names, sometimes a nickname is fun to have either as a shortened version of the full name or something related to a thing’s style or character (as a Jennifer, I get referred to as Jen or Jenny, depending on the speaker). Crewmembers who were military pilots often came with call signs when they became astronauts or acquired them while working at NASA (for example, George Nelson is “Pinky,” Kenneth Cockrell is “Taco,” and Pam Melroy is “Pambo”). When _Discovery_ arrived at Dulles Airport in 2012, I learned it also had its own nickname, which was more obvious than I expected: Disco! I can’t imagine that derived from the vehicle’s behavior, but it certainly makes flying on it sound really fun.
**History**
Not to brag, but _Discovery_ _does_ have the greatest flight history record. We often repeat the same information on tours and in printed materials: 39 missions, 365 total days spent in space. That’s quite a feat for the journeys the orbiter took. But it’s really a testament to the team that made each of those flights possible. Tens of thousands of people were involved in maintaining the vehicle, training the astronauts, preparing the science experiments, building the satellites or telescopes, and managing activities on the ground making sure everything went smoothly. Not enough can be said about their commitment to safety and mission success. And _Discovery_ had many an important mission for which that hard work was tested. For the purposes of this remembrance, let’s look a little at that very first mission, STS-41D.
</excerpt>

## Search 8 — query: "Discovery mission list commander site:wikipedia.org"
### Rank 1 of 244 — 0.56 (passed on)
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
### Rank 2 of 244 — 0.55
<excerpt title="List of Space Shuttle crews">
# List of Space Shuttle crews
## 1996–2000
| 86 | August 7 | 1997 | STS-85 | _Discovery_ | 11 d 20 h | C. Brown | Rominger | Davis | Robinson | Curbeam |  |  | Tryggvason  |  |  
| 87 | September 25 | 1997 | STS-86 | _Atlantis_ | 10 d 19 h | Wetherbee | Bloomfield | Titov  | Parazynski | Chrétien  | Lawrence | Wolf**Mir** | _Foale_ |  |  
| 88 | November 19 | 1997 | STS-87 | _Columbia_ | 15 d 16 h | Kregel | Lindsey | Scott | Chawla | Doi  |  |  | Kadenyuk  |  |  
| 89 | January 22 | 1998 | STS-89 | _Endeavour_ | 8 d 19 h | Wilcutt | [Edwards](https://en.wikipedia.org/wiki/Joe_F._Edwards_Jr. "Joe F. Edwards Jr.") | Dunbar**PC** | M.Anderson | Reilly | Sharipov  | A.Thomas**Mir** | _Wolf_ |  |  
| 90 | April 17 | 1998 | STS-90 | _Columbia_ | 15 d 21 h | Searfoss | Altman | Linnehan | D. Williams  | Hire |  |  | Buckey | Pawelczyk |  
| 91 | June 2 | 1998 | STS-91 | _Discovery_ | 9 d 19 h | Precourt | Gorie | Lawrence | Chang-Diaz | Kavandi | Ryumin  |  | _A. Thomas_ |  |  
| 92 | October 29 | 1998 | STS-95 | _Discovery_ | 8 d 21 h | C. Brown | Lindsey | Robinson**PC** | Parazynski | Duque  |  |  | Mukai  | Glenn |
</excerpt>
### Rank 3 of 244 — 0.49
<excerpt title="List of Space Shuttle crews">
# List of Space Shuttle crews
## 1986–1990
| 31 | October 18 | 1989 | STS-34 | _Atlantis_ | 4 d 23 h | D. E. Williams | McCulley | Chang-Diaz | Lucid | E. Baker |  |  |  
| 32 | November 22 | 1989 | STS-33 | _Discovery_ | 5 d 0 h | Gregory | Blaha | Musgrave | Carter | K.Thornton |  |  |  
| 33 | January 9 | 1990 | STS-32 | _Columbia_ | 10 d 21 h | Brandenstein | Wetherbee | Dunbar | Low | Ivins |  |  |  
| 34 | February 28 | 1990 | STS-36 | _Atlantis_ | 4 d 10 h | Creighton | Casper | Mullane | Hilmers | Thuot |  |  |  
| 35 | April 24 | 1990 | STS-31 | _Discovery_ | 5 d 1 h | Shriver | [Bolden](https://en.wikipedia.org/wiki/Charles_F._Bolden_Jr. "Charles F. Bolden Jr.") | Hawley | McCandless | Sullivan |  |  |  
| 36 | October 6 | 1990 | STS-41 | _Discovery_ | 4 d 2 h | R. Richards | Cabana | Shepherd | Melnick | Akers |  |  |  
| 37 | November 15 | 1990 | STS-38 | _Atlantis_ | 4 d 21 h | Covey | [Culbertson](https://en.wikipedia.org/wiki/Frank_L._Culbertson_Jr. "Frank L. Culbertson Jr.") | Springer | Meade | Gemar |  |  |  
| 38 | December 2 | 1990 | STS-35 | _Columbia_ | 8 d 23 h | Brand | G.Gardner | Hoffman | Lounge | Parker | Durrance | Parise |
</excerpt>
### Rank 4 of 244 — 0.46
<excerpt title="List of Space Shuttle crews">
# List of Space Shuttle crews
## 1991–1995
| 52 | December 2 | 1992 | STS-53 | _Discovery_ | 7 d 7 h | D. Walker | Cabana | Bluford | J. S. Voss | Clifford |  |  |  |  |  |  
| 53 | January 13 | 1993 | STS-54 | _Endeavour_ | 5 d 23 h | Casper | McMonagle | [Runco](https://en.wikipedia.org/wiki/Mario_Runco_Jr. "Mario Runco Jr.") | Harbaugh | Helms |  |  |  |  |  |  
| 54 | April 8 | 1993 | STS-56 | _Discovery_ | 9 d 6 h | Cameron | Oswald | Foale | Cockrell | Ochoa |  |  |  |  |  |  
| 55 | April 26 | 1993 | STS-55 | _Columbia_ | 9 d 23 h | Nagel | Henricks | Ross | Precourt | [Harris](https://en.wikipedia.org/wiki/Bernard_A._Harris_Jr. "Bernard A. Harris Jr.") |  |  | Walter  | Schlegel  |  |  
| 56 | June 21 | 1993 | STS-57 | _Endeavour_ | 9 d 23 h | Grabe | Duffy | Low**PC** | Sherlock | Wisoff | J. E. Voss |  |  |  |  |  
| 57 | September 12 | 1993 | STS-51 | _Discovery_ | 9 d 20 h | [Culbertson](https://en.wikipedia.org/wiki/Frank_L._Culbertson_Jr. "Frank L. Culbertson Jr.") | Readdy | Newman | Bursch | Walz |  |  |  |  |  |
</excerpt>
### Rank 5 of 244 — 0.44
<excerpt title="List of Space Shuttle crews">
# List of Space Shuttle crews
## 2001–2005
[edit]
| Order | Day | Year | Mission | Shuttle | Duration | Commander | Pilot | Mission specialists | Payload specialists |  
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |  
| 102 | February 7 | 2001 | STS-98 | _Atlantis_ | 12 d 21 h | Cockrell | Polansky | Curbeam | Jones | Ivins |  |  |  |  |  |  
| 103 | March 8 | 2001 | STS-102 | _Discovery_ | 12 d 19 h | Wetherbee | J. Kelly | A.Thomas | P.Richards | Usachev**ISS**  | J. S. Voss**ISS** | Helms**ISS** | _Shepherd_ | _Gidzenko_  | _Krikalev_  |  
| 104 | April 19 | 2001 | STS-100 | _Endeavour_ | 11 d 21 h | Rominger | Ashby | Hadfield  | Parazynski | Phillips | Guidoni  | Lonchakov  |  |  |  |  
| 105 | July 12 | 2001 | STS-104 | _Atlantis_ | 12 d 18 h | Lindsey | Hobaugh | Gernhardt | Reilly | Kavandi |  |  |  |  |  |  
| 106 | August 10 | 2001 | STS-105 | _Discovery_ | 11 d 21 h | Horowitz | Sturckow | Barry | Forrester | [Culbertson](https://en.wikipedia.org/wiki/Frank_L._Culbertson_Jr. "Frank L. Culbertson Jr.")**ISS** | Tyurin**ISS**  | Dezhurov**ISS**  | _Usachev_  | _J. S. Voss_ | _Helms_ |
</excerpt>

## Search 9 — query: "Discovery STS commander table"
### Rank 1 of 62 — 0.20 (passed on)
<excerpt title="STS-26">
### Crew seat assignments
[edit]
| Seat[[2]](https://en.wikipedia.org/wiki/STS-26#cite_note-2) | Launch | Landing |  Seats 1–4 are on the flight deck. Seats 5–7 are on the mid-deck. |  
| --- | --- | --- |  
| 1 | Hauck |  
| 2 | Covey |  
| 3 | Lounge |  
| 4 | Hilmers |  
| 5 | Nelson |  
| 6 | _Unused_ |  
| 7 | _Unused_ |
_Discovery_ lifts off from KSC, the first shuttle mission after the _Challenger_ disaster
Space Shuttle _Discovery_ lifted off from Launch Complex 39B, Kennedy Space Center, at 11:37:00 a.m. EDT on September 29, 1988, 975 days after the _Challenger_ disaster.
The launch was delayed by one hour and thirty-eight minutes due to unseasonable and unusual light winds, and the need to replace fuses in the cooling systems of two crew members' flight suits. The suits were repaired, and a waiver was issued for the wind conditions after officials determined there was a sufficient safety margin for wind loads on the orbiter's wing leading edges. At T−1:30, it was proposed that the launch be delayed at T−0:31 due to a cabin air pressure issue. It was quickly determined that the cabin pressure had been increased slightly by the activation of the oxygen systems in the crew's flight suits, and the launch was conducted without further delay. The shuttle crew—all veteran astronauts—included Commander Frederick H. "Rick" Hauck, Pilot Richard O. Covey, and Mission Specialists John M. "Mike" Lounge, George D. "Pinky" Nelson and David C. Hilmers.
The primary payload for the STS-26 mission, TDRS-C, was successfully deployed, and 11 scheduled mid-deck scientific and technological experiments were carried out. The post-_Challenger_ redesigned solid rocket booster segment joints showed no signs of leakage or overheating.[[a]](https://en.wikipedia.org/wiki/STS-26#cite_note-3)
</excerpt>
### Rank 2 of 62 — 0.15
<excerpt title="STS-26">
*   Automated Directional Solidification Furnace (ADSF)  
*   Aggregation of Red Blood Cells (ARC)  
*   Earth-Limb Radiance Experiment (ELRAD)  
*   Isoelectric Focusing Experiment (IFE)  
*   Infrared Communications Flight Experiment (IRCFE)  
*   Mesoscale Lightning Experiment (MLE)  
*   Orbiter Experiments Autonomous Supporting Instrumentation System (OASIS)  
*   Phase Partitioning Experiment (PPE)  
*   Physical Vapor Transport of Organic Solids (PVTOS-2)  
*   Protein Crystal Growth (PCG)  
*   Two Shuttle Student Involvement Program (SSIP)  
*   Voice Control Unit (VCU)
STS-26 mission patch
Back row: Lounge, Hilmers and Nelson
Front row: Covey and Hauck
Space Shuttle program
←STS-51-L (25)
STS-27→
**STS-26** was the 26th NASASpace Shuttle mission and the seventh flight of the orbiter _Discovery_. The mission launched from Kennedy Space Center, Florida, on September 29, 1988, and landed four days later on October 3, 1988. STS-26 was declared the "Return to Flight" mission, being the first mission after the Space Shuttle _Challenger_ disaster of January 28, 1986. It was the first mission since STS-9 to use the original Space Transportation System (STS) numbering system, the first to have all its crew members wear pressure suits for launch and landing since STS-4, and the first mission with bailout capacity since STS-4. STS-26 was also the first U.S. space mission with an all-veteran crew since Apollo 11, with all of its crew members having flown at least one prior mission.
The mission is technically designated **STS-26R**, as the original STS-26 designation previously belonged to STS-51-F (also known as Spacelab-2). Likewise all flights with the STS-26 through STS-33 designations would require the **R** in their documentation to avoid conflicts in tracking data between the old and new flight designations.[[1]](https://en.wikipedia.org/wiki/STS-26#cite_note-Jenkins-1)

The crew roster for STS-26 was based on the original crew assignment for STS-61-F, which would have launched the _Ulysses_ probe from _Challenger_ in 1986. _Ulysses_ was eventually launched on STS-41. Hauck, Lounge and Hilmers were all assigned to that flight, with [Roy D. Bridges Jr.](https://en.wikipedia.org/wiki/Roy_D._Bridges_Jr. "Roy D. Bridges Jr.") as pilot. Bridges never flew again after the _Challenger_ disaster, but would eventually become the director of Langley Research Center (LRC).
Covey was the CAPCOM operator during the STS-51-L launch who uttered the words, "_Challenger_, go at throttle up" to commander Francis R. Scobee, shortly after which the orbiter disintegrated. He also would have been the CAPCOM operator for the canceled STS-61-F mission during launch and landing.
</excerpt>
### Rank 3 of 62 — 0.14
<excerpt title="Discovery's Commander Confident Space Shuttle Will Launch">
# Discovery's Commander Confident Space Shuttle Will Launch
News
By Tariq Malik
Published July 16, 2005
When you purchase through links on our site, we may earn an affiliate commission. Here’s how it works.
STS-114 commander Eileen Collins will make her fourth spaceflight aboard the space shuttle Discovery.(Image credit: NASA/JSC.)
Share
*    Copy link   
*   Facebook  
*   X  
*   Reddit  
*   Pinterest  
*   Flipboard  
*   [Email](mailto:?subject=I%20found%20this%20webpage&body=Hi,%20I%20found%20this%20webpage%20and%20thought%20you%20might%20like%20it%20https://www.space.com/1320-discovery-commander-confident-space-shuttle-launch.html)
Share this article
Join the conversation
Follow us
Add us as a preferred source on Google
Newsletter
Subscribe to our newsletter
CAPECANAVERAL, Fla. - With an exact launch date for their STS-114 mission still upin the air, seven space shuttle astronauts are hanging tight here at NASA'sKennedy Space Center (KSC), the spaceflight's commander said in a statementreleased Saturday.
"Mycrew will remain in quarantine for the near future, maintaining our proficiencyfor this mission," said veteran astronaut Eileen Collins, commander of STS-114mission aboard the shuttle Discovery, in the statement. "We are keeping inclose touch with the troubleshooting plan; we have confidence that the bestpeople are working it."
Shuttleofficials said that they may be able to launch Discovery late nextweek, but only if engineers get lucky and are able to find and fix thesensor system glitch soon. But that's not set in stone, and launch officials planinstead to launch the shuttle mission four days after a fix is made, theyadded.
Latest Videos From Space
View more
Watch full video here:
</excerpt>
### Rank 4 of 62 — 0.14
<excerpt title="STS-82">
# STS-82
## Mission Highlights
EVA 2 began at 10:25 p.m., Feb. 14, and lasted seven hours, 27 minutes. Harbaugh and Tanner replaced a degraded Fine Guidance Sensor and a failed Engineering and Science Tape Recorder with new spares. Also installed a new unit called the Optical Control Electronics Enhancement Kit, which will further increase the capability of the Fine Guidance Sensor. During this EVA astronauts noted cracking and wear on thermal insulation on side of telescope facing the sun and in the direction of travel.
EVA 3 began at 9:53 p.m., Feb. 15, and lasted seven hours, 11 minutes. Lee and Smith removed and replaced a Data Interface Unit on Hubble, as well as an old reel-to-reel- style Engineering and Science Tape Recorder with a new digital Solid State Recorder (SSR) that will allow simultaneous recording and playback of data. Also changed out one of four Reaction Wheel Assembly units that use spin momentum to move the telescope toward a target and maintain it in a stable position. After this EVA, mission managers decided to add EVA 5 to repair the thermal insulation on HST.
EVA 4 began at 10:45 p.m., Feb. 16, and lasted six hours, 34 minutes. Harbaugh and Tanner replaced a Solar Array Drive Electronics package which controls the positioning of Hubble’s solar arrays. Also replaced were covers over Hubble’s magnetometers and thermal blankets of multi-layer material over two areas of degraded insulation around the light shield portion of the telescope just below the top of the observatory. Meanwhile, inside Discovery, Horowitz and Lee worked on the middeck to fabricate new insulation blankets for HST.
Final space walk, EVA 5, lasted five hours, 17 minutes. Lee and Smith attached several thermal insulation blankets to three equipment compartments at the top of the Support Systems Module section of the telescope which contain key data processing, electronics and scientific instrument telemetry packages. STS-82 EVA totaled 33 hours, 11 minutes about two hours shy of total EVA time recorded on the first servicing mission.

# STS-82
## Mission Highlights
Discovery’s maneuvering jets fired several times during the mission to reboost the telescope’s orbit by eight nautical miles. Hubble redeployed on Feb. 19 at 1:41 a.m. and is now operating at the highest altitude it has ever flown, a 335- by 321-nautical-mile orbit. Initial checkout of new instruments and equipment during mission showed all were performing nominally. Calibration of two new science instruments was to take place over a period of several weeks with first images and data anticipated in about 8 to 10 weeks. Two more servicing are missions planned for 1999 and 2002.
Performance of Discovery was nominal throughout the mission.
Hubble Servicing Mission

# STS-82
## Servicing Mission 2
The mission extended the range of wavelengths Hubble can see and increased its efficiency and performance.
Explore SM2 Details
Close-up of astronaut Steven L. Smith, STS-82 mission specialist, during Extravehicular Activity (EVA), for the Hubble Space Telescope (HST) repair. (14 Feb. 1997)

# STS-82
## STS-82
23 Images
Go To Gallery
Go To Gallery

# STS-82
## Resources


# STS-82
## STS-82 Press Kit
Get an overview of the STS mission, its crew and activities during this mission.

# STS-82
## Discovery Fact Sheet
An overview of this shuttle's flights.
</excerpt>
### Rank 5 of 62 — 0.13
<excerpt title="STS-26">
The crew roster for STS-26 was based on the original crew assignment for STS-61-F, which would have launched the _Ulysses_ probe from _Challenger_ in 1986. _Ulysses_ was eventually launched on STS-41. Hauck, Lounge and Hilmers were all assigned to that flight, with [Roy D. Bridges Jr.](https://en.wikipedia.org/wiki/Roy_D._Bridges_Jr. "Roy D. Bridges Jr.") as pilot. Bridges never flew again after the _Challenger_ disaster, but would eventually become the director of Langley Research Center (LRC).
Covey was the CAPCOM operator during the STS-51-L launch who uttered the words, "_Challenger_, go at throttle up" to commander Francis R. Scobee, shortly after which the orbiter disintegrated. He also would have been the CAPCOM operator for the canceled STS-61-F mission during launch and landing.

### Crew seat assignments
[edit]
| Seat[[2]](https://en.wikipedia.org/wiki/STS-26#cite_note-2) | Launch | Landing |  Seats 1–4 are on the flight deck. Seats 5–7 are on the mid-deck. |  
| --- | --- | --- |  
| 1 | Hauck |  
| 2 | Covey |  
| 3 | Lounge |  
| 4 | Hilmers |  
| 5 | Nelson |  
| 6 | _Unused_ |  
| 7 | _Unused_ |
_Discovery_ lifts off from KSC, the first shuttle mission after the _Challenger_ disaster
Space Shuttle _Discovery_ lifted off from Launch Complex 39B, Kennedy Space Center, at 11:37:00 a.m. EDT on September 29, 1988, 975 days after the _Challenger_ disaster.
The launch was delayed by one hour and thirty-eight minutes due to unseasonable and unusual light winds, and the need to replace fuses in the cooling systems of two crew members' flight suits. The suits were repaired, and a waiver was issued for the wind conditions after officials determined there was a sufficient safety margin for wind loads on the orbiter's wing leading edges. At T−1:30, it was proposed that the launch be delayed at T−0:31 due to a cabin air pressure issue. It was quickly determined that the cabin pressure had been increased slightly by the activation of the oxygen systems in the crew's flight suits, and the launch was conducted without further delay. The shuttle crew—all veteran astronauts—included Commander Frederick H. "Rick" Hauck, Pilot Richard O. Covey, and Mission Specialists John M. "Mike" Lounge, George D. "Pinky" Nelson and David C. Hilmers.
The primary payload for the STS-26 mission, TDRS-C, was successfully deployed, and 11 scheduled mid-deck scientific and technological experiments were carried out. The post-_Challenger_ redesigned solid rocket booster segment joints showed no signs of leakage or overheating.[[a]](https://en.wikipedia.org/wiki/STS-26#cite_note-3)
</excerpt>

## Search 10 — query: "Discovery Space Shuttle missions commander table"
### Rank 1 of 98 — 0.58 (passed on)
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
### Rank 2 of 98 — 0.55
<excerpt title="List of Space Shuttle crews">
# List of Space Shuttle crews
## 1996–2000
| 86 | August 7 | 1997 | STS-85 | _Discovery_ | 11 d 20 h | C. Brown | Rominger | Davis | Robinson | Curbeam |  |  | Tryggvason  |  |  
| 87 | September 25 | 1997 | STS-86 | _Atlantis_ | 10 d 19 h | Wetherbee | Bloomfield | Titov  | Parazynski | Chrétien  | Lawrence | Wolf**Mir** | _Foale_ |  |  
| 88 | November 19 | 1997 | STS-87 | _Columbia_ | 15 d 16 h | Kregel | Lindsey | Scott | Chawla | Doi  |  |  | Kadenyuk  |  |  
| 89 | January 22 | 1998 | STS-89 | _Endeavour_ | 8 d 19 h | Wilcutt | [Edwards](https://en.wikipedia.org/wiki/Joe_F._Edwards_Jr. "Joe F. Edwards Jr.") | Dunbar**PC** | M.Anderson | Reilly | Sharipov  | A.Thomas**Mir** | _Wolf_ |  |  
| 90 | April 17 | 1998 | STS-90 | _Columbia_ | 15 d 21 h | Searfoss | Altman | Linnehan | D. Williams  | Hire |  |  | Buckey | Pawelczyk |  
| 91 | June 2 | 1998 | STS-91 | _Discovery_ | 9 d 19 h | Precourt | Gorie | Lawrence | Chang-Diaz | Kavandi | Ryumin  |  | _A. Thomas_ |  |  
| 92 | October 29 | 1998 | STS-95 | _Discovery_ | 8 d 21 h | C. Brown | Lindsey | Robinson**PC** | Parazynski | Duque  |  |  | Mukai  | Glenn |
</excerpt>
### Rank 3 of 98 — 0.52
<excerpt title="List of Space Shuttle crews">
# List of Space Shuttle crews
## 1986–1990
| 31 | October 18 | 1989 | STS-34 | _Atlantis_ | 4 d 23 h | D. E. Williams | McCulley | Chang-Diaz | Lucid | E. Baker |  |  |  
| 32 | November 22 | 1989 | STS-33 | _Discovery_ | 5 d 0 h | Gregory | Blaha | Musgrave | Carter | K.Thornton |  |  |  
| 33 | January 9 | 1990 | STS-32 | _Columbia_ | 10 d 21 h | Brandenstein | Wetherbee | Dunbar | Low | Ivins |  |  |  
| 34 | February 28 | 1990 | STS-36 | _Atlantis_ | 4 d 10 h | Creighton | Casper | Mullane | Hilmers | Thuot |  |  |  
| 35 | April 24 | 1990 | STS-31 | _Discovery_ | 5 d 1 h | Shriver | [Bolden](https://en.wikipedia.org/wiki/Charles_F._Bolden_Jr. "Charles F. Bolden Jr.") | Hawley | McCandless | Sullivan |  |  |  
| 36 | October 6 | 1990 | STS-41 | _Discovery_ | 4 d 2 h | R. Richards | Cabana | Shepherd | Melnick | Akers |  |  |  
| 37 | November 15 | 1990 | STS-38 | _Atlantis_ | 4 d 21 h | Covey | [Culbertson](https://en.wikipedia.org/wiki/Frank_L._Culbertson_Jr. "Frank L. Culbertson Jr.") | Springer | Meade | Gemar |  |  |  
| 38 | December 2 | 1990 | STS-35 | _Columbia_ | 8 d 23 h | Brand | G.Gardner | Hoffman | Lounge | Parker | Durrance | Parise |
</excerpt>
### Rank 4 of 98 — 0.42
<excerpt title="List of Space Shuttle crews">
# List of Space Shuttle crews
## 2001–2005
[edit]
| Order | Day | Year | Mission | Shuttle | Duration | Commander | Pilot | Mission specialists | Payload specialists |  
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |  
| 102 | February 7 | 2001 | STS-98 | _Atlantis_ | 12 d 21 h | Cockrell | Polansky | Curbeam | Jones | Ivins |  |  |  |  |  |  
| 103 | March 8 | 2001 | STS-102 | _Discovery_ | 12 d 19 h | Wetherbee | J. Kelly | A.Thomas | P.Richards | Usachev**ISS**  | J. S. Voss**ISS** | Helms**ISS** | _Shepherd_ | _Gidzenko_  | _Krikalev_  |  
| 104 | April 19 | 2001 | STS-100 | _Endeavour_ | 11 d 21 h | Rominger | Ashby | Hadfield  | Parazynski | Phillips | Guidoni  | Lonchakov  |  |  |  |  
| 105 | July 12 | 2001 | STS-104 | _Atlantis_ | 12 d 18 h | Lindsey | Hobaugh | Gernhardt | Reilly | Kavandi |  |  |  |  |  |  
| 106 | August 10 | 2001 | STS-105 | _Discovery_ | 11 d 21 h | Horowitz | Sturckow | Barry | Forrester | [Culbertson](https://en.wikipedia.org/wiki/Frank_L._Culbertson_Jr. "Frank L. Culbertson Jr.")**ISS** | Tyurin**ISS**  | Dezhurov**ISS**  | _Usachev_  | _J. S. Voss_ | _Helms_ |
</excerpt>
### Rank 5 of 98 — 0.40
<excerpt title="List of Space Shuttle crews">
# List of Space Shuttle crews
## 2006–2011
| 125 | March 15 | 2009 | STS-119 | _Discovery_ | 12 d 19 h 31 min 1 s | Archambault | Antonelli | Acaba | Swanson | Arnold | Phillips | Wakata**ISS**  | _Magnus_ |  
| 126 | May 11 | 2009 | STS-125 | _Atlantis_ | 12 d 21 h 38 min 19 s | Altman | G. C. Johnson | Good | M. McArthur | Grunsfeld | Massimino | Feustel |  |  
| 127 | July 15 | 2009 | STS-127 | _Endeavour_ | 15 d 16 h 44 min 58 s | Polansky | Hurley | Cassidy | Payette  | Marshburn | Wolf | Kopra**ISS** | _Wakata_  |  
| 128 | August 28 | 2009 | STS-128 | _Discovery_ | 13 d 20 h 54 min 55 s | Sturckow | Ford | Forrester | Hernández | Fuglesang  | Olivas | Stott**ISS** | _Kopra_ |  
| 129 | November 16 | 2009 | STS-129 | _Atlantis_ | 10 d 19 h 16 min 13 s | Hobaugh | Wilmore | Melvin | Bresnik | Foreman | Satcher |  | _Stott_ |  
| 130 | February 8 | 2010 | STS-130 | _Endeavour_ | 13 d 18 h 8 min 3 s | Zamka | Virts | Hire | Robinson | Patrick | Behnken |  |  |  

# List of Space Shuttle crews
## 2006–2011
| 131 | April 5 | 2010 | STS-131 | _Discovery_ | 15 d 2 h 47 min 11 s | Poindexter | Dutton | Mastracchio | Metcalf-Lindenburger | Wilson | Yamazaki  | C.Anderson |  |  
| 132 | May 14 | 2010 | STS-132 | _Atlantis_ | 11 d 18 h 29 min | Ham | Antonelli | Reisman | Good | Bowen | Sellers |  |  |  
| 133 | February 24 | 2011 | STS-133 | _Discovery_ | 12 d 19 h 4 min 50 s | Lindsey | Boe | Stott | Drew | Barratt | Bowen |  |  |  
| 134 | May 16 | 2011 | STS-134 | _Endeavour_ | 15 d 17 h 38 min 51 s | M. Kelly | G. H. Johnson | Fincke | Vittori  | Feustel | Chamitoff |  |  |  
| 135 | July 8 | 2011 | STS-135 | _Atlantis_ | 12 d 18 h 28 min 50 s | Ferguson | Hurley | Magnus | Walheim |  |  |  |  |
</excerpt>

# Example 3
## Question
Between Earth's moon and Mars' moons, name all features that share a namesake with pre-20th century literary figures (names inspired by them), specifically, those who were known to primarily write fiction or poetry, and whose names were approved in 1973. Use https://planetarynames.wr.usgs.gov/ to source your info.

## Expected answer
Brontë (lunar crater, earth's moon) 
Shakespeare (lunar crater, earth's moon) 
Swift (crater, mars' moon deimos)
Voltaire (crater, mars' moon deimos)
Lucian (crater, earth's moon)

## Grade 0.25

## Search 1 — query: "Lunar crater named after fiction writer approved 1973"
### Rank 1 of 30 — 0.65 (passed on)
<excerpt title="Jules Verne (crater)">
From Wikipedia, the free encyclopedia
Jules Verne  
LRO image of Jules Verne crater  
Coordinates35°00′S 147°00′E / 35.0°S 147.0°E  
Diameter143 km  
Depth_Unknown_  
Colongitude215° at sunrise  
EponymJules Verne
**Jules Verne** is a large lunarimpact crater on the far side of the Moon,[[1]](https://en.wikipedia.org/wiki/Jules_Verne_(crater)#cite_note-Moore_2000-1) named after the French author. It is located to the west-southwest of the Mare Ingenii, one of the few lunar mares on the far side. To the southeast of Jules Verne is the crater Lundmark, while Koch is located to the south-southeast. To the northwest is Pavlov, a large walled plain.
Most of the interior floor of this crater has been flooded with basalticlava, leaving a dark, low-albedo surface that is relatively level and flat. It is somewhat unusual for a crater feature on the far side to be flooded with lava, as the crust is generally thicker than on the near side. The crater is located in the outer rim of the South Pole-Aitken basin.
The outer rim of Jules Verne is worn and eroded, with several craters lying across the edge. Along the eastern edge lies Jules Verne G, while Jules Verne C penetrates the northeastern rim and Jules Verne Z cuts across the northern rim. A small crater also lies across the southern rim, while Jules Verne P is attached to the exterior along the south-southwest.
Jules Verne is one of the few lunar craters that is known by a person's full name rather than the surname. It is also named for a science-fiction author rather than a noted scientist or explorer, as is typical. (But see H. G. Wells.)
By convention, these features are identified on lunar maps by placing the letter on the side of the crater midpoint that is closest to Jules Verne.[[2]](https://en.wikipedia.org/wiki/Jules_Verne_(crater)#cite_note-Grego_2015-2)
Jules Verne satellite craters
Oblique Lunar Orbiter 2 image of Jules Verne, facing south

| Jules Verne | Latitude | Longitude | Diameter |  
| --- | --- | --- | --- |  
| C | 33.2° S | 149.7° E | 30 km |  
| G | 35.1° S | 150.0° E | 42 km |  
| P | 38.0° S | 145.1° E | 62 km |  
| R | 36.9° S | 140.9° E | 49 km |  
| X | 32.1° S | 145.2° E | 15 km |  
| Y | 31.3° S | 146.0° E | 30 km |  
| Z | 32.5° S | 146.8° E | 20 km |
1.   ↑Moore, Patrick (2000). _The Data Book of Astronomy_. CRC Press. p.68. ISBN978-1-4200-3344-1.  
2.   ↑Grego, P. (2015). "Satellite Crater". In Hargitai, H.; Kereszturi, Á. (eds.). _Encyclopedia of Planetary Landforms_. New York, NY: Springer. doi:10.1007/978-1-4614-3134-3_328.
</excerpt>
### Rank 2 of 30 — 0.65
<excerpt title="H. G. Wells (crater)">
From Wikipedia, the free encyclopedia
H. G. Wells
Oblique Lunar Orbiter 5 image, facing west  
Coordinates40°50′N 122°38′E / 40.84°N 122.63°E  
Diameter108.90 km (67.67 mi)  
Depth_Unknown_  
Colongitude239° at sunrise  
EponymH. G. Wells
Oblique Apollo 16 mapping camera image
Oblique Apollo 14 Hasselblad camera image
**H. G. Wells** is a lunarimpact crater that is located on the far side of the Moon,[[1]](https://en.wikipedia.org/wiki/H._G._Wells_(crater)#cite_note-Moore_2000-1) behind the northeastern limb. It lies to the south of the crater Millikan, and to the northeast of Cantor. Just to the southeast is the smaller Tesla.
This large formation is most notable for the extremely battered state of its outer rim. Little or nothing remains of the original rim, so completely has it been eroded and incised by smaller craters. As a result, the crater floor is now surrounded by a ring of irregular peaks and worn crater valleys. This rugged surroundings intrudes only part way into the interior, while the remaining floor is relatively level and in some places gently rolling. The interior is marked only by a multitude of tiny craters.
The crater is named after the author H. G. Wells whose works include the 1901 novel _The First Men in the Moon_. Prior to formal naming by the IAU in 1970,[[2]](https://en.wikipedia.org/wiki/H._G._Wells_(crater)#cite_note-2) H. G. Wells was called _Crater 48_.[[3]](https://en.wikipedia.org/wiki/H._G._Wells_(crater)#cite_note-3)
By convention these features are identified on lunar maps by placing the letter on the side of the crater midpoint that is closest to H. G. Wells.
| H. G. Wells | Latitude | Longitude | Diameter |  
| --- | --- | --- | --- |  
| X | 40.70° N | 122.80° E | 114 km |

1.   ↑Moore, Patrick (2000). _The Data Book of Astronomy_. CRC Press. p.72. ISBN978-1-4200-3344-1.  
2.   ↑H. G. Wells, Gazetteer of Planetary Nomenclature, International Astronomical Union (IAU) Working Group for Planetary System Nomenclature (WGPSN)  
3.   ↑Lunar Farside Chart (LFC-1A), 2nd Edition October 1967
</excerpt>
### Rank 3 of 30 — 0.29
<excerpt title="Jules Verne (crater)">
| Jules Verne | Latitude | Longitude | Diameter |  
| --- | --- | --- | --- |  
| C | 33.2° S | 149.7° E | 30 km |  
| G | 35.1° S | 150.0° E | 42 km |  
| P | 38.0° S | 145.1° E | 62 km |  
| R | 36.9° S | 140.9° E | 49 km |  
| X | 32.1° S | 145.2° E | 15 km |  
| Y | 31.3° S | 146.0° E | 30 km |  
| Z | 32.5° S | 146.8° E | 20 km |
1.   ↑Moore, Patrick (2000). _The Data Book of Astronomy_. CRC Press. p.68. ISBN978-1-4200-3344-1.  
2.   ↑Grego, P. (2015). "Satellite Crater". In Hargitai, H.; Kereszturi, Á. (eds.). _Encyclopedia of Planetary Landforms_. New York, NY: Springer. doi:10.1007/978-1-4614-3134-3_328.

*   Andersson, L. E.; Whitaker, E. A. (1982). _NASA Catalogue of Lunar Nomenclature_. NASA RP-1097.  
*   Blue, Jennifer (July 25, 2007). "Gazetteer of Planetary Nomenclature". USGS. Retrieved 2007-08-05.  
*   Bussey, B.; Spudis, P. (2004). _The Clementine Atlas of the Moon_. New York: Cambridge University Press. ISBN978-0-521-81528-4.  
*   Cocks, Elijah E.; Cocks, Josiah C. (1995). _Who's Who on the Moon: A Biographical Dictionary of Lunar Nomenclature_. Tudor Publishers. ISBN978-0-936389-27-1.  
*   McDowell, Jonathan (July 15, 2007). "Lunar Nomenclature". [Jonathan's Space Report](https://en.wikipedia.org/wiki/Jonathan's_Space_Report "Jonathan's Space Report"). Archived from the original on 2012-02-08. Retrieved 2007-10-24.  
*   Menzel, D. H.; Minnaert, M.; Levin, B.; Dollfus, A.; Bell, B. (1971). "Report on Lunar Nomenclature by the Working Group of Commission 17 of the IAU". _Space Science Reviews_. **12** (2): 136–186. Bibcode:1971SSRv...12..136M. doi:10.1007/BF00171763. S2CID122125855.  
*   Moore, Patrick (2001). _On the Moon_. [Sterling Publishing Co.](https://en.wikipedia.org/wiki/Sterling_Publishing_Co. "Sterling Publishing Co.")ISBN978-0-304-35469-6.
</excerpt>
### Rank 4 of 30 — 0.22
<excerpt title="H. G. Wells (crater)">
1.   ↑Moore, Patrick (2000). _The Data Book of Astronomy_. CRC Press. p.72. ISBN978-1-4200-3344-1.  
2.   ↑H. G. Wells, Gazetteer of Planetary Nomenclature, International Astronomical Union (IAU) Working Group for Planetary System Nomenclature (WGPSN)  
3.   ↑Lunar Farside Chart (LFC-1A), 2nd Edition October 1967

*   Andersson, L. E.; Whitaker, E. A. (1982). _NASA Catalogue of Lunar Nomenclature_. NASA RP-1097.  
*   Blue, Jennifer (July 25, 2007). "Gazetteer of Planetary Nomenclature". USGS. Retrieved 2007-08-05.  
*   Bussey, B.; Spudis, P. (2004). _The Clementine Atlas of the Moon_. New York: Cambridge University Press. ISBN978-0-521-81528-4.  
*   Cocks, Elijah E.; Cocks, Josiah C. (1995). _Who's Who on the Moon: A Biographical Dictionary of Lunar Nomenclature_. Tudor Publishers. ISBN978-0-936389-27-1.  
*   McDowell, Jonathan (July 15, 2007). "Lunar Nomenclature". [Jonathan's Space Report](https://en.wikipedia.org/wiki/Jonathan's_Space_Report "Jonathan's Space Report"). Archived from the original on 2012-02-08. Retrieved 2007-10-24.  
*   Menzel, D. H.; Minnaert, M.; Levin, B.; Dollfus, A.; Bell, B. (1971). "Report on Lunar Nomenclature by the Working Group of Commission 17 of the IAU". _Space Science Reviews_. **12** (2): 136–186. Bibcode:1971SSRv...12..136M. doi:10.1007/BF00171763. S2CID122125855.  
*   Moore, Patrick (2001). _On the Moon_. [Sterling Publishing Co.](https://en.wikipedia.org/wiki/Sterling_Publishing_Co. "Sterling Publishing Co.")ISBN978-0-304-35469-6.  

*   Price, Fred W. (1988). _The Moon Observer's Handbook_. Cambridge University Press. ISBN978-0-521-33500-3.  
*   Rükl, Antonín (1990). _Atlas of the Moon_. Kalmbach Books. ISBN978-0-913135-17-4.  
*   Webb, Rev. T. W. (1962). _Celestial Objects for Common Telescopes_ (6th revised ed.). Dover. ISBN978-0-486-20917-3.  
*   Whitaker, Ewen A. (1999). _Mapping and Naming the Moon_. Cambridge University Press. ISBN978-0-521-62248-6.  
*   Wlasuk, Peter T. (2000). _Observing the Moon_. Springer. ISBN978-1-85233-193-1.
</excerpt>
### Rank 5 of 30 — 0.16
<excerpt title="Jules Verne (crater)">
*   Andersson, L. E.; Whitaker, E. A. (1982). _NASA Catalogue of Lunar Nomenclature_. NASA RP-1097.  
*   Blue, Jennifer (July 25, 2007). "Gazetteer of Planetary Nomenclature". USGS. Retrieved 2007-08-05.  
*   Bussey, B.; Spudis, P. (2004). _The Clementine Atlas of the Moon_. New York: Cambridge University Press. ISBN978-0-521-81528-4.  
*   Cocks, Elijah E.; Cocks, Josiah C. (1995). _Who's Who on the Moon: A Biographical Dictionary of Lunar Nomenclature_. Tudor Publishers. ISBN978-0-936389-27-1.  
*   McDowell, Jonathan (July 15, 2007). "Lunar Nomenclature". [Jonathan's Space Report](https://en.wikipedia.org/wiki/Jonathan's_Space_Report "Jonathan's Space Report"). Archived from the original on 2012-02-08. Retrieved 2007-10-24.  
*   Menzel, D. H.; Minnaert, M.; Levin, B.; Dollfus, A.; Bell, B. (1971). "Report on Lunar Nomenclature by the Working Group of Commission 17 of the IAU". _Space Science Reviews_. **12** (2): 136–186. Bibcode:1971SSRv...12..136M. doi:10.1007/BF00171763. S2CID122125855.  
*   Moore, Patrick (2001). _On the Moon_. [Sterling Publishing Co.](https://en.wikipedia.org/wiki/Sterling_Publishing_Co. "Sterling Publishing Co.")ISBN978-0-304-35469-6.  

*   Price, Fred W. (1988). _The Moon Observer's Handbook_. Cambridge University Press. ISBN978-0-521-33500-3.  
*   Rükl, Antonín (1990). _Atlas of the Moon_. Kalmbach Books. ISBN978-0-913135-17-4.  
*   Webb, Rev. T. W. (1962). _Celestial Objects for Common Telescopes_ (6th revised ed.). Dover. ISBN978-0-486-20917-3.  
*   Whitaker, Ewen A. (1999). _Mapping and Naming the Moon_. Cambridge University Press. ISBN978-0-521-62248-6.  
*   Wlasuk, Peter T. (2000). _Observing the Moon_. Springer. ISBN978-1-85233-193-1.
*   High resolution lunar overflight video by Seán Doran, based on LRO data, that passes over Jules Verne at the end (see album for more); other videos on YouTube pass over Jules Verne near the beginning or two thirds of the way through
</excerpt>

## Search 2 — query: "planetarynames 1973 moon feature approval 1973 moon crater"
### Rank 1 of 50 — 0.56 (passed on)
<excerpt title="List of craters on the Moon: A–B">
Bowen17°38′N 9°06′E / 17.63°N 9.1°E8.09 1973Ira Sprague Bowen (1898–1973)WGPSN  
Boyle53°17′S 177°53′E / 53.29°S 177.89°E57.13 1970Robert Boyle (1627–1691)WGPSN  
Brackett17°50′N 23°32′E / 17.84°N 23.54°E8.87 1973Frederick Sumner Brackett (1896–1988)WGPSN  
Bragg42°20′N 103°26′W / 42.33°N 103.44°W77.21 1970William Henry Bragg (1862–1942)WGPSN  
Brashear73°32′S 171°34′W / 73.54°S 171.57°W60.16 1970John Alfred Brashear (1840–1920)WGPSN  
Braude81°49′S 158°53′E / 81.82°S 158.88°E11.28 2009Semion Braude (1911–2003)WGPSN  
Brayley20°54′N 36°56′W / 20.9°N 36.94°W14.17 1935Edward William Brayley (1801–1870)WGPSN  

Bredikhin17°15′N 158°22′W / 17.25°N 158.37°W61.68 1970Fedor Aleksandrovich Bredikhin (1831–1904)WGPSN  
Breislak48°19′S 18°19′E / 48.31°S 18.31°E48.64 1935Scipione Breislak (1748–1826)WGPSN  
Brenner39°05′S 39°07′E / 39.09°S 39.11°E90.01 1935Leo Brenner (1855–1928)WGPSN  
Brewster23°16′N 34°41′E / 23.27°N 34.69°E9.83 1976David Brewster (1781–1868)WGPSN  
Brianchon74°45′N 88°22′W / 74.75°N 88.36°W137.26 1964Charles Julien Brianchon (1783–1864)WGPSN  
Bridgman43°23′N 136°59′E / 43.39°N 136.98°E81.89 1970Percy Williams Bridgman (1882–1961)WGPSN  
Briggs26°27′N 69°11′W / 26.45°N 69.19°W36.75 1935Henry Briggs (1561–1630)WGPSN
</excerpt>
### Rank 2 of 50 — 0.40
<excerpt title="List of craters on the Moon: A–B">
Bosch86°49′N 133°32′E / 86.82°N 133.54°E19.58 2009Carl Bosch (1874–1940)WGPSN  
Boscovich9°43′N 11°01′E / 9.71°N 11.01°E41.53 1935Ruggiero Giuseppe Boscovich (1711–1787)WGPSN  
Bose53°57′S 169°22′W / 53.95°S 169.36°W92.55 1970Jagadish Chandra Bose (1858–1937)WGPSN  
Boss45°45′N 88°41′E / 45.75°N 88.68°E50.2 1964Lewis Boss (1846–1912)WGPSN  
Bouguer52°19′N 35°49′W / 52.32°N 35.82°W22.23 1935Pierre Bouguer (1698–1758)WGPSN  
Boussingault70°13′S 53°44′E / 70.21°S 53.73°E127.61 1935Jean Baptiste Boussingault (1802–1887)WGPSN  
Bowditch24°58′S 103°04′E / 24.97°S 103.07°E43.04 1976Nathaniel Bowditch (1773–1848)WGPSN  

Bowen17°38′N 9°06′E / 17.63°N 9.1°E8.09 1973Ira Sprague Bowen (1898–1973)WGPSN  
Boyle53°17′S 177°53′E / 53.29°S 177.89°E57.13 1970Robert Boyle (1627–1691)WGPSN  
Brackett17°50′N 23°32′E / 17.84°N 23.54°E8.87 1973Frederick Sumner Brackett (1896–1988)WGPSN  
Bragg42°20′N 103°26′W / 42.33°N 103.44°W77.21 1970William Henry Bragg (1862–1942)WGPSN  
Brashear73°32′S 171°34′W / 73.54°S 171.57°W60.16 1970John Alfred Brashear (1840–1920)WGPSN  
Braude81°49′S 158°53′E / 81.82°S 158.88°E11.28 2009Semion Braude (1911–2003)WGPSN  
Brayley20°54′N 36°56′W / 20.9°N 36.94°W14.17 1935Edward William Brayley (1801–1870)WGPSN
</excerpt>
### Rank 3 of 50 — 0.36
<excerpt title="List of craters on the Moon: A–B">
Baade44°45′S 82°02′W / 44.75°S 82.03°W57.85 1964Walter Baade (1893–1960)WGPSN  
Babakin20°49′S 123°16′E / 20.81°S 123.26°E19.15 1973Georgij N. Babakin (1914–1971)WGPSN  
Babbage59°34′N 57°23′W / 59.56°N 57.38°W146.56 1935Charles Babbage (1792–1871)WGPSN  
Babcock4°08′N 94°08′E / 4.13°N 94.14°E95.28 1970Harold D. Babcock (1882–1968)WGPSN  
Back1°12′N 80°40′E / 1.2°N 80.67°E34.63 1976Ernst Emil Alexander Back (1881–1959)WGPSN  
Backlund16°13′S 103°21′E / 16.22°S 103.35°E75.46 1970Oskar Backlund (1846–1916)WGPSN  
Baco51°02′S 19°06′E / 51.04°S 19.1°E65.31 1935Roger Bacon (c. 1214 – c. 1294)WGPSN  

Baillaud74°37′N 37°21′E / 74.61°N 37.35°E89.44 1935Benjamin Baillaud (1848–1934)WGPSN  
Bailly66°49′S 68°54′W / 66.82°S 68.9°W300.56 1935Jean Sylvain Bailly (1736–1793)WGPSN  
Baily49°47′N 30°34′E / 49.78°N 30.56°E25.68 1935Francis Baily (1774–1844)WGPSN  
Balandin18°56′S 152°35′E / 18.94°S 152.58°E11.81 1976Aleksei Aleksandrovich Balandin (1898–1967)WGPSN  
Balboa19°14′N 83°19′W / 19.24°N 83.31°W69.19 1964Vasco Núñez de Balboa (1475–1519)WGPSN  
Baldet53°19′S 151°58′W / 53.32°S 151.96°W55.76 1970Fernand Baldet (1885–1964)WGPSN  
Ball35°55′S 8°23′W / 35.92°S 8.39°W40.31 1935William Ball (died 1690)WGPSN
</excerpt>
### Rank 4 of 50 — 0.30
<excerpt title="List of craters on the Moon: A–B">
Baillaud74°37′N 37°21′E / 74.61°N 37.35°E89.44 1935Benjamin Baillaud (1848–1934)WGPSN  
Bailly66°49′S 68°54′W / 66.82°S 68.9°W300.56 1935Jean Sylvain Bailly (1736–1793)WGPSN  
Baily49°47′N 30°34′E / 49.78°N 30.56°E25.68 1935Francis Baily (1774–1844)WGPSN  
Balandin18°56′S 152°35′E / 18.94°S 152.58°E11.81 1976Aleksei Aleksandrovich Balandin (1898–1967)WGPSN  
Balboa19°14′N 83°19′W / 19.24°N 83.31°W69.19 1964Vasco Núñez de Balboa (1475–1519)WGPSN  
Baldet53°19′S 151°58′W / 53.32°S 151.96°W55.76 1970Fernand Baldet (1885–1964)WGPSN  
Ball35°55′S 8°23′W / 35.92°S 8.39°W40.31 1935William Ball (died 1690)WGPSN  

Balmer20°16′S 70°13′E / 20.27°S 70.22°E136.3 1964Johann Balmer (1825–1898)WGPSN  
Banachiewicz5°17′N 80°01′E / 5.28°N 80.01°E99.09 1964Tadeusz Banachiewicz (1882–1954)WGPSN  
Bancroft28°04′N 6°26′W / 28.07°N 6.43°W12.5 1976Wilder Dwight Bancroft (1867–1953)WGPSN  
Bandfield5°24′S 90°46′E / 5.40°S 90.77°E1.0 2022Joshua Bandfield (1974–2019)WGPSN  
Banting26°35′N 16°26′E / 26.58°N 16.43°E5.15 1973Frederick Banting (1891–1941)WGPSN  
Barbier23°51′S 157°56′E / 23.85°S 157.93°E65.38 1970Daniel Barbier (1907–1965)WGPSN  
Barkla10°40′S 67°13′E / 10.67°S 67.22°E40.9 1979Charles Glover Barkla (1877–1944)WGPSN  
Barnard29°47′S 85°57′E / 29.79°S 85.95°E115.73 1964Edward Emerson Barnard (1857–1923)WGPSN
</excerpt>
### Rank 5 of 50 — 0.26
<excerpt title="List of craters on the Moon: A–B">
Balmer20°16′S 70°13′E / 20.27°S 70.22°E136.3 1964Johann Balmer (1825–1898)WGPSN  
Banachiewicz5°17′N 80°01′E / 5.28°N 80.01°E99.09 1964Tadeusz Banachiewicz (1882–1954)WGPSN  
Bancroft28°04′N 6°26′W / 28.07°N 6.43°W12.5 1976Wilder Dwight Bancroft (1867–1953)WGPSN  
Bandfield5°24′S 90°46′E / 5.40°S 90.77°E1.0 2022Joshua Bandfield (1974–2019)WGPSN  
Banting26°35′N 16°26′E / 26.58°N 16.43°E5.15 1973Frederick Banting (1891–1941)WGPSN  
Barbier23°51′S 157°56′E / 23.85°S 157.93°E65.38 1970Daniel Barbier (1907–1965)WGPSN  
Barkla10°40′S 67°13′E / 10.67°S 67.22°E40.9 1979Charles Glover Barkla (1877–1944)WGPSN  
Barnard29°47′S 85°57′E / 29.79°S 85.95°E115.73 1964Edward Emerson Barnard (1857–1923)WGPSN
</excerpt>

## Search 3 — query: "Lunar crater approved 1973 "planetarynames""
### Rank 1 of 61 — 0.19 (passed on)
<excerpt title="NASA's Lunar Reconnaissance Orbiter Discovers a New 222-m ...">
# NASA's Lunar Reconnaissance Orbiter Discovers a New 222-m Diameter Lunar Crater
## Share this article
The crater is also surrounded by a bright blanket of ejecta — rock and dust that splashed out in all directions when the impact occurred — that extends hundreds of meters from the rim.
**Additional Information**
**After the embargo lifts, anyone may view a copy of the manuscript at****https://www.science.org/journal/sciadv****.**
**Reporters can access the paper at VancePak,****https://www.eurekalert.org/press/vancepak/****.**
**For reporters having difficulties accessing the paper from the press package, please have them contact**[**vancepak@aaas.org**](mailto:vancepak@aaas.org)**.**
**For information on Planetary names, go to**(https://planetarynames.wr.usgs.gov/Feature/16447).
Authors of the **_Science Advances_** paper: Mark S. Robinson, Aaron K. Boyd, Prasun Mahanti, Madeleine R. Manheim, Emerson J. Speyerer, Julie D. Stopar, Robert V. Wagner
**About LPI**
The Lunar and Planetary Institute (LPI), an institute of Universities Space Research Association, was established during the Apollo program in 1968 to foster international collaboration and to serve as a repository for information gathered during the early years of the space program. Today, the LPI is an intellectual leader in lunar and planetary science. The Institute serves as a scientific forum attracting world-class visiting scientists, postdoctoral fellows, students, and resident experts; supports and serves the research community through newsletters, meetings, and other activities; collects and disseminates planetary data, engages and excites the public about space science and invests in the development of future generations of scientists. The research carried out at the LPI supports NASA's efforts to explore the solar system.More information about LPI is available atwww.lpi.usra.edu.
**About USRA**
Founded in 1969, the Universities Space Research Association (USRA) is an independent, nonprofit organization that advances space- and Earth-related science, engineering, and technology through innovative research, education, and workforce development programs. USRA partners with government agencies, academic institutions, and industry to address some of the nation's most complex scientific and technical challenges.

# NASA's Lunar Reconnaissance Orbiter Discovers a New 222-m Diameter Lunar Crater
## Share this article
For more information, visitwww.usra.edu
PR Contact:
Suraiya Farukhi
[sfarukhi@usra.edu](mailto:sfarukhi@usra.edu)
443-812-6945
SOURCE Universities Space Research Association
×

# NASA's Lunar Reconnaissance Orbiter Discovers a New 222-m Diameter Lunar Crater
## Share this article
### Modal title


# NASA's Lunar Reconnaissance Orbiter Discovers a New 222-m Diameter Lunar Crater
## Also from this source
### General Lester Lyles Receives 2026 Lifetime Achievement Award from the Air & Space Forces Association General Lester Lyles, Chair of the Board of Trustees of Universities Space Research Association, has been awarded the 2026 AFA Lifetime Achievement...


# NASA's Lunar Reconnaissance Orbiter Discovers a New 222-m Diameter Lunar Crater
## Also from this source
### USRA Contributes Planetary Science Expertise to NASA-IBM Lunar Foundation Model Universities Space Research Association (USRA) contributed planetary science expertise, lunar dataset development, and scientific evaluation to the...
More Releases From This Source
</excerpt>
### Rank 2 of 61 — 0.14
<excerpt title="Nomenclature Search Results - Planetary Names">
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
Results Per Page:
25  
50  
100  
200  
500  
Add/Remove Columns
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
### Rank 3 of 61 — 0.13
<excerpt title="Smallest Named Crater I have Detected Imaging">
# Smallest Named Crater I have Detected Imaging
## Recommended Posts
### james7ca
Posted December 18, 2023
*   ### **james7ca**

*   Hubble  
*      
*       *    14,385 

*   Loc: San Diego, CA  
*   May 21, 2011

*   

*   #19
Posted December 18, 2023 (edited)
>  On 12/15/2023 at 9:06 PM, John the Space Traveler said:   
>   
>   
>   
> ...Neil Armstrong's first bootprint supposedly got covered/stomped on as they worked near the LM. I wonder if Aldrin's famous print got stepped on as well. If not, and they find it in the future, will this become the smallest named lunar feature? "Boot Crater", 0.0003 km! (tongue in cheek question)  
>   
>   
>
Well, how about the golf ball shot done by Alan Shepard on Apollo 14? I'm sure that formed some type of crater when it landed. Shepard said that it went "miles and miles" (which I'm sure was said just for effect).
As might relate to the OP's original request, does anyone know of a source that lists the smallest named craters? I mean when ordered by size, not just in a big data dump that contains all of the named craters.
**Edited December 18, 2023 by james7ca**
*    1 

*   Quote

# Smallest Named Crater I have Detected Imaging
## Recommended Posts
### Teemu Ohman
Posted December 18, 2023
*   ### **Teemu Ohman**

*   Explorer 1  
*      
*       *    69 

*   Loc: Finland  
*   November 16, 2023

*   

*   #20
Posted December 18, 2023
>  On 12/18/2023 at 8:59 AM, james7ca said:   
>   
>   
>   
> Well, how about the golf ball shot done by Alan Shepard on Apollo 14? I'm sure that formed some type of crater when it landed. Shepard said that it went "miles and miles" (which I'm sure was said just for effect).  
>   
>   
> As might relate to the OP's original request, does anyone know of a source that lists the smallest named craters? I mean when ordered by size, not just in a big data dump that contains all of the named craters.
The best way would be to do it yourself based on the Gazetteer (https://planetarynames.wr.usgs.gov/Page/MOON/target), making sure you download craters, satellite features and landing site names and then fiddle with the data in a spreadsheet of your choice. But yes, that is not what you wanted, i.e. it is a big data dump.
Another big data dump is the LPI Lunar Impact Crater Database (https://www.lpi.usra.edu/lunar/surface/Lunar_Impact_Crater_Database_v08Sep2015.xls). The present public version is an old one (2015) and it of course has mistakes etc., but for the small ones it's probably reasonably OK. I'm hoping to get an updated version out in 2024, but that's not a promise.
Here's everything up to 200 m from my current personal version (note that this version includes doublets and clusters too):
• Name D [km] Lat. Long.
• Ballet 0.01 20.17 30.57
• Block 0.01 -3.01 -23.42
</excerpt>
### Rank 4 of 61 — 0.11
<excerpt title="NASA's Lunar Reconnaissance Orbiter Discovers a New 222-m ...">
**Washington D.C., 2026 – September 16, 2026**. NASA’s Lunar Reconnaissance Orbiter Camera team recently discovered a new crater on the Moon that is twice the length of an American football field. The study, published _in Science Advances_, was conducted by members of NASA’s Lunar Reconnaissance Orbiter (LRO) science team, including Principal Investigator and lead author Dr. Mark Robinson of Intuitive Machines and co-author Dr. Julie Stopar of USRA’s Lunar and Planetary Institute.
The crater is scientifically important because it is the largest yet that was formed and discovered during LRO's lifetime at the Moon. Scientists estimate that it was formed between April 11 and May 22, 2024, about 2.5 years ago. It measures 222-m in diameter; this is a size that is estimated to form roughly once in a lifetime, or ~130 years. The crater shows the immediate effects of the impact cratering process before exposure to space and meteorite bombardment wears it down and hence is very useful for further studies.
It is officially named McGetchin crater after Thomas McGetchin by the International Astronomical Union (https://planetarynames.wr.usgs.gov/Feature/16447). Dr. McGetchin served as Director of the Lunar and Planetary Institute (LPI), then known as the Lunar Science Institute (LSI), beginning in 1977, the same year that marked the inaugural summer of the LPI Internships in Planetary Science Program. A renowned volcanologist and lunar scientist, McGetchin made lasting contributions to planetary science. The model of impact-crater ejecta developed by McGetchin and colleagues in 1973 remains an important framework for interpreting the formation and distribution of ejecta around impact craters and basins.
The new crater seems to have formed on a boundary between the cratered and craggy lunar highlands and a wide, flat mare. Its depth is about 43 meters on average.
The crater is also surrounded by a bright blanket of ejecta — rock and dust that splashed out in all directions when the impact occurred — that extends hundreds of meters from the rim.

###
**Additional Information**
**After the embargo lifts, anyone may view a copy of the manuscript at****https://www.science.org/journal/sciadv****.**
**Reporters can access the paper at VancePak,****https://www.eurekalert.org/press/vancepak/****.**
**For reporters having difficulties accessing the paper from the press package, please have them contact**[**vancepak@aaas.org**](mailto:vancepak@aaas.org)**.**
**For information on Planetary names, go to** (https://planetarynames.wr.usgs.gov/Feature/16447).
Authors of the _**Science Advances**_ paper: Mark S. Robinson, Aaron K. Boyd, Prasun Mahanti, Madeleine R. Manheim, Emerson J. Speyerer, Julie D. Stopar, Robert V. Wagner
**About LPI**
The Lunar and Planetary Institute (LPI), an institute of Universities Space Research Association, was established during the Apollo program in 1968 to foster international collaboration and to serve as a repository for information gathered during the early years of the space program. Today, the LPI is an intellectual leader in lunar and planetary science. The Institute serves as a scientific forum attracting world-class visiting scientists, postdoctoral fellows, students, and resident experts; supports and serves the research community through newsletters, meetings, and other activities; collects and disseminates planetary data, engages and excites the public about space science and invests in the development of future generations of scientists. The research carried out at the LPI supports NASA's efforts to explore the solar system. More information about LPI is available at www.lpi.usra.edu.
**About USRA**
Founded in 1969, the Universities Space Research Association (USRA) is an independent, nonprofit organization that advances space- and Earth-related science, engineering, and technology through innovative research, education, and workforce development programs. USRA partners with government agencies, academic institutions, and industry to address some of the nation’s most complex scientific and technical challenges.
For more information, visit www.usra.edu
</excerpt>
### Rank 5 of 61 — 0.09
<excerpt title="PUBLIC NAMING OF PLANETS AND PLANETARY SATELLITES">
## 5 Results and lessons to be learned
In spite of these hiccups, the final list of approved names [14] is quite remarkable (see Appendix 3). It is composed of a wide variety of names taken from mythology, literature, or are even pure creations, but somewhat unexpectedly there were no proposal from science-fiction lore. In line with the IAU culture, the approved names represent all the continents, and there is no strong bias towards a particular country or world region. Four winning proposals were received from North America (USA, Canada), one from Latin America and the Caribbean (Mexico), two from the Middle East & Africa (Morocco, Syria), six from Europe (France, Italy, Netherlands, Spain, Switzerland), and six from Asia–Pacific (Australia, Japan, Thailand). Also, winning proposals came not only from astronomy clubs, but from schools and universities as well.
In addition, from private sources we have significant evidence that the contest triggered local actions, or even lobbying, by clubs to promote astronomy towards a broader public.
A last – but not least – consideration was the press coverage during the contest: an OAO web survey showed that over 800 articles were published worldwide, from 54 countries, spread about equally between the pre-results and the post-results periods.
Altogether, we would conclude at this stage that the NameExoWorlds project has undeniably had a great public impact, in line with the long-standing successful tradition of IAU global initiatives in outreach and education.
References: IAU Press Releases and Announcements relevant to the NameExoWorlds project
(1) Format: “PR” = Press Release; “Ann” = Announcement; “/xxxNNNN/” is short for
http://www.iau.org/news/pressreleases/detail/iauNNNN/, and
http://www.iau.org/news/announcements/detail/annNNNNN/, respectively
Appendix 1: IAU role in naming planetary objects

## 5 Results and lessons to be learned
Through the recognition of national committees, academies, and governments, the IAU has been the international authority on celestial nomenclature since its inception in 1919. Among the IAU’s early activities were the international standardization of the nomenclature of surface features on the Moon (1935) and Mars (1958). Since 1973, planetary nomenclature has been handled by the IAU Division Working Group for Planetary System Nomenclature (WGPSN; formerly under Div.III, now under Div. F), with individual task groups assigned to planets and classes of objects (e.g. Moon, Mercury, Mars, Outer Solar System, Small Bodies).
Appendix 2: Composition of the EC-WG “Public Naming of Planets and Planetary Satellites” (end 2015):
To capitalize on the experience of the IAU in the public naming of Solar System objects (as explained in the text), its current composition, showing in particular a strong involvement of Div.F, is as follows:
*   •  
Science experts:
– Division F Planetary Systems and Bioastronomy: G. Valsecchi (past Div.F President)
– Div.F/WGPSN: R. Schulz (Chair WG)
– Div.F/WGSBN/MPC: G. Williams (MPC Associate Director)
– Div.F/WG Exoplanets for the Public: A. Lecavelier des Etangs (Chair WG; Commission F2 President); E. Mamajek
– Div.B/C.B2/WG Designations (stars): D. Lubovich
*   •  
Media/Outreach:
– IAU Press Office: L. L. Christensen (Press Officer)
– Office of Astronomy Outreach (OAO): Sze-leung Cheung (International Outreach Coordinator)
*   •  
Executive Committee members:
– P. Benvenuti (GS)
– Xiaowei Liu (Vice-President)
– T. Montmerle (past GS, EC-WG Chair)
– R. Williams (Past President)
Appendix 3: Stellar and planetary names officially adopted as a result of the NameExoWorlds contest
(Citations and club names can be found at http://nameexoworlds.iau.org/names).
</excerpt>

## Search 4 — query: ""Jules Verne" 1973 "planetary names""
### Rank 1 of 682 — 0.61 (passed on)
<excerpt title="Lista de cráteres lunares - Wikipedia, a enciclopedia libre">
Van der Waals	104 km	Johannes Van der Waals (1837–1923)  
Van Gent	43 km	Hendrik Van Gent (1900–1947)  
Van Maanen	60 km	Adriaan Van Maanen (1884–1946)  
van Rhijn	46 km	Pieter Johannes van Rhijn (1886–1960)  
Van Vleck	31 km	John Monroe Van Vleck (1833–1912)  
Van Wijk	32 km	Uco van Wijk (1924–1966)  
van't Hoff	92 km	Jacobus van 't Hoff (1852–1911)  
Vasco da Gama	83 km	Vasco da Gama (1469–1524)  
Vashakidze	44 km	Mikheil Alexandres dze Vashakidze (1909–1956)  
Vasya	0.1 km	Nome ruso masculino  
Vavilov	98 km	Nikolai Ivanovich Vavilov (1887–1943)  
Sergei Ivanovich Vavilov (1891–1951)  
Vega	75 km	Jurij Vega (1754–1802)  
Vendelinus	131 km	Godefroid Wendelin (1580–1667)  
Vening Meinesz	87 km	Felix A. Vening Meinesz (1887–1966)  
Ventris	95 km	Michael George Francis Ventris (1922–1956)  
Vera	2 km	Nome feminino latino  
Vernadskiy	91 km	Vladimir Ivanovich Vernadsky (1863–1945)  
Verne	2 km	Jules Verne  
Vertregt	187 km	Marinus Vertregt (1897–1973)
</excerpt>
### Rank 2 of 682 — 0.56
<excerpt title="Myths, Symbols and Legends of Solar System Bodies [1st ed.] 978-1-4614- ...">
believed to have discovered the gas helium. In addition to having Moon craters named after them, John Flamsteed has an astronomical society named after him based in Greenwich, England, and Norman Lockyer has an observatory named after him in Sidmouth, Devon. William Herschel (1738–1822) became the king’s astronomer. He discovered Uranus and built new telescopes that used metal mirrors rather than glass lenses, capturing much more light from the stars. Sir Isaac Newton (1642–1727) discovered gravity and invented calculus as way of describing things, such as planetary orbits, using mathematical language. The Descartes Crater is named after the French philosopher and mathematician Rene Descartes (1596–1650), perhaps most famous for his philosophical statement Cotigo ergo sum, or “I think therefore I am.” However, he also combined algebra and geometry, leading to equations for, among other things, ellipses. (Mercury has a weird elliptical orbit). The Maxwell Crater is named after the Scottish James Clerk Maxwell (1831–1879), who revealed that light is an electromagnetic wave. The Planck Crater is named after Max Karl Ernest Ludwig Planck (1858–1947), who is famous for Planck’s constant, which the quantum of action (minimum amount of any physical entity in an interaction) in quantum mechanics. The Becquerel Crater is named after Henri Becquerel, who discovered radioactivity. The Ohm Crater is named after Georg Ohm (1789–1854), a German physicist who is famous for Ohm’s law of electricity, V = I × R. Ohms are also a unit of measurement for electrical resistance. Enjar Hertzsprung has a crater named after him. He was a Danish chemist and astronomer (1873–1967) who created the HertzsprungRussell diagram to plot stars and their color and temperature. The Kuiper Moon crater is named after the Dutch-born U. S. astronomer Gerard Peter Kuiper (1905– 1973). The Kuiper Belt is also named after him, and he discovered Uranus’s moon Miranda and Neptune’s moon Nereid. The Viviani Crater is named after Vincenzo Viviani, a pupil of Galileo.

The Hubble Crater is obviously named after Edwin Hubble (1889–1953), the American astronomer who discovered other galaxies beyond our Milky Way, among other things; NASA’s Hubble Space Telescope is also named after him. There are a few other lunar craters that are named after writers such as the science fiction writers Jules Verne and H. G. Wells, as well as the Chaucer Crater named after the English writer and poet Geoffrey Chaucer (1343–1400), famous for writing The Canterbury Tales. The Dante Crater is named after Danti Alighiieri (1265–1312), an Italian poet famous for his Divine Comedy. There are many other named lunar craters not mentioned in this book. There is something enchanting and magical about our beautiful, lonely Moon that bathes our Earth in a romantic, silvery glow of light reflected from the Sun. The Moon has captured the imagination of so many cultures and peoples. The sight of the Moon’s beautiful face on a clear night never fails to fill people with awe, wonder and inspiration. As our nearest heavenly body and visible with the naked eye, there is much mythology concerning the Moon. The Moon, an almost constant celestial presence and frequently visible in the daytime, has had an enormous influence on China, its people, culture and customs
84
5
Craters, Dragons, Festivals, Gods and Goddesses of Earth’s Moon
</excerpt>
### Rank 3 of 682 — 0.55
<excerpt title="Lista de cráteres lunares - Wikipedia, a enciclopedia libre">
Isidorus	42 km	San Isidoro de Sevilla (c. 570-636)  
Isis	1 km	Isis (Exipto)  
Ivan	4 km	(Nome masculino Ruso)  
Izsak	30 km	Imre Izsak (1929–1965)  
Jeditareditar a fonte  
Cráter	Diámetro	Epónimo  
J. Herschel	165 km	John Herschel (1792–1871)  
Jackson	71 km	John Jackson (1887–1958)  
Jacobi	68 km	Karl Gustav Jacob Jacobi (1804–1851)  
Jansen	23 km	Zacharias Janszoon (1580-c. 1638)  
Jansky	72 km	Karl Jansky (1905–1950)  
Janssen	199 km	Pierre Jules César Janssen (1824–1907)  
Jarvis	38 km	Gregory Bruce Jarvis (1944–1986)  
Jeans	79 km	Sir James Hopwood Jeans (1877–1946)  
Jehan	5 km	(Turco nome feminino)  
Jenkins	38 km	Louise Freeland Jenkins (1888–1970)  
Jenner	71 km	Edward Jenner (1749–1823)  
Jerik	1 km	(Escandinavia nome masculino)  
Joliot	164 km	Frédéric Joliot-Curie (1900–1958)  
Jomo	7 km	(Afrikaans nome masculino)  
José	2 km	(Español nome masculino)  
Joule	96 km	James Prescott Joule (1818–1889)  
Joy	5 km	Alfred Harrison Joy (1882–1973)  
Jules Verne	143 km	Jules Verne (1828–1905)
</excerpt>
### Rank 4 of 682 — 0.54
<excerpt title="Myths, Symbols and Legends of Solar System Bodies [1st ed.] 978-1-4614- ...">
The Hubble Crater is obviously named after Edwin Hubble (1889–1953), the American astronomer who discovered other galaxies beyond our Milky Way, among other things; NASA’s Hubble Space Telescope is also named after him. There are a few other lunar craters that are named after writers such as the science fiction writers Jules Verne and H. G. Wells, as well as the Chaucer Crater named after the English writer and poet Geoffrey Chaucer (1343–1400), famous for writing The Canterbury Tales. The Dante Crater is named after Danti Alighiieri (1265–1312), an Italian poet famous for his Divine Comedy. There are many other named lunar craters not mentioned in this book. There is something enchanting and magical about our beautiful, lonely Moon that bathes our Earth in a romantic, silvery glow of light reflected from the Sun. The Moon has captured the imagination of so many cultures and peoples. The sight of the Moon’s beautiful face on a clear night never fails to fill people with awe, wonder and inspiration. As our nearest heavenly body and visible with the naked eye, there is much mythology concerning the Moon. The Moon, an almost constant celestial presence and frequently visible in the daytime, has had an enormous influence on China, its people, culture and customs
84
5
Craters, Dragons, Festivals, Gods and Goddesses of Earth’s Moon

and, more recently, on space exploration. In 2007 China launched its first lunar orbiter, Chang’ E1, named after its Moon goddess. Unsurprisingly, a tiny crater on the Moon itself is named Chang Ngo. It seems inevitable that the Chinese will make a manned Moon landing in the near future. On December 14, 2013, China successfully landed an unmanned spacecraft on the Moon’s ancient surface. The robotic rover, which left its landing module the following day, is called Yutu, or “Jade Rabbit.” The name was chosen from an online poll of 3.4 million voters and involves a character from Chinese mythology. The Moon holds some valuable resources, such as silver and a chemical called helium 3, found in lunar soil and which is an efficient nuclear fuel. It is estimated that our satellite contains more than a million tons of helium 3. This isotope would be used in nuclear fusion reactions. Nuclear fusion uses nuclei to generate energy. The advantage of helium 3 over other isotopes is that it does not give off pollution or radioactive waste. It is estimated that 25 tonnes of helium 3 could provide enough energy to power the United States for an entire year! This Moon landing is both scientifically and symbolically important, confirming China’s status as a global superpower as well as involving ancient mythology with the choice of the rover’s name. China also plans to send a manned mission to the Moon by 2025, significantly before the United States returns. In ancient China, the emperor was believed to be divine, the son of heaven itself! He almost had to prove this by being able to predict sky events, which were believed to mirror Earthly happenings. Therefore, emperors employed astronomers who observed sky events and recorded them in great detail. The Chinese astronomers divided up the sky in a seemingly complex but methodical way. First, it was broken up into five palaces, or gong-o, representing a middle region and the four main points of the compass. The central region was believed to include a central image of the emperor himself, cementing his divine status, in addition to some family members. Constellations here include, for example, ‘The Prince.’ In addition to the constellations in the four cardinal directions, 28 lunar mansions or lodges were designated in the sky. Of time using early evening sky objects such as constellations, lunar lodges or mansions.
</excerpt>
### Rank 5 of 682 — 0.46
<excerpt title="40aedbfa...a88e68">
### Validator evidence
|None |Apr 11, 2018 | |15743 |Nemo |Nemo |Charon |44\.00 |\-15.70 |314\.10 |\-13.90 |\-17.60 |316\.10 |311\.90 |Planetocentric, +East, 0 - 360 |Europe |France |Crater, craters |AA |\- |Approved |Apr 11, 2018 |[474] |Captain of the Nautilus, a submarine, in the novels "Twenty Thousand Leagues Under the Sea" (1870) and "The Mysterious Island" (1874) by the French author Jules Verne (1825–1905). The stories recount fantastical undersea travels and explorations. |None |Apr 11, 2018 | |15740 |Pirx |Pirx |Charon |90\.00 |55\.20 |256\.30 |59\.40 |50\.90 |263\.10 |249\.90 |Planetocentric, +East, 0 - 360 |Europe |Poland |Crater, craters |AA |\- |Approved |Apr 11, 2018 |[471] |Spaceship pilot, the main character in a series of fictional stories by the Polish author Stanislaw Lem (1921–2006). He travelled between the Earth, Moon and Mars.

### Validator evidence
|None |Apr 11, 2018 | |15741 |Revati |Revati |Charon |40\.00 |20\.70 |35\.40 |22\.50 |18\.90 |37\.30 |33\.50 |Planetocentric, +East, 0 - 360 |Asia |Hindu |Crater, craters |AA |\- |Approved |Apr 11, 2018 |[472] |Hindu mythological princess, who traveled through time and space in search of a suitor, described in the epic narrative "Mahabharata". |None |Apr 11, 2018 | |15742 |Sadko |Sadko |Charon |28\.00 |\-16.10 |331\.20 |\-14.80 |\-17.30 |332\.50 |329\.70 |Planetocentric, +East, 0 - 360 |Europe |Russia |Crater, craters |AA |\- |Approved |Apr 11, 2018 |[473] |Russian merchant in the medieval epic tale (Bylina), who traveled to the bottom of the sea. |None |Apr 11, 2018 | Download all your search results in one of the follow formats ( need help? ): * CSV (comma separated values) for importing into Excel Return to top usgs-logo USGS Astrogeology Science Center The National Aeronautics and Space Administration (NASA) International Astronomical Union (IAU) The Gazetteer of Planetary Nomenclature website is maintained by the USGS Astrogeology Science Center . This work is performed on behalf of the International Astronomical Union's Working Group for Planetary System Nomenclature and is supported by the National Aeronautics and Space Administration under an Interagency Agreement. Contact Us Administrator Log In
Nomenclature Search Results - Planetary Names
</excerpt>

## Search 5 — query: "Phobos feature name "Jules" 1973 Planetary Names"
### Rank 1 of 5069 — 0.53 (passed on)
<excerpt title="NEEP602 The Nine Planets Glossary - Fusion Technology Institute">
## S
to change directly from a solid to a gas without becoming liquid **sulcus** subparallel furrows and ridges. **sunspot** an area seen as a dark spot on the photosphere of the Sun; sunspots are concentrations of magnetic flux, typically occurring in bipolar clusters or groups; they appear dark because they are cooler than the surrounding photosphere. **superior planets** the planets Mars, Jupiter, Saturn, Uranus, Neptune and Pluto are called superior planets because their orbits are farther from the Sun than Earth's orbit. **synchronous orbit radius** the orbital radius at which the satellite's orbital period is equal to the rotational period of the planet. A synchronous satellite with an orbital inclination of zero (same plane as the planet's equator) stays fixed in the sky from the perspective of an observer on the planet's surface (such orbits are commonly used for communications satellites). **synchronous rotation** said of a satellite if the period of its rotation about its axis is the same as the period of its orbit around its primary. This implies that the satellite always keeps the same hemisphere facing its primary (e.g. the Moon). It also implies that one hemisphere (the leading hemisphere) always faces in the direction of the satellite's motion while the other (trailing) one always faces backward.

## T
**tectonic** deformation forces acting on a planet's crust. **terminator** the dividing line between the illuminated and the unilluminated part of the moon's or a planet's disk. **terra** extensive land mass. **tessera** tile; terrain formed of polygonal pattern **tholus** small domical mountain or hill. **Thomson, William** 1824-1907  aka Lord Kelvin, British physicist who developed the Kelvin scale of temperature supervised the laying of a trans-Atlantic cable. (10k gif) **tidal heating** frictional heating of a satellite's interior due to flexure caused by the gravitational pull of its parent planet and possibly neighboring satellites. **Tombaugh, Clyde** 1906-  American astronomer; discovered Pluto. (4k gif) **Trekkie** a devotee of the science fiction program Star Trek. **Trojan** an object orbiting in the Lagrange points of another (larger) object. This name derives from a generalization of the names of two of the largest asteroids in Jupiter's Lagrange points: 624 Hektor and 911 Agamemmnon. Saturn's satellites Helene, Calypso and Telesto are also sometimes called Trojans.

## U
**umbra** the dark central region of a sunspot. **undae** dunes (literally 'waves').

## V
**vallis** sinuous valley (plural: valles) **Van Allen, James A.** American physicist who discovered the Earth's radiation belts (that now bear his name) with an instrument aboard the first successful American satellite, Explorer 1. **vastitas** widespread lowlands. **Verne, Jules** 1828-1905  French writer who is considered the founder of modern science fiction. His novels include "Journey to the Center of the Earth" and "From the Earth to the Moon". **volatile** As a noun, this refers to substances that are gases at ordinary temperatures. In astronomy it includes hydrogen, helium, water, ammonia, carbon dioxide and methane.

## W
**white dwarf** a whitish star of high surface temperature and low intrinsic brightness with a mass approximately equal to that of a Sun but with a density many times larger.

## X


## Y
**young** When used to describe a planetary **surface** "young" means that the visible features are of relatively recent origin, i.e. that older features have been destroyed (e.g. by erosion or lava flows). Young surfaces exhibit few impact craters and are typically varied and complex. In contrast an "old" surface is one that has changed relatively little over geologic time. The surfaces of Earth and Io are young; the surfaces of Mercury and Callisto are old.

## Z
* * *
</excerpt>
### Rank 2 of 5069 — 0.31
<excerpt title="Catalogue of Minor Planet Names and Discovery Circumstances">
## [PDF page 436]
1969  TB3.  Discovered  1969  Oct.  9  by  B.  A.  Burnasheva  to  the  public  with  his  numerous  b o oks.  (M  41382)  
at  Nauchnyj.  (5224)  Abb e  
Mariya  Romanovna  Kutsak  (1928-1997)  wa s  a  1982  DX3 .  Discovered  1982  Feb.  21  by  F.  B¨orngen  at  
scho olteacher  of  physics  and  astronomy  in  the  city  of  Tautenburg.  
Omsk  for  ab out  40  years.  (M  45336)  Named  in  memory  of  Ernst  Karl  Abb e  (1840-1905),  
(5219)  Zemka  director  of  the  Jena  Observatory  from  1877  to  1900,  
1976  GU3 .  Discovered  1976  Apr.  2  by  N.  S.  Chernykh  known  for  his  fundamental  contributions  to  optics.  
at  Nauchnyj.  These  includes  work  on  microscop es,  the  Abb e  numb er

## [PDF page 437]
(5225)  Loral  449
and  comparators  -  the  last  b eing  very  useful  for(5231)  Verne  
the  detection  of  minor  planets.  Abb e,  a  long-time  1988  JV.  Discovered  1988  May  9  by  C.  S.  Sho emaker  
collab orator  and  friend  of  Carl  Zeiss  {see  planet  and  E.  M.  Sho emaker  and  H.  E.  Holt  at  Palomar.  
(851)},  secured  considerable  ﬁnancial  supp ort  for  the  Named  for  Jules  Verne  (1828-1905),  French  novelist  
University  of  Jena  from  the  Zeiss  foundation.  The  and  playwright.  One  of  the  founding  fathers  of  mo dern  
minor  planet  is  b eing  named  on  the  o ccasion  of  the  science  ﬁction,  he  was  also  the  author  of  numerous  
ﬁrst  meeting  of  the  Astronomische  Gesellschaft  in  the  works  of  mainstream  adventure  ﬁction.  His  b est-known  
{eastern  part  of  the}  reunited  Germany.  (M  20839)  tales  include  From  the  Earth  to  the  Mo on  (1865),  
Abb e  is  also  honored  by  a  lunar  crater.  Twenty  Thousand  Leagues  under  the  Sea  (1870)  and  
Around  the  World  in  Eighty  Days  (1873).  (M  24765)  
(5225)  Loral  The  discoverers  are  great  fans  of  Verne’s  work,  as
</excerpt>
### Rank 3 of 5069 — 0.28
<excerpt title="List of craters in the Solar System">
Swift	12.5°N 1.8°E	1	1973	Jonathan; British writer (1667–1745)	WGPSN  
Voltaire	22°N 3.5°W	1.9	1973	Francios-Marie Arouet; French writer (1694–1778)	WGPSN  
back to top   
Dione (73)edit  
Main article: List of geological features on Dione § Craters  
Crater	Coordinates	Diameter  
(km)	Approval  
Year	Eponym	Ref  
Acestes	50.1°N 116.63°E	108	2008	King of Sicily	WGPSN  
Adrastus	61.66°S 46.57°W	38.5	1982	King of Argos one of the seven against Thebes and the only one to return alive	WGPSN  
Aeneas	25.89°N 46.27°W	161	1982	Hero of the Aeneid. The son of Anchises and Venus and a member of the royal family of Troy	WGPSN  
Alcander	52.89°S 64.51°E	120	2011	A Trojan defending Aeneas’ camp against the Rutulians killed by Turnus	WGPSN  
Allecto	7.73°S 135.44°E	106	2008	One of the Furies	WGPSN  
Amastrus	9.96°S 122.97°E	62.4	2008	A Trojan victim of Camilla	WGPSN  
Amata	5.17°N 80.19°E	76	1982	Mother of Lavinia (wife of Aeneas)	WGPSN  
Amycus	37.52°S 88.62°W	27.3	2008	A Trojan comrade of Aeneas	WGPSN
</excerpt>
### Rank 4 of 5069 — 0.24
<excerpt title="Which planets have 2 moons?">
# Which planets have 2 moons?
Lives in The Universe · Author has 187 answers and 495.8K answer views
·8y
Originally Answered: Which planet has two moons? ·
Mars has two, Phobos and Deimos. Jupiter, Saturn, Uranus, and Neptune all have more than two.
Upvote ·
9 2
Paul Czerner
Studied Physics · Author has 56 answers and 59.2K answer views
·3y
Originally Answered: Which planet has two Moons? ·
Any planet that has 2 or more moons has 2 moons (if you have 3 moons, you also have 2 moons, it’s incuded in the set). So out of 8 planets, only the 3 innermost ones have less than 2 moons, so 5 planets have 2 moons: Mars, Jupiter, Saturn, Uranus, Neptune.
Upvote ·
9 3
9 1
Jonathan Johnson
I've looked at the stars before · Author has 3.7K answers and 21M answer views
·8y
Originally Answered: What planet has two moons? ·
What planet has two moons?
Thinking back to my grade school days, I think it was “Janet the Planet.”
She was quite large. Kids can be so mean. That was before political correctness was discovered.
Upvote ·
Related questions
Which planets in our solar system have moons?
Which planets are the gas planets?
Why do some planets have multiple moons?
Do any two planets have the same type of moons around them?
How come all the other planets have names for their moons, but we just call ours 'The Moon'?
Do all planets’ moons come from their planet?
Why do moons sometimes leave their planets?
What is the planet that has eight moons?
Which planet has the most moons, and how many does it have?
Which planet has got 9 moons?
Is there any planet below Earth?
Why is the Moon not considered a planet?
Do bigger planets have more moons?
Do all moons have planets?
Is it possible for all planets to have different orbits?
What is the hottest planet in our Solar System?
Which moon is bigger than a planet?
Is the moon or the sun a planet?
</excerpt>
### Rank 5 of 5069 — 0.22
<excerpt title="Which planets have 2 moons?">
# Which planets have 2 moons?
All related (48)
Sort
Recommended
Krishna Gupta
Worked at Vodafone Idea Limited (2019–2022)
·2y
Several planets in our solar system have two moons:
1.   Mars: Phobos and Deimos  
2.   Uranus: Titania and Oberon
These are the only two planets with known moons in pairs.
Upvote ·
Promoted by Zafar Mirzo
What shape is the universe?
Zafar Mirzo
Sun
What shape is the Universe? From the Big Bang to the Multiverse: a short guide Fireworks or dough Almost every one of us has asked at least once: if the Universe came into being in the Big Bang, what was it like at the beginning, and what shape does it have now? Our intuition keeps producing the same p…
(more)
Upvote ·
99 87
9 7
9 1
Paul Morley
Former Graphic Designer/Printer (2011–2016) · Author has 3K answers and 14.3M answer views
·8y
Originally Answered: Which planets have two moons? ·
As far as I know; Mars is the only planet in our solar system with exactly two moons. Jupiter has 67, Saturn rings in at 62, Uranus has 27 clingers, Neptune isn’t ashamed with 14 and coming in last is Earth with just one.
Upvote ·
9 4
Related questions
More answers below
Which planet has two Moons? 25K views
Can two planets share a satellite/moon? 2.7K views
Which planet or star is closest to the moon and visible from Earth? 132.8K views
Is the Moon a planet or a star? 209.6K views
What planet is currently visible next to the Moon? 18.1K views
Ronnie Grondin
I read a lot · Author has 714 answers and 1.9M answer views
·8y
Originally Answered: Which planet has two Moons? ·

# Which planets have 2 moons?
Ignoring other planets with +/- 2 moons, Mars would be the only planet that falls into this category. Mars has two moons called Phobos and Deimos Phobos and Deimos Size and Distance Comparison Phobos The Martian moon Phobos orbits only a few thousand miles above the Red Planet's surface. Its proximity to its planet is one of the reasons astronomers were unable to see the satellite until the late 19th century. In fact, the moon is getting closer to Mars over the centuries, and eventually will either break up or be pulled into the Martian surface. Deimos Deimos is the smaller of the two Martian moons…
(more)
Ignoring other planets with +/- 2 moons, Mars would be the only planet that falls into this category.
Mars has two moons called Phobos and Deimos
Phobos and Deimos Size and Distance Comparison
Phobos
> The Martian moon Phobos orbits only a few thousand miles above the Red Planet's surface. Its proximity to its planet is one of the reasons astronomers were unable to see the satellite until the late 19th century. In fact, the moon is getting closer to Mars over the centuries, and eventually will either break up or be pulled into the Martian surface.  
>   
>   
>   
> [[1]](https://www.quora.com/Which-planets-have-2-moons#uMSwX)
Deimos
> Deimos is the smaller of the two Martian moons and is less irregular in shape. The largest crater on Deimos is approximately 2.3 km in diameter, 1/5 the size of the largest crater on Phobos. Although both moons are heavily cratered, Deimos has a smoother appearance caused by the partial filling of some of its craters. When impacted, dust and debris will leave the surface of the moon because it doesn't have enough gravitational pull to retain the ejecta. However, the gravity from Mars will keep a ring of this debris around the planet in approximately the same region that the moon orbits. As the moon revolves, the debris is redeposited as a dusty layer on its surface.  
>   
>   
>   
> [[2]](https://www.quora.com/Which-planets-have-2-moons#iPyKK)
Enjoy!
Footnotes
</excerpt>

## Search 6 — query: ""approved 1973" "planetarynames" "crater""
### Rank 1 of 100 — 0.54 (passed on)
<excerpt title="e82aec54...23c6ad">
### Task b3e2e0f9
Diameters are the Search Results values specified in the question. | Feature | Body | Woman | Earliest Nobel year | Approval year | Interval, years | Diameter, km | Sources | |---|---|---|---:|---:|---:|---:|---| | Mistral | Mercury | Gabriela Mistral | 1945 | 1976 | 31 | 102.00 | [[1]][[7]][[12]] | | Cori | Moon | Gerty Cori | 1947 | 1979 | 32 | 67.22 | [[1]][[2]][[5]][[9]] | | Cori | Venus | Gerty Cori | 1947 | 1991 | 44 | 56.10 | [[1]][[6]] | | Balch | Venus | Emily Greene Balch | 1946 | 1994 | 48 | 40.00 | [[1]][[6]] | | Buck | Venus | Pearl S.

### Task b3e2e0f9
Buck | 1938 | 1991 | 53 | 21.80 | [[1]][[6]] | | Joliot-Curie | Venus | Irène Joliot-Curie | 1935 | 1991 | 56 | 91.10 | [[1]][[6]] | | Undset | Venus | Sigrid Undset | 1928 | 1985 | 57 | 20.00 | [[1]][[6]] | | Sklodowska | Moon | Marie Curie | 1903 | 1961 | 58 | 125.55 | [[1]][[3]][[5]][[10]] | | Deledda | Venus | Grazia Deledda | 1926 | 1985 | 59 | 32.00 | [[1]][[4]][[6]] | | Addams | Venus | Jane Addams | 1931 | 1994 | 63 | 87.00 | [[1]][[6]] | | Sklodowska | Mars | Marie Curie | 1903 | 1973 | 70 | 109.72 | [[1]][[3]][[8]][[13]] | | Lagerlöf | Venus | Selma Lagerlöf | 1909 | 1985 | 76 | 56.00 | [[1]][[6]] | | von Suttner | Venus | Bertha von Suttner | 1905 | 1994 | 89 | 24.00 | [[1]][[6]] | Several plausible extra entries fail the conditions. **Curie on the Moon** and **Curie on Mars** identify Pierre Curie, so neither is an entry for Marie. **Joliot on the Moon** identifies Frédéric Joliot-Curie, so it is not an entry for Irène. The lunar **[Undest]** identifies Sigrid, but its record explicitly says the name was never approved by the IAU. It is excluded despite its namesake.
</excerpt>
### Rank 2 of 100 — 0.53
<excerpt title="e82aec54...23c6ad">
### Task b3e2e0f9
Buck | 1938 | 1991 | 53 | 21.80 | [[1]][[6]] | | Joliot-Curie | Venus | Irène Joliot-Curie | 1935 | 1991 | 56 | 91.10 | [[1]][[6]] | | Undset | Venus | Sigrid Undset | 1928 | 1985 | 57 | 20.00 | [[1]][[6]] | | Sklodowska | Moon | Marie Curie | 1903 | 1961 | 58 | 125.55 | [[1]][[3]][[5]][[10]] | | Deledda | Venus | Grazia Deledda | 1926 | 1985 | 59 | 32.00 | [[1]][[4]][[6]] | | Addams | Venus | Jane Addams | 1931 | 1994 | 63 | 87.00 | [[1]][[6]] | | Sklodowska | Mars | Marie Curie | 1903 | 1973 | 70 | 109.72 | [[1]][[3]][[8]][[13]] | | Lagerlöf | Venus | Selma Lagerlöf | 1909 | 1985 | 76 | 56.00 | [[1]][[6]] | | von Suttner | Venus | Bertha von Suttner | 1905 | 1994 | 89 | 24.00 | [[1]][[6]] | Several plausible extra entries fail the conditions. **Curie on the Moon** and **Curie on Mars** identify Pierre Curie, so neither is an entry for Marie. **Joliot on the Moon** identifies Frédéric Joliot-Curie, so it is not an entry for Irène. The lunar **[Undest]** identifies Sigrid, but its record explicitly says the name was never approved by the IAU. It is excluded despite its namesake.

### Task b3e2e0f9
[[5]][[8]][[11]][[14]] Generic given names also do not establish a commemorated laureate under the question's Origin rule. Satellite entries are excluded by Feature Type: for example, Sklodowska A actually identifies Marie in its Origin, but its Feature Type is **Satellite Feature**, rather than **Crater, craters**. [[15]] The distinction between a designated prize year and receipt date affects Deledda: her facts page calls it the **1926** prize and states that she received it in **1927**. Her interval is therefore 1985−1926 = 59 years. [[4]][[6]] ## Original mean and diameter gap The thirteen intervals sum to 31 + 32 + 44 + 48 + 53 + 56 + 57 + 58 + 59 + 63 + 70 + 76 + 89 = **736 years**. Thus the original mean is **736/13 = 56.6153846… years**. In the complete ordered population, the closest interval strictly below it is 56, belonging to Joliot-Curie on Venus, and the closest strictly above it is 57, belonging to Undset on Venus. Their Search Results diameters are 91.10 km and 20.00 km, respectively. [[6]] Therefore the original diameter gap is **|91.10 − 20.00| = 71.10 km**. ## Establishing the greatest attainable change There are eleven represented women, so the question considers **11×10/2 = 55 unordered pairs**. An omission removes all entries for either woman; the two entries each for Marie Curie and Gerty Cori must be removed together. [[2]][[3]][[5]][[6]][[8]] The largest eligible diameter is the lunar Sklodowska's 125.55 km and the smallest is Undset's 20.00 km. Consequently, no remaining population can have a diameter gap greater than **105.55 km**.
</excerpt>
### Rank 3 of 100 — 0.53
<excerpt title="6a3b4633...526b7e">
### Task 096b419c
<name>Schmidt</name><ExtendedData><SchemaData schemaUrl="#MOON_nomenclature_center_pts"><SimpleData name="clean_name">Schmidt</SimpleData><SimpleData name="approvaldt">1935/01/01 00:00:00</SimpleData><SimpleData name="origin">Johann Friedrich Julius; German astronomer (1825-1884); Bernhard Voldemar; German optician (1879-1935); Otto Yulyevich; Soviet astronomer (1891-1956).</SimpleData><SimpleData name="diameter">11.130397</SimpleData><SimpleData name="center_lon">18.7806</SimpleData><SimpleData name="center_lat">0.9564</SimpleData><SimpleData name="type">Crater, craters</SimpleData><SimpleData name="code">AA</SimpleData><SimpleData name="approval">Adopted by IAU</SimpleData><SimpleData name="min_lon">18.5971</SimpleData><SimpleData name="max_lon">18.9642</SimpleData><SimpleData name="min_lat">0.7728</SimpleData><SimpleData name="max_lat">1.1399</SimpleData><SimpleData name="ethnicity">Germany</SimpleData><SimpleData name="continent">Europe</SimpleData><SimpleData name="quad_name">Julius Caesar</SimpleData><SimpleData name="quad_code">LAC-60</SimpleData><SimpleData name="link">http://planetarynames.wr.usgs.gov/Feature/5374</SimpleData></SchemaData></ExtendedData><Point><coordinates>18.7806,0.9564</coordinates></Point></Placemark>
USGS Mars nomenclature KML export; offsets refer to the enclosed MARS_nomenclature_center_pts.kml

### Task 096b419c
<name>Cassini</name><ExtendedData><SchemaData schemaUrl="#MARS_nomenclature_center_pts"><SimpleData name="clean_name">Cassini</SimpleData><SimpleData name="approvaldt">1973/01/01 00:00:00</SimpleData><SimpleData name="origin">Giovanni; Italian astronomer (1625-1712).</SimpleData><SimpleData name="diameter">408.23099</SimpleData><SimpleData name="center_lon">32.1103</SimpleData><SimpleData name="center_lat">23.3513</SimpleData><SimpleData name="type">Crater, craters</SimpleData><SimpleData name="code">AA</SimpleData><SimpleData name="approval">Adopted by IAU</SimpleData><SimpleData name="min_lon">28.3593</SimpleData><SimpleData name="max_lon">35.8625</SimpleData><SimpleData name="min_lat">19.9076</SimpleData><SimpleData name="max_lat">26.7958</SimpleData><SimpleData name="ethnicity">Italy</SimpleData><SimpleData name="continent">Europe</SimpleData><SimpleData name="quad_name">Arabia</SimpleData><SimpleData name="quad_code">mc12</SimpleData><SimpleData name="link">http://planetarynames.wr.usgs.gov/Feature/1046</SimpleData></SchemaData></ExtendedData><Point><coordinates>32.1103,23.3513</coordinates></Point></Placemark>
</excerpt>
### Rank 4 of 100 — 0.49
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
### Rank 5 of 100 — 0.49
<excerpt title="6a3b4633...526b7e">
### Task 096b419c
Johann Heinrich; German astronomer, mathematician, physicist (1728-1777); also for Gérard; French physicist (1930-2008).
USGS Gazetteer — Lambert (Mars), feature 3254
<th>Feature Name</th><td> Lambert </td>
<th>Target</th><td id="target-name">Mars</td>
<th>Feature Type</th><td><span title="A circular depression">Crater, craters</span></td>
<th>Approval Status</th><td>Adopted by IAU</td>
<th>Approval Date</th><td> 1973 </td>
Johann H.; German physicist (1728-1777).
USGS Moon nomenclature KML export; offsets refer to the enclosed MOON_nomenclature_center_pts.kml

### Task 096b419c
<name>Cassini</name><ExtendedData><SchemaData schemaUrl="#MOON_nomenclature_center_pts"><SimpleData name="clean_name">Cassini</SimpleData><SimpleData name="approvaldt">1935/01/01 00:00:00</SimpleData><SimpleData name="origin">Giovanni Domenico; Italian-French astronomer (1625-1712); Jacques; French astronomer (1677-1756).</SimpleData><SimpleData name="diameter">56.876614</SimpleData><SimpleData name="center_lon">4.6437</SimpleData><SimpleData name="center_lat">40.2503</SimpleData><SimpleData name="type">Crater, craters</SimpleData><SimpleData name="code">AA</SimpleData><SimpleData name="approval">Adopted by IAU</SimpleData><SimpleData name="min_lon">3.4358</SimpleData><SimpleData name="max_lon">5.8496</SimpleData><SimpleData name="min_lat">39.3553</SimpleData><SimpleData name="max_lat">41.1452</SimpleData><SimpleData name="ethnicity">Italy</SimpleData><SimpleData name="continent">Europe</SimpleData><SimpleData name="quad_name">Cassini</SimpleData><SimpleData name="quad_code">LAC-25</SimpleData><SimpleData name="link">http://planetarynames.wr.usgs.gov/Feature/1045</SimpleData></SchemaData></ExtendedData><Point><coordinates>4.6437,40.2503</coordinates></Point></Placemark>
</excerpt>

## Search 7 — query: "site:planetarynames.wr.usgs.gov 1973 Moon crater fiction writer"
### Rank 1 of 80 — 0.16 (passed on)
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
### Rank 2 of 80 — 0.09
<excerpt title="Categories (Themes) for Naming Features on Planets and Satellites">
##  Mars and Martian Satellites
###  Mars
Albedo Features Names from classical mythology assigned by Schiaparelli and Antoniadi  
Large craters (approximately 50 km and larger)Scientists, especially those who have contributed significantly to the study of Mars; writers and others who have contributed to the lore of Mars  
Small craters (approximately 50 km and smaller)Small towns and villages of the world with populations of approximately 100,000 or less. This category is simply a large source of crater names. No commemoration of specific towns or villages is intended.  
Smaller features within a larger named feature The normal naming convention shall be suspended and instead their names shall be chosen so that they bear a mnemonic relationship to the given name of the larger feature, followed by the appropriate descriptor term (crater, cavus, patera, etc.).  
Large valles Name for Mars/star in various languages  
Small valles Classical or modern names of rivers  
Other features From a nearby named albedo feature on Schiaparelli or Antoniadi maps. If no nearby albedo feature name is available, then from a nearby named crater.

##  Mars and Martian Satellites
###  Deimos
Authors who wrote about martian satellites

##  Mars and Martian Satellites
###  Phobos
Scientists involved with the discovery, dynamics, or properties of the martian satellites, and people and places from Jonathan Swift's "Gulliver's Travels"

##  Satellites of Jupiter
###  Amalthea
People and places associated with the Amalthea myth

##  Satellites of Jupiter
###  Thebe
People and places associated with the Thebe myth

##  Satellites of Jupiter
###  Io
Active eruptive centers Fire, sun, thunder, and volcano gods and heroes  
Catenae Sun gods  
Fluctūs Name derived from nearby named feature, or fire, sun, thunder, volcano gods, goddesses and heroes, or mythical blacksmiths  
Mensae People associated with Io myth, people from Dante's Inferno, or derived from a nearby named feature  
Montes Places associated with Io myth, places from Dante's Inferno, or derived from a nearby named feature  
Paterae Fire, sun, thunder, volcano gods, heroes, goddesses, mythical blacksmiths, including names from the associated eruptive center  
Plana Places associated with Io myth, places from Dante's Inferno, or derived from a nearby named feature  
Regiones Places associated with Io myth, places from Dante's Inferno, or derived from a nearby named feature  
Tholi People associated with Io myth, people from Dante's Inferno, or derived from a nearby named feature  
Valles Name derived from nearby named feature

##  Satellites of Jupiter
###  Europa
Chaos and cavi Places associated with Celtic myths  
Craters and mensae Celtic gods and heroes  
Flexūs Places associated with the Europa myth, or Celtic stone rows  
Large ringed features Celtic stone circles  
Lineae and fossae People associated with the Europa myth, or Celtic stone rows  
Maculae Places associated with the Europa myth  
Regiones Places associated with Celtic myths

##  Satellites of Jupiter
###  Ganymede
Catenae Gods and heroes of ancient Fertile Crescent people  
Craters Gods and heroes of ancient Fertile Crescent people  
Faculae Places associated with Egyptian myths  
Fossae Gods (or principals) of ancient Fertile Crescent people  
Paterae Dry wadis (channels) of the Fertile Crescent region  
Regiones Astronomers who discovered Jovian satellites  
Sulci Places associated with myths of ancient people

##  Satellites of Jupiter
###  Callisto
Names are drawn from myths and folktales of cultures of the Far North such as Norse, Chukchi, Inuit, Sami, etc.
Catenae Rivers, valleys, and ravines from myths and folktales of cultures of the Far North  
Craters Characters from myths and folktales of cultures of the Far North  
Faculae Gods and characters of frost, snow, cold, and sleet from myths and folktales of cultures of the Far North  
Large ringed features Places (other than rivers, valleys and ravines) from myths and folktales of cultures of the Far North
</excerpt>
### Rank 3 of 80 — 0.09
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
### Rank 4 of 80 — 0.09
<excerpt title="Nomenclature Search Results">
Argas	Mars	3.55	23.33	309.83	Crater, craters	1988	Town in Russia.  
Arica	Mars	15.77	-23.80	110.24	Crater, craters	1991	Town in Colombia.  
Arima	Mars	53.59	-15.84	296.32	Crater, craters	Feb 22, 2012	Town in Trinidad and Tobago.  
Arkhangelsky	Mars	116.83	-41.09	335.21	Crater, craters	1979	A.D.; Russian geologist.  
Arrhenius	Mars	122.72	-40.04	122.71	Crater, craters	1973	Svante; Swedish physical chemist (1859-1927).  
Arta	Mars	3.96	21.38	305.71	Crater, craters	1988	Town in Russia.  
Artik	Mars	5.36	-34.80	130.98	Crater, craters	Aug 30, 2013	Town in Armenia.  
Arvi	Mars	7.00	-39.34	202.72	Crater, craters	Mar 23, 2022	Town in India.  
Asau	Mars	25.05	-3.63	154.68	Crater, craters	Jun 03, 2013	Village in Tuvalu.  
Asimov	Mars	80.82	-46.97	4.93	Crater, craters	May 04, 2009	Isaac; American biochemist and writer (1920-1992).  

Aspen	Mars	18.48	-21.39	336.85	Crater, craters	1976	Town in Colorado, USA.  
Auce	Mars	37.01	-27.17	80.14	Crater, craters	Oct 12, 2014	Town in Latvia.  
Auki	Mars	40.00	-15.76	96.87	Crater, craters	Aug 14, 2015	Town in the Solomon Islands.  
Avan	Mars	3.30	-10.97	290.23	Crater, craters	Nov 15, 2016	Village in Armenia.  
Avarua	Mars	49.99	-35.93	109.66	Crater, craters	Jun 21, 2010	Town in the Cook Islands.  
Aveiro	Mars	9.11	21.28	281.03	Crater, craters	1985	Town in Portugal.  
Avire	Mars	6.85	-40.82	200.24	Crater, craters	Apr 16, 2008	Town in the Republic of Vanuatu.  
  1 - 50 of 1250 results
Download all your search results in one of the follow formats (need help?):
CSV (comma separated values) for importing into Excel
</excerpt>
### Rank 5 of 80 — 0.08
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

## Search 8 — query: "Moon crater 1973 literary 19th century fiction""
### Rank 1 of 52 — 0.43 (passed on)
<excerpt title="SFE: Moon">
Several lunar craters and other features have been named for sf creators with entries in this encyclopedia: those honoured include Cyrano de Bergerac, Camille Flammarion, George Gamow, Hugo Gernsback, J B S Haldane, Hermann Oberth, Vladimir A Obruchev, Leo Szilárd, Konstantin Tsiolkovsky, Jules Verne, Wernher von Braun, H G Wells and Norbert Wiener.
Early Moon romances are collected in _The Man in the Moone: An Anthology of Antique Science Fiction_ (anth **1971**) edited by Faith K Pizor and T Allan Comp, and in _News from the Moon: Nine French Proto-Science Fiction Stories from 1768 to 1902_ (anth **2007**) translated and edited by Brian Stableford. Theme anthologies with more recent coverage include _Men on the Moon_ (anth **1958** dos; exp **1969**) edited by Donald A Wollheim and _Great Science Fiction Stories about the Moon_ (anth **1967**) edited by T E Dikty [for these and others see "further reading" below]. [BS/DRL]
**see also:**_The_Gene Machine; Hollow Earth; Lunar Lander.
**further reading**

*   Donald A Wollheim, editor. _Men on the Moon_ (New York: Ace Books, **1958**) anth: dos: pb/Ed [Emshwiller]   
    *   Donald A Wollheim, editor. _Men on the Moon_ (New York: Ace Books, **1969**) anth: exp of the above: pb/Gray [Morrow]

*   T E Dikty, editor. _Great Science Fiction Stories about the Moon_ (New York: Frederick Fell, **1967**) [anth: hb/]  
*   Hal Clement, editor. _First Flights to the Moon_ (Garden City, New York: Doubleday and Company, **1970**) [anth: hb/Roger Zimmerman]  
*   Faith K Pizor and T Allan Comp, editors. _The Man in the Moone: An Anthology of Antique Science Fiction_ (New York: Praeger Publishers, **1971**) anth: [Proto SF: hb/]  
*   Gardner Dozois and Sheila Williams, editors. _Isaac Asimov's Moons_ (New York: Ace Books, **1997**) with [anth: **Asimov's Anthologies**: pb/Den Beauvais]  
*   Brian Stableford, editor. _News from the Moon: Nine French Proto-Science Fiction Stories from 1768 to 1902_ (Encino, California: Hollywood Comics/Black Coat Press, **2007**) [anth: assembled from various sources: trans Stableford: **French Proto-Science Fiction**: pb/Gil Formosa]  
*   Matthew Shindell, editor. _Lunar: A History of the Moon in Myths, Maps, and Matter_ (Chicago, Illinois: The University of Chicago Press, **2024**) [nonfiction: illus/hb/various]
**links**
*   The Moon in Science Fiction  
*   Picture Gallery
**previous versions of this entry**
*   Internet Archive
</excerpt>
### Rank 2 of 52 — 0.43
<excerpt title="SFE: Moon">
Besides the already-cited Destination Moon and 2001: A Space Odyssey, a number of other movies feature lunar voyages and/or settings. These include the first sf film ever made, Georges Méliès's _Le_Voyage dans la Lune (_1902_); Fritz Lang's _Die_Frau im Mond (_1929_; vt _By Rocket to the Moon_; vt _The Girl in the Moon_; vt _The Woman in the Moon_); the Russian _Kosmicheskiy Reys: Fantasticheskaya Novella_ (_1935_; vt _The Cosmic Voyage_) (see Spacesuit Films); Rocketship X-M (_1950_; vt _Expedition Moon_), whose expedition is in fact diverted to Mars; the film serial Radar Men from the Moon (_1951_); Cat-Women of the Moon (_1953_; vt _Rocket to the Moon_); the Russian Space DocumentaryDoroga k Zvezdam (_1957_; vt _Road to the Stars_); Missile to the Moon (_1958_); Totò nella Luna (_1958_; vt _Totò in the Moon_); Uchū Daisensō (_1959_; vt _Battle in Outer Space_; vt _The World of Space_); Rehla ilal Kamar (_1959_; vt _Journey to the Moon_); 12 to the Moon (_1960_); Conquistador de la Luna (_1960_; vt _The Astronauts_); Nude on the Moon (_1961_); _The_Crawling Hand (_1963_); Luna (_1965_; vt _The Moon_), another Russian space documentary; Countdown (_1967_); the spoof documentary Alternative 3 (_1977_); and Moon (_2009_). A plot to steal the Moon features in Despicable Me (_2010_). Television series of relevance are Men into Space (_1959-1960_), Moonbase 3 (_1973_) and Space: 1999 (_1975-1977_), the last having the unlikely premise of a runaway Moon careering through the galaxy to encounter new worlds and Aliens roughly as often as in Star Trek.

Several lunar craters and other features have been named for sf creators with entries in this encyclopedia: those honoured include Cyrano de Bergerac, Camille Flammarion, George Gamow, Hugo Gernsback, J B S Haldane, Hermann Oberth, Vladimir A Obruchev, Leo Szilárd, Konstantin Tsiolkovsky, Jules Verne, Wernher von Braun, H G Wells and Norbert Wiener.
Early Moon romances are collected in _The Man in the Moone: An Anthology of Antique Science Fiction_ (anth **1971**) edited by Faith K Pizor and T Allan Comp, and in _News from the Moon: Nine French Proto-Science Fiction Stories from 1768 to 1902_ (anth **2007**) translated and edited by Brian Stableford. Theme anthologies with more recent coverage include _Men on the Moon_ (anth **1958** dos; exp **1969**) edited by Donald A Wollheim and _Great Science Fiction Stories about the Moon_ (anth **1967**) edited by T E Dikty [for these and others see "further reading" below]. [BS/DRL]
**see also:**_The_Gene Machine; Hollow Earth; Lunar Lander.
**further reading**
</excerpt>
### Rank 3 of 52 — 0.32
<excerpt title="Literary journeys to the Moon: The fantasies that preceded Apollo 11">
#### Fiction to defend heliocentrism: from Kepler to Cyrano
Wilkins did not think it was impossible for a man to be propelled by wings attached to his body, by a large trained bird, or by a flying chariot which a man could move using a mechanism. And he quoted Godwin’s book, which in his opinion set forth a pleasant and highly constructed fantasy concerning a journey into that other world (Wilkins, 1638/2005, p. 120).
The seventeenth century would not end without yet another trip to the Moon. This one was narrated by the Frenchman Savinien de Cyrano de Bergerac (1619–1655) in _L’Autre monde ou les états et empires de la Lune_ (“The other world: Comical history of the States and Empires of the Moon”). The book was published posthumously in 1657, in a revised version edited by one of his friends – the original full version did not emerge until 1921.
The method of travel on this occasion was even more far-fetched: powered by rockets and with beef marrow smeared on his body – which, according to him, the Moon had a habit of sucking. Cyrano’s aim was, on the one hand, to provide social criticism and to question many of the customs of his time. But what interests us most here is that he used the story to defend Copernicus’s heliocentric system.
Once again, the change of perspective makes it possible to refute Aristotle’s ideas, who «did without doubt accommodate Principles to his Philosophy» and not the other way around (De Bergerac, 1657/1999). The author maintains that the laws of physics are the same here and on the Moon and that the stars we see are other suns with their own planets. In short, that we do not live in a singularity, but in just one of the inhabited places of the universe.

#### Enter technology
In 1835, the North American author Edgar Allan Poe (1809–1849) published a text in the _Southern Literary Messenger_ titled «The unparalleled adventure of one Hans Pfaall». A manuscript read in the Dutch city of Rotterdam describes the experiences of the protagonist on the Moon. He reached the Moon with a balloon and during the journey he was able to breathe thanks to an invention of his that turns vacuum into air. Pfaall fled because he was wanted for several murders on Earth.
One of the authors who knew and admired Poe’s works was Jules Verne (1828–1905), who had read them in the translation by the poet and essayist Charles Baudelaire (1821–1867). In April 1864, Verne published four articles on Poe in _Le Musée des Familles_. The third one discussed Hans Pfaall’s trip. He stated: «it is wonderful, full of unexpected comments, of singular observations» (Verne, 1864). But before he did, he spent a few paragraphs criticising the lack of scientific rigour. Thus, he said that in the narrative «the most elementary laws of physics and mechanics are fearlessly transgressed».
> «**With Verne, the aim is not to spread heliocentric theories, but to disseminate science based on exciting and credible adventures**»
All this proves that Verne believed scientific rigour and plausibility to be essential elements in these works of fiction. That is why, when he published _From the Earth to the Moon_ in 1865, not only did he base the novel on the most cutting-edge science of the time, which he knew well thanks to numerous readings, he also asked his cousin Henri Garcet (1815–1871), a professor of mathematics, to make several calculations to lend maximum scientific credibility to his book.
</excerpt>
### Rank 4 of 52 — 0.25
<excerpt title="Getting to the Moon: How Science Fiction Became Reality">
### by Brian Clegg
##### Getting to the Moon
Surprisingly, though, the most scientific means of transport used to reach the Moon in this period came from Cyrano de Bergerac. We think of Cyrano as a fictional character because of the eponymous play from the end of the nineteenth century by French writer Edmond Rostand, but de Bergerac was a real seventeenth century playwright.
_“Houghton STC 11943.5 – The Man in the Moone, title” by Francis Godwin (author) – Houghton Library, Harvard University Houghton Library at Harvard.
Image is in the public domain via Check this for reference_
In his first person novel L’Autre Monde: ou les États et Empires de la Lune (The Other World: or the States and Empires of the Moon), Cyrano’s initial attempt at getting off the Earth involved flawed scientific thinking. He noted that the Sun made dew disappear, “drawing the fluid” off the surface. So, he surmised, a collection of bottles containing dew, attached to the astronaut with strings, should lift him into space. When the bottles didn’t work, a group of soldiers attached fireworks to Cyrano’s contraption, blasting him off using rocket power. Admittedly by luck, Cyrano had hit on the first vaguely realistic technological approach.
Plenty of other stories written over the next couple of centuries made use of the Moon as a backdrop to play with the possibilities of new social orders (or to mock existing ones), but the turning point from fantasy to science fiction was the arrival of the twin titans Jules Verne and H. G. Wells. Neither made use of realistic science in their respective books – but they brought the theme into the front rank of popular fiction. Within another 30 years, the science in space travel fiction was converging on reality.
Since our first true voyage to the Moon it has become a less popular destination in fiction. Yet that’s a shame. Every moonlit night we are presented with a reminder that we still haven’t truly conquered our nearest neighbor. The Moon has allure still as a destination for fiction and reality alike.
* * *

### by Brian Clegg
##### Getting to the Moon
BRIAN CLEGG is the author of Ten Billion Tomorrows: How Science Fiction Technology Became Reality and Shapes the Future. He holds a physics degree from Cambridge and has written regular columns, features, and reviews for numerous magazines. He lives in Wiltshire, England, with his wife and two children.
</excerpt>
### Rank 5 of 52 — 0.25
<excerpt title="Literary journeys to the Moon: The fantasies that preceded Apollo 11">
#### Enter technology
In 1835, the North American author Edgar Allan Poe (1809–1849) published a text in the _Southern Literary Messenger_ titled «The unparalleled adventure of one Hans Pfaall». A manuscript read in the Dutch city of Rotterdam describes the experiences of the protagonist on the Moon. He reached the Moon with a balloon and during the journey he was able to breathe thanks to an invention of his that turns vacuum into air. Pfaall fled because he was wanted for several murders on Earth.
One of the authors who knew and admired Poe’s works was Jules Verne (1828–1905), who had read them in the translation by the poet and essayist Charles Baudelaire (1821–1867). In April 1864, Verne published four articles on Poe in _Le Musée des Familles_. The third one discussed Hans Pfaall’s trip. He stated: «it is wonderful, full of unexpected comments, of singular observations» (Verne, 1864). But before he did, he spent a few paragraphs criticising the lack of scientific rigour. Thus, he said that in the narrative «the most elementary laws of physics and mechanics are fearlessly transgressed».
> «**With Verne, the aim is not to spread heliocentric theories, but to disseminate science based on exciting and credible adventures**»
All this proves that Verne believed scientific rigour and plausibility to be essential elements in these works of fiction. That is why, when he published _From the Earth to the Moon_ in 1865, not only did he base the novel on the most cutting-edge science of the time, which he knew well thanks to numerous readings, he also asked his cousin Henri Garcet (1815–1871), a professor of mathematics, to make several calculations to lend maximum scientific credibility to his book.

#### Enter technology
The novel tells the story of Impey Barbicane, president of the Baltimore Gun Club, who travels to the Moon with two other colleagues. They travel in an aluminium projectile launched from a large cannon. They leave from Florida because Barbicane is looking for the most vertical takeoff possible, which is why he sets the cannon close to the equator. Verne says that the necessary escape velocity is 11.2 km/s, a correct calculation if we disregard the resistance caused by air friction (Verne, 1865/2011). Other calculations are very plausible, but the work contains errors as well (Navarro, 2005, pp. 85–102). For instance, the three travellers wear a common suit, tie, and hat, which would not protect them from the force of acceleration. They carry two dogs and when one of them dies they just open the hatch and throw it out, which would have suctioned all the passengers into the void outside the ship.
The novel ends with the ship near the Moon, but without having reached its goal. The adventure continues in _Around the Moon_ (Verne, 1869/2005). After making several observations, the travellers return to Earth. Thus, contrary to popular belief, Verne’s characters never set foot on the Moon.
![Image 3: il·lustració de la terra a la lluna verne](blob:http://localhost/a93a0912c56bccf104ec4fdab5f0960f)
In 1865, the French author Jules Verne published _From the Earth to the Moon_, undoubtedly one of the reference works of science fiction focused on space travel. Verne believed scientific rigour and plausibility to be essential elements in these works of fiction. In the picture, one of the illustrations created by the French artist Henri de Montaut to accompany the novel, showing the projectile that the characters use to travel to the Moon. / New York Public Library / Archive.org
With Verne, the aim is not to spread heliocentric theories, which were already well established in the nineteenth century, but to disseminate science based on exciting and credible adventures. Verne resented the frivolous way in which authors violated the laws of physics.
</excerpt>

## Search 9 — query: "Cyrano lunar crater 1973 planetnames"
### Rank 1 of 46 — 0.84 (passed on)
<excerpt title="Cyrano - The Moon">
From The Moon
Jump to: navigation, search
*   1 Cyrano  
    *   1.1 Images  
    *   1.2 Maps  
    *   1.3 Description  
    *   1.4 Description: Wikipedia  
    *   1.5 Additional Information  
    *   1.6 Nomenclature  
    *   1.7 LPOD Articles  
    *   1.8 Bibliography  
    *   1.9 Cyrano De Bergerac in the _Sourcebook Project_ (William R. Corliss)

## Cyrano
Lat: 20.5°S, Long: 157.7°E, Diam: 80 km, Depth: km, Rükl: _(farside)_, pre-Nectarian
**Left:**Clementine image from Map-A-Planet. **Middle:** Lunar Orbiter 2 II-075-H2 image from LPI. **Right:**Color-coded topography image from Map-A-Planet.

## Images


## Maps


## Description
**Cyrano** could be seen to lie within the confluence of three main impact events that of: the 2500 kilometre-wide South-Pole Aitken Basin to its south-east; the 500 kilometre-wide Keeler-Heaviside Basin to its north-east; and the 265 kilometre-wide Gagarin crater to its west -- all pre-Nectarian (~ 4.6 to 3.92 bn years) in age. **Cyrano** is of the same age also and, by all accounts -- with its relatively sharp-looking rim (that is, in those parts that have survived subsequent crater impacts), its worn terraces, and a flat floor showing only small hilly signs of a central peak -- the crater must be of a younger age within the above-mentioned period. The crater itself, however, has seen the impact wars; the north and western sides suffering most where several major impacts have obilterated the rim, its terracing, and deposited material onto the floor -- covering, perhaps, a history of events now lost forever. - JohnMoore2

## Description: Wikipedia


## Additional Information


## Nomenclature
*   Cyrano De Bergerac Savinien; French writer (1615-1655).  
*   The crater name **Cyrano** was in the first large list of farside feature names approved by the IAU in 1970. Cyrano (the person) is one of the very few creative writers to be honored on the Moon. The citation in Menzel, 1971 mentions his writing of "imaginary visits to Moon and Sun", in particular his **Comical History of the States and Empires of the Moon** and **... of the Sun**. At the time this name was introduced, the IAU was toying with the idea of honoring many other writers, artists and musicians. That proposal was formally adopted in 1973, but almost immediately squashed in 1974/1976. No other writers were or will be added. - JimMosher  
*   **De Bergerac** (Cyrano De Bergerac) was once an unofficial name for nearside crater **Carlini D** (H.P.Wilkins and P.Moore, _The Moon_).

## LPOD Articles


## Bibliography


## Cyrano De Bergerac in the _Sourcebook Project_ (William R. Corliss)
- In _Mysterious Universe, a handbook of astronomical anomalies_ (1979) **:**
*   Page 425: **The Moons of Mars** (Roscoe Lamont, _Popular Astronomy_, 1925). Note: this is a very interesting article about possible pre-1877 observations of the two satellites of Mars (Phobos and Deimos).
* * *
</excerpt>
### Rank 2 of 46 — 0.62
<excerpt title="Cyrano (crater)">
From Wikipedia, the free encyclopedia
Cyrano
Lunar Orbiter 2 image  
Coordinates20°30′S 157°42′E / 20.5°S 157.7°E  
Diameter79.58 km (49.45 mi)[[1]](https://en.wikipedia.org/wiki/Cyrano_(crater)#cite_note-GPN-1)  
Depth_Unknown_  
Colongitude204° at sunrise  
FormationPre-Nectarian[[2]](https://en.wikipedia.org/wiki/Cyrano_(crater)#cite_note-Wilhelms_et_al_1987-2)  
EponymCyrano de Bergerac
Cyrano from Apollo 15
Oblique view of Cyrano from Apollo 17
**Cyrano** is a worn lunarimpact crater that lies on the far side of the Moon.[[3]](https://en.wikipedia.org/wiki/Cyrano_(crater)#cite_note-Moore_2000-3) It lies due east of a huge walled plain called Gagarin, and to the north of the somewhat smaller crater Barbier.[[4]](https://en.wikipedia.org/wiki/Cyrano_(crater)#cite_note-Byrne_2008-4)

On the lunar geologic timescale, this crater dates to the Pre-Nectarian epoch.[[2]](https://en.wikipedia.org/wiki/Cyrano_(crater)#cite_note-Wilhelms_et_al_1987-2) The most notable aspect of this crater are the small impacts along the western and southwest rim, with the pear-shaped Cyrano P forming the later intrusion into the interior. The remainder of the rim has received some wear, and is particularly eroded at the northern end.[[5]](https://en.wikipedia.org/wiki/Cyrano_(crater)#cite_note-Bussey_Spudis_2004-5):103 The floor has perhaps a relatively thin covering of basaltic lava.[[4]](https://en.wikipedia.org/wiki/Cyrano_(crater)#cite_note-Byrne_2008-4) There are a few small craters within the interior, with a merged crater pair near the eastern side and a crater along the northeast inner wall. The northern half of the interior floor is slightly more irregular than the southern part.
This crater is named after French author and playwright Cyrano de Bergerac (1615–1655).[[6]](https://en.wikipedia.org/wiki/Cyrano_(crater)#cite_note-Menzel_et_al_1971-6) Its designation was officially adopted by the International Astronomical Union in 1970.[[1]](https://en.wikipedia.org/wiki/Cyrano_(crater)#cite_note-GPN-1)
By convention these features are identified on lunar maps by placing the letter on the side of the crater midpoint that is closest to Cyrano.[[7]](https://en.wikipedia.org/wiki/Cyrano_(crater)#cite_note-Grego_2015-7)

| Cyrano[[5]](https://en.wikipedia.org/wiki/Cyrano_(crater)#cite_note-Bussey_Spudis_2004-5):296 | Latitude | Longitude | Diameter |  
| --- | --- | --- | --- |  
| A | 18.1° S | 158.6° E | 26 km |  
| B | 18.3° S | 159.7° E | 23 km |  
| D | 19.6° S | 162.2° E | 24 km |  
| E | 20.1° S | 161.2° E | 21 km |  
| P | 21.6° S | 156.8° E | 19 km |
</excerpt>
### Rank 3 of 46 — 0.41
<excerpt title="Cyrano de Bergerac - Scientist of the Day">
# Cyrano de Bergerac - The Linda Hall
## Cyrano de Bergerac
MARCH 6, 2019

# Scientist of the Day - Cyrano de Bergerac
March 6, 2019
Cyrano de Bergerac, a French writer and playwright, was born Mar. 6, 1619. Most people know the Cyrano of Edmund Rostand's 1897 play, the proboscidly-precocious pursuer of the lovely Roxanne, but the real Cyrano was even more interesting, since he was a student of the French atomist, Pierre Gassendi, and a proponent of a sun-centered cosmology in a Catholic France that was, officially at least, still resistant to Copernicanism. Cyrano found a vehicle for his views in an account of a voyage to the Moon, published posthumously as _L'Autre Monde: les États et Empires de la Lune (The Other World: The States and Empires of the Moon_, 1657).
[![Image 7](blob:http://localhost/41682157faee7d242c4c483bccb75396) ](https://catalog.lindahall.org/permalink/01LINDAHALL_INST/19lda7s/alma995963993405961)
First page of “Histoire comique des Etat et Empire de la Lune,” _Oeuvres_, 1703 (Linda Hall Library)
The 17th century saw a number of such imaginary voyages to the Moon, by the likes of Johannes Kepler and Francis Godwin, but Cyrano's trip is notable because of his motive power - his craft was propelled by firecrackers! This was not exactly rocket science, but it was close (Godwin had flown to the moon in a rig powered by 25 geese!). Once he arrives on the moon, the unnamed narrator (whom we assume to be Cyrano) finds that the ruling race is quadrupedal and the menials are bipeds, and the Moon creatures refuse to believe that the Earth is inhabited, because it is just a moon of the Moon, and moons are never inhabited.
</excerpt>
### Rank 4 of 46 — 0.38
<excerpt title="Cyrano de Bergerac - Scientist of the Day">
# Scientist of the Day - Cyrano de Bergerac
March 6, 2019
Cyrano de Bergerac, a French writer and playwright, was born Mar. 6, 1619. Most people know the Cyrano of Edmund Rostand's 1897 play, the proboscidly-precocious pursuer of the lovely Roxanne, but the real Cyrano was even more interesting, since he was a student of the French atomist, Pierre Gassendi, and a proponent of a sun-centered cosmology in a Catholic France that was, officially at least, still resistant to Copernicanism. Cyrano found a vehicle for his views in an account of a voyage to the Moon, published posthumously as _L'Autre Monde: les États et Empires de la Lune (The Other World: The States and Empires of the Moon_, 1657).
[![Image 7](blob:http://localhost/41682157faee7d242c4c483bccb75396) ](https://catalog.lindahall.org/permalink/01LINDAHALL_INST/19lda7s/alma995963993405961)
First page of “Histoire comique des Etat et Empire de la Lune,” _Oeuvres_, 1703 (Linda Hall Library)
The 17th century saw a number of such imaginary voyages to the Moon, by the likes of Johannes Kepler and Francis Godwin, but Cyrano's trip is notable because of his motive power - his craft was propelled by firecrackers! This was not exactly rocket science, but it was close (Godwin had flown to the moon in a rig powered by 25 geese!). Once he arrives on the moon, the unnamed narrator (whom we assume to be Cyrano) finds that the ruling race is quadrupedal and the menials are bipeds, and the Moon creatures refuse to believe that the Earth is inhabited, because it is just a moon of the Moon, and moons are never inhabited.

# Scientist of the Day - Cyrano de Bergerac
Cyrano's pioneering work of science fiction is very scarce; we have never seen a first edition. The work was translated into English in 1659, and that edition is just as rare. In 1687, there was another English translation, and this one comes on the market every now and then, although we have never been able to afford it. The frontispiece (_first image_) is supposed to depict Cyrano's first attempt at lunar flight, using bottles of dew strapped to his body, the evaporation of which would carry him upward, although it is not a very convincing depiction. The dew bottles got Cyrano only as far as Canada, where he had to resort to his firecracker firepower to carry him the rest of the way.
[![Image 10](blob:http://localhost/1e04885968a15e977643c738885aeff3) ](https://catalog.lindahall.org/permalink/01LINDAHALL_INST/19lda7s/alma995963993405961)
Portrait of Cyrano de Bergerac, engraved frontispiece, _Oeuvres_, 1703 (Linda Hall Library)
The only version of Cyrano’s lunar voyage that we have in the Library is part of a 1703 collection of his works (_second image_). Our copy has no engraving of the journey, but it does have a frontispiece portrait of Cyrano (_third image_). Cyrano was no relation to the 18th-century Swiss scientist who claimed to be his grand-nephew, Cyano de Bergerac.
_Dr. William B. Ashworth, Jr., Consultant for the History of Science, Linda Hall Library and Associate Professor, Department of History, University of Missouri-Kansas City. Comments or corrections are welcome; please direct to__ashworthw@umkc.edu__._
More
* * *
</excerpt>
### Rank 5 of 46 — 0.25
<excerpt title="Cyrano (crater)">
| Cyrano[[5]](https://en.wikipedia.org/wiki/Cyrano_(crater)#cite_note-Bussey_Spudis_2004-5):296 | Latitude | Longitude | Diameter |  
| --- | --- | --- | --- |  
| A | 18.1° S | 158.6° E | 26 km |  
| B | 18.3° S | 159.7° E | 23 km |  
| D | 19.6° S | 162.2° E | 24 km |  
| E | 20.1° S | 161.2° E | 21 km |  
| P | 21.6° S | 156.8° E | 19 km |

1.   Jump up to: 12"Cyrano". _Gazetteer of Planetary Nomenclature_. USGS Astrogeology Research Program. Retrieved 2026-07-19.  
2.   Jump up to: 12Wilhelms, Don E.; McCauley, John F.; Trask, Newell J. (1987). _The geologic history of the Moon_. USGS Professional Paper 1348. Washington: U.S. Government Printing Office. doi:10.3133/pp1348. Table 8.3.  
3.   ↑Moore, Patrick (2000). _The Data Book of Astronomy_. CRC Press. p.67. ISBN978-1-4200-3344-1.  
4.   Jump up to: 12Byrne, Charles J. (2008). _The Far Side of the Moon_. Springer. pp.80, 89. ISBN978-1-4899-8806-5.  
5.   Jump up to: 12Bussey, B.; Spudis, P. (2004). _The Clementine Atlas of the Moon_. New York: Cambridge University Press. ISBN978-0-521-81528-4.  
6.   ↑Menzel, D. H.; et al. (1971). "Report on Lunar Nomenclature by the Working Group of Commission 17 of the IAU". _Space Science Reviews_. **12** (2): 136–186. Bibcode:1971SSRv...12..136M. doi:10.1007/BF00171763. S2CID122125855.  
7.   ↑Grego, P. (2015). "Satellite Crater". In Hargitai, H.; Kereszturi, Á. (eds.). _Encyclopedia of Planetary Landforms_. New York, NY: Springer. doi:10.1007/978-1-4614-3134-3_328.

*   Rükl, Antonín (1990). _Atlas of the Moon_. Kalmbach Books. ISBN978-0-913135-17-4.  
*   Wlasuk, Peter T. (2000). _Observing the Moon_. Springer. ISBN978-1-85233-193-1.
</excerpt>

## Search 10 — query: "site:planetarynames.wr.usgs.gov "Moon" "1973" "Approved""
### Rank 1 of 2557 — 0.84 (passed on)
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
### Rank 2 of 2557 — 0.81
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
### Rank 3 of 2557 — 0.81
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
### Rank 4 of 2557 — 0.79
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
### Rank 5 of 2557 — 0.77
<excerpt title="Astronaut-named features - Gazetteer of Planetary Nomenclature">
4962RavineRavine Moon 1.06-8.84 15.56-8.82-8.85 15.58 15.54 Planetographic, +East, -180 - 180 North America American Astronaut-named features LFLAC-78Approved 1973[59]Astronaut-named feature, Apollo 16 site.None Oct 25, 2010  
5020RhyslingRhysling Moon 0.12 26.07 3.62 26.07 26.07 3.63 3.62 Planetographic, +East, -180 - 180 North America American Astronaut-named features LFLAC-41Approved 1973[59]Astronaut-named feature, Apollo 15 site.None Oct 25, 2010  
5359ScarpScarp Moon 14.76 20.29 30.59 20.29 20.29 30.59 30.59 Planetographic, +East, -180 - 180 North America American Astronaut-named features LFLAC-43Approved 1973[59]Astronaut-named feature, Apollo 17 site.None Oct 25, 2010  
5396Sculptured HillsSculptured Hills Moon 12.41 20.24 31.06 20.42 20.05 31.24 30.88 Planetographic, +East, -180 - 180 North America American Astronaut-named features LFLAC-43Approved 1973[59]Astronaut-named feature, Apollo 17 site.None Oct 25, 2010  

5455ShakespeareShakespeare Moon 0.54 20.24 30.82 20.25 20.23 30.83 30.81 Planetographic, +East, -180 - 180 Europe Great Britain Astronaut-named features LFLAC-43Approved 1973[59]Astronaut-named feature, Apollo 17 site.None Oct 25, 2010  
5472Sharp-ApolloSharp Apollo Moon 0.01-3.02-23.43-3.02-3.02-23.43-23.43 Planetographic, +East, -180 - 180 North America American Astronaut-named features LFLAC-76Approved 1973[59]Astronaut-named feature, Apollo 12 site.Nov 17, 2026  
5484SherlockSherlock Moon 0.49 20.18 30.81 20.19 20.18 30.82 30.80 Planetographic, +East, -180 - 180 Europe Great Britain Astronaut-named features LFLAC-43Approved 1973[59]Astronaut-named feature, Apollo 17 site.None Oct 25, 2010  
5500ShortyShorty Moon 0.11 20.22 30.63 20.22 20.22 30.63 30.62 Planetographic, +East, -180 - 180 North America American Astronaut-named features LFLAC-43Approved 1973[59]Astronaut-named feature, Apollo 17 site.None Oct 25, 2010
</excerpt>

# Example 4
## Question
What is the birthday of the executive producer of a 2007 TV Series that includes a voice actor who was in one episode and also a writer of 'The Roast of' a movie star who cameoed in the 2004 film 'The SpongeBob SquarePants Movie' as himself?

## Expected answer
August 6, 1973

## Grade 0.00

## Search 1 — query: "The SpongeBob SquarePants Movie 2004 cameo as himself"
### Rank 1 of 88 — 0.80 (passed on)
<excerpt title="The SpongeBob SquarePants Movie">
_**The SpongeBob SquarePants Movie**_ is a 2004 American animated adventure comedy film co-written and directed by Stephen Hillenburg. Based on the television series _SpongeBob SquarePants_ created by Hillenburg, the film features the series' regular voice cast, including Tom Kenny, Bill Fagerbakke, Clancy Brown, Rodger Bumpass and Mr. Lawrence, who are joined by Alec Baldwin, Scarlett Johansson and Jeffrey Tambor, with David Hasselhoff appearing in live action as himself. In the film, SpongeBob with Patrick sets out on a quest to Shell City to retrieve King Neptune's stolen crown, exonerate his boss Mr. Krabs, stop Plankton, and prove his manhood.
Hillenburg accepted an offer for a film adaptation of _SpongeBob SquarePants_ from Paramount Pictures in 2002, after turning it down multiple times the previous year. He assembled a team from the show's writing staff, including himself, Derek Drymon, Tim Hill, Kent Osborne, Aaron Springer and Paul Tibbitt, and structured the film as a mythical [hero's journey](https://en.wikipedia.org/wiki/Hero's_journey "Hero's journey") that would bring SpongeBob and Patrick to the surface. The film was originally intended to serve as the series finale, but due to its financial success, the show continued. Tibbitt took Hillenburg's place as showrunner afterwards.
_The SpongeBob SquarePants Movie_ premiered at the [Grauman's Chinese Theatre](https://en.wikipedia.org/wiki/Grauman's_Chinese_Theatre "Grauman's Chinese Theatre") on November 14, 2004, and was released in the United States on November 19 by Paramount. It received generally positive reviews and grossed $141 million on a $30 million budget. It is the first in a series of _SpongeBob_ films.

Mr. Krabs opens a second location of the Krusty Krab, right next to the original. His fry cook, SpongeBob SquarePants, hopes to be promoted to manager of the new restaurant, but Krabs instead selects his co-worker, Squidward Tentacles, explaining to SpongeBob that he is a "kid" who is too young and immature to handle the position. Depressed, SpongeBob goes to the Goofy Goober ice cream parlor, where he indulges himself with ice cream with his best friend Patrick Star and wakes up the following morning with a hangover.
Krabs' rival Plankton, owner of the Chum Bucket restaurant, initiates "Plan Z" in an attempt to obtain the Krabby Patty secret formula and take over the world. He steals King Neptune's crown, sends it to a place called Shell City, and frames Krabs for the theft. Neptune confronts Krabs about his stolen crown and is convinced of Krabs' guilt when a hungover SpongeBob smears him. Recovering from his hangover, SpongeBob promises Neptune that he will retrieve the crown from Shell City. Neptune freezes Krabs until further notice, telling SpongeBob to return in ten days (until Patrick argues it down to six) or Krabs will be executed. Neptune's daughter, Mindy, encourages SpongeBob and Patrick but warns them of dangers surrounding Shell City, including "the Cyclops", a monster who kidnaps sea creatures.
SpongeBob and Patrick head for Shell City in the Patty Wagon, a Krabby Patty-shaped car stored underneath the restaurant. After the duo leave Bikini Bottom, Plankton steals the formula from the frozen Krabs and uses it to sell Krabby Patties. He distributes free helmets with the Krabby Patties that brainwash customers into doing Plankton's bidding, subsequently taking over Bikini Bottom and hiring a hitman named Dennis to prevent SpongeBob and Patrick from returning with the crown.
</excerpt>
### Rank 2 of 88 — 0.77
<excerpt title="The SpongeBob SquarePants Movie">
| Distributed by | * Paramount Pictures (United States and Canada)[[1]](https://en.wikipedia.org/wiki/The_SpongeBob_SquarePants_Movie#cite_note-BFI-2)[[2]](https://en.wikipedia.org/wiki/The_SpongeBob_SquarePants_Movie#cite_note-AFI-3) * United International Pictures (International)[[3]](https://en.wikipedia.org/wiki/The_SpongeBob_SquarePants_Movie#cite_note-ScreenDaily-4) |  
| Release dates | * November 14,2004([Grauman's Chinese Theatre](https://en.wikipedia.org/wiki/Grauman's_Chinese_Theatre "Grauman's Chinese Theatre")) * November 19,2004(United States) |  
| Running time | 87 minutes[[4]](https://en.wikipedia.org/wiki/The_SpongeBob_SquarePants_Movie#cite_note-BBFC-5) |  
| Country | United States[[1]](https://en.wikipedia.org/wiki/The_SpongeBob_SquarePants_Movie#cite_note-BFI-2)[[2]](https://en.wikipedia.org/wiki/The_SpongeBob_SquarePants_Movie#cite_note-AFI-3)[[5]](https://en.wikipedia.org/wiki/The_SpongeBob_SquarePants_Movie#cite_note-LUMIERE-6) |  
| Language | English |  
| Budget | $30 million[[6]](https://en.wikipedia.org/wiki/The_SpongeBob_SquarePants_Movie#cite_note-BOM-7) |  
| Box office | $141 million[[6]](https://en.wikipedia.org/wiki/The_SpongeBob_SquarePants_Movie#cite_note-BOM-7) |

_**The SpongeBob SquarePants Movie**_ is a 2004 American animated adventure comedy film co-written and directed by Stephen Hillenburg. Based on the television series _SpongeBob SquarePants_ created by Hillenburg, the film features the series' regular voice cast, including Tom Kenny, Bill Fagerbakke, Clancy Brown, Rodger Bumpass and Mr. Lawrence, who are joined by Alec Baldwin, Scarlett Johansson and Jeffrey Tambor, with David Hasselhoff appearing in live action as himself. In the film, SpongeBob with Patrick sets out on a quest to Shell City to retrieve King Neptune's stolen crown, exonerate his boss Mr. Krabs, stop Plankton, and prove his manhood.
Hillenburg accepted an offer for a film adaptation of _SpongeBob SquarePants_ from Paramount Pictures in 2002, after turning it down multiple times the previous year. He assembled a team from the show's writing staff, including himself, Derek Drymon, Tim Hill, Kent Osborne, Aaron Springer and Paul Tibbitt, and structured the film as a mythical [hero's journey](https://en.wikipedia.org/wiki/Hero's_journey "Hero's journey") that would bring SpongeBob and Patrick to the surface. The film was originally intended to serve as the series finale, but due to its financial success, the show continued. Tibbitt took Hillenburg's place as showrunner afterwards.
_The SpongeBob SquarePants Movie_ premiered at the [Grauman's Chinese Theatre](https://en.wikipedia.org/wiki/Grauman's_Chinese_Theatre "Grauman's Chinese Theatre") on November 14, 2004, and was released in the United States on November 19 by Paramount. It received generally positive reviews and grossed $141 million on a $30 million budget. It is the first in a series of _SpongeBob_ films.
</excerpt>
### Rank 3 of 88 — 0.66
<excerpt title="The SpongeBob SquarePants Movie">
*   Tom Kenny as:   
    *   SpongeBob SquarePants  
        *   Jim Wise provides SpongeBob's singing voice on "Goofy Goober Rock"

    *   French Narrator  
    *   Gary the Snail  
    *   various other characters

*   Bill Fagerbakke as Patrick Star and others  
*   Clancy Brown as Eugene Krabs  
*   Rodger Bumpass as:   
    *   Squidward Tentacles  
    *   Fish #4

*   Mr. Lawrence as:   
    *   Sheldon J. Plankton  
    *   Various

*   Alec Baldwin as Dennis  
*   Scarlett Johansson as Princess Mindy  
*   Jeffrey Tambor as King Neptune  
*   Jill Talley as:   
    *   Karen Plankton  
    *   Old Lady

*   Carolyn Lawrence as Sandy Cheeks  
*   Mary Jo Catlett as Mrs. Puff
Other characters from the television series also appear in the film, including Pearl Krabs, voiced by Lori Alan. Other supporting voice actors include Carlos Alazraqui, Dee Bradley Baker, Sirena Irwin, Thomas F. Wilson and Joshua Seth. Neil Ross provides the Cyclops' vocal effects. Crew members Derek Drymon, Stephen Hillenburg and Aaron Springer make vocal cameo appearances.
*   David Hasselhoff as himself  
*   Aaron Hendry as the Cyclops (in-suit performer)
In a mid-credits scene, Mageina Tovah portrays a theater usher.

_The SpongeBob SquarePants Movie_ was long-planned,[[7]](https://en.wikipedia.org/wiki/The_SpongeBob_SquarePants_Movie#cite_note-RDS-8) as Nickelodeon and Paramount Pictures had approached to series creator Stephen Hillenburg for a film based on _SpongeBob SquarePants_, but he refused for more than a year.[[8]](https://en.wikipedia.org/wiki/The_SpongeBob_SquarePants_Movie#cite_note-Edel1-9) Hillenburg was concerned, after watching _The Iron Giant_ and _Toy Story_ with his son, about the challenge of SpongeBob and Patrick doing something more cinematically consequential and inspiring without losing what he called the SpongeBob "cadence".[[8]](https://en.wikipedia.org/wiki/The_SpongeBob_SquarePants_Movie#cite_note-Edel1-9) Hillenburg believed that the film's story "had to be SpongeBob in a great adventure. That's where the comedy's coming from, having these two naïve characters, SpongeBob and Patrick, a doofus and an idiot, on this incredibly dangerous heroic odyssey with all the odds against them."[[8]](https://en.wikipedia.org/wiki/The_SpongeBob_SquarePants_Movie#cite_note-Edel1-9)
> I never wanted to do a movie because I didn't think that what we wanted to say needed to be in a movie. I like the short form for animation. Then this story idea came up that lent itself to a longer format. You can't do a road trip adventure in a short form.
</excerpt>
### Rank 4 of 88 — 0.65
<excerpt title="The SpongeBob SquarePants Movie">
The film features live-action scenes directed by Mark Osborne in Santa Monica, California.[[11]](https://en.wikipedia.org/wiki/The_SpongeBob_SquarePants_Movie#cite_note-AbsorbingTales-12)[[33]](https://en.wikipedia.org/wiki/The_SpongeBob_SquarePants_Movie#cite_note-Replica1-34) The ship used during the 30-second opening featuring the pirates singing the theme song was the _Bounty_,[[34]](https://en.wikipedia.org/wiki/The_SpongeBob_SquarePants_Movie#cite_note-Bounty1-35)[[35]](https://en.wikipedia.org/wiki/The_SpongeBob_SquarePants_Movie#cite_note-36) a 180-foot-long (55 m), enlarged reconstruction of the 1787 Royal Navy sailing ship HMS _Bounty_ built for _Mutiny on the Bounty_ (1962). The ship appeared in a number of other films, including _Treasure Island_ (1999), _[Pirates of the Caribbean: Dead Man's Chest](https://en.wikipedia.org/wiki/Pirates\_of\_the\_Caribbean:\_Dead\_Man's\_Chest "Pirates of the Caribbean: Dead Man's Chest")_ (2006) and _[Pirates of the Caribbean: At World's End](https://en.wikipedia.org/wiki/Pirates\_of\_the\_Caribbean:\_At\_World's\_End "Pirates of the Caribbean: At World's End")_ (2007).[[36]](https://en.wikipedia.org/wiki/The_SpongeBob_SquarePants_Movie#cite_note-37)[[37]](https://en.wikipedia.org/wiki/The_SpongeBob_SquarePants_Movie#cite_note-38) In film trailers, live-action scenes were taken from _Das Boot_ (1981), _The Hunt for Red October_ (1990) and _U-571_ (2000).[[9]](https://en.wikipedia.org/wiki/The_SpongeBob_SquarePants_Movie#cite_note-EVT-10)
The crew built a larger-than-life replica of David Hasselhoff as his double in filming the fight scene with Dennis.

David Hasselhoff made a cameo appearance in the live-action scenes, offering SpongeBob and Patrick a ride to Bikini Bottom.[[38]](https://en.wikipedia.org/wiki/The_SpongeBob_SquarePants_Movie#cite_note-LAS1-39) The scene was originally written before consulting Hasselhoff.[[39]](https://en.wikipedia.org/wiki/The_SpongeBob_SquarePants_Movie#cite_note-10Secrets1-40)[[40]](https://en.wikipedia.org/wiki/The_SpongeBob_SquarePants_Movie#cite_note-10Secrets2-41) Hillenburg was pleased with the storyboards;[[12]](https://en.wikipedia.org/wiki/The_SpongeBob_SquarePants_Movie#cite_note-OralHistory-13) Lead storyboard artist Sherm Cohen noted the positive reaction among the film's storyboard artists after Hillenburg brought up the animatic of the scene.[[12]](https://en.wikipedia.org/wiki/The_SpongeBob_SquarePants_Movie#cite_note-OralHistory-13) Hillenburg and the staff were counting on casting Hasselhoff, who eventually agreed before seeing the script.[[39]](https://en.wikipedia.org/wiki/The_SpongeBob_SquarePants_Movie#cite_note-10Secrets1-40)[[40]](https://en.wikipedia.org/wiki/The_SpongeBob_SquarePants_Movie#cite_note-10Secrets2-41) Hillenburg said about the actor, "He's a great guy. ...He was great at making fun of himself."[[39]](https://en.wikipedia.org/wiki/The_SpongeBob_SquarePants_Movie#cite_note-10Secrets1-40)[[40]](https://en.wikipedia.org/wiki/The_SpongeBob_SquarePants_Movie#cite_note-10Secrets2-41)
</excerpt>
### Rank 5 of 88 — 0.64
<excerpt title="The SpongeBob SquarePants Movie">
SpongeBob and Patrick encounter a hazardous trench, lose the Patty Wagon, and contemplate giving up. Mindy, whom Patrick has a crush on, appears and encourages them by applying fake mustaches made of seaweed, convincing them that she magically turned them from kids into men. Armed with newfound confidence, the two successfully traverse the trench and encounter Dennis on the other side. He demonstrates that the mustaches are fake, and prepares to squash the duo with his boot but is suddenly stepped on by a much larger boot belonging to the "Cyclops", a human diver, who abducts SpongeBob and Patrick.
The duo are placed under a heat lamp by the Cyclops, learning that they have arrived in "Shell City", a gift shop selling dried sea creatures. Proud that they reached their destination, they shed tears just before getting dried up, which short-circuit the lamp and activate the fire sprinkler system, reviving the two alongside the other dried sea creatures. While the sea creatures attack the Cyclops, SpongeBob and Patrick take the crown to the beach, where David Hasselhoff offers them a ride home. Dennis catches up and fights them on Hasselhoff's back, ultimately falling into the sea as Hasselhoff passes under a catamaran.
Neptune arrives to execute Krabs, but SpongeBob and Patrick return with the crown just in time. Plankton drops a mind-control helmet on Neptune and surrounds SpongeBob, Patrick and Mindy with his army of slaves. SpongeBob, embracing the fact that he's accomplished so much despite being a kid, uses the power of rock and roll to play "Goofy Goober Rock", freeing Neptune and the citizens of Bikini Bottom from Plankton's control.
As Plankton is arrested by the police, Neptune unfreezes Krabs and the two make amends. Krabs then appoints SpongeBob as the manager of the Krusty Krab 2.

*   Tom Kenny as:   
    *   SpongeBob SquarePants  
        *   Jim Wise provides SpongeBob's singing voice on "Goofy Goober Rock"

    *   French Narrator  
    *   Gary the Snail  
    *   various other characters

*   Bill Fagerbakke as Patrick Star and others  
*   Clancy Brown as Eugene Krabs  
*   Rodger Bumpass as:   
    *   Squidward Tentacles  
    *   Fish #4

*   Mr. Lawrence as:   
    *   Sheldon J. Plankton  
    *   Various

*   Alec Baldwin as Dennis  
*   Scarlett Johansson as Princess Mindy  
*   Jeffrey Tambor as King Neptune  
*   Jill Talley as:   
    *   Karen Plankton  
    *   Old Lady

*   Carolyn Lawrence as Sandy Cheeks  
*   Mary Jo Catlett as Mrs. Puff
Other characters from the television series also appear in the film, including Pearl Krabs, voiced by Lori Alan. Other supporting voice actors include Carlos Alazraqui, Dee Bradley Baker, Sirena Irwin, Thomas F. Wilson and Joshua Seth. Neil Ross provides the Cyclops' vocal effects. Crew members Derek Drymon, Stephen Hillenburg and Aaron Springer make vocal cameo appearances.
*   David Hasselhoff as himself  
*   Aaron Hendry as the Cyclops (in-suit performer)
In a mid-credits scene, Mageina Tovah portrays a theater usher.
</excerpt>

## Search 2 — query: ""The Roast of David Hasselhoff" writer"
### Rank 1 of 44 — 0.61 (passed on)
<excerpt title="TV: 'Roast of David Hasselhoff'">
# TV: "Roast of David Hasselhoff"
No subject is off limits during Comedy Central's roasts, which means the "Roast of David Hasselhoff" should be cruel and hilarious. Besides being on two of the campiest television shows of all time - "Knight Rider" and "Baywatch" - the Hoff may be more recognized for his drinking habits and bitter divorce. Greg Giraldo and Jeffrey Ross should have some particularly amusing and nasty barbs for Mr. Ripplepecs.
> "Roast of David Hasselhoff"  
>   
>   
> 10 p.m. Sunday on Comedy Central
[](mailto:?subject=TV%3A%20%22Roast%20of%20David%20Hasselhoff%22%20-%20from%20Columbus%20Monthly&body=TV%3A%20%22Roast%20of%20David%20Hasselhoff%22%0A%0ANo%20subject%20is%20off%20limits%20during%20Comedy%20Central's%20roasts%2C%20which%20means%20the%20%22Roast%20of%20David%20Hasselhoff%22%20should%20be%20cruel%20and%20hilarious.%20Besides%20being%20on%20two%20of%20the%20campiest%20television%20shows%20of%20all%20time%20-%E2%80%A6%0A%0ACheck%20out%20this%20story%20on%20columbusmonthly.com%3A%20https%3A%2F%2Fwww.columbusmonthly.com%2Fstory%2Fentertainment%2Fmovies%2F2010%2F08%2F11%2Ftv-roast-david-hasselhoff%2F23026019007%2F)

# TV: "Roast of David Hasselhoff"
[새벽 2시간마다 깨는 ”갱년기 불면증“.. 부족한 "이것'' 때문?! 원인부터 종결시킨 [세계특허]여성갱년기 멀티케어 [리피어라] 국내유일 21중 최다기능성으로 갱년기 모든증상 한번에! 국제 특허 획득 'MS-10' 성분으로 화제!리피어라 - 갱년기 특허성분 MS-10 | AdAd](https://healyj.kr/rpta43 "새벽 2시간마다 깨는 ”갱년기 불면증“.. 부족한 \"이것'' 때문?! 원인부터 종결시킨 [세계특허]")
Undo
[갱년기 후끈거림에 직빵! 먹자마자 '열감’ 싹~! 세계특허 '이것‘[국내유일 21중 최다기능성 리피어라] 5년연속1위, 브랜드대상 10관왕!리피어라 - 갱년기 특허성분 MS-10 | AdAd 더 알아보기](https://healyj.kr/rpta46 "갱년기 후끈거림에 직빵! 먹자마자 '열감’ 싹~! 세계특허 '이것‘")
Undo
프랑스 여성이 살안찌는 이유? 유학가서 알아온 비밀 하루의 일기장 | [AdAd 더 알아보기](https://slimnote.kr/wmh27sa8 "프랑스 여성이 살안찌는 이유? 유학가서 알아온 비밀")
Undo
[[화제] 이제 파란약 몰래 안챙겨요. 40대 실제 극복기 홍조 오고 두통 올까봐 무서워 쪼개 먹던 과거 끝. '이거' 1알로 20대 광명 찾은 썰 풉니다.김차장의 이중생활 | AdAd 더 알아보기](https://blog-roan-pi.vercel.app/post/6ae831a483f79274a793f2e1 "[화제] 이제 파란약 몰래 안챙겨요. 40대 실제 극복기")
Undo
</excerpt>
### Rank 2 of 44 — 0.53
<excerpt title="TV: 'Roast of David Hasselhoff'">
# TV: "Roast of David Hasselhoff"
WeddingsParentDiningFeaturesArtsHome & StyleNewslettersLegals
Subscribe
MOVIES
Staff Writer
Columbus Alive
Aug. 11, 2010 Updated Aug. 18, 2010, 4:34 p.m. ET
[](mailto:?subject=TV%3A%20%22Roast%20of%20David%20Hasselhoff%22%20-%20from%20Columbus%20Monthly&body=TV%3A%20%22Roast%20of%20David%20Hasselhoff%22%0A%0ANo%20subject%20is%20off%20limits%20during%20Comedy%20Central's%20roasts%2C%20which%20means%20the%20%22Roast%20of%20David%20Hasselhoff%22%20should%20be%20cruel%20and%20hilarious.%20Besides%20being%20on%20two%20of%20the%20campiest%20television%20shows%20of%20all%20time%20-%E2%80%A6%0A%0ACheck%20out%20this%20story%20on%20columbusmonthly.com%3A%20https%3A%2F%2Fwww.columbusmonthly.com%2Fstory%2Fentertainment%2Fmovies%2F2010%2F08%2F11%2Ftv-roast-david-hasselhoff%2F23026019007%2F)
Video 2
Keep Watching

# TV: "Roast of David Hasselhoff"
No subject is off limits during Comedy Central's roasts, which means the "Roast of David Hasselhoff" should be cruel and hilarious. Besides being on two of the campiest television shows of all time - "Knight Rider" and "Baywatch" - the Hoff may be more recognized for his drinking habits and bitter divorce. Greg Giraldo and Jeffrey Ross should have some particularly amusing and nasty barbs for Mr. Ripplepecs.
> "Roast of David Hasselhoff"  
>   
>   
> 10 p.m. Sunday on Comedy Central
[](mailto:?subject=TV%3A%20%22Roast%20of%20David%20Hasselhoff%22%20-%20from%20Columbus%20Monthly&body=TV%3A%20%22Roast%20of%20David%20Hasselhoff%22%0A%0ANo%20subject%20is%20off%20limits%20during%20Comedy%20Central's%20roasts%2C%20which%20means%20the%20%22Roast%20of%20David%20Hasselhoff%22%20should%20be%20cruel%20and%20hilarious.%20Besides%20being%20on%20two%20of%20the%20campiest%20television%20shows%20of%20all%20time%20-%E2%80%A6%0A%0ACheck%20out%20this%20story%20on%20columbusmonthly.com%3A%20https%3A%2F%2Fwww.columbusmonthly.com%2Fstory%2Fentertainment%2Fmovies%2F2010%2F08%2F11%2Ftv-roast-david-hasselhoff%2F23026019007%2F)
</excerpt>
### Rank 3 of 44 — 0.33
<excerpt title="The Roast of David Hasselhoff">
*   work  
*   about  
*   contact

## writer | director
*   work  
*   about  
*   contact

## The Roast of David Hasselhoff
</excerpt>
### Rank 4 of 44 — 0.27
<excerpt title="The Roast Of David Hasselhoff Head Writer">
Log In
Sign Up
Watch reels about the roast of david hasselhoff head writer from people around the world.
217 📣 New Workshop! Pitching Like a Hollywood Pro 📅 Thursday April 2, 1-2pm 📍Lincoln Lodge Theater, Chicago 🔑Get your FunnyCon pass at 🔗 in bio 😝 Comedy Nerds Unite! FunnyCon runs Mar 31-Apr 2 🤝 Performances + Workshops + Connect + Community #comedy #funnycon #chicago #workshop #screenwriter
3,314 still thinking about this night ⭐️ thank you to everyone who came out to our premiere at @tosketchfest 💛 thank you for hosting @its_triciablack more soon 👀 / still photography by @jordanlburchill / additional video by @janellemcguinness #likecommentsubscribe #webseries #canadianfilm #TOsketchfest #satire
46K SEND THAT SCREENPLAY!! Full DIY Filmmaking Panel out now on YouTube! Panelists: @ilana @everette @directordaddy @seck2x @realrasankuvly @cryinroman Moderator: @meowmoriez Graphic Design: @fancyclownery
24K The Studio won a total of 13 awards at the 2025 Emmys, setting a new record for the most awards for a comedy series in a single Emmy season, breaking the previous record of 11 by The Bear (2022). Must watch TV series of the year
94.8K guest 031 @karinafontes is a Los Angeles based actress, director, and founder of short form production company @littletrickspictures
305K Copy you Writers: @isabelfiliz & meee Shot by: @isabelfiliz #filmproduction #comedyskit #onsetlife
9,192 Step into our office 📌 THE RECEPTIONIST, your new favorite workplace black comedy is now in rehearsals. Mark your calendars; performances begin April 15 at the Pershing Square Signature Center. #TheReceptionist
121K they won’t take “no” for an answer . . . #comedy #actor #sketch #pickme #filmmakers

749 Want to learn the art of sketch comedy writing? Fulfill all your SNL wishes and I Think You Should Leave dreams with this 8-week deep dive into how to write your own comedy sketches for stage or video. CLASSES START ON MARCH 10th, SO SIGN UP TODAY! Link in bio
38.5K Even better, a reading of “The Very Hungry Manager” by @ikebarinholtz at the official 2026 @producersguild Awards 🏆
775 Mae is still learning about the term “professionalism” #comedyreels #comedyseries #improv #comedyshow #webseries
200 I think they’re stoked to be here!! #webseries #comedyseries #improv #comedy #comedyshow
Get the full experience
Sign up for Instagram
</excerpt>
### Rank 5 of 44 — 0.26
<excerpt title="The Roast Of David Hasselhoff Writer Or Writers">
Log In
Sign Up
Watch reels about the roast of david hasselhoff writer or writers from people around the world.
217 📣 New Workshop! Pitching Like a Hollywood Pro 📅 Thursday April 2, 1-2pm 📍Lincoln Lodge Theater, Chicago 🔑Get your FunnyCon pass at 🔗 in bio 😝 Comedy Nerds Unite! FunnyCon runs Mar 31-Apr 2 🤝 Performances + Workshops + Connect + Community #comedy #funnycon #chicago #workshop #screenwriter
3,314 still thinking about this night ⭐️ thank you to everyone who came out to our premiere at @tosketchfest 💛 thank you for hosting @its_triciablack more soon 👀 / still photography by @jordanlburchill / additional video by @janellemcguinness #likecommentsubscribe #webseries #canadianfilm #TOsketchfest #satire
46K SEND THAT SCREENPLAY!! Full DIY Filmmaking Panel out now on YouTube! Panelists: @ilana @everette @directordaddy @seck2x @realrasankuvly @cryinroman Moderator: @meowmoriez Graphic Design: @fancyclownery
24K The Studio won a total of 13 awards at the 2025 Emmys, setting a new record for the most awards for a comedy series in a single Emmy season, breaking the previous record of 11 by The Bear (2022). Must watch TV series of the year
94.8K guest 031 @karinafontes is a Los Angeles based actress, director, and founder of short form production company @littletrickspictures
305K Copy you Writers: @isabelfiliz & meee Shot by: @isabelfiliz #filmproduction #comedyskit #onsetlife
9,192 Step into our office 📌 THE RECEPTIONIST, your new favorite workplace black comedy is now in rehearsals. Mark your calendars; performances begin April 15 at the Pershing Square Signature Center. #TheReceptionist
121K they won’t take “no” for an answer . . . #comedy #actor #sketch #pickme #filmmakers

749 Want to learn the art of sketch comedy writing? Fulfill all your SNL wishes and I Think You Should Leave dreams with this 8-week deep dive into how to write your own comedy sketches for stage or video. CLASSES START ON MARCH 10th, SO SIGN UP TODAY! Link in bio
38.5K Even better, a reading of “The Very Hungry Manager” by @ikebarinholtz at the official 2026 @producersguild Awards 🏆
775 Mae is still learning about the term “professionalism” #comedyreels #comedyseries #improv #comedyshow #webseries
200 I think they’re stoked to be here!! #webseries #comedyseries #improv #comedy #comedyshow
Get the full experience
Sign up for Instagram
</excerpt>

## Search 3 — query: ""The Roast of David Hasselhoff" writer "Jeff Ross""
### Rank 1 of 33 — 0.67 (passed on)
<excerpt title="Filmer och TV-program med Jeff Ross">
# Jeff Ross
Hailed by one critic as "the best documentary to emerge so far from the Iraq War," "Patriot Act" proved to be a poignant portrayal of both the Iraq war and the tradition of USO comedy tours made popular by legendary comic Bob Hope.Returning to his offensive nature in 2006, Ross wrote and produced the animated series "Where My Dogs At?" (MTV2). Parodying Hollywood celebrity, the series was centered on Buddy (Ross), a beagle lost on the streets of Hollywood, and his friend Woof (Tracy Morgan), a bulldog. The series was pulled after its first season however, when controversy arose about the depiction of African-American women in the episode "Woofy Loves Snoop," a parody of rapper Snoop Dogg. Undeterred, Ross went on to star in his first stand-up special on Comedy Central, "Jeffrey Ross: No Offense," in 2008. That same year, Ross signed on raise his profile outside the comedy realm by competing on ABC's reality show phenomenon "Dancing with the Stars." But his stint on the show was short lived, as he was accidentally poked in the eye by his partner, Edyta Sliwinska, during rehearsals and suffered a scratched cornea. Though he competed against doctor's orders, Ross was the first to be eliminated from the show. Meanwhile, he continued to roast a wide swath of celebrities on Comedy Central, including Larry the Cable Guy, Joan Rivers, Donald Trump, David Hasselhoff and Charlie Sheen.
MER
</excerpt>
### Rank 2 of 33 — 0.63
<excerpt title="Filmer och TV-program med Jeff Ross">
# Jeff Ross
Hailed by one critic as "the best documentary to emerge so far from the Iraq War," "Patriot Act" proved to be a poignant portrayal of both the Iraq war and the tradition of USO comedy tours made popular by legendary comic Bob Hope.Returning to his offensive nature in 2006, Ross wrote and produced the animated series "Where My Dogs At?" (MTV2). Parodying Hollywood celebrity, the series was centered on Buddy (Ross), a beagle lost on the streets of Hollywood, and his friend Woof (Tracy Morgan), a bulldog. The series was pulled after its first season however, when controversy arose about the depiction of African-American women in the episode "Woofy Loves Snoop," a parody of rapper Snoop Dogg. Undeterred, Ross went on to star in his first stand-up special on Comedy Central, "Jeffrey Ross: No Offense," in 2008. That same year, Ross signed on raise his profile outside the comedy realm by competing on ABC's reality show phenomenon "Dancing with the Stars." But his stint on the show was short lived, as he was accidentally poked in the eye by his partner, Edyta Sliwinska, during rehearsals and suffered a scratched cornea. Though he competed against doctor's orders, Ross was the first to be eliminated from the show. Meanwhile, he continued to roast a wide swath of celebrities on Comedy Central, including Larry the Cable Guy, Joan Rivers, Donald Trump, David Hasselhoff and Charlie Sheen.

# Jeff Ross
## Filmer
*    Ricky Stanicky       
*    The Roast of James Franco       
*    The Roast of Donald Trump       
*    The Roast of Charlie Sheen       
*    The Roast of Bruce Willis       
*    The Roast Of Justin Bieber       
*    The Roast of Rob Lowe       
*    The Roast of David Hasselhoff       
*    The Roast of William Shatner

# Jeff Ross
## Producent
*    Hot Listings Miami       
*    John Leguizamo: Spic-O-Rama       
*    Jeff Ross Presents: Roast Battle

# Jeff Ross
## Barn och familj
*    The Emoji Movie       
*    Trassel Serien: Drottning för en dag

# Jeff Ross
## Program
*    Jeff Ross Presents: Roast Battle
</excerpt>
### Rank 3 of 33 — 0.49
<excerpt title="What's your all-time favorite roast line? : r/Standup">
# Comments Section
MonkyThrowPoop
•3y ago
Sarah Tollemache about Joe List (her husband).
“Joe tells me a lot to go back to Africa, which is partly because I’m from South Africa, but mostly because he’s from Boston.”
Reply  Share
crazylikeajellyfish
•3y ago
Laughed out loud on this one, incredible
Reply  Share
13 more replies
13 more replies
13 more replies
Ggentry9
•3y ago
How is it possible that Courtney Love looks worse than Kurt Cobain - Jeff Ross
Reply  Share
crazylikeajellyfish
•3y ago
That's elegant, love it
Reply  Share
1 more reply
1 more reply
1 more reply
3 more replies
3 more replies
3 more replies
LogicalGold5264
•3y ago
Nikki Glaser had an amazing set at the Alec Baldwin roast, but the one that stunned the audience was to Caitlin Jennings:
"Caitlin, I know it's hard being a new mom. But even Casey Anthony knows the current location of her daughter".
Damn!
Reply  Share
crazylikeajellyfish
•3y ago
Oh man -- that Martin Short line is my standalone favorite, but this is probably my favorite full roast set. The line you called it was so good, and I was also a fan of:
"Blake [Griffin], you look like a black guy that was made by a printer running out of ink"
That single set cemented me as a Nikki Glaser fan
Reply  Share
1 more reply
1 more reply
1 more reply
More replies
Mhammerhands
•3y ago
“His mom died the way Dave lives, and unrecognizable road feature”
https://youtu.be/l7K3y4EPq10
1 more reply
1 more reply
1 more reply
CertainRoof5043
•3y ago
Greg Giraldo- {Ralphie May] You’re the only guy who watches porn and cums when the guy delivers the pizza
56 more replies
56 more replies
56 more replies
Queasy-Impression618
•3y ago
Marshmallows on a fall evening or a pot luck roast
1 more reply
1 more reply
1 more reply
</excerpt>
### Rank 4 of 33 — 0.47
<excerpt title="Last night, Roastmaster General Jeff Ross sat down with Showbiz Tonight ...">
# Get Your Classic Roast On
In anticipation of The Mother of All Roasts, the #RoseanneRoast, airing this Sunday at 10/9c, Comedy Central is now streaming full episodes of some of its most popular Roasts, including The Roast of David Hasselhoff, The Roast of Bob Saget,The Roast of Flavor Flav, and The Roast of William Shatner.
Go forth and get burned!
#comedy central roasts#david hasselhoff#bob saget#flavor flav#William Shatner#RoseanneRoast#television
3
7
comedycentral
www.colbertnation.com
Click the gif to watch Stephen's coverage of Chick-fil-A Appreciation Day from last night's Colbert Report.
#colbert report#stephen colbert#chick-fil-a#mike huckabee#television#gif
51
45
comedycentral
Reblogged
toddbarry
Follow
bit.ly
**SUMMER VALUE TOUR starts August 15! Posters for sale at all shows. Designed by Greg Sutter.Click on venue name for tickets.**
**8/15 - COLUMBIA, SC -****Tapps Arts Center****8/16 - CHARLESTON, SC -****The Pour House****8/17 - RALEIGH, NC -****Kings Barcade****8/18 - RICHMOND, VA (two shows) -****Gallery 5****8/19 - ASHEVILLE, NC -****Grey Eagle****8/21 - NASHVILLE, TN -****Exit/In****8/22 - KNOXVILLE, TN (two shows) -****Pilot Light****8/23 - ATHENS, GA -****40 Watt Club****8/24 - ATLANTA, GA -****Plaza Theatre**
#Todd Barry#Neil Hamburger#stand-up
12
11
comedycentralReblogged standupcomedyblogkatarnsarchive-blogFollow#John Mulaney#stand-up584340

# Get Your Classic Roast On
comedycentralRebloggedbrooklynmutt-deactivated2021090I figure if people don’t like what they are seeing they can do what Joe Paterno did and look the other way.Comedian Jeffrey Ross on his Joe Paterno costume at the CC roast of Rosanne Barr.- Hollywood Reporter (via brooklynmutt)Source: hollywoodreporter.com#Jeff Ross#RoseanneRoast#comedy central roasts#stand-up#joe paterno#roseanne1854
comedycentralwww.comedycentral.comCrack open an economy-sized tub of mayo, sit back and enjoy all of the original Anger Translator videos.There's more Obama and Luther coming this fall when Key & Peele returns.#Key and Peele#Obama and Luther#obama anger translator#television#Keegan-Michael Key#Jordan Peele#sketch comedy#barack obama149112
comedycentralReblogged24thoughtspersecond-deactivatedMY MATT GROENING SIGNED HYPNOTOAD FINALLY CAME TODAYThis was the best thing to come home to after an 8 hour shiftNot sure if you can see, but not only did Mr. Groening sign his name, but he drew Bender and wrote my name. Matt Groening sort of knows my name!I’m so happy.comedycentralThat's awesome! Congra--ALL GLORY TO THE HYPNOTOAD#hypnotoad#futurama#matt groening169143
comedycentralRebloggednonononono-nono-no-deactivated2i drew this in a drawing-book at school when i was 7 years old.comedycentralDeath to all humans has never been so adorable.#futurama#fanarama#fan art#bender13458
comedycentralwww.1iota.comJeff Ross's new Comedy Central series, The Burn, is coming soon. Click the image to get free tickets to a taping.Source: 1iota.com#jeff ross#the burn#the burn with jeff ross#television614
</excerpt>
### Rank 5 of 33 — 0.42
<excerpt title="Last night, Roastmaster General Jeff Ross sat down with Showbiz Tonight ...">
# Last night, Roastmaster General Jeff Ross sat down with Showbiz Tonight to discuss his controversial costume at the... – @comedycentral on Tumblr
*     
*   Explore  
*   Communities  
*    Change palette
Sign up Log in
comedycentral
Reblogged
ccroasts-blog
Follow
www.hlntv.com
Last night, Roastmaster General Jeff Ross sat down with Showbiz Tonight to discuss his controversial costume at the #RoseanneRoast.
Tune in this Sunday at 10/9c for the Mother of All Roasts to see Jeff and a whole dais of hooligans in action.
#Jeff Ross#RoseanneRoast#comedy central roasts#television#joe paterno#stand-up
2
3
6 notes
0 comments
2 reblogs
3 likes
Best comments first
Move along, nothing to see here.Check out the reblogs

# Last night, Roastmaster General Jeff Ross sat down with Showbiz Tonight to discuss his controversial costume at the... – @comedycentral on Tumblr
## More from @comedycentral
comedycentral
Reblogged
thecomicscomic
Follow
thecomicscomic.com
Lynn Shawcroft talks about Mitch Hedberg’s writing process, his notebooks and the power of daydreaming in this great installment of Scott Moran’s documentary series, “Modern Comedian.”
WATCH IT
#Mitch Hedberg#stand-up
35
56
comedycentral
www.buzzfeed.com
(via Where Are They Now: The Stars Of Roseanne)
Source: BuzzFeed
#joseph gordon-levitt#roseanne#RoseanneRoast#television
4 175
202
Sponsored
comedycentral
instagr.am
Tune in for the Mother Of All Roasts, the #RoseanneRoast, coming this Sunday at 10/9c. (Taken with Instagram)
#roseanneroast
9
18
comedycentral
Reblogged
ccroasts-blog
Follow

# Get Your Classic Roast On
In anticipation of The Mother of All Roasts, the #RoseanneRoast, airing this Sunday at 10/9c, Comedy Central is now streaming full episodes of some of its most popular Roasts, including The Roast of David Hasselhoff, The Roast of Bob Saget,The Roast of Flavor Flav, and The Roast of William Shatner.
Go forth and get burned!
#comedy central roasts#david hasselhoff#bob saget#flavor flav#William Shatner#RoseanneRoast#television
3
7
comedycentral
www.colbertnation.com
Click the gif to watch Stephen's coverage of Chick-fil-A Appreciation Day from last night's Colbert Report.
#colbert report#stephen colbert#chick-fil-a#mike huckabee#television#gif
51
45
comedycentral
Reblogged
toddbarry
Follow
bit.ly
**SUMMER VALUE TOUR starts August 15! Posters for sale at all shows. Designed by Greg Sutter.Click on venue name for tickets.**
**8/15 - COLUMBIA, SC -****Tapps Arts Center****8/16 - CHARLESTON, SC -****The Pour House****8/17 - RALEIGH, NC -****Kings Barcade****8/18 - RICHMOND, VA (two shows) -****Gallery 5****8/19 - ASHEVILLE, NC -****Grey Eagle****8/21 - NASHVILLE, TN -****Exit/In****8/22 - KNOXVILLE, TN (two shows) -****Pilot Light****8/23 - ATHENS, GA -****40 Watt Club****8/24 - ATLANTA, GA -****Plaza Theatre**
#Todd Barry#Neil Hamburger#stand-up
12
11
comedycentralReblogged standupcomedyblogkatarnsarchive-blogFollow#John Mulaney#stand-up584340
</excerpt>

## Search 4 — query: ""writer" "The Roast of David Hasselhoff""
### Rank 1 of 31 — 0.48 (passed on)
<excerpt title="Filmer och TV-program med Jeff Ross">
# Jeff Ross
Hailed by one critic as "the best documentary to emerge so far from the Iraq War," "Patriot Act" proved to be a poignant portrayal of both the Iraq war and the tradition of USO comedy tours made popular by legendary comic Bob Hope.Returning to his offensive nature in 2006, Ross wrote and produced the animated series "Where My Dogs At?" (MTV2). Parodying Hollywood celebrity, the series was centered on Buddy (Ross), a beagle lost on the streets of Hollywood, and his friend Woof (Tracy Morgan), a bulldog. The series was pulled after its first season however, when controversy arose about the depiction of African-American women in the episode "Woofy Loves Snoop," a parody of rapper Snoop Dogg. Undeterred, Ross went on to star in his first stand-up special on Comedy Central, "Jeffrey Ross: No Offense," in 2008. That same year, Ross signed on raise his profile outside the comedy realm by competing on ABC's reality show phenomenon "Dancing with the Stars." But his stint on the show was short lived, as he was accidentally poked in the eye by his partner, Edyta Sliwinska, during rehearsals and suffered a scratched cornea. Though he competed against doctor's orders, Ross was the first to be eliminated from the show. Meanwhile, he continued to roast a wide swath of celebrities on Comedy Central, including Larry the Cable Guy, Joan Rivers, Donald Trump, David Hasselhoff and Charlie Sheen.

# Jeff Ross
## Filmer
*    Ricky Stanicky       
*    The Roast of James Franco       
*    The Roast of Donald Trump       
*    The Roast of Charlie Sheen       
*    The Roast of Bruce Willis       
*    The Roast Of Justin Bieber       
*    The Roast of Rob Lowe       
*    The Roast of David Hasselhoff       
*    The Roast of William Shatner

# Jeff Ross
## Producent
*    Hot Listings Miami       
*    John Leguizamo: Spic-O-Rama       
*    Jeff Ross Presents: Roast Battle

# Jeff Ross
## Barn och familj
*    The Emoji Movie       
*    Trassel Serien: Drottning för en dag

# Jeff Ross
## Program
*    Jeff Ross Presents: Roast Battle
</excerpt>
### Rank 2 of 31 — 0.43
<excerpt title="TV: 'Roast of David Hasselhoff'">
# TV: "Roast of David Hasselhoff"
WeddingsParentDiningFeaturesArtsHome & StyleNewslettersLegals
Subscribe
MOVIES
Staff Writer
Columbus Alive
Aug. 11, 2010 Updated Aug. 18, 2010, 4:34 p.m. ET
[](mailto:?subject=TV%3A%20%22Roast%20of%20David%20Hasselhoff%22%20-%20from%20Columbus%20Monthly&body=TV%3A%20%22Roast%20of%20David%20Hasselhoff%22%0A%0ANo%20subject%20is%20off%20limits%20during%20Comedy%20Central's%20roasts%2C%20which%20means%20the%20%22Roast%20of%20David%20Hasselhoff%22%20should%20be%20cruel%20and%20hilarious.%20Besides%20being%20on%20two%20of%20the%20campiest%20television%20shows%20of%20all%20time%20-%E2%80%A6%0A%0ACheck%20out%20this%20story%20on%20columbusmonthly.com%3A%20https%3A%2F%2Fwww.columbusmonthly.com%2Fstory%2Fentertainment%2Fmovies%2F2010%2F08%2F11%2Ftv-roast-david-hasselhoff%2F23026019007%2F)
Video 2
Keep Watching

# TV: "Roast of David Hasselhoff"
No subject is off limits during Comedy Central's roasts, which means the "Roast of David Hasselhoff" should be cruel and hilarious. Besides being on two of the campiest television shows of all time - "Knight Rider" and "Baywatch" - the Hoff may be more recognized for his drinking habits and bitter divorce. Greg Giraldo and Jeffrey Ross should have some particularly amusing and nasty barbs for Mr. Ripplepecs.
> "Roast of David Hasselhoff"  
>   
>   
> 10 p.m. Sunday on Comedy Central
[](mailto:?subject=TV%3A%20%22Roast%20of%20David%20Hasselhoff%22%20-%20from%20Columbus%20Monthly&body=TV%3A%20%22Roast%20of%20David%20Hasselhoff%22%0A%0ANo%20subject%20is%20off%20limits%20during%20Comedy%20Central's%20roasts%2C%20which%20means%20the%20%22Roast%20of%20David%20Hasselhoff%22%20should%20be%20cruel%20and%20hilarious.%20Besides%20being%20on%20two%20of%20the%20campiest%20television%20shows%20of%20all%20time%20-%E2%80%A6%0A%0ACheck%20out%20this%20story%20on%20columbusmonthly.com%3A%20https%3A%2F%2Fwww.columbusmonthly.com%2Fstory%2Fentertainment%2Fmovies%2F2010%2F08%2F11%2Ftv-roast-david-hasselhoff%2F23026019007%2F)
</excerpt>
### Rank 3 of 31 — 0.41
<excerpt title="Filmer och TV-program med Jeff Ross">
# Jeff Ross
Hailed by one critic as "the best documentary to emerge so far from the Iraq War," "Patriot Act" proved to be a poignant portrayal of both the Iraq war and the tradition of USO comedy tours made popular by legendary comic Bob Hope.Returning to his offensive nature in 2006, Ross wrote and produced the animated series "Where My Dogs At?" (MTV2). Parodying Hollywood celebrity, the series was centered on Buddy (Ross), a beagle lost on the streets of Hollywood, and his friend Woof (Tracy Morgan), a bulldog. The series was pulled after its first season however, when controversy arose about the depiction of African-American women in the episode "Woofy Loves Snoop," a parody of rapper Snoop Dogg. Undeterred, Ross went on to star in his first stand-up special on Comedy Central, "Jeffrey Ross: No Offense," in 2008. That same year, Ross signed on raise his profile outside the comedy realm by competing on ABC's reality show phenomenon "Dancing with the Stars." But his stint on the show was short lived, as he was accidentally poked in the eye by his partner, Edyta Sliwinska, during rehearsals and suffered a scratched cornea. Though he competed against doctor's orders, Ross was the first to be eliminated from the show. Meanwhile, he continued to roast a wide swath of celebrities on Comedy Central, including Larry the Cable Guy, Joan Rivers, Donald Trump, David Hasselhoff and Charlie Sheen.
MER
</excerpt>
### Rank 4 of 31 — 0.41
<excerpt title="TV: 'Roast of David Hasselhoff'">
# TV: "Roast of David Hasselhoff"
No subject is off limits during Comedy Central's roasts, which means the "Roast of David Hasselhoff" should be cruel and hilarious. Besides being on two of the campiest television shows of all time - "Knight Rider" and "Baywatch" - the Hoff may be more recognized for his drinking habits and bitter divorce. Greg Giraldo and Jeffrey Ross should have some particularly amusing and nasty barbs for Mr. Ripplepecs.
> "Roast of David Hasselhoff"  
>   
>   
> 10 p.m. Sunday on Comedy Central
[](mailto:?subject=TV%3A%20%22Roast%20of%20David%20Hasselhoff%22%20-%20from%20Columbus%20Monthly&body=TV%3A%20%22Roast%20of%20David%20Hasselhoff%22%0A%0ANo%20subject%20is%20off%20limits%20during%20Comedy%20Central's%20roasts%2C%20which%20means%20the%20%22Roast%20of%20David%20Hasselhoff%22%20should%20be%20cruel%20and%20hilarious.%20Besides%20being%20on%20two%20of%20the%20campiest%20television%20shows%20of%20all%20time%20-%E2%80%A6%0A%0ACheck%20out%20this%20story%20on%20columbusmonthly.com%3A%20https%3A%2F%2Fwww.columbusmonthly.com%2Fstory%2Fentertainment%2Fmovies%2F2010%2F08%2F11%2Ftv-roast-david-hasselhoff%2F23026019007%2F)

# TV: "Roast of David Hasselhoff"
[새벽 2시간마다 깨는 ”갱년기 불면증“.. 부족한 "이것'' 때문?! 원인부터 종결시킨 [세계특허]여성갱년기 멀티케어 [리피어라] 국내유일 21중 최다기능성으로 갱년기 모든증상 한번에! 국제 특허 획득 'MS-10' 성분으로 화제!리피어라 - 갱년기 특허성분 MS-10 | AdAd](https://healyj.kr/rpta43 "새벽 2시간마다 깨는 ”갱년기 불면증“.. 부족한 \"이것'' 때문?! 원인부터 종결시킨 [세계특허]")
Undo
[갱년기 후끈거림에 직빵! 먹자마자 '열감’ 싹~! 세계특허 '이것‘[국내유일 21중 최다기능성 리피어라] 5년연속1위, 브랜드대상 10관왕!리피어라 - 갱년기 특허성분 MS-10 | AdAd 더 알아보기](https://healyj.kr/rpta46 "갱년기 후끈거림에 직빵! 먹자마자 '열감’ 싹~! 세계특허 '이것‘")
Undo
프랑스 여성이 살안찌는 이유? 유학가서 알아온 비밀 하루의 일기장 | [AdAd 더 알아보기](https://slimnote.kr/wmh27sa8 "프랑스 여성이 살안찌는 이유? 유학가서 알아온 비밀")
Undo
[[화제] 이제 파란약 몰래 안챙겨요. 40대 실제 극복기 홍조 오고 두통 올까봐 무서워 쪼개 먹던 과거 끝. '이거' 1알로 20대 광명 찾은 썰 풉니다.김차장의 이중생활 | AdAd 더 알아보기](https://blog-roan-pi.vercel.app/post/6ae831a483f79274a793f2e1 "[화제] 이제 파란약 몰래 안챙겨요. 40대 실제 극복기")
Undo
</excerpt>
### Rank 5 of 31 — 0.32
<excerpt title="The Roast Of David Hasselhoff Writer">
# The Roast Of David Hasselhoff Writer
Log In
Sign Up
Watch reels about the roast of david hasselhoff writer from people around the world.
[[](https://www.instagram.com/davidfinkelstein770) davidfinkelst... 99 Repost from pumpkin.escobar13 • From the Comedy Central Roast of David Hasselhoff (2010) #gilbertgottfried #pamelaanderson #davidhasselhoff #standup #standupcomedy #comedyroast #comedy #comedyreels #comedyvideos #funny #funnyreels #funnyvideos](https://www.instagram.com/reel/C5XX3E-uueX/?utm_source=popular_topic_grid)
[[](https://www.instagram.com/davidhasselhoff) davidhasselhoff Live auction begins tomorrow at 9am PST! Bidding is open now, link in bio! #DavidHasselhoff #TheHoff #TheHoffAuction #Auction #LiveAuction #Bidding #LiveAuctioneers #DiligentEstateSales #SpongeBob #KnightRider #MichaelKnight #KITT #Baywatch #MitchBuchannon #Lifeguard #80s #90s #Memorabilia](https://www.instagram.com/reel/CKXaXNMB0zC/?utm_source=popular_topic_grid)
[[](https://www.instagram.com/kleinezeitung) kleinezeitung 41.9K Und? Wie ist das bei euch so?😂 TV-Legende David Hasselhoff war gestern in Graz, um seine Tour 2023 zu präsentieren. Drei Termine wird es in Österreich geben, einen in Schladming, in Wien und in Graz. Alle Infos und Details des Interviews findet ihr auf unserer Website und in unseren Story-Highlights! #hasselhoff #thehoff #baywatch #knightrider #davidhasselhoff #graz #wien #stmk #österreich #musik #tournee #tour #entertainment #klz (David Hasselhoff getroffen: ✅)](https://www.instagram.com/reel/Cj79V9To2qv/?utm_source=popular_topic_grid)

# The Roast Of David Hasselhoff Writer
[[](https://www.instagram.com/davidhasselhoff) davidhasselhoff So happy to be sharing new music with you! My new single "The Passenger" is out and you can pre-order my new album "Party Your Hasselhoff" which will be out Sep. 3rd. Link in bio! @schubertmusicofficial @restless.records @the_orchard_ @abglanzentertainment #partyyourhasselhoff #davidhasselhoff #thehoff #thepassenger](https://www.instagram.com/reel/CQiLnGhhscJ/?utm_source=popular_topic_grid)
[[](https://www.instagram.com/standuprizz) standuprizz 773K David Spade ROASTS Rob Lowe 🔥😱🤣 Comedy Central Roast of Rob Lowe (2016) Comedian: @davidspade 🐐 🔥 Follow @standuprizz for more stand up content‼️ 👍 Leave a like, if you enjoyed the video. #standupgeniuses #genius #comedy #standup #standupcomedy #comedian #jokes #comedyvideos #roast #comedycentral #davidspade #roblowe](https://www.instagram.com/reel/C4oJcDUSr_L/?utm_source=popular_topic_grid)
[[](https://www.instagram.com/tom.adelsbach) tom.adelsbach 7.2M And now, more fun with Donny and the Mic ;) (SOUND UP)](https://www.instagram.com/reel/DHSP4ntPg-8/?utm_source=popular_topic_grid)
[[](https://www.instagram.com/laboursofhercule) laboursofhercule 81.9K We might be biased, but David Suchet wins this trend 😍](https://www.instagram.com/reel/DV_kB_ZhgpD/?utm_source=popular_topic_grid)
</excerpt>

## Search 5 — query: ""The Roast of David Hasselhoff" writer credited"
### Rank 1 of 100 — 0.77 (passed on)
<excerpt title="Tom Johnson, 'The Daily Show' and 'The Jeselnik Offensive' Writer, Dies ...">
Tom Johnson, a writer and stand-up comic with credits including “The Daily Show” and “The Jeselnik Offensive,” has died at the age of 55.
In a statement Friday, his family said he died at his home “Peacefully and unexpectedly” on Jan. 14. No cause of death has been made public.
“Growing up,” the family wrote in their statement, Johnson “had an insatiable curiosity. He was talented in all of the arts: a gifted artist who could draw in vivid detail, played the guitar and trombone, and acted in plays throughout college at the University of Missouri. He loved the band Kiss and enjoyed dressing up like the lead singer for Halloween.”
“Tom had a huge heart and cared deeply about taking care of others. He launched the careers of countless successful comedians. His work ethic was impeccable. He was fair, kind, talented, inclusive, and funny as hell. He was a voracious reader, eater, and rescuer of cats. It brought him great joy to play pranks on those he loved. He will be truly missed by all,” the family statement said also.
Johnson’s death was first revealed on the “WTF with Marc Maron” podcast on Thursday, which he served as executive producer and head writer on in 2010, according to his LinkedIn.
“I knew him back when he did comedy briefly. He was actually at the Comedy Cellar before me and then he became a writer for The Daily Show. This is the pre – Jon Stewart incarnation of ‘The Daily Show’ and that’s sort of how he came to Air America. He started Air America with me but Lizz Winstead, who was at the original ‘Daily Show,’ pulled Tom in as a writer and that’s where we re-met,” Maron said. “He was f—ing hilarious, like inspired as a writer but also as a performer, and he wrote so many amazing bits for us that he did on the radio.”
Johnson began working on the Comedy Central late night program as a writer and performer in May 1996 and worked on the show through January 2004. He wrote on more than 1200 episodes and won two Emmy Awards and two Peabody Awards for his work on the show.

His other credits at the network include co-executive producer and head writer on “Stand Up Nation With Greg Giraldo,” “Adult Content with Greg Giraldo,” and “Reality Bites,”a writer on the roast of David Hasselhoff and head writer on the roast of Roseanne, an executive producer and head writer on “Midnight with Anthony Jeselnik,” co-creator, executive producer and head writer on “The Jeselnik Offensive,” and a writer on “NSFW with Nikki Glaser.”
Outside of Comedy Central, he worked as a head writer and supervising producer on Game Show Network’s “Late Night Liars,” head writer and producer on Fox Broadcasting’s “Talkshow with Spike Feresten,” head writer on Spike TV’s 2010, 2012, 2014, 2015 and 2016 Guys Choice Awards and Scream Awards 2011, the 2016 MTV Music Video Awards, IFC’s Make Me Understand and Zynga’s “Words with Friends Live!,” head writer and producer on TBS’ “Lopez Tonight,” and a writer and supervising producer on MTV’s “Gamekillers.”
Additionally, Johnson served as a writer producer on HBO’s “Savage Love,” a writer on Bravo’s “Straight Talk with Joan Rivers,” A&E Television’s “Balls of Steel,” VH1’s “Best Week Ever,” MTV’s “Race Riot,” Spike TV’s 2009 Video Game Awards, Viacom’s “Martha & Snoop’s Potluck Challenge,”and Quibi’s “Nice One With Ron Funches,” head consultant on the 2014 MTV Music Video Awards, a consultant on Syfy’s “Reactor” and Fox Broadcasting’s “The All-Star Dog Rescue Celebration,” and head consultant, writer and producer on 2020’s NBA All-Star Roast.
Johnson is survived by his wife Rozie Bacchi and his sisters, brothers-in-law, nieces and their families.
</excerpt>
### Rank 2 of 100 — 0.76
<excerpt title="Tom Johnson, 'The Daily Show' and 'The Jeselnik Offensive' Writer, Dies ...">
Tom Johnson, a writer and stand-up comic with credits including "The Daily Show" and "The Jeselnik Offensive," has died at the age of 55.
In a statement Friday, his family said he died at his home "Peacefully and unexpectedly" on Jan. 14. No cause of death has been made public.
"Growing up," the family wrote in their statement, Johnson "had an insatiable curiosity. He was talented in all of the arts: a gifted artist who could draw in vivid detail, played the guitar and trombone, and acted in plays throughout college at the University of Missouri. He loved the band Kiss and enjoyed dressing up like the lead singer for Halloween."
"Tom had a huge heart and cared deeply about taking care of others. He launched the careers of countless successful comedians. His work ethic was impeccable. He was fair, kind, talented, inclusive, and funny as hell. He was a voracious reader, eater, and rescuer of cats. It brought him great joy to play pranks on those he loved. He will be truly missed by all," the family statement said also.
Johnson's death was first revealed on the "WTF with Marc Maron" podcast on Thursday, which he served as executive producer and head writer on in 2010, according to his LinkedIn.
"I knew him back when he did comedy briefly. He was actually at the Comedy Cellar before me and then he became a writer for The Daily Show. This is the pre – Jon Stewart incarnation of 'The Daily Show' and that's sort of how he came to Air America. He started Air America with me but Lizz Winstead, who was at the original 'Daily Show,' pulled Tom in as a writer and that's where we re-met," Maron said. "He was f—ing hilarious, like inspired as a writer but also as a performer, and he wrote so many amazing bits for us that he did on the radio."
Johnson began working on the Comedy Central late night program as a writer and performer in May 1996 and worked on the show through January 2004. He wrote on more than 1200 episodes and won two Emmy Awards and two Peabody Awards for his work on the show.

His other credits at the network include co-executive producer and head writer on "Stand Up Nation With Greg Giraldo," "Adult Content with Greg Giraldo," and "Reality Bites,"a writer on the roast of David Hasselhoff and head writer on the roast of Roseanne, an executive producer and head writer on "Midnight with Anthony Jeselnik," co-creator, executive producer and head writer on "The Jeselnik Offensive," and a writer on "NSFW with Nikki Glaser."
Outside of Comedy Central, he worked as a head writer and supervising producer on Game Show Network's "Late Night Liars," head writer and producer on Fox Broadcasting's "Talkshow with Spike Feresten," head writer on Spike TV's 2010, 2012, 2014, 2015 and 2016 Guys Choice Awards and Scream Awards 2011, the 2016 MTV Music Video Awards, IFC's Make Me Understand and Zynga's "Words with Friends Live!," head writer and producer on TBS' "Lopez Tonight," and a writer and supervising producer on MTV's "Gamekillers."
Additionally, Johnson served as a writer producer on HBO's "Savage Love," a writer on Bravo's "Straight Talk with Joan Rivers," A&E Television's "Balls of Steel," VH1's "Best Week Ever," MTV's "Race Riot," Spike TV's 2009 Video Game Awards, Viacom's "Martha & Snoop's Potluck Challenge,"and Quibi's "Nice One With Ron Funches," head consultant on the 2014 MTV Music Video Awards, a consultant on Syfy's "Reactor" and Fox Broadcasting's "The All-Star Dog Rescue Celebration," and head consultant, writer and producer on 2020's NBA All-Star Roast.
Johnson is survived by his wife Rozie Bacchi and his sisters, brothers-in-law, nieces and their families.
The post Tom Johnson, 'The Daily Show' and 'The Jeselnik Offensive' Writer, Dies at 55 appeared first on TheWrap.
</excerpt>
### Rank 3 of 100 — 0.60
<excerpt title="Seth MacFarlane">
## Career
### Television career
#### Television hosting
MacFarlane has participated in the Comedy Central Roasts. MacFarlane is the only person to serve as roastmaster for more than one roast. In 2010, he filled this role for the roast of David Hasselhoff.[[88]](https://en.wikipedia.org/wiki/Seth_MacFarlane#cite_note-88) The following year he was roastmaster at the roasts of Donald Trump and Charlie Sheen.

## Career
### Television career
#### Television hosting
On October 1, 2012, it was announced that MacFarlane would host the 85th Academy Awards on February 24, 2013.[[89]](https://en.wikipedia.org/wiki/Seth_MacFarlane#cite_note-89)[[90]](https://en.wikipedia.org/wiki/Seth_MacFarlane#cite_note-abcmedianet20121012-90)[[91]](https://en.wikipedia.org/wiki/Seth_MacFarlane#cite_note-91) He presented the nominees with actress Emma Stone, on January 10, 2013. In addition to hosting, MacFarlane was nominated in the Academy Award for Best Original Song category for co-writing the theme song "Everybody Needs a Best Friend" for his film _Ted_ with Walter Murphy.[[92]](https://en.wikipedia.org/wiki/Seth_MacFarlane#cite_note-Oscars-92) Critical response to MacFarlane's performance was mixed. Columnist Owen Gleiberman of _Entertainment Weekly_ commented "By calling constant attention to the naughty factor," MacFarlane created "an echo chamber of outrage, working a little too hard to top himself with faux-scandalous gags about race, Jews in Hollywood, and the killing of Abraham Lincoln."[[93]](https://en.wikipedia.org/wiki/Seth_MacFarlane#cite_note-93) Tim Goodman of _The Hollywood Reporter_ praised MacFarlane's performance saying that he did "impressively better than one would have wagered". He noted that he added "plenty of niceties with a little bit of the Ricky Gervais bite-the-hand-that-feeds-you thing and worked the juxtaposition rather nicely".[[94]](https://en.wikipedia.org/wiki/Seth_MacFarlane#cite_note-94) He stirred up controversy in the form of a musical number titled "We Saw Your Boobs".[[95]](https://en.wikipedia.org/wiki/Seth_MacFarlane#cite_note-95)

## Career
### Television career
#### Television hosting
On October 29, 2014, it was announced that MacFarlane would host the Breakthrough Prize ceremony. The event was held in Silicon Valley and televised on November 15, 2014, on Discovery Channel and Science, and globally on November 22, 2014, on BBC World News.[[96]](https://en.wikipedia.org/wiki/Seth_MacFarlane#cite_note-96) He returned to host the following year.[[97]](https://en.wikipedia.org/wiki/Seth_MacFarlane#cite_note-97)
</excerpt>
### Rank 4 of 100 — 0.59
<excerpt title="Seth MacFarlane">
## References
87.   ↑"'Grinder', 'Grandfathered', 'Bordertown' & 'Cooper Barrett' Canceled By Fox After One Season". _Deadline_. May 13, 2016. Archived from the original on May 13, 2016. Retrieved May 13, 2016.  
88.   ↑"Seth MacFarlane will lead David Hasselhoff Roast". July 21, 2010. Archived from the original on September 20, 2020. Retrieved October 1, 2013.  
89.   ↑"Seth MacFarlane to Host 85th Oscars" (Press release). AMPAS. October 1, 2012. Archived from the original on September 5, 2014. Retrieved October 17, 2012.  
90.   ↑"SETH MACFARLANE TO HOST 85TH OSCARS®, AIRING LIVE ON ABC, SUNDAY, FEBRUARY 24, 2013". _ABC Media Net_. American Broadcasting Company. October 11, 2012. Archived from the original on January 14, 2013. Retrieved October 11, 2012.  
91.   ↑Bahr, Lindsey (October 1, 2012). "Seth MacFarlane to host the Oscars – BREAKING". Entertainment Weekly. Archived from the original on September 25, 2015. Retrieved February 26, 2013.  
92.   12Morgan, David (January 10, 2013). ""Lincoln," "Life of Pi" lead Oscar race". _CBS News_. CBS Corporation. Archived from the original on March 13, 2014. Retrieved October 7, 2013.  
93.   ↑Gleiberman, Owen (February 25, 2013). "This year's Academy Awards: a lively, occasionally uneasy mixture of snark and sincerity". _Entertainment Weekly_. Archived from the original on June 11, 2020. Retrieved March 3, 2020.
</excerpt>
### Rank 5 of 100 — 0.49
<excerpt title="Seth MacFarlane">
## Career
### Television career
#### Television producing
MacFarlane in 2012
MacFarlane was the executive producer of a live-action sitcom starring Rob Corddry called _The Winner_.[[76]](https://en.wikipedia.org/wiki/Seth_MacFarlane#cite_note-76) The show ran on Fox for six episodes in Spring 2007.[[77]](https://en.wikipedia.org/wiki/Seth_MacFarlane#cite_note-77)[[78]](https://en.wikipedia.org/wiki/Seth_MacFarlane#cite_note-78)
In August 2011, Fox ordered a 13-part updated series of _Cosmos: A Spacetime Odyssey_. MacFarlane co-produced the series with Ann Druyan and Steven Soter. The series is hosted by Neil deGrasse Tyson and began airing on the channel in March 2014, with repeats airing on the National Geographic Channel on the next night.[[79]](https://en.wikipedia.org/wiki/Seth_MacFarlane#cite_note-79) In addition to serving as one of the executive producers, MacFarlane provided voices for characters during the animated portions of the series. MacFarlane returned to executive produce and provide voices to its sequel series, _Cosmos: Possible Worlds_, which aired in 2020.[[80]](https://en.wikipedia.org/wiki/Seth_MacFarlane#cite_note-80)
In 2013 and 2014, MacFarlane produced one season of a live-action sitcom called _Dads_.[[81]](https://en.wikipedia.org/wiki/Seth_MacFarlane#cite_note-Fox_2014_Cancellations-81) The series, revolves around Eli, played by Seth Green, and Warner, played by Giovanni Ribisi, two successful guys in their 30s whose world is turned upside down when their dads move in with them. MacFarlane, Alec Sulkin and Wellesley Wild executive-produced the series, with Sulkin and Wild writing.[[82]](https://en.wikipedia.org/wiki/Seth_MacFarlane#cite_note-Kenneally-82)

## Career
### Television career
#### Television producing
In 2014, MacFarlane executive produced a two-season, 20-episode series called _Blunt Talk_ for Starz.[[83]](https://en.wikipedia.org/wiki/Seth_MacFarlane#cite_note-variety-83)[[84]](https://en.wikipedia.org/wiki/Seth_MacFarlane#cite_note-84)[[85]](https://en.wikipedia.org/wiki/Seth_MacFarlane#cite_note-85)
In 2009, MacFarlane began work on the animated series _Bordertown_.[[86]](https://en.wikipedia.org/wiki/Seth_MacFarlane#cite_note-Bordertown_Announcement-86) The series is set in Texas and follows a border patrol agent and a Mexican immigrant, satirizing America's changing cultural landscape. It ran for 13 episodes in the first half of 2016, on Fox.[[87]](https://en.wikipedia.org/wiki/Seth_MacFarlane#cite_note-deadline-btcancelled-87)

## Career
### Television career
#### Television hosting
MacFarlane has participated in the Comedy Central Roasts. MacFarlane is the only person to serve as roastmaster for more than one roast. In 2010, he filled this role for the roast of David Hasselhoff.[[88]](https://en.wikipedia.org/wiki/Seth_MacFarlane#cite_note-88) The following year he was roastmaster at the roasts of Donald Trump and Charlie Sheen.
</excerpt>

## Search 6 — query: "Tom Johnson writer roast of David Hasselhoff"
### Rank 1 of 31 — 0.75 (passed on)
<excerpt title="Tom Johnson, 'The Daily Show' and 'The Jeselnik Offensive' Writer, Dies ...">
Tom Johnson, a writer and stand-up comic with credits including “The Daily Show” and “The Jeselnik Offensive,” has died at the age of 55.
In a statement Friday, his family said he died at his home “Peacefully and unexpectedly” on Jan. 14. No cause of death has been made public.
“Growing up,” the family wrote in their statement, Johnson “had an insatiable curiosity. He was talented in all of the arts: a gifted artist who could draw in vivid detail, played the guitar and trombone, and acted in plays throughout college at the University of Missouri. He loved the band Kiss and enjoyed dressing up like the lead singer for Halloween.”
“Tom had a huge heart and cared deeply about taking care of others. He launched the careers of countless successful comedians. His work ethic was impeccable. He was fair, kind, talented, inclusive, and funny as hell. He was a voracious reader, eater, and rescuer of cats. It brought him great joy to play pranks on those he loved. He will be truly missed by all,” the family statement said also.
Johnson’s death was first revealed on the “WTF with Marc Maron” podcast on Thursday, which he served as executive producer and head writer on in 2010, according to his LinkedIn.
“I knew him back when he did comedy briefly. He was actually at the Comedy Cellar before me and then he became a writer for The Daily Show. This is the pre – Jon Stewart incarnation of ‘The Daily Show’ and that’s sort of how he came to Air America. He started Air America with me but Lizz Winstead, who was at the original ‘Daily Show,’ pulled Tom in as a writer and that’s where we re-met,” Maron said. “He was f—ing hilarious, like inspired as a writer but also as a performer, and he wrote so many amazing bits for us that he did on the radio.”
Johnson began working on the Comedy Central late night program as a writer and performer in May 1996 and worked on the show through January 2004. He wrote on more than 1200 episodes and won two Emmy Awards and two Peabody Awards for his work on the show.

His other credits at the network include co-executive producer and head writer on “Stand Up Nation With Greg Giraldo,” “Adult Content with Greg Giraldo,” and “Reality Bites,”a writer on the roast of David Hasselhoff and head writer on the roast of Roseanne, an executive producer and head writer on “Midnight with Anthony Jeselnik,” co-creator, executive producer and head writer on “The Jeselnik Offensive,” and a writer on “NSFW with Nikki Glaser.”
Outside of Comedy Central, he worked as a head writer and supervising producer on Game Show Network’s “Late Night Liars,” head writer and producer on Fox Broadcasting’s “Talkshow with Spike Feresten,” head writer on Spike TV’s 2010, 2012, 2014, 2015 and 2016 Guys Choice Awards and Scream Awards 2011, the 2016 MTV Music Video Awards, IFC’s Make Me Understand and Zynga’s “Words with Friends Live!,” head writer and producer on TBS’ “Lopez Tonight,” and a writer and supervising producer on MTV’s “Gamekillers.”
Additionally, Johnson served as a writer producer on HBO’s “Savage Love,” a writer on Bravo’s “Straight Talk with Joan Rivers,” A&E Television’s “Balls of Steel,” VH1’s “Best Week Ever,” MTV’s “Race Riot,” Spike TV’s 2009 Video Game Awards, Viacom’s “Martha & Snoop’s Potluck Challenge,”and Quibi’s “Nice One With Ron Funches,” head consultant on the 2014 MTV Music Video Awards, a consultant on Syfy’s “Reactor” and Fox Broadcasting’s “The All-Star Dog Rescue Celebration,” and head consultant, writer and producer on 2020’s NBA All-Star Roast.
Johnson is survived by his wife Rozie Bacchi and his sisters, brothers-in-law, nieces and their families.
</excerpt>
### Rank 2 of 31 — 0.75
<excerpt title="Tom Johnson, 'The Daily Show' and 'The Jeselnik Offensive' Writer, Dies ...">
Tom Johnson, a writer and stand-up comic with credits including "The Daily Show" and "The Jeselnik Offensive," has died at the age of 55.
In a statement Friday, his family said he died at his home "Peacefully and unexpectedly" on Jan. 14. No cause of death has been made public.
"Growing up," the family wrote in their statement, Johnson "had an insatiable curiosity. He was talented in all of the arts: a gifted artist who could draw in vivid detail, played the guitar and trombone, and acted in plays throughout college at the University of Missouri. He loved the band Kiss and enjoyed dressing up like the lead singer for Halloween."
"Tom had a huge heart and cared deeply about taking care of others. He launched the careers of countless successful comedians. His work ethic was impeccable. He was fair, kind, talented, inclusive, and funny as hell. He was a voracious reader, eater, and rescuer of cats. It brought him great joy to play pranks on those he loved. He will be truly missed by all," the family statement said also.
Johnson's death was first revealed on the "WTF with Marc Maron" podcast on Thursday, which he served as executive producer and head writer on in 2010, according to his LinkedIn.
"I knew him back when he did comedy briefly. He was actually at the Comedy Cellar before me and then he became a writer for The Daily Show. This is the pre – Jon Stewart incarnation of 'The Daily Show' and that's sort of how he came to Air America. He started Air America with me but Lizz Winstead, who was at the original 'Daily Show,' pulled Tom in as a writer and that's where we re-met," Maron said. "He was f—ing hilarious, like inspired as a writer but also as a performer, and he wrote so many amazing bits for us that he did on the radio."
Johnson began working on the Comedy Central late night program as a writer and performer in May 1996 and worked on the show through January 2004. He wrote on more than 1200 episodes and won two Emmy Awards and two Peabody Awards for his work on the show.

His other credits at the network include co-executive producer and head writer on "Stand Up Nation With Greg Giraldo," "Adult Content with Greg Giraldo," and "Reality Bites,"a writer on the roast of David Hasselhoff and head writer on the roast of Roseanne, an executive producer and head writer on "Midnight with Anthony Jeselnik," co-creator, executive producer and head writer on "The Jeselnik Offensive," and a writer on "NSFW with Nikki Glaser."
Outside of Comedy Central, he worked as a head writer and supervising producer on Game Show Network's "Late Night Liars," head writer and producer on Fox Broadcasting's "Talkshow with Spike Feresten," head writer on Spike TV's 2010, 2012, 2014, 2015 and 2016 Guys Choice Awards and Scream Awards 2011, the 2016 MTV Music Video Awards, IFC's Make Me Understand and Zynga's "Words with Friends Live!," head writer and producer on TBS' "Lopez Tonight," and a writer and supervising producer on MTV's "Gamekillers."
Additionally, Johnson served as a writer producer on HBO's "Savage Love," a writer on Bravo's "Straight Talk with Joan Rivers," A&E Television's "Balls of Steel," VH1's "Best Week Ever," MTV's "Race Riot," Spike TV's 2009 Video Game Awards, Viacom's "Martha & Snoop's Potluck Challenge,"and Quibi's "Nice One With Ron Funches," head consultant on the 2014 MTV Music Video Awards, a consultant on Syfy's "Reactor" and Fox Broadcasting's "The All-Star Dog Rescue Celebration," and head consultant, writer and producer on 2020's NBA All-Star Roast.
Johnson is survived by his wife Rozie Bacchi and his sisters, brothers-in-law, nieces and their families.
The post Tom Johnson, 'The Daily Show' and 'The Jeselnik Offensive' Writer, Dies at 55 appeared first on TheWrap.
</excerpt>
### Rank 3 of 31 — 0.69
<excerpt title="Comedy Central Roast of David Hasselhoff DVD Review">
**Comedy Central Roast of David Hasselhoff (2010)**
Special & DVD Details **Executive Producers**: Joel Gallen (also director), Larry Thompson / **Writers**: Ray James, Josh Comers, Anthony Jesselnik, Tom Johnson, David Feldman, Roger Rittenhouse, Steve Rosenfield, Corinne Marshall, Mike Ferrucci / **Additional Material**: Aaron Lee, Patrick Meighan, John Viener **Roastee**: David Hasselhoff / **Roastmaster**: Seth MacFarlane / **Roasters**: Pamela Anderson, Jeffrey Ross, Greg Giraldo, Jerry Springer, George Hamilton, Whitney Cummings, Hulk Hogan, Gilbert Gottfried, Lisa Lampanelli / **Also Featuring**: Sharon Osborne, Piers Morgan, William Daniels (voice of KITT) **Running Time**: 72 Minutes (Extended Version) / **Rating**: Not Rated (Broadcast Version TV-MA)   
1.78:1 Anamorphic Widescreen, Dolby Stereo 2.0 (English)
Subtitles: None; Special and Extras Closed Captioned
Original Airdate: August 15, 2010 / Roast Date: August 1, 2010
DVD Release Date: January 11, 2011 / Suggested Retail Price: $16.99
Single-sided, single-layered disc (DVD-5) / Black Eco-Friendly Keepcase
Is it just me or are roasts the worst? I know that it is a long, celebrated tradition for comedians to gather together and say terrible things about one another,

but it's that kind of negativity that turns me away from stand-up even though some of my favorite entertainers made their names there.   
While roasts used to either be televised and tame or private and vulgar, Comedy Central has bridged the gap by making them both televised and vulgar. The cable network began producing and airing the New York Friars' Club's annual roasts in 1998. After five years of that, Comedy Central started creating their own roasts in the same spirit. Hardly a year has passed without the network roasting a celebrity, some of them comedians (Denis Leary, Jeff Foxworthy, Bob Saget, Larry the Cable Guy) and others less so. Adding to the latter class is **_Comedy Central Roast of David Hasselhoff_**. Having debuted last August, this most recent special now comes to DVD extended and uncensored on January 11th, allowing the "Knight Rider" actor, international singer, "America's Got Talent" judge, and reliable joke punchline to join the ranks of Comedy Central roastees like William Shatner, Flavor Flav, and his "Baywatch" co-star Pamela Anderson.
Anderson is on hand as the most relevant roaster of the program, on which "Family Guy" creator Seth MacFarlane serves as roastmaster. Other speakers include comedians and regular roasters Jeffrey Ross, Lisa Lampanelli, Whitney Cummings, and the recently deceased Greg Giraldo. Rounding out the eclectic group are Hulk Hogan, "Talent" colleague Jerry Springer, longtime actor George Hamilton, and Gilbert Gottfried.
Going by my limited exposure to Comedy Central roasts, I would deem this a fairly typical one. Each roaster chooses obvious targets while going after one another, such as MacFarlane's debt to "The Simpsons", Hamilton's age and signature tan, Springer's brand of sleaze, Lampanelli's weight and apparent predilection for black men, and the less famous folks' general obscurity. Hasselhoff, who ascends to the stage with a performance of "Hooked on a Feeling" and signs off with "This is the Moment" from his Broadway debut _Jekyll & Hyde_, barely gets more notice than the others. The comedic goldmines that are his career, personas, and personal life are widely traversed. Naturally, his battle with alcoholism emblemized by his 2007 drunken shirtless burger-eating viral video is repeatedly ridiculed.
</excerpt>
### Rank 4 of 31 — 0.25
<excerpt title="Comedy Central Roast">
## Awards and nominations
73.   ↑"Roast of Mike King | Show | Comedy Central New Zealand". Comedycentral.co.nz. November 23, 2010. Archived from the original on November 2, 2011. Retrieved October 24, 2011.  
74.   ↑Mingo, Alicia (February 22, 2019). "José Mota se enfrenta a 'El Roast' de Comedy Central el domingo 24". _Diez Minutos_.  
75.   ↑Shanfeld, Ethan (May 12, 2026). "Paul McCartney Turned Down His Own Netflix Roast (EXCLUSIVE)". _Variety_. Retrieved July 16, 2026.  
76.   ↑Black, Chris (May 14, 2026). "The Kevin Hart Roast Was Proof that Celebrity Roasts are Cooked". _GQ_. Retrieved July 16, 2026.  
77.   ↑Creaham, Danica (May 5, 2024). "How to watch 'The Roast of Tom Brady' live on Netflix tonight". _Yahoo Sports_. Retrieved July 16, 2026.

## Awards and nominations
*   _Comedy Central Roasts_ at IMDb  
*   _Comedy Central Roast of Denis Leary_ at IMDb  
*   _Comedy Central Roast of Jeff Foxworthy_ at IMDb  
*   _Comedy Central Roast of Pamela Anderson_ at IMDb  
*   _Comedy Central Roast of William Shatner_ at IMDb  
*   _Comedy Central Roast of Flavor Flav_ at IMDb  
*   _Comedy Central Roast of Bob Saget_ at IMDb  
*   _Comedy Central Roast of Larry the Cable Guy_ at IMDb  
*   _Comedy Central Roast of Joan Rivers_ at IMDb  
*   _Comedy Central Roast of David Hasselhoff_ at IMDb  
*   _Comedy Central Roast of Donald Trump_ at IMDb  
*   _Comedy Central Roast of Charlie Sheen_ at IMDb  
*   _Comedy Central Roast of Roseanne Barr_ at IMDb  
*   _Comedy Central Roast of James Franco_ at IMDb  
*   _Comedy Central Roast of Justin Bieber_ at IMDb  
*   _Comedy Central Roast of Rob Lowe_ at IMDb  
*   _Comedy Central Roast of Bruce Willis_ at IMDb  
*   _Comedy Central Roast of Alec Baldwin_ at IMDb  
*   Most Savage Roasts and Jokes List That Will Shut All Jerks Up
</excerpt>
### Rank 5 of 31 — 0.20
<excerpt title="Comedy Central Roast">
## Awards and nominations
10.   ↑"Comedy Central to Cut Paul Walker Jokes From Justin Bieber Roast Broadcast". _Vanity Fair_. March 16, 2015.  
11.   ↑Fitzgerald, Toni. "So everyone shows up to roast Denis Leary". _Media Life Magazine_. Archived from the original on October 6, 2014. Retrieved October 6, 2014.  
12.   ↑Lisa, de Moraes (March 16, 2011). ["Comedy Central roasts Donald Trump [Updated with ratings]"](https://www.washingtonpost.com/blogs/tv-column/post/comedy-central-roasts-donald-trump/2011/03/16/ABIDjrd_blog.html). _The Washington Post_. Retrieved October 6, 2014.  
13.   123Levine, Stuart (August 11, 2009). "Joan Rivers' roast dips in ratings". _Variety_. Retrieved October 6, 2014.  
14.   ↑Heffernan, Virginia (August 13, 2005). "Roasters of 'Stacked' Star Romp High to Low". _The New York Times_. Retrieved April 13, 2015.  
15.   ↑"Wednesday, August 23rd, 2006". Cynopsis Media. August 26, 2006. Retrieved October 6, 2014.  
16.   12"The Comedy Central Roast of William Shatner". Academy of Television Arts & Sciences. Retrieved January 22, 2015.  
17.   ↑Skene, Traci; Mckim, Brian (August 16, 2007). "Jeff Ross roasts Flavor Flav CORRECTION". _Shecky Magazine_. Retrieved October 6, 2014.  
18.   ↑Multi Channel News Staff (August 19, 2008). "Comedy Central Fans Applaud Saget Roast". _Multichannel News_. Retrieved October 6, 2014.  

## Awards and nominations
19.   ↑Tobey, Matt (July 14, 2008). "BREAKING: John Stamos Announced as Bob Saget Roast Master!'". ccinsider.comedycentral.com. Archived from the original on July 25, 2008. Retrieved July 26, 2008.  
20.   ↑"YouTube". YouTube. Archived from the original on June 11, 2014. Retrieved May 17, 2014.  
21.   ↑"Norm MacDonald Interview: Part 2". _The Big Lead_. The Big Lead. April 30, 2011. Retrieved May 17, 2014.  
22.   ↑Daly, Sean (August 4, 2008). "Bob Saget Roast 'Over the Top'". _New York Post_. Retrieved August 24, 2010.  
23.   ↑Official siteArchived February 21, 2009, at the Wayback Machine  
24.   ↑"Comedy Central to Roast Comedic Icon Joan Rivers". _The Futon Critic_. April 8, 2009. Retrieved January 22, 2015.  
25.   ↑Szalai, Georg (August 15, 2010). "David Hasselhoff roast a ratings hit". _The Hollywood Reporter_. Retrieved October 6, 2014.  
26.   ↑"Show Tracker". _Los Angeles Times_. July 21, 2010.  
27.   ↑Meet the Roasters | The Comedy Central Roast of David Hasselfhoff | ComedyCentral.comArchived July 31, 2010, at the Wayback Machine  
28.   ↑_The Comedy Central Roast of David Hasselhoff_; Comedy Central; August 15, 2010
</excerpt>

## Search 7 — query: "Tom Johnson executive producer 2007 television series"
### Rank 1 of 44 — 0.77 (passed on)
<excerpt title="Tom Johnson, 'The Daily Show' Writer, Dies at 55">
# Tom Johnson, ‘The Daily Show’ Writer, Dies at 55
## Related Stories
### Here's How to Watch WWE Crown Jewel 2026 Live Online


# Tom Johnson, ‘The Daily Show’ Writer, Dies at 55
## Related Stories
### Nike Releases New Jordan Spiz'ike Low 'Jam Central' Sneakers: Here’s Where To Shop a Pair Online
Johnson served as head writer for “Talk Show With Spike Feresten” from 2007 to 2009, and later worked as head writer on “Lopez Tonight.” He co-created “The Jeselnik Offensive” with Anthony Jeselnik, where Johnson served as an executive producer and head writer. Even after his death, Johnson is still banned from New Zealand because of a sketch that appeared on “The Jeselnik Offensive.”
Johnson’s other television writing credits include the Grammy Awards, “Comedy Central Roast,” the MTV Movie Awards, “Inside the NBA All-Star Roast” and more. He was one of the authors of the New York Times bestseller “America: The Book.”
Johnson was born Thomas Martin Johnson in Fairfax, Va., on July 25, 1968, to Thomas and Billie Johnson. He began his comedy career after graduating from the University of Missouri and founded the Network Comedy Troupe, where he served as writer, director and mentor.
As a touring comedian, Johnson performed at venues across the U.S. and on television shows such as A&E’s “Caroline’s Comedy Hour” and several Comedy Central specials, often appearing alongside his ventriloquist dummy named Burnie.
Johnson is survived by his wife Rozie Bacchi; sisters Pamela Dawn Foels and Cindy Johnson Doerr; brothers-in-law Stephen Foels and Steve Doerr; nieces Jennifer Lynne Sims, Amanda Jean Strathman, Brooke Alexandra Beck and their spouses; and great nieces Cameron Hazel Sims and Zoey Violet Strathman.

# Tom Johnson, ‘The Daily Show’ Writer, Dies at 55
## Related Stories
### Nike Releases New Jordan Spiz'ike Low 'Jam Central' Sneakers: Here’s Where To Shop a Pair Online
#### Read More About:
*   The Daily Show
Jump to Comments

# Tom Johnson, ‘The Daily Show’ Writer, Dies at 55
## More from Variety
*      ### The Business of Being a Business Manager; ‘The Secret Reading Club of Kabul’ Directors on Finding Inspiration and Courage     
*      ### How Citrin Cooperman’s Arnie Herrmann Built a Career Rooted in ‘Trust and Service’
Loading comments...

# Tom Johnson, ‘The Daily Show’ Writer, Dies at 55
## Most Popular
*   ### Jeff Bezos Was ‘Heavily Involved’ in Casting Robert Pattinson as James Bond and Admits Initial Fears ‘Because He’s Already So Famous…     
*   ### Amitabh Bachchan, Amish Tripathi-Backed AAA Game ‘The Age of Bhaarat’ Taps India’s Annapurna Studios for Motion Capture (EXCLUSIVE)     
*   ### Ali Fazal, Fiona Shaw, Naseeruddin Shah, Tom Mison Lead Richie Mehta’s ‘A Passage to India’ Series for BBC, CBC     
*          
*   ### Elizabeth Debicki Says ‘Tenet’ Co-Star Robert Pattinson Will Be the 'Perfect' James Bond: 'I'm So Thrilled'     
*   ### The Next Bond Girl: From Zendaya to Florence Pugh, 19 Actresses Who Could Join Robert Pattinson     
*   ### Robert Pattinson Is Officially James Bond: Meet the New 007 Actor     
*   ### The Next Bond Villain: From Idris Elba to Kristen Stewart, 22 Actors Who Should Face Off Against Robert Pattinson     
*   ### Why Denis Villeneuve Cast Robert Pattinson as James Bond: ‘I Need to Believe This Man Is a Killer’     
*   ### Diane Keaton’s ‘Memory Is Honored in Everything' in ‘Family Stone’ Sequel, Says Star Dermot Mulroney     
*   ### ‘Dune: Prophecy’ Star Tabu Joins YRF Entertainment’s Netflix Rescue Drama ‘Tunnel Men’ (EXCLUSIVE)

# Tom Johnson, ‘The Daily Show’ Writer, Dies at 55
## Must Read
*   Film
</excerpt>
### Rank 2 of 44 — 0.68
<excerpt title="Tom Johnson Dies: Emmy-Winning Comedy Writer For 'The Daily Show ...">
# Tom Johnson Dies: Emmy-Winning Comedy Writer For ‘The Daily Show’ Was 55
## Services to share this page.
### 2026-27 Awards Season Calendar: Oscars, Emmys, Grammys, Tonys, Guilds & More
Late Night TV

# Tom Johnson Dies: Emmy-Winning Comedy Writer For ‘The Daily Show’ Was 55
## Services to share this page.
### Jon Stewart Praises '60 Minutes' & Ross Douthat For Donald Trump Interview: "I Think I'm Going To Enjoy This"
Johnson wrote on more than 1,200 episodes and was one of the authors of the New York Times bestseller, _America: The Book_. Johnson won two Emmy Awards and two Peabody Awards for his work on _The Daily Show,_ but is perhaps best known for appearing on camera as anonymous hacker “Lord Viper Scorpion,” who mercilessly destroyed Stewart’s online reputation while taunting the host to “feel his sting.”

# Tom Johnson Dies: Emmy-Winning Comedy Writer For ‘The Daily Show’ Was 55
## Services to share this page.
### Watch on Deadline
[Video 9](blob:https://deadline.com/9935fb5d-c713-4e74-8ac1-46f976afb0ca)1/1 Skip Ad Continue watching after the adVisit Advertiser websiteGO TO PAGE
Video 10
Video 11
Video 12
Video 13
Video 14
Video 15
Video 16
From 2007 to 2009, he served as head writer for _Talk Show with Spike Feresten,_ the Fox network’s longest-running late night show. He went on to work as a head writer on _Lopez Tonight_ and would later cocreate _The Jeselnik Offensive with Anthony Jeselnik,_ where he served as an executive producer and head writer.
His other television writing credits include the Grammy Awards, the Comedy Central Celebrity Roasts, the MTV Movie Awards, and the _Inside the NBA All-Star Roast_, and more.
Survivors include his wife, Rozie Bacchi, sisters Pamela Dawn Foels and Cindy Johnson Doerr, brothers-in-law Stephen Foels and Steve Doerr, nieces Jennifer Lynne Sims, Amanda Jean Strathman, Brooke Alexandra Beck and their spouses, great nieces Cameron Hazel Sims and Zoey Violet Strathman, and cats Billie, Sal, and Mama.

# Tom Johnson Dies: Emmy-Winning Comedy Writer For ‘The Daily Show’ Was 55
## Must Read Stories
Hide Articles
*   ### Par-WB Shakeup Sees Top Roles For Kira Goldberg, Erhman; Who’s Out      
*   ### ‘Dancing With The Stars’ Finale Will Go Live Across The Country For First Time      
*   ### Much Ado About The Box Office: Stars Drive Lucrative Week On Broadway      
*   ### Jeff Daniels Joins Seyfried & Stone In Youssef’s Comedy ‘Martha & Muhammad’

# Tom Johnson Dies: Emmy-Winning Comedy Writer For ‘The Daily Show’ Was 55
## Read More About:
*   Emmy Awards  
*   The Daily Show  
*   Tom Johnson
2 Comments

# Tom Johnson Dies: Emmy-Winning Comedy Writer For ‘The Daily Show’ Was 55
## Subscribe to Deadline
Get our Breaking News Alerts and Keep your inbox happy.
Sign Up
</excerpt>
### Rank 3 of 44 — 0.61
<excerpt title="Tom Johnson | Emmy Awards and Nominations">
# Tom Johnson | Emmy Awards and Nominations | Television Academy
#### Membership
##### The Interviews: An Oral History of Television
The Interviews: An Oral History of Television

# Tom Johnson | Emmy Awards and Nominations | Television Academy
#### Membership
##### College Television Awards
College Television Awards

# Tom Johnson | Emmy Awards and Nominations | Television Academy
#### Membership
##### Membership
Member Log In
No Invitation Necessary
Become a Member
Peer Group Requirements
Membership Benefits
Membership
Member Log In
No Invitation Necessary
Become a Member
Peer Group Requirements
Membership Benefits

# Tom Johnson | Emmy Awards and Nominations | Television Academy
#### Membership
##### Events
Past Events
Screening Room
Events
Past Events
Screening Room

# Tom Johnson | Emmy Awards and Nominations | Television Academy
#### Membership
##### Governor Spotlight
Governor Spotlight

# Tom Johnson | Emmy Awards and Nominations | Television Academy
#### Membership
##### Viewing Platform
Viewing Platform

# Tom Johnson | Emmy Awards and Nominations | Television Academy
#### FAQ
*   How are the Emmys awarded?  
*   When were the first Emmy Awards presented?  
*   How can I find out if someone has won an Emmy Award?  
*   How often will my voting membership status be reviewed?  
*   Who can vote for the Emmy Awards?  
*   How do I become a member of the Television Academy?

# Tom Johnson | Emmy Awards and Nominations | Television Academy
#### Connect
Close

# Tom Johnson | Emmy Awards and Nominations | Television Academy
#### Connect
##### Find people, shows, articles, awards and more.
Search
Close
Member ID
Member Type
Member Since
Visit Member Dashboard Log Out
Close

# Tom Johnson | Emmy Awards and Nominations | Television Academy
## Log In
Hello, nice to see you back!
Log in to your Television Academy account:
Username
Password
Log In...
Forgot Password?
Forgot Username?

# Tom Johnson | Emmy Awards and Nominations | Television Academy
## Not a member yet?
If you're seeking ways to connect with working television industry professionals, both in front of and behind the camera, joining our organization offers you unparalleled access, benefits and opportunities.
Learn more about Television Academy Membership
If you're ready to join, click below to start the application process.
Join Now
Home>Awards
Tom Johnson
Photo Credit: _The Johnson Family_

# Tom Johnson
Writer, Producer
Close
Video 3
/
Photo Credit:
Photo Credit:
/

# Tom Johnson
###### Learn More:
*   IMDb

# Tom Johnson
Writer, Producer
Birthday  
July 25, 1968
Birthplace  
Fairfax, Virginia
Date of Passing  
January 14, 2024
ObituaryDeadline
Tom Johnson was a screenwriter and producer who worked on television series, specials and films. He was best known for being a writer on over 1,000 episodes of _The Daily Show_ for 7 years. Johnson served as head writer for series including _Stand-Up Nation with Greg Giraldo, Comedy Knockout, The Jeselnik Offensive, Lopez Tonight, Late Night Liars, Talk Show with Spike Feresten_ and _Reality Bites Back._ He was in charge of the writing for television specials including _WTF with Marc Maron, Joan Rivers' Straight Talk, Scream Awards 2011, Guys Choice Awards 2012,Guys Choice Awards 2014_ and _Guys Choice Awards 2015_. In addition to his television shows and specials,he worked on television movies including "Balls of Steel," "Adult Content with Greg Giraldo," "Race Riot" and "Gamekillers."
Johnson also served as a producer on many of the television series and specials he wrote. Other shows he produced include _Martha & Snoop's Potluck Party Challenge, Caraoke Showdown, Punk'd_ and _Best Week Ever with Paul F. Tompkins._
Awards & NominationsNews & Features

# Tom Johnson
##### 3 Nominations


# Tom Johnson
##### 2 Emmys
Show Wins Only
Winner

# Tom Johnson
##### 2 Emmys
###### Outstanding Writing For A Variety, Music Or Comedy Program - 2003
Tom Johnson, _Writer_
The Daily Show With Jon Stewart
Comedy Central
Central Productions, LLC
Nominee
</excerpt>
### Rank 4 of 44 — 0.61
<excerpt title="Tom Johnson, 'Daily Show' Writer, Dies at 55">
# Tom Johnson, ‘Daily Show’ Writer, Dies at 55
### Thom Velde, Longtime AMC Theatres Executive, Dies at 83
Movies

# Tom Johnson, ‘Daily Show’ Writer, Dies at 55
### Jeremy Conway, Agent for Anthony Hopkins and Brian Cox, Dies at 87
Born on July 25, 1968, in Fairfax, Virginia, Johnson began his career after college and founded the Network Comedy Troupe. He also toured as a comedian and performed at venues across the country and on television.
Johnson was initially hired in 1996 as a writer on Comedy Central’s _The Daily Show_ when Craig Kilborn was the host. He was there when Jon Stewart took over in 1999 and stayed until 2003. He also made a few appearances onscreen, playing the hacker Lord Viper Scorpion on a handful of episodes in 2000-01.
He won his Emmys for best writing for a variety, music or comedy program in 2001 and 2003, received two Peabody Awards and landed another Emmy nom in 2002.
Johnson co-created _The Jeselnik Offensive_ with Anthony Jeselnik in 2013, serving as executive producer and head writer, was the head writer on _Talk Show With Spike Feresten_ from 2007-09 and worked as a writer on _Lopez Tonight_ from 2010-11.
His other TV writing and producing credits included the Grammys and MTV Video Music Awards, Comedy Central roasts, _Stand-Up Nation With Greg Giraldo_, _The Gamekillers_, _Reality Bites Back_, _Lopez Tonight_, _WTF With Marc Maron_, _Comedy Knockout_, _Nice One!_, _Martha & Snoop’s Potluck Party Challenge_, _Caraoke Showdown_ and _Punk’d_.
In addition to his wife, survivors include his sisters, Pamela and Cindy; brothers-in-law Stephen and Steve; nieces Jennifer, Amanda, Brooke and their spouses; great nieces Cameron and Zoey; and cats Billie, Sal and Mama.
His wife said he had multiple projects that he was planning to pitch.

# Tom Johnson, ‘Daily Show’ Writer, Dies at 55
### Jeremy Conway, Agent for Anthony Hopkins and Brian Cox, Dies at 87
“Although he was an accomplished comedy writer with numerous fancy awards, he was selfless and always said he should have been in the F.B.I. like his father,” she said. “If you knew him, you knew that he was ‘in 9/11, on 9/11, and at 9/11’ and figured he’d be dead by the age of 40 anyway. Maybe that is why he lived his life to the fullest.
“He was a voracious reader, eater and rescuer of cats. It brought him great joy to play pranks on those he loved. … He would be so grateful to see the outpouring of love and support. Rest in peace, Tom. You deserve the best. I love you.”
A celebratory memorial will be held in the coming months.

# Tom Johnson, ‘Daily Show’ Writer, Dies at 55
### Read More About:
*   Obituaries  
*   The Daily Show

# Tom Johnson, ‘Daily Show’ Writer, Dies at 55
## THR Newsletters
Sign up for THR news straight to your inbox every day
Subscribe Sign Up

# Tom Johnson, ‘Daily Show’ Writer, Dies at 55
## More from The Hollywood Reporter
*   Tallinn Black Nights Film Festival
</excerpt>
### Rank 5 of 44 — 0.33
<excerpt title="Tom Johnson">
# Tom Johnson
### APHA 2026 — Together We Thrive: Health Across the Lifespan ## As the largest public health gathering of the year, APHA’s Annual Meeting and Expo convenes approximately 12,000 public health professionals and partners from around the world. Join us for this can’t miss opportunity to make lasting connections and learn from exhibitors, peers and today’s leaders. Together, let’s ensure health for all across the lifespan.
*   Membership
Membership

# Tom Johnson
### APHA 2026 — Together We Thrive: Health Across the Lifespan ## As the largest public health gathering of the year, APHA’s Annual Meeting and Expo convenes approximately 12,000 public health professionals and partners from around the world. Join us for this can’t miss opportunity to make lasting connections and learn from exhibitors, peers and today’s leaders. Together, let’s ensure health for all across the lifespan.
###### APHA Membership Information
*   Membership Types  
    *   Agency Membership  
    *   Member Benefits  
    *   Member Communities  
    *   APHA LEAD Online Community

    *   Member Journey  
    *   Member Directory  
    *   Join APHA  
    *   Renew Membership  
    *   Gift a Membership

# Tom Johnson
### Learn about APHA Membership The American Public Health Association is more than a professional association. We're a community. Our members work in every discipline of public health, in every U.S. state and in countries across the globe. And we're all united by a common goal: To promote optimal, equitable health and well-being for all. Join APHA. Together, we really can make a difference.
*   Join APHA

*   Home  
*   Events & Meetings  
*   APHA Policy Action Institute  
*   Meet the Speakers  
*   Tom Johnson



*    Co-Creator and Co-Host, "Why Should I Trust You?" Podcast

# Tom Johnson
### Tom Johnson
Tom W. Johnson is an award-winning news producer with experience in documentary series, digital, cable and network news. For the past 7 years, Tom was the Showrunner and an Executive Producer of Paramount+ and Showtime's five-time Emmy-nominated political news and documentary series, The Circus. Previously, he was the Executive Editor of Bloomberg Politics and Executive Producer of the nightly news program With All Due Respect, airing on Bloomberg and MSNBC. In this role, he oversaw the integration of reporting, video, and resources between a news website and a nightly news program. Before that, Tom spent two decades at ABC News, where he served as Senior Broadcast Producer for the network’s flagship evening program, World News Tonight. He worked closely with television luminaries Peter Jennings, Charles Gibson, and Diane Sawyer. His work has been honored with Emmy, Edward R. Murrow, and Peabody awards.
Follow Tom on social media: @whyshoulditrustyoupod @wsitypod
Support Public Health
800 I Street, NW
Washington, DC
20001
[202-777-2742](tel:2027772742)  
*     
*     
*     
*     
*

# Tom Johnson
### Tom Johnson
###### About Us
*   Strategic Plan  
*   History  
*   Board & Staff  
*   Affiliates  
*   Centers and Programs  
*   Governance  
*   Financial Statements  
*   Careers at APHA

# Tom Johnson
### Tom Johnson
###### Get Involved
*   Join  
*   Participate  
*   Follow  
*   Advocate  
*   Pledge  
*   Learn  
*   Donate

# Tom Johnson
### Tom Johnson
###### Our Sites
*   American Journal of Public Health   
*   The Nation's Health   
*   APHA Press   
*   Public Health Buyers Guide   
*   Get Ready   
*   CareerMart
</excerpt>

## Search 8 — query: "Josh Comers voice actor"
### Rank 1 of 12 — 0.13 (passed on)
<excerpt title="Josh Comers">
# Josh Comers | Team Coco
Skip to main content
Team Coco
Podcasts
Radio
JoinMerch
CONAN CLASSIC

# Josh Comers | Team Coco
## Josh Comers
Amazing Squint Cam Makes Average Joes Seem Celeb-TasticIt's like Jeff Bridges, Jon Cryer and Jack McBrayer are actually here. Wait a second, is that...
Browse Our

# Josh Comers | Team Coco
## Podcasts
Conan O'Brien Needs a Friend
Where Everybody Knows Your Name
Literally! With Rob Lowe
The Three Questions
Scam Goddess
Significant Others
Conan O'Brien Needs a Friend
Where Everybody Knows Your Name
Literally! With Rob Lowe
The Three Questions
Scam Goddess
Significant Others
Parks and Recollection
Inside Conan
The Juice
Good Game Nice Try
May I Elaborate?
SMARTR
Frontier Tween
Funny My Way
A Total Switch Show
Self Center
The Weird Place
View All
PodcastsContactMerchTerms of UseJoinPrivacy Policy
© 2026 Team Coco Digital LLC. All Rights Reserved.
**Follow Us**
YouTubeInstagramTwitterFacebook
</excerpt>
### Rank 2 of 12 — 0.11
<excerpt title="Josh Comers Almost Got Hit By a Bus">
# Josh Comers Almost Got Hit By a Bus
## Transcript
### John Mulaney on Hosting SNL, His Christian Bale Impression & Producing His Stepfather-in-law's Music
Jimmy Kimmel Live and John Mulaney
67K 3h ago
17:15

# Josh Comers Almost Got Hit By a Bus
## Transcript
### Jimmy O. Yang on Returning to Hong Kong After 25 Years in “Finally Home” | The Daily Show
The Daily Show
1.6M 3w ago
35:24

# Josh Comers Almost Got Hit By a Bus
## Transcript
### Pete Hegseth: Last Week Tonight with John Oliver (HBO)
LastWeekTonight
9.8M 9d ago
49:06

# Josh Comers Almost Got Hit By a Bus
## Transcript
### Ghosts are REAL and My Mom Hunts Them | Shayne Smith FULL SPECIAL
Dry Bar Comedy
2.3M 11mo ago
Show more
Show more
</excerpt>
### Rank 3 of 12 — 0.08
<excerpt title="Josh Comers | Emmy Awards and Nominations">
# Josh Comers | Emmy Awards and Nominations | Television Academy
#### Membership
##### Awards
Nominees/Winners
Awards Search
Awards News
Awards FAQs
Awards Calendar
Downloads
Awards
Nominees/Winners
Awards Search
Awards News
Awards FAQs
Awards Calendar
Downloads

# Josh Comers | Emmy Awards and Nominations | Television Academy
#### Membership
##### Emmy Awards
Emmy Awards Show
Backstage LIVE!
Creative Arts Emmys Show
Emmy Awards Search
Emmy Rules & Procedures
Nominations
Governors Award
Emmy Awards
Emmy Awards Show
Backstage LIVE!
Creative Arts Emmys Show
Emmy Awards Search
Emmy Rules & Procedures
Nominations
Governors Award

# Josh Comers | Emmy Awards and Nominations | Television Academy
#### Membership
##### Los Angeles Area Emmy Awards
Nominees
Rules & Procedures
Awards Calendar
Los Angeles Area Emmy Awards
Nominees
Rules & Procedures
Awards Calendar

# Josh Comers | Emmy Awards and Nominations | Television Academy
#### Membership
##### Engineering, Science & Technology Emmy Awards
Engineering, Science & Technology Emmy Awards

# Josh Comers | Emmy Awards and Nominations | Television Academy
#### Membership
##### Television Academy Honors
Television Academy Honors

# Josh Comers | Emmy Awards and Nominations | Television Academy
#### Membership
##### Hall of Fame
Hall of Fame

# Josh Comers | Emmy Awards and Nominations | Television Academy
#### Membership
##### College Television Awards
College Television Awards

# Josh Comers | Emmy Awards and Nominations | Television Academy
#### Membership
##### Bob Hope Humanitarian Award
Bob Hope Humanitarian Award

# Josh Comers | Emmy Awards and Nominations | Television Academy
#### Membership
##### Legacy Award
Legacy Award

# Josh Comers | Emmy Awards and Nominations | Television Academy
#### Membership
##### About the Academy
From the Chair
Frequently Asked Questions
The Emmy Statuette
History
Careers
About the Academy
From the Chair
Frequently Asked Questions
The Emmy Statuette
History
Careers

# Josh Comers | Emmy Awards and Nominations | Television Academy
#### Membership
##### Organization
Board of Governors
Executive Committee
Committees
Executive Staff
Corporate Partners
Peer Groups
Organization
Board of Governors
Executive Committee
Committees
Executive Staff
Corporate Partners
Peer Groups

# Josh Comers | Emmy Awards and Nominations | Television Academy
#### Membership
##### Advocacy
Advocacy

# Josh Comers | Emmy Awards and Nominations | Television Academy
#### Membership
##### Diversity, Equity, Inclusion & Accessibility
Diversity, Equity, Inclusion & Accessibility

# Josh Comers | Emmy Awards and Nominations | Television Academy
#### Membership
##### Corporate Partners
Corporate Partners

# Josh Comers | Emmy Awards and Nominations | Television Academy
#### Membership
##### Membership
Member Log In
Become a Member
Membership
Member Log In
Become a Member

# Josh Comers | Emmy Awards and Nominations | Television Academy
#### Membership
##### Contact Us
Document Downloads
Press Downloads
Contact Us
Document Downloads
Press Downloads

# Josh Comers | Emmy Awards and Nominations | Television Academy
#### Membership
##### Foundation
Foundation Board
Foundation Staff
Foundation Alumni
Foundation
Foundation Board
Foundation Staff
Foundation Alumni

# Josh Comers | Emmy Awards and Nominations | Television Academy
#### Membership
##### Foundation Features
Foundation News
The Take Newsletter
Strategic Impact
Foundation Features
Foundation News
The Take Newsletter
Strategic Impact

# Josh Comers | Emmy Awards and Nominations | Television Academy
#### Membership
##### Programs
Internships
Media Educators Conference
The Power of TV
Access: Behind the Screens
Programs
Internships
Media Educators Conference
The Power of TV
Access: Behind the Screens

# Josh Comers | Emmy Awards and Nominations | Television Academy
#### Membership
##### Foundation Events
Emmys Golf Classic
Emmys Pickleball Slam
Foundation Events
Emmys Golf Classic
Emmys Pickleball Slam

# Josh Comers | Emmy Awards and Nominations | Television Academy
#### Membership
##### Support
Give Today
Ways to Give
Auction
Support
Give Today
Ways to Give
Auction

# Josh Comers | Emmy Awards and Nominations | Television Academy
#### Membership
##### The Interviews: An Oral History of Television
The Interviews: An Oral History of Television
</excerpt>
### Rank 4 of 12 — 0.08
<excerpt title="Josh Comers | Emmy Awards and Nominations">
# Josh Comers | Emmy Awards and Nominations | Television Academy
#### Membership
##### The Interviews: An Oral History of Television
The Interviews: An Oral History of Television

# Josh Comers | Emmy Awards and Nominations | Television Academy
#### Membership
##### College Television Awards
College Television Awards

# Josh Comers | Emmy Awards and Nominations | Television Academy
#### Membership
##### Membership
Member Log In
No Invitation Necessary
Become a Member
Peer Group Requirements
Membership Benefits
Membership
Member Log In
No Invitation Necessary
Become a Member
Peer Group Requirements
Membership Benefits

# Josh Comers | Emmy Awards and Nominations | Television Academy
#### Membership
##### Events
Past Events
Screening Room
Events
Past Events
Screening Room

# Josh Comers | Emmy Awards and Nominations | Television Academy
#### Membership
##### Governor Spotlight
Governor Spotlight

# Josh Comers | Emmy Awards and Nominations | Television Academy
#### Membership
##### Viewing Platform
Viewing Platform

# Josh Comers | Emmy Awards and Nominations | Television Academy
#### FAQ
*   How are the Emmys awarded?  
*   When were the first Emmy Awards presented?  
*   How can I find out if someone has won an Emmy Award?  
*   How often will my voting membership status be reviewed?  
*   Who can vote for the Emmy Awards?  
*   How do I become a member of the Television Academy?

# Josh Comers | Emmy Awards and Nominations | Television Academy
#### Connect
Close

# Josh Comers | Emmy Awards and Nominations | Television Academy
#### Connect
##### Find people, shows, articles, awards and more.
Search
Close
Member ID
Member Type
Member Since
Visit Member Dashboard Log Out
Close

# Josh Comers | Emmy Awards and Nominations | Television Academy
## Log In
Hello, nice to see you back!
Log in to your Television Academy account:
Username
Password
Log In...
Forgot Password?
Forgot Username?

# Josh Comers | Emmy Awards and Nominations | Television Academy
## Not a member yet?
If you're seeking ways to connect with working television industry professionals, both in front of and behind the camera, joining our organization offers you unparalleled access, benefits and opportunities.
Learn more about Television Academy Membership
If you're ready to join, click below to start the application process.
Join Now
Home>Awards

# Josh Comers
Close
Video 2
/
Photo Credit:
Photo Credit:
/
Awards & NominationsNews & Features

# Josh Comers
##### 4 Nominations
Nominee

# Josh Comers
##### 4 Nominations
###### Outstanding Writing For A Variety Special - 2026
Josh Comers, _Written by_
The Oscars
ABC
Academy of Motion Picture Arts and Sciences
Nominee

# Josh Comers
##### 4 Nominations
###### Outstanding Writing For A Variety Special - 2016
Josh Comers, _Writer_
Triumph's Election Special 2016
Hulu
Funny Or Die
Nominee

# Josh Comers
##### 4 Nominations
###### Outstanding Writing For A Variety, Music Or Comedy Series - 2011
Josh Comers, _Writer_
Conan
TBS
Conaco, LLC
Nominee

# Josh Comers
##### 4 Nominations
###### Outstanding Writing For A Variety, Music Or Comedy Series - 2010
Josh Comers, _Writer_
The Tonight Show With Conan O'Brien
Episode #146
NBC
Conaco & NBC Universal
Click here if you have updates to this page.
The Television Academy database lists prime-time Emmy information. Click here to learn more.
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
</excerpt>
### Rank 5 of 12 — 0.08
<excerpt title="Josh Comers | Emmy Awards and Nominations">
# Josh Comers | Emmy Awards and Nominations | Television Academy
#### Academy
##### Advocacy
Advocacy

# Josh Comers | Emmy Awards and Nominations | Television Academy
#### Academy
##### Diversity, Equity, Inclusion & Accessibility
Diversity, Equity, Inclusion & Accessibility

# Josh Comers | Emmy Awards and Nominations | Television Academy
#### Academy
##### Corporate Partners
Corporate Partners

# Josh Comers | Emmy Awards and Nominations | Television Academy
#### Academy
##### Membership
Member Log In
Become a Member
Membership
Member Log In
Become a Member

# Josh Comers | Emmy Awards and Nominations | Television Academy
#### Academy
##### Contact Us
Document Downloads
Press Downloads
Contact Us
Document Downloads
Press Downloads

# Josh Comers | Emmy Awards and Nominations | Television Academy
#### Foundation
##### Foundation
Foundation Board
Foundation Staff
Foundation Alumni
Foundation
Foundation Board
Foundation Staff
Foundation Alumni

# Josh Comers | Emmy Awards and Nominations | Television Academy
#### Foundation
##### Foundation Features
Foundation News
The Take Newsletter
Strategic Impact
Foundation Features
Foundation News
The Take Newsletter
Strategic Impact

# Josh Comers | Emmy Awards and Nominations | Television Academy
#### Foundation
##### Programs
Internships
Media Educators Conference
The Power of TV
Access: Behind the Screens
Programs
Internships
Media Educators Conference
The Power of TV
Access: Behind the Screens

# Josh Comers | Emmy Awards and Nominations | Television Academy
#### Foundation
##### Foundation Events
Emmys Golf Classic
Emmys Pickleball Slam
Foundation Events
Emmys Golf Classic
Emmys Pickleball Slam

# Josh Comers | Emmy Awards and Nominations | Television Academy
#### Foundation
##### Support
Give Today
Ways to Give
Auction
Support
Give Today
Ways to Give
Auction

# Josh Comers | Emmy Awards and Nominations | Television Academy
#### Foundation
##### The Interviews: An Oral History of Television
The Interviews: An Oral History of Television

# Josh Comers | Emmy Awards and Nominations | Television Academy
#### Foundation
##### College Television Awards
College Television Awards

# Josh Comers | Emmy Awards and Nominations | Television Academy
#### Membership
##### Membership
Member Log In
No Invitation Necessary
Become a Member
Peer Group Requirements
Membership Benefits
Membership
Member Log In
No Invitation Necessary
Become a Member
Peer Group Requirements
Membership Benefits

# Josh Comers | Emmy Awards and Nominations | Television Academy
#### Membership
##### Events
Past Events
Screening Room
Events
Past Events
Screening Room

# Josh Comers | Emmy Awards and Nominations | Television Academy
#### Membership
##### Governor Spotlight
Governor Spotlight

# Josh Comers | Emmy Awards and Nominations | Television Academy
#### Membership
##### Viewing Platform
Viewing Platform
SectionsFeaturesAwardsAcademyFoundationMembership

# Josh Comers | Emmy Awards and Nominations | Television Academy
#### Membership
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

# Josh Comers | Emmy Awards and Nominations | Television Academy
#### Membership
##### Online Originals
Governor Spotlight
Online Originals
Governor Spotlight

# Josh Comers | Emmy Awards and Nominations | Television Academy
#### Membership
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

# Josh Comers | Emmy Awards and Nominations | Television Academy
#### Membership
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

# Josh Comers | Emmy Awards and Nominations | Television Academy
#### Membership
##### Awards
Nominees/Winners
Awards Search
Awards News
Awards FAQs
Awards Calendar
Downloads
Awards
Nominees/Winners
Awards Search
Awards News
Awards FAQs
Awards Calendar
Downloads
</excerpt>

## Search 9 — query: "Josh Comers voice actor 2007 episode"
### Rank 1 of 44 — 0.36 (passed on)
<excerpt title="Josh Gad">
## Early life and education
### 2020–present: Expanding ventures
| Year | Title | Role | Notes |  
| --- | --- | --- | --- |  
| 2005 | _ER_ | Sgt. Bruce Larabee | Episode: "Here and There" |  
| 2007–2008 | _Back to You_ | Ryan Church | Main role |  
| 2008 | _American Dad!_ | Art | Voice; episode: "Pulling Double Booty" |  
| 2008, 2009 | _Numbers_ | Roy McGill | 2 episodes |  
| 2009 | _Party Down_ | Jeffrey Ells | Episode: "California College Conservative Union Caucus" |  
| 2009–2011 | _The Daily Show with Jon Stewart_ | Himself (correspondent) | 5 episodes |  
| 2010 | _Bored to Death_ | Warren | Episode: "Make It Quick, Fitzgerald!" |  
| 2011 | _The Cleveland Show_ | Droopy / Pimp | Voice; episode: "Our Gang" |  
| _Californication_ | Doctor | 2 episodes |  
| _Gigi: Almost American_ | Gigi | 10 episodes; also executive producer |  
| 2011, 2020 | _Modern Family_ | Kenneth Ploufe | 2 episodes: "Punkin Chunkin" and "Dead on a Rival" |  
| 2011 | _Good Vibes_ | Mondo | Voice; main role |  
| 2012–2013 | _1600 Penn_ | Skip Gilchrist | Main role; also co-creator and executive producer |  
| 2012–2015 | _New Girl_ | Bearclaw | 3 episodes: "Katie", "Birthday", "Walk of Shame" |  
| 2013 | _Hollywood Game Night_ | Himself | Episode: "America's Got Game Night" |  
| 2014 | _Monsters vs. Aliens_ | Internet | Voice; episode: "Bride of the Internet" |  
| 2015 | _The Comedians_ | Josh | Main role |
</excerpt>
### Rank 2 of 44 — 0.35
<excerpt title="Josh Gad">
## Early life and education
### 2020–present: Expanding ventures
| 2026 | _Orangutan_ | Himself | Voice; Documentary[[59]](https://en.wikipedia.org/wiki/Josh_Gad#cite_note-59) |  
| _The Angry Birds Movie 3_† | Chuck | Voice; in production[[60]](https://en.wikipedia.org/wiki/Josh_Gad#cite_note-60) |  
| 2027 | _Spaceballs: The New One_† | TBA | Post-production; also writer and producer |  
| _[Untitled \_Ocean's Eleven\_ prequel](https://en.wikipedia.org/wiki/Untitled\_Ocean's\_Eleven\_prequel "Untitled Ocean's Eleven prequel")_† | TBA | Filming[[61]](https://en.wikipedia.org/wiki/Josh_Gad#cite_note-61) |  
| _Frozen 3_† | Olaf | Voice; in production[[62]](https://en.wikipedia.org/wiki/Josh_Gad#cite_note-62) |  
| 2028 | _[Oh, the Places You'll Go!](https://en.wikipedia.org/wiki/Oh,\_the\_Places\_You'll\_Go!#Development "Oh, the Places You'll Go!")_† | Bixby | Voice; in production[[63]](https://en.wikipedia.org/wiki/Josh_Gad#cite_note-63) |

## Early life and education
### 2020–present: Expanding ventures
| Year | Title | Role | Notes |  
| --- | --- | --- | --- |  
| 2005 | _ER_ | Sgt. Bruce Larabee | Episode: "Here and There" |  
| 2007–2008 | _Back to You_ | Ryan Church | Main role |  
| 2008 | _American Dad!_ | Art | Voice; episode: "Pulling Double Booty" |  
| 2008, 2009 | _Numbers_ | Roy McGill | 2 episodes |  
| 2009 | _Party Down_ | Jeffrey Ells | Episode: "California College Conservative Union Caucus" |  
| 2009–2011 | _The Daily Show with Jon Stewart_ | Himself (correspondent) | 5 episodes |  
| 2010 | _Bored to Death_ | Warren | Episode: "Make It Quick, Fitzgerald!" |  
| 2011 | _The Cleveland Show_ | Droopy / Pimp | Voice; episode: "Our Gang" |  
| _Californication_ | Doctor | 2 episodes |  
| _Gigi: Almost American_ | Gigi | 10 episodes; also executive producer |  
| 2011, 2020 | _Modern Family_ | Kenneth Ploufe | 2 episodes: "Punkin Chunkin" and "Dead on a Rival" |  
| 2011 | _Good Vibes_ | Mondo | Voice; main role |  
| 2012–2013 | _1600 Penn_ | Skip Gilchrist | Main role; also co-creator and executive producer |  
| 2012–2015 | _New Girl_ | Bearclaw | 3 episodes: "Katie", "Birthday", "Walk of Shame" |  
| 2013 | _Hollywood Game Night_ | Himself | Episode: "America's Got Game Night" |  
| 2014 | _Monsters vs. Aliens_ | Internet | Voice; episode: "Bride of the Internet" |  
| 2015 | _The Comedians_ | Josh | Main role |
</excerpt>
### Rank 3 of 44 — 0.25
<excerpt title="Josh Gad">
## Early life and education
### 2020–present: Expanding ventures
Gad has publicly talked about his struggle with generalized anxiety disorder, as part of his effort to combat mental health stigma and shame._[citation needed_] As an effort towards quashing the mental health stigma, Gad joined other celebrities in 2018 in an ongoing project through the Child Mind Institute, titled #MyYoungerSelf. This campaign focuses on normalizing mental health, especially in kids. The website features Gad and other celebrities talking about their own personal struggles with mental health and how they've found the help they need, while they also encourage viewers to find what can specifically help them.[[54]](https://en.wikipedia.org/wiki/Josh_Gad#cite_note-54) Gad's YouTube series _Reunited Apart_ helped him get through the pandemic and sheltering at home. While he was out of work for the duration of the pandemic, he was able to focus on the series and not let his mental health decline.[[55]](https://en.wikipedia.org/wiki/Josh_Gad#cite_note-55)
Gad has stated that while he loves the traditional aspects of Judaism and celebrates some traditions of his wife's Catholicism, he considers himself spiritual but not religious.[[9]](https://en.wikipedia.org/wiki/Josh_Gad#cite_note-vf-9)

## Early life and education
### 2020–present: Expanding ventures
| Year | Title | Role | Notes |  
| --- | --- | --- | --- |  
| 2002 | _Mary and Joe_ | Angel |  |  
| 2003 | BAQ-132 | Match factory engineer |  |  
| 2006 | _Razortooth_ | Jay Wells |  |  
| 2007 | _Watching the Detectives_ | Mark |  |  
| 2008 | _21_ | Miles |  |  
| _The Rocker_ | Matt |  |  
| 2009 | _Crossing Over_ | Howie |  |  
| _No Heroics_ | Horseforce | Television film |  
| _Waiting to Die_ | Simon |  
| _The Lost Nomads: Get Lost 22_ | Gigi / Miss Piggy / Jose Sanchez / The Clown / Spatula Lover |  |  
| _Big Guy_ | Rodney | Short film |  
| 2010 | _Marmaduke_ | Bandana Dog | Voice |  
| _Love & Other Drugs_ | Josh Randall |  |  
| 2011 | _Mardi Gras: Spring Break_ | Bump (Bartholomew T. Brown) |  |  
| 2012 | _She Wants Me_ | Sam Baum |  |  
| _Ice Age: Continental Drift_ | Louis | Voice |  
| _Thanks for Sharing_ | Neil |  |  
| 2013 | _Jobs_ | Steve Wozniak |  |  
| _The Internship_ | Headphones |  |  
| _Frozen_ | Olaf | Voice |  
| 2014 | _Wish I Was Here_ | Noah Bloom |  |  
| 2015 | _The Wedding Ringer_ | Doug Harris |  |  
| _Frozen Fever_ | Olaf | Voice; short film |  
| _Pixels_ | Ludlow Lamonsoff |  |  
| 2016 | _The Angry Birds Movie_ | Chuck | Voice[[56]](https://en.wikipedia.org/wiki/Josh_Gad#cite_note-56) |
</excerpt>
### Rank 4 of 44 — 0.24
<excerpt title="Josh Gad">
## Early life and education
### 2002–2008: Early career
[edit]
Gad made his film debut in the 2002 film _Mary and Joe_. His television debut was in 2005 in an episode of the NBC medical drama series _ER_. The same year, he replaced Dan Fogler as William Barfée in _The 25th Annual Putnam County Spelling Bee_ on Broadway after Fogler left the show.[[14]](https://en.wikipedia.org/wiki/Josh_Gad#cite_note-14) Gad went on to star in the Fox sitcom _Back to You_ as news director Ryan Church. The sitcom lasted one season from 2007 to 2008. In 2008, Gad had a supporting role in the drama film _21_, and a leading role in the comedy film _The Rocker_.

## Early life and education
### 2008–2012: Breakthrough with _The Book of Mormon_
[edit]
Gad at the 2010 Streamy Awards
After _Back to You_, Gad appeared as a correspondent on _The Daily Show_ on May 5, 2009, and became a regular correspondent on June 2, 2009.[[15]](https://en.wikipedia.org/wiki/Josh_Gad#cite_note-15) His signature segments include "The War on Christmas", in which he played an oversexed Benjamin Franklin, and "Chubby Chasers", in which he reported on Michelle Obama's efforts to curb childhood obesity.[[16]](https://en.wikipedia.org/wiki/Josh_Gad#cite_note-16) Gad made his final appearance as a correspondent on June 27, 2011.[[17]](https://en.wikipedia.org/wiki/Josh_Gad#cite_note-17) Also in 2009, Gad starred in the short-form Crackle horror comedy series _Woke Up Dead_.
In 2010, he had a supporting role in the romantic comedy-drama film _Love & Other Drugs_. That same year, Gad had a voice role in the family comedy film _Marmaduke_. In 2011, Gad voiced Mondo in the MTV adult animated sitcom _Good Vibes_. That same year, Gad portrayed Elder Cunningham in the Broadway musical _The Book of Mormon._ The show opened at the [Eugene O'Neill Theatre](https://en.wikipedia.org/wiki/Eugene_O'Neill_Theatre "Eugene O'Neill Theatre") on March 24, 2011.[[18]](https://en.wikipedia.org/wiki/Josh_Gad#cite_note-18) His last performance was June 6, 2012. Gad was nominated for the 2011 Tony Award for Best Leading Actor in a Musical and won for Grammy Award for Best Musical Theater Album, along with his costar Andrew Rannells.[[19]](https://en.wikipedia.org/wiki/Josh_Gad#cite_note-19)

## Early life and education
### 2008–2012: Breakthrough with _The Book of Mormon_
In 2012, Gad had a leading role in the independent film _She Wants Me_. Also in 2012, Gad co-created, produced and starred in the NBC sitcom _1600 Penn_. Both _Good Vibes_ and _1600 Penn_ were canceled after one season. That same year, Gad voiced the molehog Louis in _Ice Age: Continental Drift_.
</excerpt>
### Rank 5 of 44 — 0.22
<excerpt title="Josh Gad">
## Early life and education
### 2020–present: Expanding ventures
| Year | Title | Role | Notes |  
| --- | --- | --- | --- |  
| 2002 | _Mary and Joe_ | Angel |  |  
| 2003 | BAQ-132 | Match factory engineer |  |  
| 2006 | _Razortooth_ | Jay Wells |  |  
| 2007 | _Watching the Detectives_ | Mark |  |  
| 2008 | _21_ | Miles |  |  
| _The Rocker_ | Matt |  |  
| 2009 | _Crossing Over_ | Howie |  |  
| _No Heroics_ | Horseforce | Television film |  
| _Waiting to Die_ | Simon |  
| _The Lost Nomads: Get Lost 22_ | Gigi / Miss Piggy / Jose Sanchez / The Clown / Spatula Lover |  |  
| _Big Guy_ | Rodney | Short film |  
| 2010 | _Marmaduke_ | Bandana Dog | Voice |  
| _Love & Other Drugs_ | Josh Randall |  |  
| 2011 | _Mardi Gras: Spring Break_ | Bump (Bartholomew T. Brown) |  |  
| 2012 | _She Wants Me_ | Sam Baum |  |  
| _Ice Age: Continental Drift_ | Louis | Voice |  
| _Thanks for Sharing_ | Neil |  |  
| 2013 | _Jobs_ | Steve Wozniak |  |  
| _The Internship_ | Headphones |  |  
| _Frozen_ | Olaf | Voice |  
| 2014 | _Wish I Was Here_ | Noah Bloom |  |  
| 2015 | _The Wedding Ringer_ | Doug Harris |  |  
| _Frozen Fever_ | Olaf | Voice; short film |  
| _Pixels_ | Ludlow Lamonsoff |  |  
| 2016 | _The Angry Birds Movie_ | Chuck | Voice[[56]](https://en.wikipedia.org/wiki/Josh_Gad#cite_note-56) |
</excerpt>

## Search 10 — query: ""Ray James" voice actor 2007 episode"
### Rank 1 of 165 — 0.32 (passed on)
<excerpt title="James Voice Actor">
# James Voice Actor
Log In
Sign Up
James Carter Cathcart voiced James in the English dub of Pokémon starting with season 9, Ruby and Sapphire, and continued through Journeys. He also voiced Meowth and Gary Oak. Cathcart retired in 2023... more

# James Voice Actor
## james cassidy voice actor


# James Voice Actor
## team rocket james voice actor


# James Voice Actor
## james lee writer and voice actor


# James Voice Actor
## merlyn james voice actor


# James Voice Actor
## pokémon james voice actor


# James Voice Actor
## james team rocket english voice actor


# James Voice Actor
## james dorton voice actor


# James Voice Actor
## ray james voice actor 2007 tv series


# James Voice Actor
## pokemon james voice actor


# James Voice Actor
## silent hill 2 remake james voice actor
[[](https://www.instagram.com/harshadxabhira.edits) harshadxabhir... Currently rewatching old broadcasts because the new era feels a little too quiet without Jessie, James, and Ash. 📺🥺😭 I really wish pokemon was realllll!! #pokemon #pokemontrainers #pokemonmasters #ashkachum #teamrocket](https://www.instagram.com/reel/DVfeN-4EsQ0/?utm_source=popular_topic_grid)
[[](https://www.instagram.com/fwoggyplays) fwoggyplays 23.4K Professor Oak Knew Ash Growing up #pokemon #pokemoncommunity #pokemonfan #legendsza #newpokemon](https://www.instagram.com/reel/DTs66czEXoO/?utm_source=popular_topic_grid)
[[](https://www.instagram.com/saiyanbuilt) saiyanbuilt 273 Red vs Ash. Mt. Silver final boss vs World Champion from Pokemon Journeys. Full 6v6 breakdown: Red’s Pikachu, Charizard, Blastoise, Venusaur, Snorlax, Lapras vs Ash’s Pikachu, Mega Lucario, Dragonite, Gigantamax Gengar, Sirfetch’d, Dracovish. Is this nostalgia… or pure scaling? If we use game mechanics, Red dominates. If we use anime feats, Ash has the resume. Comment 🔴 for Red ⚡ for Ash #nerd #pokemon #anime #pokémoncommunity #gamer](https://www.instagram.com/reel/DVLjWM4kagT/?utm_source=popular_topic_grid)
</excerpt>
### Rank 2 of 165 — 0.31
<excerpt title="TV">
# TV
*   THE MARVELOUS MRS. MAISEL, Episode 405 & Series Finale  
*   POWER BOOK III: RAISING KANAN, STARZ, Episode 101, 103, 104, 106, 109  
*   RUSSIAN DOLL, Netflix, Episodes 201, 203, 205  
*   POWER BOOK II: GHOST, STARZ, Season 1 (Ep 1, 9), Season 3 (3 Episodes)  
*   SESAME STREET, HBO, 2016,2017-2022****  
*   THE MASTER with Ricky Moran, HBO, 2021  
*   GIRLS5EVA, Peacock TV, Episodes 1, 5  
*   RAY JAMES, HBO, Episode 110  
*   BILLIONS, ABC, Episode 601  
*   AT HOME WITH AMY SEDARIS, HULU, Episode 305  
*   BETTY, HBO, Created by Crystal Moselle and Lesley Arfin, Season 1, 2020  
*   RAMY, HULU, Created by Ramy Youssef, Season 2, 2020  
*   LITTLE AMERICA, AppleTV+, Season 1 Episode 4 (dogs), 2020  
*   DOG BOWL III (Training Feature), Animal Planet, 2020  
*   LITTLE VOICE, AppleTV+, Created by Sara Bareilles and Jessie Nelson, Produced by J.J. Abrams, 2020  
*   ALMOST FAMILY, Fox, Season 1, 2019  
*   PET SEMINARY (Mini-Mock), Comedy Central, 2019  
*   MODERN LOVE, AMAZON VIDEO, Storied Media Group; The New York Times, 2019  
*   MRS. FLETCHER, HBO, Created by Tom Perrotta, 2019  
*   THE VILLAGE, NBC, Created by Mike Daniels, Pilot and Season 1, 2019  
*   BEST IN RESCUE (Competition Judge), Hallmark Channel, 2019
</excerpt>
### Rank 3 of 165 — 0.16
<excerpt title="List of Family Guy episodes">
252	3	"Guy, Robot"	Mike Kim	Chris Regan	October 11, 2015	DACX02	2.79[283]  
253	4	"Peternormal Activity"	Greg Colton	Chris Sheridan	October 25, 2015	CACX16	3.85[284]  
254	5	"Peter, Chris & Brian"	Joe Vaux	Patrick Meighan	November 8, 2015	DACX03	2.58[285]  
255	6	"Peter's Sister"	John Holmquist	Tom Devanney	November 15, 2015	DACX04	2.91[286]  
256	7	"Hot Pocket-Dial"	Steve Robertson	Aaron Lee	November 22, 2015	DACX06	3.37[287]  
257	8	"Brokeback Swanson"	Julius Wu	Ted Jessup	December 6, 2015	DACX07	3.63[288]  
258	9	"A Shot in the Dark"	Brian Iles	Mike Desilets	December 13, 2015	DACX05	3.74[289]  
259	10	"Candy, Quahog Marshmallow"	Joseph Lee	Cherry Chevapravatdumrong	January 3, 2016	DACX01	3.26[290]  
260	11	"The Peanut Butter Kid"	Greg Colton	Artie Johann	January 10, 2016	DACX08	3.92[291]  
261	12	"Scammed Yankees"	Jerry Langford	Ray James	January 17, 2016	DACX09	3.40[292]
</excerpt>
### Rank 4 of 165 — 0.14
<excerpt title="TV">
# TV
*   POWER, STARZ, Starring Omari Hardwick, Created by Courtney Kemp Agboh, 2015  
*   TIMEFLIES – WORSE THINGS THAN LOVE, ft. Natalie La Rose Music Video, Island Records, 2015  
*   GOOD MORNING AMERICA, ABC, Segment: Paw-lympics, Starring Lara Spencer 2015  
*   THE WORLD DOG AWARDS, CW NETWORK, Starring George Lopez, 2015, 2016  
*   THE NATIONAL DOG SHOW, NBC, Watch Every Breed, Starring Johnny Weir and Tara Lipinski, 2015  
*   WISHIN AND HOPIN, LIFETIME, Starring Molly Ringwald, Directed by Colin Theys, 2015  
*   PETER PAN LIVE, NBC, Starring Allison Williams, Directed by Rob Asford and Glenn Weiss, 2014  
*   GOOD MORNING AMERICA, ABC, ‘The Silent Movie: The Good Morning’, Directed by Hana Kara 2012  
*   THE LEFTOVERS, HBO, Starring Justin Theroux and Liv Tyler, Directed by Peter Berg 2014  
*   DEEP IN THE DARKNESS, Chiller Network, Starring Dean Stockwell, Directed by Colin Theys, 2014  
*   DEAD SOULS, Chiller Network, starring Jesse James and Bill Moseley, Directed by Colin Theys, 2012  
*   FRENEMIES – Dir. Daisy Von Scherler Mayer – Staring Bella Thorne, Zendaya Coleman, Stefanie Scott – Disney Channel 2011  
*   JOHNNY AND THE SPRITES, Playhouse Disney – starring John Tartaglia, 2 epidodes 2007.  
*   SESAME STREET- 3 episodes 2007-2008 season  
*   LEGALLY BLONDE THE MUSICAL SEARCH FOR ELLE, MTV – Live recording of the show aired in 2007 starring Laura Bell Bundy  
*   CBS SUNDAY MORNING – Feature story, 2007  
*   CBS EVENING NEWS – Feature story with Richard Schlesinger, 2006  
*   SESAME STREET – Sesame Workshop, 2001-2004 seasons
</excerpt>
### Rank 5 of 165 — 0.12
<excerpt title="Mind of Mencia credits">
*   59 Episodes, 2005 - 2008  
*   59 Episodes, 2005 - 2008  
*   58 Episodes, 2005 - 2008  
*   53 Episodes, 2005 - 2007  
*   47 Episodes, 2006 - 2008  
*   47 Episodes, 2006 - 2008  
*   46 Episodes, 2006 - 2008  
*   37 Episodes, 2005 - 2008  
*   36 Episodes, 2006 - 2007  
*   36 Episodes, 2006 - 2007  
*   27 Episodes, 2005 - 2006  
*   25 Episodes, 2005 - 2007  
*   22 Episodes, 2005 - 2008  
*   19 Episodes, 2007 - 2008  
*   15 Episodes, 2006 - 2006  
*   15 Episodes, 2006 - 2006  
*   15 Episodes, 2006 - 2006  
*   12 Episodes, 2005 - 2006  
*   12 Episodes, 2005 - 2006  
*   12 Episodes, 2006 - 2006  
*   10 Episodes, 2005 - 2006  
*   10 Episodes, 2008 - 2008  
*   10 Episodes, 2008 - 2008  
*   9 Episodes, 2007 - 2008  
*   8 Episodes, 2007 - 2007  
*   5 Episodes, 2007 - 2007  
*   5 Episodes, 2008 - 2008  

*   4 Episodes, 2008 - 2008
*   46 Episodes, 2006 - 2008  
*   46 Episodes, 2006 - 2008  
*   28 Episodes, 2007 - 2008  
*   25 Episodes, 2005 - 2006  
*   21 Episodes, 2007 - 2007  
*   15 Episodes, 2006 - 2006  
*   12 Episodes, 2005 - 2006  
*   12 Episodes, 2005 - 2006  
*   11 Episodes, 2007 - 2008  
*   10 Episodes, 2005 - 2006  
*   10 Episodes, 2007 - 2007  
*   10 Episodes, 2008 - 2008  
*   6 Episodes, 2006 - 2006  
*   5 Episodes, 2007 - 2007  
*   4 Episodes, 2005 - 2005  
*   3 Episodes, 2005 - 2005  
*   3 Episodes, 2007 - 2007  
*   1 Episode, 2007 - 2007  
*   1 Episode, 2008 - 2008
</excerpt>

# Example 5
## Question
According to the CDC, which state had the lowest death rate per 100,000 people for both COVID-19 and Influenza/Pneumonia in 2020?

## Expected answer
Vermont

## Grade 0.00

## Search 1 — query: "CDC death rate per 100,000 COVID-19 2020 state lowest"
### Rank 1 of 62 — 0.73 (passed on)
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
### Rank 2 of 62 — 0.71
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
### Rank 3 of 62 — 0.65
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
### Rank 4 of 62 — 0.55
<excerpt title="COVID-19 Mortality | Stats of the States">
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

# COVID-19 Mortality
## Sources
The CDC WONDER Online Database is the source of the 2024 National Vital Statistics System death data featured in Stats of the States.
Where states are ranked, states are categorized from highest rate to lowest rate. Mortality rankings and rates are based on 2024 age-adjusted death rates.
**Keep Reading**Age Standardization of Death Rates: Implementation of the Year 2000 Standard
Although adjusted for variations in age distribution and population size, differences by state do not account for other state-specific population characteristics that may affect death rates.
When the number of deaths is small, differences between states and rankings by state may be unreliable due to instability in rates.

# COVID-19 Mortality
## On This Page
*   Mortality rates  
*   Sources
Mar. 1, 2026
SourcesPrintShare
FacebookLinkedInTwitterSyndicate
Content Source:
National Center for Health Statistics

# COVID-19 Mortality
## National Center for Health Statistics
NCHS collects, analyzes, and disseminates timely, relevant, and accurate health data and statistics to inform the public and guide program and policy decisions to improve our nation’s health.
View All
</excerpt>
### Rank 5 of 62 — 0.50
<excerpt title="Investigate rates of COVID-19 Cases in the United States by Age">
# COVID-19 cases by age in United States - Health Equity Tracker


# Health Equity Tracker
Skip to main content
[![Image 1: Health Equity Tracker logo](blob:http://localhost/93fb1ee7798a57ccbceeaf6accbc8c74)Health Equity Tracker](https://healthequitytracker.org/)
About
Insights Hub
Media & Updates
FAQs
Explore the data

# Investigate rates of COVID-19 Cases in the United States by Age
Compare mode
Off
Compare mode
Jump to
Choose
Jump to
Report insights
Age: All
* * *
View small multiples

# Investigate rates of COVID-19 Cases in the United States by Age
## Rates of COVID-19 cases (Cumulative Jan 2020 - May 2024) in the United States
Alaska has the highest value at 42k per 100k. West Virginia has the lowest at 630 per 100k. Data available for 55 states/territories.
cases per 100k
No data
< 25k
25k – 28k
28k – 32k
32k – 34k
34k – 36k
≥ 36k
1.   United States
Total population: 338,156,808 (from ACS)
Expand state/territory rate extremes

# Investigate rates of COVID-19 Cases in the United States by Age
## Rates of COVID-19 cases (Cumulative Jan 2020 - May 2024) in the United States
#### 5 Highest:
*   Alaska: 42,487 per 100k  
*   Kentucky: 40,212 per 100k  
*   North Dakota: 39,578 per 100k  
*   South Carolina: 39,280 per 100k  
*   New York: 38,732 per 100k

# Investigate rates of COVID-19 Cases in the United States by Age
## Rates of COVID-19 cases (Cumulative Jan 2020 - May 2024) in the United States
#### 5 Lowest:
*   West Virginia: 626 per 100k  
*   Northern Mariana Islands: 3,250 per 100k  
*   Puerto Rico: 6,183 per 100k  
*   Iowa: 15,692 per 100k  
*   Oklahoma: 19,177 per 100k

# Investigate rates of COVID-19 Cases in the United States by Age
## Rates of COVID-19 cases (Cumulative Jan 2020 - May 2024) in the United States
#### National overall:
*   United States: 31,345 per 100k
All rates are reported as: **Rates of COVID-19 cases (Cumulative Jan 2020 - May 2024)**.
Consider the possible impact of data reporting gaps when interpreting the highest and lowest rates.
View methodology.
Sources: CDC Case Surveillance Restricted Access Detailed Data (data from January 2020 - May 2024) and American Community Survey (ACS) 5-year estimates (data from 2024).
</excerpt>

## Search 2 — query: "CDC influenza pneumonia death rate per 100,000 2020 state lowest"
### Rank 1 of 61 — 0.70 (passed on)
<excerpt title="Influenza and Pneumonia Mortality | Stats of the States">
# Influenza and Pneumonia Mortality
## Mortality rates
### Flu (influenza) and pneumonia deaths per 100,000 total population (age-adjusted mortality rate)
| Location Sort by Location in ascending order | Death Rate Sort by Death Rate in ascending order | Deaths Sort by Deaths in ascending order |  
| --- | --- | --- |  
| Alabama | 14.5 | 956 |  
| Alaska | 10.4 | 70 |  
| Arizona | 10 | 1,009 |  
| Arkansas | 17.1 | 670 |  
| California | 11.6 | 5,535 |  
| Colorado | 5.9 | 381 |  
| Connecticut | 13.9 | 716 |  
| Delaware | 11.8 | 173 |  
| District of Columbia | 6.8 | 48 |  
| Florida | 8.5 | 3,093 |  
| Georgia | 10.4 | 1,297 |  
| Hawaii | 10.6 | 250 |  
| Idaho | 7.3 | 171 |  
| Illinois | 11.8 | 1,936 |  
| Indiana | 11.2 | 953 |  
| Iowa | 12 | 533 |  
| Kansas | 12.3 | 459 |  
| Kentucky | 13.1 | 740 |  
| Louisiana | 11.4 | 634 |  
| Maine | 10.1 | 222 |  
| Maryland | 9.3 | 727 |  
| Massachusetts | 11.1 | 1,058 |  
| Michigan | 10.5 | 1,405 |  
| Minnesota | 6.6 | 490 |  
| Mississippi | 19.1 | 701 |  
| Missouri | 12.9 | 1,045 |  
| Montana | 8.9 | 135 |  
| Nebraska | 12.1 | 296 |
</excerpt>
### Rank 2 of 61 — 0.59
<excerpt title="Influenza and Pneumonia Mortality | Stats of the States">
# Influenza and Pneumonia Mortality
## Mortality rates
### Flu (influenza) and pneumonia deaths per 100,000 total population (age-adjusted mortality rate)
*   5.9 - < 8.54  
*   8.54 - < 11.18  
*   11.18 - < 13.82  
*   13.82 - < 16.46  
*   16.46 - < 19.1
Skip Data Table
Data Table
Data table showing data for the United States Map figure.

# Influenza and Pneumonia Mortality
## Mortality rates
### Flu (influenza) and pneumonia deaths per 100,000 total population (age-adjusted mortality rate)
| Location Sort by Location in ascending order | Death Rate Sort by Death Rate in ascending order | Deaths Sort by Deaths in ascending order |  
| --- | --- | --- |  
| Alabama | 14.5 | 956 |  
| Alaska | 10.4 | 70 |  
| Arizona | 10 | 1,009 |  
| Arkansas | 17.1 | 670 |  
| California | 11.6 | 5,535 |  
| Colorado | 5.9 | 381 |  
| Connecticut | 13.9 | 716 |  
| Delaware | 11.8 | 173 |  
| District of Columbia | 6.8 | 48 |  
| Florida | 8.5 | 3,093 |  
| Georgia | 10.4 | 1,297 |  
| Hawaii | 10.6 | 250 |  
| Idaho | 7.3 | 171 |  
| Illinois | 11.8 | 1,936 |  
| Indiana | 11.2 | 953 |  
| Iowa | 12 | 533 |  
| Kansas | 12.3 | 459 |  
| Kentucky | 13.1 | 740 |  
| Louisiana | 11.4 | 634 |  
| Maine | 10.1 | 222 |  
| Maryland | 9.3 | 727 |  
| Massachusetts | 11.1 | 1,058 |  
| Michigan | 10.5 | 1,405 |  
| Minnesota | 6.6 | 490 |  
| Mississippi | 19.1 | 701 |  
| Missouri | 12.9 | 1,045 |  
| Montana | 8.9 | 135 |  
| Nebraska | 12.1 | 296 |
</excerpt>
### Rank 3 of 61 — 0.44
<excerpt title="Influenza and Pneumonia Mortality | Stats of the States">
# Influenza and Pneumonia Mortality
## Mortality rates
### Flu (influenza) and pneumonia deaths per 100,000 total population (age-adjusted mortality rate)
| Nevada | 13.9 | 556 |  
| New Hampshire | 8.6 | 177 |  
| New Jersey | 10 | 1,235 |  
| New Mexico | 14.2 | 390 |  
| New York | 15 | 4,153 |  
| North Carolina | 12.6 | 1,704 |  
| North Dakota | 9.6 | 101 |  
| Ohio | 11.5 | 1,790 |  
| Oklahoma | 14.1 | 679 |  
| Oregon | 6.1 | 346 |  
| Pennsylvania | 12.2 | 2,289 |  
| Rhode Island | 9 | 141 |  
| South Carolina | 9.4 | 665 |  
| South Dakota | 13.4 | 160 |  
| Tennessee | 15.5 | 1,360 |  
| Texas | 10.6 | 3,326 |  
| Utah | 10.1 | 299 |  
| Vermont | 8.6 | 81 |  
| Virginia | 9.6 | 1,052 |  
| Washington | 8.1 | 762 |  
| West Virginia | 18.4 | 481 |  
| Wisconsin | 7.9 | 616 |  
| Wyoming | 10 | 73 |
Download Map (PNG)Download Data (CSV)
Skipped data table.

# Influenza and Pneumonia Mortality
## Sources
The CDC WONDER Online Database is the source of the 2024 National Vital Statistics System death data featured in Stats of the States.
Where states are ranked, states are categorized from highest rate to lowest rate. Mortality rankings and rates are based on 2024 age-adjusted death rates.
**Keep Reading**Age Standardization of Death Rates: Implementation of the Year 2000 Standard
Although adjusted for variations in age distribution and population size, differences by state do not account for other state-specific population characteristics that may affect death rates.
When the number of deaths is small, differences between states and rankings by state may be unreliable due to instability in rates.

# Influenza and Pneumonia Mortality
## On This Page
*   Mortality rates  
*   Sources

# Influenza and Pneumonia Mortality
## Related Pages
*   Death Data Maps  
*   Hypertension Mortality  
*   Infant Mortality  
*   Kidney Disease Mortality  
*   Parkinson's Disease Mortality
View All Stats of the States
Kidney Disease Mortality
Mar. 6, 2026
Sources and Page InfoPrintShare
FacebookLinkedInTwitterSyndicate
Content Source:
National Center for Health Statistics
About this page
Published: August 20, 2025
Updated: March 6, 2026   
This page was last updated on this date. Updates may include minor edits, image changes, or other modifications to page content.
Reviewed: March 6, 2026   
The information on this page was last reviewed by subject matter experts to ensure accuracy.
*   Death Data Maps  
*   Hypertension Mortality  
*   Infant Mortality  
*   Kidney Disease Mortality  
*   Parkinson's Disease Mortality
View All Stats of the States
Back to Top

# Influenza and Pneumonia Mortality
## National Center for Health Statistics
NCHS collects, analyzes, and disseminates timely, relevant, and accurate health data and statistics to inform the public and guide program and policy decisions to improve our nation’s health.
View All
</excerpt>
### Rank 4 of 61 — 0.29
<excerpt title="Influenza and Pneumonia Mortality | Stats of the States">
# Influenza and Pneumonia Mortality | Stats of the States | CDC
Skip directly to site contentSkip directly to searchSkip directly to On This Page
An official website of the United States government
Here's how you know
**Official websites use .gov**  
A **.gov** website belongs to an official government organization in the United States.
**Secure .gov websites use HTTPS**  
A **lock** (  ) or **https://** means you've safely connected to the .gov website. Share sensitive information only on official, secure websites.
National Center for Health StatisticsStats of the States
Explore This Topic
Search
Search Clear Search
For Everyone
*   Birth Data Maps  
*   Death Data Maps  
*   More State Data Maps  
*   Statistics by State  
*   View all
**Related Topics:**
NCHS Pressroom
Home
_search_
clear search
National Center for Health Statistics
Stats of the States Menu
clear search
For Everyone
*   Birth Data Maps  
*   Death Data Maps  
*   More State Data Maps  
*   Statistics by State  
*   View AllHome
Related Topics
*   NCHS Pressroom
Stats of the States
![Image 6](blob:http://localhost/ace79f487aea0e638c5d51be0d2a7633)

# Influenza and Pneumonia Mortality
Death Data Maps
For Everyone
Mar. 6, 2026, visit link for details.

# Influenza and Pneumonia Mortality
## Key points
*   Find death (mortality) rates from flu (influenza) and pneumonia for each state in map and table formats.  
*   The mortality rate is the number of deaths per 100,000 total population.  
*   Mortality rates are age-adjusted to account for differences in age distribution and population size between different populations.

# Influenza and Pneumonia Mortality
## Mortality rates
Year
Skip Over Map Container

# Influenza and Pneumonia Mortality
## Mortality rates
### Flu (influenza) and pneumonia deaths per 100,000 total population (age-adjusted mortality rate)
*   5.9 - < 8.54  
*   8.54 - < 11.18  
*   11.18 - < 13.82  
*   13.82 - < 16.46  
*   16.46 - < 19.1
Skip Data Table
Data Table
Data table showing data for the United States Map figure.
</excerpt>
### Rank 5 of 61 — 0.29
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

For each search, read the top excerpt and the ones ranked below it, and judge whether the order is right for answering the question. An excerpt holding the answer, or a fact that leads to it, should outrank one that only repeats the query's words or covers the topic without a checkable fact. If none of the excerpts holds anything useful, that is the search's fault, not this instruction's. Find the ranking error that cost the most and write a new instruction that fixes it. Replace or compress existing text where you can; avoid making it much longer. Do not write the "Original question" or "Search query" lines; they are appended for you. Do not copy any fact, name, site or topic from these examples.

Provide the new instruction within ``` blocks.
