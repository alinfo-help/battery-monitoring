from db_code.db_client import get_connection
import pandas as pd

def load_data_from_db(self):
        """Load data from the database based on the selected bank and store it in a DataFrame."""
        bank_id = self.bank_dropdown.currentData()
        if not bank_id or not self.connection:
            return None

        query = """
            SELECT rd.*
            FROM readings rd
            JOIN test_runs tr ON rd.test_run_id = tr.id
            JOIN tests t ON tr.test_id = t.id
            WHERE t.bank_id = %s;
        """
        try:
            df = pd.read_sql_query(query, self.connection, params=(bank_id,))
            df = self.expand_array_columns(df)
            return df
        except Exception as e:
            print(f"Error loading data from database: {e}")
            return None
