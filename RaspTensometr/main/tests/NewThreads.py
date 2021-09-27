import turtle
from random import uniform

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt, QObject, pyqtSignal
from PyQt5.QtGui import QBrush, QPainter, QColor, QFont, QPixmap, QPen
import time
import threading
from PyQt5.QtWidgets import QLabel, QWidget


class Clock(QtWidgets.QLabel):

    def __init__(self, parent=None):
        super(Clock, self).__init__(parent)

        self.im = QtGui.QPixmap("C:\\Users\\easym\\IdeaProjects\\RaspTensometr\\main\\images\\clock.png")
        #       for PI im = QtGui.QPixmap("/home/pi/Desktop/MyProjectPyton/RaspTensometrs/main/view/clock.png")

        self.setPixmap(self.im)
    #  self.setGeometry(70, 300, im.width(), im.height())


class Pin(QtWidgets.QLabel):

    def __init__(self, parent=None):
        super(Pin, self).__init__(parent)

        self.im = QtGui.QPixmap("C:\\Users\\easym\\IdeaProjects\\RaspTensometr\\main\\images\\Pin.png")

        #        im = QtGui.QPixmap("/home/pi/Desktop/MyProjectPyton/RaspTensometrs/main/view/Pin.png")
        self.setPixmap(self.im)
    # self.setGeometry(168,315,im.width(),im.height())


class Mens(QtCore.QThread):
    trigger = pyqtSignal(float)


    def __init__(self,parent=None):
        QtCore.QThread.__init__(self,parent)

        self.counter = 0
        self.varTab = []
        self.var = 0
        self.threadState = True

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True  # Daemonize thread
        thread.start()

    def valueChanged(self, tab =[]):

        tab = self.varTab
        return tab



    def run(self):
        """ Method arledy runs forever """

        while self.threadState == True:
            # Simple simulate cell
            self.counter = self.counter + 1
            self.var = int(uniform(0.1, 5000.0))
            self.varTab.append(self.var)

            print('Doing something imporant in the background', self.counter, self.varTab)
            time.sleep(0.4)

class Communicate(QObject):

    updateMens = pyqtSignal(float)

class CarBreakerUp(QWidget):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setWindowTitle("CarBreaker")
        self.setWindowIcon(QtGui.QIcon("C:\\Users\\easym\\IdeaProjects\\RaspTensometr\\main\\images\\lo6go.png"))
        self.saveValue = 0
        self.saveValueTable = []
        self.grapgSaveValue = 0
        self.leftPaintBar = 0
        self.cilickSave = 0
        self.setMinimumWidth(600)
        self.setMinimumHeight(600)
        self.setGeometry(600, 600, 600, 600)
        self.setStyleSheet("QWidget {background-color:rgba(0,37,59,255);} QScrollBar:horizontal {width: 1px; height: "
                           "1px;background-color: rgba(0,37,59,255);} QScrollBar: vertical {width: 1px; height: "
                           "1px;background-color: rgba(0,37,59,255);}")

        # Clock left:

        self.clockL = Clock(self)
        self.clockL.setGeometry(70, 100, self.clockL.im.width(), self.clockL.im.height())
        self.pinL = Pin(self)
        self.pinL.setGeometry(168, 115, self.pinL.im.width(), self.pinL.im.height())

        # Clock right:

        self.clockR = Clock(self)
        self.clockR.setGeometry(600 - 70 - self.clockR.im.width(), 100, self.clockR.im.width(), self.clockR.im.height())
        self.pinR = Pin(self)
        self.pinR.setGeometry(600 - 168 - self.pinR.im.width(), 115, self.pinR.im.width(), self.pinR.im.height())

        # Butons
        self.startTens = QtWidgets.QPushButton(self)
        self.startTens.setStyleSheet("background-color:rgba(70,241,44)")
        self.startTens.setText("Start")
        self.startTens.setGeometry(100, 300, 150, 50)
        self.startTens.setCheckable(True)
        self.startTens.clicked.connect(lambda: self.startMensClickEv())

        self.btnGraf = QtWidgets.QPushButton(self)
        self.btnGraf.setStyleSheet("background-color:rgba(204, 255, 102)")
        self.btnGraf.setText("Draw graph")
        self.btnGraf.setGeometry(100, 400, 150, 50)
        self.btnGraf.setCheckable(True)

        self.btnGraf.clicked.connect(lambda: self.startGraphClickEv())
       # self.mensurment = Mens()


    def startGraphClickEv(self):
        self.grapgSaveValue = self.grapgSaveValue + 20
        print("graph click", self.grapgSaveValue)
        #self.saveValueTable.append(self.mensurment.var)
        print("table: ", self.saveValueTable)

    def startMensClickEv(self):
        self.saveValue = self.saveValue + 10
        #self.saveValue = int(self.mensurment.var / 10)
        #self.cilickSave = self.cilickSave + 1
        print("count clicks:", self.cilickSave)
        print("val:", self.saveValue)


    def paintEvent(self, event):

        qp = QPainter()
        qp.begin(self)
        self.drowWidged(qp)
        qp.end()





    def drowWidged(self, qp):
        ox = 40
        oy = 500

        #   Left bar

        qp.setPen(QColor(204, 255, 102))
        qp.setBrush(QColor(204, 255, 102))
        qp.drawRect(10, 50, ox, oy)

        qp.setPen(QColor(153, 102, 255))
        qp.setBrush(QColor(153, 102, 255))
        qp.drawRect(13, oy + 52 - self.saveValue, ox - 6, 1 + self.saveValue)


        #   Right bar

        qp.setPen(QColor(204, 255, 102))
        qp.setBrush(QColor(204, 255, 102))
        qp.drawRect(540, 50, ox, oy)

        qp.setPen(QColor(153, 102, 255))
        qp.setBrush(QColor(153, 102, 255))
        qp.drawRect(543, oy + 52 - self.grapgSaveValue, ox - 6, 1 + self.grapgSaveValue)

        self.update()

class RunApp(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.communicateM = Communicate()
        self.mensTable = []
        self.wid = CarBreakerUp()
        self.mens = Mens()




        self.wid.show()
        self.repaint()

    def updateChangeValue(self, val):


        print("xXXXXXXXXXXXXXXXXXXXXXXXXXXXXx")



# Run app segment:

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    desktop = QtWidgets.QApplication.desktop()
    resolution = desktop.availableGeometry()
    myapp = RunApp()
    myapp.setWindowOpacity(0.97)

    myapp.move(resolution.center() - myapp.rect().center())
    # tut = Mens()

    sys.exit(app.exec_())
else:
    desktop = QtWidgets.QApplication.desktop()
    resolution = desktop.availableGeometry()
