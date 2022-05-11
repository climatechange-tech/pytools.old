#----------------#
# Import modules #
#----------------#

import importlib
from pathlib import Path

#---------------------------------------#
# Get the all-code containing directory #
#---------------------------------------#

cwd = Path.cwd()
main_path = Path("/".join(cwd.parts[:3])[1:]).glob("*/*")

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


module_imp2 = "file_and_directory_paths.py"
module_imp2_path = f"{fixed_dirpath}/"\
                   f"files_and_directories/{module_imp2}"
                   
spec2 = importlib.util.spec_from_file_location(module_imp2, module_imp2_path)
file_and_directory_paths = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(file_and_directory_paths)


module_imp3 = "file_handler.py"
module_imp3_path = f"{fixed_dirpath}/"\
                   f"files_and_directories/{module_imp3}"
                   
spec3 = importlib.util.spec_from_file_location(module_imp3, module_imp3_path)
file_handler = importlib.util.module_from_spec(spec3)
spec3.loader.exec_module(file_handler)

#----------------------------------------------------#
# Define imported module(s)´ function call shortcuts #
#----------------------------------------------------#

file_path_specs = string_handler.file_path_specs

find_allfile_extensions = file_and_directory_paths.find_allfile_extensions
find_ext_file_paths = file_and_directory_paths.find_ext_file_paths

rename_objects = file_handler.rename_objects

#------------------#
# Define functions #
#------------------#

def reorder_files(nzeros_left,
                  extensions2skip,
                  file_name_splitchar,
                  distinguish_extensions=False):
    
    ext_list = find_allfile_extensions(extensions2skip, top_path_only=True)
    
    if distinguish_extensions:
    
        for ext in ext_list:
            filelist_byext = find_ext_file_paths(ext, cwd, top_path_only=True)
            
            for file in enumerate(filelist_byext):
                
                file_num = file[0]
                file_name = file[-1]
                            
                file_path_noname, file_path_name, file_path_name_split, file_path_ext\
                = file_path_specs(file_name, file_name_splitchar)
        
                num_format = f"{file_num+1:0{nzeros_left+1}d}"
                num_formatted_file = f"{str(file_path_noname)}/{num_format}.{file_path_ext}" 
                rename_objects(file_name, num_formatted_file)
                
    else:
        filelist = find_ext_file_paths(ext_list, cwd, top_path_only=True)
        
        for file in enumerate(filelist):
            
            file_num = file[0]
            file_name = file[-1]
                        
            file_path_noname, file_path_name, file_path_name_split, file_path_ext\
            = file_path_specs(file_name, file_name_splitchar)
    
            num_format = f"{file_num+1:0{nzeros_left+1}d}"
            num_formatted_file = f"{str(file_path_noname)}/{num_format}.{file_path_ext}" 
            rename_objects(file_name, num_formatted_file)

