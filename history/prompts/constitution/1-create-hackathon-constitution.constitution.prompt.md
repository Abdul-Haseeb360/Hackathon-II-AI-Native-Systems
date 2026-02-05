---
id: 1
title: Create Hackathon Constitution
stage: constitution
date: 2025-12-27
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: user
command: /sp.constitution
labels: [constitution, hackathon, setup]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 -
---

## Prompt

```
/sp.constitution

Project: Hackathon II – Phase 1 In-Memory Python Console Todo App

Core principles:
- Spec-driven development: all code must be generated from written specifications
- Environment discipline: all development must occur inside a UV-managed virtual environment
- Simplicity over completeness: implement only what is required for Phase 1
- Determinism: application behavior must be predictable and consistent
- Clarity: code and CLI interactions must be easy to understand for reviewers
- Discipline: no manual coding outside the AI-driven workflow

Key standards:
- A Python virtual environment must be created using UV before any implementation
- Development must follow the UV workflow: project initialization, venv creation, and activation
- No code generation without an approved specification
- All changes must be reflected in updated specs before execution
- Use Claude Code strictly as the implementation agent
- Follow Spec-Kit Plus command sequence without shortcuts

Constraints:
- Language: Python only
- Interface: Console / command-line only
- Runtime environment: UV-managed Python virtual environment
- Storage: In-memory data structures only (no files, no databases)
- Scope: Single-user, single-session usage
- External services: Not allowed
- Persistence across restarts: Not allowed

Explicit non-goals:
- No authentication or user accounts
- No web interface or APIs
- No AI features inside the application
- No optimization for future phases
- No deployment or containerization

Success criteria:
- A working Python CLI Todo application that matches the written specification
- All functionality implemented through Claude Code based on specs
- All development performed inside an activated UV virtual environment
- Zero deviation between specified behavior and actual behavior
- Clear evidence of Spec-Kit Plus methodology usage
```

## Response snapshot

Created the constitution file for the Hackathon II – Phase 1 In-Memory Python Console Todo App with all specified principles, standards, constraints, non-goals, and success criteria. The constitution establishes the foundational rules for the project including spec-driven development, environment discipline with UV, simplicity focus, deterministic behavior, clarity in code and CLI interactions, and adherence to the AI-driven workflow discipline.

## Outcome

- ✅ Impact: Created initial project constitution establishing development principles and governance
- 🧪 Tests: N/A
- 📁 Files: Created .specify/memory/constitution.md with all required principles
- 🔁 Next prompts: Proceed with project specification and implementation
- 🧠 Reflection: Constitution provides clear governance framework for the hackathon project

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin with project specification