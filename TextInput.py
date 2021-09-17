from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QHBoxLayout


class TextInput(QWidget):
    def __init__(self, text):
        super().__init__()
        self.label = QLabel(parent=self, text=text)
        self.text_field = QLineEdit()
        #self.text_field.setAlignment(Qt.AlignRight)
        self.h_layout = QHBoxLayout()
        self.setLayout(self.h_layout)
        self.h_layout.addWidget(self.label)
        self.h_layout.addWidget(self.text_field)

    @property
    def text(self):
        return self.text_field.text()
