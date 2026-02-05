"""
Test that natural language examples from specification work correctly
Testing T054: Test all natural language examples from specification work correctly in phase-3/backend
"""
import pytest
import os
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from sqlmodel import Session, create_engine, select
from sqlmodel.pool import StaticPool
from uuid import uuid4

# Import the main app
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from main import app
from src.database.database import get_session
from src.models.user import User
from src.models.conversation import Conversation
from src.models.message import Message
from src.models.task import Task


@pytest.fixture
def mock_db_session():
    """Create a mock database session for testing"""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    # Create tables
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session


@pytest.fixture
def client(mock_db_session):
    """Create a test client with mocked database session"""
    def get_test_session():
        return mock_db_session

    app.dependency_overrides[get_session] = get_test_session
    with TestClient(app) as test_client:
        yield test_client

    # Clean up overrides
    app.dependency_overrides.clear()


def test_add_task_natural_language_example(client, mock_db_session):
    """
    Test the natural language example: "Add task: Buy milk"
    From specification: Enable users to manage tasks using natural language commands like "Add task: Buy milk"
    """
    # Create a test user
    user = User(
        id=uuid4(),
        email="test@example.com",
        password_hash="hashed_password",
        name="Test User"
    )
    mock_db_session.add(user)
    mock_db_session.commit()

    # Mock Cohere response for adding a task
    mock_add_response = MagicMock()
    mock_add_response.text = "I've added the task 'Buy milk' to your list."

    # Mock the tool call
    mock_tool_call = MagicMock()
    mock_tool_call.name = "add_task"
    mock_tool_call.parameters = {"title": "Buy milk", "user_id": str(user.id)}
    mock_add_response.tool_calls = [mock_tool_call]

    # Mock final response
    mock_final_response = MagicMock()
    mock_final_response.text = "I've added the task 'Buy milk' to your list."
    mock_final_response.tool_calls = []

    with patch('agents.cohere_agent.get_cohere_client') as mock_get_client:
        mock_client = MagicMock()
        mock_client.chat.side_effect = [mock_add_response, mock_final_response]
        mock_get_client.return_value = mock_client

        # Mock JWT decoding
        with patch('src.auth.jwt.decode_jwt', return_value={"user_id": str(user.id)}):
            headers = {"Authorization": "Bearer fake-jwt-token"}

            # Test the natural language command
            response = client.post(
                "/api/chat",
                json={"message": "Add task: Buy milk"},
                headers=headers
            )

            # Verify API response
            assert response.status_code == 200
            data = response.json()
            assert "Buy milk" in data["response"]
            assert data["status"] == "success"

            # Verify task was created in database
            tasks = mock_db_session.exec(select(Task).where(Task.user_id == user.id)).all()
            assert len(tasks) == 1
            assert tasks[0].title == "Buy milk"


def test_show_pending_tasks_natural_language_example(client, mock_db_session):
    """
    Test the natural language example: "Show me pending tasks"
    From specification: Enable users to manage tasks using natural language commands like "Show me pending tasks"
    """
    # Create a test user
    user = User(
        id=uuid4(),
        email="test@example.com",
        password_hash="hashed_password",
        name="Test User"
    )
    mock_db_session.add(user)
    mock_db_session.commit()

    # Create a pending task in the database
    pending_task = Task(
        title="Buy milk",
        description="Get dairy products",
        completed=False,
        user_id=user.id
    )
    mock_db_session.add(pending_task)
    mock_db_session.commit()

    # Mock Cohere response for listing tasks
    mock_list_response = MagicMock()
    mock_list_response.text = "You have 1 pending task: Buy milk"

    # Mock the tool call
    mock_tool_call = MagicMock()
    mock_tool_call.name = "list_tasks"
    mock_tool_call.parameters = {"status": "pending", "user_id": str(user.id)}
    mock_list_response.tool_calls = [mock_tool_call]

    # Mock final response
    mock_final_response = MagicMock()
    mock_final_response.text = "You have 1 pending task: Buy milk"
    mock_final_response.tool_calls = []

    with patch('agents.cohere_agent.get_cohere_client') as mock_get_client:
        mock_client = MagicMock()
        mock_client.chat.side_effect = [mock_list_response, mock_final_response]
        mock_get_client.return_value = mock_client

        # Mock JWT decoding
        with patch('src.auth.jwt.decode_jwt', return_value={"user_id": str(user.id)}):
            headers = {"Authorization": "Bearer fake-jwt-token"}

            # Test the natural language command
            response = client.post(
                "/api/chat",
                json={"message": "Show me pending tasks"},
                headers=headers
            )

            # Verify API response
            assert response.status_code == 200
            data = response.json()
            assert "pending task" in data["response"].lower()
            assert "buy milk" in data["response"].lower()
            assert data["status"] == "success"


def test_complete_task_natural_language_example(client, mock_db_session):
    """
    Test the natural language example: "Complete task 1"
    From specification: Enable users to manage tasks using natural language commands like "Complete task 1"
    """
    # Create a test user and a task
    user = User(
        id=uuid4(),
        email="test@example.com",
        password_hash="hashed_password",
        name="Test User"
    )
    mock_db_session.add(user)
    mock_db_session.commit()

    task = Task(
        title="Buy milk",
        description="Get dairy products",
        completed=False,
        user_id=user.id
    )
    mock_db_session.add(task)
    mock_db_session.commit()

    # Mock Cohere response for completing a task
    mock_complete_response = MagicMock()
    mock_complete_response.text = "I've marked task 'Buy milk' as completed."

    # Mock the tool call
    mock_tool_call = MagicMock()
    mock_tool_call.name = "complete_task"
    mock_tool_call.parameters = {"task_id": task.id, "user_id": str(user.id)}
    mock_complete_response.tool_calls = [mock_tool_call]

    # Mock final response
    mock_final_response = MagicMock()
    mock_final_response.text = "I've marked task 'Buy milk' as completed."
    mock_final_response.tool_calls = []

    with patch('agents.cohere_agent.get_cohere_client') as mock_get_client:
        mock_client = MagicMock()
        mock_client.chat.side_effect = [mock_complete_response, mock_final_response]
        mock_get_client.return_value = mock_client

        # Mock JWT decoding
        with patch('src.auth.jwt.decode_jwt', return_value={"user_id": str(user.id)}):
            headers = {"Authorization": "Bearer fake-jwt-token"}

            # Test the natural language command
            response = client.post(
                "/api/chat",
                json={"message": f"Complete task {task.id}"},
                headers=headers
            )

            # Verify API response
            assert response.status_code == 200
            data = response.json()
            assert "completed" in data["response"].lower()
            assert "buy milk" in data["response"].lower()
            assert data["status"] == "success"

            # Verify task was updated in database
            updated_task = mock_db_session.get(Task, task.id)
            assert updated_task is not None
            assert updated_task.completed is True


def test_specification_example_variations(client, mock_db_session):
    """
    Test variations of the specification examples to ensure robustness
    """
    # Create a test user
    user = User(
        id=uuid4(),
        email="test@example.com",
        password_hash="hashed_password",
        name="Test User"
    )
    mock_db_session.add(user)
    mock_db_session.commit()

    # Test various ways to add a task
    variations = [
        "Add a task: Buy groceries",
        "Create task: Walk the dog",
        "Add task - Pay bills",
        "I want to add a task: Clean the house",
        "New task: Call mom"
    ]

    for i, variation in enumerate(variations):
        # Mock Cohere response
        mock_response = MagicMock()
        mock_response.text = f"I've added the task for you."

        # Mock the tool call - extract task name from variation
        task_title = variation.split(':')[-1].split('-')[-1].strip() if ':' in variation or '-' in variation else "Generic task"

        mock_tool_call = MagicMock()
        mock_tool_call.name = "add_task"
        mock_tool_call.parameters = {"title": task_title, "user_id": str(user.id)}
        mock_response.tool_calls = [mock_tool_call]

        mock_final_response = MagicMock()
        mock_final_response.text = f"I've added the task '{task_title}'."
        mock_final_response.tool_calls = []

        with patch('agents.cohere_agent.get_cohere_client') as mock_get_client:
            mock_client = MagicMock()
            mock_client.chat.side_effect = [mock_response, mock_final_response]
            mock_get_client.return_value = mock_client

            # Mock JWT decoding
            with patch('src.auth.jwt.decode_jwt', return_value={"user_id": str(user.id)}):
                headers = {"Authorization": "Bearer fake-jwt-token"}

                response = client.post(
                    "/api/chat",
                    json={"message": variation},
                    headers=headers
                )

                assert response.status_code == 200
                data = response.json()
                assert data["status"] == "success"


def test_multiple_specification_examples_sequence(client, mock_db_session):
    """
    Test a sequence of specification examples to ensure they work together
    """
    # Create a test user
    user = User(
        id=uuid4(),
        email="test@example.com",
        password_hash="hashed_password",
        name="Test User"
    )
    mock_db_session.add(user)
    mock_db_session.commit()

    with patch('agents.cohere_agent.get_cohere_client') as mock_get_client:
        mock_client = MagicMock()

        # Create different responses for different requests
        def mock_chat_side_effect(message=None, **kwargs):
            msg_content = kwargs.get('message', '')

            if 'add' in msg_content.lower() and ('task' in msg_content.lower()):
                # Response for adding a task
                mock_resp = MagicMock()
                mock_resp.text = "I've added the task for you."

                # Extract task title from message
                import re
                match = re.search(r'(?:add|create).*?(?:task[s]?[:,\s-]+)(.+)', msg_content, re.IGNORECASE)
                task_title = match.group(1).strip() if match else "Generic task"

                mock_tool_call = MagicMock()
                mock_tool_call.name = "add_task"
                mock_tool_call.parameters = {"title": task_title, "user_id": str(user.id)}
                mock_resp.tool_calls = [mock_tool_call]

                final_resp = MagicMock()
                final_resp.text = f"I've added the task '{task_title}'."
                final_resp.tool_calls = []
                return final_resp
            elif 'show' in msg_content.lower() and ('pending' in msg_content.lower() or 'task' in msg_content.lower()):
                # Response for showing tasks
                mock_resp = MagicMock()
                mock_resp.text = "You have 1 pending task: Buy groceries"

                mock_tool_call = MagicMock()
                mock_tool_call.name = "list_tasks"
                mock_tool_call.parameters = {"status": "pending", "user_id": str(user.id)}
                mock_resp.tool_calls = [mock_tool_call]

                final_resp = MagicMock()
                final_resp.text = "You have 1 pending task: Buy groceries"
                final_resp.tool_calls = []
                return final_resp
            else:
                # Generic response
                mock_resp = MagicMock()
                mock_resp.text = "I've processed your request."
                mock_resp.tool_calls = []
                return mock_resp

        mock_client.chat.side_effect = mock_chat_side_effect
        mock_get_client.return_value = mock_client

        # Mock JWT decoding
        with patch('src.auth.jwt.decode_jwt', return_value={"user_id": str(user.id)}):
            headers = {"Authorization": "Bearer fake-jwt-token"}

            # Step 1: Add a task using specification example
            response1 = client.post(
                "/api/chat",
                json={"message": "Add task: Buy groceries"},
                headers=headers
            )
            assert response1.status_code == 200

            # Step 2: Show pending tasks using specification example
            response2 = client.post(
                "/api/chat",
                json={"message": "Show me pending tasks"},
                headers=headers
            )
            assert response2.status_code == 200
            data2 = response2.json()
            assert "pending task" in data2["response"].lower()
            assert "buy groceries" in data2["response"].lower()


if __name__ == "__main__":
    pytest.main([__file__])