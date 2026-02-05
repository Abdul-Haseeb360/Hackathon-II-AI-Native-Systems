# FIXED MAPPER 'no property messages' ERROR - 24 Jan 2026 - Ensured relationship loading before init
"""
User model with SQLModel for the Todo API application
"""
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, field_validator
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

if TYPE_CHECKING:
    from src.models.conversation import Conversation  # type: ignore


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
    __tablename__ = "users"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    hashed_password: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to conversations owned by this user
    conversations: list["Conversation"] = Relationship(back_populates="user")


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