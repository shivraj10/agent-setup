"""ETL pipeline scaffold — extract / transform / load pattern."""

from io import BytesIO

import pandas as pd


def extract(s3_client, key: str, bucket: str) -> pd.DataFrame:
    obj = s3_client.get_object(Bucket=bucket, Key=key)
    return pd.read_parquet(BytesIO(obj["Body"].read()))


def transform(df: pd.DataFrame) -> pd.DataFrame:
    df = df.dropna(subset=["id"])
    df["processed_at"] = pd.Timestamp.utcnow().isoformat()
    return df


def load(df: pd.DataFrame, table) -> int:
    with table.batch_writer() as batch:
        for row in df.to_dict("records"):
            batch.put_item(Item=row)
    return len(df)
