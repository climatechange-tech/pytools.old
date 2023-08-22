"""
**Note**

This program is an application of the main module 'change_permissions_main.py',
and it uses the 'modify_obj_permissions' and 'modify_obj_owner' 
attributes or functions.
PLEASE DO NOT REDISTRIBUTE this program along any other directory,
as the module is designed to work with absolute paths.
"""

#----------------#
# Import modules #
#----------------#

from pathlib import Path
import sys

#-----------------------#
# Import custom modules #
#-----------------------#

# Import module that finds python tools' path #
home_PATH = Path.home()
sys.path.append(str(home_PATH))

import get_pytools_path
fixed_path = get_pytools_path.return_custom_path()

# Enumerate custom modules and their paths #
#------------------------------------------#

custom_mod_path = f"{fixed_path}/files_and_directories"
                                        
# Add the module paths to the path variable #
#-------------------------------------------#

sys.path.append(custom_mod_path)

# Perform the module importations #
#---------------------------------#

import change_permissions_main

#----------------------------------------------------#
# Define imported module(s)´ function call shortcuts #
#----------------------------------------------------#

modify_obj_permissions = change_permissions_main.modify_obj_permissions
modify_obj_owner = change_permissions_main.modify_obj_owner

#-------------------------#
# Define input parameters #
#-------------------------#

path = "/home/jonander/Documents"

# Main task control switches #
#----------------------------#

make_obj_perm_mods = False
make_obj_owner_mods = False

# General parameters #
obj_type = "file"
extensions2skip = ""

# Specific parameter oriented to object permission modification #
attr_id = 644

# Specific parameters oriented to object owner modification #
module = "shutil"

"""
**Note**

If there is no need to change the user and/or group name,
please set one or both of the following to None or 'unchanged'.
"""

new_owner = None
new_group = None

#-------------------------------------------------------------#
# Perform the tasks according to the values of the parameters #
#-------------------------------------------------------------#
    
if make_obj_perm_mods:
    modify_obj_permissions(path,
                           obj_type,
                           extensions2skip,
                           attr_id)

if make_obj_owner_mods:
    modify_obj_owner(path,
                     module,
                     obj_type,
                     extensions2skip,
                     new_owner,
                     new_group)
