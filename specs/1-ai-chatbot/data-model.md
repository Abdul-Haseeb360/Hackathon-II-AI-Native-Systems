# Data Model for AI Todo Chatbot

## Entities

### Conversation
**Description**: Represents a single chat session between user and AI assistant
**Fields**:
- `id`: Integer (Primary Key, Auto-increment)
- `user_id`: UUID (Foreign Key to User, required) - links to the user who owns this conversation
- `created_at`: DateTime (required) - when the conversation was initiated
- `updated_at`: DateTime (required) - when the conversation was last updated
- `title`: String (optional) - auto-generated summary of the conversation

**Relationships**:
- Belongs to one User
- Has many Messages

### Message
**Description**: Represents a single message in a conversation
**Fields**:
- `id`: Integer (Primary Key, Auto-increment)
- `conversation_id`: Integer (Foreign Key to Conversation, required) - links to the conversation this message belongs to
- `role`: String (required) - either "user" or "assistant"
- `content`: String (required) - the actual message content
- `created_at`: DateTime (required) - when the message was created
- `tool_calls`: JSON (optional) - any tool calls made by the assistant in this message
- `tool_results`: JSON (optional) - results from tool calls

**Relationships**:
- Belongs to one Conversation

### Task (Existing)
**Description**: Represents a todo task (existing entity extended for AI access)
**Fields**:
- `id`: Integer (Primary Key, Auto-increment)
- `user_id`: UUID (Foreign Key to User, required) - links to the user who owns this task
- `title`: String (required) - the task title
- `description`: String (optional) - additional details about the task
- `completed`: Boolean (required, default: False) - whether the task is completed
- `created_at`: DateTime (required) - when the task was created
- `updated_at`: DateTime (required) - when the task was last updated

**Relationships**:
- Belongs to one User
- Referenced by Messages (through tool calls)

## Validation Rules

### Conversation
- `user_id` must reference a valid User
- `created_at` must be in the past
- `updated_at` must be >= `created_at`

### Message
- `conversation_id` must reference a valid Conversation
- `role` must be either "user" or "assistant"
- `content` must not be empty
- `created_at` must be in the past
- `role` of "assistant" messages may contain `tool_calls` and `tool_results`

### Task (for AI access)
- `user_id` must match the authenticated user for access
- `title` must not be empty
- `completed` can only be modified by the task owner

## State Transitions

### Task State Transitions
- `pending` → `completed` when complete_task tool is called
- `completed` → `pending` when update_task tool is called to unmark completion

## Indexes
- Conversation: Index on `user_id` for efficient user-based queries
- Message: Index on `conversation_id` for efficient conversation history retrieval
- Task: Index on `user_id` for efficient user-based queries