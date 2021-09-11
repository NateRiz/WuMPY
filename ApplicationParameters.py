from PyQt5.QtWidgets import QVBoxLayout, QWidget, QFileDialog, QInputDialog

from DialogTargetInput import DialogTargetInput
from WindowManager import WindowManager


class ApplicationParameters(QWidget):
    def __init__(self):
        super().__init__()
        self.v_layout = QVBoxLayout()


        self.target = DialogTargetInput("Target:", "...")
        self.process = DialogTargetInput("Window Name:", "Scan")
        self.process.text_field.setMaximumWidth(256)
        self.target.text_field.setMaximumWidth(256)
        self.target.button.clicked.connect(lambda: self.target.text_field.setText(QFileDialog.getOpenFileName(self, 'OpenFile')[0]))
        self.process.button.clicked.connect(lambda: self.process.text_field.setText(QInputDialog.getItem(self, 'Window Names', "Window Names:", self.get_windows().keys())[0]))
        self.v_layout.addWidget(self.target)
        self.v_layout.addWidget(self.process)

        self.setLayout(self.v_layout)

    def get_windows(self):
        return WindowManager().list_windows()
