import sys
from PyQt5.QtWidgets import QApplication
from MainWindow import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("WuMPY")
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()