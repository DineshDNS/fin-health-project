def cash_flow_risk(net_cash_flow, is_volatile):
    """
    Question 2: Cash flow risk
    """

    priority_issues = []
    warnings = []

    if net_cash_flow < 0:
        priority_issues.append(
            "Negative cash flow detected"
        )

    if is_volatile:
        warnings.append(
            "Cash flow volatility detected"
        )

    return {
        "priority_issues": priority_issues,
        "warnings": warnings,
    }
