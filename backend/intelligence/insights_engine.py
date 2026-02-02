def generate_actionable_insights(
    bank_features: dict | None,
    gst_features: dict | None,
) -> list[str]:
    insights = []

    if bank_features:
        if bank_features["expense_ratio"] > 0.75:
            insights.append(
                "Reduce operating expenses to improve cash stability."
            )

        if bank_features["savings_ratio"] < 0.15:
            insights.append(
                "Increase savings to build financial resilience."
            )

    if gst_features:
        if not gst_features["is_compliant"]:
            insights.append(
                "Clear GST dues promptly to avoid penalties."
            )

    return insights
