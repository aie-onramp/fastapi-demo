"""
Database module for Blackbird Customer Support Application.

Provides SQLite schema creation, connection management, and CRUD operations.
"""

import sqlite3
from contextlib import contextmanager
from typing import Optional, List, Dict, Any

# Database file path
DATABASE_PATH = "blackbird.db"

# SQL Schema Definitions
SCHEMA_SQL = """
-- Enable foreign key constraints
PRAGMA foreign_keys = ON;

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
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE,
    CHECK (length(product) >= 1)
);

-- Indexes for search performance
CREATE INDEX IF NOT EXISTS idx_customers_email ON customers(email);
CREATE INDEX IF NOT EXISTS idx_customers_username ON customers(username);
CREATE INDEX IF NOT EXISTS idx_orders_customer_id ON orders(customer_id);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);
"""


def init_database() -> None:
    """
    Initialize the database schema.

    Creates tables and indexes if they don't exist.
    Safe to call multiple times (uses IF NOT EXISTS).
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Execute schema SQL (multiple statements)
    cursor.executescript(SCHEMA_SQL)

    conn.commit()
    conn.close()

    print(f"✓ Database schema initialized: {DATABASE_PATH}")


@contextmanager
def get_db():
    """
    Context manager for database connections.

    Usage:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM customers")
            results = cursor.fetchall()

    Yields:
        sqlite3.Connection: Database connection with row_factory set to Row

    Note:
        Automatically commits on success and rolls back on error.
        Connection is closed when context exits.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # Access columns by name
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


# ============================================================================
# Customer CRUD Operations
# ============================================================================

def get_customer(customer_id: str) -> Optional[Dict[str, Any]]:
    """
    Get customer by ID.

    Args:
        customer_id: Customer ID (7-digit string)

    Returns:
        Customer dict or None if not found
    """
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM customers WHERE id = ?",
            (customer_id,)
        )
        row = cursor.fetchone()
        return dict(row) if row else None


def search_customer(key: str, value: str) -> Optional[Dict[str, Any]]:
    """
    Search for customer by email, phone, or username.

    Args:
        key: Search field ('email', 'phone', or 'username')
        value: Search value

    Returns:
        Customer dict or None if not found

    Raises:
        ValueError: If key is not a valid search field
    """
    valid_keys = ['email', 'phone', 'username']
    if key not in valid_keys:
        raise ValueError(f"Invalid search key: {key}. Must be one of {valid_keys}")

    with get_db() as conn:
        cursor = conn.cursor()
        query = f"SELECT * FROM customers WHERE {key} = ?"
        cursor.execute(query, (value,))
        row = cursor.fetchone()
        return dict(row) if row else None


def get_all_customers() -> List[Dict[str, Any]]:
    """
    Get all customers.

    Returns:
        List of customer dicts
    """
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM customers ORDER BY name")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


def update_customer(customer_id: str, email: Optional[str] = None,
                    phone: Optional[str] = None) -> bool:
    """
    Update customer contact information.

    Args:
        customer_id: Customer ID
        email: New email (optional)
        phone: New phone (optional)

    Returns:
        True if update successful, False if customer not found

    Raises:
        ValueError: If neither email nor phone provided
    """
    if email is None and phone is None:
        raise ValueError("Must provide at least one field to update")

    updates = []
    params = []

    if email is not None:
        updates.append("email = ?")
        params.append(email)

    if phone is not None:
        updates.append("phone = ?")
        params.append(phone)

    params.append(customer_id)

    with get_db() as conn:
        cursor = conn.cursor()
        query = f"UPDATE customers SET {', '.join(updates)} WHERE id = ?"
        cursor.execute(query, tuple(params))
        return cursor.rowcount > 0


# ============================================================================
# Order CRUD Operations
# ============================================================================

def get_order(order_id: str) -> Optional[Dict[str, Any]]:
    """
    Get order by ID.

    Args:
        order_id: Order ID (5-digit string)

    Returns:
        Order dict or None if not found
    """
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM orders WHERE id = ?",
            (order_id,)
        )
        row = cursor.fetchone()
        return dict(row) if row else None


def get_customer_orders(customer_id: str) -> List[Dict[str, Any]]:
    """
    Get all orders for a customer.

    Args:
        customer_id: Customer ID

    Returns:
        List of order dicts
    """
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM orders WHERE customer_id = ? ORDER BY id",
            (customer_id,)
        )
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


def get_all_orders(status: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Get all orders, optionally filtered by status.

    Args:
        status: Filter by status ('Processing', 'Shipped', 'Delivered', 'Cancelled')
               If None, returns all orders.

    Returns:
        List of order dicts
    """
    with get_db() as conn:
        cursor = conn.cursor()

        if status:
            cursor.execute(
                "SELECT * FROM orders WHERE status = ? ORDER BY id",
                (status,)
            )
        else:
            cursor.execute("SELECT * FROM orders ORDER BY id")

        rows = cursor.fetchall()
        return [dict(row) for row in rows]


def cancel_order(order_id: str) -> Dict[str, Any]:
    """
    Cancel an order (only if status is 'Processing').

    Args:
        order_id: Order ID

    Returns:
        Dict with 'success' boolean and 'message' string

    Business rule: Orders can only be cancelled if status = 'Processing'
    """
    # Check current status
    order = get_order(order_id)

    if not order:
        return {"success": False, "message": f"Order {order_id} not found"}

    if order['status'] != 'Processing':
        return {
            "success": False,
            "message": f"Cannot cancel order {order_id}. Status is '{order['status']}'. "
                      "Only orders with status 'Processing' can be cancelled."
        }

    # Update status to Cancelled
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE orders SET status = 'Cancelled' WHERE id = ?",
            (order_id,)
        )

    return {
        "success": True,
        "message": f"Order {order_id} cancelled successfully"
    }


# ============================================================================
# Combined Operations
# ============================================================================

def get_customer_with_orders(customer_id: str) -> Optional[Dict[str, Any]]:
    """
    Get customer information with all their orders.

    Args:
        customer_id: Customer ID

    Returns:
        Dict with customer info and orders list, or None if customer not found
    """
    customer = get_customer(customer_id)

    if not customer:
        return None

    orders = get_customer_orders(customer_id)

    return {
        "customer": customer,
        "orders": orders
    }
