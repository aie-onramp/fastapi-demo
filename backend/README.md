# Blackbird Backend

FastAPI backend for the Blackbird Customer Support Application with Claude AI integration.

## Quick Start

### Prerequisites

- Python 3.11 or higher
- Anthropic API key ([Get one here](https://console.anthropic.com/))

### Setup

1. **Create virtual environment**:
```bash
cd backend
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. **Install dependencies**:
```bash
uv pip install -r requirements.txt
```

3. **Configure environment**:
```bash
# Note: .env should be at project root (one level up from backend/)
# The backend/main.py loads environment variables from the parent directory
# If .env doesn't exist, copy from template:
cp ../.env.example ../.env

# Edit .env and add your ANTHROPIC_API_KEY
nano ../.env
```

4. **Run database migration**:
```bash
# Important: Run this from the backend/ directory
# This creates backend/blackbird.db with sample data
python migrate_data.py
```

Expected output:
```
✓ Database schema created
✓ Migrated 10 customers
✓ Migrated 13 orders
✓ Migration complete
```

**Note:** The database file `blackbird.db` will be created in the `backend/` directory due to the relative path in `database.py`.

5. **Start development server**:
```bash
uvicorn main:app --reload --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive docs**: http://localhost:8000/docs
- **Health check**: http://localhost:8000/api/health

## Project Structure

```
backend/
├── main.py              # FastAPI app and routes
├── models.py            # Pydantic schemas
├── ai_tools.py          # Claude AI integration
├── database.py          # SQLite queries
├── migrate_data.py      # HuggingFace → SQLite migration
├── requirements.txt     # Python dependencies
└── tests/               # API tests
    ├── conftest.py      # Pytest fixtures
    └── test_api.py      # API contract tests
```

## API Endpoints

### Chat
- `POST /api/chat` - Send message to Claude AI assistant

### Customers
- `GET /api/customers` - List all customers
- `GET /api/customers/{id}` - Get customer by ID
- `POST /api/customers/search` - Search customers by email/phone/username
- `PATCH /api/customers/{id}` - Update customer contact info
- `GET /api/customers/{id}/orders` - Get customer's orders

### Orders
- `GET /api/orders` - List all orders (supports `?status=` filter)
- `GET /api/orders/{id}` - Get order by ID
- `PATCH /api/orders/{id}/cancel` - Cancel order (only if status=Processing)

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_api.py -v

# Run specific test
pytest tests/test_api.py::test_chat_endpoint -v
```

## Claude AI Integration

The backend integrates with Claude 4.5 Haiku using 6 function calling tools:

1. **get_user** - Search customer by email/phone/username
2. **get_order_by_id** - Lookup order details
3. **get_customer_orders** - Get all orders for a customer
4. **cancel_order** - Cancel an order (if Processing status)
5. **update_user_contact** - Update customer email/phone
6. **get_user_info** - Get customer + orders combined

See [specs/001-blackbird-refactor/contracts/ai-tools.md](../specs/001-blackbird-refactor/contracts/ai-tools.md) for full tool specifications.

## Database

- **Type**: SQLite 3.x (embedded, no server needed)
- **File**: `blackbird.db` (created by migration script)
- **Tables**: `customers`, `orders`
- **Sample data**: 10 customers, 13 orders (from HuggingFace datasets)

### Inspect database:
```bash
sqlite3 blackbird.db

# View tables
.tables

# Query customers
SELECT * FROM customers;

# Exit
.quit
```

## Development

**Important:** All commands in this section assume you're in the `backend/` directory with your virtual environment activated.

### Running in development mode:
```bash
# With auto-reload
uvicorn main:app --reload

# With custom port
uvicorn main:app --reload --port 8080

# With debug logging
uvicorn main:app --reload --log-level debug
```

### Linting and formatting:
```bash
# Check code
ruff check .

# Format code
ruff format .
```

## Troubleshooting

### "Defaulting to user installation because normal site-packages is not writeable"

**Cause**: Using `pip` instead of `uv pip` with uv-created virtual environments

**Solution**:
```bash
# Use uv pip, not pip
cd backend
rm -rf .venv  # Clean start
uv venv
source .venv/bin/activate  # Optional (uv auto-detects .venv)
uv pip install -r requirements.txt
```

**Why**: `uv venv` doesn't install pip in the virtual environment by default. Always use `uv pip` for package management with uv-created environments.

### "ImportError: cannot import name 'HfFolder' from 'huggingface_hub'"

**Cause**: Version mismatch between `datasets` and `huggingface_hub` packages

**Solution**:
```bash
# Ensure you have updated requirements.txt
cd backend
rm -rf .venv
uv venv
uv pip install -r requirements.txt
```

**Why**: Old versions of `datasets` (2.15.0) tried to import `HfFolder` which was removed in `huggingface_hub` v1.0+. Updated `datasets>=3.0.0` is compatible with modern `huggingface_hub`.

### ModuleNotFoundError
```bash
# Make sure virtual environment is created and packages installed
cd backend
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

### Database not found
```bash
# Run migration script from backend/ directory
cd backend
python migrate_data.py
```

### Claude API errors
- Check `ANTHROPIC_API_KEY` in `.env` (at project root)
- Verify API key is valid at https://console.anthropic.com/
- Check for rate limiting (429 errors)

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Anthropic Claude API](https://docs.anthropic.com/claude/reference/messages)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
