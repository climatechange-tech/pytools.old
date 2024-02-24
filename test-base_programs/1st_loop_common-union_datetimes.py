#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Wed Apr 12 11:46:48 2023

@author: jgabantxo_ext
"""

#----------------#
# Import modules #
#----------------#

from pathlib import Path
import sys

import pandas as pd

#-----------------------#
# Import custom modules #
#-----------------------#

# Find the path of the Python toolbox #
home_PATH = Path.home()
sys.path.append(str(home_PATH))

import get_pytools_path
fixed_dirpath = get_pytools_path.return_custom_path()

# Enumerate custom modules and their paths #
#------------------------------------------#

custom_mod1_path = f"{fixed_dirpath}/time_handling"
                                        
# Add the paths to the 'path' attribute of module 'sys' #
#-------------------------------------------------------#

sys.path.append(custom_mod1_path)

# Perform whole or partial module importations #
#----------------------------------------------#

import datetime_operators
import time_formatters

#--------------------------------------------------#
# Define imported modules' function call shortcuts #
#--------------------------------------------------#

datetime_range_operator = datetime_operators.datetime_range_operator
natural_year = datetime_operators.natural_year
time_format_tweaker = time_formatters.time_format_tweaker

#------------------#
# Input parameters #
#------------------#

# Time format strings and frequency 
customizing_tfs1 = "%d/%m/%Y %H:%M"
customizing_tfs2 = "%b%y"
customizing_tfs3 = "%d%m%y %H%M"
time_freq = "10min"
time_col = "date"

# Start and end dates provided by TDEM #
dt_dict = {
    "Narzym_1" : ["01/11/2021 9:40", "31/08/2023 23:50"],
    "Narzym_Sodar_1B" : ["19/02/2021 15:00", "16/09/2022 15:00"],
    "Narzym_Sodar_7" : ["16/09/2022 16:30", "31/08/2023 23:50"],
    "Vortex_ERA5_R_Narzym_1" : ["31/12/1990 23:00", "04/09/2023 22:00"],
    "Vortex_ERA5_Narzym_1" : ["31/12/1990 23:00", "04/09/2023 22:00"]
}

dt_dict_keys = list(dt_dict.keys())

for eddk in dt_dict.keys():
    unformatted_timeList = dt_dict[eddk].copy()
    dt_dict[eddk] = [time_format_tweaker(ut, time_fmt_str=customizing_tfs1)
                     for ut in unformatted_timeList]
                   
# Indices and station names #
stat_name_dict = {
    i : dt_dict_keys[i]
    for i in range(len(dt_dict))
}

# Parent and child selection cases #
idx_parent = 1
idx_child = 0

stat_name_parent = stat_name_dict[idx_parent]
extreme_dates_parent = dt_dict[stat_name_parent]

stat_name_child = stat_name_dict[idx_child]
extreme_dates_child = dt_dict[stat_name_child]

# Times as a result of the comparation #
#--------------------------------------#

date_ranges_parent = pd.DataFrame(pd.date_range(extreme_dates_parent[0], 
                                                extreme_dates_parent[1],
                                                freq=time_freq),
                                  columns=[time_col])

date_ranges_child = pd.DataFrame(pd.date_range(extreme_dates_child[0], 
                                               extreme_dates_child[1],
                                               freq=time_freq),
                                  columns=[time_col])

# Times in common #
common_times = datetime_range_operator(date_ranges_parent, 
                                       date_ranges_child,
                                       operator="inner")
try:
    common_times_start = common_times.iloc[0]
 
except:
    raise ValueError(f"Parent station '{stat_name_parent}' "
                     f"and child station '{stat_name_child}' "
                     "have no times in common.")
    
custom_common_times_start1 = time_format_tweaker(common_times_start,
                                                 time_fmt_str=customizing_tfs2)
custom_common_times_start2 = time_format_tweaker(common_times_start,
                                                 time_fmt_str=customizing_tfs3)

common_times_end = common_times.iloc[-1]
custom_common_times_end1 = time_format_tweaker(common_times_end,
                                              time_fmt_str=customizing_tfs2)
custom_common_times_end2 = time_format_tweaker(common_times_end,
                                              time_fmt_str=customizing_tfs3)

# Extension times #
extension_times = datetime_range_operator(date_ranges_parent, 
                                          date_ranges_child,
                                          operator="outer")

extension_times_start = extension_times.iloc[0]
custom_extension_times_start1 = time_format_tweaker(extension_times_start,
                                                    time_fmt_str=customizing_tfs2)
custom_extension_times_start2 = time_format_tweaker(extension_times_start,
                                                    time_fmt_str=customizing_tfs3)

extension_times_end = extension_times.iloc[-1]
custom_extension_times_end1 = time_format_tweaker(extension_times_end,
                                                  time_fmt_str=customizing_tfs2)
custom_extension_times_end2 = time_format_tweaker(extension_times_end,
                                                  time_fmt_str=customizing_tfs3)

# Time deltas #
#-------------#

timeDeltaCommon = abs(common_times_start - common_times_end)[0]
timeDeltaExtension = abs(extension_times_start - extension_times_end)[0]

# Output info table's main features #
#-----------------------------------#

stat_comp_header = f"Comparation between {stat_name_parent} and {stat_name_child}"

number_sign_list = ['#' for _ in range(len(stat_comp_header))]
number_sign_str = ''.join(number_sign_list)

correlation_name = f"{stat_name_parent}_{stat_name_child}_H_"\
                   f"({custom_common_times_start1}-{custom_common_times_end1})_N1"

# Comparation result reporting table #
#------------------------------------#

comparation_info_str = """
{}
{}

Common times
------------
    
Start : {} = {} = {}
End   : {} = {} = {}

Time delta = {}

Extension times
---------------
    
Start : {} = {} = {}
End   : {} = {} = {}

Time delta = {}

Wind speed correlation name
---------------------------

{}
"""

print(comparation_info_str.format(stat_comp_header,
                               number_sign_str,
                               common_times_start[0],
                               custom_common_times_start1,
                               custom_common_times_start2,
                               common_times_end[0],
                               custom_common_times_end1,
                               custom_common_times_end2,
                               timeDeltaCommon,
                               extension_times_start[0],
                               custom_extension_times_start1,
                               custom_extension_times_start2,
                               extension_times_end[0],
                               custom_extension_times_end1,
                               custom_extension_times_end2,
                               timeDeltaExtension,
                               correlation_name))
