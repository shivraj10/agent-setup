# Dangerous Patterns — Grep Reference

Search for these patterns in source code to detect security issues:

```
eval(
exec(
pickle.loads
yaml.load
subprocess.run.*shell=True
os.system
marshal.loads
password.*=.*['"]
api_key.*=.*['"]
secret.*=.*['"]
AWS_ACCESS_KEY
AWS_SECRET_KEY
Action.*['"]\\*['"]
Resource.*['"]\\*['"]
```

## Severity Guide

| Severity | Examples |
|---|---|
| **CRITICAL** | Hardcoded AWS keys, `eval()` on user input, public S3 with PII |
| **HIGH** | No input validation, overly broad IAM, secrets in logs |
| **MEDIUM** | Missing DLQ, unpinned dependencies, `DeletionPolicy: Delete` |
| **LOW** | Missing X-Ray tracing, log retention not set |
