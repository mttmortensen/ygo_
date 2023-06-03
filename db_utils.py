import mysql.connector
from ac_api_call import ygo_ac_call  # Import the function

def create_connection():
    try:
        connection = mysql.connector.connect(user='mattm',  # Replace with your MySQL username
                                             password='my$QL03!',  # Replace with your MySQL password
                                             host='localhost',
                                             database='ygo_cards')  # Replace with your database name

        if connection.is_connected():
            print('Connected to MySQL database')
        return connection

    except mysql.connector.Error as error:
        print(f"Failed to connect to MySQL: {error}")

def check_table_exists(connection, table_name):
    cursor = connection.cursor()
    cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
    result = cursor.fetchone()
    if result:
        print(f"Table {table_name} exists.")
        return True
    else:
        print(f"Table {table_name} does not exist.")
        return False

def count_rows_in_table(connection, table_name):
    cursor = connection.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    result = cursor.fetchone()
    if result[0]:
        print(f"Table {table_name} already contains {result[0]} rows.")
        return result[0]
    else:
        print(f"Table {table_name} is empty.")
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