from .base import LLMClient

class GPT5LLM(LLMClient):
    def __init__(self, client):
        self.client = client  # OpenAI SDK client

    def generate_narrative(self, *, input_payload: dict) -> dict:
        # 1. Serialize input_payload into prompt
        # 2. Call GPT-5
        # 3. Parse JSON output
        # 4. Validate schema
        # 5. Return dict
        pass
