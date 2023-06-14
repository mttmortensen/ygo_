import mysql.connector
from config import get_db_config  # Import the function

def create_connection():
    config = get_db_config()
    database_exists = check_database_exists(config['database'])
    if not database_exists:
        print(f"Database {config['database']} does not exist.")
        return None

    try:
        connection = mysql.connector.connect(user=config['user'],  
                                             password=config['password'],
                                             host=config['host'],
                                             database=config['database'])

        if connection.is_connected():
            print('Connected to MySQL database')
        return connection

    except mysql.connector.Error as error:
        print(f"Failed to connect to MySQL: {error}")


def check_database_exists(database_name):
    config = get_db_config()
    try:
        connection = mysql.connector.connect(user=config['user'],  
                                             password=config['password'],
                                             host=config['host'])

        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(f"SHOW DATABASES LIKE '{database_name}'")
            result = cursor.fetchone()
            connection.close()  # Close the connection
            return bool(result)  # If the result is not None, the database exists
    except mysql.connector.Error as error:
        print(f"Failed to connect to MySQL: {error}")
        return False


def check_table_exists(connection, table_name):
    cursor = connection.cursor()
    cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
    result = cursor.fetchone()
    if result:
        print(f"Table {table_name} exists.")
        return connection
    else:
        print(f"Table {table_name} does not exist. Creating it now.")
        create_table_query = f"""CREATE TABLE {table_name} (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                name VARCHAR(255),
                                race VARCHAR(255),
                                level VARCHAR(255),
                                scale VARCHAR(255),
                                linkmarkers TEXT,
                                linkval VARCHAR(255),
                                atk INT,
                                def INT,
                                archetype VARCHAR(255),
                                attribute VARCHAR(255),
                                frameType VARCHAR (255),
                                type VARCHAR(255),
                                description TEXT
                            )"""
        cursor.execute(create_table_query)
        print(f"Table {table_name} created.")
        return connection


def count_rows_in_table(connection, table_name):
    cursor = connection.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    result = cursor.fetchone()
    if result[0]:
        print(f"Table {table_name} already contains {result[0]} rows.")
        return result[0]
    else:
        print(f"Table {table_name} is empty. Insert Data...")
        return 0


def insert_data(connection, data):
    cursor = connection.cursor()
    for item in data:
        # Only keep the key-value pairs where the value is not a list
        item = {k: v for k, v in item.items() if not isinstance(v, list)}
        keys = ', '.join(item.keys())
        values = ', '.join(['%s' for _ in item.values()])
        query = f"INSERT INTO all_cards ({keys}) VALUES ({values})"
        cursor.execute(query, list(item.values()))
    connection.commit()
    print("Data inserted successfully")