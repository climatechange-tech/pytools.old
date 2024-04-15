#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

from pathlib import Path
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

custom_mod1_path = f"{fixed_path}/numeral_systems"
                                        
# Add the paths to the 'path' attribute of module 'sys' #
#-------------------------------------------------------#

sys.path.append(custom_mod1_path)

# Perform whole or partial module importations #
#----------------------------------------------#

from base_converters import base2bin, bin2dec

#-------------------------#
# Define custom functions #
#-------------------------#

def bitwise_and(n1, n2):
    res_bitwise_and = n1 & n2
    res_bin = base2bin(res_bitwise_and)
    res_dec = bin2dec(res_bin)
    return (res_bin, res_dec)

def bitwise_or(n1, n2):
    res_bitwise_or = n1 | n2
    res_bin = base2bin(res_bitwise_or)
    res_dec = bin2dec(res_bin)
    return (res_bin, res_dec)

def bitwise_xor(n1, n2):
    res_bitwise_xor = n1 ^ n2
    res_bin = base2bin(res_bitwise_xor)
    res_dec = bin2dec(res_bin)
    return (res_bin, res_dec)

def rightwards_bitshift(n, despl):
    res_right_shift = n >> despl
    res_bin = base2bin(res_right_shift)
    res_dec = bin2dec(res_bin)
    return (res_bin, res_dec)

def leftards_bitshift(n, despl):
    res_left_shift = n << despl
    res_bin = base2bin(res_left_shift)
    res_dec = bin2dec(res_bin)
    return (res_bin, res_dec)
