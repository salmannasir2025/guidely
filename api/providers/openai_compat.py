"""
OpenAI-Compatible Provider Base
================================
A reusable base class for any LLM provider that exposes an OpenAI-compatible
`/v1/chat/completions` API endpoint. New providers (Minimax, Grok, Qwen, etc.)
simply subclass this and override `base_url`, `default_model`, and `_name`.
"""

import httpx
import json
import logging
from typing import List, Dict, Optional, AsyncGenerator
from .base import BaseLLMProvider


class OpenAICompatProvider(BaseLLMProvider):
    """
    Generic provider for any service that speaks the OpenAI chat/completions dialect.
    Subclasses override: base_url, default_model, _name.
    """

    base_url: str = ""
    default_model: str = ""
    _name: str = "openai_compat"

    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = None):
        self.api_key = api_key
        self.model_name = model_name or self.default_model

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def _payload(self, messages: List[Dict[str, str]], stream: bool = False, **kwargs) -> dict:
        return {
            "model": self.model_name,
            "messages": messages,
            "stream": stream,
            **kwargs,
        }

    async def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Non-streaming chat completion."""
        if not self.api_key:
            raise ValueError(f"{self._name} API key is required.")

        url = f"{self.base_url}/chat/completions"
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                resp = await client.post(
                    url,
                    json=self._payload(messages, stream=False, **kwargs),
                    headers=self._headers(),
                )
                resp.raise_for_status()
                return resp.json()["choices"][0]["message"]["content"]
        except Exception as e:
            logging.error(f"{self._name} chat error: {e}")
            raise Exception(f"{self._name} error: {e}")

    async def stream_chat(
        self, messages: List[Dict[str, str]], **kwargs
    ) -> AsyncGenerator[str, None]:
        """Server-Sent Events streaming chat completion."""
        if not self.api_key:
            raise ValueError(f"{self._name} API key is required.")

        url = f"{self.base_url}/chat/completions"
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                async with client.stream(
                    "POST",
                    url,
                    json=self._payload(messages, stream=True, **kwargs),
                    headers=self._headers(),
                ) as resp:
                    resp.raise_for_status()
                    async for line in resp.aiter_lines():
                        if line.startswith("data: "):
                            if line.strip() == "data: [DONE]":
                                break
                            try:
                                chunk = json.loads(line[6:])
                                content = (
                                    chunk["choices"][0]
                                    .get("delta", {})
                                    .get("content")
                                )
                                if content:
                                    yield content
                            except Exception:
                                continue
        except Exception as e:
            logging.error(f"{self._name} stream error: {e}")
            raise Exception(f"{self._name} stream error: {e}")

    def get_name(self) -> str:
        return self._name
