"""
This program is an application of the
module 'change_permissions_main.py'.
Simply copy this script to the desired directory.
"""

#----------------#
# Import modules #
#----------------#

import importlib
from pathlib import Path

#---------------------------------------#
# Get the all-code containing directory #
#---------------------------------------#

cwd = Path.cwd()
main_path = Path("/".join(cwd.parts[:2])[1:]).glob("*/*")

fixed_dirpath = str([path
                     for path in main_path
                     if "pytools" in str(path).lower()][0].parent)

#-----------------------#
# Import custom modules #
#-----------------------#

module_imp1 = "change_permissions_main.py"
module_imp1_path = f"{fixed_dirpath}/"\
                  f"files_and_directories/{module_imp1}"

spec1 = importlib.util.spec_from_file_location(module_imp1, module_imp1_path)
change_permissions_main = importlib.util.module_from_spec(spec1)
spec1.loader.exec_module(change_permissions_main)


module_imp2 = "file_and_directory_paths.py"
module_imp2_path = f"{fixed_dirpath}/"\
                  f"files_and_directories/{module_imp2}"

spec2 = importlib.util.spec_from_file_location(module_imp2, module_imp2_path)
file_and_directory_paths = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(file_and_directory_paths)

#----------------------------------------------------#
# Define imported module(s)´ function call shortcuts #
#----------------------------------------------------#

find_allfile_extensions = file_and_directory_paths.find_allfile_extensions

remove_file_executability = change_permissions_main.remove_file_executability
reset_directory_permissions = change_permissions_main.reset_directory_permissions
change_directory_owner_group = change_permissions_main.change_directory_owner_group
change_file_owner_group = change_permissions_main.change_file_owner_group

#-------------------------#
# Define control switches #
#-------------------------#

remove_file_execb = True
reset_dir_permissions = True

chown_file = False
chown_dir = False
chgrp_file = False
chgrp_dir = False

#------------------------------------------#
# Define the list of extensions to exclude #
#------------------------------------------#

extensions2skip = ["gnu", "plt", "sh"]

#---------------------------------------------#
# Perform tasks according to control switches #
#---------------------------------------------#

# Design an informative table that will be printed whatever the case is #
extension_list = find_allfile_extensions(extensions2skip)

table='''
Extension list = {}
Extensions to exclude = {}

Number of extensions = {}
'''

print(table.format(extension_list,
                   extensions2skip,
                   len(extension_list)))

# Perform tasks according to the control switches # 
if remove_file_execb:
    remove_file_executability(cwd, extensions2skip)

if reset_dir_permissions:
    reset_directory_permissions(cwd)   

change_directory_owner_group(cwd, chown_dir, chgrp_dir)
change_file_owner_group(cwd, chown_file, chgrp_file, extensions2skip)
