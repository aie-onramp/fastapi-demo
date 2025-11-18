# Implementation Tasks: Blackbird Customer Support Application Refactor

**Feature**: 001-blackbird-refactor
**Branch**: `001-blackbird-refactor`
**Generated**: 2025-11-17

## Summary

**Total Tasks**: 27
**User Stories**: 3 (US1-P1, US2-P2, US3-P2)
**Parallel Opportunities**: 15 tasks
**Estimated LOC**: ~1,600 (800 backend, 600 frontend, 200 tests)

**Educational Focus**: Claude AI function calling integration with modern web stack (FastAPI + React + SQLite)

## Implementation Strategy

**MVP Scope** (Week 1): User Story 1 (P1) only
- Delivers core value: AI-powered customer support chat
- ~800 LOC (backend + minimal frontend)
- Independently testable and deployable

**Incremental Delivery**:
1. **Sprint 1** (Week 1): US1 - Chat interface with Claude AI (MVP)
2. **Sprint 2** (Week 2): US2 + US3 - Customer & Order management UIs

## Phase 1: Setup & Project Initialization

**Goal**: Initialize project structure, dependencies, and environment

**Tasks**:
- [x] T001 Create backend directory structure (backend/, backend/tests/)
- [x] T002 Create frontend directory structure (frontend/src/, frontend/src/pages/, frontend/src/components/)
- [x] T003 [P] Create backend/requirements.txt with dependencies (fastapi, anthropic, pydantic, uvicorn, datasets, pytest)
- [x] T004 [P] Create frontend/package.json with dependencies (react, react-router-dom, vite)
- [x] T005 [P] Create .env.example with ANTHROPIC_API_KEY placeholder
- [x] T006 [P] Create .gitignore for Python, Node, and SQLite files
- [x] T007 [P] Create backend/README.md with setup instructions
- [x] T008 [P] Create frontend/README.md with dev server instructions

## Phase 2: Foundational - Data Layer

**Goal**: Set up database, migrations, and data models (blocking for all user stories)

**Tasks**:
- [x] T009 Implement SQLite schema creation in backend/database.py
- [x] T010 Implement database connection function get_db() in backend/database.py
- [x] T011 Implement data migration script backend/migrate_data.py (HuggingFace → SQLite)
- [x] T012 Run migration to populate blackbird.db with 10 customers and 13 orders
- [x] T013 [P] Define Pydantic models in backend/models.py (Customer, Order, ChatMessage, ChatResponse)
- [x] T014 [P] Implement basic CRUD SQL functions in backend/database.py (get_customer, update_customer, get_order, etc.)

**Validation**: Run `python backend/migrate_data.py` and verify blackbird.db contains 10 customers, 13 orders

## Phase 3: User Story 1 (P1) - AI-Powered Chat Interface

**Story Goal**: Customer support agents can use AI chat to look up customers, view orders, and cancel orders

**Independent Test**: Open chat UI, ask "Look up customer with email john@example.com", verify AI retrieves and displays customer info with orders, can cancel Processing orders

**Tasks**:

### Backend - Claude AI Integration
- [x] T015 [US1] Define 6 Claude AI tool schemas in backend/ai_tools.py (get_user, get_order_by_id, get_customer_orders, cancel_order, update_user_contact, get_user_info)
- [x] T016 [US1] Implement tool execution function execute_tool() in backend/ai_tools.py
- [x] T017 [US1] Implement Claude API integration chat_with_claude() in backend/ai_tools.py
- [x] T018 [US1] Create POST /api/chat endpoint in backend/main.py

### Frontend - Chat UI
- [x] T019 [P] [US1] Create ChatMessage component in frontend/src/components/ChatMessage.jsx
- [x] T020 [US1] Implement ChatPage with message history and input in frontend/src/pages/ChatPage.jsx
- [x] T021 [US1] Implement sendChatMessage() in frontend/src/api.js

### Integration
- [x] T022 [US1] Create FastAPI app initialization in backend/main.py with CORS
- [x] T023 [US1] Create React App component with routing in frontend/src/App.jsx
- [x] T024 [US1] Create frontend/index.html entry point
- [x] T025 [US1] Create frontend/vite.config.js with proxy to backend

**Manual Test Scenarios**:
1. Start backend: `uvicorn backend.main:app --reload`
2. Start frontend: `cd frontend && npm run dev`
3. Open http://localhost:5173
4. Chat: "Look up customer with email john@example.com" → Verify customer data displayed
5. Chat: "What are their orders?" → Verify order list displayed
6. Chat: "Cancel order 47652" (Processing status) → Verify cancellation confirmed
7. Chat: "Cancel order 24601" (Shipped status) → Verify error message

**Story Complete**: ✅ Chat interface functional, Claude AI executes all 6 tools correctly

---

## Phase 4: User Story 2 (P2) - Customer Data Management

**Story Goal**: Support agents can view, search, and update customer information via dedicated UI

**Independent Test**: Open customers page, search for customer by email, update phone number, verify changes persist in database

**Tasks**:

### Backend - Customer API
- [x] T026 [P] [US2] Create GET /api/customers endpoint in backend/main.py
- [x] T027 [P] [US2] Create POST /api/customers/search endpoint in backend/main.py
- [x] T028 [P] [US2] Create PATCH /api/customers/{id} endpoint in backend/main.py
- [x] T029 [P] [US2] Create GET /api/customers/{id}/orders endpoint in backend/main.py

### Frontend - Customer UI
- [x] T030 [P] [US2] Create SearchBar component in frontend/src/components/SearchBar.jsx
- [x] T031 [P] [US2] Create DataTable component in frontend/src/components/DataTable.jsx
- [x] T032 [US2] Implement CustomersPage with search and table in frontend/src/pages/CustomersPage.jsx
- [x] T033 [US2] Implement customer API functions in frontend/src/api.js (fetchCustomers, searchCustomers, updateCustomer)

**Manual Test Scenarios**:
1. Navigate to /customers
2. View customer list → Verify 10 customers displayed in table
3. Search by email "john@example.com" → Verify filtered results
4. Click edit on customer row → Update phone number → Verify save
5. View customer's orders in same view → Verify related orders shown

**Story Complete**: ✅ Customer management UI functional, CRUD operations work

---

## Phase 5: User Story 3 (P2) - Order Management

**Story Goal**: Support agents can view, search, filter, and cancel orders via dedicated UI

**Independent Test**: Open orders page, filter by status "Processing", cancel an order, verify status changes to "Cancelled"

**Tasks**:

### Backend - Order API
- [x] T034 [P] [US3] Create GET /api/orders endpoint in backend/main.py with status filtering
- [x] T035 [P] [US3] Create GET /api/orders/{id} endpoint in backend/main.py
- [x] T036 [P] [US3] Create PATCH /api/orders/{id}/cancel endpoint in backend/main.py (with Processing status validation)

### Frontend - Order UI
- [x] T037 [US3] Implement OrdersPage with status filter and cancel button in frontend/src/pages/OrdersPage.jsx (reuse DataTable component)
- [x] T038 [US3] Implement order API functions in frontend/src/api.js (fetchOrders, cancelOrder)

**Manual Test Scenarios**:
1. Navigate to /orders
2. View all orders → Verify 13 orders displayed
3. Filter by status "Processing" → Verify only Processing orders shown
4. Click cancel on order → Verify confirmation, status changes to Cancelled
5. Try to cancel Shipped order → Verify error message

**Story Complete**: ✅ Order management UI functional, cancellation logic works

---

## Phase 6: Polish & Cross-Cutting Concerns

**Goal**: Add finishing touches, error handling, and basic API tests

**Tasks**:
- [ ] T039 [P] Add error handling to all API endpoints in backend/main.py (try/except, HTTP status codes)
- [ ] T040 [P] Add loading states to frontend pages (during API calls)
- [ ] T041 [P] Add basic navigation menu to frontend/src/App.jsx (links to Chat, Customers, Orders)
- [ ] T042 [P] Create backend/tests/conftest.py with pytest fixtures
- [ ] T043 [P] Create backend/tests/test_api.py with basic API contract tests (test_chat_endpoint, test_get_customers, test_cancel_order)
- [ ] T044 Run pytest backend/tests/ and verify all tests pass
- [ ] T045 Update project README.md with quickstart instructions

**Validation**: All API tests pass, all pages navigable, error states handled gracefully

---

## Task Dependencies (Execution Order)

```
Phase 1 (Setup): T001-T008 [All Parallel]
  ↓
Phase 2 (Foundation): T009 → T010 → T011 → T012 (sequential)
                       T013, T014 [Parallel after T010]
  ↓
┌─────────────────┬─────────────────┬─────────────────┐
│   Phase 3 (US1) │   Phase 4 (US2) │   Phase 5 (US3) │
│   T015-T025     │   T026-T033     │   T034-T038     │
│   (Sequential   │   (Parallel     │   (Parallel     │
│    within)      │    with US1)    │    with US1)    │
└─────────────────┴─────────────────┴─────────────────┘
  ↓
Phase 6 (Polish): T039-T045 [Parallel]
```

**Critical Path**: T001 → T009 → T010 → T011 → T012 → T015 → T016 → T017 → T018 → T020 → T025 (US1 completion)

**Parallel Execution Examples**:

**Week 1 - US1 Focus (MVP)**:
- Day 1: T001-T008 (setup), T009-T014 (database)
- Day 2: T015-T018 (Claude AI backend)
- Day 3: T019-T021 (Chat frontend components)
- Day 4: T022-T025 (integration, testing)

**Week 2 - US2 & US3 (Parallel)**:
- Day 1: T026-T029 (Customer API) + T034-T036 (Order API) in parallel
- Day 2: T030-T031 (shared components)
- Day 3: T032-T033 (Customer UI) + T037-T038 (Order UI) in parallel
- Day 4: T039-T045 (polish & testing)

## Removed from Scope

**User Story 4 (P3) - Conversation History**: Not implemented per educational simplifications (plan.md line 30). Chat is stateless like original Gradio app. No database tables for conversations/messages.

## Notes

- **No TDD**: Tests are minimal (basic API contract tests only). Manual testing for UI per plan.md line 23
- **No TypeScript**: Using JavaScript for simpler learning curve
- **No Advanced State Management**: Basic React useState, no TanStack Query/Redux
- **Flat Architecture**: All FastAPI routes in main.py, no services layer
- **Educational Focus**: Every task teaches AI integration, REST APIs, or React basics

## Task Validation Checklist

✅ All tasks follow format: `- [ ] [TID] [P?] [Story?] Description with file path`
✅ User stories organized in priority order (P1 → P2 → P2)
✅ Each story independently testable
✅ MVP scope clearly defined (US1 only)
✅ Parallel opportunities identified (15 tasks marked [P])
✅ Dependencies documented
✅ File paths specified for all implementation tasks
✅ Manual test scenarios included per story
