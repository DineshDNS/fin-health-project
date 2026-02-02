def parse_gst_dataframe(df):
    taxable_value = df["taxable_value"].sum()
    gst_paid = df["gst_paid"].sum()
    expected_gst = taxable_value * 0.18

    return {
        "taxable_value": taxable_value,
        "gst_paid": gst_paid,
        "expected_gst": expected_gst,
    }
