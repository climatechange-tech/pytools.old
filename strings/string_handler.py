#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules # 
#----------------#

import inspect

from pathlib import Path

import numpy as np
import pandas as pd
import re

#------------------#
# Define functions #
#------------------#

def find_substring_index(string,
                         substring, 
                         advanced_search=False,
                         find_whole_words=False,
                         case_sensitive=False,
                         all_matches=False):
    
    """
    substring: str or list of str
          If 'str' then it can either be as is or a regex.
          In the latter case, there is no need to explicitly define as so,
          because it connects with Python's built-in 're' module.
    """

    if isinstance(string, str):        
        if advanced_search:
            substrLowestIdx = string_VS_string_search(string, substring, 
                                                      find_whole_words,
                                                      case_sensitive,
                                                      all_matches)
        else:
            substrLowestIdx = np.char.find(string,
                                           substring,
                                           start=0,
                                           end=None)
            

    elif isinstance(string, list)\
    or isinstance(string, tuple)\
    or isinstance(string, np.ndarray):
        
        if isinstance(string, tuple):
            string = list(string)
        
        if not advanced_search:
            if isinstance(substring, str):
                substrLowestIdxNoFilt = np.char.find(string, 
                                                     substring, 
                                                     start=0,
                                                     end=None)

                substrLowestIdx = np.where(substrLowestIdxNoFilt!=-1)[0].tolist()
           
            elif isinstance(substring, list)\
            or isinstance(substring, tuple)\
            or isinstance(substring, np.ndarray):
                
                if isinstance(substring, tuple):
                    substring = list(substring)
                
                substrLowestIdx\
                = stringList_VS_stringList_search_wholeWords(string,
                                                             substring, 
                                                             start=0,
                                                             end=None)
                
        else:
            if isinstance(substring, str):
                substrLowestIdxNoFilt\
                = np.array([string_VS_string_search(s_el, substring,
                                                    find_whole_words,
                                                    case_sensitive, 
                                                    all_matches)
                            for s_el in string])
                
                substrLowestIdx = np.where(substrLowestIdxNoFilt!=-1)[0].tolist()
                
                
            elif isinstance(substring, list)\
            or isinstance(substring, tuple)\
            or isinstance(substring, np.ndarray):
                
                if isinstance(substring, tuple):
                    substring = list(substring)
                
                substrLowestIdx\
                = stringList_VS_stringList_search_wholeWords(string, 
                                                             substring,
                                                             start=0, 
                                                             end=None)
             
                substrLowestIdxNoFilt\
                = np.array([[string_VS_string_search(s_el, sb_el,
                                                     find_whole_words,
                                                     case_sensitive,
                                                     all_matches)
                             for s_el in string]
                            for sb_el in substring])
                
                substrLowestIdx = np.where(substrLowestIdxNoFilt!=-1)[-1].tolist()
                
            
    elif isinstance(string, pd.DataFrame) or isinstance(string, pd.Series):
        try:
            substrLowestIdxNoFilt = string.str.contains[substring].index
        except:
            substrLowestIdxNoFilt = string.iloc[:,0].str.contains[substring].index
        
        substrLowestIdx = substrLowestIdxNoFilt[substrLowestIdxNoFilt]
       
    
    if isinstance(substrLowestIdx, list) and len(substrLowestIdx) == 0:
        return -1
    elif isinstance(substrLowestIdx, list) and len(substrLowestIdx) == 1:
        return substrLowestIdx[0]
    else:
        return substrLowestIdx
            
    
def string_VS_string_search(string,
                            substring,
                            find_whole_words,
                            case_sensitive,
                            all_matches):
    
    # No option selected #
    #--------------------#
    
    if not case_sensitive and not all_matches and not find_whole_words:
        firstOnlyMatch = re.search(substring, string, re.IGNORECASE)
        try:
            substrLowestIdx = firstOnlyMatch.start(0)
            return substrLowestIdx
        except:
            return -1
        
    # One option selected #
    #---------------------#
        
    elif case_sensitive and not all_matches and not find_whole_words:
        firstOnlyMatch = re.search(substring, string)
        try:
            substrLowestIdx = firstOnlyMatch.start(0)
            return substrLowestIdx
        except:
            return -1
        
    elif not case_sensitive and all_matches and not find_whole_words:
        allMatchesIterator = re.finditer(substring, string, re.IGNORECASE)
        try:
            substrLowestIdx = [m.start(0) for m in allMatchesIterator]
            return substrLowestIdx
        except:
            return -1
        
    elif not case_sensitive and not all_matches and find_whole_words:
        exactMatch = re.fullmatch(substring, string, re.IGNORECASE)
        try:
            substrLowestIdx = exactMatch.start(0)
            return substrLowestIdx
        except:
            return -1

    # Two options selected #
    #----------------------# 
    
    elif case_sensitive and all_matches and not find_whole_words:
        allMatchesIterator = re.finditer(substring, string)
        try:
            substrLowestIdx = [m.start(0) for m in allMatchesIterator]
            return substrLowestIdx
        except:
            return -1
        
    elif case_sensitive and not all_matches and find_whole_words:
        exactMatch = re.fullmatch(substring, string)
        try:
            substrLowestIdx = exactMatch.start(0)
            return substrLowestIdx
        except:
            return -1
    

def stringList_VS_stringList_search_wholeWords(strList, 
                                               substrList, 
                                               method="default",
                                               start=0, 
                                               end=None):
    
    # Proper argument selection control #
    #-----------------------------------#
    
    arg_names = stringList_VS_stringList_search_wholeWords.__code__.co_varnames
    method_arg_pos = find_substring_index(arg_names, 
                                          "method",
                                          find_whole_words=True)
    
    if method not in list_wholewords_methods:
        raise ValueError(f"Wrong '{arg_names[method_arg_pos]}' option. "
                         f"Options are {list_wholewords_methods}.")
    
    # Operation part #
    #----------------#
    
    if method == "default":
        try:
            substrLowestIdx = strList.index(substrList)
        except:
            return -1    

    
    elif method == "numpy":
        substrLowestIdxNoFilt\
        = np.array([np.char.find(strList, substr_el, start=0, end=None)
                    for substr_el in substrList])
        
        substrLowestIdx = np.where(substrLowestIdxNoFilt!=-1)[-1].tolist()
        if len(substrLowestIdx) == 0:
            return -1
        else:
            return substrLowestIdx
        
   
    
def obj_path_specs(obj_path, splitchar=None):
    
    obj_PATH = Path(obj_path)
    
    obj_path_parent = obj_PATH.parent
    obj_path_name = obj_PATH.name
    obj_path_name_noext = obj_PATH.stem
    obj_path_ext = obj_PATH.suffix[1:]
    
    obj_specs_dict = {
        objSpecsKeys[0] : obj_path_parent,
        objSpecsKeys[1] : obj_path_name,
        objSpecsKeys[2] : obj_path_name_noext,
        objSpecsKeys[4] : obj_path_ext
        }
    
    if splitchar is not None:
        obj_path_name_noext_parts = obj_path_name_noext.split(splitchar)
        addItemDict = {objSpecsKeys[3] : obj_path_name_noext_parts}
        obj_specs_dict.update(addItemDict)
        
    return obj_specs_dict


def get_obj_specs(obj_path,
                  obj_spec_key=None,
                  splitchar=None):
    
    # Proper argument selection control #
    arg_names = get_obj_specs.__code__.co_varnames
    osk_arg_pos = find_substring_index(arg_names, 
                                       "obj_spec_key",
                                       find_whole_words=True)
    
    if obj_spec_key not in objSpecsKeys:
        raise ValueError(f"Wrong '{arg_names[osk_arg_pos]}' option. "
                         f"Options are {objSpecsKeys}.")
        
    # Get the object specification name #
    if not isinstance(obj_path, dict):
        obj_specs_dict = obj_path_specs(obj_path, splitchar)
    
    if obj_spec_key == objSpecsKeys[3] and splitchar is None:
        raise ValueError("You must specify a string-splitting character "
                         f"if '{arg_names[osk_arg_pos]}' == '{obj_spec_key}'.")
    else:
        obj_spec = obj_specs_dict.get(obj_spec_key)
        return obj_spec

#%%

def modify_obj_specs(target_path_obj,
                     obj2modify,
                     new_obj=None,
                     str2add=None):
    
    """
    target_path_obj : str or dict
    """
     
    # Proper argument selection control #
    arg_names = modify_obj_specs.__code__.co_varnames
    obj2ch_arg_pos = find_substring_index(arg_names, "obj2modify")
    new_obj_arg_pos = find_substring_index(arg_names, "new_obj")
    str2add_arg_pos = find_substring_index(arg_names, "str2add")
    
    
    if obj2modify not in objSpecsKeys:
        raise ValueError(f"Wrong '{arg_names[obj2ch_arg_pos]}' option. "
                         f"Options are {objSpecsKeys}.")
    
    # Get the object specification name #
    if not isinstance(target_path_obj, dict):
        obj_specs_dict = obj_path_specs(target_path_obj)
        
    obj_spec = obj_specs_dict.get(obj2modify)
    
    if obj2modify in objSpecsKeys_essential:
        if obj2modify != objSpecsKeys_essential[1]:
            if str2add is not None:
                new_obj = obj_spec + str2add
                
        else:
            if not isinstance(new_obj, tuple):
                raise TypeError(f"If the object to modify is '{objSpecsKeys[3]}', "
                                "then the provided new object must also be of type 'tuple'")
            
            else:
                name_noext = get_obj_specs(target_path_obj, obj_spec)
                new_obj = substring_replacer(name_noext, new_obj[0], new_obj[1])
                
    else:
        if new_obj is None:
            raise ValueError(f"For '{arg_names[obj2ch_arg_pos]}' = '{obj2modify}', "
                             f"'{arg_names[str2add_arg_pos]}' argument is ambiguous; "
                             "you must provide yourself the new path object "
                             f"(argument '{arg_names[new_obj_arg_pos]}') .")
            
       
    item2updateDict = {obj2modify : new_obj}
    obj_specs_dict.update(item2updateDict)
    
    new_obj_path_joint = join_obj_path_specs(obj_specs_dict)
    return new_obj_path_joint


def aux_path_strAdd(path2tweak, str2add):
    obj2change = "name_noext"
    output_path_aux = modify_obj_specs(path2tweak, obj2change, str2add=str2add)
    return output_path_aux


def aux_ext_adder(path2tweak, extension):
    obj2change = "ext"
    path_ext = get_obj_specs(path2tweak, obj2change)
    
    if len(path_ext) == 0:
        output_path = modify_obj_specs(path2tweak, obj2change, str2add=extension)
    else:
        output_path = path2tweak
    return output_path

#%%


def join_obj_path_specs(obj_specs_dict):
           
    obj_path_ext = obj_specs_dict.get(objSpecsKeys[-1])
    obj_path_name_noext = obj_specs_dict.get(objSpecsKeys[2])
  
    try:
        obj_path_parent = obj_specs_dict.get(objSpecsKeys[0])
        joint_obj_path = f"{obj_path_parent}/{obj_path_name_noext}.{obj_path_ext}"
    except:
        obj_path_parent = None
        joint_obj_path = f"{obj_path_name_noext}.{obj_path_ext}"
        
    return joint_obj_path


def fileList2String(obj_list):    
    method_name = inspect.currentframe().f_code.co_name
    
    if not (isinstance(obj_list, list) or isinstance(obj_list, np.ndarray)):
        raise TypeError(f"{method_name} method only works for lists and Numpy arrays.")
        
    else:        
        # If the Numpy array dimension is N > 1, then flatten it #
        if hasattr(obj_list, "flatten"):
            obj_list = obj_list.flatten()
    
        allobj_string = ""
        for file in obj_list:
            allobj_string += f"{file} "
    
        return allobj_string


def substring_replacer(string, string2find, string2replace, count=-1):
    
    if isinstance(string, str):
        string_replaced = string.replace(string2find, string2replace, count)
        
    elif isinstance(string, list) or isinstance(string, np.ndarray):
        if isinstance(string, list):
            string = np.array(string)
        string_replaced = np.char.replace(string, string2find, string2replace)
        
    elif isinstance(string, pd.DataFrame):
        string_replaced = pd.DataFrame.replace(string, string2find, string2replace)
        
    elif isinstance(string, pd.Series):
        string_replaced = pd.Series.replace(string, string2find, string2replace)
    
    return string_replaced


#--------------------------#
# Parameters and constants #
#--------------------------#

# Standard and essential name lists #
objSpecsKeys = ['parent', 'name', 'name_noext', 'name_noext_parts', 'ext']
objSpecsKeys_essential = objSpecsKeys[2:]

# Substring search availanble method list #
list_wholewords_methods = ['default', 'numpy']
