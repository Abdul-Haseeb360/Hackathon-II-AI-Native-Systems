"""
API endpoints for tasks in the Todo API application
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from sqlmodel import Session
from ..database.database import get_session
from ..auth.dependencies import get_current_user_id
from ..models.task import TaskCreate, TaskRead, TaskUpdate
from ..services.task_service import TaskService
from ..schemas.task import TaskStatus, TaskSort
from ..utils import UserNotOwnerException


router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TaskCreate,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the authenticated user
    """
    try:
        task = TaskService.create_task(session, task_data, user_id)
        return task
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating task: {str(e)}"
        )


@router.get("/", response_model=List[TaskRead])
def get_tasks(
    user_id: str = Depends(get_current_user_id),
    status_filter: Optional[TaskStatus] = Query(None, alias="status"),
    sort_by: Optional[TaskSort] = Query(None, alias="sort"),
    session: Session = Depends(get_session)
):
    """
    Get all tasks for the authenticated user with optional filtering and sorting
    """
    try:
        tasks = TaskService.get_tasks_by_user(
            session=session,
            user_id=user_id,
            status=status_filter.value if status_filter else None,
            sort=sort_by.value if sort_by else None
        )
        return tasks
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving tasks: {str(e)}"
        )


@router.put("/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Update an existing task for the authenticated user
    """
    try:
        updated_task = TaskService.update_task(session, task_id, task_data, user_id)
        if not updated_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found or user does not have permission to update it"
            )
        return updated_task
    except UserNotOwnerException:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not have permission to update this task"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating task: {str(e)}"
        )


@router.patch("/{task_id}/complete", response_model=TaskRead)
def complete_task(
    task_id: int,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Mark a task as complete for the authenticated user
    """
    try:
        # Create a TaskUpdate object to update only the completed status
        task_update_data = TaskUpdate(completed=True)
        updated_task = TaskService.update_task(session, task_id, task_update_data, user_id)
        if not updated_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found or user does not have permission to update it"
            )
        return updated_task
    except UserNotOwnerException:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not have permission to update this task"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating task completion status: {str(e)}"
        )


@router.delete("/{task_id}", status_code=status.HTTP_200_OK)
def delete_task(
    task_id: int,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Delete a task for the authenticated user
    """
    try:
        success = TaskService.delete_task(session, task_id, user_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found or user does not have permission to delete it"
            )
        return {"message": "Task deleted successfully"}
    except UserNotOwnerException:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not have permission to delete this task"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting task: {str(e)}"
        )