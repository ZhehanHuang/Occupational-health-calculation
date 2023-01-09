# -*- coding: utf-8 -*-
"""
Created on Wed May 25 15:36:20 2022

@author: 黄喆晗
"""

import pandas as pd
import numpy as np
from numpy import isnan, isinf

'''Step1 Import total cases of non-fatal injuries and illnesses by industry (NAICS codes)'''
nature2018 = pd.read_excel(r'.\data\allocation_data\Allocation.xlsx', sheet_name = 1, usecols='A:O') # 2018
nature2017 = pd.read_excel(r'.\data\allocation_data\Allocation_2014-2017.xlsx', sheet_name = 0, usecols='A:O') # 2017
nature2016 = pd.read_excel(r'.\data\allocation_data\Allocation_2014-2017.xlsx', sheet_name = 2, usecols='A:O') # 2016
nature2015 = pd.read_excel(r'.\data\allocation_data\Allocation_2014-2017.xlsx', sheet_name = 4, usecols='A:O') # 2015
nature2014 = pd.read_excel(r'.\data\allocation_data\Allocation_2014-2017.xlsx', sheet_name = 6, usecols='A:O') # 2014

'''Step2.1 Import total cases of non-fatal injuries and diseases by age group (BLS division)'''
age2018 = pd.read_excel(r'.\data\allocation_data\Allocation.xlsx', sheet_name = 2, usecols='A:K') # 2018
age2017 = pd.read_excel(r'.\data\allocation_data\Allocation_2014-2017.xlsx', sheet_name = 1, usecols='A:K') # 2017
age2016 = pd.read_excel(r'.\data\allocation_data\Allocation_2014-2017.xlsx', sheet_name = 3, usecols='A:K') # 2016
age2015 = pd.read_excel(r'.\data\allocation_data\Allocation_2014-2017.xlsx', sheet_name = 5, usecols='A:K') # 2015
age2014 = pd.read_excel(r'.\data\allocation_data\Allocation_2014-2017.xlsx', sheet_name = 7, usecols='A:K') # 2015

'''Step2.2 Matching the age group of the BLS classification to the WHO classification'''
def age_allocation(data):
    age_WHO = data.iloc[:,0:3]
    age_WHO['15 to 44'] = data['14 to 15'] + data['16 to 19'] + data['20 to 24'] + data['25 to 34'] + data['35 to 44']
    age_WHO['45 to 59'] = data['45 to 54'] + data['55 to 64'] * 0.5
    age_WHO['60 to 80'] = data['55 to 64'] * 0.5 + data['65 and over']
    return age_WHO

age_WHO2018 = age_allocation(age2018)
age_WHO2017 = age_allocation(age2017)
age_WHO2016 = age_allocation(age2016)
age_WHO2015 = age_allocation(age2015)
age_WHO2014 = age_allocation(age2014)

'''Step3.1 Imported long-short split coefficient for different injuries and illness'''
split = pd.read_excel(r'.\data\support_data\support_data.xlsx', sheet_name=2)

'''Step3.2 Import the duration of short-term injuries and illness'''
duration_ST = pd.read_excel(r'.\data\support_data\support_data.xlsx', sheet_name=4, usecols='A:C') # BLS
duration_ST = duration_ST.loc[:13,'Median days away from work'] / 250 # Unit is year, 250 working days a year

'''Step3.3 Import the duration of lifelong injuries and illness'''
duration_LL = pd.read_excel(r'.\data\support_data\support_data.xlsx', sheet_name=3, usecols='A:D')
duration_LL = duration_LL.iloc[:,-1] # Use gender-neutral remaining life as duration

'''Step3.4 Import the weight (severity) of short-term injuries and illness'''
weight_ST = pd.read_excel(r'.\data\support_data\support_data.xlsx', sheet_name=0)
weight_ST = pd.Series(weight_ST.iloc[:,1])
    
'''Step3.5 Import the weight (severity) of lifelong injuries and illness'''
weight_LL = pd.read_excel(r'.\data\support_data\support_data.xlsx', sheet_name=1)
weight_LL = pd.Series(weight_LL.iloc[:,1])

'''Step4.1 Calculate cases for each industry (per BLS code), for each age group and for each non-fatal injuries or illness''' 
def injury_age(nature, age):
     np_industry_injury_age = np.zeros((nature.shape[0],nature.shape[1]-2,age.shape[1]-3))
     for i in range(nature.shape[0]):   # each industry
         for j in range(nature.shape[1]-2): # each non-fatal injury or illness
             for k in range(age.shape[1]-3): # each age group
                 np_industry_injury_age[i,j,k] = age.iloc[i,3] / age.iloc[i,k+2] * nature.iloc[i,j+2]
     return np_industry_injury_age

industry_injury_age_2018 = injury_age(nature2018, age_WHO2018)
industry_injury_age_2017 = injury_age(nature2017, age_WHO2017)
industry_injury_age_2016 = injury_age(nature2016, age_WHO2016)
industry_injury_age_2015 = injury_age(nature2015, age_WHO2015)
industry_injury_age_2014 = injury_age(nature2014, age_WHO2014)

'''Step4.2 Calculate the total number of cases of short-term nonfatal injuries for each injury for each age group'''
short_coefficient = split.loc[:,'Short-term']
def short_injury(nature, age, industry_injury_age):
     np_industry_shortinj_age = np.zeros((nature.shape[0],nature.shape[1]-2,age.shape[1]-3))
     for i in range(nature.shape[0]): # each industry
         for k in range(age.shape[1]-3): # each age group
             np_industry_shortinj_age[i,:,k] = short_coefficient * industry_injury_age[i,:,k]
     return np_industry_shortinj_age

industry_shortinj_age_2018 = short_injury(nature2018, age_WHO2018, industry_injury_age_2018)
industry_shortinj_age_2017 = short_injury(nature2017, age_WHO2017, industry_injury_age_2017)
industry_shortinj_age_2016 = short_injury(nature2016, age_WHO2016, industry_injury_age_2016)
industry_shortinj_age_2015 = short_injury(nature2015, age_WHO2015, industry_injury_age_2015)
industry_shortinj_age_2014 = short_injury(nature2014, age_WHO2014, industry_injury_age_2014)

'''Step4.3 Calculate the total number of cases of lifelong nonfatal injuries for each injury for each age group'''
long_coefficient = split.loc[:,'Life-long']
def long_injury(nature, age, industry_injury_age):
     np_industry_longinj_age = np.zeros((nature.shape[0],nature.shape[1]-2,age.shape[1]-3))
     for i in range(nature.shape[0]): # each industry
         for k in range(age.shape[1]-3): # each age group
             np_industry_longinj_age[i,:,k] = long_coefficient * industry_injury_age[i,:,k]
     return np_industry_longinj_age

industry_longinj_age_2018 = long_injury(nature2018, age_WHO2018, industry_injury_age_2018)
industry_longinj_age_2017 = long_injury(nature2017, age_WHO2017, industry_injury_age_2017)
industry_longinj_age_2016 = long_injury(nature2016, age_WHO2016, industry_injury_age_2016)
industry_longinj_age_2015 = long_injury(nature2015, age_WHO2015, industry_injury_age_2015)
industry_longinj_age_2014 = long_injury(nature2014, age_WHO2014, industry_injury_age_2014)

'''Step5.1 Calculate YLD of short-term injuries and illness'''
def YLD_ST(industry_shortinj_age, nature):
     short_injuries = pd.DataFrame(industry_shortinj_age.sum(axis=2)).fillna(0) # Superimposed along the age groups
     yld_short = pd.DataFrame(short_injuries * weight_ST* duration_ST)
     yld_short.columns = nature.columns[2:]
     yld_short.insert(0,'Industry',nature.iloc[:,0])
     yld_short.insert(1,'NAICS code',nature.iloc[:,1])
     return yld_short

yld_short2018 = YLD_ST(industry_shortinj_age_2018, nature2018)
yld_short2017 = YLD_ST(industry_shortinj_age_2017, nature2017)
yld_short2016 = YLD_ST(industry_shortinj_age_2016, nature2016)
yld_short2015 = YLD_ST(industry_shortinj_age_2015, nature2015)
yld_short2014 = YLD_ST(industry_shortinj_age_2014, nature2014)

'''Step5.2 Calculate YLD of lifelong injuries and illness'''
def YLD_LL(industry_longinj_age, nature):
     yld_long = nature.copy()
     i = 0
     j = 0
     for i in range(nature.shape[0]): # each industry
         for j in range(nature.shape[1]-2): # each non-fatal injury or illness
             yld_long.iloc[i,j+2] = sum(industry_longinj_age[i,j,:] * duration_LL* weight_LL[j])
     return yld_long

yld_long2018 = YLD_LL(industry_longinj_age_2018, nature2018)
yld_long2017 = YLD_LL(industry_longinj_age_2017, nature2017)
yld_long2016 = YLD_LL(industry_longinj_age_2016, nature2016)
yld_long2015 = YLD_LL(industry_longinj_age_2015, nature2015)
yld_long2014 = YLD_LL(industry_longinj_age_2014, nature2014)

'''Step5.3 Calculate total YLD of non-fatal injuries and illness'''
def YLD_TOTAL(yld_long, yld_short, nature):
     yld_total = yld_short.iloc[:,2:] + yld_long.iloc[:,2:]
     yld_total.insert(0,'Industry',nature.iloc[:,0])
     yld_total.insert(1,'NAICS code',nature.iloc[:,1])
     return yld_total

yld_total2018 = YLD_TOTAL(yld_long2018, yld_short2018, nature2018)
yld_total2017 = YLD_TOTAL(yld_long2017, yld_short2017, nature2017)
yld_total2016 = YLD_TOTAL(yld_long2016, yld_short2016, nature2016)
yld_total2015 = YLD_TOTAL(yld_long2015, yld_short2015, nature2015)
yld_total2014 = YLD_TOTAL(yld_long2014, yld_short2014, nature2014)

'''Step6.1 Import total output of industries (g)'''
g = pd.read_excel(r'.\data\original_data\USEEIOv2.0.xlsx', sheet_name=23, usecols='A:B')
g['USEEIO_Code'] = g['USEEIO_Code'].map(lambda x: str(x)[:-3])
g['USEEIO_Code'] = g['USEEIO_Code'].astype(str)

'''Step6.2 Import total output of commodities (q)'''
q = pd.read_excel(r'.\data\original_data\USEEIOv2.0.xlsx', sheet_name=22, usecols='A:B')
q['USEEIO_Code'] = q['USEEIO_Code'].map(lambda x: str(x)[:-3])
q['USEEIO_Code'] = q['USEEIO_Code'].astype(str)

'''Step6.3 Import make matrix'''
make_mat = pd.read_excel(r'.\data\original_data\USEEIOv2.0.xlsx', sheet_name=6, usecols='A:OV')
make_mat['USEEIO_Code'] = make_mat['USEEIO_Code'].astype(str)
make_mat['USEEIO_Code'] = make_mat['USEEIO_Code'].apply(lambda x:x[:6]).tolist()
make_mat_T = pd.DataFrame(make_mat.values.T, index=make_mat.columns, columns=make_mat.index)
make_mat_T[0] = make_mat_T[0].apply(lambda x:x[:6]).tolist()

'''Step6.4 Import direct requirements matrix'''
requ_mat = pd.read_excel(r'.\data\original_data\USEEIOv2.0.xlsx', sheet_name=9, usecols='A:OV')
requ_mat['USEEIO_Code'] = requ_mat['USEEIO_Code'].map(lambda x: str(x)[:-3])
requ_mat['USEEIO_Code'] = requ_mat['USEEIO_Code'].astype(str)

'''Step6.5 Import conversion matrix'''
Conv = pd.read_excel(r'.\data\support_data\CONV.xlsx', sheet_name=2, usecols='B:OR')
Conv['Category code'] = Conv['Category code'].astype(str)
Conv['Category code'] = Conv['Category code'].map(lambda x: str(x)[:-2])

'''Step7 Calculations of Worker Health Impacts over the Entire Supply Chain'''
def CFs(yld_total):

     '''Step7.1 Import YLD data'''
     DALY_total = yld_total
     DALY_total = DALY_total.rename(columns={'NAICS code':'Category code'})
     DALY_total['Category code'] = DALY_total['Category code'].astype(str)

     '''Step7.2 Complete conversion matrix'''    
     Conv_cut = pd.merge(DALY_total, Conv, on = ['Category code'])
     Conv_cut = Conv_cut.drop(columns = Conv_cut.columns[2:16])
     Conv_cut = Conv[0:1].append(Conv_cut, ignore_index=True)
     Conv_cut = Conv_cut.drop(columns = [Conv_cut.columns[0], Conv_cut.columns[-1]])
     Conv_cut.insert(0,'Category',Conv.iloc[:,0])
     Conv_cut[0:1] = Conv_cut[0:1].astype(str)
     Conv_cut[0:1] = Conv_cut.iloc[0,:].apply(lambda x:x[:6]).tolist()
     DALY_cut = pd.merge(DALY_total, Conv, on = ['Category code'])
     DALY_cut = DALY_cut.drop(columns = DALY_cut.columns[15:])
     
     # Find the transpose of the conversion matrix
     Conv_T = pd.DataFrame(Conv_cut.values.T, index=Conv_cut.columns, columns=Conv_cut.index)
     list_io_c = Conv_T.iloc[2:,0]
     list_io_c.columns = ['USEEIO_Code']

     '''Step7.3 Compute the intersection of g with the IO code in the conversion matrix'''     
     g_cut = pd.merge(list_io_c, g, left_on = [0], right_on = ['USEEIO_Code'])
     g_cut = g_cut.drop(columns = g_cut.columns[0])
     list_io_g = pd.DataFrame(g_cut.iloc[:,0])

     '''Step7.4 Convert NAICS codes to IO codes'''
     Conv_matrix = np.array(Conv_cut.iloc[1:,2:])
     DALY_matrix = np.array(DALY_cut.iloc[:,2:])
     Conv_matrix = Conv_matrix.astype(float)
     DALY_matrix = DALY_matrix.astype(float)
     DALY_matrix[isnan(DALY_matrix)] = 0
     DALY_matrix[isinf(DALY_matrix)] = 0    
     Conv_matrix[isnan(Conv_matrix)] = 0
     DALY_io_ini_np = np.dot(Conv_matrix.T, DALY_matrix)
     DALY_io_ini_df = pd.DataFrame(DALY_io_ini_np, index = list_io_c)
     DALY_io_ini_df['USEEIO_Code'] = DALY_io_ini_df.index
     DALY_io_fin_df = pd.merge(list_io_g, DALY_io_ini_df, on = ['USEEIO_Code'])

     '''Step7.5 Incorporate g into the calculation'''
     process_1 = DALY_io_fin_df.copy()
     i = 0
     for i in range(DALY_io_fin_df.shape[1]-1):
         process_1.iloc[:,i+1] = DALY_io_fin_df.iloc[:,i+1] / g_cut.iloc[:,1]

     '''Step7.6 Complete make matrix'''    
     make_mat_T_fin = pd.merge(list_io_g, make_mat_T, left_on = ['USEEIO_Code'], right_on = [0])
     make_mat_T_fin = make_mat_T[0:1].append(make_mat_T_fin, ignore_index=True)
     make_mat_T_fin = make_mat_T_fin.drop(columns = make_mat_T_fin.columns[0])
     list_io_v1 = pd.DataFrame(make_mat_T_fin.iloc[1:,-1])
     make_mat_fin = pd.DataFrame(make_mat_T_fin.values.T, index=make_mat_T_fin.columns, columns=make_mat_T_fin.index)
     list_io_v2 = pd.DataFrame(make_mat_fin.iloc[:411,0])

     '''Step7.7 Incorporate make matrix into the calculation'''
     process_1 = pd.merge(process_1, list_io_v1, on = ['USEEIO_Code'])
     process_1_np = np.array(process_1.iloc[:,1:])
     make_mat_np = np.array(make_mat_fin.iloc[:411,1:])
     process_2_np = np.matmul(make_mat_np, process_1_np)
     process_2_df = pd.DataFrame(process_2_np, index = list_io_v2.iloc[:,0])
     process_2_df['USEEIO_Code'] = process_2_df.index

     '''Step7.8 Complete commodity output (q)'''    
     q_cut = pd.merge(list_io_v2, q, left_on = [0], right_on = ['USEEIO_Code'])
     q_cut = q_cut.drop(columns = q_cut.columns[0])
     list_io_q = pd.DataFrame(q_cut.iloc[:,0])

     '''Step7.9 Incorporate q into the calculation'''
     process_2_df = pd.merge(list_io_q, process_2_df, on = ['USEEIO_Code'])
     process_3 = process_2_df.copy()
     j = 0
     for j in range(process_2_df.shape[1]-1):
         process_3.iloc[:,j+1] = process_2_df.iloc[:,j+1] / q_cut.iloc[:,1]
     process_3_np = np.array(process_3.iloc[:,1:])
     process_3_df = pd.DataFrame(process_3_np, index = list_io_q.iloc[:,0])
     process_3_cut = pd.merge(process_3_df, list_io_v1, on = ['USEEIO_Code'])
     process_3_cut = np.array(process_3_cut.iloc[:,1:])
         
     '''Step7.10 Complete direct requirements matrix'''    
     requ_mat_fin = pd.merge(list_io_q, requ_mat, on = ['USEEIO_Code'])
     requ_mat_fin = requ_mat[0:1].append(requ_mat_fin, ignore_index=True)
     requ_mat_T = pd.DataFrame(requ_mat_fin.values.T, index=requ_mat_fin.columns, columns=requ_mat_fin.index)
     requ_mat_T[0] = requ_mat_T[0].map(lambda x: str(x)[:-3])
     requ_mat_T[0] = requ_mat_T[0].astype(str)
     requ_mat_T_fin = pd.merge(list_io_q, requ_mat_T, left_on = ['USEEIO_Code'], right_on = [0])
     requ_mat_T_fin = requ_mat_T_fin.drop(columns = requ_mat_T_fin.columns[1])
     requ_mat_T_fin = requ_mat_T[0:1].append(requ_mat_T_fin, ignore_index=True)
     requ_mat_T_fin = requ_mat_T_fin.drop(columns = requ_mat_T_fin.columns[0])
     requ_mat_real = pd.DataFrame(requ_mat_T_fin.values.T, index=requ_mat_T_fin.columns, columns=requ_mat_T_fin.index)

     '''Step7.11 Incorporate A into the calculation'''
     A_np = np.array(requ_mat_real.iloc[:404,1:])
     i_A = np.eye(404)-A_np
     i_A = np.array(i_A, dtype='float')
     i_A_inv = np.linalg.inv(i_A)
     process_4_np = np.dot(i_A_inv.T, process_3_np)
       
     indirect_in_sec = np.zeros((404,2))
     x = 0
     for x in range(404):
         indirect_in_sec[x][0] = i_A_inv[x][x]
         indirect_in_sec[x][1] = 1
         
     indirect_in_sec = pd.DataFrame(indirect_in_sec)
     indirect_in_sec.iloc[:,0] = indirect_in_sec.iloc[:,0] - indirect_in_sec.iloc[:,1]
         
     indirect_in_sec = pd.concat([indirect_in_sec, list_io_q], axis=1)
     indirect_in_sec_cut = pd.merge(indirect_in_sec, list_io_v1, on = ['USEEIO_Code'])
         
     process_4_df = pd.DataFrame(process_4_np, index = list_io_q.iloc[:,0])
     process_4_1 = pd.merge(process_4_df, list_io_v1, on = ['USEEIO_Code'])
     process_4_1_np = np.array(process_4_1.iloc[:,1:])

     '''Step7.12 Calculate CFs'''
     cf_supply = process_4_1_np.sum(axis=1)
     cf_direct = process_3_cut.sum(axis=1)  # DALY per $ in the sector
     cf_indirect = cf_supply - cf_direct
     cf_indirect_in_sector = cf_indirect * indirect_in_sec_cut.iloc[:,0]
     cf_indirect_out_sector = cf_indirect - cf_indirect_in_sector
         
     cf_supply = pd.DataFrame(cf_supply)
     cf_direct = pd.DataFrame(cf_direct)
     cf_indirect = pd.DataFrame(cf_indirect)
     cf_indirect_in_sector = pd.DataFrame(cf_indirect_in_sector)
     cf_indirect_out_sector = pd.DataFrame(cf_indirect_out_sector)
     cf_total = list_io_v1.copy()
     cf_total.reset_index(drop=True, inplace=True)
     cf_total.insert(1,'Total Impact',cf_supply.iloc[:,0])
     cf_total.insert(2,'Direct Impact',cf_direct.iloc[:,0])
     cf_total.insert(3,'Indirect Impact',cf_indirect.iloc[:,0])
     cf_total.insert(4,'Supply chain impact in producer sector',cf_indirect_in_sector.iloc[:,0])
     cf_total.insert(5,'Supply chain impact in other sectors than producer sector',cf_indirect_out_sector.iloc[:,0])
     
     return cf_total

cf_total2018 = CFs(yld_total2018)
cf_total2017 = CFs(yld_total2017)
cf_total2016 = CFs(yld_total2016)
cf_total2015 = CFs(yld_total2015)
cf_total2014 = CFs(yld_total2014)

def CFs_average():
     cf_total_average = cf_total2018.copy()
     for i in range(cf_total_average.shape[0]):
         for j in range(cf_total_average.shape[1]-1):
             cf_total_average.iloc[i,j+1] = (cf_total2018.iloc[i,j+1]+cf_total2017.iloc[i,j+1]+cf_total2016.iloc[i,j+1]+cf_total2015.iloc[i,j+1]+cf_total2014.iloc[i,j+1])/5
     return cf_total_average

cf_total_average = CFs_average()

'''Step8 Case study'''
case = pd.read_excel(r'.\data\original_data\case study.xlsx', sheet_name=0, usecols='A:B')
case['Code'] = case['Code'].astype(str)
    
def case_study(case, cf_total):
        np_case = np.matrix(case.iloc[:,1])
        np_cf_total = np.matrix(cf_total_average.iloc[:,1])
        case_result = np.dot(np_case, np_cf_total.T)
        return case_result[0,0]
        
result = case_study(case, cf_total_average)
