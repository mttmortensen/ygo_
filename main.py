from ac_api_call import ygo_ac_call
from db_utils import create_connection, check_table_exists, count_rows_in_table, insert_data, fetch_all_card_data
from pandas_data_handle import convert_to_dataframe, fill_missing_values, format_numeric_columns  # Import the new functions
from md_scrape_call import get_deck_links, get_deck_list  # Import the new functions

# establish connection to database
connection = create_connection()

# if the connection is None, it means the database does not exist
if connection is None:
    print("Cannot establish connection to the database. Exiting the script.")
    exit(1)

# check if the table exists
connection = check_table_exists(connection, 'all_cards')

# if the connection is not None, it means the table exists or has been created.
if connection:
    row_count = count_rows_in_table(connection, 'all_cards')

    # if the table is empty, insert data from API
    if row_count == 0:
        data = ygo_ac_call()  # Get data from API
        insert_data(connection, data)

    # Fetch all card data from the database
    rows, columns = fetch_all_card_data()

    # Convert the data to a pandas DataFrame
    df = convert_to_dataframe(rows, columns)

    # Fill missing values
    df = fill_missing_values(df)

    # Format the Numeric columns
    numeric_columns = ['atk', 'def', 'level', 'linkval', 'scale']
    df = format_numeric_columns(df,numeric_columns)
    print(df.head())

    # Now df is a pandas DataFrame with no missing values, ready for the next steps

    # Scrape deck data
    print("Starting to scrape deck data...")
    deck_links = get_deck_links('https://yugiohtopdecks.com/decklists')
    deck_data = [get_deck_list('https://yugiohtopdecks.com' + link) for link in deck_links]
    print("Finished scraping deck data.")
