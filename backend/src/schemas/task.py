"""
Pydantic request/response models for tasks in the Todo API application
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TaskBase(BaseModel):
    """
    Base model for Task with common fields
    """
    title: str
    description: Optional[str] = None
    completed: bool = False


class TaskCreate(TaskBase):
    """
    Model for creating a new task
    """
    title: str
    description: Optional[str] = None


class TaskUpdate(BaseModel):
    """
    Model for updating an existing task
    """
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class TaskRead(TaskBase):
    """
    Model for reading a task with ID
    """
    id: int
    user_id: str
    created_at: datetime
    updated_at: datetime


from enum import Enum


class TaskStatus(str, Enum):
    """
    Enum for task status values
    """
    all = "all"
    pending = "pending"
    completed = "completed"


class TaskSort(str, Enum):
    """
    Enum for task sort options
    """
    created = "created"
    title = "title"
    due_date = "due_date"