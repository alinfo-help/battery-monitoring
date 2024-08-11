# from PyQt5.QtWidgets import (
#     QDialog, QVBoxLayout, QLineEdit, QDialogButtonBox, QLabel,
#     QComboBox, QDateEdit, QDoubleSpinBox, QGroupBox, QFormLayout
# )
# from PyQt5.QtCore import Qt, QDate, QDateTime
# from db_code.db_client import get_connection

# class TestInfoDialog(QDialog):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.setWindowTitle('Test Information')
#         self.resize(600, 400)
#         self.test_details = {}
#         self.test_id = None  # Add this attribute to keep track of the test ID

#         layout = QVBoxLayout(self)

#         # Create Test Info GroupBox
#         test_info_group = QGroupBox("Test Information")
#         test_info_layout = QFormLayout()
        
#         self.test_name_edit = QLineEdit(self)
#         test_info_layout.addRow(QLabel("Test Name:"), self.test_name_edit)

#         self.incoming_coach_edit = QLineEdit(self)
#         test_info_layout.addRow(QLabel("Incoming Coach:"), self.incoming_coach_edit)

#         self.type_combo = QComboBox(self)
#         self.type_combo.addItems(["Charging", "Discharging"])
#         test_info_layout.addRow(QLabel("Select Type:"), self.type_combo)
        
#         self.test_duration_spin = QDoubleSpinBox(self)
#         self.test_duration_spin.setRange(0.1, 24)
#         self.test_duration_spin.setDecimals(1)
#         self.test_duration_spin.setSingleStep(0.1)
#         test_info_layout.addRow(QLabel("Test Duration (hrs):"), self.test_duration_spin)

#         self.log_date_edit = QDateEdit(self)
#         self.log_date_edit.setDate(QDate.currentDate())
#         self.log_date_edit.setCalendarPopup(True)
#         test_info_layout.addRow(QLabel("Lug Date:"), self.log_date_edit)

#         self.bench_number_edit = QLineEdit(self)
#         test_info_layout.addRow(QLabel("Bench Number:"), self.bench_number_edit)

#         self.com_port_edit = QLineEdit(self)
#         test_info_layout.addRow(QLabel("COM Port:"), self.com_port_edit)

#         test_info_group.setLayout(test_info_layout)
#         layout.addWidget(test_info_group)

#         # Add dialog buttons
#         self.buttons = QDialogButtonBox(
#             QDialogButtonBox.Save | QDialogButtonBox.Cancel,
#             Qt.Horizontal, self
#         )
#         self.buttons.accepted.connect(self.save_test_details)
#         self.buttons.rejected.connect(self.reject)
#         layout.addWidget(self.buttons)

#         self.apply_styles()

#     def apply_styles(self):
#         with open("./styles/test_info.qss","r") as file:
#             self.setStyleSheet(file.read())

#     def get_test_details(self):
#         return {
#             "test_name": self.test_name_edit.text(),
#             "incoming_coach": self.incoming_coach_edit.text(),
#             "type": self.type_combo.currentText(),
#             "test_duration": self.test_duration_spin.value(),
#             "lug_date": self.log_date_edit.date().toString('yyyy-MM-dd'),
#             "bench_number": self.bench_number_edit.text(),
#             "com_port": self.com_port_edit.text()
#         }

#     def save_test_details(self):
#         test_details = self.get_test_details()
#         conn = get_connection()
#         cur = conn.cursor()

#         if self.test_id:
#             # Update the existing test
#             cur.execute("""
#                 UPDATE tests
#                 SET incoming_coach = %s, test_name = %s, logical_test_name = %s, lug_date = %s, test_duration = %s, process_type = %s, bench_no = %s, comport = %s
#                 WHERE id = %s
#             """, (test_details["incoming_coach"], test_details["test_name"], None, test_details["lug_date"], test_details["test_duration"], test_details["type"], test_details["bench_number"], test_details["com_port"], self.test_id))
#             conn.commit()
#         else:
#             # Insert a new test
#             cur.execute("""
#                 INSERT INTO tests (bank_id, incoming_coach, test_name, logical_test_name, lug_date, test_duration, process_type, bench_no, comport)
#                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
#             """, (self.parent().current_bank_id, test_details["incoming_coach"], test_details["test_name"], None, test_details["lug_date"], test_details["test_duration"], test_details["type"], test_details["bench_number"], test_details["com_port"]))
#             self.test_id = cur.fetchone()[0]
#             cur.execute("""
#                 INSERT INTO test_runs (test_id, run_num, start_time, status)
#                 VALUES (%s, %s, %s, %s) RETURNING id
#             """, (self.test_id, 1, QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss'), 'pending'))
        
#         conn.commit()
#         cur.close()
#         conn.close()
#         self.accept()
#         self.parent().start_test_recording(self.test_id, test_details["test_duration"])

#     def populate_fields(self, test_info):
#         if test_info:
#             self.test_id = test_info["id"]
#             self.test_name_edit.setText(test_info["test_name"])
#             self.incoming_coach_edit.setText(test_info["incoming_coach"])
#             self.type_combo.setCurrentText(test_info["process_type"])
#             self.test_duration_spin.setValue(test_info["test_duration"])
#             self.log_date_edit.setDate(QDate.fromString(test_info["lug_date"], 'yyyy-MM-dd'))
#             self.bench_number_edit.setText(test_info["bench_no"])
#             self.com_port_edit.setText(test_info["comport"])
#         else:
#             self.test_id = None
#             self.test_name_edit.clear()
#             self.incoming_coach_edit.clear()
#             self.type_combo.setCurrentIndex(0)
#             self.test_duration_spin.setValue(0.1)
#             self.log_date_edit.setDate(QDate.currentDate())
#             self.bench_number_edit.clear()
#             self.com_port_edit.clear()

################################################################################################
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit, QDialogButtonBox, QLabel,
    QComboBox, QDateEdit, QDoubleSpinBox, QGroupBox, QFormLayout
)
from PyQt5.QtCore import Qt, QDate, QDateTime
from db_code.db_client import get_connection

class TestInfoDialog(QDialog):
    def __init__(self, parent=None, bank_id=None):
        super().__init__(parent)
        self.setWindowTitle('Test Information')
        self.resize(600, 400)
        self.test_details = {}
        self.test_id = None
        self.bank_id = bank_id  # Track the bank_id for this test

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
        with open("./styles/test_info.qss", "r") as file:
            self.setStyleSheet(file.read())

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

        if self.test_id:
            # Update the existing test
            cur.execute("""
                UPDATE tests
                SET incoming_coach = %s, test_name = %s, logical_test_name = %s, lug_date = %s, test_duration = %s, process_type = %s, bench_no = %s, comport = %s
                WHERE id = %s
            """, (test_details["incoming_coach"], test_details["test_name"], None, test_details["lug_date"], test_details["test_duration"], test_details["type"], test_details["bench_number"], test_details["com_port"], self.test_id))
        else:
            # Insert a new test
            cur.execute("""
                INSERT INTO tests (bank_id, incoming_coach, test_name, logical_test_name, lug_date, test_duration, process_type, bench_no, comport)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
            """, (self.bank_id, test_details["incoming_coach"], test_details["test_name"], None, test_details["lug_date"], test_details["test_duration"], test_details["type"], test_details["bench_number"], test_details["com_port"]))
            self.test_id = cur.fetchone()[0]

            # Insert a new test run
            cur.execute("""
                INSERT INTO test_runs (test_id, run_num, start_time, status)
                VALUES (%s, %s, %s, %s) RETURNING id
            """, (self.test_id, 1, QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss'), 'pending'))

        conn.commit()
        cur.close()
        conn.close()
        self.accept()

        # Trigger the start of the test recording in the parent class
        self.parent().start_test_recording(self.bank_id, self.test_id, test_details["test_duration"])

    def populate_fields(self, test_info):
        if test_info:
            self.test_id = test_info["id"]
            self.test_name_edit.setText(test_info["test_name"])
            self.incoming_coach_edit.setText(test_info["incoming_coach"])
            self.type_combo.setCurrentText(test_info["process_type"])
            self.test_duration_spin.setValue(test_info["test_duration"])
            self.log_date_edit.setDate(QDate.fromString(test_info["lug_date"], 'yyyy-MM-dd'))
            self.bench_number_edit.setText(test_info["bench_no"])
            self.com_port_edit.setText(test_info["comport"])
        else:
            self.test_id = None
            self.test_name_edit.clear()
            self.incoming_coach_edit.clear()
            self.type_combo.setCurrentIndex(0)
            self.test_duration_spin.setValue(0.1)
            self.log_date_edit.setDate(QDate.currentDate())
            self.bench_number_edit.clear()
            self.com_port_edit.clear()
