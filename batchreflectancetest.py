# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 12:20:06 2018

@author: spph-mainlab
"""

from reflectanceauto2 import reflectancecalculator
import sys
import glob
import os
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)

# Get name of images to process
imgs = glob.glob('sample-images/1/*.jpg')

for img in imgs:
    currentimage = cv2.imread(img)
    reflectancecalculator(app, currentimage, img)
