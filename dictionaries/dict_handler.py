#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

import json

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
custom_mod2_path = f"{fixed_path}/strings"

# Add the paths to the 'path' attribute of module 'sys' #
#-------------------------------------------------------#

sys.path.append(custom_mod1_path)

# Perform whole or partial module importations #
#----------------------------------------------#

from file_and_directory_paths import find_fileString_paths
from string_handler import aux_ext_adder, get_obj_specs

#-------------------------#
# Define custom functions #
#-------------------------#

def dict2JSON(dictionary, JSON_indent=4, out_file_path=None):
    
    """
    Function that converts a dictionary (not only its content, 
    but as a whole) to a string and writes the latter to a JSON file.
    
    Parameters 
    ----------
    dictionary : dict
            The original dictionary, no matter what structure is composed of.
    JSON_indent : int
            Determines the space to be used expressing the dictionary 
            as a string. Default value is that used widely, 
            a tab, equivalent to 4 whitespaces.
    out_file_path : str
            Output file path, could be absolute or relative.
            If not passed, default name 'dict2json.json' will be used.
            
    Returns
    -------
    Output file path in which the whole dictionary is written.    
    """
    
    # Convert dictionary  to string #
    dict_str = json.dumps(dictionary, indent=JSON_indent)
    
    # Write the string directly and at once to the given path #
    #---------------------------------------------------------#
    
    # Check whether a path is given #
    if out_file_path is None:
        out_file_path = f"dict2json.{extension}"
        
    # Check whether the path contains an extension, else add it #
    else:
        containsPathExtension = len(get_obj_specs(out_file_path, 'ext')) > 0
        if not containsPathExtension:
            out_file_path = aux_ext_adder(out_file_path, extension)

    try:
        out_file = open(out_file_path, 'w')        
    except:
        raise IOError("Could not write to file '{out_file_path}',"
                      "invalid path.")
    else:
        out_file.write(dict_str)
        
        # Get the file name's parent and the name without the relative path #        
        out_file_parent = get_obj_specs(out_file_path, obj_spec_key="parent")
        out_file_noRelPath = get_obj_specs(out_file_path, obj_spec_key="name")
        
        # Find already existing file #
        fileAlreadyExists = (len(find_fileString_paths(f"*{out_file_path}*", ".")) > 0)
        
        if fileAlreadyExists:
            overWriteStdIn\
            = input(f"Warning: file '{out_file_noRelPath}' "
                    f"at directory '{out_file_parent}' already exists.\n"
                    "Do you want to overwrite it? (y/n) ")
            
            while (overWriteStdIn != "y" and overWriteStdIn != "n"):
                overWriteStdIn = input("\nPlease select 'y' for 'yes' "
                                       "or 'n' for 'no': ")
            else:    
                if overWriteStdIn == "y":
                    out_file.close()
                else:
                    pass
                
    
    
    
def JSON2dict(in_file_path):
    """
    Function that converts a dictionary (not only its content, 
    but as a whole) to a string and writes the latter to a JSON file.
    
    Parameters 
    ----------
    input_file_path : str
            Input file path, could be absolute or relative.
               
    Returns
    -------
    content_dict : dict
            The content of the JSON file converted to a dictionary.
    """
    
    # Open the JSON file #
    try:
        in_file = open(in_file_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{in_file_path}' not found.")
    else:
        # Read the content of the file
        content_str = in_file.read()
    
    # Convert it to a dictionary #
    try:
        content_dict = json.loads(content_str)
    except:
        raise TypeError(f"Could not decode content from file '{in_file_path}'.")
    else:
        return content_dict
    
    
#--------------------------#
# Parameters and constants #
#--------------------------#

# File extensions #
extension = "json"