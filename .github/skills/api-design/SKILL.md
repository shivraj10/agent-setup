---
name: api-design
description: >
  REST API design patterns for FastAPI and API Gateway. Load this skill
  when designing new endpoints, error responses, pagination, filtering,
  or API versioning. Covers status codes, request/response models, and
  OpenAPI documentation.
---

# API Design Skill

## References

See `references/conventions.md` for URL naming rules and status code table.

## Templates

| Template | Use when |
|---|---|
| `templates/error_response.py` | Adding standardised error responses |
| `templates/pagination.py` | Adding paginated list endpoints |
| `templates/crud_models.py` | Defining Create / Update / Response model sets |
| `templates/health_check.py` | Adding a `/health` endpoint |

## Filtering Rules
- Optional query params for filtering
- Use Enums for fixed-value filters
- Validate date ranges (`date_from` <= `date_to`)

```python
@router.get("/deferrals")
async def list_deferrals(
    status: DeferralStatus | None = None,
    age_group: str | None = None,
    date_from: date | None = None,
    date_to: date | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    ...
```

## Rules
- Separate Create, Update, and Response models (see `templates/crud_models.py`)
- Always return `ErrorResponse` on failures (see `templates/error_response.py`)
- Always include pagination on list endpoints (see `templates/pagination.py`)
- Never expose internal error details in 500 responses
