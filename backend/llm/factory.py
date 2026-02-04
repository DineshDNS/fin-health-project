from django.conf import settings
from jsonschema import ValidationError

from llm.mock import MockLLM
from llm.gpt5 import GPT5LLM
from llm.claude import ClaudeLLM


def get_llm_client():
    """
    Factory method to return the appropriate LLM client
    based on environment configuration.

    - development → MockLLM (free, deterministic)
    - staging     → Claude (optional)
    - production  → GPT-5
    """

    env = getattr(settings, "ENVIRONMENT", "development").lower()

    if env == "production":
        return GPT5LLM(
            client=None,  # OpenAI client injected later
            system_prompt=_load_system_prompt()
        )

    if env == "staging":
        return ClaudeLLM(
            client=None,  # Anthropic client injected later
            system_prompt=_load_system_prompt()
        )

    # Default: development / testing
    return MockLLM()


def safe_generate_narrative(llm_client, input_payload: dict) -> dict:
    """
    Safely generate LLM narrative.

    - Enforces schema validation (via base class)
    - Never allows API crashes
    - Returns a compliant fallback response on failure
    """

    try:
        return llm_client.generate_narrative(
            input_payload=input_payload
        )

    except ValidationError:
        # Schema violation — fallback safely
        return _fallback_response(input_payload)

    except Exception:
        # Any unexpected LLM/provider failure
        return _fallback_response(input_payload)


def _fallback_response(input_payload: dict) -> dict:
    """
    Guaranteed-safe fallback response.
    Always schema-compliant.
    """

    risk_level = input_payload.get("financial_summary", {}).get(
        "risk_level", "MODERATE"
    )

    return {
        "executive_summary": (
            "We are unable to generate detailed insights at the moment."
        ),
        "risk_explanation": {
            "overall_risk": risk_level,
            "explanation": (
                "Please review the financial indicators and recommendations provided."
            )
        },
        "key_concerns": [],
        "action_plan": [],
        "confidence_note": (
            "This is a temporary fallback response."
        )
    }


def _load_system_prompt() -> str:
    """
    Load system prompt from file.
    Kept isolated for auditability.
    """
    with open("llm/prompts/system.txt", "r", encoding="utf-8") as f:
        return f.read()
