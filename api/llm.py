from .config import settings
from .cache import redis_cache
import logging
from .prompts import PROMPT_TEMPLATES
from .providers.gemini import GeminiProvider
from .providers.openai import OpenAIProvider
from .providers.minimax import MinimaxProvider
from .providers.grok import GrokProvider
from .providers.qwen import QwenProvider
from typing import Optional, AsyncGenerator

# Registry of all supported providers.
# Add new OpenAI-compatible providers here — no other changes needed.
_PROVIDER_REGISTRY = {
    "openai":  lambda key: OpenAIProvider(api_key=key),
    "minimax": lambda key: MinimaxProvider(api_key=key),
    "grok":    lambda key: GrokProvider(api_key=key),
    "qwen":    lambda key: QwenProvider(api_key=key),
}

def get_provider(provider_name: str = "gemini", api_key: Optional[str] = None):
    """Factory to get the appropriate LLM provider."""
    factory = _PROVIDER_REGISTRY.get(provider_name)
    if factory:
        return factory(api_key)
    # Default to Gemini (uses system key, no user key needed)
    return GeminiProvider()

class LLMError(Exception):
    """Custom exception for errors related to the Language Model API."""
    pass

async def get_llm_explanation_stream(prompt: str, provider: str = "gemini", api_key: Optional[str] = None):
    """Gets a streaming response from the specified LLM provider."""
    try:
        llm = get_provider(provider, api_key)
        async for chunk in llm.stream_chat([{"role": "user", "content": prompt}]):
            yield chunk
    except Exception as e:
        logging.error(f"Error calling LLM stream ({provider}): {e}")
        raise LLMError(f"Error generating response from {provider}.") from e

@redis_cache(ttl=86400)
async def classify_query(query: str, provider: str = "gemini", api_key: Optional[str] = None) -> str:
    """Classifies a query into a predefined category."""
    prompt = f"""You are a classification agent. Your only job is to classify the user's query... [math, physics, chemistry, programming, ai_concepts, digital_marketing, general_knowledge].

User Query:
---
{query}
---

Classification:"""
    
    try:
        llm = get_provider(provider, api_key)
        category = await llm.chat([{"role": "user", "content": prompt}])
        category = category.strip().lower()
        valid_categories = list(PROMPT_TEMPLATES.keys())
        for valid in valid_categories:
            if valid in category:
                return valid
    except Exception as e:
        logging.error(f"Classification Error: {e}")
    
    return "general_knowledge"

@redis_cache(ttl=86400)
async def translate_text(text: str, target_language: str, source_language: str, provider: str = "gemini", api_key: Optional[str] = None) -> str:
    """Translates text using the specified LLM provider."""
    safe_text = text.replace("{", "{{").replace("}", "}}")
    prompt = f"Translate from {source_language} to {target_language}:\n---\n{safe_text}\n---"
    
    try:
        llm = get_provider(provider, api_key)
        return await llm.chat([{"role": "user", "content": prompt}])
    except Exception as e:
        logging.error(f"Translation Error: {e}")
        raise LLMError("Error translating text.") from e

