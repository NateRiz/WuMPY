from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QHBoxLayout, QPushButton, QFileDialog


class TextInput(QWidget):
    def __init__(self, text):
        super().__init__()
        self.label = QLabel(parent=self, text=text)
        self.text_field = QLineEdit()
        self.h_layout = QHBoxLayout()
        self.setLayout(self.h_layout)
        self.h_layout.addWidget(self.label)
        self.h_layout.addWidget(self.text_field)

    @property
    def text(self):
        return self.text_field.text()


class TargetInput(TextInput):
    def __init__(self):
        super().__init__("Target:")
        self.button = QPushButton(text="...")
        self.h_layout.addWidget(self.button)
        self.button.setMaximumWidth(32)
        self.button.clicked.connect(lambda: self.text_field.setText(QFileDialog.getOpenFileName(self, 'OpenFile')[0]))