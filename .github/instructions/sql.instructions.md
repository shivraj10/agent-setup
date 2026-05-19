---
applyTo: "**/*.sql"
---

# SQL Standards

- All queries stored as standalone `.sql` files under their module's `queries/` directory
- Use parameterised bind variables — never string interpolation
- Use CTEs (`WITH`) for readability over deeply nested subqueries
- Column aliases must be `snake_case`
- Always qualify columns with table aliases when joining
- Aggregations should use `round()` for percentages
- Include a header comment describing the query's purpose
