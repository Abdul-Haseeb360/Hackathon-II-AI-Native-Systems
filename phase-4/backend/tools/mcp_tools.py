"""
MCP (Model-Controller-Provider) style tools for task operations
These functions provide stateless interfaces to interact with the database
and are designed to be called by the Cohere agent.
"""
from typing import List, Optional, Dict, Any
from uuid import UUID
from sqlmodel import Session, select
from src.models.task import Task  # type: ignore
from src.models.user import User  # type: ignore


def add_task(title: str, user_id: str, description: Optional[str] = None, session: Session = None) -> Dict[str, Any]:
    """
    Add a new task for the specified user.

    Args:
        title: Title of the task
        user_id: ID of the user who owns the task
        description: Optional description of the task
        session: Database session (injected by caller)

    Returns:
        Dictionary with task creation result
    """
    if not session:
        raise ValueError("Database session is required")

    try:
        # Validate inputs
        if not title or not title.strip():
            return {"status": "error", "message": "Task title cannot be empty"}

        if not user_id:
            return {"status": "error", "message": "User ID is required"}

        # Create new task
        new_task = Task(
            title=title.strip(),
            description=description,
            completed=False,
            user_id=UUID(user_id)  # Assuming user_id is passed as string but stored as UUID
        )

        session.add(new_task)
        session.commit()
        session.refresh(new_task)

        return {
            "status": "success",
            "task_id": new_task.id,
            "message": f"Task '{new_task.title}' added successfully"
        }

    except Exception as e:
        session.rollback() if session else None
        return {"status": "error", "message": f"Failed to add task: {str(e)}"}


def list_tasks(user_id: str, status: Optional[str] = None, session: Session = None) -> Dict[str, Any]:
    """
    List tasks for the specified user with optional filtering by status.

    Args:
        user_id: ID of the user whose tasks to list
        status: Optional status filter ('all', 'pending', 'completed')
        session: Database session (injected by caller)

    Returns:
        Dictionary with list of tasks
    """
    if not session:
        raise ValueError("Database session is required")

    try:
        # Build query based on status filter
        query = select(Task).where(Task.user_id == UUID(user_id))

        if status:
            if status.lower() == "pending":
                query = query.where(Task.completed == False)
            elif status.lower() == "completed":
                query = query.where(Task.completed == True)
            # If status is 'all' or any other value, return all tasks

        tasks = session.exec(query).all()

        task_list = []
        for task in tasks:
            task_dict = {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "created_at": task.created_at.isoformat() if task.created_at else None,
                "updated_at": task.updated_at.isoformat() if task.updated_at else None
            }
            task_list.append(task_dict)

        return {
            "status": "success",
            "tasks": task_list,
            "count": len(task_list),
            "message": f"Found {len(task_list)} tasks for user"
        }

    except Exception as e:
        return {"status": "error", "message": f"Failed to list tasks: {str(e)}"}


def complete_task(task_id: int, user_id: str, session: Session = None) -> Dict[str, Any]:
    """
    Mark a task as completed for the specified user.

    Args:
        task_id: ID of the task to complete
        user_id: ID of the user who owns the task
        session: Database session (injected by caller)

    Returns:
        Dictionary with completion result
    """
    if not session:
        raise ValueError("Database session is required")

    try:
        # Find the task belonging to the user
        stmt = select(Task).where(Task.id == task_id, Task.user_id == UUID(user_id))
        task = session.exec(stmt).first()

        if not task:
            return {
                "status": "error",
                "message": f"Task with ID {task_id} not found or doesn't belong to user"
            }

        # Update task to completed
        task.completed = True
        session.add(task)
        session.commit()
        session.refresh(task)

        return {
            "status": "success",
            "task_id": task.id,
            "message": f"Task '{task.title}' marked as completed"
        }

    except Exception as e:
        session.rollback() if session else None
        return {"status": "error", "message": f"Failed to complete task: {str(e)}"}


def delete_task(task_id: int, user_id: str, session: Session = None) -> Dict[str, Any]:
    """
    Delete a task for the specified user.

    Args:
        task_id: ID of the task to delete
        user_id: ID of the user who owns the task
        session: Database session (injected by caller)

    Returns:
        Dictionary with deletion result
    """
    if not session:
        raise ValueError("Database session is required")

    try:
        # Find the task belonging to the user
        stmt = select(Task).where(Task.id == task_id, Task.user_id == UUID(user_id))
        task = session.exec(stmt).first()

        if not task:
            return {
                "status": "error",
                "message": f"Task with ID {task_id} not found or doesn't belong to user"
            }

        # Delete the task
        session.delete(task)
        session.commit()

        return {
            "status": "success",
            "task_id": task_id,
            "message": f"Task '{task.title}' deleted successfully"
        }

    except Exception as e:
        session.rollback() if session else None
        return {"status": "error", "message": f"Failed to delete task: {str(e)}"}


def update_task(
    task_id: int,
    user_id: str,
    title: Optional[str] = None,
    description: Optional[str] = None,
    completed: Optional[bool] = None,
    session: Session = None
) -> Dict[str, Any]:
    """
    Update a task for the specified user.

    Args:
        task_id: ID of the task to update
        user_id: ID of the user who owns the task
        title: New title for the task (optional)
        description: New description for the task (optional)
        completed: New completion status for the task (optional)
        session: Database session (injected by caller)

    Returns:
        Dictionary with update result
    """
    if not session:
        raise ValueError("Database session is required")

    try:
        # Find the task belonging to the user
        stmt = select(Task).where(Task.id == task_id, Task.user_id == UUID(user_id))
        task = session.exec(stmt).first()

        if not task:
            return {
                "status": "error",
                "message": f"Task with ID {task_id} not found or doesn't belong to user"
            }

        # Update task fields if provided
        if title is not None:
            task.title = title.strip() if title.strip() else task.title
        if description is not None:
            task.description = description
        if completed is not None:
            task.completed = completed

        session.add(task)
        session.commit()
        session.refresh(task)

        return {
            "status": "success",
            "task_id": task.id,
            "message": f"Task '{task.title}' updated successfully"
        }

    except Exception as e:
        session.rollback() if session else None
        return {"status": "error", "message": f"Failed to update task: {str(e)}"}