#----------------#
# Import modules #
#----------------#

from pathlib import Path

import sys

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

custom_mod1_path = f"{fixed_dirpath}/strings"
                  
# Add the module paths to the path variable #
#-------------------------------------------#

sys.path.append(custom_mod1_path)

# Perform the module importations #
#---------------------------------#

import string_handler

#----------------------------------------------------#
# Define imported module(s)´ function call shortcuts #
#----------------------------------------------------#

find_substring_index = string_handler.find_substring_index

#------------------#
# Define functions #
#------------------#

def define_interval(left_limit, right_limit, method="pandas", closed="both"):
    
    # Quality control #
    #-----------------#
    
    # Main argument names and their position on the function's definition #    
    arg_names = define_interval.__code__.co_varnames
    
    method_arg_pos\
    = find_substring_index(arg_names, "method", find_whole_words=True)
    
    method_options = ["pandas", "intervaltree"]
    
    # Method argument choice #    
    if method not in method_options:
        raise ValueError(f"Wrong '{arg_names[method_arg_pos]}' option. "
                         f"Options are {method_options}.")
    
    
    if method == "pandas":
        itv = pd.Interval(left_limit, right_limit, closed=closed)
        
    # TODO: garatu 'intervaltree' metodoaren eragiketak
    # elif method == "intervaltree":
        
    return itv
    

def basic_interval_operator(interval_array,
                            obj_type="pandas",
                            operation="union", 
                            force_union=False):
    
    import piso
    piso.register_accessors()

    # TODO: diseinatu pd.arrays.IntervalArray motako matrizea,
    #       "interval_array" zerrenda edo numpy matrize bat izanik
    
    # Quality control #
    #-----------------#
    
    # Main argument names and their position on the function's definition #    
    arg_names = basic_interval_operator.__code__.co_varnames
    
    op_arg_pos = find_substring_index(arg_names, "operation", find_whole_words=True)
    obj_type_pos = find_substring_index(arg_names, "obj_type", find_whole_words=True)
    
    op_options = ["union", "difference", "intersection",
                  "symmetric_difference", "comparison"]
    
    obj_type_options = ["pandas", "intervaltree"]
    
    # Operation and object type argument choices #    
    if operation not in op_options:
        raise ValueError(f"Wrong '{arg_names[op_arg_pos]}' option. "
                         f"Options are {op_options}.")
        
    if obj_type not in obj_type_options:
        raise ValueError(f"Wrong '{arg_names[obj_type_pos]}' option. "
                         f"Options are {obj_type_options}.")
    
    
    
    # Ideia orokorra mantentzeko, laneko programa nagusitik hartutako zatia #
    
    # intervals = pd.arrays.IntervalArray(df_slice_bins,
    #                                     closed="left")
    
    # min_num_interval = intervals.min()
    # min_num_interval_left = min_num_interval.left
    
    # max_num_interval = intervals.max()
    # max_num_interval_right = max_num_interval.right
    
    # merged_bin = intervals.piso.union()[0]
    # merged_bin_left = merged_bin.left
    # merged_bin_right = merged_bin.right
    
    # if merged_bin_left != min_num_interval_left\
    #     or merged_bin_right != max_num_interval_right:
    #         merged_bin = pd.Interval(min_num_interval_left,
    #                                  max_num_interval_right,
    #                                  closed="left")
    
    """do sth"""

