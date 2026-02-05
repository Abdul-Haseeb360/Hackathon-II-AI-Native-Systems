"""
Database migration script to add Conversation and Message tables for AI chatbot feature.
This script creates the necessary tables for storing conversation history and messages.
"""

import sqlite3
from pathlib import Path

def run_migration(db_path: str = "todo_api.db"):
    """Run the migration to add Conversation and Message tables."""

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create conversations table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            title TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Create messages table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id INTEGER NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            tool_calls TEXT,
            tool_results TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (conversation_id) REFERENCES conversations(id)
        )
    """)

    # Create indexes for efficient querying
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_conversations_user_id ON conversations(user_id)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_messages_conversation_id ON messages(conversation_id)
    """)

    conn.commit()
    conn.close()

    print("Migration completed successfully!")
    print("- Created conversations table")
    print("- Created messages table")
    print("- Added indexes for efficient querying")


if __name__ == "__main__":
    import os
    db_path = os.environ.get("DATABASE_PATH", "todo_api.db")
    run_migration(db_path)