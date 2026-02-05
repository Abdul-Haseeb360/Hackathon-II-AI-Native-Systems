"""
Database connection utilities for the Todo API application
"""
from sqlmodel import create_engine, Session
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://neondb_owner:npg_mL39YARxGbfC@ep-raspy-darkness-advcm06z-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"   # Default to SQLite for development


settings = Settings()
engine = create_engine(settings.database_url)


def get_session():
    with Session(engine) as session:
        yield session