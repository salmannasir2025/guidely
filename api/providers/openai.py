import httpx
import logging
from typing import List, Dict, Any, AsyncGenerator
from .base import BaseLLMProvider

class OpenAIProvider(BaseLLMProvider):
    """OpenAI LLM provider implementation using httpx for direct API access."""

    def __init__(self, model_name: str = "gpt-4-turbo", api_key: str = None):
        self.model_name = model_name
        self.api_key = api_key
        self.base_url = "https://api.openai.com/v1/chat/completions"

    async def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Sends messages to OpenAI Chat Completions API."""
        if not self.api_key:
            raise ValueError("OpenAI API key is required")

        payload = {
            "model": self.model_name,
            "messages": messages,
            **kwargs
        }
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(self.base_url, json=payload, headers=headers, timeout=60.0)
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]
        except Exception as e:
            logging.error(f"OpenAIProvider Chat Error: {e}")
            raise Exception(f"OpenAI error: {str(e)}")

    async def stream_chat(self, messages: List[Dict[str, str]], **kwargs) -> AsyncGenerator[str, None]:
        """Streams responses from OpenAI."""
        if not self.api_key:
            raise ValueError("OpenAI API key is required")

        payload = {
            "model": self.model_name,
            "messages": messages,
            "stream": True,
            **kwargs
        }
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        try:
            async with httpx.AsyncClient() as client:
                async with client.stream("POST", self.base_url, json=payload, headers=headers, timeout=60.0) as response:
                    response.raise_for_status()
                    async for line in response.aiter_lines():
                        if line.startswith("data: "):
                            if line == "data: [DONE]":
                                break
                            import json
                            try:
                                chunk = json.loads(line[6:])
                                content = chunk["choices"][0].get("delta", {}).get("content")
                                if content:
                                    yield content
                            except Exception:
                                continue
        except Exception as e:
            logging.error(f"OpenAIProvider Stream Error: {e}")
            raise Exception(f"OpenAI stream error: {str(e)}")

    def get_name(self) -> str:
        return "openai"
