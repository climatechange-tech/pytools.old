#-------------------------#
# Define custom functions #
#-------------------------#

def print_fstring(format_string, arg_tuple):
    print(format_string.format(*arg_tuple))
        
def print_percent_string(format_string, arg_tuple):
    print(format_string %(arg_tuple))