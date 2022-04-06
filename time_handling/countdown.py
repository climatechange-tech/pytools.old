#----------------#
# Import modules #
#----------------#

import time

#------------------#
# Define functions #
#------------------#

def countdown_basic(t):
    while t > 0:
    
        print(t)
        t -= 1
        time.sleep(1)
        
        if t==0:
            print("Time up!")

def countdown_advanced(t):
    while t:
        minutes,seconds=divmod(t, 60)
        hours,minutes=divmod(minutes,60)

        timeformat = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        
        print(timeformat, end='\r')
        time.sleep(1)
        t -= 1
        
    print('Time up!')

t = int(input("Introduce any time in seconds: "))

countdown_advanced(t)
