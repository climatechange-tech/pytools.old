#----------------#
# Import modules #
#----------------#

import cftime as cft
import datetime

import importlib
from pathlib import Path

import numpy as np
import pandas as pd

#---------------------------#
# Get the fixed directories #
#---------------------------#

cwd = Path.cwd()
main_path = Path("/".join(cwd.parts[:3])[1:]).glob("*/*")

# All-code containing directory #
fixed_dirpath = str([path
                     for path in main_path
                     if "pytools" in str(path).lower()][0])

#-----------------------#
# Import custom modules #
#-----------------------#

module_imp1 = "data_frame_handler.py"
module_imp1_path = f"{fixed_dirpath}/"\
                   f"pandas_data_frames/{module_imp1}"

spec1 = importlib.util.spec_from_file_location(module_imp1, module_imp1_path)
data_frame_handler = importlib.util.module_from_spec(spec1)
spec1.loader.exec_module(data_frame_handler)


module_imp2 = "string_handler.py"
module_imp2_path = f"{fixed_dirpath}/"\
                   f"strings/{module_imp2}"

spec2 = importlib.util.spec_from_file_location(module_imp2, module_imp2_path)
string_handler = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(string_handler)


module_imp3 = "array_handler.py"
module_imp3_path = f"{fixed_dirpath}/"\
                   f"arrays_and_lists/{module_imp3}"

spec3 = importlib.util.spec_from_file_location(module_imp3, module_imp3_path)
array_handler = importlib.util.module_from_spec(spec3)
spec3.loader.exec_module(array_handler)


module_imp4 = "netcdf_handler.py"
module_imp4_path = f"{fixed_dirpath}/"\
                   f"weather_and_climate/{module_imp4}"

spec4 = importlib.util.spec_from_file_location(module_imp4, module_imp4_path)
netcdf_handler = importlib.util.module_from_spec(spec4)
spec4.loader.exec_module(netcdf_handler)


module_imp5 = "global_parameters.py"
module_imp5_path = f"{fixed_dirpath}/"\
                   f"global_parameters/{module_imp5}"

spec5 = importlib.util.spec_from_file_location(module_imp5, module_imp5_path)
global_parameters = importlib.util.module_from_spec(spec5)
spec5.loader.exec_module(global_parameters)

#----------------------------------------------------#
# Define imported module(s)´ function call shortcuts #
#----------------------------------------------------#

basic_time_format_strs = global_parameters.basic_time_format_strs

find_date_key = data_frame_handler.find_date_key
insert_column_in_df = data_frame_handler.insert_column_in_df
save2csv = data_frame_handler.save2csv
save2excel = data_frame_handler.save2excel
insert_row_in_df = data_frame_handler.insert_row_in_df

find_substring_index= string_handler.find_substring_index
join_file_path_specs = string_handler.join_file_path_specs

count_unique_type_objects = array_handler.count_unique_type_objects
select_array_elements = array_handler.select_array_elements

find_time_dimension = netcdf_handler.find_time_dimension
get_file_dimensions = netcdf_handler.get_file_dimensions

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
    # gives the date time format using pd.to_datetime formatter.
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
        
    if cftime_check:            
        time_array_reformatted\
        = pd.to_datetime([cft.datetime.strftime(time_el, basic_time_format_strs["H"])
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
    # time_df : pd.core.series.Series
    #       Pandas series containing the date-times to be checked.
    #
    # Returns
    # -------
    # time_df : pd.core.series.Series
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


def standardize_calendar(obj,
                         file_path,
                         interpolation_method=None,
                         order=None,
                         save_as_new_obj=False, extension=None, 
                         separator=",",
                         save_index=False,
                         save_header=False):
    
    # Standardizes the given calendar of an object to gregorian, and
    # makes an interpolation ALONG ROWS (axis=0) to find the missing data.
    # It usually happens when modelled atmospheric or land data is considered,
    # when each model has its own calendar.
    # This funcion is useful when several model data is handled at once.
    # 
    # It only sticks to the limits of the time array present at the object;
    # further reconstructions is a task left for the user.
    # 
    # Parameters
    # ----------
    # obj : pd.core.frame.DataFrame or xarray.core.dataset.Dataset
    #       or list of pd.core.frame.DataFrame or xarray.core.dataset.Dataset.
    #       Object containing data. For each pd.core.frame.DataFrame, if present,
    #       the first column must be of type datetime64.
    # file_path : str or list of str
    #       String referring to the file name from which data object 
    #       has been extracted.
    # save_as_new_obj : bool
    #       If True and object is pd.core.frame.DataFrame, it is saved either
    #       as CSV or Excel containing one or more frames, the latter being
    #       desired by the user.
    # extension : {"csv", "xlsx", "nc"}
    #       The first two only work if object is pd.core.frame.DataFrame,
    #       while the third works if object is xarray.core.dataset.Dataset.
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
    # obj : pd.core.frame.DataFrame, xarray.core.dataset.Dataset 
    #       or xarray.core.dataarray.DataArray.
    #       Object containing the standardized calendar to gregorian.
    # 
    # Note
    # ----
    # There is no programatic way to store multiple sheets on a CSV file,
    # as can be donde with Excel files, because CSV is rough, old format
    # but mainly for data transport used.
    
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
        if isinstance(obj[0], pd.core.frame.DataFrame):
            
            for obj_enumerate, fp in zip(enumerate(obj), file_path):
                
                obj_num = obj_enumerate[0]
                obj = obj_enumerate[-1]
                
                # Get the date key and time frequency #
                time_col = find_date_key(obj)
                time_freq = check_time_index_frequency(obj.loc[:10,time_col])
                
                # Get the time array with possible missing datetimes #
                time_miss = obj.loc[:,time_col]
                time_miss_arr = time_reformatter(time_miss.values)
                ltm = len(time_miss)
               
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
                    for ft in enumerate(full_times):
                        
                        ft_num = ft[0]
                        ft_str = ft[-1]
                         
                        # lines_remaining = lft - (ft_num+1)
                        
                        if ft_str not in time_miss_arr:
                            index_before = ft_num - 1
                            
                            missing_datetime\
                            = obj.iloc[index_before, 0] + datetime.timedelta(days=1)
                            
                            values = np.append(missing_datetime, 
                                               np.repeat(np.nan, len(obj.columns[1:])))
                            
                            insert_row_in_df(obj, ft_num, values=values)
                
                    # Reorder the data frame indexes #
                    obj = obj.sort_index().reset_index(drop=True)
                    obj.iloc[:, 1:] = obj.iloc[:, 1:].astype('d')
                                    
                    # Perform the interpolation, if requested #
                    if interpolation_method is not None:
                        
                        if (interpolation_method == "polynomial"\
                        or interpolation_method == "spline")\
                        and order is None:
                            raise ValueError("Please specify and order for the "
                                             "interpolation method "
                                             f"{interpolation_method}")
                    
                        # Fill the missing data as a consequence of missing dates #
                        print("Filling the missing data as a consequence of missing dates...")
                        
                        obj.iloc[:, 1:]\
                        = obj.iloc[:, 1:].interpolate(method=interpolation_method,
                                                     order=order)
                        
                obj_stdCalendar.append(obj)
    
                # Save the object either as Excel or CSV document #
                if save_as_new_obj:
                    
                    file_path_parent, file_path_name\
                    = string_handler.file_path_specs(fp, "_")[:-2]
                    
                    saving_file_name = join_file_path_specs(file_path_parent, 
                                                            file_path_name, 
                                                            None) + "stdCalendar" 
                    
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
                            frame_dict[excel_sheet_name] = obj.loc[:, [time_col, grid_col]]
                            
                            print("Writing and storing data into an excel document...")
                            save2excel(saving_file_name,
                                       frame_dict,
                                       save_index,
                                       save_header)
        
                    else:
                        raise ValueError("Wrong extension choice. "
                                         "Options for a Pandas data frame are {'csv', 'xlsx'}")
                        
                return obj_stdCalendar
            
        # TODO: develop the case for xarray.core.dataset.Dataset objects #
        # elif isinstance(obj[0], xr.core.dataset.Dataset)\
        # or isinstance(obj[0], xr.core.dataarray.DataArray):
        
#-----------------------------------------------#
# Define global parameters below every function #
#-----------------------------------------------#

"""Declare those global so as not to use them
repeatedly inside functions above.
"""

extensions = ["csv", "xlsx", "nc"]
