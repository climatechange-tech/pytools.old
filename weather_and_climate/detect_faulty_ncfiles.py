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

custom_mod1_path = f"{fixed_path}/time_handling"
custom_mod2_path = f"{fixed_path}/weather_and_climate"
                                        
# Add the module path to the path variable #
#------------------------------------------#

sys.path.append(custom_mod1_path)
sys.path.append(custom_mod2_path)

# Perform whole or partial module importations #
#----------------------------------------------#

from program_snippet_exec_timers import program_exec_timer
from netcdf_handler import netcdf_file_scanner

#-------------------#
# Define parameters #
#-------------------#

# Path containing string or list of strings #
path_obj = "/media/jonander/My_Basic/Dokumentuak"

# path_obj = ["/media/jonander/My_Basic/Dokumentuak"
#             "/home/jonander/Documents/03-Ikasketak]

# Switch for scanning files only at the top level of the given path(s) #
top_path_only = True

# Switch to print every file being scanned #
extra_verbose = True

#------------------------#
# Initialise the program #
#------------------------#

program_exec_timer('start')
netcdf_file_scanner(path_obj, 
                    top_path_only=top_path_only,
                    extra_verbose=extra_verbose)
    
#---------------------------------------#
# Calculate full program execution time #
#---------------------------------------#

program_exec_timer('stop')
