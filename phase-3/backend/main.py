"""
Main entry point for the FastAPI Todo application
"""
import logging
import sys
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the current directory to the Python path to resolve module imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from src.api.tasks import router as tasks_router
from src.api.auth import router as auth_router
from routers.chat import router as chat_router

# Import all models to ensure SQLModel relationships are properly registered before app starts
from src.models import User, Task, Conversation, Message  # noqa: F401

# Test database connection on startup
try:
    from src.database.init_db import create_db_and_tables
    create_db_and_tables()
except Exception as e:
    import logging
    logger = logging.getLogger(__name__)
    logger.error(f"Database connection error on startup: {str(e)}")
    # Don't crash the app on startup, let it continue but log the error
    print(f"WARNING: Could not connect to database: {str(e)}")
    print("The application may not function properly without a database connection.")


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """Custom middleware for logging requests and responses"""
    async def dispatch(self, request: Request, call_next):
        start_time = datetime.utcnow()

        # Log incoming request
        logger.info(f"Request: {request.method} {request.url.path}")

        try:
            response = await call_next(request)

            # Calculate processing time
            process_time = (datetime.utcnow() - start_time).total_seconds()

            # Log response
            logger.info(f"Response: {response.status_code} - Process time: {process_time}s")

            return response
        except Exception as e:
            # Log any exceptions
            process_time = (datetime.utcnow() - start_time).total_seconds()
            logger.error(f"Unhandled exception in {request.method} {request.url.path}: {str(e)} - Process time: {process_time}s")
            raise


app = FastAPI(
    title="Todo API",
    description="A secure, multi-user todo application with JWT authentication",
    version="1.0.0",
    # Add custom exception handlers
    exception_handlers={
        Exception: lambda request, exc: JSONResponse(
            status_code=500,
            content={"detail": "Internal server error", "error": str(exc)}
        )
    }
)

# Add logging middleware first
app.add_middleware(LoggingMiddleware)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    """Handle validation errors"""
    logger.warning(f"Validation error: {exc}")
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Validation error",
            "errors": jsonable_encoder(exc.errors())
        }
    )


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    """Middleware to handle database sessions"""
    request.state.start_time = datetime.utcnow()
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        logger.error(f"Request failed: {str(e)}")
        raise


@app.get("/")
async def root():
    """
    Root endpoint for the Todo API
    """
    return {"message": "Welcome to the Todo API"}


# Include the tasks router
app.include_router(tasks_router)

# Include the auth router
app.include_router(auth_router, prefix="/api/auth", tags=["auth"], include_in_schema=True)

# Include the chat router
app.include_router(chat_router, include_in_schema=True)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )