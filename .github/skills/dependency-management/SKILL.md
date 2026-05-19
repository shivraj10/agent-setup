---
name: dependency-management
description: >
  Python dependency management with pip, pyproject.toml, and requirements
  files. Load this skill when adding, upgrading, or auditing dependencies.
  Covers pinning, security scanning, and keeping lock files up to date.
---

# Dependency Management Skill

## File Structure
```
pyproject.toml            # primary — defines project + deps
requirements.txt          # pinned versions for production deploy
requirements-dev.txt      # dev/test-only deps (pytest, ruff, moto)
```

## pyproject.toml Pattern
```toml
[project]
name = "my-service"
version = "1.0.0"
requires-python = ">=3.11"
dependencies = [
    "pydantic>=2.0,<3.0",
    "structlog>=23.0",
    "boto3>=1.28",
    "fastapi>=0.100",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-asyncio>=0.21",
    "pytest-cov>=4.0",
    "moto[s3,dynamodb,sqs]>=5.0",
    "ruff>=0.1",
    "mypy>=1.5",
    "respx>=0.20",
]
```

## Pinning Strategy

| Context | Strategy | Example |
|---|---|---|
| `pyproject.toml` | Compatible range | `pydantic>=2.0,<3.0` |
| `requirements.txt` | Exact pin | `pydantic==2.5.3` |
| `requirements-dev.txt` | Exact pin | `pytest==7.4.3` |

### Generating pinned requirements
```bash
pip compile pyproject.toml -o requirements.txt
pip compile pyproject.toml --extra dev -o requirements-dev.txt
```

## Adding a New Dependency
1. Add to `pyproject.toml` with compatible range
2. `pip install -e ".[dev]"` to test locally
3. Regenerate `requirements.txt`
4. Run full test suite to confirm nothing breaks
5. Commit all three files together

## Upgrading Dependencies
```bash
# Check what's outdated
pip list --outdated

# Upgrade one package
pip install --upgrade <package>

# Regenerate lock file
pip compile pyproject.toml -o requirements.txt

# Run tests
pytest
```

## Security Auditing
```bash
# Check for known vulnerabilities
pip audit

# Check with safety
safety check -r requirements.txt
```

## Rules
- Never add a dependency without checking if stdlib or existing deps can do the job
- Always pin in requirements.txt — floating versions in production cause surprises
- Never commit `requirements.txt` changes without running tests
- Keep dev deps separate from production deps
- Audit dependencies before upgrading major versions
- Prefer well-maintained packages with >1000 GitHub stars for critical functionality
