"""
Alibaba Qwen Provider
======================
Uses the DashScope OpenAI-compatible International endpoint.
Base URL: https://dashscope-intl.aliyuncs.com/compatible-mode/v1
Free/cheap model: qwen-turbo (generous free tier on DashScope)
"""
from .openai_compat import OpenAICompatProvider


class QwenProvider(OpenAICompatProvider):
    base_url = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
    default_model = "qwen-turbo"
    _name = "qwen"
