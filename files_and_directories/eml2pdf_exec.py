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

custom_mod_path = f"{fixed_path}/files_and_directories" 
                  
# Add the paths to the 'path' attribute of module 'sys' #
#-------------------------------------------------------#

sys.path.append(custom_mod_path)

# Perform whole or partial module importations #
#----------------------------------------------#

import file_format_tweaker

#----------------------------------------------------#
# Define imported module(s)' function call shortcuts #
#----------------------------------------------------#

eml2pdf = file_format_tweaker.eml2pdf

#-------------------------#
# Define input parameters #
#-------------------------#

path = "/home/jonander/Documents"
delete_eml_files = False

#-----------------------------#
# Convert every email message #
#-----------------------------#

eml2pdf(path, delete_eml_files)
