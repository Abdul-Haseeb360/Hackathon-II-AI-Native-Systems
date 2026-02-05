# FIXED MAPPER 'no property messages' ERROR - 24 Jan 2026 - Ensured relationship loading before init
# Import all models to ensure proper SQLModel registration
from .user import User
from .task import Task
from .conversation import Conversation
from .message import Message

__all__ = ["User", "Task", "Conversation", "Message"]