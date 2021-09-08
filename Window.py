from random import randint
from PyQt5.QtWidgets import QTreeWidgetItem


class Window(QTreeWidgetItem):
    def __init__(self, x, y, z, w, h):
        super().__init__()
        self.x = x
        self.y = y
        self.z = z
        self.w = w
        self.h = h
        self.target = ""
        self.name = "Window"
        self.is_percentage = False
        self.color = (randint(200, 255), randint(200, 255), randint(200, 255))
        self.setText(0, str(self))
        self.setToolTip(0, str(self))

    def serialize(self):
        return self.name, self.x, self.y, self.z, self.w, self.h, self.target, self.is_percentage, self.color

    def deserialize(self, data):
        self.name, self.x, self.y, self.z, self.w, self.h, self.target, self.is_percentage, self.color = data
        self.setText(0, str(self))
        self.setToolTip(0, str(self))

    def __str__(self):
        return f"{self.name} {self.x} {self.y} {self.z} {self.w} {self.h}"

    def __repr__(self):
        return str(self)
