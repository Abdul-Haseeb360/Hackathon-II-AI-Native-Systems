# Data Model: Frontend Todo Application

## Entity: User
**Description**: Represents an authenticated user of the system
**Fields**:
- id: string (unique identifier)
- email: string (email address for authentication)
- name: string (optional display name)
- createdAt: Date (account creation timestamp)
- updatedAt: Date (last update timestamp)

**Validation rules**:
- Email must be valid email format
- Email must be unique across all users
- Name (if provided) must be 1-50 characters

**State transitions**: N/A (User state managed by Better Auth)

## Entity: Todo Task
**Description**: Represents a user's personal task with properties like title, description, completion status, and timestamps
**Fields**:
- id: string (unique identifier)
- userId: string (foreign key to User)
- title: string (task title)
- description: string (optional task description)
- completed: boolean (completion status)
- createdAt: Date (task creation timestamp)
- updatedAt: Date (last update timestamp)

**Validation rules**:
- Title must be 1-200 characters
- UserId must reference an existing user
- Completed defaults to false

**State transitions**:
- Pending → Completed (when user marks task as complete)
- Completed → Pending (when user unmarks task as complete)

## Entity: Authentication Session
**Description**: Represents the user's authenticated state with JWT token management for API requests
**Fields**:
- userId: string (reference to authenticated user)
- token: string (JWT token)
- expiresAt: Date (token expiration time)
- createdAt: Date (session creation time)

**Validation rules**:
- Token must be valid JWT format
- ExpiresAt must be in the future
- Session must correspond to valid user

**State transitions**:
- Active → Expired (when token expires)
- Active → Terminated (when user logs out)

## Relationships
- User (1) : Todo Task (Many) - One user can have many todo tasks
- User (1) : Authentication Session (1) - One user has one active session at a time

## Data Constraints
- Todo tasks can only be accessed by their owner (userId match)
- Authentication sessions expire after configured time period
- User data privacy maintained through authentication checks
- All API requests require valid authentication token

## Frontend-Specific Considerations
- Local state management for optimistic UI updates
- Caching strategies for improved performance
- Error states for failed API operations
- Loading states for pending operations