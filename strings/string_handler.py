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

    if (isinstance(string, str) and isinstance(substring, str)):
        if advanced_search:
            substr_lowest_idx = string_vs_string_search(string, substring, 
                                                      find_whole_words,
                                                      case_sensitive,
                                                      all_matches)
        else:
            substr_lowest_idx = np.char.find(string,
                                           substring,
                                           start=0,
                                           end=None)
            

    elif ((isinstance(string, str) and isinstance(substring, list))\
    or isinstance(string, list)\
    or isinstance(string, tuple)\
    or isinstance(string, np.ndarray)):
        
        if isinstance(string, tuple):
            string = list(string)
            
        elif isinstance(string, str):
            string = [string]       
        
        if not advanced_search:
            if isinstance(substring, str):
                substr_lowest_idx_no_filter = np.char.find(string, 
                                                     substring, 
                                                     start=0,
                                                     end=None)

                substr_lowest_idx = np.where(substr_lowest_idx_no_filter!=-1)[0].tolist()
           
            elif isinstance(substring, list)\
            or isinstance(substring, tuple)\
            or isinstance(substring, np.ndarray):             
                    
                if isinstance(substring, tuple):
                    substring = list(substring)
                
                substr_lowest_idx\
                = strlist_vs_strlist_search_whole_words(string,
                                                        substring, 
                                                        start=0,
                                                        end=None)
                
        else:
            if isinstance(substring, str):
                substr_lowest_idx_no_filter\
                = np.array([string_vs_string_search(s_el, substring,
                                                    find_whole_words,
                                                    case_sensitive, 
                                                    all_matches)
                            for s_el in string])
                
                substr_lowest_idx = np.where(substr_lowest_idx_no_filter!=-1)[0].tolist()
                
                
            elif isinstance(substring, list)\
            or isinstance(substring, tuple)\
            or isinstance(substring, np.ndarray):
                
                if isinstance(substring, tuple):
                    substring = list(substring)
                
                substr_lowest_idx\
                = strlist_vs_strlist_search_whole_words(string, 
                                                        substring,
                                                        start=0, 
                                                        end=None)
             
                substr_lowest_idx_no_filter\
                = np.array([[string_vs_string_search(s_el, sb_el,
                                                     find_whole_words,
                                                     case_sensitive,
                                                     all_matches)
                             for s_el in string]
                            for sb_el in substring])
                
                substr_lowest_idx = np.where(substr_lowest_idx_no_filter!=-1)[-1].tolist()
                
            
    elif isinstance(string, (pd.DataFrame, pd.Series)):
        try:
            substr_lowest_idx_no_filter = string.str.contains[substring].index
        except:
            substr_lowest_idx_no_filter = string.iloc[:,0].str.contains[substring].index
        
        substr_lowest_idx = substr_lowest_idx_no_filter[substr_lowest_idx_no_filter]
       
    
    if isinstance(substr_lowest_idx, list) and len(substr_lowest_idx) == 0:
        return -1
    elif isinstance(substr_lowest_idx, list) and len(substr_lowest_idx) == 1:
        return substr_lowest_idx[0]
    else:
        return substr_lowest_idx
            
    
def string_vs_string_search(string,
                            substring,
                            find_whole_words,
                            case_sensitive,
                            all_matches):
    
    # No option selected #
    #--------------------#
    
    if not case_sensitive and not all_matches and not find_whole_words:
        first_only_match = re.search(substring, string, re.IGNORECASE)
        try:
            substr_lowest_idx = first_only_match.start(0)
        except:
            return -1
        else:
            return substr_lowest_idx
        
    # One option selected #
    #---------------------#
        
    elif case_sensitive and not all_matches and not find_whole_words:
        first_only_match = re.search(substring, string)
        try:
            substr_lowest_idx = first_only_match.start(0)
        except:
            return -1
        else:
            return substr_lowest_idx
        
    elif not case_sensitive and all_matches and not find_whole_words:
        allMatchesIterator = re.finditer(substring, string, re.IGNORECASE)
        try:
            substr_lowest_idx = [m.start(0) for m in allMatchesIterator]
        except:
            return -1
        else:
            return substr_lowest_idx
        
    elif not case_sensitive and not all_matches and find_whole_words:
        exactMatch = re.fullmatch(substring, string, re.IGNORECASE)
        try:
            substr_lowest_idx = exactMatch.start(0)
        except:
            return -1
        else:
            return substr_lowest_idx

    # Two options selected #
    #----------------------# 
    
    elif case_sensitive and all_matches and not find_whole_words:
        allMatchesIterator = re.finditer(substring, string)
        try:
            substr_lowest_idx = [m.start(0) for m in allMatchesIterator]
            return substr_lowest_idx
        except:
            return -1
        
    elif case_sensitive and not all_matches and find_whole_words:
        exactMatch = re.fullmatch(substring, string)
        try:
            substr_lowest_idx = exactMatch.start(0)
        except:
            return -1
        else:
            return substr_lowest_idx
    

def strlist_vs_strlist_search_whole_words(strList, 
                                          substrList, 
                                          method="default",
                                          start=0, 
                                          end=None):
 
    # Proper argument selection control #
    #-----------------------------------#
    
    arg_names = strlist_vs_strlist_search_whole_words.__code__.co_varnames
    method_arg_pos = find_substring_index(arg_names, 
                                          "method",
                                          advanced_search=True,
                                          find_whole_words=True)
    
    if method not in list_wholewords_methods:
        raise ValueError(f"Wrong '{arg_names[method_arg_pos]}' option. "
                         f"Options are {list_wholewords_methods}.")
        
    
    # Operation part #
    #----------------#
    
    if method == "default":
        try:
            substr_lowest_idx = strList.index(substrList)
        except:
            return -1    
        else:
            return substr_lowest_idx

    
    elif method == "numpy":
        substr_lowest_idx_no_filter\
        = np.array([np.char.find(strList, substr_el, start=0, end=None)
                    for substr_el in substrList])
        
        substr_lowest_idx = np.where(substr_lowest_idx_no_filter!=-1)[-1].tolist()
        if len(substr_lowest_idx) == 0:
            return -1
        else:
            return substr_lowest_idx
        
   
    
def obj_path_specs(obj_path, splitdelim=None):
    
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
    
    if splitdelim is not None:
        obj_path_name_noext_parts = obj_path_name_noext.split(splitdelim)
        addItemDict = {objSpecsKeys[3] : obj_path_name_noext_parts}
        obj_specs_dict.update(addItemDict)
        
    return obj_specs_dict


def get_obj_specs(obj_path,
                  obj_spec_key=None,
                  splitdelim=None):
    
    # Proper argument selection control #
    arg_names = get_obj_specs.__code__.co_varnames
    osk_arg_pos = find_substring_index(arg_names, 
                                       "obj_spec_key",
                                       advanced_search=True,
                                       find_whole_words=True)
    
    if obj_spec_key not in objSpecsKeys:
        raise ValueError(f"Wrong '{arg_names[osk_arg_pos]}' option. "
                         f"Options are {objSpecsKeys}.")
        
    # Get the object specification name #
    if not isinstance(obj_path, dict):
        obj_specs_dict = obj_path_specs(obj_path, splitdelim)
    
    if obj_spec_key == objSpecsKeys[3] and splitdelim is None:
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


def add_str_to_aux_path(path2tweak, str2add):
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


def file_list_to_str(obj_list):    
    method_name = inspect.currentframe().f_code.co_name
    
    if not (isinstance(obj_list, (list, np.ndarray))):
        raise TypeError(f"{method_name} method only works for lists and Numpy arrays.")
        
    else:        
        # If the Numpy array dimension is N > 1, then flatten it #
        if hasattr(obj_list, "flatten"):
            obj_list = obj_list.flatten()
    
        allobj_string = ""
        for file in obj_list:
            allobj_string += f"{file} "
    
        return allobj_string


def substring_replacer(string, string2find, string2replace, count_std=-1,
                       advanced_search=False,
                       count_adv=0,
                       flags=0):
    
    arg_names = substring_replacer.__code__.co_varnames
    adv_search_arg_pos = find_substring_index(arg_names, 
                                              "advanced_search",
                                              advanced_search=True,
                                              find_whole_words=True)
            
    if not advanced_search:
        if isinstance(string, str):
            string_replaced = string.replace(string2find, string2replace, count_std)
            
        elif isinstance(string, (list, np.ndarray)):
            if isinstance(string, list):
                string = np.array(string)
            string_replaced = np.char.replace(string, string2find, string2replace)
            
        elif isinstance(string, pd.DataFrame):
            string_replaced = pd.DataFrame.replace(string, string2find, string2replace)
            
        elif isinstance(string, pd.Series):
            string_replaced = pd.Series.replace(string, string2find, string2replace)
            
        return string_replaced
            
    else:
        if not isinstance(string, str):
            raise ValueError("Input object must only be of type 'string' "
                             f"if '{arg_names[adv_search_arg_pos]}' is True.")
        else:
            string_replaced = re.sub(string2find, string2replace, 
                                     string,
                                     count_adv,
                                     flags)
        
            return string_replaced
        
        
        
def case_modifier(string, case=None):
    
    """
    Function to modify the given string case.
    
    Parameters
    ----------
    case : {'lower', 'upper', 'capitalize' 'title'}, optional.
          Case to which modify the string's current one.
            
    Returns
    -------
    String case modified accordingly
    """
    
    if (case is None or case not in case_modifier_option_keys):
        raise ValueError("You must select a case modifying option from "
                         "the following list:\n"
                         f"{case_modifier_option_keys}")
        
    else:
        str_case_modified = eval(case_modifier_option_dict.get(case))
        return str_case_modified

    
def strip(string, strip_option='strip', chars=None):
    
    """
    Removes the white spaces -or the given substring- 
    surrounding the string, except the inner ones.
    
    Parameters
    ----------
    strip_option: {'strip', 'lstrip', 'lstrip' 'title'} or None
          Location of the white spaces or substring to strip.
          Default option is the widely used 'strip'.
            
    Returns
    -------
    String with the specified characters surrounding it removed.
    """
    
    if (strip_option is None or strip_option not in strip_option_keys):
        raise ValueError("You must select a case strip option from "
                         "the following list:\n"
                         f"{strip_option_keys}")
        
    else:
        string_stripped = eval(strip_option_dict.get(strip_option))
        return string_stripped
    

#--------------------------#
# Parameters and constants #
#--------------------------#

# Standard and essential name lists #
objSpecsKeys = ['parent', 'name', 'name_noext', 'name_noext_parts', 'ext']
objSpecsKeys_essential = objSpecsKeys[2:]

# Substring search availanble method list #
list_wholewords_methods = ['default', 'numpy']

# Switch-type dictionaries #
#--------------------------#

# String case handling #
case_modifier_option_dict = {
    'lower'      : 'string.lower()',
    'upper'      : 'string.upper()',
    'capitalize' : 'string.capitalize()',
    'title'      : 'string.title()'
    }

case_modifier_option_keys = list(case_modifier_option_dict.keys())

# String stripping #
strip_option_dict = {
    'strip'  : 'string.strip(chars)',
    'lstrip' : 'string.lstrip(chars)',
    'rstrip' : 'string.rstrip(chars)',
    }

strip_option_keys = list(strip_option_dict.keys())
