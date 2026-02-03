from rest_framework.views import APIView
from rest_framework.response import Response

from analysis.models import DocumentAnalysis
from ml.model import load_model
from ml.predictor import predict_creditworthiness


class AnalysisView(APIView):
    def get(self, request):
        latest_bank = (
            DocumentAnalysis.objects
            .filter(document_type="BANK")
            .order_by("-created_at")
            .first()
        )

        latest_gst = (
            DocumentAnalysis.objects
            .filter(document_type="GST")
            .order_by("-created_at")
            .first()
        )

        latest_fin = (
            DocumentAnalysis.objects
            .filter(document_type="FIN")
            .order_by("-created_at")
            .first()
        )

        # ML prediction (advisory)
        ml_prediction = None
        try:
            if latest_bank:
                model = load_model()
                ml_prediction = predict_creditworthiness(model, latest_bank)
        except Exception:
            ml_prediction = None  # ML must never break API

        return Response({
            "bank_analysis": (
                {
                    "total_credits": latest_bank.total_credits,
                    "total_debits": latest_bank.total_debits,
                    "net_cash_flow": latest_bank.net_cash_flow,
                    "expense_ratio": latest_bank.expense_ratio,
                    "cashflow_volatile": latest_bank.cashflow_volatile,
                }
                if latest_bank else None
            ),

            "gst_analysis": (
                {
                    "taxable_value": latest_gst.taxable_value,
                    "gst_paid": latest_gst.gst_paid,
                    "expected_gst": latest_gst.expected_gst,
                    "compliance_gap": latest_gst.compliance_gap,
                    "is_compliant": latest_gst.is_compliant,
                }
                if latest_gst else None
            ),

            "financial_summary": {
                "financial_health_score": (
                    latest_fin.financial_health_score
                    if latest_fin else
                    (latest_bank.financial_health_score if latest_bank else None)
                ),
                "risk_level": (
                    latest_fin.risk_level
                    if latest_fin else
                    (latest_bank.risk_level if latest_bank else None)
                ),
            },

            "ml_prediction": ml_prediction,
        })
