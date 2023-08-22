#----------------#
# Import modules #
#----------------#

import grp
import pwd

import os
from pathlib import Path
import shutil

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
custom_mod3_path = f"{fixed_path}/strings"
                                        
# Add the module paths to the path variable #
#-------------------------------------------#

sys.path.append(custom_mod1_path)
sys.path.append(custom_mod2_path)
sys.path.append(custom_mod3_path)

# Perform the module importations #
#---------------------------------#

import file_and_directory_handler
import file_and_directory_paths
import global_parameters
import string_handler

#----------------------------------------------------#
# Define imported module(s)´ function call shortcuts #
#----------------------------------------------------#

find_allfile_extensions = file_and_directory_paths.find_allfile_extensions
find_allDirectories = file_and_directory_handler.find_allDirectories
find_ext_file_paths = file_and_directory_handler.find_ext_file_paths

find_substring_index = string_handler.find_substring_index
basic_object_types = global_parameters.basic_object_types

#-----------------------------#
# Get this laptop user´s name #
#-----------------------------#

whoami = home_PATH.parts[-1]

#-------------------------#
# Define custom functions #
#-------------------------#

def modify_obj_permissions(path, 
                           obj_type="file",
                           extensions2skip="",
                           attr_id=664):
    
    # Default permission ID configuration (as when touching files
    # or creating directories) is as follows:
    # 
    # Files: attr_id = 664
    # Directories: attr_id = 775
        
    arg_names = modify_obj_permissions.__code__.co_varnames
    ot_arg_pos = find_substring_index(arg_names, 
                                      "obj_type",
                                      find_whole_words=True)
    attr_arg_pos = find_substring_index(arg_names, 
                                        "attr_id",
                                        find_whole_words=True)
    
    if isinstance(attr_id, str):
        raise TypeError(typeErrorStr.format(arg_names[attr_arg_pos]))
        
    le2s = len(extensions2skip)
    
    if obj_type not in bo_types:
        raise ValueError(valueErrorStr.format(arg_names[ot_arg_pos], bo_types))        
  
    if obj_type == bo_types[0]:
        
        if le2s > 0:
            print(f"Modifying permissions of all files in {path} "
                  "except the following extensioned ones...\n"
                  f"{extensions2skip}")
        else:
            print(f"Modifying permissions of all files in {path}...")
            
        file_extension_list = find_allfile_extensions(extensions2skip, 
                                                      path, 
                                                      top_path_only=True)
        obj_path_list = find_ext_file_paths(file_extension_list,
                                            path, 
                                            top_path_only=True)
            
    elif obj_type == bo_types[1]:
        print(f"Modifying permissions of all directories in {path}...")
        obj_path_list = find_allDirectories(path)
        

    for obj_path in obj_path_list:
        try:
            os.chmod(obj_path, attr_id)    
        except PermissionError:
            raise PermissionError(permissionErrorStr)
                
 
def modify_obj_owner(path,
                     module="shutil",
                     obj_type="file",
                     extensions2skip="",
                     new_owner=None,
                     new_group=None):    
    # Note
    # ----
    # In order to modify file and/or directory owner and/or group names,
    # both os.chown and shutil.chown need the user to be rooted.
    
    arg_names = modify_obj_permissions.__code__.co_varnames
    mod_arg_pos = find_substring_index(arg_names, 
                                       "module",
                                       find_whole_words=True)
    ot_arg_pos = find_substring_index(arg_names, 
                                      "obj_type", 
                                      find_whole_words=True)
    
    le2s = len(extensions2skip)
    
    if obj_type not in bo_types:
        raise ValueError(valueErrorStr.format(arg_names[ot_arg_pos], bo_types))
        
    if module not in modules:
        raise ValueError(valueErrorStr.format(arg_names[mod_arg_pos], modules))
        
    if obj_type == bo_types[0]:
        
        if le2s > 0:
            print(f"Modifying permissions of all files in {path} "
                  "except the following extensioned ones...\n"
                  f"{extensions2skip}")
        else:
            print(f"Modifying permissions of all files in {path}...")
            
        file_extension_list = find_allfile_extensions(extensions2skip, 
                                                      path, 
                                                      top_path_only=True)
        obj_path_list = find_ext_file_paths(file_extension_list,
                                            path, 
                                            top_path_only=True)
        
    elif obj_type == bo_types[1]:
        print(f"Modifying permissions of all directories in {path}...")
        obj_path_list = find_allDirectories(path)
    
    for obj_path in obj_path_list:
        if module == "os":
            
            # Owner modification #
            if new_owner is None or new_owner == "unchanged":
                uid = -1
            else:
                uid = pwd.getpwnam(new_owner).pw_uid
                
            # Group modification #
            if new_group is None or new_group == "unchanged":
                gid = -1
            else:
                gid = grp.getgrnam(new_group).gr_gid
                
            try:
                os.chown(obj_path, uid, gid)
            except PermissionError:
                raise PermissionError(permissionErrorStr)
            
        elif module == "shutil":
            try:
                shutil.chown(obj_path, user=new_owner, group=new_group)
            except PermissionError:
                raise PermissionError(permissionErrorStr)
    
#------------------#
# Local parameters #
#------------------#

modules = ["os", "shutil"]
bo_types = basic_object_types

# Error indicator tables #
#------------------------#

typeErrorStr = """Argument '{}' "must be of type 'int'"""
permissionErrorStr = "Please execute the program as sudo."
valueErrorStr = """Wrong '{}' option. Options are {}."""
