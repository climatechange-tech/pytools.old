#----------------#
# Import modules #
#----------------#

import importlib
from pathlib import Path

import numpy as np
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

module_imp1 = "data_frame_handler.py"
module_imp1_path = f"{fixed_dirpath}/"\
                   f"pandas_data_frames/{module_imp1}"

spec1 = importlib.util.spec_from_file_location(module_imp1, module_imp1_path)
data_frame_handler = importlib.util.module_from_spec(spec1)
spec1.loader.exec_module(data_frame_handler)


module_imp2 = "file_handler.py"
module_imp2_path = f"{fixed_dirpath}/"\
                   f"files_and_directories/{module_imp2}"

spec2 = importlib.util.spec_from_file_location(module_imp2, module_imp2_path)
file_handler = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(file_handler)


module_imp3 = "string_handler.py"
module_imp3_path = f"{fixed_dirpath}/"\
                   f"strings/{module_imp3}"

spec3 = importlib.util.spec_from_file_location(module_imp3, module_imp3_path)
string_handler = importlib.util.module_from_spec(spec3)
spec3.loader.exec_module(string_handler)


module_imp4 = "file_and_directory_paths.py"
module_imp4_path = f"{fixed_dirpath}/"\
                   f"files_and_directories/{module_imp4}"

spec4 = importlib.util.spec_from_file_location(module_imp4, module_imp4_path)
file_and_directory_paths = importlib.util.module_from_spec(spec4)
spec4.loader.exec_module(file_and_directory_paths)


module_imp5 = "faulty_ncfile_detector.py"
module_imp5_path = f"{fixed_dirpath}/"\
                   f"weather_and_climate/{module_imp5}"

spec5 = importlib.util.spec_from_file_location(module_imp5, module_imp5_path)
faulty_ncfile_detector = importlib.util.module_from_spec(spec5)
spec5.loader.exec_module(faulty_ncfile_detector)

#----------------------------------------------------#
# Define imported module(s)´ function call shortcuts #
#----------------------------------------------------#

file_path_specs = string_handler.file_path_specs
join_file_path_specs = string_handler.join_file_path_specs

move_files_byFS_fromCodeCallDir = file_handler.move_files_byFS_fromCodeCallDir

find_ext_file_paths = file_and_directory_paths.find_ext_file_paths
find_ext_file_directories = file_and_directory_paths.find_ext_file_directories

binary_faulty_file_detector = faulty_ncfile_detector.binary_faulty_file_detector

save2csv = data_frame_handler.save2csv

#-------------------------#
# Define custom functions #
#-------------------------#

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
    
    file_name += ".nc"
    
    ds.to_netcdf(file_name, "w", format="NETCDF4")
    print(f"{file_name} file successfully created")
    
    
def saveXarrayDSAsNetCDF(xarray_ds,
                         file_name,
                         attrs_dict=None):
    
    # Function that writes a xarray data set directly into a netCDF,
    # with the option of updating attributes.
    # 
    # Parameters
    # ----------
    # xarray_ds : xarray.core.dataset.Dataset
    #       OPENED xarray data set.
    # file_name : str
    #       String for the resulting netCDF file name.
    # attrs_dict : dict
    #       Dictionary containing attributes, such as source,
    #       version, date of creation, etc.
    #       If not given, attributes will remain the same as the input file.
    # 
    # Returns
    # -------
    # netCDF file
    
    file_name += ".nc"
    
    if attrs_dict:
        xarray_ds.attrs = attrs_dict
    
    xarray_ds.to_netcdf(file_name, "w", format="NETCDF4")

    print(f"{file_name} has been successfully created")
    
    
def netCDF_regridder(ds_in, ds_image, method="bilinear"):
    
    import xesmf as xe
    
    # Function that regrids an xarray Dataset to that of the
    # desired Dataset. It is similar to CDO but more intuitive and
    # easier to understand, supported by Python.
    # 
    # Parameters
    # ----------
    # ds_in : xarray.core.dataset.Dataset
    #       Input xarray data set
    # ds_image : xarray.core.dataset.Dataset
    #       Xarray data set with grid specifications to which apply on ds_in.
    # method : {'bilinear', 'conservative', 'nearest_s2d', 'nearest_d2s', 'patch'}
    #       Regridding method. Defaults 'bilinear'.
    # 
    # Returns
    # -------
    # ds_out : xarray.core.dataset.Dataset
    #       Output data set regridded according to the grid specs of ds_in.
    
    method_list = [
        "bilinear",
        "conservative",
        "conservative_normed",
        "nearest_s2d",
        "nearest_d2s",
        "patch"
        ]
    
    if method not in method_list:
        raise ValueError("Wrong regridding method. "
                         "Options are {'bilinear', 'conservative', "
                         "'conservative_normed', 'nearest_s2d', "
                         "'nearest_d2s', 'patch'}.")
        
    regridder = xe.Regridder(ds_in, ds_image, method)
    ds_out = regridder(ds_in)
    
    return ds_out
    

def saveNCDataAsCSV(nc_file_name,
                    columns_to_drop,
                    separator,
                    save_index_bool,
                    save_header_bool,
                    date_format=None):
    
    # Function that saves netCDF data into a CSV file AS IT IS, where data variables
    # are originally 3D, dependent on (time, latitude, longitude).
    # It is intended to speed up further data processes,
    # especially when opening very large netCDF files with xarray,
    # which can take a long time.
    # Saving data into a CSV, it can then be read very rapidly so as to
    # load data for post-processing.
    # 
    # For that, it seeks for essential variables,
    # together with 'time' dimension, if present.
    # It then concatenates whole data into a data frame and then
    # saves it into a CSV file.
    # 
    # Parameters
    # ----------
    # nc_file_name : str
    #       String of the xarray data set containing file.
    # columns_to_drop : str or list of str
    #       Names of the columns to drop, if desired, from the
    #       resultant data frame of xarray.to_pandas() method.
    # separator : str
    #       String used to separate data columns.
    # save_index_bool : bool
    #       Boolean to choose whether to include a column into the excel document
    #       that identifies row numbers. Default value is False.
    # save_header_bool : bool
    #       Boolean to choose whether to include a row into the excel document
    #       that identifies column numbers. Default value is False.
    # date_format : str
    #       In case the data frame contains a time column,
    #       use to give format thereof when storing the data frame.
    # 
    # Returns
    # -------
    # CSV file containing data as arranged on the data frame.
    # 
    # Notes
    # -----
    # Remember that this function serves as a direct copy of netCDF4 data,
    # if data modifications are required, then it cannot be used.
    # Data frames are only 2D, so that those
    # can only reflect a specific point multi-variable netCDF data along time
    # or several grid points' data for a specific time position.
    # Data frame column names will be the same as those on netCDF data file.
    
    # Open netCDF data file #
    print(f"Opening {nc_file_name}...")
    ds = xr.open_dataset(nc_file_name)
    
    if isinstance(columns_to_drop, str):
        columns_to_drop = [columns_to_drop]
        
    data_frame\
    = ds.to_pandas().reset_index(drop=False).drop(columns=columns_to_drop)
        
    # Define file format saver parameters #
    #-------------------------------------#
    
    extension = "csv"
    
    file_path_noname, file_path_name, file_path_name_split, file_path_ext\
    = file_path_specs(nc_file_name, file_path_splitchar)
    
    # Change the extension to that of the desired one #
    file_path_ext = extension
    
    csv_file_name = join_file_path_specs(file_path_noname,
                                         file_path_name,
                                         file_path_ext)
    
    # Save data as desired format file #   
    #----------------------------------#
    
    save2csv(csv_file_name,
             data_frame,
             separator,
             save_index_bool,
             save_header_bool,
             date_format)
    
    print(f"{csv_file_name} successfully created.")
        
#-----------------------#
# Basic data extractors #
#-----------------------#

def get_netcdf_fileList(path_to_walk_in):
    
    netcdf_files = find_ext_file_paths(extension, 
                                       path_to_walk_in, 
                                       top_path_only=True)
    
    return netcdf_files


def get_netcdf_file_dirList(path_to_walk_in):
    
    netcdf_files_dirs = find_ext_file_directories(extension, path_to_walk_in)
    
    return netcdf_files_dirs


def extract_and_store_latlon_bounds(delta_roundoff, value_roundoff):

    #------------------------------------------------------------------------#
    # Open each file, extract coordinate dimension data and save to txt file #
    #------------------------------------------------------------------------#
    
    ofile_name = "latlon_bounds.txt"
    
    latlon_table = '''=========================================================
·File: {}

·Latitudes:
 {}

·Longitudes:
 {}

-Latitude-longitude array dimensions = {} x {}
-Latitude-longitude array delta = {} x {}
    
'''

    netcdf_files_dirs = get_netcdf_file_dirList(cwd)
    lncfd = len(netcdf_files_dirs)
    
    for ncf_dir in enumerate(netcdf_files_dirs):
        ncf_dir_name = str(ncf_dir[-1])
        ncf_dir_num = ncf_dir[0] + 1
        
        nc_files = get_netcdf_fileList(ncf_dir_name)
        lncfs = len(nc_files)
        
        ofile = open(ofile_name, "w")
    
        if lncfs > 0:
            for ncf in enumerate(nc_files):
                ncf_name = ncf[-1]
                ncf_num = ncf[0] + 1
                
                print("Extracting coordinate values "
                      f" from file {ncf_num} out of {lncfs}"
                      f" at directory {ncf_dir_num} out of {lncfd}...")
                
                faulty_file_trial = binary_faulty_file_detector(ncf_name)
                
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
                            
                            ofile.write(latlon_table.format(ncf_name,
                                                            lats, 
                                                            lons,
                                                            llats,
                                                            llons,
                                                            deltas[0],
                                                            deltas[1]))
                        except:
                            llats = 1
                            llons = 1
                            
                            lat_delta = 0
                            lon_delta = 0
                        
                            ofile.write(latlon_table.format(ncf_name,
                                                            lats, 
                                                            lons,
                                                            llats,
                                                            llons,
                                                            lat_delta,
                                                            lon_delta))
                                                
                else: 
                    ofile.write(f"FAULTY FILE {ncf_name}\n")
                            
                            
            ofile.close()
            move_files_byFS_fromCodeCallDir(ofile_name, ncf_dir_name)
                
        else:
            ofile.write(f"No netCDF files in directory {ncf_dir_name}\n")
            ofile.close()
            
            move_files_byFS_fromCodeCallDir(ofile_name, ncf_dir_name)
        

def extract_and_store_period_bounds():
    
    #---------------------------------------------------#
    # Open each file and extract time array format data #
    #---------------------------------------------------#

    ofile_name = "period_bounds.txt"
    
    period_table = '''=========================================================
·File: {}
·Time range: {} -- {}
·Array length = {}

'''
    
    netcdf_files_dirs = get_netcdf_file_dirList(cwd)
    lncfd = len(netcdf_files_dirs)
    
    for ncf_dir in enumerate(netcdf_files_dirs):
        ncf_dir_name = str(ncf_dir[-1])
        ncf_dir_num = ncf_dir[0] + 1
        
        nc_files = get_netcdf_fileList(ncf_dir_name)
        lncfs = len(nc_files)
        
        ofile = open(ofile_name, "w")
    
        if lncfs > 0:
            for ncf in enumerate(nc_files):
                ncf_name = ncf[-1]
                ncf_num = ncf[0] + 1
                    
                print("Extracting time bounds "
                      f"from file {ncf_num} out of {lncfs}"
                      f" at directory {ncf_dir_num} out of {lncfd}...")
                                
                faulty_file_trial = binary_faulty_file_detector(ncf_name)
                
                if faulty_file_trial == 0:
                
                    time_var = find_time_dimension_raiseNone(ncf_name)
                    
                    if not time_var :
                        ofile.write(f"No 'time' dimension found in file {ncf_name}\n")
                    
                    else:    
                        times = get_times(ncf_name, time_var)
                        records = len(times)
                                        
                        ofile.write(period_table.format(ncf_name,
                                                        times[0].values,
                                                        times[-1].values,
                                                        records))
                else: 
                    ofile.write(f"FAULTY FILE {ncf_name}\n")
                
            ofile.close()
            move_files_byFS_fromCodeCallDir(ofile_name, ncf_dir_name)
                
        else:
            ofile.write(f"No netCDF files in directory {ncf_dir_name}\n")    
            ofile.close()
            move_files_byFS_fromCodeCallDir(ofile_name, ncf_dir_name)


def extract_and_store_time_formats():
    
    #---------------------------------------------------#
    # Open each file and extract time array format data #
    #---------------------------------------------------#
    
    
    ofile_name = "time_formats.txt"
    
    time_format_table = '''====================================================
·File: {}
    
·Time array:
 {}

-Array length = {}

'''
    
    netcdf_files_dirs = get_netcdf_file_dirList(cwd)
    lncfd = len(netcdf_files_dirs)
    
    for ncf_dir in enumerate(netcdf_files_dirs):
        ncf_dir_name = str(ncf_dir[-1])
        ncf_dir_num = ncf_dir[0] + 1
        
        nc_files = get_netcdf_fileList(ncf_dir_name)
        lncfs = len(nc_files)
        
        ofile = open(ofile_name, "w")

        if lncfs > 0:                
            for ncf in enumerate(nc_files):
                ncf_name = ncf[-1]
                ncf_num = ncf[0] + 1
                
                print("Extracting time formats "
                      f"from file {ncf_num} out of {lncfs}"
                      f" at directory {ncf_dir_num} out of {lncfd}...")
                
                faulty_file_trial = binary_faulty_file_detector(ncf_name)
                
                if faulty_file_trial == 0:

                    time_var = find_time_dimension_raiseNone(ncf_name)
                    
                    if not time_var:
                        ofile.write(f"No 'time' dimension found in file {ncf_name}\n")
                    
                    else:
                        times = get_times(ncf_name, time_var)
                        records = len(times)
                            
                        ofile.write(time_format_table.format(ncf_name,
                                                             times.values,
                                                             records))
                        
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
    
    # Function that searches for time dimension names.
    # It should always be located among dimensions,
    # but it can happen that it either located only among variables
    # or be duplicated among those.
    # This function is designed to try both cases.
    # 
    # Parameters
    # ----------
    # nc_file_name : str or xarray.core.dataset.Dataset
    #       String of the data file or the data set itself.
    # 
    # Returns
    # -------
    # time_varlist : list
    #       List containing the strings that identify
    #       the time dimension.
    # time_varlist_retry : list
    #       List containing the strings that identify
    #       the time variable.
    #       It is returned only if the previous case is not satisfied.
    
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
    
    # Function that searches for time dimension names.
    # It should always be located among dimensions,
    # but it can happen that it either located only among variables
    # or be duplicated among those.
    # This function is designed to try both cases.
    # 
    # Parameters
    # ----------
    # nc_file_name : str or xarray.core.dataset.Dataset
    #       String of the data file or the data set itself.
    # 
    # Returns
    # -------
    # time_varlist : list
    #       List containing the strings that identify
    #       the time dimension.
    # time_varlist_retry : list
    #       List containing the strings that identify
    #       the time variable.
    #       It is returned only if the previous case is not satisfied.
    
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
    
    # Function that searches for coordinate variable names.
    # Usually those are located inside the dimension list,
    # but it can happen that in some cases are among variables.
    # This function is designed to try both cases.
    # 
    # Parameters
    # ----------
    # nc_file_name : str or xarray.core.dataset.Dataset
    #       String of the data file or the data set itself.
    # 
    # Returns
    # -------
    # coord_varlist : list
    #       List containing the strings that identify
    #       the 'latitude' and 'longitude' dimensions.
    # coord_varlist_retry : list
    #       List containing the strings that identify
    #       the 'latitude' and 'longitude' variables.
    #       It is returned only if the previous case is not satisfied.
    
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
                             f"in file {nc_file_name}")
            
    ds.close()
    
            
def find_coordinate_variables_raiseNone(nc_file_name):
    
    # Function that searches for coordinate variable names.
    # Usually those are located inside the dimension list,
    # but it can happen that in some cases are among variables.
    # This function is designed to try both cases.
    # 
    # Parameters
    # ----------
    # nc_file_name : str or xarray.core.dataset.Dataset
    #       String of the data file or the data set itself.
    # 
    # Returns
    # -------
    # coord_varlist : list
    #       List containing the strings that identify
    #       the 'latitude' and 'longitude' dimensions.
    # coord_varlist_retry : list
    #       List containing the strings that identify
    #       the 'latitude' and 'longitude' variables.
    #       It is returned only if the previous case is not satisfied.
    
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

    # Function that searches for model names present
    # in the given relative file path list.
    # Paths can either be absolute, relative or only file names,
    # but they should, as a matter of unification, contain low bars.
    # If paths are relative or absolute, i.e. contain forward slashes,
    # the function selects only the file name.
    # Then it splits the file name and select the position, defined by the user
    # taking the low bar as the separator.
    #
    # Parameters
    # ----------
    # path_list : list
    #       List of absolute/relative paths or file names.
    # split_pos : int
    #       Integer that defines which position 
    #
    # Returns
    # -------
    # unique_model_list : list
    #       Unique list containing model names found in the path list.
    
    fwd_slash_containing_files = [path
                                  for path in path_list
                                  if "/" in path]
    
    file_list = [path.name
                 if len(fwd_slash_containing_files) > 0
                 and file_path_splitchar in path
                 else path
                 for path in path_list]
    
    unique_model_list = np.unique([f.split(file_path_splitchar)[split_pos]
                                   for f in file_list
                                   if len(file_list) > 0])
    
    return unique_model_list


def get_file_dimensions(nc_file):
    
    # Function that extracts dimensions names from a netCDF file.
    # There are some cases in which variables are also among dimensions,
    # so it is convenient to eliminate those.
    # 
    # Parameters
    # ----------
    # nc_file : str or xarray.core.dataset.Dataset, throws an error otherwise.
    #       String or already opened file
    #       that identifies the netCDF file to work with.
    # 
    # Returns
    # -------
    # dimension_names = list
    #       List containing the names of the dimensions.
    
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
        
    elif isinstance(nc_file, xr.core.dataset.Dataset):
        
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
    
    # Function that extracts variable names from a netCDF file.
    # Usually some dimensions are also inside the variable list,
    # so it is convenient to eliminate those.
    # 
    # Parameters
    # ----------
    # nc_file : str or xarray.core.dataset.Dataset, throws an error otherwise.
    #       String or already opened file
    #       that identifies the netCDF file to work with.
    # 
    # Returns
    # -------
    # variable_names = list
    #       List containing the names of the variables
    
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
        
    elif isinstance(nc_file, xr.core.dataset.Dataset):
        
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
        

# TODO: grib formatotik netCDFra pasatzeko funtzioa garatu
#def grib2netcdf(file_list):
    # import eccodes as ecs
    
#-----------------------------------------------#
# Define global parameters below every function #
#-----------------------------------------------#

"""Declare those global so as not to use them
repeatedly inside functions above.
"""

extension = "nc"
file_path_splitchar = "_"