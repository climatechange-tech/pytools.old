#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

from pathlib import Path

import sys

import pandas as pd

#-----------------------#
# Import custom modules #
#-----------------------#

# Find the path of the Python toolbox #
home_PATH = Path.home()
sys.path.append(str(home_PATH))

import get_pytools_path
fixed_path = get_pytools_path.return_custom_path()

# Enumerate custom modules and their paths #
#------------------------------------------#

custom_mod1_path = f"{fixed_path}/strings"
                  
# Add the paths to the 'path' attribute of module 'sys' #
#-------------------------------------------------------#

sys.path.append(custom_mod1_path)

# Perform whole or partial module importations #
#----------------------------------------------#

import string_handler

#----------------------------------------------------#
# Define imported module(s)' function call shortcuts #
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
    
    method_arg_pos = find_substring_index(arg_names, "method")
    method_options = ["pandas", "intervaltree"]
    
    # Method argument choice #    
    if method not in method_options:
        raise ValueError(f"Wrong '{arg_names[method_arg_pos]}' option. "
                         f"Options are {method_options}.")
    
    if method == "pandas":
        import piso
        piso.register_accessors()
        itv = pd.Interval(left_limit, right_limit, closed=closed)
        
    elif method == "intervaltree":
        from intervaltree import Interval
        print(f"WARNING: method {method} does not include upper bound.")
        itv = Interval(left_limit, right_limit)
        
    return itv
    

def basic_interval_operator(interval_array,
                            obj_type="pandas",
                            closed="left",
                            operation="union", 
                            force_union=False):
    
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
        
    if obj_type == "pandas":
        import piso
        piso.register_accessors()
         
        itv_pdArray = pd.arrays.IntervalArray(interval_array,
                                              closed=closed)
        
        # TODO: garatu bost kasuak, denak web-orrialde ofizialetik
        
        if operation == "union":
            merged_bin = itv_pdArray.piso.union()[0]
            
            if not force_union:
                return merged_bin
               
            else:
                merged_bin_left = merged_bin.left
                merged_bin_right = merged_bin.right
                
                min_num_interval = itv_pdArray.min()
                min_num_interval_left = min_num_interval.left
                
                max_num_interval = itv_pdArray.max()
                max_num_interval_right = max_num_interval.right
                
                if merged_bin_left != min_num_interval_left\
                or merged_bin_right != max_num_interval_right:

                    merged_bin = define_interval(min_num_interval_left,
                                                 max_num_interval_right,
                                                 closed=closed)
                    
                    return merged_bin
                    
                else:
                    return merged_bin
                
        elif operation == "intersection":
            """do sth"""
            
        

    
    elif obj_type == "intervaltree":
        print(f"WARNING: method {obj_type} does not include upper bound.")
        
        from intervaltree import Interval, IntervalTree
        itv_ItvArray = IntervalTree.from_tuples(interval_array)
        
        # TODO: garatu bost kasuak, denak web-orrialde ofizialetik

