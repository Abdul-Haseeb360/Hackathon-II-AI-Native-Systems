# Research: Hackathon II – Phase 1 In-Memory Python Console Todo App

**Feature**: 001-console-todo-app
**Date**: 2025-12-27

## Decision: In-Memory Storage Choice

**Rationale**: In-memory storage was chosen to satisfy the Phase 1 requirement for non-persistent data. This approach keeps the application simple and avoids file I/O operations that would complicate the implementation. The data will exist only during runtime and reset upon program exit, which aligns with the specification constraints.

**Alternatives considered**:
- File-based persistence (rejected - violates "Storage: In-memory data structures only" constraint)
- Database storage (rejected - violates "No databases" constraint)

## Decision: Menu-Driven CLI Interface

**Rationale**: A menu-driven interface provides clear, user-friendly prompts that guide the user through available operations. This approach makes the application accessible to users with basic Python knowledge as specified in the target audience. The menu system will present numbered options for each operation (create, list, mark complete, etc.).

**Alternatives considered**:
- Command-line arguments (rejected - less user-friendly for basic users)
- Direct command entry (rejected - more complex error handling required)

## Decision: Single-File vs Multi-File Structure

**Rationale**: A minimal file structure with two files (main.py for CLI interface and todo_app.py for core logic) provides a good balance between organization and simplicity. This follows the "Simplicity over completeness" principle from the constitution while keeping the code readable and maintainable.

**Alternatives considered**:
- Single large file (rejected - harder to navigate and maintain)
- Multiple modules/packages (rejected - over-engineering for Phase 1 scope)

## Decision: Standard Python Libraries Only

**Rationale**: Using only standard Python libraries (sys, os, collections, etc.) ensures no external dependencies, which aligns with the constraint "External libraries: None unless strictly necessary". This approach maintains a lightweight application that can run without additional package installations.

**Alternatives considered**:
- Third-party CLI frameworks (rejected - violates "no external libraries" constraint)
- Advanced data structures from external packages (rejected - standard libraries sufficient)

## Decision: Unique Identifier Generation

**Rationale**: Using auto-incrementing integer IDs provides simple, predictable identifiers that are easy for users to reference when performing operations on specific todos. The IDs will be unique within each session and reset when the application restarts.

**Alternatives considered**:
- UUIDs (rejected - unnecessarily complex for this use case)
- User-provided IDs (rejected - adds complexity to avoid duplicates)