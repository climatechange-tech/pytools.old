"""
**Note**

Run this program if it is the first time using the repository
or it has been re-cloned.
"""

#----------------#
# Import modules #
#----------------#

import os
from pathlib import Path
import shutil

#------------------#
# Input parameters #
#------------------#

# Home path #
home_path = Path.home()

# Default path (same as the current one) 
default_path = Path.cwd()
default_path_str = str(default_path)

# Ask the user if other than the default is preferred #
custom_path\
= str(input(f"Where do you want to establish the repository? [{default_path}] >>> "))

# Path establisher function replica #
custom_path_establisher_func = """def return_custom_path():
    custom_path = "{}"
    return custom_path
"""
# Repo path retriever file attrs. #
custom_path_retriever_name = "get_custom_path.py"
custom_path_retriever_path = f"{home_path}/{custom_path_retriever_name}"

#----------------#
# Operation part #
#----------------#

lcp = len(custom_path)

# If 'Enter' key is hit, then set the path to the default one #
#-------------------------------------------------------------#

if lcp == 0:
    custom_path = default_path
    
# Otherwise, move the repo to the specified path #
#------------------------------------------------#

else:  
    
    # Define custom path with the directory as the current, default one #
    default_dir = default_path.stem
    customPathWithDefaultDir = f"{custom_path}/{default_dir}" 
    
    """
    On Windows there is a problem when copying directories,
    because some path can have double and/or quadruple backlashes and
    forward slashes mixed, which is not practical to correct.
    Instead, copy the entire directory and then delete the default one.
    """
    shutil.copytree(default_path, customPathWithDefaultDir, dirs_exist_ok=True)
    
    print(f"Changed path from '{default_path}' to '{custom_path}'.")
    
    os.chdir(f"{default_path}/..")
    shutil.rmtree(default_path, ignore_errors=True)
    
    print(f"Deleted default path '{default_path}', but"
          f"Git version controller directory '.git' will still be present.\n"
          "Please delete the mentioned path manually.")
    
#------------------------------------------------------------------------------#
# In either case, write a file containing a function that returns the path set #
#------------------------------------------------------------------------------#

"""
All modules are optimized so that the file that returns the path of this repo
is stored at /home directory.
"""

custom_path_retriever = open(custom_path_retriever_path,'w')
custom_path_retriever.write(custom_path_establisher_func.format(custom_path))
custom_path_retriever.close()