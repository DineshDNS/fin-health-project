def compute_financial_health_score(state):
    score = 100

    if state.cashflow_volatile:
        score -= 20

    if state.compliance_gap > 0:
        score -= 15

    score = max(0, min(100, score))
    return score
