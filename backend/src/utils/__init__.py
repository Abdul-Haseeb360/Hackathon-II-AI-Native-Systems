"""
Base models and error handling utilities for the Todo API application
"""
from fastapi import HTTPException, status


class UserNotOwnerException(HTTPException):
    """
    Exception raised when a user attempts to access a resource they don't own
    """
    def __init__(self, detail: str = "User does not have permission to access this resource"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )


class TaskNotFoundException(HTTPException):
    """
    Exception raised when a requested task is not found
    """
    def __init__(self, detail: str = "Task not found"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )