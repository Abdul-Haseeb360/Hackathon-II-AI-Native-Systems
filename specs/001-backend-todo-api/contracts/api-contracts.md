# API Contracts: Backend Todo API

## Task Management Endpoints

### GET /api/tasks
**Description**: Retrieve all tasks for the authenticated user with optional filtering and sorting.

**Authentication**: Required - Valid JWT token in Authorization header

**Query Parameters**:
- `status` (optional): Filter tasks by status (all, pending, completed)
- `sort` (optional): Sort order (created, title, due_date)

**Response**:
- 200: Array of Task objects
- 401: Unauthorized - Invalid or missing JWT token

### POST /api/tasks
**Description**: Create a new task for the authenticated user.

**Authentication**: Required - Valid JWT token in Authorization header

**Request Body**:
- `title` (string): Title of the task (required)
- `description` (string, optional): Description of the task

**Response**:
- 201: Created Task object
- 400: Bad Request - Invalid request data
- 401: Unauthorized - Invalid or missing JWT token

### PUT /api/tasks/{id}
**Description**: Update an existing task for the authenticated user.

**Authentication**: Required - Valid JWT token in Authorization header

**Path Parameter**:
- `id` (integer): Task ID to update

**Request Body**:
- `title` (string, optional): New title of the task
- `description` (string, optional): New description of the task
- `completed` (boolean, optional): New completion status

**Response**:
- 200: Updated Task object
- 400: Bad Request - Invalid request data
- 401: Unauthorized - Invalid or missing JWT token
- 403: Forbidden - User does not own the task
- 404: Not Found - Task does not exist

### DELETE /api/tasks/{id}
**Description**: Delete a task for the authenticated user.

**Authentication**: Required - Valid JWT token in Authorization header

**Path Parameter**:
- `id` (integer): Task ID to delete

**Response**:
- 200: Success message
- 401: Unauthorized - Invalid or missing JWT token
- 403: Forbidden - User does not own the task
- 404: Not Found - Task does not exist