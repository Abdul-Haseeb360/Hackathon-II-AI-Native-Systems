"""
Configuration management with pydantic-settings for the Todo API application
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    """
    database_url: str = "sqlite:///./todo_api.db"  # Default to SQLite for development
    better_auth_secret: str = "your-default-secret-key-for-development"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"


settings = Settings()