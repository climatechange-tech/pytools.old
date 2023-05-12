#----------------#
# Import modules #
#----------------#

import cftime as cft
import datetime
import time

import inspect
from pathlib import Path
import os
import sys

import numpy as np
import pandas as pd

#-----------------------#
# Import custom modules #
#-----------------------#

# Import module that finds python tools' path #
home_PATH = Path.home()
sys.path.append(str(home_PATH))

import get_pytools_path
fixed_dirpath = get_pytools_path.return_pytools_path()

# Enumerate custom modules and their paths #
#------------------------------------------#

custom_mod1_path = f"{fixed_dirpath}/arrays_and_lists"
custom_mod2_path = f"{fixed_dirpath}/files_and_directories" 
custom_mod3_path = f"{fixed_dirpath}/parameters_and_constants"
custom_mod4_path = f"{fixed_dirpath}/pandas_data_frames" 
custom_mod5_path = f"{fixed_dirpath}/strings"
custom_mod6_path = f"{fixed_dirpath}/weather_and_climate"
                  
# Add the module paths to the path variable #
#-------------------------------------------#

sys.path.append(custom_mod1_path)
sys.path.append(custom_mod2_path)
sys.path.append(custom_mod3_path)
sys.path.append(custom_mod4_path)
sys.path.append(custom_mod5_path)
sys.path.append(custom_mod6_path)

# Perform the module importations #
#---------------------------------#

import array_handler
import data_frame_handler
import global_parameters
import string_handler

#----------------------------------------------------#
# Define imported module(s)´ function call shortcuts #
#----------------------------------------------------#

basic_time_format_strs = global_parameters.basic_time_format_strs

infer_time_frequency = data_frame_handler.infer_time_frequency
find_date_key = data_frame_handler.find_date_key
save2csv = data_frame_handler.save2csv
save2excel = data_frame_handler.save2excel
insert_row_in_df = data_frame_handler.insert_row_in_df

modify_obj_specs = string_handler.modify_obj_specs
find_substring_index = string_handler.find_substring_index

count_unique_type_objects = array_handler.count_unique_type_objects

#------------------#
# Define functions #
#------------------#

def get_current_time(Type="datetime", time_fmt_str=None):
    
    type_options = ["datetime", "str", "timestamp"]
    arg_names = get_current_time.__code__.co_varnames
        
    type_arg_pos = find_substring_index("Type", arg_names)
    
    if Type not in type_options:
        raise TypeError("Wrong time expression type option "
                        f"at position {type_arg_pos}. "
                        f"Options are {type_options}.")
    
    if Type == "datetime":
        current_datetime = datetime.datetime.now()
    elif Type == "str":
        current_datetime = time.ctime()
    else:
        current_datetime = pd.Timestamp.now()
        
    if Type == "str" and time_fmt_str is not None:
        raise TypeError("Current time is already a string type.")
        
        current_datetime_str\
        = time_format_tweaker(current_datetime, time_fmt_str)
        return current_datetime_str    
    
    elif Type == "str" and time_fmt_str is None:
        return current_datetime
    

def count_time(mode, return_days=False):
    
    global ti
    
    if mode == "start":  
        ti = time.time()
        
    elif mode == "stop":
        tf = time.time()
        elapsed_time = abs(ti-tf)
        
        return time_format_tweaker(elapsed_time,
                                   print_str="extended", 
                                   return_days=return_days)
        
        
def time_format_tweaker(t,
                        time_fmt_str=None,
                        print_str=False,
                        return_days=False,
                        to_pandas_datetime="datetime",
                        std24HourFormat=False):
    
    # 
    # 
    # 
    # 
    # 
    # Parameters
    # ----------
    # t: int, float, str or list of str, tuple, 
    #    time.struct_time or datetime.[datetime, date, time],
    #    numpy.ndarray, pandas.Series or xarray.DataArray 
    # In either case, the object containg the date times.
    # 
    # to_pandas_datetime : {"pandas", "datetime", "model_datetime"}
    # 
    #         Method to use in order to give to the time (t) object.
    # 
    #         If "pandas" is selected, then the dates are treated as strings,
    #         so the function gives the date time format using 
    #         pd.to_datetime formatter.
    # 
    #         If "datetime", then the format is given using
    #         the built-in "datetime" module's datetime.strptime attribute.
    # 
    #         Lastly, the option "model_datetime" is designed in order
    #         to use again "datetime" module, 
    #         but creating a model (or generic) date and time where the year
    #         is 1, for example in model or calendar year calculations
    #         in climate change; that is to say the year is unimportant.         
    # 
    # Returns
    # -------
    # t_res : str, tuple, datetime.datetime,
    #         numpy.ndarray or pandas.DatetimeIndex
    # Array containg the reformatted date times.
    # If the type of calendar used in the original time array
    # is different of Gregorian, it converts to that one.
    # Otherwise the calendar type remains as Gregorian, unchanged.
    
    method_name = inspect.currentframe().f_code.co_name
    arg_names = time_format_tweaker.__code__.co_varnames
    
    print_arg_pos\
    = find_substring_index(arg_names, "print_str", find_whole_words=True)
    t_arg_pos\
    = find_substring_index(arg_names, "t", find_whole_words=True)
    to_pd_dt_arg_pos\
    = find_substring_index(arg_names, "to_pandas", find_whole_words=True)
    
    to_pd_dt_options = ["pandas", "datetime", "model_datetime"]
    print_str_options = [False, "basic", "extended"]
    
    
    if print_str not in print_str_options:
        raise ValueError(f"Wrong '{arg_names[print_arg_pos]}' option. "
                         f"Options are {print_str_options}.")
        
    if to_pandas_datetime not in to_pd_dt_options:
        raise ValueError(f"Wrong '{arg_names[to_pd_dt_arg_pos]}' option. "
                         f"Options are {to_pd_dt_options}.")
        

    if isinstance(t, int) or isinstance(t, float):
        
        # This part assumes that the input 't' time is expressed in seconds #
        if t < 0:
            # If the seconds match the next day's midnight,
            # set the hour to zero instead of 24.
            hours = (t // 3600) % 24
        else:
            hours = t // 3600
            
        minutes = (t % 3600) // 60
        seconds = t % 60
        
        t_res = hours, minutes, seconds
    
        if return_days:
            days = hours // 24
            hours %= 24
            t_res = days, hours, minutes, seconds
            
        # Time printing cases #
        #---------------------#
            
        if print_str == "basic" and not return_days:
            
            if isinstance(t, float):
                hours = int(hours)
                minutes = int(minutes)
                seconds = int(seconds)
                
            t_res_timetuple = datetime.time(hours, minutes, seconds)
            t_res = str(t_res_timetuple)
            
        elif print_str == "basic" and return_days:
            time_str_format_specCase\
            = f"{days:d}:{hours:.0f}:{minutes:.0f}:{seconds:.0f}"
            t_res = time_str_format_specCase
            
        elif print_str == "extended" and return_days:
            t_res = f"{days:.0f} days "\
                    f"{hours:.0f} hours "\
                    f"{minutes:.0f} minutes "\
                    f"{seconds:5.2f} seconds"
                    
        elif print_str == "extended" and not return_days:
            if hours != 0:
                t_res = f"{hours:.0f} hours "\
                        f"{minutes:.0f} minutes "\
                        f"{seconds:5.2f} seconds"
                
            else:
                if minutes != 0:
                    t_res = f"{minutes:.0f} minutes "\
                            f"{seconds:5.2f} seconds"
                  
                else:
                    t_res = f"{seconds:5.2f} seconds"
                    
                    
        return t_res
                    
    
    elif isinstance(t, str):

        if time_fmt_str is None:
            raise ValueError(mixed_error_string.format(type(t), 
                                                       arg_names[0],
                                                       t_arg_pos,
                                                       method_name))
        
        t_res = datetime.datetime.strptime(t, time_fmt_str)
        
        if to_pandas_datetime == "datetime":
            return t_res
        
        elif to_pandas_datetime == "pandas":
            t_timestamp = time2Timestamp(t, time_fmt_str)
            return t_timestamp
    
        elif to_pandas_datetime == "model_datetime":
            if ("%Y" not in time_fmt_str or "%y" not in time_fmt_str)\
                and "%m" not in time_fmt_str\
                and "%d" not in time_fmt_str:
                    
                t_res_aux = datetime.datetime(1, 1, 1,
                                              t_res.hour, t_res.minute, t_res.second)
                t_res = t_res_aux
                
            elif ("%Y" not in time_fmt_str or "%y" not in time_fmt_str)\
                  and "%m" not in time_fmt_str\
                  and "%d" in time_fmt_str:
    
                t_res_aux = datetime.datetime(1, 1, t_res.day, 
                                              t_res.hour, t_res.minute, t_res.second)
                t_res = t_res_aux
                
            elif ("%Y" not in time_fmt_str or "%y" not in time_fmt_str)\
                  and "%m" in time_fmt_str:
            
                t_res_aux = datetime.datetime(1, t_res.month, t_res.day, 
                                              t_res.hour, t_res.minute, t_res.second)
                t_res = t_res_aux
                
            return t_res
                  
      
    elif isinstance(t, tuple) and\
    not(isinstance(t, tuple) and isinstance(t, time.struct_time)):
        
        if time_fmt_str is None:
            raise ValueError(mixed_error_string.format(type(t), 
                                                       arg_names[0],
                                                       t_arg_pos,
                                                       method_name))
            
        t_res = datetime.datetime(*t).strftime(time_fmt_str) 
        if to_pandas_datetime == "pandas":
            raise Exception(f"'{arg_names[t_arg_pos]}' {type(t)} "
                            "will not give a satisfactory DatetimeIndex array.")
            
        return t_res
        
    
    elif isinstance(t, tuple) and isinstance(t, time.struct_time):
        if time_fmt_str is None:
            raise ValueError(mixed_error_string.format(type(t), 
                                                       arg_names[0],
                                                       t_arg_pos,
                                                       method_name))
            
        t_res = datetime.datetime(*t[:-4]).strftime(time_fmt_str)
        if to_pandas_datetime == "pandas":
            raise Exception(f"'{arg_names[t_arg_pos]}' {type(t)} "
                            "will not give a satisfactory DatetimeIndex array.")
            
        return t_res
        
        
    elif isinstance(t, datetime.datetime)\
        or isinstance(t, datetime.date)\
        or isinstance(t, datetime.time):
            
        if time_fmt_str is None:
            raise ValueError(mixed_error_string.format(type(t), 
                                                       arg_names[0],
                                                       t_arg_pos,
                                                       method_name))
            
        t_res = datetime.datetime.strftime(t, time_fmt_str) 
        
        if to_pandas_datetime == "pandas":
            t_timestamp = time2Timestamp(t, time_fmt_str)
            return t_timestamp
        elif to_pandas_datetime == "datetime":
            return t_res
    
        
    elif isinstance(t, cft.datetime):
        if time_fmt_str is None:
            raise ValueError(mixed_error_string.format(type(t), 
                                                        arg_names[0],
                                                        t_arg_pos,
                                                        method_name))
            
        t_res = cft.datetime.strftime(t, time_fmt_str)
        
        if to_pandas_datetime == "pandas":
            t_timestamp = time2Timestamp(t, time_fmt_str)
            return t_timestamp
        elif to_pandas_datetime == "datetime":
            return t_res
        
    elif isinstance(t, pd.DataFrame) or isinstance(t, pd.Series):
        
        t_values = t.values
        
        if t_values.dtype == "O":
            if std24HourFormat:
                try:
                    t_res = properHourRangeConverter(t, time_fmt_str)
                except Exception:
                    raise TypeError("Cannot handle hour range standarization "
                                    f"with '{arg_names[t_arg_pos]}' {type(t)}.")
                    
            else:
                try:
                    t_timestamp = time2Timestamp(t, time_fmt_str)
                    return t_timestamp
                except Exception:
                    raise Exception(f"Cannot convert '{arg_names[t_arg_pos]}' "
                                    f"{type(t)} to DatetimeIndex array.")
            
        else:
            try:
                t_res = t.dt.strftime(time_fmt_str)
            except:
                t_res_series = t.iloc[:,0]
                t_res = t_res_series.dt.strftime(time_fmt_str)
            
        return t_res
        
    else:
        if std24HourFormat:
            try:
                t_res = properHourRangeConverter(t, time_fmt_str)
            except Exception:
                raise TypeError("Cannot handle hour range standarization "
                                f"with '{arg_names[t_arg_pos]}' {type(t)}.")
                
        else:
            try:
                t_timestamp = time2Timestamp(t, time_fmt_str)
                return t_timestamp
            except Exception:
                raise Exception(f"Cannot convert '{arg_names[t_arg_pos]}' "
                                f"{type(t)} to DatetimeIndex array.")
                
            
    
def time2Timestamp(t, time_fmt_str=None):
    
    if not isinstance(t, list)\
        or not isinstance(t, np.ndarray)\
        or not isinstance(t, tuple):
        t_list = [t]
     
    else:
        try:
            t_list = t.values
        except Exception:
            t_list = list(t)
        
    cftime_check = np.all([isinstance(time_el, cft.datetime)
                           for time_el in t_list])
        
    if cftime_check:            
        t_timestamp\
        = pd.to_datetime([cft.datetime.strftime(time_el,
                                                basic_time_format_strs["H"])
                          for time_el in t],
                          format=time_fmt_str)
    
    else:
        t_timestamp = pd.to_datetime(t, format=time_fmt_str)
    
    return t_timestamp
    
    
def properHourRangeConverter(time_df, time_fmt_str):

    # Function that checks whether some range hours
    # are 1-24. If it is the case, it converts to 0-23,
    # otherwise it returns the same data frame.
    # Time 24:00 is assumed to mean the next day,
    # so it is converted to 00:00.
    #
    # Parameters
    # ----------
    # time_df : pd.Series
    #       Pandas series containing the date-times to be checked.
    #
    # Returns
    # -------
    # time_df : pd.Series
    #       The necessary changes are reflected onto the same
    #       data frame as the input one.

    twentyFourHour_df = time_df.str.contains("24")
    twentyFourHour_df_true = twentyFourHour_df[twentyFourHour_df]
    twentyFourHour_df_true_idx = twentyFourHour_df_true.index
    
    records_true = len(twentyFourHour_df_true)

    if records_true > 0:
        for i in twentyFourHour_df_true_idx:
            
            time = time_df.loc[i].replace("24:00","00:00")
            time = time_format_tweaker(time,
                                       time_fmt_str=time_fmt_str, 
                                       to_pandas_datetime=None)
            time += datetime.timedelta(days=1)
            time_df.loc[i] = time

        no24hour_idx = np.delete(twentyFourHour_df.index,
                                 twentyFourHour_df_true_idx)

        time_df.loc[no24hour_idx]\
        = pd.to_datetime(time_df.loc[no24hour_idx], format=time_fmt_str)

    return time_df


def time2seconds(t, time_fmt_str=None):
    
    method_name = inspect.currentframe().f_code.co_name
    
    if isinstance(t, str):
        t_dtTuple = time_format_tweaker(t, time_fmt_str)
        
        days = t_dtTuple.day
        hours = t_dtTuple.hour
        minutes = t_dtTuple.minute
        seconds = t_dtTuple.second
        
        t_secs = days*86400 + hours*3600 + minutes*60 + seconds
        return(t_secs)
        
    elif isinstance(t, tuple):
        
        lt = len(t)
        
        if lt == 4:
            days = t[0]
            hours = t[1]
            minutes = t[2]
            seconds = t[3]
            
            t_secs = days*86400 + hours*3600 + minutes*60 + seconds
            
        elif lt == 3:
            hours = t[0]
            minutes = t[1]
            seconds = t[2]
            
            t_secs = hours*3600 + minutes*60 + seconds
            
        else:
            raise ValueError(f"Method '{method_name}' does neither accept "
                              "years nor months. "
                              "Time tuple structure must be the following:\n"
                              "([days,] hours, minutes, seconds)")
            
        return(t_secs)
    

def get_obj_operation_datetime(objList,
                               attr="modification", 
                               time_fmt_str=None):
    
    attr_options = ["creation", "modification", "access"]
    arg_names = get_obj_operation_datetime.__code__.co_varnames
    
    attr_arg_pos = find_substring_index(arg_names, "attr")
    
    if attr not in attr_options:
        raise ValueError(f"Wrong attribute option at position {attr_arg_pos}. "
                         f"Options are {attr_options}.")
        
    if isinstance(objList, str):
        objList = [objList]
    
    elif isinstance(objList, list):
        
        obj_timestamp_arr = []
        
        for obj in objList:    
            if attr == "creation":
                structTime_attr_obj = time.gmtime(os.path.getctime(obj))
            elif attr == "modification":
                structTime_attr_obj = time.gmtime(os.path.getmtime(obj))
            else:
                structTime_attr_obj = time.gmtime(os.path.getatime(obj))
                
            timestamp_str_attr_obj\
            = time_format_tweaker(structTime_attr_obj, time_fmt_str)
            
            info_list = [obj, timestamp_str_attr_obj]
            obj_timestamp_arr.append(info_list)
            
        obj_timestamp_arr = np.array(obj_timestamp_arr)
        return obj_timestamp_arr
            
        
#------------------#
# Local parameters #
#------------------#

extensions = ["csv", "xlsx", "nc"]

mixed_error_string = """For {} of argument {} at position {}, 
function '{} is designed to output a time string.
Please provide a time string format identifier."""
