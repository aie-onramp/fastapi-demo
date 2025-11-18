# API Reference

## Overview

The Blackbird Customer Support API is a FastAPI-based RESTful service that provides customer relationship management (CRM) and order management capabilities enhanced with Claude AI integration. The API enables support teams to query customer information, manage orders, and leverage AI-powered natural language interactions.

**Base URL:** `http://localhost:8000/api`

**Key Features:**
- RESTful endpoints for customers and orders
- AI-powered chat interface with tool calling
- SQLite database backend
- Comprehensive validation with Pydantic models
- CORS support for React frontend integration

---

## Table of Contents

- [REST API Endpoints](#rest-api-endpoints)
  - [Health Check](#health-check)
  - [Chat Endpoints](#chat-endpoints)
  - [Customer Endpoints](#customer-endpoints)
  - [Order Endpoints](#order-endpoints)
- [Data Models](#data-models)
  - [Customer Models](#customer-models)
  - [Order Models](#order-models)
  - [Chat Models](#chat-models)
  - [Combined Response Models](#combined-response-models)
- [Database Operations](#database-operations)
  - [Customer Operations](#customer-operations)
  - [Order Operations](#order-operations)
  - [Combined Operations](#combined-operations)
- [AI Tools](#ai-tools)
  - [Tool Definitions](#tool-definitions)
  - [Tool Execution](#tool-execution)
  - [Claude Integration](#claude-integration)
- [JavaScript/Frontend API Client](#javascriptfrontend-api-client)
- [Configuration](#configuration)
- [Usage Patterns](#usage-patterns)
- [Best Practices](#best-practices)
- [Error Handling](#error-handling)
- [Appendix](#appendix)

---

## REST API Endpoints

### Health Check

#### GET /api/health

**Description:** Returns API health status for monitoring and readiness checks.

**Source:** `backend/main.py` (lines 61-64)

**Parameters:** None

**Response:**
- **Type:** `application/json`
- **Schema:**
  ```json
  {
    "status": "string",
    "service": "string"
  }
  ```

**Example Request:**
```bash
curl http://localhost:8000/api/health
```

**Example Response:**
```json
{
  "status": "healthy",
  "service": "blackbird-api"
}
```

**Status Codes:**
- `200`: Service is healthy

---

### Chat Endpoints

#### POST /api/chat

**Description:** Send a message to Claude AI assistant for natural language customer support queries. The AI can automatically use six different tools to look up customers, view orders, cancel orders, and update contact information.

**Source:** `backend/main.py` (lines 71-94)

**Request Body:**
- **Type:** `ChatMessage`
- **Schema:**
  ```json
  {
    "message": "string (1-4000 chars, required)"
  }
  ```

**Response:**
- **Type:** `ChatResponse`
- **Schema:**
  ```json
  {
    "response": "string",
    "tool_calls": [
      {
        "tool": "string",
        "input": {}
      }
    ]
  }
  ```

**Example Request:**
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Look up customer with email john@example.com"}'
```

**Example Response:**
```json
{
  "response": "I found John Doe (ID: 1213210) with email john@example.com. They have 2 active orders.",
  "tool_calls": [
    {
      "tool": "get_user",
      "input": {
        "key": "email",
        "value": "john@example.com"
      }
    },
    {
      "tool": "get_customer_orders",
      "input": {
        "customer_id": "1213210"
      }
    }
  ]
}
```

**Example Messages:**
- `"Look up customer with email john@example.com"`
- `"Show me all orders for customer 1213210"`
- `"Cancel order 47652"`
- `"Update phone number to 555-123-4567 for customer 1213210"`

**Status Codes:**
- `200`: Success
- `500`: Internal server error or Claude API error

**Error Response:**
```json
{
  "detail": "Chat error: ANTHROPIC_API_KEY not found in environment variables"
}
```

**Usage Notes:**
- Requires `ANTHROPIC_API_KEY` environment variable
- Currently stateless (no conversation history maintained)
- Tool calls are logged in response for transparency

---

### Customer Endpoints

#### GET /api/customers

**Description:** Retrieve all customers in the system, sorted alphabetically by name.

**Source:** `backend/main.py` (lines 101-108)

**Parameters:** None

**Response:**
- **Type:** `List[Customer]`
- **Description:** Array of customer objects

**Example Request:**
```bash
curl http://localhost:8000/api/customers
```

**Example Response:**
```json
[
  {
    "id": "1213210",
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "123-456-7890",
    "username": "johndoe"
  },
  {
    "id": "1234567",
    "name": "Jane Smith",
    "email": "jane@example.com",
    "phone": "555-123-4567",
    "username": "janesmith"
  }
]
```

**Status Codes:**
- `200`: Success
- `500`: Database error

**Usage Notes:**
- Returns empty array `[]` if no customers exist
- Results are ordered by customer name

---

#### GET /api/customers/{customer_id}

**Description:** Retrieve a specific customer by their unique 7-digit ID.

**Source:** `backend/main.py` (lines 111-117)

**Path Parameters:**
- `customer_id` (string, required): 7-digit customer ID (e.g., "1213210")

**Response:**
- **Type:** `Customer`
- **Description:** Single customer object

**Example Request:**
```bash
curl http://localhost:8000/api/customers/1213210
```

**Example Response:**
```json
{
  "id": "1213210",
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "123-456-7890",
  "username": "johndoe"
}
```

**Status Codes:**
- `200`: Customer found
- `404`: Customer not found
- `500`: Database error

**Error Response:**
```json
{
  "detail": "Customer 1213210 not found"
}
```

---

#### POST /api/customers/search

**Description:** Search for a customer by email address, phone number, or username. Returns the first matching customer.

**Source:** `backend/main.py` (lines 120-142)

**Request Body:**
- **Type:** `CustomerSearch`
- **Schema:**
  ```json
  {
    "key": "email|phone|username",
    "value": "string"
  }
  ```

**Response:**
- **Type:** `Customer`
- **Description:** Matching customer object

**Example Request:**
```bash
curl -X POST http://localhost:8000/api/customers/search \
  -H "Content-Type: application/json" \
  -d '{"key": "email", "value": "john@example.com"}'
```

**Example Response:**
```json
{
  "id": "1213210",
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "123-456-7890",
  "username": "johndoe"
}
```

**Valid Search Keys:**
- `email`: Search by email address (exact match)
- `phone`: Search by phone number (exact match, format: XXX-XXX-XXXX)
- `username`: Search by username (exact match, case-sensitive)

**Status Codes:**
- `200`: Customer found
- `400`: Invalid search key
- `404`: No customer found matching criteria
- `500`: Database error

**Error Responses:**
```json
{
  "detail": "No customer found with email=notfound@example.com"
}
```

```json
{
  "detail": "Invalid search key: id. Must be one of ['email', 'phone', 'username']"
}
```

---

#### PATCH /api/customers/{customer_id}

**Description:** Update a customer's contact information (email and/or phone number). At least one field must be provided.

**Source:** `backend/main.py` (lines 145-177)

**Path Parameters:**
- `customer_id` (string, required): 7-digit customer ID

**Request Body:**
- **Type:** `CustomerUpdate`
- **Schema:**
  ```json
  {
    "email": "string (optional, valid email)",
    "phone": "string (optional, format: XXX-XXX-XXXX)"
  }
  ```

**Response:**
- **Type:** `Customer`
- **Description:** Updated customer object

**Example Request (Update Email):**
```bash
curl -X PATCH http://localhost:8000/api/customers/1213210 \
  -H "Content-Type: application/json" \
  -d '{"email": "newemail@example.com"}'
```

**Example Request (Update Both):**
```bash
curl -X PATCH http://localhost:8000/api/customers/1213210 \
  -H "Content-Type: application/json" \
  -d '{"email": "new@example.com", "phone": "555-999-8888"}'
```

**Example Response:**
```json
{
  "id": "1213210",
  "name": "John Doe",
  "email": "newemail@example.com",
  "phone": "123-456-7890",
  "username": "johndoe"
}
```

**Status Codes:**
- `200`: Update successful
- `400`: Validation error or no fields provided
- `404`: Customer not found
- `500`: Database error

**Error Responses:**
```json
{
  "detail": "Must provide at least one field to update"
}
```

**Validation Rules:**
- Email must be valid email format
- Phone must match pattern: `\d{3}-\d{3}-\d{4}`
- Cannot update `id`, `name`, or `username` (immutable)

---

#### GET /api/customers/{customer_id}/orders

**Description:** Retrieve a customer with all their associated orders in a single response.

**Source:** `backend/main.py` (lines 180-191)

**Path Parameters:**
- `customer_id` (string, required): 7-digit customer ID

**Response:**
- **Type:** `CustomerWithOrders`
- **Description:** Customer object with nested orders array

**Example Request:**
```bash
curl http://localhost:8000/api/customers/1213210/orders
```

**Example Response:**
```json
{
  "customer": {
    "id": "1213210",
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "123-456-7890",
    "username": "johndoe"
  },
  "orders": [
    {
      "id": "24601",
      "customer_id": "1213210",
      "product": "Wireless Headphones",
      "quantity": 1,
      "price": 79.99,
      "status": "Shipped"
    },
    {
      "id": "47652",
      "customer_id": "1213210",
      "product": "USB-C Cable",
      "quantity": 2,
      "price": 12.99,
      "status": "Processing"
    }
  ]
}
```

**Status Codes:**
- `200`: Success
- `404`: Customer not found
- `500`: Database error

**Usage Notes:**
- Orders array will be empty `[]` if customer has no orders
- Orders are sorted by order ID

---

### Order Endpoints

#### GET /api/orders

**Description:** Retrieve all orders in the system, optionally filtered by status.

**Source:** `backend/main.py` (lines 198-210)

**Query Parameters:**
- `status` (string, optional): Filter by order status
  - Valid values: `Processing`, `Shipped`, `Delivered`, `Cancelled`

**Response:**
- **Type:** `List[Order]`
- **Description:** Array of order objects

**Example Request (All Orders):**
```bash
curl http://localhost:8000/api/orders
```

**Example Request (Filter by Status):**
```bash
curl "http://localhost:8000/api/orders?status=Processing"
```

**Example Response:**
```json
[
  {
    "id": "24601",
    "customer_id": "1213210",
    "product": "Wireless Headphones",
    "quantity": 1,
    "price": 79.99,
    "status": "Processing"
  },
  {
    "id": "47652",
    "customer_id": "1234567",
    "product": "USB-C Cable",
    "quantity": 3,
    "price": 12.99,
    "status": "Processing"
  }
]
```

**Status Codes:**
- `200`: Success
- `500`: Database error

**Usage Notes:**
- Returns empty array `[]` if no orders match criteria
- Results are ordered by order ID
- Invalid status values are ignored (returns all orders)

---

#### GET /api/orders/{order_id}

**Description:** Retrieve a specific order by its unique 5-digit ID.

**Source:** `backend/main.py` (lines 213-219)

**Path Parameters:**
- `order_id` (string, required): 5-digit order ID (e.g., "24601")

**Response:**
- **Type:** `Order`
- **Description:** Single order object

**Example Request:**
```bash
curl http://localhost:8000/api/orders/24601
```

**Example Response:**
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

**Status Codes:**
- `200`: Order found
- `404`: Order not found
- `500`: Database error

**Error Response:**
```json
{
  "detail": "Order 24601 not found"
}
```

---

#### PATCH /api/orders/{order_id}/cancel

**Description:** Cancel an order. Only orders with status "Processing" can be cancelled. Orders that are already Shipped, Delivered, or Cancelled cannot be cancelled.

**Source:** `backend/main.py` (lines 222-239)

**Path Parameters:**
- `order_id` (string, required): 5-digit order ID

**Response:**
- **Type:** `OrderCancelResponse`
- **Schema:**
  ```json
  {
    "success": "boolean",
    "message": "string"
  }
  ```

**Example Request:**
```bash
curl -X PATCH http://localhost:8000/api/orders/24601/cancel
```

**Example Response (Success):**
```json
{
  "success": true,
  "message": "Order 24601 cancelled successfully"
}
```

**Example Response (Already Shipped):**
```json
{
  "success": false,
  "message": "Cannot cancel order 24601. Status is 'Shipped'. Only orders with status 'Processing' can be cancelled."
}
```

**Status Codes:**
- `200`: Cancellation successful
- `400`: Cannot cancel (wrong status or order not found)
- `500`: Database error

**Business Rules:**
- Only orders with `status = 'Processing'` can be cancelled
- Cancelled orders have status updated to `'Cancelled'`
- Cannot re-cancel an already cancelled order

---

## Data Models

All data models use Pydantic for validation and serialization. Models include comprehensive validation rules and JSON schema examples.

**Source:** `backend/models.py`

### Customer Models

#### Customer

**Description:** Core customer data model representing a customer with contact information.

**Source:** Lines 15-42

**Fields:**

| Field | Type | Required | Validation | Description |
|-------|------|----------|------------|-------------|
| `id` | `str` | Yes | Pattern: `^\d{7}$` | 7-digit customer ID |
| `name` | `str` | Yes | Min: 1, Max: 100 chars | Customer full name |
| `email` | `EmailStr` | Yes | Valid email format | Customer email address |
| `phone` | `str` | Yes | Pattern: `^\d{3}-\d{3}-\d{4}$` | Phone in XXX-XXX-XXXX format |
| `username` | `str` | Yes | Pattern: `^[a-zA-Z0-9_]+$`, Length: 3-20 | Alphanumeric username |

**Example:**
```python
from models import Customer

customer = Customer(
    id="1213210",
    name="John Doe",
    email="john@example.com",
    phone="123-456-7890",
    username="johndoe"
)
```

**Validation Rules:**
- `id`: Must be exactly 7 digits (e.g., "1213210")
- `name`: Cannot be empty, max 100 characters
- `email`: Must be valid email format (validated by Pydantic's `EmailStr`)
- `phone`: Must match format XXX-XXX-XXXX (e.g., "555-123-4567")
- `username`: 3-20 characters, alphanumeric plus underscore only

**JSON Schema Example:**
```json
{
  "id": "1213210",
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "123-456-7890",
  "username": "johndoe"
}
```

---

#### CustomerUpdate

**Description:** Model for updating customer contact information. At least one field must be provided.

**Source:** Lines 45-60

**Fields:**

| Field | Type | Required | Validation | Description |
|-------|------|----------|------------|-------------|
| `email` | `EmailStr` | No | Valid email format | New email address |
| `phone` | `str` | No | Pattern: `^\d{3}-\d{3}-\d{4}$` | New phone number |

**Example:**
```python
from models import CustomerUpdate

# Update email only
update = CustomerUpdate(email="newemail@example.com")

# Update phone only
update = CustomerUpdate(phone="555-999-8888")

# Update both
update = CustomerUpdate(
    email="new@example.com",
    phone="555-999-8888"
)
```

**Validation Rules:**
- At least one field (`email` or `phone`) must be provided
- If provided, `email` must be valid email format
- If provided, `phone` must match XXX-XXX-XXXX format

---

#### CustomerSearch

**Description:** Model for searching customers by specific fields.

**Source:** Lines 63-78

**Fields:**

| Field | Type | Required | Validation | Description |
|-------|------|----------|------------|-------------|
| `key` | `Literal` | Yes | One of: 'email', 'phone', 'username' | Field to search by |
| `value` | `str` | Yes | Min: 1 char | Value to search for |

**Example:**
```python
from models import CustomerSearch

# Search by email
search = CustomerSearch(key="email", value="john@example.com")

# Search by phone
search = CustomerSearch(key="phone", value="123-456-7890")

# Search by username
search = CustomerSearch(key="username", value="johndoe")
```

**Valid Keys:**
- `email`: Search by email address
- `phone`: Search by phone number
- `username`: Search by username

---

### Order Models

#### Order

**Description:** Order data model representing a product purchase transaction.

**Source:** Lines 85-111

**Fields:**

| Field | Type | Required | Validation | Description |
|-------|------|----------|------------|-------------|
| `id` | `str` | Yes | Pattern: `^\d{5}$` | 5-digit order ID |
| `customer_id` | `str` | Yes | Pattern: `^\d{7}$` | 7-digit customer ID (foreign key) |
| `product` | `str` | Yes | Min: 1, Max: 200 chars | Product name |
| `quantity` | `int` | Yes | Range: 1-999 | Quantity ordered |
| `price` | `float` | Yes | Range: 0-9999.99 | Price per unit |
| `status` | `Literal` | Yes | One of: 'Processing', 'Shipped', 'Delivered', 'Cancelled' | Order status |

**Example:**
```python
from models import Order

order = Order(
    id="24601",
    customer_id="1213210",
    product="Wireless Headphones",
    quantity=1,
    price=79.99,
    status="Processing"
)
```

**Validation Rules:**
- `id`: Must be exactly 5 digits (e.g., "24601")
- `customer_id`: Must be exactly 7 digits, references a valid customer
- `product`: Cannot be empty, max 200 characters
- `quantity`: Must be greater than 0, max 999
- `price`: Must be non-negative, less than 10000
- `status`: Must be one of the four valid statuses

**Status Values:**
- `Processing`: Order received, not yet shipped
- `Shipped`: Order has been shipped
- `Delivered`: Order delivered to customer
- `Cancelled`: Order cancelled (cannot be un-cancelled)

---

#### OrderCancelResponse

**Description:** Response model for order cancellation operations.

**Source:** Lines 114-127

**Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `success` | `bool` | Yes | Whether cancellation succeeded |
| `message` | `str` | Yes | Descriptive result message |

**Example:**
```python
from models import OrderCancelResponse

# Success case
response = OrderCancelResponse(
    success=True,
    message="Order 24601 cancelled successfully"
)

# Failure case
response = OrderCancelResponse(
    success=False,
    message="Cannot cancel order 24601. Status is 'Shipped'."
)
```

---

### Chat Models

#### ChatMessage

**Description:** Request model for sending messages to Claude AI.

**Source:** Lines 134-147

**Fields:**

| Field | Type | Required | Validation | Description |
|-------|------|----------|------------|-------------|
| `message` | `str` | Yes | Length: 1-4000 chars | User's chat message |

**Example:**
```python
from models import ChatMessage

message = ChatMessage(
    message="Look up customer with email john@example.com"
)
```

**Validation Rules:**
- Message cannot be empty
- Maximum 4000 characters
- No special formatting required (natural language)

---

#### ChatResponse

**Description:** Response model from Claude AI with optional tool call information.

**Source:** Lines 150-178

**Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `response` | `str` | Yes | AI assistant's response text |
| `tool_calls` | `List[Dict]` | No | List of tools called by AI (debugging/transparency) |

**Example:**
```python
from models import ChatResponse

response = ChatResponse(
    response="I found John Doe (ID: 1213210) with email john@example.com. They have 2 orders.",
    tool_calls=[
        {
            "tool": "get_user",
            "input": {"key": "email", "value": "john@example.com"}
        },
        {
            "tool": "get_customer_orders",
            "input": {"customer_id": "1213210"}
        }
    ]
)
```

**Tool Call Structure:**
```python
{
    "tool": "string",      # Name of tool called
    "input": {             # Parameters passed to tool
        "key": "value"
    }
}
```

---

### Combined Response Models

#### CustomerWithOrders

**Description:** Combined model containing customer information with all their orders.

**Source:** Lines 185-215

**Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `customer` | `Customer` | Yes | Customer object |
| `orders` | `List[Order]` | Yes | List of customer's orders (may be empty) |

**Example:**
```python
from models import CustomerWithOrders, Customer, Order

result = CustomerWithOrders(
    customer=Customer(
        id="1213210",
        name="John Doe",
        email="john@example.com",
        phone="123-456-7890",
        username="johndoe"
    ),
    orders=[
        Order(
            id="24601",
            customer_id="1213210",
            product="Wireless Headphones",
            quantity=1,
            price=79.99,
            status="Shipped"
        )
    ]
)
```

---

#### ErrorResponse

**Description:** Standard error response model for API errors.

**Source:** Lines 222-235

**Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `error` | `str` | Yes | Error message |
| `detail` | `str` | No | Additional error details |

**Example:**
```python
from models import ErrorResponse

error = ErrorResponse(
    error="Customer not found",
    detail="No customer exists with ID 9999999"
)
```

---

## Database Operations

All database operations use SQLite with context managers for automatic connection handling and transaction management.

**Source:** `backend/database.py`

**Database Path:** `blackbird.db` (configurable via `DATABASE_PATH` constant, line 12)

### Database Initialization

#### init_database()

**Description:** Initialize the database schema. Creates tables and indexes if they don't exist. Safe to call multiple times.

**Source:** Lines 52-68

**Signature:**
```python
def init_database() -> None
```

**Parameters:** None

**Returns:** None

**Side Effects:**
- Creates `customers` table if not exists
- Creates `orders` table if not exists
- Creates indexes for email, username, customer_id, and status
- Enables foreign key constraints

**Example:**
```python
from database import init_database

# Initialize database (called on app startup)
init_database()
# Output: ✓ Database schema initialized: blackbird.db
```

**Database Schema:**
```sql
-- Customers table
CREATE TABLE IF NOT EXISTS customers (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone TEXT NOT NULL,
    username TEXT NOT NULL UNIQUE,
    CHECK (length(name) >= 1),
    CHECK (email LIKE '%@%.%'),
    CHECK (length(phone) >= 10),
    CHECK (length(username) >= 3 AND length(username) <= 20)
);

-- Orders table
CREATE TABLE IF NOT EXISTS orders (
    id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL,
    product TEXT NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    price REAL NOT NULL CHECK (price >= 0),
    status TEXT NOT NULL CHECK (status IN ('Processing', 'Shipped', 'Delivered', 'Cancelled')),
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE
);
```

**Indexes:**
- `idx_customers_email` on `customers(email)`
- `idx_customers_username` on `customers(username)`
- `idx_orders_customer_id` on `orders(customer_id)`
- `idx_orders_status` on `orders(status)`

---

#### get_db()

**Description:** Context manager for database connections with automatic commit/rollback and connection cleanup.

**Source:** Lines 71-98

**Signature:**
```python
@contextmanager
def get_db() -> sqlite3.Connection
```

**Yields:**
- `sqlite3.Connection`: Database connection with `row_factory` set to `sqlite3.Row`

**Behavior:**
- Automatically commits on success
- Automatically rolls back on exception
- Automatically closes connection when context exits
- Enables column access by name via `row_factory`

**Example:**
```python
from database import get_db

# Recommended usage with context manager
with get_db() as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers")
    results = cursor.fetchall()
    # Connection automatically committed and closed

# Access columns by name
with get_db() as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email FROM customers WHERE id = ?", ("1213210",))
    row = cursor.fetchone()
    print(row['name'])   # Access by column name
    print(row['email'])  # row_factory enables this
```

**Error Handling:**
```python
try:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO customers ...")
        # If error occurs, transaction is rolled back
except Exception as e:
    print(f"Database error: {e}")
```

---

### Customer Operations

#### get_customer()

**Description:** Retrieve a customer by their unique ID.

**Source:** Lines 105-122

**Signature:**
```python
def get_customer(customer_id: str) -> Optional[Dict[str, Any]]
```

**Parameters:**
- `customer_id` (str): Customer ID (7-digit string)

**Returns:**
- `Optional[Dict[str, Any]]`: Customer data dictionary or `None` if not found

**Example:**
```python
from database import get_customer

# Found
customer = get_customer("1213210")
if customer:
    print(f"Found: {customer['name']}")
    print(f"Email: {customer['email']}")
    # Output:
    # Found: John Doe
    # Email: john@example.com

# Not found
customer = get_customer("9999999")
print(customer)  # None
```

**Return Structure:**
```python
{
    'id': '1213210',
    'name': 'John Doe',
    'email': 'john@example.com',
    'phone': '123-456-7890',
    'username': 'johndoe'
}
```

**Performance:** Uses primary key lookup (O(log n) with B-tree index)

---

#### search_customer()

**Description:** Search for a customer by email, phone, or username.

**Source:** Lines 125-148

**Signature:**
```python
def search_customer(key: str, value: str) -> Optional[Dict[str, Any]]
```

**Parameters:**
- `key` (str): Search field - must be one of `'email'`, `'phone'`, or `'username'`
- `value` (str): Search value

**Returns:**
- `Optional[Dict[str, Any]]`: Customer data dictionary or `None` if not found

**Raises:**
- `ValueError`: If `key` is not a valid search field

**Example:**
```python
from database import search_customer

# Search by email
customer = search_customer("email", "john@example.com")

# Search by phone
customer = search_customer("phone", "123-456-7890")

# Search by username
customer = search_customer("username", "johndoe")

# Invalid key
try:
    customer = search_customer("id", "1213210")
except ValueError as e:
    print(e)
    # Output: Invalid search key: id. Must be one of ['email', 'phone', 'username']
```

**Performance:**
- Email and username searches use indexes (fast)
- Phone searches are sequential (slower on large datasets)

**Security Note:** Uses parameterized queries to prevent SQL injection

---

#### get_all_customers()

**Description:** Retrieve all customers in the system, ordered by name.

**Source:** Lines 151-162

**Signature:**
```python
def get_all_customers() -> List[Dict[str, Any]]
```

**Parameters:** None

**Returns:**
- `List[Dict[str, Any]]`: List of customer dictionaries (may be empty)

**Example:**
```python
from database import get_all_customers

customers = get_all_customers()
print(f"Total customers: {len(customers)}")

for customer in customers:
    print(f"{customer['id']}: {customer['name']} ({customer['email']})")

# Output:
# Total customers: 5
# 1213210: John Doe (john@example.com)
# 1234567: Jane Smith (jane@example.com)
# ...
```

**Performance:** Full table scan, ordered by name. Consider pagination for large datasets.

---

#### update_customer()

**Description:** Update a customer's contact information (email and/or phone).

**Source:** Lines 165-201

**Signature:**
```python
def update_customer(
    customer_id: str,
    email: Optional[str] = None,
    phone: Optional[str] = None
) -> bool
```

**Parameters:**
- `customer_id` (str): Customer ID to update
- `email` (Optional[str]): New email address (optional)
- `phone` (Optional[str]): New phone number (optional)

**Returns:**
- `bool`: `True` if update successful, `False` if customer not found

**Raises:**
- `ValueError`: If neither email nor phone provided

**Example:**
```python
from database import update_customer

# Update email only
success = update_customer("1213210", email="newemail@example.com")

# Update phone only
success = update_customer("1213210", phone="555-999-8888")

# Update both
success = update_customer(
    "1213210",
    email="new@example.com",
    phone="555-999-8888"
)

if success:
    print("Update successful")
else:
    print("Customer not found")

# Error: no fields provided
try:
    update_customer("1213210")
except ValueError as e:
    print(e)
    # Output: Must provide at least one field to update
```

**Notes:**
- Uses parameterized queries for security
- Automatically builds SQL based on provided parameters
- Does not validate email/phone format (handled by Pydantic models at API layer)

---

### Order Operations

#### get_order()

**Description:** Retrieve an order by its unique ID.

**Source:** Lines 208-225

**Signature:**
```python
def get_order(order_id: str) -> Optional[Dict[str, Any]]
```

**Parameters:**
- `order_id` (str): Order ID (5-digit string)

**Returns:**
- `Optional[Dict[str, Any]]`: Order data dictionary or `None` if not found

**Example:**
```python
from database import get_order

order = get_order("24601")
if order:
    print(f"Order {order['id']}: {order['product']}")
    print(f"Status: {order['status']}")
    print(f"Price: ${order['price']}")
    # Output:
    # Order 24601: Wireless Headphones
    # Status: Processing
    # Price: $79.99
else:
    print("Order not found")
```

**Return Structure:**
```python
{
    'id': '24601',
    'customer_id': '1213210',
    'product': 'Wireless Headphones',
    'quantity': 1,
    'price': 79.99,
    'status': 'Processing'
}
```

---

#### get_customer_orders()

**Description:** Retrieve all orders for a specific customer.

**Source:** Lines 228-245

**Signature:**
```python
def get_customer_orders(customer_id: str) -> List[Dict[str, Any]]
```

**Parameters:**
- `customer_id` (str): Customer ID (7-digit string)

**Returns:**
- `List[Dict[str, Any]]`: List of order dictionaries (may be empty)

**Example:**
```python
from database import get_customer_orders

orders = get_customer_orders("1213210")
print(f"Customer has {len(orders)} orders")

for order in orders:
    print(f"Order {order['id']}: {order['product']} - {order['status']}")

# Output:
# Customer has 2 orders
# Order 24601: Wireless Headphones - Shipped
# Order 47652: USB-C Cable - Processing
```

**Performance:** Uses index on `customer_id` for fast lookups

**Notes:**
- Returns empty list `[]` if customer has no orders
- Does not verify customer exists (returns empty list for invalid customer_id)
- Orders sorted by order ID

---

#### get_all_orders()

**Description:** Retrieve all orders, optionally filtered by status.

**Source:** Lines 248-271

**Signature:**
```python
def get_all_orders(status: Optional[str] = None) -> List[Dict[str, Any]]
```

**Parameters:**
- `status` (Optional[str]): Filter by status ('Processing', 'Shipped', 'Delivered', 'Cancelled'). If `None`, returns all orders.

**Returns:**
- `List[Dict[str, Any]]`: List of order dictionaries

**Example:**
```python
from database import get_all_orders

# Get all orders
all_orders = get_all_orders()
print(f"Total orders: {len(all_orders)}")

# Get only processing orders
processing = get_all_orders(status="Processing")
print(f"Processing orders: {len(processing)}")

# Get shipped orders
shipped = get_all_orders(status="Shipped")

# Get cancelled orders
cancelled = get_all_orders(status="Cancelled")
```

**Performance:**
- Filtered queries use status index (fast)
- Unfiltered queries scan full table

**Valid Status Values:**
- `"Processing"`
- `"Shipped"`
- `"Delivered"`
- `"Cancelled"`

---

#### cancel_order()

**Description:** Cancel an order (only if status is 'Processing'). Implements business rule that orders can only be cancelled before shipping.

**Source:** Lines 274-310

**Signature:**
```python
def cancel_order(order_id: str) -> Dict[str, Any]
```

**Parameters:**
- `order_id` (str): Order ID to cancel

**Returns:**
- `Dict[str, Any]`: Result dictionary with `success` (bool) and `message` (str)

**Return Structure:**
```python
{
    'success': True,           # or False
    'message': 'string'        # Description of result
}
```

**Example:**
```python
from database import cancel_order

# Success case
result = cancel_order("24601")
print(result)
# Output: {'success': True, 'message': 'Order 24601 cancelled successfully'}

# Already shipped
result = cancel_order("99999")
print(result)
# Output: {
#     'success': False,
#     'message': "Cannot cancel order 99999. Status is 'Shipped'. Only orders with status 'Processing' can be cancelled."
# }

# Not found
result = cancel_order("00000")
print(result)
# Output: {'success': False, 'message': 'Order 00000 not found'}
```

**Business Rules:**
1. Order must exist
2. Order status must be exactly `'Processing'`
3. Cannot cancel orders with status: `'Shipped'`, `'Delivered'`, or `'Cancelled'`
4. Cancelled orders have status updated to `'Cancelled'`

**Usage in API:**
```python
# API endpoint uses this to return appropriate HTTP status
result = cancel_order(order_id)
if not result["success"]:
    raise HTTPException(status_code=400, detail=result["message"])
```

---

### Combined Operations

#### get_customer_with_orders()

**Description:** Retrieve customer information with all their orders in a single operation.

**Source:** Lines 317-337

**Signature:**
```python
def get_customer_with_orders(customer_id: str) -> Optional[Dict[str, Any]]
```

**Parameters:**
- `customer_id` (str): Customer ID (7-digit string)

**Returns:**
- `Optional[Dict[str, Any]]`: Dictionary with `customer` and `orders` keys, or `None` if customer not found

**Return Structure:**
```python
{
    'customer': {
        'id': '1213210',
        'name': 'John Doe',
        'email': 'john@example.com',
        'phone': '123-456-7890',
        'username': 'johndoe'
    },
    'orders': [
        {
            'id': '24601',
            'customer_id': '1213210',
            'product': 'Wireless Headphones',
            'quantity': 1,
            'price': 79.99,
            'status': 'Shipped'
        }
    ]
}
```

**Example:**
```python
from database import get_customer_with_orders

result = get_customer_with_orders("1213210")
if result:
    customer = result['customer']
    orders = result['orders']

    print(f"Customer: {customer['name']}")
    print(f"Orders: {len(orders)}")

    for order in orders:
        print(f"  - {order['product']}: {order['status']}")
else:
    print("Customer not found")

# Output:
# Customer: John Doe
# Orders: 2
#   - Wireless Headphones: Shipped
#   - USB-C Cable: Processing
```

**Performance:** Makes 2 database queries (one for customer, one for orders)

**Notes:**
- Returns `None` if customer not found
- `orders` list will be empty if customer has no orders
- Useful for comprehensive customer view in single API call

---

## AI Tools

The AI tools system enables Claude AI to interact with the database through structured function calling. This implementation demonstrates best practices for AI tool integration.

**Source:** `backend/ai_tools.py`

### Tool Definitions

Six tools are available to Claude AI, defined using JSON Schema format compatible with the Anthropic API.

**Source:** Lines 26-129

#### Tool 1: get_user

**Description:** Search for a customer by email, phone number, or username.

**Schema:**
```json
{
  "name": "get_user",
  "description": "Search for a customer by email, phone number, or username. Returns customer information if found.",
  "input_schema": {
    "type": "object",
    "properties": {
      "key": {
        "type": "string",
        "enum": ["email", "phone", "username"],
        "description": "The field to search by (email, phone, or username)"
      },
      "value": {
        "type": "string",
        "description": "The value to search for"
      }
    },
    "required": ["key", "value"]
  }
}
```

**Example Tool Call:**
```json
{
  "key": "email",
  "value": "john@example.com"
}
```

**Response:**
```json
{
  "success": true,
  "customer": {
    "id": "1213210",
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "123-456-7890",
    "username": "johndoe"
  }
}
```

---

#### Tool 2: get_order_by_id

**Description:** Look up a specific order by its order ID.

**Schema:**
```json
{
  "name": "get_order_by_id",
  "description": "Look up a specific order by its order ID. Returns order details including product, quantity, price, and status.",
  "input_schema": {
    "type": "object",
    "properties": {
      "order_id": {
        "type": "string",
        "description": "The 5-digit order ID"
      }
    },
    "required": ["order_id"]
  }
}
```

**Example Tool Call:**
```json
{
  "order_id": "24601"
}
```

**Response:**
```json
{
  "success": true,
  "order": {
    "id": "24601",
    "customer_id": "1213210",
    "product": "Wireless Headphones",
    "quantity": 1,
    "price": 79.99,
    "status": "Processing"
  }
}
```

---

#### Tool 3: get_customer_orders

**Description:** Get all orders for a specific customer by their customer ID.

**Schema:**
```json
{
  "name": "get_customer_orders",
  "description": "Get all orders for a specific customer by their customer ID. Returns a list of all orders.",
  "input_schema": {
    "type": "object",
    "properties": {
      "customer_id": {
        "type": "string",
        "description": "The 7-digit customer ID"
      }
    },
    "required": ["customer_id"]
  }
}
```

**Example Tool Call:**
```json
{
  "customer_id": "1213210"
}
```

**Response:**
```json
{
  "success": true,
  "orders": [
    {
      "id": "24601",
      "customer_id": "1213210",
      "product": "Wireless Headphones",
      "quantity": 1,
      "price": 79.99,
      "status": "Shipped"
    }
  ],
  "count": 1
}
```

---

#### Tool 4: cancel_order

**Description:** Cancel an order (only if status is 'Processing').

**Schema:**
```json
{
  "name": "cancel_order",
  "description": "Cancel an order. Only orders with status 'Processing' can be cancelled. Returns success/failure message.",
  "input_schema": {
    "type": "object",
    "properties": {
      "order_id": {
        "type": "string",
        "description": "The 5-digit order ID to cancel"
      }
    },
    "required": ["order_id"]
  }
}
```

**Example Tool Call:**
```json
{
  "order_id": "24601"
}
```

**Response (Success):**
```json
{
  "success": true,
  "message": "Order 24601 cancelled successfully"
}
```

**Response (Failure):**
```json
{
  "success": false,
  "message": "Cannot cancel order 24601. Status is 'Shipped'. Only orders with status 'Processing' can be cancelled."
}
```

---

#### Tool 5: update_user_contact

**Description:** Update a customer's contact information (email and/or phone number).

**Schema:**
```json
{
  "name": "update_user_contact",
  "description": "Update a customer's contact information (email and/or phone number).",
  "input_schema": {
    "type": "object",
    "properties": {
      "customer_id": {
        "type": "string",
        "description": "The 7-digit customer ID"
      },
      "email": {
        "type": "string",
        "description": "New email address (optional)"
      },
      "phone": {
        "type": "string",
        "description": "New phone number in XXX-XXX-XXXX format (optional)"
      }
    },
    "required": ["customer_id"]
  }
}
```

**Example Tool Call:**
```json
{
  "customer_id": "1213210",
  "email": "newemail@example.com"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Updated contact info for customer 1213210"
}
```

---

#### Tool 6: get_user_info

**Description:** Get complete customer information including all their orders.

**Schema:**
```json
{
  "name": "get_user_info",
  "description": "Get complete customer information including all their orders. Combines customer details with order history.",
  "input_schema": {
    "type": "object",
    "properties": {
      "key": {
        "type": "string",
        "enum": ["email", "phone", "username", "customer_id"],
        "description": "The field to search by"
      },
      "value": {
        "type": "string",
        "description": "The value to search for"
      }
    },
    "required": ["key", "value"]
  }
}
```

**Example Tool Call:**
```json
{
  "key": "email",
  "value": "john@example.com"
}
```

**Response:**
```json
{
  "success": true,
  "customer": {
    "id": "1213210",
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "123-456-7890",
    "username": "johndoe"
  },
  "orders": [
    {
      "id": "24601",
      "customer_id": "1213210",
      "product": "Wireless Headphones",
      "quantity": 1,
      "price": 79.99,
      "status": "Shipped"
    }
  ],
  "order_count": 1
}
```

---

### Tool Execution

#### execute_tool()

**Description:** Execute a tool and return the result. This function is called by the Claude integration when the AI decides to use a tool.

**Source:** Lines 136-217

**Signature:**
```python
def execute_tool(tool_name: str, tool_input: Dict[str, Any]) -> Dict[str, Any]
```

**Parameters:**
- `tool_name` (str): Name of the tool to execute
- `tool_input` (Dict[str, Any]): Tool parameters as a dictionary

**Returns:**
- `Dict[str, Any]`: Tool execution result with success status and data

**Raises:**
- `ValueError`: If `tool_name` is not recognized

**Example:**
```python
from ai_tools import execute_tool

# Execute get_user tool
result = execute_tool("get_user", {
    "key": "email",
    "value": "john@example.com"
})
print(result)
# Output: {'success': True, 'customer': {...}}

# Execute cancel_order tool
result = execute_tool("cancel_order", {
    "order_id": "24601"
})
print(result)
# Output: {'success': True, 'message': 'Order 24601 cancelled successfully'}

# Unknown tool
try:
    result = execute_tool("unknown_tool", {})
except ValueError as e:
    print(e)
    # Output: Unknown tool: unknown_tool
```

**Implementation Details:**

The function uses a series of if-elif statements to route to the appropriate database function:

1. **get_user**: Calls `db.search_customer()`
2. **get_order_by_id**: Calls `db.get_order()`
3. **get_customer_orders**: Calls `db.get_customer_orders()`
4. **cancel_order**: Calls `db.cancel_order()`
5. **update_user_contact**: Calls `db.update_customer()`
6. **get_user_info**: Calls `db.get_customer()` or `db.search_customer()`, then `db.get_customer_orders()`

**Error Handling:**
```python
# Tools return structured error responses
result = execute_tool("get_user", {
    "key": "email",
    "value": "notfound@example.com"
})
print(result)
# Output: {'success': False, 'message': 'No customer found with email=notfound@example.com'}
```

---

### Claude Integration

#### chat_with_claude()

**Description:** Send a message to Claude with tool calling enabled. Implements the full multi-turn conversation flow with tool execution.

**Source:** Lines 224-333

**Signature:**
```python
def chat_with_claude(
    message: str,
    conversation_history: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]
```

**Parameters:**
- `message` (str): User's message
- `conversation_history` (Optional[List[Dict[str, Any]]]): Previous messages in conversation

**Returns:**
- `Dict[str, Any]`: Dictionary with `response` (str) and `tool_calls` (List)

**Example:**
```python
from ai_tools import chat_with_claude

# Simple query
result = chat_with_claude("Look up customer with email john@example.com")
print(result['response'])
# Output: "I found John Doe (ID: 1213210) with email john@example.com..."

print(result['tool_calls'])
# Output: [{'tool': 'get_user', 'input': {'key': 'email', 'value': 'john@example.com'}}]

# Action request
result = chat_with_claude("Cancel order 24601")
print(result['response'])
# Output: "I've cancelled order 24601 successfully."
```

**Conversation Flow:**

1. **Initial Request**: Send user message to Claude with available tools
2. **Tool Decision**: Claude decides if tools are needed
3. **Tool Execution**: If tools requested, execute them and get results
4. **Tool Results**: Send results back to Claude
5. **Final Response**: Claude generates response incorporating tool results

**Flow Diagram:**
```
User Message
    ↓
Claude API (with tools)
    ↓
Tool Use? ───No──→ Return Response
    ↓ Yes
Execute Tools
    ↓
Send Results to Claude
    ↓
Claude API (with tools)
    ↓
Tool Use? ───Yes──→ [Loop back to Execute Tools]
    ↓ No
Return Final Response
```

**Implementation Details:**

```python
# Step 1: Initial message with tools
response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=1024,
    tools=TOOLS,
    messages=messages
)

# Step 2: Check for tool use
while response.stop_reason == "tool_use":
    # Extract and execute tools
    tool_use_blocks = [block for block in response.content if block.type == "tool_use"]

    for tool_use in tool_use_blocks:
        result = execute_tool(tool_use.name, tool_use.input)
        tool_results.append({
            "type": "tool_result",
            "tool_use_id": tool_use.id,
            "content": json.dumps(result)
        })

    # Step 3: Send results back
    messages.append({"role": "assistant", "content": response.content})
    messages.append({"role": "user", "content": tool_results})

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        tools=TOOLS,
        messages=messages
    )
```

**Configuration:**
- **Model**: `claude-haiku-4-5-20251001` (Claude 3.5 Haiku)
- **Max Tokens**: 1024
- **API Key**: Read from `ANTHROPIC_API_KEY` environment variable

**Error Handling:**
```python
# Missing API key
result = chat_with_claude("test message")
# Returns: {
#     'response': 'Error: ANTHROPIC_API_KEY not found in environment variables...',
#     'tool_calls': []
# }

# API error
result = chat_with_claude("test")
# Returns: {
#     'response': 'Error communicating with Claude AI: <error message>',
#     'tool_calls': [...]  # Any tools called before error
# }
```

---

#### process_chat_message()

**Description:** Simplified wrapper for stateless chat. Convenience function for single-message processing without conversation history.

**Source:** Lines 340-353

**Signature:**
```python
def process_chat_message(message: str) -> Dict[str, Any]
```

**Parameters:**
- `message` (str): User's message

**Returns:**
- `Dict[str, Any]`: Dictionary with `response` and `tool_calls`

**Example:**
```python
from ai_tools import process_chat_message

# Used by API endpoint
result = process_chat_message("Show me customer C001")
return ChatResponse(
    response=result["response"],
    tool_calls=result.get("tool_calls")
)
```

**Note:** This is a thin wrapper around `chat_with_claude()` with `conversation_history=None`. In production, you would maintain conversation history per user session.

---

## JavaScript/Frontend API Client

The frontend provides a JavaScript API client for interacting with the backend from React components.

**Source:** `frontend/src/api.js`

**Base URL:** `/api` (proxied to `http://localhost:8000/api` by Vite)

### Chat Functions

#### sendChatMessage()

**Description:** Send a chat message to Claude AI.

**Source:** Lines 15-30

**Signature:**
```javascript
async function sendChatMessage(message: string): Promise<Object>
```

**Parameters:**
- `message` (string): User's message

**Returns:**
- `Promise<Object>`: Response with `{response, tool_calls}`

**Throws:**
- `Error`: If request fails or server returns error

**Example:**
```javascript
import { sendChatMessage } from './api';

try {
  const result = await sendChatMessage("Look up customer john@example.com");
  console.log(result.response);
  console.log(result.tool_calls);
} catch (error) {
  console.error("Chat error:", error.message);
}
```

**Usage in React:**
```javascript
const [response, setResponse] = useState('');

const handleSend = async () => {
  try {
    const result = await sendChatMessage(userMessage);
    setResponse(result.response);
  } catch (error) {
    alert(`Error: ${error.message}`);
  }
};
```

---

### Customer Functions

#### fetchCustomers()

**Description:** Get all customers.

**Source:** Lines 37-45

**Signature:**
```javascript
async function fetchCustomers(): Promise<Array>
```

**Returns:**
- `Promise<Array>`: List of customer objects

**Example:**
```javascript
import { fetchCustomers } from './api';

const customers = await fetchCustomers();
console.log(`Found ${customers.length} customers`);
```

---

#### searchCustomer()

**Description:** Search for a customer by email, phone, or username.

**Source:** Lines 54-69

**Signature:**
```javascript
async function searchCustomer(key: string, value: string): Promise<Object>
```

**Parameters:**
- `key` (string): Search field ('email', 'phone', or 'username')
- `value` (string): Search value

**Returns:**
- `Promise<Object>`: Customer object

**Example:**
```javascript
import { searchCustomer } from './api';

try {
  const customer = await searchCustomer('email', 'john@example.com');
  console.log(`Found: ${customer.name}`);
} catch (error) {
  console.error("Not found:", error.message);
}
```

---

#### updateCustomer()

**Description:** Update customer contact information.

**Source:** Lines 78-93

**Signature:**
```javascript
async function updateCustomer(
  customerId: string,
  updates: Object
): Promise<Object>
```

**Parameters:**
- `customerId` (string): Customer ID
- `updates` (Object): Updates object with `{email?, phone?}`

**Returns:**
- `Promise<Object>`: Updated customer object

**Example:**
```javascript
import { updateCustomer } from './api';

const updated = await updateCustomer('1213210', {
  email: 'newemail@example.com',
  phone: '555-999-8888'
});
console.log("Updated:", updated);
```

---

### Order Functions

#### fetchOrders()

**Description:** Get all orders, optionally filtered by status.

**Source:** Lines 101-113

**Signature:**
```javascript
async function fetchOrders(status?: string): Promise<Array>
```

**Parameters:**
- `status` (string, optional): Filter by status

**Returns:**
- `Promise<Array>`: List of order objects

**Example:**
```javascript
import { fetchOrders } from './api';

// All orders
const allOrders = await fetchOrders();

// Only processing orders
const processing = await fetchOrders('Processing');
```

---

#### cancelOrder()

**Description:** Cancel an order.

**Source:** Lines 121-132

**Signature:**
```javascript
async function cancelOrder(orderId: string): Promise<Object>
```

**Parameters:**
- `orderId` (string): Order ID

**Returns:**
- `Promise<Object>`: Cancellation result `{success, message}`

**Example:**
```javascript
import { cancelOrder } from './api';

try {
  const result = await cancelOrder('24601');
  if (result.success) {
    alert(result.message);
  }
} catch (error) {
  alert(`Cannot cancel: ${error.message}`);
}
```

---

## Configuration

### Environment Variables

**Location:** `.env` file in project root

**Required Variables:**

| Variable | Type | Required | Description | Example |
|----------|------|----------|-------------|---------|
| `ANTHROPIC_API_KEY` | string | Yes | Anthropic API key for Claude AI | `sk-ant-...` |

**Example `.env` file:**
```bash
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
```

**Loading:** Environment variables are loaded in `backend/main.py` (lines 30-35):

```python
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)
```

---

### Application Settings

#### Database Configuration

**Source:** `backend/database.py` (line 12)

```python
DATABASE_PATH = "blackbird.db"
```

**Description:** Path to SQLite database file (relative to project root)

**Customization:**
```python
# To use a different path:
DATABASE_PATH = "/path/to/custom/database.db"
```

---

#### CORS Configuration

**Source:** `backend/main.py` (lines 44-54)

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

**Description:** Configure Cross-Origin Resource Sharing for frontend access

**Customization:**
```python
# Production configuration
allow_origins=[
    "https://yourdomain.com",
    "https://www.yourdomain.com"
]
```

---

#### AI Configuration

**Source:** `backend/ai_tools.py` (lines 268-272)

```python
response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=1024,
    tools=TOOLS,
    messages=messages
)
```

**Configuration Options:**

| Setting | Current Value | Description | Customization |
|---------|---------------|-------------|---------------|
| `model` | `claude-haiku-4-5-20251001` | Claude model version | Use `claude-sonnet-4-5-20250929` for more capable model |
| `max_tokens` | `1024` | Maximum response length | Increase to 4096 for longer responses |
| `tools` | `TOOLS` | Available tools | Modify `TOOLS` array to add/remove tools |

---

#### FastAPI Configuration

**Source:** `backend/main.py` (lines 38-42)

```python
app = FastAPI(
    title="Blackbird Customer Support API",
    description="FastAPI backend with Claude AI integration for customer support",
    version="0.1.0"
)
```

**Configuration:**
- **Title**: Appears in API documentation
- **Description**: Shows in Swagger UI
- **Version**: API version number

---

## Usage Patterns

### Basic CRUD Operations

#### Creating and Retrieving Customers

```python
from database import get_customer, get_all_customers

# Retrieve single customer
customer = get_customer("1213210")
if customer:
    print(f"Found: {customer['name']}")

# Retrieve all customers
all_customers = get_all_customers()
for c in all_customers:
    print(f"{c['id']}: {c['name']}")
```

#### Searching Customers

```python
from database import search_customer

# Search by email
customer = search_customer("email", "john@example.com")

# Search by phone
customer = search_customer("phone", "123-456-7890")

# Search by username
customer = search_customer("username", "johndoe")
```

#### Updating Customer Information

```python
from database import update_customer, get_customer

# Update email
success = update_customer("1213210", email="new@example.com")

# Update phone
success = update_customer("1213210", phone="555-999-8888")

# Update both
success = update_customer(
    "1213210",
    email="new@example.com",
    phone="555-999-8888"
)

# Verify update
if success:
    updated = get_customer("1213210")
    print(f"New email: {updated['email']}")
```

---

### Working with Orders

#### Querying Orders

```python
from database import get_order, get_customer_orders, get_all_orders

# Get specific order
order = get_order("24601")

# Get all orders for a customer
customer_orders = get_customer_orders("1213210")
print(f"Customer has {len(customer_orders)} orders")

# Get all processing orders
processing_orders = get_all_orders(status="Processing")

# Get all orders
all_orders = get_all_orders()
```

#### Cancelling Orders

```python
from database import cancel_order

# Cancel order
result = cancel_order("24601")

if result["success"]:
    print(result["message"])
    # Output: "Order 24601 cancelled successfully"
else:
    print(f"Cannot cancel: {result['message']}")
    # Output: "Cannot cancel order 24601. Status is 'Shipped'..."
```

---

### AI Chat Integration

#### Basic Chat Usage

```python
from ai_tools import process_chat_message

# Customer lookup
result = process_chat_message("Look up customer with email john@example.com")
print(result['response'])

# Order query
result = process_chat_message("Show me all orders for customer 1213210")
print(result['response'])

# Order cancellation
result = process_chat_message("Cancel order 24601")
print(result['response'])

# Update contact info
result = process_chat_message(
    "Update phone number to 555-999-8888 for customer 1213210"
)
print(result['response'])
```

#### With Tool Call Tracking

```python
from ai_tools import process_chat_message

result = process_chat_message("What orders does john@example.com have?")

print("AI Response:", result['response'])
print("\nTools Used:")
for tool_call in result['tool_calls']:
    print(f"  - {tool_call['tool']}: {tool_call['input']}")

# Output:
# AI Response: John Doe has 2 orders: Order 24601 (Wireless Headphones - Shipped) and Order 47652 (USB-C Cable - Processing).
#
# Tools Used:
#   - get_user: {'key': 'email', 'value': 'john@example.com'}
#   - get_customer_orders: {'customer_id': '1213210'}
```

---

### Frontend Integration

#### React Component Example

```javascript
import { useState } from 'react';
import { sendChatMessage, fetchCustomers, cancelOrder } from './api';

function CustomerSupportDashboard() {
  const [customers, setCustomers] = useState([]);
  const [chatResponse, setChatResponse] = useState('');

  // Load customers on mount
  useEffect(() => {
    const loadCustomers = async () => {
      try {
        const data = await fetchCustomers();
        setCustomers(data);
      } catch (error) {
        console.error('Failed to load customers:', error);
      }
    };
    loadCustomers();
  }, []);

  // Send chat message
  const handleChat = async (message) => {
    try {
      const result = await sendChatMessage(message);
      setChatResponse(result.response);
    } catch (error) {
      alert(`Chat error: ${error.message}`);
    }
  };

  // Cancel order
  const handleCancelOrder = async (orderId) => {
    try {
      const result = await cancelOrder(orderId);
      alert(result.message);
    } catch (error) {
      alert(`Cancel failed: ${error.message}`);
    }
  };

  return (
    <div>
      {/* UI components */}
    </div>
  );
}
```

---

### Combined Operations

#### Get Customer with Orders

```python
from database import get_customer_with_orders

# Single query for customer + orders
result = get_customer_with_orders("1213210")

if result:
    print(f"Customer: {result['customer']['name']}")
    print(f"Email: {result['customer']['email']}")
    print(f"\nOrders ({len(result['orders'])}):")

    for order in result['orders']:
        print(f"  {order['id']}: {order['product']} - ${order['price']:.2f} [{order['status']}]")
else:
    print("Customer not found")
```

---

## Best Practices

### Error Handling

#### API Level

```python
from fastapi import HTTPException
from database import get_customer

@app.get("/api/customers/{customer_id}")
def get_customer_endpoint(customer_id: str):
    try:
        customer = get_customer(customer_id)
        if not customer:
            raise HTTPException(
                status_code=404,
                detail=f"Customer {customer_id} not found"
            )
        return customer
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

#### Database Level

```python
from database import get_db

try:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM customers WHERE id = ?", (customer_id,))
        # Transaction automatically rolled back on error
except sqlite3.IntegrityError as e:
    print(f"Database constraint violation: {e}")
except sqlite3.OperationalError as e:
    print(f"Database operation error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

#### Frontend Level

```javascript
try {
  const customer = await fetchCustomers();
  setCustomers(customer);
} catch (error) {
  // Show user-friendly error
  setError(`Failed to load customers: ${error.message}`);
  // Log detailed error for debugging
  console.error('API Error:', error);
}
```

---

### Data Validation

#### Use Pydantic Models

```python
from fastapi import FastAPI, HTTPException
from models import Customer, CustomerUpdate

@app.patch("/api/customers/{customer_id}")
def update_customer(customer_id: str, update: CustomerUpdate):
    # Pydantic automatically validates:
    # - Email format
    # - Phone format
    # - At least one field provided

    try:
        # Validation passed, proceed with update
        success = db.update_customer(
            customer_id,
            email=update.email,
            phone=update.phone
        )
        # ...
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors())
```

#### Validate Before Database Operations

```python
from models import Customer

# Let Pydantic validate before DB insert
try:
    customer = Customer(
        id="1213210",
        name="John Doe",
        email="invalid-email",  # Invalid!
        phone="123-456-7890",
        username="johndoe"
    )
except ValidationError as e:
    print("Validation errors:", e.errors())
```

---

### Performance

#### Use Indexes

```sql
-- Indexes are created automatically by init_database()
CREATE INDEX idx_customers_email ON customers(email);
CREATE INDEX idx_customers_username ON customers(username);
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_orders_status ON orders(status);
```

**Query Performance:**
- Customer ID lookup: O(log n) - primary key
- Email/username search: O(log n) - indexed
- Phone search: O(n) - not indexed
- Order status filter: O(log n) - indexed

#### Connection Management

```python
# GOOD: Use context manager
with get_db() as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers")
    results = cursor.fetchall()
# Connection automatically closed

# BAD: Manual connection management
conn = sqlite3.connect(DATABASE_PATH)
cursor = conn.cursor()
cursor.execute("SELECT * FROM customers")
results = cursor.fetchall()
# Might forget to close!
```

#### Batch Operations

```python
# GOOD: Batch insert
with get_db() as conn:
    cursor = conn.cursor()
    cursor.executemany(
        "INSERT INTO customers VALUES (?, ?, ?, ?, ?)",
        customers_list
    )

# BAD: Individual inserts
for customer in customers_list:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO customers VALUES (?, ?, ?, ?, ?)", customer)
```

---

### Security

#### SQL Injection Prevention

```python
# GOOD: Parameterized queries
cursor.execute(
    "SELECT * FROM customers WHERE email = ?",
    (email,)
)

# BAD: String concatenation
cursor.execute(
    f"SELECT * FROM customers WHERE email = '{email}'"
)
```

#### Input Validation

```python
from models import CustomerSearch

# GOOD: Validate search key
search = CustomerSearch(key="email", value="john@example.com")
# Pydantic ensures key is one of: email, phone, username

# BAD: Trust user input
key = request.json.get('key')
query = f"SELECT * FROM customers WHERE {key} = ?"  # SQL injection risk!
```

#### API Key Management

```python
# GOOD: Environment variables
import os
api_key = os.getenv("ANTHROPIC_API_KEY")

# BAD: Hardcoded in source
api_key = "sk-ant-api03-hardcoded-key"  # NEVER DO THIS
```

#### CORS Configuration

```python
# Development: Allow local origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Production: Restrict to your domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH"],  # Restrict methods
    allow_headers=["Content-Type"],          # Restrict headers
)
```

---

### Testing

#### Unit Tests

```python
import pytest
from database import get_customer, search_customer

def test_get_customer():
    customer = get_customer("1213210")
    assert customer is not None
    assert customer['name'] == "John Doe"

def test_get_customer_not_found():
    customer = get_customer("9999999")
    assert customer is None

def test_search_customer_by_email():
    customer = search_customer("email", "john@example.com")
    assert customer is not None
    assert customer['id'] == "1213210"

def test_search_customer_invalid_key():
    with pytest.raises(ValueError):
        search_customer("invalid_key", "value")
```

#### Integration Tests

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
    data = response.json()
    assert data['id'] == "1213210"

def test_cancel_order():
    response = client.patch("/api/orders/24601/cancel")
    assert response.status_code in [200, 400]  # Success or already cancelled
```

#### Mock External Dependencies

```python
from unittest.mock import patch, MagicMock

@patch('ai_tools.Anthropic')
def test_chat_with_claude(mock_anthropic):
    # Mock Claude API response
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.stop_reason = "end_turn"
    mock_response.content = [MagicMock(text="Test response")]
    mock_client.messages.create.return_value = mock_response
    mock_anthropic.return_value = mock_client

    result = chat_with_claude("test message")
    assert result['response'] == "Test response"
```

---

## Error Handling

### HTTP Status Codes

| Code | Description | When Used |
|------|-------------|-----------|
| 200 | Success | Successful GET, POST, PATCH operations |
| 400 | Bad Request | Validation error, cannot cancel order (wrong status) |
| 404 | Not Found | Customer or order not found |
| 422 | Unprocessable Entity | Pydantic validation error |
| 500 | Internal Server Error | Database error, Claude API error, unexpected error |

### Error Response Format

All errors return JSON with `detail` field:

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common Error Scenarios

#### Customer Not Found

**Request:**
```bash
GET /api/customers/9999999
```

**Response:** `404`
```json
{
  "detail": "Customer 9999999 not found"
}
```

---

#### Invalid Search Key

**Request:**
```bash
POST /api/customers/search
{
  "key": "invalid_key",
  "value": "test"
}
```

**Response:** `400`
```json
{
  "detail": "Invalid search key: invalid_key. Must be one of ['email', 'phone', 'username']"
}
```

---

#### Cannot Cancel Order

**Request:**
```bash
PATCH /api/orders/24601/cancel
```

**Response:** `400`
```json
{
  "detail": "Cannot cancel order 24601. Status is 'Shipped'. Only orders with status 'Processing' can be cancelled."
}
```

---

#### Validation Error

**Request:**
```bash
PATCH /api/customers/1213210
{
  "email": "invalid-email"
}
```

**Response:** `422`
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

---

#### Missing API Key

**Request:**
```bash
POST /api/chat
{
  "message": "test"
}
```

**Response:** `500`
```json
{
  "detail": "Chat error: ANTHROPIC_API_KEY not found in environment variables. Please add your API key to the .env file."
}
```

---

## Appendix

### Complete Function Reference

#### Database Functions (`database.py`)

| Function | Line | Description |
|----------|------|-------------|
| `init_database()` | 52-68 | Initialize database schema |
| `get_db()` | 71-98 | Context manager for database connections |
| `get_customer()` | 105-122 | Get customer by ID |
| `search_customer()` | 125-148 | Search customer by email/phone/username |
| `get_all_customers()` | 151-162 | Get all customers |
| `update_customer()` | 165-201 | Update customer contact info |
| `get_order()` | 208-225 | Get order by ID |
| `get_customer_orders()` | 228-245 | Get all orders for customer |
| `get_all_orders()` | 248-271 | Get all orders (optionally filtered) |
| `cancel_order()` | 274-310 | Cancel an order |
| `get_customer_with_orders()` | 317-337 | Get customer with orders combined |

#### AI Tools Functions (`ai_tools.py`)

| Function | Line | Description |
|----------|------|-------------|
| `execute_tool()` | 136-217 | Execute a single tool |
| `chat_with_claude()` | 224-333 | Full Claude conversation with tools |
| `process_chat_message()` | 340-353 | Simplified stateless chat wrapper |

#### API Endpoints (`main.py`)

| Endpoint | Method | Line | Description |
|----------|--------|------|-------------|
| `/api/health` | GET | 61-64 | Health check |
| `/api/chat` | POST | 71-94 | Chat with Claude AI |
| `/api/customers` | GET | 101-108 | Get all customers |
| `/api/customers/{id}` | GET | 111-117 | Get customer by ID |
| `/api/customers/search` | POST | 120-142 | Search customer |
| `/api/customers/{id}` | PATCH | 145-177 | Update customer |
| `/api/customers/{id}/orders` | GET | 180-191 | Get customer with orders |
| `/api/orders` | GET | 198-210 | Get all orders |
| `/api/orders/{id}` | GET | 213-219 | Get order by ID |
| `/api/orders/{id}/cancel` | PATCH | 222-239 | Cancel order |

---

### Model Hierarchy

```
BaseModel (Pydantic)
├── Customer
│   ├── id: str (7 digits)
│   ├── name: str
│   ├── email: EmailStr
│   ├── phone: str (XXX-XXX-XXXX)
│   └── username: str (3-20 chars)
│
├── CustomerUpdate
│   ├── email: Optional[EmailStr]
│   └── phone: Optional[str]
│
├── CustomerSearch
│   ├── key: Literal['email', 'phone', 'username']
│   └── value: str
│
├── Order
│   ├── id: str (5 digits)
│   ├── customer_id: str (7 digits, FK)
│   ├── product: str
│   ├── quantity: int (1-999)
│   ├── price: float (0-9999.99)
│   └── status: Literal['Processing', 'Shipped', 'Delivered', 'Cancelled']
│
├── OrderCancelResponse
│   ├── success: bool
│   └── message: str
│
├── ChatMessage
│   └── message: str (1-4000 chars)
│
├── ChatResponse
│   ├── response: str
│   └── tool_calls: Optional[List[Dict]]
│
├── CustomerWithOrders
│   ├── customer: Customer
│   └── orders: List[Order]
│
└── ErrorResponse
    ├── error: str
    └── detail: Optional[str]
```

---

### Database Schema Diagram

```
┌─────────────────────────────────┐
│         customers               │
├─────────────────────────────────┤
│ id TEXT PRIMARY KEY             │
│ name TEXT NOT NULL              │
│ email TEXT NOT NULL UNIQUE      │◄───┐
│ phone TEXT NOT NULL             │    │ Indexed
│ username TEXT NOT NULL UNIQUE   │◄───┘
└─────────────────────────────────┘
         △
         │ Foreign Key
         │ (ON DELETE CASCADE)
         │
┌────────┴────────────────────────┐
│          orders                 │
├─────────────────────────────────┤
│ id TEXT PRIMARY KEY             │
│ customer_id TEXT NOT NULL       │◄───┐ Indexed
│ product TEXT NOT NULL           │    │
│ quantity INTEGER NOT NULL       │    │
│ price REAL NOT NULL             │    │
│ status TEXT NOT NULL            │◄───┘ Indexed
└─────────────────────────────────┘
```

---

### Tool Execution Flow

```
User Message: "Cancel order 24601"
        ↓
┌───────────────────────────┐
│   POST /api/chat          │
│   {message: "Cancel..."}  │
└───────────┬───────────────┘
            ↓
┌───────────────────────────┐
│  process_chat_message()   │
└───────────┬───────────────┘
            ↓
┌───────────────────────────┐
│  chat_with_claude()       │
└───────────┬───────────────┘
            ↓
┌───────────────────────────┐
│  Claude API               │
│  (decides to use tool)    │
└───────────┬───────────────┘
            ↓
     Tool Request:
     {
       "name": "cancel_order",
       "input": {"order_id": "24601"}
     }
            ↓
┌───────────────────────────┐
│  execute_tool()           │
└───────────┬───────────────┘
            ↓
┌───────────────────────────┐
│  db.cancel_order()        │
└───────────┬───────────────┘
            ↓
     Tool Result:
     {
       "success": true,
       "message": "Order cancelled"
     }
            ↓
┌───────────────────────────┐
│  Claude API               │
│  (generates response)     │
└───────────┬───────────────┘
            ↓
     Final Response:
     "I've cancelled order 24601 successfully."
            ↓
┌───────────────────────────┐
│  ChatResponse returned    │
│  to frontend              │
└───────────────────────────┘
```

---

### Quick Reference Card

#### Customer Operations

```python
# Get
customer = db.get_customer("1213210")

# Search
customer = db.search_customer("email", "john@example.com")

# List all
customers = db.get_all_customers()

# Update
db.update_customer("1213210", email="new@example.com")

# With orders
result = db.get_customer_with_orders("1213210")
```

#### Order Operations

```python
# Get
order = db.get_order("24601")

# Customer orders
orders = db.get_customer_orders("1213210")

# All orders
orders = db.get_all_orders()

# Filtered
orders = db.get_all_orders(status="Processing")

# Cancel
result = db.cancel_order("24601")
```

#### AI Chat

```python
# Simple chat
result = process_chat_message("Look up customer john@example.com")
print(result['response'])
print(result['tool_calls'])
```

#### API Calls (curl)

```bash
# Health
curl http://localhost:8000/api/health

# Chat
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "test"}'

# Get customers
curl http://localhost:8000/api/customers

# Search customer
curl -X POST http://localhost:8000/api/customers/search \
  -H "Content-Type: application/json" \
  -d '{"key": "email", "value": "john@example.com"}'

# Cancel order
curl -X PATCH http://localhost:8000/api/orders/24601/cancel
```

---

## Documentation Metadata

**Document Version:** 1.0
**API Version:** 0.1.0
**Last Updated:** 2025-11-17
**Source Code Location:** `{PROJECT_ROOT}`

**Related Documentation:**
- Component Inventory: `01_component_inventory.md`
- Data Flows: `03_data_flows.md`

**For Questions or Issues:**
- Review source code files referenced throughout this document
- Check FastAPI docs at http://localhost:8000/docs (when server running)
- Consult Anthropic API documentation for Claude integration

---

**End of API Reference**
