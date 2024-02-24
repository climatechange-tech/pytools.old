#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
**Note**

This program is an application of the main module 'file_format_tweaker.py',
and it uses the 'pdf_file_tweaker' attributes and/or functions.
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

import file_format_tweaker

#----------------------------------------------------#
# Define imported module(s)' function call shortcuts #
#----------------------------------------------------#

pdf_file_tweaker = file_format_tweaker.select_pages_from_pdf_file

#-------------------------#
# Define input parameters #
#-------------------------#

"""
As described in the original module,
the main class distinguishes among these three cases:

1. Both the path and cat string are single strings
--------------------------------------------------

In this case, a sole output file is created from a single input file.
Then in order to distinguish
between the path (WITH or WITHOUT THE EXTENSION) and 
the string to assemble or catenate pages,
the following structure is used:
f"{output_path}; {cat_string}"

The semicolon is absolutely necessary, because the function
is designed to split the string is splitted
according to that character. 
The space aroun the semicolon is not necessary and
serves only as a description.

This case is abbreviated later as 'single-single'.

2. The path is a string, and the catenation object is a dictionary
------------------------------------------------------------------

Then it is understood that several files are going to be created
from a single input file.

The dictionary has to be structured like the following:

input_path --> type string --> it corresponds this object:
{output_path_1 : cat_str_1,
 output_path_2 : cat_str_2,
             (...)        ,
 output_path_n : cat_str_n}

This case is abbreviated later as 'single-multiple'.

3. Both the path and catenation object are lists
------------------------------------------------

This is the most complete case, in which each file
is splitted into several files.
There must be a catenation object per input path,
so the structure of the case is as follows:

input_path_1 --> type string --> it corresponds this object:
{output_path_1 : cat_str_1,
 output_path_2 : cat_str_2,
             (...)        ,
 output_path_n : cat_str_n}

[...]

input_path_n --> type string --> it corresponds this object:
{output_path_n+1 : cat_str_n+1,
 output_path_n+2 : cat_str_n+2,
               (...)        ,
 output_path_n+m : cat_str_n+m}

This case is abbreviated later as 'multiple-multiple'.
"""

# Case usage switch #
case_usage = "single-single"

# Global path (if needed) #
doc_dirpath = Path(fixed_path).parent

# 1st case usage #
#----------------#

# Select case_usage = 'single-single'

# path_str = f"{doc_dirpath}/apunteak.pdf"
path_str = "/home/jonander/Documents/apunteak.pdf"

# output_path_str = f"{doc_dirpath}/tweaked.pdf"
output_path_str = "/home/jonander/Documents/tweaked.pdf"
cat_str = "1-2 8"

cat_out_str = f"{cat_str}; {output_path_str}"

# 2nd case usage #
#----------------#

# Select case_usage = 'single-multiple'

path_str = "/home/jonander/Documents/sample_1.pdf"

output_pathlist = ["output_path_1",
                   "output_path_2",
                   "output_path_3",
                   "output_path_4"]

cat_str_list = ["1-25 34-end",
                "27-30 78 79 84 76-77west",
                "36 38 31 32 56up",
                "2-endnorth"]

cat_out_dict = {out_path : cat_str 
                for out_path, cat_str in zip(output_pathlist, cat_str_list)}

# 3rd case usage #
#----------------#

# Select case_usage = 'multiple-multiple'

path_list = ["/home/jonander/Documents/sample_1.pdf",
             "Hizkuntzak/sample_2.pdf"]

output_pathlists = [
    ["output_path_1",
     "output_path_2",
     "output_path_3",
     "output_path_4"],
    
    ["output_path_5",
     "output_path_6",
     "output_path_7",
     "output_path_8"],
    ]

cat_str_lists = [
    ["1-25 34-end",
     "27-30 78 79 84 76-77west",
     "36 38 31 32 56up",
     "2-endnorth"],
    
    ["4-end",
     "24east 45",
     "83 34north 48up",
     "4east-7",
     "1-2 8"],
    ]

cat_out_dictList\
= [{out_path : cat_str 
    for out_path, cat_str in zip(output_pathlist, cat_str_list)
    for output_pathlist, cat_str_list in zip(output_pathlists, cat_str_list)}]

#------------------------------------------------------------------#
# Cut the provided files according to the catenation string object #
#------------------------------------------------------------------#

case_usage_dict = {
    "single-single" : "pdf_file_tweaker(path_str, cat_out_str)",
    "single-multiple" : "pdf_file_tweaker(path_str, cat_out_dict)",
    "multiple-multiple" : "pdf_file_tweaker(path_list, cat_out_dictList)"
    }

case_usage_options = list(case_usage_dict.keys())
if case_usage not in case_usage_options:
    raise ValueError("Wrong case usage. Options are: {case_usage_options}")
else:
    eval(case_usage_dict.get(case_usage))
