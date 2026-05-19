---
description: Generate a new Smart Insight module with strategy, factory, queries, and prompts
agent: 'agent'
model: 'Claude Sonnet 4'
tools: ['editFiles', 'search/codebase', 'terminalLastCommand']
---

Create a new Smart Insight module for: ${input:module_name}

Follow the established pattern from `src/genai/smart_insight/waterfall/` and `src/genai/smart_insight/deferral/`:

1. `src/genai/smart_insight/${input:module_name}/common.py` — default params and constants
2. `src/genai/smart_insight/${input:module_name}/<tab>_queries/*.sql` — SQL query files
3. `src/genai/smart_insight/${input:module_name}/<tab>_prompts.yaml` — LLM prompt template
4. `src/genai/smart_insight/${input:module_name}/<strategy>.py` — strategy class
5. `src/genai/smart_insight/${input:module_name}/factory.py` — pipeline factory
6. `src/genai/smart_insight/${input:module_name}/__init__.py` — wiring and registration
7. `src/apis/routes/<domain>.py` — FastAPI route
