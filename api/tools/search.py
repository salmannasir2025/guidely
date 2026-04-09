import logging
from typing import Any, Dict
from serpapi import SerpApiClient
from fastapi.concurrency import run_in_threadpool
from .base import BaseTool
from ..config import settings
from ..cache import redis_cache

class WebSearchTool(BaseTool):
    """Tool for performing web searches via SerpAPI."""

    def get_name(self) -> str:
        return "web_search"

    def get_description(self) -> str:
        return "Performs a Google web search using SerpAPI to gather context."

    @redis_cache(ttl=3600)
    async def execute(self, query: str = None, **kwargs) -> str:
        if not query:
            return ""
            
        try:
            params = {
                "api_key": settings.serpapi_api_key,
                "engine": "google",
                "q": query,
                "gl": "pk",
                "hl": "en",
            }
            results = await run_in_threadpool(SerpApiClient(params).get_dict)
            
            context_parts = []
            if "answer_box" in results:
                answer = results["answer_box"]
                context_parts.append(answer.get("snippet") or answer.get("answer") or "")
            
            if "organic_results" in results:
                for result in results.get("organic_results", [])[:3]:
                    if "snippet" in result:
                        context_parts.append(result["snippet"])
            
            return "\n\n".join(filter(None, context_parts))
        except Exception as e:
            logging.error(f"WebSearchTool Error: {e}")
            return ""
