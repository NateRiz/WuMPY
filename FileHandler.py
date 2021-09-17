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
        """
        Serialize and store the monitors/windows into the given file.
        :param file_name: File
        :param monitors: monitors to store.
        :return:
        """
        with open(file_name, "w") as file:
            serialized = [monitor.serialize() for monitor in monitors]
            json.dump(serialized, file, indent=2)

    def load(self, file_name, out_monitors: [Monitor]):
        """
        Load the monitors and windows from the file into out_monitors.
        :param file_name: File name
        :param out_monitors: Empty list to store monitors in for return
        :return:
        """
        with open(file_name, "r") as file:
            data = json.load(file)
            for m in data:
                monitor = Monitor("", 0, 0, -1)
                monitor.deserialize(m)
                out_monitors.append(monitor)

    def get_all_workspaces(self) -> [QFileInfo]:
        return [QFileInfo(path.join(self.app_data, f)) for f in listdir(self.app_data) if path.isfile(path.join(self.app_data, f))]
