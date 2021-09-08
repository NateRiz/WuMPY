import json
from os import path, mkdir, listdir
from PyQt5.QtCore import QStandardPaths, QFileInfo

from Monitor import Monitor


class FileHandler:
    def __init__(self):
        self.app_data = QStandardPaths.writableLocation(QStandardPaths.DataLocation)
        if not path.isdir(self.app_data):
            mkdir(self.app_data)

    def save(self, file_name, monitors: [Monitor]):
        with open(file_name, "w") as file:
            serialized = [monitor.serialize() for monitor in monitors]
            json.dump(serialized, file, indent=2)

    def load(self, file_name, monitors: [Monitor]):
        with open(file_name, "r") as file:
            data = json.load(file)
            for m in data:
                monitor = Monitor("", 0, 0)
                monitor.deserialize(m)
                monitors.append(monitor)


    def get_all_workspaces(self) -> [QFileInfo]:
        return [QFileInfo(path.join(self.app_data, f)) for f in listdir(self.app_data) if path.isfile(path.join(self.app_data, f))]
