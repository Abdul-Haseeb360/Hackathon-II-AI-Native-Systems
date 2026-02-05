"""
End-to-end test for natural language → tool calls → database operations flow
Task T027: Test end-to-end flow: natural language → tool calls → database operations in phase-3/backend
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


def test_end_to_end_natural_language_flow(client, mock_db_session):
    """
    Test the complete flow: natural language → tool calls → database operations
    This tests T027: Test end-to-end flow: natural language → tool calls → database operations
    """
    # 1. Create a test user
    user = User(
        id=uuid4(),
        email="test@example.com",
        password_hash="hashed_password",
        name="Test User"
    )
    mock_db_session.add(user)
    mock_db_session.commit()

    # 2. Mock Cohere responses for the complete flow
    # First, mock the response when adding a task
    mock_add_task_response = MagicMock()
    mock_add_task_response.text = "I've added the task 'Buy groceries' to your list."

    # Mock a tool call to add_task
    mock_tool_call = MagicMock()
    mock_tool_call.name = "add_task"
    mock_tool_call.parameters = {"title": "Buy groceries", "user_id": str(user.id)}

    # Set up the tool call in the response
    mock_add_task_response.tool_calls = [mock_tool_call]

    # Mock the final response after tool execution
    mock_final_response = MagicMock()
    mock_final_response.text = "I've added the task 'Buy groceries' to your list."
    mock_final_response.tool_calls = []

    # 3. Mock Cohere client to simulate the complete interaction
    with patch('agents.cohere_agent.get_cohere_client') as mock_get_client:
        mock_client = MagicMock()

        # For the first call (which triggers tool call), return response with tool call
        # For the second call (after tool execution), return final response
        mock_client.chat.side_effect = [mock_add_task_response, mock_final_response]
        mock_get_client.return_value = mock_client

        # 4. Mock JWT decoding to authenticate the user
        with patch('src.auth.jwt.decode_jwt', return_value={"user_id": str(user.id)}):
            headers = {"Authorization": "Bearer fake-jwt-token"}

            # 5. Send a natural language request to add a task
            response = client.post(
                "/api/chat",
                json={"message": "Add a task: Buy groceries"},
                headers=headers
            )

            # 6. Verify the API response
            assert response.status_code == 200
            data = response.json()
            assert "response" in data
            assert "Buy groceries" in data["response"]
            assert data["status"] == "success"
            assert "conversation_id" in data

            # 7. Verify that the task was actually created in the database
            # Check if a task exists for this user
            created_tasks = mock_db_session.exec(select(Task).where(Task.user_id == user.id)).all()
            assert len(created_tasks) == 1
            assert created_tasks[0].title == "Buy groceries"
            assert created_tasks[0].completed is False

            # 8. Verify conversation was created
            conversations = mock_db_session.exec(
                select(Conversation).where(Conversation.user_id == user.id)
            ).all()
            assert len(conversations) == 1

            # 9. Verify messages were saved
            messages = mock_db_session.exec(
                select(Message).where(Message.conversation_id == conversations[0].id)
            ).all()
            assert len(messages) == 2  # User message + Assistant response


def test_end_to_end_list_tasks_flow(client, mock_db_session):
    """
    Test the flow for listing tasks: natural language → tool calls → database operations
    """
    # 1. Create a test user
    user = User(
        id=uuid4(),
        email="test@example.com",
        password_hash="hashed_password",
        name="Test User"
    )
    mock_db_session.add(user)
    mock_db_session.commit()

    # 2. Create some test tasks in the database
    task1 = Task(
        title="Buy groceries",
        description="Get milk and bread",
        completed=False,
        user_id=user.id
    )
    task2 = Task(
        title="Walk the dog",
        description="Evening walk",
        completed=True,
        user_id=user.id
    )
    mock_db_session.add(task1)
    mock_db_session.add(task2)
    mock_db_session.commit()

    # 3. Mock Cohere responses for listing tasks
    mock_list_response = MagicMock()
    mock_list_response.text = "Here are your pending tasks: Buy groceries"

    # Mock a tool call to list_tasks
    mock_tool_call = MagicMock()
    mock_tool_call.name = "list_tasks"
    mock_tool_call.parameters = {"status": "pending", "user_id": str(user.id)}
    mock_list_response.tool_calls = [mock_tool_call]

    # Mock final response
    mock_final_response = MagicMock()
    mock_final_response.text = "Here are your pending tasks: Buy groceries"
    mock_final_response.tool_calls = []

    with patch('agents.cohere_agent.get_cohere_client') as mock_get_client:
        mock_client = MagicMock()
        mock_client.chat.side_effect = [mock_list_response, mock_final_response]
        mock_get_client.return_value = mock_client

        # Mock JWT decoding
        with patch('src.auth.jwt.decode_jwt', return_value={"user_id": str(user.id)}):
            headers = {"Authorization": "Bearer fake-jwt-token"}

            # Send a natural language request to list tasks
            response = client.post(
                "/api/chat",
                json={"message": "Show me my pending tasks"},
                headers=headers
            )

            # Verify the response
            assert response.status_code == 200
            data = response.json()
            assert "pending tasks" in data["response"].lower()
            assert "Buy groceries" in data["response"]


def test_end_to_end_complete_task_flow(client, mock_db_session):
    """
    Test the flow for completing a task: natural language → tool calls → database operations
    """
    # 1. Create a test user and a task
    user = User(
        id=uuid4(),
        email="test@example.com",
        password_hash="hashed_password",
        name="Test User"
    )
    mock_db_session.add(user)
    mock_db_session.commit()

    task = Task(
        title="Buy groceries",
        description="Get milk and bread",
        completed=False,
        user_id=user.id
    )
    mock_db_session.add(task)
    mock_db_session.commit()

    # 2. Mock Cohere responses for completing a task
    mock_complete_response = MagicMock()
    mock_complete_response.text = "I've marked the task 'Buy groceries' as completed."

    # Mock a tool call to complete_task
    mock_tool_call = MagicMock()
    mock_tool_call.name = "complete_task"
    mock_tool_call.parameters = {"task_id": task.id, "user_id": str(user.id)}
    mock_complete_response.tool_calls = [mock_tool_call]

    # Mock final response
    mock_final_response = MagicMock()
    mock_final_response.text = "I've marked the task 'Buy groceries' as completed."
    mock_final_response.tool_calls = []

    with patch('agents.cohere_agent.get_cohere_client') as mock_get_client:
        mock_client = MagicMock()
        mock_client.chat.side_effect = [mock_complete_response, mock_final_response]
        mock_get_client.return_value = mock_client

        # Mock JWT decoding
        with patch('src.auth.jwt.decode_jwt', return_value={"user_id": str(user.id)}):
            headers = {"Authorization": "Bearer fake-jwt-token"}

            # Send a natural language request to complete a task
            response = client.post(
                "/api/chat",
                json={"message": f"Complete task {task.id}"},
                headers=headers
            )

            # Verify the response
            assert response.status_code == 200
            data = response.json()
            assert "completed" in data["response"].lower()
            assert "Buy groceries" in data["response"]

            # Verify that the task was actually updated in the database
            updated_task = mock_db_session.get(Task, task.id)
            assert updated_task is not None
            assert updated_task.completed is True


def test_multiple_operations_in_single_conversation(client, mock_db_session):
    """
    Test multiple operations in a single conversation flow
    """
    # 1. Create a test user
    user = User(
        id=uuid4(),
        email="test@example.com",
        password_hash="hashed_password",
        name="Test User"
    )
    mock_db_session.add(user)
    mock_db_session.commit()

    # 2. First request: Add a task
    mock_add_response = MagicMock()
    mock_add_response.text = "I've added the task 'Buy groceries' to your list."

    mock_add_tool_call = MagicMock()
    mock_add_tool_call.name = "add_task"
    mock_add_tool_call.parameters = {"title": "Buy groceries", "user_id": str(user.id)}
    mock_add_response.tool_calls = [mock_add_tool_call]

    mock_add_final_response = MagicMock()
    mock_add_final_response.text = "I've added the task 'Buy groceries' to your list."
    mock_add_final_response.tool_calls = []

    with patch('agents.cohere_agent.get_cohere_client') as mock_get_client:
        mock_client = MagicMock()

        # Mock different responses based on the message
        def side_effect_func(*args, **kwargs):
            message = kwargs.get('message', '')
            if 'add' in message.lower() or 'Buy groceries' in message:
                if not hasattr(side_effect_func, 'call_count'):
                    side_effect_func.call_count = 0
                side_effect_func.call_count += 1
                if side_effect_func.call_count <= 2:  # First call triggers tool, second is final response
                    if side_effect_func.call_count == 1:
                        return mock_add_response
                    else:
                        return mock_add_final_response
            # For other messages, return a generic response
            mock_generic_response = MagicMock()
            mock_generic_response.text = "Okay, I've processed your request."
            mock_generic_response.tool_calls = []
            return mock_generic_response

        mock_client.chat.side_effect = side_effect_func
        mock_get_client.return_value = mock_client

        # Mock JWT decoding
        with patch('src.auth.jwt.decode_jwt', return_value={"user_id": str(user.id)}):
            headers = {"Authorization": "Bearer fake-jwt-token"}

            # First request: Add a task
            response1 = client.post(
                "/api/chat",
                json={"message": "Add a task: Buy groceries"},
                headers=headers
            )

            assert response1.status_code == 200

            # Verify the task was created
            tasks = mock_db_session.exec(select(Task).where(Task.user_id == user.id)).all()
            assert len(tasks) == 1
            assert tasks[0].title == "Buy groceries"


if __name__ == "__main__":
    pytest.main([__file__])