import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from analysis.models import DocumentAnalysis

from core.services.overview_assembler import build_overview_dto

# ---- EXISTING HELPERS (UNCHANGED) ----
from ml.model import load_model
from ml.predictor import predict_creditworthiness

from recommendations.engine import generate_recommendations
from products.mapper import map_recommendations_to_products

from api.ui_helpers import (
    risk_ui_summary,
    decorate_recommendation_ui,
    decorate_product_ui,
)

from api.decision_helpers import (
    detect_key_concerns,
    should_offer_financing,
    build_action_plan,
)

from llm.factory import get_llm_client, safe_generate_narrative


class OverviewView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        GET /api/overview/
        FROZEN UX CONTRACT
        """

        # --------------------------------------------------
        # 1. Fetch latest analyses (SOURCE DATA)
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

        analysis = {}
        if bank:
            analysis["bank_analysis"] = bank.__dict__
        if gst:
            analysis["gst_analysis"] = gst.__dict__
        if fin:
            analysis["financial_analysis"] = fin.__dict__

        # --------------------------------------------------
        # 2. EXISTING BUSINESS LOGIC (UNCHANGED)
        #    This builds `overview_logic`
        # --------------------------------------------------
        score = 100
        alerts = []
        insights = []

        if bank:
            if bank.net_cash_flow < 0:
                score -= 25
                alerts.append("Negative net cash flow detected")
                insights.append(
                    "Improve cash inflow timing and reduce delayed receivables."
                )

            if bank.expense_ratio and bank.expense_ratio > 0.8:
                score -= 20
                alerts.append("High expense ratio")

            if bank.cashflow_volatile:
                score -= 10
                alerts.append("Cash flow volatility detected")

        if gst and gst.compliance_gap and gst.compliance_gap > 0:
            score -= 20
            alerts.append("GST compliance gap detected")

        score = max(score, 0)

        if score >= 75:
            risk_level = "LOW"
        elif score >= 50:
            risk_level = "MODERATE"
        else:
            risk_level = "HIGH"

        # ---- ML (safe) ----
        ml_result = None
        try:
            if bank:
                model = load_model()
                ml_result = predict_creditworthiness(model, bank)
        except Exception:
            ml_result = {"ml_risk_level": risk_level, "confidence": 0.0}

        # ---- Recommendations ----
        recommendation_payload = generate_recommendations(
            bank=bank,
            gst=gst,
            fin=fin,
            ml_result=ml_result,
        )

        recommendations = [
            decorate_recommendation_ui(r)
            for r in recommendation_payload["recommendations"]
        ]

        # ---- Key concerns ----
        key_concerns = detect_key_concerns(
            bank=bank,
            gst=gst,
            fin=fin,
            ml_result=ml_result,
        )

        # ---- Products ----
        offer_financing = should_offer_financing(
            recommendations=recommendation_payload["recommendations"],
            risk_level=risk_level,
        )

        eligible_products = []
        if offer_financing:
            eligible_products_raw = map_recommendations_to_products(
                recommendations=recommendation_payload["recommendations"],
                risk_level=risk_level,
                gst_compliant=(gst and gst.compliance_gap <= 0),
            )
            eligible_products = [
                decorate_product_ui(p)
                for p in eligible_products_raw
            ]

        # ---- Action plan ----
        action_plan = build_action_plan(key_concerns)

        # ---- Narrative (optional) ----
        narrative = None
        try:
            llm = get_llm_client()
            narrative = safe_generate_narrative(
                llm_client=llm,
                input_payload={
                    "financial_health_score": score,
                    "risk_level": risk_level,
                    "recommendations": recommendations,
                    "key_concerns": key_concerns,
                    "action_plan": action_plan,
                    "products": eligible_products,
                }
            )
        except Exception:
            narrative = {
                "executive_summary": "Your business shows financial risk indicators.",
                "risk_explanation": {
                    "explanation": "Assessment based on financial and ML signals."
                },
                "confidence_note": "AI-generated narrative unavailable."
            }

        # --------------------------------------------------
        # 3. Build overview_logic (DTO INPUT)
        # --------------------------------------------------
        overview_logic = {
            "financial_health_score": score,
            "health_label": "WEAK" if risk_level == "HIGH" else "MODERATE",
            "credit_readiness": "LOW" if risk_level == "HIGH" else "MEDIUM",
            "risk_level": risk_level,
            "key_concerns": key_concerns,
            "recommendations": recommendations,
            "eligible_products": eligible_products,
            "action_plan": action_plan,
            "ml_assessment": ml_result,
            "narrative": narrative,
        }

        # --------------------------------------------------
        # 4. FINAL ASSEMBLY (AUTHORITATIVE)
        # --------------------------------------------------
        dto = build_overview_dto(
            business_id=request.user.id,
            industry="Retail",
            analysis=analysis,
            overview_logic=overview_logic,
        )

        # --------------------------------------------------
        # 5. Response (FROZEN CONTRACT)
        # --------------------------------------------------
        return Response({
            "request_id": str(uuid.uuid4()),
            "status": "SUCCESS",
            "data": dto.model_dump(),
            "warnings": [],
            "errors": [],
        })
