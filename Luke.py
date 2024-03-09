import sys
from PyQt5 import QtGui, QtCore, uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
import Richie


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Currency Demystifyer")
        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.X11BypassWindowManagerHint
        )
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # sets the window to cover RP
        rect = Richie.league_window_offset(932, 18, 995, 42)
        self.setGeometry(rect[0], rect[1], rect[2] - rect[0], rect[3] - rect[1])

    def mousePressEvent(self, event):
        print('click!')
        QtWidgets.qApp.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    layout = QtWidgets.QVBoxLayout()
    mywindow = MainWindow()
    
    label = QtWidgets.QLabel("0", mywindow)
    label.setStyleSheet(
        "color: #F0E6D2; background-color: #010710; padding-left: 2px; padding-bottom: 5px; font-size: 14px; font-weight: bold;")
    label1 = QtWidgets.QLabel("0", mywindow)


    layout.addWidget(label)
    layout.addWidget()
    mywindow.show()
    app.exec_()