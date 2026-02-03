from rest_framework.views import APIView
from rest_framework.response import Response

from aggregation.services import get_cumulative_state


class AnalysisView(APIView):
    def get(self, request):
        state = get_cumulative_state()

        return Response({
            "bank_analysis": {
                "total_credits": state.total_credits,
                "total_debits": state.total_debits,
                "net_cash_flow": state.net_cash_flow,
                "closing_balance": state.closing_balance,
                "expense_ratio": state.expense_ratio,
                "savings_ratio": state.savings_ratio,
                "cashflow_volatile": state.cashflow_volatile,
            },
            "gst_analysis": {
                "taxable_value": state.taxable_value,
                "gst_paid": state.gst_paid,
                "expected_gst": state.expected_gst,
                "payment_ratio": state.payment_ratio,
                "compliance_gap": state.compliance_gap,
                "is_compliant": state.is_compliant,
            },
            "financial_health_score": state.financial_health_score,
            "risk_analysis": {
                "priority_issues": [],
                "warnings": [],
            },
        })
