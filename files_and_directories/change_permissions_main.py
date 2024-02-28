#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

# Find the path of the Python toolbox #
home_PATH = Path.home()
sys.path.append(str(home_PATH))

import get_pytools_path
fixed_path = get_pytools_path.return_custom_path()

# Enumerate custom modules and their paths #
#------------------------------------------#

custom_mod1_path = f"{fixed_path}/files_and_directories"
custom_mod2_path = f"{fixed_path}/parameters_and_constants"
custom_mod3_path = f"{fixed_path}/strings"
                                        
# Add the paths to the 'path' attribute of module 'sys' #
#-------------------------------------------------------#

sys.path.append(custom_mod1_path)
sys.path.append(custom_mod2_path)
sys.path.append(custom_mod3_path)

# Perform whole or partial module importations #
#----------------------------------------------#

import file_and_directory_paths
from global_parameters import basic_object_types
from information_output_formatters import format_string, print_format_string
from string_handler import find_substring_index

#----------------------------------------------------#
# Define imported module(s)' function call shortcuts #
#----------------------------------------------------#

find_allfile_extensions = file_and_directory_paths.find_allfile_extensions
find_allDirectories = file_and_directory_paths.find_allDirectories
find_ext_file_paths = file_and_directory_paths.find_ext_file_paths

#-----------------------------#
# Get this laptop user's name #
#-----------------------------#

whoami = home_PATH.parts[-1]

#-------------------------#
# Define custom functions #
#-------------------------#

def modify_obj_permissions(path, 
                           obj_type="file",
                           extensions2skip="",
                           attr_id=664):
    
    """
    Default permission ID configuration (as when touching files
    or creating directories) is as follows:
    
    Files: attr_id = 664
    Directories: attr_id = 775
    """    
    arg_names = modify_obj_permissions.__code__.co_varnames
    ot_arg_pos = find_substring_index(arg_names, 
                                      "obj_type",
                                      advanced_search=True,
                                      find_whole_words=True)
    attr_arg_pos = find_substring_index(arg_names, 
                                        "attr_id",
                                        advanced_search=True,
                                        find_whole_words=True)
    
    if isinstance(attr_id, str):
        raise TypeError(format_string(typeErrorStr, arg_names[attr_arg_pos]))
        
    le2s = len(extensions2skip)
    
    if obj_type not in basic_object_types:
        arg_tuple_mod_perms1 = (arg_names[ot_arg_pos], basic_object_types)
        raise ValueError(format_string(valueErrorStr, arg_tuple_mod_perms1))
  
    if obj_type == basic_object_types[0]:
        
        if le2s > 0:
            arg_tuple_mod_perms2 = ("permissions", path, extensions2skip)
            print_format_string(permModExceptionsProgressInfo, arg_tuple_mod_perms2)
        else:
            arg_tuple_mod_perms3 = ("permissions", "files", path)
            print_format_string(permModProgressInfoStr, arg_tuple_mod_perms3)
            
        file_extension_list = find_allfile_extensions(extensions2skip, 
                                                      path, 
                                                      top_path_only=True)
        obj_path_list = find_ext_file_paths(file_extension_list,
                                            path, 
                                            top_path_only=True)
            
    elif obj_type == basic_object_types[1]:
        arg_tuple_mod_perms4 = ("permissions", "directories", path)
        print_format_string(permModProgressInfoStr, arg_tuple_mod_perms4)
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
    """
    Note
    ----
    In order to modify file and/or directory owner and/or group names,
    both os.chown and shutil.chown need the user to be rooted.
    """
    
    arg_names = modify_obj_permissions.__code__.co_varnames
    mod_arg_pos = find_substring_index(arg_names, 
                                       "module",
                                       advanced_search=True,
                                       find_whole_words=True)
    ot_arg_pos = find_substring_index(arg_names, 
                                      "obj_type", 
                                      advanced_search=True,
                                      find_whole_words=True)
    
    le2s = len(extensions2skip)
    
    if obj_type not in basic_object_types:
        arg_tuple_mod_perms2 = (arg_names[ot_arg_pos], basic_object_types)
        raise ValueError(format_string(valueErrorStr, arg_tuple_mod_perms2))
        
    if module not in modules:
        arg_tuple_mod_perms3 = (arg_names[mod_arg_pos], modules)
        raise ValueError(format_string(valueErrorStr, arg_tuple_mod_perms3))
        
    if obj_type == basic_object_types[0]:
        
        if le2s > 0:
            arg_tuple_mod_perms5 = ("owner", "files", path, extensions2skip)
            print_format_string(permModExceptionsProgressInfo, arg_tuple_mod_perms5)
        else:
            arg_tuple_mod_perms6 = ("owner", "files", path)
            print_format_string(permModProgressInfoStr, arg_tuple_mod_perms6)
            
        file_extension_list = find_allfile_extensions(extensions2skip, 
                                                      path, 
                                                      top_path_only=True)
        obj_path_list = find_ext_file_paths(file_extension_list,
                                            path, 
                                            top_path_only=True)
        
    elif obj_type == basic_object_types[1]:
        arg_tuple_mod_perms7 = ("permissions", "directories", path)
        print_format_string(permModProgressInfoStr, arg_tuple_mod_perms7)
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
    
#--------------------------#
# Parameters and constants #
#--------------------------#

# OS-related #
#------------#

modules = ["os", "shutil"]

# Preformatted strings #
#----------------------#

# Error indicators #
typeErrorStr = """Argument '{}' "must be of type 'int'"""
permissionErrorStr = "Please execute the program as sudo."
valueErrorStr = """Wrong '{}' option. Options are {}."""

# Progress information #
permModExceptionsProgressInfo = """Modifying {} of all {} in {}\
except the following extensioned ones...\n{}"""

permModProgressInfoStr = """Modifying {} of all {} in {}..."""
