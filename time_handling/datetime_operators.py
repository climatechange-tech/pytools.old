#----------------#
# Import modules #
#----------------#

import datetime
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

custom_mod1_path = f"{fixed_dirpath}/arrays_and_lists"
custom_mod2_path = f"{fixed_dirpath}/files_and_directories" 
custom_mod3_path = f"{fixed_dirpath}/parameters_and_constants"
custom_mod4_path = f"{fixed_dirpath}/pandas_data_frames" 
custom_mod5_path = f"{fixed_dirpath}/sets_and_intervals"
custom_mod6_path = f"{fixed_dirpath}/strings"
custom_mod7_path = f"{fixed_dirpath}/time_handling"
                  
# Add the module paths to the path variable #
#-------------------------------------------#

sys.path.append(custom_mod1_path)
sys.path.append(custom_mod2_path)
sys.path.append(custom_mod3_path)
sys.path.append(custom_mod4_path)
sys.path.append(custom_mod5_path)
sys.path.append(custom_mod6_path)
sys.path.append(custom_mod7_path)

# Perform the module importations #
#---------------------------------#

import array_handler
import data_frame_handler
import global_parameters
import interval_operators
import string_handler
import time_formatters

#----------------------------------------------------#
# Define imported module(s)´ function call shortcuts #
#----------------------------------------------------#

basic_time_format_strs = global_parameters.basic_time_format_strs
mathematical_year_days = global_parameters.mathematical_year_days

count_unique_type_objects = array_handler.count_unique_type_objects

find_date_key = data_frame_handler.find_date_key
infer_time_frequency = data_frame_handler.infer_time_frequency
insert_row_in_df = data_frame_handler.insert_row_in_df
save2csv = data_frame_handler.save2csv
save2excel = data_frame_handler.save2excel

define_interval = interval_operators.define_interval

find_substring_index = string_handler.find_substring_index
modify_obj_specs = string_handler.modify_obj_specs

time_format_tweaker = time_formatters.time_format_tweaker

#%%

#------------------#
# Define functions #
#------------------#

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
            
            
# TODO: dt_objs (pandas, datetime edo np.datetime64)
# def datetime_obj_basic_operations():
            
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

