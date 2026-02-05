import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny  # TEMP (match overview)

from analysis.models import DocumentAnalysis

from ml.model import load_model
from ml.predictor import predict_creditworthiness

from core.services.analysis_assembler import build_analysis_dto
from core.dto.enums import RiskLevel


class AnalysisView(APIView):
    """
    GET /api/analysis/

    Deep analysis endpoint.
    Backend-first, DTO-only response.
    """

    permission_classes = [AllowAny]  # switch to IsAuthenticated later

    def get(self, request):

        # --------------------------------------------------
        # 1. Fetch latest documents
        # --------------------------------------------------
        bank = DocumentAnalysis.objects.filter(
            document_type="BANK"
        ).order_by("-created_at").first()

        gst = DocumentAnalysis.objects.filter(
            document_type="GST"
        ).order_by("-created_at").first()

        fin = DocumentAnalysis.objects.filter(
            document_type="FIN"
        ).order_by("-created_at").first()

        # --------------------------------------------------
        # 2. Rule-based scoring (same philosophy as overview)
        # --------------------------------------------------
        score = 100

        if bank:
            if bank.net_cash_flow < 0:
                score -= 30
            if bank.expense_ratio and bank.expense_ratio > 0.8:
                score -= 20
            if bank.cashflow_volatile:
                score -= 10

        if gst and gst.compliance_gap and gst.compliance_gap > 0:
            score -= 20

        score = max(score, 0)

        if score >= 70:
            risk_level = RiskLevel.LOW
        elif score >= 40:
            risk_level = RiskLevel.MODERATE
        else:
            risk_level = RiskLevel.HIGH

        # --------------------------------------------------
        # 3. ML assessment (SAFE)
        # --------------------------------------------------
        try:
            if bank:
                model = load_model()
                raw_ml = predict_creditworthiness(model, bank)
                ml_result = {
                    "confidence": float(raw_ml.get("confidence", 0.0)),
                    "key_features": raw_ml.get("key_features", []),
                    "model_version": raw_ml.get("model_version", "v1.0"),
                }
            else:
                raise ValueError("No bank data")
        except Exception:
            ml_result = {
                "confidence": 0.0,
                "key_features": [],
                "model_version": "v1.0",
            }

        # --------------------------------------------------
        # 4. Health breakdown (pillar logic)
        # --------------------------------------------------
        breakdown = {
            "liquidity": {
                "score": 35 if bank and bank.net_cash_flow < 0 else 70,
                "status": "WEAK" if bank and bank.net_cash_flow < 0 else "STABLE",
                "drivers": [
                    "Negative net cash flow"
                ] if bank and bank.net_cash_flow < 0 else [],
            },
            "profitability": {
                "score": 50 if bank and bank.expense_ratio and bank.expense_ratio > 0.7 else 75,
                "status": "MODERATE" if bank and bank.expense_ratio and bank.expense_ratio > 0.7 else "STRONG",
                "drivers": [
                    "High operating expenses"
                ] if bank and bank.expense_ratio and bank.expense_ratio > 0.7 else [],
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

        # --------------------------------------------------
        # 5. Risk factors
        # --------------------------------------------------
        risks = []

        if bank and bank.net_cash_flow < 0:
            risks.append({
                "type": "CASHFLOW_RISK",
                "severity": RiskLevel.HIGH,
                "confidence": 0.92,
                "evidence": [
                    "Sustained negative cash flow detected"
                ],
            })

        if bank and bank.expense_ratio and bank.expense_ratio > 0.8:
            risks.append({
                "type": "COST_STRUCTURE_RISK",
                "severity": RiskLevel.MODERATE,
                "confidence": 0.68,
                "evidence": [
                    "High expense ratio compared to revenue"
                ],
            })

        # --------------------------------------------------
        # 6. Trend signals
        # --------------------------------------------------
        trends = {
            "cashflow": "DECLINING" if bank and bank.net_cash_flow < 0 else "STABLE",
            "revenue": "VOLATILE" if bank and bank.cashflow_volatile else "STABLE",
            "expense": "INCREASING" if bank and bank.expense_ratio and bank.expense_ratio > 0.7 else "STABLE",
        }

        # --------------------------------------------------
        # 7. Impact simulation
        # --------------------------------------------------
        impact_actions = [
            {
                "action": "Reduce operating expenses by 10%",
                "timeframe": "60 days",
                "expected_outcome": "Improves liquidity and cash reserves",
            },
            {
                "action": "Accelerate receivable collection",
                "timeframe": "30 days",
                "expected_outcome": "Stabilizes monthly cash flow",
            },
        ]

        # --------------------------------------------------
        # 8. Build Analysis DTO
        # --------------------------------------------------
        analysis_dto = build_analysis_dto(
            score=score,
            risk_level=risk_level,
            ml_result=ml_result,
            breakdown=breakdown,
            risks=risks,
            trends=trends,
            impact_actions=impact_actions,
        )

        # --------------------------------------------------
        # 9. Response (FROZEN)
        # --------------------------------------------------
        return Response(
            {
                "request_id": str(uuid.uuid4()),
                "status": "SUCCESS",
                "data": analysis_dto.model_dump(),
                "warnings": [],
                "errors": [],
            },
            status=200,
        )
