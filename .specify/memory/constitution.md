<!--
Sync Impact Report:
- Version change: 1.0.0 → 1.1.0 (Phase-2 amendment addition)
- Added sections: Amendment section for Phase-2 Full-Stack Web Application Constitution
- Modified sections: Version and amendment date updated
- Templates requiring updates: ✅ Updated in constitution file
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

# Amendment: Hackathon II – Phase 2 Full-Stack Web Application Constitution

## Core Principles

### Full-stack architecture discipline
The application must maintain a clear separation between frontend (Next.js) and backend (FastAPI) components. All data flow must go through the defined API contracts with proper validation and error handling.

### Web-first user experience
The application must provide a responsive, accessible web interface that works across different devices and browsers. User interactions must be intuitive and provide immediate feedback.

### Authentication-first security
All user data must be protected by proper authentication and authorization mechanisms. JWT tokens must be properly validated and secured with appropriate expiration and refresh strategies.

### Persistent data integrity
Data stored in Neon database must maintain ACID properties with proper transaction handling. All database operations must include appropriate error handling and validation.

### Multi-user isolation
Each user's data must be properly isolated from other users. No user should be able to access or modify another user's data without explicit permission.

### API contract compliance
All frontend-backend communication must strictly follow defined API contracts with proper request/response validation, error handling, and versioning strategies.

## Key Standards

### Tech Stack Requirements
Frontend: Next.js 14+ with TypeScript, React Server Components, and App Router. Backend: FastAPI with Python 3.11+, async/await patterns, and proper type hints. Database: Neon PostgreSQL with SQLAlchemy ORM or equivalent.

### Authentication and Authorization Framework
JWT-based authentication with secure token storage, proper expiration handling, and refresh token strategies. All API endpoints must validate authentication unless explicitly marked as public.

### Database Management
Neon PostgreSQL database with proper connection pooling, transaction management, and migration strategies. Database schema changes must be handled through versioned migrations.

### Frontend-Backend Interface Standards
RESTful API design principles with consistent endpoint naming, proper HTTP status codes, and standardized error response formats. All API calls must include proper error handling and loading states.

## Constraints

### Technology Stack
Frontend: Next.js + React + TypeScript only. Backend: FastAPI + Python + PostgreSQL (Neon) only. Authentication: JWT tokens only. No additional frameworks without explicit approval.

### Data Persistence and Multi-user
Storage: Neon PostgreSQL database only (no in-memory storage). Scope: Multi-user support with proper data isolation. Authentication: JWT-based authentication required for all user data access.

### Security and Access Control
All user data must be encrypted in transit (HTTPS). Authentication required for all data-modifying operations. Proper input validation and sanitization required for all user inputs.

## Explicit Non-goals

### Out of Scope Requirements for Phase 2
No desktop application support. No mobile app development. No complex AI features within the application. No third-party integrations beyond Neon database. No advanced real-time features (websockets, etc.).

## Success Criteria

### Deliverables for Phase 2
A working full-stack web Todo application with Next.js frontend and FastAPI backend. JWT-based authentication and authorization implemented. Neon PostgreSQL database integration with proper data isolation between users. Responsive web interface that works across different device sizes. All functionality implemented through Claude Code based on updated specs. Clear evidence of Spec-Kit Plus methodology usage in Phase-2 context.

## Governance

This amendment governs all development activities for the Hackathon II – Phase 2 Full-Stack Web Application. All Phase-2 development must comply with these principles while maintaining compliance with Phase-1 principles where applicable. The amended constitution supersedes all other development practices and guidelines for Phase-2.

**Version**: 1.1.0 | **Ratified**: 2026-01-06 | **Last Amended**: 2026-01-06