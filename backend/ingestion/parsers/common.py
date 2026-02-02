import os
import pandas as pd


def get_file_extension(path: str) -> str:
    return os.path.splitext(path)[1].lower()


def read_tabular_file(path: str):
    ext = get_file_extension(path)

    if ext == ".csv":
        return pd.read_csv(path)

    if ext in [".xlsx", ".xls"]:
        return pd.read_excel(path)

    raise NotImplementedError("Tabular parsing not supported")
