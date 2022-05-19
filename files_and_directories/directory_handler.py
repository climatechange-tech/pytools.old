#----------------#
# Import modules #
#----------------#

import importlib
import os
from pathlib import Path
import shutil

import numpy as np
import pandas as pd

#--------------------------#
# Get the main directories #
#--------------------------#

cwd = Path.cwd()
main_path = Path("/".join(cwd.parts[:3])[1:]).glob("*/*")

# Home directory #
home_path = Path.home()

# All-code containing directory #
fixed_dirpath = str([path
                     for path in main_path
                     if "pytools" in str(path).lower()][0])

# All-document containing directory #
alldoc_dirpath = Path(fixed_dirpath).parent

#-----------------------#
# Import custom modules #
#-----------------------#

module_imp1 = "file_and_directory_paths.py"
module_imp1_path = f"{fixed_dirpath}/"\
                   f"files_and_directories/{module_imp1}"
                   
spec1 = importlib.util.spec_from_file_location(module_imp1, module_imp1_path)
file_and_directory_paths = importlib.util.module_from_spec(spec1)
spec1.loader.exec_module(file_and_directory_paths)


module_imp2 = "string_handler.py"
module_imp2_path = f"{fixed_dirpath}/"\
                   f"strings/{module_imp2}"
                   
spec2 = importlib.util.spec_from_file_location(module_imp2, module_imp2_path)
string_handler = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(string_handler)


module_imp3 = "file_handler.py"
module_imp3_path = f"{fixed_dirpath}/"\
                   f"files_and_directories/{module_imp3}"
                   
spec3 = importlib.util.spec_from_file_location(module_imp3, module_imp3_path)
file_handler = importlib.util.module_from_spec(spec3)
spec3.loader.exec_module(file_handler)

#----------------------------------------------------#
# Define imported module(s)´ function call shortcuts #
#----------------------------------------------------#

posixpath_converter = file_and_directory_paths.posixpath_converter

file_path_specs = string_handler.file_path_specs
join_file_path_specs = string_handler.join_file_path_specs 

rename_objects = file_handler.rename_objects

#------------------#
# Define functions #
#------------------#

# Recovery operations #
#---------------------#

def create_previous_dirConfig_specs():
    
    dirpath_operations = Path.cwd()
    prev_dirconfig_file = "prev_dirconfig.txt"
    prev_dirconfig_path = f"{dirpath_operations}/{prev_dirconfig_file}"
    
    return prev_dirconfig_path, dirpath_operations
    

def save_previous_dirConfig():
    
    prev_dirconfig_path, dirpath_operations = create_previous_dirConfig_specs()
    
    print("Saving previous directory configuration into a text file...")
    
    ofile_prev_dirConfig = open(prev_dirconfig_path, "w")
    
    dirlist = find_allDirectories(home_path, True)
    
    for dirc in dirlist:
        ofile_prev_dirConfig.write(f"{dirpath_operations}/{dirc}\n")
    ofile_prev_dirConfig.close()


def make_parent_directories_from_savelist():
    
    prev_dirconfig_path = create_previous_dirConfig_specs()[0]
    
    print("Parent directories will be created, "
          f"using temporary text file {prev_dirconfig_path}.")
    
    dirlist_df = pd.read_table(prev_dirconfig_path, header=None)
    ldd = len(dirlist_df)
    
    for i in range(ldd):
        dir_name = dirlist_df.iloc[i,0]
        dir_path = posixpath_converter(dir_name, False)
        make_parent_directories(dir_path)
        
        print(f"Creating parent directory {dir_name}...")
        
        
# Miscellaneous functions that work with directories #
#----------------------------------------------------#

def reorder_directories(nzeros_left):
        
    print("Reordering directories by numbers...")
    
    dir_name_splitchar = "-"
    
    dirlist = find_allDirectories(alldoc_dirpath, top_path_only=True)
    for dirc in enumerate(dirlist):
        
        num = dirc[0]
        dir_name = dirc[-1]
        
        dir_new_number = f"{num+1:0{nzeros_left+1}d}"        
        dir_path_parent, dirName, dir_name_split\
        = file_path_specs(str(dir_name), dir_name_splitchar)[:3]
        
        dir_name_split[0] = dir_new_number
        dirName_new = dir_name_splitchar.join(dir_name_split)
        
        dir_new_name = join_file_path_specs(dir_path_parent,
                                            dirName_new,
                                            "")[:-1]
        
        rename_objects(dir_name, dir_new_name)
        
        
def make_parent_directories(directory_list):
   
    if isinstance(directory_list, str):
        directory_list = [directory_list]

    dirPathList = [posixpath_converter(dirc, False)
                   for dirc in directory_list]
    
    for pathDir in dirPathList:
        pathDir.mkdir(parents=True, exist_ok=True)
        
        
def remove_directories(directory_list):

    if isinstance(directory_list, str):
        directory_list = [directory_list]

    for dirc in directory_list:
        shutil.rmtree(dirc, ignore_errors=True)


def rsync(source_paths,
          destination_paths,
          mode="avrh",
          source_allfiles_only=False,
          delete_at_destination=True):
    
    for sp, dp in zip(source_paths, destination_paths):
        
        if delete_at_destination and not source_allfiles_only:
            
            zsh_command = f"rsync -{mode} --delete '{sp}' '{dp}'"
            os.system(zsh_command)
            
        elif not delete_at_destination and not source_allfiles_only:
            zsh_command = f"rsync -{mode} '{sp}' '{dp}'"
            os.system(zsh_command)
            
        elif delete_at_destination and source_allfiles_only:
            zsh_command = f"rsync -{mode} --delete '{sp}'/* '{dp}'"
            os.system(zsh_command)
            
        elif not delete_at_destination and source_allfiles_only:
            zsh_command = f"rsync -{mode} '{sp}'/* '{dp}'"
            os.system(zsh_command)
    

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
            raise ValueError("Extension and destination directory lists "
                             "are not of the same length.")
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
                            copy_directories_themselves=True,
                            recursive_in_depth=True):
    
    if copy_directories_themselves:
        
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
                raise ValueError("Extension and destination directory lists "
                                 "are not of the same length.")
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
                    cp_command = f"cp -rv '{dirc}'/* '{dd}'"
                    os.system(cp_command)
                        
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
                    cp_command = f"cp -rv '{dirc}'/* '{dd}'"
                    os.system(cp_command)
                    
        elif isinstance(directories, list)\
        and not isinstance(destination_directories, list):
            for dirc in directories:
                cp_command = f"cp -rv '{dirc}'/* '{destination_directories}'"
                os.system(cp_command)
                    
        elif not isinstance(directories, list)\
        and isinstance(destination_directories, list):        
            for dd in destination_directories:
                cp_command = f"cp -rv '{directories}'/* '{dd}'"
                os.system(cp_command)
                    
        else:
            cp_command = f"cp -rv '{directories}'/* '{destination_directories}'"
            os.system(cp_command)        
            

def find_allDirectories(source_directory,
                        top_path_only=False,
                        include_root=True):
    
    if top_path_only:
        sd_path = posixpath_converter(source_directory, False)   
        
        dirPathList = [dirc
                       for dirc in sd_path.iterdir()
                       if dirc.is_dir()]
        
        if not include_root:
            dirPathList_noRoot = [dp.name
                                  for dp in dirPathList]            
            return list(np.unique(dirPathList_noRoot))
            
        else:            
            return list(np.unique(dirPathList))

    else:
        sd_path = posixpath_converter(source_directory) 
        dirPathList = [dirc
                       for dirc in sd_path
                       if dirc.is_dir()]
        
        if not include_root:
            dirPathList_noRoot = [dp.name
                                  for dp in dirPathList]            
            return list(np.unique(dirPathList_noRoot))
            
        else:
            return list(np.unique(dirPathList))
 