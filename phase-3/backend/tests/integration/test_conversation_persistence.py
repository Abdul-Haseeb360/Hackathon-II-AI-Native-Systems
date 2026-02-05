"""
Integration tests for conversation persistence across page refreshes and browser sessions
Testing T034 and T035:
- T034 [US2] Test multi-turn conversation persistence across page refreshes in phase-3/backend
- T035 [US2] Test conversation continuity in new browser sessions in phase-3/backend
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
import time
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


def test_conversation_persistence_across_page_refreshes(client, mock_db_session):
    """
    Test T034: Multi-turn conversation persistence across page refreshes
    This simulates a user having a conversation, refreshing the page, and continuing
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

    # 2. Mock Cohere responses for multiple exchanges
    responses = [
        # First exchange - user says "Hello"
        MagicMock(text="Hello! How can I help you?", tool_calls=[]),
        # Second exchange - user adds a task
        MagicMock(text="I've added the task 'Buy groceries'.", tool_calls=[
            MagicMock(name="add_task", parameters={"title": "Buy groceries", "user_id": str(user.id)})
        ]),
        # Third exchange - user asks to see tasks
        MagicMock(text="You have one task: Buy groceries", tool_calls=[
            MagicMock(name="list_tasks", parameters={"user_id": str(user.id)})
        ])
    ]

    with patch('agents.cohere_agent.get_cohere_client') as mock_get_client:
        mock_client = MagicMock()
        mock_client.chat.side_effect = responses
        mock_get_client.return_value = mock_client

        # Mock JWT decoding
        with patch('src.auth.jwt.decode_jwt', return_value={"user_id": str(user.id)}):
            headers = {"Authorization": "Bearer fake-jwt-token"}

            # First exchange: Say hello
            response1 = client.post(
                "/api/chat",
                json={"message": "Hello"},
                headers=headers
            )
            assert response1.status_code == 200
            data1 = response1.json()
            conversation_id = data1["conversation_id"]
            assert conversation_id > 0

            # Second exchange: Add a task (same conversation)
            response2 = client.post(
                "/api/chat",
                json={
                    "message": "Add a task: Buy groceries",
                    "conversation_id": conversation_id
                },
                headers=headers
            )
            assert response2.status_code == 200
            data2 = response2.json()
            assert data2["conversation_id"] == conversation_id  # Same conversation

            # Third exchange: List tasks (still same conversation, simulating page refresh)
            response3 = client.post(
                "/api/chat",
                json={
                    "message": "What tasks do I have?",
                    "conversation_id": conversation_id
                },
                headers=headers
            )
            assert response3.status_code == 200
            data3 = response3.json()
            assert data3["conversation_id"] == conversation_id  # Still same conversation

            # Verify that all messages are in the same conversation
            messages = mock_db_session.exec(
                select(Message).where(Message.conversation_id == conversation_id)
            ).all()
            assert len(messages) == 6  # 3 user messages + 3 assistant responses

            # Verify that the conversation exists and has the right user
            conversation = mock_db_session.get(Conversation, conversation_id)
            assert conversation is not None
            assert conversation.user_id == user.id


def test_conversation_continuity_new_browser_sessions(client, mock_db_session):
    """
    Test T035: Conversation continuity in new browser sessions
    This tests that users can return to a conversation in a new browser session
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

    # 2. Start a conversation and add some messages
    initial_responses = [
        MagicMock(text="Hello! How can I help you?", tool_calls=[]),
        MagicMock(text="I've added the task 'Buy groceries'.", tool_calls=[
            MagicMock(name="add_task", parameters={"title": "Buy groceries", "user_id": str(user.id)})
        ])
    ]

    with patch('agents.cohere_agent.get_cohere_client') as mock_get_client:
        mock_client = MagicMock()
        mock_client.chat.side_effect = initial_responses
        mock_get_client.return_value = mock_client

        # Mock JWT decoding
        with patch('src.auth.jwt.decode_jwt', return_value={"user_id": str(user.id)}):
            headers = {"Authorization": "Bearer fake-jwt-token"}

            # Start a conversation
            response1 = client.post(
                "/api/chat",
                json={"message": "Hello"},
                headers=headers
            )
            assert response1.status_code == 200
            initial_conversation_data = response1.json()
            initial_conversation_id = initial_conversation_data["conversation_id"]

            # Add a task to the conversation
            response2 = client.post(
                "/api/chat",
                json={
                    "message": "Add a task: Buy groceries",
                    "conversation_id": initial_conversation_id
                },
                headers=headers
            )
            assert response2.status_code == 200

    # 3. Simulate a new browser session by creating a new client instance
    # but with the same database session (to test persistence)
    with patch('agents.cohere_agent.get_cohere_client') as mock_get_client:
        mock_client = MagicMock()

        # Response for when user returns to the conversation
        follow_up_response = MagicMock()
        follow_up_response.text = "You have one task: Buy groceries"
        follow_up_response.tool_calls = [
            MagicMock(name="list_tasks", parameters={"user_id": str(user.id)})
        ]
        mock_client.chat.return_value = follow_up_response
        mock_get_client.return_value = mock_client

        # Mock JWT decoding for the "new session"
        with patch('src.auth.jwt.decode_jwt', return_value={"user_id": str(user.id)}):
            headers = {"Authorization": "Bearer fake-jwt-token"}

            # User returns to the same conversation in a "new session"
            response3 = client.post(
                "/api/chat",
                json={
                    "message": "What tasks do I have?",
                    "conversation_id": initial_conversation_id
                },
                headers=headers
            )
            assert response3.status_code == 200
            data3 = response3.json()
            assert data3["conversation_id"] == initial_conversation_id

            # Verify that the conversation still exists and has all messages
            messages = mock_db_session.exec(
                select(Message).where(Message.conversation_id == initial_conversation_id)
            ).all()
            assert len(messages) >= 3  # At least the messages from both "sessions"

            # Verify conversation details
            conversation = mock_db_session.get(Conversation, initial_conversation_id)
            assert conversation is not None
            assert conversation.user_id == user.id


def test_conversation_history_loading_for_context(client, mock_db_session):
    """
    Test that conversation history is properly loaded and provided as context
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

    # 2. Create an existing conversation with messages
    conversation = Conversation(
        user_id=user.id,
        title="Test Conversation"
    )
    mock_db_session.add(conversation)
    mock_db_session.commit()

    # Add some messages to the conversation
    user_message = Message(
        conversation_id=conversation.id,
        role="user",
        content="I want to add a task: Buy groceries"
    )
    assistant_message = Message(
        conversation_id=conversation.id,
        role="assistant",
        content="I've added the task 'Buy groceries'."
    )
    mock_db_session.add(user_message)
    mock_db_session.add(assistant_message)
    mock_db_session.commit()

    # 3. Mock Cohere response for follow-up message
    follow_up_response = MagicMock()
    follow_up_response.text = "You have one task: Buy groceries. Would you like me to add another?"
    follow_up_response.tool_calls = [
        MagicMock(name="list_tasks", parameters={"user_id": str(user.id)})
    ]

    with patch('agents.cohere_agent.get_cohere_client') as mock_get_client:
        mock_client = MagicMock()
        mock_client.chat.return_value = follow_up_response
        mock_get_client.return_value = mock_client

        # Mock JWT decoding
        with patch('src.auth.jwt.decode_jwt', return_value={"user_id": str(user.id)}):
            headers = {"Authorization": "Bearer fake-jwt-token"}

            # Continue the conversation with history context
            response = client.post(
                "/api/chat",
                json={
                    "message": "What tasks do I have?",
                    "conversation_id": conversation.id
                },
                headers=headers
            )
            assert response.status_code == 200
            data = response.json()
            assert data["conversation_id"] == conversation.id

            # Verify that the response acknowledges the existing task
            assert "groceries" in data["response"].lower() or "task" in data["response"].lower()


def test_conversation_isolation_between_users(client, mock_db_session):
    """
    Test that conversations are properly isolated between different users
    """
    # 1. Create two test users
    user1 = User(
        id=uuid4(),
        email="user1@example.com",
        password_hash="hashed_password",
        name="User 1"
    )
    user2 = User(
        id=uuid4(),
        email="user2@example.com",
        password_hash="hashed_password",
        name="User 2"
    )
    mock_db_session.add(user1)
    mock_db_session.add(user2)
    mock_db_session.commit()

    # 2. Create a conversation for user1
    conversation1 = Conversation(
        user_id=user1.id,
        title="User 1 Conversation"
    )
    mock_db_session.add(conversation1)
    mock_db_session.commit()

    # Add messages to user1's conversation
    user1_msg = Message(
        conversation_id=conversation1.id,
        role="user",
        content="My task is to buy groceries"
    )
    mock_db_session.add(user1_msg)
    mock_db_session.commit()

    # 3. Mock Cohere response
    response_mock = MagicMock()
    response_mock.text = "I can help you with that."
    response_mock.tool_calls = []

    with patch('agents.cohere_agent.get_cohere_client') as mock_get_client:
        mock_client = MagicMock()
        mock_client.chat.return_value = response_mock
        mock_get_client.return_value = mock_client

        # Test that user2 cannot access user1's conversation
        with patch('src.auth.jwt.decode_jwt', return_value={"user_id": str(user2.id)}):
            headers = {"Authorization": "Bearer fake-jwt-token"}

            # Try to access user1's conversation as user2
            response = client.post(
                "/api/chat",
                json={
                    "message": "What's in this conversation?",
                    "conversation_id": conversation1.id  # User2 trying to access User1's conversation
                },
                headers=headers
            )

            # Should return 404 since user2 doesn't own this conversation
            assert response.status_code == 404


if __name__ == "__main__":
    pytest.main([__file__])