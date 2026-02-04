def detect_key_concerns(bank=None, gst=None, fin=None, ml_result=None):
    concerns = []

    # Liquidity risk
    if fin and fin.current_ratio is not None and fin.current_ratio < 0.75:
        concerns.append({
            "type": "LIQUIDITY_RISK",
            "severity": "HIGH",
            "message": "Current assets may not be sufficient to meet short-term obligations"
        })

    # Persistent cash flow stress
    if bank and bank.net_cash_flow < 0:
        concerns.append({
            "type": "CASHFLOW_RISK",
            "severity": "HIGH",
            "message": "Sustained negative cash flow detected"
        })

    # GST compliance risk
    if gst and gst.compliance_gap and gst.compliance_gap > 0:
        concerns.append({
            "type": "COMPLIANCE_RISK",
            "severity": "MEDIUM",
            "message": "GST compliance gaps may attract penalties"
        })

    # ML high-risk signal
    if ml_result and ml_result.get("ml_risk_level") == "HIGH":
        concerns.append({
            "type": "CREDIT_RISK",
            "severity": "HIGH",
            "message": "High credit risk detected by ML assessment"
        })

    return concerns


def should_offer_financing(recommendations, risk_level):
    if risk_level == "HIGH":
        return True

    financing_categories = {
        "CASHFLOW_IMPROVEMENT",
        "CREDIT_READINESS",
    }

    return any(
        r["category"] in financing_categories
        for r in recommendations
    )


def build_action_plan(concerns):
    if not concerns:
        return []

    steps = []
    step_no = 1

    for c in concerns:
        if c["type"] == "CASHFLOW_RISK":
            steps.append({
                "step": step_no,
                "action": "Reduce non-essential expenses and accelerate receivables",
                "timeframe": "Next 30 days",
                "expected_outcome": "Improves monthly cash surplus"
            })
            step_no += 1

        if c["type"] == "LIQUIDITY_RISK":
            steps.append({
                "step": step_no,
                "action": "Renegotiate short-term liabilities and improve working capital",
                "timeframe": "Next 45 days",
                "expected_outcome": "Reduces liquidity pressure"
            })
            step_no += 1

        if c["type"] == "COMPLIANCE_RISK":
            steps.append({
                "step": step_no,
                "action": "Review GST filings and clear compliance gaps",
                "timeframe": "Immediate",
                "expected_outcome": "Avoids penalties and interest"
            })
            step_no += 1

    return steps
