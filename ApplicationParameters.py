from PyQt5.QtWidgets import QVBoxLayout, QWidget, QFileDialog, QInputDialog, QColorDialog

from CustomWidgets.DialogTargetInput import DialogTargetInput
from CustomWidgets.TextCheckBox import TextCheckBox
from Win32Facade import Win32Facade


class ApplicationParameters(QWidget):
    def __init__(self):
        super().__init__()
        self.v_layout = QVBoxLayout()

        self.target = DialogTargetInput("Target:", "...")
        self.target.button.clicked.connect(lambda: self.target.text_field.setText(QFileDialog.getOpenFileName(self, 'OpenFile')[0]))
        self.target.text_field.setMaximumWidth(256)
        self.v_layout.addWidget(self.target)

        self.enable_regex = TextCheckBox("Regex Search for Window Name:")
        self.v_layout.addWidget(self.enable_regex)

        self.process = DialogTargetInput("Window Name:", "Scan")
        self.process.text_field.setMaximumWidth(256)
        self.process.button.clicked.connect(self.open_window_scanner)
        self.v_layout.addWidget(self.process)

        self.color = DialogTargetInput("Color:", "Choose")
        self.color.text_field.setMaximumWidth(256)
        self.color.button.clicked.connect(self.open_color_picker)
        self.v_layout.addWidget(self.color)

        self.setLayout(self.v_layout)

    def get_windows(self):
        """
        Get names of all open windows.
        :return: [String] window names
        """
        return Win32Facade().list_windows()

    def open_color_picker(self):
        """
        Open QT Color picker window.
        :return: None
        """
        color = QColorDialog.getColor()

        # Ignore the Alpha channel
        self.color.text_field.setText(str(color.getRgb()[:-1]))

    def open_window_scanner(self):
        result, is_success = QInputDialog.getItem(self, 'Window Names', "Window Names:", self.get_windows().keys())
        if is_success:
            self.process.text_field.setText(result)

