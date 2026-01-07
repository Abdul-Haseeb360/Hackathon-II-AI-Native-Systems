---
description: "Task list for Backend Todo API with JWT Authentication implementation"
---

# Tasks: Backend Todo API with JWT Authentication

**Input**: Design documents from `/specs/001-backend-todo-api/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `backend/tests/`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Navigate to backend directory and ensure virtual environment is active
- [x] T002 [P] Add FastAPI dependencies using UV: fastapi, uvicorn[standard]
- [x] T003 [P] Add SQLModel dependencies using UV: sqlmodel, psycopg2-binary
- [x] T004 [P] Add JWT authentication dependencies using UV: python-jose[cryptography], passlib[bcrypt]
- [x] T005 [P] Add utility dependencies using UV: python-multipart, pydantic-settings
- [x] T006 Update pyproject.toml with new dependencies

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T007 Create database models directory structure in backend/src/models/
- [x] T008 [P] Setup database connection utilities in backend/src/database/
- [x] T009 [P] Implement JWT utility functions for token validation in backend/src/auth/
- [x] T010 [P] Create JWT dependency for extracting user_id from token in backend/src/auth/
- [x] T011 Create configuration management with pydantic-settings in backend/src/config/
- [x] T012 Create base models and error handling utilities in backend/src/utils/

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Create Todo Tasks (Priority: P1) 🎯 MVP

**Goal**: A registered user wants to create new todo tasks in their personal list after authenticating with their JWT token

**Independent Test**: Can be fully tested by making a POST request to /api/tasks with a valid JWT token and task data, and verifying the task is created and returned with a 201 status code

### Implementation for User Story 1

- [x] T013 [P] [US1] Create Task model with SQLModel in backend/src/models/task.py
- [x] T014 [US1] Create Pydantic request/response models for tasks in backend/src/schemas/task.py
- [x] T015 [US1] Implement Task service with database operations in backend/src/services/task_service.py
- [x] T016 [US1] Create POST /api/tasks endpoint in backend/src/api/tasks.py
- [x] T017 [US1] Add JWT authentication middleware to the endpoint
- [x] T018 [US1] Add proper error handling and validation to task creation

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View Todo Tasks (Priority: P1)

**Goal**: A registered user wants to retrieve their own todo tasks after authenticating with their JWT token. The user should only see tasks that belong to them and not tasks from other users

**Independent Test**: Can be fully tested by making a GET request to /api/tasks with a valid JWT token and verifying only the authenticated user's tasks are returned

### Implementation for User Story 2

- [x] T019 [P] [US2] Add query parameter models for filtering and sorting in backend/src/schemas/task.py
- [x] T020 [US2] Enhance Task service with query filtering methods in backend/src/services/task_service.py
- [x] T021 [US2] Create GET /api/tasks endpoint in backend/src/api/tasks.py
- [x] T022 [US2] Implement user isolation by filtering by authenticated user_id
- [x] T023 [US2] Add support for status filtering and sorting query parameters

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Update Todo Tasks (Priority: P2)

**Goal**: A registered user wants to update their own todo tasks after authenticating with their JWT token. The user should only be able to update tasks that belong to them

**Independent Test**: Can be fully tested by making a PUT request to /api/tasks/{id} with a valid JWT token and updated task data, verifying the task is updated only if it belongs to the authenticated user

### Implementation for User Story 3

- [x] T024 [US3] Add update methods to Task service in backend/src/services/task_service.py
- [x] T025 [US3] Create PATCH /api/tasks/{id}/complete endpoint in backend/src/api/tasks.py
- [x] T026 [US3] Implement ownership verification for update operations
- [x] T027 [US3] Add proper error handling for unauthorized access attempts

**Checkpoint**: User Stories 1, 2, and 3 should all work independently

---

## Phase 6: User Story 4 - Delete Todo Tasks (Priority: P2)

**Goal**: A registered user wants to delete their own todo tasks after authenticating with their JWT token. The user should only be able to delete tasks that belong to them

**Independent Test**: Can be fully tested by making a DELETE request to /api/tasks/{id} with a valid JWT token, verifying the task is deleted only if it belongs to the authenticated user

### Implementation for User Story 4

- [x] T028 [US4] Add delete methods to Task service in backend/src/services/task_service.py
- [x] T029 [US4] Create DELETE /api/tasks/{id} endpoint in backend/src/api/tasks.py
- [x] T030 [US4] Implement ownership verification for delete operations
- [x] T031 [US4] Add proper error handling for unauthorized access attempts

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T032 [P] Add comprehensive API documentation in backend/src/main.py
- [x] T033 [P] Add input validation for all request data
- [x] T034 Add proper HTTP status codes to all endpoints
- [x] T035 Add logging for all operations
- [x] T036 Create database initialization and migration scripts
- [x] T037 Run quickstart validation to ensure all functionality works

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3 but should be independently testable

### Within Each User Story

- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all models for User Story 1 together:
Task: "Create Task model with SQLModel in backend/src/models/task.py"
Task: "Create Pydantic request/response models for tasks in backend/src/schemas/task.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
