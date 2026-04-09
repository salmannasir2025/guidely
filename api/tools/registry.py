import logging
from typing import Dict, Optional, List
from .base import BaseTool

class ToolRegistry:
    """A centralized registry for application tools."""

    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}

    def register(self, tool: BaseTool):
        """Registers a tool with the registry."""
        self._tools[tool.get_name()] = tool
        logging.info(f"Tool registered: {tool.get_name()}")

    def get_tool(self, name: str) -> Optional[BaseTool]:
        """Retrieves a tool by name."""
        return self._tools.get(name)

    def list_tools(self) -> List[str]:
        """Lists todas available tools."""
        return list(self._tools.keys())

# Singleton instance for the app
tool_registry = ToolRegistry()

# Register tools
from .math_solver import MathSolverTool
from .search import WebSearchTool
from .ocr import OCRTool
from .speech import SpeechToTextTool, TextToSpeechTool

tool_registry.register(MathSolverTool())
tool_registry.register(WebSearchTool())
tool_registry.register(OCRTool())
tool_registry.register(SpeechToTextTool())
tool_registry.register(TextToSpeechTool())
