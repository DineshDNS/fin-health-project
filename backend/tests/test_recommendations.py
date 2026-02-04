import pytest

from recommendations.engine import generate_recommendations


# ---------------------------
# Mock objects
# ---------------------------

class MockBank:
    def __init__(self, net_cash_flow=None, expense_ratio=None, cashflow_volatile=False):
        self.net_cash_flow = net_cash_flow
        self.expense_ratio = expense_ratio
        self.cashflow_volatile = cashflow_volatile


class MockGST:
    def __init__(self, compliance_gap=None):
        self.compliance_gap = compliance_gap


class MockFIN:
    def __init__(self, savings_ratio=None, current_ratio=None):
        self.savings_ratio = savings_ratio
        self.current_ratio = current_ratio


# ---------------------------
# Tests
# ---------------------------

def test_negative_cashflow_generates_recommendation():
    bank = MockBank(net_cash_flow=-50000, expense_ratio=0.9)

    result = generate_recommendations(bank=bank)

    rec_ids = [r["id"] for r in result["recommendations"]]

    assert "CASHFLOW_001" in rec_ids
    assert "COST_001" in rec_ids


def test_gst_compliance_gap_generates_gst_recommendation():
    gst = MockGST(compliance_gap=25000)

    result = generate_recommendations(gst=gst)

    rec_ids = [r["id"] for r in result["recommendations"]]

    assert "GST_001" in rec_ids


def test_financial_weak_liquidity_generates_fin_recommendation():
    fin = MockFIN(savings_ratio=0.05, current_ratio=0.8)

    result = generate_recommendations(fin=fin)

    rec_ids = [r["id"] for r in result["recommendations"]]

    assert "FIN_001" in rec_ids
    assert "FIN_002" in rec_ids


def test_ml_high_risk_generates_credit_recommendation():
    ml_result = {
        "ml_risk_level": "HIGH",
        "confidence": 0.8
    }

    result = generate_recommendations(ml_result=ml_result)

    rec_ids = [r["id"] for r in result["recommendations"]]

    assert "CREDIT_001" in rec_ids


def test_recommendations_are_deduplicated():
    bank = MockBank(net_cash_flow=-10000, expense_ratio=0.95)

    result = generate_recommendations(bank=bank)

    rec_ids = [r["id"] for r in result["recommendations"]]

    assert rec_ids.count("CASHFLOW_001") == 1
    assert rec_ids.count("COST_001") == 1


def test_recommendations_sorted_by_priority():
    bank = MockBank(net_cash_flow=-10000, expense_ratio=0.95)
    fin = MockFIN(savings_ratio=0.05)

    result = generate_recommendations(bank=bank, fin=fin)

    priorities = [r["priority"] for r in result["recommendations"]]

    # HIGH should come before MEDIUM
    assert priorities.index("HIGH") < priorities.index("MEDIUM")


def test_no_inputs_returns_empty_list():
    result = generate_recommendations()

    assert result["recommendations"] == []
