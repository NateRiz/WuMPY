from PyQt5.QtWidgets import QPushButton, QFileDialog

from TextInput import TextInput


class TargetInput(TextInput):
    def __init__(self):
        super().__init__("Target:")
        self.button = QPushButton(text="...")
        self.h_layout.addWidget(self.button)
        self.button.setMaximumWidth(32)
        self.button.clicked.connect(lambda: self.text_field.setText(QFileDialog.getOpenFileName(self, 'OpenFile')[0]))