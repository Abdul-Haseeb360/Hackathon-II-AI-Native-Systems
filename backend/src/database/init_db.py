"""
Database initialization script for the Todo API application
"""
from sqlmodel import SQLModel, create_engine
from ..models.task import Task
from ..config.settings import settings


def create_db_and_tables():
    """
    Create database tables based on the defined models
    """
    engine = create_engine(settings.database_url)
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    create_db_and_tables()
    print("Database and tables created successfully!")