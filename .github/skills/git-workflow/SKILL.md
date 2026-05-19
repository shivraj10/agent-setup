---
name: git-workflow
description: >
  Git branching, commit messages, and PR workflow patterns. Load this skill
  when creating branches, writing commit messages, preparing PRs, or resolving
  merge conflicts. Follows conventional commits and feature-branch workflow.
---

# Git Workflow Skill

## Feature Branch Workflow

**Every new feature or task MUST be developed on a dedicated branch created from `main`.**

### Workflow
```
1. git checkout main && git pull origin main
2. git checkout -b feature/<name>
3. ... develop, commit ...
4. git push origin feature/<name>
5. Raise a PR to merge feature/<name> → main  (preferred)
   OR  merge locally and push main             (if user requests)
```

### Rules
- **Always** branch from an up-to-date `main` — pull before branching.
- **Never** commit directly to `main` for feature work.
- Use `feature/<name>` for the branch name (lowercase, hyphens, no spaces).
- Keep the branch focused on a single feature or task.
- When work is complete, **raise a Pull Request** to `main` by default.
  Only merge locally if the user explicitly asks to skip the PR.

### When to Create a Branch
| Situation | Action |
|---|---|
| New feature or enhancement | Create `feature/<name>` from `main` |
| Bug fix | Create `fix/<name>` from `main` |
| Refactoring | Create `refactor/<name>` from `main` |
| Documentation-only change | Commit directly to `main` (optional branch) |
| Chore (deps, CI, tooling) | Create `chore/<name>` from `main` |

## Branch Naming
```
feature/<short-description>           # new features
fix/<short-description>               # bug fixes
refactor/<short-description>          # refactoring
chore/<short-description>             # deps, CI, tooling
```

Examples:
```
feature/deferral-age-filter
feature/smart-insight-pipeline
fix/cache-key-collision
refactor/simplify-pipeline-factory
```

## Commit Messages (Conventional Commits)
```
<type>(<scope>): <short summary>

<optional body — explain WHY, not WHAT>

<optional footer — ticket refs, breaking changes>
```

### Types
| Type | When |
|---|---|
| `feat` | New feature |
| `fix` | Bug fix |
| `refactor` | No behaviour change |
| `test` | Adding/fixing tests |
| `docs` | Documentation only |
| `chore` | Build, deps, CI |
| `perf` | Performance improvement |

### Examples
```
feat(deferral): add age-group filter to diagnostic insights

The deferral diagnostic tab now accepts an age_group parameter
that filters donor demographics before generating insights.

Refs: DDJ-142
```

```
fix(cache): use stable JSON serialisation for cache keys

sort_keys=True prevents cache misses caused by dict ordering
differences between Python versions.

Fixes: DDJ-198
```

## PR Description Template
```markdown
## Summary
- <1-3 bullet points describing what changed and why>

## Changes
- `src/models/foo.py` — new Pydantic model for Foo
- `src/services/foo_service.py` — business logic
- `tests/unit/test_foo_service.py` — 12 tests, 91% coverage

## Test plan
- [ ] Unit tests pass locally
- [ ] Lint clean (ruff check + format)
- [ ] Manual test against staging (if applicable)
```

### Raising a PR (default end-of-feature action)
After pushing the feature branch:
1. Use the GitHub MCP tool to create a PR from `feature/<name>` → `main`.
2. Title follows conventional commit format: `feat(<scope>): <summary>`.
3. Fill in the PR description template above.
4. Assign reviewers if known.

### Merging Locally (only when user requests)
```bash
git checkout main
git pull origin main
git merge --squash feature/<name>
git commit -m "feat(<scope>): <summary>"
git push origin main
git branch -d feature/<name>
git push origin --delete feature/<name>
```

## Merge Strategy
- **Squash merge** for feature branches into main
- **Rebase** to keep feature branch up to date with main
- Never force-push to main/develop

## Conflict Resolution
1. `git fetch origin main`
2. `git rebase origin/main`
3. Fix conflicts file by file — keep the intent of both changes
4. `git add <file>` then `git rebase --continue`
5. Run tests after rebase to verify nothing broke
