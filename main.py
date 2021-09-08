import sys
import win32gui
import os
from Canvas import Canvas
from FileHandler import FileHandler
from LoadableWorkspace import LoadableWorkspace
from TextInput import TextInput, TargetInput
from TransformInput import TransformInput
from Monitor import Monitor
from Window import Window
from PyQt5.QtWidgets import QLabel, QMainWindow, QTreeWidget, QDesktopWidget, QApplication, QGridLayout, QPushButton, \
    QMenu, QListWidget, QHBoxLayout, QInputDialog, QStackedWidget, QAction
from PyQt5.QtWidgets import QWidget, QTreeWidgetItem, QFileDialog
from PyQt5.QtCore import Qt


def win_enum_handler(hwnd, ctx):
    if win32gui.IsWindowVisible(hwnd):
        x0, y0, x1, y1 = win32gui.GetWindowRect(hwnd)
        w = x1 - x0
        h = y1 - y0
        # print("Window:", win32gui.GetWindowText(hwnd))
        # print(x0, x1, y0, y1, w, h)
        # win32gui.MoveWindow(hwnd, x0, y0, w+500, h+500, True)


win32gui.EnumWindows(win_enum_handler, [])


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
        self.load_action = QAction("&Load", self)
        self.file.addAction(self.load_action)

        self.root = QStackedWidget()
        self.workspace_selector = WorkspaceSelector(self.open_workspace)
        self.root.addWidget(self.workspace_selector)
        self.setCentralWidget(self.root)

    def open_workspace(self, workspace_name, should_load_from_file):
        self.setFixedWidth(1000)
        self.setFixedHeight(600)
        workspace = Workspace(workspace_name, should_load_from_file)
        idx = self.root.addWidget(workspace)
        self.root.setCurrentIndex(idx)
        self.save_action.triggered.disconnect()
        self.save_action.triggered.connect(workspace.save)
        self.load_action.triggered.disconnect()
        self.load_action.triggered.connect(workspace.load_workspace)


class WorkspaceSelector(QWidget):
    def __init__(self, open_workspace_callback):
        super().__init__()
        self.open_workspace_callback = open_workspace_callback
        self.grid_layout = QGridLayout()
        label = QLabel("Load Workspace:")
        self.workspace_list = QListWidget()
        self.setLayout(self.grid_layout)
        file_handler = FileHandler()
        for f in file_handler.get_all_workspaces():
            self.workspace_list.addItem(LoadableWorkspace(f))

        h_layout = QHBoxLayout()
        load_button = QPushButton(text="Load")
        load_button.clicked.connect(self.load_workspace)
        new_button = QPushButton(text="New")
        new_button.clicked.connect(self.create_new_workspace)
        h_layout.addWidget(load_button)
        h_layout.addWidget(new_button)

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
        print(workspace_name)
        file_name = os.path.join(FileHandler().app_data, f"{workspace_name}.wmpy")
        self.open_workspace_callback(file_name, True)

class Workspace(QWidget):
    def __init__(self, workspace_name, should_load_from_file):
        super().__init__()
        self.workspace_name = workspace_name

        grid = QGridLayout()
        grid.setAlignment(Qt.AlignTop)

        self.monitor_tree = QTreeWidget()
        self.monitor_tree.setColumnCount(1)
        self.monitor_tree.setHeaderLabel("Monitors")
        self.monitors = []

        if should_load_from_file:
            self.load_workspace(self.workspace_name)
        else:
            self.create_new_workspace()

        self.monitor_tree.addTopLevelItems(self.monitors)
        grid.addWidget(QLabel("Monitors:"), 0, 0, 1, 1)
        grid.addWidget(self.monitor_tree, 1, 0, 2, 1)
        self.canvas = Canvas()
        self.monitor_label = QLabel()
        grid.addWidget(self.canvas, 1, 1, 2, 3)
        grid.addWidget(self.monitor_label, 0, 1, 1, 1)
        grid.setHorizontalSpacing(0)
        self.monitor_tree.currentItemChanged.connect(self.on_tree_select)
        for i in range(grid.columnCount()):
            grid.setColumnStretch(i, 1)
        grid.setRowStretch(1, 3)
        grid.setRowStretch(2, 3)
        grid.setRowStretch(3, 1)
        new_button = QPushButton("Add New Window")
        new_button.clicked.connect(self.add_window_to_monitor)
        grid.addWidget(new_button, 3, 0, 1, 1)
        self.transform_input = TransformInput()
        self.transform_input.x_input.text_field.textEdited.connect(self.on_change_window_property)
        self.transform_input.y_input.text_field.textEdited.connect(self.on_change_window_property)
        self.transform_input.z_input.text_field.textEdited.connect(self.on_change_window_property)
        self.transform_input.w_input.text_field.textEdited.connect(self.on_change_window_property)
        self.transform_input.h_input.text_field.textEdited.connect(self.on_change_window_property)
        grid.addWidget(self.transform_input, 3, 1, 1, 1)
        self.target = TargetInput()
        self.target.text_field.textChanged.connect(self.on_change_window_property)
        grid.addWidget(self.target, 3, 2, 1, 2)
        self.setLayout(grid)

    def on_tree_select(self, item, previous):
        if type(item) is Monitor:
            self.on_select_monitor(item)
        elif type(item) is Window:
            self.on_select_monitor(item.parent())
            self.on_select_window(item)

    def add_window_to_monitor(self):
        monitor = self.monitor_tree.currentItem()
        if type(monitor) is not Monitor:
            monitor = monitor.parent()
        monitor.add_default_window()
        monitor.setExpanded(True)
        self.canvas.update()

    def on_select_monitor(self, monitor):
        self.canvas.set_monitor(monitor)
        self.monitor_label.setText(str(monitor))

    def on_select_window(self, window):
        self.transform_input.x_input.text_field.setText(str(window.x))
        self.transform_input.y_input.text_field.setText(str(window.y))
        self.transform_input.z_input.text_field.setText(str(window.z))
        self.transform_input.w_input.text_field.setText(str(window.w))
        self.transform_input.h_input.text_field.setText(str(window.h))
        self.target.text_field.setText(str(window.target))

    def on_change_window_property(self, _):
        window = self.monitor_tree.currentItem()
        if type(window) is not Window:
            return

        x = y = z = w = h = 0
        target = ""
        try:
            x = int(self.transform_input.x_input.text)
            y = int(self.transform_input.y_input.text)
            z = int(self.transform_input.z_input.text)
            w = int(self.transform_input.w_input.text)
            h = int(self.transform_input.h_input.text)
            target = self.target.text
        except ValueError as e:
            print(e)

        window.x = x
        window.y = y
        window.z = z
        window.w = w
        window.h = h
        window.target = target
        self.canvas.update()

    def save(self):
        file_handler = FileHandler()
        file_handler.save(self.workspace_name, self.monitors)

    def load_workspace(self, filename):
        self.monitors.clear()
        file_handler = FileHandler()
        file_handler.load(filename, self.monitors)

    def create_new_workspace(self):
        for i in range(QDesktopWidget().screenCount()):
            size = QDesktopWidget().screenGeometry(i)
            self.monitors.append(Monitor(f"Monitor {i + 1}", size.width(), size.height()))


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("WuMPY")
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
