#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  3 18:59:55 2023

@author: jonander
"""

#----------------#
# Import modules #
#----------------#

import re
import numpy as np
import pandas as pd

#------------------#
# Define functions #
#------------------#

def find_substring_index(string,
                         substring, 
                         find_whole_words=False,
                         advanced_search=False,
                         case_sensitive=False,
                         all_cases=False):
    
    # substring: str or list of str
    #       If 'str' then it can either be as is or a regex.
    #       In the latter case, there is no need to explicitly define as so,
    #       because it connects with Python's built-in 're' module.

    if isinstance(string, str):
        substrLowestIdx = string_VS_string_search(string, substring, 
                                                  case_sensitive, all_cases, 
                                                  find_whole_words)

    elif isinstance(string, list) or isinstance(string, np.ndarray):
        
        if not advanced_search:
            if isinstance(substring, str):
                substrLowestIdxNoFilt = np.char.find(string, 
                                                     substring, 
                                                     start=0,
                                                     end=None)
                
                substrLowestIdx = np.where(substrLowestIdxNoFilt!=-1)[0].tolist()
                print(substrLowestIdx)
                
           
            elif isinstance(substring, list) or isinstance(substring, np.ndarray):
                substrLowestIdx\
                = stringList_VS_stringList_search_wholeWords(string,
                                                             substring, 
                                                             start=0,
                                                             end=None)
                
        else:
            if isinstance(substring, str):
                substrLowestIdx = [string_VS_string_search(s_el, substring,
                                                           case_sensitive, 
                                                           all_cases, 
                                                           find_whole_words)
                                   for s_el in string]
                
            elif isinstance(substring, list) or isinstance(substring, np.ndarray):
                
                substrLowestIdx\
                = stringList_VS_stringList_search_wholeWords(string, 
                                                             substring,
                                                             start=0, 
                                                             end=None)
                print(substrLowestIdx)
                
            
    elif isinstance(string, pd.DataFrame) or isinstance(string, pd.Series):
        try:
            substrLowestIdxNoFilt = string.str.contains[substring].index
        except:
            substrLowestIdxNoFilt = string.iloc[:,0].str.contains[substring].index
        
        substrLowestIdx = substrLowestIdxNoFilt[substrLowestIdxNoFilt]
        print(substrLowestIdx)
        
    return substrLowestIdx
            

def string_VS_string_search(string,
                            substring,
                            find_whole_words,
                            case_sensitive,
                            all_cases):
    
    # No option selected #
    #--------------------#
    
    if not case_sensitive and not all_cases and not find_whole_words:
        firstOnlyMatch = re.search(substring, string, re.IGNORECASE)
        substrLowestIdx = firstOnlyMatch.start(0)
        
    # One option selected #
    #---------------------#
        
    elif case_sensitive and not all_cases and not find_whole_words:
        firstOnlyMatch = re.search(substring, string)
        substrLowestIdx = firstOnlyMatch.start(0)
        
    elif not case_sensitive and all_cases and not find_whole_words:
        allMatchesIterator = re.finditer(substring, string, re.IGNORECASE)
        substrLowestIdx = [m.start(0) for m in allMatchesIterator]
        
    elif not case_sensitive and not all_cases and find_whole_words:
        exactMatch = re.fullmatch(substring, string, re.IGNORECASE)
        substrLowestIdx = exactMatch.start(0)

    # Two options selected #
    #----------------------# 
    
    elif case_sensitive and all_cases and not find_whole_words:
        allMatchesIterator = re.finditer(substring, string)
        substrLowestIdx = [m.start(0) for m in allMatchesIterator]
        
    elif case_sensitive and not all_cases and find_whole_words:
        exactMatch = re.fullmatch(substring, string)
        substrLowestIdx = exactMatch.start(0)
    
    return substrLowestIdx


def stringList_VS_stringList_search_wholeWords(strList, 
                                               substrList, 
                                               start=0, 
                                               end=None):
    
    substrLowestIdxNoFilt\
    = np.array([np.char.find(strList, substr_el, start=0, end=None)
                for substr_el in substrList])
    
    substrLowestIdx = np.where(substrLowestIdxNoFilt!=-1)[-1].tolist()
    return substrLowestIdx