# Data Model: Backend Todo API

## Task Entity

**Description**: Represents a user's todo item with attributes for tracking tasks and their completion status.

**Fields**:
- `id` (int, primary key, auto-increment): Unique identifier for the task
- `title` (str): Title of the task (required, max length 255)
- `description` (str, optional): Detailed description of the task
- `completed` (bool): Completion status of the task (default: false)
- `user_id` (str): ID of the user who owns the task (from JWT token)
- `created_at` (datetime): Timestamp when the task was created
- `updated_at` (datetime): Timestamp when the task was last updated

**Validation Rules**:
- Title must not be empty
- Title must be between 1-255 characters
- User_id must match the authenticated user from JWT token
- Completed status can only be updated by the task owner

**Relationships**:
- Belongs to a user (identified by user_id from JWT token)

## User Context

**Description**: User context is derived from the JWT token provided in the Authorization header, with user_id extracted for data isolation.

**Fields** (from JWT claims):
- `user_id` (str): Unique identifier of the authenticated user
- `exp` (int): Expiration timestamp of the token
- `iat` (int): Issuance timestamp of the token