import os
import sys

from OpenGL import GL

import PyQt5

from PyQt5 import QtQuick
from PyQt5 import QtCore
from PyQt5 import QtQml
from PyQt5.QtQuick import QQuickView
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QDesktopWidget
from PIL import Image

class ManualDetector:
  def __init__(self, app):
    # Instance the application once

    self.app = app

  def getFilterInfo(self, filename):
    # Create the QML user interface
    view = QQuickView()
    view.setSource(QUrl('main.qml'))
    view.setResizeMode(QQuickView.SizeRootObjectToView)

    # Set the window size and location according the size of the input image
    
    im = Image.open(filename)
    width, height = im.size

    qtRect = view.frameGeometry()
    centerPoint = QDesktopWidget().availableGeometry().center()

    new_x = centerPoint.x() - width/2
    new_y = centerPoint.y() - height/2

    print("New_x: ", new_x);
    print("New_y: ", new_y);

    view.setGeometry(new_x, new_y, width, height)
    view.setTitle(filename)
    #view.setFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint)
    view.show()

    # Grab the root QML object so we can wire up the quit signal
    rootObject = view.rootObject()
    rootObject.clicked.connect(QtCore.QCoreApplication.instance().quit)

	# Also, set the input image filename
    rootObject.setProperty("source", "file:" + filename)

    # Run the UI to collect the x,y,radius data
    self.app.exec_()

    # Retrieve the results form the QML object
    x = rootObject.property("centerX")
    y = rootObject.property("centerY")
    radius = rootObject.property("radius")

    # Package it up for return
    return (x,y,radius)
