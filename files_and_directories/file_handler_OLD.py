#----------------#
# Import modules #
#----------------#

import glob
import os
from pathlib import Path
import shutil

#---------------------------------------#
# Get the all-code containing directory #
#---------------------------------------#

cwd = Path.cwd()
main_path = Path("/".join(cwd.parts[:3])[1:]).glob("*/*")

fixed_dirpath = str([path
                     for path in main_path
                     if "pytools" in str(path).lower()][0])

#------------------#
# Define functions #
#------------------#

def move_files_byExts_fromCodeCallDir(extensions, destination_directories):
    
    # Function that moves files selected by extensions,
    # from the directory that this code is called
    # to the desired directory or directories.
    # 
    # Parameters
    # ----------
    # extensions : str or list
    #       A string of the file extension or a list of extensions,
    #       WITHOUT THE POINT MARKER in any case.
    # destination_directories : str or list
    #       A string of the directory name or a list
    #       containing several directories where to move the matching files.
    # 
    # This function distinguishes four cases:
    # 
    #   1. Both file names and directories are lists.
    #           Then it is understood that each extensioned file
    #           corresponds to a single directory (it is physically impossible to
    #           move files to multiple directories other than copying them),
    #           and it is moved to the aforementioned directory.
    #           File and directory lists have to be of the same length;
    #           throws and error otherwise.
    #   2. The extensions are contained in a list but there is
    #      a single directory.
    #           Then the matching files will be moved to that directory.
    #   3. The extension is a string and directories are contained in a list.
    #           Then the single-extension matching files will be
    #           moved to each of the directories.
    #   4. None of them are lists.
    #           Then the matching files will simply be moved to that directory.

    if isinstance(extensions, list)\
    and isinstance(destination_directories, list):
        
        len_exts = len(extensions)
        len_dds = len(destination_directories)
        
        if len_exts != len_dds:
            raise ValueError("Extension and destination directory lists "
                             "are not of the same length.")
        else:
            for ext, dd in zip(extensions, destination_directories):
                extension_allfiles = glob.glob(f"{cwd}/*.{ext}")
                
                for file in extension_allfiles:
                    file_name_nopath = file.split("/")[-1]
                    shutil.move(file, f"{dd}/{file_name_nopath}")
                
    elif isinstance(extensions, list)\
    and not isinstance(destination_directories, list):
        
        for ext in extensions:
            extension_allfiles = glob.glob(f"{cwd}/*.{ext}") 
            
            for file in extension_allfiles:
                file_name_nopath = file.split("/")[-1]
                shutil.move(file, f"{destination_directories}/{file_name_nopath}")
                
    elif not isinstance(extensions, list)\
    and isinstance(destination_directories, list):
        
        extension_allfiles = glob.glob(f"{cwd}/*.{extensions}")
        
        for dd in destination_directories:
            for file in extension_allfiles:
                file_name_nopath = file.split("/")[-1]
                shutil.move(file, f"{dd}/{file_name_nopath}")           
                
    else:
        extension_allfiles = glob.glob(f"{cwd}/*.{extensions}") 
        
        for file in extension_allfiles:
            file_name_nopath = file.split("/")[-1]
            shutil.move(file, f"{destination_directories}/{file_name_nopath}")


def move_files_byFS_fromCodeCallDir(file_strings, destination_directories):

    # Function that moves files selected by part of the file name,
    # from the directory that this code is called
    # to the desired directory or directories.
    # It uses name globbing (or main globbing, glob.glob attribute).
    #
    # There are four cases of string globbing inside the main globbing:
    #   1. The string is fixed.
    #       Then on the main globbing no asterisk is needed.
    #   2. The string has a particular beggining.
    #       Then on the main globbing the asterisk goes at the end.
    #   3. The string has a particular ending.
    #       Then on the main globbing the asterisk goes at the beggining.
    #   4. The string is composed by several particular substrings.
    #       Several asterisks are placed along the string.
    # 
    # Because these reasons and for practical purposes and simplicity,
    # the main globbing does not include any asterisk placement case,
    # so the strings are required already to have asterisks.
    # This functionality is applied to similar functions in this module.
    # 
    # Parameters
    # ----------
    # file_strings : str or list
    #       String or list of strings that identify the desired files.
    #       Accepts file name extension globbing.
    # destination_directories : str or list
    #       A string of the directory name or a list
    #       containing several directories where to move the matching files.
    # 
    # This function distinguishes four cases:
    # 
    #   1. Both file names and directories are lists.
    #           Then it is understood that each extensioned file
    #           corresponds to a single directory (it is physically impossible to
    #           move files to multiple directories other than copying them),
    #           and it is moved to the aforementioned directory.
    #           File and directory lists have to be of the same length;
    #           throws and error otherwise.
    #   2. The extensions are contained in a list but there is
    #      a single directory.
    #           Then the matching files will be moved to that directory.
    #   3. The extension is a string and directories are contained in a list.
    #           Then the single-extension matching files will be
    #           moved to each of the directories.
    #   4. None of them are lists.
    #           Then the matching files will simply be moved to that directory.

    if isinstance(file_strings, list)\
    and isinstance(destination_directories, list):
        
        len_fs = len(file_strings)
        len_dds = len(destination_directories)
        
        if len_fs != len_dds:
            raise ValueError("File string and destination directory lists "
                             "are not of the same length.")
        else:
            for fs, dd in zip(file_strings, destination_directories):
                string_allfiles = [file
                                   for file in cwd.glob(f"{fs}")
                                   if file.is_file()]
                
                for file in string_allfiles:
                    file_name_nopath = file.split("/")[-1]
                    shutil.move(file, f"{dd}/{file_name_nopath}")

    elif isinstance(file_strings, list)\
    and not isinstance(destination_directories, list):
        
        for fs in file_strings:
            string_allfiles = [file
                               for file in cwd.glob(f"{fs}")
                               if file.is_file()]
            
            for file in string_allfiles:
                file_name_nopath = file.split("/")[-1]
                shutil.move(file, f"{destination_directories}/{file_name_nopath}")
 
    elif not isinstance(file_strings, list)\
    and isinstance(destination_directories, list):
        
        string_allfiles = [file
                           for file in cwd.glob(f"{file_strings}")
                           if file.is_file()]
        
        for dd in destination_directories:
            for file in string_allfiles:
                file_name_nopath = file.split("/")[-1]
                shutil.move(file, f"{dd}/{file_name_nopath}")           

    else:
        string_allfiles = [file
                           for file in cwd.glob(f"{file_strings}")
                           if file.is_file()]
        
        for file in string_allfiles:
            file_name_nopath = file.split("/")[-1]
            shutil.move(file, f"{destination_directories}/{file_name_nopath}")
            

def move_files(source_files, destination_directories):
    
    if isinstance(source_files, list)\
    and isinstance(destination_directories, list):
        
        for sf, dd in zip(source_files, destination_directories):
            file_name_nopath = sf.split("/")[-1]
            shutil.move(sf, f"{dd}/{file_name_nopath}")
            
    elif isinstance(source_files, list)\
    and not isinstance(destination_directories, list):
        
        for sf in source_files:
            file_name_nopath = sf.split("/")[-1]
            shutil.move(sf, f"{destination_directories}/{file_name_nopath}")
    
    elif not isinstance(source_files, list)\
    and isinstance(destination_directories, list):
        
        for dd in destination_directories:
            file_name_nopath = source_files.split("/")[-1]
            shutil.move(source_files, f"{dd}/{file_name_nopath}")
            
    elif not isinstance(source_files, list)\
    and not isinstance(destination_directories, list):
        
        file_name_nopath = source_files.split("/")[-1]
        shutil.move(source_files, f"{destination_directories}/{file_name_nopath}")
        
        
def copy_files(source_files, destination_directories):
    
    if isinstance(source_files, list)\
    and isinstance(destination_directories, list):
        
        for sf, dd in zip(source_files, destination_directories):
            file_name_nopath = sf.split("/")[-1]
            shutil.copy(sf, f"{dd}/{file_name_nopath}")
            
    elif isinstance(source_files, list)\
    and not isinstance(destination_directories, list):
        
        for sf in source_files:
            file_name_nopath = sf.split("/")[-1]
            shutil.copy(sf, f"{destination_directories}/{file_name_nopath}")
    
    elif not isinstance(source_files, list)\
    and isinstance(destination_directories, list):
        
        for dd in destination_directories:
            file_name_nopath = source_files.split("/")[-1]
            shutil.copy(source_files, f"{dd}/{file_name_nopath}")
            
    elif not isinstance(source_files, list)\
    and not isinstance(destination_directories, list):
        
        file_name_nopath = source_files.split("/")[-1]
        shutil.copy(source_files, f"{destination_directories}/{file_name_nopath}")
    
        
def copy_files_byExts_fromCodeCallDir(extensions,
                                      destination_directories,
                                      recursive_in_depth=True):
    
    # Function that moves files selected by extensions,
    # from the directory that this code is called
    # to the desired directory or directories.
    #  
    # Parameters
    # ----------
    # extensions : str or list
    #       A string of the file extension or a list of extensions,
    #       WITHOUT THE POINT MARKER in any case.
    # destination_directories : str or list
    #       A string of the directory name or a list
    #       containing several directories where to move the matching files.
    # recursive_in_depth : bool
    #       Applies only to the case in which both of the first parameters are lists.
    #       Default value is True.
    #       Behavior explanation is shown below.
    # 
    # This function distinguishes four cases:
    # 
    #   1. Both file names and directories are lists.
    #       1.1 recursive_in_depth=True
    #           Then it is understood that each extensioned file
    #           corresponds to multiple directories and it is
    #           recursively copied to all of them.
    #       1.2 recursive_in_depth=False
    #           Then it is understood that each extensioned file
    #           corresponds to a single directory, and it is copied
    #           to the aforementioned directory.
    #           File and directory lists have to be of the same length;
    #           throws and error otherwise.
    #   2. The file names are contained in a list but there is
    #      a single directory.
    #           Then each file will be copied to that directory.
    #   3. The extension is a string and directories are contained in a list.
    #           Then the matching files will be recursively copied
    #           to each of the directories.
    #   4. None of them are lists.
    #           Then the matching files will simply be copied to that directory.
               
    if isinstance(extensions, list)\
    and isinstance(destination_directories, list)\
    and recursive_in_depth:
        
        for ext in extensions:
            for dd in destination_directories:
                extension_allfiles = glob.glob(f"{cwd}/*.{ext}")   
                
                for file in extension_allfiles:
                    file_name_nopath = file.split("/")[-1]
                    shutil.copy(file, f"{dd}/{file_name_nopath}")
                    
    elif isinstance(extensions, list)\
    and isinstance(destination_directories, list)\
    and not recursive_in_depth:
            
        len_exts = len(extensions)
        len_dds = len(destination_directories)
        
        if len_exts != len_dds:
            raise ValueError("Extension and destination directory lists "
                             "are not of the same length.")
        else:
            for ext, dd in zip(extensions, destination_directories):
                extension_allfiles = glob.glob(f"{cwd}/*.{ext}")   
                
                for file in extension_allfiles:
                    file_name_nopath = file.split("/")[-1]
                    shutil.copy(file, f"{dd}/{file_name_nopath}")
            
                
    elif isinstance(extensions, list)\
    and not isinstance(destination_directories, list):
        
        for ext in extensions:
            extension_allfiles = glob.glob(f"{cwd}/*.{ext}") 
            
            for file in extension_allfiles:
                file_name_nopath = file.split("/")[-1]
                shutil.copy(file, f"{destination_directories}/{file_name_nopath}")
                
    elif not isinstance(extensions, list)\
    and isinstance(destination_directories, list):
        
        extension_allfiles = glob.glob(f"{cwd}/*.{extensions}")
        
        for dd in destination_directories:
            for file in extension_allfiles:
                file_name_nopath = file.split("/")[-1]
                shutil.copy(file, f"{dd}/{file_name_nopath}")           
                
    else:
        extension_allfiles = glob.glob(f"{cwd}/*.{extensions}") 
        
        for file in extension_allfiles:
            file_name_nopath = file.split("/")[-1]
            shutil.copy(file, f"{destination_directories}/{file_name_nopath}")


def copy_files_byFS_fromCodeCallDir(file_strings,
                                    destination_directories,
                                    recursive_in_depth=True):

    # Function that copies files selected by part of the file name,
    # from the directory that this code is called
    # to the desired directory or directories.
    # 
    # Parameters
    # ----------
    # file_strings : str or list
    #       String or list of strings that identify the desired files.
    #       Accepts file name extension globbing.
    # destination_directories : str or list
    #       A string of the directory name or a list
    #       containing several directories where to move the matching files.
    # recursive_in_depth : bool
    #       Applies only to the case in which both of the first parameters are lists.
    #       Default value is True.
    #       Behavior explanation is shown below.
    # 
    # This function distinguishes five cases:
    # 
    #   1. Both file names and directories are lists.
    #       1.1 recursive_in_depth=True
    #           Then it is understood that each string file
    #           corresponds to multiple directories and it is
    #           recursively copied to all of them.
    #       1.2 recursive_in_depth=False
    #           Then it is understood that each string file
    #           corresponds to a single directory, and it is
    #           copied to the aforementioned directory. 
    #           File and directory lists have to be of the same length;
    #           throws and error otherwise.
    #   2. The file names are contained in a list but there is
    #      a single directory.
    #           Then each file will be copied to that directory.
    #   3. The extension is a string and directories are contained in a list.
    #           Then the matching files will be recursively copied
    #           to each of the directories.
    #   4. None of them are lists.
    #           Then the matching files will simply be moved to that directory.

    if isinstance(file_strings, list)\
    and isinstance(destination_directories, list)\
    and recursive_in_depth:
        
        for fs in file_strings:
            for dd in destination_directories:
                string_allfiles = [file
                                   for file in cwd.glob(f"{fs}")
                                   if file.is_file()]
                
                for file in string_allfiles:
                    file_name_nopath = file.split("/")[-1]
                    shutil.copy(file, f"{dd}/{file_name_nopath}")
                    
    elif isinstance(file_strings, list)\
    and isinstance(destination_directories, list)\
    and not recursive_in_depth:
            
        len_fs = len(file_strings)
        len_dds = len(destination_directories)
        
        if len_fs != len_dds:
            raise ValueError("Extension and destination directory lists "
                             "are not of the same length.")
        else:
            for fs, dd in zip(file_strings, destination_directories):
                string_allfiles = [file
                                   for file in cwd.glob(f"{fs}")
                                   if file.is_file()]
                
                for file in string_allfiles:
                    file_name_nopath = file.split("/")[-1]
                    shutil.copy(file, f"{dd}/{file_name_nopath}")


    elif isinstance(file_strings, list)\
    and not isinstance(destination_directories, list):
        
        for fs in file_strings:
            string_allfiles = [file
                               for file in cwd.glob(f"{fs}")
                               if file.is_file()]
            
            for file in string_allfiles:
                file_name_nopath = file.split("/")[-1]
                shutil.copy(file, f"{destination_directories}/{file_name_nopath}")
 
    elif not isinstance(file_strings, list)\
    and isinstance(destination_directories, list):
        
        string_allfiles = [file
                           for file in cwd.glob(f"{file_strings}")
                           if file.is_file()]
        
        for dd in destination_directories:
            for file in string_allfiles:
                file_name_nopath = file.split("/")[-1]
                shutil.copy(file, f"{dd}/{file_name_nopath}")           

    else:
        string_allfiles = [file
                           for file in cwd.glob(f"{file_strings}")
                           if file.is_file()]
        
        for file in string_allfiles:
            file_name_nopath = file.split("/")[-1]
            shutil.copy(file, f"{destination_directories}/{file_name_nopath}")
            
            
def remove_files_byExts(extensions,
                        destination_directories,
                        find_hidden_files=False,
                        recursive_in_depth=True):
    
    # Function that removes files selected by extensions 
    # from the specified directory or directories.
    # 
    # It also incorporates a function to remove hidden files,
    # if the path is already known; it is similar to the UNIX command.
    # Since it is not an ordinary task to work with hidden files,
    # the only task to accomplish for is to delete them.
    # 
    # Parameters
    # ----------
    # extensions : str or list
    #       A string of the file extension or a list of extensions,
    #       WITHOUT THE POINT MARKER in any case.
    # destination_directories : str or list
    #       A string of the directory name or a list
    #       containing several directories where to move the matching files.
    # find_hidden_files : bool
    #       Controls whether to seek for hidden files in the given directory
    #       by ´destination_directories´ parameter. Defaults False.
    # recursive_in_depth : bool
    #       Applies only to the case in which both of the first parameters are lists.
    #       Default value is True.
    #       Behavior explanation is shown below.
    # 
    # This function distinguishes four cases:
    # 
    #   1. Both file names and directories are lists.
    #       1.1 recursive_in_depth=True
    #           Then it is understood that each file
    #           corresponds to multiple directories and they have to be
    #           recursively removed from all of them.
    #       1.2 recursive_in_depth=False
    #           Then it is understood that each file
    #           corresponds to a single directory, and they are removed from
    #           the given directories.
    #           File and directory lists have to be of the same length;
    #           throws and error otherwise.
    #   2. The file names are contained in a list but there is
    #      a single directory.
    #           Then each file will be removed from that directory.
    #   3. The extension is a string and directories are contained in a list.
    #           Then the matching files will be recursively removed
    #           from each of the directories.
    #   4. None of them are lists.
    #           Then the matching files will simply be removed from that directory.
               
    if isinstance(extensions, list)\
    and isinstance(destination_directories, list)\
    and recursive_in_depth:
        
        for ext in extensions:
            for dd in destination_directories:
                
                if not find_hidden_files:
                    string_allfiles = glob.glob(f"{dd}/*.{ext}")
                else:
                    string_allfiles = [file
                                       for file in Path(dd).glob(f"*.{ext}")]
                
                for file in string_allfiles:
                    os.remove(file)

    elif isinstance(extensions, list)\
    and isinstance(destination_directories, list)\
    and not recursive_in_depth:
            
        len_exts = len(extensions)
        len_dds = len(destination_directories)
        
        if len_exts != len_dds:
            raise ValueError("File string and destination directory lists "
                             "are not of the same length.")
        else:
            for fs, dd in zip(extensions, destination_directories):
                
                if not find_hidden_files:
                    string_allfiles = glob.glob(f"{dd}/*.{ext}")
                else:
                    string_allfiles = [file
                                       for file in Path(dd).glob(f"*.{ext}")]
                
                for file in string_allfiles:
                    os.remove(file)

    elif isinstance(extensions, list)\
    and not isinstance(destination_directories, list):
        
        for ext in extensions:    
            
            if not find_hidden_files:
                string_allfiles = glob.glob(f"{destination_directories}/*.{ext}")
            else:
                string_allfiles\
                = [file
                   for file in Path(destination_directories).glob(f"*.{ext}")]
            
            for file in string_allfiles:
                os.remove(file)
                
    elif not isinstance(extensions, list)\
    and isinstance(destination_directories, list):
        
        for dd in destination_directories:     
            
            if not find_hidden_files:
                string_allfiles = glob.glob(f"{dd}/*.{extensions}")
            else:
                string_allfiles = [file
                                   for file in Path(dd).glob(f"*.{extensions}")]
            
            for file in string_allfiles:
                os.remove(file)
                
    else:
        
        if not find_hidden_files:
            string_allfiles = glob.glob(f"{destination_directories}/*.{extensions}")
        else:
            string_allfiles\
            = [file
               for file in Path(destination_directories).glob(f"*.{extensions}")]
        
        for file in string_allfiles:
            os.remove(file)


def remove_files_byFS(file_strings,
                      destination_directories,
                      find_hidden_files=False,
                              recursive_in_depth=True):
    
    # Function that removes files selected by part of the file name
    # from the specified directory or directories.
    # 
    # It also incorporates a function to remove hidden files,
    # if the path is already known; it is similar to the UNIX command.
    # Since it is not an ordinary task to work with hidden files,
    # the only task to accomplish for is to delete them.
    # 
    # Parameters
    # ----------
    # file_strings : str or list
    #       String or list of strings that identify the desired files.
    #       Accepts file name extension globbing.
    # destination_directories : str or list
    #       A string of the directory name or a list containing
    #       several directories.
    # find_hidden_files : bool
    #       Controls whether to seek for hidden files in the given directory
    #       by ´destination_directories´ parameter. Defaults False.
    # recursive_in_depth : bool
    #       Applies only to the case in which both of the first parameters are lists.
    #       Default value is True.
    #       Behavior explanation is shown below.
    # 
    # This function distinguishes four cases:
    # 
    #   1. Both file names and directories are lists.
    #       1.1 recursive_in_depth=True
    #           Then it is understood that each string file
    #           corresponds to multiple directories and it is
    #           recursively removed from all of them.
    #       1.2 recursive_in_depth=False
    #           Then it is understood that each string file
    #           corresponds to a single directory, and it is
    #           removed from the aforementioned directory. 
    #           File and directory lists have to be of the same length;
    #           throws and error otherwise.
    #   2. The file names are contained in a list but there is
    #      a single directory.
    #           Then each file will be removed from that directory.
    #   3. The extension is a string and directories are contained in a list.
    #           Then the matching files will be recursively removed
    #           from each of the directories.
    #   4. None of them are lists.
    #           Then the matching files will simply be removed from that directory.

    if isinstance(file_strings, list)\
    and isinstance(destination_directories, list)\
    and recursive_in_depth:
        
        for fs in file_strings:
            for dd in destination_directories:   
                
                if not find_hidden_files:
                    string_allfiles = [file
                                       for file in Path(dd).glob(fs)
                                       if file.is_file()]
                else:
                    string_allfiles = [file
                                       for file in
                                       [fileref for fileref in Path(dd).glob(fs)]
                                       if file.is_file()]
                    
                for file in string_allfiles:
                    os.remove(file)

    elif isinstance(file_strings, list)\
    and isinstance(destination_directories, list)\
    and not recursive_in_depth:
            
        len_fs = len(file_strings)
        len_dds = len(destination_directories)
        
        if len_fs != len_dds:
            raise ValueError("File string and destination directory lists "
                             "are not of the same length.")
        else:
            for fs, dd in zip(file_strings, destination_directories):
                
                if not find_hidden_files:
                    string_allfiles = [file
                                       for file in Path(dd).glob(fs)
                                       if file.is_file()]
                else:
                    string_allfiles = [file
                                       for file in
                                       [fileref for fileref in Path(dd).glob(fs)]
                                       if file.is_file()]
                
                for file in string_allfiles:
                    os.remove(file)

    elif isinstance(file_strings, list)\
    and not isinstance(destination_directories, list):
        
        for fs in file_strings:     
            
            if not find_hidden_files:
                string_allfiles = glob.glob(f"{destination_directories}/{fs}")
            else:
                string_allfiles\
                = [file
                   for file in Path(destination_directories).glob(fs)]
            
            for file in string_allfiles:
                os.remove(file)
                
    elif not isinstance(file_strings, list)\
    and isinstance(destination_directories, list):
        
        for dd in destination_directories:  
            
            if not find_hidden_files:
                string_allfiles = [file
                                   for file in Path(dd).glob(file_strings)
                                   if file.is_file()]
            else:
                string_allfiles\
                = [file
                   for file in 
                   [fileref for fileref in Path(dd).glob(file_strings)]
                   if file.is_file()]
                
            for file in string_allfiles:
                os.remove(file)
                
    else:
        
        if not find_hidden_files:
            string_allfiles\
            = [file
               for file in Path(destination_directories).glob(file_strings)
               if file.is_file()]
        else:
            string_allfiles\
            = [file
               for file in 
               [fileref for fileref in Path(destination_directories).glob(file_strings)]
               if file.is_file()]
            
        for file in string_allfiles:
            os.remove(file)


def rename_objects(relative_paths,
                   renaming_relative_paths):

    # Function that renames files specified by their relative paths.
    # 
    # In fact, os.rename can also perform the same tasks as shutil.move does,
    # therefore functions 'move_files_byExts_fromCodeCallDir' and
    # 'move_files_byFS_fromCodeCallDir', including the fact that,
    # besides moving a directory or file, it includes the option to
    # rename thereof at the destination directory, i.e. altering the
    # ultimate part of the relative path.
    # 
    # However, as a matter of distinguishing among the main usages of the modules,
    # and to invoke simple operations, this function will be used
    # such that each file or directory will be given another name,
    # without altering the relative path.
    # 
    # Parameters
    # ----------
    # relative_paths: str or list
    #       String or list of strings that identify the desired files/directories,
    #       i.e. the relative path.
    # renaming_relative_paths : str or list
    #       A string of the file/directory name or a list containing
    #       several files/directories, i.e the renamed BUT UNALTERED relative path.
    # 
    # This function distinguishes two cases:
    # 
    #   1. Both file names and directories are lists.
    #       Then it is understood that each string file or directory
    #       corresponds to another single file or directory and
    #       it is renamed as commanded. 
    #       File and directory lists have to be of the same length;
    #       throws and error otherwise.
    #   2. None of them are lists.
    #       Then the matching files will simply be renamed.
    
    if isinstance(relative_paths, list)\
    and isinstance(renaming_relative_paths, list):
        
        len_files = len(relative_paths)
        len_rf = len(renaming_relative_paths)
        
        if len_files != len_rf:
            raise ValueError("Files and renaming file lists "
                             "are not of the same length.")
        else:
            for rp, rrp in zip(relative_paths, renaming_relative_paths):
                os.rename(rp, rrp)
    

    elif not isinstance(relative_paths, list)\
    and not isinstance(renaming_relative_paths, list):
        os.rename(relative_paths, renaming_relative_paths)
                
    else:
        raise ValueError("Both input arguments must either be "
                        "strings or lists simultaneously.")
