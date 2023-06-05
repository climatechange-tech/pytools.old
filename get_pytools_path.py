#----------------#
# Import modules #
#----------------#

from pathlib import Path
import os

#------------------#
# Define functions #
#------------------#

def return_pytools_path():

    disk_unit = cwd.parts[0]
    
    username = os.getlogin() 
    
    if "C" in disk_unit:
        pytools_path = f"{disk_unit}/Users/{username}/"\
                       f"OneDrive - ACCIONA S.A\Documents/{key_dir}"
                       
    elif "R" in disk_unit:
        pytools_path = f"{disk_unit}/FORMACION/CURSOS/"\
                       f"Curso_JonAnder-Pablo_Marzo2023/{key_dir}"
     
    return pytools_path

#-------------------------#
# Define local parameters #
#-------------------------#

cwd = Path.cwd()
key_dir = "pytools"