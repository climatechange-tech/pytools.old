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

# All-document containing directory #
alldoc_dirpath = Path(fixed_dirpath).parent

#-----------------------#
# Import custom modules #
#-----------------------#

module_imp1 = "file_handler.py"
module_imp1_path = f"{fixed_dirpath}/"\
                   f"files_and_directories/{module_imp1}"

spec1 = importlib.util.spec_from_file_location(module_imp1, module_imp1_path)
file_handler = importlib.util.module_from_spec(spec1)
spec1.loader.exec_module(file_handler)


module_imp2 = "string_handler.py"
module_imp2_path = f"{fixed_dirpath}/"\
                   f"strings/{module_imp2}"

spec = importlib.util.spec_from_file_location(module_imp2, module_imp2_path)
string_handler = importlib.util.module_from_spec(spec)
spec.loader.exec_module(string_handler)


module_imp3 = "file_and_directory_paths.py"
module_imp3_path = f"{fixed_dirpath}/"\
                   f"files_and_directories/{module_imp3}"
                   
spec3 = importlib.util.spec_from_file_location(module_imp3, module_imp3_path)
file_and_directory_paths = importlib.util.module_from_spec(spec3)
spec3.loader.exec_module(file_and_directory_paths)

#----------------------------------------------------#
# Define imported module(s)´ function call shortcuts #
#----------------------------------------------------#

remove_files_byExts = file_handler.remove_files_byExts

file_path_specs = string_handler.file_path_specs
noneInString_filter = string_handler.noneInString_filter

find_ext_file_paths = file_and_directory_paths.find_ext_file_paths

#------------------#
# Define functions #
#------------------#

def return_cut_temp_file_name(file, splitchar, page_range_string):
    
        
    file_path_noname, file_path_name, file_path_name_split, file_path_ext\
    = file_path_specs(file, splitchar)
    
    cut_file_name_temp\
    = f"{file_path_noname}/{file_path_name}_{page_range_string}.{file_path_ext}"
    cfnt_noneFiltered = noneInString_filter(cut_file_name_temp)
    
    return cfnt_noneFiltered


def cut_pages(file, splitchar, page_range_string):
    
    cut_file_name_temp = return_cut_temp_file_name(file, splitchar,
                                                   page_range_string)
   
    zsh_pdftk_command = f"pdftk '{file}' cat {page_range_string} "\
                        f"output '{cut_file_name_temp}'"
                        
    os.system(zsh_pdftk_command)


def select_pages_from_pdf_file(files,
                               page_strings,
                               cut_recursively=False):

    # Function that allows to select a single page, or range(s) of pages
    # to conserve in a PDF file, the same way as it is done
    # when printing a document.
    # 
    # For that it uses pdftk tool, together with 'cat' and the
    # os.system shell emulator attribute.
    # 
    # For the sake of gathering simplicity and practicity,
    # the structure of the default output file name will be the following:
    # '{part_without_the_extension}_{page(s)}.{extension}'
    # 
    # Although in many cases an only interval page is selected from a file,
    # and the output file name is renamed to the original,
    # it has been considered, due to the range of varieties that
    # this function offers, the best option to be the previously described one
    # 
    # Parameters
    # ----------
    # files : str or list
    #       String or list of strings that identify the file(s) to work with.
    # page_strings : str or list
    #       String or list of strings that emulate
    #       individual or interval(s) of page(s) to be selected.
    # cut_recursively : bool
    #       Determines whether for a file corresponds a single or multiple
    #       page(s) or page intervals.
    # 
    # This function distinguishes four cases:
    # 
    #   1. Both file names and page strings are lists.
    #       1.1 cut_recursively=True
    #           Then it is understood that to each file
    #           multiple page strings correspond and that file is
    #           cut into all those page intervals.
    #       1.1 cut_recursively=False
    #           Then to each file corresponds a single page interval,
    #           and that file is cut accordingly.
    #   2. The file names are contained in a list but there is
    #      a single page string.
    #           Then each file will be cut for the input interval,
    #           irrespective of the cut_recursively boolean.
    #   3. The file name is a string and page strings are contained in a list.
    #           Then that individual file will be cut
    #           into the selected page intervals.
    #   4. None of them are lists.
    #           Then the input file will simply be cut accordingly.
    # 
    # Note
    # ----
    # This function is designed to operate with simple file names,
    # i.e neither with relative nor absolute paths.
        
    file_name_splitchar = "."
    
    if\
    isinstance(files, list)\
    and isinstance(page_strings, list)\
    and cut_recursively:
        
        for file in files:
            for pgs in page_strings:
                cut_pages(file, file_name_splitchar, pgs)
                
    elif\
    isinstance(files, list)\
    and isinstance(page_strings, list)\
    and not cut_recursively: 
        
        lfs = len(files)
        lpgs = len(page_strings)
        
        if lfs == lpgs:
            for file, pgs in zip(files, page_strings):
                cut_pages(file, file_name_splitchar, pgs)   
        
        else:
            raise ValueError("File and page range(s) lists "
                             "have to be of the same length.")

    elif\
    isinstance(files, list)\
    and not isinstance(page_strings, list)\
    and cut_recursively or not cut_recursively:   
        
        for file in files:
            cut_pages(file, file_name_splitchar, page_strings)
            
    elif\
    not isinstance(files, list)\
    and not isinstance(page_strings, list)\
    and cut_recursively or not cut_recursively:   
    
        cut_pages(file, file_name_splitchar, page_strings)
        

def check_wkhtmltopdf_installed():
    
    # This function checks whether the program wkhtmltopdf is installed,
    # only to be used by functions 'eml2pdf' and 'msg2pdf'.
    # 
    # It returns True if so, otherwise returns False
        
    program = "wkhtmltopdf"
    wkhtinstalled = os.popen(f"apt-cache policy {program}").read()
    
    if "ninguno" in wkhtinstalled or "none" in wkhtinstalled:
        raise ModuleNotFoundError(f"{program} is not installed,\nwhich is "
                                  "required to perform the msg to pdf conversion.\n"
                                  "Install it by typing:\n\n"
                                  f"sudo apt install {program}")


def eml2pdf(delete_eml_files):
    
    # Tool to convert email messages (.msg extension) to PDF files.
    # 
    # The main conversion is done by parsing (and cleaning)
    # the mime/structure, converting it to html and then using
    # wkhtmltopdf to convert the generated html to a pdf file.
    # In linux, 'wkhtmltopdf' program is needed
    # in order to perform the latter task.
    # 
    # Parameters
    # ----------
    # delete_eml_files : bool
    #       Option to control whether to delete eml extension files.
    #       It has been incorporated to prevent file deletion if
    #       the conversion fails, or because the user wants to keep those files.
    # 
    # Note
    # ----
    # This function is designed to operate with simple file names,
    # i.e neither with relative nor absolute paths.
    
    # Check that program 'wkhtmltopdf' is installed #
    check_wkhtmltopdf_installed()
    
    extension = "eml"
    
    # Convert email to PDF #        
    eml_files = find_ext_file_paths(extension, None, top_path_only=True)
   
    converter_tool_path\
    = f"{alldoc_dirpath}/../email-to-pdf-converter/emailconverter-2.5.3-all.jar"

    for emlf in eml_files:
        eml2pdf_command = f"java -jar {converter_tool_path} '{emlf}'"
        os.system(eml2pdf_command)
        
    if delete_eml_files:
        # Delete every email file #
        remove_files_byExts(extension, cwd)

            
def msg2pdf(delete_msg_files, delete_eml_files):
    
    # Tool to convert Microsoft Outlook messages (.msg extension)
    # to PDF files or email messages (.eml extension) to PDF.
    # 
    # It firstly it uses the 'msgconvert' tool to convert
    # msg files into email files.
    # Then the main conversion is done by parsing (and cleaning)
    # the mime/structure, converting it to html and then using
    # wkhtmltopdf to convert the generated html to a pdf file.
    # 
    # In linux, 'wkhtmltopdf' program is needed
    # in order to perform the latter task.
    # 
    # Parameters
    # ----------
    # delete_msg_files : bool
    #       Option to control whether to delete msg extension files.
    #       It has been incorporated to prevent file deletion if
    #       the conversion fails, or because the user wants to keep those files.
    # 
    # delete_eml_files : bool
    #       Same task as the previous parameter
    #       but affecting only to eml files.
    # 
    # Note
    # ----
    # This function is designed to operate with simple file names,
    # i.e neither with relative nor absolute paths.
    
    # Check whether 'wkhtmltopdf' program is installed #
    check_wkhtmltopdf_installed()
    
    extension = "msg"
            
    msg_files = find_ext_file_paths(extension, None, top_path_only=True)
    
    # Convert microsoft outlook message (.msg) to email (.eml) #
    for msgf in msg_files:
        msg2eml_command = f"msgconvert '{msgf}'"
        os.system(msg2eml_command)
        
    # Convert email to PDF #
    eml2pdf(delete_eml_files)
        
    if delete_msg_files:
        # Delete every email file #
        remove_files_byExts(extension, cwd)
