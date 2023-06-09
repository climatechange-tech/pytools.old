#----------------#
# Import modules #
#----------------#

import calendar
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
custom_mod2_path = f"{fixed_dirpath}/parameters_and_constants"
custom_mod3_path = f"{fixed_dirpath}/pandas_data_frames" 
custom_mod4_path = f"{fixed_dirpath}/strings"
custom_mod5_path = f"{fixed_dirpath}/time_handling"
                  
# Add the module paths to the path variable #
#-------------------------------------------#

sys.path.append(custom_mod1_path)
sys.path.append(custom_mod2_path)
sys.path.append(custom_mod3_path)
sys.path.append(custom_mod4_path)
sys.path.append(custom_mod5_path)

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

basic_time_format_strs = global_parameters.basic_time_format_strs

count_unique_type_objects = array_handler.count_unique_type_objects

find_date_key = data_frame_handler.find_date_key
infer_time_frequency = data_frame_handler.infer_time_frequency
insert_row_in_df = data_frame_handler.insert_row_in_df
save2csv = data_frame_handler.save2csv
save2excel = data_frame_handler.save2excel

find_substring_index = string_handler.find_substring_index
modify_obj_specs = string_handler.modify_obj_specs

time_format_tweaker = time_formatters.time_format_tweaker

#------------------#
# Define functions #
#------------------#

def standardize_calendar(obj,
                         file_path,
                         obj_type="pandas",
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
    
    obj_types = ["pandas", "xarray"]

    arg_names = standardize_calendar.__code__.co_varnames
    obj_type_arg_pos = find_substring_index(arg_names, "obj_type")
    
    if obj_type not in obj_types:
        raise ValueError(f"Wrong '{arg_names[obj_type_arg_pos]}' argument. "
                         f"Options are {obj_types}.")
        
    if obj_type == "pandas":

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
    
    elif obj_type == "xarray":
        
        # Import module and custom modules here by convenience #
        #------------------------------------------------------#
        
        import xarray as xr
        import netcdf_handler
        
        # Define imported module(s)´ function call shortcuts by convenience #
        #-------------------------------------------------------------------#
            
        find_time_dimension = netcdf_handler.find_time_dimension
        get_file_dimensions = netcdf_handler.get_file_dimensions
 
        # TODO: develop the case for xarray.Dataset objects #
        # elif isinstance(obj[0], xr.Dataset)\
        # or isinstance(obj[0], xr.DataArray):

def week_range(date):
    
    # Finds the week day-range, i.e, the first and last day of the week
    # where a given calendar day lies on.
    # In Europe weeks start on Monday and end on Sunday.
    # 
    # Parameters
    # ----------
    # date : pandas._libs.tslibs.timestamps.Timestamp
    #       Timestamp format string that contains a particular date time.
    # start_date, end_date: str
    #       Pair of strings that refer, respectively, to the first and
    #       last days of the week that lies the given date within.
    
    
    # Isocalendar function #
    #----------------------#
    
    # isocalendar calculates the year, week of the year, and day of the week (dow).
    # dow is Mon = 1, Sat = 6, Sun = 7
    
    if isinstance(date, pd._libs.tslibs.timestamps.Timestamp):
        
        year, week, dow = date.isocalendar()

        # Find the first day of the week
        #-------------------------------
        
        if dow == 1:
            # Since we want to start with Monday, let's test for that condition.
            start_date = date
        else:
            # Otherwise, subtract the `dow` number days 
            # that have passed from Monday to get the first day.
            start_date = date - (datetime.timedelta(dow) - datetime.timedelta(1))

        # Now, add 6 for the last day of the week (i.e., count up to Sunday) #
        #--------------------------------------------------------------------#
        
        end_date = start_date + datetime.timedelta(6)

        return (start_date, end_date)
        
    else:
        raise ValueError("The date given is not a Timestamp") 
        
        
def nearest_leap_year(year):
    
    year_isleap = leapYearDetector(year, year)
    
    if not year_isleap:
        year_list = list(range(year-4, year+4))
        lyl = len(year_list)
        
        nearest_leap_year_idx = [i
                                 for i in range(lyl) 
                                 if leapYearDetector(year_list[i], year_list[i])]
        
        min_idx = nearest_leap_year_idx[0]
        max_idx = nearest_leap_year_idx[1]
        
        min_idx_year_diff = abs(year_list[min_idx] - year)
        max_idx_year_diff = abs(year_list[max_idx] - year)
        
        if min_idx_year_diff > 1 and min_idx_year_diff != 2:
            nearest_lp_year = year_list[max_idx]
        elif max_idx_year_diff > 1 and max_idx_year_diff != 2:
            nearest_lp_year = year_list[min_idx]
        elif min_idx_year_diff == max_idx_year_diff:
            nearest_lp_year = f"{year_list[min_idx]} or {year_list[max_idx]}"
        
    else:
        nearest_lp_year = year
        
    return nearest_lp_year


def leapYearDetector(start_year, end_year, return_days=False):
    
    if isinstance(start_year, str):
        start_year = eval(start_year)
    if isinstance(end_year, str):
        end_year = eval(end_year)
    
    if return_days:
        
        if start_year == end_year:
            days_year = len(pd.date_range(str(start_year),
                                          str(start_year+1),
                                          inclusive="left"))
            return days_year
            
        else:
            days_per_year = [len(pd.date_range(str(year),
                                               str(year+1),
                                               inclusive="left"))
                             for year in range(start_year, end_year+1)]
            return days_per_year
        
    else:
        if start_year == end_year:
            isLeapYear = calendar.isleap(start_year)
            return isLeapYear
        
        else:
            isLeapYear_arr = [calendar.isleap(year)
                              for year in range(start_year, end_year+1)]
            return isLeapYear_arr
    
