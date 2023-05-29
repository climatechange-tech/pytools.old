#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 27 17:21:39 2023

@author: jonander
"""

import re
import numpy as np
import pandas as pd


case_sensitive = False
all_cases = False
find_whole_words = False

bilaketa_sinplea = False

s="foijwqj83d3of8fewof" 
s1="of"  # EDO regex bat izan daiteke.

# return_span=False



# =============================================================================
# FUNTZIOAK DEFINITU
# =============================================================================

def string_VS_string_search(s, s1, case_sensitive, all_cases, find_whole_words):
    
    #%% TRUE BAT ERE EZ
    
    if not case_sensitive and not all_cases and not find_whole_words:
        
        firstOnlyMatch = re.search(s1, s, re.IGNORECASE)
        substrLowestIdx = firstOnlyMatch.start(0)
        
        print(substrLowestIdx)
        
    #%% TRUE BAKARRA
        
    elif case_sensitive and not all_cases and not find_whole_words:
        
        firstOnlyMatch = re.search(s1, s)
        substrLowestIdx = firstOnlyMatch.start(0)
        
        print(substrLowestIdx)
        
    elif not case_sensitive and all_cases and not find_whole_words:
        
        allMatchesIterator = re.finditer(s1,s, re.IGNORECASE)
        substrLowestIdx = [m.start(0) for m in allMatchesIterator]
        
        print(substrLowestIdx)
    
    elif not case_sensitive and not all_cases and find_whole_words:
        
        exactMatch = re.fullmatch(s1,s, re.IGNORECASE)
        substrLowestIdx = exactMatch.start(0)

        print(substrLowestIdx)
        
    #%% BI TRUE    
    
    elif case_sensitive and all_cases and not find_whole_words:
        allMatchesIterator = re.finditer(s1,s)
        substrLowestIdx = [m.start(0) for m in allMatchesIterator]
        print(substrLowestIdx)
        
    # Ondokoa zentzugabea da karaktere soilentzat, gako osoak topatu nahi badira, 
    # kasu bakarra izango baita.
    # elif not case_sensitive and all_cases and find_whole_words:
        
    elif case_sensitive and not all_cases and find_whole_words:
        exactMatch = re.fullmatch(s1, s)
        substrLowestIdx = exactMatch.start(0)
        print(substrLowestIdx)
        
    #%% TRUE GUZTIAK EZINEZKOAK DIRA
    
    # elif case_sensitive and all_cases and find_whole_words
    
    return substrLowestIdx
#%%
    
def stringList_VS_stringList_search_wholeWords(s_list, s1_list, start=0, end=None):
    
    substrLowestIdxNoFilt = [np.char.find(s_el, s1_el, start=0, end=None)
                             for s_el in s
                             for s1_el in s1]
    
    substrLowestIdx = substrLowestIdxNoFilt[substrLowestIdxNoFilt != -1]
    
    return substrLowestIdx

# =============================================================================
# INPUT: KARAKTERE SOILA
# =============================================================================

if isinstance(s, str):
    
    substrLowestIdx = string_VS_string_search(s, s1, 
                                              case_sensitive, all_cases, 
                                              find_whole_words)
    
    print(substrLowestIdx)

# =============================================================================
# INPUT: karaktere kateen ZERRENDA, REGEXik gabe. --> EZIN DA re ERABILI --> REGEXak zentzugabeak
# =============================================================================

elif isinstance(s, list) or isinstance(s, np.ndarray):
    
    if bilaketa_sinplea:
        if isinstance(s1, str):
            substrLowestIdxNoFilt = np.char.find(s, s1, start=0, end=None)
            substrLowestIdx = substrLowestIdxNoFilt[substrLowestIdxNoFilt != -1]
            print(substrLowestIdx)
            
       
        elif isinstance(s1, list) or isinstance(s1, np.ndarray):
            substrLowestIdx\
            = stringList_VS_stringList_search_wholeWords(s, s1, start=0, end=None)
            print(substrLowestIdx)
                
            
    else:
        if isinstance(s1, str):
            substrLowestIdx = [string_VS_string_search(s_el, s1,
                                                       case_sensitive, 
                                                       all_cases, 
                                                       find_whole_words)
                               for s_el in s]
            
        elif isinstance(s1, list) or isinstance(s1, np.ndarray):
            
            substrLowestIdx\
            = stringList_VS_stringList_search_wholeWords(s, s1, start=0, end=None)
            print(substrLowestIdx)
            
        
elif isinstance(s, pd.DataFrame) or isinstance(s, pd.Series):
    try:
        substrLowestIdxNoFilt = s.str.contains[s1].index
    except:
        substrLowestIdxNoFilt = s.iloc[:,0].str.contains[s1].index
    
    substrLowestIdx = substrLowestIdxNoFilt[substrLowestIdxNoFilt]
    print(substrLowestIdx)
        