import pytest
from unittest.mock import patch

from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status


# -------------------------------------------------
# Fixtures
# -------------------------------------------------

@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="testuser",
        password="testpass123",
    )


@pytest.fixture
def auth_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


# -------------------------------------------------
# API Integration Test
# -------------------------------------------------

@pytest.mark.django_db
@patch("api.overview_view.safe_generate_narrative")
@patch("api.overview_view.map_recommendations_to_products")
@patch("api.overview_view.generate_recommendations")
@patch("api.overview_view.predict_creditworthiness")
@patch("api.overview_view.load_model")
def test_overview_api_success(
    mock_load_model,
    mock_predict,
    mock_generate_recs,
    mock_map_products,
    mock_safe_narrative,
    auth_client,
):
    """
    GIVEN authenticated user
    WHEN /api/overview/ is called
    THEN a valid OverviewDTO response is returned
    """

    # -------------------------------------------------
    # Mock ML layer
    # -------------------------------------------------
    mock_load_model.return_value = object()
    mock_predict.return_value = {
        "ml_risk_level": "HIGH",
        "confidence": 0.12,
    }

    # -------------------------------------------------
    # Mock recommendation engine
    # -------------------------------------------------
    mock_generate_recs.return_value = {
        "recommendations": []
    }

    mock_map_products.return_value = []

    # -------------------------------------------------
    # Mock LLM narrative
    # -------------------------------------------------
    mock_safe_narrative.return_value = {
        "executive_summary": "High financial risk detected",
        "risk_explanation": {
            "explanation": "Mocked explanation for testing"
        },
        "confidence_note": "AI-assisted summary",
    }

    # -------------------------------------------------
    # Call API
    # -------------------------------------------------
    response = auth_client.get("/api/overview/")

    # -------------------------------------------------
    # Assertions
    # -------------------------------------------------
    assert response.status_code == status.HTTP_200_OK

    payload = response.json()

    # ---- Top-level envelope ----
    assert "request_id" in payload
    assert payload["status"] == "SUCCESS"
    assert "data" in payload
    assert payload["errors"] == []
    assert payload["warnings"] == []

    data = payload["data"]

    # ---- Core DTO presence ----
    assert "business_context" in data
    assert "health_summary" in data
    assert "risk_summary" in data
    assert "recommendations" in data
    assert "products" in data
    assert "action_plan" in data
    assert "ml_summary" in data
    assert "narrative" in data

    # ---- Critical field checks ----
    assert data["ml_summary"]["confidence"] == 0.0
    assert data["ml_summary"]["risk_band"] == data["risk_summary"]["overall_risk_level"]
