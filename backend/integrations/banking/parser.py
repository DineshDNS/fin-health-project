def normalize_bank_data(raw_data: dict):
    """
    Normalize banking API response
    """
    return {
        "account_id": raw_data["account_id"],
        "month": raw_data["month"],
        "total_inflow": raw_data["total_inflow"],
        "total_outflow": raw_data["total_outflow"],
        "average_balance": raw_data["average_balance"],
        "loan_emi": raw_data["loan_emi"]
    }
