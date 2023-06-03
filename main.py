from ac_api_call import ygo_ac_call
from db_utils import create_connection, check_table_exists, count_rows_in_table, insert_data

# establish connection to database
connection = create_connection()

# check if the table exists
table_exists = check_table_exists(connection, 'all_cards')

# if the table exists, check if it's empty
if table_exists:
    row_count = count_rows_in_table(connection, 'all_cards')

    # if the table is empty, insert data from API
    if row_count == 0:
        data = ygo_ac_call()  # Get data from API
        insert_data(connection, data)
