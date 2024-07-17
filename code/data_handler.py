import csv

def read_latest_data(file_path):
    try:
        with open(file_path, mode='r') as file:
            csv_reader = csv.DictReader(file)
            rows = list(csv_reader)
            if rows:
                return rows[-1]
    except Exception as e:
        print(f"Error reading CSV file: {e}")
    return None
