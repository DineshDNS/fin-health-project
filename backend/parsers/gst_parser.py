import pandas as pd


def _to_number(df_or_series):
    """
    Safely convert a pandas Series OR DataFrame to numeric.
    Handles commas, currency symbols, empty strings, NaNs.
    """
    if isinstance(df_or_series, pd.DataFrame):
        return df_or_series.apply(_to_number)

    # Now guaranteed to be Series
    return (
        df_or_series.astype(str)
        .str.replace(",", "", regex=False)
        .str.replace("₹", "", regex=False)
        .str.strip()
        .replace("", "0")
        .astype(float)
    )


def parse_gst_dataframe(df):
    """
    Parse GST data from CSV / XLSX / PDF tables.
    Fully numeric-safe and crash-proof.
    """
    if df is None or df.empty:
        return {
            "taxable_value": 0.0,
            "gst_paid": 0.0,
            "expected_gst": 0.0,
            "payment_ratio": 1.0,
            "compliance_gap": 0.0,
            "is_compliant": True,
        }

    taxable_cols = df.columns[df.columns.str.contains("taxable", case=False)]
    paid_cols = df.columns[df.columns.str.contains("gst.*paid", case=False, regex=True)]
    expected_cols = df.columns[
        df.columns.str.contains("gst.*expected|gst.*payable|gst.*due", case=False, regex=True)
    ]

    taxable_value = (
        _to_number(df[taxable_cols]).sum().sum()
        if len(taxable_cols)
        else 0.0
    )

    gst_paid = (
        _to_number(df[paid_cols]).sum().sum()
        if len(paid_cols)
        else 0.0
    )

    expected_gst = (
        _to_number(df[expected_cols]).sum().sum()
        if len(expected_cols)
        else 0.0
    )

    payment_ratio = gst_paid / expected_gst if expected_gst else 1.0
    compliance_gap = expected_gst - gst_paid
    is_compliant = payment_ratio >= 0.95

    return {
        "taxable_value": float(taxable_value),
        "gst_paid": float(gst_paid),
        "expected_gst": float(expected_gst),
        "payment_ratio": float(payment_ratio),
        "compliance_gap": float(compliance_gap),
        "is_compliant": is_compliant,
    }
