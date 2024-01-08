# -*- coding: utf-8 -*-

#-------------------------#
# Define custom functions #
#-------------------------#

def format_string(format_string, arg_obj):
    if isinstance(arg_obj, tuple):
        formatted_string = format_string.format(*arg_obj)
        return formatted_string
    
    elif isinstance(arg_obj, dict):
        formatted_string = format_string.format(**arg_obj)
        return formatted_string
    
    elif not isinstance(arg_obj, tuple) and not isinstance(arg_obj, dict):
        formatted_string = format_string.format(arg_obj)
        return formatted_string
    
    else:
        raise TypeError(typeErrorStr1)


def print_format_string(string2format, arg_obj, end="\n"):
    try:
        formatted_string = format_string(string2format, arg_obj)
        print(formatted_string, end=end)
    except:
        raise TypeError(typeErrorStr2)

    
def print_percent_string(string2format, arg_obj):
    if isinstance(arg_obj, str):
        print(string2format %(arg_obj))
    else:
        raise TypeError(typeErrorStr2)

#--------------------------#
# Parameters and constants #
#--------------------------#

typeErrorStr1 = "Argument must either be of type alphanumeric, ´tuple´ or ´dict´."
typeErrorStr2 = "Argument must be of type ´str´ only."
