import pytesseract
import win32gui
from PIL import ImageGrab, ImageOps


# Replace the string with your tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

league_window_name = "League of Legends"

def get_RP():
    read_number(league_window_offset(932, 18, 995, 42))
    # read_number(get_window_rect(league_window_name))


def get_default_shop_prices():
    w = 32
    l = 17

    read_number(league_window_offset(725, 521, 725 + w, 521 + l))
    read_number(league_window_offset(722, 316, 722 + w, 316 + l))
    read_number(league_window_offset(922, 316, 922 + w, 316 + l))
    read_number(league_window_offset(722, 516, 722 + w, 516 + l))
    read_number(league_window_offset(922, 516, 922 + w, 516 + l))


def league_window_offset(x1, y1, x2, y2) :
    x,y, _, _ = get_window_rect(league_window_name)
    return x1 + x, y1 + y, x2 + x, y2 + y


def read_number(rect):
    screenshot = ImageGrab.grab(bbox=rect, all_screens=True)
    screenshot = ImageOps.invert(screenshot)
    screenshot = ImageOps.grayscale(screenshot)
    screenshot.show()
    # screenshot.save("screenshot.png")
    text = pytesseract.image_to_string(screenshot)
    print("Extracted Number:", text)


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

#get_RP()
#get_default_shop_prices()
