#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Thu Jun  9 12:14:15 2022

@author: jon ander

** DISCLAIMER **
This program serves as a module to store whatever type of parameters
that are considered as frequent use.

The parameters are organized similar as are
the directories inside "pytools" directory.
"""

#%% PHYSICAL CONCEPTS

#------#
# Time #
#------#

basic_time_format_strs = dict(
    H           = "%Y-%m-%d %H:%M:%S",
    H_NODATESEP = "%Y%m%d %H:%M:%S",
    D           = "%Y-%m-%d",
    D_NODATESEP = "%Y%m%d",
    M           = "%Y-%m",
    Y           = "%Y"
)

non_std_time_format_strs = dict(
    CFT_H = "%a %b %d %H:%M:%S %Y",
    CFT_D = "%a %b %d %Y",
    CFT_M = "%b %Y"
)

# TODO: gehitu beste batzuk

custom_time_format_strs = dict(
    CT_EXCEL_SPANISH_H       = "%d/%m/%y %H:%M:%S",
    CT_EXCEL_SPANISH_NOBAR_H = "%d%m%y %H:%M:%S",
    CT_EXCEL_SPANISH_D       = "%d/%m/%y",
    CT_EXCEL_SPANISH_NOBAR_D = "%d%m%y"
)

month_number_dict = {
    1  : "J",
    2  : "F",
    3  : "M",
    4  : "A",
    5  : "M",
    6  : "J",
    7  : "J",
    8  : "A",
    9  : "S",
    10 : "O",
    11 : "N",
    12 : "D"
}

season_timeFreq_dict = {
    1  : "Q-JAN",
    2  : "Q-FEB",
    3  : "Q-MAR",
    4  : "Q-APR",
    5  : "Q-MAY",
    6  : "Q-JUN",
    7  : "Q-JUL",
    8  : "Q-AUG",
    9  : "Q-SEP",
    10 : "Q-OCT",
    11 : "Q-NOV",
    12 : "Q-DEC"
}

MATHEMATICAL_YEAR_DAYS = 360

time_frequencies_complete = ["year", "season", "month", "day", "hour", "minute", "second"]
time_frequencies_short_1 = ["yearly", "seasonal", "monthly", "daily", "hourly"]
time_frequencies_shorter_1 = ["year", "seas", "mon", "day", "hour"]

#%% MATHEMATICAL CONCEPTS
 
#-----------------# 
# Basic operators #
#-----------------# 

basic_four_rules = ["+", "-", "*", "/"]

#%% PROGRAMMING CONCEPTS

#-------------------# 
# Operative Systems #
#-------------------# 

basic_object_types = ["file", "directory"]

#---------------------------------# 
# Widely used regular expressions #
#---------------------------------# 

regex_passwords = r"^(?=.{8,})(?=.*[a-z\s])(?=.*[A-Z\s])(?=.*\d)(?=.*[_\W]).+$"

#---------# 
# Strings #
#---------#

common_splitdelim_list = ["_", "-", ";", ",", "\n", "\t"]


#%% SOCIO-ECONOMICAL CONCEPTS

#----------------# 
# Climate change #
#----------------# 

emission_rcp_scenarios = ["historical", "rcp26", "rcp45", "rcp85"]
