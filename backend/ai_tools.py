"""
Claude AI Integration with Function Calling (November 2025 SDK Patterns).

Implements 6 tools for customer support operations:
1. get_user - Search customer by email/phone/username
2. get_order_by_id - Lookup order details
3. get_customer_orders - Get all orders for a customer
4. cancel_order - Cancel an order (if Processing status)
5. update_user_contact - Update customer email/phone
6. get_user_info - Get customer + orders combined

Educational focus: Teaching Claude AI function calling integration.

SDK Implementation Notes (2025):
- Uses Anthropic SDK v0.73.0+ with Messages API
- Tool definitions use "input_schema" (not "parameters")
- Tool results support simple string content (wrapping optional)
- Supports parallel tool execution (via tool_choice.disable_parallel_tool_use)
- Error handling via "is_error" flag in tool results
- Multi-turn conversation with proper message history management
"""

import os
import json
from typing import Dict, Any, List, Optional
from anthropic import Anthropic
import database as db


# ============================================================================
# Tool Definitions (JSON Schema format for Claude API)
# ============================================================================

TOOLS = [
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
    },
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
    },
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
    },
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
    },
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
    },
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
]


# ============================================================================
# Tool Execution Logic
# ============================================================================

def execute_tool(tool_name: str, tool_input: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute a tool and return the result.

    Args:
        tool_name: Name of the tool to execute
        tool_input: Tool parameters as a dict

    Returns:
        Dict with tool execution result

    Raises:
        ValueError: If tool_name is not recognized
    """
    if tool_name == "get_user":
        # Search customer by key/value
        customer = db.search_customer(tool_input["key"], tool_input["value"])
        if customer:
            return {"success": True, "customer": customer}
        else:
            return {"success": False, "message": f"No customer found with {tool_input['key']}={tool_input['value']}"}

    elif tool_name == "get_order_by_id":
        # Get order by ID
        order = db.get_order(tool_input["order_id"])
        if order:
            return {"success": True, "order": order}
        else:
            return {"success": False, "message": f"Order {tool_input['order_id']} not found"}

    elif tool_name == "get_customer_orders":
        # Get all orders for a customer
        orders = db.get_customer_orders(tool_input["customer_id"])
        return {"success": True, "orders": orders, "count": len(orders)}

    elif tool_name == "cancel_order":
        # Cancel an order (only if Processing)
        result = db.cancel_order(tool_input["order_id"])
        return result

    elif tool_name == "update_user_contact":
        # Update customer contact info
        customer_id = tool_input["customer_id"]
        email = tool_input.get("email")
        phone = tool_input.get("phone")

        if not email and not phone:
            return {"success": False, "message": "Must provide at least email or phone to update"}

        success = db.update_customer(customer_id, email=email, phone=phone)

        if success:
            return {"success": True, "message": f"Updated contact info for customer {customer_id}"}
        else:
            return {"success": False, "message": f"Customer {customer_id} not found"}

    elif tool_name == "get_user_info":
        # Get customer + orders combined
        key = tool_input["key"]
        value = tool_input["value"]

        # First find the customer
        if key == "customer_id":
            customer = db.get_customer(value)
        else:
            customer = db.search_customer(key, value)

        if not customer:
            return {"success": False, "message": f"No customer found with {key}={value}"}

        # Get their orders
        orders = db.get_customer_orders(customer["id"])

        return {
            "success": True,
            "customer": customer,
            "orders": orders,
            "order_count": len(orders)
        }

    else:
        raise ValueError(f"Unknown tool: {tool_name}")


# ============================================================================
# Claude API Integration
# ============================================================================

def chat_with_claude(message: str, conversation_history: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    """
    Send a message to Claude with tool calling enabled (2025 SDK Pattern).

    This implements the multi-turn conversation flow:
    1. Send user message with available tools
    2. If Claude wants to use tools (stop_reason == "tool_use"), execute them
    3. Send tool results back to Claude in proper message format
    4. Return Claude's final response

    Args:
        message: User's message
        conversation_history: Optional list of previous messages

    Returns:
        Dict with:
            - response: Claude's text response
            - tool_calls: List of tools used (for transparency/debugging)

    Educational note: This demonstrates the full Claude function calling workflow
    using November 2025 SDK patterns:
    - Proper conversation history with assistant/user role alternation
    - Tool result blocks with optional "is_error" flag
    - Support for parallel tool execution
    - Simple string content format (no wrapping required)
    """
    # Initialize Anthropic client
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return {
            "response": "Error: ANTHROPIC_API_KEY not found in environment variables. "
                       "Please add your API key to the .env file.",
            "tool_calls": []
        }

    client = Anthropic(api_key=api_key)

    # Build conversation messages
    if conversation_history is None:
        conversation_history = []

    # Add user message
    messages = conversation_history + [{"role": "user", "content": message}]

    # Track tool calls for transparency
    tool_calls_log = []

    try:
        # Step 1: Send message to Claude with tools
        # Note: Claude 2025 supports parallel tool execution by default
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",  # Claude 4.5 Haiku (latest)
            max_tokens=1024,
            tools=TOOLS,
            messages=messages,
            tool_choice={
                "type": "auto",  # Claude decides which tools to use
                "disable_parallel_tool_use": False,  # False = parallel enabled (default)
            },
            # Other tool_choice options:
            # {"type": "any"}  # Force Claude to use at least one tool
            # {"type": "tool", "name": "get_user"}  # Force specific tool
            # {"type": "none"}  # Prevent tool use
        )

        # Step 2: Check if Claude wants to use tools
        while response.stop_reason == "tool_use":
            # Extract tool use blocks
            tool_use_blocks = [block for block in response.content if block.type == "tool_use"]

            # Execute each tool
            tool_results = []
            for tool_use in tool_use_blocks:
                tool_name = tool_use.name
                tool_input = tool_use.input

                # Log the tool call
                tool_calls_log.append({
                    "tool": tool_name,
                    "input": tool_input
                })

                # Execute the tool
                try:
                    result = execute_tool(tool_name, tool_input)
                    is_error = False
                except Exception as e:
                    result = {"error": str(e)}
                    is_error = True

                # Format tool result for Claude (2025 SDK pattern)
                # Note: Simple string content is valid; wrapping in [{"type": "text"}] is optional
                tool_result = {
                    "type": "tool_result",
                    "tool_use_id": tool_use.id,
                    "content": json.dumps(result)
                }

                # Add error flag if tool execution failed (2025 SDK enhancement)
                if is_error or (isinstance(result, dict) and "error" in result):
                    tool_result["is_error"] = True

                tool_results.append(tool_result)

            # Step 3: Send tool results back to Claude
            messages = messages + [
                {"role": "assistant", "content": response.content},
                {"role": "user", "content": tool_results}
            ]

            response = client.messages.create(
                model="claude-haiku-4-5-20251001",  # Claude 4.5 Haiku
                max_tokens=1024,
                tools=TOOLS,
                messages=messages,
                tool_choice={
                    "type": "auto",
                    "disable_parallel_tool_use": False,
                },
            )

        # Step 4: Extract final text response
        text_response = ""
        for block in response.content:
            if hasattr(block, "text"):
                text_response += block.text

        return {
            "response": text_response,
            "tool_calls": tool_calls_log
        }

    except Exception as e:
        return {
            "response": f"Error communicating with Claude AI: {str(e)}",
            "tool_calls": tool_calls_log
        }


# ============================================================================
# Convenience Function for Stateless Chat
# ============================================================================

def process_chat_message(message: str) -> Dict[str, Any]:
    """
    Process a single chat message (stateless).

    This is a simplified wrapper for educational purposes.
    In production, you'd maintain conversation history per user.

    Args:
        message: User's message

    Returns:
        Dict with response and tool_calls
    """
    return chat_with_claude(message, conversation_history=None)
