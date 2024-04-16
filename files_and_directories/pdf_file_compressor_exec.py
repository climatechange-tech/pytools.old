#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
**Note**

This program is an application of the main module 'file_format_tweaker.py',
and it uses the 'pdf_file_compressor' attributes and/or functions.
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

# Find the path of the Python toolbox #
home_PATH = Path.home()
sys.path.append(str(home_PATH))

import get_pytools_path
fixed_path = get_pytools_path.return_custom_path()

# Enumerate custom modules and their paths #
#------------------------------------------#

custom_mod_path = f"{fixed_path}/files_and_directories" 
                  
# Add the paths to the 'path' attribute of module 'sys' #
#-------------------------------------------------------#

sys.path.append(custom_mod_path)

# Perform whole or partial module importations #
#----------------------------------------------#

from file_format_tweaker import pdf_file_compressor

#-------------------#
# Define parameters #
#-------------------#

# Global path (if needed) #
doc_dirpath = Path(fixed_path).parent

# 1st case usage #
#----------------#

in_path_str  = "/home/jonander/Documents/apunteak.pdf"
out_path_str = "/home/jonander/Documents/tweaked.pdf"

# 2nd case usage #
#----------------#

in_path_list = ["/home/jonander/Documents/sample_1.pdf",
                "/home/jonander/Documents/sample_2.pdf",
                "/home/jonander/Documents/sample_3.pdf",
                "/home/jonander/Documents/sample_4.pdf"]

out_path_list = ["/home/jonander/Documents/compressed_sample1.pdf",
                 "/home/jonander/Documents/compressed_sample2.pdf",
                 "/home/jonander/Documents/compressed_sample3.pdf",
                 # None,
                 "/home/jonander/Documents/compressed_sample4.pdf",]

#-----------------------------#
# Compress the provided files #
#-----------------------------#

# pdf_file_compressor(in_path_str, out_path_str)
pdf_file_compressor(in_path_list, out_path_list)
