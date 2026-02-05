# AI Todo Chatbot Phase 3 Implementation Plan

## 1. Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │     Backend      │    │   External      │
│   (Next.js)     │    │   (FastAPI)      │    │   Services      │
├─────────────────┤    ├──────────────────┤    ├─────────────────┤
│                 │    │                  │    │                 │
│ Chat UI         │◄──►│ /api/chat        │◄──►│ Cohere API      │
│ - Floating icon │    │ - Auth (JWT)     │    │ - Tool calling  │
│ - Chat panel    │    │ - Cohere agent   │    │ - NLP parsing   │
│ - Message list  │    │ - MCP tools      │    │                 │
│                 │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │   Database       │
                    │ (Neon PostgreSQL)│
                    ├──────────────────┤
                    │ - Conversation   │
                    │ - Message        │
                    │ - Task (existing)│
                    │ - User (existing)│
                    └──────────────────┘
```

The architecture follows a stateless design where:
- Frontend provides a floating chat UI that communicates with backend via `/api/chat`
- Backend authenticates requests using JWT, loads conversation history from DB
- Cohere agent processes natural language and calls MCP tools as needed
- MCP tools interact with the database to perform task operations
- All conversation state is persisted in the database for continuity

## 2. Implementation Phases

### Phase 1: Database & Auth Foundation
**Objective**: Set up database models for conversations and messages, extend authentication to protect chat endpoint
**Key deliverables**:
- `models/conversation.py` - Conversation and Message SQLModel classes
- `routers/chat.py` - Protected chat endpoint skeleton
- Database migration scripts

**Dependencies**: None (can run in parallel with existing code)
**Package additions**: None needed
**Risks & mitigations**:
- Risk: Breaking existing auth flow
- Mitigation: Carefully integrate with existing Better Auth JWT system
**Acceptance criteria**:
- New Conversation and Message models work with SQLModel
- Chat endpoint requires valid JWT authentication
- Database migration runs successfully

### Phase 2: MCP Tools Implementation
**Objective**: Create stateless tool functions that interact with the database
**Key deliverables**:
- `tools/mcp_tools.py` - add_task, list_tasks, complete_task, delete_task, update_task functions
- Unit tests for each tool function
- Proper user_id scoping for all operations

**Dependencies**: Phase 1 (needs auth foundation)
**Package additions**: None needed
**Risks & mitigations**:
- Risk: User data isolation issues
- Mitigation: All tools require user_id parameter and validate ownership
**Acceptance criteria**:
- Each tool function operates correctly with user_id scoping
- Tools return appropriate responses for Cohere consumption
- All user data remains properly isolated

### Phase 3: Cohere Agent & Chat Endpoint
**Objective**: Implement the Cohere integration with tool calling loop
**Key deliverables**:
- `agents/cohere_agent.py` - Cohere client and tool calling logic
- Enhanced `routers/chat.py` - Full chat endpoint implementation
- System prompt for task management behavior

**Dependencies**: Phases 1 & 2 (needs DB models and tools)
**Package additions**: `uv add cohere`
**Risks & mitigations**:
- Risk: Infinite tool calling loops
- Mitigation: Implement 5-iteration maximum as specified
**Acceptance criteria**:
- Cohere agent successfully calls MCP tools based on natural language
- Tool calling loop respects iteration limits
- Responses include proper confirmations

### Phase 4: Frontend Chat UI & Floating Icon
**Objective**: Create the user-facing chat interface
**Key deliverables**:
- `components/ChatIcon.tsx` - Floating chat icon component
- `components/ChatPanel.tsx` - Chat panel with message history
- API integration with `/api/chat` endpoint
- JWT token inclusion in requests

**Dependencies**: Phase 3 (needs working backend endpoint)
**Package additions**: None needed (using existing Shadcn/UI)
**Risks & mitigations**:
- Risk: UI conflicts with existing components
- Mitigation: Use existing Tailwind/Shadcn patterns
**Acceptance criteria**:
- Floating icon appears on all pages
- Chat panel opens/closes smoothly
- Messages display with proper user/assistant differentiation
- API calls include proper authentication

### Phase 5: Testing & Polish
**Objective**: Ensure quality and reliability of the implementation
**Key deliverables**:
- Comprehensive unit tests for backend components
- Integration tests for full chat flow
- Error handling and edge case coverage
- Performance optimization

**Dependencies**: All previous phases
**Package additions**: `uv add pytest` (if not already present)
**Risks & mitigations**:
- Risk: Poor AI response quality
- Mitigation: Fine-tune system prompt and tool definitions
**Acceptance criteria**:
- 80%+ code coverage achieved
- All natural language examples from spec work correctly
- Error scenarios handled gracefully

### Phase 6: Deployment & Documentation
**Objective**: Deploy to existing infrastructure and update documentation
**Key deliverables**:
- Updated README.md with COHERE_API_KEY setup
- Environment configuration for deployment
- Verification of zero-downtime deployment

**Dependencies**: All previous phases
**Package additions**: None
**Risks & mitigations**:
- Risk: Deployment conflicts with existing functionality
- Mitigation: Thorough testing in staging environment
**Acceptance criteria**:
- Feature deployed to Vercel/Hugging Face without breaking existing functionality
- Documentation updated with setup instructions
- Environment variables properly configured

## 3. Component Breakdown

### Backend modules
- `models/conversation.py`: SQLModel classes for Conversation and Message entities
- `tools/mcp_tools.py`: Stateless functions for task operations (add/list/complete/delete/update)
- `agents/cohere_agent.py`: Cohere client initialization and tool calling logic
- `routers/chat.py`: Chat endpoint with JWT auth and conversation management
- `core/config.py`: Cohere API key configuration

### DB models & migrations
- `Conversation`: Links to User, contains metadata about chat sessions
- `Message`: Stores individual messages with role, content, and timestamps
- Alembic migration scripts to create new tables

### Cohere integration logic
- Client initialization with COHERE_API_KEY
- Tool definitions in Cohere-compatible format
- Tool calling loop with iteration limit
- Error handling for API failures

### Frontend components
- `ChatIcon.tsx`: Floating button component using Shadcn/UI
- `ChatPanel.tsx`: Modal/side panel with message history and input
- `ChatMessage.tsx`: Individual message display component
- API service layer for `/api/chat` communication

## 4. Dependencies & Sequencing

```
Phase 1: DB & Auth Foundation
    ↓
Phase 2: MCP Tools          → Parallel: Frontend component scaffolding
    ↓
Phase 3: Cohere Agent & Endpoint
    ↓
Phase 4: Frontend UI Implementation
    ↓
Phase 5: Testing & Polish
    ↓
Phase 6: Deployment & Documentation
```

**Critical path**: Phases 1→2→3→4→5→6 (cannot be parallelized)
**Parallelizable work**:
- Frontend component development can begin after Phase 1
- Some testing can begin during Phase 3 implementation

## 5. Design Decisions & ADRs

### Decision 1: Direct Cohere SDK Integration vs Wrapper Libraries
**Context**: Need to integrate with Cohere's API for tool calling
**Chosen approach**: Direct integration using cohere.Client with native tool calling
**Alternatives considered**:
- OpenAI-compatible wrapper libraries
- Third-party agent frameworks
**Rationale**: Direct integration avoids unnecessary abstraction layers and ensures compatibility with Cohere's specific features
**Consequences**: More control over the integration, but requires staying up-to-date with Cohere's API changes

### Decision 2: Tool Calling Loop Implementation
**Context**: How to handle multiple tool calls in a single conversation turn
**Chosen approach**: Synchronous loop with 5-iteration maximum
**Alternatives considered**:
- Asynchronous processing with callbacks
- Single tool call per user message
**Rationale**: Synchronous approach is simpler to implement and debug, while the limit prevents infinite loops
**Consequences**: May result in longer response times for complex multi-step operations

### Decision 3: Floating Chat UI Strategy
**Context**: How to present the chat interface to users
**Chosen approach**: Fixed floating button that opens a modal panel
**Alternatives considered**:
- Always-visible sidebar
- Inline chat within main content area
- Full-screen chat overlay
**Rationale**: Floating button is unobtrusive but always accessible, modal provides focused chat experience
**Consequences**: Clean UI that doesn't interfere with main application flow

### Decision 4: Conversation Persistence Strategy
**Context**: How to manage conversation continuity across sessions
**Chosen approach**: Store full conversation history in database, allow multiple conversations per user
**Alternatives considered**:
- Single active conversation per user
- Client-side storage with server sync
- Temporary server memory with periodic persistence
**Rationale**: Database storage ensures reliability and allows users to resume previous conversations
**Consequences**: Additional database storage requirements but improved user experience

### Decision 5: Error Propagation Strategy
**Context**: How to handle and communicate errors from tools to users
**Chosen approach**: Transform technical errors into user-friendly messages while preserving essential information
**Alternatives considered**:
- Show raw technical error messages
- Hide all error details from users
- Redirect to support system
**Rationale**: Balance between transparency and user experience
**Consequences**: More robust error handling code but better user experience

### Decision 6: Package Management with uv
**Context**: How to manage Python dependencies for the backend
**Chosen approach**: Use uv exclusively for all Python package management
**Alternatives considered**:
- Continue using pip
- Mix uv and pip for different packages
**Rationale**: Consistency with project requirements and improved performance
**Consequences**: Need to learn uv commands but better long-term maintainability

## 6. Validation & Testing Strategy

### Unit tests
- MCP tools: Verify each function works correctly with different inputs and user contexts
- Database models: Test SQLModel functionality and relationships
- Cohere agent: Mock API calls and test tool calling logic

### Integration tests
- End-to-end chat flow: Simulate natural language inputs and verify correct tool calls
- Authentication: Verify JWT protection works correctly
- Database transactions: Test that all operations are properly isolated by user_id

### Manual test scenarios
Based on specification examples:
- "Add task: Buy milk" → Verify task creation and confirmation message
- "Show me pending tasks" → Verify task listing functionality
- "Complete task 1" → Verify task completion and confirmation

### Acceptance criteria mapping
- SC-001 (95% accuracy): Test with various natural language formulations of each operation
- SC-002 (5-second response): Benchmark API response times
- SC-005 (99% uptime): Test error recovery and graceful degradation

## 7. Risks & Mitigations

### Technical Risk 1: Cohere API Rate Limiting
**Impact**: High - Could cause service degradation
**Mitigation**: Implement retry logic with exponential backoff, monitor API usage, implement client-side queuing

### Technical Risk 2: Database Performance Under Load
**Impact**: Medium - Could slow down chat responses
**Mitigation**: Add proper indexes on user_id and conversation_id, implement connection pooling, optimize queries

### Cost Risk 1: High Cohere API Usage Costs
**Impact**: Medium - Could exceed budget constraints
**Mitigation**: Implement token counting and usage monitoring, optimize prompts for efficiency, set spending alerts

### Time Risk 1: Complex Tool Calling Logic
**Impact**: Medium - Could delay Phase 3 completion
**Mitigation**: Start with simple implementation and iterate, allocate extra time for debugging, prepare fallback approaches

### uv-related Risk 1: Dependency Management Issues
**Impact**: Low - Could complicate development process
**Mitigation**: Test uv commands early, maintain backup pip commands as fallback, ensure team familiar with uv

## 8. Timeline & Effort Estimate

**Total estimated effort**: 12-15 developer days

**Suggested sprint breakdown**:
- Sprint 1 (Days 1-3): Phase 1 & 2 - Database models and MCP tools
- Sprint 2 (Days 4-7): Phase 3 - Cohere integration and backend completion
- Sprint 3 (Days 8-10): Phase 4 - Frontend UI implementation
- Sprint 4 (Days 11-12): Phase 5 & 6 - Testing, polish, and deployment

## 9. Next Steps

1. **Immediate action**: Run `/sp.tasks` to generate implementation tasks from this plan
2. **Start implementation**: Begin with Phase 1 (Database & Auth Foundation)
3. **Follow workflow**: Proceed through phases sequentially, testing each phase before moving forward
4. **Monitor progress**: Regularly validate against success criteria from specification
5. **Prepare for deployment**: Coordinate with existing deployment pipeline for zero-downtime rollout