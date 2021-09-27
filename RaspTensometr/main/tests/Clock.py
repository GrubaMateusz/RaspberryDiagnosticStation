from PyQt5 import QtWidgets, QtGui


class Clock(QtWidgets.QLabel):

    def __init__(self, parent=None):
        super(Clock, self).__init__(parent)


        im = QtGui.QPixmap("C:\\Users\\easym\\IdeaProjects\\RaspTensometr\\main\\view\\clock.png")
        self.setPixmap(im)


