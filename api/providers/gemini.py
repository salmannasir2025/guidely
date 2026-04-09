import google.generativeai as genai
import logging
from typing import List, Dict, Any, AsyncGenerator
from .base import BaseLLMProvider
from ..config import settings

class GeminiProvider(BaseLLMProvider):
    """Google Gemini LLM provider implementation."""

    def __init__(self, model_name: str = "gemini-pro"):
        self.model_name = model_name
        self._model = genai.GenerativeModel(model_name)
        genai.configure(api_key=settings.gemini_api_key)

    async def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Sends messages to Gemini (converts messages to Gemini format)."""
        # For simple queries, we use generate_content
        # Note: In a full implementation, we'd map 'system', 'user', 'assistant' 
        # to Gemini's 'role' and 'parts'.
        try:
            # Flattening messages into a single prompt for speed and simplicity 
            # following the Nanobot pattern, or using Gemini's chat history.
            prompt = self._format_messages(messages)
            response = self._model.generate_content(prompt)
            return response.text
        except Exception as e:
            logging.error(f"GeminiProvider Chat Error: {e}")
            raise Exception(f"Gemini error: {str(e)}")

    async def stream_chat(self, messages: List[Dict[str, str]], **kwargs) -> AsyncGenerator[str, None]:
        """Streams responses from Gemini."""
        try:
            prompt = self._format_messages(messages)
            response = self._model.generate_content(prompt, stream=True)
            for chunk in response:
                if chunk.text:
                    yield chunk.text
        except Exception as e:
            logging.error(f"GeminiProvider Stream Error: {e}")
            raise Exception(f"Gemini stream error: {str(e)}")

    def get_name(self) -> str:
        return "gemini"

    def _format_messages(self, messages: List[Dict[str, str]]) -> str:
        """Simple formatter to convert message list to a single prompt string."""
        formatted = ""
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            formatted += f"\n{role.capitalize()}: {content}"
        return formatted.strip()
