# API Contracts: Frontend Todo Application

## Authentication Endpoints

### POST /api/auth/register
Register a new user account

**Request Body**:
```json
{
  "email": "string (valid email format)",
  "password": "string (min 8 characters)",
  "name": "string (optional)"
}
```

**Response (200 OK)**:
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "string",
      "email": "string",
      "name": "string"
    },
    "token": "string (JWT token)"
  }
}
```

**Response (400 Bad Request)**:
```json
{
  "success": false,
  "error": "string (validation error message)"
}
```

### POST /api/auth/login
Authenticate user and return JWT token

**Request Body**:
```json
{
  "email": "string (valid email)",
  "password": "string (user password)"
}
```

**Response (200 OK)**:
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "string",
      "email": "string",
      "name": "string"
    },
    "token": "string (JWT token)"
  }
}
```

## Todo Task Endpoints

### GET /api/tasks
Retrieve all tasks for the authenticated user

**Headers**:
- Authorization: Bearer {JWT_TOKEN}

**Response (200 OK)**:
```json
{
  "success": true,
  "data": [
    {
      "id": "string",
      "userId": "string",
      "title": "string",
      "description": "string",
      "completed": "boolean",
      "createdAt": "string (ISO date)",
      "updatedAt": "string (ISO date)"
    }
  ]
}
```

### POST /api/tasks
Create a new todo task

**Headers**:
- Authorization: Bearer {JWT_TOKEN}

**Request Body**:
```json
{
  "title": "string (1-200 characters)",
  "description": "string (optional)",
  "completed": "boolean (default: false)"
}
```

**Response (201 Created)**:
```json
{
  "success": true,
  "data": {
    "id": "string",
    "userId": "string",
    "title": "string",
    "description": "string",
    "completed": "boolean",
    "createdAt": "string (ISO date)",
    "updatedAt": "string (ISO date)"
  }
}
```

### PUT /api/tasks/{taskId}
Update an existing todo task

**Headers**:
- Authorization: Bearer {JWT_TOKEN}

**Request Body**:
```json
{
  "title": "string (1-200 characters) (optional)",
  "description": "string (optional)",
  "completed": "boolean (optional)"
}
```

**Response (200 OK)**:
```json
{
  "success": true,
  "data": {
    "id": "string",
    "userId": "string",
    "title": "string",
    "description": "string",
    "completed": "boolean",
    "createdAt": "string (ISO date)",
    "updatedAt": "string (ISO date)"
  }
}
```

### PATCH /api/tasks/{taskId}/toggle
Toggle the completion status of a task

**Headers**:
- Authorization: Bearer {JWT_TOKEN}

**Response (200 OK)**:
```json
{
  "success": true,
  "data": {
    "id": "string",
    "userId": "string",
    "title": "string",
    "description": "string",
    "completed": "boolean",
    "createdAt": "string (ISO date)",
    "updatedAt": "string (ISO date)"
  }
}
```

### DELETE /api/tasks/{taskId}
Delete a todo task

**Headers**:
- Authorization: Bearer {JWT_TOKEN}

**Response (200 OK)**:
```json
{
  "success": true,
  "data": {
    "message": "Task deleted successfully"
  }
}
```

## Error Responses

### 401 Unauthorized
```json
{
  "success": false,
  "error": "Authentication required"
}
```

### 403 Forbidden
```json
{
  "success": false,
  "error": "Access denied"
}
```

### 404 Not Found
```json
{
  "success": false,
  "error": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "success": false,
  "error": "Internal server error occurred"
}
```