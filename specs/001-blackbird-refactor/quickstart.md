# Quickstart Guide: Blackbird Refactor Development

**Feature**: 001-blackbird-refactor
**Date**: 2025-11-17
**Purpose**: Guide for setting up local development environment and running the application

## Prerequisites

- **Python 3.11** (specified in `.python-version`)
- **Node.js 18+** and npm (for React frontend)
- **Git** (for version control)
- **Anthropic API Key** (for Claude AI integration)
- **HuggingFace Account** (for initial data migration)

## Project Structure

```
fastapi-demo/
├── backend/          # Python FastAPI backend
├── frontend/         # React TypeScript frontend
├── database/         # SQLite database files (gitignored)
├── specs/            # Feature specifications (SpecKit)
├── .env             # Environment variables (gitignored)
└── .env.example     # Example environment file
```

## Initial Setup

### 1. Clone Repository

```bash
git clone https://github.com/aie-onramp/fastapi-demo.git
cd fastapi-demo
git checkout 001-blackbird-refactor
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python3.11 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp ../.env.example ../.env
# Edit .env and add your ANTHROPIC_API_KEY
```

### 3. Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install

# Frontend connects to backend via proxy (configured in vite.config.ts)
```

### 4. Database Setup & Migration

```bash
cd ../backend

# Initialize database schema
python -m src.database.migrations.init_schema

# Migrate data from HuggingFace
python -m src.database.migrations.migrate_from_hf

# Verify migration
python -m src.database.migrations.verify_migration
```

**Expected Output**:
```
✓ Database schema created
✓ Migrated 10 customers
✓ Migrated 13 orders
✓ Referential integrity verified
✓ Migration complete
```

## Running the Application

### Development Mode (Recommended)

**Terminal 1 - Backend**:
```bash
cd backend
source .venv/bin/activate
uvicorn src.main:app --reload --port 8000
```

**Terminal 2 - Frontend**:
```bash
cd frontend
npm run dev
```

**Access the application**:
- Frontend: http://localhost:5173
- Backend API docs: http://localhost:8000/docs (Swagger UI)
- Backend health: http://localhost:8000/api/v1/health

### Production Mode

```bash
# Build frontend
cd frontend
npm run build

# Serve frontend static files via FastAPI
cd ../backend
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

## Environment Variables

Create `.env` file in project root:

```bash
# Claude AI Configuration
ANTHROPIC_API_KEY=sk-ant-api03-...

# Database Configuration
DATABASE_URL=sqlite:///./database/blackbird.db

# Application Settings
ENVIRONMENT=development
LOG_LEVEL=INFO

# Frontend (optional, for production deployment)
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

## Testing

### Backend Tests

```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test suites
pytest tests/unit/           # Unit tests only
pytest tests/integration/    # Integration tests only
pytest tests/contract/       # Contract tests only

# Run tests in parallel
pytest -n auto
```

### Frontend Tests

```bash
cd frontend

# Run unit tests
npm test

# Run tests with coverage
npm run test:coverage

# Run E2E tests (requires backend running)
npm run test:e2e
```

## Development Workflow

### 1. Starting a New Task

```bash
# Ensure you're on the feature branch
git checkout 001-blackbird-refactor

# Pull latest changes
git pull origin 001-blackbird-refactor

# Create task branch (optional, for complex tasks)
git checkout -b task/implement-customer-api
```

### 2. Test-Driven Development (TDD - MANDATORY)

**Write tests FIRST**, then implement:

```bash
# 1. Write failing test
cd backend
vim tests/contract/test_customer_api.py

# 2. Run test - should FAIL
pytest tests/contract/test_customer_api.py -v

# 3. Implement feature
vim src/api/customers.py

# 4. Run test - should PASS
pytest tests/contract/test_customer_api.py -v

# 5. Refactor if needed, tests still passing
```

### 3. Running Linters

```bash
# Backend
cd backend
ruff check src/                # Lint
ruff format src/               # Format
mypy src/                      # Type check

# Frontend
cd frontend
npm run lint                   # ESLint
npm run format                 # Prettier
npm run type-check             # TypeScript
```

### 4. Committing Changes

```bash
# Stage changes
git add .

# Commit with descriptive message
git commit -m "feat(api): implement customer search endpoint

- Add POST /customers/search endpoint
- Add contract tests for search functionality
- Handle exact match for email/phone/username
- Return 400 for invalid search keys"

# Push to remote
git push origin 001-blackbird-refactor
```

## Common Development Tasks

### Add a New API Endpoint

1. **Define contract** in `specs/001-blackbird-refactor/contracts/api-spec.yaml`
2. **Write contract test** in `backend/tests/contract/`
3. **Implement endpoint** in `backend/src/api/`
4. **Add service logic** in `backend/src/services/`
5. **Run tests** to verify
6. **Update frontend** to consume endpoint

### Add a New AI Tool

1. **Define tool schema** in `specs/001-blackbird-refactor/contracts/ai-tools.md`
2. **Write tool test** in `backend/tests/integration/test_ai_tools.py`
3. **Implement in ToolHandler** (`backend/src/services/tool_handler.py`)
4. **Register in ChatService** (`backend/src/services/chat_service.py`)
5. **Test with chat interface**

### Add a New React Component

1. **Write component test** in `frontend/tests/unit/`
2. **Implement component** in `frontend/src/components/`
3. **Add to Storybook** (if using) for visual testing
4. **Integrate into page**

### Database Schema Changes

1. **Update models** in `backend/src/models/`
2. **Create migration script** in `backend/src/database/migrations/`
3. **Test migration** on development database
4. **Update data model docs** (`specs/001-blackbird-refactor/data-model.md`)

## Troubleshooting

### Backend won't start

**Error**: `ModuleNotFoundError: No module named 'anthropic'`
**Solution**:
```bash
cd backend
source .venv/bin/activate
pip install -r requirements.txt
```

### Database errors

**Error**: `sqlite3.OperationalError: no such table: customers`
**Solution**:
```bash
python -m src.database.migrations.init_schema
```

### Claude API rate limiting

**Error**: `429 Too Many Requests`
**Solution**: The application handles this gracefully with the message:
"Ruh roh Raggy! It's the dreaded rate limiting error from Hugging Face again!"

Wait a few minutes and try again.

### Frontend can't connect to backend

**Error**: `Network Error` in browser console
**Solution**:
1. Verify backend is running: `curl http://localhost:8000/api/v1/health`
2. Check Vite proxy configuration in `vite.config.ts`
3. Ensure CORS is enabled in FastAPI (`src/main.py`)

### Tests failing unexpectedly

```bash
# Clear pytest cache
rm -rf .pytest_cache
rm -rf **/__pycache__

# Reinstall dependencies
pip install --force-reinstall -r requirements.txt

# Run tests with verbose output
pytest -vv
```

## Development Tools

### API Testing

**Swagger UI**: http://localhost:8000/docs
- Interactive API documentation
- Test endpoints directly
- View request/response schemas

**cURL Examples**:
```bash
# Get all customers
curl http://localhost:8000/api/v1/customers

# Search customer by email
curl -X POST http://localhost:8000/api/v1/customers/search \
  -H "Content-Type: application/json" \
  -d '{"key": "email", "value": "john@example.com"}'

# Send chat message
curl -X POST http://localhost:8000/api/v1/chat/message \
  -H "Content-Type: application/json" \
  -d '{"message": "Look up customer with email john@example.com"}'
```

### Database Inspection

```bash
# SQLite CLI
sqlite3 database/blackbird.db

# View tables
.tables

# View schema
.schema customers

# Run query
SELECT * FROM customers WHERE email LIKE '%example.com';

# Exit
.quit
```

### Logging

Logs are written to stdout with structured format:

```bash
# Backend logs
cd backend
uvicorn src.main:app --reload --log-level debug

# View logs in real-time
tail -f logs/app.log  # if file logging configured
```

## Next Steps

1. **Review the spec**: Read [`spec.md`](./spec.md) for full requirements
2. **Review the plan**: Read [`plan.md`](./plan.md) for architecture details
3. **Review contracts**: Read [`contracts/api-spec.yaml`](./contracts/api-spec.yaml) and [`contracts/ai-tools.md`](./contracts/ai-tools.md)
4. **Start with tests**: Follow TDD workflow (tests → implementation → refactor)
5. **Commit frequently**: Small, focused commits with clear messages

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [SQLAlchemy ORM Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/)
- [Anthropic Claude API](https://docs.anthropic.com/claude/reference/messages)
- [Vite Guide](https://vitejs.dev/guide/)
- [pytest Documentation](https://docs.pytest.org/)
- [SpecKit Framework](../.specify/README.md)

## Getting Help

- Check existing tests for examples
- Review similar implementations in the codebase
- Consult API documentation
- Ask specific questions in code review comments
- Reference the [CLAUDE.md](../../CLAUDE.md) file for project guidance

---

**Ready to Start?** Run through the Initial Setup section, then begin with the first task in [`tasks.md`](./tasks.md) (generated by `/speckit.tasks` command).
