# AI Todo Chatbot API Documentation

## Overview
This API provides an AI-powered chat interface for managing todo tasks using natural language. The AI understands commands like "Add task: Buy groceries", "Show me pending tasks", and "Complete task 1".

## Authentication
All API endpoints require JWT authentication. Include the JWT token in the Authorization header:

```
Authorization: Bearer <jwt_token>
```

## Endpoints

### POST /api/chat
Send a message to the AI chatbot and receive a response with potential task operations.

#### Request Body
```json
{
  "message": "string (required) - The natural language message from the user",
  "conversation_id": "integer (optional) - ID of existing conversation to continue",
  "metadata": "object (optional) - Additional metadata for the request"
}
```

#### Response
```json
{
  "response": "string - AI-generated response",
  "conversation_id": "integer - ID of the conversation",
  "status": "string - Status of the operation (success, partial_success, error)",
  "tool_calls": "array (optional) - List of tools called by the AI",
  "tool_results": "array (optional) - Results from the tool calls"
}
```

#### Example Requests
- `"message": "Add task: Buy groceries"`
- `"message": "Show me pending tasks"`
- `"message": "Complete task 1"`
- `"message": "Delete task 3"`

#### Example Response
```json
{
  "response": "I've added the task 'Buy groceries' to your list.",
  "conversation_id": 123,
  "status": "success",
  "tool_calls": [
    {
      "name": "add_task",
      "parameters": {
        "title": "Buy groceries",
        "user_id": "abc-123"
      }
    }
  ],
  "tool_results": [
    {
      "call": {
        "name": "add_task",
        "parameters": {
          "title": "Buy groceries",
          "user_id": "abc-123"
        }
      },
      "outputs": [
        {
          "status": "success",
          "task_id": 456,
          "message": "Task 'Buy groceries' added successfully"
        }
      ]
    }
  ]
}
```

### GET /api/conversations
Retrieve all conversations for the authenticated user.

#### Response
```json
{
  "conversations": [
    {
      "id": "integer - Conversation ID",
      "title": "string - Conversation title",
      "created_at": "string - ISO date string",
      "updated_at": "string - ISO date string"
    }
  ]
}
```

### DELETE /api/conversations/{conversation_id}
Delete a specific conversation for the authenticated user.

#### Path Parameter
- `conversation_id`: integer - ID of the conversation to delete

#### Response
```json
{
  "message": "string - Confirmation message"
}
```

## Supported Natural Language Commands

The AI assistant supports various natural language commands for task management:

### Adding Tasks
- "Add task: [task title]"
- "Create task: [task title]"
- "I want to add a task: [task title]"
- "New task: [task title]"

### Listing Tasks
- "Show me my tasks"
- "Show me pending tasks"
- "Show me completed tasks"
- "What tasks do I have?"

### Completing Tasks
- "Complete task [task_id]"
- "Mark task [task_id] as done"
- "Finish task [task_id]"

### Updating Tasks
- "Update task [task_id] to [new_title]"
- "Change task [task_id] to [new_description]"

### Deleting Tasks
- "Delete task [task_id]"
- "Remove task [task_id]"

## Error Handling
- `401 Unauthorized`: Missing or invalid JWT token
- `403 Forbidden`: User doesn't have permission for the requested resource
- `404 Not Found`: Requested resource (e.g., conversation) not found
- `422 Unprocessable Entity`: Invalid request parameters
- `500 Internal Server Error`: Unexpected server error

## Rate Limits
The API implements rate limiting to prevent abuse. If rate limits are exceeded, a `429 Too Many Requests` status code will be returned.

## Environment Variables
The following environment variables must be set for the API to function:

- `COHERE_API_KEY`: Your Cohere API key for AI processing
- `DATABASE_URL`: Connection string for the PostgreSQL database
- `BETTER_AUTH_SECRET`: Secret key for JWT token signing
- `BETTER_AUTH_URL`: Base URL for the authentication service