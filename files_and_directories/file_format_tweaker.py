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
fixed_dirpath = get_pytools_path.return_custom_path()

# Enumerate custom modules and their paths #
#------------------------------------------#

custom_mod1_path = f"{fixed_dirpath}/files_and_directories" 
custom_mod2_path = f"{fixed_dirpath}/strings"
                  
# Add the module paths to the path variable #
#-------------------------------------------#

sys.path.append(custom_mod1_path)
sys.path.append(custom_mod2_path)

# Perform the module importations #
#---------------------------------#

import file_and_directory_handler
import file_and_directory_paths
import string_handler

#----------------------------------------------------#
# Define imported module(s)´ function call shortcuts #
#----------------------------------------------------#

remove_files_byExts = file_and_directory_handler.remove_files_byExts

get_obj_specs = string_handler.get_obj_specs
obj_path_specs = string_handler.obj_path_specs
find_substring_index = string_handler.find_substring_index
modify_obj_specs = string_handler.modify_obj_specs

find_ext_file_paths = file_and_directory_paths.find_ext_file_paths
find_fileString_paths = file_and_directory_paths.find_fileString_paths

#------------------#
# Define functions #
#------------------#

def aux_path_strAdd(path2tweak, str2add):
    
    obj2change = "name_noext"
    output_path_aux = modify_obj_specs(path2tweak, 
                                       obj2change,
                                       str2add=str2add)
    return output_path_aux


def aux_ext_adder(path2tweak, extension):
    
    obj2change = "ext"
    obj_spec_key = obj2change
    
    path_ext = get_obj_specs(path2tweak, obj_spec_key)
    
    if len(path_ext) == 0:
        output_path = modify_obj_specs(path2tweak,
                                       obj2change,
                                       new_obj=extensions)
        
    else:
        output_path = path2tweak
    
    return output_path


def tweak_pages(file, cat_str, output_path="default"):
    
    default_arg = tweak_pages.__defaults__[0]
    
    if output_path == default_arg:
        str2add_1 = f"_{cat_str}"
        output_path_aux_1 = aux_path_strAdd(output_path, str2add_1)
        
        if len(output_path_aux_1) > 60:
            str2add_2 = "_lotsOfPagesTweaked"
            output_path_aux_2 = aux_path_strAdd(output_path, str2add_2)
            output_path = output_path_aux_2
            
        else:
            output_path = output_path_aux_1
       
    zsh_pdftk_command = f"{essential_program_list[1]} '{file}' cat {cat_str} "\
                        f"output '{output_path}'"
                        
    os.system(zsh_pdftk_command)


def pdf_file_tweaker(path, cat_out_obj):
    
    """
    Function that allows to select a single page, or range(s) of pages
    to conserve in a PDF file, the same way as it is done
    when printing a document.
    
    For that it uses pdftk tool, together with 'cat' and the
    os.system shell emulator attribute.
    
    For the sake of gathering simplicity and practicity,
    the structure of the default output file name will be the following:
    '{path_without_the_extension}_{page_configuration}.{extension}'
    
    Although in many cases an only interval page is selected from a file,
    and the output file name is renamed to the original,
    it has been considered, due to the range of varieties that
    this function offers, the best option to be the previously described one.
    
    Parameters
    ----------
    path : str or PosixPath or list of str or PosixPath
          String or list of strings that identify the file(s) to work with,
          included pathlib.Path module's PosixPaths.
    cat_out_obj : str, dict or list of dict
          Object that provides the output file name(s)
          together with the strings that assemble or catenate pages.
      
    
    This function distinguishes among these three cases:
    
      1. Both the path and cat string are single strings
      --------------------------------------------------
    
      In this case, from a single input file is created
      a sole output page.
      Then in order to distinguish
      between the path (WITH or WITHOUT THE EXTENSION) and 
      the string to assemble or catenate pages,
      the following structure is used:
      f"{cat_string}; {output_path}"
      
      The semicolon is absolutely necessary, because the function
      is designed to split the string is splitted
      according to that character. 
      The space around the semicolon is not necessary and
      serves only as a description.
    
      2. The path is a string, and the catenation object is a dictionary
      ------------------------------------------------------------------
    
      Then it is understood that several files are going to be created
      from a single input file.
    
      The dictionary has to be structured like the following:
    
      input_path --> type string --> it corresponds this object:
      {output_path_1 : cat_str_1,
        output_path_2 : cat_str_2,
                    (...)        ,
        output_path_n : cat_str_n}
    
      3. Both the path and catenation object are lists
      ------------------------------------------------
    
      This is the most complete case, in which each file
      is splitted into several files.
      There must be a catenation object per input path,
      so the structure of the case is as follows:
    
      input_path_1 --> type string --> it corresponds this object:
      {output_path_1 : cat_str_1,
        output_path_2 : cat_str_2,
                    (...)        ,
        output_path_n : cat_str_n}
    
      [...]
    
      input_path_n --> type string --> it corresponds this object:
      {output_path_n+1 : cat_str_n+1,
        output_path_n+2 : cat_str_n+2,
                      (...)          ,
        output_path_n+m : cat_str_n+m}
    
    Note
    ----
    In any case, this function includes an option to
    mark the output path as 'default', that it to say,
    output_path == "default".
    
    In such case, the catenation string will be ussed
    as an appendix to the original path, 
    i.e. f"{original_path}_{catenation_string}.{extension}"
    
    However, there might be occasions in which that string is too long
    (more than 60 characters), so when this happens the string to add
    will be simply 'lotsOfPagesTweaked' and the output path will be
    f"{original_path_name_noext}_lotsOfPagesTweaked.{extension}"
    
    If any other than the default is given -as said, with or without
    the extension, irrespective of the case- , to the output path 
    the 'pdf' extension will be added if necessary. 
    Recall that the latter refers to the output path(s).
    
    Also for the sake of gathering simplicity and practicity,
    this function is designed to work with absolute paths,
    in order to have a unique function placed in a module with a fixed path.
    """
    
    arg_names = pdf_file_tweaker.__code__.co_varnames
    
    if isinstance(path, str) and isinstance(cat_out_obj, str):
        
        if cat_out_splitchar not in cat_out_obj:
            raise SyntaxError(syntax_error_string)
            
        cat_str = cat_out_obj.split(cat_out_splitchar)[0]
        output_path_aux = cat_out_obj.split(cat_out_splitchar)[1]
        
        output_path = aux_ext_adder(output_path_aux, extensions[0])        
        tweak_pages(path, cat_str, output_path)
        
        
    elif isinstance(path, str) and isinstance(cat_out_obj, dict):      
        output_pathlist = list(cat_out_obj.keys())
        cat_str_list = list(cat_out_obj.values())
        
        for output_path_aux, cat_str in zip(output_pathlist, cat_str_list):
            output_path = aux_ext_adder(output_path_aux, extensions[0])
            tweak_pages(path, cat_str, output_path)
        
    elif isinstance(path, list) and isinstance(cat_out_obj, list):
              
        for p in path:          
            output_pathlist = list(cat_out_obj.keys())
            cat_str_list = list(cat_out_obj.values())
            
            for output_path_aux, cat_str in zip(output_pathlist, cat_str_list):
                output_path = aux_ext_adder(output_path_aux, extensions[0])
                tweak_pages(p, cat_str, output_path)            
        
    else:
        raise TypeError(type_error_string_complete.format(arg_names[0], 
                                                          arg_names[1]))
        
        
def pdf_file_compressor(in_path, out_path=None):
    
    """
    Function that compresses pdf files with an imperceptible loss of quality.
    For that it uses the 'ps2pdf' tool, 
    together with os.system shell emulator attribute.
    
    Parameters
    ----------
    in_path : str or PosixPath or list of str or PosixPath.
          String or list of strings that identify the file(s) to work with,
          included pathlib.Path module's PosixPaths.
    out_path : str or PosixPath or list of str or PosixPath.
          Object that provides the output file name(s).
    
    This function distinguishes between these two cases:
    
      1. Both the input and output paths are single strings
          In this case, a single file is compressed and then 
          renamed to the custom name.
    
      2. Both the input and output paths are lists
          It is understood that, for each index, the corresponding input file 
          has to be renamed to the corresponding output file,
          after the compression.
    
    Note
    ----
    This function incorportates a default behaviour
    in which adds the string '_compressed' 
    to the extensionless part of the name.
    
    For the sake of simplicity, unlike in 'pdf_file_tweaker' because
    it is more complex, the function is designed to invoke such funcionality
    by setting the output path to None.
    
    If any other than the default is given to the output path,
    the 'pdf' extension will be added if necessary. 
    Recall that the latter refers to the output path(s).
    
    Also for the sake thereof, this function is designed to work
    with absolute paths in order to have a unique function 
    placed in a module with a fixed path.
    """
    
    arg_names = pdf_file_compressor.__code__.co_varnames
          
    if not (isinstance(in_path, str) and isinstance(out_path, str)\
        or (isinstance(in_path, list)) and isinstance(out_path, list)):
        
        raise TypeError(type_error_string_complete.format(arg_names[0], 
                                                          arg_names[1]))
        
    else:
        if isinstance(in_path, str):
            in_path = [in_path]
            
        if isinstance(out_path, str):
            out_path = [out_path]
    
    for ip, op_aux in zip(in_path, out_path):
    
        if op_aux is None:
            str2add = "compressed"
            op_aux = aux_path_strAdd(ip, str2add)
            
        op = aux_ext_adder(op_aux, extensions[0])
    
        ps2pdf_command\
        = f"{essential_program_list[0]} -dPDFSETTINGS=/ebook {ip} {op}"
    
        os.system(ps2pdf_command)
    
  
def checkEssentialProgInstallStatus():
    
    keyword_list = ["none", "ninguno"]
    
    # This function checks whether at least one of the programs is installed,
    # only to be used by functions 'eml2pdf' and 'msg2pdf'.
    # If so, it returns True, otherwise returns False.
    
    for kw, ess_prog in zip(keyword_list, essential_program_list):
        progInstalledStatusString = os.popen(f"apt-cache policy {ess_prog}").read()
        kw_idx = find_substring_index(progInstalledStatusString, 
                                      kw, 
                                      advanced_search=True,
                                      find_whole_words=True)
        
        if kw_idx == -1:
            raise ModuleNotFoundError(mnfe_string.format(ess_prog))
            
    else:
        print(f"{ess_prog} program installed, continuing.")


def eml2pdf(path_to_walk_in, delete_eml_files=False):
    
    """
    Tool to convert email messages (.msg extension) to PDF files.
    
    The main conversion is done by parsing (and cleaning)
    the mime/structure, converting it to html and then using
    wkhtmltopdf to convert the generated html to a pdf file.
    In linux, 'wkhtmltopdf' program is needed
    in order to perform the latter task.
    
    Parameters
    ----------
    path_to_walk_in : str or PosixPath
          Input path to search for 'eml' files.
    delete_eml_files : bool
          Option to control whether to delete eml extension files.
          It has been incorporated to prevent file deletion if
          the conversion fails, or because the user wants to keep those files.
          Defaults to False to prevent accidental loss.
    """
    
    extension = extensions[1]
    eml_files = find_ext_file_paths(extension,
                                    path_to_walk_in,
                                    top_path_only=True)
   
    str2find = f"*emailconverter*.{extensions[-1]}"    
    converter_tool_path = find_fileString_paths(str2find, alldoc_dirpath)

    # Convert each email to PDF #        
    for emlf in eml_files:
        eml2pdf_command = f"java -jar {converter_tool_path} '{emlf}'"
        os.system(eml2pdf_command)
        
    if delete_eml_files:
        # Delete every email file #
        remove_files_byExts(extension, path_to_walk_in)

            
def msg2pdf(path_to_walk_in,
            delete_msg_files=False,
            delete_eml_files=False):
    
    """
    Tool to convert Microsoft Outlook messages (.msg extension)
    to PDF files or email messages (.eml extension) to PDF.
    
    It firstly it uses the 'msgconvert' tool to convert
    msg files into email files.
    Then the main conversion is done by parsing (and cleaning)
    the mime/structure, converting it to html and then using
    wkhtmltopdf to convert the generated html to a pdf file.
    This is performed by calling the already defined 'eml2pdf' function.
    
    In linux, 'wkhtmltopdf' program is needed
    in order to perform the latter task.
    
    Parameters
    ----------
    path_to_walk_in : str or PosixPath
          Input path to search for 'msg' files.
    delete_msg_files : bool
          Option to control whether to delete msg extension files.
          It has been incorporated to prevent file deletion if
          the conversion fails, or because the user wants to keep those files.
          Defaults to False to prevent accidental loss.
    
    delete_eml_files : bool
          Same task as the previous parameter
          but affecting only to eml files.
          Defaults to False to prevent accidental loss.
    """
    
    extension = extensions[2]
    msg_files = find_ext_file_paths(extension,
                                    path_to_walk_in,
                                    top_path_only=True)
    
    # Convert microsoft outlook message (.msg) to email (.eml) #
    for msgf in msg_files:
        msg2eml_command = f"{essential_program_list[3]} '{msgf}'"
        os.system(msg2eml_command)
        
    # Convert email to PDF #
    eml2pdf(path_to_walk_in, delete_eml_files=delete_eml_files)
        
    if delete_msg_files:
        # Delete every email file #
        remove_files_byExts(extension, path_to_walk_in)
        
#------------------#
# Local operations #
#------------------#

# Check whether essential programs are installed #
checkEssentialProgInstallStatus()

#------------------#
# Local parameters # 
#------------------#

# Documents directory #
alldoc_dirpath = Path(fixed_dirpath).parent

extensions = ["pdf", "eml", "msg", "jar"]
cat_out_splitchar = ";"

syntax_error_string = """
Please write a semicolon (';') to separate
the page cat string from the output path, 
i.e. "{cat_str}; {output_path}"'
"""

type_error_string_basic = """
'{}' and '{}' must match one of these cases:\n                
type(in_path) == str and type(out_path) == str\n
type(in_path) == list and type(out_path) == list\n
"""

type_error_string_complete = """
'{}' and '{}' must match one of these cases:\n                
type(path) == str and type(cat_out_obj) == str\n
type(path) == str and type(cat_out_obj) == dict\n
type(path) == list and type(cat_out_obj) == list\n
"""

mnfe_string = """
'{}' is not installed,\nwhich is 
required to perform the msg-to-pdf conversion.\n
Install it by typing:\n\n
sudo apt install {}
"""

essential_program_list = ["ps2pdf", "pdftk", "wkhtmltopdf", "msgconvert"]
