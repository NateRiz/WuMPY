from os import path

from FileHandler import FileHandler
from Win32Facade import Win32Facade


class HeadlessWindowManager:
    def __init__(self, file):
        self.monitors = []
        file_handler = FileHandler()

        file_path = path.join(file_handler.app_data, "WuMPY", file)
        if path.exists(file_path):
            # First try and find the save file in the WuMPY directory in app_data
            file_handler.load(file_path, self.monitors)
        elif path.exists(file):
            # Otherwise check if they provided a full path.
            file_handler.load(file, self.monitors)

        window_manager = Win32Facade()
        window_manager.run(self.monitors)
