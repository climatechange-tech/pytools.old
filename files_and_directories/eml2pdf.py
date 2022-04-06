"""
This program is an application of the
'file_formats.py' module's 'eml2pdf' function.
Simply copy this script to the desired directory.
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

module_imp1 = "file_formats.py"
module_imp1_path = f"{fixed_dirpath}/"\
                   f"files_and_directories/{module_imp1}"

spec1 = importlib.util.spec_from_file_location(module_imp1, module_imp1_path)
file_formats = importlib.util.module_from_spec(spec1)
spec1.loader.exec_module(file_formats)

#----------------------------------------------------#
# Define imported module(s)´ function call shortcuts #
#----------------------------------------------------#

eml2pdf = file_formats.eml2pdf

#----------------------------------------------------------#
#              Convert every email message                 #
# into PDF present in the directory where this code exists #
#----------------------------------------------------------#

# Switch to control the eml extension file deletion #
delete_eml_files = False

eml2pdf(delete_eml_files)