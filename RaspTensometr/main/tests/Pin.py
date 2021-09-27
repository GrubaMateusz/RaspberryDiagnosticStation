from PyQt5 import QtWidgets, QtGui, QtCore


class Pin(QtWidgets.QLabel):

    def __init__(self, parent=None):
        super(Pin, self).__init__(parent)


        im = QtGui.QPixmap("C:\\Users\\easym\\IdeaProjects\\RaspTensometr\\main\\view\\Pin.png")
        self.setPixmap(im)

