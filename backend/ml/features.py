def extract_features(bank=None, gst=None, fin=None):
    """
    Build unified ML feature vector from BANK, GST, and FIN analyses.
    Missing data is handled safely.
    """

    return {
        # ---------- BANK ----------
        "total_credits": getattr(bank, "total_credits", 0) or 0,
        "total_debits": getattr(bank, "total_debits", 0) or 0,
        "net_cash_flow": getattr(bank, "net_cash_flow", 0) or 0,
        "expense_ratio": getattr(bank, "expense_ratio", 1) or 1,
        "cashflow_volatile": int(getattr(bank, "cashflow_volatile", 1)),

        # ---------- GST ----------
        "gst_compliance_gap": getattr(gst, "compliance_gap", 0) or 0,
        "gst_filing_delay": int(
            getattr(gst, "filing_delay_days", 0) > 30
        ),

        # ---------- FINANCIAL ----------
        "debt_to_asset_ratio": (
            getattr(fin, "total_liabilities", 0) /
            max(getattr(fin, "total_assets", 1), 1)
        ),
        "savings_ratio": getattr(fin, "savings_ratio", 0) or 0,
        "current_ratio": getattr(fin, "current_ratio", 1) or 1,
    }
