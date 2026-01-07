"""
JWT dependency for extracting user_id from token in the Todo API application
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .jwt import get_user_id_from_token


security = HTTPBearer()


def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Dependency to get current user ID from JWT token

    Args:
        credentials: HTTP authorization credentials from the request

    Returns:
        User ID extracted from the JWT token

    Raises:
        HTTPException: If token is invalid or user_id cannot be extracted
    """
    user_id = get_user_id_from_token(credentials.credentials)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user_id