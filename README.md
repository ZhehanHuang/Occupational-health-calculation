# Characterizing Occupatioanl Health Impacts

**System approach for characterizing and evaluating factors for occupational health impacts due to nonfatal injuries and illnesses for the use in life cycle assessment**

*Authors:* [Zhehan Huang](https://github.com/ZhehanHuang/)＊, [Shaobin Li](https://github.com/)＊

_________________________________________________________________________________________________

Introduction
------------

This package provides an easy way to calculate the occupational health impact of 397 industries in the U.S. The calculation module in the package can be divided into three parts:

* **[Allocation_injuries_and_illness_2014-2017.py](Allocation_injuries_and_illness_2014-2017.py) and [Allocation_injuries_and_illness_2018.py](Allocation_injuries_and_illness_2018.py) are to redistribute the number of injuries and illness to all 6-digit industry based on the number of them to 2-digit industry.** Due to an inherent flaw in the data used, not all 6-digit industries have corresponding injury data, but all 6-digit industries are needed in the latter convergence matrix, so the data need to be filled in. Since only 2-digit industries in the 6-digit classification system cover all 6-digit industries, we decided to use the injury and illness data from 2-digit industries to assign the 6-digit industries with missing data covered by them. The number of injuries and illnesses for all 6-digit industries was estimated by first deducting the existing 6-digit industry data from the injury and illness data for 2-digit industries, and then equally distributing the remaining number of injuries and illnesses to all corresponding 6-digit industries (including 6-digit industries with data). The reason to use two different codes is that the data structure varies from 2018 and 2014-2017.

* Allocation_age.py is to redistribute the original age group of BLS to the WHO equivalent age group. 
* Calculation_2014-2018_YLD_&_DALY.py is the main part to calculate the occupational health impact. 

SPA file contains original data and code for structural path analysis for either a specific industry sector or a good.
