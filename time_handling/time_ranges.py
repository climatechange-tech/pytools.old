#----------------#
# Import modules #
#----------------#

import calendar
import datetime as dt

import pandas as pd


#------------------#
# Define functions #
#------------------#

def week_range(date):
    
    # Finds the week day-range, i.e, the first and last day of the week
    # where a given calendar day lies on.
    # Weeks start on Monday and end on Sunday.
    # 
    # Parameters
    # ----------
    # date : pandas._libs.tslibs.timestamps.Timestamp
    #       Timestamp format string that contains a particular date time.
    # start_date, end_date: str
    #       Pair of strings that refer, respectively, to the first and
    #       last days of the week that lies the given date within.
    
    
    # Isocalendar function #
    #----------------------#
    
    # isocalendar calculates the year, week of the year, and day of the week (dow).
    # dow is Mon = 1, Sat = 6, Sun = 7
    
    if isinstance(date, pd._libs.tslibs.timestamps.Timestamp):
        
        year, week, dow = date.isocalendar()

        # Find the first day of the week
        #-------------------------------
        
        if dow == 1:
            # Since we want to start with Monday, let's test for that condition.
            start_date = date
        else:
            # Otherwise, subtract the `dow` number days that have passed from Monday to get the first day
            start_date = date - (dt.timedelta(dow) - dt.timedelta(1))

        # Now, add 6 for the last day of the week (i.e., count up to Sunday) #
        #--------------------------------------------------------------------#
        
        end_date = start_date + dt.timedelta(6)

        return (start_date, end_date)
        
    else:
        raise ValueError("The date given is not a Timestamp") 
        
        
def nearest_leap_year(year):
    year_list = list(range(year-4, year+4))
    lyl = len(year_list)
    
    nearest_leap_year_idx = [i
                             for i in range(lyl) 
                             if calendar.isleap(year_list[i])][0]
    
    nearest_lp_year = year_list[nearest_leap_year_idx]
    return nearest_lp_year
