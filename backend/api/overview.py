from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ingestion.models import IngestedDocument
from features.feature_store import build_feature_store

from intelligence.health_score import calculate_financial_health_score
from intelligence.risk_engine import assess_risk
from intelligence.insights_engine import generate_actionable_insights
from intelligence.product_engine import recommend_products
from intelligence.defaults import BANK_DEFAULT, GST_DEFAULT


class OverviewAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # ---- Fetch latest BANK & GST documents ----
        bank_doc = (
            IngestedDocument.objects
            .filter(user=user, detected_type="BANK")
            .order_by("-uploaded_at")
            .first()
        )

        gst_doc = (
            IngestedDocument.objects
            .filter(user=user, detected_type="GST")
            .order_by("-uploaded_at")
            .first()
        )

        # ---- BANK FEATURES (with defaults) ----
        if bank_doc and bank_doc.parsed_data:
            bank_features = build_feature_store(
                bank_doc.parsed_data,
                "BANK"
            ).get("bank_features")
        else:
            bank_features = BANK_DEFAULT.copy()

        # ---- GST FEATURES (with defaults) ----
        if gst_doc and gst_doc.parsed_data:
            gst_features = build_feature_store(
                gst_doc.parsed_data,
                "GST"
            ).get("gst_features")
        else:
            gst_features = GST_DEFAULT.copy()

        # ---- Health score ----
        health_score = calculate_financial_health_score(
            bank_features,
            gst_features
        )

        # ---- Risk level ----
        if health_score >= 75:
            risk_level = "LOW"
        elif health_score >= 50:
            risk_level = "MODERATE"
        else:
            risk_level = "HIGH"

        # ---- Risk alerts ----
        risk_data = assess_risk(bank_features)

        # ---- Insights ----
        insights = generate_actionable_insights(
            bank_features,
            gst_features
        )

        # ---- Product recommendations ----
        products = recommend_products(
            bank_features,
            risk_level
        )

        return Response({
            "financial_health_score": health_score,
            "risk_level": risk_level,
            "risk_alerts": (
                risk_data.get("priority_issues", [])
                + risk_data.get("warnings", [])
            ),
            "actionable_insights": insights,
            "product_recommendations": products,
        })
