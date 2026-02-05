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
    better_auth_url: Optional[str] = None
    neon_database_url: Optional[str] = None
    port: int = 8000
    cohere_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 10080  # 7 days in minutes (7 * 24 * 60 = 10080)

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()