#----------------#
# Import modules #
#----------------#

import os

#------------------#
# Define functions #
#------------------#

def count_time(mode):
    
    if mode == "start":  
        global ti
        ti = os.times()[-1]
        
    elif mode == "stop":
        tf = os.times()[-1]
        elapsed_time = abs(ti-tf)
        readable_elapsed_time_advanced(elapsed_time)

def readable_elapsed_time_basic(t):
    hours = int(t / 3600)
    minutes  = int(int(t - 3600 * hours) / 60)
    seconds  = t - (3600 * hours + 60 * minutes)

    if hours != 0:
        res = f"Elapsed time: {hours:.0f} hours, "\
                              f"{minutes:.0f} minutes "\
                              f"{seconds:5.2f} seconds."
        
    else:
        if minutes != 0:
            res = f"Elapsed time: {minutes:.0f} minutes"\
                                  f"{seconds:5.2f} seconds."
    
    print(res)

def readable_elapsed_time_advanced(t):
    arehours = t/60/60

    if arehours > 1:
        minutes, seconds = divmod(t, 60)
        hours, minutes = divmod(minutes, 60)
        res = f"Elapsed time: {hours:.0f} hours, "\
                              f"{minutes:.0f)} minutes "\
                              f"{seconds:5.2f} seconds."
        
    else:
        minutes, seconds = divmod(t, 60)
        if minutes != 0: 
            res = f"Elapsed time: {minutes:.0f} minutes "\
                                  f"{seconds:5.2f} seconds."
        else:
            res = f"Elapsed time: {seconds:5.2f} seconds."
            
    print(res)
    
    
def readable_elapsed_time_integer(t):
    
    t_integer = int(t)
   
    hours = t_integer // 3600
    minutes = (t_integer % 3600) // 60
    seconds = t_integer % 60
    
    if hours != 0:
        res = f"Elapsed time: {hours:.0f} hours, "\
                              f"{minutes:.0f} minutes "\
                              f"{seconds:5.2f} seconds."
        
    else:
        if minutes != 0:
            res = f"Elapsed time: {minutes:.0f} minutes "\
                                  f"{seconds:5.2f} seconds."
            
    print(res)

def readable_elapsed_time_2_raw(hours, minutes, seconds):
    
    if hours < 0:
        minutes = -1 * minutes
        seconds = -1 * seconds
    
    raw_time_hours = hours + minutes/60 + seconds/3600    
    return raw_time_hours