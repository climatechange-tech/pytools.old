#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Wed Feb  8 16:46:49 2023

@author: jonander
"""

import os

main_dir="/home/jonander/Pictures/2022"
dirlist=os.listdir(main_dir)
dirc=dirlist[0]

full_path=f"{main_dir}/{dirc}"
os.chdir(full_path)

fs=os.listdir()
fs.sort()

print(os.getcwd())
print(fs)
print(len(fs))

for f,i in zip(fs, range(1,0+len(fs)+1)):
    new_num=f"{i:02d}"
    ext=os.path.splitext(f)[-1]
    new_file=f"{new_num}{ext}"
    print(f,new_file)
    # os.rename(f,new_file)
    
    