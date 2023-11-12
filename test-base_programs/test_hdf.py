# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 14:06:11 2023

@author: jgabantxo_ext
"""

import numpy as np
import pandas as pd
import timeit

def process_data():
    
    # Date and time format strings #
    original_dt_str1 = "%d/%m/%Y %H:%M:%S"
    original_dt_str2 = "%d/%m/%Y %H:%M"
    
    standard_dt_str = '%Y-%m-%d %H:%M'
    
    # Time ranges #
    hour_range = range(24)
    month_range = range(1,13)
    
    lhours = len(hour_range)
    lmonths = len(month_range)
    
    # CSV file reading parameters #
    sepchar = ";"
    decimal_char = ","
    parse_dates = True
    
    # Excel file saving parameters #
    save_index = False
    save_header = True
    
    # Paths #
    main_path = "C:/Users/jgabantxo_ext/OneDrive - ACCIONA S.A/Documents/"\
                "01-RDT_ingenieros/bezeroak/Acciona/PROIEKTUAK/POLONIA/RYMAN"
    
    # Paths #
    input_data_dir = f"{main_path}/input_data"
    
    # Files #
    wind_10min_file = f"{input_data_dir}/Ryman_Sodar_1A_Perfilado_159,00 m_Config 1_10M.csv" 
    
    df_10min = pd.read_csv(wind_10min_file, 
                            sep = sepchar, 
                            decimal = decimal_char,
                            parse_dates = parse_dates)
    
    """Convert column 4 data to date and time"""
    time_col = "Fecha"
    df_10min_time = df_10min[time_col]
    df_10min_time_std = pd.to_datetime(df_10min_time, format = original_dt_str1)
    
    df_10min[time_col] = df_10min_time_std
    
    return df_10min


def store_hdf5():
    df = process_data()
    data_store = pd.HDFStore('processed_data.h5')
    data_store['preprocessed_df'] = df
    data_store.close()
    
    
def recover_hdf5():
    data_store = pd.HDFStore('processed_data.h5')
    df = data_store['preprocessed_df']
    data_store.close()
    
    return df

    


res1 = timeit.repeat("process_data()", repeat = 50,number = 1,globals = globals())
min_res1 = np.round(np.min(res1),3)
print(f"{res1}\n\n{min_res1}")

res2 = timeit.repeat("store_hdf5()", repeat = 50,number = 1,globals = globals())
min_res2 = np.round(np.min(res2),3)
print(f"{res2}\n\n{min_res2}")

res3 = timeit.repeat("recover_hdf5()", repeat = 50,number = 1,globals = globals())
min_res3 = np.round(np.min(res3),3)
print(f"{res3}\n\n{min_res3}")
