#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Tue May 23 12:12:33 2023

@author: jgabantxo_ext

"""

#----------------#
# Import modules #
#----------------#

from pathlib import Path

import numpy as np
import pandas as pd

import glob

import warnings
import sys

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

custom_mod1_path = f"{fixed_path}/arrays_and_lists"
custom_mod2_path = f"{fixed_path}/pandas_data_frames"
custom_mod3_path = f"{fixed_path}/strings"
custom_mod4_path = f"{fixed_path}/time_handling"
                                        
# Add the paths to the 'path' attribute of module 'sys' #
#-------------------------------------------------------#

sys.path.append(custom_mod1_path)
sys.path.append(custom_mod2_path)
sys.path.append(custom_mod3_path)
sys.path.append(custom_mod4_path)

# Perform whole or partial module importations #
#----------------------------------------------#

import array_handler
import data_frame_handler
import datetime_operators
import program_snippet_exec_timers
import string_handler

#----------------------------------------------------#
# Define imported module(s)' function call shortcuts #
#----------------------------------------------------#

list_array_to_std_array = array_handler.arrayOfList_to_array
select_list_elements = array_handler.select_list_elements
sort_array_rows_by_column = array_handler.sort_array_rows_by_column

csv2df = data_frame_handler.csv2df
excel2df_base = data_frame_handler.excel2df_base
excel2dict = data_frame_handler.excel2dict
find_date_key = data_frame_handler.find_date_key
insert_column_in_df = data_frame_handler.insert_column_in_df
merge_excel_files = data_frame_handler.merge_excel_files
save2excel = data_frame_handler.save2excel

get_obj_operation_datetime = datetime_operators.get_obj_operation_datetime
time_format_tweaker = datetime_operators.time_format_tweaker

program_exec_timer = program_snippet_exec_timers.program_exec_timer

find_substring_index = string_handler.find_substring_index

#------------------#
# Define functions #
#------------------#

def df_to_structured_array(df):
    records = df.to_records(index=False)
    data = np.array(records, dtype=records.dtype.descr)
    return data
   
def customize_excel_file_merger(results_dir, merged_file_name, excel_files):
    merged_file_path = f"{results_dir}/{merged_file_name}"
    modTimes = get_obj_operation_datetime(excel_files,
                                          attr="modification", 
                                          time_fmt_str=standard_dt_str)
    
    excel_files = sort_array_rows_by_column(modTimes, -1)[:,0]
    
    merge_excel_files(excel_files,
                      merged_file_path,
                      save_index=False,
                      save_header=False,
                      save_merged_file=True)
     
     
def df_summarizer(df, df_cols, operator):
    data_count = eval(f"df.groupby(df_cols).{operator}()")
    return data_count    


def complete_data_reach_threshold(WS_arr,
                                  WS_binned_df, WS_arr_binned,
                                  WS_arr_sum, WS_sum_cols,
                                  key_var_idx_list, key_var_list,
                                  WS_sum_df=None):
        
    # Main information from the passed arguments #
    #--------------------------------------------#

    las = len(WS_arr_sum)

    # Array for the selected cases (s), based on the key variable list #
    ####################################################################
    
    lkvil = len(key_var_idx_list)
    
    # Depending on the length of the list, consider the variable case data frame #   
    if lkvil == 0:
        arr_varcase_idx = range(las)
         
    elif lkvil == 1:   
        arr_varcase_idx = np.where(WS_arr_sum[:, 1]==key_var_idx_list)
        
    elif lkvil == 2:
        arr_varcase_idx = np.where((WS_arr_sum[:, 1]==key_var_idx_list[0])
                                    * (WS_arr_sum[:, 2]==key_var_idx_list[1]))
        
    elif lkvil == 3:            
        arr_varcase_idx = WS_sum_df[(WS_sum_df[WS_sum_cols[1]]==key_var_idx_list[0])
                                    & (WS_sum_df[WS_sum_cols[2]]==key_var_idx_list[1])
                                    & (WS_sum_df[WS_sum_cols[3]]==key_var_idx_list[2])].index
        
    arr_varcase = WS_arr_sum[arr_varcase_idx]
    arr_varcase_ref = arr_varcase.copy()
    
    lav = len(arr_varcase)

    #----------------------------------------------------#
    # Complete the data frame for each bin, if necessary #
    #----------------------------------------------------#
    
    if lav == 0:
        pass
    
    else:        
        
        for i in range(lav):
            
            # Concatenable slice of the current bin #
            list_slice = [arr_varcase_ref[i].tolist()]

            # Corresponding bin, average sigma, N-values and completed condition #
            key_var_idx = find_substring_index(WS_sum_cols, key_var_list)

            curr_bin, sigma_avg, N = select_list_elements(list_slice[0], key_var_idx)
            
            if N < valid_data_threshold:               
                
                """Scan progressively the original data frame such that
                the sum of the N-values is equal or greater than the threshold.
                
                If the valid data amount is below the threshold, by default
                the PREVIOUS bin's corresponding data frame slice will be evaluated,
                and if the condition is still not satisfied, the next bin,
                besides that previous one. These two movements constitute a cycle.
                """
                
                # Initiate the number of cycles #
                M = 0
                
                while (N < valid_data_threshold):
               
                    M += 1
                    MF = i + M
                    MB = i - M
                    
                    if MB < 0:
                        pass
                        
                    else:
                        # Concatenable slice of the previous bin with its information #
                        list2append = arr_varcase_ref[MB].tolist()
                        list_slice.append(list2append)
                        
                        prev_bin, sigma_avg_prev, N_prev\
                        = select_list_elements(list2append, key_var_idx)
        
                        # Sum up every valid data amount on the 'df2concat' frame #
                        N = np.sum(np.array(list_slice)[:,-1])
                    
                    if N < valid_data_threshold:
                        if M < lav:                        
                            if MF > lav -1:
                                pass
                            else:
                                # Concatenable slice of the next bin with its information #
                                list2append = arr_varcase_ref[MF].tolist()
                                list_slice.append(list2append)
                                
                                next_bin, sigma_avg_next, N_next\
                                = select_list_elements(list2append, key_var_idx)
                
                                # Sum up every valid data amount on the 'df2concat' frame #
                                N = np.sum(np.array(list_slice)[:,-1])
                                
                        else:
                            break
                            
                    else:
                        break
                    
                else:
    
                    """
                    Consider the necessary data to complete the missing 
                    data set of the current bin.
                    """
                    lls = len(list_slice)
                    keyDataList = []
                    
                    NT = 0
                    
                    for j in range(lls):
                        
                        """
                        From now on, 0th index will always be 
                        the binned wind speed column.
                        """
                        
                        WS_bin, N = select_list_elements(list_slice[j], [0,-1])
                        NT += N        
                      
                        """
                        Pandas's indexing method has been chosen over np.where
                        because it causes increasing performance loss over WS bin iterations.
                        """
                        
                        if lkvil == 0:
                            sigma_idx\
                            = WS_binned_df[WS_binned_df[WS_sum_cols[0]]==WS_bin].index
                       
                        elif lkvil == 1:
                            sigma_idx\
                            = WS_binned_df[(WS_binned_df[WS_sum_cols[0]]==WS_bin)
                                            & (WS_binned_df[WS_sum_cols[1]]==key_var_idx_list[0])].index
                        
                        elif lkvil == 2:
                            sigma_idx\
                            = WS_binned_df[(WS_binned_df[WS_sum_cols[0]]==WS_bin)
                                            & (WS_binned_df[WS_sum_cols[1]]==key_var_idx_list[0])
                                            & (WS_binned_df[WS_sum_cols[2]]==key_var_idx_list[1])].index
                            
                        elif lkvil == 3:
                            sigma_idx\
                            = WS_binned_df[(WS_binned_df[WS_sum_cols[0]]==WS_bin)
                                            & (WS_binned_df[WS_sum_cols[1]]==key_var_idx_list[0])
                                            & (WS_binned_df[WS_sum_cols[2]]==key_var_idx_list[1])
                                            & (WS_binned_df[WS_sum_cols[3]]==key_var_idx_list[2])].index
    
    
                        arr_binned_WS_sigma_idx = WS_arr_binned[sigma_idx]
                        arr_WS_sigma_idx = WS_arr[sigma_idx][:, np.newaxis]
                        
                        arr_WS_sigma_idx = np.append(arr_WS_sigma_idx, 
                                                     arr_binned_WS_sigma_idx, 
                                                     axis=1)
                                            
                        """The last column will always be filled-in sigma"""
                        sigma_bin = arr_WS_sigma_idx[:,-1]
    
                        if NT < valid_data_threshold:
                            keyDataList.append((sigma_bin, N))
                            
                        else:                
                            N1 = valid_data_threshold + N - NT
                            
                            curr_bin_left = curr_bin.left
                            Bin_left = WS_bin.left
                            d_bin = Bin_left - curr_bin_left
                         
                            if d_bin < 0:
                                """Take the N1 values closest to the right boundary
                                of the considered bin.
                                """
                                
                                sigma_bin_toComplMinN\
                                = sort_array_rows_by_column(arr_WS_sigma_idx, 0)[-N1:,-1]
                                
                                
                            elif d_bin > 0:
                                """Take the N1 values closest to the left boundary
                                of the considered bin.
                                """
                                sigma_bin_toComplMinN\
                                = sort_array_rows_by_column(arr_WS_sigma_idx, 0)[:N1,-1]
    
                                
                            keyDataList.append((sigma_bin_toComplMinN, N1))
                       
                    # Calculate the weighted mean of each sigma's subset array #
                    sigma_means = [nanmean
                                   for tupl in keyDataList
                                   if not np.isnan(nanmean:=np.nanmean(tupl[0]))]
                    
                    weights = [w
                               for tupl in keyDataList
                               if (w:=tupl[1])>0]
                    
                    lsm = len(sigma_means)
                    lw = len(weights)
                    
                    """
                    In some cases, due to the already used intervals and
                    insufficient or non-existent data in the original series (WS_series)
                    the sliced list (list_slice) will be empty.
                      
                    In these cases, the mean of the sigma will be set to NaN
                    and further treatmen will be required to handle them
                    once the matrix is filled-in.
                    """
                    
                    if lsm == 0 and lw == 0:
                        weighted_sigma_mean = fixedInvalidSigmaValue
                    else:
                        weighted_sigma_mean = np.average(sigma_means, weights=weights)
                        
                    
                    # If the current bin has been completed up to the minimum 
                    # available data, set the new 'N' equal to the theshold.
                    
                    if NT >= valid_data_threshold:                    
                        arr_varcase[i, key_var_idx] \
                        = curr_bin, weighted_sigma_mean, valid_data_threshold
                    
                    # If it is not the case, then set the new 'N' 
                    # equal to the extent that the sum has been updated.
                    else:
                        arr_varcase[i, key_var_idx] \
                        = curr_bin, weighted_sigma_mean, NT
                    
            else:
                pass
            
    return arr_varcase


def assign_sigma_to_original_data(original_array,
                                  WS_binned_df,
                                  sigmaFilledDf,
                                  sigmaFilledArray,
                                  WS_bins_arr,
                                  key_var_idx_list):
    
    sigmaToFillDfCols = list(sigmaFilledDf.columns)
    
    lkvil = len(key_var_idx_list)
    lwsba = len(WS_bins_arr)
    
    # Array for the selected cases (s), based on the key variable list and WS bin #
    ###############################################################################

    for i in range(lwsba):
        
        WS_bin = WS_bins_arr[i]
            
        # Depending on the length of the list, consider the variable case data frame #  
        if lkvil == 0:        
            df_varcase_idx\
            = WS_binned_df[WS_binned_df[sigmaToFillDfCols[0]]==WS_bin].index
            sigma_mean_bin_idx\
            = sigmaFilledDf[sigmaFilledDf[sigmaToFillDfCols[0]]==WS_bin].index
             
        elif lkvil == 1:   
            df_varcase_idx\
            = WS_binned_df[(WS_binned_df[sigmaToFillDfCols[0]]==WS_bin)
                           & (WS_binned_df[sigmaToFillDfCols[1]]==key_var_idx_list[0])].index
            
            sigma_mean_bin_idx\
            = sigmaFilledDf[(sigmaFilledDf[sigmaToFillDfCols[0]]==WS_bin)
                                  & (sigmaFilledDf[sigmaToFillDfCols[1]]==key_var_idx_list[0])].index          
            
        elif lkvil == 2:
            df_varcase_idx\
            = WS_binned_df[(WS_binned_df[sigmaToFillDfCols[0]]==WS_bin)
                           & (WS_binned_df[sigmaToFillDfCols[1]]==key_var_idx_list[0])
                           & (WS_binned_df[sigmaToFillDfCols[2]]==key_var_idx_list[1])].index
            
            sigma_mean_bin_idx\
            = sigmaFilledDf[(sigmaFilledDf[sigmaToFillDfCols[0]]==WS_bin)
                            & (sigmaFilledDf[sigmaToFillDfCols[1]]==key_var_idx_list[0])
                            & (sigmaFilledDf[sigmaToFillDfCols[2]]==key_var_idx_list[1])].index    
            
        elif lkvil == 3:    
            df_varcase_idx\
            = WS_binned_df[(WS_binned_df[sigmaToFillDfCols[0]]==WS_bin)
                           & (WS_binned_df[sigmaToFillDfCols[1]]==key_var_idx_list[0])
                           & (WS_binned_df[sigmaToFillDfCols[2]]==key_var_idx_list[1])
                           & (WS_binned_df[sigmaToFillDfCols[3]]==key_var_idx_list[2])].index
            
            sigma_mean_bin_idx\
            = sigmaFilledDf[(sigmaFilledDf[sigmaToFillDfCols[0]]==WS_bin)
                            & (sigmaFilledDf[sigmaToFillDfCols[1]]==key_var_idx_list[0])
                            & (sigmaFilledDf[sigmaToFillDfCols[2]]==key_var_idx_list[1])
                            & (sigmaFilledDf[sigmaToFillDfCols[3]]==key_var_idx_list[2])].index  
            
        ldfvi = len(df_varcase_idx)
        lsmbi = len(sigma_mean_bin_idx)
        
        if ldfvi > 0 and lsmbi > 0:            
            sigma_mean_bin = sigmaFilledArray[sigma_mean_bin_idx, -2]
            original_array[df_varcase_idx, -1] = sigma_mean_bin
        else:
            pass
        
    return original_array
    

#%%

#---------------------#
# Start the stopwatch #
#---------------------#

program_exec_timer("start")

#------------#
# Parameters #
#------------#

# User-defined #
#--------------#

# Paths #
main_path = "C:/Users/jgabantxo_ext/OneDrive - ACCIONA S.A/Documents/"\
            "01-RDT_ingenieros/bezeroak/Acciona/PROIEKTUAK/HEGO_AFRIKA/WOLSELEY"

results_dir = Path(f"{main_path}/results/IT_calculation")
Path.mkdir(results_dir, parents=True, exist_ok=True)

# Paths #
input_data_dir = f"{main_path}/input_data"

# Extensions #
extensions = ["csv", "xlsx"]

# Files #
wind_10min_file = f"{input_data_dir}/Wolseley_80m_2013-2015_sensor1.{extensions[0]}" 
wind_1h_fixed_file = wind_10min_file

# Sigma and IT-related thresholds and flags #
valid_data_threshold = 50
invalidSigmaValue = 9999

sigmaNanToNum = True
ITnanToNum = True

# Wind direction settings #
direc_nsectors = 12
direc_bin_width = 360 / direc_nsectors

sectorBalancementAroundZero = True

# Main result printing controls #s
print_sigmaFilled_df = False
print_IT_df = False

# Excel file saving parameters #
#------------------------------#

# Key file names #
sigmaFilledFS = "WS_byBins_sigma_10min_filled"
ITFileFS = "IT_10min"

# Individual file saving #
saveSigmaFilledAsFile = False
saveITDataAsFile = False

# Excel file merging #
mergeAllSigmaFilledFiles = True
mergeAllITFiles = True

# Case selection switches #
considerDirection = True
considerMonth = True
considerHour = True

# Pandas' data frame column names #
###################################

# Key variables #
WS_col = "Sensor 1-Velocidad media"
WS_sigma_col = "Sensor 1-Velocidad desviacion"
direc_col = "Sensor 1-Direccion media"

# Fixed #
#-------#

# Invalid sigma value #
fixedInvalidSigmaValue = np.nan

# Date and time format strings #
original_dt_str1 = "%d/%m/%Y %H:%M:%S"
original_dt_str2 = "%d/%m/%Y %H:%M"

standard_dt_str = '%Y-%m-%d %H:%M'

# Time ranges #
hour_range = range(24)
month_range = range(1,13)

lhours = len(hour_range)
lmonths = len(month_range)

# CSV file reading parameters #
sepchar = ";"
decimal_char = ","
parse_dates = True

# Excel file saving parameters #
save_index = False
save_header = True

# Case selection controls #
anyCaseSelected = bool(np.mean([eval(case)
                                for case in vars()
                                if case.startswith("consider")]))

allCasesSelected = np.all([eval(case)
                           for case in vars()
                           if case.startswith("consider")])

# Fixed pandas' data frame column names #
#########################################

# Time-related #
hour_col = "hour"
month_col = "month" 

# Key variables #
WS_col_abbr = "v(m/s)"
WS_byBins_col = "bins_velocidad_corregida_(m/s)"

WS_mean_sigma_col = "sigma_mean"
WS_sigma_corrected_col = "sigma_corregido"

direc_col_abbr = "dir(degrees)"
direc_bins_col = "bins_direccion_media_(grados)"

IT_col = "IT"

# Main and key variable list #
key_var_list = [WS_col_abbr, WS_mean_sigma_col, "N"]

# Preformatted strings #
#----------------------#

caseSelectionInfoStr = \
"""Following cases selected:
   {}
   
   Completing data...
"""

sigmaFIllRemainCasesInfoStr = \
"""Remaining cases to be treated to fill sigma values:
   Hour = {}
   Month = {}
   Direction = {}
"""

sigmaAssignRemainCasesInfoStr = \
"""Remaining cases to be treated to assign filled sigmas:
   Hour = {}
   Month = {}
   Direction = {}
"""

fixed_df_InfoStr = """
COMPLETED WS-BINNED DATA FRAME
------------------------------
{}
"""

# Mute the following warnings (irrelevant ones, already understood) #
#-------------------------------------------------------------------#
"""The origin of these errors does not in any case alter neither the results
nor the program execution.
"""
warnings.simplefilter(action='ignore', category=DeprecationWarning)
warnings.simplefilter(action='ignore', category=RuntimeWarning)

#%%

#------------------------#
# Read the CSV documents #
#------------------------#

# 10 min freq #
#-------------#

if not mergeAllSigmaFilledFiles or not mergeAllITFiles:

    print("Opening and accomodating 10-minutely data...")
    
    df_10min = csv2df(wind_10min_file, 
                      separator=sepchar, 
                      decimal=decimal_char,
                      parse_dates=parse_dates)
    
    """Convert column 4 data to date and time"""
    time_col = find_date_key(df_10min)
    df_10min_time = df_10min[time_col]
    df_10min_time_std = pd.to_datetime(df_10min_time, format=original_dt_str2)
    
    df_10min[time_col] = df_10min_time_std
    
    """Add the corrected wind speed's sigma column"""
    df_10min[WS_sigma_corrected_col] = np.nan
    
    """Get its values to use them later"""
    arr_10min = df_10min.values
    
    # 1 hour freq #
    #-------------#
    
    print("Opening and accomodating hourly data...")
    
    df_1h = csv2df(wind_1h_fixed_file,
                   separator=sepchar, 
                   decimal=decimal_char,
                   parse_dates=parse_dates)
                              
    
    """Convert column 4 data to date and time"""
    cols_1h_fixed = df_1h.columns
    df_1h_time = df_1h[time_col]
    df_1h_time_std = pd.to_datetime(df_1h_time, format=original_dt_str2)
    
    df_1h[time_col] = df_1h_time_std
    
    #------------------------------------#
    # Cut variable data frames into bins #
    #------------------------------------#
    
    # Mean wind speed #
    #-----------------#
    
    WS_10min_series = df_10min.loc[:, WS_col]
    WS_10min_arr = WS_10min_series.values
    
    max_WS_10min = np.max(df_10min[WS_col])
    max_WS_1h = np.max(df_1h[WS_col])
    
    max_WS = np.max([max_WS_10min, max_WS_1h])
    
    """The problem with the definition pair below is that numbers with small decimals
    fall into the previous bin.
    
    E.g. bar{v}=4.04 --> bin=(3,4] which is incorrect
    """
    
    # WS_numBins = int(round(max_WS,0))
    # WS_bins = pd.cut(WS_10min_series,WS_numBins)
    
    """ Instead, define a list of upper and lower limits,
    being the number either integer or float
    """
    WS_numBins = int(round(max_WS, 0))
    bin_width1 = 0.5
    bin_width2 = 1
    
    WS_bins = np.append(np.arange(1,step=bin_width1),
                        np.arange(1.5, WS_numBins+bin_width2, step=bin_width2))
    
    # Group (or cut) the values into the corresponding bin and get the indexes #
    """For the bins to be closed to the left and open to the right,
    set the 'right' option in pd.cut to False
    """
    WS_byBins_df = pd.DataFrame(pd.cut(WS_10min_series, WS_bins, right=False))
    
    # Get mean speed data frame indexes for each bin thereof #
    WS_byBins_df.columns = [WS_byBins_col]
    WS_byBins_unique = np.unique(WS_byBins_df.dropna())
    
    WS_byWS10Bins_idx\
    = [WS_10min_series[WS_10min_series.between(interval.left, interval.right)].index
       for interval in WS_byBins_unique]
    
    
    # Direction #
    #-----------#
    
    if considerDirection:
            
        # Get the mean wind speed column's position #
        direc_10min_series = df_10min[direc_col]
    
        if sectorBalancementAroundZero:
            
            """The first sector of the wind rose is centered around 0º,
            and the entire rose is circled counterclockwise.
            """
            
            direc_bins = np.arange(0-direc_bin_width/2, 360+direc_bin_width/2,
                                   step=direc_bin_width)
            
            """But then if an angle is greater or equal than 360 - direc_bin_width/2, 
            it would not be caught by pd.cut, so these angles must be subtracted by 360º.
            """
            direc_10min_fixed = np.where(direc_10min_series>=360-direc_bin_width/2,
                                         direc_10min_series-360,
                                         direc_10min_series)
            
            direc_10min_series = pd.Series(direc_10min_fixed, name=direc_col)
            
        else:
            """The case would become simpler, as the rose is continuous"""
            direc_bins = np.arange(0, 360, step=direc_bin_width)
            
            """However, again, if an angle is greater or equal than 360
            it would not be caught by pd.cut, so these angles must be 
            subtracted by 360º.
            """
            direc_10min = np.where(direc_10min_series>=360,
                                   direc_10min_series-360,
                                   direc_10min_series)
            
            direc_10min_series = pd.Series(direc_10min, name=direc_col)
        
        direc_byBins = pd.cut(direc_10min_series, direc_bins, right=False)
        direc_byBins_df = pd.DataFrame(direc_byBins, columns=[direc_col])
        
        # Get mean direction data frame indexes for each bin thereof #
        direc_byBins_df.columns = [direc_bins_col]
        
        direc_byBins_unique = np.unique(direc_byBins_df.dropna())
        l_direcBin = len(direc_byBins_unique)
        
        direc_byBins_byWS10Bins_idx\
        = [direc_10min_series[direc_10min_series.between(interval.left, interval.right)].index
           for interval in direc_byBins_unique
           if not isinstance(interval, float)]
    
    
    # Time by months #
    #----------------#
    
    if considerMonth:
        time_byMonth_idx = [df_10min[df_10min[time_col].dt.month==mon].index
                            for mon in range(1,13)]
    
    # Time by hours #
    #---------------#
    
    if considerHour:
        time_byHour_idx = [df_10min[df_10min[time_col].dt.hour==hour].index
                           for hour in range(24)]
    
    #---------------------------------------------------------------------------------#
    # Get the 10-minutely WS sigma mean according to the indexes of the binned series #
    #---------------------------------------------------------------------------------#
    
    WS_sigma_df = df_10min[WS_sigma_col]
    
    # Mean wind speed bins #
    #----------------------#
    
    WS_sigma_10min_byWSBinIdx = [WS_sigma_df.loc[row_idx_list]
                                 for row_idx_list in WS_byWS10Bins_idx]
    
    WS_sigma_10min_byWSBinIdx_avg = [df_slice.mean()
                                     for df_slice in WS_sigma_10min_byWSBinIdx]
    
    # Direction bins #
    #----------------#
    
    if considerDirection:
        WS_sigma_10min_byDirecBinIdx = [WS_sigma_df.loc[row_idx_list]
                                        for row_idx_list in direc_byBins_byWS10Bins_idx]
        
        WS_sigma_10min_byDirecBinIdx_avg = [df_slice.mean()
                                            for df_slice in WS_sigma_10min_byDirecBinIdx]
    
    # Month bins #
    #------------#
    
    if considerMonth:
        WS_sigma_10min_byMonthBinIdx = [WS_sigma_df.loc[row_idx_list]
                                        for row_idx_list in time_byMonth_idx]
        
        WS_sigma_10min_byMonth_avg = [df_slice.mean()
                                      for df_slice in WS_sigma_10min_byMonthBinIdx]
        
    # IT by hour #
    #------------#
    
    if considerHour:
        WS_sigma_10min_byHourBinIdx = [WS_sigma_df.loc[row_idx_list]
                                       for row_idx_list in time_byHour_idx]
        
        WS_sigma_10min_byHour_avg = [df_slice.mean()
                                     for df_slice in WS_sigma_10min_byHourBinIdx]
    
    
    #---------------------------------------------------------------------------------#
    # Construct the mean WS sigma data frame according to the selected parameter bins #
    #---------------------------------------------------------------------------------#
    
    # Mean wind speed #
    #-----------------#
    
    # Put data together #
    WS_byBins_sigma_df = pd.concat([WS_byBins_df, WS_sigma_df], axis=1)
    WS_byBins_Sigma_df_cols = [WS_col_abbr, WS_sigma_col]
    WS_byBins_sigma_df.columns = WS_byBins_Sigma_df_cols
    
    # Direction #
    #-----------#
    
    if considerDirection:
    
        # Construct only key column labelled data frame #
        i = len(WS_byBins_sigma_df.columns)-1    
        insert_column_in_df(WS_byBins_sigma_df, i, direc_col_abbr, direc_byBins_df)    
        
        WS_byBins_Sigma_df_cols.insert(i, direc_col_abbr)  
        
    # Month #
    #-------#
        
    if considerMonth:
        
        # Key column and its corresponding data #
        month_df = df_10min[time_col].dt.month
        
        # Construct only key column labelled data frame #
        i = len(WS_byBins_sigma_df.columns)-1
        insert_column_in_df(WS_byBins_sigma_df, i, month_col, month_df)
        
        WS_byBins_Sigma_df_cols.insert(i, month_col)
    
    # Hour #
    #------#
    
    if considerHour:
        
        # Key column and its corresponding data #
        hour_df = df_10min[time_col].dt.hour
        
        # Construct only key column labelled data frame #
        i = len(WS_byBins_sigma_df.columns)-1
        insert_column_in_df(WS_byBins_sigma_df, i, hour_col, hour_df)      
        
        WS_byBins_Sigma_df_cols.insert(i, hour_col) 
        
    # Define now an array of the binned data frame for later usage #
    #--------------------------------------------------------------#
    
    WS_byBins_sigma_arr = WS_byBins_sigma_df.values
      
    # Summarize the data #  
    #--------------------#
    
    WS_byBins_sigma_df.columns = WS_byBins_Sigma_df_cols
    
    # Count the number of available data for each parameter bin (N) and compute its mean #
    df_validDataMean =  df_summarizer(WS_byBins_sigma_df,
                                      WS_byBins_Sigma_df_cols[:-1],
                                      "mean")
    
    df_intervalNumValidData = df_summarizer(WS_byBins_sigma_df,
                                            WS_byBins_Sigma_df_cols[:-1],
                                            "count")
    
    sigmaToFill_MI_df = pd.concat([df_validDataMean, 
                                   df_intervalNumValidData],
                                  axis=1)
    
    sigmaToFill_MI_df.columns = [WS_mean_sigma_col, "N"]
    
    #-----------------------------------------------------------------#
    # Complete the WS-binned sigma data frame for each variable combo #
    #-----------------------------------------------------------------#
    
    # Define data frames easier to handle and understand #
    #----------------------------------------------------#
    
    # Reset the indexes of the summarized data frame for easier handling #
    sigmaToFilldf = sigmaToFill_MI_df.reset_index()
    
    """Indexing pandas's intervals slows the execution down,
    unless the data type is pd.CategoricalIndex, which is the case
    of the wind speed bins. These are automatically generated with pd.cut attr.
    
    Regarding direction, the data type is pd.Interval, which makes indexing 
    much slower. Converting them also to pd.CategoricalIndex increases performance.
    """
    
    if considerDirection:
        sigmaToFilldf.loc[:, direc_col_abbr]\
        = pd.CategoricalIndex(sigmaToFilldf.loc[:, direc_col_abbr],
                              ordered=True, 
                              categories=direc_byBins_unique)
        
        WS_byBins_sigma_df.loc[:, direc_col_abbr]\
        = pd.CategoricalIndex(WS_byBins_sigma_df.loc[:, direc_col_abbr],
                              ordered=True, 
                              categories=direc_byBins_unique)
    
    sigmaToFillArr = sigmaToFilldf.values
    sigmaToFillDfCols = list(sigmaToFilldf)
    
    # Final list to store fixed data #
    #--------------------------------#
    
    sigmaFilledList = []
    
    print("Completing data...")
    
    # sys.exit(0)
    
    #%%
    
    # =============================================================================
    # HIGH-COMPLEXITY CASE: WS BIN + DIRECTION BIN + MONTH + HOUR
    # =============================================================================
    
    if allCasesSelected:
        
        caseSelectionList = ["Wind speed (default)", "Direction", "Month", "Hour"]
        tab_name = "WS + DIREC + MONTH + HOUR"
        
        for i_direcBin, direcBin in enumerate(direc_byBins_unique):
            for m in month_range:
                for h in hour_range:
                    
                    key_var_idx_list1 = [direcBin, m, h]
                    sigmaFilledArrVar = complete_data_reach_threshold(WS_10min_arr,
                                                                      WS_byBins_sigma_df,
                                                                      WS_byBins_sigma_arr,
                                                                      sigmaToFillArr,
                                                                      sigmaToFillDfCols,
                                                                      key_var_idx_list1,
                                                                      key_var_list,
                                                                      WS_sum_df=sigmaToFilldf)
                    
                    sigmaFilledList.append(sigmaFilledArrVar)
                    
                    print(sigmaFIllRemainCasesInfoStr.format(lhours-h,
                                                             lmonths-(m-1),
                                                             l_direcBin-i_direcBin))                
    
    #%%
    
    # =============================================================================
    # MEDIUM-COMPLEXITY CASE: WS BIN + MONTH + HOUR
    # =============================================================================
    
    if considerMonth and considerHour and not considerDirection:
        
        caseSelectionList = ["Wind speed (default)", "Month", "Hour"]
        tab_name = "WS + MONTH + HOUR"
    
        for m in month_range:
            for h in hour_range:
    
                key_var_idx_list1 = [m, h]
                sigmaFilledArrVar = complete_data_reach_threshold(WS_10min_arr,
                                                                  WS_byBins_sigma_df,
                                                                  WS_byBins_sigma_arr,
                                                                  sigmaToFillArr,
                                                                  sigmaToFillDfCols,
                                                                  key_var_idx_list1,
                                                                  key_var_list)
                
                sigmaFilledList.append(sigmaFilledArrVar)
                
                print(sigmaFIllRemainCasesInfoStr.format(lhours-h,
                                                         lmonths-(m-1),
                                                         "(not selected)"))
    
    #%%
    
    # =============================================================================
    # MEDIUM-COMPLEXITY CASE: WS BIN + DIRECTION BIN + HOUR
    # =============================================================================
    
    if considerDirection and considerHour and not considerMonth:
        
        caseSelectionList = ["Wind speed (default)", "Direction", "Hour"]
        tab_name = "WS + DIREC + HOUR"
    
        for direc in enumerate(direc_byBins_unique):
            direcBin = direc[-1]
            i_direcBin = direc[0]
            
            for h in hour_range:            
            
                key_var_idx_list1 = [direcBin, h]
                sigmaFilledArrVar = complete_data_reach_threshold(WS_10min_arr,
                                                                  WS_byBins_sigma_df,
                                                                  WS_byBins_sigma_arr,
                                                                  sigmaToFillArr,
                                                                  sigmaToFillDfCols,
                                                                  key_var_idx_list1,
                                                                  key_var_list)
                                                               
                sigmaFilledList.append(sigmaFilledArrVar)
                
                print(sigmaFIllRemainCasesInfoStr.format(lhours-h,
                                                         "(not selected)",
                                                         l_direcBin-i_direcBin))
     
    
    #%%
    
    # =============================================================================
    # MEDIUM-COMPLEXITY CASE: WS BIN + DIRECTION BIN + MONTH
    # =============================================================================
    
    if considerDirection and considerMonth and not considerHour:
        
        caseSelectionList = ["Wind speed (default)", "Direction", "Month"]
        tab_name = "WS + DIREC + MONTH"
    
        for direc in enumerate(direc_byBins_unique):
            direcBin = direc[-1]
            i_direcBin = direc[0]
       
            for m in month_range:
                  
                key_var_idx_list1 = [direcBin, m]
                sigmaFilledArrVar = complete_data_reach_threshold(WS_10min_arr,
                                                                  WS_byBins_sigma_df,
                                                                  WS_byBins_sigma_arr,
                                                                  sigmaToFillArr,
                                                                  sigmaToFillDfCols,
                                                                  key_var_idx_list1,
                                                                  key_var_list)
                
                sigmaFilledList.append(sigmaFilledArrVar)
                
                print(sigmaFIllRemainCasesInfoStr.format("(not selected)",
                                                         lmonths-(m-1),
                                                         l_direcBin-i_direcBin))
    
    #%%
    
    # =============================================================================
    # LOW-COMPLEXITY CASE: WS BIN + DIRECTION BIN
    # =============================================================================
    
    if considerDirection and not considerMonth and not considerHour:
        
        caseSelectionList = ["Wind speed (default)", "Direction"]
        tab_name = "WS + DIREC"
    
        for direc in enumerate(direc_byBins_unique):
            direcBin = direc[-1]
            i_direcBin = direc[0]
            
            key_var_idx_list1 = [direcBin]
            sigmaFilledArrVar = complete_data_reach_threshold(WS_10min_arr,
                                                              WS_byBins_sigma_df,
                                                              WS_byBins_sigma_arr,
                                                              sigmaToFillArr,
                                                              sigmaToFillDfCols,
                                                              key_var_idx_list1,
                                                              key_var_list)
            
            sigmaFilledList.append(sigmaFilledArrVar)
            
            print(sigmaFIllRemainCasesInfoStr.format("(not selected)",
                                                     "(not selected)",
                                                     l_direcBin-i_direcBin))
            
    #%%
    
    # =============================================================================
    # LOW-COMPLEXITY CASE: WS BIN + MONTH
    # =============================================================================
    
    if considerMonth and not considerDirection and not considerHour:
        
        caseSelectionList = ["Wind speed (default)", "Month"]
        tab_name = "WS + MONTH"
    
        for m in month_range:
            
            key_var_idx_list1 = [m]
            sigmaFilledArrVar = complete_data_reach_threshold(WS_10min_arr,
                                                              WS_byBins_sigma_df,
                                                              WS_byBins_sigma_arr,
                                                              sigmaToFillArr,
                                                              sigmaToFillDfCols,
                                                              key_var_idx_list1,
                                                              key_var_list)
    
            sigmaFilledList.append(sigmaFilledArrVar)
            
            print(sigmaFIllRemainCasesInfoStr.format("(not selected)",
                                                     lmonths-(m-1),
                                                     "(not selected)"))
            
       
    #%%
    
    # =============================================================================
    # LOW-COMPLEXITY CASE: WS BIN + HOUR
    # =============================================================================
    
    if considerHour and not considerDirection and not considerMonth:
        
        caseSelectionList = ["Wind speed (default)", "Hour"]
        tab_name = "WS + HOUR"
    
        for h in hour_range:      
            key_var_idx_list1 = [h]
    
            sigmaFilledArrVar = complete_data_reach_threshold(WS_10min_arr,
                                                              WS_byBins_sigma_df,
                                                              WS_byBins_sigma_arr,
                                                              sigmaToFillArr,
                                                              sigmaToFillDfCols,
                                                              key_var_idx_list1,
                                                              key_var_list)
         
            sigmaFilledList.append(sigmaFilledArrVar)
            
            print(sigmaFIllRemainCasesInfoStr.format(lhours-h,
                                                     "(not selected)",
                                                     "(not selected)"))
            
    #%%
    
    # =============================================================================
    # SIMPLEST CASE: WS BIN
    # =============================================================================
    
    if not anyCaseSelected:
        tab_name = "WS"
    
        key_var_idx_list1 = []
        sigmaFilledArrVar = complete_data_reach_threshold(WS_10min_arr,
                                                          WS_byBins_sigma_df,
                                                          WS_byBins_sigma_arr,
                                                          sigmaToFillArr,
                                                          sigmaToFillDfCols,
                                                          key_var_idx_list1,
                                                          key_var_list)
        
        sigmaFilledList.append(sigmaFilledArrVar)
    
        
    #%%
    
    #------------------------------------------------------------------------------------#
    # Fill the original data's sigma with the mean one according to the considered cases #
    #------------------------------------------------------------------------------------#
    
    sigmaFilledArr = list_array_to_std_array(sigmaFilledList)
    sigmaFilledDf = pd.DataFrame(sigmaFilledArr, columns=sigmaToFillDfCols)
    
    #%%
    
    # =============================================================================
    # HIGH-COMPLEXITY CASE: WS BIN + DIRECTION BIN + MONTH + HOUR
    # =============================================================================
    
    if allCasesSelected:
        
        caseSelectionList = ["Wind speed (default)", "Direction", "Month", "Hour"]
        tab_name = "WS + DIREC + MONTH + HOUR"
        
        for direc in enumerate(direc_byBins_unique):
            direcBin = direc[-1]
            i_direcBin = direc[0]
       
            for m in month_range:
                for h in hour_range:
                    
                    key_var_idx_list2 = [direcBin, m, h]
                    arr_10min = assign_sigma_to_original_data(arr_10min,
                                                              WS_byBins_sigma_df, 
                                                              sigmaFilledDf,
                                                              sigmaFilledArr,
                                                              WS_byBins_unique,
                                                              key_var_idx_list2)
           
                    print(sigmaAssignRemainCasesInfoStr.format(lhours-h,
                                                               lmonths-(m-1),
                                                               l_direcBin-i_direcBin))
                                 
    
    #%%
    
    # =============================================================================
    # MEDIUM-COMPLEXITY CASE: WS BIN + MONTH + HOUR
    # =============================================================================
    
    if considerMonth and considerHour and not considerDirection:
        
        caseSelectionList = ["Wind speed (default)", "Month", "Hour"]
        tab_name = "WS + MONTH + HOUR"
    
        for m in month_range:
            for h in hour_range:
                key_var_idx_list2 = [m, h]
                arr_10min = assign_sigma_to_original_data(arr_10min,
                                                          WS_byBins_sigma_df, 
                                                          sigmaFilledDf,
                                                          sigmaFilledArr,
                                                          WS_byBins_unique,
                                                          key_var_idx_list2)
    
                print(sigmaAssignRemainCasesInfoStr.format(lhours-h,
                                                           lmonths-(m-1),
                                                           "(not selected)"))
    
    #%%
    
    # =============================================================================
    # MEDIUM-COMPLEXITY CASE: WS BIN + DIRECTION BIN + HOUR
    # =============================================================================
    
    if considerDirection and considerHour and not considerMonth:
        
        caseSelectionList = ["Wind speed (default)", "Direction", "Hour"]
        tab_name = "WS + DIREC + HOUR"
    
        for direc in enumerate(direc_byBins_unique):
            direcBin = direc[-1]
            i_direcBin = direc[0]
            
            for h in hour_range:            
                key_var_idx_list2 = [direcBin, h]
                arr_10min = assign_sigma_to_original_data(arr_10min,
                                                          WS_byBins_sigma_df, 
                                                          sigmaFilledDf,
                                                          sigmaFilledArr,
                                                          WS_byBins_unique,
                                                          key_var_idx_list2)
                
                print(sigmaAssignRemainCasesInfoStr.format(lhours-h,
                                                           "(not selected)",
                                                           l_direcBin-i_direcBin))
    #%%
    
    # =============================================================================
    # MEDIUM-COMPLEXITY CASE: WS BIN + DIRECTION BIN + MONTH
    # =============================================================================
    
    if considerDirection and considerMonth and not considerHour:
        
        caseSelectionList = ["Wind speed (default)", "Direction", "Month"]
        tab_name = "WS + DIREC + MONTH"
    
        for direc in enumerate(direc_byBins_unique):
            direcBin = direc[-1]
            i_direcBin = direc[0]
       
            for m in month_range:
                  
                key_var_idx_list2 = [direcBin, m]
                arr_10min = assign_sigma_to_original_data(arr_10min,
                                                          WS_byBins_sigma_df, 
                                                          sigmaFilledDf,
                                                          sigmaFilledArr,
                                                          WS_byBins_unique,
                                                          key_var_idx_list2)
              
                print(sigmaAssignRemainCasesInfoStr.format("(not selected)",
                                                           lmonths-(m-1),
                                                           l_direcBin-i_direcBin,))
                
    #%%
    
    # =============================================================================
    # LOW-COMPLEXITY CASE: WS BIN + DIRECTION BIN
    # =============================================================================
    
    if considerDirection and not considerMonth and not considerHour:
        
        caseSelectionList = ["Wind speed (default)", "Direction"]
        tab_name = "WS + DIREC"
    
        for direc in enumerate(direc_byBins_unique):
            direcBin = direc[-1]
            i_direcBin = direc[0]
            
            key_var_idx_list2 = [direcBin]
            arr_10min = assign_sigma_to_original_data(arr_10min,
                                                      WS_byBins_sigma_df, 
                                                      sigmaFilledDf,
                                                      sigmaFilledArr,
                                                      WS_byBins_unique,
                                                      key_var_idx_list2)
    
            print(sigmaAssignRemainCasesInfoStr.format("(not selected)",
                                                       "(not selected)",
                                                       l_direcBin-i_direcBin))
            
    #%%
    
    # =============================================================================
    # LOW-COMPLEXITY CASE: WS BIN + MONTH
    # =============================================================================
    
    if considerMonth and not considerDirection and not considerHour:
        
        caseSelectionList = ["Wind speed (default)", "Month"]
        tab_name = "WS + MONTH"
    
        for m in month_range:
            
            key_var_idx_list2 = [m]
            arr_10min = assign_sigma_to_original_data(arr_10min,
                                                      WS_byBins_sigma_df, 
                                                      sigmaFilledDf,
                                                      sigmaFilledArr,
                                                      WS_byBins_unique,
                                                      key_var_idx_list2)
    
            print(sigmaAssignRemainCasesInfoStr.format("(not selected)",
                                                       lmonths-(m-1),
                                                       "(not selected)"))
            
    #%%
    
    # =============================================================================
    # LOW-COMPLEXITY CASE: WS BIN + HOUR
    # =============================================================================
    
    if considerHour and not considerDirection and not considerMonth:
        
        caseSelectionList = ["Wind speed (default)", "Hour"]
        tab_name = "WS + HOUR"
    
        for h in hour_range:      
            key_var_idx_list2 = [h]        
    
            arr_10min = assign_sigma_to_original_data(arr_10min,
                                                      WS_byBins_sigma_df, 
                                                      sigmaFilledDf,
                                                      sigmaFilledArr,
                                                      WS_byBins_unique,
                                                      key_var_idx_list2)
              
            print(sigmaAssignRemainCasesInfoStr.format(lhours-h,
                                                       "(not selected)",
                                                       "(not selected)"))
            
    #%%
    
    # =============================================================================
    # SIMPLEST CASE: WS BIN
    # =============================================================================
    
    if not anyCaseSelected:
        tab_name = "WS"
    
        key_var_idx_list2 = []
        arr_10min = assign_sigma_to_original_data(arr_10min,
                                                  WS_byBins_sigma_df, 
                                                  sigmaFilledDf,
                                                  sigmaFilledArr,
                                                  WS_byBins_unique,
                                                  key_var_idx_list2)
    
    
    #%%
    
    #-------------------------#
    # Calculate the TI matrix #
    #-------------------------#
            
    df_10min_filled = pd.DataFrame(arr_10min, columns=df_10min.columns)
    
    df_10min_filled[IT_col]\
    = df_10min_filled[WS_sigma_corrected_col] / df_10min_filled[WS_col]
    
    if ITnanToNum:
        df_10MF_ITnanIdx = df_10min_filled[pd.isna(df_10min_filled[IT_col])].index
        df_10MF_SnanIdx = df_10min_filled[pd.isna(df_10min_filled[WS_sigma_corrected_col])].index
        
        df_10min_filled.loc[df_10MF_ITnanIdx, IT_col] = invalidSigmaValue
        df_10min_filled.loc[df_10MF_SnanIdx, WS_sigma_corrected_col] = invalidSigmaValue
        
    #%%

    # =============================================================================
    # SAVE THE SIGMA-FILLED BINNED DATA FRAME AS AN EXCEL FILE
    # =============================================================================
    
    if print_sigmaFilled_df:
        print(fixed_df_InfoStr.format(sigmaFilledDf))
    
    if saveSigmaFilledAsFile:
        
        if sigmaNanToNum:
            fsdf_nanIdx = sigmaFilledDf[pd.isna(sigmaFilledDf[WS_mean_sigma_col])].index 
            sigmaFilledDf.loc[fsdf_nanIdx, WS_mean_sigma_col] = invalidSigmaValue
        
        print("Saving sigma filled data frame into an Excel file...")
        tab_name_reSyntax = tab_name.replace(' + ', '_')
        
        elapsed_time_sigmaFill_col = "Elapsed time"
        elapsed_time_sigmaFill_df\
        = pd.DataFrame([program_exec_timer('stop')], columns=[elapsed_time_sigmaFill_col])
        
        elapsed_time_sigmaFill_sheetName = f"ET-Fill_{tab_name_reSyntax}"
        frame_dict_sigma = {tab_name : sigmaFilledDf,
                            f"{elapsed_time_sigmaFill_sheetName}": elapsed_time_sigmaFill_df}
        
        file_name_sigma = f"{sigmaFilledFS}-{tab_name_reSyntax}"
        file_path_sigma = f"{results_dir}/{file_name_sigma}"
        save2excel(file_path_sigma, frame_dict_sigma, save_index, save_header)
    
    #%%
    
    # =============================================================================
    # SAVE THE ORIGINAL DATA FRAME CONTAINING THE TI MATRIX (CORRECTED WS SIGMA INCLUDED)
    # =============================================================================
    
    if print_IT_df:
        print(fixed_df_InfoStr.format(df_10min_filled))
    
    if saveITDataAsFile:
    
        print("Saving IT matrix data frame into an Excel file...")
        
        tab_name_reSyntax = tab_name.replace(' + ', '_')
        
        frame_dict_IT = {tab_name : df_10min_filled}
        
        file_name_IT = f"{ITFileFS}-{tab_name_reSyntax}"
        file_path_IT = f"{results_dir}/{file_name_IT}"
        save2excel(file_path_IT, frame_dict_IT, save_index, save_header)

    #%%

    # =============================================================================
    # MERGE EVERY EXCEL FILE CONCERNING FILLED SIGMAS AND/OR IT MATRICES
    # =============================================================================
        
else:        
    if mergeAllSigmaFilledFiles:
        print("Mergeing all sigma filled Excel files into one...")
        
        merged_file_name = f"{sigmaFilledFS}_allCases"
        excel_files = glob.glob(f"{results_dir}/{sigmaFilledFS}-*.{extensions[1]}")  
        
        customize_excel_file_merger(results_dir, merged_file_name, excel_files)

    if mergeAllITFiles:
        
        print("Mergeing all IT matrix Excel files into one...")
        
        merged_file_name = f"{ITFileFS}_allCases"        
        excel_files = glob.glob(f"{results_dir}/{ITFileFS}-*.{extensions[1]}")
        
        customize_excel_file_merger(results_dir, merged_file_name, excel_files)
    
#%%

#--------------------------------------------#
# Calculate the program execution total time #
#--------------------------------------------#

print(f"Elapsed time: {program_exec_timer('stop')}")
