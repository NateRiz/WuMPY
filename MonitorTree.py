from PyQt5.QtWidgets import QTreeWidget

from Monitor import Monitor
from Window import Window


class MonitorTree(QTreeWidget):
    def __init__(self):
        super().__init__()
        self.setColumnCount(1)
        self.setHeaderLabel("Monitors")
        self.model().dataChanged.connect(self.on_window_rename)

    def on_window_rename(self, x, _):
        item = self.currentItem()

        # Both of these do the same things and we could combine them because Python doesn't care.
        # But they aren't technically the same type and I don't feel like adding inheritance for this.
        if type(item) is Window:
            item.name = x.data()
        elif type(item) is Monitor:
            item.name = x.data()

