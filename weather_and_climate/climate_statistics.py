#----------------#
# Import modules #
#----------------#

import importlib
from pathlib import Path

import calendar

import numpy as np
import pandas as pd
import scipy.signal as ssig
import xarray as xr

#---------------------------#
# Get the fixed directories #
#---------------------------#
# TODO: delta periodikoak cdo bitartez kalkulatu ezin edo
# bideraezina deneko kasutarako, pandas bitartez egiteko moldatu.

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

#----------------------------------------------------#
# Define imported module(s)´ function call shortcuts #
#----------------------------------------------------#

find_date_key = data_frame_handler.find_date_key
insert_column_in_df = data_frame_handler.insert_column_in_df

find_substring_index= string_handler.find_substring_index

select_array_elements = array_handler.select_array_elements

find_time_dimension = netcdf_handler.find_time_dimension

#------------------#
# Define functions #
#------------------#

def periodic_statistics(obj, statistic, freq, drop_date_idx_col):
    
    # Calculates the basic statistics (NOT CLIMATOLOGIES)
    # of the data for a certain time-frequency.
    # 
    # Parameters
    # ----------
    # obj : pd.core.frame.DataFrame or xarray.core.dataset.Dataset
    #       Object containing  data.
    # statistic : {"max", "min", "mean", "std", "sum"}
    #       String that defines which statistic to compute.
    # freq : str
    #       String that identifies the frequency to which data is filtered.
    #       For example, "D" stands for daily data, "M" for monthly and so on.
    #       See https://pandas.pydata.org/docs/user_guide/timeseries.html#timeseries-offset-aliases
    #       for more details.
    # drop_date_idx_col : bool
    #       Boolean used to whether drop the date columns in the new data frame.
    #       If it is False, then the columns of the dates will be kept.
    #       Otherwise, the dates themselves will be kept, but they will be
    #       treated as indexers, and not as a column.
    # 
    # Returns
    # -------
    # obj : pd.core.frame.DataFrame, xarray.core.dataset.Dataset 
    #       or xarray.core.dataarray.DataArray.
    #       Object containing the frecuency-statistic data.

    statistics = ["max", "min", "sum", "mean", "std"]
    
    freq_abbrs = ["year", "month", "day",
                  "hour", "minute", "second",
                  "microsecond", "nanosecond"]
    
    if statistic not in statistics:
        raise ValueError("You have entered the wrong statistic, "\
                         f"options are {statistics}.")

    if isinstance(obj, pd.core.frame.DataFrame):
        date_key = find_date_key(obj)
        
        if "date_key" in locals().keys():   
            grouper = "pd.Grouper(key=date_key, freq=freq)"
            df_groupby = f"obj.groupby({grouper})"
            
            df_stat\
            = eval(f"{df_groupby}.{statistic}()"
                   f".reset_index(drop={drop_date_idx_col})")
            return df_stat
        
        else:
            raise ValueError("No ´time´ or similar key found on data frame.")
            
    elif isinstance(obj, xr.core.dataset.Dataset)\
    or isinstance(obj, xr.core.dataarray.DataArray):        
        
        if freq not in freq_abbrs:
            raise ValueError("Wrong time-frequency.\n"\
                             f"Options are {freq_abbrs}.")
        
        date_key = [find_substring_index(list(obj.dims), kw)
                    for kw in ["tim", "dat"]][0]
        
        if date_key and date_key != -1: 
            grouper = f"obj.{date_key}.dt.{freq}"
            obj_groupby = f"obj.groupby({grouper})"
            
            obj_stat\
            = eval(f"{obj_groupby}.{statistic}()")
            return obj_stat
        
        else:
            raise ValueError("No ´time´ key or similar found on data frame.")
            
    else:
        raise ValueError("Cannot operate with this data type.")
  
  
def climat_periodic_statistics(obj,
                               statistic,
                               time_freq,
                               keep_std_dates=False, 
                               drop_date_idx_col=False,
                               season_months=None):

    # Function that calculates climatologic statistics for a time-frequency.
    # 
    # Parameters
    # ----------
    # obj : pandas.core.frame.DataFrame, xarray.core.dataset.Dataset 
    #       or xarray.core.dataarray.DataArray.
    # statistic : {"max", "min", "mean", "std", "sum"}
    #       String that defines which statistic to compute.
    # time_freq : str
    #       String that identifies the frequency to which data is filtered.
    # keep_std_dates : bool
    #       If True, standard YMD (HMS) date format is kept for all climatologics
    #       except for yearly climatologics.
    #       Otherwise dates are shown as hour, day, or month indexes,
    #       and season achronyms if "seasonal" is selected as the time frequency.
    #       Default value is False.
    # drop_date_idx_col : bool
    #       Affects only if the passed object is a pandas data frame.
    #       Boolean used to whether drop the date columns in the new data frame.
    #       If it is False, then the columns of the dates will be kept.
    #       Otherwise, the dates themselves will be kept, but they will be
    #       treated as indexers, and not as a column.
    #       Defaults to False.
    # season_months : list of integers
    #       List containing the month numbers to later refer to the time array,
    #       whatever the object is among the mentioned three types.
    #       Defaults to None.
    # 
    # Returns
    # -------
    # obj_climat : pandas.core.frame.DataFrame, xarray.core.dataset.Dataset 
    #              or xarray.core.dataarray.DataArray.
    #              Climatological average of the data.
    # 
    # Notes
    # -----
    # For pandas data frames, since it is an 2D object,
    # it is interpreted that data holds for a specific geographical point.
    
    time_freqs = ["yearly", "seasonal", "monthly", "daily", "hourly"]
    freq_abbrs = ["Y", "S", "M", "D", "H"]
    
    tf_idx = find_substring_index(time_freqs, time_freq)
    
    if tf_idx == -1:
        raise ValueError(f"Wrong time-frequency. Options are {time_freqs}.")
    else:
        freq_abbr = freq_abbrs[tf_idx]
    
        
    # Time dimension name identification #
    #------------------------------------#
    
    # Define time array identifier string #
    if isinstance(obj, pd.core.frame.DataFrame):
        date_key = find_date_key(obj)
        
    elif isinstance(obj, xr.core.dataset.Dataset)\
    or isinstance(obj, xr.core.dataarray.DataArray):
        date_key = find_time_dimension(obj)               
    
    # Climatological statistic calculation, depends on the type of the object #
    #-------------------------------------------------------------------------#
    
    # Get date array and parts of it #
    dates = obj[date_key]
    
    years = np.unique(dates.dt.year)        
    days = np.unique(dates.dt.day)
    months = np.unique(dates.dt.month)
    hours = np.unique(dates.dt.hour)
    
    # Check for the number of leap years #
    leapyear_bool_arr = [calendar.isleap(year) for year in years]
    llba = len(leapyear_bool_arr)
    
    if llba > 0:
        latest_year = years[leapyear_bool_arr][-1]
    else:
        latest_year = years[-1]

    if isinstance(obj, pd.core.frame.DataFrame):
        
        # Define the climatologic statistical data frame #
        ncols_obj = len(obj.columns)
        climat_obj_cols = [date_key] + [obj.columns[i]+"_climat" 
                                        for i in range(1, ncols_obj)]
                
        if time_freq == "hourly":            
            if keep_std_dates:
                climat_dates = pd.date_range(f"{latest_year}-01-01 0:00",
                                             f"{latest_year}-12-31 23:00",
                                             freq=freq_abbr)
            else:    
                lcd = len(climat_dates)
                climat_dates = np.arange(lcd)
                climat_obj_cols[0] = "hour_of_year"
            
            
            climat_vals\
            = [np.float64(eval("obj[(obj[date_key].dt.month==m)"\
                                   "&(obj[date_key].dt.day==d)"\
                                   "&(obj[date_key].dt.hour==h)]."\
                               f"iloc[:,1:].{statistic}()"))
               for m in months
               for d in days
               for h in hours
                       
               if len(obj[(obj[date_key].dt.month==m)
                          &(obj[date_key].dt.day==d)
                          &(obj[date_key].dt.hour==h)].iloc[:,1:]) > 0]
                
            
        elif time_freq == "daily":            
            if keep_std_dates:
                climat_dates = pd.date_range(f"{latest_year}-01-01 0:00",
                                             f"{latest_year}-12-31 23:00",
                                             freq=freq_abbr)
            else:    
                lcd = len(climat_dates)
                climat_dates = np.arange(1,lcd+1)
                climat_obj_cols[0] = "day_of_year"
                
            climat_vals\
            = [np.float64(eval("obj[(obj[date_key].dt.month==m)"\
                                    "&(obj[date_key].dt.day==d)]."\
                               f"iloc[:,1:].{statistic}()"))
               
               for m in months
               for d in days
               
               if len(obj[(obj[date_key].dt.month==m)
                          &(obj[date_key].dt.day==d)].iloc[:,1:]) > 0]
            
                
        elif time_freq == "monthly":            
            if keep_std_dates:
                climat_dates = pd.date_range(f"{latest_year}-01-01 0:00",
                                             f"{latest_year}-12-31 23:00",
                                             freq=freq_abbr)
                
            else:
                climat_dates = np.arange(1,13)
                climat_obj_cols[0] = "month_of_year"
            
            climat_vals = [np.float64(eval("obj[obj[date_key].dt.month==m]."\
                                            f"iloc[:,1:].{statistic}()"))
                            for m in months
                            if len(obj[obj[date_key].dt.month==m].iloc[:,1:]) > 0]
                
            
        elif time_freq == "seasonal":
            
            """Define a dictionary matching the month number 
            with the corresponding names first letter
            """
            mlnd = {1:"J",2:"F",3:"M",
                    4:"A",5:"M",6:"J",
                    7:"J",8:"A",9:"S",
                    10:"O",11:"N",12:"D"}
            
            if season_months is None:
                raise ValueError("You must specify the season months in a list. "\
                                 "For example: [12,1,2]")
                    
            if keep_std_dates:
                climat_dates = [obj[obj[date_key].dt.month==season_months[-1]].
                                iloc[-1][date_key].strftime("%Y-%m-%d")]
            else:
                climat_dates = "".join([mlnd[m] for m in season_months]).split()
                climat_obj_cols[0] = "season"
                
                    
            climat_vals\
            = [np.float64(eval("obj[obj[date_key].dt.month.isin(season_months)]."\
                               f"iloc[:,1:].{statistic}()"))]
                
            
        elif time_freq == "yearly":
            climat_df = periodic_statistics(obj, 
                                            statistic, 
                                            freq_abbr,
                                            drop_date_idx_col)
    
            climat_vals = [np.float64(eval(f"climat_df.iloc[:,1:].{statistic}()"))]
            climat_dates = [climat_df.iloc[-1,0]]
            
            
        # Check climatological value array's shape to later fit into the df #
        climat_vals = np.array(climat_vals)
        climat_vals_shape = climat_vals.shape
        lcvs = len(climat_vals_shape)
        
        if lcvs == 1:
            climat_vals = climat_vals[:, np.newaxis]    
        
        climat_dates = np.array(climat_dates, 'O')[:, np.newaxis]
        
        # Store climatological data into the data frame #
        climat_arr = np.append(climat_dates, climat_vals, axis=1)
        obj_climat = pd.DataFrame(climat_arr, columns=climat_obj_cols)
        
        
    elif isinstance(obj, xr.core.dataset.Dataset)\
    or isinstance(obj, xr.core.dataarray.DataArray):
          
        if time_freq == "hourly":
            
            # Define the time array #
            """Follow CDO's climatologic time array pattern,
            it is a model hourly time array"""
            
            climat_dates = pd.date_range(f"{latest_year}-1-1 0:00",
                                         f"{latest_year}-12-31 23:00",
                                         freq="H")
            lcd = len(climat_dates)
            
            # Define the hourly climatology pattern #
            obj_climat_nonstd_times = obj['time.hour']/24 + obj['time.dayofyear']        
            
            # Compute the hourly climatology #
            obj_climat\
            = eval(f"obj.groupby(obj_climat_nonstd_times).{statistic}(dim=date_key)")
            
            # if keep_std_dates:
                
            #     occ_time_name = date_key 
            #     climat_dates = climat_dates
                
            #     # Rename the analogous dimension of 'time' on dimension list #
            #     obj_climat_calc\
            #     = obj_climat_calc.rename_dims({occ_time_name_temp : occ_time_name})
                
            #     # Rename the analogous dimension name of 'time' to standard #
            #     obj_climat_calc\
            #     = obj_climat_calc.rename({occ_time_name_temp : occ_time_name})
                
            # else:
                
            #     occ_time_name = "hourofyear" 
            #     climat_dates = np.arange(lcd)
                
            #     # Rename the analogous dimension of 'time' on dimension list #
            #     obj_climat_calc\
            #     = obj_climat_calc.rename_dims({occ_time_name_temp : occ_time_name})
                
            #     # Rename the analogous dimension name of 'time' to standard #
            #     obj_climat_calc\
            #     = obj_climat_calc.rename({occ_time_name_temp : occ_time_name})
                
            
            
            
        elif time_freq == "daily":
            obj_climat\
            = eval(f"obj.groupby(obj[date_key].dt.dayofyear).{statistic}(dim=date_key)")
            
        elif time_freq == "monthly":
            obj_climat\
            = eval(f"obj.groupby(obj[date_key].dt.month).{statistic}(dim=date_key)")
            
        elif time_freq == "seasonal":
            if not season_months:
                raise ValueError("You must specify the season months in a list. "\
                                 "For example: [12,1,2]")
            
            obj_seas_sel = obj.sel({date_key: obj[date_key].dt.month.isin(season_months)})
            obj_climat = eval(f"obj_seas_sel.{statistic}(dim=date_key)")          
            
        elif time_freq == "yearly":
            obj_climat = eval(f"obj.{statistic}(dim=date_key)")
            
            
        # Choose the climatological time format #
        #---------------------------------------#
        
        if time_freq in time_freqs[2:]:
            
            # Get the analogous dimension of 'time', usually label 'group' #
            occ_dimlist = netcdf_handler.get_file_dimensions(obj_climat)
            occ_time_name_temp = occ_dimlist[-1]

            if keep_std_dates:                          
                climat_dates = pd.date_range(f"{latest_year}-1-1 0:00",
                                             f"{latest_year}-12-31 23:00",
                                             freq=freq_abbr)
                occ_time_name = date_key 
              
            else:
                climat_dates = obj_climat[occ_time_name_temp].values
                lcd = len(climat_dates)
                
                occ_time_name = occ_time_name_temp
                
                if time_freq in time_freqs[-2:]:
                    occ_time_name = time_freq[:-2] + "ofyear"    
                    climat_dates = np.arange(lcd) 
                    
            try:
                
                # Rename the analogous dimension of 'time' on dimension list #
                obj_climat\
                = obj_climat.rename_dims({occ_time_name_temp : occ_time_name})
                   
                # Rename the analogous dimension name of 'time' to standard #
                obj_climat\
                = obj_climat.rename({occ_time_name_temp : occ_time_name})
                
            except:
                
                # Rename the analogous dimension of 'time' on dimension list #
                obj_climat\
                = obj_climat.swap_dims({occ_time_name_temp : occ_time_name})
                   
                # Rename the analogous dimension name of 'time' to standard #
                obj_climat\
                = obj_climat.swap_dims({occ_time_name_temp : occ_time_name})
                
                    
            # Update the time array #
            obj_climat = obj_climat.assign_coords({occ_time_name : climat_dates})
            
    return obj_climat


def windowSum(x, N):

    # Function that computes the sum of the elements
    # of a (time, lat, lon) array, in a sliding window, i.e. the moving sum.
    # 
    # Parameters
    # ----------
    # x : numpy.ndarray
    #       Array containing data.
    # N : int
    #       Window size.
    # 
    # Returns
    # -------
    # sum_window : numpy.ndarray
    #       The sum of the elements.
    # 
    # Notes
    # -----
    # Numpy's 'convolve' function does not work for n > 1 dimensional arrays.
    # In such cases, scipy's 'convolve' function does the trick.
    
    shape = x.shape
    ls = len(shape)
    
    if ls == 1:
        try:
            sum_window = np.convolve(x,
                                     np.ones(N, np.int64),
                                     mode="valid")
            
        except:
            sum_window = np.convolve(x,
                                     np.ones(N, np.float64),
                                     mode="valid")

    elif ls > 1:   
        number_of_ones = np.append(N, np.repeat(1, ls-1))
        ones_size_tuple = tuple(number_of_ones)
             
        try:
            sum_window = ssig.convolve(x,
                                       np.ones(ones_size_tuple, np.int64),
                                       mode="same"
                                       )[1:]
        except:
            sum_window = ssig.convolve(x,
                                       np.ones(ones_size_tuple, np.float64),
                                       mode="same"
                                       )[1:]
            
    else:
        raise ValueError("Given array is an empty one!")
        
    return sum_window


def moving_average(x, N):
    
    # Returns the moving average of an array, independently of its dimension.
    # For that, firstly uses the moving sum function and divides the result
    # by the window size, N.
    # 
    # Parameters
    # ----------
    # x : numpy.ndarray
    #       Array containing data.
    # N : int
    #       Window size.
    # 
    # Returns
    # -------
    # moving_average : numpy.ndarray
    #       The moving average of the array.
    
    moving_average = windowSum(x, N) / N
    return moving_average