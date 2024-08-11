from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QGridLayout, QWidget, QLabel, QHBoxLayout, QPushButton, QFrame, QSizePolicy, QScrollArea
from PyQt5.QtCore import QTimer, Qt, QDateTime, QDate, QTime, QThread, pyqtSignal
from settings import SettingsDialog
from test_info import TestInfoDialog
from datetime import datetime, timedelta
from report import generate_pdf_report
from db_code.db_client import get_connection
from utils.db_utils import fetch_serial_numbers, get_test_run_start_time, get_no_cells, get_bank
from utils.csv_utils import read_latest_data

class TestThread(QThread):
    update_signal = pyqtSignal(int, dict)

    def __init__(self, bank_id, test_run_id, test_duration, labels, serial_numbers, parent=None):
        super().__init__(parent)
        self.bank_id = bank_id
        self.test_run_id = test_run_id
        self.test_duration = test_duration
        self.labels = labels
        self.serial_numbers = serial_numbers
        self.running = True

    def run(self):
        start_time = datetime.now()
        end_time = start_time + timedelta(seconds=self.test_duration * 60 * 60)
        while self.running and datetime.now() < end_time:
            latest_row = read_latest_data('../data/battery_data.csv')
            if latest_row:
                update_data = {}
                total_voltage = 0
                total_current = 0

                for i, label in enumerate(self.labels):
                    voltage = float(latest_row.get(f"Bank1.B{i + 1}", 0))  # Default to 0 if key not found
                    total_voltage += voltage
                    temp = float(latest_row.get(f"Temperature", 0))
                    current = float(latest_row.get(f"Current", 0))

                    color = "#4E9F3D" if voltage > 6.5 else "#ED2B2A"
                    serial_number = self.serial_numbers[i]
                    text = f'{serial_number}\nVoltage: {voltage} V\nTemp.: {temp} C'
                    update_data[i] = {"text": text, "color": color, "voltage": voltage, "current": current}

                self.update_signal.emit(self.bank_id, update_data)
                QThread.sleep(15 * 60)  # Sleep for 15 minutes

        # Final update to mark completion
        if self.running:
            self.update_test_run('completed')

    def stop(self):
        self.running = False

    def update_test_run(self, status):
        end_time = datetime.now()
        duration_tested = end_time - get_test_run_start_time(self.test_run_id)

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE test_runs
            SET end_time = %s, status = %s, duration_tested = %s
            WHERE id = %s
        """, (end_time, status, duration_tested, self.test_run_id))

        conn.commit()
        cur.close()
        conn.close()


class BatteryMonitoringSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Battery Monitoring System')
        self.resize(1200, 800)
        self.init_ui()
        self.apply_styles()
        self.current_bank_id = None
        self.running_tests = {}  # Store threads for running tests

    def init_ui(self):
        self.setWindowTitle("Battery Monitoring System V - 1.0.0")
        self.showMaximized()

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Create top bar
        top_bar = QFrame(self)
        top_bar.setObjectName("top_bar")
        top_bar.setStyleSheet("background-color: #1E3D58; color: white;")
        top_bar.setFixedHeight(100)

        top_bar_layout = QHBoxLayout(top_bar)
        top_bar_layout.setContentsMargins(10, 0, 10, 0)
        top_bar_layout.setSpacing(0)

        # Left-aligned layout
        left_layout = QHBoxLayout()
        left_layout.setAlignment(Qt.AlignLeft)
        top_bar_label = QLabel("Battery Monitoring \n System V - 1.0.0", self)
        top_bar_label.setStyleSheet("font-size: 16px; font-weight: bold; border:none")
        left_layout.addWidget(top_bar_label)

        # Center-aligned layout for recording status and remaining time
        center_layout = QVBoxLayout()
        center_layout.setAlignment(Qt.AlignCenter)

        # Create the recording status label
        self.recording_status_label = QLabel("Not Recording...")
        self.recording_status_label.setStyleSheet("color: red; font-weight: bold; border:none;")
        center_layout.addWidget(self.recording_status_label)

        # Create the counter label for remaining time
        self.counter_label = QLabel(self)
        self.counter_label.setAlignment(Qt.AlignCenter)
        self.counter_label.setStyleSheet("color: white; font-size: 16px; border:none")
        center_layout.addWidget(self.counter_label)

        # Right-aligned layout
        right_layout = QVBoxLayout()
        right_layout.setAlignment(Qt.AlignRight)
        date = QLabel(f"Date: {QDate.currentDate().toString('yyyy-MM-dd')}")
        self.clock = QLabel(f"Time(IST): {QDateTime.currentDateTime().toString('hh:mm:ss')}")
        date.setStyleSheet("font-size: 14px; padding: 5px; font-weight: bold;")
        self.clock.setStyleSheet("font-size: 14px; padding: 5px; font-weight: bold;")
        right_layout.addWidget(date)
        right_layout.addWidget(self.clock)

        # Add left, center, and right layouts to the top bar layout
        top_bar_layout.addLayout(left_layout)
        top_bar_layout.addStretch()
        top_bar_layout.addLayout(center_layout)
        top_bar_layout.addStretch()
        top_bar_layout.addLayout(right_layout)

        main_layout.addWidget(top_bar)

        # Create main layout with left menu and central area
        main_content = QHBoxLayout()
        main_layout.addLayout(main_content)

        # Create left menu
        self.left_menu = QFrame(self)
        self.left_menu.setObjectName("left_menu")
        self.left_menu.setStyleSheet("background-color: #1E3D58; color: white;")
        self.left_menu.setFixedWidth(200)
        self.left_menu_layout = QVBoxLayout(self.left_menu)
        self.left_menu_layout.setAlignment(Qt.AlignTop)

        main_content.addWidget(self.left_menu)

        # Create central area with scroll area for grid
        central_area = QWidget(self)
        central_layout = QVBoxLayout(central_area)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.grid_widget = QWidget(self)
        self.grid_layout = QGridLayout(self.grid_widget)
        self.scroll_area.setWidget(self.grid_widget)
        central_layout.addWidget(self.scroll_area)

        # Create a horizontal layout for buttons
        button_layout = QHBoxLayout()
        central_layout.addLayout(button_layout)

        self.settings_button = QPushButton("Settings", self)
        self.settings_button.clicked.connect(self.open_test_info_dialog)
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

        self.labels = {}  # To store QLabel references by bank_id
        self.serial_numbers = {}
        main_content.addWidget(central_area)

        # Create bottom bar
        bottom_bar = QFrame(self)
        bottom_bar.setObjectName("bottom_bar")
        bottom_bar.setStyleSheet("background-color: #1E3D58; color: white;")
        bottom_bar.setFixedHeight(60)
        bottom_bar_layout = QHBoxLayout(bottom_bar)
        bottom_bar_layout.setAlignment(Qt.AlignLeft)
        bottom_bar_label = QLabel("Device Status: Connected/Disconnected/Ready", self)
        bottom_bar_label.setStyleSheet("font-size: 14px; margin-left: 20px;")
        bottom_bar_layout.addWidget(bottom_bar_label)
        self.bottom_bar_data_points = QLabel("Data points logged: 0", self)
        self.bottom_bar_data_points.setStyleSheet("font-size: 14px; margin-left: 20px;")
        bottom_bar_layout.addWidget(self.bottom_bar_data_points)

        # Timer Label
        self.timer_label = QLabel("Next data log in: 15:00")
        self.timer_label.setStyleSheet("font-size: 14px; margin-left: 20px;")
        bottom_bar_layout.addWidget(self.timer_label)

        main_layout.addWidget(bottom_bar)

        self.load_banks()
        self.add_additional_buttons()

        # Timer for real-time clock
        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self.update_time)
        self.clock_timer.start(1000)

    def load_banks(self):
        banks = get_bank()
        for bank in banks:
            # print(bank)
            self.add_bank_button(bank[0], bank[1])

    def add_bank_button(self, bank_id, bank_name):
        button = QPushButton(bank_name, self)
        button.clicked.connect(lambda _, b=bank_id: self.display_bank_grid(b))
        self.left_menu_layout.addWidget(button)

    def display_bank_grid(self, bank_id):
        self.current_bank_id = bank_id
        # Clear existing grid layout
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        # Add labels to grid layout
        self.labels[bank_id] = []
        self.serial_numbers[bank_id] = fetch_serial_numbers(bank_id)

        for i in range(3):  # Assuming 3 rows
            for j in range(3):  # Assuming 3 columns
                if i * 3 + j < len(self.serial_numbers[bank_id]):
                    label = QLabel(f"Cell {i * 3 + j + 1}", self)
                    label.setFixedSize(200, 100)
                    label.setAlignment(Qt.AlignCenter)
                    label.setStyleSheet("background-color: #F4F4F4; border: 1px solid #C0C0C0;")
                    self.grid_layout.addWidget(label, i, j)
                    self.labels[bank_id].append(label)

    def update_labels(self, bank_id, data):
        if bank_id in self.labels:
            for i, label_data in data.items():
                label = self.labels[bank_id][i]
                label.setText(label_data["text"])
                label.setStyleSheet(f"background-color: {label_data['color']}; border: 1px solid #C0C0C0;")

    def open_test_info_dialog(self):
        dialog = TestInfoDialog(self)
        if dialog.exec_():
            self.test_details = dialog.get_test_details()
            test_duration = self.test_details['test_duration']
            if self.current_bank_id is not None:
                self.start_test_run(self.current_bank_id, test_duration)

    def start_test_run(self, bank_id, test_duration):
        serial_numbers = fetch_serial_numbers(bank_id)
        test_run_id = 123  # Replace with actual test run ID from your DB

        thread = TestThread(bank_id, test_run_id, test_duration, self.labels[bank_id], serial_numbers)
        thread.update_signal.connect(self.update_labels)
        self.running_tests[bank_id] = thread
        thread.start()

    def stop_recording(self):
        if self.current_bank_id in self.running_tests:
            self.running_tests[self.current_bank_id].stop()
            self.running_tests[self.current_bank_id].wait()
            del self.running_tests[self.current_bank_id]

    def add_additional_buttons(self):
        buttons = [
            {'label': 'Battery 1', 'action': self.dummy_action},
            {'label': 'Battery 2', 'action': self.dummy_action},
            {'label': 'Battery 3', 'action': self.dummy_action},
            {'label': 'Battery 4', 'action': self.dummy_action},
        ]
        for button_data in buttons:
            button = QPushButton(button_data['label'], self)
            button.clicked.connect(button_data['action'])
            self.left_menu_layout.addWidget(button)

    def dummy_action(self):
        print("Dummy action executed")

    def update_time(self):
        self.clock.setText(f"Time(IST): {QDateTime.currentDateTime().toString('hh:mm:ss')}")

    def apply_styles(self):
        self.setStyleSheet("""
            QPushButton {
                background-color: #4E9F3D;
                color: white;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #ED2B2A;
            }
            QPushButton:pressed {
                background-color: #1E3D58;
            }
        """)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = BatteryMonitoringSystem()
    window.show()
    sys.exit(app.exec_())
