def fetch_gst_data(gstin: str):
    """
    Simulated GST API call
    (Represents ClearTax / GSTN aggregator)
    """
    return {
        "gstin": gstin,
        "period": "2025-12",
        "total_sales": 1200000,
        "total_tax_paid": 216000,
        "filing_status": True
    }
