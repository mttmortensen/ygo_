import pandas as pd

def convert_to_dataframe(rows, columns):
    # Convert the data to a pandas DataFrame
    df = pd.DataFrame(rows, columns=columns)
    return df
