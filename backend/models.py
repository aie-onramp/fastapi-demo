"""
Pydantic models for request/response validation.

Defines data schemas for Customer, Order, and Chat interactions.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal, List, Dict, Any


# ============================================================================
# Customer Models
# ============================================================================

class Customer(BaseModel):
    """
    Customer data model.

    Represents a customer with contact information.
    """
    id: str = Field(..., pattern=r'^\d{7}$', description="7-digit customer ID")
    name: str = Field(..., min_length=1, max_length=100, description="Customer full name")
    email: EmailStr = Field(..., description="Customer email address")
    phone: str = Field(..., pattern=r'^\d{3}-\d{3}-\d{4}$', description="Phone in XXX-XXX-XXXX format")
    username: str = Field(
        ...,
        min_length=3,
        max_length=20,
        pattern=r'^[a-zA-Z0-9_]+$',
        description="Username (alphanumeric + underscore)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "id": "1213210",
                "name": "John Doe",
                "email": "john@example.com",
                "phone": "123-456-7890",
                "username": "johndoe"
            }
        }


class CustomerUpdate(BaseModel):
    """
    Customer update request model.

    Allows updating email and/or phone. At least one field must be provided.
    """
    email: Optional[EmailStr] = Field(None, description="New email address")
    phone: Optional[str] = Field(None, pattern=r'^\d{3}-\d{3}-\d{4}$', description="New phone in XXX-XXX-XXXX format")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "newemail@example.com",
                "phone": "555-123-4567"
            }
        }


class CustomerSearch(BaseModel):
    """
    Customer search request model.

    Search by email, phone, or username.
    """
    key: Literal['email', 'phone', 'username'] = Field(..., description="Field to search by")
    value: str = Field(..., min_length=1, description="Value to search for")

    class Config:
        json_schema_extra = {
            "example": {
                "key": "email",
                "value": "john@example.com"
            }
        }


# ============================================================================
# Order Models
# ============================================================================

class Order(BaseModel):
    """
    Order data model.

    Represents a product purchase transaction.
    """
    id: str = Field(..., pattern=r'^\d{5}$', description="5-digit order ID")
    customer_id: str = Field(..., pattern=r'^\d{7}$', description="7-digit customer ID")
    product: str = Field(..., min_length=1, max_length=200, description="Product name")
    quantity: int = Field(..., gt=0, le=999, description="Quantity ordered")
    price: float = Field(..., ge=0, lt=10000, description="Price per unit")
    status: Literal['Processing', 'Shipped', 'Delivered', 'Cancelled'] = Field(
        ...,
        description="Order status"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "id": "24601",
                "customer_id": "1213210",
                "product": "Wireless Headphones",
                "quantity": 1,
                "price": 79.99,
                "status": "Processing"
            }
        }


class OrderCancelResponse(BaseModel):
    """
    Response model for order cancellation.
    """
    success: bool = Field(..., description="Whether cancellation succeeded")
    message: str = Field(..., description="Cancellation result message")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Order 24601 cancelled successfully"
            }
        }


# ============================================================================
# Chat Models
# ============================================================================

class ChatMessage(BaseModel):
    """
    Chat message request model.

    User's message to send to Claude AI.
    """
    message: str = Field(..., min_length=1, max_length=4000, description="User's chat message")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Look up customer with email john@example.com"
            }
        }


class ChatResponse(BaseModel):
    """
    Chat response model.

    Claude AI's response with optional tool call information.
    """
    response: str = Field(..., description="AI assistant's response text")
    tool_calls: Optional[List[Dict[str, Any]]] = Field(
        None,
        description="List of tools called by AI (for debugging/transparency)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "response": "I found the customer John Doe (ID: 1213210) with email john@example.com. "
                           "They have 2 orders on file.",
                "tool_calls": [
                    {
                        "tool": "get_user",
                        "input": {"key": "email", "value": "john@example.com"}
                    },
                    {
                        "tool": "get_customer_orders",
                        "input": {"customer_id": "1213210"}
                    }
                ]
            }
        }


# ============================================================================
# Combined Response Models
# ============================================================================

class CustomerWithOrders(BaseModel):
    """
    Customer with their orders.

    Used for combined customer + orders queries.
    """
    customer: Customer
    orders: List[Order]

    class Config:
        json_schema_extra = {
            "example": {
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
                ]
            }
        }


# ============================================================================
# Error Response Models
# ============================================================================

class ErrorResponse(BaseModel):
    """
    Standard error response model.
    """
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Additional error details")

    class Config:
        json_schema_extra = {
            "example": {
                "error": "Customer not found",
                "detail": "No customer exists with ID 9999999"
            }
        }
