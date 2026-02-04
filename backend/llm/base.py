from abc import ABC, abstractmethod

class LLMClient(ABC):
    """
    Abstract base class for all LLM providers.
    """

    @abstractmethod
    def generate_narrative(self, *, input_payload: dict) -> dict:
        """
        Takes a validated LLM input contract and returns
        a validated LLM output contract.
        """
        pass
