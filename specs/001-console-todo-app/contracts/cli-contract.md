# API Contracts: Hackathon II – Phase 1 In-Memory Python Console Todo App

**Feature**: 001-console-todo-app
**Date**: 2025-12-27

## CLI Interface Contract

### User Actions

#### 1. Create Todo
- **Input**: User selects option 1, then enters a title string
- **Output**: Success message with new todo ID, or error message
- **Validation**: Title must not be empty
- **Error cases**: Empty title

#### 2. List Todos
- **Input**: User selects option 2
- **Output**: Formatted list of all todos with ID, title, and completion status
- **Validation**: None required
- **Error cases**: None (empty list is valid)

#### 3. Mark Todo Complete
- **Input**: User selects option 3, then enters a todo ID
- **Output**: Success message confirming status change, or error message
- **Validation**: Todo ID must exist in current session
- **Error cases**: Invalid ID, non-existent todo

#### 4. Update Todo Title
- **Input**: User selects option 4, enters todo ID, then enters new title
- **Output**: Success message confirming update, or error message
- **Validation**: Todo ID must exist, new title must not be empty
- **Error cases**: Invalid ID, empty title

#### 5. Delete Todo
- **Input**: User selects option 5, then enters a todo ID
- **Output**: Success message confirming deletion, or error message
- **Validation**: Todo ID must exist in current session
- **Error cases**: Invalid ID, non-existent todo

#### 6. Exit Application
- **Input**: User selects option 6
- **Output**: Clean termination of application
- **Validation**: None required
- **Error cases**: None

## Data Contract

### Todo Item Structure
```
{
  "id": integer (unique within session),
  "title": string (non-empty),
  "completed": boolean
}
```

### Todo List Structure
```
{
  "todos": [Todo Item],
  "count": integer (total number of todos)
}
```