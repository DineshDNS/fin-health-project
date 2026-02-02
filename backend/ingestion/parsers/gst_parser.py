# ingestion/parsers/gst_parser.py

def parse_gst_dataframe(df):
    """
    Supported formats:
    1) GSTR-1  : taxable_value, gst_amount
    2) GSTR-3B : total_taxable_value, total_gst
    """

    # Normalize columns
    df.columns = [str(c).strip().lower() for c in df.columns]

    parsed = {
        "return_type": None,
        "total_taxable_value": 0.0,
        "total_gst": 0.0,
    }

    # 🟢 GSTR-1 (invoice level)
    if {"taxable_value", "gst_amount"}.issubset(df.columns):
        parsed["return_type"] = "GSTR1"
        parsed["total_taxable_value"] = float(df["taxable_value"].fillna(0).sum())
        parsed["total_gst"] = float(df["gst_amount"].fillna(0).sum())

    # 🟡 GSTR-3B (summary level)
    elif {"total_taxable_value", "total_gst"}.issubset(df.columns):
        parsed["return_type"] = "GSTR3B"
        parsed["total_taxable_value"] = float(df["total_taxable_value"].fillna(0).sum())
        parsed["total_gst"] = float(df["total_gst"].fillna(0).sum())

    else:
        raise ValueError("Unsupported GST file format")

    return parsed
