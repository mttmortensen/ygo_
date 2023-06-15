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