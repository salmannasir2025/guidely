from .config import settings
from .cache import redis_cache
import logging
from fastapi.concurrency import run_in_threadpool
from .prompts import PROMPT_TEMPLATES
from .providers.gemini import GeminiProvider

# Initialize the default provider
# In a future update, this registry will load providers based on settings.
_provider = GeminiProvider()

class LLMError(Exception):
    """Custom exception for errors related to the Language Model API."""
    pass

def initialize_llm():
    """Reserved for initialization if needed (GeminiProvider handles its own config)."""
    logging.info("LLM system initialized with GeminiProvider.")

def get_llm_explanation(prompt: str) -> str:
    """Gets a response from the default LLM provider."""
    import asyncio
    try:
        # Use synchronous wrapper for the chat method
        return asyncio.run(_provider.chat([{"role": "user", "content": prompt}]))
    except Exception as e:
        logging.error(f"Error calling LLM provider: {e}")
        raise LLMError("Error generating response from the language model.") from e

async def get_llm_explanation_stream(prompt: str):
    """Gets a streaming response from the default LLM provider."""
    try:
        async for chunk in _provider.stream_chat([{"role": "user", "content": prompt}]):
            yield chunk
    except Exception as e:
        logging.error(f"Error calling LLM stream: {e}")
        raise LLMError("Error generating response from the language model.") from e

@redis_cache(ttl=86400)
async def classify_query(query: str) -> str:
    """Classifies a query into a predefined category."""
    prompt = f"""You are a classification agent. Your only job is to classify the user's query... [math, physics, chemistry, programming, ai_concepts, digital_marketing, general_knowledge].

User Query:
---
{query}
---

Classification:"""
    
    async def _classify():
        try:
            category = await _provider.chat([{"role": "user", "content": prompt}])
            category = category.strip().lower()
            valid_categories = list(PROMPT_TEMPLATES.keys())
            for valid in valid_categories:
                if valid in category:
                    return valid
            return "general_knowledge"
        except Exception as e:
            logging.error(f"Classification Error: {e}")
            return "general_knowledge"

    return await _classify()

@redis_cache(ttl=86400)
async def translate_text(text: str, target_language: str, source_language: str) -> str:
    """Translates text using the default LLM provider."""
    safe_text = text.replace("{", "{{").replace("}", "}}")
    prompt = f"Translate from {source_language} to {target_language}:\n---\n{safe_text}\n---"
    
    try:
        return await _provider.chat([{"role": "user", "content": prompt}])
    except Exception as e:
        logging.error(f"Translation Error: {e}")
        raise LLMError("Error translating text.") from e

def check_llm_client() -> bool:
    """Checks if the LLM provider is available."""
    return _provider is not None

