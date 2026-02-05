# FIXED MAPPER 'no property messages' ERROR - 24 Jan 2026 - Ensured relationship loading before init
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, Optional, List
from uuid import UUID
from sqlalchemy import ForeignKey
import sqlalchemy as sa

if TYPE_CHECKING:
    from src.models.user import User  # type: ignore
    from src.models.message import Message  # type: ignore


class ConversationBase(SQLModel):
    """Base class for Conversation model"""
    title: Optional[str] = Field(default=None, max_length=255)


class Conversation(ConversationBase, table=True):
    """Conversation model representing a chat session between user and AI"""
    __tablename__ = "conversations"

    id: int = Field(default=None, primary_key=True)
    user_id: UUID = Field(sa_column=sa.Column(sa.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False))  # Foreign key to user
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationships
    user: "User" = Relationship(back_populates="conversations")
    messages: List["Message"] = Relationship(back_populates="conversation")