def apply_credit_rules(features):
    """
    Apply hard rules and penalties.
    Returns base_score (0–100) and rule flags.
    """
    score = 100
    flags = []

    # --- Cash flow rules ---
    if features["net_cash_flow_ratio"] < 0:
        score -= 30
        flags.append("Negative net cash flow")

    elif features["net_cash_flow_ratio"] < 0.05:
        score -= 15
        flags.append("Low net cash flow margin")

    # --- Expense discipline ---
    if features["expense_ratio"] > 0.8:
        score -= 20
        flags.append("High expense ratio")

    elif features["expense_ratio"] > 0.65:
        score -= 10
        flags.append("Moderate expense pressure")

    # --- Stability ---
    if features["cashflow_volatile"]:
        score -= 10
        flags.append("Cash flow volatility detected")

    # --- GST compliance ---
    if features["gst_compliance_ratio"] < 0.8:
        score -= 25
        flags.append("Poor GST compliance")

    elif features["gst_compliance_ratio"] < 0.95:
        score -= 10
        flags.append("Minor GST compliance gaps")

    # --- Data reliability ---
    if features["data_coverage_score"] < 0.5:
        score -= 15
        flags.append("Insufficient financial data")

    return max(score, 0), flags
