# Feature Specification: AI Todo Chatbot Integration with Cohere API

**Feature Branch**: `1-ai-chatbot`
**Created**: 2026-01-21
**Status**: Draft
**Input**: User description: "Project: AI Todo Chatbot - Phase 3 Integration into Existing Full-Stack Todo App
Phase: Specification Document Generation
Goal: Generate a clear, detailed, and actionable specification document for implementing the AI chatbot using Cohere API instead of OpenAI/Gemini. The chatbot must integrate seamlessly into the existing FastAPI + Next.js application. Include backend (chat endpoint + Cohere agent with tools) and frontend (floating chat icon that opens a chat window).

Existing Context:
- Phase 1: Simple Python console app with in-memory task list (add, list, complete, delete).
- Phase 2: Full-stack app with:
  - Backend: FastAPI, SQLModel, Neon PostgreSQL, Better Auth (JWT), user-isolated task endpoints
  - Frontend: Next.js (App Router), Tailwind, Shadcn/UI, deployed on Vercel
  - Deployments: Frontend → Vercel, Backend → Hugging Face
- Phase 3 requirements (from previous spec):
  - AI chatbot for natural language task management: add_task, list_tasks, complete_task, delete_task, update_task
  - Stateless server: conversation history stored in DB (Conversation + Message models)
  - MCP-style tools: stateless functions that interact with DB, always take user_id
  - Use Cohere API for agent logic (not OpenAI or Gemini)

Provided Code Example (to be adapted):
from agents import Agent, AsyncOpenAI, Runner, OpenAIChatCompletionsModel, RunConfig
from dotenv import load_dotenv
import os
load_dotenv()
API_key = os.getenv("GEMINI_API_KEY")
if not API_key:
raise ValueError("GEMINI_API_KEY is not set.")
external_client = AsyncOpenAI(
api_key=API_key,
base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
model = OpenAIChatCompletionsModel(
model="gemini-2.0-flash",
openai_client=external_client
)
config = RunConfig(
model=model,
model_provider=external_client,
tracing_disabled=True
)
Writer = Agent(
name="Writer Agent",
instructions="You provide help with math problems. Explain your reasoning at each step and include examples"
)
response = Runner.run_sync(
Writer,
input="Write a 2 paragraph essay on Vibe coding",
run_config=config
)
print(response.final_output)
textAdaptation Rules:
- Replace Gemini with Cohere: Use Cohere SDK (cohere.Client) instead of AsyncOpenAI wrapper.
- Use Cohere's chat endpoint with tool calling support (cohere.chat with tools parameter).
- Keep the agent + runner pattern if possible, or simplify to direct Cohere chat calls with tool handling loop.
- Environment variable: COHERE_API_KEY
- Model suggestion: command-r-plus or command-r (choose based on tool-calling capability)

Specification Requirements:
1. Project Structure Updates
   - Which files/folders to create or modify in existing repo
   - New dependencies (backend & frontend)

2. Database Models (SQLModel)
   - Conversation and Message models (exact fields)
   - Relationship with existing User and Task models

3. Backend (FastAPI)
   - New endpoint: POST /api/chat (accepts message + optional conversation_id)
   - Authentication: JWT via Better Auth → get current user
   - Stateless logic: load conversation history from DB, append user message, call Cohere, handle tool calls in loop, save updated history
   - MCP Tools definition & implementation (add_task, list_tasks, complete_task, delete_task, update_task)
   - Tool calling loop (max 5 iterations)
   - System prompt for the agent (task management behavior + confirmations)

4. Cohere Integration
   - How to initialize Cohere client
   - Define tools in Cohere-compatible format
   - Handle tool calls and feed results back
   - Adapt the provided code example to use Cohere instead of Gemini/OpenAI wrapper

5. Frontend (Next.js)
   - Add a floating chatbot icon (bottom-right corner, Shadcn/UI button with chat bubble icon)
   - Clicking icon opens a chat window (modal or slide-over panel)
   - Chat UI: message list (user/assistant), input field, send button
   - Connect to /api/chat endpoint using fetch/axios (include JWT)
   - Handle conversation_id persistence (localStorage or state)
   - Loading state, error handling

6. Natural Language Behavior
   - List supported intents and example utterances → tool mapping
   - Confirmation messages (e.g., "Task 'Buy groceries' a"

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.

  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - Natural Language Task Management (Priority: P1)

A user wants to manage their todo tasks using natural language instead of clicking buttons. They open the chat interface and say "Add a task to buy groceries" or "Show me my pending tasks" or "Complete task number 3". The AI chatbot understands their intent and performs the corresponding action, then confirms the result back to the user.

**Why this priority**: This is the core value proposition of the feature - enabling natural language interaction with the todo system, which significantly improves user experience and accessibility.

**Independent Test**: Can be fully tested by typing natural language commands in the chat interface and verifying that the corresponding task operations are performed correctly in the backend, delivering the value of hands-free task management.

**Acceptance Scenarios**:

1. **Given** user is logged in and has opened the chat interface, **When** user types "Add task: Buy milk" and submits, **Then** a new task "Buy milk" is created in the user's task list and the AI confirms "Task 'Buy milk' added successfully"
2. **Given** user has multiple tasks in their list, **When** user types "Show me pending tasks", **Then** the AI responds with a list of all pending tasks
3. **Given** user has tasks in their list, **When** user types "Complete task 1", **Then** task 1 is marked as completed and the AI confirms "Task 1 marked as completed"

---

### User Story 2 - Persistent Conversations (Priority: P2)

A user engages in a multi-turn conversation with the AI chatbot, creating, listing, and modifying tasks over several exchanges. The conversation context is maintained across page reloads and browser sessions, allowing for a coherent ongoing interaction with the system.

**Why this priority**: Ensures continuity of user experience and allows for complex task management workflows that span multiple interactions.

**Independent Test**: Can be tested by engaging in a multi-turn conversation, refreshing the page, and verifying that the conversation history is preserved and the AI can reference previous interactions.

**Acceptance Scenarios**:

1. **Given** user has been chatting with the AI, **When** user refreshes the page and reopens the chat, **Then** the previous conversation history is displayed
2. **Given** user had a conversation in one session, **When** user returns to the app in a new session, **Then** the user can continue the conversation or start a new one

---

### User Story 3 - Intuitive Chat Interface (Priority: P3)

A user discovers and accesses the AI chat functionality through an intuitive interface element. The chat window is easy to use, with clear visual distinction between user and AI messages, smooth input experience, and appropriate loading indicators during AI processing.

**Why this priority**: Ensures users can easily discover and use the chat functionality, improving adoption and satisfaction.

**Independent Test**: Can be tested by verifying the presence and functionality of the chat icon, the appearance and usability of the chat interface, and the clarity of the message display.

**Acceptance Scenarios**:

1. **Given** user is on any page of the application, **When** user sees the floating chat icon, **Then** it's clearly visible and recognizable as a chat interface
2. **Given** user clicks the chat icon, **When** the chat window opens, **Then** it displays a clean interface with message history and input field

---

### Edge Cases

- What happens when a user sends malformed or ambiguous natural language requests?
- How does the system handle API errors from the Cohere service?
- What occurs when a user tries to access another user's tasks through the chat interface?
- How does the system handle rate limiting from the Cohere API?
- What happens when the database is temporarily unavailable during a chat interaction?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a natural language interface for todo task management using Cohere AI
- **FR-002**: System MUST support the following task operations via natural language: add, list, complete, delete, update
- **FR-003**: System MUST authenticate all chat requests using existing JWT authentication
- **FR-004**: System MUST store conversation history in the database for persistence
- **FR-005**: System MUST ensure user data isolation - users can only access their own tasks through the chat
- **FR-006**: System MUST provide a floating chat interface accessible from any page in the application
- **FR-007**: System MUST handle tool calling loops with a maximum of 5 iterations to prevent infinite loops
- **FR-008**: System MUST provide clear confirmation messages after each task operation (e.g., "Task 'Buy groceries' added successfully")
- **FR-009**: System MUST handle Cohere API errors gracefully and provide informative messages to users
- **FR-010**: System MUST persist conversation state across browser sessions using the database

### Key Entities *(include if feature involves data)*

- **Conversation**: Represents a single chat session between user and AI, contains metadata like creation time and user association
- **Message**: Represents a single message in a conversation, with role (user/assistant), content, and timestamp
- **Task**: Existing entity extended to be accessible via AI tools, representing todo items with title, description, completion status

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: Users can successfully perform all basic task operations (add/list/complete/delete/update) using natural language with 95% accuracy
- **SC-002**: AI response time is under 5 seconds for typical requests
- **SC-003**: Users report 80% satisfaction with the natural language task management experience
- **SC-004**: At least 30% of users engage with the chat feature within the first week of availability
- **SC-005**: The system maintains 99% uptime for the chat functionality