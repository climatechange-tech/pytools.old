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
    
    # =============================================================================
    # INPUT: KARAKTERE SOILA
    # =============================================================================

    if isinstance(string, str):
        
        substrLowestIdx = string_VS_string_search(string, substring, 
                                                  case_sensitive, all_cases, 
                                                  find_whole_words)
        
        print(substrLowestIdx)

    # =============================================================================
    # INPUT: karaktere kateen ZERRENDA, REGEXik gabe. --> EZIN DA 're' ERABILI --> REGEXak zentzugabeak
    # =============================================================================

    elif isinstance(string, list) or isinstance(string, np.ndarray):
        
        if not advanced_search:
            if isinstance(substring, str):
                substrLowestIdxNoFilt = np.char.find(string, 
                                                     substring, 
                                                     start=0,
                                                     end=None)
                
                # TODO: eman begirada bat ondokoari, np.where erabili beharko litzake ta
                substrLowestIdx = substrLowestIdxNoFilt[substrLowestIdxNoFilt != -1]
                print(substrLowestIdx)
                
           
            elif isinstance(substring, list) or isinstance(substring, np.ndarray):
                substrLowestIdx\
                = stringList_VS_stringList_search_wholeWords(string,
                                                             substring, 
                                                             start=0,
                                                             end=None)
                print(substrLowestIdx)
                    
                
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
            
    
    #%%


def string_VS_string_search(s,
                            substring,
                            find_whole_words,
                            case_sensitive,
                            all_cases):
    
    #%% TRUE BAT ERE EZ
    
    if not case_sensitive and not all_cases and not find_whole_words:
        
        firstOnlyMatch = re.search(substring, string, re.IGNORECASE)
        substrLowestIdx = firstOnlyMatch.start(0)
        
        print(substrLowestIdx)
        
    #%% TRUE BAKARRA
        
    elif case_sensitive and not all_cases and not find_whole_words:
        
        firstOnlyMatch = re.search(substring, string)
        substrLowestIdx = firstOnlyMatch.start(0)
        
        print(substrLowestIdx)
        
    elif not case_sensitive and all_cases and not find_whole_words:
        
        allMatchesIterator = re.finditer(substring, string, re.IGNORECASE)
        substrLowestIdx = [m.start(0) for m in allMatchesIterator]
        
        print(substrLowestIdx)
    
    elif not case_sensitive and not all_cases and find_whole_words:
        
        exactMatch = re.fullmatch(substring, string, re.IGNORECASE)
        substrLowestIdx = exactMatch.start(0)

        print(substrLowestIdx)
        
    #%% BI TRUE    
    
    elif case_sensitive and all_cases and not find_whole_words:
        allMatchesIterator = re.finditer(substring, string)
        substrLowestIdx = [m.start(0) for m in allMatchesIterator]
        print(substrLowestIdx)
        
    # Ondokoa zentzugabea da karaktere soilentzat, gako osoak topatu nahi badira, 
    # kasu bakarra izango baita.
    # elif not case_sensitive and all_cases and find_whole_words:
        
    elif case_sensitive and not all_cases and find_whole_words:
        exactMatch = re.fullmatch(substring, string)
        substrLowestIdx = exactMatch.start(0)
        print(substrLowestIdx)
        
    #%% TRUE GUZTIAK EZINEZKOAK DIRA
    
    # elif case_sensitive and all_cases and find_whole_words
    
    return substrLowestIdx


def stringList_VS_stringList_search_wholeWords(strList, 
                                               substrList, 
                                               start=0, 
                                               end=None):
    
    substrLowestIdxNoFilt = [np.char.find(str_el, substr_el, start=0, end=None)
                             for str_el in strList
                             for substr_el in substrList]
    
    # TODO: eman begirada bat ondokoari, np.where erabili beharko litzake ta
    substrLowestIdx = substrLowestIdxNoFilt[substrLowestIdxNoFilt != -1]
    
    return substrLowestIdx

#%%
    
#------------------------#
# Global TEST parameters #
#------------------------#

string="foijwqj83d3of8fewof" 
substring="of"  # EDO regex bat izan daiteke (ez da beharrezkoa 'regex'=True,
                # edo halakorik definitzea, hori 're' moduluarekin baitoa)

# Bilaketa aurreratuaren modua #

# Ondoko argumentuak maiusk./minusk, kasu guztiak edota hitz osoak
# bilatzeko modua aktibatu edo ez agintzen du
advanced_search = False

case_sensitive = False
all_cases = False
find_whole_words = False

idx = find_substring_index(string, 
                           substring,
                           find_whole_words=find_whole_words,
                           advanced_search=advanced_search,
                           all_cases=all_cases, 
                           case_sensitive=case_sensitive)