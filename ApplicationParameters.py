from PyQt5.QtWidgets import QVBoxLayout, QWidget, QFileDialog, QInputDialog, QColorDialog

from DialogTargetInput import DialogTargetInput
from WindowManager import WindowManager


class ApplicationParameters(QWidget):
    def __init__(self):
        super().__init__()
        self.v_layout = QVBoxLayout()

        self.target = DialogTargetInput("Target:", "...")
        self.target.button.clicked.connect(lambda: self.target.text_field.setText(QFileDialog.getOpenFileName(self, 'OpenFile')[0]))
        self.target.text_field.setMaximumWidth(256)
        self.v_layout.addWidget(self.target)

        self.process = DialogTargetInput("Window Name:", "Scan")
        self.process.text_field.setMaximumWidth(256)
        self.process.button.clicked.connect(lambda: self.process.text_field.setText(QInputDialog.getItem(self, 'Window Names', "Window Names:", self.get_windows().keys())[0]))
        self.v_layout.addWidget(self.process)

        self.color = DialogTargetInput("Color:", "Choose")
        self.color.text_field.setMaximumWidth(256)
        self.color.button.clicked.connect(self.open_color_picker)
        self.v_layout.addWidget(self.color)

        self.setLayout(self.v_layout)

    def get_windows(self):
        return WindowManager().list_windows()

    def open_color_picker(self):
        color = QColorDialog.getColor()
        self.color.text_field.setText(str(color.getRgb()[:-1]))
