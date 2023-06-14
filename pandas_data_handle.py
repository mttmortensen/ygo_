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
