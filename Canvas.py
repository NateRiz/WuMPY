from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPainter, QBrush, QColor, QPaintEvent


class Canvas(QLabel):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: gray")
        self.monitor = None

        self.monitor_dimensions = (-1, -1, -1, -1)
        self.scale = 0

    def set_monitor(self, monitor):
        self.monitor = monitor
        self.update()

    def paintEvent(self, a0: QPaintEvent) -> None:
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
        painter = QPainter(self)
        brush = QBrush(QColor(255, 255, 255))
        painter.setBrush(brush)
        painter.drawRect(*self.monitor_dimensions)

        windows = sorted([self.monitor.child(i) for i in range(self.monitor.childCount())],
                         key=lambda window: window.z)
        [self._draw_window(window) for window in windows]

    def _draw_window(self, window):
        painter = QPainter(self)
        brush = QBrush(QColor(*window.color))
        painter.setBrush(brush)
        monitor_x, monitor_y, *_ = self.monitor_dimensions

        x = monitor_x + (window.x // self.scale)
        y = monitor_y + (window.y // self.scale)
        w = window.w // self.scale
        h = window.h // self.scale

        painter.drawRect(x, y, w, h)