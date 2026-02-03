def extract_features(state):
    """
    Convert CumulativeAnalysisState into normalized ML-ready features.
    Works with FLAT state attributes (no nested dicts).
    """

    features = {}

    # ------------------
    # Bank-related fields
    # ------------------
    total_credits = getattr(state, "total_credits", 0) or 0
    total_debits = getattr(state, "total_debits", 0) or 0
    net_cash_flow = getattr(state, "net_cash_flow", 0) or 0

    features["net_cash_flow_ratio"] = (
        net_cash_flow / total_credits if total_credits else 0
    )

    features["expense_ratio"] = getattr(state, "expense_ratio", 0) or 0
    features["savings_ratio"] = getattr(state, "savings_ratio", 0) or 0
    features["cashflow_volatile"] = int(
        getattr(state, "cashflow_volatile", False)
    )

    # ------------------
    # GST-related fields
    # ------------------
    expected_gst = getattr(state, "expected_gst", 0) or 0
    gst_paid = getattr(state, "gst_paid", 0) or 0
    compliance_gap = getattr(state, "compliance_gap", 0) or 0

    features["gst_compliance_ratio"] = (
        gst_paid / expected_gst if expected_gst else 1
    )

    features["compliance_gap_ratio"] = (
        compliance_gap / expected_gst if expected_gst else 0
    )

    # ------------------
    # Data coverage (confidence)
    # ------------------
    has_bank_data = int(total_credits > 0)
    has_gst_data = int(expected_gst > 0)

    features["data_coverage_score"] = (has_bank_data + has_gst_data) / 2

    return features
