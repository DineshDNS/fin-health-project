from rest_framework.views import APIView
from rest_framework.response import Response

from aggregation.services import get_cumulative_state


class OverviewView(APIView):
    def get(self, request):
        state = get_cumulative_state()

        risk_level = "LOW"
        alerts = []

        if state.cashflow_volatile:
            risk_level = "MODERATE"
            alerts.append("High expense ratio indicates cash flow volatility")

        if state.compliance_gap > 0:
            risk_level = "HIGH"
            alerts.append("GST compliance gap detected")

        return Response({
            "financial_health_score": state.financial_health_score,
            "risk_level": risk_level,
            "risk_alerts": alerts,
            "actionable_insights": [
                "Reduce operating expenses to improve cash stability"
            ] if alerts else [],
            "product_recommendations": [],
        })
