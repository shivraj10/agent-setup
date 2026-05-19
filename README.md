# VS Code Copilot Agent Setup

Multi-agent SDLC orchestration using GitHub Copilot custom agents, skills, instructions, and prompts. Automates the full lifecycle from Jira ticket to merged PR with quality gates.

## What's Included

```
.github/
  agents/           # Custom agent definitions (Developer, Tester, Planner, etc.)
  instructions/     # Code standards applied automatically by file pattern
  skills/           # Domain knowledge packages (coding, security, debugging, etc.)
  prompts/          # Reusable prompt templates for common workflows
  diagrams/         # Architecture and workflow diagrams
  agent-outputs/    # Example shared context file (ticket lifecycle audit trail)
  copilot-instructions.md  # Project-level Copilot instructions
.vscode/
  mcp.json          # MCP server configuration (GitHub, Atlassian, Obsidian)
AGENTS.md           # Build, test, deploy commands and workflow paths
```

## Agent Workflow

```
Product Owner → Planner (Triage) → Developer → Tester ⇄ Developer → Pre-PR Review ⇄ Developer → PR → Documentation Agent
```

### Agents

| Agent | Role |
|-------|------|
| **Product Owner** | Translates requirements into Jira stories with acceptance criteria |
| **Planner** | Triages tickets, assesses workability, plans implementation, delegates |
| **Developer** | Writes code, lints, hands off to Tester and Reviewer (never tests/reviews itself) |
| **Tester** | Writes and runs pytest suites, reports coverage and failures |
| **Pre-PR Review** | Reviews code against acceptance criteria, reports HIGH/CRITICAL findings only |
| **Code Documentation Agent** | Updates Confluence, closes Jira tickets post-merge |

### Workflow Paths

- **Path A (Full lifecycle):** Confluence/PRD → Product Owner → Jira Stories → Planner → Developer → Tester → Review → PR → Docs → Done
- **Path B (Existing ticket):** Jira ticket → Planner Triage → Developer → Tester → Review → PR → Docs → Done
- **Path C (Quick planning):** Feature description → Planner (exploration/estimation)
- **Path D (Post-merge):** Merged PR → Documentation Agent → Confluence + Jira closure

## Skills

| Skill | Purpose |
|-------|---------|
| `coding` | Python architecture patterns, templates for routes/handlers/models |
| `api-design` | REST API conventions, status codes, pagination |
| `cicd-pipeline` | SAM templates, GitHub Actions workflows |
| `code-review` | Structured review with severity ratings |
| `debugging` | Systematic root cause analysis |
| `security` | OWASP scanning, IAM policy review |
| `linting` | Ruff + mypy fix strategies |
| `logging` | structlog patterns, what to log/never log |
| `git-workflow` | Branching, conventional commits, PR workflow |
| `optimization` | Performance patterns (Python, Lambda, DynamoDB, DataFrame) |
| `planning-memory` | Multi-step task tracking across sessions |
| `refactoring` | Behaviour-preserving code restructuring |
| `mermaid-diagrams` | Architecture and flow diagrams |
| `excalidraw-diagram-generator` | Visual argument diagrams |
| `commenting` | Google-style docstrings |
| `dependency-management` | pip/pyproject.toml patterns |

## Setup

1. Clone this repo into your VS Code workspace
2. Copy `.vscode/mcp.json` to your project (or merge with existing)
3. Copy `.github/` directory to your project
4. Copy `AGENTS.md` to your project root
5. Customize instructions and skills for your tech stack

## Requirements

- VS Code with GitHub Copilot extension
- MCP servers: GitHub (built-in), Atlassian (for Jira/Confluence), Obsidian (optional)
- Python 3.12+ (for the example project standards)

## License

MIT
