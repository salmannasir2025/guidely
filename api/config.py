from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
import os


class Settings(BaseSettings):
    """Loads and validates settings from environment variables."""

    gemini_api_key: str
    serpapi_api_key: str
    mongo_connection_string: str
    redis_url: str
    frontend_url: str
    mongo_db_name: str = "ai_tutor_db"
    mongo_interactions_collection: str = "interactions"
    mongo_feedback_collection: str = "feedback"

    # This makes .env loading robust by specifying the path relative to this file.
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), ".env"),
        env_file_encoding="utf-8",
    )


@lru_cache
def get_settings():
    """Returns a cached instance of the settings."""
    return Settings()


settings = get_settings()
