from rest_framework.views import APIView
from rest_framework.response import Response

from analysis.models import DocumentAnalysis
from ml.model import load_model
from ml.predictor import predict_creditworthiness


class AnalysisView(APIView):
    def get(self, request):
        # ---------------- FETCH LATEST ANALYSES ----------------
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

        # ---------------- ML PREDICTION (BANK + GST + FIN) ----------------
        ml_prediction = None
        try:
            model = load_model()
            if model:
                ml_prediction = predict_creditworthiness(
                    model,
                    bank=bank,
                    gst=gst,
                    fin=fin
                )
        except Exception:
            ml_prediction = None

        # ---------------- RESPONSE ----------------
        return Response({
            "bank_analysis": (
                {
                    "total_credits": bank.total_credits,
                    "total_debits": bank.total_debits,
                    "net_cash_flow": bank.net_cash_flow,
                    "expense_ratio": bank.expense_ratio,
                    "cashflow_volatile": bank.cashflow_volatile,
                }
                if bank else None
            ),

            "gst_analysis": (
                {
                    "taxable_value": gst.taxable_value,
                    "gst_paid": gst.gst_paid,
                    "expected_gst": gst.expected_gst,
                    "compliance_gap": gst.compliance_gap,
                    "is_compliant": gst.is_compliant,
                }
                if gst else None
            ),

            # 🔒 SAFE FIN HANDLING (NO ASSUMPTIONS)
            "financial_analysis": (
                {
                    "financial_health_score": getattr(fin, "financial_health_score", None),
                    "risk_level": getattr(fin, "risk_level", None),

                    # Optional future fields (won't crash if missing)
                    "total_assets": getattr(fin, "total_assets", None),
                    "total_liabilities": getattr(fin, "total_liabilities", None),
                    "savings_ratio": getattr(fin, "savings_ratio", None),
                    "current_ratio": getattr(fin, "current_ratio", None),
                }
                if fin else None
            ),

            "ml_prediction": ml_prediction,
        })
