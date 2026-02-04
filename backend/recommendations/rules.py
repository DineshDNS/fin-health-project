from .constants import RecommendationCategory


# -----------------------------
# BANK-BASED RECOMMENDATIONS
# -----------------------------

def negative_cashflow_rule(bank):
    """
    Triggered when business spends more than it earns.
    """
    if not bank:
        return None

    if bank.net_cash_flow is not None and bank.net_cash_flow < 0:
        return {
            "id": "CASHFLOW_001",
            "category": RecommendationCategory.CASHFLOW_IMPROVEMENT,
            "priority": "HIGH",
            "trigger": "Negative net cash flow",
            "action": "Reduce non-essential expenses and accelerate customer receivables",
            "expected_impact": "Improves liquidity within 30–60 days",
            "confidence": "HIGH",
        }

    return None


def high_expense_ratio_rule(bank):
    """
    Triggered when expenses consume most of the income.
    """
    if not bank:
        return None

    if bank.expense_ratio is not None and bank.expense_ratio > 0.8:
        return {
            "id": "COST_001",
            "category": RecommendationCategory.COST_OPTIMIZATION,
            "priority": "HIGH",
            "trigger": "High expense ratio",
            "action": "Review fixed costs and reduce discretionary spending",
            "expected_impact": "Improves profit margin and cash reserves",
            "confidence": "HIGH",
        }

    return None


def cashflow_volatility_rule(bank):
    """
    Triggered when income is unstable month-to-month.
    """
    if not bank:
        return None

    if bank.cashflow_volatile:
        return {
            "id": "CASHFLOW_002",
            "category": RecommendationCategory.CASHFLOW_IMPROVEMENT,
            "priority": "MEDIUM",
            "trigger": "Cash flow volatility detected",
            "action": "Stabilize income sources and maintain a monthly cash buffer",
            "expected_impact": "Reduces operational risk during low-revenue periods",
            "confidence": "MEDIUM",
        }

    return None


# -----------------------------
# GST-BASED RECOMMENDATIONS
# -----------------------------

def gst_compliance_gap_rule(gst):
    """
    Triggered when GST liability is not fully settled.
    """
    if not gst:
        return None

    if gst.compliance_gap is not None and gst.compliance_gap > 0:
        return {
            "id": "GST_001",
            "category": RecommendationCategory.GST_COMPLIANCE,
            "priority": "HIGH",
            "trigger": "GST compliance gap detected",
            "action": "Set aside GST collections separately and file returns on time",
            "expected_impact": "Avoids penalties and improves creditworthiness",
            "confidence": "HIGH",
        }

    return None


def gst_overpayment_rule(gst):
    """
    Triggered when GST paid exceeds expected liability.
    """
    if not gst:
        return None

    if gst.compliance_gap is not None and gst.compliance_gap < 0:
        return {
            "id": "GST_002",
            "category": RecommendationCategory.GST_COMPLIANCE,
            "priority": "LOW",
            "trigger": "GST overpayment detected",
            "action": "Review GST filings and adjust future payments or claim refunds",
            "expected_impact": "Improves cash availability",
            "confidence": "MEDIUM",
        }

    return None


# -----------------------------
# FINANCIAL-STATEMENT RECOMMENDATIONS
# -----------------------------

def low_savings_ratio_rule(fin):
    """
    Triggered when savings buffer is weak.
    """
    if not fin:
        return None

    if fin.savings_ratio is not None and fin.savings_ratio < 0.1:
        return {
            "id": "FIN_001",
            "category": RecommendationCategory.FINANCIAL_STABILITY,
            "priority": "MEDIUM",
            "trigger": "Low savings buffer",
            "action": "Build a cash reserve equal to at least 3 months of expenses",
            "expected_impact": "Improves financial resilience",
            "confidence": "MEDIUM",
        }

    return None


def weak_liquidity_rule(fin):
    """
    Triggered when current ratio indicates liquidity stress.
    """
    if not fin:
        return None

    if fin.current_ratio is not None and fin.current_ratio < 1.0:
        return {
            "id": "FIN_002",
            "category": RecommendationCategory.FINANCIAL_STABILITY,
            "priority": "HIGH",
            "trigger": "Weak liquidity position",
            "action": "Improve working capital by reducing short-term liabilities",
            "expected_impact": "Prevents short-term cash shortages",
            "confidence": "HIGH",
        }

    return None


# -----------------------------
# ML-BASED RECOMMENDATIONS
# -----------------------------

def ml_high_risk_rule(ml_result):
    """
    Triggered when ML model predicts high credit risk.
    """
    if not ml_result:
        return None

    if ml_result.get("ml_risk_level") == "HIGH":
        return {
            "id": "CREDIT_001",
            "category": RecommendationCategory.CREDIT_READINESS,
            "priority": "HIGH",
            "trigger": "High credit risk detected by ML assessment",
            "action": "Stabilize cash flow and maintain compliance before applying for credit",
            "expected_impact": "Improves loan eligibility and approval chances",
            "confidence": "HIGH",
        }

    return None


def ml_moderate_risk_rule(ml_result):
    """
    Triggered when ML model predicts moderate credit risk.
    """
    if not ml_result:
        return None

    if ml_result.get("ml_risk_level") == "MODERATE":
        return {
            "id": "CREDIT_002",
            "category": RecommendationCategory.CREDIT_READINESS,
            "priority": "MEDIUM",
            "trigger": "Moderate credit risk detected by ML assessment",
            "action": "Maintain consistent cash flow and timely tax compliance",
            "expected_impact": "Strengthens credit profile over time",
            "confidence": "MEDIUM",
        }

    return None
