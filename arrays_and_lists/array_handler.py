#----------------#
# Import modules #
#----------------#

import numpy as np
import pandas as pd

#------------------#
# Define functions # 
#------------------#

def df_to_structured_array(df):
    records = df.to_records(index=False)
    data = np.array(records, dtype=records.dtype.descr)
    return data


def insert_values(x, index, values, axis=None):
    
    """
    Inserts values at the specified index either on a list or numpy array.
    
    Parameters
    ----------
    x : list or numpy.ndarray
          Object containing whatever type of data
    index : int
          Position where to introduce new data.
          Same behaviour as introducing a blank space at the left
          and then filling it with new data.
    values : list, numpy.array or pandas.Series
          If values are part of a data frame, they equally can be introduced
          into a list, to then call its data in the appropriate manner.
    axis : int or NoneType
          Axis along which to insert 'values'.  If 'axis' is None then 'x'
          is flattened first.
    
    Returns
    -------
    appended_array : numpy.ndarray
          Only if 'x' is a numpy.ndarray. Array with new data appended.
    """
    
    lx = len(x)
    
    if isinstance(x, list):        
        if index >= lx:
            print(f"Index {index} beyond list length, "
                  "will be appended at the end of it.")
            
        x.insert(index, values)
        return x
        
    elif isinstance(x, np.ndarray):
        x_appended = np.insert(x, index, values, axis=axis)
        return x_appended
        
    else:
        raise TypeError("Wrong type of data. "
                        "Data must either be a list or numpy array.")
        
        
def extend_array(obj, obj2extend, np_axis=None):
    if isinstance(obj, list):
        obj_extended = obj.extend(obj2extend)
    elif isinstance(obj, np.ndarray):
        obj_extended = np.concatenate((obj, obj2extend), axis=np_axis)
    else:
        raise TypeError("Input argument to be extended must either be of type "
                        "´list´ or ´np.ndarray´.")
    return obj_extended


def arrayOfList_to_array(arrayList):
    
    dimList = np.unique([len(arr.shape) for arr in arrayList])
    ld = len(dimList)
    
    # If all lists in the object are of the same dimension #
    if ld == 1:
        dims = dimList[0]
        
        if dims == 2:
            array = np.vstack(arrayList)
        elif dims == 3:
            array = np.stack(arrayList)
        else:
            raise Exception("Cannot handle lists containing D > 3 arrays.")
            
    # If the lists are multi-dimensional #
    else:
        array = extend_array(array, arrayList)
        # array = np.hstack(arrayList) (EQUIVALENT for 'np.concatenate')
        
    return array


def sort_array_rows_by_column(array, ncol, sort_order="ascending", order=None):
    
    """
    Function that sorts the values in a 2D dimension array
    against a specific column in an ASCENDING order.
    
    The result is an array with every row sorted out,
    such that the values in the selected column are the actual sorted values,
    i.e. only one value of every row is sorted out,
    with respect of the rest of that column, and the rest remains ummovable.
    
    This tool is useful when the array contains parameters with
    different semantics and only one column is needed to sort.
    
    Parameters
    ----------
    array : numpy.ndarray
          Array to be sorted.
    ncol : int
          Number of the column which values are going to be sorted against to.
    sort_order : {"ascending", "descending"}
          Default order is "ascending".
    
    Returns
    -------
    sorted_array : numpy.ndarray
          Array containing the sorted values as explained.
    
    Examples
    --------
    
    >>> array=np.random.randint(1,10,size=(3,4))
    >>> array
    array([[6, 4, 2, 3],
            [3, 9, 7, 1],
            [4, 6, 4, 5]])
    
    Suppose that we want to sort the values of the first column (ncol=0),
    but when it is done so, we want the rest of the values of each row to
    be fixed, instead of being sorted out.
    
    That is to say, the lowest value of the mentioned column is 3
    and the rest of the values of that row that it is defined are 9, 7 and 1.
    If we sort the column, the first number will be 3, but 9,7 and 1
    are required to follow number 3 and stay in the same row.
    The rest of the values of that first column are ordered
    following the same mechanism, and the result is the following:
    
    sort_array_rows_by_column(array, ncol=0)
    array([[3, 9, 7, 1],
            [4, 6, 4, 5],
            [6, 4, 2, 3]])
    
    Another example, more intuitive,
    where several files are needed to be sorted out
    with respect to the modification time, i.e. the second column:
    
    array([['VID-20221230_110.jpg', '2022-12-30 15:10:34'],
            ['VID-20221230_146.jpg', '2022-12-30 15:10:29'],
            ['VID-20221230_162.jpg', '2022-12-30 15:10:28'],
            ['VID-20221230_190.jpg', '2022-12-30 15:10:30'],
            ['VID-20221230_305.jpg', '2022-12-30 15:10:32'],
            ['VID-20221230_320.jpg', '2022-12-30 15:10:35']], dtype='<U27')
    
    sort_array_rows_by_column(array, ncol=1)
    array([['VID-20221230_162.jpg', '2022-12-30 15:10:28'],
            ['VID-20221230_146.jpg', '2022-12-30 15:10:29'],
            ['VID-20221230_190.jpg', '2022-12-30 15:10:30'],
            ['VID-20221230_305.jpg', '2022-12-30 15:10:32'],
            ['VID-20221230_110.jpg', '2022-12-30 15:10:34'],
            ['VID-20221230_320.jpg', '2022-12-30 15:10:35']], dtype='<U27')
    
    This example could be extended by adding the creation
    and last time access columns, but the mechanism remains exactly the same.
    """
    
    sort_order_ops = ["ascending", "descending"]
    
    if sort_order not in sort_order_ops:
        raise ValueError("Wrong sort order option. "
                         f"Options are {sort_order_ops}.")
    
    if sort_order == "ascending":
        try:
            sorted_array_rbc = array[np.argsort(array[:,ncol])]
        except:
            sorted_array_rbc = np.sort(array, order=order)
            
    else:
        try:    
            sorted_array_rbc = array[np.fliplr([np.argsort(array[:,ncol])])[0]]
        except:
            sorted_array_rbc = np.sort(array, axis=-1, order=order)
        
    return sorted_array_rbc


def sort_array_columns_by_row(array, nrow, sort_order="ascending"):
    
    """
    Function that sorts the values in a 2D dimension array
    against a specific row in an ASCENDING order.
    
    The result is an array with every column sorted out,
    such that the values in the selected row are the actual sorted values,
    i.e. only one value of every column is sorted out,
    with respect of the rest of that row, and the rest remains ummovable.
    
    This tool is useful when the array contains parameters with
    different semantics and only one row is needed to be sorted.
    
    Parameters
    ----------
    array : numpy.ndarray
          Array to be sorted.
    nrow : int
          Number of the row which values are going to be sorted against to.
    sort_order : {"ascending", "descending"}
          Default order is "ascending".
    
    Returns
    -------
    sorted_array : numpy.ndarray
          Array containing the sorted values as explained.
    
    Examples
    --------
    
    >>> array=np.random.randint(1,10,size=(3,4))
    >>> array
    array([[6, 4, 2, 3],
            [3, 9, 7, 1],
            [4, 6, 4, 5]])
    
    Suppose that we want to sort the values of the first row (row=0),
    but when it is done so, we want the rest of the values of each column to
    be fixed, instead of being sorted out.
    
    That is to say, the lowest value of the mentioned row is 2
    and the rest of the values of the column that it is defined are 7 and 4.
    If we sort the row, the first number will be 2, but 7 and 4
    are required to follow number 2 and stay in the same row.
    
    The rest of the values of that first row are ordered
    following the same mechanism.
    
    However, due to the naturally arised difficulty by the matrix definition,
    it is not straightforward to perform this operation programatically.
    Nevertheless, the matrix definition does allow 
    to work with consecutive transposes!
    
    >>> array1=array.T
    >>> array1
    array([[6, 3, 4],
            [4, 9, 6],
            [2, 7, 4],
            [3, 1, 5]])
    
    And now we apply the same method as sorting ROWS AGAINST a specified
    COLUMN, where now array === array.T, and ncol=nrow=0
    which is performed by the 'sort_array_rows_by_column' function:
    
    >>> array1_tr=sort_array_rows_by_column(array.T, ncol=0)
    >>> array1_tr
    array([[2, 7, 4],
            [3, 1, 5],
            [4, 9, 6],
            [6, 3, 4]])
    
    And now we calculate its transpose.
    >>> array2 = array1_tr.T
    >>> array2
    array([[2, 3, 4, 6],
            [7, 1, 9, 3],
            [4, 5, 6, 4]])
    """
    
    array_dtype = array.dtype
    
    try:
        array_tr = array.T
        sorted_array_cbr_tr = sort_array_rows_by_column(array_tr, nrow, sort_order)
        sorted_array_cbr = sorted_array_cbr_tr.T
        return sorted_array_cbr
    
    except:
        raise TypeError("Cannot perform operation with numpy arrays "
                        f"of data type {array_dtype}.")
    


def sort_array_complete(array, ncol, nrow, sort_order="ascending"):
    
    """
    This functon sorts a 2D array 'completely' at once, in the sense
    that the operations are only accomplished such that
    there are always ummovable elements, instead of sorting each and every
    value in an array, like np.sort() method does.
    The order is always ASCENDING.
    
    It firstly performs the sorting against a specific column,
    for that calling to the 'sort_array_rows_by_column' function.
    Then it sort every column of the resulting array against a specific row,
    for that calling the 'sort_array_columns_by_row' function.
    Recall that the rest of the rows are not sorted, again,
    like np.sort() would do.
    
    This tool is useful when the array contains parameters with
    different semantics and firstly only one column and secondly, 
    after that operation, every row needs to be sorted without
    considering them individually.
    
    Parameters
    ----------
    array : numpy.ndarray
          Array to be sorted.
    ncol : int
          Number of the column which values are going to be sorted against to.
    nrow : int
          Number of the row which values are going to be sorted against to.
    sort_order : {"ascending", "descending"}
          Default order is "ascending".
    
    Returns
    -------
    sorted_array : numpy.ndarray
          Array containing the sorted values as explained.
    
    Example
    -------
    
    >>> array=np.random.randint(1,10,size=(3,4))
    >>> array
    array([[6, 4, 2, 3],
            [3, 9, 7, 1],
            [4, 6, 4, 5]])
    
    sort_array_complete(array, ncol=0, nrow=0)
    array([[1, 3, 7, 9],
            [5, 4, 4, 6],
            [3, 6, 2, 4]])
    """
    
    array_dtype = array.dtype
    
    try:
        sorted_array_rbc = sort_array_rows_by_column(array, ncol, sort_order)
        sorted_array_cbr = sort_array_columns_by_row(sorted_array_rbc, 
                                                     nrow,
                                                     sort_order)
        sorted_array_complete = sorted_array_cbr.copy()
        return sorted_array_complete
    
    except:
        raise TypeError("Cannot perform operation with numpy arrays "
                        f"of data type {array_dtype}.")


def approach_value_in_array(array, given_value):
    
    """
    Finds the index of the nearest numerical value 
    compared to the original one in the given array.
    
    Parameters
    ----------
    array : list, numpy.ndarray or pandas.DataFrame
            or pandas.Series
            Array or pandas data frame or series containing the values.
    
    given_value : float
          Value which to compare with those contained in the 'array' parameter.
    
    Returns
    -------
    value_approach : int or float
          Closest value in array to the given value.
    value_approach_idx : int or float or tuple
          Index of the closest value.
          If the array or pandas series is of 1D, it returns a float
          number where the closest value is located.
          If the array or pandas series is of 2D, it returns a tuple
          containing the rows and columns where the closest value is located.
    """
    
    if not isinstance(array, list):
        shape = array.shape
        lsh = len(shape)
        
        if isinstance(array, pd.DataFrame):
            array = array.values
        
        diff_array = abs(array - given_value)
        
        value_approach_idx = np.where(array==np.min(diff_array))     
        if lsh == 1:        
            value_approach_idx = value_approach_idx[0][0]
            
        value_approach = array[value_approach_idx]
            
    else:
        shape = len(array)        
        diff_array = [abs(array[i] - given_value)
                      for i in range(shape)]
        value_approach_idx = [j
                              for j in range(shape) 
                              if diff_array[j]==min(diff_array)]
        
        if isinstance(value_approach_idx, list):
            value_approach_idx = value_approach_idx[0]
            
        value_approach = select_array_elements(array, value_approach_idx)
            
    return value_approach, value_approach_idx


def basicObjectValueTypeConverter(obj_data, old_type, new_type, colname=None):

    """
    Function that converts an object's values from the original dtype
    to the desired one.
    If the data's dtype is not the same as the original (old) one
    (e.g, if the original dtype is given mistakenly),
    the function simply returns the object unchanged,
    as well as printing a message showing the latter.
    
    Parameters
    ----------
    obj_data : pd.DataFrame or numpy.ndarray
          Object containing data.
    old_type : str
          Type of the given object's values.
          Options are {"O": object, "U": string, "d": double}.
    new_type : str
          Type the data has to be converted to.
          Options are the same as for parameter 'old_type'.
    colname : str
          Only necessary if pd.DataFrame cases is passed.
          Column name along which to perform the conversion.
          Set to None if a numpy.ndarray is passed.
    
    Returns
    -------
    obj_data : pd.DataFrame or numpy.ndarray
          Object containing floated data, if necessary.

    """  
    
    arg_names = basicObjectValueTypeConverter.__code__.co_varnames
    
    type_option_list = ["O", "U", "d"]
    
    if old_type not in type_option_list:
        raise ValueError(f"Wrong option of the original data type "
                         f"(argument '{arg_names[1]}').\n"
                         f"Options are {type_option_list}.")
    
    
    if isinstance(obj_data, pd.DataFrame):

        data_type = obj_data.loc[:,colname].dtype
        
        if colname is None:
            raise ValueError("Please introduce a valid "
                             f"column name (argument '{arg_names[3]})"
                             "of the obj_data frame.")

        else:            
            if data_type == old_type or old_type in data_type.str:
                data_floated = obj_data.copy()
                
                try:
                    data_floated.loc[:,colname]\
                    = data_floated.loc[:,colname].astype(new_type)
                    return data_floated
                    
                except:
                    raise TypeError(f"Cannot convert object to type '{new_type}'.")
                    
            else:
                print("Returning object with its values' type unchanged.")
                return obj_data

    else:
        
        data_type = obj_data.dtype

        if colname is not None:
            raise ValueError(f"Please set the argument '{arg_names[3]}' "
                             "to 'None'.")

        else:

            if data_type == old_type or old_type in data_type.str:
                try:
                    data_floated = obj_data.copy().astype(new_type)
                    return data_floated
                except:
                    raise TypeError(f"Cannot convert object to type '{new_type}'.")
            else:
                print("Returning object with its values' type unchanged.")
                return obj_data

def sort_values_externally(array, key=None, reverse=False,
                           axis=-1, order=None,
                           wantarray=False):
    
    """
    Function that sorts array values,
    using this time np.sort() or list.sort() method, depending on the case.
    It is intended to use especially in such cases where
    the simple use of sort() method would lead
    no other option than assigning a variable,
    which causes to return a generator.
    Of course, this function can be used however simple the case it is.
    
    Parameters
    ----------
    array : list or numpy.ndarray
          Array containing string, integer, float, etc. values,
          but all of the same semantic type.
    wantarray : bool
          Determines whether to return the sorted values
          in an array, otherwise the functions returns
          them in a list. Default behaviour is the latter one.
          
    Returns
    -------
    sorted_array : list or numpy.ndarray
          List or array of sorted values.
    """

    if isinstance(array, list):
        # Invoke the method without assigning a new variable #
        array.sort(key=None, reverse=reverse)

    elif isinstance(array, np.ndarray):
        array = np.sort(array, axis=axis, order=order)

    if wantarray:
        array = np.array(array)

    sorted_values = array.copy()
    return sorted_values


def count_unique_type_objects(list_of_objects):
    
    """
    Checks whether all objects contained in a given list are the same,
    for that iterating over the list, getting the type,
    make the list of types unique and checking its length.
    
    Parameters
    ----------
    list_of_objects : list
          List of whatever objects.
    
    Returns
    -------
    unique_type_list : list of types
          List containing the unique types of the objects in the list.
    lutl : int
          Length of the unique object type list.
    """
    
    unique_type_list = np.unique([str(type(element)) for element in list_of_objects])
    lutl = len(unique_type_list)
    
    return unique_type_list, lutl    
        

def select_array_elements(array, idx2access):

    """
    Function to select a slice of a 1D array or list.
    If dimension number is greater than one,
    then throws a warning indicating that.
    
    Parameters
    ----------
    array : list or numpy.ndarray
          List or array containing whatever values
    idx2access : int or list or numpy.ndarray
          List or array to select multiple values.
          If a single value is detected, 
          then it will be converted to list, because
          and integer object is not iterable.
    
    Returns
    -------
    slice : int or list or numpy.ndarray
          Single value or a slice of the input list or array
    """
    
    if isinstance(idx2access, int):
        idx2access = [idx2access]
    
    if isinstance(array, list):
        accessed_mapping = map(array.__getitem__, idx2access)
        accessed_list = list(accessed_mapping)
        
        lal = len(accessed_list)
        if lal == 1:
            accessed_list = accessed_list[0]
        return accessed_list
    
    elif isinstance(array, np.ndarray):
        accessed_array = array[idx2access]
        
        laa = len(accessed_array)
        if laa == 1:
            accessed_array = accessed_array[0]
        return accessed_array
    
    
def remove_elements_from_array(array, idx2access, axis=None):
    
    """
    Function that removes certain elements either from a list or numpy array,
    selected by indexes, which can be integers or booleans.
    
    Parameters
    ----------
    array : list or numpy.array
          List or array containing the values.
    idx2access : list or numpy.array of integers or booleans
          Object containing indexes used to select elements
          from the previous list or array.
          If ´array´ is of type list, then only a number is accepted.
    
    Returns
    -------
    array_filtered : numpy.ndarray
          NumPy's array with the selected elements removed.
    """
    
    if isinstance(array, list):
        array_filtered = array.copy()
        
        if not isinstance(idx2access, int):
            raise TypeError("For a list-type input argument, "\
                            "only an integer is accepted to index it.")
        else:
            array_filtered.pop(idx2access)
    
    elif isinstance(array, np.ndarray):
        array_filtered = np.delete(array, idx2access, axis=axis)
        
    else:
        raise TypeError("Input argument must either be of type ´list´ or numpy array.")
    
    
    return array_filtered