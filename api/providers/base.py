from abc import ABC, abstractmethod
from typing import AsyncGenerator, List, Dict, Any

class BaseLLMProvider(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    async def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Sends a set of messages and returns a complete string response."""
        pass

    @abstractmethod
    async def stream_chat(self, messages: List[Dict[str, str]], **kwargs) -> AsyncGenerator[str, None]:
        """Sends a set of messages and returns an async generator for streaming."""
        yield ""

    @abstractmethod
    def get_name(self) -> str:
        """Returns the name of the provider."""
        pass
