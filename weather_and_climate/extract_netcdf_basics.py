"""
This program is an application of the main module netcdf_handler.py
Simply copy this script to the desired directory.
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

custom_mod1_path = f"{fixed_path}/time_handling"
custom_mod2_path = f"{fixed_path}/weather_and_climate"

                                        
# Add the module path to the path variable #
#------------------------------------------#

sys.path.append(custom_mod1_path)
sys.path.append(custom_mod2_path)

# Perform the module importations #
#---------------------------------#

import program_snippet_exec_timers
import netcdf_handler

#----------------------------------------------------#
# Define imported module(s)´ function call shortcuts #
#----------------------------------------------------#

program_exec_timer = program_snippet_exec_timers.program_exec_timer

extract_and_store_latlon_bounds = netcdf_handler.extract_and_store_latlon_bounds 
extract_and_store_period_bounds = netcdf_handler.extract_and_store_period_bounds
extract_and_store_time_formats = netcdf_handler.extract_and_store_time_formats

#-------------------#
# Start the program #
#-------------------#

program_exec_timer("start")


#------------------#
# Input parameters #
#------------------#

# Delta and value roundoffs for coordinate values #
DELTA_ROUNDOFF = 3
VALUE_ROUNDOFF = 5

#-----------------------------------------------------------------------#
# Extract every netCDF file´s basic information present in this project #
#-----------------------------------------------------------------------#

extract_and_store_latlon_bounds(DELTA_ROUNDOFF, VALUE_ROUNDOFF)
extract_and_store_period_bounds()
extract_and_store_time_formats()

#-----------------------------------------------#
# Calculate the elapsed time for full execution #
#-----------------------------------------------#

program_exec_timer("stop")
