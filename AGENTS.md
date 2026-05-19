# Build & Test

- Install: `pip install -e ".[dev]"` or `uv sync`
- Lint: `ruff check . --fix && ruff format .`
- Type check: `mypy src/`
- Unit tests: `pytest tests/unit/ -v --tb=short`
- Integration tests: `pytest tests/integration/ -v --tb=short`
- Coverage: `pytest --cov=src --cov-report=term-missing`
- Full check: `ruff check . && ruff format --check . && pytest tests/unit/ -v`

# Before Committing

1. Run all tests and ensure they pass
2. Run `ruff check . && ruff format --check .` — zero errors
3. Use conventional commit format: `feat:`, `fix:`, `refactor:`, `docs:`, `test:`
4. Never commit `.env`, secrets, or API keys

# Project Structure

- `src/` — application code (models, APIs, services, database, genai)
- `src/genai/smart_insight/` — AI insight pipeline (core, deferral, waterfall, deep_dive)
- `src/database/sql/` — standalone SQL query files
- `tests/unit/` — unit tests (mirror src/ structure)
- `tests/integration/` — integration tests (DB, LLM, WebSocket)
- `tools/` — developer utilities (AST tools, doc generation)

# Deployment

- SAM for Lambda packaging: `sam build && sam deploy`
- CI/CD: `.github/workflows/` (dev, test, prod pipelines)

# Jira Ticket Lifecycle

Agents manage Jira transitions through the SDLC:

- `To Do` → `In Progress`: Planner (workable tickets only)
- `In Progress` → `Test`: Pre-PR Review (when PR is opened and review passes)
- `Test` → `Done`: Documentation Agent (after merge + Confluence update)
- Non-workable tickets remain in `To Do` with a comment explaining what's missing

# Workflow Paths

- **Path A (Full lifecycle):** Confluence/PRD → Product Owner → Jira Stories → Planner Triage → Developer → Tester → Pre-PR Review → PR → Documentation Agent → Done
- **Path B (Existing ticket):** Jira ticket → Planner Triage (`triage-ticket.prompt.md`) → Developer → Tester → Pre-PR Review → PR → Documentation Agent → Done
- **Path C (Quick planning):** Feature description → `plan-feature.prompt.md` → Planner (skips formal ticket creation, used for exploration/estimation)
- **Path D (Post-merge):** Merged PR → `post-merge.prompt.md` → Documentation Agent → Confluence update + Jira closure
