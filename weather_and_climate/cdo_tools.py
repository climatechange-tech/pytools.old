#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#5
# Import modules #
#----------------#

from pathlib import Path
import sys

#-----------------------#
# Import custom modules #
#-----------------------#

# Find the path of the Python toolbox #
home_PATH = Path.home()
sys.path.append(str(home_PATH))

import get_pytools_path
fixed_path = get_pytools_path.return_custom_path()

# Enumerate custom modules and their paths #
#------------------------------------------#

custom_mod1_path = f"{fixed_path}/files_and_directories" 
custom_mod2_path = f"{fixed_path}/operative_systems"  
custom_mod3_path = f"{fixed_path}/parameters_and_constants"  
custom_mod4_path = f"{fixed_path}/strings"
custom_mod5_path = f"{fixed_path}/weather_and_climate"
                                        
# Add the paths to the 'path' attribute of module 'sys' #
#-------------------------------------------------------#

sys.path.append(custom_mod1_path)
sys.path.append(custom_mod2_path)
sys.path.append(custom_mod3_path)
sys.path.append(custom_mod4_path)

# Perform whole or partial module importations #
#----------------------------------------------#

from file_and_directory_handler import rename_objects
import global_parameters
from information_output_formatters import format_string
import netcdf_handler
from os_operations import exec_shell_command
import string_handler

#----------------------------------------------------#
# Define imported module(s)' function call shortcuts #
#----------------------------------------------------#

basic_four_rules = global_parameters.basic_four_rules
common_splitdelim_list = global_parameters.common_splitdelim_list
freq_abbrs = global_parameters.time_frequencies_shorter_1
time_freqs = global_parameters.time_frequencies_short_1

get_file_variables = netcdf_handler.get_file_variables
find_time_dimension_raise_none = netcdf_handler.find_time_dimension_raiseNone
get_times = netcdf_handler.get_times

add_str_to_aux_path = string_handler.aux_path_strAdd
find_substring_index = string_handler.find_substring_index
file_list_to_str = string_handler.fileList2String
obj_path_specs = string_handler.get_file_spec
modify_obj_specs = string_handler.modify_obj_specs

#-------------------------#
# Define custom functions #
#-------------------------#

# Character string processing #
#-----------------------------#
                    
def get_variable_name_in_file_name(file,
                                   return_std_varname=False,
                                   varlist_original=None,
                                   varlist_standardized=None):
        
    fsk = "name_noext_parts"
    file_path_name_noext_parts = obj_path_specs(file,
                                                file_spec_key=fsk,
                                                splitdelim=splitdelim1)
                                
    # Usually the first part of the file name is precisely the variable name #
    var_file = file_path_name_noext_parts[0]
    
    if return_std_varname:
        
        # Find the variable in the provided original variable list #
        var_pos = find_substring_index(varlist_original, var_file)
        
        if var_pos != -1:
            var_std = varlist_standardized[var_pos]
            return var_std
        
        else:
            raise ValueError(f"Variable '{var_file}' found at file '{file}' "
                             f"not present at original variable list {varlist_original}.")
            
    else:
        return var_file
            

def change_file_names_byvar(file_list,
                            varlist_original,
                            varlist_standardized):

    obj2change = "name_noext_parts"
    
    for file in file_list:
        
        var_std = get_variable_name_in_file_name(file,
                                              True,
                                              varlist_original, 
                                              varlist_standardized)
        
        file_path_name_parts = obj_path_specs(file, 
                                             file_spec_key=obj2change,
                                             splitdelim=splitdelim1)
        
        fpnp_changes_tuple = (file_path_name_parts[0], var_std)
        varname_changed_file_path_name = modify_obj_specs(file, 
                                                           obj2change,
                                                           fpnp_changes_tuple)
              
        rename_objects(file, varname_changed_file_path_name)

# Miscellaneous operations #
#--------------------------#

def standardize_file_name(variable,
                          time_freq,
                          model,
                          experiment,
                          calculation_method,
                          period,
                          region,
                          extension):

    standard_name = f"{variable}_"\
                    f"{time_freq}_"\
                    f"{model}_"\
                    f"{experiment}_"\
                    f"{calculation_method}_"\
                    f"{region}_"\
                    f"{period}.{extension}"
                    
    return standard_name


def cdo_sellonlatbox(file_list,
                     coordinate_list,
                     time_freq,
                     model,
                     experiment,
                     calculation_method,
                     region,
                     extension):

    for file in file_list:                 
        variable = get_variable_name_in_file_name(file)
            
        time_var = find_time_dimension_raise_none(file)
        times = get_times(file, time_var)
            
        start_year = f"{times.dt.year.values[0]}"
        end_year = f"{times.dt.year.values[-1]}"
        
        period = f"{start_year}-{end_year}"
        
        standardized_output_file_name = standardize_file_name(variable,
                                                              time_freq,
                                                              model,
                                                              experiment,
                                                              calculation_method,
                                                              period,
                                                              region,
                                                              extension)
        
        sellonlatbox_command = f"cdo sellonlatbox,{coordinate_list} "\
                               f"'{file}' {standardized_output_file_name}"
        exec_shell_command(sellonlatbox_command)


def cdo_mergetime(file_list,
                  variable,
                  time_freq,
                  model,
                  experiment,
                  calculation_method,
                  period,
                  region,
                  extension):
                       
    standardized_output_file_name = standardize_file_name(variable,
                                                          time_freq,
                                                          model,
                                                          experiment,
                                                          calculation_method,
                                                          period,
                                                          region,
                                                          extension)
    
    start_year = f"{period.split(splitdelim2)[0]}"
    end_year = f"{period.split(splitdelim2)[-1]}"
    
    fsk = "name_noext_parts"
    
    file_list_selyear\
    = [file
       for file in file_list
       if (year := obj_path_specs(file, fsk, splitdelim1)[-1])
       >= start_year
       and year
       <= end_year]
    
    
    
    allfiles_string = file_list_to_str(file_list_selyear)
    mergetime_command = f"cdo -b F64 -f nc4 mergetime '{allfiles_string}' "\
                        f"{standardized_output_file_name}"
    exec_shell_command(mergetime_command)
    
    
def custom_cdo_mergetime(file_list,
                         custom_output_file_name,
                         create_temporal_file=False):
    
    allfiles_string = file_list_to_str(file_list)
    
    if not create_temporal_file:
        mergetime_command = f"cdo -b F64 -f nc4 mergetime '{allfiles_string}' "\
                            f"{custom_output_file_name}"
    else:
        temp_file = add_str_to_aux_path(file_list[0])
        mergetime_command = f"cdo -b F64 -f nc4 mergetime '{allfiles_string}' "\
                            f"{temp_file}"
                     
    exec_shell_command(mergetime_command)
        
    
def cdo_selyear(file_list,
                selyear_string,
                time_freq,
                model,
                experiment,
                calculation_method,
                region,
                extension):
    
    
    fsk = "name_noext_parts"
    selyear_string_split = obj_path_specs(selyear_string, 
                                          file_spec_key=fsk,
                                          splitdelim=splitdelim2)
    
    start_year = f"{selyear_string_split[0]}"
    end_year = f"{selyear_string_split[-1]}"
    
    selyear_string_cdo = f"{start_year}/{end_year}"   
    period_selyear = f"{start_year}-{end_year}"    
    
    for file in file_list:
        variable = get_variable_name_in_file_name(file)
        
        standardized_output_file_name = standardize_file_name(variable,
                                                              time_freq,
                                                              model,
                                                              experiment,
                                                              calculation_method,
                                                              period_selyear,
                                                              region,
                                                              extension)
     
        selyear_command = f"cdo selyear,{selyear_string_cdo} "\
                          f"'{file}' {standardized_output_file_name}"
        exec_shell_command(selyear_command)
        
    
def cdo_anomalies(input_file_full_time,
                  input_file_freq_avg,
                  variable,
                  time_freq,
                  model,
                  experiment,
                  calculation_method,
                  period,
                  region,
                  extension):
                       
    standardized_output_file_name = standardize_file_name(variable,
                                                          time_freq,
                                                          model,
                                                          experiment,
                                                          calculation_method,
                                                          period,
                                                          region,
                                                          extension)
 
    anomaly_calc_command = f"cdo sub '{input_file_freq_avg}' '{input_file_full_time}' "\
                           f"{standardized_output_file_name}"
    exec_shell_command(anomaly_calc_command)


def cdo_shifttime(file_list,
                  shift_value):
                       
    for file in file_list:
        
        temp_file = add_str_to_aux_path(file)
        
        shifttime_command = f"cdo shifttime,{shift_value} '{file}' '{temp_file}'"
        exec_shell_command(shifttime_command)
        
        rename_objects(temp_file, file)
        
        
def cdo_inttime(file_list,
                year0,
                month0,
                day0,
                hour0,
                minute0,
                second0,
                time_step):
    
    for file in file_list:
        
        temp_file = add_str_to_aux_path(file)
        star_date_format = f"{year0}-{month0}-{day0} "\
                           f"{hour0:2d}:{minute0:2d}:{second0:2d}"
        
        inttime_command = f"cdo inttime,{star_date_format},{time_step} "\
                          f"'{file}' '{temp_file}'"
        exec_shell_command(inttime_command)
        
        rename_objects(temp_file, file)
  
    
def cdo_rename(file_list, 
               varlist_original,
               varlist_standardized):
    
    lfl = len(file_list)
    
    for file_num, file_name in enumerate(file_list, start=1):

        # Find the variable in the provided original variable list #   
        var_file = get_file_variables(file_name)
        
        # Find the standardized variable, provided the std variable list #        
        var_std = get_variable_name_in_file_name(file_name,
                                              True,
                                              varlist_original,
                                              varlist_standardized)
            
        print(f"Renaming original variable '{var_file}' to '{var_std}' "
              f"on file {file_num} out of {lfl}...")
    
        file_name_chname = add_str_to_aux_path(file_name, 
                                                     splitdelim1)
        chname_command = f"cdo chname,{var_file},{var_std} "\
                         f"'{file_name}' '{file_name_chname}'"
        exec_shell_command(chname_command)
    
        # Rename the cdo output file name to the original one #
        rename_objects(file_name_chname, file_name)
        
# Mathematic and statistical operations #
#---------------------------------------#

def cdo_time_mean(input_file,
                  variable,
                  time_freq,
                  model,
                  experiment,
                  calculation_method,
                  period,
                  region,
                  extension):
                       
    standardized_output_file_name = standardize_file_name(variable,
                                                          time_freq,
                                                          model,
                                                          experiment,
                                                          calculation_method,
                                                          period,
                                                          region,
                                                          extension)
 
    time_mean_command = f"cdo -{calculation_method} '{input_file}' "\
                        f"{standardized_output_file_name}"
    exec_shell_command(time_mean_command)
    

def cdo_remap(file_list,
              remap_method_str,
              variable,
              time_freq,
              model,
              experiment,
              calculation_method,
              period,
              region,
              extension,
              remap_method="bilinear"):
    
    standardized_output_file_name = standardize_file_name(variable,
                                                          time_freq,
                                                          model,
                                                          experiment,
                                                          calculation_method,
                                                          period,
                                                          region,
                                                          extension)
    
    if remap_method not in cdo_remap_options:
        arg_tuple_remap = ("remapping option", cdo_remap_options)
        raise ValueError(choice_error_str, arg_tuple_remap)
         
    else:
        remap_method_cdo = cdo_remap_option_dict.get(remap_method_str)
     
        for file in file_list:            
            remap_command = f"cdo {remap_method_cdo},{remap_method_str} "\
                            f"'{file}' {standardized_output_file_name}" 
            exec_shell_command(remap_command)
        
        
def create_grid_header_file(output_file, **kwargs):
    """ Create grid header

    Parameters
    ----------
    output_file: str or Path
                 Path to the txt file where the reference grid will be stored.
    kwargs:
            Parameters that define the grid (e.g. xmin, ymax, total lines,
            total columns, etc.).

    Returns
    -------
    None

    """
    
    kwargs_values = list(kwargs.values())
    kwargs_keys = list(kwargs.keys())
    kwargs_keys.sort()
    
    if kwargs_keys != keylist:
        kwargs = {key : val 
                  for key,val in zip(keylist,kwargs_values)}
    
    #%%
    grid = \
"""gridtype  = lonlat
xsize     = {0:d}
ysize     = {1:d}
xname     = longitude
xlongname = "Longitude values"
xunits    = "degrees_east"
yname     = latitude
ylongname = "Latitude values"
yunits    = "degrees_north"
xfirst    = {2:.20f}
xinc      = {3:.20f}
yfirst    = {4:.20f}
"""
    
    arg_tuple = tuple([kwargs[keylist[i]] for i in range(6)])
    grid_formatted = format_string(grid, arg_tuple)
        
    output_file_object = open(output_file, 'w')
    output_file_object.write(grid_formatted)
    output_file_object.close()

        
def cdo_periodic_statistics(nc_file_name, statistic, isclimatic, freq, season_str=None):
    
    """
    Function to calculate basic statistics (included climatologies)
    with netCDF files, without the need of opening them.
    
    Notes
    -----
    It is not recommended to use output file names within
    those functions that calculate deltas,
    since doing so lowers disk I/O performance.
    """
    
    # Quality control #
    if statistic not in statistics:
        raise ValueError(format_string(choice_error_str, statistics))
        
    # Identify the abbreviature for the selected time frequency #
    period_abbr_idx = find_substring_index(time_freqs, freq)
  
    if period_abbr_idx == -1:
        arg_tuple_period_stats = ("time-frequency", time_freqs)
        raise ValueError(choice_error_str, arg_tuple_period_stats)
    else:
        period_abbr = freq_abbrs[period_abbr_idx]
        
    # Determine whether to calculate the climatological statistic #
    if not isclimatic:
        statname = f"{period_abbr}{statistic}"            
    else:
        statname = f"y{period_abbr}{statistic}"
        
    if period_abbr == freq_abbrs[3]:
        if season_str is not None:
            statname += f" -select,season={season_str}"
            
    # Get the file name for string manipulation #
    file_path_name\
    = add_str_to_aux_path(nc_file_name, return_file_name_noext=True)
    
    """Special case for seasonal time frequency"""
    if season_str is not None:
        statname_season = f"{statname.split()[0]}_{statname[-3:]}"
        string2add = f"{splitdelim1}{statname_season}"
        file_path_name_longer = add_str_to_aux_path(file_path_name, string2add)
        
    else:
        string2add = f"{splitdelim1}{statname}"
        file_path_name_longer = add_str_to_aux_path(file_path_name, string2add)
        
    # Define the output file name based on the configuration chosen #
    obj2change = "name_noext"
    output_file_name\
    = modify_obj_specs(nc_file_name, obj2change, file_path_name_longer)
        
    # Perform the computation #
    cdo_stat_command = f"cdo {statname} {nc_file_name} {output_file_name}"
    exec_shell_command(cdo_stat_command)

    
def calculate_periodic_deltas(projected_ncfile,
                              historical_ncfile,
                              operator="+",
                              delta_period="monthly",
                              proj_model=None):
    
    period_abbr_idx = find_substring_index(time_freqs_delta, delta_period) 
    delta_calc_filename = add_str_to_aux_path(historical_ncfile, 
                                              return_file_name_noext=True)

    if proj_model is None:
        raise ValueError("The model name's position contained on the file name "\
                         f"{projected_ncfile} can vary significantly "\
                         "from files belonging to one project from another. "\
                         "It is safer to manually define the model used "\
                         "for projections.")

    if period_abbr_idx == -1:
        raise ValueError(format_string(choice_error_str, arg_tuple_delta1))
    else:
        period_abbr = freq_abbrs_delta[period_abbr_idx]
    
    hist_mean_command = f"-y{period_abbr}mean {historical_ncfile}"
    proj_mean_command = f"-y{period_abbr}mean {projected_ncfile}"

    string2add = f"{period_abbr}Deltas_{proj_model}.nc"
    delta_calc_filename_longer = add_str_to_aux_path(delta_calc_filename, string2add)
    
    if operator not in basic_four_rules:
        raise ValueError(format_string(choice_error_str, arg_tuple_delta2))
    else:  
        cdo_operator_str = cdo_operator_str_dict.get(operator)
        arg_tuple_delta_calc = (cdo_operator_str,
                               hist_mean_command, proj_mean_command,
                               delta_calc_filename_longer)
                                           
        delta_calc_command = format_string(deltaCalc_command_dict.get(operator),
                                           arg_tuple_delta_calc)
        exec_shell_command(delta_calc_command)
    

def apply_periodic_deltas(projected_ncfile,
                          historical_ncfile,
                          operator="+",
                          delta_period="monthly",
                          proj_model=None):
    
    
    period_abbr_idx = find_substring_index(time_freqs_delta, delta_period)
    delta_apply_fn = add_str_to_aux_path(historical_ncfile, 
                                      return_file_name_noext=True)
    
    if proj_model is None:
        raise ValueError("The model name's position contained on the file name "\
                         f"{projected_ncfile} can vary significantly "\
                         "from files belonging to one project from another. "\
                         "It is safer to manually define the model used "\
                         "for projections.")

    if period_abbr_idx == -1:
        arg_tuple_periodic_delta1 = ("time-frequency", time_freqs_delta)
        raise ValueError(format_string(choice_error_str, arg_tuple_periodic_delta1))
    else:
        period_abbr = freq_abbrs_delta[period_abbr_idx]
        
    string2add = f"{period_abbr}DeltaApplied_{proj_model}.nc"
    delta_apply_fn_longer = add_str_to_aux_path(deltaApply_fn, string2add)
    
    hist_mean_command = f"-y{period_abbr}mean {historical_ncfile}"
    
    if operator not in basic_four_rules:
        arg_tuple_periodic_delta2 = ("basic operator", basic_four_rules)
        raise ValueError(format_string(choice_error_str, arg_tuple_periodic_delta2))
    else:   
        cdo_operator_str = cdo_operator_str_dict.get(operator)
        arg_tuple_delta_apply = (period_abbr, cdo_operator_str,
                                projected_ncfile, hist_mean_command,
                                delta_apply_fn_longer)
                                           
        delta_apply_command = format_string(deltaApply_command_dict.get(operator),
                                           arg_tuple_delta_apply)
        exec_shell_command(delta_apply_command)
        
    
#--------------------------#
# Parameters and constants #
#--------------------------#

# Strings #
#---------#

# String-splitting delimiters #
splitdelim1 = common_splitdelim_list[0]
splitdelim2 = common_splitdelim_list[1]

# Grid header file function key list #
keylist = ['total_columns', 'total_lines', 'xmin', 'xres', 'ymin', 'yres']

# Calendar and date-time parameters #
time_freqs_delta = [time_freqs[0]] + time_freqs[2:4]
freq_abbrs_delta = [freq_abbrs[0]] + freq_abbrs[2:4]

# Tuples to pass in into preformatted strings #
arg_tuple_delta1 = ("time-frequency", time_freqs_delta)
arg_tuple_delta2 = ("basic operator", basic_four_rules)

# Statistics and operators #
#--------------------------#

# Basic statistics #
statistics = ["max", "min", "sum", 
              "mean", "avg", 
              "var", "var1",
              "std", "std1"]
  
# CDO remapping options #
cdo_remap_option_dict = {
    'ordinary' : 'remap',
    'bilinear' : 'remapbil',
    'nearest_neighbour' : 'remapnn',
    'bicubic' : 'remapbic',
    'conservative1' : 'remapcon',
    'conservative2' : 'remapcon2',
    'conservative1_y' : 'remapycon',
    'distance_weighted_average' : 'remapdis',
    'vertical_hybrid' : 'remapeta',
    'vertical_hybrid_sigma' : 'remapeta_s',
    'vertical_hybrid_z' : 'remapeta_z',
    'largest_area_fraction' : 'remaplaf',
    'sum' : 'remapsum',
    }

cdo_remap_options = list(cdo_remap_option_dict.keys())

                          
# Basic operator switch-case dictionary #
cdo_operator_str_dict = {
    basic_four_rules[0] : "add",
    basic_four_rules[1] : "sub",
    basic_four_rules[2] : "mul",
    basic_four_rules[3] : "div"
    }

# Preformatted strings #
#----------------------#

choice_error_str = "Wrong {}. Options are {}."

cdo_operator_syntax = """cdo {} {} {} {}"""
cdo_delta_syntax = """cdo y{}{} {} {} {}"""

# Dictionaries constructed from some preformatted strings (fromkeys) #
delta_calc_command_dict = dict.fromkeys(basic_four_rules, cdo_operator_syntax)
delta_apply_command_dict = dict.fromkeys(basic_four_rules, cdo_delta_syntax)
