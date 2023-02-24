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
        ti = os.times()[-1]
        
    elif mode == "stop":
        tf = os.times()[-1]
        elapsed_time = abs(ti-tf)
        
        return time_format_tweaker(elapsed_time,
                                   print_str="extended", 
                                   return_days=return_days)
        
        
def time_format_tweaker(t,
                        time_fmt_str=None,
                        print_str=None,
                        return_days=False,
                        to_pandas_datetime=False,
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
    # to_pandas_datetime : bool
    #         If True, the function gives, if necessary, the standard (Gregorian)
    #         calendar format to the given array containing datetimes.
    #         In any case, Python sees the dates as strings, so the function
    #         gives the date time format using pd.to_datetime formatter.
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
    
    print_str_options = [None, "basic", "extended"]
    
    if print_str not in print_str_options:
        raise ValueError(f"Wrong '{arg_names[print_arg_pos]}' option. "
                         f"Options are {print_str_options}.")
        

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
        
        if to_pandas_datetime is None:
            return t_res
        
        elif to_pandas_datetime:
            t_timestamp = time2Timestamp(t, time_fmt_str)
            return t_timestamp
    
        else:
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
        if to_pandas_datetime:
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
        if to_pandas_datetime:
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
        
        if to_pandas_datetime:
            t_timestamp = time2Timestamp(t, time_fmt_str)
            return t_timestamp
        else:
            return t_res
    
        
    elif isinstance(t, cft.datetime):
        if time_fmt_str is None:
            raise ValueError(mixed_error_string.format(type(t), 
                                                        arg_names[0],
                                                        t_arg_pos,
                                                        method_name))
            
        t_res = cft.datetime.strftime(t, time_fmt_str)
        
        if to_pandas_datetime:
            t_timestamp = time2Timestamp(t, time_fmt_str)
            return t_timestamp
        else:
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
            

def standardize_calendar(obj,
                         file_path,
                         interpolation_method=None,
                         order=None,
                         save_as_new_obj=False, 
                         extension=None, 
                         separator=",",
                         save_index=False,
                         save_header=False):
        
    # **Function global note** 
    # ------------------------
    # This functions imports 'netcdf_handler' which at the same imports xarray.
    # But not always will the conda environment have installed xarray
    # or the user will not fot_resee any need of installing it,
    # mainly because the basic libraries are already installed.
    #
    # To this day, taking account the structure of the modules
    # and practicity and cleanliness of this function,
    # the 'netcdf_handler' module will only be imported here
    # together with xarray.
    
    # Import module and custom modules here by convenience #
    #------------------------------------------------------#
    
    import xarray as xr
    import netcdf_handler
    
    # Define imported module(s)´ function call shortcuts by convenience #
    #-------------------------------------------------------------------#
        
    find_time_dimension = netcdf_handler.find_time_dimension
    get_file_dimensions = netcdf_handler.get_file_dimensions
    
    #--------------------------------------------------------------------#
    
    # This function standardizes the given calendar of an object to gregorian
    # and makes an interpolation ALONG ROWS (axis=0) to find the missing data.
    # It usually happens when modelled atmospheric or land data is considered,
    # when each model has its own calendar.
    # This funcion is useful when several model data is handled at once.
    # 
    # It only sticks to the limits of the time array pt_resent at the object;
    # further reconstructions is a task left for the user.
    # 
    # Parameters
    # ----------
    # obj : pd.DataFrame or xarray.Dataset
    #       or list of pd.DataFrame or xarray.Dataset.
    #       Object containing data. For each pd.DataFrame, if pt_resent,
    #       the first column must be of type datetime64.
    # file_path : str or list of str
    #       String referring to the file name from which data object 
    #       has been extracted.
    # save_as_new_obj : bool
    #       If True and object is pd.DataFrame, it is saved either
    #       as CSV or Excel containing one or more frames, the latter being
    #       desired by the user.
    # extension : {"csv", "xlsx", "nc"}
    #       The first two only work if object is pd.DataFrame,
    #       while the third works if object is xarray.Dataset.
    #       If "csv" chosen, the whole data frame will be stored in a single
    #       document.
    #       On the other hand, if "xlsx" is selected, then all columns other
    #       than the time array will be introduced in separate tabs,
    #       together with the time array itself.
    # separator : str
    #       String used to separate data columns.
    #       Default value is a comma (',').
    # save_index : bool
    #       Boolean to choose whether to include a column into the excel document
    #       that identifies row numbers. Default value is False.
    # save_header : bool
    #       Boolean to choose whether to include a row into the excel document
    #       that identifies column numbers. Default value is False.
    # 
    # 
    # Returns
    # -------
    # obj : pd.DataFrame, xarray.Dataset 
    #       or xarray.DataArray.
    #       Object containing the standardized calendar to gregorian.
    # 
    # Note
    # ----
    # There is no programatic way to store multiple sheets on a CSV file,
    # as can be donde with Excel files, because CSV is rough, old format
    # but mainly for data transport used.
    
    if isinstance(obj, pd.Dataframe):
        
        if not isinstance(obj, list) and not isinstance(obj, np.ndarray):
            obj = [obj]
            
        if not isinstance(file_path, list) and not isinstance(file_path, np.ndarray):
            file_path = [file_path]
            
        obj_stdCalendar = []
        len_objects = len(obj)
            
        # Check whether all objects passed in a list are of the same type #
        len_unique_type_list = count_unique_type_objects(obj)[-1]
        
        if len_unique_type_list > 1:
            raise ValueError("Not every object in the list is of the same type.")
            
        else:
            """It is supposed that every component is of the same type"""
            if isinstance(obj[0], pd.DataFrame):
                
                for obj_enumerate, fp in zip(enumerate(obj), file_path):
                    
                    obj_num = obj_enumerate[0]
                    obj = obj_enumerate[-1]
                    
                    # Get the date key and time frequency #
                    time_col = find_date_key(obj)
                    time_freq = infer_time_frequency(obj.loc[:10,time_col])
                    
                    # Get the time array with possible missing datetimes #
                    time_shorter = obj.loc[:,time_col]
                    time_shorter_arr = time_format_tweaker(time_shorter)
                    ltm = len(time_shorter)
                   
                    # Construct full time array to compare with the previous array #
                    first_datetime = obj.iloc[0, 0]
                    last_datetime = obj.iloc[-1, 0]
                    
                    full_times = pd.date_range(first_datetime,
                                                last_datetime, 
                                                freq=time_freq)
                    lft = len(full_times)
                    
                    data_frames_remaining = len_objects - (obj_num+1) 
                    print(f"Data frames remaining: {data_frames_remaining}")
                    
                    # Compare both time arrays, even if they have the same length #
                    if ltm != lft:
                        for ft in full_times:
                            if ft not in time_shorter_arr:
                                
                                """Previous day of the missing date-time (indexing)"""
                                missing_date_yesterday\
                                = ft - datetime.timedelta(days=1)
                                index_yesterday\
                                = obj[obj[time_col]==missing_date_yesterday].index
                                
                                """Actual missing time"""
                                index_missing_time = int((index_yesterday + 1).to_numpy())
                                
                                missing_datetime\
                                = missing_date_yesterday + datetime.timedelta(days=1)
                                
                                """Define values to insert"""
                                values = np.append(missing_datetime,
                                                   np.repeat(np.nan, len(obj.columns[1:])))
                                
                                insert_row_in_df(obj, index_missing_time, values=values)
                    
                        # Reorder the data frame indexes #
                        obj = obj.sort_index().t_reset_index(drop=True)
                        obj.iloc[:, 1:] = obj.iloc[:, 1:].astype('d')
                                        
                        # Perform the interpolation, if requested #
                        if interpolation_method is not None:
                            
                            if (interpolation_method == "polynomial"\
                            or interpolation_method == "spline")\
                            and order is None:
                                raise ValueError("Please specify and order for the "
                                                  "interpolation method "
                                                  f"{interpolation_method}")
                        
                            # Fill the missing data as a   #
                            # consequence of missing dates #
                            print("Filling the missing data "
                                  "as a consequence of missing dates...")
                            
                            obj.iloc[:, 1:]\
                            = obj.iloc[:, 1:].interpolate(method=interpolation_method,
                                                          order=order)
                            
                    obj_stdCalendar.append(obj)
        
                    # Save the object either as Excel or CSV document #
                    if save_as_new_obj:
                        
                        obj2change = "name_noext"
                        str2add = "_stdCalendar"
                        
                        saving_file_name = modify_obj_specs(fp,
                                                            obj2change,
                                                            new_obj=None,
                                                            str2add=str2add)
                        
                        if extension == "csv":        
                            
                            print("Saving data into a CSV document...")
                            save2csv(saving_file_name,
                                      obj,
                                      separator,
                                      save_index,
                                      save_header,
                                      date_format=basic_time_format_strs[time_freq])
                            
                        elif extension == "xlsx":
                            
                            frame_dict = {}
                            obj_cols = obj.columns
                            
                            for grid_col in obj_cols[1:]:
                                
                                excel_sheet_name = grid_col
                                frame_dict[excel_sheet_name]\
                                = obj.loc[:, [time_col, grid_col]]
                                
                                print("Writing and storing data "
                                      "into an excel document...")
                                save2excel(saving_file_name,
                                            frame_dict,
                                            save_index,
                                            save_header)
            
                        else:
                            raise ValueError("Wrong extension choice. "
                                             "Options for a Pandas data frame "
                                             "are {'csv', 'xlsx'}.")
                            
        return obj_stdCalendar
    
    # elif isinstance(obj, xr.Dataset) \
    #     or isinstance(obj, xr.DataArray):
            
        # TODO: develop the case for xarray.Dataset objects #
        # elif isinstance(obj[0], xr.Dataset)\
        # or isinstance(obj[0], xr.DataArray):
            

        
#------------------#
# Local parameters #
#------------------#

extensions = ["csv", "xlsx", "nc"]

mixed_error_string = """For {} of argument {} at position {}, 
function '{} is designed to output a time string.
Please provide a time string format identifier."""
