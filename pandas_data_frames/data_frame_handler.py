#----------------#
# Import modules #
#----------------#

import datetime

import json
from pathlib import Path
import sys

import numpy as np
import pandas as pd

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
custom_mod2_path = f"{fixed_path}/parameters_and_constants"
custom_mod3_path = f"{fixed_path}/strings"
                                        
# Add the module path to the path variable #
#------------------------------------------#

sys.path.append(custom_mod1_path)
sys.path.append(custom_mod2_path)
sys.path.append(custom_mod3_path)

# Perform the module importations #
#---------------------------------#

import file_and_directory_handler
import file_and_directory_paths
import global_parameters
import string_handler

#----------------------------------------------------#
# Define imported module(s)´ function call shortcuts #
#----------------------------------------------------#

basic_time_format_strs = global_parameters.basic_time_format_strs

find_fileString_paths = file_and_directory_paths.find_fileString_paths
remove_files_byFS = file_and_directory_handler.remove_files_byFS

get_obj_specs = string_handler.get_obj_specs
find_substring_index = string_handler.find_substring_index

#------------------#
# Define functions #
#------------------#

def infer_time_frequency(df_or_index):
    
    """
    Infer the most likely frequency given the input index,
    using pandas's infer_freq method.
    If the frequency is uncertain, a warning will be printed.
    
    Parameters
    ----------
    df_or_index : pandas.DataFrame or
                  pandas.Series or
                  DatetimeIndex or TimedeltaIndex
    
          The method will first assume that the input argument 
          is a pandas object, so that is has a date key column,
          and will attempt to infer the time frequency.
          
          To do so, the already defined 'find_date_key' attempts
          to find the date column. If cannot be found,
          that will mean that the input argument is not a pandas object
          but a DatetimeIndex of TimedeltaIndex object instead.
    
    Returns
    -------
    str
          The time frequency.
          If the frequency cannot be determined, pandas.infer_freq
          method returns None. In such case, this function is designed
          to raise a ValueError that indicates so.
    
    Note
    ----
          If passed a pandas's Series 
          will use the values of the series (NOT THE INDEX).
    """
   
    try:
        date_key = find_date_key(df_or_index)
        time_freq = pd.infer_freq(df_or_index[date_key])
    except:
        time_freq = pd.infer_freq(df_or_index)
        
    if time_freq is None:
        raise ValueError("Could not determine the time frequency.")
    else:
        return time_freq

    
def infer_full_period_of_time(df):
    
    date_key = find_date_key(df)
    years = np.unique(df[date_key].dt.year)
    full_period = f"{years[0]-years[-1]}"
    
    return full_period


def find_date_key(df):
    
    """
    Function that searches for date key in the columns of a pandas data frame.
    
    Parameters
    ----------
    df : pandas.DataFrame
          Pandas data frame containing data.
    
    Returns
    -------
    date_key : str
          String which date key is identified with.
    """
    
    df_cols = np.char.lower(df.columns.tolist())
    time_kws = ["da", "fe", "tim", "yy"]
    
    date_key_idx = find_substring_index(df_cols, time_kws)
    
    try:
        date_key = df_cols[date_key_idx]
        return date_key
    except:
        raise ValueError("Grouper name 'date' or similar not found")

def read_table_and_split_bywhitespaces(file_name,
                                       minimum_white_nspaces_column=1,
                                       engine=None,
                                       encoding=None,
                                       row=None):
    """
    Function that uses pandas module to read a text file
    and converts to a data frame.
    
    For that it uses the read_table function; if the result
    is a data frame that has only one columns
    (usually because each row is a long string)
    then it tries to split according to whitespaces
    in order to form columns.
    
    It is assumed that the whitespace is one character long
    throughout the whole data frame.
    
    Parameters
    ----------
    
    file_name : str
          String that identifies the file to be examined.
    minimum_white_nspaces_column : int
          Defines the minimum number of spaces in order to consider
          a column splitting. Defaults to a single white space.
    engine : {'c', 'python', 'pyarrow'}, optional
          Parser engine to use. The C and pyarrow engines are faster, 
          while the python engine is currently more feature-complete. 
          Multithreading is currently only supported by the pyarrow engine.
          Defaults to None.
    encoding : str
          String that identifies the encoding to use for UTF
          when reading/writing.
          The widely value is 'utf-8' but it can happen that
          the text file has internal strange characters that
          UTF-8 encoding is not able to read.
          In such cases "latin1" is reccommended to use.
          Default value is ´None´ in which case
          ´errors="replace"´ is passed to ´open()´.
    row : int or NoneType
          Integer that is used to specify the first row
          to read the text file from.
          Default value is None, for the case in which
          the text file has no header at all.
    
    Returns
    -------
    new_df : pandas.Dataset
          Text file converted to a data frame.
    """

    df = pd.read_table(file_name, 
                       header=row, 
                       encoding=encoding,
                       engine=engine)

    # Find the number of columns #
    ncols = len(df.iloc[:,0].str.split("\s{1,}")[0])
    
    # Define the minimum-number-of-white-space splitter format #
    str_left = "\s{"
    str_right = ",}"
    column_splitting_formatter\
    = f"{str_left}{minimum_white_nspaces_column}{str_right}"

    # Define a new data frame and loop through each column,
    # concatting thereof to the new data frame.
    
    new_df = pd.DataFrame()
    
    for icol in range(ncols):
        df_col = df.iloc[:,0].str.split(column_splitting_formatter).str[icol]
        df_col_vals = df_col.values
        new_df = pd.concat([new_df,
                            pd.DataFrame(df_col_vals)],
                           axis=1,
                           ignore_index=True)
    return new_df

def read_table_simple(file_name,
                      engine=None,
                      whitespace_char=None,
                      encoding=None,
                      row=None):
    
    """
    Function that uses pandas module to read a text file
    and converts to a data frame.
    
    Its functioning is simpler than the function above,
    because it assumes that the text file is well organised,
    with no irregular spaces, and that spaces mean 
    there should be different columns.
    
    It is still assumed that the whitespace is one character long
    throughout the whole data frame.
    
    Parameters
    ----------
    
    file_name : str
          String that identifies the file to be examined..
    engine : {'c', 'python', 'pyarrow'}, optional
          Parser engine to use. The C and pyarrow engines are faster, 
          while the python engine is currently more feature-complete. 
          Multithreading is currently only supported by the pyarrow engine.
          Defaults to None.
    encoding : str
          String that identifies the encoding to use for UTF
          when reading/writing.
          Default value is 'utf-8' but it can happen that
          the text file has internal strange characters that
          UTF-8 encoding is not able to read.
          In such cases "latin1" is reccommended to use.
    whitespace_char : str
          Delimiter to use as a separator of columns.
    row : int or NoneType
          Integer that is used to specify the first row
          to read the text file from.
          Default value is None, for the case in which
          the text file has no header at all.
    Returns
    -------
    new_df : pandas.Dataset
          Text file converted to a data frame.
    """
    
    df = pd.read_table(file_name,
                       engine=engine,
                       encoding=encoding,
                       header=row,
                       delim_whitespace=whitespace_char)
    
    return df


def excel2df_base(df):
      
    """
    Use the 'rename' method to rename our columns
    by using a 'lambda', we simply take
    the final entry of the list obtained by splitting each column name
    any time there is a new line.
    If there is no new line, the column name is unchanged.
    """
    
    df_fixed = df.rename(columns=lambda x: x.split("\n")[-1])
    return df_fixed


def excel2dict(file_name):
    
    sheetsDataDict = pd.read_excel(file_name, sheet_name=None)
    allDataDict = {}
    
    for sht_name, sheet_df in sheetsDataDict.items():
        sheet_df_fixed = excel2df_base(sht_name, sheet_df)
        
        """Append to the 'full dictionary' """
        sht_dict = {sht_name : sheet_df_fixed}
        allDataDict.update(sht_dict)
        
    return allDataDict
    

def excel2df(file_name):
    
    sheetsDataDict = pd.read_excel(file_name, sheet_name=None)
    all_data_df = pd.DataFrame()
    
    for sht_name, sheet_df in sheetsDataDict.items():
        sheet_df_fixed = excel2df_base(sht_name, sheet_df)
        
        """Append to the 'full table' """
        all_data_df = pd.concat([all_data_df, sheet_df_fixed])
        all_data_df.reset_index(inplace=True, drop=True)
        
        """
        Delete the 'sheet' named column
        as a result of the application of ´reset_index´
        """
        all_data_df = all_data_df.drop(columns=["sheet"])
        
    return all_data_df


def save2excel(file_name,
               frame_obj,
               indiv_sheet_name="Sheet1",
               save_index=False,
               save_header=False):
    
    """
    Function that saves a data frame or set of data frames
    into separate excel tabs.
    
    Parameters
    ----------
    file_name : str
          String used to give a name or full path to the excel file.
    frame_obj : dict or pandas.DataFrame
          Object to introduce data into the excel file.
          A dictionary is used to introduce data with custom named tabs.
          Keys are tab or sheet names and values are pandas data frames.
          A pandas data frame is used to introduce
          single default name tab data.
    indiv_sheet_name : str
          Relevant only if 'frame_obj' is a data frame. Name of the single sheet
          in which to store the object.
    save_index : bool
          Boolean to choose whether to include a column into the excel document
          that identifies row numbers. Default value is False.
    save_header : bool
          Boolean to choose whether to include a row into the excel document
          that identifies column numbers. Default value is False.
    """
    
    name_ext = get_obj_specs(file_name, obj_spec_key="ext")
    lne = len(name_ext)
    
    if lne == 0:
        file_name += f".{extensions[1]}"
    
    file_name_noRelPath = get_obj_specs(file_name, obj_spec_key="name")
    fn_parent = get_obj_specs(file_name, obj_spec_key="parent")
    
    fileAlreadyExists\
    = bool(len(find_fileString_paths(file_name_noRelPath, 
                                     fn_parent,
                                     top_path_only=True)))
    
    if isinstance(frame_obj, dict):
        writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
        
        for sheet, frame in frame_obj.items():
            frame.to_excel(writer,
                           sheet_name=sheet,
                           index=save_index,
                           header=save_header)
            
        if fileAlreadyExists:
            overWriteStdIn\
            = input(f"Warning: file '{file_name}' "
                    f"at directory '{fn_parent}' already exists.\n"
                    "Do you want to overwrite it? (y/n) ")
            
            while overWriteStdIn != "y" and overWriteStdIn != "n":
                overWriteStdIn = input("\nPlease select 'y' for 'yes' "
                                       "or 'n' for 'no': ")
                
            if overWriteStdIn == "y":
                writer.close() 
            else:
                pass
        
        else:
            writer.close()


    elif isinstance(frame_obj, pd.DataFrame):
        
        if fileAlreadyExists:
            overWriteStdIn\
            = input(f"Warning: file '{file_name}' "
                    f"at directory '{fn_parent}' already exists.\n"
                    "Do you want to overwrite it? (y/n) ")
            
            while overWriteStdIn != "y" and overWriteStdIn != "n":
                overWriteStdIn = input("\nPlease select 'y' for 'yes' "
                                       "or 'n' for 'no': ")
                
            if overWriteStdIn == "y":
                remove_files_byFS(file_name, fn_parent)
                frame_obj.to_excel(file_name, 
                                   sheet_name=indiv_sheet_name,
                                   index=save_index,
                                   header=save_header)
            else:
                pass
            
        else:
            frame_obj.to_excel(file_name, save_index, save_header)
        
    else:
        raise ValueError("Wrong type of frame. "
                         "It must either be of type dict or"
                         "pd.DataFrame")
        

def merge_excel_files(input_file_list,
                      output_file_name,
                      save_index=False,
                      save_header=False,
                      save_merged_file=False):
    
    # Input_file_list and output_file_name can either be simple names or full paths
    
    if isinstance(input_file_list, str):
        input_file_list = [input_file_list]
        
    lifn = len(input_file_list)
    
    if lifn == 1:
        raise ValueError("At least 2 files must be given "
                          "in order to perform the merge.")
        
    sheet_name_list = []
    
    for file in input_file_list:
        sheet_name_file = list(excel2dict(file).keys())
        for snf in sheet_name_file:
            sheet_name_list.append(snf)
    
    sheet_names_unique = np.unique(sheet_name_list)
    
    lsnl = len(sheet_name_list)
    lsnu = len(sheet_names_unique)
    
    if lsnl != lsnu:
        raise OSError("Some files have sheet names in common. "
                      "That would lead to an overwrite of the data.\n"
                      "Please check the sheet names.")
    
    allFileDataDict = {}
    
    for file in input_file_list:
        sheet_name_dict = excel2dict(file)
        allFileDataDict.update(sheet_name_dict)
        
    if save_merged_file:
        save2excel(output_file_name,
                   allFileDataDict, 
                   save_index=save_index, 
                   save_header=save_header)
        
    else:
        ind_file_df_list = list(allFileDataDict.values())
        
        ind_file_df_nrow_list = []
        all_file_data_df = pd.DataFrame()
        
        for file_df in ind_file_df_list:
            all_file_data_df = pd.concat([all_file_data_df, file_df], axis=1)
           
            file_df_shape = file_df.shape
            ind_file_df_nrow_list.append(file_df_shape[0])
                
        ind_file_df_nrow_unique = np.unique(ind_file_df_nrow_list)
        lifdnu = len(ind_file_df_nrow_unique)
        
        if lifdnu > 1:
            print("Warning: number of rows of data in some files "
                  "is not common to all data.")

        return all_file_data_df
        
        
def json2df(json_file_list):
    
    if isinstance(json_file_list, str):
        json_file_list = [json_file_list]
    
    df = pd.DataFrame()

    for json_file in json_file_list:
        
        with open(json_file, 'r', encoding='latin1') as jsf:
            data = json.load(jsf)
            next_df = pd.json_normalize(data)
            df = pd.concat([df, next_df],ignore_index=True)
 
    return df


def save2csv(file_name,
             data_frame,
             separator,
             save_index,
             save_header,
             decimal=".",
             date_format=None):
    
    """
    Function that saves a data frame into a CSV file.
    
    Parameters
    ----------
    file_name : str
          String that identifies the name of the output file.
    data_frame : pandas.DataFrame
          Data frame where data is stored.
    separator : str
          String used to separate data columns.
    save_index : bool
          Boolean to choose whether to include a column into the excel document
          that identifies row numbers. Default value is False.
    save_header : bool
          Boolean to choose whether to include a row into the excel document
          that identifies column numbers. Default value is False.
    date_format : str
          In case the data frame contains a time column,
          use to give format thereof when storing the data frame.
    """
    
    if isinstance(data_frame, pd.DataFrame):
        
        name_ext = get_obj_specs(file_name, obj_spec_key="ext")
        lne = len(name_ext)
        
        if lne == 0:
            file_name += f".{extensions[0]}"
        
        file_name_noRelPath = get_obj_specs(file_name, obj_spec_key="name")
        fn_parent = get_obj_specs(file_name, obj_spec_key="parent")
        
        fileAlreadyExists\
        = bool(len(find_fileString_paths(file_name_noRelPath, 
                                         fn_parent,
                                         top_path_only=True)))
        
        if not date_format:
            
            if fileAlreadyExists:
                overWriteStdIn\
                = input(f"Warning: file '{file_name}' "
                        f"at directory '{fn_parent}' already exists.\n"
                        "Do you want to overwrite it? (y/n) ")
                
                while overWriteStdIn != "y" and overWriteStdIn != "n":
                    overWriteStdIn = input("\nPlease select 'y' for 'yes' "
                                            "or 'n' for 'no': ")
                    
                if overWriteStdIn == "y":
                    remove_files_byFS(file_name, fn_parent)
                    data_frame.to_csv(file_name,
                                      sep=separator,
                                      decimal=decimal,
                                      index=save_index,
                                      header=save_header)
                    
                else:
                    pass
                
            else:
                data_frame.to_csv(file_name,
                                  sep=separator,
                                  decimal=decimal,
                                  index=save_index,
                                  header=save_header)
                
            
        else:
            if fileAlreadyExists:
                overWriteStdIn\
                = input(f"Warning: file '{file_name}' "
                        f"at directory '{fn_parent}' already exists.\n"
                        "Do you want to overwrite it? (y/n) ")
                
                while overWriteStdIn != "y" and overWriteStdIn != "n":
                    overWriteStdIn = input("\nPlease select 'y' for 'yes' "
                                            "or 'n' for 'no': ")
                    
                if overWriteStdIn == "y":
                    remove_files_byFS(file_name, fn_parent)
                    data_frame.to_csv(file_name,
                                      sep=separator,
                                      decimal=decimal,
                                      date_format=date_format,
                                      index=save_index,
                                      header=save_header)
                    
                else:
                    pass
                
            else:
                data_frame.to_csv(file_name,
                                  sep=separator,
                                  decimal=decimal,
                                  date_format=date_format,
                                  index=save_index,
                                  header=save_header)
            
    else:        
        raise TypeError("Wrong type of data. It must be of type 'pd.DataFrame'.")
    
def csv2df(file_name,
           separator,
           engine=None,
           encoding=None,
           header='infer',
           parse_dates=False,
           infer_dt_format_bool=False,
           index_col=None,
           decimal="."):
    
    """
    Function that loads a CSV file and loads the content
    into a pandas data frame to a CSV file.
    
    Parameters
    ----------
    file_name : str
          String that identifies the name of the file to evaluate.
    separator : str
          Delimiter to use.
    engine : {'c', 'python', 'pyarrow'}, optional
          Parser engine to use. The C and pyarrow engines are faster, 
          while the python engine is currently more feature-complete. 
          Multithreading is currently only supported by the pyarrow engine.
          Defaults to None.
    encoding : str
          Encoding to use for UTF when reading or writing.
          When this is ´None´, ´errors="replace"´ is passed to
          ´open()´; technically no encoding is used.
          Otherwise, ´errors="strict"´ is passed to ´open()´.
    header : int, list of int, str or NoneType
          Row number(s) to use as the column names, and the start of the
          data. Default behaviour is to infer the column names: if no names
          are passed the behaviour is identical to 'header=0' and column
          names are inferred from the first line of the file, if column
          names are passed explicitly then the behaviour is identical to
          'header=None'. Explicitly pass 'header=0' to be able to
          replace existing names.
    parse_dates : bool or list of int or names or list of lists or dict, default False
    The behaviour is as follows:
    
      * boolean. If True -> try parsing the index.
      * list of int or names. e.g. If [1, 2, 3] -> try parsing columns 1, 2, 3
          each as a separate date column.
      * list of lists. e.g.  If [[1, 3]] -> combine columns 1 and 3 and parse as
          a single date column.
        * dict, e.g. {'foo' : [1, 3]} -> parse columns 1, 3 as date and call
          result 'foo'
    
    infer_dt_format_bool : bool
          If True and ´parse_dates´ is enabled, pandas will attempt to infer the
          format of the datetime strings in the columns, and if it can be inferred,
          switch to a faster method of parsing them. In some cases this can increase
          the parsing speed by 5-10x
    index_col : int, str, sequence of int / str, False or NoneType
          Column(s) to use as the row labels of the 'DataFrame', either given as
          string name or column index. If a sequence of int / str is given, a
          MultiIndex is used.
    decimal : str
          Character to recognize as decimal point (e.g. use ',' 
          for European data). Default value is '.' (dot).
    """
        
    if not parse_dates:
        df = pd.read_csv(file_name, 
                         sep=separator,
                         decimal=decimal,
                         encoding=encoding,
                         header=header,
                         index_col=index_col,
                         engine=engine)
        
    elif parse_dates and not infer_dt_format_bool:
        raise ValueError("Please set ´infer_datetime_format´ argument to True")
        
    else:
        df = pd.read_csv(file_name, 
                         sep=separator,
                         decimal=decimal,
                         encoding=encoding,
                         header=header,
                         engine=engine,
                         parse_dates=parse_dates,
                         index_col=index_col,
                         infer_datetime_format=infer_dt_format_bool)
    
    return df


def merge_csv_files(input_file_list, 
                    output_file_name,
                    separator_in,
                    separator_out=";",
                    engine=None,
                    encoding=None,
                    header='infer',
                    parse_dates=False,
                    infer_dt_format_bool=False,
                    index_col=None,
                    decimal=".",                                 
                    save_index=False,
                    save_header=False,
                    save_merged_file=False):
    
    # Usage of separator_in applies for all files, which means
    # that every file must have the same separator.
    
    if isinstance(input_file_list, str):
        input_file_list = [input_file_list]
        
    lifn = len(input_file_list)
    
    if lifn == 1:
        raise ValueError("At least 2 files must be given "
                          "in order to perform the merge.")
        
    ind_file_df_nrow_list = []
    all_file_data_df = pd.DataFrame()
        
    for file in input_file_list:
        file_df = csv2df(separator=separator_in,
                         engine=engine,
                         encoding=encoding,
                         header=header,
                         parse_dates=parse_dates,
                         infer_dt_format_bool=infer_dt_format_bool,
                         index_col=index_col,
                         decimal=decimal)
        
        all_file_data_df = pd.concat([all_file_data_df, file_df], axis=1)
        
        file_df_shape = file_df.shape
        ind_file_df_nrow_list.append(file_df_shape[0])
        
    ind_file_df_nrow_unique = np.unique(ind_file_df_nrow_list)
    lifdnu = len(ind_file_df_nrow_unique)
    
    if lifdnu > 1:
        print("Warning: number of rows of data in some files "
              "is not common to all data.")
        
    if save_merged_file:
        save2csv(output_file_name, 
                 all_file_data_df, 
                 separator=separator_out,
                 decimal=decimal,
                 save_index=save_index, 
                 save_header=save_header)
        
    else:
        return all_file_data_df
    

def insert_column_in_df(df, index_col, column_name, values):
    
    """
    Function that inserts a column on a simple, non multi-index
    pandas data frame, specified by an index column.
    
    Parameters
    ----------
    df : pandas.DataFrame
          Data frame containing data.
    index_col : int
          Denotes the column position to insert new data.
          It is considered that data is desired to introduced
          at the LEFT of that index, so that once inserted data on that position, 
          the rest of the data will be displaced rightwards.
    column_name : str
          Name of the column to be inserted.
    values : list, numpy.array or pandas.Series
    """

    df.insert(index_col, column_name, values)
    
    
def insert_row_in_df(df, index_row, values=np.nan, reset_indexes=False):
    
    """
    Function that inserts a row on a simple, non multi-index
    pandas data frame, in a specified index column.
    That row can be introduced at the begginning, ending,
    or in any position between them.
    This function works either with integer or DatetimeIndex arrays.
    
    Parameters
    ----------
    df : pandas.DataFrame
          Data frame containing data.
    index_row : int, str, datetime.datetime
                or pandas._libs.tslibs.timestamps.Timestamp
          Denotes the row position to insert new data.
          It is considered that data is desired to introduced
          ABOVE that index, so that once inserted data on that position, 
          the rest of the data will be displaced downwards.
          
          Strictly speaking, this function distinguishes between four cases:
          1. The index is an integer:
              If index_row == 0 then the row will be introduced
              at the begginning, ending if index_row == -1,
              else at any other position.
          2. The index is a datetime.datetime tuple:
              The index will be introduced at the end of the data frame,
              and then the indexes will be sorted.
              Note this means that the new time array spacing is NOT even.
              
    values : single value or list or numpy.array or pandas.Series
          The type of the value(s) is considered as irrelevant.
          Default value is a row of NaNs.
    """
    
    idx = df.index
    
    if isinstance(idx, pd.RangeIndex)\
    or isinstance(idx, pd.Float64Index):
    
        if index_row == 0:
            df_shift = df.shift()
            df_shift.loc[idx[-1]+1] = df.loc[idx[-1]] 
            df_shift.loc[idx[0], :] = values
            df = df_shift
            
        elif index_row == -1:
            df.loc[idx[-1]+1, :] = values
            
        else:
            index_between = index_row - 0.5
            df.loc[index_between, :] = values
            
            if reset_indexes:
                df = df.reset_index(drop=True)
    
    else:
        try:
            time_freq = pd.infer_freq(idx)
        except:
            time_freq = pd.infer_freq(idx[100])
            
        time_abbrs = basic_time_format_strs
        
        if isinstance(index_row, str):
            if time_freq not in time_abbrs:
                time_format = basic_time_format_strs["H"]
            else:
                time_format = basic_time_format_strs[time_freq]
                
            index_row = datetime.datetime.strptime(index_row, time_format)
        
        df.loc[index_row, :] = values
        df.sort_index()
        
    return df
        
    
    
def sort_df_indexes(df,
                    axis=0,
                    ignore_index_bool=False,
                    level=None,
                    ascending_bool=True,
                    na_position="last",
                    sort_remaining_bool=True,
                    key=None):
    
    """
    Returns a new data frame sorted 
    
    Parameters
    ----------
    df : pandas.DataFrame or pandas.Series.
    level : int or level name or list of ints or list of level names
          If not None, sort on values in specified index level(s)
    axis : {0, 'index', 1, 'columns'}
          Axis to be sorted; default value is 0.
    ignore_index : bool
          Boolean to determine whether to relabel indexes
          at ascending order: 0, 1, ..., n-1 or remain them unchanged.
          Defaults False.
    ascending : bool or list of bool
          Sort ascending vs. descending. Specify list for multiple sort
          orders. Default is True boolean.
    na_position : {'first', 'last'}.
          Puts NaNs at the beginning if ´first´; ´last´ puts NaNs at the end.
          Defaults to "last".
    sort_remaining : bool
          If True and sorting by level and index is multilevel, sort by other
          levels too (in order) after sorting by specified level.
          Default value is True.
    key : callable, optional
          Apply the key function to the values
          before sorting. This is similar to the ´key´ argument in the
          builtin :meth:´sorted´ function, with the notable difference that
          this ´key´ function should be *vectorized*.
    """
            
    df.sort_index(axis=axis, 
                  level=level,
                  ascending=ascending_bool,
                  na_position=na_position,
                  sort_remaining=sort_remaining_bool,
                  ignore_index=ignore_index_bool,
                  key=key)
    
    return df
    
    
def sort_df_values(df,
                   by,
                   ignore_index_bool=False,
                   axis=0,
                   ascending_bool=True,
                   na_position="last",
                   key=None):
    
    """
    Sort by the values along either axis
    
    Parameters
    ----------
    df : pandas.DataFrame or pandas.Series.
    by : str or list of str
          Name or list of names to sort by.
    ignore_index : bool
          Boolean to determine whether to relabel indexes
          at ascending order: 0, 1, ..., n-1 or remain them unchanged.
          Defaults False.
    axis : {0, 'index', 1, 'columns'}
          Axis to be sorted; default value is 0.
    ascending : bool or list of bool
          Sort ascending vs. descending. Specify list for multiple sort
          orders. Default is True boolean.
    na_position : {'first', 'last'}
          Puts NaNs at the beginning if ´first´; ´last´ puts NaNs at the end.
          Defaults to "last".
    key : callable, optional
          Apply the key function to the values
          before sorting. This is similar to the ´key´ argument in the
          builtin :meth:´sorted´ function, with the notable difference that
          this ´key´ function should be *vectorized*.
    """
    
    df = df.sort_values(by=by,
                        axis=axis, 
                        ascending=ascending_bool,
                        na_position=na_position,
                        ignore_index=ignore_index_bool,
                        key=key)

    return df


def reindex_df(df, col_to_replace=None, vals_to_replace=None):
    
    """
    Further function than df.reset_index method,
    for resetting the index of the given pandas data frame,
    using any specified column and then resetting the latter.
    This method applies only for one-leveled objects
    (i.e, cannot have a MultiIndex) and can contain any tipe of index.
    It can also be applied for simple reindexing.
    
    Parameters
    ----------
    df : pandas.DataFrame or pandas.Series.
    vals_to_replace : list, np.ndarray or pandas.Series
          New labels / index to conform to.
    col_to_replace : str or int
          If further reindexing is required,
          an it is a string, then it selects the columns to put as index.
          Otherwise it selects the number column.
          Defaults to None, that is, to simple reindexing.
    """
    
    if col_to_replace is None and vals_to_replace is None:
        raise ValueError("You must provide an object containing values to"
                         "put as index.")
        
    elif col_to_replace is None and vals_to_replace is not None:
        df = df.reindex(vals_to_replace)
        
    else:
        
        if isinstance(col_to_replace, str):

            # Substitute the index as desired #  
            df_reidx_dropCol\
            = df.reindex(df[col_to_replace]).drop(columns=col_to_replace)
            
            # Assign the remaining values to the new data frame #
            df_reidx_dropCol.loc[:,:]\
            = df.drop(columns=col_to_replace).values
            
        elif isinstance(col_to_replace, int):
            
            columns = df.columns
            colname_to_drop = columns[col_to_replace]
            
            # Substitute the index as desired #              
            df_reidx_dropCol\
            = df.reindex(df.iloc[:, col_to_replace]).drop(columns=colname_to_drop)
        
            # Assign the remaining values to the new data frame #
            df_reidx_dropCol.loc[:,:]\
            = df.drop(columns=colname_to_drop).values
        
    return df_reidx_dropCol


def create_pivot_table(df, df_values, df_index, funcToApplyOnValues):
    
    pivot_table = pd.pivot_table(df,
                                 values=df_values, 
                                 index=df_index,
                                 aggfunc=funcToApplyOnValues)
    
    return pivot_table


def countDataByConcept(df, df_cols):
    dataCount = df.groupby(df_cols).count()
    return dataCount    


#-----------------------------------------------#
# Define global parameters below every function #
#-----------------------------------------------#

"""Declare those global so as not to use them
repeatedly inside functions above.
"""

extensions = ["csv", "xlsx"]
