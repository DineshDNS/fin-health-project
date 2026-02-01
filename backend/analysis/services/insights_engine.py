def generate_actionable_insights(
    profitability_risk,
    net_cash_flow,
    cash_flow_volatile,
):
    insights = []

    # ---- Profitability-based insights ----
    if profitability_risk == "HIGH":
        insights.append(
            "Reduce operating expenses by reviewing fixed and variable costs."
        )

    if profitability_risk == "MEDIUM":
        insights.append(
            "Improve profit margins by optimizing pricing or reducing overheads."
        )

    # ---- Cash flow-based insights ----
    if net_cash_flow < 0:
        insights.append(
            "Improve cash collections by tightening credit terms and following up on receivables."
        )

    if cash_flow_volatile:
        insights.append(
            "Build a short-term cash buffer to manage cash flow volatility."
        )

    return insights
