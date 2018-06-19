import sys
from detector import ManualDetector
from PyQt5.QtWidgets import QApplication

# This needs to be done first. Couldn't find a way to put it in the ManualDetector
app = QApplication(sys.argv)

# Create the ManualDetector which will be used for successive images
detector = ManualDetector(app)

# Specify a list of input filenames. This could be a set of files
# in a particular directory, for example. Just hardcode a few filenames
# here to demonstrate
filenames = ['reference-images/Reflectance-Template-2.3.png', 'mt-hood.png']


# For each filename call getFilterInfo to get and display the filter data
for filename in filenames:
  (centerX, centerY, radius) = detector.getFilterInfo(filename)
  print("Info for '", filename, "'")
  print("  centerX: ", centerX)
  print("  centerY: ", centerY)
  print("  radius: ", radius)

sys.exit(0)
