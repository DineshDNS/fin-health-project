import camelot
import pandas as pd


def extract_financial_table_from_pdf(path: str) -> pd.DataFrame:
    """
    Extract Profit & Loss / Financial tables from a text-based PDF.
    Expected to return DataFrame with columns:
    account | amount
    """

    tables = camelot.read_pdf(path, pages="all", flavor="stream")

    if tables.n == 0:
        raise ValueError("No tables found in Financial PDF")

    for table in tables:
        df = table.df.copy()

        # Use first row as header
        df.columns = df.iloc[0]
        df = df[1:]

        # Normalize headers
        df.columns = [str(c).strip().lower() for c in df.columns]

        # Common header variants → normalize
        rename_map = {}
        if "particulars" in df.columns:
            rename_map["particulars"] = "account"
        if "account name" in df.columns:
            rename_map["account name"] = "account"
        if "description" in df.columns:
            rename_map["description"] = "account"

        if "value" in df.columns:
            rename_map["value"] = "amount"
        if "total" in df.columns:
            rename_map["total"] = "amount"
        if "amount" in df.columns:
            rename_map["amount"] = "amount"

        df = df.rename(columns=rename_map)

        if {"account", "amount"}.issubset(df.columns):
            # Clean amount column
            df["amount"] = (
                df["amount"]
                .astype(str)
                .str.replace(",", "")
                .str.replace("(", "-")
                .str.replace(")", "")
                .str.strip()
                .replace("", "0")
                .astype(float)
            )
            return df[["account", "amount"]]

    raise ValueError("No recognizable Financial (P&L) table found in PDF")
