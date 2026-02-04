from .base import LLMClient

class MockLLM(LLMClient):
    """
    Deterministic mock LLM for development and testing.
    """

    def generate_narrative(self, *, input_payload: dict) -> dict:
        risk = input_payload["financial_summary"]["risk_level"]

        if risk == "HIGH":
            summary = "Your business is under financial stress and needs immediate attention."
        elif risk == "MODERATE":
            summary = "Your business shows some financial risks that should be addressed soon."
        else:
            summary = "Your business is financially stable at the moment."

        return {
            "executive_summary": summary,
            "risk_explanation": {
                "overall_risk": risk,
                "explanation": "This assessment is based on cash flow, compliance, and financial stability signals."
            },
            "key_concerns": [],
            "action_plan": [],
            "confidence_note": "This guidance is generated for informational purposes."
        }
