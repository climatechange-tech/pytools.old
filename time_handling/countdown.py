#----------------#
# Import modules #
#----------------#

from pathlib import Path
import sys

import datetime
import time

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
custom_mod2_path = f"{fixed_path}/time_handling"

# Add the module paths to the path variable #
#-------------------------------------------#

sys.path.append(custom_mod1_path)
sys.path.append(custom_mod2_path)

# Perform the module importations #
#---------------------------------#

import string_handler
import time_formatters

#----------------------------------------------------#
# Define imported module(s)´ function call shortcuts #
#----------------------------------------------------#

substring_replacer = string_handler.substring_replacer
time_format_tweaker = time_formatters.time_format_tweaker

#------------------#
# Define functions #
#------------------#

def countdown(t, string_arr1, string_arr2, 
              time_fmt_str=None, print_str=False):
    
    # if isinstance(t, str) or isinstance(t, tuple):
    if isinstance(t, str):
        time_dt = time_format_tweaker(t, time_fmt_str=time_fmt_str)
      
        if "%Y" not in time_fmt_str:
            time_dt = time_format_tweaker(t, method="model_datetime",
                                          time_fmt_str=time_fmt_str)
        
        for s2find_1, s2replace_1 in zip(string_arr1[:,0], string_arr1[:,1]):
            time_fmt_str = substring_replacer(time_fmt_str, 
                                              s2find_1, 
                                              s2replace_1)
                    
        try:
            
            zero_pad_ans = input("Would you like to include zero padding? [y/n] ")
            while zero_pad_ans != "y" and zero_pad_ans != "n":
                zero_pad_ans = input("Please write 'y' for 'yes' or 'n' for 'no' ")
                
            if zero_pad_ans == "n":
                for s2find_2, s2replace_2 in zip(string_arr2[:,0], 
                                                 string_arr2[:,1]):
                    
                    time_fmt_str = substring_replacer(time_fmt_str, 
                                                      s2find_2,
                                                      s2replace_2)
                
            while t:
                time_str = time_dt.strftime(time_fmt_str)
                print(time_str, end="\r")
                
                time.sleep(1)
                time_dt -= datetime.timedelta(seconds=1)
           
        except OverflowError:
            print("Time up!")
            
        
    elif isinstance(t, int):
        t_secs = time_format_tweaker(t)
        
        while t_secs:
            time_str = time_format_tweaker(t_secs, print_str=True)
            print(time_str, end="\r")
            
            time.sleep(1)
            t_secs -= 1
            
        print("Time up!")

#------------------#
# Local parameters #
#------------------#

# Additional parameters #
#-----------------------#

string_arr1 = np.array([["%d", "%d-1"],
                        ["%m", "%m-1"],
                        ["%Y", "%Y-1"],
                        ["%y", "%y-1"]])

string_arr2 = np.array([["%d", "%-d"],
                        ["%m", "%-m"],
                        ["%Y", "%-Y"],
                        ["%y", "%-y"]])

# Function gear #
#---------------#

t = input("Introduce any time: ")

try:
    eval(t)
    
    print_str = input("Convertible time format detected. "
                      "Would you like to print the time in string format? [y/n] ")
    
    while print_str != "y" and print_str != "n":
        print_str = input("Please write 'y' for 'yes' or 'n' for 'no' ")
            
    countdown(t, string_arr1, string_arr2, print_str=print_str)    
    
except:
    time_fmt_str = input("String format detected. "
                         "Introduce the formatting string without quotes: ")
    countdown(t, string_arr1, string_arr2, time_fmt_str=time_fmt_str)
    
    
