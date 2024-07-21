import sys
import csv
from PyQt5.QtWidgets import (
    QMainWindow, QLabel, QVBoxLayout, QWidget, QGridLayout, QHBoxLayout, QPushButton,
    QApplication, QMessageBox
)
from PyQt5.QtCore import QTimer, QTime, Qt, QDateTime
from PyQt5.QtGui import QFont
from settings import SettingsDialog
from test_info import TestInfoDialog
from report import generate_pdf_report
from data_handler import read_latest_data

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Battery Data Monitoring'
        self.setGeometry(0, 0, QApplication.desktop().screenGeometry().width(), QApplication.desktop().screenGeometry().height())
        self.serial_numbers = [None] * 19
        self.test_details = {}
        self.recording_start_time = None
        self.recording_timer = QTimer()
        self.elapsed_time = 0
        self.recording_csv_file = None
        self.last_recording_timestamp = None  
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.showMaximized()

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        header_layout = QHBoxLayout()
        layout.addLayout(header_layout)

        self.clock = QLabel('', self)
        self.clock.setFont(QFont('Arial', 12, QFont.Bold))
        header_layout.addWidget(self.clock, alignment=Qt.AlignRight | Qt.AlignTop)

        self.recording_label = QLabel('', self)
        self.recording_label.setFont(QFont('Arial', 12, QFont.Bold))
        header_layout.addWidget(self.recording_label, alignment=Qt.AlignLeft | Qt.AlignTop)

        self.grid_layout = QGridLayout()
        layout.addLayout(self.grid_layout)

        self.labels = self.create_grid()

        self.button_layout = QHBoxLayout()
        layout.addLayout(self.button_layout)

        self.settings_button = QPushButton('Settings', self)
        self.start_button = QPushButton('Start', self)
        self.stop_button = QPushButton('Stop', self)
        self.report_button = QPushButton('Report', self)

        self.button_layout.addWidget(self.settings_button)
        self.button_layout.addWidget(self.start_button)
        self.button_layout.addWidget(self.stop_button)
        self.button_layout.addWidget(self.report_button)

        self.settings_button.clicked.connect(self.open_settings_dialog)
        self.start_button.clicked.connect(self.open_test_info_dialog)
        self.stop_button.clicked.connect(self.stop_recording)
        self.report_button.clicked.connect(generate_pdf_report)

        # Set up a timer to refresh the data every 5 seconds
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(5000)

        # Set up a timer to update the clock every second
        self.clock_timer = QTimer()
        self.clock_timer.timeout.connect(self.update_clock)
        self.clock_timer.start(1000)

        self.apply_styles()

    def create_grid(self):
        labels = []
        for i in range(19):
            label = QLabel(f'Battery {i+1}: N/A', self)
            label.setFont(QFont('Arial', 10))
            label.setAlignment(Qt.AlignCenter)
            self.grid_layout.addWidget(label, i // 4, i % 4)
            labels.append(label)
        return labels

    def update_data(self):
        latest_row = read_latest_data('../data/battery_data.csv')
        if latest_row:
            current_time = QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss')
            if self.recording_csv_file:
                # Check if new data is available since the last write
                if self.last_recording_timestamp != current_time:
                    self.write_to_recording_csv(latest_row)
                    self.last_recording_timestamp = current_time

            for i, label in enumerate(self.labels):
                voltage = float(latest_row[f"Bank1.B{i+1}"])
                color = "#4E9F3D" if voltage > 6.5 else "#ED2B2A"
                serial_number = self.serial_numbers[i]
                text = f'Battery {i+1}: {voltage} V'
                if serial_number:
                    text += f'\nSerial: {serial_number}'
                label.setStyleSheet(f"background-color: {color}; color: white; border: 0.5px solid black; border-radius: 5px; padding: 35px;")
                label.setText(text)

    def write_to_recording_csv(self, battery_data):
        if self.recording_csv_file:
            with open(self.recording_csv_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                if file.tell() == 0:
                    writer.writerow([
                        "DateTime", "Bank1.B1", "Bank1.B2", "Bank1.B3", "Bank1.B4", "Bank1.B5", 
                        "Bank1.B6", "Bank1.B7", "Bank1.B8", "Bank1.B9", "Bank1.B10", "Bank1.B11", 
                        "Bank1.B12", "Bank1.B13", "Bank1.B14", "Bank1.B15", "Bank1.B16", "Bank1.B17", 
                        "Bank1.B18", "Bank1.B19", "Temperature", "Current"
                    ])
                current_time = QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss')
                row = [current_time]
                for key in [
                    "Bank1.B1", "Bank1.B2", "Bank1.B3", "Bank1.B4", "Bank1.B5", "Bank1.B6",
                    "Bank1.B7", "Bank1.B8", "Bank1.B9", "Bank1.B10", "Bank1.B11", "Bank1.B12",
                    "Bank1.B13", "Bank1.B14", "Bank1.B15", "Bank1.B16", "Bank1.B17", "Bank1.B18",
                    "Bank1.B19", "Temperature", "Current"
                ]:
                    row.append(battery_data[key])
                writer.writerow(row)

    def update_clock(self):
        current_time = QTime.currentTime().toString('hh:mm:ss')
        self.clock.setText(current_time)

        if self.recording_start_time:
            elapsed = QTime(0, 0).addSecs(self.elapsed_time)
            self.recording_label.setText(f"Recording: {elapsed.toString('hh:mm:ss')}")
            self.elapsed_time += 1

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

    def start_recording(self):
        self.recording_start_time = QDateTime.currentDateTime()
        self.elapsed_time = 0
        self.recording_csv_file = f"../data/recording_{self.recording_start_time.toString('yyyyMMdd_hhmmss')}.csv"
        self.last_recording_timestamp = None  # Initialize with None
        self.recording_timer.start(1000)
        self.start_button.setEnabled(False)

    def stop_recording(self):
        self.recording_timer.stop()
        self.start_button.setEnabled(True)
        recording_stop_time = QDateTime.currentDateTime()
        duration = self.recording_start_time.secsTo(recording_stop_time)
        elapsed = QTime(0, 0).addSecs(duration)

        message = QMessageBox()
        message.setWindowTitle("Recording Summary")
        message.setText(f"Recording started at: {self.recording_start_time.toString('hh:mm:ss')}\n"
                        f"Recording stopped at: {recording_stop_time.toString('hh:mm:ss')}\n"
                        f"Duration: {elapsed.toString('hh:mm:ss')}\n"
                        f"Recording CSV File: {self.recording_csv_file}")
        message.exec_()

        self.recording_start_time = None
        self.recording_label.setText("")
        self.recording_csv_file = None

    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ffffff;
            }
            QLabel {
                font-family: Arial;
                font-size: 12pt;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
                margin: 5px;
                background-color: #ffffff;
            }
            QPushButton {
                background-color: #468585;
                color: white;
                border: none;
                padding: 10px 24px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 14px;
                margin: 4px 2px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #50B498;
            }
            QDialog {
                background-color: #ffffff;
            }
            QLineEdit {
                border: 1px solid #ddd;
                padding: 5px;
                border-radius: 5px;
            }
            QDialogButtonBox {
                background-color: #f5f5f5;
            }
        """)
