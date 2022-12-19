"""
This program is an application of the main module netcdf_handler.py
Simply copy this script to the desired directory.
"""

#----------------#
# Import modules #
#----------------#

import importlib
from pathlib import Path

#---------------------------------------#
# Get the all-code containing directory #
#---------------------------------------#

cwd = Path.cwd()
main_path = Path("/".join(cwd.parts[:3])[1:]).glob("*/*")

fixed_dirpath = str([path
                     for path in main_path
                     if "pytools" in str(path).lower()][0])

#-----------------------#
# Import custom modules #
#-----------------------#

module_imp1 = "readable_time_displayers.py"
module_imp1_path = f"{fixed_dirpath}/"\
                   f"time_handling/{module_imp1}"

spec1 = importlib.util.spec_from_file_location(module_imp1, module_imp1_path)
readable_time_displayers = importlib.util.module_from_spec(spec1)
spec1.loader.exec_module(readable_time_displayers)


module_imp2 = "netcdf_handler.py"
module_imp2_path = f"{fixed_dirpath}/"\
                   f"weather_and_climate/{module_imp2}"

spec2 = importlib.util.spec_from_file_location(module_imp2, module_imp2_path)
netcdf_handler = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(netcdf_handler)

#----------------------------------------------------#
# Define imported module(s)´ function call shortcuts #
#----------------------------------------------------#

count_time = readable_time_displayers.count_time

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
