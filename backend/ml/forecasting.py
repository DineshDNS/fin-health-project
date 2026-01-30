import numpy as np


def cashflow_forecast(bank_records, months=3):
    """
    bank_records: list of BankStatement objects (ordered by month)
    months: number of future months to predict
    """

    inflows = [b.total_inflow for b in bank_records]
    outflows = [b.total_outflow for b in bank_records]

    # Simple moving average
    avg_inflow = np.mean(inflows)
    avg_outflow = np.mean(outflows)

    forecast = []
    for i in range(1, months + 1):
        forecast.append({
            "month": f"Month +{i}",
            "predicted_inflow": round(avg_inflow, 2),
            "predicted_outflow": round(avg_outflow, 2),
            "predicted_net_cashflow": round(avg_inflow - avg_outflow, 2)
        })

    return forecast
