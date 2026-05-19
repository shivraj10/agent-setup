---
name: security
description: >
  Security scanning for Python code and AWS SAM/CloudFormation templates.
  Load this skill when checking for vulnerabilities, hardcoded secrets,
  overly broad IAM policies, and dangerous code patterns.
---

# Security Skill

## Workflow
```
INVENTORY → SCAN → ANALYSE → REPORT
```

1. **INVENTORY** — find all `.py` and `.yaml` files; separate app code from tests
2. **SCAN** — check for secrets, dangerous functions, IAM violations
3. **ANALYSE** — evaluate severity, remove false positives
4. **REPORT** — structured security report

## References

| Reference | Covers |
|---|---|
| `references/python_checklist.md` | Input validation, dangerous functions, secrets, dependencies |
| `references/sam_checklist.md` | IAM, encryption at rest, public access, operational config |
| `references/dangerous_patterns.md` | Grep patterns to detect issues + severity guide |

## Scripts

Run the project security scanner for automated detection:

```bash
python tools/security_tools.py
```

## Rules
- Every finding must include file path, line number, and severity
- Always separate app code findings from test code findings
- Never mark test-only issues as CRITICAL
- Always verify a finding before reporting (check context, not just pattern match)
