from db_code.db_client import get_connection

def fetch_serial_numbers(bank_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT serial_number
        FROM batteries
        WHERE bank_id = %s
        ORDER BY battery_number
    """, (bank_id,))
    serial_numbers = [row[0] for row in cur.fetchall()]
    cur.close()
    conn.close()
    return serial_numbers

# Method to get the start_time from the test_runs table
def get_test_run_start_time(test_run_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT start_time FROM test_runs WHERE id = %s
    """, (test_run_id,))
    start_time = cur.fetchone()[0]
    cur.close()
    conn.close()
    return start_time

def get_pending_test_info(self, bank_id):
        query = """
        SELECT t.*, tr.*
        FROM tests t
        JOIN test_runs tr ON t.id = tr.test_id
        WHERE t.bank_id = %s AND tr.status = 'pending'
        LIMIT 1;
        """
        cursor = self.conn.cursor()
        cursor.execute(query, (bank_id,))
        result = cursor.fetchone()
        cursor.close()
        return result

def get_no_cells(bank_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT number_of_cells FROM banks WHERE id = %s", (bank_id,))
    number_of_cells = cur.fetchone()[0]
    cur.close()
    conn.close()
    return number_of_cells

def get_bank():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM banks")
    banks = cur.fetchall()
    cur.close()
    conn.close()
    return banks

def get_bank_with_no_cell():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, number_of_cells FROM banks")
    banks = cur.fetchall()
    cur.close()
    conn.close()
    return banks


def check_if_tables_exist():
    # Example connection string; modify as per your database config
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name='banks');")
    banks_exists = cur.fetchone()[0]
    
    cur.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name='batteries');")
    batteries_exists = cur.fetchone()[0]
    
    cur.close()
    conn.close()
    
    return banks_exists and batteries_exists

def check_if_data_exists():
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT COUNT(*) FROM banks;")
    banks_count = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM batteries;")
    batteries_count = cur.fetchone()[0]
    
    cur.close()
    conn.close()
    
    return banks_count > 0 and batteries_count > 0
