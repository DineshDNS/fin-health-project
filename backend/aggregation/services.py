from .models import CumulativeAnalysisState


def get_cumulative_state():
    """
    Read-only accessor for cumulative financial state.
    Used by overview & analysis APIs.
    """
    state, _ = CumulativeAnalysisState.objects.get_or_create(id=1)
    return state


def update_cumulative_state(parsed_data, document_type):
    """
    Merge newly parsed document data into cumulative state.
    Accumulates values instead of overwriting.
    """
    state, _ = CumulativeAnalysisState.objects.get_or_create(id=1)

    if document_type == "BANK":
        state.total_credits += parsed_data.get("total_credits", 0)
        state.total_debits += parsed_data.get("total_debits", 0)
        state.net_cash_flow += parsed_data.get("net_cash_flow", 0)
        state.closing_balance = parsed_data.get(
            "closing_balance", state.closing_balance
        )
        state.expense_ratio = (
            state.total_debits / state.total_credits
            if state.total_credits
            else 0
        )
        state.savings_ratio = (
            state.net_cash_flow / state.total_credits
            if state.total_credits
            else 0
        )
        state.cashflow_volatile = state.expense_ratio > 0.7

    elif document_type == "GST":
        state.taxable_value += parsed_data.get("taxable_value", 0)
        state.gst_paid += parsed_data.get("gst_paid", 0)
        state.expected_gst += parsed_data.get("expected_gst", 0)
        state.compliance_gap = state.expected_gst - state.gst_paid

    # FIN documents reserved for future

    state.save()
    return state
