---
name: debugging
description: >
  Systematic debugging and root cause analysis for Python applications.
  Load this skill when investigating bugs, errors, or unexpected behaviour.
  Covers log analysis, bisecting, reproducing issues, and common Python pitfalls.
---

# Debugging Skill

## Workflow
```
REPRODUCE → ISOLATE → DIAGNOSE → FIX → VERIFY
```

### 1. REPRODUCE
- Read the error message / stack trace fully before acting
- Write a minimal test case that triggers the bug
- If you can't reproduce, check: environment, data, timing, concurrency

### 2. ISOLATE
- Narrow down to the exact file, function, and line
- Use binary search: comment out half the code, see if bug persists
- Check git blame: did a recent commit introduce this?

### 3. DIAGNOSE
- Read the code around the failure — don't guess
- Check inputs: are they what you expect? (type, value, None?)
- Check state: is any shared/mutable state being modified?
- Check async: is something not awaited? Race condition?

### 4. FIX
- Fix the root cause, not the symptom
- If a None check fixes the crash but None shouldn't be possible, find WHY it's None
- Minimal change — don't refactor while fixing bugs

### 5. VERIFY
- Run the reproducing test — it should pass now
- Run the full test suite — no regressions
- Check edge cases around the fix

## Common Python Pitfalls

### Mutable default arguments
```python
# BUG: all calls share the same list
def append(item, items=[]):
    items.append(item)
    return items

# FIX:
def append(item, items=None):
    items = items or []
    items.append(item)
    return items
```

### Late binding closures
```python
# BUG: all functions return 4
funcs = [lambda: i for i in range(5)]

# FIX: capture i in default arg
funcs = [lambda i=i: i for i in range(5)]
```

### Async not awaited
```python
# BUG: coroutine never executes (no await)
async def handler():
    save_to_db(item)  # missing await!

# FIX:
async def handler():
    await save_to_db(item)
```

### Dictionary mutation during iteration
```python
# BUG: RuntimeError
for key in my_dict:
    if should_remove(key):
        del my_dict[key]

# FIX: iterate over a copy
for key in list(my_dict):
    if should_remove(key):
        del my_dict[key]
```

### Import-time side effects
```python
# BUG: module-level code runs at import, not at call time
client = boto3.client("s3")  # fails if AWS creds not set at import

# FIX: lazy init
_client = None
def get_client():
    global _client
    if _client is None:
        _client = boto3.client("s3")
    return _client
```

## Debugging Async Code
- Always check: is every coroutine awaited?
- Use `asyncio.create_task()` results — don't fire-and-forget without error handling
- Check for: task cancellation, event loop not running, mixing sync/async

## Debugging Lambda
- Check CloudWatch logs FIRST
- Verify environment variables are set
- Check IAM permissions (most common: missing DynamoDB/S3 access)
- Check timeout — is the function hitting the 30s/15min limit?
- Check memory — OOM kills look like silent failures

## Log Reading Strategy
1. Find the ERROR/EXCEPTION log entry
2. Read the full stack trace bottom-to-top
3. Find the LAST line of YOUR code (ignore framework internals)
4. Read the function at that line
5. Check what was passed to it (look at the preceding INFO logs)
