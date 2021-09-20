from random import randint

from PyQt5.QtCore import Qt
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
        self.is_regex_enabled = False
        self.setFlags(self.flags() | Qt.ItemIsEditable)
        self.is_pixel_precision_enabled = False
        self.color = (randint(200, 255), randint(200, 255), randint(200, 255))
        self.setText(0, self.name)
        self.setToolTip(0, self.name)

    def serialize(self):
        return self.name, self.win_x, self.win_y, self.win_z, self.win_w, self.win_h, self.target, self.process_name, self.is_pixel_precision_enabled, self.is_regex_enabled, self.color

    def deserialize(self, data):
        self.name, self.win_x, self.win_y, self.win_z, self.win_w, self.win_h, self.target, self.process_name, self.is_pixel_precision_enabled, self.is_regex_enabled, self.color = data
        self.setText(0, self.name)
        self.setToolTip(0, self.name)

    def __str__(self):
        return f"{self.name} {self.win_x} {self.win_y} {self.win_z} {self.win_w} {self.win_h}"

    def __repr__(self):
        return str(self)
