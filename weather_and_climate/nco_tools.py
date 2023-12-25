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
fixed_path = get_pytools_path.return_custom_path()

# Enumerate custom modules and their paths #
#------------------------------------------#

custom_mod1_path = f"{fixed_path}/files_and_directories"
custom_mod2_path = f"{fixed_path}/parameters_and_constants"
custom_mod3_path = f"{fixed_path}/operative_systems"     

# Add the module paths to the path variable #
#-------------------------------------------#

sys.path.append(custom_mod1_path)
sys.path.append(custom_mod2_path)
sys.path.append(custom_mod3_path)

# Perform the module importations #
#---------------------------------#

import file_and_directory_handler
import file_format_tweaker
import global_parameters
import os_operations

#----------------------------------------------------#
# Define imported module(s)´ function call shortcuts #
#----------------------------------------------------#

rename_objects = file_and_directory_handler.rename_objects
aux_path_strAdd = file_format_tweaker.aux_path_strAdd
basic_four_rules = global_parameters.basic_four_rules
exec_shell_command = os_operations.exec_shell_command

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
        
    for file in enumerate(file_list): 
        
        file_name = file[-1]
        file_num = file[0] + 1
                
        temp_file = aux_path_strAdd(file_name, str2add=file_name)
        
        isactuallyfloat = (abs(value-int(value)) == 0)
        
        var_chunit_command\
        = f"ncatted -a units,{variable_name},o,c,'{new_unit}' '{file_name}'"
        exec_shell_command(var_chunit_command)
        
        # TODO: ondoko aukera guztiak hiztegi-aukeraketaren 'SWITCH' motako funtzio bidez egingarria denentz berrikusi
        if operator == "+":
            
            print(f"Adding the value of {value} to "
                  f"'{variable_name}' variable's values for file "
                  f"{file_num} out of {lfl}...")
            
            if isactuallyfloat:
                varval_mod_command =\
                f"ncap2 -O -s "\
                f"'{variable_name}={variable_name}+{value}.0f' "\
                f"'{file_name}' '{temp_file}'"
                                     
            else:
                varval_mod_command =\
                f"ncap2 -O -s "\
                f"'{variable_name}={variable_name}+{value}' "\
                f"'{file_name}' '{temp_file}'"
                                     
            exec_shell_command(varval_mod_command)            
            rename_objects(temp_file, file_name)
                                     
                                     
        elif operator == "-":
            
            print(f"Subtracting the value of {value} to "
                  f"'{variable_name}' variable's values for file "
                  f"{file_num} out of {lfl}...")
            
            if isactuallyfloat:
                varval_mod_command =\
                f"ncap2 -O -s "\
                f"'{variable_name}={variable_name}-{value}.0f' "\
                f"'{file_name}' '{temp_file}'"
                                     
            else:
                varval_mod_command =\
                f"ncap2 -O -s "\
                f"'{variable_name}={variable_name}-{value}' "\
                f"'{file_name}' '{temp_file}'"
                                     
            exec_shell_command(varval_mod_command)            
            rename_objects(temp_file, file_name)
                                     
        elif operator == "*":
            
            print(f"Multiplying the value of {value} to "
                  f"'{variable_name}' variable's values for file "
                  f"{file_num} out of {lfl}...")
            
            if isactuallyfloat:
                varval_mod_command =\
                f"ncap2 -O -s "\
                f"'{variable_name}={variable_name}*{value}.0f' "\
                f"'{file_name}' '{temp_file}'"
                                     
            else:
                varval_mod_command =\
                f"ncap2 -O -s "\
                f"'{variable_name}={variable_name}*{value}' "\
                f"'{file_name}' '{temp_file}'"
                                     
            exec_shell_command(varval_mod_command)            
            rename_objects(temp_file, file_name)
                                     
        elif operator == "/":
            
            print(f"Dividing the value of {value} to "
                  f"'{variable_name}' variable's values for file "
                  f"{file_num} out of {lfl}...")
            
            if isactuallyfloat:
                varval_mod_command =\
                f"ncap2 -O -s "\
                f"'{variable_name}={variable_name}/{value}.0f' "\
                f"'{file_name}' '{temp_file}'"
                                     
            else:
                varval_mod_command =\
                f"ncap2 -O -s "\
                f"'{variable_name}={variable_name}/{value}' "\
                f"'{file_name}' '{temp_file}'"
            
            exec_shell_command(varval_mod_command)            
            rename_objects(temp_file, file_name)
                                     
        else:
            raise ValueError("Wrong basic operator chosen.\n"
                             f"Options are {basic_four_rules}")


def modify_coordinate_values_byThreshold(file_list,
                                         dimension_name,
                                         threshold,
                                         operator,
                                         value,
                                         threshold_mode="max"):
    
    if not isinstance(file_list, list):
        file_list = [file_list]
    lfl = len(file_list) 
    
    for file in enumerate(file_list): 
        
        file_name = file[-1]
        file_num = file[0] + 1

        temp_file = aux_path_strAdd(file_name, str2add=file_name)
        
        isactuallyfloat = (abs(value-int(value)) == 0)
                                
        if operator == "+":
            
            print(f"Adding, where necessary, the value of {value} to "
                  f"'{dimension_name}' dimension's values for file "
                  f"{file_num} out of {lfl}...")
        
            if threshold_mode == "max":      
                if isactuallyfloat:                    
                    dimval_mod_command =\
                    f"ncap2 -O -s 'where({dimension_name}<{threshold}) "\
                    f"{dimension_name}={dimension_name}+{value}' "\
                    f"'{file_name}' '{temp_file}'"
                    
                else:                    
                    dimval_mod_command =\
                    f"ncap2 -O -s 'where({dimension_name}<{threshold}) "\
                    f"{dimension_name}={dimension_name}+{value}.0f' "\
                    f"'{file_name}' '{temp_file}'"
                                   
            elif threshold_mode == "min":
                if isactuallyfloat:
                    dimval_mod_command =\
                    f"ncap2 -O -s 'where({dimension_name}>{threshold}) "\
                    f"{dimension_name}={dimension_name}+{value}' "\
                    f"'{file_name}' '{temp_file}'"
                    
                else:
                    dimval_mod_command =\
                    f"ncap2 -O -s 'where({dimension_name}>{threshold}) "\
                    f"{dimension_name}={dimension_name}+{value}.0f' "\
                    f"'{file_name}' '{temp_file}'"
                                     
            exec_shell_command(dimval_mod_command)            
            rename_objects(temp_file, file_name)
                                     
        elif operator == "-":
            
            print(f"Subtracting, where necessary, the value of {value} to "
                  f"'{dimension_name}' dimension's values for file "
                  f"{file_num} out of {lfl}...")
        
            if threshold_mode == "max":      
                if isactuallyfloat:
                    dimval_mod_command =\
                    f"ncap2 -O -s 'where({dimension_name}<{threshold}) "\
                    f"{dimension_name}={dimension_name}-{value}' "\
                    f"'{file_name}' '{temp_file}'"
                
                else:
                    dimval_mod_command =\
                    f"ncap2 -O -s 'where({dimension_name}<{threshold}) "\
                    f"{dimension_name}={dimension_name}-{value}.0f' "\
                    f"'{file_name}' '{temp_file}'"
                                   
            elif threshold_mode == "min":
                if isactuallyfloat:
                    dimval_mod_command =\
                    f"ncap2 -O -s 'where({dimension_name}>{threshold}) "\
                    f"{dimension_name}={dimension_name}-{value}' "\
                    f"'{file_name}' '{temp_file}'"
                    
                else:
                    dimval_mod_command =\
                    f"ncap2 -O -s 'where({dimension_name}>{threshold}) "\
                    f"{dimension_name}={dimension_name}-{value}.0f' "\
                    f"'{file_name}' '{temp_file}'"
                                     
            exec_shell_command(dimval_mod_command)            
            rename_objects(temp_file, file_name)
                                                 
        elif operator == "*":
            
            print(f"Multiplying, where necessary, the value of {value} to "
                  f"'{dimension_name}' dimension's values for file "
                  f"{file_num} out of {lfl}...")
        
            if threshold_mode == "max":      
                if isactuallyfloat:
                    dimval_mod_command =\
                    f"ncap2 -O -s 'where({dimension_name}<{threshold}) "\
                    f"{dimension_name}={dimension_name}*{value}' "\
                    f"'{file_name}' '{temp_file}'"
                    
                else:
                    dimval_mod_command =\
                    f"ncap2 -O -s 'where({dimension_name}<{threshold}) "\
                    f"{dimension_name}={dimension_name}*{value}.0f' "\
                    f"'{file_name}' '{temp_file}'"
                                   
            elif threshold_mode == "min":
                if isactuallyfloat:
                    dimval_mod_command =\
                    f"ncap2 -O -s 'where({dimension_name}>{threshold}) "\
                    f"{dimension_name}={dimension_name}*{value}' "\
                    f"'{file_name}' '{temp_file}'"
                
                else:
                    dimval_mod_command =\
                    f"ncap2 -O -s 'where({dimension_name}>{threshold}) "\
                    f"{dimension_name}={dimension_name}*{value}.0f' "\
                    f"'{file_name}' '{temp_file}'"
                                     
            exec_shell_command(dimval_mod_command)            
            rename_objects(temp_file, file_name)
                                     
        elif operator == "/":
            
            print(f"Dividing, where necessary, the value of {value} to "
                  f"'{dimension_name}' dimension's values for file "
                  f"{file_num} out of {lfl}...")
        
            if threshold_mode == "max":                
                if isactuallyfloat:
                    dimval_mod_command =\
                    f"ncap2 -O -s 'where({dimension_name}<{threshold}) "\
                    f"{dimension_name}={dimension_name}/{value}' "\
                    f"'{file_name}' '{temp_file}'"
                                         
                else:
                    dimval_mod_command =\
                    f"ncap2 -O -s 'where({dimension_name}<{threshold}) "\
                    f"{dimension_name}={dimension_name}/{value}.0f' "\
                    f"'{file_name}' '{temp_file}'"
                                         
            elif threshold_mode == "min":
                if isactuallyfloat:
                    dimval_mod_command =\
                    f"ncap2 -O -s 'where({dimension_name}>{threshold}) "\
                    f"{dimension_name}={dimension_name}/{value}' "\
                    f"'{file_name}' '{temp_file}'"
                    
                else:
                    dimval_mod_command =\
                    f"ncap2 -O -s 'where({dimension_name}>{threshold}) "\
                    f"{dimension_name}={dimension_name}/{value}.0f' "\
                    f"'{file_name}' '{temp_file}'"
                                         
            exec_shell_command(dimval_mod_command)            
            rename_objects(temp_file, file_name)
                                                  
        else:
            raise ValueError("Wrong basic operator chosen.\n"
                             f"Options are {basic_four_rules}")

# TODO: koordenatu guztiei balio bera sar dakieeneko ondoko funtzioa atondu.
def modify_coordinate_allValues(file_list,
                                dimension_name,
                                threshold,
                                operator,
                                value,
                                threshold_mode="max"):
    
    if not isinstance(file_list, list):
        file_list = [file_list]
    lfl = len(file_list) 
    
    for file in enumerate(file_list): 
        
        file_name = file[-1]
        file_num = file[0] + 1

        temp_file = aux_path_strAdd(file_name, str2add=file_name)
        
        isactuallyfloat = (abs(value-int(value)) == 0)
                                
        if operator == "+":
            
            print(f"Adding, where necessary, the value of {value} to "
                  f"'{dimension_name}' dimension's values for file "
                  f"{file_num} out of {lfl}...")
        
            if threshold_mode == "max":      
                if isactuallyfloat:                    
                    dimval_mod_command =\
                    f"ncap2 -O -s 'where({dimension_name}<{threshold}) "\
                    f"{dimension_name}={dimension_name}+{value}' "\
                    f"'{file_name}' '{temp_file}'"
                    
                else:                    
                    dimval_mod_command =\
                    f"ncap2 -O -s 'where({dimension_name}<{threshold}) "\
                    f"{dimension_name}={dimension_name}+{value}.0f' "\
                    f"'{file_name}' '{temp_file}'"
                                   
            elif threshold_mode == "min":
                if isactuallyfloat:
                    dimval_mod_command =\
                    f"ncap2 -O -s 'where({dimension_name}>{threshold}) "\
                    f"{dimension_name}={dimension_name}+{value}' "\
                    f"'{file_name}' '{temp_file}'"
                    
                else:
                    dimval_mod_command =\
                    f"ncap2 -O -s 'where({dimension_name}>{threshold}) "\
                    f"{dimension_name}={dimension_name}+{value}.0f' "\
                    f"'{file_name}' '{temp_file}'"
                                     
            exec_shell_command(dimval_mod_command)            
            rename_objects(temp_file, file_name)
                                     
        elif operator == "-":
            
            print(f"Subtracting, where necessary, the value of {value} to "
                  f"'{dimension_name}' dimension's values for file "
                  f"{file_num} out of {lfl}...")
        
            if threshold_mode == "max":      
                if isactuallyfloat:
                    dimval_mod_command =\
                    f"ncap2 -O -s 'where({dimension_name}<{threshold}) "\
                    f"{dimension_name}={dimension_name}-{value}' "\
                    f"'{file_name}' '{temp_file}'"
                
                else:
                    dimval_mod_command =\
                    f"ncap2 -O -s 'where({dimension_name}<{threshold}) "\
                    f"{dimension_name}={dimension_name}-{value}.0f' "\
                    f"'{file_name}' '{temp_file}'"
                                   
            elif threshold_mode == "min":
                if isactuallyfloat:
                    dimval_mod_command =\
                    f"ncap2 -O -s 'where({dimension_name}>{threshold}) "\
                    f"{dimension_name}={dimension_name}-{value}' "\
                    f"'{file_name}' '{temp_file}'"
                    
                else:
                    dimval_mod_command =\
                    f"ncap2 -O -s 'where({dimension_name}>{threshold}) "\
                    f"{dimension_name}={dimension_name}-{value}.0f' "\
                    f"'{file_name}' '{temp_file}'"
                                     
            exec_shell_command(dimval_mod_command)            
            rename_objects(temp_file, file_name)
                                                 
        elif operator == "*":
            
            print(f"Multiplying, where necessary, the value of {value} to "
                  f"'{dimension_name}' dimension's values for file "
                  f"{file_num} out of {lfl}...")
        
            if threshold_mode == "max":      
                if isactuallyfloat:
                    dimval_mod_command =\
                    f"ncap2 -O -s 'where({dimension_name}<{threshold}) "\
                    f"{dimension_name}={dimension_name}*{value}' "\
                    f"'{file_name}' '{temp_file}'"
                    
                else:
                    dimval_mod_command =\
                    f"ncap2 -O -s 'where({dimension_name}<{threshold}) "\
                    f"{dimension_name}={dimension_name}*{value}.0f' "\
                    f"'{file_name}' '{temp_file}'"
                                   
            elif threshold_mode == "min":
                if isactuallyfloat:
                    dimval_mod_command =\
                    f"ncap2 -O -s 'where({dimension_name}>{threshold}) "\
                    f"{dimension_name}={dimension_name}*{value}' "\
                    f"'{file_name}' '{temp_file}'"
                
                else:
                    dimval_mod_command =\
                    f"ncap2 -O -s 'where({dimension_name}>{threshold}) "\
                    f"{dimension_name}={dimension_name}*{value}.0f' "\
                    f"'{file_name}' '{temp_file}'"
                                     
            exec_shell_command(dimval_mod_command)            
            rename_objects(temp_file, file_name)
                                     
        elif operator == "/":
            
            print(f"Dividing, where necessary, the value of {value} to "
                  f"'{dimension_name}' dimension's values for file "
                  f"{file_num} out of {lfl}...")
        
            if threshold_mode == "max":                
                if isactuallyfloat:
                    dimval_mod_command =\
                    f"ncap2 -O -s 'where({dimension_name}<{threshold}) "\
                    f"{dimension_name}={dimension_name}/{value}' "\
                    f"'{file_name}' '{temp_file}'"
                                         
                else:
                    dimval_mod_command =\
                    f"ncap2 -O -s 'where({dimension_name}<{threshold}) "\
                    f"{dimension_name}={dimension_name}/{value}.0f' "\
                    f"'{file_name}' '{temp_file}'"
                                         
            elif threshold_mode == "min":
                if isactuallyfloat:
                    dimval_mod_command =\
                    f"ncap2 -O -s 'where({dimension_name}>{threshold}) "\
                    f"{dimension_name}={dimension_name}/{value}' "\
                    f"'{file_name}' '{temp_file}'"
                    
                else:
                    dimval_mod_command =\
                    f"ncap2 -O -s 'where({dimension_name}>{threshold}) "\
                    f"{dimension_name}={dimension_name}/{value}.0f' "\
                    f"'{file_name}' '{temp_file}'"
                                         
            exec_shell_command(dimval_mod_command)            
            rename_objects(temp_file, file_name)
                                                  
        else:
            raise ValueError("Wrong basic operator chosen. "
                             f"Options are {basic_four_rules}")
