from rest_framework.views import APIView
from rest_framework.response import Response

from analysis.models import DocumentAnalysis
from ml.model import load_model
from ml.predictor import predict_creditworthiness

from recommendations.engine import generate_recommendations

# OPTIONAL LLM (safe abstraction)
from llm.factory import get_llm_client, safe_generate_narrative


class OverviewView(APIView):
    def get(self, request):

        alerts = []
        insights = []
        score = 100

        # -------------------------------
        # Fetch latest analyses
        # -------------------------------
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

        # -------------------------------
        # Rule-based financial score
        # -------------------------------
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

        # -------------------------------
        # ML assessment
        # -------------------------------
        ml_result = None
        try:
            if bank:
                model = load_model()
                ml_result = predict_creditworthiness(model, bank)
        except Exception:
            ml_result = None  # ML must never break API

        # -------------------------------
        # Phase 8: Recommendation Engine
        # -------------------------------
        recommendation_payload = generate_recommendations(
            bank=bank,
            gst=gst,
            fin=fin,
            ml_result=ml_result
        )

        # -------------------------------
        # OPTIONAL: LLM Narrative Layer
        # -------------------------------
        narrative = None
        try:
            llm = get_llm_client()

            llm_input = {
                "business_context": {
                    "business_type": "SME",
                    "industry": "General",
                    "region": "India",
                    "language": "en"
                },
                "financial_summary": {
                    "financial_health_score": score,
                    "risk_level": risk_level
                },
                "bank_signals": {
                    "cashflow_status": (
                        "NEGATIVE" if bank and bank.net_cash_flow < 0 else
                        "BREAKEVEN" if bank and bank.net_cash_flow == 0 else
                        "POSITIVE"
                    ),
                    "expense_level": (
                        "HIGH" if bank and bank.expense_ratio > 0.8 else
                        "MODERATE"
                    ),
                    "volatility": (
                        "UNSTABLE" if bank and bank.cashflow_volatile else
                        "STABLE"
                    )
                },
                "gst_signals": {
                    "compliance_status": (
                        "NON_COMPLIANT" if gst and gst.compliance_gap > 0 else
                        "COMPLIANT"
                    ),
                    "severity": (
                        "HIGH" if gst and gst.compliance_gap > 0 else
                        "LOW"
                    )
                },
                "financial_signals": {
                    "liquidity_status": (
                        "WEAK" if fin and fin.current_ratio and fin.current_ratio < 1
                        else "ADEQUATE"
                    ),
                    "savings_status": (
                        "LOW" if fin and fin.savings_ratio and fin.savings_ratio < 0.1
                        else "GOOD"
                    )
                },
                "ml_assessment": {
                    "risk_level": (
                        ml_result["ml_risk_level"] if ml_result else "MODERATE"
                    ),
                    "confidence_bucket": (
                        "HIGH" if ml_result and ml_result["confidence"] > 0.7 else
                        "MEDIUM" if ml_result and ml_result["confidence"] > 0.4 else
                        "LOW"
                    )
                },
                "recommendations": recommendation_payload["recommendations"]
            }

            narrative = safe_generate_narrative(
                llm_client=llm,
                input_payload=llm_input
            )

        except Exception:
            narrative = None  # LLM must NEVER break API

        # -------------------------------
        # Final response
        # -------------------------------
        return Response({
            "financial_health_score": score,
            "risk_level": risk_level,
            "risk_alerts": list(set(alerts)),
            "actionable_insights": list(set(insights)),
            "recommendations": recommendation_payload["recommendations"],
            "ml_assessment": ml_result,
            "narrative": narrative,  # None if LLM disabled
        })
