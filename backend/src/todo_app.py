"""
Todo application core logic and data structures
"""
from typing import List, Optional


class TodoItem:
    """
    Represents a single todo item with id, title, and completion status
    """
    def __init__(self, id: int, title: str, completed: bool = False):
        """
        Initialize a TodoItem

        Args:
            id: Unique identifier for the todo item
            title: Description of the todo item
            completed: Completion status (default: False)
        """
        if not title or not title.strip():
            raise ValueError("Title cannot be empty")

        self.id = id
        self.title = title.strip()
        self.completed = completed

    def __str__(self):
        """String representation of the todo item"""
        status = "✅" if self.completed else "○"
        return f"[{status}] {self.id}. {self.title}"

    def __repr__(self):
        """Developer representation of the todo item"""
        return f"TodoItem(id={self.id}, title='{self.title}', completed={self.completed})"


class TodoList:
    """
    Collection of Todo Items managed in memory during the application session
    """
    def __init__(self):
        """Initialize an empty todo list with next ID counter"""
        self.todos = {}  # Dictionary to store todos by ID for O(1) lookup
        self.next_id = 1  # Counter for generating unique IDs

    def add_todo(self, title: str) -> TodoItem:
        """
        Add a new todo item to the list with a unique ID

        Args:
            title: The title of the new todo item

        Returns:
            The created TodoItem
        """
        # Create a new TodoItem with the next available ID
        new_todo = TodoItem(self.next_id, title)

        # Add to the collection
        self.todos[self.next_id] = new_todo

        # Increment the ID counter for the next todo
        self.next_id += 1

        return new_todo

    def get_all_todos(self) -> List[TodoItem]:
        """
        Retrieve all todos in the list, sorted by ID

        Returns:
            List of all TodoItem objects, sorted by ID
        """
        return sorted(self.todos.values(), key=lambda x: x.id)

    def mark_complete(self, todo_id: int) -> bool:
        """
        Mark a todo item as completed

        Args:
            todo_id: The ID of the todo to mark as complete

        Returns:
            True if the todo was found and updated, False otherwise
        """
        if todo_id in self.todos:
            self.todos[todo_id].completed = True
            return True
        return False

    def update_title(self, todo_id: int, new_title: str) -> bool:
        """
        Update the title of an existing todo item

        Args:
            todo_id: The ID of the todo to update
            new_title: The new title for the todo

        Returns:
            True if the todo was found and updated, False otherwise
        """
        if todo_id in self.todos and new_title and new_title.strip():
            self.todos[todo_id].title = new_title.strip()
            return True
        return False

    def delete_todo(self, todo_id: int) -> bool:
        """
        Remove a todo item from the list

        Args:
            todo_id: The ID of the todo to delete

        Returns:
            True if the todo was found and deleted, False otherwise
        """
        if todo_id in self.todos:
            del self.todos[todo_id]
            return True
        return False

    def find_todo(self, todo_id: int) -> Optional[TodoItem]:
        """
        Find a todo item by its ID

        Args:
            todo_id: The ID of the todo to find

        Returns:
            The TodoItem if found, None otherwise
        """
        return self.todos.get(todo_id)

    def get_count(self) -> int:
        """Get the total number of todos in the list"""
        return len(self.todos)