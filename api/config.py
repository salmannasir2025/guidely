from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from typing import List
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
    mongo_users_collection: str = "users"
    
    # JWT Settings
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    password_reset_token_expire_hours: int = 1

    # Email settings for password recovery
    mail_username: str
    mail_password: str
    mail_from: str
    mail_port: int = 587
    mail_server: str
    mail_starttls: bool = True
    mail_ssl_tls: bool = False

    # File settings
    file_upload_max_size: int = 10 * 1024 * 1024  # 10 MB
    allowed_file_types: List[str] = ["image/jpeg", "image/png", "image/gif"]

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
