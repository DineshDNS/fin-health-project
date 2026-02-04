import pytest

from products.mapper import map_recommendations_to_products


# ---------------------------
# Fixtures
# ---------------------------

@pytest.fixture
def cashflow_recommendation():
    return {
        "id": "CASHFLOW_001",
        "category": "CASHFLOW_IMPROVEMENT",
        "priority": "HIGH",
        "action": "Improve cash inflows"
    }


@pytest.fixture
def credit_recommendation():
    return {
        "id": "CREDIT_001",
        "category": "CREDIT_READINESS",
        "priority": "MEDIUM",
        "action": "Improve credit readiness"
    }


# ---------------------------
# Tests
# ---------------------------

def test_cashflow_products_returned_for_moderate_risk(cashflow_recommendation):
    products = map_recommendations_to_products(
        recommendations=[cashflow_recommendation],
        risk_level="MODERATE",
        gst_compliant=True,
    )

    product_types = [p["product_type"] for p in products]

    assert "OVERDRAFT" in product_types
    assert "INVOICE_FINANCING" in product_types


def test_high_risk_excludes_low_risk_products(credit_recommendation):
    products = map_recommendations_to_products(
        recommendations=[credit_recommendation],
        risk_level="HIGH",
        gst_compliant=True,
    )

    # TERM_LOAN requires LOW risk → should not appear
    assert products == []


def test_gst_compliance_required_products_excluded_when_non_compliant(cashflow_recommendation):
    products = map_recommendations_to_products(
        recommendations=[cashflow_recommendation],
        risk_level="MODERATE",
        gst_compliant=False,
    )

    # OVERDRAFT requires GST compliance
    product_ids = [p["product_id"] for p in products]

    assert "OD_001" not in product_ids
    assert "INVOICE_001" in product_ids


def test_confidence_score_is_between_0_and_1(cashflow_recommendation):
    products = map_recommendations_to_products(
        recommendations=[cashflow_recommendation],
        risk_level="LOW",
        gst_compliant=True,
    )

    for p in products:
        assert 0.0 <= p["confidence_score"] <= 1.0


def test_products_sorted_by_confidence_descending(cashflow_recommendation):
    products = map_recommendations_to_products(
        recommendations=[cashflow_recommendation],
        risk_level="LOW",
        gst_compliant=True,
    )

    scores = [p["confidence_score"] for p in products]

    assert scores == sorted(scores, reverse=True)


def test_duplicate_products_keep_highest_confidence(cashflow_recommendation):
    # Same recommendation twice → deduplication should occur
    products = map_recommendations_to_products(
        recommendations=[cashflow_recommendation, cashflow_recommendation],
        risk_level="LOW",
        gst_compliant=True,
    )

    product_ids = [p["product_id"] for p in products]

    # Each product appears only once
    assert len(product_ids) == len(set(product_ids))
