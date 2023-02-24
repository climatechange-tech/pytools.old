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
fixed_dirpath = get_pytools_path.return_pytools_path()

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
import faulty_ncfile_detector_main

#----------------------------------------------------#
# Define imported module(s)´ function call shortcuts #
#----------------------------------------------------#

count_time = time_formatters.count_time
netcdf_file_scanner = faulty_ncfile_detector_main.netcdf_file_scanner

#-------------------------#
# Define input parameters #
#-------------------------#

# Path containing string or list of strings #
# path_obj = "/media/jonander/My_Basic/Dokumentuak"

path_obj = "/media/jonander/My_Basic/Dokumentuak/03-Ikasketak/"\
           "02-UCM_meteorologiako_masterra/TFM/input_data"

# path_obj = ["/media/jonander/My_Basic/Dokumentuak"
#             "/home/jonander/Documents/03-Ikasketak/"]

# Switch for scanning files only at the top level of the given path(s) #
top_path_only = True

# Switch to print every file being scanned #
extra_verbose = True

#------------------------#
# Initialise the program #
#------------------------#

count_time('start')
netcdf_file_scanner(path_obj, 
                    top_path_only=top_path_only,
                    extra_verbose=extra_verbose)
    
#---------------------------------------#
# Calculate full program execution time #
#---------------------------------------#

count_time('stop')
