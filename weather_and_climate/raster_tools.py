#----------------#
# Import modules #
#----------------#

import os
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

custom_mod_path = f"{fixed_path}/strings"
                                        
# Add the module paths to the path variable #
#-------------------------------------------#

sys.path.append(custom_mod_path)

# Perform the module importations #
#---------------------------------#

import string_handler

#----------------------------------------------------#
# Define imported module(s)´ function call shortcuts #
#----------------------------------------------------#

obj_path_specs = string_handler.obj_path_specs
fileList2String = string_handler.fileList2String
obj_path_specs = string_handler.get_file_spec
modify_obj_specs = string_handler.modify_obj_specs

#-------------------------#
# Define custom functions #
#-------------------------#

def netCDF2raster(nc_file_list,
                  output_file_format,
                  raster_extension,
                  raster_resolution,
                  nodata_value=None,
                  crs="EPSG:4326"):
    
    if not isinstance(nc_file_list, list):
        nc_file_list = [nc_file_list]
    
    lncfl = len(nc_file_list)
    obj2change = "ext"
    
    for ncf_file in enumerate(nc_file_list):
        
        ncf_name = ncf_file[-1]
        ncf_num = ncf_file[0] + 1
        
        print(f"Converting netCDF file to raster...\n"
              f"{ncf_num} out of {lncfl}...")
        
        raster_file_name\
        = modify_obj_specs(ncf_name, obj2change, raster_extension)
    
        if nodata_value:
            zsh_rasterization\
            = f"gdal_translate -a_nodata {nodata_value} "\
              f"-a_srs {crs} "\
              f"-of {output_file_format} "\
              f"{ncf_name} {raster_file_name} "\
              f"--config GDAL_PDF_DPI {raster_resolution}"
            
        else:
            zsh_rasterization\
            = f"gdal_translate -of {output_file_format} "\
              f"-a_srs {crs} "\
              f"{ncf_name} {raster_file_name} "\
              f"--config GDAL_PDF_DPI {raster_resolution}"
                            
        os.system(zsh_rasterization)


def merge_independent_rasters(raster_files_dict,
                              output_file_format,
                              joint_region_name,
                              output_file_name_ext,
                              nodata_value=None):
    
    keys = list(raster_files_dict)
    lkeys = len(keys)
    
    list_lengths_set = set([len(raster_files_dict[key]) for key in keys])
    lls_length = len(list_lengths_set)

    if lls_length > 1:
        raise ValueError("Not every key list is of the same length!")
    
    else:
        
        lls_num = list(list_lengths_set)[0]
        obj2change = "name_noext_parts"
        
        for i in range(lls_num):
            
            print(f"Processing the files no. {i+1} out of {lls_num-(i+1)} "
                  f"of the {lkeys} regions...")
            
            raster_file_list = [raster_files_dict[key][i]
                                for key in keys]
            
            file_path_name_parts = obj_path_specs(raster_file_list[0],
                                                 file_spec_key=obj2change,
                                                 splitchar=splitchar)
            
            fpnp_changes_tuple = (file_path_name_parts[-2], joint_region_name)

            """It is assumed that every file follows
            the standard name described at module cdo_tools.py
            """
            
            output_file_name = modify_obj_specs(raster_file_list[0],
                                                 obj2change,
                                                 fpnp_changes_tuple)           
            
            zsh_allfile_string = fileList2String(raster_file_list)
            
            if nodata_value: 
                zsh_raster_merge = f"gdal_merge.py "\
                                   f"-o {output_file_name} "\
                                   f"-of {output_file_format} "\
                                   f"-a_nodata {nodata_value} "\
                                   f"{zsh_allfile_string}" 
            else:
                zsh_raster_merge = f"gdal_merge.py "\
                                   f"-o {output_file_name} "\
                                   f"-of {output_file_format} "\
                                   f"{zsh_allfile_string}"  
                                   
            os.system(zsh_raster_merge)


#-------------------------#
# Define global variables #
#-------------------------#
    
splitchar = "_"
