"""
Main entry point for the FastAPI Todo application
"""
import logging
from fastapi import FastAPI
from src.api.tasks import router as tasks_router
from src.utils.logging import setup_logging


# Setup logging
setup_logging()

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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )