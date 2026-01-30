def calculate_health_score(features: dict):
    score = 0

    # Profit margin (30%)
    score += min(features["profit_margin"] * 30, 30)

    # Cash flow (25%)
    score += min(features["cash_flow_ratio"] * 25, 25)

    # EMI burden (20%)
    score += max(20 - (features["emi_ratio"] * 20), 0)

    # Tax compliance (15%)
    score += features["tax_compliance"] * 15

    # Liquidity (10%)
    score += min(features["liquidity_ratio"] * 10, 10)

    return round(score, 2)


def classify_risk(score):
    if score >= 75:
        return "LOW"
    elif score >= 50:
        return "MEDIUM"
    else:
        return "HIGH"
