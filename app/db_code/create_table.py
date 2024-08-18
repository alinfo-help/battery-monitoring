from db_code.db_client import get_connection
from db_code.db_config import read_config
import csv

def create_tables() :
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS banks (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL UNIQUE,
            number_of_cells INTEGER NOT NULL,
            description TEXT,
            voltage DECIMAL(10, 2) NOT NULL
        );

        CREATE TABLE IF NOT EXISTS batteries (
            id SERIAL PRIMARY KEY,
            bank_id INTEGER NOT NULL REFERENCES banks(id),
            battery_number INTEGER NOT NULL,
            serial_number VARCHAR(255),
            UNIQUE(bank_id, battery_number)
        );

        CREATE TABLE IF NOT EXISTS tests (
            id SERIAL PRIMARY KEY,
            bank_id INTEGER REFERENCES banks(id),
            incoming_coach VARCHAR(255),
            test_name VARCHAR(255) NOT NULL,
            logical_test_name VARCHAR(255),
            lug_date DATE,
            test_duration FLOAT,  
            process_type VARCHAR(50) NOT NULL,  
            bench_no VARCHAR(50),  
            comport VARCHAR(50),  
            test_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS test_runs (
            id SERIAL PRIMARY KEY,
            test_id INTEGER NOT NULL REFERENCES tests(id),
            run_num INTEGER NOT NULL,
            start_time TIMESTAMP,
            end_time TIMESTAMP,
            status VARCHAR(50) CHECK (status IN ('completed', 'pending')),
            duration_tested INTERVAL,
            UNIQUE(test_id, run_num)
        );

    """)
    conn.commit()
    cur.close()
    conn.close()
        # CREATE TABLE IF NOT EXISTS recorded_data (
        #     id SERIAL PRIMARY KEY,
        #     test_run_id INTEGER NOT NULL REFERENCES test_runs(id),
        #     battery_id INTEGER NOT NULL REFERENCES batteries(id),
        #     voltage DECIMAL(10, 2) NOT NULL,
        #     current DECIMAL(10, 2) NOT NULL,
        #     temperature DECIMAL(10, 2) NOT NULL,
        #     timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        # );

def create_recording_table() :
    db_config = read_config()
    csv_file_path = db_config['csv_file_path']
    with open(csv_file_path, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        i=1
        for row in csvreader:
            name = row['name']
            create_recorded_data_table(f"{i}")
            i+=1

def create_recorded_data_table(bank_name):
    conn = get_connection()
    cur = conn.cursor()
    table_name = f"recorded_data_{bank_name.lower().replace(' ', '_')}"
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id SERIAL PRIMARY KEY,
            test_run_id INTEGER NOT NULL REFERENCES test_runs(id),
            voltage DECIMAL(10, 2)[] NOT NULL,
            total_voltage DECIMAL(10, 2) NOT NULL,
            current DECIMAL(10, 2) NOT NULL,
            temperature DECIMAL(10, 2)[] NOT NULL,
            avg_temperature DECIMAL(10, 2) NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    cur.close()
    conn.close()


# Call the function to create the tables
# create_tables()
# create_recording_table()
