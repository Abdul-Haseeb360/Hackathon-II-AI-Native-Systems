# Backend Setup

## Prerequisites
- Python 3.11+
- UV package manager
- PostgreSQL database
- Cohere API key

## Setup
1. Install dependencies:
   ```bash
   uv sync
   ```

2. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Add your Cohere API key to `COHERE_API_KEY` in the `.env` file
   - Configure your database URL in `DATABASE_URL`

3. Run database migrations:
   ```bash
   uv run python migrate_conversation_tables.py
   ```

## Running the Application
```bash
cd backend
uvicorn main:app --reload --port 8000
```

## Deployment

### Heroku Deployment
1. Create a new Heroku app:
   ```bash
   heroku create your-app-name
   ```

2. Set environment variables:
   ```bash
   heroku config:set COHERE_API_KEY=your_cohere_api_key
   heroku config:set DATABASE_URL=your_database_url
   heroku config:set BETTER_AUTH_SECRET=your_auth_secret
   heroku config:set BETTER_AUTH_URL=https://your-app-name.herokuapp.com
   ```

3. Deploy:
   ```bash
   git push heroku main
   ```

### Other Platforms
For deployment to other platforms like Render, Railway, or Fly.io, ensure the following:
- Set the `COHERE_API_KEY` environment variable
- Set the `DATABASE_URL` environment variable
- Set the `BETTER_AUTH_SECRET` environment variable
- Use the `Procfile` provided in the repository
- Run the migration script after deployment

### Zero-Downtime Deployment
The application is designed for zero-downtime deployment:
- The API endpoints are stateless and can scale horizontally
- Database migrations are designed to be backward compatible
- New deployments won't interrupt existing user sessions
- Health checks are available at the root endpoint (`/`)

### Monitoring and Logging
The application includes comprehensive monitoring:
- All requests and responses are logged with timestamps
- Performance metrics track response times
- Error logging captures all exceptions with context
- Token usage for the Cohere API is monitored for cost control
- Database queries are logged for performance analysis
