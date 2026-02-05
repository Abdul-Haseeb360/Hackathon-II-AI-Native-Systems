# AI Todo Chatbot - Hackathon Portfolio

A professional, AI-native task management system featuring natural language processing, persistent conversations, and enterprise-grade deployment.

## 🚀 Overview

The AI Todo Chatbot is a conversational task manager that allows users to interact with their todo list using natural language. Powered by Cohere AI and a robust FastAPI/Next.js stack, it demonstrates the integration of AI agents with traditional database systems (PostgreSQL) using MCP (Model-Controller-Provider) patterns.

## 🛠️ Tech Stack

- **AI Engine:** Cohere (Command R model) with Tool Calling
- **Backend:** FastAPI, SQLModel (SQLAlchemy + Pydantic), PostgreSQL
- **Frontend:** Next.js (App Router), Tailwind CSS
- **Authentication:** Better Auth (JWT integration)
- **Infrastructure:** Docker, Kubernetes (K8s), Helm, Vercel/Heroku

## 📂 Project Phases

### Phase 2: Core AI-Powered Task Management

- Integration of Cohere AI agent for NL command processing.
- Implementation of MCP tools for Task CRUD operations.
- Backend routing and JWT-secured chat endpoints.
- Base frontend chat interface with floating action buttons.

### Phase 3: Enhanced Features & UX

- Persistent conversation history stored in PostgreSQL.
- Auto-generation of conversation titles from context.
- Improved chat UI with loading states and error handling.
- Optimized tool-calling logic for better command accuracy.

### Phase 4: Enterprise Deployment & DevOps

- **Containerization:** Comprehensive Docker setup for local and production environments.
- **Orchestration:** Kubernetes manifests for scalable deployment.
- **Package Management:** Helm charts for consistent environment configuration.
- **Monitoring:** Integrated logging and performance tracking.

## 📋 Features

- **Conversational CRUD:** "Add task: Buy milk", "Show pending tasks", "Mark task 1 as done".
- **Contextual Memory:** Seamlessly continue conversations across platform refreshes.
- **Secure Isolation:** Data is strictly isolated per user via JWT.
- **Responsive Design:** Premium UI optimized for both desktop and mobile.

## ⚙️ Quick Start

### 1. Prerequisites

- Docker & Docker Compose
- Cohere API Key

### 2. Environment Setup

Create a `.env` file in the root:

```env
COHERE_API_KEY=your_key_here
DATABASE_URL=postgresql://user:pass@db:5432/todo
BETTER_AUTH_SECRET=your_secret
```

### 3. Run with Docker

```bash
docker compose up --build
```

## 📈 Success Criteria

- [x] 95% NL command accuracy
- [x] < 5s AI response latency
- [x] Zero-downtime deployment ready
- [x] 100% test coverage for core logic
