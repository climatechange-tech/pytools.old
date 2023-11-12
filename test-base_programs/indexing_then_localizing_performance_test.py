# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 09:03:17 2023

@author: jgabantxo_ext
"""


import numpy as np
import pandas as pd

import timeit


def a_sel(a, rows, cols):
    a1=a[rows][:, cols]
    return a1
    
def df_sel(df, rows,cols):
    df1=df.loc[rows,cols]
    return df1

def a_where(a,val1,val2):
    anpw=np.where((a==val1) * (a==val2))
    return anpw
    
def df_where(df,val1,val2):
    dfw=df[(df==val1)&(df==val2)]
    return dfw
        
    
n=int(1e6)

a=np.random.randint(0,n,size=(n,4))
la=len(a)
step=0.05


cols=['itvs','a', 'b', 'c', 'd']
rows=np.unique(np.random.randint(0,n,size=la//2))
cols1=[2,3]
cols1df=cols[slice(2,5,2)]
val1=27
val2=54

itvs=[pd.Interval(i,i+step, closed="left") for i in range(la)]

a=np.append(np.array(itvs)[:, np.newaxis], a, axis=1)

df=pd.DataFrame(a, columns=cols)

repeats=10
number=1

a_sel_res=np.round(timeit.repeat("a_sel(a,rows,cols1)", repeat=repeats, number=number, globals=globals()),3)
df_sel_res=np.round(timeit.repeat("df_sel(df,rows,cols1df)", repeat=repeats, number=number, globals=globals()),3)

a_where_res=np.round(timeit.repeat("a_where(a,val1,val2)", repeat=repeats, number=number, globals=globals()),3)
df_where_res=np.round(timeit.repeat("df_where(df,val1,val2)", repeat=repeats, number=number, globals=globals()),3)




res_table="""Execution times for {} loops with {} reps:
    
INDEXING
--------
    
Numpy generic: {}; best {}
Pandas: {}; best {}

LOCALIZING
----------
    
Numpy where: {}; best {}
Pandas: {}; best {}

"""

print(res_table.format(repeats, number, 
                       a_sel_res, min(a_sel_res),
                       df_sel_res, min(df_sel_res),
                       a_where_res, min(a_where_res),
                       df_where_res, min(df_where_res)))
