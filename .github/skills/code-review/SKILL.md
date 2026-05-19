---
name: code-review
description: >
  Structured code review for Python and SAM templates. Load this skill when
  reviewing code for correctness, security, performance, and convention
  violations. Produces a severity-rated report with remediation guidance.
---

# Code Review Skill

## Workflow
```
READ → ANALYSE → REPORT
```

1. **READ** — read the target files and their imports
2. **ANALYSE** — check every category in the checklist below
3. **REPORT** — produce a structured review with severity ratings

## Review Checklist

### Correctness
- Logic matches the stated requirement
- Edge cases handled (empty input, None, boundary values)
- Error paths return/raise correctly
- No off-by-one errors
- Async code properly awaited

### Security
- No hardcoded secrets, API keys, or passwords
- Input validated with Pydantic models
- SQL/NoSQL injection not possible (parameterised queries)
- No `eval()`, `exec()`, `pickle.loads()` on untrusted input
- Secrets fetched from SSM/Secrets Manager
- No sensitive data in logs

### Performance
- No N+1 query patterns
- No unbounded loops or recursion
- Expensive objects created once (module-level or cached)
- DynamoDB queries use key conditions, not full scans

### Conventions
- Repository pattern followed (no boto3 in handlers/services)
- Pydantic models for data shapes
- structlog for logging
- Domain exceptions defined and used
- Google-style docstrings on public interfaces
- Test coverage 80%+

### AWS Best Practices
- Lambda handler is thin (delegates to service)
- Environment variables for resource names
- Batch item failures returned for SQS triggers
- Connection reuse (module-level clients)
- DLQs configured

## Severity Guide

| Severity | Meaning |
|---|---|
| **CRITICAL** | Bug causing data loss, security breach, or outage — must fix |
| **HIGH** | Incorrect behaviour in production — must fix |
| **MEDIUM** | Convention violation, missing error handling — should fix |
| **LOW** | Style issue, minor improvement — fix at discretion |

## Report Format
```
<REVIEW>
File: ...

CRITICAL (N)
[C1] Line XX: description
  Recommendation: ...

HIGH (N)
[H1] Line XX: description
  Recommendation: ...

SUMMARY
Total findings: X (N critical, N high, N medium, N low)
Verdict: APPROVED / CHANGES REQUESTED
</REVIEW>
```

## Output Persistence

When this skill is used by the Pre-PR Review agent, the review output
must be written to `.github/agent-outputs/<TICKET-ID>-review.md`.
See the Pre-PR Review agent instructions for the full file format
including iteration tracking, AC mapping, and fix history.
