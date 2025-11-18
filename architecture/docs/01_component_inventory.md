# Component Inventory

## Overview

The Blackbird Customer Support Application is a FastAPI-based web service with Claude AI integration. It provides a REST API for customer support operations including customer management, order management, and AI-powered chat assistance. The backend uses SQLite for data persistence and integrates with Anthropic's Claude AI for intelligent function calling.

**Project Structure:**
```
fastapi-demo/
├── main.py                  # Simple Hello World entry point
├── backend/                 # Main application code
│   ├── main.py             # FastAPI application and routes
│   ├── models.py           # Pydantic data models
│   ├── database.py         # SQLite database operations
│   ├── ai_tools.py         # Claude AI integration
│   └── migrate_data.py     # Data migration script
├── frontend/               # React frontend (not analyzed)
└── pyproject.toml          # Project metadata
```

---

## Public API

### Modules

#### `backend/main.py`
**Purpose:** FastAPI application entry point with REST API endpoints
**Lines:** 1-261
**Description:** Defines the main FastAPI application with CORS middleware and implements REST endpoints for chat, customer management, and order management operations.

#### `backend/models.py`
**Purpose:** Pydantic data models for request/response validation
**Lines:** 1-236
**Description:** Defines all data schemas using Pydantic for type validation and serialization, including Customer, Order, Chat, and error response models.

#### `backend/database.py`
**Purpose:** Database layer with SQLite operations
**Lines:** 1-338
**Description:** Provides database schema initialization, connection management via context managers, and CRUD operations for customers and orders.

#### `backend/ai_tools.py`
**Purpose:** Claude AI integration with function calling
**Lines:** 1-354
**Description:** Implements the Claude AI integration with 6 function calling tools for customer support operations, handling the full conversation flow with tool execution.

### Classes

#### `Customer` (models.py, lines 15-42)
**Purpose:** Customer data model
**Public Methods/Properties:**
- `id: str` - 7-digit customer ID with pattern validation
- `name: str` - Customer full name (1-100 chars)
- `email: EmailStr` - Validated email address
- `phone: str` - Phone in XXX-XXX-XXXX format
- `username: str` - Alphanumeric username (3-20 chars)

**Description:** Pydantic model representing customer data with comprehensive validation rules.

#### `CustomerUpdate` (models.py, lines 45-60)
**Purpose:** Customer update request model
**Public Methods/Properties:**
- `email: Optional[EmailStr]` - New email address
- `phone: Optional[str]` - New phone number

**Description:** Pydantic model for partial customer updates (email and/or phone).

#### `CustomerSearch` (models.py, lines 63-78)
**Purpose:** Customer search request model
**Public Methods/Properties:**
- `key: Literal['email', 'phone', 'username']` - Search field
- `value: str` - Search value

**Description:** Pydantic model for searching customers by different fields.

#### `Order` (models.py, lines 85-111)
**Purpose:** Order data model
**Public Methods/Properties:**
- `id: str` - 5-digit order ID
- `customer_id: str` - 7-digit customer ID
- `product: str` - Product name (1-200 chars)
- `quantity: int` - Quantity ordered (>0, ≤999)
- `price: float` - Price per unit (≥0, <10000)
- `status: Literal['Processing', 'Shipped', 'Delivered', 'Cancelled']` - Order status

**Description:** Pydantic model representing an order with validation constraints.

#### `OrderCancelResponse` (models.py, lines 114-127)
**Purpose:** Order cancellation response model
**Public Methods/Properties:**
- `success: bool` - Whether cancellation succeeded
- `message: str` - Result message

**Description:** Standardized response for order cancellation operations.

#### `ChatMessage` (models.py, lines 134-147)
**Purpose:** Chat message request model
**Public Methods/Properties:**
- `message: str` - User's chat message (1-4000 chars)

**Description:** Pydantic model for incoming chat messages to Claude AI.

#### `ChatResponse` (models.py, lines 150-178)
**Purpose:** Chat response model
**Public Methods/Properties:**
- `response: str` - AI assistant's response text
- `tool_calls: Optional[List[Dict[str, Any]]]` - Tools called by AI (for debugging)

**Description:** Standardized response from Claude AI including tool usage information.

#### `CustomerWithOrders` (models.py, lines 185-215)
**Purpose:** Combined customer and orders response model
**Public Methods/Properties:**
- `customer: Customer` - Customer information
- `orders: List[Order]` - List of customer's orders

**Description:** Composite model for queries requiring both customer and order data.

#### `ErrorResponse` (models.py, lines 222-235)
**Purpose:** Standard error response model
**Public Methods/Properties:**
- `error: str` - Error message
- `detail: Optional[str]` - Additional error details

**Description:** Standardized error response format for API endpoints.

### Functions

#### REST API Endpoints (backend/main.py)

##### `health_check()` (lines 62-64)
**Path:** `GET /api/health`
**Purpose:** Health check endpoint
**Returns:** Status dictionary with service name
**Description:** Simple health check for monitoring service availability.

##### `chat(message: ChatMessage)` (lines 72-94)
**Path:** `POST /api/chat`
**Purpose:** Send message to Claude AI assistant
**Parameters:**
- `message: ChatMessage` - User's chat message
**Returns:** `ChatResponse` with AI response and tool calls
**Description:** Main entry point for AI-powered chat, delegates to `ai_tools.process_chat_message()`.

##### `get_customers()` (lines 102-108)
**Path:** `GET /api/customers`
**Purpose:** Retrieve all customers
**Returns:** `List[Customer]`
**Description:** Returns all customers from the database, ordered by name.

##### `get_customer(customer_id: str)` (lines 111-117)
**Path:** `GET /api/customers/{customer_id}`
**Purpose:** Get specific customer by ID
**Parameters:**
- `customer_id: str` - 7-digit customer ID
**Returns:** `Customer`
**Description:** Retrieves a single customer or raises 404 if not found.

##### `search_customer(search: CustomerSearch)` (lines 120-142)
**Path:** `POST /api/customers/search`
**Purpose:** Search for customer by email, phone, or username
**Parameters:**
- `search: CustomerSearch` - Search criteria
**Returns:** `Customer`
**Description:** Flexible customer search supporting multiple field types.

##### `update_customer(customer_id: str, update: CustomerUpdate)` (lines 145-177)
**Path:** `PATCH /api/customers/{customer_id}`
**Purpose:** Update customer contact information
**Parameters:**
- `customer_id: str` - 7-digit customer ID
- `update: CustomerUpdate` - Fields to update
**Returns:** `Customer` - Updated customer data
**Description:** Updates email and/or phone for a customer, validates existence first.

##### `get_customer_with_orders(customer_id: str)` (lines 180-191)
**Path:** `GET /api/customers/{customer_id}/orders`
**Purpose:** Get customer with all their orders
**Parameters:**
- `customer_id: str` - 7-digit customer ID
**Returns:** `CustomerWithOrders`
**Description:** Combined query returning customer info and order history.

##### `get_orders(status: Optional[str])` (lines 198-210)
**Path:** `GET /api/orders`
**Purpose:** Get all orders with optional status filter
**Parameters:**
- `status: Optional[str]` - Filter by order status (query param)
**Returns:** `List[Order]`
**Description:** Returns all orders, optionally filtered by status.

##### `get_order(order_id: str)` (lines 213-219)
**Path:** `GET /api/orders/{order_id}`
**Purpose:** Get specific order by ID
**Parameters:**
- `order_id: str` - 5-digit order ID
**Returns:** `Order`
**Description:** Retrieves a single order or raises 404 if not found.

##### `cancel_order(order_id: str)` (lines 222-239)
**Path:** `PATCH /api/orders/{order_id}/cancel`
**Purpose:** Cancel an order
**Parameters:**
- `order_id: str` - 5-digit order ID
**Returns:** `OrderCancelResponse`
**Description:** Cancels an order if status is 'Processing', otherwise returns error.

##### `startup_event()` (lines 246-255)
**Purpose:** Initialize database on application startup
**Description:** Event handler that initializes the database schema and prints startup information.

#### Database Operations (backend/database.py)

##### `init_database()` (lines 52-68)
**Purpose:** Initialize database schema
**Returns:** None
**Description:** Creates tables and indexes if they don't exist, safe to call multiple times.

##### `get_db()` (lines 71-98)
**Purpose:** Context manager for database connections
**Yields:** `sqlite3.Connection` with row_factory set to Row
**Description:** Provides connection with automatic commit/rollback and cleanup.

##### `get_customer(customer_id: str)` (lines 105-122)
**Purpose:** Get customer by ID
**Parameters:**
- `customer_id: str` - 7-digit customer ID
**Returns:** `Optional[Dict[str, Any]]` - Customer dict or None
**Description:** Retrieves customer data by primary key.

##### `search_customer(key: str, value: str)` (lines 125-148)
**Purpose:** Search customer by email, phone, or username
**Parameters:**
- `key: str` - Search field ('email', 'phone', 'username')
- `value: str` - Search value
**Returns:** `Optional[Dict[str, Any]]` - Customer dict or None
**Raises:** `ValueError` for invalid search keys
**Description:** Flexible customer search with field validation.

##### `get_all_customers()` (lines 151-162)
**Purpose:** Get all customers
**Returns:** `List[Dict[str, Any]]`
**Description:** Returns all customers ordered by name.

##### `update_customer(customer_id: str, email: Optional[str], phone: Optional[str])` (lines 165-201)
**Purpose:** Update customer contact information
**Parameters:**
- `customer_id: str` - Customer ID
- `email: Optional[str]` - New email
- `phone: Optional[str]` - New phone
**Returns:** `bool` - True if updated successfully
**Raises:** `ValueError` if no fields provided
**Description:** Updates one or more customer contact fields.

##### `get_order(order_id: str)` (lines 208-225)
**Purpose:** Get order by ID
**Parameters:**
- `order_id: str` - 5-digit order ID
**Returns:** `Optional[Dict[str, Any]]` - Order dict or None
**Description:** Retrieves order data by primary key.

##### `get_customer_orders(customer_id: str)` (lines 228-245)
**Purpose:** Get all orders for a customer
**Parameters:**
- `customer_id: str` - Customer ID
**Returns:** `List[Dict[str, Any]]`
**Description:** Returns all orders for a specific customer.

##### `get_all_orders(status: Optional[str])` (lines 248-271)
**Purpose:** Get all orders with optional status filter
**Parameters:**
- `status: Optional[str]` - Filter by status
**Returns:** `List[Dict[str, Any]]`
**Description:** Returns all orders, optionally filtered by status.

##### `cancel_order(order_id: str)` (lines 274-310)
**Purpose:** Cancel an order if status is 'Processing'
**Parameters:**
- `order_id: str` - Order ID
**Returns:** `Dict[str, Any]` - Success/failure dict with message
**Description:** Implements business rule that only Processing orders can be cancelled.

##### `get_customer_with_orders(customer_id: str)` (lines 317-337)
**Purpose:** Get customer with all their orders
**Parameters:**
- `customer_id: str` - Customer ID
**Returns:** `Optional[Dict[str, Any]]` - Dict with customer and orders
**Description:** Combined query for customer and order data.

#### AI Tools (backend/ai_tools.py)

##### `execute_tool(tool_name: str, tool_input: Dict[str, Any])` (lines 136-217)
**Purpose:** Execute a Claude AI tool and return results
**Parameters:**
- `tool_name: str` - Name of tool to execute
- `tool_input: Dict[str, Any]` - Tool parameters
**Returns:** `Dict[str, Any]` - Tool execution result
**Raises:** `ValueError` for unknown tools
**Description:** Routes tool calls to appropriate database operations, handles 6 different tools.

##### `chat_with_claude(message: str, conversation_history: Optional[List[Dict[str, Any]]])` (lines 224-333)
**Purpose:** Send message to Claude with tool calling enabled
**Parameters:**
- `message: str` - User's message
- `conversation_history: Optional[List[Dict[str, Any]]]` - Previous messages
**Returns:** `Dict[str, Any]` - Response and tool_calls list
**Description:** Implements full Claude function calling workflow with multi-turn conversations.

##### `process_chat_message(message: str)` (lines 340-353)
**Purpose:** Process single chat message (stateless)
**Parameters:**
- `message: str` - User's message
**Returns:** `Dict[str, Any]` - Response and tool_calls
**Description:** Simplified wrapper for stateless chat interactions.

---

## Internal Implementation

### Modules

#### `backend/migrate_data.py`
**Purpose:** Data migration script from HuggingFace to SQLite
**Lines:** 1-181
**Description:** One-time migration script that loads data from HuggingFace datasets (dwb2023/blackbird-customers and dwb2023/blackbird-orders) and populates the SQLite database.

#### `main.py`
**Purpose:** Simple Hello World entry point
**Lines:** 1-7
**Description:** Minimal entry point at project root, not part of the main application.

### Constants

#### `TOOLS` (ai_tools.py, lines 26-129)
**Purpose:** JSON Schema definitions for Claude AI function calling
**Type:** `List[Dict]`
**Description:** Defines 6 tools available to Claude AI:
1. `get_user` - Search customer by email/phone/username
2. `get_order_by_id` - Lookup order details
3. `get_customer_orders` - Get all orders for customer
4. `cancel_order` - Cancel order if Processing
5. `update_user_contact` - Update customer email/phone
6. `get_user_info` - Get customer + orders combined

#### `DATABASE_PATH` (database.py, line 12)
**Purpose:** SQLite database file path
**Value:** `"blackbird.db"`
**Description:** Location of the SQLite database file.

#### `SCHEMA_SQL` (database.py, lines 15-49)
**Purpose:** Database schema definition
**Type:** `str`
**Description:** SQL script defining customers and orders tables with constraints and indexes.

### Functions

#### `migrate()` (migrate_data.py, lines 19-170)
**Purpose:** Execute data migration from HuggingFace to SQLite
**Returns:** None
**Description:** 5-step migration process: initialize schema, load datasets, insert customers, insert orders, verify migration.

#### `main()` (main.py root, lines 1-2)
**Purpose:** Simple Hello World function
**Returns:** None
**Description:** Prints greeting message, not used in main application.

---

## Entry Points

### Main Application Entry Point

**File:** `backend/main.py`
**Lines:** 258-260
**Entry point:**
```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```
**Description:** Starts the FastAPI application using Uvicorn ASGI server on port 8000. Can be run directly with `python main.py` or via `uvicorn main:app --reload`.

**API Documentation:** Auto-generated at `http://localhost:8000/docs` (Swagger UI)

### Data Migration Script

**File:** `backend/migrate_data.py`
**Lines:** 173-180
**Entry point:**
```python
if __name__ == "__main__":
    try:
        migrate()
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
```
**Description:** Standalone script to migrate data from HuggingFace datasets to SQLite. Run with `python migrate_data.py`.

### Simple Hello World

**File:** `main.py`
**Lines:** 5-6
**Entry point:**
```python
if __name__ == "__main__":
    main()
```
**Description:** Simple test script at project root, not part of main application.

---

## Module Dependencies

### Dependency Graph

```
main.py (FastAPI app)
├── models.py (Pydantic schemas)
│   └── pydantic
│   └── typing
├── database.py (SQLite operations)
│   └── sqlite3
│   └── contextlib
│   └── typing
├── ai_tools.py (Claude AI)
│   ├── anthropic (Claude SDK)
│   ├── database.py
│   ├── json
│   ├── os
│   └── typing
└── External Dependencies
    ├── fastapi
    ├── uvicorn
    └── python-dotenv

migrate_data.py (standalone)
├── database.py
├── datasets (HuggingFace)
└── sqlite3
```

### Key Import Relationships

#### `backend/main.py` imports:
- `fastapi` (FastAPI, HTTPException, Query)
- `fastapi.middleware.cors` (CORSMiddleware)
- `dotenv` (load_dotenv)
- `typing` (List, Optional)
- `database` as `db` (all database operations)
- `ai_tools` (process_chat_message)
- `models` (all Pydantic models)
- `os`, `pathlib` (environment setup)

#### `backend/ai_tools.py` imports:
- `os` (environment variables)
- `json` (tool result serialization)
- `typing` (Dict, Any, List, Optional)
- `anthropic` (Anthropic client)
- `database` as `db` (database operations)

#### `backend/database.py` imports:
- `sqlite3` (database operations)
- `contextlib` (contextmanager decorator)
- `typing` (Optional, List, Dict, Any)

#### `backend/models.py` imports:
- `pydantic` (BaseModel, EmailStr, Field)
- `typing` (Optional, Literal, List, Dict, Any)

#### `backend/migrate_data.py` imports:
- `sqlite3` (direct database access)
- `datasets` (load_dataset from HuggingFace)
- `database` (init_database, DATABASE_PATH)

### External Dependencies (from requirements.txt)

**Core:**
- `fastapi==0.104.1` - Web framework
- `uvicorn[standard]==0.24.0` - ASGI server
- `python-multipart==0.0.6` - Form data parsing

**AI/ML:**
- `anthropic==0.7.8` - Claude AI SDK
- `datasets==2.15.0` - HuggingFace datasets

**Data Validation:**
- `pydantic==2.5.0` - Data validation
- `pydantic[email]==2.5.0` - Email validation

**Environment:**
- `python-dotenv==1.0.0` - Environment variables

**Testing:**
- `pytest==7.4.3` - Testing framework
- `pytest-asyncio==0.21.1` - Async test support
- `httpx==0.25.2` - HTTP client for testing

**Development:**
- `ruff==0.1.6` - Linting and formatting

---

## Architecture Notes

### Design Patterns

1. **Layered Architecture:**
   - **API Layer** (main.py): REST endpoints, request/response handling
   - **Business Logic** (ai_tools.py): Claude AI orchestration, tool execution
   - **Data Access** (database.py): SQLite operations, CRUD abstractions
   - **Data Models** (models.py): Validation, serialization schemas

2. **Dependency Injection:**
   - Database connections via context managers
   - AI client initialization per request
   - Environment configuration via .env

3. **Separation of Concerns:**
   - Each module has single responsibility
   - Clear boundaries between layers
   - No business logic in API handlers

4. **Function Calling Pattern:**
   - AI tools defined as JSON schemas
   - Tool execution router pattern
   - Multi-turn conversation flow

### Key Characteristics

- **Database:** SQLite embedded database (no server required)
- **API Style:** RESTful with OpenAPI documentation
- **AI Integration:** Claude 3.5 Sonnet with function calling
- **Data Source:** HuggingFace datasets for initial data
- **Validation:** Comprehensive Pydantic models with regex patterns
- **Error Handling:** Consistent HTTP exceptions and error responses

### File Statistics

| File | Lines | Purpose | Complexity |
|------|-------|---------|------------|
| backend/main.py | 261 | API endpoints | Medium |
| backend/ai_tools.py | 354 | AI integration | High |
| backend/database.py | 338 | Data access | Medium |
| backend/models.py | 236 | Data schemas | Low |
| backend/migrate_data.py | 181 | Migration script | Low |
| main.py (root) | 7 | Hello World | Minimal |

**Total Backend Code:** ~1,377 lines of Python (excluding tests, frontend, and tooling)

---

## Configuration Files

### `pyproject.toml`
**Purpose:** Project metadata and dependencies
**Key Configuration:**
- Project name: `fastapi-demo`
- Version: `0.1.0`
- Python requirement: `>=3.11`
- Main dependency: `claude-agent-sdk>=0.1.6`

### `backend/requirements.txt`
**Purpose:** Python package dependencies
**Description:** Lists all runtime and development dependencies with pinned versions for reproducible builds.

---

## Summary

The Blackbird Customer Support Application is a well-structured FastAPI application with clear separation of concerns. The codebase consists of:

- **4 core backend modules** providing API, AI integration, database access, and data validation
- **10 Pydantic models** for comprehensive request/response validation
- **11 REST endpoints** for customers, orders, and chat
- **12 database operations** with proper error handling
- **6 AI tools** for Claude function calling
- **1 migration script** for data initialization

The architecture follows best practices with layered design, context managers for resource management, comprehensive validation, and clear module boundaries. The integration with Claude AI demonstrates production-ready function calling patterns with multi-turn conversations and tool execution.
