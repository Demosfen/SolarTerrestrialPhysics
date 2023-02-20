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
