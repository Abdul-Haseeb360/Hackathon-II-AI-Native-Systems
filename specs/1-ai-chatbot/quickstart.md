# Quickstart Guide: AI Todo Chatbot

## Prerequisites
- Python 3.11+
- Node.js 18+
- UV package manager installed
- PostgreSQL database (Neon recommended)
- Cohere API key

## Setup

### Backend Setup
1. Clone the repository and navigate to the backend directory
2. Install dependencies using UV:
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv sync
   ```
3. Set environment variables:
   ```bash
   export COHERE_API_KEY="your-cohere-api-key"
   export DATABASE_URL="postgresql://..."
   export JWT_SECRET="your-jwt-secret"
   ```
4. Run database migrations:
   ```bash
   uv run alembic upgrade head
   ```
5. Start the backend:
   ```bash
   uv run uvicorn main:app --reload
   ```

### Frontend Setup
1. Navigate to the frontend directory
2. Install dependencies:
   ```bash
   npm install
   ```
3. Set environment variables in `.env.local`:
   ```bash
   NEXT_PUBLIC_API_BASE_URL="http://localhost:8000"
   ```
4. Start the development server:
   ```bash
   npm run dev
   ```

## Using the AI Chatbot

### Starting a Conversation
1. Log in to the application
2. Click the floating chat icon in the bottom-right corner
3. Type a natural language command, such as:
   - "Add a task to buy groceries"
   - "Show me my pending tasks"
   - "Complete task number 1"
   - "Update task 2 to 'Buy organic groceries'"
   - "Delete task 3"

### Expected Behavior
- The AI will interpret your natural language command
- If tools need to be called, the system will execute them
- You'll receive a confirmation response with the result
- Conversation history will be preserved in the database

## Development

### Adding New Tools
1. Create a new function in `tools/mcp_tools.py`
2. Ensure it accepts a `user_id` parameter for proper isolation
3. Register the tool in the Cohere agent's tool definitions
4. Test with various natural language inputs

### Modifying the Chat Interface
1. Update components in `components/Chat*.tsx`
2. Modify the API call in the frontend service layer
3. Ensure JWT authentication is properly passed with each request