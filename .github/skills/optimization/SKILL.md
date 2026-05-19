---
name: optimization
description: >
  Code optimization for Python services. Load this skill when improving
  performance, reducing memory usage, speeding up queries, or reducing
  Lambda cold starts. Always measure before and after — never optimize
  without proof that the code is actually slow.
---

# Optimization Skill

## Golden Rule
**Measure first. Optimize second.**
Never guess where the bottleneck is — profile it, then fix the right thing.

```python
import time
t0 = time.perf_counter()
result = slow_function()
print(f"elapsed: {(time.perf_counter() - t0) * 1000:.1f}ms")
```

## References

| Reference | Covers |
|---|---|
| `references/python_patterns.md` | Built-ins, sets, generators, caching, string ops |
| `references/dynamodb_patterns.md` | Batch reads/writes, projections, Query vs Scan |
| `references/lambda_async_patterns.md` | Cold starts, lazy imports, asyncio.gather |
| `references/dataframe_patterns.md` | Vectorised ops, filter pushdown, dtypes |

## When NOT to Optimise
- Code that runs once or rarely (scripts, migrations)
- Code that's not on the critical path
- Code that's already fast enough for its SLA
- Before writing tests — premature optimisation breaks untested code

## Rules
- Always benchmark before and after the change
- Fix the algorithm before micro-optimising (O(n²) → O(n) > any micro-opt)
- Never sacrifice readability for marginal gains
- Document WHY a non-obvious optimisation was needed
