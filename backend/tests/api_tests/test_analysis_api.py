from rest_framework.test import APITestCase
from django.urls import reverse
import copy


class TestAnalysisAPI(APITestCase):

    def test_analysis_api_snapshot(self):
        url = reverse("analysis")
        response = self.client.get(url)

        assert response.status_code == 200

        actual = response.json()

        # ---- request_id is dynamic, remove before snapshot compare ----
        actual_snapshot = copy.deepcopy(actual)
        actual_snapshot.pop("request_id", None)

        # ---- FROZEN SNAPSHOT (PHASE 14) ----
        expected_snapshot = {
            "status": "SUCCESS",
            "data": {
                "health_breakdown": {
                    "liquidity": {
                        "score": 30,
                        "status": "WEAK",
                        "drivers": ["Low cash buffer"]
                    },
                    "profitability": {
                        "score": 55,
                        "status": "MODERATE",
                        "drivers": ["Stable margins"]
                    },
                    "compliance": {
                        "score": 80,
                        "status": "STRONG",
                        "drivers": ["Timely GST filings"]
                    },
                    "cashflow": {
                        "score": 25,
                        "status": "WEAK",
                        "drivers": ["Irregular inflows"]
                    }
                },
                "risk_factors": [
                    {
                        "type": "CASHFLOW_RISK",
                        "severity": "HIGH",
                        "confidence": 0.92,
                        "evidence": [
                            "Negative operating cash flow",
                            "Receivables aging > 60 days"
                        ]
                    },
                    {
                        "type": "CREDIT_RISK",
                        "severity": "HIGH",
                        "confidence": 0.88,
                        "evidence": [
                            "High credit utilization",
                            "Low repayment buffer"
                        ]
                    }
                ],
                "trend_signals": {
                    "cashflow": "DECLINING",
                    "revenue": "STABLE",
                    "expenses": "RISING"
                },
                "ml_explainability": {
                    "risk_band": "HIGH",
                    "confidence": 0.98,
                    "key_features": [
                        "Transaction volatility",
                        "Compliance consistency",
                        "Credit utilization ratio"
                    ],
                    "model_version": "v2.1"
                },
                "impact_simulation": [
                    {
                        "action": "Reduce expenses by 10%",
                        "timeframe": "30 days",
                        "expected_outcome": {
                            "risk_level": "MEDIUM",
                            "credit_readiness": "MEDIUM"
                        }
                    },
                    {
                        "action": "Improve receivable collection cycle",
                        "timeframe": "60 days",
                        "expected_outcome": {
                            "cashflow_status": "STABLE"
                        }
                    }
                ]
            },
            "warnings": [],
            "errors": []
        }

        # ---- STRICT SNAPSHOT ASSERTION ----
        assert actual_snapshot == expected_snapshot
