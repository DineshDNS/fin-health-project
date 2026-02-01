def recommend_products(profitability_risk, net_cash_flow, cash_flow_volatile):
    products = []

    if net_cash_flow < 0:
        products.append({
            "name": "SME Working Capital Loan",
            "provider": "HDFC Bank",
            "category": "Working Capital",
        })

        products.append({
            "name": "Invoice Discounting Facility",
            "provider": "TReDS Platform",
            "category": "Receivables Financing",
        })

    if cash_flow_volatile:
        products.append({
            "name": "Business Overdraft Facility",
            "provider": "ICICI Bank",
            "category": "Liquidity",
        })

    if profitability_risk == "LOW" and net_cash_flow > 0:
        products.append({
            "name": "Business Expansion Loan",
            "provider": "SBI",
            "category": "Growth",
        })

    return products
