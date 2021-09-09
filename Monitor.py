from Window import Window
from PyQt5.QtWidgets import QTreeWidgetItem


class Monitor(QTreeWidgetItem):
    def __init__(self, name, width, height):
        super().__init__()
        self.monitor_width = width
        self.monitor_height = height
        self.name = name
        self.windows = []

        self.setText(0, str(self))
        self.setToolTip(0, str(self))

    def __str__(self):
        return f"{self.name} ({self.monitor_width}x{self.monitor_height})"

    def __repr__(self):
        return str(self)

    def serialize(self):
        windows = tuple(window.serialize() for window in self.windows)
        return self.name, self.monitor_width, self.monitor_height, windows

    def deserialize(self, data):
        self.name, self.monitor_width, self.monitor_height, windows = data
        for w in windows:
            window = Window(0, 0, 0, 0, 0)
            window.deserialize(w)
            self.add_window(window)

        self.setText(0, str(self))
        self.setToolTip(0, str(self))

    def add_default_window(self):
        window = Window(0, 0, 0, self.monitor_width//3, self.monitor_height//2)
        self.add_window(window)
        return window

    def add_window(self, window):
        self.addChild(window)
        self.windows.append(window)
