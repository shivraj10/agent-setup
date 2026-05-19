---
name: coding
description: >
  Production-grade Python development patterns. Covers architecture layers
  (models, repository, service, handler), FastAPI routes, Lambda handlers,
  ETL pipelines, and LLM infrastructure. Load this skill when writing new
  code or modifying existing modules.
---

# Coding Skill

## Architecture Layers (top to bottom)

1. **Models** — Pydantic v2 dataclasses; no logic, just shapes
2. **Repository** — all boto3 / external I/O lives here, nowhere else
3. **Service** — business logic; depends on repository + models; no boto3
4. **Handler / Route** — thin Lambda handler or FastAPI route; delegates to service

## Code Standards
- Use `structlog` for logging, never `print()`
- Use Pydantic models for all data shapes, never raw `dict` params
- Define domain exceptions in `src/exceptions.py`
- Environment variables for all resource names (table names, bucket names, queue URLs)
- Module-level clients for connection reuse in Lambda
- No mutable default arguments
- No bare `except:` — always catch specific exceptions
- No `from module import *`

## Templates

Use the scaffolds in `templates/` as starting points for new modules:

| Template | Use when |
|---|---|
| `templates/lambda_handler.py` | Creating a new Lambda function |
| `templates/fastapi_route.py` | Adding a new FastAPI route |
| `templates/repository.py` | Adding a new data access layer |
| `templates/pydantic_model.py` | Defining a new data shape |
| `templates/domain_exceptions.py` | Adding domain-specific errors |
| `templates/etl_pipeline.py` | Building an extract/transform/load pipeline |
