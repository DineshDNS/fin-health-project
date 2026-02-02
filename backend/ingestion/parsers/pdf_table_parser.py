import camelot
import pandas as pd
import re


def extract_bank_table_from_pdf(path: str) -> pd.DataFrame:
    """
    Try Camelot table extraction first.
    If it fails, fallback to text-based row parsing.
    """

    # ---- 1️⃣ Try Camelot ----
    try:
        tables = camelot.read_pdf(path, pages="all", flavor="stream")
        if tables.n > 0:
            for table in tables:
                df = table.df.copy()
                df.columns = df.iloc[0]
                df = df[1:]
                df.columns = [str(c).strip().lower() for c in df.columns]

                REQUIRED = {"date", "description", "debit", "credit", "balance"}
                if REQUIRED.issubset(set(df.columns)):
                    for col in ["debit", "credit", "balance"]:
                        df[col] = (
                            df[col]
                            .astype(str)
                            .str.replace(",", "")
                            .str.strip()
                            .replace("", "0")
                            .astype(float)
                        )
                    return df
    except Exception:
        pass  # fallback below

    # ---- 2️⃣ Fallback: parse pipe-separated text ----
    from ingestion.parsers.pdf_parser import extract_pdf_text

    text = extract_pdf_text(path)
    rows = []

    for line in text.splitlines():
        if "|" in line and any(ch.isdigit() for ch in line):
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 5:
                rows.append(parts[:5])

    if not rows:
        raise ValueError("No bank table data found in PDF")

    df = pd.DataFrame(
        rows,
        columns=["date", "description", "debit", "credit", "balance"],
    )

    for col in ["debit", "credit", "balance"]:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace(",", "")
            .replace("", "0")
            .astype(float)
        )

    return df
