#------------------#
# Define functions #
#------------------#

def dict_value_basic_operator(dict1, dict2, basic_math_operator):

    """
    Performs the basic mathematical operations between two dictionaries.
    
    Parameters
    ----------
    dict1 : dict
          First dictionary containing some values.
    dict2 : dict
          Second dictionary containing some values.
    basic_math_operator : {'+', '-', '*', '/'}
    
    Returns
    -------
    Depending on the operation chosen:
    sum_dict : dict:
          Dictionary with summed values.
    subtr_dict : dict:
          Dictionary with subtracted values.
    mult_dict : dict:
          Dictionary with multiplied values.
    div_dict : dict:
          Dictionary with divided values.
    """

    if basic_math_operator == '+':
        sum_dict = {key:
                    dict1[key] + dict2[key]
                    for key in dict1.keys() & dict2}
        return sum_dict

    elif basic_math_operator == '-':
        subtr_dict = {key:
                      dict1[key] - dict2[key]
                      for key in dict1.keys() & dict2}
        return subtr_dict

    elif basic_math_operator == '*':
        mult_dict = {key:
                     dict1[key] * dict2[key]
                     for key in dict1.keys() & dict2}
        return mult_dict

    elif basic_math_operator == '/':
        div_dict = {key:
                    dict1[key] / dict2[key]
                    for key in dict1.keys() & dict2}
        return div_dict

    else:
        raise ValueError("Wrong operator sign.")

def merge_dictionaries(dict_list):
    
    ldl = len(dict_list)
    if ldl == 1:
        raise ValueError("2 dictionaries at least must be passed.")
    
    str2eval = "{"
    for d in dict_list:
        str2eval += f"**{d},"
    str2eval += "}"
    
    merged_dict = eval(str2eval)
    return merged_dict
