from PyQt5.QtWidgets import QPushButton, QFileDialog

from TextInput import TextInput


class DialogTargetInput(TextInput):
    def __init__(self, text, button_text):
        super().__init__(text)
        self.button = QPushButton(text=button_text)
        self.h_layout.addWidget(self.button)
        self.button.setMaximumWidth(48)
