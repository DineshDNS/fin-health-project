def calculate_financial_health_score(
    bank_features: dict | None,
    gst_features: dict | None,
) -> int:
    """
    Returns score between 0–100
    """

    score = 0
    weight = 0

    # ---- BANK (60%) ----
    if bank_features:
        bank_score = 0

        if bank_features["net_cash_flow"] > 0:
            bank_score += 25

        if bank_features["expense_ratio"] < 0.7:
            bank_score += 20

        if bank_features["savings_ratio"] > 0.2:
            bank_score += 15

        score += bank_score
        weight += 60

    # ---- GST (40%) ----
    if gst_features:
        gst_score = 0

        if gst_features["is_compliant"]:
            gst_score += 25

        gst_score += min(
            15,
            gst_features["payment_ratio"] * 15
        )

        score += gst_score
        weight += 40

    if weight == 0:
        return 0

    return round(score)
