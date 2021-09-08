import sys
import win32gui
from PyQt5.QtWidgets import QApplication

from MainWindow import MainWindow


def win_enum_handler(hwnd, ctx):
    if win32gui.IsWindowVisible(hwnd):
        x0, y0, x1, y1 = win32gui.GetWindowRect(hwnd)
        w = x1 - x0
        h = y1 - y0
        # print("Window:", win32gui.GetWindowText(hwnd))
        # print(x0, x1, y0, y1, w, h)
        # win32gui.MoveWindow(hwnd, x0, y0, w+500, h+500, True)


win32gui.EnumWindows(win_enum_handler, [])


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("WuMPY")
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
