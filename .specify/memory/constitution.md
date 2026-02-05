<!--
Sync Impact Report:
- Version change: 1.1.0 → 1.2.0 (Phase-3 AI Chatbot addition)
- Added sections: Amendment section for Phase-3 AI Todo Chatbot Constitution
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

# Amendment: Hackathon II – Phase 3 AI Todo Chatbot Constitution

## Core Principles

### Integration-First
All new features must integrate seamlessly into the existing full-stack app without creating separate repos or breaking existing functionality. Reuse existing User/Task models, JWT authentication, and API routes.

### Stateless and Scalable
Backend must remain stateless (no in-memory sessions); all state (tasks, conversations, messages) persisted in Neon PostgreSQL via SQLModel. The system must scale horizontally without relying on shared memory or session state.

### AI Reliability
Use Cohere API (via Cohere SDK) for all AI logic, including tool calling and multi-turn conversations. Adapt any OpenAI-style code to Cohere (e.g., replace openai.ChatCompletion with cohere.Chat, handle tools in Cohere format).

### Security and Isolation
Enforce user isolation via JWT (Better Auth); all tools/actions scoped to authenticated user_id. Maintain the same security standards established in Phase 2 for data access and authentication.

### Quality and Testability
All outputs must be verifiable, error-handled, and confirmed. AI responses include action confirmations like "Task added: Buy groceries". Implement comprehensive error handling for AI interactions.

### Ethical AI
Handle natural language gracefully, assume good intent, no moralizing; support edgy but legal queries per safety guidelines. AI responses must be helpful and non-judgmental while maintaining safety.

## Key Standards

### Code Quality Standards
All Python code must use type hints, follow PEP 8 (testable via black/flake8); frontend TSX must use strict types. AI integration code must include proper error handling and logging.

### API Security Standards
All endpoints (e.g., /api/chat) protected by JWT; validate inputs (e.g., Pydantic); handle errors with HTTP status codes (e.g., 404 for task not found). Maintain same security standards as Phase 2.

### Database Integrity Standards
Use SQLModel for models (Task: user_id(UUID), id(int), title(str), description(str optional), completed(bool), created_at(datetime), updated_at(datetime); Conversation: user_id(UUID), id(int), created_at(datetime), updated_at(datetime); Message: conversation_id(int), role(str: user/assistant), content(str), created_at(datetime)). Run migrations via Alembic or SQLModel.create_all.

### AI Performance Standards
Cohere model (e.g., command-r-plus) must parse natural language intents accurately (e.g., "Add task to buy groceries" → add_task tool); chain tools if needed (e.g., list then delete); limit agent loops to 5 iterations to prevent infinite runs; confirm actions (e.g., "Task 3 marked complete"); handle errors (e.g., "Task not found, please check ID").

### Testing Standards
All features testable via examples (e.g., "Show pending tasks" → list_tasks with status="pending"); minimum 80% code coverage via pytest; UI tested via Cypress or manual. Include tests for AI tool calling functionality.

### Documentation Standards
Update README.md with setup (e.g., env vars: COHERE_API_KEY, DATABASE_URL); include architecture diagram in ASCII. Document AI integration patterns and API endpoints.

### Deployment Standards
Updates must deploy to existing Vercel/Hugging Face; frontend uses OpenAI ChatKit (adapted for Cohere if needed, with domain allowlist configured). Maintain zero-downtime deployment patterns.

## Constraints

### Tech Stack Lock
No changes to core stack (FastAPI, SQLModel, Neon PG, Next.js, Better Auth); adapt Cohere for agent (e.g., cohere.Client(api_key=COHERE_API_KEY).chat with tools param). Maintain backward compatibility with existing features.

### Performance Constraints
API responses < 2s; DB queries optimized (e.g., indexes on user_id). AI response times should not exceed 5 seconds for typical requests.

### Size and Complexity Constraints
Constitution document < 2000 words; code files < 500 lines where possible. MCP tools must remain stateless functions in backend (add_task, list_tasks(status: all/pending/completed), complete_task, delete_task, update_task); all take user_id (UUID required); returns JSON (e.g., {"task_id": 5, "status": "created"}).

### Budget Constraints
Cohere API calls < 1000 tokens per request; use cheapest effective model. Optimize token usage through efficient prompting and response handling.

## Explicit Non-goals

### Out of Scope Requirements for Phase 3
No replacement of existing functionality with AI. No breaking changes to existing API contracts. No introduction of new authentication methods. No complex AI features beyond natural language task management. No offline AI processing or local models.

## Success Criteria

### Deliverables for Phase 3
A working AI chatbot integrated into the existing full-stack Todo application that enables natural language task management (add/list/complete/delete/edit tasks, get user info). Cohere API integration with MCP tools for operations. DB-persisted conversation history for stateless server. Integrated into existing backend/frontend without disrupting current functionality. All functionality implemented through Claude Code based on updated specs. Clear evidence of Spec-Kit Plus methodology usage in Phase-3 context.

### Integration Success Metrics
Chatbot works end-to-end in existing app (e.g., POST /api/chat with message/conversation_id → Cohere agent calls MCP tools → DB update → response with confirmation). Maintains backward compatibility with existing features.

### Quality Metrics
Zero security vulnerabilities (via bandit); 100% error handling coverage; AI accuracy > 95% on spec examples (e.g., "Mark task 3 complete" → complete_task). Passes unit tests for tools (e.g., add_task creates DB entry); e2e tests for natural language (e.g., "Delete task 2" → confirmation if successful).

### Final Validation
Chatbot resumes conversations after restart (DB-persisted); handles multi-tool chains; deploys without downtime. Maintains all Phase 1 and Phase 2 functionality.

## Governance

This amendment governs all development activities for the Hackathon II – Phase 3 AI Todo Chatbot. All Phase-3 development must comply with these principles while maintaining compliance with Phase-1 and Phase-2 principles where applicable. The amended constitution supersedes all other development practices and guidelines for Phase-3.

**Version**: 1.2.0 | **Ratified**: 2026-01-21 | **Last Amended**: 2026-01-21