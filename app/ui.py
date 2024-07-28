import csv
import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QGridLayout, QWidget, QLabel, QHBoxLayout, QPushButton, QFrame, QSizePolicy, QScrollArea
from PyQt5.QtCore import QTimer, Qt, QDateTime, QDate ,QTime
from db_code.db_client import get_connection
from settings import SettingsDialog
from test_info import TestInfoDialog
from datetime import datetime, timedelta
from report import generate_pdf_report

class BatteryMonitoringSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Battery Monitoring System')
        self.resize(1200, 800)
        self.init_ui()
        self.apply_styles()
        self.current_bank_id = None
        # Timer to update data every 5 seconds
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_data)
        self.timer.start(5000)  # Update every 5 seconds

        self.prev_button = None
        #timeer
        self.recording_timer = None
        self.remaining_time = 0
        self.counter_timer = None

        #counter for bottom logging data 
        self.data_log_counter = 0
        
    def init_ui(self):
        self.setWindowTitle("Battery Management System V - 1.0.0")
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

         # Create the counter label
        self.counter_label = QLabel(self)
        self.counter_label.setAlignment(Qt.AlignCenter)
        self.counter_label.setStyleSheet("color: white; font-size: 16px;")
        top_bar_layout.addWidget(self.counter_label)

        # Left-aligned layout
        left_layout = QHBoxLayout()
        left_layout.setAlignment(Qt.AlignLeft)
        top_bar_label = QLabel("Battery Management System V - 1.0.0", self)
        top_bar_label.setStyleSheet("font-size: 12px; font-weight: bold;")
        left_layout.addWidget(top_bar_label)

        # Right-aligned layout
        right_layout = QVBoxLayout()
        right_layout.setAlignment(Qt.AlignRight)
        date = QLabel(f"Date: {QDate.currentDate().toString('yyyy-MM-dd')}")
        self.clock = QLabel(f"Time(IST): {QDateTime.currentDateTime().toString('hh:mm:ss')}")
        date.setStyleSheet("font-size: 10px; padding: 5px;")
        self.clock.setStyleSheet("font-size: 10px; padding: 5px;")
        right_layout.addWidget(date)
        right_layout.addWidget(self.clock)

        # Add left and right layouts to the top bar layout
        top_bar_layout.addLayout(left_layout)
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
        # self.data_log_counter = 0
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
        main_layout.addWidget(bottom_bar)

        self.load_banks()
        self.add_additional_buttons()

        # Timer for real-time clock
        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self.update_clock)
        self.clock_timer.start(1000)  # Update every second

    def update_clock(self):
        self.clock.setText(f"Time(IST): {QDateTime.currentDateTime().toString('hh:mm:ss')}")

    def load_banks(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name FROM banks")
        banks = cur.fetchall()
        cur.close()
        conn.close()

        # Add a label for the new section
        section_label = QLabel("Avaliable Banks", self)
        section_label.setStyleSheet("font-size: 14px; font-weight: bold; margin-top: 20px; color: white;")
        self.left_menu_layout.addWidget(section_label)

        for bank in banks:
            button = QPushButton(bank[1], self)
            button.setStyleSheet("""
                                        QPushButton {
                                        background-color: #1E3D58;
                                        color: white;
                                        border: none;
                                        font-size: 16px;
                                        padding: 5px;
                                    }
                                    QPushButton:hover {
                                        background-color: #50B498;
                                        color: black;
                                    }
                                """)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            button.setFixedHeight(40)
            button.clicked.connect(lambda _, bank_id=bank[0], btn=button: self.on_menu_button_click(bank_id, btn))
            self.left_menu_layout.addWidget(button)

    def on_menu_button_click(self, bank_id, button):
        self.current_bank_id = bank_id
        if self.prev_button:
            # self.prev_button.setStyleSheet("background-color: #1E3D58; color: white; border: none; font-size: 16px; padding: 5px;")
            self.prev_button.setStyleSheet("""
                                        QPushButton {
                                        background-color: #1E3D58;
                                        color: white;
                                        border: none;
                                        font-size: 16px;
                                        padding: 5px;
                                    }
                                    QPushButton:hover {
                                        background-color: #50B498;
                                        color: black;
                                    }
                                """)
        
        button.setStyleSheet("background-color: #50B498; color: black; border: none; font-size: 16px; padding: 5px;")
        self.prev_button = button

        self.display_batteries(bank_id)

    def fetch_serial_numbers(self, bank_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT serial_number
            FROM batteries
            WHERE bank_id = %s
            ORDER BY battery_number
        """, (bank_id,))
        serial_numbers = [row[0] for row in cur.fetchall()]
        cur.close()
        conn.close()
        return serial_numbers
    
    def display_batteries(self, bank_id):
        for i in reversed(range(self.grid_layout.count())):
            widget_to_remove = self.grid_layout.itemAt(i).widget()
            self.grid_layout.removeWidget(widget_to_remove)
            widget_to_remove.setParent(None)

        if bank_id:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT number_of_cells FROM banks WHERE id = %s", (bank_id,))
            number_of_cells = cur.fetchone()[0]
            cur.close()
            conn.close()

            self.labels = []
            self.serial_numbers = self.fetch_serial_numbers(bank_id)

            for i in range(number_of_cells):
                label = QLabel(f'Battery {i+1}')
                self.grid_layout.addWidget(label, i // 4, i % 4)
                self.labels.append(label)
                # self.serial_numbers.append()  # Initialize with empty serial numbers or load from DB

            self.update_data()

    def update_data(self):
        latest_row = self.read_latest_data('../data/battery_data.csv')
        if latest_row:
            for i, label in enumerate(self.labels):
                voltage = float(latest_row.get(f"Bank1.B{i+1}", 0))  # Default to 0 if key not found
                temp = float(latest_row.get(f"Temperature", 0))
                color = "#4E9F3D" if voltage > 6.5 else "#ED2B2A"
                serial_number = self.serial_numbers[i]
                text = f'Battery {i+1}: {serial_number} '
                text += f"\nVoltage: {voltage} V"
                text += f'\nTemp.: {temp} C'
                # if serial_number:
                #     text += f'\nSerial: {serial_number}'
                label.setStyleSheet(f"background-color: {color}; color: white; border: 0.5px solid black; border-radius: 5px; padding: 10px;")
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
        if self.current_bank_id is None:
            return
        number_of_cells = len(self.labels)  # Get the number of cells based on the labels
        dialog = SettingsDialog(self, self.serial_numbers, number_of_cells)
        dialog.save_data.connect(self.save_serial_numbers)
        if dialog.exec_():
            self.serial_numbers = dialog.get_serial_numbers()
            self.update_data()
    
    def save_serial_numbers(self, serial_numbers):
        conn = get_connection()
        cur = conn.cursor()

        # Update the serial numbers in the batteries table based on the current_bank_id
        for i, serial_number in enumerate(serial_numbers):
            # Assuming the batteries table has columns `battery_id`, `bank_id`, and `serial_number`
            battery_id = i + 1  # Adjust based on your logic for battery_id
            cur.execute("""
                UPDATE batteries
                SET serial_number = %s
                WHERE battery_number = %s AND bank_id = %s
            """, (serial_number, battery_id, self.current_bank_id))
        
        conn.commit()
        cur.close()
        conn.close()

    def open_test_info_dialog(self):
        if(self.current_bank_id):
            dialog = TestInfoDialog(self)
            if dialog.exec_():
                self.test_details = dialog.get_test_details()
                # self.start_recording()

    def start_test_recording(self, test_run_id, test_duration):
        print("Recording started")
        # Set the remaining time to the test duration
        self.remaining_time = test_duration * 60 * 60 # Convert minutes to seconds
        
        # Create a QTimer for updating the counter
        self.counter_timer = QTimer(self)
        self.counter_timer.timeout.connect(self.update_counter)
        self.counter_timer.start(1000)  # Update every second

        self.test_run_id = test_run_id
        self.test_end_time = datetime.now() + timedelta(minutes=test_duration*60)
        self.record_data()  # Record initial data

        # Set up a QTimer to record data every 15 minutes
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.record_data)
        self.timer.start(2 * 60 * 1000)  # 15 minutes in milliseconds

    #Counter for reaming timimg
    def update_counter(self):
        if self.remaining_time > 0:
            self.remaining_time -= 1
            time_str = str(QTime(0, 0).addSecs(int(self.remaining_time)).toString("hh:mm:ss"))
            self.counter_label.setText(f"Remaining Time: {time_str}")
        else:
            self.counter_timer.stop()

    #function to update the test_run db
    def update_test_run(self, status):
        end_time = datetime.now()
        if 'start_time' not in self.test_details:
            self.test_details['start_time'] = self.get_test_run_start_time(self.test_run_id)
        duration_tested = end_time - self.test_details['start_time']
        
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
  
    def record_data(self):
        # Check if the test duration has passed
        if datetime.now() >= self.test_end_time:
            self.timer.stop()
            self.update_test_run('completed')
            print("Test recording completed")
            return

        latest_row = self.read_latest_data('../data/battery_data.csv')
        if self.current_bank_id:
            if latest_row:
                for i, label in enumerate(self.labels):
                    conn = get_connection()
                    cur = conn.cursor()
                    table_name = f"recorded_data_{self.current_bank_id}"
                    cur.execute(f"""
                        INSERT INTO {table_name} (test_run_id, battery_number, voltage, current, temperature)
                        VALUES (%s, %s, %s, %s, %s) RETURNING id
                    """, (self.test_run_id, i + 1, latest_row.get(f"Bank1.B{i + 1}"), latest_row.get("Current", 0), latest_row.get("Temperature", 0)))
                    conn.commit()
                    cur.close()
                    conn.close()
                self.data_log_counter +=1
                self.update_data_log_count(self.data_log_counter)
                print("Data recorded at", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))  

    def stop_recording(self):
        if self.recording_timer:
            self.recording_timer.stop()
        if self.counter_timer:
            self.counter_timer.stop()
        
        # Fetch the start time from the database if not present in test_details
        if 'start_time' not in self.test_details:
            self.test_details['start_time'] = self.get_test_run_start_time(self.test_run_id)
        
        # Update the test run status
        self.update_test_run('pending')
    
    # Method to get the start_time from the test_runs table
    def get_test_run_start_time(self, test_run_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT start_time FROM test_runs WHERE id = %s
        """, (test_run_id,))
        start_time = cur.fetchone()[0]
        cur.close()
        conn.close()
        return start_time

    #Method for updating the counter of data logging
    def update_data_log_count(self, count):
        self.bottom_bar_data_points.setText(f"Data points logged: {count}")

    def add_additional_buttons(self):
        # Add a label for the new section
        section_label = QLabel("Menu", self)
        section_label.setStyleSheet("font-size: 14px; font-weight: bold; margin-top: 20px; color: white;")
        self.left_menu_layout.addWidget(section_label)        
        # Add the additional buttons
        # options = ["Graph", "Reports", "Test History", "About"]
        options = ["Graph", "Reports",  "About"]
        for option in options:
            button = QPushButton(option, self)
            button.setStyleSheet("""
                                        QPushButton {
                                        background-color: #1E3D58;
                                        color: white;
                                        border: none;
                                        font-size: 16px;
                                        padding: 5px;
                                    }
                                    QPushButton:hover {
                                        background-color: #50B498;
                                        color: black;
                                    }
                                """)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            button.setFixedHeight(40)
            # Connect buttons to appropriate slots or methods
            if option == "Graph":
                button.clicked.connect(self.show_graph)
            elif option == "Reports":
                button.clicked.connect(self.show_reports)
            # elif option == "Test History":
            #     button.clicked.connect(self.show_test_history)
            elif option == "About":
                button.clicked.connect(self.show_about)
            self.left_menu_layout.addWidget(button)

    def show_graph(self):
        pass  # Add logic to show graph

    def show_reports(self):
        pass  # Add logic to show reports

    # def show_test_history(self):
    #     pass  # Add logic to show test history

    def show_about(self):
        pass  # Add logic to show about

    def apply_styles(self):
        with open("./styles/styles.qss", 'r') as file:
            self.setStyleSheet(file.read())

