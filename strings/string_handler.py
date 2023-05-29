#----------------#
# Import modules # 
#----------------#

from pathlib import Path

import numpy as np

#------------------#
# Define functions #
#------------------#

def find_substring_index(string, substring, find_whole_words=False):
    
    # Function that finds substrings in a given string.
    # 
    # Parameters
    # ----------
    # string : str or list of strings
    # substring : str or list
    #       Part of the string to be found. 
    # 
    # It distinguishes two cases, together with another
    # two minor cases.
    #   1. The input string is, as the name indicates, a string.
    #       Then an attempt to find the substring along the string will be made.
    #   2. The input string is a list of strings.
    #       Then the attempt will be made for each string on the list.
    # 
    # find_whole_words : bool
    #       Determines whether to find only whole words. Defaults to False.
    # 
    # Returns
    # -------
    # 
    # substr_idx_list : int, list or dict
    #       Object containing matching indices.
    #   
    #       Three cases are distinguished
    #       -----------------------------
    # 
    #       1. The string is, as stated, a single string.
    #           Then the only result will be an integer indicating the
    #           coincidence position, else it returns -1.
    # 
    #       2. The string is actually a list of them.
    #           2.1 The substring to find is a single string.
    #               Then the result will be a list of indexes.
    #           2.2 The substring to find is a list of strings.
    #               Then the functions returns a dictionary
    #               containing the result of the search of every substring;
    #               the position of the string is identified with the keys
    #               of this dictionary.
    # 
    # Note
    # ----
    # The substring can be a continuous string, separated
    # with whitespaces or a list. In any case,
    # unless it is already a list, it will be splitted,
    # even if the substring is continuous.
    # Whatever the case it is, for a True output,
    # every substring must be found at the string.
    
    if isinstance(string, str):
        
        if isinstance(substring, str):
            substring = substring.split(" ")   
            
        if not find_whole_words:
            substr_idx_list = [var_idx
                               for el in substring
                               if (var_idx := string.find(el)) != -1]
            
        else:
            substr_idx_list = [var_idx
                               for el in substring
                               if (var_idx := string.find(el)) != -1
                               and "" in string.split(el)]
            
            
        # Assume that every substring must be found at the string #
        lsil = len(substr_idx_list)
        if lsil == 1:
            return substr_idx_list[0]
        elif lsil > 1 :
            return substr_idx_list
        else:
            return -1
        
    else:
        
        if isinstance(substring, str):
            substring = substring.split(" ")
        
        # Assume that every substring must be found at the string #
        lstr = len(string)
        lsbtr = len(substring)
        
        if not find_whole_words:
            if lsbtr == 1:
                substr_idx_list = [strng[0]
                                   for strng in enumerate(string)
                                   for el in substring
                                   if (var_idx := strng[-1].find(el)) != -1]
            else:
                substr_idx_list = {i :
                                   tuple(var_idx
                                         for el in substring
                                         if (var_idx := string[i].find(el)) != -1)
                                   for i in range(lstr)}
                    
        else:
            if lsbtr == 1:
                substr_idx_list = [strng[0]
                                   for strng in enumerate(string)
                                   for el in substring
                                   if (var_idx := strng[-1].find(el)) != -1
                                   and len(np.unique(strng[-1].split(el))) == 1]
            else:
                substr_idx_list = {i :
                                   tuple(var_idx
                                         for el in substring
                                         if (var_idx := string[i].find(el)) != -1
                                         and len(np.unique(string[i].split(el))) == 1)
                                   for i in range(lstr)}
                    
        lsil = len(substr_idx_list)
        if lsil == 1:
            return substr_idx_list[0]
        elif lsil > 1 :
            return substr_idx_list
        else:
            return -1

    
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
    
    arg_names = get_obj_specs.__code__.co_varnames
    osk_arg_pos = find_substring_index(arg_names, 
                                       "obj_spec_key",
                                       find_whole_words=True)
    
    if obj_spec_key not in objSpecsKeys_short:
        raise ValueError(f"Wrong '{arg_names[osk_arg_pos]}' option. "
                         f"Options are {objSpecsKeys_short}.")
        
    if not isinstance(obj_path, dict):
        obj_specs_dict = obj_path_specs(obj_path, splitchar)
    
    if obj_spec_key == "parent":
        osk = objSpecsKeys[0]
        
    elif obj_spec_key == "name":
        osk = objSpecsKeys[1]
    
    elif obj_spec_key == "name_noext":
        osk = objSpecsKeys[2]
        
    elif obj_spec_key == "name_noext_parts" and splitchar is not None:
        osk = objSpecsKeys[3]
        
    elif obj_spec_key == "name_noext_parts" and splitchar is None:
        raise ValueError("You must specify a string-splitting character "
                         f"if '{arg_names[osk_arg_pos]}' == {obj_spec_key}.")
        
    elif obj_spec_key == "ext":
        osk = objSpecsKeys[4]
    
    obj_spec = obj_specs_dict[osk]
    return obj_spec
    
    
def modify_obj_specs(target_path_obj,
                     obj2change,
                     new_obj=None,
                     str2add=None):
    
    # target_path_obj : str or dict
    
    arg_names = modify_obj_specs.__code__.co_varnames
    obj2ch_arg_pos = find_substring_index(arg_names, "obj2")
    
    if obj2change not in objSpecsKeys_short:
        raise ValueError(f"Wrong {arg_names[obj2ch_arg_pos]} option. "
                         "Options are {objSpecsKeys_short}.")
    
    if not isinstance(target_path_obj, dict):
        obj_specs_dict = obj_path_specs(target_path_obj)
        
    if obj2change == "name_noext_parts" and not isinstance(new_obj, tuple):
        raise ValueError("bi gauzak bete behar dira: "
                         "tupla(aldatzeko karaktere-katea, ordezkoa")
            
    if obj2change == "parent":
        osk = objSpecsKeys[0]
        
    elif obj2change == "name":
        osk = objSpecsKeys[1]
            
    elif obj2change == "name_noext":
        osk = objSpecsKeys[2]

        if str2add is not None:
            obj_specs_dict[osk] += str2add    
            lengthened_fileName = join_obj_path_specs(obj_specs_dict)
            new_obj = lengthened_fileName
        
    elif obj2change == "name_noext_parts" and isinstance(new_obj, tuple):
        osk = objSpecsKeys[2]
        name_noext = get_obj_specs(target_path_obj, osk)
        new_obj_aux = substring_replacer(name_noext, new_obj[0], new_obj[1])
        new_obj = new_obj_aux
            
    elif obj2change == "ext":
        osk = objSpecsKeys[4]

    item2updateDict = {osk : new_obj}
    obj_specs_dict.update(item2updateDict)
    
    new_obj_path_joint = join_obj_path_specs(obj_specs_dict)
    return new_obj_path_joint
        

def join_obj_path_specs(obj_specs_dict):
           
    obj_path_ext = obj_specs_dict[objSpecsKeys[-1]]
    obj_path_name_noext = obj_specs_dict[objSpecsKeys[2]]
  
    try:
        obj_path_parent = obj_specs_dict[objSpecsKeys[0]]
    except:
        obj_path_parent = None
    
    if obj_path_parent is not None:
        joint_obj_path = f"{obj_path_parent}/{obj_path_name_noext}.{obj_path_ext}"
    else:
        joint_obj_path = f"{obj_path_name_noext}.{obj_path_ext}"
        
    return joint_obj_path


def fileList2String(obj_list):

    allObjStr = ""
    for file in obj_list:
        allObjStr += f"{file} "

    return allObjStr


def substring_replacer(string, string2find, string2replace, 
                       numCoincidences="all"):
    
    arg_names = substring_replacer.__code__.co_varnames
    maxc_arg_pos = find_substring_index(arg_names, 
                                       "numCoincidences",
                                       find_whole_words=True)
    
    if not isinstance(numCoincidences, int)\
        and (isinstance(numCoincidences, str)\
        and numCoincidences != "all"):
    
    # if (not isinstance(numCoincidences, int) or (isinstance(numCoincidences, str) and numCoincidences=="all")):
            
        raise TypeError(f"Argument '{arg_names[maxc_arg_pos]}' "
                        "must either be 'all' or an integer.")
        
        
    if numCoincidences == "all":
        count = -1
    else:
        count = numCoincidences
        
    string_replaced = string.replace(string2find, string2replace, count)
    return string_replaced

#------------------#
# Local parameters #
#------------------#

objSpecsKeys = ["obj_path_parent",
                "obj_path_name", 
                "obj_path_name_noext",
                "obj_path_name_noext_parts",
                "obj_path_ext"]

objSpecsKeys_short = [substring_replacer(s, "obj_path_", "","all")
                      for s in objSpecsKeys]