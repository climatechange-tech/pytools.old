#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
**Note**

This program is an application of the main module 'merge_audio_and_video_main.py',
and it uses the 'merge_audio_and_video_files' attributes and/or functions.
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

custom_mod_path = f"{fixed_path}/miscellaneous"
                                        
# Add the paths to the 'path' attribute of module 'sys' #
#-------------------------------------------------------#

sys.path.append(custom_mod_path)

# Perform whole or partial module importations #
#----------------------------------------------#

from merge_audio_and_video_main import merge_audio_and_video_files

#-------------------------#
# Define input parameters #
#-------------------------#

input_video_file_list = [
    ]

# output_file_name_list = None
output_file_name_list = [
    ]

ZERO_PADDING = 1

#------------------#
# Perform the task #
#------------------#

merge_audio_and_video_files(input_video_file_list,
                            input_audio_file_list,
                            output_file_name_list=None,
                            ZERO_PADDING=ZERO_PADDING)
