from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .services.health_score import profitability_score
from .services.risk_engine import cash_flow_risk
from .services.insights_engine import generate_actionable_insights
from .services.product_engine import recommend_products
from .services.llm_recommender import generate_llm_product_recommendations


class OverviewView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        total_revenue = 1_200_000
        total_expenses = 950_000

        net_cash_flow = -150_000
        cash_flow_volatile = True

        q1 = profitability_score(
            total_revenue=total_revenue,
            total_expenses=total_expenses,
        )

        q2_risk = cash_flow_risk(
            net_cash_flow=net_cash_flow,
            is_volatile=cash_flow_volatile,
        )

        risk_flags = {
            "priority_issues": [],
            "warnings": [],
        }

        if q1["risk"] == "HIGH":
            risk_flags["priority_issues"].append(
                "Business is operating at a loss"
            )

        if q1["risk"] == "MEDIUM":
            risk_flags["warnings"].append(
                "Profit margins are thin"
            )

        risk_flags["priority_issues"].extend(
            q2_risk["priority_issues"]
        )
        risk_flags["warnings"].extend(
            q2_risk["warnings"]
        )

        actionable_insights = generate_actionable_insights(
            profitability_risk=q1["risk"],
            net_cash_flow=net_cash_flow,
            cash_flow_volatile=cash_flow_volatile,
        )

        rule_products = recommend_products(
            profitability_risk=q1["risk"],
            net_cash_flow=net_cash_flow,
            cash_flow_volatile=cash_flow_volatile,
        )

        llm_payload = {
            "business_profile": {
                "type": "SME",
                "country": "India",
            },
            "financial_summary": {
                "profitability_risk": q1["risk"],
                "net_cash_flow": net_cash_flow,
                "cash_flow_volatile": cash_flow_volatile,
            },
            "identified_risks": risk_flags,
        }

        product_recommendations = generate_llm_product_recommendations(
            payload=llm_payload,
            rule_products=rule_products,
        )

        risk_level_map = {
            "LOW": "Low",
            "MEDIUM": "Medium",
            "HIGH": "High",
        }

        return Response({
            "health_score": q1["score"],
            "risk_level": risk_level_map[q1["risk"]],
            "risk_flags": risk_flags,
            "actionable_insights": actionable_insights,
            "product_recommendations": product_recommendations,
        })
