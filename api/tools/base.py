from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseTool(ABC):
    """Abstract base class for all tools."""

    @abstractmethod
    async def execute(self, **kwargs) -> Any:
        """Executes the tool's primary capability."""
        pass

    @abstractmethod
    def get_name(self) -> str:
        """Returns the name of the tool."""
        pass

    @abstractmethod
    def get_description(self) -> str:
        """Returns a description of what the tool does."""
        pass
