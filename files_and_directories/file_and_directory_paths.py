#----------------#
# Import modules #
#----------------#

from pathlib import Path
import numpy as np

#--------------------------------------------------------#
# Get the directory from where this code is being called #
#--------------------------------------------------------#

cwd = Path.cwd()

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

# Global function for this part #
def get_file_extension(file_name):
    
    path = posixpath_converter(file_name, False)
    extension = path.suffix[1:]
    
    return extension

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
    # top_path_only : boolptwi
    #       Controls whether to search for subdirectories.
    #       If True, the function will search for the given extensions
    #       only at the top of the given path,
    #       without deepening through the subdirectories.
    #        
    # Returns
    # -------
    # unique_pathlist : list
    #       List containing unique paths where the
    #       selected extensions files are present.
    
    if isinstance(extensions, str):
        extensions = [extensions]
        
    if top_path_only:
        ptwi_path = posixpath_converter(path_to_walk_in, glob_bool=False)
        pathlist = [str(file)
                    for file in ptwi_path.iterdir()
                    for ext in extensions
                    if file.is_file()
                    and file.suffix == f".{ext}"]
        
    else:
        ptwi_path = posixpath_converter(path_to_walk_in)
        pathlist = [str(file)
                    for file in ptwi_path
                    for ext in extensions
                    if file.is_file()
                    and file.suffix == f".{ext}"]
        
    unique_pathlist = list(np.unique(pathlist))
    return unique_pathlist


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
    # unique_pathlist : list
    #       List containing unique paths where the
    #       provided file strings are present.

    if isinstance(file_string, str):
        file_string = [file_string]
        
    if top_path_only:
        ptwi_path = posixpath_converter(path_to_walk_in, glob_bool=False)
        pathlist = [str(file)
                    for fs in file_string
                    for file in ptwi_path.glob(f"{fs}")
                    if file.is_file()]
        
    else:
        ptwi_path = posixpath_converter(path_to_walk_in)
        pathlist = [str(file)
                    for path in ptwi_path
                    for fs in file_string
                    for file in path.glob(f"{fs}")
                    if file.is_file()]
        
    unique_pathlist = list(np.unique(pathlist))
    return unique_pathlist
    

def find_allfile_extensions(extensions2skip, top_path_only=False):
    
    if top_path_only:
        path_to_walk_in = posixpath_converter(Path.cwd(), glob_bool=False)
        
        extension_list = [get_file_extension(file)
                          for file in path_to_walk_in.iterdir()
                          if file.is_file()
                          and get_file_extension(file)
                          and get_file_extension(file) not in extensions2skip]

    else:
        path_to_walk_in = posixpath_converter(cwd)
        
        extension_list = [get_file_extension(file)
                          for file in path_to_walk_in
                          if file.is_file()
                          and get_file_extension(file)
                          and get_file_extension(file) not in extensions2skip]
    
    unique_extension_list = list(np.unique(extension_list))        
    return unique_extension_list


# Operations involving directories as a result #
#----------------------------------------------#  

def find_ext_file_directories(extensions, path_to_walk_in):
    
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
    # 
    # Returns
    # -------
    # unique_dirlist : list
    #       List containing unique directories where the
    #       selected extensions files are present.
    
    if isinstance(extensions, str):
        extensions = [extensions]
        
    ptwi_path = posixpath_converter(path_to_walk_in)
    
    # Loop through the given path #
    dirlist = [path.parent
               for path in ptwi_path
               for ext in extensions
               if f".{ext}" == path.suffix]
            
    unique_dirlist = list(np.unique(dirlist))    
    return unique_dirlist


def find_fileString_directories(file_string, path_to_walk_in):
    
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
    # 
    # Returns
    # -------
    # unique_dirlist : list
    #       List containing unique directories where the
    #       provided file strings are present.
    
    if isinstance(file_string, str):
        file_string = [file_string]
        
    ptwi_path = posixpath_converter(path_to_walk_in)
        
    dirlist = [path.parent
               for path in ptwi_path
               for fs in file_string
               if len(list(path.glob(f"{fs}"))) > 0]
    
    unique_dirlist = list(np.unique(dirlist))
    return unique_dirlist