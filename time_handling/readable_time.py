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
    hours = int(t/3600)
    mins  = int(int(t-3600*hours)/60)
    secs  = t-(3600*hours+60*mins)

    if hours != 0:
        res = f"Elapsed time: {int(hours)} hours, {int(mins)} minutes {secs:5.2f} seconds."
        
    else:
        if mins != 0:
            res = f"Elapsed time: {int(mins)} minutes {secs:5.2f} seconds."
    
    print(res)

def readable_elapsed_time_advanced(t):
    arehours = t/60/60

    if arehours > 1:
        mins, secs = divmod(t, 60)
        hours, mins = divmod(mins, 60)
        res = f"Elapsed time: {int(hours)} hours, {int(mins)} minutes {secs:5.2f} seconds."
        
    else:
        mins, secs = divmod(t, 60)
        if mins != 0: 
            res = f"Elapsed time: {int(mins)} minutes {secs:5.2f} seconds."
        else:
            res = f"Elapsed time: {secs:5.2f} seconds."
            
    print(res)

def readable_elapsed_time_2_raw(hours, minutes, seconds):
    
    if hours < 0:
        minutes = -1*minutes
        seconds = -1*seconds
    
    raw_time_hours = hours + minutes/60 + seconds/3600    
    return raw_time_hours