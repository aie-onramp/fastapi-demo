# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python 3.11 FastAPI demonstration project for the AI Engineering Onramp course. Uses the **SpecKit feature development framework** for structured, test-driven development.

**Current Status**: Specification and planning phase for feature 001-blackbird-refactor (React + FastAPI + SQLite customer support app with Claude AI integration).

**Core Educational Objective**: Teaching Claude AI function calling integration with modern web development (React frontend + FastAPI backend).

## SpecKit Workflow (MANDATORY)

All feature development MUST follow the SpecKit phase-based workflow:

### Feature Development Commands

1. **`/speckit.specify`** - Create feature specification from natural language description
   - Outputs: `specs/###-feature-name/spec.md`
   - Focus: WHAT and WHY (technology-agnostic, stakeholder-focused)

2. **`/speckit.clarify`** - Identify underspecified areas and encode clarifications
   - Asks up to 5 targeted questions
   - Updates spec.md with answers

3. **`/speckit.plan`** - Generate technical implementation plan
   - Outputs: `plan.md`, `research.md`, `data-model.md`, `contracts/`
   - Focus: HOW (technical details, architecture decisions)

4. **`/speckit.tasks`** - Create dependency-ordered task breakdown
   - Outputs: `tasks.md`
   - Dependency analysis with parallelization opportunities

5. **`/speckit.analyze`** - Cross-artifact consistency and quality analysis
   - Runs AFTER task generation
   - Validates spec.md ↔ plan.md ↔ tasks.md consistency

6. **`/speckit.implement`** - Execute implementation plan
   - Processes all tasks from tasks.md
   - Follows TDD workflow (tests first, then implementation)

7. **`/speckit.checklist`** - Generate custom validation checklist

8. **`/speckit.taskstoissues`** - Convert tasks to GitHub issues

9. **`/speckit.constitution`** - Update project constitution

## Development Commands

### Feature Management
```bash
# Create new feature branch and spec structure
.specify/scripts/bash/create-new-feature.sh <feature-number> <feature-name>

# Setup implementation planning
.specify/scripts/bash/setup-plan.sh

# Validate feature prerequisites
.specify/scripts/bash/check-prerequisites.sh
```

### Python Development
```bash
# Ensure Python 3.11 is active (check .python-version)
python --version

# Backend setup (when backend/ exists)
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Environment setup
cp ../.env.example ../.env
# Edit .env and add your ANTHROPIC_API_KEY from https://console.anthropic.com/

# Data migration (HuggingFace → SQLite) - run BEFORE starting server
python migrate_data.py

# Run FastAPI development server (from backend/ directory)
uvicorn main:app --reload --port 8000

# Run tests (when tests/test_api.py exists)
pytest tests/ -v
pytest tests/test_api.py -v  # Run specific test file
pytest tests/test_api.py::test_function_name -v  # Run single test
pytest --cov=. --cov-report=html  # Run with coverage

# Linting and formatting (ruff is in requirements.txt)
ruff check .  # Check code
ruff format .  # Format code
```

### Frontend Development
```bash
# Frontend setup (when frontend/ exists)
cd frontend
npm install

# Run Vite development server (opens at http://localhost:5173)
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Linting
npm run lint
```

### Environment Variables
```bash
# Copy template and configure
cp .env.example .env

# Required variables in .env:
# ANTHROPIC_API_KEY=sk-ant-api03-your-key-here  # Get from https://console.anthropic.com/
# DATABASE_URL=sqlite:///./blackbird.db
# ENVIRONMENT=development
```

## Architecture Principles (Constitutional)

### 1. Library-First Design
- All features start as standalone, reusable libraries
- Enables composition and independent testing

### 2. CLI Text I/O Protocol
- Input: stdin or command-line arguments
- Output: stdout (structured text)
- Ensures debuggability and observability

### 3. Test-Driven Development (NON-NEGOTIABLE)
- Write tests BEFORE implementation
- Get test approval BEFORE writing production code
- Integration tests for library interfaces
- No exceptions to TDD workflow

### 4. Documentation Separation
- **spec.md**: Technology-agnostic requirements (WHAT/WHY)
- **plan.md**: Technical implementation details (HOW)
- **tasks.md**: Execution plan with dependencies
- Keep implementation details OUT of spec.md

## Project Structure

### Feature Branch Pattern
```
###-feature-name/          # Numbered feature branch
└── specs/
    └── ###-feature-name/
        ├── spec.md        # Requirements specification
        ├── plan.md        # Technical implementation plan
        ├── tasks.md       # Dependency-ordered tasks
        ├── research.md    # Technical decisions & rationale
        ├── data-model.md  # Entities & relationships
        ├── contracts/     # API specifications & test requirements
        └── checklists/    # Quality validation checklists
```

### Progressive Context Loading
- Load only necessary artifacts for each phase
- Avoid loading all specs simultaneously
- Each feature is isolated in its own directory

## Constitutional Governance

The project constitution (`.specify/memory/constitution.md`) defines core principles, constraints, and governance rules that take **precedence over all other practices**.

**Note**: Constitution file is currently a template. Use `/speckit.constitution` to create or update it based on project principles.

Key governance principles enforced by SpecKit:
- Test-first development is mandatory
- All requirements must be measurable and testable
- Success criteria must be unambiguous
- Constitution compliance is checked during `/speckit.analyze`

## MCP Servers Available

The following MCP servers are configured for documentation access:
- **mcp-server-time**: Timezone and time conversion
- **sequential-thinking**: Sequential thinking workflows
- **Context7**: Library documentation from Upstash
- **ai-docs-server**: MCP, FastMCP, LangChain, LangGraph, Anthropic docs
- **ai-docs-server-full**: Full versions of above documentation

## Current Feature: 001-blackbird-refactor

**Branch**: `001-blackbird-refactor`

**Goal**: Refactor Gradio + HuggingFace customer support app → React + FastAPI + SQLite

**Current Status** (as of 2025-11-17, updated 2025-11-17):
- ✅ Phase 1: Project setup complete (T001-T008)
- ✅ Phase 2: Data layer complete (T009-T011) - database.py, models.py, migrate_data.py fully implemented
- ✅ Phase 3: Backend API complete (T012-T018) - main.py (13 endpoints), ai_tools.py (6 Claude tools), models.py (~1000 LOC total)
- ✅ Phase 4: Frontend complete (T019-T026) - All 3 pages (ChatPage, CustomersPage, OrdersPage) + 3 reusable components (~600 LOC)
- ❌ **CRITICAL GAP**: backend/tests/ directory is EMPTY - NO tests exist despite TDD being "NON-NEGOTIABLE" in constitution
- 📋 See `specs/001-blackbird-refactor/tasks.md` for complete task list

**⚠️ TESTING REQUIREMENT VIOLATION**: This project mandates Test-Driven Development but contains zero test files. Future work should prioritize creating the test suite described in `specs/001-blackbird-refactor/contracts/`.

**Architecture** (per `specs/001-blackbird-refactor/plan.md`):
- **Backend**: 5 files (~1000 LOC) - ✅ FULLY IMPLEMENTED
  - [backend/main.py](backend/main.py) - FastAPI app with 13 REST endpoints (~260 LOC)
  - [backend/models.py](backend/models.py) - Pydantic schemas with validation (~236 LOC)
  - [backend/ai_tools.py](backend/ai_tools.py) - Claude AI integration + 6 function calling tools (~354 LOC)
  - [backend/database.py](backend/database.py) - SQLite CRUD operations (~338 LOC)
  - [backend/migrate_data.py](backend/migrate_data.py) - HuggingFace → SQLite migration (~181 LOC)
- **Frontend**: 8 files (~600 LOC) - ✅ FULLY IMPLEMENTED - React 18 + Vite, 3 pages (Chat, Customers, Orders), 3 reusable components
  - [frontend/src/App.jsx](frontend/src/App.jsx) - React Router navigation
  - [frontend/src/api.js](frontend/src/api.js) - 6 API wrapper functions
  - [frontend/src/pages/ChatPage.jsx](frontend/src/pages/ChatPage.jsx) - Chat interface with Claude AI
  - [frontend/src/pages/CustomersPage.jsx](frontend/src/pages/CustomersPage.jsx) - Customer management with inline edit
  - [frontend/src/pages/OrdersPage.jsx](frontend/src/pages/OrdersPage.jsx) - Order management with status filtering
  - [frontend/src/components/](frontend/src/components/) - DataTable, SearchBar, ChatMessage components
- **Database**: SQLite with 2 tables (customers, orders) - NO conversation history storage (educational simplification)

**Key Endpoints**:
- `POST /api/chat` - Claude AI integration with function calling
- `GET/PATCH /api/customers/*` - Customer CRUD
- `GET/PATCH /api/orders/*` - Order management

**6 Claude AI Tools** (primary learning objective):
1. `get_user` - Search by email/phone/username
2. `get_order_by_id` - Order lookup
3. `get_customer_orders` - Customer's order history
4. `cancel_order` - Cancel if Processing
5. `update_user_contact` - Update email/phone
6. `get_user_info` - Customer + orders combined

See `specs/001-blackbird-refactor/plan.md` for complete technical details.

## Important Notes for Claude Code

1. **Educational focus** - This is a teaching application for AI Engineering Onramp, not production code
2. **SpecKit workflow is mandatory** - Never bypass the specify → plan → tasks → implement workflow
3. **TDD is non-negotiable** - Tests must exist and pass before implementation
4. **Simplicity over architecture** - Removed layered architecture, logging, monitoring to focus on AI integration
5. **Feature isolation** - Each feature gets a numbered branch and isolated spec directory
6. **Technology-agnostic specs** - Keep implementation details in plan.md, not spec.md
7. **Measurable requirements** - All success criteria must be testable

## Active Technologies
- Python 3.11 (backend)
- JavaScript/React 18 (frontend with Vite)
- FastAPI (web framework)
- SQLite 3.x (embedded database)
- Anthropic Claude API (AI function calling)
