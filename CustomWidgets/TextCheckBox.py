from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QCheckBox, QSizePolicy


class TextCheckBox(QWidget):
    def __init__(self):
        super().__init__()
        self.label = QLabel(parent=self, text="Pixel Precision:")
        self.check_box = QCheckBox()
        self.h_layout = QHBoxLayout()
        self.setLayout(self.h_layout)
        self.h_layout.addWidget(self.label)
        self.h_layout.addWidget(self.check_box)
        self.label.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)

    @property
    def text(self):
        return self.text_field.text()
