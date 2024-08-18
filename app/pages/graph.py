from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QHBoxLayout, QGroupBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd
import datetime
from utils.db_utils import get_bank_with_no_cell  
from db_code.db_client import get_connection

class GraphPage(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the main vertical layout
        main_layout = QVBoxLayout(self)

        # Create a group box to contain the dropdowns and the graph
        group_box = QGroupBox("Battery Monitoring Graph")
        group_box.setStyleSheet("color: black;")

        # Create a vertical layout for the group box
        group_box_layout = QVBoxLayout(group_box)

        # Create a horizontal layout for the dropdowns
        dropdown_layout = QHBoxLayout()

        # Create a dropdown for selecting the bank
        self.bank_dropdown = QComboBox(self)
        self.bank_data = self.get_available_banks()
        for bank_id, bank_info in self.bank_data.items():
            bank_name = bank_info['name']
            self.bank_dropdown.addItem(bank_name, bank_id)
        self.bank_dropdown.currentIndexChanged.connect(self.update_yaxis_dropdown)
        dropdown_layout.addWidget(self.bank_dropdown)

        # Create a dropdown for selecting the y-axis metric
        self.yaxis_dropdown = QComboBox(self)
        dropdown_layout.addWidget(self.yaxis_dropdown)

        # Create a dropdown for selecting the duration
        self.interval_dropdown = QComboBox(self)
        self.interval_dropdown.addItems(["15 mins", "30 mins", "45 mins", "1 hrs"])
        self.interval_dropdown.currentIndexChanged.connect(self.update_graph)
        dropdown_layout.addWidget(self.interval_dropdown)

        # Add the horizontal dropdown layout to the group box layout
        group_box_layout.addLayout(dropdown_layout)

        # Create a matplotlib figure and add it to the group box layout
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        group_box_layout.addWidget(self.canvas)

        # Add the group box to the main layout
        main_layout.addWidget(group_box)

        # Set the layout for the widget
        self.setLayout(main_layout)

        # Database connection setup
        self.connection = get_connection()  # Create a connection to the database

        # Load initial data from the database
        self.data = self.load_data_from_db()

        # Initial update of the y-axis dropdown and graph display
        self.update_yaxis_dropdown()
        self.update_graph()

    def get_available_banks(self):
        """Retrieve available banks from the database, including the number of cells."""
        banks = get_bank_with_no_cell()
        bank_dict = {bank[0]: {'name': bank[1], 'no_of_cells': bank[2]} for bank in banks}
        return bank_dict

    def load_data_from_db(self):
        """Load data from the database based on the selected bank and store it in a DataFrame."""
        bank_id = self.bank_dropdown.currentData()
        if not bank_id or not self.connection:
            return None

        query = """
            SELECT rd.*
            FROM recorded_data_%s rd
            JOIN test_runs tr ON rd.test_run_id = tr.id
            JOIN tests t ON tr.test_id = t.id
            WHERE t.bank_id = %s
            AND t.id = (
                SELECT MAX(id) 
                FROM tests 
                WHERE bank_id = %s
            );
        """
        try:
            df = pd.read_sql_query(query, self.connection, params=(bank_id,bank_id,bank_id))
            df = self.expand_array_columns(df)
            return df
        except Exception as e:
            print(f"Error loading data from database: {e}")
            return None

    def expand_array_columns(self, df):
        """Expand the voltage and temperature array columns into separate columns."""
        df = df.copy()
        voltage_columns = pd.DataFrame(df['voltage'].tolist(), index=df.index, columns=[f"B{i+1} Voltage" for i in range(len(df['voltage'][0]))])
        temperature_columns = pd.DataFrame(df['temperature'].tolist(), index=df.index, columns=[f"B{i+1} Temperature" for i in range(len(df['temperature'][0]))])
        df = df.drop(['voltage', 'temperature'], axis=1).join(voltage_columns).join(temperature_columns)
        return df

    def update_yaxis_dropdown(self):
        """Update the y-axis dropdown options based on the selected bank."""
        self.yaxis_dropdown.clear()

        bank_id = self.bank_dropdown.currentData()
        if bank_id is None:
            return

        self.data = self.load_data_from_db()
        if self.data is None or self.data.empty:
            return

        no_of_cells = len([col for col in self.data.columns if col.startswith("B") and col.endswith("Voltage")])

        # Add cell voltage options
        for i in range(1, no_of_cells + 1):
            self.yaxis_dropdown.addItem(f"B{i} Voltage")

        # Add other options
        self.yaxis_dropdown.addItem("Total Voltage")
        self.yaxis_dropdown.addItem("Current")
        self.yaxis_dropdown.addItem("Avg Temperature")

        # Ensure the first item is selected to avoid an empty selection
        self.yaxis_dropdown.setCurrentIndex(0)

        # Manually trigger the graph update after updating the dropdown
        self.update_graph()

    def update_graph(self):
        """Update the graph based on the selected bank, y-axis metric, and interval."""
        if self.data is None or self.data.empty:
            return

        y_axis = self.yaxis_dropdown.currentText()  # Get the selected metric for the y-axis
        interval = self.interval_dropdown.currentText()  # Get the selected time interval

        if not y_axis:
            return  # Prevents KeyError if y_axis is not set correctly

        if interval == "15 mins":
            minutes = 15
        elif interval == "30 mins":
            minutes = 30
        elif interval == "45 mins":
            minutes = 45
        elif interval == "1 hrs":
            minutes = 60

        # Filter data for the last 'minutes' duration
        end_time = self.data['timestamp'].max()
        start_time = end_time - pd.Timedelta(minutes=minutes)
        filtered_data = self.data[(self.data['timestamp'] >= start_time) & (self.data['timestamp'] <= end_time)]

        # Extract x and y values
        x_values = filtered_data['timestamp']
        y_values = filtered_data[y_axis]

        # Clear the previous figure
        self.figure.clear()

        # Create a new subplot
        ax = self.figure.add_subplot(111)
        ax.plot(x_values, y_values, marker='o', linestyle='-')

        # Format the x-axis to show time
        ax.xaxis_date()
        self.figure.autofmt_xdate()  # Rotate date labels

        # Set labels and title
        ax.set_xlabel("Time")
        ax.set_ylabel(y_axis)  # Y-axis label is the selected metric
        bank_name = self.bank_dropdown.currentText()
        ax.set_title(f"{y_axis} Over the Last {interval} for {bank_name}")

        # Draw the canvas with the updated data
        self.canvas.draw()
