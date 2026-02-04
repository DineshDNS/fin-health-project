from rest_framework.views import APIView
from rest_framework.response import Response

from analysis.models import DocumentAnalysis
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
    def get(self, request):

        alerts = []
        insights = []
        score = 100

        # --------------------------------------------------
        # Fetch latest analyses
        # --------------------------------------------------
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

        # --------------------------------------------------
        # Rule-based financial scoring
        # --------------------------------------------------
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

        # --------------------------------------------------
        # ML assessment (never breaks API)
        # --------------------------------------------------
        ml_result = None
        try:
            if bank:
                model = load_model()
                ml_result = predict_creditworthiness(model, bank)
        except Exception:
            ml_result = None

        # --------------------------------------------------
        # Recommendations
        # --------------------------------------------------
        recommendation_payload = generate_recommendations(
            bank=bank,
            gst=gst,
            fin=fin,
            ml_result=ml_result
        )

        recommendations = [
            decorate_recommendation_ui(r)
            for r in recommendation_payload["recommendations"]
        ]

        # --------------------------------------------------
        # Key concerns detection
        # --------------------------------------------------
        key_concerns = detect_key_concerns(
            bank=bank,
            gst=gst,
            fin=fin,
            ml_result=ml_result,
        )

        # --------------------------------------------------
        # Financing decision + product mapping
        # --------------------------------------------------
        gst_compliant = (
            gst is not None and
            gst.compliance_gap is not None and
            gst.compliance_gap <= 0
        )

        offer_financing = should_offer_financing(
            recommendations=recommendation_payload["recommendations"],
            risk_level=risk_level,
        )

        eligible_products = []
        product_state = {
            "status": "NOT_REQUIRED",
            "message": "Your business does not require financing products at this time."
        }

        if offer_financing:
            eligible_products_raw = map_recommendations_to_products(
                recommendations=recommendation_payload["recommendations"],
                risk_level=risk_level,
                gst_compliant=gst_compliant,
            )

            eligible_products = [
                decorate_product_ui(p)
                for p in eligible_products_raw
            ]

            product_state = {
                "status": "AVAILABLE",
                "message": "Suitable financial products identified based on your profile."
            }

        # --------------------------------------------------
        # Action plan (only when recovery is needed)
        # --------------------------------------------------
        action_plan = build_action_plan(key_concerns)

        # --------------------------------------------------
        # UI summary
        # --------------------------------------------------
        ui_summary = risk_ui_summary(score, risk_level)

        # --------------------------------------------------
        # Optional LLM narrative (safe fallback)
        # --------------------------------------------------
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
            narrative = None

        # --------------------------------------------------
        # Final response
        # --------------------------------------------------
        return Response({
            "financial_health_score": score,
            "risk_level": risk_level,
            "ui_summary": ui_summary,
            "risk_alerts": list(set(alerts)),
            "actionable_insights": list(set(insights)),
            "recommendations": recommendations,
            "eligible_products": eligible_products,
            "product_state": product_state,
            "key_concerns": key_concerns,
            "action_plan": action_plan,
            "ml_assessment": ml_result,
            "narrative": narrative,
        })
