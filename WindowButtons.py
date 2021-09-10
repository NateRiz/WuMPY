from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton


class WindowButtons(QWidget):
    def __init__(self):
        super().__init__()
        self.v_layout = QVBoxLayout()

        self.add_new_window = QPushButton(text="Add New Window")
        self.delete_window = QPushButton(text="Delete Window")
        self.run = QPushButton(text="Run")

        self.v_layout.addWidget(self.add_new_window)
        self.v_layout.addWidget(self.delete_window)
        self.v_layout.addWidget(self.run)

        self.setLayout(self.v_layout)