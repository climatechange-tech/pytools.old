#----------------#
# Import modules # 
#----------------#

import os
from pathlib import Path

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
    #   1. The string is, as the name indicates, a string.
    #       Then an attempt to find the substring along the string will be made.
    #   2. The string is a list of strings.
    #       Then the attempt will be made for each string on the list.
    # 
    # find_whole_words : bool
    #       Determines whether to find only whole words. Defaults to False.
    # 
    # Returns
    # -------
    # 
    # substr_idx_list : list or dict
    #       Object containing matching indices.
    #       It returns a list in the case of a continuous, single string.
    #       If the string is a list of string, then returns a dictionary
    #       containing the result of the search of every substring;
    #       the position of the string is identified with the keys
    #       of this dictionary.
    #       Here whether the substring is continuous or separated is redundant.
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
        lsl = len(substring)
        
        if not find_whole_words:
            if lsl == 1:
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
            if lsl == 1:
                substr_idx_list = [strng[0]
                                   for strng in enumerate(string)
                                   for el in substring
                                   if (var_idx := strng[-1].find(el)) != -1
                                   and "" in strng[-1].split(el)]
            else:
                substr_idx_list = {i :
                                   tuple(var_idx
                                         for el in substring
                                         if (var_idx := string[i].find(el)) != -1
                                         and "" in string[i].split(el))
                                   for i in range(lstr)}
                    
        lsil = len(substr_idx_list)
        if lsil == 1:
            return substr_idx_list[0]
        elif lsil > 1 :
            return substr_idx_list
        else:
            return -1


def file_path_specs(file_path, splitchar):
    
    file_PATH = Path(file_path)
    
    file_path_parent = file_PATH.parent
    file_path_name = file_PATH.stem
    file_path_name_split = file_path_name.split(splitchar)
    file_path_ext = file_PATH.suffix[1:]
    
    if "/" in file_path:
        return file_path_parent, file_path_name, file_path_name_split, file_path_ext
    else:
        return None, file_path_name, file_path_name_split, file_path_ext
    


def get_file_name_noRelPath(file_path, splitchar):
    
    file_path_parent, file_path_name, file_path_name_split, file_path_ext\
    = file_path_specs(file_path, splitchar)
        
    file_name_noRelPath = f"{file_path_name}.{file_path_ext}"

    return file_name_noRelPath

    
def create_temporal_file_name(file_path, splitchar):
    
    file_path_parent, file_path_name, file_path_name_split, file_path_ext\
    = file_path_specs(file_path, splitchar)
    
    temp_file = f"{file_path_parent}/{file_path_name}_temp.{file_path_ext}"
    temp_file_noneFiltered = noneInString_filter(temp_file)
        
    return temp_file_noneFiltered


def insert_str_into_file_name(file_path,
                              file_path_splitchar,
                              string2insert,
                              idx):
        
    file_path_parent, file_path_name, file_path_name_split, file_path_ext\
    = file_path_specs(file_path, file_path_splitchar)
    
    file_path_name_split.insert(idx, string2insert)
    file_path_name = file_path_splitchar.join(file_path_name_split)
    
    new_file_name = join_file_path_specs(file_path_parent, 
                                         file_path_name, 
                                         file_path_ext)
    
    return new_file_name


def join_file_path_specs(file_path_parent, 
                         file_path_name, 
                         file_path_ext,
                         file_path_name_joiner=None):
        
    if file_path_name_joiner is not None:
        file_path_name = file_path_name_joiner.join(file_path_name)
    
    new_file_path = f"{file_path_parent}/{file_path_name}.{file_path_ext}"
    new_file_path_noneFiltered = noneInString_filter(new_file_path)
    
    return new_file_path_noneFiltered


def file_list_2_string(file_list):

    allfile_string = ""
    for file in file_list:
        allfile_string += f"{file} "

    return allfile_string


def substring_replacer(string, string2find, string2replace):
    string_replaced = string.replace(string2find, string2replace)
    return string_replaced

    
def noneInString_filter(string):
    if "/" in string:
        string_filtered = substring_replacer(string, "None/","")
    else:
        string_filtered = substring_replacer(string, "None","")
    return string_filtered