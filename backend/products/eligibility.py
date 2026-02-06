import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from analysis.models import DocumentAnalysis
from api.documents.models import Document

from ml.model import load_model
from ml.predictor import predict_creditworthiness

from core.services.analysis_assembler import build_analysis_dto
from core.dto.enums import RiskLevel


class AnalysisView(APIView):
    """
    GET /api/analysis/
    FINAL SAFE VERSION
    """

    permission_classes = [AllowAny]

    def get(self, request):

        # ==================================================
        # STEP 0 — ACTIVE DOCUMENT CHECK
        # ==================================================
        active_docs_exist = Document.objects.filter(status="UPLOADED").exists()

        if not active_docs_exist:
            empty_dto = build_analysis_dto(
                score=0,
                risk_level=RiskLevel.INFO,
                ml_result={
                    "confidence": 0.0,
                    "key_features": [],
                    "model_version": "v1.0",
                },
                breakdown={
                    "liquidity": {"score": 0, "status": "INFO", "drivers": []},
                    "profitability": {"score": 0, "status": "INFO", "drivers": []},
                    "compliance": {"score": 0, "status": "INFO", "drivers": []},
                    "cashflow": {"score": 0, "status": "INFO", "drivers": []},
                },
                risks=[],
                trends={
                    "cashflow": "STABLE",
                    "revenue": "STABLE",
                    "expense": "STABLE",
                },
                impact_actions=[],
            )

            return Response({
                "request_id": str(uuid.uuid4()),
                "status": "SUCCESS",
                "data": empty_dto.model_dump(),
                "warnings": [],
                "errors": [],
            })

        # ==================================================
        # STEP 1 — FETCH LATEST ANALYSIS
        # ==================================================
        bank = DocumentAnalysis.objects.filter(
            document_type="BANK"
        ).order_by("-created_at").first()

        gst = DocumentAnalysis.objects.filter(
            document_type="GST"
        ).order_by("-created_at").first()

        fin = DocumentAnalysis.objects.filter(
            document_type="FIN"
        ).order_by("-created_at").first()

        # ==================================================
        # STEP 2 — SCORE ENGINE
        # ==================================================
        score = 100

        if bank:
            if bank.net_cash_flow and bank.net_cash_flow < 0:
                score -= 30

            if bank.expense_ratio and bank.expense_ratio > 0.8:
                score -= 20

            if bank.cashflow_volatile:
                score -= 10

        if gst and gst.compliance_gap and gst.compliance_gap > 0:
            score -= 20

        if fin and fin.current_ratio and fin.current_ratio < 1:
            score -= 20

        score = max(score, 0)

        if score >= 70:
            risk_level = RiskLevel.LOW
        elif score >= 40:
            risk_level = RiskLevel.MODERATE
        else:
            risk_level = RiskLevel.HIGH

        # ==================================================
        # STEP 3 — ML
        # ==================================================
        ml_confidence = 0.0
        try:
            if bank:
                model = load_model()
                raw = predict_creditworthiness(model, bank)
                ml_confidence = float(raw.get("confidence", 0.0))
        except Exception:
            pass

        # ==================================================
        # STEP 4 — BREAKDOWN
        # ==================================================
        breakdown = {
            "liquidity": {
                "score": 35 if bank and bank.net_cash_flow and bank.net_cash_flow < 0 else 70,
                "status": "WEAK" if bank and bank.net_cash_flow and bank.net_cash_flow < 0 else "STABLE",
                "drivers": ["Negative net cash flow"] if bank and bank.net_cash_flow and bank.net_cash_flow < 0 else [],
            },
            "profitability": {
                "score": 50 if bank and bank.expense_ratio and bank.expense_ratio > 0.7 else 75,
                "status": "MODERATE" if bank and bank.expense_ratio and bank.expense_ratio > 0.7 else "STRONG",
                "drivers": ["High operating expenses"] if bank and bank.expense_ratio and bank.expense_ratio > 0.7 else [],
            },
            "compliance": {
                "score": 80 if gst and gst.compliance_gap == 0 else 50,
                "status": "STRONG" if gst and gst.compliance_gap == 0 else "MODERATE",
                "drivers": [] if gst and gst.compliance_gap == 0 else ["GST compliance gaps"],
            },
            "cashflow": {
                "score": 40 if bank and bank.cashflow_volatile else 70,
                "status": "WEAK" if bank and bank.cashflow_volatile else "STABLE",
                "drivers": ["Cash flow volatility"] if bank and bank.cashflow_volatile else [],
            },
        }

        # ==================================================
        # STEP 5 — SAFE TRENDS (NEVER FAIL)
        # ==================================================
        trends = {
            "cashflow": "DECLINING" if bank and bank.net_cash_flow and bank.net_cash_flow < 0 else "STABLE",
            "revenue": "VOLATILE" if bank and bank.cashflow_volatile else "STABLE",
            "expense": "INCREASING" if bank and bank.expense_ratio and bank.expense_ratio > 0.7 else "STABLE",
        }

        # GUARANTEE keys exist
        trends.setdefault("cashflow", "STABLE")
        trends.setdefault("revenue", "STABLE")
        trends.setdefault("expense", "STABLE")

        # ==================================================
        # STEP 6 — BUILD DTO
        # ==================================================
        analysis_dto = build_analysis_dto(
            score=score,
            risk_level=risk_level,
            ml_result={
                "confidence": ml_confidence,
                "key_features": [],
                "model_version": "v1.0",
            },
            breakdown=breakdown,
            risks=[],
            trends=trends,
            impact_actions=[
                {
                    "action": "Reduce operating expenses by 10%",
                    "timeframe": "60 days",
                    "expected_outcome": "Improves liquidity and cash reserves",
                }
            ],
        )

        return Response({
            "request_id": str(uuid.uuid4()),
            "status": "SUCCESS",
            "data": analysis_dto.model_dump(),
            "warnings": [],
            "errors": [],
        })
