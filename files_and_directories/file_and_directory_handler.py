#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

import os
from pathlib import Path
import shutil
import sys

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

custom_mod1_path = f"{fixed_path}/files_and_directories"
custom_mod2_path = f"{fixed_path}/operative_systems"
                                        
# Add the module paths to the path variable #
#-------------------------------------------#

sys.path.append(custom_mod1_path)
sys.path.append(custom_mod2_path)

# Perform whole or partial module importations #
#----------------------------------------------#

from file_and_directory_paths import posixpath_converter
import information_output_formatters
from os_operations import exec_shell_command

#----------------------------------------------------#
# Define imported module(s)' function call shortcuts #
#----------------------------------------------------#

print_format_string = information_output_formatters.print_format_string
format_string = information_output_formatters.format_string

#------------------#
# Define functions #
#------------------#

# Operations involving files #
#----------------------------#

def move_files_byExts_fromCodeCallDir(extensions, destination_directories):
    
    """
    Function that moves files selected by extensions,
    from the directory that this code is called
    to the desired directory or directories.
    
    Parameters
    ----------
    extensions : str or list
          A string of the file extension or a list of extensions,
          WITHOUT THE POINT MARKER in any case.
    destination_directories : str or list
          A string of the directory name or a list
          containing several directories where to move the matching files.
    
    This function distinguishes four cases:
    
      1. Both file names and directories are lists.
              Then it is understood that each extensioned file
              corresponds to a single directory (it is physically impossible to
              move files to multiple directories other than copying them),
              and it is moved to the aforementioned directory.
              File and directory lists have to be of the same length;
              throws and error otherwise.
      2. The extensions are contained in a list but there is
          a single directory.
              Then the matching files will be moved to that directory.
      3. The extension is a string and directories are contained in a list.
              Then the single-extension matching files will be
              moved to each of the directories.
      4. None of them are lists.
              Then the matching files will simply be moved to that directory.
    """
    
    if isinstance(extensions, list)\
    and isinstance(destination_directories, list):
        
        len_exts = len(extensions)
        len_dds = len(destination_directories)
        
        if len_exts != len_dds:
            raise ValueError(format_string(notEqualLengthErrorStr, arg_tuple_exts_dirs))
        else:
            for ext, dd in zip(extensions, destination_directories):
                extension_allfiles = cwd.glob(f"*.{ext}")
                
                for file in extension_allfiles:
                    file_name_nopath = file.name
                    shutil.move(file, f"{dd}/{file_name_nopath}")
                
    elif isinstance(extensions, list)\
    and not isinstance(destination_directories, list):
        
        for ext in extensions:
            
            extension_allfiles = cwd.glob(f"*.{ext}")
            
            for file in extension_allfiles:
                file_name_nopath = file.name
                shutil.move(file, f"{destination_directories}/{file_name_nopath}")
                
    elif not isinstance(extensions, list)\
    and isinstance(destination_directories, list):
        
        extension_allfiles = cwd.glob(f"*.{extensions}")
        
        for dd in destination_directories:
            for file in extension_allfiles:
                file_name_nopath = file.name
                shutil.move(file, f"{dd}/{file_name_nopath}")           
                
    else:
        extension_allfiles = cwd.glob(f"*.{extensions}") 
        
        for file in extension_allfiles:
            file_name_nopath = file.name
            shutil.move(file, f"{destination_directories}/{file_name_nopath}")


def move_files_byFS_fromCodeCallDir(file_strings, destination_directories):

    """
    Function that moves files selected by part of the file name,
    from the directory that this code is called
    to the desired directory or directories.
    It uses name globbing (or main globbing, Path(path).glob attribute).
    
    There are four cases of string globbing inside the main globbing:
      1. The string is fixed.
          Then on the main globbing no asterisk is needed.
      2. The string has a particular beggining.
          Then on the main globbing the asterisk goes at the end.
      3. The string has a particular ending.
          Then on the main globbing the asterisk goes at the beggining.
      4. The string is composed by several particular substrings.
          Several asterisks are placed along the string.
    
    Because these reasons and for practical purposes and simplicity,
    the main globbing does not include any asterisk placement case,
    so the strings are required already to have asterisks.
    This functionality is applied to similar functions in this module.
    
    Parameters
    ----------
    file_strings : str or list
          String or list of strings that identify the desired files.
          Accepts file name extension globbing.
    destination_directories : str or list
          A string of the directory name or a list
          containing several directories where to move the matching files.
    
    This function distinguishes four cases:
    
      1. Both file names and directories are lists.
              Then it is understood that each extensioned file
              corresponds to a single directory (it is physically impossible to
              move files to multiple directories other than copying them),
              and it is moved to the aforementioned directory.
              File and directory lists have to be of the same length;
              throws and error otherwise.
      2. The extensions are contained in a list but there is
          a single directory.
              Then the matching files will be moved to that directory.
      3. The extension is a string and directories are contained in a list.
              Then the single-extension matching files will be
              moved to each of the directories.
      4. None of them are lists.
              Then the matching files will simply be moved to that directory.
    """
    
    if isinstance(file_strings, list)\
    and isinstance(destination_directories, list):
        
        len_fs = len(file_strings)
        len_dds = len(destination_directories)
        
        if len_fs != len_dds:
            raise ValueError(format_string(notEqualLengthErrorStr, arg_tuple_FS_dirs))
        else:
            for fs, dd in zip(file_strings, destination_directories):
                string_allfiles = [file
                                   for file in cwd.glob(fs)
                                   if file.is_file()]
                
                for file in string_allfiles:
                    file_name_nopath = file.name
                    shutil.move(file, f"{dd}/{file_name_nopath}")

    elif isinstance(file_strings, list)\
    and not isinstance(destination_directories, list):
        
        for fs in file_strings:
            string_allfiles = [file
                               for file in cwd.glob(fs)
                               if file.is_file()]
            
            for file in string_allfiles:
                file_name_nopath = file.name
                shutil.move(file, f"{destination_directories}/{file_name_nopath}")
 
    elif not isinstance(file_strings, list)\
    and isinstance(destination_directories, list):
        
        string_allfiles = [file
                           for file in cwd.glob(f"{file_strings}")
                           if file.is_file()]
        
        for dd in destination_directories:
            for file in string_allfiles:
                file_name_nopath = file.name
                shutil.move(file, f"{dd}/{file_name_nopath}")           

    else:
        string_allfiles = [file
                           for file in cwd.glob(f"{file_strings}")
                           if file.is_file()]
        
        for file in string_allfiles:
            file_name_nopath = file.name
            shutil.move(file, f"{destination_directories}/{file_name_nopath}")
            

def move_files(source_files, destination_directories):
    
    source_files = [posixpath_converter(sf, glob_bool=False)
                    for sf in source_files]
    
    if isinstance(source_files, list)\
    and isinstance(destination_directories, list):
        
        for sf, dd in zip(source_files, destination_directories):
            file_name_nopath = sf.name
            shutil.move(sf, f"{dd}/{file_name_nopath}")
            
    elif isinstance(source_files, list)\
    and not isinstance(destination_directories, list):
        
        for sf in source_files:
            file_name_nopath = sf.name
            shutil.move(sf, f"{destination_directories}/{file_name_nopath}")
    
    elif not isinstance(source_files, list)\
    and isinstance(destination_directories, list):
        
        for dd in destination_directories:
            file_name_nopath = source_files.name
            shutil.move(source_files, f"{dd}/{file_name_nopath}")
            
    elif not isinstance(source_files, list)\
    and not isinstance(destination_directories, list):
        
        file_name_nopath = source_files.name
        shutil.move(source_files, f"{destination_directories}/{file_name_nopath}")
        
        
def copy_files(source_files, destination_directories):
    
    source_files = [posixpath_converter(sf, glob_bool=False)
                    for sf in source_files]
    
    if isinstance(source_files, list)\
    and isinstance(destination_directories, list):
        
        for sf, dd in zip(source_files, destination_directories):
            file_name_nopath = sf.name
            shutil.copy(sf, f"{dd}/{file_name_nopath}")
            
    elif isinstance(source_files, list)\
    and not isinstance(destination_directories, list):
        
        for sf in source_files:
            file_name_nopath = sf.name
            shutil.copy(sf, f"{destination_directories}/{file_name_nopath}")
    
    elif not isinstance(source_files, list)\
    and isinstance(destination_directories, list):
        
        for dd in destination_directories:
            file_name_nopath = source_files.name
            shutil.copy(source_files, f"{dd}/{file_name_nopath}")
            
    elif not isinstance(source_files, list)\
    and not isinstance(destination_directories, list):
        
        file_name_nopath = source_files.name
        shutil.copy(source_files, f"{destination_directories}/{file_name_nopath}")
    
        
def copy_files_byExts_fromCodeCallDir(extensions,
                                      destination_directories,
                                      recursive_in_depth=True):
    
    """
    Function that moves files selected by extensions,
    from the directory that this code is called
    to the desired directory or directories.
      
    Parameters
    ----------
    extensions : str or list
          A string of the file extension or a list of extensions,
          WITHOUT THE POINT MARKER in any case.
    destination_directories : str or list
          A string of the directory name or a list
          containing several directories where to move the matching files.
    recursive_in_depth : bool
          Applies only to the case in which both of the first parameters are lists.
          Default value is True.
          Behavior explanation is shown below.
    
    This function distinguishes four cases:
    
      1. Both file names and directories are lists.
          1.1 recursive_in_depth=True
              Then it is understood that each extensioned file
              corresponds to multiple directories and it is
              recursively copied to all of them.
          1.2 recursive_in_depth=False
              Then it is understood that each extensioned file
              corresponds to a single directory, and it is copied
              to the aforementioned directory.
              File and directory lists have to be of the same length;
              throws and error otherwise.
      2. The file names are contained in a list but there is
          a single directory.
              Then each file will be copied to that directory.
      3. The extension is a string and directories are contained in a list.
              Then the matching files will be recursively copied
              to each of the directories.
      4. None of them are lists.
              Then the matching files will simply be copied to that directory.
    """          
    
    if isinstance(extensions, list)\
    and isinstance(destination_directories, list)\
    and recursive_in_depth:
        
        for ext in extensions:
            for dd in destination_directories:
                extension_allfiles = cwd.glob(f"*.{ext}")   
                
                for file in extension_allfiles:
                    file_name_nopath = file.name
                    shutil.copy(file, f"{dd}/{file_name_nopath}")
                    
    elif isinstance(extensions, list)\
    and isinstance(destination_directories, list)\
    and not recursive_in_depth:
            
        len_exts = len(extensions)
        len_dds = len(destination_directories)
        
        if len_exts != len_dds:
            raise ValueError(format_string(notEqualLengthErrorStr, arg_tuple_exts_dirs))
        else:
            for ext, dd in zip(extensions, destination_directories):
                extension_allfiles = cwd.glob(f"*.{ext}")   
                
                for file in extension_allfiles:
                    file_name_nopath = file.name
                    shutil.copy(file, f"{dd}/{file_name_nopath}")
            
                
    elif isinstance(extensions, list)\
    and not isinstance(destination_directories, list):
        
        for ext in extensions:
            extension_allfiles = cwd.glob(f"*.{ext}")
            
            for file in extension_allfiles:
                file_name_nopath = file.name
                shutil.copy(file, f"{destination_directories}/{file_name_nopath}")
                
    elif not isinstance(extensions, list)\
    and isinstance(destination_directories, list):
        
        extension_allfiles = cwd.glob(f"*.{extensions}")
        
        for dd in destination_directories:
            for file in extension_allfiles:
                file_name_nopath = file.name
                shutil.copy(file, f"{dd}/{file_name_nopath}")           
                
    else:
        extension_allfiles = cwd.glob(f"*.{extensions}") 
        
        for file in extension_allfiles:
            file_name_nopath = file.name
            shutil.copy(file, f"{destination_directories}/{file_name_nopath}")


def copy_files_byFS_fromCodeCallDir(file_strings,
                                    destination_directories,
                                    recursive_in_depth=True):

    """
    Function that copies files selected by part of the file name,
    from the directory that this code is called
    to the desired directory or directories.
    
    Parameters
    ----------
    file_strings : str or list
          String or list of strings that identify the desired files.
          Accepts file name extension globbing.
    destination_directories : str or list
          A string of the directory name or a list
          containing several directories where to move the matching files.
    recursive_in_depth : bool
          Applies only to the case in which both of the first parameters are lists.
          Default value is True.
          Behavior explanation is shown below.
    
    This function distinguishes five cases:
    
      1. Both file names and directories are lists.
          1.1 recursive_in_depth=True
              Then it is understood that each string file
              corresponds to multiple directories and it is
              recursively copied to all of them.
          1.2 recursive_in_depth=False
              Then it is understood that each string file
              corresponds to a single directory, and it is
              copied to the aforementioned directory. 
              File and directory lists have to be of the same length;
              throws and error otherwise.
      2. The file names are contained in a list but there is
          a single directory.
              Then each file will be copied to that directory.
      3. The extension is a string and directories are contained in a list.
              Then the matching files will be recursively copied
              to each of the directories.
      4. None of them are lists.
              Then the matching files will simply be moved to that directory.
    """

    if isinstance(file_strings, list)\
    and isinstance(destination_directories, list)\
    and recursive_in_depth:
        
        for fs in file_strings:
            for dd in destination_directories:
                string_allfiles = [file
                                   for file in cwd.glob(fs)
                                   if file.is_file()]
                
                for file in string_allfiles:
                    file_name_nopath = file.name
                    shutil.copy(file, f"{dd}/{file_name_nopath}")
                    
    elif isinstance(file_strings, list)\
    and isinstance(destination_directories, list)\
    and not recursive_in_depth:
            
        len_fs = len(file_strings)
        len_dds = len(destination_directories)
        
        if len_fs != len_dds:
            raise ValueError(format_string(notEqualLengthErrorStr, arg_tuple_exts_dirs))
        else:
            for fs, dd in zip(file_strings, destination_directories):
                string_allfiles = [file
                                   for file in cwd.glob(fs)
                                   if file.is_file()]
                
                for file in string_allfiles:
                    file_name_nopath = file.name
                    shutil.copy(file, f"{dd}/{file_name_nopath}")


    elif isinstance(file_strings, list)\
    and not isinstance(destination_directories, list):
        
        for fs in file_strings:
            string_allfiles = [file
                               for file in cwd.glob(fs)
                               if file.is_file()]
            
            for file in string_allfiles:
                file_name_nopath = file.name
                shutil.copy(file, f"{destination_directories}/{file_name_nopath}")
 
    elif not isinstance(file_strings, list)\
    and isinstance(destination_directories, list):
        
        string_allfiles = [file
                           for file in cwd.glob(f"{file_strings}")
                           if file.is_file()]
        
        for dd in destination_directories:
            for file in string_allfiles:
                file_name_nopath = file.name
                shutil.copy(file, f"{dd}/{file_name_nopath}")           

    else:
        string_allfiles = [file
                           for file in cwd.glob(f"{file_strings}")
                           if file.is_file()]
        
        for file in string_allfiles:
            file_name_nopath = file.name
            shutil.copy(file, f"{destination_directories}/{file_name_nopath}")
            
            
def remove_files_byExts(extensions,
                        destination_directories,
                        find_hidden_files=False,
                        recursive_in_depth=True):
    
    """
    Function that removes files selected by extensions 
    from the specified directory or directories.
    
    It also incorporates a function to remove hidden files,
    if the path is already known; it is similar to the UNIX command.
    Since it is not an ordinary task to work with hidden files,
    the only task to accomplish for is to delete them.
    
    Parameters
    ----------
    extensions : str or list
          A string of the file extension or a list of extensions,
          WITHOUT THE POINT MARKER in any case.
    destination_directories : str or list
          A string of the directory name or a list
          containing several directories where to move the matching files.
    find_hidden_files : bool
          Controls whether to seek for hidden files in the given directory
          by 'destination_directories' parameter. Defaults False.
    recursive_in_depth : bool
          Applies only to the case in which both of the first parameters are lists.
          Default value is True.
          Behavior explanation is shown below.
    
    This function distinguishes four cases:
    
      1. Both file names and directories are lists.
          1.1 recursive_in_depth=True
              Then it is understood that each file
              corresponds to multiple directories and they have to be
              recursively removed from all of them.
          1.2 recursive_in_depth=False
              Then it is understood that each file
              corresponds to a single directory, and they are removed from
              the given directories.
              File and directory lists have to be of the same length;
              throws and error otherwise.
      2. The file names are contained in a list but there is
          a single directory.
              Then each file will be removed from that directory.
      3. The extension is a string and directories are contained in a list.
              Then the matching files will be recursively removed
              from each of the directories.
      4. None of them are lists.
              Then the matching files will simply be removed from that directory.
    """ 
          
    if isinstance(destination_directories, list):
        destination_directories = [posixpath_converter(dirc, False)
                                   for dirc in str(destination_directories)]
        
    else:
        destination_directories = [posixpath_converter(destination_directories, False)]
    
    if isinstance(extensions, list)\
    and isinstance(destination_directories, list)\
    and recursive_in_depth:
        
        for ext in extensions:
            for dd in destination_directories:
                
                if not find_hidden_files:
                    string_allfiles = dd.glob(f"*.{ext}")
                else:
                    string_allfiles = [file
                                       for file in dd.glob(f"*.{ext}")]
                
                for file in string_allfiles:
                    os.remove(file)

    elif isinstance(extensions, list)\
    and isinstance(destination_directories, list)\
    and not recursive_in_depth:
            
        len_exts = len(extensions)
        len_dds = len(destination_directories)
        
        if len_exts != len_dds:
            raise ValueError(format_string(notEqualLengthErrorStr, arg_tuple_exts_dirs))
        else:
            for fs, dd in zip(extensions, destination_directories):
                
                if not find_hidden_files:
                    string_allfiles = dd.glob(f"*.{ext}")
                else:
                    string_allfiles = [file for file in dd.glob(f"*.{ext}")]
                
                for file in string_allfiles:
                    os.remove(file)

    elif isinstance(extensions, list)\
    and not isinstance(destination_directories, list):
        
        destination_directories = destination_directories[0]
      
        for ext in extensions:    
            
            if not find_hidden_files:
                string_allfiles = destination_directories.glob(f"*.{ext}")
            else:
                string_allfiles\
                = [file for file in destination_directories.glob(f"*.{ext}")]
            
            for file in string_allfiles:
                os.remove(file)
                
    elif not isinstance(extensions, list)\
    and isinstance(destination_directories, list):
        
        for dd in destination_directories:   
            
            if not find_hidden_files:
                string_allfiles = dd.glob(f"*.{extensions}")
            else:
                string_allfiles = [file for file in dd.glob(f"*.{extensions}")]
            
            for file in string_allfiles:
                os.remove(file)
                
    else:
        destination_directories = destination_directories[0]
        
        if not find_hidden_files:
            string_allfiles = destination_directories.glob(f"*.{extensions}")
        else:
            string_allfiles\
            = [file for file in destination_directories.glob(f"*.{extensions}")]
        
        for file in string_allfiles:
            os.remove(file)


def remove_files_byFS(file_strings,
                      destination_directories,
                      find_hidden_files=False,
                      recursive_in_depth=True):
    
    """
    Function that removes files selected by part of the file name
    from the specified directory or directories.
    
    It also incorporates a function to remove hidden files,
    if the path is already known; it is similar to the UNIX command.
    Since it is not an ordinary task to work with hidden files,
    the only task to accomplish for is to delete them.
    
    Parameters
    ----------
    file_strings : str or list
          String or list of strings that identify the desired files.
          Accepts file name extension globbing.
    destination_directories : str or list
          A string of the directory name or a list containing
          several directories.
    find_hidden_files : bool
          Controls whether to seek for hidden files in the given directory
          by 'destination_directories' parameter. Defaults False.
    recursive_in_depth : bool
          Applies only to the case in which both of the first parameters are lists.
          Default value is True.
          Behavior explanation is shown below.
    
    This function distinguishes four cases:
    
      1. Both file names and directories are lists.
          1.1 recursive_in_depth=True
              Then it is understood that each string file
              corresponds to multiple directories and it is
              recursively removed from all of them.
          1.2 recursive_in_depth=False
              Then it is understood that each string file
              corresponds to a single directory, and it is
              removed from the aforementioned directory. 
              File and directory lists have to be of the same length;
              throws and error otherwise.
      2. The file names are contained in a list but there is
          a single directory.
              Then each file will be removed from that directory.
      3. The extension is a string and directories are contained in a list.
              Then the matching files will be recursively removed
              from each of the directories.
      4. None of them are lists.
              Then the matching files will simply be removed from that directory.
    """ 
    
    if isinstance(destination_directories, list):
        destination_directories = [posixpath_converter(dirc, False)
                                   for dirc in str(destination_directories)]
        
    else:
        destination_directories\
        = posixpath_converter(destination_directories, False)


    if isinstance(file_strings, list)\
    and isinstance(destination_directories, list):
        
        if recursive_in_depth:
        
            for fs in file_strings:
                for dd in destination_directories:   
                    
                    if not find_hidden_files:
                        string_allfiles = [file
                                           for file in dd.glob(fs)
                                           if file.is_file()]
                    else:
                        string_allfiles = [file
                                           for file in
                                           [fileref for fileref in dd.glob(fs)]
                                           if file.is_file()]
                        
                    for file in string_allfiles:
                        os.remove(file)
                        
        else:
            len_fs = len(file_strings)
            len_dds = len(destination_directories)
            
            if len_fs != len_dds:
                raise ValueError(format_string(notEqualLengthErrorStr, arg_tuple_FS_dirs))
            else:
                for fs, dd in zip(file_strings, destination_directories):
                    
                    if not find_hidden_files:
                        string_allfiles = [file
                                           for file in dd.glob(fs)
                                           if file.is_file()]
                    else:
                        string_allfiles = [file
                                           for file in
                                           [fileref for fileref in dd.glob(fs)]
                                           if file.is_file()]
                    
                    for file in string_allfiles:
                        os.remove(file)


    elif isinstance(file_strings, list)\
    and not isinstance(destination_directories, list):
        
        for fs in file_strings:     
            
            if not find_hidden_files:
                string_allfiles = destination_directories.glob(fs)
            else:
                string_allfiles\
                = [file
                   for file in destination_directories.glob(fs)]
            
            for file in string_allfiles:
                os.remove(file)
                
    elif not isinstance(file_strings, list)\
    and isinstance(destination_directories, list):
    
        for dd in destination_directories:
            
            if not find_hidden_files:
                string_allfiles = [file
                                   for file in dd.glob(file_strings)
                                   if file.is_file()]
            else:
                string_allfiles\
                = [file
                   for file in 
                   [fileref for fileref in dd.glob(file_strings)]
                   if file.is_file()]
                
            for file in string_allfiles:
                os.remove(file)
                
    else:
       
        if not find_hidden_files:
            string_allfiles\
            = [file
               for file in destination_directories.glob(file_strings)
               if file.is_file()]
        else:
            string_allfiles\
            = [file
               for file in 
               [fileref for fileref in destination_directories.glob(file_strings)]
               if file.is_file()]
            
        for file in string_allfiles:
            os.remove(file)


# Operations involving directories #
#----------------------------------#

def make_parent_directories(directory_list):
   
    if isinstance(directory_list, str):
        directory_list = [directory_list]

    dirPathList = [posixpath_converter(dirc, False)
                   for dirc in directory_list]
    
    for pathDir in dirPathList:
        pathDir.mkdir(parents=True, exist_ok=True)
        
        
def remove_entire_directories(directory_list):

    if isinstance(directory_list, str):
        directory_list = [directory_list]

    for dirc in directory_list:
        shutil.rmtree(dirc, ignore_errors=True)


def rsync(source_paths,
          destination_paths,
          mode="avh",
          delete_at_destination=True,
          source_allfiles_only=False):
    
    for sp, dp in zip(source_paths, destination_paths):
        
        if delete_at_destination and not source_allfiles_only:
            option_num = 1
            
        elif not delete_at_destination and not source_allfiles_only:
            option_num = 2
            
        elif delete_at_destination and source_allfiles_only:
            option_num = 3
            
        elif not delete_at_destination and source_allfiles_only:
            option_num = 4
            
        rsync_command_prefmt = rsync_command_dict.get(option_num)
        arg_tuple_rsync = (mode, sp, dp)
        
        rsync_command = format_string(rsync_command_prefmt, arg_tuple_rsync)
        exec_shell_command(rsync_command)
    

def move_entire_directories(directories, destination_directories):
    
    if isinstance(directories, list)\
    and isinstance(destination_directories, list):
        
        for dirc in directories:
            for dd in destination_directories:
                shutil.move(dirc, 
                            dd,
                            copy_function=shutil.copytree)
                    
    elif isinstance(directories, list)\
    and isinstance(destination_directories, list):
            
        len_exts = len(directories)
        len_dds = len(destination_directories)
        
        if len_exts != len_dds:
            raise ValueError(format_string(notEqualLengthErrorStr, arg_tuple_exts_dirs))
        else:
            for dirc, dd in zip(directories, destination_directories):
                shutil.move(dirc,
                            dd,
                            copy_function=shutil.copytree)
                
    elif isinstance(directories, list)\
    and not isinstance(destination_directories, list):
        for dirc in directories:
            shutil.move(dirc, 
                        destination_directories, 
                        copy_function=shutil.copytree)
                
    elif not isinstance(directories, list)\
    and isinstance(destination_directories, list):        
        for dd in destination_directories:
            shutil.move(directories,
                        dd, 
                        copy_function=shutil.copytree)
                
    else:
        shutil.move(directories, 
                    destination_directories, 
                    copy_function=shutil.copytree)
            
        
def copy_entire_directories(directories,
                            destination_directories,
                            files_only=False,
                            recursive_in_depth=True):
    
    if not files_only:
        
        if isinstance(directories, list)\
        and isinstance(destination_directories, list)\
        and recursive_in_depth:
            
            for dirc in directories:
                for dd in destination_directories:
                    shutil.copytree(dirc, dd, dirs_exist_ok=True)
                        
        elif isinstance(directories, list)\
        and isinstance(destination_directories, list)\
        and not recursive_in_depth:
                
            len_exts = len(directories)
            len_dds = len(destination_directories)
            
            if len_exts != len_dds:
                raise ValueError(format_string(notEqualLengthErrorStr, arg_tuple_exts_dirs))
            else:
                for dirc, dd in zip(directories, destination_directories):
                    shutil.copytree(dirc, dd, dirs_exist_ok=True)
                    
        elif isinstance(directories, list)\
        and not isinstance(destination_directories, list):
            for dirc in directories:
                shutil.copytree(dirc, destination_directories, dirs_exist_ok=True)
                    
        elif not isinstance(directories, list)\
        and isinstance(destination_directories, list):        
            for dd in destination_directories:
                shutil.copytree(directories, dd, dirs_exist_ok=True)
                    
        else:
            shutil.copytree(directories, destination_directories, dirs_exist_ok=True)
            
    else:
        
        if isinstance(directories, list)\
        and isinstance(destination_directories, list)\
        and recursive_in_depth:
            
            for dirc in directories:
                for dd in destination_directories:
                    exec_shell_command(format_string(cp_command_str, (dirc, dd)))
                        
        elif isinstance(directories, list)\
        and isinstance(destination_directories, list)\
        and not recursive_in_depth:
                
            len_exts = len(directories)
            len_dds = len(destination_directories)
            
            if len_exts != len_dds:
                raise ValueError("Extension and destination directory lists "
                                 "are not of the same length.")
            else:
                for dirc, dd in zip(directories, destination_directories):
                    exec_shell_command(format_string(cp_command_str, (dirc, dd)))
                    
        elif isinstance(directories, list)\
        and not isinstance(destination_directories, list):
            for dirc in directories:
                exec_shell_command(format_string(cp_command_str, (dirc, 
                                                              destination_directories)))
                    
        elif not isinstance(directories, list)\
        and isinstance(destination_directories, list):        
            for dd in destination_directories:
                exec_shell_command(format_string(cp_command_str, (directories, dd)))
                    
        else:
            exec_shell_command(format_string(cp_command_str, (directories,
                                                          destination_directories)))

# Operations involving both files and directories #
#-------------------------------------------------#

def rename_objects(relative_paths, renaming_relative_paths):

    """
    Function that renames files specified by their absolute paths.
    
    In fact, os.rename can also perform the same tasks as shutil.move does,
    therefore functions 'move_files_byExts_fromCodeCallDir' and
    'move_files_byFS_fromCodeCallDir', including the fact that,
    besides moving a directory or file, it includes the option to
    rename thereof at the destination directory, i.e. altering the
    ultimate part of the absolute path.
    
    However, as a matter of distinguishing among the main usages of the modules,
    and to invoke simple operations, this function will be used
    such that each file or directory will be given another name,
    without altering the absolute path.
    
    Parameters
    ----------
    relative_paths: str or list
          String or list of strings that identify the desired files/directories,
          i.e. the absolute path.
    renaming_relative_paths : str or list
          A string of the file/directory name or a list containing
          several files/directories, i.e the renamed BUT UNALTERED absolute path.
    
    This function distinguishes two cases:
    
      1. Both file names and directories are lists.
          Then it is understood that each string file or directory
          corresponds to another single file or directory and
          it is renamed as commanded. 
          File and directory lists have to be of the same length;
          throws and error otherwise.
      2. None of them are lists.
          Then the matching files will simply be renamed.
    """
    
    if isinstance(relative_paths, list)\
    and isinstance(renaming_relative_paths, list):
        
        len_files = len(relative_paths)
        len_rf = len(renaming_relative_paths)
        
        if len_files != len_rf:
            raise ValueError(format_string(notEqualLengthErrorStr, arg_tuple_rename_objs))
        else:
            for rp, rrp in zip(relative_paths, renaming_relative_paths):
                os.rename(rp, rrp)
    

    elif not isinstance(relative_paths, list)\
    and not isinstance(renaming_relative_paths, list):
        os.rename(relative_paths, renaming_relative_paths)
                
    else:
        raise TypeError(objTypeErrorStr)
                         
#--------------------------#
# Parameters and constants #
#--------------------------#

# Get the directory from where this code is being called #
cwd = Path.cwd()
alldoc_dirpath = Path(fixed_path).parent

# Tuples to pass in into preformatted strings #
arg_tuple_exts_dirs = ("Extension", "destination directory")
arg_tuple_FS_dirs = ("File string", "destination directory")
arg_tuple_rename_objs = ("Files", "renaming file")

# Preformatted strings #
#----------------------#

cp_command_str = """cp -rv {}/* {}""" # TODO: 'bash' agindua saihes daiteke?
notEqualLengthErrorStr = """{} and {} lists are not of the same length."""
objTypeErrorStr = "Both input arguments must either be strings or lists simultaneously."

# 'rsync' command switch-case dictionary #
rsync_command_dict = {
    1 : """rsync -{} --delete '{}' '{}' """,
    2 : """rsync -{} '{}' '{}' """,
    3 : """rsync -{} --delete '{}'/ '{}' """,
    4 : """rsync -{} '{}'/ '{}' """
    }
