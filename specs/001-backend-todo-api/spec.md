# Feature Specification: Backend Todo API with JWT Authentication

**Feature Branch**: `001-backend-todo-api`
**Created**: 2026-01-06
**Status**: Draft
**Input**: User description: "Generate a detailed specification plan for implementing the Backend of Phase II: Full-Stack Todo Web Application.

Project Context:

- We are in Phase II of the hackathon.

- Transitioning from Phase-1 console app to multi-user web app.

- Using monorepo with Spec-Kit Plus structure.

- All implementation must be done via Claude Code — no manual coding.

- Constitution has been amended to v1.1.0 with new governance rules.

Objective:

Create a comprehensive /sp.specify file that defines the exact steps, order, and spec references needed to fully implement the Python FastAPI backend with authentication, persistence, and user isolation.

Technology Stack (Backend):

- FastAPI (main.py as entry point)

- SQLModel (for models and ORM)

- Neon Serverless PostgreSQL (via DATABASE_URL env var)

- Better Auth integration via JWT tokens (shared BETTER_AUTH_SECRET)

- Pydantic for request/response models

- JWT verification middleware for securing all routes

Key Requirements:

1. Database setup and models (users managed by Better Auth, tasks with user_id foreign key)

2. JWT authentication middleware (verify token, extract user_id, enforce ownership)

3. All CRUD endpoints under /api/tasks (no {user_id} in path — use authenticated user from JWT)

4. Full user isolation — every query must filter by authenticated user_id

5. Proper error handling (401 Unauthorized, 403 Forbidden if ownership)

5. Error handling and security

6. Testing instructions

## Final Output Expectations

- Fully functional FastAPI backend at http://localhost:8000

- Protected routes requiring valid JWT

- All task operations isolated per user

- OpenAPI docs available at /docs

Use clear markdown formatting with code blocks for examples (e.g., middleware snippet, dependency pattern).

Follow Spec-Kit Plus conventions."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create Todo Tasks (Priority: P1)

A registered user wants to create new todo tasks in their personal list after authenticating with their JWT token. The user can provide a title and optional description for their task, which gets stored securely in the database and is only accessible to them.

**Why this priority**: This is the core functionality that enables users to add items to their todo list, which is the fundamental value proposition of the application.

**Independent Test**: Can be fully tested by making a POST request to /api/tasks with a valid JWT token and task data, and verifying the task is created and returned with a 201 status code.

**Acceptance Scenarios**:

1. **Given** a user has a valid JWT token, **When** they POST to /api/tasks with valid task data, **Then** the task is created and returned with 201 status
2. **Given** a user does not have a valid JWT token, **When** they POST to /api/tasks, **Then** they receive a 401 Unauthorized response

---

### User Story 2 - View Todo Tasks (Priority: P1)

A registered user wants to retrieve their own todo tasks after authenticating with their JWT token. The user should only see tasks that belong to them and not tasks from other users.

**Why this priority**: This is the core read functionality that allows users to view their todo list, which is essential for the application's purpose.

**Independent Test**: Can be fully tested by making a GET request to /api/tasks with a valid JWT token and verifying only the authenticated user's tasks are returned.

**Acceptance Scenarios**:

1. **Given** a user has a valid JWT token and has created tasks, **When** they GET /api/tasks, **Then** they receive only their own tasks with 200 status
2. **Given** a user does not have a valid JWT token, **When** they GET /api/tasks, **Then** they receive a 401 Unauthorized response

---

### User Story 3 - Update Todo Tasks (Priority: P2)

A registered user wants to update their own todo tasks after authenticating with their JWT token. The user should only be able to update tasks that belong to them.

**Why this priority**: This allows users to modify their existing tasks, such as marking them as complete or changing their details.

**Independent Test**: Can be fully tested by making a PUT request to /api/tasks/{id} with a valid JWT token and updated task data, verifying the task is updated only if it belongs to the authenticated user.

**Acceptance Scenarios**:

1. **Given** a user has a valid JWT token and owns a task, **When** they PUT to /api/tasks/{id} with updated data, **Then** the task is updated with 200 status
2. **Given** a user has a valid JWT token but does not own a task, **When** they PUT to /api/tasks/{id}, **Then** they receive a 403 Forbidden response

---

### User Story 4 - Delete Todo Tasks (Priority: P2)

A registered user wants to delete their own todo tasks after authenticating with their JWT token. The user should only be able to delete tasks that belong to them.

**Why this priority**: This allows users to remove completed or unwanted tasks from their list.

**Independent Test**: Can be fully tested by making a DELETE request to /api/tasks/{id} with a valid JWT token, verifying the task is deleted only if it belongs to the authenticated user.

**Acceptance Scenarios**:

1. **Given** a user has a valid JWT token and owns a task, **When** they DELETE /api/tasks/{id}, **Then** the task is deleted with 200 status
2. **Given** a user has a valid JWT token but does not own a task, **When** they DELETE /api/tasks/{id}, **Then** they receive a 403 Forbidden response

---

### Edge Cases

- What happens when a user tries to access a task that doesn't exist?
- How does the system handle expired JWT tokens?
- What happens when a user tries to create a task with invalid data?
- How does the system handle database connection failures?
- What happens when a user tries to access another user's task?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST verify JWT tokens from Better Auth before allowing access to any task operations
- **FR-002**: System MUST extract user_id from JWT token and use it for all task ownership verification
- **FR-003**: System MUST store tasks in Neon PostgreSQL database with user_id foreign key relationship
- **FR-004**: System MUST filter all task queries by authenticated user_id to ensure data isolation
- **FR-005**: System MUST provide CRUD operations for tasks under /api/tasks endpoint
- **FR-006**: System MUST return 401 Unauthorized for invalid or missing JWT tokens
- **FR-007**: System MUST return 403 Forbidden when users try to access tasks they don't own
- **FR-008**: System MUST validate task data format before storing in the database
- **FR-009**: System MUST provide proper error messages for all error conditions
- **FR-010**: System MUST support standard HTTP methods (GET, POST, PUT, DELETE) for task operations
- **FR-011**: System MUST provide OpenAPI documentation at /docs endpoint
- **FR-012**: System MUST use SQLModel for database models and ORM operations

### Key Entities *(include if feature involves data)*

- **Task**: Represents a user's todo item with attributes like title, description, completion status, and creation timestamp
- **User**: Represents an authenticated user identified by user_id from JWT token, with tasks relationship

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can create new tasks with valid JWT token in under 2 seconds
- **SC-002**: Users can retrieve their own tasks with valid JWT token in under 2 seconds
- **SC-003**: System prevents unauthorized access to tasks with 100% accuracy (401/403 responses for invalid access attempts)
- **SC-004**: 100% of task operations are properly filtered by authenticated user_id to ensure data isolation
- **SC-005**: API endpoints return proper HTTP status codes for all scenarios (200, 201, 401, 403, 404, etc.)
- **SC-006**: OpenAPI documentation is available at /docs and accurately reflects all task endpoints