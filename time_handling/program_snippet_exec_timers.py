#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

import numpy as np

from pathlib import Path

import time
import timeit
import sys

#-----------------------#
# Import custom modules #
#-----------------------#

# Find the path of the Python toolbox #
home_PATH = Path.home()
sys.path.append(str(home_PATH))

import get_pytools_path
fixed_path = get_pytools_path.return_custom_path()

# Enumerate custom modules and their paths #
#------------------------------------------#

custom_mod1_path = f"{fixed_path}/strings"
custom_mod2_path = f"{fixed_path}/time_handling"
                  
# Add the module paths to the path variable #
#-------------------------------------------#

sys.path.append(custom_mod1_path)
sys.path.append(custom_mod2_path)

# Perform whole or partial module importations #
#----------------------------------------------#

from information_output_formatters import format_string, print_format_string
from string_handler import find_substring_index
from time_formatters import time_format_tweaker

#%%

def program_exec_timer(mode, return_days=False):
    
    global ti
    
    if mode == "start":  
        ti = time.time()
        
    elif mode == "stop":
        tf = time.time()
        elapsed_time = abs(ti-tf)
        
        return time_format_tweaker(elapsed_time,
                                   return_str="extended", 
                                   return_days=return_days)
    
    
def snippet_exec_timer(snippet_str, 
                       repeats=None, 
                       trials=int(1e4), 
                       roundoff=None,
                       format_time_str=False):
    
    # Quality control #
    arg_names = snippet_exec_timer.__code__.co_varnames
        
    roundoff_arg_pos = find_substring_index("roundoff", 
                                            arg_names,
                                            advanced_search=True,
                                            find_whole_words=True)
    
    # Execution time in the specified number of trials with no repeats #
    if repeats is None:
        exec_time_norep = timeit.timeit(snippet_str,
                                        number=trials,
                                        globals=globals())
        """
        Equivalent to the following
        ---------------------------
        exec_time_norep = timeit.repeat(snippet_str, repeat=1, number=10000)[0]
        """
        
        if roundoff is not None:
            if not isinstance(roundoff, int):
                raise TypeError(format_string(typeErrorStr, '{arg_names[roundoff_arg_pos]}'))
            else:
                exec_time_norep = np.round(exec_time_norep)
                time_unit_str = sec_time_unit_str
        
        if format_time_str:
            exec_time_norep = time_format_tweaker(exec_time_norep,
                                                  return_str="extended")
            
            time_unit_str = default_time_unit_str
        
        # Complete and display the corresponding output information table #
        arg_tuple_exec_timer1 = (time_unit_str, trials, exec_time_norep)
        print_format_string(norep_exec_time_info_str, arg_tuple_exec_timer1)
      
    # Execution time in the specified number of trials for several repeats #
    else:
        exec_time_rep = timeit.repeat(snippet_str, 
                                      repeat=repeats,
                                      number=trials,
                                      globals=globals())
        
        if roundoff is not None:
            if not isinstance(roundoff, int):
                raise TypeError(format_string(typeErrorStr, '{arg_names[roundoff_arg_pos]}'))
            else:
                exec_time_rep = np.round(exec_time_rep)
                time_unit_str = sec_time_unit_str
        
        if format_time_str:
            exec_time_rep = time_format_tweaker(exec_time_rep,
                                                return_str="extended")
            
            time_unit_str = default_time_unit_str
          
        # Complete and display the corresponding output information table #
        arg_tuple_exec_timer2 = (time_unit_str, repeats, trials, exec_time_rep)
        print_format_string(rep_exec_time_info_str, arg_tuple_exec_timer2)
       
#%%

#--------------------------#
# Parameters and constants #
#--------------------------#

# Time units #
sec_time_unit_str = 's'
default_time_unit_str = 'default'

# Preformatted strings #
norep_exec_time_info_str = \
"""Snippet execution time ({}), for {} trials with no repeats: {}"""

rep_exec_time_info_str = \
"""Snippet execution time ({}), for {} trials with and {} repeats:\n{}"""

typeErrorStr = """Argument '{}' must be of type 'int'."""
