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
        raise TypeError("Argument must either be of type alphanumeric, ´tuple´ or ´dict´.")


def print_format_string(string2format, arg_obj):
    try:
        formatted_string = format_string(string2format, arg_obj)
        print(formatted_string)
    except:
        raise TypeError("Argument must either be of type alphanumeric, ´tuple´ or ´dict´.")

    
def print_percent_string(string2format, arg_obj):
    if isinstance(arg_obj, str):
        print(string2format %(arg_obj))
    else:
        raise TypeError("Argument must be of type ´str´ only.")
