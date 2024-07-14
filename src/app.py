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
import sys
import csv
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget, QGridLayout, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtCore import QTimer, QTime, Qt
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import QMargins

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Battery Data Monitoring'
        self.left = 100
        self.top = 100
        self.width = 800
        self.height = 600
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        header_layout = QHBoxLayout()
        layout.addLayout(header_layout)

        self.clock = QLabel('', self)
        self.clock.setFont(QFont('Arial', 12, QFont.Bold))
        header_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        header_layout.addWidget(self.clock, alignment=Qt.AlignRight)

        self.grid_layout = QGridLayout()
        layout.addLayout(self.grid_layout)

        self.labels = self.create_grid()

        # Set up a timer to refresh the data every 5 seconds
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(5000)

        # Set up a timer to update the clock every second
        self.clock_timer = QTimer()
        self.clock_timer.timeout.connect(self.update_clock)
        self.clock_timer.start(1000)

    def create_grid(self):
        labels = []
        for i in range(19):
            label = QLabel(f'Battery {i+1}: N/A', self)
            label.setStyleSheet("background-color: green; color: white; border: 1px solid black; padding: 5px;")
            label.setFont(QFont('Arial', 10))
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
                        label.setText(f'Battery {i+1}: {latest_row[f"Bank1.B{i+1}"]}')
        except Exception as e:
            print(f"Error reading CSV file: {e}")

    def update_clock(self):
        current_time = QTime.currentTime().toString('hh:mm:ss')
        self.clock.setText(current_time)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())

