#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 3 21:19:13 2023

@author: jonander
"""

#----------------#
# Import modules #
#----------------#

from pathlib import Path
import sys

# Find the path of the Python toolbox #
home_PATH = Path.home()
sys.path.append(str(home_PATH))

import get_pytools_path
fixed_path = get_pytools_path.return_custom_path()

# Enumerate custom modules and their paths #
#------------------------------------------#

custom_mod1_path = f"{fixed_path}/arrays_and_lists"
custom_mod2_path = f"{fixed_path}/files_and_directories"  
custom_mod3_path = f"{fixed_path}/strings"
custom_mod4_path = f"{fixed_path}/time_handling"
custom_mod5_path = f"{fixed_path}/weather_and_climate"
                                        
# Add the paths to the 'path' attribute of module 'sys' #
#-------------------------------------------------------#

sys.path.append(custom_mod1_path)
sys.path.append(custom_mod2_path)
sys.path.append(custom_mod3_path)
sys.path.append(custom_mod4_path)
sys.path.append(custom_mod5_path)

# Perform whole or partial module importations #
#----------------------------------------------#

import array_handler
import cds_tools
import file_and_directory_handler
import file_and_directory_paths
import netcdf_handler
import program_snippet_exec_timers
import string_handler

#--------------------------------------------------#
# Define imported modules' function call shortcuts #
#--------------------------------------------------#

select_from_array_element = array_handler.select_from_array_element

download_data = cds_tools.download_data

make_parent_directories = file_and_directory_handler.make_parent_directories
move_files_by_ext_from_exec_code = file_and_directory_handler.move_files_byExts_fromCodeCallDir

find_files_by_globstr = file_and_directory_paths.find_files_by_globstr

netcdf_file_scanner = netcdf_handler.netcdf_file_scanner

program_exec_timer = program_snippet_exec_timers.py.program_exec_timer

find_substring_index = string_handler.find_substring_index
substring_replacer = string_handler.substring_replacer 

#-------------------------#
# Define custom functions #
#-------------------------#

def check_correct_domain(domain):
    if domain not in available_domains:
        raise ValueError(f"Wrong product. Options are '{available_domains}'.")
   
        
def return_rcp_std(rcp):
    
    try:
        rcp_num = eval(rcp)            
    except:            
        if rcp not in available_rcps:
            raise ValueError(f"Wrong RCP scenario. Options are '{available_rcps}'.")
        else:
            return rcp
        
    else:
        if not (isinstance(rcp_num, (float, str))):
            raise ValueError(f"Wrong RCP scenario. Options are '{available_rcps}'.")
        else:
            rcp_mod = substring_replacer(rcp, charSplitDelim1, charSplitDelim2)  
            rcp_std = f"rcp_{rcp_mod}"
            
            if rcp_std not in available_rcps:
                raise ValueError(f"Wrong RCP scenario. Options are '{available_rcps}'.")
            else:
                return rcp_std
        
        
def check_correct_gcm(gcm):
    if gcm not in available_gcms:
        raise ValueError(f"Wrong GCM. Options are '{available_gcms}'.")
        
        
def check_correct_rcm(rcm):
    if rcm not in available_rcms:
        raise ValueError(f"Wrong rcm. Options are '{available_rcms}'.")
        
    
def return_rcp_period(rcp):
    local_vals = list(locals())
    rcp_abbr = rcp[:4]
    
    rcp_local_key_idx = find_substring_index(local_vals, rcp_abbr)
    rcp_local_key = select_from_array_element(local_vals, rcp_local_key_idx)
    
    return rcp_local_key
    
    
        
def return_file_extension(file_format):
    extension_idx = find_substring_index(available_formats, file_format)
    
    if extension_idx == -1:
        raise ValueError(f"Wrong file format. Options are '{available_formats}'.")
    else:
        extension = available_extensions[extension_idx]
        return extension
    

def return_horizontal_std_resolution(h_resolution):
    if h_resolution not in available_h_resolutions:
        raise ValueError(f"Wrong horizontal resolution. Options are {available_h_resolutions}")
    else:
        h_resolution1 = substring_replacer(h_resolution,
                                           charSplitDelim1,
                                           charSplitDelim2)
        
        h_resolution_std = f"{h_resolution1}_x_{h_resolution1}_degree"
        return h_resolution_std
    
    
def check_correct_temporal_resolution(t_resolution):    
    if t_resolution not in available_t_resolutions:
        raise ValueError(f"Wrong temporal resolution. Options are {available_t_resolutions}")    
           
#---------------------#
# Variable parameters #
#---------------------#

# Project name #
project_name = "climate-change"

# Domain #
domain = "Africa"
check_correct_domain(domain)

# RCP (experiment) number #
rcp = "2.6"
return_rcp_std(rcp)

# Horizontal resolution #
h_resolution = "0.11"

# Temporal resolution #
t_resolution = "daily_mean"

# Variables #
variable_list = [
    'maximum_temperature',
    'mean_temperature',
    'minimum_temperature',
    'precipitation_amount'
    ]

# Climate models #
#----------------#

# GCM #
gcm = "ichec-ec-earth"
check_correct_gcm(gcm)

# RCM #
rcm = "smhi-rca4"
check_correct_rcm(rcm)

# Ensemble member #
#-----------------#

ensemble = "r1i1p1"

# Downloadable formats and extensions #
#-------------------------------------#

file_format = "zip"
extension = return_file_extension(file_format)

# Date and times #
#----------------#

# Start #
eval_start_ys = [f"{i:04d}" for i in range(1979,2019)]
hist_start_ys = [f"{i:04d}" for i in range(1948,2006)]
rcp_all_start_ys = [f"{i:04d}" for i in range(2005,2100)]

sel_rcp_start_ys = return_rcp_std(rcp)[0]

# End #
eval_end_ys = [f"{i:04d}" for i in range(1979,2019)]
hist_end_ys = [f"{i:04d}" for i in range(1948,2006)]
rcp_all_end_ys = [f"{i:04d}" for i in range(2005,2100)]

sel_rcp_end_ys = return_rcp_std(rcp)[1]

#------------------#
# Fixed parameters #
#------------------#

# Character splitting delimiters #
charSplitDelim1 = "."
charSplitDelim2 = "_"

# Main directories #
#------------------#

# Project (main) directory #
project_dir = f"{fixed_path}/test-base_programs/{project_name}"

# Code-containing directory #
codes_dir = f"{project_dir}/codes"

# Input (downloaded) data main directory #
main_input_data_dir = f"{project_dir}/input_data"

# Dataset #
#---------#

dataset = "CORDEX"
dataset_lower = dataset.lower()

# Product attributes #
#--------------------#

# Product name #
product_name = f"projections-{dataset_lower}-domains-single-levels"

# Domains #
#---------#

domain_kw = "domain"

available_domains = [
    "africa",
    "antarctic",
    "arctic",
    "australasia",
    "central_america",
    "central_asia",
    "east_asia",
    "europe",
    "mediterranean",
    "middle_east_and_north_africa",
    "north_america",
    "south_america",
    "south-east_asia",
    "south_asia"
    ]

# RCP (experiment) number #
#-------------------------#

rcp_kw = "experiment"

available_rcps = [
    "evaluation",
    "historical",
    "rcp_2_6",
    "rcp_4_5",
    "rcp_8_5"
    ]

# Date and times #
#----------------#

start_year_kw = "start_year"
end_year_kw = "end_year"

# Horizontal resolution #
#-----------------------#

h_resolution_kw = "horizontal_resolution"

available_h_resolutions = ["0.11", "0.20", "0.22", "0.44", "interpolated_0.44"]
h_resolution_std = return_horizontal_std_resolution(h_resolution)

# Temporal resolution #
#---------------------#

t_resolution_kw = "temporal_resolution"

available_t_resolutions = [
    "daily_mean",
    "monthly_mean",
    "seasonal_mean",
    "3_hours",
    "6_hours",
    "fixed"
    ]

check_correct_temporal_resolution(t_resolution)

# Variables #
#-----------#

variable_kw = "variable"

# Climate models #
#----------------#

# GCM #
gcm_kw = "gcm_model"

available_gcms = [
    "cccma_canesm2",
    "cnrm_cerfacs_cm5",
    "csiro_bom_access1_0",
    "csiro_bom_access1_3",
    "csiro_qccce_csiro_mk3_6_0",
    "era_interim",
    "ichec_ec_earth",
    "ipsl_cm5a_lr",
    "ipsl_cm5a_mr",
    "miroc_miroc5",
    "mohc_hadgem2_es",
    "mpi_m_mpi_esm_lr",
    "mpi_m_mpi_esm_mr",
    "ncar_ccsm4",
    "ncc_noresm1_m",
    "noaa_gfdl_gfdl_esm2g",
    "noaa_gfdl_esm2m"
    ]

# RCM #
rcm_kw = "rcm_model"

available_rcms = [
    "awi_hirham5",
    "bccr_wrf331",
    "boun_regcm4_3",
    "cccma_canrcm4",
    "clmcom_btu_cclm4_8_17",
    "clmcom_clm_cclm4_8_17",
    "clmcom_cclm4_8_17_clm3_5",
    "clmcom_cclm5_0_2",
    "clmcom_eth_cosmo_crclim",
    "clmcom_hzg_cclm5_0_15",
    "clmcom_kit_cclm5_0_15",
    "cmcc_cclm4_8_19",
    "cnrm_aladin52",
    "cnrm_aladin53",
    "cnrm_aladin63",
    "csiro_ccam_2008",
    "cyi_wrf351",
    "dmi_hirham5",
    "elu_regcm4_3",
    "gerics_remo2009",
    "gerics_remo2015",
    "guf_cclm4_8_18_germany",
    "ictp_regcm4_3",
    "ictp_regcm4_4",
    "ictp_regcm4_6",
    "ictp_regcm4_7",
    "iitm_regcm4_4",
    "inpe_eta",
    "ipsl_wrf381p",
    "isu_regcm4",
    "knmi_racmo21p",
    "knmi_racmo22e",
    "knmi_racmo22t",
    "lmd_lmdz4nemomed8",
    "mgo_rrcm",
    "mohc_hadrem3_ga7_05",
    "mohc_hadrm3p",
    "mpi_csc_remo2009",
    "ncar_regcm4",
    "ncar_wrf",
    "ornl_regcm4_7",
    "ouranos_crcm5",
    "rmib_ugent_alaro_0 ",
    "ru_core_regcm4_3",
    "smhi_rca4",
    "smhi_rca4_sn",
    "ua_wrf",
    "ucan_wrf341i",
    "uhoh_wrf361h",
    "ulg_mar311",
    "ulg_mar36",
    "unsw_wrf360j",
    "unsw_wrf360k",
    "unsw_wrf360l",
    "uqam_crcm5",
    "uqam_crcm5_sn"
    ]

# Ensemble member #
#-----------------#

ensemble_kw = "ensemble_member"

# Downloadable formats and extensions #
#-------------------------------------#

format_kw = "format"

available_formats = ["zip", "tgz"]
available_extensions = ["zip", "tar.gz"]


#--------------------#
# Initialize program #
#--------------------#

program_exec_timer('start')

#-----------------------------------#
# Loop through the different ranges #
#-----------------------------------#

"""
Create, if necessary, the input data directory
specific both for the data set and domain.
"""

ds_input_data_dir = f"{main_input_data_dir}/{dataset}/{domain}"
make_parent_directories(ds_input_data_dir)

"""
It is possible that there will not be data for certain period(s) of time,
or if it is the case, not every variable will be available.

Analyzing each and every one of the possibilities requires
a great effort, but there is no way to catch the 
exit status of the downloading process, so if there is an error,
the CDS API will specify the type thereof and will lead to a program halt.

However, at least for a little guidance, options for the following
variables have been included. These can change over time:
    
    1. Domain
    2. Experiment
    3. GCM
    4. RCM
"""

for start_year, end_year in zip(sel_rcp_start_ys, sel_rcp_end_ys):
                    
    # Set the keyword argument dictionary to pass in later on #
    kwargs = {
        domain_kw : domain,
        rcp_kw : rcp,
        h_resolution_kw : h_resolution,
        t_resolution_kw : t_resolution,
        variable_kw : variable_list,
        gcm_kw : gcm,
        rcm_kw : rcm,
        ensemble_kw : ensemble,
        start_year_kw : start_year,
        end_year_kw : end_year,                        
        format_kw : file_format,
        }
    
    # Gather every parameter to form the output file name #
    output_file_name = f"{dataset_lower}-{gcm}-{rcm}-{ensemble}-"\
                       f"{h_resolution}-{t_resolution}-{start_year}.{extension}"

    """
    Test whether the file is already downloaded
    (current or downloaded data directory)
    """
    ofn_list = find_files_by_globstr(f"*{output_file_name}*",
                                     path_to_walk_into=project_dir)
    
    lofnl = len(ofn_list)
    
    if lofnl > 0:
        num_faulty_ncfiles\
        = netcdf_file_scanner(path_to_walk_into=codes_dir)
        
        if num_faulty_ncfiles > 0:   
            # Download the specified data #
            download_data(product_name, output_file_name, **kwargs)
            
    else:
        # Download the specified data #
        download_data(product_name, output_file_name, **kwargs)                                 
                

# Move the downloaded data from the directory where the code is being called #
move_files_by_ext_from_exec_code(extension, ds_input_data_dir)

#---------------------------------------#
# Calculate full program execution time #
#---------------------------------------#

program_exec_timer('stop')
