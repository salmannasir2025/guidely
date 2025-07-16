from .config import settings
from serpapi import SerpApiClient
from .cache import redis_cache
from fastapi.concurrency import run_in_threadpool
import logging

@redis_cache(ttl=3600)  # Cache web search results for 1 hour
async def perform_web_search(query: str) -> str:
    """
    Performs a web search using SerpAPI and returns a compiled context string.
    This context is built from the answer box and top organic result snippets.
    """
    try:
        params = {
            "api_key": settings.serpapi_api_key,
            "engine": "google",
            "q": query,
            "gl": "pk",  # Geolocation Pakistan, as per project requirements
            "hl": "en",  # Language English
        }
        # Run the synchronous search in a thread to avoid blocking.
        results = await run_in_threadpool(SerpApiClient(params).get_dict)

        context_parts = []

        # Prioritize the answer box for direct, concise answers if it exists
        if "answer_box" in results:
            answer_box = results["answer_box"]
            if "snippet" in answer_box:
                context_parts.append(answer_box["snippet"])
            elif "answer" in answer_box:
                context_parts.append(answer_box["answer"])

        # Add snippets from the top 3 organic results for broader context
        if "organic_results" in results:
            for result in results.get("organic_results", [])[:3]:
                if "snippet" in result:
                    context_parts.append(result["snippet"])

        return "\n\n".join(context_parts)
    except Exception as e:
        logging.error(
            "SerpAPI search failed.",
            extra={"query": query, "error": str(e)}
        )
        return ""