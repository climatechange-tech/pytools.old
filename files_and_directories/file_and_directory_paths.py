#----------------#
# Import modules #
#----------------#

from pathlib import Path
import sys

import numpy as np

#-----------------------#
# Import custom modules #
#-----------------------#

# Import module that finds python tools' path #
home_PATH = Path.home()
sys.path.append(str(home_PATH))

import get_pytools_path
fixed_dirpath = get_pytools_path.return_pytools_path()

# Enumerate custom modules and their paths #
#------------------------------------------#

custom_mod_path = f"{fixed_dirpath}/strings"
                                        
# Add the module paths to the path variable #
#-------------------------------------------#

sys.path.append(custom_mod_path)

# Perform the module importations #
#---------------------------------#

import string_handler

#--------------------------------------------------#
# Define imported modules' function call shortcuts #
#--------------------------------------------------#

get_obj_specs = string_handler.get_obj_specs

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

def find_ext_file_paths(extensions, path_to_walk_in, top_path_only=False):
    
    # Function that searches for full paths containing the
    # provided extensioned files, given a path to walk in,
    # which is equivalent to the shell command 'find',
    # for the case of files.
    # 
    # Especially with 'xml' files, sometimes can happen that
    # python is not able to read the files encountered directly,
    # due to their intrinsic structure is not compatible 
    # with python interpreter standards.
    # In such cases, an attempt will be done to decode file strings
    # using charts like utf-8 or latin.
    # 
    # Parameters
    # ---------- 
    # extensions : str or list
    #       A string of the file extension or a list of extensions,
    #       WITHOUT THE POINT MARKER in any case.
    # path_to_walk_in : str
    #       String that contains the path to search for the desired files.
    # top_path_only : bool
    #       Controls whether to search for subdirectories.
    #       If True, the function will search for the given extensions
    #       only at the top of the given path,
    #       without deepening through the subdirectories.
    #        
    # Returns
    # -------
    # unique_filelist : list
    #       List containing unique paths where the
    #       selected extensions files are present.
    
    if isinstance(extensions, str):
        extensions = [extensions]
        
    if top_path_only:
        ptwi_path = posixpath_converter(path_to_walk_in, glob_bool=False)
        filelist = [str(file)
                    for file in ptwi_path.iterdir()
                    for ext in extensions
                    if file.is_file()
                    and file.suffix == f".{ext}"]
        
    else:
        ptwi_path = posixpath_converter(path_to_walk_in)
        filelist = [str(file)
                    for file in ptwi_path
                    for ext in extensions
                    if file.is_file()
                    and file.suffix == f".{ext}"]
        
    unique_filelist = list(np.unique(filelist))   
    # luf = len(unique_filelist)
    
    # if luf > 1:
    #     return unique_filelist
    # elif luf == 1:
    #     return unique_filelist[0]
    return unique_filelist
    

def find_fileString_paths(file_string, path_to_walk_in, top_path_only=False):
    
    # Function that searches for full paths containing the
    # part of the file name (i.e, file string), given a path to walk in,
    # which is equivalent to the shell command 'find',
    # for the case of files. Accepts string globbing.
    # 
    # Parameters
    # ---------- 
    # file_string : str or list
    #       A string of the string to be searched or a list of strings.
    # path_to_walk_in : str
    #       String that contains the path to search for the desired files.
    # top_path_only : bool
    #       Controls whether to search for subdirectories.
    #       If True, the function will search for the given extensions
    #       only at the top of the given path,
    #       without deepening through the subdirectories.
    # 
    # Returns
    # -------
    # unique_filelist : list
    #       List containing unique paths where the
    #       provided file strings are present.

    if isinstance(file_string, str):
        file_string = [file_string]
        
    if top_path_only:
        ptwi_path = posixpath_converter(path_to_walk_in, glob_bool=False)
        filelist = [str(file)
                    for fs in file_string
                    for file in ptwi_path.glob(f"{fs}")
                    if file.is_file()]
            
    else:
        ptwi_path = posixpath_converter(path_to_walk_in)
        ptwi_top = posixpath_converter(path_to_walk_in, glob_bool=False)
        
        filelist_main = [str(file)
                         for path in ptwi_path
                         for fs in file_string
                         for file in path.glob(f"{fs}")
                         if file.is_file()]
        
        filelist_top = [str(file)
                        for fs in file_string
                        for file in ptwi_top.glob(f"{fs}")
                        if file.is_file()]
        
        filelist = filelist_main + filelist_top
        
    unique_filelist = list(np.unique(filelist))
    # luf = len(unique_filelist)
    
    # if luf > 1:
    #     return unique_filelist
    # elif luf == 1:
    #     return unique_filelist[0]
    return unique_filelist
    

def find_allfile_extensions(extensions2skip,
                            path_to_walk_in,
                            top_path_only=False):
    
    if isinstance(extensions2skip, str):
        extensions2skip = [extensions2skip]
    
    if top_path_only:
        cwd_local = Path.cwd()
        path_to_walk_in = posixpath_converter(cwd_local, glob_bool=False)
        
        extension_list = [get_obj_specs(file, "ext")
                          for file in path_to_walk_in.iterdir()
                          if file.is_file()
                          and get_obj_specs(file, "ext")
                          and get_obj_specs(file, "ext") not in extensions2skip]

    else:
        path_to_walk_in = posixpath_converter(path_to_walk_in)
        
        extension_list = [get_obj_specs(file, "ext")
                          for file in path_to_walk_in
                          if file.is_file()
                          and get_obj_specs(file, "ext")
                          and get_obj_specs(file, "ext") not in extensions2skip]
    
    unique_extension_list = list(np.unique(extension_list))
    # luel = len(unique_extension_list)
    
    # if luel > 1:
    #     return unique_extension_list
    # elif luel == 1:
    #     return unique_extension_list[0]
    return unique_extension_list
         

# Operations involving directories as a result #
#----------------------------------------------#

def find_allDirectories(source_directory,
                        top_path_only=False,
                        include_root=True):
    
    if top_path_only:
        sd_path = posixpath_converter(source_directory, glob_bool=False)   
        
        dirfilelist = [dirc
                       for dirc in sd_path.iterdir()
                       if dirc.is_dir()]        
        # ld = len(dirfilelist)
        
        if not include_root:
            dirfilelist_noRoot = [dp.name
                                  for dp in dirfilelist]  
            
            list_udn = list(np.unique(dirfilelist_noRoot))
            # ldn = len(dirfilelist_noRoot)
            # if ldn > 1:
            #     return list(np.unique(dirfilelist_noRoot))
            # elif ldn == 1:
            #     return list(np.unique(dirfilelist_noRoot))[0]
            return list_udn
            
        else:
            list_ud = list(np.unique(dirfilelist))
            # if ld > 1:
            #     return list(np.unique(dirfilelist))
            # elif ld == 1:
            #     return list(np.unique(dirfilelist))[0]
            return list_ud
            
            
    else:
        sd_path = posixpath_converter(source_directory) 
        dirfilelist = [dirc
                       for dirc in sd_path
                       if dirc.is_dir()]
        # ld = len(dirfilelist)
        
        if not include_root:
            dirfilelist_noRoot = [dp.name
                                  for dp in dirfilelist] 
            
            list_udn = list(np.unique(dirfilelist_noRoot))
            
            # ldn = len(dirfilelist_noRoot)
            # if ldn > 1:
            #     return list(np.unique(dirfilelist_noRoot))
            # elif ldn == 1:
            #     return list(np.unique(dirfilelist_noRoot))[0]
            return list_udn
            
        else:
            list_ud = list(np.unique(dirfilelist))
            # if ld > 1:
            #     return list(np.unique(dirfilelist))
            # elif ld == 1:
            #     return list(np.unique(dirfilelist))[0]
            return list_ud
        

def find_ext_file_directories(extensions,
                              path_to_walk_in,
                              top_path_only=False):
    
    # Function that searches for directories containing the
    # provided extensioned files, given a path to walk in.
    # 
    # Parameters
    # ---------- 
    # extensions : str or list
    #       A string of the file extension or a list of extensions,
    #       WITHOUT THE POINT MARKER in any case.
    # path_to_walk_in : str
    #       String that contains the path to search for the desired files.
    # top_path_only : bool
    #       Controls whether to search for subdirectories.
    #       If True, the function will search for the given extensions
    #       only at the top of the given path,
    #       without deepening through the subdirectories.
    # 
    # Returns
    # -------
    # unique_dirlist : list
    #       List containing unique directories where the
    #       selected extensions files are present.
    
    if isinstance(extensions, str):
        extensions = [extensions]
        
    if top_path_only:
        ptwi_path = posixpath_converter(path_to_walk_in, glob_bool=False)
        dirlist = [path.parent
                   for path in ptwi_path.iterdir()
                   for ext in extensions
                   if f".{ext}" == path.suffix]

    elif not top_path_only:
        ptwi_path = posixpath_converter(path_to_walk_in)
        dirlist = [path.parent
                   for path in ptwi_path
                   for ext in extensions
                   if f".{ext}" == path.suffix]
            
    unique_dirlist = list(np.unique(dirlist))    
    # lud = len(unique_dirlist)
    
    # if lud > 1:
    #     return unique_dirlist
    # elif lud == 1:
    #     return unique_dirlist[0]
    return unique_dirlist


def find_fileString_directories(file_string,
                                path_to_walk_in,
                                top_path_only=False):
    
    # Function that searches for directories containing the
    # provided part of file names, given a path to walk in,
    # therefore it uses globbing (or main globbing, glob.glob attribute).
    #
    # There are three cases of string globbing inside the main globbing:
    #   1. The string is fixed.
    #       Then on the main globbing no asterisk is needed.
    #   2. The string has a particular beggining.
    #       Then on the main globbing the asterisk goes at the end.
    #   3. The string has a particular ending.
    #       Then on the main globbing the asterisk goes at the beggining.
    # 
    # Because these reasons and for practical purposes and simplicity,
    # the main globbing does not include any asterisk placement case,
    # so the strings are required already to have asterisks.
    # This functionality is applied to similar functions in this module.
    # 
    # Parameters
    # ---------- 
    # file_string : str or list
    #       A string of the string to be searched or a list of strings.
    # path_to_walk_in : str
    #       String that contains the path to search for the desired files.
    # top_path_only : bool
    #       Controls whether to search for subdirectories.
    #       If True, the function will search for the given extensions
    #       only at the top of the given path,
    #       without deepening through the subdirectories.
    # 
    # Returns
    # -------
    # unique_dirlist : list
    #       List containing unique directories where the
    #       provided file strings are present.
    
    if isinstance(file_string, str):
        file_string = [file_string]
    
    if top_path_only:
        ptwi_path = posixpath_converter(path_to_walk_in, glob_bool=False)
        
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
            
        ptwi_path = posixpath_converter(path_to_walk_in)
        ptwi_top = posixpath_converter(path_to_walk_in, glob_bool=False)
            
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
    # lud = len(unique_dirlist)
    
    # if lud > 1:
    #     return unique_dirlist
    # elif lud == 1:
    #     return unique_dirlist[0]
    return unique_dirlist
