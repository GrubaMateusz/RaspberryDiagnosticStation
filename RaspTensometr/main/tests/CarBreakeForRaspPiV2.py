from random import uniform

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PyQt5.QtGui import QBrush, QPainter, QColor, QFont, QPixmap
from PyQt5.QtWidgets import QLabel, QWidget, QSizePolicy
import time
import threading
import sys
import RPi.GPIO as GPIO
from hx711 import HX711
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class Clock(QtWidgets.QLabel):

    def __init__(self, parent=None):
        super(Clock, self).__init__(parent)

        #self.im = QtGui.QPixmap("C:\\Users\\easym\\IdeaProjects\\RaspTensometr\\main\\images\\clock.png")
        self.im = QtGui.QPixmap("/home/pi/Desktop/MyProjectPyton/RaspTensometr/main/images/clock.png")

        self.setPixmap(self.im)
    #  self.setGeometry(70, 300, im.width(), im.height())


class Pin(QtWidgets.QLabel):

    def __init__(self, parent=None):
        super(Pin, self).__init__(parent)

        #self.im = QtGui.QPixmap("C:\\Users\\easym\\IdeaProjects\\RaspTensometr\\main\\images\\Pin.png")

        self.im = QtGui.QPixmap("/home/pi/Desktop/MyProjectPyton/RaspTensometr/main/images/Pin.png")
        self.setPixmap(self.im)
    # self.setGeometry(168,315,im.width(),im.height())


class Mens(QtCore.QThread):
    trigger = pyqtSignal(int)


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
        hx = HX711(5,6)
        hx.set_reading_format("MSB", "MSB")
        hx.set_reference_unit(91)
        hx.tare()
        print("start Thread")

        while True:
            try:
                hx.reset()
                self.var = hx.get_weight(1)
                print(self.var)
                self.varTab.append(self.var)
                self.trigger.emit(int(self.var))
                time.sleep(0.00001)
            except (KeyboardInterrupt, SystemExit):
                print("end")

class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        #self.axes = fig.add_subplot(111)
        plt.rcParams.update({'font.size': 7})
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        #self.plot()
        self.data = []

    def plot(self,var):

        if(var <=0):
            self.data.append(0)
        else:
            self.data.append(var)

        ax = self.figure.add_subplot(111)

        ax.plot(self.data, 'r-')
        ax.set_title('Siła nacisku [N]')
        self.draw()


class CarBreakerUp(QWidget):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setWindowTitle("CarBreaker")
        self.setWindowIcon(QtGui.QIcon("C:\\Users\\easym\\IdeaProjects\\RaspTensometr\\main\\images\\lo6go.png"))
        self.windowWidth = 600
        self.windowHeight = 600

        self.saveValue = 1
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
        self.startTens.setGeometry(70, 290, 150, 50)
        self.startTens.setCheckable(True)
        self.startTens.clicked.connect(lambda: self.startMensClickEv())

        self.btnGraf = QtWidgets.QPushButton(self)
        self.btnGraf.setStyleSheet("background-color:rgba(204, 255, 102)")
        self.btnGraf.setText("Draw graph")
        self.btnGraf.setGeometry(70, 350, 150, 50)
        self.btnGraf.setCheckable(True)

        self.btnGraf.clicked.connect(lambda: self.startGraphClickEv())

        # Start Thread Meansurment and update interface
        self.mensurment = Mens()
        self.mensurment.trigger.connect(self.updateGui)
        #Graph

        self.m = PlotCanvas(self, width=3, height=2)
        self.m.move(self.windowWidth-370,self.windowHeight-251)
        self.mensurment.trigger.connect(self.m.plot)

    def updateGui(self,var):
        self.saveValue = var
        self.update()


    def startGraphClickEv(self):
        self.grapgSaveValue = self.grapgSaveValue + 20
        print("graph click", self.grapgSaveValue)
        #self.saveValueTable.append(self.mensurment.var)
        print("table: ", self.saveValueTable)

    def startMensClickEv(self):
        #self.saveValue = self.saveValue + 10
        self.saveValue = self.mensurment.var
        self.cilickSave = self.cilickSave + 1
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
        changeValue = int(self.saveValue / 10)
        #   Left bar

        qp.setPen(QColor(204, 255, 102))
        qp.setBrush(QColor(204, 255, 102))
        qp.drawRect(10, 50, ox, oy)

        qp.setPen(QColor(153, 102, 255))
        qp.setBrush(QColor(153, 102, 255))
        if(changeValue > 400):
            qp.setBrush(QColor(254,5,5))
        qp.drawRect(13, oy + 52 - changeValue, ox - 6, 1 + changeValue)
        qp.drawRect(13, oy + 52 - changeValue, ox - 6, 1 + changeValue)


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


        self.mensTable = []
        self.wid = CarBreakerUp()





        self.wid.show()
        self.repaint()



# Run app segment:

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    desktop = QtWidgets.QApplication.desktop()
    resolution = desktop.availableGeometry()
    myapp = RunApp()
    myapp.setWindowOpacity(0.97)

    myapp.move(resolution.center() - myapp.rect().center())


    sys.exit(app.exec_())
else:
    desktop = QtWidgets.QApplication.desktop()
    resolution = desktop.availableGeometry()
