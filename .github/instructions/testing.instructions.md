---
applyTo: "**/tests/**"
excludeAgent: "code-review"
---

# Test Standards

- pytest as the sole test framework
- Test files mirror source structure: `src/foo/bar.py` → `tests/unit/test_bar.py`
- Use `pytest-asyncio` for async tests with `@pytest.mark.asyncio`
- Mock external dependencies (DB, LLM, HTTP) — never call real services in unit tests
- Use `pytest.fixture` for shared setup — avoid test-level setup/teardown
- Target ≥80% coverage on all new modules
- Name tests: `test_<function>_<scenario>_<expected_result>`
- Use `pytest.raises` for expected exceptions
