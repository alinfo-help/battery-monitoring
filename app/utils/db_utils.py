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

