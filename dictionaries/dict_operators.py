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

custom_mod1_path = f"{fixed_path}/parameters_and_constants"

# Add the paths to the 'path' attribute of module 'sys' #
#-------------------------------------------------------#

sys.path.append(custom_mod1_path)

# Perform whole or partial module importations #
#----------------------------------------------#

from global_parameters import basic_four_rules

#-------------------------#
# Define custom functions #
#-------------------------#

# Mathematical operations #
#-------------------------#

def sum_dict_values(dict1, dict2):
    sum_dict = {key:
                dict1[key] + dict2[key]
                for key in dict1.keys() & dict2}
    return sum_dict
    
def subtr_dict_values(dict1, dict2):
    subtr_dict = {key:
                  dict1[key] - dict2[key]
                  for key in dict1.keys() & dict2}
    return subtr_dict

def mult_dict_values(dict1, dict2):
    mult_dict = {key:
                 dict1[key] * dict2[key]
                 for key in dict1.keys() & dict2}
    return mult_dict

def div_dict_values(dict1, dict2):
    div_dict = {key:
                dict1[key] / dict2[key]
                for key in dict1.keys() & dict2}
    return div_dict
    

def dict_value_basic_operator(dict1, dict2, 
                              basic_math_operator,
                              return_sorted_keys=False):

    """
    Performs the basic mathematical operations between two dictionaries,
    calling the specific function for the chosen mathematical operator.
    It is not necessary for both dictionaries' to be sorted
    (always referring to the keys) because the same key is referred to them.    
    
    Parameters
    ----------
    dict1 : dict
          First dictionary containing some values.
    dict2 : dict
          Second dictionary containing some values.
    basic_math_operator : {'+', '-', '*', '/'}
    return_sorted_keys : bool
          Determines whether to return the resulting dictionary with sorted keys.
          Defaults to False.
    
    Returns
    -------
    result_dict : dict
          Dictionary with common key's values operated according to the
          chosen mathematical operator.
          Depending on the value of 'return_sorted_keys', the dictionary's
          keys will be sorted.
    
    Note
    ----
    As aforementioned, this function uses the specific ones for the 
    chosen mathematical operators, which are defined to operate
    among common keys to both dictionaries.
    
    Then, defining two dictionaries with different lengths will not
    trigger an error as it is a Python's natively accepted operation,
    but it has to be taken into account to avoid misinterpretations.    
    """
    
    # Quality control #
    if basic_math_operator not in basic_four_rules:
        raise ValueError ("Wrong basic operator sign. Accepted operators are: "\
                          f"{basic_four_rules}.")
         
    accepted_operation_dict = {
        basic_four_rules[0] : sum_dict_values(dict1, dict2),
        basic_four_rules[1] : subtr_dict_values(dict1, dict2),
        basic_four_rules[2] : mult_dict_values(dict1, dict2),
        basic_four_rules[3] : div_dict_values(dict1, dict2)
        }
    
    result_dict = accepted_operation_dict.get(basic_math_operator)
    
    if return_sorted_keys: 
        result_dict = sort_dictionary_byKeys(result_dict)
        
    return result_dict


# Merge and sort operations #
#---------------------------#

def sort_dictionary_byKeys(dic):
    keys_sorted_list = sorted(dic)
    dic_sorted_byKeys = {key : dic[key]
                         for key in keys_sorted_list}
    return dic_sorted_byKeys
    

def merge_dictionaries(dict_list):
    
    ldl = len(dict_list)
    if ldl == 1:
        raise ValueError("2 dictionaries at least must be passed.")
    
    str2eval = "{"
    for d in dict_list:
        str2eval += f"**{d},"
    str2eval += "}"
    
    merged_dict = eval(str2eval)
    return merged_dict
