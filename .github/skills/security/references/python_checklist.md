# Python Security Checklist

## Input Validation
- [ ] All external input validated with Pydantic models
- [ ] No raw `dict` from events used without validation
- [ ] No string concatenation for SQL/DynamoDB expressions
- [ ] No user input passed to `os.system()`, `subprocess.run()`, or `eval()`

## Dangerous Functions
- [ ] No `eval()` or `exec()` on any input
- [ ] No `pickle.loads()` on untrusted data
- [ ] No `yaml.load()` without `Loader=SafeLoader`
- [ ] No `subprocess.run(shell=True)` with variable input
- [ ] No `os.system()` calls

## Secrets & Credentials
- [ ] No API keys, tokens, or passwords in source code
- [ ] No secrets in environment variable defaults
- [ ] No `.env` files committed to version control
- [ ] Secrets fetched at runtime from SSM/Secrets Manager
- [ ] No secrets in log output

## Dependencies
- [ ] No known-vulnerable packages
- [ ] All packages pinned to specific versions
