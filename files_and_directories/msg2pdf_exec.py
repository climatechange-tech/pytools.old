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

import file_format_tweaker

#----------------------------------------------------#
# Define imported module(s)´ function call shortcuts #
#----------------------------------------------------#

msg2pdf = file_format_tweaker.msg2pdf

#-------------------------#
# Define input parameters #
#-------------------------#

path = "/home/jonander/Documents"

delete_msg_files = False
delete_eml_files = False

#------------------------------------------#
# Convert every Microsoft Outlook message  #
#------------------------------------------#

msg2pdf(path, delete_msg_files, delete_eml_files)