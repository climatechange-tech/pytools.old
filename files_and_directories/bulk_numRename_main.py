#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
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

custom_mod1_path = f"{fixed_path}/arrays_and_lists"
custom_mod2_path = f"{fixed_path}/files_and_directories"  
custom_mod3_path = f"{fixed_path}/parameters_and_constants"
custom_mod4_path = f"{fixed_path}/strings"
custom_mod5_path = f"{fixed_path}/time_handling"
                                        
# Add the module paths to the path variable #
#-------------------------------------------#

sys.path.append(custom_mod1_path)
sys.path.append(custom_mod2_path)
sys.path.append(custom_mod3_path)
sys.path.append(custom_mod4_path)
sys.path.append(custom_mod5_path)

# Perform whole or partial module importations #
#----------------------------------------------#

from array_handler import select_array_elements
from datetime_operators import get_current_time, get_obj_operation_datetime
import file_and_directory_paths
from file_and_directory_handler import rename_objects
import global_parameters
import information_output_formatters
import string_handler

#--------------------------------------------------#
# Define imported modules' objname_unevennction call shortcuts #
#--------------------------------------------------#

find_allfile_extensions = file_and_directory_paths.find_allfile_extensions
find_ext_file_paths = file_and_directory_paths.find_ext_file_paths
find_fileString_paths = file_and_directory_paths.find_fileString_paths

find_allDirectories = file_and_directory_paths.find_allDirectories
find_fileString_directories = file_and_directory_paths.find_fileString_directories

print_format_string = information_output_formatters.print_format_string
format_string = information_output_formatters.format_string

find_substring_index = string_handler.find_substring_index
obj_path_specs = string_handler.obj_path_specs
modify_obj_specs = string_handler.modify_obj_specs

basic_time_format_strs = global_parameters.basic_time_format_strs
basic_object_types = global_parameters.basic_object_types
non_std_time_format_strs = global_parameters.non_std_time_format_strs

#------------------#
# Define functions #
#------------------#

def shorten_conflicting_obj_list():
    if not ((not isinstance(lcos_upperLimit, int) and (isinstance(lcos_upperLimit, str))\
             and lcos_upperLimit == 'inf')\
            or (isinstance(lcos_upperLimit, int) and lcos_upperLimit>=1)):
        
        raise ValueError("Limit of the number of conflicting files "
                         "to be written to an output file "
                         "must be an integer ranging from 1 to 'inf'.")
    else:
        if lcos_upperLimit == 'inf':
            return False
        else:
            return True


def loop_renamer(objList,
                 obj_type="file",
                 starting_number="default",  
                 zero_padding="default",
                 dry_run=False,
                 splitchar=None):
    
    arg_names = loop_renamer.__code__.co_varnames
    ot_arg_pos = find_substring_index(arg_names, 
                                      "obj_type",
                                      find_whole_words=True)
    
    if obj_type not in basic_object_types:
        raise ValueError(f"Wrong '{arg_names[ot_arg_pos]}' option. "
                         f"Options are {basic_object_types}.")
        
    num_formatted_objs = []
    obj2change = obj2change_dict.get(obj_type)

    for obj_num, obj_name in enumerate(objList, start=starting_number):
        if zero_padding == "default":
            fpn_noext = obj_path_specs(obj_name, obj_spec_key="name_noext")
            new_zp = str(len(fpn_noext))
            num_format = f"{obj_num:0{new_zp}d}"    
        else:
            num_format = f"{obj_num:0{zero_padding}d}"    
            
        if obj_type == basic_object_types[0]:
            num_formatted_obj = modify_obj_specs(obj_name,
                                                 obj2change, 
                                                 num_format)
        else:
            fpn_parts = obj_path_specs(obj_name,
                                       obj_spec_key="name_noext_parts",
                                       splitchar=splitchar)
                    
            nf_changes_tuple = (fpn_parts[0], num_format)
            num_formatted_obj = modify_obj_specs(obj_name,
                                                   obj2change, 
                                                   nf_changes_tuple)
            
        if dry_run:
            num_formatted_objs.append(num_formatted_obj)
            
        else:
            rename_objects(obj_name, num_formatted_obj)
            
    lnffs = len(num_formatted_objs)
    
    if lnffs > 0:
        print("Dry-run mode chosen, "
              f"potentially renamed {obj_type} list will be given.")
        
        return num_formatted_objs
            

def loop_direct_renamer(objList, fixed_new_objList):  
    for obj, new_obj in zip(objList, fixed_new_objList):
        rename_objects(obj, new_obj)
        

def return_report_file_fixedPath(file_path_noname, 
                                 file_name,
                                 extension):
    
    report_file_path = f"{file_path_noname}/{file_name}.{extension}"
    return report_file_path


def reorder_objs(path,
                 obj_type,
                 extensions2skip="",
                 index_range="all",
                 starting_number="default",
                 zero_padding="default",
                 splitchar=None):
    
    # Quality control of the input parameters #
    arg_names = reorder_objs.__code__.co_varnames
    defaults = reorder_objs.__defaults__
        
    zp_arg_pos = find_substring_index(arg_names, "zero_padding")
    stn_arg_pos = find_substring_index(arg_names, "starting_number")
    ir_arg_pos = find_substring_index(arg_names, "index_range")
    
    if ((zero_padding != 'default' and not isinstance(zero_padding, int))\
        or (zero_padding != 'default'
            and isinstance(zero_padding, int) 
            and zero_padding < 1)):
        raise TypeError(f"Argument '{arg_names[zp_arg_pos]}' "
                        f"at position {zp_arg_pos} must either be "
                        "an integer equal or greater than 1.\n"
                        "Set to `None` if no zero padding is desired.")
          
    if path is None:
        raise ValueError("A path string or PosixPath must be given.")
        
    if isinstance(index_range, str) or index_range != "all":
        raise TypeError("Index range format must be of range(min, max).")
    
    if obj_type == basic_object_types[0]:
        ext_list = find_allfile_extensions(extensions2skip, path, top_path_only=True)
        objList_uneven = find_ext_file_paths(ext_list, path, top_path_only=True)
    
    elif obj_type == basic_object_types[1]:
        objList_uneven = find_allDirectories(path, 
                                             top_path_only=True,
                                             include_root=True)
        
    lou = len(objList_uneven)
    
    if index_range == "all":
        
        """
        1st step
        --------
        
        Rename objects (files or directories) starting from the highest number,
        to prevent overwriting and object deletion because of
        unevenly spaced numbering.
        This operation guarantees monotonous and unity-increasing numbering.
        
        By default the program uses the length of the object list,
        but it can be change as needed.
        
        Due to irregular numbering 
        as a result of object copying or renaming from different devices,
        any numbered object can be larger than that length.
        Appart from that, there can be newer objects that contain characters
        and they even need to be placed back in the time.
        
        In order to prevent that problem, 
        the user can customize the starting number.
        
        In any case the program will firstly attempt a dry run and
        let know if there are conflicting objects.
        """
          
        if starting_number == "default":
            resetting_number = lou + 1
            
        else:
            """This option lets the user choose any starting number."""
            resetting_number = starting_number
            
        num_formatted_objs_dryRun_1 = loop_renamer(objList_uneven, 
                                                   starting_number=resetting_number,
                                                   zero_padding=zero_padding,
                                                   dry_run=True,
                                                   splitchar=splitchar)
                          
        """2nd step:
        Rename directories starting from 1, now that object numbering
        is evenly spaced.
        """
        
        num_formatted_objs_dryRun_2 = loop_renamer(num_formatted_objs_dryRun_1,
                                                   starting_number=1, 
                                                   zero_padding=zero_padding,
                                                   dry_run=True,
                                                   splitchar=splitchar)
                                        
        # Check for equally named, conflicting objects #
        #----------------------------------------------#
        
        if obj_type == basic_object_types[0]:
            conflicting_objs = [find_fileString_paths(f"*{Path(nff_dR2).stem}*",
                                                      path,
                                                      top_path_only=True)
                                for nff_dR2 in num_formatted_objs_dryRun_2]
            
        elif obj_type == basic_object_types[1]:
            conflicting_objs = [find_fileString_directories(f"*{Path(nff_dR2).stem}*",
                                                            path,
                                                            top_path_only=True)
                                for nff_dR2 in num_formatted_objs_dryRun_2]
        
        lcos = len(conflicting_objs)
        
        if lcos > 0:
            
            # Set maximum length of the conflicting objects to write on file, if not 'inf'
            wantlimit = shorten_conflicting_obj_list()
            if wantlimit:
                conflicting_objs = conflicting_objs[:lcos_upperLimit]            
            
            report_file_name = report_filename_dict.get(obj_type)     
            report_file_path = return_report_file_fixedPath(path,
                                                            report_file_name,
                                                            fixed_ext)
            
            rf = open(report_file_path, "w")                    
         
            timestamp_str_objname_uneven\
            = get_obj_operation_datetime(objList_uneven,
                                         "modification", 
                                         time_format_str)
            
            timestamp_str_nff_dR2\
            = get_current_time(time_fmt_string=ctime_format_str)
            
            timestamp_str_confl_obj\
            = get_obj_operation_datetime(conflicting_objs,
                                         "modification", 
                                         time_format_str)
            
            for objname_uneven, nff_dR2, confl_obj in zip(objList_uneven,
                                                          num_formatted_objs_dryRun_2,
                                                          conflicting_objs):
            
                arg_tuple_reorder_objs1 = (objname_uneven, 
                                           timestamp_str_objname_uneven,
                                           nff_dR2,
                                           timestamp_str_nff_dR2,
                                           confl_obj, 
                                           timestamp_str_confl_obj)
                rf.write(format_string(conf_obj_info_str, arg_tuple_reorder_objs1))
                         
            rf.close()
                
            if obj_type == basic_object_types[0]:
                arg_tuple_reorder1 = ("files", report_file_name)
                print_format_string(conflictingObjectsWarning, arg_tuple_reorder1)
                
            elif obj_type == basic_object_types[1]:
                arg_tuple_reorder2 = ("directories", report_file_name)
                print_format_string(conflictingObjectsWarning, arg_tuple_reorder2) 
 
        else:
            
            report_file_name = "dry-run_renaming_report"    
            report_file_path = return_report_file_fixedPath(path,
                                                            report_file_name,
                                                            fixed_ext)
            rf = open(report_file_path, "w")                    
            
            for objname_uneven, nff_dR2 in zip(objList_uneven, num_formatted_objs_dryRun_2):
                arg_tuple_reorder_objs2 = (objname_uneven,
                                           timestamp_str_objname_uneven,
                                           nff_dR2,
                                           timestamp_str_nff_dR2)
                rf.write(conf_obj_info_str, arg_tuple_reorder_objs2)
                         
            rf.close()
                
            if obj_type == basic_object_types[0]:
                arg_tuple_reorder3 = ("files", report_file_name)
                print_format_string(noConflictingObjectsMessage, arg_tuple_reorder3)
                
            elif obj_type == basic_object_types[1]:
                arg_tuple_reorder4 = ("directories", report_file_name)
                print_format_string(noConflictingObjectsMessage, arg_tuple_reorder4)
                
            ansPerformChanges\
            = input("Would you like to perform the changes? [y/n] ")
 
            while (ansPerformChanges != "y" and ansPerformChanges != "n"):   
                ansPerformChanges\
                = input("Please write 'y' for 'yes' or 'n' for 'no' ")
                
            else:
                loop_direct_renamer(objList_uneven, num_formatted_objs_dryRun_2)
             
    else:
        
        objList_uneven_slice = select_array_elements(objList_uneven,
                                                     index_range)   
        
        if starting_number == "default":
            raise ValueError(f"'{arg_names[stn_arg_pos]}' argument "
                             f"at position {stn_arg_pos} "
                             f"cannot be '{defaults[stn_arg_pos]}' "
                             f"if '{ir_arg_pos}' argument is not None")
               
        num_formatted_objs_dryRun = loop_renamer(objList_uneven_slice, 
                                                 starting_number=starting_number, 
                                                 zero_padding=zero_padding,
                                                 dry_run=True,
                                                 splitchar=splitchar)
          
        # Check for equally named, conflicting objects #
        #----------------------------------------------#
        
        if obj_type == basic_object_types[0]:
            conflicting_objs = [find_fileString_paths(f"*{Path(nff_dR).stem}*",
                                                      path,
                                                      top_path_only=True)
                                for nff_dR in num_formatted_objs_dryRun]
        
        elif obj_type == basic_object_types[1]:
            conflicting_objs = [find_fileString_directories(f"*{Path(nff_dR).stem}*",
                                                            path,
                                                            top_path_only=True)
                                for nff_dR in num_formatted_objs_dryRun]
            
        lcos = len(conflicting_objs)
        
        if lcos > 0:
            
            # Set maximum length of the conflicting objects to write on file, if not 'inf'
            wantlimit = shorten_conflicting_obj_list()
            if wantlimit:
                conflicting_objs = conflicting_objs[:lcos_upperLimit]   
                
            report_file_name = report_filename_dict.get(obj_type)
            report_file_path = return_report_file_fixedPath(path,
                                                            report_file_name,
                                                            fixed_ext)
            
            rf = open(report_file_path, "w")                    
              
            timestamp_str_objname_unevens\
            = get_obj_operation_datetime(objList_uneven_slice,
                                         "modification", 
                                         time_format_str)
            
            timestamp_str_nff_dR\
            = get_current_time(time_fmt_string=ctime_format_str)
            
            timestamp_str_confl_obj\
            = get_obj_operation_datetime(conflicting_objs,
                                         "modification", 
                                         time_format_str)
            
            for objname_unevens, nff_dR, confl_obj in zip(objList_uneven_slice,
                                                          num_formatted_objs_dryRun,
                                                          conflicting_objs):
            
                arg_tuple_reorder_objs3 = (objname_unevens, 
                                           timestamp_str_objname_unevens,
                                           nff_dR,
                                           timestamp_str_nff_dR,
                                           confl_obj,
                                           timestamp_str_confl_obj)
                rf.write(format_string(conf_obj_info_str, arg_tuple_reorder_objs3))
                         
            rf.close()
                
            print(f"\n\nSome renamed objs conflict! Information is stored "
                  f"at file '{report_file_name}'.")
                
        else:
            
            report_file_name = "dry-run_renaming_report"    
            report_file_path = return_report_file_fixedPath(path,
                                                           report_file_name,
                                                           fixed_ext)
            rf = open(report_file_path, "w")                    
            
            for objname_unevens, nff_dr in zip(objList_uneven_slice, 
                                               num_formatted_objs_dryRun):
                arg_tuple_reorder_objs4 = (objname_unevens, nff_dR)
                rf.write(format_string(dry_run_info_str, arg_tuple_reorder_objs4))
                         
            rf.close()
                
            print("No conflicting objs found. "
                  "Please check the dry-run renaming information "
                  f"at file '{report_file_name}'.")
       
            ansPerformChanges\
            = input("Would you like to perform the changes? [y/n] ")
 
            while (ansPerformChanges != "y" and ansPerformChanges != "n"):
                ansPerformChanges\
                = input("Please write 'y' for 'yes' or 'n' for 'no' ")
            else:
                loop_direct_renamer(objList_uneven_slice, num_formatted_objs_dryRun)
                           

#--------------------------#
# Parameters and constants #
#--------------------------#

# Time formatting strings #
time_format_str = basic_time_format_strs["H"]
ctime_format_str = non_std_time_format_strs["CFT_H"]

# Fixed extension to reuse at different parts of the objname_unevennctions #
fixed_ext = "txt"

# Fixed length of the list containing the conflicting file or directory names #
"""Set the minimum limit to 1.
If no limit wants to be considered, set the parameter to 'inf'
"""
lcos_upperLimit = 2
        

# Preformatted strings #
#----------------------#

# Object path comparisons and conflicts, if any, due to already existing ones #
conf_obj_info_str\
= """'{}' <--> '{}' renamed to '{}' <--> '{}' conflicts with '{}' <--> '{}'\n"""

dry_run_info_str = """'{}' renamed to '{}'\n"""

conflictingObjectsWarning = """\n\nSome renamed {} conflict!
Information is stored at file '{}'."""

noConflictingObjectsMessage = """No conflicting {} found
Please check the dry-run renaming information at file '{}'."""


# Switch-case dictionaries #
#--------------------------#

report_filename_dict = {
    basic_object_types[0] : "conflicting_files_report",
    basic_object_types[1] : "conflicting_directories_report"
    }

obj2change_dict = {
    basic_object_types[0] : "name_noext",
    basic_object_types[1] : "name_noext_parts"
    }
