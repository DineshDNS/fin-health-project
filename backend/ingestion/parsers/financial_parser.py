# ingestion/parsers/financial_parser.py

def parse_financial_dataframe(df):
    """
    Expected columns:
    account | amount
    """

    # Normalize columns
    df.columns = [str(c).strip().lower() for c in df.columns]

    if not {"account", "amount"}.issubset(df.columns):
        raise ValueError("Financial file must contain 'account' and 'amount' columns")

    total_revenue = 0.0
    total_expenses = 0.0

    for _, row in df.iterrows():
        account = str(row["account"]).lower()
        amount = float(row["amount"] or 0)

        if any(word in account for word in ["revenue", "sales", "income"]):
            total_revenue += amount

        elif any(word in account for word in ["expense", "cost", "rent", "salary"]):
            total_expenses += amount

    return {
        "total_revenue": round(total_revenue, 2),
        "total_expenses": round(total_expenses, 2),
        "net_profit": round(total_revenue - total_expenses, 2),
    }
