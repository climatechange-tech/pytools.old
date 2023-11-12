# -*- coding: utf-8 -*-
"""
Created on Tue May 30 08:48:30 2023

@author: jgabantxo_ext
"""

import numpy as np
import pandas as pd

import timeit

def df_to_structured_array(df):
    records = df.to_records(index=False)
    data = np.array(records, dtype=records.dtype.descr)
    return data

def a_sel(a, rows, cols):
    a1=a[rows][:, cols]
    return a1
    
def sa_sel(sa, rows,cols):
    sa1=sa[rows][cols]
    return sa1
    
def df_sel(df, rows,cols):
    df1=df.loc[rows,cols]
    return df1
    


a=np.random.randint(0,300,size=(100000,4))
la=len(a)
step=0.05

cols=['itvs','a', 'b', 'c', 'd']
rows=np.random.randint(0,la,size=la//2)
cols1=[2,4]
itvs=[pd.Interval(i,i+step, closed="left") for i in range(la)]

a=np.append(np.array(itvs)[:, np.newaxis], a, axis=1)

df=pd.DataFrame(a, columns=cols)

sa=df_to_structured_array(df)


repeats=5
number=5000

a_sel_res=np.round(timeit.repeat("a_sel(a,rows,cols1)", repeat=repeats, number=number, globals=globals()),4)
sa_sel_res=np.round(timeit.repeat("sa_sel(sa,rows,cols1)", repeat=repeats, number=number, globals=globals()),4)
df_sel_res=np.round(timeit.repeat("df_sel(df,rows,cols1)", repeat=repeats, number=number, globals=globals()),4)

res_table="""Execution times for {} loops with {} reps:
Numpy generic: {}, best {}
Numpy structured array: {}, best {}
Pandas: {}, best {}
"""

print(res_table.format(repeats, number, 
                       a_sel_res, min(a_sel_res),
                       sa_sel_res, min(sa_sel_res),
                       df_sel_res, min(df_sel_res)))
