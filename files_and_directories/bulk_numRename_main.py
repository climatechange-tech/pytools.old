#----------------#
# Import modules #
#----------------#

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

# Perform the module importations #
#---------------------------------#

import array_handler
import file_and_directory_paths
import file_and_directory_handler
import global_parameters
import string_handler
import time_formatters

#--------------------------------------------------#
# Define imported modules' function call shortcuts #
#--------------------------------------------------#

select_array_elements = array_handler.select_array_elements

find_allfile_extensions = file_and_directory_paths.find_allfile_extensions
find_ext_file_paths = file_and_directory_paths.find_ext_file_paths
find_fileString_paths = file_and_directory_paths.find_fileString_paths

find_allDirectories = file_and_directory_paths.find_allDirectories
find_fileString_directories = file_and_directory_paths.find_fileString_directories

find_substring_index = string_handler.find_substring_index
obj_path_specs = string_handler.obj_path_specs
modify_obj_specs = string_handler.modify_obj_specs

rename_objects = file_and_directory_handler.rename_objects

get_current_time = time_formatters.get_current_time
get_obj_operation_datetime = time_formatters.get_obj_operation_datetime

basic_time_format_strs = global_parameters.basic_time_format_strs
basic_object_types = global_parameters.basic_object_types

move_files_byExts_fromCodeCallDir = file_and_directory_handler.move_files_byExts_fromCodeCallDir

#------------------#
# Define functions #
#------------------#

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
    
    if obj_type not in bo_types:
        raise ValueError(f"Wrong '{arg_names[ot_arg_pos]}' option. "
                         f"Options are {bo_types}.")
        
    num_formatted_objs = []
    
    if obj_type == bo_types[0]:
        obj2change = "name_noext"
    else:
        obj2change = "name_noext_parts"

    for obj in enumerate(objList, start=starting_number):
        
        obj_num = obj[0]
        obj_name = obj[-1]

        if zero_padding == "default":
            fpn_noext = obj_path_specs(obj_name, obj_spec_key="name_noext")
            new_zp = str(len(fpn_noext))
            num_format = f"{obj_num:0{new_zp}d}"    
            
        else:
            num_format = f"{obj_num:0{zero_padding}d}"    
            
        if obj_type == bo_types[0]:
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
    
    arg_names = reorder_objs.__code__.co_varnames
    defaults = reorder_objs.__defaults__
        
    zp_arg_pos = find_substring_index(arg_names, "zero")
    stn_arg_pos = find_substring_index(arg_names, "start")
    ir_arg_pos = find_substring_index(arg_names, "index")
    
    if zero_padding != "default" and not isinstance(zero_padding, int):
        raise TypeError(f"Argument '{arg_names[zp_arg_pos]}' "
                        f"at position {zp_arg_pos} must either be "
                        "an integer or 'default'.")
        
    if path is None:
        raise ValueError("A path string or PosixPath must be given.")
        
    if isinstance(index_range, str) or index_range != "all":
        raise TypeError("Index range format must be of range(min, max).")
    
    if obj_type == bo_types[0]:
        ext_list = find_allfile_extensions(extensions2skip, path, top_path_only=True)
        objList_uneven = find_ext_file_paths(ext_list, path, top_path_only=True)
    
    elif obj_type == bo_types[1]:
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
                                        
        # Check for equally named conflicting objs #
        #-------------------------------------------#
        
        if obj_type == bo_types[0]:
            conflicting_objs = [find_fileString_paths(f"*{Path(nff_dR2).stem}*",
                                                      path,
                                                      top_path_only=True)
                                for nff_dR2 in num_formatted_objs_dryRun_2]
            
        elif obj_type == bo_types[1]:
            conflicting_objs = [find_fileString_directories(f"*{Path(nff_dR2).stem}*",
                                                            path,
                                                            top_path_only=True)
                                for nff_dR2 in num_formatted_objs_dryRun_2]
        
        lcos = len(conflicting_objs)
        
        if lcos > 0:
            
            if obj_type == bo_types[0]:
                report_file_name = "conflicting_files_report"    
            elif obj_type == bo_types[1]:
                report_file_name = "conflicting_directories_report"    
                
            report_file_path = return_report_file_fixedPath(path,
                                                           report_file_name,
                                                           fixed_ext)
            
            rf = open(report_file_path, "w")                    
         
            timestamp_str_fu\
            = get_obj_operation_datetime(objList_uneven,
                                         "modification", 
                                         time_format_str)
            
            timestamp_str_nff_dR2\
            = get_current_time(time_fmt_string=ctime_format_str)
            
            timestamp_str_cf\
            = get_obj_operation_datetime(conflicting_objs,
                                         "modification", 
                                         time_format_str)
            
            for fu, nff_dR2, cf in zip(objList_uneven,
                                       num_formatted_objs_dryRun_2,
                                       conflicting_objs):
            
                rf.write(conf_obj_table.format(fu, timestamp_str_fu,
                                                nff_dR2, timestamp_str_nff_dR2,
                                                cf, timestamp_str_cf))
                         
            rf.close()
                
            if obj_type == bo_types[0]:
                print(f"\n\nSome renamed files conflict! Information is stored "
                      f"at file '{report_file_name}'.")
                
            elif obj_type == bo_types[1]:
                print("\n\nSome renamed directories conflict! "
                      f"Information is stored at file '{report_file_name}'.") 
 
        else:
            
            report_file_name = "dry-run_renaming_report"    
            report_file_path = return_report_file_fixedPath(path,
                                                            report_file_name,
                                                            fixed_ext)
            rf = open(report_file_path, "w")                    
            
            for fu, nff_dR2 in zip(objList_uneven, num_formatted_objs_dryRun_2):
                rf.write(conf_obj_table.format(fu, timestamp_str_fu,
                                                nff_dR2, timestamp_str_nff_dR2))
                         
            rf.close()
                
            if obj_type == bo_types[0]:
                print("No conflicting files found. "
                      "Please check the dry-run renaming information "
                      f"at file '{report_file_name}'.")
                
            elif obj_type == bo_types[1]:
                print("No conflicting directories found. "
                      "Please check the dry-run renaming information "
                      f"at file '{report_file_name}'.")
           
            ansPerformChanges\
            = input("Would you like to perform the changes? [y/n] ")
 
            while (ansPerformChanges != "y" and ansPerformChanges != "n"):   
                ansPerformChanges\
                = input("Please write 'y' for 'yes' or 'n' for 'no' ")
                
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
          
        # Check for equally named conflicting objs #
        #-------------------------------------------#
        
        if obj_type == bo_types[0]:
            conflicting_objs = [find_fileString_paths(f"*{Path(nff_dR).stem}*",
                                                      path,
                                                      top_path_only=True)
                                for nff_dR in num_formatted_objs_dryRun]
        
        elif obj_type == bo_types[1]:
            conflicting_objs = [find_fileString_directories(f"*{Path(nff_dR).stem}*",
                                                            path,
                                                            top_path_only=True)
                                for nff_dR in num_formatted_objs_dryRun]
            
        lcos = len(conflicting_objs)
        
        if lcos > 0:
            
            if obj_type == bo_types[0]:
                report_file_name = "conflicting_files_report"    
            elif obj_type == bo_types[1]:
                report_file_name = "conflicting_directories_report"    
                
            report_file_path = return_report_file_fixedPath(path,
                                                          report_file_name,
                                                          fixed_ext)
            
            rf = open(report_file_path, "w")                    
              
            timestamp_str_fus\
            = get_obj_operation_datetime(objList_uneven_slice,
                                          "modification", 
                                          time_format_str)
            
            timestamp_str_nff_dR\
            = get_current_time(time_fmt_string=ctime_format_str)
            
            timestamp_str_cf\
            = get_obj_operation_datetime(conflicting_objs,
                                          "modification", 
                                          time_format_str)
            
            for fus, nff_dR, cf in zip(objList_uneven_slice,
                                       num_formatted_objs_dryRun,
                                       conflicting_objs):
            
                rf.write(conf_obj_table.format(fus, timestamp_str_fus,
                                                nff_dR, timestamp_str_nff_dR,
                                                cf, timestamp_str_cf))
                         
            rf.close()
                
            print(f"\n\nSome renamed objs conflict! Information is stored "
                  f"at file '{report_file_name}'.")
                
        else:
            
            report_file_name = "dry-run_renaming_report"    
            report_file_path = return_report_file_fixedPath(path,
                                                           report_file_name,
                                                           fixed_ext)
            rf = open(report_file_path, "w")                    
            
            for fus, nff_dr in zip(objList_uneven_slice, 
                                   num_formatted_objs_dryRun):
                rf.write(dry_run_table.format(fus, nff_dR))
                         
            rf.close()
                
            print("No conflicting objs found. "
                  "Please check the dry-run renaming information "
                  f"at file '{report_file_name}'.")
       
            ansPerformChanges\
            = input("Would you like to perform the changes? [y/n] ")
 
            while (ansPerformChanges != "y" and ansPerformChanges != "n"):
                ansPerformChanges\
                = input("Please write 'y' for 'yes' or 'n' for 'no' ")
                
            loop_direct_renamer(objList_uneven_slice, num_formatted_objs_dryRun)
                           

#------------------#
# Local parameters #
#------------------#

# Time formatting strings #
time_format_str = basic_time_format_strs["H"]
ctime_format_str = basic_time_format_strs["CFT"]

# Fixed extension to reuse at different parts of the functions #
fixed_ext = "txt"

# Fixed length of the list containing the conflicting file or directory names #
lcos_upperLimit = 50

# obj comparison tables #
conf_obj_table\
= """{} <--> {} renamed to {} <--> {} conflicts with {} <--> {}\n"""

dry_run_table = """{} renamed to {}\n"""

# Basic object types #
bo_types = basic_object_types
