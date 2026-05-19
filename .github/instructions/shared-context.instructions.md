---
applyTo: "**/*.agent.md,**/*.prompt.md"
---

# Shared Context File Rules

All agents working on a Jira ticket MUST use a single shared context file as the
source of truth for the entire ticket lifecycle. This file lives at:

```
.github/agent-outputs/<TICKET-ID>.md
```

## Agent Context and Actions Boundaries

Each agent has a bounded context and list of actions. If it is not listed below,
it is out of scope for that agent.

| Agent | Persona | Objective | Input Context | Actions | Output Context | Context Persistence |
|---|---|---|---|---|---|---|
| **Product Owner** | Product Owner / PM | Translate business requirements into structured Jira epics and stories with acceptance criteria | Confluence pages, PRDs, meeting transcripts, supporting documents | Create epics, create stories, write acceptance criteria, flag missing/ambiguous requirements | Jira: epic and story descriptions, acceptance criteria, missing requirements log | Jira is the system of record. Source documents remain in Confluence (linked in ticket). |
| **Planner (Triage)** | Technical Planner | Assess ticket workability, classify domain, recommend sub-agent, create plan, dispatch | Jira tickets in `To Do` (one at a time), attachments, codebase (scoped to assessment) | Read Jira, assess workability, add sub-agent recommendation as Jira comment, transition `To Do` → `In Progress`, create shared context file, create plan, dispatch | Jira comment: triage result + plan. Shared context file with Plan section. | Jira is the system of record. Shared context file committed with code. |
| **Developer** | Software Developer | Implement the feature per the plan, iterate with Tester (≤3x) and Code Review (≤3x) | Jira description, shared context file (Plan section), codebase | Create branch, write code, lint, **hand off to Tester** (do NOT test yourself), **hand off to Pre-PR Review** (do NOT review yourself), commit, push, open PR, append `[Developer]` entries to Dev Logs | Code on ticket branch. `[Developer]` log entries in shared context file. | Shared context file (`.github/agent-outputs/<TICKET-ID>.md`) is the evolving artifact across all iterations. |
| **Tester** | QA Engineer | Generate tests, run them, report results, iterate with Developer on failures (≤3 attempts) | Shared context file (Plan + Dev Logs), implementation code, Jira ACs | Read codebase, write tests, execute tests, append `[Tester]` entries to Dev Logs | Test code on branch. `[Tester]` log entries in shared context file. | Shared context file preserved across all Developer ↔ Tester iterations. |
| **Pre-PR Review** | Senior Code Reviewer | Answer: did we build the right thing? Check AC coverage, test completeness, security | PR diff, Jira ticket, shared context file (all sections) | Read PR diff, Jira, shared context file. Append `[Pre-PR Review]` entries to Dev Logs. When READY FOR PR: transition Jira `In Progress` → `Test`, add PR link comment. | `[Pre-PR Review]` log entries in shared context file. Jira comment with PR link. | Shared context file + Jira comment. |
| **PR Review** | Staff Engineer (GitHub Copilot built-in) | Answer: did we build it the right way? Check conventions, security, architecture | Open PR diff, codebase, `copilot-instructions.md` | Post review comments in PR | PR review comments | PR review comments on GitHub. |
| **Documentation** | Technical Writer | After merge, update Confluence and close Jira ticket with final summary | Merged PR diff, Jira ticket, existing Confluence docs, shared context file | Read merged diff, update Confluence pages, add Jira comment, transition `Test` → `Done` | Updated Confluence pages. Closed Jira ticket. | Confluence is the system of record for docs. Jira for ticket closure. |

## Jira State Machine

Agents manage Jira ticket transitions through the lifecycle:

```
To Do → In Progress → Test → Done
  ↑         ↑           ↑       ↑
Planner  Planner    Pre-PR   Documentation
creates  transitions Review   Agent closes
         workable   opens PR  after merge
         tickets
```

| Transition | Triggered By | Condition |
|---|---|---|
| `To Do` → `In Progress` | Planner | Ticket passes triage workability check |
| `In Progress` → `Test` | Pre-PR Review | Verdict is `READY FOR PR` and PR is opened |
| `Test` → `Done` | Documentation Agent | Post-merge: Confluence updated, ticket closed |

**Non-workable tickets remain in `To Do`** with a Jira comment explaining what's missing.

**Note:** PR Review (GitHub Copilot built-in) is not a custom agent — it is GitHub's
built-in Copilot review system that runs automatically on open PRs. It uses
`copilot-instructions.md` for project-specific review rules.

## Handoff Semantics

In agent `.agent.md` frontmatter, each handoff has a `send` field:

| Value | Meaning |
|-------|--------|
| `send: true` | Active handoff — agent should execute this delegation as part of its workflow |
| `send: false` | Available handoff — optional, used on-demand when needed (not auto-triggered) |

## Post-Merge Workflow Trigger

After a PR is merged to `dev`, the post-merge workflow is triggered by:
- **Manual:** User invokes `post-merge.prompt.md` with the ticket key, OR
- **Planner delegation:** Planner invokes Step 6 to delegate to Documentation Agent

The Documentation Agent then updates Confluence and closes the Jira ticket.

## File Ownership

| Agent | Section Owned | Action |
|-------|---------------|--------|
| **Planner** | Creates the file | Creates on ticket triage with header, ticket summary, and AC |
| **Developer** | Creates as fallback | Creates the file only if Planner didn't create it (direct invocation without Planner) |
| **Planner** | `## Plan` | Writes implementation steps, AC mapping, key decisions |
| **Developer** | `## Dev Logs` — `[Developer]` entries | Appends timestamped log entries for implementation, fixes, handoff notes |
| **Tester** | `## Dev Logs` — `[Tester]` entries | Appends timestamped log entries for test iterations, verdicts, coverage |
| **Pre-PR Review** | `## Dev Logs` — `[Pre-PR Review]` entries | Appends timestamped log entries for review iterations, findings, verdicts |

## Rules

- **One file per ticket** — never create separate output files per agent
- **Append only** — never overwrite or delete previous log entries
- **Read before writing** — always read the file first to understand current state
- **Prefix every entry with `[Agent Name]`** — `[Developer]`, `[Tester]`, `[Pre-PR Review]`
- **Timestamp every entry** — format: `YYYY-MM-DD HH:MM`
- **Chronological order** — entries appear in the order they happened, never reorder
- **Cross-reference** — Tester reads Developer entries to know what changed; Reviewer reads Tester entries to confirm tests pass
- **Verdicts are mandatory** — every Tester and Pre-PR Review entry must end with a verdict line
- **Dev Logs is the single section** — do NOT create separate `## Testing` or `## Code Review` sections; everything goes under `## Dev Logs`

## File Structure

```markdown
# <TICKET-ID> — <summary>

**Ticket:** <KEY> — <summary>
**Branch:** feature/<ticket-id>-<slug>
**Date Started:** <YYYY-MM-DD>
**Status:** In Progress

---

## Plan
<!-- Planner writes: AC mapping, implementation steps, key decisions -->

---

## Dev Logs
<!-- All agents append timestamped log entries here. Each entry is prefixed with [Agent Name]. -->
<!-- Entries are append-only and chronological — NEVER overwrite or reorder. -->

### [Developer] Implementation — <YYYY-MM-DD HH:MM>
**Action:** Initial implementation complete, handing off to Tester
**Files Created:** ...
**Files Modified:** ...
**Key Decisions:** ...
**Lint Status:** ✅ Zero errors

### [Tester] Testing Iteration 1 — <YYYY-MM-DD HH:MM>
**Action:** Wrote and ran tests
**Test File:** tests/unit/test_module.py
**Results:** X passed, Y failed | Coverage: Z%
**Verdict:** TESTS PASSING / TESTS FAILING
**Failures (if any):**
- `test_name`: root cause → recommended fix in `src/file.py:line`

### [Developer] Fix for Testing Iteration 1 — <YYYY-MM-DD HH:MM>
**Action:** Fixed failing tests, handing back to Tester
**What was fixed:** ...
**Files Changed:** ...
**Lint Status:** ✅ Zero errors

### [Tester] Testing Iteration 2 — <YYYY-MM-DD HH:MM>
**Action:** Re-ran tests after developer fix
**Results:** X passed, 0 failed | Coverage: Z%
**Verdict:** TESTS PASSING

### [Pre-PR Review] Review Iteration 1 — <YYYY-MM-DD HH:MM>
**Action:** Reviewed implementation against ACs
**AC Mapping:**
| # | AC | Status | Evidence |
|---|-----|--------|----------|
| 1 | ... | met    | file:line |
**Findings:**
| ID | Severity | File | Description | Recommendation |
|----|----------|------|-------------|----------------|
| H1 | HIGH | ... | ... | ... |
**Verdict:** CHANGES REQUIRED / READY FOR PR

### [Developer] Fix for Review Iteration 1 — <YYYY-MM-DD HH:MM>
**Action:** Fixed review findings, handing to Tester then back to Reviewer
**Findings Fixed:** H1 — <what was changed>
**Files Changed:** ...
**Lint Status:** ✅ Zero errors

### [Developer] Completion — <YYYY-MM-DD HH:MM>
- **Testing Iterations Used:** N / 2
- **Review Iterations Used:** N / 2
- **All Tests Passing:** Yes
- **Coverage:** X%
- **Review Verdict:** READY FOR PR
- **Status:** Ready for commit
```

## Workflow Reference

See `.github/diagrams/agent-workflow.md` for the visual flow:

```
Product Owner → Planner (Triage) → Developer → Tester ⇄ Developer → Reviewer ⇄ Developer → PR → Documentation Agent
     ↕                ↕                ↕            ↕            ↕            ↕                        ↕
  [Confluence]   [Jira: To Do     [────── Shared Context File (.github/agent-outputs/TICKET-ID.md) ──────]  [Confluence]
   + PRDs         → In Progress]                                                                         [Jira: Done]
```

### Full Lifecycle Flow

```
1. Product Owner: Confluence/PRD → Jira Epics & Stories (with ACs)
2. Planner: Triage ticket → Workable? → Create shared context file → Plan → Delegate
3. Developer: Branch → Code → Lint → Handoff Tester (≤2 iterations) → Handoff Reviewer (≤2 iterations) → PR
4. Pre-PR Review: READY FOR PR → Jira In Progress → Test
5. GitHub Copilot PR Review: Conventions, security, architecture
6. Merge to dev
7. Documentation Agent: Update Confluence → Close Jira (Test → Done)
```
