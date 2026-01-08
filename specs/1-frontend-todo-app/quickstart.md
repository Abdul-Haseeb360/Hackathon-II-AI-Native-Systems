# Quickstart Guide: Frontend Todo Application

## Prerequisites
- Node.js 18+ installed
- npm package manager
- Access to backend API (already deployed)
- Better Auth account or secret key for JWT

## Setup Instructions

### 1. Initialize the Project
```bash
# Navigate to frontend directory
cd frontend

# Initialize Next.js project with required configurations
npx create-next-app@latest . --typescript --tailwind --eslint --app --src-dir --import-alias "@/*"
```

### 2. Install Dependencies
```bash
# Core dependencies
npm install next react react-dom typescript

# Authentication dependencies
npm install better-auth better-auth/react

# UI dependencies
npx shadcn@latest init
npx shadcn@latest add button input card table dialog checkbox label slot

# Form handling
npm install react-hook-form zod @hookform/resolvers

# Utility dependencies
npm install class-variance-authority clsx tailwind-merge lucide-react tailwindcss-animate
```

### 3. Environment Configuration
Create a `.env.local` file in the frontend directory:
```env
BETTER_AUTH_SECRET=your-better-auth-secret-here
BETTER_AUTH_URL=http://localhost:8080  # Backend auth URL
NEXT_PUBLIC_API_URL=http://localhost:8080  # Backend API URL
```

### 4. Project Structure
After setup, your project structure should look like:
```
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
│   │   ├── dashboard/
│   │   ├── ui/           # Shadcn/UI components
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

## Development Workflow

### 1. Start Development Server
```bash
npm run dev
```
The application will be available at http://localhost:3000

### 2. Key Implementation Steps
1. **API Client Setup**: Implement centralized API client in `src/lib/api.ts` with JWT token attachment
2. **Authentication**: Set up Better Auth in `src/lib/auth.ts` and create auth context
3. **Protected Routes**: Implement route protection component
4. **Authentication Pages**: Create login and signup pages with forms
5. **Dashboard**: Build task list and CRUD functionality

### 3. Testing the Application
1. Register a new user account
2. Log in to access the dashboard
3. Create, read, update, and delete tasks
4. Verify responsive design on different screen sizes
5. Test error handling scenarios

## Key Files to Implement

### API Client (`src/lib/api.ts`)
```typescript
// Centralized API client that automatically attaches JWT tokens
// Implements error handling and response parsing
```

### Authentication (`src/lib/auth.ts`)
```typescript
// Better Auth configuration and session management
// JWT token handling and user state
```

### Types (`src/types/index.ts`)
```typescript
// TypeScript interfaces for User, Todo Task, and API responses
```

## Common Commands
```bash
# Start development server
npm run dev

# Build for production
npm run build

# Run type checking
npm run type-check

# Lint code
npm run lint
```

## Troubleshooting

### Environment Variables Not Loading
- Ensure `.env.local` file is in the root of the frontend directory
- Restart development server after adding environment variables

### Authentication Issues
- Verify that `BETTER_AUTH_URL` points to the running backend
- Check that `BETTER_AUTH_SECRET` matches the backend configuration

### API Requests Failing
- Confirm that `NEXT_PUBLIC_API_URL` points to the backend API
- Verify JWT tokens are being attached to requests properly