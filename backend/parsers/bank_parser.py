import pandas as pd


def _to_number(df_or_series):
    """
    Safely convert a pandas Series OR DataFrame to numeric.
    Handles commas, currency symbols, empty strings, NaNs.
    """
    if isinstance(df_or_series, pd.DataFrame):
        return df_or_series.apply(_to_number)

    return (
        df_or_series.astype(str)
        .str.replace(",", "", regex=False)
        .str.replace("₹", "", regex=False)
        .str.strip()
        .replace("", "0")
        .astype(float)
    )


def parse_bank_dataframe(df):
    """
    Parse bank statement data from CSV / XLSX / PDF tables.
    Fully numeric-safe and crash-proof.
    """
    if df is None or df.empty:
        return {
            "total_credits": 0.0,
            "total_debits": 0.0,
            "net_cash_flow": 0.0,
            "closing_balance": 0.0,
            "expense_ratio": 0.0,
            "savings_ratio": 0.0,
            "cashflow_volatile": False,
        }

    credit_cols = df.columns[df.columns.str.contains("credit", case=False)]
    debit_cols = df.columns[df.columns.str.contains("debit", case=False)]
    balance_cols = df.columns[df.columns.str.contains("balance", case=False)]

    total_credits = (
        _to_number(df[credit_cols]).sum().sum()
        if len(credit_cols)
        else 0.0
    )

    total_debits = (
        _to_number(df[debit_cols]).sum().sum()
        if len(debit_cols)
        else 0.0
    )

    closing_balance = (
        _to_number(df.iloc[-1][balance_cols]).sum()
        if len(balance_cols)
        else 0.0
    )

    net_cash_flow = total_credits - total_debits

    expense_ratio = total_debits / total_credits if total_credits else 0.0
    savings_ratio = net_cash_flow / total_credits if total_credits else 0.0

    cashflow_volatile = expense_ratio > 0.7

    return {
        "total_credits": float(total_credits),
        "total_debits": float(total_debits),
        "net_cash_flow": float(net_cash_flow),
        "closing_balance": float(closing_balance),
        "expense_ratio": float(expense_ratio),
        "savings_ratio": float(savings_ratio),
        "cashflow_volatile": cashflow_volatile,
    }
