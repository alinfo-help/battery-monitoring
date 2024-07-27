import csv
from db_config import read_config
from db_client import get_connection
from psycopg2.extras import RealDictCursor

def insert_bank(name, number_of_cells, description, voltage):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO banks (name, number_of_cells, description, voltage)
        VALUES (%s, %s, %s, %s) RETURNING id
    """, (name, number_of_cells, description, voltage))
    bank_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return bank_id

def insert_banks_from_csv():
    db_config = read_config()
    csv_file_path = db_config['csv_file_path']

    with open(csv_file_path, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            name = row['name']
            number_of_cells = int(row['number_of_cells'])
            description = row['description']
            voltage = float(row['voltage'])
            insert_bank(name, number_of_cells, description, voltage)

def get_all_banks():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM banks")
    banks = cur.fetchall()
    cur.close()
    conn.close()
    return banks

def insert_battery(bank_id, battery_number, serial_number):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO batteries (bank_id, battery_number, serial_number)
        VALUES (%s, %s, %s) RETURNING id
    """, (bank_id, battery_number, serial_number))
    battery_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return battery_id

def insert_batteries_for_all_banks():
    banks = get_all_banks()
    for bank in banks:
        bank_id = bank['id']
        number_of_cells = bank['number_of_cells']
        bank_name = bank['name']
        for battery_number in range(1, number_of_cells + 1):
            serial_number = f"{bank_name}.B{battery_number}"
            insert_battery(bank_id, battery_number,serial_number)


# insert_banks_from_csv()
insert_batteries_for_all_banks()