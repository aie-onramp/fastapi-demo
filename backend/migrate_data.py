"""
Data migration script: HuggingFace datasets → SQLite

Migrates customer and order data from HuggingFace datasets to SQLite database.

Source datasets:
- dwb2023/blackbird-customers (10 customers)
- dwb2023/blackbird-orders (13 orders)

Usage:
    python migrate_data.py
"""

import sqlite3
from datasets import load_dataset
from database import init_database, DATABASE_PATH


def migrate():
    """
    Migrate data from HuggingFace datasets to SQLite.

    Steps:
    1. Initialize database schema
    2. Load HuggingFace datasets
    3. Insert customers
    4. Insert orders
    5. Verify migration
    """
    print("=" * 60)
    print("Blackbird Data Migration: HuggingFace → SQLite")
    print("=" * 60)

    # Step 1: Initialize database schema
    print("\n[1/5] Initializing database schema...")
    init_database()

    # Step 2: Load HuggingFace datasets
    print("\n[2/5] Loading HuggingFace datasets...")
    print("  - Loading dwb2023/blackbird-customers...")
    customers = load_dataset("dwb2023/blackbird-customers", split="train")
    print(f"    ✓ Loaded {len(customers)} customers")

    print("  - Loading dwb2023/blackbird-orders...")
    orders = load_dataset("dwb2023/blackbird-orders", split="train")
    print(f"    ✓ Loaded {len(orders)} orders")

    # Step 3: Insert customers
    print("\n[3/5] Migrating customers...")
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Clear existing data
    cursor.execute("DELETE FROM orders")  # Delete orders first (foreign key constraint)
    cursor.execute("DELETE FROM customers")

    inserted_customers = 0
    for customer in customers:
        try:
            # Clean phone number (remove "updated_" prefix if present)
            phone = customer['phone'].replace('updated_', '')

            cursor.execute(
                """
                INSERT INTO customers (id, name, email, phone, username)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    customer['id'],
                    customer['name'],
                    customer['email'],
                    phone,
                    customer['username']
                )
            )
            inserted_customers += 1
        except sqlite3.IntegrityError as e:
            print(f"    ⚠ Skipped customer {customer['id']}: {e}")

    conn.commit()
    print(f"  ✓ Migrated {inserted_customers} customers")

    # Step 4: Insert orders
    print("\n[4/5] Migrating orders...")
    inserted_orders = 0
    skipped_orders = 0

    for order in orders:
        try:
            cursor.execute(
                """
                INSERT INTO orders (id, customer_id, product, quantity, price, status)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    order['id'],
                    order['customer_id'],
                    order['product'],
                    order['quantity'],
                    order['price'],
                    order['status']
                )
            )
            inserted_orders += 1
        except sqlite3.IntegrityError as e:
            print(f"    ⚠ Skipped order {order['id']}: {e}")
            skipped_orders += 1

    conn.commit()
    print(f"  ✓ Migrated {inserted_orders} orders")
    if skipped_orders > 0:
        print(f"  ⚠ Skipped {skipped_orders} orders (foreign key or duplicate errors)")

    # Step 5: Verify migration
    print("\n[5/5] Verifying migration...")

    # Count customers
    cursor.execute("SELECT COUNT(*) FROM customers")
    customer_count = cursor.fetchone()[0]
    print(f"  - Customers in database: {customer_count}")

    # Count orders
    cursor.execute("SELECT COUNT(*) FROM orders")
    order_count = cursor.fetchone()[0]
    print(f"  - Orders in database: {order_count}")

    # Verify foreign key integrity
    cursor.execute(
        """
        SELECT COUNT(*) FROM orders o
        LEFT JOIN customers c ON o.customer_id = c.id
        WHERE c.id IS NULL
        """
    )
    orphaned_orders = cursor.fetchone()[0]

    if orphaned_orders > 0:
        print(f"  ⚠ WARNING: {orphaned_orders} orders have invalid customer_id!")
    else:
        print("  ✓ All orders have valid customer references")

    # Show sample data
    print("\n" + "=" * 60)
    print("Sample Data")
    print("=" * 60)

    print("\nCustomers (first 3):")
    cursor.execute("SELECT * FROM customers LIMIT 3")
    for row in cursor.fetchall():
        print(f"  ID: {row[0]}, Name: {row[1]}, Email: {row[2]}")

    print("\nOrders (first 3):")
    cursor.execute("SELECT * FROM orders LIMIT 3")
    for row in cursor.fetchall():
        print(f"  ID: {row[0]}, Customer: {row[1]}, Product: {row[2]}, Status: {row[5]}")

    conn.close()

    # Final summary
    print("\n" + "=" * 60)
    print("Migration Complete!")
    print("=" * 60)
    print(f"✓ Database: {DATABASE_PATH}")
    print(f"✓ Customers: {customer_count}")
    print(f"✓ Orders: {order_count}")
    print("\nNext steps:")
    print("  1. Start backend: uvicorn main:app --reload")
    print("  2. View API docs: http://localhost:8000/docs")
    print("  3. Start frontend: cd frontend && npm run dev")
    print("=" * 60)


if __name__ == "__main__":
    try:
        migrate()
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
