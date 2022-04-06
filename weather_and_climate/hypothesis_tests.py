#----------------#
# Import modules #
#----------------#

import importlib
from pathlib import Path

import numpy as np
import pandas as pd

import scipy.signal as ssig
import scipy.stats as ss
from scipy.cluster.vq import whiten

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

module_imp1 = "netcdf_handler.py"
module_imp1_path = f"{fixed_dirpath}/"\
                   f"weather_and_climate/{module_imp1}"

spec1 = importlib.util.spec_from_file_location(module_imp1, module_imp1_path)
netcdf_handler = importlib.util.module_from_spec(spec1)
spec1.loader.exec_module(netcdf_handler)


module_imp2 = "array_numerical_operations.py"
module_imp2_path = f"{fixed_dirpath}/"\
                   f"arrays_and_lists/{module_imp2}"

spec2 = importlib.util.spec_from_file_location(module_imp2, module_imp2_path)
array_numerical_operations = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(array_numerical_operations)

#----------------------------------------------------#
# Define imported module(s)´ function call shortcuts #
#----------------------------------------------------#

# file_path_specs = string_handler.file_path_specs
# join_file_path_specs = string_handler.join_file_path_specs

# move_files_byFS_fromCodeCallDir = file_handler.move_files_byFS_fromCodeCallDir

# find_ext_file_paths = file_and_directory_paths.find_ext_file_paths
# find_ext_file_directories = file_and_directory_paths.find_ext_file_directories

# binary_faulty_file_detector = faulty_ncfile_detector.binary_faulty_file_detector

#------------------#
# Define functions #
#------------------#


# TODO: batez ere LIFE proiektuan aurrera egin ahala joan definitzen OINARRIZKOAK
