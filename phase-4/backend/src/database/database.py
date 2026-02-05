"""
Database connection utilities for the Todo API application
"""
from sqlmodel import create_engine, Session
from sqlalchemy.pool import QueuePool
from sqlalchemy import event
from ..config.settings import settings
from ..models import User, Task, Conversation, Message  # noqa: F401


# Create engine with proper connection pooling and retry settings
# Handle Neon/PostgreSQL specific connection parameters
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
    pool_size=10,  # Number of connections to maintain
    max_overflow=20,  # Additional connections beyond pool_size
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=300,  # Recycle connections after 5 minutes
    echo=False,  # Set to True for debugging SQL queries
    connect_args={
        "connect_timeout": 15,  # Increase connection timeout
        "keepalives_idle": 30,  # Seconds after which TCP starts sending keepalive probes
        "keepalives_interval": 5,  # Interval between keepalive probes
        "keepalives_count": 3,  # Number of keepalive probes before declaring dead
    }
)


# Add event listener to handle connection recovery
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """Configure connection-level settings"""
    if "sqlite" not in settings.database_url:
        # For PostgreSQL, ensure proper connection handling
        with dbapi_connection.cursor() as cursor:
            # Set statement timeout to prevent long-running queries
            cursor.execute("SET statement_timeout = 30000;")  # 30 seconds
            # Set lock timeout to prevent hanging
            cursor.execute("SET lock_timeout = 10000;")  # 10 seconds


def get_session():
    """Get database session with connection error handling"""
    try:
        with Session(engine) as session:
            yield session
    except Exception as e:
        # Log the error for debugging
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Database session error: {str(e)}")

        # Re-raise the exception to be handled by the calling function
        raise