#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Tue May 30 08:48:30 2023

@author: jgabantxo_ext
"""

#%% IMPORT STANDARD AND CUSTOM MODULES

#----------------#
# Import modules #
#----------------#

from pathlib import Path
import sys

import timeit

import numpy as np
import pandas as pd

#-----------------------#
# Import custom modules #
#-----------------------#

# Find the path of the Python toolbox #
home_PATH = Path.home()
sys.path.append(str(home_PATH))

import get_pytools_path
fixed_path = get_pytools_path.return_custom_path()

# Enumerate custom modules and their paths #
#------------------------------------------#

custom_mod1_path = f"{fixed_path}/strings"
                                        
# Add the paths to the 'path' attribute of module 'sys' #
#-------------------------------------------------------#

sys.path.append(custom_mod1_path)

# Perform whole or partial module importations #
#----------------------------------------------#

import information_output_formatters

#--------------------------------------------------#
# Define imported modules' objname_unevennction call shortcuts #
#--------------------------------------------------#

print_format_string = information_output_formatters.print_format_string
format_string = information_output_formatters.format_string

#%% DEFINE FUNCTIONS

def df_to_structured_array(df):
    records  =  df.to_records(index = False)
    data  =  np.array(records, dtype = records.dtype.descr)
    return data

def a_sel(a, rows, cols):
    a1 = a[rows][:, cols]
    return a1
    
def sa_sel(sa, rows, cols):
    sa1 = sa[rows][cols]
    return sa1
    
def df_sel(df, rows, cols):
    df1 = df.iloc[rows,cols]
    return df1

#%% INPUT PARAMETERS

# Basic parameters #
nrows = int(1e5)
step = 0.05

limit_tuple = (0, 300)
array_size = (nrows, 4)
    
# Random number and interval arrays and their characteristics #
a = np.random.randint(*limit_tuple, size = array_size) 
la = len(a)
itvs = [pd.Interval(i,i+step, closed = "left") for i in range(la)]

# Data selection coordinates #
cols = ['itvs','a', 'b', 'c', 'd']
rows = np.sort(np.random.randint(0,la,size = la//2))
icols = [2,4]

# Preformatted strings #
header_str = "Execution times for {} loops with {} reps (in seconds)"

exec_time_res_str = """{}\n{}
· Numpy generic: {}, best {}
· Numpy structured array: {}, best {}
· Pandas: {}, best {}
"""

#%% Data conversion to array, Pandas Dataframe and structured array, respectively #

a = np.append(np.array(itvs)[:, np.newaxis], a, axis = 1)
df = pd.DataFrame(a, columns = cols)
sa = df_to_structured_array(df)

#%% PERFORMANCE MONITORING

# Define repeat and trial amounts #
repeats = 5
trials = 5000

# Define setup to pass it into 'timeit' module #
array_sel_setup = "a_sel(a,rows,icols)"
struct_array_sel_setup = "sa_sel(sa,rows,icols)"
df_sel_setup = "df_sel(df,rows,icols)"

# Perform the trials with block repetitions #
a_sel_res = np.round(timeit.repeat(array_sel_setup, repeat = repeats, number = trials, globals = globals()),4)
sa_sel_res = np.round(timeit.repeat(struct_array_sel_setup, repeat = repeats, number = trials, globals = globals()),4)
df_sel_res = np.round(timeit.repeat(df_sel_setup, repeat = repeats, number = trials, globals = globals()),4)

#%% PRINT RESULTS

arg_tuple_header = (repeats, trials)
header_formatted = format_string(header_str, arg_tuple_header)
lhf = len(header_formatted)

arg_tuple_exec_time = (header_formatted, 
                       f"{'=':=^lhf}",
                       a_sel_res, min(a_sel_res),
                       sa_sel_res, min(sa_sel_res),
                       df_sel_res, min(df_sel_res))
print_format_string(exec_time_res_str, arg_tuple_exec_time)                 
