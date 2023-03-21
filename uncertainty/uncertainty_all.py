# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import pandas as pd
from numpy import isnan

mc_2018 = np.load('./2018MCS_1.npy',encoding = "latin1")
mc_2018[isnan(mc_2018)] = 0

mc_2017 = np.load('./2017MCS_1.npy',encoding = "latin1")
mc_2017[isnan(mc_2017)] = 0

mc_2016 = np.load('./2016MCS_1.npy',encoding = "latin1")
mc_2016[isnan(mc_2016)] = 0

mc_2015 = np.load('./2015MCS_1.npy',encoding = "latin1")
mc_2015[isnan(mc_2015)] = 0

mc_2014 = np.load('./2014MCS_1.npy',encoding = "latin1")
mc_2014[isnan(mc_2014)] = 0

mc_average = (mc_2018 + mc_2017 + mc_2016 + mc_2015 + mc_2014)/5

mc_hl = np.zeros((2,397,5))

for i in range(397):
    for j in range(5):
        low = np.percentile(mc_average[:,i,j],2.5)
        high = np.percentile(mc_average[:,i,j],97.5)
        mc_hl[0,i,j] = low
        mc_hl[1,i,j] = high

mc_fin = np.zeros((397,5)) 
mc_fin = pd.DataFrame(mc_fin)
mc_hl = np.round(mc_hl,15) 

for i in range(397):
    for j in range(5):
        mc_fin.iloc[i,j] = "[" + str(mc_hl[0,i,j]) + "," + str(mc_hl[1,i,j]) + "]"