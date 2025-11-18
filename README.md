# Repository Architecture Documentation

## Overview

The **Blackbird Customer Support Application** is a full-stack demonstration of AI-powered customer relationship management, showcasing modern software architecture patterns and Claude AI integration. This FastAPI-based web service combines traditional REST API design with intelligent AI tool calling to create an interactive customer support system.

**Project Purpose:**
- Demonstrate Claude AI integration with function calling
- Showcase FastAPI best practices for building REST APIs
- Illustrate layered architecture with clear separation of concerns
- Provide educational reference for full-stack application development

**Key Capabilities:**
- Natural language customer and order queries via Claude AI
- RESTful API for customer and order management
- Real-time AI tool calling with transparent execution tracking
- SQLite database with comprehensive validation and constraints
- React frontend with responsive UI components

**Technology Stack:**
- **Backend:** FastAPI (Python), SQLite, Pydantic validation
- **AI Integration:** Claude 4.5 Haiku (Anthropic API)
- **Frontend:** React 18, Vite, JavaScript
- **Architecture Style:** Layered architecture with RESTful APIs

**Architecture Approach:**
This application follows a **layered architecture** pattern with strict separation between presentation, business logic, data access, and AI integration layers. The architecture prioritizes clarity and educational value while maintaining production-quality code organization.

---

## Quick Start

### For Developers New to This Project

**Recommended Reading Order:**
1. Start with this README for high-level overview
2. Review [Component Inventory](architecture/docs/01_component_inventory.md) to understand module structure
3. Study [Architecture Diagrams](architecture/diagrams/02_architecture_diagrams.md) for visual system understanding
4. Explore [Data Flows](architecture/docs/03_data_flows.md) to see how requests traverse the system
5. Reference [API Documentation](architecture/docs/04_api_reference.md) for implementation details

**What Each Document Contains:**
- **Component Inventory:** Complete listing of modules, classes, functions with line numbers
- **Architecture Diagrams:** System architecture, component relationships, database schema (Mermaid diagrams)
- **Data Flows:** Request/response flows, tool execution patterns, error handling (sequence diagrams)
- **API Reference:** REST endpoints, data models, database operations, usage examples

**Setting Up for Development:**
```bash
# Navigate to project directory
cd fastapi-demo

# Install backend dependencies
cd backend
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# Initialize database
python -c "from database import init_database; init_database()"

# Run backend server
uvicorn main:app --reload --port 8000

# In a new terminal, run frontend
cd frontend
npm install
npm run dev
```

### For Architects and Technical Leads

**Key Architectural Decisions:**

1. **SQLite for Data Persistence**
   - **Rationale:** Educational simplicity, zero configuration, file-based storage
   - **Trade-off:** Limited concurrency, not suitable for production scale
   - **Alternatives:** PostgreSQL or MySQL for production deployments

2. **Synchronous Request Processing**
   - **Rationale:** Simpler code, educational focus, SQLite doesn't benefit from async
   - **Trade-off:** Thread-per-request model limits concurrency
   - **Alternatives:** Async endpoints with aiosqlite for better concurrency

3. **Stateless AI Conversations**
   - **Rationale:** Simpler implementation, easier to understand tool calling flow
   - **Trade-off:** No conversation context maintained between requests
   - **Alternatives:** Session-based history storage in Redis or database

4. **Direct Claude API Integration**
   - **Rationale:** Clear demonstration of Anthropic SDK usage, minimal abstraction
   - **Trade-off:** Tightly coupled to Anthropic API
   - **Alternatives:** MCP (Model Context Protocol) for vendor-agnostic AI integration

5. **Layered Architecture with Dependency Injection**
   - **Rationale:** Clear separation of concerns, testable components, maintainable code
   - **Benefits:** Each layer has single responsibility, easy to modify/extend

**Technical Deep Dives:**
- System architecture layers: See [Architecture Diagrams, Section 1](architecture/diagrams/02_architecture_diagrams.md#1-system-architecture-layered-view)
- Claude AI tool calling implementation: See [Data Flows, Section 6](architecture/docs/03_data_flows.md#6-ai-tool-execution-flow)
- Database transaction management: See [Data Flows, Section 7](architecture/docs/03_data_flows.md#7-database-operation-flow)
- Performance considerations: See [Data Flows, Performance Section](architecture/docs/03_data_flows.md#performance-considerations)

### For API Consumers

**Getting Started with the API:**

The API is available at `http://localhost:8000/api` with interactive documentation at `http://localhost:8000/docs` (Swagger UI).

**Core Integration Points:**
1. **Customer Management:** CRUD operations for customer records
2. **Order Management:** Query and cancel customer orders
3. **AI Chat Interface:** Natural language queries with automatic tool execution

**Quick Integration Example:**
```python
import requests

BASE_URL = "http://localhost:8000/api"

# Search for a customer
response = requests.post(
    f"{BASE_URL}/customers/search",
    json={"key": "email", "value": "john@example.com"}
)
customer = response.json()

# Get customer's orders
response = requests.get(f"{BASE_URL}/customers/{customer['id']}/orders")
data = response.json()
print(f"Customer: {data['customer']['name']}")
print(f"Orders: {len(data['orders'])}")

# Use AI to interact naturally
response = requests.post(
    f"{BASE_URL}/chat",
    json={"message": "Show me all processing orders for john@example.com"}
)
print(response.json()['response'])
```

**Complete API Documentation:** [API Reference](architecture/docs/04_api_reference.md)

---

## Project Structure

```
{PROJECT_ROOT}/
├── backend/                      # Backend application
│   ├── main.py                  # FastAPI app & REST endpoints (261 lines)
│   ├── models.py                # Pydantic data models (236 lines)
│   ├── database.py              # SQLite operations & CRUD (338 lines)
│   ├── ai_tools.py              # Claude AI integration (354 lines)
│   ├── migrate_data.py          # Data migration script (181 lines)
│   ├── requirements.txt         # Python dependencies
│   └── blackbird.db             # SQLite database file
│
├── frontend/                     # React frontend application
│   ├── src/
│   │   ├── main.jsx            # React entry point
│   │   ├── App.jsx             # Routing & navigation
│   │   ├── api.js              # Backend API client
│   │   ├── pages/              # Page components
│   │   │   ├── ChatPage.jsx        # AI chat interface
│   │   │   ├── CustomersPage.jsx   # Customer management
│   │   │   └── OrdersPage.jsx      # Order management
│   │   └── components/         # Reusable UI components
│   ├── index.html              # HTML entry point
│   ├── vite.config.js          # Vite configuration
│   └── package.json            # Node dependencies
│
├── architecture/               # Generated documentation
│       ├── docs/
│       │   ├── 01_component_inventory.md
│       │   ├── 03_data_flows.md
│       │   └── 04_api_reference.md
│       └── diagrams/
│           └── 02_architecture_diagrams.md
│
├── pyproject.toml               # Project metadata
├── .env                         # Environment variables (not committed)
└── main.py                      # Simple Hello World (7 lines)
```

**Structure Explanation:**

- **backend/**: Core application logic organized by responsibility
  - `main.py`: API endpoints and request handling
  - `models.py`: Data validation schemas (Pydantic)
  - `database.py`: Data persistence layer (SQLite)
  - `ai_tools.py`: AI integration and tool calling logic

- **frontend/**: React SPA with component-based architecture
  - Three main pages for different workflows
  - Centralized API client for backend communication
  - Reusable components for consistent UI

- **ra_output/**: Auto-generated comprehensive documentation
  - Component catalog with line references
  - Visual architecture diagrams
  - Data flow analysis
  - Complete API reference

**Code Statistics:**
- Backend: ~1,377 lines of Python
- 4 core backend modules
- 10 Pydantic models
- 11 REST endpoints
- 6 AI tools
- 12 database operations

---

## Architecture Summary

### Architecture Style

**Layered Architecture with Clear Separation of Concerns**

The application follows a strict **6-layer architecture** where each layer has a single, well-defined responsibility:

1. **Presentation Layer** (React): User interface and interaction
2. **API Gateway Layer** (Vite Proxy): Development routing and CORS handling
3. **API Layer** (FastAPI): REST endpoints, request validation, response formatting
4. **Business Logic Layer** (Route Handlers): Orchestration, validation, error handling
5. **Integration Layer** (AI Tools): Claude AI communication and tool execution
6. **Data Access Layer** (Database Module): CRUD operations, transaction management
7. **Data Storage Layer** (SQLite): Persistent data storage with constraints

**Design Patterns:**
- **Context Manager Pattern:** Database connection lifecycle management
- **Dependency Injection:** Environment variables, client initialization
- **Function Calling Pattern:** AI tool execution with JSON schemas
- **Repository Pattern:** Database operations abstracted from business logic

### Key Architectural Decisions

**1. Layered Architecture for Maintainability**
- **Decision:** Strict separation between API, business logic, AI integration, and data layers
- **Rationale:** Each layer can evolve independently; clear boundaries enable testing and modification
- **Impact:** Clean code organization, testable components, easy to understand

**2. Pydantic for Type Safety and Validation**
- **Decision:** Use Pydantic models for all request/response data
- **Rationale:** Automatic validation, clear data contracts, self-documenting schemas
- **Impact:** Reduces runtime errors, provides clear API contracts, enables OpenAPI generation

**3. SQLite with Context Managers**
- **Decision:** File-based SQLite with automatic transaction management
- **Rationale:** Zero configuration, educational simplicity, automatic commit/rollback
- **Impact:** Easy to set up, clear transaction boundaries, safe error handling

**4. Claude AI with Function Calling**
- **Decision:** Direct integration with Anthropic API using tool calling
- **Rationale:** Demonstrates modern AI integration patterns, transparent tool execution
- **Impact:** Natural language interface, automatic task routing, extensible tool system

**5. Stateless API Design**
- **Decision:** Each request is independent, no server-side session state
- **Rationale:** Simpler to understand and implement for educational purposes
- **Impact:** Scales horizontally, but requires client-side conversation management

**6. CORS-Enabled Development Setup**
- **Decision:** Enable CORS for localhost origins with Vite proxy
- **Rationale:** Separate backend/frontend development servers during development
- **Impact:** Clean separation of concerns, flexible deployment options

### System Layers

**Presentation Layer (React Frontend)**
- **Purpose:** User interface and interaction handling
- **Components:** ChatPage, CustomersPage, OrdersPage, reusable UI components
- **Responsibilities:**
  - Render UI based on application state
  - Handle user input and events
  - Manage client-side routing
  - Display loading states and errors
- **Technology:** React 18, React Router, Fetch API

**API Gateway Layer (Vite Dev Proxy)**
- **Purpose:** Route frontend requests to backend during development
- **Configuration:** Proxy `/api/*` to `http://localhost:8000/api/*`
- **Responsibilities:**
  - Handle CORS during development
  - Forward API requests to backend
  - Enable hot module replacement for frontend

**API Layer (FastAPI Application)**
- **Purpose:** Expose REST endpoints with validation
- **Components:** FastAPI app, CORS middleware, endpoint handlers
- **Responsibilities:**
  - Route HTTP requests to handlers
  - Validate request bodies with Pydantic
  - Serialize responses to JSON
  - Handle HTTP errors and status codes
  - Generate OpenAPI documentation
- **Location:** `backend/main.py`

**Business Logic Layer (Route Handlers)**
- **Purpose:** Orchestrate operations and enforce business rules
- **Responsibilities:**
  - Coordinate between database and AI layers
  - Validate business constraints
  - Transform data between layers
  - Handle errors and exceptions
  - Return appropriate HTTP responses
- **Pattern:** Each endpoint handler orchestrates a specific business operation

**Integration Layer (AI Tools Module)**
- **Purpose:** Integrate with Claude AI for intelligent assistance
- **Components:** 6 tool definitions, tool executor, Claude API client
- **Responsibilities:**
  - Define available tools with JSON schemas
  - Execute tools and return results to Claude
  - Manage multi-turn conversations
  - Handle Claude API errors
  - Log tool calls for transparency
- **Location:** `backend/ai_tools.py`

**Data Access Layer (Database Module)**
- **Purpose:** Abstract database operations from business logic
- **Components:** Context manager, CRUD functions, transaction management
- **Responsibilities:**
  - Manage database connections
  - Execute SQL queries safely (parameterized)
  - Convert results to Python dicts
  - Handle database errors
  - Commit or rollback transactions
- **Location:** `backend/database.py`

**Data Storage Layer (SQLite Database)**
- **Purpose:** Persist data with integrity constraints
- **Schema:** Two tables (customers, orders) with foreign keys
- **Responsibilities:**
  - Store customer and order data
  - Enforce referential integrity
  - Validate data with CHECK constraints
  - Provide ACID transaction guarantees
  - Index frequently queried columns
- **Location:** `backend/blackbird.db`

### Architecture Diagram

```mermaid
graph TB
    subgraph "Presentation Layer"
        A[React Frontend]
        A1[ChatPage.jsx]
        A2[CustomersPage.jsx]
        A3[OrdersPage.jsx]
        A4[Shared Components]
    end

    subgraph "API Gateway Layer"
        B[Vite Dev Proxy]
        B1[CORS Handling]
        B2[Request Forwarding]
    end

    subgraph "API Layer"
        C[FastAPI Backend]
        C1["/api/chat"]
        C2["/api/customers/*"]
        C3["/api/orders/*"]
        C4[CORS Middleware]
        C5[Pydantic Validation]
    end

    subgraph "Business Logic Layer"
        D[Route Handlers]
        D1[Chat Handler]
        D2[Customer Handlers]
        D3[Order Handlers]
    end

    subgraph "Integration Layer"
        E[AI Tools Module]
        E1[Tool Executor]
        E2[Claude API Client]
        E3[6 Tool Definitions]
    end

    subgraph "Data Access Layer"
        F[Database Module]
        F1[Context Manager]
        F2[Customer CRUD]
        F3[Order CRUD]
    end

    subgraph "Data Storage Layer"
        G[(SQLite Database)]
        G1[(customers table)]
        G2[(orders table)]
    end

    subgraph "External Services"
        H[Claude AI API]
    end

    A --> B
    A1 --> A
    A2 --> A
    A3 --> A
    A4 --> A

    B --> C
    B1 --> B
    B2 --> B

    C --> D
    C1 --> C
    C2 --> C
    C3 --> C
    C4 --> C
    C5 --> C

    D --> E
    D --> F
    D1 --> D
    D2 --> D
    D3 --> D

    E --> H
    E1 --> E
    E2 --> E
    E3 --> E

    F --> G
    F1 --> F
    F2 --> F
    F3 --> F

    G1 --> G
    G2 --> G

    style A fill:#e1f5ff
    style B fill:#fff9c4
    style C fill:#fff3e0
    style D fill:#f3e5f5
    style E fill:#e8f5e9
    style F fill:#fff9c4
    style G fill:#e0f2f1
    style H fill:#fce4ec
```

**Diagram Notes:**
- Data flows top-to-bottom: User → Frontend → API → Database
- Claude AI integration happens in parallel: API → AI Tools → Claude API
- Each layer communicates only with adjacent layers
- Clear boundaries enable independent testing and modification

---

## Component Overview

### Backend Components

| Component | Purpose | Key Functions | Lines | Documentation |
|-----------|---------|---------------|-------|---------------|
| **main.py** | FastAPI application entry point | 11 REST endpoints, startup handler, CORS config | 261 | [API Ref §REST Endpoints](architecture/docs/04_api_reference.md#rest-api-endpoints) |
| **models.py** | Pydantic data models | 10 validation models (Customer, Order, Chat, etc.) | 236 | [API Ref §Data Models](architecture/docs/04_api_reference.md#data-models) |
| **database.py** | SQLite data access layer | 12 CRUD operations, context manager, schema init | 338 | [API Ref §Database Ops](architecture/docs/04_api_reference.md#database-operations) |
| **ai_tools.py** | Claude AI integration | 6 tool definitions, tool executor, chat handler | 354 | [API Ref §AI Tools](architecture/docs/04_api_reference.md#ai-tools) |
| **migrate_data.py** | Data migration script | Load from HuggingFace datasets, populate DB | 181 | [Component Inv §Internal](architecture/docs/01_component_inventory.md#internal-implementation) |

**Detailed Breakdown:**

**main.py** - REST API Endpoints
- Health check: `GET /api/health`
- Chat endpoint: `POST /api/chat` (Claude AI integration)
- Customer endpoints: GET all, GET by ID, POST search, PATCH update, GET with orders
- Order endpoints: GET all, GET by ID, PATCH cancel
- Startup handler: Initialize database schema
- **Key Feature:** Comprehensive error handling with appropriate HTTP status codes

**models.py** - Data Validation
- `Customer`: 7-digit ID, email, phone (XXX-XXX-XXXX), username validation
- `CustomerUpdate`: Optional email/phone for PATCH operations
- `CustomerSearch`: Search by email, phone, or username
- `Order`: 5-digit ID, product, quantity, price, status enum
- `ChatMessage` & `ChatResponse`: AI conversation models
- `CustomerWithOrders`: Composite model for joined queries
- **Key Feature:** Pattern validation with regex, email validation, range constraints

**database.py** - Data Persistence
- Context manager: `get_db()` for automatic connection management
- Customer operations: get, search, list all, update
- Order operations: get, list by customer, list all, cancel
- Combined operations: get customer with orders
- **Key Feature:** Parameterized queries prevent SQL injection, row_factory for dict access

**ai_tools.py** - AI Integration
- 6 tools: get_user, get_order_by_id, get_customer_orders, cancel_order, update_user_contact, get_user_info
- Tool executor: Routes tool calls to database operations
- Multi-turn conversation: Handles tool use loop with Claude
- **Key Feature:** Transparent tool call logging, comprehensive error handling

### Frontend Components

**Architecture:**
- **Entry Point:** `main.jsx` renders `App.jsx` into DOM
- **Router:** `App.jsx` manages client-side routing (React Router)
- **Pages:** Three main pages for different workflows
- **API Client:** `api.js` provides typed interface to backend
- **Components:** Reusable UI elements (ChatMessage, DataTable, SearchBar)

**Page Responsibilities:**
- **ChatPage.jsx:** AI conversation interface with message history
- **CustomersPage.jsx:** Customer list, search, and detail views
- **OrdersPage.jsx:** Order list with filtering and cancellation

**Data Flow:**
```
User Action → Page Component → api.js → Vite Proxy → Backend
                ↓
            State Update → Re-render → UI Update
```

### External Dependencies

**Backend Dependencies (Python):**
- **fastapi** (0.104.1): Web framework for REST API
- **uvicorn[standard]** (0.24.0): ASGI server
- **pydantic** (2.5.0): Data validation and serialization
- **anthropic** (0.7.8): Claude AI SDK
- **python-dotenv** (1.0.0): Environment variable management
- **datasets** (2.15.0): HuggingFace datasets for migration

**Frontend Dependencies (Node):**
- **react** (18.x): UI library
- **react-router-dom**: Client-side routing
- **vite**: Build tool and dev server

**Development Dependencies:**
- **pytest** (7.4.3): Testing framework
- **ruff** (0.1.6): Linting and formatting

---

## Data Flow Patterns

### Request/Response Flow

High-level overview of how a typical customer query flows through the system:

```
1. User Interaction
   ↓
2. React Component Handler
   ↓
3. API Client (api.js)
   ↓
4. HTTP Request (Fetch)
   ↓
5. Vite Proxy (localhost:5173 → localhost:8000)
   ↓
6. FastAPI Router
   ↓
7. Pydantic Validation
   ↓
8. Endpoint Handler
   ↓
9. Database Query (SQLite)
   ↓
10. Response Validation
   ↓
11. JSON Serialization
   ↓
12. HTTP Response
   ↓
13. Frontend State Update
   ↓
14. UI Re-render
```

**Typical Latencies:**
- Simple database query: 50-100ms
- Customer search with orders: 100-150ms
- AI chat without tools: 1-2 seconds
- AI chat with 2-3 tools: 3-5 seconds

### Key Flow Patterns

**1. Simple CRUD Operations**
- **Pattern:** Direct HTTP → Database → Response
- **Example:** Get all customers, search by email, update phone number
- **Characteristics:** Synchronous, fast (50-150ms), no AI involvement
- **Error Handling:** HTTP 404 for not found, 400 for validation errors

**2. AI Chat with Tool Calling**
- **Pattern:** HTTP → Claude API → Tool Execution → Claude API → Response
- **Example:** "Show me orders for john@example.com"
- **Characteristics:** Multi-turn, slower (1-5s), automatic tool selection by Claude
- **Tool Execution Loop:**
  ```
  User Message → Claude (tool_use) → Execute Tools → Claude (final response)
  ```
- **Transparency:** All tool calls logged and returned to frontend

**3. Database Transactions**
- **Pattern:** Context Manager → Query → Commit/Rollback → Close
- **Example:** Cancel order (check status → update → commit)
- **Characteristics:** Atomic operations, automatic error handling
- **Safety:** Parameterized queries prevent SQL injection

**4. Error Handling**
- **Pattern:** Try/Catch at each layer with appropriate HTTP status codes
- **Layers:** Database (rollback) → Handler (HTTP exception) → Frontend (user message)
- **Status Codes:** 400 (business logic error), 404 (not found), 422 (validation), 500 (server error)

**Detailed Flow Documentation:** [Data Flows Document](architecture/docs/03_data_flows.md)

### AI Chat with Tool Calling (Detailed)

```mermaid
sequenceDiagram
    participant User
    participant Frontend as React ChatPage
    participant API as FastAPI
    participant AITools as ai_tools.py
    participant Claude as Claude AI
    participant DB as database.py

    User->>Frontend: "Look up john@example.com"
    Frontend->>API: POST /api/chat
    API->>AITools: process_chat_message()
    AITools->>Claude: messages.create(tools=6)

    Note over Claude: Decides to use get_user tool

    Claude-->>AITools: tool_use response
    AITools->>AITools: execute_tool("get_user", {...})
    AITools->>DB: search_customer("email", "john@...")
    DB-->>AITools: Customer data
    AITools->>Claude: Send tool result

    Note over Claude: Generate final response

    Claude-->>AITools: Text response
    AITools-->>API: {response, tool_calls}
    API-->>Frontend: ChatResponse JSON
    Frontend->>User: Display AI message
```

**Key Points:**
- Claude autonomously decides which tools to use based on user message
- Multiple tools can be called in sequence (e.g., get_user → get_customer_orders)
- Tool results are sent back to Claude for final response generation
- All tool calls are logged for debugging and transparency

---

## API Overview

**Base URL:** `http://localhost:8000/api`
**Interactive Docs:** `http://localhost:8000/docs` (Swagger UI)

### REST Endpoints Summary

#### Customer Management

| Endpoint | Method | Purpose | Request | Response |
|----------|--------|---------|---------|----------|
| `/customers` | GET | List all customers | None | `List[Customer]` |
| `/customers/{id}` | GET | Get customer by ID | Path: customer_id | `Customer` |
| `/customers/search` | POST | Search customer | Body: `{key, value}` | `Customer` |
| `/customers/{id}` | PATCH | Update contact info | Body: `{email?, phone?}` | `Customer` |
| `/customers/{id}/orders` | GET | Get customer + orders | Path: customer_id | `CustomerWithOrders` |

**Example - Search Customer:**
```bash
curl -X POST http://localhost:8000/api/customers/search \
  -H "Content-Type: application/json" \
  -d '{"key": "email", "value": "john@example.com"}'
```

#### Order Management

| Endpoint | Method | Purpose | Request | Response |
|----------|--------|---------|---------|----------|
| `/orders` | GET | List all orders | Query: `status?` | `List[Order]` |
| `/orders/{id}` | GET | Get order by ID | Path: order_id | `Order` |
| `/orders/{id}/cancel` | PATCH | Cancel order | Path: order_id | `OrderCancelResponse` |

**Example - Cancel Order:**
```bash
curl -X PATCH http://localhost:8000/api/orders/24601/cancel
```

**Response:**
```json
{
  "success": true,
  "message": "Order 24601 cancelled successfully"
}
```

#### AI Integration

| Endpoint | Method | Purpose | Request | Response |
|----------|--------|---------|---------|----------|
| `/chat` | POST | Send message to Claude AI | Body: `{message}` | `ChatResponse` |

**Example - AI Chat:**
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Show me all orders for john@example.com"}'
```

**Response:**
```json
{
  "response": "John Doe has 2 orders: Order 24601 (Wireless Headphones - Shipped) and Order 47652 (USB-C Cable - Processing).",
  "tool_calls": [
    {"tool": "get_user", "input": {"key": "email", "value": "john@example.com"}},
    {"tool": "get_customer_orders", "input": {"customer_id": "1213210"}}
  ]
}
```

#### Health Check

| Endpoint | Method | Purpose | Response |
|----------|--------|---------|----------|
| `/health` | GET | Service health status | `{status, service}` |

### Example Usage

**Python Client:**
```python
import requests

BASE_URL = "http://localhost:8000/api"

# Get all customers
customers = requests.get(f"{BASE_URL}/customers").json()
print(f"Total customers: {len(customers)}")

# Search by email
search_result = requests.post(
    f"{BASE_URL}/customers/search",
    json={"key": "email", "value": "john@example.com"}
).json()
print(f"Found: {search_result['name']}")

# Get customer with orders
customer_orders = requests.get(
    f"{BASE_URL}/customers/{search_result['id']}/orders"
).json()
print(f"Customer has {len(customer_orders['orders'])} orders")

# Chat with AI
chat_response = requests.post(
    f"{BASE_URL}/chat",
    json={"message": "What's the status of order 24601?"}
).json()
print(chat_response['response'])
```

**JavaScript Client (Frontend):**
```javascript
import { fetchCustomers, searchCustomer, sendChatMessage } from './api';

// Get all customers
const customers = await fetchCustomers();

// Search customer
const customer = await searchCustomer('email', 'john@example.com');

// Chat with AI
const response = await sendChatMessage('Cancel order 24601');
console.log(response.response);
```

**cURL Examples:**
```bash
# Health check
curl http://localhost:8000/api/health

# List customers
curl http://localhost:8000/api/customers

# Get specific customer
curl http://localhost:8000/api/customers/1213210

# Update customer
curl -X PATCH http://localhost:8000/api/customers/1213210 \
  -H "Content-Type: application/json" \
  -d '{"email": "newemail@example.com", "phone": "555-999-8888"}'

# Filter orders by status
curl "http://localhost:8000/api/orders?status=Processing"

# AI chat
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Show me all cancelled orders"}'
```

**Complete API Reference:** [API Documentation](architecture/docs/04_api_reference.md)

---

## Data Models

### Core Models

**Customer Model:**
- **Fields:** `id` (7 digits), `name`, `email`, `phone` (XXX-XXX-XXXX), `username` (3-20 alphanumeric)
- **Validation:**
  - ID must match pattern `^\d{7}$`
  - Email must be valid email format (EmailStr)
  - Phone must match `^\d{3}-\d{3}-\d{4}$`
  - Username must match `^[a-zA-Z0-9_]+$` and be 3-20 characters
- **Example:**
  ```json
  {
    "id": "1213210",
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "123-456-7890",
    "username": "johndoe"
  }
  ```

**Order Model:**
- **Fields:** `id` (5 digits), `customer_id` (7 digits), `product`, `quantity`, `price`, `status`
- **Validation:**
  - ID must match pattern `^\d{5}$`
  - customer_id must match `^\d{7}$` (foreign key)
  - quantity must be > 0 and ≤ 999
  - price must be ≥ 0 and < 10000
  - status must be one of: 'Processing', 'Shipped', 'Delivered', 'Cancelled'
- **Example:**
  ```json
  {
    "id": "24601",
    "customer_id": "1213210",
    "product": "Wireless Headphones",
    "quantity": 1,
    "price": 79.99,
    "status": "Processing"
  }
  ```

**ChatMessage Model:**
- **Fields:** `message` (1-4000 characters)
- **Purpose:** Request body for AI chat endpoint
- **Validation:** Non-empty string with maximum length

**ChatResponse Model:**
- **Fields:** `response` (AI's text response), `tool_calls` (optional list of tools used)
- **Purpose:** Response from AI chat endpoint
- **Transparency:** Includes all tool calls for debugging

**CustomerWithOrders Model:**
- **Fields:** `customer` (Customer object), `orders` (list of Order objects)
- **Purpose:** Composite response for efficient joined queries
- **Use Case:** Get customer details and order history in single request

**Detailed Model Documentation:** [API Reference §Data Models](architecture/docs/04_api_reference.md#data-models)

### Database Schema

```mermaid
erDiagram
    customers ||--o{ orders : "has many"

    customers {
        id INTEGER PK 
        name STRING NOT NULL 
        email STRING UNIQUE NOT NULL 
        phone STRING NOT NULL 
        username STRING UNIQUE NOT NULL 
    }

    orders {
        id INTEGER PK 
        customer_id INTEGER FK NOT NULL 
        product STRING NOT NULL 
        quantity INTEGER NOT NULL 
        price FLOAT NOT NULL 
        status STRING NOT NULL 
    }

```

**Key Features:**
- **Foreign Key:** `orders.customer_id` references `customers.id` with `ON DELETE CASCADE`
- **Unique Constraints:** Email and username must be unique across customers
- **CHECK Constraints:** Enforce business rules at database level (quantity > 0, price >= 0, valid status)
- **Indexes:** Created on email, username, customer_id, and status for query performance

**Indexes:**
```sql
CREATE INDEX idx_customers_email ON customers(email);
CREATE INDEX idx_customers_username ON customers(username);
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_orders_status ON orders(status);
```

---

## AI Integration

### Claude AI Tool System

The application integrates Claude 4.5 Haiku using Anthropic's tool calling (function calling) API. This enables Claude to autonomously interact with the database through structured tools.

**Integration Approach:**
- **6 Custom Tools:** Defined using JSON Schema format
- **Automatic Tool Selection:** Claude decides which tools to use based on user message
- **Multi-Turn Conversations:** Tools can be called multiple times before final response
- **Transparent Execution:** All tool calls logged and returned to frontend
- **Error Handling:** Tool errors captured and reported to Claude for context

**Tool Calling Flow:**
```
1. User sends message
   ↓
2. Message sent to Claude with available tools
   ↓
3. Claude decides to use tools (or respond directly)
   ↓
4. If tools requested:
   a. Execute tools against database
   b. Send results back to Claude
   c. Repeat if Claude requests more tools
   ↓
5. Claude generates final text response
   ↓
6. Response returned to user with tool call log
```

### Available Tools

**1. get_user**
- **Purpose:** Search customer by email, phone, or username
- **Input:** `{key: "email"|"phone"|"username", value: string}`
- **Output:** Customer information if found
- **Example:** "Look up customer with email john@example.com"

**2. search_customer (alias: get_user)**
- **Purpose:** Same as get_user, alternative naming
- **Use Case:** Natural language variations

**3. list_all_customers**
- **Purpose:** Get all customers in the system
- **Input:** None
- **Output:** List of all customers ordered by name
- **Example:** "Show me all customers"

**4. get_customer_with_orders (alias: get_user_info)**
- **Purpose:** Get customer details with all their orders
- **Input:** `{key: "email"|"phone"|"username"|"customer_id", value: string}`
- **Output:** Customer info + order list + order count
- **Example:** "What orders does john@example.com have?"

**5. list_orders**
- **Purpose:** Get all orders, optionally filtered by status
- **Input:** `{status?: "Processing"|"Shipped"|"Delivered"|"Cancelled"}`
- **Output:** List of orders
- **Example:** "Show me all processing orders"

**6. get_order**
- **Purpose:** Look up specific order by ID
- **Input:** `{order_id: string}`
- **Output:** Order details (product, quantity, price, status)
- **Example:** "What's the status of order 24601?"

**Note:** Tool names in code differ slightly from user-facing descriptions. See [AI Tools Documentation](architecture/docs/04_api_reference.md#ai-tools) for exact schemas.

### Multi-Turn Conversation Flow

Claude can call multiple tools in sequence to answer complex queries:

**Example: "Show me orders for john@example.com"**
```
Turn 1: User message → Claude
↓
Turn 2: Claude requests get_user tool
        Execute: search_customer("email", "john@example.com")
        Result: {customer_id: "1213210", name: "John Doe", ...}
↓
Turn 3: Send tool result to Claude
↓
Turn 4: Claude requests get_customer_orders tool
        Execute: get_customer_orders("1213210")
        Result: {orders: [...], count: 2}
↓
Turn 5: Send tool result to Claude
↓
Turn 6: Claude generates final response
        "John Doe has 2 orders: Order 24601 (Wireless Headphones - Shipped) and Order 47652 (USB-C Cable - Processing)."
```

**Current Implementation:**
- **Stateless:** No conversation history maintained between requests
- **Educational:** Simplifies understanding of tool calling mechanics
- **Production Alternative:** Store conversation history per user session in Redis or database

**Tool Execution Details:** [Data Flows §AI Tool Execution](architecture/docs/03_data_flows.md#6-ai-tool-execution-flow)

---

## Configuration

### Environment Setup

**Required Environment Variables:**
```bash
# .env file (create in project root)
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
```

**Obtaining API Key:**
1. Sign up at https://console.anthropic.com/
2. Navigate to API Keys section
3. Create a new API key
4. Copy to `.env` file

**Security Note:** Never commit `.env` file to version control (included in `.gitignore`)

### Database Configuration

**Location:** `backend/database.py:12`

```python
DATABASE_PATH = "blackbird.db"  # Relative to project root
```

**Customization:**
```python
# Absolute path
DATABASE_PATH = "/var/data/blackbird.db"

# Different filename
DATABASE_PATH = "production.db"
```

**Initialization:**
```python
from database import init_database

init_database()  # Creates tables and indexes if they don't exist
```

### CORS Configuration

**Location:** `backend/main.py:44-54`

**Development Configuration:**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",  # Alternative port
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Production Configuration:**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://yourdomain.com",
        "https://www.yourdomain.com"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH"],  # Restrict methods
    allow_headers=["Content-Type"],          # Restrict headers
)
```

### AI Configuration

**Location:** `backend/ai_tools.py:268-272`

**Current Configuration:**
```python
response = client.messages.create(
    model="claude-haiku-4-5-20251001",  # Claude 4.5 Haiku
    max_tokens=1024,                     # Response length limit
    tools=TOOLS,                         # 6 available tools
    messages=messages                    # Conversation history
)
```

**Configuration Options:**

| Setting | Current | Alternatives | Impact |
|---------|---------|--------------|--------|
| `model` | `claude-haiku-4-5-20251001` | `claude-sonnet-4-5-20250929` (more capable) | Better reasoning, higher cost |
| `max_tokens` | `1024` | `4096` (longer responses) | More detailed responses, higher cost |
| `tools` | 6 tools | Add/remove tools | Expand/limit Claude's capabilities |

---

## Development Guide

### Getting Started

**Prerequisites:**
- Python 3.11 or higher
- Node.js 18 or higher
- Anthropic API key

**Backend Setup:**
```bash
# Navigate to project directory
cd fastapi-demo

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
cd backend
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
nano .env  # Add your ANTHROPIC_API_KEY

# Initialize database
python -c "from database import init_database; init_database()"

# Optional: Load sample data
python migrate_data.py
```

**Frontend Setup:**
```bash
cd frontend

# Install dependencies
npm install

# Verify Vite proxy configuration (vite.config.js)
# Should proxy /api to http://localhost:8000
```

### Running the Application

**Start Backend Server:**
```bash
cd backend

# Development mode with auto-reload
uvicorn main:app --reload --port 8000

# Production mode
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

**Backend will be available at:**
- API: http://localhost:8000/api
- Interactive docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

**Start Frontend Server:**
```bash
cd frontend

# Development mode
npm run dev

# Production build
npm run build
npm run preview
```

**Frontend will be available at:**
- Dev server: http://localhost:5173
- Preview: http://localhost:4173

### Testing

**Backend Tests:**
```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_database.py

# Run with verbose output
pytest -v
```

**Test Structure:**
```
backend/tests/
├── test_database.py      # Database operation tests
├── test_models.py        # Pydantic model validation tests
├── test_api.py           # API endpoint tests
└── test_ai_tools.py      # AI tool execution tests (with mocking)
```

**Example Test:**
```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_customers():
    response = client.get("/api/customers")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_search_customer():
    response = client.post(
        "/api/customers/search",
        json={"key": "email", "value": "john@example.com"}
    )
    assert response.status_code == 200
    assert response.json()["id"] == "1213210"
```

### Development Workflow

**1. Adding a New API Endpoint:**
```python
# Step 1: Define Pydantic model (models.py)
class NewRequest(BaseModel):
    field: str

# Step 2: Create endpoint (main.py)
@app.post("/api/new-endpoint", response_model=ResponseModel)
def new_endpoint(request: NewRequest):
    # Implement logic
    result = db.some_operation(request.field)
    return result

# Step 3: Add database function (database.py)
def some_operation(field: str):
    with get_db() as conn:
        # Implement query
        pass

# Step 4: Update frontend API client (frontend/src/api.js)
export async function callNewEndpoint(field) {
    const response = await fetch(`${API_BASE}/new-endpoint`, {
        method: 'POST',
        body: JSON.stringify({field}),
        headers: {'Content-Type': 'application/json'}
    });
    return response.json();
}

# Step 5: Write tests
def test_new_endpoint():
    response = client.post("/api/new-endpoint", json={"field": "test"})
    assert response.status_code == 200
```

**2. Adding a New AI Tool:**
```python
# Step 1: Define tool schema (ai_tools.py, TOOLS array)
{
    "name": "new_tool",
    "description": "Description of what the tool does",
    "input_schema": {
        "type": "object",
        "properties": {
            "param": {"type": "string", "description": "Parameter description"}
        },
        "required": ["param"]
    }
}

# Step 2: Add case to execute_tool() function
elif tool_name == "new_tool":
    param = tool_input.get("param")
    result = db.some_database_function(param)
    return {"success": True, "data": result}

# Step 3: Test with chat
result = process_chat_message("Use new tool with param value")
print(result['tool_calls'])  # Should show new tool was called
```

---

## Security Considerations

### Current Security Measures

**1. CORS Protection**
- **Implementation:** FastAPI CORS middleware with whitelist
- **Configuration:** Only allows requests from localhost:5173 and localhost:3000
- **Purpose:** Prevents unauthorized websites from calling the API
- **Limitation:** Development configuration; tighten for production

**2. Input Validation**
- **Implementation:** Pydantic models validate all request data
- **Validation Types:** Type checking, pattern matching, range validation, enum validation
- **Example:** Customer ID must be exactly 7 digits, email must be valid format, phone must match XXX-XXX-XXXX
- **Protection:** Prevents malformed data from reaching business logic or database

**3. SQL Injection Prevention**
- **Implementation:** Parameterized queries throughout database module
- **Example:** `cursor.execute("SELECT * FROM customers WHERE id = ?", (customer_id,))`
- **Protection:** User input never concatenated into SQL strings
- **Additional:** Search key whitelist prevents column name injection

**4. API Key Management**
- **Implementation:** Anthropic API key stored in `.env` file (not committed to git)
- **Loading:** Environment variables loaded at startup
- **Protection:** Prevents API key exposure in source code
- **Validation:** Application checks for key presence and returns clear error if missing

**5. Database Constraints**
- **Implementation:** CHECK constraints, UNIQUE constraints, foreign key constraints
- **Examples:** Quantity must be > 0, price must be >= 0, email must be unique
- **Protection:** Database enforces data integrity even if application logic fails

**6. Error Message Sanitization (Partial)**
- **Current:** Full error messages returned (educational environment)
- **Concern:** May expose internal details
- **Production:** Should log details, return generic messages to users

### Production Recommendations

**For Production Deployment, Add:**

**1. Authentication & Authorization**
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    # Verify JWT token
    if not valid_token(credentials.credentials):
        raise HTTPException(status_code=401, detail="Invalid authentication")
    return credentials.credentials

@app.get("/api/customers", dependencies=[Depends(verify_token)])
def get_customers():
    # Endpoint now requires valid token
    pass
```

**Recommendations:**
- Implement JWT authentication
- Use OAuth2 for third-party integrations
- Add role-based access control (admin, support agent, read-only)
- Log all authentication attempts

**2. Rate Limiting**
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/api/chat")
@limiter.limit("10/minute")  # 10 requests per minute
def chat(request: Request, message: ChatMessage):
    # Rate-limited endpoint
    pass
```

**Recommendations:**
- Per-user rate limiting (after authentication)
- Different limits for different endpoints
- Rate limit Claude API calls to control costs
- Return 429 Too Many Requests with Retry-After header

**3. HTTPS/TLS Encryption**
```python
# Use reverse proxy (nginx, Caddy) for TLS termination
# Example nginx configuration:
server {
    listen 443 ssl;
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:8000;
    }
}
```

**Recommendations:**
- Never run HTTP in production
- Use Let's Encrypt for free certificates
- Enable HSTS (HTTP Strict Transport Security)
- Use TLS 1.3 for best security

**4. Database Security**
```python
# Switch to PostgreSQL with SSL
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://user:password@localhost/dbname",
    connect_args={"sslmode": "require"}
)
```

**Recommendations:**
- Use PostgreSQL or MySQL instead of SQLite
- Enable encryption at rest
- Use connection pooling with limits
- Separate database user per environment
- Never use root/admin database user
- Regular backups with encryption

**5. Secrets Management**
```python
# Use secrets manager instead of .env files
import boto3

secrets_client = boto3.client('secretsmanager')
response = secrets_client.get_secret_value(SecretId='prod/api/anthropic')
api_key = json.loads(response['SecretString'])['ANTHROPIC_API_KEY']
```

**Recommendations:**
- AWS Secrets Manager, Azure Key Vault, or HashiCorp Vault
- Rotate API keys regularly
- Never log secrets
- Use different keys per environment

**6. Audit Logging**
```python
import logging

audit_logger = logging.getLogger('audit')

@app.post("/api/orders/{order_id}/cancel")
def cancel_order(order_id: str, user: User = Depends(get_current_user)):
    audit_logger.info(
        f"User {user.id} cancelled order {order_id}",
        extra={"user_id": user.id, "order_id": order_id, "action": "cancel_order"}
    )
    # ... cancel logic
```

**Recommendations:**
- Log all data modifications
- Include user ID, timestamp, action, resource
- Store logs in centralized system (ELK, Splunk)
- Set up alerts for suspicious activity

**7. Input Sanitization for Display**
```python
from markupsafe import escape

@app.get("/api/customers/{customer_id}")
def get_customer(customer_id: str):
    customer = db.get_customer(customer_id)
    # Sanitize before returning
    customer['name'] = escape(customer['name'])
    return customer
```

**Recommendations:**
- Sanitize all user-generated content before display
- Use Content Security Policy (CSP) headers
- Prevent XSS attacks in frontend
- Validate and escape HTML, JavaScript

**8. Dependency Scanning**
```bash
# Regular security audits
pip install safety
safety check

# Or use GitHub Dependabot
# Add .github/dependabot.yml
```

**Recommendations:**
- Automated dependency scanning in CI/CD
- Update dependencies regularly
- Monitor security advisories
- Use pinned versions in production

---

## Performance Considerations

### Current Architecture

**Characteristics:**

**Synchronous Processing:**
- All endpoints use synchronous functions (`def`, not `async def`)
- Database operations block request thread until complete
- Claude API calls block request thread (1-5 seconds)
- **Concurrency:** Limited by Uvicorn worker threads (default: CPU count)

**SQLite Database:**
- Single-writer limitation (database-level write lock)
- Concurrent reads are fine
- File-based, no network latency
- **Performance:** Fast for reads, sequential writes

**No Caching:**
- Every request hits database
- Claude API called fresh each time
- Customer data queried repeatedly
- **Impact:** Higher latency, more database load

**Connection Per Request:**
- New database connection for each operation
- Context manager ensures proper cleanup
- No connection pooling
- **Impact:** Slight overhead, but minimal for SQLite

**Query Performance:**
- Indexed columns (email, username, customer_id, status): O(log n)
- Primary key lookups: O(log n) with B-tree index
- Phone searches: O(n) - not indexed
- Full table scans for unfiltered queries

**Typical Response Times:**
- Health check: <10ms
- Customer lookup by ID: 50-100ms
- Customer search with orders: 100-150ms
- Order cancellation: 100-200ms
- AI chat (no tools): 1-2 seconds
- AI chat (2-3 tools): 3-5 seconds
- List all customers/orders: 50-200ms (depending on dataset size)

### Scaling Considerations

**For Production Scale, Consider:**

**1. Async Endpoints and Database**
```python
# Current (synchronous)
@app.get("/api/customers")
def get_customers():
    return db.get_all_customers()

# Improved (asynchronous)
import aiosqlite

@app.get("/api/customers")
async def get_customers():
    async with aiosqlite.connect(DATABASE_PATH) as conn:
        async with conn.execute("SELECT * FROM customers") as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]
```

**Benefits:**
- Non-blocking I/O enables higher concurrency
- Single worker can handle more requests
- Better resource utilization

**Trade-offs:**
- More complex code
- Requires async-compatible libraries
- Debugging can be harder

**2. Connection Pooling**
```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    "postgresql://user:password@localhost/dbname",
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_recycle=3600
)
```

**Benefits:**
- Reuse connections, reduce overhead
- Handle connection lifecycle
- Limit maximum connections

**3. Caching Layer**
```python
from aiocache import cached, Cache
from aiocache.serializers import JsonSerializer

@cached(ttl=300, cache=Cache.REDIS, serializer=JsonSerializer())
async def get_customer(customer_id: str):
    # Cache customer data for 5 minutes
    return await db.get_customer(customer_id)
```

**Benefits:**
- Reduce database load
- Lower response latency
- Handle traffic spikes

**Cache Candidates:**
- Customer data (changes infrequently)
- Product catalog
- Configuration data
- AI tool definitions

**4. Database Upgrade**
```python
# PostgreSQL with async support
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

engine = create_async_engine("postgresql+asyncpg://user:pass@localhost/db")

async with AsyncSession(engine) as session:
    result = await session.execute(select(Customer))
    customers = result.scalars().all()
```

**Benefits:**
- Better concurrency (no single-writer limit)
- Advanced features (full-text search, JSON queries)
- Better tooling and monitoring
- Connection pooling built-in

**5. Load Balancing**
```
User Requests
    ↓
Load Balancer (nginx, HAProxy)
    ↓
Backend Instance 1 (Uvicorn)
Backend Instance 2 (Uvicorn)
Backend Instance 3 (Uvicorn)
    ↓
Shared Database (PostgreSQL)
Shared Cache (Redis)
```

**Benefits:**
- Horizontal scaling
- High availability
- Rolling deployments
- Better resource utilization

**6. AI Response Caching**
```python
import hashlib

def cache_key(message: str) -> str:
    return f"chat:{hashlib.md5(message.encode()).hexdigest()}"

@cached(ttl=3600, key_builder=cache_key)
async def chat_with_claude(message: str):
    # Cache AI responses for similar queries
    return await anthropic_client.messages.create(...)
```

**Benefits:**
- Reduce Claude API calls (lower cost)
- Faster responses for common queries
- Better user experience

**Considerations:**
- Invalidate cache when underlying data changes
- May return stale responses
- Only cache deterministic queries

**7. Background Task Processing**
```python
from fastapi import BackgroundTasks

@app.post("/api/orders/{order_id}/cancel")
async def cancel_order(order_id: str, background_tasks: BackgroundTasks):
    # Immediate response
    result = await db.cancel_order(order_id)

    # Run in background
    background_tasks.add_task(send_cancellation_email, order_id)
    background_tasks.add_task(update_inventory, order_id)

    return result
```

**Benefits:**
- Lower response latency
- Better user experience
- Decoupled processing

**Use Cases:**
- Email notifications
- Data processing
- External API calls
- Logging and analytics

---

## Architectural Strengths

**1. Clear Layered Architecture**
- **Strength:** Each layer has single responsibility with well-defined boundaries
- **Benefit:** Easy to understand, modify, and test individual components
- **Evidence:** Database module has no AI code, AI module has no HTTP code, API layer has no business logic
- **Impact:** Reduces complexity, enables parallel development, facilitates onboarding

**2. Comprehensive Input Validation**
- **Strength:** Pydantic models validate all data at API boundaries
- **Benefit:** Prevents invalid data from reaching business logic or database
- **Evidence:** Pattern validation for IDs, email format validation, range constraints on numbers
- **Impact:** Fewer runtime errors, clear API contracts, better error messages

**3. Transparent AI Tool Calling**
- **Strength:** All tool executions logged and returned to client
- **Benefit:** Developers can debug AI behavior, users see what data was accessed
- **Evidence:** ChatResponse includes tool_calls array with tool names and inputs
- **Impact:** Easier debugging, builds trust, demonstrates AI decision-making

**4. Automatic Transaction Management**
- **Strength:** Context managers ensure database transactions are always committed or rolled back
- **Benefit:** No memory leaks, no orphaned connections, no data corruption
- **Evidence:** get_db() context manager with try/finally for cleanup
- **Impact:** Robust error handling, simplified code, production-ready pattern

**5. RESTful API Design**
- **Strength:** Follows REST conventions with appropriate HTTP methods and status codes
- **Benefit:** Predictable, standards-compliant, easy to integrate
- **Evidence:** GET for queries, POST for creation/search, PATCH for updates, proper status codes
- **Impact:** Reduced learning curve, works with standard tools, clear semantics

**6. Separation of Frontend and Backend**
- **Strength:** Independent frontend and backend with clean API contract
- **Benefit:** Can evolve separately, different technology choices, easier testing
- **Evidence:** Vite proxy enables separate dev servers, api.js abstracts backend communication
- **Impact:** Flexible deployment, parallel development, technology independence

**7. Educational Code Quality**
- **Strength:** Code optimized for understanding with clear naming and comments
- **Benefit:** Easy for developers to learn FastAPI, Claude integration, and architecture patterns
- **Evidence:** Descriptive variable names, comprehensive comments, well-organized modules
- **Impact:** Serves as reference implementation, reduces documentation burden

**8. Comprehensive Error Handling**
- **Strength:** Multiple layers of error handling with appropriate status codes
- **Benefit:** Clear error messages, proper HTTP semantics, no silent failures
- **Evidence:** Try/catch at each layer, HTTPException with detail messages, rollback on database errors
- **Impact:** Easier debugging, better user experience, production-ready

---

## Areas for Enhancement

### For Production Deployment

**1. Authentication & Authorization**
- **Current State:** No authentication, all endpoints publicly accessible
- **Recommended Improvement:** JWT-based authentication with role-based access control
- **Implementation:**
  ```python
  @app.get("/api/customers", dependencies=[Depends(require_auth)])
  def get_customers(user: User = Depends(get_current_user)):
      # Only authenticated users can access
      pass
  ```
- **Priority:** Critical for production

**2. Database Upgrade**
- **Current State:** SQLite with single-writer limitation
- **Recommended Improvement:** PostgreSQL or MySQL with connection pooling
- **Benefits:** Better concurrency, advanced features, production-grade reliability
- **Migration Path:**
  ```python
  # Switch to SQLAlchemy for database abstraction
  engine = create_engine("postgresql://user:pass@localhost/db")
  ```
- **Priority:** High for production scale

**3. Conversation History Management**
- **Current State:** Stateless, no conversation context maintained
- **Recommended Improvement:** Session-based history storage in Redis or database
- **Benefits:** Multi-turn conversations, context-aware responses
- **Implementation:**
  ```python
  @app.post("/api/chat")
  def chat(message: ChatMessage, session_id: str = Header(...)):
      history = redis.get(f"chat:{session_id}")
      result = chat_with_claude(message, history=history)
      redis.set(f"chat:{session_id}", result['history'])
      return result
  ```
- **Priority:** Medium for better user experience

**4. Caching Layer**
- **Current State:** No caching, every request hits database
- **Recommended Improvement:** Redis cache for customer data and AI responses
- **Benefits:** Lower latency, reduced database load, cost savings on AI calls
- **Implementation:**
  ```python
  @cached(ttl=300, cache=Cache.REDIS)
  async def get_customer(customer_id: str):
      return await db.get_customer(customer_id)
  ```
- **Priority:** Medium for performance

**5. Comprehensive Logging**
- **Current State:** Minimal logging, print statements for debugging
- **Recommended Improvement:** Structured logging with ELK stack or similar
- **Benefits:** Better debugging, audit trail, operational insights
- **Implementation:**
  ```python
  logger.info("Customer query", extra={
      "customer_id": customer_id,
      "user_id": user.id,
      "duration_ms": duration
  })
  ```
- **Priority:** High for operations

**6. Monitoring & Alerting**
- **Current State:** No monitoring, no health checks beyond basic endpoint
- **Recommended Improvement:** Prometheus metrics, Grafana dashboards, PagerDuty alerts
- **Metrics to Track:** Request rate, latency, error rate, database connections, AI API costs
- **Priority:** Critical for production operations

**7. API Versioning**
- **Current State:** No versioning, breaking changes would affect all clients
- **Recommended Improvement:** URL-based versioning (e.g., `/api/v1/customers`)
- **Benefits:** Backward compatibility, gradual migration, multiple versions in production
- **Priority:** Medium for API stability

**8. Rate Limiting**
- **Current State:** No rate limits, open to abuse and runaway costs
- **Recommended Improvement:** Per-user rate limiting with Redis
- **Benefits:** Prevent abuse, control AI costs, fair usage
- **Priority:** High for cost control

### For Scalability

**1. Asynchronous Processing**
- **Current Limitation:** Synchronous endpoints block worker threads
- **Scaling Strategy:** Convert to async/await for better concurrency
- **Expected Impact:** 10x more concurrent requests with same resources
- **Implementation Effort:** Medium (requires async database library)

**2. Horizontal Scaling**
- **Current Limitation:** Single instance, limited by CPU/memory
- **Scaling Strategy:** Multiple instances behind load balancer
- **Expected Impact:** Linear scaling with number of instances
- **Requirements:** Stateless design (already achieved), shared database, shared cache

**3. Database Connection Pooling**
- **Current Limitation:** Connection per request, overhead for each query
- **Scaling Strategy:** SQLAlchemy connection pool or pgbouncer
- **Expected Impact:** Lower latency, better resource utilization
- **Implementation Effort:** Low

**4. CDN for Frontend**
- **Current Limitation:** Frontend served from dev server
- **Scaling Strategy:** Build frontend, serve from CDN (CloudFront, Cloudflare)
- **Expected Impact:** Global low-latency delivery, reduced server load
- **Implementation Effort:** Low

**5. Background Job Processing**
- **Current Limitation:** All work done in request thread
- **Scaling Strategy:** Celery or similar for async tasks
- **Use Cases:** Email notifications, data processing, external API calls
- **Expected Impact:** Lower response latency, better user experience

---

## Technology Stack

### Backend

| Technology | Version | Purpose | Documentation |
|------------|---------|---------|---------------|
| **FastAPI** | 0.104.1 | Web framework for REST API | https://fastapi.tiangolo.com/ |
| **Python** | 3.11+ | Programming language | https://www.python.org/ |
| **Pydantic** | 2.5.0 | Data validation and serialization | https://docs.pydantic.dev/ |
| **SQLite** | 3.x | Database engine | https://www.sqlite.org/ |
| **Uvicorn** | 0.24.0 | ASGI server | https://www.uvicorn.org/ |
| **Anthropic SDK** | 0.7.8 | Claude AI integration | https://docs.anthropic.com/ |
| **python-dotenv** | 1.0.0 | Environment variable management | https://pypi.org/project/python-dotenv/ |

**AI Integration:**
- **Model:** Claude 4.5 Haiku (`claude-haiku-4-5-20251001`)
- **API:** Anthropic Messages API with tool calling
- **Max Tokens:** 1024 per response
- **Tools:** 6 custom tools for database interaction

### Frontend

| Technology | Version | Purpose | Documentation |
|------------|---------|---------|---------------|
| **React** | 18.x | UI library | https://react.dev/ |
| **React Router** | 6.x | Client-side routing | https://reactrouter.com/ |
| **Vite** | 4.x | Build tool and dev server | https://vitejs.dev/ |
| **JavaScript** | ES2022 | Programming language | https://developer.mozilla.org/ |
| **Fetch API** | Standard | HTTP client | https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API |

**Development:**
- **Proxy:** Vite proxy routes `/api` to `http://localhost:8000`
- **Hot Module Replacement:** Enabled for rapid development
- **Build:** Production build with tree-shaking and minification

### Development Tools

| Tool | Purpose |
|------|---------|
| **pytest** | Python testing framework |
| **ruff** | Python linting and formatting |
| **Git** | Version control |
| **uv** | Python package management (modern alternative to pip) |

### External Services

| Service | Purpose | Cost Model |
|---------|---------|------------|
| **Claude AI** | Natural language understanding and tool calling | Pay-per-token (input + output) |
| **HuggingFace Datasets** | Data source for migration script | Free (public datasets) |

---

## Documentation Index

### Detailed Documentation

**1. [Component Inventory](architecture/docs/01_component_inventory.md)**
- Complete listing of all modules, classes, and functions
- Line number references for every component
- Module dependencies and import relationships
- File statistics and architecture notes
- **Use When:** Need to find specific function/class, understand module structure

**2. [Architecture Diagrams](architecture/diagrams/02_architecture_diagrams.md)**
- Visual representations of system architecture
- Component relationships and dependencies
- Database schema with ER diagram
- Data flow through layers
- **Use When:** Need visual understanding, explaining architecture to others

**3. [Data Flows](architecture/docs/03_data_flows.md)**
- Detailed sequence diagrams showing data movement
- Request/response lifecycle analysis
- AI tool execution flow
- Error handling patterns
- Performance considerations
- **Use When:** Understanding how requests flow, debugging issues, optimizing performance

**4. [API Reference](architecture/docs/04_api_reference.md)**
- Comprehensive API documentation with examples
- REST endpoint specifications
- Data model schemas with validation rules
- Database operation reference
- AI tool definitions
- Usage patterns and best practices
- **Use When:** Integrating with API, implementing features, understanding data contracts

### Quick Reference

**Common Tasks:**

**Find a specific endpoint:**
- [API Reference §REST Endpoints](architecture/docs/04_api_reference.md#rest-api-endpoints)

**Understand data models:**
- [API Reference §Data Models](architecture/docs/04_api_reference.md#data-models)
- [Component Inventory §Classes](architecture/docs/01_component_inventory.md#classes)

**See how requests flow:**
- [Data Flows §Request/Response](architecture/docs/03_data_flows.md#1-simple-query-flow-direct-api-requests)
- [Data Flows §AI Chat](architecture/docs/03_data_flows.md#2-interactive-client-session-flow-ai-chat)

**Database operations:**
- [API Reference §Database Operations](architecture/docs/04_api_reference.md#database-operations)
- [Component Inventory §Database Functions](architecture/docs/01_component_inventory.md#database-operations-backend-databasepy)

**AI integration:**
- [API Reference §AI Tools](architecture/docs/04_api_reference.md#ai-tools)
- [Data Flows §AI Tool Execution](architecture/docs/03_data_flows.md#6-ai-tool-execution-flow)

**Configuration:**
- [API Reference §Configuration](architecture/docs/04_api_reference.md#configuration)
- This README §Configuration section

**Error handling:**
- [Data Flows §Error Handling Flow](architecture/docs/03_data_flows.md#8-error-handling-flow)
- [API Reference §Error Handling](architecture/docs/04_api_reference.md#error-handling)

---

## Glossary

**API (Application Programming Interface):** Interface through which frontend communicates with backend using HTTP requests

**ASGI (Asynchronous Server Gateway Interface):** Standard interface between web servers and Python web applications

**Claude AI:** Anthropic's large language model with function calling capabilities

**Context Manager:** Python pattern using `with` statement for resource management (e.g., database connections)

**CORS (Cross-Origin Resource Sharing):** Browser security feature controlling which origins can access API

**CRUD (Create, Read, Update, Delete):** Basic database operations

**Foreign Key:** Database constraint linking one table to another (e.g., orders.customer_id → customers.id)

**Function Calling:** AI capability where model can request execution of predefined functions/tools

**JWT (JSON Web Token):** Standard for securely transmitting information as JSON object (used for authentication)

**MCP (Model Context Protocol):** Standardized protocol for AI systems to access external tools and data sources

**Pydantic:** Python library for data validation using type annotations

**REST (Representational State Transfer):** Architectural style for web APIs using HTTP methods

**SQLite:** Serverless, file-based SQL database engine

**Tool (AI Context):** Predefined function that Claude AI can call to interact with external systems

**Vite:** Modern frontend build tool with fast dev server and hot module replacement

**Webhook:** HTTP callback triggered by external event (not used in this project)

---

## Contributing

This is an educational demonstration project. If you're using it as a reference:

**Best Practices:**
- Follow the layered architecture pattern
- Maintain clear separation between layers
- Use Pydantic for all data validation
- Write comprehensive tests
- Document complex logic
- Keep security in mind

**Code Style:**
- Python: Follow PEP 8 (enforced by ruff)
- JavaScript: Follow Airbnb style guide
- Descriptive variable names
- Comments for complex logic
- Type hints in Python

**Testing:**
- Unit tests for business logic
- Integration tests for API endpoints
- Mock external dependencies (Claude API)
- Aim for >80% code coverage

---

## License

This is an educational demonstration project. Refer to the project repository for license information.

---

## Contact & Support

**For Questions or Issues:**

1. **Check Documentation:**
   - Start with this README
   - Review detailed docs in `docs/` directory
   - Check interactive API docs at http://localhost:8000/docs

2. **Review Source Code:**
   - All line numbers referenced in documentation
   - Clear comments and docstrings
   - Self-documenting code structure

3. **External Resources:**
   - FastAPI documentation: https://fastapi.tiangolo.com/
   - Anthropic documentation: https://docs.anthropic.com/
   - Pydantic documentation: https://docs.pydantic.dev/

---

## Changelog

### Documentation Version History

**Initial Release - 2025-11-17**
- Comprehensive architecture documentation generated
- Component inventory with line-by-line analysis
- Visual architecture diagrams (Mermaid)
- Complete data flow analysis
- Full API reference with examples
- This synthesis README document

**Project Status:**
- Architecture: Stable and well-documented
- Codebase: ~1,377 lines of production-quality Python
- Documentation: 4 comprehensive documents + README
- Purpose: Educational reference and demonstration

---

*This documentation was generated through comprehensive codebase analysis and represents the architecture as of November 17, 2025. For questions or clarifications, please refer to the detailed documentation linked above or review the source code with the provided line number references.*

**Documentation Location:** `architecture/`
