from .base import LLMClient

class ClaudeLLM(LLMClient):
    def __init__(self, client, system_prompt: str):
        self.client = client
        self.system_prompt = system_prompt

    def generate_narrative(self, *, input_payload: dict) -> dict:
        raise NotImplementedError("Claude integration not enabled yet")
