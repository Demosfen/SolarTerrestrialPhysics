#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 20:41:21 2022

@author: alexander
"""

# === Import libs ===

import os
#from datetime import datetime
import pathlib

# === Def's section ===

# --- Read ASCII file ---
def io(path):
    file = open(path,'r')
    data = file.readlines() # vector of the data (line-by-line, string format)
    file.close()
    return data

# === Default variables ===

srcFolderNameLenght = 3
    
currentFolder = str(pathlib.Path(__file__).parent.resolve())[:-srcFolderNameLenght]

substormListNames = ['SolarMinimum20132014.dat', 
                 'SolarUprising20162017.dat', 
                 'SolarMaximum20192020.dat']

substormListsPath = [currentFolder + 'lists/' + name for name in substormListNames]

kpPath = currentFolder + 'data/'+'Kp/'+'2013_2019.dat'

# ====================== Main ==============================

# --- Check and create output folder ---

if not os.path.exists(currentFolder+'output/'):
    print("Create /output folder...")
    os.makedirs(currentFolder+'output')

# --- Reading data ---

for i in range (len(substormListsPath)):
    
    substormsDateTimeStringData = io(substormListsPath[i])
