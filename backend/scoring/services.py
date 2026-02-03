def compute_financial_health_score(data, document_type):
    """
    Rule-based financial health scoring (per document).
    """
    score = 100

    if document_type == "BANK":
        if data.get("net_cash_flow", 0) < 0:
            score -= 30

        if data.get("expense_ratio", 0) > 0.8:
            score -= 20

        if data.get("cashflow_volatile", False):
            score -= 10

    elif document_type == "GST":
        if data.get("compliance_gap", 0) > 0:
            score -= 25

    elif document_type == "FIN":
        # Placeholder for future financial logic
        score -= 10  # minimal impact for now

    return max(score, 0)


def determine_risk_level(score):
    """
    Convert numeric score into risk band.
    """
    if score >= 75:
        return "LOW"
    elif score >= 50:
        return "MODERATE"
    else:
        return "HIGH"
