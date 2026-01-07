"""
Task service with database operations for the Todo API application
"""
from typing import List, Optional
from sqlmodel import Session, select
from ..models.task import Task, TaskCreate, TaskUpdate
from ..utils import UserNotOwnerException, TaskNotFoundException


class TaskService:
    """
    Service class for handling task operations
    """

    @staticmethod
    def create_task(session: Session, task_data: TaskCreate, user_id: str) -> Task:
        """
        Create a new task for the authenticated user

        Args:
            session: Database session
            task_data: Task creation data
            user_id: ID of the user creating the task

        Returns:
            Created Task object
        """
        task = Task.model_validate(task_data)
        task.user_id = user_id
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    @staticmethod
    def get_tasks_by_user(
        session: Session,
        user_id: str,
        status: Optional[str] = None,
        sort: Optional[str] = None
    ) -> List[Task]:
        """
        Get all tasks for a specific user with optional filtering and sorting

        Args:
            session: Database session
            user_id: ID of the user whose tasks to retrieve
            status: Optional status filter (all, pending, completed)
            sort: Optional sort order (created, title)

        Returns:
            List of Task objects belonging to the user
        """
        query = select(Task).where(Task.user_id == user_id)

        # Apply status filter if specified
        if status and status.lower() != 'all':
            if status.lower() == 'pending':
                query = query.where(Task.completed == False)
            elif status.lower() == 'completed':
                query = query.where(Task.completed == True)

        # Apply sorting if specified
        if sort:
            if sort.lower() == 'title':
                query = query.order_by(Task.title)
            elif sort.lower() == 'created':
                query = query.order_by(Task.created_at.desc())

        tasks = session.exec(query).all()
        return tasks

    @staticmethod
    def get_task_by_id_and_user(session: Session, task_id: int, user_id: str) -> Optional[Task]:
        """
        Get a specific task by ID for a specific user

        Args:
            session: Database session
            task_id: ID of the task to retrieve
            user_id: ID of the user who owns the task

        Returns:
            Task object if found and belongs to user, None otherwise
        """
        query = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        task = session.exec(query).first()
        return task

    @staticmethod
    def update_task(session: Session, task_id: int, task_data: TaskUpdate, user_id: str) -> Optional[Task]:
        """
        Update an existing task for a specific user

        Args:
            session: Database session
            task_id: ID of the task to update
            task_data: Task update data
            user_id: ID of the user who owns the task

        Returns:
            Updated Task object if successful, None if task doesn't exist or user doesn't own it

        Raises:
            UserNotOwnerException: If the user doesn't own the task
        """
        task = TaskService.get_task_by_id_and_user(session, task_id, user_id)
        if not task:
            raise UserNotOwnerException("Task does not exist or user does not have permission to update it")

        # Update task fields based on provided data
        update_data = task_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if value is not None:
                setattr(task, field, value)

        task.updated_at = task.__class__.updated_at.default.func()
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    @staticmethod
    def delete_task(session: Session, task_id: int, user_id: str) -> bool:
        """
        Delete a task for a specific user

        Args:
            session: Database session
            task_id: ID of the task to delete
            user_id: ID of the user who owns the task

        Returns:
            True if task was deleted, False if task doesn't exist or user doesn't own it

        Raises:
            UserNotOwnerException: If the user doesn't own the task
        """
        task = TaskService.get_task_by_id_and_user(session, task_id, user_id)
        if not task:
            raise UserNotOwnerException("Task does not exist or user does not have permission to delete it")

        session.delete(task)
        session.commit()
        return True