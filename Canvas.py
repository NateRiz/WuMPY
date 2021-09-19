from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPainter, QBrush, QColor, QPaintEvent


class Canvas(QLabel):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: gray")
        self.monitor = None
        self.window = None

        self.monitor_dimensions = (-1, -1, -1, -1)
        self.scale = 0

    def set_monitor(self, monitor):
        """
        Set the currently selected monitor to draw.
        :param monitor: Monitor
        :return: None
        """
        self.monitor = monitor
        self.update()

    def set_window(self, window):
        self.window = window
        self.update()

    def paintEvent(self, _: QPaintEvent) -> None:
        """
        Draw the Canvas
        :return: None
        """
        if not self.monitor:
            return

        monitor_height = self.monitor.monitor_height
        monitor_width = self.monitor.monitor_width

        max_res = max(monitor_height, monitor_width)
        self.scale = max_res // 300
        scaled_width = monitor_width // self.scale
        scaled_height = monitor_height // self.scale

        x = self.width() // 2 - scaled_width // 2
        y = self.height() // 2 - scaled_height // 2
        self.monitor_dimensions = (x, y, scaled_width, scaled_height)

        self._draw_monitor()

    def _draw_monitor(self):
        """
        Draw rectangle representing monitor dimensions
        :return: None
        """
        painter = QPainter(self)
        brush = QBrush(QColor(255, 255, 255))
        painter.setBrush(brush)
        painter.drawRect(*self.monitor_dimensions)

        # Sort by z index. Selected window should be drawn on top of everything.
        windows = sorted([self.monitor.child(i) for i in range(self.monitor.childCount())],
                         key=lambda window: (window is self.window, window.win_z))

        [self._draw_window(window) for window in windows]

    def _draw_window(self, window):
        """
        Draw window by percentage or by exact pixel.
        :param window: Window
        :return: None
        """
        painter = QPainter(self)
        brush = QBrush(QColor(*window.color))
        painter.setBrush(brush)
        monitor_x, monitor_y, monitor_w, monitor_h = self.monitor_dimensions

        if window.is_pixel_precision_enabled:
            x = monitor_x + int(window.win_x / self.scale)
            y = monitor_y + int(window.win_y / self.scale)
            w = int(window.win_w / self.scale)
            h = int(window.win_h / self.scale)
        else:
            x = monitor_x + int((window.win_x / 100) * monitor_w)
            y = monitor_y + int((window.win_y / 100) * monitor_h)
            w = int((window.win_w / 100) * monitor_w)
            h = int((window.win_h / 100) * monitor_h)

        painter.drawRect(x, y, w, h)

        if self.window is window:
            radius = 4
            painter.setBrush(QBrush(QColor(225, 225, 225)))
            painter.drawEllipse(QPoint(x, y), radius, radius)
            painter.drawEllipse(QPoint(x + w, y), radius, radius)
            painter.drawEllipse(QPoint(x, y + h), radius, radius)
            painter.drawEllipse(QPoint(x + w, y + h), radius, radius)
