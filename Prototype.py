import pytesseract
from PyQt5 import QtGui, QtCore, uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
import win32gui
import sys
from PIL import ImageGrab, ImageOps


# Replace the string with your tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

league_window_name = "League of Legends"

poss = [[722, 316, 722, 316],[922, 316, 922, 316],[722, 516, 722, 516],[922, 516, 922, 516]]

# This list was written with the assumption that no single item will cost more than 4500 RP.    
# First RP then price in USD with no tax.
usd_RP = [[575, 4.99], [1380, 10.99], [2800, 21.99], [4500, 34.99]]


def get_RP():
    return read_number(league_window_offset(932, 18, 995, 42))
    # read_number(get_window_rect(league_window_name))


def get_default_shop_prices():
    w = 32
    l = 17
    holder = []
    #read_number(league_window_offset(725, 521, 725 + w, 521 + l))
    holder.append(read_number(league_window_offset(722, 316, 722 + w, 316 + l)))
    holder.append(read_number(league_window_offset(922, 316, 922 + w, 316 + l)))
    holder.append(read_number(league_window_offset(722, 516, 722 + w, 516 + l)))
    holder.append(read_number(league_window_offset(922, 516, 922 + w, 516 + l)))
    for i in holder:
        try:
            int(i)
        except text_or_error:
            i = 0

    return holder

def league_window_offset(x1, y1, x2, y2) :
    x,y, _, _ = get_window_rect(league_window_name)
    return x1 + x, y1 + y, x2 + x, y2 + y


def read_number(rect):
    screenshot = ImageGrab.grab(bbox=rect, all_screens=True)
    screenshot = ImageOps.invert(screenshot)
    screenshot = ImageOps.grayscale(screenshot)
    # screenshot.show()
    # screenshot.save("screenshot.png")
    text = pytesseract.image_to_string(screenshot)
    if text == '':
        return 0
    return text


def get_window_rect(window_title):
    hwnd = win32gui.FindWindow(None, window_title)
    if hwnd:
        rect = win32gui.GetWindowRect(hwnd)
        return rect
    else:
        return None

def get_window_size(window_title):
    hwnd = win32gui.FindWindow(None, window_title)
    if hwnd:
        rect = win32gui.GetWindowRect(hwnd)
        return (rect[2] - rect[0], rect[3] - rect[1])
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

def convert_RP_to(inp, cur):
    inp = round(inp/cur/100, 2)
    return "$: " + str(inp)
def covert_RP_from(inp, cur):
    inp = round(inp*cur*100, 2)
    return str(inp)


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
        rect = get_window_rect(league_window_name)
        self.setGeometry(rect[0], rect[1], rect[2] - rect[0], rect[3] - rect[1])

    def mousePressEvent(self, event):
        print('click!')
        QtWidgets.qApp.quit()

def load_window(mywindow, layout, shop_prices):
    label = QtWidgets.QLabel(convert_RP_to(int(rp),usd), mywindow)
    label.setStyleSheet(
        "color: #F0E6D2; background-color: #010710; padding-left: 2px; padding-bottom: 5px; font-size: 14px; font-weight: bold;")
    layout.addWidget(label)
    label.move(932, 18)
    #label1 = QtWidgets.QLabel("0", mywindow)
    y = 0
    for i in shop_prices:
        holder_widget = QtWidgets.QLabel(convert_RP_to(int(i),usd), mywindow)
        layout.addWidget(holder_widget)
        holder_widget.move(poss[y][0], poss[y][1])
        holder_widget.setStyleSheet(
            "color: #F0E6D2; background-color: #010710; padding-left: 2px; padding-bottom: 0px; font-size: 14px; font-weight: bold;")
        y += 1

if __name__ == '__main__':
    usd = 1.15
    app = QApplication(sys.argv)
    layout = QtWidgets.QVBoxLayout()
    mywindow = MainWindow()
    rp = get_RP()
    shop_prices = get_default_shop_prices()

    load_window(mywindow, layout, shop_prices)
    
    #layout.addWidget()
    mywindow.show()
    app.exec_()