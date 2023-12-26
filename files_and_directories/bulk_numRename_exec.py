"""
**Note**

This program is an application of the main module 'bulk_numRename_main.py',
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

# Import module that finds python tools' path #
home_PATH = Path.home()
sys.path.append(str(home_PATH))

import get_pytools_path
fixed_path = get_pytools_path.return_custom_path()

# Enumerate custom modules and their paths #
#------------------------------------------#

custom_mod_path = f"{fixed_path}/files_and_directories"
                                        
# Add the module paths to the path variable #
#-------------------------------------------#

sys.path.append(custom_mod_path)

# Perform the module importations #
#---------------------------------#

import bulk_numRename_main

#----------------------------------------------------#
# Define imported module(s)´ function call shortcuts #
#----------------------------------------------------#

reorder_objs = bulk_numRename_main.reorder_objs

#-------------------------#
# Define input parameters #
#-------------------------#

path = "/home/jonander/Pictures/2023/Tenerife_test_rename_pytools"
obj_type = "file"

ZERO_PADDING = 3
extensions2skip = ""

starting_number = "default"
index_range = "all"

splitchar=None

#------------------#
# Perform the task #
#------------------#

reorder_objs(path,
             obj_type,
             extensions2skip,
             index_range,
             starting_number,
             ZERO_PADDING,
             splitchar=splitchar)