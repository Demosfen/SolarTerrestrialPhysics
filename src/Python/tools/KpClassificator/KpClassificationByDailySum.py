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
import HelperRoutines

# --- Common Settings ---
dataFileCommentedRow = "#"
srcFolderNameLength = 35
kpIndexFilename = 'Kp_2012_2021.dat'
outputHeader = "YYYY-MM-DD\tKp"

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
outputPath = currentFolder + 'output/'

# === List generator settings ===
cycleMoments = [[datetime(2013, 6, 1).timestamp(), datetime(2014, 8, 1).timestamp()],
                [datetime(2015, 3, 1).timestamp(), datetime(2016, 8, 1).timestamp()],
                [datetime(2018, 6, 1).timestamp(), datetime(2022, 1, 1).timestamp()]]

# --- Run() ---
kpIndexStringData = HelperRoutines.io(kpIndexPath)

for i in range(0, len(kpIndexStringData), 24):

    kpIndexDataRow = kpIndexStringData[i]

    try:
        kpIndexDataRow.index(dataFileCommentedRow)

    except ValueError:
        [year, doy, hour, kp] = kpIndexDataRow.split()
        kpIndexDateTime = datetime.strptime(year + '-' + doy + '-' + hour, '%Y-%j-%H')
        kpSum = HelperRoutines.kp_classification(kp)

        for j in range(3, 21, 3):
            kpIndexDataRow = kpIndexStringData[i + j]
            [year, doy, hour, kp] = kpIndexDataRow.split()
            kpSum += HelperRoutines.kp_classification(kp)

        output_i = HelperRoutines.epoch_index(cycleMoments, kpIndexDateTime.timestamp())

        if output_i >= 0:
            output_j = HelperRoutines.season_index(kpIndexDateTime.month)
            output[output_i][output_j].append("\t".join([kpIndexDateTime.strftime("%Y-%m-%d"), str(kpSum)]))

    HelperRoutines.print_list(outputPath, 'SolarMaximumWinter_KpSum', outputHeader, output[0][0])
    HelperRoutines.print_list(outputPath, 'SolarMaximumSummer_KpSum', outputHeader, output[0][1])
    HelperRoutines.print_list(outputPath, 'SolarMaximumOffSeason_KpSum', outputHeader, output[0][2])
    HelperRoutines.print_list(outputPath, 'SolarMidWinter_KpSum', outputHeader, output[1][0])
    HelperRoutines.print_list(outputPath, 'SolarMidSummer_KpSum', outputHeader, output[1][1])
    HelperRoutines.print_list(outputPath, 'SolarMidOffSeason_KpSum', outputHeader, output[1][2])
    HelperRoutines.print_list(outputPath, 'SolarMinimumWinter_KpSum', outputHeader, output[2][0])
    HelperRoutines.print_list(outputPath, 'SolarMinimumSummer_KpSum', outputHeader, output[2][1])
    HelperRoutines.print_list(outputPath, 'SolarMinimumOffSeason_KpSum', outputHeader, output[2][2])

    print("Success!")
