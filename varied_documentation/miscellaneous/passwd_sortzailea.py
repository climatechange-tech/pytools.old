import numpy as np

lower = 50
upper = 150
size_1d = 50

chars = []

ns = np.random.randint(lower,upper,size=size_1d)
len_ns = len(ns)

for n in range(len_ns):
    char = chr(ns[n])
    chars.append(char)

delim = ""
chars = delim.join(chars)

print("Automatikoki sortutako pasahitza:",chars)

