import sys
import pytesseract
import win32gui
from PyQt5 import QtGui, QtCore, uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

league_window_name = "League of Legends"



class MainWindow(QMainWindow):
    
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Currency Demystifyer")
        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.X11BypassWindowManagerHint
        )
        self.setGeometry(
            QtWidgets.QStyle.alignedRect(
            QtCore.Qt.LeftToRight, QtCore.Qt.AlignCenter,
            QtCore.QSize(220, 32),
            QtWidgets.qApp.desktop().availableGeometry()
        ))
    def get_window_rect(window_title):
        hwnd = win32gui.FindWindow(None, window_title)
        if hwnd:
            rect = win32gui.GetWindowRect(hwnd)
            return rect
        else:
            return None   

    def get_open_windows():
        windows = []

        def enum_windows_callback(hwnd, window_list):
            if win32gui.IsWindowVisible(hwnd):
                window_text = win32gui.GetWindowText(hwnd)
                if window_text:
                    window_list.append((hwnd, window_text))

        win32gui.EnumWindows(enum_windows_callback, windows)
        return windows
    
    def alignWindowToLoL(self):
        x,y,z,zz = get_window_rect(league_window_name)
        self.setGeometry(x,y,z,zz)

    def mousePressEvent(self, event):
        print('click!')
        #QtWidgets.qApp.quit()

   

