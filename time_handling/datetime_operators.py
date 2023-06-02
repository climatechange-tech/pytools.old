#----------------#
# Import modules #
#----------------#

import datetime
import os
import time

from pathlib import Path
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

custom_mod1_path = f"{fixed_dirpath}/parameters_and_constants"
custom_mod2_path = f"{fixed_dirpath}/pandas_data_frames" 
custom_mod3_path = f"{fixed_dirpath}/strings"
custom_mod4_path = f"{fixed_dirpath}/time_handling"
                  
# Add the module paths to the path variable #
#-------------------------------------------#

sys.path.append(custom_mod1_path)
sys.path.append(custom_mod2_path)
sys.path.append(custom_mod3_path)
sys.path.append(custom_mod4_path)

# Perform the module importations #
#---------------------------------#

import data_frame_handler
import global_parameters
import interval_operators
import string_handler
import time_formatters

#----------------------------------------------------#
# Define imported module(s)´ function call shortcuts #
#----------------------------------------------------#

mathematical_year_days = global_parameters.mathematical_year_days
find_date_key = data_frame_handler.find_date_key
define_interval = interval_operators.define_interval
find_substring_index = string_handler.find_substring_index
time_format_tweaker = time_formatters.time_format_tweaker

#%%

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

def datetime_range_operator(df1, df2, operator, time_fmt_str=None):
    
    # Quality control #
    #-----------------#
    
    # Main argument names and their position on the function's definition #    
    arg_names = datetime_range_operator.__code__.co_varnames
    
    df1_arg_pos\
    = find_substring_index(arg_names, "df1", find_whole_words=True)
    
    df2_arg_pos\
    = find_substring_index(arg_names, "df2", find_whole_words=True)
    
    operator_arg_pos\
    = find_substring_index(arg_names, "operator", find_whole_words=True)
    
    operators = ["merge", "intersect", "cross", "left", "right"]
    
    # Operator argument choice #    
    if operator not in operators:
        raise ValueError(f"Wrong '{arg_names[operator_arg_pos]}' option. "
                         f"Options are {operators}.")
        
    # Right input argument types #
    if not isinstance(df1, pd.DataFrame):
        raise ValueError(f"Argument '{arg_names[df1_arg_pos]}' "
                         "must be of type pd.DataFrame")
        
    if not isinstance(df2, pd.DataFrame)\
    or not isinstance(df2, pd.Series):
        raise ValueError(f"Argument '{arg_names[df2_arg_pos]}' "
                         "must be of type pd.DataFrame")
        
        
    elif isinstance(df2, pd.Series):
        if not hasattr(df2, "name"):
            raise ValueError(f"Argument '{arg_names[df2_arg_pos]}' "
                             "is of type pd.Series but it is unnamed. "
                             "Please set a name using "
                             f"{arg_names[df2_arg_pos]}.name attribute.")
            
            
    # Operations #
    #------------#
    
    res_dts = pd.merge(df1, df2, how=operator)
    
    # Sort values by the time-column #
    try:
        dt_colname = find_date_key(df1)
    except:
        try:
            dt_colname = find_date_key(df2)
        except:
            raise ValueError("Could not find a common time column name.")
    
    res_dts = res_dts.sort_values(by=dt_colname)
    
    # Choose whether to customize ll times' format #
    if time_fmt_str is not None:
        res_dts = time_format_tweaker(res_dts, time_fmt_str)
        
    return res_dts

    
def natural_year(dt_start, dt_end, time_fmt_str=None,
                 strict=False, exact_year=False,
                 return_format="str"):
    
    # Quality control #
    #-----------------#
    
    # Main argument names and their position on the function's definition #    
    arg_names = natural_year.__code__.co_varnames
    
    dt_start_arg_pos\
    = find_substring_index(arg_names, "dt_start", find_whole_words=True)
    
    dt_end_arg_pos\
    = find_substring_index(arg_names, "dt_end", find_whole_words=True)
    
    return_fmt_arg_pos\
    = find_substring_index(arg_names, "return_format", find_whole_words=True)
    
    return_fmt_options = ["str", "pandas", "datetime"]
    
    # Result printing format's argument choice #    
    if return_format not in return_fmt_options:
        raise ValueError(f"Wrong '{arg_names[return_fmt_arg_pos]}' option. "
                         f"Options are {return_fmt_options}.")
        
      
    # String to string format conversion checker #
    try:     
        dt_start_std = time_format_tweaker(dt_start, time_fmt_str,
                                           to_pandas_datetime=return_format)
        
    except ValueError:
        print(f"Please set the argument '{arg_names[return_fmt_arg_pos]}' to "
              f"'{return_fmt_options[1]}' or '{return_fmt_options[-1]}', "
              f"else make the argument '{arg_names[dt_start_arg_pos]}' to be of type "
              "'pd.Timestamp' or 'datetime.datetime'")
        
    try:
        dt_end_std = time_format_tweaker(dt_end, time_fmt_str,
                                         to_pandas_datetime=return_format)
        
    except ValueError:
        print(f"Please set the argument {return_format} to "
              f"'{return_fmt_options[1]}' or '{return_fmt_options[-1]}', "
              f"else make the argument '{arg_names[dt_end_arg_pos]}' to be of type "
              "'pd.Timestamp' or 'datetime.datetime'")


    # Operations #    
    timeDelta = abs(dt_start_std - dt_end_std)
    
    try:
        timeDelta_days = timeDelta.days
    except:
        timeDelta_days = timeDelta.to_pytimedelta().days
    
    n = timeDelta_days // mathematical_year_days    
    
    # Intervals #    
    ndays_oneYear_upper_half\
    = define_interval(mathematical_year_days*n + mathematical_year_days/2,
                      mathematical_year_days*(n+1),
                      closed="left")

    
    #%%
    
    tf_natural_day = dt_end_std.day
    
    if n > 0:
        ti_natural_month = dt_end_std.month
        tf_natural_month = ti_natural_month
        
        if strict:
            tf_natural_year = dt_end_std.year
            ti_natural_year = tf_natural_year - 1
            
            if exact_year:
                ti_natural_day = dt_end_std.day 
                
                if return_format == "pandas":
                    dt_start_natural\
                    = pd.Timestamp(ti_natural_year, 
                                   ti_natural_month,
                                   ti_natural_day) + pd.Timedelta(days=1)
                    
                else:
                    dt_start_natural\
                    = datetime.datetime(ti_natural_year, 
                                        ti_natural_month,
                                        ti_natural_day)+ datetime.timedelta(days=1)
        
            
            else:
                ti_natural_day = 1
                
                if return_format == "pandas":
                    dt_start_natural = pd.Timestamp(ti_natural_year, 
                                                    ti_natural_month,
                                                    ti_natural_day)
                elif return_format == "datetime":
                    dt_start_natural = datetime.datetime(ti_natural_year, 
                                                         ti_natural_month,
                                                         ti_natural_day)
                    
        else:
            tf_natural_year = dt_end_std.year
            ti_natural_year = tf_natural_year - n
            
            
            if timeDelta_days in ndays_oneYear_upper_half:
                ti_natural_month = dt_start_std.month
                    
            elif timeDelta_days not in ndays_oneYear_upper_half:
                ti_natural_month = dt_end_std.month
                
            if exact_year:
                ti_natural_day = tf_natural_day
                dt_start_natural\
                = pd.Timestamp(ti_natural_year, 
                               ti_natural_month,
                               ti_natural_day) + pd.Timedelta(days=1)
    
            else:
                ti_natural_day = 1
                dt_start_natural = pd.Timestamp(ti_natural_year, 
                                                ti_natural_month,
                                                ti_natural_day)
                
    elif n == 0:
        
        ti_natural_year = dt_start_std.year
        ti_natural_month = dt_start_std.month
        ti_natural_day = dt_start_std.day
        
        tf_natural_year = dt_end_std.year
        tf_natural_month = dt_end_std.month
        
        if return_format == "pandas":
            dt_start_natural = pd.Timestamp(ti_natural_year, 
                                            ti_natural_month,
                                            ti_natural_day)        
        elif return_format == "datetime":
            dt_start_natural = datetime.datetime(ti_natural_year, 
                                                 ti_natural_month,
                                                 ti_natural_day)  
            
    if return_format == "pandas":
        dt_end_natural = pd.Timestamp(tf_natural_year, 
                                      tf_natural_month,
                                      tf_natural_day)
        
    elif return_format == "datetime":
        dt_end_natural = datetime.datetime(tf_natural_year, 
                                           tf_natural_month,
                                           tf_natural_day)
        
    # Choose between returning the results as strings or datetime objects #     
    if return_format == "str":
        natural_year_range_table ="""
        {} -- {}
        
        |
        |
        v
        
        {dt_start_natural} --{dt_end_natural}
        """
           
        print(natural_year_range_table.format(dt_start_std, dt_end_std))
    
    else:
        return dt_start_natural, dt_end_natural

