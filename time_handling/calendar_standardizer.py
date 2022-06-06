#----------------#
# Import modules #
#----------------#

import datetime

import importlib
from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr

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


module_imp2 = "time_formatters.py"
module_imp2_path = f"{fixed_dirpath}/"\
                   f"time_handling/{module_imp2}"

spec2 = importlib.util.spec_from_file_location(module_imp2, module_imp2_path)
time_formatters = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(time_formatters)


module_imp3 = "string_handler.py"
module_imp3_path = f"{fixed_dirpath}/"\
                   f"strings/{module_imp3}"

spec3 = importlib.util.spec_from_file_location(module_imp3, module_imp3_path)
string_handler = importlib.util.module_from_spec(spec3)
spec3.loader.exec_module(string_handler)


module_imp4 = "array_handler.py"
module_imp4_path = f"{fixed_dirpath}/"\
                   f"arrays_and_lists/{module_imp4}"

spec4 = importlib.util.spec_from_file_location(module_imp4, module_imp4_path)
array_handler = importlib.util.module_from_spec(spec4)
spec4.loader.exec_module(array_handler)


module_imp5 = "netcdf_handler.py"
module_imp5_path = f"{fixed_dirpath}/"\
                   f"weather_and_climate/{module_imp5}"

spec5 = importlib.util.spec_from_file_location(module_imp5, module_imp5_path)
netcdf_handler = importlib.util.module_from_spec(spec5)
spec5.loader.exec_module(netcdf_handler)


#----------------------------------------------------#
# Define imported module(s)´ function call shortcuts #
#----------------------------------------------------#

time_reformatter = time_formatters.time_reformatter
check_time_index_frequency = time_formatters.check_time_index_frequency

find_date_key = data_frame_handler.find_date_key
insert_column_in_df = data_frame_handler.insert_column_in_df

find_substring_index= string_handler.find_substring_index

count_unique_type_objects = array_handler.count_unique_type_objects
select_array_elements = array_handler.select_array_elements

find_time_dimension = netcdf_handler.find_time_dimension
get_file_dimensions = netcdf_handler.get_file_dimensions

#------------------#
# Define functions #
#------------------#

def standardize_calendar(obj,
                         interpolation_method=None,
                         order=None,
                         save_as_new_obj=False, extension=None):
    
    # Standardizes the given calendar of an object to gregorian, and
    # makes an interpolation ALONG ROWS to find the missing data.
    # It usually happens when modelled atmospheric or land data is considered,
    # when each model has its own calendar.
    # This funcion is useful when several model data is handled at once.
    # 
    # It only sticks to the limits of the time array present at the object;
    # further reconstructions is a task left for the user.
    # 
    # Parameters
    # ----------
    # obj : pandas.core.frame.DataFrame or xarray.core.dataset.Dataset
    #       or list of pandas.core.frame.DataFrame or xarray.core.dataset.Dataset.
    #       Object containing data. For each pandas.core.frame.DataFrame, if present,
    #       the first column must be of type datetime64.
    # save_as_new_obj : bool
    #       If True and object is pandas.core.frame.DataFrame, it is saved either
    #       as CSV or Excel containing one or more frames, the latter being
    #       desired by the user.
    # extension : {"csv", "xlsx", "nc"}
    #       The first two only work if object is pandas.core.frame.DataFrame,
    #       while the third works if object is xarray.core.dataset.Dataset,
    # 
    # Returns
    # -------
    # obj : pandas.core.frame.DataFrame, xarray.core.dataset.Dataset 
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
        
    len_objects = len(obj)
        
    # Check whether all objects passed in a list are of the same type #
    unique_type_list, lutl = array_handler.count_unique_type_objects(obj)
    
    if lutl > 1:
        raise ValueError("Not every object in the list is of the same type.")
    else:
        main_type = unique_type_list[0]
    
    if isinstance(main_type, pd.core.frame.DataFrame):
        
        time_std_progress_table = """
        Data frames remaining: {}
        Lines to review remaining: {}
        """
        
        for df_enumerate in obj:
            
            df_num = df_enumerate[0]
            df = df_enumerate[-1]
            
            # Get the date key and time frequency #
            time_col = find_date_key(df)
            time_freq = check_time_index_frequency(df.loc[:10,time_col])
            
            # Get the time array with possible missing datetimes #
            time_miss = df.loc[:,time_col]
            time_miss_arr = time_reformatter(time_miss.values)
            ltm = len(time_miss)
           
            # Construct full time array to compare with the previous array #
            first_datetime = df.iloc[0, 0]
            last_datetime = df.iloc[-1, 0]
            
            full_times = pd.date_range(first_datetime,
                                       last_datetime, 
                                       freq=time_freq)
            lft = len(full_times)
            
            data_frames_remaining = len_objects - (df_num+1) 
            
            # Compare both time arrays, even if they have the same length #
            if ltm != lft:
                for ft in enumerate(full_times):
                    
                    ft_num = ft[0]
                    ft_str = ft[-1]
                     
                    lines_remaining = lft - (ft_num+1)
                    
                    print(time_std_progress_table.format(data_frames_remaining, 
                                                         lines_remaining))
                    
                    if ft_str not in time_miss_arr:
                        
                        index_between = ft_num - 0.5
                        index_before = ft_num - 1
                        
                        missing_datetime\
                        = df.iloc[index_before, 0] + datetime.timedelta(days=1)
                        
                        df.loc[index_between] = np.nan
                        df.loc[index_between, time_col] = missing_datetime
            
                # Reorder the data frame indexes #
                df = df.sort_index().reset_index(drop=True)
                df.iloc[:, 1:] = df.iloc[:, 1:].astype('d')
            
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
                    
                    df = df.iloc[:, 1:].interpolate(method=interpolation_method,
                                                    order=order)

    # TODO: develop the case for xarray.core.dataset.Dataset objects #
    # elif isinstance(main_type, xr.core.dataset.Dataset):