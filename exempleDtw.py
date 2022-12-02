#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
installation :
    
    pip3 install dtaidistance
    pip3 install --global-option=--noopenmp dtaidistance

Created on Tue Nov 29 13:08:42 2022
@author: hfchame
"""

from dtaidistance import dtw
from dtaidistance import dtw_visualisation as dtwvis
import numpy as np


## A noisy sine wave as query
idx = np.linspace(0,np.pi*6,num=100)
s1 = np.sin(idx) + np.random.uniform(size=100)/10.0

## A cosine is for template; sin and cos are offset by 25 samples
s2 = np.cos(idx)

path = dtw.warping_path(s1, s2)
#path = dtw.warping_path(template, query)
dtwvis.plot_warping(s1, s2, path, filename="warp.png")

distance = dtw.distance(s1, s2)
print(distance)
