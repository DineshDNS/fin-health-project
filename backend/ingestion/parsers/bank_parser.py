def parse_bank_dataframe(df):
    credits = 0
    debits = 0

    for _, row in df.iterrows():
        amount = float(row["amount"])
        txn_type = str(row["type"]).upper().strip()

        if txn_type == "CREDIT":
            credits += amount
        elif txn_type == "DEBIT":
            debits += amount

    return {
        "total_credits": credits,
        "total_debits": debits,
        "closing_balance": credits - debits,
    }
