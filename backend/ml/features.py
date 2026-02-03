def extract_features(analysis):
    """
    Convert DocumentAnalysis → ML feature vector
    """

    return {
        # BANK FEATURES
        "net_cash_flow": analysis.net_cash_flow,
        "expense_ratio": analysis.expense_ratio,
        "cashflow_volatile": int(analysis.cashflow_volatile),

        # GST FEATURES
        "compliance_gap": analysis.compliance_gap,
        "gst_paid_ratio": (
            analysis.gst_paid / analysis.expected_gst
            if analysis.expected_gst > 0 else 1
        ),

        # GLOBAL
        "financial_health_score": analysis.financial_health_score,
    }
