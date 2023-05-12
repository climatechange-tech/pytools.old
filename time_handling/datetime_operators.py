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
custom_mod5_path = f"{fixed_dirpath}/strings"
custom_mod6_path = f"{fixed_dirpath}/time_handling"
                  
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
import time_formatters

#----------------------------------------------------#
# Define imported module(s)´ function call shortcuts #
#----------------------------------------------------#

# basic_time_format_strs = global_parameters.basic_time_format_strs
mathematical_year_days = global_parameters.mathematical_year_days

# count_unique_type_objects = array_handler.count_unique_type_objects

# infer_time_frequency = data_frame_handler.infer_time_frequency
# find_date_key = data_frame_handler.find_date_key
# save2csv = data_frame_handler.save2csv
# save2excel = data_frame_handler.save2excel
# insert_row_in_df = data_frame_handler.insert_row_in_df

# modify_obj_specs = string_handler.modify_obj_specs

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
            
#%%

# TODO: birfindu ondoko guztia
            
# def natural_year(dt_start, dt_end, 
#                   time_fmt_str=None,
#                   strict=False, exact_year=False,
#                   return_str=False):
    
dt_start="210528"
dt_end="230227"

# time_fmt_str="%d%m%y"
time_fmt_str="%y%m%d"

strict=False
exact_year=True


    
dt_start_std = time_format_tweaker(dt_start,
                                   time_fmt_str, 
                                   to_pandas_datetime="datetime")

dt_end_std = time_format_tweaker(dt_end, 
                                 time_fmt_str,
                                 to_pandas_datetime="datetime")

timeDelta = abs(dt_start_std - dt_end_std)

try:
    timeDelta_days = timeDelta.to_pytimedelta().days
except:
    timeDelta_days = timeDelta.days

n = timeDelta_days // mathematical_year_days    

# Intervals #

# TODO: ondokoa ibiltarteen sortzaileen funtzioren batera???
ndays_oneYear = pd.Interval(mathematical_year_days*n,
                            mathematical_year_days*(n+1),
                            closed="left")

ndays_oneYear_upper_half\
= pd.Interval(mathematical_year_days*n + mathematical_year_days/2,
              mathematical_year_days*(n+1),
              closed="left")

#%%

if not strict:
    
    if n > 0:
        
        # TODO: eta ondokoa hobeto?
        # timeDelta_days not in ndays_oneYear_upper_half
        
        if timeDelta_days in ndays_oneYear\
        and timeDelta_days not in ndays_oneYear_upper_half:
            
            ti_natural_year = dt_end_std.year - n
            ti_natural_month = dt_end_std.month
            
            tf_natural_year = dt_start_std.year
            tf_natural_month = ti_natural_month
            tf_natural_day = dt_end_std.day
            
            if not exact_year:
                ti_natural_day = 1
                
            else:
                ti_natural_day = tf_natural_day
                dt_start_natural = pd.Timestamp(ti_natural_year, 
                                                ti_natural_month,
                                                ti_natural_day) + pd.Timedelta(days=1)
                
                
        # TODO: eta ondokoa hobeto?
        # elif timeDelta_days in ndays_oneYear_upper_half:
                    
        elif timeDelta_days in ndays_oneYear\
            and timeDelta_days in ndays_oneYear_upper_half:
            
            ti_natural_year = dt_end_std.year - n
            ti_natural_month = dt_start_std.month
            
            tf_natural_year = dt_start_std.year
            tf_natural_month = ti_natural_month
            tf_natural_day = dt_end_std.day
            
            if not exact_year:
                ti_natural_day = 1
                
            else:
                ti_natural_day = tf_natural_day
                dt_start_natural = pd.Timestamp(ti_natural_year, 
                                                ti_natural_month,
                                                ti_natural_day) + pd.Timedelta(days=1)
      
    elif n == 0:
                
        ti_natural_year = dt_start_std.year
        ti_natural_month = dt_start_std.month
        ti_natural_day = dt_start_std.day
        
        tf_natural_year = dt_end_std.year
        tf_natural_month = dt_end_std.month
        tf_natural_day = dt_end_std.day
        
        dt_start_natural = pd.Timestamp(tf_natural_year, 
                                      tf_natural_month,
                                      tf_natural_day)        
        
        dt_end_natural = pd.Timestamp(tf_natural_year, 
                                      tf_natural_month,
                                      tf_natural_day)
      
#%%
            
else:
    #%%
          
    ti_natural_year = dt_end_std.year - 1
    ti_natural_month = dt_end_std.month
    
    tf_natural_year = dt_end_std.year
    tf_natural_month = ti_natural_month
    tf_natural_day = dt_end_std.day
    
    if not exact_year:
        ti_natural_day = 1
        
        dt_start_natural = pd.Timestamp(ti_natural_year, 
                                        ti_natural_month,
                                        ti_natural_day)
           
    else:
        ti_natural_day = dt_end_std.day
        
        if tf_natural_month == 12:
            tf_natural_month_next = 1
            tf_natural_year_next = tf_natural_year + 1
        else:
            tf_natural_month_next = tf_natural_month + 1
            tf_natural_year_next = tf_natural_year
               
        dt_start_natural = pd.Timestamp(ti_natural_year, 
                                        ti_natural_month,
                                        ti_natural_day) + pd.Timedelta(days=1)
        
    dt_end_natural = pd.Timestamp(tf_natural_year, 
                                  tf_natural_month,
                                  tf_natural_day)

print(dt_start_natural, dt_end_natural)
                

#%%

if n > 0:
    
    
    
elif n == 0:
    
    ti_natural_year = dt_start_std.year
    ti_natural_month = dt_start_std.month
    ti_natural_day = dt_start_std.day
    
    tf_natural_year = dt_end_std.year
    tf_natural_month = dt_end_std.month
    tf_natural_day = dt_end_std.day
    
    dt_start_natural = pd.Timestamp(tf_natural_year, 
                                  tf_natural_month,
                                  tf_natural_day)        
    
    dt_end_natural = pd.Timestamp(tf_natural_year, 
                                  tf_natural_month,
                                  tf_natural_day)
    
    # kitto
                
#%%

# if format_output:
    
#     natural_year_range_table ="""
#     Natural year belonging to the date range
#     """
    
#     print(natural_year_range_table.format())
    
            
            