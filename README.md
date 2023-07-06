# covid19-kurdistan
This repository holds the required codes that were in place for conducting a research on COVID-19 in Kurdistan Regions of Iraq.
Full-text published work available on: https://jidc.org/index.php/journal/article/view/13993


The map of Karezan neighbourhood has been geographically redrawn in the form of a single picture, with normalized colours, rotated, and presented as one single Numpy array. Where each colour represents a type of building or an area, it is shown as animations on the dimension of time for each scenario. The virtual world has a semi-randomized population that represents a single community in the region. The reason we call it semi-randomized is because we have intentionally selected few virtual citizens to have some pre-existing conditions that are vulnerable to COVID-19. The ages of virtual citizens are randomly determined up to 75 years, which are the average ages in the region according to the data we have from Ministry of Health. The population distribution over residences is entirely random, because there is no data to suggest an area to be populated differently than another. The artificial citizens live their lives from a time window that begins at 9 am and ends at midnight. It is assumed that there will be no movement after that time, or simply we monitor the life of the AI particles within that range of time per day. Their behaviour relies on the scenario they inhabit. We have created several scenarios, which are sets of policies that apply to a community. For instance, in a scenario where all citizens remain at home, AI particles do not exit out of their homes. 

There are four scenarios that we have focused on in the simulations. To our model the level of freedom of people is an attribute that indicate each scenario. In each scenario the level of freedom is set to an integer value 1-4:
  1.	In a world where there is complete lockdown.
  2.	Only one person per family can go out.
  3.	The hours of going out is set to 9 AM to 17 PM.
  4.	No restriction at all.
  
 Each scenario provides us with an animation of days in that world, the event and daily records of infection, recovery and deaths. The recovery or death factor is set on several arguments such as age and health conditions. The disease has shown itself to be more devastating for victims with weak immune systems. That has been set to a random indicator. The recovery days in real life has been set to be between 5 to 15 days,  where we added some random effect that some people will take less time and some will take longer to recover. 
The simulated world has a population of 100 people where only one of them is infected previously or to be called in Day 1. The age limits are between 1-75 years. The younger an individual, the less effective the virus spread. The disease factor is selected among most vulnerable ones, listed to the respect of their fatality rates:
 
 •	Cardiovascular Diseases
  •	Diabetes
  •	Chronic respiratory diseases
  •	Hypertension
  •	Cancer
  
Each world is simulated for 20 days of virtual life. In the Figure 8 we can see all four scenarios at one glance after one week of simulated life when the time of their virtual world has been stopped at 15:30. Each home has number of inhabitants and they form a family. The simulation did not take in account that the recovered citizens could be once more infected with the virus, as no available report support or refutes that possibility. The world is re-paused at day 11, on 9:30 shown in Figure 9. Should we compare both observations on the level of freedom at 2 and 3, we could see that at beginning, there is not a significant change in the number of infected, and mostly it relies on the random effects. However, on day 11, it is shown that when the level of freedom is set to 3, it provides a more dangerous situation to the area. In all cases, the best option of such community is to stay at home in the case that unknown virus carriers are in the region. It is also clear that with no applied movement restriction, the entire population of a small zone can be 100% affected in less than a week.

Copyright © 2021 Abdullah et al. This is an open-access article distributed under the Creative Commons Attribution License, which permits unrestricted use, distribution, and reproduction in any medium, provided the original work is properly cited.

To cite:
```
@article{abdullah_time_2021,
	title = {Time Series Modelling and Simulating the Lockdown Scenarios of {COVID}-19 in Kurdistan Region of Iraq},
	volume = {15},
	rights = {Copyright (c) 2021 Milad Ashqi  Abdullah, Kamal Kolo, Peyman  Aspoukeh, Rahel  Hamad, James R.  Bailey},
	issn = {1972-2680},
	url = {https://jidc.org/index.php/journal/article/view/33839712},
	doi = {10.3855/jidc.13993},
	pages = {370--381},
	number = {3},
	journaltitle = {The Journal of Infection in Developing Countries},
	author = {Abdullah, Milad and Kolo, Kamal and Aspoukeh, Peyman and Hamad, Rahel and Bailey, James R.},
	urldate = {2023-03-22},
	date = {2021-03-31},
	langid = {english},
	note = {Number: 03},
	keywords = {Forecasting, {AI} Simulations, {COVID}-19, Iraq, Kurdistan Region, Time Series Modelling},
}
```
