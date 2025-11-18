# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python 3.11 FastAPI demonstration project that uses the **SpecKit feature development framework** for structured, test-driven development. The project is currently in greenfield state with no application code yet implemented.

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

### Python Environment
- Python version: 3.11 (specified in `.python-version`)
- Package manager: Standard Python tooling (pyproject.toml)
- Dependencies: Not yet defined

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

Key governance principles:
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

## Important Notes for Claude Code

1. **This is a greenfield project** - No FastAPI application code exists yet
2. **SpecKit workflow is mandatory** - Never bypass the specify → plan → tasks → implement workflow
3. **TDD is non-negotiable** - Tests must exist and pass before implementation
4. **Constitution is authority** - Project constitution overrides all other practices
5. **Feature isolation** - Each feature gets a numbered branch and isolated spec directory
6. **Technology-agnostic specs** - Keep implementation details in plan.md, not spec.md
7. **Measurable requirements** - All success criteria must be testable

## Active Technologies
- Python 3.11 (backend), TypeScript/JavaScript (frontend with React) (001-blackbird-refactor)
- SQLite 3.x (embedded database with WAL mode for concurrency) (001-blackbird-refactor)

## Recent Changes
- 001-blackbird-refactor: Added Python 3.11 (backend), TypeScript/JavaScript (frontend with React)
