#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This simple script classifies daily activity using Kp thresholds.
They are:
    No activity: Sum(Kp) <= 15
    Weak-to-moderate activity: 15 < Sum(Kp) < 24
    Disturbed conditions: Kp >= 24
--- HOW TO USE ---
1. ...
Created on Mon Feb 20 10:32:14 2023
@author: Alexander Nikolaev
"""

import os
from datetime import datetime
import pathlib
from HelperRoutines import io
from HelperRoutines import kp_classification as kpclass

# --- Common Settings ---
dataFileCommentedRow = "#"
srcFolderNameLength = 35
kpIndexFilename = 'Kp_2012_2021.dat'

# --- Initialize arrays ---
kpIndexUnixTime = []
kpIndexValues = []

# -- OUTPUT structure [i,j] vectors in vectors ---
output = [
    [[], [], []],
    [[], [], []],
    [[], [], []]
]

# --- SubRoutines ---
currentFolder = str(pathlib.Path(__file__).parent.resolve())[:-srcFolderNameLength]
kpIndexPath = currentFolder + 'data/' + kpIndexFilename

# === List generator settings ===
cycleMoments = [[datetime(2013, 6, 1).timestamp(), datetime(2014, 8, 1).timestamp()],
                [datetime(2015, 3, 1).timestamp(), datetime(2016, 8, 1).timestamp()],
                [datetime(2018, 6, 1).timestamp(), datetime(2022, 1, 1).timestamp()]]

# --- Run() ---
kpIndexStringData = io(kpIndexPath)

for kpIndexDataRow in kpIndexStringData:

    try:
        kpIndexDataRow.index(dataFileCommentedRow)

    except ValueError:
        [year, doy, hour, kp] = kpIndexDataRow.split()
        kpIndexUnixTime.append(datetime.strptime(year + '-' + doy + '-' + hour, '%Y-%j-%H').timestamp())
        kpIndexValues.append(kpclass(kp))
