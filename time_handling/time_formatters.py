#----------------#
# Import modules #
#----------------#

import cftime as cft

import numpy as np
import pandas as pd

#------------------#
# Define functions #
#------------------#

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
    time_array_list_strDtype_split = time_array_list_strDtype.split("), ")
    
    cftime_check = any("cftime" in string
                       for string in time_array_list_strDtype_split)
    
    if cftime_check :
        records = len(time_array)
        time_format = "%Y-%m-%d %H:%M:%S"
        
        for i in range(records):
            time_array[i] = cft.datetime.strftime(time_array[i], time_format)
        time_array_reformatted = pd.to_datetime(time_array)
    
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
            time = dt.datetime.strptime(time, time_format_str)
            time += dt.timedelta(days=1)
            time_df.loc[i] = time

        no24hour_idx = np.delete(twentyFourHour_df.index,
                                 twentyFourHour_df_true_idx)

        time_df.loc[no24hour_idx]\
        = pd.to_datetime(time_df.loc[no24hour_idx], format = time_format_str)

    return time_df

