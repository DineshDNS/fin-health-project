import pandas as pd

def extract_xlsx_columns(file):
    df = pd.read_excel(file, nrows=0)
    return list(df.columns)
