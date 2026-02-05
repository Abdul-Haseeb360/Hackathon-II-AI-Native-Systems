"""
JWT utility functions for token validation in the Todo API application
"""
from datetime import datetime, timedelta
from typing import Optional
import os
from jose import JWTError, jwt
from fastapi import HTTPException, status


SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "your-default-secret-key-for-development")
ALGORITHM = "HS256"


def verify_token(token: str) -> Optional[dict]:
    """
    Verify JWT token and extract user information

    Args:
        token: JWT token string to verify

    Returns:
        User information from token payload if valid, None otherwise
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        if user_id is None:
            return None
        return payload
    except JWTError:
        return None


def get_user_id_from_token(token: str) -> Optional[str]:
    """
    Extract user_id from JWT token

    Args:
        token: JWT token string to extract user_id from

    Returns:
        User ID if token is valid, None otherwise
    """
    payload = verify_token(token)
    if payload:
        return payload.get("user_id")
    return None