from PyQt5.QtWidgets import QMainWindow, QMenu, QAction, QStackedWidget

from Workspace import Workspace
from WorkspaceSelector import WorkspaceSelector


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WuMPY")
        self.setFixedHeight(300)
        self.setFixedWidth(400)

        self.file = QMenu("&File")
        self.menuBar().addMenu(self.file)
        self.save_action = QAction("&Save", self)
        self.file.addAction(self.save_action)
        self.save_action.triggered.connect(lambda: self.workspace and self.workspace.save())
        self.load_action = QAction("&Load", self)
        self.file.addAction(self.load_action)
        self.load_action.triggered.connect(self.return_to_workspace_selector)

        self.root = QStackedWidget()
        self.workspace_selector = WorkspaceSelector(self.open_workspace)
        self.workspace_selector_idx = self.root.addWidget(self.workspace_selector)
        self.workspace = None
        self.setCentralWidget(self.root)

    def open_workspace(self, workspace_name, should_load_from_file):
        self.workspace = Workspace(workspace_name, should_load_from_file, self.return_to_workspace_selector)
        if not self.is_workspace_loaded():
            return

        self.setFixedWidth(1000)
        self.setFixedHeight(600)
        idx = self.root.addWidget(self.workspace)
        self.root.setCurrentIndex(idx)

    def return_to_workspace_selector(self):
        self.setFixedHeight(300)
        self.setFixedWidth(400)

        if self.workspace:
            self.root.removeWidget(self.workspace)
        self.root.setCurrentIndex(self.workspace_selector_idx)
        self.workspace_selector.load_all_workspaces()

    def is_workspace_loaded(self):
        return len(self.workspace.monitors) > 0
