"""
Main entry point for the FastAPI Todo application
"""
from fastapi import FastAPI
from .api.tasks import router as tasks_router
from .api.auth import router as auth_router

# Import all models to ensure SQLModel relationships are properly registered before app starts
from .models import User, Task, Conversation, Message  # noqa: F401

# Test database connection on startup
try:
    from .database.init_db import create_db_and_tables
    create_db_and_tables()
except Exception as e:
    import logging
    logger = logging.getLogger(__name__)
    logger.error(f"Database connection error on startup: {str(e)}")
    # Don't crash the app on startup, let it continue but log the error
    print(f"WARNING: Could not connect to database: {str(e)}")
    print("The application may not function properly without a database connection.")

app = FastAPI(
    title="Todo API",
    description="A secure, multi-user todo application with JWT authentication",
    version="1.0.0"
)


@app.get("/")
async def root():
    """
    Root endpoint for the Todo API
    """
    return {"message": "Welcome to the Todo API"}


# Include the tasks router
app.include_router(tasks_router)
app.include_router(auth_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )