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
    # In Europe weeks start on Monday and end on Sunday.
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
            # Otherwise, subtract the `dow` number days 
            # that have passed from Monday to get the first day.
            start_date = date - (dt.timedelta(dow) - dt.timedelta(1))

        # Now, add 6 for the last day of the week (i.e., count up to Sunday) #
        #--------------------------------------------------------------------#
        
        end_date = start_date + dt.timedelta(6)

        return (start_date, end_date)
        
    else:
        raise ValueError("The date given is not a Timestamp") 
        
        
def nearest_leap_year(year):
    
    if not calendar.isleap(year):
        year_list = list(range(year-4, year+4))
        lyl = len(year_list)
        
        nearest_leap_year_idx = [i
                                 for i in range(lyl) 
                                 if calendar.isleap(year_list[i])]
        
        min_idx = nearest_leap_year_idx[0]
        max_idx = nearest_leap_year_idx[1]
        
        min_idx_year_diff = abs(year_list[min_idx] - year)
        max_idx_year_diff = abs(year_list[max_idx] - year)
        
        if min_idx_year_diff > 1 and min_idx_year_diff != 2:
            nearest_lp_year = year_list[max_idx]
        elif max_idx_year_diff > 1 and max_idx_year_diff != 2:
            nearest_lp_year = year_list[min_idx]
        elif min_idx_year_diff == max_idx_year_diff:
            nearest_lp_year = f"{year_list[min_idx]} or {year_list[max_idx]}"
        
    else:
        nearest_lp_year = year
        
    return nearest_lp_year


def leapYear_detector(start_year, end_year, return_days=False):
    
    if isinstance(start_year, str):
        start_year = eval(start_year)
    if isinstance(end_year, str):
        end_year = eval(end_year)
    
    if return_days:
        days_per_year = [len(pd.date_range(str(year),
                                           str(year+1),
                                           inclusive="left"))
                         for year in range(start_year, end_year+1)]
        return days_per_year
        
    else:
        isLeapYear_arr = [calendar.isleap(year)
                          for year in range(start_year, end_year+1)]
        return isLeapYear_arr
    
