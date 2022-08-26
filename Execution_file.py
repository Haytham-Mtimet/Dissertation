# -*- coding: utf-8 -*-
"""
Created on Sat Jul 23 23:16:27 2022

@author: hm21396
"""

import subprocess

# This is our shell command, executed by Popen.

file1 = open('search_tweet.txt', 'r')
Lines = file1.readlines()
for line in Lines :
    #print(line)
    p = subprocess.run(line, stdout=subprocess.PIPE, shell=True)

print(p.communicate())