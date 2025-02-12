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
import datetime

app = QApplication(sys.argv)

csvname = "Reflectance "+datetime.datetime.today().strftime("%m-%d-%Y")

print("Saving results to:" + csvname)

# Get name of images to process - specify directory to look in
imgs = glob.glob('sample-images/1/*.jpg')

for img in imgs:
    currentimage = cv2.imread(img)
    reflectancecalculator(app, currentimage, img, csvname)
