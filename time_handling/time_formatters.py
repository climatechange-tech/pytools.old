#----------------#
# Import modules #
#----------------#

import datetime
import time

import inspect
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

custom_mod1_path = f"{fixed_dirpath}/files_and_directories" 
custom_mod2_path = f"{fixed_dirpath}/strings"
                  
# Add the module paths to the path variable #
#-------------------------------------------#

sys.path.append(custom_mod1_path)
sys.path.append(custom_mod2_path)

# Perform the module importations #
#---------------------------------#

import string_handler

#----------------------------------------------------#
# Define imported module(s)´ function call shortcuts #
#----------------------------------------------------#

find_substring_index = string_handler.find_substring_index
substring_replacer = string_handler.substring_replacer

#------------------#
# Define functions #
#------------------#
        
def time_format_tweaker(t,
                        time_fmt_str=None,
                        return_str=False,
                        return_days=False,
                        method="datetime",
                        infer_dt_format=False, # Only if method=="pandas"
                        standardizeHourRange=False):
    
    # 
    # 
    # 
    # 
    # 
    # Parameters
    # ----------
    # t: int, float, str or list of str, tuple, 
    #    time.struct_time or datetime.[datetime, date, time],
    #    array-like, pandas.Series or xarray.DataArray 
    # In either case, the object containg the dates and times.
    # 
    # TODO: ondoko guztiak hobeto azaldu
    # method : {"numpy_generic", "numpy_dt64",
    #           "pandas", 
    #           "datetime", "model_datetime"}
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
    #         array-like or pandas.[DatetimeIndex, DataFrame, Series]
    # 
    # Array containg the reformatted date times.
    # If the type of calendar used in the original time array
    # is different of Gregorian, it converts to that one.
    # Otherwise the calendar type remains as Gregorian, unchanged.
    
    method_name = inspect.currentframe().f_code.co_name
    arg_names = time_format_tweaker.__code__.co_varnames
    
    print_arg_pos\
    = find_substring_index(arg_names, "return_str", find_whole_words=True)
    t_arg_pos\
    = find_substring_index(arg_names, "t", find_whole_words=True)
    method_arg_pos\
    = find_substring_index(arg_names, "method", find_whole_words=True)
    
    return_str_options = [False, "basic", "extended"]
    
    
    if return_str not in return_str_options:
        raise ValueError(ValueErrorStr.format(arg_names[print_arg_pos],
                                              return_str_options))
        
    if method not in method_options:
        raise ValueError(ValueErrorStr.format(arg_names[method_arg_pos],
                                              method_options))

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
            
        if return_str == "basic" and not return_days:
            
            if isinstance(t, float):
                hours = int(hours)
                minutes = int(minutes)
                seconds = int(seconds)
                
            t_res_timetuple = datetime.time(hours, minutes, seconds)
            t_res = str(t_res_timetuple)
            
        elif return_str == "basic" and return_days:
            time_str_format_specCase\
            = f"{days:d}:{hours:.0f}:{minutes:.0f}:{seconds:.0f}"
            t_res = time_str_format_specCase
            
        elif return_str == "extended" and return_days:
            t_res = f"{days:.0f} days "\
                    f"{hours:.0f} hours "\
                    f"{minutes:.0f} minutes "\
                    f"{seconds:6.3f} seconds"
                    
        elif return_str == "extended" and not return_days:
            if hours != 0:
                t_res = f"{hours:.0f} hours "\
                        f"{minutes:.0f} minutes "\
                        f"{seconds:6.3f} seconds"
                
            else:
                if minutes != 0:
                    t_res = f"{minutes:.0f} minutes "\
                            f"{seconds:6.3f} seconds"
                  
                else:
                    t_res = f"{seconds:6.3f} seconds"
                    
                    
        return t_res
                    
    
    elif isinstance(t, str):

        if time_fmt_str is None:
            raise ValueError(noStringFormatErrorStr.format(type(t), 
                                                           arg_names[0],
                                                           t_arg_pos,
                                                           method_name))

        particularAllowedMethods = ["pandas", "datetime", "model_datetime"]
        if method not in particularAllowedMethods:
            raise ValueError(ValueErrorForTypeCaseStr.format\
                             (arg_names[method_arg_pos],
                              method,
                              arg_names[t_arg_pos],
                              type(eval(arg_names[t_arg_pos])),
                              particularAllowedMethods))
        
    
        if method == "model_datetime":
            t_res = frequentTimeFormatConverter(t,
                                                method="datetime",
                                                time_fmt_str=time_fmt_str)
            
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
        
        else:
            t_res = frequentTimeFormatConverter(t, method, time_fmt_str)
            return t_res
                  
      
    elif isinstance(t, tuple) and\
    not(isinstance(t, tuple) and isinstance(t, time.struct_time)):
        
        if time_fmt_str is None:
            raise ValueError(noStringFormatErrorStr.format(type(t), 
                                                           arg_names[0],
                                                           t_arg_pos,
                                                           method_name))
            
        t_res = datetime.datetime(*t).strftime(time_fmt_str) 
        if method == "pandas":            
            raise Exception(notSatisfactoryDTObjectErrorStr.format\
                            (arg_names[t_arg_pos], type(t)))
            
        return t_res
        
    
    elif isinstance(t, tuple) and isinstance(t, time.struct_time):
        if time_fmt_str is None:
            raise ValueError(noStringFormatErrorStr.format(type(t), 
                                                           arg_names[0],
                                                           t_arg_pos,
                                                           method_name))
            
        t_res = datetime.datetime(*t[:-3]).strftime(time_fmt_str)
        if method == "pandas":
            raise Exception(notSatisfactoryDTObjectErrorStr.format\
                            (arg_names[t_arg_pos], type(t)))
            
        return t_res
        
        
    elif (isinstance(t, datetime.datetime)\
        or isinstance(t, datetime.date)\
        or isinstance(t, datetime.time))\
        and not isinstance(t, pd.Timestamp):
            
        if not return_days:
            method = "pandas"
            t_res = frequentTimeFormatConverter(t, method, time_fmt_str) 
        else:
            t_res = datetime.datetime.strftime(t, time_fmt_str)
        
        return t_res


    elif isinstance(t, pd.Timestamp):
        
        if not return_str:
        
            particularAllowedMethods = ["numpy_generic", "numpy_dt64", "datetime_pydt"]
            if method not in particularAllowedMethods:                    
                raise ValueError(ValueErrorForTypeCaseStr.format\
                                 (arg_names[method_arg_pos],
                                  method,
                                  arg_names[t_arg_pos],
                                  type(eval(arg_names[t_arg_pos])),
                                  particularAllowedMethods))
            
            if method == "numpy_generic":
                t_res = frequentTimeFormatConverter(t, method)
            elif method == "numpy_dt64":
                t_res = frequentTimeFormatConverter(t, method)
            elif method == "datetime_pydt":
                t_res = frequentTimeFormatConverter(t, method)
            
            return t_res
        
        elif return_str == "extended":
            raise ValueError(ValueErrorForTypeCaseStr.format\
                             (arg_names[print_arg_pos],
                              return_days,
                              arg_names[t_arg_pos],
                              type(eval(arg_names[t_arg_pos])),
                              particularAllowedMethods))
            
        elif return_str == "basic" :
            t_res = t.strftime(time_fmt_str)
            return t_res
        
    elif isinstance(t, np.datetime64):
        
        if method == "datetime_list":
            t_res = frequentTimeFormatConverter(t, method)
        if return_str:
            t_res = str(t)
        return t_res
    

    
    else:
                
        particularAllowedMethod = "datetime_list"
        if method != particularAllowedMethod:
            raise ValueError(ValueErrorForTypeCaseStr.format\
                             (arg_names[method_arg_pos],
                              method,
                              arg_names[t_arg_pos],
                              type(eval(arg_names[t_arg_pos])),
                              particularAllowedMethod))
                
        if standardizeHourRange:
            try:
                t_res = over24HourFixer(t)
            except Exception:                
                raise TypeError(unhandleableErrorStr.format(arg_names[t_arg_pos],
                                                            type(t)))
                
        else:
                    
            particularAllowedMethods = ["numpy_dt64_array", "pandas"]
            if method not in particularAllowedMethods:
                raise ValueError(ValueErrorForTypeCaseStr.format\
                                 (arg_names[method_arg_pos],
                                  method,
                                  arg_names[t_arg_pos],
                                  type(eval(arg_names[t_arg_pos])),
                                  particularAllowedMethods))
            
            if method == "pandas":
                t_res = frequentTimeFormatConverter(t, method, time_fmt_str)             
            elif method == "numpy_dt64_array":
                t_res = frequentTimeFormatConverter(t, method)
            
        if return_str:
            if isinstance(t_res, pd.DataFrame) or isinstance(t_res, pd.Series):
                t_res = t_res.dt.strftime(time_fmt_str) 
            elif isinstance(t_res, np.ndarray):
                t_res = t_res.astype('U')
            else:
                try:
                    t_res  = t_res.strftime(time_fmt_str)
                except:
                    raise Exception(unconverteablePandasDTObjectErrorStr.format\
                                    (arg_names[t_arg_pos, type(t_res)]))
    
        return t_res
                
                
def frequentTimeFormatConverter(t,
                                method=None,
                                time_fmt_str=None,
                                infer_dt_format=False):
    
    arg_names = frequentTimeFormatConverter.__code__.co_varnames
    
    method_arg_pos\
    = find_substring_index(arg_names, "method", find_whole_words=False)
    
    if method not in method_options:
        raise ValueError(ValueErrorStr.format(arg_names[method_arg_pos], 
                                              method_options))
    
    if method == "datetime":
        dtobj = datetime.datetime.strptime(t, time_fmt_str)
        
    elif method == "datetime_list":
        dtobj = t.tolist()
        
    elif method == "datetime_pydt":
        dtobj = t.to_pydatetime()
        
    elif method == "pandas":
        try:
            dtobj = pd.to_datetime(t,
                                   format=time_fmt_str,
                                   infer_datetime_format=infer_dt_format)
            
        except:        
            import cftime as cft
            dtobj\
            = pd.to_datetime([cft.datetime.strftime(time_el,
                                                    format=time_fmt_str)
                              for time_el in t],
                              format=time_fmt_str,
                              infer_datetime_format=infer_dt_format)
            
    elif method == "numpy_dt64":
        dtobj = t.to_datetime64()
            
    elif method == "numpy_dt64_array":
        dtobj = np.array(t, dtype=np.datetime64)
        
    elif method == "numpy_generic":
        dtobj = t.to_numpy()
        
    return dtobj
    
    
def over24HourFixer(time_obj):

    # Function that checks whether the range of hours
    # contained in an object (numpy's or pandas's) is the 24-hour standard 0-23.
    # 
    # For the task, the date and times in the input object 
    # must only be of type string, otherwise it is not possible
    # to define non standard hour ranges like 1-24
    # with Timestamp-like attributes.
    # 
    # Time 24:00 is assumed to mean the next day,
    # so it is converted to string 23:00 and then 
    # an hour time delta is added to it.
    #
    # Parameters
    # ----------
    # time_obj : array-like of strings, pandas.DataFrame or pandas.Series
    #       Object containing the date and times to be checked.
    #
    # Returns
    # -------
    # time_obj_fixed : array-like, pandas.DataFrame or pandas.Series
    #       Object containing fixed dates and times.
   
    if isinstance(time_obj, np.ndarray):
        twentyFourHourIdx = find_substring_index(time_obj, "24:0")
        time_obj_no24Hour = substring_replacer(time_obj, "24:0", "23:0")
        
        time_obj_fixed = frequentTimeFormatConverter(time_obj_no24Hour, 
                                                     method="numpy_dt64_array")
        time_obj_fixed[twentyFourHourIdx] += np.timedelta64(1, "s")
        
    elif isinstance(time_obj, pd.DataFrame) or isinstance(time_obj, pd.Series):
        try:
            twentyFourHourIdx = time_obj.str.contains("24:0")
        except:
            twentyFourHourIdx = time_obj.iloc[:,0].str.contains("24:0")
            
        twentyFourHourIdxFilt = twentyFourHourIdx[twentyFourHourIdx]  
        time_obj_no24Hour = substring_replacer(time_obj, "24:0", "23:0")
            
        time_obj_fixed = frequentTimeFormatConverter(time_obj_no24Hour,
                                                     method="pandas")
        time_obj_fixed[twentyFourHourIdxFilt] += pd.Timedelta(hours=1)
        
    # TODO: ondokoa garatu
    # else:
    #     import xarray as xr
             
    return time_obj_fixed


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
    

#------------------#
# Local parameters #
#------------------#

# Global method options #
method_options = ["datetime", "datetime_list", "datetime_pydt",
                  "pandas", "numpy_dt64", "numpy_dt64_array", "numpy_generic"]

# Extension list #
extensions = ["csv", "xlsx", "nc"]

# Error message strings #
noStringFormatErrorStr = \
"""For {} of argument '{}' at position {}, 
function '{}' is designed to output a time string.
Please provide a time string format identifier.
"""

ValueErrorStr = """Wrong '{}' option. Options are {}."""
ValueErrorForTypeCaseStr = """'{}'=='{}' not allowed for argument '{}' of type {}.
Options are {}."""

AttributeErrorStr = """Wrong attribute option at position {}. Options are {}. """

notSatisfactoryDTObjectErrorStr = \
"""{} of type {} will not give a satisfactory pandas's timestamp containing object."""

unhandleableErrorStr = """Cannot handle hour range standarization with {} of type {}."""

unconverteablePandasDTObjectErrorStr = \
"""Cannot convert {} of type {} to pandas's timestamp containing object."""