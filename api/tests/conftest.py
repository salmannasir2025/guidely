"""
This file provides shared fixtures for the entire test suite.
Pytest automatically discovers and uses these fixtures.
"""

import pytest
from unittest.mock import AsyncMock


@pytest.fixture
def mock_ask_dependencies(mocker):
    """Mocks all dependencies for the /ask endpoint handler."""
    mocks = {
        "classify_query": mocker.patch("api.ask.classify_query", new_callable=AsyncMock),
        "perform_web_search": mocker.patch("api.ask.perform_web_search", new_callable=AsyncMock),
        "get_rag_prompt": mocker.patch("api.ask.get_rag_prompt"),
        "get_llm_explanation_stream": mocker.patch("api.ask.get_llm_explanation_stream", new_callable=AsyncMock),
        "solve_math_problem": mocker.patch("api.ask.solve_math_problem"),
        "log_interaction": mocker.patch("api.ask.log_interaction", new_callable=AsyncMock),
    }
    return mocks


@pytest.fixture
def mock_stream_generator():
    """Creates a mock async generator for streaming responses."""
    async def _generator(content: str):
        yield content
    return _generator


@pytest.fixture
def mock_health_dependencies(mocker):
    """Mocks all dependency health check functions."""
    mocks = {
        "db": mocker.patch("api.database.check_db_connection", new_callable=AsyncMock),
        "redis": mocker.patch("api.cache.check_redis_connection", new_callable=AsyncMock),
        "llm": mocker.patch("api.llm.check_llm_client"),
        "vision": mocker.patch("api.ocr.check_vision_client"),
        "stt": mocker.patch("api.speech.check_speech_to_text_client"),
        "tts": mocker.patch("api.speech.check_text_to_speech_client"),
    }
    return mocks