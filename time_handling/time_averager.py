# Adapted from https://stackoverflow.com/questions/12033905/using-python-to-create-an-average-out-of-a-list-of-times

#----------------#
# Import modules #
#----------------#

from pathlib import Path
import sys

import datetime
import numpy as np

#-----------------------#
# Import custom modules #
#-----------------------#

# Import module that finds python tools' path #
home_PATH = Path.home()
sys.path.append(str(home_PATH))

import get_pytools_path
fixed_dirpath = get_pytools_path.return_pytools_path()

# Enumerate custom modules and their paths #
#------------------------------------------#

custom_mod_path = f"{fixed_dirpath}/time_handling"

# Add the module paths to the path variable #
#-------------------------------------------#

sys.path.append(custom_mod_path)

# Perform the module importations #
#---------------------------------#

import time_formatters

#----------------------------------------------------#
# Define imported module(s)´ function call shortcuts #
#----------------------------------------------------#

time2seconds = time_formatters.time2seconds
time_format_tweaker = time_formatters.time_format_tweaker

#------------------#
# Define functions #
#------------------#

def datetime_to_radians(x):
    # Radians are calculated using a 24-hour circle, not 12-hour, 
    # starting at north and moving clockwise.
    
    # If the given time is already a datetime.time() object,
    # skip to the next step.
    
    if isinstance(x, datetime.time):
        time_of_day = x
    else:
        time_of_day = x.time()
    
    time_tuple = (time_of_day.hour, time_of_day.minute, time_of_day.second)
    seconds_from_midnight = time2seconds(time_tuple)
    
    radians = seconds_from_midnight / (24 * 60 * 60) * 2 * np.pi
    return radians

def average_angle(angles):
    # Angles are measured in RADIANS
    x_sum = np.sum([np.sin(x) for x in angles])
    y_sum = np.sum([np.cos(x) for x in angles])
    
    x_mean = x_sum / len(angles)
    y_mean = y_sum / len(angles)
    
    return np.arctan2(x_mean, y_mean)   

def radians_to_time_of_day(x):
    # Radians are measured clockwise from north and represent time in a 24-hour circle
    seconds_from_midnight = x / (2 * np.pi) * 24 * 60 * 60
    
    # It cannot be considered the next second
    # until the decimal fraction equals to 1.
    # However in some cases due to the previous calculations using np.pi()
    # and the seconds of a whole day, the decimal fraction can
    # be almost one by an extremely small number.
    # In these cases add one second to the integer part.
    tol = 1.0e-9
    
    second_fraction_to_one\
    = abs(abs(seconds_from_midnight - int(seconds_from_midnight)) - 1)
    
    if second_fraction_to_one < tol:
        seconds_from_midnight_int = int(seconds_from_midnight) + 1
        
    else:
        seconds_from_midnight_int = int(seconds_from_midnight)
    
    # If the seconds match the next day's midnight,
    # set the hour to zero instead of 24.
    # Minutes and seconds are calculated on the 60th basis.
    hour, minute, second = time_format_tweaker(seconds_from_midnight_int)
    
    dt_time = datetime.time(hour, minute, second)
    
    return dt_time

def average_times_of_day(x):
    # input datetime.datetime array and output datetime.time value
    angles = [datetime_to_radians(y) for y in x]
    avg_angle = average_angle(angles)
    
    return radians_to_time_of_day(avg_angle)
