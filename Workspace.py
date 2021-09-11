from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QGridLayout, QTreeWidget, QLabel, QPushButton, QDesktopWidget, QMessageBox

from ApplicationParameters import ApplicationParameters
from Canvas import Canvas
from FileHandler import FileHandler
from Monitor import Monitor
from MonitorTree import MonitorTree
from TransformInput import TransformInput
from Window import Window
from WindowButtons import WindowButtons
from WindowManager import WindowManager


class Workspace(QWidget):
    def __init__(self, workspace_name, should_load_from_file, return_to_workspace_selector_callback):
        super().__init__()
        self.workspace_name = workspace_name
        self.return_to_workspace_selector_callback = return_to_workspace_selector_callback

        grid = QGridLayout()
        grid.setAlignment(Qt.AlignTop)

        self.monitor_tree = MonitorTree()
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
        window_buttons = WindowButtons()
        window_buttons.add_new_window.clicked.connect(self.add_window_to_monitor)
        window_buttons.delete_window.clicked.connect(self.delete_window)
        window_buttons.run.clicked.connect(self.run)
        grid.addWidget(window_buttons, 3, 0, 1, 1)
        self.application_parameters = ApplicationParameters()
        self.transform_input = TransformInput()
        self.transform_input.x_input.text_field.textEdited.connect(self.on_change_window_property)
        self.transform_input.y_input.text_field.textEdited.connect(self.on_change_window_property)
        self.transform_input.z_input.text_field.textEdited.connect(self.on_change_window_property)
        self.transform_input.w_input.text_field.textEdited.connect(self.on_change_window_property)
        self.transform_input.h_input.text_field.textEdited.connect(self.on_change_window_property)
        self.transform_input.exact_position_toggle.check_box.toggled.connect(self.on_toggle_pixel_precision)
        grid.addWidget(self.transform_input, 3, 1, 1, 1)
        self.application_parameters.target.text_field.textChanged.connect(self.on_change_window_property)
        self.application_parameters.process.text_field.textChanged.connect(self.on_change_window_property)
        grid.addWidget(self.application_parameters, 3, 2, 1, 2)
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

    def delete_window(self):
        window = self.monitor_tree.currentItem()
        if type(window) is not Window:
            return
        monitor = window.parent()
        monitor.delete_window(window)

    def on_select_monitor(self, monitor):
        self.canvas.set_monitor(monitor)
        self.monitor_label.setText(str(monitor))
        self.hide_properties()

    def on_toggle_pixel_precision(self, is_enabled):
        window = self.monitor_tree.currentItem()
        if type(window) is not Window:
            return
        window.is_pixel_precision_enabled = is_enabled
        if is_enabled:
            self.convert_window_to_px()
        else:
            self.convert_window_from_px()

    def convert_window_to_px(self):
        window = self.monitor_tree.currentItem()
        if type(window) is not Window:
            return
        monitor = window.parent()
        monitor_width = monitor.monitor_width
        monitor_height = monitor.monitor_height
        window.win_x = (window.win_x * monitor_width) // 100
        window.win_y = (window.win_y * monitor_height) // 100
        window.win_w = (window.win_w * monitor_width) // 100
        window.win_h = (window.win_h * monitor_height) // 100
        self.update_text_fields(window)

    def convert_window_from_px(self):
        window = self.monitor_tree.currentItem()
        if type(window) is not Window:
            return
        monitor = window.parent()
        monitor_width = monitor.monitor_width
        monitor_height = monitor.monitor_height
        window.win_x = int(100 * window.win_x / monitor_width)
        window.win_y = int(100 * window.win_y / monitor_height)
        window.win_w = int(100 * window.win_w / monitor_width)
        window.win_h = int(100 * window.win_h / monitor_height)
        self.update_text_fields(window)

    def on_select_window(self, window):
        self.update_text_fields(window)

    def update_text_fields(self, window):
        self.disconnect_fields()
        self.transform_input.x_input.text_field.setText(str(window.win_x))
        self.transform_input.y_input.text_field.setText(str(window.win_y))
        self.transform_input.z_input.text_field.setText(str(window.win_z))
        self.transform_input.w_input.text_field.setText(str(window.win_w))
        self.transform_input.h_input.text_field.setText(str(window.win_h))
        self.transform_input.exact_position_toggle.check_box.setChecked(window.is_pixel_precision_enabled)
        self.application_parameters.target.text_field.setText(str(window.target))
        self.application_parameters.process.text_field.setText(str(window.process_name))
        self.connect_fields()
        self.show_properties()
        self.canvas.update()

    def disconnect_fields(self):
        self.transform_input.exact_position_toggle.check_box.toggled.disconnect()
        self.application_parameters.target.text_field.textChanged.disconnect()
        self.application_parameters.process.text_field.textChanged.disconnect()
        self.transform_input.x_input.text_field.textEdited.disconnect()
        self.transform_input.y_input.text_field.textEdited.disconnect()
        self.transform_input.z_input.text_field.textEdited.disconnect()
        self.transform_input.w_input.text_field.textEdited.disconnect()
        self.transform_input.h_input.text_field.textEdited.disconnect()

    def connect_fields(self):
        self.transform_input.exact_position_toggle.check_box.toggled.connect(self.on_toggle_pixel_precision)
        self.application_parameters.target.text_field.textChanged.connect(self.on_change_window_property)
        self.application_parameters.process.text_field.textChanged.connect(self.on_change_window_property)
        self.transform_input.x_input.text_field.textEdited.connect(self.on_change_window_property)
        self.transform_input.y_input.text_field.textEdited.connect(self.on_change_window_property)
        self.transform_input.z_input.text_field.textEdited.connect(self.on_change_window_property)
        self.transform_input.w_input.text_field.textEdited.connect(self.on_change_window_property)
        self.transform_input.h_input.text_field.textEdited.connect(self.on_change_window_property)

    def on_change_window_property(self, _):
        window = self.monitor_tree.currentItem()
        if type(window) is not Window:
            return

        try:
            x = int(self.transform_input.x_input.text)
            y = int(self.transform_input.y_input.text)
            z = int(self.transform_input.z_input.text)
            w = int(self.transform_input.w_input.text)
            h = int(self.transform_input.h_input.text)
            target = self.application_parameters.target.text
            process_name = self.application_parameters.process.text
            is_pixel_precision_enabled = self.transform_input.exact_position_toggle.check_box.isChecked()
        except ValueError as e:
            print(e)
            return

        window.win_x = x
        window.win_y = y
        window.win_z = z
        window.win_w = w
        window.win_h = h
        window.target = target
        window.process_name = process_name
        window.is_pixel_precision_enabled = is_pixel_precision_enabled
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
        self.application_parameters.setHidden(True)

    def show_properties(self):
        self.transform_input.setHidden(False)
        self.application_parameters.setHidden(False)

    def run(self):
        window_manager = WindowManager()
        window_manager.run(self.monitors)
