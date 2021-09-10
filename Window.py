from random import randint
from PyQt5.QtWidgets import QTreeWidgetItem


class Window(QTreeWidgetItem):
    def __init__(self, x, y, z, w, h):
        super().__init__()
        self.win_x = x
        self.win_y = y
        self.win_z = z
        self.win_w = w
        self.win_h = h
        self.target = ""
        self.process_name = ""
        self.name = "Window"
        self.is_pixel_precision_enabled = False
        self.color = (randint(200, 255), randint(200, 255), randint(200, 255))
        self.setText(0, str(self))
        self.setToolTip(0, str(self))

    def serialize(self):
        return self.name, self.win_x, self.win_y, self.win_z, self.win_w, self.win_h, self.target, self.process_name, self.is_pixel_precision_enabled, self.color

    def deserialize(self, data):
        self.name, self.win_x, self.win_y, self.win_z, self.win_w, self.win_h, self.target, self.process_name, self.is_pixel_precision_enabled, self.color = data
        self.setText(0, str(self))
        self.setToolTip(0, str(self))

    def __str__(self):
        return f"{self.name} {self.win_x} {self.win_y} {self.win_z} {self.win_w} {self.win_h}"

    def __repr__(self):
        return str(self)

    @property
    def absolute_x(self):
        if not self.is_pixel_precision_enabled:
            return int(self.win_x / 100 * self.parent().monitor_width)
        return self.win_x

    @property
    def absolute_y(self):
        if not self.is_pixel_precision_enabled:
            return int(self.win_y / 100 * self.parent().monitor_height)
        return self.win_y
    
    @property
    def absolute_z(self):
        return self.win_z
    
    @property
    def absolute_w(self):
        if not self.is_pixel_precision_enabled:
            return int(self.win_w / 100 * self.parent().monitor_width)
        return self.win_w
    
    @property
    def absolute_h(self):
        if not self.is_pixel_precision_enabled:
            return int(self.win_h / 100 * self.parent().monitor_height)
        return self.win_h


