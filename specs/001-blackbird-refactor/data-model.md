# Data Model: Blackbird Customer Support Application

**Feature**: 001-blackbird-refactor
**Date**: 2025-11-17
**Educational Context**: Simplified for AI Engineering Onramp course

## Overview

Simple 2-table data model preserving the original HuggingFace dataset structure. **No conversation history** - chat is stateless like the original Gradio app.

## Entity Relationship Diagram

```
┌─────────────────┐         ┌──────────────────┐
│    Customer     │1       *│      Order       │
│─────────────────│◄────────│──────────────────│
│ id (PK)         │         │ id (PK)          │
│ name            │         │ customer_id (FK) │
│ email (UNIQUE)  │         │ product          │
│ phone           │         │ quantity         │
│ username (UNIQUE)│        │ price            │
└─────────────────┘         │ status           │
                            └──────────────────┘
```

## Entities

### 1. Customer

**Purpose**: End-user customer account with contact information

**Fields**:

| Field | Type | Constraints | Example |
|-------|------|-------------|---------|
| id | TEXT | PRIMARY KEY | "1213210" |
| name | TEXT | NOT NULL | "John Doe" |
| email | TEXT | NOT NULL, UNIQUE | "john@example.com" |
| phone | TEXT | NOT NULL | "123-456-7890" |
| username | TEXT | NOT NULL, UNIQUE | "johndoe" |

**Validation**:
- Email: standard format (contains @, domain)
- Phone: XXX-XXX-XXXX format
- Username: 3-20 characters, alphanumeric + underscore

**Relationships**: One customer → Many orders

---

### 2. Order

**Purpose**: Product purchase transaction

**Fields**:

| Field | Type | Constraints | Example |
|-------|------|-------------|---------|
| id | TEXT | PRIMARY KEY | "24601" |
| customer_id | TEXT | NOT NULL, FK → customers(id) | "1213210" |
| product | TEXT | NOT NULL | "Wireless Headphones" |
| quantity | INTEGER | NOT NULL, > 0 | 2 |
| price | REAL | NOT NULL, >= 0 | 79.99 |
| status | TEXT | NOT NULL, ENUM | "Processing" |

**Status Values**:
- `Processing` - Can be cancelled
- `Shipped` - Cannot be cancelled
- `Delivered` - Final state
- `Cancelled` - Final state

**Business Rules**:
- Orders can only be cancelled if status = "Processing"
- Status transitions: Processing → (Shipped OR Cancelled)
- Status transitions: Shipped → Delivered

**Relationships**: Many orders → One customer

---

## SQLite Schema

```sql
-- Enable foreign key constraints
PRAGMA foreign_keys = ON;

-- Customers table
CREATE TABLE customers (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone TEXT NOT NULL,
    username TEXT NOT NULL UNIQUE,
    CHECK (length(name) >= 1),
    CHECK (email LIKE '%@%.%'),
    CHECK (phone LIKE '___-___-____'),
    CHECK (length(username) >= 3 AND length(username) <= 20)
);

-- Orders table
CREATE TABLE orders (
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
CREATE INDEX idx_customers_email ON customers(email);
CREATE INDEX idx_customers_username ON customers(username);
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_orders_status ON orders(status);
```

---

## Pydantic Models (Python)

```python
from pydantic import BaseModel, EmailStr, Field
from typing import Literal

class Customer(BaseModel):
    id: str = Field(..., pattern=r'^\d{7}$')
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone: str = Field(..., pattern=r'^\d{3}-\d{3}-\d{4}$')
    username: str = Field(..., min_length=3, max_length=20, pattern=r'^[a-zA-Z0-9_]+$')

class CustomerUpdate(BaseModel):
    email: EmailStr | None = None
    phone: str | None = Field(None, pattern=r'^\d{3}-\d{3}-\d{4}$')

class Order(BaseModel):
    id: str = Field(..., pattern=r'^\d{5}$')
    customer_id: str = Field(..., pattern=r'^\d{7}$')
    product: str = Field(..., min_length=1, max_length=200)
    quantity: int = Field(..., gt=0, le=999)
    price: float = Field(..., ge=0, lt=10000)
    status: Literal['Processing', 'Shipped', 'Delivered', 'Cancelled']

class ChatMessage(BaseModel):
    message: str = Field(..., min_length=1, max_length=4000)

class ChatResponse(BaseModel):
    response: str
    tool_calls: list[dict] | None = None  # Optional: show which tools were used
```

---

## Data Migration Mapping

**HuggingFace → SQLite** (one-time migration):

| Source Dataset | Target Table | Records |
|----------------|--------------|---------|
| dwb2023/blackbird-customers | customers | 10 |
| dwb2023/blackbird-orders | orders | 13 |

**Migration Steps**:
1. Load HF datasets: `load_dataset("dwb2023/blackbird-customers")`
2. Create SQLite schema: `CREATE TABLE customers ...`
3. Insert customers: 10 records
4. Insert orders: 13 records
5. Verify foreign keys: All order.customer_id exist in customers.id
6. Verify counts: `SELECT COUNT(*) FROM customers` = 10

**Migration Script** (migrate_data.py):
```python
from datasets import load_dataset
import sqlite3

def migrate():
    # Load HF datasets
    customers = load_dataset("dwb2023/blackbird-customers", split="train")
    orders = load_dataset("dwb2023/blackbird-orders", split="train")

    # Create SQLite database
    conn = sqlite3.connect("blackbird.db")
    cursor = conn.cursor()

    # Create schema (SQL above)
    # ...

    # Insert customers
    for customer in customers:
        cursor.execute(
            "INSERT INTO customers VALUES (?, ?, ?, ?, ?)",
            (customer['id'], customer['name'], customer['email'],
             customer['phone'], customer['username'])
        )

    # Insert orders
    for order in orders:
        cursor.execute(
            "INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?)",
            (order['id'], order['customer_id'], order['product'],
             order['quantity'], order['price'], order['status'])
        )

    conn.commit()
    print(f"✓ Migrated {len(customers)} customers, {len(orders)} orders")
```

---

## Sample Data

**Customers** (3 of 10):
```
id=1213210, name=John Doe, email=john@example.com, phone=123-456-7890, username=johndoe
id=2837622, name=Priya Patel, email=priya@example.com, phone=987-654-3210, username=priya123
id=3924156, name=Liam Nguyen, email=liam@example.com, phone=555-123-4567, username=liamn
```

**Orders** (3 of 13):
```
id=24601, customer_id=1213210, product=Wireless Headphones, quantity=1, price=79.99, status=Shipped
id=13579, customer_id=1213210, product=Smartphone Case, quantity=2, price=19.99, status=Cancelled
id=97531, customer_id=2837622, product=Bluetooth Speaker, quantity=1, price=49.99, status=Processing
```

---

## Validation Rules Summary

**Customer**:
- ID: 7-digit string
- Email: valid email format
- Phone: XXX-XXX-XXXX
- Username: 3-20 chars, alphanumeric + _

**Order**:
- ID: 5-digit string
- Customer ID: must exist in customers table
- Quantity: positive integer
- Price: non-negative decimal
- Status: one of 4 enum values
- Cancel rule: only if status="Processing"

---

## Educational Notes

**Why only 2 tables?**
- Matches original Gradio app simplicity
- Students focus on AI integration, not database design
- Conversation history adds complexity with no learning value for this course

**Why no timestamps?**
- Not in original HuggingFace datasets
- Not needed for core learning objectives
- Can be added later if students want to extend the project

**Why TEXT IDs instead of AUTOINCREMENT INTEGER?**
- Preserves exact data from HuggingFace datasets
- Shows that IDs don't have to be integers
- Avoids migration complexity of ID mapping

This simplified model supports all P1 and P2 user stories without the overhead of conversation tracking.
