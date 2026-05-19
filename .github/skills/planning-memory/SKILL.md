---
name: planning-memory
description: >
  Planning and progress tracking for multi-step development work. Load this
  skill when a Jira ticket requires more than 3 implementation steps, when
  work may span multiple sessions, or when building a large feature end-to-end.
  Covers creating implementation plans, tracking step progress, resuming
  across sessions, and cleaning up plans after PR creation.
---

# Planning & Memory for Long-Running Development

## When to Use

- Jira ticket requires **4+ implementation steps**
- Feature touches **5+ files** across multiple packages
- Work is complex enough that it may **span multiple chat sessions**
- You need a resumable progress tracker that survives session expiry

## Plan File Location & Naming

Store plans in the workspace so they persist across sessions:

```
.github/plans/<ticket-id>-<slug>.md
```

Example: `.github/plans/DINA-8558-conversational-bi.md`

**Never store plans in session memory only** — session memory is lost when the
conversation ends. The workspace file is the source of truth.

## Step 1 — Create the Plan

After reading the Jira ticket and before writing any code, create a plan file.

**Every plan MUST include a Progress Tracker table** immediately after the title.
This table provides an at-a-glance view of overall progress and MUST be kept
up to date as steps are completed.

```markdown
# <TICKET-ID> — <Title>

## Progress Tracker

| Step | Description | Status |
|------|-------------|--------|
| 1 | <Step 1 name> | ⬜ Not started |
| 2 | <Step 2 name> | ⬜ Not started |
| ... | ... | ... |

Status values: ⬜ Not started → 🔄 In progress → ✅ Completed

## Ticket Summary
<1-2 sentence summary of what needs to be built>

## Acceptance Criteria
- AC1: <criteria from ticket>
- AC2: <criteria from ticket>
- ...

## Implementation Steps

### Step 1 — <Name> (<Effort>) [<Owner>]
- [ ] <What to build>
- Files: `path/to/file.py` (new|modify)
- Dependencies: None

### Step 2 — <Name> (<Effort>) [<Owner>]
- [ ] <What to build>
- Files: `path/to/file.py` (new|modify)
- Dependencies: Step 1

...
```

### Plan Rules

1. **Each step must be independently completable** — no step should require
   another unfinished step to run or test
2. **Map every AC to at least one step** — if an AC has no step, add one
3. **Effort labels**: Low (< 30 min), Medium (30-60 min), High (> 60 min)
4. **File listing**: List every file to create or modify per step
5. **Keep steps to 3-8 per plan** — split or merge if outside this range

## Step 2 — Track Progress During Implementation

As you complete each step, update the plan file in-place:

- Change `- [ ]` to `- [x]` when a step is done
- Add a brief note if the implementation deviated from the plan

```markdown
### Step 1 — Pydantic Models (Low) [Developer]
- [x] Models created: ConversationalBIRequest, ConversationalBIResponse
- Files: `src/models/conversational_bi.py` (new)
- Dependencies: None
```

### Progress Update Rules

1. **Update the Progress Tracker table first** — change the step status to
   🔄 before starting and ✅ after completing
2. **Update the plan after completing each step** — not in batches
3. **If a step changes scope**, update the plan before implementing
4. **If you add a step**, insert it in the correct dependency order and add
   a row to the Progress Tracker table
5. **Never delete completed steps** — they serve as a record

## Step 3 — Resume Across Sessions

When starting a new session on an existing ticket:

1. **Check for existing plans**: `ls .github/plans/`
2. **Read the plan file** to understand what's done and what's remaining
3. **Find the first unchecked step** (`- [ ]`) and resume from there
4. **Verify completed work** — run tests for completed steps before continuing
5. **Continue the workflow** from the current step

### Resume Checklist

```
1. Read .github/plans/<ticket-id>-*.md
2. Run existing tests: pytest tests/unit/ -q --no-header
3. Run lint: ruff check . && ruff format --check .
4. Identify next unchecked step
5. Continue implementation
```

## Step 4 — Close Out After PR

Once the PR is created:

1. **Copy the plan into the PR description** — include:
   - Ticket summary
   - Acceptance criteria as checkboxes
   - Implementation steps (completed) as a changelog
   - Pre-PR review verdict

2. **Delete the plan file** from the workspace:
   ```bash
   git rm .github/plans/<ticket-id>-*.md
   git commit -m "chore: remove implementation plan for <TICKET-ID>"
   ```

3. **Clean up session memory** if any was created:
   - Remove any `/memories/session/` files related to this ticket

### PR Description Template

When adding the plan to the PR body, use this structure:

```markdown
<!-- jira-context -->
## Jira: <TICKET-ID>
<Ticket summary>

### Acceptance Criteria
- [x] AC1: ...
- [x] AC2: ...

### Implementation Steps
1. ✅ Step 1 — <Name>: <brief summary of what was done>
2. ✅ Step 2 — <Name>: <brief summary>
...

### Changes
- Created: `path/to/new/file.py`
- Modified: `path/to/existing/file.py`
- Deleted: `path/to/old/file.py` (if any)

### Pre-PR Review Verdict
✅ READY FOR PR
<!-- end-jira-context -->
```

## Anti-Patterns

- **No plan for large features** — jumping straight into code without a plan
  causes scope creep and missed ACs
- **Plan only in chat** — chat context is lost on session expiry; always write
  to `.github/plans/`
- **Stale plans** — forgetting to update checkboxes means the next session
  can't resume accurately
- **Plans left after merge** — plan files committed to `dev`/`main` are clutter;
  always delete them in a cleanup commit before or after merge
