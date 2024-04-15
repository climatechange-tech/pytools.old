#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

from pathlib import Path
import sys

import numpy as np

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

custom_mod_path = f"{fixed_path}/strings"
                                        
# Add the paths to the 'path' attribute of module 'sys' #
#-------------------------------------------------------#

sys.path.append(custom_mod_path)

# Perform whole or partial module importations #
#----------------------------------------------#

from string_handler import get_obj_specs

#------------------#
# Define functions #
#------------------#

def posixpath_converter(path, glob_bool=True):
    
    if glob_bool:
        posixpath = Path(path).glob("**/*")
    else:
        posixpath = Path(path)
        
    return posixpath

# Operations involving files as a result #
#----------------------------------------#

def find_files_by_ext(extensions, path_to_walk_into, top_path_only=False):
    
    """
    Function that searches for absolute paths given an extension or
    list thereof, walking into a path (i.e. directory)
    which is equivalent to the shell command 'find' -including the extension-
    for the case of files.
    
    Especially with html-like files, sometimes can happen that
    python is not able to read the files encountered directly,
    due to their intrinsic structure is not compatible 
    with python interpreter standards.
    In such cases, an attempt will be done to decode file strings
    using charts like utf-8 or latin.
    
    Parameters
    ---------- 
    extensions : str or list
          A string of the file extension or a list of extensions,
          WITHOUT THE POINT MARKER in any case.
    path_to_walk_into : str
          String that contains the path to search for the desired files.
    top_path_only : bool
          Controls whether to search for subdirectories.
          If True, the function will search for the given extensions
          only at the top of the given path,
          without deepening through the subdirectories.
            
    Returns
    -------
    unique_filelist : list
          List containing unique paths where the
          selected extensions files are present.
    """
    
    if isinstance(extensions, str):
        extensions = [extensions]
        
    if top_path_only:
        ptwi_path = posixpath_converter(path_to_walk_into, glob_bool=False)
        filelist = [str(file)
                    for file in ptwi_path.iterdir()
                    for ext in extensions
                    if file.is_file()
                    and file.suffix == f".{ext}"]
        
    else:
        ptwi_path = posixpath_converter(path_to_walk_into)
        filelist = [str(file)
                    for file in ptwi_path
                    for ext in extensions
                    if file.is_file()
                    and file.suffix == f".{ext}"]
        
    unique_filelist = list(np.unique(filelist))   
    return unique_filelist
    

def find_files_by_globstring(file_string, path_to_walk_into, top_path_only=False):
    
    """
    Function that searches for absolute paths given a part of
    the file name to be searched, walking into a path (i.e. directory)
    which is equivalent to the shell command 'find'
    for the case of files. Accepts string globbing.
    
    Parameters
    ----------
    file_string : str or list
          A string of the string to be searched or a list of strings.
          It also works for complete names in case it is known.
          Because at the date it has not been implemented yet,
          for now non-relative paths (i.e. full paths) are not allowed,
          and only the ultimate file name(s) is (are) accepted.
    path_to_walk_into : str
          String that contains the path to search for the desired files.
    top_path_only : bool
          Controls whether to search for subdirectories.
          If True, the function will search for the given extensions
          only at the top of the given path,
          without deepening through subdirectories.
    
    Returns
    -------
    unique_filelist : list
          List containing unique paths where the
          provided file strings are present.
    """
    
    if isinstance(file_string, str):
        file_string = [file_string]
        
    if top_path_only:
        ptwi_path = posixpath_converter(path_to_walk_into, glob_bool=False)
        
        try:
            filelist = [str(file)
                        for fs in file_string
                        for file in ptwi_path.glob(f"{fs}")
                        if file.is_file()]
            
        except NotImplementedError:
            raise NotImplementedError("Please, for now provide a name "
                                      "without the absolute path.")
            
    else:
        ptwi_path = posixpath_converter(path_to_walk_into)
        ptwi_top = posixpath_converter(path_to_walk_into, glob_bool=False)
        
        try:
            filelist_main = [str(file)
                             for path in ptwi_path
                             for fs in file_string
                             for file in path.glob(f"{fs}")
                             if file.is_file()]
  
        except NotImplementedError:
            raise NotImplementedError("Please, for now provide a name "
                                      "without the absolute path.")
        try:
            filelist_top = [str(file)
                            for fs in file_string
                            for file in ptwi_top.glob(f"{fs}")
                            if file.is_file()]
     
        except NotImplementedError:
            raise NotImplementedError("Please, for now provide a name "
                                      "without the absolute path.")
    
        filelist = filelist_main + filelist_top
        
    unique_filelist = list(np.unique(filelist))
    return unique_filelist
    

def find_all_file_extensions(extensions2skip,
                             path_to_walk_into,
                             top_path_only=False):
    
    if isinstance(extensions2skip, str):
        extensions2skip = [extensions2skip]
    
    if top_path_only:
        cwd_local = Path.cwd()
        path_to_walk_into = posixpath_converter(cwd_local, glob_bool=False)
        
        extension_list = [get_obj_specs(file, "ext")
                          for file in path_to_walk_into.iterdir()
                          if file.is_file()
                          and get_obj_specs(file, "ext")
                          and get_obj_specs(file, "ext") not in extensions2skip]

    else:
        path_to_walk_into = posixpath_converter(path_to_walk_into)
        
        extension_list = [get_obj_specs(file, "ext")
                          for file in path_to_walk_into
                          if file.is_file()
                          and get_obj_specs(file, "ext")
                          and get_obj_specs(file, "ext") not in extensions2skip]
    
    unique_extension_list = list(np.unique(extension_list))
    return unique_extension_list
         

# Operations involving directories as a result #
#----------------------------------------------#

def find_all_directories(source_directory,
                         top_path_only=False,
                         include_root=True):
    
    if top_path_only:
        sd_path = posixpath_converter(source_directory, glob_bool=False)   
        
        dir_list = [dirc
                    for dirc in sd_path.iterdir()
                    if dirc.is_dir()]        
        
        if not include_root:
            dir_list_no_root = [dp.name
                                for dp in dir_list]  
            
            list_udn = list(np.unique(dir_list_no_root))
            return list_udn
            
        else:
            list_ud = list(np.unique(dir_list))
            return list_ud
            
            
    else:
        sd_path = posixpath_converter(source_directory) 
        dir_list = [dirc
                    for dirc in sd_path
                    if dirc.is_dir()]
    
        if not include_root:
            dir_list_no_root = [dp.name
                                for dp in dir_list] 
            
            list_udn = list(np.unique(dir_list_no_root))
            return list_udn
            
        else:
            list_ud = list(np.unique(dir_list))
            return list_ud
        

def find_file_containing_dirs_by_ext(extensions,
                                     path_to_walk_into,
                                     top_path_only=False):
    
    """
    Function that searches for directories containing the
    provided extensioned files, given a path to walk into.
    
    Parameters
    ---------- 
    extensions : str or list
          A string of the file extension or a list of extensions,
          WITHOUT THE POINT MARKER in any case.
    path_to_walk_into : str
          String that contains the path to search for the desired files.
    top_path_only : bool
          Controls whether to search for subdirectories.
          If True, the function will search for the given extensions
          only at the top of the given path,
          without deepening through the subdirectories.
    
    Returns
    -------
    unique_dirlist : list
          List containing unique directories where the
          selected extensions files are present.
    """
    
    if isinstance(extensions, str):
        extensions = [extensions]
        
    if top_path_only:
        ptwi_path = posixpath_converter(path_to_walk_into, glob_bool=False)
        dirlist = [path.parent
                   for path in ptwi_path.iterdir()
                   for ext in extensions
                   if f".{ext}" == path.suffix]

    elif not top_path_only:
        ptwi_path = posixpath_converter(path_to_walk_into)
        dirlist = [path.parent
                   for path in ptwi_path
                   for ext in extensions
                   if f".{ext}" == path.suffix]
            
    unique_dirlist = list(np.unique(dirlist))    
    return unique_dirlist


def find_file_containing_dirs_by_globstring(file_string,
                                            path_to_walk_into,
                                            top_path_only=False):
    
    """
    Function that searches for directories containing the
    provided part of file names, given a path to walk into,
    therefore it uses globbing (or main globbing, glob.glob attribute).
    
    There are three cases of string globbing inside the main globbing:
      1. The string is fixed.
          Then on the main globbing no asterisk is needed.
      2. The string has a particular beggining.
          Then on the main globbing the asterisk goes at the end.
      3. The string has a particular ending.
          Then on the main globbing the asterisk goes at the beggining.
    
    Because these reasons and for practical purposes and simplicity,
    the main globbing does not include any asterisk placement case,
    so the strings are required already to have asterisks.
    The functionality and the latter rule applies 
    for similar functions in this module.
    
    Parameters
    ---------- 
    file_string : str or list
          A string of the string to be searched or a list of strings.
    path_to_walk_into : str
          String that contains the path to search for the desired files.
    top_path_only : bool
          Controls whether to search for subdirectories.
          If True, the function will search for the given extensions
          only at the top of the given path,
          without deepening through the subdirectories.
    
    Returns
    -------
    unique_dirlist : list
          List containing unique directories where the
          provided file strings are present.
    """
    
    if isinstance(file_string, str):
        file_string = [file_string]
    
    if top_path_only:
        ptwi_path = posixpath_converter(path_to_walk_into, glob_bool=False)
        
        # Equivalent to bash command-line: find (path) -maxdepth 2
        dirlist_main = [dirc
                        for dirc in ptwi_path.iterdir()
                        for fs in file_string
                        if len(list(dirc.glob(f"{fs}"))) > 0
                        and dirc.is_dir()]
        
        # Equivalent to bash command-line: find (path) -maxdepth 1
        dirlist_top = [file
                       for fs in file_string
                       for file in ptwi_path.glob(f"{fs}")
                       if file.is_file()]
        
        dirlist_top_parent = [path.parent 
                              for path in dirlist_top]
        
        
    elif not top_path_only:
            
        ptwi_path = posixpath_converter(path_to_walk_into)
        ptwi_top = posixpath_converter(path_to_walk_into, glob_bool=False)
            
        dirlist_main = [dirc
                        for dirc in ptwi_path
                        for fs in file_string
                        if len(list(dirc.glob(f"{fs}"))) > 0
                        and dirc.is_dir()]
        
        dirlist_top = [file
                       for fs in file_string
                       for file in ptwi_top.glob(f"{fs}")
                       if file.is_file()]
            
        dirlist_top_parent = [path.parent 
                              for path in dirlist_top]
        
    dirlist = dirlist_main + dirlist_top_parent

    unique_dirlist = list(np.unique(dirlist))
    return unique_dirlist
