# What to Log vs Never Log

## ALWAYS log
- Entry/exit of key operations
- External calls (API, DB, LLM) with duration
- Errors with context and `exc_info=True`
- State transitions with old/new values

```python
logger.info("insight_generation_started", tab=tab, params_count=len(params))
logger.info("insight_generation_completed", tab=tab, duration_ms=elapsed, from_cache=cached)
logger.info("llm_request_sent", model=model, prompt_tokens=token_count)
logger.error("query_execution_failed", query=query_name, error=str(exc), exc_info=True)
logger.info("deferral_status_changed", deferral_id=did, old_status=old, new_status=new)
```

## NEVER log
- PII: SSN, email, name, phone, address
- Credentials: passwords, API keys, tokens, secrets
- Full request/response bodies (may contain PII)

## Safe alternatives
```python
# Log IDs, not values
logger.info("donor_created", donor_id=donor.id)

# Log counts, not contents
logger.info("batch_processed", record_count=len(records))

# Mask if you must reference
logger.info("api_key_used", key_suffix=api_key[-4:])
```
