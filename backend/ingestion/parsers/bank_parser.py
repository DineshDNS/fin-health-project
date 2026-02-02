# ingestion/parsers/bank_parser.py

def parse_bank_dataframe(df):
    """
    Expected columns (case-insensitive):
    Date | Description | Debit | Credit | Balance
    """

    # 🔹 Normalize column names
    df.columns = [str(c).strip().lower() for c in df.columns]

    REQUIRED_COLUMNS = {"date", "description", "debit", "credit", "balance"}
    missing = REQUIRED_COLUMNS - set(df.columns)

    if missing:
        raise ValueError(f"Missing required bank columns: {missing}")

    total_credits = 0.0
    total_debits = 0.0
    closing_balance = 0.0
    transaction_count = 0

    for _, row in df.iterrows():
        debit = float(row.get("debit") or 0)
        credit = float(row.get("credit") or 0)
        balance = row.get("balance")

        total_debits += debit
        total_credits += credit
        transaction_count += 1

        # Always take last non-null balance
        if balance not in ("", None):
            closing_balance = float(balance)

    net_cash_flow = total_credits - total_debits

    return {
        "total_credits": round(total_credits, 2),
        "total_debits": round(total_debits, 2),
        "net_cash_flow": round(net_cash_flow, 2),
        "closing_balance": round(closing_balance, 2),
        "transaction_count": transaction_count,
    }
