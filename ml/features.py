def compute_features(gst, bank):
    """
    gst: GSTRecord instance
    bank: BankStatement instance
    """

    revenue = gst.total_sales
    tax_paid = gst.total_tax_paid

    inflow = bank.total_inflow
    outflow = bank.total_outflow
    emi = bank.loan_emi
    avg_balance = bank.average_balance

    features = {
        "profit_margin": (revenue - outflow) / revenue if revenue else 0,
        "cash_flow_ratio": inflow / outflow if outflow else 0,
        "emi_ratio": emi / inflow if inflow else 0,
        "tax_compliance": 1 if gst.filing_status else 0,
        "liquidity_ratio": avg_balance / outflow if outflow else 0,
    }

    return features
