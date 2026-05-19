# DynamoDB Optimization Patterns

## Batch reads instead of N+1
```python
# SLOW — N separate GetItem calls
results = []
for donor_id in donor_ids:
    item = table.get_item(Key={"pk": donor_id})
    results.append(item["Item"])

# FAST — single BatchGetItem (max 100 items per call)
response = dynamodb.batch_get_item(
    RequestItems={
        TABLE_NAME: {
            "Keys": [{"pk": did} for did in donor_ids]
        }
    }
)
results = response["Responses"][TABLE_NAME]
```

## Batch writes instead of N separate puts
```python
# SLOW — N separate PutItem calls
for item in items:
    table.put_item(Item=item)

# FAST — BatchWriter (auto-chunks into groups of 25)
with table.batch_writer() as batch:
    for item in items:
        batch.put_item(Item=item)
```

## Project only needed attributes
```python
# SLOW — fetches entire item (could be KB of data)
response = table.get_item(Key={"pk": donor_id})

# FAST — fetch only what you need
response = table.get_item(
    Key={"pk": donor_id},
    ProjectionExpression="pk, #n, email, status",
    ExpressionAttributeNames={"#n": "name"},
)
```

## Use Query not Scan
```python
# SLOW — full table scan
table.scan(FilterExpression=Attr("status").eq("active"))

# FAST — targeted query on GSI
table.query(
    IndexName="status-index",
    KeyConditionExpression=Key("status").eq("active"),
)
```
