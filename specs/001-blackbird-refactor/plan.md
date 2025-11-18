# Implementation Plan: Blackbird Customer Support Application Refactor

**Branch**: `001-blackbird-refactor` | **Date**: 2025-11-17 | **Spec**: [spec.md](./spec.md)

**Educational Context**: Teaching application for AI Engineering Onramp course - focus on AI integration, not production architecture

## Summary

Refactor Blackbird from Gradio + HuggingFace datasets to React + FastAPI + SQLite. Core learning objective: **Claude AI function calling integration**. Students learn modern web development (React + FastAPI) with real AI capabilities.

**Original Gradio App → React Refactor:**
- Chat tab with AI → ChatPage.jsx + Claude API
- Customer data tab → CustomersPage.jsx + REST API
- Order data tab → OrdersPage.jsx + REST API

## Technical Context

**Language**: Python 3.11 (backend), JavaScript (frontend)
**Dependencies**:
- Backend: FastAPI, Anthropic SDK, Pydantic, uvicorn
- Frontend: React 18, Vite
**Storage**: SQLite (basic, no optimization)
**Testing**: Basic API tests (pytest), manual UI testing
**Scope**: ~1,600 LOC total (~800 backend, ~600 frontend, ~200 tests)

## Educational Simplifications

**Removed for Clarity:**
- ❌ Layered architecture (services/schemas/models layers)
- ❌ Conversation history storage (P3 user story)
- ❌ Production logging/monitoring/audit trails
- ❌ Performance optimization (WAL mode, pooling)
- ❌ Comprehensive testing (E2E, integration, unit)
- ❌ TypeScript, TanStack Query, custom hooks
- ❌ SLA/performance requirements

**Core Learning Focus:**
- ✅ Claude AI function calling (6 tools) - **PRIMARY OBJECTIVE**
- ✅ FastAPI routing and request/response handling
- ✅ React components and state management
- ✅ Data migration (HuggingFace → SQLite)
- ✅ REST API design basics

## Project Structure

### Backend (4 files, ~800 LOC)

```
backend/
├── main.py              # FastAPI app + routes (~400 LOC)
│                        # - Customer CRUD endpoints
│                        # - Order CRUD endpoints
│                        # - POST /api/chat (Claude integration)
│
├── models.py            # Pydantic request/response models (~200 LOC)
│                        # - Customer, Order schemas
│                        # - ChatMessage request/response
│
├── ai_tools.py          # Claude AI integration (~300 LOC)
│                        # - 6 function calling tools
│                        # - Tool execution handler
│                        # - Anthropic API client
│
├── database.py          # SQLite connection + queries (~100 LOC)
│                        # - get_db() connection
│                        # - Basic CRUD SQL functions
│
├── migrate_data.py      # HF datasets → SQLite (~150 LOC)
│                        # - Load from dwb2023/blackbird-customers
│                        # - Load from dwb2023/blackbird-orders
│                        # - Insert into SQLite with validation
│
├── requirements.txt     # Dependencies (6 packages)
└── tests/
    ├── test_api.py      # API contract tests (~200 LOC)
    └── conftest.py      # Pytest setup
```

### Frontend (8 files, ~600 LOC)

```
frontend/
├── src/
│   ├── App.jsx              # Main app + routing (~80 LOC)
│   │                        # - React Router setup
│   │                        # - Navigation between pages
│   │
│   ├── api.js               # Fetch API wrapper (~100 LOC)
│   │                        # - fetchCustomers(), updateCustomer()
│   │                        # - fetchOrders(), cancelOrder()
│   │                        # - sendChatMessage()
│   │
│   ├── pages/
│   │   ├── ChatPage.jsx     # Chat interface (~150 LOC)
│   │   │                    # - Message history display
│   │   │                    # - Input + send button
│   │   │                    # - Call POST /api/chat
│   │   │
│   │   ├── CustomersPage.jsx # Customer management (~120 LOC)
│   │   │                     # - DataTable component
│   │   │                     # - Search bar
│   │   │                     # - Inline edit
│   │   │
│   │   └── OrdersPage.jsx    # Order management (~120 LOC)
│   │                         # - DataTable component
│   │                         # - Status filter dropdown
│   │                         # - Cancel button
│   │
│   └── components/
│       ├── ChatMessage.jsx  # Message display (~40 LOC)
│       ├── DataTable.jsx    # Reusable table (~80 LOC)
│       └── SearchBar.jsx    # Search input (~30 LOC)
│
├── index.html               # HTML entry point
├── package.json             # Dependencies (react, react-router-dom, vite)
├── vite.config.js           # Vite build config
└── README.md
```

### Database

```
blackbird.db                 # SQLite file (gitignored)
```

## Gradio → React Component Mapping

| Gradio UI | React Component | Backend | Learning Objective |
|-----------|----------------|---------|-------------------|
| Chat tab + message list | ChatPage.jsx | POST /api/chat | **Claude AI function calling** |
| Customer data table | CustomersPage.jsx | GET /api/customers | REST API + React state |
| Customer search | SearchBar | GET /api/customers/search | Query parameters |
| Customer edit inline | Form in DataTable | PATCH /api/customers/{id} | PATCH requests |
| Order data table | OrdersPage.jsx | GET /api/orders | Data fetching |
| Order status filter | Dropdown | GET /api/orders?status={} | Query filtering |
| Order cancel button | Button | PATCH /api/orders/{id}/cancel | Business logic validation |

## Backend Endpoint Mapping

| Original Tool | FastAPI Endpoint | Method | Description |
|--------------|------------------|--------|-------------|
| get_user(key, value) | /api/customers/search | POST | Search by email/phone/username |
| get_order_by_id(id) | /api/orders/{id} | GET | Get order details |
| get_customer_orders(customer_id) | /api/customers/{id}/orders | GET | Get customer's orders |
| cancel_order(id) | /api/orders/{id}/cancel | PATCH | Cancel if status=Processing |
| update_user_contact(id, email, phone) | /api/customers/{id} | PATCH | Update contact info |
| get_user_info(key, value) | /api/customers/{id} | GET | Get customer + orders |
| Chat message | /api/chat | POST | Send to Claude, execute tools, return response |

## Claude AI Integration (Core Learning)

### 6 Function Calling Tools

```python
# ai_tools.py

TOOLS = [
    {
        "name": "get_user",
        "description": "Search customer by email, phone, or username",
        "input_schema": {
            "type": "object",
            "properties": {
                "key": {"type": "string", "enum": ["email", "phone", "username"]},
                "value": {"type": "string"}
            },
            "required": ["key", "value"]
        }
    },
    # ... 5 more tools (get_order_by_id, get_customer_orders, cancel_order,
    #                  update_user_contact, get_user_info)
]

def execute_tool(tool_name, tool_input):
    """Execute tool and return result"""
    if tool_name == "get_user":
        return db.search_customer(tool_input["key"], tool_input["value"])
    # ... handle other tools

async def chat_with_claude(message, conversation_history):
    """Send message to Claude with tools, execute tool calls, return response"""
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    # Send to Claude with tools
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",  # Claude 4.5 Haiku
        max_tokens=1024,
        tools=TOOLS,
        messages=conversation_history + [{"role": "user", "content": message}]
    )

    # If tool use, execute and continue conversation
    if response.stop_reason == "tool_use":
        tool_results = []
        for tool_use in response.content:
            if tool_use.type == "tool_use":
                result = execute_tool(tool_use.name, tool_use.input)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": tool_use.id,
                    "content": json.dumps(result)
                })

        # Send tool results back to Claude
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",  # Claude 4.5 Haiku
            max_tokens=1024,
            tools=TOOLS,
            messages=conversation_history + [
                {"role": "user", "content": message},
                {"role": "assistant", "content": response.content},
                {"role": "user", "content": tool_results}
            ]
        )

    return response.content[0].text
```

**Key Learning Points:**
1. Tool schema definition (JSON schema for function parameters)
2. Claude API integration (messages.create with tools parameter)
3. Tool use detection (stop_reason == "tool_use")
4. Tool execution (map tool name to database function)
5. Multi-turn conversation (send tool results back to Claude)

## Data Model

### Customer (2 tables only - no conversation history)

```sql
CREATE TABLE customers (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone TEXT NOT NULL,
    username TEXT NOT NULL UNIQUE
);

CREATE TABLE orders (
    id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL,
    product TEXT NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    price REAL NOT NULL CHECK (price >= 0),
    status TEXT NOT NULL CHECK (status IN ('Processing', 'Shipped', 'Delivered', 'Cancelled')),
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);
```

**Validation Rules:**
- Email format: standard email regex
- Phone format: XXX-XXX-XXXX
- Username: 3-20 chars, alphanumeric + underscore
- Order status: enum (Processing/Shipped/Delivered/Cancelled)
- Cancel only if status = 'Processing'

## Development Workflow

### 1. Setup

```bash
# Backend
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python migrate_data.py  # One-time migration
uvicorn main:app --reload

# Frontend (separate terminal)
cd frontend
npm install
npm run dev
```

### 2. Testing

```bash
# Backend API tests
cd backend
pytest tests/test_api.py -v

# Frontend - manual testing
# Open http://localhost:5173 and click through:
# - Chat: send message "look up customer john@example.com"
# - Customers: search, edit email/phone
# - Orders: filter by status, cancel order
```

### 3. Learning Checkpoints

**Session 1 (LLM APIs):**
- [ ] Claude API key configured
- [ ] Can send basic chat message
- [ ] Tool schema defined correctly
- [ ] Tool execution returns data

**Session 2 (Frontend):**
- [ ] React app renders 3 pages
- [ ] Chat page displays messages
- [ ] Customer/Order tables display data

**Session 3 (Backend):**
- [ ] FastAPI routes respond to requests
- [ ] CRUD operations work
- [ ] Database queries return correct data

**Session 4 (Integration):**
- [ ] Frontend → Backend → Database works end-to-end
- [ ] Chat invokes Claude → executes tools → returns AI response
- [ ] Can complete user stories P1, P2

## Removed Complexity

**Not implementing (production features with no educational value):**
- Conversation history persistence
- Audit trails and logging infrastructure
- Performance optimization (WAL mode, connection pooling)
- Comprehensive testing (unit/integration/E2E)
- Advanced error handling and monitoring
- SLA/uptime requirements
- Responsive design testing
- Docker containerization
- CI/CD pipelines

**Result:** Focus 100% on AI integration learning, not DevOps/architecture

## Success Criteria (Simplified)

- ✅ Chat interface sends messages to Claude and displays responses
- ✅ Claude correctly invokes tools based on user queries
- ✅ Tools execute and return accurate customer/order data
- ✅ Frontend displays customer and order data from SQLite
- ✅ Can search, update, and cancel via UI
- ✅ Data migration from HuggingFace completes successfully
- ✅ Students understand function calling workflow

## Next Steps

1. Run `/speckit.tasks` to generate implementation tasks
2. Run `/speckit.analyze` for consistency check
3. Begin implementation following simplified structure
4. Prioritize Claude AI integration (core learning objective)
5. Keep it simple - if it doesn't teach AI concepts, remove it
