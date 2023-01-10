# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 19:37:43 2022

GOES #15 List compiler. Collects all the names of
quicklook plots and generates List_l0.dat, containing only
dates.

@author: Alexander
"""

import os
from datetime import datetime
import pathlib

currentFolder = str(pathlib.Path(__file__).parent.resolve())
currentFolder = currentFolder[:len(currentFolder)-6].replace("\\", '/')

fileNames = os.listdir(currentFolder+'lists/GOESevents/')

dates = [datetime.strptime(fileName[-17:-9], '%Y%m%d').strftime('%Y-%m-%d/%H:%M:%S') for fileName in fileNames]

listHeader = 'YYYY MM DD HH MN    UNIXtime   dHZ     E/P   disp  gr/sh   dtMPB   dMPB    dtSCW   Iscw'

file = open(currentFolder+'lists/GOES15List_l0.dat','w')
file.write(listHeader)
file.write('\n')
for line in dates:
    file.write(line)
    file.write('\n')
file.close()

""" TODO: download CDFs and extract electron fluxes

os.environ["CDF_LIB"] = 'C:/Program Files/CDF_Distribution/cdf38_1-dist/'
import spacepy.pycdf as cdf

dataFilePaths = ['f:/Injections_vs_DIP/data/GOES/'+
                 date[0:4]+'/goes15_eps-maged_1min_'+
                 date[0:6] + '_v01.cdf' for date in dates]
"""
