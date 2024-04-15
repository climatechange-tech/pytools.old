#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

import itertools as it
import more_itertools as mit

import numpy as np

#------------------#
# Define functions #
#------------------#

# Mathematical operations #
#-------------------------#

def count_consecutive(array, calculate_max_consec=False):
    
    """
    Function that counts:
      1 : consecutive numbers in an array or pandas series,
          also distinguishing them by blocks.
      2 : maximum consecutive number subset length
          starting from an array that already satisfies certain condition,
          i.e. boolean array.
    
    Example 1
    ---------
    random_list = [45, 46, 47, 48, 80, 81, 83, 87]
    
    As can be seen, the first four numbers are consecutive,
    it stops there and another two consecutive number sequence begins.
    
    The result is then the following array:
    consec_times_array = [4, 2]
    
    Example 2
    ---------
    bool_array = [False, False, True, True, True, True, True, False, True, True]
    consec_times_array = [5, 2]
    max_consec_num = 5
    """
    
    if not calculate_max_consec:
        
        consec_times_array_byGroups_lengths\
        = [len(list(group)) for group in mit.consecutive_groups(array)]
        
        if len(consec_times_array_byGroups_lengths) > 1:
            consec_times_array_byGroups_lengths_gt1\
            = [lng for lng in consec_times_array_byGroups_lengths if lng >1]
            return consec_times_array_byGroups_lengths_gt1
            
        elif len(consec_times_array_byGroups_lengths) == 1:
            return consec_times_array_byGroups_lengths
        
        else:
            return None
    
    else:
    
        bool_groups = [list(group) for _, group in it.groupby(array)]
        
        consec_times_array_byGroups_lengths_gt1\
        = [len(group) for group in bool_groups if group[0] and len(group)>1]
        
        if len(consec_times_array_byGroups_lengths_gt1) > 0:
            max_consec_num = np.max(consec_times_array_byGroups_lengths_gt1)
            return max_consec_num
        else:
            return None


def calc_all_unique_pairs(array_like, method="python-default"):
    
    """
    Function to calculate all possible pairs, irrespective of the order,
    in a list or 1D array.
    
    Example
    -------
    arr = [1,7,4]
    
    Having 3 items in the list, there are fact(3) = 6 combinations
    Manually, one can deduce the following ones:
    
    1-7, 1-4, 4-1, 7-1, 7-4, 4-7
    
    but since the order is unimportant, actual number of combos is
    fact(3)/2 = 3.
    In this case, pairs number 3, 4 and 6 can be ruled out, 
    remaining these combos:
        
    1-7, 1-4 and 4-7
    
    Programatically, this function is designed to store each possible
    pair in a tuple, conforming a list thereof, so for this case
    the output would be:
        
    [(1,7), (1,4), (4,7)]
    
    Calculations can either be performed using standard Python procedures,
    or with the built-in 'itertools' library.
    
    Parameters
    ----------
    array_like : array-like of numbers, i.e. list or np.ndarray thereof.    
          Input data. In both cases it will be converted to a NumPy array,
          and if the latter's dimension is N > 1, it will also be flattened.
         
          Programatically, all types of data are allowed to co-exist
          in the array, being these simple or complex, which in that case
          converting to a NumPy array would result in an 'object' data type array.
          However, with no other context, the pairing would be nonsensical.

          In order to give some meaning to the pairing, object-type arrays
          are not allowed, else TypeError is raised.
          Numbers can be of type integer, float, complex
          or a combination among them.
            
    method : {'python-default', 'itertools'}
          Method to be used. Using 'itertools' built-in library
          the execution time is slightly improved.
            
    Returns
    -------
    all_pair_combo_arr : list or array of tuples
          The resulting list or array (depending the method used) of tuples.    
    """
    
    # arameter correctness checkings #
    #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
    
    # Input array #
    array = np.array(array_like)
    data_type = array.dtype

    if data_type == 'O':       
        raise TypeError("All elements of the array must either be of type"
                        "'int', 'float', 'complex', 'str' or a combination among them.")
        
    else:
        dims = len(array.shape)
        if dims > 1:
            array = array.flatten()
    
    # Method #
    if method not in return_pairs_options:
        raise ValueError(f"Wrong method. Options are {return_pairs_options}")
    
    
    # Number pair computations #
    #-#-#-#-#-#-#-#-#-#-#-#-#-#-
    
    all_pair_combo_arr = eval(return_pairs_opt_dict.get(method))
    return all_pair_combo_arr
    

# Time arrays #
#-------------#
 
def decompose_24h_cumulative_data(array, zeros_dtype='d'):
    
    """
    Function that obtains the 1-hour time step cumulative data,
    subtracting to the next cumulative data, the previous cumulative value.
    It is only intended for 24-hour time step hourly data.
    
    The methodology, by its nature, gives negative values every 24 hours.
    Assuming that data follow a cumulative distribution
    and is definite positive, then those negative values
    are considered as spurious and they are substituted by
    arrays of zeroes.
    It suffices to encounter a single negative value
    along the n-1 dimensional array (for a time index) to set it to zero.
    
    Parameters
    ----------
    array : numpy.ndarray
          Multi-dimensional array which contains data,
          being the first index corresponding to 'time' dimension.
    zeros_dtype : str or numpy type (e.g. numpy.int, numpy.float64)
          Sets the precision of the array composed of zeroes.
    
    Returns
    -------
    hour_TS_array : numpy.ndarray
          Multi dimensional array containing
          1-hour time step cumulative data.
    """
    
    records = len(array)
    array_shape = array.shape
    
    unmet_case_values = np.zeros(array_shape, dtype=zeros_dtype)
    
    hour_TS_array\
    = np.array([array[t+1] - array[t]
                if np.all((res :=array[t+1] - array[t])\
                          [~np.isnan(res)] >= 0.
                          )
                else unmet_case_values
                for t in range(records-1)])
           
    hour_TS_array = np.append(hour_TS_array,
                              np.mean(hour_TS_array[-2:], axis=0)[np.newaxis,:],
                              axis=0)

#--------------------------#
# Parameters and constants #
#--------------------------#

# Pair-combo calculation function #
#---------------------------------#

# Method options #
return_pairs_method_list = ["python-default", "itertools-comb"]

# Switch-type operation dictionary #
return_pairs_opt_dict = {
    "python-default" : "[(i,j) for i_aux,i in enumerate(array_like) for j in array[i_aux+1:]]",
    "itertools-comb" : "list(it.combinations(array_like, 2))"
}

return_pairs_options = list(return_pairs_opt_dict.keys())
