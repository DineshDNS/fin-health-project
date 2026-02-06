import uuid

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from analysis.models import DocumentAnalysis
from core.services.overview_assembler import build_overview_dto

# ---- ML & ENGINES ----
from ml.model import load_model
from ml.predictor import predict_creditworthiness

from recommendations.engine import generate_recommendations
from products.mapper import map_recommendations_to_products

from api.ui_helpers import (
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

    permission_classes = [AllowAny]

    def get(self, request):

        # --------------------------------------------------
        # 1. Fetch latest analyses
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
        # 2. NEW SCORING MODEL (DATA + RISK BASED)
        # --------------------------------------------------
        score = 100

        # ⭐ DATA AVAILABILITY PENALTY
        if not bank:
            score -= 30
        if not gst:
            score -= 20
        if not fin:
            score -= 15

        # ⭐ RISK PENALTIES (only if data exists)
        if bank:
            if bank.net_cash_flow < 0:
                score -= 25
            if bank.expense_ratio and bank.expense_ratio > 0.8:
                score -= 20
            if bank.cashflow_volatile:
                score -= 10

        if gst and gst.compliance_gap and gst.compliance_gap > 0:
            score -= 20

        score = max(score, 0)

        if score >= 75:
            risk_level = "LOW"
        elif score >= 50:
            risk_level = "MODERATE"
        else:
            risk_level = "HIGH"

        # --------------------------------------------------
        # 3. ML Assessment
        # --------------------------------------------------
        try:
            if bank:
                model = load_model()
                raw_ml = predict_creditworthiness(model, bank)
                ml_result = {
                    "ml_risk_level": raw_ml.get("ml_risk_level", risk_level),
                    "confidence": float(raw_ml.get("confidence", 0.0)),
                }
            else:
                raise ValueError("No bank data")
        except Exception:
            ml_result = {
                "ml_risk_level": risk_level,
                "confidence": 0.0,
            }

        # --------------------------------------------------
        # 4–9. (UNCHANGED BELOW)
        # --------------------------------------------------
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

        key_concerns = detect_key_concerns(
            bank=bank,
            gst=gst,
            fin=fin,
            ml_result=ml_result,
        )

        offer_financing = should_offer_financing(
            recommendations=recommendation_payload["recommendations"],
            risk_level=risk_level,
        )

        eligible_products = []
        if offer_financing:
            raw_products = map_recommendations_to_products(
                recommendations=recommendation_payload["recommendations"],
                risk_level=risk_level,
                gst_compliant=bool(gst and gst.compliance_gap <= 0),
            )
            eligible_products = [
                decorate_product_ui(p)
                for p in raw_products
            ]

        action_plan = build_action_plan(key_concerns)

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

        dto = build_overview_dto(
            business_id=request.user.id if request.user and request.user.id else 0,
            industry="Retail",
            analysis=analysis,
            overview_logic=overview_logic,
        )

        response = dto.model_dump()
        response["request_id"] = str(uuid.uuid4())

        return Response(response)
