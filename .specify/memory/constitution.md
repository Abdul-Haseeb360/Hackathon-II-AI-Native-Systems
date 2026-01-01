<!--
Sync Impact Report:
- Version change: N/A → 1.0.0 (initial creation)
- Added sections: All principles and governance sections
- Templates requiring updates: N/A (new file)
- Follow-up TODOs: None
-->
# Hackathon II – Phase 1 In-Memory Python Console Todo App Constitution

## Core Principles

### Spec-driven development
All code must be generated from written specifications. No implementation work should proceed without an approved specification document that clearly defines the requirements and behavior.

### Environment discipline
All development must occur inside a UV-managed virtual environment. This ensures consistent dependencies and reproducible builds across different development environments.

### Simplicity over completeness
Implement only what is required for Phase 1. Focus on the minimal viable functionality needed to demonstrate the core concepts without adding unnecessary features or complexity.

### Determinism
Application behavior must be predictable and consistent. The application should produce the same outputs for the same inputs and have no random or time-dependent behavior that could cause inconsistency.

### Clarity
Code and CLI interactions must be easy to understand for reviewers. All functionality should be clearly documented through code structure, naming conventions, and comments where necessary.

### Discipline
No manual coding outside the AI-driven workflow. All changes must be made through Claude Code as the implementation agent following the Spec-Kit Plus methodology.

## Key Standards

### UV Virtual Environment Requirement
A Python virtual environment must be created using UV before any implementation. Development must follow the UV workflow: project initialization, venv creation, and activation. All development activities must occur within this managed environment.

### Specification-driven Implementation
No code generation without an approved specification. All changes must be reflected in updated specs before execution. Use Claude Code strictly as the implementation agent and follow Spec-Kit Plus command sequence without shortcuts.

## Constraints

### Language and Interface
Language: Python only. Interface: Console / command-line only. Runtime environment: UV-managed Python virtual environment.

### Storage and Scope
Storage: In-memory data structures only (no files, no databases). Scope: Single-user, single-session usage. External services: Not allowed. Persistence across restarts: Not allowed.

## Explicit Non-goals

### Out of Scope Requirements
No authentication or user accounts. No web interface or APIs. No AI features inside the application. No optimization for future phases. No deployment or containerization.

## Success Criteria

### Deliverables
A working Python CLI Todo application that matches the written specification. All functionality implemented through Claude Code based on specs. All development performed inside an activated UV virtual environment. Zero deviation between specified behavior and actual behavior. Clear evidence of Spec-Kit Plus methodology usage.

## Governance

This constitution governs all development activities for the Hackathon II – Phase 1 In-Memory Python Console Todo App. All development must comply with these principles. Amendments to this constitution require explicit approval and documentation of the changes. The constitution supersedes all other development practices and guidelines.

**Version**: 1.0.0 | **Ratified**: 2025-12-27 | **Last Amended**: 2025-12-27