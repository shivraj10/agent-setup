# Lambda & Async Optimization Patterns

## Module-level initialisation (avoid cold start overhead)
```python
# SLOW — creates client on every invocation
def lambda_handler(event, context):
    s3 = boto3.client("s3")
    db = boto3.resource("dynamodb")

# FAST — initialise once outside handler
s3 = boto3.client("s3")
db = boto3.resource("dynamodb")
table = db.Table(os.getenv("TABLE_NAME"))

def lambda_handler(event, context):
    ...
```

## Lazy-load heavy dependencies
```python
# SLOW — pandas imported at module level (adds ~200ms cold start)
import pandas as pd

# FAST — import inside function (only pays cost when actually needed)
def process_csv(data):
    import pandas as pd
    return pd.read_csv(data)
```

## Reduce package size
- Use `--exclude` to strip unnecessary files from Lambda zip
- Prefer `boto3` (already in Lambda runtime) over bundling it
- Use Lambda Layers for large shared dependencies (pandas, numpy)

## Run independent I/O calls concurrently
```python
# SLOW — sequential (total time = sum of all calls)
data_a = await fetch_a()
data_b = await fetch_b()

# FAST — concurrent (total time = slowest call)
data_a, data_b = await asyncio.gather(fetch_a(), fetch_b())
```

## Don't block the event loop
```python
# SLOW — blocks event loop
time.sleep(2)
result = sync_io()

# FAST — offload blocking work to thread pool
await asyncio.sleep(2)
result = await asyncio.to_thread(sync_io)
```
