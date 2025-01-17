from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QGridLayout, QWidget, QLabel, QHBoxLayout, QPushButton, QFrame, QSizePolicy, QScrollArea, QStackedWidget
from PyQt5.QtCore import QTimer, Qt, QDateTime, QDate, QTime

from settings import SettingsDialog
from test_info import TestInfoDialog
from datetime import datetime, timedelta
from report import generate_pdf_report
from db_code.db_client import get_connection
from utils.db_utils import fetch_serial_numbers, get_test_run_start_time, get_no_cells, get_bank
from utils.csv_utils import read_latest_data

from pages.graph import GraphPage
from pages.about import AboutPage
from pages.reports import ReportPage

class BatteryMonitoringSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Battery Monitoring System')
        self.resize(1200, 800)
        self.init_ui()
        self.apply_styles()
        self.current_bank_id = None

        # Dictionary to store the state of multiple banks
        self.bank_tests = {}

        # Timer for real-time clock
        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self.update_clock)
        self.clock_timer.start(1000)  # Update every second

        # Initialize Timer to update data every 5 seconds
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_data)  # Connect to a method that updates data for the current bank
        self.timer.start(5000)  # 5000 milliseconds = 5 seconds

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

        # Center-aligned layout for recording status, test name, and remaining time
        center_layout = QVBoxLayout()
        center_layout.setAlignment(Qt.AlignCenter)

        # Create the recording status label
        self.recording_status_label = QLabel("Not Recording...", self)
        self.recording_status_label.setStyleSheet("color: red; font-weight: bold; border:none")
        center_layout.addWidget(self.recording_status_label)

        # Create a horizontal layout for test name, duration, and counter
        test_info_layout = QHBoxLayout()
        test_info_layout.setAlignment(Qt.AlignCenter)

        # Create the test name and duration labels (these will be updated dynamically)
        self.test_name_label = QLabel("Test: N/A", self)
        self.test_name_label.setStyleSheet("color: white; font-size: 16px; font-weight: bold; margin-right: 20px;")
        test_info_layout.addWidget(self.test_name_label)

        self.test_duration_label = QLabel("Duration: 0 hrs", self)
        self.test_duration_label.setStyleSheet("color: white; font-size: 16px; font-weight: bold; margin-right: 20px;")
        test_info_layout.addWidget(self.test_duration_label)

        # Create the counter label for remaining time
        self.counter_label = QLabel(self)
        self.counter_label.setAlignment(Qt.AlignCenter)
        self.counter_label.setStyleSheet("color: white; font-size: 16px; border:none")
        test_info_layout.addWidget(self.counter_label)

        center_layout.addLayout(test_info_layout)

        # Right-aligned layout
        right_layout = QVBoxLayout()
        right_layout.setAlignment(Qt.AlignRight)
        date = QLabel(f"Date: {QDate.currentDate().toString('yyyy-MM-dd')}", self)
        self.clock = QLabel(f"Time(IST): {QDateTime.currentDateTime().toString('hh:mm:ss')}", self)
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

        # # Create central area with scroll area for grid
        # central_area = QWidget(self)
        # central_layout = QVBoxLayout(central_area)

        # self.scroll_area = QScrollArea(self)
        # self.scroll_area.setWidgetResizable(True)
        # self.grid_widget = QWidget(self)
        # self.grid_layout = QGridLayout(self.grid_widget)
        # self.scroll_area.setWidget(self.grid_widget)
        # central_layout.addWidget(self.scroll_area)

        # # Create a horizontal layout for buttons
        # button_layout = QHBoxLayout()
        # central_layout.addLayout(button_layout)

        # self.settings_button = QPushButton("Settings", self)
        # self.settings_button.clicked.connect(self.open_settings_dialog)
        # button_layout.addWidget(self.settings_button)

        # self.start_button = QPushButton("Start", self)
        # self.start_button.clicked.connect(self.open_test_info_dialog)
        # button_layout.addWidget(self.start_button)

        # self.stop_button = QPushButton("Stop", self)
        # self.stop_button.clicked.connect(self.stop_recording)
        # button_layout.addWidget(self.stop_button)

        # self.report_button = QPushButton("Report", self)
        # self.report_button.clicked.connect(generate_pdf_report)
        # button_layout.addWidget(self.report_button)


        # # Initialize the QStackedWidget
        # self.stacked_widget = QStackedWidget(self)

        # # Create and add the pages to the QStackedWidget
        # self.graph_page = GraphPage()
        # self.report_page = ReportPage()
        # self.about_page = AboutPage()

        # self.stacked_widget.addWidget(self.graph_page)
        # self.stacked_widget.addWidget(self.report_page)
        # self.stacked_widget.addWidget(self.about_page)
        # # Add the stacked widget to the central area of the main content layout
        # main_content.addWidget(self.stacked_widget)

        # main_content.addWidget(central_area)

            # Create the bank details widget (scroll area + buttons)
        self.bank_details_widget = QWidget(self)
        bank_details_layout = QVBoxLayout(self.bank_details_widget)

        # Scroll area with grid layout for battery cells
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.grid_widget = QWidget(self)
        self.grid_layout = QGridLayout(self.grid_widget)
        self.scroll_area.setWidget(self.grid_widget)
        bank_details_layout.addWidget(self.scroll_area)

        # Button layout (Settings, Start, Stop, Report)
        button_layout = QHBoxLayout()
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

        bank_details_layout.addLayout(button_layout)

        # Add the bank details widget to the main content
        main_content.addWidget(self.bank_details_widget)

        # Initialize the QStackedWidget for the other pages
        self.stacked_widget = QStackedWidget(self)

        # Create and add the pages to the QStackedWidget
        self.graph_page = GraphPage()
        self.report_page = ReportPage()
        self.about_page = AboutPage()

        self.stacked_widget.addWidget(self.graph_page)
        self.stacked_widget.addWidget(self.report_page)
        self.stacked_widget.addWidget(self.about_page)

        # Add the stacked widget to the main content
        main_content.addWidget(self.stacked_widget)

        # Hide the stacked widget by default (only show it when a menu item is selected)
        self.stacked_widget.hide()

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
        self.timer_label = QLabel("Next data log in: 15:00", self)
        self.timer_label.setStyleSheet("font-size: 14px; margin-left: 20px;")
        bottom_bar_layout.addWidget(self.timer_label)

        main_layout.addWidget(bottom_bar)

        self.load_banks()
        self.add_additional_buttons()

    # IST clock
    def update_clock(self):
        self.clock.setText(f"Time(IST): {QDateTime.currentDateTime().toString('hh:mm:ss')}")

    def load_banks(self):
        banks = get_bank()
        # Add a label for the new section
        section_label = QLabel("Available Banks", self)
        section_label.setStyleSheet("font-size: 14px; font-weight: bold; margin-top: 20px; color: white;")
        self.left_menu_layout.addWidget(section_label)

        for bank in banks:
            button = QPushButton(bank[1], self)
            with open("./styles/button.qss", "r") as file:
                button.setStyleSheet(file.read())
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            button.setFixedHeight(40)
            button.clicked.connect(lambda _, bank_id=bank[0], btn=button: self.on_menu_button_click(bank_id, btn))
            self.left_menu_layout.addWidget(button)

    def refresh_data(self):
        if self.current_bank_id:
            self.update_data(self.current_bank_id)

    def on_menu_button_click(self, bank_id, button):
        self.bank_details_widget.show()
        self.stacked_widget.hide()
        if bank_id not in self.bank_tests:
            # Create the QLabel objects with styling immediately
            recording_status_label = QLabel("Not Recording...", self)
            recording_status_label.setStyleSheet("color: red; font-weight: bold;")

            counter_label = QLabel(self)
            counter_label.setStyleSheet("color: white; font-size: 16px;")

            test_name_label = QLabel("Test: N/A", self)
            test_name_label.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")

            test_duration_label = QLabel("Duration: 0 hrs", self)
            test_duration_label.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")

            self.bank_tests[bank_id] = {
                'labels': [],
                'serial_numbers': [],
                'is_recording': False,
                'timer': None,
                'recording_timer': None,
                'remaining_time': 0,
                'counter_timer': None,
                'data_log_counter': 0,
                'recording_status_label': recording_status_label,  # Independent recording status
                'counter_label': counter_label,  # Independent counter label
                'data_points_label': QLabel("Data points logged: 0", self),  # Independent data points counter
                'timer_label': QLabel("Next data log in: 00:00", self),  # Independent timer label
                'test_name_label': test_name_label,  # Independent test name label
                'test_duration_label': test_duration_label,  # Independent test duration label
            }

        self.current_bank_id = bank_id  # Set the current_bank_id here

        if 'prev_button' in self.bank_tests:
            with open("./styles/button.qss", "r") as file:
                self.bank_tests['prev_button'].setStyleSheet(file.read())

        button.setStyleSheet("background-color: #50B498; color: black; border: none; font-size: 16px; padding: 5px;")
        self.bank_tests['prev_button'] = button
        self.display_batteries(bank_id)
        self.update_ui_for_selected_bank(bank_id)  # Update the UI when switching banks

    def update_ui_for_selected_bank(self, bank_id):
        bank_test = self.bank_tests[bank_id]

        # Update recording status label
        self.recording_status_label.setText(bank_test['recording_status_label'].text())
        self.recording_status_label.setStyleSheet(bank_test['recording_status_label'].styleSheet())

        # Update counter label
        self.counter_label.setText(bank_test['counter_label'].text())
        self.counter_label.setStyleSheet(bank_test['counter_label'].styleSheet())

        # Update data points label
        self.bottom_bar_data_points.setText(bank_test['data_points_label'].text())
        self.timer_label.setText(bank_test['timer_label'].text())

        # Update test name and duration on the top bar
        self.test_name_label.setText(bank_test['test_name_label'].text())
        self.test_duration_label.setText(bank_test['test_duration_label'].text())

    def display_batteries(self, bank_id):
        bank_test = self.bank_tests[bank_id]

        for i in reversed(range(self.grid_layout.count())):
            widget_to_remove = self.grid_layout.itemAt(i).widget()
            self.grid_layout.removeWidget(widget_to_remove)
            widget_to_remove.setParent(None)

        if bank_id:
            number_of_cells = get_no_cells(bank_id)
            bank_test['labels'] = []
            bank_test['serial_numbers'] = fetch_serial_numbers(bank_id)

            # Add QLabel for total voltage and current at the top
            bank_test['total_voltage_label'] = QLabel('Total Voltage: 0 V\t\tTotal Current: 0 A')
            self.grid_layout.addWidget(bank_test['total_voltage_label'], 0, 0, 1, 4)
            bank_test['total_voltage_label'].setStyleSheet(
                "background-color: #50B498; color: #000; border: 0.5px solid black; border-radius: 5px; padding: 10px;")

            for i in range(number_of_cells):
                label = QLabel(f'Battery {i + 1}')
                self.grid_layout.addWidget(label, (i // 4) + 1, i % 4)  # Adjust the row and column index
                bank_test['labels'].append(label)

            self.update_data(bank_id)

    def update_data(self, bank_id):
        bank_test = self.bank_tests[bank_id]

        latest_row = read_latest_data('../data/battery_data.csv')  # No bank_id needed here
        if latest_row:
            total_voltage = 0
            total_current = 0

            for i, label in enumerate(bank_test['labels']):
                # Assuming data for each battery is stored with a pattern like 'Bank1.B1', 'Bank2.B1', etc.
                voltage_key = f"Bank1.B{i + 1}"
                voltage = float(latest_row.get(voltage_key, 0))  # Default to 0 if key not found
                total_voltage += voltage
                temp = float(latest_row.get("Temperature", 0))
                current = float(latest_row.get("Current", 0))

                color = "#4E9F3D" if voltage > 6.5 else "#ED2B2A"
                serial_number = bank_test['serial_numbers'][i]
                text = f'{serial_number}'
                text += f"\nVoltage: {voltage:.2f} V"
                text += f'\nTemp.: {temp:.2f} C'
                label.setStyleSheet(f"background-color: {color}; color: white; border: 0.5px solid black; border-radius: 5px; padding: 10px;")
                label.setText(text)

            # Update total voltage and current for the specific bank
            bank_test['total_voltage_label'].setText(f'Total Voltage: {total_voltage:.2f} V\t\tTotal Current: {current:.2f} A')

        # If this is the currently selected bank, update the displayed data
        if bank_id == self.current_bank_id:
            self.update_ui_for_selected_bank(bank_id)

    def update_remaining_time_counter(self, bank_id):
        bank_test = self.bank_tests[bank_id]
        if bank_test['remaining_time'] > 0:
            bank_test['remaining_time'] -= 1
            time_str = QTime(0, 0).addSecs(int(bank_test['remaining_time'])).toString("hh:mm:ss")
            bank_test['counter_label'].setText(f"Remaining Time: {time_str}")
        else:
            bank_test['counter_timer'].stop()
            bank_test['counter_label'].setText("Test Completed")

        if bank_id == self.current_bank_id:
            self.counter_label.setText(bank_test['counter_label'].text())

    def open_settings_dialog(self):
        if self.current_bank_id is None:
            return
        
        bank_test = self.bank_tests[self.current_bank_id]
        dialog = SettingsDialog(self, bank_id=self.current_bank_id, serial_numbers=bank_test['serial_numbers'], number_of_cells=len(bank_test['labels']))
        dialog.save_data.connect(self.save_serial_numbers)
        if dialog.exec_():
            bank_test['serial_numbers'] = dialog.get_serial_numbers()
            self.update_data(self.current_bank_id)

    def save_serial_numbers(self, data):
        bank_id = data['bank_id']
        serial_numbers = data['serial_numbers']
        
        bank_test = self.bank_tests[bank_id]
        bank_test['serial_numbers'] = serial_numbers

        conn = get_connection()
        cur = conn.cursor()
        # Update the serial numbers in the batteries table based on the current bank_id
        for i, serial_number in enumerate(serial_numbers):
            battery_id = i + 1  
            cur.execute("""
                UPDATE batteries
                SET serial_number = %s
                WHERE battery_number = %s AND bank_id = %s
            """, (serial_number, battery_id, bank_id))
        
        conn.commit()
        cur.close()
        conn.close()

        # Optionally, update the displayed data for the current bank
        if bank_id == self.current_bank_id:
            self.update_data(bank_id)

    def open_test_info_dialog(self):
        bank_id = self.current_bank_id  # Ensure that the current_bank_id is being used
        bank_test = self.bank_tests[bank_id] if bank_id else None
        if not bank_test['is_recording']:
            if bank_id:
                dialog = TestInfoDialog(self, bank_id=bank_id)
                if dialog.exec_():
                    bank_test['test_details'] = dialog.get_test_details()

    def start_test_recording(self, bank_id, test_run_id, test_duration, test_name):
        bank_test = self.bank_tests[bank_id]
        if not bank_test['is_recording']:
            bank_test['is_recording'] = True
            bank_test['remaining_time'] = test_duration * 60 * 60  # Convert hours to seconds
            bank_test['test_run_id'] = test_run_id
            bank_test['test_end_time'] = datetime.now() + timedelta(hours=test_duration)

            # Update the test name and duration labels in the top bar
            bank_test['test_name_label'].setText(f"Test: {test_name}")
            bank_test['test_duration_label'].setText(f"Duration: {test_duration} hrs")

            if bank_id == self.current_bank_id:
                self.test_name_label.setText(bank_test['test_name_label'].text())
                self.test_duration_label.setText(bank_test['test_duration_label'].text())

            self.update_recording_status(bank_id)
            self.update_remaining_time_counter(bank_id)
            self.record_data(bank_id)

            # Start the counter for the remaining time
            bank_test['counter_timer'] = QTimer(self)
            bank_test['counter_timer'].timeout.connect(lambda: self.update_remaining_time_counter(bank_id))
            bank_test['counter_timer'].start(1000)  # Update every second

            # Start the 15-minute data logging timer
            bank_test['remaining_time_for_logging'] = 2 * 60  # 15 minutes in seconds
            bank_test['logging_timer'] = QTimer(self)
            bank_test['logging_timer'].timeout.connect(lambda: self.update_data_logging_timer(bank_id))
            bank_test['logging_timer'].start(1000)  # Update every second

    def update_counter(self, bank_id):
        bank_test = self.bank_tests[bank_id]
        if bank_test['remaining_time'] > 0:
            bank_test['remaining_time'] -= 1
            time_str = str(QTime(0, 0).addSecs(int(bank_test['remaining_time'])).toString("hh:mm:ss"))
            bank_test['counter_label'].setText(f"Remaining Time: {time_str}")
        else:
            bank_test['counter_timer'].stop()

        # If this is the currently selected bank, update the displayed label
        if bank_id == self.current_bank_id:
            self.counter_label.setText(bank_test['counter_label'].text())

    def update_test_run(self, bank_id, status):
        bank_test = self.bank_tests[bank_id]
        end_time = datetime.now()
        if 'start_time' not in bank_test['test_details']:
            bank_test['test_details']['start_time'] = get_test_run_start_time(bank_test['test_run_id'])
        duration_tested = end_time - bank_test['test_details']['start_time']

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE test_runs
            SET end_time = %s, status = %s, duration_tested = %s
            WHERE id = %s
        """, (end_time, status, duration_tested, bank_test['test_run_id']))

        conn.commit()
        cur.close()
        conn.close()

    def record_data(self, bank_id):
        bank_test = self.bank_tests[bank_id]

        # Stop logging if test has ended
        if datetime.now() >= bank_test['test_end_time']:
            bank_test['logging_timer'].stop()
            bank_test['is_recording'] = False
            self.update_test_run(bank_id, 'completed')
            return

        latest_row = read_latest_data('../data/battery_data.csv')
        if bank_id and latest_row:
            conn = get_connection()
            cur = conn.cursor()
            table_name = f"recorded_data_{bank_id}"

            # Gather all voltages and temperatures into arrays
            voltages = []
            temperatures = []
            for i in range(len(bank_test['labels'])):
                voltage = float(latest_row.get(f"Bank1.B{i + 1}", 0.0))
                temperature = float(latest_row.get("Temperature", 0.0))
                voltages.append(voltage)
                temperatures.append(temperature)

            # Calculate total_voltage and avg_temperature
            total_voltage = sum(voltages)
            avg_temperature = sum(temperatures) / len(temperatures) if temperatures else 0.0

            # Get current value
            current = float(latest_row.get("Current", 0.0))

            # Insert data into the table
            cur.execute(f"""
                INSERT INTO {table_name} (test_run_id, voltage, total_voltage, current, temperature, avg_temperature)
                VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
            """, (
                bank_test['test_run_id'],
                voltages,  # Array of all cell voltages
                total_voltage,  # Sum of all cell voltages
                current,
                temperatures,  # Array of all cell temperatures
                avg_temperature  # Average temperature
            ))

            conn.commit()
            cur.close()
            conn.close()

            # Update the UI
            bank_test['data_log_counter'] += 1
            bank_test['data_points_label'].setText(f"Data points logged: {bank_test['data_log_counter']}")

            # Reset the timer for the next logging interval
            bank_test['remaining_time_for_logging'] = 15 * 60  # Reset to 15 minutes
            self.update_data_logging_timer(bank_id)

    def update_data_logging_timer(self, bank_id):
        bank_test = self.bank_tests[bank_id]
        if bank_test['remaining_time_for_logging'] > 0:
            bank_test['remaining_time_for_logging'] -= 1
            time_str = QTime(0, 0).addSecs(int(bank_test['remaining_time_for_logging'])).toString("mm:ss")
            bank_test['timer_label'].setText(f"Next data log in: {time_str}")

            # If this is the currently selected bank, update the displayed label
            if bank_id == self.current_bank_id:
                self.timer_label.setText(bank_test['timer_label'].text())
        else:
            # Time to log data
            self.record_data(bank_id)
            # Reset the timer for the next 15-minute interval
            bank_test['remaining_time_for_logging'] = 2 * 60  # Reset to 15 minutes
            self.update_data_logging_timer(bank_id)  # Restart the countdown

    def stop_recording(self, bank_id=None):
        bank_id = bank_id or self.current_bank_id
        bank_test = self.bank_tests[bank_id]
        if bank_test['is_recording']:
            if bank_test['recording_timer']:
                bank_test['recording_timer'].stop()
            if bank_test['counter_timer']:
                bank_test['counter_timer'].stop()
            if bank_test['timer']:
                bank_test['timer'].stop()

            bank_test['is_recording'] = False
            self.update_recording_status(bank_id)

            if 'start_time' not in bank_test['test_details']:
                bank_test['test_details']['start_time'] = get_test_run_start_time(bank_test['test_run_id'])

            self.update_test_run(bank_id, 'pending')

    def update_recording_status(self, bank_id):
        bank_test = self.bank_tests[bank_id]
        if bank_test['is_recording']:
            bank_test['recording_status_label'].setText("Recording...")
            bank_test['recording_status_label'].setStyleSheet("color: green; font-weight: bold;")
        else:
            bank_test['recording_status_label'].setText("Not Recording...")
            bank_test['recording_status_label'].setStyleSheet("color: red; font-weight: bold;")

        # If this is the currently selected bank, update the displayed label
        if bank_id == self.current_bank_id:
            self.recording_status_label.setText(bank_test['recording_status_label'].text())
            self.recording_status_label.setStyleSheet(bank_test['recording_status_label'].styleSheet())

    def update_data_log_count(self, bank_id, count):
        self.bottom_bar_data_points.setText(f"Data points logged: {count}")

    # def add_additional_buttons(self):
    #     # Add a label for the new section
    #     section_label = QLabel("Menu", self)
    #     section_label.setStyleSheet("font-size: 14px; font-weight: bold; margin-top: 20px; color: white;")
    #     self.left_menu_layout.addWidget(section_label)
    #     # Add the additional buttons
    #     options = ["Graph", "Reports", "About"]
    #     for option in options:
    #         button = QPushButton(option, self)
    #         with open("./styles/button.qss", "r") as file:
    #             button.setStyleSheet(file.read())
    #         button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    #         button.setFixedHeight(40)
    #         if option == "Graph":
    #             button.clicked.connect(self.show_graph)
    #         elif option == "Reports":
    #             button.clicked.connect(self.show_reports)
    #         elif option == "About":
    #             button.clicked.connect(self.show_about)
    #         self.left_menu_layout.addWidget(button)

    def add_additional_buttons(self):
        section_label = QLabel("Menu", self)
        section_label.setStyleSheet("font-size: 14px; font-weight: bold; margin-top: 20px; color: white;")
        self.left_menu_layout.addWidget(section_label)
        
        options = ["Graph", "Reports", "About"]
        for i, option in enumerate(options):
            button = QPushButton(option, self)
            with open("./styles/button.qss", "r") as file:
                button.setStyleSheet(file.read())
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            button.setFixedHeight(40)
            if option == "Graph":
                button.clicked.connect(self.show_graph_page)
            elif option == "Reports":
                button.clicked.connect(self.show_report_page)
            elif option == "About":
                button.clicked.connect(self.show_about_page)
            self.left_menu_layout.addWidget(button)

    def show_graph_page(self):
        self.bank_details_widget.hide()
        self.recording_status_label.hide()
        self.test_duration_label.hide()
        self.test_name_label.hide()
        self.counter_label.hide()
        self.stacked_widget.show()
        self.stacked_widget.setCurrentWidget(self.graph_page)

    def show_report_page(self):
        self.bank_details_widget.hide()
        self.recording_status_label.hide()
        self.test_duration_label.hide()
        self.test_name_label.hide()
        self.counter_label.hide()
        self.stacked_widget.show()
        self.stacked_widget.setCurrentWidget(self.report_page)

    def show_about_page(self):
        self.bank_details_widget.hide()
        self.test_duration_label.hide()
        self.recording_status_label.hide()
        self.test_name_label.hide()
        self.counter_label.hide()
        self.stacked_widget.show()
        self.stacked_widget.setCurrentWidget(self.about_page)

    def update_timer(self, bank_id):
        bank_test = self.bank_tests[bank_id]
        bank_test['time_remaining'] = bank_test['time_remaining'].addSecs(-1)
        self.update_timer_label(bank_id)

        if bank_test['time_remaining'] == QTime(0, 0, 0):
            self.reset_timer(bank_id)

    def update_timer_label(self, bank_id):
        bank_test = self.bank_tests[bank_id]
        time_remaining = QTime(0, 0).addSecs(bank_test['remaining_time'])
        bank_test['timer_label'].setText(f"Next data log in: {time_remaining.toString('mm:ss')}")

        # If this is the currently selected bank, update the displayed label
        if bank_id == self.current_bank_id:
            self.timer_label.setText(bank_test['timer_label'].text())

    def reset_timer(self, bank_id):
        bank_test = self.bank_tests[bank_id]
        bank_test['time_remaining'] = QTime(0, 15, 0)

    def apply_styles(self):
        with open("./styles/styles.qss", 'r') as file:
            self.setStyleSheet(file.read())
