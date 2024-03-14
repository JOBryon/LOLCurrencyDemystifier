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
window_state_save = ""

main_widgets = []
skin_buy_widget = None
featured_buy_widget = None

colorblind_mode = False
dyslexic_mode = False
current_currency = "US Dollar"
custom_conversion = False
custom_amount = 150
custom_symbol = "$"

currency_list = {}

# This list was written with the assumption that no single item will cost more than 4500 RP.    
# First RP then price in USD with no tax.
usd_RP = [[575, 4.99], [1380, 10.99], [2800, 21.99], [4500, 34.99]]

# Currency object that holds the name of each currency, the symbol representation and the prices of rp in that currency listed [RP, price] in a list of arrays
class Currency:
    def __init__(self, name, symbol, lol_prices) -> None:
        self.name = name
        self.symbol = symbol
        self.league_prices = lol_prices
    
    def get_conversion_rate(self):
        return self.league_prices[0][0] // self.league_prices[0][1]

def makeCurrencyList():
    currency_list = {}
    # United States Dollar
    currency_list["US Dollar"] = Currency("US Dollar","$",[[575, 4.99],[1380,10.99],[2800,21.99],[4500,34.99],[6500,49.99],[13500,99.99]])
    # Canadian Dollar
    currency_list["Canadian Dollar"] = Currency("Canadian Dollar","$",[[475, 5.49],[1380,14.99],[2800,29.99],[4800,49.99],[7250,74.99],[13000,129.99]])
    # Euro
    currency_list["Euro"] = Currency("Euro", "€", [[575,4.99],[1380,10.99],[2800,21.99],[4500,34.99],[6500,49.99],[13500,99.99]])
    # Great British Pound
    currency_list["Great British Pound"] = Currency("Great British Pound","£",[[575,4.49],[1450,10.99],[2850,20.99],[5000,34.99],[7250,49.99],[15000,99.99]])
    # Polish Ztoty
    currency_list["Polish złoty"] = Currency("Polish złoty", "zł",[[350,13.99],[750,27.99],[1380,47.99],[2950,99.99],[5250,174.99],[10750,349.99]])
    # Czech Koruna
    currency_list["Czech Koruna"] = Currency("Czech Koruna","Kč",[[325,79],[650,149],[1380,299],[2800,599],[6250,1290],[12500,2490]])
    # Romanian New Leu
    currency_list["Romanian New Leu"] = Currency("Romanian New Leu", "RON",[[250,9.99],[650,24.99],[1380,49.99],[2800,99.99],[5750,199.99],[12500,429.99]])
    # Hungarian Forint
    currency_list["Hungarian Forint"] = Currency("Hungarian Forint", "Ft", [[250,799],[650,1990],[1400,3990],[2850,7990],[5500,14990],[11500,29990]])
    # Brazil Real
    currency_list["Brazilian Real"] = Currency("Brazilian Real", "R$", [[400,10.90],[1275,34.90],[2575,69.90],[4575,124.90],[6425,174.90],[12850,349.90]])
    # Australian Dollar
    currency_list["Australian Dollar"] = Currency("Australian Dollar", "$", [[475,5.99],[1425,16.99],[2800,30.99],[4600,49.99],[7000,74.99],[12500,129.99]])
    # New Zealand Dollar 
    currency_list["New Zealand Dollar"] = Currency("New Zealand Dollar", "$", [[520,6.99],[1380,16.99],[2850,34.99],[4200,49.99],[6500,74.99],[12750,139.99]])
    return currency_list

def get_RP():
    return read_number(league_window_offset(932, 18, 995, 42))
    # read_number(get_window_rect(league_window_name))


def setup_widgets(loc_offset, width):
    w = 32
    l = 17

    horizontal_offset = 30

    for i in range(width):
        poss.append([loc_offset + (200 * i) - horizontal_offset, 316, loc_offset + w + (200 * i) - horizontal_offset, 316 + l])
        poss.append([loc_offset + (200 * i) - horizontal_offset, 516, loc_offset + w + (200 * i) - horizontal_offset, 516 + l])


def get_default_shop_prices(loc_offset, width):
    w = 32
    l = 17
    print("READING PRICES")
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
    text = pytesseract.image_to_string(screenshot, config="--psm 7 -c tessedit_char_whitelist=0123456789.")
    if text == '':
        return 0
    try:
        int(text)
    except:
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

def convert_RP_to(inp):
    if not custom_conversion:
        rate = currency_list[current_currency].get_conversion_rate() / 100
        symbol = currency_list[current_currency].symbol
    else:
        rate = custom_amount / 100
        symbol = custom_symbol

    inp = round(inp/rate/100, 2)
    return symbol + ": " + str(inp)

def covert_RP_from(inp, cur):
    inp = round(inp*cur*100, 2)
    return str(inp)

# Wallet is current RP and price is price for the item and cur is currency list of RP prices
def RP_to_purchase(wallet, price):
    if not custom_conversion:
        symbol = currency_list[current_currency].symbol
        cur = currency_list[current_currency].league_prices
    else:
        symbol = custom_symbol
        cur = [[custom_amount, 1]]

    if price <= wallet:
        holder = str(convert_RP_to(price))
        if holder[-2] != '.':
            return holder
        else:
            return holder + '0'

    dif = price - wallet
    for i in cur:
        if dif < i[0]:
            holder = str(i[1])
            if holder[-2] != '.':
                return symbol + ': ' + holder
            else:
                return symbol + ': ' + holder + '0'

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
        
        # stores settings window
        self.settings = SettingsWindow()

        # sets the window to cover RP
        rect = get_window_rect(league_window_name)
        self.setGeometry(rect[0], rect[1], rect[2] - rect[0], rect[3] - rect[1])

    def mousePressEvent(self, event):
        print('click!')
    
    def openSettings(self):
        self.settings.show()


class NoLeagueWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Error")
        layout = QtWidgets.QVBoxLayout()

        self.currency_label = QtWidgets.QLabel("Please open League of Legends before running Currency Demystifier!", self)
        layout.addWidget(self.currency_label)

        self.close = QtWidgets.QPushButton("Close", self)
        self.close.clicked.connect(app.quit)
        layout.addWidget(self.close)

        self.setLayout(layout)


class SettingsWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Currency Demystifyer Settings")
        # self.setWindowFlags(
        #     QtCore.Qt.WindowStaysOnTopHint |
        #     QtCore.Qt.FramelessWindowHint |
        #     QtCore.Qt.X11BypassWindowManagerHint
        # )
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # rect = get_window_rect(league_window_name)
        # self.setGeometry(rect[0], rect[1], 300, 400)

        layout = QtWidgets.QVBoxLayout()
        
        self.colorblind = QtWidgets.QCheckBox("Colorblind mode", self)
        layout.addWidget(self.colorblind)

        self.dyslexic = QtWidgets.QCheckBox("Use OpenDsylexic font", self)
        layout.addWidget(self.dyslexic)

        self.currency_label = QtWidgets.QLabel("Currency: ", self)
        layout.addWidget(self.currency_label)
        self.currency = QtWidgets.QComboBox(self)
        self.currency_list = makeCurrencyList()
        i = 0
        for curr in self.currency_list.values():
            self.currency.insertItem(i, curr.name)
            i += 1
        layout.addWidget(self.currency)

        self.custom_currency = QtWidgets.QCheckBox("Use custom currency conversion", self)
        layout.addWidget(self.custom_currency)
        self.custom_conversion = QtWidgets.QLineEdit("150", self)
        layout.addWidget(self.custom_conversion)
        self.custom_conversion_label = QtWidgets.QLabel("Riot Points per", self)
        layout.addWidget(self.custom_conversion_label)
        self.custom_symbol = QtWidgets.QLineEdit("$", self)
        layout.addWidget(self.custom_symbol)

        self.save = QtWidgets.QPushButton("Save", self)
        self.save.clicked.connect(self.saveValues)
        layout.addWidget(self.save)

        self.setLayout(layout)
    
    def saveValues(self):
        global colorblind_mode
        global dyslexic_mode
        global current_currency
        global custom_conversion
        global custom_amount
        global custom_symbol

        colorblind_mode = self.colorblind.isChecked()
        dyslexic_mode = self.dyslexic.isChecked()
        current_currency = self.currency.currentText()
        custom_conversion = self.custom_currency.isChecked()
        custom_amount = int(self.custom_conversion.text())
        custom_symbol = self.custom_symbol.text()

        print(current_currency)
        print(custom_conversion)
        print(custom_amount)
        print(custom_symbol)
        self.hide()


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
    global window_state_save

    if button == Button.left and not pressed:
        if check_collision_rect(x, y, 241, 89, 241 + 53, 89 + 17):
            window_state = "skins"
        elif check_collision_rect(x, y, 33, 89, 33 + 74, 89 + 17):
            window_state = "featured"
        elif check_collision_rect(x, y, 813, 6, 813 + 56, 6 + 71):
            window_state = "featured"
        elif window_state == "buy":
            if window_state_save == "featured" and check_collision_rect(x, y, 924, 193, 924 + 44, 193 + 44):
                featured_buy_widget.hide()
                main_widgets[0].hide()
                main_widgets[1].hide()
                main_widgets[2].hide()
                main_widgets[3].hide()
                main_widgets[4].show()
                main_widgets[5].show()
                main_widgets[6].show()
                main_widgets[7].show()
                window_state = window_state_save
            if window_state_save == "skins" and check_collision_rect(x, y, 871, 125, 871 + 24, 125 + 24):
                skin_buy_widget.hide()
                main_widgets[0].show()
                main_widgets[1].show()
                main_widgets[2].show()
                main_widgets[3].show()
                main_widgets[4].show()
                main_widgets[5].show()
                main_widgets[6].show()
                main_widgets[7].show()
                window_state = window_state_save
        elif buy_button_collision(x, y):
            print("BUY BUTTON COLLIDE")
            skin_buy_widget.hide()
            featured_buy_widget.hide()


            #         styling = "background-color: #010710; padding-left: 2px; padding-bottom: 0px; font-size: 14px; font-weight: bold;"
            #
            #         to_purchase = RP_to_purchase(int(userRP),int(price))
            #
            #
            #         if float(to_purchase[to_purchase.find(":") + 2:]) > 0:
            #             if colorblind_mode:
            #                 styling += "color: #0000FF;"
            #             else:
            #                 styling += "color: #FF0000;"
            #         else:
            #             styling += "color: #F0E6D2;"
            #         main_widgets[i].setText(to_purchase)
            #         main_widgets[i].setStyleSheet(styling)

            styling = "background-color: #010710; padding-left: 2px; padding-bottom: 0px; font-size: 14px; font-weight: bold; width: 140px; height: 41px;"

            if window_state == "featured":
                price = read_number(league_window_offset(372, 477, 372 + 41, 477 + 17))
                to_purchase = RP_to_purchase(int(userRP), int(price))
                if float(to_purchase[to_purchase.find(":") + 2:]) > 0:
                    if colorblind_mode:
                        styling += "color: #0000FF;"
                    else:
                        styling += "color: #FF0000;"
                else:
                    styling += "color: #F0E6D2;"

                featured_buy_widget.setText(to_purchase)
                featured_buy_widget.setStyleSheet(styling)
                featured_buy_widget.show()
            elif window_state == "skins":
                price = read_number(league_window_offset(652, 523, 652 + 42, 523 + 16))
                to_purchase = RP_to_purchase(int(userRP), int(price))
                if float(to_purchase[to_purchase.find(":") + 2:]) > 0:
                    if colorblind_mode:
                        styling += "color: #0000FF;"
                    else:
                        styling += "color: #FF0000;"
                else:
                    styling += "color: #F0E6D2;"

                skin_buy_widget.setText(to_purchase)
                skin_buy_widget.setStyleSheet(styling)
                skin_buy_widget.show()

            window_state_save = window_state
            window_state = "buy"

def buy_button_collision(x, y):
    if window_state == 'featured':
        for i in range(2):
            if check_collision_rect(x, y, 634 + (i * 200), 149, 634 + 190 + (i * 200), 149 + 190):
                return True
            if check_collision_rect(x, y, 634 + (i * 200), 349, 634 + 190 + (i * 200), 349 + 190):
                return True
    elif window_state == 'skins':
        for i in range(4):
            if check_collision_rect(x, y, 234 + (i * 200), 149, 234 + 190 + (i * 200), 149 + 190):
                return True
            if check_collision_rect(x, y, 234 + (i * 200), 349, 234 + 190 + (i * 200), 349 + 190):
                return True

    return False

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


def load_window(mywindow, layout, shop_prices):
    global main_widgets
    print("LOADING")
    currency_list = makeCurrencyList()

    rp = get_RP()
    label = QtWidgets.QLabel(convert_RP_to(int(rp)), mywindow)
    
    # TODO: add an if statement here that hinges on colorblind_mode and dyslexic_mode to change styling for different modes
    label.setStyleSheet(
        "color: #F0E6D2; background-color: #010710; padding-left: 2px; padding-bottom: 5px; font-size: 14px; font-weight: bold; min-width: 150px")
    
    
    layout.addWidget(label)
    label.move(905, 16)
    #label1 = QtWidgets.QLabel("0", mywindow)
    y = 0
    for i in shop_prices:
        holder_widget = QtWidgets.QLabel(RP_to_purchase(int(rp),int(i)), mywindow)
        layout.addWidget(holder_widget)
        holder_widget.move(poss[y][0], poss[y][1])
        main_widgets.append(holder_widget)
        # TODO: add an if statement here that hinges on colorblind_mode and dyslexic_mode to change styling for different modes
        holder_widget.setStyleSheet(
            "color: #F0E6D2; background-color: #010710; padding-left: 2px; padding-bottom: 0px; font-size: 14px; font-weight: bold;")
        
        y += 1

    settings_button = QtWidgets.QPushButton("Settings", mywindow)
    settings_button.clicked.connect(mywindow.openSettings)
    layout.addWidget(settings_button)

    global skin_buy_widget
    global featured_buy_widget
    skin_buy_widget = QtWidgets.QLabel("SKIN HERE", mywindow)
    layout.addWidget(skin_buy_widget)
    skin_buy_widget.move(570, 510)

    skin_buy_widget.setStyleSheet(
        "color: #F0E6D2; background-color: #010710; padding-left: 2px; padding-bottom: 0px; font-size: 14px; font-weight: bold; width: 140px; height: 41px;")

    featured_buy_widget = QtWidgets.QLabel("FEAT HERE", mywindow)
    layout.addWidget(featured_buy_widget)
    featured_buy_widget.move(318, 469)
    featured_buy_widget.setStyleSheet(
        "color: #F0E6D2; background-color: #010710; padding-left: 2px; padding-bottom: 0px; font-size: 14px; font-weight: bold; text-align: center; width: 140px; height: 41px;")

    skin_buy_widget.hide()
    featured_buy_widget.hide()

    mywindow.setLayout(layout)
    # mywindow.update()

def update_labels(loc_offset, width):
    global main_widgets
    global userRP
    w = 32
    l = 17

    print("UPDATING LABELS")

    if window_state == 'featured':
        start = 4
        end = 7
    elif window_state == 'skins':
        start = 0
        end = 7
    else:
        start = 0
        end = 7

    for i in range(start, end + 1):

        if i % 2 == 0:
            price = read_number(league_window_offset(loc_offset + (200 * i), 316, loc_offset + w + (200 * i), 316 + l))
        else:
            price = read_number(league_window_offset(loc_offset + (200 * i), 516, loc_offset + w + (200 * i), 516 + l))

        styling = "background-color: #010710; padding-left: 2px; padding-bottom: 0px; font-size: 14px; font-weight: bold;"

        to_purchase = RP_to_purchase(int(userRP),int(price))


        if float(to_purchase[to_purchase.find(":") + 2:]) > 0:
            if colorblind_mode:
                styling += "color: #0000FF;"
            else:
                styling += "color: #FF0000;"
        else:
            styling += "color: #F0E6D2;"
        main_widgets[i].setText(to_purchase)
        main_widgets[i].setStyleSheet(styling)


def state_change():
    print("CHANGING")
    match window_state:
        case "featured":
            shop_prices = get_default_shop_prices(723, 2)
            update_labels(723, 2)
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
            update_labels(323, 4)
            main_widgets[0].show()
            main_widgets[1].show()
            main_widgets[2].show()
            main_widgets[3].show()
            main_widgets[4].show()
            main_widgets[5].show()
            main_widgets[6].show()
            main_widgets[7].show()

        case "buy":
            main_widgets[0].hide()
            main_widgets[1].hide()
            main_widgets[2].hide()
            main_widgets[3].hide()
            main_widgets[4].hide()
            main_widgets[5].hide()
            main_widgets[6].hide()
            main_widgets[7].hide()

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
        last_window_state = window_state
        main_widgets[0].hide()
        main_widgets[1].hide()
        main_widgets[2].hide()
        main_widgets[3].hide()
        main_widgets[4].hide()
        main_widgets[5].hide()
        main_widgets[6].hide()
        main_widgets[7].hide()
        QTimer.singleShot(1000, state_change)
        # # clear_layout(layout)
        # load_window(mywindow, layout, shop_prices)
        # print(layout.count())


def quit_program():
    print("QUIT")
    mywindow.close()
    app.quit()
    exit(0)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window_exists = win32gui.FindWindow(None, league_window_name)

    if not window_exists:
        error_window = NoLeagueWindow()
        error_window.show()
        app.exec_()
        exit(0)

    listener_thread = threading.Thread(target=start_listener)
    listener_thread.start()

    currency_list = makeCurrencyList()
    layout = QtWidgets.QVBoxLayout()
    mywindow = MainWindow()
    poss = []
    setup_widgets(323, 4)
    shop_prices = get_default_shop_prices(323, 4)

    userRP = get_RP()

    print(poss)
    load_window(mywindow, layout, shop_prices)

    close_button = QtWidgets.QPushButton("Close", mywindow)
    layout.addWidget(close_button)
    close_button.clicked.connect(quit_program)
    close_button.move(1200, 0)

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