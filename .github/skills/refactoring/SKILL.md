---
name: refactoring
description: >
  Behaviour-preserving code refactoring. Load this skill when restructuring
  existing code without changing external behaviour. Covers extract method,
  polymorphic dispatch, rename, dead code removal, and the one-at-a-time rule.
---

# Refactoring Skill

## Workflow
```
BASELINE → ANALYSE → PLAN → REFACTOR → VERIFY
```

1. **BASELINE** — run tests first. If they fail, STOP. Do not refactor on a red baseline.
2. **ANALYSE** — identify long functions (>30 lines), deep nesting (3+ levels), duplicated code
3. **PLAN** — output a `<REFACTOR_PLAN>` listing each refactoring in execution order
4. **REFACTOR** — apply ONE refactoring at a time, run tests after EACH one
5. **VERIFY** — all tests pass, coverage not decreased, no new lint issues

## Refactoring Catalogue

### Extract Method
```python
# BEFORE: 45-line function
def process_order(self, order):
    # ... 20 lines discount ...
    # ... 15 lines tax ...
    # ... 10 lines shipping ...

# AFTER: composed from small methods
def process_order(self, order):
    discount = self._calculate_discount(order)
    tax = self._calculate_tax(order, discount)
    shipping = self._calculate_shipping(order)
    return OrderResult(discount=discount, tax=tax, shipping=shipping)
```

### Replace Conditional with Polymorphism
```python
# BEFORE: 5-branch if/elif
if order.type == "standard": ...
elif order.type == "express": ...

# AFTER: dispatch table
processors = {"standard": StandardProcessor(), "express": ExpressProcessor()}
processors[order.type].process(order)
```

### Simplify Conditionals
```python
if condition == True:      # -> if condition:
if not x == y:             # -> if x != y:
if len(items) > 0:         # -> if items:
```

### Remove Dead Code
- Verify with `search_codebase` before deleting anything

## Rules
- **One-at-a-time**: apply one refactoring, run tests, then next
- **Baseline rule**: never refactor on a failing test suite
- **Coverage rule**: coverage must not decrease
- **Interface rule**: never change public method signatures
- Never add features during refactoring
- Never refactor test files — tests are the safety net
- Never introduce new dependencies
