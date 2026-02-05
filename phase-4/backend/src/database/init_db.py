"""
Database initialization script for the Todo API application
"""
from sqlmodel import SQLModel, create_engine
from sqlalchemy.pool import QueuePool
from ..models.task import Task
from ..models.user import User
from ..models.conversation import Conversation
from ..models.message import Message
from ..config.settings import settings


def create_db_and_tables():
    """
    Create database tables based on the defined models
    """
    import urllib.parse

    # Parse the database URL to modify problematic parameters
    parsed_url = urllib.parse.urlparse(settings.database_url)
    if parsed_url.scheme.startswith('postgresql'):
        # Remove channel_binding parameter if present, as it can cause connection issues with Neon
        query_params = urllib.parse.parse_qs(parsed_url.query)
        if 'channel_binding' in query_params:
            del query_params['channel_binding']

        # Rebuild the query string without channel_binding
        new_query = urllib.parse.urlencode(query_params, doseq=True)
        modified_url = parsed_url._replace(query=new_query).geturl()
    else:
        modified_url = settings.database_url

    engine = create_engine(
        modified_url,
        poolclass=QueuePool,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,
        pool_recycle=300,
        echo=False,
        connect_args={
            "connect_timeout": 15,  # Increase connection timeout
        }
    )

    # Drop and recreate all tables to ensure correct schema
    # This will ensure UUID columns are properly defined
    from sqlmodel import SQLModel
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    create_db_and_tables()
    print("Database and tables created successfully!")