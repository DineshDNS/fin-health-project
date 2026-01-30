def normalize_gst_data(raw_data: dict):
    """
    Normalize GST API response to DB-ready format
    """
    return {
        "gstin": raw_data["gstin"],
        "period": raw_data["period"],
        "total_sales": raw_data["total_sales"],
        "total_tax_paid": raw_data["total_tax_paid"],
        "filing_status": raw_data["filing_status"]
    }
