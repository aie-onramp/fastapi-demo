"""
Blackbird Customer Support Application - FastAPI Backend

Main application file with API routes for:
- Chat (Claude AI integration)
- Customer management
- Order management
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from typing import List, Optional

import database as db
import ai_tools
from models import (
    Customer,
    CustomerUpdate,
    CustomerSearch,
    Order,
    OrderCancelResponse,
    ChatMessage,
    ChatResponse,
    CustomerWithOrders,
    ErrorResponse
)

# Load environment variables from .env (look in parent directory)
import os
from pathlib import Path

# Get the parent directory (project root)
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Create FastAPI app
app = FastAPI(
    title="Blackbird Customer Support API",
    description="FastAPI backend with Claude AI integration for customer support",
    version="0.1.0"
)

# Configure CORS for React frontend
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


# ============================================================================
# Health Check
# ============================================================================

@app.get("/api/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "blackbird-api"}


# ============================================================================
# Chat Endpoints (Claude AI)
# ============================================================================

@app.post("/api/chat", response_model=ChatResponse)
def chat(message: ChatMessage):
    """
    Send a message to Claude AI assistant.

    The AI can use 6 tools to help with customer support:
    - Look up customers
    - View orders
    - Cancel orders
    - Update customer contact info

    Example messages:
    - "Look up customer with email john@example.com"
    - "Show me their orders"
    - "Cancel order 47652"
    """
    try:
        result = ai_tools.process_chat_message(message.message)
        return ChatResponse(
            response=result["response"],
            tool_calls=result.get("tool_calls")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")


# ============================================================================
# Customer Endpoints
# ============================================================================

@app.get("/api/customers", response_model=List[Customer])
def get_customers():
    """Get all customers."""
    try:
        customers = db.get_all_customers()
        return customers
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/customers/{customer_id}", response_model=Customer)
def get_customer(customer_id: str):
    """Get a specific customer by ID."""
    customer = db.get_customer(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail=f"Customer {customer_id} not found")
    return customer


@app.post("/api/customers/search", response_model=Customer)
def search_customer(search: CustomerSearch):
    """
    Search for a customer by email, phone, or username.

    Request body:
    {
        "key": "email|phone|username",
        "value": "search value"
    }
    """
    try:
        customer = db.search_customer(search.key, search.value)
        if not customer:
            raise HTTPException(
                status_code=404,
                detail=f"No customer found with {search.key}={search.value}"
            )
        return customer
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.patch("/api/customers/{customer_id}", response_model=Customer)
def update_customer(customer_id: str, update: CustomerUpdate):
    """
    Update a customer's contact information.

    Can update email and/or phone. At least one field must be provided.
    """
    try:
        # Check if customer exists
        customer = db.get_customer(customer_id)
        if not customer:
            raise HTTPException(status_code=404, detail=f"Customer {customer_id} not found")

        # Update customer
        success = db.update_customer(
            customer_id,
            email=update.email,
            phone=update.phone
        )

        if not success:
            raise HTTPException(status_code=500, detail="Update failed")

        # Return updated customer
        updated_customer = db.get_customer(customer_id)
        return updated_customer

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/customers/{customer_id}/orders", response_model=CustomerWithOrders)
def get_customer_with_orders(customer_id: str):
    """Get a customer with all their orders."""
    try:
        result = db.get_customer_with_orders(customer_id)
        if not result:
            raise HTTPException(status_code=404, detail=f"Customer {customer_id} not found")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Order Endpoints
# ============================================================================

@app.get("/api/orders", response_model=List[Order])
def get_orders(status: Optional[str] = Query(None, description="Filter by status")):
    """
    Get all orders, optionally filtered by status.

    Query parameters:
    - status: Filter by status (Processing, Shipped, Delivered, Cancelled)
    """
    try:
        orders = db.get_all_orders(status=status)
        return orders
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/orders/{order_id}", response_model=Order)
def get_order(order_id: str):
    """Get a specific order by ID."""
    order = db.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail=f"Order {order_id} not found")
    return order


@app.patch("/api/orders/{order_id}/cancel", response_model=OrderCancelResponse)
def cancel_order(order_id: str):
    """
    Cancel an order.

    Only orders with status 'Processing' can be cancelled.
    Returns success/failure message.
    """
    try:
        result = db.cancel_order(order_id)
        if not result["success"]:
            # Return 400 if cancellation not allowed (e.g., order already shipped)
            raise HTTPException(status_code=400, detail=result["message"])
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Startup Event
# ============================================================================

@app.on_event("startup")
def startup_event():
    """Initialize database on startup."""
    print("🚀 Starting Blackbird Customer Support API...")
    print("📊 Initializing database...")
    db.init_database()
    print("✅ Database initialized")
    print("🤖 Claude AI integration ready")
    print("📡 API available at http://localhost:8000")
    print("📚 Docs available at http://localhost:8000/docs")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
