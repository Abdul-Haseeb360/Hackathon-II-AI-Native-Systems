"""
Task model with SQLModel for the Todo API application
"""
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID
import sqlalchemy as sa


class TaskBase(SQLModel):
    """
    Base model for Task with common fields
    """
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)


class Task(TaskBase, table=True):
    """
    Task model with database table configuration
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", nullable=False)  # Foreign key to user (from JWT)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class TaskCreate(TaskBase):
    """
    Model for creating a new task
    """
    pass  # user_id will be set from JWT token, not from request body


class TaskUpdate(SQLModel):
    """
    Model for updating an existing task
    """
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: Optional[bool] = None


class TaskRead(TaskBase):
    """
    Model for reading a task with ID
    """
    id: int
    user_id: UUID
    created_at: datetime
    updated_at: datetime