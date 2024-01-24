#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

from pathlib import Path
import sys

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
                  
# Add the module paths to the path variable #
#-------------------------------------------#

sys.path.append(custom_mod1_path)

# Perform whole or partial module importations #
#----------------------------------------------#

from string_handler import find_substring_index

#-------------------------#
# Define custom functions #
#-------------------------#

def operations_with_sets(array_of_sets1, 
                         array_of_sets2=None, 
                         obj_type="built-in",
                         operation="union"):

    arg_names = operations_with_sets.__code__.co_varnames
    operation_arg_pos = find_substring_index(arg_names, "operation")
    obj_type_arg_pos = find_substring_index(arg_names, "obj_type")
    
    operation_opt_array = list(operation_dict.keys())
    
    if operation not in operation_opt_array:
        raise ValueError(f"Wrong '{arg_names[operation_arg_pos]}' argument. "
                         f"Options are {operation_opt_array}.")
        
        
    if obj_type not in obj_types:
        raise ValueError(f"Wrong '{arg_names[obj_type_arg_pos]}' argument. "
                         f"Options are {obj_types}.")
        
    if obj_type == "built-in":
        if operation == operation_opt_array[-1]:
            from itertools import product    
            
        res_set = eval(operation_dict.get(operation))            
        return res_set
            
    elif obj_type == "sympy":
        
        # TODO: garatu 'sympy' motako multzoen kasua
        # from sympy import FiniteSet
        raise NotImplementedError("Please for now set argument "
                                  f"'{arg_names[obj_type_arg_pos]}' to "
                                  f"{obj_types[0]}.")

#--------------------------#        
# Parameters and constants #
#--------------------------#

obj_types = ["built-in", "sympy"]

operation_dict = {
    'union': "array_of_sets1.union(array_of_sets2)",
    'intersection': "array_of_sets1.intersection(array_of_sets2)",
    'difference': "array_of_sets1.difference(array_of_sets2)",
    'symmetric_difference': "array_of_sets1.symmetric_difference(array_of_sets2)",
    'cartesian_product': "set(product(array_of_sets1))"
}
