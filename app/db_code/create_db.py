import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from db_code.db_config import read_config

def create_database(dbname, user, password, host='localhost', port='5432'):
    # Connect to the default database 'postgres' to execute the creation of your target database
    conn = psycopg2.connect(dbname="postgres", user=user, password=password, host=host, port=port)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)  # Required for database creation
    
    cur = conn.cursor()

    # Check if the database already exists
    cur.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{dbname}';")
    exists = cur.fetchone()

    if not exists:
        # Create the database
        cur.execute(f"CREATE DATABASE {dbname};")
        print(f"Database '{dbname}' created successfully.")
    else:
        print(f"Database '{dbname}' already exists.")
    
    cur.close()
    conn.close()

if __name__ == "__main__":
    db_config = read_config()
    create_database(dbname=db_config['dbname'], user=db_config['user'], password=db_config['password'])
