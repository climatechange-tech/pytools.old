#-------------------------#
# Define custom functions #
#-------------------------#

def print_fstring(format_string, arg_obj):
    if isinstance(arg_obj, str):
        print(format_string.format(arg_obj))
    elif isinstance(arg_obj, tuple):
        print(format_string.format(*arg_obj))
    elif isinstance(arg_obj, dict):
        print(format_string.format(**arg_obj))
    else:
        raise TypeError("Argument must either be of type ´str´, ´tuple´ or ´dict´.")
    
def print_percent_string(format_string, arg_obj):
    if isinstance(arg_obj, str):
        print(format_string %(arg_obj))
    else:
        raise TypeError("Argument must be of type ´str´ only.")
    
