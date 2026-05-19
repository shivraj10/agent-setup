---
description: Run post-merge workflow — update Confluence documentation and close the Jira ticket
agent: 'Planner'
model: 'Claude Sonnet 4'
tools: ['search/codebase', 'fetch']
---

Run the post-merge workflow for: ${input:jira_ticket_key}

The PR has been merged. Follow the Planner's post-merge workflow:
1. Delegate to Code Documentation Agent with the ticket key and merged PR link
2. Code Documentation Agent will:
   - Update linked Confluence pages with the merged changes
   - Add a final delivery summary comment on the Jira ticket
   - Transition the Jira ticket from Test → Done
3. Confirm closure: Confluence updated, Jira closed, any follow-up items surfaced
