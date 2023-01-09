# Characterizing Occupatioanl Health Impacts

**System approach for characterizing and evaluating factors for occupational health impacts due to nonfatal injuries and illnesses for the use in life cycle assessment**

*Authors:* [Zhehan Huang](https://github.com/ZhehanHuang/)＊, [Shaobin Li](https://github.com/)＊

_________________________________________________________________________________________________

## Introduction

This package provides an easy way to calculate the occupational health impact of 397 industry sectors in the U.S. The calculation module in the package can be divided into three parts:

* **[Allocation_injuries_and_illness_2014-2017.py](Allocation_injuries_and_illness_2014-2017.py) and [Allocation_injuries_and_illness_2018.py](Allocation_injuries_and_illness_2018.py) are to redistribute the number of injuries and illness to all 6-digit industries based on the number of them to 2-digit industries.** Due to an inherent flaw in the data used, not all 6-digit industries have corresponding injury data, but all 6-digit industries are needed in the latter convergence matrix, so the data need to be filled in. Since only 2-digit industries in the 6-digit classification system cover all 6-digit industries, we decided to use the injury and illness data from 2-digit industries to assign the 6-digit industries with missing data covered by them. The number of injuries and illnesses for all 6-digit industries was estimated by first deducting the existing 6-digit industry data from the injury and illness data for 2-digit industries, and then equally distributing the remaining number of injuries and illnesses to all corresponding 6-digit industries (including 6-digit industries with data). The reason to use two different codes is that the data structure varies from 2018 and 2014-2017.

* **[Allocation_age_2016-2017.py](Allocation_age_2016-2017.py) and [Allocation_age_2018.py](Allocation_age_2018.py) are to redistribute the original age group of BLS to the WHO equivalent age group.** We assume that each age grouping is uniform distributed and therefore use averaging to redistribute age groups. Age data for 2014 to 2015 are missing and we used the average of the age distribution from 2016 to 2018 combined with the number of employed in that year for the estimation. 

* **[Calculation_2014-2018_YLD_&_DALY.py](Calculation_2014-2018_YLD_&_DALY.py) is the main part to calculate the characterization factors for occupational health impacts.** Methodology and data source will be mentioned later in the [Methodology and Data source](Methodology-and-Data-source) section.

This package also provides a way to use **Structural Path Analysis (SPA)** to find out the contribution of each industries to a specific industry sector or a good. [SPA](SPA) file contains original data and codes for SPA.

## Methodology and Data source

### Methodology

We used the following equations to calculate occupational health impacts.
$$YLD_n= YLD_{n,LL}× f_{LL}+YLD_{n,ST}×f_{ST}$$
$$YLD_{n,ST}=\sum_{c=1}^{13} \sum_{a=1}^{3}I_{c,a,ST} ×W_{c,ST}×D_{c,a,ST}$$
$$YLD_{n,LL}=\sum_{c=1}^{13} \sum_{a=1}^{3}I_{c,a,LL} ×W_{c,ST}×D_{c,a,LL}$$
where $f_{LL}$ and $f_{ST}$ represent the lifelong and short-term split for an injury or illness, respectively. $I_{c,a,ST}$ represents different occupational injuries and illnesses (c) in each age group (a) for short-term (ST) non-fatal injuries and illnesses. $W_{c,ST}$ is the proportion of short-term disabilities indicated by each of the nature codes (c). $D_{c,a,ST}$ indicates the duration of each short-term injury or illness (c) in each age group (a). And the definitions are similar to $I_{c,a,LL}$, $W_{c,LL}$ and $D_{c,a,LL}$.

To further calculate characterization factors, we used the following equation.
$$CF_{total}= \overrightarrow{yld} \ \boldsymbol{CONV_{norm}} \ \widehat{g^{-1}} \ \boldsymbol{V} \ \widehat{q^{-1}} \ \boldsymbol{(I-A)^{-1}} \ \overrightarrow{y} $$
where $CF_{total}$ represents the total CF for occupational health across all US economic sectors. $\overrightarrow{yld}$  represents direct impacts across different industry sectors, which is an n-dimensional vector consisting n industry sectors of $YLD_n$. $\widehat{g^{-1}}$ is the inverse of the diagonal matrix of the total output of the different industries in units of the inverse of the dollar. $\boldsymbol{V}$ is a make matrix. $\widehat{q^{-1}}$ is an inverse diagonal matrix based on the total output of commodities in different industries. $\boldsymbol{I}$ represents identity matrix and $\boldsymbol{A}$ represents direct requirement matrix. $\boldsymbol{(I-A)^{-1}}$ is the [Leontief inverse matrix](https://www.openriskmanual.org/wiki/Leontief_Inverse_Matrix#:~:text=Leontief%20Inverse%20Matrix%20). The vector $\overrightarrow{y}$ is the final demand vector for each good in the manufacturing stage in $ per good.

### Data source
