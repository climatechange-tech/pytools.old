#----------------#
# Import modules #
#----------------#

from pathlib import Path

import sys

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
substring_replacer = string_handler.substring_replacer

#------------------#
# Define functions #
#------------------#

def operations_with_sets(array_of_sets1, 
                         array_of_sets2=None, 
                         obj_type="built-in",
                         operation="union"):

    operation_opt_array = ["union", 
                           "intersection", 
                           "difference", 
                           "symmetric_difference", 
                           "cartesian_product"]
    
    obj_types = ["built-in", "sympy"]

    arg_names = operations_with_sets.__code__.co_varnames
    operation_arg_pos = find_substring_index(arg_names, "operation")
    obj_type_arg_pos = find_substring_index(arg_names, "obj_type")
    
    if operation not in operation_opt_array:
        raise ValueError(f"Wrong '{arg_names[operation_arg_pos]}' argument. "
                         f"Options are {operation_opt_array}.")
        
        
    if obj_type not in obj_types:
        raise ValueError(f"Wrong '{arg_names[obj_type_arg_pos]}' argument. "
                         f"Options are {obj_types}.")
        
    if obj_type == "built-in":
        if operation == "union":
            res_set = array_of_sets1.union(array_of_sets2)
            
        elif operation == "intersection":
            res_set = array_of_sets1.intersection(array_of_sets2)
        
        elif operation == "difference":
            res_set = array_of_sets1.difference(array_of_sets2)
        
        elif operation == "symmetric_difference":
            res_set = array_of_sets1.symmetric_difference(array_of_sets2)
           
        elif operation == "cartesian_product":
            from itertools import product
            res_set = set(product(array_of_sets1))
            
        return res_set
            
    elif obj_type == "sympy":
        
        # TODO: garatu 'sympy' motako multzoen kasua
        # from sympy import FiniteSet
        raise NotImplementedError("Please for now set argument "
                                  f"'{arg_names[obj_type_arg_pos]}' to "
                                  f"{obj_types[0]}.")
        
        
    
    
