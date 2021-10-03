from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton

from CustomWidgets.DialogTargetInput import DialogTargetInput
from CustomWidgets.TextInput import TextInput


class MonitorProperties(QWidget):
    def __init__(self):
        super().__init__()
        self.v_layout = QVBoxLayout()

        self.monitor_index = DialogTargetInput("Monitor Index:", "Identify")
        self.monitor_index.text_field.setValidator(QIntValidator())
        self.v_layout.addWidget(self.monitor_index)

        self.retry_time = TextInput("Retry Time (sec):")
        self.retry_time.text_field.setValidator(QIntValidator())
        self.v_layout.addWidget(self.retry_time)

        self.add_new_window = QPushButton(text="Add New Window")
        self.delete_window = QPushButton(text="Delete Window")
        self.run = QPushButton(text="Run")

        self.v_layout.addWidget(self.add_new_window)
        self.v_layout.addWidget(self.delete_window)
        self.v_layout.addWidget(self.run)

        self.setLayout(self.v_layout)