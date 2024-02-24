#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

from pathlib import Path
import sys

import numpy as np
import xarray as xr

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
custom_mod2_path = f"{fixed_path}/pandas_data_frames"
custom_mod3_path = f"{fixed_path}/parameters_and_constants"
custom_mod4_path = f"{fixed_path}/operative_systems"
custom_mod5_path = f"{fixed_path}/strings"
custom_mod6_path = f"{fixed_path}/weather_and_climate"
                                        
# Add the paths to the 'path' attribute of module 'sys' #
#-------------------------------------------------------#

sys.path.append(custom_mod1_path)
sys.path.append(custom_mod2_path)
sys.path.append(custom_mod3_path)
sys.path.append(custom_mod4_path)
sys.path.append(custom_mod5_path)
sys.path.append(custom_mod6_path)

# Perform whole or partial module importations #
#----------------------------------------------#

from data_frame_handler import save2csv
import file_and_directory_paths
from file_and_directory_handler import move_files_byFS_fromCodeCallDir
import information_output_formatters
from global_parameters import common_splitchar_list
from os_operations import exec_shell_command
import string_handler

#----------------------------------------------------#
# Define imported module(s)' function call shortcuts #
#----------------------------------------------------#

find_ext_file_paths = file_and_directory_paths.find_ext_file_paths
find_ext_file_directories = file_and_directory_paths.find_ext_file_directories

print_format_string = information_output_formatters.print_format_string
format_string = information_output_formatters.format_string

fileList2String = string_handler.fileList2String
find_substring_index = string_handler.find_substring_index
get_obj_specs = string_handler.get_obj_specs
modify_obj_specs = string_handler.modify_obj_specs

#-------------------------#
# Define custom functions #
#-------------------------#

# Faulty netCDF file detecting #
#------------------------------#

def ncfile_integrity_status(ncfile_name):
    
    try:
        ds=xr.open_dataset(ncfile_name)
        ds.close()
        return 0
    
    except:
        return -1
        
def netcdf_file_scanner(path_to_walk_into, 
                        top_path_only=False,
                        verbose=False,
                        extra_verbose=False,
                        create_report=False):

    # Proper argument selection control #
    arg_names = netcdf_file_scanner.__code__.co_varnames
    verb_arg_pos = find_substring_index(arg_names, 
                                        "verbose",
                                        find_whole_words=True)
    
    xverb_arg_pos = find_substring_index(arg_names, 
                                         "extra_verbose",
                                         find_whole_words=True)
    
    # Define the input data directories and files #
    #---------------------------------------------#
    
    if not isinstance(path_to_walk_into, list):        
        path_to_walk_into = [path_to_walk_into]
        
    for ptwi in path_to_walk_into:
        ncgrib_file_list = find_ext_file_paths(extensions[0],
                                          ptwi,
                                          top_path_only=top_path_only)
        lncfl = len(ncgrib_file_list)
    
        # Initialise faulty file counter #
        #--------------------------------#
        
        faulty_ncf_counter = [lncfl, 0]
        faulty_ncf_list = []
        
        # Loop through all path list #
        #----------------------------#
        
        for file_num, file_name in enumerate(ncgrib_file_list, start=1):
            if verbose and extra_verbose:
                raise ValueError(f"Arguments '{arg_names[verb_arg_pos]}' "
                                 f"and '{arg_names[xverb_arg_pos]}' "
                                 "cannot be 'True' at the same time.")
                
            else:
                if verbose:
                    arg_tuple_file_scan1 = (file_num, lncfl, ptwi)
                    print_format_string(scan_progress_info_str,
                                        arg_tuple_file_scan1,
                                        end="\r")
                elif extra_verbose:
                    arg_tuple_file_scan2 = (file_name, file_num, lncfl, ptwi)
                    print_format_string(scan_progress_str_evb,
                                        arg_tuple_file_scan2,
                                        end="\r")
        
            integrity_status = ncfile_integrity_status(file_name)
            
            if integrity_status == -1:
                faulty_ncf_counter[-1] += 1
                faulty_ncf_list.append(file_name)
                
        if create_report:
        
            # Create faulty netCDF file report #
            #----------------------------------#
            
            ofile_name = f"{codeCallDir}/{report_fn_noext}.txt"
            ofile = open(ofile_name, "w")
            
            arg_tuple_file_scan3 = (ptwi,
                                    faulty_ncf_counter[0], 
                                    faulty_ncf_counter[-1])
            ofile.write(format_string(report_info_str, arg_tuple_file_scan3))
            
            for faulty_ncf in faulty_ncf_list:
                ofile.write(f" {faulty_ncf}\n")
            
            print("Faulty netCDF file report created at the current directory.")
            ofile.close()
            
        else:
            return faulty_ncf_counter[-1]

# netCDF data creating and manipulating #
#---------------------------------------#

def create_ds_component(var_name,
                        data_array,
                        dimlist,
                        dim_dict,
                        attrs_dict):
    
    DataArray_dict = {
        var_name : xr.DataArray(
            data=data_array,
            dims=dimlist,
            coords=dim_dict,
            attrs=attrs_dict,
            )
        }
    
    return DataArray_dict


def saveDataAsNETCDF_standard(file_name,
                              vardim_names_for_ds,
                              data_arrays,
                              dimlists,
                              dim_dictlist,
                              attrs_dictlist,
                              global_attrs_dict):

    ds = xr.Dataset()
    
    for vardim, data_array, dimlist, dim_dict, attrs_dict in zip(vardim_names_for_ds,
                                                                 data_arrays,
                                                                 dimlists,
                                                                 dim_dictlist,
                                                                 attrs_dictlist):
        
        DataArray_dict = create_ds_component(vardim,
                                             data_array,
                                             dimlist,
                                             dim_dict,
                                             attrs_dict)
        ds = ds.merge(DataArray_dict)
        
    ds.attrs = global_attrs_dict
    
    file_name += ".{extensions[0]}"
    
    ds.to_netcdf(file_name, "w", format="NETCDF4")
    print(f"{file_name} file successfully created")
    
    
def saveXarrayDSAsNetCDF(xarray_ds,
                         file_name,
                         attrs_dict=None):
    
    """
    Function that writes a xarray data set directly into a netCDF,
    with the option of updating attributes.
    
    Parameters
    ----------
    xarray_ds : xarray.Dataset
          OPENED xarray data set.
    file_name : str
          String for the resulting netCDF file name.
    attrs_dict : dict
          Dictionary containing attributes, such as source,
          version, date of creation, etc.
          If not given, attributes will remain the same as the input file.
    
    Returns
    -------
    netCDF file
    """
    
    file_name += ".nc"
    
    if attrs_dict:
        xarray_ds.attrs = attrs_dict
    
    xarray_ds.to_netcdf(file_name, "w", format="NETCDF4")

    print(f"{file_name} has been successfully created")
    
    
def netCDF_regridder(ds_in, ds_image, method="bilinear"):
    
    
    import xesmf as xe
    
    """
    Function that regrids an xarray Dataset to that of the
    desired Dataset. It is similar to CDO but more intuitive and
    easier to understand, supported by Python.
    
    Parameters
    ----------
    ds_in : xarray.Dataset
          Input xarray data set
    ds_image : xarray.Dataset
          Xarray data set with grid specifications to which apply on ds_in.
    method : {'bilinear', 'conservative', 'nearest_s2d', 'nearest_d2s', 'patch'}
          Regridding method. Defaults 'bilinear'.
    
    Returns
    -------
    ds_out : xarray.Dataset
          Output data set regridded according to the grid specs of ds_in.
    """
    
    if method not in method_list:
        raise ValueError("Wrong regridding method.\n"
                         f"Options are {method_list}.")
        
    else:
        regridder = xe.Regridder(ds_in, ds_image, method)
        ds_out = regridder(ds_in)
        return ds_out
    

def saveNCdataAsCSV(nc_file, 
                    columns_to_drop,
                    separator,
                    save_index,
                    save_header,
                    csv_file_name="default",
                    date_format=None,
                    approximate_coords=False,
                    latitude_point=None,
                    longitude_point=None):
    
    """
    Function that saves netCDF data into a CSV file AS IT IS, where data variables
    may originally be 3D, usually dependent on (time, latitude, longitude).
    It is intended to speed up further data processes,
    especially when opening very large netCDF files with xarray,
    which can take a long time.
    Saving data into a CSV, it can then be read very rapidly so as to
    load data for post-processing.
    
    For that, it seeks for essential variables,
    together with 'time' dimension, if present.
    It then concatenates whole data into a data frame and then
    saves it into a CSV file.
    
    Parameters
    ----------
    nc_file : str or xarray.Dataset or 
                    xarray.DataArray
          String of the xarray data set containing file or
          the already opened data array or set.
    columns_to_drop : str or list of str
          Names of the columns to drop, if desired, from the
          resultant data frame of xarray.to_pandas() method.
          If None, then the function will not drop any column.
          To drop only coordinate labels, select "coords".
          Else, the function will drop the custom labels passed.
    separator : str
          String used to separate data columns.
    save_index : bool
          Boolean to choose whether to include a column into the excel document
          that identifies row numbers. Default value is False.
    save_header : bool
          Boolean to choose whether to include a row into the excel document
          that identifies column numbers. Default value is False.
    csv_file_name : str, optional
          If nc_file is a string and "default" option is chosen,
          then the function will attempt to extract a location name.
          If nc_file is a xarray object, a custom name must be provided.    #       
    date_format : str
          In case the data frame contains a time column,
          use to give format thereof when storing the data frame.
    approximate_coords : str
          If both latitude and longitude arrays are length higher than 1,
          determines whether to select a coordinate point and then
          perform the saving. If true and both lengths are 1,
          throws and error telling that data is already located at a point.
    latitude_point : float
          Valid only if approximate_coords is True.
    longitude_point : float
          Valid only if approximate_coords is True.
    
    Returns
    -------
    CSV file containing data as arranged on the data frame.
    
    Notes
    -----
    Remember that this function serves as a direct copy of netCDF4 data,
    if data modifications are required, then it cannot be used.
    Data frames are only 2D, so that those
    can only reflect a specific point multi-variable netCDF data along time
    or several grid points' data for a specific time position.
    Data frame column names will be the same as those on netCDF data file.
    """
    
    # Open netCDF data file if passed a string #
    if isinstance(nc_file, str):
        print(f"Opening {nc_file}...")
        ds = xr.open_dataset(nc_file)
        
    else:
        ds = nc_file.copy()
        
    if latitude_point is not None or longitude_point is not None:
        
        coord_varlist = find_coordinate_variables(ds)
        lats = ds[coord_varlist[0]]
        lons = ds[coord_varlist[1]]
        
        llats, llons = len(lats), len(lons)
        
        if llats == llons == 1:
            raise ValueError("Object is already located at a point data")
        else:
            if latitude_point is None:
                raise ValueError("Latitude point coordinate not given")
            
            elif longitude_point is None:
                raise ValueError("Longitude point coordinate not given")
            
            elif latitude_point is None and longitude_point is None:
                raise ValueError("Both latitude and longitude "
                                 "point coordinates not given.")
                
            else:
                
                if approximate_coords:
                    
                    lat_idx = abs(lats - latitude_point).argmin()
                    lon_idx = abs(lons - longitude_point).argmin()
                    
                    coord_idx_kw = {
                        coord_varlist[0] : lat_idx,
                        coord_varlist[1] : lon_idx
                        }
                    
                    ds = ds.isel(**coord_idx_kw)
                    
                else:
                    
                    coord_idx_kw = {
                        coord_varlist[0] : latitude_point,
                        coord_varlist[1] : longitude_point
                        }
                    
                    ds = ds.sel(**coord_idx_kw)
                    
    elif latitude_point is not None\
    and isinstance(approximate_coords, str):
                
        print(f"Coordinate label is {approximate_coords}")
        
        coord_idx_kw = {
            approximate_coords : latitude_point,
            }
        
        ds = ds.isel(**coord_idx_kw)
        
    elif latitude_point is None\
    and isinstance(approximate_coords, str):
        
        raise ValueError("You must provide a coordinate or ID")

    # Drop columns if desired #
    if columns_to_drop is None:
        data_frame\
        = ds.to_pandas().reset_index(drop=False)
    
    elif columns_to_drop == "coords": 
        columns_to_drop = coord_varlist.copy()
        data_frame\
        = ds.to_pandas().reset_index(drop=False).drop(columns=columns_to_drop)
        
    else:
        data_frame\
        = ds.to_pandas().reset_index(drop=False).drop(columns=columns_to_drop)
       
    # Create the saving file's name or maintain the user-defined name #
    #-----------------------------------------------------------------#
    
    if isinstance(nc_file, str) and csv_file_name == "default":
        obj2change = "ext"
        csv_file_name = get_obj_specs(nc_file, obj2change, extensions[1])
    
    elif not isinstance(nc_file, str) and csv_file_name == "default":
        raise ValueError("You must provide a CSV file name.")
        
    else:
        # Save data as desired format file #   
        #----------------------------------#
        
        save2csv(csv_file_name,
                 data_frame,
                 separator,
                 save_index,
                 save_header,
                 date_format)
    
    
def saveDataArrayAsCSV(data_array, 
                       separator,
                       save_index,
                       save_header,
                       csv_file_name=None,
                       new_columns="default",
                       date_format=None):
    
    """
    Function that saves a xr.DataArray object into a CSV file AS IT IS,
    where data variables may originally be 3D, 
    usually dependent on (time, latitude, longitude).
    This function works exactly as 'saveNCdataAsCSV' function does,
    so the docstrings also apply.
    Parameters
    ----------
    data_array : xarray.DataArray
    new_columns : str or list of str
          Names of the columns for the data frame created from the object.
          Default ones include 'time' and variable name label.
    separator : str
          String used to separate data columns.
    save_index : bool
          Boolean to choose whether to include a column into the excel document
          that identifies row numbers. Default value is False.
    save_header : bool
          Boolean to choose whether to include a row into the excel document
          that identifies column numbers. Default value is False.
    csv_file_name : str, optional
          If nc_file is a string and "default" option is chosen,
          then the function will attempt to extract a location name.
          If nc_file is a xarray object, a custom name must be provided.    #       
    date_format : str
    
    Returns
    -------
    CSV file containing data as arranged on the data frame.
    """
    
    # Drop information to a data frame #
    data_frame = data_array.to_pandas().reset_index(drop=False)        
        
    # Define the 'time' dimension name #
    date_key = find_time_dimension(data_array)
    
    # Rename the resulting data frame columns #
    if new_columns == "default":
        da_varname = data_array.name
        new_columns = [date_key, da_varname]

    data_frame.columns = new_columns
       
    # Create the saving file's name or maintain the user-defined name #
    if csv_file_name is None:
        raise ValueError("You must provide a CSV file name.")
        
    # Save data as desired format file #     
    else:
        save2csv(csv_file_name,
                 data_frame,
                 separator,
                 save_index,
                 save_header,
                 date_format)
        
#-----------------------#
# Basic data extractors #
#-----------------------#

def infer_time_frequency(nc_file):
    
    if isinstance(nc_file, str):
        print(f"Opening {nc_file}...")
        ds = xr.open_dataset(nc_file)
        
    else:
        ds = nc_file.copy()
        
    date_key = find_time_dimension(ds)
    time_freq = xr.infer_freq(ds[date_key])
    
    return time_freq


def infer_full_period_of_time(nc_file):
    
    if isinstance(nc_file, str):
        print(f"Opening {nc_file}...")
        ds = xr.open_dataset(nc_file)
        
    else:
        ds = nc_file.copy()
        
    date_key = find_time_dimension(ds)
    
    years = np.unique(ds[date_key].dt.year)
    full_period = f"{years[0]-years[-1]}"
    
    return full_period


def get_netcdf_fileList(path_to_walk_into):
    
    netcdf_files = find_ext_file_paths(extensions[0], 
                                       path_to_walk_into, 
                                       top_path_only=True)
    
    return netcdf_files


def get_netcdf_file_dirList(path_to_walk_into):
    
    netcdf_files_dirs = find_ext_file_directories(extensions[0], path_to_walk_into)
    
    return netcdf_files_dirs


def extract_and_store_latlon_bounds(delta_roundoff, value_roundoff):

    #------------------------------------------------------------------------#
    # Open each file, extract coordinate dimension data and save to txt file #
    #------------------------------------------------------------------------#
    
    netcdf_files_dirs = get_netcdf_file_dirList(codeCallDir)
    lncfd = len(netcdf_files_dirs)
    
    for ncf_dir_num, ncf_dir_name in enumerate(netcdf_files_dirs, start=1):
        nc_files = get_netcdf_fileList(ncf_dir_name)
        lncfs = len(nc_files)
        
        ofile = open(latlon_bound_ofile_name, "w")
    
        if lncfs > 0:
            for ncf_num, ncf_name in enumerate(nc_files, start=1):
                print("Extracting coordinate values "
                      f"from file {ncf_num} out of {lncfs} "
                      f"at directory {ncf_dir_num} out of {lncfd}...")
                
                faulty_file_trial = ncfile_integrity_status(ncf_name)
                
                if faulty_file_trial == 0:
                    
                    coord_varlist\
                    = find_coordinate_variables_raiseNone(ncf_name)
                            
                    if not coord_varlist:
                        ofile.write(f"No 'latitude' or 'longitude' coordinates "
                                    f"found in file {ncf_name}\n")
                        
                    else:        
                        latlons = get_latlon_bounds(ncf_name,
                                                    coord_varlist[0],
                                                    coord_varlist[1],
                                                    value_roundoff)
                        
                        lats = latlons[0]
                        lons = latlons[1]
                        
                        try:
                            llats = len(lats)
                            llons = len(lons)
                            
                            deltas = get_latlon_deltas(lats, lons, delta_roundoff)
                            
                            arg_tuple_latlons1 = (
                                ncf_name,
                                lats, 
                                lons,
                                llats,
                                llons,
                                deltas[0],
                                deltas[1]
                                )
                            ofile.write(format_string(latlon_info_str, 
                                                      arg_tuple_latlons1))
                        except:
                            llats = 1
                            llons = 1
                            
                            lat_delta = 0
                            lon_delta = 0
                        
                            arg_tuple_latlons2 = (ncf_name,
                                                  lats, 
                                                  lons,
                                                  llats,
                                                  llons,
                                                  lat_delta,
                                                  lon_delta)
                            ofile.write(format_string(latlon_info_str,
                                                      arg_tuple_latlons2))
                                                
                else: 
                    ofile.write(f"FAULTY FILE {ncf_name}\n")
                            
                            
            ofile.close()
            move_files_byFS_fromCodeCallDir(latlon_bound_ofile_name, ncf_dir_name)
                
        else:
            ofile.write(f"No netCDF files in directory {ncf_dir_name}\n")
            ofile.close()
            
            move_files_byFS_fromCodeCallDir(latlon_bound_ofile_name, ncf_dir_name)
        

def extract_and_store_period_bounds():
    
    #---------------------------------------------------#
    # Open each file and extract time array format data #
    #---------------------------------------------------#
 
    netcdf_files_dirs = get_netcdf_file_dirList(codeCallDir)
    lncfd = len(netcdf_files_dirs)
    
    for ncf_dir_num, ncf_dir_name in enumerate(netcdf_files_dirs, start=1):
        nc_files = get_netcdf_fileList(ncf_dir_name)
        lncfs = len(nc_files)
        
        ofile = open(period_bound_ofile_name, "w")
    
        if lncfs > 0:
            for ncf_num, ncf_name in enumerate(nc_files, start=1):    
                print("Extracting time bounds "
                      f"from file {ncf_num} out of {lncfs} "
                      f"at directory {ncf_dir_num} out of {lncfd}...")
                                
                faulty_file_trial = ncfile_integrity_status(ncf_name)
                
                if faulty_file_trial == 0:
                
                    time_var = find_time_dimension_raiseNone(ncf_name)
                    
                    if not time_var :
                        ofile.write(f"No 'time' dimension found in file {ncf_name}\n")
                    
                    else:    
                        times = get_times(ncf_name, time_var)
                        records = len(times)
                                        
                        arg_tuple_bounds1 = (
                            ncf_name,
                            times[0].values,
                            times[-1].values,
                            records
                            )
                        ofile.write(format_string(period_info_str, arg_tuple_bounds1))
                else: 
                    ofile.write(f"FAULTY FILE {ncf_name}\n")
                
            ofile.close()
            move_files_byFS_fromCodeCallDir(period_bound_ofile_name, ncf_dir_name)
                
        else:
            ofile.write(f"No netCDF files in directory {ncf_dir_name}\n")    
            ofile.close()
            move_files_byFS_fromCodeCallDir(period_bound_ofile_name, ncf_dir_name)


def extract_and_store_time_formats():
    
    #---------------------------------------------------#
    # Open each file and extract time array format data #
    #---------------------------------------------------#
    
    ofile_name = "time_formats.txt"

    netcdf_files_dirs = get_netcdf_file_dirList(codeCallDir)
    lncfd = len(netcdf_files_dirs)
    
    for ncf_dir_num, ncf_dir_name in enumerate(netcdf_files_dirs, start=1):
        nc_files = get_netcdf_fileList(ncf_dir_name)
        lncfs = len(nc_files)
        
        ofile = open(ofile_name, "w")

        if lncfs > 0:                
            for ncf_num, ncf_name in enumerate(nc_files, start=1):
                print("Extracting time formats "
                      f"from file {ncf_num} out of {lncfs} "
                      f"at directory {ncf_dir_num} out of {lncfd}...")
                
                faulty_file_trial = ncfile_integrity_status(ncf_name)
                
                if faulty_file_trial == 0:

                    time_var = find_time_dimension_raiseNone(ncf_name)
                    
                    if not time_var:
                        ofile.write(f"No 'time' dimension found in file {ncf_name}\n")
                    
                    else:
                        times = get_times(ncf_name, time_var)
                        records = len(times)
                            
                        arg_tuple_bounds2 = (
                            ncf_name,
                            times.values,
                            records
                            )
                        ofile.write(format_string(time_format_info_str, arg_tuple_bounds2))
                        
                else:
                    ofile.write(f"FAULTY FILE {ncf_name}\n")
                    
            ofile.close()
            move_files_byFS_fromCodeCallDir(ofile_name, ncf_dir_name)
            
        else:
            ofile.write(f"No netCDF files in directory {ncf_dir_name}\n")
            ofile.close()
            move_files_byFS_fromCodeCallDir(ofile_name, ncf_dir_name)


#--------------------#
# Dimension handlers #
#--------------------#

def find_time_dimension(nc_file_name):
    
    """
    Function that searches for time dimension names.
    It should always be located among dimensions,
    but it can happen that it either located only among variables
    or be duplicated among those.
    This function is designed to try both cases.
    
    Parameters
    ----------
    nc_file_name : str or xarray.Dataset
          String of the data file or the data set itself.
    
    Returns
    -------
    time_varlist : list
          List containing the strings that identify
          the time dimension.
    time_varlist_retry : list
          List containing the strings that identify
          the time variable.
          It is returned only if the previous case is not satisfied.
    """
    
    # Open the netCDF file if necessary #
    if isinstance(nc_file_name, str):
        ds = xr.open_dataset(nc_file_name)
        
    else:
        ds = nc_file_name.copy()
    
    # Search inside the dimension list #    
    dimlist = list(ds.dims)
    
    time_varlist = [key
                    for key in dimlist
                    if key.lower().startswith("t")
                    or key.lower().startswith("ti")
                    or key.lower().startswith("da")]
    time_varlist.sort()
    
    if len(time_varlist) > 0:       
        return time_varlist[0]
        
    else:
        
        # Search inside the variable list #    
        varlist = list(ds.variables)
        
        time_varlist_retry = [key
                              for key in varlist
                              if key.lower().startswith("t")
                              or key.lower().startswith("ti")
                              or key.lower().startswith("da")]
        time_varlist_retry.sort()
        
        if len(time_varlist_retry) > 0:
            return time_varlist_retry[0]
        
        else:
            raise ValueError("No 'time' dimension found in file {nc_file_name}")
            
    ds.close()
            
            
def find_time_dimension_raiseNone(nc_file_name):
    
    """
    Function that searches for time dimension names.
    It should always be located among dimensions,
    but it can happen that it either located only among variables
    or be duplicated among those.
    This function is designed to try both cases.
    
    Parameters
    ----------
    nc_file_name : str or xarray.Dataset
          String of the data file or the data set itself.
    
    Returns
    -------
    time_varlist : list
          List containing the strings that identify
          the time dimension.
    time_varlist_retry : list
          List containing the strings that identify
          the time variable.
          It is returned only if the previous case is not satisfied.
    """
    
    # Open the netCDF file if necessary #
    if isinstance(nc_file_name, str):
        ds = xr.open_dataset(nc_file_name)
        
    else:
        ds = nc_file_name.copy()
    
    # Search inside the dimension list #    
    dimlist = list(ds.dims)
    
    time_varlist = [key
                    for key in dimlist
                    if key.lower().startswith("t")
                    or key.lower().startswith("ti")
                    or key.lower().startswith("da")]
    time_varlist.sort()
    
    if len(time_varlist) > 0:       
        return time_varlist[0]
        
    else:
        
        # Search inside the variable list #    
        varlist = list(ds.variables)
        
        time_varlist_retry = [key
                              for key in varlist
                              if key.lower().startswith("t")
                              or key.lower().startswith("ti")
                              or key.lower().startswith("da")]
        time_varlist_retry.sort()
        
        if len(time_varlist_retry) > 0:
            return time_varlist_retry[0]
        
        else:
            return None
        
    ds.close()
            
            
def find_coordinate_variables(nc_file_name):
    
    """
    Function that searches for coordinate variable names.
    Usually those are located inside the dimension list,
    but it can happen that in some cases are among variables.
    This function is designed to try both cases.
    
    Parameters
    ----------
    nc_file_name : str or xarray.Dataset
          String of the data file or the data set itself.
    
    Returns
    -------
    coord_varlist : list
          List containing the strings that identify
          the 'latitude' and 'longitude' dimensions.
    coord_varlist_retry : list
          List containing the strings that identify
          the 'latitude' and 'longitude' variables.
          It is returned only if the previous case is not satisfied.
    """
    
    # Open the netCDF file if necessary #
    if isinstance(nc_file_name, str):
        ds = xr.open_dataset(nc_file_name)
        
    else:
        ds = nc_file_name.copy()
    
    # Search inside the dimension list #    
    dimlist = list(ds.dims)
    
    coord_varlist = [key
                     for key in dimlist
                     if key.lower().startswith("lat")
                     or key.lower().startswith("y")
                     or key.lower().startswith("lon")
                     or key.lower().startswith("x")]                             
    
    if len(coord_varlist) == 2: 
        coord_varlist.sort()
        return coord_varlist
        
    else:
        
        # Search inside the variable list #    
        varlist = list(ds.variables)
        coord_varlist_retry = [key
                               for key in varlist
                               if key.lower().startswith("lat")
                               or key.lower().startswith("y")
                               or key.lower().startswith("lon")
                               or key.lower().startswith("x")]
        
        if len(coord_varlist_retry) == 2:
            coord_varlist_retry.sort()
            return coord_varlist_retry
        
        else:
            raise ValueError("No 'latitude' or 'longitude' coordinates found "
                             f"in file '{nc_file_name}'")
            
    ds.close()
    
            
def find_coordinate_variables_raiseNone(nc_file_name):
    
    """
    Function that searches for coordinate variable names.
    Usually those are located inside the dimension list,
    but it can happen that in some cases are among variables.
    This function is designed to try both cases.
    
    Parameters
    ----------
    nc_file_name : str or xarray.Dataset
          String of the data file or the data set itself.
    
    Returns
    -------
    coord_varlist : list
          List containing the strings that identify
          the 'latitude' and 'longitude' dimensions.
    coord_varlist_retry : list
          List containing the strings that identify
          the 'latitude' and 'longitude' variables.
          It is returned only if the previous case is not satisfied.
    """
    
    # Open the netCDF file if necessary #
    if isinstance(nc_file_name, str):
        ds = xr.open_dataset(nc_file_name)
        
    else:
        ds = nc_file_name.copy()
    
    # Search inside the dimension list #    
    dimlist = list(ds.dims)
    
    coord_varlist = [key
                     for key in dimlist
                     if key.lower().startswith("lat")
                     or key.lower().startswith("y")
                     or key.lower().startswith("lon")
                     or key.lower().startswith("x")]
    
    if len(coord_varlist) == 2:       
        return coord_varlist
        
    else:
        
        # Search inside the variable list #    
        varlist = list(ds.variables)
        coord_varlist_retry = [key
                               for key in varlist
                               if key.lower().startswith("lat")
                               or key.lower().startswith("y")
                               or key.lower().startswith("lon")
                               or key.lower().startswith("x")]                             
        
        if len(coord_varlist_retry) == 2:
            return coord_varlist_retry
        
        else:
            return None
        
    ds.close()

        
def get_model_list(path_list, split_pos):

    """
    Function that searches for model names present
    in the given relative file path list.
    Paths can either be absolute, relative or only file names,
    but they should, as a matter of unification, contain low bars.
    If paths are relative or absolute, i.e. contain forward slashes,
    the function selects only the file name.
    Then it splits the file name and select the position, defined by the user
    taking the low bar as the separator.
    
    Parameters
    ----------
    path_list : list
          List of relative/absolute paths or file names.
    split_pos : int
          Integer that defines which position 
    
    Returns
    -------
    unique_model_list : list
          Unique list containing model names found in the path list.
    """
    
    fwd_slash_containing_files = [path
                                  for path in path_list
                                  if "/" in path]
    
    grib_file_list = [path.name
                 if len(fwd_slash_containing_files) > 0
                 and splitchar in path
                 else path
                 for path in path_list]
    
    unique_model_list = np.unique([f.split(splitchar)[split_pos]
                                   for f in grib_file_list
                                   if len(grib_file_list) > 0])
    
    return unique_model_list


def get_file_dimensions(nc_file):
    
    """
    Function that extracts dimensions names from a netCDF file.
    There are some cases in which variables are also among dimensions,
    so it is convenient to eliminate those.
    
    Parameters
    ----------
    nc_file : str or xarray.Dataset, throws an error otherwise.
          String or already opened file
          that identifies the netCDF file to work with.
    
    Returns
    -------
    dimension_names = list
          List containing the names of the dimensions.
    """
    
    if isinstance(nc_file, str):
        
        ds = xr.open_dataset(nc_file)
            
        varlist = list(ds.variables)
        dimlist = list(ds.dims)
        
        # Remove variables from the dimension list if present #
        dimlist_nodim = [dim
                         for dim in varlist
                         if dim in dimlist]
        
        ldn = len(dimlist_nodim)
        if ldn == 1:
            return dimlist_nodim[0]
        else:
            return dimlist_nodim
        
        ds.close()
        
    elif isinstance(nc_file, xr.Dataset):
        
        varlist = list(nc_file.variables)
        dimlist = list(nc_file.dims)
        
        # Remove variables from the dimension list if present #
        dimlist_nodim = [dim
                         for dim in varlist
                         if dim in dimlist]
        
        ldn = len(dimlist_nodim)
        if ldn == 1:
            return dimlist_nodim[0]
        else:
            return dimlist_nodim
    
    else:
        return TypeError("Cannot handle data file, wrong type of data file.")


def get_file_variables(nc_file):
    
    """
    Function that extracts variable names from a netCDF file.
    Usually some dimensions are also inside the variable list,
    so it is convenient to eliminate those.
    
    Parameters
    ----------
    nc_file : str or xarray.Dataset, throws an error otherwise.
          String or already opened file
          that identifies the netCDF file to work with.
    
    Returns
    -------
    variable_names = list
          List containing the names of the variables.
    """
    
    if isinstance(nc_file, str):
        
        ds = xr.open_dataset(nc_file)
        varlist = list(ds.variables)
        dimlist = list(ds.dims)
        
        # Remove dimensions from the variable list if present #
        varlist_nodim = [var
                         for var in varlist
                         if var not in dimlist]
        
        lvn = len(varlist_nodim)
        if lvn == 1:
            return varlist_nodim[0]
        else:
            return varlist_nodim
        
        ds.close()
        
    elif isinstance(nc_file, xr.Dataset):
        
        varlist = list(nc_file.variables)
        dimlist = list(nc_file.dims)
        
        # Remove dimensions from the variable list if present #
        varlist_nodim = [var
                         for var in varlist
                         if var not in dimlist]
        
        lvn = len(varlist_nodim)
        if lvn == 1:
            return varlist_nodim[0]
        else:
            return varlist_nodim
    
    else:
        return TypeError("Cannot handle data file, wrong type of data file.")


def get_latlon_bounds(netcdf_file,
                      lat_dimension_name,
                      lon_dimension_name,
                      value_roundoff):

    ds = xr.open_dataset(netcdf_file)
    
    lat_values = ds[lat_dimension_name].values.round(value_roundoff)
    lon_values = ds[lon_dimension_name].values.round(value_roundoff)
    
    ds.close()
        
    return lat_values, lon_values


def get_latlon_deltas(lat_values,
                      lon_values,
                      delta_roundoff):
    
    lat_delta = f"{abs(lat_values[0]-lat_values[1]):.{delta_roundoff}f}"
    lon_delta = f"{abs(lon_values[0]-lon_values[1]):.{delta_roundoff}f}"
    
    return lat_delta, lon_delta    
        
    
def get_times(netcdf_file,
              time_dimension_name):
    
    ds = xr.open_dataset(netcdf_file)
        
    time_values = ds[time_dimension_name]
    ds.close()

    return time_values


def find_nearest_coordinates(nc_file_name, lats_obs, lons_obs):
    
    coord_varlist = find_coordinate_variables(nc_file_name)
    
    ds = xr.open_dataset(nc_file_name)    
    lats_ds = np.array(ds[coord_varlist[0]], 'd')
    lons_ds = np.array(ds[coord_varlist[1]], 'd')
    
    lats_obs = np.array(lats_obs, 'd')
    lons_obs = np.array(lons_obs, 'd')
        
    nearest_lats = []
    nearest_lons = []
        
    for lat_obs, lon_obs in zip(lats_obs, lons_obs):
        nearest_lat_idx = (abs(lat_obs-lats_ds)).argmin()
        nearest_lon_idx = (abs(lon_obs-lons_ds)).argmin()
        
        nearest_lat = lats_ds[nearest_lat_idx]
        nearest_lon = lons_ds[nearest_lon_idx]
        
        nearest_lats.append(nearest_lat)
        nearest_lons.append(nearest_lon)
        
    ds.close()
    
    nearest_lats = np.round(nearest_lats, 3)
    nearest_lons = np.round(nearest_lons, 3)
        
    return nearest_lats, nearest_lons

        
def grib2netcdf(grib_file_list, on_shell=False, option_str=None):
        
    if on_shell:
        if isinstance(grib_file_list, str):
            nc_file_new = modify_obj_specs(grib_file_list, "ext", extensions[0])
            
        else:
            grib_allfile_info_str = fileList2String(grib_file_list)
            nc_file_new_noext = input("Please introduce a name "
                                      "for the netCDF file, "
                                      "WITHOUT THE EXTENSION: ")
            
            allowed_minimum_char_idx = find_substring_index(nc_file_new_noext,
                                                            regex_grib2nc,
                                                            advanced_search=True)
            
            while (allowed_minimum_char_idx == -1):
                print("Invalid file name.\nIt can contain alphanumeric characters, "
                      "as well as the following non-word characters: {. _ -}")
                
                nc_file_new_noext = input("Please introduce a valid name: ")
                allowed_minimum_char_idx = find_substring_index(nc_file_new_noext,
                                                                regex_grib2nc,
                                                                advanced_search=True)
                
            else:
                nc_file_new_noext = modify_obj_specs(nc_file_new_noext,
                                                     obj2modify="ext",
                                                     new_obj=extensions[0])
            
        if option_str is None:
            grib2netcdf_comm = f"grib_to_netcdf -o {nc_file_new} {grib_allfile_info_str}"                
        else:
            grib2netcdf_comm = f"grib_to_netcdf {option_str} -o {nc_file_new} {grib_allfile_info_str}"
            
        exec_shell_command(grib2netcdf_comm)
        
    else:   
        if isinstance(grib_file_list, str):
            grib_file_list = [grib_file_list]

        for grib_file in grib_file_list:
            grib_file_noext = get_obj_specs(grib_file, "name_noext", extensions[0])
            ds = xr.open_dataset(grib_file, engine="cfgrib")
            saveXarrayDSAsNetCDF(ds, grib_file_noext)
                
#--------------------------#
# Parameters and constants #
#--------------------------#

# Directory from where this code is being called #
codeCallDir = Path.cwd()

# File extensions #
extensions = ["nc", "csv"]

# Main file names #
latlon_bound_ofile_name = "latlon_bounds.txt"
period_bound_ofile_name = "period_bounds.txt"

# String splitting character #
splitchar = common_splitchar_list[0]

# RegEx control for GRIB-to-netCDF single file name #
regex_grib2nc = "^[a-zA-Z0-9\._-]$"

# Regridding method options #
method_list = [
    "bilinear",
    "conservative",
    "conservative_normed",
    "nearest_s2d",
    "nearest_d2s",
    "patch"
    ]

# Preformatted strings #
#----------------------#

# Main parameter scanning info strings #
latlon_info_str = \
"""=========================================================
·File: {}

·Latitudes:
 {}

·Longitudes:
 {}

-Latitude-longitude array dimensions = {} x {}
-Latitude-longitude array delta = ({}, {})
    
"""

period_info_str = \
"""=========================================================
·File: {}
·Time range: {} -- {}
-Range length = {}

"""
    
time_format_info_str = \
"""=========================================================
·File: {}
    
·Time array:
 {}

-Array length = {}

"""
    
# File scanning progress information strings #
report_fn_noext = "faulty_netcdf_file_report"

scan_progress_info_str =\
"""
File number: {} out of {}
Directory: {}
"""

scan_progress_str_evb =\
"""
File: {}
File number: {} out of {}
Directory: {}
"""

# Faulty file report's header string #
report_info_str =\
"""Faulty NETCDF format file report
--------------------------------

·Directory: {}
·Total scanned files scanned: {}
·Faulty file number: {}

·Faulty files:
"""
