def assess_risk(bank_features: dict | None) -> dict:
    """
    Generates risk alerts
    """

    priority_issues = []
    warnings = []

    if not bank_features:
        return {
            "priority_issues": [],
            "warnings": [],
        }

    if bank_features["net_cash_flow"] < 0:
        priority_issues.append(
            "Negative cash flow detected"
        )

    if bank_features["cashflow_volatile"]:
        warnings.append(
            "High expense ratio indicates cash flow volatility"
        )

    return {
        "priority_issues": priority_issues,
        "warnings": warnings,
    }
