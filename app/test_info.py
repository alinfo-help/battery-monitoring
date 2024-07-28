from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit, QDialogButtonBox, QLabel,
    QComboBox, QDateEdit, QDoubleSpinBox, QGroupBox, QFormLayout
)
from PyQt5.QtCore import Qt, QDate, QDateTime
from PyQt5.QtGui import QFont
import psycopg2
from psycopg2.extras import RealDictCursor
from db_code.db_client import get_connection

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

        self.incoming_coach_edit = QLineEdit(self)
        test_info_layout.addRow(QLabel("Incoming Coach:"), self.incoming_coach_edit)

        self.type_combo = QComboBox(self)
        self.type_combo.addItems(["Charging", "Discharging"])
        test_info_layout.addRow(QLabel("Select Type:"), self.type_combo)
        
        self.test_duration_spin = QDoubleSpinBox(self)
        self.test_duration_spin.setRange(0.1, 24) 
        self.test_duration_spin.setDecimals(1) 
        self.test_duration_spin.setSingleStep(0.1)
        test_info_layout.addRow(QLabel("Test Duration (hrs):"), self.test_duration_spin)

        self.log_date_edit = QDateEdit(self)
        self.log_date_edit.setDate(QDate.currentDate())
        self.log_date_edit.setCalendarPopup(True)
        test_info_layout.addRow(QLabel("Lug Date:"), self.log_date_edit)

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
        self.buttons.accepted.connect(self.save_test_details)
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
                color: #000;
            }
            QLineEdit, QComboBox, QDoubleSpinBox, QDateEdit {
                font-family: Arial;
                font-size: 10pt;
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: #fff;
                color: #000;           
            }
            QGroupBox {
                font-family: Arial;
                font-size: 11pt;
                font-weight: bold;
                padding: 7px;
                border: 1px solid #ccc;
                border-radius: 5px;
                margin-top: 10px;
                color: #000;
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
            "incoming_coach": self.incoming_coach_edit.text(),
            "type": self.type_combo.currentText(),
            "test_duration": self.test_duration_spin.value(),
            "lug_date": self.log_date_edit.date().toString('yyyy-MM-dd'),
            "bench_number": self.bench_number_edit.text(),
            "com_port": self.com_port_edit.text()
        }

    def save_test_details(self):
        test_details = self.get_test_details()
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO tests (bank_id, incoming_coach, test_name, logical_test_name, lug_date, test_duration, process_type, bench_no, comport)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
        """, (self.parent().current_bank_id, test_details["incoming_coach"], test_details["test_name"], None, test_details["lug_date"], test_details["test_duration"], test_details["type"], test_details["bench_number"], test_details["com_port"]))
        test_id = cur.fetchone()[0]
        cur.execute("""
            INSERT INTO test_runs (test_id, run_num, start_time, status)
            VALUES (%s, %s, %s, %s) RETURNING id
        """, (test_id, 1, QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss'), 'pending'))
        test_run_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        self.accept()
        self.parent().start_test_recording(test_run_id, test_details["test_duration"])
