#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 30 09:44:55 2022

@author: jonander
"""

from pathlib import Path

def return_pytools_path():
    
    operations_PATH = Path.cwd()
    home_PATH = Path.home()
    
    pytools_dir = "pytools"
    lpd = len(pytools_dir)
    
    if str(home_PATH) in str(operations_PATH):
        basic_PATH = home_PATH
        
    else:
        basic_PATH_parts = operations_PATH.parts[:3]
        
        joinchar = basic_PATH_parts[0]
        basic_path= joinchar.join(basic_PATH_parts)[1:]
        basic_PATH = Path(basic_path)
        
    main_PATH = basic_PATH.glob("*/*")
    
    pytools_PATH = str([PATH
                        for PATH in main_PATH
                        if pytools_dir in str(PATH).lower()
                        and len(PATH.stem) == lpd][0])
    
    return pytools_PATH