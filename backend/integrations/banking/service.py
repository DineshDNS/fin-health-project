def fetch_bank_data(account_id: str):
    """
    Simulated Account Aggregator API call
    """
    return {
        "account_id": account_id,
        "month": "2025-12",
        "total_inflow": 900000,
        "total_outflow": 820000,
        "average_balance": 150000,
        "loan_emi": 40000
    }
