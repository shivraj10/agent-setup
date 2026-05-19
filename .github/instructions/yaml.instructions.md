---
applyTo: "**/*.yaml,**/*.yml"
---

# YAML Standards

- Use YAML for prompt templates and configuration — not inline strings
- Indent with 2 spaces, no tabs
- Use block scalars (`|` or `>`) for multi-line text
- Quote strings containing special characters (`:`, `#`, `{`, `}`)
- Prompt template keys follow the pattern: `{tab}_template`
- System role definitions belong in prompt YAML files, not in code
