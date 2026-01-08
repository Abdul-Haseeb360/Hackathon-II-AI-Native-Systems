# Implementation Plan: Frontend Implementation for Multi-User Todo Web Application

**Branch**: `1-frontend-todo-app` | **Date**: 2026-01-07 | **Spec**: specs/1-frontend-todo-app/spec.md
**Input**: Feature specification from `/specs/1-frontend-todo-app/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement a Next.js 16+ frontend application with App Router for a multi-user todo web application. The implementation will include Better Auth with JWT authentication, a centralized API client that attaches JWT tokens to requests, authentication pages (login/signup), protected routes, and a dashboard with full CRUD functionality for todo tasks. The UI will use Shadcn/UI components with responsive design using Tailwind CSS.

## Technical Context

**Language/Version**: TypeScript with Next.js 16+ App Router
**Primary Dependencies**: Next.js, React, Tailwind CSS, Better Auth, Shadcn/UI, @radix-ui/react
**Storage**: API backend (no local storage)
**Testing**: Manual testing based on acceptance criteria from spec
**Target Platform**: Web browsers (Chrome, Firefox, Safari, Edge)
**Project Type**: Web frontend application
**Performance Goals**: All task CRUD operations complete within 3 seconds under normal network conditions
**Constraints**: <200ms p95 for UI interactions, responsive on 320px-1920px screen sizes, offline-capable for cached data
**Scale/Scope**: Multi-user system with data isolation per user

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] No manual coding - all via Claude Code prompts
- [x] Follows Spec-Driven Development principles
- [x] Uses Next.js with App Router as specified
- [x] Implements Better Auth with JWT as required
- [x] Uses Shadcn/UI components for UI elements
- [x] Responsive design with Tailwind CSS
- [x] Protected routes for authentication

## Project Structure

### Documentation (this feature)

```text
specs/1-frontend-todo-app/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
frontend/
├── src/
│   ├── app/
│   │   ├── (auth)/
│   │   │   ├── login/
│   │   │   │   └── page.tsx
│   │   │   └── signup/
│   │   │       └── page.tsx
│   │   ├── dashboard/
│   │   │   ├── page.tsx
│   │   │   └── layout.tsx
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   └── providers.tsx
│   ├── components/
│   │   ├── auth/
│   │   │   ├── login-form.tsx
│   │   │   └── signup-form.tsx
│   │   ├── dashboard/
│   │   │   ├── task-list.tsx
│   │   │   ├── task-form.tsx
│   │   │   └── task-item.tsx
│   │   ├── ui/           # Shadcn/UI components
│   │   │   ├── button.tsx
│   │   │   ├── input.tsx
│   │   │   ├── card.tsx
│   │   │   ├── table.tsx
│   │   │   ├── dialog.tsx
│   │   │   └── ...
│   │   └── protected-route.tsx
│   ├── lib/
│   │   ├── api.ts
│   │   ├── auth.ts
│   │   └── utils.ts
│   ├── hooks/
│   │   └── use-auth.ts
│   └── types/
│       └── index.ts
├── public/
├── .env.local
├── next.config.js
├── tailwind.config.js
├── tsconfig.json
└── package.json
```

**Structure Decision**: Web application structure selected with frontend directory containing Next.js app with App Router, component organization by feature (auth, dashboard) and type (ui components), and centralized API and auth utilities in lib folder.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [N/A] | [N/A] | [N/A] |

## Overview
- High-level architecture sketch (Next.js App Router → Server Components → Client Components for interactivity → Better Auth → API Client → Backend)
- Section structure outline

The frontend application will use Next.js App Router for routing and layout management. Server Components will handle initial data fetching and layout rendering, while Client Components will provide interactive functionality for authentication and task management. Better Auth will handle user sessions and JWT token management, which will be automatically attached to API requests via the centralized API client. The API client will communicate with the backend API to perform CRUD operations on todo tasks.

## Dependencies
- List all required packages (next, react, tailwind, better-auth, shadcn-ui, @radix-ui, classnames, etc.)
- Environment variables (.env.local): BETTER_AUTH_SECRET, BETTER_AUTH_URL, NEXT_PUBLIC_API_URL

### Core Dependencies:
- next: ^16.0.0
- react: ^19.0.0
- react-dom: ^19.0.0
- typescript: ^5.0.0
- tailwindcss: ^3.4.0

### Authentication Dependencies:
- better-auth: ^0.5.0
- better-auth/react: ^0.5.0

### UI Dependencies:
- shadcn/ui: latest
- @radix-ui/react-dialog: latest
- @radix-ui/react-checkbox: latest
- @radix-ui/react-label: latest
- @radix-ui/react-slot: latest
- class-variance-authority: ^0.7.0
- clsx: ^2.0.0
- lucide-react: ^0.450.0
- tailwind-merge: ^2.0.0
- tailwindcss-animate: ^1.0.0

### Utility Dependencies:
- zod: ^3.23.0
- react-hook-form: ^7.50.0

### Environment Variables:
- BETTER_AUTH_SECRET: Secret key for JWT signing
- BETTER_AUTH_URL: URL for Better Auth API
- NEXT_PUBLIC_API_URL: Public URL for the backend API

## Decisions Needing Documentation

| Decision Area | Options Considered | Final Choice | Rationale |
|---------------|-------------------|--------------|-----------|
| UI Library | Shadcn/UI vs Material UI vs Headless UI | Shadcn/UI | Specified in requirements as mandatory for all UI elements |
| Auth State Management | Better Auth built-in vs Zustand vs Context | Better Auth sessions | Better Auth provides comprehensive session management |
| API Client | fetch vs axios | fetch with custom wrapper | Next.js works well with fetch, custom wrapper for JWT |
| Form Handling | React Hook Form + Zod vs native | React Hook Form + Zod | Better validation and type safety |

## Testing Strategy
- Manual testing based on acceptance criteria from spec
- Validation: Signup → Login → Create task → View → Update → Toggle complete → Delete
- Responsive check on mobile/desktop
- Error handling (network fail, invalid login, expired token)

### Testing Approach:
1. Functional Testing: Complete user journey from signup to task management
2. Authentication Testing: Login, logout, protected route access
3. CRUD Testing: Create, read, update, delete tasks
4. UI Testing: Responsive design across screen sizes
5. Error Handling: Network failures, invalid inputs, expired tokens
6. Security Testing: Verify data isolation between users

## Technical Details
- Research approach: Concurrent (research Shadcn/UI components, Better Auth JWT setup while implementing)
- Project structure: /src/app, /src/components, /src/lib (api.ts, auth.ts), /src/ui (shadcn components)
- Shadcn/UI setup: init + add components (button, input, card, table, dialog, checkbox, etc.)

### Implementation Approach:
1. Research Better Auth JWT integration with Next.js App Router
2. Set up Shadcn/UI component library with required components
3. Implement API client with automatic JWT attachment
4. Create authentication pages and protected route components
5. Build dashboard with task management functionality
6. Implement responsive design with Tailwind CSS

## Implementation Steps (Sequential Phases)

### Phase 1: Project Initialization & Setup
1. Navigate to frontend folder
2. Initialize Next.js project with App Router and Tailwind CSS
3. Set up TypeScript configuration
4. Configure Tailwind CSS

### Phase 2: Shadcn/UI Installation and Configuration
1. Initialize Shadcn/UI in the project
2. Add required components: button, input, card, table, dialog, checkbox
3. Configure styling and themes

### Phase 3: Better Auth Setup with JWT Plugin
1. Install Better Auth dependencies
2. Configure authentication with JWT plugin
3. Set up environment variables
4. Implement session management

### Phase 4: API Client Implementation
1. Create centralized API client in /src/lib/api.ts
2. Implement JWT token attachment to requests
3. Add error handling and response parsing

### Phase 5: Authentication Pages (Login/Signup)
1. Create login page with form and validation
2. Create signup page with form and validation
3. Implement form submission and error handling

### Phase 6: Protected Layout & Route Protection
1. Create protected route component
2. Implement authentication checks
3. Set up dashboard layout with navigation

### Phase 7: Dashboard Page with Task List
1. Create dashboard page to display tasks
2. Implement task fetching and display
3. Add loading states and error handling

### Phase 8: Task CRUD Forms & Modals
1. Create task creation form
2. Implement task editing functionality
3. Add task deletion confirmation
4. Implement task completion toggle

### Phase 9: Polish: Loading States, Error Handling, Responsiveness
1. Add loading indicators
2. Implement comprehensive error handling
3. Ensure responsive design across all components
4. Add animations and transitions

### Phase 10: Final Validation & Testing
1. Test complete user flow
2. Verify all acceptance criteria from spec
3. Validate responsive design
4. Test error scenarios

## Final Validation
- Run commands: npm run dev (port 3000)
- Full user flow works: signup → login → manage tasks → logout
- JWT automatically attached to API calls
- UI uses Shadcn/UI components consistently

### Validation Checklist:
- [ ] Application starts successfully with `npm run dev`
- [ ] User can register with valid credentials
- [ ] User can login with valid credentials
- [ ] Unauthenticated users redirected to login page
- [ ] Authenticated users can access dashboard
- [ ] Users can create new tasks
- [ ] Users can view their task list
- [ ] Users can update task details
- [ ] Users can mark tasks as complete/incomplete
- [ ] Users can delete tasks
- [ ] JWT tokens automatically attached to API requests
- [ ] UI is responsive on mobile and desktop
- [ ] All Shadcn/UI components are used consistently
- [ ] Error handling works for invalid inputs and network failures
- [ ] Users can only see their own tasks (data isolation verified)