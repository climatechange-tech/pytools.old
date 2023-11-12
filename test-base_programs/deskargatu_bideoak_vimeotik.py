# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Sun Oct 22 13:11:48 2023

@author: jonander
"""


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
fixed_path = get_pytools_path.return_custom_path()

# Enumerate custom modules and their paths #
#------------------------------------------#

custom_mod1_path = f"{fixed_path}/files_and_directories"
custom_mod2_path = f"{fixed_path}/pandas_data_frames"
custom_mod3_path = f"{fixed_path}/operative_systems"
custom_mod4_path = f"{fixed_path}/strings"
                                        
# Add the module path to the path variable #
#------------------------------------------#

sys.path.append(custom_mod1_path)
sys.path.append(custom_mod2_path)
sys.path.append(custom_mod3_path)
sys.path.append(custom_mod4_path)

# Perform the module importations #
#---------------------------------#

import data_frame_handler
import file_and_directory_handler
import file_and_directory_paths
import os_operations
import string_handler

#----------------------------------------------------#
# Define imported module(s)´ function call shortcuts #
#----------------------------------------------------#

read_table = data_frame_handler.read_table

find_allDirectories = file_and_directory_paths.find_allDirectories
remove_files_byFS = file_and_directory_handler.remove_files_byFS

exec_shell_command = os_operations.exec_shell_command
find_substring_index = string_handler.find_substring_index

#------------------#
# Input parameters #
#------------------#

# File extensions #
#-----------------#

extensions = ["txt", "mp4"]

# Directories in current path #
#-----------------------------#

# Get current path #
curpath = os.path.dirname(os.path.abspath(__file__))
os.chdir(curpath)

# Target directories #
targetDirList = ["adarreko_bideoak", "bideoklaseak"]
targetPathList = [f"{curpath}/{target_dir}"
                  for target_dir in targetDirList]

# Get directories inside target (primary) ones #
curPathDirArr = [find_allDirectories(target_path)
                 for target_path in targetPathList]

# yt-dlp program syntaxes #
#-------------------------#

# General syntax #
yt_dlp_flist = """yt-dlp -F {} > {}"""
yt_dlp_download = """yt-dlp -f {} {} --sleep-interval {} -o {}"""

downloads_sleep_secs = 100

# Generic yt-dlp output catching file name #
default_fn = f"url_format_table.{extensions[0]}"

# Pandas data frame parameters #
#------------------------------#

keyword = "unknown"

# Characteristics of the videos to download #
#-------------------------------------------#

# Troncal videos #
#-#-#-#-#-#-#-#-#-
 
# Name list #
troncalVidNameListArr = [
    ["Colaboratory_Google"],
    ["Configuracion_de_entornos"],
    ["Funciones_ampliadas_del_tipo_STRING"],
    ["Rendimiento_y_optimizacion_en_la_ejecucion_de_los_bucles"],
    ["Scrapping_web_dinamico"],
    ["Generacion_de_ficheros_a_traves_de_Scrapping_desde_web"],
    ["Configuracion_del_servidor_de_bases_de_datos"]
]

# URL lists (each primary list by target directory) #
troncalVidURLListArr = [
    ["https://vimeo.com/571137543/2e5412dd14"],
    ["https://vimeo.com/571137725/b835bf1e80"],
    ["https://vimeo.com/571138058/428c4e1b49"],
    ["https://vimeo.com/571136153/0e6d64b7e2"],
    ["https://vimeo.com/571136282/8f3d3238b8"],
    ["https://vimeo.com/571136995/729dcf095d"],
    ["https://vimeo.com/571137275/d1722b3ac4"]
]

ltrvula = len(troncalVidURLListArr)

# Videoclasses #
#-#-#-#-#-#-#-#-

# Name list #
vidclassNameListArr = [
    ["Por_que_estudiar_Python",
     "Primeros_pasos_con_Python",
     "Crear_variables_y_trabajar_con_ellas"],
    ["Como_crear_equipos_DevOps"],
    ["Tipos_de_datos_tuplas_vs_listas",
     "Tipos_de_datos_diccionarios",
     "Operaciones_con_booleanos",
     "Listas_en_Python",
     "Metodos_string",
     "Tuplas",
     "Diccionarios"],
    ["Estructura_y_Elementos_I_Como_Programar_en_Python",
     "Estructura_y_elementos_II_Como_programar_en_Python",
     "Flujos_de_control_condicionales",
     "Flujos_de_control_iteratividad",
     "Aumentamos_nivel_recursividad",
     "Instrucciones_de_Break-Continue",
     "Control_y_manejo_de_excepciones"],
    ["Python_Orientado_a_Objetos",
     "Creacion_de_objetos_en_Python",
     "Concepto_de_polimorfismo",
     "Concepto_de_herencia_y_herencia_multiple",
     "Modulos_y_paquetes",
     "Paquetes_mas_importantes"],
    ["Ficheros",
     "Creando_un_Programa_de_Lectura_y_Escritura",
     "JSON_Que_es",
     "Utilizando_JSON_como_Base_de_Datos"],
    ["Introduccion_a_Bases_de_Datos_en_Python",
     "SQLite_en_Python_Gestion_de_Bases_de_Datos_Locales",
     "Conexion_y_Manipulación_de_Bases_de_Datos_MySQL_con_Python"]
]

# URL lists (each primary list by target directory) #
vidclassURLListArr = [
    ["https://vimeo.com/805454676/db917942c5",
     "https://vimeo.com/810062265/54715f6f36",
     "https://vimeo.com/812335996/5c496f7550"],
    ["https://vimeo.com/807841991/29d50dd3ef"],
    ["https://vimeo.com/697285068/c49ff173bf",
     "https://vimeo.com/706875518/27318bfaf1",
     "https://vimeo.com/817197031/761adb51b4",
     "https://vimeo.com/818639848/53c504ad3f",
     "https://vimeo.com/819424302/2ab53573e9",
     "https://vimeo.com/821182589/8a908d2168",
     "https://vimeo.com/823640960/20d521ed17"],
    ["https://vimeo.com/673516157/70e1ef0e2f",
     "https://vimeo.com/694947772/df621e3886",
     "https://vimeo.com/825012754/918e7c85f5",
     "https://vimeo.com/827180102/5e982ba253",
     "https://vimeo.com/829349581/5e624f0cbe",
     "https://vimeo.com/833613022/4fb5c3f9dc",
     "https://vimeo.com/835710300/88334f6119"],
    ["https://vimeo.com/837830983/2520dbc748",
     "https://vimeo.com/840736669/d15f16fcd8",
     "https://vimeo.com/842106995/21ea7dbb42",
     "https://vimeo.com/844157839/0f25fc49b8",
     "https://vimeo.com/846178254/731eb21af9",
     "https://vimeo.com/850175808/affffad60f"],
    ["https://vimeo.com/861978695/6449b45c86",
     "https://vimeo.com/863895162/8fe4a86f85",
     "https://vimeo.com/865871384/76222e5685",
     "https://vimeo.com/868267983/e96fb93534"],
    ["https://vimeo.com/870600987/9bfaec0363",
     "https://vimeo.com/872830735/12cbf7b5b2",
     "https://vimeo.com/875086599/bdc9644ae2"]                    
]

lvcula = len(vidclassURLListArr)

# Downloading process info table #
#--------------------------------#

download_process_table = """
Download progress information
-----------------------------

·Module: {} (out of {})
·File {} ({} out of {} for the current module)
"""

#----------------------#
# Downloadings section #
#----------------------#

# Change primary directory for each troncal video URL #
for secDirListEnum in enumerate(curPathDirArr, start=1):

    secDirList = secDirListEnum[1]
    secDirListNum = secDirListEnum[0]
    
    # Troncal videos #
    #-#-#-#-#-#-#-#-#-
        
    if secDirListNum == 1: 
        
        # To each secondary directory, a list of URLs corresponds #
        for d, troncalVidURLListEnum, troncalVidNameList\
        in zip(secDirList, enumerate(troncalVidURLListArr,start=1),
               troncalVidNameListArr):
             
            troncalVidURLListNum = troncalVidURLListEnum[0]
            troncalVidURLList = troncalVidURLListEnum[-1]
            ltrvul = len(troncalVidURLList)
                
            # Loop through all elements in each list #
            for troncalVidURLEnum, troncalVidName in zip(enumerate(troncalVidURLList,start=1),
                                                         troncalVidNameList):
                
                troncalVidURLNum = troncalVidURLEnum[0]
                troncalVidURL = troncalVidURLEnum[-1]
                
                # Execute yt-dlp through os.system to get the URL format table #
                yt_dlp_specsyn = yt_dlp_flist.format(troncalVidURL, default_fn)
                yt_dlp_list_comm = exec_shell_command(yt_dlp_specsyn)
                
                if isinstance(yt_dlp_list_comm, int) and yt_dlp_list_comm >= 0:
                    
                    """
                    For each secondary directory, get the available format ID
                    table using yt-dlp and insert into a text doc.
                    """
                                
                    # Read the content of the format file #            
                    df_troncalVid_ID = read_table(default_fn, header=18)
                    
                    """
                    Because of the wide range of separators in the table,
                    Python's built-in ´re´ module will be used,
                    maintaining the data frame as is, with an only column.
                                     
                    The best quality tag is the last ID,
                    but some times an unknown format tag appears,
                    so it has to be filtered out.                
                    """
    
                    lastAttr = df_troncalVid_ID.iloc[-1,0]
                    least2lastAttr = df_troncalVid_ID.iloc[-2,0]
                    isLastAttributeUnknown = find_substring_index(lastAttr, keyword)
                    
                    if isLastAttributeUnknown:
                        format_ID = least2lastAttr.split()[0]
                    else:
                        format_ID = lastAttr.split()[0]
                        
                    # Download the video #                        
                    output_file_name = f"{d}/{troncalVidName}.{extensions[1]}"
                    print(download_process_table.format(troncalVidURLListNum,
                                                        ltrvula,
                                                        output_file_name,
                                                        troncalVidURLNum,
                                                        ltrvul))
                    
                    yt_dlp_download_syn = yt_dlp_download.format(format_ID, 
                                                                 troncalVidURL,
                                                                 downloads_sleep_secs,
                                                                 output_file_name)
                    
                    yt_dlp_download_comm = exec_shell_command(yt_dlp_download_syn)
                    
                    if not (isinstance(yt_dlp_download_comm, int)\
                    and yt_dlp_download_comm >= 0):
                        raise OSError(f"Could not execute command '{yt_dlp_download_comm}'")
                        
                else:
                    raise OSError(f"Could not execute command '{yt_dlp_list_comm}'")
                    
    elif secDirListNum == 2:
        
        # Video classes #
        #-#-#-#-#-#-#-#-#
        
        # To each secondary directory, a list of URLs corresponds #
        for d, vidclassURLListEnum, vidclassNameList\
        in zip(secDirList, enumerate(vidclassURLListArr, start=1),
               vidclassNameListArr):
            
            vidclassURLListNum = vidclassURLListEnum[0]
            vidclassURLList = vidclassURLListEnum[-1]
            lvcul = len(vidclassURLList)
            
            # Loop through all elements in each list #
            for vidclassURLEnum, vidclassName in zip(enumerate(vidclassURLList, start=1),
                                                     vidclassNameList):
                
                vidclassURLNum = vidclassURLEnum[0]
                vidclassURL = vidclassURLEnum[-1]
                
                # Execute yt-dlp through os.system to get the URL format table #
                yt_dlp_specsyn = yt_dlp_flist.format(vidclassURL, default_fn)
                yt_dlp_list_comm = exec_shell_command(yt_dlp_specsyn)
                
                if isinstance(yt_dlp_list_comm, int) and yt_dlp_list_comm >= 0:
                    
                    """
                    For each secondary directory, get the available format ID
                    table using yt-dlp and insert into a text doc.
                    """
                                
                    # Read the content of the format file #            
                    df_vidclass_ID = read_table(default_fn, header=18)
                    
                    """
                    Because of the wide range of separators in the table,
                    Python's built-in ´re´ module will be used,
                    maintaining the data frame as is, with an only column.
                                     
                    The best quality tag is the last ID,
                    but some times an unknown format tag appears,
                    so it has to be filtered out.                
                    """
    
                    lastAttr = df_vidclass_ID.iloc[-1,0]
                    least2lastAttr = df_vidclass_ID.iloc[-2,0]
                    isLastAttributeUnknown = find_substring_index(lastAttr, keyword)
                    
                    if isLastAttributeUnknown != -1:
                        format_ID = least2lastAttr.split()[0]
                    else:
                        format_ID = lastAttr.split()[0]
                        
                    # Download the video #
                    output_file_name = f"{d}/{vidclassName}.{extensions[1]}"
                    print(download_process_table.format(vidclassURLListNum,
                                                        lvcula,
                                                        output_file_name,
                                                        vidclassURLNum,
                                                        lvcul))
                    
                    yt_dlp_download_syn = yt_dlp_download.format(format_ID, 
                                                                 vidclassURL,
                                                                 downloads_sleep_secs,
                                                                 output_file_name)
                    
                    print(yt_dlp_download_syn)
                    yt_dlp_download_comm = exec_shell_command(yt_dlp_download_syn)
                    
                    if not (isinstance(yt_dlp_download_comm, int)\
                    and yt_dlp_download_comm >= 0):
                        raise OSError(f"Could not execute command '{yt_dlp_download_comm}'")
                        
                else:
                    raise OSError(f"Could not execute command '{yt_dlp_list_comm}'")
                    
#--------------------------------------------------------#
# Delete the temporary file containing available formats #
#--------------------------------------------------------#

remove_files_byFS(f"*{default_fn}*", ".")