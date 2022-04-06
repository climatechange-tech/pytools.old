"""
This program is an application of the
'file_formats.py' module's 'select_pages_from_pdf_file' function.
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


module_imp2 = "file_and_directory_paths.py"
module_imp2_path = f"{fixed_dirpath}/"\
                   f"files_and_directories/{module_imp2}"
                   
spec2 = importlib.util.spec_from_file_location(module_imp2, module_imp2_path)
file_and_directory_paths = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(file_and_directory_paths)

#----------------------------------------------------#
# Define imported module(s)´ function call shortcuts #
#----------------------------------------------------#

find_ext_file_paths = file_and_directory_paths.find_ext_file_paths
find_fileString_paths = file_and_directory_paths.find_fileString_paths
select_pages_from_pdf_file = file_formats.select_pages_from_pdf_file

#-----------------------------#
# Define the input parameters #
#-----------------------------#

"""
In the main class, it is assumed that generally
the user wants either to specify a single or several files to operate with, 
or perform an operation with string- or extension-matching files.

Then three options are available in this section:
    
·1: specify several files manually.
·2: provide a file string and find matches.
·3: provide a file extension and find matches.
"""

files = []

# extension = "pdf"
# files = find_ext_file_paths(extension, None, top_path_only=True)

# file_string = ""
# files = find_fileString_paths(extension, None, top_path_only=True)


pages = "1-2 8"
cut_recursively = False

#---------------------------------------------------------------#
# Cut the provided files according to the page selection string #
#---------------------------------------------------------------#

select_pages_from_pdf_file(files, pages, cut_recursively)
