#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 11:11:21 2023

@author: jonander

**Deskribapena**
Artxibo batzuk haiei dagokien direktoriotik hona kopiatu ondoren
karpeta konprimatu batean gordetzeko programa.
"""

#----------------#
# Import modules #
#----------------#

import os
from pathlib import Path
import sys
import time

#-----------------------#
# Import custom modules #
#-----------------------#

# Find the path of the Python toolbox #
home_PATH = Path.home()
sys.path.append(str(home_PATH))

import get_pytools_path
fixed_dirpath = get_pytools_path.return_custom_path()

# Enumerate custom modules and their paths #
#------------------------------------------#

custom_mod_path1 = f"{fixed_dirpath}/arrays_and_lists"
custom_mod_path2 = f"{fixed_dirpath}/files_and_directories"
custom_mod_path3 = f"{fixed_dirpath}/strings"
                                        
# Add the paths to the 'path' attribute of module 'sys' #
#-------------------------------------------------------#

sys.path.append(custom_mod_path1)
sys.path.append(custom_mod_path2)
sys.path.append(custom_mod_path3)

# Perform whole or partial module importations #
#----------------------------------------------#

import array_handler
import file_and_directory_handler
import file_and_directory_paths
import string_handler

#--------------------------------------------------#
# Define imported modules' function call shortcuts #
#--------------------------------------------------#

basic_value_data_type_converter = array_handler.basicObjectValueTypeConverter
select_array_elements = array_handler.select_array_elements
remove_elements_from_array = array_handler.remove_elements_from_array

file_list_to_str = string_handler.file_list_to_str
find_substring_index = string_handler.find_substring_index

find_files_by_globstr = file_and_directory_paths.find_files_by_globstr

copy_files = file_and_directory_handler.copy_files
remove_files_by_globstr = file_and_directory_handler.remove_files_by_globstr
rename_objects = file_and_directory_handler.rename_objects

#----------------------#
# Parametroak definitu #
#----------------------#

docpath = Path(fixed_dirpath).parent
exts = ["jpg", "pdf", "zip"]
keyWord = "kopiatu"

kw_del_list = ["kopiatu", "RDT"]

#---------------------#
# Kontrol-etengailuak #
#---------------------#

compress_copied_and_renamed_files = True

#--------------------------#
# Zehaztu artxiboen izenak #
#--------------------------#

# Jatorrizko izenak #
#-------------------#

file_list_orig = [
    f"2023_garbiago.{exts[0]}",
    f"Jon_Ander_Gabantxo_betea.{exts[1]}",
    f"NAN_aurrealdea.{exts[0]}",
    f"NAN_atzealdea.{exts[0]}",
    f"aurrealdea.{exts[0]}",
    f"atzealdea.{exts[0]}",
    f"lan-bizitza_2023-10-20.{exts[1]}",
    f"meteorologia-ikastaroa.{exts[1]}",
    f"Aula_Carpe_Diem-MySQL_PHP.{exts[1]}",
    f"EGA.{exts[1]}",
    f"titulu_ofiziala.{exts[1]}",
    f"HEO-ingelesa_C1.{exts[1]}",
    f"titulo_oficial.{exts[1]}"
]

# Berrizendaketak (hizkuntza edo testua soilik) #
#-----------------------------------------------#

file_list_2rename = [
    f"2023.{exts[0]}",
    f"CV_betea.{exts[1]}",
    f"NAN_aurrealdea.{exts[0]}",
    f"NAN_atzealdea.{exts[0]}",
    f"gida-baimena_aurrealdea.{exts[1]}",
    f"gida-baimena_atzealdea.{exts[1]}",
    f"lan-bizitza_2023-10-20.{exts[1]}",
    f"meteorologia-ikastaroa_ziurtagiria.{exts[1]}",
    f"MySQL-PHP_ziurtagiria.{exts[0]}",
    f"EGA-titulu_ofiziala.{exts[1]}",
    f"fisikako_gradua-titulu_ofiziala.{exts[1]}",
    f"ingelesa_C1-titulu_ofiziala.{exts[1]}",
    f"master_meteorologia_titulo_oficial.{exts[1]}"
]

# Ezabatu direktorio honetako fitxategi guztiak, batzuk izan ezik #
#-----------------------------------------------------------------#

print("Direktorio honetako fitxategiak batzuk izan ezik ezabatzen...")

# Artxiboak zerrendatu #
file_list_cwd = os.listdir()

# Zerrendatik programa batzuk ezabatu #
delFileObj = find_substring_index(file_list_cwd, kw_del_list)

if isinstance(delFileObj, dict):
    del_file_idx = [key 
                  for key in delFileObj
                  if len(delFileObj[key]) > 0]
    
elif isinstance(delFileObj, list):
    del_file_idx = delFileObj.copy()
    
else:
    del_file_idx = delFileObj


files2delete = remove_elements_from_array(file_list_cwd, del_file_idx)
files2delete = list(basic_value_data_type_converter(files2delete, 'U', 'O'))

# Ezabatu zerrenda erresultantean ageri diren artxiboak #

remove_files_by_globstr(files2delete, ".")

# Bilatu euskaraz izendatutako artxiboak #
#----------------------------------------#

print("Jatorrizko programak bilatzen...")
path_list_orig = find_files_by_globstr(file_list_orig, docpath)

# Kopiatu bilatutako artxiboak direktorio hona #
#----------------------------------------------#

print("Bilatutako programak direktorio honetara bertara kopiatzen...")

copy_files(path_list_orig, ".")

# Kopiatutako artxiboak berrizendatu #
#------------------------------------#

print("Kopiatutako programak berrizendatzen...")

rename_objects(file_list_orig, file_list_2rename)

# Berrizendatutako artxiboak karpeta konprimatu batean gorde #
#------------------------------------------------------------#

if compress_copied_and_renamed_files:
    
    print("Berrizendatutako programak karpeta konprimatu batean gordetzen...")
    time.sleep(0.5)
    
    output_zip_file = f"Jon_Ander_Gabantxo.{exts[-1]}"
    
    file_list_2rename_str = file_list_to_str(file_list_2rename)
    files_excluded_from_zipping\
    = file_list_to_str(select_array_elements(file_list_cwd, del_file_idx))
    
    zip_command = f"zip {output_zip_file} {file_list_2rename_str} -x {files_excluded_from_zipping}"
    os.system(zip_command)
