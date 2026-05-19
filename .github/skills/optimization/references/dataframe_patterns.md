# DataFrame / Pandas Optimization Patterns

## Use vectorised operations over apply/loops
```python
# SLOW — row-by-row Python loop
df["total"] = df.apply(lambda row: row["price"] * row["qty"], axis=1)

# FAST — vectorised C operation
df["total"] = df["price"] * df["qty"]
```

## Filter early, process less
```python
# SLOW — load all rows, then filter
df = pd.read_parquet("large_file.parquet")
df = df[df["status"] == "active"]

# FAST — push filter into read (row group pruning)
df = pd.read_parquet("large_file.parquet", filters=[("status", "==", "active")])
```

## Use appropriate dtypes
```python
# SLOW — default int64 uses 8 bytes per value
df["age"] = df["age"].astype("int64")

# FAST — int8 uses 1 byte (valid for 0–127)
df["age"] = df["age"].astype("int8")

# Use category for low-cardinality string columns
df["status"] = df["status"].astype("category")
```
