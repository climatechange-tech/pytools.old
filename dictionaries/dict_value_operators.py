#----------------#
# Import modules #
#----------------#

import datetime
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

custom_mod6_path = f"{fixed_dirpath}/strings"
                  
# Add the module paths to the path variable #
#-------------------------------------------#

sys.path.append(custom_mod6_path)

# Perform the module importations #
#---------------------------------#

import string_handler

#----------------------------------------------------#
# Define imported module(s)´ function call shortcuts #
#----------------------------------------------------#

substring_replacer = string_handler.substring_replacer

#------------------#
# Define functions #
#------------------#

def dict_value_basic_operator(dict1, dict2, basic_math_operator):

    # Performs the basic mathematical operations between two dictionaries.
    # 
    # Parameters
    # ----------
    # dict1 : dict
    #       First dictionary containing some values.
    # dict2 : dict
    #       Second dictionary containing some values.
    # basic_math_operator : {'+', '-', '*', '/'}
    # 
    # Returns
    # -------
    # Depending on the operation chosen:
    # sum_dict : dict:
    #       Dictionary with summed values.
    # subtr_dict : dict:
    #       Dictionary with subtracted values.
    # mult_dict : dict:
    #       Dictionary with multiplied values.
    # div_dict : dict:
    #       Dictionary with divided values.

    if basic_math_operator == '+':
        sum_dict = {key:
                    dict1[key] + dict2[key]
                    for key in dict1.keys() & dict2}
        return sum_dict

    elif basic_math_operator == '-':
        subtr_dict = {key:
                      dict1[key] - dict2[key]
                      for key in dict1.keys() & dict2}
        return subtr_dict

    elif basic_math_operator == '*':
        mult_dict = {key:
                     dict1[key] * dict2[key]
                     for key in dict1.keys() & dict2}
        return mult_dict

    elif basic_math_operator == '/':
        div_dict = {key:
                    dict1[key] / dict2[key]
                    for key in dict1.keys() & dict2}
        return div_dict

    else:
        raise ValueError("Wrong operator sign.")
        

def merge_dictionaries(dict_list):
    
    ldl = len(dict_list)
    if ldl == 1:
        raise ValueError("2 dictionaries at least must be passed.")
    
    dl_str = str(dict_list)
    
    substr1_find = "[{"
    substr1_replace = "[**{"
    
    substr2_find = ", "
    substr2_replace = ", **"
    
    substr3_find = "["
    substr3_replace = "{"
    
    substr4_find = "]"
    substr4_replace = "}"
    
    dl_str = substring_replacer(dl_str, substr1_find, substr1_replace)
    dl_str = substring_replacer(dl_str, substr2_find, substr2_replace)
    dl_str = substring_replacer(dl_str, substr3_find, substr3_replace)
    dl_str = substring_replacer(dl_str, substr4_find, substr4_replace)

    merged_dict = eval(dl_str)
    
    return merged_dict
