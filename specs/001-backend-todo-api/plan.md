# Implementation Plan: Backend Todo API with JWT Authentication

## Overview

This plan outlines the implementation of the Backend component for Phase II: Multi-User Full-Stack Todo Web Application. The backend will be built using FastAPI with SQLModel ORM, Neon Serverless PostgreSQL, and JWT authentication middleware. The system will provide secure, isolated task management for multiple users with proper authentication and authorization.

## Dependencies

- **FastAPI**: Modern Python web framework with automatic API documentation
- **SQLModel**: SQL database modeling and querying library
- **uvicorn[standard]**: ASGI server for running the FastAPI application
- **psycopg2-binary**: PostgreSQL database adapter
- **python-jose[cryptography]**: JWT token handling and verification
- **passlib[bcrypt]**: Password hashing utilities
- **python-multipart**: Form data parsing support
- **pydantic-settings**: Settings management for configuration
- **Neon Serverless PostgreSQL**: Cloud PostgreSQL database service

## Decisions Needing Documentation

- **Database Connection Management**: Decision on connection pooling and session management patterns for SQLModel with Neon
- **JWT Token Validation Strategy**: Approach for validating Better Auth JWT tokens with shared BETTER_AUTH_SECRET
- **Error Response Format**: Standardized format for API error responses across all endpoints
- **Task Model Design**: Detailed field definitions for the Task entity with user_id foreign key relationship

## Testing Strategy

- **Unit Tests**: Individual function and class tests for data models and utility functions
- **Integration Tests**: API endpoint tests with mocked JWT authentication
- **Security Tests**: Validation of user isolation and authentication requirements
- **Database Tests**: Tests for data persistence and query filtering functionality
- **Load Testing**: Performance validation under expected user load

## Technical Details

### Architecture
- FastAPI application with SQLAlchemy/SQLModel ORM
- JWT middleware for authentication
- Dependency injection for database sessions
- Pydantic models for request/response validation

### Data Model
- Task model with fields: id, title, description, completed status, user_id, created_at, updated_at
- User relationship via user_id from JWT token
- Proper indexing for performance

### API Endpoints
- GET /api/tasks - Retrieve user's tasks with query parameters (status, sort)
- POST /api/tasks - Create new task for authenticated user
- PUT /api/tasks/{id} - Update existing task (user must own the task)
- DELETE /api/tasks/{id} - Delete task (user must own the task)

### Security
- JWT token validation middleware
- User isolation enforcement on all database queries
- Proper HTTP status codes (401, 403, 404, etc.)

## Implementation Steps (Sequential)

### Phase 1: Environment and Dependencies
1. Navigate to backend directory and ensure virtual environment is active
2. Use UV to add required packages: fastapi, uvicorn[standard], sqlmodel, psycopg2-binary, python-jose[cryptography], passlib[bcrypt], python-multipart, pydantic-settings
3. Update pyproject.toml with new dependencies

### Phase 2: Database Setup
1. Create database models directory structure
2. Define Task model with SQLModel including user_id foreign key
3. Set up database connection and session management utilities
4. Create database initialization and migration scripts

### Phase 3: JWT Authentication
1. Create JWT utility functions for token validation
2. Implement JWT dependency for extracting user_id from token
3. Create authentication middleware to validate Better Auth JWT tokens
4. Set up configuration for BETTER_AUTH_SECRET

### Phase 4: API Endpoints
1. Create FastAPI application instance
2. Implement GET /api/tasks endpoint with query parameter support
3. Implement POST /api/tasks endpoint for creating new tasks
4. Implement PUT /api/tasks/{id} endpoint for updating tasks
5. Implement DELETE /api/tasks/{id} endpoint for deleting tasks
6. Add proper error handling and response validation

### Phase 5: Security Implementation
1. Add user isolation checks to all database queries
2. Validate that each operation is performed by the task owner
3. Implement proper error responses for unauthorized access attempts
4. Add input validation for all request data

### Phase 6: Testing and Documentation
1. Create unit tests for all components
2. Implement integration tests for API endpoints
3. Add OpenAPI documentation generation
4. Create basic test data and validation scripts

## Final Validation

- API endpoints return proper HTTP status codes (200, 201, 401, 403, 404)
- JWT tokens are properly validated and user_id extracted
- All database queries filter by authenticated user_id
- Task operations only succeed when user owns the task
- Query parameters (status, sort) work correctly on GET /api/tasks
- OpenAPI documentation available at /docs endpoint
- Application runs successfully with uvicorn
- All unit and integration tests pass