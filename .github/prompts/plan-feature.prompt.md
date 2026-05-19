---
description: Plan a new feature by analysing the codebase and producing an implementation plan
agent: 'Planner'
model: 'Claude Sonnet 4'
tools: ['search/codebase', 'fetch']
---

Analyse the codebase and create an implementation plan for: ${input:feature_description}

Output the plan in this format:
```
<PLAN>
Task: <one-line summary>
Steps:
  1. [Developer] <action> — Inputs: ... → Outputs: ...
  2. [Developer] <action> — Depends on: step 1
  3. [Tester] Write tests — Depends on: steps 1-2
  4. [manual] Deploy — Depends on: step 3
Complexity: low | medium | high
</PLAN>
```
