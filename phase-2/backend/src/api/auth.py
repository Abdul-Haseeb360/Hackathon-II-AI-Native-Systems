"""
Authentication API endpoints for the Todo API application
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from typing import Optional
from datetime import datetime, timedelta
from jose import jwt
from pydantic import BaseModel
import bcrypt
from ..database.database import get_session
from ..models.user import User, UserCreate, UserSignIn
from ..auth.jwt import SECRET_KEY, ALGORITHM


class UserResponse(BaseModel):
    """Response model for user with token"""
    user: dict
    token: str

router = APIRouter(tags=["auth"], include_in_schema=True)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    try:
        # Truncate password to 72 bytes to comply with bcrypt limitations
        truncated_password = plain_password.encode('utf-8')[:72]
        stored_hash = hashed_password.encode('utf-8')
        return bcrypt.checkpw(truncated_password, stored_hash)
    except Exception:
        return False


def get_password_hash(password: str) -> str:
    """Hash a plain password using bcrypt."""
    # Truncate password to 72 bytes to comply with bcrypt limitations
    truncated_password = password[:72] if len(password) > 72 else password
    # Encode the password to bytes and hash it
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(truncated_password.encode('utf-8'), salt)
    # Decode back to string for storage
    return hashed.decode('utf-8')


@router.post("/signup", tags=["auth"], include_in_schema=True, response_model=UserResponse)
def signup(user_create: UserCreate, session: Session = Depends(get_session)) -> UserResponse:
    """Register a new user account."""
    try:
        # Check if user with this email already exists
        existing_user = session.exec(select(User).where(User.email == user_create.email)).first()
        if existing_user:
            raise HTTPException(status_code=409, detail="Email already registered")

        # Hash the password
        hashed_password = get_password_hash(user_create.password)

        # Create new user
        db_user = User(
            id=str(datetime.utcnow().timestamp()),  # Generate a unique ID
            email=user_create.email,
            name=user_create.name,
            hashed_password=hashed_password
        )

        session.add(db_user)
        session.commit()
        session.refresh(db_user)

        # Generate JWT token
        payload = {
            "user_id": db_user.id,
            "exp": datetime.utcnow() + timedelta(days=7)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        # Return user info with token
        return UserResponse(
            user={
                "id": db_user.id,
                "email": db_user.email,
                "name": db_user.name
            },
            token=token
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/signin", tags=["auth"], include_in_schema=True, response_model=UserResponse)
def signin(user_signin: UserSignIn, session: Session = Depends(get_session)) -> UserResponse:
    """Authenticate user and return user info with token."""
    try:
        # Find user by email
        user = session.exec(select(User).where(User.email == user_signin.email)).first()
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # Verify password
        if not verify_password(user_signin.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # Generate JWT token
        payload = {
            "user_id": user.id,
            "exp": datetime.utcnow() + timedelta(days=7)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        return UserResponse(
            user={
                "id": user.id,
                "email": user.email,
                "name": user.name
            },
            token=token
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))