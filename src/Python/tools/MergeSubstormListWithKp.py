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

5. Change "substormListNames" list variable in line 77
        according to the name(s) of your substorm(s) list(s);
        
6. Change header of the output file (if needed) in line 72
        
6. Launch the script.

--- Data formats ---

1. No need to change Kp-index data file from omniweb;

2. Your substorm onset list(s) should start with Date and Time columns:
   - Year, Month and Day should be separated with "-" symbol;
   - Hours, Minutes and Seconds should be separated with ":" symbol;
   - In Time column can be only Hours or Hours and Minutes;
   - Date and Time columns should be separated with whitespace.
   - Example of Date and Time columns:
       2013-02-13 14:32:34
   - This script ignores all other columns and add corresponding Kp
       as the last column.
   - If you want to comment ssome lines in your onsets list,
       use "#" sign at the end of line.

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

substormListNames = ['SolarMinimum20132015.dat', 
                     'SolarUprising20162017.dat', 
                     'SolarMaximum20192020.dat']

kpIndexFilename = 'Kp_2013_2019.dat'

substormListsPath = [currentFolder + 'lists/' + name for name in substormListNames]

kpIndexPath = currentFolder + 'data/' + kpIndexFilename

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
            [substormDate, substormTime] = substormOnset.split()
            substormHour = substormTime.split(':')[0]
            
            try:
                substormUnixTime = datetime.strptime(substormDate + ' ' + substormHour, '%Y-%m-%d %H').timestamp()
                
            except ValueError:
                substormUnixTime = datetime.strptime(substormDate + ' ' + substormHour, '%m/%d/%Y %H').timestamp()
                
            # --- Merging substorm with concurrent Kp-index value ---
            # --- and writing down the output to the list ---
            
            try:
                i = kpIndexUnixTime.index(substormUnixTime)
                kpIndexValue = kpIndexValues[i]
                
                output.append("  ".join([substormOnset.rstrip('\n')[:-secondsCut], kpIndexValue]))
                
            except ValueError:
                print("There is no Kp-index for: " + substormOnset)
                output.append("  ".join([substormOnset.rstrip('\n')[:-secondsCut], "NaN"]))
    
    # --- Printing output for corresponding substorm list ---
                
    file = open(currentFolder+'/output/'+substormListPath.lstrip(currentFolder+'lists/')[:-extensionLenght]+'_plusKp.dat','w')
    file.write(outputHeader)
    file.write('\n')
    for line in output:
        file.write(line)
        file.write('\n')
    file.close()
