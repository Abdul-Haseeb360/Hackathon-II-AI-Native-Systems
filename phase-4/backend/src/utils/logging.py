"""
Logging utilities for the Todo API application
"""
import logging
from typing import Any, Dict
from fastapi import Request


def setup_logging():
    """
    Setup logging configuration for the application
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )


def log_request(request: Request, user_id: str, action: str, details: Dict[str, Any] = None):
    """
    Log API request information

    Args:
        request: The FastAPI request object
        user_id: ID of the authenticated user
        action: Description of the action being performed
        details: Additional details about the request
    """
    logger = logging.getLogger("api")
    logger.info(f"User {user_id} performed action: {action} on {request.url.path}")
    if details:
        logger.info(f"Details: {details}")


def log_error(user_id: str, action: str, error: Exception):
    """
    Log error information

    Args:
        user_id: ID of the authenticated user
        action: Description of the action that caused the error
        error: The exception that occurred
    """
    logger = logging.getLogger("api")
    logger.error(f"Error for user {user_id} in action {action}: {str(error)}")