#----------------#
# Import modules #
#----------------#

from pathlib import Path
import sys

import calendar

import numpy as np
import pandas as pd
import scipy.signal as ssig
import xarray as xr

#-----------------------#
# Import custom modules #
#-----------------------#

# Import module that finds python tools' path #
home_PATH = Path.home()
sys.path.append(str(home_PATH))

import get_pytools_path
fixed_path = get_pytools_path.return_custom_path()

# Enumerate custom modules and their paths #
#------------------------------------------#

custom_mod1_path = f"{fixed_path}/arrays_and_lists"
custom_mod2_path = f"{fixed_path}/files_and_directories" 
custom_mod3_path = f"{fixed_path}/parameters_and_constants"
custom_mod4_path = f"{fixed_path}/pandas_data_frames" 
custom_mod5_path = f"{fixed_path}/strings"
custom_mod6_path = f"{fixed_path}/time_handling"
custom_mod7_path = f"{fixed_path}/weather_and_climate"
                  
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
import netcdf_handler
import string_handler
import time_formatters

#----------------------------------------------------#
# Define imported module(s)´ function call shortcuts #
#----------------------------------------------------#

basic_time_format_strs = global_parameters.basic_time_format_strs
month_number_dict = global_parameters.month_number_dict
season_timeFreq_dict = global_parameters.season_timeFreq_dict

find_date_key = data_frame_handler.find_date_key
insert_column_in_df = data_frame_handler.insert_column_in_df

find_substring_index= string_handler.find_substring_index

select_array_elements = array_handler.select_array_elements

find_time_dimension = netcdf_handler.find_time_dimension
get_file_dimensions = netcdf_handler.get_file_dimensions

time_format_tweaker = time_formatters.time_format_tweaker

#------------------#
# Define functions #
#------------------#

def periodic_statistics(obj, statistic, freq,
                        groupby_dates=False,
                        drop_date_idx_col=False,
                        season_months=None):
    
    """
    Calculates the basic statistics (NOT CLIMATOLOGIES)
    of the data for a certain time-frequency.
    
    Parameters
    ----------
    obj : pandas.DataFrame or xarray.Dataset
          or xarray.DataArray
          Object containing data.
    statistic : {"max", "min", "mean", "std", "sum"}
          String that defines which statistic to compute.
    freq : str
          String that identifies the frequency to which data is filtered.
          For example, "D" stands for daily data, "M" for monthly and so on.
          See https://pandas.pydata.org/docs/user_guide/timeseries.html#timeseries-offset-aliases
          for more details.
    groupby_dates : bool
          Available only if obj is xarray.Dataset 
          or xarray.DataArray.
          -----
          The standard procedure to calculate time-statistics
          is to group the dates according to a time-frequency 
          (which technically would be to make an 'upsampling').
          For example, if a data set which contains 30 years expressed
          in an hourly basis and daily mean is required to compute,
          then the result would be another data set with the equal 30 years
          but on a daily basis.
          -----
          However, xarray.Dataset or xarray.DataArray includes
          a resampling method that groups every time-frequency of all years.
          Taking the previous example, the result would be a data set with
          31 time steps, because it takes every day 1, day 2, etc. of all years.
          These are not climatological values but 'groupby' values, which
          is not that common to compute.
          This functions incorporates this option.
    drop_date_idx_col : bool
          Boolean used to whether drop the date columns in the new data frame.
          If it is False, then the columns of the dates will be kept.
          Otherwise, the dates themselves will be kept, but they will be
          treated as indexers, and not as a column.
          Defaults to False.
    season_months : list of integers
          List containing the month numbers to later refer to the time array,
          whatever the object is among the mentioned three types.
          Defaults to None.
    
    Returns
    -------
    obj : pd.DataFrame, xarray.Dataset 
          or xarray.DataArray.
          Object containing the frecuency-statistic data.
    """
    
    # Quality control of input parameters # 
    statistics = ["max", "min", "sum", "mean", "std"]
    
    if statistic not in statistics:
        raise ValueError("You have entered the wrong statistic, "\
                         f"options are {statistics}.")

    time_freqs = ["year", "season", "month", "day", "hour", "minute", "second"]
    freq_abbrs = ["Y", "SEAS", "M", "D", "H", "min", "S"]
    
    if isinstance(obj, pd.DataFrame):   
        date_key = find_date_key(obj)
        
        if freq not in freq_abbrs and season_months is None:
            raise ValueError("Wrong time-frequency.\n"\
                             f"Options are {freq_abbrs}.")
                
        elif freq == freq_abbrs[1] and season_months is None:
            raise ValueError("You must specify the season months in a list. "\
                             "For example: [12,1,2].")
                
        elif freq == freq_abbrs[1] and season_months is not None:
            if len(season_months) != 3:
                raise ValueError("Season length must strictly be of 3 months.")
                
            freq = season_timeFreq_dict[season_months[-1]]
        
        grouper = "pd.Grouper(key=date_key, freq=freq)"
        df_groupby = f"obj.groupby({grouper})"
        
        df_stat\
        = eval(f"{df_groupby}.{statistic}()"
               f".reset_index(drop={drop_date_idx_col})")
            
        return df_stat
    
        
    elif isinstance(obj, xr.Dataset)\
    or isinstance(obj, xr.DataArray): 
        
        date_key = find_time_dimension(obj)
        
        if groupby_dates:
            
            if freq not in time_freqs and season_months is None:
                raise ValueError("Wrong time-frequency.\n"\
                                 f"Options are {time_freqs}.")
            
            elif freq == time_freqs[1] and season_months is None:
                raise ValueError("You must specify the season months in a list. "\
                                 "For example: [12,1,2].")
                    
            elif freq == time_freqs[1] and season_months is not None:
                if len(season_months) != 3:
                    raise ValueError("Season length must strictly be of 3 months.")
                    
                freq = season_timeFreq_dict[season_months[-1]]
            
            grouper = f"obj.{date_key}.dt.{freq}"
            obj_groupby = f"obj.groupby({grouper})"
            
        else:
            if freq not in freq_abbrs and season_months is None:
                raise ValueError("Wrong time-frequency.\n"\
                                 f"Options are {freq_abbrs}.")
            
            elif freq == freq_abbrs[1] and season_months is None:
                raise ValueError("You must specify the season months in a list. "\
                                 "For example: [12,1,2].")
                    
            elif freq == freq_abbrs[1] and season_months is not None:
                if len(season_months) != 3:
                    raise ValueError("Season length must strictly be of 3 months.")
                    
                freq = season_timeFreq_dict[season_months[-1]]
            
            obj_groupby = f"obj.resample({date_key}='{freq}')"
            
            
        obj_stat = eval(f"{obj_groupby}.{statistic}()")
        return obj_stat
            
    else:
        raise ValueError("Cannot operate with this data type.")
  
  
def climat_periodic_statistics(obj,
                               statistic,
                               time_freq,
                               keep_std_dates=False, 
                               drop_date_idx_col=False,
                               season_months=None):

    """
    Function that calculates climatologic statistics for a time-frequency.
    
    Parameters
    ----------
    obj : pandas.DataFrame, xarray.Dataset 
          or xarray.DataArray.
    statistic : {"max", "min", "mean", "std", "sum"}
          String that defines which statistic to compute.
    time_freq : str
          String that identifies the frequency to which data is filtered.
    keep_std_dates : bool
          If True, standard YMD (HMS) date format is kept for all climatologics
          except for yearly climatologics.
          Otherwise dates are shown as hour, day, or month indexes,
          and season achronyms if "seasonal" is selected as the time frequency.
          Default value is False.
    drop_date_idx_col : bool
          Affects only if the passed object is a pandas data frame.
          Boolean used to whether drop the date columns in the new data frame.
          If it is False, then the columns of the dates will be kept.
          Otherwise, the dates themselves will be kept, but they will be
          treated as indexers, and not as a column.
          Defaults to False.
    season_months : list of integers
          List containing the month numbers to later refer to the time array,
          whatever the object is among the mentioned three types.
          Defaults to None.
    
    Returns
    -------
    obj_climat : pandas.DataFrame, xarray.Dataset 
                  or xarray.DataArray.
                  Climatological average of the data.
    
    Notes
    -----
    For pandas data frames, since it is an 2D object,
    it is interpreted that data holds for a specific geographical point.
    """
    
    # Quality control of input parameters # 
    time_freqs = ["yearly", "seasonal", "monthly", "daily", "hourly"]
    freq_abbrs = ["Y", "S", "M", "D", "H"]
    
    tf_idx = find_substring_index(time_freqs, time_freq)
    
    if tf_idx == -1:
        tf_idx = find_substring_index(freq_abbrs, time_freq)
        time_freq = time_freqs[tf_idx]
        freq_abbr = freq_abbrs[tf_idx]
        
        if tf_idx == -1:
            raise ValueError(f"Wrong time-frequency. Options are {time_freqs}.")
    else:
        freq_abbr = freq_abbrs[tf_idx]
    
    # Identify the time dimension #
    #-----------------------------#
    
    if isinstance(obj, pd.DataFrame):
        date_key = find_date_key(obj)
        
    elif isinstance(obj, xr.Dataset)\
    or isinstance(obj, xr.DataArray):
        date_key = find_time_dimension(obj)               
    
    # Calculate statistical climatologies #
    #-------------------------------------#

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

    if isinstance(obj, pd.DataFrame):
        
        # Define the climatologic statistical data frame #
        ncols_obj = len(obj.columns)
        climat_obj_cols = [date_key] + [obj.columns[i]+"_climat" 
                                        for i in range(1, ncols_obj)]
                
        if time_freq == "hourly":  
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
                
            if keep_std_dates:
                climat_dates = pd.date_range(f"{latest_year}-01-01 0:00",
                                             f"{latest_year}-12-31 23:00",
                                             freq=freq_abbr)
            else:    
                lcv = len(climat_vals)
                climat_dates = np.arange(lcv)
                climat_obj_cols[0] = "hour_of_year"
            
            
        elif time_freq == "daily":   
            climat_vals\
            = [np.float64(eval("obj[(obj[date_key].dt.month==m)"\
                                    "&(obj[date_key].dt.day==d)]."\
                               f"iloc[:,1:].{statistic}()"))
               
               for m in months
               for d in days
               
               if len(obj[(obj[date_key].dt.month==m)
                          &(obj[date_key].dt.day==d)].iloc[:,1:]) > 0]
                
            if keep_std_dates:
                climat_dates = pd.date_range(f"{latest_year}-01-01 0:00",
                                             f"{latest_year}-12-31 23:00",
                                             freq=freq_abbr)
            else:    
                lcv = len(climat_vals)
                climat_dates = np.arange(1,lcv+1)
                climat_obj_cols[0] = "day_of_year"
                
                
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
            
            if season_months is None:
                raise ValueError("You must specify the season months in a list. "\
                                 "For example: [12,1,2]")
                    
            if keep_std_dates:
                
                # hobetu ondokoa #
                climat_dates = [obj[obj[date_key].dt.month==season_months[-1]].
                                iloc[-1][date_key].strftime(daytime_fmt_str)]
            else:
                climat_dates = "".join([month_number_dict[m] for m in season_months]).split()
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
        
        obj_climat.iloc[:, 0] = time_format_tweaker(obj_climat.iloc[:, 0],
                                                    to_pandas_datetime="pand")        
        
    elif isinstance(obj, xr.Dataset)\
    or isinstance(obj, xr.DataArray):
          
        if time_freq == "hourly":
            
            # Define the time array #
            """Follow CDO's climatologic time array pattern,
            it is a model hourly time array.
            """

            # Define the hourly climatology pattern #
            obj_climat_nonstd_times = obj['time.hour']/24 + obj['time.dayofyear']        
            
            # Compute the hourly climatology #
            obj_climat\
            = eval(f"obj.groupby(obj_climat_nonstd_times).{statistic}(dim=date_key)")
            
            
        elif time_freq == "daily":
            obj_climat\
            = eval(f"obj.groupby(obj[date_key].dt.dayofyear).{statistic}(dim=date_key)")
            
            
        elif time_freq == "monthly":
            obj_climat\
            = eval(f"obj.groupby(obj[date_key].dt.month).{statistic}(dim=date_key)")
            
            
        elif time_freq == "seasonal":
            if season_months is None:
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
            occ_time_name_temp = find_time_dimension(obj_climat)

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
                
            # 'time' dimension renaming and its assignment #
            try:
                # Rename the analogous dimension of 'time' on dimension list #
                obj_climat\
                = obj_climat.rename_dims({occ_time_name_temp : occ_time_name})
                   
            except:
                # Rename the analogous dimension name of 'time' to standard #
                obj_climat\
                = obj_climat.rename({occ_time_name_temp : occ_time_name})
                
            try:
                # Rename the analogous dimension of 'time' on dimension list #
                obj_climat\
                = obj_climat.swap_dims({occ_time_name_temp : occ_time_name})
                
            except:
                try:
                    # Rename the analogous dimension name of 'time' to standard #
                    obj_climat\
                    = obj_climat.swap_dims({occ_time_name_temp : occ_time_name})
                    
                except:
                    pass   
                    
        elif time_freq == time_freqs[1]:
            
            if keep_std_dates:
                        
                seas_end_monthDay\
                = calendar.monthcalendar(latest_year, season_months[-1])[-1][-1]
                climat_dates\
                = pd.Timestamp(latest_year, season_months[-1], seas_end_monthDay)
                
                occ_time_name = date_key
                
            else:
                occ_time_name = time_freq[:-2]
                climat_dates = "".join([month_number_dict[m] for m in season_months])
                    
        # Update the time array #
        obj_climat = obj_climat.assign_coords({occ_time_name : climat_dates})
            
    return obj_climat


def calculate_and_apply_deltas(observed_series,
                               reanalysis_series,
                               time_freq,
                               delta_type="absolute",
                               statistic="mean",
                               preference_over="observed",
                               keep_std_dates=True, 
                               drop_date_idx_col=False,
                               season_months=None):

    """
    Function that calculates simple deltas between two objects
    and then applies to any of them.
    
    For that, it firstly calculates the given time-frequency climatologies
    for both objects using 'climat_periodic_statistics' function,
    and then performs the delta calculation, 
    depending on the math operator chosen:
      1. Absolute delta: subtraction between both objects
      2. Relative delta: division between both objects
    
    Once calculated, delta values are climatologically applied to the chosen
    object, by addition if the deltas are absolute or multiplication if they
    are relative.
    
    Parameters
    ----------
    observed_series : pandas.DataFrame, xarray.Dataset 
                      or xarray.DataArray.
    reanalysis_series : pandas.DataFrame, xarray.Dataset 
                        or xarray.DataArray.
          This object can be that extracted from a reanalysis,
          CORDEX projections or similar.
    time_freq : str
          String that identifies the frequency to which data is filtered.
    delta_type : {"absolute", "relative"}
    statistic : {"max", "min", "mean", "std", "sum"}
          String that defines which statistic to compute.
          Default is "mean" so that climatologic means are calculated.
    preference_over : {"observed", "reanalysis"}
          If "observed", then the observed series will be treated as the 'truth'
          and the reanalysis will be delta-corrected.
          Otherwise, though it is not common, the reanalysis will be treated
          as the truth and observations will be delta-corrected.
          Defaults to give preference to the observed series.
    keep_std_dates : bool
          If True, standard YMD (HMS) date format is kept for all climatologics
          except for yearly climatologics.
          Otherwise dates are shown as hour, day, or month indexes,
          and season achronyms if "seasonal" is selected as the time frequency.
          Default value is False.
    drop_date_idx_col : bool
          Affects only if the passed object is a pandas data frame.
          Boolean used to whether drop the date columns in the new data frame.
          If it is False, then the columns of the dates will be kept.
          Otherwise, the dates themselves will be kept, but they will be
          treated as indexers, and not as a column.
          Defaults to True in order to return date-time incorporated series.
    season_months : list of integers
          List containing the month numbers to later refer to the time array,
          whatever the object is among the mentioned three types.
          Defaults to None.
    
    Returns
    -------
    obj_climat : pandas.DataFrame, xarray.Dataset 
                  or xarray.DataArray.
                  Climatological average of the data.
    
    Notes
    -----
    For pandas data frames, since it is an 2D object,
    it is interpreted that data holds for a specific geographical point.
    """
    
    # Quality control of input parameters # 
    delta_types = ["absolute", "relative"]
    if delta_type not in delta_types:
        raise ValueError(f"Wrong delta type. Options are {delta_types}")
        
    preferences_over = ["observed", "reanalysis"]
    if delta_type not in delta_types:
        raise ValueError(f"Wrong preference type. Options are {preferences_over}")
    
    # Identify the time dimension #
    #-----------------------------#
    
    if isinstance(observed_series, pd.DataFrame) \
    and isinstance(reanalysis_series, pd.DataFrame):
        
        date_key = find_date_key(observed_series)
        date_key_rean = find_date_key(observed_series)

        if date_key != date_key_rean:
            reanalysis_series.columns = [date_key] + reanalysis_series.columns[1:]

    elif (isinstance(observed_series, xr.Dataset) \
        and isinstance(reanalysis_series, xr.Dataset)) \
    or (isinstance(observed_series, xr.DataArray) \
        and isinstance(reanalysis_series, xr.DataArray)):
        
        date_key = find_time_dimension(observed_series)
        date_key_rean = find_time_dimension(observed_series)
        
        if date_key != date_key_rean:
            
            try:
                
                # Rename the analogous dimension of 'time' on dimension list #
                reanalysis_series\
                = reanalysis_series.rename_dims({date_key_rean : date_key})
                   
                # Rename the analogous dimension name of 'time' to standard #
                reanalysis_series\
                = reanalysis_series.rename({date_key_rean : date_key})
                
            except:
                
                # Rename the analogous dimension of 'time' on dimension list #
                reanalysis_series\
                = reanalysis_series.swap_dims({date_key_rean : date_key})
                   
                # Rename the analogous dimension name of 'time' to standard #
                reanalysis_series\
                = reanalysis_series.swap_dims({date_key_rean : date_key})
    
    # Calculate statistical climatologies #
    #------------------------------------#
    
    print(delta_appliance_panel.format("Calculating observed climatologies...",
                                       time_freq,
                                       "N/P",
                                       "N/P",
                                       "N/P"))
    
    obs_climat = climat_periodic_statistics(observed_series, 
                                            statistic, 
                                            time_freq,
                                            keep_std_dates,
                                            drop_date_idx_col,
                                            season_months)
    
    print(delta_appliance_panel.format("Calculating reanalysis climatologies...",
                                       time_freq,
                                       "N/P",
                                       "N/P",
                                       "N/P"))
    
    rean_climat = climat_periodic_statistics(reanalysis_series, 
                                             statistic, 
                                             time_freq,
                                             keep_std_dates,
                                             drop_date_idx_col,
                                             season_months)
    
    # Calculate deltas #
    #------------------#

    if isinstance(observed_series, pd.DataFrame) \
    and isinstance(reanalysis_series, pd.DataFrame):
        
        if preference_over == "observed":
            delta_cols = observed_series.columns[1:]
            
            if delta_type == "absolute":
                delta_arr = rean_climat.iloc[:, 1:].values - obs_climat.iloc[:, 1:].values
            else:
                delta_arr = rean_climat.iloc[:, 1:].values / obs_climat.iloc[:, 1:].values
            
        elif preference_over == "reanalysis":
            delta_cols = reanalysis_series.columns[1:]
            
            if delta_type == "absolute":
                delta_arr = obs_climat.iloc[:, 1:].values - rean_climat.iloc[:, 1:].values
            else:
                delta_arr = obs_climat.iloc[:, 1:].values / rean_climat.iloc[:, 1:].values
            
        delta_obj = pd.concat([obs_climat[date_key],
                               pd.DataFrame(delta_arr, columns=delta_cols)],
                              axis=1)
        
    
    elif (isinstance(observed_series, xr.Dataset) \
        and isinstance(reanalysis_series, xr.Dataset)) \
    or (isinstance(observed_series, xr.DataArray) \
        and isinstance(reanalysis_series, xr.DataArray)):
            
        if preference_over == "observed":
            
            if delta_type == "absolute":
                delta_obj = rean_climat - obs_climat
            else:
                delta_obj = rean_climat / obs_climat
            
        elif preference_over == "reanalysis":            
            if delta_type == "absolute":
                delta_obj = obs_climat - rean_climat
            else:
                delta_obj = obs_climat / rean_climat
            
    # Apply the deltas over the chosen series # 
    #-----------------------------------------#
    
    months_delta = np.unique(delta_obj[date_key].dt.month)
    days_delta = np.unique(delta_obj[date_key].dt.day)
    hours_delta = np.unique(delta_obj[date_key].dt.hour)
    
    if time_freq == "seasonal":
        freq_abbr = time_freq
        
    else:
        
        if isinstance(observed_series, pd.DataFrame) \
        and isinstance(reanalysis_series, pd.DataFrame):  
            
            freq_abbr = pd.infer_freq(obs_climat[date_key])
            
        elif (isinstance(observed_series, xr.Dataset) \
            and isinstance(reanalysis_series, xr.Dataset)) \
        or (isinstance(observed_series, xr.DataArray) \
            and isinstance(reanalysis_series, xr.DataArray)):
                
            freq_abbr = xr.infer_freq(obs_climat[date_key])
    
    if preference_over == "observed":
        obj_aux = reanalysis_series.copy()
    else:
        obj_aux = observed_series.copy()
    
    """Acronyms used in the following lines:
        
    obj2C === object (can either be a pandas data frame or a xarray data set)
              to be corrected
    objD === delta object
    """

    # Seasonal time-frequency #
    ###########################
    
    if time_freq == "seasonal":
        obj2C = obj_aux[obj_aux[date_key].dt.month.isin(season_months)]
        
        # Delta application #
        print(delta_appliance_panel.format(
            f"Applying deltas over the {preference_over} series...",
            freq_abbr,season_months,"all","all"))
        
        if isinstance(observed_series, pd.DataFrame) \
        and isinstance(reanalysis_series, pd.DataFrame):  
            
            if delta_type == "absolute":    
                obj_aux.loc[obj2C.index, delta_cols]\
                += delta_obj.loc[:, delta_cols].values
            else:
                obj_aux.loc[obj2C.index, delta_cols]\
                *= delta_obj.loc[:, delta_cols].values
                
        elif (isinstance(observed_series, xr.Dataset) \
            and isinstance(reanalysis_series, xr.Dataset)) \
        or (isinstance(observed_series, xr.DataArray) \
            and isinstance(reanalysis_series, xr.DataArray)):
                
            if delta_type == "absolute":
                obj_aux.loc[obj2C.time] += delta_obj.values
            else:
                obj_aux.loc[obj2C.time] *= delta_obj.values
             
    
    # Monthly time-frequency #
    ##########################
    
    elif time_freq == "monthly":
        
        for m in months_delta:            
            obj2C = obj_aux[obj_aux[date_key].dt.month==m]
            objD = delta_obj[delta_obj[date_key].dt.month==m]
            
            # Delta application #
            print(delta_appliance_panel.format(
                f"Applying deltas over the {preference_over} series...",
                freq_abbr,m,"all","all"))
            
            if isinstance(observed_series, pd.DataFrame) \
            and isinstance(reanalysis_series, pd.DataFrame):
            
                if delta_type == "absolute":
                    obj_aux.loc[obj2C.index, delta_cols]\
                    += objD.loc[:, delta_cols].values
                else:
                    obj_aux.loc[obj2C.index, delta_cols]\
                    *= objD.loc[:, delta_cols].values
                    
            elif (isinstance(observed_series, xr.Dataset) \
                and isinstance(reanalysis_series, xr.Dataset)) \
            or (isinstance(observed_series, xr.DataArray) \
                and isinstance(reanalysis_series, xr.DataArray)):
                    
                if delta_type == "absolute":
                    obj_aux.loc[obj2C.time] += objD.values
                else:
                    obj_aux.loc[obj2C.time] *= objD.values
                
            
    # Daily time-frequency #
    ########################
        
    elif time_freq == "daily":
        
        for m in months_delta: 
            for d in days_delta:
                    
                obj2C = obj_aux[(obj_aux[date_key].dt.month==m)&
                                (obj_aux[date_key].dt.day==d)]
                
                objD = delta_obj[(delta_obj[date_key].dt.month==m)&
                                 (delta_obj[date_key].dt.day==d)]
                
                # Delta application #
                if len(obj2C) > 0 and len(objD) > 0:
                    
                    print(delta_appliance_panel.format(
                        f"Applying deltas over the {preference_over} series...",
                        freq_abbr,m,d,"all"))
                    
                    if isinstance(observed_series, pd.DataFrame) \
                    and isinstance(reanalysis_series, pd.DataFrame):
                    
                        if delta_type == "absolute":
                            obj_aux.loc[obj2C.index, delta_cols] \
                            += objD.loc[:, delta_cols].values
                        
                        else:
                            obj_aux.loc[obj2C.index, delta_cols] \
                            *= objD.loc[:, delta_cols].values
                            
                    elif (isinstance(observed_series, xr.Dataset) \
                        and isinstance(reanalysis_series, xr.Dataset)) \
                    or (isinstance(observed_series, xr.DataArray) \
                        and isinstance(reanalysis_series, xr.DataArray)):
                            
                        if delta_type == "absolute":
                            obj_aux.loc[obj2C.time] += objD.values
                        else:
                            obj_aux.loc[obj2C.time] *= objD.values
                    
                else:
                    pass
                       
    # Hourly time-frequency #
    #########################
    
    elif time_freq == "hourly":
            
        for m in months_delta:
            for d in days_delta:
                for h in hours_delta:
                    
                    obj2C = obj_aux[(obj_aux[date_key].dt.month==m)&
                                    (obj_aux[date_key].dt.day==d)&
                                    (obj_aux[date_key].dt.hour==h)]
                   
                    objD = delta_obj[(delta_obj[date_key].dt.month==m)&
                                     (delta_obj[date_key].dt.day==d)&
                                     (delta_obj[date_key].dt.hour==h)]
                   
                    # Delta application #
                    if len(obj2C) > 0 and len(objD) > 0:
                        
                        print(delta_appliance_panel.format(
                            f"Applying deltas over the {preference_over} series...",
                            freq_abbr,m,d,h))
                        
                        if isinstance(observed_series, pd.DataFrame) \
                        and isinstance(reanalysis_series, pd.DataFrame):
                        
                            if delta_type == "absolute":
                                obj_aux.loc[obj2C.index, delta_cols] \
                                += objD.loc[:, delta_cols].values
                            else:
                                obj_aux.loc[obj2C.index, delta_cols] \
                                *= objD.loc[:, delta_cols].values
                                
                        elif (isinstance(observed_series, xr.Dataset) \
                            and isinstance(reanalysis_series, xr.Dataset)) \
                        or (isinstance(observed_series, xr.DataArray) \
                            and isinstance(reanalysis_series, xr.DataArray)):
                            
                            if delta_type == "absolute":
                                obj_aux.loc[obj2C.time] += objD.values
                            else:
                                obj_aux.loc[obj2C.time] *= objD.values
                   
                    else:
                        pass
                   
    delta_corrected_obj = obj_aux.copy()    
    return delta_corrected_obj


def windowSum(x, N):

    """
    Function that computes the sum of the elements
    of a (time, lat, lon) array, in a sliding window, i.e. the moving sum.
    
    Parameters
    ----------
    x : numpy.ndarray
          Array containing data.
    N : int
          Window size.
    
    Returns
    -------
    sum_window : numpy.ndarray
          The sum of the elements.
    
    Notes
    -----
    Numpy's 'convolve' function does not work for n > 1 dimensional arrays.
    In such cases, scipy's 'convolve' function does the trick.
    """
    
    shape = x.shape
    dims = len(shape)
    
    if dims == 1:
        try:
            sum_window = np.convolve(x,
                                     np.ones(N, np.int64),
                                     mode="valid")
            
        except:
            sum_window = np.convolve(x,
                                     np.ones(N, np.float64),
                                     mode="valid")

    elif dims > 1:   
        number_of_ones = np.append(N, np.repeat(1, dims-1))
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
    
    """
    Returns the moving average of an array, independently of its dimension.
    For that, firstly uses the moving sum function and divides the result
    by the window size, N.
    
    Parameters
    ----------
    x : numpy.ndarray
          Array containing data.
    N : int
          Window size.
    
    Returns
    -------
    moving_average : numpy.ndarray
          The moving average of the array.
    """
    
    moving_average = windowSum(x, N) / N
    
    return moving_average
    
#------------------#
# Local parameters #
#------------------#

delta_appliance_panel = """{}
Time frequency : {}
Month = {}
Day = {}
Hour = {}
"""

daytime_fmt_str = basic_time_format_strs["D"]
