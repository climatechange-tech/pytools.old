#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 19:17:36 2022

@author: jonander
"""

# Adapted from https://stackoverflow.com/questions/12033905/using-python-to-create-an-average-out-of-a-list-of-times

import datetime
import numpy as np

def datetime_to_radians(x):    
    # Radians are calculated using a 24-hour circle, not 12-hour, 
    # starting at north and moving clockwise.
    
    # If the time given is already a datetime.time() object,
    # skip to the next step
    
    if isinstance(x, datetime.time):
        time_of_day = x
    else:
        time_of_day = x.time()
    
    seconds_from_midnight = 3600 * time_of_day.hour + \
                            60 * time_of_day.minute + \
                            time_of_day.second
                            
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
    hour = (seconds_from_midnight_int // 3600) % 24
    minute = (seconds_from_midnight_int % 3600) // 60
    second = seconds_from_midnight_int % 60
    
    return datetime.time(hour, minute, second)

def average_times_of_day(x):
    # input datetime.datetime array and output datetime.time value
    angles = [datetime_to_radians(y) for y in x]
    avg_angle = average_angle(angles)
    
    return radians_to_time_of_day(avg_angle)
