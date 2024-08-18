from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class AboutPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel("About Page")
        layout.addWidget(label)
        self.setLayout(layout)
        # Add more widgets for your about information here