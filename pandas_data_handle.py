import pandas as pd

def convert_to_dataframe(rows, columns):
    # Convert the data to a pandas DataFrame
    df = pd.DataFrame(rows, columns=columns)
    return df

# Filling in missing values with 'Not Applicable'
def fill_missing_values(df, fill_value='Not Applicable'):
    # Fill missing values
    df.fillna(value=fill_value, inplace=True)
    print("Empty Values have been filled.")
    return df

def format_numeric_columns(df, numeric_columns):
    for column in numeric_columns:
        df[column] = df[column].apply(lambda x: f"{int(x):04d}" if pd.notnull(pd.to_numeric(x, errors='coerce')) else x)
    return df

def flatten_deck_data(deck_dict, all_card_data):
    print("Starting to format deck data...")
    flattened_data = []
    for deck_part, card_list in deck_dict.items():
        for card in card_list:
            card_quantity, card_name = card
            card_details = all_card_data[all_card_data['name'] == card_name]
            if not card_details.empty:
                card_details = card_details.to_dict('records')[0]
                card_details['deck_part'] = deck_part
                card_details['quantity'] = card_quantity
                flattened_data.append(card_details)
    print("Finished formatting deck data.")
    return pd.DataFrame(flattened_data)