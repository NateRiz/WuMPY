from PyQt5.QtWidgets import QTreeWidget

from Window import Window


class MonitorTree(QTreeWidget):
    def __init__(self):
        super().__init__()
        self.setColumnCount(1)
        self.setHeaderLabel("Monitors")
        self.model().dataChanged.connect(self.on_window_rename)

    def on_window_rename(self, x, _):
        window = self.currentItem()
        if type(window) is Window:
            window.name = x.data()
