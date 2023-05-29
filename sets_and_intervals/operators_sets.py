#----------------#
# Import modules #
#----------------#

import inspect

#------------------#
# Define functions #
#------------------#

# TODO: GARATU AUKERAK

def operations_with_sets(array_of_sets, operation="union"):

    operation_opt_array = ["union", 
                           "intersection", 
                           "difference", 
                           "symmetric_difference", 
                           "cartesian_product"]

    arg_names = get_obj_specs.__code__.co_varnames
    operation_arg_pos = 
    obj2ch_arg_pos = find_substring_index(arg_names, "obj2")
    if operation not in operation_opt_array:
        raise ValueError(f"Wrong '{operator_arg}' argument. Options are {operation_opt_array}.")
