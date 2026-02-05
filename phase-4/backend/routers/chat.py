"""
Chat API router for AI chatbot functionality
"""
import logging
import re
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from typing import Optional
from src.auth.dependencies import get_current_user_id
from pydantic import BaseModel, validator
from uuid import UUID
from sqlmodel import Session, select
from src.models.conversation import Conversation
from src.models.message import Message
from src.database.database import engine
from agents.cohere_agent import get_cohere_agent

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["chat"])

security = HTTPBearer()


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[int] = None
    metadata: Optional[dict] = None

    @validator('message')
    def validate_message(cls, v):
        if not v or not v.strip():
            raise ValueError('Message cannot be empty')

        # Sanitize input to prevent injection attacks
        sanitized = re.sub(r'[<>\'";]', '', v)  # Basic sanitization

        # Check for potential harmful patterns
        harmful_patterns = [
            r'javascript:',
            r'on\w+\s*=',
            r'<script',
            r'eval\s*\(',
            r'exec\s*\('
        ]

        for pattern in harmful_patterns:
            if re.search(pattern, sanitized, re.IGNORECASE):
                raise ValueError('Message contains prohibited content')

        if len(sanitized) > 1000:  # Limit message length
            raise ValueError('Message is too long (max 1000 characters)')

        return sanitized


class ChatResponse(BaseModel):
    response: str
    conversation_id: int
    status: str
    tool_calls: Optional[list] = None
    tool_results: Optional[list] = None


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Main chat endpoint that processes natural language messages and returns AI responses
    with potential tool calls for task operations.

    Args:
        request: Chat request containing the user message and optional conversation_id
        current_user_id: User ID extracted from JWT token

    Returns:
        ChatResponse containing AI response and conversation information
    """
    import time
    start_time = time.time()

    try:
        logger.info(f"Processing chat request for user {current_user_id}, conversation {request.conversation_id}")

        # Create database session
        with Session(engine) as session:
            # Get or create conversation
            if request.conversation_id:
                # Try to get existing conversation
                conversation_stmt = select(Conversation).where(
                    Conversation.id == request.conversation_id,
                    Conversation.user_id == UUID(current_user_id)
                )
                conversation = session.exec(conversation_stmt).first()

                if not conversation:
                    logger.warning(f"Conversation {request.conversation_id} not found for user {current_user_id}")
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Conversation not found or doesn't belong to user"
                    )
            else:
                # Create new conversation
                title = request.message[:50] + "..." if len(request.message) > 50 else request.message
                conversation = Conversation(
                    user_id=UUID(current_user_id),
                    title=title
                )
                session.add(conversation)
                session.commit()
                session.refresh(conversation)
                logger.info(f"Created new conversation {conversation.id} for user {current_user_id}")

            # Get conversation history for context
            history_stmt = select(Message).where(
                Message.conversation_id == conversation.id
            ).order_by(Message.created_at)
            history_records = session.exec(history_stmt).all()

            # Format conversation history for the agent
            conversation_history = [
                {
                    "role": msg.role,
                    "content": msg.content
                }
                for msg in history_records
            ]

            # Save user message to conversation
            user_message = Message(
                conversation_id=conversation.id,
                role="user",
                content=request.message
            )
            session.add(user_message)
            session.commit()

            # Process the message with the Cohere agent
            agent = get_cohere_agent()
            result = agent.process_message(
                message=request.message,
                user_id=current_user_id,
                conversation_history=conversation_history
            )

            # Check if the response took too long (performance monitoring)
            processing_time = time.time() - start_time
            if processing_time > 5.0:  # More than 5 seconds
                logger.warning(f"Slow response for user {current_user_id}: {processing_time:.2f}s")

            # Save assistant response to conversation
            assistant_message = Message(
                conversation_id=conversation.id,
                role="assistant",
                content=result.get('response', ''),
                tool_calls=result.get('tool_calls'),
                tool_results=result.get('tool_results')
            )
            session.add(assistant_message)
            session.commit()

            # Prepare response
            response_data = {
                "response": result.get('response', 'No response generated'),
                "conversation_id": conversation.id,
                "status": result.get('status', 'success')
            }

            if 'tool_calls' in result:
                response_data['tool_calls'] = result['tool_calls']
            if 'tool_results' in result:
                response_data['tool_results'] = result['tool_results']

            logger.info(f"Successfully processed chat request for user {current_user_id} in {processing_time:.2f}s")
            return ChatResponse(**response_data)

    except HTTPException as http_exc:
        processing_time = time.time() - start_time
        logger.error(f"HTTP error in chat endpoint for user {current_user_id}: {http_exc.detail} after {processing_time:.2f}s")
        raise
    except Exception as e:
        processing_time = time.time() - start_time
        logger.error(f"Unexpected error in chat endpoint for user {current_user_id}: {str(e)} after {processing_time:.2f}s")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing chat request: {str(e)}"
        )


@router.get("/conversations")
async def get_user_conversations(
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Get list of conversations for the current user

    Args:
        current_user_id: User ID extracted from JWT token

    Returns:
        List of user's conversations
    """
    try:
        with Session(engine) as session:
            conversations_stmt = select(Conversation).where(
                Conversation.user_id == UUID(current_user_id)
            ).order_by(Conversation.created_at.desc())

            conversations = session.exec(conversations_stmt).all()

            return {
                "conversations": [
                    {
                        "id": conv.id,
                        "title": conv.title,
                        "created_at": conv.created_at.isoformat(),
                        "updated_at": conv.updated_at.isoformat()
                    }
                    for conv in conversations
                ]
            }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving conversations: {str(e)}"
        )


@router.delete("/conversations/{conversation_id}")
async def delete_conversation(
    conversation_id: int,
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Delete a specific conversation for the current user

    Args:
        conversation_id: ID of the conversation to delete
        current_user_id: User ID extracted from JWT token

    Returns:
        Deletion confirmation
    """
    try:
        with Session(engine) as session:
            # Check if conversation exists and belongs to user
            conversation_stmt = select(Conversation).where(
                Conversation.id == conversation_id,
                Conversation.user_id == UUID(current_user_id)
            )
            conversation = session.exec(conversation_stmt).first()

            if not conversation:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Conversation not found or doesn't belong to user"
                )

            # Delete the conversation (and associated messages due to FK constraints)
            session.delete(conversation)
            session.commit()

            return {"message": f"Conversation {conversation_id} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting conversation: {str(e)}"
        )