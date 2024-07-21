from db_client import get_connection

def create_tables():
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
    """)
    conn.commit()
    cur.close()
    conn.close()