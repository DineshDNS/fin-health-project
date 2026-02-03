import pandas as pd

def extract_csv_columns(file):
    df = pd.read_csv(file, nrows=0)
    return list(df.columns)
