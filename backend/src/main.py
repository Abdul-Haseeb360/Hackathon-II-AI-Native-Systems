"""
Main entry point for the console todo application
"""
from todo_app import TodoList, TodoItem
import sys


def get_user_input(prompt: str) -> str:
    """
    Get input from the user with proper error handling

    Args:
        prompt: The prompt to display to the user

    Returns:
        The user's input as a string
    """
    try:
        return input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        print("\nApplication interrupted. Exiting...")
        sys.exit(0)


def display_menu():
    """Display the main menu options to the user"""
    print("\n" + "="*40)
    print("         TODO APPLICATION")
    print("="*40)
    print("1. Create a new todo")
    print("2. List all todos")
    print("3. Mark a todo as completed")
    print("4. Update a todo title")
    print("5. Delete a todo")
    print("6. Exit")
    print("="*40)


def handle_create_todo(todo_list: TodoList):
    """
    Handle the create todo functionality

    Args:
        todo_list: The TodoList instance to add the todo to
    """
    title = get_user_input("Enter the todo title: ")

    if not title:
        print("Error: Title cannot be empty.")
        return

    try:
        new_todo = todo_list.add_todo(title)
        print(f"✓ Successfully created todo with ID {new_todo.id}: {new_todo.title}")
    except ValueError as e:
        print(f"Error: {e}")


def handle_list_todos(todo_list: TodoList):
    """
    Handle the list todos functionality

    Args:
        todo_list: The TodoList instance to list todos from
    """
    todos = todo_list.get_all_todos()

    if not todos:
        print("\nNo todos found.")
        return

    print("\nYour todos:")
    print("-" * 50)
    for todo in todos:
        status = "✓ Completed" if todo.completed else "○ Pending"
        print(f"{todo.id}. [{status}] {todo.title}")
    print("-" * 50)
    print(f"Total: {len(todos)} todo(s)")


def handle_mark_complete(todo_list: TodoList):
    """
    Handle the mark todo as completed functionality

    Args:
        todo_list: The TodoList instance to update
    """
    if todo_list.get_count() == 0:
        print("No todos available to mark as complete.")
        return

    try:
        todo_id_str = get_user_input("Enter the ID of the todo to mark as completed: ")
        if not todo_id_str:
            print("Error: Please enter a valid ID.")
            return

        todo_id = int(todo_id_str)

        # Check if the todo exists
        if not todo_list.find_todo(todo_id):
            print(f"Error: No todo found with ID {todo_id}.")
            return

        success = todo_list.mark_complete(todo_id)
        if success:
            print(f"✓ Successfully marked todo {todo_id} as completed.")
        else:
            print(f"Error: Failed to mark todo {todo_id} as completed.")
    except ValueError:
        print("Error: Please enter a valid numeric ID.")


def handle_update_title(todo_list: TodoList):
    """
    Handle the update todo title functionality

    Args:
        todo_list: The TodoList instance to update
    """
    if todo_list.get_count() == 0:
        print("No todos available to update.")
        return

    try:
        todo_id_str = get_user_input("Enter the ID of the todo to update: ")
        if not todo_id_str:
            print("Error: Please enter a valid ID.")
            return

        todo_id = int(todo_id_str)

        # Check if the todo exists
        if not todo_list.find_todo(todo_id):
            print(f"Error: No todo found with ID {todo_id}.")
            return

        new_title = get_user_input("Enter the new title: ")
        if not new_title:
            print("Error: Title cannot be empty.")
            return

        success = todo_list.update_title(todo_id, new_title)
        if success:
            print(f"✓ Successfully updated todo {todo_id} title.")
        else:
            print(f"Error: Failed to update todo {todo_id} title.")
    except ValueError:
        print("Error: Please enter a valid numeric ID.")


def handle_delete_todo(todo_list: TodoList):
    """
    Handle the delete todo functionality

    Args:
        todo_list: The TodoList instance to delete from
    """
    if todo_list.get_count() == 0:
        print("No todos available to delete.")
        return

    try:
        todo_id_str = get_user_input("Enter the ID of the todo to delete: ")
        if not todo_id_str:
            print("Error: Please enter a valid ID.")
            return

        todo_id = int(todo_id_str)

        # Check if the todo exists
        if not todo_list.find_todo(todo_id):
            print(f"Error: No todo found with ID {todo_id}.")
            return

        success = todo_list.delete_todo(todo_id)
        if success:
            print(f"✓ Successfully deleted todo {todo_id}.")
        else:
            print(f"Error: Failed to delete todo {todo_id}.")
    except ValueError:
        print("Error: Please enter a valid numeric ID.")


def main():
    """Main application loop"""
    print("Welcome to the Todo Application!")
    print("This is a simple in-memory todo list manager.")
    print("All data will be lost when the application exits.")

    # Initialize the todo list
    todo_list = TodoList()

    while True:
        display_menu()
        choice = get_user_input("Select an option (1-6): ")

        if choice == "1":
            handle_create_todo(todo_list)
        elif choice == "2":
            handle_list_todos(todo_list)
        elif choice == "3":
            handle_mark_complete(todo_list)
        elif choice == "4":
            handle_update_title(todo_list)
        elif choice == "5":
            handle_delete_todo(todo_list)
        elif choice == "6":
            print("Thank you for using the Todo Application. Goodbye!")
            break
        else:
            print(f"Invalid option '{choice}'. Please select a number between 1 and 6.")

        # Pause to let user see the result before showing the menu again
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()