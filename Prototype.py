import pytesseract
from PyQt5 import QtGui, QtCore, uic
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow, QApplication
import win32gui
import sys
import threading
import random
import time
from pynput.mouse import Listener
from PIL import ImageGrab, ImageOps

layout = None

# Replace the string with your tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

league_window_name = "League of Legends"

last_window_state = ""
window_state = ""

main_widgets = []
skin_buy_widgets = []
featured_buy_widget = None

# This list was written with the assumption that no single item will cost more than 4500 RP.    
# First RP then price in USD with no tax.
usd_RP = [[575, 4.99], [1380, 10.99], [2800, 21.99], [4500, 34.99]]


def get_RP():
    return read_number(league_window_offset(932, 18, 995, 42))
    # read_number(get_window_rect(league_window_name))


def setup_widgets(loc_offset, width):
    w = 32
    l = 17

    for i in range(width):
        poss.append([loc_offset + (200 * i), 316, loc_offset + w + (200 * i), 316 + l])
        poss.append([loc_offset + (200 * i), 516, loc_offset + w + (200 * i), 516 + l])


def get_default_shop_prices(loc_offset, width):
    w = 32
    l = 17
    holder = []
    for i in range(width):
        holder.append(read_number(league_window_offset(loc_offset + (200 * i), 316, loc_offset + w + (200 * i), 316 + l)))
        holder.append(read_number(league_window_offset(loc_offset + (200 * i), 516, loc_offset + w + (200 * i), 516 + l)))

    for i in holder:
        try:
            int(i)
        except:
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

# Wallet is current RP and price is price for the item and cur is currency list of RP prices
def RP_to_purchase(wallet, price, cur):
    if price <= wallet:
        holder = str(convert_RP_to(price, 1.15))
        if holder[-2] != '.':
            return holder
        else:
            return holder + '0'

    dif = price - wallet
    for i in cur:
        if dif < i[0]:
            holder = str(i[1])
            if holder[-2] != '.':
                return '$: ' + holder
            else:
                return '$: ' + holder + '0'

    return '-1'


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

from pynput.mouse import Listener, Button

def check_collision_rect(mouseX, mouseY, x1, y1, x2, y2):
    xx, yy, _, _ = get_window_rect(league_window_name)
    x1 += xx
    x2 += xx
    y1 += yy
    y2 += yy

    return (x1 < mouseX < x2) and (y1 < mouseY < y2)


def on_click(x, y, button, pressed):
    global window_state
    if button == Button.left and not pressed:
        if check_collision_rect(x, y, 241, 89, 241 + 53, 89 + 17):
            window_state = "skins"
        elif check_collision_rect(x, y, 33, 89, 33 + 74, 89 + 17):
            window_state = "featured"
        elif check_collision_rect(x, y, 813, 6, 813 + 56, 6 + 71):
            window_state ="featured"



def clear_layout(layout):
    global poss
    while layout.count() > 0:
        widget = layout.itemAt(0).widget()
        layout.removeWidget(widget)
        widget.deleteLater()


def on_scroll(x, y, dx, dy):
    # print(x, y, dx, dy)
    pass

def start_listener():
    with Listener(on_click=on_click, on_scroll=on_scroll) as listener:
        listener.join()

listener_thread = threading.Thread(target=start_listener)
listener_thread.start()


def load_window(mywindow, layout, shop_prices):
    global main_widgets
    print("LOADING")
    rp = get_RP()
    label = QtWidgets.QLabel(convert_RP_to(int(rp),usd), mywindow)
    label.setStyleSheet(
        "color: #F0E6D2; background-color: #010710; padding-left: 2px; padding-bottom: 5px; font-size: 14px; font-weight: bold;")
    layout.addWidget(label)
    label.move(932, 18)
    #label1 = QtWidgets.QLabel("0", mywindow)
    y = 0
    for i in shop_prices:
        holder_widget = QtWidgets.QLabel(RP_to_purchase(int(rp),int(i),usd_RP), mywindow)
        layout.addWidget(holder_widget)
        holder_widget.move(poss[y][0], poss[y][1])
        main_widgets.append(holder_widget)
        holder_widget.setStyleSheet(
            "color: #F0E6D2; background-color: #010710; padding-left: 2px; padding-bottom: 0px; font-size: 14px; font-weight: bold;")
        y += 1

    mywindow.setLayout(layout)
    # mywindow.update()

def update_labels(loc_offset, width):
    global main_widgets
    w = 32
    l = 17
    rp = get_RP()

    for i in range(width):
        if main_widgets[i].isHidden():
            continue

        if i % 2 == 0:
            read_number(league_window_offset(loc_offset + (200 * i), 316, loc_offset + w + (200 * i), 316 + l))
        else:
            read_number(league_window_offset(loc_offset + (200 * i), 516, loc_offset + w + (200 * i), 516 + l))

        main_widgets[i].setText(RP_to_purchase(int(rp),int(i),usd_RP))


def poll():
    global last_window_state
    global main_widgets
    #
    # test_wd.setText(str(random.randint(1,50)))
    #
    # if test_wd.isHidden():
    #     test_wd.show()
    # else:
    #     test_wd.hide()

    if window_state != last_window_state:
        print ("STATE CHANGE")
        match window_state:
            case "featured":
                shop_prices = get_default_shop_prices(723, 2)
                main_widgets[0].hide()
                main_widgets[1].hide()
                main_widgets[2].hide()
                main_widgets[3].hide()
                main_widgets[4].show()
                main_widgets[5].show()
                main_widgets[6].show()
                main_widgets[7].show()

            case "skins":
                shop_prices = get_default_shop_prices(323, 4)
                main_widgets[0].show()
                main_widgets[1].show()
                main_widgets[2].show()
                main_widgets[3].show()

        last_window_state = window_state
        # # clear_layout(layout)
        # load_window(mywindow, layout, shop_prices)
        # print(layout.count())




if __name__ == '__main__':
    usd = 1.15
    app = QApplication(sys.argv)
    layout = QtWidgets.QVBoxLayout()
    mywindow = MainWindow()
    poss = []
    setup_widgets(323, 4)
    shop_prices = get_default_shop_prices(323, 4)

    print(poss)
    load_window(mywindow, layout, shop_prices)

    # test_wd = QtWidgets.QLabel("ASWD", mywindow)
    # layout.addWidget(test_wd)
    # test_wd.move(500, 200)
    # test_wd.setStyleSheet(
    #     "color: #F0E6D2; background-color: #010710; padding-left: 2px; padding-bottom: 0px; font-size: 14px; font-weight: bold;")

    main_widgets[0].hide()
    main_widgets[1].hide()
    main_widgets[2].hide()
    main_widgets[3].hide()
    main_widgets[4].hide()
    main_widgets[5].hide()
    main_widgets[6].hide()
    main_widgets[7].hide()
    mywindow.show()

    timer = QTimer()
    timer.timeout.connect(poll)
    timer.start(200)

    app.exec_()