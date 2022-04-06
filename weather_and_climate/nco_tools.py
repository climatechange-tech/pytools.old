#----------------#
# Import modules #
#----------------#

import importlib
import os
from pathlib import Path

#---------------------------#
# Get the fixed directories #
#---------------------------#

cwd = Path.cwd()
main_path = Path("/".join(cwd.parts[:3])[1:]).glob("*/*")

# All-code containing directory #
fixed_dirpath = str([path
                     for path in main_path
                     if "pytools" in str(path).lower()][0])

#-----------------------#
# Import custom modules #
#-----------------------#

module_imp1 = "string_handler.py"
module_imp1_path = f"{fixed_dirpath}/"\
                   f"strings/{module_imp1}"

spec1 = importlib.util.spec_from_file_location(module_imp1, module_imp1_path)
string_handler = importlib.util.module_from_spec(spec1)
spec1.loader.exec_module(string_handler)


module_imp2 = "file_handler.py"
module_imp2_path = f"{fixed_dirpath}/"\
                   f"files_and_directories/{module_imp2}"

spec2 = importlib.util.spec_from_file_location(module_imp2, module_imp2_path)
file_handler = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(file_handler)

#----------------------------------------------------#
# Define imported module(s)´ function call shortcuts #
#----------------------------------------------------#

create_temporal_file_name = string_handler.create_temporal_file_name
rename_objects = file_handler.rename_objects

#------------------------#
# Define global variable # 
#------------------------#

file_name_splitchar = "_"

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
                
        temp_file = string_handler.create_temporal_file_name(file_name,
                                                             file_name_splitchar)
        
        isactuallyfloat = (abs(value-int(value)) == 0)
        
        var_chunit_command\
        = f"ncatted -a units,{variable_name},o,c,'{new_unit}' '{file_name}'"
        os.system(var_chunit_command)
        
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
                                     
            os.system(varval_mod_command)            
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
                                     
            os.system(varval_mod_command)            
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
                                     
            os.system(varval_mod_command)            
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
            
            os.system(varval_mod_command)            
            rename_objects(temp_file, file_name)
                                     
        else:
            raise ValueError("Wrong basic operator chosen. "
                             "Options are {'+', '-', '*', '/'}")


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

        temp_file = string_handler.create_temporal_file_name(file_name,
                                                             file_name_splitchar)
        
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
                                     
            os.system(dimval_mod_command)            
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
                                     
            os.system(dimval_mod_command)            
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
                                     
            os.system(dimval_mod_command)            
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
                                         
            os.system(dimval_mod_command)            
            rename_objects(temp_file, file_name)
                                                  
        else:
            raise ValueError("Wrong basic operator chosen. "
                             "Options are {'+', '-', '*', '/'}")

# TODO: koordenatu guztiei balio bera sar dakieeneko ondoko funtzioa atondu.
def modify_coordinate_allValues(file_list,
                                dimension_name,
                                threshold,
                                operator,
                                value):
    
    if not isinstance(file_list, list):
        file_list = [file_list]
    lfl = len(file_list) 
    
    for file in enumerate(file_list): 
        
        file_name = file[-1]
        file_num = file[0] + 1

        temp_file = string_handler.create_temporal_file_name(file_name,
                                                             file_name_splitchar)
        
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
                                     
            os.system(dimval_mod_command)            
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
                                     
            os.system(dimval_mod_command)            
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
                                     
            os.system(dimval_mod_command)            
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
                                         
            os.system(dimval_mod_command)            
            rename_objects(temp_file, file_name)
                                                  
        else:
            raise ValueError("Wrong basic operator chosen. "
                             "Options are {'+', '-', '*', '/'}")
