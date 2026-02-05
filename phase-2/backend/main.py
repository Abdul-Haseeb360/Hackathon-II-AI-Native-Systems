"""
Main entry point for the FastAPI Todo application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.tasks import router as tasks_router
from src.api.auth import router as auth_router


app = FastAPI(
    title="Todo API",
    description="A secure, multi-user todo application with JWT authentication",
    version="1.0.0"
)

# Add CORS middleware right after app creation
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )