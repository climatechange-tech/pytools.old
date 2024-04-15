#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

import numpy as np

#------------------#
# Define functions #
#------------------#

def generate_automated_password(lower_char_idx,
                                upper_char_idx,
                                password_length):

    # Parameters #
    #------------#
    
    # Output info elements #
    key_expl = "Automatically generated password"
    lke = len(key_expl)
    hashtag_underliner = '#' * lke
    
    # List delimiter #
    delim = ""
    
    # Construct the password #
    #------------------------#
    
    # Get the corresponding unicode string list #
    chars_glob = [chr(i) for i in range(lower_char_idx, upper_char_idx)]
    lcg = len(chars_glob)
    
    # Define random numbers ranging from 0 to the length of the list #
    random_idx = np.random.randint(lcg, size=password_length)
    
    # Select unicode strings according to these random numbers #
    char_randomsel_list = [chars_glob[j] for j in random_idx]
    
    # Convert the list to string #
    passwd = delim.join(char_randomsel_list)
    
    # Output the password with formatted printing #
    passwd_str = f"{key_expl}\n{hashtag_underliner}\n{passwd}"
    return passwd_str
    
#--------------------#
# Call the functions #
#--------------------#

automated_passwd = generate_automated_password(31, 127, 16)
print(automated_passwd)