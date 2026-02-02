from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ingestion.models import IngestedDocument
from features.feature_store import build_feature_store
from intelligence.health_score import calculate_financial_health_score
from intelligence.risk_engine import assess_risk
from intelligence.defaults import BANK_DEFAULT, GST_DEFAULT


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

        # ---------------- BANK ----------------
        if bank_doc and bank_doc.parsed_data:
            bank_features = build_feature_store(
                bank_doc.parsed_data,
                "BANK"
            ).get("bank_features")
        else:
            bank_features = BANK_DEFAULT.copy()

        # ---------------- GST ----------------
        if gst_doc and gst_doc.parsed_data:
            gst_features = build_feature_store(
                gst_doc.parsed_data,
                "GST"
            ).get("gst_features")
        else:
            gst_features = GST_DEFAULT.copy()

        # ---------------- HEALTH SCORE ----------------
        health_score = calculate_financial_health_score(
            bank_features,
            gst_features
        )

        # ---------------- RISK ----------------
        risk = assess_risk(bank_features)

        return Response({
            "bank_analysis": bank_features,
            "gst_analysis": gst_features,
            "financial_health_score": health_score,
            "risk_analysis": risk,
        })
