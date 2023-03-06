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
kpIndexFilename = 'Kp_2012_2021_Kyoto.dat'
outputHeader = "YYYY-MM-DD\tKp"

# ... File Names ...
epoch_string = ["SolarMax", "SolarMid", "SolarMin"]
season_string = ["Winter", "Summer", "OffSeason"]
activity_string = ["NoActivity", "LowDisturbance", "Disturbed"]

# --- Initialize arrays ---
kpIndexUnixTime = []
kpIndexValues = []

# -- OUTPUT structure [i,j] vectors in vectors ---
# --- [epoch[season[activity]]]
output = [
    [[[], [], []], [[], [], []], [[], [], []]],
    [[[], [], []], [[], [], []], [[], [], []]],
    [[[], [], []], [[], [], []], [[], [], []]]
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
        # kpSum = HelperRoutines.kp_classification(kp)
        kpSum = int(kp)/10

        for j in range(3, 21, 3):
            kpIndexDataRow = kpIndexStringData[i + j]
            [year, doy, hour, kp] = kpIndexDataRow.split()
            # kpSum += HelperRoutines.kp_classification(kp)
            kpSum += int(kp)/10

        output_i = HelperRoutines.epoch_index(cycleMoments, kpIndexDateTime.timestamp())

        if output_i >= 0:
            output_j = HelperRoutines.season_index(kpIndexDateTime.month)
            output_k = HelperRoutines.activity_index(kpSum)
            kpSum = '%.2f' % kpSum
            output[output_i][output_j][output_k].append("\t".join([kpIndexDateTime.strftime("%Y-%m-%d"), kpSum]))

for i in range(0, 3):
    for j in range(0, 3):
        for k in range(0, 3):
            HelperRoutines.print_list(outputPath, "".join([epoch_string[i], season_string[j], activity_string[k]]),
                                      outputHeader, output[i][j][k])

print("Success!")
