# from PyQt5.QtWidgets import (
#     QDialog, QVBoxLayout, QGridLayout, QLineEdit, QDialogButtonBox, QLabel
# )
# from PyQt5.QtCore import Qt
# from PyQt5.QtCore import pyqtSignal

# class SettingsDialog(QDialog):
#     # Signal to emit when saving data
#     save_data = pyqtSignal(list)

#     def __init__(self, parent=None, serial_numbers=None, number_of_cells=19, columns=2):
#         super().__init__(parent)
#         self.setWindowTitle('Battery Serial Numbers')
#         self.resize(850, 500)
#         self.number_of_cells = number_of_cells
#         self.serial_numbers = serial_numbers or [None] * self.number_of_cells
#         self.line_edits = [QLineEdit(self) for _ in range(self.number_of_cells)]

#         # Calculate the number of columns based on the number of cells
#         if self.number_of_cells > 20:
#             columns = 4
#         elif self.number_of_cells > 10:
#             columns = 3
#         else:
#             columns = 2
        
#         layout = QVBoxLayout(self)

#         # Create Serial Numbers GroupBox
#         serial_numbers_group = QGridLayout()

#         for i, line_edit in enumerate(self.line_edits, start=1):
#             line_edit.setText(self.serial_numbers[i-1] if i-1 < len(self.serial_numbers) else "")
#             serial_numbers_group.addWidget(QLabel(f'Battery {i}:'), (i-1) // columns, (i-1) % columns * 2)
#             serial_numbers_group.addWidget(line_edit, (i-1) // columns, (i-1) % columns * 2 + 1)

#         layout.addLayout(serial_numbers_group)

#         # Add dialog buttons
#         self.buttons = QDialogButtonBox(
#             QDialogButtonBox.Save | QDialogButtonBox.Cancel,    
#             Qt.Horizontal, self
#         )
#         self.buttons.accepted.connect(self.on_save)
#         self.buttons.rejected.connect(self.reject)
#         layout.addWidget(self.buttons)

#         self.apply_styles()
    
#     def on_save(self):
#         # Emit signal with the serial numbers when saving
#         self.save_data.emit(self.get_serial_numbers())
#         self.accept()

#     def apply_styles(self):
#         with open("./styles/setting.qss", "r") as file:
#             self.setStyleSheet(file.read())

#     def get_serial_numbers(self):
#         return [
#             line_edit.text() if line_edit.text() else self.serial_numbers[i]
#             for i, line_edit in enumerate(self.line_edits)
#         ]

#####################################################################################################################################
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QGridLayout, QLineEdit, QDialogButtonBox, QLabel
)
from PyQt5.QtCore import Qt, pyqtSignal

class SettingsDialog(QDialog):
    # Signal to emit when saving data
    save_data = pyqtSignal(dict)

    def __init__(self, parent=None, bank_id=None, serial_numbers=None, number_of_cells=19, columns=2):
        super().__init__(parent)
        self.setWindowTitle('Battery Serial Numbers')
        self.resize(850, 500)
        self.bank_id = bank_id  # Store the bank_id to identify which bank's settings are being modified
        self.number_of_cells = number_of_cells
        self.serial_numbers = serial_numbers or [None] * self.number_of_cells
        self.line_edits = [QLineEdit(self) for _ in range(self.number_of_cells)]

        # Calculate the number of columns based on the number of cells
        if self.number_of_cells > 20:
            columns = 4
        elif self.number_of_cells > 10:
            columns = 3
        else:
            columns = 2

        layout = QVBoxLayout(self)

        # Create Serial Numbers GroupBox
        serial_numbers_group = QGridLayout()

        for i, line_edit in enumerate(self.line_edits, start=1):
            line_edit.setText(self.serial_numbers[i-1] if i-1 < len(self.serial_numbers) else "")
            serial_numbers_group.addWidget(QLabel(f'Battery {i}:'), (i-1) // columns, (i-1) % columns * 2)
            serial_numbers_group.addWidget(line_edit, (i-1) // columns, (i-1) % columns * 2 + 1)

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
        # Emit signal with the bank_id and serial numbers when saving
        self.save_data.emit({
            'bank_id': self.bank_id,
            'serial_numbers': self.get_serial_numbers()
        })
        self.accept()

    def apply_styles(self):
        with open("./styles/setting.qss", "r") as file:
            self.setStyleSheet(file.read())

    def get_serial_numbers(self):
        return [
            line_edit.text() if line_edit.text() else self.serial_numbers[i]
            for i, line_edit in enumerate(self.line_edits)
        ]
