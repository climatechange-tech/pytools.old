#----------------#
# Import modules #
#----------------#

import numpy as np
import pandas as pd

import inspect
import types
from typing import cast

#------------------#
# Define functions # 
#------------------#

def sort_array_rows_by_column(array, ncol):
    
    # Function that sorts the values contained in a specific column of
    # an array. Then the values of the rest of the columns are
    # sorted out the same way they are on the first column.
    # 
    # Parameters
    # ----------
    # array : numpy.ndarray
    #       Array containing the values.
    # ncol : int
    #       Integer indicating which column values are going to be sorted.
    # 
    # Returns
    # -------
    # sorted_array : numpy.ndarray
    #       Array containing the sorted values along the specified column.
    # 
    # Example
    # -------
    # 
    # >>> array=np.random.randint(1,10,size=(10,4))
    # >>> array
    # array([[4, 6, 6, 1],
    #        [4, 6, 4, 1],
    #        [1, 4, 2, 8],
    #        [5, 6, 1, 8],
    #        [4, 2, 4, 2],
    #        [2, 9, 7, 2],
    #        [5, 7, 6, 2],
    #        [7, 2, 7, 1],
    #        [7, 4, 4, 6],
    #        [2, 7, 5, 4]])
    # 
    # sort_array_rows_by_column(array, 0)
    # array([[1, 4, 2, 8],
    #        [2, 9, 7, 2],
    #        [2, 7, 5, 4],
    #        [4, 6, 6, 1],
    #        [4, 6, 4, 1],
    #        [4, 2, 4, 2],
    #        [5, 6, 1, 8],
    #        [5, 7, 6, 2],
    #        [7, 2, 7, 1],
    #        [7, 4, 4, 6]])
    
    sorted_array = array[np.argsort(array[:,ncol])]
    return sorted_array

def approach_value_in_array(array, given_value):
    
    # Finds the index of the nearest value compared to the original one
    # in an array.
    # 
    # Parameters
    # ----------
    # array : numpy.ndarray or pandas.core.frame.DataFrame
    #         or pandas.core.series.Series
    #         Array or pandas data frame or series containing the values.
    # 
    # given_value : float
    #       Value which to compare with those contained in the 'array' parameter.
    # 
    # Returns
    # -------
    # approached_val : float
    #       Closest value in array to the given value.
    # approached_val_idx : tuple or float
    #       Index of the closest value.
    #       If the array or pandas series is of 1D, it returns a float
    #       number where the closest value is located.
    #       If the array or pandas series is of 2D, it returns a tuple
    #       containing the rows and columns where the closest value is located.
    
    shape = array.shape
    
    if len(shape) > 1:
        
        if not isinstance(array, np.ndarray):
            array = array.values
            
        array_vs_given_value_diff_function = lambda array: abs(array-given_value)
        approached_val = min(array.flatten(), key=array_vs_given_value_diff_function)
        approached_val_idx = np.where(array==approached_val)
                        
    else: 
        
        if not isinstance(array, np.ndarray):  
            array = array.values
            
        array_vs_given_value_diff_function = lambda array: abs(array-given_value)        
        approached_val = min(array, key=array_vs_given_value_diff_function)
        approached_val_idx = np.where(array==approached_val)[0][0]

    return approached_val, approached_val_idx


def objectvalues2float(data, colname):

    # Function that converts dtype==object ('O') data
    # to 64-bit precision float numbers.
    # If there is no such type of data, it returns the same type of data.
    #
    # Parameters
    # ----------
    # data : pd.core.frame.DataFrame or numpy.ndarray
    #       Object containing data.
    # colname : str
    #       Necessary only if pd.core.frame.DataFrame cases is passed.
    #       Column name along which to perform the conversion.
    #       Set to None if a numpy.ndarray is passed.
    #
    # Returns
    # -------
    # data : pd.core.frame.DataFrame or numpy.ndarray
    #       Object containing floated data, if necessary.

    method_name = cast(types.FrameType, inspect.currentframe()).f_code.co_name

    if isinstance(data, pd.core.frame.DataFrame):

        if colname == None:
            print("Please introduce a valid column name of the data frame")

        else:

            if data.loc[:,colname].dtype == 'O':
                data_floated = data.copy()
                data_floated.loc[:,colname] = data_floated.loc[:,colname].astype('d')
                return data_floated
            else:
                return data

    else:

        if colname != None:
            print("Please set the second argument "
                  f"of the '{method_name}' function to 'None'")

        else:

            if data.dtype == 'O':
                data_floated = data.copy().astype('d')
                return data_floated
            else:
                return data

def sort_values_externally(array, wantarray=False):
    
    # Function that sorts array values,
    # irrespective of the type (except special cases) of data.
    # It is intended to use in such cases where
    # the simple use of sort() method would lead
    # no other option than assigning a variable,
    # which causes to return a generator;
    # of course, this function can be used
    # however simple the case it is.
    # 
    # Parameters
    # ----------
    # array : list or numpy.ndarray
    #       Array containing string, integer, float, etc. values,
    #       but all of the same semantic type.
    # wantarray : bool
    #       Determines whether to return the sorted values
    #       in an array, otherwise the functions returns
    #       them in a list. Default behavior is the latter one.
    #       
    # Returns
    # -------
    # sorted_array : list or numpy.ndarray
    #       List or array of sorted values.

    if isinstance(array, list):
        # Invoke the method without assigning a new variable #
        array.sort()

    elif isinstance(array, np.ndarray):
        array = np.sort(array)

    if wantarray:
        array = np.array(array)

    sorted_values = array.copy()
    return sorted_values


def count_unique_type_objects(list_of_objects):
    
    # Checks whether all objects contained in a given list are the same,
    # for that iterating over the list, getting the type,
    # make the list of types unique and checking its length.
    # 
    # Parameters
    # ----------
    # list_of_objects : list
    #       List of whatever objects.
    # 
    # Returns
    # -------
    # unique_type_list : list of types
    #       List containing the unique types of the objects in the list.
    # lutl : int
    #       Length of the unique object type list.
    
    unique_type_list = np.unique([str(type(element)) for element in list_of_objects])
    lutl = len(unique_type_list)
    
    return unique_type_list, lutl    
        


def select_array_elements(array, idx2access):

    # Function to select a slice of a 1D array or list.
    # If dimension number is greater than one,
    # then throws a warning indicating that.
    #
    # Parameters
    # ----------
    # array : list or numpy.ndarray
    #       List or array containing whatever values
    # idx2access : int or list or numpy.ndarray
    #       List or array to select multiple values.
    #       If a single value is detected, 
    #       then it will be converted to list, because
    #       and integer object is not iterable.
    #
    # Returns
    # -------
    # slice : int or list or numpy.ndarray
    #       Single value or a slice of the input list or array
    
    if isinstance(idx2access, int):
        idx2access = [idx2access]
    
    if isinstance(array, list):
        accessed_mapping = map(array.__getitem__, idx2access)
        accessed_list = list(accessed_mapping)
        return accessed_list
    
    elif isinstance(array, np.ndarray):
        accessed_array = array[idx2access]
        return accessed_array
    
    
def remove_elements_from_array(array, idx2access, axis=None):
    
    # Function that removes certain elements either from a list or numpy array,
    # selected by indexes, which can be integers or booleans.
    # 
    # Parameters
    # ----------
    # array : list or numpy.array
    #       List or array containing whatever values
    # idx2access : list or numpy.array of integers or booleans
    #       Object containing indexes used to select elements
    #       from the previous list or array.
    # 
    # Returns
    # -------
    # array_filtered : numpy.ndarrayararray_filteredray_filtered
    #       NumPy's array with the selected elements removed.
    
    array_filtered = np.delete(array, idx2access, axis=axis)
    
    return array_filtered