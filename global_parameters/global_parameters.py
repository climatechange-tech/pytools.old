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

basic_time_format_strs = dict(
    H="%Y-%m-%d %H:%M:%S",
    D="%Y-%m-%d",
    M="%Y-%m",
    Y="%Y"
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


emission_rcp_scenarios = ["historical", "rcp26", "rcp45", "rcp85"]