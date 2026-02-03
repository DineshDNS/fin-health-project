def parse_financial_dataframe(df):
    """
    Parse financial statement ONLY if a valid DataFrame is provided.
    """
    if df is None or df.empty:
        return {
            "financial_total": 0.0
        }

    # Common pattern: account | amount
    amount_column = df.columns[-1]

    total_amount = df[amount_column].sum()

    return {
        "financial_total": float(total_amount)
    }
