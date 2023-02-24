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
fixed_dirpath = get_pytools_path.return_pytools_path()

# Enumerate custom modules and their paths #
#------------------------------------------#

custom_mod1_path = f"{fixed_dirpath}/files_and_directories"      
custom_mod2_path = f"{fixed_dirpath}/strings"
custom_mod3_path = f"{fixed_dirpath}/weather_and_climate"
                                        
# Add the module paths to the path variable #
#-------------------------------------------#

sys.path.append(custom_mod1_path)
sys.path.append(custom_mod2_path)
sys.path.append(custom_mod3_path)

# Perform the module importations #
#---------------------------------#

import file_and_directory_handler
import netcdf_handler
import string_handler

#----------------------------------------------------#
# Define imported module(s)´ function call shortcuts #
#----------------------------------------------------#

addExtraName2File = string_handler.addExtraName2File
find_substring_index = string_handler.find_substring_index
fileList2String = string_handler.fileList2String
obj_path_specs = string_handler.get_file_spec
modify_obj_specs = string_handler.modify_obj_specs

rename_objects = file_and_directory_handler.rename_objects

get_file_variables = netcdf_handler.get_file_variables
find_time_dimension_raiseNone = netcdf_handler.find_time_dimension_raiseNone
get_times = netcdf_handler.get_times

#-------------------------#
# Define custom functions #
#-------------------------#

# Character string processing #
#-----------------------------#
                    
def get_variable_name_inFileStr(file,
                                return_std_varname=False,
                                varlist_original=None,
                                varlist_standardized=None):
        
    fsk = "name_noext_parts"
    file_path_name_noext_parts = obj_path_specs(file,
                                               file_spec_key=fsk,
                                               splitchar=splitchar1)
                                
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
        
        var_std = get_variable_name_inFileStr(file,
                                              True,
                                              varlist_original, 
                                              varlist_standardized)
        
        file_path_name_parts = obj_path_specs(file, 
                                             file_spec_key=obj2change,
                                             splitchar=splitchar1)
        
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
                          calculationMethod,
                          period,
                          region,
                          extension):

    standard_name = f"{variable}_"\
                    f"{time_freq}_"\
                    f"{model}_"\
                    f"{experiment}_"\
                    f"{calculationMethod}_"\
                    f"{region}_"\
                    f"{period}.{extension}"
                    
    return standard_name


def cdo_sellonlatbox(file_list,
                     coordinate_list,
                     time_freq,
                     model,
                     experiment,
                     calculationMethod,
                     region,
                     extension):

    for file in file_list:                 
        variable = get_variable_name_inFileStr(file)
            
        time_var = find_time_dimension_raiseNone(file)
        times = get_times(file, time_var)
            
        start_year = f"{times.dt.year.values[0]}"
        end_year = f"{times.dt.year.values[-1]}"
        
        period = f"{start_year}-{end_year}"
        
        standardized_output_file_name = standardize_file_name(variable,
                                                              time_freq,
                                                              model,
                                                              experiment,
                                                              calculationMethod,
                                                              period,
                                                              region,
                                                              extension)
        
        sellonlatbox_command = f"cdo sellonlatbox,{coordinate_list} "\
                               f"'{file}' {standardized_output_file_name}"
        os.system(sellonlatbox_command)


def cdo_mergetime(file_list,
                  variable,
                  time_freq,
                  model,
                  experiment,
                  calculationMethod,
                  period,
                  region,
                  extension):
                       
    standardized_output_file_name = standardize_file_name(variable,
                                                          time_freq,
                                                          model,
                                                          experiment,
                                                          calculationMethod,
                                                          period,
                                                          region,
                                                          extension)
    
    start_year = f"{period.split(splitchar2)[0]}"
    end_year = f"{period.split(splitchar2)[-1]}"
    
    fsk = "name_noext_parts"
    
    file_list_selyear\
    = [file
       for file in file_list
       if (year := obj_path_specs(file, fsk, splitchar1)[-1])
       >= start_year
       and year
       <= end_year]
    
    
    
    allfiles_string = fileList2String(file_list_selyear)
    mergetime_command = f"cdo -b F64 -f nc4 mergetime '{allfiles_string}' "\
                        f"{standardized_output_file_name}"
    os.system(mergetime_command)
    
    
def custom_cdo_mergetime(file_list,
                         custom_output_file_name,
                         create_temporal_file=False):
    
    allfiles_string = fileList2String(file_list)
    
    if not create_temporal_file:
        mergetime_command = f"cdo -b F64 -f nc4 mergetime '{allfiles_string}' "\
                            f"{custom_output_file_name}"
    else:
        temp_file = addExtraName2File(file_list[0])
        mergetime_command = f"cdo -b F64 -f nc4 mergetime '{allfiles_string}' "\
                            f"{temp_file}"
                     
    os.system(mergetime_command)
        
    
def cdo_selyear(file_list,
                selyear_string,
                time_freq,
                model,
                experiment,
                calculationMethod,
                region,
                extension):
    
    
    fsk = "name_noext_parts"
    selyear_string_split = obj_path_specs(selyear_string, 
                                         file_spec_key=fsk,
                                         splitchar=splitchar2)
    
    start_year = f"{selyear_string_split[0]}"
    end_year = f"{selyear_string_split[-1]}"
    
    selyear_string_cdo = f"{start_year}/{end_year}"   
    period_selyear = f"{start_year}-{end_year}"    
    
    for file in file_list:
        variable = get_variable_name_inFileStr(file)
        
        standardized_output_file_name = standardize_file_name(variable,
                                                              time_freq,
                                                              model,
                                                              experiment,
                                                              calculationMethod,
                                                              period_selyear,
                                                              region,
                                                              extension)
     
        selyear_command = f"cdo selyear,{selyear_string_cdo} "\
                          f"'{file}' {standardized_output_file_name}"
        os.system(selyear_command)
        
    
def cdo_anomalies(input_file_full_time,
                  input_file_freq_avg,
                  variable,
                  time_freq,
                  model,
                  experiment,
                  calculationMethod,
                  period,
                  region,
                  extension):
                       
    standardized_output_file_name = standardize_file_name(variable,
                                                          time_freq,
                                                          model,
                                                          experiment,
                                                          calculationMethod,
                                                          period,
                                                          region,
                                                          extension)
 
    anomaly_calc_command = f"cdo sub '{input_file_freq_avg}' '{input_file_full_time}' "\
                           f"{standardized_output_file_name}"
    os.system(anomaly_calc_command)


def cdo_shifttime(file_list,
                  shift_value):
                       
    for file in file_list:
        
        temp_file = addExtraName2File(file)
        
        shifttime_command = f"cdo shifttime,{shift_value} '{file}' '{temp_file}'"
        os.system(shifttime_command)
        
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
        
        temp_file = addExtraName2File(file)
        star_date_format = f"{year0}-{month0}-{day0} "\
                           f"{hour0:2d}:{minute0:2d}:{second0:2d}"
        
        inttime_command = f"cdo inttime,{star_date_format},{time_step} "\
                          f"'{file}' '{temp_file}'"
        os.system(inttime_command)
        
        rename_objects(temp_file, file)
  
    
def cdo_rename(file_list, 
               varlist_original,
               varlist_standardized):
    
    lfl = len(file_list)
    
    for file in enumerate(file_list):
        
        file_num = file[0] + 1
        file_name = file[-1]

        # Find the variable in the provided original variable list #   
        var_file = get_file_variables(file_name)
        
        # Find the standardized variable, provided the std variable list #        
        var_std = get_variable_name_inFileStr(file_name,
                                              True,
                                              varlist_original,
                                              varlist_standardized)
            
        print(f"Renaming original variable '{var_file}' to '{var_std}' "
              f"on file {file_num} out of {lfl}...")
    
        file_name_chname = addExtraName2File(file_name, 
                                                     splitchar1)
        chname_command = f"cdo chname,{var_file},{var_std} "\
                         f"'{file_name}' '{file_name_chname}'"
        os.system(chname_command)
    
        # Rename the cdo output file name to the original one #
        rename_objects(file_name_chname, file_name)
        
# Mathematic and statistical operations #
#---------------------------------------#

def cdo_time_mean(input_file,
                  variable,
                  time_freq,
                  model,
                  experiment,
                  calculationMethod,
                  period,
                  region,
                  extension):
                       
    standardized_output_file_name = standardize_file_name(variable,
                                                          time_freq,
                                                          model,
                                                          experiment,
                                                          calculationMethod,
                                                          period,
                                                          region,
                                                          extension)
 
    time_mean_command = f"cdo -{calculationMethod} '{input_file}' "\
                        f"{standardized_output_file_name}"
    os.system(time_mean_command)
    

def cdo_remap(file_list,
              remap_method_str,
              variable,
              time_freq,
              model,
              experiment,
              calculationMethod,
              period,
              region,
              extension,
              remap_method="bilinear"):
    
    standardized_output_file_name = standardize_file_name(variable,
                                                          time_freq,
                                                          model,
                                                          experiment,
                                                          calculationMethod,
                                                          period,
                                                          region,
                                                          extension)
    
    cdo_remap_options = ['ordinary', 'bilinear', 'nearest_neighbour',
                         'bicubic', 'conservative1', 'conservative2'
                         'distance_weighted_average', 'vertical_hybrid', 
                         'vertical_hybrid_sigma', 'vertical_hybrid_z'
                         'remapeta_z', 'largest_area_fraction', 'sum', 
                         'conservative1_y']
    
    if remap_method == "ordinary":
        remap_method_cdo = "remap"
    
    if remap_method == "bilinear":
        remap_method_cdo = "remapbil"
                        
    elif remap_method == "nearest_neighbour":
        remap_method_cdo = "remapnn"
                        
    elif remap_method == "bicubic":
        remap_method_cdo = "remapbic"
                        
    elif remap_method == "conservative1":
        remap_method_cdo = "remapcon"
                        
    elif remap_method == "conservative2":
        remap_method_cdo = "remapcon2"
        
    elif remap_method == "distance_weighted_average":
        remap_method_cdo = "remapdis"
                        
    elif remap_method == "vertical_hybrid":
        remap_method_cdo = "remapeta"
                        
    elif remap_method == "vertical_hybrid_sigma":
        remap_method_cdo = "remapeta_s"
                        
    elif remap_method == "vertical_hybrid_z":
        remap_method_cdo = "remapeta_z"
                        
    elif remap_method == "largest_area_fraction":
        remap_method_cdo = "remaplaf"
                        
    elif remap_method == "sum":
        remap_method_cdo = "remapsum"
                        
    elif remap_method == "conservative1_y":
        remap_method_cdo = "remapycon"
        
    else:
        raise ValueError("Wrong remapping option. Available options are:\n"
                         f"{cdo_remap_options}")
 
    for file in file_list:            
        remap_command = f"cdo {remap_method_cdo},{remap_method_str} "\
                        f"'{file}' {standardized_output_file_name}" 
        os.system(remap_command)
        
        
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
    
    keylist = ['total_columns', 'total_lines', 'xmin', 'xres', 'ymin', 'yres']
    
    kwargs_values = list(kwargs.values())
    kwargs_keys = list(kwargs.keys())
    kwargs_keys.sort()
    
    if kwargs_keys != keylist:
        kwargs = {key : val 
                  for key,val in zip(keylist,kwargs_values)}
    
    grid = (
        'gridtype  = lonlat\n'
        'xsize     = %d\n'
        'ysize     = %d\n'
        'xname     = longitude\n'
        'xlongname = "Longitude values"\n'
        'xunits    = "degrees_east"\n'
        'yname     = latitude\n'
        'ylongname = "Latitude values"\n'
        'yunits    = "degrees_north"\n'
        'xfirst    = %.20f\n'
        'xinc      = %.20f\n'
        'yfirst    = %.20f\n'
        'yinc      = %.20f'
        % (
            kwargs[keylist[0]],
            kwargs[keylist[1]],
            kwargs[keylist[2]],
            kwargs[keylist[3]],
            kwargs[keylist[4]],
            kwargs[keylist[5]]
        )
    )
   
    output_file_object = open(output_file, 'w')
    output_file_object.write(grid)
    output_file_object.close()

        
def cdo_periodic_statistics(nc_file_name, statistic, isclimatic, freq, season_str=None):
    
    # Function to calculate basic statistics (included climatologies)
    # with netCDF files, without the need of opening them.
    # 
    # Notes
    # -----
    # It is not recommended to use output file names within
    # those functions that calculate deltas,
    # since doing so lowers disk I/O performance.
    
    statistics = ["max", "min", "sum", 
                  "mean", "avg", 
                  "var", "var1",
                  "std", "std1"]
    
    time_freqs = ['hourly', 'daily', 'monthly', 'seasonal', 'yearly']
    period_abbrs = ['hour', 'day', 'mon', 'seas', 'year']
    
    # Quality control #
    if statistic not in statistics:
        raise ValueError(f"Wrong statistic. Options are {statistics}.")
        
    # Identify the abbreviature for the selected time frequency #
    period_abbr_idx = find_substring_index(time_freqs, freq)
  
    if period_abbr_idx == -1:
        raise ValueError(f"Wrong time frequency. Options are {time_freqs}.")
    else:
        period_abbr = period_abbrs[period_abbr_idx]
        
    # Determine whether to calculate the climatological statistic #
    if not isclimatic:
        statname = f"{period_abbr}{statistic}"            
    else:
        statname = f"y{period_abbr}{statistic}"
        
    if period_abbr == period_abbrs[3]:
        if season_str is not None:
            statname += f" -select,season={season_str}"
            
    # Get the file name for string manipulation #
    file_path_name\
    = addExtraName2File(nc_file_name, return_file_name_noext=True)
    
    """Special case for seasonal time frequency"""
    if season_str is not None:
        statname_seas = f"{statname.split()[0]}_{statname[-3:]}"
        string2add = f"{splitchar1}{statname_seas}"
        file_path_name_longer = addExtraName2File(file_path_name, string2add)
        
    else:
        string2add = f"{splitchar1}{statname}"
        file_path_name_longer = addExtraName2File(file_path_name, string2add)
        
    # Define the output file name based on the configuration chosen #
    obj2change = "name_noext"
    output_file_name\
    = modify_obj_specs(nc_file_name, obj2change, file_path_name_longer)
        
    # Perform the computation #
    cdo_stat_command = f"cdo {statname} {nc_file_name} {output_file_name}"
    os.system(cdo_stat_command)

    
def calculate_periodic_deltas(projected_ncfile,
                              historical_ncfile,
                              operator="+",
                              delta_period="monthly",
                              proj_model=None):
    
    time_freqs = ['hourly', 'monthly', 'seasonal']
    period_abbrs = ['hour', 'mon', 'seas']
    
    period_abbr_idx = find_substring_index(time_freqs, delta_period) 
    deltaApply_fn = addExtraName2File(historical_ncfile, 
                                      return_file_name_noext=True)

    if proj_model is None:
        raise ValueError("The model name's position contained on the file name "\
                         f"{projected_ncfile} can vary significantly "\
                         "from files belonging to one project from another. "\
                         "It is safer to manually define the model used "\
                         "for projections.")

    if period_abbr_idx == -1:
        raise ValueError(f"Wrong time frequency. Options are {time_freqs}.")
    else:
        period_abbr = period_abbrs[period_abbr_idx]
    
        
    hist_mean_command = f"-y{period_abbr}mean {historical_ncfile}"
    proj_mean_command = f"-y{period_abbr}mean {projected_ncfile}"

    string2add = f"{period_abbr}Deltas_{proj_model}.nc"
    deltaApply_fn_longer = addExtraName2File(deltaApply_fn, string2add)
    
    if operator == "+":
        deltaCalc_command = f"cdo add {hist_mean_command} {proj_mean_command}"\
                            f"{deltaApply_fn_longer}"
   
    elif operator == "-":
        deltaCalc_command = f"cdo sub {hist_mean_command} {proj_mean_command}"\
                            f"{deltaApply_fn_longer}"
                             
    elif operator == "*":
        deltaCalc_command = f"cdo mul {hist_mean_command} {proj_mean_command}"\
                            f"{deltaApply_fn_longer}"
                             
    elif operator == "/":
        deltaCalc_command = f"cdo div {hist_mean_command} {proj_mean_command}"\
                            f"{deltaApply_fn_longer}"
                             
    else:
        raise ValueError("Wrong basic operator. Options are "
                         "{'+', '-', '*', '/'}.")
                    
    os.system(deltaCalc_command)
        

def apply_periodic_deltas(projected_ncfile,
                          historical_ncfile,
                          operator="+",
                          delta_period="monthly",
                          proj_model=None):
    
    time_freqs = ['hourly', 'monthly', 'seasonal']
    period_abbrs = ['hour', 'month', 'seas']
    
    period_abbr_idx = find_substring_index(time_freqs, delta_period)
    deltaApply_fn = addExtraName2File(historical_ncfile, 
                                      return_file_name_noext=True)
    
    if proj_model is None:
        raise ValueError("The model name's position contained on the file name "\
                         f"{projected_ncfile} can vary significantly "\
                         "from files belonging to one project from another. "\
                         "It is safer to manually define the model used "\
                         "for projections.")

    if period_abbr_idx == -1:
        raise ValueError(f"Wrong time frequency. Options are {time_freqs}.")
    else:
        period_abbr = period_abbrs[period_abbr_idx]

        
    string2add = f"{period_abbr}DeltaApplied_{proj_model}.nc"
    deltaApply_fn_longer = addExtraName2File(deltaApply_fn, string2add)
    
    hist_mean_command = f"-y{period_abbr}mean {historical_ncfile}"
        
    if operator == "+":
        deltaApply_command = f"cdo y{period_abbr}add {projected_ncfile} "\
                             f"{hist_mean_command} " \
                             f"{deltaApply_fn_longer}"
   
    elif operator == "-":
        deltaApply_command = f"cdo y{period_abbr}sub {projected_ncfile} "\
                             f"{hist_mean_command} " \
                             f"{deltaApply_fn_longer}"
                             
    elif operator == "*":
        deltaApply_command = f"cdo y{period_abbr}mul {projected_ncfile} "\
                             f"{hist_mean_command} " \
                             f"{deltaApply_fn_longer}"
                             
    elif operator == "/":
        deltaApply_command = f"cdo y{period_abbr}div {projected_ncfile} "\
                             f"{hist_mean_command} " \
                             f"{deltaApply_fn_longer}"
                             
    else:
        raise ValueError("Wrong basic operator. Options are "
                         "{'+', '-', '*', '/'}.")
                      
    os.system(deltaApply_command)
    
#------------------#
# Local parameters #
#------------------#

splitchar1 = "_"
splitchar2 = "-"