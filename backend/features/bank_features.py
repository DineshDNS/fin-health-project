def compute_bank_features(parsed_bank_data: dict) -> dict:
    """
    Input:
    {
        total_credits,
        total_debits,
        closing_balance
    }
    """

    total_credits = parsed_bank_data.get("total_credits", 0)
    total_debits = parsed_bank_data.get("total_debits", 0)
    closing_balance = parsed_bank_data.get("closing_balance", 0)

    net_cash_flow = total_credits - total_debits

    expense_ratio = (
        total_debits / total_credits
        if total_credits > 0 else 0
    )

    savings_ratio = (
        net_cash_flow / total_credits
        if total_credits > 0 else 0
    )

    cashflow_volatile = expense_ratio > 0.7

    return {
        "total_credits": total_credits,
        "total_debits": total_debits,
        "net_cash_flow": net_cash_flow,
        "closing_balance": closing_balance,
        "expense_ratio": round(expense_ratio, 2),
        "savings_ratio": round(savings_ratio, 2),
        "cashflow_volatile": cashflow_volatile,
    }
