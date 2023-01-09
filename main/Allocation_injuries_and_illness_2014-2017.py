# -*- coding: utf-8 -*-
"""
Created on Fri Dec 31 01:38:04 2021

@author: huangzehan
"""

import pandas as pd

'''Step1：Import original data'''
coding_exist = pd.read_excel(r'.\data\original_data\2017\cd_r1_2017_SL.xlsx', skiprows=2, usecols='A:S')
# coding_exist = pd.read_excel(r'.\data\original_data\2016\cd_r1_2016.xlsx', skiprows=2, usecols='A:S')
# coding_exist = pd.read_excel(r'.\data\original_data\2015\ostb4753.xlsx', skiprows=2, usecols='A:S')
# coding_exist = pd.read_excel(r'.\data\original_data\2014\ostb4367.xlsx', skiprows=2, usecols='A:S')
coding_exist = coding_exist.replace('-',0)
coding_exist = coding_exist.replace('–',0)

# Reallocate "Total" column under "cuts, lacerations, punctures" catagory (The method is to distribute the uncounted data equally to each counted data)
unaccounted = coding_exist.loc[:,'Total'] - coding_exist.loc[:,'Cuts, lacerations'] - coding_exist.loc[:,'Punctures (except gunshot wounds)']
coding_exist.loc[:,'Cuts, lacerations'] = coding_exist.loc[:,'Cuts, lacerations'] + 0.5 * unaccounted
coding_exist.loc[:,'Punctures (except gunshot wounds)'] = coding_exist.loc[:,'Punctures (except gunshot wounds)'] + 0.5 * unaccounted

# Remove columns named "Total cases", "Total", "With sprains","With fractures", "Multiple traumatic injuries (Total)"
coding_exist = coding_exist.drop(columns=[coding_exist.columns[2], coding_exist.columns[5], coding_exist.columns[-4], coding_exist.columns[-3]])

# Remove rows with null NAICS codes
coding_exist = coding_exist.dropna(subset=['NAICS code(2)'])
coding_exist['NAICS code(2)'] = coding_exist['NAICS code(2)'].astype(str)

# Import all 6-digit industries
coding_total = pd.read_excel(r'.\data\support_data\total_6-level_industry.xlsx', sheet_name = 0, usecols='A:B')
coding_total['2012 NAICS Code'] = coding_total['2012 NAICS Code'].astype(str)

# Insert the rating of the industry
coding_exist.insert(2,'NAICS coding level',0)
for z in range(coding_exist.shape[0]):
    if (coding_exist.iloc[z,1])[-4:] == '0000':
        coding_exist.iloc[z,2] = 2
    elif len(coding_exist.iloc[z,1]) != 6:
        coding_exist.iloc[z,2] = 2
    elif (coding_exist.iloc[z,1])[-3:] == '000':
        coding_exist.iloc[z,2] = 3
    elif (coding_exist.iloc[z,1])[-2:] == '00':
        coding_exist.iloc[z,2] = 4
    elif coding_total.iloc[:,0].str.contains(coding_exist.iloc[z,1]).any():
        coding_exist.iloc[z,2] = 6
    else: 
        coding_exist.iloc[z,2] = 5

# Retain industries with ranks 2 and 6
coding_exist = coding_exist[-coding_exist.iloc[:,2].isin([1,3,4,5])]

# Take out industries with ranks 2 and 6 respectively
coding_level2 = coding_exist[-coding_exist.iloc[:,2].isin([6])]
coding_level6 = coding_exist[-coding_exist.iloc[:,2].isin([2])]

'''Step2：Screen for 6-digit industries with no data'''
coding_level6['NAICS code(2)'] = coding_level6['NAICS code(2)'].astype(str)

coding_merge = pd.merge(coding_total, coding_level6, how = 'left', left_on = ['2012 NAICS Code'], right_on = ['NAICS code(2)'])

coding_level6_left = coding_merge.copy()
j = 0
for k in range(coding_merge.shape[0]):
    if coding_merge.iloc[k,2] != coding_merge.iloc[k,2]:
        coding_level6_left.iloc[j,:] = coding_merge.iloc[k,:]
        j = j + 1
        
coding_level6_left = coding_level6_left.iloc[:j-1,:]
coding_level6_left = coding_level6_left.drop(columns = [coding_level6_left.columns[2], coding_level6_left.columns[3], coding_level6_left.columns[4]])

'''Step3：Counting for allocation to fill vacant values'''
coding_counting = coding_level2.iloc[:,0:2]
coding_counting['exist'] = ''
coding_counting['left'] = ''
coding_counting['sum'] = ''
coding_counting = coding_counting.reset_index()
coding_counting = coding_counting.drop(columns = [coding_counting.columns[0]])

def counting1(a,b,c,d,column):
    e = 0
    for l in range(a.shape[0]):
        string = a.iloc[l,column]
        if string[:2] == b:
            e = e + 1
    coding_counting.iloc[c,d] = e
    
def counting2(a,b,c,d,f,column):
    e = 0
    for l in range(a.shape[0]):
        string = a.iloc[l,column]
        if string[:2] == b or string[:2] == c:
            e = e + 1
    coding_counting.iloc[d,f] = e
    
def counting3(a,b,c,d,f,g,column):
    e = 0
    for l in range(a.shape[0]):
        string = a.iloc[l,column]
        if string[:2] == b or string[:2] == c or string[:2] == d:
            e = e + 1
    coding_counting.iloc[f,g] = e

# Counting 6-digit industries with available data
def counting_all(a,b,c,d):
    counting1(a, '11', b, c, d)
    counting1(a, '21', b+1, c, d)
    counting1(a, '23', b+2, c, d)
    counting3(a, '31', '32', '33', b+3, c, d)
    counting1(a, '22', b+4, c, d)
    counting1(a, '42', b+5, c, d)
    counting2(a, '44', '45', b+6, c, d)
    counting2(a, '48', '49', b+7, c, d)
    counting1(a, '51', b+8, c, d)
    counting1(a, '52', b+9, c, d)
    counting1(a, '53', b+10, c, d)
    counting1(a, '54', b+11, c, d)
    counting1(a, '55', b+12, c, d)
    counting1(a, '56', b+13, c, d)
    counting1(a, '61', b+14, c, d)
    counting1(a, '62', b+15, c, d)
    counting1(a, '71', b+16, c, d)
    counting1(a, '72', b+17, c, d)
    counting1(a, '81', b+18, c, d)
    
counting_all(coding_level6, 0, 2, 1)

# Counting 6-digit industries with vacant values
counting_all(coding_level6_left, 0, 3, 0)

coding_counting.iloc[:,4] = coding_counting.iloc[:,3] + coding_counting.iloc[:,2] 

# Calculate the sum of existing data classification data
coding_data = coding_level2.copy()
for l in range(coding_counting.shape[0]):
    if l == 0:
        m = 0
    else:
        m = coding_counting.iloc[:l,2].sum()
    n = coding_counting.iloc[l,2]
    coding_data.iloc[l,3:] = coding_level6.iloc[m:m+n,3:].sum()
coding_data = coding_data.drop(columns = [coding_data.columns[2]])

# Calculate the sum of missing category data
coding_data_left = coding_data.copy()
coding_data_left.iloc[:,2:] = coding_level2.iloc[:,3:] - coding_data.iloc[:,2:]

# Distribute the sum of missing data equally to all industries
coding_average_all = coding_data.copy()
for o in range(coding_average_all.shape[0]):
    coding_average_all.iloc[o,2:] = coding_data_left.iloc[o,2:] / coding_counting.iloc[o,4]
coding_average_all.iloc[:,2:] = coding_average_all.iloc[:,2:].astype(int)

## Backfill the missing data after calculating the average
coding_level6_left_fix_all = coding_level6_left.copy()
for l in range(coding_counting.shape[0]):
    if l == 0:
        m = 0
    else:
        m = coding_counting.iloc[:l,3].sum()
    n = coding_counting.iloc[l,3]
    coding_level6_left_fix_all.iloc[m:m+n,2:] = coding_average_all.iloc[l,2:]

coding_level6_fix_all = coding_level6.copy()
coding_level6_fix_all = coding_level6_fix_all.drop(columns=[coding_level6_fix_all.columns[2]])
for p in range(coding_counting.shape[0]):
    if p == 0:
        x = 0
    else:
        x = coding_counting.iloc[:p,2].sum()
    y = coding_counting.iloc[p,2]
    coding_level6_fix_all.iloc[x:x+y,2:] = coding_level6.iloc[x:x+y,3:] + coding_average_all.iloc[p,2:]

## Merge existing data with fill data
coding_fix_all = coding_level6_fix_all.append(coding_level6_left_fix_all, ignore_index = True)
a = pd.DataFrame(coding_level6.shape)
b = a.iloc[0,0]
coding_fix_all.iloc[b:,0] = coding_level6_left_fix_all.iloc[:,1]
coding_fix_all.iloc[b:,1] = coding_level6_left_fix_all.iloc[:,0]
