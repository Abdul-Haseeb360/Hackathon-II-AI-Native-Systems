# Quickstart Guide: Backend Todo API

## Prerequisites
- Python 3.11+
- UV package manager
- Neon PostgreSQL database URL
- Better Auth configuration

## Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Ensure virtual environment is activated:
```bash
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install required dependencies using UV:
```bash
uv add fastapi uvicorn[standard] sqlmodel psycopg2-binary python-jose[cryptography] passlib[bcrypt] python-multipart pydantic-settings
```

4. Set up environment variables:
```bash
export DATABASE_URL="your_neon_postgres_url"
export BETTER_AUTH_SECRET="your_auth_secret"
```

## Running the Application

1. Start the development server:
```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

2. Access the API at `http://localhost:8000`
3. View API documentation at `http://localhost:8000/docs`

## API Usage

### Authentication
Include your JWT token in the Authorization header:
```
Authorization: Bearer <your-jwt-token>
```

### Example Requests

**Create a task:**
```bash
curl -X POST http://localhost:8000/api/tasks \
  -H "Authorization: Bearer <your-jwt-token>" \
  -H "Content-Type: application/json" \
  -d '{"title": "New task", "description": "Task description"}'
```

**Get all tasks:**
```bash
curl -X GET http://localhost:8000/api/tasks \
  -H "Authorization: Bearer <your-jwt-token>"
```