#----------------#
# Import modules #
#----------------#

import os
from pathlib import Path
import sys

import numpy as np

#-----------------------#
# Import custom modules #
#-----------------------#

# Import module that finds python tools' path #
home_PATH = Path.home()
sys.path.append(str(home_PATH))

import get_pytools_path
fixed_path = get_pytools_path.return_custom_path()

# Enumerate custom modules and their paths #
#------------------------------------------#

custom_mod1_path = f"{fixed_path}/strings"
                                        
# Add the module paths to the path variable #
#-------------------------------------------#

sys.path.append(custom_mod1_path)

# Perform the module importations #
#---------------------------------#

import information_output_formatters

#--------------------------------------------------#
# Define imported modules' function call shortcuts #
#--------------------------------------------------#

format_string = information_output_formatters.format_string

#------------------#
# Define functions #
#------------------#

def merge_audio_and_video_files(input_video_file_list,
                                input_audio_file_list,
                                output_file_name_list=None,
                                zero_padding=1):
    
    # Check whether the compulsory lists are of the same length #
    livfl = len(input_video_file_list)
    liafl = len(input_audio_file_list)
    
    if livfl != liafl:
        raise ValueError("Input audio and video files have to be of the same length.")
    else:
        # If output file name list is not provided, create a default one #
        if output_file_name_list is None:
            output_file_name_list_default = [f"merged_video_{i:0{zero_padding+1}d}"
                                             for i in range(1, livfl+1)]
            lofnl = len(output_file_name_list_default)
        else:
            lofnl = len(output_file_name_list)
            
        length_lists = [livfl, liafl, lofnl]
        unique_lengths = np.unique(length_lists)
        lul = len(unique_lengths)
        
        if lul > 1:
            raise ValueError("All lists have to be of the same length.")
            
        # Perform the operations #
        else:
            for in_video_fn, in_audio_fn, out_video_fn in zip(input_audio_file_list,
                                                              input_audio_file_list,
                                                              output_file_name_list):
                
                arg_tuple = (in_video_fn, in_audio_fn, out_video_fn)
                merge_command = format_string(ffmpeg_merge_syntax, arg_tuple)
                os.system(merge_command)

#--------------------------#
# Parameters and constants #
#--------------------------#

# FFMPEG merge syntax #
ffmpeg_merge_syntax = "ffmpeg -i {} -i {} -c:v copy -c:a aac {}"