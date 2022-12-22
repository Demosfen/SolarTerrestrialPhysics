#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This simple script compares substorm onsets 
listed in ASCII file(s) with Kp-index.

--- HOW TO USE ---

1. Download Kp indexes from https://omniweb.gsfc.nasa.gov/form/dx1.html
    (please uncheck all checkboxes and check "Kp*10 Index") 
    
2. Change "kpIndexFilename" variable (line 119)
        according to the name of the downloaded Kp-index file ;
        
3. Put Kp-index data file to ../data directory;

4. Put your substorm onsets list to ../lists directory;
    (download list here: https://supermag.jhuapl.edu/substorms/?tab=download)

5. Change "substormListNames" list variable (line 117)
        according to the name(s) of your substorm(s) list(s);
        
6. Change header of the output file (if needed) (line 101-106)
        
6. Launch the script.

--- Data formats ---

1. No need to change Kp-index data file from OMNIweb;

2. Example of Date and Time columns in the list file:
       '2013 02 13 14 32 ...'
3. This script ignores all other columns and append corresponding Kp
       to the end of the line.
4. If you want to comment some lines in your onsets list,
       use "#" sign at the beginning of the line.

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

# --- Epoch and Substorm onset compare ---
def EpochIndex(cycle,time):
    
    k = -1
    
    for i in range(len(cycle)):
        if int(time) in range(int(cycle[i][0]),int(cycle[i][1]),50):
            k = i
        
    return k

# --- Season search ---
            
def SeasonIndex(month):
    
    if month in range(3,6) or month in range(9,12):
        return 2    # off-season
    elif month in range(6,9):
        return 1    # Summer
    else:
        return 0    # Winter

# --- Print list ---
def PrintList(path, name, outputHeader, toPrint):
    
    file = open(path+name+'.lst','w')
    file.write(outputHeader)
    file.write('\n')
    
    for line in toPrint:
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
outputHeader = "# The standard Kp values look like 0, 0+, 1-, 1, 1+, 2-, ... \n\
# but are stored as Kp = 0, 3, 7, 10, 13, 17, ... in the OMNI data set. \n\
# OMNI have mapped 0+ to 3, 1- to 7, 1 to 10, 1+ to 13, 2- to 17, etc. \n\
# For example Kp = 7+ is coded as 73; Kp = 7- is coded as 77; Kp = 7 as 70 \n\
# \n\
#Date      Time   Kp"

# -- OUTPUT structure [i,j] vectors in vectors ---
output = [
          [ [],[],[] ],
          [ [],[],[] ],
          [ [],[],[] ]
         ]
    
currentFolder = str(pathlib.Path(__file__).parent.resolve())[:-srcFolderNameLenght]

substormListNames = ['substorms-ohtani-20120101_000000_to_20211231_235900.ascii']

kpIndexFilename = 'Kp_2012_2021.dat'

substormListsPath = [currentFolder + 'lists/' + name for name in substormListNames]

kpIndexPath = currentFolder + 'data/' + kpIndexFilename

# === List generator settings ===

cycleMoments = [[datetime(2013, 6, 1).timestamp(),datetime(2014, 8, 1).timestamp()],
                [datetime(2015, 3, 1).timestamp(),datetime(2016, 8, 1).timestamp()],
                [datetime(2018, 6, 1).timestamp(),datetime(2020, 1, 1).timestamp()]]

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
            
            i = EpochIndex(cycleMoments,substormUnixTime)
            
            if i >= 0:
                
                j = SeasonIndex(int(dataRow[1]))
                
            # --- Merging substorm with concurrent Kp-index value ---
            # --- and writing down the output to the list ---
            
                try:
                    i_kp = kpIndexUnixTime.index(substormUnixTime)
                    kpIndexValue = kpIndexValues[i_kp]
                    output[i][j].append("  ".join([substormOnset.rstrip('\n'), kpIndexValue]))
                    
                except ValueError:
                    print("There is no Kp-index for: " + substormOnset)
                    output[i][j].append("  ".join([substormOnset.rstrip('\n'), "NaN"]))
    
    outputPath = currentFolder+'output/'
    
    PrintList(outputPath,'SolarMaximumWinter',outputHeader,output[0][0])
    PrintList(outputPath,'SolarMaximumSummer',outputHeader,output[0][1])
    PrintList(outputPath,'SolarMaximumOffSeason',outputHeader,output[0][2])
    PrintList(outputPath,'SolarMidWinter',outputHeader,output[1][0])
    PrintList(outputPath,'SolarMidSummer',outputHeader,output[1][1])
    PrintList(outputPath,'SolarMidOffSeason',outputHeader,output[1][2])
    PrintList(outputPath,'SolarMinimumWinter',outputHeader,output[2][0])
    PrintList(outputPath,'SolarMinimumSummer',outputHeader,output[2][1])
    PrintList(outputPath,'SolarMinimumOffSeason',outputHeader,output[2][2])
    
    del output[:][:]
