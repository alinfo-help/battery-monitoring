import configparser

def read_config(file_path="F:\\Alinfo\\BMS\\BMS_App\\app\\config\\config.txt"):
    config = configparser.ConfigParser()
    config.read(file_path)
    db_config = {
        'dbname': config.get('DEFAULT', 'dbname'),
        'user': config.get('DEFAULT', 'user'),
        'password': config.get('DEFAULT', 'password'),
        'host': config.get('DEFAULT', 'host'),
        'port': config.get('DEFAULT', 'port'),
        'csv_file_path': config.get('DEFAULT', 'csv_file_path')
    }
    return db_config