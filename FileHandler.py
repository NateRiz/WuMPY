import json
from os import path, mkdir, listdir
from PyQt5.QtCore import QStandardPaths, QFileInfo

from Monitor import Monitor


class FileHandler:
    def __init__(self):
        self.app_data = QStandardPaths.writableLocation(QStandardPaths.DataLocation)
        if not path.isdir(self.app_data):
            mkdir(self.app_data)

    def save(self, file_name, monitors: [Monitor], retry_time):
        """
        Serialize and store the monitors/windows into the given file.
        :param file_name: File
        :param monitors: monitors to store.
        :return:
        """
        with open(file_name, "w") as file:
            serialized = [retry_time] + [monitor.serialize() for monitor in monitors]
            json.dump(serialized, file, indent=2)

    def load(self, file_name):
        """
        Load the monitors and windows from the file into out_monitors.
        :param file_name: File name
        :param monitors: Empty list to store monitors in for return
        :return:
        """
        monitors = []
        with open(file_name, "r") as file:
            data = json.load(file)
            retry_time = data[0]
            for m in data[1:]:
                monitor = Monitor("", 0, 0, -1)
                monitor.deserialize(m)
                monitors.append(monitor)

        return monitors, retry_time

    def get_all_workspaces(self) -> [QFileInfo]:
        return [QFileInfo(path.join(self.app_data, f)) for f in listdir(self.app_data) if path.isfile(path.join(self.app_data, f))]
