from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QGridLayout, QTreeWidget, QLabel, QPushButton, QDesktopWidget, QMessageBox

from Canvas import Canvas
from FileHandler import FileHandler
from Monitor import Monitor
from TextInput import TargetInput
from TransformInput import TransformInput
from Window import Window


class Workspace(QWidget):
    def __init__(self, workspace_name, should_load_from_file, return_to_workspace_selector_callback):
        super().__init__()
        self.workspace_name = workspace_name
        self.return_to_workspace_selector_callback = return_to_workspace_selector_callback

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
        self.monitor_tree.setCurrentItem(monitor.add_default_window())
        monitor.setExpanded(True)
        self.canvas.update()

    def on_select_monitor(self, monitor):
        self.canvas.set_monitor(monitor)
        self.monitor_label.setText(str(monitor))
        self.hide_properties()

    def on_select_window(self, window):
        self.transform_input.x_input.text_field.setText(str(window.x))
        self.transform_input.y_input.text_field.setText(str(window.y))
        self.transform_input.z_input.text_field.setText(str(window.z))
        self.transform_input.w_input.text_field.setText(str(window.w))
        self.transform_input.h_input.text_field.setText(str(window.h))
        self.target.text_field.setText(str(window.target))
        self.show_properties()

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
        try:
            file_handler.load(filename, self.monitors)
        except Exception as e:
            QMessageBox(text=F"Couldn't load {self.workspace_name}: ({e})", icon=QMessageBox.Critical).exec()
            self.monitors.clear()

    def create_new_workspace(self):
        for i in range(QDesktopWidget().screenCount()):
            size = QDesktopWidget().screenGeometry(i)
            self.monitors.append(Monitor(f"Monitor {i + 1}", size.width(), size.height()))

    def hide_properties(self):
        self.transform_input.setHidden(True)
        self.target.setHidden(True)

    def show_properties(self):
        self.transform_input.setHidden(False)
        self.target.setHidden(False)