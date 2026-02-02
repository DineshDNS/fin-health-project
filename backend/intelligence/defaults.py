# intelligence/defaults.py

BANK_DEFAULT = {
    "total_credits": 0.0,
    "total_debits": 0.0,
    "net_cash_flow": 0.0,
    "closing_balance": 0.0,
    "expense_ratio": 0.0,
    "savings_ratio": 0.0,
    "cashflow_volatile": False,
    "status": "no_structured_bank_data",
}

GST_DEFAULT = {
    "total_taxable_value": 0.0,
    "total_gst": 0.0,
    "is_compliant": False,
    "payment_ratio": 0.0,
    "return_type": None,
    "status": "no_structured_gst_data",
}


FIN_DEFAULT = {
    "total_revenue": 0.0,
    "total_expenses": 0.0,
    "net_profit": 0.0,
    "profit_margin": 0.0,
    "status": "no_structured_financial_data",
}
