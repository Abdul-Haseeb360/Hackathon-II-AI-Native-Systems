"""
Unit tests for MCP tools functions in phase-3/backend/tools/mcp_tools.py
"""
import pytest
from unittest.mock import Mock, MagicMock
from sqlmodel import Session
from uuid import UUID
from tools.mcp_tools import (
    add_task,
    list_tasks,
    complete_task,
    delete_task,
    update_task
)


def test_add_task_success():
    """Test successful task addition"""
    mock_session = Mock(spec=Session)
    mock_task = Mock()
    mock_task.id = 1
    mock_task.title = "Test Task"
    mock_task.description = None
    mock_task.completed = False
    mock_task.user_id = UUID("12345678-1234-5678-1234-567812345678")

    # Mock the session operations
    mock_session.add = Mock()
    mock_session.commit = Mock()
    mock_session.refresh = Mock(side_effect=lambda obj: setattr(obj, 'id', 1))

    result = add_task(
        title="Test Task",
        user_id="12345678-1234-5678-1234-567812345678",
        session=mock_session
    )

    assert result["status"] == "success"
    assert result["task_id"] == 1
    assert "added successfully" in result["message"]

    # Verify session methods were called
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()


def test_add_task_empty_title():
    """Test adding task with empty title"""
    result = add_task(
        title="",
        user_id="12345678-1234-5678-1234-567812345678",
        session=Mock(spec=Session)
    )

    assert result["status"] == "error"
    assert "cannot be empty" in result["message"]


def test_add_task_missing_user_id():
    """Test adding task without user ID"""
    result = add_task(
        title="Test Task",
        user_id="",
        session=Mock(spec=Session)
    )

    assert result["status"] == "error"
    assert "User ID is required" in result["message"]


def test_add_task_exception_handling():
    """Test exception handling in add_task"""
    mock_session = Mock(spec=Session)
    mock_session.add.side_effect = Exception("Database error")
    mock_session.rollback = Mock()

    result = add_task(
        title="Test Task",
        user_id="12345678-1234-5678-1234-567812345678",
        session=mock_session
    )

    assert result["status"] == "error"
    assert "Failed to add task" in result["message"]
    mock_session.rollback.assert_called_once()


def test_list_tasks_success():
    """Test successful task listing"""
    mock_session = Mock(spec=Session)
    mock_task = Mock()
    mock_task.id = 1
    mock_task.title = "Test Task"
    mock_task.description = "Test Description"
    mock_task.completed = False
    mock_task.created_at = Mock()
    mock_task.created_at.isoformat.return_value = "2023-01-01T00:00:00"
    mock_task.updated_at = Mock()
    mock_task.updated_at.isoformat.return_value = "2023-01-01T00:00:00"
    mock_task.user_id = UUID("12345678-1234-5678-1234-567812345678")

    mock_session.exec = Mock(return_value=Mock())
    mock_session.exec.return_value.all.return_value = [mock_task]

    result = list_tasks(
        user_id="12345678-1234-5678-1234-567812345678",
        session=mock_session
    )

    assert result["status"] == "success"
    assert result["count"] == 1
    assert len(result["tasks"]) == 1
    assert result["tasks"][0]["title"] == "Test Task"


def test_list_tasks_pending_filter():
    """Test listing tasks with pending filter"""
    mock_session = Mock(spec=Session)
    mock_result = Mock()
    mock_session.exec = Mock(return_value=mock_result)
    mock_result.all.return_value = []

    result = list_tasks(
        user_id="12345678-1234-5678-1234-567812345678",
        status="pending",
        session=mock_session
    )

    assert result["status"] == "success"


def test_list_tasks_completed_filter():
    """Test listing tasks with completed filter"""
    mock_session = Mock(spec=Session)
    mock_result = Mock()
    mock_session.exec = Mock(return_value=mock_result)
    mock_result.all.return_value = []

    result = list_tasks(
        user_id="12345678-1234-5678-1234-567812345678",
        status="completed",
        session=mock_session
    )

    assert result["status"] == "success"


def test_list_tasks_exception_handling():
    """Test exception handling in list_tasks"""
    mock_session = Mock(spec=Session)
    mock_session.exec.side_effect = Exception("Database error")

    result = list_tasks(
        user_id="12345678-1234-5678-1234-567812345678",
        session=mock_session
    )

    assert result["status"] == "error"
    assert "Failed to list tasks" in result["message"]


def test_complete_task_success():
    """Test successful task completion"""
    mock_session = Mock(spec=Session)
    mock_task = Mock()
    mock_task.id = 1
    mock_task.title = "Test Task"
    mock_task.completed = False
    mock_task.user_id = UUID("12345678-1234-5678-1234-567812345678")

    mock_result = Mock()
    mock_result.first.return_value = mock_task
    mock_session.exec = Mock(return_value=mock_result)
    mock_session.add = Mock()
    mock_session.commit = Mock()
    mock_session.refresh = Mock()

    result = complete_task(
        task_id=1,
        user_id="12345678-1234-5678-1234-567812345678",
        session=mock_session
    )

    assert result["status"] == "success"
    assert result["task_id"] == 1
    assert "marked as completed" in result["message"]

    # Verify task was marked as completed
    assert mock_task.completed is True
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()


def test_complete_task_not_found():
    """Test completing a task that doesn't exist"""
    mock_session = Mock(spec=Session)
    mock_result = Mock()
    mock_result.first.return_value = None
    mock_session.exec = Mock(return_value=mock_result)

    result = complete_task(
        task_id=999,
        user_id="12345678-1234-5678-1234-567812345678",
        session=mock_session
    )

    assert result["status"] == "error"
    assert "not found" in result["message"]


def test_complete_task_exception_handling():
    """Test exception handling in complete_task"""
    mock_session = Mock(spec=Session)
    mock_session.exec.side_effect = Exception("Database error")
    mock_session.rollback = Mock()

    result = complete_task(
        task_id=1,
        user_id="12345678-1234-5678-1234-567812345678",
        session=mock_session
    )

    assert result["status"] == "error"
    assert "Failed to complete task" in result["message"]
    mock_session.rollback.assert_called_once()


def test_delete_task_success():
    """Test successful task deletion"""
    mock_session = Mock(spec=Session)
    mock_task = Mock()
    mock_task.id = 1
    mock_task.title = "Test Task"
    mock_task.user_id = UUID("12345678-1234-5678-1234-567812345678")

    mock_result = Mock()
    mock_result.first.return_value = mock_task
    mock_session.exec = Mock(return_value=mock_result)
    mock_session.delete = Mock()
    mock_session.commit = Mock()

    result = delete_task(
        task_id=1,
        user_id="12345678-1234-5678-1234-567812345678",
        session=mock_session
    )

    assert result["status"] == "success"
    assert result["task_id"] == 1
    assert "deleted successfully" in result["message"]

    mock_session.delete.assert_called_once()
    mock_session.commit.assert_called_once()


def test_delete_task_not_found():
    """Test deleting a task that doesn't exist"""
    mock_session = Mock(spec=Session)
    mock_result = Mock()
    mock_result.first.return_value = None
    mock_session.exec = Mock(return_value=mock_result)

    result = delete_task(
        task_id=999,
        user_id="12345678-1234-5678-1234-567812345678",
        session=mock_session
    )

    assert result["status"] == "error"
    assert "not found" in result["message"]


def test_delete_task_exception_handling():
    """Test exception handling in delete_task"""
    mock_session = Mock(spec=Session)
    mock_session.exec.side_effect = Exception("Database error")
    mock_session.rollback = Mock()

    result = delete_task(
        task_id=1,
        user_id="12345678-1234-5678-1234-567812345678",
        session=mock_session
    )

    assert result["status"] == "error"
    assert "Failed to delete task" in result["message"]
    mock_session.rollback.assert_called_once()


def test_update_task_success():
    """Test successful task update"""
    mock_session = Mock(spec=Session)
    mock_task = Mock()
    mock_task.id = 1
    mock_task.title = "Old Title"
    mock_task.description = "Old Description"
    mock_task.completed = False
    mock_task.user_id = UUID("12345678-1234-5678-1234-567812345678")

    mock_result = Mock()
    mock_result.first.return_value = mock_task
    mock_session.exec = Mock(return_value=mock_result)
    mock_session.add = Mock()
    mock_session.commit = Mock()
    mock_session.refresh = Mock()

    result = update_task(
        task_id=1,
        user_id="12345678-1234-5678-1234-567812345678",
        title="New Title",
        description="New Description",
        completed=True,
        session=mock_session
    )

    assert result["status"] == "success"
    assert result["task_id"] == 1
    assert "updated successfully" in result["message"]

    # Verify task was updated
    assert mock_task.title == "New Title"
    assert mock_task.description == "New Description"
    assert mock_task.completed is True

    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()


def test_update_task_partial_updates():
    """Test updating only some fields of a task"""
    mock_session = Mock(spec=Session)
    mock_task = Mock()
    mock_task.id = 1
    mock_task.title = "Original Title"
    mock_task.description = "Original Description"
    mock_task.completed = False
    mock_task.user_id = UUID("12345678-1234-5678-1234-567812345678")

    mock_result = Mock()
    mock_result.first.return_value = mock_task
    mock_session.exec = Mock(return_value=mock_result)
    mock_session.add = Mock()
    mock_session.commit = Mock()
    mock_session.refresh = Mock()

    result = update_task(
        task_id=1,
        user_id="12345678-1234-5678-1234-567812345678",
        title="Updated Title",
        session=mock_session  # Only updating title, not description or completion status
    )

    assert result["status"] == "success"
    assert mock_task.title == "Updated Title"
    # Description and completion status should remain unchanged
    assert mock_task.description == "Original Description"
    assert mock_task.completed is False


def test_update_task_not_found():
    """Test updating a task that doesn't exist"""
    mock_session = Mock(spec=Session)
    mock_result = Mock()
    mock_result.first.return_value = None
    mock_session.exec = Mock(return_value=mock_result)

    result = update_task(
        task_id=999,
        user_id="12345678-1234-5678-1234-567812345678",
        title="New Title",
        session=mock_session
    )

    assert result["status"] == "error"
    assert "not found" in result["message"]


def test_update_task_exception_handling():
    """Test exception handling in update_task"""
    mock_session = Mock(spec=Session)
    mock_session.exec.side_effect = Exception("Database error")
    mock_session.rollback = Mock()

    result = update_task(
        task_id=1,
        user_id="12345678-1234-5678-1234-567812345678",
        title="New Title",
        session=mock_session
    )

    assert result["status"] == "error"
    assert "Failed to update task" in result["message"]
    mock_session.rollback.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__])