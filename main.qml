import QtQuick 2.5

Item {
  id: root
  width: 240
  height: 240

  signal clicked

  property alias source: image.source

  property int centerX: 100
  property int centerY: 0
  property int radius: 80 

  property bool positionLocked: false
  property bool nudging: false

  MouseArea {
    cursorShape: Qt.CrossCursor
    anchors.fill: parent
	hoverEnabled: true
	onClicked: {
	  positionLocked = true
	  nudging = true
	  okButton.visible = true
    }
	onPositionChanged: {
	  if (!positionLocked) {
	    centerX = mouse.x
	    centerY = mouse.y
	    canvas.requestPaint()
	  }
	}
	onPressed: {
	  positionLocked = false
	}
	onReleased: {
	  positionLocked = true
	}
  }
  
  Image {
    id: image
	source: "./reference-images/Reflectance-Template-2.3.png"
  }

  Button {
    id: okButton
	visible: false
    width: 100
    height: 50
	x: parent.width/2 - width/2
	y: parent.height - 100
	bgColor: "blue"
	text: "OK"
	opacity: 0.5

	onClicked: {
	  root.clicked()
	}
  }

  Canvas {
    id: canvas
    anchors.fill: parent
	focus: true

    onPaint: {
      var ctx = getContext("2d")
      ctx.reset()
      ctx.beginPath()
      ctx.fillStyle = "rgba(255,0,0,0.5)"
      ctx.moveTo(centerX, centerY)
      ctx.arc(centerX, centerY, radius, 0, 2*Math.PI, false)
      ctx.lineTo(centerX, centerY)
      ctx.fill()
    }

    Keys.onPressed: {
      if (event.key == Qt.Key_Left) {
        centerX--
        event.accepted = true;
      }
	  else if (event.key == Qt.Key_Right) {
        centerX++
        event.accepted = true;
      }
	  else if (event.key == Qt.Key_Up) {
        if (event.modifiers & Qt.ControlModifier) {
		  if (radius >= 1) {
		    radius++
		  }
        }
		else {
          centerY--
        }
        event.accepted = true;
      }
	  else if (event.key == Qt.Key_Down) {
        if (event.modifiers & Qt.ControlModifier) {
		  if (radius >= 1) {
		    radius--
		  }
        }
		else {
          centerY++
        }
        event.accepted = true;
      }

	  canvas.requestPaint()
    }
  }
}
