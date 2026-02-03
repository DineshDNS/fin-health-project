from rest_framework.views import APIView
from rest_framework.response import Response

from analysis.models import DocumentAnalysis
from ml.model import load_model
from ml.predictor import predict_creditworthiness


class OverviewView(APIView):
    def get(self, request):
        alerts = []
        insights = []
        score = 100

        # Latest analyses
        bank = (
            DocumentAnalysis.objects
            .filter(document_type="BANK")
            .order_by("-created_at")
            .first()
        )

        gst = (
            DocumentAnalysis.objects
            .filter(document_type="GST")
            .order_by("-created_at")
            .first()
        )

        fin = (
            DocumentAnalysis.objects
            .filter(document_type="FIN")
            .order_by("-created_at")
            .first()
        )

        # ---------------- RULE ENGINE ----------------
        if bank:
            if bank.net_cash_flow < 0:
                score -= 25
                alerts.append("Negative net cash flow detected")
                insights.append(
                    "Improve cash inflow timing and reduce delayed receivables."
                )

            if bank.expense_ratio > 0.8:
                score -= 20
                alerts.append("High expense ratio")

            if bank.cashflow_volatile:
                score -= 10
                alerts.append("Cash flow volatility detected")

        if gst and gst.compliance_gap > 0:
            score -= 20
            alerts.append("GST compliance gap detected")
            insights.append(
                "Set aside GST collections separately to avoid compliance gaps."
            )

        if fin:
            score -= 5

        score = max(score, 0)

        if score >= 75:
            risk_level = "LOW"
        elif score >= 50:
            risk_level = "MODERATE"
        else:
            risk_level = "HIGH"

        # ---------------- ML PREDICTION ----------------
        ml_prediction = None
        try:
            model = load_model()
            if bank:
                ml_prediction = predict_creditworthiness(model, bank)
        except Exception:
            ml_prediction = None  # ML must NEVER break API

        return Response({
            "financial_health_score": score,
            "risk_level": risk_level,
            "risk_alerts": list(set(alerts)),
            "actionable_insights": list(set(insights)),
            "product_recommendations": [],
            "ml_prediction": ml_prediction
        })
