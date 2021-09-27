from random import uniform

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PyQt5.QtGui import QBrush, QPainter, QColor, QFont, QPixmap,QLinearGradient
from PyQt5.QtWidgets import QLabel, QWidget, QSizePolicy
import time
import threading
import sys
import RPi.GPIO as GPIO
from hx711 import HX711
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


#   Class responsible for meansure in the background
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
                self.var =int( hx.get_weight(1))
               # print(self.var)
                self.varTab.append(self.var)
                self.trigger.emit(int(self.var))

                time.sleep(0.00001)
            except (KeyboardInterrupt, SystemExit):
                print("end")
#   Plot dynamic canvas
class PlotDynamicCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)

        plt.rcParams.update({'font.size': 7})

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.data = []

    def plot(self,var):

        if(var <=0):
            self.data.append(0)
        else:

            self.data.append(var/100)

        ax = self.figure.add_subplot(111)

        ax.plot(self.data, 'r-')
        ax.set_title('Siła nacisku [N]')


        self.draw()

#   Creating static canvas
class PlotStaticCanvas(FigureCanvas):
    def __init__(self, parent=None, width=1, height=1, dpi=144):
        fig = Figure(figsize=(width, height), dpi=dpi)

        plt.rcParams.update({'font.size': 7})

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.data = []
    def plot(self,var):

        if(var <=0):
         self.data.append(0)
        else:
           self.data.append(var)

        ax = self.figure.add_subplot(111)

        ax.plot(self.data, 'r-')

        ax.set_title('Siła nacisku [N]')

#   Canvas static Window
class CanvasWindow(QWidget):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setWindowTitle("Pomiar sily hamowania [N]")
        #self.setWindowIcon(QtGui.QIcon("C:\\Users\\easym\\IdeaProjects\\RaspTensometr\\main\\images\\lo6go.png"))
        self.windowWidth = 800
        self.windowHeight = 600
        self.move(20,20)
        self.setStyleSheet("QWidget {background-color:rgba(0,37,59,255);} QScrollBar:horizontal {width: 1px; height: "
                           "1px;background-color: rgba(0,37,59,255);} QScrollBar: vertical {width: 1px; height: "
                           "1px;background-color: rgba(0,37,59,255);}")


        self.setMinimumWidth(800)
        self.setMinimumHeight(600)
        self.plotCanvas = PlotDynamicCanvas(self, width=8, height=7)  #3,2
        self.plotCanvas.move(10,10)    #370,251







class CarBreakerUp(QWidget):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setWindowTitle("CarBreaker")
       # self.setWindowIcon(QtGui.QIcon("C:\\Users\\easym\\IdeaProjects\\RaspTensometr\\main\\images\\lo6go.png"))
        self.windowWidth = 800
        self.windowHeight = 600
        self.move(20,20)

        self.saveValue = 1
        self.saveValueTable = []
        self.grapgSaveValue = 0
        self.leftPaintBar = 0
        self.cilickSave = 0
        self.setMinimumWidth(800)
        #self.setMinimumHeight(600)
        self.setMaximumHeight(600)
        self.setStyleSheet("QWidget {background-color:rgba(0,37,59,255);} QScrollBar:horizontal {width: 1px; height: "
                           "1px;background-color: rgba(0,37,59,255);} QScrollBar: vertical {width: 1px; height: "
                           "1px;background-color: rgba(0,37,59,255);}")
#   Butons
        self.startTens = QtWidgets.QPushButton(self)

        self.startTens.setStyleSheet("background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgb(61, 217, 245), stop:1 rgb(178, 255, 102));"+
                                    "font-weight: bold; border-radius:25px;")
        self.startTens.setText("Start")
        self.startTens.setGeometry(110, 350, 150, 50)    #(70, 350, 150, 50)
        self.startTens.setCheckable(True)
        self.startTens.clicked.connect(lambda: self.startMensClickEv())

        self.btnGraf = QtWidgets.QPushButton(self)
        self.btnGraf.setStyleSheet("background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgb(61, 217, 245), stop:1 rgb(240,248,255));"+
                                   "font-weight: bold; border-radius:25px;")
        self.btnGraf.setText("Draw graph")
        self.btnGraf.setGeometry(110, 410, 150, 50)  #70, 410, 150, 50
        self.btnGraf.setCheckable(True)

        self.btnGraf.clicked.connect(lambda: self.startGraphClickEv())

#   Start Thread Meansurment and update interface
        self.mensurment = Mens()
        self.mensurment.trigger.connect(self.updateGui)
#   Graph
#   Graph SIZE in main window:
        self.plotCanvas = PlotDynamicCanvas(self, width=4, height=2.6)   #3,2
        self.plotCanvas.move(self.windowWidth-470,self.windowHeight-320)  #370 ,251

       # self.mensurment.trigger.connect(self.plotCanvas.plot)

    def updateGui(self,var):
        self.saveValue = var
        self.update()


    def startGraphClickEv(self):
        self.grapgSaveValue = self.grapgSaveValue + 20
        print("graph click", self.grapgSaveValue)
        #self.saveValueTable.append(self.mensurment.var)
        print("table: ", self.saveValueTable)
        self.fileSave = open("SaveMensurmentValue.txt","w")

        var = "\n".join(str(e) for e in self.mensurment.varTab)
        self.fileSave.write(var)
        self.fileSave.close()
        tempTab = self.mensurment.varTab

        self.canvasStaticWindow = CanvasWindow()
        for i in tempTab:
            self.canvasStaticWindow.plotCanvas.plot(i)
        tempTab.clear()

        #self.canvasStaticWindow.plotCanvas.plot(self.saveValue)


        self.canvasStaticWindow.show()

    def startMensClickEv(self):

        self.cilickSave = self.cilickSave + 1

        if(self.cilickSave%2 == 1):
            self.startTens.setText("Stop")
            self.startTens.setStyleSheet("background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgb(61, 217, 245), stop:1 rgb(255,51,51));"+
                                         "font-weight: bold; border-radius:25px;")
            self.mensurment.trigger.connect(self.plotCanvas.plot)
        else:
            self.startTens.setText("Start")
            self.startTens.setStyleSheet("background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgb(61, 217, 245), stop:1 rgb(178, 255, 102));"+
                                         "font-weight: bold; border-radius:25px;")

            self.mensurment.trigger.disconnect()

    def paintEvent(self, event):

        qp = QPainter()
        qp.begin(self)
        self.drowWidged(qp)
        qp.end()





    def drowWidged(self, qp):
        ox = 40                     # Width bar
        oy = 500                    # Height bar
        changeValueForClock = int(self.mensurment.var)
        if(0 > changeValueForClock):
            changeValueForClock = 0
        if(self.cilickSave%2 == 0):
            changeValue = 0
        else:
            changeValue = int(self.mensurment.var / 10)

        qp.setRenderHints(qp.Antialiasing)
        #   Left analog clock
        r = QtCore.QRect(110,40,20,20)                              #   create rectangle
        size = r.size()                                             #   get rectangle size
        r.setSize(size*10)                                          #   set size
        startAngle = 310*16                                         #   set start angle to draw arc
        endAngle = 280*16                                           #   set end arc angle
        menStartAngle = 225*16
        mensEndAngle = 5*16
        qp.setPen(QtGui.QPen(QtGui.QColor(255,240,255), 11))        #   arc color
        qp.setFont(QFont("Arial",15))
        qp.drawText(100,240,"0 [N]")
        qp.drawText(290,240,"50 [N]")
        printValue = "0.000 [N]"
        if(changeValueForClock>=0):
            printValue = str(changeValueForClock/100)+" [N]"
            qp.drawText(180,150,printValue)
        else:
            qp.drawText(180,150,printValue)

        qp.drawArc(r, startAngle, endAngle)
        qp.setPen(QtGui.QPen(QtGui.QColor(255,5,0), 5))
        if(changeValueForClock >= 0):

            qp.drawArc(r,menStartAngle-changeValueForClock,mensEndAngle+changeValueForClock)

            #qp.drawChord(r,startAngle,endAngle+changeValueForClock)
        else:
            qp.drawArc(r,menStartAngle,mensEndAngle)



        #   Right analog clock


        r = QtCore.QRect(self.windowWidth-280,40,20,20)                              #   create rectangle
        size = r.size()                                             #   get rectangle size

        r.setSize(size*10)                                          #   set size
        startAngle = 310*16                                         #   set start angle to draw arc
        endAngle = 280*16                                           #   set end arc angle
        menStartAngle = 225*16
        mensEndAngle = 5*16
        qp.setPen(QtGui.QPen(QtGui.QColor(255,240,255), 11))        #   arc color
        qp.drawArc(r, startAngle, endAngle)
        qp.setPen(QtGui.QPen(QtGui.QColor(255,5,0), 5))
        if(changeValueForClock >= 0):

            qp.drawArc(r,menStartAngle-changeValueForClock,mensEndAngle+changeValueForClock)
            #qp.drawChord(r,startAngle,endAngle+changeValueForClock)
        else:
            qp.drawArc(r,menStartAngle,mensEndAngle)



        #   Left bar

        qp.setPen(QColor(204, 255, 102))
        brush = QBrush(Qt.HorPattern)

        grad = QLinearGradient(0,0,0,400)
        grad.setColorAt(0.6, QColor(51,255,51))     #GREEN
        grad.setColorAt(0.8, QColor(255,213,71))    #ORANGE
        grad.setColorAt(0.95, QColor(255,51,51))     #RED
        qp.setBrush(QBrush(grad))

        qp.drawRect(10, 50, ox, oy)

        qp.setPen(QColor(255,255,255))              #Dynamic bar
        qp.setBrush(QColor(80,80,255,90))
        if(changeValue > 400):
            qp.setBrush(QColor(254,5,5,90))
        qp.drawRect(13, oy + 52 - changeValue, ox - 6, 1 + changeValue)
        qp.drawRect(13, oy + 52 - changeValue, ox - 6, 1 + changeValue)


        qp.setPen(QColor(255,255,255))
        qp.setBrush(QColor(255,255,255))

        qp.drawText(63,oy+52,"[0 N]")
        qp.drawRect(58,oy+45,3,2)
        qp.drawText(63,oy-184,"[25 N]")
        qp.drawRect(58,oy-193,3,2)
        qp.drawText(63,oy-442,"[50 N]")
        qp.drawRect(58,oy-449,3,2)



        #   Right bar

        qp.setPen(QColor(204, 255, 102))
        qp.setBrush(QBrush(grad))
        qp.drawRect(self.windowWidth-50,50,ox,oy)

        qp.setPen(QColor(255,255,255))        #Dynamic bar
        qp.setBrush(QColor(80,80,255,90))
        if(changeValue > 100):
            qp.setBrush(QColor(254,5,5,90))
        qp.drawRect(self.windowWidth-47, oy + 52 - changeValue, ox - 6, 1 + changeValue)

        self.update()


class RunApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):

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
