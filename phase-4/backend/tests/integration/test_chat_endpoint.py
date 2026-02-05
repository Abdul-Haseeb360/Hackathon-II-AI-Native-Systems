"""
Integration tests for chat endpoint in phase-3/backend/routers/chat.py
"""
import pytest
import os
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from sqlmodel import Session, create_engine
from sqlmodel.pool import StaticPool

# Import the main app
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from main import app
from src.database.database import get_session
from src.models.user import User
from src.models.conversation import Conversation
from src.models.message import Message
from src.models.task import Task
from uuid import uuid4


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


def test_chat_endpoint_requires_auth(client):
    """Test that chat endpoint requires authentication"""
    response = client.post("/api/chat", json={"message": "Hello"})

    # Should return 401 or 403 since no auth token is provided
    assert response.status_code in [401, 403]


def test_chat_endpoint_with_valid_jwt(client, mock_db_session):
    """Test chat endpoint with valid JWT authentication"""
    # Create a mock user in the database
    user = User(
        id=uuid4(),
        email="test@example.com",
        password_hash="hashed_password",
        name="Test User"
    )
    mock_db_session.add(user)
    mock_db_session.commit()

    # Mock the Cohere agent response
    mock_response = MagicMock()
    mock_response.text = "Hello! How can I help you with your tasks?"
    mock_response.tool_calls = []

    with patch('agents.cohere_agent.get_cohere_client') as mock_get_client:
        mock_client = MagicMock()
        mock_client.chat.return_value = mock_response
        mock_get_client.return_value = mock_client

        # Mock JWT decoding to return our test user
        with patch('src.auth.jwt.decode_jwt', return_value={"user_id": str(user.id)}):
            headers = {"Authorization": "Bearer fake-jwt-token"}
            response = client.post(
                "/api/chat",
                json={"message": "Hello"},
                headers=headers
            )

            assert response.status_code == 200
            data = response.json()
            assert "response" in data
            assert "conversation_id" in data


def test_chat_endpoint_creates_conversation(client, mock_db_session):
    """Test that chat endpoint creates new conversation when none provided"""
    # Create a mock user in the database
    user = User(
        id=uuid4(),
        email="test@example.com",
        password_hash="hashed_password",
        name="Test User"
    )
    mock_db_session.add(user)
    mock_db_session.commit()

    # Mock the Cohere agent response
    mock_response = MagicMock()
    mock_response.text = "Sure, I can help you add that task."
    mock_response.tool_calls = []

    with patch('agents.cohere_agent.get_cohere_client') as mock_get_client:
        mock_client = MagicMock()
        mock_client.chat.return_value = mock_response
        mock_get_client.return_value = mock_client

        # Mock JWT decoding
        with patch('src.auth.jwt.decode_jwt', return_value={"user_id": str(user.id)}):
            headers = {"Authorization": "Bearer fake-jwt-token"}
            response = client.post(
                "/api/chat",
                json={"message": "Add a task: Buy groceries"},
                headers=headers
            )

            assert response.status_code == 200

            # Check that a conversation was created in the database
            conversations = mock_db_session.query(Conversation).filter_by(user_id=user.id).all()
            assert len(conversations) >= 1


def test_chat_endpoint_continues_existing_conversation(client, mock_db_session):
    """Test that chat endpoint continues an existing conversation when ID provided"""
    # Create a mock user in the database
    user = User(
        id=uuid4(),
        email="test@example.com",
        password_hash="hashed_password",
        name="Test User"
    )
    mock_db_session.add(user)
    mock_db_session.commit()

    # Create an existing conversation
    conversation = Conversation(
        user_id=user.id,
        title="Test Conversation"
    )
    mock_db_session.add(conversation)
    mock_db_session.commit()

    # Mock the Cohere agent response
    mock_response = MagicMock()
    mock_response.text = "Okay, I've continued our conversation."
    mock_response.tool_calls = []

    with patch('agents.cohere_agent.get_cohere_client') as mock_get_client:
        mock_client = MagicMock()
        mock_client.chat.return_value = mock_response
        mock_get_client.return_value = mock_client

        # Mock JWT decoding
        with patch('src.auth.jwt.decode_jwt', return_value={"user_id": str(user.id)}):
            headers = {"Authorization": "Bearer fake-jwt-token"}
            response = client.post(
                "/api/chat",
                json={
                    "message": "Continue our previous discussion",
                    "conversation_id": conversation.id
                },
                headers=headers
            )

            assert response.status_code == 200
            data = response.json()
            assert data["conversation_id"] == conversation.id


def test_chat_endpoint_processes_tool_calls(client, mock_db_session):
    """Test that chat endpoint processes tool calls from Cohere agent"""
    # Create a mock user in the database
    user = User(
        id=uuid4(),
        email="test@example.com",
        password_hash="hashed_password",
        name="Test User"
    )
    mock_db_session.add(user)
    mock_db_session.commit()

    # Mock a tool call response from Cohere
    mock_tool_call = MagicMock()
    mock_tool_call.name = "add_task"
    mock_tool_call.parameters = {"title": "Test Task", "user_id": str(user.id)}

    mock_response = MagicMock()
    mock_response.text = "I've added the task for you."
    mock_response.tool_calls = [mock_tool_call]

    # Mock the tool result
    mock_tool_result = {
        "status": "success",
        "task_id": 1,
        "message": "Task 'Test Task' added successfully"
    }

    with patch('agents.cohere_agent.get_cohere_client') as mock_get_client, \
         patch('tools.mcp_tools.add_task', return_value=mock_tool_result) as mock_add_task:

        mock_client = MagicMock()
        # Mock second response after tool call
        final_response = MagicMock()
        final_response.text = "I've added the task for you."
        final_response.tool_calls = []
        mock_client.chat.return_value = final_response  # Return final response after tool call

        mock_get_client.return_value = mock_client

        # Mock JWT decoding
        with patch('src.auth.jwt.decode_jwt', return_value={"user_id": str(user.id)}):
            headers = {"Authorization": "Bearer fake-jwt-token"}
            response = client.post(
                "/api/chat",
                json={"message": "Add a task: Test Task"},
                headers=headers
            )

            assert response.status_code == 200
            mock_add_task.assert_called_once()


def test_chat_endpoint_handles_invalid_request(client):
    """Test that chat endpoint handles invalid requests gracefully"""
    # Mock JWT decoding
    with patch('src.auth.jwt.decode_jwt', return_value={"user_id": str(uuid4())}):
        headers = {"Authorization": "Bearer fake-jwt-token"}
        response = client.post(
            "/api/chat",
            json={},  # Empty request body
            headers=headers
        )

        # Should return 422 for validation error or 400 for bad request
        assert response.status_code in [400, 422]


def test_chat_endpoint_handles_cohere_errors(client, mock_db_session):
    """Test that chat endpoint handles Cohere API errors gracefully"""
    # Create a mock user in the database
    user = User(
        id=uuid4(),
        email="test@example.com",
        password_hash="hashed_password",
        name="Test User"
    )
    mock_db_session.add(user)
    mock_db_session.commit()

    # Mock Cohere client to raise an exception
    with patch('agents.cohere_agent.get_cohere_client') as mock_get_client:
        mock_client = MagicMock()
        mock_client.chat.side_effect = Exception("Cohere API error")
        mock_get_client.return_value = mock_client

        # Mock JWT decoding
        with patch('src.auth.jwt.decode_jwt', return_value={"user_id": str(user.id)}):
            headers = {"Authorization": "Bearer fake-jwt-token"}
            response = client.post(
                "/api/chat",
                json={"message": "Hello"},
                headers=headers
            )

            # Should handle the error gracefully and return a proper response
            assert response.status_code == 500 or response.status_code == 200
            if response.status_code == 200:
                data = response.json()
                # The endpoint should catch the error and return an appropriate message


if __name__ == "__main__":
    pytest.main([__file__])