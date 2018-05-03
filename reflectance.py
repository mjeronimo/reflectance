# 
# This program ... 
# 
#   TODO: description of the program
#   Purpose: automate reflectance calculation
#   The cal values are in "reflectance units"
#   Doing the reflectance takes a lot of time
#   Correlation between reflectance and red channel
#

import numpy as np
import cv2
import math

from matplotlib import pyplot as plt
from scipy import stats

#
# The extent of the x and y axes on the output graph
#
X_AXIS_MAX = 125
Y_AXIS_MAX = 255

# The reference template
template_filename = 'reference-images/Reflectance-Template-2.3.png'

# The target file to examine
target_filename = 'sample-images/220444813_1500.jpg'  # works
#target_filename = 'sample-images/220444813.JPG'      # works
#target_filename = 'sample-images/220441889.JPG'      # fails
#target_filename = 'sample-images/220445319.JPG'      # fails
#target_filename = 'sample-images/220445388.JPG'      # works

print "Processing '{}'".format(target_filename)

# Open the target image in grayscale and color
img_gray = cv2.imread(target_filename, 0)
img_color = cv2.imread(target_filename)

# Open the template in grayscale and color
ref_gray = cv2.imread(template_filename, 0)
ref_color = cv2.imread(template_filename)

#
# A class to represent a square on the target image
#
SIDE = 112
class Square:
	def __init__(self, name, parent, x, y, reflectance=0):
		self.name = name
		self.matrix = parent[y:y+SIDE,x:x+SIDE]
		self.shape = self.matrix.shape
		self.reflectance = reflectance

	def mode(self):
		return stats.mode(self.matrix, axis=None)[0][0]

	def show(self):
		cv2.imshow(self.name, self.matrix)

#
# White correction (optional for now)
#
#   To what extent is the image evently lit? 
#   Beginning of each session
# 	  Use a white sheet of same material
#	  Same camera setup
#	  Create a mask to use for subtraction
#
## TODO

#
# Correct for camera distorion
#
#   yml file, camera intrinsics, OpenCV
#
## TODO

#
# Image warping using SIFT feature matching and homography
#

# Create a SIFT feature detector
sift = cv2.xfeatures2d.SIFT_create()

# Find the keypoints and descriptors using SIFT
kp1,des1 = sift.detectAndCompute(img_gray, None)
kp2,des2 = sift.detectAndCompute(ref_gray, None)

FLANN_INDEX_KDTREE = 0

index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks = 50)

flann = cv2.FlannBasedMatcher(index_params, search_params)
matches = flann.knnMatch(des1,des2,k=2)

good = []

for m,n in matches:
   if m.distance < 0.7*n.distance:
      good.append(m)

# Find the homography and perform a warp of the target image to match the reference
# image perspective

MIN_MATCH_COUNT = 10

if len(good)>MIN_MATCH_COUNT:

  src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
  dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

  M,mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
  h,w = img_gray.shape
  template_h,template_w = ref_gray.shape

  result = cv2.warpPerspective(img_color,M,(w,h))[0:template_h,0:template_w]

#
# Get the squares in the target and reference images
# 

# Get the red channel for the target image and the reference image
img_rchannel = result[:, :, 2]
ref_rchannel = ref_color[:, :, 2]

# The calibration squares include their associated reflectance values
cal_01 = Square("cal_01", ref_rchannel, 169, 600, 3.4)
cal_02 = Square("cal_02", ref_rchannel, 169, 450, 4.2)
cal_03 = Square("cal_03", ref_rchannel, 169, 300, 8.9)
cal_05 = Square("cal_05", ref_rchannel, 319, 150, 11.0)
cal_06 = Square("cal_06", ref_rchannel, 469, 150, 20.2)
cal_07 = Square("cal_07", ref_rchannel, 619, 150, 36.8)
cal_09 = Square("cal_09", ref_rchannel, 769, 300, 44.3)
cal_10 = Square("cal_10", ref_rchannel, 769, 450, 70.0)
cal_11 = Square("cal_11", ref_rchannel, 769, 600, 100.2)

# The target image will use detected red channel values 
img_01 = Square("img_01", img_rchannel, 169, 600)
img_02 = Square("img_02", img_rchannel, 169, 450)
img_03 = Square("img_03", img_rchannel, 169, 300)
img_05 = Square("img_05", img_rchannel, 319, 150)
img_06 = Square("img_06", img_rchannel, 469, 150)
img_07 = Square("img_07", img_rchannel, 619, 150)
img_09 = Square("img_09", img_rchannel, 769, 300)
img_10 = Square("img_10", img_rchannel, 769, 450)
img_11 = Square("img_11", img_rchannel, 769, 600)

# Print the table of reflectance/R channel values
print 'Reflectance  R Channel Mode'
print '%8s' % cal_11.reflectance, '%12s' % img_11.mode()
print '%8s' % cal_10.reflectance, '%12s' % img_10.mode()
print '%8s' % cal_09.reflectance, '%12s' % img_09.mode()
print '%8s' % cal_07.reflectance, '%12s' % img_07.mode()
print '%8s' % cal_06.reflectance, '%12s' % img_06.mode()
print '%8s' % cal_05.reflectance, '%12s' % img_05.mode()
print '%8s' % cal_03.reflectance, '%12s' % img_03.mode()
print '%8s' % cal_02.reflectance, '%12s' % img_02.mode()
print '%8s' % cal_01.reflectance, '%12s' % img_01.mode()

# Create a merged image for display
alpha = 0.8
merged = (alpha * ref_color + (1 - alpha) * result).astype(dtype=np.uint8)

cv2.imshow('img_rchannel', img_rchannel)
cv2.imshow('merged', merged)

def second_largest(numbers):
    count = 0
    m1 = m2 = float('-inf')
    for x in numbers:
        count += 1
        if x > m2:
            if x >= m1:
                m1, m2 = x, m1            
            else:
                m2 = x
    return m2 if count >= 2 else None

def find_index(row, value):
    count = 0
    for val in row:
      if val == value:
        return count
      count += 1
    return None

circles = cv2.HoughCircles(img_rchannel, cv2.HOUGH_GRADIENT, 1, 100)

if circles is not None:
  circles = np.round(circles[0, :]).astype("int")

  for (x,y,r) in circles:
    mask = np.zeros((merged.shape[0], merged.shape[1]), dtype=np.uint8)
    cv2.circle(mask, (x,y), r, (1,1,1),-1,8,0) 
    out = img_rchannel * (mask.astype(merged.dtype))

    out[np.where(out==[0])] = [255]

    cv2.imshow('out', out)
    cv2.waitKey(0)

    histg = cv2.calcHist([out],[0],None,[256],[0,256])
    idx = second_largest(histg)

    r_channel_val = find_index(histg, idx)

    print "R Channel Mode of sample: ", r_channel_val

cv2.destroyAllWindows()

x = [cal_01.reflectance, cal_02.reflectance, cal_03.reflectance, cal_05.reflectance, cal_06.reflectance,
	cal_07.reflectance, cal_09.reflectance, cal_10.reflectance, cal_11.reflectance]

xi = np.array(x)

y = [img_01.mode(),img_02.mode(),img_03.mode(),img_05.mode(),img_06.mode(),
	img_07.mode(),img_09.mode(),img_10.mode(),img_11.mode()]

plt.axis([0, X_AXIS_MAX, 0, Y_AXIS_MAX])
plt.grid(True)
plt.plot(x, y, 'ro')

coefs = np.polyfit(x, y, 2)
polynomial = np.poly1d(coefs)

# Solve the quadratic equation for x

a = coefs[0]
b = coefs[1]
c = coefs[2]
y = float(r_channel_val)

d = (b**2)-(4*a*c)+(4*a*y)

sol1 = (-b - math.sqrt(d))/(2*a)
sol2 = (-b + math.sqrt(d))/(2*a)

reflectance_val = sol2 if (sol1 < 0 or sol1 > X_AXIS_MAX) else sol1
print "Reflectance of sample: {0:0.3f}".format(reflectance_val)

xs = np.arange(0.0, X_AXIS_MAX, 0.1)
ys = polynomial(xs)

# Display the table of results

equation_str = "y = {0:.3f}x^2 + {1:.3f}x + {2:.3f}".format(coefs[0], coefs[1], coefs[2])
str2 = "(x,y) = ({0:0.3f}, {1:0.3f})".format(reflectance_val, r_channel_val)
#title = "Reflectance vs R Channel Mode\n{}\n".format(target_filename)
title = "{}".format(target_filename)

plt.suptitle(title, fontsize=16)
plt.xlabel('Reflectance')
plt.ylabel('R Channel Mode')
plt.text(10, 225, equation_str, fontsize=12)
plt.text(10, 210, str2, fontsize=12)
plt.plot(xs, ys)
plt.axhline(y, 0.0, reflectance_val/X_AXIS_MAX, alpha=1.0, color='red', linestyle='dashed')
plt.axvline(reflectance_val, 0.0, y/Y_AXIS_MAX, alpha=1.0, color='red', linestyle='dashed')
plt.show()
