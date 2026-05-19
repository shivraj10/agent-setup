# Project Standards

- Python 3.12+ with type hints on all public functions and methods
- Pydantic v2 models for all data structures — never raw dicts as function params
- FastAPI for HTTP routes, Mangum for Lambda integration
- structlog for logging — never use `print()`
- Google-style docstrings on all public classes, methods, and functions
- Ruff for linting and formatting (`ruff check` + `ruff format`)
- pytest for testing with ≥80% coverage target
- Conventional commit messages: `feat:`, `fix:`, `refactor:`, `docs:`, `test:`
- Never hardcode secrets, resource names, or API keys
- Never use bare `except:` — catch specific exceptions
- Prefer async/await for I/O-bound operations
- All SQL queries stored as standalone `.sql` files, loaded at runtime
- YAML for prompt templates and configuration — not inline strings

## Code Review

When performing a code review, read the acceptance criteria listed in the pull request description and verify that the code changes satisfy each criterion. Flag any acceptance criteria that are not met.

When performing a code review, check for: missing type hints, raw dicts instead of Pydantic models, `print()` instead of structlog, bare `except:` clauses, hardcoded secrets, and SQL string interpolation.

### Copilot Review Focus

- Prioritize only HIGH and CRITICAL findings (correctness, security, data loss, behavioural regressions).
- Avoid LOW-value style nits, wording suggestions, and cosmetic formatting comments.
- Do not comment on generated files, boilerplate, or non-functional docs-only changes unless there is a concrete risk.
- If no HIGH/CRITICAL issue is found, explicitly say no blocking findings instead of adding minor suggestions.
- Prefer a small number of high-signal comments over many minor comments.

## References

- [Build & Test Commands](../AGENTS.md)
- [Python Standards](instructions/python.instructions.md)
- [SQL Standards](instructions/sql.instructions.md)
- [YAML Standards](instructions/yaml.instructions.md)
- [Testing Standards](instructions/testing.instructions.md)
- [Security Standards](instructions/security.instructions.md)
- [Shared Context & Agent Boundaries](instructions/shared-context.instructions.md)
