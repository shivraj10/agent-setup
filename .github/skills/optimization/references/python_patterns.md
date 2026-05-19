# Python Optimization Patterns

## Use built-ins over manual loops
```python
# SLOW
total = 0
for x in numbers:
    total += x

# FAST — built-in C implementation
total = sum(numbers)

# SLOW
filtered = []
for x in items:
    if x.active:
        filtered.append(x)

# FAST — list comprehension
filtered = [x for x in items if x.active]
```

## Use sets for membership checks
```python
# SLOW — O(n) per lookup
valid_codes = ["A01", "B02", "C03", ...]
if code in valid_codes:   # linear scan

# FAST — O(1) per lookup
valid_codes = {"A01", "B02", "C03", ...}
if code in valid_codes:   # hash lookup
```

## String concatenation
```python
# SLOW — creates a new string on every iteration
result = ""
for part in parts:
    result += part

# FAST — single allocation
result = "".join(parts)
```

## Avoid recomputing inside loops
```python
# SLOW — len() called every iteration
for i in range(len(items)):
    process(items[i])

# BETTER — just iterate directly
for item in items:
    process(item)
```

## Use generators for large sequences
```python
# SLOW — materialises entire list in memory
total = sum([row["amount"] for row in huge_dataset])

# FAST — streams one item at a time
total = sum(row["amount"] for row in huge_dataset)
```

## Cache expensive repeated calls
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_config(key):
    return load_yaml_from_disk(key)
```
