# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 12:20:06 2018

@author: spph-mainlab
"""

from reflectanceauto2 import reflectancecalculator
import glob
import os
import cv2
import numpy as np
#

#set working directory
os.chdir('c:/program files/reflectance method/reflectance/sample-images/1/')

# Get images
imgs = glob.glob('*.jpg')
#imgs.extend(glob.glob('*.jpeg'))

for img in imgs:
    #currentimagegray = cv2.imread(img,0)
    currentimage = cv2.imread(img)
#    cv2.imshow('Current Image',currentimage)
#    cv2.waitKey(0)
#    cv2.destroyAllWindows()
#This last step doesn't work yet.  
    reflectancecalculator(currentimage)

