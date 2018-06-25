#!/usr/bin/env python
__author__ = 'Alex Galea'

''' Script to resize all files in current directory,
    saving new .jpg and .jpeg images in a new folder. '''


# This resizes images to be an appropriate size/type for the detector. Folder is set manually.

import cv2
import glob
import os
import numpy as np

#set working directory
os.chdir('c:/users/jeronimo/pictures/centre 2/')

# Get images
imgs = glob.glob('*.jpg')
imgs.extend(glob.glob('*.jpeg'))

print('Found files:')
print(imgs)

#desired width
width = 1500
print('Resizing all images to be %d pixels wide' % width)

folder = 'resized'
if not os.path.exists(folder):
    os.makedirs(folder)

# Iterate through resizing and saving
for img in imgs:
    pic = cv2.imread(img, cv2.IMREAD_UNCHANGED)
    height = int(width * pic.shape[0] / pic.shape[1])
    pic = cv2.resize(pic, (width, height))
    cv2.imwrite(folder + '/' + 'resized_' + img, pic)
    print(pic.dtype)