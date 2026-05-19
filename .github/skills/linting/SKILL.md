---
name: linting
description: >
  Static analysis with ruff and mypy. Load this skill when fixing lint
  errors, formatting code, or adding type annotations. Covers fix priority,
  common rule patterns, and noqa/type-ignore guidelines.
---

# Linting Skill

## Workflow
```
SCAN → TRIAGE → FIX → VERIFY
```

1. **SCAN** — run `ruff check .` and `ruff format --check .`
2. **TRIAGE** — prioritise by severity (see below)
3. **FIX** — auto-fix first (`ruff check --fix`), then manual fixes
4. **VERIFY** — re-run linter + run tests to confirm no regressions

## Fix Priority Order
1. **Security** — `S` rules (bandit), `B` rules (bugbear)
2. **Bugs** — `F` rules (pyflakes: unused imports, undefined names)
3. **Type errors** — mypy errors (missing return types, incompatible types)
4. **Style** — `E` / `W` rules (formatting, whitespace)
5. **Complexity** — `C90` (McCabe), `PLR` (refactoring suggestions)

## Common Ruff Rules

| Rule | Description | Fix |
|---|---|---|
| `F401` | Unused import | Remove the import line |
| `F841` | Unused variable | Remove or prefix with `_` |
| `E501` | Line too long (>88 chars) | Break the line logically |
| `E711` | Comparison to None | Use `is None` / `is not None` |
| `E712` | Comparison to True/False | Use `if x:` / `if not x:` |
| `B006` | Mutable default argument | Use `None` + set in body |
| `I001` | Import not sorted | Let `ruff --fix` handle it |
| `S101` | Use of `assert` in non-test | Only flag in production code |
| `S105` | Hardcoded password | Flag as security issue |
| `C901` | Too complex (McCabe > 10) | Needs refactoring |

## Common Mypy Fixes

| Error | Fix |
|---|---|
| `Missing return statement` | Add explicit `return None` or fix control flow |
| `Incompatible return type` | Fix the return type annotation |
| `has no attribute` | Fix attribute name or add type narrowing |

## Rules
- Preserve exact semantics — a lint fix must not change behaviour
- Run tests after each batch of fixes
- Add `# noqa: XXXX` only for genuine false positives, with a reason comment
- Never add blanket `# type: ignore` without a specific error code
- Never suppress `S` (security) rules without explicit justification
- Never change function signatures to fix lint issues
- Never remove code that looks unused without checking usages first
