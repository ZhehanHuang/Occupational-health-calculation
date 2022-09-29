# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 18:55:56 2022

@author: 黄喆晗
"""

import pyspa
import pandas as pd
import numpy as np



with pd.ExcelWriter('output.xlsx') as writer:
    for i in range(404):
        sc = pyspa.get_spa(target_ID = i+1, max_stage = 2, a_matrix_file_path ='A_matrix_template.csv', infosheet_file_path='Infosheet_template.csv', thresholds_file_path='Thresholds_template.csv')
        sc.export_to_csv('spa_results_%d.txt' % (i))
        with open('spa_results_%d.txt' % (i), 'r') as f, open('output_%d.txt' % (i), 'w') as fo:
            for line in f:
                fo.write(line.replace('"', '').replace("'", ""))
        column_names = [j for j in range(0, 5)]
        df = pd.read_csv('output_%d.txt' % (i),sep='\t',header=None, names=column_names)
        df.to_excel(writer, sheet_name='%d' %(i),encoding="utf_8_sig",index=False,header=False) 

def read_data(i):
    cf = pd.read_excel('output.xlsx', sheet_name=i,header = None)
    cf1 = cf.iloc[15:,:]
    cf1.columns = ['percentage','direct impact','total impact','stage 1','stage 2']
    cf1.insert(0,'end sector', cf.iloc[0,1])
    cf1['percentage'] = cf1['percentage'].str[:-1]
    cf1['percentage'] = cf1['percentage'].astype(float)
    cf1['percentage'] = cf1['percentage']/100
    cf1.iloc[:,1:4] = cf1.iloc[:,1:4].astype(float)
    cf1 = cf1.reset_index(drop=True)
    return cf1

def calculate_SPA(lst_spa):
    lst = pd.DataFrame(np.zeros((0,6)))
    lst.columns = ['end sector','percentage','direct impact','total impact','stage 1','stage 2']
    for k in range(lst_spa.shape[0]):
        if lst_spa.iloc[k,2] != 0:
            data = read_data(k)
            data.iloc[:,2] = data.iloc[:,2] * lst_spa.iloc[k,2]
            data.iloc[:,3] = data.iloc[:,3] * lst_spa.iloc[k,2]
            lst = lst.append(data)
            
    sum = 0
    for m in range(lst.shape[0]):
        if lst.iloc[m,4] == 'DIRECT Stage 0':
            sum = sum + lst.iloc[m,3]

    m = 0        
    for m in range(lst.shape[0]):
        lst.iloc[m,1] = lst.iloc[m,2]/sum

    lst = lst.sort_values('percentage', ascending=False)
    lst = lst.reset_index(drop=True)
    
    return lst    

good_list = pd.read_excel('list.xlsx', usecols='B:D', sheet_name = 0)
good_list['Value'] = good_list['Value'].astype(float)
lst_chair = calculate_SPA(good_list)

all_list = pd.read_excel('list.xlsx', usecols='B:D', sheet_name = 1)
all_list['Value'] = all_list['Value'].astype(float)
lst_all = calculate_SPA(all_list)
