---
name: logging
description: >
  Structured logging with structlog for Python services. Load this skill
  when adding log statements, configuring logging, choosing log levels,
  or ensuring sensitive data is never logged. Covers structlog setup,
  correlation IDs, Lambda/FastAPI integration, and what to log at each level.
---

# Logging Skill

## Templates

| Template | Use when |
|---|---|
| `templates/structlog_config.py` | Setting up structlog in a new service |
| `templates/correlation_id.py` | Adding request tracing (Lambda or FastAPI) |
| `templates/timing_wrapper.py` | Measuring operation duration |

## References

See `references/what_to_log.md` for the full always/never log guide with examples.

## Log Levels — When to Use Each

| Level | When | Example |
|---|---|---|
| `DEBUG` | Internal state useful only during development | `logger.debug("cache_key_built", key=key[:16])` |
| `INFO` | Normal operations worth recording | `logger.info("request_processed", donor_id=donor_id, duration_ms=elapsed)` |
| `WARNING` | Unexpected but recoverable situations | `logger.warning("cache_miss_fallback", tab=tab)` |
| `ERROR` | Failures that need attention | `logger.error("payment_failed", error=str(exc), donor_id=donor_id)` |
| `CRITICAL` | System-level failures, service down | `logger.critical("database_unreachable", host=db_host)` |

### Level rules of thumb
- **INFO** is the default production level — log enough to trace a request end-to-end
- **DEBUG** is noisy — only useful when actively investigating
- **WARNING** should be actionable — if nobody would act on it, it's probably DEBUG
- **ERROR** means something broke — always include enough context to diagnose

## Key-Value Style (not sentences)

```python
# GOOD — structured, searchable, parseable
logger.info("cache_hit", layer="InMemory", tab="waterfall", key=key[:16])

# BAD — unstructured sentence
logger.info(f"Found {len(df)} rows in deferral_trend_analysis query after 45ms")
```

## Rules
- Always use `structlog.get_logger()`, never `logging.getLogger()` or `print()`
- Always use key=value style, never f-string sentences
- Always include `exc_info=True` on error logs for stack traces
- Always log operation duration for external calls (DB, API, LLM)
- Always set a correlation ID at the entry point (handler/middleware)
- Never log PII, secrets, tokens, passwords, or full request bodies
- Never use `logger.exception()` outside an except block
- Never log at ERROR level for expected/handled situations (use WARNING)
