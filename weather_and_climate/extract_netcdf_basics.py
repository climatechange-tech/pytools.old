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
fixed_dirpath = get_pytools_path.return_custom_path()

# Enumerate custom modules and their paths #
#------------------------------------------#

custom_mod1_path = f"{fixed_dirpath}/time_handling"
custom_mod2_path = f"{fixed_dirpath}/weather_and_climate"

                                        
# Add the module path to the path variable #
#------------------------------------------#

sys.path.append(custom_mod1_path)
sys.path.append(custom_mod2_path)

# Perform the module importations #
#---------------------------------#

import time_formatters
import netcdf_handler

#----------------------------------------------------#
# Define imported module(s)´ function call shortcuts #
#----------------------------------------------------#

count_time = time_formatters.count_time

extract_and_store_latlon_bounds = netcdf_handler.extract_and_store_latlon_bounds 
extract_and_store_period_bounds = netcdf_handler.extract_and_store_period_bounds
extract_and_store_time_formats = netcdf_handler.extract_and_store_time_formats

#-------------------#
# Start the program #
#-------------------#

count_time("start")

#-----------------------------------------------------------------------#
# Extract every netCDF file´s basic information present in this project #
#-----------------------------------------------------------------------#

# Define the delta and value roundoffs for coordinate values #
delta_roundoff = 3
value_roundoff = 5

extract_and_store_latlon_bounds(delta_roundoff, value_roundoff)
extract_and_store_period_bounds()
extract_and_store_time_formats()

#-----------------------------------------------#
# Calculate the elapsed time for full execution #
#-----------------------------------------------#

count_time("stop")
