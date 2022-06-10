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

emission_rcp_scenarios = ["historical", "rcp26", "rcp45", "rcp85"]