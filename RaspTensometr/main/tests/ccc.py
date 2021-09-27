import os
from functools import partial

import cups

import sip

import time
from PyQt5 import QtCore, QtWidgets



class Ui_MainWindow(object):

    def setupBasics(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1024, 600)
        MainWindow.setWindowTitle("Prepack Print Station")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(910, 10, 90, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("Reload")
        self.pushButton.clicked.connect(self.on_click)

        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(0, 50, 1027, 541))
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(False)
        self.scrollArea.setObjectName("scrollArea")

        MainWindow.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.setupDynamics()



    def setupDynamics(self):

        self.scrollAreaWidgetContents = QtWidgets.QWidget()

        rows = len(sql.get_prepacks()) / 5
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1027, rows * 280))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")



        self.show_cartons()

    def on_click(self):
        self.refresh()

    def show_cartons(self):
        i = 0
        z = 20
        y = 20

        pre_packs = sql.get_prepacks()
        for p in pre_packs:

            pz = 35
            py = 30

            # Box
            self.frame = QtWidgets.QFrame(self.scrollAreaWidgetContents)
            self.frame.setGeometry(QtCore.QRect(z, y, 150, 200))
            self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.frame.setFrameShadow(QtWidgets.QFrame.Raised)

            # Prepack ID
            self.label = QtWidgets.QLabel(self.frame)
            self.label.setGeometry(QtCore.QRect(pz, py, 100, 20))
            self.label.setText(str(p[0]))

            py = py + 40

            # Altcode

            self.label_2 = QtWidgets.QLabel(self.frame)
            self.label_2.setGeometry(QtCore.QRect(pz, py, 100, 20))
            self.label_2.setText(str(p[1]))

            py = py + 40

            # Colour

            self.label_3 = QtWidgets.QLabel(self.frame)
            self.label_3.setGeometry(QtCore.QRect(pz, py, 100, 20))
            self.label_3.setText(str(p[2]))

            py = py + 40

            # Button

            self.p_button = QtWidgets.QPushButton(self.frame)
            self.p_button.setGeometry(QtCore.QRect(10, py, 130, 40))
            self.p_button.setText("Print " + str(p[3]) + " Labels")
            self.p_button.clicked.connect(partial(self.print_clicked, str(p[0])))

            z = z + 180
            i = i + 1

            if i == 5:
                z = 20
                i = 0
                y = y + 230

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.scrollArea.repaint()

    def print_clicked(self, pp):
        labels = sql.get_labelsforprepack(pp)
        conn = cups.Connection()
        totallabels = len(labels)
        alloccode = labels[0][1]
        bcode = barcode.get('code39', str(alloccode), writer=ImageWriter())
        filename = bcode.save('bcode')
        conn.printFile("USB", filename, "Test", {"copies":  str(totallabels)})

        sql.insert_print_record(alloccode)

        for l in labels:
            sql.insert_carton(str(l[0]), str(l[1]))

        self.refresh()

    def refresh(self):

        d = self.scrollAreaWidgetContents.children()
        e = reversed(d)

        for g in e:
            g.deleteLater()

        self.scrollAreaWidgetContents.deleteLater()
        self.setupDynamics()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupBasics(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())