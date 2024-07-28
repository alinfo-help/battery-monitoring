from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QGridLayout, QLineEdit, QDialogButtonBox, QLabel
)
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal

class SettingsDialog(QDialog):
    # Signal to emit when saving data
    save_data = pyqtSignal(list)

    def __init__(self, parent=None, serial_numbers=None, number_of_cells=19):
        super().__init__(parent)
        self.setWindowTitle('Battery Serial Numbers')
        self.resize(700, 500)
        self.number_of_cells = number_of_cells
        self.serial_numbers = serial_numbers or [None] * self.number_of_cells
        self.line_edits = [QLineEdit(self) for _ in range(self.number_of_cells)]

        layout = QVBoxLayout(self)

        # Create Serial Numbers GroupBox
        serial_numbers_group = QGridLayout()

        for i, line_edit in enumerate(self.line_edits, start=1):
            line_edit.setText(self.serial_numbers[i-1] if i-1 < len(self.serial_numbers) else "")
            serial_numbers_group.addWidget(QLabel(f'Battery {i}:'), (i-1) // 2, (i-1) % 2 * 2)
            serial_numbers_group.addWidget(line_edit, (i-1) // 2, (i-1) % 2 * 2 + 1)

        layout.addLayout(serial_numbers_group)

        # Add dialog buttons
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Save | QDialogButtonBox.Cancel,    
            Qt.Horizontal, self
        )
        self.buttons.accepted.connect(self.on_save)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)

        self.apply_styles()
    
    def on_save(self):
        # Emit signal with the serial numbers when saving
        self.save_data.emit(self.get_serial_numbers())
        self.accept()

    def apply_styles(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #fff;
            }
            QLabel {
                font-family: Arial;
                font-size: 10pt;
                padding: 5px;
                color: #000;  /* Set text color to black */
            }
            QLineEdit {
                font-family: Arial;
                font-size: 10pt;
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: #fff;
                color: #000;  /* Set text color to black */
            }
            QGroupBox {
                font-family: Arial;
                font-size: 11pt;
                font-weight: bold;
                padding: 7px;
                border: 1px solid #ccc;
                border-radius: 5px;
                margin-top: 10px;
                color: #000;  /* Set text color to black */
            }
            QDialogButtonBox {
                background-color: #f0f0f0;
                padding: 10px;
            }
            QPushButton {
                background-color: #468585;
                color: white;
                border: none;
                padding: 10px 24px;
                text-align: center;
                text-decoration: none;
                font-size: 14px;
                margin: 4px 2px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #50B498;
            }
        """)


    def get_serial_numbers(self):
        return [
            line_edit.text() if line_edit.text() else self.serial_numbers[i]
            for i, line_edit in enumerate(self.line_edits)
        ]
