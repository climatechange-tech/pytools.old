#-------------------------#
# Define custom functions #
#-------------------------#

# Decimal to other bases #
#------------------------#

"""
This operations involve the following operations:
    -Decimal to:
        --> binary ('b', base 2)
        --> octal ('o', base 8)
        --> hexadecimal ('x', base 16)
"""

# TODO: sartu strings/information_output_formatters.py programako menpekotasuna
# TODO: aurrekoagatik, aukerak moldatu

def dec2bin(n, zero_pad=None, custom_fmt_str=None):
    
    if custom_fmt_str is None:
        n_bin = f"{n:b}"
    else:
        n_bin = "zuzenean, f-string-a aplikatzen duen funtzioa"
    
def dec2oct(n, zero_pad=None, custom_fmt_str=None):
    
    
def dec2hex(n, zero_pad=None, custom_fmt_str=None):

# Conversions among other bases #
#-------------------------------#

# Frequently used #
def specBase2Bin(n, zero_pad=None, custom_fmt_str=None):
    f"{0b11:b}"
    f"{0o27:b}"
    f"{0x16:b}"
    
def specBase2Oct(n, zero_pad=None, custom_fmt_str=None):
    f"{0b11:o}"
    f"{0o27:o}"
    f"{0x16:o}"
    
def specBase2Dec(n, zero_pad=None, custom_fmt_str=None):
    f"{0b11:d}"
    f"{0o27:d}"
    f"{0x16:d}"
    
    # int("36", [2,8,16])
    
def specBase2Hex(n, zero_pad=None, custom_fmt_str=None):
    f"{0b11:x}"
    f"{0o27:x}"
    f"{0x16:x}"

# Arbitrary bases #
def arbSpecBase2Dec(x, base=10):
    
    if isinstance(x, int):    
        x_str = str(x)
    else:
        x_str = x
    y = int(x_str, base=base) # int("2", 7)
    
    

    
