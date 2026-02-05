"""
User model with SQLModel for the Todo API application
"""
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, field_validator


class UserBase(SQLModel):
    """
    Base model for User with common fields
    """
    email: str = Field(unique=True, index=True)
    name: Optional[str] = Field(default=None)


class User(UserBase, table=True):
    """
    User model with database table configuration
    """
    id: str = Field(primary_key=True)
    hashed_password: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class UserCreate(UserBase):
    """
    Model for creating a new user
    """
    password: str

    @field_validator('password')
    @classmethod
    def validate_password_length(cls, v):
        if len(v) > 72:
            raise ValueError('Password must be 72 characters or less')
        return v


class UserRead(BaseModel):
    """
    Model for reading a user with ID
    """
    id: str
    email: str
    name: Optional[str]
    created_at: datetime


class UserSignIn(SQLModel):
    """
    Model for user sign in
    """
    email: str
    password: str