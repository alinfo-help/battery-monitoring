# from PyQt5.QtWidgets import  QMainWindow, QVBoxLayout, QGridLayout, QWidget, QLabel, QHBoxLayout, QPushButton, QFrame, QSizePolicy, QScrollArea
# from PyQt5.QtCore import QTimer, Qt, QDateTime, QDate ,QTime

# from settings import SettingsDialog
# from test_info import TestInfoDialog
# from datetime import datetime, timedelta
# from report import generate_pdf_report
# from db_code.db_client import get_connection
# from utils.db_utils import fetch_serial_numbers, get_test_run_start_time, get_no_cells, get_bank
# from utils.csv_utils import read_latest_data

# class BatteryMonitoringSystem(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle('Battery Monitoring System')
#         self.resize(1200, 800)
#         self.init_ui()
#         self.apply_styles()
#         self.current_bank_id = None
#         # Timer to update data every 5 seconds
#         self.timer = QTimer(self)
#         self.timer.timeout.connect(self.update_data)
#         self.timer.start(5000)  # Update every 5 seconds

#         self.prev_button = None
#         #timeer
#         self.recording_timer = None
#         self.remaining_time = 0
#         self.counter_timer = None

#         #counter for bottom logging data 
#         self.data_log_counter = 0
        
#         #flag for recording lable 
#         self.is_recording = False
        
#     def init_ui(self):
#         self.setWindowTitle("Battery Monitoring System V - 1.0.0")
#         self.showMaximized()

#         central_widget = QWidget(self)
#         self.setCentralWidget(central_widget)

#         main_layout = QVBoxLayout(central_widget)
#         main_layout.setContentsMargins(0, 0, 0, 0)

#         # Create top bar
#         top_bar = QFrame(self)
#         top_bar.setObjectName("top_bar")
#         top_bar.setStyleSheet("background-color: #1E3D58; color: white;")
#         top_bar.setFixedHeight(100)

#         top_bar_layout = QHBoxLayout(top_bar)
#         top_bar_layout.setContentsMargins(10, 0, 10, 0)
#         top_bar_layout.setSpacing(0)

#         # Left-aligned layout
#         left_layout = QHBoxLayout()
#         left_layout.setAlignment(Qt.AlignLeft)
#         top_bar_label = QLabel("Battery Monitoring \n System V - 1.0.0", self)
#         top_bar_label.setStyleSheet("font-size: 16px; font-weight: bold; border:none")
#         left_layout.addWidget(top_bar_label)

#         # Center-aligned layout for recording status and remaining time
#         center_layout = QVBoxLayout()
#         center_layout.setAlignment(Qt.AlignCenter)
        
#         # Create the recording status label
#         self.recording_status_label = QLabel("Not Recording...")
#         self.recording_status_label.setStyleSheet("color: red; font-weight: bold; border:none;")
#         center_layout.addWidget(self.recording_status_label)

#         # Create the counter label for remaining time
#         self.counter_label = QLabel(self)
#         self.counter_label.setAlignment(Qt.AlignCenter)
#         self.counter_label.setStyleSheet("color: white; font-size: 16px; border:none")
#         center_layout.addWidget(self.counter_label)

#         # Right-aligned layout
#         right_layout = QVBoxLayout()
#         right_layout.setAlignment(Qt.AlignRight)
#         date = QLabel(f"Date: {QDate.currentDate().toString('yyyy-MM-dd')}")
#         self.clock = QLabel(f"Time(IST): {QDateTime.currentDateTime().toString('hh:mm:ss')}")
#         date.setStyleSheet("font-size: 14px; padding: 5px; font-weight: bold;")
#         self.clock.setStyleSheet("font-size: 14px; padding: 5px; font-weight: bold;")
#         right_layout.addWidget(date)
#         right_layout.addWidget(self.clock)

#         # Add left, center, and right layouts to the top bar layout
#         top_bar_layout.addLayout(left_layout)
#         top_bar_layout.addStretch()
#         top_bar_layout.addLayout(center_layout)
#         top_bar_layout.addStretch()
#         top_bar_layout.addLayout(right_layout)

#         main_layout.addWidget(top_bar)

#         # Create main layout with left menu and central area
#         main_content = QHBoxLayout()
#         main_layout.addLayout(main_content)

#         # Create left menu
#         self.left_menu = QFrame(self)
#         self.left_menu.setObjectName("left_menu")
#         self.left_menu.setStyleSheet("background-color: #1E3D58; color: white;")
#         self.left_menu.setFixedWidth(200)
#         self.left_menu_layout = QVBoxLayout(self.left_menu)
#         self.left_menu_layout.setAlignment(Qt.AlignTop)

#         main_content.addWidget(self.left_menu)

#         # Create central area with scroll area for grid
#         central_area = QWidget(self)
#         central_layout = QVBoxLayout(central_area)

#         self.scroll_area = QScrollArea(self)
#         self.scroll_area.setWidgetResizable(True)
#         self.grid_widget = QWidget(self)
#         self.grid_layout = QGridLayout(self.grid_widget)
#         self.scroll_area.setWidget(self.grid_widget)
#         central_layout.addWidget(self.scroll_area)

#         # Create a horizontal layout for buttons
#         button_layout = QHBoxLayout()
#         central_layout.addLayout(button_layout)

#         self.settings_button = QPushButton("Settings", self)
#         self.settings_button.clicked.connect(self.open_settings_dialog)
#         button_layout.addWidget(self.settings_button)

#         self.start_button = QPushButton("Start", self)
#         self.start_button.clicked.connect(self.open_test_info_dialog)
#         button_layout.addWidget(self.start_button)

#         self.stop_button = QPushButton("Stop", self)
#         self.stop_button.clicked.connect(self.stop_recording)
#         button_layout.addWidget(self.stop_button)

#         self.report_button = QPushButton("Report", self)
#         self.report_button.clicked.connect(generate_pdf_report)
#         button_layout.addWidget(self.report_button)

#         self.labels = []  # To store QLabel references
#         self.serial_numbers = []
#         main_content.addWidget(central_area)

#         # Create bottom bar
#         bottom_bar = QFrame(self)
#         bottom_bar.setObjectName("bottom_bar")
#         bottom_bar.setStyleSheet("background-color: #1E3D58; color: white;")
#         bottom_bar.setFixedHeight(60)
#         bottom_bar_layout = QHBoxLayout(bottom_bar)
#         bottom_bar_layout.setAlignment(Qt.AlignLeft)
#         bottom_bar_label = QLabel("Device Status: Connected/Disconnected/Ready", self)
#         bottom_bar_label.setStyleSheet("font-size: 14px; margin-left: 20px;")
#         bottom_bar_layout.addWidget(bottom_bar_label)
#         self.bottom_bar_data_points = QLabel("Data points logged: 0", self)
#         self.bottom_bar_data_points.setStyleSheet("font-size: 14px; margin-left: 20px;")
#         bottom_bar_layout.addWidget(self.bottom_bar_data_points)
        
#         # Timer Label
#         self.timer_label = QLabel("Next data log in: 15:00")
#         self.timer_label.setStyleSheet("font-size: 14px; margin-left: 20px;")
#         bottom_bar_layout.addWidget(self.timer_label)
#          # Initialize Timer
#         self.time_remaining = QTime(0, 2, 0)
#         self.update_timer_label()

#         # Timer Label
#         # self.timer_label = QLabel("Next data log in: 15:00")
#         # bottom_bar_layout.addWidget(self.timer_label)

#         main_layout.addWidget(bottom_bar)

#         self.load_banks()
#         self.add_additional_buttons()

#         # Timer for real-time clock
#         self.clock_timer = QTimer(self)
#         self.clock_timer.timeout.connect(self.update_clock)
#         self.clock_timer.start(1000)  # Update every second

#         #timer for 15-min remaing timer 
#         self.min_15_remaing_timer = QTimer(self)
#         self.min_15_remaing_timer.timeout.connect(self.update_timer)
        
#     #IST clock
#     def update_clock(self):
#         self.clock.setText(f"Time(IST): {QDateTime.currentDateTime().toString('hh:mm:ss')}")

#     def load_banks(self):
#         banks = get_bank()
#         # Add a label for the new section
#         section_label = QLabel("Avaliable Banks", self)
#         section_label.setStyleSheet("font-size: 14px; font-weight: bold; margin-top: 20px; color: white;")
#         self.left_menu_layout.addWidget(section_label)

#         for bank in banks:
#             button = QPushButton(bank[1], self)
#             with open("./styles/button.qss","r") as file:
#                 button.setStyleSheet(file.read())
#             button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
#             button.setFixedHeight(40)
#             button.clicked.connect(lambda _, bank_id=bank[0], btn=button: self.on_menu_button_click(bank_id, btn))
#             self.left_menu_layout.addWidget(button)

#     def on_menu_button_click(self, bank_id, button):
#         self.current_bank_id = bank_id
#         if self.prev_button:
#             with open("./styles/button.qss","r") as file:
#                 self.prev_button.setStyleSheet(file.read())
        
#         button.setStyleSheet("background-color: #50B498; color: black; border: none; font-size: 16px; padding: 5px;")
#         self.prev_button = button
#         self.display_batteries(bank_id)
    
#     def display_batteries(self, bank_id):
#         for i in reversed(range(self.grid_layout.count())):
#             widget_to_remove = self.grid_layout.itemAt(i).widget()
#             self.grid_layout.removeWidget(widget_to_remove)
#             widget_to_remove.setParent(None)

#         if bank_id:
#             number_of_cells = get_no_cells(bank_id)
#             self.labels = []
#             self.serial_numbers = fetch_serial_numbers(bank_id)

#             # Add QLabel for total voltage and current at the top
#             self.total_voltage_label = QLabel('Total Voltage: 0 V\t\tTotal Current: 0 A')
#             self.grid_layout.addWidget(self.total_voltage_label, 0, 0, 1, 4)
#             self.total_voltage_label.setStyleSheet("background-color: #50B498; color: #000; border: 0.5px solid black; border-radius: 5px; padding: 10px;")

#             for i in range(number_of_cells):
#                 label = QLabel(f'Battery {i+1}')
#                 self.grid_layout.addWidget(label, (i // 4) + 1, i % 4)  # Adjust the row and column index
#                 self.labels.append(label)

#             self.update_data()

#     def update_data(self):
#         if(self.current_bank_id):
#             latest_row = read_latest_data('../data/battery_data.csv')
#             if latest_row:
#                 total_voltage = 0
#                 total_current = 0

#                 for i, label in enumerate(self.labels):
#                     voltage = float(latest_row.get(f"Bank1.B{i+1}", 0))  # Default to 0 if key not found
#                     total_voltage += voltage
#                     temp = float(latest_row.get(f"Temperature", 0))
#                     current = float(latest_row.get(f"Current", 0))  # Assuming current data is available in CSV
#                     # total_current += current

#                     color = "#4E9F3D" if voltage > 6.5 else "#ED2B2A"
#                     serial_number = self.serial_numbers[i]
#                     text = f'{serial_number}'
#                     text += f"\nVoltage: {voltage} V"
#                     text += f'\nTemp.: {temp} C'
#                     # if serial_number:
#                     #     text += f'\nSerial: {serial_number}'
#                     label.setStyleSheet(f"background-color: {color}; color: white; border: 0.5px solid black; border-radius: 5px; padding: 10px;")
#                     label.setText(text)

#                 # Update total voltage and current
#                 self.total_voltage_label.setText(f'Total Voltage: {total_voltage} V\t\tTotal Current: {current} A')

#     def open_settings_dialog(self):
#         if self.current_bank_id is None:
#             return
#         number_of_cells = len(self.labels)  # Get the number of cells based on the labels
#         dialog = SettingsDialog(self, self.serial_numbers, number_of_cells)
#         dialog.save_data.connect(self.save_serial_numbers)
#         if dialog.exec_():
#             self.serial_numbers = dialog.get_serial_numbers()
#             self.update_data()
    
#     def save_serial_numbers(self, serial_numbers):
#         conn = get_connection()
#         cur = conn.cursor()
#         # Update the serial numbers in the batteries table based on the current_bank_id
#         for i, serial_number in enumerate(serial_numbers):
#             battery_id = i + 1  
#             cur.execute("""
#                 UPDATE batteries
#                 SET serial_number = %s
#                 WHERE battery_number = %s AND bank_id = %s
#             """, (serial_number, battery_id, self.current_bank_id))
        
#         conn.commit()
#         cur.close()
#         conn.close()

#     def open_test_info_dialog(self):
#         if (not self.is_recording):
#             if(self.current_bank_id):
#                 dialog = TestInfoDialog(self)
#                 if dialog.exec_():
#                     self.test_details = dialog.get_test_details()
#                     # self.start_recording()

#     def start_test_recording(self, test_run_id, test_duration):
#         print("Recording started")
#         if not self.is_recording:
#             self.is_recording = True
#             self.update_recording_status()
#             self.min_15_remaing_timer.start(1000)
#         # Set the remaining time to the test duration
#         self.remaining_time = test_duration * 60 * 60 # Convert minutes to seconds
        
#         # Create a QTimer for updating the counter
#         self.counter_timer = QTimer(self)
#         self.counter_timer.timeout.connect(self.update_counter)
#         self.counter_timer.start(1000)  # Update every second

#         self.test_run_id = test_run_id
#         self.test_end_time = datetime.now() + timedelta(minutes=test_duration*60)
#         self.record_data()  # Record initial data

#         # Set up a QTimer to record data every 15 minutes
#         self.timer = QTimer(self)
#         self.timer.timeout.connect(self.record_data)
#         self.timer.start(2 * 60 * 1000)  # 15 minutes in milliseconds

#     #Counter for reaming timimg
#     def update_counter(self):
#         if self.remaining_time > 0:
#             self.remaining_time -= 1
#             time_str = str(QTime(0, 0).addSecs(int(self.remaining_time)).toString("hh:mm:ss"))
#             self.counter_label.setText(f"Remaining Time: {time_str}")
#         else:
#             self.counter_timer.stop()

#     #function to update the test_run db
#     def update_test_run(self, status):
#         end_time = datetime.now()
#         if 'start_time' not in self.test_details:
#             self.test_details['start_time'] = get_test_run_start_time(self.test_run_id)
#         duration_tested = end_time - self.test_details['start_time']
        
#         conn = get_connection()
#         cur = conn.cursor()
#         cur.execute("""
#             UPDATE test_runs
#             SET end_time = %s, status = %s, duration_tested = %s
#             WHERE id = %s
#         """, (end_time, status, duration_tested, self.test_run_id))
        
#         conn.commit()
#         cur.close()
#         conn.close()
  
#     def record_data(self):
#         # Check if the test duration has passed
#         if datetime.now() >= self.test_end_time:
#             self.timer.stop()
#             self.update_test_run('completed')
#             if self.is_recording:
#                 self.is_recording = False
#                 self.update_recording_status()
#             print("Test recording completed")
#             self.min_15_remaing_timer.stop()
#             return

#         latest_row = read_latest_data('../data/battery_data.csv')
#         if self.current_bank_id:
#             if latest_row:
#                 for i, label in enumerate(self.labels):
#                     conn = get_connection()
#                     cur = conn.cursor()
#                     table_name = f"recorded_data_{self.current_bank_id}"
#                     cur.execute(f"""
#                         INSERT INTO {table_name} (test_run_id, battery_number, voltage, current, temperature)
#                         VALUES (%s, %s, %s, %s, %s) RETURNING id
#                     """, (self.test_run_id, i + 1, latest_row.get(f"Bank1.B{i + 1}"), latest_row.get("Current", 0), latest_row.get("Temperature", 0)))
#                     conn.commit()
#                     cur.close()
#                     conn.close()
#                 self.data_log_counter +=1
#                 self.update_data_log_count(self.data_log_counter)
#                 print("Data recorded at", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))  

#     #TODO: counter and recoding lable stoped but recoding is still goin no no added logic to stop actual recoding 
#     def stop_recording(self):
#         if self.is_recording:
#             if self.recording_timer:
#                 self.recording_timer.stop()
#             if self.counter_timer:
#                 self.counter_timer.stop()
#             if self.min_15_remaing_timer:
#                 self.min_15_remaing_timer.stop()
#             if self.is_recording:
#                 self.is_recording = False
#                 self.update_recording_status()
            
#         # Fetch the start time from the database if not present in test_details
#             if 'start_time' not in self.test_details:
#                 self.test_details['start_time'] = get_test_run_start_time(self.test_run_id)
        
#             # Update the test run status
#             self.update_test_run('pending')

#     #method for recoding lable logic 
#     def update_recording_status(self):
#         if self.is_recording:
#             self.recording_status_label.setText("Recording...")
#             self.recording_status_label.setStyleSheet("color: green; font-weight: bold;")
#         else:
#             self.recording_status_label.setText("Not Recording")
#             self.recording_status_label.setStyleSheet("color: red; font-weight: bold;")

#     #Method for updating the counter of data logging
#     def update_data_log_count(self, count):
#         self.bottom_bar_data_points.setText(f"Data points logged: {count}")

#     def add_additional_buttons(self):
#         # Add a label for the new section
#         section_label = QLabel("Menu", self)
#         section_label.setStyleSheet("font-size: 14px; font-weight: bold; margin-top: 20px; color: white;")
#         self.left_menu_layout.addWidget(section_label)        
#         # Add the additional buttons
#         # options = ["Graph", "Reports", "Test History", "About"]
#         options = ["Graph", "Reports",  "About"]
#         for option in options:
#             button = QPushButton(option, self)
#             with open("./styles/button.qss","r") as file:
#                 button.setStyleSheet(file.read())
#             button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
#             button.setFixedHeight(40)
#             # Connect buttons to appropriate slots or methods
#             if option == "Graph":
#                 button.clicked.connect(self.show_graph)
#             elif option == "Reports":
#                 button.clicked.connect(self.show_reports)
#             # elif option == "Test History":
#             #     button.clicked.connect(self.show_test_history)
#             elif option == "About":
#                 button.clicked.connect(self.show_about)
#             self.left_menu_layout.addWidget(button)

#     def update_timer(self):
#         self.time_remaining = self.time_remaining.addSecs(-1)
#         self.update_timer_label()
        
#         if self.time_remaining == QTime(0, 0, 0):
#             self.reset_timer()

#     #function for 15 mins timer
#     def update_timer_label(self):
#         self.timer_label.setText(f"Next data log in: {self.time_remaining.toString('mm:ss')}")
    
#     def reset_timer(self):
#         self.time_remaining = QTime(0, 2, 0)

#     def show_graph(self):
#         pass  # Add logic to show graph

#     def show_reports(self):
#         pass  # Add logic to show reports

#     # def show_test_history(self):
#     #     pass  # Add logic to show test history

#     def show_about(self):
#         pass  # Add logic to show about

#     def apply_styles(self):
#         with open("./styles/styles.qss", 'r') as file:
#             self.setStyleSheet(file.read())


##############################################################################################################################################
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QGridLayout, QWidget, QLabel, QHBoxLayout, QPushButton, QFrame, QSizePolicy, QScrollArea
from PyQt5.QtCore import QTimer, Qt, QDateTime, QDate, QTime

from settings import SettingsDialog
from test_info import TestInfoDialog
from datetime import datetime, timedelta
from report import generate_pdf_report
from db_code.db_client import get_connection
from utils.db_utils import fetch_serial_numbers, get_test_run_start_time, get_no_cells, get_bank
from utils.csv_utils import read_latest_data


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
        if bank_id not in self.bank_tests:
            self.bank_tests[bank_id] = {
                'labels': [],
                'serial_numbers': [],
                'is_recording': False,
                'timer': None,
                'recording_timer': None,
                'remaining_time': 0,
                'counter_timer': None,
                'data_log_counter': 0,
                'recording_status_label': QLabel("Not Recording...", self),  # Independent recording status
                'counter_label': QLabel(self)  # Independent counter label
            }

        self.current_bank_id = bank_id  # Set the current_bank_id here

        if 'prev_button' in self.bank_tests:
            with open("./styles/button.qss", "r") as file:
                self.bank_tests['prev_button'].setStyleSheet(file.read())

        button.setStyleSheet("background-color: #50B498; color: black; border: none; font-size: 16px; padding: 5px;")
        self.bank_tests['prev_button'] = button
        self.display_batteries(bank_id)
        self.update_ui_for_selected_bank(bank_id)  # Update the UI when switching banks
        self.update_data(bank_id)

    def update_ui_for_selected_bank(self, bank_id):
        bank_test = self.bank_tests[bank_id]

        # Update recording status label
        self.recording_status_label.setText(bank_test['recording_status_label'].text())
        self.recording_status_label.setStyleSheet(bank_test['recording_status_label'].styleSheet())

        # Update counter label
        self.counter_label.setText(bank_test['counter_label'].text())
        self.counter_label.setStyleSheet(bank_test['counter_label'].styleSheet())


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
                text += f"\nVoltage: {voltage} V"
                text += f'\nTemp.: {temp} C'
                label.setStyleSheet(f"background-color: {color}; color: white; border: 0.5px solid black; border-radius: 5px; padding: 10px;")
                label.setText(text)

            # Update total voltage and current for the specific bank
            bank_test['total_voltage_label'].setText(f'Total Voltage: {total_voltage} V\t\tTotal Current: {current} A')

        # If this is the currently selected bank, update the displayed data
        if bank_id == self.current_bank_id:
            self.update_ui_for_selected_bank(bank_id)


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

    def start_test_recording(self, bank_id, test_run_id, test_duration):
        bank_test = self.bank_tests[bank_id]
        if not bank_test['is_recording']:
            bank_test['is_recording'] = True
            bank_test['remaining_time'] = test_duration * 60 * 60  # Convert minutes to seconds
            bank_test['test_run_id'] = test_run_id
            bank_test['test_end_time'] = datetime.now() + timedelta(minutes=test_duration * 60)

            # Update the UI for the selected bank
            self.update_recording_status(bank_id)
            self.update_counter(bank_id)
            self.record_data(bank_id)

            bank_test['counter_timer'] = QTimer(self)
            bank_test['counter_timer'].timeout.connect(lambda: self.update_counter(bank_id))
            bank_test['counter_timer'].start(1000)  # Update every second

            # Timer for recording data every 15 minutes
            bank_test['timer'] = QTimer(self)
            bank_test['timer'].timeout.connect(lambda: self.record_data(bank_id))
            bank_test['timer'].start(2 * 60 * 1000)  # 15 minutes in milliseconds


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

        if datetime.now() >= bank_test['test_end_time']:
            bank_test['timer'].stop()
            bank_test['is_recording'] = False
            self.update_test_run(bank_id, 'completed')
            return

        latest_row = read_latest_data('../data/battery_data.csv')
        if bank_id:
            if latest_row:
                for i, label in enumerate(bank_test['labels']):
                    conn = get_connection()
                    cur = conn.cursor()
                    table_name = f"recorded_data_{bank_id}"
                    cur.execute(f"""
                        INSERT INTO {table_name} (test_run_id, battery_number, voltage, current, temperature)
                        VALUES (%s, %s, %s, %s, %s) RETURNING id
                    """, (bank_test['test_run_id'], i + 1, latest_row.get(f"Bank1.B{i + 1}"), latest_row.get("Current", 0), latest_row.get("Temperature", 0)))
                    conn.commit()
                    cur.close()
                    conn.close()
                bank_test['data_log_counter'] += 1
                self.update_data_log_count(bank_id, bank_test['data_log_counter'])

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

    def add_additional_buttons(self):
        # Add a label for the new section
        section_label = QLabel("Menu", self)
        section_label.setStyleSheet("font-size: 14px; font-weight: bold; margin-top: 20px; color: white;")
        self.left_menu_layout.addWidget(section_label)
        # Add the additional buttons
        options = ["Graph", "Reports", "About"]
        for option in options:
            button = QPushButton(option, self)
            with open("./styles/button.qss", "r") as file:
                button.setStyleSheet(file.read())
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            button.setFixedHeight(40)
            if option == "Graph":
                button.clicked.connect(self.show_graph)
            elif option == "Reports":
                button.clicked.connect(self.show_reports)
            elif option == "About":
                button.clicked.connect(self.show_about)
            self.left_menu_layout.addWidget(button)

    def update_timer(self, bank_id):
        bank_test = self.bank_tests[bank_id]
        bank_test['time_remaining'] = bank_test['time_remaining'].addSecs(-1)
        self.update_timer_label(bank_id)

        if bank_test['time_remaining'] == QTime(0, 0, 0):
            self.reset_timer(bank_id)

    def update_timer_label(self, bank_id):
        bank_test = self.bank_tests[bank_id]
        self.timer_label.setText(f"Next data log in: {bank_test['time_remaining'].toString('mm:ss')}")

    def reset_timer(self, bank_id):
        bank_test = self.bank_tests[bank_id]
        bank_test['time_remaining'] = QTime(0, 15, 0)

    def show_graph(self):
        pass  # Add logic to show graph

    def show_reports(self):
        pass  # Add logic to show reports

    def show_about(self):
        pass  # Add logic to show about

    def apply_styles(self):
        with open("./styles/styles.qss", 'r') as file:
            self.setStyleSheet(file.read())
