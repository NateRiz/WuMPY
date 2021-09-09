from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLayout, QCheckBox

from TextCheckBox import TextCheckBox
from TextInput import TextInput


class TransformInput(QWidget):
    def __init__(self):
        super().__init__()
        self.v_layout = QVBoxLayout()

        self.exact_position_toggle = TextCheckBox()

        self.x_input = TextInput("X:")
        self.y_input = TextInput("Y:")
        self.z_input = TextInput("Z-index:")
        self.w_input = TextInput("W:")
        self.h_input = TextInput("H:")
        self.v_layout.addWidget(self.exact_position_toggle)
        self.v_layout.addWidget(self.x_input)
        self.v_layout.addWidget(self.y_input)
        self.v_layout.addWidget(self.z_input)
        self.v_layout.addWidget(self.w_input)
        self.v_layout.addWidget(self.h_input)

        self.v_layout.setSpacing(0)
        self.v_layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.v_layout)