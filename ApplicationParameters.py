from PyQt5.QtWidgets import QVBoxLayout, QWidget

from TargetInput import TargetInput
from TextInput import TextInput


class ApplicationParameters(QWidget):
    def __init__(self):
        super().__init__()
        self.v_layout = QVBoxLayout()

        self.target = TargetInput()
        self.process = TextInput("Window Name:")
        self.v_layout.addWidget(self.target)
        self.v_layout.addWidget(self.process)

        self.setLayout(self.v_layout)