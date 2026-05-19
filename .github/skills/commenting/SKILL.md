---
name: commenting
description: >
  Google-style docstrings and inline comments for Python code. Load this
  skill when adding documentation to existing code. Covers module, class,
  function, and method docstrings plus inline comment standards.
---

# Commenting Skill

## Workflow
```
READ → MAP → WRITE → LINT → VERIFY
```

1. **READ** — read the target module(s) and see what already has docstrings
2. **MAP** — output a `<DOCSTRING_PLAN>` listing what needs docstrings vs what to skip
3. **WRITE** — add docstrings and comments per the plan
4. **LINT** — run linter after every file write
5. **VERIFY** — run tests to make sure docstrings didn't break anything

## Templates

See `templates/docstring_examples.py` for complete module, class, `__init__`, and method docstring examples in Google style.

## What to Document vs Skip

### ALWAYS document
- All public classes
- All public methods and functions
- All `__init__` methods with non-trivial parameters
- Module-level docstrings for every file
- Non-obvious algorithms (regex, bitwise ops, retry logic)
- Business rules
- Constants with non-obvious values

### NEVER document
- Simple property getters/setters (`@property` with single return)
- Private methods with self-evident names
- Test functions (test name IS the documentation)
- Obvious one-liners (`return self._items`)

## Inline Comment Rules

### Good comments explain WHY, not WHAT
```python
# Gateway requires amount in cents, not dollars
amount_cents = int(request.amount * 100)

# Using batch_writer for automatic chunking (max 25 items per batch)
with table.batch_writer() as batch:
```

### Placement
- On the line above the code, not at the end
- Section separators: `# -- Section Name --`
- Never inside comprehensions or lambdas

## Rules
- Never change function logic, signatures, or return values
- Never rename variables, functions, or classes
- Never add type annotations (that's the linting skill)
- Never remove existing comments or docstrings
- Never write docstrings that just repeat the function name
