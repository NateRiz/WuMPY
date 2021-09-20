from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QMessageBox

from ApplicationParameters import ApplicationParameters
from Canvas import Canvas
from FileHandler import FileHandler
from Monitor import Monitor
from MonitorTree import MonitorTree
from TransformInput import TransformInput
from Util.WMPYMath import try_parse_color
from Window import Window
from MonitorProperties import MonitorProperties
from Win32Facade import Win32Facade


class Workspace(QWidget):
    def __init__(self, workspace_name, hwnd, should_load_from_file, return_to_workspace_selector_callback):
        super().__init__()
        self.workspace_name = workspace_name
        self.return_to_workspace_selector_callback = return_to_workspace_selector_callback
        self.is_saved = True
        self.hwnd = hwnd

        grid = QGridLayout()
        grid.setAlignment(Qt.AlignTop)

        self.monitor_tree = MonitorTree()
        self.monitors = []

        self.monitor_properties = MonitorProperties()
        self.monitor_properties.monitor_index.button.clicked.connect(self.identify_monitor)
        self.monitor_properties.add_new_window.clicked.connect(self.add_window_to_monitor)
        self.monitor_properties.delete_window.clicked.connect(self.delete_window)
        self.monitor_properties.run.clicked.connect(self.run)
        grid.addWidget(self.monitor_properties, 3, 0, 1, 1)
        self.hide_monitor_properties()

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

        self.application_parameters = ApplicationParameters()
        self.transform_input = TransformInput()
        self.hide_window_properties()
        self.monitor_properties.monitor_index.text_field.textChanged.connect(self.on_change_monitor_property)
        self.transform_input.x_input.text_field.textChanged.connect(self.on_change_window_property)
        self.transform_input.y_input.text_field.textChanged.connect(self.on_change_window_property)
        self.transform_input.z_input.text_field.textChanged.connect(self.on_change_window_property)
        self.transform_input.w_input.text_field.textChanged.connect(self.on_change_window_property)
        self.transform_input.h_input.text_field.textChanged.connect(self.on_change_window_property)
        self.transform_input.exact_position_toggle.check_box.toggled.connect(self.on_toggle_pixel_precision)
        grid.addWidget(self.transform_input, 3, 1, 1, 1)
        self.application_parameters.target.text_field.textChanged.connect(self.on_change_window_property)
        self.application_parameters.process.text_field.textChanged.connect(self.on_change_window_property)
        self.application_parameters.color.text_field.textChanged.connect(self.on_change_window_property)
        self.application_parameters.enable_regex.check_box.toggled.connect(self.on_change_window_property)
        grid.addWidget(self.application_parameters, 3, 2, 1, 2)
        self.setLayout(grid)

    def get_selected_monitor(self):
        monitor = self.monitor_tree.currentItem()
        if not monitor:
            return
        if type(monitor) == Window:
            return monitor.parent()
        return monitor

    def get_selected_window(self):
        window = self.monitor_tree.currentItem()
        if type(window) != Window:
            return None
        return window

    def on_tree_select(self, item, previous):
        """
        Callback when something is selected in the tree.
        :param item: Newly selected item
        :param previous: Item that was unselected
        :return: None
        """
        if type(item) is Monitor:
            self.on_select_monitor(item)
        elif type(item) is Window:
            self.on_select_monitor(item.parent())
            self.on_select_window(item)

    def add_window_to_monitor(self):
        """
        Add a new default Window to the current monitor
        :return: None
        """
        monitor = self.get_selected_monitor()
        if not monitor:
            return

        if type(monitor) is not Monitor:
            monitor = monitor.parent()

        self.monitor_tree.setCurrentItem(monitor.add_default_window())
        monitor.setExpanded(True)
        self.canvas.update()

    def delete_window(self):
        """
        Remove a window from the current monitor
        :return:  None
        """
        window = self.get_selected_window()
        if not window:
            return
        monitor = window.parent()
        monitor.delete_window(window)

    def on_select_monitor(self, monitor):
        """
        Called when user selects a monitor in the tree.
        :param monitor: Newly selected monitor
        :return: None
        """
        self.canvas.set_monitor(monitor)
        self.monitor_label.setText(str(monitor))
        self.monitor_properties.monitor_index.text_field.setText(str(monitor.index))
        self.show_monitor_properties()
        self.hide_window_properties()

    def on_toggle_pixel_precision(self, is_enabled):
        """
        Converts all the transforms to either pixel perfect or percentage based.
        :param is_enabled: if pixel precision is enabled
        :return: None
        """
        window = self.get_selected_window()
        if not window:
            return
        window.is_pixel_precision_enabled = is_enabled
        if is_enabled:
            self.convert_window_to_px()
        else:
            self.convert_window_from_px()

    def convert_window_to_px(self):
        """
        convert label from percentage to pixels
        :return:
        """
        window = self.get_selected_window()
        if not window:
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
        """
        Convert label from pixels to percentage
        :return:
        """
        window = self.get_selected_window()
        if not window:
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
        """
        Callback when user selects a window.
        :param window: New Window
        :return: None
        """
        self.canvas.set_window(window)
        self.update_text_fields(window)

    def update_text_fields(self, window):
        """
        Callback when a new window is selected.
        :param window: What window owns the fields
        :return: None
        """
        self.disconnect_fields()
        self.transform_input.x_input.text_field.setText(str(window.win_x))
        self.transform_input.y_input.text_field.setText(str(window.win_y))
        self.transform_input.z_input.text_field.setText(str(window.win_z))
        self.transform_input.w_input.text_field.setText(str(window.win_w))
        self.transform_input.h_input.text_field.setText(str(window.win_h))
        self.transform_input.exact_position_toggle.check_box.setChecked(window.is_pixel_precision_enabled)
        self.application_parameters.target.text_field.setText(str(window.target))
        self.application_parameters.process.text_field.setText(str(window.process_name))
        self.application_parameters.color.text_field.setText(str(window.color))
        self.application_parameters.enable_regex.check_box.setChecked(window.is_regex_enabled)
        self.connect_fields()
        self.show_window_properties()
        self.canvas.update()

    def disconnect_fields(self):
        """
        Whe we switch windows, we programmatically set the text for every label.
        This causes the textChanged callback to get called and breaks things.
        We must disconnect and reconnect all callbacks when loading in text into a text field.
        :return:
        """
        self.transform_input.exact_position_toggle.check_box.toggled.disconnect()
        self.application_parameters.target.text_field.textChanged.disconnect()
        self.application_parameters.process.text_field.textChanged.disconnect()
        self.application_parameters.color.text_field.textChanged.disconnect()
        self.application_parameters.enable_regex.check_box.toggled.disconnect()
        self.monitor_properties.monitor_index.text_field.textChanged.disconnect()
        self.transform_input.x_input.text_field.textChanged.disconnect()
        self.transform_input.y_input.text_field.textChanged.disconnect()
        self.transform_input.z_input.text_field.textChanged.disconnect()
        self.transform_input.w_input.text_field.textChanged.disconnect()
        self.transform_input.h_input.text_field.textChanged.disconnect()

    def connect_fields(self):
        """
        Reconnect all the fields to their callbacks
        :return:
        """
        self.transform_input.exact_position_toggle.check_box.toggled.connect(self.on_toggle_pixel_precision)
        self.application_parameters.enable_regex.check_box.toggled.connect(self.on_change_window_property)
        self.application_parameters.target.text_field.textChanged.connect(self.on_change_window_property)
        self.application_parameters.process.text_field.textChanged.connect(self.on_change_window_property)
        self.application_parameters.color.text_field.textChanged.connect(self.on_change_window_property)
        self.monitor_properties.monitor_index.text_field.textChanged.connect(self.on_change_monitor_property)
        self.transform_input.x_input.text_field.textChanged.connect(self.on_change_window_property)
        self.transform_input.y_input.text_field.textChanged.connect(self.on_change_window_property)
        self.transform_input.z_input.text_field.textChanged.connect(self.on_change_window_property)
        self.transform_input.w_input.text_field.textChanged.connect(self.on_change_window_property)
        self.transform_input.h_input.text_field.textChanged.connect(self.on_change_window_property)

    def on_change_window_property(self, _):
        self.is_saved = False
        window = self.get_selected_window()
        if not window:
            return

        try:
            x = int(self.transform_input.x_input.text)
            y = int(self.transform_input.y_input.text)
            z = int(self.transform_input.z_input.text)
            w = int(self.transform_input.w_input.text)
            h = int(self.transform_input.h_input.text)
            target = self.application_parameters.target.text
            process_name = self.application_parameters.process.text
            color = self.application_parameters.color.text
            is_pixel_precision_enabled = self.transform_input.exact_position_toggle.check_box.isChecked()
            is_regex_enabled = self.application_parameters.enable_regex.check_box.isChecked()
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
        window.color = try_parse_color(color)
        window.is_pixel_precision_enabled = is_pixel_precision_enabled
        window.is_regex_enabled = is_regex_enabled
        self.canvas.update()

    def on_change_monitor_property(self, _):
        self.is_saved = False
        monitor = self.get_selected_monitor()
        if monitor is None:
            return

        try:
            index = int(self.monitor_properties.monitor_index.text)
        except ValueError as e:
            print(e)
            return
        monitor.index = index


    def save(self):
        """
        Save current new workspace
        :return:
        """
        file_handler = FileHandler()
        file_handler.save(self.workspace_name, self.monitors)
        self.is_saved = True

    def load_workspace(self, filename):
        self.monitors.clear()
        file_handler = FileHandler()
        try:
            file_handler.load(filename, self.monitors)
        except Exception as e:
            QMessageBox(text=F"Could not load {self.workspace_name}: ({e})", icon=QMessageBox.Critical).exec()
            self.monitors.clear()

    def create_new_workspace(self):
        win32_facade = Win32Facade()
        for i, monitor in enumerate(win32_facade.get_monitors()):
            left, top, right, bottom = monitor
            width = right - left
            height = bottom - top
            self.monitors.append(Monitor(f"Monitor", width, height, i))

    def hide_monitor_properties(self):
        self.monitor_properties.monitor_index.setHidden(True)

    def show_monitor_properties(self):
        self.monitor_properties.monitor_index.setHidden(False)

    def hide_window_properties(self):
        """
        Hide the properties when a window is not selected. ie monitor is selected
        :return: None
        """
        self.transform_input.setHidden(True)
        self.application_parameters.setHidden(True)

    def show_window_properties(self):
        """
        Show properties when a window is selected
        :return: None
        """
        self.transform_input.setHidden(False)
        self.application_parameters.setHidden(False)

    def try_prompt_for_save(self):
        if self.is_saved:
            return True
        response = QMessageBox.question(self, "Save", "Do you want to save your changes?", QMessageBox.Cancel | QMessageBox.Discard | QMessageBox.Save, defaultButton=QMessageBox.Cancel)
        if response == QMessageBox.Save:
            self.save()
            return True
        elif response == QMessageBox.Discard:
            return True
        elif response == QMessageBox.Cancel:
            return False
        return False

    def identify_monitor(self):
        monitor = self.get_selected_monitor()
        if not monitor:
            return

        win32_facade = Win32Facade()
        win32_facade.move_window_to_monitor(self.hwnd, monitor.index)
        message = QMessageBox()
        message.setWindowTitle("Identify")
        message.setText(f"Moved WuMPY to monitor index: {monitor.index}")
        message.setIcon(QMessageBox.Information)
        message.exec()

    def run(self):
        window_manager = Win32Facade()
        window_manager.run(self.monitors)
