"""
xAI Grok Provider
==================
Uses the OpenAI-compatible endpoint from xAI.
Base URL: https://api.x.ai/v1
Latest model: grok-beta
"""
from .openai_compat import OpenAICompatProvider


class GrokProvider(OpenAICompatProvider):
    base_url = "https://api.x.ai/v1"
    default_model = "grok-beta"
    _name = "grok"
