"""
This program is an application of the
module 'reorder_files_main.py'.
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

module_imp1 = "reorder_files_main.py"
module_imp1_path = f"{fixed_dirpath}/"\
                  f"files_and_directories/{module_imp1}"

spec1 = importlib.util.spec_from_file_location(module_imp1, module_imp1_path)
reorder_files_main = importlib.util.module_from_spec(spec1)
spec1.loader.exec_module(reorder_files_main)

#----------------------------------------------------#
# Define imported module(s)´ function call shortcuts #
#----------------------------------------------------#

reorder_files = reorder_files_main.reorder_files

#------------------#
# Perform the task #
#------------------#

nzeros_left = 1
extensions2skip = "swp"
file_name_splitchar = "-"

reorder_files(nzeros_left, extensions2skip)