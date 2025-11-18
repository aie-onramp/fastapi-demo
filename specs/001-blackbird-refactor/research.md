# Research & Technical Decisions: Blackbird Refactor

**Feature**: 001-blackbird-refactor
**Date**: 2025-11-17
**Phase**: 0 - Research & Discovery

## Overview

This document captures research findings and technical decisions made during the planning phase for refactoring the Blackbird customer support application from HuggingFace Spaces (Gradio + HF datasets) to a modern web stack (React + FastAPI + SQLite).

## Research Areas

### 1. HuggingFace Dataset Schema Analysis

**Research Question**: What is the exact structure of the existing data that must be migrated?

**Findings**:
- **Customers Dataset** (`dwb2023/blackbird-customers`):
  - 10 records, 3.32 kB
  - Fields: `id` (TEXT), `name` (TEXT), `email` (TEXT), `phone` (TEXT), `username` (TEXT)
  - All fields populated, no nulls
  - Email and username appear to have uniqueness constraints (based on current data)

- **Orders Dataset** (`dwb2023/blackbird-orders`):
  - 13 records, 3.63 kB
  - Fields: `id` (TEXT), `customer_id` (TEXT FK), `product` (TEXT), `quantity` (INTEGER), `price` (FLOAT), `status` (TEXT)
  - Status values: "Processing", "Shipped", "Delivered", "Cancelled"
  - One-to-many relationship: customers → orders via `customer_id`

**Decision**: Use identical schema in SQLite with proper constraints (PRIMARY KEY, FOREIGN KEY, UNIQUE, CHECK) to maintain data integrity during and after migration.

**Rationale**: Preserving the exact schema ensures zero data loss and maintains compatibility with existing Claude AI function calling tools that reference these fields.

**Alternatives Considered**:
- Normalizing orders into order_items table: Rejected - current simple schema adequate for scope (SC-006: up to 10,000 records)
- Using integer IDs: Rejected - existing IDs are strings; migration would require ID mapping and tool updates

---

### 2. SQLite Concurrency Strategy

**Research Question**: How can SQLite handle 50 concurrent connections (NFR-003) when it's traditionally single-writer?

**Findings**:
- SQLite default journal mode supports 1 writer + multiple readers
- Write-Ahead Logging (WAL) mode enables 1 writer + unlimited concurrent readers
- WAL mode provides better concurrency and performance for read-heavy workloads
- Read operations do not block each other in WAL mode
- Write operations complete faster in WAL mode

**Decision**: Enable WAL mode for SQLite database with connection pooling.

**Implementation**:
```python
# database/session.py
SQLALCHEMY_DATABASE_URL = "sqlite:///./database/blackbird.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={
        "check_same_thread": False,
        "timeout": 30
    },
    pool_pre_ping=True,
    pool_size=50,
    max_overflow=10
)

# Enable WAL mode
with engine.connect() as conn:
    conn.execute(text("PRAGMA journal_mode=WAL"))
    conn.execute(text("PRAGMA synchronous=NORMAL"))
```

**Rationale**: WAL mode is specifically designed for applications with concurrent readers, which matches our use case (customer support agents reading data while AI performs occasional writes).

**Alternatives Considered**:
- PostgreSQL: Rejected - adds deployment complexity, violates simplicity principle; SQLite adequate for stated scale
- Connection limiting middleware: Rejected - doesn't solve underlying single-writer limitation

---

### 3. React State Management for Chat

**Research Question**: What's the best approach for managing conversational state in the React chat interface?

**Findings**:
- Chat requires: message history, streaming responses, optimistic updates, error handling
- Options evaluated:
  1. **TanStack Query (React Query)**: Server state management with caching, automatic refetching
  2. **Zustand**: Lightweight client state management
  3. **Redux Toolkit**: Full-featured state management with Redux DevTools
  4. **Context API**: Built-in React state management

**Decision**: Use TanStack Query for server state + React useState/useReducer for local chat UI state.

**Rationale**:
- TanStack Query excels at server state synchronization (customer/order data fetching)
- Chat message history can use local state since it's session-specific
- Avoids complexity of Redux for a relatively simple UI
- TanStack Query provides automatic retries, caching, and background updates for data tables

**Alternatives Considered**:
- Redux Toolkit: Rejected - overkill for application scope; adds boilerplate
- Zustand only: Rejected - doesn't provide server state sync features (caching, refetching)
- Context API only: Rejected - requires manual implementation of caching/refetching logic

---

### 4. Claude AI Function Calling Integration

**Research Question**: How should we structure the AI service to maintain compatibility with existing function calling tools?

**Findings**:
- Existing system has 6 tools: `get_user`, `get_order_by_id`, `get_customer_orders`, `cancel_order`, `update_user_contact`, `get_user_info`
- Tools are defined with JSON schemas in `tool_handler.py`
- Current implementation makes HTTP POST requests to external FastAPI service
- Claude SDK expects tool schemas + execution callback

**Decision**: Refactor tool handler to call local service layer directly instead of HTTP requests.

**Architecture**:
```
Chat Endpoint → ChatService → Claude API (with tools)
                             ↓ (tool use)
                        ToolHandler → CustomerService/OrderService → Database
                             ↓ (tool result)
                        Claude API → Response
```

**Rationale**:
- Eliminates network hop (external API → local service)
- Simplifies error handling and transaction management
- Maintains identical tool schemas for Claude API compatibility
- Allows tools to participate in database transactions

**Alternatives Considered**:
- Keep HTTP-based tools: Rejected - adds latency, requires running two services, complicates local development
- Merge tools directly into chat endpoint: Rejected - violates separation of concerns, makes testing harder

---

### 5. Frontend Build Tool Selection

**Research Question**: Which build tool provides the best developer experience for React + TypeScript?

**Findings**:
- **Vite**: Modern build tool, instant HMR, optimized for frontend frameworks, native ESM
- **Create React App (CRA)**: Traditional React bootstrapper, webpack-based, slower builds
- **Next.js**: React framework with SSR/SSG, adds complexity for SPA needs
- **Parcel**: Zero-config bundler, good but less ecosystem support than Vite

**Decision**: Use Vite for frontend build tooling.

**Rationale**:
- Lightning-fast Hot Module Replacement (HMR) improves developer experience
- Out-of-box TypeScript support without configuration
- Optimized production builds with code splitting
- Large ecosystem and active development
- Perfect for SPA (Single Page Application) requirements

**Alternatives Considered**:
- CRA: Rejected - slow development server, webpack configuration complexity
- Next.js: Rejected - SSR/SSG features unnecessary for authenticated internal tool
- Parcel: Rejected - smaller ecosystem, less community support than Vite

---

### 6. API Testing Strategy

**Research Question**: How should we implement comprehensive API testing per constitution requirement for contract tests?

**Findings**:
- Constitution requires contract tests for library interfaces (adapted to API endpoints)
- pytest provides fixtures, parametrization, and async support
- FastAPI has `TestClient` for synchronous testing
- `httpx.AsyncClient` for asynchronous endpoint testing
- OpenAPI schema auto-generated by FastAPI can validate request/response contracts

**Decision**: Three-tier testing approach:
1. **Contract Tests**: Validate API contracts (request/response schemas, status codes, OpenAPI compliance)
2. **Integration Tests**: Test database interactions, AI tool execution, data migration
3. **Unit Tests**: Test individual services, models, utilities

**Structure**:
```
tests/
├── contract/
│   ├── test_customer_api.py    # POST/GET/PUT endpoints, schema validation
│   ├── test_order_api.py        # Order CRUD + cancellation business logic
│   └── test_chat_api.py         # Chat endpoint, tool invocation flow
├── integration/
│   ├── test_database.py         # SQLAlchemy models, transactions, concurrency
│   ├── test_ai_tools.py         # Tool handler with mocked Claude API
│   └── test_data_migration.py   # HF dataset → SQLite migration
└── unit/
    ├── test_models.py            # Model validation, relationships
    ├── test_services.py          # Service layer logic
    └── test_schemas.py           # Pydantic schema validation
```

**Rationale**:
- Contract tests ensure API stability (critical for frontend integration)
- Integration tests verify end-to-end flows without external dependencies
- Unit tests provide fast feedback for business logic
- Aligns with constitution's testing requirements adapted for web APIs

**Alternatives Considered**:
- Only integration tests: Rejected - slower, harder to diagnose failures
- External API testing tools (Postman, Insomnia): Rejected - requires manual maintenance, not in CI/CD pipeline

---

### 7. Data Migration Approach

**Research Question**: What's the safest way to migrate data from HuggingFace datasets to SQLite?

**Findings**:
- HuggingFace `datasets` library provides Python API to load datasets
- Current data is small (10 customers, 13 orders) but process should scale
- Need idempotency (can re-run without duplicates)
- Need validation (confirm all data migrated correctly)

**Decision**: Create standalone migration script with validation and rollback support.

**Process**:
1. Create empty SQLite database with schema
2. Load HF datasets using `datasets.load_dataset()`
3. Validate data before insertion (check required fields, referential integrity)
4. Insert data in transaction (customers first, then orders)
5. Validate post-migration (record counts, sample data verification)
6. Generate migration report

**Migration Script**:
```python
# backend/src/database/migrations/migrate_from_hf.py
def migrate_from_huggingface():
    # Load datasets
    customers_ds = load_dataset("dwb2023/blackbird-customers", split="train")
    orders_ds = load_dataset("dwb2023/blackbird-orders", split="train")

    # Validate
    validate_dataset_integrity(customers_ds, orders_ds)

    # Migrate in transaction
    with Session() as session:
        migrate_customers(session, customers_ds)
        migrate_orders(session, orders_ds)
        session.commit()

    # Verify
    verify_migration_success()
```

**Rationale**:
- Transactional approach ensures atomicity (all-or-nothing)
- Validation steps catch data quality issues early
- Idempotency allows safe re-runs during development/testing
- Meets SC-005: 100% data integrity requirement

**Alternatives Considered**:
- SQL dump/import: Rejected - HF datasets are Parquet files, not SQL
- Manual CSV export: Rejected - error-prone, not automated, doesn't scale

---

## Technology Stack Summary

### Backend
- **Framework**: FastAPI 0.111+
- **Database**: SQLite 3.x with WAL mode
- **ORM**: SQLAlchemy 2.x
- **AI Integration**: Anthropic SDK (Claude 3.5 Sonnet)
- **Testing**: pytest, httpx
- **Validation**: Pydantic v2

### Frontend
- **Framework**: React 18+
- **Language**: TypeScript 5.x
- **Build Tool**: Vite 5.x
- **State Management**: TanStack Query v5 + React hooks
- **Styling**: Tailwind CSS 3.x
- **Testing**: Vitest, React Testing Library, Playwright
- **HTTP Client**: Axios

### Development Tools
- **Package Management**: pip (backend), npm (frontend)
- **Code Quality**: Ruff (backend linting), ESLint (frontend)
- **Type Checking**: mypy (backend), TypeScript compiler (frontend)
- **Containerization**: Docker + docker-compose (optional, for deployment)

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| SQLite concurrency limits | Low | High | WAL mode + connection pooling; monitoring for write contention |
| Claude API rate limiting | Medium | Medium | Implement request queuing; display "Ruh roh Raggy!" message per existing pattern |
| Data migration failures | Low | High | Extensive validation + rollback support; dry-run mode |
| Frontend/backend contract mismatch | Medium | Medium | OpenAPI schema generation + contract tests; shared TypeScript types |
| Browser compatibility issues | Low | Low | Target modern browsers (Chrome 90+); Vite handles transpilation |

---

## Open Questions

**None** - All technical clarifications resolved during research phase.

---

## References

- [SQLite WAL Mode Documentation](https://www.sqlite.org/wal.html)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Anthropic Claude API](https://docs.anthropic.com/claude/reference/messages)
- [TanStack Query Guide](https://tanstack.com/query/latest)
- [React Testing Best Practices](https://react.dev/learn/testing)
- [HuggingFace Datasets Library](https://huggingface.co/docs/datasets/)

---

**Phase 0 Completion**: All technical unknowns resolved. Ready to proceed to Phase 1 (Design & Contracts).
