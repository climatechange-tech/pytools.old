#----------------#
# Import modules #
#----------------#

import importlib
import os
from pathlib import Path

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

module_imp1 = "string_handler.py"
module_imp1_path = f"{fixed_dirpath}/"\
                   f"strings/{module_imp1}"

spec1 = importlib.util.spec_from_file_location(module_imp1, module_imp1_path)
string_handler = importlib.util.module_from_spec(spec1)
spec1.loader.exec_module(string_handler)

#----------------------------------------------------#
# Define imported module(s)´ function call shortcuts #
#----------------------------------------------------#

file_path_specs = string_handler.file_path_specs
file_list_2_string = string_handler.file_list_2_string
join_file_path_specs = string_handler.join_file_path_specs

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
    
    for ncf_file in enumerate(nc_file_list):
        
        ncf_name = ncf_file[-1]
        ncf_num = ncf_file[0] + 1
        
        print(f"Converting netCDF file to raster...\n"
              f"{ncf_num} out of {lncfl}...")
        
        file_path_noname, file_path_name, file_path_name_split, file_path_ext\
        = file_path_specs(ncf_name, "_")
        
        file_path_ext = raster_extension
        raster_file_name = join_file_path_specs(file_path_noname,
                                                file_path_name,
                                                file_path_ext)
    
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
    
    splitchar = "_"

    if lls_length > 1:
        raise ValueError("Not every key list is of the same length!")
    
    else:
        
        lls_num = list(list_lengths_set)[0]
        for i in range(lls_num):
            
            print(f"Processing the files no. {i+1} out of {lls_num-(i+1)} "
                  f"of the {lkeys} regions...")
            
            raster_file_list = [raster_files_dict[key][i]
                                for key in keys]
            
            file_path_noname, file_path_name, file_path_name_split, file_path_ext\
            = file_path_specs(raster_file_list[0], splitchar)
            
            file_path_name_split[-2] = joint_region_name


            """It is assumed that every file follows
            the standard name described at module cdo_tools.py
            """
            file_path_name_new = splitchar.join(file_path_name_split)
            
            output_file_name = join_file_path_specs(file_path_noname,
                                                    file_path_name_new,
                                                    file_path_ext)            
            
            zsh_allfile_string = file_list_2_string(raster_file_list)
            
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
