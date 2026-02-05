---
id: 2
title: "create-implementation-plan-for-ai-chatbot"
stage: "plan"
date_iso: "2026-01-21"
surface: "agent"
model: "Claude Sonnet 4.5"
feature: "ai-chatbot"
branch: "1-ai-chatbot"
user: "user"
command: "/sp.plan"
labels: ["plan", "ai-chatbot", "architecture", "implementation"]
spec: "../spec.md"
ticket: null
adr: null
pr: null
files_yaml: |
  - specs/1-ai-chatbot/plan.md
  - specs/1-ai-chatbot/research.md
  - specs/1-ai-chatbot/data-model.md
  - specs/1-ai-chatbot/contracts/chat-api.yaml
  - specs/1-ai-chatbot/quickstart.md
tests_yaml: |
  - None
prompt_text: |
  Project: AI Todo Chatbot - Phase 3 Integration into Existing Full-Stack Todo App

  Use the specification document generated in the previous /sp.specify phase as the primary input.

  Core Goal of this Plan:
  Generate a realistic, detailed, and executable implementation plan (plan.md) that shows exactly how to integrate the Cohere-powered AI chatbot into the existing full-stack application without breaking Phase 1/Phase 2 functionality.

  Key Constraints & Context from Constitution & Specification:
  - Existing stack: FastAPI (backend), SQLModel + Neon PostgreSQL, Better Auth (JWT), Next.js App Router + Tailwind + Shadcn/UI (frontend)
  - Stateless design: All conversation state in DB (Conversation + Message models)
  - AI: Use Cohere SDK (cohere.Client with chat + tools support) — NO OpenAI/Gemini wrappers
  - Tools: Stateless MCP-style functions (add_task, list_tasks, complete_task, delete_task, update_task) — all take user_id (UUID)
  - Frontend: Add floating chat icon → opens chat panel/modal → connects to /api/chat
  - Environment: COHERE_API_KEY required; deploy updates to existing Vercel + Hugging Face
  - No new repos; all changes in current GitHub repo
  - Agent behavior: natural language parsing → tool calls → confirmations + error handling

  Important Backend Package Management Rule (must be followed in all phases):
  - We are using **uv**[](https://docs.astral.sh/uv/) instead of pip for managing Python dependencies in the backend.
  - Whenever a new package needs to be added to the backend, the following steps must be followed:
    1. Activate the virtual environment (uv venv)
    2. Run:  uv add <package-name>
  - Do NOT use pip install for any backend dependency.
  - Existing dependencies should be managed via uv (i.e. uv sync / uv lock should be used to keep pyproject.toml and uv.lock in sync).
  - All installation instructions in README.md and in any implementation steps must use uv commands.

  Plan Structure Requirements (follow this exactly in plan.md):

  # AI Todo Chatbot Phase 3 Implementation Plan

  ## 1. Architecture Overview
  - High-level diagram (ASCII or mermaid if possible)
  - How frontend, backend, Cohere, DB, and MCP tools interact
  - Key integration points (auth, endpoint, DB models, UI component)

  ## 2. Implementation Phases (3–6 logical phases)
  Break the entire work into sequential phases with clear goals, estimated effort (story points or hours), and success criteria.
  Suggested phases (you may adjust):
  - Phase 1: Database & Auth Foundation
  - Phase 2: MCP Tools Implementation
  - Phase 3: Cohere Agent & Chat Endpoint
  - Phase 4: Frontend Chat UI & Floating Icon
  - Phase 5: Testing & Polish
  - Phase 6: Deployment & Documentation

  For each phase:
  - Objective
  - Key deliverables (files created/modified)
  - Dependencies (what previous phases must complete)
  - Package additions (if any) — MUST specify exact uv add command(s)
  - Risks & mitigations
  - Acceptance criteria

  ## 3. Component Breakdown
  List major components/modules and their responsibilities:
  - Backend modules (routers/chat.py, tools/mcp_tools.py, agents/cohere_agent.py, etc.)
  - DB models & migrations
  - Cohere integration logic (client init, tool definitions, call loop)
  - Frontend components (ChatIcon.tsx, ChatPanel.tsx, etc.)
  - Shared utilities (if any)

  ## 4. Dependencies & Sequencing
  - Visual dependency graph (text-based or mermaid)
  - Critical path (what blocks deployment)
  - Parallelizable work (if any)

  ## 5. Design Decisions & ADRs
  List 4–8 architecturally significant decisions that should be documented as ADRs later (/sp.adr).
  For each:
  - Decision title
  - Context (why needed)
  - Chosen approach
  - Alternatives considered
  - Rationale
  - Consequences (positive/negative)

  Examples to cover:
  - Why direct Cohere SDK instead of agent framework wrapper
  - How to handle multi-tool calls in one turn (loop logic)
  - Floating chat UI strategy (modal vs drawer vs fixed panel)
  - Conversation persistence strategy (single active convo vs multiple)
  - Error propagation from tools to user-friendly messages
  - Package management: using uv instead of pip

  ## 6. Validation & Testing Strategy
  - Unit tests (tools, endpoint handlers)
  - Integration tests (full chat flow with Cohere mock if possible)
  - Manual test scenarios (based on natural language examples from spec)
  - Acceptance criteria mapping back to specification

  ## 7. Risks & Mitigations
  - Top 5 risks (technical, time, cost, Cohere-specific, uv-related)
  - Mitigation plan for each

  ## 8. Timeline & Effort Estimate
  - Rough total effort (in developer-days or story points)
  - Suggested sprint/iteration breakdown

  ## 9. Next Steps
  - Immediate actions after approving this plan (e.g., run /sp.tasks, start /sp.implement on Phase 1)
  - Commands to use next in Spec-Kit Plus workflow

  Additional Instructions for the Plan:
  - In every phase wher
response_text: |
  Created comprehensive implementation plan for the AI Todo Chatbot integration. The plan includes:

  1. Architecture Overview: Detailed ASCII diagram showing the interaction between frontend, backend, Cohere API, and database components.

  2. Six Implementation Phases:
     - Phase 1: Database & Auth Foundation
     - Phase 2: MCP Tools Implementation
     - Phase 3: Cohere Agent & Chat Endpoint
     - Phase 4: Frontend Chat UI & Floating Icon
     - Phase 5: Testing & Polish
     - Phase 6: Deployment & Documentation

  3. Component Breakdown: Identified all major components including backend modules, DB models, Cohere integration, and frontend components.

  4. Dependencies & Sequencing: Clear dependency graph showing the critical path and parallelizable work.

  5. Design Decisions & ADRs: Six architecturally significant decisions documented covering Cohere integration, tool calling, UI strategy, and error handling.

  6. Validation & Testing Strategy: Comprehensive approach including unit, integration, and manual testing.

  7. Risks & Mitigations: Five major risks identified with specific mitigation strategies.

  8. Timeline & Effort Estimate: 12-15 developer days across 4 sprints.

  9. Next Steps: Clear action items to proceed with the implementation.

  Additionally created supporting documents:
  - research.md: Key decisions and rationale
  - data-model.md: Detailed database schema
  - contracts/chat-api.yaml: OpenAPI specification
  - quickstart.md: Setup and usage guide
outcome: |
  Successfully created implementation plan and supporting documentation for AI Todo Chatbot.
  - Created plan.md with comprehensive implementation strategy
  - Created research.md with key decisions
  - Created data-model.md with entity relationships
  - Created API contract in YAML format
  - Created quickstart guide for developers
  - All artifacts placed in specs/1-ai-chatbot/ directory
evaluation: |
  The implementation plan successfully addresses all requirements:
  ✓ Follows specified structure and format
  ✓ Incorporates constitution constraints (uv package management, Cohere API)
  ✓ Defines clear phases with deliverables and dependencies
  ✓ Identifies architecturally significant decisions
  ✓ Provides comprehensive testing and risk mitigation strategies
  ✓ Includes supporting documentation (research, data models, contracts)
  ✓ Ready for task breakdown phase (/sp.tasks)
---