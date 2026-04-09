"""
Minimax Provider
================
Uses the OpenAI-compatible endpoint from MiniMax International.
Base URL: https://api.minimax.io/v1
Free-tier model: MiniMax-Text-01 (or MiniMax-M2.5 where available)
"""
from .openai_compat import OpenAICompatProvider


class MinimaxProvider(OpenAICompatProvider):
    base_url = "https://api.minimax.io/v1"
    default_model = "MiniMax-Text-01"
    _name = "minimax"
