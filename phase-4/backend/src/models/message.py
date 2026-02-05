# FIXED MAPPER 'no property messages' ERROR - 24 Jan 2026 - Ensured relationship loading before init
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, Optional, Union
from uuid import UUID
from sqlalchemy import JSON
import sqlalchemy as sa

if TYPE_CHECKING:
    from src.models.conversation import Conversation  # type: ignore


class MessageBase(SQLModel):
    """Base class for Message model"""
    role: str = Field(max_length=20, nullable=False)  # "user" or "assistant"
    content: str = Field(nullable=False)
    tool_calls: Optional[Union[dict, list]] = Field(default=None, sa_type=JSON)  # JSON for tool calls made by assistant
    tool_results: Optional[Union[dict, list]] = Field(default=None, sa_type=JSON)  # JSON for results from tool calls


class Message(MessageBase, table=True):
    """Message model representing a single message in a conversation"""
    __tablename__ = "messages"

    id: int = Field(default=None, primary_key=True)
    conversation_id: int = Field(
        sa_column=sa.Column(sa.Integer, sa.ForeignKey("conversations.id"), nullable=False)
    )
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationship to conversation this message belongs to
    conversation: "Conversation" = Relationship(back_populates="messages")