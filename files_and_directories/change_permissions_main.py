#----------------#
# Import modules #
#----------------#

import importlib
import os
from pathlib import Path

#---------------------------------------#
# Get the all-code containing directory #
#---------------------------------------#

cwd = Path.cwd()
main_path = Path("/".join(cwd.parts[:3])[1:]).glob("*/*")

fixed_dirpath = str([path
                     for path in main_path
                     if "pytools" in str(path).lower()][0])

#-----------------------#
# Import custom modules #
#-----------------------#

module_imp1 = "file_and_directory_paths.py"
module_imp1_path = f"{fixed_dirpath}/"\
                   f"files_and_directories/{module_imp1}"
                   
spec1 = importlib.util.spec_from_file_location(module_imp1, module_imp1_path)
file_and_directory_paths = importlib.util.module_from_spec(spec1)
spec1.loader.exec_module(file_and_directory_paths)


module_imp2 = "directory_handler.py"
module_imp2_path = f"{fixed_dirpath}/"\
                   f"files_and_directories/{module_imp2}"
                   
spec2 = importlib.util.spec_from_file_location(module_imp2, module_imp2_path)
directory_handler = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(directory_handler)

#----------------------------------------------------#
# Define imported module(s)´ function call shortcuts #
#----------------------------------------------------#

find_allfile_extensions = file_and_directory_paths.find_allfile_extensions
find_allDirectories = directory_handler.find_allDirectories

#-----------------------------#
# Get this laptop user´s name #
#-----------------------------#

whoami = os.popen("whoami").read()[:-1]

#-------------------------#
# Define custom functions #
#-------------------------#

def remove_file_executability(source_directory, extensions2skip):
    
    print("Removing executability permission of all files "
          "except the following extensioned ones:\n"
          f"{extensions2skip}")
    
    file_extension_list = find_allfile_extensions(extensions2skip)
    for extension in file_extension_list:
        find_exec_command = f"sudo find '{source_directory}' -name '*.{extension}' "\
                            "-exec chmod ugo-x "\
                            r"'{}' "\
                            "\;"
        os.system(find_exec_command)
        

def reset_directory_permissions(source_directory):
    
    print("Resetting directory permissions to default...")
    
    dirlist = directory_handler.find_allDirectories(source_directory)
    for dirc in dirlist:
        find_exec_command = f"sudo find '{source_directory}' -wholename '{dirc}' -type d "\
                            "-exec chmod 775 "\
                            r"'{}' "\
                            "\;"
        os.system(find_exec_command)
        
 
def change_file_owner_group(source_directory,
                            change_owner,
                            change_group, 
                            extensions2skip):
    
    file_extension_list = find_allfile_extensions(extensions2skip)
    
    if change_owner and change_group:
        print("Changing all files' owner and group "
              "except the following ones:\n"
              f"{extensions2skip}")

        for extension in file_extension_list:
            find_exec_command = f"sudo find '{source_directory}' -name '*.{extension}' "\
                                f"-exec chown {whoami} "\
                                r"'{}' "\
                                "\; "\
                                f"-exec chgrp {whoami} "\
                                r"'{}' "\
                                "\;"
            os.system(find_exec_command)
        
    elif change_owner and not change_group:
        print("Changing all files' owner except the following ones:\n"
              f"{extensions2skip}")

        for extension in file_extension_list:
            find_exec_command = f"sudo find '{source_directory}' -name '*.{extension}' "\
                                f"-exec chown {whoami} "\
                                r"'{}' "\
                                "\;"
            os.system(find_exec_command)
            
    elif not change_owner and change_group:
        print("Changing all files' group except the following ones:\n"
              f"{extensions2skip}")
        
        for extension in file_extension_list:
            find_exec_command = f"sudo find '{source_directory}' -name '*.{extension}' "\
                                f"-exec chgrp {whoami} "\
                                r"'{}' "\
                                "\;"
            os.system(find_exec_command)
        

def change_directory_owner_group(source_directory,
                                 change_owner,
                                 change_group):
    
    dirlist = directory_handler.find_allDirectories(source_directory)
    if change_owner and change_group:
        print("Changing all directories' owner and group...")

        for dirc in dirlist:
            find_exec_command = f"sudo find '{source_directory}' -wholename '{dirc}' -type d "\
                                f"-exec chown {whoami} "\
                                r"'{}' "\
                                "\; "\
                                f"-exec chgrp {whoami} "\
                                r"'{}' "\
                                "\;"                                
            os.system(find_exec_command)
            
    elif change_owner and not change_group:
        print("Changing all directories' owner...")
        
        for dirc in dirlist:
            find_exec_command = f"sudo find '{source_directory}' -wholename '{dirc}' -type d "\
                                f"-exec chown {whoami} "\
                                r"'{}' "\
                                "\;"                               
            os.system(find_exec_command)
            
    elif not change_owner and change_group:
        print("Changing all directories' group...")
        
        for dirc in dirlist:
            find_exec_command = f"sudo find '{source_directory}' -wholename '{dirc}' -type d "\
                                f"-exec chgrp {whoami} "\
                                r"'{}' "\
                                "\;"                                
            os.system(find_exec_command)
