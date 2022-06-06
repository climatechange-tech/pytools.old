#----------------#
# Import modules #
#----------------#

import cftime as cft
import datetime

import numpy as np
import pandas as pd

#------------------#
# Define functions #
#------------------#

def check_time_index_frequency(index):
    
    # Infer the most likely frequency given the input index. If the frequency is
    # uncertain, a warning will be printed.
    # 
    # Parameters
    # ----------
    # index : DatetimeIndex or TimedeltaIndex or pd.core.series.Series
    #        If passed a Series will use the values of the series (NOT THE INDEX).
    # 
    # Returns
    # -------
    # str or None
    #     None if no discernible frequency.
    
    time_freq = pd.infer_freq(index)
    
    if time_freq is None:
        raise ValueError("Could not determine the time frequency.")
    else:
        return time_freq

def time_reformatter(time_array):
    
    # Function that gives, if necessary, the standard (Gregorian)
    # calendar format to the given array containing date times.
    # In any case, Python sees the dates as strings, so the functions
    # gives the date time format using pandas.to_datetime formatter.
    # 
    # Parameters
    # ----------
    # time_array : str, list, numpy.ndarray or xarray.core.dataarray.DataArray
    #       Object containg the date times.
    # 
    # Returns
    # -------
    # time_array_reformatted : numpy.ndarray
    #       Array containg the reformatted date times.
    #       If the type of calendar used in the original times array
    #       is different than the gregorian, it converts to that one.
    #       Otherwise it keeps the same as the original.   
    
    if isinstance(time_array, list):
        time_array_list = time_array.copy()
    
    elif isinstance(time_array, np.ndarray):
        time_array_list = list(time_array)
        
    elif isinstance(time_array, str):
        time_array_list = [time_array]
        
    else:
        time_array_list = list(time_array.values)
        
    time_array_list_strDtype = np.str_(time_array_list)    
    cftime_check = "cftime" in time_array_list_strDtype
    
    # TODO: is it possible to use the parameter below as global
    # FOR ALL FUNCTIONS INSIDE 'pytools' directory ???
    general_time_format = "%Y-%m-%d %H:%M:%S"
    
    if cftime_check:            
        time_array_reformatted\
        = pd.to_datetime([cft.datetime.strftime(time_el, general_time_format)
                          for time_el in time_array])
    
    else:
        time_array_reformatted = pd.to_datetime(time_array)
    
    return time_array_reformatted
           

def time_rearranger(time_df, time_format_str):

    # Function that checks whether some range hours
    # are 1-24. If it is the case, it converts to 0-23,
    # otherwise it returns the same data frame.
    # Time 24:00 is assumed to mean the next day,
    # so it is converted to 00:00.
    #
    # Parameters
    # ----------
    # time_df : pandas.core.series.Series
    #       Pandas series containing the date-times to be checked.
    #
    # Returns
    # -------
    # time_df : pandas.core.series.Series
    #       The necessary changes are reflected onto the same
    #       data frame as the entering one.

    twentyFourHour_df = time_df.str.contains("24")
    twentyFourHour_df_true = twentyFourHour_df[twentyFourHour_df]
    twentyFourHour_df_true_idx = twentyFourHour_df_true.index

    records_true = len(twentyFourHour_df_true)

    if records_true > 0:
        for i in twentyFourHour_df_true_idx:
            
            time = time_df.loc[i].replace("24:00","00:00")
            time = datetime.datetime.strptime(time, time_format_str)
            time += datetime.timedelta(days=1)
            time_df.loc[i] = time

        no24hour_idx = np.delete(twentyFourHour_df.index,
                                 twentyFourHour_df_true_idx)

        time_df.loc[no24hour_idx]\
        = pd.to_datetime(time_df.loc[no24hour_idx], format = time_format_str)

    return time_df

