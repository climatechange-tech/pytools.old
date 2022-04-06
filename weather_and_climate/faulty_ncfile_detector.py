#----------------#
# Import modules #
#----------------#

import importlib
from pathlib import Path

import xarray as xr

#---------------------------#
# Get the fixed directories #
#---------------------------#

cwd = Path.cwd()
main_path = Path("/".join(cwd.parts[:3])[1:]).glob("*/*")

# All-code containing directory #
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
        
def netcdf_file_scanner():
    
    #---------------------------------------------#
    # Define the input data directories and files #
    #---------------------------------------------#
    
    extension = "nc"
    ncfile_list = find_ext_file_paths(extension, cwd, top_path_only=True)
    lncfl = len(ncfile_list)

    #--------------------------------#
    # Initialise faulty file counter #
    #--------------------------------#
    
    faulty_ncf_counter = [lncfl, 0]
    faulty_ncf_list = []
    
    #------------------------#
    # Loop through all paths #
    #------------------------#
    
    for ncf in enumerate(ncfile_list):
        
        file_num = ncf[0] + 1
        file_name = ncf[-1]
        
        print(f"Scanning file no. {file_num} out of {lncfl} "
              f"at current directory...")
        
        try:
            ds = xr.open_dataset(file_name)
            ds.close()
        except:
            faulty_ncf_counter[-1] += 1
            faulty_ncf_list.append(file_name)
            
    return faulty_ncf_counter, faulty_ncf_list
    

def return_faulty_files():
    
    faulty_ncf_counter = netcdf_file_scanner()[0]
    faulty_ncf_list = netcdf_file_scanner()[1]
    
    ofile_name = "faulty_netcdf_file_report.txt"
    ofile = open(ofile_name, "w")
    
    output_table =\
"""·Total scanned files at the current directory: {}
·Faulty file number: {}
·Faulty files:
"""
    
    ofile.write(output_table.format(faulty_ncf_counter[0], 
                                    faulty_ncf_counter[-1]))
    
    for faulty_ncf in faulty_ncf_list:
        ofile.write(f"{faulty_ncf}\n")
    
    print("Faulty netCDF file report created.")
    ofile.close()
