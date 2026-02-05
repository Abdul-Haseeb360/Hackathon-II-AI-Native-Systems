# Development Tasks: Hackathon II – Phase 1 In-Memory Python Console Todo App

**Feature**: 001-console-todo-app
**Date**: 2025-12-27
**Status**: Generated from `/sp.tasks` command

## Implementation Strategy

**MVP First**: User Story 1 (Create Todo Item) forms the minimum viable product that demonstrates core functionality. Each user story builds incrementally to create a complete application.

**Delivery Approach**: Implement each user story as a complete, independently testable increment. Tasks are organized by priority and dependency requirements.

## Phase 1: Setup

- [x] T001 Create project directory structure with src/ and tests/ directories
- [x] T002 Initialize Python project with basic configuration files
- [x] T003 Set up UV virtual environment as specified in constitution
- [x] T004 Create src/ directory and initial file structure (main.py, todo_app.py)

## Phase 2: Foundational

- [x] T005 [P] Define TodoItem class with id, title, completed attributes in src/todo_app.py
- [x] T006 [P] Define TodoList class with todos collection and next_id counter in src/todo_app.py
- [x] T007 [P] Implement basic CLI menu structure in src/main.py with placeholder functions
- [x] T008 [P] Set up error handling and input validation utilities

## Phase 3: User Story 1 - Create Todo Item (Priority: P1)

**Goal**: Enable users to add new todo items to their list with unique identifiers

**Independent Test**: Can be fully tested by starting the application, creating a new todo with a title, and verifying the item appears in the list.

**Tasks**:
- [x] T009 [US1] Implement TodoItem constructor with validation (title not empty, completed=False by default)
- [x] T010 [US1] Implement TodoList.add_todo() method to add new items and assign unique IDs
- [x] T011 [US1] Create CLI function for option 1 that prompts for title and creates todo
- [x] T012 [US1] Add input validation to ensure title is not empty
- [x] T013 [US1] Display success message with new todo ID after creation
- [x] T014 [US1] Test creating a todo with valid title and verify it appears in the list

## Phase 4: User Story 2 - List All Todo Items (Priority: P1)

**Goal**: Enable users to view all their existing todo items with clear status indicators

**Independent Test**: Can be fully tested by creating several todos and then listing them to verify all appear with correct status indicators.

**Tasks**:
- [x] T015 [US2] Implement TodoList.get_all_todos() method to retrieve all items
- [x] T016 [US2] Create CLI function for option 2 that displays formatted list of todos
- [x] T017 [US2] Format output to show ID, title, and completion status clearly
- [x] T018 [US2] Handle case when no todos exist with appropriate message
- [x] T019 [US2] Test listing todos when multiple items exist
- [x] T020 [US2] Test listing todos when no items exist

## Phase 5: User Story 3 - Mark Todo as Completed (Priority: P1)

**Goal**: Enable users to mark a todo item as completed to track their progress

**Independent Test**: Can be fully tested by creating a todo, marking it as completed, and then listing todos to verify the status has changed.

**Tasks**:
- [x] T021 [US3] Implement TodoList.mark_complete() method to update completion status
- [x] T022 [US3] Create CLI function for option 3 that prompts for todo ID and marks as complete
- [x] T023 [US3] Add validation to ensure the specified todo ID exists
- [x] T024 [US3] Display success message after marking todo as complete
- [x] T025 [US3] Handle error case when invalid todo ID is provided
- [x] T026 [US3] Test marking an existing todo as complete and verifying status change

## Phase 6: User Story 6 - Exit Application (Priority: P1)

**Goal**: Provide clean application termination for proper lifecycle management

**Independent Test**: Can be fully tested by starting the application and using the exit command to terminate it cleanly.

**Tasks**:
- [x] T027 [US6] Implement CLI function for option 6 that exits the application cleanly
- [x] T028 [US6] Ensure proper cleanup before exit (if any needed)
- [x] T029 [US6] Test clean exit functionality without errors
- [x] T030 [US6] Verify application terminates properly when option 6 is selected

## Phase 7: User Story 4 - Update Todo Title (Priority: P2)

**Goal**: Enable users to change the title of an existing todo item

**Independent Test**: Can be fully tested by creating a todo, updating its title, and then listing todos to verify the title has changed.

**Tasks**:
- [x] T031 [US4] Implement TodoList.update_title() method to change todo title
- [x] T032 [US4] Create CLI function for option 4 that prompts for todo ID and new title
- [x] T033 [US4] Add validation to ensure todo ID exists and new title is not empty
- [x] T034 [US4] Display success message after updating todo title
- [x] T035 [US4] Handle error cases for invalid ID or empty title
- [x] T036 [US4] Test updating a todo title and verifying the change

## Phase 8: User Story 5 - Delete Todo Item (Priority: P2)

**Goal**: Enable users to remove a todo item from their list

**Independent Test**: Can be fully tested by creating a todo, deleting it, and then listing todos to verify it's no longer present.

**Tasks**:
- [x] T037 [US5] Implement TodoList.delete_todo() method to remove items
- [x] T038 [US5] Create CLI function for option 5 that prompts for todo ID and deletes it
- [x] T039 [US5] Add validation to ensure the specified todo ID exists
- [x] T040 [US5] Display success message after deleting todo
- [x] T041 [US5] Handle error case when invalid todo ID is provided
- [x] T042 [US5] Test deleting a todo and verifying it's removed from the list

## Phase 9: Polish & Cross-Cutting Concerns

**Goal**: Enhance user experience and handle edge cases for robustness

**Tasks**:
- [x] T043 Add graceful handling for invalid menu selections with error messages
- [x] T044 Implement validation for empty or very long todo titles
- [x] T045 Handle special characters in todo titles appropriately
- [x] T046 Ensure all error cases from specification are handled gracefully
- [x] T047 Add clear and user-friendly CLI prompts as specified
- [x] T048 Test edge cases: invalid input, non-existent todos, empty titles
- [x] T049 Verify application meets all success criteria from specification
- [x] T050 Complete final integration test of all functionality

## Dependencies

**User Story Order**: All P1 stories (US1, US2, US3, US6) can be implemented independently. P2 stories (US4, US5) depend on core functionality established in P1 stories.

**Critical Path**: T001→T005→T006→T007→T009→T010→T011→T015→T016→T021→T022→T027→T028

## Parallel Execution Examples

**Per User Story**:
- **US1**: T009, T010 can be done in parallel with other foundational tasks
- **US2**: T015, T016 can be developed in parallel
- **US3**: T021, T022 can be developed in parallel
- **US4**: T031, T032 can be developed in parallel
- **US5**: T037, T038 can be developed in parallel

**Cross-Story Parallelism**: After foundational work, multiple user stories can be developed in parallel if needed.