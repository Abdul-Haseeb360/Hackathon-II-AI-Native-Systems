# Data Model: Hackathon II – Phase 1 In-Memory Python Console Todo App

**Feature**: 001-console-todo-app
**Date**: 2025-12-27

## Entity: Todo Item

**Representation**: A single task in the todo list

**Fields**:
- `id` (integer): Unique identifier within the session, auto-incremented
- `title` (string): The description/text of the todo item
- `completed` (boolean): Status indicating whether the todo is completed

**Validation rules**:
- `id` must be unique within the session
- `title` must not be empty or None
- `completed` defaults to False when creating a new todo

**State transitions**:
- New todo: `completed = False`
- Marked complete: `completed = True`
- Marked incomplete: `completed = False` (if functionality exists to unmark)

## Entity: Todo List

**Representation**: Collection of Todo Items managed in memory during the application session

**Fields**:
- `todos` (list/dict): Collection of Todo Item objects
- `next_id` (integer): Counter for generating unique IDs

**Validation rules**:
- Each Todo Item in the collection must have a unique `id`
- IDs should be sequential integers starting from 1
- No persistence across application restarts

**Operations supported**:
- Add a new Todo Item
- List all Todo Items
- Find Todo Item by ID
- Update Todo Item (title or completion status)
- Remove Todo Item by ID

## Relationships

- Todo List contains multiple Todo Items
- Each Todo Item belongs to exactly one Todo List (during the session)
- Todo Items are uniquely identified by their `id` within the Todo List