import camelot
import pandas as pd


def extract_gst_table_from_pdf(path: str) -> pd.DataFrame:
    """
    Extract GST tables from a text-based PDF.
    Supports:
    - GSTR-1 (invoice-level)
    - GSTR-3B (summary-level)
    """

    tables = camelot.read_pdf(path, pages="all", flavor="stream")

    if tables.n == 0:
        raise ValueError("No tables found in GST PDF")

    # Try each table until one matches GST patterns
    for table in tables:
        df = table.df.copy()

        # First row as header
        df.columns = df.iloc[0]
        df = df[1:]

        df.columns = [str(c).strip().lower() for c in df.columns]

        # 🟢 GSTR-1 pattern
        if {"taxable value", "gst amount"}.issubset(df.columns):
            df = df.rename(
                columns={
                    "taxable value": "taxable_value",
                    "gst amount": "gst_amount",
                }
            )
            return df

        # 🟡 GSTR-3B pattern
        if {"total taxable value", "total gst"}.issubset(df.columns):
            df = df.rename(
                columns={
                    "total taxable value": "total_taxable_value",
                    "total gst": "total_gst",
                }
            )
            return df

    raise ValueError("No recognizable GST table found in PDF")
