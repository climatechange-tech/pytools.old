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

from file_format_tweaker import msg2pdf

#-------------------#
# Define parameters #
#-------------------#

path = "/home/jonander/Documents"

delete_msg_files = False
delete_eml_files = False

#------------------------------------------#
# Convert every Microsoft Outlook message  #
#------------------------------------------#

msg2pdf(path, delete_msg_files, delete_eml_files)