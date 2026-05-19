# EXAMPLE-123 — Add User Authentication Endpoint

**Ticket:** EXAMPLE-123 — Add JWT-based authentication endpoint
**Branch:** feature/EXAMPLE-123-auth-endpoint
**Date Started:** 2026-05-19
**Status:** Complete

---

## Plan

### Ticket Summary
Create a JWT authentication endpoint that validates user credentials and returns access tokens.

### Acceptance Criteria
- AC1: POST /auth/login accepts email + password, returns JWT token
- AC2: Token expires after 1 hour
- AC3: Invalid credentials return 401 with error message
- AC4: Rate limiting: max 5 attempts per minute per IP

### Implementation Steps

| # | Step | Complexity | Files | Status |
|---|------|-----------|-------|--------|
| 1 | Pydantic models for auth request/response | Low | `src/models/auth.py` (new) | ✅ Done |
| 2 | Auth service with JWT generation | Medium | `src/services/auth_service.py` (new) | ✅ Done |
| 3 | FastAPI route | Low | `src/apis/routes/auth.py` (new) | ✅ Done |
| 4 | Rate limiting middleware | Medium | `src/middleware/rate_limit.py` (new) | ✅ Done |
| 5 | Lint, type check, format | Low | — | ✅ Done |
| 6 | Pre-PR review, commit, push, open PR | Low | — | ✅ Done |

### Key Decisions
- Using python-jose for JWT encoding/signing
- Token stored in response body (not cookie) for API-first design
- Rate limit state stored in-memory (Redis in production)

---

## Dev Logs

### [Developer] Implementation — 2026-05-19 09:30
**Action:** Initial implementation complete, handing off to Tester
**Files Created:**
- `src/models/auth.py` — LoginRequest, TokenResponse models
- `src/services/auth_service.py` — JWT generation, credential validation
- `src/apis/routes/auth.py` — POST /auth/login endpoint
- `src/middleware/rate_limit.py` — IP-based rate limiting

**Key Decisions:**
- Token TTL configured via environment variable AUTH_TOKEN_TTL_SECONDS
- Password hashing with bcrypt

**Lint Status:** ✅ Zero errors (ruff + mypy)

### [Tester] Testing Iteration 1 — 2026-05-19 10:15
**Action:** Wrote and ran tests for auth module
**Test File(s):** `tests/unit/test_auth_service.py`, `tests/unit/test_auth_route.py`

**Tests Generated:**
| # | Test Name | Scenario | Status |
|---|-----------|----------|--------|
| 1 | test_login_valid_credentials_returns_token | Happy path | passed |
| 2 | test_login_invalid_password_returns_401 | Wrong password | passed |
| 3 | test_login_unknown_email_returns_401 | Non-existent user | passed |
| 4 | test_token_contains_expected_claims | JWT payload | passed |
| 5 | test_rate_limit_blocks_after_5_attempts | Rate limiting | passed |

**Results:** 5 passed, 0 failed | Coverage: 94%

**Verdict:** TESTS PASSING

### [Pre-PR Review] Review Iteration 1 — 2026-05-19 10:45
**Action:** Reviewed implementation against ACs

**AC Mapping:**
| # | Acceptance Criterion | Status | Evidence |
|---|----------------------|--------|----------|
| 1 | POST /auth/login returns JWT | met | `src/apis/routes/auth.py:15` |
| 2 | Token expires after 1 hour | met | `src/services/auth_service.py:28` — TTL=3600 |
| 3 | Invalid credentials return 401 | met | `src/apis/routes/auth.py:22` |
| 4 | Rate limiting 5/min/IP | met | `src/middleware/rate_limit.py:18` |

**Findings:**
| ID | Severity | File | Line | Description | Recommendation |
|----|----------|------|------|-------------|----------------|
| (none) | | | | No blocking findings | |

**Verdict:** READY FOR PR

### [Developer] Completion — 2026-05-19 11:00
- **Testing Iterations Used:** 1 / 2
- **Review Iterations Used:** 1 / 2
- **All Tests Passing:** Yes
- **Coverage:** 94%
- **Review Verdict:** READY FOR PR
- **Status:** Ready for commit
