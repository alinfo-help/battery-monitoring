import psycopg2
from db_code.db_config import read_config

def get_connection():
    db_config = read_config()
    return psycopg2.connect(
        dbname=db_config['dbname'], 
        user=db_config['user'], 
        password=db_config['password'], 
        host=db_config['host'], 
        port=db_config['port']
    )

if(get_connection()):
    print("connected")
