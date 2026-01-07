"""
Database connection utilities for the Todo API application
"""
from sqlmodel import create_engine, Session
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///./todo_api.db"  # Default to SQLite for development


settings = Settings()
engine = create_engine(settings.database_url)


def get_session():
    with Session(engine) as session:
        yield session