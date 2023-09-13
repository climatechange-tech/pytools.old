#----------------#
# Import modules #
#----------------#

import numpy as np

#------------------#
# Input parameters #
#------------------#

# Unicode string indexes #
lower_char_idx = 31
upper_char_idx = 127

# Length of the password #
passwd_len = 16

# Output info elements #
key_expl = "Automatically generated password"
lke = len(key_expl)
hashtag_underliner = '#' * lke

#------------------------#
# Construct the password #
#------------------------#

# Get the corresponding unicode string list #
chars_glob = [chr(i) for i in range(lower_char_idx, upper_char_idx)]
lcg = len(chars_glob)

# Define random numbers ranging from 0 to the length of the list #
random_idx = np.random.randint(lcg, size=passwd_len)

# Select unicode strings according to these random numbers #
char_randomsel_list = [chars_glob[j] for j in random_idx]

# Convert the list to string #
delim = ""
passwd = delim.join(char_randomsel_list)

print(f"{key_expl}\n{hashtag_underliner}\n{passwd}")
