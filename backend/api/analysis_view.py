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
    permission_classes = [AllowAny]

    def get(self, request):

        # ==================================================
        # 0️⃣ ACTIVE DOCUMENTS
        # ==================================================
        active_docs = Document.objects.filter(status="UPLOADED")

        if not active_docs.exists():
            empty_dto = build_analysis_dto(
                score=0,
                risk_level=RiskLevel.INFO,
                ml_result={"confidence": 0.0, "key_features": [], "model_version": "v1.0"},
                breakdown={},
                risks=[],
                trends={},
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
        # 1️⃣ FETCH LATEST ANALYSIS PER TYPE
        # ==================================================
        bank = DocumentAnalysis.objects.filter(document_type="BANK").order_by("-created_at").first()
        gst = DocumentAnalysis.objects.filter(document_type="GST").order_by("-created_at").first()
        fin = DocumentAnalysis.objects.filter(document_type="FIN").order_by("-created_at").first()

        # ==================================================
        # 2️⃣ DATA AVAILABILITY SCORE (20)
        # ==================================================
        availability_score = 0
        if bank: availability_score += 7
        if gst: availability_score += 7
        if fin: availability_score += 6

        # ==================================================
        # 3️⃣ FINANCIAL STRENGTH SCORE (40)
        # ==================================================
        financial_score = 0

        if bank:
            if bank.net_cash_flow and bank.net_cash_flow > 0:
                financial_score += 15
            if bank.expense_ratio and bank.expense_ratio < 0.7:
                financial_score += 10
            if not bank.cashflow_volatile:
                financial_score += 5

        if fin:
            if fin.current_ratio and fin.current_ratio > 1.5:
                financial_score += 5
            if fin.total_assets and fin.total_liabilities and fin.total_assets > fin.total_liabilities:
                financial_score += 5
            if fin.savings_ratio and fin.savings_ratio > 0.2:
                financial_score += 5

        # ==================================================
        # 4️⃣ COMPLIANCE SCORE (20)
        # ==================================================
        compliance_score = 0
        if gst:
            if gst.compliance_gap == 0:
                compliance_score = 20
            elif gst.compliance_gap < 50000:
                compliance_score = 10

        # ==================================================
        # 5️⃣ ML SCORE (20)
        # ==================================================
        ml_score = 0
        ml_confidence = 0.0
        ml_risk = "LOW"

        try:
            if bank:
                model = load_model()
                raw = predict_creditworthiness(model, bank)
                ml_confidence = float(raw.get("confidence", 0))
                ml_risk = raw.get("ml_risk_level", "LOW")

                if ml_risk == "LOW":
                    ml_score = 20
                elif ml_risk == "MODERATE":
                    ml_score = 12
                else:
                    ml_score = 5

                ml_score *= ml_confidence
        except:
            pass

        # ==================================================
        # 6️⃣ FINAL SCORE
        # ==================================================
        score = int(availability_score + financial_score + compliance_score + ml_score)
        score = max(0, min(100, score))

        if score >= 75:
            risk_level = RiskLevel.LOW
        elif score >= 45:
            risk_level = RiskLevel.MODERATE
        else:
            risk_level = RiskLevel.HIGH

        # ==================================================
        # 7️⃣ BREAKDOWN
        # ==================================================
        breakdown = {
            "liquidity": {"score": 70 if bank else 40, "status": "STABLE", "drivers": []},
            "profitability": {"score": 75 if fin else 45, "status": "STRONG", "drivers": []},
            "compliance": {"score": 80 if gst else 30, "status": "STRONG", "drivers": []},
            "cashflow": {"score": 70 if bank else 40, "status": "STABLE", "drivers": []},
        }

        # ==================================================
        # 8️⃣ BUILD DTO
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
            trends={},
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
            "data": analysis_dto,
            "warnings": [],
            "errors": [],
        })
