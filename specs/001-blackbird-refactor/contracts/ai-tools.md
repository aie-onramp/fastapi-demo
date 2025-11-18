# AI Tool Contracts: Claude Function Calling

**Feature**: 001-blackbird-refactor
**Date**: 2025-11-17
**Purpose**: Define Claude AI function calling tools for customer support operations

## Overview

These tool definitions maintain compatibility with the existing Blackbird HuggingFace application while adapting to the new SQLite backend. All tool schemas follow the Anthropic Claude API format for function calling.

## Tool Definitions

### 1. get_user

**Purpose**: Search for a customer by email, phone, or username

**Schema**:
```json
{
  "name": "get_user",
  "description": "Retrieves customer information by searching with email, phone, or username. Returns the customer's full profile including ID, name, email, phone, and username.",
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
        "description": "The value to search for in the specified field"
      }
    },
    "required": ["key", "value"]
  }
}
```

**Example Usage**:
```
User: "Look up customer with email john@example.com"

Tool Call:
{
  "name": "get_user",
  "input": {
    "key": "email",
    "value": "john@example.com"
  }
}

Tool Response:
{
  "id": "1213210",
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "123-456-7890",
  "username": "johndoe"
}
```

**Implementation**: Calls `CustomerService.search_customer(key, value)`

---

### 2. get_order_by_id

**Purpose**: Retrieve order details using order ID

**Schema**:
```json
{
  "name": "get_order_by_id",
  "description": "Retrieves order details by order ID. Returns order information including customer ID, product, quantity, price, and current status.",
  "input_schema": {
    "type": "object",
    "properties": {
      "order_id": {
        "type": "string",
        "pattern": "^\\d{5}$",
        "description": "The 5-digit order ID"
      }
    },
    "required": ["order_id"]
  }
}
```

**Example Usage**:
```
User: "What's the status of order 24601?"

Tool Call:
{
  "name": "get_order_by_id",
  "input": {
    "order_id": "24601"
  }
}

Tool Response:
{
  "id": "24601",
  "customer_id": "1213210",
  "product": "Wireless Headphones",
  "quantity": 1,
  "price": 79.99,
  "status": "Shipped"
}
```

**Implementation**: Calls `OrderService.get_order(order_id)`

---

### 3. get_customer_orders

**Purpose**: Retrieve all orders for a specific customer

**Schema**:
```json
{
  "name": "get_customer_orders",
  "description": "Retrieves all orders associated with a customer ID. Returns an array of order objects.",
  "input_schema": {
    "type": "object",
    "properties": {
      "customer_id": {
        "type": "string",
        "pattern": "^\\d{7}$",
        "description": "The 7-digit customer ID"
      }
    },
    "required": ["customer_id"]
  }
}
```

**Example Usage**:
```
User: "Show me all orders for customer 1213210"

Tool Call:
{
  "name": "get_customer_orders",
  "input": {
    "customer_id": "1213210"
  }
}

Tool Response:
[
  {
    "id": "24601",
    "customer_id": "1213210",
    "product": "Wireless Headphones",
    "quantity": 1,
    "price": 79.99,
    "status": "Shipped"
  },
  {
    "id": "13579",
    "customer_id": "1213210",
    "product": "Smartphone Case",
    "quantity": 2,
    "price": 19.99,
    "status": "Cancelled"
  }
]
```

**Implementation**: Calls `OrderService.get_customer_orders(customer_id)`

---

### 4. cancel_order

**Purpose**: Cancel an order (only if status is "Processing")

**Schema**:
```json
{
  "name": "cancel_order",
  "description": "Cancels an order by changing its status to 'Cancelled'. Only works if the order status is currently 'Processing'. Returns an error if the order has already shipped or been delivered.",
  "input_schema": {
    "type": "object",
    "properties": {
      "order_id": {
        "type": "string",
        "pattern": "^\\d{5}$",
        "description": "The 5-digit order ID to cancel"
      }
    },
    "required": ["order_id"]
  }
}
```

**Example Usage (Success)**:
```
User: "Cancel order 47652"

Tool Call:
{
  "name": "cancel_order",
  "input": {
    "order_id": "47652"
  }
}

Tool Response:
{
  "status": "Cancelled",
  "message": "Order 47652 has been successfully cancelled"
}
```

**Example Usage (Failure)**:
```
User: "Cancel order 24601"

Tool Call:
{
  "name": "cancel_order",
  "input": {
    "order_id": "24601"
  }
}

Tool Response (Error):
{
  "error": "Order has already shipped. Can't cancel it.",
  "status": "Shipped"
}
```

**Implementation**: Calls `OrderService.cancel_order(order_id)` which validates status before updating

---

### 5. update_user_contact

**Purpose**: Update customer email and/or phone number

**Schema**:
```json
{
  "name": "update_user_contact",
  "description": "Updates a customer's contact information (email and/or phone number). At least one field must be provided. Returns the updated customer profile.",
  "input_schema": {
    "type": "object",
    "properties": {
      "user_id": {
        "type": "string",
        "pattern": "^\\d{7}$",
        "description": "The 7-digit customer ID"
      },
      "email": {
        "type": "string",
        "format": "email",
        "description": "New email address (optional)"
      },
      "phone": {
        "type": "string",
        "pattern": "^\\d{3}-\\d{3}-\\d{4}$",
        "description": "New phone number in format XXX-XXX-XXXX (optional)"
      }
    },
    "required": ["user_id"],
    "minProperties": 2
  }
}
```

**Example Usage**:
```
User: "Update customer 1213210's email to newemail@example.com"

Tool Call:
{
  "name": "update_user_contact",
  "input": {
    "user_id": "1213210",
    "email": "newemail@example.com"
  }
}

Tool Response:
{
  "id": "1213210",
  "name": "John Doe",
  "email": "newemail@example.com",
  "phone": "123-456-7890",
  "username": "johndoe",
  "message": "User information updated successfully"
}
```

**Implementation**: Calls `CustomerService.update_customer(user_id, email, phone)`

---

### 6. get_user_info

**Purpose**: Get comprehensive user information including orders in one call

**Schema**:
```json
{
  "name": "get_user_info",
  "description": "Retrieves comprehensive customer information including their profile and all associated orders. This is a convenience method that combines get_user and get_customer_orders.",
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
        "description": "The value to search for in the specified field"
      }
    },
    "required": ["key", "value"]
  }
}
```

**Example Usage**:
```
User: "Show me everything about customer johndoe"

Tool Call:
{
  "name": "get_user_info",
  "input": {
    "key": "username",
    "value": "johndoe"
  }
}

Tool Response:
{
  "user_info": {
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
      "id": "13579",
      "customer_id": "1213210",
      "product": "Smartphone Case",
      "quantity": 2,
      "price": 19.99,
      "status": "Cancelled"
    }
  ]
}
```

**Implementation**: Calls `CustomerService.get_user_with_orders(key, value)`

---

## Tool Handler Implementation Pattern

The `ToolHandler` class orchestrates tool execution:

```python
class ToolHandler:
    def __init__(self, db_session):
        self.customer_service = CustomerService(db_session)
        self.order_service = OrderService(db_session)

    async def execute_tool(self, tool_name: str, tool_input: dict) -> dict:
        """Execute a tool and return its result"""
        tool_map = {
            "get_user": self._get_user,
            "get_order_by_id": self._get_order_by_id,
            "get_customer_orders": self._get_customer_orders,
            "cancel_order": self._cancel_order,
            "update_user_contact": self._update_user_contact,
            "get_user_info": self._get_user_info,
        }

        if tool_name not in tool_map:
            raise ValueError(f"Unknown tool: {tool_name}")

        return await tool_map[tool_name](tool_input)

    async def _get_user(self, tool_input: dict) -> dict:
        return await self.customer_service.search_customer(
            tool_input["key"],
            tool_input["value"]
        )

    # ... other tool implementations
```

## Error Handling

All tools follow consistent error response format:

```json
{
  "error": "Human-readable error message",
  "details": {
    "field": "value"
  }
}
```

**Common Errors**:
- **Customer not found**: `{"error": "Couldn't find a user with {key} of {value}"}`
- **Order not found**: `{"error": "Order not found"}`
- **Cannot cancel**: `{"error": "Order has already shipped. Can't cancel it.", "status": "Shipped"}`
- **Email in use**: `{"error": "Email already in use by another customer"}`
- **Invalid input**: `{"error": "Validation failed", "details": [...]}`

## Testing Strategy

**Unit Tests** (`tests/unit/test_tool_handler.py`):
- Test each tool with valid inputs
- Test error cases (not found, validation errors)
- Mock service layer

**Integration Tests** (`tests/integration/test_ai_tools.py`):
- Test tools with real database (test fixtures)
- Verify database state changes (updates, cancellations)
- Test transactional behavior

**Contract Tests** (`tests/contract/test_ai_tools.py`):
- Validate tool schemas match Claude API format
- Verify all required fields present
- Test with Claude SDK (mocked API responses)

## Migration Notes

**Changes from HuggingFace Implementation**:
1. Tool handler now calls local services instead of HTTP POST to external API
2. Database operations use SQLAlchemy ORM instead of HuggingFace datasets
3. Error responses standardized across all tools
4. Tool execution is asynchronous (async/await pattern)

**Compatibility**:
- Tool names unchanged
- Input schemas unchanged
- Output formats unchanged (JSON structure identical)
- Error messages preserved where possible

This ensures the Claude AI system prompt and tool invocation logic requires no changes.
