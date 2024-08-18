import sys
from PyQt5.QtWidgets import QApplication
from db_code.create_db import create_database
from ui import BatteryMonitoringSystem
from db_code.create_table import create_tables, create_recording_table
from db_code.insert_data import insert_banks_from_csv, insert_batteries_for_all_banks
from utils.db_utils import check_if_tables_exist, check_if_data_exists


def main():
    # Create the database if it doesn't exist
    # create_database()

    app = QApplication(sys.argv)
    print("not working.......")
    
    print("Checking if tables need to be created...")
    if not check_if_tables_exist():
        print("Creating required tables...")
        create_tables()
        create_recording_table()
    
    print("Checking if data needs to be inserted...")
    if not check_if_data_exists():
        print("Inserting data from CSV...")
        insert_banks_from_csv()
        insert_batteries_for_all_banks()
    
    window = BatteryMonitoringSystem()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
