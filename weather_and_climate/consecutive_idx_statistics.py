#----------------#
# Import modules #
#----------------#

import importlib
from pathlib import Path

import numpy as np

#---------------------------#
# Get the fixed directories #
#---------------------------#

cwd = Path.cwd()
main_path = Path("/".join(cwd.parts[:3])[1:]).glob("*/*")

# All-code containing directory #
fixed_path = str([path
                     for path in main_path
                     if "pytools" in str(path).lower()][0])

#-----------------------#
# Import custom modules #
#-----------------------#

module_imp1 = "array_numerical_operations.py"
custom_mod1_path = f"{fixed_path}/"\
                   f"arrays_and_lists/{module_imp1}"

spec1 = importlib.util.spec_from_file_location(module_imp1, custom_mod1_path)
array_numerical_operations = importlib.util.module_from_spec(spec1)
spec1.loader.exec_module(array_numerical_operations)

#----------------------------------------------------#
# Define imported module(s)´ function call shortcuts #
#----------------------------------------------------#

count_consecutive = array_numerical_operations.count_consecutive
decompose_24h_cumulative_data\
= array_numerical_operations.decompose_24h_cumulative_data

#------------------#
# Define functions #
#------------------#

def get_1hour_time_step_data(array, zero_threshold, zeros_dtype='d'):
    
    """
    Function that obtains the 1-hour time step cumulative data,
    subtracting to the next cumulative, the previous cumulative value.
    
    In many cases, data is expressed as 24-hour cumulative,
    where data is summed up for every 1 hour,
    but each value is added to that of the previous hour.
    This is usually the case of the radiation.
    
    The methodology, by its nature, still computes
    negative or too small unrealistic values,
    only at the edges of the time array,
    so BELOW this threshold those edges are set to zero.
    E.g. radiation, where at midnight the sun does not radiate.
    
    Parameters
    ----------
    array : numpy.ndarray
          Multi-dimensional array which contains data,
          being the first index corresponding to ´time´ dimension.
    zero_threshold: int or float:
          Defines the value BELOW which data values are set to zero.
    zeros_dtype : str or numpy type (e.g. numpy.int, numpy.float64)
          Sets the precision of the array composed of zeroes.
    
    Returns
    -------
    hour_TS_delEdges : numpy.ndarray
          Multi dimensional array containing
          1-hour time step cumulative data,
          with the problem of the edges solved.
    """
    
    records = len(array)
    array_shape = array.shape
    
    hour_TS_array = decompose_24h_cumulative_data(array)
    unmet_case_values = np.zeros(array_shape, dtype=zeros_dtype)
    
    hour_TS_delEdges\
    = np.array([hour_TS_array[t]
                if np.all(~np.isnan(hour_TS_array[t]) < zero_threshold)
                else unmet_case_values
                for t in range(records)])
    
    return hour_TS_delEdges


def count_consecutive_days_maxdata(
        array, max_threshold,
        min_consec_days=None,
        calculate_max_consecutive_days=False):
    
    """
    Function that counts the number of days in which the daily maximum
    value exceeds certain threshold.
    
    Parameters
    ----------
    array : numpy.ndarray or pandas.Series
          An array which contains the daily maximum value data.
    max_threshold : int
          Upper limit.
    min_consec_days : int
          Minimum consecutive days number. It is set to None by default.
          If it is set to None, then no minimum consecutive days will
          be considered, and the number of days above the threshold
          will simply be summed.
    calculate_max_consecutive_days : bool
          Returns the largest consecutive days subset
    
    Returns
    -------
    consec_num_days : int
          Total number of days in which the condition has been satisfied.
    max_consec_num_days : int
          Maximum number of consecutive days in which the condition has been satisfied.
    """
    
    above_thres_idx = array > max_threshold
    
    if min_consec_days is None and not calculate_max_consecutive_days:
        consec_num_days = np.count_nonzero(above_thres_idx)        
        return consec_num_days
    
    elif min_consec_days is None and calculate_max_consecutive_days:
        max_consec_num_days = count_consecutive(above_thres_idx, True)
        
        if max_consec_num_days:
            return max_consec_num_days
        else:
            return 0
    
    else:
        N = min_consec_days        
        block_consecutive_idx = np.flatnonzero(
                                np.convolve(above_thres_idx,
                                            np.ones(N, dtype=int),
                                            mode='valid')
                                >=N)
        
        consec_nums_on_consecutive_idx = count_consecutive(block_consecutive_idx)
        
        if consec_nums_on_consecutive_idx:    
            consec_num_days = int(len(consec_nums_on_consecutive_idx)
                                  * (N-1)
                                  + sum(consec_nums_on_consecutive_idx))
            return consec_num_days
        else:
            return 0
    
    
def count_consecutive_days_mindata(
        array, min_threshold,
        threshold_mode="below",
        min_consec_days=None,
        calculate_min_consecutive_days=False):
    
    """
    Function that counts the number of days in which the daily minimum
    value exceeds certain threshold.
    
    Parameters
    ----------
    array : numpy.ndarray or pandas.Series
          An array which contains the daily minimum value data.
    min_threshold : int
          Integer that defines an upper or lower limit of the minimum value.
    threshold_mode : {"below","above"}, optional
          Defines whether to select the data that lies
          above or below the threshold. Default value is "below".
    min_consec_days : int
          Minimum consecutive days number. It is set to None by default.
          If it is set to None, then no minimum consecutive days will
          be considered, and the number of days above the threshold
          will simply be summed.
    calculate_min_consecutive_days : bool
          Returns the largest consecutive days subset

    Returns
    -------
    consec_num_days : int
          Total number of days in which the condition has been satisfied.
    min_consec_num_days : int
          minimum number of consecutive days in which the condition has been satisfied.
    """
    
    if threshold_mode == "below":
        above_thres_idx = array < min_threshold
    
        if not min_consec_days and not calculate_min_consecutive_days:
            consec_num_days = np.count_nonzero(above_thres_idx)
            return consec_num_days
        
        elif not min_consec_days and calculate_min_consecutive_days:
            min_consec_num_days = count_consecutive(above_thres_idx, True)
            
            if min_consec_num_days:
                return min_consec_num_days
            else:
                return 0
        
        else:
            N = min_consec_days        
            block_consecutive_idx = np.flatnonzero(
                                    np.convolve(above_thres_idx,
                                                np.ones(N, dtype=int),
                                                mode='valid')
                                    <=N)
            
            consec_nums_on_consecutive_idx = count_consecutive(block_consecutive_idx)
            
            if consec_nums_on_consecutive_idx:
                consec_num_days = int(len(consec_nums_on_consecutive_idx)
                                      * (N-1)
                                      + sum(consec_nums_on_consecutive_idx))
                return consec_num_days
            else:
                return 0
            
    elif threshold_mode == "above" :
        above_thres_idx = array > min_threshold
    
        if not min_consec_days and not calculate_min_consecutive_days:
            consec_num_days = np.count_nonzero(above_thres_idx)
            return consec_num_days
        
        elif not min_consec_days and calculate_min_consecutive_days :
            min_consec_num_days = count_consecutive(above_thres_idx, True)
            
            if min_consec_num_days:
                return min_consec_num_days
            else:
                return 0
        
        else:
            N = min_consec_days        
            block_consecutive_idx = np.flatnonzero(
                                    np.convolve(above_thres_idx,
                                                np.ones(N, dtype=int),
                                                mode='valid')
                                    >=N)
            
            consec_nums_on_consecutive_idx = count_consecutive(block_consecutive_idx)
            
            if consec_nums_on_consecutive_idx:        
                consec_num_days = int(len(consec_nums_on_consecutive_idx)
                                      * (N-1)
                                      + sum(consec_nums_on_consecutive_idx))
                return consec_num_days
            else:
                return 0
        
        
    else:
        raise ValueError("You have entered the wrong threshold mode, "\
                         "options are {'below', 'above'}")
