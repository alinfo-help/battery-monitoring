import os
import csv

def read_latest_data(csv_file_path):
        if not os.path.isfile(csv_file_path):
            return None
        with open(csv_file_path, 'r') as csvfile:
            csvreader = csv.DictReader(csvfile)
            latest_row = None
            for row in csvreader:
                latest_row = row  
            return latest_row