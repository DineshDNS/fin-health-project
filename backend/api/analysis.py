from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ingestion.models import IngestedDocument
from features.feature_store import build_feature_store
from intelligence.health_score import calculate_financial_health_score
from intelligence.risk_engine import assess_risk


class AnalysisAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

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

        bank_features = None
        gst_features = None

        if bank_doc:
            bank_features = build_feature_store(
                bank_doc.parsed_data,
                "BANK"
            ).get("bank_features")

        if gst_doc:
            gst_features = build_feature_store(
                gst_doc.parsed_data,
                "GST"
            ).get("gst_features")

        health_score = calculate_financial_health_score(
            bank_features,
            gst_features
        )

        risk = assess_risk(bank_features)

        return Response({
            "bank_analysis": bank_features,
            "gst_analysis": gst_features,
            "financial_health_score": health_score,
            "risk_analysis": risk,
        })
