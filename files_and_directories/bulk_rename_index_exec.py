#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
**Note**

This program is an application of the main module 'bulk_rename_index_main.py',
and it uses the 'reorder_objs' attributes and/or functions.
PLEASE DO NOT REDISTRIBUTE this program along any other directory,
as the module is designed to work with absolute paths.
"""

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

custom_mod_path = f"{fixed_path}/files_and_directories"
                                        
# Add the paths to the 'path' attribute of module 'sys' #
#-------------------------------------------------------#

sys.path.append(custom_mod_path)

# Perform whole or partial module importations #
#----------------------------------------------#

import bulk_rename_index_main

#----------------------------------------------------#
# Define imported module(s)' function call shortcuts #
#----------------------------------------------------#

reorder_objs = bulk_rename_index_main.reorder_objs

#-------------------#
# Define parameters #
#-------------------#

path = "/home/jonander/Pictures/2023/Tenerife_test_rename_pytools"
obj_type = "file"

ZERO_PADDING = 3
extensions2skip = ""

starting_number = "default"
index_range = "all"

splitdelim = None

#------------------#
# Perform the task #
#------------------#

reorder_objs(path,
             obj_type,
             extensions2skip,
             index_range,
             starting_number,
             ZERO_PADDING,
             splitdelim=splitdelim)
