# import sys
# import csv
# from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget, QGridLayout
# from PyQt5.QtCore import QTimer

# class App(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.title = 'Battery Data Monitoring'
#         self.left = 100
#         self.top = 100
#         self.width = 800
#         self.height = 600
#         self.initUI()

#     def initUI(self):
#         self.setWindowTitle(self.title)
#         self.setGeometry(self.left, self.top, self.width, self.height)

#         central_widget = QWidget(self)
#         self.setCentralWidget(central_widget)
#         layout = QVBoxLayout(central_widget)

#         self.grid_layout = QGridLayout()
#         layout.addLayout(self.grid_layout)

#         self.labels = self.create_grid()

#         # Set up a timer to refresh the data every 5 seconds
#         self.timer = QTimer()
#         self.timer.timeout.connect(self.update_data)
#         self.timer.start(5000)

#     def create_grid(self):
#         labels = []
#         for i in range(19):
#             label = QLabel(f'Battery {i+1}: N/A', self)
#             self.grid_layout.addWidget(label, i // 4, i % 4)
#             labels.append(label)
#         return labels

#     def update_data(self):
#         try:
#             with open('../data/battery_data.csv', mode='r') as file:
#                 csv_reader = csv.DictReader(file)
#                 rows = list(csv_reader)
#                 if rows:
#                     latest_row = rows[-1]
#                     for i, label in enumerate(self.labels):
#                         label.setText(f'Battery {i+1}: {latest_row[f"Bank1.B{i+1}"]}')
#         except Exception as e:
#             print(f"Error reading CSV file: {e}")

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = App()
#     ex.show()
#     sys.exit(app.exec_())


###############################################################################################################################
# import sys
# import csv
# from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget, QGridLayout, QHBoxLayout
# from PyQt5.QtCore import QTimer, QTime, Qt

# class App(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.title = 'Battery Data Monitoring'
#         self.left = 100
#         self.top = 100
#         self.width = 800
#         self.height = 600
#         self.initUI()

#     def initUI(self):
#         self.setWindowTitle(self.title)
#         self.setGeometry(self.left, self.top, self.width, self.height)

#         central_widget = QWidget(self)
#         self.setCentralWidget(central_widget)
#         layout = QVBoxLayout(central_widget)

#         header_layout = QHBoxLayout()
#         layout.addLayout(header_layout)

#         self.clock = QLabel('', self)
#         header_layout.addWidget(self.clock, alignment=Qt.AlignRight)

#         self.grid_layout = QGridLayout()
#         layout.addLayout(self.grid_layout)

#         self.labels = self.create_grid()

#         # Set up a timer to refresh the data every 5 seconds
#         self.timer = QTimer()
#         self.timer.timeout.connect(self.update_data)
#         self.timer.start(5000)

#         # Set up a timer to update the clock every second
#         self.clock_timer = QTimer()
#         self.clock_timer.timeout.connect(self.update_clock)
#         self.clock_timer.start(1000)

#     def create_grid(self):
#         labels = []
#         for i in range(19):
#             label = QLabel(f'Battery {i+1}: N/A', self)
#             self.grid_layout.addWidget(label, i // 4, i % 4)
#             labels.append(label)
#         return labels

#     def update_data(self):
#         try:
#             with open('../data/battery_data.csv', mode='r') as file:
#                 csv_reader = csv.DictReader(file)
#                 rows = list(csv_reader)
#                 if rows:
#                     latest_row = rows[-1]
#                     for i, label in enumerate(self.labels):
#                         label.setText(f'Battery {i+1}: {latest_row[f"Bank1.B{i+1}"]}')
#         except Exception as e:
#             print(f"Error reading CSV file: {e}")

#     def update_clock(self):
#         current_time = QTime.currentTime().toString('hh:mm:ss')
#         self.clock.setText(current_time)

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = App()
#     ex.show()
#     sys.exit(app.exec_())

########################################################
# import sys
# import csv
# from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget, QGridLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QPushButton
# from PyQt5.QtCore import QTimer, QTime, Qt
# from PyQt5.QtGui import QFont

# class App(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.title = 'Battery Data Monitoring'
#         self.left = 100
#         self.top = 100
#         self.width = 800
#         self.height = 600
#         self.initUI()

#     def initUI(self):
#         self.setWindowTitle(self.title)
#         self.setGeometry(self.left, self.top, self.width, self.height)

#         central_widget = QWidget(self)
#         self.setCentralWidget(central_widget)
#         layout = QVBoxLayout(central_widget)

#         header_layout = QHBoxLayout()
#         layout.addLayout(header_layout)

#         self.clock = QLabel('', self)
#         self.clock.setFont(QFont('Arial', 12, QFont.Bold))
#         header_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
#         header_layout.addWidget(self.clock, alignment=Qt.AlignRight)

#         self.grid_layout = QGridLayout()
#         layout.addLayout(self.grid_layout)

#         self.labels = self.create_grid()

#         self.button_layout = QHBoxLayout()
#         layout.addLayout(self.button_layout)

#         self.settings_button = QPushButton('Settings', self)
#         self.start_button = QPushButton('Start', self)
#         self.stop_button = QPushButton('Stop', self)
#         self.report_button = QPushButton('Report', self)

#         self.button_layout.addWidget(self.settings_button)
#         self.button_layout.addWidget(self.start_button)
#         self.button_layout.addWidget(self.stop_button)
#         self.button_layout.addWidget(self.report_button)

#         # Set up a timer to refresh the data every 5 seconds
#         self.timer = QTimer()
#         self.timer.timeout.connect(self.update_data)
#         self.timer.start(5000)

#         # Set up a timer to update the clock every second
#         self.clock_timer = QTimer()
#         self.clock_timer.timeout.connect(self.update_clock)
#         self.clock_timer.start(1000)

#     def create_grid(self):
#         labels = []
#         for i in range(19):
#             label = QLabel(f'Battery {i+1}: N/A', self)
#             label.setFont(QFont('Arial', 10))
#             self.grid_layout.addWidget(label, i // 4, i % 4)
#             labels.append(label)
#         return labels

#     def update_data(self):
#         try:
#             with open('../data/battery_data.csv', mode='r') as file:
#                 csv_reader = csv.DictReader(file)
#                 rows = list(csv_reader)
#                 if rows:
#                     latest_row = rows[-1]
#                     for i, label in enumerate(self.labels):
#                         voltage = float(latest_row[f"Bank1.B{i+1}"])
#                         color = "green" if voltage > 6.5 else "red"
#                         label.setStyleSheet(f"background-color: {color}; color: white; border: 1px solid black; padding: 5px;")
#                         label.setText(f'Battery {i+1}: {voltage}')
#         except Exception as e:
#             print(f"Error reading CSV file: {e}")

#     def update_clock(self):
#         current_time = QTime.currentTime().toString('hh:mm:ss')
#         self.clock.setText(current_time)

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = App()
#     ex.show()
#     sys.exit(app.exec_())

##########################################################-------WorkingCodeWithPdf---------------###########################################
# import sys
# import csv
# import os
# from PyQt5.QtWidgets import (
#     QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget, QGridLayout, QHBoxLayout,
#     QSpacerItem, QSizePolicy, QPushButton, QDialog, QFormLayout, QLineEdit, QDialogButtonBox
# )
# from PyQt5.QtCore import QTimer, QTime, Qt
# from PyQt5.QtGui import QFont
# from fpdf import FPDF

# class SettingsDialog(QDialog):
#     def __init__(self, parent=None, serial_numbers=None):
#         super().__init__(parent)
#         self.setWindowTitle('Battery Settings')
#         self.serial_numbers = serial_numbers or [None] * 19
#         self.line_edits = [QLineEdit(self) for _ in range(19)]

#         layout = QFormLayout(self)
#         for i, line_edit in enumerate(self.line_edits, start=1):
#             line_edit.setText(self.serial_numbers[i-1] if self.serial_numbers[i-1] else "")
#             layout.addRow(f'Battery {i} Serial Number:', line_edit)

#         self.buttons = QDialogButtonBox(
#             QDialogButtonBox.Save | QDialogButtonBox.Cancel,
#             Qt.Horizontal, self
#         )
#         self.buttons.accepted.connect(self.accept)
#         self.buttons.rejected.connect(self.reject)
#         layout.addRow(self.buttons)

#     def get_serial_numbers(self):
#         return [
#             line_edit.text() if line_edit.text() else self.serial_numbers[i]
#             for i, line_edit in enumerate(self.line_edits)
#         ]

# class App(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.title = 'Battery Data Monitoring'
#         self.left = 100
#         self.top = 100
#         self.width = 800
#         self.height = 600
#         self.serial_numbers = [None] * 19
#         self.initUI()

#     def initUI(self):
#         self.setWindowTitle(self.title)
#         self.setGeometry(self.left, self.top, self.width, self.height)

#         central_widget = QWidget(self)
#         self.setCentralWidget(central_widget)
#         layout = QVBoxLayout(central_widget)

#         header_layout = QHBoxLayout()
#         layout.addLayout(header_layout)

#         self.clock = QLabel('', self)
#         self.clock.setFont(QFont('Arial', 12, QFont.Bold))
#         header_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
#         header_layout.addWidget(self.clock, alignment=Qt.AlignRight)

#         self.grid_layout = QGridLayout()
#         layout.addLayout(self.grid_layout)

#         self.labels = self.create_grid()

#         self.button_layout = QHBoxLayout()
#         layout.addLayout(self.button_layout)

#         self.settings_button = QPushButton('Settings', self)
#         self.start_button = QPushButton('Start', self)
#         self.stop_button = QPushButton('Stop', self)
#         self.report_button = QPushButton('Report', self)

#         self.button_layout.addWidget(self.settings_button)
#         self.button_layout.addWidget(self.start_button)
#         self.button_layout.addWidget(self.stop_button)
#         self.button_layout.addWidget(self.report_button)

#         self.settings_button.clicked.connect(self.open_settings_dialog)
#         self.report_button.clicked.connect(self.generate_pdf_report)

#         # Set up a timer to refresh the data every 5 seconds
#         self.timer = QTimer()
#         self.timer.timeout.connect(self.update_data)
#         self.timer.start(5000)

#         # Set up a timer to update the clock every second
#         self.clock_timer = QTimer()
#         self.clock_timer.timeout.connect(self.update_clock)
#         self.clock_timer.start(1000)

#     def create_grid(self):
#         labels = []
#         for i in range(19):
#             label = QLabel(f'Battery {i+1}: N/A', self)
#             label.setFont(QFont('Arial', 10))
#             self.grid_layout.addWidget(label, i // 4, i % 4)
#             labels.append(label)
#         return labels

#     def update_data(self):
#         try:
#             with open('../data/battery_data.csv', mode='r') as file:
#                 csv_reader = csv.DictReader(file)
#                 rows = list(csv_reader)
#                 if rows:
#                     latest_row = rows[-1]
#                     for i, label in enumerate(self.labels):
#                         voltage = float(latest_row[f"Bank1.B{i+1}"])
#                         color = "green" if voltage > 6.5 else "red"
#                         serial_number = self.serial_numbers[i]
#                         text = f'Battery {i+1}: {voltage}'
#                         if serial_number:
#                             text += f'\nSerial: {serial_number}'
#                         label.setStyleSheet(f"background-color: {color}; color: white; border: 1px solid black; padding: 5px;")
#                         label.setText(text)
#         except Exception as e:
#             print(f"Error reading CSV file: {e}")

#     def update_clock(self):
#         current_time = QTime.currentTime().toString('hh:mm:ss')
#         self.clock.setText(current_time)

#     def open_settings_dialog(self):
#         dialog = SettingsDialog(self, self.serial_numbers)
#         if dialog.exec_():
#             self.serial_numbers = dialog.get_serial_numbers()
#             self.update_data()

#     def generate_pdf_report(self):
#         pdf = FPDF()
#         pdf.add_page()
#         pdf.set_font("Arial", size=12)

#         try:
#             with open('../data/battery_data.csv', mode='r') as file:
#                 csv_reader = csv.DictReader(file)
#                 for i, row in enumerate(csv_reader):
#                     if i == 0:
#                         # Add the header row
#                         header = ', '.join(row.keys())
#                         pdf.cell(200, 10, txt=header, ln=True)
#                     # Add the data rows
#                     line = ', '.join(row.values())
#                     pdf.cell(200, 10, txt=line, ln=True)

#             # Save the PDF to a file
#             pdf_output_path = "battery_report.pdf"
#             pdf.output(pdf_output_path)
#             print(f"PDF report generated: {pdf_output_path}")

#             # Open the PDF automatically
#             if sys.platform == "win32":
#                 os.startfile(pdf_output_path)
#             else:
#                 os.system(f"open {pdf_output_path}")
#         except Exception as e:
#             print(f"Error generating PDF report: {e}")

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = App()
#     ex.show()
#     sys.exit(app.exec_())



#####################################################################################################################################
import sys
import csv
import os
from PyQt5.QtWidgets import (
    QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget, QGridLayout, QHBoxLayout,
    QSpacerItem, QSizePolicy, QPushButton, QDialog, QFormLayout, QLineEdit, QDialogButtonBox,
    QGroupBox
)
from PyQt5.QtCore import QTimer, QTime, Qt
from PyQt5.QtGui import QFont
from fpdf import FPDF

class SettingsDialog(QDialog):
    def __init__(self, parent=None, serial_numbers=None):
        super().__init__(parent)
        self.setWindowTitle('Battery Settings')
        self.serial_numbers = serial_numbers or [None] * 19
        self.line_edits = [QLineEdit(self) for _ in range(19)]

        layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        left_group_box = QGroupBox()
        right_group_box = QGroupBox()
        left_layout = QFormLayout(left_group_box)
        right_layout = QFormLayout(right_group_box)

        for i, line_edit in enumerate(self.line_edits, start=1):
            line_edit.setText(self.serial_numbers[i-1] if self.serial_numbers[i-1] else "")
            if i <= 10:
                left_layout.addRow(f'Battery {i} Serial Number:', line_edit)
            else:
                right_layout.addRow(f'Battery {i} Serial Number:', line_edit)

        layout.addWidget(left_group_box)
        layout.addWidget(right_group_box)

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Save | QDialogButtonBox.Cancel,
            Qt.Horizontal, self
        )
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)

    def get_serial_numbers(self):
        return [
            line_edit.text() if line_edit.text() else self.serial_numbers[i]
            for i, line_edit in enumerate(self.line_edits)
        ]

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Battery Data Monitoring'
        self.setGeometry(0, 0, QApplication.desktop().screenGeometry().width(), QApplication.desktop().screenGeometry().height())
        self.serial_numbers = [None] * 19
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
        self.report_button.clicked.connect(self.generate_pdf_report)

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
        try:
            with open('../data/battery_data.csv', mode='r') as file:
                csv_reader = csv.DictReader(file)
                rows = list(csv_reader)
                if rows:
                    latest_row = rows[-1]
                    for i, label in enumerate(self.labels):
                        voltage = float(latest_row[f"Bank1.B{i+1}"])
                        color = "#4E9F3D" if voltage > 6.5 else "#ED2B2A"
                        serial_number = self.serial_numbers[i]
                        text = f'Battery {i+1}: {voltage} V'
                        if serial_number:
                            text += f'\nSerial: {serial_number}'
                        label.setStyleSheet(f"background-color: {color}; color: white; border: 0.5px solid black; border-radius: 5px; padding: 35px; opacity: 0.4")
                        label.setText(text)
        except Exception as e:
            print(f"Error reading CSV file: {e}")

    def update_clock(self):
        current_time = QTime.currentTime().toString('hh:mm:ss')
        self.clock.setText(current_time)

    def open_settings_dialog(self):
        dialog = SettingsDialog(self, self.serial_numbers)
        if dialog.exec_():
            self.serial_numbers = dialog.get_serial_numbers()
            self.update_data()

    def generate_pdf_report(self):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        try:
            with open('../data/battery_data.csv', mode='r') as file:
                csv_reader = csv.DictReader(file)
                for i, row in enumerate(csv_reader):
                    if i == 0:
                        # Add the header row
                        header = ', '.join(row.keys())
                        pdf.cell(200, 10, txt=header, ln=True)
                    # Add the data rows
                    line = ', '.join(row.values())
                    pdf.cell(200, 10, txt=line, ln=True)

            # Save the PDF to a file
            pdf_output_path = "battery_report.pdf"
            pdf.output(pdf_output_path)
            print(f"PDF report generated: {pdf_output_path}")

            # Open the PDF automatically
            if sys.platform == "win32":
                os.startfile(pdf_output_path)
            else:
                os.system(f"open {pdf_output_path}")
        except Exception as e:
            print(f"Error generating PDF report: {e}")

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())

#################################################################################################################
# import sys
# import csv
# import os
# import shutil
# from PyQt5.QtWidgets import (
#     QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget, QGridLayout, QHBoxLayout,
#     QPushButton, QLineEdit, QFileDialog, QDialog, QDialogButtonBox, QGroupBox
# )
# from PyQt5.QtCore import QTimer, QTime, Qt
# from PyQt5.QtGui import QFont
# from fpdf import FPDF
# from datetime import datetime

# class SettingsDialog(QDialog):
#     def __init__(self, parent=None, serial_numbers=None):
#         super().__init__(parent)
#         self.setWindowTitle('Battery Settings')
#         self.serial_numbers = serial_numbers or [None] * 19
#         self.line_edits = [QLineEdit(self) for _ in range(19)]

#         layout = QVBoxLayout(self)
#         form_layout = QGridLayout()

#         left_group_box = QGroupBox()
#         right_group_box = QGroupBox()
#         left_layout = QVBoxLayout(left_group_box)
#         right_layout = QVBoxLayout(right_group_box)

#         for i, line_edit in enumerate(self.line_edits, start=1):
#             line_edit.setText(self.serial_numbers[i-1] if self.serial_numbers[i-1] else "")
#             if i <= 10:
#                 left_layout.addWidget(QLabel(f'Battery {i} Serial Number:'))
#                 left_layout.addWidget(line_edit)
#             else:
#                 right_layout.addWidget(QLabel(f'Battery {i} Serial Number:'))
#                 right_layout.addWidget(line_edit)

#         form_layout.addWidget(left_group_box, 0, 0)
#         form_layout.addWidget(right_group_box, 0, 1)

#         layout.addLayout(form_layout)

#         self.buttons = QDialogButtonBox(
#             QDialogButtonBox.Save | QDialogButtonBox.Cancel,
#             Qt.Horizontal, self
#         )
#         self.buttons.accepted.connect(self.accept)
#         self.buttons.rejected.connect(self.reject)
#         layout.addWidget(self.buttons)

#     def get_serial_numbers(self):
#         return [line_edit.text() if line_edit.text() else self.serial_numbers[i]
#                 for i, line_edit in enumerate(self.line_edits)]


# class App(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.title = 'Battery Data Monitoring'
#         self.setGeometry(0, 0, QApplication.desktop().screenGeometry().width(),
#                          QApplication.desktop().screenGeometry().height())
#         self.serial_numbers = [None] * 19
#         self.csv_dir = "../data/"
#         self.current_csv_path = None
#         self.initUI()

#     def initUI(self):
#         self.setWindowTitle(self.title)
#         self.showMaximized()

#         central_widget = QWidget(self)
#         self.setCentralWidget(central_widget)
#         layout = QVBoxLayout(central_widget)

#         header_layout = QHBoxLayout()
#         layout.addLayout(header_layout)

#         # Input box for CSV file path selection
#         self.csv_path_edit = QLineEdit(self)
#         self.csv_path_edit.setPlaceholderText('Select CSV file...')
#         self.csv_path_edit.setReadOnly(True)
#         select_csv_button = QPushButton('Select', self)
#         select_csv_button.clicked.connect(self.select_csv_file)

#         header_layout.addWidget(self.csv_path_edit)
#         header_layout.addWidget(select_csv_button)

#         self.clock = QLabel('', self)
#         self.clock.setFont(QFont('Arial', 12, QFont.Bold))
#         header_layout.addWidget(self.clock, alignment=Qt.AlignRight | Qt.AlignTop)

#         self.grid_layout = QGridLayout()
#         layout.addLayout(self.grid_layout)

#         self.labels = self.create_grid()

#         self.button_layout = QHBoxLayout()
#         layout.addLayout(self.button_layout)

#         self.settings_button = QPushButton('Settings', self)
#         self.start_button = QPushButton('Start', self)
#         self.stop_button = QPushButton('Stop', self)
#         self.report_button = QPushButton('Report', self)

#         self.button_layout.addWidget(self.settings_button)
#         self.button_layout.addWidget(self.start_button)
#         self.button_layout.addWidget(self.stop_button)
#         self.button_layout.addWidget(self.report_button)

#         self.settings_button.clicked.connect(self.open_settings_dialog)
#         self.report_button.clicked.connect(self.generate_pdf_report)

#         # Set up a timer to refresh the data every 5 seconds
#         self.timer = QTimer()
#         self.timer.timeout.connect(self.update_data)
#         self.timer.start(5000)

#         # Set up a timer to update the clock every second
#         self.clock_timer = QTimer()
#         self.clock_timer.timeout.connect(self.update_clock)
#         self.clock_timer.start(1000)

#         self.apply_styles()

#     def create_grid(self):
#         labels = []
#         for i in range(19):
#             label = QLabel(f'Battery {i+1}: N/A', self)
#             label.setFont(QFont('Arial', 10))
#             label.setAlignment(Qt.AlignCenter)
#             self.grid_layout.addWidget(label, i // 4, i % 4)
#             labels.append(label)
#         return labels

#     def update_data(self):
#         try:
#             # Ensure current CSV path is set
#             if not self.current_csv_path:
#                 return

#             with open(self.current_csv_path, mode='r') as file:
#                 csv_reader = csv.DictReader(file)
#                 rows = list(csv_reader)
#                 if rows:
#                     latest_row = rows[-1]
#                     for i, label in enumerate(self.labels):
#                         voltage = float(latest_row[f"Bank1.B{i+1}"])
#                         color = "green" if voltage > 6.5 else "red"
#                         serial_number = self.serial_numbers[i]
#                         text = f'Battery {i+1}: {voltage}'
#                         if serial_number:
#                             text += f'\nSerial: {serial_number}'
#                         label.setStyleSheet(
#                             f"background-color: {color}; color: white; border: 1px solid black; border-radius: 10px; padding: 5px;")
#                         label.setText(text)
#         except Exception as e:
#             print(f"Error reading CSV file: {e}")

#     def update_clock(self):
#         current_time = QTime.currentTime().toString('hh:mm:ss')
#         self.clock.setText(current_time)

#     def select_csv_file(self):
#         options = QFileDialog.Options()
#         options |= QFileDialog.DontUseNativeDialog
#         filename, _ = QFileDialog.getOpenFileName(self, "Select CSV File", "", "CSV Files (*.csv)", options=options)
#         if filename:
#             self.csv_path_edit.setText(filename)
#             self.create_hourly_copy(filename)
#             self.current_csv_path = filename
#             self.update_data()

#     def create_hourly_copy(self, src_path):
#         try:
#             current_time = datetime.now()
#             hour_str = current_time.strftime("%Y%m%d%H")
#             dst_filename = f"{self.csv_dir}/battery_data_{hour_str}.csv"
#             shutil.copy(src_path, dst_filename)
#             print(f"Hourly copy created: {dst_filename}")
#         except Exception as e:
#             print(f"Error creating hourly copy: {e}")

#     def open_settings_dialog(self):
#         dialog = SettingsDialog(self, self.serial_numbers)
#         if dialog.exec_():
#             self.serial_numbers = dialog.get_serial_numbers()
#             self.update_data()

#     def generate_pdf_report(self):
#         pdf = FPDF()
#         pdf.add_page()
#         pdf.set_font("Arial", size=12)

#         try:
#             with open(self.current_csv_path, mode='r') as file:
#                 csv_reader = csv.DictReader(file)
#                 for i, row in enumerate(csv_reader):
#                     if i == 0:
#                         # Add the header row
#                         header = ', '.join(row.keys())
#                         pdf.cell(200, 10, txt=header, ln=True)
#                     # Add the data rows
#                     line = ', '.join(row.values())
#                     pdf.cell(200, 10, txt=line, ln=True)

#             # Save the PDF to a file
#             pdf_output_path = "battery_report.pdf"
#             pdf.output(pdf_output_path)
#             print(f"PDF report generated: {pdf_output_path}")

#             # Open the PDF automatically
#             if sys.platform == "win32":
#                 os.startfile(pdf_output_path)
#             else:
#                 os.system(f"open {pdf_output_path}")
#         except Exception as e:
#             print(f"Error generating PDF report: {e}")

#     def apply_styles(self):
#         self.setStyleSheet("""
#             QMainWindow {
#                 background-color: #f5f5f5;
#             }
#             QLabel {
#                 font-family: Arial;
#                 font-size: 12pt;
#                 padding: 10px;
#                 border: 1px solid #ddd;
#                 border-radius: 5px;
#                 margin: 5px;
#                 background-color: #ffffff;
#             }
#             QPushButton {
#                 background-color: #4CAF50;
#                 color: white;
#                 border: none;
#                 padding: 10px 24px;
#                 text-align: center;
#                 text-decoration: none;
#                 display: inline-block;
#                 font-size: 14px;
#                 margin: 4px 2px;
#                 border-radius: 5px;
#             }
#             QPushButton:hover {
#                 background-color: #45a049;
#             }
#             QDialog {
#                 background-color: #ffffff;
#             }
#             QLineEdit {
#                 border: 1px solid #ddd;
#                 padding: 5px;
#                 border-radius: 5px;
#             }
#             QDialogButtonBox {
#                 background-color: #f5f5f5;
#             }
#         """)

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = App()
#     ex.show()
#     sys.exit(app.exec_())

