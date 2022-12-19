"""
This is an application of the general program 'faulty_ncfile_detector.py'.
Simply copy this script on the desired directory.
"""
#----------------#
# Import modules #
#----------------#

import importlib
from pathlib import Path

#---------------------------#
# Get the fixed directories #
#---------------------------#

cwd = Path.cwd()
main_path = Path("/".join(cwd.parts[:3])[1:]).glob("*/*")

# All-code containing directory #
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


module_imp2 = "faulty_ncfile_detector.py"
module_imp2_path = f"{fixed_dirpath}/"\
                   f"weather_and_climate/{module_imp2}"
                   
spec2 = importlib.util.spec_from_file_location(module_imp2, module_imp2_path)
faulty_ncfile_detector = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(faulty_ncfile_detector)

#----------------------------------------------------#
# Define imported module(s)´ function call shortcuts #
#----------------------------------------------------#

count_time = readable_time_displayers.count_time
return_faulty_files = faulty_ncfile_detector.return_faulty_files

#------------------------#
# Initialise the program #
#------------------------#

count_time('start')

#-------------------------------------------------------#
# Scan for faulty netCDF files in the current directory #
#-------------------------------------------------------#

return_faulty_files()
    
#---------------------------------------#
# Calculate full program execution time #
#---------------------------------------#

count_time('stop')
