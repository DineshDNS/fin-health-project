import pandas as pd


def parse_financial_dataframe(df: pd.DataFrame):
    """
    Safely parse FIN CSV.
    Expected columns:
    metric,value,year,source
    """

    # Normalize column names
    df.columns = [c.strip().lower() for c in df.columns]

    # Validate structure
    if "metric" not in df.columns or "value" not in df.columns:
        raise ValueError("FIN file must contain metric and value columns")

    financials = {}

    for _, row in df.iterrows():
        metric = str(row["metric"]).strip().lower()
        value = row["value"]

        try:
            financials[metric] = float(value)
        except (ValueError, TypeError):
            # Ignore non-numeric safely
            continue

    return financials
