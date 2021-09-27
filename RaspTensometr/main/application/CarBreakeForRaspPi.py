from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QPainter, QColor, QFont, QPixmap
from PyQt5.QtWidgets import QLabel
import time
import threading
import sys
import RPi.GPIO as GPIO
from hx711 import HX711

class Clock(QtWidgets.QLabel):

    def __init__(self, parent=None):
        super(Clock, self).__init__(parent)

#        im = QtGui.QPixmap("C:\\Users\\easym\\IdeaProjects\\RaspTensometr\\main\\view\\clock.png")
        im = QtGui.QPixmap("/home/pi/Desktop/MyProjectPyton/RaspTensometrs/main/view/clock.png")

        self.setPixmap(im)



class Pin(QtWidgets.QLabel):

    def __init__(self, parent=None):
        super(Pin, self).__init__(parent)

        #im = QtGui.QPixmap("C:\\Users\\easym\\IdeaProjects\\RaspTensometr\\main\\view\\Pin.png")

        im = QtGui.QPixmap("/home/pi/Desktop/MyProjectPyton/RaspTensometrs/main/view/Pin.png")
        self.setPixmap(im)

class Mens():
    def __init__(self, interval=1):
        self.interval = interval
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True  # Daemonize thread
        thread.start()

    def run(self):
        """ Method that runs forever """
        hx = HX711(5,6)
        hx.set_reading_format("MSB", "MSB")
        hx.set_reference_unit(100)
        print("start Thread")
        
        while True:
            # Mensure

            
            hx.reset()
            hx.tare()
        
            val = hx.get_weight(5)
            print(val)
            hx.power_down()
            hx.power_up()

            time.sleep(0.2)
        
    def runTens(self):
        
        referenceUnit = 1
        hx = HX711(5,6)
        hx.set_reading_format("MSB", "MSB")
        hx.set_reference_unit(100)
        hx.reset()
        hx.tare()
        
        val = hx.get_weight(5)
        print(val)
        hx.power_down()
        hx.power_up()
   
 
        
    
    
    


class CarBreakerUp(QtWidgets.QWidget):

    
        

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setWindowTitle("CarBreaker")
      #  self.setWindowIcon(QtGui.QIcon("C:\\Users\\easym\\IdeaProjects\\RaspTensometr\\main\\view\\lo6go.png"))
        self.setMinimumWidth(600)
        self.setMinimumHeight(600)
        self.setStyleSheet("QWidget {background-color:rgba(0,37,59,255);} QScrollBar:horizontal {width: 1px; height: "
                           "1px;background-color: rgba(0,37,59,255);} QScrollBar: vertical {width: 1px; height: "
                           "1px;background-color: rgba(0,37,59,255);}")

        # Clocks:
        self.clockL = Clock(self)
        self.pinL = Pin(self)
        self.pinL3 = QtWidgets


        self.clockR = Clock(self)
        self.pinR = Pin(self)

        
        # adding layout grid
      #  self.layoutG = QtWidgets.QGridLayout()

    #    self.layoutG.addWidget(self.clockL, 0, 1, 1, 1)
    #    self.layoutG.addWidget(self.clockR, 0, 5, 1, 1)
    #    self.layoutG.addWidget(self.pinR, 1, 5, 1, 1)
     #   self.layoutG.addWidget(self.pinL, 1, 1, 1, 1)

     #   self.setLayout(self.layoutG)

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        qp.setPen(QColor(Qt.blue))
        qp.drawLine(10,100,100,100)
        qp.drawRect(10,150,150,100)


        qp.end()

# Run app segment:

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    desktop = QtWidgets.QApplication.desktop()
    resolution = desktop.availableGeometry()
    myapp = CarBreakerUp()
    myapp.setWindowOpacity(0.97)
    myapp.show()
    myapp.move(resolution.center() - myapp.rect().center())
    
    mens = Mens()
    
    sys.exit(app.exec_())
else:
    desktop = QtWidgets.QApplication.desktop()
    resolution = desktop.availableGeometry()
