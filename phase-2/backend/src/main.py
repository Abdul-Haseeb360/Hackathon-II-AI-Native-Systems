"""
Main entry point for the FastAPI Todo application
"""
from fastapi import FastAPI
from .api.tasks import router as tasks_router
from .api.auth import router as auth_router

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