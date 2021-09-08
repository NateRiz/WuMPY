from PyQt5.QtCore import QFileInfo
from PyQt5.QtWidgets import QListWidgetItem


class LoadableWorkspace(QListWidgetItem):
    def __init__(self, file_name: QFileInfo):
        super().__init__()

        self.setText(file_name.baseName())
        self.setToolTip(file_name.baseName())

