import csv
import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QGridLayout, QWidget, QLabel, QComboBox, QHBoxLayout, QPushButton
from PyQt5.QtCore import QTimer, QDateTime
from db_code.db_client import get_connection
from settings import SettingsDialog
from test_info import TestInfoDialog
from report import generate_pdf_report

class BatteryMonitoringSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Battery Monitoring System')
        self.resize(800, 600)
        self.init_ui()
        self.apply_styles()

        # Timer to update data every 5 seconds
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_data)
        self.timer.start(5000)  # Update every 5 seconds

    def init_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.bank_selector = QComboBox(self)
        self.bank_selector.currentIndexChanged.connect(self.display_batteries)
        layout.addWidget(self.bank_selector)

        self.grid_layout = QGridLayout()
        layout.addLayout(self.grid_layout)

        # Create a horizontal layout for buttons
        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)

        self.menu_bar = QHBoxLayout()
        layout.addLayout(self.menu_bar)

        self.settings_button = QPushButton("Settings", self)
        self.settings_button.clicked.connect(self.open_settings_dialog)
        button_layout.addWidget(self.settings_button)

        self.start_button = QPushButton("Start", self)
        self.start_button.clicked.connect(self.open_test_info_dialog)
        button_layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop", self)
        self.stop_button.clicked.connect(self.stop_recording)
        button_layout.addWidget(self.stop_button)

        self.report_button = QPushButton("Report", self)
        self.report_button.clicked.connect(generate_pdf_report)
        button_layout.addWidget(self.report_button)


        self.labels = []  # To store QLabel references
        self.serial_numbers = []

        self.load_banks()

    def load_banks(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name FROM banks")
        banks = cur.fetchall()
        cur.close()
        conn.close()

        self.bank_selector.addItem("Select a bank")
        for bank in banks:
            self.bank_selector.addItem(bank[1], bank[0])
        
        # Set default bank
        default_bank = next((bank[0] for bank in banks if bank[1] == "70ah"), None)
        if default_bank:
            self.bank_selector.setCurrentIndex(self.bank_selector.findData(default_bank))
            self.display_batteries()

    def display_batteries(self):
        for i in reversed(range(self.grid_layout.count())):
            widget_to_remove = self.grid_layout.itemAt(i).widget()
            self.grid_layout.removeWidget(widget_to_remove)
            widget_to_remove.setParent(None)

        bank_id = self.bank_selector.currentData()
        if bank_id:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT number_of_cells FROM banks WHERE id = %s", (bank_id,))
            number_of_cells = cur.fetchone()[0]
            cur.close()
            conn.close()

            self.labels = []
            self.serial_numbers = []  # Clear serial numbers list

            for i in range(number_of_cells):
                label = QLabel(f'Battery {i+1}')
                self.grid_layout.addWidget(label, i // 4, i % 4)
                self.labels.append(label)
                self.serial_numbers.append("")  # Initialize with empty serial numbers or load from DB

    def update_data(self):
        latest_row = self.read_latest_data('../data/battery_data.csv')
        if latest_row:
            for i, label in enumerate(self.labels):
                voltage = float(latest_row.get(f"Bank1.B{i+1}", 0))  # Default to 0 if key not found
                color = "#4E9F3D" if voltage > 6.5 else "#ED2B2A"
                serial_number = self.serial_numbers[i]
                text = f'Battery {i+1}: {voltage} V'
                if serial_number:
                    text += f'\nSerial: {serial_number}'
                label.setStyleSheet(f"background-color: {color}; color: white; border: 0.5px solid black; border-radius: 5px; padding: 35px;")
                label.setText(text)

    def read_latest_data(self, csv_file_path):
        if not os.path.isfile(csv_file_path):
            return None
        with open(csv_file_path, 'r') as csvfile:
            csvreader = csv.DictReader(csvfile)
            latest_row = None
            for row in csvreader:
                latest_row = row  # Last row will be the latest
            return latest_row

    def open_settings_dialog(self):
        dialog = SettingsDialog(self, self.serial_numbers)
        if dialog.exec_():
            self.serial_numbers = dialog.get_serial_numbers()
            self.update_data()

    def open_test_info_dialog(self):
        dialog = TestInfoDialog(self)
        if dialog.exec_():
            self.test_details = dialog.get_test_details()
            self.start_recording()

    def stop_recording(self):
        # self.recording_timer.stop()
        # self.start_button.setEnabled(True)
        # recording_stop_time = QDateTime.currentDateTime()
        # duration = self.recording_start_time.secsTo(recording_stop_time)
        # elapsed = QTime(0, 0).addSecs(duration)

        # message = QMessageBox()
        # message.setWindowTitle("Recording Summary")
        # message.setText(f"Recording started at: {self.recording_start_time.toString('hh:mm:ss')}\n"
        #                 f"Recording stopped at: {recording_stop_time.toString('hh:mm:ss')}\n"
        #                 f"Duration: {elapsed.toString('hh:mm:ss')}\n"
        #                 f"Recording CSV File: {self.recording_csv_file}")
        # message.exec_()

        # self.recording_start_time = None
        # self.recording_label.setText("")
        # self.recording_csv_file = None
        pass

    def apply_styles(self):
        with open("./styles/styles.qss", 'r') as file:
            self.setStyleSheet(file.read())

