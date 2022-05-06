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


module_imp2 = "file_handler.py"
module_imp2_path = f"{fixed_dirpath}/"\
                   f"files_and_directories/{module_imp2}"

spec2 = importlib.util.spec_from_file_location(module_imp2, module_imp2_path)
file_handler = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(file_handler)


module_imp3 = "netcdf_handler.py"
module_imp3_path = f"{fixed_dirpath}/"\
                   f"weather_and_climate/{module_imp3}"

spec3 = importlib.util.spec_from_file_location(module_imp3, module_imp3_path)
netcdf_handler = importlib.util.module_from_spec(spec3)
spec3.loader.exec_module(netcdf_handler)

#----------------------------------------------------#
# Define imported module(s)´ function call shortcuts #
#----------------------------------------------------#

file_path_specs = string_handler.file_path_specs
find_substring_index = string_handler.find_substring_index
join_file_path_specs = string_handler.join_file_path_specs
file_list_2_string = string_handler.file_list_2_string
create_temporal_file_name = string_handler.create_temporal_file_name
noneInString_filter = string_handler.noneInString_filter

rename_objects = file_handler.rename_objects

get_file_variables = netcdf_handler.get_file_variables
find_time_dimension_raiseNone = netcdf_handler.find_time_dimension_raiseNone
get_times = netcdf_handler.get_times

#------------------------------------------------------#
# Define global variable used in many custom functions #
#------------------------------------------------------#

name_splitchar1 = "_"
name_splitchar2 = "-"

#-------------------------#
# Define custom functions #
#-------------------------#

# Character string processing #
#-----------------------------#
                    
def get_standard_variable_name(file,
                               varlist_original,
                               varlist_standardized):
    
    file_path_noname, file_path_name, file_path_name_split, file_path_ext\
    = file_path_specs(file, name_splitchar1)
        
    var_file = file_path_name_split[0]
    
    # Find the variable in the provided original variable list #
    var_pos = find_substring_index(varlist_original, var_file)
    if var_pos != -1:
        var_std = varlist_standardized[var_pos]
        
        return\
            var_std, \
            file_path_noname, \
            file_path_name, \
            file_path_name_split, \
            file_path_ext
    else:
        raise ValueError(f"Variable '{var_file}' found at file '{file}' "
                         f"not present at original variable list {varlist_original}")
        

def change_file_names_byvar(file_list,
                            varlist_original,
                            varlist_standardized):

    for file in file_list:
        
        var_std, file_path_noname, file_path_name, file_path_name_split, file_path_ext \
        = get_standard_variable_name(file, varlist_original, varlist_standardized) 
               
        extension = file_path_ext
        file_path_name_split[0] = var_std
        
        varname_changed_file_path_name = join_file_path_specs(file_path_noname,
                                                              file_path_name_split,
                                                              extension,
                                                              name_splitchar1)
              
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
        
        file_path_noname, file_path_name, file_path_name_split, file_path_ext\
        = file_path_specs(file, name_splitchar1)
                    
        variable = file_path_name_split[0]
            
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
    
    start_year = f"{period.split(name_splitchar2)[0]}"
    end_year = f"{period.split(name_splitchar2)[-1]}"
    
    file_list_selyear\
    = [file
       for file in file_list
       if (year := file_path_specs(file, name_splitchar1)[-2][-1])
       >= start_year
       and year
       <= end_year]
    
    allfiles_string = file_list_2_string(file_list_selyear)
    mergetime_command = f"cdo -b F64 -f nc4 mergetime '{allfiles_string}' "\
                        f"{standardized_output_file_name}"
    os.system(mergetime_command)
    
    
def custom_cdo_mergetime(file_list,
                         custom_output_file_name,
                         create_temporal_file=False):
    
    allfiles_string = file_list_2_string(file_list)
    
    if not create_temporal_file:
        mergetime_command = f"cdo -b F64 -f nc4 mergetime '{allfiles_string}' "\
                            f"{custom_output_file_name}"
    else:
        temp_file = create_temporal_file_name(file_list[0])
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
    
    selyear_string_split = file_path_specs(selyear_string, name_splitchar2)[-2]
    
    start_year = f"{selyear_string_split[0]}"
    end_year = f"{selyear_string_split[-1]}"
    
    selyear_string_cdo = f"{start_year}/{end_year}"   
    period_selyear = f"{start_year}-{end_year}"    
    
    for file in file_list:
        
        file_path_noname, file_path_name, file_path_name_split, file_path_ext\
        = file_path_specs(file, name_splitchar1)
            
        variable = file_path_name_split[0]
        
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
        
        temp_file = create_temporal_file_name(file)
        
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
        
        temp_file = create_temporal_file_name(file)
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
        var_std = get_standard_variable_name(file_name,
                                             varlist_original,
                                             varlist_standardized)[0]
            
        print(f"Renaming original variable '{var_file}' to '{var_std}' "
              f"on file {file_num} out of {lfl}...")
    
        file_name_chname = create_temporal_file_name(file_name, 
                                                     name_splitchar1)
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
              coordinate_list,
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
        remap_cdo = "remap"
    
    if remap_method == "bilinear":
        remap_cdo = "remapbil"
                        
    elif remap_method == "nearest_neighbour":
        remap_cdo = "remapnn"
                        
    elif remap_method == "bicubic":
        remap_cdo = "remapbic"
                        
    elif remap_method == "conservative1":
        remap_cdo = "remapcon"
                        
    elif remap_method == "conservative2":
        remap_cdo = "remapcon2"
        
    elif remap_method == "distance_weighted_average":
        remap_cdo = "remapdis"
                        
    elif remap_method == "vertical_hybrid":
        remap_cdo = "remapeta"
                        
    elif remap_method == "vertical_hybrid_sigma":
        remap_cdo = "remapeta_s"
                        
    elif remap_method == "vertical_hybrid_z":
        remap_cdo = "remapeta_z"
                        
    elif remap_method == "largest_area_fraction":
        remap_cdo = "remaplaf"
                        
    elif remap_method == "sum":
        remap_cdo = "remapsum"
                        
    elif remap_method == "conservative1_y":
        remap_cdo = "remapycon"
        
    else:
        raise ValueError("Wrong remapping option. Available options are:\n"
                         f"{cdo_remap_options}")
 
    for file in file_list:            
        remap_command = f"cdo {remap_cdo},{coordinate_list} "\
                        f"'{file}' {standardized_output_file_name}" 
        os.system(remap_command)
        
        
def cdo_periodic_statistics(nc_file_name, statistic, isclimatic, freq):
    
    # TODO: urtarokoa deneko kasuan, zehaztu ea urtaro guztiak ()
    # edo bakarren bat hartu nahi denentz (-select,season="DJF"...)
    
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
    period_abbrs = ['hour', 'day', 'month', 'seas', 'year']
    
    
    if statistic not in statistics:
        raise ValueError(f"Wrong statistic. Options are {statistics}.")
        
    period_abbr_idx = find_substring_index(time_freqs, freq)
  
    if period_abbr_idx == -1:
        raise ValueError(f"Wrong time frequency. Options are {time_freqs}.")
    else:
        period_abbr = period_abbrs[period_abbr_idx]
        
    
    file_path_noname, file_path_name, file_path_name_split, file_ext\
    = file_path_specs(nc_file_name, name_splitchar1)
    
    if not isclimatic:
        statname = f"{period_abbr}{statistic}"
    else:
        statname = f"y{period_abbr}{statistic}"
    
    file_path_name += statname
    
    output_file_name = f"{file_path_noname}/{file_path_name}.{file_ext}"
    ofn_noneFiltered = noneInString_filter(output_file_name)
    
    cdo_stat_command = f"cdo {statname} {nc_file_name} {ofn_noneFiltered}"
    os.system(cdo_stat_command)    

        
def calculate_periodic_deltas(projected_ncfile,
                              historical_ncfile,
                              operator="+",
                              delta_period="monthly"):
    
    time_freqs = ['hourly', 'monthly', 'seasonal']
    period_abbrs = ['hour', 'month', 'seas']
    
    period_abbr_idx = find_substring_index(time_freqs, delta_period) 
    deltaApply_fn = file_path_specs(historical_ncfile, name_splitchar1)[2]
    proj_model = file_path_specs(projected_ncfile, name_splitchar1)[2][2]
    
     
    if period_abbr_idx == -1:
        raise ValueError(f"Wrong time frequency. Options are {time_freqs}.")
    else:
        period_abbr = period_abbrs[period_abbr_idx]
    
        
    hist_mean_command = f"-y{period_abbr}mean {historical_ncfile}"
    proj_mean_command = f"-y{period_abbr}mean {projected_ncfile}"

    deltaApply_fn += f"{period_abbr}Deltas_{proj_model}.nc"
    
    if operator == "+":
        deltaCalc_command = f"cdo add {hist_mean_command} {proj_mean_command}"\
                            f"{deltaApply_fn}"
   
    elif operator == "-":
        deltaCalc_command = f"cdo sub {hist_mean_command} {proj_mean_command}"\
                            f"{deltaApply_fn}"
                             
    elif operator == "*":
        deltaCalc_command = f"cdo mul {hist_mean_command} {proj_mean_command}"\
                            f"{deltaApply_fn}"
                             
    elif operator == "/":
        deltaCalc_command = f"cdo div {hist_mean_command} {proj_mean_command}"\
                            f"{deltaApply_fn}"
                             
    else:
        raise ValueError("Wrong basic operator. Options are "
                         "{'+', '-', '*', '/'}.")
                    
    os.system(deltaCalc_command)
        

def apply_periodic_deltas(projected_ncfile,
                          historical_ncfile,
                          operator="+",
                          delta_period="monthly"):
    
    time_freqs = ['hourly', 'monthly', 'seasonal']
    period_abbrs = ['hour', 'month', 'seas']
    
    period_abbr_idx = find_substring_index(time_freqs, delta_period)  
    
    deltaApply_fn = file_path_specs(historical_ncfile, name_splitchar1)[2]
    proj_model = file_path_specs(projected_ncfile, name_splitchar1)[2][2] 
    

    if period_abbr_idx == -1:
        raise ValueError(f"Wrong time frequency. Options are {time_freqs}.")
    else:
        period_abbr = period_abbrs[period_abbr_idx]

        
    deltaApply_fn += f"{period_abbr}DeltaApplied_{proj_model}.nc"
    hist_mean_command = f"-y{period_abbr}mean {historical_ncfile}"
        
    if operator == "+":
        deltaApply_command = f"cdo y{period_abbr}add {projected_ncfile} "\
                             f"{hist_mean_command} " \
                             f"{deltaApply_fn}"
   
    elif operator == "-":
        deltaApply_command = f"cdo y{period_abbr}sub {projected_ncfile} "\
                             f"{hist_mean_command} " \
                             f"{deltaApply_fn}"
                             
    elif operator == "*":
        deltaApply_command = f"cdo y{period_abbr}mul {projected_ncfile} "\
                             f"{hist_mean_command} " \
                             f"{deltaApply_fn}"
                             
    elif operator == "/":
        deltaApply_command = f"cdo y{period_abbr}div {projected_ncfile} "\
                             f"{hist_mean_command} " \
                             f"{deltaApply_fn}"
                             
    else:
        raise ValueError("Wrong basic operator. Options are "
                         "{'+', '-', '*', '/'}.")
                      
    os.system(deltaApply_command)
    
