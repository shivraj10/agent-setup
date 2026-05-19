---
name: cicd-pipeline
description: >
  CI/CD pipeline creation for AWS SAM templates and GitHub Actions workflows.
  Load this skill when creating SAM templates, deployment workflows, or
  environment-level pipeline configurations. Covers SAM resource patterns,
  GitHub Actions workflow structure, and multi-environment deployment.
---

# CI/CD Pipeline Skill

## When to Use
- Creating or modifying AWS SAM `template.yml`
- Creating GitHub Actions deployment workflows (dev/test/prod)
- Adding CI gates (lint, test, security scan) to pipelines
- Setting up multi-environment parameter strategies

## SAM Template Standards

### Parameters
- Parameterise ALL environment-specific values (never hardcode)
- Required params: `RuntimeEnvironment`, `LambdaIamRoleArn`
- Use `Default` values for non-sensitive params (timeouts, memory)
- Sensitive values (tokens, ARNs) have no defaults — passed at deploy time

### Resources
- Name pattern: `!Sub '${AWS::StackName}-${RuntimeEnvironment}-<Name>'`
- Tag all resources: `apms-id: APMS-XXXXX`
- Lambda config:
  - Runtime: `python3.12`
  - Handler: `main.handler` (Mangum entry point)
  - VPC config for database-connected functions
  - Layers for dependencies (core + auth separated)
- Secrets Manager for credentials — never environment variables
- API Gateway with explicit route definitions per endpoint

### Outputs
- Export Lambda ARN, API Gateway URL, Secret ARN
- Use `!Sub` export names for cross-stack references

## GitHub Actions Workflow Standards

### Structure
- One workflow file per environment: `dev-deployment.yml`, `test-deployment.yml`, `prod-deployment.yml`
- Separate CI workflow for PR validation: `pr-checks.yml`

### CI Gates (run before deploy)
1. `ruff check . && ruff format --check .` — lint
2. `pytest tests/unit/ -v --tb=short` — unit tests
3. `sam validate` — template validation
4. `sam build` — build verification

### Deploy Steps
1. Checkout code
2. Set up Python + SAM CLI
3. Install dependencies
4. Run CI gates
5. `sam build`
6. `sam deploy` with env-specific parameters

### Security
- Use `${{ secrets.* }}` for ALL sensitive values
- Pin action versions: `actions/checkout@v4`, NOT `actions/checkout@latest`
- Set minimal `permissions` block per job
- Never echo secrets or write them to files
- Use OIDC for AWS auth when possible (`aws-actions/configure-aws-credentials@v4`)

### Environment Strategy
| Environment | Trigger | Branch | Approval |
|-------------|---------|--------|----------|
| dev | push | `dev` | none |
| test | manual / push | `test` | none |
| prod | manual | `main` | required |

## Templates

Use the scaffolds in `templates/` as starting points:

| Template | Use when |
|---|---|
| `templates/sam_template.yml` | Creating a new SAM template |
| `templates/deployment_workflow.yml` | Creating an env-level deployment workflow |
| `templates/pr_checks_workflow.yml` | Creating a PR validation pipeline |
