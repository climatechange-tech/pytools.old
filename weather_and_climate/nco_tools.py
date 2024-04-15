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

custom_mod1_path = f"{fixed_path}/files_and_directories"
custom_mod2_path = f"{fixed_path}/parameters_and_constants"
custom_mod3_path = f"{fixed_path}/operative_systems"   
custom_mod4_path = f"{fixed_path}/strings"   
  

# Add the paths to the 'path' attribute of module 'sys' #
#-------------------------------------------------------#

sys.path.append(custom_mod1_path)
sys.path.append(custom_mod2_path)
sys.path.append(custom_mod3_path)
sys.path.append(custom_mod4_path)

# Perform whole or partial module importations #
#----------------------------------------------#

from file_and_directory_handler import rename_objects
from file_format_tweaker import add_str_to_aux_path
from global_parameters import basic_four_rules
from information_output_formatters import format_string, print_format_string
from os_operations import exec_shell_command

#-------------------------#
# Define custom functions #
#-------------------------#

def modify_variable_units_and_values(file_list,
                                     variable_name,
                                     operator,
                                     value,
                                     new_unit):
    
    if not isinstance(file_list, list):
        file_list = [file_list]
    lfl = len(file_list)    
        
    for file_num, file_name in enumerate(file_list, start=1): 
        temp_file = add_str_to_aux_path(file_name, str2add=file_name)
        
        isactuallyfloat = (abs(value-int(value)) == 0)
        isactuallyfloat_int = int(isactuallyfloat)
        
        var_chunit_command\
        = f"ncatted -a units,{variable_name},o,c,'{new_unit}' '{file_name}'"
        exec_shell_command(var_chunit_command)
        
        if operator not in basic_four_rules:
            raise ValueError(wrong_operator_errtext)
        else:            
            # Print progress information #
            operator_gerund = operator_gerund_dict.get(operator)
            arg_tuple_print = (ncap2_comm_args, 
                               operator_gerund, value, variable_name, 
                               file_num, lfl)
            print_format_string(prefmt_str_progress_UV, arg_tuple_print)
            
            # Get the command from the corresponding switch dictionary #
            arg_tuple_command = (ncap2_comm_args,
                                 variable_name, variable_name, value,
                                 file_name, temp_file)
            
            varval_mod_command = \
            format_string(varval_mod_command_dict_UV
                          .get(operator)
                          .get(isactuallyfloat_int),
                          arg_tuple_command)
        
            # Execute the command through the shell #
            exec_shell_command(varval_mod_command)            
            rename_objects(temp_file, file_name)
                                                 

def modify_coordinate_values_by_threshold(file_list,
                                          dimension_name,
                                          threshold,
                                          operator,
                                          value,
                                          threshold_mode="max"):
    
    if not isinstance(file_list, list):
        file_list = [file_list]
    lfl = len(file_list) 
    
    for file_num, file_name in enumerate(file_list, start=1):
        temp_file = add_str_to_aux_path(file_name, str2add=file_name)
        
        isactuallyfloat = (abs(value-int(value)) == 0)
        isactuallyfloat_int = int(isactuallyfloat)
        
        if operator not in basic_four_rules:
            raise ValueError(wrong_operator_errtext)
        else:
            if threshold_mode not in threshold_mode_opts:
                raise ValueError(format_string(prefmt_wrong_threshold_mode,
                                               threshold_mode_opts))
            
            else:
                # Print progress information #
                operator_gerund = operator_gerund_dict.get(operator)
                    
                arg_tuple_print = (ncap2_comm_args, 
                                   operator_gerund, value, dimension_name, 
                                   file_num, lfl)
                
                print_format_string(prefmt_str_progress_BTH, arg_tuple_print)
                
                # Get the command from the corresponding switch dictionary #
                arg_tuple_command = (ncap2_comm_args,
                                     dimension_name, threshold,
                                     dimension_name, dimension_name, value,
                                     file_name, temp_file)
                
                dimval_mod_command = \
                format_string(varval_mod_command_dict_BTH
                              .get(operator)
                              .get(threshold_mode)
                              .get(isactuallyfloat_int),
                              arg_tuple_command)
            
                # Execute the command through the shell #
                exec_shell_command(dimval_mod_command)            
                rename_objects(temp_file, file_name)
            

def modify_coordinate_all_values(file_list,
                                 dimension_name,
                                 threshold,
                                 operator,
                                 value,
                                 threshold_mode="max"):
    
    if not isinstance(file_list, list):
        file_list = [file_list]
    lfl = len(file_list) 
    
    for file_num, file_name in enumerate(file_list, start=1): 
        temp_file = add_str_to_aux_path(file_name, str2add=file_name)
        
        isactuallyfloat = (abs(value-int(value)) == 0)
        isactuallyfloat_int = int(isactuallyfloat)
        
        if operator not in basic_four_rules:
            raise ValueError(wrong_operator_errtext)
        else:
            if threshold_mode not in threshold_mode_opts:
                raise ValueError(format_string(prefmt_wrong_threshold_mode,
                                               threshold_mode_opts))
            
            else:
                # Print progress information #
                operator_gerund = operator_gerund_dict.get(operator)
                    
                arg_tuple_print = (ncap2_comm_args, 
                                   operator_gerund, value, dimension_name, 
                                   file_num, lfl)
                
                print_format_string(prefmt_str_progress_BTH, arg_tuple_print)
                
                # Get the command from the corresponding switch dictionary #
                arg_tuple_command = (ncap2_comm_args,
                                     dimension_name, dimension_name, value,
                                     file_name, temp_file)
                
                dimval_mod_command = \
                format_string(varval_mod_command_dict_all
                              .get(operator)
                              .get(threshold_mode)
                              .get(isactuallyfloat_int),
                              arg_tuple_command)
            
                # Execute the command through the shell #
                exec_shell_command(dimval_mod_command)            
                rename_objects(temp_file, file_name)

            
#--------------------------#
# Parameters and constants #
#--------------------------#

# Fixed and preformatted strings #
#--------------------------------#

# NCAP2 command #
ncap2_comm_args = "ncap2 -O -s"

# Progress verbose #
prefmt_str_progress_UV = \
"""{} the value of {} to '{}' variable's value for file
{} out of {}..."""

prefmt_str_progress_BTH = \
"""{}, where necessary, the value of {} to '{}' dimension's values for file
{} out of {}..."""

prefmt_str_progress_all = \
"""{} the value of {} to '{}' dimension's values for file
{} out of {}..."""

# NCAP2 command's argument syntaxes, for all values or dimensions #
prefmt_str_addvalue = """{} '{}={}+{}' '{}' '{}'"""
prefmt_str_subtrvalue = """{} '{}={}-{}' '{}' '{}'"""
prefmt_str_multvalue = """{} '{}={}*{}' '{}' '{}'"""
prefmt_str_divvalue = """{} '{}={}/{}' '{}' '{}'"""

prefmt_str_addvalue_float = """{} '{}={}+{}.0f' '{}' '{}'"""
prefmt_str_subtrvalue_float = """{} '{}={}-{}.0f' '{}' '{}'"""
prefmt_str_multvalue_float = """{} '{}={}*{}.0f' '{}' '{}'"""
prefmt_str_divvalue_float = """{} '{}={}/{}.0f' '{}' '{}'"""

# NCAP2 command's argument syntaxes, conditional #
prefmt_str_addvalue_where_max = """{} 'where({}<{}) {}={}+{}' '{}' '{}'"""
prefmt_str_subtrvalue_where_max = """{} 'where({}<{}) {}={}-{}' '{}' '{}'"""
prefmt_str_multvalue_where_max = """{} 'where({}<{}) {}={}*{}' '{}' '{}'"""
prefmt_str_divvalue_where_max = """{} 'where({}<{}) {}={}/{}' '{}' '{}'"""

prefmt_str_addvalue_where_max_float = """{} 'where({}<{}) {}={}+{}.0f' '{}' '{}'"""
prefmt_str_subtrvalue_where_max_float = """{} 'where({}<{}) {}={}-{}.0f' '{}' '{}'"""
prefmt_str_multvalue_where_max_float = """{} 'where({}<{}) {}={}*{}.0f' '{}' '{}'"""
prefmt_str_divvalue_where_max_float = """{} 'where({}<{}) {}={}/{}.0f' '{}' '{}'"""


prefmt_str_addvalue_where_min = """{} 'where({}>{}) {}={}+{}' '{}' '{}'"""
prefmt_str_subtrvalue_where_min = """{} 'where({}>{}) {}={}-{}' '{}' '{}'"""
prefmt_str_multvalue_where_min = """{} 'where({}>{}) {}={}*{}' '{}' '{}'"""
prefmt_str_divvalue_where_min = """{} 'where({}>{}) {}={}/{}' '{}' '{}'"""

prefmt_str_addvalue_where_min_float = """{} 'where({}>{}) {}={}+{}.0f' '{}' '{}'"""
prefmt_str_subtrvalue_where_min_float = """{} 'where({}>{}) {}={}-{}.0f' '{}' '{}'"""
prefmt_str_multvalue_where_min_float = """{} 'where({}>{}) {}={}*{}.0f' '{}' '{}'"""
prefmt_str_divvalue_where_min_float = """{} 'where({}>{}) {}={}/{}.0f' '{}' '{}'"""

# Error messages #
wrong_operator_errtext = \
f"Wrong basic operator chosen. Options are {basic_four_rules}."
prefmt_wrong_threshold_mode = \
"""Wrong threshold mode. Options are {}."""


# Locally available threshold mode list #
#---------------------------------------#

threshold_mode_opts = ["max", "min"]

# Switch-case dictionaries #
#--------------------------#

operator_gerund_dict = {
    basic_four_rules[0] : "Adding",
    basic_four_rules[1] : "Subtracting",
    basic_four_rules[2] : "Multiplying",
    basic_four_rules[3] : "Dividing"
    }

varval_mod_command_dict_UV = {
    basic_four_rules[0] : {
        1 : prefmt_str_addvalue,
        0 : prefmt_str_addvalue_float
    },
    basic_four_rules[1] : {
        1 : prefmt_str_subtrvalue,
        0 : prefmt_str_subtrvalue_float
    },
    basic_four_rules[2] : {
        1 : prefmt_str_multvalue,
        0 : prefmt_str_multvalue_float
    },
    basic_four_rules[3] : {
        1 : prefmt_str_divvalue,
        0 : prefmt_str_divvalue_float
    }
}

varval_mod_command_dict_BTH = {
    basic_four_rules[0] : {
        "max" : {
            1 : prefmt_str_addvalue_where_max,
            0 : prefmt_str_addvalue_where_max_float
        },
        "min" : {
            1 : prefmt_str_addvalue_where_min,
            0 : prefmt_str_addvalue_where_min_float
        },
    },
    basic_four_rules[1] : {
        "max" : {
            1 : prefmt_str_subtrvalue_where_max,
            0 : prefmt_str_subtrvalue_where_max_float
        },
        "min" : {
            1 : prefmt_str_subtrvalue_where_min,
            0 : prefmt_str_subtrvalue_where_min_float
        },
    },
    basic_four_rules[2] : {
        "max" : {
            1 : prefmt_str_multvalue_where_max,
            0 : prefmt_str_multvalue_where_max_float
        },
        "min" : {
            1 : prefmt_str_multvalue_where_min,
            0 : prefmt_str_multvalue_where_min_float
        },
    },
    basic_four_rules[3] : {
        "max" : {
            1 : prefmt_str_divvalue_where_max,
            0 : prefmt_str_divvalue_where_max_float
        },
        "min" : {
            1 : prefmt_str_divvalue_where_min,
            0 : prefmt_str_divvalue_where_min_float
        }
    }
}

varval_mod_command_dict_all = {
    basic_four_rules[0] : {
        "max" : {
            1 : prefmt_str_addvalue,
            0 : prefmt_str_addvalue_float
        },
        "min" : {
            1 : prefmt_str_addvalue,
            0 : prefmt_str_addvalue_float
        },
    },
    basic_four_rules[1] : {
        "max" : {
            1 : prefmt_str_subtrvalue,
            0 : prefmt_str_subtrvalue_float
        },
        "min" : {
            1 : prefmt_str_subtrvalue,
            0 : prefmt_str_subtrvalue_float
        },
    },
    basic_four_rules[2] : {
        "max" : {
            1 : prefmt_str_multvalue,
            0 : prefmt_str_multvalue_float
        },
        "min" : {
            1 : prefmt_str_multvalue,
            0 : prefmt_str_multvalue_float
        },
    },
    basic_four_rules[3] : {
        "max" : {
            1 : prefmt_str_divvalue,
            0 : prefmt_str_divvalue_float
        },
        "min" : {
            1 : prefmt_str_divvalue,
            0 : prefmt_str_divvalue_float
        }
    }
}
