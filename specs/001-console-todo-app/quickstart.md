# Quickstart Guide: Hackathon II – Phase 1 In-Memory Python Console Todo App

**Feature**: 001-console-todo-app
**Date**: 2025-12-27

## Prerequisites

- Python 3.8 or higher
- UV package manager for virtual environment management

## Environment Setup

1. **Initialize the project with UV**:
   ```bash
   # If starting fresh, initialize a new project
   uv init
   ```

2. **Create and activate UV-managed virtual environment**:
   ```bash
   # Create virtual environment
   uv venv

   # Activate the virtual environment
   # On Windows:
   source .venv/Scripts/activate
   # On macOS/Linux:
   source .venv/bin/activate
   ```

3. **Verify isolated Python runtime**:
   ```bash
   # Check that you're using the virtual environment Python
   which python
   python --version
   ```

## Running the Application

1. **Navigate to the project directory** where main.py is located

2. **Execute the application**:
   ```bash
   python src/main.py
   ```

3. **The application will start and present a menu** with options:
   - 1. Create a new todo
   - 2. List all todos
   - 3. Mark a todo as completed
   - 4. Update a todo title
   - 5. Delete a todo
   - 6. Exit

## Basic Usage

1. **Creating a todo**: Select option 1, then enter the todo title when prompted
2. **Listing todos**: Select option 2 to see all todos with their status
3. **Marking as completed**: Select option 3, then enter the todo ID
4. **Updating a title**: Select option 4, enter the todo ID and new title
5. **Deleting a todo**: Select option 5, enter the todo ID to remove
6. **Exiting**: Select option 6 to cleanly terminate the application

## Validation Steps

After implementing each feature, verify:

1. **Create operation**: Create a todo and verify it appears in the list
2. **List operation**: Confirm all todos are displayed with correct status
3. **Complete operation**: Mark a todo as complete and verify status change
4. **Update operation**: Change a todo title and verify the change
5. **Delete operation**: Remove a todo and confirm it's no longer in the list
6. **Exit operation**: Terminate cleanly without errors
7. **Error handling**: Test with invalid inputs to ensure graceful handling