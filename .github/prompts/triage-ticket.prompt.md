---
description: Triage a Jira ticket — assess workability, classify domain, recommend sub-agent, and dispatch for delivery
agent: 'Planner'
model: 'Claude Sonnet 4'
tools: ['search/codebase', 'fetch']
---

Triage this Jira ticket for delivery: ${input:jira_ticket_key}

Follow the Planner's triage workflow:
1. Fetch the Jira ticket and assess workability (ACs exist, scope bounded, testable criteria)
2. If NOT workable: flag what's missing in a Jira comment and STOP
3. If workable: classify the domain, recommend a sub-agent, transition To Do → In Progress
4. Create the shared context file at `.github/agent-outputs/<TICKET-ID>.md`
5. Write the implementation plan
6. Delegate to the recommended sub-agent for end-to-end delivery
