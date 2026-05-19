---
applyTo: "**/*.py"
---

# Python Code Standards

- Use `from __future__ import annotations` at the top of every module
- Type hints on all public functions, methods, and class attributes
- Pydantic v2 `BaseModel` for all data structures — never raw dicts as params
- Use `structlog` for logging — never `print()` or `logging.getLogger()`
- Google-style docstrings on all public classes, methods, and functions
- Import ordering: stdlib → third-party → local (enforced by `ruff`)
- Prefer `async def` for I/O-bound operations (DB, HTTP, LLM calls)
- Never use bare `except:` — catch specific exceptions
- Domain exceptions inherit from a module-level base exception
- Use `@dataclass` only for simple value objects; prefer Pydantic for validation
