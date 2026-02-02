def recommend_products(
    bank_features: dict | None,
    risk_level: str,
) -> list[dict]:
    products = []

    if not bank_features:
        return products

    if bank_features["net_cash_flow"] < 0:
        products.append({
            "name": "Working Capital Loan",
            "provider": "HDFC Bank",
            "reason": "To manage short-term cash flow gaps",
            "suitability": "High",
        })

    if risk_level == "LOW" and bank_features["net_cash_flow"] > 0:
        products.append({
            "name": "Business Expansion Loan",
            "provider": "SBI",
            "reason": "Stable finances support growth",
            "suitability": "Medium",
        })

    return products
