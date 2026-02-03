def merge_bank(state, data):
    state.total_credits += data["total_credits"]
    state.total_debits += data["total_debits"]
    state.net_cash_flow += data["net_cash_flow"]
    state.closing_balance = data["closing_balance"]

    state.expense_ratio = (
        state.total_debits / state.total_credits
        if state.total_credits else 0
    )

    state.savings_ratio = (
        state.net_cash_flow / state.total_credits
        if state.total_credits else 0
    )

    state.cashflow_volatile = state.expense_ratio > 0.7
