import os

try:
    from jsonschema import validate, ValidationError
except ImportError:
    # Safe fallback if jsonschema is not installed
    ValidationError = Exception
    validate = None


# --------------------------------------------------
# Narrative output schema (frontend + audit safe)
# --------------------------------------------------
NARRATIVE_SCHEMA = {
    "type": "object",
    "properties": {
        "executive_summary": {"type": "string"},
        "risk_explanation": {
            "type": "object",
            "properties": {
                "overall_risk": {"type": "string"},
                "explanation": {"type": "string"},
            },
            "required": ["overall_risk", "explanation"],
        },
        "key_concerns": {"type": "array"},
        "action_plan": {"type": "array"},
        "confidence_note": {"type": "string"},
    },
    "required": [
        "executive_summary",
        "risk_explanation",
        "key_concerns",
        "action_plan",
        "confidence_note",
    ],
}


# --------------------------------------------------
# LLM client abstraction
# --------------------------------------------------
class BaseLLMClient:
    def generate(self, prompt: str) -> dict:
        raise NotImplementedError


class MockLLMClient(BaseLLMClient):
    """
    Used when no paid LLM is configured.
    Always triggers fallback narrative.
    """

    def generate(self, prompt: str) -> dict:
        raise RuntimeError("LLM not configured")


def get_llm_client():
    """
    Factory method.
    Replace this later with GPT-5 / Claude client.
    """

    # Example:
    # if os.getenv("OPENAI_API_KEY"):
    #     return OpenAILLMClient()

    return MockLLMClient()


# --------------------------------------------------
# Fallback narrative (CRITICAL FIX)
# --------------------------------------------------
def fallback_narrative(input_payload: dict) -> dict:
    risk_level = input_payload.get("risk_level", "MODERATE")

    return {
        "executive_summary": (
            "Your business is financially stable with no critical risks detected."
            if risk_level == "LOW"
            else "Your business shows financial risk indicators that require attention."
        ),
        "risk_explanation": {
            "overall_risk": risk_level,
            "explanation": (
                "The assessment is based on financial health score, cash flow stability, "
                "compliance indicators, and ML-based credit evaluation."
            ),
        },
        "key_concerns": input_payload.get("key_concerns", []),
        "action_plan": input_payload.get("action_plan", []),
        "confidence_note": "AI-generated narrative is temporarily unavailable.",
    }


# --------------------------------------------------
# Safe narrative generation wrapper
# --------------------------------------------------
def safe_generate_narrative(llm_client: BaseLLMClient, input_payload: dict) -> dict:
    """
    Attempts LLM generation.
    Falls back deterministically on ANY failure.
    """

    try:
        prompt = (
            "Generate a clear, professional financial narrative based on:\n"
            f"{input_payload}\n"
            "Return structured JSON only."
        )

        output = llm_client.generate(prompt)

        # Validate schema if jsonschema is available
        if validate:
            validate(instance=output, schema=NARRATIVE_SCHEMA)

        return output

    except Exception:
        # NEVER let narrative break API
        return fallback_narrative(input_payload)
