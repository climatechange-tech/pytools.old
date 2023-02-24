#----------------#
# Import modules #
#----------------#

from pathlib import Path
import sys

import xarray as xr

#-----------------------#
# Import custom modules #
#-----------------------#

# Import module that finds python tools' path #
home_PATH = Path.home()
sys.path.append(str(home_PATH))

import get_pytools_path
fixed_dirpath = get_pytools_path.return_pytools_path()

# Enumerate custom modules and their paths #
#------------------------------------------#

custom_mod_path = f"{fixed_dirpath}/files_and_directories"
                                        
# Add the module path to the path variable #
#------------------------------------------#

sys.path.append(custom_mod_path)

# Perform the module importations #
#---------------------------------#

import file_and_directory_paths

#----------------------------------------------------#
# Define imported module(s)´ function call shortcuts #
#----------------------------------------------------#

find_ext_file_paths = file_and_directory_paths.find_ext_file_paths

#-------------------------#
# Define custom functions #
#-------------------------#

def binary_faulty_file_detector(ncfile_name):
    
    try:
        ds=xr.open_dataset(ncfile_name)
        ds.close()
        return 0
    
    except:
        return -1
        
def netcdf_file_scanner(path_to_walk_in, 
                        top_path_only=False,
                        extra_verbose=False):
    
    # Define the input data directories and files #
    #---------------------------------------------#
    
    if not isinstance(path_to_walk_in, list):        
        path_to_walk_in = [path_to_walk_in]
        
    for ptwi in path_to_walk_in:
        ncfile_list = find_ext_file_paths(extension,
                                          ptwi,
                                          top_path_only=top_path_only)
        lncfl = len(ncfile_list)
    
        # Initialise faulty file counter #
        #--------------------------------#
        
        faulty_ncf_counter = [lncfl, 0]
        faulty_ncf_list = []
        
        # Loop through all path list #
        #----------------------------#
        
        for ncf in enumerate(ncfile_list,start=1):
            
            file_num = ncf[0]
            file_name = ncf[-1]
            
            if not extra_verbose:
                print(scan_progress_table.format(file_num, lncfl,
                                                 ptwi),
                      end="\r")
            else:
                print(scan_progress_table_evb.format(file_name,
                                                     file_num, lncfl,
                                                     ptwi),
                      end="\r")
        
            try:
                ds = xr.open_dataset(file_name)
                ds.close()
            except:
                faulty_ncf_counter[-1] += 1
                faulty_ncf_list.append(file_name)
                
                
        # Create_faulty_ncfile_report #
        #-----------------------------#
        
        ofile_name = f"{codeCallDir}/faulty_netcdf_file_report.txt"
        ofile = open(ofile_name, "w")
        
        ofile.write(report_table.format(ptwi,
                                        faulty_ncf_counter[0], 
                                        faulty_ncf_counter[-1]))
        
        for faulty_ncf in faulty_ncf_list:
            ofile.write(f" {faulty_ncf}\n")
        
        print("Faulty netCDF file report created at the current directory.")
        ofile.close()
        

#------------------#
# Local parameters #
#------------------#

extension = "nc"

scan_progress_table =\
"""File number: {} out of {}
Directory: {}
"""

scan_progress_table_evb =\
"""
File: {}
File number: {} out of {}
Directory: {}
"""

report_table =\
"""Faulty NETCDF format file report
--------------------------------

·Directory: {}
·Total scanned files scanned: {}
·Faulty file number: {}

·Faulty files:
"""

codeCallDir = Path.cwd()