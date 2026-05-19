---
name: codebase-indexer
description: >
  Generates a navigable code index for AGENTS.md so agents can locate files
  without broad searching. Load this skill when onboarding a new codebase,
  when the project grows beyond ~50 files, or when agents are doing excessive
  file searches. Produces a structured map of modules, key classes, and
  public functions with file paths and line numbers.
---

# Codebase Indexer Skill

## Purpose

When a codebase exceeds ~50 source files, agents waste tokens doing broad
`grep` / `file_search` sweeps to locate relevant code. This skill generates
a machine-friendly code index that agents read **before** searching, letting
them jump directly to the right file.

## When to Use

- Initial project onboarding (first time an agent works with a repo)
- After major refactors that move files or rename modules
- When agents are searching 10+ files to find one thing
- Periodically (e.g., pre-commit hook or CI step) to keep the index fresh

## How It Works

1. Run `python tools/generate_code_index.py` from the project root
2. The tool uses `tools/ast_tools.py` to parse every `.py` file under `src/`
3. Outputs a structured index to `AGENTS.md` (appended under `# Code Index`)
   or to a standalone `.code-index.md` file

## Command

```bash
# Append code index to AGENTS.md (recommended — agents always read this)
python tools/generate_code_index.py --target agents-md

# Write standalone index file (for very large repos)
python tools/generate_code_index.py --target standalone

# Print to stdout (for inspection)
python tools/generate_code_index.py
```

## Output Format

The generated index follows this structure:

```markdown
# Code Index

> Auto-generated. Run `python tools/generate_code_index.py --target agents-md` to refresh.

## Key Entry Points
- FastAPI app: `src/main.py`
- LLM client: `src/genai/bedrock.py` → `DatabricksChat`
- Smart Insight pipeline: `src/genai/smart_insight/insight_generator.py` → `InsightPipeline`
- Conversational BI: `src/genai/conversational_bi/factory.py` → `ConversationalBIPipelineFactory`

## Module Map

| Directory | Purpose | Key classes/functions |
|-----------|---------|---------------------|
| `src/models/` | Pydantic data shapes | `DeferralRequest`, `InsightResponse`, ... |
| `src/database/` | DB connections + queries | `get_databricks_connection()`, `ExecutionLogRepository` |
| `src/genai/smart_insight/` | AI insight pipeline | `InsightPipeline`, `LLMClient`, `FollowUpGenerator` |
| ...       | ...     | ...                 |

## Symbol Index (top public classes & functions)

| Symbol | File | Line | Type |
|--------|------|------|------|
| `DatabricksChat` | `src/genai/bedrock.py` | 36 | class |
| `execute_query` | `src/genai/common.py` | 12 | async function |
| ...    | ...  | ...  | ...  |
```

## Integration Points

- **AGENTS.md**: Append the index so every agent reads it on startup
- **Pre-commit hook**: Regenerate on every commit to keep it current
- **CI/CD**: Add as a build step to detect index drift

## Configuration

The indexer respects these settings (defined at the top of the script):

| Setting | Default | Description |
|---------|---------|-------------|
| `SRC_DIRS` | `["src/"]` | Directories to scan |
| `EXCLUDE_DIRS` | `["__pycache__"]` | Directories to skip |
| `EXCLUDE_FILES` | `["__init__.py"]` | Files to skip (usually empty modules) |
| `MAX_SYMBOLS` | `100` | Cap on symbols in the index (keeps it concise) |
| `INCLUDE_PRIVATE` | `False` | Whether to include `_private` functions |

## Best Practices

1. **Keep it concise** — The index should be <200 lines. Agents load it into
   context, so bloat defeats the purpose.
2. **Prioritize entry points** — List the files agents are most likely to need
   first (handlers, factories, main pipelines).
3. **Group by domain** — Not alphabetical. Group by what the code does.
4. **Refresh after refactors** — Stale indexes are worse than no index.
5. **Don't index tests** — Agents find tests by mirroring src/ structure.
