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

# Import module that finds python tools' path #
home_PATH = Path.home()
sys.path.append(str(home_PATH))

import get_pytools_path
fixed_dirpath = get_pytools_path.return_custom_path()

# Enumerate custom modules and their paths #
#------------------------------------------#

custom_mod_path1 = f"{fixed_dirpath}/arrays_and_lists"
custom_mod_path2 = f"{fixed_dirpath}/files_and_directories"
custom_mod_path3 = f"{fixed_dirpath}/strings"
                                        
# Add the module paths to the path variable #
#-------------------------------------------#

sys.path.append(custom_mod_path1)
sys.path.append(custom_mod_path2)
sys.path.append(custom_mod_path3)

# Perform the module importations #
#---------------------------------#

import array_handler
import file_and_directory_handler
import file_and_directory_paths
import string_handler

#--------------------------------------------------#
# Define imported modules' function call shortcuts #
#--------------------------------------------------#

basicObjectValueTypeConverter = array_handler.basicObjectValueTypeConverter
select_array_elements = array_handler.select_array_elements
remove_elements_from_array = array_handler.remove_elements_from_array

fileList2String = string_handler.fileList2String
find_substring_index = string_handler.find_substring_index

find_fileString_paths = file_and_directory_paths.find_fileString_paths

copy_files = file_and_directory_handler.copy_files
remove_files_byFS = file_and_directory_handler.remove_files_byFS
rename_objects = file_and_directory_handler.rename_objects

#----------------------#
# Parametroak definitu #
#----------------------#

docPath = Path(fixed_dirpath).parent
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

fileListOrig = [
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

fileListRename = [
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
fileListCWD = os.listdir()

# Zerrendatik programa batzuk ezabatu #
delFileObj = find_substring_index(fileListCWD, kw_del_list)

if isinstance(delFileObj, dict):
    delFileIdx = [key 
                  for key in delFileObj.keys()
                  if len(delFileObj[key]) > 0]
    
elif isinstance(delFileObj, list):
    delFileIdx = delFileObj.copy()
    
else:
    delFileIdx = delFileObj


files2delete = remove_elements_from_array(fileListCWD, delFileIdx)
files2delete = list(basicObjectValueTypeConverter(files2delete, 'U', 'O'))

# Ezabatu zerrenda erresultantean ageri diren artxiboak #

remove_files_byFS(files2delete, ".")

# Bilatu euskaraz izendatutako artxiboak #
#----------------------------------------#

print("Jatorrizko programak bilatzen...")
pathListOrig = find_fileString_paths(fileListOrig, docPath)

# Kopiatu bilatutako artxiboak direktorio hona #
#----------------------------------------------#

print("Bilatutako programak direktorio honetara bertara kopiatzen...")

copy_files(pathListOrig, ".")

# Kopiatutako artxiboak berrizendatu #
#------------------------------------#

print("Kopiatutako programak berrizendatzen...")

rename_objects(fileListOrig, fileListRename)

# Berrizendatutako artxiboak karpeta konprimatu batean gorde #
#------------------------------------------------------------#

if compress_copied_and_renamed_files:
    
    print("Berrizendatutako programak karpeta konprimatu batean gordetzen...")
    time.sleep(0.5)
    
    outputZipFile = f"Jon_Ander_Gabantxo.{exts[-1]}"
    
    fileListRenameStr = fileList2String(fileListRename)
    files2ExcludeFromZipping\
    = fileList2String(select_array_elements(fileListCWD, delFileIdx))
    
    zip_command = f"zip {outputZipFile} {fileListRenameStr} -x {files2ExcludeFromZipping}"
    os.system(zip_command)
