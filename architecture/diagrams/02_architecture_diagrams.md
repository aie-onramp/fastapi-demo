# Architecture Diagrams

## Overview

This document provides comprehensive architectural diagrams for the Blackbird Customer Support Application, a full-stack web application demonstrating Claude AI integration with FastAPI and React. The system consists of:

- **Frontend**: React SPA with three main pages (AI Chat, Customers, Orders)
- **Backend**: FastAPI REST API with AI tool calling integration
- **Database**: SQLite database for customer and order management
- **AI Integration**: Claude AI (Anthropic) with 6 custom tools for customer support operations

---

## 1. System Architecture (Layered View)

This diagram shows the high-level architecture organized into distinct layers, illustrating the separation of concerns and data flow through the system.

```mermaid
graph TB
    subgraph "Presentation Layer"
        A[React Frontend]
        A1[ChatPage.jsx]
        A2[CustomersPage.jsx]
        A3[OrdersPage.jsx]
        A4[Components]
    end

    subgraph "API Layer"
        B[Vite Dev Proxy]
        C[FastAPI Backend]
        C1["/api/chat"]
        C2["/api/customers/*"]
        C3["/api/orders/*"]
        C4[CORS Middleware]
    end

    subgraph "Business Logic Layer"
        D[API Route Handlers]
        E[Pydantic Models]
        F[AI Tools Module]
        F1[execute_tool]
        F2[chat_with_claude]
    end

    subgraph "Integration Layer"
        G[Claude AI API]
        G1[6 Custom Tools]
        G2[Function Calling]
    end

    subgraph "Data Access Layer"
        H[Database Module]
        H1[Customer CRUD]
        H2[Order CRUD]
        H3[Context Manager]
    end

    subgraph "Data Storage Layer"
        I[(SQLite Database)]
        I1[(customers table)]
        I2[(orders table)]
    end

    A --> B
    B --> C
    C --> D
    D --> E
    D --> F
    F --> G
    D --> H
    H --> I

    A1 --> A
    A2 --> A
    A3 --> A
    A4 --> A

    C1 --> C
    C2 --> C
    C3 --> C
    C4 --> C

    F1 --> F
    F2 --> F

    G1 --> G
    G2 --> G

    H1 --> H
    H2 --> H
    H3 --> H

    I1 --> I
    I2 --> I

    style A fill:#e1f5ff
    style C fill:#fff3e0
    style D fill:#f3e5f5
    style F fill:#e8f5e9
    style G fill:#fce4ec
    style H fill:#fff9c4
    style I fill:#e0f2f1
```

### Key Points

- **Presentation Layer**: React-based SPA with client-side routing (React Router). Three main pages for different user workflows.
- **API Layer**: FastAPI serves RESTful endpoints with CORS enabled. Vite proxy handles development routing.
- **Business Logic Layer**: Route handlers orchestrate data validation (Pydantic), database operations, and AI integration.
- **Integration Layer**: Claude AI provides intelligent assistance through 6 custom tools (get_user, get_order_by_id, get_customer_orders, cancel_order, update_user_contact, get_user_info).
- **Data Access Layer**: Abstracted database operations with context managers for connection handling.
- **Data Storage Layer**: SQLite database with foreign key constraints and indexed columns for performance.

---

## 2. Component Relationships

This diagram illustrates how the main modules and components interact with each other, showing the dependencies and communication patterns.

```mermaid
graph TB
    subgraph "Frontend (React)"
        FE_MAIN[main.jsx]
        FE_APP[App.jsx]
        FE_API[api.js]

        subgraph "Pages"
            PAGE_CHAT[ChatPage]
            PAGE_CUST[CustomersPage]
            PAGE_ORD[OrdersPage]
        end

        subgraph "Components"
            COMP_MSG[ChatMessage]
            COMP_TBL[DataTable]
            COMP_SEARCH[SearchBar]
        end
    end

    subgraph "Backend (Python)"
        BE_MAIN[main.py]
        BE_MODELS[models.py]
        BE_DB[database.py]
        BE_AI[ai_tools.py]

        subgraph "External Dependencies"
            LIB_FASTAPI[FastAPI]
            LIB_PYDANTIC[Pydantic]
            LIB_SQLITE[sqlite3]
            LIB_ANTHROPIC[Anthropic SDK]
        end
    end

    subgraph "External Services"
        EXT_CLAUDE[Claude AI API]
        EXT_DB[(blackbird.db)]
    end

    %% Frontend relationships
    FE_MAIN --> FE_APP
    FE_APP --> PAGE_CHAT
    FE_APP --> PAGE_CUST
    FE_APP --> PAGE_ORD

    PAGE_CHAT --> COMP_MSG
    PAGE_CUST --> COMP_TBL
    PAGE_CUST --> COMP_SEARCH
    PAGE_ORD --> COMP_TBL

    PAGE_CHAT --> FE_API
    PAGE_CUST --> FE_API
    PAGE_ORD --> FE_API

    %% Frontend to Backend
    FE_API -.HTTP/JSON.-> BE_MAIN

    %% Backend relationships
    BE_MAIN --> BE_MODELS
    BE_MAIN --> BE_DB
    BE_MAIN --> BE_AI

    BE_AI --> BE_DB
    BE_AI --> LIB_ANTHROPIC

    BE_MAIN --> LIB_FASTAPI
    BE_MODELS --> LIB_PYDANTIC
    BE_DB --> LIB_SQLITE

    %% External connections
    LIB_ANTHROPIC -.HTTPS.-> EXT_CLAUDE
    LIB_SQLITE --> EXT_DB

    style FE_MAIN fill:#e3f2fd
    style FE_APP fill:#e3f2fd
    style FE_API fill:#e3f2fd
    style BE_MAIN fill:#fff3e0
    style BE_MODELS fill:#fff3e0
    style BE_DB fill:#fff3e0
    style BE_AI fill:#fff3e0
    style EXT_CLAUDE fill:#fce4ec
    style EXT_DB fill:#e0f2f1
```

### Key Points

- **Frontend Entry Point**: `main.jsx` initializes React and renders `App.jsx`
- **Routing**: `App.jsx` manages client-side routing to three pages
- **API Abstraction**: `api.js` provides a clean interface for all backend communication
- **Page Components**: Each page imports shared components (ChatMessage, DataTable, SearchBar)
- **Backend Entry Point**: `main.py` defines FastAPI app and all route handlers
- **Data Validation**: `models.py` (Pydantic) ensures type safety for all API requests/responses
- **Data Persistence**: `database.py` handles all SQLite operations with context managers
- **AI Integration**: `ai_tools.py` manages Claude AI communication and tool execution
- **External Dependencies**: Clear separation of framework code (FastAPI, Pydantic, Anthropic SDK)

---

## 3. Class Hierarchies

This diagram shows the Pydantic model structure and their relationships, which define the data contracts throughout the application.

```mermaid
classDiagram
    class BaseModel {
        <<Pydantic>>
        +model_validate()
        +model_dump()
        +Config
    }

    class Customer {
        +str id
        +str name
        +EmailStr email
        +str phone
        +str username
        +pattern: r'^\\d{7}$' (id)
        +pattern: r'^\\d{3}-\\d{3}-\\d{4}$' (phone)
        +pattern: r'^[a-zA-Z0-9_]+$' (username)
    }

    class CustomerUpdate {
        +Optional~EmailStr~ email
        +Optional~str~ phone
        +pattern: r'^\\d{3}-\\d{3}-\\d{4}$' (phone)
    }

    class CustomerSearch {
        +Literal['email'|'phone'|'username'] key
        +str value
    }

    class Order {
        +str id
        +str customer_id
        +str product
        +int quantity
        +float price
        +Literal['Processing'|'Shipped'|'Delivered'|'Cancelled'] status
        +pattern: r'^\\d{5}$' (id)
        +pattern: r'^\\d{7}$' (customer_id)
        +constraint: quantity > 0
        +constraint: price >= 0
    }

    class OrderCancelResponse {
        +bool success
        +str message
    }

    class ChatMessage {
        +str message
        +min_length: 1
        +max_length: 4000
    }

    class ChatResponse {
        +str response
        +Optional~List~Dict~str,Any~~~ tool_calls
    }

    class CustomerWithOrders {
        +Customer customer
        +List~Order~ orders
    }

    class ErrorResponse {
        +str error
        +Optional~str~ detail
    }

    BaseModel <|-- Customer
    BaseModel <|-- CustomerUpdate
    BaseModel <|-- CustomerSearch
    BaseModel <|-- Order
    BaseModel <|-- OrderCancelResponse
    BaseModel <|-- ChatMessage
    BaseModel <|-- ChatResponse
    BaseModel <|-- CustomerWithOrders
    BaseModel <|-- ErrorResponse

    CustomerWithOrders *-- Customer
    CustomerWithOrders *-- Order

    note for Customer "7-digit ID\nEmail validation\nPhone format XXX-XXX-XXXX"
    note for Order "5-digit ID\nForeign key to Customer\nStatus enum constraint"
    note for CustomerWithOrders "Composite model\nCombines Customer + Orders"
```

### Key Points

- **Inheritance**: All models inherit from Pydantic's `BaseModel` for automatic validation
- **Field Validation**: Pattern matching ensures data integrity (customer ID: 7 digits, order ID: 5 digits, phone format)
- **Type Safety**: EmailStr provides email validation, Literal types enforce enums
- **Constraints**: Quantity must be positive, price must be non-negative
- **Composition**: `CustomerWithOrders` combines customer and order data for efficient queries
- **API Contracts**: These models define the shape of all API requests and responses
- **Optional Fields**: `CustomerUpdate` allows partial updates, `ChatResponse.tool_calls` is optional for transparency

---

## 4. Module Dependencies

This diagram shows the import relationships between Python modules, revealing the dependency structure and potential circular dependencies.

```mermaid
graph LR
    subgraph "Backend Modules"
        MAIN[main.py]
        MODELS[models.py]
        DB[database.py]
        AI[ai_tools.py]
    end

    subgraph "Standard Library"
        STD_OS[os]
        STD_JSON[json]
        STD_SQLITE[sqlite3]
        STD_TYPING[typing]
        STD_CTX[contextlib]
        STD_PATH[pathlib]
    end

    subgraph "Third-Party"
        FASTAPI[fastapi]
        PYDANTIC[pydantic]
        ANTHROPIC[anthropic]
        DOTENV[python-dotenv]
        UVICORN[uvicorn]
    end

    %% main.py imports
    MAIN --> FASTAPI
    MAIN --> DOTENV
    MAIN --> STD_TYPING
    MAIN --> STD_OS
    MAIN --> STD_PATH
    MAIN --> MODELS
    MAIN --> DB
    MAIN --> AI
    MAIN --> UVICORN

    %% models.py imports
    MODELS --> PYDANTIC
    MODELS --> STD_TYPING

    %% database.py imports
    DB --> STD_SQLITE
    DB --> STD_CTX
    DB --> STD_TYPING

    %% ai_tools.py imports
    AI --> STD_OS
    AI --> STD_JSON
    AI --> STD_TYPING
    AI --> ANTHROPIC
    AI --> DB

    style MAIN fill:#ff9800
    style MODELS fill:#4caf50
    style DB fill:#2196f3
    style AI fill:#9c27b0
    style FASTAPI fill:#e0e0e0
    style PYDANTIC fill:#e0e0e0
    style ANTHROPIC fill:#e0e0e0
    style DOTENV fill:#e0e0e0
```

### Key Points

- **Entry Point**: `main.py` is the root module that imports all other application modules
- **Clean Separation**: No circular dependencies between modules
- **Database Independence**: `database.py` only depends on standard library (sqlite3, contextlib, typing)
- **Model Isolation**: `models.py` only depends on Pydantic, no application logic
- **AI Integration**: `ai_tools.py` depends on `database.py` but not `models.py` or `main.py`
- **Dependency Flow**: main.py → {models.py, database.py, ai_tools.py}, ai_tools.py → database.py
- **Framework Usage**: FastAPI and Pydantic in presentation layer, Anthropic SDK in AI layer, SQLite in data layer

---

## 5. API Request Flow

This sequence diagram illustrates how a typical chat request flows through the system, demonstrating the multi-turn conversation pattern with Claude AI tool calling.

```mermaid
sequenceDiagram
    actor User
    participant Frontend as React Frontend
    participant API as api.js
    participant Vite as Vite Proxy
    participant FastAPI as FastAPI Backend
    participant Handler as Route Handler
    participant AITools as ai_tools.py
    participant Claude as Claude AI API
    participant DB as database.py
    participant SQLite as SQLite DB

    User->>Frontend: Types "Look up john@example.com"
    Frontend->>API: sendChatMessage(message)
    API->>Vite: POST /api/chat
    Vite->>FastAPI: Forward to :8000/api/chat
    FastAPI->>Handler: chat(ChatMessage)
    Handler->>AITools: process_chat_message(message)

    Note over AITools: Create conversation with tools
    AITools->>Claude: messages.create(tools=TOOLS)

    Note over Claude: Decides to use get_user tool
    Claude-->>AITools: Response with tool_use

    Note over AITools: Extract tool_use blocks
    AITools->>AITools: execute_tool("get_user", {...})
    AITools->>DB: search_customer("email", "john@...")
    DB->>SQLite: SELECT * FROM customers WHERE email=?
    SQLite-->>DB: Row data
    DB-->>AITools: Customer dict

    Note over AITools: Send tool results back
    AITools->>Claude: messages.create(tool_results)
    Claude-->>AITools: Final text response

    AITools-->>Handler: {response, tool_calls}
    Handler-->>FastAPI: ChatResponse(...)
    FastAPI-->>Vite: JSON response
    Vite-->>API: HTTP 200 + JSON
    API-->>Frontend: {response, tool_calls}
    Frontend->>User: Display AI response
```

### Key Points

- **Vite Proxy**: Development proxy routes `/api/*` to backend `localhost:8000/api/*`
- **Request Validation**: FastAPI automatically validates request body against `ChatMessage` Pydantic model
- **Multi-Turn Conversation**: Claude AI may call tools multiple times before final response
- **Tool Execution Loop**: While `stop_reason == "tool_use"`, execute tools and send results back
- **Tool Transparency**: Response includes `tool_calls` array for debugging/transparency
- **Database Access**: Each tool execution may query the database through the abstracted `database.py` module
- **Error Handling**: Try-catch at multiple levels (API layer, tool execution, database access)
- **Response Serialization**: Pydantic models ensure type-safe JSON serialization

---

## 6. Database Schema

This ER diagram shows the database structure, relationships, and constraints.

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

### Database Details

**Indexes:**
```sql
-- Performance indexes
CREATE INDEX idx_customers_email ON customers(email);
CREATE INDEX idx_customers_username ON customers(username);
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_orders_status ON orders(status);
```

**Constraints:**
- **Foreign Key**: `orders.customer_id` references `customers.id` with `ON DELETE CASCADE`
- **CHECK Constraints**:
  - `customers.name` length >= 1
  - `customers.email` LIKE '%@%.%'
  - `customers.phone` length >= 10
  - `customers.username` length 3-20
  - `orders.quantity` > 0
  - `orders.price` >= 0
  - `orders.status` IN ('Processing', 'Shipped', 'Delivered', 'Cancelled')
  - `orders.product` length >= 1

**Relationship:**
- One customer can have many orders (1:N)
- Cascade delete: When customer is deleted, all their orders are deleted

### Key Points

- **Primary Keys**: Text-based IDs (customer: 7 digits, order: 5 digits)
- **Unique Constraints**: Email and username must be unique across customers
- **Referential Integrity**: Foreign key constraint with cascade delete
- **Data Validation**: CHECK constraints enforce business rules at database level
- **Query Performance**: Indexes on frequently searched columns (email, username, customer_id, status)
- **Status Enum**: Orders have exactly 4 possible statuses
- **Row Factory**: `sqlite3.Row` used in context manager for dictionary-like access

---

## 7. AI Integration Flow

This diagram shows how the Claude AI integration works with tool calling, including the tool definitions and execution flow.

```mermaid
sequenceDiagram
    participant User
    participant Backend as FastAPI Handler
    participant AIModule as ai_tools.py
    participant Claude as Claude AI API
    participant ToolExec as Tool Executor
    participant DB as database.py

    User->>Backend: Chat message
    Backend->>AIModule: process_chat_message(msg)

    rect rgb(240, 248, 255)
        Note over AIModule: Define 6 Tools
        AIModule->>AIModule: TOOLS = [get_user, get_order_by_id,<br/>get_customer_orders, cancel_order,<br/>update_user_contact, get_user_info]
    end

    AIModule->>Claude: messages.create(<br/>model="claude-haiku-4-5",<br/>tools=TOOLS,<br/>messages=[{role: user, content: msg}])

    alt Claude wants to use tools
        Claude-->>AIModule: stop_reason="tool_use"<br/>content=[{type: tool_use, name: "get_user", ...}]

        loop For each tool_use block
            AIModule->>ToolExec: execute_tool(name, input)

            alt get_user
                ToolExec->>DB: search_customer(key, value)
                DB-->>ToolExec: customer dict
            else get_order_by_id
                ToolExec->>DB: get_order(order_id)
                DB-->>ToolExec: order dict
            else get_customer_orders
                ToolExec->>DB: get_customer_orders(customer_id)
                DB-->>ToolExec: orders list
            else cancel_order
                ToolExec->>DB: cancel_order(order_id)
                DB-->>ToolExec: {success, message}
            else update_user_contact
                ToolExec->>DB: update_customer(id, email, phone)
                DB-->>ToolExec: success bool
            else get_user_info
                ToolExec->>DB: search_customer + get_customer_orders
                DB-->>ToolExec: {customer, orders}
            end

            ToolExec-->>AIModule: tool_result
        end

        AIModule->>Claude: messages.create(<br/>messages=[...previous, tool_results])
        Claude-->>AIModule: stop_reason="end_turn"<br/>content=[{type: text, text: "..."}]
    else Claude responds directly
        Claude-->>AIModule: stop_reason="end_turn"<br/>content=[{type: text, text: "..."}]
    end

    AIModule-->>Backend: {response: text, tool_calls: [...]}
    Backend-->>User: ChatResponse
```

### AI Tools Reference

**Tool Definitions (ai_tools.py lines 26-129):**

1. **get_user**: Search customer by email, phone, or username
   - Input: `{key: enum, value: string}`
   - Returns: Customer information if found

2. **get_order_by_id**: Lookup order by 5-digit order ID
   - Input: `{order_id: string}`
   - Returns: Order details (product, quantity, price, status)

3. **get_customer_orders**: Get all orders for a customer
   - Input: `{customer_id: string}`
   - Returns: List of orders

4. **cancel_order**: Cancel an order (only if status = 'Processing')
   - Input: `{order_id: string}`
   - Returns: `{success: bool, message: string}`

5. **update_user_contact**: Update customer email/phone
   - Input: `{customer_id: string, email?: string, phone?: string}`
   - Returns: `{success: bool, message: string}`

6. **get_user_info**: Combined customer + orders query
   - Input: `{key: enum, value: string}`
   - Returns: `{customer: {...}, orders: [...], order_count: int}`

### Key Points

- **Model**: Uses `claude-haiku-4-5-20251001` (latest Claude 3.5 Haiku model)
- **Tool Schema**: JSON Schema format defining input parameters and descriptions
- **Multi-Turn Loop**: Continues sending tool results back until Claude finishes (`stop_reason != "tool_use"`)
- **Error Handling**: Try-catch around tool execution returns error in tool result
- **Tool Transparency**: All tool calls logged and returned to frontend for debugging
- **Stateless**: Current implementation doesn't maintain conversation history (educational simplification)
- **Function Dispatch**: `execute_tool()` routes to appropriate database function based on tool name
- **Business Logic**: Tools enforce business rules (e.g., can only cancel Processing orders)

---

## Additional Architecture Notes

### File Structure
```
{PROJECT_ROOT}/
├── backend/
│   ├── main.py           # FastAPI app, routes, startup
│   ├── models.py         # Pydantic models
│   ├── database.py       # SQLite CRUD operations
│   ├── ai_tools.py       # Claude AI integration
│   └── blackbird.db      # SQLite database file
├── frontend/
│   ├── src/
│   │   ├── main.jsx      # React entry point
│   │   ├── App.jsx       # Routing and navigation
│   │   ├── api.js        # Backend API wrapper
│   │   ├── pages/        # ChatPage, CustomersPage, OrdersPage
│   │   └── components/   # Reusable UI components
│   └── index.html        # HTML template
└── pyproject.toml        # Python dependencies
```

### Technology Stack

**Frontend:**
- React 18 with JSX
- React Router for client-side routing
- Vite for development server and build
- Fetch API for HTTP requests

**Backend:**
- FastAPI for REST API
- Pydantic for data validation
- SQLite3 for database
- Anthropic SDK for Claude AI
- Uvicorn for ASGI server

**Development:**
- CORS enabled for local development
- Vite proxy for API routing
- Environment variables via python-dotenv

### Security Considerations

1. **API Key**: ANTHROPIC_API_KEY stored in `.env` file (not committed)
2. **SQL Injection**: Parameterized queries used throughout
3. **Input Validation**: Pydantic models validate all inputs
4. **CORS**: Restricted to specific origins (localhost:5173, localhost:3000)
5. **Foreign Keys**: Enabled in SQLite for referential integrity

### Scalability Notes

**Current Limitations (Educational Demo):**
- SQLite database (single-file, not for high concurrency)
- No authentication/authorization
- Stateless chat (no conversation history)
- No caching layer
- Synchronous database operations

**Production Improvements:**
- Use PostgreSQL/MySQL for production database
- Add JWT authentication
- Implement conversation history storage
- Add Redis cache for frequently accessed data
- Use async database library (asyncpg, aiomysql)
- Add rate limiting and request throttling
- Implement proper logging and monitoring

---

## Conclusion

The Blackbird Customer Support Application demonstrates a well-structured full-stack architecture with clear separation of concerns:

1. **Frontend** handles presentation and user interaction
2. **Backend** provides RESTful API with validation
3. **Database layer** abstracts data persistence
4. **AI layer** integrates Claude for intelligent assistance
5. **Models** ensure type safety across the stack

The architecture is designed for educational purposes, showcasing Claude AI function calling integration while maintaining clean code principles and proper separation of concerns.
