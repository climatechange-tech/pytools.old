#-------------------------#
# Define custom functions #
#-------------------------#

# Quality control functions #
#---------------------------#

def check_input_number_format(x):
    if isinstance(x, int):    
        x_str = str(x)
    else:
        x_str = x
    return x_str

def method_checker(method_list, arg):
    if arg not in method_list:
        raise ValueError(f"Wrong method. Options are {method_list}.")
        
# Operations with frequently used bases #
#---------------------------------------#

# Bases: 2, 8, 10, 16
def base2bin(n, method="fstring", zero_pad=4):
    method_checker(method_opts, method)

    if method == "default":
        n_bin = bin(n)
    elif method == "fstring":
        n_bin = f"{n:0{zero_pad}b}"
    return n_bin

def base2oct(n, method="fstring", zero_pad=4):
    method_checker(method_opts, method)

    if method == "default":
        n_oct = oct(n)
    elif method == "fstring":
        n_oct = f"{n:0{zero_pad}o}"
    return n_oct

def base2hex(n, method="fstring", zero_pad=4):
    method_checker(method_opts, method)

    if method == "default":
        n_hex = hex(n)
    elif method == "fstring":
        n_hex = f"{n:0{zero_pad}h}"
    return n_hex
    

# From above bases to decimal #
def bin2dec(n_bin):
    if isinstance(n_bin, int):
        n = n_bin
    else:
        int(n_bin, base=2)
    return n

def oct2dec(n_oct):
    if isinstance(n_oct, int):
        n = n_oct
    else:
        int(n_oct, base=8)
    return n

def hex2dec(n_hex):
    if isinstance(n_hex, int):
        n = n_hex
    else:
        int(n_hex, base=16)
    return n

    
# Operations with arbitrary bases #
#---------------------------------#
    
# From arbitrary base to decimal #
def arbBase2Dec(x, base=10):
    x = check_input_number_format(x)
    n = int(x, base=base)
    return n
    
# Conversions among arbitrary bases #
def conv_arbBases(x, base):
    x = check_input_number_format(x)
    y = int(x, base=base)
    return y
    
    
# Local parameters #
#------------------#

method_opts = ['default', 'fstring']