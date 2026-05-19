---
applyTo: "**/*.instructions.md,**/*.agent.md,**/SKILL.md,**/AGENTS.md,**/*.prompt.md"
---

# Security-Sensitive File Rules

- Never hardcode API keys, tokens, passwords, or connection strings
- Never include real Confluence page IDs, Jira project keys, or user emails inline
- Reference secrets via environment variables or AWS Secrets Manager
- Never expose internal hostnames, database endpoints, or S3 bucket names
- Use `CONFLUENCE_API_TOKEN` env var pattern — not inline credentials
- Never include PII (donor names, emails, IDs) in prompt templates or examples
