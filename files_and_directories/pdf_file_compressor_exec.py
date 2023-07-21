"""
**Note**

This program is an application of the main module 'file_format_tweaker.py',
and it uses the 'pdf_file_compressor' attribute or function.
PLEASE DO NOT REDISTRIBUTE this program along any other directory,
as the module is designed to work with absolute paths.
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

custom_mod_path = f"{fixed_dirpath}/files_and_directories" 
                  
# Add the module paths to the path variable #
#-------------------------------------------#

sys.path.append(custom_mod_path)

# Perform the module importations #
#---------------------------------#

import file_format_tweaker

#----------------------------------------------------#
# Define imported module(s)´ function call shortcuts #
#----------------------------------------------------#

pdf_file_compressor = file_format_tweaker.pdf_file_compressor

#-------------------------#
# Define input parameters #
#-------------------------#

# Global path (if needed) #
doc_dirpath = Path(fixed_dirpath).parent

# 1st case usage #
#----------------#

inPathObj  = "/home/jonander/Documents/apunteak.pdf"
outPathObj = "/home/jonander/Documents/tweaked.pdf"

# 2nd case usage #
#----------------#

inPathObj = ["/home/jonander/Documents/sample_1.pdf",
             "/home/jonander/Documents/sample_2.pdf",
             "/home/jonander/Documents/sample_3.pdf",
             "/home/jonander/Documents/sample_4.pdf"]

inPathObj = ["/home/jonander/Documents/compressed_sample1.pdf",
             "/home/jonander/Documents/compressed_sample2.pdf",
             "/home/jonander/Documents/compressed_sample3.pdf",
             # None,
             "/home/jonander/Documents/compressed_sample4.pdf",]

#-----------------------------#
# Compress the provided files #
#-----------------------------#

pdf_file_compressor(inPathObj, outPathObj)
