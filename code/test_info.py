from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit, QDialogButtonBox, QLabel,
    QComboBox, QDateEdit, QSpinBox, QGroupBox, QHBoxLayout, QFormLayout
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont

class TestInfoDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Test Information')
        self.resize(600, 400)
        self.test_details = {}

        layout = QVBoxLayout(self)

        # Create Test Info GroupBox
        test_info_group = QGroupBox("Test Information")
        test_info_layout = QFormLayout()
        
        self.test_name_edit = QLineEdit(self)
        test_info_layout.addRow(QLabel("Test Name:"), self.test_name_edit)

        self.type_combo = QComboBox(self)
        self.type_combo.addItems(["Charging", "Discharging"])
        test_info_layout.addRow(QLabel("Select Type:"), self.type_combo)

        self.test_duration_spin = QSpinBox(self)
        self.test_duration_spin.setRange(1, 9999)
        test_info_layout.addRow(QLabel("Test Duration (minutes):"), self.test_duration_spin)

        self.log_date_edit = QDateEdit(self)
        self.log_date_edit.setDate(QDate.currentDate())
        self.log_date_edit.setCalendarPopup(True)
        test_info_layout.addRow(QLabel("Log Date:"), self.log_date_edit)

        self.bench_number_edit = QLineEdit(self)
        test_info_layout.addRow(QLabel("Bench Number:"), self.bench_number_edit)

        self.com_port_edit = QLineEdit(self)
        test_info_layout.addRow(QLabel("COM Port:"), self.com_port_edit)

        test_info_group.setLayout(test_info_layout)
        layout.addWidget(test_info_group)

        # Add dialog buttons
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Save | QDialogButtonBox.Cancel,    
            Qt.Horizontal, self
        )
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)

        self.apply_styles()

    def apply_styles(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #fff;
            }
            QLabel {
                font-family: Arial;
                font-size: 10pt;
                padding: 5px;
            }
            QLineEdit, QComboBox, QSpinBox, QDateEdit {
                font-family: Arial;
                font-size: 10pt;
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: #fff;
            }
            QGroupBox {
                font-family: Arial;
                font-size: 11pt;
                font-weight: bold;
                padding: 7px;
                border: 1px solid #ccc;
                border-radius: 5px;
                margin-top: 10px;
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

    def get_test_details(self):
        return {
            "test_name": self.test_name_edit.text(),
            "type": self.type_combo.currentText(),
            "test_duration": self.test_duration_spin.value(),
            "log_date": self.log_date_edit.date().toString('yyyy-MM-dd'),
            "bench_number": self.bench_number_edit.text(),
            "com_port": self.com_port_edit.text()
        }
