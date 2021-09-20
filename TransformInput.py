from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QWidget, QVBoxLayout

from CustomWidgets.TextCheckBox import TextCheckBox
from CustomWidgets.TextInput import TextInput


class TransformInput(QWidget):
    def __init__(self):
        super().__init__()
        self.v_layout = QVBoxLayout()

        self.exact_position_toggle = TextCheckBox("Pixel Precision:")

        self.x_input = TextInput("X:")
        self.y_input = TextInput("Y:")
        self.z_input = TextInput("Z-index:")
        self.w_input = TextInput("W:")
        self.h_input = TextInput("H:")
        self.x_input.text_field.setMaximumWidth(96)
        self.y_input.text_field.setMaximumWidth(96)
        self.z_input.text_field.setMaximumWidth(96)
        self.w_input.text_field.setMaximumWidth(96)
        self.h_input.text_field.setMaximumWidth(96)
        self.x_input.text_field.setValidator(QIntValidator())
        self.y_input.text_field.setValidator(QIntValidator())
        self.z_input.text_field.setValidator(QIntValidator())
        self.w_input.text_field.setValidator(QIntValidator())
        self.h_input.text_field.setValidator(QIntValidator())
        self.v_layout.addWidget(self.exact_position_toggle)
        self.v_layout.addWidget(self.x_input)
        self.v_layout.addWidget(self.y_input)
        self.v_layout.addWidget(self.z_input)
        self.v_layout.addWidget(self.w_input)
        self.v_layout.addWidget(self.h_input)

        self.v_layout.setSpacing(0)
        self.v_layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.v_layout)