#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This simple script compares substorm onsets 
listed in ASCII file(s) with Kp-index.

--- HOW TO USE ---

1. Download Kp indexes from https://omniweb.gsfc.nasa.gov/form/dx1.html
    (please uncheck all checkboxes and check "Kp*10 Index") 
    
2. Change "kpIndexFilename" variable in line 81 
        according to the name of the downloaded Kp-index file ;
        
3. Put Kp-index data file to ../data directory;

4. Put your substorm onsets list to ../lists directory;
    (download list here: https://supermag.jhuapl.edu/substorms/?tab=download)

5. Change "substormListNames" list variable in line 77
        according to the name(s) of your substorm(s) list(s);
        
6. Change header of the output file (if needed) in line 72
        
6. Launch the script.

--- Data formats ---

1. No need to change Kp-index data file from omniweb;

2. Your substorm onset list(s) should start with Date and Time columns:
   - Year, Month and Day should be separated with whitespace;
   - Hours, Minutes and Seconds should be separated with whitespace;
   - Date and Time columns should be separated with whitespace.
   - Example of Date ad Time columns:
       2013 02 13 14 32
   - This script ignores all other columns and add corresponding Kp
       as the last column.
   - If you want to comment some lines in your onsets list,
       use "#" sign at the beginning of line.

-------------------

@author: Alexander Nikolaev
"""

# === Import libs ===

import os
from datetime import datetime
import pathlib

# === Def's section ===

# --- Read ASCII file ---
def io(path):
    file = open(path,'r')
    data = file.readlines() # vector of the data (line-by-line, string type)
    file.close()
    return data

# --- Matching def ---
def season(month):
    if month in range(3,5) or month in range(9,11):
        
            
    

# --- Print list ---
def PrintList(path, name, outputHeader,output):
    file = open(path+name+'.lst','w')
    file.write(outputHeader)
    file.write('\n')
    for line in output:
        file.write(line)
        file.write('\n')
        file.close()

# === Default variables ===

srcFolderNameLenght = 3
extensionLenght = 4
secondsCut = 3
dataFileCommentedRow = "#"
kpIndexUnixTime = []
kpIndexValues = []
outputHeader = "Date       Time   Kp"
output = []
    
currentFolder = str(pathlib.Path(__file__).parent.resolve())[:-srcFolderNameLenght]

substormListNames = ['substorms-ohtani-20120101_000000_to_20211231_235900.ascii']

kpIndexFilename = 'Kp_2012_2021.dat'

substormListsPath = [currentFolder + 'lists/' + name for name in substormListNames]

kpIndexPath = currentFolder + 'data/' + kpIndexFilename

# === List generator settings ===

minimumStart = datetime(2018, 6, 1).timestamp()
minimumEnd = datetime(2020, 1, 1).timestamp()
maximumStart = datetime(2013, 6, 1).timestamp()
maximumEnd = datetime(2014, 8, 1).timestamp()
midStart = datetime(2015, 3, 1).timestamp()
midEnd = datetime(2016, 8, 1).timestamp()

# --- suffix section ---

solarMinEq = []
solarMinWin = []
solarMinSum = []
solarMaxEq = []
solarMaxWin = []
solarMaxSum = []
solarMidEq = []
solarMidWin = []
solarMidSum = []


# ====================== Main ==============================

# --- Check and create output folder ---

if not os.path.exists(currentFolder+'output/'):
    print("Create /output folder...")
    os.makedirs(currentFolder+'output')
    
# --- Reading Kp-index data ---

kpIndexStringData = io(kpIndexPath)

for kpIndexRow in kpIndexStringData:
    
    try:
        kpIndexRow.index(dataFileCommentedRow)
        
    except ValueError:
        [year, doy, hour, kp] = kpIndexRow.split()
        kpIndexUnixTime.append(datetime.strptime(year+'-'+doy+'-'+hour, '%Y-%j-%H').timestamp())
        kpIndexValues.append(kp) 

# --- Reading substorm lists ---

for substormListPath in substormListsPath:
    
    substormOnsets = io(substormListPath)
    
    for substormOnset in substormOnsets:
        
        try:
            substormOnset.index(dataFileCommentedRow)
            
        except ValueError:
            dataRow = substormOnset.split()
            substormDate = dataRow[0]+'-'+dataRow[1]+'-'+dataRow[2]
            substormTime = dataRow[3]+':'+dataRow[4]
            substormHour = dataRow[3]
            substormOnset = substormDate + ' ' + substormTime
            substormUnixTime = datetime.strptime(substormDate + ' ' + substormHour, '%Y-%m-%d %H').timestamp()
            
            if (substormUnixTime in range(maximumStart, maximumEnd)):
                
                
            # --- Merging substorm with concurrent Kp-index value ---
            # --- and writing down the output to the list ---
            
            try:
                i = kpIndexUnixTime.index(substormUnixTime)
                kpIndexValue = kpIndexValues[i]
                
                output.append("  ".join([substormOnset.rstrip('\n'), kpIndexValue]))
                
            except ValueError:
                print("There is no Kp-index for: " + substormOnset)
                output.append("  ".join([substormOnset.rstrip('\n')[:-secondsCut], "NaN"]))
    
    del output[:]
