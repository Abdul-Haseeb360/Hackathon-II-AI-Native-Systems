---
id: 2
title: Create Backend Todo API Spec
stage: spec
date: 2026-01-06
surface: agent
model: claude-sonnet-4-5-20250929
feature: backend-todo-api
branch: 001-backend-todo-api
user:
command: sp.specify
labels: [specification, backend, todo-api, jwt-auth, fastapi]
links:
  spec: specs/001-backend-todo-api/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/001-backend-todo-api/spec.md
 - specs/001-backend-todo-api/checklists/requirements.md
tests:
 -
---

## Prompt

/sp.specify

Generate a detailed specification plan for implementing the Backend of Phase II: Full-Stack Todo Web Application.

Project Context:

- We are in Phase II of the hackathon.

- Transitioning from Phase-1 console app to multi-user web app.

- Using monorepo with Spec-Kit Plus structure.

- All implementation must be done via Claude Code — no manual coding.

- Constitution has been

## Overview

Brief summary of backend goals for Phase II.

## Dependencies

- Environment variables required

- Python packages (fastapi, uvicorn, sqlmodel, psycopg2-binary, python-jose[cryptography], python-multipart, passlib[bcrypt])

## Implementation Phases (in order)

1. Project structure and initial setup

2. Database models and connection

3. JWT middleware and dependency

4. Task CRUD roamended to v1.1.0 with new governance rules.

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

5. Proper error handling (401 Unauthorized, 403 Forbidden if ownershutes with ownership enforcement

5. Error handling and security

6. Testing instructions



## Final Output Expectations

- Fully functional FastAPI backend at http://localhost:8000

- Protected routes requiring valid JWT

- All task operations isolated per user

- OpenAPI docs available at /docs

Use clear markdown formatting with code blocks for examples (e.g., middleware snippet, dependency pattern).

Follow Spec-Kit Plus conventions.

## Response snapshot

Created a comprehensive specification for the Backend Todo API with JWT Authentication. The specification includes:

- User stories for all CRUD operations with proper authentication and authorization
- Functional requirements for JWT verification, task operations, user isolation, and error handling
- Key entities (Task and User) with proper relationships
- Measurable success criteria for performance and security
- Edge cases for error conditions and security scenarios

The specification follows Spec-Kit Plus conventions and is ready for the planning phase.

## Outcome

- ✅ Impact: Comprehensive backend API specification created with security and user isolation requirements
- 🧪 Tests: N/A
- 📁 Files: Created spec.md and requirements checklist for backend-todo-api feature
- 🔁 Next prompts: Ready for /sp.plan to create implementation plan
- 🧠 Reflection: Specification properly captures JWT authentication requirements and user data isolation

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin planning phase with /sp.plan