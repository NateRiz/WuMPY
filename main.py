import sys
from PyQt5.QtWidgets import QApplication

from HeadlessWindowManager import HeadlessWindowManager
from MainWindow import MainWindow


def main():
    clargs = sys.argv[1::]
    if clargs:
        HeadlessWindowManager(clargs[0])
    else:
        app = QApplication(sys.argv)
        app.setApplicationName("WuMPY")
        main_window = MainWindow()
        main_window.show()
        sys.exit(app.exec())


if __name__ == '__main__':
    main()