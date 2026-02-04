import pandas as pd
from ml.model import train_model

# Load training dataset
df = pd.read_csv("data/credit_dataset.csv")

FEATURES = [
    "total_credits",
    "total_debits",
    "net_cash_flow",
    "expense_ratio",
    "cashflow_volatile",
    "gst_compliance_gap",
    "gst_filing_delay",
    "debt_to_asset_ratio",
    "savings_ratio",
    "current_ratio",
]

X = df[FEATURES]
y = df["is_good_credit"]

# Train and save scaled ML pipeline
train_model(X, y)

print("ML model retrained and saved successfully")
