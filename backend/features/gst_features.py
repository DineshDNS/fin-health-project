def compute_gst_features(parsed_gst_data: dict) -> dict:
    """
    Input:
    {
        taxable_value,
        gst_paid,
        expected_gst
    }
    """

    taxable_value = parsed_gst_data.get("taxable_value", 0)
    gst_paid = parsed_gst_data.get("gst_paid", 0)
    expected_gst = parsed_gst_data.get("expected_gst", 0)

    payment_ratio = (
        gst_paid / expected_gst
        if expected_gst > 0 else 0
    )

    compliance_gap = max(0, expected_gst - gst_paid)

    return {
        "taxable_value": taxable_value,
        "gst_paid": gst_paid,
        "expected_gst": expected_gst,
        "payment_ratio": round(payment_ratio, 2),
        "compliance_gap": compliance_gap,
        "is_compliant": payment_ratio >= 0.95,
    }
