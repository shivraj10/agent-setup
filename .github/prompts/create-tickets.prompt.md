---
description: Translate business requirements into structured Jira epics and stories with acceptance criteria
agent: 'Product Owner'
model: 'Claude Sonnet 4'
tools: ['search/codebase', 'fetch']
---

Create Jira tickets from these requirements: ${input:requirements_source}

Follow the Product Owner workflow:
1. Gather and read all input sources (Confluence pages, PRDs, descriptions)
2. Analyse for completeness — flag any ambiguities or missing requirements
3. Decompose into epics and stories with Given/When/Then acceptance criteria
4. Create Jira tickets with full structure (summary, ACs, dependencies, scope)
5. Validate all stories have ≥2 testable ACs
6. Hand off to Planner for triage and delivery
