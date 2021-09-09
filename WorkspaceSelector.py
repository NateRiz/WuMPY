import os

from PyQt5.QtWidgets import QWidget, QInputDialog, QGridLayout, QLabel, QListWidget, QHBoxLayout, QPushButton

from FileHandler import FileHandler
from LoadableWorkspace import LoadableWorkspace


class WorkspaceSelector(QWidget):
    def __init__(self, open_workspace_callback):
        super().__init__()
        self.open_workspace_callback = open_workspace_callback
        self.grid_layout = QGridLayout()
        label = QLabel("Load Workspace:")
        self.workspace_list = QListWidget()
        self.workspace_list.itemDoubleClicked.connect(self.load_workspace)
        self.setLayout(self.grid_layout)

        h_layout = QHBoxLayout()
        self.load_button = QPushButton(text="Load")
        self.load_button.clicked.connect(self.load_workspace)
        new_button = QPushButton(text="New")
        new_button.clicked.connect(self.create_new_workspace)
        h_layout.addWidget(self.load_button)
        h_layout.addWidget(new_button)

        self.load_all_workspaces()

        self.grid_layout.addWidget(label, 0, 0, 1, 2)
        self.grid_layout.addWidget(self.workspace_list, 1, 0, 1, 2)
        self.grid_layout.addLayout(h_layout, 2, 1, 1, 1)

    def create_new_workspace(self):
        workspace_name = QInputDialog.getText(self, "Workspace Name", "Workspace Name:")[0].strip()
        if not workspace_name:
            return
        file_name = os.path.join(FileHandler().app_data, f"{workspace_name}.wmpy")
        self.open_workspace_callback(file_name, False)

    def load_workspace(self):
        workspace_name = self.workspace_list.currentItem().text()
        file_name = os.path.join(FileHandler().app_data, f"{workspace_name}.wmpy")
        self.open_workspace_callback(file_name, True)

    def load_all_workspaces(self):
        self.workspace_list.clear()
        file_handler = FileHandler()
        for f in file_handler.get_all_workspaces():
            self.workspace_list.addItem(LoadableWorkspace(f))

        if self.workspace_list.count():
            self.workspace_list.setCurrentItem(self.workspace_list.item(0))
            self.load_button.setDisabled(False)
        else:
            self.load_button.setDisabled(True)
